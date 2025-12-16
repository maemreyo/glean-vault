# 🚀 Glean Vault - Obsidian Vocabulary Learning System

Hệ thống học từ vựng và cấu trúc tiếng Anh được thiết kế đặc biệt cho Obsidian với phương pháp Spaced Repetition và kết nối tri thức.

## 📁 Cấu trúc thư mục

```
📁 glean/
├── 📁 00_Inbox/          # Ghi chú tạm, chưa xử lý
├── 📁 10_Sources/        # Nguồn học tập
│   ├── 📁 Videos/        # Video từ YouTube, TED, etc.
│   └── 📁 Articles/      # Bài báo, tin tức, blog
├── 📁 20_Vocabulary/     # Notes từ vựng (mỗi từ = 1 note)
├── 📁 30_Structures/     # Ngữ pháp, idioms, collocations
├── 📁 99_Templates/      # Templates cho Obsidian
│   ├── tpl_Source_Input.md
│   ├── tpl_Vocabulary.md
│   └── tpl_Structure.md
├── 📁 99_System/         # Dashboard và file hệ thống
│   └── Dashboard.md
└── 📁 .obsidian/         # Cấu hình Obsidian
```

## 🛠️ Plugins đã cài đặt

- ✅ **Templater** - Tự động điền template
- ✅ **Dataview** - Query và hiển thị dữ liệu
- ✅ **Spaced Repetition** - Ôn tập theo khoa học
- ✅ **Graph Link Types** - Tạo các loại liên kết đặc biệt
- ✅ **Dictionary** - Tra từ ngay trong Obsidian
- ✅ **HiWords** - Highlight từ khó trong bài đọc
- ✅ **Media Extended** - Xem video trực tiếp
- ✅ **Git** - Backup tự động

## 🎯 Workflow sử dụng

### 1. Thêm nguồn học mới
1. Tạo note mới trong `10_Sources/Videos/` hoặc `10_Sources/Articles/`
2. Sử dụng template `tpl_Source_Input`
3. Điền link và thông tin nguồn

### 2. Trích xuất từ vựng
1. Khi xem/đọc, bôi đen từ mới → tạo link `[[word]]`
2. Click vào link → tạo note mới trong `20_Vocabulary/`
3. Sử dụng template `tpl_Vocabulary`
4. Điền đầy đủ thông tin: IPA, định nghĩa, ví dụ, liên kết

### 3. Ôn tập hàng ngày
1. Mở `Dashboard.md` để xem tiến độ
2. Sử dụng Spaced Repetition plugin để ôn tập flashcards
3. Update mastery level sau mỗi lần ôn

### 4. Xem tiến độ
- Dashboard hiển thị thống kê chi tiết
- Graph view để xem kết nối giữa các từ
- Theo dõi số lượng từ đã học

## 📊 Màu sắc mastery level

- 🔴 **New** - Mới học (1-2 ngày)
- 🟡 **Learning** - Đang học (3-7 ngày)
- 🟢 **Familiar** - Quen thuộc (1-2 tuần)
- 🔵 **Mastered** - Đã thành thạo (1+ tháng)

## 🔗 Link types trong Graph

- `is_synonym_of` - Từ đồng nghĩa (xanh lá)
- `is_antonym_of` - Từ trái nghĩa (đỏ)
- `is_derived_from` - Từ gốc/phái sinh (vàng)
- `appears_in` - Xuất hiện trong (xanh dương)
- `related_to` - Liên quan (tím)

## 🎬 Ví dụ thực tế

1. Mở video YouTube về TED Talk
2. Tạo note trong `10_Sources/Videos/` với template `tpl_Source_Input`
3. Dùng Media Extended để xem video ngay trong Obsidian
4. Nghe thấy từ mới "procrastination"
5. Bôi đen → `[[procrastination]]` → tạo note
6. Điền thông tin vào template `tpl_Vocabulary`
7. Thêm liên kết: `[[is_synonym_of::delay]]`, `[[related_to::time management]]`
8. Tạo flashcard cho từ này
9. Lặp lại với các từ khác

## 🚀 Bắt đầu

1. Mở Obsidian với vault này
2. Check dashboard ở `99_System/Dashboard.md`
3. Bắt đầu với một video hoặc bài báo
4. Tạo từ vựng đầu tiên của bạn!

## 💡 Tips hiệu quả

- **Chất lượng hơn số lượng**: Chỉ note từ thực sự hữu ích
- **Ngữ cảnh là VUA**: Luôn ghi lại câu gốc
- **Tạo liên kết**: Kết nối từ mới với từ đã biết
- **Ôn tập đều đặn**: Duy trì thói quen hàng ngày
- **Sử dụng Graph**: Khám phá các kết nối bất ngờ

---

🎉 **Chúc bạn học tập hiệu quả với Glean Vault!**