# -*- coding: utf-8 -*-
{
    'name': 'SAM AI Insights',
    'version': '18.0.1.0',
    'category': 'Productivity/AI',
    'summary': 'Ecosystem Intelligence - Track, Trace, and Analyze the SAM AI Codebase',
    'description': """
SAM AI Insights - Ecosystem Intelligence Tool
==============================================

A comprehensive analysis tool that knows EVERYTHING about your SAM AI ecosystem.

**What It Detects:**

Dangling References:
- Views referencing non-existent fields
- Actions pointing to deleted models
- Menu items with broken actions
- JS components calling undefined Python methods

Redundant Code:
- Multiple models doing similar things (similarity scoring)
- Duplicate utility functions across modules
- CSS classes defined multiple times
- JS functions with same logic, different names

Orphaned Assets:
- JS files not in any asset bundle
- CSS not imported anywhere
- Python files not imported in __init__.py
- XML views never rendered

Relationship Mapping:
- Model → Views → Actions → Menus (full trace)
- Field usage across all views
- JS ↔ Python controller mappings
- Module dependency graph

**Features:**
- Static analysis (AST parsing for Python, XML parsing for views)
- Runtime analysis (queries Odoo registry)
- Duplicate detection with similarity scoring
- HTML/JSON report generation
- Dashboard with ecosystem health metrics
- Scheduled weekly scans
- Integration with SAM Chat for natural language queries

**Architecture:**
Scanner → Analyzer → Reporter → Dashboard
    """,
    'author': 'SAM AI',
    'website': 'https://samai.com',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'web',
        'ai_sam_base',
    ],
    'data': [
        # Security
        'security/ir.model.access.csv',

        # Data
        'data/scheduled_actions.xml',

        # Views
        'views/insights_settings_views.xml',
        'views/insights_scan_views.xml',
        'views/insights_finding_views.xml',
        'views/insights_dashboard_views.xml',
        'views/insights_menus.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'ai_sam_insights/static/src/css/insights_dashboard.css',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
}
