import os
import re
import argparse
import sys
import shutil
import json
import datetime
import hashlib
import subprocess
import yaml # Requires pyyaml, but we can do simple parsing if dependency is an issue.
# To avoid dependencies, we will parse simple Frontmatter manually.

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

def parse_frontmatter_aliases(filepath):
    """
    Parses 'aliases: [a, b, c]' or 'aliases: \n - a \n - b' from Frontmatter.
    Simple manual parsing to avoid external dependencies.
    Handles content before the Frontmatter block.
    """
    aliases = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        if not lines:
            return []
            
        fm_start_idx = -1
        for i, line in enumerate(lines):
            if line.strip() == '---':
                fm_start_idx = i
                break
                
        if fm_start_idx == -1:
            return []
            
        in_alias_block = False
        
        # Start scanning after the first ---
        for i in range(fm_start_idx + 1, len(lines)):
            line = lines[i]
            line_strip = line.strip()
            
            if line_strip == '---':
                break # End of FM
                
            # Check for inline aliases: "aliases: [one, two]"
            if line_strip.startswith('aliases:'):
                # Check for inline array list
                inline_match = re.search(r'\[(.*?)\]', line_strip)
                if inline_match:
                    content = inline_match.group(1)
                    if content:
                        items = [x.strip() for x in content.split(',')]
                        aliases.extend(items)
                else:
                    in_alias_block = True
                    
            elif in_alias_block:
                if line_strip.startswith('-'):
                    # List item: "- alias"
                    alias = line_strip[1:].strip()
                    if alias:
                        aliases.append(alias)
                elif ':' in line_strip:
                    # New key, end of alias block
                    in_alias_block = False
                    
    except Exception as e:
        print(f"Warning: Error parsing {filepath}: {e}")
        
    return aliases

def get_terms():
    """
    Scans vocabulary and structure directories for .md files recursively.
    Priority: Filename (Main Term) > Aliases.
    Returns a dictionary mapping lowercase term -> vault-relative path.
    """
    terms = {}
    alias_candidates = [] # Store (alias, path) pairs for the second pass
    
    # Helper to scan a directory recursively
    def scan_dir(directory):
        if not os.path.exists(directory):
            print(f"Warning: Directory not found: {directory}")
            return
            
        for root, dirs, files in os.walk(directory):
            for f in files:
                if f.endswith(".md"):
                    # Filename is the term
                    filename = f[:-3] # Remove .md
                    if "|" in filename:
                        continue
                    
                    full_abs_path = os.path.join(root, f)
                    full_rel_path = os.path.relpath(full_abs_path, VAULT_ROOT)
                    if full_rel_path.endswith(".md"):
                        full_rel_path = full_rel_path[:-3]
                    
                    # 1. First Pass: Add main term (filename)
                    # Filenames ALWAYS take priority
                    terms[filename.lower()] = full_rel_path
                    
                    # 2. Collect aliases for second pass
                    aliases = parse_frontmatter_aliases(full_abs_path)
                    for alias in aliases:
                        if alias:
                            alias_candidates.append((alias.lower(), full_rel_path))

    scan_dir(VOCAB_DIR)
    scan_dir(STRUCT_DIR)
    
    # 2. Second Pass: Add aliases only if they don't conflict with main terms
    for alias, path in alias_candidates:
        if alias not in terms:
            terms[alias] = path
        # If alias is already in terms (as a filename), we skip it as requested.
    
    return terms

def migrate_aliases_field(dry_run=True):
    """
    Scans all vocab/structure files. If 'aliases:' is missing in FM, adds 'aliases: []'.
    """
    targets = []
    print(f"Scanning for migration targets in:\n- {VOCAB_DIR}\n- {STRUCT_DIR}")
    for d in [VOCAB_DIR, STRUCT_DIR]:
        if os.path.exists(d):
            # Recursively find all MD files
            for root, dirs, files in os.walk(d):
                for f in files:
                    if f.endswith(".md"):
                        targets.append(os.path.join(root, f))
    
    print(f"Found {len(targets)} potential files to check.")
    count = 0
    
    for filepath in targets:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except Exception:
            continue
            
        if not lines:
            continue
            
        fm_start_index = -1
        fm_end_index = -1
        has_aliases = False
        
        # 1. Find Start of Frontmatter
        for i, line in enumerate(lines):
            if line.strip() == '---':
                fm_start_index = i
                break
        
        if fm_start_index == -1:
            # No FM start found
            continue
            
        # 2. Find End of Frontmatter (search after start)
        for i in range(fm_start_index + 1, len(lines)):
            line = lines[i].strip()
            if line == '---':
                fm_end_index = i
                break
            if line.startswith('aliases:'):
                has_aliases = True
                
        # Only proceed if we found a closed FM block
        if fm_end_index > fm_start_index and not has_aliases:
            # Need to insert aliases
            if dry_run:
                # Limit debug output
                if count < 5:
                     print(f"[DRY RUN] Would add 'aliases: []' to {os.path.basename(filepath)}")
                count += 1
            else:
                # Find 'tags:' line to insert after
                insert_idx = fm_end_index 
                found_tags = False
                
                for i in range(fm_start_index + 1, fm_end_index):
                    if lines[i].strip().startswith('tags:'):
                         found_tags = True
                         # Try to find end of tags block if it's a list
                         j = i + 1
                         while j < fm_end_index:
                             next_line = lines[j].strip()
                             if next_line.startswith('-'):
                                 j += 1
                             else:
                                 break
                         insert_idx = j
                         break
                
                new_lines = lines[:]
                # Use same indentation as tags if possible, otherwise no indent
                indent = ""
                
                new_lines.insert(insert_idx, f"{indent}aliases: []\n")
                
                print(f"Migrating: {os.path.basename(filepath)}")
                # create_backup(filepath, ["Added aliases: [] field"])
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.writelines(new_lines)
                count += 1

    if dry_run:
        print(f"[DRY RUN] Total files to migrate: {count}")
    else:
        print(f"Migrated {count} files.")

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
                    
                    # If original text matches term filename case-insensitively, we can just use [[Term]]
                    # But if it's an alias or different case, we need [[Term|Original]]
                    term_filename = os.path.basename(rel_path)
                    
                    # Always use piped link for clarity and alias support
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

def restore_session(session_prefix):
    inventory = load_inventory()
    # Filter entries that start with this prefix
    entries = [item for item in inventory if item["id"].startswith(session_prefix)]
    
    if not entries:
        print(f"Error: No backups found matching session prefix '{session_prefix}'.")
        return
    
    print(f"Found {len(entries)} files in session '{session_prefix}'. Restoring...")
    
    success_count = 0
    for entry in entries:
        backup_path = entry["backup_path"]
        original_path = entry["original_path"]
        
        if not os.path.exists(backup_path):
            print(f"Warning: Backup file missing for {os.path.basename(original_path)}")
            continue
            
        try:
            shutil.copy2(backup_path, original_path)
            success_count += 1
            print(f"  - Restored: {os.path.basename(original_path)}")
        except Exception as e:
            print(f"  - Error restoring {os.path.basename(original_path)}: {e}")
            
    print(f"Restoration complete. {success_count}/{len(entries)} files restored.")

def restore_to_original(path):
    """
    Restore a file or all files in a folder to their oldest backup version.
    """
    inventory = load_inventory()
    abs_path = os.path.abspath(path)
    
    # Check if path is a directory
    if os.path.isdir(abs_path):
        print(f"Restoring all files in folder: {abs_path}")
        
        # Collect all unique original paths within this directory
        files_to_restore = []
        for item in inventory:
            orig_path = item.get("original_path")
            if orig_path and orig_path.startswith(abs_path):
                files_to_restore.append(orig_path)
        
        # Remove duplicates
        files_to_restore = list(set(files_to_restore))
        
        if not files_to_restore:
            print(f"Error: No backup history found for any files in '{path}'.")
            return
        
        print(f"Found {len(files_to_restore)} file(s) with backup history.")
        success_count = 0
        
        for file_path in sorted(files_to_restore):
            # Find oldest backup for this file
            entries = [item for item in inventory if item.get("original_path") == file_path]
            if not entries:
                continue
                
            entries.sort(key=lambda x: x["timestamp"])
            oldest_entry = entries[0]
            backup_path = oldest_entry["backup_path"]
            
            if not os.path.exists(backup_path):
                print(f"  ⚠️  Skipping '{os.path.basename(file_path)}': backup missing")
                continue
            
            print(f"  ✅ Restoring '{os.path.basename(file_path)}' (from {oldest_entry['timestamp']})")
            try:
                shutil.copy2(backup_path, file_path)
                success_count += 1
            except Exception as e:
                print(f"  ❌ Error restoring '{os.path.basename(file_path)}': {e}")
        
        print(f"\nRestored {success_count}/{len(files_to_restore)} files successfully.")
        
    else:
        # Single file restore (original behavior)
        entries = [item for item in inventory if item.get("original_path") == abs_path]
        
        if not entries:
            print(f"Error: No backup history found for '{os.path.basename(path)}'.")
            return
        
        # Sort by timestamp ascending to find the oldest (original) one
        entries.sort(key=lambda x: x["timestamp"])
        oldest_entry = entries[0]
        
        backup_path = oldest_entry["backup_path"]
        if not os.path.exists(backup_path):
            print(f"Error: The oldest backup file is missing at {backup_path}")
            return
            
        print(f"Restoring '{os.path.basename(path)}' to its OLDEST version ({oldest_entry['timestamp']})...")
        try:
            shutil.copy2(backup_path, abs_path)
            print("Restore successful.")
        except Exception as e:
            print(f"Error restoring file: {e}")

def main():
    parser = argparse.ArgumentParser(description="Auto-link vocabulary in articles.")
    parser.add_argument("--file", help="Process a single specific file (relative or absolute path)")
    parser.add_argument("--folder", help="Process all files in a specific folder (relative or absolute path)")
    parser.add_argument("--dry-run", action="store_true", help="Print changes without modifying files")
    parser.add_argument("--no-dry-run", action="store_false", dest="dry_run", help="Actually modify files")
    parser.add_argument("--list-backups", nargs='?', const='ALL', help="List available backups. Optional: provide file path to filter.")
    parser.add_argument("--restore", help="Restore a single file from a specific backup ID")
    parser.add_argument("--restore-all", help="Restore all files from a specific session (timestamp prefix)")
    parser.add_argument("--restore-original", help="Restore a specific file to its very first (oldest) backup version")
    parser.add_argument("--migrate-aliases", action="store_true", help="One-time utility: Add 'aliases: []' to existing vocabulary files.")
    parser.add_argument("--restore-before-link", action="store_true", help="Restore all target files to original before linking (requires --folder or --file)")
    parser.add_argument("--clean-quotes", action="store_true", help="Run clean_quotes.py on target files before linking (requires --folder or --file)")
    
    parser.set_defaults(dry_run=True)
    
    args = parser.parse_args()
    
    # Handle Restore
    if args.restore:
        restore_backup(args.restore)
        return

    # Handle Batch Restore
    if args.restore_all:
        restore_session(args.restore_all)
        return
        
    # Handle Restore Original
    if args.restore_original:
        restore_to_original(args.restore_original)
        return

    # Handle List Backups
    if args.list_backups:
        file_filter = None
        if args.list_backups != 'ALL':
            file_filter = args.list_backups
        list_backups(file_filter)
        return
        
    # Handle Migration
    if args.migrate_aliases:
        print("Starting alias migration scan...")
        migrate_aliases_field(dry_run=args.dry_run)
        return
    
    # Determine target path for workflow options
    target_path = None
    if args.file:
        target_path = os.path.abspath(args.file)
        if not os.path.exists(target_path):
            potential_path = os.path.join(VAULT_ROOT, args.file)
            if os.path.exists(potential_path):
                target_path = potential_path
    elif args.folder:
        target_path = os.path.abspath(args.folder)
        if not os.path.exists(target_path):
            potential_path = os.path.join(VAULT_ROOT, args.folder)
            if os.path.exists(potential_path):
                target_path = potential_path
    else:
        # Default to articles dir
        target_path = ARTICLES_DIR
    
    # Handle restore-before-link
    if args.restore_before_link:
        if not (args.file or args.folder):
            print("⚠️  Warning: --restore-before-link requires --file or --folder. Using default Articles directory.")
        print("\n🔄 Step 1: Restoring files to original state...")
        print("=" * 60)
        restore_to_original(target_path)
        print("\n")
    
    # Handle clean-quotes
    if args.clean_quotes:
        if not (args.file or args.folder):
            print("⚠️  Warning: --clean-quotes requires --file or --folder. Using default Articles directory.")
        print("\n🧹 Step 2: Cleaning quotes..." if args.restore_before_link else "\n🧹 Step 1: Cleaning quotes...")
        print("=" * 60)
        
        # Build clean_quotes.py command
        clean_script = os.path.join(os.path.dirname(__file__), "clean_quotes.py")
        
        if os.path.isdir(target_path):
            cmd = ["python3", clean_script, "--folder", target_path, "--no-dry-run"]
        else:
            cmd = ["python3", clean_script, "--file", target_path, "--no-dry-run"]
        
        try:
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            print(result.stdout)
            if result.stderr:
                print(result.stderr)
        except subprocess.CalledProcessError as e:
            print(f"❌ Error running clean_quotes.py: {e}")
            print(e.stdout)
            print(e.stderr)
            return
        print("\n")
    
    # Normal Processing
    step_num = 1
    if args.restore_before_link:
        step_num += 1
    if args.clean_quotes:
        step_num += 1
    
    if step_num > 1:
        print(f"\n🔗 Step {step_num}: Linking vocabulary...")
        print("=" * 60)
    
    print(f"Scanning terms in:\n- {VOCAB_DIR}\n- {STRUCT_DIR}")
    terms_map = get_terms()
    
    sorted_term_keys = sorted(terms_map.keys(), key=len, reverse=True)
    print(f"Found {len(terms_map)} unique terms (including aliases).")
    
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
