---
description: Process English grammar structure files in batches using internal knowledge only. Follows the English Tutor plugin standard.
---

This workflow automates the processing of English grammar structure files that are marked as `status: pending`. It replicates the behavior of the `/structure` command and the `structure-analyst` agent.

### ⛔ CRITICAL: INTERNAL KNOWLEDGE ONLY
- **DO NOT** use `web_search` or `web_fetch`.
- Use your internal linguistic training for formulas, components, CEFR, and common mistakes.
- If unsure, provide reasonable linguistic approximations or placeholders like `[context-dependent]`.

### Workflow Steps

1. **Discovery & Selection**
   - Find the directory containing structure files (priority: `glean/30_Structures`).
   - Find all `.md` files containing `status: pending`.
   - Ask the user for confirmation if the list is long, or process in batches.

2. **Template Preparation**
   - Read the standard template from `plugins/english-tutor/assets/tpl_Structure.md`.
   - Ensure you understand the 11-card flashcard requirement.

// turbo
3. **Batch Processing**
   - Group files into batches (recommended: 10-15 files).
   - For each file:
     - Read the file content.
     - Select a hierarchical tag from the commented list at the top.
     - Extract/Simplify the structure name from the filename.
     - Populate the `aliases` array in the frontmatter.
     - **Link Formatting:** Use `|` instead of `/` inside links (e.g., `[[take sb|st around]]`).
     - **Link Length:** Relations/Connections **MUST** be 2+ words (e.g., `[[make sense]]`).
     - Fill all sections using internal knowledge.
     - Generate all 11 flashcards.
     - Update `status: pending` to `status: done`.
     - Write the content back to the file.

4. **Validation (Defense in Depth)**
   - After each batch or at the end, run a check to ensure no web links or forbidden tool traces were added.
   - Run the validation script for structures: `.claude/scripts/validate_structure_output.sh`

5. **Final Reporting**
   - Provide a summary of processed files.
   - List any files that failed or need manual review.

### Usage
Run this workflow by asking Antigravity to "Process pending grammar structures" or "/english-grammar-analysis" if configured.
