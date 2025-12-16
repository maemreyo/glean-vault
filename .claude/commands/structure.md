# /structure - Grammar Structure Template Auto-Fill

## Purpose

Automatically analyzes grammar structures and fills structure templates with pattern formulation, usage examples, and learning aids. Quick systematic analysis without external data sources.

**"Fill structure template"** - Auto-populate grammar pattern cards with minimal effort.

## Aliases

```bash
/structure [pattern]
/struct [pattern]
/grammar [pattern]
```

## Usage

```bash
# Use current file name as the pattern
/structure

# Specify pattern explicitly
/structure "passive voice"

# Single file with relative path
/structure struct/passive-voice.md

# Batch mode with relative paths (auto-detected from multiple paths)
/structure struct/passive-voice.md struct/conditional-type-2.md struct/relative-clauses.md

# Batch process entire folder
/structure --batch

# With specific focus (future enhancement)
/structure struct/subjunctive.md --examples=10
```

## Arguments

- `$ARGUMENTS`: One or more paths to structure files (relative or absolute), or pattern name to analyze
  - Single argument: Process one file or pattern
  - Multiple arguments: Auto-trigger batch mode and process all files
  - No arguments: Use current filename
  - Relative paths are resolved from workspace root

## Flags

| Flag | Description | Example |
|------|-------------|---------| 
| `--batch` | Process all .md files with `process_status: pending` | `--batch` |
| `--examples=N` | Number of examples to generate (default: 4) | `--examples=8` |
| `--contexts=list` | Specific contexts (formal,informal,academic,business) | `--contexts=formal,academic` |
| `--cefr=level` | Force CEFR level (A1-C2) | `--cefr=B2` |
| `--template=path` | Custom template path | `--template=custom.md` |

---

## Core Methodology

**Reference**: `.claude/skills/structure-analysis/SKILL.md`
**Primary Agent**: Structure-Analyst (`.claude/agents/structure-analyst.md`)
**No Web Search Required**: Uses AI linguistic knowledge

### Systematic Pattern Analysis

```
Pattern Recognition
    ↓
Component Analysis
    ↓
Rule Formulation
    ↓
Example Generation (Multiple Contexts)
    ↓
Template Populated
    ✅ Complete
```

**Key Principle**: Systematic analysis from pattern to examples, filling template completely in one pass.

---

## Workflow

Analyzing structure for: **{{ if $ARGUMENTS }}$ARGUMENTS{{ else }}[current filename]{{ endif }}**

**Template**: {{ if --template provided }}`$TEMPLATE`{{ else }}`.claude/skills/vocabulary-research/99_Templates/tpl_Structure.md`{{ endif }}

**Target file**: `struct/[pattern-name].md`

**Duration**: 2-4 minutes (single pass, no web search)

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
    SOURCE = "structure_folder"
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

# Extract pattern from filename
pattern_name = basename(absolute_path).replace(".md", "")
```

#### 1.3 Pattern Extraction & Validation

{{ if MODE == "single" }}
{{ if SOURCE == "current_file" }}
- Extract from currently open file
- Remove .md extension
{{ else if SOURCE is path }}
- Extract from filename: `$SOURCE`
{{ else }}
- Use provided pattern: `$SOURCE`
{{ endif }}
{{ else }}
- Extract from each file in batch
{{ endif }}

**Process for each pattern**:
- Normalize pattern name (e.g., "passive-voice" → "Passive Voice")
- Identify pattern type (tense, mood, voice, clause, etc.)
- Validate pattern is recognizable

**Output**: 
{{ if MODE == "single" }}
- Normalized pattern: `[PATTERN]`
- Target file: `[ABSOLUTE_PATH]`
{{ else }}
- Pattern list: `[PATTERN1, PATTERN2, PATTERN3, ...]`
- File list: `[PATH1, PATH2, PATH3, ...]`
- Processing queue ready
{{ endif }}

---

### Step 2: Pattern Analysis

**Agent**: Structure-Analyst (`.claude/agents/structure-analyst.md`)
**Skill**: `.claude/skills/structure-analysis/SKILL.md`

**Goal**: Systematically analyze the grammar structure.

**Analysis Steps**:

1. **Pattern Recognition**:
   - Identify pattern type
   - Formulate structural formula
   - Extract components
   
2. **Rule Formulation**:
   - Document formation rules
   - Identify constraints
   - Map variations

3. **Contextual Mapping**:
   - Register preferences (formal/informal)
   - Domain usage
   - Frequency assessment
   - CEFR level determination

4. **Example Generation**:
   {{ if --examples }}
   - Generate $EXAMPLES contextual examples
   {{ else }}
   - Generate 4 examples (formal, informal, academic, business)
   {{ endif }}
   - Each with Vietnamese translation
   - Context appropriateness notes

5. **Error Patterns**:
   - Common mistakes by learners
   - Corrections with explanations
   - How to avoid errors

6. **Related Structures**:
   - Similar patterns: `[[pattern1]]`, `[[pattern2]]`
   - Contrasting patterns
   - Progressive learning path

---

### Step 3: Template Population

**Goal**: Fill all template sections with analyzed data in one complete pass.

**Template Sections Filled**:

- ✅ 🔄 **Process Status**: Update `process_status` from `pending` to `done`
- ✅ 📊 Meta Information (type, pattern, complexity, CEFR, frequency, register)
- ✅ 🔍 Structural Analysis (pattern formula, components, rules, variations)
- ✅ 💡 Meaning & Usage (core meaning, function, Vietnamese, nuances)
- ✅ 🔗 Relations (similar structures `[[]]`, contrasting structures, related concepts)
- ✅ 📝 Usage Examples (formal, informal, academic, business contexts)
- ✅ ⚠️ Common Mistakes (error patterns with corrections)
- ✅ 🎯 Learning Strategies (strategies, mastery criteria checklist)
- ✅ 🧩 Context Analysis (situation, purpose, audience, effectiveness)
- ✅ 📚 Advanced Analysis (stylistics, frequency, culture)
- ✅ 💭 Personal Notes (suggested mnemonics, examples)
- ✅ 🔖 Tags & Classification (tags, context, complexity, function)
- ✅ 📝 Quick Reference (formula, rules, dos/don'ts, signals)
- ✅ 🧠 Spaced Repetition Flashcards (7 cards types)

**Quality Checks**:
- Pattern formula is correct
- All components identified
- Examples are natural and varied
- Vietnamese translations accurate
- Related structures linked with `[[]]`
- No empty required sections

---

## Completion

**Template Filled**: `struct/[pattern-name].md`

**Verification Checklist**:
- [ ] Pattern formula accurate
- [ ] All components identified
- [ ] Formation rules documented
- [ ] Examples cover multiple contexts
- [ ] Vietnamese translations natural
- [ ] Common mistakes identified
- [ ] Related structures linked with `[[]]`
- [ ] Learning aids comprehensive

### Post-Fill Actions

1. **Review**: Quick scan of pattern analysis
2. **Practice**: Try the exercises
3. **Create Examples**: Generate own sentences
4. **Spaced Repetition**: Use flashcards

---

## Batch Processing

**Triggered when**:
- Multiple paths provided: `/structure struct/pattern1.md struct/pattern2.md`
- Explicit flag used: `/structure --batch`

### Mode 1: Explicit Paths (Recommended)

**User provides paths directly**:

```bash
/structure struct/passive-voice.md struct/conditional.md struct/relative-clauses.md
```

**Process**:
1. Normalize all paths to absolute
2. Validate each file exists
3. Extract pattern from each filename
4. Process sequentially with progress tracking

### Mode 2: Folder Discovery

**User triggers batch discovery**:

```bash
/structure --batch
```

**Process**:
1. **File Discovery**:
   ```bash
   # Search for markdown files, excluding .claude, node_modules, and hidden files
   find . -type f -name "*.md" -not -path '*/.*' -not -path '*/node_modules/*' -not -path '*/.claude/*' | grep "struct\|grammar"
   
   # Or specifically in the struct folder if it exists
   # find struct/ -name "*.md" -type f
   ```

2. **Filtering**:
   - Skip templates (files with `tpl_` prefix)
   - CHECK Content: Read file frontmatter
   - KEEP if `process_status: pending`
   - SKIP if `process_status: done` or field missing
   - Process remaining files

3. **Processing Queue**:
   - Sort files alphabetically
   - Process each file sequentially
   - Track success/failure for each

### Progress Tracking

For both modes, display progress:

```
📐 Grammar Structure Batch Processing
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Processing: [1/4] passive-voice.md
  ✓ Pattern analyzed
  ✓ Examples generated (4 contexts)
  ✓ Template populated
  ⏱️  Completed in 2.8s

Processing: [2/4] conditional-type-2.md
  ✓ Pattern analyzed
  ✓ Examples generated (4 contexts)
  ✓ Template populated
  ⏱️  Completed in 3.1s

Processing: [3/4] relative-clauses.md
  ✓ Pattern analyzed
  ✓ Examples generated (4 contexts)
  ✓ Template populated
  ⏱️  Completed in 2.9s

Processing: [4/4] subjunctive-mood.md
  ✓ Pattern analyzed
  ✓ Examples generated (4 contexts)
  ✓ Template populated
  ⏱️  Completed in 3.4s

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Summary: 4/4 completed successfully
Total time: 12.2s
Average: 3.0s per structure
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

**Error log saved to**: `.structure-batch-errors.log`

---

## Examples

```bash
# Quick fill for current structure file
/structure

# Fill specific file by path
/structure struct/passive-voice.md

# Batch mode - multiple files with relative paths
/structure struct/passive.md struct/conditional.md struct/relative-clauses.md

# Detailed analysis with more examples
/structure struct/subjunctive.md --examples=8

# Batch process entire folder (only pending files)
/structure --batch

# Batch with options (applies to all files)
/structure struct/pattern1.md struct/pattern2.md --examples=6
```

---

## Error Handling

**Common Issues & Solutions**:

| Issue | Solution |
|-------|----------|
| Pattern unclear | Simplify to basic components |
| Ambiguous usage | Provide context-specific examples |
| Complex variations | Document each separately |
| CEFR level uncertain | Estimate based on complexity |
| Regional differences | Note BE vs. AE if significant |

---

## Related Skills

- **structure-analysis**: Core methodology for pattern analysis
- **grammar-analysis**: Advanced grammatical structure analysis
- **contextual-examples**: Context-aware example generation

---

## Notes

- Systematic pattern-to-examples approach
- No web search required (uses AI knowledge)
- Complete template population in one pass
- Average completion time: 2-4 minutes per structure
- Suitable for batch processing grammar pattern libraries
- All related structures linked with `[[]]` for Obsidian navigation
