import os
import re
import argparse
import sys
import shutil
import json
import datetime
import hashlib

# Configuration
VAULT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
VOCAB_DIR = os.path.join(VAULT_ROOT, "20_Vocabulary")
STRUCT_DIR = os.path.join(VAULT_ROOT, "30_Structures")
ARTICLES_DIR = os.path.join(VAULT_ROOT, "10_Sources/Articles")
BACKUP_DIR = os.path.join(VAULT_ROOT, "99_Tools/backups")
INVENTORY_FILE = os.path.join(BACKUP_DIR, "inventory.json")

def ensure_backup_dir():
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)
    if not os.path.exists(INVENTORY_FILE):
        with open(INVENTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f)

def load_inventory():
    ensure_backup_dir()
    try:
        with open(INVENTORY_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def save_inventory(inventory):
    ensure_backup_dir()
    with open(INVENTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(inventory, f, indent=2)

def create_backup(filepath, changes_summary):
    ensure_backup_dir()
    
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    file_hash = hashlib.md5(filepath.encode()).hexdigest()[:6]
    backup_filename = f"{timestamp}_{file_hash}_{os.path.basename(filepath)}"
    backup_path = os.path.join(BACKUP_DIR, backup_filename)
    
    # Copy original file to backup
    shutil.copy2(filepath, backup_path)
    
    backup_entry = {
        "id": f"{timestamp}_{file_hash}",
        "timestamp": timestamp,
        "original_path": os.path.abspath(filepath),
        "backup_path": backup_path,
        "changes_count": len(changes_summary),
        "changes_sample": changes_summary[:5]  # Store first 5 changes as sample
    }
    
    inventory = load_inventory()
    inventory.insert(0, backup_entry) # Prepend to show latest first
    save_inventory(inventory)
    
    return backup_entry["id"]

def list_backups(file_filter=None):
    inventory = load_inventory()
    if not inventory:
        print("No backups found.")
        return

    print(f"{'ID':<25} | {'Date':<20} | {'File':<40} | {'Changes'}")
    print("-" * 100)
    
    count = 0
    for entry in inventory:
        # If filter is applied, only show backups for that file
        if file_filter:
            abs_filter = os.path.abspath(file_filter)
            if entry.get('original_path') != abs_filter:
                continue
                
        fname = os.path.basename(entry.get('original_path', 'unknown'))
        ts = datetime.datetime.strptime(entry.get('timestamp'), "%Y%m%d_%H%M%S").strftime("%Y-%m-%d %H:%M:%S")
        print(f"{entry['id']:<25} | {ts:<20} | {fname:<40} | {entry.get('changes_count', 0)}")
        count += 1
        
    print("-" * 100)
    print(f"Total backups listed: {count}")

def restore_backup(backup_id):
    inventory = load_inventory()
    entry = next((item for item in inventory if item["id"] == backup_id), None)
    
    if not entry:
        print(f"Error: Backup ID '{backup_id}' not found.")
        return
    
    backup_path = entry["backup_path"]
    original_path = entry["original_path"]
    
    if not os.path.exists(backup_path):
        print(f"Error: Backup file missing at {backup_path}")
        return
        
    print(f"Restoring '{original_path}' from backup '{backup_id}'...")
    try:
        shutil.copy2(backup_path, original_path)
        print("Restore successful.")
    except Exception as e:
        print(f"Error restoring file: {e}")

def get_terms():
    """
    Scans vocabulary and structure directories for .md files.
    Returns a dictionary mapping lowercase term -> vault-relative path (without extension).
    """
    terms = {}
    
    # Helper to scan a directory
    def scan_dir(directory):
        if not os.path.exists(directory):
            print(f"Warning: Directory not found: {directory}")
            return
            
        # Get relative path from vault root to this directory
        rel_dir = os.path.relpath(directory, VAULT_ROOT)
            
        for f in os.listdir(directory):
            if f.endswith(".md"):
                # Filename is the term
                filename = f[:-3] # Remove .md
                if "|" in filename:
                    continue
                
                # Construct vault-relative path for the link
                # e.g. glean/20_Vocabulary/term
                full_rel_path = os.path.join(rel_dir, filename)
                
                terms[filename.lower()] = full_rel_path

    scan_dir(VOCAB_DIR)
    scan_dir(STRUCT_DIR)
    
    return terms

def process_file(filepath, terms_map, sorted_term_keys, dry_run=True):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Escape terms for regex
    escaped_terms = [re.escape(t) for t in sorted_term_keys]
    
    # Pattern to match existing links or our terms
    pattern_str = r"(\[\[.*?\]\])|(\[[^\]]*?\]\([^\)]*?\))|(\b(?:" + "|".join(escaped_terms) + r")\b)"
    regex = re.compile(pattern_str, re.IGNORECASE)

    changes_made = []
    new_lines = []
    file_modified = False

    for line in lines:
        # Check if line is a table row (starts with | potentially preceded by whitespace)
        is_table_row = line.lstrip().startswith('|')
        
        def replace_func(match):
            g1 = match.group(1) # Wikilink
            g2 = match.group(2) # MD link
            g3 = match.group(3) # Term match
            
            if g1: return g1
            if g2: return g2
            if g3:
                original_text = g3
                lower_text = original_text.lower()
                
                if lower_text in terms_map:
                    rel_path = terms_map[lower_text]
                    
                    # If in a table row, escape the pipe
                    separator = "\\|" if is_table_row else "|"
                    new_text = f"[[{rel_path}{separator}{original_text}]]"
                    
                    changes_made.append(f"'{original_text}' -> '{new_text}'")
                    return new_text
                
                return original_text
                
            return match.group(0)

        new_line = regex.sub(replace_func, line)
        if new_line != line:
            file_modified = True
        new_lines.append(new_line)
    
    if file_modified:
        if dry_run:
            print(f"[DRY RUN] Would modify: {os.path.basename(filepath)}")
            print(f"  - Found {len(changes_made)} terms to link:")
            unique_changes = sorted(list(set(changes_made)))
            for change in unique_changes[:50]:
                print(f"    - {change}")
            if len(unique_changes) > 50:
                print(f"    - ... and {len(unique_changes) - 50} more unique terms.")

        else:
            # Create backup before writing
            print(f"Backing up: {os.path.basename(filepath)}")
            backup_id = create_backup(filepath, changes_made)
            print(f"  - Backup created: {backup_id}")
            
            print(f"Updating: {os.path.basename(filepath)}")
            print(f"  - Linked {len(changes_made)} terms.")
            with open(filepath, 'w', encoding='utf-8') as f:
                f.writelines(new_lines)

def main():
    parser = argparse.ArgumentParser(description="Auto-link vocabulary in articles.")
    parser.add_argument("--file", help="Process a single specific file (relative or absolute path)")
    parser.add_argument("--folder", help="Process all files in a specific folder (relative or absolute path)")
    parser.add_argument("--dry-run", action="store_true", help="Print changes without modifying files")
    parser.add_argument("--no-dry-run", action="store_false", dest="dry_run", help="Actually modify files")
    parser.add_argument("--list-backups", nargs='?', const='ALL', help="List available backups. Optional: provide file path to filter.")
    parser.add_argument("--restore", help="Restore a file from a backup ID")
    
    parser.set_defaults(dry_run=True)
    
    args = parser.parse_args()
    
    # Handle Restore
    if args.restore:
        restore_backup(args.restore)
        return

    # Handle List Backups
    if args.list_backups:
        file_filter = None
        if args.list_backups != 'ALL':
            file_filter = args.list_backups
        list_backups(file_filter)
        return
    
    # Normal Processing
    print(f"Scanning terms in:\n- {VOCAB_DIR}\n- {STRUCT_DIR}")
    terms_map = get_terms()
    
    sorted_term_keys = sorted(terms_map.keys(), key=len, reverse=True)
    print(f"Found {len(terms_map)} unique terms.")
    
    target_files = []

    if args.file:
        # Process single file
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
        # Process specific folder
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
        # Default: Process Articles Dir
        print(f"No file or folder specified. Defaulting to: {ARTICLES_DIR}")
        if os.path.exists(ARTICLES_DIR):
             for root, dirs, files in os.walk(ARTICLES_DIR):
                for file in files:
                    if file.endswith(".md"):
                        target_files.append(os.path.join(root, file))
        else:
            print("Articles directory not found!")
            return

    print(f"Processing {len(target_files)} files...")
    count = 0
    for filepath in target_files:
        process_file(filepath, terms_map, sorted_term_keys, dry_run=args.dry_run)
        count += 1
                
    print(f"Processed {count} files.")
    if args.dry_run:
        print("Run with --no-dry-run to apply changes.")

if __name__ == "__main__":
    main()
