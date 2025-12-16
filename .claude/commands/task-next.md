# /task-next - Show Next Task

## Purpose

Display the next uncompleted task from an implementation plan, analyze its requirements, and prepare a plan of action. Does NOT execute code - only shows what needs to be done.

**"Scout before you build"** - Understand the task before implementing.

## Aliases

```bash
/task-next [plan-file]
/next-task [plan-file]
/tn [plan-file]
```

## Usage

```bash
# Show next uncompleted task
/task-next plans/multi-theme.md

# Preview without loading context
/task-next plans/feature.md --preview

# Show specific task
/task-next plans/feature.md --task=B.3

# Show next task in specific phase
/task-next plans/feature.md --phase=A
```

## Arguments

- `$ARGUMENTS`: Path to implementation plan markdown file

## Flags

| Flag | Description | Example |
|------|-------------|---------|
| `--preview` | Quick preview without deep context loading | `--preview` |
| `--task=ID` | Show specific task instead of next | `--task=A.1` |
| `--phase=ID` | Find next task in specific phase | `--phase=B` |
| `--show-context` | Show related files that will be modified | `--show-context` |

---

## Core Philosophy

**Single Source of Truth**: Read directly from plan markdown
- Find first `- [ ]` task (uncompleted)
- Read task details (File, Action, Verify, Dependencies)
- Load context from existing code if MODIFY operation
- Output clear plan of action

**No State Mutation**: This command only READS, never writes

---

## Workflow

### Step 1: Parse Plan & Find Next Task (2-5 min)

```markdown
Plan Parser

GOAL: Find next uncompleted task from plan

INPUT:
- Plan file: $ARGUMENTS
- Flags: {{ flags }}

---

LOGIC:

1. Read plan markdown file

2. {{ if --task provided }}
   Find task with ID: $TASK_ID
   {{ else if --phase provided }}
   Find first uncompleted task in Phase $PHASE_ID
   {{ else }}
   Find first uncompleted task (starts with "- [ ]")
   {{ endif }}

3. Parse task structure:
   ```markdown
   ### A.1: Task Name [Estimate]
   - **File**: `path/to/file.ts`
   - **Action**: What to do
   - **Depends on**: (optional)
   - **Verify**: How to test
   ```

4. Extract:
   - Task ID (e.g., A.1)
   - Description
   - File path(s)
   - Operation type: CREATE | MODIFY | DELETE
   - Estimate
   - Dependencies (if any)
   - Verification command

OUTPUT: Task object
```

---

### Step 2: Validate Dependencies (1-2 min)

```markdown
Dependency Checker

GOAL: Ensure dependencies are met

{{ if task has dependencies }}
STEPS:
1. Read dependency tasks from plan
2. Check if marked [x] (completed)
3. {{ if any dependency incomplete }}
   ⚠️ WARNING: Dependencies not met
   - Task {{ dep ID }}: NOT COMPLETE
   → Recommend completing dependencies first
   {{ else }}
   ✅ All dependencies met
   {{ endif }}
{{ else }}
No dependencies
{{ endif }}

OUTPUT: Dependency status
```

---

### Step 3: Load Context (5-10 min for MODIFY, skip for CREATE)

{{ if not --preview and operation is MODIFY }}

```markdown
Context Loader

GOAL: Understand current code before suggesting changes

STEPS:

1. Read target file: `{{ file path }}`

2. Understand current implementation:
   - File structure
   - Existing patterns (React component, utility, type def)
   - Dependencies (imports)
   - Key functions/classes

3. {{ if --show-context }}
   Identify related files:
   - Files that import this file
   - Files imported by this file
   - Test files
   {{ endif }}

4. Note potential modification points:
   - Where to add new code
   - What existing code might be affected
   - Potential conflicts

OUTPUT: Context summary
```

{{ else }}

Skip context loading (CREATE operation or --preview mode)

{{ endif }}

---

### Step 4: Generate Plan of Action (3-5 min)

```markdown
Action Planner

GOAL: Create clear implementation plan for this task

STEPS:

1. Analyze task requirements from plan

2. Based on operation type:
   
   {{ if CREATE }}
   **Creating new file**: `{{ file path }}`
   - Determine file structure
   - Identify necessary imports
   - Plan initial implementation
   
   {{ else if MODIFY }}
   **Modifying existing**: `{{ file path }}`
   - Changes needed: {{ from plan Action }}
   - Current state: {{ from context }}
   - Modification strategy:
     * Preserve existing logic: [what to keep]
     * Add new logic: [what to add]
     * Update imports/exports: [what to change]
   
   {{ else if DELETE }}
   **Deleting file**: `{{ file path }}`
   - Files that depend on this: [list]
   - Cleanup required: [imports, references]
   {{ endif }}

3. Identify verification strategy:
   - Test command: {{ from plan }}
   - Expected outcome
   - Potential issues

4. Estimate confidence:
   - High: Straightforward implementation
   - Medium: Some complexity
   - Low: Significant unknowns

OUTPUT: Implementation plan
```

---

## Output Format

```markdown
═══════════════════════════════════════════════
📋 NEXT TASK

**Task**: {{ task ID }}: {{ description }}
**Phase**: {{ phase ID }}
**Estimate**: {{ time estimate }}
**Status**: {{ Ready | Blocked }}

═══════════════════════════════════════════════

## Dependencies

{{ if dependencies }}
{{ for each dependency }}
- {{ dep ID }}: {{ ✅ Complete | ⏸️ Incomplete }}
{{ endfor }}
{{ else }}
No dependencies
{{ endif }}

═══════════════════════════════════════════════

## Files Involved

**Operation**: {{ CREATE | MODIFY | DELETE }}
**Target**: `{{ file path }}`

{{ if MODIFY and not --preview }}
### Current State
```typescript
// Relevant excerpts from current file
{{ code snippet }}
```

**Key observations**:
- {{ observation 1 }}
- {{ observation 2 }}
{{ endif }}

{{ if --show-context }}
### Related Files
- `{{ related file 1 }}` (imports this)
- `{{ related file 2 }}` (imported by this)
- `{{ test file }}` (tests for this)
{{ endif }}

═══════════════════════════════════════════════

## Implementation Plan

{{ if CREATE }}
**Create new file**: `{{ path }}`

**Structure**:
```typescript
{{ proposed structure }}
```

**Implementation steps**:
1. {{ step 1 }}
2. {{ step 2 }}
3. {{ step 3 }}

{{ else if MODIFY }}
**Modify existing**: `{{ path }}`

**Changes required**:
1. {{ change 1 }}
2. {{ change 2 }}

**Code sections to update**:
- Line {{ X-Y }}: {{ what to change }}
- Add new {{ function/component }}: {{ where }}

**Preserve** (do not modify):
- {{ critical logic to keep }}

{{ else if DELETE }}
**Delete file**: `{{ path }}`

**Impact analysis**:
- {{ X }} files import this
- Cleanup required in: {{ list }}

**Migration steps**:
1. {{ step 1 }}
2. {{ step 2 }}
{{ endif }}

═══════════════════════════════════════════════

## Verification

**Command**: `{{ verification command from plan }}`

**Expected outcome**:
- {{ expected result }}

**Potential issues**:
- {{ potential issue 1 }}
- {{ potential issue 2 }}

═══════════════════════════════════════════════

## Confidence Level

{{ if high confidence }}
✅ **HIGH CONFIDENCE**
- Straightforward implementation
- Clear requirements
- Well-defined scope
{{ else if medium confidence }}
⚠️ **MEDIUM CONFIDENCE**
- Some complexity involved
- May need iterations
- Watch for edge cases
{{ else }}
🔴 **LOW CONFIDENCE**
- Significant unknowns
- Complex integration
- Recommend research first
{{ endif }}

═══════════════════════════════════════════════

## Next Steps

1. Review this plan
2. If approved, execute:
   ```bash
   /task-execute {{ plan file }} --task={{ task ID }}
   ```
3. After implementation, verify:
   ```bash
   /task-verify {{ plan file }}
   ```
4. Mark complete:
   ```bash
   /task-done {{ plan file }} --task={{ task ID }}
   ```

═══════════════════════════════════════════════
```

---

## Examples

### Example 1: Next Task (Auto-detect)

```bash
/task-next plans/multi-theme.md
```

**Output**:
```markdown
📋 NEXT TASK

**Task**: A.1: Implement CSS Sanitization
**Phase**: A (Security Fixes)
**Estimate**: 5 hours
**Status**: Ready

Files Involved:
- CREATE: `src/lib/theme-security.ts`

Implementation Plan:
1. Install dompurify dependency
2. Create sanitization functions
3. Export sanitize API
...
```

### Example 2: Specific Task

```bash
/task-next plans/feature.md --task=B.3
```

Shows task B.3 even if earlier tasks incomplete.

### Example 3: Quick Preview

```bash
/task-next plans/feature.md --preview
```

Skips context loading for speed.

---

## Integration

### With Other Commands

```bash
# Typical workflow
/task-next plan.md           # Review next task
/task-execute plan.md --task=A.1  # Execute if approved
/task-verify plan.md         # Verify implementation
/task-done plan.md --task=A.1     # Mark complete
```

### With IDE

```bash
# VSCode command
"Show Next Task": "/task-next ${activeWorkspace}/plans/current.md"
```

---

## Success Criteria

- [ ] Correctly finds next uncompleted task
- [ ] Parses task structure from plan
- [ ] Validates dependencies
- [ ] Loads context for MODIFY operations
- [ ] Generates clear implementation plan
- [ ] Provides confidence assessment
- [ ] Shows clear next steps

---

## Related Commands

- `/task-execute` - Execute the task
- `/task-verify` - Verify implementation
- `/task-done` - Mark task complete
- `/task-progress` - Show overall progress
- `/plan` - Create implementation plans

---

## Pro Tips

1. **Always run task-next before task-execute**:
   ```bash
   /task-next plan.md && /task-execute plan.md
   ```

2. **Use --preview for quick overview**:
   ```bash
   /task-next plan.md --preview
   ```

3. **Check dependencies explicitly**:
   ```bash
   /task-next plan.md --task=B.3
   # Shows if A.1, A.2 are incomplete
   ```

4. **Review context before complex modifications**:
   ```bash
   /task-next plan.md --show-context
   ```

---

**Remember**: This command only shows what to do. Use `/task-execute` to actually implement! 🔍
