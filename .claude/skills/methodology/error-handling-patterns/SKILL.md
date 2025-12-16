---
name: error-handling-patterns
description: Comprehensive error handling strategies for robust applications. Use when implementing error boundaries, validation layers, retry mechanisms, fallback strategies, or error reporting systems. Covers try-catch patterns, error propagation, graceful degradation, and user experience during failures.
---

# Error Handling Patterns

Robust error handling strategies that fail gracefully and recover intelligently.

## Quick Start

```javascript
// Universal error handling template
try {
  const result = await operation();
  return { success: true, data: result };
} catch (error) {
  // 1. Log with context
  logger.error(operation.name, { error, context });

  // 2. Handle specific error types
  if (error.code === 'ENOTFOUND') {
    return { success: false, error: 'Service unavailable', retry: true };
  }

  // 3. Return user-friendly response
  return { success: false, error: 'Operation failed' };
}
```

## Error Handling Principles

### 1. Fail Fast, Fail Loud
```javascript
// Bad: Silent failure
function getUser(id) {
  const user = db.find(id);
  return user.name; // Crashes if user is null
}

// Good: Explicit error
function getUser(id) {
  const user = db.find(id);
  if (!user) {
    throw new Error(`User ${id} not found`);
  }
  return user.name;
}
```

### 2. Preserve Context
```javascript
class OrderProcessor {
  async processOrder(orderId) {
    try {
      const order = await this.fetchOrder(orderId);
      return await this.validateOrder(order);
    } catch (error) {
      // Preserve full context for debugging
      throw new Error(`Failed to process order ${orderId}: ${error.message}`, {
        cause: error,
        orderId,
        timestamp: new Date().toISOString()
      });
    }
  }
}
```

### 3. Handle at Appropriate Layer

| Layer | Responsibility | Example |
|-------|----------------|---------|
| **Database** | Data integrity | Unique constraint violations |
| **Service** | Business logic | Invalid business rules |
| **API** | Protocol concerns | Malformed requests |
| **UI** | User experience | Friendly error messages |

## Core Patterns

### 1. Result Type Pattern
```typescript
type Result<T, E = Error> =
  | { success: true; data: T }
  | { success: false; error: E };

// Usage eliminates try-catch chains
function parseJSON(json: string): Result<any> {
  try {
    return { success: true, data: JSON.parse(json) };
  } catch (error) {
    return { success: false, error: error as Error };
  }
}

// Chain operations safely
const result = parseJSON(input)
  .flatMap(validateData)
  .flatMap(transformData);
```

### 2. Error Boundary Pattern
```typescript
// React Error Boundary
class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true };
  }

  componentDidCatch(error, errorInfo) {
    this.props.onError(error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return this.props.fallback || <ErrorFallback />;
    }
    return this.props.children;
  }
}
```

### 3. Circuit Breaker Pattern
```typescript
class CircuitBreaker {
  constructor(
    private threshold = 5,
    private timeout = 60000
  ) {
    this.failureCount = 0;
    this.lastFailureTime = null;
    this.state = 'CLOSED'; // CLOSED, OPEN, HALF_OPEN
  }

  async execute(operation) {
    if (this.state === 'OPEN') {
      if (Date.now() - this.lastFailureTime > this.timeout) {
        this.state = 'HALF_OPEN';
      } else {
        throw new Error('Circuit breaker is OPEN');
      }
    }

    try {
      const result = await operation();
      this.onSuccess();
      return result;
    } catch (error) {
      this.onFailure();
      throw error;
    }
  }

  private onSuccess() {
    this.failureCount = 0;
    this.state = 'CLOSED';
  }

  private onFailure() {
    this.failureCount++;
    this.lastFailureTime = Date.now();
    if (this.failureCount >= this.threshold) {
      this.state = 'OPEN';
    }
  }
}
```

## Specific Error Types

### Validation Errors
```typescript
class ValidationError extends Error {
  constructor(
    message: string,
    public field?: string,
    public value?: any
  ) {
    super(message);
    this.name = 'ValidationError';
  }
}

// Usage
function validateUser(user: User) {
  if (!user.email.includes('@')) {
    throw new ValidationError('Invalid email format', 'email', user.email);
  }
}
```

### Network Errors
```typescript
class NetworkError extends Error {
  constructor(
    message: string,
    public statusCode?: number,
    public retryable: boolean = false
  ) {
    super(message);
    this.name = 'NetworkError';
  }
}

// Usage
async function fetchWithRetry(url: string, maxRetries = 3) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      const response = await fetch(url);
      if (!response.ok) {
        throw new NetworkError(
          `HTTP ${response.status}`,
          response.status,
          response.status >= 500
        );
      }
      return await response.json();
    } catch (error) {
      if (error instanceof NetworkError && error.retryable && i < maxRetries - 1) {
        await delay(1000 * Math.pow(2, i)); // Exponential backoff
        continue;
      }
      throw error;
    }
  }
}
```

### Database Errors
```typescript
class DatabaseError extends Error {
  constructor(
    message: string,
    public query?: string,
    public code?: string
  ) {
    super(message);
    this.name = 'DatabaseError';
  }
}

// Usage
async function queryDatabase(sql: string, params: any[]) {
  try {
    return await db.query(sql, params);
  } catch (error) {
    if (error.code === '23505') {
      throw new DatabaseError('Duplicate entry', sql, error.code);
    }
    throw new DatabaseError(error.message, sql, error.code);
  }
}
```

## Error Recovery Strategies

### Retry with Exponential Backoff
```typescript
async function retry<T>(
  operation: () => Promise<T>,
  maxAttempts = 3,
  baseDelay = 1000
): Promise<T> {
  let lastError: Error;

  for (let attempt = 1; attempt <= maxAttempts; attempt++) {
    try {
      return await operation();
    } catch (error) {
      lastError = error;

      if (attempt === maxAttempts) {
        throw error;
      }

      const delay = baseDelay * Math.pow(2, attempt - 1);
      await new Promise(resolve => setTimeout(resolve, delay));
    }
  }

  throw lastError!;
}
```

### Fallback Pattern
```typescript
class FallbackCache {
  constructor(private primary: DataService, private fallback: DataService) {}

  async getData(key: string) {
    try {
      return await this.primary.getData(key);
    } catch (error) {
      logger.warn('Primary service failed, using fallback', { key, error });
      return await this.fallback.getData(key);
    }
  }
}
```

### Graceful Degradation
```typescript
function renderUserProfile(user: User) {
  return (
    <div>
      <h2>{user.name}</h2>
      {user.avatar ? (
        <img src={user.avatar} alt={user.name} />
      ) : (
        <div className="avatar-placeholder" /> // Fallback UI
      )}
      {user.email && (
        <p>{user.email}</p>
      )}
    </div>
  );
}
```

For comprehensive error handling patterns and language-specific implementations, see:
- [error-patterns-catalog.md](resources/error-patterns-catalog.md)
- [error-handling-by-language.md](resources/error-handling-by-language.md)

## Error Logging and Monitoring

### Structured Error Logging
```typescript
interface ErrorContext {
  userId?: string;
  requestId?: string;
  operation?: string;
  metadata?: Record<string, any>;
}

class ErrorLogger {
  error(message: string, error: Error, context?: ErrorContext) {
    const logEntry = {
      timestamp: new Date().toISOString(),
      level: 'ERROR',
      message,
      error: {
        name: error.name,
        message: error.message,
        stack: error.stack
      },
      context
    };

    this.writeLog(logEntry);
  }

  private writeLog(entry: any) {
    // Send to logging service
    if (process.env.NODE_ENV === 'production') {
      this.sendToRemoteLogger(entry);
    } else {
      console.error(JSON.stringify(entry, null, 2));
    }
  }
}
```

### Error Reporting
```typescript
class ErrorReporter {
  async report(error: Error, context?: ErrorContext) {
    const report = {
      error: {
        name: error.name,
        message: error.message,
        stack: error.stack
      },
      context,
      environment: process.env.NODE_ENV,
      timestamp: new Date().toISOString()
    };

    try {
      await fetch('https://error-reporting-service.com/api/errors', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(report)
      });
    } catch (reportingError) {
      console.error('Failed to report error:', reportingError);
    }
  }
}
```

## Error Handling Best Practices

### DO ✅
- Handle errors at appropriate abstraction levels
- Provide meaningful error messages
- Include context for debugging
- Implement recovery mechanisms
- Log errors with sufficient detail
- Use typed errors when possible
- Implement circuit breakers for external services

### DON'T ❌
- Silently swallow errors
- Expose internal error details to users
- Use exceptions for control flow
- Log sensitive information
- Return null instead of proper error handling
- Ignore error boundaries in UI
- Skip error handling in async operations

## Error Handling Checklist

### Before Implementation
- [ ] Identify all possible error conditions
- [ ] Define error types and categories
- [ ] Plan error recovery strategies
- [ ] Design error logging format

### During Implementation
- [ ] Use consistent error types
- [ ] Include relevant context
- [ ] Implement proper error propagation
- [ ] Add user-friendly error messages
- [ ] Set up error logging and monitoring

### After Implementation
- [ ] Test error scenarios
- [ ] Verify error recovery works
- [ ] Check logging in production
- [ ] Review error rates
- [ ] Update documentation