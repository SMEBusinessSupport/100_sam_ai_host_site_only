import re

manifest = open(r'C:\Working With AI\ai_sam\ai_sam\ai_sam\__manifest__.py').read()

# Extract assets section
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
xmls = re.findall(r"['\"]([^'\"]+\.xml)['\"]", assets_section)

print("=== XML files extracted from assets ===")
for xml in xmls:
    print(xml)
