# /cook - Pragmatic Task Iterator (V2)

## Purpose

Execute the **next uncompleted task** from an implementation plan, verify it works, and stop for developer review. Acts as a focused iterator - one task per invocation.

**"One task at a time, solid execution"** - Stateless, atomic, developer-controlled.

## Aliases

```bash
/cook [plan-file]              # Normal mode with full discovery
/cook [plan-file] --task=ID    # Fast-track to specific task
/cook [plan-file] --resume     # Quick resume from last task
/cook-next [plan-file]         # Alias for --resume
```

## Usage

```bash
# Execute next uncompleted task
/cook plans/multi-theme.md

# Execute next task in specific phase
/cook plans/feature.md --phase=A

# Dry run (preview without changes)
/cook plans/feature.md --dry-run

# Skip verification (fast mode, use carefully)
/cook plans/feature.md --skip-verify

# Allow auto-fix on test failures
/cook plans/feature.md --auto-fix
```

## Arguments

- `$ARGUMENTS`: Path to implementation plan markdown file

## Flags

| Flag | Description | Example |
|------|-------------|---------|
| `--task=ID` | Skip discovery, execute specific task | `--task=A.2` |
| `--resume` | Quick resume from last completed task | `--resume` |
| `--phase=ID` | Limit to specific phase | `--phase=A` |
| `--dry-run` | Preview without executing | `--dry-run` |
| `--skip-verify` | Skip test verification | `--skip-verify` |
| `--auto-fix` | Auto-retry once on test failure | `--auto-fix` |
| `--no-update` | Don't update plan checkbox | `--no-update` |
| `--skip-subtasks` | Skip all subtasks of current main task | `--skip-subtasks` |
| `--suggest-split` | Auto-suggest subtasks for large tasks | `--suggest-split` |

---

## Core Philosophy

### Iterator Pattern

**Not a loop, but a single step**:
- Each `/cook` = Exactly 1 task
- Reads plan → Finds first `[ ]` → Executes → Stops
- Developer reviews → Commits → Runs `/cook` again

### Stateless Design

**No hidden state**:
- Source of truth: Markdown plan file (`[ ]` vs `[x]`)
- No progress.json, no memory files
- Each invocation reads fresh from plan

### Developer Control

**Human in the loop**:
- AI implements + tests
- Developer reviews (`git diff`)
- Developer commits (approval)
- `/cook` updates plan `[x]` automatically (unless --no-update)
- Developer runs next iteration

### Subtask Support

**Hierarchical task breakdown**:
- Main tasks: `- [ ] A.1: Task name`
- Subtasks (indented): `  - [ ] A.1.a: Subtask name`
- Auto-detect subtasks and execute them first
- Skip subtasks with `--skip-subtasks` flag
- Checkbox states: `[ ]` uncompleted, `[x]` completed, `[~]` skipped

---

## Workflow (4 Phases)

### Phase 1: Discovery (2-5 min → 10s with fast-track)

```markdown
Task Scanner

GOAL: Find next task to execute

---

**FAST TRACK CHECK** (NEW):

{{ if --task provided }}
   ⚡ **FAST TRACK MODE: Explicit Task**
   
   Task specified: {{ task ID }}
   Skipping full discovery (saves 2-5 min)
   
   STEPS:
   1. Read plan file: $ARGUMENTS
   
   2. Search for exact task line:
      Pattern: `- [ ] {{ task ID }}:`
   
   3. {{ if task not found }}
      ❌ ERROR: Task "{{ task ID }}" not found in plan
      
      Possible issues:
      - Wrong task ID
      - Task already completed [x]
      - Typo in --task flag
      
      Suggestion: Run discovery to find next task
      ```bash
      /cook {{ plan file }}
      ```
      
      STOP
   {{ endif }}
   
   4. {{ if task marked [x] }}
      ⚠️ WARNING: Task {{ task ID }} already completed
      
      Re-run anyway? This will re-implement completed work.
      
      Suggestion: Find next uncompleted task
      ```bash
      /cook {{ plan file }}
      ```
      
      STOP
   {{ endif }}
   
   5. Extract task details (same as normal step 5-6)
   6. Validate dependencies (same as normal step 8)
   
   ✅ Fast track validated: {{ task ID }}
   ⏱️ Time saved: ~2-4 minutes
   
   {{ PROCEED TO PHASE 2 }}

{{ else if --resume }}
   ⚡ **RESUME MODE: Continue from last**
   
   Checking conversation context...
   
   STEPS:
   1. Search conversation history for last completed task:
      - Look for "COOK COMPLETE" messages
      - Extract last task ID marked [x]
   
   2. {{ if found last task }}
      Last completed: {{ last task ID }} ✅
      
      Read plan file: $ARGUMENTS
      
      Find next uncompleted task after {{ last task ID }}:
      - Same phase if available
      - Next phase if current phase complete
      
      {{ if found next task }}
         ✅ Resume point: {{ next task ID }}
         ⏱️ Quick lookup: ~20 seconds (vs 2-5 min full scan)
         
         Extract task details and proceed
         
         {{ PROCEED with this task }}
      {{ else }}
         No tasks found after {{ last task ID }}
         
         Possible reasons:
         - Plan complete 🎉
         - All remaining tasks in different phase
         
         {{ Fall back to NORMAL DISCOVERY }}
      {{ endif }}
   {{ else }}
      ⚠️ No previous completion found in conversation
      
      This might be:
      - First run in this conversation
      - Long conversation (history truncated)
      - Different plan file
      
      {{ Fall back to NORMAL DISCOVERY }}
   {{ endif }}

{{ else }}
   🔍 **NORMAL DISCOVERY MODE**
   
   Full plan analysis required
   
{{ endif }}

---

STEPS (if NORMAL DISCOVERY):

1. Read plan file: $ARGUMENTS

2. Parse markdown for tasks:
   - Main task pattern: `- [ ] [Task ID]: [Description]`
   - Subtask pattern: `  - [ ] [Task ID].[a-z]: [Description]` (2-space indent)
   - Example main: `- [ ] A.1: Implement CSS Sanitization`
   - Example subtask: `  - [ ] A.1.a: Setup dependencies`

3. Find next uncompleted task with subtask awareness:
   {{ if --phase provided }}
   - Search within Phase {{ phase ID }} section only
   {{ endif }}
   
   a. Find first uncompleted main task (no indent): `- [ ] X.Y:`
   
   b. Check for subtasks:
      - Look for indented tasks with pattern: `  - [ ] X.Y.[a-z]:`
      - Count uncompleted subtasks
   
   c. Determine what to execute:
      {{ if --skip-subtasks }}
      - Mark all subtasks of current main task as [~] (skipped)
      - Execute main task
      {{ else if has uncompleted subtasks }}
      - Execute first uncompleted subtask (e.g., A.1.a)
      - Main task waits until all subtasks complete
      {{ else if all subtasks [x] or [~] }}
      - All subtasks done/skipped → Execute main task
      {{ else }}
      - No subtasks → Execute main task directly
      {{ endif }}

4. {{ if no uncompleted task found }}
   🎉 **PLAN COMPLETE**
   All tasks are marked [x]!
   
   Summary:
   - Total tasks: {{ count }}
   - All completed ✅
   
   Next steps:
   - Review final code
   - Run full test suite
   - Deploy to staging
   
   EXIT
   {{ endif }}

5. Extract task details:
   ```markdown
   ### A.1: Task Name [Estimate]
   - **File**: `path/to/file.ts`
   - **Action**: What to do
   - **Depends on**: (optional)
   - **Verify**: npm test command
   ```

6. Parse:
   - Task ID (e.g., A.1)
   - Description
   - File path(s)
   - Operation: CREATE | MODIFY | DELETE
   - Verification command
   - Dependencies

7. {{ if --suggest-split and task estimate > 4 hours }}
   Complexity Detection:
   - Large task detected ({{ estimate }}h)
   - Analyze task description
   - Generate subtask suggestions
   
   Suggest breakdown:
   ```markdown
   ⚠️ LARGE TASK DETECTED
   
   Task {{ task ID }} is estimated at {{ estimate }}h.
   Consider breaking into subtasks:
   
   ```diff
   - - [ ] {{ task ID }}: {{ description }} [{{ estimate }}h]
   + - [ ] {{ task ID }}: {{ description }} [Summary]
   +   - [ ] {{ task ID }}.a: {{ subtask 1 }} [Xh]
   +   - [ ] {{ task ID }}.b: {{ subtask 2 }} [Yh]
   +   - [ ] {{ task ID }}.c: {{ subtask 3 }} [Zh]
   ```
   
   Options:
   1. [y] Add subtasks automatically
   2. [n] Continue with main task
   3. [e] Show markdown to copy manually
   
   {{ wait for user input }}
   
   {{ if user chooses y }}
   - Insert subtasks into plan file
   - Re-run discovery to find first subtask
   {{ else if user chooses e }}
   - Display suggested markdown
   - User copies manually
   - Exit (user re-runs /cook)
   {{ else }}
   - Continue with main task
   {{ endif }}
   {{ endif }}

8. {{ if task has dependencies }}
   Validate dependencies:
   - Check if dependency tasks marked [x]
   - {{ if any incomplete }}
     ⚠️ ERROR: Dependencies not met
     - Task {{ dep ID }}: Still [ ] (incomplete)
     
     Recommend:
     /cook {{ plan file }} --phase={{ dep phase }}
     
     STOP
   {{ endif }}
   {{ endif }}

OUTPUT: Task object with all details
```

---

### Phase 2: Contextualization (5-10 min for MODIFY, skip for CREATE)

{{ if not --dry-run }}

```markdown
Context Loader

GOAL: Understand current code before changes

{{ if operation is MODIFY }}

STEPS:

1. Read target file: `{{ file path }}`

2. Analyze current implementation:
   - File structure
   - Existing functions/classes
   - Patterns used
   - Dependencies (imports)

3. Identify modification points:
   - Where to add new code
   - What to preserve
   - Potential conflicts

4. Create modification strategy:
   - Specific lines to change
   - New code to add
   - Logic to preserve

OUTPUT: Context summary + modification plan

{{ else if operation is CREATE }}

STEPS:

1. Identify directory structure
2. Determine file template (component, utility, type, etc.)
3. Gather necessary imports

OUTPUT: Creation plan

{{ else if operation is DELETE }}

STEPS:

1. Find files that depend on target
2. List cleanup required

OUTPUT: Deletion checklist

{{ endif }}
```

{{ else }}

DRY RUN: Skip context loading

{{ endif }}

---

### Phase 3: Implementation (10-45 min depending on task)

{{if not --dry-run }}

**Dispatch Task-Executor Agent** (`.claude/agents/task-executor.md`):

```markdown
Task-Executor Agent - Implement {{ task.id }}

GOAL: Implement code changes per task specification

TASK SPECIFICATION:
- ID: {{ task.id }}
- Description: {{ task.description }}
- Files: {{ task.files }}
- Action: {{ task.action }}
- Expected: {{ task.expected }}

{{ if context from Phase 2 }}
CONTEXT (from Scout):
{{ scout analysis and modification strategy }}
{{ endif }}

IMPLEMENTATION DETAILS:
{{ task details from plan }}

{{ if task.issues }}
KNOWN ISSUES (from plan):
{{ task.issues }}
{{ endif }}

---

INSTRUCTIONS FOR TASK-EXECUTOR:

{{ if CREATE }}
**Operation**: CREATE new file `{{ file path }}`

Requirements:
1. Determine file type and template (see .claude/docs/task-executor/create-patterns.md)
2. Generate proper file structure:
   - Imports section
   - Type definitions
   - Main implementation
   - Exports
3. Follow project conventions:
   - Check similar files for patterns
   - Match naming style
   - Use consistent formatting
4. Add JSDoc documentation
5. Ensure all exports are correct

{{ else if MODIFY }}
**Operation**: MODIFY existing file `{{ file path }}`

Requirements (see .claude/docs/task-executor/modify-strategies.md):
1. Read current file content first
2. Identify exact modification points
3. Choose edit tool:
   - Single change → replace_file_content
   - Multiple changes → multi_replace_file_content
4. Preserve existing code:
   - Keep formatting
   - Maintain comments
   - Preserve variable names
5. Minimize changes - only modify what's necessary
6. Update imports/exports if needed

{{ else if DELETE }}
**Operation**: DELETE file `{{ file path }}`

Requirements (see .claude/docs/task-executor/delete-workflows.md):
1. Analyze dependencies FIRST:
   ```bash
   grep_search "from.*{{ filename }}"
   grep_search "import.*{{ filename }}"
   ```
2. Create cleanup plan for all references
3. Clean dependencies:
   - Remove imports from consuming files
   - Remove from index files
   - Update any re-exports
   - Fix or remove usages
4. Validate no references remain
5. Only then delete the file
6. Re-validate syntax

{{ endif }}

---

SYNTAX VALIDATION:

After implementing changes:

{{ if TypeScript project }}
1. Run: `npx tsc --noEmit {{ changed files }}`
2. If errors found:
   - Apply auto-fix patterns (see .claude/docs/task-executor/error-handling.md)
   - Common fixes:
     * Missing imports → Add them
     * Type errors → Add annotations
     * Unused variables → Remove or prefix with _
   - Re-run validation
   - Max 3 fix attempts
3. Report syntax status

{{ else if JavaScript project }}
1. Run: `node --check {{ changed files }}`
2. Fix syntax errors
3. Report status
{{ endif }}

---

OUTPUT FORMAT:

```markdown
## IMPLEMENTATION COMPLETE: {{ task.id }}

### Files Changed
{{ if CREATE }}
Created: `{{ file path }}` ({{ lines }} lines)
- Structure: {{ type }}
- Exports: {{ list }}
{{ endif }}

{{ if MODIFY }}
Modified: `{{ file path }}`
- Added: {{ X }} lines
- Modified: {{ Y }} lines
- Deleted: {{ Z }} lines
- Functions affected: {{ list }}
{{ endif }}

{{ if DELETE }}
Deleted: `{{ file path }}`

Dependencies Cleaned:
- {{ file 1 }}: {{ changes }}
- {{ file 2 }}: {{ changes }}
{{ endif }}

### Syntax Validation
Command: `{{ validation command }}`
Result: {{ PASS | FAIL }}

{{ if auto-fixes applied }}
Auto-Fixes Applied:
- {{ fix 1 }}
- {{ fix 2 }}
{{ endif }}

### Status
{{ PASS → "🟢 READY FOR VERIFICATION" }}
{{ FAIL → "🔴 SYNTAX ERRORS REMAIN" }}
```

TIME LIMIT: 30 minutes
```

WAIT for Task-Executor response...

{{ else }}

DRY RUN: Show what would be implemented

OUTPUT: Implementation preview

{{ endif }}


---

### Phase 4: Verification & Handoff (5-20 min)

{{ if --dry-run }}

**DRY RUN MODE: Skip verification**

Show what verification would run:
- Command: `{{ task.verify }}`
- Expected: {{ task.expected }}

{{ PROCEED TO OUTPUT }}

{{ else if --skip-verify }}

**SKIP VERIFICATION MODE**

⚠️ Verification skipped (--skip-verify flag)

{{ if not --no-update }}
   Update plan immediately (no verification):
   1. Read plan file: `{{ plan file path }}`
   2. Find task line: `- [ ] {{ task.id }}:`
   3. Update checkbox: `- [ ]` → `- [x]`
   4. Write updated plan
   
   ✅ Plan updated - Task {{ task.id }} marked complete (without verification)
{{ else }}
   Plan NOT updated (--no-update flag)
{{ endif }}

{{ PROCEED TO OUTPUT }}

{{ else }}

**VERIFICATION MODE** (default)

---

> **🚨 CRITICAL INSTRUCTION FOR MAIN AI 🚨**
> 
> You are the DISPATCHER, NOT the executor.
> 
> **DO NOT**:
> - ❌ Run `npm test` yourself
> - ❌ Run `npm run build` yourself  
> - ❌ Execute ANY verification commands directly
> - ❌ Parse test output yourself
> 
> **DO**:
> - ✅ Dispatch the Test-Runner Agent
> - ✅ WAIT for Test-Runner's response
> - ✅ Use Test-Runner's results to update plan
> 
> Your role: Orchestrate, not execute.

---

**STEP 4.1: Dispatch Test-Runner Agent** (`.claude/agents/test-runner.md`)

```markdown
Test-Runner Agent - Verify {{ task.id }}

GOAL: Execute verification and report results

VERIFICATION REQUEST:
- Task: {{ task.id }}
- Description: {{ task.description }}
- Files Changed: {{ from task-executor output }}

VERIFICATION:
- Command: `{{ task.verify }}`
- Expected: {{ task.expected }}

{{ if --auto-fix }}
AUTO-FIX MODE: ENABLED
- If verification fails, attempt one fix
- Re-run verification after fix
- Report final status
{{ endif }}

---

INSTRUCTIONS FOR TEST-RUNNER:

1. **Run Verification Command**:
   ```bash
   {{ task.verify }}
   ```
   
2. **Capture Output**:
   - Exit code (0 = success)
   - stdout/stderr
   - Execution time
   
3. **Parse Results**:
   {{ if command contains "test" }}
   - Extract test counts: X/Y passed
   - Extract coverage if available
   - Identify failed test names
   {{ else if command contains "type-check" }}
   - Count TypeScript errors
   - Extract error locations
   - Parse error messages
   {{ else if command contains "build" }}
   - Check build success
   - Note warnings
   - Check bundle size
   {{ else }}
   - Generic pass/fail status
   {{ endif }}

4. **Analyze Failures** (if any):
   - Categorize error type:
     * Assertion failures
     * Type errors
     * Import errors
     * Runtime errors
   - Locate error source (file + line)
   - Identify root cause
   - Suggest fix

{{ if --auto-fix }}
5. **Attempt Auto-Fix** (if failed):
   - Apply fix pattern (see .claude/docs/test-runner/auto-fix-strategies.md)
   - Common fixes:
     * Add missing import
     * Fix type annotation
     * Add null check
     * Correct syntax
   - Re-run verification
   - Max 1 attempt
   - Report retry result
{{ endif }}

---

OUTPUT FORMAT:

```markdown
## VERIFICATION RESULTS: {{ task.id }}

### Execution
Command: `{{ task.verify }}`
Working Dir: {{ cwd }}
Exit Code: {{ code }}
Duration: {{ seconds }}s
Status: {{ PASS | FAIL }}

### Results

{{ if PASS }}
Tests Passed: {{ X/Y }}
{{ if coverage }}
Coverage: {{ % }}
{{ endif }}

Output:
\```
{{ relevant success output }}
\```

{{ else if FAIL }}
Tests Failed: {{ failures/total }}

#### Failed Tests
1. **{{ test name }}**
   - Expected: {{ expected }}
   - Actual: {{ actual }}
   - Location: `{{ file }}:{{ line }}`

2. **{{ test name }}**
   - Error: {{ error message }}

#### Error Analysis
Type: {{ error category }}
Root Cause: {{ diagnosis }}
Affected Files: {{ list }}

#### Full Error Output
\```
{{ error output }}
\```
{{ endif }}

{{ if --auto-fix and FAIL }}
### Auto-Fix Attempt
Diagnosis: {{ error type }}

Fix Applied:
\```{{ language }}
{{ code change }}
\```

Retry Result: {{ PASS | FAIL }}

{{ if still FAIL }}
❌ Auto-fix unsuccessful. Manual intervention required.
{{ else }}
✅ Auto-fix successful!
{{ endif }}
{{ endif }}

{{ if FAIL and not auto-fixed }}
### Suggested Fix
\```{{ language }}
{{ suggested code }}
\```

Explanation: {{ why this should work }}
{{ endif }}
```

TIME LIMIT: 20 minutes
```

---

**STEP 4.2: WAIT for Test-Runner Response**

⏳ Waiting for Test-Runner Agent to complete...

Do NOT proceed until Test-Runner returns with VERIFICATION RESULTS.

---

**STEP 4.3: Process Test-Runner Results**

{{ if Test-Runner returned PASS }}

   ✅ Verification PASSED
   
   {{ if not --no-update }}
      **Update Plan**:
      1. Read plan file: `{{ plan file path }}`
      2. Find task line: `- [ ] {{ task.id }}:`
      3. Update checkbox: `- [ ]` → `- [x]`
      4. Write updated plan
      
      ✅ Plan updated - Task {{ task.id }} marked complete
   {{ else }}
      ⏸️ Plan NOT updated (--no-update flag)
   {{ endif }}
   
   {{ PROCEED TO SUCCESS OUTPUT }}

{{ else if Test-Runner returned FAIL }}

   ❌ Verification FAILED
   
   **Do NOT update plan** - Task {{ task.id }} remains `[ ]`
   
   {{ PROCEED TO FAILURE OUTPUT }}

{{ endif }}

{{ endif }}

---

## Output Format

### Success Case ✅

```markdown
═══════════════════════════════════════════════
🍳 COOK COMPLETE

**Task**: {{ task ID }}: {{ description }}
**Phase**: {{ phase ID }}
**Duration**: {{ time taken }}

═══════════════════════════════════════════════

## Changes Made

{{ if CREATE }}
✅ Created: `{{ file path }}` ({{ lines }} lines)
{{ else if MODIFY }}
✅ Modified: `{{ file path }}`
   - {{ added }} lines added
   - {{ modified }} lines modified
   - {{ deleted }} lines removed
{{ else if DELETE }}
✅ Deleted: `{{ file path }}`
✅ Cleaned up {{ X }} dependent files
{{ endif }}

═══════════════════════════════════════════════

## Verification

{{ if not --skip-verify }}
**Command**: `{{ verification command }}`
**Result**: ✅ PASS ({{ X/Y }} tests)
**Coverage**: {{ coverage% }}
**Duration**: {{ test time }}
{{ else }}
⚠️ Verification skipped (--skip-verify)
{{ endif }}

═══════════════════════════════════════════════

## Plan Updated

{{ if not --no-update }}
✅ Marked complete in plan:
   `- [x] {{ task ID }}: {{ description }}`
{{ else }}
⏸️ Plan not updated (--no-update flag)
Manual update required
{{ endif }}

═══════════════════════════════════════════════

## Next Steps

**1. Review changes**:
```bash
git diff
```

**2. If satisfied, commit**:
```bash
git add .
git commit -m "{{ commit message suggestion }}"
```

**3. Continue to next task** ⚡:

{{ if next task preview }}
**Next task**: {{ next task ID }}: {{ next description }}

**Fast-track option** (recommended - saves 2-5 min):
```bash
/cook {{ plan file }} --task={{ next task ID }}
```

**Auto-resume option** (finds next task automatically):
```bash
/cook {{ plan file }} --resume
```

**Normal mode** (full discovery):
```bash
/cook {{ plan file }}
```

{{ else }}
🎉 **This was the last task!** Plan complete.

**Final verification**:
```bash
npm test
npm run build
git push
```
{{ endif }}

═══════════════════════════════════════════════
```

---

### Failure Case ❌

```markdown
═══════════════════════════════════════════════
❌ TASK FAILED

**Task**: {{ task ID }}: {{ description }}
**Phase**: {{ phase ID }}

═══════════════════════════════════════════════

## Changes Made

{{ changes summary }}

═══════════════════════════════════════════════

## Verification FAILED

**Command**: `{{ verification command }}`
**Exit Code**: {{ non-zero }}

**Errors**:
```
{{ error output }}
```

**Failed Tests**:
- {{ test 1 name }}: {{ assertion failure }}
- {{ test 2 name }}: {{ error message }}

═══════════════════════════════════════════════

{{ if --auto-fix }}
## Auto-Fix Attempted

Attempted fix:
- {{ what was tried }}

Result: ❌ Still failing

{{ endif }}

═══════════════════════════════════════════════

## Diagnosis

**Error Type**: {{ TypeScript | Test Assertion | Runtime }}
**Location**: `{{ file }}:{{ line }}`
**Cause**: {{ likely cause }}

**Suggested Fix**:
```typescript
{{ suggested code change }}
```

═══════════════════════════════════════════════

## Recovery Options

**Option 1: Fix manually**
1. Review error above
2. Edit: `{{ file path }}`
3. Re-run: `/cook {{ plan file }}`
   (Will retry same task)

**Option 2: Skip this task**
1. Mark task as [x] in plan (manual)
2. Add TODO comment about issue
3. Run: `/cook {{ plan file }}`
   (Will move to next task)

**Option 3: Rollback**
```bash
git checkout {{ files modified }}
```

═══════════════════════════════════════════════

⚠️ Plan NOT updated (task still [ ])
Task will retry on next `/cook` run

═══════════════════════════════════════════════
```

---

### Dry Run Case 🔍

```markdown
═══════════════════════════════════════════════
🔍 DRY RUN: Next Task Preview

**Task**: {{ task ID }}: {{ description }}
**Phase**: {{ phase ID }}
**Estimate**: {{ time estimate }}

═══════════════════════════════════════════════

## Files Involved

**Operation**: {{ CREATE | MODIFY | DELETE }}
**Target**: `{{ file path }}`

{{ if MODIFY }}
### Current State
- File exists: {{ size }}
- Key functions: {{ list }}

### Planned Changes
- {{ change 1 }}
- {{ change 2 }}
{{ endif }}

═══════════════════════════════════════════════

## Implementation Plan

{{ step-by-step plan }}

═══════════════════════════════════════════════

## Verification

**Command**: `{{ verification command }}`
**Expected**: {{ tests should pass }}

═══════════════════════════════════════════════

## To Execute

Remove --dry-run flag:
```bash
/cook {{ plan file }}
```

═══════════════════════════════════════════════
```

---

## Examples

### Example 1: Basic Usage

```bash
/cook plans/multi-theme.md
```

**What happens**:
1. Finds first `[ ]` task (e.g., A.1)
2. Checks for subtasks (A.1.a, A.1.b, etc.)
3. If subtasks exist → cooks first subtask (A.1.a)
4. If no subtasks → cooks main task (A.1)
5. Implements code
6. Runs tests
7. Updates plan: `[ ]` → `[x]`
8. Shows git diff suggestion
9. Stops

Developer then: `git commit` → `/cook` again

---

### Example 2: Preview Mode

```bash
/cook plans/feature.md --dry-run
```

**What happens**:
1. Shows what task would be executed
2. Previews changes
3. No files modified
4. Plan not updated

---

### Example 3: Phase-Specific

```bash
/cook plans/feature.md --phase=A
```

**What happens**:
1. Finds first `[ ]` in Phase A
2. Executes that task
3. Stops (even if Phase A has more tasks)

Run again to do next Phase A task.

---

### Example 4: Fast Mode (Skip Tests)

```bash
/cook plans/docs.md --skip-verify
```

⚠️ **Use only for low-risk tasks** (e.g., documentation)

---

### Example 5: Auto-Fix on Failure

```bash
/cook plans/refactor.md --auto-fix
```

If tests fail, attempts one auto-fix before giving up.

---

### Example 6: Subtask Workflow

```bash
# Plan has:
- [ ] A.1: Implement Authentication [Summary]
  - [ ] A.1.a: Setup dependencies [1h]
  - [ ] A.1.b: Create login logic [3h]
  - [ ] A.1.c: Add tests [2h]
- [ ] A.2: Next task

# Run 1
/cook plan.md
# → Cooks A.1.a (first subtask)
# → Marks [x] A.1.a
git commit -m "feat: setup auth dependencies (A.1.a)"

# Run 2
/cook plan.md
# → Cooks A.1.b (next subtask)
# → Marks [x] A.1.b
git commit -m "feat: create login logic (A.1.b)"

# Run 3
/cook plan.md
# → Cooks A.1.c (last subtask)
# → Marks [x] A.1.c
git commit -m "feat: add auth tests (A.1.c)"

# Run 4
/cook plan.md
# → All subtasks [x], now cooks main A.1
# → Marks [x] A.1
git commit -m "feat: complete authentication system (A.1)"

# Run 5
/cook plan.md
# → Cooks A.2 (next main task)
```

---

### Example 7: Skip Subtasks

```bash
# Plan has:
- [ ] B.1: Refactor Theme System [Summary]
  - [ ] B.1.a: Extract utilities [30m]
  - [ ] B.1.b: Update components [1h]
  - [ ] B.1.c: Add tests [30m]

# Developer knows the refactor is simple
/cook plan.md --skip-subtasks

# → Marks all B.1.x as [~] (skipped)
# → Cooks B.1 directly as one piece
# → Marks [x] B.1

# Next run
/cook plan.md
# → Goes to B.2 (next main task)
```

---

### Example 8: Fast-Track Mode

```bash
# Scenario: Continuous cooking in same conversation

# First run - needs discovery
/cook plans/feature.md
# ✅ Task A.1 complete
# Output suggests: /cook plans/feature.md --task=A.2

git commit -m "feat: task A.1"

# Second run - use suggested command (FAST! ~10 seconds vs 3 min)
/cook plans/feature.md --task=A.2
# ✅ Task A.2 complete  
# Output suggests: /cook plans/feature.md --task=A.3

git commit -m "feat: task A.2"

# Third run - even faster with auto-resume
/cook plans/feature.md --resume
# 🔍 Found last task: A.2 ✅
# ⚡ Resume point: A.3
# ✅ Task A.3 complete
```

**Time savings**: 
- Normal: 3 min + 3 min + 3 min = 9 min
- Fast-track: 3 min + 10s + 10s = ~3.5 min
- **Saved: 5.5 minutes** (60%+ faster)

---

### Example 9: Jump to Specific Task

```bash
# Skip ahead to critical task that blocks others
/cook plans/feature.md --task=C.5

# Go back to fix something without marking complete
/cook plans/feature.md --task=A.2 --no-update

# Preview specific task
/cook plans/feature.md --task=B.3 --dry-run
```

---

### Example 10: Auto-Suggest Subtasks

```bash
# Plan has large task:
- [ ] C.1: Build Admin Dashboard [8h]

/cook plan.md --suggest-split

# Output:
⚠️ LARGE TASK DETECTED

Task C.1 is estimated at 8h.
Consider breaking into subtasks:

- [ ] C.1: Build Admin Dashboard [Summary]
  - [ ] C.1.a: Create layout component [2h]
  - [ ] C.1.b: Add user table [2h]
  - [ ] C.1.c: Implement filters [2h]
  - [ ] C.1.d: Add tests [2h]

Add subtasks? [y/n/e]: y

# → Subtasks inserted into plan
# → Re-scans and starts with C.1.a
```

---

## Typical Developer Workflow

### Iteration Loop

```bash
# Iteration 1
/cook plan.md           # AI: implements A.1, tests ✅, marks [x]
git diff                # Dev: reviews changes
git commit -m "..."     # Dev: approves

# Iteration 2
/cook plan.md           # AI: implements A.2, tests ✅, marks [x]
git diff                # Dev: reviews
git commit -m "..."     # Dev: approves

# Iteration 3
/cook plan.md           # AI: implements A.3, tests ❌
# Dev: reads error, fixes manually
/cook plan.md           # AI: retries A.3, tests ✅, marks [x]
git commit -m "..."     # Dev: commits fix + implementation

# ... repeat until plan complete
```

---

## Integration

### With /plan Command

```bash
# Create plan
/plan "multi-theme" --current=docs/theme/ --tdd --output=plans/theme.md

# Execute plan
/cook plans/theme.md
# (repeat until done)
```

### With Git Workflow

```bash
# Feature branch
git checkout -b feature/multi-theme

# Cook tasks
/cook plans/theme.md
git commit -m "feat: implement CSS sanitization (A.1)"

/cook plans/theme.md
git commit -m "feat: add input validation (A.2)"

# ... continue ...

# Push when phase complete
git push origin feature/multi-theme
```

### With CI/CD

```bash
# In CI pipeline (for automated testing)
/cook test-plan.md --skip-verify  # Just implement
npm test                           # Separate test step
```

---

## Key Differences from V1

### V1 (Monolithic)
```bash
/cook plan.md --auto
# → Runs ALL 33 tasks automatically
# → 33 commits created
# → Hard to debug
# → Low control
```

### V2 (Iterator)
```bash
/cook plan.md  # Task 1
git commit
/cook plan.md  # Task 2
git commit
# ... manual iteration
# → 1 task at a time
# → Full control
# → Easy to debug
```

---

## Safety Features

1. **Idempotency**: Safe to re-run (retries current `[ ]` task)
2. **Dependency Validation**: Won't run task if deps incomplete
3. **Automatic Plan Update**: Marks `[x]` when verified
4. **Test Gate**: Stops if verification fails (unless --skip-verify)
5. **No Hidden State**: Everything visible in plan markdown
6. **Syntax Check**: Validates code before testing

---

## Success Criteria

- [ ] Finds next uncompleted task correctly
- [ ] Validates dependencies
- [ ] Implements code per spec
- [ ] Runs verification tests
- [ ] Updates plan checkbox automatically
- [ ] Stops after one task
- [ ] Handles failures gracefully
- [ ] Provides clear next steps

---

## Related Commands

- `/plan` - Create implementation plans to cook
- `/task-progress` - View overall progress dashboard
- `/task-next` - Preview next task (alternative manual approach)

---

## Pro Tips

1. **Use fast-track for continuous cooking** ⚡:
   ```bash
   # First run (needs discovery)
   /cook plan.md
   # Output suggests: /cook plan.md --task=A.2
   
   git commit -m "feat: task A.1"
   
   # Copy-paste the suggested command (saves 2-5 min)
   /cook plan.md --task=A.2
   # Output suggests: /cook plan.md --task=A.3
   
   git commit -m "feat: task A.2"
   
   # Or use auto-resume
   /cook plan.md --resume
   ```

2. **Use dry-run to preview**:
   ```bash
   /cook plan.md --dry-run
   /cook plan.md --task=A.5 --dry-run  # Preview specific task
   ```

3. **Keyboard-driven workflow** (bash/zsh):
   ```bash
   # Add to ~/.zshrc or ~/.bashrc
   function cook-next() {
     /cook "$1" --resume
   }
   
   # Usage - super fast iteration:
   cook-next plan.md  # runs next task
   git commit -m "auto"
   cook-next plan.md  # runs next task
   git commit -m "auto"
   # repeat...
   ```

4. **One-liner for rapid execution**:
   ```bash
   # Execute and commit in one go (review first!)
   /cook plan.md --resume && git add . && git commit -m "$(git diff --cached --name-only | head -1)"
   ```

5. **Focus on one phase at a time**:
   ```bash
   /cook plan.md --phase=A  # Security phase
   # Complete all Phase A
   /cook plan.md --phase=B  # Architecture phase
   ```

6. **Use --auto-fix for routine refactoring**:
   ```bash
   /cook refactor-plan.md --auto-fix --resume
   ```

7. **Check progress anytime**:
   ```bash
   /task-progress plan.md
   ```

8. **Jump to specific task when needed**:
   ```bash
   # Skip ahead to critical task
   /cook plan.md --task=B.3
   
   # Go back to fix something
   /cook plan.md --task=A.1 --no-update  # Don't mark complete again
   ```

---

**Remember**: `/cook` is an iterator, not a loop. One task, one review, one commit. Repeat. 🍳✨
