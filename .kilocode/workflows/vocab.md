# vocab.md

Batch process English vocabulary files with `status: pending`. Uses internal knowledge only.

**📋 NEW: Now using 14-card template with Synonym/Antonym quizzes (Cards 13 & 14)**
- See: `docs/obisidian-spaced-repetition/Quick_Guide_Cards_13_14_Synonym_Antonym_Quizzes.md`
- Template: `docs/obisidian-spaced-repetition/Vocabulary_Flashcard_Template_14_Cards.md`
- Example: `glean/20_Vocabulary/relax_example_14cards.md`

## ⛔ CRITICAL: NO WEB SEARCH

**DISABLED TOOLS:** `web_search`, `web_fetch` - NEVER use under ANY circumstances.

**WHY:** Vocabulary analysis must be consistent. You are an expert linguist with comprehensive training data.

**IF UNSURE:**
- Use best linguistic judgment
- Provide approximations: `~1400s`, `CEFR: B1-B2`
- Use placeholder: `[context-dependent]`
- NEVER attempt to search

---

## Steps

### 1. Discovery
Find the vocabulary directory:
1. Check: `glean/20_Vocabulary` (preferred)
2. Fallback: Search for `*Vocab*` folder
3. If not found: Ask user for path

### 2. Scan Pending Files
```bash
find '<directory_path>' -name '*.md' -exec grep -l '^status: pending' {} \;
```
- Use single quotes for paths with spaces
- Optional: Add `| head -n <limit>` to limit files

### 3. Batch Processing (Concurrent Agents)

Group files into batches of **10-15 files** per agent.

**For each batch, spawn a parallel agent with these instructions:**

```markdown
Process these vocabulary files CONCURRENTLY:

FILES TO PROCESS:
<list of absolute paths>

RULES:
- Use internal knowledge only (NO web search)
- Read each file → Extract word from filename
- **CLEANUP TAGS (CRITICAL):**
  1. Select ONE hierarchical tag from the comment block
  2. Place it at the top of the file
  3. **DELETE the entire `<!-- ... -->` comment block** (do not leave it in the file)
- **POPULATE ALIASES:**
  - Fill `aliases: [...]` with 5+ variations (Plurals, Tenses, POS, Synonyms)
  - **DELETE the trailing comment** `# Variations...` from the line
  - valid: `aliases: [accident, accidental, accidents]`
  - invalid: `aliases: [] # Variations...`
- Fill ALL 12 flashcards as defined below
- Update status: pending → done
- Write content back to file

FLASHCARD REQUIREMENTS (14 cards):

### Group 1: Foundation (Cards 1, 2, 10)
1. Meaning & Mental Model (include 🧠 Mental Model: VN explanation)
2. Production (Reverse) - Definition → Word
10. IPA Decoding (with tips for VN speakers)

### Group 2: Activation (Cards 3, 4)
3. Usage & Analysis (include 🔍 Analysis: why it works)
4. Collocations by Logic (group by type with VN notes)

### Group 3: Differentiation (Cards 6, 11)
6. Nuance Barrier (explain "The Barrier" - synonym comparison)
11. Mistake Hunter (common errors)

### Group 4: Mastery (Cards 5, 7, 8, 9)
5. Word Upgrade (Writer's Rewrite with "Why it works")
7. Scenario Reaction (include Director's Note)
8. Etymology Story (connect root to meaning)
9. Word Family & Roots

### Group 5: Synonym & Antonym Mastery (Cards 12, 13, 14) 🆕
12. Antonym Flip (include "Contrast" note)
13. Synonym Context Quiz (TEST: Choose correct synonym in specific context) 🆕
14. Antonym Context Quiz (TEST: Choose correct antonym in specific context) 🆕

 FORMAT RULES:
- Keep callout format: > [!info], > [!question]-, etc.
- Mandatory: Include `?` separator between Q&A
- Fill [[ word ]] with actual Obsidian links
- Write all content in English

### Card 13: Synonym Context Quiz Format
```markdown
### Card 13: Synonym Context Quiz

🧩 **Quiz:** In this context, which synonym of **{{WORD}}** is correct?

**Context:** <Provide a specific situation/sentence pattern>

**Options:**
- A) [[Synonym 1]]
- B) [[Synonym 2]]
- C) [[Synonym 3]]

?
> ✅ **Answer:** [[Correct Synonym]]
> 🧠 **Why:** <Explain which synonym fits best in this specific context (VN/EN mix)>
```

### Card 14: Antonym Context Quiz Format
```markdown
### Card 14: Antonym Context Quiz

🔃 **Quiz:** In this context, which antonym of **{{WORD}}** is correct?

**Context:** <Provide a specific situation/sentence pattern>

**Options:**
- A) [[Antonym 1]]
- B) [[Antonym 2]]
- C) [[Antonym 3]]

?
> ✅ **Answer:** [[Correct Antonym]]
> 🧠 **Why:** <Explain which antonym fits best in this specific context (VN/EN mix)>
```

### Tag for Group 5
Use: `#flashcards/[source-tag]/06-synonym-antonym-mastery`
```

### 4. Validation
After all batches complete:
```bash
# Check for web traces
grep -r "web_search\|http://" glean/20_Vocabulary/ | grep "status: done"

# Check card counts
for f in glean/20_Vocabulary/*.md; do
  grep -q "status: done" "$f" && echo "$f: $(grep -c '### Card' "$f") cards"
done
```

### 5. Report Summary
```
✅ Processed X/Y files successfully
📦 Batches executed: N
❌ Failed files: [list if any]
```

---

## Usage Examples

```
# Process all pending files
/vocab.md

# With custom path
Process vocabulary in workspace/english/20_Vocabulary

# Dry run (list only)
Show pending vocabulary files without processing

# Reprocess files needing Cards 13 & 14
/vocab.md
(Will add Synonym/Antonym quizzes to existing 12-card files)
```

## Example: Cards 13 & 14 Content

### For word: **relax**

**Card 13: Synonym Context Quiz**
```markdown
### Card 13: Synonym Context Quiz

🧩 **Quiz:** In this context, which synonym of **relax** is correct?

**Context:** You're working in an office. It's Friday evening. Everyone is finishing their tasks. Someone suggests staying late to do more work. Another person disagrees.

**Sentence to complete:** "No, let's just _____ for the weekend."

**Options:**
- A) [[rest]]
- B) [[unwind]]
- C) [[sleep]]

?
> ✅ **Answer:** [[unwind]]
> 🧠 **Why:** "Unwind" is perfect for releasing mental/physical tension after work (relaxing). "Rest" is about stopping activity, "sleep" is specific to sleeping. In this work context, "unwind" captures the idea of letting go of work stress.
```

**Card 14: Antonym Context Quiz**
```markdown
### Card 14: Antonym Context Quiz

🔃 **Quiz:** In this context, which antonym of **relax** is correct?

**Context:** A yoga instructor is encouraging students to focus on their pose. Some students are letting their muscles go loose.

**Sentence to complete:** "Don't _____, engage your core muscles!"

**Options:**
- A) [[tense]]
- B) [[stress]]
- C) [[tighten]]

?
> ✅ **Answer:** [[tense]]
> 🧠 **Why:** "Tense" refers to the physical state of muscles being tight/ready for action. It's the direct physical opposite of "relax" in this yoga/fitness context. "Stress" is mental, "tighten" is an action, while "tense" describes the state being changed.
```

## Guidelines for Cards 13 & 14

### Card 13: Synonym Context Quiz
1. **Purpose:** Test if learner can identify the RIGHT synonym for a specific context
2. **Format:** Multiple choice (3 options)
3. **Options:** Use synonyms listed in the Word Analysis section
4. **Answer:** Choose the one that BEST fits the context
5. **Explanation:** Explain WHY this synonym is correct vs others (VN/EN mix)

### Card 14: Antonym Context Quiz
1. **Purpose:** Test if learner can identify the RIGHT antonym for a specific context
2. **Format:** Multiple choice (3 options)
3. **Options:** Use antonyms listed in the Word Analysis section
4. **Answer:** Choose the one that BEST fits the context
5. **Explanation:** Explain WHY this antonym is correct vs others (VN/EN mix)

### What Makes Good Contexts for Cards 13-14?
- **Specific scenarios:** Office, sports, home, education, medical, travel
- **Clear contrast:** Options should be plausible but only one is contextually perfect
- **Vietnamese explanations:** Explain the nuance in VN to help learners understand
- **Distractors:** Include plausible wrong answers (synonyms that don't quite fit)

### When to Add Cards 13 & 14
- Words with **multiple synonyms** that have different nuances
- Words with **multiple antonyms** for different contexts
- Commonly confused words where context determines meaning
- Words where learners often make synonym/antonym errors

## Success Criteria

- [x] All `status: pending` → `status: done`
- [x] 14 flashcards per file (was 12, now includes Synonym/Antonym quizzes)
- [x] Cards 13 & 14 test synonym/antonym recognition in context
- [x] Aliases populated (5+ variations)
- [x] Obsidian links filled
- [x] No web search traces

---

## 🔄 Flashcard Structure Summary (14 Cards)

| Group | Card | Name | Tests |
|-------|------|------|-------|
| 1: Foundation | 1 | Meaning & Mental Model | Basic understanding |
| 1: Foundation | 2 | Production (Reverse) | Recall from definition |
| 1: Foundation | 10 | IPA Decoding | Pronunciation |
| 2: Activation | 3 | Usage & Analysis | Contextual usage |
| 2: Activation | 4 | Collocations by Logic | Word combinations |
| 3: Differentiation | 6 | Nuance Barrier | Synonym comparison |
| 3: Differentiation | 11 | Mistake Hunter | Error correction |
| 4: Mastery | 5 | Word Upgrade | Writing improvement |
| 4: Mastery | 7 | Scenario Reaction | Situational use |
| 4: Mastery | 8 | Etymology Story | Historical connection |
| 4: Mastery | 9 | Word Family & Roots | Morphology |
| 5: Synonym/Antonym | 12 | Antonym Flip | Direct antonym |
| 5: Synonym/Antonym | 13 | Synonym Context Quiz | 🆕 **TEST synonym** |
| 5: Synonym/Antonym | 14 | Antonym Context Quiz | 🆕 **TEST antonym** |

## 🆕 NEW: Group 5 - Synonym & Antonym Mastery

Purpose: Test learner's ability to **choose correct synonym/antonym** for specific contexts.

### When Required:
- Word has multiple synonyms with different nuances
- Word has multiple antonyms for different contexts
- Common confusion points for learners
- Context-dependent meaning

### Card 13: Synonym Context Quiz
- **Format:** Multiple choice (A, B, C)
- **Options:** 3 synonyms from Word Analysis section
- **Context:** Specific situation where one synonym is clearly best
- **Answer:** Most appropriate synonym for that context
- **Why:** Explanation in VN/EN why this is correct

### Card 14: Antonym Context Quiz
- **Format:** Multiple choice (A, B, C)
- **Options:** 3 antonyms from Word Analysis section
- **Context:** Specific situation where one antonym is clearly best
- **Answer:** Most appropriate antonym for that context
- **Why:** Explanation in VN/EN why this is correct
