# SAM AI Documentation & Insights

**Technical Name**: `ai_sam_documentation`
**Version**: 18.0.3.0.0

SAM AI Knowledge System - File-based eLearning content

## Description


SAM AI Documentation & Insights
===============================

Knowledge publishing system built on Odoo eLearning.

Features:
- Markdown files auto-convert to eLearning content
- Hierarchical sidebar navigation (training mode)
- Stable /sam_insights/ URLs for AI sessions
- Sync on module upgrade

Source: docs/*.md files
URLs: /sam_insights/<slug> (stable) -> /slides/... (eLearning)

Architecture:
- Uses website_slides (eLearning) for all UI
- Populates slide.channel and slide.slide from local .md files
- Runs build script on module install/upgrade via post_init_hook
    

## Dependencies

- `website_slides`
