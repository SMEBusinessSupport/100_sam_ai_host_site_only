import os
import json
import csv
from pathlib import Path
from collections import Counter

# Path to n8n nodes
nodes_path = r"C:\Working With AI\Odoo Projects\custom-modules-v18\the_ai_automator\static\src\n8n\n8n_nodes"

# Collect ALL .node.json files
all_nodes = []
category_counter = Counter()
supplier_counter = Counter()
file_extension_counter = Counter()
error_files = []

print("=" * 70)
print("COMPREHENSIVE N8N NODE ANALYSIS - ALL .node.json FILES")
print("=" * 70)
print(f"\nScanning directory: {nodes_path}")
print("Looking for ALL files ending with .node.json\n")

for root, dirs, files in os.walk(nodes_path):
    for file in files:
        if file.endswith('.node.json'):
            file_path = os.path.join(root, file)

            # Get full relative path from nodes_path
            rel_path = os.path.relpath(root, nodes_path)

            # Get supplier name (top-level folder)
            path_parts = rel_path.split(os.sep)
            supplier = path_parts[0] if path_parts[0] != '.' else 'Root'

            # Get subfolder depth
            folder_depth = len(path_parts) if path_parts[0] != '.' else 0
            subfolder = os.sep.join(path_parts[1:]) if len(path_parts) > 1 else ''

            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                    node_type = data.get('node', 'unknown')
                    categories = data.get('categories', [])
                    node_version = data.get('nodeVersion', '1.0')
                    display_name = data.get('displayName', '')
                    description = data.get('description', '')

                    # Extract the base filename pattern
                    base_name = file.replace('.node.json', '')

                    # Determine if trigger or action based on filename pattern
                    if base_name.endswith('Trigger'):
                        node_classification = 'Trigger'
                        service_name = base_name[:-7]  # Remove 'Trigger' suffix
                    else:
                        node_classification = 'Action'
                        service_name = base_name

                    all_nodes.append({
                        'supplier': supplier,
                        'subfolder': subfolder,
                        'folder_depth': folder_depth,
                        'service_name': service_name,
                        'file_name': file,
                        'display_name': display_name,
                        'node_id': node_type,
                        'node_classification': node_classification,
                        'categories': '|'.join(categories) if categories else '',
                        'category_count': len(categories),
                        'node_version': node_version,
                        'full_path': rel_path,
                        'absolute_path': file_path
                    })

                    # Count categories
                    for cat in categories:
                        category_counter[cat] += 1

                    # Count suppliers
                    supplier_counter[supplier] += 1

            except Exception as e:
                error_files.append({
                    'file': file,
                    'path': file_path,
                    'error': str(e)
                })
                print(f"[ERROR] {file}: {e}")

print(f"\n[OK] Found {len(all_nodes)} nodes")
print(f"[OK] Found {len(supplier_counter)} suppliers")
print(f"[OK] Found {len(category_counter)} unique categories")

# Write comprehensive CSV report
csv_path = r"C:\Users\total\n8n_nodes_complete_analysis.csv"
with open(csv_path, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=[
        'supplier', 'subfolder', 'folder_depth', 'service_name', 'file_name',
        'display_name', 'node_id', 'node_classification', 'categories',
        'category_count', 'node_version', 'full_path', 'absolute_path'
    ])
    writer.writeheader()
    writer.writerows(all_nodes)

print(f"\n[REPORT] CSV Report saved to: {csv_path}")

# Print category analysis
print("\n" + "="*60)
print("CATEGORY FREQUENCY ANALYSIS")
print("="*60)
for category, count in category_counter.most_common():
    print(f"{category:30} : {count:4} nodes")

# Print supplier analysis (top 20)
print("\n" + "="*60)
print("TOP 20 SUPPLIERS BY NODE COUNT")
print("="*60)
for supplier, count in supplier_counter.most_common(20):
    print(f"{supplier:30} : {count:4} nodes")

# Categorize by node type
triggers = [n for n in all_nodes if n['node_classification'] == 'Trigger']
actions = [n for n in all_nodes if n['node_classification'] == 'Action']

print("\n" + "="*60)
print("NODE TYPE DISTRIBUTION")
print("="*60)
print(f"Total Triggers: {len(triggers)}")
print(f"Total Actions:  {len(actions)}")

# Find nodes with multiple categories
multi_cat = [n for n in all_nodes if n['category_count'] > 1]
print(f"\nNodes with multiple categories: {len(multi_cat)}")

# Print error summary
if error_files:
    print("\n" + "="*60)
    print("ERRORS ENCOUNTERED")
    print("="*60)
    for error in error_files:
        print(f"{error['file']}: {error['error']}")
else:
    print("\n[OK] No errors encountered during analysis")

print("\n" + "="*70)
print("[COMPLETE] Comprehensive analysis complete!")
print(f"Report saved to: {csv_path}")
print("="*70)