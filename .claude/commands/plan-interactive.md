# /plan-interactive - Interactive Planning with Clarification

## Purpose

Create implementation plans through an interactive dialogue. AI asks clarifying questions before generating the plan to ensure requirements are fully understood.

## Usage

```bash
/plan-interactive [task description]
```

## Arguments

- `$ARGUMENTS`: Initial description of the task (can be vague)

## When to Use

- ✅ Requirements are unclear or incomplete
- ✅ Exploring problem space
- ✅ Need to discuss trade-offs
- ✅ Complex decisions to make
- ✅ Multiple possible approaches
- ✅ Stakeholder requirements gathering

---

## Workflow

For task: **$ARGUMENTS**

### Step 1: Analyze Initial Request

Review the initial task description and identify:
- What's clear vs unclear
- Missing critical information
- Technical decisions needed
- Scope ambiguities

### Step 2: Ask Clarifying Questions

Present questions organized by category. Be specific and provide options where helpful.

### Step 3: Process Answers

After receiving answers:
- Summarize understanding
- Confirm any assumptions
- Ask follow-up questions if needed

### Step 4: Generate Tailored Plan

Create a plan customized to the specific answers received.

---

## Question Template

```markdown
🤔 **I need to understand your requirements better for: [Task Name]**

Based on your initial description, I have some questions:

---

### 1. Scope & Goals 🎯

**What problem are we solving?**
- What's the main pain point or need?
- Who are the primary users?
- What does success look like?

**Scope clarification:**
- Is this MVP or full-featured?
- Any hard deadline or time constraint?
- Are there related features to consider?

---

### 2. Technical Context 🔧

**Current state:**
- Is there existing code to work with?
- What's the current tech stack?
- Any constraints or limitations?

**Integration:**
- What systems does this need to connect to?
- Are there existing APIs or services to use?
- Any authentication/authorization requirements?

---

### 3. Requirements Details 📋

**Functional:**
- [Specific question about functionality #1]
- [Specific question about functionality #2]
- [Specific question about edge cases]

**Non-functional:**
- Performance requirements? (load time, throughput)
- Scalability needs? (users, data volume)
- Security concerns? (sensitive data, compliance)

---

### 4. Preferences & Constraints 🎨

**Approach:**
- Any preferred patterns or libraries?
- Testing requirements? (coverage, TDD)
- Documentation needs?

**Team:**
- Solo or collaborative work?
- Code review process?
- Deployment strategy?

---

### 5. Priority & Trade-offs ⚖️

If we need to make trade-offs, what's most important?
- [ ] Speed of delivery
- [ ] Code quality/maintainability
- [ ] Feature completeness
- [ ] Performance
- [ ] Security

---

**Please answer what you can** - even partial answers help me create a better plan. 

Or reply with:
- `"standard"` - for a generic plan with common assumptions
- `"minimal"` - just answer essential questions
- `"skip [section]"` - to skip specific sections
```

---

## Example Interaction

### User Request
```bash
/plan-interactive "rebuild the dashboard"
```

### AI Questions
```markdown
🤔 **I need to understand your dashboard requirements better:**

### 1. Data & Metrics 📊
- What metrics/data should be displayed?
- Where does the data come from? (API, database, real-time?)
- How often should data refresh?

### 2. User Experience 👥
- Who are the primary users? (roles, technical level)
- What actions should users take from the dashboard?
- Mobile support needed?

### 3. Technical Stack 🔧
- Current tech stack? (React, Vue, Angular?)
- Current dashboard to migrate from?
- Performance requirements?

### 4. Scope & Timeline ⏰
- MVP vs full-featured?
- Hard deadline?
- Team size available?

**Answer what you can, and I'll create a tailored plan!**
```

### User Answers
```
1. Sales metrics, revenue, user signups. From our REST API. Real-time not needed, 5-min refresh OK.
2. Sales team, non-technical. Need to filter by date range and export to CSV. Mobile nice-to-have.
3. React + TypeScript, using Recharts. Old dashboard uses class components.
4. MVP first, 2 weeks deadline, just me.
```

### AI Response
```markdown
✅ **Got it! Here's what I understand:**

**Scope**: Sales dashboard MVP with revenue, signups, date filtering, CSV export
**Tech**: React + TypeScript, Recharts, modernizing from class components
**Timeline**: 2 weeks, solo developer
**Priority**: Speed of delivery (MVP), then mobile later

**Key Decisions**:
- Functional components with hooks (modernize from class)
- 5-minute auto-refresh (polling or react-query)
- Client-side CSV export (no backend changes needed)
- Desktop-first, mobile as stretch goal

**Quick follow-up:**
1. Authentication already handled, or need to add?
2. Any existing design mockups, or I design as I go?

[After confirmation, generates detailed plan...]
```

---

## Handling Different Response Styles

### Minimal Answers
If user gives brief answers, ask targeted follow-ups:
```markdown
Thanks! A few quick clarifications:
1. For [X], did you mean [A] or [B]?
2. Should I assume [assumption]?
```

### Detailed Answers
Skip to plan generation with a summary:
```markdown
Perfect, I have everything I need! Here's my understanding:
[Summary]

Generating your plan now...
```

### "Standard" Response
Generate plan with common assumptions, noting what was assumed:
```markdown
Got it! Generating a standard plan with these assumptions:
- [Assumption 1]
- [Assumption 2]

⚠️ Let me know if any assumptions are wrong!
```

---

## Post-Clarification Plan

After clarification, generate a plan that:

1. **References the answers** - Show how requirements shaped the plan
2. **Notes assumptions** - Clearly mark what was assumed vs confirmed
3. **Highlights decisions** - Explain key technical decisions based on answers
4. **Includes alternatives** - Mention options not chosen (for future reference)

---

## Tips for Effective Questions

1. **Be specific**: "What framework?" not "Tell me about the tech"
2. **Offer options**: "React, Vue, or Angular?" helps anchor discussion
3. **Prioritize**: Ask most critical questions first
4. **Batch wisely**: 4-6 questions per section, not 20 at once
5. **Accept partial**: "Answer what you can" reduces friction

---

---

## Execution After Planning

After interactive planning session, execute the refined plan with `/execute-plan`.

**Reference**: `.claude/skills/methodology/executing-plans/SKILL.md`

### Interactive → Subagent Execution Flow

```
1. Interactive Planning
   ┌─────────────────────────┐
   │ AI asks questions       │
   │ You provide answers     │
   │ AI clarifies ambiguity  │
   │ Refined plan generated  │
   └─────────────────────────┘
   ↓
2. Save Plan
   /plan-interactive --save=plans/feature.md "description"
   ↓
3. Review Plan
   Read plans/feature.md
   Verify it matches your intent
   ↓
4. Execute with Subagents
   /execute-plan plans/feature.md
   ┌─────────────────────────┐
   │ Fresh subagent per task │
   │ Code review gates       │
   │ Quality guaranteed      │
   └─────────────────────────┘
   ↓
5. Complete! ✅
```

### Why Interactive + Subagents?

- ✅ **Better understanding**: Q&A clarifies requirements
- ✅ **Refined plan**: More accurate task breakdown
- ✅ **Quality execution**: Subagents + reviews ensure correctness
- ✅ **Less rework**: Fewer surprises, better outcomes

### Example

```bash
# Step 1: Interactive planning
/plan-interactive "add real-time notifications feature"
# AI asks: "Which notification channels? Push, Email, SMS?"
# You answer, AI refines plan

# Step 2: Save and execute
# (AI auto-saves or you use --save)
/execute-plan plans/notifications.md
```

---

## Related Commands

```bash
/plan           # Direct planning without questions
/plan-detailed  # TDD micro-tasks after clarification
/brainstorm     # Explore ideas before planning
```
