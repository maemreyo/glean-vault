# /task-cook - Automated Task Execution (Convenience Wrapper)

## Purpose

Convenience wrapper that automates the full task workflow: execute → verify → commit. **Use with caution** - this is the "auto mode" for routine, low-risk tasks.

**"Automate the routine, control the critical"** - Fast-forward through simple tasks.

## Aliases

```bash
/task-cook [plan-file]
/cook [plan-file]
/tc [plan-file]
```

## Usage

```bash
# Cook single task (with confirmation)
/task-cook plans/routine.md --task=C.2

# Cook entire phase (confirms each task)
/task-cook plans/routine.md --phase=D

# Full auto mode (DANGEROUS - no confirmations)
/task-cook plans/routine.md --task=E.1 --auto

# Cook until failure (stops on first error)
/task-cook plans/feature.md --until-fail
```

## Arguments

- `$ARGUMENTS`: Path to implementation plan markdown file

## Flags

| Flag | Description | Example |
|------|-------------|---------|
| `--task=ID` | Cook specific task | `--task=C.2` |
| `--phase=ID` | Cook entire phase | `--phase=D` |
| `--auto` | Skip all confirmations (DANGEROUS) | `--auto` |
| `--until-fail` | Continue until first failure | `--until-fail` |
| `--max-tasks=N` | Limit number of tasks | `--max-tasks=3` |

---

## ⚠️ WARNING

**This command combines**:
1. `/task-execute` (implements code)
2. `/task-verify` (runs tests)
3. `/task-done` (commits changes)

**Use only for**:
- Low-risk tasks
- Routine updates
- Well-tested patterns

**Do NOT use for**:
- Security fixes
- Critical business logic
- Complex integrations
- First-time implementations

---

## Core Philosophy

**Convenience ≠ Careless**:
- Still validates dependencies
- Still runs tests
- Still creates atomic commits
- But: Less human oversight

**Interactive by Default**:
- Shows preview before each task
- Waits for confirmation
- `--auto` mode is opt-in

---

## Workflow

### For Each Task:

```markdown
Task Cooker Loop

STEP 1: Load Next Task
- Find next uncompleted `[ ]` task
- Validate dependencies

STEP 2: Execute
{{ if not --auto }}
- Show implementation preview
- Wait for confirmation: [Y/n/skip]
{{ endif }}
- Run: /task-execute (inline)

STEP 3: Verify
{{ if not --auto }}
- Show test results
- If fail: [retry/fix-manually/skip]
{{ endif }}
- Run: /task-verify (inline)

STEP 4: Commit
{{ if verification passed }}
- Run: /task-done (inline)
- Mark [x] in plan
- Git commit
{{ else }}
STOP (unless --until-fail and user chooses skip)
{{ endif }}

STEP 5: Continue or Stop
{{ if --phase and more tasks in phase }}
Continue to next task
{{ else if --until-fail and no error }}
Continue to next task
{{ else if --max-tasks not reached }}
Continue to next task
{{ else }}
STOP
{{ endif }}
```

---

## Output Example

```markdown
═══════════════════════════════════════════════
🍳 COOKING TASKS

**Plan**: plans/routine.md
**Mode**: {{ Interactive | Auto }}
**Target**: {{ Single task | Phase X | Until fail }}

═══════════════════════════════════════════════

## Task 1/3: D.1 - Update Documentation

📋 Loading task...
✅ Dependencies met
✅ Execution complete (src/docs/ updated)
✅ Tests passed (5/5)
✅ Committed: abc1234 "docs: update documentation (D.1)"

⏱️ Duration: 2m 15s

---

## Task 2/3: D.2 - Add API Examples

📋 Loading task...
✅ Dependencies met

🔨 **Implementation Preview**:
- CREATE: examples/api-usage.ts
- Estimated changes: 120 lines

⏸️ Approve? [Y/n/skip]: _

{{ wait for user input }}

{{ if Y }}
✅ Execution complete
✅ Tests passed (3/3)
✅ Committed: def5678 "docs: add API examples (D.2)"

⏱️ Duration: 3m 45s
{{ endif }}

---

## Task 3/3: D.3 - Update README

... (similar flow)

═══════════════════════════════════════════════

✅ COOKING COMPLETE

**Tasks Completed**: 3/3
**Duration**: 8m 30s
**Commits**: 3

**Next**: Phase E or manual work

═══════════════════════════════════════════════
```

---

## Examples

### Example 1: Cook Single Task

```bash
/task-cook plans/routine.md --task=D.2
```

Executes + verifies + commits task D.2 with confirmation.

### Example 2: Cook Entire Phase

```bash
/task-cook plans/docs.md --phase=E
```

Cooks all tasks in Phase E, confirming each.

### Example 3: Auto Mode (DANGEROUS)

```bash
/task-cook plans/simple.md --task=C.1 --auto
```

⚠️ **No confirmations, full automation.**

### Example 4: Cook Until Failure

```bash
/task-cook plans/feature.md --until-fail --max-tasks=10
```

Cooks up to 10 tasks or until first failure.

---

## When to Use

✅ **Good for**:
- Documentation updates
- Simple refactoring
- Adding tests
- Code formatting
- Config file updates

❌ **Bad for**:
- Security fixes
- Database migrations
- API changes
- Authentication logic
- Payment processing

---

## Safety Features

1. **Dependency Validation**: Won't cook if deps incomplete
2. **Test Gate**: Stops if verification fails
3. **Interactive Default**: Confirms before each task
4. **Atomic Commits**: One task = one commit
5. **Max Tasks Limit**: Prevents runaway execution

---

## Comparison with Manual Workflow

### Manual (Full Control)

```bash
/task-next plan.md
/task-execute plan.md --task=A.1
/task-verify plan.md
/task-done plan.md --task=A.1
# Repeat for each task
```

**Time**: 4 commands × 3 tasks = 12 commands
**Control**: Maximum

### Automated (task-cook)

```bash
/task-cook plan.md --phase=A
```

**Time**: 1 command (3 confirmations if interactive)
**Control**: Moderate (can abort mid-phase)

### Full Auto (DANGER)

```bash
/task-cook plan.md --phase=A --auto
```

**Time**: 1 command, 0 confirmations
**Control**: Minimal

---

## Integration

### In CI/CD

```bash
# For automated testing
/task-cook test-plan.md --auto --max-tasks=5
exit_code=$?
```

### For Bulk Updates

```bash
# Cook all documentation tasks
/task-cook plan.md --phase=E  # (Phase E = Docs)
```

---

## Success Criteria

- [ ] Executes tasks in sequence
- [ ] Validates dependencies
- [ ] Shows preview in interactive mode
- [ ] Runs verification after each task
- [ ] Creates git commits
- [ ] Stops on failure (unless --until-fail)
- [ ] Respects --max-tasks limit

---

## Related Commands

- `/task-next` - Manual approach (step 1)
- `/task-execute` - Manual approach (step 2)
- `/task-verify` - Manual approach (step 3)
- `/task-done` - Manual approach (step 4)
- `/task-progress` - Check status

---

## Pro Tips

1. **Test on routine tasks first**:
   ```bash
   /task-cook plan.md --task=E.1  # Documentation task
   ```

2. **Never use --auto on critical code**:
   ```bash
   # ❌ NEVER
   /task-cook security-fix.md --auto
   
   # ✅ ALWAYS
   /task-execute security-fix.md --task=A.1  # Manual
   ```

3. **Use --max-tasks for safety**:
   ```bash
   /task-cook plan.md --until-fail --max-tasks=5
   # Won't cook more than 5 even if all pass
   ```

4. **Monitor first cooking run**:
   ```bash
   /task-cook plan.md --phase=D  # Watch closely first time
   ```

---

**Remember**: Automation is powerful but dangerous. When in doubt, go manual! 🍳⚠️
