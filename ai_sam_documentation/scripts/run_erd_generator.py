#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Standalone ERD Generator Runner

Run this script from the Odoo server directory to generate the ERD
without needing to reinstall the module.

Usage:
    cd "C:\Program Files\SAM AI\server"
    python -c "from odoo.cli import main; main()" shell -c odoo.conf -d sam_ai < path/to/run_erd_generator.py

Or simpler - just use Odoo shell:
    python odoo-bin shell -c odoo.conf -d sam_ai

Then in the shell:
    from ai_sam_documentation.scripts.generate_erd import generate_erd
    generate_erd(env)
    env.cr.commit()
"""

if __name__ == '__main__':
    print("""
To generate the ERD, run Odoo shell and execute:

    cd "C:\\Program Files\\SAM AI\\server"
    python odoo-bin shell -c odoo.conf -d sam_ai

Then in the shell:
    >>> from ai_sam_documentation.scripts.generate_erd import generate_erd
    >>> generate_erd(env)
    >>> env.cr.commit()
    >>> exit()

The ERD will be generated at:
    D:\\SAMAI-18-SaaS\\github-repos\\05-samai-core\\ai_sam_documentation\\docs\\05_architecture\\SAM_AI_ERD.md
""")
