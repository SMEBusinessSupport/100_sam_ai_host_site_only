# Phase1 Safe Deprecation

**Original file:** `PHASE1_SAFE_DEPRECATION.py`
**Type:** PYTHON

---

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase 1: SAFE Model Deprecation Script
=======================================

CTO-Approved Strategy: Rename → Test → Delete

This script renames N8N duplication models with _PREPARE_TO_DELETE_ prefix.
If server restarts successfully, models can be deleted.
If server crashes, rollback is instant (just rename back).

Author: Anthony Gardiner - Odoo Consulting & Claude AI
Date: 2025-10-31
CTO Decision: Risk mitigation before deletion
"""

import os
import sys
import shutil
from datetime import datetime

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# Base path
BASE_PATH = r"C:\Working With AI\ai_sam\ai_sam\ai_brain\models"
BACKUP_DIR = r"C:\Working With AI\ai_sam\ai_sam\ai_brain\.deprecation_backup"

# Models to deprecate (6 N8N duplication models)
MODELS_TO_DEPRECATE = [
    'nodes.py',
    'connections.py',
    'n8n_node_types.py',
    'n8n_simple_nodes.py',
    'n8n_simple_extractor.py',
    'workflow_types.py',
]

# Known dependencies (from grep analysis)
KNOWN_DEPENDENCIES = {
    'nodes.py': [
        'canvas.py (line 100: node_ids One2many)',
        'ai_sam_workflows/controllers/node_type_mapper.py',
    ],
    'connections.py': [
        'canvas.py (connection_ids - to be verified)',
        'executions.py (possible reference)',
    ],
    'n8n_node_types.py': [
        'node_type_mapper.py (line 41: env["node_types"])',
        'nodes.py (node_type_id Many2one)',
    ],
    'n8n_simple_nodes.py': [
        'n8n_simple_extractor.py',
    ],
    'n8n_simple_extractor.py': [
        'ai_sam_workflows module (extraction scripts)',
    ],
    'workflow_types.py': [
        'canvas.py (workflow_type_id Many2one)',
    ],
}


def create_backup_dir():
    """Create backup directory if not exists"""
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)
        print(f"✅ Created backup directory: {BACKUP_DIR}")


def backup_file(filename):
    """Create timestamped backup before rename"""
    source = os.path.join(BASE_PATH, filename)
    if not os.path.exists(source):
        print(f"⚠️  WARNING: {filename} not found at {source}")
        return False

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_name = f"{filename}.backup_{timestamp}"
    backup_path = os.path.join(BACKUP_DIR, backup_name)

    shutil.copy2(source, backup_path)
    print(f"✅ Backed up: {filename} → {backup_name}")
    return True


def rename_to_deprecate(filename):
    """Rename file with _PREPARE_TO_DELETE_ prefix"""
    source = os.path.join(BASE_PATH, filename)
    new_name = f"_PREPARE_TO_DELETE_{filename}"
    target = os.path.join(BASE_PATH, new_name)

    if not os.path.exists(source):
        print(f"❌ ERROR: {filename} not found!")
        return False

    if os.path.exists(target):
        print(f"⚠️  WARNING: {new_name} already exists! Skipping.")
        return False

    os.rename(source, target)
    print(f"✅ Renamed: {filename} → {new_name}")
    return True


def rollback_rename(filename):
    """Rollback: Remove _PREPARE_TO_DELETE_ prefix"""
    new_name = f"_PREPARE_TO_DELETE_{filename}"
    source = os.path.join(BASE_PATH, new_name)
    target = os.path.join(BASE_PATH, filename)

    if not os.path.exists(source):
        print(f"❌ ERROR: {new_name} not found for rollback!")
        return False

    os.rename(source, target)
    print(f"✅ Rolled back: {new_name} → {filename}")
    return True


def print_dependency_report():
    """Print known dependencies report"""
    print("\n" + "=" * 80)
    print("KNOWN DEPENDENCIES REPORT")
    print("=" * 80)
    print("\n⚠️  These models have CONFIRMED dependencies that will break:\n")

    for model, deps in KNOWN_DEPENDENCIES.items():
        print(f"📄 {model}")
        for dep in deps:
            print(f"   └─ {dep}")
        print()

    print("=" * 80)
    print("NEXT STEPS AFTER RENAME:")
    print("=" * 80)
    print("1. Update ai_brain/models/__init__.py (comment out imports)")
    print("2. Restart Odoo server: python odoo-bin -c odoo.conf")
    print("3. Watch for import errors in logs")
    print("4. If server crashes, run: python PHASE1_SAFE_DEPRECATION.py --rollback")
    print("5. If server starts, fix dependencies, then run: python PHASE1_SAFE_DEPRECATION.py --delete")
    print("=" * 80)


def main_deprecate():
    """Main deprecation workflow"""
    print("\n" + "=" * 80)
    print("PHASE 1: SAFE MODEL DEPRECATION")
    print("=" * 80)
    print(f"\nTarget: {len(MODELS_TO_DEPRECATE)} N8N duplication models")
    print(f"Strategy: Rename with _PREPARE_TO_DELETE_ prefix")
    print(f"Risk: LOW (instant rollback available)\n")

    # Create backup directory
    create_backup_dir()

    # Show dependency report FIRST
    print_dependency_report()

    # Confirm action
    print("\n⚠️  WARNING: This will rename models and BREAK imports!")
    print("💡 TIP: Keep this terminal open for rollback instructions.\n")
    confirm = input("Continue with rename? (yes/no): ").strip().lower()

    if confirm != 'yes':
        print("❌ Aborted by user.")
        return

    print("\n" + "=" * 80)
    print("STARTING DEPRECATION...")
    print("=" * 80 + "\n")

    success_count = 0
    for filename in MODELS_TO_DEPRECATE:
        print(f"\n📄 Processing: {filename}")

        # Backup first
        if not backup_file(filename):
            print(f"   ⚠️  Skipping {filename} (backup failed)")
            continue

        # Rename
        if rename_to_deprecate(filename):
            success_count += 1
        else:
            print(f"   ❌ Failed to rename {filename}")

    print("\n" + "=" * 80)
    print("DEPRECATION COMPLETE")
    print("=" * 80)
    print(f"\n✅ Successfully renamed: {success_count}/{len(MODELS_TO_DEPRECATE)} models")
    print(f"📁 Backups stored in: {BACKUP_DIR}\n")

    print("=" * 80)
    print("NEXT STEP: Update __init__.py")
    print("=" * 80)
    print("\nManually edit: ai_brain/models/__init__.py")
    print("\nComment out these imports:")
    for filename in MODELS_TO_DEPRECATE:
        model_name = filename.replace('.py', '')
        print(f"  # from . import {model_name}  # DEPRECATED 2025-10-31 - Phase 1")
    print("\nThen restart Odoo and watch for errors!")
    print("=" * 80 + "\n")


def main_rollback():
    """Rollback all renames"""
    print("\n" + "=" * 80)
    print("PHASE 1: ROLLBACK DEPRECATION")
    print("=" * 80)
    print("\n⚠️  This will restore all renamed models.\n")

    confirm = input("Continue with rollback? (yes/no): ").strip().lower()
    if confirm != 'yes':
        print("❌ Rollback aborted.")
        return

    print("\n" + "=" * 80)
    print("STARTING ROLLBACK...")
    print("=" * 80 + "\n")

    success_count = 0
    for filename in MODELS_TO_DEPRECATE:
        print(f"\n📄 Rolling back: {filename}")
        if rollback_rename(filename):
            success_count += 1

    print("\n" + "=" * 80)
    print("ROLLBACK COMPLETE")
    print("=" * 80)
    print(f"\n✅ Successfully restored: {success_count}/{len(MODELS_TO_DEPRECATE)} models\n")


def main_delete():
    """Final deletion (only after testing)"""
    print("\n" + "=" * 80)
    print("PHASE 1: FINAL DELETION")
    print("=" * 80)
    print("\n⚠️  WARNING: This will PERMANENTLY DELETE deprecated models!")
    print("⚠️  Only proceed if Odoo server started successfully after rename.\n")

    confirm = input("Have you tested Odoo restart? (yes/no): ").strip().lower()
    if confirm != 'yes':
        print("❌ Test Odoo restart first!")
        return

    confirm2 = input("Are dependencies fixed? (yes/no): ").strip().lower()
    if confirm2 != 'yes':
        print("❌ Fix dependencies before deletion!")
        return

    confirm3 = input("FINAL CONFIRMATION - Delete models permanently? (yes/no): ").strip().lower()
    if confirm3 != 'yes':
        print("❌ Deletion aborted.")
        return

    print("\n" + "=" * 80)
    print("STARTING DELETION...")
    print("=" * 80 + "\n")

    success_count = 0
    for filename in MODELS_TO_DEPRECATE:
        new_name = f"_PREPARE_TO_DELETE_{filename}"
        file_path = os.path.join(BASE_PATH, new_name)

        if not os.path.exists(file_path):
            print(f"⚠️  {new_name} not found (already deleted?)")
            continue

        os.remove(file_path)
        print(f"✅ Deleted: {new_name}")
        success_count += 1

    print("\n" + "=" * 80)
    print("DELETION COMPLETE")
    print("=" * 80)
    print(f"\n✅ Successfully deleted: {success_count} models")
    print(f"📁 Backups preserved in: {BACKUP_DIR}\n")


if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1:
        action = sys.argv[1].lower()
        if action == '--rollback':
            main_rollback()
        elif action == '--delete':
            main_delete()
        else:
            print("Usage:")
            print("  python PHASE1_SAFE_DEPRECATION.py           # Rename models")
            print("  python PHASE1_SAFE_DEPRECATION.py --rollback  # Undo rename")
            print("  python PHASE1_SAFE_DEPRECATION.py --delete    # Final deletion")
    else:
        main_deprecate()

```
