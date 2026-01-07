# Developer Session Prompt: SAM Insights eLearning Wrapper

**Created**: 2025-01-02
**Type**: Implementation Session
**Module**: ai_sam_documentation

---

## Context

You are implementing a knowledge publishing system for SAM AI that wraps Odoo's eLearning module (`website_slides`). The architecture has been planned and approved.

**Key Decision**: We are NOT creating custom models. We populate `slide.channel` and `slide.slide` from local `.md` files on module upgrade.

---

## Your Task

Implement the SAM Insights eLearning wrapper as specified in the architecture plan.

**Plan Location**:
```
D:\SAMAI-18-SaaS\github-repos\05-samai-core\ai_sam_documentation\plans\2025-01-02_sam_insights_architecture_v2.md
```

**Read this plan FIRST before implementing anything.**

---

## Implementation Order

### Phase 1: Foundation
1. Update `__manifest__.py` (depends on `website_slides`)
2. Update root `__init__.py` with post_init_hook
3. Create `docs/_url_registry.json`
4. Create `docs/_course_config.json`

### Phase 2: Build Script
1. Create `scripts/__init__.py`
2. Create `scripts/build_courses.py` (main logic)

### Phase 3: Redirect Controller
1. Create `controllers/__init__.py`
2. Create `controllers/redirect_controller.py`

### Phase 4: Folder Structure & Sample Content
1. Create folder structure in `docs/`
2. Create sample `.md` files for testing

---

## Key Technical Details

### Module Location
```
D:\SAMAI-18-SaaS\github-repos\05-samai-core\ai_sam_documentation\
```

### Dependency
```python
'depends': ['website_slides']
```

### Folder → eLearning Mapping
```
docs/00_sam_skills/           → slide.channel (Course)
docs/00_sam_skills/cto/       → slide.slide (is_category=True, Section)
docs/00_sam_skills/cto/x.md   → slide.slide (article content)
```

### URL Pattern
```
/sam_insights/<slug>  → redirects to → /slides/slide/<id>
```

### Channel Type
Use `channel_type='training'` for hierarchical sidebar navigation.

---

## What Already Exists

The module folder exists with some old files. You may need to:
- Clean up old files that conflict
- Keep the `docs/` folder content (existing .md files may be migrated later)
- Update manifest and init files

---

## Validation

After implementation:
1. Install module: `-u ai_sam_documentation`
2. Check Odoo logs for "Building SAM AI Courses..."
3. Visit `/slides` - courses should appear
4. Visit `/sam_insights/` - should redirect to `/slides`
5. Check sidebar shows hierarchical navigation (training mode)

---

## Do NOT

- Create custom models (use slide.channel, slide.slide)
- Create custom templates (use eLearning templates)
- Overthink it - this is a thin wrapper, ~200 lines of code
- Change the URL registry structure without discussing

---

## Questions?

If you hit blockers or need clarification, ask. The architecture decisions have been made - focus on clean implementation.

---

**Start by reading the full plan, then implement Phase 1.**
