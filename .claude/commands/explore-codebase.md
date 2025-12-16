# /explore-codebase - Analyze Codebase & Features

## Purpose

Explore and analyze your codebase to understand how features are implemented, trace code flow, find dependencies, and map architecture.

## Aliases

```bash
/explore-codebase [feature/component]
/explore [feature]              # Short alias
/analyze [feature]              # Alternative alias
```

## Usage

```bash
/explore-codebase "authentication"
/explore "user profile feature"
/explore "payment flow"
/explore --component="Button"
/explore --api="/api/users"
/explore --trace="checkout process"

# Save output to file
/explore "authentication" --output=docs/architecture/auth-analysis.md
/explore "payment" --output=docs/features/payment-flow.md
```

## Arguments

- `$ARGUMENTS`: Feature name, component, API route, or functionality to explore

## Flags

| Flag | Description | Example |
|------|-------------|---------|
| `--output=path` | Save analysis to specific file | `--output=docs/analysis.md` |
| `--component="Name"` | Focus on specific component | `--component="Button"` |
| `--api="route"` | Focus on API endpoint | `--api="/api/users"` |
| `--trace="flow"` | Trace execution flow | `--trace="checkout"` |
| `--show-tests` | Include test coverage details | `--show-tests` |
| `--show-deps` | Deep dependency analysis | `--show-deps` |
| `--format=json` | Output as JSON | `--format=json` |

---

## Workflow

Explore codebase for: **$ARGUMENTS**

{{ if --output flag provided }}
**Output will be saved to**: `$OUTPUT_PATH`
{{ endif }}

### Phase 1: Search & Locate 🔍

**Find relevant code**:

1. **Search for keywords**
   ```bash
   # Search in file names
   Find files matching: [feature-name]
   
   # Search in code content
   Grep for: "[feature-name]", "[Feature]", "[FEATURE]"
   ```

2. **Identify entry points**
   - Pages/routes where feature is used
   - Main components
   - API endpoints
   - Database models

3. **List findings**
   ```markdown
   Found in:
   - Files: [list]
   - Components: [list]
   - API routes: [list]
   - Database: [tables/models]
   ```

---

### Phase 2: Analyze Structure 🏗️

**Map the architecture**:

1. **Component hierarchy**
   ```
   Page
   └── FeatureContainer
       ├── FeatureHeader
       ├── FeatureList
       │   └── FeatureItem
       └── FeatureForm
   ```

2. **Data flow**
   ```
   User Action → Component → Hook → API Call → Backend → Database
   ```

3. **Dependencies**
   ```markdown
   External:
   - react-hook-form
   - zod
   - @tanstack/react-query
   
   Internal:
   - @/lib/api
   - @/components/ui
   ```

---

### Phase 3: Code Analysis 💻

**Analyze implementation**:

1. **Show key files with context**
   ```typescript
   // src/features/auth/LoginForm.tsx
   export function LoginForm() {
     const { login } = useAuth();  // ← Custom hook
     const form = useForm();       // ← react-hook-form
     
     // Key logic here
   }
   ```

2. **Identify patterns**
   - State management approach
   - Error handling strategy
   - Validation method
   - Testing coverage

3. **Note interesting details**
   - Design patterns used
   - Performance optimizations
   - Security measures
   - Edge cases handled

---

### Phase 4: Document Findings 📋

Generate comprehensive documentation of how the feature works.

{{ if --output flag provided }}

**Save to file**: Write complete analysis to `$OUTPUT_PATH`

Include all sections:
- ✅ File locations and structure
- ✅ Architecture overview with diagrams
- ✅ Data flow explanation
- ✅ Code snippets with context
- ✅ Dependencies and patterns
- ✅ Testing coverage
- ✅ Security measures
- ✅ Performance notes
- ✅ Known issues and TODOs
- ✅ How to modify guide

**File created**: `$OUTPUT_PATH` ready for team review and documentation

{{ else }}

**Display in chat**: Show analysis in conversation for immediate review

{{ endif }}

---

## Output Format

```markdown
## 🔍 Codebase Exploration: [Feature Name]

**Analyzed**: [Date]  
**Feature**: [Feature description]  
**Status**: [Active/Deprecated/In Progress]

---

### 📁 File Locations

**Main Files**:
- `src/features/[feature]/index.tsx` - Main entry point
- `src/features/[feature]/components/` - React components
- `src/features/[feature]/hooks/` - Custom hooks
- `app/api/[route]/route.ts` - API endpoints
- `prisma/schema.prisma` - Database models

**Related Files**:
- `src/lib/[feature]-utils.ts` - Utilities
- `src/types/[feature].ts` - Type definitions
- `__tests__/[feature].test.ts` - Tests

**Configuration**:
- `config/[feature].ts` - Feature config
- `.env` variables: `NEXT_PUBLIC_[FEATURE]_*`

---

### 🏗️ Architecture Overview

**Component Hierarchy**:
```
app/[route]/page.tsx
└── FeatureContainer (src/features/[feature]/FeatureContainer.tsx)
    ├── FeatureHeader (components/FeatureHeader.tsx)
    ├── FeatureList (components/FeatureList.tsx)
    │   └── FeatureItem (components/FeatureItem.tsx)
    └── FeatureForm (components/FeatureForm.tsx)
        ├── Input (src/components/ui/Input.tsx)
        └── Button (src/components/ui/Button.tsx)
```

**Folder Structure**:
```
src/features/[feature]/
├── components/
│   ├── FeatureHeader.tsx
│   ├── FeatureList.tsx
│   ├── FeatureItem.tsx
│   └── FeatureForm.tsx
├── hooks/
│   ├── useFeature.ts
│   ├── useFeatureForm.ts
│   └── useFeatureQuery.ts
├── api/
│   └── featureApi.ts
├── types/
│   └── feature.types.ts
├── utils/
│   └── featureHelpers.ts
└── index.tsx
```

---

### 🔄 Data Flow

**User Interaction Flow**:
```
1. User clicks button in FeatureForm
   ↓
2. handleSubmit() called
   ↓
3. useFeatureForm hook validates data (zod)
   ↓
4. featureApi.create() makes API call
   ↓
5. POST /api/features (app/api/features/route.ts)
   ↓
6. Middleware: auth check (middleware.ts)
   ↓
7. Database: INSERT into features table
   ↓
8. Response returned
   ↓
9. React Query updates cache
   ↓
10. UI re-renders with new data
```

**State Management**:
- **Server State**: React Query (useQuery, useMutation)
- **Form State**: React Hook Form
- **UI State**: useState in components
- **Global State**: [Context/Zustand/None]

---

### 💻 Key Code Snippets

**Main Component** (`src/features/[feature]/FeatureContainer.tsx`):
```typescript
// Lines 15-45
export function FeatureContainer() {
  // Data fetching
  const { data, isLoading } = useFeatureQuery();
  
  // Mutations
  const createMutation = useFeatureCreate();
  
  // Event handlers
  const handleCreate = (values) => {
    createMutation.mutate(values);
  };
  
  return (
    <div>
      <FeatureHeader />
      <FeatureList items={data} />
      <FeatureForm onSubmit={handleCreate} />
    </div>
  );
}
```

**Custom Hook** (`hooks/useFeatureQuery.ts`):
```typescript
// Lines 8-25
export function useFeatureQuery() {
  return useQuery({
    queryKey: ['features'],
    queryFn: async () => {
      const response = await fetch('/api/features');
      return response.json();
    },
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
}
```

**API Route** (`app/api/features/route.ts`):
```typescript
// Lines 10-30
export async function POST(request: Request) {
  // 1. Auth check
  const session = await getServerSession(authOptions);
  if (!session) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }
  
  // 2. Parse & validate
  const body = await request.json();
  const validated = featureSchema.parse(body);
  
  // 3. Database operation
  const feature = await prisma.feature.create({
    data: {
      ...validated,
      userId: session.user.id,
    },
  });
  
  // 4. Return response
  return NextResponse.json(feature, { status: 201 });
}
```

**Validation Schema** (`types/feature.types.ts`):
```typescript
// Lines 5-15
export const featureSchema = z.object({
  name: z.string().min(1).max(100),
  description: z.string().optional(),
  status: z.enum(['active', 'inactive']),
  priority: z.number().int().min(1).max(5),
});

export type Feature = z.infer<typeof featureSchema>;
```

---

### 🔗 Dependencies

**External Libraries**:
- `@tanstack/react-query` - Server state management
- `react-hook-form` - Form handling
- `zod` - Schema validation
- `@prisma/client` - Database ORM

**Internal Dependencies**:
- `@/lib/api` - API client utilities
- `@/components/ui` - Shared UI components
- `@/hooks/useAuth` - Authentication hook
- `@/lib/db` - Database connection

**Dependency Graph**:
```
FeatureContainer
  ├─→ useFeatureQuery (hooks/)
  │     └─→ React Query
  ├─→ FeatureForm (components/)
  │     ├─→ react-hook-form
  │     └─→ zod
  └─→ featureApi (api/)
        └─→ fetch API
```

---

### 🎨 Patterns & Practices

**Design Patterns**:
- ✅ **Container/Presentational**: Separates logic from UI
- ✅ **Custom Hooks**: Reusable logic extraction
- ✅ **Compound Components**: Flexible composition
- ✅ **Server Actions**: (if using Next.js 14)

**State Management**:
- Server state: React Query
- Form state: React Hook Form
- Optimistic updates: Enabled for mutations

**Error Handling**:
```typescript
// Client-side
try {
  await createMutation.mutateAsync(values);
  toast.success('Created successfully');
} catch (error) {
  toast.error(error.message);
}

// Server-side
if (!validated.success) {
  return NextResponse.json(
    { error: validated.error },
    { status: 400 }
  );
}
```

**Validation**:
- Client: Zod schema + react-hook-form
- Server: Same Zod schema (shared types)
- Database: Prisma schema constraints

---

### 🧪 Testing Coverage

**Test Files Found**:
- `__tests__/features/[feature]/FeatureContainer.test.tsx` ✅
- `__tests__/features/[feature]/FeatureForm.test.tsx` ✅
- `__tests__/api/features.test.ts` ✅

**Coverage**:
- Components: 85%
- Hooks: 92%
- API routes: 78%
- Utils: 95%

**What's Tested**:
- ✅ Rendering with different props
- ✅ User interactions (click, submit)
- ✅ Form validation
- ✅ API success/error cases
- ⚠️ Missing: Edge cases for empty data

**What's NOT Tested**:
- ❌ Loading states transitions
- ❌ Race conditions
- ❌ Concurrent mutations

---

### 🔐 Security Measures

**Authentication**:
- ✅ Middleware checks on API routes
- ✅ Session validation with NextAuth
- ✅ Protected pages with getServerSession

**Authorization**:
- ✅ User owns resource check
- ✅ Role-based access (if applicable)

**Data Validation**:
- ✅ Client-side with Zod
- ✅ Server-side with same schema
- ✅ SQL injection prevention (Prisma)

**XSS Prevention**:
- ✅ React escapes output by default
- ✅ No dangerouslySetInnerHTML used

---

### ⚡ Performance Optimizations

**Implemented**:
- ✅ React Query caching (5 min stale time)
- ✅ Memoization with `useMemo` for filtered lists
- ✅ `React.memo` on FeatureItem component
- ✅ Lazy loading for heavy components

**Opportunities**:
- 💡 Add pagination (currently loading all items)
- 💡 Virtual scrolling for long lists
- 💡 Debounce search input
- 💡 Preload next page on hover

---

### 🐛 Known Issues / TODOs

**From Code Comments**:
```typescript
// TODO: Add optimistic updates for delete
// FIXME: Handle race condition when editing same item
// HACK: Temporary workaround for validation bug
```

**GitHub Issues**:
- #123: Feature doesn't work on Safari
- #145: Performance issue with 1000+ items

---

### 🔄 Related Features

This feature interacts with:
- **User Authentication** (src/features/auth/)
- **Notifications** (src/features/notifications/)
- **Activity Log** (src/features/activity/)

**Shared Components**:
- Uses: `Button`, `Input`, `Modal` from `src/components/ui/`
- Provides: Nothing (self-contained)

---

### 📚 Documentation

**Internal Docs**:
- `docs/features/[feature].md` - Feature specification
- `docs/api/[feature].md` - API documentation

**External Resources**:
- [Design in Figma](url)
- [Product Spec](url)

---

### 🎯 How to Modify This Feature

**To add a new field**:
1. Update `featureSchema` in `types/feature.types.ts`
2. Update Prisma schema
3. Run `prisma migrate dev`
4. Update form in `FeatureForm.tsx`
5. Update tests

**To change validation**:
1. Modify Zod schema in `types/`
2. Tests will catch breaking changes

**To add new action**:
1. Add mutation hook in `hooks/`
2. Add API endpoint in `app/api/`
3. Add button/trigger in component
4. Add test

---

### 🚀 Quick Start (for New Developers)

**To work on this feature**:

1. **Install dependencies**:
   ```bash
   pnpm install
   ```

2. **Set up database**:
   ```bash
   pnpm db:push
   ```

3. **Start dev server**:
   ```bash
   pnpm dev
   ```

4. **Navigate to**:
   ```
   http://localhost:3000/[route]
   ```

5. **Key files to start with**:
   - `src/features/[feature]/index.tsx` - Overview
   - `components/FeatureForm.tsx` - Main interaction
   - `hooks/useFeature.ts` - Core logic

---

### 💡 Insights & Learnings

**Good Practices Found**:
- ✅ Type-safe with TypeScript
- ✅ Shared validation schemas
- ✅ Well-organized folder structure
- ✅ Proper error handling

**Areas for Improvement**:
- ⚠️ Could extract more reusable hooks
- ⚠️ Some components are too large (>200 lines)
- ⚠️ Missing E2E tests

**Interesting Approaches**:
- 💡 Uses React Query for all server state (consistent)
- 💡 Form and API use same Zod schema (DRY)
- 💡 Optimistic updates for better UX

---

### 🎓 For Learning

**If you want to understand**:
- **Data fetching**: Check `hooks/useFeatureQuery.ts`
- **Form handling**: Check `components/FeatureForm.tsx`
- **API design**: Check `app/api/features/route.ts`
- **Validation**: Check `types/feature.types.ts`

**Good examples of**:
- React Query usage
- Form validation with Zod
- Type-safe API routes
- Component composition

---

**Next Steps**:
→ `/plan-feature` to plan enhancements  
→ `/add-tests` to improve test coverage  
→ `/refactor` if code needs cleanup
```

---

## Examples

### Example 1: Explore Authentication

**Input**: `/explore "authentication"`

**Output**:
- Files: `src/features/auth/`, `app/api/auth/`
- Flow: Login → useAuth hook → NextAuth → Session
- Shows: Auth provider setup, session management, protected routes
- Dependencies: next-auth, bcrypt, prisma

### Example 2: Explore Payment

**Input**: `/explore "payment flow"`

**Output**:
- Traces: Checkout → Payment → Stripe → Webhook → Database
- Shows: Stripe integration, webhook handling, order updates
- Identifies: Security measures, error handling, retry logic

### Example 3: Find Component

**Input**: `/explore --component="Button"`

**Output**:
- Location: `src/components/ui/Button.tsx`
- Usage: Found in 47 files
- Variants: primary, secondary, outline, ghost
- Props: onClick, disabled, loading, icon

### Example 4: Trace API

**Input**: `/explore --api="/api/users"`

**Output**:
- Handler: `app/api/users/route.ts`
- Methods: GET, POST, PUT, DELETE
- Auth: Middleware protected
- Database: Prisma User model
- Tests: `__tests__/api/users.test.ts`

---

## Usage Examples

### Save Analysis for Documentation

```bash
# Analyze and save authentication flow
/explore "authentication" --output=docs/architecture/auth-flow.md

# Deep dive into payment with dependencies
/explore "payment" --show-deps --output=docs/features/payment-analysis.md

# Component analysis for design system docs
/explore --component="Button" --output=docs/components/button-usage.md

# API endpoint documentation
/explore --api="/api/users" --show-tests --output=docs/api/users-endpoint.md
```

### Quick Exploration (Display in Chat)

```bash
# Quick look at feature
/explore "user profile"

# Trace flow without saving
/explore --trace="checkout process"

# Component usage check
/explore --component="Modal"
```

---

## Output File Format

When using `--output=path`, the generated file includes:

```markdown
# Codebase Exploration: [Feature Name]

## Overview
[Summary and status]

## Architecture
[Component hierarchy, folder structure]

## Implementation Details
[Code snippets, patterns, data flow]

## Dependencies
[External and internal dependencies]

## Testing & Security
[Coverage, security measures]

## Modification Guide
[How to extend or modify]

## References
[Related features, documentation links]
```

**Benefits of saving to file**:
- ✅ **Team knowledge base**: Share with new developers
- ✅ **Architecture documentation**: Auto-generated docs
- ✅ **Onboarding material**: Understand features quickly
- ✅ **Planning reference**: Use when modifying features
- ✅ **Code review context**: Understand changes better

---

## Tips for Best Results

1. **Be specific**: "user authentication" > "auth"
2. **Use component names**: "Button component" finds exact match
3. **Use API routes**: "/api/users" finds endpoints
4. **Check tests**: Use `--show-tests` to see coverage
5. **Save important analyses**: Use `--output=docs/` for documentation
6. **Version control**: Commit saved analyses for team reference

---

## Related Commands

```bash
/auto-plan [feature]         # Auto-explore + analyze + plan (all-in-one)
/find [search-term]         # Quick file/code search
/plan-feature [feature]     # Plan new feature
/plan-refactor [feature]    # Plan refactoring
/add-tests [file]           # Add tests to file
/review [file]              # Code review
/research [technology]      # Research external tech (not codebase)
```

**Tip**: Instead of running `/explore` manually, use `/auto-plan` which automatically explores, analyzes, and generates a complete plan!

---

**Pro Tip**: Use `/explore --output=docs/` to build your project's architecture documentation automatically!
