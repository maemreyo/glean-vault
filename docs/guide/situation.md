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
- **CLEANUP TAGS (CRITICAL):**
  1. Select hierarchical tag(s) from MASTER TAGGING SYSTEM comment
  2. Use formula: `#flashcards/ielts-<skill>/<PILLAR>/<subtopic>/<drill-type>`
  3. Place tag(s) above EACH flashcard header
  4. **DELETE the entire `<!-- MASTER TAGGING SYSTEM ... -->` comment block**
- **POPULATE ALIASES:**
  - Fill `aliases: [...]` with pattern variations/paraphrases
  - **DELETE the trailing comment** `# common variations...`
  - valid: `aliases: [contacting businesses, reaching out to companies]`
  - invalid: `aliases: [] # common variations...`
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
  - Ensure EVERY line in a flashcard block starts with `>` (if part of callout) or has NO empty lines between the header and the `?` separator.
- Mandatory: Include `?` separator between Q&A
- Use `==highlight==` for key terms (MANDATORY!)
- Write analysis in Vietnamese/English mix as per template
- Replace ALL {{PLACEHOLDER}} with actual content
```

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

| Tier | Card | Name | Tests |
|------|------|------|-------|
| 1: Daily | 1 | 3-Way Prediction Brainstorm | Paraphrasing imagination |
| 1: Daily | 2 | Verb + Noun Association | Collocation recall |
| 1: Daily | 3 | Signpost Detection | Signal word recognition |
| 2: Weekly | 4 | Reverse Matching | Audio → Option matching |
| 2: Weekly | 5 | Trap Identification | Negation signal detection |
| 2: Weekly | 6 | Confusion Differentiation | Similar option distinction |
| 2: Weekly | 7 | Context Cloze | Gap-fill comprehension |
| 3: Bi-weekly | 8 | Paraphrase Chain | Multi-level rewording |
| 3: Bi-weekly | 9 | Full Distractor Analysis | Error analysis |
| 3: Bi-weekly | 10 | Script-to-Option Mapping | Paraphrase identification |
| 3: Bi-weekly | 11 | 5-Second Prediction Drill | Speed recall |

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
- **Definition:** Core meaning của option
- **Denotation:** Literal meaning
- **Distractor:** Từ nghe giống nhưng KHÔNG PHẢI
- **Deep Dive:** Paraphrasing sâu hơn

### Imagination & Sensory
- **Visual:** Hình ảnh mental
- **Auditory:** Âm thanh đặc trưng
- **Action:** Hành động cụ thể
- **Collocations:** Verb+Noun, Noun+of+Noun, Adj+Noun patterns

### Traps & Distractors
- 2 traps với:
  - *Why it's tricky:* Tại sao nghe giống?
  - *Actual meaning:* Nghĩa thật là gì?

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
