# Auto-Link Vocabulary Script

**Path:** `glean/99_Tools/scripts/auto_link_vocab.py`

This script automates the process of linking vocabulary and structure terms in your Obsidian Markdown files. It scans your vault for terms defined in `20_Vocabulary` and `30_Structures` and creates wikilinks (e.g., `[[path/to/term|term]]`) in your target files.

## Features

- **Smart Linking:** Scans for terms and creates valid Obsidian links using vault-relative paths.
- **Table Support:** Correctly handles Markdown tables by escaping pipe characters (`|` -> `\|`) inside table rows, preserving table structure.
- **Safety First:** Defaults to `--dry-run` to show you what will happen without touching files.
- **Automatic Backups:** Automatically creates a backup of any file before modifying it (unless in dry-run mode).
- **Restore Capability:** Built-in commands to list backups and restore files to previous versions.

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

## Technical Details

- **Backup Location:** `glean/99_Tools/backups/`
- **Inventory File:** `glean/99_Tools/backups/inventory.json`
- **Regex Logic:** Matches exact whole words (`\bterm\b`) to avoid partial matches within other words.
