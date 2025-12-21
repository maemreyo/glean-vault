# Auto-Link Vocabulary Script

**Path:** `glean/99_Tools/scripts/auto_link_vocab.py`

This script automates the process of linking vocabulary and structure terms in your Obsidian Markdown files. It scans your vault for terms defined in `20_Vocabulary` and `30_Structures` and creates wikilinks (e.g., `[[path/to/term|term]]`) in your target files.

## Features

- **Smart Linking**: Finds terms from `20_Vocabulary` and `30_Structures` and links them.
- **Alias Support**: Automatically reads `aliases` from a note's Frontmatter (YAML) and links those variations to the main note.
- **Recursive Scanning**: Finds vocabulary and structure terms in subdirectories.
- **Markdown Table Support**: Automatically escapes the pipe character (`\|`) when inserting links inside table rows to prevent breaking the table layout.
- **Safety First**: Optional `--dry-run` to preview changes.
- **Backup & Restore**: Automatically creates backups before modifying files. Includes a robust inventory system to list and restore from previous versions.
- **Migration Tool**: Includes a `--migrate-aliases` flag to batch-add missing alias fields to existing notes.

## Usage

Run the script from the vault root or any subdirectory (it auto-detects vault root).

```bash
python3 glean/99_Tools/scripts/auto_link_vocab.py [arguments]
```

### Arguments

| Argument | Description |
| :--- | :--- |
| `--file <path>` | Process a single specific file. |
| `--folder <path>` | Process all `.md` files in a folder recursively. |
| `--dry-run` | **Default.** Print proposed changes to stdout without modifying files. |
| `--no-dry-run` | Apply changes to the files. **Triggers automatic backup.** |
| `--list-backups [path]` | List available backups. Optionally filter by original file path. |
| `--restore <id>` | Restore a specific backup by its ID. |
| `--restore-all <timestamp>` | Restore all files from a specific session (batch undo). |
| `--restore-original <path>` | Restore a file or folder to its oldest backup (pre-script state). |
| `--restore-before-link` | **Workflow:** Restore files to original before linking. |
| `--clean-quotes` | **Workflow:** Run `clean_quotes.py` before linking. |

## Use Cases

### 1. Check changes before applying (Dry Run)
Always recommended as the first step.
```bash
python3 glean/99_Tools/scripts/auto_link_vocab.py --file "glean/10_Sources/Articles/New Article.md"
```

### 2. Process a single article
Once satisfied with the dry run, apply the changes.
```bash
python3 glean/99_Tools/scripts/auto_link_vocab.py --file "glean/10_Sources/Articles/New Article.md" --no-dry-run
```

### 3. Process an entire folder
Useful for batch processing a new set of imported articles.
```bash
python3 glean/99_Tools/scripts/auto_link_vocab.py --folder "glean/10_Sources/Articles" --no-dry-run
```

### 4. Listing Backups
If you suspect a mistake was made, check the backup history.
```bash
python3 glean/99_Tools/scripts/auto_link_vocab.py --list-backups
```
*Output Example:*
```
ID                        | Date                 | File                                     | Changes
----------------------------------------------------------------------------------------------------
20251219_113004_1b8b0f    | 2025-12-19 11:30:04  | The giant heat pumps...md                | 2
```

### 5. Restoring a File
Restore a file to a previous state using the ID found in the list.
```bash
python3 glean/99_Tools/scripts/auto_link_vocab.py --restore 20251219_113004_1b8b0f
```

### 6. Batch Restore (Undo All)
If you processed a folder and want to revert **every file** modified in that specific run:
```bash
# Use the first part of the backup ID (the timestamp portion)
python3 glean/99_Tools/scripts/auto_link_vocab.py --restore-all 20251219_113004
```

### 7. Restore to Original Version
If you want to completely reset a **file** or **folder** to its state before you ever used this script (the very first backup):

**Restore a single file:**
```bash
python3 glean/99_Tools/scripts/auto_link_vocab.py --restore-original "glean/10_Sources/Articles/MyFile.md"
```

**Restore all files in a folder:**
```bash
python3 glean/99_Tools/scripts/auto_link_vocab.py --restore-original "glean/10_Sources/Articles"
```
```
This will restore **all files** in the folder (and subfolders) that have backup history to their very first backed-up version.

### 8. Workflow Integration: Full Pipeline
For a complete workflow that restores files, cleans quotes, and then links vocabulary in one command:

```bash
python3 glean/99_Tools/scripts/auto_link_vocab.py \
  --folder "glean/10_Sources/Articles" \
  --restore-before-link \
  --clean-quotes \
  --no-dry-run
```

**Pipeline steps:**
1. 🔄 **Restore files** to their original pre-script state
2. 🧹 **Clean quotes** (convert Unicode curly quotes to straight quotes)
3. 🔗 **Link vocabulary** (create wikilinks to terms)

Each step displays a visual indicator and progress information.

**Individual workflow flags:**
```bash
# Only restore before linking
python3 glean/99_Tools/scripts/auto_link_vocab.py --folder "glean/10_Sources/Articles" --restore-before-link --no-dry-run

# Only clean quotes before linking
python3 glean/99_Tools/scripts/auto_link_vocab.py --folder "glean/10_Sources/Articles" --clean-quotes --no-dry-run
```


## Technical Details

- **Backup Location:** `glean/99_Tools/backups/`
- **Inventory File:** `glean/99_Tools/backups/inventory.json`
- **Regex Logic:** Matches exact whole words (`\bterm\b`) to avoid partial matches within other words.

## Alias Support

The script reads the `aliases` field from the YAML frontmatter of your vocabulary and structure notes. This is the recommended way to handle:
- **Plurals:** `[passengers, cities, boxes]`
- **Verb Tenses:** `[developed, developing, develops]`
- **Word Families (POS):** `[portionable, portionally, portioning]`
- **Possessives:** `[passenger's, city's]`
- **Irregular Forms:** `[went, gone, better, best]`
- **Shortened Forms:** `[approx., prep]`

**Example Frontmatter in `portion.md`:**
```yaml
---
aliases: [portions, portioned, portionable, portionally]
---
```

When the script finds any of these variations in an article, it will link it back to the parent note using the original text: `[[glean/20_Vocabulary/portion|portionable]]`.

### Priority Rules
If there is a conflict between a note's filename and an alias from another note, the **Filename (Main Term)** always takes priority.
- **Example:** If you have `confirm.md` and `confirmation.md` (with alias `confirm`), any mention of `confirm` will link to `confirm.md` directly.


## Migration Tool

If your existing notes are missing the `aliases` field, you can add it to all files in bulk:

```bash
# Preview the migration
python3 glean/99_Tools/scripts/auto_link_vocab.py --migrate-aliases --dry-run

# Run the migration (adds aliases: [] to all files lacking it)
python3 glean/99_Tools/scripts/auto_link_vocab.py --migrate-aliases --no-dry-run
```

