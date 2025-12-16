# Testing Setup - Troubleshooting Guide

This guide covers common issues encountered during `/setup-testing` and how to resolve them.

---

## 🔧 Common Errors & Quick Fixes

### 1. ResizeObserver is not defined

**Error**:
```
ReferenceError: ResizeObserver is not defined
```

**Fix**: Auto-added to `vitest.setup.ts`

```typescript
// Already included in setup
global.ResizeObserver = vi.fn().mockImplementation(() => ({
  observe: vi.fn(),
  unobserve: vi.fn(),
  disconnect: vi.fn(),
}));
```

---

### 2. scrollIntoView is not a function

**Error**:
```
TypeError: element.scrollIntoView is not a function
```

**Fix**: Auto-added to `vitest.setup.ts`

```typescript
Element.prototype.scrollIntoView = vi.fn();
```

---

### 3. Duplicate msw.workerDirectory in package.json

**Error**:
```
Error: Duplicate key 'msw.workerDirectory' in package.json
```

**Fix**: Automatically removed during setup

```bash
# Manual fix if needed:
# Remove from package.json, MSW finds worker in public/ automatically
```

---

### 4. Translation/i18n Errors in Tests

**Error**:
```
Error: useTranslations() is not available in non-Client Components
```

**Fix**: Auto-detected if `next-intl` found

```typescript
// Auto-added to vitest.setup.ts if next-intl detected
vi.mock('next-intl', () => ({
  useTranslations: () => (key: string) => key,
  useLocale: () => 'en',
  useMessages: () => ({}),
}));
```

**Manual fix for custom i18n**:
```typescript
// vitest.setup.ts
vi.mock('@/lib/i18n', () => ({
  getTranslations: () => ({
    t: (key: string) => key,
  }),
}));
```

---

### 5. Playwright Browsers Not Installed

**Error**:
```
Error: browserType.launch: Executable doesn't exist
```

**Fix**:
```bash
npx playwright install
# or just chromium for faster install
npx playwright install chromium
```

**Note for M1/M2 Mac**:
- May need Rosetta 2: `softwareupdate --install-rosetta`
- Or install ARM browsers: `npx playwright install --with-deps`

---

### 6. playwright-bdd Conflict

**Error**:
```
Error: Conflicting Playwright configurations
```

**Detection**: Setup automatically detects `playwright-bdd`

**Resolution**:
- If BDD detected: Keeps existing config, adds examples only
- If converting: Prompts to migrate or keep separate

---

### 7. Vitest Config Not Found

**Error**:
```
Error: Cannot find vitest.config.ts
```

**Fix**: Run setup again or create manually

```bash
# Re-run setup
/setup-testing --vitest

# Or create minimal config
touch vitest.config.ts
```

---

### 8. Path Alias Not Working (@/...)

**Error**:
```
Error: Cannot find module '@/components/Button'
```

**Fix**: Auto-added `vite-tsconfig-paths` plugin

```typescript
// vitest.config.ts
import tsconfigPaths from 'vite-tsconfig-paths';

export default defineConfig({
  plugins: [react(), tsconfigPaths()],  // ← This resolves @/
});
```

---

### 9. CSS Import Errors

**Error**:
```
Error: Unknown file extension ".css"
```

**Fix**: Already configured in vitest.config.ts

```typescript
test: {
  css: true,  // ← This enables CSS
}
```

For CSS modules:
```typescript
test: {
  css: {
    modules: {
      classNameStrategy: 'non-scoped',
    },
  },
}
```

---

### 10. Next.js Image Component Errors

**Error**:
```
Error: Invalid src prop on `next/image`
```

**Fix**: Auto-mocked in vitest.setup.ts

```typescript
vi.mock('next/image', () => ({
  default: (props: any) => <img {...props} />,
}));
```

---

## 🍎 macOS/M1/M2 Specific Issues

### Rosetta 2 Required

Some dependencies may need Rosetta 2:

```bash
# Check if Rosetta is installed
pgrep -q oahd && echo "Rosetta is installed" || echo "Rosetta is NOT installed"

# Install Rosetta 2
softwareupdate --install-rosetta
```

### Playwright Browser Installation

```bash
# ARM-native browsers (recommended for M1/M2)
npx playwright install --with-deps

# Or install specific browser
npx playwright install chromium
```

### Permission Issues

If you get permission errors:

```bash
# May need admin for browser installation
sudo npx playwright install

# Or change npm global directory
mkdir ~/.npm-global
npm config set prefix '~/.npm-global'
```

---

## 🐛 Storybook Integration Issues

### Conflict with Vitest

**Fix**: Detected automatically, creates separate configs

```typescript
// vitest.config.ts - exclude Storybook
exclude: [
  '**/*.stories.*',
  '.storybook',
  'storybook-static',
]
```

### Shared Test Utilities

```typescript
// src/test/utils/index.ts
export * from '@testing-library/react';
export { default as userEvent } from '@testing-library/user-event';

// Both Vitest and Storybook can use
```

---

## 📦 Package Manager Issues

### pnpm Playwright Install

```bash
# pnpm may need this flag
pnpm exec playwright install
```

### Yarn Berry (v2+)

```bash
# Add .yarnrc.yml
nodeLinker: node-modules

# Then install
yarn install
```

---

## 🔄 Migration from Jest

### Automatic Cleanup

If `--clean` flag used:
- Backs up old Jest config
- Removes conflicting files
- Updates git ignore

### Manual Migration

```bash
# 1. Remove Jest
pnpm remove jest jest-environment-jsdom @types/jest

# 2. Remove configs
rm jest.config.js
rm jest.setup.js

# 3. Run Vitest setup
/setup-testing --vitest
```

### Convert Tests

Most tests work as-is, but change imports:

```typescript
// Before (Jest)
import { describe, it, expect } from '@jest/globals';

// After (Vitest)
import { describe, it, expect } from 'vitest';
```

---

## ⚡ Performance Issues

### Slow Test Execution

**Check**:
1. Too many files being processed
2. No exclusions in config
3. Heavy setup files

**Fix**:
```typescript
// vitest.config.ts
exclude: [
  'node_modules',
  'dist',
  '.next',
  'coverage',
  // Add problem directories
],
```

### Playwright Slow Startup

```bash
# Use headed mode for debugging only
pnpm test:e2e:debug

# Production: headless (faster)
pnpm test:e2e
```

---

## 🌐 Network/MSW Issues

### Handlers Not Working

**Check**:
1. MSW server started in setup file
2. Handlers imported correctly
3. Using correct MSW v2 syntax

**Fix**:
```typescript
// vitest.setup.ts
import { server } from './mocks/server';

beforeAll(() => server.listen({ onUnhandledRequest: 'warn' }));
afterEach(() => server.resetHandlers());
afterAll(() => server.close());
```

### CORS Errors in Tests

MSW should handle this, but if not:

```typescript
// mocks/handlers.ts
http.get('/api/data', () => {
  return HttpResponse.json(data, {
    headers: {
      'Access-Control-Allow-Origin': '*',
    },
  });
}),
```

---

## 🔐 Authentication Issues in Tests

### Next-Auth Mock

```typescript
// vitest.setup.ts
vi.mock('next-auth/react', () => ({
  useSession: () => ({
    data: {
      user: { id: '1', name: 'Test User', email: 'test@example.com' },
    },
    status: 'authenticated',
  }),
}));
```

### Custom Auth Hook

```typescript
vi.mock ('@/hooks/useAuth', () => ({
  useAuth: () => ({
    user: { id: '1', role: 'admin' },
    isAuthenticated: true,
    login: vi.fn(),
    logout: vi.fn(),
  }),
}));
```

---

## 📱 Environment Variables in Tests

### Loading .env.test

```typescript
// vitest.config.ts
import { loadEnv } from 'vite';

export default defineConfig(({ mode }) => ({
  define: {
    'process.env': loadEnv(mode, process.cwd(), ''),
  },
  // ... rest of config
}));
```

### Mock env vars

```typescript
// vitest.setup.ts
process.env.NEXT_PUBLIC_API_URL = 'http://localhost:3000/api';
process.env.NODE_ENV = 'test';
```

---

## 🆘 Still Having Issues?

### 1. Check Setup Verification

```bash
# Re-run verification
/setup-testing --verify
```

### 2. View Logs

```bash
# Vitest verbose mode
pnpm test --reporter=verbose

# Playwright debug
DEBUG=pw:api pnpm test:e2e
```

### 3. Clean Install

```bash
# Nuclear option
rm -rf node_modules
rm pnpm-lock.yaml
pnpm install
npx playwright install
```

### 4. Ask for Help

Include in your question:
- Node version: `node --version`
- Package manager: `pnpm --version`
- OS: macOS/Linux/Windows
- Error message (full stack trace)
- Relevant config files

---

## 📋 Diagnostic Checklist

Run through this if setup fails:

```markdown
## Setup Diagnostic

Environment:
- [ ] Node.js ≥ 18.0.0
- [ ] pnpm/npm/yarn installed
- [ ] Next.js project

Files Created:
- [ ] vitest.config.ts exists
- [ ] vitest.setup.ts exists
- [ ] mocks/handlers.ts exists
- [ ] mocks/server.ts exists
- [ ] playwright.config.ts exists (if E2E)

Dependencies:
- [ ] vitest installed
- [ ] @testing-library/react installed
- [ ] msw installed
- [ ] @playwright/test installed (if E2E)

Test Files:
- [ ] At least one .test.tsx file exists
- [ ] Can run `pnpm test`
- [ ] Tests pass

Common Mocks:
- [ ] ResizeObserver mocked
- [ ] scrollIntoView mocked
- [ ] next/navigation mocked
- [ ] next/image mocked
- [ ] i18n mocked (if applicable)
```

If all checked andiện still failing, it's likely a project-specific issue.

---

## 💡 Pro Tips

1. **Use test:ui for debugging**: `pnpm test:ui` is much easier than terminal
2. **Playwright trace viewer**: `pnpm test:e2e --trace on`
3. **Coverage reports**: Check `coverage/index.html` for gaps
4. **Test one file**: `pnpm test Button.test.tsx`
5. **Watch specific**: `pnpm test src/components`

---

**Need more help?** Check `/help` or ask in your team chat!
