---
created: <% tp.file.creation_date("YYYY-MM-DD") %>
type: <% tp.system.suggester(["📺 Video", "📰 Article"], ["Video", "Article"]) %>
status: 🟡 Processing
tags: source/input
url:
language: English
---

# <% tp.file.title %>

## 🔗 Source Information

**Link gốc:** <% tp.file.cursor(1) %>
**Ngày học:** <% tp.date.now("YYYY-MM-DD") %>

---

## 📝 Notes & Key Points

<% tp.file.cursor(2) %>

---

## 💎 Vocabulary Mining

### New Words
- [[ ]] -
- [[ ]] -

### New Structures
- [[ ]] -
- [[ ]] -

---

## 🎯 Action Items
- [ ] Xem xong/Đọc xong
- [ ] Tạo notes cho từ mới
- [ ] Ôn tập lần 1
- [ ] Chuyển status → ✅ Completed

---

## 📊 Stats
**Words extracted:**
**Structures extracted:**