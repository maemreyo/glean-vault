#!/usr/bin/env python3
"""
Cleanup Backups Script

Keeps only the earliest (oldest) backup for each unique file in the inventory,
deleting all newer backups to save space.
"""

import os
import json
import shutil
from pathlib import Path
from datetime import datetime

# Configuration
VAULT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
BACKUP_DIR = os.path.join(VAULT_ROOT, "99_Tools/backups")
INVENTORY_FILE = os.path.join(BACKUP_DIR, "inventory.json")

def load_inventory():
    if not os.path.exists(INVENTORY_FILE):
        return []
    try:
        with open(INVENTORY_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading inventory: {e}")
        return []

def save_inventory(inventory):
    try:
        with open(INVENTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(inventory, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Error saving inventory: {e}")

def cleanup_backups(dry_run=True):
    inventory = load_inventory()
    if not inventory:
        print("No backups found in inventory.")
        return

    # Group backups by original_path
    groups = {}
    for entry in inventory:
        path = entry.get('original_path')
        if not path:
            continue
        if path not in groups:
            groups[path] = []
        groups[path].append(entry)

    to_keep = []
    to_delete = []
    
    print(f"Total files in inventory: {len(groups)}")
    print(f"Total backup entries: {len(inventory)}")
    print("-" * 40)

    for path, entries in groups.items():
        # Sort by timestamp (ascending)
        # Assuming timestamp format is YYYYMMDD_HHMMSS
        sorted_entries = sorted(entries, key=lambda x: x.get('timestamp', ''))
        
        # Keep the oldest one
        oldest = sorted_entries[0]
        to_keep.append(oldest)
        
        # Mark others for deletion
        others = sorted_entries[1:]
        to_delete.extend(others)

    print(f"Entries to keep: {len(to_keep)}")
    print(f"Entries to delete: {len(to_delete)}")
    
    if not to_delete:
        print("Nothing to clean up.")
        return

    if dry_run:
        print("\n[DRY RUN] Would delete the following physical files:")
        for entry in to_delete[:10]:
            print(f"  - {os.path.basename(entry['backup_path'])}")
        if len(to_delete) > 10:
            print(f"  ... and {len(to_delete) - 10} more.")
        print("\nUse --no-dry-run to actually delete files and update inventory.")
    else:
        print("\nDeleting physical files...")
        deleted_count = 0
        for entry in to_delete:
            backup_path = entry.get('backup_path')
            if backup_path and os.path.exists(backup_path):
                try:
                    os.remove(backup_path)
                    deleted_count += 1
                except Exception as e:
                    print(f"  Error deleting {backup_path}: {e}")
            else:
                # Even if file is missing, we'll remove it from inventory
                pass
        
        print(f"Successfully deleted {deleted_count} files.")
        
        # Update and save inventory
        save_inventory(to_keep)
        print("Inventory updated.")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Cleanup backups but keep the oldest version of each file.")
    parser.add_argument("--no-dry-run", action="store_true", help="Actually perform the cleanup")
    args = parser.parse_args()
    
    cleanup_backups(dry_run=not args.no_dry_run)
