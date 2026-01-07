import os

nodes_path = r"C:\Working With AI\Odoo Projects\custom-modules-v18\the_ai_automator\static\src\n8n\n8n_nodes"

# Find all .node.js files
js_files = []
json_files = []

for root, dirs, files in os.walk(nodes_path):
    for file in files:
        if file.endswith('.node.js'):
            base_name = file.replace('.node.js', '')
            js_files.append((base_name, root, file))
        elif file.endswith('.node.json'):
            base_name = file.replace('.node.json', '')
            json_files.append((base_name, root, file))

print(f"Found {len(js_files)} .node.js files")
print(f"Found {len(json_files)} .node.json files")
print(f"Difference: {len(js_files) - len(json_files)} nodes missing JSON metadata\n")

# Create lookup sets
json_set = {(name, path) for name, path, _ in json_files}
js_set = {(name, path) for name, path, _ in js_files}

# Find JS files without JSON
missing_json = []
for name, path, file in js_files:
    if (name, path) not in json_set:
        rel_path = os.path.relpath(path, nodes_path)
        missing_json.append((name, rel_path, file))

print(f"Nodes with .node.js BUT NO .node.json metadata:")
print("=" * 80)
for name, path, file in sorted(missing_json):
    print(f"{path:60} {file}")

# Also find JSON files without JS (edge case)
missing_js = []
for name, path, file in json_files:
    if (name, path) not in js_set:
        rel_path = os.path.relpath(path, nodes_path)
        missing_js.append((name, rel_path, file))

if missing_js:
    print(f"\n\nNodes with .node.json BUT NO .node.js code (unusual):")
    print("=" * 80)
    for name, path, file in sorted(missing_js):
        print(f"{path:60} {file}")