# Auto-Link Vocabulary Script

**Path:** `glean/99_Tools/scripts/auto_link_vocab.py` (original) or `auto_link_vocab_v2.py` (new modular version)

This script automates the process of linking vocabulary and structure terms in your Obsidian Markdown files. It scans your vault for terms defined in `20_Vocabulary` and `30_Structures` and creates wikilinks (e.g., `[[path/to/term|term]]`) in your target files.

## Features

- **Smart Linking**: Finds terms from `20_Vocabulary` and `30_Structures` and links them
- **Alias Support**: Automatically reads `aliases` from frontmatter and links those variations
- **Recursive Scanning**: Finds vocabulary and structure terms in subdirectories
- **Markdown Table Support**: Escapes pipe character (`\|`) when inserting links in table rows
- **Safety First**: Optional `--dry-run` to preview changes
- **Configurable Backup**: Three backup strategies - original, session, or off
- **Quote Cleaning**: Integrated cleaning of curly quotes to straight quotes
- **Phase Tagging**: Add phase-based flashcard tags from `ref:` field in frontmatter

## Usage

Run the script from the vault root or any subdirectory (it auto-detects vault root).

### Option 1: OpenCode Custom Commands (Recommended for OpenCode users)

If you're using OpenCode, you can run commands directly from TUI:

```bash
# Link a single file or folder
/link-vocab glean/10_Sources/Articles/article.md

# Link with all features enabled
/link-vocab-full glean/10_Sources/Articles

# Manage backups
/vocab-backup

# Clean up redundant backups
/vocab-cleanup
```

**Benefits:**
- Integrated with OpenCode TUI
- Just type command, no need to remember paths
- Auto dry-run before applying changes
- Safety prompts for dangerous operations

### Option 2: Interactive Menu (Recommended for terminal use)

Run the interactive menu for a user-friendly interface:

```bash
python3 glean/99_Tools/scripts/vocab_linker.py
```

**Features:**
- Menu-driven interface with 8 options
- Remembers last settings (config file)
- Shows current configuration
- Confirmation prompts for all operations
- Color-coded output for readability

### Option 3: Direct Script Execution

For maximum control, run the script directly:

#### Original Script
```bash
python3 glean/99_Tools/scripts/auto_link_vocab.py [arguments]
```

#### New Modular Script (Recommended)
```bash
python3 glean/99_Tools/scripts/auto_link_vocab_v2.py [arguments]
```

## Arguments

### Target Selection
| Argument | Description |
| :--- | :--- |
| `--file <path>` | Process a single specific file |
| `--folder <path>` | Process all `.md` files in a folder recursively |

### Backup Strategy (NEW)
| Argument | Description |
| :--- | :--- |
| `--backup-mode original` | **Default.** Keep only the first (original) backup for each file. Saves space. |
| `--backup-mode session` | Create backup for each session (each run). Uses more space. |
| `--backup-mode off` | No backup. Dangerous, use with caution. |

### Processing Options
| Argument | Description |
| :--- | :--- |
| `--dry-run` | **Default.** Print proposed changes without modifying files |
| `--no-dry-run` | Apply changes to files (triggers backup) |
| `--strip-links` | **Default.** Strip existing vocab/structure links before re-linking |
| `--no-strip-links` | Keep existing links and add new ones |
| `--no-clean-quotes` | Skip cleaning curly quotes (default: clean) |

### Phase Tagging
| Argument | Description |
| :--- | :--- |
| `--add-ref-tags` | Add phase-based flashcard tags from `ref:` field in frontmatter |

### Restore & Management
| Argument | Description |
| :--- | :--- |
| `--list-backups [path]` | List available backups, optionally filter by path |
| `--restore <id>` | Restore a file from specific backup ID |
| `--restore-all <prefix>` | Restore all files from a session (timestamp prefix) |
| `--restore-original <path>` | Restore file(s) to their oldest (original) backup |
| `--cleanup-backups` | Remove redundant backups, keep only originals |

## Use Cases

### 1. Check changes before applying (Dry Run)
Always recommended as the first step.
```bash
python3 glean/99_Tools/scripts/auto_link_vocab_v2.py --file "glean/10_Sources/Articles/New Article.md"
```

### 2. Process a single article (Default backup mode)
Once satisfied, apply changes. Only the first backup is kept (saves space).
```bash
python3 glean/99_Tools/scripts/auto_link_vocab_v2.py --file "glean/10_Sources/Articles/New Article.md" --no-dry-run
```

### 3. Process an entire folder
Useful for batch processing imported articles.
```bash
python3 glean/99_Tools/scripts/auto_link_vocab_v2.py --folder "glean/10_Sources/Articles" --no-dry-run
```

### 4. Process with session backup mode
Create backup for each run (more history, uses more space).
```bash
python3 glean/99_Tools/scripts/auto_link_vocab_v2.py --folder "glean/10_Sources/Articles" --backup-mode session --no-dry-run
```

### 5. Process Folder + Auto-Tag Vocabulary
This command will **Link** your articles AND **Auto-Tag** your vocabulary files (using the 5-Phase System) in one go.
```bash
python3 glean/99_Tools/scripts/auto_link_vocab_v2.py \
  --folder "glean/10_Sources/Articles" \
  --add-ref-tags \
  --no-dry-run
```

### 6. Listing Backups
Check backup history.
```bash
python3 glean/99_Tools/scripts/auto_link_vocab_v2.py --list-backups
```
Output:
```
ID                        | Date                 | File                         | Changes
----------------------------------------------------------------------------------------------------
20251224_120000_abc123    | 2025-12-24 12:00:00  | New Article.md               | 45
```

### 7. Restoring a File
Restore using the backup ID.
```bash
python3 glean/99_Tools/scripts/auto_link_vocab_v2.py --restore 20251224_120000_abc123
```

### 8. Batch Restore (Undo Session)
Restore all files modified in a specific run.
```bash
python3 glean/99_Tools/scripts/auto_link_vocab_v2.py --restore-all 20251224_120000
```

### 9. Restore to Original Version
Reset a file or folder to its very first backup (pre-script state).
```bash
# Single file
python3 glean/99_Tools/scripts/auto_link_vocab_v2.py --restore-original "glean/10_Sources/Articles/MyFile.md"

# Entire folder
python3 glean/99_Tools/scripts/auto_link_vocab_v2.py --restore-original "glean/10_Sources/Articles"
```

### 10. Cleanup Redundant Backups (NEW)
Remove all but the original (oldest) backup for each file. Great for reclaiming space.
```bash
python3 glean/99_Tools/scripts/auto_link_vocab_v2.py --cleanup-backups
```
Output:
```
Deleted 243 redundant backup(s)
Kept 87 original backup(s)
```

## Key Differences: Original vs New Script

### Original Script Behavior
- Creates a backup **every time** `--no-dry-run` is run
- By default **restores to original** before linking (removes ALL edits, not just links)
- More disk space usage over time
- One file with all functionality

### New Script (v2) Behavior
- **Default backup mode: `original`** - only keeps the first backup (saves space!)
- **Default: strip-links without restore** - only removes vocab links, keeps manual edits
- Modular architecture with separate classes for each concern
- Configurable backup modes per use case
- Integrated quote cleaning (no subprocess dependency)

## Linking Behavior

### Default Mode (Recommended)
```bash
python3 glean/99_Tools/scripts/auto_link_vocab_v2.py --folder "Articles" --no-dry-run
```
Process:
1. Strip all existing vocab/structure links
2. Re-scan terms
3. Create new links with updated terms
4. **Preserves your manual edits** (only links are affected)

### Keep Existing Links Mode
```bash
python3 glean/99_Tools/scripts/auto_link_vocab_v2.py --folder "Articles" --no-strip-links --no-dry-run
```
Process:
1. Keep all existing links
2. Add links for newly found terms
3. May miss updates to existing term mappings

## Auto-Tag from Ref Field (5-Phase Mastery System)

Automatically add **Phase-based** flashcard tags based on the `ref:` field in vocabulary frontmatter.

**How it works:**
1. Reads `ref: [[Cam 19 Listening Test 04]]`
2. Generates base tag: `#flashcards/cam-19-listening-test-04`
3. Removes old header tags if present
4. Injects phase tags before specific cards:
   - **Foundation (Cards 1, 10):** `#flashcards/.../01-foundation`
   - **Activation (Cards 2, 3, 4):** `#flashcards/.../02-activation`
   - **Differentiation (Cards 6, 11, 12):** `#flashcards/.../03-differentiation`
   - **Mastery (Cards 5, 7, 8):** `#flashcards/.../04-mastery`
   - **Addition (Card 9):** `#flashcards/.../05-addition`

```bash
python3 glean/99_Tools/scripts/auto_link_vocab_v2.py --folder "glean/20_Vocabulary" --add-ref-tags --no-dry-run
```

## Technical Details

- **Backup Location:** `glean/99_Tools/backups/`
- **Inventory File:** `glean/99_Tools/backups/inventory.json`
- **Regex Logic:** Matches exact whole words (`\bterm\b`) to avoid partial matches

## Alias Support

The script reads the `aliases` field from YAML frontmatter. This handles:
- **Plurals:** `[passengers, cities, boxes]`
- **Verb Tenses:** `[developed, developing, develops]`
- **Word Families:** `[portionable, portionally, portioning]`
- **Possessives:** `[passenger's, city's]`
- **Irregular Forms:** `[went, gone, better, best]`
- **Shortened Forms:** `[approx., prep]`

**Example in `portion.md`:**
```yaml
---
aliases: [portions, portioned, portionable, portionally]
---
```

### Priority Rules
**Filename (Main Term)** always takes priority over aliases.
- If you have `confirm.md` and `confirmation.md` (with alias `confirm`), mentions of `confirm` link to `confirm.md`.

## Migration Tool (Original Script)

If you need to add `aliases: []` to existing notes:
```bash
python3 glean/99_Tools/scripts/auto_link_vocab.py --migrate-aliases --dry-run
python3 glean/99_Tools/scripts/auto_link_vocab.py --migrate-aliases --no-dry-run
```
