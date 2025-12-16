# Error Patterns Catalog

A comprehensive collection of error handling patterns for various scenarios.

## 1. Validation Patterns

### Input Validation Pattern
```typescript
interface ValidationRule<T> {
  validate(value: T): ValidationResult;
  message: string;
}

type ValidationResult =
  | { valid: true }
  | { valid: false; error: string };

class Validator<T> {
  constructor(private rules: ValidationRule<T>[]) {}

  validate(value: T): ValidationResult {
    for (const rule of this.rules) {
      const result = rule.validate(value);
      if (!result.valid) {
        return { valid: false, error: rule.message };
      }
    }
    return { valid: true };
  }
}

// Usage
const emailValidator = new Validator<string>([
  {
    validate: (email) => ({ valid: !!email }),
    message: 'Email is required'
  },
  {
    validate: (email) => ({ valid: email.includes('@') }),
    message: 'Invalid email format'
  }
]);
```

### Property Validation Pattern
```typescript
type PropertyValidator<T, K extends keyof T> = {
  property: K;
  rules: ValidationRule<T[K]>[];
};

class ObjectValidator<T> {
  constructor(private validators: PropertyValidator<T, keyof T>[]) {}

  validate(obj: T): { valid: true } | { valid: false; errors: Record<string, string> } {
    const errors: Record<string, string> = {};

    for (const validator of this.validators) {
      const value = obj[validator.property];
      for (const rule of validator.rules) {
        const result = rule.validate(value);
        if (!result.valid) {
          errors[validator.property as string] = result.error;
          break;
        }
      }
    }

    return Object.keys(errors).length === 0
      ? { valid: true }
      : { valid: false, errors };
  }
}

// Usage
const userValidator = new ObjectValidator<User>([
  {
    property: 'email',
    rules: [requiredRule, emailRule]
  },
  {
    property: 'age',
    rules: [requiredRule, minAgeRule]
  }
]);
```

## 2. Resilience Patterns

### Timeout Pattern
```typescript
class TimeoutError extends Error {
  constructor(operation: string, timeout: number) {
    super(`Operation ${operation} timed out after ${timeout}ms`);
    this.name = 'TimeoutError';
  }
}

async function withTimeout<T>(
  operation: Promise<T>,
  timeoutMs: number,
  operationName: string = 'operation'
): Promise<T> {
  const timeoutPromise = new Promise<never>((_, reject) => {
    setTimeout(() => reject(new TimeoutError(operationName, timeoutMs)), timeoutMs);
  });

  return Promise.race([operation, timeoutPromise]);
}

// Usage
try {
  const result = await withTimeout(
    fetch('https://api.example.com/data'),
    5000,
    'API fetch'
  );
} catch (error) {
  if (error instanceof TimeoutError) {
    // Handle timeout
  }
}
```

### Bulkhead Pattern
```typescript
class Bulkhead {
  constructor(
    private maxConcurrent: number,
    private queueSize: number = 100
  ) {
    this.running = 0;
    this.queue = [];
  }

  async execute<T>(operation: () => Promise<T>): Promise<T> {
    return new Promise((resolve, reject) => {
      if (this.queue.length >= this.queueSize) {
        reject(new Error('Bulkhead queue full'));
        return;
      }

      this.queue.push({ resolve, reject, operation });
      this.process();
    });
  }

  private async process() {
    if (this.running >= this.maxConcurrent || this.queue.length === 0) {
      return;
    }

    this.running++;
    const { resolve, reject, operation } = this.queue.shift()!;

    try {
      const result = await operation();
      resolve(result);
    } catch (error) {
      reject(error);
    } finally {
      this.running--;
      this.process();
    }
  }
}
```

### Cache-Aside Pattern with Error Handling
```typescript
class CacheWithErrorHandling {
  constructor(
    private cache: Cache,
    private fallback: FallbackDataSource
  ) {}

  async get<T>(key: string): Promise<T> {
    try {
      // Try cache first
      const cached = await this.cache.get<T>(key);
      if (cached !== null) {
        return cached;
      }
    } catch (error) {
      console.warn(`Cache read failed for key ${key}:`, error);
    }

    try {
      // Fallback to primary source
      const data = await this.fallback.get<T>(key);

      // Try to cache for future reads
      try {
        await this.cache.set(key, data);
      } catch (cacheError) {
        console.warn(`Cache write failed for key ${key}:`, cacheError);
      }

      return data;
    } catch (error) {
      throw new Error(`Failed to retrieve data for key ${key}: ${error.message}`);
    }
  }
}
```

## 3. State Management Patterns

### State Machine Error Handling
```typescript
type State = 'idle' | 'loading' | 'success' | 'error';
type Event = 'start' | 'success' | 'error' | 'reset';

type StateTransition = {
  from: State;
  event: Event;
  to: State;
  action?: () => void;
};

class StateMachine {
  private currentState: State = 'idle';
  private error?: Error;

  constructor(private transitions: StateTransition[]) {}

  transition(event: Event, error?: Error): void {
    const transition = this.transitions.find(
      t => t.from === this.currentState && t.event === event
    );

    if (!transition) {
      throw new Error(`Invalid transition: ${this.currentState} -> ${event}`);
    }

    this.currentState = transition.to;
    if (error) {
      this.error = error;
    }

    transition.action?.();
  }

  getState() {
    return {
      state: this.currentState,
      error: this.error
    };
  }
}

// Usage
const stateMachine = new StateMachine([
  { from: 'idle', event: 'start', to: 'loading' },
  { from: 'loading', event: 'success', to: 'success' },
  { from: 'loading', event: 'error', to: 'error' },
  { from: 'error', event: 'reset', to: 'idle' }
]);
```

### Saga Pattern for Error Recovery
```typescript
type SagaStep<T> = {
  execute: () => Promise<T>;
  compensate?: (result: T) => Promise<void>;
};

class Saga {
  private compensations: Array<() => Promise<void>> = [];

  async execute<T>(steps: SagaStep<T>[]): Promise<T[]> {
    const results: T[] = [];

    try {
      for (const step of steps) {
        const result = await step.execute();
        results.push(result);

        if (step.compensate) {
          this.compensations.push(() => step.compensate!(result));
        }
      }
      return results;
    } catch (error) {
      await this.rollback();
      throw error;
    }
  }

  private async rollback(): Promise<void> {
    for (const compensation of this.compensations.reverse()) {
      try {
        await compensation();
      } catch (rollbackError) {
        console.error('Rollback failed:', rollbackError);
      }
    }
    this.compensations = [];
  }
}

// Usage
const saga = new Saga();

const orderId = await saga.execute([
  {
    execute: () => createOrder(orderData),
    compensate: (result) => deleteOrder(result.id)
  },
  {
    execute: (previous) => processPayment(previous.id),
    compensate: (result) => refundPayment(result.id)
  },
  {
    execute: (previous) => sendConfirmationEmail(previous.email)
  }
]);
```

## 4. API Error Patterns

### GraphQL Error Handling
```typescript
interface GraphQLError {
  message: string;
  path?: (string | number)[];
  extensions?: Record<string, any>;
}

class GraphQLErrorHandler {
  formatError(error: GraphQLError): GraphQLError {
    // Don't expose internal errors
    if (error.extensions?.code === 'INTERNAL_ERROR') {
      return {
        message: 'Internal server error',
        extensions: { code: 'INTERNAL_ERROR' }
      };
    }

    return {
      message: error.message,
      path: error.path,
      extensions: error.extensions
    };
  }

  handleErrors(errors: GraphQLError[]): GraphQLError[] {
    return errors.map(error => this.formatError(error));
  }
}
```

### REST API Error Response
```typescript
interface ApiError {
  error: {
    code: string;
    message: string;
    details?: any;
    timestamp: string;
    requestId?: string;
  };
}

class ApiErrorBuilder {
  static create(
    code: string,
    message: string,
    details?: any,
    requestId?: string
  ): ApiError {
    return {
      error: {
        code,
        message,
        details,
        timestamp: new Date().toISOString(),
        requestId
      }
    };
  }

  static notFound(resource: string, id?: string): ApiError {
    return this.create(
      'NOT_FOUND',
      `${resource}${id ? ` with id ${id}` : ''} not found`
    );
  }

  static validation(errors: Record<string, string[]>): ApiError {
    return this.create(
      'VALIDATION_ERROR',
      'Validation failed',
      { fields: errors }
    );
  }

  static internal(error: Error, requestId?: string): ApiError {
    return this.create(
      'INTERNAL_ERROR',
      'An internal error occurred',
      process.env.NODE_ENV === 'development' ? { stack: error.stack } : undefined,
      requestId
    );
  }
}
```

## 5. Database Error Patterns

### Transaction with Rollback
```typescript
class TransactionManager {
  async execute<T>(
    operations: Array<() => Promise<T>>
  ): Promise<T[]> {
    const transaction = await this.beginTransaction();
    const results: T[] = [];

    try {
      for (const operation of operations) {
        const result = await operation();
        results.push(result);
      }

      await transaction.commit();
      return results;
    } catch (error) {
      await transaction.rollback();
      throw new DatabaseTransactionError(
        'Transaction failed, rolled back',
        error
      );
    }
  }
}

// Usage
const transactionManager = new TransactionManager();

const [user, order] = await transactionManager.execute([
  () => db.users.create(userData),
  () => db.orders.create(orderData)
]);
```

### Optimistic Locking with Retry
```typescript
class OptimisticLockError extends Error {
  constructor(message: string, public retryCount: number) {
    super(message);
    this.name = 'OptimisticLockError';
  }
}

async function updateWithOptimisticLock<T>(
  repository: Repository<T>,
  id: string,
  updateFn: (entity: T) => T,
  maxRetries: number = 3
): Promise<T> {
  let retryCount = 0;

  while (retryCount < maxRetries) {
    try {
      const entity = await repository.findById(id);
      if (!entity) {
        throw new Error(`Entity with id ${id} not found`);
      }

      const updated = updateFn(entity);
      return await repository.update(id, updated);
    } catch (error) {
      if (error.code === 'OPTIMISTIC_LOCK' && retryCount < maxRetries - 1) {
        retryCount++;
        await delay(100 * Math.pow(2, retryCount)); // Exponential backoff
        continue;
      }
      throw error;
    }
  }

  throw new OptimisticLockError(
    `Failed to update after ${maxRetries} attempts`,
    maxRetries
  );
}
```

## 6. Stream Processing Patterns

### Stream Error Handling
```typescript
class StreamProcessor<T, R> {
  constructor(
    private transform: (item: T) => Promise<R>,
    private errorHandler: (error: Error, item: T) => Promise<R | null>
  ) {}

  async process(stream: AsyncIterable<T>): Promise<R[]> {
    const results: R[] = [];

    for await (const item of stream) {
      try {
        const result = await this.transform(item);
        results.push(result);
      } catch (error) {
        console.error(`Failed to process item:`, error);

        const fallback = await this.errorHandler(error, item);
        if (fallback !== null) {
          results.push(fallback);
        }
      }
    }

    return results;
  }
}

// Usage
const processor = new StreamProcessor(
  async (data) => processData(data),
  async (error, data) => {
    // Try alternative processing
    return await processFallback(data);
  }
);
```

### Batch Processing with Error Collection
```typescript
class BatchProcessor<T> {
  constructor(
    private batchSize: number,
    private processItem: (item: T) => Promise<void>
  ) {}

  async process(items: T[]): Promise<{
    processed: number;
    errors: Array<{ item: T; error: Error }>;
  }> {
    const errors: Array<{ item: T; error: Error }> = [];
    let processed = 0;

    for (let i = 0; i < items.length; i += this.batchSize) {
      const batch = items.slice(i, i + this.batchSize);

      await Promise.allSettled(
        batch.map(async (item) => {
          try {
            await this.processItem(item);
            processed++;
          } catch (error) {
            errors.push({ item, error: error as Error });
          }
        })
      );
    }

    return { processed, errors };
  }
}
```

## 7. Async Error Patterns

### Promise Chain Error Handling
```typescript
class PromiseChain {
  private operations: Array<() => Promise<any>> = [];

  then<T>(operation: () => Promise<T>): PromiseChain {
    this.operations.push(operation);
    return this;
  }

  catch<T>(errorHandler: (error: Error) => Promise<T>): PromiseChain {
    this.operations.push(async () => {
      try {
        return await this.operations.pop()!();
      } catch (error) {
        return await errorHandler(error as Error);
      }
    });
    return this;
  }

  async execute(): Promise<any> {
    let result: any;

    for (const operation of this.operations) {
      result = await operation();
    }

    return result;
  }
}

// Usage
const result = await new PromiseChain()
  .then(() => fetchData())
  .then(data => processData(data))
  .catch(error => handleDataError(error))
  .then(processed => saveData(processed))
  .execute();
```

### Async Error Accumulator
```typescript
class AsyncErrorAccumulator {
  private errors: Error[] = [];

  async execute<T>(operations: Array<() => Promise<T>>): Promise<{
    results: T[];
    errors: Error[];
  }> {
    const results = await Promise.allSettled(operations);

    const successful: T[] = [];
    const failed: Error[] = [];

    results.forEach((result, index) => {
      if (result.status === 'fulfilled') {
        successful.push(result.value);
      } else {
        failed.push(result.reason);
        this.errors.push(result.reason);
      }
    });

    return { results: successful, errors: failed };
  }

  hasErrors(): boolean {
    return this.errors.length > 0;
  }

  getErrors(): Error[] {
    return [...this.errors];
  }
}
```

## 8. Resource Management Patterns

### Resource Cleanup Pattern
```typescript
class ResourceManager {
  private resources: Array<() => Promise<void>> = [];

  register<T extends { dispose(): Promise<void> }>(resource: T): T {
    this.resources.push(() => resource.dispose());
    return resource;
  }

  registerSync<T extends { dispose(): void }>(resource: T): T {
    this.resources.push(() => Promise.resolve(resource.dispose()));
    return resource;
  }

  async dispose(): Promise<void> {
    const errors: Error[] = [];

    for (const cleanup of this.resources.reverse()) {
      try {
        await cleanup();
      } catch (error) {
        errors.push(error as Error);
      }
    }

    this.resources = [];

    if (errors.length > 0) {
      throw new Error(
        `Resource cleanup failed: ${errors.map(e => e.message).join(', ')}`
      );
    }
  }
}

// Usage
const manager = new ResourceManager();

const connection = manager.register(await createConnection());
const file = manager.registerSync(openFile('data.txt'));

try {
  // Use resources
  await processFile(file, connection);
} finally {
  await manager.dispose();
}
```

### Connection Pool with Error Recovery
```typescript
class ConnectionPool {
  private connections: Connection[] = [];
  private failed = false;

  constructor(
    private factory: () => Promise<Connection>,
    private maxSize: number = 10,
    private healthCheckInterval: number = 30000
  ) {}

  async acquire(): Promise<Connection> {
    if (this.failed) {
      throw new Error('Connection pool is failed');
    }

    if (this.connections.length > 0) {
      return this.connections.pop()!;
    }

    try {
      return await this.factory();
    } catch (error) {
      this.failed = true;
      throw new Error(`Failed to create connection: ${error.message}`);
    }
  }

  release(connection: Connection): void {
    if (this.failed || !connection.isHealthy()) {
      connection.close();
      return;
    }

    if (this.connections.length < this.maxSize) {
      this.connections.push(connection);
    } else {
      connection.close();
    }
  }

  async recover(): Promise<void> {
    this.failed = false;

    // Close all existing connections
    for (const connection of this.connections) {
      connection.close();
    }
    this.connections = [];
  }
}
```

## 9. Security Error Patterns

### Rate Limiting Error Handler
```typescript
class RateLimitError extends Error {
  constructor(
    message: string,
    public retryAfter: number,
    public limit: number
  ) {
    super(message);
    this.name = 'RateLimitError';
  }
}

class RateLimitHandler {
  private requests = new Map<string, number[]>();

  checkLimit(
    identifier: string,
    limit: number,
    windowMs: number
  ): void {
    const now = Date.now();
    const requests = this.requests.get(identifier) || [];

    // Remove old requests
    const validRequests = requests.filter(
      time => now - time < windowMs
    );

    if (validRequests.length >= limit) {
      throw new RateLimitError(
        `Rate limit exceeded for ${identifier}`,
        windowMs,
        limit
      );
    }

    validRequests.push(now);
    this.requests.set(identifier, validRequests);
  }
}
```

### Security Error Sanitization
```typescript
class SecurityErrorSanitizer {
  static sanitize(error: Error): Error {
    // Check for sensitive patterns
    const sensitivePatterns = [
      /password/i,
      /secret/i,
      /token/i,
      /key/i,
      /credential/i
    ];

    const message = error.message;
    const stack = error.stack;

    // Remove sensitive information from message
    let sanitizedMessage = message;
    for (const pattern of sensitivePatterns) {
      sanitizedMessage = sanitizedMessage.replace(
        new RegExp(`(${pattern.source}["'\\s]*[:=]["'\\s]*)([^"\\s\\}]*)`, 'gi'),
        '$1***'
      );
    }

    // Remove file paths from stack in production
    const sanitizedStack = process.env.NODE_ENV === 'production'
      ? stack?.replace(/\/.*?\/([^\/]+\.js:\d+:\d+)/g, '$1')
      : stack;

    const sanitizedError = new Error(sanitizedMessage);
    sanitizedError.name = error.name;
    sanitizedError.stack = sanitizedStack;

    return sanitizedError;
  }
}