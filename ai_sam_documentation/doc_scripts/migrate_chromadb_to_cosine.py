#!/usr/bin/env python3
"""
Migrate ChromaDB collection from L2 to cosine similarity
"""

import sys
sys.path.insert(0, r"C:\Program Files\Odoo 18\server")

import odoo
from odoo import api

# Initialize Odoo
odoo.tools.config.parse_config([
    '-c', r'C:\Program Files\Odoo 18\server\odoo.conf',
    '-d', 'ai_automator_db'
])

registry = odoo.registry('ai_automator_db')

print("=" * 70)
print("MIGRATING CHROMADB TO COSINE SIMILARITY")
print("=" * 70)

with registry.cursor() as cr:
    env = api.Environment(cr, 1, {})

    vector_service = env['ai.vector.service']
    client = vector_service._get_chroma_client()

    # Delete old collection
    print("\nDeleting old L2-based collection...")
    try:
        client.delete_collection('sam_ai_conversations')
        print("Old collection deleted")
    except:
        print("No old collection found (this is fine)")

    # Create new collection with cosine similarity
    print("\nCreating new cosine-based collection...")
    collection = client.create_collection(
        name='sam_ai_conversations',
        metadata={
            "description": "SAM AI conversation embeddings",
            "hnsw:space": "cosine"
        }
    )
    print(f"New collection created: {collection.name}")
    print(f"Distance metric: cosine")

    # Re-embed all conversations
    print("\nRe-embedding all conversations...")
    conversations = env['ai.conversation'].search([])

    total = len(conversations)
    success = 0
    skip = 0

    for idx, conv in enumerate(conversations, 1):
        if conv.ai_message_ids:
            try:
                result = vector_service.add_conversation_embedding(conv.id)
                if result.get('success'):
                    success += 1
                else:
                    skip += 1

                if idx % 10 == 0:
                    print(f"  Progress: {idx}/{total} ({success} embedded, {skip} skipped)")
            except Exception as e:
                skip += 1
                print(f"  Error on conv {conv.id}: {str(e)[:50]}")
        else:
            skip += 1

    cr.commit()

    print("\n" + "=" * 70)
    print("MIGRATION COMPLETE!")
    print("=" * 70)
    print(f"  Total conversations: {total}")
    print(f"  Successfully embedded: {success}")
    print(f"  Skipped: {skip}")
    print("=" * 70)
    print("\nCollection now uses cosine similarity!")
    print("Semantic search will work correctly.")
