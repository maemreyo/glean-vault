---
name: typescript
description: TypeScript development with strict typing, advanced type utilities, generics, interfaces, and modern patterns. Covers type inference, conditional types, mapped types, utility types, and best practices for building type-safe applications. Use when working with .ts/.tsx files, building typed JavaScript applications, or implementing type systems.
---

# TypeScript

Type-safe JavaScript development with static typing and advanced type system features.

## Quick Start

```bash
# Initialize TypeScript project
npm init -y
npm install -D typescript @types/node ts-node

# Create tsconfig.json
npx tsc --init

# Compile TypeScript
npx tsc

# Run directly with ts-node
npx ts-node file.ts
```

## Core Type System

### Basic Types
```typescript
// Primitive types
let isDone: boolean = false;
let decimal: number = 6;
let color: string = "blue";
let list: number[] = [1, 2, 3];
let x: [string, number] = ["hello", 10];

// Object types
interface User {
  id: number;
  name: string;
  email?: string;  // Optional
  readonly createdAt: Date;  // Read-only
}

// Union types
type Status = 'pending' | 'active' | 'inactive';
type ID = string | number;

// Intersection types
type UserWithStatus = User & { status: Status };
```

### Advanced Types

```typescript
// Generic types
interface ApiResponse<T> {
  data: T;
  error?: string;
  status: number;
}

interface PaginatedResponse<T> extends ApiResponse<T[]> {
  pagination: {
    page: number;
    limit: number;
    total: number;
  };
}

// Conditional types
type NonNullable<T> = T extends null | undefined ? never : T;
type ReturnType<T> = T extends (...args: any[]) => infer R ? R : never;

// Mapped types
type PartialUser = {
  [K in keyof User]?: User[K];
};

type ReadOnlyUser = {
  readonly [K in keyof User]: User[K];
};

// Template literal types
type EventName<T extends string> = `on${Capitalize<T>}`;
type UserEvents = EventName<'login' | 'logout'>; // "onLogin" | "onLogout"
```

## Utility Types

### Built-in Utilities
```typescript
interface User {
  id: number;
  name: string;
  email: string;
  age: number;
}

// Partial<T> - All properties optional
type UserUpdate = Partial<User>;

// Required<T> - All properties required
type RequiredUser = Required<Partial<User>>;

// Pick<T, K> - Select specific properties
type UserPublic = Pick<User, 'id' | 'name'>;

// Omit<T, K> - Remove specific properties
type UserPrivate = Omit<User, 'id'>;

// Record<K, T> - Dictionary type
type UserMap = Record<string, User>;

// Exclude<T, U> - Remove types from union
type StatusWithoutPending = Exclude<Status, 'pending'>;

// Extract<T, U> - Extract types from union
type StringKeys<T> = Extract<keyof T, string>;
```

### Custom Utilities
```typescript
// Deep readonly
type DeepReadOnly<T> = {
  readonly [P in keyof T]: T[P] extends object ? DeepReadOnly<T[P]> : T[P];
};

// Branded types for nominal typing
type Brand<T, B> = T & { __brand: B };
type UserId = Brand<number, 'UserId'>;

// Type guards
function isString(value: unknown): value is string {
  return typeof value === 'string';
}

function isUser(obj: unknown): obj is User {
  return (
    typeof obj === 'object' &&
    obj !== null &&
    'id' in obj &&
    'name' in obj
  );
}
```

## Patterns & Best Practices

For comprehensive TypeScript patterns and advanced techniques, see:
- [typescript-patterns.md](resources/typescript-patterns.md)
- [typescript-advanced-types.md](resources/typescript-advanced-types.md)
- [typescript-by-framework.md](resources/typescript-by-framework.md)

## Working with Generics

### Generic Functions
```typescript
function identity<T>(arg: T): T {
  return arg;
}

// Generic constraints
interface Lengthwise {
  length: number;
}

function loggingIdentity<T extends Lengthwise>(arg: T): T {
  console.log(arg.length);
  return arg;
}

// Using key of with generics
function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] {
  return obj[key];
}
```

### Generic Classes
```typescript
class GenericNumber<T> {
  zeroValue: T;
  add: (x: T, y: T) => T;

  constructor(zero: T, addFn: (x: T, y: T) => T) {
    this.zeroValue = zero;
    this.add = addFn;
  }
}

let myGenericNumber = new GenericNumber<number>(0, (x, y) => x + y);
```

## tsconfig.json Best Practices

### Recommended Configuration
```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "lib": ["ES2022"],
    "allowJs": true,
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "strictFunctionTypes": true,
    "strictBindCallApply": true,
    "strictPropertyInitialization": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitOverride": true,
    "exactOptionalPropertyTypes": true,
    "moduleResolution": "node",
    "allowSyntheticDefaultImports": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true,
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true,
    "removeComments": false,
    "importHelpers": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist", "**/*.test.ts", "**/*.spec.ts"]
}
```

## Type-Safe APIs

### Request/Response Types
```typescript
// API request types
interface CreateUserRequest {
  name: string;
  email: string;
  password: string;
}

// API response wrapper
interface ApiSuccess<T> {
  success: true;
  data: T;
}

interface ApiError {
  success: false;
  error: {
    code: string;
    message: string;
    details?: any;
  };
}

type ApiResponse<T> = ApiSuccess<T> | ApiError;

// Type-safe API client
class ApiClient {
  async post<T>(
    endpoint: string,
    data: unknown
  ): Promise<ApiResponse<T>> {
    try {
      const response = await fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      });

      const result = await response.json();

      if (response.ok) {
        return { success: true, data: result };
      } else {
        return {
          success: false,
          error: result.error || { code: 'UNKNOWN', message: 'Unknown error' }
        };
      }
    } catch (error) {
      return {
        success: false,
        error: {
          code: 'NETWORK_ERROR',
          message: 'Network request failed'
        }
      };
    }
  }
}
```

## Type Guards and Discriminated Unions

### Discriminated Unions
```typescript
// Shape types with discriminant
interface Circle {
  kind: 'circle';
  radius: number;
}

interface Square {
  kind: 'square';
  sideLength: number;
}

type Shape = Circle | Square;

// Type guard using discriminant
function getArea(shape: Shape): number {
  switch (shape.kind) {
    case 'circle':
      return Math.PI * shape.radius ** 2;
    case 'square':
      return shape.sideLength ** 2;
    default:
      const _exhaustiveCheck: never = shape;
      return _exhaustiveCheck;
  }
}
```

### User-Defined Type Guards
```typescript
interface Cat {
  name: string;
  meow(): void;
}

interface Dog {
  name: string;
  bark(): void;
}

type Animal = Cat | Dog;

// Type guard functions
function isCat(animal: Animal): animal is Cat {
  return 'meow' in animal;
}

function makeSound(animal: Animal): void {
  if (isCat(animal)) {
    animal.meow();
  } else {
    animal.bark();
  }
}
```

## Module System

### ES Modules
```typescript
// math.ts
export function add(a: number, b: number): number {
  return a + b;
}

export const PI = 3.14159;

export interface Point {
  x: number;
  y: number;
}

// Default export
export default class Calculator {
  add(a: number, b: number): number {
    return a + b;
  }
}

// Using modules
// main.ts
import Calculator, { add, PI, Point } from './math';
import * as MathUtils from './math';
```

### Type-Only Imports/Exports
```typescript
// types.ts
export interface User {
  id: number;
  name: string;
}

// type-only import
import type { User } from './types';

// type-only export
export type { User };
```

## Declaration Files

### Writing Declaration Files
```typescript
// my-library.d.ts
export interface MyLibraryOptions {
  debug?: boolean;
  version?: string;
}

export class MyLibrary {
  constructor(options?: MyLibraryOptions);
  start(): void;
  stop(): void;
}

export function createLibrary(options?: MyLibraryOptions): MyLibrary;

// Global augmentation
declare global {
  interface Window {
    myLibrary: MyLibrary;
  }
}
```

### Using Declaration Files
```typescript
/// <reference path="path/to/declaration.d.ts" />

// Or include in tsconfig.json
{
  "include": ["src/**/*", "types/**/*"]
}
```

## Performance Considerations

### Type Performance
- Use interfaces over type aliases for object types
- Prefer generic constraints over any
- Use type predicates for complex conditions
- Avoid deep conditional types in hot paths

### Compilation Performance
```json
{
  "compilerOptions": {
    "skipLibCheck": true,
    "incremental": true,
    "tsBuildInfoFile": ".tsbuildinfo"
  }
}
```

## Common Pitfalls

### 1. Using `any` Type
```typescript
// Bad
function process(data: any) {
  return data.result;
}

// Good
interface Data {
  result: string;
}
function process(data: Data) {
  return data.result;
}
```

### 2. Type Assertion Abuse
```typescript
// Bad
const user = {} as User;

// Good
const user: User = {
  id: 1,
  name: 'John'
};
```

### 3. Optional vs Undefined Properties
```typescript
// Bad - unclear if property exists or can be undefined
interface Config {
  timeout?: number | undefined;
}

// Good
interface Config {
  timeout?: number;
}
```

## TypeScript Best Practices Checklist

- [ ] Enable strict mode in tsconfig.json
- [ ] Use interfaces for object shapes
- [ ] Prefer union types over enums
- [ ] Use type guards for runtime type checking
- [ ] Leverage utility types
- [ ] Avoid `any` - use `unknown` instead
- [ ] Use generic types for reusable code
- [ ] Document complex types with comments
- [ ] Use `readonly` for immutable data
- [ ] Implement proper error types
- [ ] Use declaration files for untyped libraries
- [ ] Configure proper module resolution

For detailed examples and patterns, see the resource files in the `resources/` directory.