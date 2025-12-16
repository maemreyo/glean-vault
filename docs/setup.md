# 🚀 Obsidian Vocabulary Learning System - Setup Complete

## 📋 CHECKLIST - Làm theo thứ tự này

- [ ] **Bước 1:** Tạo cấu trúc thư mục
- [ ] **Bước 2:** Cấu hình Templater
- [ ] **Bước 3:** Tạo các Template files
- [ ] **Bước 4:** Cấu hình Graph Link Types
- [ ] **Bước 5:** Tạo Dashboard
- [ ] **Bước 6:** Cấu hình Git auto-backup
- [ ] **Bước 7:** Test workflow với một ví dụ

---

## 🗂️ BƯỚC 1: Tạo Cấu trúc Thư mục

Tạo các thư mục sau trong vault của bạn:

```
📁 Your Vault/
├── 📁 00_Inbox/
├── 📁 10_Sources/
│   ├── 📁 Videos/
│   └── 📁 Articles/
├── 📁 20_Vocabulary/
├── 📁 30_Structures/
├── 📁 99_Templates/
└── 📁 99_System/
    └── 📄 Dashboard.md
```

**Giải thích:**
- `00_Inbox`: Nơi chứa ghi chú tạm, chưa xử lý
- `10_Sources`: Tất cả nguồn học (video, bài báo)
- `20_Vocabulary`: Mỗi từ vựng = 1 note
- `30_Structures`: Cấu trúc ngữ pháp, idioms, collocations
- `99_Templates`: Chứa các template
- `99_System`: Dashboard và các file hệ thống

---

## ⚙️ BƯỚC 2: Cấu hình Templater

1. Vào `Settings` → `Templater`
2. **Template folder location:** Chọn `99_Templates`
3. **Trigger Templater on new file creation:** BẬT
4. Thêm các phím tắt (tuỳ chọn):
   - `Ctrl/Cmd + T`: Templater: Open Insert Template modal
   - `Alt + N`: Templater: Create new note from template

---

## 📝 BƯỚC 3: Tạo các Template Files

### Template 1: Source Input (Video/Article)

**Tên file:** `99_Templates/tpl_Source_Input.md`

```markdown
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
```

---

### Template 2: Vocabulary Note

**Tên file:** `99_Templates/tpl_Vocabulary.md`

```markdown
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
```

---

### Template 3: Structure/Grammar Note

**Tên file:** `99_Templates/tpl_Structure.md`

```markdown
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
```

---

## 🎨 BƯỚC 4: Cấu hình Graph Link Types

1. Vào `Settings` → `Graph Link Types`
2. Thêm các link types sau:

```
is_synonym_of → Màu xanh lá
is_antonym_of → Màu đỏ
is_derived_from → Màu vàng
appears_in → Màu xanh dương
related_to → Màu tím
```

**Cách dùng:**
- Trong note, thay vì viết `[[happy]]`, viết: `[[is_synonym_of::joyful]]`
- Hoặc dùng command `Graph Link Types: Add link type`

---

## 📊 BƯỚC 5: Tạo Dashboard

**Tên file:** `99_System/Dashboard.md`

```markdown
# 📊 Vocabulary Learning Dashboard

Last updated: `= date(today)`

---

## 🔢 Overall Statistics

```dataview
TABLE WITHOUT ID
  length(rows) as "Total Words"
FROM #vocabulary
```

```dataview
TABLE WITHOUT ID
  length(rows.file) as "Total Structures"
FROM #structure
```

---

## 🆕 Recently Added (20 từ mới nhất)

```dataview
TABLE 
  mastery as "Mastery",
  difficulty as "Difficulty",
  source as "Source",
  file.ctime as "Added"
FROM #vocabulary
SORT file.ctime DESC
LIMIT 20
```

---

## 🔴 Need Review (Từ chưa thuộc)

```dataview
TABLE
  difficulty as "Difficulty",
  source as "Source",
  reviewed as "Times Reviewed"
FROM #vocabulary
WHERE mastery = "🔴 New" OR mastery = "🟡 Learning"
SORT file.ctime DESC
```

---

## ✅ Mastered Words (Từ đã thuộc)

```dataview
TABLE
  source as "Source",
  reviewed as "Reviews"
FROM #vocabulary
WHERE mastery = "🟢 Mastered"
SORT file.ctime DESC
LIMIT 10
```

---

## 📚 Sources Progress

```dataview
TABLE
  length(file.outlinks) as "Words Extracted",
  status as "Status"
FROM "10_Sources"
SORT file.ctime DESC
```

---

## 📈 This Week's Activity

```dataview
TABLE WITHOUT ID
  file.link as "Word",
  file.ctime as "Added"
FROM #vocabulary
WHERE file.ctime >= date(today) - dur(7 days)
SORT file.ctime DESC
```

---

## 🎯 Daily Goals
- [ ] Học 10 từ mới
- [ ] Ôn tập 20 từ cũ
- [ ] Hoàn thành 1 source material
```

---

## 💾 BƯỚC 6: Cấu hình Git Auto-backup

1. Vào `Settings` → `Git`
2. **Cấu hình:**
   - `Automatic pull on startup`: BẬT
   - `Automatic push on commit`: BẬT
   - `Auto backup interval (minutes)`: `30`
   - `Commit message`: `vault backup: {{date}}`

3. **Setup lần đầu:**
   - Tạo repo trên GitHub (private)
   - Trong terminal tại thư mục vault:
   ```bash
   git init
   git remote add origin YOUR_REPO_URL
   git add .
   git commit -m "Initial setup"
   git push -u origin main
   ```

---

## 🎬 BƯỚC 7: Test Workflow - Ví dụ Thực tế

### Scenario: Học từ một video YouTube

1. **Mở Obsidian** → Tạo note mới trong `10_Sources/Videos/`
2. **Đặt tên:** "BBC - Climate Change Documentary"
3. **Áp dụng template:** `tpl_Source_Input`
4. **Dán link YouTube** vào trường URL
5. **Dùng Media Extended:** 
   - Click chuột phải vào link → "Open with Media Extended"
   - Video sẽ mở ngay trong Obsidian
   
6. **Trong khi xem:**
   - Nghe thấy từ mới "mitigation" (00:05:23)
   - Bấm phím tắt timestamp (thường là `Ctrl + T`)
   - Ghi chú: "[00:05:23] mitigation - giảm thiểu"

7. **Tạo note từ vựng:**
   - Bôi đen "mitigation" → `[[mitigation]]`
   - Click vào link → Tạo note mới trong `20_Vocabulary/`
   - Áp dụng `tpl_Vocabulary`

8. **Tra từ ngay:**
   - Mở Dictionary plugin (sidebar phải)
   - Gõ "mitigation" → Copy định nghĩa vào note

9. **Tạo liên kết:**
   - Thêm synonym: `[[is_synonym_of::reduction]]`
   - Thêm related: `[[related_to::climate change]]`

10. **Lưu và xem Graph:**
    - Mở Graph View (`Ctrl + G`)
    - Thấy node "mitigation" kết nối với "reduction" và "climate change"

---

## 🔄 Daily Workflow

### Mỗi Sáng (15-20 phút)
1. Mở **Dashboard** → Check "Need Review"
2. Mở **Spaced Repetition** plugin
3. Ôn tập các flashcard theo lịch
4. Đánh giá: Hard / Good / Easy

### Khi Học Mới (30-60 phút)
1. Chọn source (video/article)
2. Tạo note từ template
3. Vừa xem/đọc vừa highlight từ mới
4. Tạo vocabulary notes ngay (đừng để sau!)
5. Thêm flashcards
6. Update mastery level

### Cuối Ngày (5 phút)
1. Check Dashboard
2. Git sẽ tự backup
3. Review tiến độ

---

## 🎓 Pro Tips

### Tip 1: Sử dụng HiWords cho Articles
- Copy bài báo → Paste vào note
- Bật HiWords → Tự động highlight từ khó
- Click vào từ được highlight → Tạo note ngay

### Tip 2: Color Code Mastery Levels
- 🔴 New (1-2 ngày)
- 🟡 Learning (3-7 ngày) 
- 🟢 Familiar (1-2 tuần)
- 🔵 Mastered (1+ tháng)

### Tip 3: Batch Processing
- Đừng tạo note cho MỌI từ
- Chỉ note từ thực sự hữu ích
- Aim for quality, not quantity

### Tip 4: Graph Navigation
- Dùng Graph để review connections
- Click vào từ → Xem related words
- Học theo "cụm từ" thay vì riêng lẻ

---

## ✅ Setup Complete Checklist

Kiểm tra lại tất cả:

- [ ] Đã tạo đủ 6 thư mục chính
- [ ] Đã tạo 3 template files
- [ ] Templater đã được cấu hình
- [ ] Graph Link Types đã setup
- [ ] Dashboard đã hiển thị đúng
- [ ] Git backup đang chạy
- [ ] Đã test với 1 ví dụ thực tế
- [ ] Spaced Repetition hoạt động

---

## 🆘 Troubleshooting

**Lỗi: Template không hiện**
→ Check lại `Settings` → `Templater` → Template folder path

**Lỗi: Dataview không chạy**
→ `Settings` → `Dataview` → Enable "Enable JavaScript Queries"

**Lỗi: Media Extended không mở video**
→ Cài thêm iframe player trong settings của Media Extended

**Flashcards không xuất hiện**
→ Check format `Question::` và `Answer::` (2 dấu hai chấm!)

---

## 🎉 You're All Set!

Bây giờ bạn có một hệ thống hoàn chỉnh để:
- ✅ Thu thập từ vựng từ mọi nguồn
- ✅ Tổ chức theo cấu trúc logic
- ✅ Tạo kết nối giữa các từ
- ✅ Ôn tập theo khoa học (Spaced Repetition)
- ✅ Theo dõi tiến độ
- ✅ Backup tự động

**Bắt đầu ngay với một video hoặc bài báo yêu thích của bạn! 🚀**