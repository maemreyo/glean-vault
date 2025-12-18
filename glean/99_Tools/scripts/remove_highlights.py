import os
import re
import argparse
import sys

# Configuration
VAULT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
ARTICLES_DIR = os.path.join(VAULT_ROOT, "10_Sources/Articles")

def process_file(filepath, dry_run=True):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Regex to find <mark ...>text</mark>
    # <mark[^>]*> matches opening tag with any attributes
    # (.*?) matches inner content (non-greedy)
    # </mark> matches closing tag
    # flags=re.DOTALL allows matching across newlines if needed, though usually highlights are inline.
    # Let's assume inline for now, but DOTALL is safer if user highlighted a block.
    regex = re.compile(r"<mark[^>]*>(.*?)</mark>", re.IGNORECASE | re.DOTALL)

    changes_made = []

    def replace_func(match):
        inner_text = match.group(1)
        original_match = match.group(0)
        
        # Don't strip if inner text is empty? Or just strip it?
        # <mark></mark> -> "" (empty string) is fine.
        
        changes_made.append(f"Removed highlight from: '{inner_text.strip()}'")
        return inner_text

    new_content = regex.sub(replace_func, content)
    
    if new_content != content:
        if dry_run:
            print(f"[DRY RUN] Would modify: {os.path.basename(filepath)}")
            print(f"  - Found {len(changes_made)} highlights to remove:")
            for change in changes_made[:20]:
                print(f"    - {change}")
            if len(changes_made) > 20:
                print(f"    - ... and {len(changes_made) - 20} more.")
        else:
            print(f"Updating: {os.path.basename(filepath)}")
            print(f"  - Removed {len(changes_made)} highlights.")
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)

def main():
    parser = argparse.ArgumentParser(description="Remove Highlightr <mark> tags from Markdown files.")
    parser.add_argument("--file", help="Process a single specific file (relative or absolute path)")
    parser.add_argument("--folder", help="Process all files in a specific folder (relative or absolute path)")
    parser.add_argument("--dry-run", action="store_true", help="Print changes without modifying files")
    parser.add_argument("--no-dry-run", action="store_false", dest="dry_run", help="Actually modify files")
    parser.set_defaults(dry_run=True)
    
    args = parser.parse_args()
    
    target_files = []

    if args.file:
        target_file = os.path.abspath(args.file)
        if not os.path.exists(target_file):
             potential_path = os.path.join(VAULT_ROOT, args.file)
             if os.path.exists(potential_path):
                 target_file = potential_path
        
        if os.path.exists(target_file):
             target_files.append(target_file)
        else:
            print(f"Error: File not found: {args.file}")
            return
            
    elif args.folder:
        target_folder = os.path.abspath(args.folder)
        if not os.path.exists(target_folder):
             potential_path = os.path.join(VAULT_ROOT, args.folder)
             if os.path.exists(potential_path):
                 target_folder = potential_path
        
        if not os.path.exists(target_folder):
            print(f"Error: Folder not found: {args.folder}")
            return
            
        print(f"Scanning folder: {target_folder}")
        for root, dirs, files in os.walk(target_folder):
            for file in files:
                if file.endswith(".md"):
                    target_files.append(os.path.join(root, file))
    
    else:
        print("Please specify a file or folder using --file or --folder.")
        return

    print(f"Processing {len(target_files)} files...")
    count = 0
    for filepath in target_files:
        process_file(filepath, dry_run=args.dry_run)
        count += 1
                
    print(f"Processed {count} files.")
    if args.dry_run:
        print("Run with --no-dry-run to apply changes.")

if __name__ == "__main__":
    main()
