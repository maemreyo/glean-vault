---
description: Link vocabulary in files
---

Link vocabulary and structure terms to markdown files.

**Process:**

When user runs `/link-vocab <path>`:

1. **Parse path argument** (`$ARGUMENTS` or `$1`)
   - If argument is provided, use it as file or folder path
   - If no argument, ask user what they want to process:
     - Single file (provide path)
     - Entire folder (provide path)
     - Current directory

2. **Run dry-run first** (safety check):
   ```bash
   python3 glean/99_Tools/scripts/auto_link_vocab_v2.py --file "<path>" --dry-run
   ```
   OR for folder:
   ```bash
   python3 glean/99_Tools/scripts/auto_link_vocab_v2.py --folder "<path>" --dry-run
   ```

3. **Show dry-run summary**:
   - Number of files to be processed
   - Number of links to be created per file
   - Estimated changes

4. **Ask user confirmation**:
   - "Do you want to apply these changes? (yes/no)"
   - If "yes", proceed to step 5
   - If "no", stop

5. **Apply changes** with backup:
   ```bash
   # Default: backup-mode = original (saves space)
   python3 glean/99_Tools/scripts/auto_link_vocab_v2.py \
     --file "<path>" \
     --no-dry-run \
     --backup-mode original
   ```
   OR for folder:
   ```bash
   python3 glean/99_Tools/scripts/auto_link_vocab_v2.py \
     --folder "<path>" \
     --no-dry-run \
     --backup-mode original
   ```

**Variables:**
- `$ARGUMENTS` or `$1` = file or folder path (relative or absolute)

**Examples:**
```
/link-vocab glean/10_Sources/Articles/article.md
/link-vocab glean/20_Vocabulary
/link-vocab .
```

**Notes:**
- Backup mode is set to `original` (keeps only first backup)
- This saves disk space by default
- To use different backup mode, run script directly or use `/vocab-backup` command
