#!/usr/bin/env python3
"""
Clean Curly Quotes Script

Automatically replaces curly quotes with straight quotes in Markdown files.
Supports dry-run, backup, and restore functionality.

Usage:
    python3 glean/99_Tools/scripts/clean_quotes.py --file "glean/10_Sources/Articles/file.md"
    python3 glean/99_Tools/scripts/clean_quotes.py --folder "glean/10_Sources/Articles"
    python3 glean/99_Tools/scripts/clean_quotes.py --file "glean/10_Sources/Articles/file.md" --no-dry-run
"""

import os
import sys
import argparse
import json
import shutil
from datetime import datetime
from pathlib import Path

# Quote mappings
QUOTE_REPLACEMENTS = {
    # Single quotes
    "\u2018": "'",  # Left single quotation mark
    "\u2019": "'",  # Right single quotation mark
    "\u201A": "'",  # Single low-9 quotation mark
    "\u201B": "'",  # Single high-reversed-9 quotation mark
    
    # Double quotes
    "\u201C": '"',  # Left double quotation mark
    "\u201D": '"',  # Right double quotation mark
    "\u201E": '"',  # Double low-9 quotation mark
    "\u201F": '"',  # Double high-reversed-9 quotation mark
}

class QuoteCleaner:
    def __init__(self, vault_root):
        self.vault_root = Path(vault_root).resolve()
        self.backup_dir = self.vault_root / "99_Tools" / "backups"
        self.inventory_file = self.backup_dir / "inventory.json"
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        
    def clean_quotes(self, text):
        """Replace all curly quotes with straight quotes"""
        cleaned = text
        for curly, straight in QUOTE_REPLACEMENTS.items():
            cleaned = cleaned.replace(curly, straight)
        return cleaned
    
    def count_replacements(self, original, cleaned):
        """Count how many quotes were replaced"""
        count = 0
        for curly in QUOTE_REPLACEMENTS.keys():
            count += original.count(curly)
        return count
    
    def create_backup(self, file_path, original_content, changes_count=0):
        """Create a backup of the file before modification"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_id = abs(hash(str(file_path))) % 1000000
        backup_id = f"{timestamp}_{file_id:06x}"
        
        backup_file = self.backup_dir / f"{backup_id}_{file_path.name}"
        backup_file.write_text(original_content, encoding='utf-8')
        
        # Update inventory
        inventory = self.load_inventory()
        # relative_path = str(file_path.relative_to(self.vault_root)) if file_path.is_relative_to(self.vault_root) else str(file_path)
        
        inventory.append({
            "id": backup_id,
            "timestamp": timestamp,
            "original_path": str(file_path),
            "backup_path": str(backup_file),
            "changes_count": changes_count,
            "tool": "clean_quotes"
        })
        
        self.save_inventory(inventory)
        return backup_id
    
    def load_inventory(self):
        """Load backup inventory"""
        if self.inventory_file.exists():
            try:
                data = json.loads(self.inventory_file.read_text(encoding='utf-8'))
                if isinstance(data, list):
                    return data
                return []
            except Exception:
                return []
        return []
    
    def save_inventory(self, inventory):
        """Save backup inventory"""
        self.inventory_file.write_text(
            json.dumps(inventory, indent=2, ensure_ascii=False),
            encoding='utf-8'
        )
    
    def process_file(self, file_path, dry_run=True):
        """Process a single file"""
        file_path = Path(file_path).resolve()
        
        if not file_path.exists():
            print(f"❌ File not found: {file_path}")
            return False
        
        if not file_path.suffix == '.md':
            print(f"⏭️  Skipping non-markdown file: {file_path}")
            return False
        
        try:
            original_content = file_path.read_text(encoding='utf-8')
            cleaned_content = self.clean_quotes(original_content)
            
            replacements = self.count_replacements(original_content, cleaned_content)
            
            if replacements == 0:
                print(f"✓ No curly quotes found: {file_path.name}")
                return True
            
            if dry_run:
                print(f"\n📝 {file_path.name}")
                print(f"   Found {replacements} curly quote(s) to replace")
                print(f"   (Dry run - no changes made)")
            else:
                # Create backup
                backup_id = self.create_backup(file_path, original_content, replacements)
                
                # Write cleaned content
                file_path.write_text(cleaned_content, encoding='utf-8')
                
                print(f"\n✅ {file_path.name}")
                print(f"   Replaced {replacements} curly quote(s)")
                print(f"   Backup ID: {backup_id}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error processing {file_path}: {e}")
            return False
    
    def process_folder(self, folder_path, dry_run=True):
        """Process all markdown files in a folder recursively"""
        folder_path = Path(folder_path).resolve()
        
        if not folder_path.exists():
            print(f"❌ Folder not found: {folder_path}")
            return
        
        md_files = list(folder_path.rglob("*.md"))
        
        if not md_files:
            print(f"No markdown files found in {folder_path}")
            return
        
        print(f"\n🔍 Found {len(md_files)} markdown file(s)")
        print(f"{'=' * 60}")
        
        success_count = 0
        for md_file in md_files:
            if self.process_file(md_file, dry_run):
                success_count += 1
        
        print(f"\n{'=' * 60}")
        print(f"✓ Processed {success_count}/{len(md_files)} files")
        
        if dry_run:
            print("\n💡 Use --no-dry-run to apply changes")
    
    def list_backups(self, filter_path=None):
        """List all backups"""
        inventory = self.load_inventory()
        
        if not inventory:
            print("No backups found")
            return
        
        print("\nBackup History:")
        print(f"{'ID':<25} | {'Date':<20} | {'File':<40}")
        print("-" * 90)
        
        for item in sorted(inventory, key=lambda x: x['timestamp'], reverse=True):
            if filter_path and filter_path not in item['original_path']:
                continue
            
            timestamp = datetime.strptime(item['timestamp'], "%Y%m%d_%H%M%S")
            date_str = timestamp.strftime("%Y-%m-%d %H:%M:%S")
            file_name = Path(item['original_path']).name
            
            print(f"{item['id']:<25} | {date_str:<20} | {file_name:<40}")
    
    def restore_backup(self, backup_id):
        """Restore a file from backup"""
        inventory = self.load_inventory()
        
        if not inventory:
            print("No backups found")
            return False

        info = next((item for item in inventory if item['id'] == backup_id), None)
        
        if not info:
            print(f"❌ Backup ID not found: {backup_id}")
            return False
            
        backup_file = Path(info['backup_path'])
        original_file = Path(info['original_path'])
        
        if not backup_file.exists():
            print(f"❌ Backup file not found: {backup_file}")
            return False
        
        try:
            backup_content = backup_file.read_text(encoding='utf-8')
            original_file.write_text(backup_content, encoding='utf-8')
            
            print(f"✅ Restored: {info['original_path']}")
            print(f"   From backup: {backup_id}")
            return True
            
        except Exception as e:
            print(f"❌ Error restoring backup: {e}")
            return False

    def resolve_path(self, path_str, is_folder=False):
        """
        Resolve a path string to a Path object.
        1. Check if it exists as is (relative to CWD or absolute)
        2. Check if it exists relative to vault root
        3. If it's a file, search for it by name in the vault
        """
        # 1. Check relative to CWD or absolute
        path = Path(path_str).resolve()
        if path.exists():
            return path
            
        # 2. Check relative to vault root
        vault_path = (self.vault_root / path_str).resolve()
        if vault_path.exists():
            return vault_path
            
        # 3. If it's a file name, search in vault
        if not is_folder:
            print(f"🔍 Searching for '{path_str}' in vault...")
            matches = list(self.vault_root.rglob(path_str))
            
            if len(matches) == 1:
                print(f"   Found: {matches[0].relative_to(self.vault_root)}")
                return matches[0]
            elif len(matches) > 1:
                print(f"❌ Ambiguous file name. Found {len(matches)} matches:")
                for m in matches[:5]:
                    print(f"   - {m.relative_to(self.vault_root)}")
                if len(matches) > 5:
                    print("   ...")
                return None
        
        print(f"❌ Path not found: {path_str}")
        return None

def find_vault_root():
    """Find vault root by looking for .obsidian folder"""
    current = Path.cwd()
    
    # First check if we are in the repo root (above glean)
    if (current / "glean" / ".obsidian").exists():
        return current / "glean"
    
    while current != current.parent:
        if (current / ".obsidian").exists():
            return current
        current = current.parent
    
    return Path.cwd()

def main():
    parser = argparse.ArgumentParser(
        description="Clean curly quotes in Markdown files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Dry run (default - preview changes)
  python3 clean_quotes.py --file "article.md"
  
  # Apply changes
  python3 clean_quotes.py --file "article.md" --no-dry-run
  
  # Process entire folder
  python3 clean_quotes.py --folder "10_Sources/Articles" --no-dry-run
  
  # List backups
  python3 clean_quotes.py --list-backups
  
  # Restore from backup
  python3 clean_quotes.py --restore 20251220_120000_abc123
        """
    )
    
    parser.add_argument('--file', help='Process a single file')
    parser.add_argument('--folder', help='Process all .md files in folder')
    parser.add_argument('--dry-run', action='store_true', default=True,
                       help='Preview changes without modifying files (default)')
    parser.add_argument('--no-dry-run', action='store_true',
                       help='Apply changes to files')
    parser.add_argument('--list-backups', nargs='?', const='', metavar='PATH',
                       help='List available backups, optionally filter by path')
    parser.add_argument('--restore', metavar='ID',
                       help='Restore a backup by ID')
    
    args = parser.parse_args()
    
    # Determine dry run mode
    dry_run = not args.no_dry_run
    
    # Find vault root
    vault_root = find_vault_root()
    print(f"Vault root: {vault_root}\n")
    
    cleaner = QuoteCleaner(vault_root)
    
    # Handle commands
    if args.restore:
        cleaner.restore_backup(args.restore)
    elif args.list_backups is not None:
        cleaner.list_backups(args.list_backups if args.list_backups else None)
    elif args.file:
        file_path = cleaner.resolve_path(args.file, is_folder=False)
        if file_path:
            cleaner.process_file(file_path, dry_run)
    elif args.folder:
        folder_path = cleaner.resolve_path(args.folder, is_folder=True)
        if folder_path:
            cleaner.process_folder(folder_path, dry_run)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()