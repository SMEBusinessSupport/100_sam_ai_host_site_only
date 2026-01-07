import os
import json
import csv
from pathlib import Path
from collections import Counter, defaultdict

# Path to n8n nodes
nodes_path = r"C:\Working With AI\Odoo Projects\custom-modules-v18\the_ai_automator\static\src\n8n\n8n_nodes"

print("=" * 80)
print("MASTER N8N KNOWLEDGE REPORT - ALL HIERARCHY LEVELS")
print("=" * 80)

all_rows = []
supplier_stats = {}
supplier_services = defaultdict(set)  # Track services per supplier

# Walk through all suppliers
for supplier_folder in os.listdir(nodes_path):
    supplier_path = os.path.join(nodes_path, supplier_folder)

    # Skip if not a directory
    if not os.path.isdir(supplier_path):
        continue

    supplier_name = supplier_folder

    # Initialize supplier stats
    if supplier_name not in supplier_stats:
        supplier_stats[supplier_name] = {
            'actions': 0,
            'triggers': 0,
            'total': 0
        }

    # Check if supplier has direct .node.js files (Type 2 - flat structure)
    supplier_node_js_files = [f for f in os.listdir(supplier_path) if f.endswith('.node.js') and os.path.isfile(os.path.join(supplier_path, f))]

    if supplier_node_js_files:
        # TYPE 2: Flat structure - supplier has direct nodes
        for node_file in supplier_node_js_files:
            node_name = node_file.replace('.node.js', '')
            node_path = os.path.join(supplier_path, node_file)

            # Look for corresponding .node.json
            json_file = node_file.replace('.node.js', '.node.json')
            json_path = os.path.join(supplier_path, json_file)

            categories = ''
            display_name = ''
            node_type = ''

            if os.path.exists(json_path):
                try:
                    with open(json_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        categories = '|'.join(data.get('categories', []))
                        display_name = data.get('displayName', '')
                        node_type = data.get('node', '')
                except:
                    pass

            # Determine if trigger or action
            node_classification = 'Trigger' if 'Trigger' in node_name else 'Action'

            # Update stats
            supplier_stats[supplier_name]['total'] += 1
            if node_classification == 'Trigger':
                supplier_stats[supplier_name]['triggers'] += 1
            else:
                supplier_stats[supplier_name]['actions'] += 1

            all_rows.append({
                'supplier': supplier_name,
                'supplier_actions': '',  # Will fill at end
                'supplier_triggers': '',  # Will fill at end
                'supplier_services': '',  # Will fill at end
                'structure_type': 'Flat (Type 2)',
                'l1_service': '',
                'l2_node_name': node_name,
                'l2_classification': node_classification,
                'l2_display_name': display_name,
                'l2_node_type': node_type,
                'l2_categories': categories,
                'l2_has_json': 'Yes' if os.path.exists(json_path) else 'No',
                'l3_resource': '',
                'l4_operation': '',
                'file_path': supplier_folder,
                'notes': 'Supplier has direct nodes'
            })

    # TYPE 1: Nested structure - scan for L1 services
    for l1_folder in os.listdir(supplier_path):
        l1_path = os.path.join(supplier_path, l1_folder)

        # Skip files and special folders
        if not os.path.isdir(l1_path) or l1_folder.startswith('__') or l1_folder in ['test', 'v1', 'v2', 'v3']:
            continue

        # Check if L1 folder contains .node.js files
        l1_node_js_files = [f for f in os.listdir(l1_path) if f.endswith('.node.js') and os.path.isfile(os.path.join(l1_path, f))]

        if not l1_node_js_files:
            continue

        l1_service_name = l1_folder

        # Track this service for the supplier
        supplier_services[supplier_name].add(l1_service_name)

        # Process each L2 node in this L1 service
        for node_file in l1_node_js_files:
            node_name = node_file.replace('.node.js', '')
            node_path = os.path.join(l1_path, node_file)

            # Look for corresponding .node.json
            json_file = node_file.replace('.node.js', '.node.json')
            json_path = os.path.join(l1_path, json_file)

            categories = ''
            display_name = ''
            node_type = ''
            resources = []

            if os.path.exists(json_path):
                try:
                    with open(json_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        categories = '|'.join(data.get('categories', []))
                        display_name = data.get('displayName', '')
                        node_type = data.get('node', '')
                except:
                    pass

            # Try to extract resources from .node.js file
            try:
                with open(node_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Look for resource definitions (simplified extraction)
                    if 'resource:' in content or 'resources:' in content:
                        # Basic resource detection
                        import re
                        resource_matches = re.findall(r"resource:\s*['\"](\w+)['\"]", content)
                        resources = list(set(resource_matches))[:5]  # Limit to 5 for readability
            except:
                pass

            # Determine if trigger or action
            node_classification = 'Trigger' if 'Trigger' in node_name else 'Action'

            # Update stats
            supplier_stats[supplier_name]['total'] += 1
            if node_classification == 'Trigger':
                supplier_stats[supplier_name]['triggers'] += 1
            else:
                supplier_stats[supplier_name]['actions'] += 1

            # Create row for L2 node
            if resources:
                for resource in resources:
                    all_rows.append({
                        'supplier': supplier_name,
                        'supplier_actions': '',  # Will fill at end
                        'supplier_triggers': '',  # Will fill at end
                        'supplier_services': '',  # Will fill at end
                        'structure_type': 'Nested (Type 1)',
                        'l1_service': l1_service_name,
                        'l2_node_name': node_name,
                        'l2_classification': node_classification,
                        'l2_display_name': display_name,
                        'l2_node_type': node_type,
                        'l2_categories': categories,
                        'l2_has_json': 'Yes' if os.path.exists(json_path) else 'No',
                        'l3_resource': resource,
                        'l4_operation': '',
                        'file_path': f"{supplier_folder}\\{l1_folder}",
                        'notes': 'Has resources detected'
                    })
            else:
                all_rows.append({
                    'supplier': supplier_name,
                    'supplier_actions': '',  # Will fill at end
                    'supplier_triggers': '',  # Will fill at end
                    'supplier_services': '',  # Will fill at end
                    'structure_type': 'Nested (Type 1)',
                    'l1_service': l1_service_name,
                    'l2_node_name': node_name,
                    'l2_classification': node_classification,
                    'l2_display_name': display_name,
                    'l2_node_type': node_type,
                    'l2_categories': categories,
                    'l2_has_json': 'Yes' if os.path.exists(json_path) else 'No',
                    'l3_resource': '',
                    'l4_operation': '',
                    'file_path': f"{supplier_folder}\\{l1_folder}",
                    'notes': ''
                })

# Fill in supplier stats and services for all rows
for row in all_rows:
    supplier = row['supplier']
    row['supplier_actions'] = supplier_stats[supplier]['actions']
    row['supplier_triggers'] = supplier_stats[supplier]['triggers']

    # Add services list
    if supplier in supplier_services and supplier_services[supplier]:
        services_list = sorted(list(supplier_services[supplier]))
        row['supplier_services'] = ', '.join(services_list)
    else:
        row['supplier_services'] = ''

print(f"\nProcessed {len(all_rows)} total rows")

# Calculate overall stats
total_actions = sum(stats['actions'] for stats in supplier_stats.values())
total_triggers = sum(stats['triggers'] for stats in supplier_stats.values())
total_nodes = sum(stats['total'] for stats in supplier_stats.values())

print(f"\nOVERALL STATISTICS:")
print(f"  Total Suppliers: {len(supplier_stats)}")
print(f"  Total Nodes: {total_nodes}")
print(f"  Total Actions: {total_actions}")
print(f"  Total Triggers: {total_triggers}")
print(f"  Suppliers with Services (Type 1): {len(supplier_services)}")

# Write to CSV
csv_path = r"C:\Users\total\n8n_master_knowledge_report.csv"
with open(csv_path, 'w', newline='', encoding='utf-8') as f:
    fieldnames = [
        'supplier',
        'supplier_actions',
        'supplier_triggers',
        'supplier_services',
        'structure_type',
        'l1_service',
        'l2_node_name',
        'l2_classification',
        'l2_display_name',
        'l2_node_type',
        'l2_categories',
        'l2_has_json',
        'l3_resource',
        'l4_operation',
        'file_path',
        'notes'
    ]

    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(all_rows)

# Print top suppliers by node count
print(f"\nTOP 10 SUPPLIERS BY NODE COUNT:")
top_suppliers = sorted(supplier_stats.items(), key=lambda x: x[1]['total'], reverse=True)[:10]
for supplier, stats in top_suppliers:
    services_str = ''
    if supplier in supplier_services and supplier_services[supplier]:
        services_str = f" [Services: {', '.join(sorted(list(supplier_services[supplier])))}]"
    print(f"  {supplier:30} Actions: {stats['actions']:3}, Triggers: {stats['triggers']:3}{services_str}")

print(f"\n[COMPLETE] Master knowledge report saved to:")
print(f"{csv_path}")
print("\nColumn structure:")
print("  - supplier (Column A)")
print("  - supplier_actions (Column B)")
print("  - supplier_triggers (Column C)")
print("  - supplier_services (Column D) - comma-separated list of L1 services")
print("\nYou can now open this in Excel and:")
print("  - Filter by supplier (Column A)")
print("  - See action/trigger counts per supplier")
print("  - See which suppliers have services (Type 1 nested structure)")
print("  - Sort/filter by structure type")
print("=" * 80)