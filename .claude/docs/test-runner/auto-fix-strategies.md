# Auto-Fix Strategies

When and how to automatically fix common test failures.

## Auto-Fix Philosophy

**Fix automatically when**:
- Error is mechanical (not logical)
- Solution is unambiguous
- Fix is safe and reversible
- Pattern has been seen before

**DON'T auto-fix when**:
- Logic bug (needs human judgment)
- Multiple possible solutions
- Would mask real problem
- Complex refactoring needed

## Maximum Attempts

**Rule**: Only ONE auto-fix attempt per verification run

Why:
- Prevents infinite loops
- Forces precise fixes
- Maintains safety
- Keeps verification fast

## Auto-Fixable Error Types

### 1. Missing Import

**Pattern**:
```
Cannot find name 'DOMPurify'
Cannot find module 'lodash'
```

**Auto-fix**:
```typescript
// Add to top of file
import DOMPurify from 'dompurify';
```

**Strategy**:
1. Extract symbol name from error
2. Check if it's a known library (use common library map)
3. Or search project for export: `grep_search "export.*DOMPurify"`
4. Add appropriate import statement
5. Place in correct import section

**Safety check**:
- Verify package exists in package.json
- Don't add if ambiguous source

### 2. Missing Type Annotation

**Pattern**:
```
Parameter 'x' implicitly has 'any' type
```

**Auto-fix**:
```typescript
// Before
function process(x) { return x.length; }

// After
function process(x: string) { return x.length; }
```

**Strategy**:
1. Identify parameter needing type
2. Infer type from usage:
   - Uses `.length` → string or array
   - Uses `.toUpperCase()` → string
   - Used in arithmetic → number
3. Add type annotation
4. Use `unknown` if can't infer

**Safety check**:
- Only fix if usage clearly indicates type
- Mark for manual review if uncertain

### 3. Unused Variable

**Pattern**:
```
'tempResult' is declared but its value is never read
```

**Auto-fix Option A** (if used later):
```typescript
// Might be legitimately unused
const tempResult = calculate(); // Don't remove if has side effects
```

**Auto-fix Option B** (parameter):
```typescript
// Before
function handler(event, context) { }

// After (prefix with _)
function handler(_event, _context) { }
```

**Strategy**:
1. Check if variable/parameter is truly unused
2. For unused parameters: Prefix with `_`
3. For unused local variables:
   - If no side effects: Remove
   - If side effects: Keep but consider naming
4. For imports: Remove if safe

**Safety check**:
- Don't remove if has side effects
- Don't remove if used in comments/docs

### 4. Null Safety

**Pattern**:
```
Object is possibly 'null' or 'undefined'
Cannot read property 'length' of undefined
```

**Auto-fix**:
```typescript
// Before
return data.length;

// After (optional chaining)
return data?.length ?? 0;
```

**Strategy**:
1. Add optional chaining `?.`
2. Add nullish coalescing `??` with default value
3. Or add explicit null check if complex

**Safety check**:
- Choose appropriate default value
- Don't mask real null errors

### 5. Syntax Errors (Simple)

**Pattern**:
```
Unexpected token, expected ";"
Missing closing parenthesis
```

**Auto-fix**:
```typescript
// Before
if (condition {

// After
if (condition) {
```

**Strategy**:
1. Identify missing/extra character
2. Apply straightforward fix:
   - Add missing semicolon
   - Add missing bracket
   - Remove extra comma
3. Match project style

**Safety check**:
- Only fix obvious syntax errors
- Don't fix if structure unclear

## Auto-Fix Workflow

```
1. Capture verification error
   ↓
2. Categorize error type
   ↓
3. Check if auto-fixable
   ├─ No → Suggest manual fix
   └─ Yes → Continue
       ↓
4. Generate fix code
   ↓
5. Apply fix with edit_file
   ↓
6. Re-run verification
   ↓
7. Report result:
   ├─ Fixed → Success!
   └─ Still fails → Report both attempts
```

### Step 4: Suggest/Apply Fix

```markdown
{{ if --auto-fix and FAIL }}
AUTO-FIX STRATEGY:

1. Identify fix type needed:
   - Type annotation
   - Import addition
   - Null check
   - Syntax correction

2. Generate fix code

3. Apply fix using edit_file (MCP tool)

4. Re-run verification command

5. Report retry result

{{ else if FAIL }}
SUGGEST FIX:

1. Generate suggested code fix
2. Explain why fix should work
3. Provide specific file/line to modify
{{ endif }}
```

## Fix Templates

### Template 1: Add Import

```typescript
// Location: Top of file, after existing imports
import { SymbolName } from 'package-name';
// or
import SymbolName from 'package-name';
```

### Template 2: Add Type

```typescript
// Location: Parameter or variable declaration
: TypeName
```

### Template 3: Null Check

```typescript
// Pattern A: Optional chaining
object?.property

// Pattern B: Nullish coalescing  
value ?? defaultValue

// Pattern C: Full check
if (value !== null && value !== undefined) {
  // use value
}
```

### Template 4: Prefix Unused

```typescript
// Pattern: Add underscore
_unusedParam
_unusedVariable
```

## Decision Matrix

| Error Type | Auto-fix? | Condition |
|------------|-----------|-----------|
| Missing import | YES | If source is clear |
| Type annotation | YES | If type inferable |
| Unused variable | YES | If safe to remove/prefix |
| Null access | YES | If default value obvious |
| Simple syntax | YES | If fix unambiguous |
| Assertion failure | NO | Needs logic review |
| Complex type error | NO | Needs design decision |
| Runtime logic error | NO | Needs debugging |

## Safety Checks

Before applying any auto-fix:

```typescript
function isSafeToAutoFix(error: Error): boolean {
  // Check 1: Error is in known auto-fixable category
  if (!FIXABLE_ERROR_TYPES.includes(error.type)) {
    return false;
  }
  
  // Check 2: Fix doesn't modify core logic
  if (isLogicChange(error)) {
    return false;
  }
  
  // Check 3: Fix is deterministic
  if (hasMultipleSolutions(error)) {
    return false;
  }
  
  // Check 4: Can verify fix worked
  if (!canVerify(error)) {
    return false;
  }
  
  return true;
}
```

## Example Auto-Fix Session

**Initial error**:
```
src/utils.ts:15:10 - error TS2322: Type 'string | undefined' is not assignable to type 'string'.
```

**Auto-fix applied**:
```typescript
// Before (line 15)
const result: string = data.value;

// After (added null check)
const result: string = data.value ?? '';
```

**Re-run verification**:
```
Found 0 errors.
```

**Report**:
```markdown
Auto-Fix Applied:
Added nullish coalescing operator with empty string default

File: `src/utils.ts:15`
Change: `data.value` → `data.value ?? ''`

Retry Result: PASS
```

## When Auto-Fix Fails

If error persists after auto-fix:

```markdown
## Auto-Fix Attempt

Diagnosis: Type error on line 15

Fix Applied:
\```typescript
const result: string = data.value ?? '';
\```

Retry Result: FAIL

New Error: Type 'number | string' is not assignable to type 'string'

Analysis: The default value should match the actual usage.
The fix addressed null but revealed type inconsistency.

Suggested Manual Fix:
Change type declaration to accept both:
\```typescript
const result: string | number = data.value ?? '';
\```
Or add proper type guard.
```

## Learning from Failures

Track which auto-fixes work:
- Success rate by error type
- Common fix patterns
- Failures needing manual intervention

Improve auto-fix logic over time based on patterns.

## Constraints

- **Time limit**: Auto-fix should take <5 seconds
- **Scope**: Only fix the specific error, not refactor
- **Reversibility**: Changes should be easily undone if wrong
- **Documentation**: Always report what was changed and why
