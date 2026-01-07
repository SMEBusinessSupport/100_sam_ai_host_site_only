# Developer Prompt: Interactive ERD Generator for SAM AI Documentation

## Context

SAM AI documentation module (`ai_sam_documentation`) currently generates text-based schema documentation. We need to add **visual ERD diagrams** with zoom/pan capability to help onboard Claude agents and humans to the database structure.

The documentation module already has:
- `post_init_hook` that runs on module upgrade
- `build_courses.py` that generates eLearning content from markdown
- Controllers for viewing documentation

We're adding an ERD generator that:
1. Queries PostgreSQL via Odoo ORM for SAM AI models
2. Generates Mermaid ERD syntax
3. Serves an interactive diagram at `/sam_insights/erd`

## Goal

Create an interactive, zoomable/pannable ERD diagram showing all SAM AI database models and their relationships, auto-generated on module upgrade.

## Technical Approach

- **Mermaid.js** - Renders ERD syntax to SVG (CDN, no install needed)
- **svg-pan-zoom.js** - Adds zoom/pan/drag to the SVG (CDN, no install needed)
- **Odoo ORM** - Query `ir.model` and `ir.model.fields` for schema info
- **post_init_hook** - Regenerate on every module upgrade

## Implementation Steps

### Step 1: Create ERD Generation Script

**File:** `scripts/generate_erd.py`

```python
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

    # Add relationships
    for model in models:
        model_name = model['name']
        table_name = model['table']
        relationships = all_relationships.get(model_name, [])

        for rel in relationships:
            target = rel['target']
            rel_type = rel['type']
            field_name = rel['field']

            # Convert model names to table format for Mermaid
            source_table = table_name
            target_table = target.replace('.', '_')

            # Determine relationship notation
            # many2one: source }o--|| target (many sources to one target)
            # one2many: source ||--o{ target (one source to many targets)
            # many2many: source }o--o{ target (many to many)

            if rel_type == 'many2one':
                # Show relationship with field name as label
                lines.append(f'    {source_table} }}o--|| {target_table} : "{field_name}"')
            elif rel_type == 'one2many':
                lines.append(f'    {source_table} ||--o{{ {target_table} : "{field_name}"')
            elif rel_type == 'many2many':
                lines.append(f'    {source_table} }}o--o{{ {target_table} : "{field_name}"')

            defined_models.add(source_table)
            defined_models.add(target_table)

    # Add any models without relationships (orphans)
    for model in models:
        table_name = model['table']
        if table_name not in defined_models:
            # Just define the entity
            lines.append(f'    {table_name} {{')
            lines.append(f'        string name "Primary model"')
            lines.append(f'    }}')

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
| `\|\|--o{{` | One-to-Many |
| `}}o--\|\|` | Many-to-One |
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
```

### Step 2: Create ERD Controller

**File:** `controllers/erd_controller.py`

```python
# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request, Response
from pathlib import Path
import logging

_logger = logging.getLogger(__name__)


class ERDController(http.Controller):

    @http.route('/sam_insights/erd', type='http', auth='user', website=True)
    def view_erd(self):
        """Serve interactive ERD viewer page."""

        # Read the generated ERD markdown
        erd_content = self._get_erd_mermaid_content()

        if not erd_content:
            return Response("ERD not yet generated. Please upgrade the module.", status=404)

        # Render full-page ERD viewer
        html = self._render_erd_page(erd_content)
        return Response(html, content_type='text/html')

    def _get_erd_mermaid_content(self):
        """Extract Mermaid content from ERD markdown file."""
        from odoo.modules.module import get_module_path

        module_path = Path(get_module_path('ai_sam_documentation'))
        erd_path = module_path / 'docs' / '05_architecture' / 'SAM_AI_ERD.md'

        if not erd_path.exists():
            return None

        content = erd_path.read_text(encoding='utf-8')

        # Extract mermaid block
        import re
        match = re.search(r'```mermaid\n(.*?)\n```', content, re.DOTALL)
        if match:
            return match.group(1)

        return None

    def _render_erd_page(self, mermaid_content):
        """Render the interactive ERD viewer HTML page."""

        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SAM AI - Database Schema</title>

    <!-- Mermaid for ERD rendering -->
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>

    <!-- SVG Pan Zoom for interactivity -->
    <script src="https://cdn.jsdelivr.net/npm/svg-pan-zoom@3.6.1/dist/svg-pan-zoom.min.js"></script>

    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: #1a1a2e;
            color: #eee;
            overflow: hidden;
        }}

        .header {{
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            height: 60px;
            background: #16213e;
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 20px;
            z-index: 100;
            box-shadow: 0 2px 10px rgba(0,0,0,0.3);
        }}

        .header h1 {{
            font-size: 20px;
            font-weight: 600;
        }}

        .header h1 span {{
            color: #0f3460;
            background: #e94560;
            padding: 4px 10px;
            border-radius: 4px;
            margin-right: 10px;
        }}

        .controls {{
            display: flex;
            gap: 10px;
        }}

        .controls button {{
            background: #0f3460;
            color: #fff;
            border: none;
            padding: 8px 16px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 14px;
            transition: background 0.2s;
        }}

        .controls button:hover {{
            background: #e94560;
        }}

        .erd-container {{
            position: fixed;
            top: 60px;
            left: 0;
            right: 0;
            bottom: 0;
            overflow: hidden;
            background: #1a1a2e;
        }}

        #erd-diagram {{
            width: 100%;
            height: 100%;
        }}

        #erd-diagram svg {{
            width: 100%;
            height: 100%;
        }}

        .instructions {{
            position: fixed;
            bottom: 20px;
            left: 20px;
            background: rgba(22, 33, 62, 0.9);
            padding: 15px 20px;
            border-radius: 8px;
            font-size: 13px;
            z-index: 100;
        }}

        .instructions p {{
            margin: 5px 0;
            opacity: 0.8;
        }}

        .instructions kbd {{
            background: #0f3460;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: monospace;
        }}

        /* Mermaid theme overrides for dark mode */
        .mermaid {{
            background: transparent !important;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1><span>SAM AI</span> Database Schema</h1>
        <div class="controls">
            <button onclick="resetZoom()">Reset View</button>
            <button onclick="fitToScreen()">Fit to Screen</button>
            <button onclick="zoomIn()">Zoom In</button>
            <button onclick="zoomOut()">Zoom Out</button>
            <button onclick="window.location.href='/sam_insights'">Back to Docs</button>
        </div>
    </div>

    <div class="erd-container">
        <div id="erd-diagram">
            <pre class="mermaid">
{mermaid_content}
            </pre>
        </div>
    </div>

    <div class="instructions">
        <p><kbd>Scroll</kbd> to zoom in/out</p>
        <p><kbd>Click + Drag</kbd> to pan</p>
        <p><kbd>Double-click</kbd> to reset view</p>
    </div>

    <script>
        // Initialize Mermaid with dark theme
        mermaid.initialize({{
            startOnLoad: true,
            theme: 'dark',
            er: {{
                useMaxWidth: false,
                layoutDirection: 'TB'
            }},
            securityLevel: 'loose'
        }});

        // Global pan-zoom instance
        let panZoomInstance = null;

        // Wait for Mermaid to render, then attach pan-zoom
        function initPanZoom() {{
            const svg = document.querySelector('#erd-diagram svg');
            if (svg) {{
                panZoomInstance = svgPanZoom(svg, {{
                    zoomEnabled: true,
                    controlIconsEnabled: false,
                    fit: true,
                    center: true,
                    minZoom: 0.1,
                    maxZoom: 20,
                    zoomScaleSensitivity: 0.3
                }});
                console.log('Pan-zoom initialized');
            }} else {{
                // Retry if SVG not ready
                setTimeout(initPanZoom, 500);
            }}
        }}

        // Initialize after page load
        window.addEventListener('load', () => {{
            setTimeout(initPanZoom, 1000);
        }});

        // Control functions
        function resetZoom() {{
            if (panZoomInstance) {{
                panZoomInstance.reset();
            }}
        }}

        function fitToScreen() {{
            if (panZoomInstance) {{
                panZoomInstance.fit();
                panZoomInstance.center();
            }}
        }}

        function zoomIn() {{
            if (panZoomInstance) {{
                panZoomInstance.zoomIn();
            }}
        }}

        function zoomOut() {{
            if (panZoomInstance) {{
                panZoomInstance.zoomOut();
            }}
        }}

        // Double-click to reset
        document.getElementById('erd-diagram').addEventListener('dblclick', resetZoom);
    </script>
</body>
</html>"""
```

### Step 3: Update Controllers __init__.py

**File:** `controllers/__init__.py`

Add import for new controller:

```python
from . import documentation_controller
from . import redirect_controller
from . import erd_controller  # ADD THIS LINE
```

### Step 4: Update Module __init__.py

**File:** `__init__.py`

Modify to call ERD generator:

```python
# -*- coding: utf-8 -*-
from . import controllers
from .scripts.build_courses import build_courses
from .scripts.generate_erd import generate_erd  # ADD THIS LINE


def post_init_hook(env):
    """Build courses and ERD from docs/ folder after install/upgrade."""
    build_courses(env)
    generate_erd(env)  # ADD THIS LINE
```

### Step 5: Update scripts __init__.py

**File:** `scripts/__init__.py`

Ensure generate_erd is importable:

```python
from . import build_courses
from . import generate_erd  # ADD THIS LINE (if not already present)
```

## Expected Files After Implementation

**New:**
- `scripts/generate_erd.py` - ERD generation logic
- `controllers/erd_controller.py` - Interactive viewer route
- `docs/05_architecture/SAM_AI_ERD.md` - Generated ERD markdown (auto-created)

**Modified:**
- `__init__.py` - Import and call generate_erd
- `controllers/__init__.py` - Import erd_controller
- `scripts/__init__.py` - Import generate_erd

## Validation Checklist

After implementation, verify:

- [ ] Module upgrades without errors: `-u ai_sam_documentation`
- [ ] Check logs for "Generating SAM AI ERD..." and "ERD generation complete!"
- [ ] File exists: `docs/05_architecture/SAM_AI_ERD.md`
- [ ] File contains valid Mermaid ERD syntax
- [ ] Route `/sam_insights/erd` loads (requires login)
- [ ] Mermaid diagram renders (not blank)
- [ ] Mouse wheel zoom works
- [ ] Click-drag pan works
- [ ] "Reset View" button works
- [ ] "Fit to Screen" button works
- [ ] All SAM AI models appear (check count in logs matches diagram)
- [ ] Relationships shown with arrows

## Testing Commands

```bash
# Upgrade module to trigger ERD generation
python odoo-bin -c odoo.conf -u ai_sam_documentation --stop-after-init

# Check the generated file
cat ai_sam_documentation/docs/05_architecture/SAM_AI_ERD.md

# Then start Odoo and visit:
# http://localhost:8069/sam_insights/erd
```

## Notes

- **CDN Dependencies:** Uses Mermaid.js and svg-pan-zoom from CDN. If offline access needed, vendor these in `static/lib/`.
- **Dark Theme:** ERD viewer uses dark theme to match SAM AI branding. Adjust colors in CSS if needed.
- **Performance:** 54 models with ~100 relationships renders quickly. If future growth exceeds 200+ entities, consider splitting by module.
- **Security:** Route requires `auth='user'` - only logged-in users can view.

## Success Criteria

1. ERD auto-generates on every module upgrade
2. Interactive viewer at `/sam_insights/erd` works with zoom/pan
3. All SAM AI models and their FK relationships are visible
4. Claude agents and humans can explore the schema visually
