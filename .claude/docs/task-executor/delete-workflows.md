# DELETE Operation Workflows

Safe file deletion procedures with comprehensive dependency cleanup.

## Core Principles

1. **Impact Analysis First**: Understand what depends on the file
2. **Clean Dependencies**: Remove all references before deleting
3. **Preserve Functionality**: Ensure no broken imports remain
4. **Document Changes**: Track what was cleaned up

## DELETE Workflow

```
1. Analyze Dependencies
   ↓
2. Plan Cleanup
   ↓
3. Clean References
   ↓
4. Validate Changes
   ↓
5. Delete Target File
   ↓
6. Verify Syntax
```

## Step 1: Analyze Dependencies

### Find All References

```bash
# Find direct imports
grep_search "from ['\"]\./path/to/target['\"]"
grep_search "from ['\"]\.\./path/to/target['\"]"

# Find by module name
grep_search "import.*ModuleName"

# Find re-exports
grep_search "export.*from.*target"

# Check index files
grep_search "export.*target" "*/index.ts"
```

### Categorize Dependencies

**Critical** (Must clean):
- Direct imports in source files
- Re-exports in index files
- Type imports in declaration files
- Config references

**Optional** (Consider cleaning):
- Comments mentioning the file
- Documentation references
- Test files (might be okay to leave)

## Step 2: Plan Cleanup

Create cleanup checklist:

```markdown
Target: `src/utils/old-helper.ts`

Dependencies Found:
- [ ] src/components/App.tsx (import oldHelper)
- [ ] src/utils/index.ts (re-export)
- [ ] src/types/index.ts (import types)
- [ ] package.json (if it's a main export)
- [ ] tsconfig.json (if in paths)

Cleanup Strategy:
1. Remove import from App.tsx
2. Remove re-export from utils/index.ts
3. Remove type imports from types/index.ts
4. Update configs if needed
5. Delete target file
6. Run syntax validation
```

## Step 3: Clean References

### Pattern 1: Remove Import Statement

```typescript
// Before
import React from 'react';
import { oldHelper } from './utils/old-helper';  // ← Remove this
import { newHelper } from './utils/new-helper';

export function Component() {
  const result = oldHelper(data);  // ← This will also need fixing
  return <div>{result}</div>;
}

// After
import React from 'react';
import { newHelper } from './utils/new-helper';

export function Component() {
  const result = newHelper(data);  // ← Updated to use replacement
  return <div>{result}</div>;
}
```

**Steps:**
1. Find the import line
2. Check if any destructured items are used
3. Remove entire import if nothing else used
4. Or remove only the specific import if others remain

### Pattern 2: Clean Index Files

```typescript
// Before: src/utils/index.ts
export { oldHelper } from './old-helper';  // ← Remove this
export { newHelper } from './new-helper';
export { anotherUtil } from './another-util';

// After
export { newHelper } from './new-helper';
export { anotherUtil } from './another-util';
```

### Pattern 3: Remove Re-exports

```typescript
// Before
export * from './old-module';  // ← Remove this
export * from './new-module';

// After
export * from './new-module';
```

### Pattern 4: Clean Up Usage

```typescript
// If file was used, need to:
// 1. Find replacement (from task spec)
// 2. Update all usages
// 3. Or remove feature if being deprecated

// Before
import { oldFormatter } from './old-formatter';

const display = oldFormatter(data);

// After (with replacement)
import { newFormatter } from './new-formatter';

const display = newFormatter(data);

// Or After (feature removed)
// Remove the entire usage if no replacement
```

## Step 4: Validate Changes

Before deleting file:

```bash
# Check no remaining references
grep_search "old-helper"
# Should return no results in source files

# Run syntax check on modified files
npx tsc --noEmit src/components/App.tsx src/utils/index.ts
```

## Step 5: Delete Target File

```bash
# Only after all references cleaned
rm src/utils/old-helper.ts
```

## Step 6: Verify Syntax

```bash
# Run full syntax check
npx tsc --noEmit

# Or check specific files that were modified
npx tsc --noEmit $(git diff --name-only | grep -E '\.(ts|tsx)$')
```

## Common Scenarios

### Scenario 1: Delete Unused Component

```typescript
Target: src/components/OldButton.tsx

1. Find usages:
   grep_search "import.*OldButton"
   grep_search "<OldButton"

2. If found usages:
   - Replace with new component
   - Or remove feature
   
3. Clean index.ts:
   // Before
   export { OldButton } from './OldButton';
   // After: Remove line

4. Delete file

5. Validate
```

### Scenario 2: Delete Utility with Dependencies

```typescript
Target: src/utils/string-helpers.ts

Issue: Other files import from it

Solution:
1. Check what's imported:
   grep_search "from.*string-helpers"
   
2. For each import:
   a. Find if there's a replacement
   b. Update import to new location
   c. Update function calls if API changed

3. Clean up:
   - Remove from utils/index.ts
   - Update any type references
   
4. Delete file
```

### Scenario 3: Delete with Breaking Changes

```typescript
Target: src/api/old-client.ts

Issue: No direct replacement, API changed

Solution:
1. Identify all consumers:
   grep_search "import.*old-client"

2. For each consumer:
   a. Understand what it's doing
   b. Rewrite using new API
   c. Update types
   d. Test logic still works

3. This might require CREATE/MODIFY tasks first

4. Only DELETE after all consumers updated
```

### Scenario 4: Delete Test File

```typescript
Target: src/components/Button.test.tsx

Check: Is component also being deleted?

If component deleted:
  - Safe to delete test
  
If component still exists:
  - Don't delete test
  - Or update test for new implementation
  
If asked to delete:
  1. Just delete (tests are rarely imported)
  2. Check test script still works
```

## Cleanup Checklist

For each DELETE operation:

### Pre-Delete
- [ ] Analyze all dependencies
- [ ] Create cleanup plan
- [ ] Identify replacement (if any)
- [ ] Check if config changes needed

### During Cleanup
- [ ] Remove all imports
- [ ] Remove from index files
- [ ] Remove type references
- [ ] Update usages or remove features
- [ ] Clean up comments/docs

### Post-Delete
- [ ] Delete target file
- [ ] Run syntax validation
- [ ] Check no broken imports
- [ ] Verify builds successfully

## Safe Deletion Patterns

### Pattern: Delete with Migration

```markdown
1. Create new replacement file (CREATE task)
2. Update all consumers to use new file (MODIFY tasks)
3. Verify all references updated (grep_search)
4. Delete old file (DELETE task)

This is multi-step and safest approach.
```

### Pattern: Direct Delete (Low Risk)

```markdown
Safe when:
- File has no imports (grep confirms)
- File is not exported anywhere
- File is isolated (test file, example, etc.)

Steps:
1. Quick reference check
2. Delete immediately
3. Syntax check
```

### Pattern: Delete with Deprecation

```markdown
1. Add deprecation notice to file
2. Update imports to show warning
3. Migrate consumers gradually
4. Delete after migration complete

For gradual removal over time.
```

## Error Recovery

If deletion breaks something:

```markdown
1. Identify the error
   - Missing import?
   - Broken type reference?
   - Lost functionality?

2. Options:
   a. Fix the error (update import path)
   b. Restore file temporarily
   c. Create replacement file

3. Document the issue

4. Retry deletion with better cleanup
```

## Special Cases

### Deleting Types

```typescript
// Type was: src/types/User.ts
export interface User {
  id: string;
  name: string;
}

// Consumers:
src/components/UserCard.tsx
src/api/users.ts
src/store/userSlice.ts

// Strategy:
1. Find replacement type or inline
2. Update all type references:
   import { User } from '../types/User';  // Old
   import { User } from '../types/Models'; // New
   
3. Or inline small types:
   interface User { id: string; name: string; }
   
4. Delete file
```

### Deleting Configs

```typescript
// Target: config/old-config.ts

// Check package.json, tsconfig.json, webpack.config.js, etc.
grep_search "old-config" "*.json" "*.config.*"

// Update all config references
// Delete file
```

### Deleting Assets

```typescript
// Target: public/images/old-logo.png

// Find references:
grep_search "old-logo"

// Check:
- HTML files
- CSS files
- React components
- README/docs

// Update all references
// Delete file
```

## Validation Commands

```bash
# TypeScript project
npx tsc --noEmit

# JavaScript project
node --check src/**/*.js

# Build check
npm run build

# Test check (if safe)
npm test

# Lint check
npm run lint
```

## Reporting Format

```markdown
## DELETION COMPLETE: [task-id]

### Deleted File
`src/utils/old-helper.ts`

### Dependencies Cleaned
1. `src/components/App.tsx`
   - Removed: `import { oldHelper } from '../utils/old-helper'`
   - Updated: Usage replaced with `newHelper`

2. `src/utils/index.ts`
   - Removed: `export { oldHelper } from './old-helper'`

3. `src/types/index.ts`
   - Removed: Type import for `OldHelperOptions`

### Syntax Validation
Command: `npx tsc --noEmit`
Result: ✅ PASS

No remaining references found (verified with grep_search)

### Status
🟢 DELETION SUCCESSFUL - All dependencies cleaned
```

## Red Flags - When NOT to Delete

🚩 **Stop if:**
- File has >10 dependencies (needs careful planning)
- No clear replacement identified
- Would break published API
- Affects multiple teams
- Required by external packages
- Part of build output

**Instead:** Report complexity and suggest multi-phase approach.

## Best Practices

1. **Always check dependencies first**
2. **Clean references before deleting**
3. **Validate after each change**
4. **Document what was cleaned**
5. **Test if possible**
6. **Commit changes atomically**

The key to safe deletion: **Clean first, delete last**.