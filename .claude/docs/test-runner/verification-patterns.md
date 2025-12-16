# Verification Patterns

Comprehensive guide for running different types of verification commands.

## Test Frameworks

### Pattern 1: npm test (Jest/Vitest)

**Command patterns**:
```bash
npm test
npm test -- pattern
npm test -- --run
npm test -- --coverage
```

**Output parsing**:
```bash
# Success pattern
✓ Test suite passed
PASS tests/module.test.ts
  ✓ should work (3ms)
  
Tests: 5 passed, 5 total

# Failure pattern
FAIL tests/module.test.ts
  ✗ should work
    Expected: 5
    Received: 4
    
Tests: 4 passed, 1 failed, 5 total
```

**Extract**:
- Pass count: Look for "X passed"
- Fail count: Look for "X failed"
- Coverage: Look for "Coverage: X%"
- Duration: Look for "(Xms)" or total time
- Failed test names: After "✗" or "FAIL"

### Pattern 2: TypeScript Type Check

**Command patterns**:
```bash
npm run type-check
npx tsc --noEmit
npx tsc --noEmit src/
```

**Output parsing**:
```bash
# Success
Found 0 errors.

# Failure  
src/file.ts:42:10 - error TS2322: Type 'string' is not assignable to type 'number'.
src/other.ts:15:5 - error TS2345: Argument of type 'X' is not assignable to parameter of type 'Y'.

Found 2 errors.
```

**Extract**:
- Error count: "Found X errors"
- Error codes: "TS2322", "TS2345", etc.
- Locations: "file.ts:line:col"
- Messages: After " - error TSXXXX:"

### Pattern 3: Build Commands

**Command patterns**:
```bash
npm run build
vite build
next build
```

**Output parsing**:
```bash
# Success
✓ built in 1.23s
dist/index.js  45.2 kB

# Failure
✗ Build failed with 3 errors:
Error: Cannot resolve module 'X'
```

**Extract**:
- Build status: "built in" or "Build failed"
- Bundle size: Look for kB/MB
- Errors: Lines starting with "Error:"
- Warnings: Lines starting with "Warning:"

### Pattern 4: Linters

**Command patterns**:
```bash
npm run lint
npx eslint src/
npx biome check
```

**Output parsing**:
```bash
# ESLint
src/component.tsx
  42:10  error    'x' is defined but never used  no-unused-vars
  45:1   warning  Missing semicolon               semi
  
✖ 2 problems (1 error, 1 warning)

# Biome
src/component.tsx:42:10 lint/suspicious/noUnusedVariables
  × This variable is unused.
```

**Extract**:
- File path: First non-whitespace text
- Line:col: "42:10" format
- Severity: "error" or "warning"
- Rule name: Last part of line
- Total count: "X problems"

## Coverage Reports

**Pattern**: Coverage percentage

```bash
# Jest/Vitest
-------------|---------|----------|---------|---------|
File         | % Stmts | % Branch | % Funcs | % Lines |
-------------|---------|----------|---------|---------|
module.ts    |   95.23 |    87.50 |  100.00 |   94.44 |
-------------|---------|----------|---------|---------|

# Or inline
Coverage: 85.5% Statements 234/274
```

**Extract**:
- Overall coverage: Look for "Coverage: X%"
- Per-file: Parse table rows
- Thresholds: Compare against expected (from task)

## Performance Benchmarks

**Pattern**: Execution time

```bash
# Test duration
Test Suites: 5 passed, 5 total
Time:        2.345s

# Build time
⚡ Built in 1.23s
```

**Extract**:
- Total time: Look for "Time:" or "in Xs"
- Per-test time: "(Xms)" after test names
- Warn if: >5s for tests, >10s for builds

## E2E Tests (Playwright/Cypress)

**Command patterns**:
```bash
npm run test:e2e
npx playwright test
npx cypress run
```

**Output parsing**:
```bash
# Playwright
Running 15 tests
  ✓ login flow (1.2s)
  ✗ checkout flow (timeout)
  
15 passed, 1 failed

# Cypress
  login.spec.ts
    ✓ should login successfully (847ms)
    1) should handle invalid credentials
```

**Extract**:
- Test names: After ✓ or ✗
- Durations: in parentheses
- Failures: Lines with numbers like "1)"
- Screenshots: Look for "Screenshot:" paths

## Custom Commands

**Pattern**: Generic command output

```bash
# Any command
npm run custom-check
```

**Parse strategy**:
1. Check exit code (0 = success)
2. Look for common success patterns:
   - "success", "passed", "ok", "✓"
3. Look for failure patterns:
   - "error", "failed", "✗", "FAIL"
4. If ambiguous, report raw output

## Parsing Decision Tree

```
1. Check exit code
   ├─ 0 → Likely success
   └─ non-zero → Likely failure

2. Analyze command type
   ├─ Contains "test" → Parse test framework output
   ├─ Contains "type-check" or "tsc" → Parse TypeScript errors
   ├─ Contains "build" → Parse build output
   ├─ Contains "lint" → Parse lint violations
   └─ Unknown → Generic parsing

3. Extract details
   ├─ Test: counts, names, assertions
   ├─ Type: error codes, locations
   ├─ Build: bundle info, errors
   └─ Lint: files, rules, severity

4. Format results
   └─ Use structured output template
```

## Best Practices

1. **Always capture full output**: Useful for debugging
2. **Parse incrementally**: Don't try to parse everything at once
3. **Handle variations**: Different tools format differently
4. **Contextualize errors**: Show surrounding code if possible
5. **Prioritize actionable info**: What file, what line, what fix

## Example Parsing Code

```typescript
function parseTestOutput(output: string): TestResults {
  // Look for pass/fail counts
  const passMatch = output.match(/(\d+) passed/);
  const failMatch = output.match(/(\d+) failed/);
  
  // Extract failed test names
  const failedTests = output
    .split('\n')
    .filter(line => line.includes('✗') || line.includes('FAIL'))
    .map(extractTestName);
  
  return {
    passed: passMatch ? parseInt(passMatch[1]) : 0,
    failed: failMatch ? parseInt(failMatch[1]) : 0,
    failedTests,
    status: failMatch ? 'FAIL' : 'PASS'
  };
}
```
