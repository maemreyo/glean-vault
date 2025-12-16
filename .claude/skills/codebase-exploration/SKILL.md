---
name: Codebase Exploration
description: This methodology should be used when conducting deep codebase exploration through multi-phase analysis, coordinating multiple agents to comprehensively map code structure, dependencies, and implementation details. Used by `/how` command and other exploration workflows.
version: 1.0.0
---

# Codebase Exploration Methodology

## Overview

Multi-agent methodology for comprehensive codebase exploration through coordinated phases. Each phase specializes in different aspects of analysis with immediate documentation to prevent context loss.

**Key concepts:**
- Phase-based exploration (Discovery → Analysis → Documentation)
- Agent coordination with clear handoffs
- Immediate documentation after each phase
- Parallel execution when safe and beneficial
- Quality gates between phases

## When to Use

- Understanding how a feature works in existing codebase
- Onboarding to new project or domain
- Investigating complex systems before making changes
- Documenting legacy code
- Planning migrations or refactors
- Security audits of critical features
- Finding specific patterns or code smells

## Search Integration

This skill includes a Python search utility for rapid codebase analysis:

```bash
# Search for files matching pattern
python3 .claude/skills/codebase-exploration/scripts/search.py "auth.*service"

# Analyze architecture
python3 .claude/skills/codebase-exploration/scripts/search.py "" --type architecture

# Find dependencies for specific framework
python3 .claude/skills/codebase-exploration/scripts/search.py "" --type dependencies --framework react

# Search for specific code patterns
python3 .claude/skills/codebase-exploration/scripts/search.py "useState.*useEffect" --type patterns
```

## Quick Analysis Workflow

When you need rapid insights about the codebase:

```bash
# 1. Get overview
python3 .claude/skills/codebase-exploration/scripts/search.py "" --type architecture

# 2. Find files for feature
python3 .claude/skills/codebase-exploration/scripts/search.py "feature-name" --type files

# 3. Analyze patterns
python3 .claude/skills/codebase-exploration/scripts/search.py "TODO|FIXME|XXX" --type patterns
```

## Phase 1: Discovery & Structure

**Primary Agent**: Scout
**Support Agent**: Scout External (+ Researcher if needed)

### Mission Prompt Template

Use this prompt to dispatch the Scout agent:

```markdown
GOAL: Find all code related to "$ARGUMENTS" AND analyze its structure

INPUT:
- Search query: "$ARGUMENTS"
- Scope: {{ if --source }}$SOURCE_PATH{{ else }}Entire workspace{{ endif }}
- Mode: {{ if --comprehensive }}Comprehensive{{ else }}Standard{{ endif }}

---

### STEP 1: Internal Discovery (Scout)

1. **File Search** (find_by_name):
   - Patterns: exact match, camelCase, PascalCase, kebab-case
   - Common paths: src/, app/, components/, lib/

2. **Content Search** (grep_search):
   - Definitions: `class X`, `function X`, `interface X`
   - Usage: `import.*X`, `new X`
   - API: `@Route`, `endpoint`

3. **Structure Mapping**:
   - Create file inventory (Implementation, Tests, Config, Types)
   - Map component hierarchy (Parent -> Child)
   - Identify entry points

4. **Internal Dependencies**:
   - Map local imports
   - Identify shared util usage

---

### STEP 2: External Context (Scout External)

*Trigger: If key external libraries or patterns are identified.*

1. **Library Identification**:
   - Check `package.json` for major dependencies related to "$ARGUMENTS"
   - Example: If exploring "Auth", check for `next-auth`, `clerk`, `firebase`.

2. **Pattern Verification** (Optional - if unfamiliar):
   - Search external docs for best practices of utilized libraries.
   - Compare implementation with standard patterns.

---

### STEP 3: Analysis of Architecture

1. **Pattern Recognition**:
   - Container/Presentational?
   - MVC/MVVM?
   - Hook-based?

2. **State Management**:
   - Local vs Global (Redux, Context, Zustand)
   - Server State (React Query, SWR)

---

### OUTPUT: Discovery Report

Generate a report structured as:
1. **File Inventory**: Grouped by type
2. **Architecture**: Diagram and description
3. **Dependencies**: Internal & External (+ Diagram)
4. **External Context**: relevant library docs/versions
```

## Phase 2: Deep Analysis

**Primary Agent**: Code-Reviewer
**Support Agents**: Security Auditor, Database Admin

### Mission Prompt Template

Use this prompt to dispatch the Code-Reviewer agent:

```markdown
GOAL: Analyze implementation details, logic, and safety for "$ARGUMENTS"

INPUT:
- Phase 1 Discovery Report (file list, structure)
- Target Files: [List from Phase 1]

---

### STEP 1: Logic Extraction (Code-Reviewer)

1. **Business Logic**:
   - Extract critical algorithms (pricing, permissions, state transitions)
   - Document with line numbers and explanations
   - Identify "MUST PRESERVE" rules

2. **Data Flow**:
   - Trace data from Entry -> Process -> Persistence
   - Document transformations

3. **Data Models**:
   - Analyze Schemas/Types (Zod, TS Interfaces, DB Models)
   - Note validation rules

---

### STEP 2: Specialized Checks

1. **Database Check** (if DB models found):
   - *Agent: Database Admin (simulated or delegated)*
   - Review schema efficiency, indexing, relationships.

2. **Security Sweep** (if API/Auth/Input handled):
   - *Agent: Security Auditor (simulated or delegated)*
   - Check input sanitization, auth checks, CSRF, sensitive data handling.
   - Identify top vulnerabilities.

---

### STEP 3: Quality & Patterns

1. **Error Handling**:
   - Try/catch patterns, boundaries, user feedback.

2. **Performance**:
   - Memoization, lazy loading, N+1 query checks.

3. **Test Coverage**:
   - Review associated tests for coverage of critical logic.

---

### OUTPUT: Analysis Report

Generate a report structured as:
1. **Business Logic**: Detailed algorithms & rules
2. **Data Models**: Schemas and types
3. **Security & Safety**: Vulnerabilities and protections
4. **Key Insights**: Patterns, Tech Debt, Recommendations
```

## Report Templates

### Phase 1 Report Structure
- **Topic**: Title
- **Files**: List
- **Architecture**: Description + Diagram
- **Dependencies**: List + Diagram
- **External Context**: Library notes

### Phase 2 Report Structure
- **Business Logic**: Section with code blocks
- **Security**: Security findings
- **Data Models**: Interface/Schema definitions
- **Insights**: Good/Bad/Ugly

## Integration with Commands

This skill is used by:
- `/how [feature]` - Main exploration command
- `/auto-plan [feature]` - Exploration before planning
- `/apply [source]` - Pattern extraction for cloning
- `/refactor-from [feature]` - Analysis before refactoring

## Additional Resources

### Reference Files

For detailed implementation guidance:

- **`references/agent-coordination.md`** - Complete agent coordination patterns
- **`examples/exploration-workflows.md`** - Real-world examples and workflows

### Scripts Directory

The `scripts/` directory contains Python utilities for codebase analysis:

#### search.py
Search and analyze codebase with multiple modes:
- `--type files` - Find files by name/path
- `--type architecture` - Analyze codebase structure
- `--type dependencies` - Extract import dependencies
- `--type patterns` - Search for specific code patterns

#### core.py
Core utilities including:
- File categorization logic
- Architecture detection
- Dependency analysis
- Report generation

### Related Skills

- **`exploration-documentation`** - Generate comprehensive documentation from findings
- **`exploration-examples`** - Practical examples and troubleshooting
- **`pattern-analysis`** - Extract patterns for use with `/apply`
- **`documentation-synthesis`** - Create knowledge base from exploration
