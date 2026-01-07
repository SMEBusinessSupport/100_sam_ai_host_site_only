"""
Quick script to reload agents into ai_automator_db
"""
import sys
import os

# Add Odoo to path
sys.path.insert(0, r"C:\Program Files\Odoo 18\server")
os.chdir(r"C:\Working With AI\ai_sam\ai_sam")

import odoo
from odoo import api

# Initialize Odoo
odoo.tools.config.parse_config([
    '-c', r'C:\Program Files\Odoo 18\server\odoo.conf',
    '-d', 'ai_automator_db'
])

# Get registry and cursor
registry = odoo.registry('ai_automator_db')

with registry.cursor() as cr:
    # Import and run hook
    from odoo.addons.ai_sam_intelligence import hooks

    print("Running agent reload hook...")
    hooks.post_init_hook(cr, registry)
    cr.commit()
    print("Done!")

    # Verify
    env = api.Environment(cr, 1, {})  # SUPERUSER_ID = 1
    agents = env['ai.agent.registry'].search([])

    print(f"\nLoaded {len(agents)} agents:")
    for agent in agents:
        prompt_length = len(agent.system_prompt) if agent.system_prompt else 0
        print(f"  - {agent.name}: {prompt_length:,} characters")
