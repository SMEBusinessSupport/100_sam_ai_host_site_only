import os
import json
import csv

# Path to n8n nodes
nodes_path = r"C:\Working With AI\Odoo Projects\custom-modules-v18\the_ai_automator\static\src\n8n\n8n_nodes"

print("=" * 80)
print("N8N NODE CATEGORIZATION ANALYSIS")
print("=" * 80)

all_nodes = []

# Walk through all suppliers
for supplier_folder in os.listdir(nodes_path):
    supplier_path = os.path.join(nodes_path, supplier_folder)

    if not os.path.isdir(supplier_path):
        continue

    supplier_name = supplier_folder

    # Check for direct .node.json files (Type 2 - flat)
    for file in os.listdir(supplier_path):
        if file.endswith('.node.json'):
            json_path = os.path.join(supplier_path, file)

            try:
                with open(json_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                    # Extract categorization data
                    node_id = data.get('node', '')
                    categories = data.get('categories', [])
                    subcategories = data.get('subcategories', {})
                    alias = data.get('alias', [])

                    # Determine trigger/action from filename
                    base_name = file.replace('.node.json', '')
                    filename_type = 'Trigger' if 'Trigger' in base_name else 'Action'

                    # Format subcategories for readability
                    subcat_str = ''
                    if subcategories:
                        parts = []
                        for parent_cat, sub_list in subcategories.items():
                            parts.append(f"{parent_cat}: {', '.join(sub_list)}")
                        subcat_str = ' | '.join(parts)

                    all_nodes.append({
                        'supplier': supplier_name,
                        'file_name': file,
                        'node_id': node_id,
                        'filename_classification': filename_type,
                        'categories': ', '.join(categories) if categories else '',
                        'subcategories': subcat_str,
                        'alias': ', '.join(alias) if alias else '',
                        'l1_service': '',
                        'file_path': supplier_folder
                    })
            except Exception as e:
                print(f"Error reading {file}: {e}")

    # Check for nested structure (Type 1)
    for l1_folder in os.listdir(supplier_path):
        l1_path = os.path.join(supplier_path, l1_folder)

        if not os.path.isdir(l1_path) or l1_folder.startswith('__') or l1_folder in ['test', 'v1', 'v2', 'v3']:
            continue

        # Check for .node.json files in L1 folder
        for file in os.listdir(l1_path):
            if file.endswith('.node.json'):
                json_path = os.path.join(l1_path, file)

                try:
                    with open(json_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)

                        # Extract categorization data
                        node_id = data.get('node', '')
                        categories = data.get('categories', [])
                        subcategories = data.get('subcategories', {})
                        alias = data.get('alias', [])

                        # Determine trigger/action from filename
                        base_name = file.replace('.node.json', '')
                        filename_type = 'Trigger' if 'Trigger' in base_name else 'Action'

                        # Format subcategories for readability
                        subcat_str = ''
                        if subcategories:
                            parts = []
                            for parent_cat, sub_list in subcategories.items():
                                parts.append(f"{parent_cat}: {', '.join(sub_list)}")
                            subcat_str = ' | '.join(parts)

                        all_nodes.append({
                            'supplier': supplier_name,
                            'file_name': file,
                            'node_id': node_id,
                            'filename_classification': filename_type,
                            'categories': ', '.join(categories) if categories else '',
                            'subcategories': subcat_str,
                            'alias': ', '.join(alias) if alias else '',
                            'l1_service': l1_folder,
                            'file_path': f"{supplier_folder}\\{l1_folder}"
                        })
                except Exception as e:
                    print(f"Error reading {file}: {e}")

print(f"\nFound {len(all_nodes)} nodes with .node.json files")

# Count nodes with subcategories
nodes_with_subcats = len([n for n in all_nodes if n['subcategories']])
nodes_with_alias = len([n for n in all_nodes if n['alias']])

print(f"Nodes with subcategories: {nodes_with_subcats}")
print(f"Nodes with aliases: {nodes_with_alias}")

# Write to CSV
csv_path = r"C:\Users\total\n8n_categorization_analysis.csv"
with open(csv_path, 'w', newline='', encoding='utf-8') as f:
    fieldnames = [
        'supplier',
        'l1_service',
        'file_name',
        'filename_classification',
        'node_id',
        'categories',
        'subcategories',
        'alias',
        'file_path'
    ]

    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(all_nodes)

print(f"\n[COMPLETE] Categorization analysis saved to:")
print(f"{csv_path}")
print("\nThis CSV shows:")
print("  - supplier: Supplier name")
print("  - l1_service: L1 service (if nested structure)")
print("  - file_name: The .node.json filename")
print("  - filename_classification: Trigger/Action based on filename pattern")
print("  - node_id: N8N node identifier")
print("  - categories: Main categories (e.g., 'Development, Core Nodes')")
print("  - subcategories: UI subcategory placement (e.g., 'Core Nodes: Helpers, Flow')")
print("  - alias: Search terms/aliases")
print("\nKey insight:")
print("  - filename_classification comes from the FILENAME pattern (*Trigger.node.json)")
print("  - NOT from data inside the JSON file!")
print("  - This is why we detect it by checking if 'Trigger' is in the filename")
print("=" * 80)