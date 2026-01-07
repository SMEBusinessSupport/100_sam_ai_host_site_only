#!/usr/bin/env python3
import subprocess
import time
import sys
import os

def run_command(cmd, description=""):
    """Run a command and return success status"""
    try:
        print(f"Running: {description}...")
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"SUCCESS: {description}")
            return True
        else:
            print(f"FAILED: {description}")
            print(f"   Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"ERROR: {description} - {e}")
        return False

def main():
    print("Restarting Odoo to reload JavaScript changes...")
    print("=" * 50)
    
    # Try different methods to restart Odoo
    restart_commands = [
        ('sc stop odoo-server-18.0 && sc start odoo-server-18.0', 'Service control restart'),
        ('net stop odoo-server-18.0 && net start odoo-server-18.0', 'Net command restart'),
        ('powershell -Command "Restart-Service -Name odoo-server-18.0 -Force"', 'PowerShell restart'),
    ]
    
    # Try each restart method
    for cmd, desc in restart_commands:
        if run_command(cmd, desc):
            break
        time.sleep(2)
    
    print("\nWaiting for Odoo to start up...")
    time.sleep(10)
    
    print("Odoo restart complete!")
    print("\nNext steps:")
    print("1. Hard refresh browser (Ctrl+F5)")
    print("2. Click Visual Editor button")
    print("3. Check if blue canvas appears")

if __name__ == "__main__":
    main()