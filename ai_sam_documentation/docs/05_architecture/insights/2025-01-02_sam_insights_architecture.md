# SAM Insights Architecture - Implementation Plan

**Created**: 2025-01-02
**Status**: Ready for Implementation
**Module**: ai_sam_documentation (self-contained)
**URL Pattern**: /sam_insights/

---

## Executive Summary

Transform ai_sam_documentation into a knowledge publishing system where:
- Local `.md` files are the source of truth
- Stable URLs never change (even when files reorganize)
- Content auto-syncs on module upgrade
- Website pages render as proper Odoo snippets (not raw HTML)

---

## Architecture Overview

```
ai_sam_documentation/
│
├── docs/                           ← KNOWLEDGE SOURCE
│   ├── _url_registry.json          ← Slug → file path mapping
│   ├── knowledge_index.md          ← AUTO-GENERATED (don't edit)
│   │
│   ├── 00_sam_skills/              ← Agent capabilities
│   │   ├── cto/
│   │   ├── developer/
│   │   └── architect/
│   │
│   ├── 01_modules/                 ← Per-module reference
│   │   ├── ai_brain/
│   │   │   ├── description.md
│   │   │   └── schema.md
│   │   ├── ai_sam/
│   │   └── ai_sam_workflows/
│   │
│   ├── 02_data_flows/              ← How data moves
│   │   ├── apis/
│   │   ├── chat/
│   │   ├── node_creation/
│   │   └── system_prompt_builder/
│   │
│   ├── 03_platform_skins/          ← How skins work
│   │
│   ├── 04_architecture/            ← High-level patterns
│   │
│   └── 05_vision/                  ← Strategic direction
│
├── external_registry.json          ← Links to files in OTHER modules
│
├── scripts/
│   └── build_knowledge.py          ← Runs on upgrade (post_init_hook)
│
├── models/
│   ├── __init__.py
│   ├── insight_page.py             ← insight.page model
│   └── insight_category.py         ← insight.category model
│
├── controllers/
│   ├── __init__.py
│   └── website_controller.py       ← /sam_insights/ routes
│
├── views/
│   ├── website_templates.xml       ← Odoo website page templates
│   ├── website_index.xml           ← Index page template
│   └── backend_views.xml           ← Admin interface (optional)
│
├── security/
│   └── ir.model.access.csv
│
├── static/
│   └── src/
│       └── css/
│           └── insights.css        ← Styling for insight pages
│
└── __manifest__.py
```

---

## Phase 1: Foundation

### Task 1.1: Update Manifest

**File**: `__manifest__.py`

```python
{
    'name': 'SAM AI Documentation & Insights',
    'version': '18.0.1.0.0',
    'author': 'Anthony Gardiner - Odoo Consulting & Claude AI',
    'maintainer': 'Anthony Gardiner <anthony@sme.ec>',
    'website': 'https://sme.ec',
    'category': 'Website/Knowledge',
    'license': 'LGPL-3',
    'summary': 'SAM AI Knowledge Publishing System - /sam_insights/',
    'description': """
SAM AI Documentation & Insights
================================

Knowledge publishing system for SAM AI ecosystem.

Features:
- Markdown files → Odoo website pages
- Stable URLs (files can reorganize, URLs stay same)
- Auto-sync on module upgrade
- Proper Odoo website snippets (theme-aware)

URL Pattern: /sam_insights/<slug>
    """,
    'depends': [
        'base',
        'web',
        'website',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/website_templates.xml',
        'views/website_index.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'ai_sam_documentation/static/src/css/insights.css',
        ],
    },
    'post_init_hook': 'post_init_hook',
    'images': ['static/description/icon.png'],
    'installable': True,
    'application': False,
    'auto_install': False,
}
```

### Task 1.2: Create Models

**File**: `models/__init__.py`
```python
from . import insight_category
from . import insight_page
```

**File**: `models/insight_category.py`
```python
from odoo import fields, models

class InsightCategory(models.Model):
    _name = 'insight.category'
    _description = 'Insight Category'
    _order = 'sequence, name'

    name = fields.Char(required=True)
    slug = fields.Char(required=True, index=True)
    sequence = fields.Integer(default=10)
    description = fields.Text()
    page_ids = fields.One2many('insight.page', 'category_id', string='Pages')
    page_count = fields.Integer(compute='_compute_page_count')
    folder_path = fields.Char(help='Folder path in docs/, e.g., 00_sam_skills')

    def _compute_page_count(self):
        for rec in self:
            rec.page_count = len(rec.page_ids)
```

**File**: `models/insight_page.py`
```python
from odoo import fields, models, api
import re

class InsightPage(models.Model):
    _name = 'insight.page'
    _description = 'Insight Page'
    _order = 'category_id, sequence, name'

    name = fields.Char(required=True)
    slug = fields.Char(required=True, index=True, unique=True)
    category_id = fields.Many2one('insight.category', string='Category', ondelete='set null')

    # Content
    content_md = fields.Text(string='Markdown Source')
    content_html = fields.Html(string='Rendered HTML', sanitize=False)

    # Source tracking
    source_path = fields.Char(help='Relative path in docs/')
    source_type = fields.Selection([
        ('internal', 'Internal (docs/ folder)'),
        ('external', 'External (other module)'),
    ], default='internal')
    external_module = fields.Char(help='Module name for external sources')

    # Metadata
    sequence = fields.Integer(default=10)
    last_sync = fields.Datetime()
    website_url = fields.Char(compute='_compute_website_url', store=True)
    active = fields.Boolean(default=True)

    _sql_constraints = [
        ('slug_unique', 'UNIQUE(slug)', 'Slug must be unique!')
    ]

    @api.depends('slug')
    def _compute_website_url(self):
        for rec in self:
            rec.website_url = f'/sam_insights/{rec.slug}' if rec.slug else False
```

### Task 1.3: Create URL Registry Structure

**File**: `docs/_url_registry.json`
```json
{
  "_meta": {
    "description": "Maps permanent slugs to current file paths. URLs never change, files can move.",
    "updated": "2025-01-02"
  },
  "pages": {
    "example-insight": {
      "path": "04_architecture/example.md",
      "category": "architecture",
      "title": "Example Insight",
      "created": "2025-01-02"
    }
  },
  "categories": {
    "sam-skills": {
      "folder": "00_sam_skills",
      "sequence": 0,
      "description": "Agent capabilities and skills"
    },
    "modules": {
      "folder": "01_modules",
      "sequence": 10,
      "description": "Per-module reference documentation"
    },
    "data-flows": {
      "folder": "02_data_flows",
      "sequence": 20,
      "description": "How data moves through the system"
    },
    "platform-skins": {
      "folder": "03_platform_skins",
      "sequence": 30,
      "description": "How platform skins work"
    },
    "architecture": {
      "folder": "04_architecture",
      "sequence": 40,
      "description": "High-level patterns and decisions"
    },
    "vision": {
      "folder": "05_vision",
      "sequence": 50,
      "description": "Strategic direction"
    }
  }
}
```

### Task 1.4: Create Build Script

**File**: `scripts/__init__.py`
```python
from . import build_knowledge
```

**File**: `scripts/build_knowledge.py`
```python
import json
import logging
from pathlib import Path
from datetime import datetime

_logger = logging.getLogger(__name__)

# Optional markdown - fallback to basic conversion if not available
try:
    import markdown
    MARKDOWN_AVAILABLE = True
except ImportError:
    MARKDOWN_AVAILABLE = False
    _logger.warning("markdown library not installed. Using basic conversion.")


def get_module_path():
    """Get the ai_sam_documentation module path."""
    from odoo.modules.module import get_module_path
    return Path(get_module_path('ai_sam_documentation'))


def load_url_registry():
    """Load the URL registry JSON."""
    registry_path = get_module_path() / 'docs' / '_url_registry.json'
    if registry_path.exists():
        with open(registry_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"_meta": {}, "pages": {}, "categories": {}}


def convert_md_to_html(content):
    """Convert markdown to HTML."""
    if MARKDOWN_AVAILABLE:
        return markdown.markdown(
            content,
            extensions=['tables', 'fenced_code', 'toc', 'meta']
        )
    else:
        # Basic conversion
        import re
        html = content
        html = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
        html = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
        html = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
        html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
        html = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html)
        html = re.sub(r'```(.+?)```', r'<pre><code>\1</code></pre>', html, flags=re.DOTALL)
        html = re.sub(r'`(.+?)`', r'<code>\1</code>', html)
        return f'<div class="markdown-content">{html}</div>'


def sync_categories(env, registry):
    """Sync categories from registry."""
    Category = env['insight.category']

    for slug, data in registry.get('categories', {}).items():
        existing = Category.search([('slug', '=', slug)], limit=1)
        vals = {
            'name': data.get('description', slug.replace('-', ' ').title()),
            'slug': slug,
            'sequence': data.get('sequence', 50),
            'description': data.get('description', ''),
            'folder_path': data.get('folder'),
        }
        if existing:
            existing.write(vals)
        else:
            Category.create(vals)

    _logger.info(f"Synced {len(registry.get('categories', {}))} categories")


def sync_pages(env, registry):
    """Sync pages from registry and docs folder."""
    Page = env['insight.page']
    Category = env['insight.category']
    module_path = get_module_path()
    docs_path = module_path / 'docs'
    now = datetime.now()

    synced = 0

    for slug, data in registry.get('pages', {}).items():
        file_path = docs_path / data['path']

        if not file_path.exists():
            _logger.warning(f"File not found for slug '{slug}': {data['path']}")
            continue

        # Read and convert content
        content_md = file_path.read_text(encoding='utf-8')
        content_html = convert_md_to_html(content_md)

        # Find category
        category = Category.search([('slug', '=', data.get('category', ''))], limit=1)

        # Create or update page
        existing = Page.search([('slug', '=', slug)], limit=1)
        vals = {
            'name': data.get('title', slug.replace('-', ' ').title()),
            'slug': slug,
            'category_id': category.id if category else False,
            'content_md': content_md,
            'content_html': content_html,
            'source_path': data['path'],
            'source_type': 'internal',
            'last_sync': now,
        }

        if existing:
            existing.write(vals)
        else:
            Page.create(vals)

        synced += 1

    _logger.info(f"Synced {synced} pages")


def generate_knowledge_index(env):
    """Generate the knowledge_index.md file."""
    Category = env['insight.category']
    module_path = get_module_path()
    index_path = module_path / 'docs' / 'knowledge_index.md'

    lines = [
        "# SAM AI Knowledge Index",
        "",
        f"_Auto-generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}_",
        "",
        "---",
        "",
    ]

    categories = Category.search([], order='sequence, name')
    for cat in categories:
        lines.append(f"## {cat.name}")
        lines.append("")
        if cat.description:
            lines.append(f"_{cat.description}_")
            lines.append("")

        for page in cat.page_ids:
            lines.append(f"- [{page.name}]({page.website_url})")

        lines.append("")

    index_path.write_text('\n'.join(lines), encoding='utf-8')
    _logger.info(f"Generated knowledge_index.md with {len(categories)} categories")


def build_knowledge(env):
    """Main entry point - run on module upgrade."""
    _logger.info("Building SAM AI Knowledge...")

    registry = load_url_registry()
    sync_categories(env, registry)
    sync_pages(env, registry)
    generate_knowledge_index(env)

    _logger.info("SAM AI Knowledge build complete!")
```

**File**: `__init__.py` (update root)
```python
from . import models
from . import controllers
from .scripts.build_knowledge import build_knowledge

def post_init_hook(env):
    """Run knowledge build after module install/upgrade."""
    build_knowledge(env)
```

### Task 1.5: Create Website Controller

**File**: `controllers/__init__.py`
```python
from . import website_controller
```

**File**: `controllers/website_controller.py`
```python
from odoo import http
from odoo.http import request

class SamInsightsController(http.Controller):

    @http.route('/sam_insights', type='http', auth='public', website=True)
    def insights_index(self, **kwargs):
        """Index page - list all categories and pages."""
        categories = request.env['insight.category'].sudo().search([], order='sequence, name')
        return request.render('ai_sam_documentation.insights_index', {
            'categories': categories,
        })

    @http.route('/sam_insights/<string:slug>', type='http', auth='public', website=True)
    def insight_page(self, slug, **kwargs):
        """Individual insight page by slug."""
        page = request.env['insight.page'].sudo().search([
            ('slug', '=', slug),
            ('active', '=', True),
        ], limit=1)

        if not page:
            return request.not_found()

        # Get sibling pages for navigation
        siblings = []
        if page.category_id:
            siblings = page.category_id.page_ids.filtered(lambda p: p.active)

        return request.render('ai_sam_documentation.insight_page', {
            'page': page,
            'siblings': siblings,
        })

    @http.route('/sam_insights/category/<string:slug>', type='http', auth='public', website=True)
    def insights_category(self, slug, **kwargs):
        """Category listing page."""
        category = request.env['insight.category'].sudo().search([
            ('slug', '=', slug),
        ], limit=1)

        if not category:
            return request.not_found()

        return request.render('ai_sam_documentation.insights_category', {
            'category': category,
            'pages': category.page_ids.filtered(lambda p: p.active),
        })
```

### Task 1.6: Create Website Templates

**File**: `views/website_index.xml`
```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>

    <!-- Index Page Template -->
    <template id="insights_index" name="SAM Insights Index">
        <t t-call="website.layout">
            <div id="wrap" class="oe_structure">
                <section class="s_title pt48 pb24">
                    <div class="container">
                        <h1>SAM AI Knowledge Base</h1>
                        <p class="lead">Architecture, modules, data flows, and strategic insights.</p>
                    </div>
                </section>

                <section class="s_text_block pt24 pb48">
                    <div class="container">
                        <div class="row">
                            <t t-foreach="categories" t-as="category">
                                <div class="col-lg-4 col-md-6 mb-4">
                                    <div class="card h-100">
                                        <div class="card-body">
                                            <h5 class="card-title">
                                                <a t-attf-href="/sam_insights/category/#{category.slug}">
                                                    <t t-esc="category.name"/>
                                                </a>
                                            </h5>
                                            <p class="card-text text-muted" t-if="category.description">
                                                <t t-esc="category.description"/>
                                            </p>
                                            <p class="card-text">
                                                <small class="text-muted">
                                                    <t t-esc="category.page_count"/> pages
                                                </small>
                                            </p>
                                        </div>
                                        <div class="card-footer bg-transparent">
                                            <a t-attf-href="/sam_insights/category/#{category.slug}"
                                               class="btn btn-sm btn-outline-primary">
                                                Browse
                                            </a>
                                        </div>
                                    </div>
                                </div>
                            </t>
                        </div>
                    </div>
                </section>
            </div>
        </t>
    </template>

    <!-- Category Page Template -->
    <template id="insights_category" name="SAM Insights Category">
        <t t-call="website.layout">
            <div id="wrap" class="oe_structure">
                <section class="s_title pt48 pb24">
                    <div class="container">
                        <nav aria-label="breadcrumb">
                            <ol class="breadcrumb">
                                <li class="breadcrumb-item">
                                    <a href="/sam_insights">Knowledge Base</a>
                                </li>
                                <li class="breadcrumb-item active" t-esc="category.name"/>
                            </ol>
                        </nav>
                        <h1 t-esc="category.name"/>
                        <p class="lead" t-if="category.description" t-esc="category.description"/>
                    </div>
                </section>

                <section class="s_text_block pt24 pb48">
                    <div class="container">
                        <div class="list-group">
                            <t t-foreach="pages" t-as="page">
                                <a t-attf-href="/sam_insights/#{page.slug}"
                                   class="list-group-item list-group-item-action d-flex justify-content-between align-items-center">
                                    <span t-esc="page.name"/>
                                    <small class="text-muted" t-if="page.last_sync">
                                        Updated: <t t-esc="page.last_sync" t-options="{'widget': 'date'}"/>
                                    </small>
                                </a>
                            </t>
                        </div>
                    </div>
                </section>
            </div>
        </t>
    </template>

</odoo>
```

**File**: `views/website_templates.xml`
```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>

    <!-- Individual Insight Page Template -->
    <template id="insight_page" name="SAM Insight Page">
        <t t-call="website.layout">
            <div id="wrap" class="oe_structure">
                <section class="s_title pt48 pb24">
                    <div class="container">
                        <nav aria-label="breadcrumb">
                            <ol class="breadcrumb">
                                <li class="breadcrumb-item">
                                    <a href="/sam_insights">Knowledge Base</a>
                                </li>
                                <li class="breadcrumb-item" t-if="page.category_id">
                                    <a t-attf-href="/sam_insights/category/#{page.category_id.slug}">
                                        <t t-esc="page.category_id.name"/>
                                    </a>
                                </li>
                                <li class="breadcrumb-item active" t-esc="page.name"/>
                            </ol>
                        </nav>
                        <h1 t-esc="page.name"/>
                        <p class="text-muted" t-if="page.last_sync">
                            Last updated: <t t-esc="page.last_sync" t-options="{'widget': 'datetime'}"/>
                        </p>
                    </div>
                </section>

                <section class="s_text_block pt24 pb48">
                    <div class="container">
                        <div class="row">
                            <!-- Main Content -->
                            <div class="col-lg-9">
                                <div class="insight-content" t-raw="page.content_html"/>
                            </div>

                            <!-- Sidebar Navigation -->
                            <div class="col-lg-3" t-if="siblings">
                                <div class="card">
                                    <div class="card-header">
                                        <strong>In This Category</strong>
                                    </div>
                                    <ul class="list-group list-group-flush">
                                        <t t-foreach="siblings" t-as="sibling">
                                            <li class="list-group-item"
                                                t-attf-class="list-group-item #{'active' if sibling.id == page.id else ''}">
                                                <a t-attf-href="/sam_insights/#{sibling.slug}"
                                                   t-attf-class="#{'text-white' if sibling.id == page.id else ''}">
                                                    <t t-esc="sibling.name"/>
                                                </a>
                                            </li>
                                        </t>
                                    </ul>
                                </div>
                            </div>
                        </div>
                    </div>
                </section>
            </div>
        </t>
    </template>

</odoo>
```

### Task 1.7: Create Security

**File**: `security/ir.model.access.csv`
```csv
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_insight_category_public,insight.category.public,model_insight_category,,1,0,0,0
access_insight_page_public,insight.page.public,model_insight_page,,1,0,0,0
access_insight_category_admin,insight.category.admin,model_insight_category,base.group_system,1,1,1,1
access_insight_page_admin,insight.page.admin,model_insight_page,base.group_system,1,1,1,1
```

### Task 1.8: Create CSS

**File**: `static/src/css/insights.css`
```css
/* SAM Insights Page Styling */

.insight-content {
    line-height: 1.7;
}

.insight-content h1,
.insight-content h2,
.insight-content h3 {
    margin-top: 1.5em;
    margin-bottom: 0.5em;
}

.insight-content h1 { border-bottom: 2px solid #dee2e6; padding-bottom: 0.3em; }
.insight-content h2 { border-bottom: 1px solid #dee2e6; padding-bottom: 0.2em; }

.insight-content code {
    background-color: #f8f9fa;
    padding: 0.2em 0.4em;
    border-radius: 3px;
    font-size: 0.9em;
}

.insight-content pre {
    background-color: #2d3748;
    color: #e2e8f0;
    padding: 1em;
    border-radius: 6px;
    overflow-x: auto;
}

.insight-content pre code {
    background-color: transparent;
    padding: 0;
    color: inherit;
}

.insight-content table {
    width: 100%;
    margin: 1em 0;
    border-collapse: collapse;
}

.insight-content th,
.insight-content td {
    border: 1px solid #dee2e6;
    padding: 0.75em;
    text-align: left;
}

.insight-content th {
    background-color: #f8f9fa;
    font-weight: 600;
}

.insight-content blockquote {
    border-left: 4px solid #007bff;
    padding-left: 1em;
    margin-left: 0;
    color: #6c757d;
}
```

---

## Phase 2: Folder Structure Setup

### Task 2.1: Create New Folder Structure

Run these commands to set up the docs folder:

```bash
cd D:\SAMAI-18-SaaS\github-repos\05-samai-core\ai_sam_documentation

# Create new structure
mkdir -p docs/00_sam_skills
mkdir -p docs/01_modules
mkdir -p docs/02_data_flows/apis
mkdir -p docs/02_data_flows/chat
mkdir -p docs/02_data_flows/node_creation
mkdir -p docs/02_data_flows/system_prompt_builder
mkdir -p docs/03_platform_skins
mkdir -p docs/04_architecture
mkdir -p docs/05_vision

# Create scripts folder
mkdir -p scripts
```

### Task 2.2: Migrate Existing Content

Move existing docs to appropriate folders:

| Current Location | New Location |
|------------------|--------------|
| `docs/architecture/*.md` | `docs/04_architecture/` |
| `docs/canvas/*.md` | `docs/04_architecture/` or `docs/02_data_flows/` |
| `docs/development/*.md` | `docs/05_vision/` or archive |
| `docs/current_state.md` | `docs/04_architecture/current_state.md` |

**Note**: This is manual curation. Not all old docs need to migrate - some may be obsolete.

---

## Phase 3: First Content

### Task 3.1: Create Initial Registry Entries

After moving files, update `_url_registry.json` with entries like:

```json
{
  "pages": {
    "current-state": {
      "path": "04_architecture/current_state.md",
      "category": "architecture",
      "title": "SAM AI Current State",
      "created": "2025-01-02"
    },
    "canvas-skeleton": {
      "path": "04_architecture/CANVAS_SKELETON_CORE_ARCHITECTURE.md",
      "category": "architecture",
      "title": "Canvas Skeleton Architecture",
      "created": "2025-01-02"
    }
  }
}
```

### Task 3.2: Test the System

1. Install/upgrade module: `-u ai_sam_documentation`
2. Visit: `http://localhost:8069/sam_insights`
3. Verify categories appear
4. Click through to individual pages
5. Check URLs are stable

---

## Validation Checklist

- [ ] Module installs without errors
- [ ] `/sam_insights/` shows index page
- [ ] Categories appear with correct names
- [ ] Individual pages render markdown as HTML
- [ ] URLs are slug-based (not file-path based)
- [ ] CSS styling applies correctly
- [ ] Breadcrumbs navigate properly
- [ ] `knowledge_index.md` auto-generates

---

## Future Enhancements (Not in Scope Now)

- Search functionality
- Full-text search across content
- External registry for other module docs
- API endpoint for AI sessions to fetch content
- Version history (currently rely on git)
- Admin interface for editing in Odoo

---

## Developer Handoff

When ready to implement, create a new developer session with:

```
Implement Phase 1 of the SAM Insights architecture plan.

Plan location: D:\SAMAI-18-SaaS\github-repos\05-samai-core\ai_sam_documentation\plans\2025-01-02_sam_insights_architecture.md

Start with Tasks 1.1 through 1.8.
```

---

**End of Plan**
