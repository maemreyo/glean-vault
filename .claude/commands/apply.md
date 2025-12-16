# /apply - Apply Patterns from Explored Code

## Purpose

Apply architectural and code patterns from explored code (`/how` output) to new implementations. Leverages comprehensive exploration documentation to ensure consistent pattern replication.

**"Clone the DNA, not just the code"** - Apply proven patterns to new features.

## Aliases

```bash
/apply [source] --to=[target]
/apply-pattern [source] --to=[target]
```

## Usage

```bash
# Basic usage
/apply "authentication" --to="user-profile"

# With explicit docs path
/apply --from=docs/auth/ --to="admin-dashboard"

# Apply specific pattern only
/apply "calculator" --to="converter" --pattern="validation"

# Preview mode (no changes)
/apply "payment" --to="subscription" --preview
```

## Arguments

- `source`: Feature name (will look for docs in `docs/<source>/`) or explicit path
- `--to`: Target directory for pattern application

## Flags

| Flag | Description | Example |
|------|-------------|---------|
| `--from=path` | Explicit source docs folder | `--from=docs/auth/` |
| `--to=path` | Target directory (required) | `--to=src/profile/` |
| `--pattern=name` | Specific pattern to apply | `--pattern=validation` |
| `--preview` | Preview changes without applying | `--preview` |
| `--skip-review` | Skip review gates | `--skip-review` |

---

## Integration with /how

This command is designed to work seamlessly with `/how` output:

```bash
# Step 1: Explore source feature
/how "authentication"
→ Creates docs/authentication/phase-1-discovery-structure.md
→ Creates docs/authentication/phase-2-analysis.md

# Step 2: Apply patterns to new feature  
/apply "authentication" --to="user-management"
→ Reads docs/authentication/
→ Applies patterns to src/features/user-management/
→ Updates docs/authentication/README.md with application history
```

---

## Workflow

Execute for: **$SOURCE** → **$TARGET**

{{ if --from provided }}
**Source docs**: `$FROM_PATH`
{{ else }}
**Source docs**: `docs/$SOURCE/` (auto-detected)
{{ endif }}

**Target directory**: `$TO_PATH`

{{ if --pattern provided }}
**Specific pattern**: `$PATTERN`
{{ else }}
**Applying**: All patterns
{{ endif }}

{{ if --preview }}
**Mode**: Preview only (no changes)
{{ else }}
**Mode**: Apply changes
{{ endif }}

---

### Phase 1: Load Source Documentation 🔍

**Goal**: Extract patterns from `/how` exploration docs

**Duration**: 5-10 minutes

---

**Steps**:

1. **Locate documentation folder**
   ```bash
   {{ if --from provided }}
   DOCS_PATH="$FROM_PATH"
   {{ else }}
   DOCS_PATH="docs/$(echo "$SOURCE" | tr '[:upper:]' '[:lower:]' | tr ' ' '-')/"
   {{ endif }}
   ```

2. **Verify documentation exists**
   ```bash
   if [ ! -d "$DOCS_PATH" ]; then
     echo "❌ Documentation not found at: $DOCS_PATH"
     echo "💡 Run: /how \"$SOURCE\" first to generate docs"
     exit 1
   fi
   ```

3. **Read documentation files**
   - `phase-1-discovery-structure.md` → File inventory, architecture patterns, dependencies
   - `phase-2-analysis.md` → Code patterns, business logic, implementation details

4. **Extract patterns using `pattern-analysis` skill**

**Dispatch Pattern Analyzer SubAgent**:

```markdown
Pattern Analyzer SubAgent

GOAL: Extract reusable patterns from exploration docs

INPUT:
- Documentation path: $DOCS_PATH
{{ if --pattern provided }}
- Focus on specific pattern: $PATTERN
{{ else }}
- Extract all patterns
{{ endif }}

---

SUBTASK 1.1: Read Discovery & Structure Documentation (5 min)

**Steps**:
1. Read `phase-1-discovery-structure.md`
2. Extract:
   - File inventory and locations
   - Folder structure convention
   - File naming patterns
   - Component hierarchy
   - Architecture style (Container/Presentational, etc.)
   - State management approach
   - Dependencies used
   - Integration points

**Output**: Structure pattern summary

---

SUBTASK 1.2: Read Code Patterns (5-10 min)

**Steps**:
1. Read `phase-2-analysis.md`
2. Extract:
   - Business logic patterns
   - Error handling patterns
   - Validation approach (Zod, Yup, etc.)
   - Form handling (react-hook-form, Formik, etc.)
   - API communication pattern
   - Testing patterns
   - Type definitions style
   - Key insights and recommendations

**Output**: Code pattern summary

---

SUBTASK 1.3: Identify Reusable Components (5 min)

**Steps**:
1. List shared components used
2. Note their props/interfaces
3. Identify base utilities
4. Extract constants/config

**Output**: Component inventory

---

OUTPUT: Return pattern DNA to main agent

```markdown
📋 PATTERN DNA EXTRACTED

Source: $SOURCE
Documentation: $DOCS_PATH

---

## Folder Structure Pattern

```
src/features/[feature]/
├── components/
│   ├── [Feature]Header.tsx
│   ├── [Feature]Content.tsx
│   └── [Feature]Item.tsx
├── hooks/
│   ├── use[Feature].ts
│   └── use[Feature]Query.ts
├── api/
│   └── [feature]Api.ts
├── types/
│   └── [feature].types.ts
└── index.tsx
```

Convention: Feature-based with type subfolders

---

## Architecture Pattern

**Style**: Container/Presentational
- Container: Handles logic, state, API calls
- Presentational: Pure UI components

**State Management**: 
- Server State: React Query
- Form State: react-hook-form
- UI State: useState

**Data Flow**: Unidirectional (props down, events up)

---

## Code Patterns

### Form Handling
```typescript
// Pattern
const form = useForm({
  resolver: zodResolver(schema),
  defaultValues: {...}
});
```

### Validation
```typescript
// Pattern: Zod schema
const schema = z.object({
  field: z.string().min(1).max(100),
  ...
});
```

### API Communication
```typescript
// Pattern: React Query
const { data, isLoading } = useQuery({
  queryKey: ['entity'],
  queryFn: async () => entityApi.getAll()
});
```

### Error Handling
```typescript
// Pattern: Try/catch with toast
try {
  await mutation.mutateAsync(data);
  toast.success('Success message');
} catch (error) {
  toast.error(error.message);
}
```

---

## Testing Pattern

- Framework: Jest + React Testing Library
- File location: `__tests__/` or adjacent `*.test.tsx`
- Coverage: ~80% target
- Structure: `describe('[Component]', () => { it('should...') })`

---

## Dependencies

External:
- react-hook-form@7.x
- zod@3.x
- @tanstack/react-query@4.x

Internal:
- @/components/ui
- @/lib/api
- @/types

---

PATTERN EXTRACTION COMPLETE ✅
```
```

**Return**: Pattern DNA report to main agent

---

### Phase 2: Analyze Target Location 🎯

**Goal**: Understand target directory and identify adaptation needs

**Duration**: 5-10 minutes

---

**Dispatch Scout SubAgent**:

```markdown
Scout SubAgent - Target Analysis

GOAL: Analyze target directory for pattern application

INPUT:
- Target path: $TO_PATH
- Pattern DNA: [from Phase 1]

---

SUBTASK 2.1: Check Target Directory (3 min)

**Steps**:
1. Check if target directory exists
   - If exists: Analyze existing structure
   - If not exists: Plan directory creation

2. List existing files in target
3. Identify potential conflicts
4. Note existing patterns (if any)

**Output**: Target directory status

---

SUBTASK 2.2: Identify Adaptation Points (5 min)

**Steps**:
1. Compare target with source structure
2. Identify naming transformations needed:
   - Feature name: "$SOURCE" → "$TARGET_FEATURE"
   - File names: How to adapt
   - Component names: Transformation rules

3. Note integration points:
   - Existing API endpoints
   - Shared components to use
   - Existing types to extend

**Output**: Adaptation strategy

---

OUTPUT: Return target analysis

```markdown
📋 TARGET ANALYSIS

Target: $TO_PATH
Status: {{ Directory exists / Will be created }}

---

## Current Structure

{{ if directory exists }}
```
$TO_PATH/
├── existing-file-1.tsx
├── existing-file-2.ts
└── ...
```

Existing patterns detected:
- [List any existing patterns]

Conflicts:
{{ if conflicts exist }}
- File X will be overwritten
- Directory Y already has different structure
{{ else }}
- No conflicts detected
{{ endif }}

{{ else }}
Directory will be created fresh.
No conflicts.
{{ endif }}

---

## Naming Transformations

| Source Entity | Target Entity |
|---------------|---------------|
| "$SOURCE" | "$TARGET_FEATURE" |
| "use$SourceQuery" | "use$TargetQuery" |
| "$SourceApi" | "$TargetApi" |
| "$SOURCE_TYPES" | "$TARGET_TYPES" |

---

## Integration Points

- API base path: {{ Detect or suggest }}
- Shared components: {{ List available }}
- Existing types: {{ List to extend }}

---

TARGET ANALYSIS COMPLETE ✅
```
```

**Return**: Target analysis to main agent

---

### Phase 3: Create Adaptation Plan 📋

**Goal**: Create detailed plan for applying patterns to target

**Duration**: 10-15 minutes

---

**Dispatch Planner SubAgent**:

```markdown
Planner SubAgent - Pattern Application

GOAL: Create detailed application plan

INPUT:
- Pattern DNA: [from Phase 1]
- Target Analysis: [from Phase 2]
- Transformation rules: [naming mappings]

---

SUBTASK 3.1: Plan Directory Structure (5 min)

**Steps**:
1. Map source structure to target
2. Create directory creation plan

**Output**:
```markdown
Directories to create:
- $TO_PATH/
- $TO_PATH/components/
- $TO_PATH/hooks/
- $TO_PATH/api/
- $TO_PATH/types/
- $TO_PATH/__tests__/
```

---

SUBTASK 3.2: Plan File Generation (10-15 min)

**Steps**:
1. For each file in source pattern:
   - Determine target filename
   - Identify code transformations needed
   - List dependencies to update

2. Create file-by-file plan

**Output**:
```markdown
Files to create:

1. $TO_PATH/index.tsx
   - Purpose: Main entry point
   - Based on: [source file]
   - Transformations:
     * Replace import paths
     * Rename component/hook names
     * Update export names

2. $TO_PATH/components/$TargetHeader.tsx
   - Purpose: Header component
   - Based on: [source component]
   - Transformations:
     * Component name: $SourceHeader → $TargetHeader
     * Props interface: I$SourceProps → I$TargetProps
     * Update imports

[... for each file ...]
```

---

SUBTASK 3.3: Plan Verification Steps (5 min)

**Steps**:
1. Define acceptance criteria
2. List tests to run
3. Identify review checkpoints

**Output**:
```markdown
Verification Plan:

1. Compilation check
   - Run: tsc --noEmit (if TypeScript)
   - Expect: No errors

2. Test execution
   - Run: npm test $TO_PATH
   - Expect: All tests passing

3. Code review
   - Check: Pattern adherence
   - Check: No copy-paste errors
   - Check: Proper naming transformations

4. Manual review
   - Verify: Folder structure matches
   - Verify: Dependencies correctly imported
   - Verify: No leftover source names
```

---

OUTPUT: Return complete application plan

```markdown
📋 APPLICATION PLAN

Source: $SOURCE (docs at $DOCS_PATH)
Target: $TO_PATH
Estimated time: 20-30 minutes

---

## Phase A: Directory Setup (2 min)

Create directories:
- [ ] $TO_PATH/
- [ ] $TO_PATH/components/
- [ ] $TO_PATH/hooks/
- [ ] $TO_PATH/api/
- [ ] $TO_PATH/types/
- [ ] $TO_PATH/__tests__/

---

## Phase B: File Generation (15-20 min)

### Group 1: Type Definitions (5 min)

**File**: `$TO_PATH/types/$target.types.ts`
- Copy pattern from source types
- Transform: Entity names
- Add: Type exports

### Group 2: API Layer (5 min)

**File**: `$TO_PATH/api/$targetApi.ts`
- Copy API pattern
- Transform: Endpoint paths
- Transform: Function names
- Keep: Error handling pattern

### Group 3: Hooks (5-8 min)

**File**: `$TO_PATH/hooks/use$Target.ts`
- Copy hook pattern
- Transform: Hook names
- Update: API client imports
- Keep: React Query structure

**File**: `$TO_PATH/hooks/use$TargetForm.ts`
- Copy form hook pattern
- Transform: Schema name
- Update: Validation references

### Group 4: Components (8-10 min)

**File**: `$TO_PATH/components/$TargetHeader.tsx`
- Copy component structure
- Transform: Component name, props
- Update: Imports
- Keep: UI structure

**File**: `$TO_PATH/components/$TargetContent.tsx`
- [Similar...]

**File**: `$TO_PATH/components/$TargetItem.tsx`
- [Similar...]

### Group 5: Entry Point (2 min)

**File**: `$TO_PATH/index.tsx`
- Copy main structure
- Export all components
- Wire up providers (if any)

---

## Phase C: Testing (3-5 min)

- [ ] Create test files mirroring source
- [ ] Update test descriptions
- [ ] Run tests, expect passing

---

## Phase D: Verification (5 min)

- [ ] TypeScript compilation
- [ ] Linting
- [ ] Code review gate
- [ ] Manual check for leftover names

---

APPLICATION PLAN COMPLETE ✅
```
```

**Return**: Application plan to main agent

---

{{ if --preview }}

### Phase 4: Preview Changes 👁️

**Goal**: Show what would be created without making changes

**Steps**:

1. **Display directory structure**
   ```
   Changes to be made:
   
   $TO_PATH/                          [CREATE]
   ├── components/                    [CREATE]
   │   ├── $TargetHeader.tsx          [CREATE - 80 lines]
   │   ├── $TargetContent.tsx         [CREATE - 120 lines]
   │   └── $TargetItem.tsx            [CREATE - 60 lines]
   ├── hooks/                         [CREATE]
   │   ├── use$Target.ts              [CREATE - 40 lines]
   │   └── use$TargetForm.ts          [CREATE - 50 lines]
   ├── api/                           [CREATE]
   │   └── $targetApi.ts              [CREATE - 70 lines]
   ├── types/                         [CREATE]
   │   └── $target.types.ts           [CREATE - 45 lines]
   └── index.tsx                      [CREATE - 30 lines]
   
   Total: 9 files, ~495 lines
   ```

2. **Show sample transformations**
   ```diff
   Source component name:
   - export function AuthenticationHeader() {
   + export function UserProfileHeader() {
   
   Source hook name:
   - export function useAuthenticationQuery() {
   + export function useUserProfileQuery() {
   
   Source API path:
   - const endpoint = '/api/auth';
   + const endpoint = '/api/user-profile';
   ```

3. **Display next steps**
   ```
   To apply these changes, run:
   /apply "$SOURCE" --to="$TO_PATH"
   
   (without --preview flag)
   ```

**Output**: Preview complete

**END** (no changes made)

{{ else }}

### Phase 4: Apply Patterns 🏗️

**Goal**: Generate/modify code following extracted patterns

**Duration**: 20-30 minutes

---

**Dispatch Implementation SubAgent**:

```markdown
Implementation SubAgent - Pattern Application

GOAL: Generate code following pattern DNA and application plan

INPUT:
- Pattern DNA: [from Phase 1]
- Target Analysis: [from Phase 2]
- Application Plan: [from Phase 3]
- Transformation Rules: [naming mappings]

CONSTRAINTS:
- MUST follow source pattern structure exactly
- MUST apply all naming transformations
- MUST NOT copy-paste without transforming
- MUST preserve pattern intent

---

EXECUTION:

For each file in application plan:

1. Read application plan for this file
2. Load source pattern (from docs or inferred)
3. Apply transformations:
   - Entity names
   - Import paths
   - Function/component names
   - API endpoints
   - Type references

4. Generate target file
5. Verify:
   - No source names left
   - Imports resolve
   - Types are correct

---

SUBTASK 4.1: Create Directory Structure (2 min)

```bash
mkdir -p $TO_PATH/{components,hooks,api,types,__tests__}
```

---

SUBTASK 4.2: Generate Type Definitions (5 min)

**File**: `$TO_PATH/types/$target.types.ts`

Based on source pattern, generate:
```typescript
// Auto-generated from pattern
export interface $Target {
  id: string;
  // ... fields from source transformed
}

export const $targetSchema = z.object({
  // ... validation from source transformed
});

export type $Target = z.infer<typeof $targetSchema>;
```

---

SUBTASK 4.3: Generate API Layer (5 min)

**File**: `$TO_PATH/api/$targetApi.ts`

Based on source pattern:
```typescript
// Auto-generated from pattern
import { api } from '@/lib/api';
import type { $Target } from '../types/$target.types';

export const $targetApi = {
  getAll: async (): Promise<$Target[]> => {
    const response = await api.get('/api/$target-endpoint');
    return response.data;
  },
  // ... other methods from source pattern
};
```

---

SUBTASK 4.4: Generate Hooks (5-8 min)

Based on source hooks pattern, generate React Query hooks

---

SUBTASK 4.5: Generate Components (8-10 min)

For each component in pattern:
1. Copy component structure
2. Apply transformations
3. Update imports
4. Preserve UI/logic patterns

---

SUBTASK 4.6: Generate Entry Point (2 min)

Create main index.tsx with exports

---

SUBTASK 4.7: Generate Tests (Optional, 5-8 min)

If tests exist in source:
1. Copy test structure
2. Transform test descriptions
3. Update component/hook names
4. Keep test patterns

---

OUTPUT: Return implementation summary

```markdown
✅ IMPLEMENTATION COMPLETE

Target: $TO_PATH
Files created: 9
Lines generated: ~500

---

## Files Created

### Type Definitions
- ✅ types/$target.types.ts (45 lines)

### API Layer
- ✅ api/$targetApi.ts (70 lines)

### Hooks
- ✅ hooks/use$Target.ts (40 lines)
- ✅ hooks/use$TargetForm.ts (50 lines)

### Components
- ✅ components/$TargetHeader.tsx (80 lines)
- ✅ components/$TargetContent.tsx (120 lines)
- ✅ components/$TargetItem.tsx (60 lines)

### Entry
- ✅ index.tsx (30 lines)

### Tests (if generated)
- ✅ __tests__/$target.test.tsx (50 lines)

---

## Patterns Applied

✅ Folder structure: Matches source exactly
✅ State management: React Query pattern preserved
✅ Form handling: react-hook-form + zod preserved
✅ Error handling: try/catch + toast pattern preserved
✅ Validation: Zod schema pattern preserved
✅ API communication: Same pattern as source

---

## Transformations Applied

- Entity name: "$SOURCE" → "$TARGET"
- All file names updated
- All imports updated
- All component/hook names updated
- API endpoints updated

---

READY FOR VERIFICATION ✅
```
```

**Return**: Implementation summary to main agent

---

### Phase 5: Verify Application 🧪

**Goal**: Ensure patterns applied correctly

**Duration**: 10-15 minutes

---

**Steps**:

1. **Check file creation**
   ```bash
   ls -R $TO_PATH
   # Verify all files exist
   ```

2. **Run TypeScript compilation** (if applicable)
   ```bash
   tsc --noEmit
   # or
   pnpm type-check
   ```
   
   Expected: ✅ No errors

3. **Run linter**
   ```bash
   pnpm lint $TO_PATH
   ```
   
   Expected: ✅ No errors or warnings

4. **Check for leftover source names**
   ```bash
   grep -r "$SOURCE" $TO_PATH
   ```
   
   Expected: ✅ No matches (or only in comments/strings)

5. **Run tests**
   ```bash
   pnpm test $TO_PATH
   ```
   
   Expected: ✅ All tests passing

{{ if not --skip-review }}

6. **Dispatch Code Reviewer SubAgent**

```markdown
Code Reviewer SubAgent

GOAL: Verify pattern application quality

REVIEW SCOPE: $TO_PATH

CHECK:
- [ ] Folder structure matches source pattern
- [ ] File names follow transformation rules
- [ ] No copy-paste errors (leftover source names)
- [ ] Imports are correct
- [ ] Types are properly defined
- [ ] Components follow pattern structure
- [ ] Tests exist and pass
- [ ] No compilation errors
- [ ] Follows project conventions

RETURN:
- Critical issues (must fix)
- Important issues (should fix)
- Minor issues (can defer)
- Approval status
```

**Handle review findings**:

```markdown
{{ if critical or important issues }}
  1. List issues to user
  2. Dispatch fix subagent for each
  3. Re-run verification
  4. Re-request review
  5. Repeat until clean
{{ else }}
  Proceed to completion
{{ endif }}
```

{{ endif }}

---

**Verification Report**:

```markdown
✅ VERIFICATION COMPLETE

Target: $TO_PATH

---

## Checks Passed

✅ Files created successfully (9 files)
✅ TypeScript compilation: No errors
✅ Linting: Clean
✅ Leftover names: None found
✅ Tests: {{ X }} passing, {{ Y }} failing
{{ if review passed }}
✅ Code review: Approved
{{ endif }}

{{ if issues }}
---

## Issues Found

{{ list issues with severity }}

{{ if critical }}
⚠️  CRITICAL ISSUES - Must fix before using
{{ endif }}

{{ if important }}
⚠️  IMPORTANT ISSUES - Should fix soon
{{ endif }}

{{ if minor }}
ℹ️  MINOR ISSUES - Can defer
{{ endif }}

{{ endif }}

---

APPLICATION VERIFIED ✅
```

{{ endif }}

---

## Completion

```markdown
✅ PATTERN APPLICATION COMPLETE

Source: $SOURCE (docs/$SOURCE/)
Target: $TO_PATH

---

## Summary

**Pattern Applied**: $SOURCE architecture → $TARGET implementation
**Files Created**: {{ count }} files (~{{ lines }} lines)
**Tests**: {{ passing }}/{{ total }} passing
**Status**: {{ Ready to use / Needs fixes }}

---

## What Was Created

Your new feature at `$TO_PATH` now has:

✅ Same folder structure as $SOURCE
✅ Same architecture patterns
✅ Same state management approach
✅ Same validation/error handling patterns
✅ Properly transformed naming
✅ Working tests (if source had tests)

---

## Next Steps

1. **Review the code**: Check generated files in `$TO_PATH`

2. **Customize business logic**: 
   - Update validation rules for your specific needs
   - Modify API endpoints if different
   - Adjust UI components for your use case

3. **Run the feature**:
   ```bash
   pnpm dev
   # Navigate to your new feature
   ```

4. **Add more tests** (if needed):
   ```bash
   /test-from "$TARGET" --coverage=90
   ```

5. **Refactor if needed**:
   ```bash
   /refactor-from "$TARGET" --improve="specific area"
   ```

---

🎉 Pattern successfully applied! Your new feature follows the same proven patterns as $SOURCE.
```

---

### Phase 6: Update Source Documentation 📝

**Goal**: Track pattern application in source documentation

**Duration**: 2-3 minutes

---

**Steps**:

1. **Update README.md** in source docs folder
   - Append application history to `docs/$SOURCE/README.md`

2. **Add application record**:

```markdown
## Pattern Applications

This pattern has been applied to the following features:

### $TARGET (applied on [date])
- **Location**: `$TO_PATH`
- **Applied by**: `/apply` command
- **Files created**: {{ count }} files
- **Status**: ✅ Complete

**What was replicated**:
- ✅ Folder structure
- ✅ Component hierarchy  
- ✅ State management patterns
- ✅ Validation patterns
- ✅ Error handling
- ✅ Testing structure
```

**Output**: Documentation updated ✅

---

## Final Completion

```markdown
✅ PATTERN APPLICATION COMPLETE

Source: $SOURCE (docs/$SOURCE/)
Target: $TO_PATH
Documentation: ✅ Updated

---

🎉 Pattern successfully applied and tracked!
```

---

## Success Criteria

- [ ] Source documentation loaded successfully
- [ ] Target location analyzed
- [ ] Application plan created
- [ ] All files generated correctly
- [ ] Naming transformations applied
- [ ] No leftover source names
- [ ] TypeScript compiles
- [ ] Tests pass
- [ ] Code review approved (if not skipped)

---

## Examples

### Example 1: Apply Auth Pattern to User Profile

```bash
/apply "authentication" --to="user-profile"
```

**Output**:
```
✅ Applying patterns from docs/authentication/ to src/features/user-profile/

Patterns identified:
- JWT-based authentication flow
- react-hook-form + zod validation
- Token refresh mechanism
- Protected route pattern

Creating 9 files in src/features/user-profile/...

Files created:
- ✅ types/user-profile.types.ts
- ✅ api/userProfileApi.ts
- ✅ hooks/useUserProfile.ts
- ✅ hooks/useUserProfileForm.ts
- ✅ components/UserProfileHeader.tsx
- ✅ components/UserProfileContent.tsx
- ✅ components/UserProfileItem.tsx
- ✅ index.tsx
- ✅ __tests__/user-profile.test.tsx

Tests: ✅ 12 passing
Review: ✅ Passed

✅ Pattern application complete!
```

### Example 2: Apply Specific Validation Pattern

```bash
/apply "calculator" --to="converter" --pattern="validation"
```

**Output**:
```
✅ Applying validation pattern from docs/calculator/ to src/converter/

Pattern: Zod schema with custom validators

Creating:
- ✅ src/converter/validation/schema.ts (adapted from calculator)

Pattern applied successfully!
Only validation pattern copied, other code untouched.
```

### Example 3: Preview Mode

```bash
/apply "payment" --to="subscription" --preview
```

**Output**:
```
📋 PREVIEW: Pattern Application

Source: payment (docs/payment/)
Target: subscription (src/features/subscription/)

Would create:
- src/features/subscription/              [DIR]
- src/features/subscription/components/   [DIR]
  - SubscriptionHeader.tsx               [CREATE - 85 lines]
  - SubscriptionForm.tsx                 [CREATE - 150 lines]
  - SubscriptionList.tsx                 [CREATE - 90 lines]
- src/features/subscription/hooks/       [DIR]
  - useSubscription.ts                   [CREATE - 45 lines]
  - useSubscriptionForm.ts               [CREATE - 55 lines]
...

Sample transformations:
- PaymentHeader → SubscriptionHeader
- usePaymentQuery → useSubscriptionQuery
- /api/payments → /api/subscriptions

Total: 9 files, ~550 lines would be created

To apply, run without --preview flag.
```

---

## Related Commands

- `/how [feature]` - Explore code to generate pattern docs (prerequisite)
- `/mimic [instruction]` - Alternative pattern cloning approach
- `/extend [feature]` - Extend existing feature with new capabilities
- `/test-from [feature]` - Generate tests from exploration docs

---

## Pro Tips

1. **Always run `/how` first**: This command requires exploration docs
   ```bash
   /how "authentication"  # Generate docs first
   /apply "authentication" --to="new-feature"  # Then apply
   ```

2. **Use preview mode** when unsure:
   ```bash
   /apply "source" --to="target" --preview
   ```

3. **Apply specific patterns** to avoid overwriting:
   ```bash
   /apply "source" --to="target" --pattern="validation"
   ```

4. **Combine with `/extend`** for incremental development:
   ```bash
   /apply "auth" --to="profile"        # Clone base pattern
   /extend "profile" --with="avatar"   # Add new capability
   ```

---

**Remember**: This command clones the pattern structure and approach, not the business logic. You'll still need to customize for your specific requirements!
