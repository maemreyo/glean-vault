# Deck Management System

This document outlines the **Space Repetition Deck System** for the Glean Vault. It is designed based on the capabilities of the [Obsidian Spaced Repetition Plugin](https://www.stephenmwangi.com/obsidian-spaced-repetition/flashcards/decks/).

## 1. Core Philosophy: Tag-Based Hierarchy

We utilize a **Tag-based Strategy** rather than a Folder-based strategy. This allows files to remain organized by their content type (e.g., all vocabulary in `20_Vocabulary`) while dynamically belonging to different flashcard decks based on their properties (Topic, Difficulty, Source).

### Why Tags?
- **Flexibility**: A single note can belong to multiple decks (e.g., a word relevant to both "Business" and "Writing").
- **Portability**: You don't need to move files around if you change your deck structure.
- **Granularity**: You can have a general `#flashcard` tag for the file, and specific tags for individual questions if needed.

---

## 2. Deck Hierarchy Structure

To keep the system organized, we define a clear hierarchy using **nested tags**. The plugin parses `/` as a sub-deck separator.

### Root Tag & Strict Rules
All flashcards must include the root tag (defined in plugin settings, default `#flashcards`).

> [!important] Strict Tagging Rule
> 1. **File-Level Tag:** Every flashcard file MUST start with a deck tag at the very top of the file (before frontmatter, or as the first line).
>    - Format: `#flashcards/<type>/<topic>`
>    - Example: `#flashcards/vocabulary/technology`
>
> **Note on Frontmatter:** Placing content before `---` YAML frontmatter may theoretically affect how some plugins read metadata, but for the Spaced Repetition plugin, it ensures the file is recognized. If you use properties heavily, ensure your Obsidian configuration supports this, or place the tag *after* the frontmatter if issues arise. (User preference: Top of file).

### Recommendations Deck Tree

Based on a comprehensive analysis of your current vocabulary, here is the full recommended deck structure:

```text
# Vocabulary
#flashcards/vocabulary/general/functional-words
#flashcards/vocabulary/general/abstract-concepts
#flashcards/vocabulary/general/emotions-personality-adjectives

#flashcards/vocabulary/topic-specific/environment/climate-change-global-warming
#flashcards/vocabulary/topic-specific/environment/pollution-waste-management
#flashcards/vocabulary/topic-specific/environment/wildlife-conservation

#flashcards/vocabulary/topic-specific/sci-tech/technology
#flashcards/vocabulary/topic-specific/sci-tech/space-exploration
#flashcards/vocabulary/topic-specific/sci-tech/scientific-research

#flashcards/vocabulary/topic-specific/history-archaeology/archaeology
#flashcards/vocabulary/topic-specific/history-archaeology/ancient-civilizations
#flashcards/vocabulary/topic-specific/history-archaeology/evolution-anthropology

#flashcards/vocabulary/topic-specific/psychology-behavior/cognitive-science
#flashcards/vocabulary/topic-specific/psychology-behavior/child-development
#flashcards/vocabulary/topic-specific/psychology-behavior/social-psychology

#flashcards/vocabulary/topic-specific/agriculture-food/modern-farming
#flashcards/vocabulary/topic-specific/agriculture-food/food-science
#flashcards/vocabulary/topic-specific/agriculture-food/history-of-spices

#flashcards/vocabulary/topic-specific/society-urbanization/urban-life-city-planning
#flashcards/vocabulary/topic-specific/society-urbanization/family-gender-relationships
#flashcards/vocabulary/topic-specific/society-urbanization/globalization-integration

#flashcards/vocabulary/topic-specific/education/university-academic-life
#flashcards/vocabulary/topic-specific/education/online-learning-vs-traditional
#flashcards/vocabulary/topic-specific/education/child-discipline-parenting

#flashcards/vocabulary/topic-specific/work-economy/advertising-marketing-consumerism
#flashcards/vocabulary/topic-specific/work-economy/employment-management-styles
#flashcards/vocabulary/topic-specific/work-economy/business-models

#flashcards/vocabulary/topic-specific/health/physical-health-diet
#flashcards/vocabulary/topic-specific/health/mental-health-stress
#flashcards/vocabulary/topic-specific/health/healthcare-systems

#flashcards/vocabulary/topic-specific/arts-architecture/art-forms
#flashcards/vocabulary/topic-specific/arts-architecture/architecture
#flashcards/vocabulary/topic-specific/arts-architecture/media-literature-film

#flashcards/vocabulary/topic-specific/language-linguistics/language-acquisition
#flashcards/vocabulary/topic-specific/language-linguistics/origins-of-language
#flashcards/vocabulary/topic-specific/language-linguistics/communication-types

#flashcards/vocabulary/topic-specific/law-crime-politics/crime-punishment
#flashcards/vocabulary/topic-specific/law-crime-politics/laws-legislation
#flashcards/vocabulary/topic-specific/law-crime-politics/government-spending

#flashcards/vocabulary/topic-specific/travel-culture/tourism-types
#flashcards/vocabulary/topic-specific/travel-culture/cultural-heritage
#flashcards/vocabulary/topic-specific/travel-culture/migration-immigration

#flashcards/vocabulary/topic-specific/sport-leisure/professional-sports
#flashcards/vocabulary/topic-specific/sport-leisure/extreme-sports
#flashcards/vocabulary/topic-specific/sport-leisure/leisure-activities

#flashcards/vocabulary/phrasal-idioms/collocations-by-verb
#flashcards/vocabulary/phrasal-idioms/collocations-by-topic
#flashcards/vocabulary/phrasal-idioms/idioms-for-speaking

# Structure
#flashcards/structure/grammar-foundation/comparison
#flashcards/structure/grammar-foundation/conditional
#flashcards/structure/grammar-foundation/passive-voice
#flashcards/structure/grammar-foundation/cohesion

#flashcards/structure/writing-patterns/task-1/trend-language
#flashcards/structure/writing-patterns/task-1/comparative-language
#flashcards/structure/writing-patterns/task-1/map-describing
#flashcards/structure/writing-patterns/task-1/process-cycle

#flashcards/structure/writing-patterns/task-2/introduction-templates
#flashcards/structure/writing-patterns/task-2/opinion-argumentation
#flashcards/structure/writing-patterns/task-2/problem-solution-patterns
#flashcards/structure/writing-patterns/task-2/counter-argument

#flashcards/structure/speaking-patterns/part-1
#flashcards/structure/speaking-patterns/part-2
#flashcards/structure/speaking-patterns/part-3

# Sources
#flashcards/sources/ielts-cambridge-series
#flashcards/sources/authentic-reading
#flashcards/sources/mistakes-review
```

---

## 3. Implementation Guide

### A. Vocabulary Files (`glean/20_Vocabulary`)

In your `tpl_Vocabulary.md` or when processing files, ensure the **Tag is the FIRST line**, before the frontmatter.

**Example File:**
```markdown
#flashcards/vocabulary/health
---
tags:
  - vocabulary
category: word
mastery: 🔴 New
---
# arthritis
...
```

### B. Structure Files (`glean/30_Structures`)

Similarly for grammar structures, categorize by difficulty or function at the top.

**Example File:**
```markdown
#flashcards/structure/advanced
---
tags:
  - structure
mastery: 🔴 New
---
...
```

### C. Contextual/Article Cards

When creating cards directly inside an Article (in `glean/10_Sources/Articles`), you may not want to tag the whole file. Instead, use **Question Specific Tags** for individual flashcards scattered in the text.

**Example Inline Card:**
```markdown
#flashcards/sources/ielts-cam-19
What implies a 'modern lifestyle'?::It implies contemporary habits involving technology and urbanization.
```

---

## 4. Workflows

### 🆕 Creating New Cards
1. **Apply Template**: When applying `tpl_Vocabulary` or `tpl_Structure`.
2. **Select Deck**: Manually append the specific sub-deck to the existing `tags` property.
   - Change `tags: [vocabulary]` to `tags: [flashcards/vocabulary/your-topic]`.

### 🔄 Refactoring Existing Decks
If you want to move 50 words into a "Business" deck:
1. Open Obsidian Search.
2. Search for the words.
3. Use a batch editor (or manually) to append `/business` to their tags.
4. The Spaced Repetition plugin will automatically restructure the decks in the sidebar review queue.

## 5. Card Types & Templates

### A. Vocabulary Card Types (`tpl_Vocabulary.md`)
These generic card types apply to any topic in the `vocabulary` deck.

| Card # | Type | Purpose |
| :--- | :--- | :--- |
| **1** | **Meaning & Mental Model** | Define word + Vietnamese + Mental image. |
| **2** | **Production (Reverse)** | Given definition, recall the word. |
| **3** | **Usage & Analysis** | Create a sentence + analyze why it fits. |
| **4** | **Collocations by Logic** | Grouped collocations (Usage patterns). |
| **5** | **Word Upgrade** | Replace a basic word with this advanced one. |
| **6** | **Nuance Barrier** | Compare with a near-synonym. |
| **7** | **Scenario Reaction** | Use word in a specific emotional context. |
| **8** | **Etymology Story** | Origin story for memory hooking. |
| **9** | **Word Family** | Related forms (noun, verb, adj). |
| **10** | **IPA Decoding** | Pronunciation focus. |
| **11** | **Mistake Hunter** | Correct common errors. |
| **12** | **Antonym Flip** | Recall opposites. |

### B. Structure Card Types (`tpl_Structure.md`)
These correspond to grammar patterns in the `structure` deck.

| Card # | Type | Purpose |
| :--- | :--- | :--- |
| **1** | **Pattern Recognition** | Identify the formula/structure. |
| **2** | **Functional Meaning** | What does it express? (Vibe/function). |
| **3** | **Contextual Usage** | When to use (Formal/Informal). |
| **4** | **Example & Analysis** | Create an example. |
| **5** | **Error Correction** | Fix a broken sentence. |
| **6** | **Comparison (Nuance)** | Compare with similar structures. |
| **7** | **Transformation** | Rewrite a sentence using the structure. |
| **8** | **Writer's Rewrite** | Upgrade a sentence styling. |
| **9** | **Metaphor Deconstruction** | Analyze literal vs figurative meaning. |
| **10** | **Scenario Reaction** | Use mechanism in a dramatic context. |

## 6. Current Active Decks

Based on current vault analysis:

| Deck Name | Tag | Description |
| :--- | :--- | :--- |
| **Vocabulary** | `#flashcards/vocabulary` | Main deck for all discrete words. |
| **Structure** | `#flashcards/structure` | Main deck for grammar patterns. |

*Additional sub-decks will be created automatically as you add topics to your tags.*
