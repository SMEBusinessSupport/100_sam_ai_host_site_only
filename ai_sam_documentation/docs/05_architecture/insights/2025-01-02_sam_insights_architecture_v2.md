# SAM Insights Architecture v2 - eLearning Wrapper

**Created**: 2025-01-02
**Status**: Ready for Implementation
**Module**: ai_sam_documentation
**Approach**: Wrapper around website_slides (eLearning)

---

## Executive Summary

Leverage Odoo's eLearning module (`website_slides`) for all UI/UX, and populate it from local `.md` files on module upgrade. Add a thin redirect layer for stable shareable URLs.

**Key Benefits:**
- Get eLearning's battle-tested UI for FREE (sidebar, fullscreen, search, responsive)
- Training mode gives hierarchical collapsible sidebar
- ~200 lines of custom code instead of 1000+
- Stable `/sam_insights/` URLs that never change

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         URL LAYERS                                       │
│                                                                          │
│  STABLE (Share with AI)          eLEARNING (Actual Content)             │
│  ━━━━━━━━━━━━━━━━━━━━━━          ━━━━━━━━━━━━━━━━━━━━━━━━━              │
│  /sam_insights/<slug>    ──────→  /slides/<channel>/<slide>             │
│                          redirect                                        │
│                                                                          │
│  Examples:                                                               │
│  /sam_insights/cto-capabilities  → /slides/sam-skills/cto-capabilities  │
│  /sam_insights/ai-brain-schema   → /slides/modules/ai-brain-schema      │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                         DATA FLOW                                        │
│                                                                          │
│  docs/*.md files                                                         │
│       │                                                                  │
│       ▼                                                                  │
│  build_courses.py (runs on -u upgrade)                                  │
│       │                                                                  │
│       ▼                                                                  │
│  slide.channel (Courses) + slide.slide (Content)                        │
│       │                                                                  │
│       ▼                                                                  │
│  eLearning Templates (website_slides)                                   │
│       │                                                                  │
│       ▼                                                                  │
│  /slides/... URLs (with training mode sidebar)                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Folder Structure

```
ai_sam_documentation/
│
├── __manifest__.py
├── __init__.py
│
├── docs/                                ← KNOWLEDGE SOURCE
│   ├── _url_registry.json               ← Stable slug mappings
│   ├── _course_config.json              ← Course metadata
│   │
│   ├── 00_sam_skills/                   → Creates Course "SAM Skills"
│   │   ├── cto/                         → Section "CTO"
│   │   │   ├── capabilities.md          → Slide (article)
│   │   │   └── workflow.md              → Slide (article)
│   │   └── developer/                   → Section "Developer"
│   │       └── patterns.md              → Slide (article)
│   │
│   ├── 01_modules/                      → Creates Course "Modules"
│   │   ├── ai_brain/                    → Section "AI Brain"
│   │   │   ├── description.md
│   │   │   └── schema.md
│   │   └── ai_sam/                      → Section "AI SAM"
│   │
│   ├── 02_data_flows/                   → Creates Course "Data Flows"
│   │   ├── apis/
│   │   ├── chat/
│   │   ├── node_creation/
│   │   └── system_prompt_builder/
│   │
│   ├── 03_platform_skins/               → Creates Course "Platform Skins"
│   │
│   ├── 04_architecture/                 → Creates Course "Architecture"
│   │
│   └── 05_vision/                       → Creates Course "Vision"
│
├── controllers/
│   ├── __init__.py
│   └── redirect_controller.py           ← /sam_insights/ redirect
│
├── scripts/
│   ├── __init__.py
│   └── build_courses.py                 ← Main build script
│
├── data/
│   └── website_menu.xml                 ← Optional menu items
│
├── security/
│   └── ir.model.access.csv              ← Minimal (if needed)
│
└── static/
    └── description/
        └── icon.png
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
    'category': 'Website/eLearning',
    'license': 'LGPL-3',
    'summary': 'SAM AI Knowledge System - File-based eLearning content',
    'description': """
SAM AI Documentation & Insights
================================

Knowledge publishing system built on Odoo eLearning.

Features:
- Markdown files auto-convert to eLearning content
- Hierarchical sidebar navigation (training mode)
- Stable /sam_insights/ URLs for AI sessions
- Sync on module upgrade

Source: docs/*.md files
URLs: /sam_insights/<slug> (stable) → /slides/... (eLearning)
    """,
    'depends': [
        'website_slides',  # eLearning - provides all UI
    ],
    'data': [
        # 'security/ir.model.access.csv',
        # 'data/website_menu.xml',
    ],
    'post_init_hook': 'post_init_hook',
    'post_load': None,
    'images': ['static/description/icon.png'],
    'installable': True,
    'application': False,
    'auto_install': False,
}
```

### Task 1.2: Create Root __init__.py

**File**: `__init__.py`

```python
from . import controllers
from .scripts.build_courses import build_courses


def post_init_hook(env):
    """Build courses from docs/ folder after install/upgrade."""
    build_courses(env)
```

### Task 1.3: Create URL Registry

**File**: `docs/_url_registry.json`

```json
{
  "_meta": {
    "description": "Maps stable /sam_insights/ slugs to eLearning locations",
    "note": "When content moves, update target_channel/target_slide here. Slug never changes.",
    "updated": "2025-01-02"
  },
  "redirects": {
    "cto-capabilities": {
      "target_channel": "00-sam-skills",
      "target_slide": "cto-capabilities",
      "title": "CTO Capabilities",
      "created": "2025-01-02"
    },
    "ai-brain-overview": {
      "target_channel": "01-modules",
      "target_slide": "ai-brain-description",
      "title": "AI Brain Overview",
      "created": "2025-01-02"
    }
  }
}
```

### Task 1.4: Create Course Config

**File**: `docs/_course_config.json`

```json
{
  "_meta": {
    "description": "Configuration for auto-generated courses",
    "updated": "2025-01-02"
  },
  "courses": {
    "00_sam_skills": {
      "name": "SAM Skills",
      "description": "Agent capabilities and skills documentation",
      "channel_type": "training",
      "sequence": 0,
      "visibility": "members",
      "enroll": "invite"
    },
    "01_modules": {
      "name": "Modules",
      "description": "Per-module reference documentation",
      "channel_type": "training",
      "sequence": 10,
      "visibility": "members",
      "enroll": "invite"
    },
    "02_data_flows": {
      "name": "Data Flows",
      "description": "How data moves through the system",
      "channel_type": "training",
      "sequence": 20,
      "visibility": "members",
      "enroll": "invite"
    },
    "03_platform_skins": {
      "name": "Platform Skins",
      "description": "How platform skins work",
      "channel_type": "training",
      "sequence": 30,
      "visibility": "members",
      "enroll": "invite"
    },
    "04_architecture": {
      "name": "Architecture",
      "description": "High-level patterns and decisions",
      "channel_type": "training",
      "sequence": 40,
      "visibility": "members",
      "enroll": "invite"
    },
    "05_vision": {
      "name": "Vision",
      "description": "Strategic direction",
      "channel_type": "training",
      "sequence": 50,
      "visibility": "members",
      "enroll": "invite"
    }
  },
  "defaults": {
    "channel_type": "training",
    "visibility": "members",
    "enroll": "invite",
    "allow_comment": false
  }
}
```

---

## Phase 2: Build Script

### Task 2.1: Create Build Script

**File**: `scripts/__init__.py`

```python
from . import build_courses
```

**File**: `scripts/build_courses.py`

```python
"""
Build eLearning courses from docs/ folder structure.

Folder structure:
  docs/
    00_sam_skills/        → slide.channel (Course)
      cto/                → slide.slide (is_category=True, Section)
        capabilities.md   → slide.slide (article content)

Runs on module install/upgrade via post_init_hook.
"""

import json
import logging
import re
from pathlib import Path
from datetime import datetime

_logger = logging.getLogger(__name__)

# Optional markdown - fallback to basic if not available
try:
    import markdown
    MARKDOWN_AVAILABLE = True
except ImportError:
    MARKDOWN_AVAILABLE = False
    _logger.warning("markdown library not installed. Using basic conversion.")


def get_module_path():
    """Get the ai_sam_documentation module path."""
    from odoo.modules.module import get_module_path as odoo_get_module_path
    return Path(odoo_get_module_path('ai_sam_documentation'))


def load_json_config(filename):
    """Load a JSON config file from docs/."""
    config_path = get_module_path() / 'docs' / filename
    if config_path.exists():
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}


def slugify(text):
    """Convert text to URL-safe slug."""
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    return text


def convert_md_to_html(content):
    """Convert markdown content to HTML."""
    if MARKDOWN_AVAILABLE:
        return markdown.markdown(
            content,
            extensions=['tables', 'fenced_code', 'toc', 'meta', 'nl2br']
        )
    else:
        # Basic conversion
        html = content
        html = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
        html = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
        html = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
        html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
        html = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html)
        html = re.sub(r'```(\w*)\n(.*?)```', r'<pre><code class="language-\1">\2</code></pre>', html, flags=re.DOTALL)
        html = re.sub(r'`(.+?)`', r'<code>\1</code>', html)
        html = html.replace('\n\n', '</p><p>')
        return f'<div class="markdown-content"><p>{html}</p></div>'


def extract_title_from_md(content, filename):
    """Extract title from markdown content or filename."""
    # Try to find # Title at start
    match = re.match(r'^#\s+(.+)$', content.strip(), re.MULTILINE)
    if match:
        return match.group(1).strip()
    # Fall back to filename
    return filename.replace('.md', '').replace('_', ' ').replace('-', ' ').title()


def get_or_create_channel(env, folder_name, config):
    """Get or create a slide.channel for the given folder."""
    Channel = env['slide.channel']

    # Get config for this course
    course_config = config.get('courses', {}).get(folder_name, {})
    defaults = config.get('defaults', {})

    # Generate slug from folder name (e.g., "00_sam_skills" → "00-sam-skills")
    channel_slug = folder_name.replace('_', '-')

    # Check if channel exists (by website_slug or name pattern)
    # website_slug might not exist, so we search by name pattern
    display_name = course_config.get('name', folder_name.replace('_', ' ').title())

    existing = Channel.search([
        '|',
        ('name', '=', display_name),
        ('name', 'ilike', f'%{display_name}%')
    ], limit=1)

    if existing:
        _logger.info(f"Found existing channel: {existing.name}")
        return existing

    # Create new channel
    vals = {
        'name': display_name,
        'description': course_config.get('description', ''),
        'channel_type': course_config.get('channel_type', defaults.get('channel_type', 'training')),
        'visibility': course_config.get('visibility', defaults.get('visibility', 'members')),
        'enroll': course_config.get('enroll', defaults.get('enroll', 'invite')),
        'allow_comment': course_config.get('allow_comment', defaults.get('allow_comment', False)),
        'sequence': course_config.get('sequence', 50),
        'is_published': False,  # Start unpublished
    }

    channel = Channel.create(vals)
    _logger.info(f"Created channel: {channel.name}")
    return channel


def get_or_create_section(env, channel, section_name, sequence):
    """Get or create a section (slide with is_category=True)."""
    Slide = env['slide.slide']

    display_name = section_name.replace('_', ' ').replace('-', ' ').title()

    existing = Slide.search([
        ('channel_id', '=', channel.id),
        ('is_category', '=', True),
        ('name', '=', display_name)
    ], limit=1)

    if existing:
        return existing

    section = Slide.create({
        'name': display_name,
        'channel_id': channel.id,
        'is_category': True,
        'is_published': False,
        'sequence': sequence,
    })
    _logger.info(f"Created section: {section.name} in {channel.name}")
    return section


def get_or_create_slide(env, channel, section, md_file, sequence):
    """Get or create a slide from markdown file."""
    Slide = env['slide.slide']

    # Read markdown content
    content_md = md_file.read_text(encoding='utf-8')
    title = extract_title_from_md(content_md, md_file.name)
    content_html = convert_md_to_html(content_md)

    # Generate slug
    slug = slugify(md_file.stem)

    # Check if slide exists
    existing = Slide.search([
        ('channel_id', '=', channel.id),
        ('name', '=', title)
    ], limit=1)

    if existing:
        # Update content
        existing.write({
            'html_content': content_html,
        })
        _logger.info(f"Updated slide: {existing.name}")
        return existing

    # Create new slide
    slide = Slide.create({
        'name': title,
        'channel_id': channel.id,
        'slide_category': 'article',  # Use article type for .md content
        'html_content': content_html,
        'is_published': False,
        'is_preview': False,
        'sequence': sequence,
    })
    _logger.info(f"Created slide: {slide.name} in {channel.name}")
    return slide


def build_courses(env):
    """Main entry point - build all courses from docs/ folder."""
    _logger.info("=" * 60)
    _logger.info("Building SAM AI Courses from docs/ folder...")
    _logger.info("=" * 60)

    module_path = get_module_path()
    docs_path = module_path / 'docs'

    if not docs_path.exists():
        _logger.warning(f"docs/ folder not found at {docs_path}")
        return

    # Load configuration
    course_config = load_json_config('_course_config.json')

    # Track statistics
    stats = {
        'channels': 0,
        'sections': 0,
        'slides': 0,
    }

    # Process each numbered folder (00_*, 01_*, etc.)
    course_folders = sorted([
        f for f in docs_path.iterdir()
        if f.is_dir() and not f.name.startswith('_') and re.match(r'^\d{2}_', f.name)
    ])

    for course_folder in course_folders:
        _logger.info(f"\nProcessing course folder: {course_folder.name}")

        # Create/get channel
        channel = get_or_create_channel(env, course_folder.name, course_config)
        stats['channels'] += 1

        # Process subfolders as sections
        section_sequence = 0
        for section_folder in sorted(course_folder.iterdir()):
            if not section_folder.is_dir():
                continue
            if section_folder.name.startswith('_'):
                continue

            section_sequence += 10
            section = get_or_create_section(env, channel, section_folder.name, section_sequence)
            stats['sections'] += 1

            # Process .md files in section
            slide_sequence = 0
            for md_file in sorted(section_folder.glob('*.md')):
                slide_sequence += 10
                slide = get_or_create_slide(env, channel, section, md_file, slide_sequence)
                stats['slides'] += 1

        # Also process .md files directly in course folder (no section)
        slide_sequence = 1000  # High sequence to put at end
        for md_file in sorted(course_folder.glob('*.md')):
            slide_sequence += 10
            slide = get_or_create_slide(env, channel, None, md_file, slide_sequence)
            stats['slides'] += 1

    _logger.info("=" * 60)
    _logger.info(f"Build complete!")
    _logger.info(f"  Channels: {stats['channels']}")
    _logger.info(f"  Sections: {stats['sections']}")
    _logger.info(f"  Slides:   {stats['slides']}")
    _logger.info("=" * 60)

    # Commit to ensure data is saved
    env.cr.commit()
```

---

## Phase 3: Redirect Controller

### Task 3.1: Create Redirect Controller

**File**: `controllers/__init__.py`

```python
from . import redirect_controller
```

**File**: `controllers/redirect_controller.py`

```python
"""
Redirect controller for stable /sam_insights/ URLs.

Maps stable slugs to actual eLearning URLs.
Allows content to be reorganized without breaking shared links.
"""

import json
import logging
from pathlib import Path

from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class SamInsightsRedirect(http.Controller):

    def _load_registry(self):
        """Load URL registry from JSON file."""
        from odoo.modules.module import get_module_path
        module_path = Path(get_module_path('ai_sam_documentation'))
        registry_path = module_path / 'docs' / '_url_registry.json'

        if registry_path.exists():
            with open(registry_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {'redirects': {}}

    @http.route('/sam_insights', type='http', auth='public', website=True)
    def insights_index(self, **kwargs):
        """Index page - redirect to eLearning courses list or custom page."""
        return request.redirect('/slides')

    @http.route('/sam_insights/<string:slug>', type='http', auth='public', website=True)
    def insight_redirect(self, slug, **kwargs):
        """Redirect stable slug to actual eLearning URL."""
        registry = self._load_registry()
        redirects = registry.get('redirects', {})

        if slug in redirects:
            entry = redirects[slug]
            target_channel = entry.get('target_channel', '')
            target_slide = entry.get('target_slide', '')

            # Build eLearning URL
            if target_slide:
                target_url = f'/slides/slide/{target_slide}'
            elif target_channel:
                target_url = f'/slides/{target_channel}'
            else:
                target_url = '/slides'

            _logger.debug(f"Redirecting /sam_insights/{slug} → {target_url}")
            return request.redirect(target_url)

        # Slug not found - try to find by searching slides
        Slide = request.env['slide.slide'].sudo()
        slide = Slide.search([
            ('name', 'ilike', slug.replace('-', ' ')),
            ('is_category', '=', False)
        ], limit=1)

        if slide:
            return request.redirect(f'/slides/slide/{slide.id}')

        # Not found
        _logger.warning(f"SAM Insights slug not found: {slug}")
        return request.redirect('/slides')

    @http.route('/sam_insights/course/<string:course_slug>', type='http', auth='public', website=True)
    def course_redirect(self, course_slug, **kwargs):
        """Redirect to a course/channel."""
        Channel = request.env['slide.channel'].sudo()

        # Try to find channel by slug pattern
        search_name = course_slug.replace('-', ' ').replace('_', ' ')
        channel = Channel.search([
            ('name', 'ilike', f'%{search_name}%')
        ], limit=1)

        if channel:
            return request.redirect(f'/slides/{channel.id}')

        return request.redirect('/slides')
```

---

## Phase 4: Initial Content Setup

### Task 4.1: Create Folder Structure

```bash
cd D:\SAMAI-18-SaaS\github-repos\05-samai-core\ai_sam_documentation

# Create docs structure
mkdir -p docs/00_sam_skills/cto
mkdir -p docs/00_sam_skills/developer
mkdir -p docs/00_sam_skills/architect
mkdir -p docs/01_modules/ai_brain
mkdir -p docs/01_modules/ai_sam
mkdir -p docs/01_modules/ai_sam_workflows
mkdir -p docs/02_data_flows/apis
mkdir -p docs/02_data_flows/chat
mkdir -p docs/02_data_flows/node_creation
mkdir -p docs/02_data_flows/system_prompt_builder
mkdir -p docs/03_platform_skins
mkdir -p docs/04_architecture
mkdir -p docs/05_vision

# Create controller folder
mkdir -p controllers

# Create scripts folder
mkdir -p scripts
```

### Task 4.2: Create Sample Content

**File**: `docs/00_sam_skills/cto/capabilities.md`

```markdown
# CTO Capabilities

The CTO agent provides strategic technical leadership.

## Core Capabilities

- Infrastructure strategy and planning
- Technology stack decisions
- Scalability architecture
- Security oversight

## When to Use

Use the CTO agent when you need:
- High-level architectural decisions
- Technology evaluation
- Strategic technical planning

## Invocation

```
/cto
```
```

**File**: `docs/01_modules/ai_brain/description.md`

```markdown
# AI Brain Module

The foundation data layer of SAM AI.

## Purpose

AI Brain (`ai_brain`) is the core data layer where ALL models live.
Platform skins can be uninstalled without losing data.

## Key Models

- `canvas` - Workflow canvas
- `nodes` - Canvas nodes
- `ai.conversation` - Chat conversations
- `ai.message` - Chat messages

## Philosophy

"The Brain" - permanent data storage, never uninstall.
```

---

## Phase 5: Testing & Validation

### Task 5.1: Install and Test

```bash
# Upgrade module
./odoo-bin -u ai_sam_documentation -d your_database

# Check logs for build output
# Should see: "Building SAM AI Courses from docs/ folder..."
```

### Task 5.2: Validation Checklist

- [ ] Module installs without errors
- [ ] Courses appear in eLearning (/slides)
- [ ] Each numbered folder creates a Course
- [ ] Subfolders create Sections (collapsible in sidebar)
- [ ] .md files create Article slides
- [ ] Content displays correctly (HTML from markdown)
- [ ] `/sam_insights/<slug>` redirects work
- [ ] Training mode sidebar shows hierarchy

---

## Mapping Reference

### Folder → eLearning

| Folder Structure | eLearning Equivalent |
|------------------|----------------------|
| `docs/00_sam_skills/` | `slide.channel` (Course) |
| `docs/00_sam_skills/cto/` | `slide.slide` (is_category=True, Section) |
| `docs/00_sam_skills/cto/capabilities.md` | `slide.slide` (article) |

### URL Mapping

| Stable URL | Redirects To |
|------------|--------------|
| `/sam_insights/` | `/slides` |
| `/sam_insights/cto-capabilities` | `/slides/slide/<id>` |
| `/sam_insights/course/sam-skills` | `/slides/<channel_id>` |

---

## Future Enhancements (Not in Scope)

- Auto-generate `_url_registry.json` from slides
- Search across all insights
- API endpoint for AI sessions to fetch content
- Webhook to rebuild on git push
- Custom eLearning template overrides (if needed)

---

## Developer Handoff

When ready to implement, start a developer session with:

```
Implement the SAM Insights eLearning wrapper.

Plan: D:\SAMAI-18-SaaS\github-repos\05-samai-core\ai_sam_documentation\plans\2025-01-02_sam_insights_architecture_v2.md

Start with Phase 1 (manifest, __init__.py, config files).
Then Phase 2 (build script).
Then Phase 3 (redirect controller).
Then Phase 4 (create folder structure and sample content).

The module depends on website_slides (eLearning).
We are NOT creating custom models - we populate slide.channel and slide.slide.
```

---

**End of Plan v2**
