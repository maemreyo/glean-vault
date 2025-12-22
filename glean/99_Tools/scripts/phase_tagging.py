import os
import re
import argparse
from pathlib import Path

def get_phase_mapping(base_tag):
    """
    Returns a dictionary mapping card numbers to the full tag string.
    Phases:
    1. Foundation: 1, 10
    2. Activation: 2, 3, 4
    3. Differentiation: 6, 11, 12
    4. Mastery: 5, 7, 8
    5. Addition: 9
    """
    phases = {
        '01-foundation': [1, 10],
        '02-activation': [2, 3, 4],
        '03-differentiation': [6, 11, 12],
        '04-mastery': [5, 7, 8],
        '05-addition': [9]
    }
    
    card_map = {}
    for phase_suffix, card_nums in phases.items():
        full_tag = f"{base_tag}/{phase_suffix}"
        for card_num in card_nums:
            card_map[card_num] = full_tag
            
    return card_map

def process_file(file_path, target_tag_prefix, dry_run=False):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return False

    # Find the specific test tag (e.g., #flashcards/cam-20-listening-test-01)
    # Regex looks for #flashcards/(prefix[\w-]+)
    # We allow it to be anywhere in the line, preceded by start-of-line or whitespace
    tag_pattern = re.compile(r'(?:^|\s)#flashcards/(' + re.escape(target_tag_prefix) + r'[\w-]*)')
    
    match = tag_pattern.search(content)
    if not match:
        return False # Tag not found, skip file

    # The group(1) is just the suffix part if we used parentheses around prefix... 
    # Wait, my regex `(prefix[\w-]*)` captures the part AFTER #flashcards/ if I strictly followed the previous logic?
    # No, the previous logic was `#flashcards/(...)`. 
    # Let's adjust to capture the FULL tag for replacement safety.
    
    full_tag_match = re.search(r'(#flashcards/' + re.escape(target_tag_prefix) + r'[\w-]*)', content)
    if not full_tag_match:
        return False
        
    base_tag = full_tag_match.group(1) # e.g. #flashcards/cam-20-listening-test-01

    print(f"Processing {os.path.basename(file_path)}...")
    print(f"  Found tag: {base_tag}")

    card_map = get_phase_mapping(base_tag)
    
    # 1. Remove the base tag from the header
    lines = content.splitlines()
    new_lines = []
    
    tag_removed = False
    
    for line in lines:
        if not tag_removed and base_tag in line:
            # Check if this is a "phase" tag already
            if re.search(re.escape(base_tag) + r'/\d{2}-', line):
                new_lines.append(line)
                continue
                
            # Remove the tag
            # We must be careful about spaces ensuring we don't leave double spaces
            # Simple approach: split by spaces, filter, join
            parts = line.split()
            new_parts = [p for p in parts if p != base_tag]
            modified_line = ' '.join(new_parts)
            
            if modified_line:
                new_lines.append(modified_line)
            else:
                # If line is empty after removal, maintain a blank line if logic allows,
                # but usually header lines are better compact.
                # However, if it separates frontmatter, we might need it.
                # If the line was JUST the tag, it's likely a tag line.
                pass 
            tag_removed = True
        else:
            new_lines.append(line)

    content = '\n'.join(new_lines)
    
    # 2. Inject phase tags
    # We look for "### Card X:"
    # We insert the tag line ABOVE it.
    
    def replace_card_header(match):
        card_num = int(match.group(1))
        original_header = match.group(0)
        
        if card_num in card_map:
            tag_to_insert = card_map[card_num]
            # Ensure there's a newline before the tag for cleanliness, matching user format
            return f"{tag_to_insert}\n{original_header}"
        return original_header

    # Pattern: ### Card (\d+)
    # We use re.sub with a callback
    card_header_pattern = re.compile(r'(?m)^### Card (\d+)(.|$)')
    
    new_content = card_header_pattern.sub(replace_card_header, content)

    if content == new_content and tag_removed:
        print("  Warning: Tag removed but no cards tagged? (Check card formats)")
    
    if content == new_content and not tag_removed:
        print("  No changes needed (maybe already processed).")
        return False

    if dry_run:
        print("  [DRY RUN] Would write modifications.")
        # print(new_content[:500]) # Preview
        return False
    else:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("  Updated file.")
        return True

def main():
    parser = argparse.ArgumentParser(description="Reorganize flashcard tags into phases.")
    parser.add_argument('--folder', required=True, help="Folder to scan")
    parser.add_argument('--target', required=True, help="Target tag prefix (e.g. cam-20)")
    parser.add_argument('--dry-run', action='store_true', help="Don't save changes")

    args = parser.parse_args()

    count = 0
    folder = Path(args.folder)
    
    if not folder.exists():
        print(f"Folder not found: {folder}")
        return

    for file_path in folder.rglob('*.md'):
        if process_file(file_path, args.target, args.dry_run):
            count += 1

    print(f"\nTotal files processed: {count}")

if __name__ == "__main__":
    main()
