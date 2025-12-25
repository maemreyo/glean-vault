# Task Context: IELTS Situation Flashcard Processing - New Batch 1

Session ID: ielts-situation-new-batch-1
Created: 2025-12-25
Status: in_progress

## Current Request
Process 8 IELTS situation flashcard files with `status: pending` and fill them with complete content including analysis sections and flashcards.

## Requirements
- Read the situation guide: `/Users/trung.ngo/Documents/zaob-dev/glean-vault/docs/guide/situation.md`
- Process each file according to the guide
- NO WEB SEARCH - use internal knowledge only
- Update status: pending → done
- Follow all formatting rules (callouts, highlighting with ==, etc.)
- Delete MASTER TAGGING SYSTEM comment block
- Add proper tags to each card

## Decisions Made
- Batch size: 8 files for parallel processing
- Question type auto-detection from filename:
  - Contains "?" → multi-option (18 cards)
  - No "?" → single-option (14 cards, delete cards 10, 11, 12, 18)
- Tag formula: `#flashcards/ielts-listening/<PILLAR>/<subtopic>/<tier>/<drill-type>`
- Context: These relate to theatre programmes history and archaeology

## Files to Process (Batch 1 - Theatre & Multi-option)
- `/Users/trung.ngo/Documents/zaob-dev/glean-vault/glean/40_Situation/Finn and Maya both think that, compared to 19nd-century programmes, those from the 18nd century? were more original, were more colourful or were more informative.md` - multi-option (theatre history)
- `/Users/trung.ngo/Documents/zaob-dev/glean-vault/glean/40_Situation/Finn was pleased to discover that their topic? was not familiar to their module leader, had not been chosen by other students or did not prove to be difficult to research.md` - multi-option (academic project)
- `/Users/trung.ngo/Documents/zaob-dev/glean-vault/glean/40_Situation/Finn was surprised that, in early British theatre, programmes? were difficult for audiences to obtain, were given out free of charge or were seen as a kind of contract.md` - multi-option (theatre distribution)
- `/Users/trung.ngo/Documents/zaob-dev/glean-vault/glean/40_Situation/How was the gold coin found? Heavy rain had removed some of the soil, the ground was dug up by wild rabbits or a person with a metal detector searched the area.md` - multi-option (archaeology discovery)
- `/Users/trung.ngo/Documents/zaob-dev/glean-vault/glean/40_Situation/Maya doesn't fully understand why, in the 20th century, very few theatre programmes were printed in the USA; British theatre programmes failed to develop for so long or theatre programmes in Britain copied fashions from the USA.md` - multi-option (theatre development)
- `/Users/trung.ngo/Documents/zaob-dev/glean-vault/glean/40_Situation/Maya feels their project should include an explanation of why companies of actors? promoted their own plays, performed plays outdoors or had to tour with their plays.md` - multi-option (theatre companies)
- `/Users/trung.ngo/Documents/zaob-dev/glean-vault/glean/40_Situation/Maya says a mistaken belief about theatre programmes is that? theatres pay companies to produce them, few theatre-goers buy them nowadays or they contain far more adverts than previously.md` - multi-option (theatre programmes misconceptions)
- `/Users/trung.ngo/Documents/zaob-dev/glean-vault/glean/40_Situation/What are the team still hoping to find? everyday pottery, animal bones or pieces of jewellery.md` - multi-option (archaeology finds)

## Static Context Available
- `/Users/trung.ngo/Documents/zaob-dev/glean-vault/docs/guide/situation.md` - Full processing guide
- `/Users/trung.ngo/Documents/zaob-dev/glean-vault/glean/99_Templates/tpl_Situation.md` - Flashcard template

## Constraints/Notes
- CRITICAL: NO EMPTY LINES INSIDE CALLOUTS
- Use `==` for highlighting, NOT `**` bold
- Maintain callout format: `> [!info]`, `> [!success]`, `> [!fail]`, etc.
- Each card must have UNIQUE tag suffix (see guide table)
- Delete MASTER TAGGING SYSTEM comment block entirely
- For single-option files: Delete cards 10, 11, 12, 18 (keep 14 cards total)
- For multi-option files: Keep all 18 cards
- Fill ALL placeholders: {{PLACEHOLDER}} → actual content
- Use Vietnamese/English mix in analysis sections as per template

## Progress
- [ ] Read and understand situation guide
- [ ] Process file 1: Finn and Maya both think that... (multi-option - theatre history)
- [ ] Process file 2: Finn was pleased to discover... (multi-option - academic project)
- [ ] Process file 3: Finn was surprised that... (multi-option - theatre distribution)
- [ ] Process file 4: How was the gold coin found? (multi-option - archaeology)
- [ ] Process file 5: Maya doesn't fully understand why... (multi-option - theatre development)
- [ ] Process file 6: Maya feels their project... (multi-option - theatre companies)
- [ ] Process file 7: Maya says a mistaken belief... (multi-option - theatre misconceptions)
- [ ] Process file 8: What are the team still hoping to find? (multi-option - archaeology)

---

**Instructions for Subagent:**

Read the situation guide at `/Users/trung.ngo/Documents/zaob-dev/glean-vault/docs/guide/situation.md` first. This contains complete instructions for processing these files.

For each file:
1. Detect question type from filename (contains "?" = multi, otherwise single)
2. Read the existing file content
3. Fill ALL analysis sections:
   - Question Profile (Type, Stem, Context, Source)
   - Options Analysis (table with Core Meaning, Paraphrase Keywords, Trap Potential)
   - Deep Analysis (5D Framework: Definition, Denotation, Distractor, Deep Dive)
   - Imagination & Sensory (Visual, Auditory, Action, Collocation Patterns)
   - Real Audio Phrases (4+ authentic IELTS phrases)
   - Traps & Distractors (2 traps with explanations)
   - Example Scripts (2 IELTS-level audio scripts)
4. Generate flashcards:
   - Single-option: 14 cards (delete cards 10, 11, 12, 18)
   - Multi-option: 18 cards (keep all)
5. Add proper tags to each card using formula: `#flashcards/ielts-listening/<PILLAR>/<subtopic>/<tier>/<drill-type>`
6. Remove the MASTER TAGGING SYSTEM comment block entirely
7. Update YAML frontmatter: question_type, options_count, status: done
8. Populate aliases with variations (YAML list format)
9. Write updated content back to file

TAG SUFFIX GUIDE (critical - must match guide):
- Card 1: `daily/01-prediction` (All)
- Card 2: `daily/02-keywords` (All)
- Card 3: `daily/03-signpost` (All)
- Card 4: `daily/04-sound` (All)
- Card 5: `recognition/01-reverse` (All)
- Card 6: `recognition/02-trap` (All)
- Card 7: `recognition/03-differentiate` (All)
- Card 8: `recognition/04-cloze` (All)
- Card 9: `recognition/05-spatial` (All - placeholder if no map)
- Card 10: `weekly/01-elimination` (MCQ Only)
- Card 11: `weekly/02-cross-confusion` (MCQ Only)
- Card 12: `weekly/03-validation` (MCQ Only)
- Card 13: `weekly/04-agreement` (All)
- Card 14: `weekly/05-swap` (All)
- Card 15: `biweekly/01-full-trap` (All)
- Card 16: `biweekly/02-script-match` (All)
- Card 17: `biweekly/03-speed` (All)
- Card 18: `biweekly/04-synthesis` (MCQ Only)

SELECT PILLAR from MASTER TAGGING SYSTEM:
- #culture-media (for theatre programmes, history)
- #education-training (for academic projects, research)
- #science-tech (for archaeology, discoveries)

Examples:
- Theatre content → PILLAR: culture-media, subtopic: theatre-history
- Archaeology content → PILLAR: science-tech, subtopic: archaeology
- Academic project → PILLAR: education-training, subtopic: academic-research

QUALITY RULES:
- NO SUMMARIES - be detailed and specific
- Use `==` for highlighting, NOT `**`
- Callout format: `> [!info]` with NO empty lines inside
- Explain WHY things work, not just WHAT
- For Card 11 (MCQ): Analyze exact phrases and explain nuances
- For Card 18 (MCQ): Trace full cognitive path, don't just summarize
- Provide approximations for audio scripts, use [context-dependent] placeholders when unsure

IMPORTANT: These files are from IELTS Listening Section 3 context. The theatre files relate to:
- Historical theatre programmes (18th vs 19th century)
- Theatre distribution and access
- Theatre companies and their practices
- Misconceptions about theatre programmes

The archaeology files relate to:
- Site discoveries (gold coin, pottery, animal bones, jewellery)
- How artifacts are found (weather, animals, metal detector)
- Archaeological methods

Use appropriate academic context in your analysis. These are likely from students discussing theatre history or participating in archaeological excavations.
