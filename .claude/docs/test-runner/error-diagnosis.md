# Error Diagnosis Guide

Systematic approach to diagnosing test failures and identifying root causes.

## Diagnosis Framework

### 1. Categorize Error Type

```
Error Type Decision Tree:

Exit code non-zero?
├─ Contains "expected" vs "received" → Assertion Failure
├─ Contains "TS" error code → Type Error
├─ Contains "Cannot find module" → Import Error
├─ Contains "SyntaxError" → Syntax Error
├─ Contains "TypeError" or "ReferenceError" → Runtime Error
├─ Contains "timeout" → Timeout Error
└─ Unknown → Generic Failure
```

### 2. Locate Error Source

**From stack trace**:
```
Error: Test failed
    at Object.<anonymous> (/path/to/test.ts:42:10)
    at process._tickCallback (internal/process/next_tick.js:68:7)
```

Extract:
- File: `/path/to/test.ts`
- Line: `42`
- Column: `10`

**From test framework**:
```
FAIL tests/module.test.ts
  ● suite name › test name
  
    expect(received).toBe(expected)
    
    at tests/module.test.ts:15:23
```

Extract:
- Test file: `tests/module.test.ts`
- Test name: "test name"
- Line: `15`

### 3. Identify Root Cause

Read code at error location and analyze:
- What was expected?
- What actually happened?
- Why did it happen?
- What needs to change?

## Error Type Diagnosis

### Assertion Failures

**Symptoms**:
```
Expected: 5
Received: 4

expect(result).toBe(true)
Received: false
```

**Diagnosis steps**:
1. Read the assertion: What's being tested?
2. Check implementation: Is logic correct?
3. Check test: Is expectation correct?
4. Trace data flow: Where does value come from?

**Common causes**:
- Off-by-one errors
- Wrong calculation
- Missing edge case handling
- Test expectation outdated

**Fix strategy**:
- If logic wrong: Fix implementation
- If test wrong: Update test expectation
- If edge case: Add handling in code

### Type Errors

**Symptoms**:
```
error TS2322: Type 'string' is not assignable to type 'number'
error TS2345: Argument of type 'X' is not assignable to parameter of type 'Y'
error TS2339: Property 'foo' does not exist on type 'Bar'
```

**Diagnosis steps**:
1. Identify mismatched types
2. Check variable/parameter declaration
3. Trace value source
4. Determine correct type

**Common causes**:
- Missing type annotation
- Incorrect type declaration
- Type inference failure
- API mismatch

**Fix strategy**:
- Add explicit type annotations
- Fix type declarations
- Add type guards
- Use type assertions (cautiously)

### Import Errors

**Symptoms**:
```
Cannot find module 'lodash'
Module not found: Can't resolve './utils/helper'
```

**Diagnosis steps**:
1. Check if module exists in node_modules
2. Verify import path is correct
3. Check if file exists at path
4. Verify exports from target module

**Common causes**:
- Typo in module name or path
- Missing npm package
- Wrong relative path
- File moved/renamed

**Fix strategy**:
- Correct typo
- Install missing package
- Fix relative path
- Update import after file move

### Syntax Errors

**Symptoms**:
```
SyntaxError: Unexpected token '}'
ParseError: Expected identifier
```

**Diagnosis steps**:
1. Look at line number from error
2. Check for:
   - Missing/extra brackets
   - Missing semicolons (if required)
   - Invalid JavaScript/TypeScript syntax

**Common causes**:
- Unmatched brackets/parentheses
- Typo in keyword
- Invalid syntax for language version

**Fix strategy**:
- Match brackets/parentheses
- Correct keyword spelling
- Fix syntax to valid form

### Runtime Errors

**Symptoms**:
```
TypeError: Cannot read property 'length' of undefined
ReferenceError: variable is not defined
TypeError: obj.method is not a function
```

**Diagnosis steps**:
1. Identify which variable/property caused error
2. Trace where it should be defined
3. Check initialization
4. Verify control flow

**Common causes**:
- Accessing property on null/undefined
- Variable used before initialization
- Async timing issues
- Wrong API usage

**Fix strategy**:
- Add null checks
- Initialize variables properly
- Use optional chaining (?.)
- Fix async/await handling

### Timeout Errors

**Symptoms**:
```
Test timeout of 5000ms exceeded
Timeout - Async callback was not invoked within timeout
```

**Diagnosis steps**:
1. Check if test has async operations
2. Verify promises are resolved/rejected
3. Check for infinite loops
4. Look for missing done() calls

**Common causes**:
- Forgotten await
- Promise never resolves
- Infinite loop
- Slow operation

**Fix strategy**:
- Add await to async calls
- Ensure promises resolve
- Fix loop conditions
- Increase timeout or optimize code

## Diagnostic Checklist

For any test failure, answer:

- [ ] What type of error is it?
- [ ] Which file and line caused it?
- [ ] What was the code trying to do?
- [ ] Why did it fail?
- [ ] Is it a code bug or test bug?
- [ ] What's the minimal fix?
- [ ] Are there related failures?

## Reading Stack Traces

```
Error: Test failed
    at functionC (/src/utils.ts:15:10)
    at functionB (/src/processor.ts:42:5)
    at functionA (/src/index.ts:89:12)
    at Test.runTest (/node_modules/vitest/...)
```

Read bottom-to-top for call chain:
1. Test called functionA
2. functionA called functionB
3. functionB called functionC
4. functionC threw error at line 15

Focus on **first non-node_modules entry** (utils.ts:15:10)

## Error Pattern Recognition

Build mental library of patterns:

```typescript
// Pattern 1: Null access
data.forEach(item => item.name)
// If data is null → TypeError

// Pattern 2: Async not awaited
const result = fetchData(); // Missing await
console.log(result.value); // undefined

// Pattern 3: Wrong scope
if (condition) {
  const x = 5;
}
console.log(x); // ReferenceError

// Pattern 4: Type coercion
"5" + 2 // "52" not 7
```

## Multi-Error Diagnosis

When multiple errors appear:

1. **Group by type**: How many of each error type?
2. **Find pattern**: Same file? Same function?
3. **Identify root**: Is one error causing others?
4. **Fix order**: Fix root cause first

Example:
```
10 errors total:
- 7x "Cannot find module './utils'"
- 2x Type errors in files that import utils
- 1x Test failure in component using utils

Root cause: utils.ts was moved/renamed
Fix: Update 7 import statements → fixes all 10 errors
```

## Context Gathering

Before diagnosing, gather context:

```bash
# View the failing test
view_file tests/module.test.ts

# View the implementation
view_file src/module.ts

# Check for related changes
grep_search "functionName"

# Check recent modifications (if in git context)
# See what changed recently
```

## Diagnosis Output Template

```markdown
## Error Diagnosis: [error-type]

### Location
File: `path/to/file.ts:42`
Function: `calculateTotal`

### What Happened
The test expected `calculateTotal([1,2,3])` to return `6`,
but it returned `5`.

### Root Cause
The function uses `reduce((sum, n) => sum + n, 0)` but the
initial value is actually `undefined`, making first iteration
`undefined + 1 = NaN`, then continues incorrectly.

### Fix Required
Change line 42 from:
`return items.reduce((sum, n) => sum + n)`
to:
`return items.reduce((sum, n) => sum + n, 0)`

Add the missing initial value `0`.
```

## Advanced: Flaky Test Diagnosis

If test sometimes passes, sometimes fails:

1. **Race condition**: Async timing issue
2. **Global state**: Tests affecting each other  
3. **Random data**: Test uses Math.random() or Date.now()
4. **External dependency**: API/network flakiness

Diagnosis:
- Run test 10x in a row
- Check for global variables
- Look for timing-dependent code
- Verify test isolation
