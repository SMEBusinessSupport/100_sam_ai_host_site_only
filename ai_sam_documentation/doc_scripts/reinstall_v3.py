#!/usr/bin/env python3
"""
Clean Reinstall of V3 Modules
===============================

Uninstalls and reinstalls ai_trunk and ai_poppy to ensure clean XML/data loading.
Fixes the "tree" vs "list" view mode issue and ensures fresh database state.

Usage:
    python reinstall_v3.py
"""

import subprocess
import sys
import os

# Odoo configuration
ODOO_BIN = r"C:\Program Files\Odoo 18\server\odoo-bin"
ODOO_CONFIG = r"C:\Program Files\Odoo 18\server\odoo.conf"

def run_odoo_command(modules, action="install"):
    """Run Odoo command with specified modules"""
    if action == "uninstall":
        flag = "-u"  # Odoo uses -u for both install AND uninstall (it's context-dependent)
    else:
        flag = "-i"  # Install

    cmd = [
        sys.executable,
        ODOO_BIN,
        "-c", ODOO_CONFIG,
        flag, modules,
        "--stop-after-init"
    ]

    print(f"\n{'='*80}")
    print(f"  {action.upper()}: {modules}")
    print(f"{'='*80}\n")

    result = subprocess.run(cmd, capture_output=False)
    return result.returncode == 0

def main():
    print("""
================================================================================
  V3 Module Clean Reinstall
================================================================================

This will:
1. Uninstall ai_poppy (if installed)
2. Uninstall ai_trunk (if installed)
3. Reinstall ai_trunk (fresh XML with view_mode='list')
4. Reinstall ai_poppy (with ai_base dependency)

ai_base will remain installed (data layer should not be touched).

Press CTRL+C to cancel, or ENTER to continue...
""")

    try:
        input()
    except KeyboardInterrupt:
        print("\n\nCancelled.")
        return

    # Step 1: Uninstall ai_poppy (dependent module first)
    print("\n[1/4] Uninstalling ai_poppy...")
    # Note: We can't directly uninstall via command line easily
    # The proper way is through Odoo's module manager

    print("""
================================================================================
  MANUAL UNINSTALL REQUIRED
================================================================================

Please perform these steps in Odoo:

1. Open your browser to http://localhost:8069
2. Go to Apps menu
3. Remove any filters (click X on filter chips)
4. Search for "ai_poppy"
   - If installed: Click "Uninstall" button
5. Search for "ai_trunk"
   - Click "Uninstall" button
6. Wait for uninstall to complete

Then press ENTER to continue with reinstall...
""")

    try:
        input()
    except KeyboardInterrupt:
        print("\n\nCancelled.")
        return

    # Step 2: Install ai_trunk (fresh)
    print("\n[3/4] Installing ai_trunk (fresh)...")
    if not run_odoo_command("ai_trunk", "install"):
        print("❌ Failed to install ai_trunk")
        return 1

    print("✅ ai_trunk installed successfully")

    # Step 3: Install ai_poppy (fresh)
    print("\n[4/4] Installing ai_poppy (fresh)...")
    if not run_odoo_command("ai_poppy", "install"):
        print("❌ Failed to install ai_poppy")
        return 1

    print("✅ ai_poppy installed successfully")

    print("""
================================================================================
  ✅ REINSTALL COMPLETE
================================================================================

V3 Modules reinstalled with:
- ai_trunk: Clean XML (view_mode='list', <list> views)
- ai_poppy: Proper dependencies (ai_base + ai_trunk)

Next steps:
1. Refresh browser (Ctrl+Shift+R)
2. Click "SAM AI" menu - should work without errors
3. Test platform functionality

================================================================================
""")

if __name__ == "__main__":
    sys.exit(main() or 0)
