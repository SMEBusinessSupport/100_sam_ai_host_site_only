#!/usr/bin/env python3
"""
Fix Odoo Stuck Upgrade - Clean broken model references
Run this in Odoo shell: python odoo-bin shell -d ai_automator_db < fix_stuck_upgrade.py
"""

# 1. Find and remove broken ir.model entries
broken_models = [
    'privacy.log',
    'privacy.lookup.wizard',
    'privacy.lookup.wizard.line'
]

print("🔍 Searching for broken model references...")

for model_name in broken_models:
    # Remove from ir.model
    broken_model = env['ir.model'].search([('model', '=', model_name)])
    if broken_model:
        print(f"  ❌ Found broken model: {model_name} (ID: {broken_model.id})")
        broken_model.unlink()
        print(f"  ✅ Deleted: {model_name}")
    else:
        print(f"  ℹ️  Model not found in ir.model: {model_name}")

    # Remove from ir.model.data (XML IDs)
    broken_data = env['ir.model.data'].search([('model', '=', model_name)])
    if broken_data:
        print(f"  ❌ Found {len(broken_data)} ir.model.data entries for {model_name}")
        broken_data.unlink()
        print(f"  ✅ Deleted ir.model.data entries")

    # Remove from ir.model.fields
    broken_fields = env['ir.model.fields'].search([('model', '=', model_name)])
    if broken_fields:
        print(f"  ❌ Found {len(broken_fields)} fields for {model_name}")
        broken_fields.unlink()
        print(f"  ✅ Deleted fields")

# 2. Find modules in 'to upgrade' or 'to install' state
print("\n🔍 Checking module states...")
stuck_modules = env['ir.module.module'].search([
    ('state', 'in', ['to upgrade', 'to install', 'to remove'])
])

if stuck_modules:
    print(f"  ⚠️  Found {len(stuck_modules)} stuck modules:")
    for mod in stuck_modules:
        print(f"     - {mod.name}: {mod.state}")
        # Reset to installed or uninstalled
        if mod.state == 'to upgrade':
            mod.state = 'installed'
            print(f"     ✅ Reset {mod.name} to 'installed'")
        elif mod.state == 'to install':
            mod.state = 'uninstalled'
            print(f"     ✅ Reset {mod.name} to 'uninstalled'")
        elif mod.state == 'to remove':
            mod.state = 'uninstalled'
            print(f"     ✅ Reset {mod.name} to 'uninstalled'")
else:
    print("  ✅ No stuck modules found")

# 3. Clear registry cache
print("\n🔄 Clearing registry cache...")
env.registry.clear_caches()
print("  ✅ Cache cleared")

# 4. Commit changes
env.cr.commit()
print("\n✅ ALL FIXES APPLIED! Restart Odoo now.")
print("\nRestart command:")
print("  sc stop odoo-server && sc start odoo-server")
