# Task Context: IELTS Situation Flashcards Batch Processing

Session ID: situation-batch-20241224
Created: 2024-12-24
Status: in_progress

## Current Request
Process 7 pending IELTS situation files in `glean/40_Situation/` directory:
- Fill all analysis sections (Question Profile, Options Analysis, Deep Analysis, etc.)
- Generate flashcards (11 for single-option, 15 for multi-option)
- Update status: pending → done
- Apply proper tags (remove MASTER TAGGING SYSTEM comment block)

## Requirements

### Core Requirements
1. Detect question type from filename:
   - **Single-option:** `the role of X is [option].md` → 11 cards
   - **Multi-option (MCQ):** `[question]? [opt1], [opt2] or [opt3].md` → 15 cards

2. Fill ALL sections:
   - YAML frontmatter: `question_type`, `options_count`, `status: done`
   - Question Profile: Question Type, Question Stem, Context, Source Test
   - Options Analysis: Table with all options (include "Correct Answer" for MCQ only)
   - Deep Analysis (5D Framework): Type of Info, Topic Category
   - Imagination & Sensory: Visual, Auditory, Action, Collocations
   - Real Audio Phrases: 4+ realistic IELTS phrases
   - Traps & Distractors: 2 traps with explanations
   - Example Scripts: 2 IELTS-level audio scripts
   - Flashcards: 11 (single) or 15 (multi)

3. **CRITICAL:** Tags cleanup
   - Select PILLAR & subtopic from MASTER TAGGING SYSTEM comment
   - Use formula: `#flashcards/ielts-listening/<PILLAR>/<subtopic>/<tier>/<drill-type>`
   - **EACH CARD** must have SPECIFIC tag suffix (see table below)
   - **DELETE** entire `<!-- MASTER TAGGING SYSTEM ... -->` comment block
   - Tags must appear ONLY directly above their respective card headers

4. **CRITICAL:** Fill aliases with variations (YAML list format, remove trailing comment)

5. **CRITICAL:** Single-option files SKIP Cards 8, 9, 10, 15 (MCQ-specific)

### Files to Process
1. `/Users/trung.ngo/Documents/zaob-dev/glean-vault/glean/40_Situation/New volunteers will start working in the week beginning? 2 Sep, 9 Sep, or 23 Sep.md` (multi)
2. `/Users/trung.ngo/Documents/zaob-dev/glean-vault/glean/40_Situation/What is the most important requirement for volunteers at the festivals? interpersonal skills, personal interest in the event or flexibility.md` (multi)
3. `/Users/trung.ngo/Documents/zaob-dev/glean-vault/glean/40_Situation/What is the next annual event for volunteers? A boat trip, a barbecue or a party.md` (multi)
4. `/Users/trung.ngo/Documents/zaob-dev/glean-vault/glean/40_Situation/Which event requires the largest number of volunteers? The music festival, the science festival, the book festival.md` (multi)
5. `/Users/trung.ngo/Documents/zaob-dev/glean-vault/glean/40_Situation/the role of the volunteers is collecting feedback on events.md` (single)
6. `/Users/trung.ngo/Documents/zaob-dev/glean-vault/glean/40_Situation/the role of the volunteers is contacting local businesses.md` (single)
7. `/Users/trung.ngo/Documents/zaob-dev/glean-vault/glean/40_Situation/the role of the volunteers is encouraging cooperation between local organisations.md` (single)

## Static Context Available
- Template: `/Users/trung.ngo/Documents/zaob-dev/glean-vault/glean/99_Templates/tpl_Situation.md`
- Guide: `/Users/trung.ngo/Documents/zaob-dev/glean-vault/docs/guide/situation.md`

## Constraints/Notes

### ⛔ CRITICAL: NO WEB SEARCH
**DISABLED TOOLS:** `web_search`, `web_fetch` - NEVER use under ANY circumstances.
**WHY:** Situation analysis must be consistent. Use internal knowledge only as an IELTS instructor.
**IF UNSURE:**
- Use best linguistic judgment
- Provide approximations for audio scripts
- Use placeholder: `[context-dependent]`
- NEVER attempt to search

### Format Rules
- **Callout Format:** Keep `> [!info]`, `> [!success]`, `> [!fail]`, etc. exactly as is.
- **CRITICAL: NO EMPTY LINES INSIDE CALLOUTS OR BETWEEN BLOCKS.**
  - If visual break needed within block, use line with only `>`
  - Use `>` line between logical items in lists
  - Ensure EVERY line in flashcard block starts with `>` or has NO empty lines between header and `?`
- **Separator:** Mandatory `?` separator between Q&A.
- **Highlighting:** Use `==` pair to highlight important words/phrases (MANDATORY!). Do NOT use `**` for emphasis within content.
- **Language:** Analysis in Vietnamese/English mix as per template.
- **Placeholders:** Replace ALL `{{PLACEHOLDER}}` with actual content.

### Quality & Detail Rules (MANDATORY)
- **Highlighting:** Consistently use `==` to highlight key terms.
- **Deep Analysis:** Avoid superficial 1-2 word answers. Provide *detailed, specific* explanations.
- **5D Framework:** "Definition" and "Denotation" must be full sentences explaining context, not just synonyms.
- **Imagination:** "Sensory Triggers" must describe *meaningful* scenes, sounds, and actions.
- **Flashcards:** Explanations in "Logic Chain" and "Why" sections must be comprehensive.
- **Real Audio Phrases:** Must sound authentic to IELTS Listening (use contractions, natural fillers like "actually", "well", "you see").

### Tag Suffix Per Card (MANDATORY)
| Card | Tier | Tag suffix | MCQ Only? |
|------|------|------------|-----------|
| 1 | daily | `daily/01-prediction` | No |
| 2 | daily | `daily/02-keywords` | No |
| 3 | daily | `daily/03-signpost` | No |
| 4 | recognition | `recognition/01-reverse` | No |
| 5 | recognition | `recognition/02-trap` | No |
| 6 | recognition | `recognition/03-differentiate` | No |
| 7 | recognition | `recognition/04-cloze` | No |
| 8 | weekly | `weekly/01-elimination` | **Yes** |
| 9 | weekly | `weekly/02-cross-confusion` | **Yes** |
| 10 | weekly | `weekly/03-validation` | **Yes** |
| 11 | weekly | `weekly/04-chain` | No |
| 12 | biweekly | `biweekly/01-full-trap` | No |
| 13 | biweekly | `biweekly/02-script-match` | No |
| 14 | biweekly | `biweekly/03-speed` | No |
| 15 | biweekly | `biweekly/04-synthesis` | **Yes** |

### MASTER TAGGING SYSTEM (for tag selection)
```
1. #survival-essentials
   housing | accommodation | travel | transport | banking | shopping
   insurance | utilities | postal | repairs | maintenance

2. #health-food
   medical | hospital | pharmacy | dentist | fitness | gym
   nutrition | diet | restaurant | cafe | cooking | recipes

3. #work-career
   job-search | recruitment | interview | cv-resume | workplace | office
   salary | benefits | promotion | freelance | entrepreneurship

4. #education-training
   university | courses | enrollment | assignments | projects | exams
   library | research | tutoring | feedback | scholarships | graduation

5. #social-leisure
   events | festivals | parties | sports | fitness-activities | hobbies
   clubs | entertainment | cinema | concerts | relationships | volunteering

6. #science-tech
   biology | chemistry | physics | astronomy | IT | computers
   innovation | AI | robotics | environment | ecology | sustainability

7. #culture-media
   history | archaeology | arts | museums | literature | books
   tourism | attractions | journalism | news | film | music | theatre

8. #business-legal
   commerce | trade | marketing | advertising | finance | investment
   contracts | law | regulations | negotiations | customer-service
```

**For this batch:** All files are about **volunteering at festivals/events** → Use **PILLAR: social-leisure, subtopic: volunteering**

## Progress
- [ ] Read template file
- [ ] Process all 7 files (concurrently)
- [ ] Validate output (card counts, no placeholders, no web traces)
- [ ] Report summary

---

## Instructions for Subagent

### Task: Process 7 IELTS situation flashcard files CONCURRENTLY

#### Step 1: Read the Template
First, read the template file to understand the structure:
```
/Users/trung.ngo/Documents/zaob-dev/glean-vault/glean/99_Templates/tpl_Situation.md
```

#### Step 2: For EACH file, follow this process:

**DETECT QUESTION TYPE FROM FILENAME:**
- If filename contains "?" → `question_type: multi` → 15 cards
- Otherwise → `question_type: single` → 11 cards (SKIP Cards 8, 9, 10, 15)

**PARSE FILENAME:**
- **Single-option:** Extract option text after "is "
  - Example: `the role of the volunteers is collecting feedback on events.md`
    - Question Stem: "the role of the volunteers is"
    - Option: "collecting feedback on events"
- **Multi-option:** Extract question stem (before "?") and options (split by ", " and " or ")
  - Example: `What is the most important requirement...? interpersonal skills, personal interest in the event or flexibility.md`
    - Question Stem: "What is the most important requirement...?"
    - Options: ["interpersonal skills", "personal interest in the event", "flexibility"]

**UPDATE YAML FRONTMATTER:**
```yaml
question_type: single  # or multi
options_count: 1      # 1, 2, 3, or 4
status: done          # Update from pending
```

**POPULATE ALIASES:**
- Fill `aliases:` with variations using YAML list format (bullet points)
- DELETE the trailing comment `# common variations...`

**FILL ANALYSIS SECTIONS:**

1. **Question Profile:**
   - Question Type: single/multi
   - Question Stem: extracted from filename
   - Context: infer from topic (volunteering, festivals, events)
   - Source Test: from `ref:` field if available

2. **Options Analysis Table:**
   - For **single-option**: 1 row only, NO "Correct Answer" line
   - For **multi-option**: 2-4 rows, include "Correct Answer" line
   - Each row: Option, Core Meaning (Vietnamese), Paraphrase Keywords, Trap Potential

3. **Deep Analysis (5D Framework):**
   - Type of Info: Hành động/Địa điểm/Người chịu trách nhiệm/Cảm xúc/Thời gian
   - Topic Category: Volunteering/Events/Festivals (use ==highlight==)
   - Definition, Denotation, Distractor, Deep Dive with detailed explanations

4. **Imagination & Sensory:**
   - Visual, Auditory, Action triggers (meaningful descriptions)
   - Collocation Patterns: Verb+Noun, Noun+of+Noun, Adj+Noun

5. **Real Audio Phrases:**
   - 4+ realistic IELTS phrases with contractions, natural fillers

6. **Traps & Distractors:**
   - 2 traps with "Why it's tricky" and "Actual meaning" explanations

7. **Example Scripts:**
   - 2 IELTS-level audio scripts showing paraphrasing

**GENERATE FLASHCARDS:**

- Use ==highlight== for important words/phrases
- Keep callout format (> [!info], etc.)
- NO empty lines inside callouts
- Mandatory `?` separator between Q&A
- **CRITICAL:** EACH card must have its specific tag above the header

**TAG CLEANUP (CRITICAL):**
1. DELETE the entire `<!-- MASTER TAGGING SYSTEM ... -->` comment block
2. Add proper tags before EACH card header using formula:
   `#flashcards/ielts-listening/<PILLAR>/<subtopic>/<tier>/<drill-type>`
3. For this batch, use: `#flashcards/ielts-listening/social-leisure/volunteering/<tier>/<drill-type>`
4. Replace `<tier>/<drill-type>` with specific suffix from table above
5. Tags appear ONLY directly above their respective card headers

**SINGLE-OPTION FILES ONLY:**
- SKIP Cards 8, 9, 10, 15 (MCQ-specific)
- Total: 11 cards
- Renumber remaining cards sequentially

**WRITE CONTENT BACK TO FILE:**
- Replace ALL {{PLACEHOLDER}} with actual content
- Update status: pending → done
- Ensure no empty lines inside callouts

#### Step 3: Validation
After processing all files:
- Verify card counts (11 for single, 15 for multi)
- Check no placeholders remaining (grep for `{{`)
- Ensure no web search traces
- Verify MASTER TAGGING comment block removed

#### Step 4: Return Summary Report
```
✅ Processed X/Y files successfully
📦 Files processed: 7
📊 Single-option files: 3 (11 cards each)
📊 Multi-option files: 4 (15 cards each)
📊 Total cards generated: 93
❌ Failed files: [list if any]
```

**Remember: Use INTERNAL KNOWLEDGE ONLY. NO WEB SEARCH under ANY circumstances.**
