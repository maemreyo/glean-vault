# TypeScript Patterns

Common patterns and idioms for effective TypeScript development.

## Design Patterns

### 1. Builder Pattern
```typescript
class QueryBuilder {
  private query: string = '';

  select(columns: string[]): this {
    this.query = `SELECT ${columns.join(', ')}`;
    return this;
  }

  from(table: string): this {
    this.query += ` FROM ${table}`;
    return this;
  }

  where(condition: string): this {
    this.query += ` WHERE ${condition}`;
    return this;
  }

  build(): string {
    return this.query;
  }
}

// Usage
const query = new QueryBuilder()
  .select(['id', 'name'])
  .from('users')
  .where('active = true')
  .build();
```

### 2. Factory Pattern
```typescript
interface DatabaseConfig {
  host: string;
  port: number;
  database: string;
}

abstract class DatabaseConnection {
  abstract connect(): Promise<void>;
  abstract disconnect(): Promise<void>;
  abstract query(sql: string): Promise<any[]>;
}

class PostgreSQLConnection extends DatabaseConnection {
  constructor(private config: DatabaseConfig) {
    super();
  }

  async connect() {
    console.log(`Connecting to PostgreSQL at ${this.config.host}`);
  }

  async disconnect() {
    console.log('Disconnecting from PostgreSQL');
  }

  async query(sql: string) {
    console.log(`Executing PostgreSQL query: ${sql}`);
    return [];
  }
}

class DatabaseFactory {
  static createConnection(type: 'postgres' | 'mysql', config: DatabaseConfig): DatabaseConnection {
    switch (type) {
      case 'postgres':
        return new PostgreSQLConnection(config);
      case 'mysql':
        throw new Error('MySQL not implemented yet');
      default:
        throw new Error(`Unsupported database type: ${type}`);
    }
  }
}
```

### 3. Repository Pattern
```typescript
interface Entity {
  id: string;
  createdAt: Date;
  updatedAt: Date;
}

interface Repository<T extends Entity> {
  create(data: Omit<T, 'id' | 'createdAt' | 'updatedAt'>): Promise<T>;
  findById(id: string): Promise<T | null>;
  findAll(): Promise<T[]>;
  update(id: string, data: Partial<T>): Promise<T>;
  delete(id: string): Promise<void>;
}

class UserRepository implements Repository<User> {
  constructor(private database: Database) {}

  async create(userData: Omit<User, 'id' | 'createdAt' | 'updatedAt'>): Promise<User> {
    const user: User = {
      ...userData,
      id: generateId(),
      createdAt: new Date(),
      updatedAt: new Date()
    };

    await this.database.users.save(user);
    return user;
  }

  async findById(id: string): Promise<User | null> {
    return await this.database.users.findById(id);
  }

  async findAll(): Promise<User[]> {
    return await this.database.users.find();
  }

  async update(id: string, userData: Partial<User>): Promise<User> {
    const existingUser = await this.findById(id);
    if (!existingUser) {
      throw new Error(`User with id ${id} not found`);
    }

    const updatedUser: User = {
      ...existingUser,
      ...userData,
      updatedAt: new Date()
    };

    await this.database.users.update(id, updatedUser);
    return updatedUser;
  }

  async delete(id: string): Promise<void> {
    await this.database.users.delete(id);
  }
}
```

### 4. Observer Pattern
```typescript
type EventHandler<T = any> = (data: T) => void;

interface EventEmitter {
  on<T>(event: string, handler: EventHandler<T>): void;
  off<T>(event: string, handler: EventHandler<T>): void;
  emit<T>(event: string, data: T): void;
}

class TypedEventEmitter implements EventEmitter {
  private handlers: Map<string, Set<EventHandler>> = new Map();

  on<T>(event: string, handler: EventHandler<T>): void {
    if (!this.handlers.has(event)) {
      this.handlers.set(event, new Set());
    }
    this.handlers.get(event)!.add(handler);
  }

  off<T>(event: string, handler: EventHandler<T>): void {
    const handlers = this.handlers.get(event);
    if (handlers) {
      handlers.delete(handler);
      if (handlers.size === 0) {
        this.handlers.delete(event);
      }
    }
  }

  emit<T>(event: string, data: T): void {
    const handlers = this.handlers.get(event);
    if (handlers) {
      handlers.forEach(handler => handler(data));
    }
  }
}

// Usage with typed events
interface UserEvents {
  'user:created': { id: string; name: string };
  'user:updated': { id: string; changes: Partial<User> };
  'user:deleted': { id: string };
}

class UserService {
  private emitter = new TypedEventEmitter();

  on<K extends keyof UserEvents>(
    event: K,
    handler: EventHandler<UserEvents[K]>
  ): void {
    this.emitter.on(event, handler);
  }

  async createUser(userData: CreateUserRequest): Promise<User> {
    const user = await this.repository.create(userData);
    this.emitter.emit('user:created', { id: user.id, name: user.name });
    return user;
  }
}
```

### 5. State Machine Pattern
```typescript
type State = 'idle' | 'loading' | 'success' | 'error';
type Event = 'fetch' | 'success' | 'error' | 'reset';

interface StateTransition {
  from: State;
  event: Event;
  to: State;
}

class StateMachine {
  private currentState: State;
  private transitions: Map<string, StateTransition[]> = new Map();

  constructor(initialState: State) {
    this.currentState = initialState;
  }

  addTransition(transition: StateTransition): void {
    const from = this.transitions.get(transition.from) || [];
    from.push(transition);
    this.transitions.set(transition.from, from);
  }

  canTransition(event: Event): boolean {
    const transitions = this.transitions.get(this.currentState) || [];
    return transitions.some(t => t.event === event);
  }

  transition(event: Event): boolean {
    const transitions = this.transitions.get(this.currentState) || [];
    const transition = transitions.find(t => t.event === event);

    if (transition) {
      this.currentState = transition.to;
      return true;
    }

    return false;
  }

  getState(): State {
    return this.currentState;
  }
}

// Usage
class DataLoader {
  private stateMachine: StateMachine;

  constructor() {
    this.stateMachine = new StateMachine('idle');

    // Define allowed transitions
    this.stateMachine.addTransition({ from: 'idle', event: 'fetch', to: 'loading' });
    this.stateMachine.addTransition({ from: 'loading', event: 'success', to: 'success' });
    this.stateMachine.addTransition({ from: 'loading', event: 'error', to: 'error' });
    this.stateMachine.addTransition({ from: 'success', event: 'fetch', to: 'loading' });
    this.stateMachine.addTransition({ from: 'error', event: 'fetch', to: 'loading' });
    this.stateMachine.addTransition({ from: 'success', event: 'reset', to: 'idle' });
    this.stateMachine.addTransition({ from: 'error', event: 'reset', to: 'idle' });
  }

  async load(): Promise<void> {
    if (!this.stateMachine.canTransition('fetch')) {
      throw new Error(`Cannot fetch data in state: ${this.stateMachine.getState()}`);
    }

    this.stateMachine.transition('fetch');

    try {
      const data = await fetchData();
      this.stateMachine.transition('success');
    } catch (error) {
      this.stateMachine.transition('error');
      throw error;
    }
  }
}
```

## Type-Safe Patterns

### 1. Branded Types
```typescript
// Brand types for nominal typing
type Brand<T, B> = T & { __brand: B };

type UserId = Brand<string, 'UserId'>;
type Email = Brand<string, 'Email'>;
type Password = Brand<string, 'Password'>;

// Factory functions
function createUserId(id: string): UserId {
  if (!id.match(/^[a-zA-Z0-9_-]+$/)) {
    throw new Error('Invalid user ID format');
  }
  return id as UserId;
}

function createEmail(email: string): Email {
  if (!email.includes('@')) {
    throw new Error('Invalid email format');
  }
  return email as Email;
}

// Usage prevents mixing up IDs
function getUserById(id: UserId): User | null {
  // Implementation
  return null;
}

// This would cause a compile error
// getUserById('some-string'); // Error: string is not assignable to UserId
getUserById(createUserId('user_123')); // OK
```

### 2. Opaque Types
```typescript
// Creating opaque types with module pattern
declare const OpaqueSymbol: unique symbol;

type Opaque<Type, Token = unknown> = Type & {
  readonly [OpaqueSymbol]: Token;
};

// Specific opaque types
type Currency = Opaque<number, 'Currency'>;
type Temperature = Opaque<number, 'Temperature'>;

// Constructor functions
function Currency(value: number): Currency {
  return value as Currency;
}

function Temperature(celsius: number): Temperature {
  return celsius as Temperature;
}

// Prevents mixing units
function addMoney(a: Currency, b: Currency): Currency {
  return Currency(a + b);
}

// This would cause an error
// addMoney(Currency(10), 20); // Error: number is not Currency
addMoney(Currency(10), Currency(20)); // OK
```

### 3. Tagged Union Types
```typescript
type Result<T, E = Error> =
  | { success: true; data: T }
  | { success: false; error: E };

// Helper functions
function success<T>(data: T): Result<T> {
  return { success: true, data };
}

function failure<E>(error: E): Result<never, E> {
  return { success: false, error };
}

// Usage
function parseJSON(json: string): Result<any, SyntaxError> {
  try {
    return success(JSON.parse(json));
  } catch (error) {
    return failure(error as SyntaxError);
  }
}

// Pattern matching
function handleResult<T>(result: Result<T>): string {
  if (result.success) {
    return `Success: ${JSON.stringify(result.data)}`;
  } else {
    return `Error: ${result.error.message}`;
  }
}
```

### 4. Singleton Pattern with Type Safety
```typescript
class Singleton<T> {
  private static instances = new Map<Function, any>();

  private constructor() {}

  static getInstance<T>(ctor: new () => T): T {
    if (!Singleton.instances.has(ctor)) {
      Singleton.instances.set(ctor, new ctor());
    }
    return Singleton.instances.get(ctor);
  }

  static clear<T>(ctor: new () => T): void {
    Singleton.instances.delete(ctor);
  }
}

// Usage
class Database {
  private connection: any = null;

  connect() {
    if (!this.connection) {
      this.connection = { /* database connection */ };
    }
    return this.connection;
  }
}

// Type-safe singleton access
const db1 = Singleton.getInstance(Database);
const db2 = Singleton.getInstance(Database);
console.log(db1 === db2); // true
```

## Functional Patterns

### 1. Pipe Function
```typescript
type PipeFunction<T> = (value: T) => T;

function pipe<T>(value: T, ...fns: PipeFunction<T>[]): T {
  return fns.reduce((acc, fn) => fn(acc), value);
}

// Generic pipe
function pipeG<T, U, V>(fn1: (x: T) => U, fn2: (x: U) => V) {
  return (x: T): V => fn2(fn1(x));
}

// Usage
const add5 = (x: number) => x + 5;
const multiplyBy2 = (x: number) => x * 2;
const toString = (x: number) => x.toString();

const result = pipe(10, add5, multiplyBy2, toString); // "30"

// Or with generic pipe
const pipe1 = pipeG(add5, multiplyBy2);
const result2 = pipe1(10); // 30
```

### 2. Currying
```typescript
function curry<T, U, V>(fn: (x: T, y: U) => V): (x: T) => (y: U) => V {
  return (x: T) => (y: U) => fn(x, y);
}

// Usage
const add = (a: number, b: number): number => a + b;
const curriedAdd = curry(add);

const add5 = curriedAdd(5);
const result = add5(3); // 8
```

### 3. Maybe Monad
```typescript
interface Maybe<T> {
  map<U>(fn: (value: T) => U): Maybe<U>;
  flatMap<U>(fn: (value: T) => Maybe<U>): Maybe<U>;
  orElse(defaultValue: T): T;
  filter(predicate: (value: T) => boolean): Maybe<T>;
  isJust(): boolean;
  isNothing(): boolean;
}

class Just<T> implements Maybe<T> {
  constructor(private value: T) {}

  map<U>(fn: (value: T) => U): Maybe<U> {
    return new Just(fn(this.value));
  }

  flatMap<U>(fn: (value: T) => Maybe<U>): Maybe<U> {
    return fn(this.value);
  }

  orElse(): T {
    return this.value;
  }

  filter(predicate: (value: T) => boolean): Maybe<T> {
    return predicate(this.value) ? this : new Nothing();
  }

  isJust(): boolean {
    return true;
  }

  isNothing(): boolean {
    return false;
  }
}

class Nothing<T> implements Maybe<T> {
  map<U>(): Maybe<U> {
    return this as unknown as Maybe<U>;
  }

  flatMap<U>(): Maybe<U> {
    return this as unknown as Maybe<U>;
  }

  orElse(defaultValue: T): T {
    return defaultValue;
  }

  filter(): Maybe<T> {
    return this;
  }

  isJust(): boolean {
    return false;
  }

  isNothing(): boolean {
    return true;
  }
}

// Helper functions
function just<T>(value: T): Maybe<T> {
  return new Just(value);
}

function nothing<T>(): Maybe<T> {
  return new Nothing<T>();
}

function fromNullable<T>(value: T | null | undefined): Maybe<T> {
  return value === null || value === undefined ? nothing<T>() : just(value);
}

// Usage
const user = fromNullable(getUserFromDatabase());
const userName = user
  .map(u => u.profile)
  .map(p => p.name)
  .orElse('Guest');
```

### 4. Either Monad for Error Handling
```typescript
type Either<L, R> = Left<L, R> | Right<L, R>;

class Left<L, R> {
  readonly value: L;

  constructor(value: L) {
    this.value = value;
  }

  isLeft(): this is Left<L, R> {
    return true;
  }

  isRight(): this is Right<L, R> {
    return false;
  }
}

class Right<L, R> {
  readonly value: R;

  constructor(value: R) {
    this.value = value;
  }

  isLeft(): this is Left<L, R> {
    return false;
  }

  isRight(): this is Right<L, R> {
    return true;
  }
}

// Helper functions
function left<L, R>(value: L): Either<L, R> {
  return new Left(value);
}

function right<L, R>(value: R): Either<L, R> {
  return new Right(value);
}

// Usage
function parseAge(input: string): Either<string, number> {
  const age = parseInt(input, 10);
  return isNaN(age) ? left('Invalid age') : right(age);
}

const result = parseAge('25');
if (result.isRight()) {
  console.log(`Age: ${result.value}`);
} else {
  console.error(`Error: ${result.value}`);
}
```

## Configuration Patterns

### 1. Type-Safe Configuration
```typescript
interface DatabaseConfig {
  host: string;
  port: number;
  database: string;
  username: string;
  password: string;
}

interface ServerConfig {
  port: number;
  host: string;
  cors: boolean;
}

interface AppConfig {
  database: DatabaseConfig;
  server: ServerConfig;
  environment: 'development' | 'staging' | 'production';
}

type ConfigKey = keyof AppConfig;

class ConfigManager {
  private config: Partial<AppConfig> = {};

  set<K extends ConfigKey>(key: K, value: AppConfig[K]): void {
    this.config[key] = value;
  }

  get<K extends ConfigKey>(key: K): AppConfig[K] {
    const value = this.config[key];
    if (value === undefined) {
      throw new Error(`Configuration key '${key}' not set`);
    }
    return value;
  }

  isSet<K extends ConfigKey>(key: K): boolean {
    return this.config[key] !== undefined;
  }

  validate(): void {
    const required: ConfigKey[] = ['database', 'server', 'environment'];
    const missing = required.filter(key => !this.isSet(key));

    if (missing.length > 0) {
      throw new Error(`Missing configuration keys: ${missing.join(', ')}`);
    }
  }
}

// Usage with environment variables
function loadConfigFromEnv(): ConfigManager {
  const config = new ConfigManager();

  config.set('server', {
    port: parseInt(process.env.PORT || '3000', 10),
    host: process.env.HOST || 'localhost',
    cors: process.env.CORS === 'true'
  });

  config.set('database', {
    host: process.env.DB_HOST || 'localhost',
    port: parseInt(process.env.DB_PORT || '5432', 10),
    database: process.env.DB_NAME || 'myapp',
    username: process.env.DB_USER || 'user',
    password: process.env.DB_PASSWORD || 'password'
  });

  config.set('environment', (process.env.NODE_ENV as any) || 'development');

  return config;
}
```

### 2. Plugin Pattern
```typescript
interface Plugin {
  name: string;
  version: string;
  install(app: Application): void;
  uninstall(app: Application): void;
}

abstract class BasePlugin implements Plugin {
  abstract name: string;
  abstract version: string;

  install(app: Application): void {
    console.log(`Installing plugin: ${this.name} v${this.version}`);
  }

  uninstall(app: Application): void {
    console.log(`Uninstalling plugin: ${this.name}`);
  }
}

interface Application {
  use(plugin: Plugin): void;
  remove(pluginName: string): void;
  getPlugin(name: string): Plugin | undefined;
}

class PluginManager implements Application {
  private plugins: Map<string, Plugin> = new Map();

  use(plugin: Plugin): void {
    if (this.plugins.has(plugin.name)) {
      throw new Error(`Plugin ${plugin.name} is already installed`);
    }

    plugin.install(this);
    this.plugins.set(plugin.name, plugin);
  }

  remove(pluginName: string): void {
    const plugin = this.plugins.get(pluginName);
    if (!plugin) {
      throw new Error(`Plugin ${pluginName} is not installed`);
    }

    plugin.uninstall(this);
    this.plugins.delete(pluginName);
  }

  getPlugin(name: string): Plugin | undefined {
    return this.plugins.get(name);
  }
}

// Usage
class LoggerPlugin extends BasePlugin {
  name = 'logger';
  version = '1.0.0';

  install(app: Application): void {
    super.install(app);
    // Initialize logger
  }

  uninstall(app: Application): void {
    super.uninstall(app);
    // Cleanup logger
  }
}

const app = new PluginManager();
app.use(new LoggerPlugin());
```

## Performance Patterns

### 1. Memoization
```typescript
function memoize<TArgs extends any[], TReturn>(
  fn: (...args: TArgs) => TReturn
): (...args: TArgs) => TReturn {
  const cache = new Map<string, TReturn>();

  return (...args: TArgs): TReturn => {
    const key = JSON.stringify(args);

    if (cache.has(key)) {
      return cache.get(key)!;
    }

    const result = fn(...args);
    cache.set(key, result);
    return result;
  };
}

// Usage with typed function
const fibonacci = memoize((n: number): number => {
  if (n < 2) return n;
  return fibonacci(n - 1) + fibonacci(n - 2);
});
```

### 2. Lazy Initialization
```typescript
class Lazy<T> {
  private value?: T;
  private initialized = false;
  private factory: () => T;

  constructor(factory: () => T) {
    this.factory = factory;
  }

  get(): T {
    if (!this.initialized) {
      this.value = this.factory();
      this.initialized = true;
    }
    return this.value!;
  }

  isInitialized(): boolean {
    return this.initialized;
  }

  reset(): void {
    this.value = undefined;
    this.initialized = false;
  }
}

// Usage
const expensiveResource = new Lazy(() => {
  console.log('Creating expensive resource...');
  return { /* expensive object */ };
});

// Resource is only created when accessed
const resource = expensiveResource.get();
```

## Anti-Patterns to Avoid

### 1. The `any` Type
```typescript
// Bad
function processData(data: any): any {
  return data.result;
}

// Good
interface Data {
  result: string;
}
function processData(data: Data): string {
  return data.result;
}

// Better - Use unknown and type guards
function processDataUnknown(data: unknown): string {
  if (typeof data === 'object' && data !== null && 'result' in data) {
    const dataObj = data as { result: unknown };
    if (typeof dataObj.result === 'string') {
      return dataObj.result;
    }
  }
  throw new Error('Invalid data format');
}
```

### 2. Type Assertions Instead of Type Guards
```typescript
// Bad
const user = response.data as User;

// Good
function isUser(obj: unknown): obj is User {
  return (
    typeof obj === 'object' &&
    obj !== null &&
    'id' in obj &&
    'name' in obj &&
    typeof (obj as User).id === 'number' &&
    typeof (obj as User).name === 'string'
  );
}

const data = response.data;
if (isUser(data)) {
  // TypeScript knows data is User here
  console.log(data.name);
}
```

### 3. Optional Properties for API Responses
```typescript
// Bad - Unclear if property can be undefined
interface User {
  id: number;
  name?: string; // Might be undefined or just optional?
}

// Good
interface User {
  id: number;
  name: string | null; // Explicitly can be null
  email?: string; // Truly optional
}

// Better - Use discriminated unions for different states
interface UserBase {
  id: number;
}

interface UserWithName extends UserBase {
  type: 'complete';
  name: string;
}

interface UserWithoutName extends UserBase {
  type: 'incomplete';
}

type User = UserWithName | UserWithoutName;
```

These patterns help you write more maintainable, type-safe TypeScript code that's easier to reason about and less prone to runtime errors.