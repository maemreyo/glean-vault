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
## 🌳 Root Word

```dataview
TABLE 
  Root as "Root",
  length(rows) as "Words"
FROM #vocabulary
WHERE Root != null
GROUP BY Root
SORT length(rows) DESC
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