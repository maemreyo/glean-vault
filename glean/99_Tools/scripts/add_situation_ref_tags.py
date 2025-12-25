#!/usr/bin/env python3
"""
Add ref-based tags to Situation flashcard files.
This script reads the 'ref:' field from frontmatter and adds corresponding tags to each flashcard.
"""

import os
import re
import sys
import shutil
import json
import datetime
import hashlib

# Configuration
# Script is in glean/99_Tools/scripts/ (3 levels deep)
VAULT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
SITUATION_DIR = os.path.join(VAULT_ROOT, "glean/40_Situation")
BACKUP_DIR = os.path.join(VAULT_ROOT, "glean/99_Tools/backups")
INVENTORY_FILE = os.path.join(BACKUP_DIR, "inventory.json")


def ensure_backup_dir():
    """Create backup directory if it doesn't exist."""
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)
    if not os.path.exists(INVENTORY_FILE):
        with open(INVENTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f)


def load_inventory():
    """Load backup inventory."""
    ensure_backup_dir()
    try:
        with open(INVENTORY_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []


def save_inventory(inventory):
    """Save backup inventory."""
    ensure_backup_dir()
    with open(INVENTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(inventory, f, indent=2)


def create_backup(filepath, changes_summary):
    """Create a backup of the file before modification."""
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
        "changes_sample": changes_summary[:5]
    }
    
    inventory = load_inventory()
    inventory.insert(0, backup_entry)
    save_inventory(inventory)
    
    return backup_entry["id"]


def convert_ref_to_tag(ref_text):
    """
    Convert a reference like 'Cam 20 Listening Test 03' to '#flashcards/cambridge/cam-20-listening-test-03'
    """
    # Clean the ref text (remove wikilink brackets if any)
    clean_text = re.sub(r'\[\[|\]\]', '', ref_text).strip()
    
    # Convert to lowercase and replace spaces with hyphens
    tag_text = clean_text.lower().replace(' ', '-')
    
    # Build the full tag
    return f"#flashcards/cambridge/{tag_text}"


def parse_frontmatter_refs(filepath):
    """
    Parse the 'ref:' field from frontmatter and return list of reference names.
    Handles both inline and list format:
    - ref: [[File]]
    - ref:
        - [[File 1]]
        - [[File 2]]
    Also handles plain text without wikilinks:
    - ref:
        - Cam 20 Listening Test 03
    """
    refs = []
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
            
        in_ref_block = False
        
        # Start scanning after the first ---
        for i in range(fm_start_idx + 1, len(lines)):
            line = lines[i]
            line_strip = line.strip()
            
            if line_strip == '---':
                break  # End of FM
                
            # Check for inline ref: "ref: [[File]]" or "ref: Text"
            if line_strip.startswith('ref:'):
                # Check for inline wikilink
                inline_match = re.search(r'\[\[([^\]]+)\]\]', line_strip)
                if inline_match:
                    refs.append(inline_match.group(1))
                else:
                    # Check for plain text after colon
                    text_match = re.match(r'ref:\s*(.+)', line_strip)
                    if text_match and text_match.group(1).strip():
                        refs.append(text_match.group(1).strip())
                    else:
                        in_ref_block = True
                    
            elif in_ref_block:
                if line_strip.startswith('-'):
                    # List item: "- [[File]]" or "- Text"
                    wikilink_match = re.search(r'\[\[([^\]]+)\]\]', line_strip)
                    if wikilink_match:
                        refs.append(wikilink_match.group(1))
                    else:
                        # Plain text list item
                        text = line_strip[1:].strip()
                        if text:
                            refs.append(text)
                elif ':' in line_strip and not line_strip.startswith(' '):
                    # New key, end of ref block
                    in_ref_block = False
                    
    except Exception as e:
        print(f"Warning: Error parsing refs from {filepath}: {e}")
        
    return refs


def add_ref_tags_to_file(filepath, dry_run=True):
    """
    Read the ref: field from frontmatter, generate tags, and add them to each flashcard tag line.
    """
    try:
        # 1. Parse refs from frontmatter
        refs = parse_frontmatter_refs(filepath)
        
        if not refs:
            return False, "No refs found"
            
        # 2. Generate tags from refs
        ref_tags = [convert_ref_to_tag(ref) for ref in refs]
        ref_tag = ref_tags[0]  # Use the first ref tag
        
        # 3. Read the file
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        if not lines:
            return False, "Empty file"
            
        # 4. Find all flashcard tag lines (lines starting with #flashcards)
        modified = False
        new_lines = []
        
        for i, line in enumerate(lines):
            if line.strip().startswith('#flashcards'):
                # Check if ref tag already exists
                if ref_tag in line:
                    new_lines.append(line)
                else:
                    # Add ref tag to the end of the line
                    new_line = line.rstrip() + ' ' + ref_tag + '\n'
                    new_lines.append(new_line)
                    modified = True
            else:
                new_lines.append(line)
                
        if not modified:
            return False, "Tags already present"
            
        if dry_run:
            return True, f"Would add: {ref_tag}"
        else:
            # 5. Create backup
            backup_id = create_backup(filepath, [f"Added ref tag: {ref_tag}"])
            
            # 6. Update the file
            with open(filepath, 'w', encoding='utf-8') as f:
                f.writelines(new_lines)
                
            return True, f"Added: {ref_tag} (backup: {backup_id})"
            
    except Exception as e:
        return False, f"Error: {e}"


def process_files_from_commit(commit_hash, dry_run=True):
    """
    Process all files from a specific commit.
    """
    # Get list of files from commit
    import subprocess
    
    try:
        # Use -z to get null-terminated paths (handles special characters in filenames)
        result = subprocess.run(
            ['git', 'show', '--name-only', '-z', '--pretty=format:', commit_hash],
            cwd=VAULT_ROOT,
            capture_output=True,
            text=True,
            check=True
        )
        
        # Split by null byte
        files = [line for line in result.stdout.split('\0') if line.strip()]
        files = [f for f in files if f.startswith('glean/40_Situation/') and f.endswith('.md')]
        
    except subprocess.CalledProcessError as e:
        print(f"Error getting files from commit: {e}")
        return
        
    if not files:
        print("No Situation files found in commit.")
        return
        
    print(f"Processing {len(files)} file(s) from commit {commit_hash}...")
    print("=" * 80)
    
    success_count = 0
    skip_count = 0
    error_count = 0
    
    for file_rel_path in sorted(files):
        filepath = os.path.join(VAULT_ROOT, file_rel_path)
        filename = os.path.basename(filepath)
        
        if not os.path.exists(filepath):
            print(f"⚠️  {filename}: File not found")
            error_count += 1
            continue
            
        success, message = add_ref_tags_to_file(filepath, dry_run=dry_run)
        
        if success:
            print(f"✅ {filename}")
            print(f"   {message}")
            success_count += 1
        else:
            if "already present" in message.lower() or "no refs" in message.lower():
                skip_count += 1
                if dry_run:
                    print(f"⏭️  {filename}: {message}")
            else:
                print(f"⚠️  {filename}: {message}")
                error_count += 1
                
    print("=" * 80)
    print(f"Summary: {success_count} updated, {skip_count} skipped, {error_count} errors")
    
    if dry_run:
        print("\nRun with --no-dry-run to apply changes.")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Add ref-based tags to Situation flashcard files'
    )
    parser.add_argument(
        '--commit',
        default='14d5b84790de624c9ec05d50af83042cd0717fb9',
        help='Git commit hash to process files from'
    )
    parser.add_argument(
        '--no-dry-run',
        action='store_true',
        help='Actually modify files (default is dry-run)'
    )
    
    args = parser.parse_args()
    
    dry_run = not args.no_dry_run
    
    if dry_run:
        print("🔍 DRY RUN MODE - No files will be modified")
        print()
    
    process_files_from_commit(args.commit, dry_run=dry_run)


if __name__ == '__main__':
    main()
