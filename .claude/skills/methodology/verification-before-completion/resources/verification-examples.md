# Verification Examples

This document provides detailed, real-world examples of the 5-step verification process.

## Example 1: Test Suite Verification

```markdown
## Task: Implement user authentication

### Step 1: IDENTIFY
Claim: "All tests pass"
Command: npm test

### Step 2: EXECUTE
$ npm test

### Step 3: READ
Test Suites: 12 passed, 12 total
Tests:       156 passed, 156 total
Snapshots:   0 total
Time:        3.456 s

### Step 4: VERIFY
- ✓ 156 tests passing
- ✓ 0 tests failing
- ✓ All test suites passing
- Matches claim "All tests pass"

### Step 5: CLAIM
✓ All authentication tests pass (156/156) - verified at 14:32:10
```

## Example 2: Bug Fix Verification

```markdown
## Task: Fix login timeout error

### Before Fix - Step 1-3:
$ npm test -- --grep "login timeout"
FAIL: should handle login timeout (2.3ms)

### After Fix - Step 1-5:
$ npm test -- --grep "login timeout"
PASS: should handle login timeout (15ms)

### Step 4: VERIFY
- Test now passes
- Specific error case fixed
- No regression in related tests

### Step 5: CLAIM
✓ Login timeout bug fixed - test passes, verified with red-green cycle
```

## Example 3: Build Verification

```markdown
## Task: Optimize bundle size

### Step 1: IDENTIFY
Claim: "Build succeeds and bundle is under 1MB"
Command: npm run build && du -h dist/

### Step 2: EXECUTE
$ npm run build && du -h dist/
Build completed in 2.3s
987K    dist/

### Step 4: VERIFY
- ✓ Build succeeds (exit code 0)
- ✓ Bundle size: 987K (< 1MB requirement)
- ✓ No build errors

### Step 5: CLAIM
✓ Build optimized - succeeds at 987K (under 1MB target)
```

## Example 4: Agent Work Verification

```markdown
## Task: Review agent's database migration fix

### Agent Report:
"Fixed migration script - all good"

### Independent Verification:
$ npm run migration:up
Migration successful

$ npm run migration:status
All migrations applied

$ npm test -- --grep "database"
Tests: 45 passing, 0 failing

### Step 5: CLAIM
✓ Migration fix verified - applied successfully, tests pass
```

## Example 5: Multi-language Verification

### Python Project
```markdown
## Task: Add input validation to API endpoint

### Verification:
$ pytest tests/test_api.py -v
============================= test session starts ==============================
collected 24 items

tests/test_api.py::TestValidation::test_required_fields PASSED
tests/test_api.py::TestValidation::test_email_format PASSED
tests/test_api.py::TestValidation::test_phone_format PASSED
...
============================== 24 passed in 1.23s ===============================

### Claim:
✓ Input validation complete - all 24 API tests pass, edge cases covered
```

### TypeScript Project
```markdown
## Task: Refactor user service to use async/await

### Verification:
$ npm run typecheck
> typecheck
> tsc --noEmit

$ npm test -- test/user-service.test.ts
> test
> jest test/user-service.test.ts

PASS src/__tests__/user-service.test.ts
  UserService
    ✓ should create user async
    ✓ should handle duplicate email
    ✓ should validate input
    ...
Test Suites: 1 passed, 1 total
Tests:       8 passed, 8 total

### Claim:
✓ UserService refactored - typecheck passes, 8/8 tests pass
```

## Example 6: E2E Test Verification

```markdown
## Task: Implement checkout flow

### Verification:
$ npm run test:e2e
> e2e
> playwright test

Running 5 tests using 1 worker
  ✓ [chromium] › checkout.spec.ts:3:1 › Checkout Flow (2.3s)
  ✓ [firefox] › checkout.spec.ts:3:1 › Checkout Flow (2.1s)
  ✓ [webkit] › checkout.spec.ts:3:1 › Checkout Flow (2.4s)
  ✓ [mobile] › checkout.spec.ts:3:1 › Checkout Flow (2.6s)
  ✓ [tablet] › checkout.spec.ts:3:1 › Checkout Flow (2.2s)

  5 passed (12.3s)

### Claim:
✓ Checkout flow implemented - E2E tests pass on all 5 browsers
```

## Example 7: Performance Verification

```markdown
## Task: Optimize database queries

### Verification:
$ npm run test:performance
> performance
> node scripts/benchmark.js

Before optimization:
- User list: 2.3s
- User search: 1.8s
- User analytics: 4.2s

After optimization:
- User list: 0.4s (82% improvement)
- User search: 0.3s (83% improvement)
- User analytics: 0.8s (81% improvement)

$ npm test  # Ensure no regressions
Tests: 234 passing, 0 failing

### Claim:
✓ Database optimized - queries 80% faster, all tests pass
```

## Example 8: Security Verification

```markdown
## Task: Add rate limiting to API

### Verification:
$ npm run test:security
> security
> npm audit

audited 1234 packages in 2.345s

# npm audit report
No vulnerabilities found

$ npm run test:load
> load
> artillery run load-test.yml

All requests passed:
- 1000 requests in 30s
- 0 errors
- Average response time: 120ms
- Max requests per IP: 10 (rate limited)

### Claim:
✓ Rate limiting implemented - passes security audit, handles load test
```

## Example 9: Documentation Verification

```markdown
## Task: Update API documentation

### Verification:
$ npm run build:docs
> build:docs
> redoc-cli build api/openapi.yaml

Documentation built successfully: docs/index.html

$ npm run test:docs
> test:docs
> spectral lint api/openapi.yaml

OpenAPI 3.0.0 valid.
0 errors, 0 warnings

### Manual verification:
- ✓ All endpoints documented
- ✓ Examples provided
- ✓ Authentication documented
- ✓ Error responses documented

### Claim:
✓ API docs updated - builds without errors, passes Spectral validation
```

## Example 10: Migration Verification

```markdown
## Task: Migrate from v1 to v2 API

### Verification:
$ npm run test:backward-compatibility
> test:bc
> node scripts/test-compatibility.js

Testing v1 clients against v2 API...
✓ List users endpoint
✓ Get user endpoint
✓ Create user endpoint
✓ Update user endpoint
✓ Delete user endpoint

$ npm test -- --grep "v2"
Tests: 89 passing, 0 failing

### Claim:
✓ API v2 migration complete - backward compatible, 89 tests pass
```

## Common Verification Pitfalls

### 1. Partial Test Run
```markdown
❌ BAD: Ran `npm test -- --grep "specific"` and claimed "all tests pass"
✅ GOOD: Ran `npm test` without filters, verified full test suite
```

### 2. Ignoring Warnings
```markdown
❌ BAD: Build had warnings but claimed "build succeeds"
✅ GOOD: Build with warnings noted, or fixed warnings before claiming success
```

### 3. No Baseline Comparison
```markdown
❌ BAD: "Performance improved" without measuring before
✅ GOOD: "Performance improved from 2.3s to 0.4s (82% improvement)"
```

### 4. Missing Edge Cases
```markdown
❌ BAD: Tested happy path only
✅ GOOD: Tested happy path, error cases, edge cases, boundary conditions
```