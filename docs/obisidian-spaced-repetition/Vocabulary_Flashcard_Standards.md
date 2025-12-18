# Vocabulary Flashcard Standards

This document defines the strict formatting, syntax, and semantic rules for maintaining the high-quality Vocabulary Flashcard system in this vault.

## 1. General Architecture

### Syntax Rules
1.  **Headers:** All cards uses `**Card X: ...**` bold syntax. Do **NOT** use Markdown headers (`###`), which creates unwanted subdecks.
2.  **Separators:**
    -   Must have **at least one completely empty line** before every `**Card X**` header.
    -   Must have **no whitespace characters** on empty lines (no rogue `>`).
3.  **Question/Answer:**
    -   The `?` character is the delimiter.
    -   Always leave a blank line after the question block before the `?`.
4.  **Styling Strategy:**
    -   **Blockquotes (`>`)**: Used for the "Answer" block to create a visual container.
    -   **Icons**: Used to denote semantic fields (Definition, IPA, Example).
    -   **Typography**: Italics for metadata (POS, IPA), Bold for labels.

---

## 2. Card-by-Card Specifications

### Card 1: Meaning & Context
**Purpose:** The "Big Picture" card for recognition.

**Format:**
```markdown
**Card 1: Meaning & Context (Multi-line)**

What does **<word>** (*/<ipa>/*) mean?
?
> 📖 **Meaning:** <English Definition>
> 🇻🇳 **Vietnamese:** <Vietnamese Definition>
> 🗣️ **IPA:** */<ipa>/*
> 💡 **Nuance:** <Explanation of usage/connotation>
```
**Rules:**
-   **Meaning:** Concise English definition.
-   **Nuance:** explain *how* it differs from synonyms.

---

### Card 2: Production (Reverse)
**Purpose:** The hardest card. Active recall from definition to word.

**Format:**
```markdown
**Card 2: Production (Reverse)**

**Definition:** "<English Definition>"
**Vietnamese:** <Vietnamese Definition>
→ **Target Word?**
?
**<word>** (*/<ipa>/*)
```
**Rules:**
-   **Input:** Do NOT use blockquotes (`>`) for the question side here (clean layout).
-   **Prompt:** Always use `→ **Target Word?**`.

---

### Card 3: Usage
**Purpose:** Contextual understanding.

**Format:**
```markdown
**Card 3: Usage (Multi-line)**

Use **<word>** in a sentence.
?
> 📝 **Sentence:** <English Sentence>
> 🇻🇳 **Translation:** <Vietnamese Sentence>
```
**Rules:**
-   **Sentence:** Must be a valid, natural sentence.

---

### Card 4: Collocations
**Purpose:** Chunking and natural usage patterns.

**Format:**
```markdown
**Card 4: Collocations (Multi-line)**

List 3 common collocations for **<word>**.
?
> 🔗 **Collocations:**
> 1. <Collocation 1>
> 2. <Collocation 2>
> 3. <Collocation 3>
```

---

### Card 5: Word Family
**Purpose:** Morphology and etymology.

**Format:**
```markdown
**Card 5: Root & Word Family (Multi-line)**

Analyze the root/family of **<word>**.
?
> 🌱 **Root:** <Language> `<root_word>` (<meaning>)
> 👨‍👩‍👧 **Family:** 
> - *(<pos>)* <related_word>
> - *(<pos>)* <related_word>
```
**Rules:**
-   **Root:** Use code ticks for foreign roots: e.g., Latin `veritas`.
-   **Family:** Use bullet points for list. Italicize POS tags `*(noun)*`.

---

### Card 6: Context Cloze
**Purpose:** Active recall in context.

**Format:**
```markdown
**Card 6: Context Cloze**

> 🗣️ *<Sentence with ==word== hidden>*
>
> 🇻🇳 **Vi:** <Vietnamese Translation>
```
**Rules:**
-   **Visuals:** Use Blockquote `>` + Italics `*`.
-   **Deletion:** Use `==` syntax. E.g., `==acquittal==`.

---

### Card 7: IPA Decoding
**Purpose:** Pronunciation-to-Word recognition.

**Format:**
```markdown
**Card 7: IPA Decoding**

> 🔊 */<ipa>/*
?
**<word>**
```
**Rules:**
-   **Question:** The IPA is the prompt.
-   **Answer:** The word is the reveal.

---

## 3. Maintenance Guide
To update all files programmatically, use regex that respects:
1.  **Boundaries:** `\n\n**Card` (Double newline).
2.  **Typography**:
    -   POS: `\((noun|verb|adj)\)` → `*(\1)*`
    -   IPA: `/\w+/` → `*/\w+/*`
    -   Roots: `"word"` → `` `word` ``
