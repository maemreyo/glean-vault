# Performance Optimization

## Description

A scientific approach to performance tuning that prioritizes profiling and simulation over guessing. Prevents "optimization for optimization's sake".

## When to Use

- Specific performance complaints ("The page loads slowly")
- High resource consumption (CPU/Memory spikes)
- Database bottlenecks
- Complex calculation refactoring

## The Process

### Phase 1: Profile (Measure)

**Goal**: Identify the *actual* bottleneck with data.

**Techniques**:
- **Browser**: Network tab, Performance tab, React DevTools Profiler.
- **Backend**: Slow query logs, endpoint response times.
- **Code**: Complexity analysis (Big O notation).

**Rule**: "If you can't measure it, you can't optimize it."

### Phase 2: Simulate (Hypothesize)

**Goal**: Predict the impact of changes before coding.

**Strategy**:
- Propose specific interventions (e.g., "Add Redis cache", "Virtualize list").
- Estimate "Theoretical Max Improvement" (e.g., "Caching eliminates DB call -> saves 200ms").
- Assess Trade-offs (Complexity vs Speed).

### Phase 3: Restructure (Prepare)

**Goal**: Refactor code to make it optimizable without breaking logic.

- Extract heavy computations into pure functions.
- Decouple view from logic.
- Add regression tests (Critical!).

### Phase 4: Optimize (Execute)

**Goal**: Apply the fix.

- Implement the chosen strategy.
- Verify using the same metrics from Phase 1.

## Output Format (for Analyzer Subagent)

```markdown
# Optimization Plan: [Target]

## 1. Profile Results
- **Bottleneck**: `calculateTax` function re-runs on every render.
- **Metric**: 500ms blocking time.

## 2. Simulation
- **Option A**: Use `useMemo`.
  - **Impact**: 500ms -> 0ms (on re-render).
  - **Cost**: Low code change.
- **Option B**: Move to Web Worker.
  - **Impact**: UI non-blocking.
  - **Cost**: High complexity.

## 3. Recommendation
- Implement Option A first.
```
