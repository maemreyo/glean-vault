# MODIFY Operation Strategies

Strategies for targeted code changes while preserving existing functionality using MCP Filesystem tools.

## Tool Usage

**Primary tool**: `edit_file`
- Makes selective modifications to existing files
- Preserves unchanged content
- Use for all MODIFY operations

**Supporting tools**:
- `read_file` - Read current file state first
- `grep_search` - Find dependent files
- `list_directory` - Check file structure

## Core Principles

1. **Read First**: Always use `read_file` to understand current state
2. **Minimal Changes**: Only modify what's necessary
3. **Preserve Context**: Keep existing code structure and formatting
4. **Verify Impact**: Use `grep_search` to check dependent files

## Strategy Selection

### Use `edit_file` for all modifications

The MCP `edit_file` tool handles both:
- Single targeted changes
- Multiple changes in same file

```typescript
// Old code
export function calculate(a, b) {
  return a + b;
}

// New code (add type annotations using edit_file)
export function calculate(a: number, b: number): number {
  return a + b;
}
```

## Common Modification Patterns

### 1. Adding Imports

**Strategy**: Insert at top of import section

```typescript
// Existing imports
import React from 'react';
import { useState } from 'react';

// Add new import (maintain grouping)
import { useEffect } from 'react';  // ← Add here (same library)
import axios from 'axios';          // ← Add here (different library)
```

**Groups order**:
1. React/framework imports
2. External libraries
3. Internal modules (absolute imports)
4. Relative imports
5. Type imports
6. CSS/style imports

### 2. Adding Function Parameters

**Strategy**: Extend parameter list, add defaults for optional params

```typescript
// Before
function createUser(name: string) {
  return { name, role: 'user' };
}

// After (preserve backward compatibility)
function createUser(
  name: string,
  role: string = 'user',  // ← Add with default
  metadata?: Record<string, unknown>  // ← Optional
) {
  return { name, role, metadata };
}
```

### 3. Adding Properties to Objects/Interfaces

**Strategy**: Append to existing definition

```typescript
// Before
interface Config {
  apiUrl: string;
  timeout: number;
}

// After
interface Config {
  apiUrl: string;
  timeout: number;
  retries?: number;      // ← Add optional first
  headers: Record<string, string>;  // ← Required after optional
}
```

### 4. Wrapping Existing Logic

**Strategy**: Preserve original logic, add wrapper behavior

```typescript
// Before
export function saveData(data: Data) {
  return database.save(data);
}

// After (add validation)
export function saveData(data: Data) {
  // Add validation wrapper
  if (!isValid(data)) {
    throw new Error('Invalid data');
  }
  
  // Original logic preserved
  return database.save(data);
}
```

### 5. Adding Middleware/Interceptors

**Strategy**: Insert before or after existing logic

```typescript
// Before
app.get('/api/data', handler);

// After (add middleware)
app.get('/api/data', 
  authMiddleware,      // ← Add before
  validateMiddleware,  // ← Add before
  handler,
  logMiddleware        // ← Add after
);
```

### 6. Extending Classes

**Strategy**: Add methods without changing existing ones

```typescript
// Before
class DataService {
  fetch() { }
  save() { }
}

// After
class DataService {
  fetch() { }  // Unchanged
  save() { }   // Unchanged
  
  // New methods
  fetchById(id: string) {
    return this.fetch().find(item => item.id === id);
  }
  
  saveMany(items: Data[]) {
    return Promise.all(items.map(item => this.save(item)));
  }
}
```

### 7. Adding Error Handling

**Strategy**: Wrap existing code in try-catch

```typescript
// Before
export async function fetchUser(id: string) {
  const response = await api.get(`/users/${id}`);
  return response.data;
}

// After
export async function fetchUser(id: string) {
  try {
    const response = await api.get(`/users/${id}`);
    return response.data;
  } catch (error) {
    console.error(`Failed to fetch user ${id}:`, error);
    throw new Error(`User fetch failed: ${error.message}`);
  }
}
```

### 8. Adding Conditional Logic

**Strategy**: Early returns for new conditions

```typescript
// Before
export function process(data: Data) {
  const result = transform(data);
  return result;
}

// After (add validation)
export function process(data: Data) {
  // Early return for new condition
  if (!data || !data.id) {
    throw new Error('Invalid data');
  }
  
  // Early return for edge case
  if (data.type === 'skip') {
    return null;
  }
  
  // Original logic preserved
  const result = transform(data);
  return result;
}
```

## Preservation Techniques

### Maintain Formatting

```typescript
// ❌ Bad: Changed indentation
export function calculate(a,b) {
return a+b;
}

// ✅ Good: Preserved formatting
export function calculate(a: number, b: number): number {
  return a + b;
}
```

### Preserve Comments

```typescript
// Before
export function calculate(a, b) {
  // This handles edge cases
  if (a === 0) return b;
  return a + b;
}

// After
export function calculate(a: number, b: number): number {
  // This handles edge cases  ← KEEP THIS
  if (a === 0) return b;
  return a + b;
}
```

### Keep Variable Names

```typescript
// ❌ Bad: Renamed unnecessarily
const result = data.map(item => processItem(item));

// ✅ Good: Kept original name
const processedData = data.map(item => processItem(item));
```

## Change Impact Analysis

Before modifying, check impact:

```bash
# Find where function is used
grep_search "calculateTotal"

# Find where type is imported
grep_search "import.*UserConfig"

# Find test files
grep_search "describe.*calculateTotal"
```

## Safe Modification Checklist

Before applying changes:
- [ ] Read entire file to understand context
- [ ] Identify exact insertion/modification points
- [ ] Check if change affects function signature
- [ ] Verify no duplicate imports added
- [ ] Ensure proper spacing/formatting
- [ ] Keep existing error handling patterns
- [ ] Preserve all comments and documentation

After applying changes:
- [ ] Run syntax validation
- [ ] Check dependent files (grep_search)
- [ ] Verify exports remain correct
- [ ] Ensure backward compatibility

## Rollback Strategy

If modification causes issues:
1. Note the exact error message
2. Revert the specific change (not entire file)
3. Try alternative approach
4. Document why original approach failed

## Examples by Complexity

### Simple: Add Single Import

```typescript
// Find import section
import React from 'react';

// Add after similar imports
import { useState } from 'react';
```

### Medium: Add Function to Existing Module

```typescript
// Existing code stays
export function existingFunction() { }

// Add new function at end
export function newFunction(param: string): string {
  return param.toUpperCase();
}
```

### Complex: Refactor with Backward Compatibility

```typescript
// Before
export function fetchData(url) {
  return axios.get(url);
}

// After (add options, keep old signature working)
export function fetchData(
  url: string,
  options?: RequestOptions
): Promise<Response> {
  // New implementation with options
  const config = options ? buildConfig(options) : {};
  return axios.get(url, config);
}
```

## Anti-Patterns to Avoid

❌ **Don't**: Rewrite entire functions when adding one line  
✅ **Do**: Insert the line exactly where needed

❌ **Don't**: Change indentation/style of untouched code  
✅ **Do**: Match existing file style exactly

❌ **Don't**: Assume dependencies exist  
✅ **Do**: Check imports before using libraries

❌ **Don't**: Remove "unused" code without checking  
✅ **Do**: Use grep_search to verify code isn't used

❌ **Don't**: Make assumptions about types  
✅ **Do**: Read type definitions from source