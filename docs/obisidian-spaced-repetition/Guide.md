# Hướng dẫn Chi tiết Cú pháp Obsidian Spaced Repetition (SR)

Tài liệu này cung cấp hướng dẫn chuyên sâu về cú pháp tạo flashcards, bao gồm các tính năng nâng cao và ví dụ minh họa.

## 1. Thẻ Một Dòng (Single-line Cards)

Loại thẻ này phù hợp cho các câu hỏi ngắn, định nghĩa từ vựng, hoặc sự kiện lịch sử.

### 1.1. Thẻ Cơ bản (Basic)
Cấu trúc: `Câu hỏi::Câu trả lời`

**Ví dụ:**
- `Thủ đô của Nhật Bản là gì?::Tokyo`
- `H2O là công thức hóa học của?::Nước`

### 1.2. Thẻ Đảo Ngược (Reversed)
Cấu trúc: `Mặt 1:::Mặt 2`
Tác dụng: Tạo ra 2 thẻ riêng biệt (Mặt 1 -> Mặt 2 và Mặt 2 -> Mặt 1).

**Ví dụ:**
- `Apple:::Quả táo`
  -> Creates Card 1: Q: Apple / A: Quả táo
  -> Creates Card 2: Q: Quả táo / A: Apple
- `1 kg:::1000 g`

## 2. Thẻ Nhiều Dòng (Multi-line Cards)

Dùng cho nội dung dài, danh sách, hoặc nội dung cần định dạng phức tạp.

### 2.1. Thẻ Cơ bản (Basic)
Cấu trúc: Sử dụng `?` trên một dòng riêng biệt để ngăn cách.

```markdown
Câu hỏi dòng 1
Câu hỏi dòng 2
?
Câu trả lời dòng 1
Câu trả lời dòng 2
```

### 2.2. Thẻ Đảo Ngược (Reversed)
Cấu trúc: Sử dụng `??` trên một dòng riêng biệt.

```markdown
Khái niệm: Spaced Repetition
??
Kỹ thuật lặp lại ngắt quãng giúp cải thiện trí nhớ dài hạn.
```

## 3. Thẻ Điền Khuyết (Cloze Cards)

Ẩn một phần nội dung để kiểm tra khả năng nhớ từ khóa hoặc ngữ cảnh.

**Các cách tạo Cloze:**
1. **Highlight (Mặc định)**: `==từ cần ẩn==`
   - Ví dụ: `Thủ đô của ==Việt Nam== là Hà Nội.`
2. **Bold (Cần bật trong setting)**: `**từ cần ẩn**`
3. **Curly Braces (Cần bật trong setting)**: `{{từ cần ẩn}}`

**Cloze nâng cao:**
Trong một câu có thể có nhiều vị trí điền khuyết. Mỗi vị trí sẽ tạo ra một thẻ riêng (sibling cards).
- Ví dụ: `==Hà Nội== là thủ đô của ==Việt Nam==.`
  -> Card 1: `[...] là thủ đô của Việt Nam.`
  -> Card 2: `Hà Nội là thủ đô của [...].`

## 4. Nội Dung Nâng Cao (Advanced Support)

Plugin hỗ trợ hầu hết các định dạng Markdown của Obsidian trong thẻ.

### 4.1. Hình ảnh (Images)
Bạn có thể chèn hình ảnh vào câu hỏi hoặc câu trả lời.

```markdown
Đây là lá cờ nước nào?
![[flag-vietnam.png]]
?
Việt Nam
```

### 4.2. Khối Mã (Code Blocks)
Rất hữu ích để học lập trình.

```markdown
Cú pháp in ra màn hình trong Python?
?
```python
print("Hello World")
```
```

### 4.3. Công thức Toán học (LaTeX)
Sử dụng `$` hoặc `$$` để viết công thức.

```markdown
Công thức tính diện tích hình tròn?
?
$$A = \pi r^2$$
```

### 4.4. Audio & Video
Nhúng file âm thanh để học phát âm.

```markdown
Nghe và điền từ còn thiếu:
![[audio.mp3]]
The quick brown fox ==jumps== over the lazy dog.
```

## 5. Quy tắc & Lưu ý

1. **Dòng trống**: Plugin sử dụng dòng trống để xác định điểm bắt đầu và kết thúc của một thẻ nhiều dòng. Hãy đảm bảo có dòng trống giữa các thẻ.
2. **Thụt đầu dòng**: Câu trả lời có thể giữ nguyên thụt đầu dòng (indentation) của danh sách (lists).
3. **HTML**: Bạn có thể dùng thẻ HTML như `<br>` để xuống dòng trong thẻ một dòng nếu cần thiết (nhưng nên dùng thẻ nhiều dòng thì hơn).
4. **ID Thẻ**: Sau khi review lần đầu, plugin sẽ thêm ID (dạng `<!--SR:...!-->`). **Không được sửa hoặc xóa** ID này thủ công.

## 6. Ví dụ Tổng hợp

```markdown
# Flashcards Ôn Tập

## Lịch sử
Chiến thắng Điện Biên Phủ năm nào?::1954

## Lập trình
Giải thích cơ chế Event Loop?
?
Event Loop là cơ chế giúp Javascript thực hiện các tác vụ bất đồng bộ (non-blocking)...

## Tiếng Anh
Water:::Nước

## Cloze
Công thức nước là ==H2O== và khí cacbonic là ==CO2==.
```
