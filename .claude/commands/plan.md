# /plan - Intelligent Implementation Planning (V3)

## Purpose

Generate comprehensive implementation plans by intelligently combining current-state documentation (from `/how`), implementation guides, or auto-exploration. Leverages multi-agent workflow with fresh context per phase for optimal planning quality.

**"Plans built on knowledge, not assumptions"** - Smart planning through structured analysis.

## Aliases

```bash
/plan [description]
/create-plan [description]
```

## Usage

```bash
# Basic planning (auto-explores if no docs)
/plan "implement multi-theme support"

# With current state documentation
/plan "multi-theme system" --current=temp/theme-system/

# With implementation guide
/plan "multi-theme system" --guide=temp/theme-system/extensions/multi-theme-guide.md

# With both (ideal for migrations)
/plan "multi-theme system" \
  --current=temp/theme-system/ \
  --guide=temp/theme-system/extensions/multi-theme-guide.md

# TDD micro-tasks (2-5 min)
/plan "authentication" --tdd

# With custom output
/plan "feature" --current=docs/feature/ --output=plans/feature.md --summary

# Auto-explore mode
/plan "user dashboard" --auto-explore --type=react
```

## Arguments

- `$ARGUMENTS`: Feature or task description to plan

## Flags

| Flag | Description | Example |
|------|-------------|---------|
| `--current=path` | Path to current-state docs (from `/how`) - Optional | `--current=docs/theme/` |
| `--guide=path` | Path to implementation guide - Optional | `--guide=extensions/multi-theme.md` |
| `--output=path` | Save detailed plan to file | `--output=plans/feature.md` |
| `--summary` | Generate concise summary (via Docs-Manager) | `--summary` |
| `--tdd` | Use TDD micro-tasks (2-5 min) | `--tdd` |
| `--auto-explore` | Auto-explore codebase if no current state | `--auto-explore` |
| `--type=TYPE` | Type hint: react/api/utility/component | `--type=react` |
| `--skip-review` | Skip review gates (faster, less safe) | `--skip-review` |

---

## Core Philosophy

1. **Flexible Inputs**: No longer requires both --current and --guide
2. **TDD Support**: --tdd flag for 2-5 min micro-tasks
3. **Strategy Selection**: Intelligent choice of planning approach
4. **Requirements-Driven**: MUST/SHOULD/COULD categorization
5. **Fresh Context**: Each phase gets a clean subagent
6. **Clear Names**: Scout, Researcher, Planner (not generic names)

---

## Workflow Overview

Planning: **$ARGUMENTS**

{{ if --current provided }}
**Current state**: `$CURRENT_PATH`
{{ else if --auto-explore }}
**Mode**: Auto-exploration
{{ else }}
**Mode**: Fresh planning
{{ endif }}

{{ if --guide provided }}
**Implementation guide**: `$GUIDE_PATH`
{{ endif }}

{{ if --tdd }}
**Task size**: TDD micro-tasks (2-5 minutes)
{{ else }}
**Task size**: Standard tasks (15-60 minutes)
{{ endif }}

**Output**: {{ if --output }}$OUTPUT_PATH{{ else }}Display in chat{{ endif }}

---

## Agent Workflow (6 Phases)

### Phase 0: Setup & Mode Detection (5 min)

**Main Agent**: Setup coordinator

```markdown
GOAL: Determine planning mode and validate inputs

DETECTION LOGIC:

{{ if --current and --guide }}
MODE: Full Context Planning
- Current state available
- Implementation guide available
- Best case scenario
{{ else if --current }}
MODE: Extension Planning
- Current state available
- Will infer new requirements
{{ else if --guide }}
MODE: Greenfield with Guide
- Implementation guide available
- No current constraints
{{ else if --auto-explore }}
MODE: Auto-Exploration
- Will explore codebase first
- Then plan based on findings
{{ else }}
MODE: Fresh Feature Planning
- Decompose from requirements
- No existing context
{{ endif }}

OUTPUT: Selected mode → Dispatch to Phase 1
```

---

### Phase 1: Load Current State (10-15 min)

**Agent**: Scout (`.claude/agents/scout.md`)
**Skill**: `codebase-exploration` (auto-triggered)

{{ if --current provided }}

**Dispatch Scout Agent**:

```markdown
Scout Agent - Current State Loading

GOAL: Extract comprehensive understanding from `/how` documentation

INPUT:
- Documentation: $CURRENT_PATH
- Feature: "$ARGUMENTS"

---

SUBTASK 1.1: Read Discovery Phase (5 min)

1. Read `phase-1-discovery-structure.md`
2. Extract:
   - File inventory
   - Architecture patterns
   - Dependencies
   - Integration points

SUBTASK 1.2: Read Analysis Phase (5 min)

1. Read `phase-2-analysis.md`
2. Extract:
   - Current capabilities
   - Business logic
   - Patterns used
   - Known issues
   - Tech debt

SUBTASK 1.3: Synthesize (5 min)

Create structured summary:

```markdown
## Current State

### Files & Architecture
- Components: [list]
- State: [management approach]
- APIs: [endpoints]

### Capabilities
- Implemented: [features]
- Missing: [gaps]

### Tech Debt
- [issues]
```

OUTPUT: Current state context

---

SUBTASK 1.4: Extract Verification Commands (3 min)

{{ if --current }}
**Steps**:
1. Read project `package.json` from root
2. Extract test-related scripts from `scripts` section:
   - test*
   - lint*
   - type-check*
   - build*
   - coverage*

3. Identify verification patterns:
   - Unit tests: `npm test`, `jest`, `vitest`
   - Integration: patterns with "integration"
   - E2E: `cypress`, `playwright`
   - Type checking: `tsc`, `type-check`
   - Linting: `eslint`, `lint`
   - Build: `build`, `compile`

4. Create verification commands inventory:

```markdown
## Available Verification Commands

### From package.json
- `npm test` - Run all tests
- `npm run type-check` - TypeScript validation
- `npm run lint:fix` - Code style check
- `npm run build` - Production build
- `npm test -- --coverage` - Coverage report

### Patterns for Specific Tests
- Feature tests: `npm test {feature-name}`
- Path-specific: `npm run type-check {path}`
- Watch mode: `npm test -- --watch=false`
```

OUTPUT: Verification commands for Planner
{{ else }}
**Infer from project type**:
- JavaScript/TypeScript → npm test, tsc
- Python → pytest
- Go → go test
- Rust → cargo test
{{ endif }}
```

{{ else if --auto-explore }}

**Trigger Auto-Exploration**:

Use `intelligent-planning` skill with `--auto-explore` mode:
- 3-phase exploration
- Fresh subagent per phase
- Quality gates

{{ else }}

**Skip to Phase 2** (no current state to load)

{{ endif }}

---

{{ if not --skip-review and --current }}
**Review Gate 1**: Current State Loaded
- Architecture understood?
- Capabilities documented?
→ Proceed to Phase 2
{{ endif }}

---

### Phase 2: Solution Analysis (10-15 min)

**Agent**: Researcher (`.claude/agents/researcher.md`)

{{ if --guide provided }}

**Dispatch Researcher Agent**:

```markdown
Researcher Agent - Solution Analysis

GOAL: Extract implementation strategy from guide

INPUT:
- Guide: $GUIDE_PATH
- Current state: [from Phase 1, if available]
- Target: "$ARGUMENTS"

---

SUBTASK 2.1: Parse Guide (10 min)

1. Identify proposed architecture
2. Extract implementation steps
3. Note prerequisites
4. Identify code patterns

SUBTASK 2.2: Extract Requirements (5 min)

1. New components needed
2. API changes required
3. Configuration updates
4. Testing requirements

SUBTASK 2.3: Integration Analysis (5 min)

{{ if --current }}
1. Map to current state
2. Identify modifications needed
3. Backward compatibility checks
{{ else }}
1. Identify dependencies
2. Note integration points
{{ endif }}

OUTPUT: Implementation strategy
```

{{ else }}

**Skip to Phase 3** (no guide provided)

{{ endif }}

---

{{ if not --skip-review and --guide }}
**Review Gate 2**: Solution Understood
- Guide parsed correctly?
- Requirements extracted?
→ Proceed to Phase 3
{{ endif }}

---

### Phase 3: Requirements & Gap Analysis (15-20 min)

**Agent**: Analyst (delegate to Researcher with requirements focus)

**Dispatch Analyst Subagent**:

```markdown
Analyst Subagent - Requirements Extraction

GOAL: Define clear, prioritized requirements

INPUT:
- Current state: [from Phase 1, if available]
- Solution guide: [from Phase 2, if available]
- Feature: "$ARGUMENTS"

---

SUBTASK 3.1: Requirements Definition (10 min)

{{ if --current and --guide }}
**Gap Analysis Approach**:
1. Map current → desired state
2. Identify missing pieces
3. Categorize changes:
   - 🔴 MUST: Critical functionality
   - 🟡 SHOULD: Important features  
   - 🟢 COULD: Nice-to-haves

{{ else if --current }}
**Extension Approach**:
1. Analyze what exists
2. Infer new requirements from "$ARGUMENTS"
3. Categorize by impact

{{ else if --guide }}
**Guided Approach**:
1. Extract requirements from guide
2. Prioritize based on dependencies
3. Add acceptance criteria

{{ else }}
**Feature Decomposition**:
1. Break "$ARGUMENTS" into epics
2. Create user stories
3. Define acceptance criteria
4. Prioritize: MUST/SHOULD/COULD
{{ endif }}

SUBTASK 3.2: Technical Requirements (5-10 min)

1. Architecture decisions
2. Components: CREATE/MODIFY/DELETE
3. API endpoints required
4. Database changes
5. Testing strategy

OUTPUT: Complete requirements specification

```markdown
## Requirements

### 🔴 MUST Have (Critical)
- REQ-1: [description]
- REQ-2: [description]

### 🟡 SHOULD Have (Important)
- REQ-3: [description]

### 🟢 COULD Have (Nice-to-have)
- REQ-4: [description]

---

## Technical Requirements

### Files to CREATE
| File | Purpose | Estimate |
|------|---------|----------|
| path/to/new.ts | Description | M |

### Files to MODIFY
| File | Changes | Estimate |
|------|---------|----------|
| path/to/existing.ts | What changes | S |

### Files to DELETE
| File | Reason |
|------|--------|
| path/to/old.ts | Replaced by X |

---

## Architecture Decisions
1. [Decision 1]
2. [Decision 2]

---

## Risks
- 🔴 [High risk] → Mitigation: [strategy]
- 🟡 [Medium risk] → Mitigation: [strategy]
```
```

---

{{ if not --skip-review }}
**Review Gate 3**: Requirements Complete
- All requirements defined?
- Prioritization clear?
- Technical reqs specified?
→ Proceed to Phase 4
{{ endif }}

---

### Phase 4: Planning Strategy Selection (5 min)

**Main Agent**: Strategy selector

```markdown
GOAL: Choose optimal planning approach

INPUT:
- Requirements: [from Phase 3]
- Flags: {{ if --tdd }}TDD requested{{ endif }}
- Complexity: [assess from requirements]

---

STRATEGY OPTIONS:

1. **Standard Planning** (default)
   - Task size: 15-60 minutes
   - Best for: Experienced teams, straightforward features
   - Skill: `intelligent-planning` (standard mode)

2. **TDD Micro-Planning** (--tdd flag)
   - Task size: 2-5 minutes
   - Best for: Complex features, learning, high quality
   - Skill: `writing-plans` (superpowers methodology)
   - Pattern: Test → Implement → Verify → Commit

3. **Auto-Exploration Planning** (--auto-explore)
   - First: 3-phase exploration
   - Then: Comprehensive planning
   - Best for: Unknown codebases
   - Skill: `intelligent-planning` (full mode)

---

DECISION:

{{ if --tdd }}
SELECTED: TDD Micro-Planning
- 2-5 minute tasks
- Complete code samples
- Exact file paths
- TDD workflow
{{ else if --auto-explore }}
SELECTED: Auto-Exploration
- Explore → Analyze → Plan
- Multi-subagent workflow
{{ else }}
SELECTED: Standard Planning
- 15-60 minute tasks
- Clear acceptance criteria
{{ endif }}

OUTPUT: Strategy for Phase 5
```

---

### Phase 5: Plan Generation (30-60 min)

**Agent**: Planner (`.claude/agents/planner.md`)
**Skills**: Context-dependent

**Dispatch Planner Agent**:

```markdown
Planner Agent - Implementation Plan Creation

GOAL: Generate execution-ready implementation plan

INPUT:
- Requirements: [complete specification from Phase 3]
- Current state: [from Phase 1, if available]
- Solution guide: [from Phase 2, if available]
- Strategy: [selected in Phase 4]

---

{{ if --tdd }}
METHODOLOGY: writing-plans skill (TDD micro-tasks)

TASK STRUCTURE:
- Size: 2-5 minutes each
- Format: Test → Implement → Verify → Commit
- Include: Exact file paths, complete code samples
- Verify: Expected test outputs

{{ else if --auto-explore }}
METHODOLOGY: intelligent-planning skill (comprehensive)

PROCESS:
- 3-phase subagent exploration
- Quality gates between phases
- Comprehensive documentation

{{ else }}
METHODOLOGY: intelligent-planning skill (standard)

TASK STRUCTURE:
- Size: 15-60 minutes
- Clear acceptance criteria
- File paths included
- Context references
{{ endif }}

---

VERIFICATION COMMANDS INTEGRATION:

INPUT from Phase 1:
- Available test commands: {{ from Scout SUBTASK 1.4 }}
- Project conventions: {{ inferred }}

USAGE in Tasks:

FOR EACH task, select appropriate verification:

1. **Identify task type**:
   - CREATE new feature → feature-specific test
   - MODIFY existing → affected module test
   - DELETE → dependent modules tests
   - EXECUTE → command validation

2. **Select verification command**:
   {{ if CREATE and has unit test }}
   - **Verify**: `npm test {feature-name}`
   {{ else if CREATE and TypeScript }}
   - **Verify**: `npm run type-check {file-path}`
   {{ else if MODIFY }}
   - **Verify**: `npm test {module-name}`
   {{ else if DELETE }}
   - **Verify**: `npm test` (ensure no breaks)
   {{ else if task is BUILD/DEPLOY }}
   - **Verify**: `npm run build`
   {{ endif }}

3. **Fallback strategy** (if no specific test):
   - TypeScript: `npm run type-check`
   - Any JS/TS: `npm run lint:fix`
   - Last resort: `npm run build`

**CRITICAL RULES**:

❌ NEVER use vague commands:
- "Check if it works"
- "Test manually"
- "Verify functionality"

✅ ALWAYS use runnable commands:
- `npm test theme-security`
- `npm run type-check src/types/theme.ts`
- `npm run build`
- `npm test -- --coverage`

---

TASK COMPLEXITY DETECTION:

FOR EACH planned task:

1. **Estimate complexity**:
   - Simple: < 30 min
   - Medium: 30 min - 2 hours
   - Complex: 2-4 hours
   - Very Complex: > 4 hours

2. {{ if estimate > 4 hours }}
   **AUTO-SPLIT into subtasks**:
   
   Example:
   ```markdown
   - [ ] A.1: Build Admin Dashboard [8h] → SPLIT INTO:
   
   - [ ] A.1: Build Admin Dashboard [Summary]
     - [ ] A.1.a: Create layout component [2h]
       - **File**: `src/components/admin/Layout.tsx`
       - **Action**: CREATE
       - **Verify**: `npm test admin/Layout`
     
     - [ ] A.1.b: Add user table [2h]
       - **File**: `src/components/admin/UserTable.tsx`
       - **Action**: CREATE
       - **Verify**: `npm test admin/UserTable`
     
     - [ ] A.1.c: Implement filters [2h]
       - **File**: `src/components/admin/Filters.tsx`
       - **Action**: CREATE
       - **Verify**: `npm test admin/Filters`
     
     - [ ] A.1.d: Add tests [2h]
       - **File**: `src/components/admin/__tests__/`
       - **Action**: CREATE
       - **Verify**: `npm test admin -- --coverage`
   ```
   {{ endif }}

3. {{ if --tdd }}
   **TDD micro-split** (2-5 min each):
   - Red: Write failing test
   - Green: Make it pass
   - Refactor: Clean up
   {{ endif }}

---

DEPENDENCY ANALYSIS:

FOR EACH task, identify and add dependencies:

1. **Analyze task relationships**:
   - Sequential file operations: CREATE then MODIFY -> dependency
   - Same file modifications: Later tasks depend on earlier
   - Build on previous output: Explicit dependency needed
   - Phase relationships: Phase B depends on Phase A completion

2. **Common dependency patterns**:
   
   **Pattern 1: File creation chain**
   ```markdown
   - [ ] A.1: Create base types
     - **File**: `types.ts`
     - **Action**: CREATE
   
   - [ ] A.2: Create utilities  
     - **File**: `utils.ts`
     - **Action**: CREATE
     - **Depends on**: A.1  # Uses types from A.1
   ```
   
   **Pattern 2: Subtask dependencies**
   ```markdown
   - [ ] B.1: Implement feature [Summary]
     - [ ] B.1.a: Install deps
       - **Action**: MODIFY package.json
     
     - [ ] B.1.b: Create code
       - **Action**: CREATE
       - **Depends on**: B.1.a  # Needs deps installed
   ```
   
   **Pattern 3: Cross-phase dependencies**
   ```markdown
   - [ ] B.1: Migrate architecture
     - **Depends on**: A.3  # Needs security fixes complete
   ```

3. **Automatic dependency detection**:
   {{ if task modifies file that was created in previous task }}
   - Add **Depends on**: {previous task ID}
   {{ endif }}
   
   {{ if task in Phase B and Phase A has tasks }}
   - Add **Depends on**: Last task of Phase A
   {{ endif }}
   
   {{ if subtask uses output from sibling subtask }}
   - Add **Depends on**: {sibling task ID}
   {{ endif }}

4. **Validation rules**:
   - Circular dependencies: NOT allowed (error)
   - Forward references: NOT allowed (A.2 can't depend on A.3)
   - Missing dependencies: WARN planner to add

---

CRITICAL OUTPUT FORMAT REQUIREMENTS:

**Task Format** (MANDATORY for cook.md compatibility):
```markdown
- [ ] {Phase}.{Number}: {Description} [{Estimate}]
  - **File**: `{path/to/file.ext}` (comma-separated if multiple)
  - **Action**: {CREATE | MODIFY | DELETE | EXECUTE}
  - **Verify**: {exact npm/shell command}
  - **Expected**: {concrete success criteria}
  - **Depends on**: {Task IDs, optional}
  - **Issues**: (optional, for complex tasks)
    {Problem description} -> {Solution}
    {Another issue} -> {Fix}
```

**Subtask Format** (when task > 4h or --tdd):
```markdown
- [ ] A.1: Main Task [Summary]
  - [ ] A.1.a: Subtask One [Estimate]
    - **File**: `{path}`
    - **Action**: {type}
    - **Verify**: {command}`
    - **Expected**: {result}
    - **Depends on**: A.1.a (if applicable)
  - [ ] A.1.b: Subtask Two [Estimate]
    - **File**: `{path}`
    - **Action**: {type}
    - **Verify**: {command}
    - **Expected**: {result}
    - **Depends on**: A.1.a
```

**Action Type Rules**:
- `CREATE`: New files that don't exist yet
- `MODIFY`: Changes to existing files
- `DELETE`: Removing files
- `EXECUTE`: Commands only (no file changes), e.g., "Run full test suite"

**Verification Rules**:
1. MUST be runnable shell command (not description)
2. Use specific patterns when possible: `npm test {specific-test}`
3. If no test exists, use: `npm run type-check` or `npm run build`
4. For phase completion: `npm test -- --coverage`

**Expected Output Rules** (NEW - MANDATORY):
1. MUST include concrete success criteria
2. Use measurable metrics: test counts, coverage %, time limits
3. Format examples:
   - `15/15 tests pass, coverage >95%`
   - `0 TypeScript errors, build successful`
   - `Bundle size <500KB, <16ms execution`
   - `All security tests pass, 0 vulnerabilities`

**Dependency Rules**:
1. MUST include if task uses output from previous task
2. Format: Single ID `A.1` or multiple `A.1, A.2, B.3`
3. For subtasks: `A.1.a` references sibling subtask
4. cook.md will validate dependencies before execution

**Common Issues Field** (OPTIONAL but recommended for complex tasks):
1. Use for tasks with known failure modes
2. Format: `{Problem} -> {Solution}` (one per line)
3. Keep concise, actionable
4. Examples:
   ```markdown
   - **Issues**:
     DOMPurify install fails -> npm install --legacy-peer-deps
     TypeScript errors -> Add @types/dompurify to devDependencies
     Build size increase -> Enable tree-shaking in build config
   ```

**Subtask Rules**:
1. Use when:
   - Task estimate > 4 hours
   - --tdd flag is set
   - Task has distinct implementation phases
2. Format: Parent ID + lowercase letter (A.1.a, A.1.b, A.1.c)
3. Indent with 2 spaces
4. Each subtask needs full metadata (File, Action, Verify, Expected)

---

**ASCII-FIRST FORMATTING GUIDELINES**:

Use ASCII symbols instead of Unicode for better compatibility and token efficiency:

| Instead of | Use | Meaning |
|------------|-----|---------|
| ✓ ✅ | [x] | Completed/Success |
| ❌ | [X] | Error/Failed |
| 🔴 | [!] | Critical/MUST |
| 🟡 | [~] | Important/SHOULD |
| 🟢 | [?] | Optional/COULD |
| ⚠️ | [!] | Warning |
| → | -> | Arrow/Flow |
| ↓ | \| v | Vertical chain |

**Diagram Guidelines**:
- Use ASCII art for dependency chains
- Tree structures: `+--` for branches, `|` for trunk
- Flow: `->` for horizontal, `|` and `v` for vertical
- Boxes: Use `+---+` or `===` for headers

**Example ASCII Diagram**:
```
PHASE DEPENDENCY CHAIN:

  [A] Security (12h)
   |--- BLOCKS: All other phases
   v
  [B] Architecture (18h)
   |--- REQUIRES: A complete
   v
  [C] Performance (8h)
   |
   v
  [D] Features  --|
  [E] Testing   --|--> Can run parallel
   |            --|
   v
  [F] Docs (3h)
   
CRITICAL PATH: A -> B -> C -> F
```

---

PLAN STRUCTURE:

## 1. Executive Summary
- Feature: "$ARGUMENTS"
- Time estimate: X-Y hours
- Risk level: Low/Medium/High
- Success criteria

## 2. Current State (if available)
- What exists
- What's working well
- Integration points

## 3. Verification Commands Reference

> **Note**: Use these commands in task **Verify** fields

{{ if --current }}
### Available Commands (from package.json)

| Command | Purpose | When to Use |
|---------|---------|-------------|
| `npm test {pattern}` | Run specific tests | After implementing feature code |
| `npm run type-check {path}` | TypeScript validation | After creating/modifying types |
| `npm run lint:fix` | Code style check | After any code changes |
| `npm run build` | Production build | After major changes |
| `npm test -- --coverage` | Coverage report | After completing phase |
{{ else }}
### Inferred Commands (for this project type)

| Command | Purpose |
|---------|----------|
| `npm test` | Assumed test runner |
| `npm run type-check` | If TypeScript detected |
| `npm run build` | Standard build |
{{ endif }}

### Common Verification Patterns

**For CREATE tasks** (new files):
```bash
npm run type-check src/path/to/new-file.ts
npm test new-feature -- --watch=false
```

**For MODIFY tasks** (existing files):
```bash
npm test affected-module
npm run lint:fix
```

**For PHASE completion**:
```bash
npm test -- --coverage
npm run build
```

---

## 4. Implementation Phases

### Phase A: Foundation (Est: X hours)

{{ if --tdd }}
- [ ] A.1: Create basic structure [15m]
  - **File**: `src/components/Component.tsx`
  - **Action**: CREATE
  - **Verify**: `npm run type-check src/components/Component.tsx`
  - **Expected**: 0 TypeScript errors, file created successfully
  
  - [ ] A.1.a: Write test skeleton [5m]
    - **File**: `src/components/__tests__/Component.test.tsx`
    - **Action**: CREATE
    - **Verify**: `npm test Component -- --watch=false`
    - **Expected**: Test file runs, 0/1 tests pass (expected TDD red)
  
  - [ ] A.1.b: Implement component to pass test [10m]
    - **File**: `src/components/Component.tsx`
    - **Action**: MODIFY
    - **Verify**: `npm test Component -- --watch=false --coverage`
    - **Expected**: 1/1 tests pass, coverage >80%
    - **Depends on**: A.1.a

- [ ] A.2: Add component props validation [10m]
  - **File**: `src/components/Component.tsx`
  - **Action**: MODIFY
  - **Verify**: `npm test Component`
  - **Expected**: All prop validation tests pass
  - **Depends on**: A.1
  
  - [ ] A.2.a: Write prop types test [5m]
    - **File**: `src/components/__tests__/Component.test.tsx`
    - **Action**: MODIFY
    - **Verify**: `npm test Component`
  
  - [ ] A.2.b: Implement validation [5m]
    - **File**: `src/components/Component.tsx`
    - **Action**: MODIFY
    - **Verify**: `npm test Component -- --coverage`

{{ else }}
- [ ] A.1: Create type definitions [30m]
  - **File**: `src/types/theme.ts`
  - **Action**: CREATE
  - **Verify**: `npm run type-check src/types/`
  - **Expected**: 0 TypeScript errors, all exports available

- [ ] A.2: Set up configuration [45m]
  - **File**: `src/config/theme.ts`
  - **Action**: CREATE
  - **Verify**: `npm test theme-config`
  - **Expected**: 8/8 tests pass, no runtime errors
  - **Depends on**: A.1
  - **Issues**:
    Import errors -> Check tsconfig paths
    Type mismatches -> Ensure A.1 exports correct types
{{ endif }}

### Phase B: Core Implementation
[... detailed tasks ...]

### Phase C: Integration  
[... detailed tasks ...]

### Phase D: Testing
[... detailed tasks ...]

### Phase E: Documentation
[... detailed tasks ...]

---

## 5. Cross-Cutting Concerns

{{ if --current }}
### Preservation Requirements
- [ ] Existing feature X unchanged
- [ ] Backward compatibility maintained
- [ ] No breaking changes to public API
{{ endif }}

### Testing Strategy
- Unit tests: {{ coverage target, e.g., 80% }}
- Integration tests: {{ key scenarios }}
- E2E tests: {{ critical flows }}

### Documentation Updates
- [ ] README.md updates
- [ ] API documentation
- [ ] User guides
- [ ] Migration guide (if breaking changes)

---

## 6. Verification Checklist
- [ ] All Phase A tasks complete
- [ ] All Phase B tasks complete
- [ ] All Phase C tasks complete
- [ ] All Phase D tasks complete
- [ ] All Phase E tasks complete
- [ ] All tests passing
- [ ] No breaking changes (or documented)
- [ ] Documentation updated
- [ ] Code review completed
- [ ] Ready for `/cook` execution

---

**EXECUTION INSTRUCTIONS**:

Once plan is approved:
```bash
# Execute with cook iterator
/cook {{ output path }}

# Or view progress
/task-progress {{ output path }}

# Or manual approach
/task-next {{ output path }}
/task-execute {{ output path }} --task=A.1
```

---

**CRITICAL: WRITE PLAN TO FILE**

BEFORE showing output, Planner agent MUST:

1. **Determine output file**:
   ```
   {{ if --output }}
   FILE_PATH = $OUTPUT_PATH
   {{ else }}
   FILE_PATH = ./implementation-plan.md (current directory)
   {{ endif }}
   ```

2. **Write complete plan to file**:
   ```
   WRITE_FILE(FILE_PATH, complete_plan_markdown)
   ```

3. **Verify file written**:
   ```
   if FILE_EXISTS(FILE_PATH):
     ✅ Success: Plan written
   else:
     ❌ ERROR: File write failed
     STOP - Do not proceed to OUTPUT
   ```

4. **Only after file is written**: Proceed to OUTPUT summary

**This is NOT optional. Plan file MUST exist before showing summary.**

---

OUTPUT: Plan file path + summary
```

---

{{ if not --skip-review }}
**Review Gate 4**: Plan Quality Check
- Tasks are atomic?
- Dependencies clear?
- Estimates reasonable?
→ Proceed to Phase 6 or Complete
{{ endif }}

---

### Phase 6: Summary Generation (10 min)

**Agent**: Docs-Manager (`.claude/agents/docs-manager.md`)

{{ if --summary }}

**Dispatch Docs-Manager Agent**:

```markdown
Docs-Manager Agent - Executive Summary

GOAL: Create concise, stakeholder-ready summary

INPUT:
- Full plan: [from Phase 5]
- Target audience: Development team + stakeholders
- Length: 1-2 pages max

---

TASKS:

1. **Extract Key Info** (5 min)
   - Feature purpose (2-3 sentences)
   - Main phases
   - Critical tasks
   - Timeline

2. **Create Summary** (5 min)

```markdown
# Summary: $ARGUMENTS

## Overview
[2-3 sentence description]

## Key Changes
- [Change 1]
- [Change 2]
- [Change 3]

## Timeline
- **Estimated effort**: X-Y hours
- **Phases**: [count]
{{ if --tdd }}
- **Task granularity**: TDD micro-tasks (2-5 min)
{{ else }}
- **Task granularity**: Standard (15-60 min)
{{ endif }}

## Top Risks
1. [Risk] → [Mitigation]
2. [Risk] → [Mitigation]

## Success Criteria
- [ ] [Criterion 1]
- [ ] [Criterion 2]

## Next Steps
1. Review full plan
2. Execute with `/execute-plan`
3. Track progress
```

OUTPUT: Concise summary
```

{{ else }}

**Skip summary generation** (--summary flag not provided)

{{ endif }}

---

## Output

### Display in Chat

```markdown
✅ PLAN GENERATED: $ARGUMENTS

## Quick Overview
- **Mode**: {{ mode detected in Phase 0 }}
- **Phases**: {{ count }}
- **Tasks**: {{ count }}
- **Estimate**: X-Y hours
- **Risk**: Low/Medium/High

{{ if --current }}
## Current State
✓ Analyzed from: $CURRENT_PATH
- Gaps identified: {{ count }}
{{ endif }}

{{ if --guide }}
## Implementation Guide
✓ Integrated from: $GUIDE_PATH
{{ endif}}

## Requirements
- 🔴 MUST have: {{ count }}
- 🟡 SHOULD have: {{ count }}
- 🟢 COULD have: {{ count }}

{{ if --tdd }}
## Task Granularity
✓ TDD micro-tasks (2-5 min)
- Test → Implement → Verify → Commit pattern
{{ endif }}

## Next Steps
{{ if --output }}
1. Review full plan: $OUTPUT_PATH
{{ else }}
1. [Plan displayed above]
{{ endif }}
2. Execute: `/execute-plan {{ --output or 'inline' }}`
3. Track progress with TodoWrite
### Save to File (MANDATORY)

**CRITICAL**: Implementation plan MUST be written to file.

{{ if --output }}
**Primary output**: `$OUTPUT_PATH`
{{ else }}
**Default output**: `implementation-plan.md` (in current directory)
{{ endif }}

**File requirements**:
1. MUST write complete plan to file
2. MUST use cook-compatible format
3. MUST include all sections (Executive Summary → Verification Checklist)
4. File MUST be created before showing summary

**Write sequence**:
```bash
# Step 1: Determine output path
OUTPUT_FILE={{ if --output }}$OUTPUT_PATH{{ else }}./implementation-plan.md{{ endif }}

# Step 2: Write complete plan
write_file($OUTPUT_FILE, complete_plan_content)

# Step 3: Verify file created
if file_exists($OUTPUT_FILE):
  ✅ Plan written to: $OUTPUT_FILE
else:
  ❌ ERROR: Failed to write plan file
  STOP execution
```

---

### Display in Chat (Summary Only)

After plan file is written, show summary:

```markdown
✅ PLAN GENERATED: $ARGUMENTS

## Plan File
📝 **Written to**: {{ if --output }}$OUTPUT_PATH{{ else }}implementation-plan.md{{ endif }}
- Size: {{ file size }}
- Tasks: {{ count }}
- Phases: {{ count }}

## Quick Overview
- **Mode**: {{ mode detected in Phase 0 }}
- **Estimate**: X-Y hours
- **Risk**: Low/Medium/High

{{ if --current }}
## Current State
✓ Analyzed from: $CURRENT_PATH
{{ endif }}

{{ if --guide }}
## Implementation Guide
✓ Integrated from: $GUIDE_PATH
{{ endif}}

## Requirements
- 🔴 MUST have: {{ count }}
- 🟡 SHOULD have: {{ count }}
- 🟢 COULD have: {{ count }}

{{ if --tdd }}
## Task Granularity
✓ TDD micro-tasks (2-5 min)
{{ endif }}

## Next Steps
1. Review full plan: {{ output file path }}
2. Execute: `/cook {{ output file path }}`
3. Track progress: `/task-progress {{ output file path }}`
```

---

### File Content Template

The implementation plan file MUST contain:

```markdown
# Implementation Plan: {{ feature name }}

## 1. Executive Summary
{{ from Phase 5 }}

## 2. Current State
{{ from Phase 1 if --current }}

## 3. Verification Commands Reference
{{ from Phase 1 SUBTASK 1.4 }}

## 4. Implementation Phases

### Phase A: {{ name }}
{{ tasks with cook-compatible format }}

### Phase B: {{ name }}
{{ tasks }}

... (all phases)

## 5. Cross-Cutting Concerns
{{ preservation, testing, docs }}

## 6. Verification Checklist
{{ all checkboxes }}

---

**EXECUTION INSTRUCTIONS**:

Once plan is approved:
\```bash
# Execute with cook iterator
/cook {{ output path }}

# Or view progress
/task-progress {{ output path }}
\```
```

---

## Integration with Skills

### Auto-Triggered Skills

1. **Phase 1**: `codebase-exploration` (if --current)
2. **Phase 2**: `documentation-synthesis` (if --guide)
3. **Phase 3**: `pattern-analysis` (requirements extraction)
4. **Phase 5**: 
   - `writing-plans` (if --tdd)
   - `intelligent-planning` (if --auto-explore or standard)

### Fresh Context Benefits

- Each subagent starts clean
- No context pollution across phases  
- Specialized focus per agent type
- Independent retry capability
- Parallel mental models

---

## Examples

### Example 1: Full Context (Current + Guide)

```bash
/plan "multi-theme system" \
  --current=temp/theme-system/ \
  --guide=temp/theme-system/extensions/multi-theme-guide.md \
  --tdd \
  --summary
```

**What happens**:
1. Phase 0: Detects "Full Context" mode
2. Phase 1: Scout loads current theme system docs
3. Phase 2: Researcher analyzes multi-theme guide
4. Phase 3: Analyst creates MUST/SHOULD/COULD requirements
5. Phase 4: Selects TDD Micro-Planning (--tdd)
6. Phase 5: Planner creates 2-5 min tasks with TDD workflow
7. Phase 6: Docs-Manager writes executive summary

### Example 2: Extension (Current Only)

```bash
/plan "add export PDF" --current=docs/reports/
```

**What happens**:
1. Phase 0: Detects "Extension" mode
2. Phase 1: Scout loads current reports system
3. **Phase 2: Skipped** (no guide)
4. Phase 3: Analyst infers PDF export requirements
5. Phase 4: Selects Standard Planning
6. Phase 5: Planner creates 15-60 min tasks
7. **Phase 6: Skipped** (no --summary)

### Example 3: Greenfield (Guide Only)

```bash
/plan "authentication v2" --guide=docs/auth-v2-spec.md --tdd
```

**What happens**:
1. Phase 0: Detects "Greenfield with Guide" mode
2. **Phase 1: Skipped** (no current state)
3. Phase 2: Researcher analyzes auth v2 spec
4. Phase 3: Analyst extracts requirements from spec
5. Phase 4: Selects TDD Micro-Planning
6. Phase 5: Planner creates micro-tasks
7. **Phase 6: Skipped**

### Example 4: Auto-Explore

```bash
/plan "user dashboard" --auto-explore --type=react
```

**What happens**:
1. Phase 0: Detects "Auto-Exploration" mode
2. Phase 1: **Triggers 3-phase exploration** via intelligent-planning
3. **Phases 2-3: Integrated into exploration**
4. Phase 4: Selects Auto-Exploration Planning
5. Phase 5: Planner uses exploration results
6. **Phase 6: Skipped**

---

## Success Criteria

- [ ] Works with any combination of --current / --guide
- [ ] Handles auto-explore when no docs
- [ ] Supports TDD micro-tasks (--tdd)
- [ ] Categorizes requirements (MUST/SHOULD/COULD)
- [ ] Fresh context per phase
- [ ] Clear agent names (Scout, Researcher, Planner, Docs-Manager)
- [ ] Structured, verifiable output
