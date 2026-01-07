# -*- coding: utf-8 -*-
{
    'name': 'SAM AI - Development Mode',
    'version': '18.0.1.1.0',
    'category': 'SAM AI/Development',
    'summary': 'Enables SAM AI development mode with enhanced debugging and testing features',
    'description': """
SAM AI - Development Mode
=========================

**Install this module to enable SAM AI Development Mode.**

When installed, this module enables:

**SAM Chat Dev Features:**
- System prompt injected on every message (for testing prompt changes)
- Verbose debug logging in Odoo logs
- Debug files written (debug_last_prompt.md, etc.)
- Enhanced error messages

**Module Catalog Dev Features:**
- Pre-configured local filesystem repository paths
- Prefer local copy over GitHub API
- Auto-scan of local repositories

**System Parameters Set:**
- ``sam.dev_mode`` = True (master dev flag)
- ``sam.always_inject_prompt`` = True
- ``sam.debug_logging`` = True
- ``sam.write_debug_files`` = True

**For Development Only:**
This module should NOT be deployed to production SaaS clients.
Uninstalling this module reverts SAM to production mode behavior.

Author: Better Business Builders
License: LGPL-3
    """,
    'author': 'Better Business Builders',
    'website': 'https://betterbusinessbuilders.com.au',
    'license': 'LGPL-3',
    'depends': [
        'ai_sam_base',
        'sam_ai_odoo_modules',
    ],
    'data': [
        # Pre-configured repositories and settings
        'data/dev_repository_data.xml',
        'data/dev_config_data.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'post_init_hook': 'post_init_hook',
    'uninstall_hook': 'uninstall_hook',
}
