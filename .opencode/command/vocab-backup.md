---
description: Manage vocabulary backups
---

Manage vocabulary link backups - list, restore, or clean up.

**Process:**

When user runs `/vocab-backup`:

1. **Ask user which operation**:
   - 1. List all backups
   - 2. Restore from specific backup ID
   - 3. Restore to original (oldest backup)
   - 4. Restore session (batch restore)

2. **Execute selected operation:**

   **Option 1: List backups**
   ```bash
   python3 glean/99_Tools/scripts/auto_link_vocab_v2.py --list-backups
   ```
   - Show backup table with ID, date, file, changes count
   - Optionally filter by path: `/vocab-backup glean/10_Sources/Articles/article.md`

   **Option 2: Restore from ID**
   - Prompt for backup ID (or select from list)
   ```bash
   python3 glean/99_Tools/scripts/auto_link_vocab_v2.py --restore "<backup_id>"
   ```
   - Show file to be restored
   - Ask for confirmation

   **Option 3: Restore to original**
   - Prompt for file or folder path
   ```bash
   python3 glean/99_Tools/scripts/auto_link_vocab_v2.py --restore-original "<path>"
   ```
   - Show oldest backup date
   - Ask for confirmation

   **Option 4: Restore session**
   - Prompt for session prefix (timestamp)
   ```bash
   python3 glean/99_Tools/scripts/auto_link_vocab_v2.py --restore-all "<prefix>"
   ```
   - Show number of files to be restored
   - Ask for confirmation

**Examples:**
```
/vocab-backup
# Select operation 1 to list

/vocab-backup glean/10_Sources/Articles/article.md
# List backups for specific file
```

**Notes:**
- Use `/vocab-cleanup` to remove redundant backups
- Original backup mode means only one backup per file exists
- Session restore uses timestamp prefix (e.g., `20251224_120000`)
