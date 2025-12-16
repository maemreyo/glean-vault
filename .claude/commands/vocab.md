# /vocab - Vocabulary Template Auto-Fill

## Purpose

Automatically fills vocabulary information into the template based on filename. Quick single-pass research gathering all necessary data.

**"Fill vocabulary template"** - Auto-populate vocabulary cards with minimal effort.

## Aliases

```bash
/vocab [word]
/fill-vocab [word]
```

## Usage

```bash
# Use current file name as the word
/vocab

# Specify word explicitly
/vocab "serendipity"

# Single file with relative path
/vocab vocab/serendipity.md

# Batch mode with relative paths (auto-detected from multiple paths)
/vocab vocab/serendipity.md vocab/ephemeral.md vocab/ubiquitous.md

# Include advanced examples
/vocab vocab/ephemeral.md --examples=5

# Include etymology research
/vocab vocab/quintessential.md --etymology=deep

# Specify CEFR level
/vocab vocab/ubiquitous.md --cefr=C1

# Include usage frequency
/vocab vocab/plethora.md --frequency

# Batch with explicit flag (optional, auto-detected from multiple paths)
/vocab --batch
```

## Arguments

- `$ARGUMENTS`: One or more paths to vocabulary files (relative or absolute), or word to fill
  - Single argument: Process one file or word
  - Multiple arguments: Auto-trigger batch mode and process all files
  - No arguments: Use current filename
  - Relative paths are resolved from workspace root

## Flags

| Flag | Description | Example |
|------|-------------|---------|
| `--batch` | Process all .md files in Vocabulary folder | `--batch` |
| `--examples=N` | Number of examples to generate (default: 3) | `--examples=5` |
| `--etymology=level` | Etymology depth: basic/standard/deep | `--etymology=deep` |
| `--cefr=level` | Force CEFR level (A1-C2) | `--cefr=C1` |
| `--frequency` | Include frequency analysis | `--frequency` |
| `--collocations=N` | Number of collocations (default: 8) | `--collocations=12` |
| `--domain` | Specific domain (business/academic/technical) | `--domain=business` |
| `--template=path` | Custom template path | `--template=custom.md` |

---

## Core Methodology

**Reference**: `.claude/skills/vocabulary-research/SKILL.md`
**Dictionary APIs**: Oxford, Merriam-Webster, Etymonline, Thesaurus.com
**Primary Agent**: Vocab-Analyst (`.claude/agents/vocab-analyst.md`)
**Fallback Agent**: Researcher (`.claude/agents/researcher.md`)

### Single-Pass Information Gathering

```
Comprehensive Research
    ↓
All Data Sources Queried Simultaneously
    ↓
Template Populated in One Go
    ✅ Complete
```

**Key Principle**: Gather all information in parallel from multiple sources and fill the template completely in one pass.

---

## Workflow

Filling vocabulary for: **{{ if $ARGUMENTS }}$ARGUMENTS{{ else }}[current filename]{{ endif }}**

**Template**: {{ if --template provided }}`$TEMPLATE`{{ else }}`glean/99_Templates/tpl_Vocabulary.md`{{ endif }}

**Target file**: `glean/20_Vocabulary/[word].md`

{{ if --frequency }}
**Frequency analysis**: Enabled
{{ endif }}

{{ if --domain provided }}
**Domain focus**: $DOMAIN
{{ endif }}

**Duration**: 3-5 minutes (single pass)

---

### Step 1: Path Normalization & Batch Detection

**Goal**: Process arguments and determine execution mode.

#### 1.1 Analyze Arguments

```bash
# Count arguments
ARG_COUNT = count($ARGUMENTS)

# Determine mode
if ARG_COUNT == 0:
    MODE = "single"
    SOURCE = "current_file"
elif ARG_COUNT == 1 AND $ARGUMENTS[0] == "--batch":
    MODE = "batch_discovery"
    SOURCE = "vocabulary_folder"
elif ARG_COUNT == 1:
    MODE = "single"
    SOURCE = $ARGUMENTS[0]
else:  # ARG_COUNT > 1
    MODE = "batch_explicit"
    SOURCE = $ARGUMENTS[]
```

#### 1.2 Path Normalization

For each path in SOURCE:

```bash
# Normalize path
if path.is_relative():
    # Resolve from workspace root
    absolute_path = workspace_root + "/" + path
else:
    absolute_path = path

# Validate file exists
if not file_exists(absolute_path):
    error(f"File not found: {absolute_path}")
    continue

# Extract word from filename
word = basename(absolute_path).replace(".md", "")
```

#### 1.3 Word Extraction & Validation

{{ if MODE == "single" }}
{{ if SOURCE == "current_file" }}
- Extract from currently open file
- Remove .md extension
{{ else if SOURCE is path }}
- Extract from filename: `$SOURCE`
{{ else }}
- Use provided word: `$SOURCE`
{{ endif }}
{{ else }}
- Extract from each file in batch
{{ endif }}

**Process for each word**:
- Convert to lowercase
- Remove special characters
- Handle compound words (e.g., "well-being" → "wellbeing")
- Validate word existence in dictionary

**Output**: 
{{ if MODE == "single" }}
- Normalized word: `[WORD]`
- Target file: `[ABSOLUTE_PATH]`
{{ else }}
- Word list: `[WORD1, WORD2, WORD3, ...]`
- File list: `[PATH1, PATH2, PATH3, ...]`
- Processing queue ready
{{ endif }}

---

### Step 2: Comprehensive Data Collection

**Agent**: Vocab-Analyst (`.claude/agents/vocab-analyst.md`)
**Skill**: `.claude/skills/vocabulary-research/SKILL.md`

**Goal**: Gather ALL information needed from multiple sources simultaneously.

**Data Sources to Query**:

```bash
# Dictionary APIs (parallel queries)
- Oxford Dictionary API: definitions, IPA, CEFR
- Merriam-Webster: pronunciation, usage
- Collins Cobuild: collocations, frequency

# Etymology
- Etymonline: word origin and history

# Synonyms & Antonyms
- Thesaurus.com
- Power Thesaurus

# Collocations
- Just The Word
- Ozdic
- COCA data

# Backup
- Dictionary.com
- Wiktionary
```

**Information to Collect**:

1. **Basic Info**:
   - IPA transcription
   - Part(s) of speech
   - All definitions
   - CEFR level
   - Register (formal/informal)
   {{ if --frequency }}
   - Frequency data
   {{ endif }}

2. **Etymology & Word Family**:
   {{ if --etymology=deep }}
   - Detailed etymology with historical usage
   {{ else }}
   - Basic etymology
   {{ endif }}
   - Root word analysis
   - Related forms (noun/verb/adjective/adverb)
   - Common derivatives

3. **Usage & Examples**:
   {{ if --examples }}
   - Generate $EXAMPLES contextual examples
   {{ else }}
   - Generate 3 examples
   {{ endif }}
   - Different contexts for each meaning
   - Include translations

4. **Relations & Patterns**:
   - Synonyms (grouped by nuance)
   - Antonyms
   {{ if --collocations }}
   - $COLLOCATIONS common collocations
   {{ else }}
   - 8 common collocations
   {{ endif }}
   - Preposition patterns
   - Register variations

5. **Learning Materials**:
   - Common mistakes
   - Memory techniques
   - Practice suggestions
   - Flashcard content

---

### Step 3: Template Population

**Goal**: Fill all template sections with collected data in one complete pass.

**Template Sections Filled**:

- ✅ 📊 Meta Information (IPA, CEFR, register, frequency)
- ✅ 🌳 Root Word Analysis (etymology, word family)
- ✅ 💡 Root Meaning (basic definition)
- ✅ 💡 Context Meaning (detailed usage)
- ✅ 💡 Vietnamese Translation
- ✅ 💡 Nuances (subtle differences)
- ✅ 🔗 Relations (synonyms, antonyms)
- ✅ 📝 Examples (with translations)
- ✅ 📝 Collocations (common patterns)
- ✅ 📝 Common Mistakes
- ✅ 🎯 Learning Tips
- ✅ 🧠 Spaced Repetition Flashcards
- ✅ 🔖 Tags & Categories

**Quality Checks**:
- All `[[]]` placeholders preserved
- Information accurate from sources
- Examples varied and contextual
- Collocations common and useful
- No empty sections

---

## Completion

**Template Filled**: `glean/20_Vocabulary/[word].md`

**Verification Checklist**:
- [ ] All required fields filled
- [ ] IPA accurate
- [ ] Definitions clear and complete
- [ ] Examples varied
- [ ] Etymology included
- [ ] Collocations useful
- [ ] Learning aids comprehensive

### Post-Fill Actions

1. **Review**: Quick scan of filled information
2. **Personalize**: Add personal notes/connections
3. **Practice**: Complete practice exercises
4. **Spaced Repetition**: Import flashcards

---

## Batch Processing

**Triggered when**:
- Multiple paths provided: `/vocab vocab/word1.md vocab/word2.md vocab/word3.md`
- Explicit flag used: `/vocab --batch`

### Mode 1: Explicit Paths (Recommended)

**User provides paths directly**:

```bash
/vocab vocab/serendipity.md vocab/ephemeral.md vocab/ubiquitous.md
```

**Process**:
1. Normalize all paths to absolute
2. Validate each file exists
3. Extract word from each filename
4. Process sequentially with progress tracking

### Mode 2: Folder Discovery

**User triggers batch discovery**:

```bash
/vocab --batch
```

**Process**:
1. **File Discovery**:
   ```bash
   find glean/20_Vocabulary -name "*.md" -type f
   ```

2. **Filtering**:
   - Skip templates (files with `[ ]` in name or `tpl_` prefix)
   - Skip already filled files (no `[[]]` placeholders remaining)
   - Process remaining files

3. **Processing Queue**:
   - Sort files alphabetically
   - Process each file sequentially
   - Track success/failure for each

### Progress Tracking

For both modes, display progress:

```
📚 Vocabulary Batch Processing
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Processing: [1/5] serendipity.md
  ✓ Data collected from 8 sources
  ✓ Template populated
  ✓ Quality checks passed
  ⏱️  Completed in 3.2s

Processing: [2/5] ephemeral.md
  ✓ Data collected from 8 sources
  ✓ Template populated
  ✓ Quality checks passed
  ⏱️  Completed in 2.8s

Processing: [3/5] ubiquitous.md
  ✗ Word not found in dictionaries
  ⚠️  Skipped

Processing: [4/5] quintessential.md
  ✓ Data collected from 8 sources
  ✓ Template populated
  ✓ Quality checks passed
  ⏱️  Completed in 4.1s

Processing: [5/5] leverage.md
  ✓ Data collected from 8 sources
  ✓ Template populated
  ✓ Quality checks passed
  ⏱️  Completed in 3.5s

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Summary: 4/5 completed successfully
Failed: 1 (ubiquitous.md - word not found)
Total time: 13.6s
Average: 3.4s per word
```

### Error Handling

**Continue on error**: Don't stop batch processing if one file fails

```bash
# Log errors but continue
if error_occurred:
    log_error(file, error_message)
    continue_to_next_file()

# Report all errors at end
show_error_summary()
```

**Error log saved to**: `.vocab-batch-errors.log`

---

## Examples

```bash
# Quick fill for current word (file you have open)
/vocab

# Fill specific file by path
/vocab vocab/serendipity.md

# Batch mode - multiple files with relative paths
/vocab vocab/serendipity.md vocab/ephemeral.md vocab/ubiquitous.md

# Detailed research with examples
/vocab vocab/serendipity.md --examples=5 --etymology=deep

# Business English focus
/vocab vocab/leverage.md --domain=business --frequency

# Batch process entire folder
/vocab --batch

# Advanced level word with many collocations
/vocab vocab/ubiquitous.md --cefr=C2 --collocations=15

# Batch with options (applies to all files)
/vocab vocab/word1.md vocab/word2.md vocab/word3.md --examples=5 --frequency
```

---

## Error Handling

**Common Issues & Solutions**:

| Issue | Solution |
|-------|----------|
| Word not found | Try alternative spellings, use Wiktionary |
| Multiple etymologies | Include primary etymology, note variants |
| Phrasal verbs | Mark as "phrasal verb", handle separately |
| Technical terms | Provide domain-specific definitions |
| Missing CEFR level | Estimate based on frequency/complexity |

---

## Related Skills

- **vocabulary-research**: Core methodology for word research
- **template-filling**: Automated template population
- **contextual-examples**: Context-aware example generation
- **etymology-analysis**: Deep word origin research

---

## Notes

- Single-pass design for maximum efficiency
- All data sources queried simultaneously
- Complete template population in one go
- Average completion time: 3-5 minutes per word
- Suitable for batch processing large vocabulary lists