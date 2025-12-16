---
name: vitest
description: Modern JavaScript/TypeScript testing framework with Vite integration. Features hot module reloading, TypeScript support, mocking, coverage, and snapshot testing. Use when testing JavaScript/TypeScript projects, React/Vue/Svelte components, or modern web applications built with Vite.
---

# Vitest

Next-generation testing framework built for Vite with instant feedback loop and TypeScript-first design.

## Quick Start

```bash
# Install Vitest and related packages
npm install -D vitest @vitest/ui jsdom

# Add test script to package.json
{
  "scripts": {
    "test": "vitest",
    "test:ui": "vitest --ui",
    "test:coverage": "vitest --coverage"
  }
}

# Run tests
npm test                    # Watch mode by default
npm run test:ui           # Visual interface
npm run test:coverage      # With coverage report
```

## Test Structure

### Basic Test File
```typescript
// math.test.ts
import { describe, it, expect, beforeEach } from 'vitest';
import { add, subtract } from './math';

describe('Math operations', () => {
  beforeEach(() => {
    // Setup before each test
  });

  it('should add two numbers', () => {
    expect(add(2, 3)).toBe(5);
  });

  it('should subtract two numbers', () => {
    expect(subtract(10, 3)).toBe(7);
  });

  it('should handle decimal numbers', () => {
    expect(add(0.1, 0.2)).toBeCloseTo(0.3);
  });
});
```

### Test Organization
```typescript
// user.test.ts
import { describe, it, expect, test } from 'vitest';
import { User, UserService } from '../src/user';

describe('UserService', () => {
  const service = new UserService();

  describe('createUser', () => {
    it('creates user with valid data', () => {
      const userData = { name: 'John', email: 'john@example.com' };
      const user = service.createUser(userData);

      expect(user.name).toBe('John');
      expect(user.email).toBe('john@example.com');
      expect(user.id).toBeDefined();
    });

    test('throws error with invalid email', () => {
      const userData = { name: 'John', email: 'invalid' };

      expect(() => service.createUser(userData))
        .toThrow('Invalid email format');
    });
  });
});
```

## Mocking

### Module Mocking
```typescript
import { vi, describe, it, expect } from 'vitest';
import { fetchUserData } from './api';

// Mock entire module
vi.mock('./api', () => ({
  fetchUserData: vi.fn(),
}));

describe('API mocking', () => {
  it('mocks module import', async () => {
    const mockFetch = vi.mocked(fetchUserData);
    mockFetch.mockResolvedValue({ id: 1, name: 'Test' });

    const data = await fetchUserData(1);

    expect(data).toEqual({ id: 1, name: 'Test' });
    expect(mockFetch).toHaveBeenCalledWith(1);
  });
});
```

### Partial Mocking
```typescript
import { vi } from 'vitest';
import { externalApi } from './external';

vi.mock('./external', async () => {
  const actual = await vi.importActual('./external');
  return {
    ...actual,
    externalApi: {
      ...actual.externalApi,
      fetch: vi.fn(),
    },
  };
});

it('mocks only specific function', async () => {
  vi.mocked(externalApi).fetch.mockResolvedValue({ data: 'mocked' });

  const result = await externalApi.fetch();
  expect(result).toEqual({ data: 'mocked' });
});
```

### Mock Implementations
```typescript
vi.mock('./utils', () => ({
  formatDate: vi.fn((date) => `Formatted: ${date}`),
  calculateTotal: vi.fn((items) =>
    items.reduce((sum, item) => sum + item.price, 0)
  ),
}));

it('uses mock implementations', () => {
  const { formatDate, calculateTotal } = await import('./utils');

  expect(formatDate('2024-01-01')).toBe('Formatted: 2024-01-01');

  const items = [{ price: 10 }, { price: 20 }];
  expect(calculateTotal(items)).toBe(30);
});
```

### Time Mocking
```typescript
import { vi, beforeEach, afterEach } from 'vitest';

beforeEach(() => {
  vi.useFakeTimers();
});

afterEach(() => {
  vi.useRealTimers();
});

it('mocks time-based functions', () => {
  const timeoutCallback = vi.fn();

  setTimeout(timeoutCallback, 1000);

  // Fast-forward time
  vi.advanceTimersByTime(1000);

  expect(timeoutCallback).toHaveBeenCalledTimes(1);
});
```

## Async Testing

### Promise Testing
```typescript
import { describe, it, expect } from 'vitest';

describe('Async operations', () => {
  it('handles resolved promises', async () => {
    const result = await Promise.resolve('success');
    expect(result).toBe('success');
  });

  it('handles rejected promises', async () => {
    await expect(Promise.reject(new Error('failure')))
      .rejects.toThrow('failure');
  });

  it('handles multiple async operations', async () => {
    const results = await Promise.all([
      fetchUser(1),
      fetchUser(2),
      fetchUser(3),
    ]);

    expect(results).toHaveLength(3);
  });
});
```

### Async/Await with Cleanup
```typescript
import { beforeEach, afterEach, describe, it, expect } from 'vitest';

describe('Database operations', () => {
  let db: Database;

  beforeEach(async () => {
    db = new Database();
    await db.connect();
  });

  afterEach(async () => {
    await db.disconnect();
  });

  it('performs transaction', async () => {
    await db.transaction(async (trx) => {
      await trx.insert('users', { name: 'Test' });
      await trx.insert('posts', { title: 'Hello' });
    });

    const users = await db.select('users');
    const posts = await db.select('posts');

    expect(users).toHaveLength(1);
    expect(posts).toHaveLength(1);
  });
});
```

## React Testing

### Component Testing
```typescript
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import userEvent from '@testing-library/user-event';
import Counter from '../src/Counter';

describe('Counter component', () => {
  it('renders initial state', () => {
    render(<Counter initial={0} />);

    expect(screen.getByText('Count: 0')).toBeInTheDocument();
  });

  it('increments count', async () => {
    const user = userEvent.setup();
    render(<Counter initial={0} />);

    await user.click(screen.getByRole('button', { name: /increment/i }));

    expect(screen.getByText('Count: 1')).toBeInTheDocument();
  });

  it('handles async operations', async () => {
    render(<Counter initial={0} />);

    // Trigger async operation
    fireEvent.click(screen.getByRole('button', { name: /load data/i }));

    // Wait for async completion
    await waitFor(() => {
      expect(screen.getByText('Data loaded')).toBeInTheDocument();
    });
  });
});
```

### Custom Hooks Testing
```typescript
import { renderHook, act, waitFor } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import useApi from '../src/useApi';

describe('useApi hook', () => {
  it('fetches data on mount', async () => {
    const { result } = renderHook(() => useApi('/api/users'));

    expect(result.current.loading).toBe(true);

    await waitFor(() => {
      expect(result.current.data).toEqual([{ id: 1, name: 'Test' }]);
    });
    expect(result.current.loading).toBe(false);
  });
});
```

## Snapshots

### Inline Snapshots
```typescript
import { test, expect } from 'vitest';
import { generateReport } from './report';

test('generates correct report', () => {
  const report = generateReport({ title: 'Test Report' });

  expect(report).toMatchInlineSnapshot(`
    {
      "title": "Test Report",
      "generatedAt": Date<some date string>,
      "content": [
        "Section 1",
        "Section 2"
      ]
    }
  `);
});
```

### File Snapshots
```typescript
import { test, expect } from 'vitest';
import { Component } from './Component';

test('component renders correctly', () => {
  const { container } = render(<Component />);

  expect(container.firstChild).toMatchSnapshot();
});
```

## Test Environments

### DOM Testing
```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config';

export default defineConfig({
  testEnvironment: 'jsdom',
  setupFiles: ['./test/setup.ts'],
});

// test/setup.ts
import { beforeEach } from 'vitest';
import { configure } from '@testing-library/dom';

beforeEach(() => {
  configure({ testIdAttribute: 'data-test-id' });
});

// component.test.tsx
test('finds element by test id', () => {
  render(<Component />);

  expect(screen.getByTestId('submit-button')).toBeInTheDocument();
});
```

### Node.js Environment
```typescript
// vitest.config.ts
export default defineConfig({
  testEnvironment: 'node',
  globals: {
    __TEST__: true,
  },
});

// server.test.ts
import { test, expect } from 'vitest';

test('server functionality', () => {
  expect(typeof __TEST__).toBe('boolean');
  expect(process.env.NODE_ENV).toBeDefined();
});
```

## Configuration

### vitest.config.ts
```typescript
import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig({
  plugins: [react()],
  testEnvironment: 'jsdom',
  include: ['src/**/*.{test,spec}.{js,mjs,cjs,ts,jsx,tsx}'],
  exclude: ['node_modules'],
  globals: {
    // Global variables available in tests
    __DEV__: true,
  },
  setupFiles: ['./test/setup.ts'],
  coverage: {
    reporter: ['text', 'html'],
    exclude: [
      'node_modules/',
      'test/',
    ],
  },
  testTimeout: 10000, // 10 seconds
});
```

### Type Checking
```typescript
// test/types.ts
import { expect, describe } from 'vitest';
import type { User, Product } from '../src/types';

describe('Type definitions', () => {
  test('User type is properly defined', () => {
    const user: User = {
      id: 1,
      name: 'Test',
      email: 'test@example.com',
    };

    expectTypeOf(user.id).toBe('number');
    expectTypeOf(user.name).toBe('string');
  });
});

// Helper to check types at runtime
function expectTypeOf<T>(value: T): 'string' | 'number' | 'boolean' | 'object' | 'undefined' {
  return typeof value;
}
```

## Performance Testing

### Timer Simulation
```typescript
import { vi, describe, it, expect, beforeEach } from 'vitest';

describe('Performance', () => {
  beforeEach(() => {
    vi.useFakeTimers();
  });

  it('measures execution time', () => {
    const startTime = Date.now();

    // Run performance-intensive code
    heavyComputation();

    vi.advanceTimersByTime(0);
    const endTime = Date.now();

    expect(endTime - startTime).toBeLessThan(100);
  });
});
```

## Advanced Patterns

### Custom Matchers
```typescript
import { expect } from 'vitest';

// Custom matcher
expect.extend({
  toBeWithinRange(received: number, floor: number, ceiling: number) {
    const pass = received >= floor && received <= ceiling;

    if (pass) {
      return {
        message: () =>
          `expected ${received} to be within range ${floor} - ${ceiling}`,
        pass: true,
      };
    } else {
      return {
        message: () =>
          `expected ${received} to be within range ${floor} - ${ceiling}`,
        pass: false,
      };
    }
  },
});

test('custom matcher usage', () => {
  expect(25).toBeWithinRange(20, 30);
  expect(15).not.toBeWithinRange(20, 30);
});
```

### Test Utilities
```typescript
// test/utils.ts
import { vi } from 'vitest';

export function createMockUser(overrides = {}) {
  return {
    id: 1,
    name: 'Test User',
    email: 'test@example.com',
    createdAt: new Date(),
    ...overrides,
  };
}

export function mockApiResponse<T>(data: T) {
  return vi.fn().mockResolvedValue({
    data,
    status: 200,
    headers: { 'content-type': 'application/json' },
  });
}

// test/user.test.ts
import { describe, it, expect } from 'vitest';
import { createMockUser, mockApiResponse } from './utils';

describe('User utilities', () => {
  it('creates mock user', () => {
    const user = createMockUser({ name: 'Custom' });
    expect(user.name).toBe('Custom');
  });

  it('mocks API response', async () => {
    const mockFetch = mockApiResponse({ id: 1 });
    const response = await mockFetch();
    expect(response.data).toEqual({ id: 1 });
  });
});
```

## Best Practices

### 1. Test Isolation
```typescript
// Good: Each test is independent
describe('Feature', () => {
  it('works in isolation', () => {
    const result = process(true);
    expect(result).toBe(true);
  });

  it('also works independently', () => {
    const result = process(false);
    expect(result).toBe(false);
  });
});

// Bad: Tests share state
let sharedState: any;

describe('Feature with shared state', () => {
  beforeEach(() => {
    sharedState = new State();
  });

  it('modifies shared state', () => {
    sharedState.value = 1;
  });

  it('depends on previous test', () => {
    expect(sharedState.value).toBe(1); // Fragile!
  });
});
```

### 2. Mock at Boundaries
```typescript
// Good: Mock at module boundary
vi.mock('../src/api', () => ({
  fetchData: vi.fn(),
}));

// Bad: Mock implementation details
vi.mock('../src/utils', () => ({
  // Don't mock internal implementation!
  deepComplexLogic: vi.fn(),
}));
```

### 3. Use Arrange-Act-Assert Pattern
```typescript
it('follows AAA pattern', () => {
  // Arrange
  const input = { value: 42 };
  const expected = { value: 84 };

  // Act
  const result = doubleValue(input);

  // Assert
  expect(result).toEqual(expected);
});
```

## Running Tests

### Command Line Options
```bash
# Basic commands
vitest                          # Watch mode
vitest run                     # Single run
vitest --ui                   # Visual interface
vitest --reporter=verbose       # Detailed output

# Filtering
vitest user                   # Run files matching pattern
vitest -t "integration"        // Run tests with specific text
vitest -g "should.*succeed"     // Run tests matching regex

# Coverage
vitest --coverage              # Generate coverage
vitest --coverage.reporter=html # HTML report

# Parallel execution
vitest --run                   # Run tests in parallel files
```

### CI Integration
```bash
# CI script
npm run test:run              # Single run for CI
npm run test:coverage          # Coverage for CI
npm run test:ui                # Visual testing locally
```

## Resources

- [Vitest Documentation](https://vitest.dev/)
- [Vitest UI](https://vitest.dev/guide/ui)
- [Vitest Configuration](https://vitest.dev/config/)
- [Testing Library Docs](https://testing-library.com/)
