---
name: executing-plans
description: Subagent-driven development pattern for executing detailed implementation plans with quality gates. Uses fresh agents per task to prevent context pollution and mandatory code review between tasks for quality assurance. Use when executing plans created with writing-plans skill, implementing independent tasks, or systematic development with verification.
---

# Executing Plans

## Quick Start

1. Load the implementation plan file
2. Create TodoWrite with all tasks from plan
3. For each task: dispatch subagent → code review → handle findings
4. Complete with final review and branch cleanup

## Instructions

### Prerequisites
- Must have an approved implementation plan (created with `writing-plans` skill)
- Plan should be saved in a readable file
- All requirements should be clearly defined

### Execution Process

#### Step 1: Load and Prepare
1. Read the plan file completely
2. Verify plan is approved and ready for execution
3. Create TodoWrite with all tasks extracted from plan
4. Set first task status to `in_progress`

#### Step 2: Execute Each Task
For every task in the plan:

1. **Dispatch implementation subagent** with:
   - Task details and requirements
   - Files to modify/create
   - Success criteria from plan

2. **Subagent follows TDD**:
   - Write failing test first
   - Verify test actually fails
   - Implement minimal code to pass
   - Verify test passes
   - Commit changes with clear message

3. **Get completion summary**:
   - Files modified
   - Tests added/updated
   - Commit hash
   - Any deviations from plan

#### Step 3: Code Review Gate
1. **Dispatch code-reviewer subagent**
2. Review scope: ONLY changes from current task
3. Review against:
   - Plan requirements for this task
   - Code quality standards
   - Security best practices
   - Test coverage

4. **Categorize findings**:
   - **Critical**: Security issues, broken functionality
   - **Important**: Performance, maintainability, test gaps
   - **Minor**: Style, documentation, optimizations

#### Step 4: Handle Review Results
```yaml
IF Critical or Important issues:
  - Fix immediately before proceeding
  - Re-request code review
  - Repeat until clean

IF only Minor issues:
  - Note for cleanup task
  - Proceed to next task
```

#### Step 5: Update Progress
1. Mark current task `completed` in TodoWrite
2. Move to next task (`pending` → `in_progress`)
3. Repeat from Step 2

### Final Steps (After All Tasks)
1. Comprehensive code review of entire implementation
2. Verify all success criteria from plan are met
3. Run full test suite
4. Use `finishing-development-branch` skill for cleanup
5. Provide execution summary to user

## When to Use

✅ **Perfect for**:
- Executing approved plans from `writing-plans` skill
- Implementing independent tasks in current session
- Quality-focused development without human delays
- Systematic implementation with verification

❌ **NOT for**:
- Plans that need review first (use `brainstorming` skill)
- Tightly coupled tasks requiring shared context
- Plans that need revision during execution
- Simple one-off tasks (implement directly)

## Critical Rules

### 🚫 Never Skip Code Reviews
Every task MUST be reviewed before proceeding. No exceptions.

### 🚫 Never Proceed with Critical Issues
Critical issues block progress until fixed.

### 🚫 Never Run Parallel Tasks
Tasks execute sequentially: Implement → Review → Next Task

### ✅ Always Read Plan First
Never implement from memory - read plan file for each task.

## Examples

### Example 1: Simple 3-Task Plan
```markdown
# Plan: Add User Authentication

## Tasks
1. Create User model with validation
2. Implement JWT authentication endpoints
3. Add authentication middleware

## Execution Flow:
Task 1 → Review → Task 2 → Review → Task 3 → Review → Final Review
```

### Example 2: Subagent Communication
```markdown
### Dispatching Implementation Subagent
"Implement user login endpoint following these requirements:
- POST /auth/login
- Validate email/password
- Return JWT token on success
- Use bcrypt for password hashing
- Follow TDD pattern
- Return completion summary"

### Handling Code Review
"Code review completed:
- Critical: Missing rate limiting (must fix)
- Important: Add logging for failed attempts (should fix)
- Minor: Extract password policy to config (can defer)

Fixing critical issues before proceeding..."
```

### Example 3: TodoWrite Tracking
```markdown
| Task | Status | Notes |
|------|--------|-------|
| 1. User model | completed | ✅ Reviewed, no issues |
| 2. Auth endpoints | in_progress | 🔄 Fixing critical security issue |
| 3. Middleware | pending | ⏳ Waiting for task 2 |
```

## Best Practices

### Planning Phase
- Always use `writing-plans` skill to create detailed plans
- Ensure every task has clear success criteria
- Get plan approved before execution

### Implementation Phase
- Use fresh subagent for each task (no context carryover)
- Follow TDD: test first, implement minimal code
- Commit after each completed task
- Never skip code review gates

### Quality Assurance
- Critical issues block progress - fix immediately
- Important issues should be fixed before proceeding
- Minor issues can be deferred to cleanup task
- Always review against plan requirements

### Progress Tracking
- Update TodoWrite in real-time
- Clear status transitions: pending → in_progress → completed
- Document any deviations from plan
- Provide regular summaries to user

### Error Handling
- If task fails after 2 retries, pause and report
- Major review issues after 2 cycles may need plan revision
- Always communicate blockers to user
- Keep detailed logs of decisions and changes

## Requirements

### Prerequisites
- Approved implementation plan file
- Write access to target repository
- Test framework configured
- Code review guidelines established

### Dependencies
- `writing-plans` skill (for plan creation)
- `code-reviewer` skill (for quality gates)
- `finishing-development-branch` skill (for cleanup)
- Task management with TodoWrite

---

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

---

## Execution Workflow

### Step 1: Load Plan

```markdown
1. Read the plan file
2. Verify plan is complete and approved
3. Create TodoWrite with all tasks from plan
4. Set first task to in_progress
```

### Step 2: Execute Task

For each task:

```markdown
1. Dispatch fresh subagent with task details
2. Subagent implements following TDD cycle:
   - Write failing test
   - Verify test fails
   - Implement minimally
   - Verify test passes
   - Commit
3. Subagent returns completion summary
```

### Step 3: Code Review

After each task:

```markdown
1. Dispatch code-reviewer subagent
2. Review scope: only changes from current task
3. Reviewer returns findings:
   - Critical: Must fix before proceeding
   - Important: Should fix before proceeding
   - Minor: Can fix later
```

### Step 4: Handle Review Findings

```markdown
IF Critical or Important issues found:
  1. Dispatch fix subagent for each issue
  2. Re-request code review
  3. Repeat until no Critical/Important issues

IF only Minor issues:
  1. Note for later cleanup
  2. Proceed to next task
```

### Step 5: Mark Complete

```markdown
1. Update TodoWrite - mark task completed
2. Move to next task
3. Repeat from Step 2
```

### Step 6: Final Review

After all tasks complete:

```markdown
1. Dispatch comprehensive code review
2. Review entire implementation against plan
3. Verify all success criteria met
4. Run full test suite
5. Use `finishing-development-branch` skill
```

---

## Critical Rules

### Never Skip Code Reviews

Every task must be reviewed before proceeding. No exceptions.

### Never Proceed with Critical Issues

Critical issues must be fixed. The pattern is:
```
implement → review → fix critical → re-review → proceed
```

### Never Run Parallel Implementation

Tasks run sequentially:
```
WRONG: Run Task 1, 2, 3 simultaneously
RIGHT: Run Task 1 → Review → Task 2 → Review → Task 3 → Review
```

### Always Read Plan Before Implementing

```
WRONG: Start coding based on memory of plan
RIGHT: Read plan file, extract task details, then implement
```

---

## Subagent Communication

### Implementation Subagent Prompt

```markdown
## Task: [Task Name]

**Context**: Executing plan for [Feature Name]

**Files to modify**:
- [File paths from plan]

**Steps**:
[Exact steps from plan]

**Requirements**:
- Follow TDD: test first, then implement
- Commit after completion
- Return summary of what was done

**Output expected**:
- Files modified
- Tests added
- Commit hash
- Any issues encountered
```

### Code Review Subagent Prompt

```markdown
## Code Review Request

**Scope**: Changes from Task [N]

**Files changed**:
- [List of files]

**Review against**:
- Plan requirements for this task
- Code quality standards
- Security best practices
- Test coverage

**Return**:
- Critical issues (must fix)
- Important issues (should fix)
- Minor issues (can defer)
- Approval status
```

---

## TodoWrite Integration

Maintain task status throughout:

```markdown
| Task | Status |
|------|--------|
| Task 1: Create model | completed |
| Task 2: Add validation | completed |
| Task 3: Create endpoint | in_progress |
| Task 4: Add tests | pending |
| Task 5: Documentation | pending |
```

Update status in real-time:
- `pending` → `in_progress` when starting
- `in_progress` → `completed` when reviewed and approved

---

## Error Handling

### Task Fails

```markdown
1. Capture error details
2. Attempt fix (max 2 retries)
3. If still failing, pause execution
4. Report to user with:
   - Which task failed
   - Error details
   - Suggested resolution
5. Wait for user decision
```

### Review Finds Major Issues

```markdown
1. List all Critical/Important issues
2. Dispatch fix subagent for each
3. Re-run code review
4. If issues persist after 2 cycles:
   - Pause execution
   - Report to user
   - May need plan revision
```

---

## Completion Checklist

Before declaring plan execution complete:

- [ ] All tasks marked completed
- [ ] All code reviews passed
- [ ] Full test suite passes
- [ ] No Critical issues outstanding
- [ ] No Important issues outstanding
- [ ] Final comprehensive review done
- [ ] Ready for `finishing-development-branch`

---
