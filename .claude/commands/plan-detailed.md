# /plan-detailed - TDD Micro-Tasks Planning

## Purpose

Create highly detailed implementation plans with 2-5 minute micro-tasks following TDD methodology. Perfect for learning, complex tasks, or when you need step-by-step guidance.

## Usage

```bash
/plan-detailed [task description]
```

## Arguments

- `$ARGUMENTS`: Description of the task to plan with detailed TDD steps

## When to Use

- ✅ Learning new technology
- ✅ Complex/unfamiliar problems
- ✅ Pair programming sessions
- ✅ Want TDD discipline
- ✅ Teaching someone
- ✅ Need confidence at each step

---

## Workflow

Create a detailed TDD implementation plan for: **$ARGUMENTS**

### Planning Approach

1. **Bite-sized tasks**: Each task should take 2-5 minutes
2. **Exact file paths**: Always include full paths
3. **Complete code samples**: Actual code, not descriptions
4. **TDD cycle per task**: Write test → verify fail → implement → verify pass → commit
5. **Expected outputs**: Specify what success looks like
6. **Immediate feedback**: Know if you're on track after each micro-task

---

## Output Format

For each task, generate:

```markdown
## 🎯 Plan: [Feature Name] (Detailed TDD Mode)

**Total Tasks**: X | **Total Time**: X-Y minutes | **Approach**: Test-Driven Development

---

## Task [N]: [Task Name] ⏱️ 3-5 min

**Goal**: [One sentence - what this accomplishes]

**Files**:
- Create: `path/to/new-file.ts`
- Modify: `path/to/existing-file.ts` (lines X-Y)
- Test: `path/to/test-file.test.ts`

**Context**: 
[1-2 sentences explaining why this task matters]

---

### Steps (TDD Cycle):

#### 1️⃣ Write Failing Test (60 seconds)
```typescript
// path/to/test-file.test.ts
import { FeatureName } from './feature';

describe('FeatureName', () => {
  it('should do something specific', () => {
    const result = FeatureName.method();
    expect(result).toBe(expectedValue);
  });
});
```

**Expected Output**:
```bash
$ npm test -- feature.test.ts
❌ FAIL  FeatureName
  ✗ should do something specific
  
  Error: method is not defined
  
  1 failing
```

#### 2️⃣ Verify Test Fails (30 seconds)
```bash
npm test -- --grep "should do something specific"
# Expected: ❌ 1 failing (confirms test is working)
```

**✅ Checkpoint**: If test doesn't fail, fix the test first!

#### 3️⃣ Implement Minimally (2 minutes)
```typescript
// path/to/feature.ts
export class FeatureName {
  static method() {
    // Minimal implementation to pass test
    return expectedValue;
  }
}
```

**💡 Pro Tip**: Implement ONLY what makes the test pass. No extras!

#### 4️⃣ Verify Test Passes (30 seconds)
```bash
npm test -- --grep "should do something specific"
# Expected: ✅ 1 passing
```

**Expected Output**:
```bash
$ npm test -- feature.test.ts
✅ PASS  FeatureName
  ✓ should do something specific (2ms)
  
  1 passing
```

**✅ Checkpoint**: Green! Ready to commit.

#### 5️⃣ Commit (30 seconds)
```bash
git add src/feature.ts tests/feature.test.ts
git commit -m "feat(feature): add method implementation

- Implements basic method functionality
- Adds test coverage for expected behavior"
```

**✅ Task Complete!** → Move to Task [N+1]

---

### 🎯 Definition of Done:
- [x] Test written and initially failing
- [x] Implementation makes test pass
- [x] Code committed with descriptive message
- [x] No new warnings or errors
- [x] Ready for next task

**Time Check**: ⏱️ Should take 3-5 minutes total

**Next Task**: #[N+1] - [Next task name]
```

---

## Why Detailed Mode Works

### For Beginners
- Can't get lost - steps are tiny
- Immediate feedback every 3-5 minutes
- Builds muscle memory for TDD
- Clear success criteria at each step

### For Complex Tasks
- Breaks intimidating work into manageable pieces
- Forces you to think through implementation
- Catches mistakes early (fast feedback)
- Easy to pause/resume

### For Teaching/Pairing
- Perfect for mentoring sessions
- Driver/navigator can switch every task
- Clear progress tracking
- Builds confidence incrementally

---

## Example: Password Reset Token

```markdown
## Task 1: Create PasswordResetToken model (5 min) ⏱️

**Files**:
- Create: `src/models/PasswordResetToken.ts`
- Test: `tests/models/PasswordResetToken.test.ts`

### Steps:

#### 1️⃣ Write Failing Test (90 sec)
```typescript
// tests/models/PasswordResetToken.test.ts
import { PasswordResetToken } from '../../src/models/PasswordResetToken';

describe('PasswordResetToken', () => {
  it('should generate 32-character token', () => {
    const token = PasswordResetToken.generate();
    expect(token).toHaveLength(32);
    expect(token).toMatch(/^[a-f0-9]{32}$/);
  });
});
```

#### 2️⃣ Verify Test Fails
```bash
npm test PasswordResetToken.test.ts
# Expected: ❌ Cannot find module 'PasswordResetToken'
```

#### 3️⃣ Implement (2 min)
```typescript
// src/models/PasswordResetToken.ts
import crypto from 'crypto';

export class PasswordResetToken {
  static generate(): string {
    return crypto.randomBytes(16).toString('hex');
  }
}
```

#### 4️⃣ Verify Test Passes
```bash
npm test PasswordResetToken.test.ts
# Expected: ✅ 1 passing
```

#### 5️⃣ Commit
```bash
git add .
git commit -m "feat(auth): add password reset token generation"
```

✅ **Task 1 Complete!** → Next: Task 2
```

---

## Tips for Success

1. **Don't skip the red step**: Seeing the test fail confirms it's testing the right thing
2. **Resist gold-plating**: Implement minimum to pass, refactor later
3. **Commit frequently**: Each green state is a safe checkpoint
4. **Time yourself**: If >5 min, break task down further
5. **Take breaks**: After 4-5 tasks, step away for 5 minutes

---

---

## Execution with Subagents

This command generates plans optimized for `/execute-plan` with **subagent-driven execution**.

**Reference**: `.claude/skills/methodology/executing-plans/SKILL.md`

### Methodology

**"Fresh subagent per task group + code review between groups = high quality, fast iteration"**

When you execute plans from this command with `/execute-plan`:

1. **Task Grouping**
   - Related micro-tasks grouped together (3-5 tasks, 15-30 min)
   - Example: Test + Implement + Enhance + Test + Commit for one component

2. **Fresh Subagent per Group**
   - Dispatch new subagent for each task group
   - Subagent reads plan context
   - Studies referenced files (from Context section)
   - Implements following your strategy (not copying exact code)
   - Returns completion summary

3. **Code Review Between Groups**
   - Separate reviewer subagent dispatched
   - Reviews only current group's changes
   - Finds: Critical, Important, or Minor issues
   - Must fix Critical/Important before proceeding

4. **Quality Gates**
   - No skipping reviews
   - No proceeding with critical issues
   - Sequential execution (no parallel)
   - Fresh context per group prevents pollution

### Execution Flow

```
Your Plan (with context + strategy)
  ↓
Save to file: /plan-detailed --save=plans/feature.md "description"
  ↓
Execute: /execute-plan plans/feature.md
  ↓
┌─────── Task Group 1 (Component A)
│ Subagent reads: Context, Strategy, References
│ Subagent studies: Similar existing code
│ Subagent implements: Adapts pattern (not copies)
│ Subagent tests: Runs tests, commits
│ Returns: Summary
└─────── ✅
  ↓
┌─────── Review Group 1
│ Reviewer checks: Tests, patterns, quality
│ Returns: Issues (if any)
└─────── ✅
  ↓
[Fix if needed]
  ↓
┌─────── Task Group 2 (Component B)
│ Fresh subagent (clean context)
│ ...same process...
└─────── ✅
  ↓
Continue until all groups complete
  ↓
Final comprehensive review
  ↓
Done! 🎉
```

### Benefits

- ✅ **Fresh context**: Each task group starts clean
- ✅ **Focused implementation**: Subagent only thinks about current feature
- ✅ **Quality gates**: Reviews catch issues early
- ✅ **Easy retries**: Can re-run individual groups
- ✅ **Better code**: AI must study and adapt, not copy
- ✅ **Consistent style**: Forces following existing patterns

---

## Related Commands

```bash
/plan              # Standard mode (15-60 min tasks)
/plan-interactive  # AI asks questions first
/execute-plan      # Execute any plan with assistance
/tdd               # Quick TDD cycle helper
```
