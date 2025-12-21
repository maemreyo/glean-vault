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

def convert_ref_to_tag(ref_text):
    """
    Convert a reference like 'Cam 19 Listening Test 02' to '#flashcards/cambridge-19-test-02'
    """
    # Clean the ref text (remove wikilink brackets if any)
    clean_text = re.sub(r'\\[\\[|\\]\\]', '', ref_text).strip()
    
    # Convert to lowercase and replace spaces with hyphens
    tag_text = clean_text.lower().replace(' ', '-')
    
    # Build the full tag
    return f"#flashcards/{tag_text}"

def parse_frontmatter_refs(filepath):
    """
    Parse the 'ref:' field from frontmatter and return list of reference names.
    Handles both inline and list format:
    - ref: [[File]]
    - ref:
        - [[File 1]]
        - [[File 2]]
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
                break # End of FM
                
            # Check for inline ref: "ref: [[File]]"
            if line_strip.startswith('ref:'):
                # Check for inline wikilink
                inline_match = re.search(r'\\[\\[([^\\]]+)\\]\\]', line_strip)
                if inline_match:
                    refs.append(inline_match.group(1))
                else:
                    in_ref_block = True
                    
            elif in_ref_block:
                if line_strip.startswith('-'):
                    # List item: "- [[File]]"
                    wikilink_match = re.search(r'\\[\\[([^\\]]+)\\]\\]', line_strip)
                    if wikilink_match:
                        refs.append(wikilink_match.group(1))
                elif ':' in line_strip and not line_strip.startswith(' '):
                    # New key, end of ref block
                    in_ref_block = False
                    
    except Exception as e:
        print(f"Warning: Error parsing refs from {filepath}: {e}")
        
    return refs

def add_ref_tags_to_file(filepath, dry_run=True):
    """
    Read the ref: field from frontmatter, generate tags, and add them to the flashcard tag line.
    """
    try:
        # 1. Parse refs from frontmatter
        refs = parse_frontmatter_refs(filepath)
        
        if not refs:
            return False, "No refs found"
            
        # 2. Generate tags from refs
        ref_tags = [convert_ref_to_tag(ref) for ref in refs]
        
        # 3. Read the file
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        if not lines:
            return False, "Empty file"
            
        # 4. Find the flashcard tag line (first line starting with #flashcards)
        flashcard_line_idx = -1
        for i, line in enumerate(lines):
            if line.strip().startswith('#flashcards'):
                flashcard_line_idx = i
                break
                
        if flashcard_line_idx == -1:
            return False, "No flashcard tag line found"
            
        # 5. Check if ref tags already exist
        current_line = lines[flashcard_line_idx].strip()
        tags_to_add = []
        
        for ref_tag in ref_tags:
            if ref_tag not in current_line:
                tags_to_add.append(ref_tag)
                
        if not tags_to_add:
            return False, "Tags already present"
            
        # 6. Add tags to the end of the line
        new_line = current_line + ' ' + ' '.join(tags_to_add) + '\\n'
        
        if dry_run:
            return True, f"Would add: {', '.join(tags_to_add)}"
        else:
            # 7. Create backup
            backup_id = create_backup(filepath, [f"Added ref tags: {', '.join(tags_to_add)}"])
            
            # 8. Update the file
            lines[flashcard_line_idx] = new_line
            with open(filepath, 'w', encoding='utf-8') as f:
                f.writelines(lines)
                
            return True, f"Added: {', '.join(tags_to_add)} (backup: {backup_id})"
            
    except Exception as e:
        return False, f"Error: {e}"

def process_ref_tags(target_path, dry_run=True):
    """
    Process all vocabulary files in target_path and add ref-based tags.
    """
    if os.path.isfile(target_path):
        files_to_process = [target_path]
    else:
        files_to_process = []
        for root, dirs, files in os.walk(target_path):
            for f in files:
                if f.endswith('.md'):
                    files_to_process.append(os.path.join(root, f))
                    
    if not files_to_process:
        print("No files to process.")
        return
        
    print(f"Processing {len(files_to_process)} file(s)...")
    print("=" * 60)
    
    success_count = 0
    skip_count = 0
    
    for filepath in sorted(files_to_process):
        filename = os.path.basename(filepath)
        success, message = add_ref_tags_to_file(filepath, dry_run=dry_run)
        
        if success:
            print(f"✅ {filename}")
            print(f"   {message}")
            success_count += 1
        else:
            if "already present" in message.lower() or "no refs" in message.lower():
                skip_count += 1
            else:
                print(f"⚠️  {filename}: {message}")
                
    print("=" * 60)
    print(f"Summary: {success_count} updated, {skip_count} skipped")
    
    if dry_run:
        print("\\nRun with --no-dry-run to apply changes.")
