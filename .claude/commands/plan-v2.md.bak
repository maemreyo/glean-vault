# /plan - Intelligent Planning with Documentation Integration

## Purpose

Create comprehensive implementation plans by loading existing documentation and implementation guides. Leverages the agent ecosystem to analyze current state, research solutions, and generate execution-ready plans with proper task decomposition.

**Core Philosophy**: "Well-informed plans lead to successful implementations"

## Usage

```bash
# Basic planning with current state analysis
/plan "implement multi-theme support"

# Load existing documentation
/plan "multi-theme system" --current-state=temp/theme-system/

# Load implementation guide
/plan "multi-theme system" --implementation-guide=temp/theme-system/extensions/multi-theme-guide.md

# Load both current state and implementation guide
/plan "multi-theme system" \
  --current-state=temp/theme-system/ \
  --implementation-guide=temp/theme-system/extensions/multi-theme-guide.md

# Save outputs
/plan "multi-theme system" \
  --current-state=temp/theme-system/ \
  --implementation-guide=temp/theme-system/extensions/multi-theme-guide.md \
  --output=plans/multi-theme-implementation.md \
  --summary=docs/multi-theme-summary.md

# Planning with specific methodology
/plan "authentication system" --detailed  # 2-5 min TDD tasks
/plan "feature migration" --auto-explore  # 3-phase exploration
```

## Arguments

- `$ARGUMENTS`: Feature or task description to plan

## Flags

| Flag | Description | Example |
|------|-------------|---------|
| `--current-state=path` | Path to existing state documentation (from `/how`) | `--current-state=temp/theme-system/` |
| `--implementation-guide=path` | Path to implementation guide/solution | `--implementation-guide=docs/solution.md` |
| `--output=path` | Save detailed plan to file | `--output=plans/feature.md` |
| `--summary=path` | Save concise summary (via dedicated agent) | `--summary=docs/summary.md` |
| `--detailed` | Use TDD micro-tasks (2-5 min) instead of standard | `--detailed` |
| `--auto-explore` | Auto-explore codebase if no current state provided | `--auto-explore` |
| `--type=TYPE` | Type hint: react/api/utility/component | `--type=react` |
| `--skip-review` | Skip quality gates (faster, less safe) | `--skip-review` |
| `--mode=MODE` | Behavioral mode: default, brainstorm, token-efficient | `--mode=brainstorm` |

---

## Workflow

Planning: **$ARGUMENTS**

{{ if --current-state provided }}
**Current state docs**: `$CURRENT_STATE_PATH`
{{ endif }}

{{ if --implementation-guide provided }}
**Implementation guide**: `$IMPLEMENTATION_GUIDE_PATH`
{{ endif }}

{{ if --detailed }}
**Planning mode**: TDD micro-tasks (2-5 minutes)
{{ else }}
**Planning mode**: Standard tasks (15-60 minutes)
{{ endif }}

---

## Agent Orchestration Flow

### Phase 0: Setup & Context Loading (5 min)

**Main Agent**: Context coordinator

```markdown
Setup Phase - Preparing for Planning

INPUT:
- Task: "$ARGUMENTS"
{{ if --current-state provided }}
- Current State: $CURRENT_STATE_PATH
{{ endif }}
{{ if --implementation-guide provided }}
- Implementation Guide: $IMPLEMENTATION_GUIDE_PATH
{{ endif }}

STEPS:

1. Validate paths exist
2. Load documentation into structured context
3. Identify planning approach based on available information
4. Prepare agent dispatches

OUTPUT: Ready for analysis phases
```

---

### Phase 1: Current State Analysis (15-20 min)
{{ if --current-state provided }}

**Dispatch Documentation Analyzer Subagent**:

```markdown
Documentation Analyzer Subagent

GOAL: Extract comprehensive understanding from existing exploration documentation

INPUT:
- Documentation path: $CURRENT_STATE_PATH
- Feature: "$ARGUMENTS"

---

SUBTASK 1.1: Read Discovery Documentation (5 min)

1. Read phase-1-discovery-structure.md
2. Extract:
   - Current file inventory
   - Architecture patterns
   - Dependencies identified
   - Integration points
   - Technical debt noted

SUBTASK 1.2: Read Analysis Documentation (5 min)

1. Read phase-2-analysis.md
2. Extract:
   - Current capabilities
   - Business logic present
   - Patterns used
   - Issues identified
   - Key insights

SUBTASK 1.3: Synthesize Current State (5-10 min)

Create structured summary:
```markdown
## Current State Analysis

### Architecture
- Components: [list from discovery]
- Patterns: [from analysis]
- State Management: [identified]
- API Integration: [documented]

### Current Capabilities
- Implemented: [features]
- Missing: [gaps]
- Issues: [problems]

### Integration Points
- APIs: [endpoints]
- Components: [dependencies]
- Database: [schemas]

### Technical Debt
- Code quality: [issues]
- Performance: [problems]
- Testing: [coverage]
```

OUTPUT: Current state understanding for planning
```

{{ else if --auto-explore }}

**Skip to Phase 2 with auto-exploration**
(Will use intelligent-planning skill)

{{ endif }}

---

### Phase 2: Implementation Guide Analysis (15-20 min)
{{ if --implementation-guide provided }}

**Dispatch Solution Analyzer Subagent**:

```markdown
Solution Analyzer Subagent

GOAL: Extract actionable implementation steps from guide documentation

INPUT:
- Guide path: $IMPLEMENTATION_GUIDE_PATH
- Current state: [from Phase 1]
- Target: "$ARGUMENTS"

---

SUBTASK 2.1: Parse Implementation Strategy (10 min)

1. Identify proposed solution architecture
2. Extract step-by-step implementation
3. Note prerequisites and dependencies
4. Identify code patterns to follow

SUBTASK 2.2: Extract Technical Requirements (5 min)

1. New components needed
2. API changes required
3. Configuration updates
4. Testing requirements

SUBTASK 2.3: Map to Current State (5 min)

1. Where does solution integrate with existing?
2. What needs to be modified vs created?
3. Backward compatibility considerations
4. Migration strategy (if applicable)

OUTPUT: Implementation strategy synthesis
```

{{ endif }}

---

### Phase 3: Gap Analysis & Requirements (10-15 min)

**Dispatch Gap Analyzer Subagent**:

```markdown
Gap Analyzer Subagent

GOAL: Identify requirements by analyzing current state vs desired solution

INPUT:
- Current State: [from Phase 1 or exploration]
- Implementation Guide: [from Phase 2, if provided]
- Feature: "$ARGUMENTS"

---

SUBTASK 3.1: Define Requirements (10 min)

{{ if --current-state and --implementation-guide }}
1. Map current capabilities to desired solution
2. Identify missing pieces
3. Create requirements backlog:
   - MUST have: Critical functionality
   - SHOULD have: Important features
   - COULD have: Nice-to-haves
{{ else if --current-state }}
1. Analyze current state gaps
2. Infer requirements from missing functionality
3. Prioritize based on impact
{{ else }}
1. Decompose feature into epics
2. Break epics into user stories
3. Define acceptance criteria
{{ endif }}

SUBTASK 3.2: Technical Requirements (5 min)

1. Architecture decisions needed
2. Components to create/modify
3. API endpoints required
4. Database changes
5. Testing strategy

OUTPUT: Complete requirements specification
```

---

### Phase 4: Planning Strategy Selection (5 min)

**Main Agent**: Select appropriate planning approach

```markdown
Planning Strategy Selection

INPUT:
- Requirements: [from Phase 3]
- Current State: [from Phase 1]
{{ if --detailed }}
- User Request: TDD micro-tasks
{{ endif }}

OPTIONS:

1. **Standard Planning** (default)
   - 15-60 minute tasks
   - Good for experienced teams
   - Faster planning

2. **TDD Micro-Planning** (--detailed)
   - 2-5 minute tasks
   - Test-driven approach
   - Better for learning/complex features

3. **Intelligent Planning** (--auto-explore)
   - 3-phase exploration first
   - Comprehensive analysis
   - Best for unknown codebases

DECISION: Select based on inputs and flags
```

---

### Phase 5: Plan Generation (30-60 min)

**Dispatch Planner Subagent** with full context:

```markdown
Master Planner Subagent

GOAL: Generate comprehensive, execution-ready implementation plan

INPUT:
- Requirements: [complete specification]
- Current State: [analysis or exploration results]
- Implementation Guide: [strategy, if provided]
- Planning Strategy: [selected in Phase 4]

---

{{ if --detailed }}
USE: writing-plans skill
- Create 2-5 minute TDD micro-tasks
- Include exact file paths
- Provide complete code samples
- Structure: Test → Implement → Verify → Commit pattern
{{ else if --auto-explore }}
USE: intelligent-planning skill
- 3-phase subagent workflow
- Fresh subagent per phase
- Quality gates between phases
- Comprehensive exploration
{{ else }}
USE: intelligent-planning skill (lighter)
- Direct planning with exploration
- Standard task sizes (15-60 min)
- Focus on execution readiness
{{ endif }}

PLAN STRUCTURE:

1. **Executive Summary**
   - Feature overview
   - Time estimate
   - Risk assessment
   - Success criteria

2. **Current State Summary**
   - What exists
   - What's missing
   - Integration points

3. **Implementation Phases**
   - Phase 1: Foundation (types, constants, setup)
   - Phase 2: Core Logic (business rules, algorithms)
   - Phase 3: Components (UI implementation)
   - Phase 4: Integration (API, state, routing)
   - Phase 5: Testing (unit, integration, E2E)
   - Phase 6: Polish (accessibility, performance, docs)

4. **Detailed Tasks**
   {{ if --detailed }}
   - TDD micro-tasks (2-5 min)
   - Exact file paths
   - Complete code examples
   - Expected test outputs
   {{ else }}
   - Standard tasks (15-60 min)
   - Clear acceptance criteria
   - File paths included
   - Context references
   {{ endif }}

5. **Cross-Cutting Concerns**
   - Preservation requirements (if migrating)
   - Testing strategy
   - Documentation needs
   - Deployment considerations

OUTPUT: Complete implementation plan
```

---

### Phase 6: Summary Generation (10-15 min)

**Dispatch Documentation Synthesizer Subagent**:

```markdown
Documentation Synthesizer Subagent

GOAL: Create concise, human-readable summary of the plan

INPUT:
- Full Plan: [from Phase 5]
- Target Audience: Development team
- Length: Concise (1-2 pages max)

---

TASKS:

1. **Extract Key Information** (5 min)
   - Feature purpose
   - Main phases
   - Critical tasks
   - Dependencies
   - Timeline

2. **Create Executive Summary** (5 min)
   - One paragraph overview
   - Bullet point highlights
   - Resource needs
   - Risk factors

3. **Implementation Roadmap** (5 min)
   - Phase milestones
   - Key deliverables
   - Decision points
   - Success metrics

FORMAT: Clean markdown suitable for:
- Project documentation
- Team onboarding
- Stakeholder communication
- Quick reference during implementation

OUTPUT: Concise summary document
```

---

## Output Generation

### 1. Save Plan File
{{ if --output provided }}
```bash
Save complete plan to: $OUTPUT_PATH
```
{{ endif }}

### 2. Save Summary
{{ if --summary provided }}
```bash
Save concise summary to: $SUMMARY_PATH
```
{{ endif }}

### 3. Display in Chat
```markdown
# 📋 Plan Generated: [Feature Name]

## Quick Overview
- **Phases**: X
- **Tasks**: Y
- **Estimate**: Z hours
- **Risk**: Low/Medium/High

{{ if --current-state }}
## Current State
- Analyzed: Documentation loaded
- Gaps identified: X items
{{ endif }}

{{ if --implementation-guide }}
## Implementation Strategy
- Guide integrated: ✓
- Adaptation needed: Yes/No
{{ endif }}

## Next Steps
1. Review full plan {{ if --output }}(saved to $OUTPUT_PATH){{ endif }}
2. Execute with: `/execute-plan {{ $OUTPUT_PATH or 'plan-file.md' }}`
3. Track progress with TodoWrite integration
```

---

## Integration with Agent/Skill System

### Automatic Skill Triggers

1. **Documentation Loading**
   - `documentation-synthesis` skill for organizing inputs
   - `exploration-documentation` for parsing /how outputs

2. **Analysis Phases**
   - `pattern-analysis` for identifying reusable patterns
   - `sequential-thinking` for complex reasoning

3. **Planning Phase**
   - `intelligent-planning` for comprehensive planning
   - `writing-plans` for TDD micro-tasks
   - `verification-before-completion` for quality gates

4. **Quality Assurance**
   - `code-reviewer` for plan validation
   - `systematic-debugging` for issue identification

### Agent Coordination Pattern

```
Main Agent (Coordinator)
  ↓
Phase 1: Documentation Analyzer → Review Gate
  ↓
Phase 2: Solution Analyzer → Review Gate
  ↓
Phase 3: Gap Analyzer → Review Gate
  ↓
Phase 4: Strategy Selector (Main Agent)
  ↓
Phase 5: Master Planner (with skills)
  ↓
Phase 6: Documentation Synthesizer
  ↓
Complete Plan + Summary ✅
```

### Fresh Context Benefits

- Each phase gets clean context (no pollution)
- Specialized focus per agent type
- Independent retry capability
- Parallel mental model development

---

## Examples

### Example 1: Planning with Existing Documentation

```bash
/plan "multi-theme system" \
  --current-state=temp/theme-system/ \
  --implementation-guide=temp/theme-system/extensions/multi-theme-guide.md \
  --output=plans/multi-theme.md \
  --summary=docs/multi-theme-summary.md
```

**What happens**:
1. Loads theme system documentation from `/how` exploration
2. Parses implementation guide for multi-theme solution
3. Analyzes gaps between current and desired state
4. Creates detailed plan with specific tasks
5. Generates concise summary for team sharing

### Example 2: Fresh Planning with Auto-Exploration

```bash
/plan "user dashboard" --auto-explore --type=react --detailed
```

**What happens**:
1. Auto-explores codebase for dashboard-related code
2. Analyzes current patterns and components
3. Creates TDD micro-task plan (2-5 min tasks)
4. Includes React-specific patterns
5. Ready for `/execute-plan`

### Example 3: Migration Planning

```bash
/plan "migrate auth to v2" \
  --current-state=temp/auth-v1/ \
  --implementation-guide=docs/auth-v2-migration.md
```

**What happens**:
1. Analyzes current v1 authentication system
2. Understands v2 migration requirements
3. Creates preservation checklist
4. Plans incremental migration strategy
5. Includes rollback procedures

### Example 4: Feature Extension

```bash
/plan "add export PDF to reports" \
  --current-state=temp/reports/ \
  --detailed
```

**What happens**:
1. Loads current reports system documentation
2. Plans PDF export extension
3. Uses TDD micro-tasks for careful implementation
4. Preserves existing functionality
5. Adds comprehensive testing

---

## Success Criteria

- [ ] Current state properly analyzed (if provided)
- [ ] Implementation guide integrated (if provided)
- [ ] Requirements clearly defined
- [ ] Tasks are actionable and verifiable
- [ ] Plan is execution-ready
- [ ] Summary is concise and useful
- [ ] All agents and skills properly utilized

---

## Related Commands

```bash
/how [feature]              # Generate current state docs
/extend [feature]           # Extend existing features
/auto-plan [feature]        # Auto-explore + plan
/plan-detailed [task]       # TDD micro-tasks only
/execute-plan [plan-file]   # Execute generated plan
/research-plan [feature]    # Research-driven planning
```

---

## Pro Tips

1. **Always use `/how` first** for existing features:
   ```bash
   /how "theme system"     # Generates documentation
   /plan "theme system" --current-state=temp/theme-system/
   ```

2. **Create implementation guides** for complex solutions:
   - Document your research
   - Include code examples
   - Reference patterns
   - Use as input to `/plan`

3. **Use TDD mode for complex features**:
   - Better for learning
   - Safer implementation
   - Immediate feedback

4. **Save both plan and summary**:
   - Plan: For execution (`/execute-plan`)
   - Summary: For team communication

5. **Review the plan before executing**:
   - Check assumptions
   - Verify dependencies
   - Adjust timelines if needed

---

## Troubleshooting

### Documentation Not Found

```bash
# Generate documentation first
/how "feature name"

# Then plan with it
/plan "enhancement" --current-state=temp/feature/
```

### Plan Too Generic

```bash
# Add more context
/plan "feature" --type=react --current-state=path/
```

### Missing Implementation Details

```bash
# Create implementation guide first
# Then reference it in plan
/plan "feature" --implementation-guide=docs/solution.md
```

---

**Remember**: Good planning comes from good information. Use the documentation and agent ecosystem to create well-informed, execution-ready plans! 📋✨