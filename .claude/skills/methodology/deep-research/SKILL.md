# Deep Research
 
## Description

A systematic methodology for gathering, verifying, and synthesizing information from multiple external sources (web, documentation, examples) to solve complex problems or plan new features. 

## When to Use

- Planning features from scratch (no existing code to clone)
- Evaluating new technologies or libraries
- Investigating complex security requirements (e.g., OAuth, Payment)
- Debugging obscure errors with no obvious root cause
- Comparing architectural approaches

## When NOT to Use

- Simple syntax lookups
- Exploring *existing* local code (use `explore-codebase` or `intelligent-planning`)
- When requirements are already fully defined

---

## The Research Process

### Phase 1: Decomposition & Query Formulation

**Goal**: Break the problem down into searchable chunks.

**Strategy**:
- Identify key unknowns (e.g., "How does PKCE flow work?", "What are the security risks?")
- Formulate specific search queries for each unknown
- Avoid generic queries like "how to build X"

**Example**:
```
Unknown: "How to secure OAuth tokens in SPA?"
Queries: 
1. "SPA OAuth token storage best practices 2024"
2. "localStorage vs httpOnly cookies for access tokens"
3. "XSS risk in React applications auth"
```

### Phase 2: Source Triangulation

**Goal**: Verify information by cross-referencing multiple sources.

**Rule of Three**:
Try to find at least 3 types of sources:
1.  **Official Documentation** (RFCs, Library Docs) - Source of Truth
2.  **Community Tutorials** (Blogs, Videos) - Practical Implementation
3.  **Discussions** (GitHub Issues, StackOverflow) - Common Pitfalls & Edge Cases

**Verification**:
- If sources disagree, prioritize Official Documentation > Recent Community usage > Old discussions.
- Check dates! (Web development moves fast, 2020 advice might be obsolete).

### Phase 3: Synthesis & Application

**Goal**: Convert information into actionable decisions.

**Output Structure**:
1.  **Key Findings**: Summary of what was learned.
2.  **Decision Matrix**: Comparison of options (if applicable).
3.  **Consensus/Recommendation**: What we will do.
4.  **Security Checklist**: Specific risks to mitigate.
5.  **Reference Links**: Bibliography.

---

## Research Report Format

Standard output format for the Researcher Subagent:

```markdown
# Research Report: [Topic]

## Executive Summary
[Brief overview of findings]

## Key Findings

### 1. [Finding Name]
- **Details**: [Explanation]
- **Source**: [Link to docs/article]
- **Implication**: [How this affects our plan]

### 2. [Finding Name]
...

## Technical Recommendations

### Libraries/Tools
| Tool | Pros | Cons | Recommendation |
|------|------|------|----------------|
| Tool A | ... | ... | ✅ Best choice |
| Tool B | ... | ... | ❌ Overkill |

### Architecture Decisions
- **Decision**: Use httpOnly cookies for token storage.
- **Why**: Mitigates XSS attacks (localStorage is vulnerable).
- **Trade-off**: Requires CSRF protection on API.

## Security Checklist
- [ ] Implement CSRF tokens
- [ ] Use PKCE flow
- [ ] ...

## References
1. [Official Spec](url)
2. [Security Best Practices](url)
```

---

## Integration with Planning

### From Research to Design
Feed the **Research Report** into the **Design** phase (using `brainstorming` skill):
- "Based on the recommendation to use httpOnly cookies, how should we design the API authentication endpoints?"

### From Research to Plan
Feed the **Technical Recommendations** into the **Plan** phase (using `writing-plans` skill):
- "Create tasks to install the selected 'Tool A' and configure it according to the 'Security Checklist'."

---

## Best Practices

- **Cite Sources**: Always include URLs. Don't hallucinate APIs.
- **Check Version Compatibility**: Ensure researched solutions work with the project's current stack versions.
- **Look for "Why Not"**: Actively search for reasons *not* to use a library (e.g., "Tool A performance issues", "Tool B unmaintained").
