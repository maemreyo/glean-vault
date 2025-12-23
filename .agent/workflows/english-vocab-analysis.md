---
description: Process English vocabulary files in batches using internal knowledge only. Follows the English Tutor plugin standard.
---

This workflow automates the processing of English vocabulary files that are marked as `status: pending`. It replicates the behavior of the `/vocab` command and the `vocab-analyst` agent.

### ⛔ CRITICAL: INTERNAL KNOWLEDGE ONLY
- **DO NOT** use `web_search` or `web_fetch`.
- Use your internal linguistic training for IPA, Etymology, CEFR, and Collocations.
- If unsure, use approximations (e.g., `~1400s`, `CEFR: B1-B2`) or placeholders like `[context-dependent]`.

### Workflow Steps

1. **Discovery & Selection**
   - Find the directory containing vocabulary files (priority: `glean/20_Vocabulary`).
   - Find all `.md` files containing `status: pending`.
   - Ask the user for confirmation if the list is long, or process in batches.

2. **Template Preparation**
   - Read the standard template from `plugins/english-tutor/assets/tpl_Vocabulary.md`.
   - Ensure you understand the 12-card flashcard requirement.

// turbo
3. **Batch Processing**
   - Group files into batches (recommended: 10-15 files).
   - For each file:
     - Read the file content.
     - Select a hierarchical tag from the commented list at the top.
     - Extract the keyword from the filename.
     - Populate the `aliases` array in the frontmatter.
     - Fill all sections using internal knowledge.
     - Generate all 12 flashcards.
     - Update `status: pending` to `status: done`.
     - Write the content back to the file.

4. **Validation (Defense in Depth)**
   - After each batch or at the end, run a quick check to ensure no web links or "web_search" traces were accidentally added.
   - Run the validation script if it exists: `.claude/scripts/validate_vocab_output.sh`

5. **Final Reporting**
   - Provide a summary of processed files.
   - List any files that failed or need manual review.

### Usage
Run this workflow by asking Antigravity to "Process pending vocabulary files" or "/english-vocab-analysis" if configured.
