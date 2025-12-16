# Brainstorming Output Templates

This file contains reusable templates for formatting brainstorming outputs.

---

## Template 1: Brainstorm Session

Use this template for comprehensive brainstorming sessions with multiple ideas.

```markdown
## Brainstorm: [Topic]

### Challenge
[Clear problem statement in 1-2 sentences]

### Constraints
- [Technical constraint 1]
- [Business constraint 2]
- [Resource constraint 3]

### Context
[Brief background from Step 0 context gathering]
- Files analyzed: [list]
- Key findings: [summary]

---

### Ideas Generated

#### Idea 1: [Descriptive Name]
**Description**: [2-3 sentence explanation of the approach]

**Pros**: 
- [Benefit 1]
- [Benefit 2]
- [Benefit 3]

**Cons**: 
- [Drawback 1]
- [Drawback 2]

**Effort**: [Low/Medium/High] ([time estimate])

**Example**:
```[language]
// Brief code snippet or diagram
```

#### Idea 2: [Descriptive Name]
**Description**: [2-3 sentence explanation]

**Pros**: 
- [Benefit 1]
- [Benefit 2]

**Cons**: 
- [Drawback 1]
- [Drawback 2]

**Effort**: [Low/Medium/High] ([time estimate])

**Example**:
```[language]
// Brief code snippet or diagram
```

#### Idea 3: [Descriptive Name]
[Follow same format as above]

#### Idea 4: [Descriptive Name]
[Follow same format as above]

#### Idea 5: [Descriptive Name]
[Follow same format as above]

---

### Wild Card Ideas
💡 **[Unconventional Idea 1]**: [Brief description of creative/risky approach]

💡 **[Unconventional Idea 2]**: [Another outside-the-box idea]

---

### Comparison Matrix

| Criteria | Idea 1 | Idea 2 | Idea 3 | Idea 4 | Idea 5 |
|----------|--------|--------|--------|--------|--------|
| **Feasibility** (1-5) | 4 | 5 | 3 | 4 | 2 |
| **Impact** (1-5) | 5 | 3 | 5 | 4 | 5 |
| **Effort** (1-5, lower better) | 3 | 5 | 2 | 3 | 4 |
| **Risk** (1-5, lower better) | 4 | 5 | 2 | 3 | 1 |
| **Team Fit** (1-5) | 4 | 5 | 4 | 3 | 2 |
| **TOTAL** | 20 | 23 | 16 | 17 | 14 |

**Scoring Guide**:
- Feasibility: 5=can start today, 1=requires major dependencies
- Impact: 5=solves problem completely, 1=minor improvement
- Effort: 5=very low effort, 1=very high effort (inverted scale)
- Risk: 5=very low risk, 1=very high risk (inverted scale)
- Team Fit: 5=matches current skills, 1=requires new expertise

---

### Recommendation

**🎯 Recommended Approach: [Name of top-scoring or most strategic idea]**

**Rationale**:
[2-3 paragraphs explaining why this is the best choice given constraints, team context, and business goals]

**Alternative**: If [specific condition], consider [2nd choice] instead because [reason].

---

### Validation Artifact

[Pseudo-code, interface definition, or architecture diagram showing the recommended approach is implementable]

```[language]
// Concrete code example showing key implementation details
// This proves the idea is feasible and provides starting point
```

---

### Next Steps

**Immediate** (This week):
1. [Action item 1]
2. [Action item 2]

**Short-term** (Next sprint):
1. [Action item 3]
2. [Action item 4]

**Long-term** (Next quarter):
1. [Action item 5]

**Success Metrics**:
- [Measurable outcome 1]
- [Measurable outcome 2]
```

---

## Template 2: Alternative Approaches

Use this template when comparing alternatives to an existing solution.

```markdown
## Alternatives Analysis: [Problem/Feature]

### Current Approach

**Description**: [How it currently works]

**Pain Points**:
- [Issue 1]
- [Issue 2]
- [Issue 3]

**What's Working**:
- [Positive aspect 1]
- [Positive aspect 2]

---

### Alternative 1: [Approach Name]

**Description**: 
[2-3 paragraph explanation of this alternative approach]

**How it Works**:
```[language]
// Code example showing implementation
```

**Trade-offs**:
- ✅ **Advantages**:
  - [Pro 1]
  - [Pro 2]
  - [Pro 3]
- ❌ **Disadvantages**:
  - [Con 1]
  - [Con 2]

**Migration Path**: [If switching from current approach, how to migrate]

**When to Use**: 
- [Scenario 1]
- [Scenario 2]

**Real-world Examples**:
- [Company/Project using this approach]

---

### Alternative 2: [Approach Name]

**Description**: 
[2-3 paragraph explanation]

**How it Works**:
```[language]
// Code example
```

**Trade-offs**:
- ✅ **Advantages**:
  - [Pro 1]
  - [Pro 2]
- ❌ **Disadvantages**:
  - [Con 1]
  - [Con 2]

**Migration Path**: [Migration strategy]

**When to Use**: 
- [Scenario 1]
- [Scenario 2]

**Real-world Examples**:
- [Company/Project using this]

---

### Alternative 3: [Approach Name]

[Follow same structure as Alternative 1 & 2]

---

### Decision Matrix

| Factor | Weight | Current | Alt 1 | Alt 2 | Alt 3 |
|--------|--------|---------|-------|-------|-------|
| Performance | 30% | 3 | 5 | 4 | 5 |
| Maintainability | 25% | 2 | 4 | 5 | 3 |
| Cost | 20% | 4 | 3 | 4 | 2 |
| Team Familiarity | 15% | 5 | 3 | 4 | 2 |
| Scalability | 10% | 3 | 5 | 4 | 5 |
| **Weighted Total** | | **3.15** | **4.05** | **4.25** | **3.65** |

---

### Decision Guide

**Choose [Alternative 1] when**:
- [Condition 1]
- [Condition 2]
- [Condition 3]

**Choose [Alternative 2] when**:
- [Condition 1]
- [Condition 2]

**Choose [Alternative 3] when**:
- [Condition 1]
- [Condition 2]

**Stick with Current Approach when**:
- [Condition 1]
- [Condition 2]

---

### Recommendation

**For your specific case**: [Recommended alternative]

**Because**:
1. [Reason 1 based on your constraints]
2. [Reason 2 based on your context]
3. [Reason 3 based on your goals]

**Implementation Approach**: [High-level plan]

---

### Proof of Concept

[Minimal code example proving the recommendation works]

```[language]
// Working prototype or interface definition
// Demonstrates feasibility and provides confidence
```

**Expected Outcomes**:
- [Metric 1]: [Before] → [After]
- [Metric 2]: [Before] → [After]
```

---

## Quick Mode Template

For simple/urgent requests, use this condensed format:

```markdown
## Quick Ideas: [Problem]

### Option 1: [Name]
- **What**: [One sentence]
- **Pros**: [Brief]
- **Cons**: [Brief]
- **Effort**: [Time estimate]

### Option 2: [Name]
- **What**: [One sentence]
- **Pros**: [Brief]
- **Cons**: [Brief]
- **Effort**: [Time estimate]

### Option 3: [Name]
- **What**: [One sentence]
- **Pros**: [Brief]
- **Cons**: [Brief]
- **Effort**: [Time estimate]

**Recommend**: [Option X] because [one sentence rationale]
```

---

## Template 3: Assumption Challenging

Use this template to challenge assumptions before generating solutions.

```markdown
## Assumption Challenge: {{ PROBLEM }}

### Problem Statement (As Given)
{{ original problem description }}

### Assumptions to Challenge

#### 1. Scope Assumption
**Assumed**: {{ what we think the scope is }}
**Challenge**: Are we solving the right problem?
**Questions**:
- Is this the root cause or just a symptom?
- Could a different framing be more valuable?
- What problem are users *actually* trying to solve?

**Reframe**: {{ alternative problem statement if applicable }}

---

#### 2. State Assumption
**Assumed**: {{ assumptions about state/data }}
**Challenge**: What state needs to be preserved?
**Questions**:
- What happens when feature is enabled/disabled/re-enabled?
- Should previous state be restored or reset?
- What's the user mental model for state transitions?

**Edge Cases**:
- {{ state transition scenario 1 }}
- {{ state transition scenario 2 }}

---

#### 3. User Assumption
**Assumed**: {{ single user type or use case }}
**Challenge**: Are there different user groups?
**Questions**:
- Could different users want different behaviors?
- Are there power users vs casual users?
- Could multiple modes coexist?

**User Segments**:
- **Group A**: {{ needs/expectations }}
- **Group B**: {{ different needs }}
- **Implication**: {{ hybrid solution? settings toggle? }}

---

#### 4. Constraint Assumption
**Assumed**: {{ constraints we're accepting }}
**Challenge**: Are constraints real or assumed?
**Questions**:
- Is this technical constraint or business constraint?
- Could constraint be relaxed with different approach?
- What would we do with unlimited resources/time?

**Re-evaluation**:
- {{ which constraints are hard (real) }}
- {{ which constraints are soft (assumed) }}
- {{ opportunities if soft constraints removed }}

---

#### 5. Dependency Assumption
**Assumed**: {{ what we think depends on what }}
**Challenge**: What else is affected?
**Questions**:
- Are there features dependent on this?
- Could this change break existing functionality?
- What's the cascade of effects?

**Impact Analysis**:
- **Direct impacts**: {{ features directly affected }}
- **Indirect impacts**: {{ downstream effects }}
- **Mitigation**: {{ how to handle dependencies }}

---

#### 6. Reversibility Assumption
**Assumed**: {{ assumptions about undo/rollback }}
**Challenge**: Can this be undone? How?
**Questions**:
- Is this change reversible?
- What needs to be saved/logged for rollback?
- What's the recovery path if things go wrong?

**Reversibility Plan**:
- {{ what can be undone automatically }}
- {{ what requires manual intervention }}
- {{ what's permanent/irreversible }}

---

### Challenged Problem Statement

Based on assumption challenges:

**Original**: {{ original problem }}

**Refined**: {{ refined problem statement addressing challenged assumptions }}

**New Constraints**:
- {{ real constraints identified }}
- {{ assumptions removed }}

**New Opportunities**:
- {{ opportunities from challenged assumptions }}

---

### Ready for Solutions

Now generate solutions for the **refined** problem statement with:
- Challenged assumptions documented
- Edge cases identified
- User segments considered
- Dependencies mapped
- Reversibility planned
```

---

## Template 4: Hybrid Solution Design

Use this when multiple valid approaches exist and hybrid solution is needed.

```markdown
## Hybrid Solution: {{ PROBLEM }}

### Context
Multiple valid approaches exist because:
- {{ reason 1: e.g., "Different user groups have different needs" }}
- {{ reason 2: e.g., "Multiple scenarios are equally common" }}
- {{ reason 3: e.g., "Trade-offs vary by context" }}

---

### Approaches Being Combined

#### Approach A: {{ Name }}
**Best for**: {{ use case A }}
**Strengths**: {{ pros }}
**Weaknesses**: {{ cons }}

#### Approach B: {{ Name }}
**Best for**: {{ use case B }}
**Strengths**: {{ pros }}
**Weaknesses**: {{ cons }}

{{ if more approaches }}
#### Approach C: {{ Name }}
**Best for**: {{ use case C }}
**Strengths**: {{ pros }}
**Weaknesses**: {{ cons }}
{{ endif }}

---

### Hybrid Design

**Core Idea**: {{ how approaches are combined }}

**Architecture**:
```{{ language }}
// Interface/structure showing hybrid design
{{ code showing how both modes coexist }}
```

**Mode Selection**:
- **Default mode**: {{ which approach is default and why }}
- **Switch mechanism**: {{ how users switch between modes }}
- **Auto-detection**: {{ if applicable, what triggers which mode }}

**Examples**:

**Scenario 1** ({{ use case A }}):
```{{ language }}
// Using Mode A
{{ code example }}
```

**Scenario 2** ({{ use case B }}):
```{{ language }}
// Using Mode B
{{ code example }}
```

---

### Implementation Details

#### State Management
```{{ language }}
// How to manage state across modes
interface HybridState {
  currentMode: 'A' | 'B' {{ | 'C' }};
  // Mode-specific state
  modeAState: {{ ... }};
  modeBState: {{ ... }};
  // Shared state
  sharedState: {{ ... }};
  // Transition history (for undo/redo)
  previousMode?: 'A' | 'B';
}
```

#### Mode Switching
```{{ language }}
function switchMode(from: Mode, to: Mode, state: HybridState) {
  // Save current state
  state.previousMode = from;
  
  // Mode-specific transition logic
  if (from === 'A' && to === 'B') {
    {{ transition logic }}
  }
  
  // Update current mode
  state.currentMode = to;
}
```

#### Settings/Preferences
```{{ language }}
interface UserPreferences {
  defaultMode: 'A' | 'B';
  rememberLastMode: boolean;
  {{ other preferences }}
}
```

---

### Edge Cases Handled

#### Edge Case 1: Mode Switch Mid-Operation
**Scenario**: {{ what happens if user switches mode while X is happening }}
**Handling**: {{ how to handle gracefully }}

#### Edge Case 2: State Conflict
**Scenario**: {{ when state from Mode A conflicts with Mode B }}
**Handling**: {{ conflict resolution strategy }}

#### Edge Case 3: Missing Data
**Scenario**: {{ mode requires data that doesn't exist }}
**Handling**: {{ fallback, defaults, or error }}

#### Edge Case 4: Performance
**Scenario**: {{ performance implications of hybrid approach }}
**Handling**: {{ optimization strategy }}

---

### Trade-offs

**Hybrid Approach**:
- ✅ **Pros**:
  - Satisfies multiple user groups
  - Flexible for future needs
  - Covers more use cases
- ❌ **Cons**:
  - More complex implementation
  - More code to maintain
  - Potential for mode confusion
  - Settings UI needed

**Compared to Single Approach**:
- **vs Mode A only**: {{ comparison }}
- **vs Mode B only**: {{ comparison }}

**Complexity Justification**:
{{ why the additional complexity is worth it }}
{{ measurable benefit: e.g., "serves 70% more users" }}

---

### Testing Strategy

**Test Cases**:
1. Mode A in isolation
2. Mode B in isolation
3. Switch A → B
4. Switch B → A
5. Rapid switching
6. State persistence across modes
7. Default mode selection
8. Settings save/load
9. Edge cases handling
10. Performance under load

**Test Data**:
```{{ language }}
// Sample test scenarios
const testScenarios = [
  { mode: 'A', input: {{ ... }}, expected: {{ ... }} },
  { mode: 'B', input: {{ ... }}, expected: {{ ... }} },
  { transition: 'A->B', state: {{ ... }}, expected: {{ ... }} }
];
```

---

### Migration Path

{{ if replacing existing feature }}
**From Current Implementation**:

1. **Phase 1**: Add Mode A (or B) alongside existing
2. **Phase 2**: Add mode switching capability
3. **Phase 3**: Add Mode B (or A)
4. **Phase 4**: Deprecate old implementation
5. **Phase 5**: Remove old code

**User Communication**:
- {{ how to announce new modes }}
- {{ how to help users choose right mode }}
- {{ migration guide for power users }}
{{ endif }}

---

### Recommendation

**Use Hybrid Approach** when:
- ✅ Multiple user groups with different needs
- ✅ Trade-offs vary significantly by use case
- ✅ No single "winner" approach
- ✅ Flexibility is valued over simplicity
- ✅ Additional complexity is justified by user value

**Use Single Approach** when:
- ❌ Clear winner exists for 90%+ of use cases
- ❌ Complexity cost > user value benefit
- ❌ Team resources limited
- ❌ Maintenance burden too high

**Decision for this case**: {{ HYBRID or SINGLE }} because {{ reasoning }}
```
