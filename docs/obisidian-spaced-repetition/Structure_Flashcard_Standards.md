# Structure Flashcard Standards

This document defines the strict formatting, syntax, and semantic rules for maintaining the high-quality **Structure Flashcard System** in this vault.

## 1. General Architecture

### Syntax Rules
1.  **Headers:** All cards use `**Card X: Title**` bold syntax. Do **NOT** use Markdown headers (`###`), which creates unwanted subdecks.
2.  **Separators:**
    -   Must have **at least one completely empty line** before every `**Card X**` header.
    -   **Question/Answer Delimiter:** The `?` character must be on its own line between the Question block and the Answer block for Multi-line cards.
3.  **Styling Strategy:**
    -   **Rich Text:** Both Questions and Answers use specialized semantic icons.
    -   **Blockquotes (`>`)**: Used exclusively for the **Answer** block to create a visual container.
    -   **Icons:** specific emojis assigned to each card type (e.g., 🧩 Pattern, 🎭 Scenario).

---

## 2. Card Specifications (Standard 7)

### Card 1: Pattern Recognition
**Purpose:** Identifying the grammatical formula.

**Format:**
```markdown
**Card 1: Pattern Recognition**

🧩 **Pattern Analysis:** What is the structure pattern for **<phrase>**?
?
> 🏗️ **Structure:** [Component 1] + [Component 2] ...
```

---

### Card 2: Functional Meaning
**Purpose:** Understanding purpose and definition.

**Format:**
```markdown
**Card 2: Meaning**

🤔 **Meaning:** What does **<phrase>** express?
?
> 📖 **Function:** <Definition/Function>
```

---

### Card 3: Contextual Usage
**Purpose:** Knowing when to use it.

**Format:**
```markdown
**Card 3: Usage**

❓ **Usage:** When should you use **<phrase>**?
?
> 📝 **Context:** <Usage Context (Formal/Informal/Academic)>
```

---

### Card 4: Production (Example)
**Purpose:** creating a sentence from scratch.

**Format:**
```markdown
**Card 4: Example**

✍️ **Production:** Create a sentence with **<phrase>** about <topic>
?
> 🧪 **Example:** <Example Sentence>
```

---

### Card 5: Error Correction
**Purpose:** Identifying common pitfalls.

**Format:**
```markdown
**Card 5: Error Correction**

🕵️ **Spot the Error:** What's wrong with: "<Incorrect Sentence>"
?
> 🛠️ **Correction:** <Explanation of error>
```

---

### Card 6: Comparison
**Purpose:** Distinguishing from synonyms.

**Format:**
```markdown
**Card 6: Comparison**

🆚 **Comparison:** How is **<phrase>** different from [[<related_structure>]]?
?
> ⚖️ **Difference:** <Detailed comparison>
```

---

### Card 7: Transformation
**Purpose:** Rewrite skill.

**Format:**
```markdown
**Card 7: Transformation**

🔄 **Transformation:** Transform this sentence using **<phrase>**: "<Source Sentence>"
?
> 🔄 **Result:** <Target Sentence>
```

---

## 3. Creative Genius Cards (Advanced Loop)

These cards are designed for C1/C2 mastery, focusing on nuance, register shifting, and metaphorical competence.

### Card 8: Writer's Rewrite
**Purpose:** Register shifting (Basic -> Advanced).

**Format:**
```markdown
**Card 8: Writer's Rewrite**

✍️ **Rewrite:** Upgrade this boring sentence using **<phrase>**: "<Basic Sentence>"
?
> 🖋️ **Improved:** "<Advanced Sentence>"
> 💡 **Effect:** <Explanation of stylistic improvement>
```

---

### Card 9: Metaphor Deconstruction
**Purpose:** Deep semantic analysis.

**Format:**
```markdown
**Card 9: Metaphor Deconstruction**

🧩 **Deconstruct:** In **<phrase>**, what does "<word>" imply?
?
> 🔍 **Insight:** <Analysis of metaphorical imagery>
```

---

### Card 10: Scenario Application
**Purpose:** Real-world contextual flexibility.

**Format:**
```markdown
**Card 10: Scenario Application**

🎭 **Scenario:** <Specific Role/Situation Prompt>
?
> 🎬 **Narration:** "<hypothetical_sentence>"
```

---

## 4. Maintenance Guide

### Footer Handling
-   The "Learning Progress" footer (starting with `## 📈`) must remain **outside** any blockquotes.
-   Ensure a separator `---` exists between the last card (Card 10) and the footer.

### Visual Icon Legend
| Icon | Meaning | Card |
| :--- | :--- | :--- |
| 🧩 | Pattern / Deconstruct | 1, 9 |
| 🏗️ | Structure Formula | 1 |
| 🤔 | Meaning Question | 2 |
| 📖 | Function Definition | 2 |
| ❓ | Usage Question | 3 |
| 📝 | Context Description | 3 |
| ✍️ | Production / Rewrite | 4, 8 |
| 🧪 | Example Sentence | 4 |
| 🕵️ | Spot the Error | 5 |
| 🛠️ | Correction | 5 |
| 🆚 | Comparison | 6 |
| ⚖️ | Difference Analysis | 6 |
| 🔄 | Transformation | 7 |
| 🖋️ | Improved Version | 8 |
| 💡 | Stylistic Effect | 8 |
| 🔍 | Semantic Insight | 9 |
| 🎭 | Scenario Prompt | 10 |
| 🎬 | Narration Response | 10 |
