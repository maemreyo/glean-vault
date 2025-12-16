# Error Handling & Auto-Fix Strategies

Comprehensive guide for diagnosing and automatically fixing common code errors.

## Auto-Fix Philosophy

**Goals:**
- Fix simple, mechanical errors automatically
- Provide clear diagnosis for complex errors
- Learn from project patterns
- Preserve developer intent

**When to auto-fix:**
- Missing imports for standard libraries
- Basic type annotations
- Unused variable cleanup
- Common syntax patterns

**When NOT to auto-fix:**
- Design/architectural issues
- Breaking changes required
- Ambiguous solutions
- Security-sensitive code

## Common TypeScript Errors

### 1. Cannot find name 'X'

**Diagnosis**: Missing import

**Auto-fix Strategy:**
```typescript
// Error: Cannot find name 'React'

// Step 1: Check if it's a standard library
const standardImports = {
  'React': "import React from 'react';",
  'useState': "import { useState } from 'react';",
  'axios': "import axios from 'axios';",
  'lodash': "import _ from 'lodash';"
};

// Step 2: Check project files
grep_search "export.*React" 

// Step 3: Add import at top
import React from 'react';  // ← Auto-add
```

**Fix Pattern:**
1. Identify missing symbol
2. Search for export in project (`grep_search "export.*SymbolName"`)
3. If found: Add relative import
4. If not found: Check if it's standard library
5. Add import in correct section

### 2. Type 'X' is not assignable to type 'Y'

**Diagnosis**: Type mismatch

**Auto-fix Strategy:**
```typescript
// Error: Type 'string' is not assignable to type 'number'
const count: number = "5";  // ❌

// Fix 1: Add conversion (if safe)
const count: number = parseInt("5", 10);  // ✅

// Fix 2: Change type annotation (if appropriate)
const count: string = "5";  // ✅

// Fix 3: Add type assertion (as last resort)
const count = "5" as any as number;  // ⚠️ Use sparingly
```

**Decision Tree:**
```
Type mismatch detected
  ├─ Value is literal → Suggest type change
  ├─ Conversion exists (string→number) → Apply conversion
  ├─ Union type possible → Use union (string | number)
  └─ Complex case → Report, don't auto-fix
```

### 3. Property 'X' does not exist on type 'Y'

**Diagnosis**: Missing property or wrong type

**Auto-fix Strategy:**
```typescript
// Error: Property 'username' does not exist on type 'User'

// Step 1: Check type definition
interface User {
  name: string;
  email: string;
}

// Step 2: Determine fix
// Option A: Property name typo
user.username // ❌
user.name     // ✅ Auto-suggest correction

// Option B: Add to interface (if specification requires it)
interface User {
  name: string;
  email: string;
  username: string;  // ← Auto-add if in task spec
}

// Option C: Make optional
interface User {
  name: string;
  email: string;
  username?: string;  // ← Add as optional
}
```

### 4. 'X' is declared but never used

**Diagnosis**: Unused import or variable

**Auto-fix Strategy:**
```typescript
// Error: 'React' is declared but its value is never read
import React from 'react';  // ❌ Not used in file

// Fix: Remove unused import
// (Check if file uses JSX first)

// Error: 'temp' is declared but never used
function process() {
  const temp = calculate();  // ❌
  return 42;
}

// Fix 1: Use the variable
function process() {
  const temp = calculate();
  return temp;  // ✅
}

// Fix 2: Remove if truly unused
function process() {
  return 42;  // ✅
}

// Fix 3: Prefix with _ if intentionally unused
function process(_temp: number) {  // ✅ Tells linter it's intentional
  return 42;
}
```

### 5. Cannot find module 'X'

**Diagnosis**: Missing package or wrong path

**Auto-fix Strategy:**
```typescript
// Error: Cannot find module 'lodash'

// Step 1: Check if it's a dependency
// Look in package.json

// Step 2: If missing, check task spec
// Task might require: "Use lodash for groupBy"
// → Note: Package needs to be installed first

// Step 3: If wrong path
import { utils } from './utls';  // ❌ Typo
import { utils } from './utils'; // ✅ Auto-fix

// Use file search to find correct path
grep_search "export.*utils"
```

### 6. Duplicate identifier 'X'

**Diagnosis**: Name collision

**Auto-fix Strategy:**
```typescript
// Error: Duplicate identifier 'User'
interface User { }
class User { }  // ❌

// Fix 1: Rename one (convention-based)
interface User { }
class UserImpl { }  // ✅

interface UserType { }
class User { }  // ✅

// Fix 2: Use namespace
namespace Models {
  export interface User { }
}
class User { }  // ✅
```

## Common JavaScript Errors

### 1. Unexpected token

**Diagnosis**: Syntax error

**Auto-fix Strategy:**
```javascript
// Error: Unexpected token ')'
function calculate(a, b,) {  // ❌ Trailing comma in old JS
  return a + b;
}

// Fix: Remove trailing comma
function calculate(a, b) {  // ✅
  return a + b;
}
```

### 2. Missing semicolon

**Auto-fix:** Add semicolon (if project uses them)

```javascript
const x = 5  // ❌ (if project uses semicolons)
const x = 5; // ✅
```

Check project style first:
```bash
# Look at existing files
view_file src/index.js | grep -c ";"
```

### 3. Undefined variable

**Diagnosis**: Variable not declared

**Auto-fix Strategy:**
```javascript
// Error: result is not defined
function process() {
  result = calculate();  // ❌
  return result;
}

// Fix: Add declaration
function process() {
  const result = calculate();  // ✅
  return result;
}
```

## React-Specific Errors

### 1. React is not defined

**Diagnosis**: Missing React import (React 16 and below)

**Auto-fix:**
```jsx
// Error in React 16: React is not defined
export function Component() {  // ❌
  return <div>Hello</div>;
}

// Fix: Add React import
import React from 'react';  // ✅
export function Component() {
  return <div>Hello</div>;
}
```

Note: React 17+ with new JSX transform doesn't need this.

### 2. Invalid hook call

**Diagnosis**: Hook used incorrectly

```jsx
// Error: Hooks can only be called inside function components
class Component extends React.Component {
  render() {
    const [state] = useState(0);  // ❌
    return <div>{state}</div>;
  }
}

// Fix: Convert to function component
function Component() {  // ✅
  const [state] = useState(0);
  return <div>{state}</div>;
}
```

**Auto-fix:** Only if task specifies conversion; otherwise report error.

## Auto-Fix Workflow

```
1. Run syntax check
   ↓
2. Parse error output
   ↓
3. Categorize error type
   ↓
4. Check if auto-fixable
   ├─ Yes → Apply fix pattern
   │         ↓
   │      Re-run validation
   │         ↓
   │      Success? → Done
   │         ↓ No
   │      Try alternative fix
   │         ↓
   │      Max attempts? → Report
   │
   └─ No → Report with diagnosis
```

## Fix Patterns Library

### Pattern: Add Import

```typescript
// Template
import { SYMBOL } from 'PACKAGE';

// Or for default
import SYMBOL from 'PACKAGE';

// Or for relative
import { SYMBOL } from './relative/path';
```

### Pattern: Add Type Annotation

```typescript
// Template
const variable: TYPE = value;

// Or for function
function name(param: TYPE): RETURN_TYPE { }
```

### Pattern: Fix Async/Await

```typescript
// Before
function fetchData() {
  return axios.get('/api');  // ❌ Returns Promise
}

// After
async function fetchData() {  // ✅ Add async
  return await axios.get('/api');  // Add await
}
```

### Pattern: Null Safety

```typescript
// Before
const value = obj.property.nested;  // ❌ Can be null

// After
const value = obj?.property?.nested;  // ✅ Optional chaining

// Or
const value = obj && obj.property && obj.property.nested;
```

## Error Report Format

When auto-fix fails, provide detailed report:

```markdown
## Syntax Error - Cannot Auto-Fix

**Error**: Type 'UserInput' is not assignable to type 'ValidatedUser'

**Location**: `src/validators/user.ts:45:12`

**Diagnosis**: 
The UserInput interface is missing required properties that ValidatedUser expects:
- `isVerified: boolean`
- `verificationDate: Date`

**Suggested Fix**:
Add missing properties to UserInput or create a type guard:

```typescript
function isValidatedUser(user: UserInput): user is ValidatedUser {
  return user.isVerified && user.verificationDate !== null;
}
```

**Why Auto-Fix Skipped**:
This requires understanding of business logic and validation rules.
Cannot determine correct approach automatically.

**Next Steps**:
1. Review task specification for validation requirements
2. Decide if UserInput should include these fields
3. Or create proper type guard/converter function
```

## Max Attempts & Fallback

```typescript
const MAX_FIX_ATTEMPTS = 3;

let attempts = 0;
while (attempts < MAX_FIX_ATTEMPTS) {
  const errors = runSyntaxCheck();
  
  if (errors.length === 0) {
    return SUCCESS;
  }
  
  const fixable = errors.filter(isAutoFixable);
  
  if (fixable.length === 0) {
    return REPORT_MANUAL_FIX_NEEDED;
  }
  
  applyFixes(fixable);
  attempts++;
}

return REPORT_MAX_ATTEMPTS_EXCEEDED;
```

## Learning from Project

Before applying fixes, learn project patterns:

```bash
# Check how project handles imports
view_file src/components/Button.tsx
# Note: Uses named imports, no React import (React 17+)

# Check type annotation style
grep_search "interface.*Props"
# Note: Props interfaces use PascalCase with "Props" suffix

# Check error handling
grep_search "try.*catch"
# Note: Project uses custom error classes
```

Apply fixes consistent with project style.

## Safety Checks

Before applying any fix:
- [ ] Does fix match task specification?
- [ ] Does fix follow project conventions?
- [ ] Will fix preserve existing functionality?
- [ ] Is fix the minimal change needed?
- [ ] Can fix be explained clearly?

If any check fails → Don't auto-fix, report instead.