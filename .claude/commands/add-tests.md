# /add-tests - Generate Tests for Existing Code

## Purpose

Automatically generate comprehensive tests for existing React components, hooks, or API routes using modern testing practices.

## Usage

```bash
/add-tests [file-path]
/add-tests src/components/Button.tsx
/add-tests src/hooks/useUser.ts
/add-tests app/api/users/route.ts
```

## Arguments

- `$ARGUMENTS`: Path to the file to generate tests for

---

## Workflow

### Step 1: Analyze File

Read and understand the code:
- Component props and state
- User interactions (clicks, inputs, etc.)
- Side effects (API calls, localStorage, etc.)
- Edge cases and error states

### Step 2: Generate Test File

Create a test file following naming conventions:
- `Component.tsx` → `Component.test.tsx`
- `useHook.ts` → `useHook.test.ts`
- `route.ts` → `route.test.ts`

### Step 3: Write Comprehensive Tests

Include:
- **Rendering tests**: Component displays correctly
- **Interaction tests**: User events work as expected
- **State tests**: State updates correctly
- **Edge cases**: Error states, empty data, loading, etc.
- **Accessibility**: ARIA attributes, keyboard navigation

---

## Output Format

For the file: **$ARGUMENTS**

```markdown
## 🧪 Generated Tests for: [FileName]

**File Type**: [Component/Hook/API Route]
**Testing Approach**: [React Testing Library/Vitest]

---

### Analysis Summary

**Identified Test Cases**:
1. Rendering with default props
2. User interactions (click, type, etc.)
3. State changes
4. API calls (if any)
5. Error handling
6. Edge cases

**Props/Parameters**:
- `prop1`: [type] - [description]
- `prop2`: [type] - [description]

**Interactions**:
- Click events
- Form submissions
- Keyboard events

---

### Generated Test File

**Create**: `[filepath].test.tsx`

```typescript
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, it, expect, vi } from 'vitest';
import { ComponentName } from './ComponentName';

describe('ComponentName', () => {
  // Test 1: Rendering
  it('should render with default props', () => {
    render(<ComponentName />);
    expect(screen.getByRole('[role]')).toBeInTheDocument();
  });

  // Test 2: Props
  it('should render with custom text', () => {
    render(<ComponentName text="Custom" />);
    expect(screen.getByText('Custom')).toBeInTheDocument();
  });

  // Test 3: User Interaction
  it('should call onClick when button is clicked', async () => {
    const handleClick = vi.fn();
    const user = userEvent.setup();
    
    render(<ComponentName onClick={handleClick} />);
    
    await user.click(screen.getByRole('button'));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  // Test 4: State Changes
  it('should toggle state when clicked', async () => {
    const user = userEvent.setup();
    render(<ComponentName />);
    
    const button = screen.getByRole('button');
    await user.click(button);
    
    expect(screen.getByText(/active/i)).toBeInTheDocument();
  });

  // Test 5: Error States
  it('should display error message on failure', () => {
    render(<ComponentName error="Something went wrong" />);
    expect(screen.getByRole('alert')).toHaveTextContent('Something went wrong');
  });

  // Test 6: Accessibility
  it('should be keyboard accessible', async () => {
    const user = userEvent.setup();
    render(<ComponentName />);
    
    const button = screen.getByRole('button');
    await user.tab();
    
    expect(button).toHaveFocus();
  });
});
```

---

### Coverage Report

**Expected Coverage**:
- Lines: 85%+
- Branches: 80%+
- Functions: 90%+
- Statements: 85%+

**Run tests**:
```bash
pnpm test ComponentName.test.tsx
pnpm test:coverage
```
```

---

## Examples

### Example 1: React Component

**Input**: `src/components/LoginForm.tsx`

```typescript
// LoginForm.tsx
interface LoginFormProps {
  onSubmit: (email: string, password: string) => void;
  isLoading?: boolean;
  error?: string;
}

export function LoginForm({ onSubmit, isLoading, error }: LoginFormProps) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit(email, password);
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        placeholder="Email"
        aria-label="Email"
      />
      <input
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        placeholder="Password"
        aria-label="Password"
      />
      <button type="submit" disabled={isLoading}>
        {isLoading ? 'Loading...' : 'Login'}
      </button>
      {error && <div role="alert">{error}</div>}
    </form>
  );
}
```

**Generated Tests**: `LoginForm.test.tsx`

```typescript
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, it, expect, vi } from 'vitest';
import { LoginForm } from './LoginForm';

describe('LoginForm', () => {
  const mockOnSubmit = vi.fn();

  // Reset mock before each test
  beforeEach(() => {
    mockOnSubmit.mockClear();
  });

  it('should render email and password inputs', () => {
    render(<LoginForm onSubmit={mockOnSubmit} />);
    
    expect(screen.getByLabelText(/email/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/password/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /login/i })).toBeInTheDocument();
  });

  it('should submit form with email and password', async () => {
    const user = userEvent.setup();
    render(<LoginForm onSubmit={mockOnSubmit} />);
    
    await user.type(screen.getByLabelText(/email/i), 'test@example.com');
    await user.type(screen.getByLabelText(/password/i), 'password123');
    await user.click(screen.getByRole('button', { name: /login/i }));
    
    expect(mockOnSubmit).toHaveBeenCalledWith('test@example.com', 'password123');
    expect(mockOnSubmit).toHaveBeenCalledTimes(1);
  });

  it('should disable submit button when loading', () => {
    render(<LoginForm onSubmit={mockOnSubmit} isLoading={true} />);
    
    expect(screen.getByRole('button')).toBeDisabled();
    expect(screen.getByText(/loading/i)).toBeInTheDocument();
  });

  it('should display error message when provided', () => {
    render(<LoginForm onSubmit={mockOnSubmit} error="Invalid credentials" />);
    
    expect(screen.getByRole('alert')).toHaveTextContent('Invalid credentials');
  });

  it('should not submit form when inputs are empty', async () => {
    const user = userEvent.setup();
    render(<LoginForm onSubmit={mockOnSubmit} />);
    
    await user.click(screen.getByRole('button', { name: /login/i }));
    
    expect(mockOnSubmit).toHaveBeenCalledWith('', '');
  });
});
```

---

### Example 2: Custom Hook

**Input**: `src/hooks/useCounter.ts`

```typescript
// useCounter.ts
export function useCounter(initialValue = 0) {
  const [count, setCount] = useState(initialValue);

  const increment = () => setCount((c) => c + 1);
  const decrement = () => setCount((c) => c - 1);
  const reset = () => setCount(initialValue);

  return { count, increment, decrement, reset };
}
```

**Generated Tests**: `useCounter.test.ts`

```typescript
import { renderHook, act } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import { useCounter } from './useCounter';

describe('useCounter', () => {
  it('should initialize with default value', () => {
    const { result } = renderHook(() => useCounter());
    expect(result.current.count).toBe(0);
  });

  it('should initialize with custom value', () => {
    const { result } = renderHook(() => useCounter(10));
    expect(result.current.count).toBe(10);
  });

  it('should increment count', () => {
    const { result } = renderHook(() => useCounter());
    
    act(() => {
      result.current.increment();
    });
    
    expect(result.current.count).toBe(1);
  });

  it('should decrement count', () => {
    const { result } = renderHook(() => useCounter(5));
    
    act(() => {
      result.current.decrement();
    });
    
    expect(result.current.count).toBe(4);
  });

  it('should reset to initial value', () => {
    const { result } = renderHook(() => useCounter(10));
    
    act(() => {
      result.current.increment();
      result.current.increment();
      result.current.reset();
    });
    
    expect(result.current.count).toBe(10);
  });

  it('should handle multiple increments', () => {
    const { result } = renderHook(() => useCounter());
    
    act(() => {
      result.current.increment();
      result.current.increment();
      result.current.increment();
    });
    
    expect(result.current.count).toBe(3);
  });
});
```

---

### Example 3: API Route (Next.js)

**Input**: `app/api/users/route.ts`

```typescript
// app/api/users/route.ts
import { NextRequest, NextResponse } from 'next/server';

export async function GET() {
  const users = await db.user.findMany();
  return NextResponse.json(users);
}

export async function POST(request: NextRequest) {
  const body = await request.json();
  
  if (!body.email) {
    return NextResponse.json(
      { error: 'Email is required' },
      { status: 400 }
    );
  }
  
  const user = await db.user.create({ data: body });
  return NextResponse.json(user, { status: 201 });
}
```

**Generated Tests**: `route.test.ts`

```typescript
import { describe, it, expect, vi } from 'vitest';
import { GET, POST } from './route';

// Mock database
vi.mock('@/lib/db', () => ({
  db: {
    user: {
      findMany: vi.fn(),
      create: vi.fn(),
    },
  },
}));

import { db } from '@/lib/db';

describe('/api/users', () => {
  describe('GET', () => {
    it('should return list of users', async () => {
      const mockUsers = [
        { id: '1', name: 'John', email: 'john@example.com' },
        { id: '2', name: 'Jane', email: 'jane@example.com' },
      ];
      
      vi.mocked(db.user.findMany).mockResolvedValue(mockUsers);
      
      const response = await GET();
      const data = await response.json();
      
      expect(response.status).toBe(200);
      expect(data).toEqual(mockUsers);
      expect(db.user.findMany).toHaveBeenCalledTimes(1);
    });
  });

  describe('POST', () => {
    it('should create a new user', async () => {
      const newUser = { name: 'New User', email: 'new@example.com' };
      const createdUser = { id: '3', ...newUser };
      
      vi.mocked(db.user.create).mockResolvedValue(createdUser);
      
      const request = new Request('http://localhost:3000/api/users', {
        method: 'POST',
        body: JSON.stringify(newUser),
      });
      
      const response = await POST(request as any);
      const data = await response.json();
      
      expect(response.status).toBe(201);
      expect(data).toEqual(createdUser);
      expect(db.user.create).toHaveBeenCalledWith({ data: newUser });
    });

    it('should return 400 if email is missing', async () => {
      const request = new Request('http://localhost:3000/api/users', {
        method: 'POST',
        body: JSON.stringify({ name: 'No Email' }),
      });
      
      const response = await POST(request as any);
      const data = await response.json();
      
      expect(response.status).toBe(400);
      expect(data.error).toBe('Email is required');
      expect(db.user.create).not.toHaveBeenCalled();
    });
  });
});
```

---

## Testing Patterns

### Pattern 1: Component with State

```typescript
it('should update state on user interaction', async () => {
  const user = userEvent.setup();
  render(<Component />);
  
  // Initial state
  expect(screen.getByText(/off/i)).toBeInTheDocument();
  
  // Interact
  await user.click(screen.getByRole('button'));
  
  // Updated state
  expect(screen.getByText(/on/i)).toBeInTheDocument();
});
```

### Pattern 2: Component with API Call

```typescript
it('should fetch and display data', async () => {
  // MSW will handle mocking
  render(<Component />);
  
  // Loading state
  expect(screen.getByText(/loading/i)).toBeInTheDocument();
  
  // Wait for data
  await waitFor(() => {
    expect(screen.getByText('Data loaded')).toBeInTheDocument();
  });
});
```

### Pattern 3: Form Validation

```typescript
it('should show validation error', async () => {
  const user = userEvent.setup();
  render(<Form />);
  
  // Submit without filling
  await user.click(screen.getByRole('button', { name: /submit/i }));
  
  // Error displayed
  expect(screen.getByText(/email is required/i)).toBeInTheDocument();
});
```

---

## Success Criteria

- [x] Test file created
- [x] All component behaviors tested
- [x] Edge cases covered
- [x] Tests pass
- [x] Coverage ≥ 80%

**Next steps**:
```bash
# Run the tests
pnpm test [filename].test.tsx

# Check coverage
pnpm test:coverage

# View in UI
pnpm test:ui
```
