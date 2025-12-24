# situation.md

Batch process IELTS situation/option files with `status: pending`. Uses internal knowledge only.

**📋 Template: 11-card Situation Flashcards (3 Tiers)**
- Template: `glean/99_Templates/tpl_Situation.md`
- Directory: `glean/40_Situation`

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

### 3. Batch Processing (Concurrent Agents)

Group files into batches of **5-7 files** per agent.

**For each batch, spawn a parallel agent with these instructions:**

```markdown
Process these situation files CONCURRENTLY:

FILES TO PROCESS:
<list of absolute paths>

RULES:
- Use internal knowledge only (NO web search)
- Read each file → Extract situation/option from filename
- **CLEANUP TAGS (CRITICAL - EACH CARD HAS UNIQUE TAG):**
  1. Select PILLAR & subtopic from MASTER TAGGING SYSTEM comment
  2. Use tag formula: `#flashcards/ielts-listening/<PILLAR>/<subtopic>/<tier>/<drill-type>`
  3. **EACH CARD must have its SPECIFIC tag suffix (see table below)**
  4. **DELETE the entire `<!-- MASTER TAGGING SYSTEM ... -->` comment block**
  5. **LOCATION RULE:** Tags must ONLY appear directly above their respective card headers in the `## 🧠 Spaced Repetition Flashcards` section. NEVER place flashcard tags in the YAML frontmatter or anywhere else.
  
  **⚠️ TAG SUFFIX PER CARD (MANDATORY):**
  | Card | Tier | Tag suffix |
  |------|------|------------|
  | 1 | daily | `daily/01-prediction` |
  | 2 | daily | `daily/02-keywords` |
  | 3 | daily | `daily/03-signpost` |
  | 4 | weekly | `weekly/01-reverse` |
  | 5 | weekly | `weekly/02-trap` |
  | 6 | weekly | `weekly/03-differentiate` |
  | 7 | weekly | `weekly/04-cloze` |
  | 8 | biweekly | `biweekly/01-chain` |
  | 9 | biweekly | `biweekly/02-full-trap` |
  | 10 | biweekly | `biweekly/03-script-match` |
  | 11 | biweekly | `biweekly/04-speed` |
  
  **Example (for PILLAR=social-leisure, subtopic=events):**
  - Card 1: `#flashcards/ielts-listening/social-leisure/events/daily/01-prediction`
  - Card 5: `#flashcards/ielts-listening/social-leisure/events/weekly/02-trap`
  - Card 11: `#flashcards/ielts-listening/social-leisure/events/biweekly/04-speed`
  **🔀 MULTI-TAGGING (when applicable):**
  - A single card MAY have MULTIPLE TAGS, separated by SPACE
  - Syntax: `tag1 tag2 tag3` (all on the same line)
  
  **When to use multi-tagging:**
  - ✅ Phrases fitting ≥2 pillars (e.g., "gym membership" → health-food + social-leisure)
  - ✅ Academic vocabulary appearing in multiple contexts (e.g., "research" → education + science-tech)
  - ❌ DO NOT exceed 4 tags per card for maintainability
  
  **Multi-tag example:**
  ```
  #flashcards/ielts-listening/social-leisure/events/daily/01-prediction #flashcards/ielts-listening/work-career/volunteering/daily/01-prediction
  ### Card 1: 3-Way Prediction Brainstorm
  ```
  

- **POPULATE ALIASES (MULTI-LINE LIST):**
  - Use the YAML list format (bullet points) for better readability.
  - Fill `aliases:` with variation 1, variation 2, etc. each on a new line with `-`.
  - **DELETE the trailing comment** `# common variations...`
  - Valid format:
    ```yaml
    aliases:
      - variation 1
      - variation 2
      - variation 3
    ```
- **FILL ANALYSIS SECTIONS** (before flashcards):
  - Option Profile → Replace all {{PLACEHOLDER}} variables
  - Target Analysis → Type of Info, Topic Category, 5D Framework
  - Imagination & Sensory → Visual/Auditory/Action, Collocations
  - Real Audio Phrases → 4+ realistic IELTS phrases
  - Traps & Distractors → 2 traps with explanations
  - Example Scripts → 2 IELTS-level audio scripts
- Fill ALL 11 flashcards as defined below
- Update status: pending → done
- Write content back to file

FLASHCARD REQUIREMENTS (11 cards):

### Tier 1: Daily Quick Review (Cards 1-3)
1. 3-Way Prediction Brainstorm - 3 paraphrasing scenarios (Action/Object/Abstract)
2. Verb + Noun Association - V+N collocations (không dùng từ gốc)
3. Signpost Detection - Before/After signpost words + Audio Cue

### Tier 2: Weekly Intensive (Cards 4-7)
4. Reverse Matching (Thực chiến) - Audio script → Option matching
5. Trap Identification - Negation signals + Other Traps
6. Confusion Differentiation - Compare similar options + Key Barrier
7. Context Cloze (Điền từ) - Fill in blank với Vietnamese translation

### Tier 3: Bi-weekly Mastery (Cards 8-11)
8. Paraphrase Chain - 4-level chain (Direct/Related/Contextual/Implicit)
9. Full Distractor Analysis - 2 distractors + why wrong
10. Script-to-Option Mapping - Highlight all paraphrases
11. 5-Second Prediction Drill - Speed challenge (2 paraphrases)

FORMAT RULES:
- Keep callout format: > [!info], > [!success], > [!fail], etc.
- **CRITICAL: NO EMPTY LINES INSIDE CALLOUTS OR BETWEEN BLOCKS.**
  - If a visual break is needed within a `> [!tip]` or similar, use a line with only `>`
  - **Visual Breaks (Mandatory):** Use a `>` line between logical items in lists (Cards 1, 5, 8, 10, 11) and before concluding summary points (e.g., before "Core Concept", "Logic Chain", "Key Barrier").
  - Ensure EVERY line in a flashcard block starts with `>` (if part of callout) or has NO empty lines between the header and the `?` separator.
- Mandatory: Include `?` separator between Q&A
- **Highlighting:** Use `==` pair to highlight important words/phrases (MANDATORY!). Do not use bold `**` for emphasis within the content, use `==` instead.
- Write analysis in Vietnamese/English mix as per template

- Replace ALL {{PLACEHOLDER}} with actual content

**💎 QUALITY & DETAIL RULES (MANDATORY):**
- **Highlighting:** Consistently use `==` to highlight key terms, important variables, or critical parts of an explanation.
- **Deep Analysis:** Avoid superficial 1-2 word answers. Provide *detailed, specific* explanations.
- **5D Framework:** "Definition" and "Denotation" must be full sentences explaining context, not just synonyms.
- **Imagination:** "Sensory Triggers" must describe *meaningful* scenes, sounds, and actions (e.g., "Hearing the *ching* sound of a cash register closing" vs just "sound of money").
- **Flashcards:**
  - **Why/Logic:** Explanations in "Logic Chain" and "Why" sections must be comprehensive. Explain *exactly how* the paraphrase works or *specifically why* a distractor is wrong.
  - **Distinctions:** Clearly articulate the *nuance* between confusing options, not just "A is X, B is Y".
- **Real Audio Phrases:** Must sound authentic to IELTS Listening (use contractions, natural fillers like "actually", "well", "you see").


### 4. Validation
After all batches complete:
```bash
# Check for web traces
grep -r "web_search\|http://" glean/40_Situation/ | grep "status: done"

# Check card counts (should be 11)
for f in glean/40_Situation/*.md; do
  grep -q "status: done" "$f" && echo "$f: $(grep -c '### Card' "$f") cards"
done

# Verify no placeholders remaining
grep -r '{{' glean/40_Situation/*.md

# Verify comment blocks removed
grep -r 'MASTER TAGGING SYSTEM' glean/40_Situation/*.md

# Check for empty lines in blocks (should be minimized)
# (Visual check recommended for '>' placeholder lines)
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
/situation.md

# With custom path
Process situation files in workspace/ielts/40_Situation

# Dry run (list only)
Show pending situation files without processing
```

---

## 🔄 Flashcard Structure Summary (11 Cards)

| Tier | Card | Name | Tag Suffix |
|------|------|------|------------|
| Daily | 1 | 3-Way Prediction Brainstorm | `daily/01-prediction` |
| Daily | 2 | Verb + Noun Association | `daily/02-keywords` |
| Daily | 3 | Signpost Detection | `daily/03-signpost` |
| Weekly | 4 | Reverse Matching | `weekly/01-reverse` |
| Weekly | 5 | Trap Identification | `weekly/02-trap` |
| Weekly | 6 | Confusion Differentiation | `weekly/03-differentiate` |
| Weekly | 7 | Context Cloze | `weekly/04-cloze` |
| Bi-weekly | 8 | Paraphrase Chain | `biweekly/01-chain` |
| Bi-weekly | 9 | Full Distractor Analysis | `biweekly/02-full-trap` |
| Bi-weekly | 10 | Script-to-Option Mapping | `biweekly/03-script-match` |
| Bi-weekly | 11 | 5-Second Prediction Drill | `biweekly/04-speed` |


---

## 📝 Analysis Sections Guide

### Option Profile
```markdown
> [!info] Option Profile
> **Option Letter:** ==A/B/C/D/E/F/G/H==
> **Option Text:** ==contacting local businesses==
> **Context:** *Volunteering at community center*
> **Source Test:** Cam 20 Listening Test 02
```

### Target Analysis (5D Framework)
- **Definition:** Core meaning của option (highlight keywords with `==`)
- **Denotation:** Literal meaning (highlight keywords with `==`)
- **Distractor:** Từ nghe giống nhưng KHÔNG PHẢI (highlight keywords with `==`)
- **Deep Dive:** Paraphrasing sâu hơn (highlight keywords with `==`)

### Imagination & Sensory
- **Visual:** Hình ảnh mental (use `==`)
- **Auditory:** Âm thanh đặc trưng (use `==`)
- **Action:** Hành động cụ thể (use `==`)
- **Collocations:** Verb+Noun, Noun+of+Noun, Adj+Noun patterns (highlight parts)

### Traps & Distractors
- 2 traps với:
  - *Why it's tricky:* Tại sao nghe giống? (use `==` for signals)
  - *Actual meaning:* Nghĩa thật là gì? (use `==` for core meaning)

### Example Scripts
- 2 IELTS-level audio scripts
- Với `→ **Match:** ==option text==`

---

## Success Criteria

- [x] All `status: pending` → `status: done`
- [x] 11 flashcards per file
- [x] Analysis sections filled (no {{placeholders}})
- [x] Aliases populated with variations
- [x] MASTER TAGGING comment block removed
- [x] No web search traces
