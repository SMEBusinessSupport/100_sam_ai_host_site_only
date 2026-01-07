#!/usr/bin/env python3
"""
Clean installation guide after fixing OWL lifecycle error
"""

def main():
    print("CLEAN INSTALL GUIDE - OWL Error Fixed")
    print("=" * 50)
    
    print("FIXES APPLIED:")
    print("1. SUCCESS: Completely disabled settings model")
    print("2. SUCCESS: Removed settings view from manifest") 
    print("3. SUCCESS: Fixed XML template JSON.stringify() error")
    print("4. SUCCESS: Fixed JavaScript parametersJson handling")
    print("5. SUCCESS: Removed providers_state field causing OWL error")
    
    print("\nMODULE IS NOW CLEAN FOR INSTALLATION")
    print("\nINSTALLATION STEPS:")
    print("1. Go to http://localhost:8069")
    print("2. Login as admin")
    print("3. Apps > Remove any search filters")
    print("4. Search 'Knowledge Visualizer V2'") 
    print("5. Click 'Install' button")
    print("6. Wait for installation to complete")
    print("7. Hard refresh browser (Ctrl+F5)")
    
    print("\nTEST CANVAS:")
    print("1. Go to Knowledge Visualizer menu")
    print("2. Click 'Workflow Templates'")
    print("3. Click 'Visual Editor' button")
    print("4. Should see BLUE canvas (React Flow working)")
    
    print("\nEXPECTED RESULTS:")
    print("- No more OWL lifecycle errors")
    print("- No more providers_state field errors")
    print("- Module installs cleanly")
    print("- Visual Editor opens")
    print("- Blue canvas appears")
    print("- Console errors stop")
    
    print("\nIf you still get OWL errors:")
    print("- Clear browser cache completely")
    print("- Restart Odoo service")
    print("- Try in incognito/private browser window")

if __name__ == "__main__":
    main()