# vocab.md

Batch process English vocabulary files with `status: pending`. Uses internal knowledge only.

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

FLASHCARD REQUIREMENTS (12 cards):
1. Meaning & Mental Model (include 🧠 Mental Model: VN explanation)
2. Production (Reverse) - Definition → Word
3. Usage & Analysis (include 🔍 Analysis: why it works)
4. Collocations by Logic (group by type with VN notes)
5. Word Upgrade (Writer's Rewrite with "Why it works")
6. Nuance Barrier (explain "The Barrier")
7. Scenario Reaction (include Director's Note)
8. Etymology Story (connect root to meaning)
9. Word Family & Roots
10. IPA Decoding (with tips for VN speakers)
11. Mistake Hunter (common errors)
12. Antonym Flip (include "Contrast" note)

FORMAT RULES:
- Keep callout format: > [!info], > [!question]-, etc.
- Mandatory: Include `?` separator between Q&A
- Fill [[ word ]] with actual Obsidian links
- Write all content in English
```

### 4. Validation
After all batches complete:
```bash
# Check for web traces
grep -r "web_search\|http://" glean/20_Vocabulary/ | grep "status: done"

# Check card counts
for f in glean/20_Vocabulary/*.md; do
  grep -q "status: done" "$f" && echo "$f: $(grep -c '#### Card' "$f") cards"
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
```

## Success Criteria

- [x] All `status: pending` → `status: done`
- [x] 12 flashcards per file
- [x] Aliases populated
- [x] Obsidian links filled
- [x] No web search traces
