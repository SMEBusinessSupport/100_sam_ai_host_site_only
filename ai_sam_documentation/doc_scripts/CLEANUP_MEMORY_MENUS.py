#!/usr/bin/env python3
"""
CLEANUP SCRIPT: Remove Orphaned Memory Menus via Odoo ORM
===========================================================

This script safely removes orphaned memory-related menu items from the database
using Odoo's ORM (respects access rights, triggers, and constraints).

USAGE:
------
1. Stop Odoo server
2. Run this script:
   python "C:\Working With AI\ai_sam\ai_sam\CLEANUP_MEMORY_MENUS.py"
3. Start Odoo server
4. Refresh browser and verify menus are gone

"""

import sys
import os

# Add Odoo to Python path
sys.path.insert(0, r'C:\Program Files\Odoo 18\server')
os.chdir(r'C:\Program Files\Odoo 18\server')

import odoo
from odoo import api, SUPERUSER_ID

# Configuration
config_file = r'C:\Program Files\Odoo 18\server\odoo.conf'
database = 'ai_automator_db'

print("=" * 80)
print("  CLEANUP: Removing Orphaned Memory Menus")
print("=" * 80)
print()

# Load Odoo configuration
odoo.tools.config.parse_config(['-c', config_file])

# Get registry and environment
registry = odoo.registry(database)
with registry.cursor() as cr:
    env = api.Environment(cr, SUPERUSER_ID, {})

    print("[1/4] Searching for memory-related menus...")
    memory_menus = env['ir.ui.menu'].search([
        '|', '|', '|',
        ('name', 'ilike', 'memory'),
        ('name', 'ilike', 'import conversation'),
        ('name', 'ilike', 'extractor'),
        ('name', 'ilike', 'uninstall helper')
    ])

    if memory_menus:
        print(f"      Found {len(memory_menus)} memory-related menus:")
        for menu in memory_menus:
            print(f"      - [{menu.id}] {menu.name} (parent: {menu.parent_id.name if menu.parent_id else 'None'})")
    else:
        print("      No memory menus found (already clean!)")

    print()
    print("[2/4] Searching for memory-related actions (act_window)...")
    memory_actions = env['ir.actions.act_window'].search([
        '|', '|', '|',
        ('name', 'ilike', 'memory'),
        ('name', 'ilike', 'import conversation'),
        ('name', 'ilike', 'extractor'),
        ('res_model', 'in', ['ai.memory.config', 'ai.conversation.import', 'ai.extractor.plugin'])
    ])

    if memory_actions:
        print(f"      Found {len(memory_actions)} memory-related actions:")
        for action in memory_actions:
            print(f"      - [{action.id}] {action.name} (model: {action.res_model})")
    else:
        print("      No memory actions found (already clean!)")

    print()
    print("[3/4] Searching for memory-related actions (act_url)...")
    memory_url_actions = env['ir.actions.act_url'].search([
        '|',
        ('name', 'ilike', 'memory'),
        ('url', 'ilike', 'memory')
    ])

    if memory_url_actions:
        print(f"      Found {len(memory_url_actions)} memory URL actions:")
        for action in memory_url_actions:
            print(f"      - [{action.id}] {action.name} (url: {action.url})")
    else:
        print("      No memory URL actions found (already clean!)")

    print()
    print("[4/4] Deleting orphaned records...")

    total_deleted = 0

    if memory_menus:
        print(f"      Deleting {len(memory_menus)} menus...")
        memory_menus.unlink()
        total_deleted += len(memory_menus)

    if memory_actions:
        print(f"      Deleting {len(memory_actions)} actions...")
        memory_actions.unlink()
        total_deleted += len(memory_actions)

    if memory_url_actions:
        print(f"      Deleting {len(memory_url_actions)} URL actions...")
        memory_url_actions.unlink()
        total_deleted += len(memory_url_actions)

    # Commit changes
    cr.commit()

    print()
    print("=" * 80)
    if total_deleted > 0:
        print(f"  ✅ SUCCESS: Deleted {total_deleted} orphaned records")
    else:
        print("  ✅ SUCCESS: Database already clean (no orphaned records found)")
    print("=" * 80)
    print()
    print("Next steps:")
    print("1. Start Odoo server")
    print("2. Refresh browser (Ctrl+F5)")
    print("3. Verify memory menus are gone")
    print()
