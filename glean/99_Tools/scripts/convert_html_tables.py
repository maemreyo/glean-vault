import os
import re
import argparse
from pathlib import Path
from html.parser import HTMLParser

class TableParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.rows = []
        self.current_row = []
        self.current_cell = []
        self.in_table = False
        self.in_row = False
        self.in_cell = False
        self.cell_tag = None
        
    def handle_starttag(self, tag, attrs):
        if tag == 'table':
            self.in_table = True
            self.rows = []
        elif tag == 'tr' and self.in_table:
            self.in_row = True
            self.current_row = []
        elif tag in ['td', 'th'] and self.in_row:
            self.in_cell = True
            self.cell_tag = tag
            self.current_cell = []
            
    def handle_endtag(self, tag):
        if tag == 'table':
            self.in_table = False
        elif tag == 'tr' and self.in_row:
            self.in_row = False
            if self.current_row:
                self.rows.append(self.current_row)
        elif tag in ['td', 'th'] and self.in_cell:
            self.in_cell = False
            cell_text = ''.join(self.current_cell).strip()
            self.current_row.append({
                'text': cell_text,
                'is_header': self.cell_tag == 'th'
            })
            
    def handle_data(self, data):
        if self.in_cell:
            self.current_cell.append(data)

def html_table_to_markdown(html_table):
    """Convert HTML table to Markdown table format."""
    parser = TableParser()
    parser.feed(html_table)
    
    if not parser.rows:
        return html_table  # Return original if parsing failed
    
    # Build markdown table
    md_lines = []
    
    for i, row in enumerate(parser.rows):
        # Extract cell texts
        cells = [cell['text'] for cell in row]
        
        # Create table row
        md_line = '| ' + ' | '.join(cells) + ' |'
        md_lines.append(md_line)
        
        # Add separator after header row
        if i == 0:
            # Check if first row is header
            is_header_row = any(cell['is_header'] for cell in row)
            if is_header_row or i == 0:
                separator = '| ' + ' | '.join(['---'] * len(cells)) + ' |'
                md_lines.append(separator)
    
    return '\n'.join(md_lines)

def process_file(filepath, dry_run=False):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return False

    # Find all HTML tables (multiline)
    # Using DOTALL to match across newlines
    pattern = re.compile(r'<table>.*?</table>', re.DOTALL | re.IGNORECASE)
    
    matches = list(pattern.finditer(content))
    
    if not matches:
        return False
    
    # Replace each table
    new_content = content
    for match in reversed(matches):  # Reverse to maintain indices
        html_table = match.group(0)
        md_table = html_table_to_markdown(html_table)
        new_content = new_content[:match.start()] + md_table + new_content[match.end():]
    
    if content == new_content:
        return False
    
    if dry_run:
        print(f"[DRY RUN] Would convert {len(matches)} HTML table(s) in: {os.path.basename(filepath)}")
        return True
    else:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Converted {len(matches)} HTML table(s) in: {os.path.basename(filepath)}")
        return True

def main():
    parser = argparse.ArgumentParser(description="Convert HTML tables to Markdown tables.")
    parser.add_argument('--folder', help="Folder to scan")
    parser.add_argument('--file', help="Single file to process")
    parser.add_argument('--dry-run', action='store_true', help="Don't save changes")

    args = parser.parse_args()

    count = 0
    
    if args.file:
        if process_file(args.file, args.dry_run):
            count += 1
    elif args.folder:
        folder = Path(args.folder)
        if not folder.exists():
            print(f"Folder not found: {folder}")
            return

        print("Scanning files...")
        for file_path in folder.rglob('*.md'):
            if process_file(str(file_path), args.dry_run):
                count += 1
    else:
        print("Please provide --folder or --file")
        return

    print(f"\nTotal files updated: {count}")

if __name__ == "__main__":
    main()
