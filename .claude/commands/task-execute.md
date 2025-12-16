# /task-execute - Execute Specific Task

## Purpose

Execute a specific task from an implementation plan. This command implements the code changes, runs basic validation, and prepares for verification. Works in **interactive mode by default** - shows changes and waits for approval.

**"Code with confidence, not blind automation"** - Developer controls execution.

## Aliases

```bash
/task-execute [plan-file] --task=ID
/execute-task [plan-file] --task=ID
/te [plan-file] --task=ID
```

## Usage

```bash
# Execute specific task (interactive mode - default)
/task-execute plans/multi-theme.md --task=A.1

# Execute next uncompleted task
/task-execute plans/feature.md

# Auto mode (skip confirmations - use carefully)
/task-execute plans/routine.md --task=B.2 --auto

# Dry run (preview changes only)
/task-execute plans/feature.md --task=A.1 --dry-run
```

## Arguments

- `$ARGUMENTS`: Path to implementation plan markdown file

## Flags

| Flag | Description | Example |
|------|-------------|---------|
| `--task=ID` | Specific task to execute (required if not using next) | `--task=A.1` |
| `--auto` | Skip confirmations (dangerous, use carefully) | `--auto` |
| `--dry-run` | Show changes without applying | `--dry-run` |
| `--skip-deps-check` | Skip dependency validation | `--skip-deps-check` |

---

## Core Philosophy

**Interactive by Default**: 
- Show what will change
- Wait for developer approval
- Apply changes only after confirmation

**Developer Control**:
- Can abort at any time
- Can modify approach mid-execution
- Can manually fix before proceeding

---

## Workflow

### Step 1: Load Task & Dependencies (2-5 min)

Uses same logic as `/task-next`:

```markdown
Task Loader

GOAL: Load task details and validate readiness

STEPS:

1. {{ if --task provided }}
   Load task {{ task ID }} from plan
   {{ else }}
   Find next uncompleted task (first "- [ ]")
   {{ endif }}

2. Parse task structure:
   - File path(s)
   - Operation: CREATE | MODIFY | DELETE
   - Action description
   - Verification command

3. {{ if not --skip-deps-check }}
   Validate dependencies:
   - Check if dependency tasks marked [x]
   - {{ if any incomplete }}
     ⚠️ ERROR: Dependencies not met
     → Recommend running: /task-execute plan.md --task={{ dep ID }}
     → Or override: --skip-deps-check
     STOP
   {{ endif }}
   {{ endif }}

OUTPUT: Task object
```

---

### Step 2: Load Context (for MODIFY operations) (5-10 min)

```markdown
Context Loader

GOAL: Read existing code to understand modification scope

{{ if operation is MODIFY }}

STEPS:

1. Read target file: `{{ file path }}`

2. Analyze structure:
   - Identify key sections
   - Find modification points
   - Note patterns to preserve

3. Create modification strategy:
   - What to add
   - What to change
   - What to preserve

OUTPUT: Context + modification plan

{{ else if operation is CREATE }}

Skip (new file, no context needed)

{{ else if operation is DELETE }}

STEPS:
1. Find files that import/depend on target
2. List cleanup required

OUTPUT: Cleanup checklist

{{ endif }}
```

---

### Step 3: Generate Implementation (10-30 min depending on task)

```markdown
Code Generator

GOAL: Implement changes per task specification

{{ if CREATE }}

**Creating new file**: `{{ file path }}`

STEPS:

1. Generate file content based on:
   - Task description from plan
   - Project patterns (from context)
   - Code examples (if provided in plan)

2. Add proper:
   - Imports
   - Types (if TypeScript)
   - Exports
   - Comments for complex logic

3. Follow project conventions:
   - Formatting
   - Naming
   - File structure

OUTPUT: New file content

{{ else if MODIFY }}

**Modifying file**: `{{ file path }}`

STEPS:

1. Read current file content

2. Apply changes:
   - {{ change from task description }}
   - Preserve existing logic
   - Update imports if needed

3. Maintain patterns:
   - Consistent formatting
   - Same conventions
   - Add comments if complex

OUTPUT: Modified file content (diff)

{{ else if DELETE }}

**Deleting file**: `{{ file path }}`

STEPS:

1. Remove target file

2. Update dependent files:
   - Remove imports
   - Update references
   - Add migration comments

OUTPUT: Cleanup list

{{ endif }}
```

---

### Step 4: Preview & Confirmation (Interactive Mode)

{{ if not --auto and not --dry-run }}

```markdown
Interactive Confirmation

GOAL: Show changes and get developer approval

DISPLAY:

═══════════════════════════════════════════════
🔨 TASK EXECUTION PREVIEW

**Task**: {{ task ID }}: {{ description }}
**Operation**: {{ CREATE | MODIFY | DELETE }}
**Files**: {{ file count }}

═══════════════════════════════════════════════

{{ if CREATE }}
## File to CREATE

**Path**: `{{ file path }}`

```typescript
{{ new file content - first 50 lines }}
... ({{ remaining lines }} more lines)
```
{{ endif }}

{{ if MODIFY }}
## Changes to MAKE

**Path**: `{{ file path }}`

```diff
{{ git diff style output }}
```

**Summary**:
- {{ X }} lines added
- {{ Y }} lines modified
- {{ Z }} lines removed
{{ endif }}

{{ if DELETE }}
## File to DELETE

**Path**: `{{ file path }}`

**Impact**:
- {{ X }} files will need import updates
- {{ cleanup tasks }}
{{ endif }}

═══════════════════════════════════════════════

❓ **APPROVAL REQUIRED**

Review the changes above.

Options:
1. **Approve** - Apply changes and continue
2. **Modify** - Adjust approach (chat to explain)
3. **Skip** - Skip this task for now
4. **Abort** - Stop execution

Your choice: [1/2/3/4]

═══════════════════════════════════════════════
```

**Wait for user input**

{{ if user approves }}
→ Proceed to Step 5
{{ else if user wants modifications }}
→ Chat with user to adjust, regenerate, repeat Step 4
{{ else if user skips }}
→ End (task remains [ ] in plan)
{{ else if user aborts }}
→ Exit command
{{ endif }}

{{ endif }}

---

### Step 5: Apply Changes (2-5 min)

```markdown
Change Applicator

GOAL: Write changes to file system

{{ if not --dry-run }}

STEPS:

1. {{ if CREATE }}
   Write new file: `{{ file path }}`
   {{ else if MODIFY }}
   Update file: `{{ file path }}`
   {{ else if DELETE }}
   Delete file: `{{ file path }}`
   Update dependent files
   {{ endif }}

2. Verify file system:
   - File exists (CREATE/MODIFY)
   - File removed (DELETE)
   - Permissions correct

3. Run quick syntax check:
   - {{ if TypeScript }}
     npx tsc --noEmit {{ file path }}
   {{ else if JavaScript }}
     node --check {{ file path }}
   {{ endif }}

OUTPUT: Changes applied

{{ else }}

DRY RUN MODE: No changes written

{{ endif }}
```

---

### Step 6: Post-Execution Summary

```markdown
Execution Summary

═══════════════════════════════════════════════
✅ TASK EXECUTED

**Task**: {{ task ID }}: {{ description }}
**Duration**: {{ time taken }}

═══════════════════════════════════════════════

## Changes Applied

{{ if CREATE }}
✅ Created: `{{ file path }}` ({{ line count }} lines)
{{ else if MODIFY }}
✅ Modified: `{{ file path }}`
   - {{ added lines }} added
   - {{ modified lines }} modified
   - {{ removed lines }} removed
{{ else if DELETE }}
✅ Deleted: `{{ file path }}`
✅ Updated {{ X }} dependent files
{{ endif }}

═══════════════════════════════════════════════

## Next Steps

1. **Verify implementation**:
   ```bash
   /task-verify {{ plan file }}
   ```
   
2. **If tests pass**, mark complete:
   ```bash
   /task-done {{ plan file }} --task={{ task ID }}
   ```

3. **If tests fail**, you can:
   - Fix manually and re-verify
   - Run /task-execute again (will re-read latest code)

═══════════════════════════════════════════════

{{ if --dry-run }}
🔍 DRY RUN: No changes were actually applied
Run without --dry-run to apply changes
{{ endif }}

{{ if --auto }}
⚠️ AUTO MODE: Changes applied without confirmation
Review carefully before committing
{{ endif }}

═══════════════════════════════════════════════
```

---

## Examples

### Example 1: Interactive Execution (Default)

```bash
/task-execute plans/multi-theme.md --task=A.1
```

**Behavior**:
1. Shows what will be created/modified
2. Displays preview of changes
3. Waits for [1] Approve
4. Applies changes
5. Suggests verification command

### Example 2: Execute Next Task

```bash
/task-execute plans/feature.md
```

Finds first `[ ]` task and executes it.

### Example 3: Auto Mode (Routine Tasks)

```bash
/task-execute plans/routine.md --task=B.2 --auto
```

⚠️ **Use with caution**: Skips confirmation

### Example 4: Dry Run

```bash
/task-execute plans/critical.md --task=A.1 --dry-run
```

Shows what would happen without actually changing files.

---

## Integration

### Typical Workflow

```bash
# 1. Review next task
/task-next plan.md

# 2. Execute after review
/task-execute plan.md --task=A.1

# 3. Verify implementation  
/task-verify plan.md

# 4. Mark complete
/task-done plan.md --task=A.1
```

### Quick Execution (Trusted Tasks)

```bash
/task-execute plan.md --task=B.2 --auto && /task-verify plan.md
```

---

## Safety Features

1. **Dependency Check**: Won't execute if dependencies incomplete
2. **Interactive Confirmation**: Shows changes before applying
3. **Dry Run Mode**: Preview without risk
4. **Syntax Validation**: Quick check after changes
5. **Rollback Friendly**: Changes not committed until task-done

---

## Success Criteria

- [ ] Loads task correctly from plan
- [ ] Validates dependencies
- [ ] Loads context for MODIFY operations
- [ ] Generates appropriate code changes
- [ ] Shows preview in interactive mode
- [ ] Waits for approval before applying
- [ ] Applies changes correctly
- [ ] Suggests next steps

---

## Related Commands

- `/task-next` - Preview task before executing
- `/task-verify` - Verify implementation
- `/task-done` - Mark complete & commit
- `/task-progress` - Check overall status

---

## Pro Tips

1. **Always use interactive mode for critical code**:
   ```bash
   /task-execute security-fix.md --task=A.1
   # (interactive is default)
   ```

2. **Use --dry-run to preview**:
   ```bash
   /task-execute plan.md --task=B.3 --dry-run
   ```

3. **Auto mode only for routine tasks**:
   ```bash
   /task-execute routine.md --task=C.1 --auto
   ```

4. **Combine with next for fluid workflow**:
   ```bash
   /task-next plan.md && /task-execute plan.md
   ```

---

**Remember**: This command changes code. Always review changes in interactive mode! 🔨
