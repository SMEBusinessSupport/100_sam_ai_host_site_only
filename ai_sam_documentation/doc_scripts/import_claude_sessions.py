#!/usr/bin/env python3
"""
Batch import Claude Code JSONL sessions to Odoo
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
print("IMPORTING CLAUDE CODE SESSIONS TO ODOO")
print("=" * 70)

with registry.cursor() as cr:
    env = api.Environment(cr, 1, {})

    # Get all JSONL files
    jsonl_files = [f for f in os.listdir(JSONL_DIR) if f.endswith('.jsonl')]
    total_files = len(jsonl_files)

    print(f"\nFound {total_files} JSONL files to import\n")

    importer = env['ai.conversation.import']

    success_count = 0
    error_count = 0
    skip_count = 0

    for idx, filename in enumerate(jsonl_files, 1):
        filepath = os.path.join(JSONL_DIR, filename)

        try:
            # Check if already imported (by filename or session ID)
            session_id = filename.replace('.jsonl', '')
            existing = env['ai.conversation'].search([
                ('name', 'ilike', session_id)
            ], limit=1)

            if existing:
                skip_count += 1
                if idx % 10 == 0:
                    print(f"[{idx}/{total_files}] SKIP: {filename[:40]}... (already exists)")
                continue

            # Create import record
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
                    print(f"[{idx}/{total_files}] OK: {filename[:40]}... ({import_record.imported_messages} messages)")
                else:
                    skip_count += 1
            else:
                error_count += 1
                print(f"[{idx}/{total_files}] ERROR: {filename[:40]}...")

            # Commit every 10 imports
            if idx % 10 == 0:
                cr.commit()

        except Exception as e:
            error_count += 1
            print(f"[{idx}/{total_files}] ERROR: {filename[:40]}... - {str(e)[:50]}")

    # Final commit
    cr.commit()

    print("\n" + "=" * 70)
    print("IMPORT COMPLETE!")
    print("=" * 70)
    print(f"  Total files:     {total_files}")
    print(f"  Imported:        {success_count}")
    print(f"  Skipped:         {skip_count}")
    print(f"  Errors:          {error_count}")
    print("=" * 70)

    # Now embed all conversations
    print("\nEmbedding conversations to ChromaDB...")

    vector_service = env['ai.vector.service']
    all_convs = env['ai.conversation'].search([])

    embedded = 0
    for conv in all_convs:
        if conv.ai_message_ids:
            try:
                result = vector_service.add_conversation_embedding(conv.id)
                if result.get('success'):
                    embedded += 1
            except:
                pass

    cr.commit()

    print(f"Embedded {embedded} conversations to ChromaDB")
    print("\nDONE! SAM can now search your conversation history.")
