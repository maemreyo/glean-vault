# Task Context: IELTS Situation Flashcard Processing - Batch 2

Session ID: ielts-situation-batch-2
Created: 2025-12-25
Status: in_progress

## Current Request
Process 7 IELTS situation flashcard files with `status: pending` and fill them with complete content including analysis sections and flashcards.

## Requirements
- Read the situation guide: `/Users/trung.ngo/Documents/zaob-dev/glean-vault/docs/guide/situation.md`
- Process each file according to the guide
- NO WEB SEARCH - use internal knowledge only
- Update status: pending → done
- Follow all formatting rules (callouts, highlighting with ==, etc.)
- Delete MASTER TAGGING SYSTEM comment block
- Add proper tags to each card

## Decisions Made
- Batch size: 7 files for parallel processing
- Question type auto-detection from filename:
  - Contains "?" → multi-option (18 cards)
  - No "?" → single-option (14 cards, delete cards 10, 11, 12, 18)
- Tag formula: `#flashcards/ielts-listening/<PILLAR>/<subtopic>/<tier>/<drill-type>`
- Use Cam 20 Listening Test 02 as source test reference

## Files to Process (Batch 2)
- `/Users/trung.ngo/Documents/zaob-dev/glean-vault/glean/40_Situation/The students agree that developing disused industrial sites may? have unexpected costs, damage the urban environment or destroy valuable historical buildings.md` - multi-option
- `/Users/trung.ngo/Documents/zaob-dev/glean-vault/glean/40_Situation/The students will mention Masdar City as an example of an attemp to achieve? daily collections for waste recycling, sustainable energy use or free transport for everyone.md` - multi-option
- `/Users/trung.ngo/Documents/zaob-dev/glean-vault/glean/40_Situation/This human geography aspect may not be relevant to their course.md` - single-option
- `/Users/trung.ngo/Documents/zaob-dev/glean-vault/glean/40_Situation/This human geography aspect will involve only a small number of statistics.md` - single-option
- `/Users/trung.ngo/Documents/zaob-dev/glean-vault/glean/40_Situation/What is the next annual event for volunteers? A boat trip, a barbecue or a party.md` - multi-option
- `/Users/trung.ngo/Documents/zaob-dev/glean-vault/glean/40_Situation/What recent additions to the outskirts of their cities are both students happy about? conference centres, sport centres or retail centres.md` - multi-option
- `/Users/trung.ngo/Documents/zaob-dev/glean-vault/glean/40_Situation/When discussing the ecotown of Greenhill Abbots, Colin is uncertain about? what its objectives were, why there was opposition to it or how much of it has actually been built.md` - multi-option

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
- [ ] Process file 1: The students agree that developing disused... (multi-option)
- [ ] Process file 2: The students will mention Masdar City... (multi-option)
- [ ] Process file 3: This human geography aspect may not be relevant...
- [ ] Process file 4: This human geography aspect will involve only...
- [ ] Process file 5: What is the next annual event... (multi-option)
- [ ] Process file 6: What recent additions to the outskirts... (multi-option)
- [ ] Process file 7: When discussing the ecotown... (multi-option)

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

SELECT PILLAR from MASTER TAGGING SYSTEM (already in each file):
- #survival-essentials
- #health-food
- #work-career
- #education-training
- #social-leisure
- #science-tech
- #culture-media
- #business-legal

Example: For human geography content → PILLAR: education-training, subtopic: academic-research
For event/festival content → PILLAR: social-leisure, subtopic: events

QUALITY RULES:
- NO SUMMARIES - be detailed and specific
- Use `==` for highlighting, NOT `**`
- Callout format: `> [!info]` with NO empty lines inside
- Explain WHY things work, not just WHAT
- For Card 11 (MCQ): Analyze exact phrases and explain nuances
- For Card 18 (MCQ): Trace full cognitive path, don't just summarize
- Provide approximations for audio scripts, use [context-dependent] placeholders when unsure

IMPORTANT: These files are from IELTS Listening Section 1-2 context. The human geography files relate to academic discussions about research topics. The volunteer/event files relate to festival volunteering. Use appropriate context in your analysis.
