---
created: <% tp.file.creation_date("YYYY-MM-DD") %>
tags: structure, flashcard, grammar
mastery: 🔴 New
type: <% tp.system.suggester(["Grammar", "Idiom", "Collocation", "Phrase", "Sentence"], ["grammar", "idiom", "collocation", "phrase", "sentence"]) %>
source: [[<%*
const activeFile = app.workspace.getActiveFile();
if (activeFile) {
  tR += activeFile.basename;
} else {
  tR += tp.system.prompt("No active file. Enter source:");
}
%>]]
---

# <% tp.file.title %>

<%*
const type = tp.frontmatter.type;
*%>

## 📊 Meta Information

| Property | Value |
| -------- | ----- |
| **Type** | <% type %> |
| **Structure** |  |
| **Complexity** |  |
| **CEFR Level** | (A1/A2/B1/B2/C1/C2) |
| **Frequency** | (common/uncommon/rare) |
| **Register** | (formal/informal/academic/business) |

---

<%* if (type === "phrase") { *%>

## 🎯 Phrase Analysis

### Phrase Structure
**Type:** (phrasal verb/idiom/collocation/compound noun)
**Pattern:** <% tp.file.cursor(1) %>
**Components:**
- **Main word:**
- **Particle/Preposition:**
- **Additional elements:**

### Meaning
**Literal meaning:** <% tp.file.cursor(2) %>
**Figurative meaning:**
**Vietnamese translation:**
**Usage notes:**

### Variations
1. **Variation 1:**  -
2. **Variation 2:**  -

<%* } else if (type === "sentence") { *%>

## 📝 Sentence Analysis

### Sentence Structure
**Type:** (simple/compound/complex)
**Complexity:** (basic/intermediate/advanced)
**Purpose:** (inform/persuade/describe/question/etc)
**Tone:** (formal/informal/neutral/ironic/etc)

### Components
**Subject:** <% tp.file.cursor(1) %>
**Predicate:**
**Main clause:**
**Subordinate clauses:**

### Meaning Analysis
**Main idea:** <% tp.file.cursor(2) %>
**Supporting ideas:**
**Sentiment:** (positive/negative/neutral/mixed)

### Style Analysis
**Clarity:**
**Conciseness:**
**Emphasis:**

<%* } else if (type === "collocations") { *%>

## 🔗 Collocation Analysis

### Focus Words
<% tp.file.cursor(1) %>

### Collocation Patterns
**Type:** (verb+noun/adjective+noun/adverb+verb/etc)
**Frequency level:** (very common/common/uncommon)

### Identified Collocations
1. **:**
   - **Structure:**
   - **Meaning:**
   - **Usage:**
   - **Frequency:**

2. **:**
   - **Structure:**
   - **Meaning:**
   - **Usage:**
   - **Frequency:**

3. **:**
   - **Structure:**
   - **Meaning:**
   - **Usage:**
   - **Frequency:**

<%* } else if (type === "idioms") { *%>

## 🎭 Idiom Analysis

### Idiom Information
**Full idiom:** <% tp.file.cursor(1) %>
**Type:** (proverb/slang/metaphor/etc)
**Cultural context:** (British/American/global/etc)
**Historical period:**

### Meaning
**Literal meaning:**
**Figurative meaning:** <% tp.file.cursor(2) %>
**Origin:**
- **Source:**
- **Historical context:**

### Usage
**Context:**
**Register:** (formal/informal/literary/business)
**Frequency:** (very common/common/uncommon/archaic)

### Variations
1. **Form:**  -
2. **Form:**  -

### Related Expressions
-  -
-  -

<%* } else if (type === "grammar") { *%>

## 📐 Grammar Analysis

### Grammar Focus
**Structure type:** <% tp.file.cursor(1) %>
**Pattern:**
**Complexity level:** (basic/intermediate/advanced)

### Rule Explanation
**Description:** <% tp.file.cursor(2) %>
**Formation:**
**Usage rules:**

### Examples
1. **Correct:**
   **Translation:**
   **Analysis:**

2. **Correct:**
   **Translation:**
   **Analysis:**

### Common Errors
1. **Error:**
   **Correction:**
   **Explanation:**

2. **Error:**
   **Correction:**
   **Explanation:**

### Variations
- **Formal:**
- **Informal:**
- **Alternative:**

<%* } *%>

---

## 📝 Usage Examples

### Example 1

| | |
| --- | --- |
| **Sentence** | <% tp.file.cursor(3) %> |
| **Translation** | |
| **Context** | |
| **Source** | |

### Example 2

| | |
| --- | --- |
| **Sentence** | |
| **Translation** | |
| **Context** | |
| **Source** | |

### Example 3

| | |
| --- | --- |
| **Sentence** | |
| **Translation** | |
| **Context** | |
| **Source** | |

---

## ⚠️ Common Mistakes

| Mistake ❌ | Correction ✅ | Explanation |
| --- | --- | --- |
| | | |
| | | |
| | | |

---

## 🎯 Learning Tips

### Memory Techniques
1. <% tp.file.cursor(4) %>
2.
3.

### Practice Exercises
1.
2.
3.

### Usage Guidelines
- When to use:
- When to avoid:
- Formal vs. informal:

---

## 🔗 Related Structures
- [[ ]]
- [[ ]]
- [[ ]]

---

## 🧩 Context

> [!quote] Original
> <% tp.file.cursor(5) %>
> — From: [[<%*
const activeFile = app.workspace.getActiveFile();
if (activeFile) {
  tR += activeFile.basename;
} else {
  tR += tp.system.prompt("No active file. Enter source:");
}
%>]]

**Context Analysis:**


---

## 🧠 Spaced Repetition Flashcards

### Card 1: Recognition
**Question::** What does **<% tp.file.title %>** mean?
**Answer::**

### Card 2: Production
**Question::** Complete the sentence: [sentence with blank]
**Answer::**

### Card 3: Usage
**Question::** Use **<% tp.file.title %>** in a [context type] sentence.
**Answer::**

### Card 4: Error Correction
**Question::** Correct this sentence: [incorrect sentence]
**Answer::**

### Card 5: Pattern Recognition
**Question::** Identify the structure in: [example sentence]
**Answer::**

---

## 📈 Learning Progress

**Times encountered:** 1
**Times reviewed:** 0
**Confidence level:** 🔴 New → 🟡 Learning → 🟢 Familiar → 🔵 Mastered
**Next review:**

---

## 💭 Personal Notes & Mnemonics

### Visual Association


### Memory Hook


### Personal Connection


---

## 🔖 Tags & Categories

**Type:** #<% type %>
**Themes:** #
**Topics:** #
**Difficulty:** #
**Context:** #spoken #written #academic #business #casual