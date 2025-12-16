# Test Runner Usage Examples

Real-world examples of test verification workflows.

## Example 1: Jest Test Suite - All Pass

### Input
```markdown
VERIFICATION REQUEST: A.1

TASK: A.1 - Create theme sanitizer
Files Changed: src/lib/theme-sanitizer.ts

VERIFICATION:
- Command: `npm test theme-sanitizer`
- Expected: All tests pass, coverage >90%
```

### Execution
```bash
$ npm test theme-sanitizer

PASS src/lib/__tests__/theme-sanitizer.test.ts
  sanitizeCSS
    ✓ should sanitize malicious CSS (3ms)
    ✓ should preserve safe CSS (2ms)
    ✓ should handle empty strings (1ms)
  sanitizeThemeConfig
    ✓ should sanitize all fields (4ms)
    ✓ should handle partial configs (2ms)

Tests: 5 passed, 5 total
Time: 0.847s
Coverage: 95.2%
```

### Output
```markdown
## VERIFICATION RESULTS: A.1

### Execution
Command: `npm test theme-sanitizer`
Exit Code: 0
Duration: 0.85s
Status: ✅ PASS

### Results
Tests Passed: 5/5
Coverage: 95.2%

All sanitization tests verified successfully.
```

---

## Example 2: TypeScript Type Check - Errors Found

### Input
```markdown
VERIFICATION REQUEST: B.2

TASK: B.2 - Add validation to theme provider
Files Changed: src/components/ThemeProvider.tsx

VERIFICATION:
- Command: `npm run type-check`
- Expected: 0 TypeScript errors
```

### Execution
```bash
$ npm run type-check

src/components/ThemeProvider.tsx:42:10 - error TS2322: Type 'string | undefined' is not assignable to type 'string'.

42     const theme: string = config.theme;
            ~~~~~

src/components/ThemeProvider.tsx:55:5 - error TS2345: Argument of type 'ThemeConfig | null' is not assignable to parameter of type 'ThemeConfig'.

55     applyTheme(sanitized);
       ~~~~~~~~~~

Found 2 errors.
```

### Output
```markdown
## VERIFICATION RESULTS: B.2

### Execution
Command: `npm run type-check`
Exit Code: 2
Duration: 1.2s
Status: ❌ FAIL

### Results
TypeScript Errors: 2

#### Error 1
**Location**: `src/components/ThemeProvider.tsx:42:10`
**Code**: TS2322
**Message**: Type 'string | undefined' is not assignable to type 'string'

**Analysis**: The `config.theme` property can be undefined, but the variable is typed as string.

#### Error 2
**Location**: `src/components/ThemeProvider.tsx:55:5`
**Code**: TS2345
**Message**: Argument of type 'ThemeConfig | null' is not assignable to parameter of type 'ThemeConfig'

**Analysis**: The sanitize function can return null, but applyTheme expects non-null.

### Suggested Fix
\```typescript
// Line 42: Add null coalescing
const theme: string = config.theme ?? 'default';

// Line 55: Add null check
if (sanitized) {
  applyTheme(sanitized);
}
\```

**Explanation**: Handle potential null/undefined values with proper guards or defaults.
```

---

## Example 3: Test Failure with Auto-Fix

### Input
```markdown
VERIFICATION REQUEST: C.1

TASK: C.1 - Implement theme persistence
Files Changed: src/hooks/useThemePersistence.ts

VERIFICATION:
- Command: `npm test useThemePersistence`
- Expected: All persistence tests pass
- AUTO-FIX: ENABLED
```

### Execution (Attempt 1)
```bash
$ npm test useThemePersistence

FAIL src/hooks/__tests__/useThemePersistence.test.ts
  ● useThemePersistence › should save theme to localStorage

    TypeError: Cannot read property 'setItem' of undefined

      14 | export function saveTheme(theme: string) {
      15 |   localStorage.setItem('theme', theme);
         |               ^

    at saveTheme (src/hooks/useThemePersistence.ts:15:15)
```

### Auto-Fix Applied
```typescript
// Diagnosis: localStorage not mocked in test environment

// Fix: Add mock check
export function saveTheme(theme: string) {
  if (typeof localStorage !== 'undefined') {
    localStorage.setItem('theme', theme);
  }
}
```

### Execution (Attempt 2)
```bash
$ npm test useThemePersistence

PASS src/hooks/__tests__/useThemePersistence.test.ts
  ✓ should save theme to localStorage (5ms)
  ✓ should load theme from localStorage (3ms)

Tests: 2 passed, 2 total
```

### Output
```markdown
## VERIFICATION RESULTS: C.1

### Execution
Command: `npm test useThemePersistence`
Initial Result: FAIL
Final Result: ✅ PASS

### Auto-Fix Attempt

**Initial Error**: TypeError - localStorage undefined in test environment

**Fix Applied**:
\```typescript
// Added environment check
if (typeof localStorage !== 'undefined') {
  localStorage.setItem('theme', theme);
}
\```

**File**: `src/hooks/useThemePersistence.ts:15`

### Retry Results
Tests Passed: 2/2
Duration: 0.3s

✅ Auto-fix successful! Tests now passing.
```

---

## Example 4: Build Failure

### Input
```markdown
VERIFICATION REQUEST: D.1

TASK: D.1 - Bundle theme utilities
Files Changed: Multiple files

VERIFICATION:
- Command: `npm run build`
- Expected: Build succeeds, bundle <500KB
```

### Execution
```bash
$ npm run build

vite v4.5.0 building for production...
✓ 234 modules transformed.

✗ Build failed with 1 error:
Error: Could not resolve './themes/custom' from src/index.ts
```

### Output
```markdown
## VERIFICATION RESULTS: D.1

### Execution
Command: `npm run build`
Exit Code: 1
Duration: 2.3s
Status: ❌ FAIL

### Results
Build Failed

**Error**: Module resolution failure
**Missing**: `./themes/custom`
**Imported from**: `src/index.ts`

### Error Analysis
**Type**: Import Error
**Root Cause**: The file `./themes/custom` doesn't exist or path is incorrect

**Investigation**:
\```bash
# Check if file exists
ls src/themes/
# Result: default.ts, corporate.ts, creative.ts
# custom.ts is missing
\```

### Suggested Fix
**Option 1**: Create the missing file
\```bash
touch src/themes/custom.ts
# Then implement custom theme
\```

**Option 2**: Remove the import if not needed
\```typescript
// In src/index.ts, remove:
export { default as customTheme } from './themes/custom';
\```

**Recommendation**: Check task specification to determine which option is correct.
```

---

## Example 5: Lint Violations

### Input
```markdown
VERIFICATION REQUEST: E.1

TASK: E.1 - Add error handling
Files Changed: src/utils/error-handler.ts

VERIFICATION:
- Command: `npm run lint`
- Expected: No lint errors
```

### Execution
```bash
$ npm run lint

src/utils/error-handler.ts
  15:7   error    'error' is defined but never used  @typescript-eslint/no-unused-vars
  23:1   warning  Unexpected console statement        no-console
  42:82  error    Line exceeds 80 characters          max-len

✖ 3 problems (2 errors, 1 warning)
```

### Output
```markdown
## VERIFICATION RESULTS: E.1

### Execution
Command: `npm run lint`
Exit Code: 1
Status: ❌ FAIL

### Results
Lint Violations: 3 (2 errors, 1 warning)

#### Line 15
**Severity**: Error
**Rule**: @typescript-eslint/no-unused-vars
**Message**: 'error' is defined but never used

**Fix**: Remove unused variable or prefix with underscore
\```typescript
const _error = new Error(); // Or remove if truly unused
\```

#### Line 23
**Severity**: Warning
**Rule**: no-console
**Message**: Unexpected console statement

**Fix**: Use proper logger or remove console.log
\```typescript
logger.error('Error occurred'); // Instead of console.log
\```

#### Line 42
**Severity**: Error
**Rule**: max-len
**Message**: Line exceeds 80 characters

**Fix**: Break line into multiple lines
\```typescript
// Before (long line)
const message = `This is a very long error message that exceeds the maximum line length`;

// After (split)
const message = `This is a very long error message ` +
  `that exceeds the maximum line length`;
\```

### Summary
Fix 2 hard errors, 1 warning. All fixes are straightforward formatting/cleanup.
```

---

## Example 6: E2E Test with Screenshot

### Input
```markdown
VERIFICATION REQUEST: F.1

TASK: F.1 - Add theme switcher UI
Files Changed: src/components/ThemeSwitcher.tsx

VERIFICATION:
- Command: `npm run test:e2e -- theme-switcher`
- Expected: UI tests pass, theme switches correctly
```

### Execution
```bash
$ npm run test:e2e -- theme-switcher

Running 3 tests using 1 worker

  ✓ theme-switcher.spec.ts:5 › should display theme options (1.2s)
  ✗ theme-switcher.spec.ts:15 › should switch theme on click (timeout)
  ✓ theme-switcher.spec.ts:25 › should persist theme selection (0.8s)

2 passed, 1 failed
Failures:
  theme-switcher.spec.ts:15 › should switch theme on click
    Timeout 5000ms exceeded waiting for selector ".theme-dark"
    
Screenshot: test-results/theme-switcher-should-switch-theme-0.png
```

### Output
```markdown
## VERIFICATION RESULTS: F.1

### Execution
Command: `npm run test:e2e -- theme-switcher`
Exit Code: 1
Duration: 8.5s
Status: ❌ FAIL

### Results
E2E Tests: 2/3 passed

✅ Passed:
- should display theme options (1.2s)
- should persist theme selection (0.8s)

❌ Failed:
- should switch theme on click

### Failure Details

**Test**: should switch theme on click
**Error**: Timeout waiting for selector `.theme-dark`
**Duration**: 5000ms (timeout)
**Screenshot**: `test-results/theme-switcher-should-switch-theme-0.png`

### Error Analysis
**Type**: Timeout
**Root Cause**: The dark theme class never applied to body/element

**Possible Issues**:
1. Theme switcher onClick handler not triggering
2. Theme state not updating
3. CSS class not being applied
4. Selector is incorrect (wrong class name)

### Suggested Fix
\```typescript
// Check if onClick is properly bound
\u003cbutton onClick={() => setTheme('dark')}\u003e

// Verify theme state updates
useEffect(() => {
  document.body.className = `theme-${currentTheme}`;
}, [currentTheme]);

// Or check if selector matches actual output
// Maybe it's "dark-theme" not "theme-dark"?
\```

### Debug Steps
1. View screenshot at `test-results/theme-switcher-should-switch-theme-0.png`
2. Check what class is actually applied
3. Verify onClick handler in component
4. Add console.log to track theme state
```

---

## Tips from Examples

### DO:
✅ Parse output systematically by error type  
✅ Extract file locations and line numbers  
✅ Provide specific, actionable fixes  
✅ Group related errors together  
✅ Reference screenshots/artifacts when available  
✅ Explain root cause, not just symptoms

### DON'T:
❌ Just dump raw error output  
❌ Suggest vague "check the code" fixes  
❌ Miss important details in output  
❌ Ignore warnings (they often indicate real issues)  
❌ Auto-fix complex logic failures  
❌ Skip verification of auto-fixes

### Key Patterns

1. **Always categorize**: Test/Type/Build/Lint helps diagnosis
2. **Extract cleanly**: File, line, error type, message
3. **Explain cause**: Don't just show error, explain why
4. **Suggest fix**: Provide code snippet when possible
5. **Verify results**: Re-run after auto-fix
6. **Report clearly**: Structure makes output scannable
