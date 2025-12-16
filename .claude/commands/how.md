# /how - Multi-Phase Codebase Exploration

## Purpose

Deep codebase exploration using a multi-phase SubAgent approach with per-phase documentation to prevent context loss. Each phase completes and documents before the next begins, ensuring comprehensive and detailed analysis.

**"How does this work?"** - Get comprehensive answers with organized documentation.

## Aliases

```bash
/how [topic]
/how-it-works [topic]
```

## Usage

```bash
# Basic usage
/how "authentication"

# With recent commits analysis
/how "payment flow" --recent=5

# With specific commit
/how "checkout" --commit=abc123

# With commit range
/how "user management" --commit=abc123..def456

# With source path
/how "payment flow" --source=old-app/payments

# Compare recent changes with plan
/how "authentication" --recent=3 --plan=plans/auth-update.md

# Custom output
/how "checkout" --output=docs/custom-analysis

# Specific phases only
/how "auth" --phases=1,2

# Comprehensive mode
/how "calculator" --comprehensive
```

## Arguments

- `$ARGUMENTS`: Feature name, component, or functionality to explore

## Flags

| Flag | Description | Example |
|------|-------------|---------|
| `--source=path` | Specify source directory to search | `--source=old-app/auth` |
| `--output=path` | Custom output folder | `--output=docs/auth-analysis` |
| `--phases=N,N` | Run specific phases only (1-2) | `--phases=1,2` |
| `--comprehensive` | Generate extra detailed reports | `--comprehensive` |
| `--skip-review` | Skip review gates between phases | `--skip-review` |
| `--recent=N` | Analyze changes from last N commits | `--recent=5` |
| `--commit=ID` | Analyze specific commit | `--commit=abc123` |
| `--commit=RANGE` | Analyze commit range | `--commit=abc123..def456` |
| `--plan=path` | Compare changes with plan file | `--plan=plans/feature.md` |

---

## Core Methodology

**Reference**: `.claude/skills/methodology/intelligent-planning/SKILL.md`
**Exploration Skill**: `.claude/skills/codebase-exploration/SKILL.md`

### Multi-Phase SubAgent Workflow

```
Phase 1: Discovery & Structure (Scout + Scout External)
    ↓ [Document NOW]
    docs/<topic>/phase-1-discovery-structure.md
    ↓ [Review Gate]
    
Phase 2: Code Analysis (Code-Reviewer + Security Auditor)
    ↓ [Document NOW]
    docs/<topic>/phase-2-analysis.md
    ✅ Complete
```

**Key Principle**: Each phase writes documentation IMMEDIATELY after completion to prevent context loss.

---

## Workflow

Exploring: **$ARGUMENTS**

{{ if --source provided }}
**Source directory**: `$SOURCE_PATH`
{{ else }}
**Source**: Auto-detect across codebase
{{ endif }}

**Output folder**: {{ if --output provided }}`$OUTPUT_PATH`{{ else }}`docs/[topic-slug]/`{{ endif }}

{{ if --phases provided }}
**Phases to run**: $PHASES
{{ else }}
**Phases to run**: All (1, 2)
{{ endif }}

{{ if --recent or --commit provided }}
**Git Analysis**:
{{ if --recent provided }}
- Last $RECENT commits
{{ endif }}
{{ if --commit provided }}
{{ if --commit contains '..' }}
- Commit range: $COMMIT
{{ else }}
- Specific commit: $COMMIT
{{ endif }}
{{ endif }}
{{ if --plan provided }}
- Plan comparison: $PLAN
{{ endif }}
{{ endif }}

---

{{ if --recent or --commit provided }}
### Pre-Phase 0: Change Analysis 🔍

**Goal**: Identify and analyze recent changes before exploration.

**Agent**: git-manager + researcher

**Steps**:

1. **Git Analysis** (git-manager):
   {{ if --recent provided }}
   - Run `git log --oneline -$RECENT` to get recent commit messages
   - Run `git diff --name-only HEAD~$RECENT..HEAD` to identify changed files
   {{ endif }}
   {{ if --commit provided }}
   {{ if --commit contains '..' }}
   - Run `git log --oneline $COMMIT` to get commit messages in range
   - Run `git diff --name-only $COMMIT` to identify changed files
   {{ else }}
   - Run `git show --name-only --format="" $COMMIT` for single commit
   {{ endif }}
   {{ endif }}

2. **Impact Assessment** (researcher):
   - Categorize changes: Business Logic, UI/UX, API, Configuration, Tests
   - Identify critical paths affected by changes
   - Detect breaking changes or risky modifications
   {{ if --plan provided }}
   - Read plan file and compare with actual changes
   - Calculate completion percentage
   {{ endif }}

3. **Change Prioritization**:
   ```
   Priority 1: Business Logic & API changes
   Priority 2: Database schema & security changes
   Priority 3: UI/UX changes
   Priority 4: Configuration & utility changes
   ```

**Output**: Change analysis report saved to `$OUTPUT_DIR/recent-changes-analysis.md`

---

{{ endif }}
### Setup: Prepare Output Folder

**Action**: Create output directory structure

```bash
# Generate topic slug from $ARGUMENTS
TOPIC_SLUG=$(echo "$ARGUMENTS" | tr '[:upper:]' '[:lower:]' | tr ' ' '-')

# Set output path
{{ if --output provided }}
OUTPUT_DIR="$OUTPUT_PATH"
{{ else }}
OUTPUT_DIR="docs/$TOPIC_SLUG"
{{ endif }}

# Create directory
mkdir -p "$OUTPUT_DIR"
```

**Created folder**: `$OUTPUT_DIR/`

---

### Phase 1: Discovery & Structure 🔍🏗️

**Primary Agent**: Scout (`.claude/agents/scout.md`)
**Secondary Agent**: Scout External (`.claude/agents/scout-external.md`)
**Methodology Reference**: `.claude/skills/codebase-exploration/SKILL.md`

**Goal**: Find all code related to the topic AND map architecture, dependencies, and external context.

**Duration**: 10-20 minutes

---

**Execution Steps**:

1. **Dispatch Scout Agent**:
   - **Instruction**: "Find all code related to '$ARGUMENTS' and analyze its structure, architecture, and dependencies. The scout agent will automatically trigger the codebase-exploration skill for comprehensive analysis."
   - **Context**:
     - Argument: "$ARGUMENTS"
     - Source: {{ if --source }}$SOURCE_PATH{{ else }}Auto-detected{{ endif }}
     - Mode: {{ if --comprehensive }}Comprehensive{{ else }}Standard{{ endif }}

3. **External Context Check** (Agent: Scout External):
   - **Trigger**: If `package.json` or imports show specific external libraries key to the feature (e.g., Auth0, Stripe, React Query).
   - **Action**: Run `scout-external` to fetch docs/patterns for that library if not well-known.
   - **Integration**: Start this in parallel if possible, or immediately after file inventory.

4. **Report Generation**:
   - SubAgent returns findings with comprehensive discovery report including file inventory, architecture mapping, and dependency analysis.

---

**Main Agent Action: Document Phase 1**

**Immediately write documentation**: `$OUTPUT_DIR/phase-1-discovery-structure.md`

The scout agent will provide the report structure following the codebase-exploration methodology.

---

{{ if not --skip-review }}
**Review Gate 1**: Verify Completeness
- All files found?
- Architecture mapped?
- External context added (if needed)?
-> If No: Re-run Scout.
-> If Yes: Proceed to Phase 2.
{{ endif }}

---

### Phase 2: Code Analysis 💻

**Primary Agent**: Code-Reviewer (`.claude/agents/code-reviewer.md`)
**Secondary Agents**: Security Auditor, Database Admin
**Methodology Reference**: `.claude/skills/codebase-exploration/SKILL.md`

**Goal**: Deep-dive into implementation details, business logic, safety, and patterns.

**Duration**: 20-30 minutes

---

**Execution Steps**:

1. **Dispatch Code-Reviewer Agent**:
   - **Instruction**: "Perform deep analysis of the code identified in Phase 1. Focus on business logic, implementation details, security considerations, and data patterns. The scout agent will have already triggered the codebase-exploration skill which coordinates the multi-agent analysis workflow."
   - **Context**:
     - Input: Phase 1 findings
     - Target: Deep analysis of business logic and safety

3. **Specialized Checks** (Delegation):
   - **Security Check**: Use `security-auditor` if sensitive logic (auth, payments, PII) is identified.
     - *Task*: Check for vulnerabilities in the identified files.
   - **Database Check**: Use `database-admin` if schema definitions/migrations are involved.
     - *Task*: detailed schema review.

4. **Report Generation**:
   - SubAgent returns findings with detailed analysis of business logic, security considerations, data models, and implementation patterns.

---

**Main Agent Action: Document Phase 2**

**Immediately write documentation**: `$OUTPUT_DIR/phase-2-analysis.md`

The code reviewer will provide the analysis report following the codebase-exploration methodology.

---

{{ if not --skip-review }}
**Review Gate 2**: Verify Analysis
- Business logic captured?
- Security risks identified?
- Data models clear?
-> If Yes: Complete Command.
{{ endif }}

---

## Completion

**Final Output**:
- `$OUTPUT_DIR/README.md` (Overview & Index)
- `$OUTPUT_DIR/phase-1-discovery-structure.md`
- `$OUTPUT_DIR/phase-2-analysis.md`

### Post-Exploration Actions

After `/how` completes:

1. **Apply Patterns**: `/apply "$ARGUMENTS" --to="new-feature"`
2. **Extend Feature**: `/extend "$ARGUMENTS" --with="new-capability"`
3. **Generate Tests**: `/test-from "$ARGUMENTS"`
4. **Refactor**: `/refactor-from "$ARGUMENTS"`

---

**Pro Tip**: The `/how` command leverages these skills for consistent analysis:
- **codebase-exploration**: Core methodology and agent coordination
- **exploration-documentation**: Documentation generation patterns
- **exploration-examples**: Real-world examples and workflows

## Examples

For detailed examples, see: `.claude/skills/methodology/exploration-examples/SKILL.md`

Quick examples:
```bash
# Explore authentication feature
/how "authentication"

# Analyze recent changes
/how "cart" --recent=5

# Deep dive with external research
/how "stripe integration" --comprehensive --include-external

# Explore specific directory
/how "user profile" --source=src/features/users
```

## Related Skills

- **codebase-exploration**: Multi-phase agent methodology
- **pattern-analysis**: Extract patterns for `/apply` command
- **documentation-synthesis**: Create comprehensive docs
