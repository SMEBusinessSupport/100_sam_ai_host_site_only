# Location-Aware Introspection System Design

## Version History
- **V1 (Dec 2025)**: Content-based approach - hardcoded popular integrations
- **V2 (Dec 2025)**: Schema-driven approach - expose model schemas, let AI discover

## Problem Statement

SAM AI assistant runs inside Odoo but lacks awareness of its platform context. When a user is in the workflow canvas, SAM doesn't know:
- What node types are available (500+ from n8n.simple.node)
- What's currently on the canvas
- What the user can build

The AI gives generic advice instead of platform-specific guidance.

## Design Philosophy (V2)

**The AI should DISCOVER rather than be TOLD.**

Instead of hardcoding "popular integrations like Gmail, Slack...", we expose:
1. Model schemas (fields, types, record counts)
2. Available tools for querying
3. The AI then queries these models at conversation time

This scales to ANY Odoo domain without developer maintenance.

## Solution: Location-Aware Introspection

Build a system that:
1. **Auto-detects location** from context data (already have this)
2. **Discovers relevant models** based on location
3. **Queries those models** to understand the domain
4. **Injects knowledge** into the system prompt

## Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                   ai.location.introspector                          │
│                   (New AbstractModel in ai_sam_base)                │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ENTRY POINT: introspect(context_data)                             │
│                                                                     │
│  Returns: {                                                         │
│    'domain': 'workflow',           # Detected domain               │
│    'location': {...},              # Parsed location details       │
│    'knowledge': {...},             # Domain-specific knowledge     │
│    'capabilities': [...],          # What user can do here         │
│    'prompt_section': '...'         # Ready-to-inject prompt text   │
│  }                                                                  │
└─────────────────────────────────────────────────────────────────────┘
```

## Implementation Phases

### Phase 1: Domain Detection

Given `context_data`, determine which domain the user is in:

```python
DOMAIN_DETECTION_RULES = {
    'workflow': {
        'models': ['canvas', 'nodes'],
        'context_flags': ['is_workflow_chat', 'is_node_chat'],
        'menu_patterns': ['workflow', 'automation', 'ai builder'],
    },
    'crm': {
        'models': ['crm.lead', 'crm.stage'],
        'menu_patterns': ['crm', 'pipeline', 'leads'],
    },
    'sales': {
        'models': ['sale.order', 'sale.order.line'],
        'menu_patterns': ['sales', 'quotations'],
    },
    # ... more domains
}
```

### Phase 2: Model Discovery

For each domain, define the relevant models and their relationships:

```python
DOMAIN_MODEL_MAP = {
    'workflow': {
        'primary_models': ['canvas', 'nodes'],
        'catalog_models': ['n8n.simple.node', 'n8n.simple.supplier'],
        'related_models': ['workflow.connection', 'workflow.execution'],
        'knowledge_queries': [
            {
                'name': 'available_node_types',
                'model': 'n8n.simple.node',
                'method': '_get_node_type_catalog',
            },
            {
                'name': 'current_workflow',
                'model': 'canvas',
                'method': '_get_workflow_summary',
            },
        ]
    },
    'crm': {
        'primary_models': ['crm.lead'],
        'catalog_models': ['crm.stage', 'crm.team'],
        'knowledge_queries': [
            {
                'name': 'pipeline_stages',
                'model': 'crm.stage',
                'method': '_get_pipeline_stages',
            },
        ]
    },
}
```

### Phase 3: Knowledge Extraction

Domain-specific knowledge extraction methods:

```python
def _get_node_type_catalog(self):
    """Get available workflow node types grouped by category."""
    nodes = self.env['n8n.simple.node'].search([])

    # Group by supplier
    by_supplier = {}
    for node in nodes:
        supplier = node.supplier or 'Other'
        if supplier not in by_supplier:
            by_supplier[supplier] = []
        by_supplier[supplier].append({
            'name': node.display_name,
            'type': node.node_id,
            'is_trigger': node.is_trigger,
        })

    return {
        'total_count': len(nodes),
        'by_supplier': by_supplier,
        'top_suppliers': list(by_supplier.keys())[:20],
    }

def _get_workflow_summary(self, canvas_id):
    """Get current workflow summary."""
    canvas = self.env['canvas'].browse(canvas_id)
    if not canvas.exists():
        return None

    return {
        'name': canvas.name,
        'node_count': len(canvas.node_ids),
        'has_trigger': any(n.is_trigger for n in canvas.node_ids),
        'node_types': list(set(n.node_type for n in canvas.node_ids)),
    }
```

### Phase 4: Prompt Generation

Convert knowledge into prompt-ready text:

```python
def _format_workflow_knowledge(self, knowledge):
    """Format workflow knowledge for prompt injection."""
    sections = []

    sections.append("## PLATFORM KNOWLEDGE: Workflow Builder\n")

    # Node catalog
    catalog = knowledge.get('available_node_types', {})
    sections.append(f"**Available Node Types:** {catalog.get('total_count', 0)} integrations\n")

    top_suppliers = catalog.get('top_suppliers', [])
    if top_suppliers:
        sections.append("**Popular Integrations:**")
        for supplier in top_suppliers[:15]:
            count = len(catalog['by_supplier'].get(supplier, []))
            sections.append(f"- {supplier} ({count} nodes)")

    # Capabilities
    sections.append("\n**Your Capabilities:**")
    sections.append("- Use `canvas_node_types` tool to search for specific node types")
    sections.append("- Use `canvas_read` to see the current workflow")
    sections.append("- Use `canvas_edit` to add/modify nodes")
    sections.append("- Query the n8n.simple.node model for detailed node info")

    return '\n'.join(sections)
```

## Integration Points

### 1. System Prompt Building (ai_brain.py)

In `_build_system_prompt()`, add:

```python
# Inject platform knowledge based on location
if context_data:
    introspector = self.env['ai.location.introspector']
    location_knowledge = introspector.introspect(context_data)
    if location_knowledge.get('prompt_section'):
        prompt_parts.append(location_knowledge['prompt_section'])
```

### 2. Context Gathering (chat_input.py)

In `gather_context()`, enhance with:

```python
# Add location-aware knowledge
introspector = self.env['ai.location.introspector']
context['location_knowledge'] = introspector.introspect(context_data)
```

### 3. Tool Loading (canvas_tools.py)

Tools are already loaded based on `is_canvas_context()`. The introspector enhances this with knowledge, not tools.

## File Structure

```
ai_sam_base/
├── models/
│   ├── ai_context_builder.py      # Existing - general context
│   ├── ai_location_introspector.py  # NEW - location-aware knowledge
│   └── __init__.py                # Add import
├── data/
│   └── domain_definitions.xml     # Domain → model mappings (optional)
└── docs/
    └── LOCATION_INTROSPECTION_DESIGN.md  # This document
```

## Domain Definitions

### Workflow Domain
- **Primary Model:** canvas
- **Catalog Models:** n8n.simple.node, n8n.simple.supplier
- **Key Knowledge:**
  - Available node types (500+)
  - Node categories (Communication, CRM, Data, etc.)
  - Current workflow state
  - Connection patterns

### CRM Domain
- **Primary Model:** crm.lead
- **Catalog Models:** crm.stage, crm.team, res.partner
- **Key Knowledge:**
  - Pipeline stages
  - Team structure
  - Lead fields and statuses

### Generic Domain (Fallback)
- Uses ir.model introspection
- Gets field definitions
- Provides model schema

## Success Criteria

1. When user opens AI Builder chat, SAM knows:
   - 500+ node types are available
   - How to search for specific integrations
   - What's currently on the canvas

2. When user says "I want to connect Gmail to Google Sheets":
   - SAM suggests specific nodes (Gmail Trigger, Google Sheets)
   - Uses `canvas_node_types` to find exact node types
   - Can build the workflow with correct node IDs

3. Generic fallback works for any Odoo model:
   - SAM can introspect field definitions
   - Understands model relationships
   - Provides relevant guidance

## V2 Architecture: Schema-Driven Discovery

### Key Methods

```python
# Resolve /odoo/action-1875 to model
resolve_action_to_model(action_id) → {'model': 'sale.order', 'name': 'Sales Orders'}

# Get model schema using ir.model + ir.model.fields
get_model_schema(model_name) → {
    'model': 'n8n.simple.node',
    'record_count': 505,
    'fields': [{'name': 'display_name', 'type': 'char'}, ...]
}

# Get all schemas for a domain
get_domain_schemas(domain_key) → {
    'primary_models': [...],
    'catalog_models': [...],
    'tools': [...]
}

# Format for prompt injection
format_schema_prompt(domain_key) → "## PLATFORM CONTEXT: Workflow Builder..."
```

### Example V2 Prompt Output

```
## PLATFORM CONTEXT: Workflow Builder

Visual automation builder with N8N-compatible nodes

### Available Data Models

Use these models to discover and query platform data:

**canvas** (42 records) - Workflow Canvas
  Fields: name, display_name, active, json_definition, ...

**n8n.simple.node** (505 records) - N8N Simple Node
  Fields: name, display_name, node_id, is_trigger, supplier, ...

**n8n.simple.supplier** (87 records) - N8N Simple Supplier
  Fields: name, total_nodes, trigger_count, action_count, ...

### Available Tools

- **canvas_node_types**: Search for node types by name/category
- **canvas_read**: Read current workflow state
- **canvas_edit**: Add, modify, or remove nodes

### How to Help Users

Query the models above to find specific information.
Example: `self.env['n8n.simple.node'].search([('display_name', 'ilike', 'gmail')])`
```

### Why V2 is Better

| V1 (Content-Based) | V2 (Schema-Driven) |
|---|---|
| Hardcoded "Gmail, Slack, Notion" | AI discovers via model queries |
| Developer maintains each domain | Self-describing via ir.model |
| Stale if data changes | Always current |
| Doesn't scale | Scales to any Odoo model |

## Implementation Status

- [x] Create `ai_location_introspector.py` model
- [x] Implement domain detection logic
- [x] Implement V1 content-based knowledge extraction
- [x] Wire into system prompt building
- [x] Create debug visualization tool
- [x] Implement V2 schema-driven discovery
- [x] Add action-ID to model resolution
- [x] Update debug page for V2 display

## Next Steps

1. Test V2 with workflow canvas - verify schema output
2. Extend to other domains (CRM, Sales, etc.)
3. Add model query tool for AI to execute Odoo searches
4. Consider caching schemas for performance
