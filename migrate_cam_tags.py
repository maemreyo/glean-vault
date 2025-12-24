import os
import re
import argparse

def migrate_tags(vault_path, dry_run=True):
    # Pattern to match #flashcards/cam- but not #flashcards/cambridge/cam-
    # We use a negative lookahead to avoid double-prefixing if already renamed
    pattern = re.compile(r'#flashcards/(?!cambridge/)cam-')
    replacement = '#flashcards/cambridge/cam-'
    
    modified_count = 0
    total_files = 0
    
    # Directories to skip
    skip_dirs = {'.git', '.obsidian', '.trash', '99_Tools/backups', '.gemini'}
    
    for root, dirs, files in os.walk(vault_path):
        # Prune skip_dirs
        dirs[:] = [d for d in dirs if d not in skip_dirs]
        
        for file in files:
            if not file.endswith('.md'):
                continue
                
            total_files += 1
            file_path = os.path.join(root, file)
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                if pattern.search(content):
                    new_content = pattern.sub(replacement, content)
                    modified_count += 1
                    
                    if not dry_run:
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        print(f"✅ Updated: {os.path.relpath(file_path, vault_path)}")
                    else:
                        print(f"🔍 [DRY RUN] Would update: {os.path.relpath(file_path, vault_path)}")
            except Exception as e:
                print(f"❌ Error processing {file_path}: {e}")
                
    return modified_count, total_files

def main():
    parser = argparse.ArgumentParser(description="Rename #flashcards/cam- to #flashcards/cambridge/cam-")
    parser.add_argument('--vault', default='.', help="Path to the vault root")
    parser.add_argument('--no-dry-run', action='store_true', help="Apply changes permanently")
    
    args = parser.parse_args()
    vault_path = os.path.abspath(args.vault)
    
    print(f"Starting migration in: {vault_path}")
    print(f"Dry run: {not args.no_dry_run}")
    print("-" * 40)
    
    modified, total = migrate_tags(vault_path, dry_run=not args.no_dry_run)
    
    print("-" * 40)
    print(f"Summary:")
    print(f"Total .md files checked: {total}")
    print(f"Files {'to be ' if not args.no_dry_run else ''}modified: {modified}")
    
    if not args.no_dry_run:
        print("\nMigration complete.")
    else:
        print("\nRun with --no-dry-run to apply changes.")

if __name__ == "__main__":
    main()
