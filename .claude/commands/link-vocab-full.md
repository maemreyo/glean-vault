---
description: Full vocab linking pipeline with quotes, tables, and phase tags
argument-hint: [folder]
allowed-tools: AskUserQuestion, Bash(python3:*), Read, Write
---

# Full Vocabulary Linking Pipeline

Link vocabulary with quotes cleaning, table conversion, and phase tagging enabled.

## Step 1: Parse Folder Argument

Set the target folder:
- If user provided `$1`: use `$1`
- If no argument: use `glean/10_Sources/Articles` (default)

Validate folder exists before proceeding.

## Step 2: Run Dry-Run

Execute dry-run to analyze what will be done:

```bash
python3 glean/99_Tools/scripts/auto_link_vocab_v2.py \
  --folder "<FOLDER>" \
  --dry-run \
  --backup-mode original
```

## Step 3: Show Comprehensive Summary

Based on the dry-run output, present:

**Files Analysis:**
- Total files to be processed
- Files requiring HTML table conversion
- Files requiring quote cleaning
- Files that need phase tagging

**Expected Changes:**
- Number of new vocabulary links to be created
- Number of existing links that will be stripped and recreated

Display this summary clearly to the user.

## Step 4: User Confirmation

Use AskUserQuestion to confirm:

**Question:**
```
Apply all features including clean quotes, convert tables, and add phase tags?
```

**Header:** "Confirm"

**Options:**
- Yes (Proceed with full pipeline)
- No (Cancel operation)

## Step 5: Apply All Features (if confirmed)

If user selects "Yes", execute the full pipeline:

```bash
python3 glean/99_Tools/scripts/auto_link_vocab_v2.py \
  --folder "<FOLDER>" \
  --no-dry-run \
  --backup-mode original \
  --add-ref-tags
```

If user selects "No", cancel operation and report no changes made.

## Step 6: Report Results

After execution, show:
- Files processed
- Links created
- Tables converted
- Quotes cleaned
- Phase tags added
- Backup location (if applicable)

**Notes:**
- This is the "full pipeline" command for complete workflow in one pass
- Backup mode is `original` (space-saving)
- Strip existing links, clean curly quotes, convert HTML tables to Markdown, create new vocab links, add phase tags

**Examples:**
```
/link-vocab-full glean/10_Sources/Articles
/link-vocab-full glean/20_Vocabulary
/link-vocab-full .
```
