# /how-recent-changes - Understand Recent Git Changes

## Purpose

Phân tích và giải thích các thay đổi hiện tại trong thư mục làm việc, bao gồm cả staged changes (sẵn sàng commit) và unstaged changes (đang trong quá trình làm việc). Command này giúp bạn hiểu trạng thái công việc hiện tại, xác nhận ý định của bạn và phát hiện các vấn đề tiềm ẩn trước khi commit.

## Aliases

```bash
/recent-changes
/status-explained
/diff-explained
```

## Usage

```bash
# Basic usage (analyzes current git status and saves by default)
/how-recent-changes

# Analyze recent commits
/how-recent-changes --recent=5              # Last 5 commits
/how-recent-changes --commit=abc123         # Specific commit
/how-recent-changes --commit=abc123..def456 # Commit range

# Compare with plan file
/how-recent-changes --plan=plans/feature-x.md
/how-recent-changes --recent=3 --plan=plans/auth-update.md

# With specific analysis depth
/how-recent-changes --deep

# Focus on specific files
/how-recent-changes --files=src/components,src/utils
/how-recent-changes --recent=5 --files=src/auth

# Skip saving to file
/how-recent-changes --no-save

# Output in different formats
/how-recent-changes --format=json
```

---

## Workflow

### Phase 1: Gather Git Status & Diffs 🔍

**Agent**: [`git-manager`](.claude/agents/git-manager.md)

**Goal**: Retrieve the raw data about what has changed.

**Steps**:

{{ if not --recent and not --commit }}
1.  **Check Git Status**
    ```bash
    git status
    ```

2.  **Get Unstaged Changes**
    ```bash
    git diff
    ```

3.  **Get Staged Changes**
    ```bash
    git diff --staged
    ```

4.  **Identify Modified Files**
    - List of files with staged changes
    - List of files with unstaged changes
    - List of untracked files
{{ endif }}

{{ if --recent }}
1.  **Get Recent Commits**
    ```bash
    git log --oneline -$RECENT
    ```

2.  **Get Changed Files in Recent Commits**
    ```bash
    git diff --name-only HEAD~$RECENT..HEAD
    ```

3.  **Get Detailed Changes**
    ```bash
    git diff HEAD~$RECENT..HEAD
    ```

4.  **Commit Analysis**:
    - Extract commit messages and categorize changes
    - Identify authors and timestamps
    - Note breaking changes or critical updates
{{ endif }}

{{ if --commit and not --commit contains '..' }}
1.  **Get Specific Commit Details**
    ```bash
    git show --stat $COMMIT
    ```

2.  **Get Files Changed**
    ```bash
    git show --name-only --format="" $COMMIT
    ```

3.  **Get Diff for Commit**
    ```bash
    git show $COMMIT
    ```
{{ endif }}

{{ if --commit and --commit contains '..' }}
1.  **Get Commits in Range**
    ```bash
    git log --oneline $COMMIT
    ```

2.  **Get Changed Files in Range**
    ```bash
    git diff --name-only $COMMIT
    ```

3.  **Get Detailed Changes**
    ```bash
    git diff $COMMIT
    ```
{{ endif }}

---

### Phase 2: Analyze Context & Intent 🧠

**Agent**: [`researcher`](.claude/agents/researcher.md)

**Skills**: 
- [`pattern-analysis`](.claude/skills/methodology/pattern-analysis/SKILL.md) - To identify code patterns
- [`sequential-thinking`](.claude/skills/methodology/sequential-thinking/SKILL.md) - For logical analysis

**Goal**: Interpret the changes to understand the high-level goal and implementation details.

**Analysis Tasks**:

1.  **Plan Comparison (if --plan flag provided)**:
    - Read the plan file specified using [`ReadMcpResourceTool`](https://docs.anthropic.com)
    - Extract tasks and requirements from plan
    - Parse plan structure:
      - Tasks/Checklists
      - Implementation requirements
      - File changes expected
      - Acceptance criteria
    - Compare actual changes with planned items:
      - ✅ Completed tasks (matching changes found)
      - ⏳ In-progress tasks (partial changes found)
      - ❌ Missing tasks (no changes found)
      - ➕ Extra work (changes not in plan)
    - Calculate metrics:
      - Completion percentage: `(Completed tasks / Total tasks) * 100`
      - Task breakdown by priority
      - File coverage percentage
    - Generate detailed comparison report

2.  **Infer Intent**:
    - Look at the combination of changes.
    - Is this a refactor? A feature addition? A bug fix?
    - consistency check: Do the changes match the inferred intent?
    - Use [`pattern-analysis`](.claude/skills/methodology/pattern-analysis/SKILL.md) to identify recurring patterns

3.  **Analyze Staged vs. Unstaged**:
    - **Staged**: likely a coherent set of changes ready for a commit. Analyze them as a unit
    - **Unstaged**: likely work in progress or experimental changes.
    - Check for overlap: Are there files with both staged and unstaged changes? This can be confusing and risky
    - Apply [`sequential-thinking`](.claude/skills/methodology/sequential-thinking/SKILL.md) to understand workflow

4.  **Detailed File Analysis**:
    - For each modified file, determine *what* changed logically (not just line-by-line).
    - "Added validation to `UserForm`" instead of "Added lines 40-45".
    - Use [`pattern-analysis`](.claude/skills/methodology/pattern-analysis/SKILL.md) to understand architectural patterns

5.  **Risk Assessment**:
    - Are there breaking changes?
    - Are there `console.log` or debug code left?
    - Are there missing tests for new logic?
    - Use [`sequential-thinking`](.claude/skills/methodology/sequential-thinking/SKILL.md) to evaluate potential issues

---

### Phase 3: Synthesize Report 📝

**Agent**: [`docs-manager`](.claude/agents/docs-manager.md)

**Goal**: Present the analysis in a structured, actionable format.
*Only runs when --save flag is enabled or when explicitly requested*

**Output Template**:

```markdown
# 🕵️ Phân Tích Thay Đổi Gần Đây

## 🎯 Tóm Tắt
[Tóm tắt cấp cao về mục tiêu của các thay đổi này, ví dụ: "Refactor luồng Authentication và sửa lỗi chính tả trong Dashboard."]

{{ if --recent or --commit }}
---

## 📜 Lịch Sử Commit
{{ if --recent }}
### **$RECENT Commits Gần Nhất**
{{ for each commit in commits }}
- **Commit**: `commit_hash` - `commit_message` (author, date)
  - Files: [list of changed files]
  - Type: [feature|fix|refactor|docs|chore]
{{ endfor }}
{{ endif }}

{{ if --commit and not --commit contains '..' }}
### **Commit Chi Tiết**
- **Hash**: `commit_hash`
- **Message**: `commit_message`
- **Author**: `author_name` <author@email>
- **Date**: `commit_date`
- **Files changed**: [count] files
{{ endif }}

{{ if --commit and --commit contains '..' }}
### **Commit Range: $COMMIT**
- **Total commits**: [count]
- **Date range**: [start_date] to [end_date]
- **Contributors**: [list of authors]
{{ endif }}
{{ endif }}

---

## 📋 So Sánh Với Plan (nếu có)
*(Khi sử dụng --plan flag)*

### **Tiến Độ Hoàn Thành**
- **Tasks đã hoàn thành**: [số lượng]/[tổng số] ✅
- **Tasks đang thực hiện**: [số lượng]/[tổng số] ⏳
- **Tasks chưa bắt đầu**: [số lượng]/[tổng số] ❌
- **Completion rate**: [X]%
- **Công việc thừa**: [số lượng] items ➕

### **Phân Tích Chi Tiết**
{{ for each task in plan_tasks }}
- **[task_name]**:
  - Status: [✅ hoàn thành | ⏳ đang làm | ❌ chưa làm]
  - Evidence: [files/thay đổi chứng minh]
  - Notes: [ghi chú bổ sung]
{{ endfor }}

### **Phân Tích Deviation**
- **Thừa**: [các thay đổi không có trong plan]
  - Impact: [đánh giá tác động]
- **Thiếu**: [các tasks trong plan chưa implement]
  - Priority: [mức độ ưu tiên]
- **Khác biệt**: [phân tích sự khác biệt so với plan]

---

## 🟢 Thay Đổi Đã Thực Hiện
{{ if not --recent and not --commit }}
### **Thay Đổi Đã Staged (Sẵn Sàng Commit)**
*(Các thay đổi đã được thêm vào index)*
{{ endif }}

{{ if --recent or --commit }}
### **Các File Đã Thay Đổi**
{{ endif }}

{{ for each file in changed_files }}
#### **[file_path]**
- **Thay đổi**: [Mô tả ngắn gọn về thay đổi]
- **Loại thay đổi**: [feature|fix|refactor|docs|test|chore]
- **Tác động**: [Tại sao thay đổi này quan trọng]
{{ if not --recent and not --commit }}
- **Trạng thái**: [staged|unstaged|untracked]
{{ endif }}
{{ if lines_added or lines_removed }}
- **Lines**: +lines_added/-lines_removed
{{ endif }}
{{ endfor }}

---

## 📊 Thống Kê
{{ if --recent or --commit }}
- **Commit range**: [commit_count] commits
{{ endif }}
- **Total files changed**: [số lượng]
- **Lines added**: [số lượng]
- **Lines removed**: [số lượng]
{{ if file_categories }}
- **Phân loại thay đổi**:
  - Features: [count]
  - Fixes: [count]
  - Refactoring: [count]
  - Documentation: [count]
  - Tests: [count]
  - Configuration: [count]
{{ endif }}
- **Complexity score**: [low/medium/high]

{{ if --plan }}
- **Plan completion**: [X]%
- **Tasks completed**: [completed]/[total]
{{ endif }}

---

## 🔍 Phân Tích Sâu
*(Nếu liên quan, khám phá các thay đổi phức tạp cụ thể)*

{{ for complex_change in complex_changes }}
- **Thay đổi Logic trong `[Component]`**:
  - Giải thích sự thay đổi logic
  - Code trước/sau nếu hữu ích
  - Tác động đến system

{{ endfor }}

- **Phân Tích Pattern**:
  - Các pattern được áp dụng: [từ pattern-analysis]
  - Tính nhất quán với codebase: [đánh giá]
  - Best practices được tuân thủ/vi phạm

---

## ⚠️ Quan Sát & Gợi Ý
{{ for observation in observations }}
- **[Quan sát]**: [nội dung quan sát]
  - Severity: [high|medium|low]
  - Action: [hành động đề xuất]
{{ endfor }}

- **[Gợi ý]**: [recommendations]
- **[Dọn dẹp]**: [cleanup items]
- **[Security]**: [security concerns]
- **[Performance]**: [performance considerations]

---

## 🔄 Hành Động Đề Xuất
1. [Hành động cụ thể 1 với priority]
2. [Hành động cụ thể 2 với priority]
3. [Hành động cụ thể 3 với priority]

{{ if --plan and completion_rate < 100 }}
## 🎯 Next Steps cho Plan
- Tasks cần hoàn thành: [list]
- Estimated effort: [time estimate]
- Dependencies: [list]
{{ endif }}
```

---

## Integration with Subagents & Skills

### Agent Collaboration

1. **git-manager**:
   - Thực hiện các git commands
   - Cung cấp raw diff data
   - Đánh giá clean history practices

2. **researcher**:
   - Phân tích patterns trong code
   - Tìm các best practices liên quan
   - Đánh giá architectural consistency

3. **docs-manager**:
   - Tạo báo cáo có cấu trúc
   - Đảm bảo clarity và actionability
   - Lưu artifacts nếu cần

### Skill Application

1. **pattern-analysis**:
   - Nhận diện structural patterns
   - So sánh với existing codebase
   - Đề xuất improvements

2. **sequential-thinking**:
   - Phân tích logical flow
   - Đánh giá risk factors
   - Document reasoning chain

---

## Output Integration

This command provides an immediate report in the chat and saves by default to `.claude/artifacts/recent-changes-[timestamp].md`.

### Flags

| Flag | Description | Example |
|------|-------------|---------|
| `--plan=[path]` | Compare changes with plan file | `/how-recent-changes --plan=plans/feature-x.md` |
| `--recent=N` | Analyze last N commits | `/how-recent-changes --recent=5` |
| `--commit=ID` | Analyze specific commit | `/how-recent-changes --commit=abc123` |
| `--commit=RANGE` | Analyze commit range | `/how-recent-changes --commit=abc123..def456` |
| `--deep` | Deep analysis with pattern recognition | `/how-recent-changes --deep` |
| `--files=[paths]` | Focus on specific files/directories | `/how-recent-changes --files=src/components,src/utils` |
| `--no-save` | Skip saving to file | `/how-recent-changes --no-save` |
| `--format=[json|markdown]` | Output format | `/how-recent-changes --format=json` |

---

## Best Practices

1. **Run before commits**: Always check before committing to catch issues early
2. **Use with --deep**: For complex changes or before PRs
3. **Save important analyses**: For documentation or team sharing
4. **Address flagged issues**: Pay attention to risk assessments and cleanup suggestions

---

## Related Commands

- [`/status`](.claude/commands/status.md) - Quick project status
- [`/commit`](.claude/commands/commit.md) - Create commits with analysis
- [`/review`](.claude/commands/review.md) - Code review with subagents
