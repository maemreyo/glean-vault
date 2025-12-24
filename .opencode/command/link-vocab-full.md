---
description: Link vocabulary with all features
agent: plan
model: anthropic/claude-3-5-sonnet-20241022
---

Link vocabulary with quotes cleaning, table conversion, and phase tagging enabled.

**Process:**

When user runs `/link-vocab-full <folder>`:

1. **Parse folder argument** (`$ARGUMENTS` or `$1`)
   - Default to `glean/10_Sources/Articles` if no argument
   - Validate folder exists

2. **Run dry-run first**:
   ```bash
   python3 glean/99_Tools/scripts/auto_link_vocab_v2.py \
     --folder "<folder>" \
     --dry-run \
     --backup-mode original
   ```

3. **Show comprehensive summary**:
   - Total files to be processed
   - Files requiring HTML table conversion
   - Files requiring quote cleaning
   - Expected number of new links
   - Files that need phase tagging

4. **Ask user confirmation**:
   - "Apply all features including clean quotes, convert tables, and add phase tags? (yes/no)"

5. **Apply all features**:
   ```bash
   python3 glean/99_Tools/scripts/auto_link_vocab_v2.py \
     --folder "<folder>" \
     --no-dry-run \
     --backup-mode original \
     --add-ref-tags
   ```

**Features enabled:**
- ✅ Strip existing links
- ✅ Clean curly quotes
- ✅ Convert HTML tables to Markdown
- ✅ Create new vocab links
- ✅ Add phase tags (for vocabulary files)

**Examples:**
```
/link-vocab-full glean/10_Sources/Articles
/link-vocab-full glean/20_Vocabulary
/link-vocab-full .
```

**Notes:**
- This is the "full pipeline" command
- Use for complete workflow in one pass
- Backup mode is `original` (space-saving)
