#!/usr/bin/env python3
"""
Quick script to check and update SAM AI config credit balance
"""
import xmlrpc.client

# Odoo connection settings
url = 'http://localhost:8069'
db = 'odoo_db_v18'  # Try this database first
username = 'admin'
password = 'admin'

# Connect to Odoo
common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
uid = common.authenticate(db, username, password, {})

if not uid:
    print(f"❌ Failed to authenticate to database: {db}")
    print("Try one of these databases:")
    print("  - odoo18")
    print("  - odoo_db")
    print("  - odoo_db_v18")
    exit(1)

print(f"✅ Authenticated as user ID: {uid}")

# Get models object
models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')

# Search for active AI config
config_ids = models.execute_kw(
    db, uid, password,
    'ai.service.config', 'search',
    [[('active', '=', True)]]
)

if not config_ids:
    print("❌ No active AI service config found!")
    exit(1)

print(f"✅ Found active config ID: {config_ids[0]}")

# Read config data
config = models.execute_kw(
    db, uid, password,
    'ai.service.config', 'read',
    [config_ids],
    {'fields': ['name', 'api_provider', 'model_name', 'total_cost', 'credit_balance', 'remaining_balance', 'balance_percentage']}
)[0]

print(f"\n📊 Current Config ({config['name']}):")
print(f"  Provider: {config['api_provider']}")
print(f"  Model: {config['model_name']}")
print(f"  Total Cost: ${config['total_cost']:.2f}")
print(f"  Credit Balance: ${config['credit_balance']:.2f}")
print(f"  Remaining Balance: ${config['remaining_balance']:.2f}")
print(f"  Balance %: {config['balance_percentage']:.1f}%")

# Update credit balance to $5.00 if it's 0
if config['credit_balance'] == 0.0:
    print(f"\n🔧 Setting credit_balance to $5.00...")
    models.execute_kw(
        db, uid, password,
        'ai.service.config', 'write',
        [[config_ids[0]], {'credit_balance': 5.00}]
    )

    # Re-read to confirm
    updated_config = models.execute_kw(
        db, uid, password,
        'ai.service.config', 'read',
        [config_ids],
        {'fields': ['credit_balance', 'remaining_balance', 'balance_percentage']}
    )[0]

    print(f"✅ Updated!")
    print(f"  Credit Balance: ${updated_config['credit_balance']:.2f}")
    print(f"  Remaining Balance: ${updated_config['remaining_balance']:.2f}")
    print(f"  Balance %: {updated_config['balance_percentage']:.1f}%")
else:
    print(f"\n✅ Credit balance already set to ${config['credit_balance']:.2f}")

print("\n🎯 Now refresh your browser to see the updated token counter!")
