# /plan-refactor - Refactoring Plan

## Purpose

Create a structured plan for code improvements and refactoring, ensuring safety through comprehensive testing and incremental changes.

## Usage

```bash
/plan-refactor [refactoring description]
```

## Arguments

- `$ARGUMENTS`: Description of what to refactor and why

---

## Workflow

Create a refactoring plan for: **$ARGUMENTS**

### Phase 1: Analysis

1. **Current State Assessment**
   - Document existing code structure
   - Identify pain points
   - Measure current metrics (complexity, coverage)

2. **Target State Definition**
   - Define desired architecture
   - List improvement goals
   - Set measurable success criteria

3. **Risk Assessment**
   - Identify high-risk areas
   - Check test coverage
   - Plan for backwards compatibility

### Phase 2: Preparation

1. **Test Coverage**
   - Ensure adequate tests exist
   - Add characterization tests if needed
   - Verify tests cover edge cases

2. **Documentation**
   - Document current behavior
   - Note any undocumented assumptions
   - Create before/after diagrams

### Phase 3: Incremental Refactoring

1. **Small, Safe Steps**
   - One change at a time
   - Tests pass after each step
   - Commit frequently

2. **Refactoring Patterns**
   - Extract → Test → Verify
   - Rename → Test → Verify
   - Move → Test → Verify

### Phase 4: Verification

1. **Final Review**
   - Compare to target state
   - Performance comparison
   - Code review

---

## Output Format

```markdown
## 🔄 Refactoring Plan: [Refactoring Name]

**Estimate**: X-Y hours | **Risk**: [Low/Medium/High] | **Test Coverage**: X%

### Motivation

**Why refactor?**
- [Pain point 1]
- [Pain point 2]

**Current problems**:
- [Specific issue]
- Code smell: [smell type]

**Benefits after refactoring**:
- [Improvement 1]
- [Improvement 2]

---

### Current State

**Code Structure**:
```
current/
├── monolith.ts (500 lines) ← Too large
├── utils.ts (mixed concerns)
└── types.ts
```

**Metrics**:
- Cyclomatic complexity: [current]
- Test coverage: [current]%
- Dependencies: [count]

**Pain Points**:
1. [Issue 1]: [description]
2. [Issue 2]: [description]

---

### Target State

**New Structure**:
```
refactored/
├── core/
│   ├── domain.ts
│   └── domain.test.ts
├── services/
│   ├── serviceA.ts
│   └── serviceA.test.ts
├── utils/
│   ├── helpers.ts
│   └── validators.ts
└── types/
    └── index.ts
```

**Target Metrics**:
- Cyclomatic complexity: [target]
- Test coverage: [target]%
- Max file size: [limit] lines

---

### Refactoring Strategy

**Approach**: [Strangler Fig / Branch by Abstraction / Big Bang]

**Key Principles**:
1. Tests must pass after every change
2. No behavior changes (unless explicitly noted)
3. Small, reversible commits
4. Performance must not regress

**Backwards Compatibility**:
- [ ] API contracts maintained
- [ ] Deprecation warnings added for old interfaces
- [ ] Migration path documented

---

### Tasks

#### Phase 1: Preparation [Xh] 🛡️
| # | Task | Size | Est |
|---|------|------|-----|
| 1 | Add missing tests for existing behavior | M | 45m |
| 2 | Create characterization tests | M | 40m |
| 3 | Document current behavior | S | 25m |
| 4 | Set up metrics baseline | S | 20m |

#### Phase 2: Extract [Xh] 📦
| # | Task | Size | Est |
|---|------|------|-----|
| 5 | Extract [module A] | M | 40m |
| 6 | Add tests for extracted module | M | 35m |
| 7 | Extract [module B] | M | 40m |
| 8 | Add tests for extracted module | M | 35m |

#### Phase 3: Restructure [Xh] 🏗️
| # | Task | Size | Est |
|---|------|------|-----|
| 9 | Reorganize folder structure | S | 25m |
| 10 | Update imports and exports | M | 35m |
| 11 | Verify all tests pass | S | 15m |

#### Phase 4: Cleanup [Xh] 🧹
| # | Task | Size | Est |
|---|------|------|-----|
| 12 | Remove dead code | S | 20m |
| 13 | Improve naming | S | 25m |
| 14 | Add/update documentation | M | 35m |
| 15 | Final code review prep | S | 20m |

#### Phase 5: Verification [Xm] ✅
| # | Task | Size | Est |
|---|------|------|-----|
| 16 | Run full test suite | S | 15m |
| 17 | Performance comparison | M | 30m |
| 18 | Update metrics report | S | 15m |

---

### Refactoring Steps (Detailed)

For complex refactorings, detail each step:

**Step 1: Extract UserValidator**
```typescript
// Before: monolith.ts
function processUser(user) {
  // validation logic mixed in
  if (!user.email) throw new Error('Email required');
  if (!user.email.includes('@')) throw new Error('Invalid email');
  // ... more logic
}

// After: validators/userValidator.ts
export function validateUser(user) {
  const errors = [];
  if (!user.email) errors.push('Email required');
  if (!user.email.includes('@')) errors.push('Invalid email');
  return errors;
}

// After: monolith.ts (using extracted function)
import { validateUser } from './validators/userValidator';

function processUser(user) {
  const errors = validateUser(user);
  if (errors.length) throw new ValidationError(errors);
  // ... remaining logic
}
```

---

### Testing Strategy

**Before Refactoring**:
- [ ] All existing tests pass
- [ ] Coverage at [X]%
- [ ] Characterization tests added for untested paths

**During Refactoring**:
- [ ] Tests pass after each commit
- [ ] No tests deleted (only moved)
- [ ] New unit tests for extracted modules

**After Refactoring**:
- [ ] All tests still pass
- [ ] Coverage at [Y]% (same or better)
- [ ] Performance benchmarks pass

---

### Rollback Plan

**If issues discovered**:

1. **During development**: `git revert` to last known good state
2. **After merge**: 
   ```bash
   git revert --no-commit HEAD~[N]..HEAD
   git commit -m "revert: undo [refactoring name] due to [issue]"
   ```
3. **In production**: Feature flag or quick hotfix

---

### Success Criteria

**Functional**:
- [ ] All tests pass
- [ ] No behavior changes (unless intended)
- [ ] No new bugs introduced

**Quality**:
- [ ] Complexity reduced by [X]%
- [ ] Test coverage maintained/improved
- [ ] Code review approved

**Performance**:
- [ ] No regression in response times
- [ ] Memory usage stable
- [ ] Build time not significantly increased

---

### 🚀 Ready to Refactor?

Start with Task #1 to ensure test coverage before making changes.
```

---

## Safe Refactoring Tips

1. **Test first**: Never refactor without tests
2. **Small steps**: One refactoring at a time
3. **Commit often**: Easy to revert if needed
4. **No behavior changes**: Refactoring ≠ feature changes
5. **IDE tools**: Use rename, extract, move tools

---

## Common Refactoring Patterns

| Pattern | When to Use |
|---------|-------------|
| **Extract Function** | Long functions, repeated code |
| **Extract Class** | Class doing too much |
| **Move Function** | Wrong location |
| **Rename** | Unclear naming |
| **Introduce Parameter Object** | Too many parameters |
| **Replace Conditional with Polymorphism** | Complex conditionals |

---

---

## Execution with Subagents

Refactoring plans work excellently with `/execute-plan` and **subagent methodology**.

**Reference**: `.claude/skills/methodology/executing-plans/SKILL.md`

### Refactoring with Subagents

```
Phase 1: Prepare & Test Coverage
  → Subagent adds missing tests
  → Ensures existing behavior captured
  → Returns: Test suite complete
  ↓
Review: Test coverage sufficient?
  ↓
Phase 2: Extract & Refactor
  → Fresh subagent refactors code
  → Keeps all tests passing
  → Improves structure
  → Returns: Refactored code
  ↓
Review: Code quality improved?
  ↓
Phase 3: Cleanup & Optimize
  → Fresh subagent cleans up
  → Removes dead code
  → Optimizes if needed
  ↓
Final Review: All tests still passing?
  ↓
Complete! ✅ Better code, same behavior
```

### Why Subagents for Refactoring?

- ✅ **Safety**: Tests verify behavior preserved
- ✅ **Focus**: Each phase handled by dedicated subagent
- ✅ **Quality gates**: Reviews ensure no regressions
- ✅ **Isolated changes**: Can revert individual phases if needed
- ✅ **Better outcomes**: Multiple review cycles catch issues

### Critical for Refactoring

When using `/execute-plan` for refactors:

1. **Tests MUST pass** after each phase
2. **Behavior MUST NOT change** (unless that's the goal)
3. **Reviews are mandatory** (never skip for refactors)
4. **Commit after each phase** (easy rollback if needed)

### Example

```bash
# Generate refactoring plan
/plan-refactor --save=plans/refactor-auth-service.md "extract auth logic into separate service"

# Execute with safety nets
/execute-plan plans/refactor-auth-service.md
# Each phase: test → refactor → test → review → commit
```

---

## Related Commands

```bash
/plan           # General planning
/plan-feature   # Adding new features
/review         # Code review assistance
```
