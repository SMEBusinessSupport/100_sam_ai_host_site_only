#!/usr/bin/env python3
"""
Make Knowledge Visualizer V2 ultra-minimal (only base + web)
"""
import os

def make_ultra_minimal():
    manifest_path = r"C:\Working With AI\Odoo Projects\custom-modules-v18\knowledge_visualizer_v2\__manifest__.py"
    
    print("Making Knowledge Visualizer V2 ultra-minimal...")
    
    # Read current manifest
    with open(manifest_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace dependencies section
    old_deps = """    'depends': [
        # Essential core modules only
        'base',        # Core Odoo framework (required)
        'web',         # Web interface for client actions (required)
        'mail',        # Basic messaging system (optional - can be removed if no notifications needed)
    ],"""
    
    new_deps = """    'depends': [
        # Ultra-minimal setup - only core requirements
        'base',        # Core Odoo framework (required)
        'web',         # Web interface for client actions (required)
    ],"""
    
    if old_deps in content:
        content = content.replace(old_deps, new_deps)
        
        # Write updated manifest
        with open(manifest_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
        print("✅ SUCCESS: Knowledge Visualizer V2 is now ultra-minimal")
        print("✅ Dependencies: base + web only (2 modules)")
        print("✅ Ready for installation with minimal conflicts")
    else:
        print("❌ Could not find dependencies section to update")

if __name__ == "__main__":
    make_ultra_minimal()