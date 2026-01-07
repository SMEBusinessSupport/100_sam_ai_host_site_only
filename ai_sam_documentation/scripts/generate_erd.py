# -*- coding: utf-8 -*-
"""
Generate Mermaid ERD from SAM AI database models.

Queries ir.model and ir.model.fields to build relationship diagram.
Runs on module install/upgrade via post_init_hook.
"""

import logging
from pathlib import Path

_logger = logging.getLogger(__name__)


def get_module_path():
    """Get the ai_sam_documentation module path."""
    from odoo.modules.module import get_module_path as odoo_get_module_path
    return Path(odoo_get_module_path('ai_sam_documentation'))


def get_sam_models(env):
    """
    Get all SAM AI models from ir.model.

    Returns list of dicts: [{'name': 'ai.conversation', 'model': 'ai_conversation', ...}]
    """
    IrModel = env['ir.model']

    # Find models starting with 'ai.' or 'sam.'
    models = IrModel.search([
        '|',
        ('model', '=like', 'ai.%'),
        ('model', '=like', 'sam.%'),
    ])

    result = []
    for model in models:
        # Skip transient models (wizards)
        if model.transient:
            continue

        result.append({
            'name': model.model,  # e.g., 'ai.conversation'
            'table': model.model.replace('.', '_'),  # e.g., 'ai_conversation'
            'description': model.name or model.model,
        })

    _logger.info(f"Found {len(result)} SAM AI models")
    return result


def get_model_relationships(env, model_name):
    """
    Get foreign key relationships for a model.

    Returns list of dicts: [{'field': 'user_id', 'target': 'res.users', 'type': 'many2one'}]
    """
    IrModelFields = env['ir.model.fields']

    fields = IrModelFields.search([
        ('model', '=', model_name),
        ('ttype', 'in', ['many2one', 'one2many', 'many2many']),
        ('relation', '!=', False),
    ])

    relationships = []
    for field in fields:
        # Skip computed/related fields that don't represent real DB relationships
        if field.related:
            continue

        relationships.append({
            'field': field.name,
            'target': field.relation,
            'type': field.ttype,
        })

    return relationships


def generate_mermaid_erd(models, all_relationships):
    """
    Generate Mermaid ERD syntax from models and relationships.

    Args:
        models: List of model dicts
        all_relationships: Dict mapping model_name -> list of relationships

    Returns:
        String containing Mermaid ERD syntax
    """
    lines = ['erDiagram']

    # Track which models we've defined (to avoid duplicates)
    defined_models = set()

    # Create a set of SAM AI model names for quick lookup
    sam_model_names = {m['name'] for m in models}
    sam_table_names = {m['table'] for m in models}

    # Fields to SKIP (Odoo boilerplate noise)
    SKIP_FIELDS = {
        'create_uid', 'write_uid', 'create_date', 'write_date',
        'message_follower_ids', 'message_ids', 'message_partner_ids',
        'website_message_ids', 'activity_ids', 'activity_user_id',
        'activity_calendar_event_id', 'rating_ids',
    }

    # Models to SKIP as targets (Odoo core noise)
    SKIP_TARGETS = {
        'res.users', 'res.company', 'res.partner', 'res.currency',
        'mail.message', 'mail.followers', 'mail.activity',
        'calendar.event', 'rating.rating', 'ir.attachment',
        'ir.model', 'ir.model.fields', 'ir.ui.view', 'ir.module.module',
    }

    # Add relationships - ONLY between SAM AI models
    for model in models:
        model_name = model['name']
        table_name = model['table']
        relationships = all_relationships.get(model_name, [])

        for rel in relationships:
            target = rel['target']
            rel_type = rel['type']
            field_name = rel['field']

            # SKIP noise fields
            if field_name in SKIP_FIELDS:
                continue

            # SKIP relationships to Odoo core models (unless it's a SAM AI model)
            if target in SKIP_TARGETS and target not in sam_model_names:
                continue

            # Convert model names to table format for Mermaid
            source_table = table_name
            target_table = target.replace('.', '_')

            # Determine relationship notation
            if rel_type == 'many2one':
                lines.append(f'    {source_table} }}o--|| {target_table} : "{field_name}"')
            elif rel_type == 'one2many':
                lines.append(f'    {source_table} ||--o{{ {target_table} : "{field_name}"')
            elif rel_type == 'many2many':
                lines.append(f'    {source_table} }}o--o{{ {target_table} : "{field_name}"')

            defined_models.add(source_table)
            defined_models.add(target_table)

    # Add SAM AI models without relationships as standalone entities
    for model in models:
        table_name = model['table']
        if table_name not in defined_models:
            lines.append(f'    {table_name} {{')
            lines.append(f'        string name "Core model"')
            lines.append(f'    }}')
            defined_models.add(table_name)

    return '\n'.join(lines)


def write_erd_markdown(mermaid_content, model_count, relationship_count):
    """Write ERD to markdown file in docs folder."""
    module_path = get_module_path()
    output_path = module_path / 'docs' / '05_architecture' / 'SAM_AI_ERD.md'

    # Ensure directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)

    content = f"""# SAM AI Database Schema (ERD)

**Auto-generated** on module upgrade.

- **Models:** {model_count}
- **Relationships:** {relationship_count}

## Interactive View

For zoom/pan capability, visit: `/sam_insights/erd`

## Entity Relationship Diagram

```mermaid
{mermaid_content}
```

## Legend

| Symbol | Meaning |
|--------|---------|
| `||--o{{` | One-to-Many |
| `}}o--||` | Many-to-One |
| `}}o--o{{` | Many-to-Many |

"""

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)

    _logger.info(f"Wrote ERD to {output_path}")
    return output_path


def generate_erd(env):
    """
    Main entry point - generate ERD from database schema.

    Called from post_init_hook on module install/upgrade.
    """
    _logger.info("=" * 60)
    _logger.info("Generating SAM AI ERD...")
    _logger.info("=" * 60)

    # Get all SAM AI models
    models = get_sam_models(env)

    if not models:
        _logger.warning("No SAM AI models found!")
        return

    # Get relationships for each model
    all_relationships = {}
    total_relationships = 0

    for model in models:
        relationships = get_model_relationships(env, model['name'])
        all_relationships[model['name']] = relationships
        total_relationships += len(relationships)

        if relationships:
            _logger.debug(f"  {model['name']}: {len(relationships)} relationships")

    # Generate Mermaid ERD
    mermaid_content = generate_mermaid_erd(models, all_relationships)

    # Write to markdown file
    write_erd_markdown(mermaid_content, len(models), total_relationships)

    _logger.info("=" * 60)
    _logger.info(f"ERD generation complete!")
    _logger.info(f"  Models: {len(models)}")
    _logger.info(f"  Relationships: {total_relationships}")
    _logger.info("=" * 60)


# Allow running standalone for testing
if __name__ == '__main__':
    print("This script should be run via Odoo post_init_hook")
    print("It requires access to the Odoo environment (env)")
