# Developer Session Prompt v2: Migration Fix + Menu Segmentation

**Created**: 2025-01-02
**Type**: Bug Fix + Feature Enhancement
**Module**: ai_sam_documentation

---

## Context

The module was implemented but has two issues:
1. `post_init_hook` only runs on INSTALL, not UPGRADE - new .md files aren't being picked up
2. Need website menu segmentation for different audiences (Internal/Free/Premium)

---

## Task 1: Add Migration Script

### Problem
`post_init_hook` in `__manifest__.py` only runs on first install. When we add new .md files and upgrade the module, they don't get synced to eLearning.

### Solution
Create a migration script that runs `build_courses()` on every upgrade.

### Implementation

**Step 1: Create migrations folder structure**
```
ai_sam_documentation/
├── migrations/
│   └── 18.0.3.0.1/
│       └── post-migrate.py
```

**Step 2: Create migration script**

**File**: `migrations/18.0.3.0.1/post-migrate.py`
```python
# -*- coding: utf-8 -*-
import logging

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    """Run build_courses on module upgrade."""
    _logger.info("Running SAM AI Documentation migration...")

    # Import here to avoid issues during migration
    from odoo import api, SUPERUSER_ID
    from odoo.modules.module import get_module_path

    env = api.Environment(cr, SUPERUSER_ID, {})

    # Import and run build_courses
    try:
        from odoo.addons.ai_sam_documentation.scripts.build_courses import build_courses
        build_courses(env)
        _logger.info("SAM AI Documentation migration complete!")
    except Exception as e:
        _logger.error(f"Migration failed: {e}")
        raise
```

**Step 3: Bump version in manifest**

**File**: `__manifest__.py`
Change:
```python
'version': '18.0.3.0.0',
```
To:
```python
'version': '18.0.3.0.1',
```

### Testing
1. Add a new .md file to `docs/03_modules/` (or verify existing ones)
2. Run: `-u ai_sam_documentation`
3. Check Odoo logs for "Running SAM AI Documentation migration..."
4. Verify new slides appear in eLearning

---

## Task 2: Website Menu Segmentation

### Goal
Create separate website entry points for different audiences:

| Menu Item | URL | Shows Courses Tagged |
|-----------|-----|----------------------|
| SAM Docs | `/sam_insights/` | `internal` |
| Learn | `/learn/` | `free` |
| Training | `/training/` | `premium` |

### Implementation

**Step 1: Create channel tags via data file**

**File**: `data/channel_tags.xml`
```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <data noupdate="1">
        <!-- Channel Tags for filtering -->
        <record id="channel_tag_internal" model="slide.channel.tag">
            <field name="name">Internal</field>
        </record>
        <record id="channel_tag_free" model="slide.channel.tag">
            <field name="name">Free</field>
        </record>
        <record id="channel_tag_premium" model="slide.channel.tag">
            <field name="name">Premium</field>
        </record>
    </data>
</odoo>
```

**Step 2: Create website menu items**

**File**: `data/website_menus.xml`
```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <data>
        <!-- SAM Docs Menu (Internal) -->
        <record id="menu_sam_docs" model="website.menu">
            <field name="name">SAM Docs</field>
            <field name="url">/sam_insights/</field>
            <field name="parent_id" ref="website.main_menu"/>
            <field name="sequence">50</field>
        </record>

        <!-- Learn Menu (Free) -->
        <record id="menu_learn" model="website.menu">
            <field name="name">Learn</field>
            <field name="url">/learn/</field>
            <field name="parent_id" ref="website.main_menu"/>
            <field name="sequence">51</field>
        </record>

        <!-- Training Menu (Premium) -->
        <record id="menu_training" model="website.menu">
            <field name="name">Training</field>
            <field name="url">/training/</field>
            <field name="parent_id" ref="website.main_menu"/>
            <field name="sequence">52</field>
        </record>
    </data>
</odoo>
```

**Step 3: Update controller with filtered routes**

**File**: `controllers/redirect_controller.py`

Add these routes to the existing controller:

```python
@http.route('/sam_insights/', type='http', auth='user', website=True)
def sam_insights_index(self, **kwargs):
    """Internal documentation - requires login, shows 'internal' tagged courses."""
    Tag = request.env['slide.channel.tag'].sudo()
    internal_tag = Tag.search([('name', '=', 'Internal')], limit=1)

    domain = [('is_published', '=', True)]
    if internal_tag:
        domain.append(('tag_ids', 'in', [internal_tag.id]))

    channels = request.env['slide.channel'].sudo().search(domain)

    return request.render('website_slides.courses_home', {
        'channels': channels,
        'tag': internal_tag,
        'page_title': 'SAM Documentation',
    })


@http.route('/learn/', type='http', auth='public', website=True)
def learn_index(self, **kwargs):
    """Free courses - public access, shows 'free' tagged courses."""
    Tag = request.env['slide.channel.tag'].sudo()
    free_tag = Tag.search([('name', '=', 'Free')], limit=1)

    domain = [('is_published', '=', True)]
    if free_tag:
        domain.append(('tag_ids', 'in', [free_tag.id]))

    channels = request.env['slide.channel'].sudo().search(domain)

    return request.render('website_slides.courses_home', {
        'channels': channels,
        'tag': free_tag,
        'page_title': 'Learn',
    })


@http.route('/training/', type='http', auth='user', website=True)
def training_index(self, **kwargs):
    """Premium courses - requires login, shows 'premium' tagged courses."""
    Tag = request.env['slide.channel.tag'].sudo()
    premium_tag = Tag.search([('name', '=', 'Premium')], limit=1)

    domain = [('is_published', '=', True)]
    if premium_tag:
        domain.append(('tag_ids', 'in', [premium_tag.id]))

    channels = request.env['slide.channel'].sudo().search(domain)

    return request.render('website_slides.courses_home', {
        'channels': channels,
        'tag': premium_tag,
        'page_title': 'Training',
    })
```

**Step 4: Update manifest to include data files**

**File**: `__manifest__.py`
```python
'data': [
    'data/channel_tags.xml',
    'data/website_menus.xml',
],
```

**Step 5: Update build_courses.py to auto-tag internal courses**

In `get_or_create_channel()` function, add internal tag to created channels:

```python
def get_or_create_channel(env, folder_name, config):
    """Get or create a slide.channel for the given folder."""
    Channel = env['slide.channel']
    Tag = env['slide.channel.tag']

    # ... existing code ...

    # After creating channel, add internal tag
    if channel:
        internal_tag = Tag.search([('name', '=', 'Internal')], limit=1)
        if internal_tag and internal_tag not in channel.tag_ids:
            channel.write({'tag_ids': [(4, internal_tag.id)]})

    return channel
```

---

## Task 3: Bump Version for Migration

After all changes, ensure manifest version is:
```python
'version': '18.0.3.0.1',
```

---

## Files to Create/Modify

| File | Action |
|------|--------|
| `migrations/18.0.3.0.1/post-migrate.py` | CREATE |
| `data/channel_tags.xml` | CREATE |
| `data/website_menus.xml` | CREATE |
| `controllers/redirect_controller.py` | MODIFY (add routes) |
| `scripts/build_courses.py` | MODIFY (add auto-tagging) |
| `__manifest__.py` | MODIFY (version + data files) |

---

## Testing Checklist

- [ ] Module upgrades without errors
- [ ] Migration runs and logs "Running SAM AI Documentation migration..."
- [ ] New .md files from `03_modules/` appear as slides in eLearning
- [ ] `/sam_insights/` shows only Internal tagged courses
- [ ] `/learn/` shows only Free tagged courses (public access)
- [ ] `/training/` shows only Premium tagged courses (requires login)
- [ ] Website menu shows SAM Docs, Learn, Training links
- [ ] Existing courses get Internal tag applied

---

## Notes

- All current courses (00_vision through 07_development) should be tagged as `internal`
- The tags `free` and `premium` are created but no courses use them yet
- Menu items are created but will show empty until courses are tagged appropriately
- `/sam_insights/` requires login (`auth='user'`)
- `/learn/` is public (`auth='public'`)
- `/training/` requires login (`auth='user'`)

---

**Start with Task 1 (migration), then Task 2 (menus), then test.**
