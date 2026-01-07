# Dependency Options

**Original file:** `dependency_options.py`
**Type:** PYTHON

---

```python
#!/usr/bin/env python3
"""
Knowledge Visualizer V2 - Dependency Options
"""

def main():
    print("KNOWLEDGE VISUALIZER V2 - DEPENDENCY OPTIONS")
    print("=" * 60)
    
    print("CURRENT MINIMAL SETUP (Recommended):")
    print("SUCCESS: base  - Core Odoo framework (REQUIRED)")
    print("SUCCESS: web   - Web interface for client actions (REQUIRED)")  
    print("SUCCESS: mail  - Basic messaging system (optional)")
    print("  Total: 3 dependencies")
    
    print("\nULTRA-MINIMAL SETUP (If removing mail module):")
    print("SUCCESS: base  - Core Odoo framework (REQUIRED)")
    print("SUCCESS: web   - Web interface for client actions (REQUIRED)")
    print("  Total: 2 dependencies")
    
    print("\nREMOVED DEPENDENCIES (15 modules eliminated):")
    print("REMOVED: web_tour       - Guided tours")
    print("REMOVED: portal         - Portal users")  
    print("REMOVED: base_automation - Automated actions")
    print("REMOVED: link_tracker   - Link tracking")
    print("REMOVED: mass_mailing   - Email marketing")
    print("REMOVED: crm           - Customer relationship") 
    print("REMOVED: project       - Project management")
    print("REMOVED: sale          - Sales management")
    print("REMOVED: purchase      - Purchase management") 
    print("REMOVED: stock         - Inventory management")
    print("REMOVED: account       - Accounting")
    print("REMOVED: hr            - Human resources")
    print("REMOVED: calendar      - Calendar integration")
    print("REMOVED: contacts      - Contact management")
    print("REMOVED: website       - Website builder")
    
    print("\nIF YOU'RE UNINSTALLING MAIL MODULE:")
    print("Run this command to make it ultra-minimal:")
    print("python make_ultra_minimal.py")
    
    print("\nCURRENT STATUS:")
    print("SUCCESS: Dependencies reduced from 18 to 3 modules")
    print("SUCCESS: Should eliminate most module conflicts")
    print("SUCCESS: Canvas functionality preserved")
    print("SUCCESS: Ready for clean installation")

if __name__ == "__main__":
    main()
```
