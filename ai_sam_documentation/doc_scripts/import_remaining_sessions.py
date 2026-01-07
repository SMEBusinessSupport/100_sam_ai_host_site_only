#!/usr/bin/env python3
"""
Import remaining Claude Code sessions that were skipped
"""

import sys
import os
sys.path.insert(0, r"C:\Program Files\Odoo 18\server")

import odoo
from odoo import api

# Initialize Odoo
odoo.tools.config.parse_config([
    '-c', r'C:\Program Files\Odoo 18\server\odoo.conf',
    '-d', 'ai_automator_db'
])

registry = odoo.registry('ai_automator_db')

# Path to JSONL files
JSONL_DIR = r"C:\Users\total\.claude\projects\C--Users-total"

print("=" * 70)
print("IMPORTING REMAINING CLAUDE CODE SESSIONS")
print("=" * 70)

with registry.cursor() as cr:
    env = api.Environment(cr, 1, {})

    # Get all JSONL files
    jsonl_files = [f for f in os.listdir(JSONL_DIR) if f.endswith('.jsonl')]
    total_files = len(jsonl_files)

    print(f"\nFound {total_files} JSONL files\n")

    importer = env['ai.conversation.import']

    success_count = 0
    error_count = 0
    skip_count = 0

    for idx, filename in enumerate(jsonl_files, 1):
        filepath = os.path.join(JSONL_DIR, filename)

        try:
            # Create import record (let Odoo's duplicate check handle it)
            import_record = importer.create({
                'name': f'Import {filename}',
                'source_path': filepath,
                'skip_duplicates': True,
            })

            # Run import
            import_record.action_validate_source()

            if import_record.is_valid:
                import_record.action_import_data()

                if import_record.imported_conversations > 0:
                    success_count += 1
                    print(f"[{idx}/{total_files}] OK: {filename[:50]} ({import_record.imported_messages} msgs)")
                else:
                    skip_count += 1
            else:
                error_count += 1

            # Commit every 10 imports
            if idx % 10 == 0:
                cr.commit()
                print(f"  Committed batch at {idx}/{total_files} - Success: {success_count}, Skip: {skip_count}, Error: {error_count}")

        except Exception as e:
            error_count += 1
            if 'No conversations found' not in str(e):
                print(f"[{idx}/{total_files}] ERROR: {filename[:40]}... - {str(e)[:80]}")

    # Final commit
    cr.commit()

    print("\n" + "=" * 70)
    print("IMPORT COMPLETE!")
    print("=" * 70)
    print(f"  Total files:     {total_files}")
    print(f"  Newly imported:  {success_count}")
    print(f"  Skipped:         {skip_count}")
    print(f"  Errors:          {error_count}")
    print("=" * 70)

    # Count final conversations
    all_convs = env['ai.conversation'].search([])
    print(f"\nTotal conversations in Odoo: {len(all_convs)}")
