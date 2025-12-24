#!/usr/bin/env python3
"""
Auto-Link Vocabulary Script (Modular Version)

Automatically links vocabulary and structure terms in Obsidian Markdown files.
Scans vault for terms in 20_Vocabulary and 30_Structures and creates wikilinks.

Features:
- Smart linking with alias support
- HTML table to Markdown conversion
- Clean quotes (integrated)
- Backup management with configurable modes
- Phase tagging from ref field
- Dry-run mode for preview

Usage:
    python3 glean/99_Tools/scripts/auto_link_vocab.py [options]
"""

import os
import re
import sys
import json
import shutil
import argparse
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any, Set
from dataclasses import dataclass, asdict
from enum import Enum
from html.parser import HTMLParser


# ============================================================================
# Configuration
# ============================================================================

VAULT_ROOT = Path(__file__).parent.parent.parent.resolve()
VOCAB_DIR = VAULT_ROOT / "20_Vocabulary"
STRUCT_DIR = VAULT_ROOT / "30_Structures"
ARTICLES_DIR = VAULT_ROOT / "10_Sources" / "Articles"
BACKUP_DIR = VAULT_ROOT / "99_Tools" / "backups"
INVENTORY_FILE = BACKUP_DIR / "inventory.json"


# ============================================================================
# Enums and Data Classes
# ============================================================================

class BackupMode(Enum):
    """Backup strategy modes"""
    ORIGINAL = "original"  # Keep only the first (original) backup
    SESSION = "session"    # Create backup per session
    OFF = "off"            # No backup (dangerous)


@dataclass
class BackupEntry:
    """Backup metadata"""
    id: str
    timestamp: str
    original_path: str
    backup_path: str
    changes_count: int
    changes_sample: List[str]
    tool: str = "auto_link_vocab"


@dataclass
class ProcessResult:
    """Result of processing a file"""
    success: bool
    message: str
    backup_id: Optional[str] = None
    changes_count: int = 0


# ============================================================================
# Backup Manager Module
# ============================================================================

class BackupManager:
    """Manages backup operations with configurable strategies"""

    def __init__(self, backup_dir: Path = BACKUP_DIR, inventory_file: Path = INVENTORY_FILE):
        self.backup_dir = backup_dir
        self.inventory_file = inventory_file
        self._ensure_dirs()

    def _ensure_dirs(self) -> None:
        """Create backup directory and inventory file if needed"""
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        if not self.inventory_file.exists():
            self._save_inventory([])

    def _load_inventory(self) -> List[Dict[str, Any]]:
        """Load backup inventory from file"""
        try:
            content = self.inventory_file.read_text(encoding='utf-8')
            return json.loads(content) if content else []
        except (json.JSONDecodeError, Exception):
            return []

    def _save_inventory(self, inventory: List[Dict[str, Any]]) -> None:
        """Save backup inventory to file"""
        self.inventory_file.write_text(
            json.dumps(inventory, indent=2, ensure_ascii=False),
            encoding='utf-8'
        )

    def _generate_backup_id(self, original_path: Path) -> str:
        """Generate unique backup ID"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        # Use hash of path for consistency
        path_hash = abs(hash(str(original_path))) % 1000000
        return f"{timestamp}_{path_hash:06x}"

    def _get_backup_filename(self, backup_id: str, original_path: Path) -> str:
        """Generate backup filename"""
        return f"{backup_id}_{original_path.name}"

    def create_backup(
        self,
        original_path: Path,
        changes: List[str],
        mode: BackupMode = BackupMode.ORIGINAL,
        tool: str = "auto_link_vocab"
    ) -> Optional[str]:
        """
        Create backup of a file with specified mode.

        Returns:
            Backup ID if backup was created, None if skipped (e.g., ORIGINAL mode with existing backup)
        """
        if mode == BackupMode.OFF:
            return None

        original_path = Path(original_path).resolve()
        original_path_str = str(original_path)

        # For ORIGINAL mode, check if backup already exists
        if mode == BackupMode.ORIGINAL:
            inventory = self._load_inventory()
            existing = [
                item for item in inventory
                if item.get('original_path') == original_path_str
                and item.get('tool') == tool
            ]
            if existing:
                return None  # Already have original backup

        # Generate backup ID and path
        backup_id = self._generate_backup_id(original_path)
        backup_filename = self._get_backup_filename(backup_id, original_path)
        backup_path = self.backup_dir / backup_filename

        # Copy file to backup
        shutil.copy2(original_path, backup_path)

        # Create backup entry
        entry = BackupEntry(
            id=backup_id,
            timestamp=datetime.now().strftime("%Y%m%d_%H%M%S"),
            original_path=original_path_str,
            backup_path=str(backup_path),
            changes_count=len(changes),
            changes_sample=changes[:5],  # Store first 5 as sample
            tool=tool
        )

        # Update inventory
        inventory = self._load_inventory()
        inventory.append(asdict(entry))
        self._save_inventory(inventory)

        return backup_id

    def list_backups(self, filter_path: Optional[Path] = None) -> List[BackupEntry]:
        """List available backups, optionally filtered by path"""
        inventory = self._load_inventory()
        entries = []

        for item in inventory:
            if item.get('tool') != 'auto_link_vocab':
                continue

            if filter_path:
                filter_path_str = str(filter_path.resolve())
                if item.get('original_path') != filter_path_str:
                    continue

            entries.append(BackupEntry(**item))

        return sorted(entries, key=lambda x: x.timestamp, reverse=True)

    def restore_backup(self, backup_id: str) -> ProcessResult:
        """Restore a file from specific backup ID"""
        inventory = self._load_inventory()
        entry_data = next(
            (item for item in inventory if item.get('id') == backup_id),
            None
        )

        if not entry_data:
            return ProcessResult(
                success=False,
                message=f"Backup ID '{backup_id}' not found"
            )

        backup_path = Path(entry_data['backup_path'])
        original_path = Path(entry_data['original_path'])

        if not backup_path.exists():
            return ProcessResult(
                success=False,
                message=f"Backup file missing at {backup_path}"
            )

        try:
            shutil.copy2(backup_path, original_path)
            return ProcessResult(
                success=True,
                message=f"Restored '{original_path.name}' from backup {backup_id}",
                backup_id=backup_id
            )
        except Exception as e:
            return ProcessResult(
                success=False,
                message=f"Error restoring file: {e}"
            )

    def restore_session(self, session_prefix: str) -> Tuple[int, int]:
        """Restore all backups from a specific session (timestamp prefix)

        Returns:
            Tuple of (success_count, total_count)
        """
        inventory = self._load_inventory()
        entries = [
            item for item in inventory
            if item['id'].startswith(session_prefix) and item.get('tool') == 'auto_link_vocab'
        ]

        if not entries:
            return 0, 0

        success_count = 0
        for entry_data in entries:
            backup_path = Path(entry_data['backup_path'])
            original_path = Path(entry_data['original_path'])

            if backup_path.exists():
                try:
                    shutil.copy2(backup_path, original_path)
                    success_count += 1
                except Exception:
                    pass

        return success_count, len(entries)

    def restore_to_original(self, path: Path) -> Tuple[int, int]:
        """Restore file(s) to their oldest (first) backup

        Returns:
            Tuple of (success_count, total_count)
        """
        inventory = self._load_inventory()
        abs_path = path.resolve()

        if abs_path.is_dir():
            # Find all files in directory
            files_to_restore = []
            for item in inventory:
                if item.get('tool') != 'auto_link_vocab':
                    continue
                orig_path = Path(item.get('original_path', ''))
                if orig_path and orig_path.is_relative_to(abs_path):
                    files_to_restore.append(orig_path)
            files_to_restore = list(set(files_to_restore))
        else:
            files_to_restore = [abs_path]

        success_count = 0
        for file_path in files_to_restore:
            entries = [
                item for item in inventory
                if item.get('original_path') == str(file_path)
                and item.get('tool') == 'auto_link_vocab'
            ]

            if not entries:
                continue

            # Sort by timestamp, get oldest
            entries.sort(key=lambda x: x['timestamp'])
            oldest_entry = entries[0]
            backup_path = Path(oldest_entry['backup_path'])

            if backup_path.exists():
                try:
                    shutil.copy2(backup_path, file_path)
                    success_count += 1
                except Exception:
                    pass

        return success_count, len(files_to_restore)

    def cleanup_redundant(self) -> Tuple[int, int]:
        """Remove all but the original (oldest) backup for each file

        Returns:
            Tuple of (deleted_count, remaining_count)
        """
        inventory = self._load_inventory()

        # Group backups by original_path
        backups_by_file: Dict[str, List[Dict[str, Any]]] = {}
        for item in inventory:
            if item.get('tool') != 'auto_link_vocab':
                continue
            orig_path = item.get('original_path', '')
            if orig_path not in backups_by_file:
                backups_by_file[orig_path] = []
            backups_by_file[orig_path].append(item)

        # Keep only the oldest backup for each file
        to_delete = []
        new_inventory = []

        for orig_path, backups in backups_by_file.items():
            if not backups:
                continue

            # Sort by timestamp
            backups.sort(key=lambda x: x['timestamp'])

            # Keep the oldest
            new_inventory.append(backups[0])

            # Mark others for deletion
            for backup in backups[1:]:
                to_delete.append(backup)

        # Delete physical files
        deleted_count = 0
        for backup in to_delete:
            backup_path = Path(backup['backup_path'])
            if backup_path.exists():
                backup_path.unlink()
                deleted_count += 1

        # Save updated inventory
        self._save_inventory(new_inventory)

        return deleted_count, len(new_inventory)


# ============================================================================
# Frontmatter Parser Module
# ============================================================================

class FrontmatterParser:
    """Parses YAML frontmatter without external dependencies"""

    @staticmethod
    def extract_frontmatter(content: str) -> Tuple[Optional[str], str]:
        """
        Extract frontmatter and remaining content.

        Returns:
            Tuple of (frontmatter_text, remaining_content)
            Returns (None, content) if no frontmatter found
        """
        lines = content.splitlines()

        if not lines or lines[0].strip() != '---':
            return None, content

        # Find closing ---
        for i, line in enumerate(lines[1:], start=1):
            if line.strip() == '---':
                fm_text = '\n'.join(lines[1:i])
                remaining = '\n'.join(lines[i+1:])
                return fm_text, remaining

        return None, content

    @staticmethod
    def parse_field(frontmatter: str, field_name: str) -> Optional[Any]:
        """
        Parse a single field from frontmatter.

        Supports:
        - Inline: field: value
        - Inline list: field: [a, b, c]
        - Block list:
          field:
            - a
            - b
        """
        lines = frontmatter.splitlines()
        values = []

        for i, line in enumerate(lines):
            line_stripped = line.strip()

            # Check for inline field
            if line_stripped.startswith(f'{field_name}:'):
                # Check for inline list: [a, b, c]
                inline_match = re.search(r'\[(.*?)\]', line_stripped)
                if inline_match:
                    content = inline_match.group(1)
                    if content:
                        values = [x.strip() for x in content.split(',')]
                        return values if len(values) > 1 else (values[0] if values else None)
                else:
                    # Single value or block start
                    value_part = line_stripped[len(f'{field_name}:'):].strip()

                    # Check if it's a list start
                    if i + 1 < len(lines):
                        next_line = lines[i + 1].strip()
                        if next_line.startswith('-'):
                            # Block list - collect items
                            values = []
                            for j in range(i + 1, len(lines)):
                                item_line = lines[j].strip()
                                if item_line.startswith('-'):
                                    values.append(item_line[1:].strip())
                                elif item_line and ':' in item_line and not item_line.startswith(' '):
                                    # New field
                                    break
                                elif not item_line:
                                    continue
                            return values if values else None

                    # Single value
                    return value_part if value_part else None

        return values if values else None

    @staticmethod
    def parse_aliases(filepath: Path) -> List[str]:
        """Parse aliases from a file's frontmatter"""
        try:
            content = filepath.read_text(encoding='utf-8')
            fm, _ = FrontmatterParser.extract_frontmatter(content)

            if not fm:
                return []

            aliases = FrontmatterParser.parse_field(fm, 'aliases')
            return aliases if isinstance(aliases, list) else ([aliases] if aliases else [])
        except Exception:
            return []

    @staticmethod
    def parse_refs(filepath: Path) -> List[str]:
        """Parse ref field from frontmatter"""
        try:
            content = filepath.read_text(encoding='utf-8')
            fm, _ = FrontmatterParser.extract_frontmatter(content)

            if not fm:
                return []

            refs = FrontmatterParser.parse_field(fm, 'ref')
            return refs if isinstance(refs, list) else ([refs] if refs else [])
        except Exception:
            return []


# ============================================================================
# Term Scanner Module
# ============================================================================

class TermScanner:
    """Scans vocabulary and structure directories for terms"""

    def __init__(self, vocab_dir: Path = VOCAB_DIR, struct_dir: Path = STRUCT_DIR):
        self.vocab_dir = vocab_dir
        self.struct_dir = struct_dir

    def scan_terms(self) -> Dict[str, Path]:
        """
        Scan vocabulary and structure directories.

        Returns:
            Dictionary mapping lowercase term (or alias) -> vault relative path
        """
        terms: Dict[str, Path] = {}
        alias_candidates: List[Tuple[str, Path]] = []

        # Scan directories
        for base_dir in [self.vocab_dir, self.struct_dir]:
            if not base_dir.exists():
                continue

            for md_file in base_dir.rglob("*.md"):
                filename = md_file.stem

                # Skip files with | in name
                if '|' in filename:
                    continue

                # Get vault-relative path (without .md extension)
                rel_path = md_file.relative_to(VAULT_ROOT).with_suffix('')

                # Filename takes priority (main term)
                terms[filename.lower()] = rel_path

                # Collect aliases for second pass
                aliases = FrontmatterParser.parse_aliases(md_file)
                for alias in aliases:
                    if alias:
                        alias_candidates.append((alias.lower(), rel_path))

        # Second pass: Add aliases only if they don't conflict with filenames
        for alias, path in alias_candidates:
            if alias not in terms:
                terms[alias] = path

        return terms


# ============================================================================
# HTML Table Parser Module
# ============================================================================

class HTMLTableParser(HTMLParser):
    """Parse HTML tables and convert to Markdown"""

    def __init__(self):
        super().__init__()
        self.rows: List[List[Dict[str, Any]]] = []
        self.current_row: List[Dict[str, Any]] = []
        self.current_cell: List[str] = []
        self.in_table = False
        self.in_row = False
        self.in_cell = False
        self.cell_tag: Optional[str] = None

    def handle_starttag(self, tag: str, attrs: List[Tuple[str, Optional[str]]]) -> None:
        if tag == 'table':
            self.in_table = True
            self.rows = []
        elif tag == 'tr' and self.in_table:
            self.in_row = True
            self.current_row = []
        elif tag in ('td', 'th') and self.in_row:
            self.in_cell = True
            self.cell_tag = tag
            self.current_cell = []

    def handle_endtag(self, tag: str) -> None:
        if tag == 'table':
            self.in_table = False
        elif tag == 'tr' and self.in_row:
            self.in_row = False
            if self.current_row:
                self.rows.append(self.current_row)
        elif tag in ('td', 'th') and self.in_cell:
            self.in_cell = False
            cell_text = ''.join(self.current_cell).strip()
            self.current_row.append({
                'text': cell_text,
                'is_header': self.cell_tag == 'th'
            })

    def handle_data(self, data: str) -> None:
        if self.in_cell:
            self.current_cell.append(data)


def convert_html_tables(content: str) -> Tuple[str, int]:
    """Convert HTML tables to Markdown format

    Returns:
        Tuple of (converted_content, table_count)
    """
    pattern = re.compile(r'<table>.*?</table>', re.DOTALL | re.IGNORECASE)
    matches = list(pattern.finditer(content))

    if not matches:
        return content, 0

    new_content = content
    for match in reversed(matches):  # Reverse to maintain indices
        html_table = match.group(0)
        parser = HTMLTableParser()
        parser.feed(html_table)

        if not parser.rows:
            continue

        # Build markdown table
        md_lines = []
        for i, row in enumerate(parser.rows):
            cells = [cell['text'] for cell in row]
            md_line = '| ' + ' | '.join(cells) + ' |'
            md_lines.append(md_line)

            # Add separator after header row
            if i == 0:
                separator = '| ' + ' | '.join(['---'] * len(cells)) + ' |'
                md_lines.append(separator)

        md_table = '\n'.join(md_lines)
        new_content = new_content[:match.start()] + md_table + new_content[match.end():]

    return new_content, len(matches)


# ============================================================================
# Quote Cleaner Module
# ============================================================================

QUOTE_REPLACEMENTS = {
    "\u2018": "'",  # Left single
    "\u2019": "'",  # Right single
    "\u201A": "'",  # Single low-9
    "\u201B": "'",  # Single high-reversed-9
    "\u201C": '"',  # Left double
    "\u201D": '"',  # Right double
    "\u201E": '"',  # Double low-9
    "\u201F": '"',  # Double high-reversed-9
}


def clean_quotes(content: str) -> Tuple[str, int]:
    """Replace curly quotes with straight quotes

    Returns:
        Tuple of (cleaned_content, replacement_count)
    """
    count = sum(content.count(curly) for curly in QUOTE_REPLACEMENTS.keys())
    if count == 0:
        return content, 0

    cleaned = content
    for curly, straight in QUOTE_REPLACEMENTS.items():
        cleaned = cleaned.replace(curly, straight)

    return cleaned, count


# ============================================================================
# Link Processor Module
# ============================================================================

class LinkProcessor:
    """Processes markdown links for vocabulary and structure terms"""

    def __init__(self, terms_map: Dict[str, Path]):
        self.terms_map = terms_map
        # Sort by length (descending) for proper matching
        self.sorted_terms = sorted(terms_map.keys(), key=len, reverse=True)
        # Escape terms for regex
        self.escaped_terms = [re.escape(t) for t in self.sorted_terms]

    def strip_existing_links(self, content: str) -> str:
        """
        Remove all wikilinks and markdown links pointing to 20_Vocabulary or 30_Structures.

        Returns:
            Content with links removed (text only)
        """
        # Wikilinks with pipe: [[20_Vocabulary/term|alias]] -> alias
        content = re.sub(
            r'\[\[(?:20_Vocabulary|30_Structures)/[^\]|]+\|([^\]]+)\]\]',
            r'\1',
            content
        )

        # Simple wikilinks: [[20_Vocabulary/term]] -> term
        content = re.sub(
            r'\[\[(?:20_Vocabulary|30_Structures)/([^\]]+)\]\]',
            r'\1',
            content
        )

        # Markdown links: [alias](20_Vocabulary/term.md) -> alias
        content = re.sub(
            r'\[([^\]]+)\]\((?:20_Vocabulary|30_Structures)/[^\)]+\)',
            r'\1',
            content
        )

        return content

    def process_content(self, content: str) -> Tuple[str, List[str]]:
        """
        Process content to add wikilinks for vocabulary and structure terms.

        Returns:
            Tuple of (processed_content, changes_made)
        """
        lines = content.splitlines(keepends=True)
        changes_made: List[str] = []
        new_lines = []

        # Build regex pattern to match existing links OR our terms
        pattern_str = (
            r"(\[\[.*?\]\])|"  # Wikilinks
            r"(\[[^\]]*?\]\([^\)]*?\))|"  # MD links
            r"(\b(?:" + "|".join(self.escaped_terms) + r")\b)"  # Terms
        )
        regex = re.compile(pattern_str, re.IGNORECASE)

        for line in lines:
            is_table_row = line.lstrip().startswith('|')

            def replace_func(match: re.Match) -> str:
                g1 = match.group(1)  # Wikilink
                g2 = match.group(2)  # MD link
                g3 = match.group(3)  # Term match

                if g1:
                    return g1
                if g2:
                    return g2
                if g3:
                    original_text = g3
                    lower_text = original_text.lower()

                    if lower_text in self.terms_map:
                        rel_path = self.terms_map[lower_text]
                        separator = "\\|" if is_table_row else "|"

                        # Use piped link for alias support
                        new_text = f"[[{rel_path}{separator}{original_text}]]"
                        changes_made.append(f"'{original_text}' -> '{new_text}'")
                        return new_text

                    return original_text

                return match.group(0)

            new_line = regex.sub(replace_func, line)
            new_lines.append(new_line)

        return ''.join(new_lines), changes_made


# ============================================================================
# Phase Tagger Module
# ============================================================================

class PhaseTagger:
    """Adds phase-based flashcard tags from ref field"""

    PHASE_MAPPING = {
        '01-foundation': [1, 10],
        '02-activation': [2, 3, 4],
        '03-differentiation': [6, 11, 12],
        '04-mastery': [5, 7, 8],
        '05-addition': [9]
    }

    @staticmethod
    def convert_ref_to_tag(ref_text: str) -> str:
        """Convert ref to base tag"""
        clean_text = re.sub(r'\[\[|\]\]', '', ref_text).strip()
        tag_text = clean_text.lower().replace(' ', '-')
        return f"#flashcards/{tag_text}"

    @staticmethod
    def get_phase_mapping(base_tag: str) -> Dict[int, str]:
        """Get mapping of card numbers to phase tags"""
        card_map = {}
        for phase_suffix, card_nums in PhaseTagger.PHASE_MAPPING.items():
            full_tag = f"{base_tag}/{phase_suffix}"
            for card_num in card_nums:
                card_map[card_num] = full_tag
        return card_map

    def add_ref_tags(self, filepath: Path, dry_run: bool = True) -> ProcessResult:
        """Add phase-based tags to a vocabulary file"""
        refs = FrontmatterParser.parse_refs(filepath)

        if not refs:
            return ProcessResult(
                success=False,
                message="No refs found"
            )

        base_tag = self.convert_ref_to_tag(refs[0])
        card_map = self.get_phase_mapping(base_tag)

        try:
            content = filepath.read_text(encoding='utf-8')
        except Exception as e:
            return ProcessResult(
                success=False,
                message=f"Error reading file: {e}"
            )

        if not content:
            return ProcessResult(
                success=False,
                message="Empty file"
            )

        # Remove old header tag if present
        lines = content.splitlines()
        new_lines = []
        tag_removed = False

        for line in lines:
            if not tag_removed and line.strip().startswith('#flashcards') and base_tag in line:
                # Check if already has phase tags
                if re.search(re.escape(base_tag) + r'/\d{2}-', line):
                    return ProcessResult(
                        success=False,
                        message="Already has phase tags"
                    )
                # Remove the tag line
                parts = line.split()
                new_parts = [p for p in parts if base_tag not in p]
                if new_parts:
                    new_lines.append(' '.join(new_parts))
                tag_removed = True
            else:
                new_lines.append(line)

        content = '\n'.join(new_lines)

        # Inject phase tags before card headers
        card_pattern = re.compile(
            r'(?m)^(?:(?P<tag>#flashcards/[^\n]+)\n)?(?P<card>### Card (?P<num>\d+)(?:.|$))'
        )

        def replace_card_header(match: re.Match) -> str:
            existing_tag_line = match.group('tag')
            card_header = match.group('card')
            card_num = int(match.group('num'))

            if card_num in card_map:
                desired_tag = card_map[card_num]

                if existing_tag_line and desired_tag in existing_tag_line:
                    return match.group(0)

                return f"{desired_tag}\n{card_header}"
            return match.group(0)

        new_content = card_pattern.sub(replace_card_header, content)

        if content == new_content and not tag_removed:
            return ProcessResult(
                success=False,
                message="No changes needed"
            )

        if dry_run:
            return ProcessResult(
                success=True,
                message=f"Would add phase tags for {base_tag}"
            )

        try:
            filepath.write_text(new_content, encoding='utf-8')
            return ProcessResult(
                success=True,
                message=f"Added phase tags for {base_tag}"
            )
        except Exception as e:
            return ProcessResult(
                success=False,
                message=f"Error writing file: {e}"
            )


# ============================================================================
# File Processor Module
# ============================================================================

class FileProcessor:
    """Main orchestrator for file processing"""

    def __init__(
        self,
        terms_map: Dict[str, Path],
        backup_manager: BackupManager,
        backup_mode: BackupMode = BackupMode.ORIGINAL
    ):
        self.terms_map = terms_map
        self.backup_manager = backup_manager
        self.backup_mode = backup_mode
        self.link_processor = LinkProcessor(terms_map)

    def process_file(
        self,
        filepath: Path,
        dry_run: bool = True,
        strip_links: bool = True,
        clean_quotes_flag: bool = True,
        convert_tables: bool = True
    ) -> ProcessResult:
        """Process a single file

        Returns:
            ProcessResult with success status and message
        """
        filepath = filepath.resolve()

        try:
            content = filepath.read_text(encoding='utf-8')
        except Exception as e:
            return ProcessResult(
                success=False,
                message=f"Error reading file: {e}"
            )

        changes: List[str] = []

        # Step 1: Convert HTML tables
        if convert_tables:
            content, table_count = convert_html_tables(content)
            if table_count > 0:
                changes.append(f"Converted {table_count} HTML table(s)")

        # Step 2: Clean quotes
        if clean_quotes_flag:
            content, quote_count = clean_quotes(content)
            if quote_count > 0:
                changes.append(f"Cleaned {quote_count} curly quote(s)")

        # Step 3: Strip existing links
        if strip_links:
            stripped_content = self.link_processor.strip_existing_links(content)
            if stripped_content != content:
                content = stripped_content
                changes.append("Stripped existing vocab links")

        # Step 4: Create new links
        content, link_changes = self.link_processor.process_content(content)
        if link_changes:
            changes.extend(link_changes)

        if not any('Converted' in c or 'Cleaned' in c or 'Stripped' in c or '->' in c for c in changes):
            return ProcessResult(
                success=True,
                message="No changes needed",
                changes_count=0
            )

        if dry_run:
            unique_changes = sorted(list(set(link_changes)))[:50]
            change_summary = f"Found {len(link_changes)} terms to link"
            if len(link_changes) > 50:
                change_summary += f" (showing first 50)"
            return ProcessResult(
                success=True,
                message=change_summary,
                changes_count=len(link_changes)
            )

        # Create backup
        backup_id = self.backup_manager.create_backup(
            filepath,
            changes,
            mode=self.backup_mode
        )

        # Write changes
        try:
            filepath.write_text(content, encoding='utf-8')
            return ProcessResult(
                success=True,
                message=f"Linked {len(link_changes)} terms",
                backup_id=backup_id,
                changes_count=len(link_changes)
            )
        except Exception as e:
            return ProcessResult(
                success=False,
                message=f"Error writing file: {e}"
            )


# ============================================================================
# Main CLI
# ============================================================================

def find_vault_root() -> Path:
    """Find vault root by looking for .obsidian folder"""
    current = Path.cwd()

    # Check if we're in repo root (above glean)
    if (current / "glean" / ".obsidian").exists():
        return current / "glean"

    # Search upward for .obsidian
    while current != current.parent:
        if (current / ".obsidian").exists():
            return current
        current = current.parent

    return Path.cwd()


def resolve_path(path_str: str, is_folder: bool = False) -> Optional[Path]:
    """Resolve a path string to a Path object"""
    # Check as-is
    path = Path(path_str).resolve()
    if path.exists():
        return path

    # Check relative to vault root
    vault_root = find_vault_root()
    vault_path = (vault_root / path_str).resolve()
    if vault_path.exists():
        return vault_path

    # Search for file name in vault
    if not is_folder:
        matches = list(vault_root.rglob(path_str))
        if len(matches) == 1:
            return matches[0]

    return None


def main():
    parser = argparse.ArgumentParser(
        description="Auto-link vocabulary in Obsidian Markdown files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Dry run (preview changes)
  python3 auto_link_vocab.py --file "article.md"

  # Process file with original backup mode (default)
  python3 auto_link_vocab.py --file "article.md" --no-dry-run

  # Process folder with session backup mode
  python3 auto_link_vocab.py --folder "10_Sources/Articles" --backup-mode session --no-dry-run

  # Process with phase tagging
  python3 auto_link_vocab.py --folder "20_Vocabulary" --add-ref-tags --no-dry-run

  # List backups
  python3 auto_link_vocab.py --list-backups

  # Restore from backup
  python3 auto_link_vocab.py --restore 20251220_120000_abc123

  # Restore to original
  python3 auto_link_vocab.py --restore-original "article.md"
        """
    )

    # Target selection
    parser.add_argument('--file', help='Process a single file')
    parser.add_argument('--folder', help='Process all .md files in folder')

    # Backup options
    parser.add_argument(
        '--backup-mode',
        choices=['original', 'session', 'off'],
        default='original',
        help='Backup strategy: original (keep first), session (per run), off (no backup)'
    )

    # Processing options
    parser.add_argument('--dry-run', action='store_true', default=True,
                       help='Preview changes without modifying files (default)')
    parser.add_argument('--no-dry-run', action='store_true',
                       help='Apply changes to files')
    parser.add_argument('--strip-links', action='store_true', default=True,
                       help='Strip existing vocab links before re-linking (default)')
    parser.add_argument('--no-strip-links', action='store_true',
                       help='Keep existing links and add new ones')
    parser.add_argument('--no-clean-quotes', action='store_true',
                       help='Skip cleaning curly quotes')

    # Phase tagging
    parser.add_argument('--add-ref-tags', action='store_true',
                       help='Add phase-based flashcard tags from ref field')

    # Restore options
    parser.add_argument('--list-backups', nargs='?', const='',
                       help='List backups, optionally filter by path')
    parser.add_argument('--restore', metavar='ID',
                       help='Restore from specific backup ID')
    parser.add_argument('--restore-all', metavar='PREFIX',
                       help='Restore all backups from a session')
    parser.add_argument('--restore-original', metavar='PATH',
                       help='Restore file(s) to their oldest backup')

    # Cleanup
    parser.add_argument('--cleanup-backups', action='store_true',
                       help='Remove redundant backups, keep only originals')

    args = parser.parse_args()

    # Determine dry run
    dry_run = not args.no_dry_run

    # Initialize backup manager
    backup_manager = BackupManager()
    backup_mode = BackupMode(args.backup_mode)

    # Handle restore/list/cleanup operations
    if args.list_backups is not None:
        filter_path = resolve_path(args.list_backups) if args.list_backups else None
        backups = backup_manager.list_backups(filter_path)

        if not backups:
            print("No backups found")
            return

        print(f"{'ID':<25} | {'Date':<20} | {'File':<40} | {'Changes'}")
        print("-" * 100)
        for entry in backups:
            ts = datetime.strptime(entry.timestamp, "%Y%m%d_%H%M%S")
            ts_str = ts.strftime("%Y-%m-%d %H:%M:%S")
            filename = Path(entry.original_path).name
            print(f"{entry.id:<25} | {ts_str:<20} | {filename:<40} | {entry.changes_count}")
        print("-" * 100)
        print(f"Total: {len(backups)} backup(s)")
        return

    if args.restore:
        result = backup_manager.restore_backup(args.restore)
        if result.success:
            print(f"✅ {result.message}")
        else:
            print(f"❌ {result.message}")
        return

    if args.restore_all:
        success, total = backup_manager.restore_session(args.restore_all)
        print(f"Restored {success}/{total} files from session '{args.restore_all}'")
        return

    if args.restore_original:
        path = resolve_path(args.restore_original, is_folder=True)
        if not path:
            print(f"❌ Path not found: {args.restore_original}")
            return

        success, total = backup_manager.restore_to_original(path)
        print(f"Restored {success}/{total} files to original")
        return

    if args.cleanup_backups:
        deleted, remaining = backup_manager.cleanup_redundant()
        print(f"Deleted {deleted} redundant backup(s)")
        print(f"Kept {remaining} original backup(s)")
        return

    # Handle phase tagging
    if args.add_ref_tags:
        target_path = None
        if args.file:
            target_path = resolve_path(args.file)
        elif args.folder:
            target_path = resolve_path(args.folder, is_folder=True)
        else:
            target_path = VOCAB_DIR

        if not target_path:
            print("❌ Target path not found")
            return

        files = []
        if target_path.is_file():
            files = [target_path]
        else:
            files = list(target_path.rglob("*.md"))

        tagger = PhaseTagger()
        success_count = 0
        skip_count = 0

        print(f"Processing {len(files)} file(s) for phase tagging...")
        for filepath in sorted(files):
            result = tagger.add_ref_tags(filepath, dry_run=dry_run)
            if result.success:
                print(f"✅ {filepath.name}")
                print(f"   {result.message}")
                success_count += 1
            else:
                if "already" in result.message.lower() or "no refs" in result.message.lower():
                    skip_count += 1
                else:
                    print(f"⚠️  {filepath.name}: {result.message}")

        print(f"\nSummary: {success_count} updated, {skip_count} skipped")
        if dry_run:
            print("Run with --no-dry-run to apply changes")
        return

    # Determine target files for linking
    target_files: List[Path] = []
    if args.file:
        target_path = resolve_path(args.file)
        if target_path:
            target_files = [target_path]
        else:
            print(f"❌ File not found: {args.file}")
            return
    elif args.folder:
        target_path = resolve_path(args.folder, is_folder=True)
        if target_path:
            target_files = list(target_path.rglob("*.md"))
        else:
            print(f"❌ Folder not found: {args.folder}")
            return
    else:
        # Default to articles dir
        if ARTICLES_DIR.exists():
            target_files = list(ARTICLES_DIR.rglob("*.md"))
        else:
            print("❌ Articles directory not found")
            return

    # Scan terms
    scanner = TermScanner()
    terms_map = scanner.scan_terms()

    print(f"Scanned {len(terms_map)} terms from vocabulary/structure")

    # Process files
    strip_links = not args.no_strip_links
    clean_quotes_flag = not args.no_clean_quotes

    processor = FileProcessor(
        terms_map,
        backup_manager,
        backup_mode=backup_mode
    )

    print(f"Processing {len(target_files)} file(s)...")
    if dry_run:
        print("(Dry run mode - no changes will be made)")

    success_count = 0
    skip_count = 0

    for filepath in target_files:
        result = processor.process_file(
            filepath,
            dry_run=dry_run,
            strip_links=strip_links,
            clean_quotes_flag=clean_quotes_flag
        )

        if result.success:
            if result.changes_count > 0:
                print(f"✅ {filepath.name}")
                print(f"   {result.message}")
                if result.backup_id:
                    print(f"   Backup: {result.backup_id}")
                success_count += 1
            else:
                skip_count += 1
        else:
            print(f"❌ {filepath.name}: {result.message}")

    print(f"\nSummary: {success_count} modified, {skip_count} unchanged")

    if dry_run:
        print("Run with --no-dry-run to apply changes")


if __name__ == "__main__":
    main()
