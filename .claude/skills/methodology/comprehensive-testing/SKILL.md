---
name: comprehensive-testing
description: Systematic testing methodology using adversarial mindset to find weaknesses beyond happy path. Covers boundary testing, null checks, type mismatches, edge cases, and error injection. Use when adding tests to legacy code, ensuring critical features are robust, increasing coverage metrics, or regression testing before refactoring.
---

# Comprehensive Testing

Adversarial testing methodology that systematically breaks code to ensure robustness beyond basic happy path testing.

## Quick Start

```bash
# Example test cases to always include:
describe('functionName', () => {
  it('handles null input', () => {
    expect(() => functionName(null)).toThrow();
  });

  it('handles undefined input', () => {
    expect(() => functionName(undefined)).toThrow();
  });

  it('handles empty array/string', () => {
    expect(functionName([])).toEqual(expectedDefaultValue);
  });
});
```

## Testing Phases

### 1. Hunt - Identify Attack Surface

Map code structure:
- **Control Flow**: All `if/else`, `switch`, loops, early returns
- **Boundaries**: Min/max values, array indices, string lengths
- **State Transitions**: Valid → Invalid states, error conditions
- **External Dependencies**: Database, APIs, file system, network

### 2. Attack - Design Breakage Scenarios

Use these attack patterns:

| Attack Type | Examples | Expected Behavior |
|-------------|----------|-------------------|
| Null/Undefined | `null`, `undefined`, `void 0` | Graceful error |
| Type Mismatch | `123` instead of string, `{}` instead of array | Type validation |
| Boundary Violations | `-1`, `Number.MAX_VALUE`, empty strings | Input validation |
| Resource Exhaustion | Huge arrays, deep recursion | Rate limiting/timeout |
| malformed Data | Missing fields, wrong data types | Schema validation |

### 3. Fortify - Write Resilient Tests

```javascript
// Template for comprehensive test
describe('moduleName', () => {
  // Happy path
  it('works with valid input', () => {
    expect(module(validInput)).toEqual(expectedOutput);
  });

  // Null/undefined handling
  it.each([null, undefined])('handles %s input', (input) => {
    expect(() => module(input)).toThrow('Required field');
  });

  // Type validation
  it.each([123, [], {}])('rejects wrong type: %s', (input) => {
    expect(() => module(input)).toThrow('Invalid type');
  });

  // Boundary testing
  it('handles boundary values', () => {
    expect(module(minValue)).toBeDefined();
    expect(module(maxValue)).toBeDefined();
  });
});
```

## Test Coverage Strategy

### Critical Paths (100% coverage required)
- Authentication/authorization
- Payment processing
- Data validation
- Error handling

### Risk-Based Testing
 prioritize:
1. **High Impact**: Data corruption, security breaches
2. **High Probability**: User input processing, API calls
3. **Complex Logic**: Multi-step workflows, state machines

### Coverage Examples

```typescript
// Boundary testing for numeric input
it.each([
  [0, 'minimum boundary'],
  [100, 'maximum boundary'],
  [-1, 'below minimum'],
  [101, 'above maximum']
])('handles %s (%s)', (value, description) => {
  if (value < 0 || value > 100) {
    expect(() => validateScore(value)).toThrow();
  } else {
    expect(validateScore(value)).toBe(true);
  }
});
```

## Common Anti-Patterns to Test

| Anti-Pattern | Test Case | Fix Strategy |
|--------------|-----------|--------------|
| Implicit null checks | `obj.prop` without null check | Add validation or optional chaining |
| Magic numbers | Hardcoded values | Use constants with validation |
| Unhandled promises | Missing catch blocks | Add error boundaries |
| Type coercion | `==` instead of `===` | Use strict equality |
| Silent failures | Errors not logged/propagated | Add proper error handling |

## Error Injection Testing

```javascript
// Test failure scenarios
describe('error handling', () => {
  it('handles database connection failure', async () => {
    mockDatabase.connect.mockRejectedValue(new Error('Connection failed'));

    await expect(service.getData()).rejects.toThrow('Service unavailable');
  });

  it('gracefully degrades when external API is down', async () => {
    mockAPI.get.mockRejectedValue(new Error('API unavailable'));

    const result = await.service.getData();
    expect(result).toEqual(cachedData);
  });
});
```

## Resources

- [OWASP Testing Guide](https://owasp.org/www-project-web-security-testing-guide/) for security testing
- [Mutation Testing](https://github.com/stryker-js/stryker-js) for test quality validation
- [Property-Based Testing](https://jsverify.github.io/) for edge case discovery
