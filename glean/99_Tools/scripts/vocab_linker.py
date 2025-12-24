#!/usr/bin/env python3
"""
Vocabulary Linking Assistant - Interactive Menu

Provides user-friendly interface for auto-linking vocabulary in Obsidian vault.
Supports OpenCode integration via custom commands.
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from typing import Dict, Any, List, Optional
import re

# Configuration
VAULT_ROOT = Path(__file__).parent.parent.resolve()
SCRIPT_PATH = VAULT_ROOT / "scripts" / "auto_link_vocab.py"
CONFIG_FILE = VAULT_ROOT / "99_Tools" / "scripts" / "vocab_linker_config.json"


class Config:
    """Configuration management for vocab linker"""

    DEFAULT_CONFIG = {
        "backup_mode": "original",
        "default_folder": "glean/10_Sources/Articles",
        "clean_quotes": True,
        "strip_links": True,
        "last_file": "",
        "last_folder": "",
        "remember_settings": True
    }

    def __init__(self):
        self.config = self.load_config()

    def load_config(self) -> Dict:
        """Load config from file or return defaults"""
        if CONFIG_FILE.exists():
            try:
                with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                    return {**self.DEFAULT_CONFIG, **json.load(f)}
            except (json.JSONDecodeError, Exception):
                return self.DEFAULT_CONFIG.copy()
        return self.DEFAULT_CONFIG.copy()

    def save_config(self) -> None:
        """Save config to file"""
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=2)

    def get(self, key: str, default: Any = None) -> Any:
        """Get config value"""
        if key in self.config:
            return self.config[key]
        return self.DEFAULT_CONFIG.get(key, default)

    def set(self, key: str, value) -> None:
        """Set config value and save if remember_settings is enabled"""
        self.config[key] = value
        if self.config.get("remember_settings", True):
            self.save_config()

    def get_backup_mode_display(self) -> str:
        """Get human-readable backup mode"""
        mode = self.get("backup_mode", "original")
        if not isinstance(mode, str):
            mode = "original"
        mode_map = {
            "original": "Original (keep first only)",
            "session": "Session (per-run)",
            "off": "Off (no backup)"
        }
        return mode_map.get(mode, f"Unknown ({mode})")


class Colors:
    """ANSI color codes for terminal output"""

    HEADER = "\033[95m"      # Light magenta
    OKBLUE = "\033[94m"       # Light blue
    OKGREEN = "\033[92m"      # Light green
    WARNING = "\033[93m"      # Light yellow
    FAIL = "\033[91m"         # Light red
    ENDC = "\033[0m"          # Reset
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def print_header(text: str) -> None:
    """Print formatted header"""
    print(f"{Colors.HEADER}{Colors.BOLD}{text}{Colors.ENDC}")
    print(f"{Colors.HEADER}{'=' * len(text)}{Colors.ENDC}\n")


def print_success(text: str) -> None:
    """Print success message"""
    print(f"{Colors.OKGREEN}✓ {text}{Colors.ENDC}")


def print_error(text: str) -> None:
    """Print error message"""
    print(f"{Colors.FAIL}✗ {text}{Colors.ENDC}")


def print_warning(text: str) -> None:
    """Print warning message"""
    print(f"{Colors.WARNING}⚠ {text}{Colors.ENDC}")


def print_info(text: str) -> None:
    """Print info message"""
    print(f"{Colors.OKBLUE}ℹ {text}{Colors.ENDC}")


def resolve_path(path_str: str, must_exist: bool = True) -> Optional[Path]:
    """Resolve path relative to vault root"""
    # Try absolute
    path = Path(path_str)
    if path.is_absolute():
        if not must_exist or path.exists():
            return path
        return None

    # Try relative to vault root
    path = VAULT_ROOT / path_str
    if not must_exist or path.exists():
        return path

    return None


def run_script(args: List[str], dry_run: bool = False) -> subprocess.CompletedProcess:
    """Run auto_link_vocab_v2.py script"""
    final_args = ["python3", str(SCRIPT_PATH)] + args
    if dry_run:
        final_args.append("--dry-run")

    print_info(f"Running: {' '.join(final_args)}")

    result = subprocess.run(
        final_args,
        capture_output=True,
        text=True,
        cwd=str(VAULT_ROOT)
    )
    return result


def confirm(message: str) -> bool:
    """Ask for user confirmation"""
    while True:
        response = input(f"{Colors.BOLD}{message} (y/n): {Colors.ENDC}").strip().lower()
        if response in ['y', 'yes']:
            return True
        elif response in ['n', 'no']:
            return False
        print_warning("Please enter 'y' or 'n'")


def menu_link_single_file(config: Config) -> None:
    """Menu option 1: Link a single file"""
    print_header("Link a Single File")

    # Get file path
    default_path = config.get("last_file", "")
    if default_path:
        prompt = f"Enter file path (default: {default_path}): "
    else:
        prompt = "Enter file path: "

    path_str = input(prompt).strip()
    if not path_str and default_path:
        path_str = default_path

    if not path_str:
        print_error("No file path provided")
        return

    path = resolve_path(path_str)
    if not path:
        print_error(f"File not found: {path_str}")
        return

    config.set("last_file", str(path.relative_to(VAULT_ROOT)))

    # Show dry-run
    print_info("Running dry-run first...")
    result = run_script(["--file", str(path), "--no-strip-links"], dry_run=True)
    print(result.stdout)
    if result.stderr:
        print(result.stderr)

    # Ask to apply
    if confirm("Do you want to apply these changes?"):
        print_info("Applying changes...")
        result = run_script([
            "--file", str(path),
            "--no-dry-run",
            "--backup-mode", config.get("backup_mode", "original")
        ])
        print(result.stdout)
        if result.stderr:
            print(result.stderr)
        print_success("File processed successfully")
    else:
        print_warning("Changes not applied")


def menu_link_folder(config: Config) -> None:
    """Menu option 2: Link entire folder"""
    print_header("Link Entire Folder")

    # Get folder path
    default_path = config.get("last_folder", "")
    if default_path:
        prompt = f"Enter folder path (default: {default_path}): "
    else:
        prompt = "Enter folder path: "

    path_str = input(prompt).strip()
    if not path_str and default_path:
        path_str = default_path

    if not path_str:
        print_error("No folder path provided")
        return

    path = resolve_path(path_str)
    if not path:
        print_error(f"Folder not found: {path_str}")
        return

    config.set("last_folder", str(path.relative_to(VAULT_ROOT)))

    # Show dry-run
    print_info("Running dry-run first...")
    result = run_script(["--folder", str(path), "--no-strip-links"], dry_run=True)
    print(result.stdout)
    if result.stderr:
        print(result.stderr)

    # Ask to apply
    if confirm("Do you want to apply these changes?"):
        print_info("Applying changes...")
        result = run_script([
            "--folder", str(path),
            "--no-dry-run",
            "--backup-mode", config.get("backup_mode", "original")
        ])
        print(result.stdout)
        if result.stderr:
            print(result.stderr)
        print_success("Folder processed successfully")
    else:
        print_warning("Changes not applied")


def menu_list_backups(config: Config) -> None:
    """Menu option 3: List all backups"""
    print_header("List All Backups")

    result = run_script(["--list-backups"])
    print(result.stdout)
    if result.stderr:
        print(result.stderr)


def menu_restore_backup(config: Config) -> None:
    """Menu option 4: Restore from backup ID"""
    print_header("Restore from Backup ID")

    # List backups first
    print_info("Listing available backups...")
    result = run_script(["--list-backups"])
    print(result.stdout)

    backup_id = input("\nEnter backup ID to restore (leave empty to cancel): ").strip()
    if not backup_id:
        print_info("Operation cancelled")
        return

    if confirm(f"Restore backup {backup_id}?"):
        result = run_script(["--restore", backup_id])
        print(result.stdout)
        if result.stderr:
            print(result.stderr)
        print_success("Restore completed")
    else:
        print_warning("Restore cancelled")


def menu_restore_original(config: Config) -> None:
    """Menu option 5: Restore to original"""
    print_header("Restore to Original (Oldest Backup)")

    path_str = input("Enter file or folder path (leave empty for last folder): ").strip()

    if path_str:
        path = resolve_path(path_str)
        if not path:
            print_error(f"Path not found: {path_str}")
            return
    else:
        path_str = config.get("last_folder", "glean/10_Sources/Articles")
        path = VAULT_ROOT / path_str

    print_info(f"Restoring to original backup for: {path.relative_to(VAULT_ROOT)}")

    if confirm("Proceed with restore?"):
        result = run_script(["--restore-original", str(path)])
        print(result.stdout)
        if result.stderr:
            print(result.stderr)
        print_success("Restore completed")
    else:
        print_warning("Restore cancelled")


def menu_cleanup_backups(config: Config) -> None:
    """Menu option 6: Clean up redundant backups"""
    print_header("Clean Up Redundant Backups")

    # Show current status
    print_info("Checking current backup status...")
    result = run_script(["--list-backups"])

    backup_count = result.stdout.count('\n') - 3  # Approximate

    print(f"\nCurrent backups: ~{backup_count} files")
    print(f"Backup location: {VAULT_ROOT / '99_Tools' / 'backups'}")

    if backup_count < 10:
        print_info("Backup count is low. Cleanup may not be needed.")
        if not confirm("Continue anyway?"):
            return

    if confirm(f"Delete redundant backups and keep only originals?"):
        print_info("Cleaning up backups...")
        result = run_script(["--cleanup-backups"])
        print(result.stdout)
        if result.stderr:
            print(result.stderr)
        print_success("Cleanup completed")
    else:
        print_warning("Cleanup cancelled")


def menu_add_phase_tags(config: Config) -> None:
    """Menu option 7: Add phase tags to vocabulary"""
    print_header("Add Phase Tags to Vocabulary")

    path_str = input("Enter folder path (default: glean/20_Vocabulary): ").strip()

    if not path_str:
        path_str = "glean/20_Vocabulary"

    path = resolve_path(path_str)
    if not path:
        print_error(f"Folder not found: {path_str}")
        return

    print_info(f"Adding phase tags to: {path.relative_to(VAULT_ROOT)}")

    # Show dry-run
    result = run_script(["--folder", str(path), "--add-ref-tags"], dry_run=True)
    print(result.stdout)
    if result.stderr:
        print(result.stderr)

    if confirm("Do you want to apply these phase tags?"):
        result = run_script(["--folder", str(path), "--add-ref-tags", "--no-dry-run"])
        print(result.stdout)
        if result.stderr:
            print(result.stderr)
        print_success("Phase tags added")
    else:
        print_warning("Operation cancelled")


def menu_settings(config: Config) -> None:
    """Menu option 8: Settings"""
    print_header("Settings")

    while True:
        print("\nCurrent Settings:")
        print(f"  1. Backup mode: {config.get_backup_mode_display()}")
        print(f"  2. Default folder: {config.get('default_folder')}")
        print(f"  3. Clean quotes: {config.get('clean_quotes')}")
        print(f"  4. Strip links: {config.get('strip_links')}")
        print(f"  5. Remember settings: {config.get('remember_settings')}")
        print(f"  0. Back to main menu")

        choice = input("\nSelect setting to change (0-5): ").strip()

        if choice == "1":
            print("\nBackup modes:")
            print("  1. Original (keep first only) - saves space")
            print("  2. Session (per-run) - more history")
            print("  3. Off - no backup (dangerous)")
            mode_choice = input("Select mode (1-3): ").strip()

            mode_map = {"1": "original", "2": "session", "3": "off"}
            if mode_choice in mode_map:
                config.set("backup_mode", mode_map[mode_choice])
                print_success(f"Backup mode set to: {mode_map[mode_choice]}")
            else:
                print_error("Invalid choice")

        elif choice == "2":
            folder = input("Enter default folder path: ").strip()
            if folder:
                config.set("default_folder", folder)
                print_success(f"Default folder set to: {folder}")

        elif choice == "3":
            current = config.get("clean_quotes")
            new_val = not current
            config.set("clean_quotes", new_val)
            print_success(f"Clean quotes: {'enabled' if new_val else 'disabled'}")

        elif choice == "4":
            current = config.get("strip_links")
            new_val = not current
            config.set("strip_links", new_val)
            print_success(f"Strip links: {'enabled' if new_val else 'disabled'}")

        elif choice == "5":
            current = config.get("remember_settings")
            new_val = not current
            config.set("remember_settings", new_val)
            print_success(f"Remember settings: {'enabled' if new_val else 'disabled'}")

        elif choice == "0":
            return

        else:
            print_error("Invalid choice")


def show_main_menu(config: Config) -> None:
    """Display main menu"""
    os.system('clear' if os.name == 'posix' else 'cls')

    print_header("Vocabulary Linking Assistant")

    # Show current config
    print(f"{Colors.OKBLUE}Backup mode:{Colors.ENDC} {config.get_backup_mode_display()}")
    print(f"{Colors.OKBLUE}Default folder:{Colors.ENDC} {config.get('default_folder')}")
    print()

    print("Menu:")
    print("  1. Link a single file (keeps existing links)")
    print("  2. Link entire folder (keeps existing links)")
    print("  3. List all backups")
    print("  4. Restore from backup")
    print("  5. Restore to original")
    print("  6. Clean up redundant backups")
    print("  7. Add phase tags to vocabulary")
    print("  8. Settings")
    print("  0. Exit")
    print()


def main():
    """Main entry point"""
    config = Config()

    while True:
        show_main_menu(config)
        choice = input("Select option (0-8): ").strip()

        if choice == "1":
            menu_link_single_file(config)
        elif choice == "2":
            menu_link_folder(config)
        elif choice == "3":
            menu_list_backups(config)
        elif choice == "4":
            menu_restore_backup(config)
        elif choice == "5":
            menu_restore_original(config)
        elif choice == "6":
            menu_cleanup_backups(config)
        elif choice == "7":
            menu_add_phase_tags(config)
        elif choice == "8":
            menu_settings(config)
        elif choice == "0":
            print_success("Goodbye!")
            sys.exit(0)
        else:
            print_error("Invalid choice")

        input("\nPress Enter to continue...")


if __name__ == "__main__":
    # Check if script exists
    if not SCRIPT_PATH.exists():
        print_error(f"Script not found: {SCRIPT_PATH}")
        print_info("Please ensure auto_link_vocab_v2.py is in glean/99_Tools/scripts/")
        sys.exit(1)

    main()
