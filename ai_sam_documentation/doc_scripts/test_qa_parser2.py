import re
from pathlib import Path

manifest = open(r'C:\Working With AI\ai_sam\ai_sam\ai_sam\__manifest__.py').read()
module_path = Path(r'C:\Working With AI\ai_sam\ai_sam\ai_sam')

# Extract assets section (same logic as QA tool)
assets_start = manifest.find("'assets'")
brace_start = manifest.find('{', assets_start)
brace_count = 1
pos = brace_start + 1

while pos < len(manifest) and brace_count > 0:
    if manifest[pos] == '{':
        brace_count += 1
    elif manifest[pos] == '}':
        brace_count -= 1
    pos += 1

assets_section = manifest[brace_start:pos]
manifest_files = re.findall(r"['\"]([^'\"]+\.xml)['\"]", assets_section)

print("=== Manifest files (from QA tool logic) ===")
for f in manifest_files:
    print(f"  '{f}'")

# Find XML files
all_xml_files = [f for f in Path(module_path).rglob('*.xml')]

print("\n=== Checking actual XML files ===")
for xml_file in all_xml_files[:10]:  # Just first 10
    try:
        rel_path = str(xml_file.relative_to(module_path)).replace('\\', '/')
        in_manifest = rel_path in manifest_files

        print(f"{in_manifest and '✅' or '❌'} {xml_file.name:40} -> '{rel_path}'")

        if not in_manifest and 'components' in rel_path:
            # Check if it matches with different prefix
            for mf in manifest_files:
                if xml_file.name in mf:
                    print(f"   MATCH: '{mf}'")
                    break
    except ValueError:
        continue
