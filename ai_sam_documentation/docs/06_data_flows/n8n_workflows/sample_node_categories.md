# Sample Node Categories

**Original file:** `sample_node_categories.py`
**Type:** PYTHON

---

```python
import os
import json
from pathlib import Path

# Path to n8n nodes
nodes_path = r"C:\Working With AI\Odoo Projects\custom-modules-v18\the_ai_automator\static\src\n8n\n8n_nodes"

# Collect samples
samples = []
count = 0
for root, dirs, files in os.walk(nodes_path):
    for file in files:
        if file.endswith('.node.json') and count < 30:
            file_path = os.path.join(root, file)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    categories = data.get('categories', [])
                    node_type = data.get('node', 'unknown')
                    samples.append({
                        'file': file,
                        'node': node_type,
                        'categories': categories
                    })
                    count += 1
            except Exception as e:
                pass

# Print results
print("\n=== N8N Node Category Sampling ===\n")
for sample in samples:
    print(f"File: {sample['file']}")
    print(f"Node: {sample['node']}")
    print(f"Categories: {', '.join(sample['categories'])}")
    print("---")

# Analyze patterns
all_categories = set()
for sample in samples:
    all_categories.update(sample['categories'])

print(f"\n=== Unique Categories Found ({len(all_categories)}) ===")
for cat in sorted(all_categories):
    print(f"  - {cat}")
```
