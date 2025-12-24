# situation.md

Batch process IELTS situation/option files with `status: pending`. Uses internal knowledge only.

**📋 Template: 15-card Situation Flashcards (4 Tiers)**
- Template: `glean/99_Templates/tpl_Situation.md`
- Directory: `glean/40_Situation`

## 📂 File Types Supported

| Type | Filename Pattern | Example | Cards |
|------|------------------|---------|-------|
| **Single-Option** | `the role of X is [option].md` | `the role of the volunteers is collecting feedback on events.md` | 11 cards |
| **Multi-Option (MCQ)** | `[question]? [opt1], [opt2] or [opt3].md` | `What is the most important requirement...? interpersonal skills, personal interest in the event or flexibility.md` | 15 cards |

---

## ⛔ CRITICAL: NO WEB SEARCH

**DISABLED TOOLS:** `web_search`, `web_fetch` - NEVER use under ANY circumstances.

**WHY:** Situation analysis must be consistent. You are an expert IELTS instructor with comprehensive training data.

**IF UNSURE:**
- Use best linguistic judgment
- Provide approximations for audio scripts
- Use placeholder: `[context-dependent]`
- NEVER attempt to search

---

## Steps

### 1. Discovery
Find the situation directory:
1. Check: `glean/40_Situation` (preferred)
2. Fallback: Search for `*Situation*` folder
3. If not found: Ask user for path

### 2. Scan Pending Files
```bash
find 'glean/40_Situation' -name '*.md' -exec grep -l '^status: pending' {} \;
```
- Use single quotes for paths with spaces
- Optional: Add `| head -n <limit>` to limit files

### 3. Filename Parsing (CRITICAL)

**Detect Question Type from Filename:**

```
SINGLE-OPTION: "the role of X is [option].md"
→ question_type: single
→ options_count: 1
→ Extract: option text after "is "

MULTI-OPTION: "[question]? [opt1], [opt2] or [opt3].md"
→ question_type: multi
→ options_count: 2-4
→ Extract: question stem (before "?"), options (split by ", " and " or ")
```

**Parsing Examples:**

| Filename | Type | Question Stem | Options |
|----------|------|---------------|---------|
| `the role of the volunteers is collecting feedback on events.md` | single | "the role of the volunteers is" | collecting feedback on events |
| `What is the most important requirement...? interpersonal skills, personal interest in the event or flexibility.md` | multi | "What is the most important requirement...?" | interpersonal skills, personal interest in the event, flexibility |

### 4. Batch Processing (Concurrent Agents)

Group files into batches of **5-7 files** per agent.

**For each batch, spawn a parallel agent with these instructions:**

```markdown
Process these situation files CONCURRENTLY:

FILES TO PROCESS:
<list of absolute paths>

RULES:
- Use internal knowledge only (NO web search)
- **STEP 1: DETECT QUESTION TYPE FROM FILENAME**
  - If filename contains "?" → `question_type: multi`
  - Otherwise → `question_type: single`
  - Count options (split by ", " and " or ")
  
- **STEP 2: UPDATE YAML FRONTMATTER**
  ```yaml
  question_type: single | multi
  options_count: 1 | 2 | 3 | 4
  ```

- **STEP 3: FILL QUESTION PROFILE**
  - **Question Stem:** Extract from filename
  - **Context:** Infer from topic (volunteering, events, etc.)
  - **Source Test:** From `ref:` field if available

- **STEP 4: FILL OPTIONS ANALYSIS TABLE**
  - For **single-option**: 1 row only, no "Correct Answer" line
  - For **multi-option**: 2-4 rows, include "Correct Answer" line
  - Each row: Option, Core Meaning, Paraphrase Keywords, Trap Potential

- **CLEANUP TAGS (CRITICAL - EACH CARD HAS UNIQUE TAG):**
  1. Select PILLAR & subtopic from MASTER TAGGING SYSTEM comment
  2. Use tag formula: `#flashcards/ielts-listening/<PILLAR>/<subtopic>/<tier>/<drill-type>`
  3. **EACH CARD must have its SPECIFIC tag suffix (see table below)**
  4. **DELETE the entire `<!-- MASTER TAGGING SYSTEM ... -->` comment block**
  5. **LOCATION RULE:** Tags must ONLY appear directly above their respective card headers
  
  **⚠️ TAG SUFFIX PER CARD (MANDATORY):**
  
  | Card | Tier | Tag suffix | MCQ Only? |
  |------|------|------------|-----------|
  | 1 | daily | `daily/01-prediction` | No |
  | 2 | daily | `daily/02-keywords` | No |
  | 3 | daily | `daily/03-signpost` | No |
  | 4 | recognition | `recognition/01-reverse` | No |
  | 5 | recognition | `recognition/02-trap` | No |
  | 6 | recognition | `recognition/03-differentiate` | No |
  | 7 | recognition | `recognition/04-cloze` | No |
  | 8 | weekly | `weekly/01-elimination` | **Yes** |
  | 9 | weekly | `weekly/02-cross-confusion` | **Yes** |
  | 10 | weekly | `weekly/03-validation` | **Yes** |
  | 11 | weekly | `weekly/04-chain` | No |
  | 12 | biweekly | `biweekly/01-full-trap` | No |
  | 13 | biweekly | `biweekly/02-script-match` | No |
  | 14 | biweekly | `biweekly/03-speed` | No |
  | 15 | biweekly | `biweekly/04-synthesis` | **Yes** |
  
  **FOR SINGLE-OPTION FILES:**
  - **SKIP Cards 8, 9, 10, 15** (MCQ-specific)
  - Total: **11 cards**
  - Renumber remaining cards sequentially

- **POPULATE ALIASES (MULTI-LINE LIST):**
  - Use the YAML list format (bullet points)
  - Fill `aliases:` with variations
  - **DELETE the trailing comment** `# common variations...`

- **FILL ALL ANALYSIS SECTIONS** (before flashcards):
  - Question Profile → Question Type, Question Stem, Context, Source
  - Options Analysis → Table with all options
  - Deep Analysis → Type of Info, Topic Category, 5D Framework
  - Imagination & Sensory → Visual/Auditory/Action, Collocations
  - Real Audio Phrases → 4+ realistic IELTS phrases
  - Traps & Distractors → 2 traps with explanations
  - Example Scripts → 2 IELTS-level audio scripts

- Fill ALL flashcards (11 for single, 15 for multi)
- Update status: pending → done
- Write content back to file

FORMAT RULES:
- Keep callout format: > [!info], > [!success], > [!fail], etc.
- **CRITICAL: NO EMPTY LINES INSIDE CALLOUTS**
- Mandatory: Include `?` separator between Q&A
- **Highlighting:** Use `==` pair to highlight important words (MANDATORY!)
- Replace ALL {{PLACEHOLDER}} with actual content
```

### 5. Validation
After all batches complete:
```bash
# Check for web traces
grep -r "web_search\|http://" glean/40_Situation/ | grep "status: done"

# Check card counts
for f in glean/40_Situation/*.md; do
  grep -q "status: done" "$f" && echo "$f: $(grep -c '### Card' "$f") cards"
done

# Verify no placeholders remaining
grep -r '{{' glean/40_Situation/*.md

# Verify comment blocks removed
grep -r 'MASTER TAGGING SYSTEM' glean/40_Situation/*.md
```

### 6. Report Summary
```
✅ Processed X/Y files successfully
📦 Batches executed: N
📊 Single-option files: X (11 cards each)
📊 Multi-option files: Y (15 cards each)
❌ Failed files: [list if any]
```

---

## 🔄 Flashcard Structure Summary (15 Cards)

| Tier | Card | Name | Tag Suffix | MCQ Only? |
|------|------|------|------------|-----------|
| **Daily** | 1 | 3-Way Prediction Brainstorm | `daily/01-prediction` | No |
| **Daily** | 2 | Verb + Noun Association | `daily/02-keywords` | No |
| **Daily** | 3 | Signpost Detection | `daily/03-signpost` | No |
| **Recognition** | 4 | Reverse Matching | `recognition/01-reverse` | No |
| **Recognition** | 5 | Trap Identification | `recognition/02-trap` | No |
| **Recognition** | 6 | Confusion Differentiation | `recognition/03-differentiate` | No |
| **Recognition** | 7 | Context Cloze | `recognition/04-cloze` | No |
| **Weekly** | 8 | Option Elimination Drill | `weekly/01-elimination` | **Yes** |
| **Weekly** | 9 | Cross-Option Confusion | `weekly/02-cross-confusion` | **Yes** |
| **Weekly** | 10 | Answer Validation | `weekly/03-validation` | **Yes** |
| **Weekly** | 11 | Paraphrase Chain | `weekly/04-chain` | No |
| **Bi-weekly** | 12 | Full Distractor Analysis | `biweekly/01-full-trap` | No |
| **Bi-weekly** | 13 | Script-to-Option Mapping | `biweekly/02-script-match` | No |
| **Bi-weekly** | 14 | 5-Second Prediction Drill | `biweekly/03-speed` | No |
| **Bi-weekly** | 15 | Complete Question Synthesis | `biweekly/04-synthesis` | **Yes** |

---

## 📝 Analysis Sections Guide

### Question Profile
```markdown
> [!info] 📋 Question Profile
> **Question Type:** ==single== / ==multi==
> **Question Stem:** ==What is the most important requirement for volunteers?==
> **Context:** *Volunteering at community festivals*
> **Source Test:** Cam 20 Listening Test 02
```

### Options Analysis (NEW)
```markdown
> [!abstract] 🔀 Options Analysis
>
> | # | Option | Core Meaning | Paraphrase Keywords | Trap Potential |
> |---|--------|--------------|---------------------|----------------|
> | A | ==interpersonal skills== | Khả năng giao tiếp | work with people | ⚠️ High |
> | B | ==personal interest== | Đam mê cá nhân | passionate about | ⚠️ Medium |
> | C | ==flexibility== | Linh hoạt | adapt, change plans | ⚠️ High |
>
> **✅ Correct Answer:** ==C. flexibility==
```

### Deep Analysis (5D Framework)
- **Definition:** Core meaning (highlight keywords with `==`)
- **Denotation:** Literal meaning (highlight keywords with `==`)
- **Distractor:** Similar-sounding but wrong (highlight keywords with `==`)
- **Deep Dive:** Advanced paraphrasing (highlight keywords with `==`)

---


## 💎 Quality & Formatting Rules

### Format Rules
- **Callout Format:** Keep `> [!info]`, `> [!success]`, `> [!fail]`, etc. exactly as is.
- **CRITICAL: NO EMPTY LINES INSIDE CALLOUTS OR BETWEEN BLOCKS.**
  - If a visual break is needed within a block, use a line with only `>`.
  - **Visual Breaks (Mandatory):** Use a `>` line between logical items in lists and before concluding summary points.
  - Ensure EVERY line in a flashcard block starts with `>` or has NO empty lines between header and `?`.
- **Separator:** Mandatory `?` separator between Q&A.
- **Highlighting:** Use `==` pair to highlight important words/phrases (MANDATORY!). Do NOT use bold `**` for emphasis within content.
- **Language:** Analysis in Vietnamese/English mix as per template.
- **Placeholders:** Replace ALL `{{PLACEHOLDER}}` with actual content.

### Quality & Detail Rules (MANDATORY)
- **Highlighting:** Consistently use `==` to highlight key terms, important variables, or critical parts of an explanation.
- **Deep Analysis:** Avoid superficial 1-2 word answers. Provide *detailed, specific* explanations.
- **5D Framework:** "Definition" and "Denotation" must be full sentences explaining context, not just synonyms.
- **Imagination:** "Sensory Triggers" must describe *meaningful* scenes, sounds, and actions (e.g., "Hearing the *ching* sound of a cash register closing" vs just "sound of money").
- **Flashcards:**
  - **Why/Logic:** Explanations in "Logic Chain" and "Why" sections must be comprehensive. Explain *exactly how* the paraphrase works or *specifically why* a distractor is wrong.
  - **Distinctions:** Clearly articulate the *nuance* between confusing options, not just "A is X, B is Y".
- **Real Audio Phrases:** Must sound authentic to IELTS Listening (use contractions, natural fillers like "actually", "well", "you see").

---

## Success Criteria

- [x] All `status: pending` → `status: done`
- [x] 11 flashcards for single-option files
- [x] 15 flashcards for multi-option files
- [x] Options Analysis table filled correctly
- [x] Analysis sections filled (no {{placeholders}})
- [x] Aliases populated with variations
- [x] MASTER TAGGING comment block removed
- [x] No web search traces
