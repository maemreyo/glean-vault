# Agent Coordination Reference

Reference for coordinating multiple agents during codebase exploration phases.

## Agent Mapping

### Phase 1: Discovery & Structure

| Role | Primary Agent | Secondary Agents | When to Use |
|------|---------------|------------------|-------------|
| File Discovery | `scout` | - | All explorations |
| External Research | `scout-external` | - | Third-party integrations |
| Context Analysis | `researcher` | - | Complex domains |
| Architecture | `scout` + `researcher` | - | Large systems |

### Phase 2: Code Analysis

| Role | Primary Agent | Secondary Agents | When to Use |
|------|---------------|------------------|-------------|
| Code Review | `code-reviewer` | - | All explorations |
| Security | `code-reviewer` + `security-auditor` | - | Auth, payments, data |
| Database | `code-reviewer` + `database-admin` | - | Data-heavy features |
| Performance | `code-reviewer` + `performance-engineer` | - | Critical paths |

## Parallel Execution Patterns

### Safe Parallel Execution
```markdown
# Can run in parallel (no shared state):
- Scout (file discovery)
- Scout-External (library research)
- Researcher (context analysis)
```

### Sequential Dependencies
```markdown
# Must run sequentially:
1. Scout → Code-Reviewer (Phase 1 → Phase 2)
2. Code-Reviewer → Security-Auditor (after code analysis)
3. Database-Admin → Code-Reviewer (schema first)
```

## Agent Handoffs

### Phase 1 → Phase 2 Handoff
```markdown
## Required Data
- Complete file inventory with categories
- Architecture patterns identified
- Entry points and integration points
- External dependencies noted
- Critical files prioritized

## Format
{
  "files": {
    "main": [...],
    "components": [...],
    "tests": [...],
    "config": [...]
  },
  "architecture": {
    "pattern": "Container/Presentational",
    "state": "React Query",
    "entryPoints": ["src/index.tsx"]
  },
  "dependencies": {
    "external": ["react", "react-query"],
    "internal": ["@/components/ui"]
  }
}
```

### Security Auditor Trigger
```markdown
## Conditions
- Authentication/authorization code found
- Payment processing identified
- PII handling detected
- API endpoints discovered

## Scope to Review
- Input validation
- Authentication flows
- Data exposure
- OWASP Top 10 compliance
```

## Communication Patterns

### Agent Instructions Template
```markdown
## Mission: [Specific Task]

**Context**:
- You are part of a multi-phase codebase exploration
- Previous phase findings: [summary]
- Expected output: [format]

**Scope**:
- Files to analyze: [list or pattern]
- Focus areas: [specific aspects]
- Exclusions: [what to ignore]

**Deliverables**:
1. [Required output 1]
2. [Required output 2]
3. [Analysis/insights]

**Quality Standards**:
- [Specific criteria]
- [Format requirements]
- [Depth expectations]
```

### Results Aggregation
```markdown
## Agent Results Summary

**Scout Agent**:
- Files found: X
- Architecture: [pattern]
- Dependencies: [list]

**Security Auditor**:
- Critical issues: X
- Recommendations: [list]

**Database Admin**:
- Schema efficiency: [assessment]
- Indexes needed: [list]

**Synthesis**:
- Overall health: [rating]
- Priority actions: [numbered]
```

## Error Handling

### Agent Timeout
```markdown
## Timeout Handling
1. Check if agent is stuck in large file
2. Split task into smaller chunks
3. Focus on high-priority files first
4. Document partial results
```

### Incomplete Analysis
```markdown
## Recovery Protocol
1. Identify missing coverage
2. Re-dispatch with focused scope
3. Combine with previous results
4. Note gaps in documentation
```

## Performance Optimization

### Agent Selection Guidelines
```markdown
# Use haiku for:
- Simple file counting
- Pattern matching
- Quick categorization

# Use sonnet for:
- Standard code analysis
- Pattern recognition
- Documentation generation

# Use opus for:
- Complex business logic
- Security vulnerability analysis
- Architecture assessment
```

### Task Distribution
```markdown
# Optimize for parallelism:
1. Separate concerns by file type
2. Distribute by domain knowledge
3. Avoid overlapping file access
4. Aggregate results at the end
```

## Quality Assurance

### Cross-Validation
```markdown
# When multiple agents analyze same code:
1. Compare findings
2. Resolve conflicts
3. Merge insights
4. Note disagreements
```

### Review Gates
```markdown
# Before Phase 2 complete:
- [ ] Business logic documented
- [ ] Security review done (if applicable)
- [ ] Database review done (if applicable)
- [ ] Performance considerations noted
- [ ] Technical debt identified
```

## Integration with Commands

### /how Command Coordination
```typescript
// Internal flow
async function executeHow(topic: string, options: HowOptions) {
  // Phase 1
  const phase1Results = await Promise.all([
    runScoutAgent(topic, options),
    options.includeExternal ? runScoutExternal(topic) : null
  ]);

  // Phase 2
  const phase2Results = await runCodeReviewer(phase1Results);

  // Specialized agents
  if (hasSecurity(phase2Results)) {
    const securityResults = await runSecurityAuditor(phase2Results);
    phase2Results.merge(securityResults);
  }

  // Documentation
  await generateDocumentation(phase1Results, phase2Results);
}
```

### Tool Requirements
```markdown
# Each agent needs access to:
- Read: File content analysis
- Glob: Pattern matching
- Grep: Content searching
- Bash: (optional) git context
- WebSearch: (scout-external only)
```

## Best Practices

1. **Clear Scopes**: Define precise boundaries for each agent
2. **Non-overlapping**: Avoid duplicate work between agents
3. **Structured Handoffs**: Use consistent data formats
4. **Documentation First**: Write docs immediately after each phase
5. **Quality Gates**: Verify completeness before proceeding
6. **Error Recovery**: Handle failures gracefully