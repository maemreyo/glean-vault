---
created: <% tp.file.creation_date("YYYY-MM-DD") %>
tags: vocabulary, flashcard
type: word
mastery: 🔴 New
difficulty: <% tp.system.suggester(["⭐ Easy", "⭐⭐ Medium", "⭐⭐⭐ Hard"], ["easy", "medium", "hard"]) %>
reviewed: 0
source: [[<% tp.system.prompt("Nguồn (tên bài báo/video)?") %>]]
---

# <% tp.file.title %>

## 🔊 Pronunciation & IPA
**IPA:** /<% tp.file.cursor(1) %>/
**Audio:** (dùng Dictionary plugin để nghe)

---

## 💡 Definition & Meaning

**Meaning (English):** <% tp.file.cursor(2) %>

**Nghĩa (Tiếng Việt):** <% tp.file.cursor(3) %>

**Word type:** <% tp.system.suggester(["noun", "verb", "adjective", "adverb", "preposition", "conjunction"], ["noun", "verb", "adjective", "adverb", "preposition", "conjunction"]) %>

---

## 🧩 Context (Ngữ cảnh gốc)

> [!quote] Original Sentence
> <% tp.file.cursor(4) %>
>
> — From: [[<% tp.system.prompt("Tên nguồn?") %>]]

**Giải thích ngữ cảnh:**
<% tp.file.cursor(5) %>

---

## 🎯 Example Sentences (Tự tạo)

1. <% tp.file.cursor(6) %>
2.
3.

---

## 🕸️ Connections & Relationships

### Related Words
- **Synonym (Đồng nghĩa):** [[ ]]
- **Antonym (Trái nghĩa):** [[ ]]
- **Word Family:** [[ ]] → [[ ]] → [[ ]]
- **Collocation:** [[ ]] + [[ ]]

---

## 🧠 Spaced Repetition Cards

### Card 1: Recognition
Question:: What does **<% tp.file.title %>** mean?
Answer:: <% tp.file.cursor(7) %>

### Card 2: Production
Question:: How do you say "..." in English? (context)
Answer:: **<% tp.file.title %>**

### Card 3: Usage
Question:: Complete: "Yesterday, I ___ (verb) to the store"
Answer:: <% tp.file.title %> (với giải thích)

---

## 📈 Learning Progress

**Lần gặp:** 1
**Lần ôn tập:** 0
**Độ tự tin:** 🔴 Chưa nhớ

---

## 💭 Personal Notes & Mnemonic
> Thủ thuật ghi nhớ cá nhân, hình ảnh liên tưởng, câu chuyện...

<% tp.file.cursor(8) %>