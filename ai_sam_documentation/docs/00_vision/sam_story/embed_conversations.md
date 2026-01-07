# Embed Conversations

**Original file:** `embed_conversations.py`
**Type:** PYTHON

---

```python
"""
One-time script to embed all existing conversations to ChromaDB
Future conversations will auto-embed via model hook
"""
import sys
import os

# Setup Odoo path
sys.path.insert(0, r"C:\Program Files\Odoo 18\server")
os.chdir(r"C:\Working With AI\ai_sam\ai_sam")

import odoo
from odoo import api

# Initialize
odoo.tools.config.parse_config([
    '-c', r'C:\Program Files\Odoo 18\server\odoo.conf',
    '-d', 'ai_automator_db'
])

registry = odoo.registry('ai_automator_db')

print("Embedding conversations to ChromaDB...")
print("=" * 60)

with registry.cursor() as cr:
    env = api.Environment(cr, 1, {})

    # Get all conversations
    conversations = env['ai.conversation'].search([])
    total = len(conversations)

    print(f"Found {total} conversations to embed\n")

    vector_service = env['ai.vector.service']

    success_count = 0
    skip_count = 0
    error_count = 0

    for idx, conv in enumerate(conversations, 1):
        try:
            # Check if already embedded (optional - ChromaDB handles duplicates)
            result = vector_service.add_conversation_embedding(conv.id)

            if result.get('success'):
                success_count += 1
                status = "OK"
            else:
                skip_count += 1
                status = "SKIP"

            # Progress update every 10 conversations
            if idx % 10 == 0 or idx == total:
                print(f"{status} [{idx}/{total}] {conv.name[:50]}")

            # Commit every 50 to avoid memory issues
            if idx % 50 == 0:
                cr.commit()

        except Exception as e:
            error_count += 1
            print(f"ERROR: Failed to embed conversation {conv.id}: {e}")

    # Final commit
    cr.commit()

    print("\n" + "=" * 60)
    print("EMBEDDING COMPLETE!")
    print(f"   Successfully embedded: {success_count}")
    print(f"   Skipped (empty): {skip_count}")
    print(f"   Errors: {error_count}")
    print("=" * 60)
    print("\nSAM can now search your conversation history!")

```
