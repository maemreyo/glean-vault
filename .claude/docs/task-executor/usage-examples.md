# Task Executor Usage Examples

Real-world examples demonstrating task execution workflows.

## Example 1: CREATE - New Utility Function

### Task Specification

```markdown
TASK: A.1 - Create CSS Sanitizer
- ID: A.1
- Description: Create theme sanitization utility using DOMPurify
- Files: src/lib/theme-sanitizer.ts
- Action: CREATE
- Expected: Function that sanitizes CSS strings safely

IMPLEMENTATION DETAILS:
- Use DOMPurify for sanitization
- Export sanitizeCSS function
- Add TypeScript types
- Handle edge cases (null, empty strings)
- Add JSDoc documentation
```

### Execution Steps

**1. Analyze Task**
```
Operation: CREATE
Target: src/lib/theme-sanitizer.ts
Requirements:
  - DOMPurify integration
  - sanitizeCSS function
  - TypeScript types
  - Error handling
```

**2. Check Project Patterns**
```bash
# See how project imports DOMPurify
grep_search "import.*dompurify"
# Found: import DOMPurify from 'dompurify'

# Check existing sanitizer patterns
view_file src/lib/html-sanitizer.ts
# Note: Uses try-catch and returns empty string on error
```

**3. Implement File**
```typescript
import DOMPurify from 'dompurify';

/**
 * Sanitizes CSS string to prevent XSS attacks
 * 
 * @param css - Raw CSS string to sanitize
 * @returns Sanitized CSS string safe for injection
 * 
 * @example
 * ```typescript
 * const safe = sanitizeCSS('color: red; background: blue;');
 * ```
 */
export function sanitizeCSS(css: string): string {
  if (!css || typeof css !== 'string') {
    return '';
  }

  try {
    // Configure DOMPurify for CSS
    const clean = DOMPurify.sanitize(css, {
      ALLOWED_TAGS: [],
      ALLOWED_ATTR: [],
    });
    
    return clean;
  } catch (error) {
    console.error('CSS sanitization failed:', error);
    return '';
  }
}

/**
 * Sanitizes theme configuration object
 */
export interface ThemeConfig {
  primaryColor?: string;
  backgroundColor?: string;
  customCSS?: string;
}

export function sanitizeThemeConfig(config: ThemeConfig): ThemeConfig {
  return {
    primaryColor: config.primaryColor ? sanitizeCSS(config.primaryColor) : undefined,
    backgroundColor: config.backgroundColor ? sanitizeCSS(config.backgroundColor) : undefined,
    customCSS: config.customCSS ? sanitizeCSS(config.customCSS) : undefined,
  };
}
```

**4. Validate Syntax**
```bash
npx tsc --noEmit src/lib/theme-sanitizer.ts
# Result: No errors found
```

**5. Report**
```markdown
## IMPLEMENTATION COMPLETE: A.1

### Files Changed
Created: `src/lib/theme-sanitizer.ts` (47 lines)
- Exports: sanitizeCSS, sanitizeThemeConfig, ThemeConfig
- Imports: dompurify
- Structure: Utility functions with TypeScript types

### Syntax Validation
Command: `npx tsc --noEmit src/lib/theme-sanitizer.ts`
Result: ✅ PASS

### Status
🟢 READY FOR VERIFICATION
```

---

## Example 2: MODIFY - Add Validation

### Task Specification

```markdown
TASK: B.2 - Add Input Validation
- ID: B.2
- Description: Add validation to theme provider before applying theme
- Files: src/components/ThemeProvider.tsx
- Action: MODIFY
- Expected: Validate theme config before applying, show error on invalid input

IMPLEMENTATION DETAILS:
- Import sanitizeThemeConfig from A.1
- Add validation before applyTheme
- Show error message if validation fails
- Don't break existing functionality
```

### Execution Steps

**1. Read Current File**
```bash
view_file src/components/ThemeProvider.tsx
```

Current content:
```typescript
import React from 'react';
import { applyTheme } from '../utils/theme-utils';

export function ThemeProvider({ config, children }) {
  const handleApply = () => {
    applyTheme(config);
  };

  return (
    <div>
      <button onClick={handleApply}>Apply Theme</button>
      {children}
    </div>
  );
}
```

**2. Plan Changes**
```markdown
Changes needed:
1. Add import for sanitizeThemeConfig
2. Add import for useState (error state)
3. Add validation logic in handleApply
4. Add error display in UI
5. Add TypeScript types
```

**3. Apply Modifications**

Using `multi_replace_file_content` for multiple changes:

```typescript
// Change 1: Add imports
import React, { useState } from 'react';
import { applyTheme } from '../utils/theme-utils';
import { sanitizeThemeConfig, ThemeConfig } from '../lib/theme-sanitizer';

// Change 2: Add types and state
interface ThemeProviderProps {
  config: ThemeConfig;
  children: React.ReactNode;
}

export function ThemeProvider({ config, children }: ThemeProviderProps) {
  const [error, setError] = useState<string | null>(null);

  // Change 3: Add validation
  const handleApply = () => {
    try {
      // Validate and sanitize config
      const sanitized = sanitizeThemeConfig(config);
      
      // Check if anything was sanitized
      if (JSON.stringify(sanitized) !== JSON.stringify(config)) {
        setError('Theme config contained unsafe values and was sanitized');
      }
      
      applyTheme(sanitized);
      setError(null);
    } catch (err) {
      setError('Failed to apply theme: ' + (err as Error).message);
    }
  };

  return (
    <div>
      {error && <div className="error">{error}</div>}
      <button onClick={handleApply}>Apply Theme</button>
      {children}
    </div>
  );
}
```

**4. Validate**
```bash
npx tsc --noEmit src/components/ThemeProvider.tsx
# Result: No errors
```

**5. Report**
```markdown
## IMPLEMENTATION COMPLETE: B.2

### Files Changed
Modified: `src/components/ThemeProvider.tsx`
- Added: 18 lines
- Modified: 5 lines
- Functions affected: ThemeProvider, handleApply

### Changes Detail
1. Added imports: useState, sanitizeThemeConfig, ThemeConfig
2. Added TypeScript interface: ThemeProviderProps
3. Added error state management
4. Added validation logic in handleApply
5. Added error display in UI

### Syntax Validation
Command: `npx tsc --noEmit src/components/ThemeProvider.tsx`
Result: ✅ PASS

### Status
🟢 READY FOR VERIFICATION
```

---

## Example 3: DELETE - Remove Deprecated Code

### Task Specification

```markdown
TASK: C.1 - Remove Old Theme Utility
- ID: C.1
- Description: Remove deprecated old-theme-utils.ts and clean up references
- Files: src/utils/old-theme-utils.ts
- Action: DELETE
- Expected: File deleted, all imports removed, no broken references

CONTEXT:
New theme-utils.ts has replaced all functionality.
All consumers should already be updated.
```

### Execution Steps

**1. Analyze Dependencies**
```bash
# Find all imports
grep_search "from.*old-theme-utils"
# Results:
# - src/components/LegacyTheme.tsx:3
# - src/utils/index.ts:5

# Find any usage
grep_search "old-theme-utils"
# Same results
```

**2. Check Each Dependency**

```bash
# Check LegacyTheme.tsx
view_file src/components/LegacyTheme.tsx
```

Found:
```typescript
import { oldApplyTheme } from '../utils/old-theme-utils';

export function LegacyTheme() {
  oldApplyTheme({ color: 'blue' });
  return <div>Legacy Theme</div>;
}
```

```bash
# Check index.ts
view_file src/utils/index.ts
```

Found:
```typescript
export { oldApplyTheme } from './old-theme-utils';
export { applyTheme } from './theme-utils';
```

**3. Clean Dependencies**

**File 1: LegacyTheme.tsx**
```typescript
// Before
import { oldApplyTheme } from '../utils/old-theme-utils';

export function LegacyTheme() {
  oldApplyTheme({ color: 'blue' });
  return <div>Legacy Theme</div>;
}

// After
import { applyTheme } from '../utils/theme-utils';

export function LegacyTheme() {
  applyTheme({ primaryColor: 'blue' }); // Updated to new API
  return <div>Legacy Theme</div>;
}
```

**File 2: index.ts**
```typescript
// Before
export { oldApplyTheme } from './old-theme-utils';
export { applyTheme } from './theme-utils';

// After
export { applyTheme } from './theme-utils';
```

**4. Validate Cleanup**
```bash
# Check no remaining references
grep_search "old-theme-utils"
# Result: No matches found

# Validate modified files
npx tsc --noEmit src/components/LegacyTheme.tsx src/utils/index.ts
# Result: No errors
```

**5. Delete File**
```bash
# Now safe to delete
rm src/utils/old-theme-utils.ts
```

**6. Final Validation**
```bash
npx tsc --noEmit
# Result: No errors
```

**7. Report**
```markdown
## DELETION COMPLETE: C.1

### Deleted File
`src/utils/old-theme-utils.ts`

### Dependencies Cleaned

1. **src/components/LegacyTheme.tsx**
   - Removed: `import { oldApplyTheme } from '../utils/old-theme-utils'`
   - Updated: Changed to use `applyTheme` from new utils
   - Updated call: `oldApplyTheme()` → `applyTheme()` with new API

2. **src/utils/index.ts**
   - Removed: `export { oldApplyTheme } from './old-theme-utils'`

### Syntax Validation
Command: `npx tsc --noEmit`
Result: ✅ PASS

Verified: No remaining references to old-theme-utils (grep_search confirmed)

### Status
🟢 DELETION SUCCESSFUL - All dependencies cleaned
```

---

## Example 4: Complex Task with Auto-Fix

### Task Specification

```markdown
TASK: D.1 - Refactor Data Processor
- ID: D.1  
- Description: Add TypeScript types to data-processor.js
- Files: src/processors/data-processor.js
- Action: MODIFY
- Expected: Convert to TypeScript, add proper types, maintain functionality
```

### Execution Steps

**1. Read Current File**
```javascript
// src/processors/data-processor.js
export function processData(data) {
  const filtered = data.filter(item => item.active);
  const mapped = filtered.map(item => ({
    id: item.id,
    name: item.name,
    value: item.count * 2
  }));
  return mapped;
}

export function aggregateData(items) {
  return items.reduce((acc, item) => acc + item.value, 0);
}
```

**2. Implement Changes**
```typescript
// Rename to .ts and add types
interface DataItem {
  id: string;
  name: string;
  active: boolean;
  count: number;
}

interface ProcessedItem {
  id: string;
  name: string;
  value: number;
}

export function processData(data: DataItem[]): ProcessedItem[] {
  const filtered = data.filter(item => item.active);
  const mapped = filtered.map(item => ({
    id: item.id,
    name: item.name,
    value: item.count * 2
  }));
  return mapped;
}

export function aggregateData(items: ProcessedItem[]): number {
  return items.reduce((acc, item) => acc + item.value, 0);
}
```

**3. First Validation**
```bash
npx tsc --noEmit src/processors/data-processor.ts
# Error: Cannot find module '../types/DataItem'
```

**4. Auto-Fix Applied**

Error diagnosis: Missing import for types that might exist elsewhere

```bash
# Search for DataItem definition
grep_search "interface DataItem"
# Found in: src/types/models.ts
```

Auto-fix: Add import
```typescript
import { DataItem } from '../types/models';

// Remove inline interface definition
// Keep ProcessedItem as it's local to this file

interface ProcessedItem {
  id: string;
  name: string;
  value: number;
}

export function processData(data: DataItem[]): ProcessedItem[] {
  // ... rest of code
}
```

**5. Second Validation**
```bash
npx tsc --noEmit src/processors/data-processor.ts
# Error: Property 'count' does not exist on type 'DataItem'
```

**6. Auto-Fix Attempt 2**

Diagnosis: DataItem in models.ts doesn't have 'count' property

```bash
view_file src/types/models.ts
```

Found:
```typescript
export interface DataItem {
  id: string;
  name: string;
  active: boolean;
  quantity: number; // Note: it's 'quantity', not 'count'
}
```

Auto-fix: Update property name
```typescript
export function processData(data: DataItem[]): ProcessedItem[] {
  const filtered = data.filter(item => item.active);
  const mapped = filtered.map(item => ({
    id: item.id,
    name: item.name,
    value: item.quantity * 2  // Changed count → quantity
  }));
  return mapped;
}
```

**7. Third Validation**
```bash
npx tsc --noEmit src/processors/data-processor.ts
# Result: No errors ✅
```

**8. Report**
```markdown
## IMPLEMENTATION COMPLETE: D.1

### Files Changed
Modified: `src/processors/data-processor.js` → `data-processor.ts`
- Added: 15 lines (type definitions)
- Modified: 8 lines (type annotations)
- Functions affected: processData, aggregateData

### Syntax Validation
Command: `npx tsc --noEmit src/processors/data-processor.ts`
Result: ✅ PASS (after auto-fixes)

### Auto-Fixes Applied

**Fix 1**: Added missing import
- Added: `import { DataItem } from '../types/models'`
- Removed: Inline DataItem interface (used existing type)

**Fix 2**: Corrected property name
- Changed: `item.count` → `item.quantity`
- Reason: DataItem interface uses 'quantity', not 'count'

**Validation Attempts**: 3
- Attempt 1: Missing import ❌
- Attempt 2: Wrong property name ❌  
- Attempt 3: All checks passed ✅

### Status
🟢 READY FOR VERIFICATION
```

---

## Tips from Examples

### DO:
✅ Read existing files to learn patterns  
✅ Use grep_search to find dependencies  
✅ Apply minimal necessary changes  
✅ Validate after each change  
✅ Report auto-fixes clearly  
✅ Follow project conventions

### DON'T:
❌ Make changes without reading context  
❌ Delete before cleaning references  
❌ Skip syntax validation  
❌ Break existing functionality  
❌ Ignore project patterns  
❌ Auto-fix without understanding

### Key Takeaways

1. **Context First**: Always understand before implementing
2. **Incremental Changes**: Small, validated steps
3. **Safety Checks**: Validate before and after
4. **Clear Communication**: Report what changed and why
5. **Learn & Adapt**: Follow project patterns