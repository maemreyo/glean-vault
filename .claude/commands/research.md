# /research - Technology Research Command

## Purpose

Conduct comprehensive technology research with real data from web search, provide comparisons, metrics, and actionable recommendations tailored to your context.

## Usage

```bash
/research [topic]
/research --compare [topic]            # Compare alternatives automatically
/research --quick [topic]              # Quick overview (TL;DR)
/research --deep [topic]               # Exhaustive research with citations
/research --for="context" [topic]      # Context-aware (e.g., --for="next.js")
/research --save=path [topic]          # Save to markdown file
```

## Arguments

- `$ARGUMENTS`: Technology, library, or approach to research

---

## Workflow

Create comprehensive research for: **$ARGUMENTS**

### Phase 1: Context Gathering 🎯

**Quick Clarifications** (if topic is broad):

Ask user:
1. What's your specific use case?
2. Current tech stack? (React, Next.js, Node.js, etc.)
3. Team size/experience level?
4. Performance/bundle size constraints?
5. Any specific requirements? (TypeScript, SSR, etc.)

**Example**:
```
🤔 To give you the best research, I need to know:

1. Use case: [e.g., "form validation for Next.js app"]
2. Stack: [e.g., "React 18 + Next.js 14 + TypeScript"]
3. Priority: [Performance / DX / Simplicity]

(Or skip with default assumptions)
```

---

### Phase 2: Data Collection 📊

**Web Search for**:

1. **Official Documentation**
   - Latest version and features
   - Getting started guide
   - API reference

2. **Package Statistics** (if library):
   - npm downloads/week (npmtrends.com)
   - GitHub stars, forks, issues
   - Last commit date
   - Contributors count
   - Bundle size (bundlephobia.com)

3. **Community Insights**:
   - Recent articles (2024)
   - Stack Overflow discussions
   - Reddit/Twitter sentiment
   - GitHub Discussions/Issues patterns

4. **Benchmark Data**:
   - Performance comparisons
   - Bundle size comparisons
   - Build time comparisons

5. **Real-World Usage**:
   - Who's using it? (companies)
   - Production-ready?
   - Common pain points

---

### Phase 3: Analysis 🔍

**Evaluate Against Criteria**:

1. **Maturity & Maintenance** (20%)
   - Age and stability
   - Release frequency
   - Breaking changes history
   - Long-term viability

2. **Community & Ecosystem** (20%)
   - Size of community
   - Available plugins/integrations
   - Quality of support
   - Learning resources

3. **Performance & Size** (20%)
   - Runtime performance
   - Bundle size
   - Memory usage
   - Build time impact

4. **Developer Experience** (25%)
   - API design
   - TypeScript support
   - Error messages
   - Debugging tools
   - Learning curve

5. **Documentation & Examples** (15%)
   - Docs quality
   - Examples availability
   - Migration guides
   - Video tutorials

**Score each area: 🟢 Excellent | 🟡 Good | 🟠 Fair | 🔴 Poor**

---

### Phase 4: Generate Recommendations 🎯

**Decision Matrix** (if multiple options):

Create comparison table with:
- Feature parity
- Performance metrics
- Bundle sizes
- Community size
- DX ratings
- Learning curve
- Best use cases

**Clear Recommendation**:
- Primary choice with reasoning
- When to use alternatives
- Migration complexity (if replacing something)
- Long-term considerations

---

## Output Format

```markdown
## 🔍 Research: [Topic]

**Research Date**: [YYYY-MM-DD]  
**Context**: [Your specific context]  
**Research Depth**: [Quick/Standard/Deep]  
**Confidence Level**: [High/Medium/Low]

---

### 📋 TL;DR

[1-2 sentence summary + main recommendation]

**Bottom Line**: Use **[Recommendation]** because [key reason].

---

### 📊 Overview

**What is it?**  
[Brief description - what problem does it solve?]

**Current State (2024)**:  
[Maturity, adoption, recent developments]

**Key Features**:
- [Feature 1]
- [Feature 2]
- [Feature 3]

---

### 📈 Metrics & Statistics

{{ if is_library }}

| Metric | Value | Assessment |
|--------|-------|------------|
| **npm Downloads/week** | [X] | [emoji] [trend] |
| **GitHub Stars** | [X] | [emoji] [popularity level] |
| **Last Commit** | [X days ago] | [emoji] [active/stale] |
| **Open Issues** | [X] | [emoji] [maintenance quality] |
| **Contributors** | [X] | [emoji] [community size] |
| **Bundle Size** | [X KB gzipped] | [emoji] [size rating] |
| **TypeScript** | [Native/DefinitelyTyped/None] | [emoji] |
| **License** | [MIT/etc] | [emoji] |
| **First Released** | [YYYY] | [age indicator] |

**Trend**: [📈 Growing / 📊 Stable / 📉 Declining]

{{ endif }}

---

### ✅ Strengths

1. **[Strength #1]**
   - [Detailed explanation]
   - [Why this matters in your context]
   - [Example or proof]

2. **[Strength #2]**
   - [Details]
   - [Impact]

3. **[Strength #3]**
   - [Details]

---

### ❌ Limitations & Drawbacks

1. **[Limitation #1]**
   - [Impact on your use case]
   - [Workaround]: [If exists]
   - [Severity]: [Critical/Moderate/Minor]

2. **[Limitation #2]**
   - [Details]
   - [When this matters]

3. **[Limitation #3]**
   - [Details]

---

### 🆚 Comparison with Alternatives

{{ if compare_mode }}

**Comparing**: [Option A] vs [Option B] vs [Option C]

| Aspect | [Option A] | [Option B] | [Option C] |
|--------|-----------|-----------|-----------|
| **Performance** | ⚡ Excellent (X ms) | 🐌 Slow (Y ms) | ⚡ Good (Z ms) |
| **Bundle Size** | 🟢 Small (12 KB) | 🔴 Large (45 KB) | 🟢 Tiny (8 KB) |
| **DX Rating** | 😊 9/10 | 😐 6/10 | 😊 8/10 |
| **Learning Curve** | 📚 Easy | 📚📚 Hard | 📚 Medium |
| **TypeScript** | ✅ Native | ✅ DT | ❌ None |
| **Community** | 🔥 Huge (50K⭐) | 🔥 Large (30K⭐) | 💫 Growing (5K⭐) |
| **Maintenance** | ✅ Active | ⚠️ Slow | ✅ Active |
| **Ecosystem** | 🌟 Rich | 🌟 Moderate | 💫 Small |
| **Best For** | Large production apps | Legacy projects | New small projects |
| **Pricing** | Free | Free | Free/Paid |

**Performance Benchmark**:
```
Option A: 100ms (baseline)
Option B: 380ms (3.8x slower) 🔴
Option C: 85ms (1.2x faster) ✅
```

**Winner for [Your Context]**: **[Choice]**

**Reasoning**:
- [Key differentiator #1]
- [Key differentiator #2]
- [Trade-off explanation]

{{ endif }}

---

### 🎯 Recommendation

**For your context ([specific context])**:

Use **[Primary Recommendation]** ⭐

**Why**:
1. [Reason #1 - specific to your needs]
2. [Reason #2 - backed by data]
3. [Reason #3 - practical consideration]

**When NOT to use**:
- ❌ If [scenario] → Use [alternative] instead
- ❌ If [constraint] → Consider [alternative]

**Confidence**: [High/Medium/Low]  
**Risk**: [Low/Medium/High]

---

### 🔄 Migration Path

{{ if replacing_existing }}

**From [Old Technology]**:

**Difficulty**: [Easy/Medium/Hard]  
**Estimated Time**: [X hours/days]  
**Breaking Changes**: [Yes/No]

**Steps**:
1. [Migration step 1]
2. [Migration step 2]
3. [Migration step 3]

**Gotchas**:
- ⚠️ [Common pitfall #1]
- ⚠️ [Common pitfall #2]

**Gradual Migration Possible?** [Yes/No]

{{ endif }}

---

### 📚 Resources

**Official**:
- 📖 [Documentation](url)
- 🎓 [Getting Started Guide](url)
- 📺 [Official Tutorial](url)

**Community**:
- 💬 [Discord/Community](url)
- 📊 [Benchmarks](url)
- 🎯 [Awesome List](url)

**Learning**:
- 🎓 [Best Tutorial](url)
- 📝 [In-depth Article](url)
- 🎬 [Video Course](url)

**Tools**:
- 🛠️ [Playground/REPL](url)
- 📦 [npm Package](url)
- 💻 [GitHub Repository](url)

---

### 🚀 Quick Start

**Installation**:
```bash
# Using npm
npm install [package]

# Using pnpm
pnpm add [package]

# Using yarn
yarn add [package]
```

**Basic Usage**:
```typescript
// Minimal working example
import { [feature] } from '[package]';

[code example showing key features]
```

**With TypeScript**:
```typescript
// TypeScript example
[typed example]
```

**Common Patterns**:
```typescript
// Pattern 1: [Use case]
[example]

// Pattern 2: [Use case]
[example]
```

---

### ⚙️ Configuration

**Minimal Config**:
```javascript
// Just enough to get started
{
  [minimal config]
}
```

**Recommended Config**:
```javascript
// Production-ready setup
{
  [recommended config]
}
```

**Advanced Options**:
```javascript
// For complex use cases
{
  [advanced config]
}
```

---

### 🧪 Testing

**Test Setup**:
```typescript
// How to test code using this technology
[test example]
```

**Mock/Stub**:
```typescript
// How to mock in tests
[mocking example]
```

---

### 🎯 Next Steps

Based on this research, here's what you should do:

**Immediate (Today)**:
1. [Actionable step - e.g., "Try the quick start example"]
2. [Actionable step - e.g., "Read the getting started guide"]

**This Week**:
1. [Medium-term action - e.g., "Build a small proof-of-concept"]
2. [Medium-term action - e.g., "Evaluate with your team"]

**Before Production**:
1. [Important consideration]
2. [Risk mitigation step]

**Optional/Future**:
1. [Nice-to-have]
2. [Advanced exploration]

---

### 💡 Pro Tips

**Best Practices**:
- ✅ [Best practice #1]
- ✅ [Best practice #2]
- ✅ [Best practice #3]

**Common Mistakes**:
- ❌ [Mistake #1] → [How to avoid]
- ❌ [Mistake #2] → [How to avoid]

**Performance Tips**:
- ⚡ [Optimization #1]
- ⚡ [Optimization #2]

---

### 🤔 FAQs

**Q: [Common question 1]?**  
A: [Clear answer]

**Q: [Common question 2]?**  
A: [Clear answer]

**Q: [Common question 3]?**  
A: [Clear answer]

---

### 🚨 Known Issues

**Be Aware of**:
- ⚠️ [Issue #1] - [Status: Fixed in v2 / Workaround exists / Open]
- ⚠️ [Issue #2] - [Details]

**Breaking Changes Coming**:
- [Upcoming change] in [version]

---

### 📊 Decision Summary

**Choose [Recommendation] if**:
- ✅ [Criterion 1]
- ✅ [Criterion 2]
- ✅ [Criterion 3]

**Choose [Alternative] if**:
- ✅ [Different criterion]

**Still unsure?** [Additional guidance]

---

**Want to implement this?**  
→ Use `/plan-react [feature using this tech]` to create implementation plan  
→ Use `/setup-testing` to set up tests for this technology  
→ Use `/compare [this] vs [alternative]` for deeper comparison

**Need more research?**  
→ `/research --deep [topic]` for exhaustive analysis  
→ `/research --for="your-stack" [related-topic]` for related technologies
```

---

## Real-World Examples

### Example 1: Form Library Research

**Input**:
```bash
/research "React form libraries"
```

**Output includes**:
- React Hook Form vs Formik vs Yup vs Zod
- Performance benchmarks (renders, validation speed)
- Bundle size comparison (12KB vs 45KB)
- DX ratings with examples
- TypeScript support comparison
- **Recommendation**: React Hook Form + Zod for modern apps

---

### Example 2: State Management

**Input**:
```bash
/research --compare --for="next.js 14" "React state management"
```

**Output includes**:
- Context vs Redux Toolkit vs Zustand vs Jotai vs Recoil
- Next.js App Router compatibility
- Server Components considerations
- Performance in SSR
- Bundle impact
- **Recommendation**: Zustand for client state, Server Actions for server state

---

### Example 3: Quick Tech Check

**Input**:
```bash
/research --quick "Bun runtime"
```

**Output**:
- Brief TL;DR: "Node.js alternative, 3x faster, growing ecosystem"
- Key metrics: Speed, compatibility, adoption
- Quick comparison with Node.js/Deno
- **Recommendation**: "Promising but wait for v2 for production"

---

### Example 4: Database ORM

**Input**:
```bash
/research --deep --for="nextjs fullstack typescript" "database ORMs"
```

**Output**:
- Exhaustive comparison: Prisma vs Drizzle vs TypeORM vs Kysely
- Edge runtime compatibility
- Type safety comparison
- Performance benchmarks
- Migration tooling
- Schema evolution
- **Recommendation**: Drizzle for edge, Prisma for traditional

---

### Example 5: Authentication

**Input**:
```bash
/research "authentication solutions for Next.js"
```

**Output**:
- NextAuth vs Clerk vs Auth0 vs Supabase Auth
- Feature comparison (OAuth, magic links, MFA)
- Pricing tiers
- Setup complexity
- Customization level
- **Recommendation**: NextAuth for self-hosted, Clerk for managed

---

## Flags Reference

| Flag | Description | Example |
|------|-------------|---------|
| `--compare` | Auto-compare multiple alternatives | `--compare` |
| `--quick` | Brief overview, TL;DR focus | `--quick` |
| `--deep` | Exhaustive research with citations | `--deep` |
| `--for="context"` | Context-aware (tailors to your stack) | `--for="next.js+ts"` |
| `--save=path` | Save research to markdown file | `--save=docs/orm.md` |
| `--format=json` | Output as JSON (for programmatic use) | `--format=json` |

---

## Research Quality Indicators

**High Quality Research Includes**:
- ✅ Real npm/GitHub stats (not guessed)
- ✅ Recent data (2024)
- ✅ Actual benchmark numbers
- ✅ Cited sources
- ✅ Context-specific recommendations
- ✅ Clear action items

**Confidence Levels**:
- **High**: Well-established, clear winner, proven track record
- **Medium**: Multiple good options, depends on trade-offs
- **Low**: Emerging tech, limited data, rapidly changing

---

## Tips for Best Results

1. **Be Specific**: "form validation for React" > "forms"
2. **Add Context**: Use `--for="your-stack"` for tailored results
3. **Compare Mode**: Use `--compare` when evaluating options
4. **Save Results**: Use `--save=` to keep research for team
5. **Follow Up**: Use generated "Next Steps" for action items

---

## Related Commands

```bash
/plan-react [feature]    # Plan implementation after research
/compare [A] vs [B]      # Quick comparison (shortcut)
/brainstorm [topic]      # Explore ideas before deep research
/setup-testing           # Set up tests for chosen technology
```

---

**Remember**: Technology research should lead to **action**. After research, use `/plan` to create implementation strategy!
