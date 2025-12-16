# /compare - Quick Technology Comparison

## Purpose

Quickly compare 2-3 technologies or libraries with a side-by-side breakdown. Faster than full `/research` when you just need to decide between specific options.

## Usage

```bash
/compare [option A] vs [option B]
/compare [A] vs [B] vs [C]
/compare --for="context" [A] vs [B]
```

## Arguments

- `$ARGUMENTS`: Technologies to compare in format "A vs B" or "A vs B vs C"

**Examples**:
```bash
/compare React vs Vue
/compare Vitest vs Jest vs Playwright
/compare Prisma vs Drizzle
/compare --for="next.js" NextAuth vs Clerk
```

---

## Workflow

Quick comparison for: **$ARGUMENTS**

### Step 1: Parse Options

Extract technologies from "A vs B vs C" format.

### Step 2: Web Search (Brief)

For each option, gather:
- Current version
- npm downloads/week
- GitHub stars
- Bundle size
- Key features

### Step 3: Generate Comparison Table

Create side-by-side comparison with decision matrix.

---

## Output Format

```markdown
## ⚖️ Quick Comparison: [A] vs [B] vs [C]

**Context**: [Your context if --for flag used]  
**Updated**: [Date]

---

### 📊 At a Glance

| Aspect | [Option A] | [Option B] | [Option C] |
|--------|-----------|-----------|-----------|
| **Downloads/week** | 1.2M | 800K | 150K |
| **GitHub Stars** | 50K ⭐ | 35K ⭐ | 8K ⭐ |
| **Bundle Size** | 12KB | 45KB | 8KB |
| **First Release** | 2018 | 2015 | 2022 |
| **Latest Update** | 2 days ago | 1 week ago | Yesterday |
| **TypeScript** | ✅ Native | ✅ DT | ✅ Native |
| **License** | MIT | MIT | MIT |

**Popularity**: [A] > [B] > [C]  
**Maturity**: [B] > [A] > [C]  
**Modern**: [C] > [A] > [B]

---

### ⚡ Performance

| Metric | [Option A] | [Option B] | [Option C] |
|--------|-----------|-----------|-----------|
| **Speed** | ⚡ Fast | 🐌 Slow | ⚡⚡ Fastest |
| **Bundle Impact** | 🟢 Small | 🔴 Large | 🟢 Tiny |
| **Memory** | Normal | High | Low |

**Winner**: [Option C] - [Reasoning]

---

### 😊 Developer Experience

| Aspect | [Option A] | [Option B] | [Option C] |
|--------|-----------|-----------|-----------|
| **API Design** | 😊 Great | 😐 OK | 😍 Excellent |
| **Documentation** | 📚 Excellent | 📚 Good | 📚 Growing |
| **Learning Curve** | Easy | Hard | Medium |
| **Error Messages** | ✅ Clear | ⚠️ Cryptic | ✅ Helpful |
| **TypeScript DX** | ✅ Great | ⚠️ OK | ✅ Excellent |

**Winner**: [Option A/C] - [Reasoning]

---

### 🌟 Features

| Feature | [Option A] | [Option B] | [Option C] |
|---------|-----------|-----------|-----------|
| [Key Feature 1] | ✅ Yes | ✅ Yes | ❌ No |
| [Key Feature 2] | ✅ Yes | ❌ No | ✅ Yes |
| [Key Feature 3] | ⚠️ Partial | ✅ Yes | ✅ Yes |
| [Key Feature 4] | ✅ Yes | ✅ Yes | 🚧 Planned |

**Feature Richness**: [B] > [A] > [C]

---

### 🎯 Best Use Cases

**[Option A]**: ⭐ Recommended for
- ✅ [Use case 1]
- ✅ [Use case 2]
- ❌ NOT for: [scenario]

**[Option B]**: Recommended for
- ✅ [Use case 1]
- ✅ [Use case 2]
- ❌ NOT for: [scenario]

**[Option C]**: Recommended for
- ✅ [Use case 1]
- ✅ [Use case 2]
- ❌ NOT for: [scenario]

---

### 💰 Pricing (if applicable)

| Tier | [Option A] | [Option B] | [Option C] |
|------|-----------|-----------|-----------|
| **Free** | ✅ Unlimited | ✅ Up to 10K users | ✅ OSS |
| **Paid** | - | $29/mo | $99/mo |
| **Enterprise** | - | Custom | Custom |

---

### ✅ Pros & ❌ Cons

**[Option A]**:
- ✅ [Pro 1]
- ✅ [Pro 2]
- ❌ [Con 1]
- ❌ [Con 2]

**[Option B]**:
- ✅ [Pro 1]
- ✅ [Pro 2]
- ❌ [Con 1]
- ❌ [Con 2]

**[Option C]**:
- ✅ [Pro 1]
- ✅ [Pro 2]
- ❌ [Con 1]
- ❌ [Con 2]

---

### 🏆 Winner: [Recommended Option]

**For [your context]**: Choose **[Option]** ⭐

**Why**:
1. [Key reason #1]
2. [Key reason #2]
3. [Key reason #3]

**When to use alternatives**:
- Use [Option B] if [condition]
- Use [Option C] if [condition]

**Confidence**: [High/Medium/Low]

---

### 🔄 Migration Between Options

**From [A] to [B]**: [Easy/Hard] - [Time estimate]  
**From [B] to [C]**: [Easy/Hard] - [Time estimate]  
**From [C] to [A]**: [Easy/Hard] - [Time estimate]

**Can you use multiple?** [Yes/No] - [Explanation]

---

### 📚 Quick Links

**[Option A]**:
- 📖 [Docs](url) | 📦 [npm](url) | 💻 [GitHub](url)

**[Option B]**:
- 📖 [Docs](url) | 📦 [npm](url) | 💻 [GitHub](url)

**[Option C]**:
- 📖 [Docs](url) | 📦 [npm](url) | 💻 [GitHub](url)

---

### 🚀 Next Steps

1. **Try the winner**: [Quick start command]
2. **Read more**: Use `/research [winner]` for deep dive
3. **Plan implementation**: `/plan-react "add [feature] with [winner]"`

---

**Need more details?** Use `/research [option]` for comprehensive analysis.
```

---

## Examples

### Example 1: Test Runners

**Input**: `/compare Vitest vs Jest`

**Output**:
```
⚖️ Vitest vs Jest

Speed: Vitest ⚡⚡ (5-10x faster) vs Jest 🐌
DX: Vitest 😍 (modern) vs Jest 😊 (familiar)
Maturity: Jest ⭐ (battle-tested) vs Vitest 💫 (newer)

Winner: Vitest for new projects
Use Jest: If migrating is too costly
```

### Example 2: State Management

**Input**: `/compare --for="next.js 14" Redux vs Zustand vs Jotai`

**Output**:
- Redux: 🔴 Large bundle, 😐 OK DX, ✅ Mature
- Zustand: 🟢 Tiny, 😊 Great DX, ✅ SSR-friendly
- Jotai: 🟢 Small, 😍 Excellent DX, ⚠️ Learning curve

**For Next.js 14**: Zustand (best balance)

### Example 3: Databases

**Input**: `/compare Prisma vs Drizzle`

**Output**:
- Prisma: ✅ Mature, ❌ Not edge-ready, 😊 Great DX
- Drizzle: ✅ Edge-ready, ✅ Fast, 💫 Newer

**For Edge/Serverless**: Drizzle
**For Traditional**: Prisma

---

## When to Use

✅ **Use `/compare`** when:
- You have 2-3 specific options
- Need quick decision
- Already know what to compare
- Time-sensitive decision

❌ **Use `/research` instead** when:
- Don't know options yet
- Need comprehensive analysis
- Want to explore ecosystem
- Building documentation

---

## Related Commands

```bash
/research [topic]        # Comprehensive research
/research --compare      # Research + comparison
/brainstorm [topic]      # Explore options first
/plan-react [feature]    # Implement after deciding
```

---

**Pro Tip**: Use `/compare` to narrow down, then `/research [winner]` for implementation details!
