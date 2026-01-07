# -*- coding: utf-8 -*-
"""
Diagnostic script for ai_brain.py
Run this from command line to check if the file loads correctly.

Usage:
    cd D:\SAMAI-18-SaaS\github-repos\05-samai-core
    python -c "import ai_sam_base.diagnose_brain"

Or directly:
    python ai_sam_base\diagnose_brain.py
"""

import sys
import os

print("=" * 60)
print("AI Brain Diagnostic Script")
print("=" * 60)

# Check Python version
print(f"\n1. Python Version: {sys.version}")

# Check encoding
print(f"\n2. Default Encoding: {sys.getdefaultencoding()}")
print(f"   Filesystem Encoding: {sys.getfilesystemencoding()}")
print(f"   stdout Encoding: {sys.stdout.encoding}")

# Try to read the file
brain_path = os.path.join(os.path.dirname(__file__), 'models', 'ai_brain.py')
print(f"\n3. Checking file: {brain_path}")

if os.path.exists(brain_path):
    print("   File exists: YES")

    # Try to read with UTF-8
    try:
        with open(brain_path, 'r', encoding='utf-8') as f:
            content = f.read()
        print(f"   File size: {len(content)} chars")
        print("   UTF-8 read: SUCCESS")

        # Check for specific markers
        markers = [
            '[STREAM 12.5]',
            'file_keywords',
            '_get_sam_tools',
            'Increased recursion limit',
        ]

        print("\n4. Checking for code markers:")
        for marker in markers:
            found = marker in content
            status = "FOUND" if found else "MISSING"
            print(f"   '{marker}': {status}")

        # Find line numbers
        print("\n5. Key line locations:")
        lines = content.split('\n')
        for i, line in enumerate(lines, 1):
            if 'STREAM 12.5' in line:
                print(f"   Line {i}: {line.strip()[:80]}")
            if 'file_keywords' in line:
                print(f"   Line {i}: {line.strip()[:80]}")

    except UnicodeDecodeError as e:
        print(f"   UTF-8 read: FAILED - {e}")

        # Try to find the problematic character
        with open(brain_path, 'rb') as f:
            raw = f.read()

        # Find non-ASCII characters
        print("\n   Scanning for non-ASCII characters...")
        line_num = 1
        col = 0
        for i, byte in enumerate(raw):
            if byte == ord('\n'):
                line_num += 1
                col = 0
            else:
                col += 1

            if byte > 127:
                # Get context
                start = max(0, i - 20)
                end = min(len(raw), i + 20)
                context = raw[start:end]
                print(f"   Line {line_num}, Col {col}: byte={byte} (0x{byte:02x})")
                print(f"   Context: {context}")

else:
    print("   File exists: NO")

print("\n6. Try importing the module...")
try:
    # Add parent to path if needed
    parent = os.path.dirname(os.path.dirname(__file__))
    if parent not in sys.path:
        sys.path.insert(0, parent)

    # Try syntax check only (compile)
    import py_compile
    py_compile.compile(brain_path, doraise=True)
    print("   Syntax check: PASSED")

except py_compile.PyCompileError as e:
    print(f"   Syntax check: FAILED")
    print(f"   Error: {e}")
except Exception as e:
    print(f"   Import: FAILED - {type(e).__name__}: {e}")

print("\n" + "=" * 60)
print("Diagnostic complete")
print("=" * 60)

if __name__ == '__main__':
    pass
