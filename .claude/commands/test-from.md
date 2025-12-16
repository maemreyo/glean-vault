# /test-from - Generate Tests from Explored Code

## Purpose

Generate comprehensive tests based on business logic and patterns documented in `/how` exploration. Leverages detailed code analysis to create thorough test coverage targeting critical paths and edge cases.

**"Test what matters"** - Generate tests based on actual business logic, not guesswork.

## Aliases

```bash
/test-from [feature]
/generate-tests [feature]
```

## Usage

```bash
# Generate tests from exploration docs
/test-from "calculator" --coverage=90

# Focus on specific test types
/test-from "auth" --type="integration"

# Preview test plan
/test-from "payment" --preview
```

## Arguments

- `feature`: Feature name (will look for docs in `docs/<feature>/`)

## Flags

| Flag | Description | Example |
|------|-------------|---------|
| `--from=path` | Explicit docs folder | `--from=docs/calc/` |
| `--coverage=N` | Target coverage % | `--coverage=85` |
| `--type=types` | Test types | `--type="unit,integration"` |
| `--preview` | Preview test plan only | `--preview` |

---

## Integration with /how

Reads business logic from exploration docs:

```bash
# Step 1: Explore with detailed analysis
/how "calculator"
→ docs/calculator/phase-1-discovery-structure.md contains file inventory
→ docs/calculator/phase-2-analysis.md contains:
  - Business logic with line numbers
  - Data models
  - Edge cases
  - Critical functions

# Step 2: Generate targeted tests
/test-from "calculator" --coverage=90
→ Creates tests for all business logic
→ Covers edge cases from docs
→ Achieves 90% coverage
→ Updates docs/calculator/README.md with test coverage info
```

---

## Workflow

Generate tests for: **$FEATURE**

{{ if --from provided }}
**Source docs**: `$FROM_PATH`
{{ else }}
**Source docs**: `docs/$FEATURE/`
{{ endif }}

{{ if --coverage provided }}
**Target coverage**: `$COVERAGE%`
{{ else }}
**Target coverage**: 80% (default)
{{ endif }}

{{ if --type provided }}
**Test types**: `$TYPES`
{{ else }}
**Test types**: unit, integration (default)
{{ endif }}

---

### Phase 1: Load Business Logic 📖

**Goal**: Extract testable code from exploration docs

**Duration**: 5-10 minutes

---

**Steps**:

1. **Read exploration docs**
   ```bash
   DOCS_PATH="docs/$FEATURE/"
   ```

2. **Extract from phase-2-analysis.md**:
   - Business logic functions with line numbers
   - Data models and validation
   - Critical paths
   - Edge cases mentioned
   - TODO/FIXME notes about untested code

3. **Extract from phase-1-discovery-structure.md**:
   - Component hierarchy for integration tests
   - API endpoints to test
   - Data flow for E2E tests
   - File locations

**Output**:
```markdown
Testable Code Inventory:

Business Logic:
- calculateTotalPrice() - pricing.ts:45-89
- validateCoupon() - coupons.ts:20-55
- checkInventory() - inventory.ts:10-30

Components:
- CheckoutForm (user interaction)
- ProductCard (display)

API Endpoints:
- POST /api/checkout
- GET /api/products

Edge Cases Noted:
- Division by zero in calculator
- Expired coupons
- Race condition in inventory
```

---

### Phase 2: Plan Test Coverage 📋

**Goal**: Create comprehensive test plan

**Duration**: 10-15 minutes

---

**Dispatch Test Planner SubAgent**:

```markdown
Test Planner SubAgent

GOAL: Create test plan for "$FEATURE" targeting $COVERAGE% coverage

INPUT:
- Testable code inventory: [from Phase 1]
- Target coverage: $COVERAGE%
- Test types: $TYPES

---

SUBTASK 2.1: Identify Test Scenarios (10 min)

**For each business logic function**:
1. Happy path scenarios
2. Edge cases
3. Error scenarios
4. Boundary conditions

**Example** (for calculateTotalPrice):
```
Happy Path:
- Calculate with normal items
- Calculate with discount
- Calculate with tax

Edge Cases:
- Empty cart
- Zero price items
- Maximum quantity

Errors:
- Invalid coupon
- Negative prices
```

**Output**: Test scenario list

---

SUBTASK 2.2: Plan Test Files (5 min)

**Steps**:
1. Map scenarios to test files
2. Follow existing test structure
3. Identify reusable test utilities

**Output**:
```
Test files to create:
- pricing.test.ts (15 tests)
- coupons.test.ts (10 tests)
- inventory.test.ts (8 tests)
- CheckoutForm.test.tsx (12 tests)
- checkout-flow.integration.test.ts (5 tests)

Total: 50 tests estimated
```

---

OUTPUT: Return test plan

```markdown
📋 TEST PLAN

Feature: $FEATURE
Target Coverage: $COVERAGE%
Estimated Tests: ~50

---

## Unit Tests (35 tests)

### pricing.test.ts (15 tests)
**Function**: calculateTotalPrice()

Tests:
1. ✅ Calculate simple total
2. ✅ Apply item discounts
3. ✅ Apply coupon discount
4. ✅ Calculate tax by region
5. ✅ Add shipping cost
6. ✅ Handle empty cart
7. ✅ Handle zero-price items
8. ✅ Handle maximum quantity
9. ✅ Throw error on negative price
10. ✅ Throw error on invalid region
11. ✅ Round to 2 decimals
12. ✅ Preserve precision with cents
13. ✅ Handle bundle discounts
14. ✅ Apply multiple coupons
15. ✅ Tax-exempt regions

### coupons.test.ts (10 tests)
**Function**: validateCoupon()

Tests:
1. ✅ Valid coupon
2. ✅ Expired coupon → error
3. ✅ Exceeded usage → error
4. ✅ Below minimum purchase → error
5. ✅ Percentage discount
6. ✅ Fixed discount
7. ✅ First-time user only
8. ✅ Active vs inactive
9. ✅ Coupon stacking
10. ✅ Case insensitive code

[... more tests ...]

---

## Integration Tests (10 tests)

### checkout-flow.integration.test.ts

Tests:
1. ✅ Full checkout flow
2. ✅ Add to cart → apply coupon → checkout
3. ✅ Inventory check during checkout
4. ✅ Failed payment handling
5. ✅ Success state persistence
[... more integration tests ...]

---

## E2E Tests (5 tests) - Optional

### checkout.e2e.test.ts

Tests:
1. ✅ Browse → Add → Checkout → Success
2. ✅ Apply invalid coupon → Error shown
3. ✅ Out of stock → Prevented
4. ✅ Navigate back → Cart preserved
5. ✅ Refresh → Session maintained

---

ESTIMATED COVERAGE: 88%
TEST PLAN COMPLETE ✅
```
```

**Return**: Test plan to main agent

---

{{ if --preview }}

### Phase 3: Preview Test Plan 👁️

**Display plan to user**

```markdown
📋 TEST GENERATION PLAN

Feature: $FEATURE
Target Coverage: $COVERAGE%

---

## Tests to Create

Unit Tests: 35 tests across 3 files
Integration Tests: 10 tests
E2E Tests: 5 tests (optional)

Total: 50 tests

---

## Estimated Coverage

Current: ~65% (from docs)
After: ~88%
Gain: +23%

---

## Files to Create

- __tests__/pricing.test.ts (15 tests)
- __tests__/coupons.test.ts (10 tests)
- __tests__/inventory.test.ts (8 tests)
- __tests__/components/CheckoutForm.test.tsx (12 tests)
- __tests__/integration/checkout-flow.test.ts (10 tests)
- __tests__/e2e/checkout.e2e.test.ts (5 tests)

---

Execution time: ~2-3 hours

To generate: /test-from "$FEATURE"
(without --preview)
```

**END** (no generation)

{{ else }}

### Phase 3: Generate Tests 🧪

**Goal**: Create test files

**Duration**: 2-3 hours (for comprehensive suite)

---

**Dispatch Tester SubAgent** (using `test-master` agent):

```markdown
Test Master SubAgent

GOAL: Generate comprehensive test suite for "$FEATURE"

INPUT:
- Test plan: [from Phase 2]
- Business logic: [from Phase 1]
- Existing test patterns: [from exploration docs]

REFERENCE:
- `.claude/agents/test-master.md`
- `.claude/skills/methodology/comprehensive-testing/SKILL.md`

---

EXECUTION:

For each test file in plan:

1. **Read test plan for this file**
2. **Study existing test patterns** (from docs)
3. **Generate test file**:
   - Follow existing patterns
   - Use same test framework
   - Match naming conventions
   - Apply AAA pattern (Arrange, Act, Assert)

4. **Run tests**:
   ```bash
   npm test [test-file]
   ```

5. **Verify**:
   - All tests passing (or intentionally failing if TDD)
   - Coverage meets target
   - No flaky tests

---

EXAMPLE OUTPUT (pricing.test.ts):

```typescript
import { calculateTotalPrice } from '../utils/pricing';
import { TAX_RATES } from '../constants';

describe('calculateTotalPrice', () => {
  describe('Happy path', () => {
    it('should calculate simple total correctly', () => {
      // Arrange
      const items = [
        { price: 1000, quantity: 2, discount: 0 }
      ];
      
      // Act
      const total = calculateTotalPrice(items, 'CA', null);
      
      // Assert
      const expected = 2000 + (2000 * TAX_RATES.CA);
      expect(total).toBe(expected);
    });
    
    it('should apply item discounts', () => {
      const items = [
        { price: 1000, quantity: 1, discount: 0.1 } // 10% off
      ];
      
      const total = calculateTotalPrice(items, 'CA', null);
      
      const subtotal = 900; // 1000 - 10%
      const expected = subtotal + (subtotal * TAX_RATES.CA);
      expect(total).toBe(expected);
    });
  });
  
  describe('Edge cases', () => {
    it('should handle empty cart', () => {
      const total = calculateTotalPrice([], 'CA', null);
      expect(total).toBe(0);
    });
    
    it('should handle zero-price items', () => {
      const items = [{ price: 0, quantity: 5, discount: 0 }];
      const total = calculateTotalPrice(items, 'CA', null);
      expect(total).toBe(0);
    });
  });
  
  describe('Error handling', () => {
    it('should throw on negative price', () => {
      const items = [{ price: -100, quantity: 1, discount: 0 }];
      expect(() => calculateTotalPrice(items, 'CA', null))
        .toThrow('Price cannot be negative');
    });
    
    it('should throw on invalid region', () => {
      const items = [{ price: 1000, quantity: 1, discount: 0 }];
      expect(() => calculateTotalPrice(items, 'XX', null))
        .toThrow('Invalid region');
    });
  });
});
```

---

OUTPUT: Return test generation summary

```markdown
✅ TEST GENERATION COMPLETE

Feature: $FEATURE

---

## Tests Created

Unit Tests:
- ✅ pricing.test.ts (15 tests, all passing)
- ✅ coupons.test.ts (10 tests, all passing)
- ✅ inventory.test.ts (8 tests, 7 passing, 1 TODO)

Component Tests:
- ✅ CheckoutForm.test.tsx (12 tests, all passing)

Integration Tests:
- ✅ checkout-flow.integration.test.ts (10 tests, all passing)

E2E Tests:
- ✅ checkout.e2e.test.ts (5 tests, all passing)

---

Total: 60 tests (59 passing, 1 TODO)

---

## Coverage Report

Before: 65%
After: 91%
Gain: +26%

---

Files Created:
- 6 test files
- ~800 lines of test code

---

TESTS READY ✅
```
```

**Return**: Test generation summary

{{ endif }}

---

### Phase 4: Verify Coverage 📊

**Goal**: Measure and report coverage

**Duration**: 5-10 minutes

---

**Steps**:

1. **Run coverage report**
   ```bash
   npm test -- --coverage
   # or
   pytest --cov=src
   ```

2. **Analyze results**
   - Overall coverage %
   - Per-file coverage
   - Uncovered lines
   - Branch coverage

3. **Identify gaps**
   - What's still untested
   - Why (intentional or oversight)
   - Recommendations

**Output**:
```markdown
📊 COVERAGE REPORT

Feature: $FEATURE

---

## Overall Coverage

Statements: 91% (target: 90%) ✅
Branches: 88% (target: 85%) ✅
Functions: 95% ✅
Lines: 91% ✅

---

## Per-File Coverage

pricing.ts:        98% ✅
coupons.ts:        95% ✅
inventory.ts:      85% ⚠️
CheckoutForm.tsx:  92% ✅

---

## Uncovered Lines

inventory.ts:
- Line 25-27: Race condition handler (difficult to test)
- Recommendation: Add note, or integration test

CheckoutForm.tsx:
- Line 145: Error boundary edge case
- Recommendation: Manual testing OK

---

## Summary

Target met: ✅ YES (91% > 90%)
Critical paths: ✅ 100% covered
Edge cases: ✅ Most covered
TODOs: 1 (race condition test)

---

VERIFICATION COMPLETE ✅
```

---

## Completion

```markdown
✅ TEST GENERATION COMPLETE

Feature: $FEATURE
Target Coverage: $COVERAGE%
Achieved: 91% ✅

---

## Summary

Tests Created: 60
Tests Passing: 59
Coverage Gain: +26%

Files:
- 6 test files
- ~800 lines of test code

---

## Next Steps

1. **Review tests**
   - Check generated tests make sense
   - Verify edge cases covered
   - Adjust assertions if needed

2. **Run tests locally**
   ```bash
   npm test
   ```

3. **Commit tests**
   ```bash
   git add __tests__/
   git commit -m "test: add comprehensive test suite for $FEATURE"
   ```

4. **Monitor coverage** in CI/CD

---

🎉 Comprehensive test suite generated!
```

---

### Phase 5: Update Documentation 📝

**Goal**: Track test coverage in source documentation

**Duration**: 2-3 minutes

---

**Steps**:

1. **Update README.md** with test coverage info
   ```bash
   # Append to docs/$FEATURE/README.md
   ```

2. **Add test coverage section**:
   ```markdown
   ## Test Coverage
   
   **Last updated**: [date]
   **Generated by**: `/test-from` command
   
   ### Coverage Metrics
   - **Overall**: {{ X }}%
   - **Statements**: {{ X }}%
   - **Branches**: {{ X }}%
   - **Functions**: {{ X }}%
   - **Lines**: {{ X }}%
   
   ### Test Files
   - `__tests__/{{ file }}.test.ts` ({{ count }} tests)
   - {{ list all test files }}
   
   **Total tests**: {{ count }}
   **Status**: ✅ All passing
   ```

**Output**: Documentation updated ✅

---

## Final Completion

```markdown
✅ TEST GENERATION COMPLETE

Feature: $FEATURE
Coverage: {{ X }}% ✅
Documentation: ✅ Updated

🎉 Tests generated and tracked!
```

---

## Examples

### Example 1: Generate Tests with High Coverage

```bash
/test-from "calculator" --coverage=90
```

**Output**:
```
Reading docs/calculator/phase-3-analysis.md...

Business logic found:
- calculate() - 4 operations
- validateInput() - type checking
- formatResult() - display logic

Generating tests...

Created:
- calculator.test.ts (20 tests)
- validation.test.ts (8 tests)
- formatting.test.ts (5 tests)

Coverage: 93% (target: 90%) ✅
All tests passing ✅
```

### Example 2: Focus on Integration Tests

```bash
/test-from "auth" --type="integration"
```

**Output**:
```
Skipping unit tests (--type=integration)

Generating integration tests...

Created:
- auth-flow.integration.test.ts (15 tests)
  - Login flow
  - Logout flow
  - Password reset
  - Session management
  - Token refresh

All integration tests passing ✅
```

### Example 3: Preview Mode

```bash
/test-from "payment" --preview
```

**Output**:
```
📋 Test Plan Preview

Would create:
- payment.test.ts (12 tests)
- stripe-integration.test.ts (8 tests)
- payment-flow.integration.test.ts (10 tests)

Estimated coverage: 87%
Execution time: ~2 hours

To generate: /test-from "payment"
```

---

## Related Commands

- `/how [feature]` - Explore code (prerequisite)
- `/test-master [target]` - Alternative adversarial testing
- `/add-tests [file]` - Add tests to specific file

---

## Pro Tips

1. **Explore thoroughly first**:
   ```bash
   /how "feature" --comprehensive
   # More detailed docs = better test generation
   ```

2. **Set realistic coverage targets**:
   - 80-85% for most code
   - 90%+ for critical business logic
   - 100% not always necessary

3. **Review generated tests**:
   - Are assertions meaningful?
   - Do edge cases make sense?
   - Adjust as needed

4. **Combine with TDD**:
   ```bash
   /test-from "feature"  # Generate base tests
   # Then manually add specific cases
   ```

---

**Remember**: Generated tests are a great starting point, but review and adjust for your specific requirements!
