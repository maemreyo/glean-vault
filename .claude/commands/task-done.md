# /task-done - Mark Task Complete

## Purpose

Mark a task as complete in the plan, create a git commit, and prepare for the next task. This is the final step in the task execution workflow.

**"Commit with confidence"** - Lock in verified work and move forward.

## Aliases

```bash
/task-done [plan-file] --task=ID
/done-task [plan-file] --task=ID
/td [plan-file] --task=ID
```

## Usage

```bash
# Mark specific task complete (with auto-commit)
/task-done plans/multi-theme.md --task=A.1

# Custom commit message
/task-done plans/feature.md --task=B.2 --message="feat: add dark mode support"

# Skip git commit (manual commit later)
/task-done plans/feature.md --task=A.1 --no-commit

# Mark current task done (auto-detect last executed)
/task-done plans/feature.md
```

## Arguments

- `$ARGUMENTS`: Path to implementation plan markdown file

## Flags

| Flag | Description | Example |
|------|-------------|---------|
| `--task=ID` | Specific task to mark complete | `--task=A.1` |
| `--message="text"` | Custom git commit message | `--message="feat: add feature"` |
| `--no-commit` | Skip git commit (mark [x] only) | `--no-commit` |
| `--no-verify` | Skip pre-commit hooks | `--no-verify` |
| `--show-next` | Show next task after completion | `--show-next` (default: true) |

---

## Core Philosophy

**Atomic Commits**:
- One task = one commit
- Clear commit messages
- Traceable history

**Single Source of Truth**:
- Update [x] directly in plan markdown
- No hidden state files

---

## Workflow

### Step 1: Validate Task Ready (1-2 min)

```markdown
Readiness Validator

GOAL: Ensure task is ready to mark complete

STEPS:

1. {{ if --task provided }}
   Load task {{ task ID }} from plan
   {{ else }}
   Auto-detect last executed task
   {{ endif }}

2. Check task status:
   - {{ if already marked [x] }}
     ⚠️ WARNING: Task already complete
     → Nothing to do
     STOP
   {{ endif }}

3. {{ if not --no-commit }}
   Pre-commit validation:
   
   a. Check git status:
      - Modified files exist?
      - {{ if no changes }}
        ⚠️ WARNING: No changes to commit
        → Did you run /task-execute?
        → Recommend: --no-commit to just mark [x]
      {{ endif }}
   
   b. Check verification status (optional reminder):
      - "Have you run /task-verify?"
      - {{ if user confirms yes }}
        Proceed
      {{ else }}
        → Recommend: /task-verify {{ plan file }} first
        → User can choose to proceed anyway
      {{ endif }}

{{ endif }}

OUTPUT: Validation status
```

---

### Step 2: Update Plan Markdown (1 min)

```markdown
Plan Updater

GOAL: Mark task as complete in plan file

STEPS:

1. Read plan file: {{ plan file }}

2. Find task line:
   - Pattern: `- [ ] {{ task ID }}:`
   - Example: `- [ ] A.1: Implement CSS Sanitization`

3. Update to complete:
   - Replace `- [ ]` with `- [x]`
   - Add timestamp (optional):
     `- [x] A.1: Implement CSS Sanitization <!-- completed: {{ timestamp }} -->`

4. Write updated plan back to file

5. Verify update:
   - Read plan again
   - Confirm task now shows `[x]`

OUTPUT: Updated plan file
```

---

### Step 3: Git Commit (2-5 min)

{{ if not --no-commit }}

```markdown
Git Committer

GOAL: Create atomic commit for this task

STEP 3.1: Generate Commit Message

{{ if --message provided }}
Use custom message: {{ user message }}

{{ else }}
Auto-generate from task:
- Read task description from plan
- Format: "{{ type }}: {{ description }} ({{ task ID }})"

Type detection:
{{ if task creates new feature }}
Type: feat
{{ else if task fixes bug }}
Type: fix
{{ else if task refactors }}
Type: refactor
{{ else if task updates docs }}  
Type: docs
{{ else if task adds tests }}
Type: test
{{ else }}
Type: chore
{{ endif }}

Example:
- Task: "A.1: Implement CSS Sanitization"
- Message: "feat: implement CSS sanitization (A.1)"
```

STEP 3.2: Stage Changes

```bash
# Add all modified files related to task
git add {{ files modified by task }}

# Or if unsure, add all:
git add .
```

STEP 3.3: Create Commit

```bash
git commit -m "{{ commit message }}" {{ if --no-verify }}--no-verify{{ endif }}
```

STEP 3.4: Capture Commit Hash

```bash
commit_hash=$(git rev-parse HEAD)
```

OUTPUT: Commit created, hash captured

{{ else }}

Skip git commit (--no-commit flag)

{{ endif }}

---

### Step 4: Show Progress & Next Task (1-2 min)

```markdown
Progress Reporter

GOAL: Show completion status and what's next

DISPLAY:

═══════════════════════════════════════════════
✅ TASK COMPLETE

**Task**: {{ task ID }}: {{ description }}
**Phase**: {{ phase ID }}
**Timestamp**: {{ completion time }}

═══════════════════════════════════════════════

## Changes

{{ if not --no-commit }}
✅ Git commit created:
   **Hash**: {{ commit hash }}
   **Message**: "{{ commit message }}"
   **Files**: {{ file count }} changed

   View commit:
   ```bash
   git show {{ commit hash }}
   ```
{{ endif }}

✅ Plan updated:
   `- [x] {{ task ID }}: {{ description }}`

═══════════════════════════════════════════════

## Progress Update

**Phase {{ phase ID }}**:
- Completed: {{ X }}/{{ Y }} tasks ({{ percentage }}%)
- Remaining: {{ task IDs }}

**Overall**:
- Completed: {{ X }}/{{ total }} tasks ({{ percentage }}%)
- Estimated time remaining: {{ estimate }}

Progress: ████████░░░░ {{ percentage }}%

═══════════════════════════════════════════════

{{ if --show-next }}
## Next Task

{{ run /task-next inline to show next task preview }}

**Quick start**:
```bash
/task-next {{ plan file }}
/task-execute {{ plan file }} --task={{ next task ID }}
```
{{ endif }}

═══════════════════════════════════════════════
```

---

## Output Examples

### Example 1: Standard Completion

```markdown
✅ TASK COMPLETE

**Task**: A.1: Implement CSS Sanitization
**Phase**: A (Security Fixes)
**Timestamp**: 2025-12-12 16:55:00

═══════════════════════════════════════════════

## Changes

✅ Git commit created:
   **Hash**: abc1234
   **Message**: "feat: implement CSS sanitization (A.1)"
   **Files**: 3 changed

✅ Plan updated:
   `- [x] A.1: Implement CSS Sanitization`

═══════════════════════════════════════════════

## Progress Update

**Phase A**: 1/3 tasks (33%)
**Overall**: 1/33 tasks (3%)

═══════════════════════════════════════════════

## Next Task

📋 A.2: Add Input Validation
- File: `src/validation.ts`
- Estimate: 3 hours

Run: /task-next plans/multi-theme.md
```

---

### Example 2: No Commit Mode

```markdown
✅ TASK MARKED COMPLETE

**Task**: B.2: Update CSS Structure
**Phase**: B (Architecture)

═══════════════════════════════════════════════

## Changes

⏭️ Git commit skipped (--no-commit)
   → You can commit manually later

✅ Plan updated:
   `- [x] B.2: Update CSS Structure`

═══════════════════════════════════════════════
```

---

## Examples

### Example 1: Standard Usage

```bash
/task-done plans/multi-theme.md --task=A.1
```

Marks A.1 as [x] and creates git commit.

### Example 2: Custom Commit Message

```bash
/task-done plans/feature.md --task=B.2 --message="feat: add comprehensive dark mode support with theme switching"
```

### Example 3: Mark Without Committing

```bash
/task-done plans/feature.md --task=A.1 --no-commit
```

Updates plan but skips git commit (manual commit later).

### Example 4: Auto-detect Last Task

```bash
/task-done plans/feature.md
```

Marks most recent executed task as complete.

---

## Integration

### Full Task Workflow

```bash
# 1. Review task
/task-next plan.md

# 2. Execute
/task-execute plan.md --task=A.1

# 3. Verify
/task-verify plan.md

# 4. Mark done (this command)
/task-done plan.md --task=A.1

# 5. Repeat
/task-next plan.md
```

### Quick Workflow (After Verification)

```bash
/task-verify plan.md && /task-done plan.md --task=A.1
```

---

## Safety Features

1. **Validation**: Checks if task already complete
2. **Verification Reminder**: Prompts to verify first
3. **Git Safety**: Can skip commit with --no-commit
4. **Clear History**: One task = one commit
5. **Progress Tracking**: Shows completion percentage

---

## Success Criteria

- [ ] Validates task ready for completion
- [ ] Updates plan markdown ([x])
- [ ] Creates git commit with clear message
- [ ] Shows completion summary
- [ ] Displays next task
- [ ] Updates progress metrics

---

## Related Commands

- `/task-execute` - Implement the task
- `/task-verify` - Verify before marking done
- `/task-next` - Show next task
- `/task-progress` - Full progress dashboard

---

## Pro Tips

1. **Always verify before marking done**:
   ```bash
   /task-verify plan.md && /task-done plan.md --task=A.1
   ```

2. **Use descriptive commit messages for important features**:
   ```bash
   /task-done plan.md --task=B.1 --message="feat: implement centralized Theme Manager with singleton pattern and performance optimizations"
   ```

3. **Review commit before pushing**:
   ```bash
   /task-done plan.md --task=A.1
   git show HEAD  # Review
   git push       # Push when ready
   ```

4. **Batch commits for related small tasks** (when appropriate):
   ```bash
   /task-execute plan.md --task=A.1
   /task-execute plan.md --task=A.2
   /task-verify plan.md --phase=A
   /task-done plan.md --task=A.1 --no-commit
   /task-done plan.md --task=A.2 --message="feat: complete security hardening (A.1, A.2)"
   ```

---

**Remember**: A well-committed task is a task you can confidently build upon! ✅🎯
