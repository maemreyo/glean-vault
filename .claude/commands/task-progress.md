# /task-progress - Show Progress Dashboard

## Purpose

Display comprehensive progress dashboard for implementation plan. Shows completion status, time tracking, and phase breakdown. Read-only visualization command.

**"Know where you stand"** - Clear visibility into plan execution.

## Aliases

```bash
/task-progress [plan-file]
/progress [plan-file]
/tp [plan-file]
```

## Usage

```bash
# Show full progress dashboard
/task-progress plans/multi-theme.md

# Specific phase only
/task-progress plans/feature.md --phase=A

# Compact format
/task-progress plans/feature.md --compact

# JSON output (for scripts)
/task-progress plans/feature.md --format=json
```

## Arguments

- `$ARGUMENTS`: Path to implementation plan markdown file

## Flags

| Flag | Description | Example |
|------|-------------|---------|
| `--phase=ID` | Show specific phase only | `--phase=A` |
| `--compact` | Compact table view | `--compact` |
| `--format=FORMAT` | Output format: table\|json\|markdown | `--format=json` |

---

## Output Format

```markdown
═══════════════════════════════════════════════
📊 PROGRESS DASHBOARD

**Plan**: {{ plan filename }}
**Last Updated**: {{ timestamp }}

═══════════════════════════════════════════════

## Overall Progress

████████████░░░░░░░░ 60% (20/33 tasks)

- **Total Tasks**: 33
- **Completed**: 20 ✅
- **In Progress**: 1 ⏳ ({{ current task ID }})
- **Remaining**: 12 ⏸️
- **Estimated Remaining**: ~15-20 hours

═══════════════════════════════════════════════

## Phase Breakdown

### Phase A: Security Fixes ✅
████████████████████ 100% (3/3 tasks)
- **Status**: Complete
- **Time**: 10h 15m
- **Last Task**: A.3 (completed {{ timestamp }})

### Phase B: Architecture Migration ⏳
████████████░░░░░░░░ 67% (4/6 tasks)
- **Status**: In Progress
- **Time**: 8h 30m (est. 6h remaining)
- **Current**: B.5 - Add Dark Mode
- **Remaining**: B.5, B.6

### Phase C: Component Updates ⏸️
░░░░░░░░░░░░░░░░░░░░ 0% (0/8 tasks)
- **Status**: Not Started
- **Est. Time**: 8-12 hours
- **Next**: C.1 - Update Header Component

### Phase D: Performance ⏸️
░░░░░░░░░░░░░░░░░░░░ 0% (0/5 tasks)

### Phase E: Documentation ⏸️
░░░░░░░░░░░░░░░░░░░░ 0% (0/4 tasks)

═══════════════════════════════════════════════

## Recent Activity

- ✅ B.4: Updated Components (2h ago)
- ✅ B.3: Migrated Theme Provider (4h ago)
- ✅ B.2: Updated CSS Structure (6h ago)
- ✅ B.1: Created ThemeManager (8h ago)

═══════════════════════════════════════════════

## Git Commits

**Total**: 20 commits created
**Latest**: abc1234 "feat: update components (B.4)"

View all commits:
```bash
git log --oneline --grep="(A|B|C|D|E)\.[0-9]"
```

═══════════════════════════════════════════════

## Next Steps

**Current Task**: B.5 - Add Dark Mode (3h est.)
**After That**: B.6, C.1, C.2...

**Resume work**:
```bash
/task-next {{ plan file }}
/task-execute {{ plan file }}
```

═══════════════════════════════════════════════
```

---

## Related Commands

- `/task-next` - Show next task details
- `/task-execute` - Execute tasks
- `/task-verify` - Verify implementation
- `/task-done` - Mark complete

---

**Quick snapshot of where you are in the plan! 📊**
