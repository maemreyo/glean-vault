---
name: brainstorm-facilitator
description: Generate creative ideas using multiple techniques (mind mapping, SCAMPER, reverse brainstorming), organize and visualize ideas, evaluate and prioritize systematically. Use when user mentions "brainstorm", "ideate", "generate ideas", "creative thinking", or needs help with innovation, problem-solving, or organizing thoughts into actionable solutions.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebFetch, WebSearch
---

# Brainstorm Facilitator

This skill helps transform scattered ideas into actionable solutions through structured creative thinking techniques and systematic evaluation.

## Quick Start

```bash
# Start a brainstorming session
"Let's brainstorm features for our mobile app"

# Use specific technique
"Can you help me SCAMPER this existing feature?"

# Evaluate ideas
"Help me prioritize these brainstorming results"
```

## Core Techniques

### 1. Mind Mapping
- Visual exploration of central themes
- Branching out to related concepts
- Free association and pattern discovery
- Great for initial idea expansion

### 2. SCAMPER Method
- **S**ubstitute: What can we replace?
- **C**ombine: What can we merge?
- **A**dapt: How can we adapt this?
- **M**odify: How can we change this?
- **P**ut to other uses: Other applications?
- **E**liminate: What can we remove?
- **R**everse: What if we did the opposite?

### 3. Reverse Brainstorming
- Identify problems instead of solutions
- "How could we make this worse?"
- Turn problems into opportunities
- Reveals hidden assumptions

### 4. Six Thinking Hats
- **White Hat**: Facts and data
- **Red Hat**: Emotions and feelings
- **Black Hat**: Risks and cautions
- **Yellow Hat**: Benefits and positives
- **Green Hat**: New ideas and creativity
- **Blue Hat**: Process and control

## Session Workflow

### Phase 1: Preparation
1. **Define the challenge clearly**
   - What specific problem are we solving?
   - What constraints exist?
   - What does success look like?

2. **Gather context**
   - Review existing materials
   - Research relevant examples
   - Understand stakeholder needs

3. **Choose technique(s)**
   - Mind mapping for exploration
   - SCAMPER for improvement
   - Reverse brainstorming for risks

### Phase 2: Idea Generation
1. **Create safe space for ideas**
   - No judgment in generation phase
   - Quantity over quality initially
   - Build on others' ideas

2. **Use chosen technique**
   - Follow structured prompts
   - Document everything
   - Encourage wild ideas

3. **Switch perspectives**
   - Try different hats/roles
   - Consider extreme users
   - Challenge assumptions

### Phase 3: Organization
1. **Cluster similar ideas**
   - Group related concepts
   - Identify patterns
   - Create categories

2. **Create visual representations**
   - Mind maps
   - Connection diagrams
   - Concept hierarchies

### Phase 4: Evaluation
1. **Establish criteria**
   - Impact vs effort matrix
   - Feasibility assessment
   - Alignment with goals

2. **Score and rank**
   - Use consistent scoring system
   - Consider multiple perspectives
   - Document reasoning

3. **Select top ideas**
   - Choose for immediate action
   - Plan for future exploration
   - Archive rejected ideas

## Implementation Steps

### Step 1: Initial Assessment
```markdown
- Ask clarifying questions about the problem
- Identify stakeholders and constraints
- Determine session format (individual/group)
- Select appropriate techniques
- Set up documentation structure
```

### Step 2: Context Gathering
```bash
# Find relevant project files
grep -r "problem\|challenge\|goal" src/ --include="*.md"
grep -r "TODO\|FIXME\|IDEA" . --include="*.md" --include="*.txt"

# Create brainstorming workspace
mkdir -p brainstorming/$(date +%Y-%m-%d)-session
```

### Step 3: Execute Brainstorming
- Facilitate chosen technique
- Document all ideas without judgment
- Encourage participation
- Maintain energy and focus

### Step 4: Process Results
- Organize and cluster ideas
- Apply evaluation framework
- Create action items
- Plan next steps

## Templates and Formats

### Mind Map Template
```markdown
# Mind Map: [Topic]

## Central Theme
- [Core concept]

## Main Branches
### Branch 1
- Sub-idea
  - Detail
  - Connection

### Branch 2
- Sub-idea
  - Detail
  - Connection
```

### SCAMPER Worksheet
```markdown
# SCAMPER Analysis: [Product/Idea]

## Substitute
- What can be replaced?
- Alternative materials?
- Different approach?

## Combine
- What can we merge?
- Features to combine?
- Integrations possible?

## Adapt
- How can we adapt?
- What can we modify?
- New contexts?

[... continue for all letters]
```

### Evaluation Matrix
```markdown
# Idea Evaluation Matrix

| Idea | Impact (1-10) | Effort (1-10) | Feasibility (1-10) | Total Score |
|------|---------------|---------------|-------------------|-------------|
| Idea 1 | 8 | 4 | 7 | 19 |
| Idea 2 | 6 | 6 | 9 | 21 |
```

## Export Formats

### 1. Mind Map (Markdown)
- Nested bullet points
- Emoji for visual interest
- Links for connections

### 2. Structured List
- Numbered priorities
- Clear action items
- Owner assignments

### 3. Decision Matrix
- Scoring criteria
- Weighted importance
- Clear rankings

### 4. Action Plan
- Next steps
- Timelines
- Dependencies

## Best Practices

### During Brainstorming
- Defer judgment completely
- Encourage wild ideas
- Build on others' suggestions
- Stay focused on topic
- One conversation at a time
- Visualize ideas
- Go for quantity

### For Facilitators
- Prepare clear prompts
- Manage time effectively
- Ensure all voices heard
- Document everything
- Maintain positive energy
- Handle conflicts gracefully

### For Virtual Sessions
- Use collaborative tools
- Enable video for connection
- Have backup tech ready
- Schedule breaks
- Send prep materials
- Record session (with permission)

## Common Pitfalls to Avoid

- **Analysis paralysis**: Don't overthink during generation
- **Groupthink**: Encourage diverse perspectives
- **Premature judgment**: Separate generation from evaluation
- **Dominant voices**: Ensure inclusive participation
- **Vague problems**: Start with specific, well-defined challenges
- **No action**: End with clear next steps

## Advanced Techniques

### Morphological Analysis
- Break problem into parameters
- List all possible values
- Combine systematically
- Identify novel combinations

### TRIZ (Theory of Inventive Problem Solving)
- Identify contradictions
- Use 40 inventive principles
- Resolve technical conflicts
- Predict evolution paths

### Design Thinking
- Empathize with users
- Define problem statement
- Ideate solutions
- Prototype quickly
- Test and iterate

## Group Session Tips

### Preparation
- Send agenda in advance
- Prepare space and materials
- Test technology
- Assign roles (facilitator, note-taker)

### During Session
- Start with icebreaker
- Set ground rules
- Use timeboxing
- Capture everything
- Summarize frequently

### Follow-up
- Send summary within 24 hours
- Assign clear action items
- Schedule check-ins
- Archive outputs properly

## Requirements

### Dependencies
- Python 3.8+ (for mind map scripts)
- Graphviz (optional, for visual diagrams)
- Pandas (for data analysis in evaluation)

### Installation
```bash
pip install graphviz pandas matplotlib
```

## Integration with Project Workflows

### Before Sprint Planning
- Brainstorm feature ideas
- Prioritize backlog items
- Identify risks and dependencies

### During Design Reviews
- Generate alternative solutions
- Evaluate trade-offs
- Consider edge cases

### Problem-Solving
- Root cause analysis
- Solution exploration
- Risk assessment

## Examples

### Product Feature Brainstorm
```markdown
# Challenge: How might we improve user onboarding?

Mind Map branches:
- Simplification
- Personalization
- Gamification
- Social integration
- Analytics and feedback
```

### Process Improvement
```markdown
# Challenge: Reduce deployment time

SCAMPER results:
- Substitute: Manual steps with automation
- Combine: Testing and deployment
- Adapt: Use CI/CD best practices
```

## Troubleshooting

**Low energy in session?**
- Try warm-up exercises
- Change environment
- Introduce constraints
- Use rapid-fire rounds

**Running out of ideas?**
- Change perspective
- Use random prompts
- Take a break
- Research similar problems

**Ideas too similar?**
- Challenge assumptions
- Introduce constraints
- Use opposites
- Bring in outsiders

## Success Metrics

Track the effectiveness of your brainstorming:
- Number of actionable ideas generated
- Diversity of solutions
- Implementation rate
- Team engagement scores
- Problem resolution speed

Remember: The goal is not just ideas, but actionable solutions that move projects forward!