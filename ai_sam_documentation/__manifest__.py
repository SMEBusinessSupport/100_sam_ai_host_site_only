# -*- coding: utf-8 -*-
{
    'name': 'SAM AI Documentation & Insights',
    'version': '18.0.4.0.0',
    'author': 'Anthony Gardiner - Odoo Consulting & Claude AI',
    'maintainer': 'Anthony Gardiner <anthony@sme.ec>',
    'website': 'https://sme.ec',
    'category': 'Website/eLearning',
    'license': 'LGPL-3',
    'summary': 'SAM AI Knowledge System - File-based eLearning content with Documentation Hub',
    'description': """
SAM AI Documentation & Insights
===============================

Knowledge publishing system built on Odoo eLearning with a standalone Documentation Hub.

Features:
- Markdown files auto-convert to eLearning content
- **NEW: /documentation/ route** - GitBook-style standalone documentation viewer
- Hierarchical sidebar navigation
- Stable /sam_insights/ URLs for AI sessions
- Full multimedia support (video, images, code highlighting)
- Search functionality across all documentation
- Sync on module upgrade

URLs:
- /documentation/ - Standalone GitBook-style documentation hub
- /documentation/<section>/<article> - Direct article links
- /sam_insights/<slug> (stable) -> /slides/... (eLearning)

Architecture:
- Uses website_slides (eLearning) as content backend
- Custom /documentation/ frontend with GitBook/ReadTheDocs styling
- Populates slide.channel and slide.slide from local .md files
- Runs build script on module install/upgrade via post_init_hook
    """,
    'depends': [
        'website_slides',       # eLearning - provides content backend
    ],
    'data': [
        'data/channel_tags.xml',
        'data/website_menus.xml',
        'views/documentation_hub_templates.xml',
    ],
    'post_init_hook': 'post_init_hook',
    'assets': {
        'web.assets_frontend': [
            'ai_sam_documentation/static/src/scss/documentation_hub.scss',
            'ai_sam_documentation/static/src/js/documentation_hub.js',
        ],
    },
    'images': ['static/description/icon.png'],
    'installable': True,
    'application': False,
    'auto_install': False,
    'sequence': 110,
}
