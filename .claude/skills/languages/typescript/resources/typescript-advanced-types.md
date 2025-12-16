# Advanced TypeScript Types

Deep dive into TypeScript's advanced type system features and patterns.

## Conditional Types

### Basic Conditional Types
```typescript
// T extends U ? X : Y
type IsString<T> = T extends string ? true : false;

type Test1 = IsString<string>; // true
type Test2 = IsString<number>; // false

// Practical example
type NonNullable<T> = T extends null | undefined ? never : T;

type Test3 = NonNullable<string | null>; // string
type Test4 = NonNullable<string | undefined>; // string
type Test5 = NonNullable<string | null | undefined>; // string
```

### Conditional Type Constraints
```typescript
// Using conditional types with generics
type TypeName<T> =
  T extends string ? 'string' :
  T extends number ? 'number' :
  T extends boolean ? 'boolean' :
  T extends undefined ? 'undefined' :
  T extends Function ? 'function' :
  'object';

type T1 = TypeName<string>; // 'string'
type T2 = TypeName<() => void>; // 'function'
type T3 = TypeName<string[]>; // 'object'
```

### Distributive Conditional Types
```typescript
// Conditional types are distributive over union types
type ToArray<T> = T extends any ? T[] : never;

type T1 = ToArray<string | number>; // string[] | number[]

// Example: Extracting array element types
type ArrayElement<T> = T extends (infer U)[] ? U : never;

type T2 = ArrayElement<string[]>; // string
type T3 = ArrayElement<number[]>; // number
type T4 = ArrayElement<(string | number)[]>; // string | number
```

## Mapped Types

### Basic Mapped Types
```typescript
type OptionsFlags<T> = {
  [K in keyof T]: boolean;
};

interface FeatureFlags {
  darkMode: boolean;
  notifications: boolean;
  experimentalFeatures: boolean;
}

type FeatureOptions = OptionsFlags<FeatureFlags>;
// {
//   darkMode: boolean;
//   notifications: boolean;
//   experimentalFeatures: boolean;
// }
```

### Mapped Type Modifiers
```typescript
// Making all properties optional
type Partial<T> = {
  [P in keyof T]?: T[P];
};

// Making all properties required
type Required<T> = {
  [P in keyof T]-?: T[P];
};

// Making all properties readonly
type Readonly<T> = {
  readonly [P in keyof T]: T[P];
};

// Removing readonly modifier
type Mutable<T> = {
  -readonly [P in keyof T]: T[P];
};
```

### Advanced Mapped Types
```typescript
// Deep readonly
type DeepReadonly<T> = {
  readonly [P in keyof T]: T[P] extends object ? DeepReadonly<T[P]> : T[P];
};

interface Nested {
  a: {
    b: {
      c: number;
    };
  };
}

type T1 = DeepReadonly<Nested>;
// {
//   readonly a: {
//     readonly b: {
//       readonly c: number;
//     };
//   };
// }

// Mapping to different types
type StringifyProperties<T> = {
  [K in keyof T]: T[K] extends string ? T[K] : `${T[K]}`;
};

interface Config {
  timeout: number;
  retries: number;
  endpoint: string;
}

type T2 = StringifyProperties<Config>;
// {
//   timeout: "0" | "1" | "2" | ... (string representation of number)
//   retries: "0" | "1" | "2" | ...
//   endpoint: string
// }
```

## Template Literal Types

### Basic Template Literals
```typescript
type EventName<T extends string> = `on${Capitalize<T>}`;

type T1 = EventName<'click'>; // 'onClick'
type T2 = EventName<'hover'>; // 'onHover'

// Combining template literals
type Greeting<T extends string> = `Hello, ${T}!`;

type T3 = Greeting<'World'>; // 'Hello, World!'
type T4 = Greeting<'TypeScript'>; // 'Hello, TypeScript!'
```

### Advanced Template Literals
```typescript
// Building CSS-in-JS types
type CSSProperties = {
  [K in keyof CSSDeclaration as K extends string
    ? K extends `Webkit${infer Rest}`
      ? `-${Lowercase<Rest>}`
      : K extends `Moz${infer Rest}`
      ? `-${Lowercase<Rest>}`
      : K
    : never]: CSSDeclaration[K];
};

// Router path types
type RouteParams<Path extends string> = Path extends `${string}:${infer Param}/${infer Rest}`
  ? { [K in Param | keyof RouteParams<`/${Rest}`>]: string }
  : Path extends `${string}:${infer Param}`
  ? { [K in Param]: string }
  : {};

type T1 = RouteParams<'/users/:id/posts/:postId'>;
// { id: string; postId: string }
```

### String Manipulation Types
```typescript
// Uppercase and lowercase
type T1 = Uppercase<'hello'>; // 'HELLO'
type T2 = Lowercase<'WORLD'>; // 'world'

// Capitalize and Uncapitalize
type T3 = Capitalize<'hello'>; // 'Hello'
type T4 = Uncapitalize<'WORLD'>; // 'wORLD'

// Using in conditional types
type FirstCharToUpper<T extends string> =
  T extends `${infer First}${infer Rest}`
    ? `${Uppercase<First>}${Rest}`
    : T;

type T5 = FirstCharToUpper<'hello world'>; // 'Hello world'
```

## Type Inferrence

### Infer with Conditional Types
```typescript
// Infer return type
type ReturnType<T> = T extends (...args: any[]) => infer R ? R : never;

type T1 = ReturnType<() => string>; // string
type T2 = ReturnType<(x: number) => boolean>; // boolean

// Infer parameter types
type FirstParameter<T> = T extends (first: infer P, ...args: any[]) => any ? P : never;

type T3 = FirstParameter<(x: number, y: string) => void>; // number
type T4 = FirstParameter<() => void>; // unknown (no parameter)

// Infer array element type
type ArrayElement<T> = T extends (infer U)[] ? U : never;
type T5 = ArrayElement<string[]>; // string
type T6 = ArrayElement<Array<number>>; // number

// Infer promise value type
type UnpackPromise<T> = T extends Promise<infer U> ? U : never;
type T7 = UnpackPromise<string>; // string
type T8 = UnpackPromise<number>; // number
type T9 = UnpackPromise<string>; // string
type T10 = UnpackPromise<Promise<boolean>>; // boolean
```

### Advanced Infer Patterns
```typescript
// Flatten nested tuples
type Flatten<T extends readonly unknown[]> = T extends readonly [infer Head, ...infer Tail]
  ? Head extends readonly unknown[]
    ? [...Flatten<Head>, ...Flatten<Tail>]
    : [Head, ...Flatten<Tail>]
  : [];

type T1 = Flatten<[1, [2, [3, 4]], 5]>; // [1, 2, 3, 4, 5]

// Get function parameter types as tuple
type Parameters<T> = T extends (...args: infer P) => any ? P : never;
type T2 = Parameters<(x: number, y: string) => void>; // [number, string]

// Extract object keys matching certain value type
type KeysOfType<T, U> = {
  [K in keyof T]: T[K] extends U ? K : never
}[keyof T];

interface User {
  id: number;
  name: string;
  email: string;
  age: number;
}

type StringKeys = KeysOfType<User, string>; // 'name' | 'email'
type NumberKeys = KeysOfType<User, number>; // 'id' | 'age'
```

## Recursive Types

### Basic Recursive Types
```typescript
// JSON type definition
type JSONValue =
  | string
  | number
  | boolean
  | null
  | JSONValue[]
  | { [key: string]: JSONValue };

// Deep partial type
type DeepPartial<T> = {
  [P in keyof T]?: T[P] extends object ? DeepPartial<T[P]> : T[P];
};

// Deep required type
type DeepRequired<T> = {
  [P in keyof T]-?: T[P] extends object ? DeepRequired<T[P]> : T[P];
};

interface Nested {
  a?: {
    b?: {
      c?: string;
    };
  };
}

type T1 = DeepPartial<Nested>;
// All properties become optional

type T2 = DeepRequired<Partial<Nested>>;
// All properties become required (if they exist)
```

### Advanced Recursive Types
```typescript
// Type to get all paths in an object
type Paths<T, Prefix extends string = ''> = T extends object
  ? {
      [K in keyof T]: K extends string
        ? T[K] extends object
          ? Paths<T[K], `${Prefix}${K}.`> | `${Prefix}${K}`
          : `${Prefix}${K}`
        : never;
    }[keyof T]
  : never;

interface User {
  id: number;
  profile: {
    name: string;
    address: {
      street: string;
      city: string;
    };
  };
}

type UserPaths = Paths<User>;
// 'id' | 'profile' | 'profile.name' | 'profile.address' | 'profile.address.street' | 'profile.address.city'

// Type-safe path getter
type Get<T, Path extends string> = Path extends keyof T
  ? T[Path]
  : Path extends `${infer Key}.${infer Rest}`
  ? Key extends keyof T
    ? Get<T[Key], Rest>
    : never
  : never;

function get<T, P extends Paths<T>>(obj: T, path: P): Get<T, P> {
  return path.split('.').reduce((o, k) => o[k], obj as any);
}

const user: User = {
  id: 1,
  profile: {
    name: 'John',
    address: {
      street: '123 Main St',
      city: 'New York'
    }
  }
};

const name = get(user, 'profile.name'); // string
const city = get(user, 'profile.address.city'); // string
```

## Utility Type Patterns

### 1. Branded Types for Safety
```typescript
// Brand types for nominal typing
type Brand<T, B> = T & { __brand: B };

type UserId = Brand<string, 'UserId'>;
type Email = Brand<string, 'Email'>;
type Password = Brand<string, 'Password'>;

type SafeId<T> = T & { readonly __symbol: unique symbol };

// Type-safe constructors
function createId<T>(value: string): Brand<string, T> {
  if (!value.match(/^[a-zA-Z0-9_-]+$/)) {
    throw new Error('Invalid ID format');
  }
  return value as Brand<string, T>;
}

const userId = createId<'UserId'>('user_123');
const postId = createId<'PostId'>('post_456');

// These would cause compile errors:
// userId === postId // Error: different types
```

### 2. Omit and Pick Variants
```typescript
// OmitDeep - recursively omit properties
type OmitDeep<T, K extends string> = {
  [P in keyof T as P extends K ? never : P]: T[P] extends object
    ? OmitDeep<T[P], K>
    : T[P];
};

// PickDeep - recursively pick properties
type PickDeep<T, K extends string> = {
  [P in keyof T]: P extends K
    ? T[P] extends object
      ? PickDeep<T[P], K>
      : T[P]
    : never;
};

// StrictOmit - only omit from immediate level
type StrictOmit<T, K extends keyof T> = {
  [P in keyof T as P extends K ? never : P]: T[P];
};

// StrictPick - only pick from immediate level
type StrictPick<T, K extends keyof T> = {
  [P in K]: T[P];
};
```

### 3. Function Type Utilities
```typescript
// Curry function types
type Curry<T> = T extends (...args: infer A) => infer R
  ? A extends [infer First, ...infer Rest]
    ? (arg: First) => Curry<(...args: Rest) => R>
    : () => R
  : never;

type CurriedAdd = Curry<(a: number, b: number, c: number) => number>;
// (a: number) => (b: number) => (c: number) => number

// Flip function argument order
type Flip<T> = T extends (...args: infer A) => infer R
  ? A extends [infer First, infer Second, ...infer Rest]
    ? (...args: [Second, First, ...Rest]) => R
    : never
  : never;

type Flipped = Flip<(a: number, b: string) => void>;
// (b: string, a: number) => void

// Promisify function type
type Promisify<T> = T extends (...args: infer A) => infer R
  ? (...args: A) => Promise<R>
  : never;

type AsyncAdd = Promisify<(a: number, b: number) => number>;
// (a: number, b: number) => Promise<number>
```

### 4. Collection Type Utilities
```typescript
// Join arrays
type Join<T extends readonly unknown[], D extends string> =
  T extends readonly []
    ? ''
    : T extends readonly [infer F]
    ? `${F & string}`
    : T extends readonly [infer F, ...infer R]
    ? `${F & string}${D}${Join<R, D>}`
    : string;

type T1 = Join<[1, 2, 3], ', '>; // '1, 2, 3'

// Split string
type Split<S extends string, D extends string> =
  S extends `${infer T}${D}${infer U}`
    ? [T, ...Split<U, D>]
    : [S];

type T2 = Split<'a,b,c', ','>; // ['a', 'b', 'c']

// Array to union
type ArrayToUnion<T extends readonly unknown[]> = T[number];
type T3 = ArrayToUnion<[string, number, boolean]>; // string | number | boolean

// Union to array
type UnionToArray<T> = T extends never
  ? []
  : [T, ...UnionToArray<Exclude<T, T>>]; // This doesn't work perfectly, but shows concept
```

## Complex Real-World Examples

### 1. Type-Safe HTTP Client
```typescript
type HTTPMethod = 'GET' | 'POST' | 'PUT' | 'DELETE' | 'PATCH';

type Endpoint<Path extends string> = Path extends `${infer _}${string}`
  ? Path
  : never;

interface RouteDefinition {
  path: string;
  method: HTTPMethod;
  response: unknown;
  request?: unknown;
}

type RouteTypes<T extends RouteDefinition> = {
  [K in keyof T]: {
    path: T[K]['path'];
    method: T[K]['method'];
    response: T[K]['response'];
    request: T[K]['request'];
  };
};

// Extract route parameters
type RouteParams<Path extends string> =
  Path extends `${string}:${infer Param}/${infer Rest}`
    ? { [K in Param | keyof RouteParams<`/${Rest}>]?: string }
    : Path extends `${string}:${infer Param}`
    ? { [K in Param]?: string }
    : {};

// Example API routes
const apiRoutes = {
  getUser: {
    path: '/users/:id',
    method: 'GET' as const,
    response: { id: number, name: string } as const
  },
  createUser: {
    path: '/users',
    method: 'POST' as const,
    request: { name: string; email: string } as const,
    response: { id: number; name: string; email: string } as const
  }
} as const;

type ApiRoutes = RouteTypes<typeof apiRoutes>;

// Type-safe API client
class TypedClient {
  async get<K extends keyof ApiRoutes>(
    route: K,
    params: RouteParams<ApiRoutes[K]['path']>
  ): Promise<ApiRoutes[K]['response']> {
    // Implementation with type safety
    return {} as any;
  }

  async post<K extends keyof ApiRoutes>(
    route: K,
    data: ApiRoutes[K]['request'],
    params: RouteParams<ApiRoutes[K]['path']>
  ): Promise<ApiRoutes[K]['response']> {
    // Implementation with type safety
    return {} as any;
  }
}
```

### 2. Type-Safe State Machine
```typescript
type State = string;
type Event = string;
type Transition = {
  from: State;
  event: Event;
  to: State;
};

type StateMachineConfig<T extends Transition> = {
  initial: T['from'];
  states: {
    [K in T['from']]: {
      on: {
        [L in T extends { from: K } ? T['event'] : never]: T extends { from: K; event: L }
          ? T['to']
          : never;
      };
    };
  };
};

// Example usage
type UserTransitions =
  | { from: 'idle'; event: 'login'; to: 'authenticated' }
  | { from: 'authenticated'; event: 'logout'; to: 'idle' }
  | { from: 'authenticated'; event: 'edit'; to: 'editing' }
  | { from: 'editing'; event: 'save'; to: 'authenticated' }
  | { from: 'editing'; event: 'cancel'; to: 'authenticated' };

type UserStateMachine = StateMachineConfig<UserTransitions>;

// Type-safe state machine implementation
class StateMachine<T extends StateMachineConfig<any>> {
  private currentState: T['initial'];

  constructor(
    private config: T,
    initialState: T['initial'] = config.initial
  ) {
    this.currentState = initialState;
  }

  canTransition<E extends keyof T['states'][T['initial']]['on']>(
    event: E
  ): boolean {
    return event in this.config.states[this.currentState].on;
  }

  transition<E extends keyof T['states'][T['initial']]['on']>(
    event: E
  ): T['states'][T['initial']]['on'][E] {
    if (!this.canTransition(event)) {
      throw new Error(`Cannot transition from ${this.currentState} with ${String(event)}`);
    }

    const nextState = this.config.states[this.currentState].on[event];
    this.currentState = nextState;
    return nextState;
  }

  getState(): T['initial'] {
    return this.currentState;
  }
}
```

### 3. Type-Safe Builder Pattern
```typescript
type RequiredFields<T> = {
  [K in keyof T]-?: undefined extends T[K] ? never : K;
}[keyof T];

type OptionalFields<T> = {
  [K in keyof T]-?: undefined extends T[K] ? K : never;
}[keyof T];

interface Builder<T> {
  with<K extends OptionalFields<T>>(
    field: K,
    value: NonNullable<T[K]>
  ): Builder<Omit<T, K> & Required<Pick<T, K>>>;
  build(): RequiredFields<T> extends never ? T : Required<T>;
}

function createBuilder<T extends object>(): Builder<T> & T {
  return new Proxy({} as any, {
    get(target, prop) {
      if (prop === 'with') {
        return (field: string, value: any) => {
          return createBuilder<T>({ ...target, [field]: value });
        };
      }
      if (prop === 'build') {
        return () => target;
      }
      return target[prop as keyof T];
    }
  });
}

// Example usage
interface User {
  id?: number;
  name: string;
  email?: string;
  age?: number;
}

const userBuilder = createBuilder<User>();
const user = userBuilder
  .with('name', 'John')
  .with('email', 'john@example.com')
  .with('age', 30)
  .build();
```

## Performance Considerations

### Type Performance Tips
1. **Use interfaces over type aliases for objects** - interfaces are generally faster and can be merged
2. **Prefer unions over overloads** - unions are typically faster to resolve
3. **Avoid deep conditional types in hot paths** - they can slow down compilation
4. **Use `as const` for literals** - creates more specific types
5. **Leverage type inference** - let TypeScript infer when possible

### Compilation Performance
```typescript
// Use type assertions for complex transformations in hot paths
// instead of complex conditional types

// Bad (slow compilation)
type ComplexTransform<T> = T extends { [K in keyof T]: infer U }
  ? U extends { [P in keyof U]: infer V }
    ? V
    : never
  : never;

// Good (fast compilation)
function transform<T>(obj: T) {
  return (obj as any).result as any;
}
```

These advanced type patterns enable you to create highly type-safe, self-documenting code that catches errors at compile-time rather than runtime.