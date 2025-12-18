import os
import re
import argparse
import sys

# Configuration
# This script is located in glean/99_Tools/scripts/
# We want to go up 3 levels to reach the vault root (glean/99_Tools/scripts -> glean/99_Tools -> glean -> root)
# Wait, glean/99_Tools/scripts is deep.
# Path: glean-vault/glean/99_Tools/scripts/auto_link_vocab.py
# Root: glean-vault
# ../../../ is correct.

VAULT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
VOCAB_DIR = os.path.join(VAULT_ROOT, "20_Vocabulary")
STRUCT_DIR = os.path.join(VAULT_ROOT, "30_Structures")
ARTICLES_DIR = os.path.join(VAULT_ROOT, "10_Sources/Articles")

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
        content = f.read()

    # Escape terms for regex
    escaped_terms = [re.escape(t) for t in sorted_term_keys]
    
    pattern_str = r"(\[\[.*?\]\])|(\[[^\]]*?\]\([^\)]*?\))|(\b(?:" + "|".join(escaped_terms) + r")\b)"
    regex = re.compile(pattern_str, re.IGNORECASE)

    changes_made = []

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
                # relative path, e.g. glean/20_Vocabulary/word
                rel_path = terms_map[lower_text]
                
                # Check if we should use an alias
                # We almost always want to preserve the original text as the alias if it differs from the path basename
                # Or even if it's the same, to be safe?
                # Actually, Obsidian links: [[path/to/file|Display Text]]
                
                new_text = f"[[{rel_path}|{original_text}]]"
                
                changes_made.append(f"'{original_text}' -> '{new_text}'")
                return new_text
            
            return original_text
            
        return match.group(0)

    new_content = regex.sub(replace_func, content)
    
    if new_content != content:
        if dry_run:
            print(f"[DRY RUN] Would modify: {os.path.basename(filepath)}")
            print(f"  - Found {len(changes_made)} terms to link:")
            # Limit output if too many, or show all? 
            # User likely wants to see them to verify. Let's show up to 20, then summarize.
            unique_changes = sorted(list(set(changes_made)))
            for change in unique_changes[:50]:
                print(f"    - {change}")
            if len(unique_changes) > 50:
                print(f"    - ... and {len(unique_changes) - 50} more unique terms.")

        else:
            print(f"Updating: {os.path.basename(filepath)}")
            print(f"  - Linked {len(changes_made)} terms.")
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
    # else:
    #     if dry_run:
    #         print(f"[DRY RUN] No terms found in: {os.path.basename(filepath)}")

def main():
    parser = argparse.ArgumentParser(description="Auto-link vocabulary in articles.")
    parser.add_argument("--file", help="Process a single specific file (relative or absolute path)")
    parser.add_argument("--folder", help="Process all files in a specific folder (relative or absolute path)")
    parser.add_argument("--dry-run", action="store_true", help="Print changes without modifying files")
    parser.add_argument("--no-dry-run", action="store_false", dest="dry_run", help="Actually modify files")
    parser.set_defaults(dry_run=True)
    
    args = parser.parse_args()
    
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
