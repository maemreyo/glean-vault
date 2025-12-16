# /plan-migration - Smart Migration Planning with Auto-Exploration

## Purpose

Intelligently plan code migrations by **automatically exploring the old implementation** before creating the migration plan. No manual exploration needed!

## Usage

```bash
# Simple: Auto-explore and plan
/plan-migration "salary calculator from old project"

# With specific source
/plan-migration "payment flow" --source=legacy/payment

# Save outputs
/plan-migration "user auth" \
  --source=old-app/auth \
  --analysis=docs/migration/auth-analysis.md \
  --plan=plans/auth-migration.md

# For React/Next.js
/plan-migration "dashboard components" --react

# For API endpoints
/plan-migration "user API" --api
```

## Arguments

- `$ARGUMENTS`: Feature/module name to migrate from old codebase

## Flags

| Flag | Description | Example |
|------|-------------|---------|
| `--source=path` | Path to old implementation (auto-detect if not specified) | `--source=old-app/features/auth` |
| `--target=path` | Target directory for new implementation | `--target=src/features/auth` |
| `--analysis=path` | Where to save exploration analysis | `--analysis=docs/analysis.md` |
| `--plan=path` | Where to save migration plan | `--plan=plans/migration.md` |
| `--react` | Optimize for React/Next.js migration | `--react` |
| `--api` | Optimize for API endpoint migration | `--api` |
| `--include-tests` | Explore and plan test migration | `--include-tests` |
| `--estimate` | Include time estimates | `--estimate` |

---

## Intelligent Workflow

This command runs a **3-phase automated workflow**:

```
Phase 1: EXPLORE (Auto)
  ↓
Phase 2: ANALYZE (Auto)  
  ↓
Phase 3: PLAN (Auto with full context)
  ↓
Output: Complete migration plan ready for /execute-plan
```

---

### Phase 1: Auto-Explore Old Implementation 🔍

**Automatically finds and explores old code**:

```markdown
1. **Detect Source** (if not --source provided):
   - Search for: "[feature-name]" in common locations
   - Check: old-app/, legacy/, previous/, docs/migration/
   - Find: Most relevant implementation

2. **Deep Exploration**:
   Run: /explore-codebase "[feature]" --source=[detected-path]
   
   Captures:
   - ✅ All business logic
   - ✅ Data models and interfaces
   - ✅ API endpoints and routes
   - ✅ Dependencies (external + internal)
   - ✅ Validation rules
   - ✅ Edge cases and error handling
   - ✅ Test coverage (if exists)
   - ✅ Security measures
   - ✅ Performance optimizations

3. **Save Analysis** (if --analysis flag):
   File: `analysis/[feature]-old-implementation.md`
   
   Or display summary in chat
```

**Example Auto-Exploration Output**:
```markdown
🔍 Exploring old implementation...

Found: old-app/modules/Tools/SalaryConversion/
Files analyzed:
- SalaryContent/index.tsx (250 lines)
- API integration: api-dev.finzone.vn/tools/salary
- Store: useSalaryConversionStore (Zustand)
- Dependencies: react-hook-form, zod

Key findings:
✅ Tax brackets: 7 progressive levels
✅ Insurance: Employee 10.5%, Employer 21.5%
✅ Regional zones: 4 levels
✅ Net ↔ Gross conversion (bidirectional)
✅ Detailed breakdown display
⚠️  Tests: Minimal coverage (23%)
⚠️  Complexity: Some large components (>200 lines)

Analysis saved to: analysis/salary-old-implementation.md
```

---

### Phase 2: Auto-Analyze Patterns & Requirements 📊

**Extracts actionable insights**:

```markdown
1. **Business Logic Analysis**:
   - Tax calculation formula
   - Insurance deduction rules
   - Allowance calculations
   - Regional variations
   - Validation constraints

2. **Technical Pattern Analysis**:
   - Component architecture
   - State management approach
   - API communication pattern
   - Form handling strategy
   - Error handling method

3. **Identify Migration Challenges**:
   - Breaking changes needed
   - Dependencies to update
   - Tests to create
   - Edge cases to handle

4. **Extract Reusable Patterns**:
   - Components to replicate
   - Logic to preserve
   - Patterns to follow
   - Anti-patterns to avoid
```

**Example Analysis Output**:
```markdown
📊 Analysis Summary:

Business Rules to Preserve:
1. Tax Brackets (7 levels): 5%, 10%, 15%, 20%, 25%, 30%, 35%
2. Insurance Rates: 
   - Employee: SI 8%, HI 1.5%, UI 1%
   - Employer: SI 17.5%, HI 3%, UI 1%
3. Allowances: 11M self + 4.4M per dependent
4. Regions: I (4.68M), II (4.16M), III (3.64M), IV (3.25M)

Patterns to Follow:
✅ API-based calculation (backend heavy)
✅ Zustand for state management
✅ React Hook Form + Zod validation
✅ Detailed result breakdown

Improvements Needed:
⚠️  Add comprehensive tests
⚠️  Split large components
⚠️  Add loading/error states
⚠️  Improve TypeScript types
```

---

### Phase 3: Generate Complete Migration Plan 📋

**Creates detailed, execution-ready plan with full context**:

```markdown
1. **Plan Structure**:
   Based on analysis, create phases:
   
   Phase 1: Foundation & Setup
   - Type definitions (ISalary interface)
   - Constants (tax brackets, rates)
   - Utility functions
   
   Phase 2: Core Logic
   - Tax calculation engine
   - Insurance deduction calculator
   - Allowance calculator
   - Regional handler
   
   Phase 3: Components
   - Input form (with validation)
   - Results display
   - Breakdown view
   - Regional selector
   
   Phase 4: Integration
   - API connection
   - Store setup
   - Error handling
   - Loading states
   
   Phase 5: Testing
   - Unit tests for calculations
   - Component tests
   - Integration tests
   - Edge case tests
   
   Phase 6: Polish
   - Accessibility
   - Performance
   - Documentation

2. **Task Details**:
   Each task includes:
   - **Context**: Reference to old implementation
   - **Strategy**: How to approach (not exact code)
   - **Acceptance Criteria**: What "done" means
   - **Example Pattern**: Reference implementation
   - **Expected Result**: ✅/❌ Test result

3. **Preservation Notes**:
   ```markdown
   ⚠️  MUST PRESERVE:
   - Tax bracket formula (line 65-73 in old code)
   - Insurance calculation order (SI → HI → UI)
   - Regional minimum validation logic
   
   ✅ CAN IMPROVE:
   - Component structure (split large files)
   - Type safety (add strict types)
   - Test coverage (from 23% to 80%+)
   ```
```

**Example Generated Plan**:
```markdown
# Migration Plan: Salary Calculator

## Context
Migrating from: old-app/modules/Tools/SalaryConversion/
Analysis: analysis/salary-old-implementation.md

## Estimate: 6-8 hours | Risk: Medium | Confidence: High

---

## Phase 1: Foundation [1h]

### Task 1.1: Create ISalary Interface (10m)
**File**: `src/types/salary.ts`

**Context**:
- Old interface: old-app/modules/Tools/SalaryConversion/types.ts (lines 5-25)
- Must preserve all fields from old implementation
- Add strict TypeScript types

**Strategy**:
1. Study old ISalary interface
2. Add missing fields (if any)
3. Use strict number types
4. Add JSDoc comments

**Acceptance Criteria**:
- [ ] All fields from old interface present
- [ ] Strict TypeScript types used
- [ ] Documented with JSDoc

**Expected**: ✅ Interface compiles without errors

---

### Task 1.2: Define Tax Bracket Constants (15m)
**File**: `src/lib/salary/constants.ts`

**Context**:
- Old tax logic: SalaryContent/index.tsx (lines 65-73)
- 7 progressive tax brackets
- CRITICAL: Must match exactly

**Business Rules to Preserve**:
```typescript
// From old implementation - DO NOT CHANGE THESE VALUES
const TAX_BRACKETS = [
  { max: 5_000_000, rate: 0.05 },      // 5%
  { max: 10_000_000, rate: 0.10 },     // 10%
  { max: 18_000_000, rate: 0.15 },     // 15%
  { max: 32_000_000, rate: 0.20 },     // 20%
  { max: 52_000_000, rate: 0.25 },     // 25%
  { max: 80_000_000, rate: 0.30 },     // 30%
  { max: Infinity, rate: 0.35 },       // 35%
];
```

**Strategy**:
1. Create constant file
2. Copy exact bracket values from old code
3. Add TypeScript types
4. Export for use in calculator

**Test**:
- Write test that verifies bracket values match old implementation

**Expected**: ✅ Tests pass, values identical to old system

---

[... complete detailed breakdown ...]

## Phase 2: Core Logic [2h]

### Task 2.1: Implement Tax Calculator (30m)
**File**: `src/lib/salary/calculate-tax.ts`

**Context**:
- Old logic: SalaryContent/index.tsx (lines 80-120)
- Progressive tax calculation
- Must handle all 7 brackets

**Strategy**:
1. Study old calculateTax function
2. Understand progressive calculation
3. Write test FIRST (TDD):
   ```typescript
   // Test case from old system
   calculateTax(6_900_000) // Should = 440,000
   // Breakdown: 5M × 5% + 1.9M × 10%
   ```
4. Implement following same algorithm
5. Verify against old system's test cases

**Acceptance Criteria**:
- [ ] Handles all 7 tax brackets
- [ ] Progressive calculation correct
- [ ] Matches old system results
- [ ] Pure function (no side effects)

**Expected**: ✅ All edge case tests pass

---

[... all tasks with full context ...]

## Migration Checklist

Before execution:
- [ ] Read analysis file: analysis/salary-old-implementation.md
- [ ] Understand all business rules
- [ ] Review old code patterns
- [ ] Note critical sections to preserve

During execution:
- [ ] Follow TDD cycle per task
- [ ] Reference old code frequently
- [ ] Test against old system outputs
- [ ] Commit after each logical unit

After execution:
- [ ] /verify-against-spec salary-calculation-flow.md
- [ ] Compare outputs with old system
- [ ] Test all edge cases
- [ ] Document any deviations
```

---

## Output Files

### If --analysis flag provided:
```
analysis/[feature]-old-implementation.md
```
Contains:
- Complete exploration results
- Business logic documentation
- Technical patterns
- Migration notes

### If --plan flag provided:
```
plans/[feature]-migration.md
```
Contains:
- Complete migration plan
- References to analysis
- TDD micro-tasks
- Preservation notes

### If no flags:
Displays both analysis and plan in chat for immediate review

---

## Smart Features

### 1. Auto-Detection
```bash
/plan-migration "salary calculator"

# Auto-detects:
# - Old location: Searches common migration paths
# - Feature type: React component, API, utility
# - Dependencies: Scans imports
# - Test files: Finds associated tests
```

### 2. Context Preservation
```markdown
Every task includes:
- Reference to old code (file + line numbers)
- "MUST PRESERVE" critical business logic
- "CAN IMPROVE" technical enhancements
- Test cases from old system
```

### 3. Risk Assessment
```markdown
Automatic risk scoring:
- High: Complex algorithms, many dependencies
- Medium: Standard features, some complexity
- Low: Simple utilities, well-isolated

Flags risky sections for extra care
```

### 4. Compatibility Checks
```markdown
Checks:
- ✅ Old dependencies still available?
- ✅ Breaking changes in libraries?
- ✅ API changes needed?
- ⚠️  Flags compatibility issues upfront
```

---

## Examples

### Example 1: Basic Migration

```bash
/plan-migration "salary calculator"
```

**What happens**:
1. Searches for "salary" in old code
2. Finds: `old-app/modules/Tools/SalaryConversion/`
3. Explores: Components, API, logic, tests
4. Analyzes: Extracts business rules and patterns
5. Generates: Complete migration plan with 45 micro-tasks
6. Displays: Plan in chat for review

### Example 2: Migration with Files

```bash
/plan-migration "payment processing" \
  --source=legacy/payment \
  --analysis=docs/migration/payment-analysis.md \
  --plan=plans/payment-migration.md \
  --include-tests
```

**What happens**:
1. Explores: `legacy/payment/` directory
2. Saves analysis to: `docs/migration/payment-analysis.md`
3. Generates plan to: `plans/payment-migration.md`
4. Includes test migration tasks
5. Reports: File locations and contents

### Example 3: React Component Migration

```bash
/plan-migration "user profile dashboard" \
  --source=old-app/components/UserProfile \
  --target=src/features/user-profile \
  --react \
  --analysis=docs/migration/user-profile-old.md \
  --plan=plans/user-profile-migration.md
```

**What happens**:
1. Explores React patterns in old code
2. Identifies: component tree, hooks, state management
3. Analyzes: Props, context, styling approach
4. Generates React-optimized plan:
   - Component-by-component migration
   - Hook extraction
   - State management setup
   - Styling approach
5. Saves to specified files

### Example 4: API Migration

```bash
/plan-migration "user authentication API" \
  --source=api-old/auth \
  --api \
  --include-tests
```

**What happens**:
1. Explores API routes and handlers
2. Documents: Endpoints, methods, auth flow
3. Analyzes: Middleware, validation, database
4. Generates API-focused plan:
   - Route setup
   - Middleware migration
   - Database schema
   - Auth flow
   - API tests

---

## Integration with Other Commands

### Execute After Planning

```bash
# 1. Generate migration plan
/plan-migration "salary calculator" --plan=plans/salary.md

# 2. Execute with subagents
/execute-plan plans/salary.md

# 3. Verify completeness
/verify-against-spec salary-calculation-flow.md --code=src/features/salary
```

### Update Existing Migration

```bash
# 1. Initial migration
/plan-migration "feature-v1" --plan=plans/feature.md

# 2. Re-analyze after discovering more requirements
/plan-migration "feature-v1" \
  --source=old-app/feature-v1-extended \
  --plan=plans/feature-updated.md

# 3. Compare plans
diff plans/feature.md plans/feature-updated.md
```

---

## Tips for Best Results

1. **Let it auto-detect**: Don't specify --source unless needed
2. **Save analysis files**: Always use --analysis for documentation
3. **Review before executing**: Check generated plan makes sense
4. **Preserve business logic**: Pay attention to "MUST PRESERVE" notes
5. **Test against old system**: Compare outputs during migration

---

## Pro Tips

### For Complex Migrations

```bash
# Break into phases
/plan-migration "complex-feature-core" --plan=plans/phase-1.md
/plan-migration "complex-feature-ui" --plan=plans/phase-2.md
/plan-migration "complex-feature-integration" --plan=plans/phase-3.md
```

### For Team Migrations

```bash
# Generate analysis for team review
/plan-migration "feature" \
  --analysis=docs/migration/feature-analysis.md

# Team reviews analysis
# Then generate plan

/plan-react --context=docs/migration/feature-analysis.md \
  --output=plans/feature-final.md \
  "migrate feature with team feedback"
```

---

## Related Commands

```bash
/auto-plan [feature]            # Universal auto-planning (works for any code type)
/explore-codebase [feature]     # Manual exploration only
/plan-react [feature]           # Plan without auto-explore
/execute-plan [plan]            # Execute migration plan
/verify-against-spec [spec]     # Verify migration completeness
/audit-implementation [plan]    # Check if complete
```

**Note**: `/auto-plan` is the newer, more universal command that works for any code type (React, API, utilities), while `/plan-migration` is migration-specific with additional migration-focused features.
