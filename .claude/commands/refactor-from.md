# /refactor-from - Refactor Based on Exploration Insights

## Purpose

Refactor code based on insights, tech debt, and improvement opportunities identified during `/how` exploration. Uses documentation to guide safe, incremental refactoring while preserving functionality.

**"Improve with confidence"** - Refactor using documented insights, not assumptions.

## Aliases

```bash
/refactor-from [feature]
/refactor [feature] --from-docs
```

## Usage

```bash
# Refactor based on exploration insights
/refactor-from "calculator" --improve="error-handling"

# Extract business logic
/refactor-from "auth" --goal="Extract to utils"

# Preview refactoring plan
/refactor-from "payment" --preview
```

## Arguments

- `feature`: Feature name (will look for docs in `docs/<feature>/`)

## Flags

| Flag | Description | Example |
|------|-------------|---------|
| `--from=path` | Explicit docs folder | `--from=docs/calc/` |
| `--improve=area` | Specific area to improve | `--improve="validation"` |
| `--goal=desc` | Refactoring goal | `--goal="Reduce duplication"` |
| `--preview` | Preview plan only | `--preview` |

---

## Integration with /how

Leverages insights from exploration:

```bash
# Step 1: Explore and identify issues
/how "calculator"
→ docs/calculator/phase-2-analysis.md shows:
  - ⚠️ Files > 200 lines (should split)
  - ⚠️ Duplicated validation logic
  - ⚠️ TODO: Extract to utils
  - 💡 Could use custom hooks

# Step 2: Refactor based on insights
/refactor-from "calculator" --improve="extract-utils"
→ Extracts business logic to utils/
→ Reduces duplication
→ All tests still passing ✅
→ Updates docs/calculator/README.md with refactoring history
```

---

## Workflow

Refactoring: **$FEATURE**

{{ if --from provided }}
**Source docs**: `$FROM_PATH`
{{ else }}
**Source docs**: `docs/$FEATURE/`
{{ endif }}

{{ if --improve provided }}
**Focus**: `$IMPROVE`
{{ else if --goal provided }}
**Goal**: `$GOAL`
{{ else }}
**Focus**: All identified issues
{{ endif }}

---

### Phase 1: Load Insights 📖

**Goal**: Identify refactoring opportunities from docs

**Duration**: 5-10 minutes

---

**Steps**:

1. **Read exploration docs**
   ```bash
   DOCS_PATH="docs/$FEATURE/"
   ```

2. **Extract from phase-2-analysis.md**:
   - Technical debt notes
   - TODO/FIXME comments
   - Areas for improvement
   - Code smells identified
   - Patterns that could be improved
   - Key insights

3. **Extract from phase-1-discovery-structure.md**:
   - Large files to split
   - Coupling issues
   - Dependency problems
   - File locations

**Output**:
```markdown
Refactoring Opportunities:

Technical Debt:
- ⚠️ CheckoutForm.tsx (280 lines - should split)
- ⚠️ Duplicated validation in 3 files
- ⚠️ Mixed concerns in pricing.ts

TODOs/FIXMEs:
- TODO pricing.ts:67 - Extract bundle logic
- FIXME inventory.ts:25 - Race condition

Improvements:
- 💡 Extract price calculation to utils
- 💡 Create useCheckout custom hook
- 💡 Consolidate error handling
```

---

### Phase 2: Plan Refactoring 📋

**Goal**: Create safe refactoring plan

**Duration**: 15-20 minutes

---

**Dispatch Refactoring Planner SubAgent**:

```markdown
Refactoring Planner SubAgent

GOAL: Create safe refactoring plan for "$FEATURE"

INPUT:
- Refactoring opportunities: [from Phase 1]
- Current code structure: [from exploration docs]
{{ if --improve or --goal }}
- Specific focus: "$IMPROVE" or "$GOAL"
{{ endif }}

CONSTRAINTS:
- MUST preserve all functionality
- MUST keep all existing tests passing
- MUST make incremental changes
- MUST verify after each step

---

SUBTASK 2.1: Prioritize Improvements (5 min)

**Steps**:
1. List all refactoring candidates
2. Prioritize by:
   - Safety (low risk first)
   - Impact (high value first)
   - Dependencies (least dependent first)

3. {{ if --improve or --goal }}
   Filter to focus area: "$IMPROVE"
   {{ else }}
   Select top 3-5 improvements
   {{ endif }}

**Output**: Prioritized refactoring list

---

SUBTASK 2.2: Design Refactoring Strategy (10 min)

**For each refactoring**:

1. **What**: Describe the change
2. **Why**: Benefit from docs
3. **How**: Step-by-step approach
4. **Safety**: Preservation strategy

**Example** (Extract pricing utils):
```
What: Extract price calculation to utils/pricing.ts
Why: Duplicated in 3 components (noted in docs)
How:
  1. Create utils/pricing.ts
  2. Move calculatePrice function
  3. Update imports in components
  4. Run tests → verify passing
  5. Remove old implementations
  6. Run tests again
Safety: Tests exist for all 3 usages
```

**Output**: Detailed refactoring strategy

---

SUBTASK 2.3: Create Incremental Plan (10 min)

**Break into small, safe steps**:
- Each step testable
- Each step reversible
- Dependencies ordered correctly

**Output**: Step-by-step refactoring plan

---

OUTPUT: Return complete refactoring plan

```markdown
📋 REFACTORING PLAN

Feature: $FEATURE
Focus: {{ --improve or "General improvements" }}

---

## Improvements Selected

### Priority 1: Extract Price Calculation (Low Risk, High Impact)
**Issue**: Duplicated logic in 3 files
**Goal**: Single source of truth
**Estimated**: 30 min

### Priority 2: Split Large Component (Medium Risk, Medium Impact)
**Issue**: CheckoutForm.tsx (280 lines)
**Goal**: Split into smaller components
**Estimated**: 1 hour

### Priority 3: Consolidate Error Handling (Low Risk, Medium Impact)
**Issue**: Inconsistent error patterns
**Goal**: Unified error handling
**Estimated**: 45 min

---

## Detailed Plan: Extract Price Calculation

### Step 1: Create Utility Module (5 min)
- Create utils/pricing.ts
- Add TypeScript types
- Export calculatePrice function
- No logic changes yet

**Test**: File compiles

---

### Step 2: Move calculatePrice (10 min)
- Copy function from Component A
- Adjust imports
- Add unit tests
- Verify tests pass

**Test**: Unit tests for utility

---

### Step 3: Update Component A (5 min)
- Import from utils/pricing
- Replace local function
- Remove old code
- Run component tests

**Test**: Component A tests pass

---

### Step 4: Update Component B (5 min)
- Same as Step 3 for Component B

**Test**: Component B tests pass

---

### Step 5: Update Component C (5 min)
- Same as Step 3 for Component C

**Test**: Component C tests pass

---

### Step 6: Final Verification (5 min)
- Run full test suite
- Check for unused imports
- Verify no regressions

**Test**: All tests pass

---

## Safety Checklist

⚠️ **BEFORE each step**:
- [ ] All tests passing
- [ ] No uncommitted changes
- [ ] Create checkpoint (git commit)

⚠️ **AFTER each step**:
- [ ] Run affected tests
- [ ] Verify no errors
- [ ] Commit if passing

⚠️ **IF tests fail**:
- [ ] Analyze failure
- [ ] Fix or rollback
- [ ] Never proceed with failing tests

---

REFACTORING PLAN COMPLETE ✅
```
```

**Return**: Refactoring plan

---

{{ if --preview }}

### Phase 3: Preview Plan 👁️

**Display plan to user**

```markdown
📋 REFACTORING PLAN PREVIEW

Feature: $FEATURE

---

## Changes Planned

1. Extract Price Calculation (~30 min)
   - Create utils/pricing.ts
   - Update 3 components
   - Benefit: DRY, easier to test

2. Split CheckoutForm (~1 hour)
   - Split into 4 smaller components
   - Benefit: Better maintainability

3. Consolidate Error Handling (~45 min)
   - Create unified error handler
   - Update 8 call sites
   - Benefit: Consistency

---

Total time: ~2.5 hours
Risk level: Low (all have tests)

To execute: /refactor-from "$FEATURE"
```

**END** (no execution)

{{ else }}

### Phase 3: Execute Refactoring 🔧

**Goal**: Apply refactoring incrementally

**Duration**: Based on plan (2-3 hours for typical refactoring)

---

**Execute plan step-by-step**:

```markdown
For each refactoring in plan:
  For each step in refactoring:
    1. Create checkpoint (git commit)
    2. Apply change
    3. Run tests
    4. IF tests pass:
         Commit change
         Proceed to next step
       ELSE:
         Rollback
         Analyze failure
         Fix or skip step
```

**Example execution** (Extract pricing utils):

```typescript
// Step 1: Create utils/pricing.ts
export interface PriceCalculation {
  subtotal: number;
  tax: number;
  total: number;
}

export function calculatePrice(
  items: Item[],
  region: string
): PriceCalculation {
  // Moved from CheckoutForm.tsx:145-167
  const subtotal = items.reduce((sum, item) => 
    sum + item.price * item.quantity, 0
  );
  
  const tax = subtotal * TAX_RATES[region];
  const total = subtotal + tax;
  
  return { subtotal, tax, total };
}
```

```typescript
// Step 2: Update CheckoutForm.tsx
import { calculatePrice } from '@/utils/pricing';

function CheckoutForm() {
  // Before (lines 145-167):
  // const subtotal = items.reduce(...);
  // const tax = subtotal * TAX_RATES[region];
  // ...
  
  // After (line 145):
  const { subtotal, tax, total } = calculatePrice(items, region);
  
  // ... rest of component
}
```

**Run tests after each step**:
```bash
npm test CheckoutForm.test.tsx
# ✅ All passing → Proceed

npm test ProductPage.test.tsx
# ✅ All passing → Proceed

npm test
# ✅ All passing → Refactoring complete
```

**Output**:
```markdown
✅ REFACTORING COMPLETE

Step 1: Create utility ✅ (5 min)
Step 2: Move function ✅ (10 min)
Step 3: Update Component A ✅ (5 min)
Step 4: Update Component B ✅ (5 min)
Step 5: Update Component C ✅ (5 min)
Step 6: Verification ✅ (5 min)

Total: 35 min
Tests: ✅ All passing
Regressions: None

Files changed:
+ utils/pricing.ts (new)
M CheckoutForm.tsx (-20 lines)
M ProductPage.tsx (-22 lines)
M OrderSummary.tsx (-18 lines)

Net: -25 lines of duplication
```

{{ endif }}

---

### Phase 4: Verify & Document 📝

**Goal**: Ensure refactoring succeeded

**Duration**: 10 minutes

---

**Steps**:

1. **Run full test suite**
   ```bash
   npm test
   pytest
   ```
   Expected: ✅ All passing

2. **Run linter**
   ```bash
   npm run lint
   ```
   Expected: ✅ No new issues

3. **Check for regressions**
   - Manual testing of affected features
   - Verify functionality unchanged

4. **Update documentation**
   - Update exploration docs (or re-run /how)
   - Note what was refactored
   - Document new structure

**Output**:
```markdown
✅ VERIFICATION COMPLETE

Tests: ✅ All passing (125/125)
Linting: ✅ No errors
Manual testing: ✅ Functionality preserved
Documentation: ✅ Updated

Refactoring successful!
```

4. **Update documentation**
   ```bash
   # Append to docs/$FEATURE/README.md
   ```

5. **Add refactoring history**:
   ```markdown
   ## Refactorings
   
   This feature has been refactored with the following improvements:
   
   ### {{ improvement name }} (refactored on [date])
   - **Refactored by**: `/refactor-from` command
   - **Focus**: {{ --improve or --goal }}
   - **Files modified**: {{ count }} files
   - **Lines removed**: {{ count }} (duplication)
   - **Lines added**: {{ count }}
   - **Status**: ✅ Complete
   
   **Changes made**:
   - {{ list refactorings }}
   
   **Benefits**:
   - {{ list improvements }}
   
   **Tests**: ✅ All passing
   ```

**Output**: Documentation updated ✅

---

## Final Completion

```markdown
✅ REFACTORING COMPLETE

Feature: $FEATURE
Documentation: ✅ Updated in docs/$FEATURE/README.md

Refactoring successful and tracked!
```

---

## Completion

```markdown
✅ REFACTORING COMPLETE

Feature: $FEATURE
{{ if --improve }}
Focus: $IMPROVE
{{ endif }}

---

## Changes Made

Refactorings Applied: 3
Files Modified: 8
Lines Removed: 95 (duplication)
Lines Added: 45 (new utils)
Net: -50 lines

---

## Improvements

✅ Extracted price calculation to utils
✅ Split large component (280 → 4×70 lines)
✅ Consolidated error handling

---

## Verification

✅ All tests passing
✅ No regressions
✅ Linting clean
✅ Documentation updated

---

## Next Steps

1. **Review changes**
   ```bash
   git diff
   ```

2. **Commit refactoring**
   ```bash
   git add .
   git commit -m "refactor: improve $FEATURE based on exploration"
   ```

3. **Deploy** (if ready)

---

🎉 Code successfully refactored!
```

---

## Success Criteria

- [ ] Insights loaded from docs
- [ ] Refactoring plan created
- [ ] Changes applied incrementally
- [ ] All tests passing (before & after)
- [ ] No regressions introduced
- [ ] Code quality improved
- [ ] Documentation updated

---

## Examples

### Example 1: Extract Business Logic

```bash
/refactor-from "calculator" --improve="extract-utils"
```

**Output**:
```
Loading insights from docs/calculator/...

Issues found:
- Calculation logic duplicated in 4 components
- Validation mixed with UI logic

Refactoring plan:
1. Create utils/calculations.ts
2. Create utils/validation.ts
3. Update 4 components

Executing...

✅ Refactoring complete
Lines removed: 120 (duplication)
Tests: All passing
```

### Example 2: Split Large File

```bash
/refactor-from "checkout" --goal="Split CheckoutForm"
```

**Output**:
```
CheckoutForm.tsx: 280 lines (too large)

Splitting into:
- CheckoutHeader.tsx (40 lines)
- CheckoutItems.tsx (80 lines)
- CheckoutPayment.tsx (90 lines)
- CheckoutSummary.tsx (70 lines)

✅ Split complete
Tests: All passing
Maintainability: Improved
```

### Example 3: Consolidate Patterns

```bash
/refactor-from "auth" --improve="error-handling"
```

**Output**:
```
Inconsistent error handling found in 8 files

Creating unified error handler...
Updating 8 call sites...

✅ Error handling consolidated
Consistency: 100%
Tests: All passing
```

---

## Related Commands

- `/how [feature]` - Explore code (prerequisite)
- `/plan-refactor [feature]` - Alternative refactoring planner
- `/test-from [feature]` - Add tests before refactoring

---

## Pro Tips

1. **Explore first**:
   ```bash
   /how "feature" --comprehensive
   # Gets detailed refactoring opportunities
   ```

2. **Add tests before refactoring**:
   ```bash
   /test-from "feature" --coverage=85
   /refactor-from "feature"
   # Tests catch regressions
   ```

3. **Start small**:
   - Focus on one improvement at a time
   - Low-risk changes first
   - Build confidence

4. **Commit frequently**:
   - Each successful step = commit
   - Easy to rollback if needed
   - Clear change history

5. **Verify after every change**:
   - Run tests immediately
   - Don't batch changes
   - Catch issues early

---

## Common Refactoring Patterns

### Extract Utilities
```bash
/refactor-from "feature" --improve="extract-utils"
# → Moves logic from components to utils/
```

### Split Large Files
```bash
/refactor-from "feature" --goal="Split large components"
# → Breaks big files into smaller ones
```

### Reduce Duplication
```bash
/refactor-from "feature" --improve="DRY"
# → Consolidates duplicated code
```

### Improve Structure
```bash
/refactor-from "feature" --improve="separation-of-concerns"
# → Separates logic from UI
```

---

**Remember**: Refactoring should preserve behavior. Always have tests, always verify, never skip verification!
