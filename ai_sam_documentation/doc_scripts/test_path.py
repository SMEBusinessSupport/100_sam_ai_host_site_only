from pathlib import Path

module_path = Path(r'C:\Working With AI\ai_sam\ai_sam\ai_sam')
xml_file = Path(r'C:\Working With AI\ai_sam\ai_sam\ai_sam\static\src\components\sam_ai_chat_interface.xml')

rel_path = str(xml_file.relative_to(module_path)).replace('\\', '/')

print(f"Module path:  {module_path}")
print(f"XML file:     {xml_file}")
print(f"Relative:     {rel_path}")
print()
print("Manifest has: ai_sam/static/src/components/sam_ai_chat_interface.xml")
print(f"Match? {rel_path == 'ai_sam/static/src/components/sam_ai_chat_interface.xml'}")
print(f"Match? {rel_path == 'static/src/components/sam_ai_chat_interface.xml'}")
