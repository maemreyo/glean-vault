---
name: vocabulary-research
description: "Comprehensive vocabulary research and analysis. Gathers linguistic data from dictionaries (Oxford, Merriam-Webster, Cambridge), etymology (Etymonline), thesaurus (synonyms, antonyms), collocations (COCA, BNC), and frequency databases. Actions: research, analyze, fill, populate, generate vocabulary templates. Topics: word etymology, IPA pronunciation, CEFR levels, collocations, synonyms, antonyms, word families, Vietnamese translation, flashcards, spaced repetition. Elements: root analysis, usage examples, common mistakes, memory techniques."
---

# Vocabulary Research - Linguistic Intelligence

Automated vocabulary research system that gathers comprehensive linguistic data from multiple authoritative sources and populates vocabulary templates in single-pass methodology.

## Prerequisites

This skill requires web search capabilities to access online dictionaries and linguistic databases.

**Required Resources:**
- Dictionary APIs: Oxford, Merriam-Webster, Cambridge
- Etymology: Etymonline, Wiktionary
- Thesaurus: Thesaurus.com, Power Thesaurus
- Collocations: COCA, BNC, Just The Word
- Frequency: Google Books Ngram, COCA frequency lists

---

## How to Use This Skill

When user requests vocabulary analysis (`/vocab` command), follow this workflow:

### Step 1: Analyze Input

Extract key information from user request:
- **Word/File**: Single word or vocabulary file path(s)
- **Mode**: Single file or batch processing
- **Depth**: Basic, standard, or deep research
- **Options**: CEFR level, domain, examples count, etymology depth

### Step 2: Parallel Data Collection

Use **single-pass parallel gathering** - query ALL sources simultaneously:

```bash
# Dictionary APIs (definitions, IPA, CEFR)
Search: Oxford Dictionary + "[word]"
Search: Merriam-Webster + "[word]"
Search: Cambridge Dictionary + "[word]"

# Etymology (word origin and history)
Search: Etymonline + "[word]"
Search: Wiktionary etymology + "[word]"

# Thesaurus (synonyms and antonyms)
Search: Thesaurus.com + "[word]"
Search: Power Thesaurus + "[word]"

# Collocations (usage patterns)
Search: "[word] collocations" COCA
Search: "[word] common phrases" BNC

# Frequency data
Search: Google Ngram + "[word]"
Search: COCA frequency + "[word]"
```

### Step 3: Data Validation

Cross-validate information from multiple sources:
- **IPA**: Verify pronunciation from 2+ dictionaries
- **CEFR**: Confirm level using frequency + complexity
- **Etymology**: Use authoritative sources only
- **Examples**: Ensure natural, current usage
- **Collocations**: Verify frequency in corpus data

### Step 4: Template Population

Fill the appropriate template (see `99_Templates/` folder):
- **tpl_Vocabulary.md**: Full word entries with all linguistic data
- **tpl_Structure.md**: Grammar patterns and structures
- **tpl_Source_Input.md**: Content from external sources

---

## Research Domains

### Domain 1: Basic Information
**What to collect:**
- IPA transcription (verify with 2+ sources)
- Part(s) of speech
- All major definitions
- CEFR level (A1-C2)
- Register (formal/informal/neutral/technical)
- Frequency rating (common/moderate/rare)

### Domain 2: Etymology & Word Family
**What to collect:**
- Language(s) of origin
- Historical development
- Root analysis (prefix + root + suffix)
- Word family (noun, verb, adjective, adverb forms)
- Related derivatives

**Keywords for search:**
```
etymology, origin, root, Latin, Greek, Germanic, French, 
word family, derivatives, morphology
```

### Domain 3: Semantic Relations
**What to collect:**
- Synonyms (grouped by nuance differences)
- Antonyms (direct opposites)
- Nuances (how it differs from similar words)
- Register variations

**Keywords for search:**
```
synonym, antonym, similar words, difference between,
nuance, connotation
```

### Domain 4: Usage & Collocations
**What to collect:**
- Common collocations (verb+noun, adj+noun, adv+verb, prepositions)
- Usage examples in different contexts
- Idiomatic phrases
- Domain-specific usage

**Keywords for search:**
```
[word] collocations, common phrases, usage examples,
COCA corpus, BNC corpus, frequency
```

### Domain 5: Learning Aids
**What to collect:**
- Common mistakes by learners
- Memory techniques and mnemonics
- Practice suggestions
- Flashcard content for spaced repetition

**Keywords for search:**
```
common mistakes, errors, mnemonics, memory techniques,
how to remember
```

---

## Templates Reference

### tpl_Vocabulary.md (Main Template)

Comprehensive vocabulary entry with:
- 📊 Meta Information (IPA, CEFR, register, frequency, etymology)
- 🌳 Root Word Analysis (root components, word family, related words)
- 💡 Definitions (root meaning, context meaning, Vietnamese, nuances)
- 🔗 Relations (synonyms, antonyms)
- 📝 Usage (collocations, examples, common mistakes)
- 🎯 Learning Tips (memory techniques, practice exercises)
- 🧩 Context (original source quotes)
- 🧠 Spaced Repetition Flashcards (5 cards: recognition, production, usage, collocation, root)
- 📈 Learning Progress tracking

### tpl_Structure.md

Grammar structures and patterns with:
- 📐 Structure Pattern (syntax formula)
- 🧩 Context Example (real usage)
- 🎯 More Examples (correct/incorrect)
- 🧠 Flashcards
- 🔗 Related Structures

---

## Quality Assurance Checklist

Before completing vocabulary research, verify:

### Data Quality
- [ ] IPA verified from multiple dictionaries
- [ ] All definitions clear and accurate
- [ ] Etymology from authoritative sources
- [ ] Examples show natural, varied usage
- [ ] Vietnamese translations are appropriate and natural

### Completeness
- [ ] All required fields populated
- [ ] No placeholder text `[[]]` remaining (except for personal notes)
- [ ] Word family shows all major forms
- [ ] At least 3 usage examples provided
- [ ] At least 8 collocations included

### Cross-Validation
- [ ] No contradictions between sources
- [ ] CEFR level matches frequency data
- [ ] Collocations verified in corpus
- [ ] Synonyms accurately reflect nuance differences

---

## Common Rules for Vocabulary Research

### Data Collection Rules

| Rule | Do | Don't |
|------|----|----- |
| **Multi-source verification** | Cross-check IPA from 2+ dictionaries | Trust single source |
| **Current usage** | Use examples from recent sources (2020+) | Use outdated or archaic examples |
| **Natural Vietnamese** | Translate contextually, not word-for-word | Use literal translations |
| **Corpus-verified collocations** | Check COCA/BNC frequency | List rare or invented combinations |

### Template Population Rules

| Rule | Do | Don't |
|------|----|----- |
| **Single-pass completion** | Fill all sections in one go | Leave sections incomplete |
| **Preserve structure** | Keep all template sections and formatting | Remove or reorganize sections |
| **Obsidian Links** | Format related words, synonyms, antonyms, and word family members as `[[word]]` | Use plain text `word` or bold `**word**` only |
| **Clear examples** | Use complete, context-rich sentences | Use fragments or unclear examples |
| **Spaced repetition cards** | Create testable, clear flashcards | Write vague or multi-part questions |

---

## Example Workflow

**User request:** `/vocab vocab/serendipity.md vocab/ephemeral.md --etymology=deep --examples=5`

**AI should:**

```bash
# For each word (serendipity, ephemeral):

# 1. Dictionary research
Search: "serendipity Oxford Dictionary IPA CEFR"
Search: "serendipity Merriam-Webster pronunciation definition"
Search: "serendipity Cambridge Dictionary"

# 2. Etymology (deep flag set)
Search: "serendipity etymology Etymonline"
Search: "serendipity word origin history"
Search: "serendipity root Latin Greek"

# 3. Thesaurus
Search: "serendipity synonyms"
Search: "serendipity antonyms"
Search: "serendipity vs coincidence difference"

# 4. Collocations
Search: "serendipity collocations COCA"
Search: "serendipity common phrases"

# 5. Frequency
Search: "serendipity Google Ngram"
Search: "serendipity CEFR level"

# 6. Usage examples (5 examples requested)
Search: "serendipity usage examples contemporary"
Search: "serendipity in sentences"
```

**Then:** Synthesize all results and populate `tpl_Vocabulary.md` template completely.

---

## Tips for Better Results

1. **Search comprehensively** - Query all domains before filling template
2. **Verify IPA carefully** - Pronunciation errors are common
3. **Group synonyms by nuance** - Don't just list similar words
4. **Use corpus data** - COCA/BNC for authentic collocations
5. **Natural examples** - Prefer sentences from real sources
6. **Context matters** - Show different meanings with different examples
7. **Vietnamese precision** - Match register and formality level

---

## Batch Processing Notes

When processing multiple files:
1. Extract word from each filename
2. Process sequentially with progress tracking
3. Log errors but continue processing
4. Report summary: completed/failed/total time

**Error handling:** Skip invalid words but complete valid ones.

---

## Integration with Commands

This skill is used by:
- `/vocab` command - Main vocabulary template filling
- Vocab-Analyst agent - Specialized vocabulary research

**Default templates location:** `.claude/skills/vocabulary-research/99_Templates/`

---

## Performance Metrics

Target quality standards:
- **Research Time**: 3-5 minutes per word (single pass)
- **Completeness**: 100% of required fields filled
- **Accuracy**: Cross-validation passed for all data points
- **Source Quality**: All sources authoritative
- **Example Quality**: Natural, contemporary usage

---

## Related Skills

- **contextual-examples**: Generate natural usage examples
- **etymology-analysis**: Deep word origin research
- **linguistic-analysis**: Advanced language structure analysis
