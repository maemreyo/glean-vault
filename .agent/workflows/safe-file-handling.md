---
description: Best practices for handling files with spaces and special characters
---

# Safe File Handling Guide

> **Problem:** Files with spaces, apostrophes, parentheses, and other special characters often cause errors when processing in shell commands, Python scripts, and AI instructions.

## 🎯 Quick Reference

| Context | Solution | Example |
|---------|----------|---------|
| **Shell/Terminal** | Use single quotes `'...'` | `cat '/path/to/file with spaces.md'` |
| **Python** | Use `pathlib.Path` or regular strings | `Path("file with spaces.md")` |
| **AI Instructions** | Use backticks and full paths | `` `/full/path/to/file.md` `` |

---

## 1️⃣ Shell Commands (Terminal)

### ✅ Best Practices

```bash
# ALWAYS use single quotes for filenames
cat '/Users/trung.ngo/Documents/glean/30_Structures/put st somewhere safe.md'

# ALWAYS use single quotes in loops
for file in '/path/to/folder'/*.md; do
    echo "Processing: $file"
    cat "$file"  # Inside variables, use double quotes
done

# For commands with multiple files
cp '/source/file with spaces.md' '/destination/another file.md'
```

### ❌ Common Mistakes

```bash
# DON'T use unquoted paths
cat /path/to/file with spaces.md  # ❌ Will fail

# DON'T use backslash escaping (hard to read)
cat /path/to/file\ with\ spaces.md  # ❌ Works but ugly

# DON'T use double quotes with special chars like apostrophes
cat "/path/to/file's name.md"  # ❌ May fail depending on shell
```

### 🔧 Advanced: When Working with Variables

```bash
# Store path in variable with quotes
FILE_PATH="/path/to/file with spaces.md"

# Use variable with double quotes
cat "$FILE_PATH"  # ✅ Good

# Array of files (for batch processing)
FILES=(
    "/path/to/first file.md"
    "/path/to/second's file.md"
    "/path/to/third (copy).md"
)

for file in "${FILES[@]}"; do
    cat "$file"
done
```

---

## 2️⃣ Python Scripts

### ✅ Best Practices

```python
from pathlib import Path
import os

# METHOD 1: pathlib (RECOMMENDED)
file_path = Path("glean/30_Structures/put st somewhere safe.md")

# Read file
content = file_path.read_text(encoding='utf-8')

# Write file
file_path.write_text(content, encoding='utf-8')

# Check if exists
if file_path.exists():
    print(f"Found: {file_path}")

# Iterate over files in directory
folder = Path("glean/30_Structures")
for file in folder.glob("*.md"):
    print(f"Processing: {file.name}")
    content = file.read_text(encoding='utf-8')
```

```python
# METHOD 2: os.path (Traditional)
import os

file_path = "glean/30_Structures/put st somewhere safe.md"

# Read file
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Write file
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

# Check if exists
if os.path.exists(file_path):
    print(f"Found: {file_path}")
```

### 🔧 Advanced: Safe File Operations

```python
from pathlib import Path
import shutil

def safe_file_operation(file_path: str | Path) -> None:
    """Safely handle any filename"""
    path = Path(file_path)
    
    # Validate path
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    
    # Get safe filename for display
    safe_name = path.name
    print(f"Processing: {safe_name}")
    
    # Read with error handling
    try:
        content = path.read_text(encoding='utf-8')
    except UnicodeDecodeError:
        # Fallback for non-UTF8 files
        content = path.read_text(encoding='latin-1')
    
    return content

# Example: Process all markdown files recursively
def process_all_markdown(root_dir: str | Path) -> None:
    """Process all .md files, regardless of filename"""
    root = Path(root_dir)
    
    for md_file in root.rglob("*.md"):
        # pathlib handles special chars automatically
        content = md_file.read_text(encoding='utf-8')
        print(f"✓ Processed: {md_file.relative_to(root)}")

# Usage
process_all_markdown("glean/30_Structures")
```

### 🚫 What NOT to Do

```python
# DON'T manually escape paths (Python handles it)
file_path = "glean/30_Structures/put\\ st\\ somewhere\\ safe.md"  # ❌

# DON'T use shell=True with subprocess
import subprocess
subprocess.run(f"cat {file_path}", shell=True)  # ❌ DANGEROUS

# DO use list arguments instead
subprocess.run(["cat", file_path])  # ✅ Safe
```

---

## 3️⃣ AI Instructions (Claude Code)

### ✅ Best Practices

When giving instructions to Claude, be **explicit and formatted**:

```markdown
# OPTION 1: Use backticks for inline paths
Please read the file `/Users/trung.ngo/Documents/glean/30_Structures/put st somewhere safe.md`

# OPTION 2: Use code blocks for multiple files
Process these files:
```
/path/to/file with spaces.md
/path/to/another's file.md
/path/to/file (with parentheses).md
```

# OPTION 3: Use markdown lists
Please process:
- `/path/to/file with spaces.md`
- `/path/to/another's file.md`
- `/path/to/third [version].md`
```

### 🎯 Writing Claude Code Skills/Agents

```markdown
# In .claude/skills/*.md or .claude/agents/*.md

## Example Instructions

When referencing files in instructions:

```markdown
1. Read all markdown files in the folder:
   `/Users/trung.ngo/Documents/glean-vault/glean/30_Structures/`

2. For each file, process content using Python's pathlib:
   ```python
   from pathlib import Path
   
   folder = Path("glean/30_Structures")
   for file in folder.glob("*.md"):
       # pathlib automatically handles special chars
       content = file.read_text(encoding='utf-8')
   ```

3. When running shell commands, ALWAYS use single quotes:
   ```bash
   cat '/path/to/file with spaces.md'
   ```
```

### 📋 Template for File Processing Instructions

```markdown
**Task:** Process all markdown files in [FOLDER]

**Safe Handling Requirements:**
1. ✅ Use `pathlib.Path` for Python operations
2. ✅ Use single quotes `'...'` for shell commands
3. ✅ Use full absolute paths when possible
4. ✅ Handle Unicode characters (UTF-8 encoding)
5. ✅ Log each file processed with its exact name

**Example Code:**
```python
from pathlib import Path

folder = Path("[ABSOLUTE_PATH]")
for file in folder.glob("*.md"):
    try:
        content = file.read_text(encoding='utf-8')
        print(f"✓ Processed: {file.name}")
    except Exception as e:
        print(f"✗ Failed: {file.name} - {e}")
```
```

---

## 4️⃣ Common Problematic Characters

| Character | Problem | Solution |
|-----------|---------|----------|
| Space ` ` | Breaks unquoted paths | Use quotes: `'file name.md'` |
| Apostrophe `'` | Conflicts with single quotes | Use double quotes or escape: `"file's name.md"` |
| Parentheses `()` | Shell metacharacters | Use quotes: `'file (copy).md'` |
| Brackets `[]` | Glob patterns | Use quotes: `'file [v2].md'` |
| Ampersand `&` | Background process | Use quotes: `'file & stuff.md'` |
| Dollar `$` | Variable expansion | Use single quotes: `'file $100.md'` |
| Asterisk `*` | Wildcard | Use quotes: `'file * notes.md'` |

### 🧪 Test Files

Here are example filenames to test your code:

```
put st somewhere safe.md
I don't think so either.md
as far as I'm concerned ___.md
file (copy).md
file [version 2].md
file & notes.md
file $100 budget.md
file * important.md
```

---

## 5️⃣ Debugging Tips

### When Things Go Wrong

```python
from pathlib import Path

def debug_file_path(file_path: str | Path) -> None:
    """Debug helper for file path issues"""
    path = Path(file_path)
    
    print(f"Original input: {file_path}")
    print(f"Path object: {path}")
    print(f"Absolute path: {path.absolute()}")
    print(f"Exists: {path.exists()}")
    print(f"Is file: {path.is_file()}")
    print(f"Parent dir: {path.parent}")
    print(f"Filename: {path.name}")
    print(f"Stem: {path.stem}")
    print(f"Suffix: {path.suffix}")

# Usage
debug_file_path("glean/30_Structures/put st somewhere safe.md")
```

### Shell Command Debugging

```bash
# Test if file exists before processing
FILE="/path/to/file with spaces.md"

if [ -f "$FILE" ]; then
    echo "✓ File exists: $FILE"
    cat "$FILE"
else
    echo "✗ File not found: $FILE"
    # List similar files
    ls -la "$(dirname "$FILE")"
fi
```

---

## 6️⃣ Quick Checklist

Before processing files, verify:

- [ ] **Python:** Using `pathlib.Path` or quoted strings
- [ ] **Shell:** All paths wrapped in single quotes `'...'`
- [ ] **Encoding:** UTF-8 specified for read/write
- [ ] **Error Handling:** Try-except blocks for file operations
- [ ] **Logging:** Print which file is being processed
- [ ] **Testing:** Tested with actual problematic filenames
- [ ] **Variables:** Shell variables wrapped in double quotes `"$VAR"`

---

## 7️⃣ Real-World Example: Batch Processing

```python
#!/usr/bin/env python3
"""
Safe batch processor for markdown files with special characters
"""
from pathlib import Path
from typing import List
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s'
)

def process_markdown_folder(
    folder_path: str | Path,
    pattern: str = "*.md"
) -> List[Path]:
    """
    Safely process all markdown files in a folder
    
    Args:
        folder_path: Path to folder (can have spaces/special chars)
        pattern: Glob pattern for files to process
    
    Returns:
        List of successfully processed files
    """
    folder = Path(folder_path)
    
    if not folder.exists():
        raise FileNotFoundError(f"Folder not found: {folder}")
    
    if not folder.is_dir():
        raise NotADirectoryError(f"Not a directory: {folder}")
    
    processed_files = []
    failed_files = []
    
    # Get all matching files
    files = list(folder.glob(pattern))
    logging.info(f"Found {len(files)} files matching '{pattern}'")
    
    for file_path in files:
        try:
            # Read file content
            content = file_path.read_text(encoding='utf-8')
            
            # Process content here
            # ... your processing logic ...
            
            logging.info(f"✓ Processed: {file_path.name}")
            processed_files.append(file_path)
            
        except UnicodeDecodeError as e:
            logging.error(f"✗ Encoding error in {file_path.name}: {e}")
            failed_files.append(file_path)
            
        except Exception as e:
            logging.error(f"✗ Failed to process {file_path.name}: {e}")
            failed_files.append(file_path)
    
    # Summary
    logging.info(f"\n{'='*60}")
    logging.info(f"Processed: {len(processed_files)} files")
    logging.info(f"Failed: {len(failed_files)} files")
    
    if failed_files:
        logging.warning("Failed files:")
        for f in failed_files:
            logging.warning(f"  - {f.name}")
    
    return processed_files

# Usage example
if __name__ == "__main__":
    folder = "/Users/trung.ngo/Documents/zaob-dev/glean-vault/glean/30_Structures"
    process_markdown_folder(folder)
```

---

## 🎓 Summary

**Golden Rules:**

1. **Shell Commands:** Always use single quotes `'path/to/file.md'`
2. **Python:** Always use `pathlib.Path` (modern) or regular strings (traditional)
3. **AI Instructions:** Always use backticks or code blocks with full paths
4. **Never:** Manually escape paths or use shell=True in subprocess
5. **Always:** Test with real filenames containing spaces and special characters

**Remember:** Modern Python and proper quoting handle 99% of special character issues automatically. Don't overthink it! 🚀

---

## 📚 Additional Resources

- [Python pathlib documentation](https://docs.python.org/3/library/pathlib.html)
- [Bash quoting guide](https://www.gnu.org/software/bash/manual/html_node/Quoting.html)
- [Unicode in Python](https://docs.python.org/3/howto/unicode.html)
