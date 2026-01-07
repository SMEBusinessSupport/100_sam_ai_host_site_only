# Fix Module Completely

**Original file:** `fix_module_completely.py`
**Type:** PYTHON

---

```python
#!/usr/bin/env python3
"""
Complete module fix script - uninstall and reinstall to clear cached models
"""

def create_fix_instructions():
    instructions = """
COMPLETE MODULE FIX INSTRUCTIONS
================================

The settings model is not loading properly because Odoo has cached the old model definition.
We need to completely uninstall and reinstall the module.

STEP 1: Uninstall Module
------------------------
1. Open http://localhost:8069
2. Login as admin
3. Go to Apps menu
4. Search for "Knowledge Visualizer V2"
5. Click the module to open its details
6. Click "Uninstall" button
7. Confirm uninstallation

STEP 2: Clear Cache (Manual)
----------------------------
1. Close browser completely
2. Wait 30 seconds for Odoo to clear internal caches

STEP 3: Reinstall Module  
------------------------
1. Open http://localhost:8069 in fresh browser window
2. Login as admin
3. Go to Apps menu
4. Remove any search filters (click "x" on search)
5. Search for "Knowledge Visualizer V2"
6. Click "Install" button
7. Wait for installation to complete

STEP 4: Test Canvas
-------------------
1. Hard refresh browser (Ctrl+F5)
2. Go to Knowledge Visualizer menu
3. Click "Workflow Templates"
4. Click "Visual Editor" button on any template
5. Look for BLUE canvas background

WHY THIS IS NEEDED:
------------------
- Odoo caches model definitions in memory
- Settings fields were added after initial installation
- Upgrade doesn't always refresh cached models properly
- Complete reinstall forces Odoo to reload all model definitions

ALTERNATIVE IF ABOVE FAILS:
---------------------------
1. Stop Odoo service completely
2. Restart Odoo service  
3. Then follow reinstall steps
"""
    
    with open("C:/Users/total/complete_fix_instructions.txt", "w") as f:
        f.write(instructions)
    
    print("Complete fix instructions written to: complete_fix_instructions.txt")
    print("\nCRITICAL: Module must be UNINSTALLED then REINSTALLED")
    print("Upgrade is not sufficient - the settings model cache needs to be cleared.")

if __name__ == "__main__":
    create_fix_instructions()
```
