# /setup-testing - Modern Next.js Testing Stack Setup

## Purpose

Automatically set up a complete, modern testing environment for Next.js projects (both Frontend-only and Fullstack with API routes).

## Usage

```bash
/setup-testing                      # Auto-detect and setup (recommended)
/setup-testing --vitest            # Use Vitest (faster, recommended)
/setup-testing --jest              # Use Jest (if you prefer)
/setup-testing --playwright        # Use Playwright for E2E (recommended)
/setup-testing --cypress           # Use Cypress for E2E
/setup-testing --minimal           # Unit tests only, skip E2E
/setup-testing --with-storybook    # Include Storybook integration
/setup-testing --no-e2e            # Skip E2E setup entirely
/setup-testing --clean             # Remove old configs before setup
```

---

## Modern Next.js Testing Stack (2024)

Based on industry research and best practices, the recommended stack is:

### 📦 **Recommended Stack**

| Layer | Tool | Purpose | Why? |
|-------|------|---------|------|
| **Unit/Component** | Vitest + RTL | Component & hook testing | ⚡ Faster than Jest, better DX |
| **API Mocking** | MSW (Mock Service Worker) | Mock API responses | Works with SSR, reliable |
| **E2E Testing** | Playwright | Full user flows | Fast, reliable, cross-browser |
| **Utilities** | React Testing Library | User-centric testing | Industry standard |

### 🆚 **Alternative: Classic Stack**

| Layer | Tool | Purpose |
|-------|------|---------|
| **Unit/Component** | Jest + RTL | Component testing |
| **API Mocking** | MSW | Mock APIs |
| **E2E Testing** | Cypress | E2E flows |

---

## Workflow

### Phase 0: Pre-flight Checks ✈️

Before starting, verify:

```markdown
## 🔍 Pre-flight Checklist

**Environment Checks**:
- [ ] Node.js version ≥ 18.0.0
- [ ] Package manager installed (npm/pnpm/yarn)
- [ ] No conflicting test runners (check package.json)

**Project Analysis**:
- [ ] Detect Next.js version
- [ ] Check for existing test configs
- [ ] Detect internationalization (next-intl, i18next)
- [ ] Check for Storybook installation
- [ ] Identify API routes presence

**Compatibility Checks**:
- [ ] Check for playwright-bdd vs standard Playwright
- [ ] Verify no duplicate msw.workerDirectory in package.json
- [ ] Check for Rosetta 2 (M1/M2 Mac if applicable)

✅ All checks passed → Proceed
⚠️ Issues found → Show resolution steps
```

---

### Phase 1: Detect Existing Setup 🔎

**Smart Detection**:

```typescript
interface ProjectAnalysis {
  // Package Manager
  packageManager: 'npm' | 'pnpm' | 'yarn';
  
  // Next.js
  nextjsVersion: string;
  hasAppRouter: boolean;
  hasPagesRouter: boolean;
  hasApiRoutes: boolean;
  
  // Testing
  existingConfigs: {
    vitest?: string;      // Path to existing config
    jest?: string;
    playwright?: string;
    cypress?: string;
  };
  
  // Integrations
  hasStorybook: boolean;
  storybookVersion?: string;
  hasPlaywrightBDD: boolean;
  
  // i18n
  i18nLibrary?: 'next-intl' | 'i18next' | 'none';
  
  // TypeScript
  isTypeScript: boolean;
}
```

**Conflict Resolution**:

```markdown
If existing configs found:

1. **vitest.config.ts exists**:
   - Prompt: "Found existing Vitest config. Merge or replace?"
   - Option A: Merge (preserve custom settings)
   - Option B: Backup and replace
   - Option C: Skip Vitest setup

2. **playwright.config.ts exists**:
   - Check if playwright-bdd is installed
   - If BDD: Keep existing config, add test examples only
   - If standard: Offer to merge configurations

3. **Storybook detected**:
   - Check for @storybook/test-runner
   - Offer to integrate with Vitest addon
   - Create shared test utilities
```

---

### Phase 2: Install Dependencies 📦

**Smart Installation**:

```bash
# Analyze what's needed based on detection
if (no_vitest_config && !user_selected_jest):
  install_vitest_stack()

if (has_storybook && user_wants_integration):
  install_storybook_test_integration()

if (has_next_intl):
  install_i18n_test_helpers()

if (user_wants_e2e && !has_playwright):
  install_playwright()
```

**Handle Conflicts**:

```bash
# Remove duplicate dependencies
check_duplicate_msw_worker_directory()
clean_duplicate_package_json_entries()

# Version compatibility
ensure_compatible_versions({
  'msw': '^2.0.0',
  'vitest': '^1.0.0',
  '@playwright/test': '^1.40.0'
})
```

---

### Phase 3: Configuration Files ⚙️

**Create with Auto-fixes**:

1. **vitest.config.ts** (with common fixes):

```typescript
// AUTO-GENERATED with common fixes
import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';
import tsconfigPaths from 'vite-tsconfig-paths';

export default defineConfig({
  plugins: [react(), tsconfigPaths()],
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: './vitest.setup.ts',
    
    // ✅ Auto-exclude problematic directories
    exclude: [
      'node_modules',
      '.next',
      'dist',
      'build',
      'coverage',
      '.storybook',
      'storybook-static',
      '**/*.config.*',
      '**/playwright/**',     // Exclude E2E tests
      '**/e2e/**',
    ],
    
    css: true,
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
      exclude: [
        'node_modules/',
        '.next/',
        '**/*.d.ts',
        '**/*.config.*',
        '**/mockData/*',
        '**/*.stories.*',      // Exclude Storybook stories
      ],
    },
  },
});
```

2. **vitest.setup.ts** (with ALL common mocks):

```typescript
import '@testing-library/jest-dom';
import { cleanup } from '@testing-library/react';
import { afterEach, vi } from 'vitest';

// Cleanup after each test
afterEach(() => {
  cleanup();
});

// ✅ FIX: ResizeObserver mock (common issue)
global.ResizeObserver = vi.fn().mockImplementation(() => ({
  observe: vi.fn(),
  unobserve: vi.fn(),
  disconnect: vi.fn(),
}));

// ✅ FIX: scrollIntoView mock (common issue)
Element.prototype.scrollIntoView = vi.fn();

// ✅ FIX: IntersectionObserver mock
global.IntersectionObserver = vi.fn().mockImplementation(() => ({
  observe: vi.fn(),
  unobserve: vi.fn(),
  disconnect: vi.fn(),
}));

// Mock Next.js router
vi.mock('next/navigation', () => ({
  useRouter() {
    return {
      push: vi.fn(),
      replace: vi.fn(),
      prefetch: vi.fn(),
      back: vi.fn(),
      forward: vi.fn(),
      refresh: vi.fn(),
      pathname: '/',
    };
  },
  usePathname() {
    return '/';
  },
  useSearchParams() {
    return new URLSearchParams();
  },
  useParams() {
    return {};
  },
}));

// Mock Next.js Image component
vi.mock('next/image', () => ({
  default: (props: any) => {
    // eslint-disable-next-line jsx-a11y/alt-text
    return <img {...props} />;
  },
}));

// ✅ AUTO-ADDED: next-intl mock (if detected)
{{ if has_next_intl }}
vi.mock('next-intl', () => ({
  useTranslations: () => (key: string) => key,
  useLocale: () => 'en',
}));
{{ endif }}
```

3. **MSW Setup** (with auto-fix):

```typescript
// mocks/handlers.ts - Auto-generated based on API routes detected

{{ if has_api_routes }}
import { http, HttpResponse } from 'msw';

export const handlers = [
  // Auto-generated from detected API routes
  {{ for each api_route }}
  http.{{ method }}('{{ route_path }}', () => {
    return HttpResponse.json({{ example_response }});
  }),
  {{ endfor }}
];
{{ endif }}
```

---

### Phase 4: Smart Test Generation 🧪

**Instead of generic tests, scan actual components**:

```typescript
// Scan src/ for components
const components = scanDirectory('src/components');

for (const component of components) {
  const analysis = analyzeComponent(component);
  
  // Generate test based on actual props and usage
  generateTestFile({
    componentPath: component.path,
    props: analysis.props,
    hooks: analysis.hooks,
    apiCalls: analysis.apiCalls,
    hasTranslations: analysis.usesI18n,
  });
}
```

**Example Generated Test** (based on real component):

```typescript
// Auto-generated for src/components/Button.tsx
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, it, expect, vi } from 'vitest';
import { Button } from './Button';

// Props detected: variant, size, onClick, disabled, children
describe('Button', () => {
  it('should render with children', () => {
    render(<Button>Click me</Button>);
    expect(screen.getByRole('button', { name: /click me/i })).toBeInTheDocument();
  });
  
  // Test all detected variants
  it.each(['primary', 'secondary', 'outline'])(
    'should render %s variant',
    (variant) => {
      render(<Button variant={variant}>Test</Button>);
      expect(screen.getByRole('button')).toHaveClass(variant);
    }
  );
  
  // onClick detected in props
  it('should call onClick when clicked', async () => {
    const handleClick = vi.fn();
    const user = userEvent.setup();
    
    render(<Button onClick={handleClick}>Click me</Button>);
    await user.click(screen.getByRole('button'));
    
    expect(handleClick).toHaveBeenCalledTimes(1);
  });
});
```

---

### Phase 5: Project-Specific Customizations 🎨

**Next.js with next-intl**:

```typescript
// Create test utilities for translations
// src/test/utils/intl.tsx

import { NextIntlClientProvider } from 'next-intl';
import { ReactElement } from 'react';
import { render, RenderOptions } from '@testing-library/react';

const messages = {
  // Auto-load from your messages files
};

export function renderWithIntl(
  ui: ReactElement,
  options?: RenderOptions
) {
  return render(
    <NextIntlClientProvider locale="en" messages={messages}>
      {ui}
    </NextIntlClientProvider>,
    options
  );
}
```

**Storybook Integration**:

```typescript
// .storybook/test-runner.ts
import type { TestRunnerConfig } from '@storybook/test-runner';

const config: TestRunnerConfig = {
  async postRender(page, context) {
    // Add accessibility tests
    await require('@storybook/test-runner').checkA11y(page, context);
  },
};

export default config;
```

---

### Phase 6: Package.json Updates 📝

**Smart merge (no duplicates)**:

```typescript
// Check for duplicate keys
const existingScripts = packageJson.scripts || {};

// Remove duplicates
if (existingScripts.test && existingScripts.test.includes('vitest')) {
  // Already has test script, don't override
  console.log('✓ Test script already exists');
} else {
  // Add new scripts
  packageJson.scripts = {
    ...existingScripts,
    "test": "vitest",
    "test:ui": "vitest --ui",
    "test:coverage": "vitest --coverage",
    "test:e2e": "playwright test",
    "test:e2e:ui": "playwright test --ui",
  };
}

// ✅ FIX: Remove duplicate msw.workerDirectory if exists
if (packageJson.msw?.workerDirectory) {
  delete packageJson.msw.workerDirectory; // Will be in public/
}
```

---

### Phase 7: Post-Setup Verification ✅

**Automatic Verification**:

```bash
## 🧪 Running Verification Tests

1. Testing Vitest setup...
   ✓ Vitest config valid
   ✓ Can import testing utilities
   ✓ ResizeObserver mock works
   
2. Running sample test...
   ✓ Sample component test passes
   
3. Testing MSW setup...
   ✓ MSW handlers load correctly
   ✓ API mocking works
   
4. Checking E2E setup...
   ✓ Playwright installed
   ⚠ Browsers not installed (run: npx playwright install)
   
5. Checking for common issues...
   ✓ No duplicate package.json keys
   ✓ No config conflicts
   ✓ All mocks properly configured
```

**If Issues Found**:

```markdown
⚠️ Issues Detected:

1. **Playwright browsers not installed**
   Fix: npx playwright install
   
2. **Translation files found but no mock**
   Fix: Added next-intl mock to vitest.setup.ts
   
3. **Storybook detected but not integrated**
   Suggestion: Run /setup-testing --with-storybook
```

---

### Phase 8: Cleanup (Optional) 🧹

**If `--clean` flag used**:

```bash
## 🧹 Cleaning Old Configurations

Found old configs:
- jest.config.js (from previous setup)
- .babelrc (not needed with Vitest)
- __tests__/setup.js (old Jest setup)

Actions:
✓ Backed up to .backup/
✓ Removed old configs
✓ Updated .gitignore
```

---

## Output: Setup Plan

```markdown
## 🧪 Testing Setup Plan for Next.js

**Detected**:
- Next.js: 15.0.0
- TypeScript: ✅
- App Router: ✅
- API Routes: ✅
- Package Manager: pnpm

**Selected Stack**:
- ✅ Vitest (unit/component tests)
- ✅ React Testing Library
- ✅ MSW (API mocking)
- ✅ Playwright (E2E tests)

---

### Tasks

#### Phase 1: Install Dependencies [5 min] 📦

**Unit Testing (Vitest)**:
```bash
pnpm add -D vitest @vitejs/plugin-react jsdom
pnpm add -D @testing-library/react @testing-library/jest-dom
pnpm add -D @testing-library/user-event @testing-library/dom
pnpm add -D vite-tsconfig-paths  # For TypeScript path aliases
```

**API Mocking (MSW)**:
```bash
pnpm add -D msw
```

**E2E Testing (Playwright)**:
```bash
pnpm add -D @playwright/test
npx playwright install
```

---

#### Phase 2: Configuration Files [10 min] ⚙️

**Task 1: Create `vitest.config.ts`**

```typescript
import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';
import tsconfigPaths from 'vite-tsconfig-paths';

export default defineConfig({
  plugins: [react(), tsconfigPaths()],
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: './vitest.setup.ts',
    css: true,
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
      exclude: [
        'node_modules/',
        '.next/',
        'vitest.config.ts',
        '**/*.d.ts',
        '**/*.config.*',
        '**/mockData/*',
      ],
    },
  },
});
```

**Task 2: Create `vitest.setup.ts`**

```typescript
import '@testing-library/jest-dom';
import { cleanup } from '@testing-library/react';
import { afterEach, vi } from 'vitest';

// Cleanup after each test
afterEach(() => {
  cleanup();
});

// Mock Next.js router
vi.mock('next/navigation', () => ({
  useRouter() {
    return {
      push: vi.fn(),
      replace: vi.fn(),
      prefetch: vi.fn(),
      back: vi.fn(),
    };
  },
  usePathname() {
    return '/';
  },
  useSearchParams() {
    return new URLSearchParams();
  },
}));

// Mock Next.js Image component
vi.mock('next/image', () => ({
  default: (props: any) => {
    // eslint-disable-next-line jsx-a11y/alt-text
    return <img {...props} />;
  },
}));
```

**Task 3: Create `playwright.config.ts`**

```typescript
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'html',
  
  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
  },

  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },
    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] },
    },
  ],

  webServer: {
    command: 'pnpm dev',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
  },
});
```

**Task 4: Initialize MSW**

```bash
# Create public/mockServiceWorker.js
npx msw init public/ --save
```

**Task 5: Create `mocks/handlers.ts`**

```typescript
import { http, HttpResponse } from 'msw';

export const handlers = [
  // Example: Mock GET /api/users
  http.get('/api/users', () => {
    return HttpResponse.json([
      { id: '1', name: 'John Doe', email: 'john@example.com' },
      { id: '2', name: 'Jane Smith', email: 'jane@example.com' },
    ]);
  }),

  // Example: Mock POST /api/users
  http.post('/api/users', async ({ request }) => {
    const newUser = await request.json();
    return HttpResponse.json(
      { id: '3', ...newUser },
      { status: 201 }
    );
  }),
];
```

**Task 6: Create `mocks/server.ts` (for Node/Vitest)**

```typescript
import { setupServer } from 'msw/node';
import { handlers } from './handlers';

export const server = setupServer(...handlers);
```

**Task 7: Update `vitest.setup.ts` with MSW**

```typescript
import { beforeAll, afterEach, afterAll } from 'vitest';
import { server } from './mocks/server';

// Start MSW server before all tests
beforeAll(() => server.listen({ onUnhandledRequest: 'warn' }));

// Reset handlers after each test
afterEach(() => server.resetHandlers());

// Clean up after all tests
afterAll(() => server.close());
```

---

#### Phase 3: Test Structure [5 min] 📁

**Create folder structure**:

```
project-root/
├── __tests__/              # Unit tests (alternative location)
├── e2e/                    # Playwright E2E tests
│   └── home.spec.ts
├── mocks/                  # MSW mock handlers
│   ├── handlers.ts
│   └── server.ts
├── src/
│   ├── app/
│   │   └── page.test.tsx   # Co-located component tests
│   ├── components/
│   │   ├── Button.tsx
│   │   └── Button.test.tsx
│   └── hooks/
│       ├── useUser.ts
│       └── useUser.test.ts
├── vitest.config.ts
├── vitest.setup.ts
└── playwright.config.ts
```

---

#### Phase 4: Example Tests [10 min] ✍️

**Component Test Example**:

```typescript
// src/components/Button.test.tsx
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, it, expect, vi } from 'vitest';
import { Button } from './Button';

describe('Button', () => {
  it('should render with text', () => {
    render(<Button>Click me</Button>);
    expect(screen.getByRole('button', { name: /click me/i })).toBeInTheDocument();
  });

  it('should call onClick when clicked', async () => {
    const handleClick = vi.fn();
    const user = userEvent.setup();
    
    render(<Button onClick={handleClick}>Click me</Button>);
    
    await user.click(screen.getByRole('button'));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  it('should be disabled when disabled prop is true', () => {
    render(<Button disabled>Click me</Button>);
    expect(screen.getByRole('button')).toBeDisabled();
  });
});
```

**Hook Test Example**:

```typescript
// src/hooks/useUser.test.ts
import { renderHook, waitFor } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import { useUser } from './useUser';

// MSW will handle the API mocking

describe('useUser', () => {
  it('should fetch user data', async () => {
    const { result } = renderHook(() => useUser('1'));

    // Initially loading
    expect(result.current.isLoading).toBe(true);

    // Wait for data
    await waitFor(() => {
      expect(result.current.isLoading).toBe(false);
    });

    expect(result.current.data).toEqual({
      id: '1',
      name: 'John Doe',
      email: 'john@example.com',
    });
  });
});
```

**API Route Test Example** (Next.js API routes):

```typescript
// app/api/users/route.test.ts
import { GET, POST } from './route';
import { describe, it, expect } from 'vitest';

describe('/api/users', () => {
  it('GET should return users list', async () => {
    const request = new Request('http://localhost:3000/api/users');
    const response = await GET(request);
    const data = await response.json();

    expect(response.status).toBe(200);
    expect(data).toHaveLength(2);
  });

  it('POST should create a new user', async () => {
    const request = new Request('http://localhost:3000/api/users', {
      method: 'POST',
      body: JSON.stringify({ name: 'New User', email: 'new@example.com' }),
    });

    const response = await POST(request);
    const data = await response.json();

    expect(response.status).toBe(201);
    expect(data.name).toBe('New User');
  });
});
```

**E2E Test Example** (Playwright):

```typescript
// e2e/home.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Home Page', () => {
  test('should display the home page', async ({ page }) => {
    await page.goto('/');
    
    await expect(page).toHaveTitle(/Home/);
    await expect(page.getByRole('heading', { name: /welcome/i })).toBeVisible();
  });

  test('should navigate to about page', async ({ page }) => {
    await page.goto('/');
    
    await page.getByRole('link', { name: /about/i }).click();
    
    await expect(page).toHaveURL(/\/about/);
    await expect(page.getByRole('heading', { name: /about/i })).toBeVisible();
  });

  test('should submit a form', async ({ page }) => {
    await page.goto('/contact');
    
    await page.getByLabel(/name/i).fill('John Doe');
    await page.getByLabel(/email/i).fill('john@example.com');
    await page.getByLabel(/message/i).fill('Hello!');
    
    await page.getByRole('button', { name: /submit/i }).click();
    
    await expect(page.getByText(/thank you/i)).toBeVisible();
  });
});
```

---

#### Phase 5: Update package.json [2 min] 📝

```json
{
  "scripts": {
    "test": "vitest",
    "test:ui": "vitest --ui",
    "test:coverage": "vitest --coverage",
    "test:e2e": "playwright test",
    "test:e2e:ui": "playwright test --ui",
    "test:e2e:debug": "playwright test --debug",
    "test:all": "pnpm test && pnpm test:e2e"
  }
}
```

---

#### Phase 6: CI/CD Integration [5 min] 🚀

**Create `.github/workflows/test.yml`**:

```yaml
name: Tests

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - uses: pnpm/action-setup@v2
        with:
          version: 8
      
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'pnpm'
      
      - name: Install dependencies
        run: pnpm install
      
      - name: Run unit tests
        run: pnpm test:coverage
      
      - name: Install Playwright browsers
        run: npx playwright install --with-deps
      
      - name: Run E2E tests
        run: pnpm test:e2e
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage/coverage-final.json
      
      - name: Upload Playwright report
        uses: actions/upload-artifact@v3
        if: always()
        with:
          name: playwright-report
          path: playwright-report/
          retention-days: 30
```

---

### Testing Guidelines

**Created as `TESTING.md` in project root**:

```markdown
# Testing Guide

## Running Tests

```bash
# Unit/Component tests
pnpm test              # Run in watch mode
pnpm test:ui           # Open Vitest UI
pnpm test:coverage     # Generate coverage report

# E2E tests
pnpm test:e2e          # Run all E2E tests
pnpm test:e2e:ui       # Playwright UI mode
pnpm test:e2e:debug    # Debug mode

# All tests
pnpm test:all          # Run everything
```

## Writing Tests

### Component Tests
- Focus on user behavior, not implementation
- Use `screen.getByRole()` for accessibility
- Test user interactions with `userEvent`
- Mock external dependencies with MSW

### API Route Tests
- Test both success and error cases
- Validate request/response shapes
- Check status codes
- Test authentication/authorization

### E2E Tests
- Test critical user flows
- Use data-testid sparingly (prefer accessible selectors)
- Keep tests independent
- Run against production build

## Best Practices

1. **Test Naming**: Describe behavior, not implementation
   ```typescript
   // ✅ Good
   it('should display error message when login fails', ...)
   
   // ❌ Bad
   it('should call setError', ...)
   ```

2. **Arrange-Act-Assert Pattern**:
   ```typescript
   it('should ...', () => {
     // Arrange: Set up test data & state
     const user = userEvent.setup();
     render(<Component />);
     
     // Act: Perform action
     await user.click(screen.getByRole('button'));
     
     // Assert: Verify outcome
     expect(screen.getByText(/success/i)).toBeInTheDocument();
   });
   ```

3. **Accessibility**: Always query by role
   ```typescript
   // ✅ Good - accessible
   screen.getByRole('button', { name: /submit/i })
   screen.getByLabelText(/email/i)
   
   // ❌ Bad - fragile
   screen.getByTestId('submit-button')
   screen.getByClassName('email-input')
   ```

## Coverage Goals

- Unit tests: 80%+
- Integration tests: Key user flows
- E2E tests: Critical paths only

## Troubleshooting

See [TROUBLESHOOTING.md](./TROUBLESHOOTING.md)
```

---

### Success Criteria

- [x] All dependencies installed
- [x] Configuration files created
- [x] Example tests added
- [x] Scripts in package.json
- [x] CI/CD workflow configured
- [x] Documentation created

**Test the setup**:
```bash
pnpm test          # Should run successfully
pnpm test:e2e      # Should pass E2E tests
```

---

## Alternative: Jest Setup

If user prefers Jest over Vitest:

```bash
pnpm add -D jest jest-environment-jsdom @testing-library/react @testing-library/jest-dom
```

**jest.config.js**:
```javascript
const nextJest = require('next/jest');

const createJestConfig = nextJest({
  dir: './',
});

const config = {
  setupFilesAfterEnv: ['<rootDir>/jest.setup.js'],
  testEnvironment: 'jest-environment-jsdom',
  preset: 'ts-jest',
};

module.exports = createJestConfig(config);
```

---

## Why This Stack?

| Tool | Reason |
|------|--------|
| **Vitest** | 5-10x faster than Jest, better DX, Vite native |
| **React Testing Library** | Industry standard, focuses on user behavior |
| **MSW** | Works with SSR/SSG, reliable API mocking |
| **Playwright** | Fast, reliable, great debugging, multi-browser |

## Post-Setup Commands

After setup completes, suggest:

```bash
# 1. Run tests to verify
pnpm test

# 2. Explore Vitest UI
pnpm test:ui

# 3. Generate example component with test
/generate-component Button --with-test

# 4. Write tests for existing components
/add-tests src/components/Header.tsx
```
```

---

## 🆘 Troubleshooting

Common issues and solutions: See `/setup-testing-troubleshooting.md`

**Quick fixes**:
- ResizeObserver errors → Auto-fixed in setup
- Translation errors → Auto-detected and mocked
- Duplicate package.json keys → Auto-removed
- Path aliases not working → Auto-configured with vite-tsconfig-paths

---

## 🎯 What's New (Based on Real Usage)

### Auto-Fixes Included:
- ✅ ResizeObserver mock
- ✅ scrollIntoView mock
- ✅ IntersectionObserver mock
- ✅ Duplicate msw.workerDirectory removal
- ✅ next-intl mock (if detected)
- ✅ Proper directory exclusions

### Smart Detection:
- ✅ Existing configs (merge instead of overwrite)
- ✅ Storybook integration
- ✅ playwright-bdd vs standard Playwright
- ✅ i18n library (next-intl, i18next)
- ✅ API routes (auto-generate mocks)
- ✅ Package manager (npm/pnpm/yarn)

### Better Error Handling:
- ✅ Pre-flight checks before setup
- ✅ Conflict resolution prompts
- ✅ Post-setup verification
- ✅ Detailed error messages with fixes

### Flexibility:
- ✅ Multiple setup options (--minimal, --with-storybook, --no-e2e, --clean)
- ✅ Smart component scanning
- ✅ Project-specific customizations
- ✅ Cleanup old configs option

---

## Related Commands

- `/generate-component` - Create component with tests
- `/add-tests` - Add tests to existing file
- `/plan-react` - Plan React features with testing
- `/setup-testing-troubleshooting` - Detailed troubleshooting guide
