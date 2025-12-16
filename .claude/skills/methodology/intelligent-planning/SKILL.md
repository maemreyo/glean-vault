# Intelligent Planning with Auto-Exploration

## Description

Automated planning methodology that ALWAYS explores existing code before generating migration/implementation plans. Uses a 3-phase subagent workflow (Explorer → Analyzer → Planner) with quality gates to ensure complete understanding and context preservation.

## When to Use

- Migrating features from old codebase to new
- Reimplementing existing functionality
- Need to preserve critical business logic
- Want comprehensive understanding before planning
- Complex migrations requiring detailed context

---

## Core Philosophy

**"Can't plan well without understanding existing code"**

This methodology enforces exploration-first planning:
1. **Explore** existing implementation thoroughly
2. **Analyze** requirements and patterns
3. **Plan** with complete context

Never plan based on assumptions or incomplete information.

---

## 3-Phase Subagent Workflow

### Phase 1: Explorer Subagent 🔍

**Goal**: Find and thoroughly document existing implementation

**Duration**: 60-90 minutes (9 subtasks)

**Key Outputs**:
- File inventory with line counts
- Business logic with line number references
- Data models and interfaces
- Technical patterns used
- Dependencies (external + internal)
- Test coverage assessment
- Issues and improvement opportunities

**Critical Success Factor**: Document exact line numbers for business logic

### Phase 2: Analyzer Subagent 📊

**Goal**: Extract requirements and create migration strategy

**Duration**: 60-80 minutes (7 subtasks)

**Key Outputs**:
- Structured requirements (Critical/Important/Nice-to-have)
- Preservation requirements (MUST NOT CHANGE items)
- Technical pattern analysis (KEEP vs IMPROVE)
- Data flow mapping
- Gap analysis
- Migration strategy with risk assessment

**Critical Success Factor**: Identify all MUST PRESERVE items

### Phase 3: Planner Subagent 📋

**Goal**: Generate execution-ready plan with TDD micro-tasks

**Duration**: 80-100 minutes (9 subtasks)

**Key Outputs**:
- 6-phase plan structure
- 40+ micro-tasks (2-5 min each)
- Task context with old code references
- PRESERVE notes on critical tasks
- Preservation checklist
- Execution instructions
- Verification strategy

**Critical Success Factor**: Every task has explicit file paths and context

---

## Subagent Benefits

### 1. Fresh Context Per Phase

```
Explorer completes → Context discarded
  ↓
Analyzer starts fresh
  ↓
  No bias from exploration
  ↓
Focuses on analysis only
```

**Why**: Prevents context pollution, ensures specialized focus

### 2. Quality Gates Between Phases

```
Explorer → Review Gate 1 → Analyzer → Review Gate 2 → Planner → Review Gate 3
```

**Gates Check**:
- Completeness of output
- Quality sufficient to proceed
- No ambiguities or gaps

**Action if fails**: Re-run specific phase, don't proceed

### 3. Independent Retry

```
If Analyzer fails:
  ↓
Re-dispatch Analyzer only
(Explorer results preserved)
  ↓
No need to re-explore
```

**Why**: Efficient error recovery, isolated debugging

### 4. Specialized Attention

Each subagent optimized for its task:
- **Explorer**: Search, read, document
- **Analyzer**: Extract, categorize, strategize
- **Planner**: Structure, detail, verify

**Why**: Better quality than single agent doing all

---

## Preservation Requirements

### Critical Items (MUST PRESERVE)

Always identify and document:

1. **Business Logic**
   - Tax formulas, calculation algorithms
   - Legal/regulatory requirements
   - Expected behaviors that must match

2. **Data Structures**
   - Exact field names and types
   - Validation constraints
   - API contracts

3. **Integration Points**
   - External API endpoints
   - Database schemas
   - Third-party services

### Documentation Format

```markdown
⚠️  MUST PRESERVE:

1. Tax Bracket Values
   - Values: [exact values]
   - Reason: Legal requirement
   - Source: old-app/file.ts (lines 65-73)
   - Verification: Test against old system outputs
   - Impact if wrong: [consequences]

2. Insurance Rates
   - Values: [percentages]
   - Reason: Legal mandate
   - Source: [file:line]
   - Verification: [method]
   - Impact if wrong: [consequences]
```

### Verification Strategy

Every PRESERVE item must have:
- Source code reference (file + line numbers)
- Reason why it can't change
- Verification method (how to test)
- Impact assessment (what breaks if wrong)

---

## Task Format

### Micro-Task Structure

Each task in generated plan:

```markdown
### Task X.Y: [Task Name] (Estimated time)

**File**: `exact/path/to/file.ts`

**Context**:
- Old implementation: old-app/path/file.ts (lines X-Y)
- Related files: [list]
- CRITICAL: [what must be preserved]

**Strategy** (not exact code):
1. Study old [function/component]
2. Understand [pattern/algorithm]
3. Write test cases (use old system outputs)
4. Implement following same [logic/pattern]
5. Verify against old system

**Acceptance Criteria**:
- [ ] [Specific criterion 1]
- [ ] [Specific criterion 2]
- [ ] Tests pass
- [ ] Outputs match old system

**Expected**: ✅/❌ [Expected test result]
```

### Why This Format?

- **File path**: No ambiguity about where to work
- **Context**: References to study, not copy-paste
- **Strategy**: Approach, not exact solution (AI must think)
- **Acceptance**: Clear definition of "done"
- **Expected**: Know what success looks like

---

## Migration Strategy Patterns

### Incremental Replacement

```
Phase 1: Foundation (types, constants)
  ↓ (enables)
Phase 2: Core Logic (business rules) ← HIGH RISK
  ↓ (enables)
Phase 3: Components (UI)
  ↓ (enables)
Phase 4: Integration (wiring)
  ↓ (validates)
Phase 5: Testing (comprehensive)
  ↓ (enhances)
Phase 6: Polish (accessibility, performance)
```

**When**: Large existing implementation
**Why**: Reduce risk, enable testing at each stage

### Parallel Implementation

```
Old System (running)
  ↓
New System (development)
  ↓
Run both in parallel
  ↓
Compare outputs
  ↓
Switch when verified
```

**When**: Critical features, zero-downtime requirement
**Why**: Verify correctness before cutover

### Feature Flag Rollout

```
Implement new version
  ↓
Add feature flag
  ↓
Enable for 1% users
  ↓
Monitor metrics
  ↓
Gradually increase % if stable
```

**When**: User-facing features
**Why**: Gradual rollout, easy rollback

---

## Execution Integration

### With /execute-plan

Generated plans are optimized for `/execute-plan`:

```bash
# 1. Generate plan with auto-exploration
/auto-plan "salary calculator" --output=plans/salary.md

# 2. Execute with subagents
/execute-plan plans/salary.md

# Execution uses:
# - Fresh subagent per task group
# - Code review between groups
# - Quality gates
# - Context from plan (old code references)
```

### Task Grouping

```
Group 1: Foundation Tasks (5 tasks)
  → Subagent executes all 5
  → Review
  → Fix if needed

Group 2: Core Logic Tasks (8 tasks)
  → Fresh subagent
  → Execute all 8
  → Review
  → Fix if needed

[Continue...]
```

**Why group**: Maintain context within feature, fresh context between features

---

## Success Criteria

### Plan Quality Metrics

A good plan has:

✅ **Complete Context**
- All business logic documented with line numbers
- Preservation items clearly marked
- Old code references in every task

✅ **Clear Strategy**
- 6 phases with dependencies
- 40+ micro-tasks (2-5 min each)
- Risk assessment per phase

✅ **Verification Plan**
- How to test against old system
- Expected outputs specified
- Edge cases covered

✅ **Execution Ready**
- Explicit file paths
- No ambiguity
- Ready for /execute-plan

### Migration Success Criteria

✅ **Functional Correctness**
- All outputs match old system (100%)
- All edge cases handled
- No regressions

✅ **Code Quality**
- Test coverage increased
- Technical debt reduced
- Better structure than old code

✅ **Knowledge Preservation**
- Critical business logic documented
- Why decisions were made
- How to verify correctness

---

## Common Pitfalls

### ❌ Planning Without Exploration

```
Problem: Plan based on assumptions
Result: Missing requirements, incomplete plan
Fix: ALWAYS explore first (enforced by /auto-plan)
```

### ❌ Vague Context References

```
Problem: "Check old authentication code"
Result: Executor doesn't know where to look
Fix: "Check old-app/auth/login.ts (lines 45-89)"
```

### ❌ Generic Preservation Notes

```
Problem: "Preserve business logic"
Result: Don't know WHAT to preserve
Fix: "Preserve tax bracket values [exact values] (legal requirement)"
```

### ❌ No Verification Strategy

```
Problem: How to know if migration is correct?
Result: Bugs in production
Fix: Test suite with 20+ scenarios, compare with old system
```

---

## Integration with Other Skills

### Related Skills

- **executing-plans**: Executes generated plans with subagents
- **writing-plans**: Original planning methodology
- **test-driven-development**: TDD approach used in tasks
- **code-review**: Review gates used between phases
- **verification-before-completion**: Final verification strategy

### Skill Dependencies

```
intelligent-planning requires:
  → exploring (find old code)
  → analyzing (extract requirements)
  → planning (structure tasks)
  → preserving (critical logic)
  → verifying (correctness)
```

---

## Examples

### Example 1: Simple Utility Migration

```
Input: /auto-plan "email validation utility"

Explorer (20 min):
- Find: src/utils/email-validator.ts (50 lines)
- Logic: Regex pattern + domain check
- Tests: 8 tests, 85% coverage

Analyzer (15 min):
- REQ-1: Same regex pattern (preserve)
- REQ-2: Add TypeScript strict types (improve)
- Strategy: Rewrite with better tests

Planner (30 min):
- 8 tasks
- Estimate: 45 minutes
- Phases: Types → Logic → Tests → Polish

Output: Execution-ready plan
```

### Example 2: Complex Feature Migration

```
Input: /auto-plan "salary calculator"

Explorer (90 min):
- Find: 12 files, 1200 lines
- Logic: Tax (7 brackets), insurance, allowances
- Critical: Legal requirements, exact formulas

Analyzer (80 min):
- 9 requirements (4 critical)
- 4 MUST PRESERVE items
- Strategy: Incremental, test-heavy

Planner (100 min):
- 42 tasks
- Estimate: 6-8 hours
- Phases: Foundation → Core (critical) → Components → Integration → Tests → Polish

Output: Comprehensive migration plan
```

---

## Best Practices

### 1. Trust the Exploration

Don't skip or rush exploration phase:
- 60-90 minutes is normal
- Thoroughness pays off in planning
- Missing details = incomplete plan

### 2. Mark Everything PRESERVE

When in doubt, preserve:
- Better to preserve and optimize later
- Than break and debug in production
- Can always remove preservation later

### 3. Reference, Don't Copy

Plans should guide, not dictate:
- ✅ "Study old calculateTax, same algorithm"
- ❌ "Copy paste this exact code [500 lines]"

### 4. Test Against Old System

Every critical function:
- Run old system with test inputs
- Record outputs
- New system must match exactly
- 100% match = correct migration

### 5. Document Assumptions

If exploration incomplete:
- Document what's unknown
- Note assumptions made
- Flag for verification during execution

---

## Command Usage

```bash
# Basic usage
/auto-plan "feature to migrate"

# With source path
/auto-plan "authentication" --source=old-app/auth

# Save outputs
/auto-plan "payment" \
  --output=plans/payment.md \
  --analysis=docs/payment-analysis.md

# Then execute
/execute-plan plans/payment.md
```

---

## Summary

**Intelligent Planning** = Explore → Analyze → Plan

**Key Principles**:
1. ALWAYS explore before planning
2. Use fresh subagent per phase
3. Quality gates between phases
4. Preserve critical business logic
5. Verify against old system

**Result**: Complete, context-rich, execution-ready migration plans
