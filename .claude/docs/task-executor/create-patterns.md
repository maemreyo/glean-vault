# CREATE Operation Patterns

Reference guide for creating new files with proper structure using MCP Filesystem tools.

## Tool Usage

**Primary tool**: `write_file`
- Creates new files or overwrites existing ones
- Syntax: `write_file(path, content)`
- Use for all CREATE operations

**Supporting tools**:
- `create_directory` - Make parent directories if needed
- `read_file` - Read similar files as templates
- `list_directory` - Check what files exist

## React Components

### Functional Component with TypeScript

```typescript
import React from 'react';

interface [ComponentName]Props {
  // Props from task specification
  id?: string;
  className?: string;
  children?: React.ReactNode;
}

/**
 * [Brief description from task]
 * 
 * @param props - Component properties
 */
export const [ComponentName]: React.FC<[ComponentName]Props> = ({
  id,
  className,
  children,
}) => {
  // Implementation logic
  
  return (
    <div id={id} className={className}>
      {children}
    </div>
  );
};

export default [ComponentName];
```

### Component with Hooks

```typescript
import React, { useState, useEffect } from 'react';

interface [ComponentName]Props {
  initialValue?: string;
  onChange?: (value: string) => void;
}

export const [ComponentName]: React.FC<[ComponentName]Props> = ({
  initialValue = '',
  onChange,
}) => {
  const [value, setValue] = useState(initialValue);
  
  useEffect(() => {
    // Side effects
  }, [value]);
  
  const handleChange = (newValue: string) => {
    setValue(newValue);
    onChange?.(newValue);
  };
  
  return (
    // JSX
  );
};
```

## Utility Functions

### Pure Function with JSDoc

```typescript
/**
 * [Function description from task]
 * 
 * @param input - Input parameter description
 * @returns Return value description
 * @throws {Error} When validation fails
 * 
 * @example
 * ```typescript
 * const result = utilityFunction('input');
 * ```
 */
export function utilityFunction(input: string): string {
  if (!input) {
    throw new Error('Input is required');
  }
  
  // Implementation
  return result;
}
```

### Async Function with Error Handling

```typescript
import { CustomError } from './types';

/**
 * [Async function description]
 * 
 * @param param - Parameter description
 * @returns Promise resolving to result
 */
export async function asyncFunction(param: string): Promise<Result> {
  try {
    // Async implementation
    const data = await fetchData(param);
    return processData(data);
  } catch (error) {
    throw new CustomError('Operation failed', { cause: error });
  }
}
```

## Type Definitions

### Interface

```typescript
/**
 * [Interface description from task]
 */
export interface [InterfaceName] {
  /** Field description */
  id: string;
  
  /** Field description */
  name: string;
  
  /** Optional field description */
  metadata?: Record<string, unknown>;
}
```

### Type Alias

```typescript
/**
 * [Type description]
 */
export type [TypeName] = {
  field1: string;
  field2: number;
} | null;
```

### Enum

```typescript
/**
 * [Enum description]
 */
export enum [EnumName] {
  /** Option 1 description */
  OPTION_1 = 'option_1',
  
  /** Option 2 description */
  OPTION_2 = 'option_2',
}
```

## Service/API Functions

### API Service

```typescript
import axios, { AxiosInstance } from 'axios';

interface [ServiceName]Config {
  baseURL: string;
  timeout?: number;
}

/**
 * [Service description from task]
 */
export class [ServiceName] {
  private client: AxiosInstance;
  
  constructor(config: [ServiceName]Config) {
    this.client = axios.create({
      baseURL: config.baseURL,
      timeout: config.timeout || 5000,
    });
  }
  
  /**
   * [Method description]
   */
  async fetchData(id: string): Promise<Data> {
    try {
      const response = await this.client.get(`/data/${id}`);
      return response.data;
    } catch (error) {
      throw new Error(`Failed to fetch data: ${error.message}`);
    }
  }
}
```

## Configuration Files

### JSON Config

```json
{
  "$schema": "https://example.com/schema.json",
  "version": "1.0.0",
  "settings": {
    "key": "value"
  }
}
```

### TypeScript Config

```typescript
import { ConfigType } from './types';

/**
 * [Config description]
 */
export const config: ConfigType = {
  environment: process.env.NODE_ENV || 'development',
  api: {
    baseURL: process.env.API_URL || 'http://localhost:3000',
    timeout: 5000,
  },
  features: {
    enableFeatureX: true,
    enableFeatureY: false,
  },
};

export default config;
```

## Index Files

### Re-export Pattern

```typescript
// Export all from module
export * from './module-a';
export * from './module-b';

// Export specific items
export { SpecificItem } from './module-c';

// Export with rename
export { OldName as NewName } from './module-d';

// Export default
export { default } from './main';
```

### Barrel Export with Types

```typescript
// Components
export { ComponentA } from './ComponentA';
export { ComponentB } from './ComponentB';
export type { ComponentAProps } from './ComponentA';
export type { ComponentBProps } from './ComponentB';

// Utils
export * from './utils';

// Types
export type * from './types';
```

## Test Files

### Unit Test Template

```typescript
import { describe, it, expect, beforeEach, afterEach } from 'vitest';
import { functionToTest } from './module';

describe('[FunctionName]', () => {
  beforeEach(() => {
    // Setup
  });
  
  afterEach(() => {
    // Cleanup
  });
  
  it('should [expected behavior]', () => {
    // Arrange
    const input = 'test';
    
    // Act
    const result = functionToTest(input);
    
    // Assert
    expect(result).toBe('expected');
  });
  
  it('should throw error when [condition]', () => {
    expect(() => functionToTest(null)).toThrow();
  });
});
```

## File Structure Guidelines

1. **Imports Order**:
   - External libraries (React, lodash, etc.)
   - Internal modules (relative imports)
   - Types and interfaces
   - Styles

2. **Content Order**:
   - Imports
   - Type definitions
   - Constants
   - Helper functions (private)
   - Main implementation
   - Exports

3. **Naming Conventions**:
   - Components: PascalCase (`ThemeProvider.tsx`)
   - Utilities: camelCase (`sanitize-theme.ts`)
   - Types: PascalCase (`Theme.types.ts`)
   - Constants: UPPER_SNAKE_CASE in code
   - Test files: `*.test.ts` or `*.spec.ts`

4. **Documentation**:
   - JSDoc for all public functions
   - Inline comments for complex logic
   - README.md for modules/packages

## Integration Points

When creating files, always consider:
- Where it's imported (check with `grep_search`)
- What it exports (needed by other files)
- Dependencies it requires (npm packages)
- Side effects (state, API calls, etc.)