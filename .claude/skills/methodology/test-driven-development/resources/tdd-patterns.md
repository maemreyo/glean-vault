# TDD Patterns

This document covers common TDD patterns and approaches for different scenarios.

## Fundamental TDD Patterns

### 1. Red-Green-Refactor
The core TDD cycle applied to different scenarios.

#### Feature Development
```typescript
// RED: Test for new feature
describe('Feature: User Registration', () => {
  it('should create user with valid data', () => {
    const userData = {
      email: 'test@example.com',
      password: 'securePassword123',
      name: 'Test User'
    };

    const user = userService.register(userData);

    expect(user.id).toBeDefined();
    expect(user.email).toBe(userData.email);
    expect(user.password).not.toBe(userData.password); // Should be hashed
  });
});

// GREEN: Minimal implementation
class UserService {
  register(userData: UserData) {
    return {
      id: Math.random().toString(),
      email: userData.email,
      password: this.hash(userData.password)
    };
  }

  private hash(password: string) {
    return `hashed_${password}`;
  }
}

// REFACTOR: Improve implementation
class UserService {
  register(userData: UserData) {
    this.validate(userData);

    const user = new User({
      id: this.generateId(),
      email: userData.email,
      password: this.hash(userData.password),
      name: userData.name,
      createdAt: new Date()
    });

    this.repository.save(user);
    return user.toDTO();
  }

  private validate(userData: UserData) {
    if (!userData.email || !userData.password) {
      throw new Error('Email and password required');
    }
  }
}
```

### 2. Transformation Priority Premise
Order of transformations to guide implementation from simple to complex:

1. ({}->nil) - no code to code returning nil
2. (nil->constant)
3. (constant->constant+) - one constant to another
4. (constant->scalar) - constant to variable
5. (statement->statements) - adding more statements
6. (conditional->if) - adding if statements
7. (scalar->array) - single value to collection
8. (array->array+) - more array operations
9. (statement->recursion) - introduce recursion
10. (if->while) - introduce loops
11. (expression->function) - extract function
12. (variable->assignment) - introduce assignment

#### Example: FizzBuzz
```typescript
// Test 1: Return 1 for 1
it('should return 1 for 1', () => {
  expect(fizzBuzz(1)).toBe('1');
});

// Implementation 1: ({ }->nil->constant)
function fizzBuzz(n: number): string {
  return '1';
}

// Test 2: Return 2 for 2
it('should return 2 for 2', () => {
  expect(fizzBuzz(2)).toBe('2');
});

// Implementation 2: (constant->scalar)
function fizzBuzz(n: number): string {
  return n.toString();
}

// Test 3: Return "Fizz" for 3
it('should return Fizz for multiples of 3', () => {
  expect(fizzBuzz(3)).toBe('Fizz');
});

// Implementation 3: (scalar->conditional)
function fizzBuzz(n: number): string {
  if (n % 3 === 0) return 'Fizz';
  return n.toString();
}

// Test 4: Return "Buzz" for 5
it('should return Buzz for multiples of 5', () => {
  expect(fizzBuzz(5)).toBe('Buzz');
});

// Implementation 4: (conditional->if->if)
function fizzBuzz(n: number): string {
  if (n % 3 === 0) return 'Fizz';
  if (n % 5 === 0) return 'Buzz';
  return n.toString();
}

// Test 5: Return "FizzBuzz" for 15
it('should return FizzBuzz for multiples of both 3 and 5', () => {
  expect(fizzBuzz(15)).toBe('FizzBuzz');
});

// Implementation 5: (if->if->if)
function fizzBuzz(n: number): string {
  if (n % 15 === 0) return 'FizzBuzz';
  if (n % 3 === 0) return 'Fizz';
  if (n % 5 === 0) return 'Buzz';
  return n.toString();
}
```

## State-Based Testing Patterns

### 1. State Verification
Test the state after operations.

```typescript
describe('Bank Account', () => {
  it('should update balance after deposit', () => {
    // Arrange
    const account = new BankAccount(100);

    // Act
    account.deposit(50);

    // Assert - verify state
    expect(account.balance).toBe(150);
  });
});
```

### 2. State Transition Testing
Test valid and invalid state transitions.

```typescript
describe('Order Status', () => {
  it('should transition from pending to confirmed', () => {
    const order = new Order({ status: 'pending' });

    order.confirm();

    expect(order.status).toBe('confirmed');
  });

  it('should not transition from delivered to pending', () => {
    const order = new Order({ status: 'delivered' });

    expect(() => order.setPending()).toThrow('Invalid transition');
  });
});
```

## Behavior-Based Testing Patterns

### 1. Command Pattern
Test commands and their effects.

```typescript
describe('Command Pattern', () => {
  it('should execute add item command', () => {
    const cart = new ShoppingCart();
    const command = new AddItemCommand({ id: 1, name: 'Book', price: 10 });

    command.execute(cart);

    expect(cart.items).toContain({ id: 1, name: 'Book', price: 10 });
  });

  it('should undo add item command', () => {
    const cart = new ShoppingCart();
    const command = new AddItemCommand({ id: 1, name: 'Book', price: 10 });

    command.execute(cart);
    command.undo(cart);

    expect(cart.items).toEqual([]);
  });
});
```

### 2. Observer Pattern
Test notifications and event handling.

```typescript
describe('Observer Pattern', () => {
  it('should notify observers of state change', () => {
    const subject = new Subject();
    const observer = jest.fn();

    subject.subscribe(observer);
    subject.setState('new value');

    expect(observer).toHaveBeenCalledWith('new value');
  });
});
```

## Collection-Based Testing Patterns

### 1. Collection Testing
Test operations on collections.

```typescript
describe('Product Catalog', () => {
  it('should add products to catalog', () => {
    const catalog = new ProductCatalog();
    const product = new Product({ id: 1, name: 'Laptop' });

    catalog.add(product);

    expect(catalog.getById(1)).toBe(product);
  });

  it('should remove products from catalog', () => {
    const catalog = new ProductCatalog();
    const product = new Product({ id: 1, name: 'Laptop' });
    catalog.add(product);

    catalog.remove(1);

    expect(catalog.getById(1)).toBeUndefined();
  });
});
```

### 2. Iterator Pattern
Test iteration over collections.

```typescript
describe('Iterator', () => {
  it('should iterate over all items', () => {
    const collection = new Collection([1, 2, 3]);
    const iterator = collection.createIterator();
    const results = [];

    while (iterator.hasNext()) {
      results.push(iterator.next());
    }

    expect(results).toEqual([1, 2, 3]);
  });
});
```

## Error Handling Patterns

### 1. Exception Testing
Test error conditions.

```typescript
describe('Validation', () => {
  it('should throw error for invalid email', () => {
    expect(() => validateEmail('invalid')).toThrow('Invalid email format');
  });

  it('should provide specific error message', () => {
    try {
      validateEmail('');
    } catch (error) {
      expect(error.message).toBe('Email cannot be empty');
    }
  });
});
```

### 2. Result Type Pattern
Test success/failure results without exceptions.

```typescript
describe('Result Type', () => {
  it('should return success result', () => {
    const result = divide(10, 2);

    expect(result.isSuccess()).toBe(true);
    expect(result.value).toBe(5);
  });

  it('should return failure result', () => {
    const result = divide(10, 0);

    expect(result.isFailure()).toBe(true);
    expect(result.error).toBe('Division by zero');
  });
});
```

## Mocking and Stubbing Patterns

### 1. Test Doubles
Different types of test doubles for different scenarios.

```typescript
// Stub: Returns canned responses
const userRepository = {
  findById: jest.fn().mockResolvedValue({ id: 1, name: 'Test' })
};

// Mock: Verifies interactions
const emailService = {
  send: jest.fn()
};

// Fake: Working implementation but simplified
class InMemoryUserRepository {
  private users = new Map();

  async save(user) {
    this.users.set(user.id, user);
    return user;
  }
}

// Dummy: Passed around but never used
const dummyLogger = { log: jest.fn() };
```

### 2. Dependency Injection for Testing
Make dependencies testable.

```typescript
class UserService {
  constructor(
    private repository: UserRepository,
    private emailService: EmailService
  ) {}

  async register(userData: UserData) {
    const user = await this.repository.save(userData);
    await this.emailService.sendWelcome(user.email);
    return user;
  }
}

// Test
it('should register user and send welcome email', async () => {
  const mockRepo = { save: jest.fn().mockResolvedValue({ id: 1 }) };
  const mockEmail = { sendWelcome: jest.fn() };

  const service = new UserService(mockRepo, mockEmail);

  await service.register({ email: 'test@test.com' });

  expect(mockRepo.save).toHaveBeenCalled();
  expect(mockEmail.sendWelcome).toHaveBeenCalledWith('test@test.com');
});
```

## Integration Testing Patterns

### 1. Database Testing
Test with real database.

```typescript
describe('User Repository Integration', () => {
  let db: Database;
  let repository: UserRepository;

  beforeEach(async () => {
    db = await Database.connect(':memory:');
    repository = new UserRepository(db);
  });

  afterEach(async () => {
    await db.close();
  });

  it('should persist user to database', async () => {
    const user = await repository.save({
      email: 'test@test.com',
      name: 'Test User'
    });

    const retrieved = await repository.findById(user.id);
    expect(retrieved.email).toBe('test@test.com');
  });
});
```

### 2. API Testing
Test API endpoints.

```typescript
describe('User API', () => {
  let app: Express;

  beforeEach(() => {
    app = createApp();
  });

  it('should create user via POST', async () => {
    const response = await request(app)
      .post('/api/users')
      .send({
        email: 'test@test.com',
        name: 'Test'
      })
      .expect(201);

    expect(response.body.email).toBe('test@test.com');
    expect(response.body.id).toBeDefined();
  });
});
```

## Property-Based Testing Patterns

### 1. Generative Testing
Test with many random inputs.

```typescript
import fc from 'fast-check';

describe('String Utils', () => {
  it('should preserve length after reversal', () => {
    fc.assert(
      fc.property(fc.string(), (str) => {
        expect(reverse(reverse(str))).toBe(str);
      })
    );
  });

  it('should handle Unicode correctly', () => {
    fc.assert(
      fc.property(fc.unicodeString(), (str) => {
        const reversed = reverse(str);
        expect([...reversed].length).toBe([...str].length);
      })
    );
  });
});
```

## Test Organization Patterns

### 1. Test Suite Structure
Organize tests logically.

```typescript
describe('Payment Processing', () => {
  describe('Credit Card Payments', () => {
    it('should process valid credit card');
    it('should reject expired card');
    it('should handle insufficient funds');
  });

  describe('PayPal Payments', () => {
    it('should process valid PayPal account');
    it('should handle authentication failure');
  });

  describe('Refunds', () => {
    it('should refund full amount');
    it('should refund partial amount');
  });
});
```

### 2. Shared Examples
Reuse test logic.

```typescript
function itBehavesLikeCache(cache: Cache) {
  it('should store and retrieve values', async () => {
    await cache.set('key', 'value');
    expect(await cache.get('key')).toBe('value');
  });

  it('should return null for missing keys', async () => {
    expect(await cache.get('missing')).toBeNull();
  });
}

describe('Memory Cache', () => {
  let cache: Cache;
  beforeEach(() => cache = new MemoryCache());

  itBehavesLikeCache(cache);
});

describe('Redis Cache', () => {
  let cache: Cache;
  beforeEach(async () => cache = new RedisCache());

  itBehavesLikeCache(cache);
});
```

## Performance Testing Patterns

### 1. Benchmark Testing
Test performance characteristics.

```typescript
describe('Performance', () => {
  it('should process 1000 items quickly', async () => {
    const start = Date.now();

    await processor.processLargeList(generateItems(1000));

    const duration = Date.now() - start;
    expect(duration).toBeLessThan(1000); // < 1 second
  });

  it('should not leak memory', () => {
    const initialMemory = process.memoryUsage().heapUsed;

    for (let i = 0; i < 10000; i++) {
      processor.process(createItem());
    }

    const finalMemory = process.memoryUsage().heapUsed;
    const increase = finalMemory - initialMemory;
    expect(increase).toBeLessThan(10 * 1024 * 1024); // < 10MB
  });
});
```

## Continuous Integration Patterns

### 1. Test Pyramid
Balance between unit, integration, and E2E tests.

```
    E2E Tests (few)
       ^
       |
Integration Tests (some)
       ^
       |
  Unit Tests (many)
```

### 2. Test Strategy
Organize tests by type and purpose.

```typescript
// Unit tests - Fast, isolated
describe('UserService Validation', () => {
  // Test validation logic
});

// Integration tests - Medium speed
describe('UserRepository Integration', () => {
  // Test with database
});

// E2E tests - Slow, full system
describe('User Registration E2E', () => {
  // Test through API
});
```

## Refactoring with Tests

### 1. Characterization Tests
Understand existing behavior before refactoring.

```typescript
// Write tests for existing code to understand behavior
describe('Legacy Function', () => {
  it('should handle null input', () => {
    expect(legacyFunction(null)).toBe('default');
  });

  it('should handle empty string', () => {
    expect(legacyFunction('')).toBe('default');
  });

  it('should process normal input', () => {
    expect(legacyFunction('input')).toBe('processed_input');
  });
});

// Now refactor with confidence
```

### 2. Incremental Refactoring
Refactor in small, testable steps.

```typescript
// Step 1: Extract method with tests
class Calculator {
  calculateTotal(items) {
    return items.reduce((sum, item) => {
      return sum + this.calculateItemTotal(item);
    }, 0);
  }

  // Extracted with tests
  private calculateItemTotal(item) {
    return item.price * item.quantity;
  }
}

// Step 2: Apply more refactoring
// Each step verified by existing tests
```