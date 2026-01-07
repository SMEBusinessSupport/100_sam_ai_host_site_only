# Module Tools

**Original file:** `module_tools.py`
**Type:** PYTHON

---

```python
#!/usr/bin/env python3
"""
Module Development Tools
========================

Comprehensive toolkit for Odoo module development.
Consolidates: cleanup_module_safe, create_module_story, validate_module_split

Features:
- Module documentation generator
- Dependency validator
- Safe archiving of old code
- Statistics and reporting

Usage:
    # Generate module documentation
    python module_tools.py docs --module ai_base

    # Validate module dependencies
    python module_tools.py validate --base ai_base --trunk ai_trunk

    # Archive old/commented code
    python module_tools.py archive --module the_ai_automator --dry-run

Author: Better Business Builders
Date: October 2025
"""

import os
import sys
import re
import json
import shutil
import argparse
from pathlib import Path
from datetime import datetime
from collections import defaultdict


class ModuleTools:
    """Comprehensive module development utilities"""

    def __init__(self, module_path):
        self.module_path = Path(module_path)
        self.module_name = self.module_path.name

    # ========================================================================
    # DOCUMENTATION GENERATOR
    # ========================================================================

    def generate_documentation(self):
        """Generate comprehensive module documentation"""
        print("=" * 80)
        print(f"MODULE DOCUMENTATION: {self.module_name}")
        print("=" * 80)

        doc = {
            'module': self.module_name,
            'path': str(self.module_path),
            'generated': datetime.now().isoformat(),
            'statistics': self._get_statistics(),
            'structure': self._get_structure(),
            'models': self._get_models(),
            'views': self._get_views(),
            'dependencies': self._get_dependencies(),
        }

        # Print summary
        self._print_documentation(doc)

        # Save to file
        output_file = self.module_path.parent / f"{self.module_name}_DOCS.json"
        with open(output_file, 'w') as f:
            json.dump(doc, f, indent=2)

        print(f"\n[*] Documentation saved to: {output_file}")
        return doc

    def _get_statistics(self):
        """Get module statistics"""
        stats = {
            'python_files': 0,
            'python_lines': 0,
            'xml_files': 0,
            'xml_lines': 0,
            'js_files': 0,
            'js_lines': 0,
            'css_files': 0,
            'css_lines': 0,
        }

        for ext, key_files, key_lines in [
            ('.py', 'python_files', 'python_lines'),
            ('.xml', 'xml_files', 'xml_lines'),
            ('.js', 'js_files', 'js_lines'),
            ('.css', 'css_files', 'css_lines'),
        ]:
            files = list(self.module_path.rglob(f'*{ext}'))
            stats[key_files] = len(files)

            for file in files:
                try:
                    with open(file, 'r', encoding='utf-8') as f:
                        stats[key_lines] += len(f.readlines())
                except:
                    pass

        return stats

    def _get_structure(self):
        """Get module directory structure"""
        structure = {}

        for item in self.module_path.iterdir():
            if item.is_dir() and not item.name.startswith('.'):
                structure[item.name] = len(list(item.rglob('*')))

        return structure

    def _get_models(self):
        """Extract model definitions"""
        models = []

        models_dir = self.module_path / 'models'
        if not models_dir.exists():
            return models

        for py_file in models_dir.glob('*.py'):
            if py_file.name == '__init__.py':
                continue

            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                    # Find model definitions
                    matches = re.finditer(r"_name\s*=\s*['\"]([^'\"]+)['\"]", content)
                    for match in matches:
                        model_name = match.group(1)

                        # Get description
                        desc_match = re.search(r"_description\s*=\s*['\"]([^'\"]+)['\"]", content)
                        description = desc_match.group(1) if desc_match else "No description"

                        models.append({
                            'name': model_name,
                            'description': description,
                            'file': py_file.name
                        })
            except:
                pass

        return models

    def _get_views(self):
        """Extract view definitions"""
        views = []

        views_dir = self.module_path / 'views'
        if not views_dir.exists():
            return views

        for xml_file in views_dir.glob('*.xml'):
            try:
                with open(xml_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                    # Count records
                    records = len(re.findall(r'<record', content))
                    menus = len(re.findall(r'<menuitem', content))

                    views.append({
                        'file': xml_file.name,
                        'records': records,
                        'menus': menus
                    })
            except:
                pass

        return views

    def _get_dependencies(self):
        """Get module dependencies from manifest"""
        manifest_path = self.module_path / '__manifest__.py'
        if not manifest_path.exists():
            return []

        try:
            with open(manifest_path, 'r', encoding='utf-8') as f:
                content = f.read()

                # Extract depends list
                match = re.search(r"'depends':\s*\[(.*?)\]", content, re.DOTALL)
                if match:
                    depends_str = match.group(1)
                    depends = re.findall(r"['\"]([^'\"]+)['\"]", depends_str)
                    return depends
        except:
            pass

        return []

    def _print_documentation(self, doc):
        """Print documentation to console"""
        print(f"\n[*] MODULE: {doc['module']}")
        print(f"    Path: {doc['path']}")

        print(f"\n[*] STATISTICS:")
        stats = doc['statistics']
        print(f"    Python: {stats['python_files']} files, {stats['python_lines']} lines")
        print(f"    XML: {stats['xml_files']} files, {stats['xml_lines']} lines")
        print(f"    JavaScript: {stats['js_files']} files, {stats['js_lines']} lines")
        print(f"    CSS: {stats['css_files']} files, {stats['css_lines']} lines")

        print(f"\n[*] MODELS: {len(doc['models'])}")
        for model in doc['models'][:5]:  # Show first 5
            print(f"    - {model['name']}: {model['description']}")
        if len(doc['models']) > 5:
            print(f"    ... and {len(doc['models']) - 5} more")

        print(f"\n[*] DEPENDENCIES: {len(doc['dependencies'])}")
        for dep in doc['dependencies']:
            print(f"    - {dep}")

    # ========================================================================
    # DEPENDENCY VALIDATOR
    # ========================================================================

    def validate_dependencies(self, other_module_path):
        """Validate dependencies between two modules"""
        other_path = Path(other_module_path)

        print("=" * 80)
        print(f"VALIDATING DEPENDENCIES")
        print(f"  Base: {self.module_name}")
        print(f"  Other: {other_path.name}")
        print("=" * 80)

        issues = []
        warnings = []

        # Check if other depends on this
        other_manifest = other_path / '__manifest__.py'
        if other_manifest.exists():
            with open(other_manifest, 'r') as f:
                content = f.read()
                if self.module_name not in content:
                    issues.append(f"{other_path.name} should depend on {self.module_name}")

        # Check for cross-references in Python
        print("\n[*] Checking Python cross-references...")
        for py_file in other_path.rglob('*.py'):
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                    # Check for model references
                    models = self._get_models()
                    for model in models:
                        if model['name'] in content:
                            warnings.append(f"{py_file.name} references {model['name']}")
            except:
                pass

        # Report
        print(f"\n[*] VALIDATION RESULTS:")
        if issues:
            print(f"\n[!] ISSUES ({len(issues)}):")
            for issue in issues:
                print(f"    - {issue}")

        if warnings:
            print(f"\n[?] WARNINGS ({len(warnings)}):")
            for warning in warnings[:10]:  # Show first 10
                print(f"    - {warning}")
            if len(warnings) > 10:
                print(f"    ... and {len(warnings) - 10} more")

        if not issues and not warnings:
            print("    [OK] No issues found")

        return len(issues) == 0

    # ========================================================================
    # ARCHIVE OLD CODE
    # ========================================================================

    def archive_old_code(self, dry_run=False):
        """Archive commented-out code and uncertain files"""
        print("=" * 80)
        print(f"ARCHIVING OLD CODE: {self.module_name}")
        print(f"Mode: {'DRY RUN' if dry_run else 'LIVE'}")
        print("=" * 80)

        # Create archive directory
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        archive_dir = self.module_path.parent / f"{self.module_name}_ARCHIVE_{timestamp}"

        archived_items = []

        # Find commented-out code
        print("\n[*] Scanning for commented code...")
        for py_file in self.module_path.rglob('*.py'):
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()

                commented_blocks = []
                block_start = None

                for i, line in enumerate(lines):
                    if line.strip().startswith('#') and ('import' in line or 'def ' in line or 'class ' in line):
                        if block_start is None:
                            block_start = i
                    elif block_start is not None:
                        if not line.strip().startswith('#'):
                            commented_blocks.append((block_start, i))
                            block_start = None

                if commented_blocks:
                    archived_items.append(f"{py_file.name}: {len(commented_blocks)} commented blocks")

            except:
                pass

        # Find uncertain/old directories
        print("\n[*] Checking for old directories...")
        old_dirs = ['uncertain_files', 'backup', 'archive', 'old', 'deprecated']
        for dir_name in old_dirs:
            dir_path = self.module_path / dir_name
            if dir_path.exists():
                archived_items.append(f"Directory: {dir_name}/")

                if not dry_run:
                    # Move to archive
                    dest = archive_dir / dir_name
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    shutil.move(str(dir_path), str(dest))

        # Report
        print(f"\n[*] ARCHIVE SUMMARY:")
        print(f"    Items found: {len(archived_items)}")
        for item in archived_items[:10]:
            print(f"    - {item}")
        if len(archived_items) > 10:
            print(f"    ... and {len(archived_items) - 10} more")

        if not dry_run and archived_items:
            print(f"\n[*] Archived to: {archive_dir}")
        elif dry_run:
            print(f"\n[*] DRY RUN - No changes made")

        return archive_dir if not dry_run else None


def main():
    parser = argparse.ArgumentParser(description="Module Development Tools")
    parser.add_argument("command", choices=["docs", "validate", "archive"], help="Command to run")
    parser.add_argument("--module", required=True, help="Module path")
    parser.add_argument("--other", help="Other module for validation")
    parser.add_argument("--dry-run", action="store_true", help="Dry run (no changes)")

    args = parser.parse_args()

    tools = ModuleTools(args.module)

    if args.command == "docs":
        tools.generate_documentation()

    elif args.command == "validate":
        if not args.other:
            print("[!] --other required for validation")
            sys.exit(1)
        tools.validate_dependencies(args.other)

    elif args.command == "archive":
        tools.archive_old_code(dry_run=args.dry_run)


if __name__ == "__main__":
    main()

```
