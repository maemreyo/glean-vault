# /optimize-flow (The Architect) 🏗️

## Purpose

Scientific performance tuning and complex refactoring. Moves optimization from "guessing" to "measuring".

**Required Skills**: `performance-optimization`
**References**:
- `.claude/skills/methodology/performance-optimization/SKILL.md`

## Usage

```bash
/optimize-flow "Why is the dashboard slow?" --target=src/components/Dashboard
```

## Workflow

### Phase 1: PROFILE (Explorer Subagent) ⏱️

**Goal**: Gather metrics and find bottlenecks.

#### Subtask 1.1: Static Analysis (10 min)

**Context**: Find obvious performance killers in code.

**Steps**:
1. Scan target files for:
   - Nested loops (O(n^2)).
   - Heavy computations in Render bodies.
   - Large bundle imports.
2. Check for missing memoization (`useMemo`, `useCallback` missing deps).

**Example Output**:
```markdown
Static Profile:
- `Dashboard.tsx`: `heavyCalc()` called on every render (line 45).
- `Grid.tsx`: Maps over 5000 items without virtualization.
```

#### Subtask 1.2: Metric Collection (Optional) (5-10 min)

1. If logs/profile provided: Analyze flame graphs.
2. If not: Estimate "Hot Paths" based on code structure.

---

### Phase 2: SIMULATE (Analyzer Subagent) 🧪

**Goal**: Hypothesis testing without coding.

#### Subtask 2.1: Intervention Proposals (15-20 min)

**Guidance**: Use `performance-optimization` skill.

**Steps**:
1. Propose 3 Optimizations:
   - **Low Hanging Fruit**: Add `useMemo`.
   - **Structural**: Virtualize list, Pagination.
   - **Architectural**: Move to Web Worker, Server-Side Filtering.
2. **Simulate Impact**: "If we memoize X, we avoid Y re-renders."

**Example Output**:
```markdown
Simulation:
1. Memoize `heavyCalc` -> Saves ~200ms per keystroke. (Cost: Low)
2. Virtualize Grid -> Saves ~800ms initial load. (Cost: Medium)
```

#### Subtask 2.2: Trade-off Analysis (5 min)

**Steps**:
1. Compare Complexity vs Benefit.
2. Recommend the best ROI option.

> **REVIEW GATE**: Is the proposed optimization worth the added complexity?

---

### Phase 3: RESTRUCTURE (Planner Subagent) 📐

**Goal**: Safe implementation plan.

#### Subtask 3.1: Refactoring Plan (15 min)

**Context**: Optimization often requires changing structure.

**Steps**:
1. Plan "Extraction": Move logic out of components to pure functions (easier to test/optimize).
2. Plan "Integration": Where to inject the cache/worker.

#### Subtask 3.2: Regression Risk Assessment (5 min)

**Steps**:
1. What logic could break?
2. Plan tests to ensure correctness (Baseline Test).

---

### Phase 4: OPTIMIZE (Executor Subagent) ⚡

**Goal**: Apply and Verify.

#### Subtask 4.1: Baseline Verification (10 min)
- **Action**: Run existing tests to ensure they pass BEFORE starting.
- **Action**: (Optional) Measure current execution time if possible.

#### Subtask 4.2: Implementation (20-30 min)
- **Action**: Apply the Refactoring Plan.
- **Action**: Implement the Optimization.

#### Subtask 4.3: Verification (10 min)
- **Action**: Verify correctness (Tests must pass).
- **Action**: Verify perf gain (Describe why it's faster).

## Success Criteria

- [ ] Optimization implemented.
- [ ] No logical regressions (tests pass).
- [ ] Code is still readable (comments added explaining *why* optimization exists).
