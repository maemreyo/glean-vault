# /plan - Implementation Planning from Exploration Docs

## Purpose

Generate comprehensive implementation plans by combining current-state documentation (from `/how`) with new implementation guides. Delegates all analysis and planning to specialized agents for organized, context-efficient execution.

**"Plan from knowledge, not guesswork"** - Build plans on documented understanding.

## Aliases

```bash
/plan [description] --current=[path] --guide=[path]
/create-plan [description] --current=[path] --guide=[path]
```

## Usage

```bash
# Basic usage (requires both current state and guide)
/plan "implement multi-theme system" \
  --current=temp/theme-system/ \
  --guide=temp/theme-system/extensions/multi-theme-guide.md

# With custom output
/plan "migrate to OAuth" \
  --current=docs/authentication/ \
  --guide=docs/authentication/extensions/oauth-guide.md \
  --output=plans/oauth-migration/

# With summary document
/plan "add dark mode" --current=docs/theme/ --guide=docs/dark-mode.md --summary

# Preview only (no file creation)
/plan "refactor payment" --current=docs/payment/ --guide=docs/stripe-v3.md --preview
```

## Arguments

- `$ARGUMENTS`: Brief description of what to plan (e.g., "implement multi-theme system")

## Flags

| Flag | Description | Example |
|------|-------------|---------|
| `--current=path` | Path to current-state docs (from `/how`) | `--current=docs/theme-system/` |
| `--guide=path` | Path to new implementation guide | `--guide=extensions/multi-theme.md` |
| `--output=path` | Output folder for plan | `--output=plans/theme-migration/` |
| `--summary` | Generate summary doc (via agent) | `--summary` |
| `--preview` | Preview plan without file creation | `--preview` |
| `--skip-review` | Skip review gates between phases | `--skip-review` |

---

## Core Methodology

**Reference Skills**:
- `.claude/skills/codebase-exploration/SKILL.md` (Phase 1)
- `.claude/skills/methodology/intelligent-planning/SKILL.md` (Phase 3)

### Multi-Agent Workflow

```
Phase 1: SCOUT (Load Documents) → Review Gate →
Phase 2: RESEARCHER (Gap Analysis) → Review Gate →
Phase 3: PLANNER (Create Plan) → Review Gate →
Phase 4: DOCS-MANAGER (Summary - Optional)
```

Each phase dispatches a **fresh subagent** with clear goals, subtasks, and expected outputs.

---

## Workflow

Planning: **$ARGUMENTS**

**Current state docs**: `{{ if --current }}$CURRENT_PATH{{ else }}ERROR: --current required{{ endif }}`
**Implementation guide**: `{{ if --guide }}$GUIDE_PATH{{ else }}ERROR: --guide required{{ endif }}`
**Output folder**: `{{ if --output }}$OUTPUT_PATH{{ else }}plans/[generated-slug]/{{ endif }}`

---

### Setup: Validate Inputs & Create Output Folder

**Steps**:

1. **Validate required flags**:
   ```bash
   {{ if not --current }}
   echo "❌ ERROR: --current flag required"
   echo "💡 Usage: /plan \"description\" --current=docs/feature/ --guide=path/to/guide.md"
   exit 1
   {{ endif }}
   
   {{ if not --guide }}
   echo "❌ ERROR: --guide flag required"
   echo "💡 Usage: /plan \"description\" --current=docs/feature/ --guide=path/to/guide.md"
   exit 1
   {{ endif }}
   ```

2. **Create output folder**:
   ```bash
   PLAN_SLUG=$(echo "$ARGUMENTS" | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | head -c 30)
   
   {{ if --output }}
   OUTPUT_DIR="$OUTPUT_PATH"
   {{ else }}
   OUTPUT_DIR="plans/$PLAN_SLUG"
   {{ endif }}
   
   mkdir -p "$OUTPUT_DIR"
   ```

---

### Phase 1: Load Documents 📖

**Agent**: Scout (`.claude/agents/scout.md`)
**Skill Trigger**: `codebase-exploration` (auto-triggered for document analysis)

**Goal**: Read and synthesize current-state docs and implementation guide into structured context.

**Duration**: 5-10 minutes

---

**Dispatch Scout Agent**:

```markdown
Scout Agent - Document Loading

GOAL: Load and synthesize all relevant documentation for planning "$ARGUMENTS"

INPUT:
- Current state docs: $CURRENT_PATH
- Implementation guide: $GUIDE_PATH

---

SUBTASK 1.1: Load Current State (5 min)

**Steps**:
1. Read `$CURRENT_PATH/phase-1-discovery-structure.md`
2. Read `$CURRENT_PATH/phase-2-analysis.md`
3. Read `$CURRENT_PATH/README.md` (if exists)
4. Extract:
   - File inventory (current files)
   - Architecture (patterns, state management)
   - Dependencies (internal & external)
   - Business logic highlights
   - Known issues or tech debt

**Output**: Structured current state summary

---

SUBTASK 1.2: Load Implementation Guide (5 min)

**Steps**:
1. Read guide file: $GUIDE_PATH
2. Extract:
   - Proposed changes
   - New patterns or architecture
   - Required dependencies
   - Migration steps (if any)
   - Success criteria

**Output**: Structured guide summary

---

SUBTASK 1.3: Create Merged Context (3 min)

**Steps**:
1. Combine current state + guide into unified context
2. Highlight overlapping areas
3. Note potential conflicts

**Output**: Write to $OUTPUT_DIR/context.md

---

OUTPUT FORMAT:

```markdown
# Loaded Context

## Current State Summary
[From /how output]

### File Inventory
- [list of current files]

### Architecture
- Pattern: [pattern name]
- State: [state management]

### Key Business Logic
- [critical rules]

---

## Implementation Guide Summary
[From guide document]

### Proposed Changes
- [list of changes]

### New Dependencies
- [new packages or libs]

### Success Criteria
- [list of criteria]

---

## Overlap Analysis
- Area 1: [current] vs [proposed]
- Area 2: [current] vs [proposed]
```
```

**Return**: Context document path

---

{{ if not --skip-review }}
**Review Gate 1**: Context Loaded
- Current state captured?
- Guide understood?
- Overlaps identified?
→ If Yes: Proceed to Phase 2
→ If No: Re-run Scout with clarifications
{{ endif }}

---

### Phase 2: Gap Analysis 🔍

**Agent**: Researcher (`.claude/agents/researcher.md`)

**Goal**: Compare current state vs. desired state, identify what needs to change.

**Duration**: 10-15 minutes

---

**Dispatch Researcher Agent**:

```markdown
Researcher Agent - Gap Analysis

GOAL: Analyze gaps between current state and desired implementation for "$ARGUMENTS"

INPUT:
- Context document: $OUTPUT_DIR/context.md
- Original guide: $GUIDE_PATH

---

SUBTASK 2.1: Identify Changes Required (5-10 min)

**Steps**:
1. For each area in the guide, determine:
   - What exists and can be reused?
   - What needs modification?
   - What must be created from scratch?
   - What should be removed?

2. Categorize changes:
   - 🔴 BREAKING: Changes that affect existing functionality
   - 🟡 SIGNIFICANT: Major additions or modifications
   - 🟢 MINOR: Small tweaks or additions

**Output**: Change categorization

---

SUBTASK 2.2: Identify Risks & Blockers (5 min)

**Steps**:
1. Technical risks:
   - Breaking changes
   - Complex migrations
   - Performance concerns
2. Blockers:
   - Missing dependencies
   - Required research
   - External approvals needed
3. Mitigations:
   - Fallback strategies
   - Incremental rollout options

**Output**: Risk assessment

---

SUBTASK 2.3: Estimate Effort (5 min)

**Steps**:
1. For each change category, estimate:
   - Small (S): < 1 hour
   - Medium (M): 1-4 hours
   - Large (L): > 4 hours
2. Calculate total estimate range

**Output**: Effort breakdown

---

OUTPUT FORMAT:

```markdown
# Gap Analysis

## Changes Required

### Files to CREATE (New)
| File | Purpose | Effort |
|------|---------|--------|
| path/to/new.ts | Description | M |

### Files to MODIFY
| File | Changes | Effort |
|------|---------|--------|
| path/to/existing.ts | What changes | S |

### Files to DELETE
| File | Reason |
|------|--------|
| path/to/old.ts | Replaced by X |

---

## Risks & Blockers

### 🔴 High Risk
- [Risk description] → Mitigation: [strategy]

### 🟡 Medium Risk
- [Risk description] → Mitigation: [strategy]

### Blockers
- [Blocker] → Resolution: [action needed]

---

## Effort Estimate

| Category | Count | Effort |
|----------|-------|--------|
| Create | X files | Y hours |
| Modify | X files | Y hours |
| Delete | X files | 30 min |
| **Total** | | **Z hours** |
```
```

**Return**: Gap analysis path: $OUTPUT_DIR/gap-analysis.md

---

{{ if not --skip-review }}
**Review Gate 2**: Gap Analysis Complete
- All changes identified?
- Risks assessed?
- Estimates reasonable?
→ If Yes: Proceed to Phase 3
→ If No: Re-analyze specific areas
{{ endif }}

---

### Phase 3: Create Implementation Plan 📋

**Agent**: Planner (`.claude/agents/planner.md`)
**Skill Trigger**: `intelligent-planning`, `writing-plans`

**Goal**: Create detailed, actionable implementation plan with phased tasks.

**Duration**: 15-20 minutes

---

**Dispatch Planner Agent**:

```markdown
Planner Agent - Implementation Planning

GOAL: Create detailed implementation plan for "$ARGUMENTS"

INPUT:
- Context: $OUTPUT_DIR/context.md
- Gap Analysis: $OUTPUT_DIR/gap-analysis.md
- Original guide: $GUIDE_PATH

CONSTRAINTS:
- Tasks must be 15-60 minutes each
- Dependencies must be clear
- Each task must be verifiable
- Include testing for each phase

---

SUBTASK 3.1: Design Phase Structure (5 min)

**Steps**:
1. Group changes into logical phases:
   - Phase A: Foundation (types, configs, dependencies)
   - Phase B: Core Implementation (main logic)
   - Phase C: Integration (connect to existing code)
   - Phase D: Testing (unit, integration)
   - Phase E: Documentation & Cleanup

**Output**: Phase outline

---

SUBTASK 3.2: Create Detailed Tasks (10-15 min)

**Steps**:
1. For each phase, create atomic tasks:
   - Clear action description
   - File path(s) involved
   - Acceptance criteria
   - Effort estimate (S/M/L)
   - Dependencies on other tasks

2. Use superpowers methodology:
   - Break into 2-5 minute subtasks where possible
   - Include expected outputs
   - Add verification steps

**Output**: Task list per phase

---

SUBTASK 3.3: Create TodoWrite Format (5 min)

**Steps**:
1. Convert tasks to TodoWrite-compatible format
2. Add IDs for dependency tracking
3. Include verification checkboxes

**Output**: tasks.md

---

OUTPUT FORMAT:

Write to $OUTPUT_DIR/implementation.md:

```markdown
# Implementation Plan: $ARGUMENTS

## Overview
[2-3 sentence summary]

## Scope
- **In Scope**: [what will be done]
- **Out of Scope**: [what won't be done]

---

## Phase A: Foundation (Est: X hours)

### A.1: [Task Name] [S]
- **File**: `path/to/file.ts`
- **Action**: [what to do]
- **Verify**: [how to verify]

### A.2: [Task Name] [M]
- **File**: `path/to/file.ts`
- **Action**: [what to do]
- **Depends on**: A.1
- **Verify**: [how to verify]

---

## Phase B: Core Implementation (Est: X hours)
[...]

---

## Phase C: Integration (Est: X hours)
[...]

---

## Phase D: Testing (Est: X hours)
[...]

---

## Phase E: Documentation (Est: X hours)
[...]

---

## Verification Checklist

- [ ] All Phase A tasks complete
- [ ] All Phase B tasks complete
- [ ] All tests passing
- [ ] Documentation updated
- [ ] No breaking changes to existing functionality
```

Write to $OUTPUT_DIR/tasks.md:

```markdown
# Tasks

## Phase A: Foundation
- [ ] A.1: [Task description] [S]
- [ ] A.2: [Task description] [M] (depends: A.1)

## Phase B: Core Implementation
- [ ] B.1: [Task description] [M]
[...]
```
```

**Return**: Plan paths

---

{{ if not --skip-review }}
**Review Gate 3**: Plan Complete
- Tasks are atomic and verifiable?
- Dependencies are clear?
- Estimates are reasonable?
→ If Yes: {{ if --summary }}Proceed to Phase 4{{ else }}Complete{{ endif }}
→ If No: Refine specific sections
{{ endif }}

---

{{ if --summary }}
### Phase 4: Generate Summary 📝

**Agent**: Docs-Manager (`.claude/agents/docs-manager.md`)

**Goal**: Create executive summary for stakeholders.

**Duration**: 5-10 minutes

---

**Dispatch Docs-Manager Agent**:

```markdown
Docs-Manager Agent - Summary Generation

GOAL: Create concise executive summary for "$ARGUMENTS" implementation

INPUT:
- Implementation plan: $OUTPUT_DIR/implementation.md
- Gap analysis: $OUTPUT_DIR/gap-analysis.md

---

TASK: Write Executive Summary

**Content**:
1. **Overview**: What will be implemented (2-3 sentences)
2. **Key Changes**: Bullet list of major changes
3. **Timeline**: Estimated total effort
4. **Risks**: Top 3 risks with mitigations
5. **Success Criteria**: How to validate completion

**Style**:
- Concise (max 1 page)
- Non-technical language where possible
- Actionable next steps

---

OUTPUT: Write to $OUTPUT_DIR/summary.md

```markdown
# Summary: $ARGUMENTS

## Overview
[Brief description of what will be implemented]

## Key Changes
- [Change 1]
- [Change 2]
- [Change 3]

## Timeline
- **Estimated Effort**: X-Y hours
- **Phases**: 5 (Foundation → Implementation → Integration → Testing → Docs)

## Top Risks
1. [Risk 1] → [Mitigation]
2. [Risk 2] → [Mitigation]
3. [Risk 3] → [Mitigation]

## Success Criteria
- [ ] [Criterion 1]
- [ ] [Criterion 2]
- [ ] [Criterion 3]

## Next Steps
1. Review this plan
2. Run `/execute-plan $OUTPUT_DIR/tasks.md`
3. Monitor progress
```
```

**Return**: Summary path

{{ endif }}

---

{{ if --preview }}
### Preview Mode 👁️

**Display plan summary without creating files**

```markdown
📋 PLAN PREVIEW

Planning: "$ARGUMENTS"

Current State: $CURRENT_PATH
Guide: $GUIDE_PATH

---

Phases:
1. Foundation: ~X tasks
2. Implementation: ~Y tasks
3. Integration: ~Z tasks
4. Testing: ~N tasks
5. Documentation: ~M tasks

Estimated Total: X-Y hours

---

To create this plan:
/plan "$ARGUMENTS" --current=$CURRENT_PATH --guide=$GUIDE_PATH
(remove --preview flag)
```

**END** (no file creation)

{{ else }}

---

## Completion

```markdown
✅ PLAN CREATED

Planning for: "$ARGUMENTS"

Output folder: $OUTPUT_DIR/

---

## Generated Files

📁 $OUTPUT_DIR/
├── README.md           # Overview & Navigation
├── context.md          # Loaded context (Phase 1)
├── gap-analysis.md     # Gap analysis (Phase 2)
├── implementation.md   # Detailed plan (Phase 3)
├── tasks.md            # TodoWrite-compatible tasks
{{ if --summary }}
└── summary.md          # Executive summary (Phase 4)
{{ endif }}

---

## Next Steps

1. **Review the plan**:
   ```bash
   cat $OUTPUT_DIR/implementation.md
   ```

2. **Execute the plan**:
   ```bash
   /execute-plan "$OUTPUT_DIR/tasks.md"
   ```

3. **Track progress**:
   - Check off tasks as completed
   - Update $OUTPUT_DIR/README.md with status

---

🎯 Plan ready for execution!
```

{{ endif }}

---

## Success Criteria

- [ ] Current state docs loaded
- [ ] Implementation guide analyzed
- [ ] Gap analysis complete
- [ ] Detailed plan created
- [ ] Tasks are actionable
- [ ] Output files generated

---

## Examples

### Example 1: Theme System Migration

```bash
/plan "implement multi-theme system" \
  --current=temp/theme-system/ \
  --guide=temp/theme-system/extensions/multi-theme-guide.md \
  --output=plans/multi-theme/ \
  --summary
```

**Output**:
```
Loading docs from temp/theme-system/...
Reading implementation guide...

Gap Analysis:
- 3 files to CREATE
- 5 files to MODIFY
- 0 files to DELETE
- Estimated: 8-12 hours

Creating plan...

✅ Plan created at plans/multi-theme/
- implementation.md (detailed plan)
- tasks.md (45 tasks)
- summary.md (executive summary)
```

### Example 2: OAuth Migration

```bash
/plan "migrate to OAuth 2.0" \
  --current=docs/authentication/ \
  --guide=docs/auth/oauth-migration-guide.md
```

---

## Related Commands

- `/how` - Generate current-state docs first
- `/execute-plan` - Execute the generated plan
- `/extend` - Simpler extension without full planning
