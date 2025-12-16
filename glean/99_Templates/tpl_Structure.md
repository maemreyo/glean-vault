---
created: <% tp.file.creation_date("YYYY-MM-DD") %>
tags: structure, flashcard, grammar
mastery: 🔴 New
type: <% tp.system.suggester(["Grammar", "Idiom", "Collocation", "Phrase"], ["grammar", "idiom", "collocation", "phrase"]) %>
source: [[<% tp.system.prompt("Nguồn?") %>]]
---

# <% tp.file.title %>

## 📐 Structure Pattern

**Pattern:** <% tp.file.cursor(1) %>

**Usage:** <% tp.file.cursor(2) %>

---

## 🧩 Context Example

> [!quote] Original
> <% tp.file.cursor(3) %>
> — From: [[<% tp.system.prompt("Nguồn?") %>]]

---

## 🎯 More Examples

1. ✅ <% tp.file.cursor(4) %>
2. ✅
3. ❌ Wrong:
   ✅ Right:

---

## 🧠 Flashcard

Question:: When do we use the structure **<% tp.file.title %>**?
Answer:: <% tp.file.cursor(5) %>

Question:: Create a sentence with: <% tp.file.title %>
Answer:: (Your answer)

---

## 🔗 Related Structures
- [[ ]]
- [[ ]]