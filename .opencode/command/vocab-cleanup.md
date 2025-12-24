---
description: Clean up redundant backups
agent: plan
model: anthropic/claude-3-5-sonnet-20241022
---

Remove redundant backups and keep only the original (oldest) backup for each file.

**Process:**

When user runs `/vocab-cleanup`:

1. **Check current backup status:**
   ```bash
   !python3 glean/99_Tools/scripts/auto_link_vocab_v2.py --list-backups
   ```

2. **Show analysis:**
   - Total number of backups
   - Estimated number of redundant backups (approx. total - unique files)
   - Estimated space to be freed
   - Files with multiple backups

3. **Ask for confirmation:**
   - "Found X backups. Keep only original backups and delete X redundant ones? (yes/no)"
   - Show affected files list

4. **Run cleanup:**
   ```bash
   python3 glean/99_Tools/scripts/auto_link_vocab_v2.py --cleanup-backups
   ```

5. **Show results:**
   - Number of backups deleted
   - Number of backups kept
   - Space saved (if available)
   - Cleanup location: `glean/99_Tools/backups/`

**Examples:**
```
/vocab-cleanup
# Run cleanup on all backups
```

**What gets deleted:**
- All backup versions except the FIRST (oldest) for each file
- Example: If file has 5 backups, keep 1st, delete 4
- Preserves: The original pre-script state

**When to use:**
- After multiple linking sessions
- When backup directory grows large
- Before archiving or sharing project

**Warning:**
- ⚠️ This operation cannot be undone (unless you have git)
- Consider using `/vocab-backup` first if unsure
- Original backups are always preserved
