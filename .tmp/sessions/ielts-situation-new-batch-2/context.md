# Task Context: IELTS Situation Flashcard Processing - New Batch 2

Session ID: ielts-situation-new-batch-2
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
- Context: These relate to archaeology projects and show/programme descriptions

## Files to Process (Batch 2 - Archaeology & Show Descriptions)
- `/Users/trung.ngo/Documents/zaob-dev/glean-vault/glean/40_Situation/What do the team plan to do after work ends this summer? prepare a display for a museum, take part in a television programme or start to organise school visits.md` - multi-option (archaeology project planning)
- `/Users/trung.ngo/Documents/zaob-dev/glean-vault/glean/40_Situation/What led to archaeologists to believe there was an ancient village on this site? The lucky discovery of old records, bases of several structures visible in the grass or unusual stones found near the castle.md` - multi-option (archaeological evidence)
- `/Users/trung.ngo/Documents/zaob-dev/glean-vault/glean/40_Situation/What was found on the other side of the river to the castle? The remains of a large palace, the outline of fields or a number of small huts.md` - multi-option (site discoveries)
- `/Users/trung.ngo/Documents/zaob-dev/glean-vault/glean/40_Situation/Who was responsible for starting the community project? The castle owners, a national charity or the local council.md` - multi-option (project origin)
- `/Users/trung.ngo/Documents/zaob-dev/glean-vault/glean/40_Situation/This show's programme contains insights into the show.md` - single-option (show analysis)
- `/Users/trung.ngo/Documents/zaob-dev/glean-vault/glean/40_Situation/This show's programme is historically significant for a country.md` - single-option (show analysis)
- `/Users/trung.ngo/Documents/zaob-dev/glean-vault/glean/40_Situation/This show's programme is included in a recent project.md` - single-option (show analysis)
- `/Users/trung.ngo/Documents/zaob-dev/glean-vault/glean/40_Situation/This show's programme resembles an artwork.md` - single-option (show analysis)
- `/Users/trung.ngo/Documents/zaob-dev/glean-vault/glean/40_Situation/This show's programme was effective at attracting audiences.md` - single-option (show analysis)
- `/Users/trung.ngo/Documents/zaob-dev/glean-vault/glean/40_Situation/This show's programme's origin is somewhat controversial.md` - single-option (show analysis)

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
- [ ] Process file 1: What do the team plan to do... (multi-option - archaeology planning)
- [ ] Process file 2: What led to archaeologists to believe... (multi-option - archaeological evidence)
- [ ] Process file 3: What was found on the other side... (multi-option - site discoveries)
- [ ] Process file 4: Who was responsible for starting... (multi-option - project origin)
- [ ] Process file 5: This show's programme contains insights... (single-option)
- [ ] Process file 6: This show's programme is historically significant... (single-option)
- [ ] Process file 7: This show's programme is included in a project... (single-option)
- [ ] Process file 8: This show's programme resembles an artwork... (single-option)
- [ ] Process file 9: This show's programme was effective at attracting audiences... (single-option)
- [ ] Process file 10: This show's programme's origin is somewhat controversial... (single-option)

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
- #science-tech (for archaeology, discoveries, scientific research)
- #culture-media (for shows, programmes, cultural artifacts)
- #education-training (for academic projects, presentations)

Examples:
- Archaeology content → PILLAR: science-tech, subtopic: archaeology
- Show/programme analysis → PILLAR: culture-media, subtopic: show-programmes
- Museum displays → PILLAR: culture-media, subtopic: museum-exhibitions

QUALITY RULES:
- NO SUMMARIES - be detailed and specific
- Use `==` for highlighting, NOT `**`
- Callout format: `> [!info]` with NO empty lines inside
- Explain WHY things work, not just WHAT
- For Card 11 (MCQ): Analyze exact phrases and explain nuances
- For Card 18 (MCQ): Trace full cognitive path, don't just summarize
- Provide approximations for audio scripts, use [context-dependent] placeholders when unsure

IMPORTANT: These files are from IELTS Listening Section 3-4 context. The archaeology files relate to:
- Archaeological excavations and discoveries
- How evidence is interpreted
- Planning post-excavation activities (museum displays, TV programmes)
- Community involvement in projects

The show analysis files describe characteristics of theatre/programme descriptions:
- Content insights
- Historical significance
- Inclusion in projects
- Visual/artistic qualities
- Audience attraction
- Origins and controversies

Use appropriate academic context in your analysis. These are likely from discussions about archaeological findings or analysis of historical programmes/documents.
