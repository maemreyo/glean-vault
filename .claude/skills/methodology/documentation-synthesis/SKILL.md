# Documentation Synthesis

## Description

A skill for "Reverse Engineering" understanding from code and synthesizing it into human-readable documentation. Focuses on the "Why" and "How" rather than just the "What" (which code already shows).

## When to Use

- Writing READMEs for modules
- Handing over code to other teams
- Documenting legacy systems
- Creating onboarding guides

## The Process

### Phase 1: Understand (Code -> Mental Model)

**Goal**: Extract intent from implementation.

**Techniques**:
- **Entity Mapping**: Trace relationships between major classes/interfaces.
- **Decision Identification**: Why was this pattern used? (Look for constraints, edge cases).
- **Terminology**: Identify the "Language of the Domain" used in the code.

### Phase 2: Synthesize (Mental Model -> Structure)

**Goal**: Organize information logically for a human reader.

**Structure**:
1.  **The "One-Liner"**: What does this thing do?
2.  **Key Concepts**: Definitions of domain terms.
3.  **Core Workflows**: Step-by-step logic explanations.
4.  **Gotchas**: Non-obvious behaviors or requirements.

### Phase 3: Narrate (Structure -> Prose)

**Goal**: Write clearly and concisely.

**Rules**:
- Use active voice ("The service validates input" > "Input is validated").
- Use diagrams (Mermaid) for complex flows.
- Include "Good vs Bad" examples.

## Output Format (for Analyzer Subagent)

```markdown
# Documentation Draft: [Module Name]

## 1. Overview
[Brief summary]

## 2. Key Concepts
- **Entity**: [Definition]

## 3. Data Flow (Mermaid)
[Diagram source]

## 4. Implementation Details
[Explanation of complex logic]
```
