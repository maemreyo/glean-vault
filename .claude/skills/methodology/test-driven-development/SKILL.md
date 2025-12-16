---
name: test-driven-development
description: Strict TDD methodology following Red-Green-Refactor cycle. Fundamental principle: "If you didn't watch the test fail, you don't know if it tests the right thing." Requires writing failing test first, implementing minimal code to pass, then refactoring. Use for new feature development, bug fixes, or refactoring existing code.
---

# Test-Driven Development (TDD)

## Quick Start

1. **Write failing test** for desired behavior
2. **Verify it fails** for the right reason
3. **Write minimal code** to make test pass
4. **Refactor** while keeping tests green

## Instructions

### When to Use TDD
✅ **Always use for**:
- New feature development
- Bug fixes (write test that reproduces bug first)
- Refactoring (ensure tests exist before changing)
- Any behavior change

❌ **NOT for** (requires explicit approval):
- Throwaway prototypes
- Generated/scaffolded code
- Pure configuration changes

### Core Principle
**"If you didn't watch the test fail, you don't know if it tests the right thing."**

### The Red-Green-Refactor Cycle

#### Step 1: RED - Write Failing Test
```typescript
describe('calculateTotal', () => {
  it('should sum item prices', () => {
    const items = [{ price: 10 }, { price: 20 }];
    expect(calculateTotal(items)).toBe(30);
  });
});
```

#### Step 2: Verify Test Fails
```bash
npm test -- --grep "sum item prices"
# Expected: FAIL - "calculateTotal is not defined"
```
The failure should be because feature doesn't exist, not syntax errors.

#### Step 3: GREEN - Write Minimal Code
```typescript
function calculateTotal(items: Item[]): number {
  return items.reduce((sum, item) => sum + item.price, 0);
}
```
Write the simplest code that passes. Don't over-engineer.

#### Step 4: Verify Test Passes
```bash
npm test -- --grep "sum item prices"
# Expected: PASS
```

#### Step 5: REFACTOR - Clean Up
- Extract functions
- Rename variables
- Remove duplication
- Run tests after each change

### The Non-Negotiable Rule

**NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST**

This is a rule, not a guideline.

### Already Wrote Code?
Delete it completely. Don't keep as reference.

```
WRONG: "I'll keep this code as reference"
RIGHT: Delete, write test, rewrite from scratch
```

### Why So Strict?
- Tests written after code just verify what was written
- True TDD produces better designs
- Prevents rationalization and bias

## Examples

For comprehensive TDD examples and patterns, see [tdd-patterns.md](resources/tdd-patterns.md).

Quick examples:
- **Feature development**: Write test for behavior, implement to pass
- **Bug fix**: Write test that reproduces bug, fix until test passes
- **Refactoring**: Ensure tests pass, then refactor with confidence

## TDD for Different Scenarios

### New Feature Development
1. Write test for desired behavior
2. Verify test fails (feature doesn't exist)
3. Implement minimal code
4. Refactor while tests green

### Bug Fixes
1. Write test that reproduces bug
2. Verify test fails (bug exists)
3. Fix bug
4. Verify test passes
5. Add related edge case tests

### Refactoring
1. Ensure comprehensive test coverage
2. Run tests to confirm green
3. Refactor incrementally
4. Run tests after each change

For language-specific TDD practices, see [tdd-language-examples.md](resources/tdd-language-examples.md).

## Test Structure Guidelines

### AAA Pattern (Arrange-Act-Assert)
```typescript
it('should calculate discount for premium user', () => {
  // Arrange
  const user = { tier: 'premium' };
  const amount = 100;

  // Act
  const result = calculateDiscount(user, amount);

  // Assert
  expect(result).toBe(10); // 10% discount
});
```

### Test Naming
- Use "should" or "should not"
- Describe behavior, not implementation
- Be specific about expected outcome

### One Assertion Per Test
```typescript
// Good
it('should validate email format', () => {
  expect(isValidEmail('test@example.com')).toBe(true);
});

it('should reject invalid email', () => {
  expect(isValidEmail('invalid')).toBe(false);
});

// Avoid
it('should handle email validation', () => {
  expect(isValidEmail('test@example.com')).toBe(true);
  expect(isValidEmail('invalid')).toBe(false);
  expect(isValidEmail(null)).toBe(false);
});
```

## Common TDD Anti-patterns

### 1. Writing Tests After Code
```typescript
// WRONG: Write code then tests
function addUser(user) {
  // ... implementation
}

// Then write test to verify
test('addUser adds user', () => {
  // ... verifies implementation
});

// RIGHT: Test first
test('addUser adds user', () => {
  // ... describe desired behavior
});
// Then implement
```

### 2. Testing Implementation Details
```typescript
// WRONG: Tests internal structure
test('uses array internally', () => {
  expect(users.data).toBeInstanceOf(Array);
});

// RIGHT: Tests behavior
test('can add multiple users', () => {
  addUser(user1);
  addUser(user2);
  expect(getAllUsers()).toEqual([user1, user2]);
});
```

### 3. Skipping Red Phase
```typescript
// WRONG: Write test and code together
test('calculates total', () => {
  expect(calculateTotal(items)).toBe(30);
});
function calculateTotal(items) { /* implementation */ }

// RIGHT: Ensure test fails first
test('calculates total', () => {
  expect(calculateTotal(items)).toBe(30);
});
// Run: FAIL (function doesn't exist)
// Then implement
```

## Test First vs Test After

### Test First (True TDD)
- ✅ Drives design
- ✅ Ensures testability
- ✅ Prevents over-engineering
- ✅ Guarantees all behavior is tested
- ✅ Produces better code organization

### Test After
- ❌ Just verifies implementation
- ❌ Can lead to untestable code
- ❌ May miss edge cases
- ❌ Encourages writing too much code

## TDD Workflow Checklist

### Before Writing Code
- [ ] Test written for behavior
- [ ] Test fails (feature doesn't exist)
- [ ] Failure reason is correct
- [ ] Test is isolated
- [ ] Test has clear assertion

### While Writing Code
- [ ] Write minimal implementation
- [ ] Run tests frequently
- [ ] No extra features
- [ ] No over-engineering
- [ ] Keep it simple

### After Code Passes
- [ ] All tests pass
- [ ] No test duplication
- [ ] Code is clean
- [ ] Refactor if needed
- [ ] Run full test suite

## TDD by Example

### Shopping Cart Feature

#### Step 1: Write Failing Test
```typescript
describe('Shopping Cart', () => {
  it('should calculate total with tax', () => {
    const cart = new ShoppingCart();
    cart.addItem({ name: 'Book', price: 20 });
    cart.addItem({ name: 'Pen', price: 5 });

    const total = cart.getTotal(0.1); // 10% tax

    expect(total).toBe(27.5); // 25 + 2.5 tax
  });
});
```

#### Step 2: Verify Failure
```bash
FAIL: ShoppingCart is not defined
```

#### Step 3: Implement to Pass
```typescript
class ShoppingCart {
  private items: Item[] = [];

  addItem(item: Item) {
    this.items.push(item);
  }

  getTotal(taxRate: number) {
    const subtotal = this.items.reduce((sum, item) => sum + item.price, 0);
    return subtotal * (1 + taxRate);
  }
}
```

#### Step 4: Refactor
```typescript
class ShoppingCart {
  private items: Item[] = [];

  addItem(item: Item) {
    this.items.push(item);
  }

  getTotal(taxRate: number) {
    return this.getSubtotal() * (1 + taxRate);
  }

  private getSubtotal() {
    return this.items.reduce((sum, item) => sum + item.price, 0);
  }
}
```

## TDD for Bug Fixes

### Example: Login Bug

#### Bug Report
"Users with special characters in password can't login"

#### Step 1: Write Test that Reproduces Bug
```typescript
describe('Login', () => {
  it('should handle passwords with special characters', () => {
    const user = {
      email: 'test@example.com',
      password: 'p@$$w0rd!123'
    };

    expect(() => loginUser(user)).not.toThrow();
  });
});
```

#### Step 2: Verify Test Fails
```bash
FAIL: Invalid password format
```

#### Step 3: Fix Bug
```typescript
function loginUser(credentials: UserCredentials) {
  // Fix: Remove invalid password validation
  if (!credentials.password || credentials.password.length < 8) {
    throw new Error('Password too short');
  }
  // ... rest of login logic
}
```

#### Step 4: Add More Edge Cases
```typescript
it('should handle empty password', () => {
  expect(() => loginUser({ email: 'test@test.com', password: '' }))
    .toThrow('Password too short');
});

it('should handle unicode characters', () => {
  const user = {
    email: 'user@example.com',
    password: 'pássword123' // Contains accent
  };
  expect(() => loginUser(user)).not.toThrow();
});
```

## TDD Best Practices

### 1. Keep Tests Simple
- Test one behavior per test
- Use clear, descriptive names
- Arrange-Act-Assert pattern

### 2. Write Fast Tests
- Avoid external dependencies
- Use mocks/doubles when needed
- Focus on unit tests first

### 3. Maintain Test Independence
- Tests should not depend on each other
- Use fresh setup for each test
- Avoid shared state

### 4. Run Tests Frequently
- After each code change
- Before committing
- In CI/CD pipeline

### 5. Refactor Mercilessly
- Improve code while tests are green
- Remove duplication
- Enhance readability

For comprehensive TDD patterns and language-specific examples, see:
- [tdd-patterns.md](resources/tdd-patterns.md)
- [tdd-language-examples.md](resources/tdd-language-examples.md)