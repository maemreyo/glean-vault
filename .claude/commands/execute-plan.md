# /execute-plan - Subagent-Driven Plan Execution

## Purpose

Execute a detailed implementation plan using fresh subagents per task with mandatory code review gates between tasks.

## Usage

```
/execute-plan [plan-file-path]
```

## Arguments

- `$ARGUMENTS`: Path to the plan file (created with `/plan --detailed`)

---

Execute plan from: **$ARGUMENTS**

## Methodology

**Reference**: `.claude/skills/methodology/executing-plans/SKILL.md`

This command uses the superpowers execution methodology for quality-gated implementation.

## Core Pattern

**"Fresh subagent per task + review between tasks = high quality, fast iteration"**

### Why Fresh Subagents?

- **Prevents context pollution**: Each task starts with clean slate
- **Focused attention**: Subagent only thinks about current task
- **Failures don't cascade**: One task's issues won't affect others
- **Easier to retry**: Can re-run individual tasks independently
- **Parallel mental models**: Can work on tasks conceptually in parallel

### Why Code Review Between Tasks?

- **Catches issues early**: Review right after implementation
- **Ensures code matches intent**: Verify against acceptance criteria
- **Prevents technical debt**: Fix issues before moving on
- **Creates natural checkpoints**: Safe points to pause/resume
- **Learning opportunity**: AI learns from review feedback

### Updated for TDD Micro-Tasks

With new TDD micro-task format from `/plan-react`:
- Subagent per **logical group** (e.g., one component = 5 micro-tasks)
- Review after **complete feature** (not every 2-min micro-task)
- Smarter task grouping based on file paths and dependencies

## Methodology

**Reference**: `.claude/skills/methodology/executing-plans/SKILL.md`

This command uses the superpowers execution methodology for quality-gated implementation.

## Core Pattern

**"Fresh subagent per task + review between tasks = high quality, fast iteration"**

### Why Fresh Agents?

- Prevents context pollution between tasks
- Each task gets focused attention
- Failures don't cascade
- Easier to retry individual tasks

### Why Code Review Between Tasks?

- Catches issues early
- Ensures code matches intent
- Prevents technical debt accumulation
- Creates natural checkpoints

## Workflow

### Step 1: Load & Parse Plan

1. **Read the plan file**
2. **Verify plan structure**:
   - Has clear task sections
   - Tasks have explicit file paths
   - Acceptance criteria present
   - Expected results defined
3. **Parse task list**:
   - Extract all tasks (support both table and ## Task X.Y formats)
   - Identify TDD micro-task cycles (Test → Implement → Enhance → Test → Commit)
   - Group related tasks (e.g., all tasks for one component)
4. **Create TodoWrite** with all parsed tasks
5. **Set first task to `in_progress`**

---

### Step 2: Detect Task Type

For each task, identify type:

| Pattern | Type | Execution Strategy |
|---------|------|-------------------|
| "Write Test", "Test -" | Test Task | Write test code, run, expect fail |
| "Implement", "Minimal" | Implementation | Write minimal code to pass test |
| "Enhance", "Refactor" | Enhancement | Improve code, keep tests passing |
| "Additional Tests" | Test Addition | Add more test cases |
| "Commit" | Commit | Git add + commit |
| "Create Types", "Data" | Foundation | No test needed, just implement |

---

### Step 3: Execute Task Group (Using Fresh Subagent)

**Task Grouping Strategy**:
- Group related micro-tasks (e.g., Test + Implement + Enhance for one component)
- Typical group: 3-5 micro-tasks, 15-30 minutes total
- Group by: Same component, same file, or logical feature unit

**For Each Task Group**:

```markdown
1. **Identify task group** (e.g., Tasks 2.1-2.5: Build LoginForm)
   
2. **Dispatch fresh implementation subagent** with:
   - All tasks in group (2.1, 2.2, 2.3, 2.4, 2.5)
   - Plan context for this group
   - References to similar components
   - Acceptance criteria
   
3. **Subagent executes TDD cycle for group**:
   
   For "Write Test" task:
   - Read plan's **Context** section (existing patterns to reference)
   - Study referenced files (e.g., RegisterForm.test.tsx)
   - Write test following existing pattern
   - Run test → expect ❌ fail
   - Report: Test created and failing as expected
   
   For "Implementation" task:
   - Read plan's **Implementation Strategy**
   - Study referenced components (e.g., RegisterForm.tsx)
   - Adapt pattern to current component
   - Write code (guided by plan, not copied)
   - Run test → expect ✅ pass
   - Report: Implementation complete, tests passing
   
   For "Enhancement" task:
   - Read current implementation
   - Apply enhancements from plan
   - Keep tests passing
   - Report: Enhanced, tests still passing
   
   For "Additional Tests" task:
   - Add edge case tests
   - Add interaction tests
   - Report: Additional coverage added
   
   For "Commit" task:
   - Stage files
   - Commit with message from plan
   - Report: Changes committed
   
4. **Subagent returns completion summary**:
   ```
   Task Group 2.1-2.5: LoginForm Component - COMPLETE
   
   Files created:
   - src/features/auth/components/LoginForm.tsx
   - src/features/auth/components/__tests__/LoginForm.test.tsx
   
   Tests: 5 passing
   Commits: 1 ("feat(auth): add LoginForm component")
   
   Notes: 
   - Followed RegisterForm pattern as specified
   - Used same validation approach
   - Matched existing error display style
   ```
```

**Key Difference from Old Approach**:
- **Old**: One subagent per task (inefficient for 2-min tasks)
- **New**: One subagent per task **group** (efficient, maintains context within feature)

---

### Step 4: Code Review (After Task Group)

**After each task group completes**:

```markdown
1. **Dispatch code-reviewer subagent**
   
2. **Review scope**: Only changes from current task group
   - Files: LoginForm.tsx and LoginForm.test.tsx
   - Commits: Last commit only
   
3. **Reviewer checks**:
   - ✅ Tests actually test the right behavior
   - ✅ Implementation follows plan's strategy (not copy-paste)
   - ✅ Code matches existing patterns (referenced files)
   - ✅ Acceptance criteria all met
   - ✅ TypeScript types correct
   - ✅ Accessibility present (if UI component)
   - ✅ No obvious bugs or edge cases missed
   - ✅ Consistent style with project
   
4. **Reviewer returns findings**:
   - 🔴 **Critical**: Must fix before proceeding
     Example: "LoginForm doesn't validate email format"
   
   - 🟡 **Important**: Should fix before proceeding
     Example: "Missing accessibility labels on inputs"
   
   - 🟢 **Minor**: Can fix later (note for cleanup)
     Example: "Variable could be renamed for clarity"
```

---

### Step 5: Handle Review Findings

```markdown
IF Critical or Important issues found:
  
  1. **List all issues** to user
     ```
     Review found 2 issues in LoginForm:
     - Critical: Email validation missing
     - Important: Missing ARIA labels
     ```
  
  2. **Dispatch fix subagent** for each issue
     - Subagent reads review feedback
     - Applies fixes
     - Re-runs tests
     - Returns: Fixed
  
  3. **Re-request code review**
     - Same reviewer checks fixes
     - Verifies issues resolved
  
  4. **Repeat until clean**
     - Max 2 fix cycles
     - If still issues: Pause, ask user
  
  5. **Update task group status**: ✅ Complete (after fixes)

IF only Minor issues:
  
  1. **Note for later cleanup**
     - Add to deferred items list
     - Don't block progress
  
  2. **Update task group status**: ✅ Complete
  
  3. **Proceed to next group**

IF no issues (review passed):
  
  1. **Update task group status**: ✅ Complete
  2. **Proceed to next group**
```

---

### Step 6: Progress Tracking & Reporting

Track at two levels:

**Micro-task level** (for detail):
```markdown
### Phase 2: Presentational Components [IN PROGRESS]

Task Group 2.1-2.5: LoginForm ✅ COMPLETE (18min)
├─ Task 2.1: Write Test ✅ (3min)
├─ Task 2.2: Implement ✅ (5min)
├─ Task 2.3: Enhance ✅ (5min)
├─ Task 2.4: Add Tests ✅ (3min)
└─ Task 2.5: Commit ✅ (1min)
Review: ✅ Passed (1 minor deferred)

Task Group 2.6-2.10: Button Component ▶️ IN PROGRESS
├─ Task 2.6: Write Test ✅ (2min)
├─ Task 2.7: Implement ▶️ CURRENT
└─ Tasks 2.8-2.10: Pending
```

**Phase level** (for overview):
```markdown
## Execution Progress

✅ Phase 1: Foundation (4 task groups, 45min) - COMPLETE
🔄 Phase 2: Components (8 task groups, 2h est) - 25% (2/8 groups)
⏳ Phase 3: Integration (3 task groups, 40min est) - PENDING
⏳ Phase 4: Polish (2 task groups, 30min est) - PENDING

Overall: 6/17 task groups (35%) | 1h 23min elapsed / 4h est
Tests: 24 passing, 0 failing
Commits: 6
```

---

### Step 7: Final Review & Completion

After all task groups complete:

```markdown
1. **Dispatch comprehensive review subagent**
   - Reviews entire implementation
   - Checks all files together
   - Verifies integration
   - Tests cross-component interactions

2. **Verify all success criteria from plan**
   - Functional requirements ✅
   - Quality requirements ✅  
   - Performance requirements ✅

3. **Run full test suite**
   ```bash
   npm test -- --coverage
   ```
   - All tests passing ✅
   - Coverage meets target ✅

4. **Generate completion summary**

5. **Suggest next steps**:
   - Run linter: `npm run lint`
   - Manual testing checklist
   - Use `/ship` to create PR
   - Deploy to staging environment
```

---

## Critical Rules

### Never Skip Code Reviews

Every task **group** must be reviewed before proceeding. No exceptions.

**Why**: One bad component can break entire feature

### Never Proceed with Critical Issues

Critical issues MUST be fixed:
```
implement → review → [if critical] → fix → re-review → proceed
```

**Loop max 2 times**, then pause for user

### Tasks Run Sequentially (Groups Can Be Conceptual)

```
WRONG: Run TaskGroup 1, 2, 3 simultaneously
RIGHT: TaskGroup 1 → Review → TaskGroup 2 → Review → TaskGroup 3 → Review
```

**Exception**: Independent groups (different features) could run parallel mentally, but execute sequentially

### Always Read Plan Before Implementing

For each task group:
```
WRONG: Remember plan from context, start coding
RIGHT: Read plan section, extract details, check references, then implement
```

**Subagent must**:
- Read **Context** section (what to reference)
- Read **Implementation Strategy** (how to approach)
- Check referenced files (study existing patterns)
- Then implement (adapt, not copy)

#### For "Write Test" Tasks

```markdown
1. Parse task for:
   - File path (from **File**: marker)
   - Test code (from **Test**: code block)
   - Expected result (from **Expected**: marker)

2. Create test file at specified path

3. Write test code from plan

4. Run test:
   ```bash
   npm test [test-file-path]
   ```

5. Verify test fails (as expected):
   - If fails as expected: ✅ Mark task complete
   - If passes unexpectedly: ⚠️ Warning, proceed
   - If error: Report error to user

6. Report:
   ```
  

 ✅ Task X.Y Complete: Test created and failing as expected
   File: src/components/Button.test.tsx
   ```
```

#### For "Implementation" Tasks

```markdown
1. Parse task for:
   - File path
   - Implementation code (from **Implementation**: block)
   - Acceptance Criteria checkboxes
   - Related test file

2. Create implementation file

3. Write code from plan (or improved version)

4. Run related test:
   ```bash
   npm test [related-test-file]
   ```

5. Verify test passes:
   - If passes: ✅ Mark complete
   - If fails: Attempt fix (max 2 retries)
   - If still fails: Pause, report to user

6. Report:
   ```
   ✅ Task X.Y Complete: Component implemented, tests passing
   File: src/components/Button.tsx
   Tests: ✅ All passing (3/3)
   ```
```

#### For "Enhancement" Tasks

```markdown
1. Read current implementation

2. Apply enhancements from plan:
   - Add structure, styling
   - Add accessibility
   - Add TypeScript types
   - Keep tests passing

3. Run all related tests

4. Verify no regressions:
   - If all pass: ✅ Complete
   - If some fail: Revert, try again
   - If persistent: Pause, report

5. Report:
   ```
   ✅ Task X.Y Complete: Component enhanced
   Changes: Added a11y, styling, types
   Tests: ✅ All passing (5/5)
   ```
```

#### For "Commit" Tasks

```markdown
1. Parse commit message from plan

2. Stage files:
   ```bash
   git add [files-from-plan]
   ```

3. Commit:
   ```bash
   git commit -m "[message-from-plan]"
   ```

4. Verify:
   - Clean working tree: ✅ Complete
   - Uncommitted changes: ⚠️ Warning

5. Report:
   ```
   ✅ Task X.Y Complete: Changes committed
   Files: 2 files committed
   Message: "feat(auth): add LoginForm component"
   ```
```

---

### Step 4: Code Review (Configurable)

**After each logical group** (e.g., all micro-tasks for one component):

```markdown
IF --review flag enabled:

  1. Dispatch code-reviewer subagent
  
  2. Review scope: Changes from recent tasks
  
  3. Reviewer checks:
     - Tests actually test the right things
     - Implementation follows plan
     - Accessibility present
     - TypeScript types correct
     - No obvious bugs
  
  4. Reviewer returns findings:
     - ✅ Looks good: Proceed
     - ⚠️ Minor issues: Note for later
     - 🔴 Critical issues: Pause, fix now

ELSE:
  Skip review, proceed to next task
```

**Note**: For TDD micro-tasks, review every 3-5 tasks (one complete component) instead of every task.

---

### Step 5: Handle Failures

#### Test Fails Unexpectedly

```markdown
1. Capture error output

2. Analyze failure:
   - Syntax error → Fix automatically
   - Logic error → Attempt fix
   - Environment issue → Report to user

3. Retry (max 2 attempts):
   - Attempt 1: Fix obvious issues
   - Attempt 2: Try alternative approach
   - Still failing: Pause execution

4. Report to user:
   ```
   ⚠️ Task X.Y Failed: Test not passing
   Error: Expected 'value' but got 'undefined'
   File: src/components/Button.test.tsx:15
   
   Attempted fixes: 2
   Suggestions:
   - Check if props are passed correctly
   - Verify component exports
   
   Options:
   1. Skip this task
   2. Manual fix (pause execution)
   3. Modify plan
   ```
```

#### File Path Issues

```markdown
1. If file path not found in plan:
   - Look for **File**: marker
   - Look for code block comments
   - Infer from task description
   - Ask user if still unclear

2. If directory doesn't exist:
   - Create parent directories
   - Log creation
   - Proceed

3. If file already exists (unexpected):
   - Ask user: Overwrite or skip?
   - If critical file: Always ask
   - If test file: Can overwrite
```

---

### Step 6: Progress Tracking

Track and report progress continuously:

```markdown
## Execution Progress

### Phase 1: Foundation & Types ✅ COMPLETE
- Task 1.1: Create Types ✅ (10min)
- Task 1.2: Write Test - API Client ✅ (3min)
- Task 1.3: Implement - API Client ✅ (8min)
- Task 1.4: Write Test - useFeature Hook ✅ (3min)
- Task 1.5: Implement - useFeature Hook ✅ (10min)
- Task 1.6: Commit Foundation ✅ (1min)
**Phase Total**: 35min

### Phase 2: Presentational Components 🔄 IN PROGRESS (60% - 18/30 tasks)
- Task 2.1: Write Test - FeatureItem ✅ (3min)
- Task 2.2: Implement - FeatureItem ✅ (4min)
- Task 2.3: Enhance - FeatureItem ✅ (4min)
- Task 2.4: Additional Tests - FeatureItem ✅ (3min)
- Task 2.5: Commit - FeatureItem ✅ (1min)
- Task 2.6: Write Test - Button ▶️ IN PROGRESS
- Task 2.7-2.30: Pending

### Overall Progress
**Completed**: 21/89 tasks (24%)
**Time Spent**: 1h 15min / est. 4h total
**Tests**: 18 passing, 0 failing
**Commits**: 6
```

---

### Step 7: Final Verification

After all tasks complete:

```markdown
1. Run comprehensive test suite:
   ```bash
   npm test -- --coverage
   ```

2. Verify coverage meets goals (from plan)

3. Check all acceptance criteria from plan

4. Verify all commits made

5. Run linter:
   ```bash
   npm run lint
   ```

6. Generate summary report

7. Suggest next steps:
   - Run `/review code` for deeper review
   - Run `/ship` to create PR
   - Runn `/ execute-plan [next-phase]` if phased approach
```

## Critical Rules

### Never Skip Code Reviews

Every task must be reviewed before proceeding. No exceptions.

### Never Proceed with Critical Issues

Critical issues must be fixed:
```
implement → review → fix critical → re-review → proceed
```

### Never Run Parallel Implementation

Tasks run sequentially:
```
WRONG: Run Task 1, 2, 3 simultaneously
RIGHT: Task 1 → Review → Task 2 → Review → Task 3 → Review
```

### Always Read Plan Before Implementing

```
WRONG: Start coding based on memory of plan
RIGHT: Read plan file, extract task details, then implement
```

## Error Handling

### Task Fails

1. Capture error details
2. Attempt fix (max 2 retries)
3. If still failing, pause execution
4. Report to user with:
   - Which task failed
   - Error details
   - Suggested resolution
5. Wait for user decision

### Review Finds Major Issues

1. List all Critical/Important issues
2. Dispatch fix subagent for each
3. Re-run code review
4. If issues persist after 2 cycles:
   - Pause execution
   - Report to user
   - May need plan revision

## Output

### Progress Updates

```markdown
## Execution Progress

### Task 1: Create User model ✓
- Files modified: src/models/user.ts
- Tests added: 3
- Review: Passed

### Task 2: Add validation ✓
- Files modified: src/models/user.ts
- Tests added: 2
- Review: Passed (1 minor deferred)

### Task 3: Create endpoint [IN PROGRESS]
- Status: Implementing...
```

### Completion Summary

```markdown
## Execution Complete

### Summary
- Tasks completed: 8/8
- Tests added: 24
- Coverage: 92%

### Files Created
- src/models/user.ts
- src/services/user-service.ts
- src/routes/user.ts

### Files Modified
- src/routes/index.ts
- src/types/index.ts

### Deferred Items
- Minor: Variable rename in user-service.ts line 12

### Next Steps
- Run full test suite
- Use /ship to create PR
```

## Prerequisites

Before using this command:

1. Plan file exists and is complete
2. Plan was created with `/plan --detailed`
3. Plan has been reviewed and approved
4. Tests can be run (`npm test` or `pytest`)

## Related Commands

- `/plan --detailed` - Create detailed plan
- `/brainstorm` - Design before planning
- `/ship` - Create PR after execution
