# Odoo Log Analyzer

**Original file:** `odoo_log_analyzer.py`
**Type:** PYTHON

---

```python
﻿#!/usr/bin/env python3
"""
Odoo Log Analyzer
=================

Analyzes Odoo log files for common errors and provides solutions.

Usage:
    # Analyze recent errors
    python odoo_log_analyzer.py --log "path/to/odoo.log"

    # Analyze with specific error filter
    python odoo_log_analyzer.py --log "path/to/odoo.log" --filter "ValueError"

    # Get last N lines
    python odoo_log_analyzer.py --log "path/to/odoo.log" --tail 200

Author: Better Business Builders
Date: October 2025
"""

import argparse
import re
import sys
from pathlib import Path
from collections import defaultdict


class OdooLogAnalyzer:
    """Analyzes Odoo log files and provides solutions"""

    def __init__(self, log_file):
        self.log_file = Path(log_file)
        self.errors = []
        self.solutions = {}

        # Known error patterns and solutions
        self.error_patterns = {
            'invalid_version': {
                'pattern': r"Invalid version '([^']+)'.*format.*18\.0",
                'title': 'Invalid Module Version Format',
                'solution': '''
FIX: Update module __manifest__.py version to start with 18.0

Current: {error_value}
Required: 18.0.x.y or 18.0.x.y.z

Example fixes:
- Change '3.0.0.0' -> '18.0.3.0.0'
- Change '1.0.0' -> '18.0.1.0.0'
- Change '2.5' -> '18.0.2.5.0'

Steps:
1. Open module/__manifest__.py
2. Find 'version': '{error_value}'
3. Change to 'version': '18.0.x.y.z'
4. Restart Odoo server
''',
                'severity': 'CRITICAL'
            },

            'missing_dependency': {
                'pattern': r"No module named '([^']+)'",
                'title': 'Missing Python Dependency',
                'solution': '''
FIX: Install missing Python package

Missing package: {error_value}

Install command:
pip install {error_value}

Or if in Odoo venv:
/path/to/odoo/venv/bin/pip install {error_value}
''',
                'severity': 'CRITICAL'
            },

            'module_not_found': {
                'pattern': r"Module ([^ ]+): invalid manifest",
                'title': 'Module Manifest Error',
                'solution': '''
FIX: Check module manifest file

Module: {error_value}

Common issues:
1. Invalid version format (must start with 18.0)
2. Missing required fields (name, version, depends)
3. Syntax error in __manifest__.py
4. Invalid dependency name

Steps:
1. Check {error_value}/__manifest__.py
2. Validate version format
3. Check all fields are properly quoted
4. Ensure valid Python dictionary syntax
''',
                'severity': 'CRITICAL'
            },

            'import_error': {
                'pattern': r"ImportError: cannot import name '([^']+)'",
                'title': 'Python Import Error',
                'solution': '''
FIX: Module import issue

Failed import: {error_value}

Common causes:
1. Typo in import statement
2. Module file doesn't exist
3. Circular import
4. Missing __init__.py

Steps:
1. Check spelling of '{error_value}'
2. Verify file exists in models/ folder
3. Check models/__init__.py includes the import
4. Look for circular dependencies
''',
                'severity': 'HIGH'
            },

            'database_error': {
                'pattern': r"psycopg2\..*Error: (.+)",
                'title': 'Database Error',
                'solution': '''
FIX: PostgreSQL database issue

Error: {error_value}

Common solutions:
1. Check PostgreSQL is running
2. Verify database credentials in odoo.conf
3. Check database user permissions
4. Ensure database exists

Check commands:
- Windows: sc query postgresql-x64-15
- Linux: systemctl status postgresql
''',
                'severity': 'CRITICAL'
            },

            'access_denied': {
                'pattern': r"AccessDenied|AccessError: (.+)",
                'title': 'Access Rights Error',
                'solution': '''
FIX: User permission issue

Error: {error_value}

Solutions:
1. Check security/ir.model.access.csv
2. Verify user groups assignment
3. Add proper access rules for models
4. Check record rules

Example access rule:
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_model_user,model.user,model_model,base.group_user,1,1,1,1
''',
                'severity': 'HIGH'
            },

            'field_error': {
                'pattern': r"Field '([^']+)' does not exist",
                'title': 'Missing Field Error',
                'solution': '''
FIX: Field not found in model

Field: {error_value}

Common causes:
1. Typo in field name
2. Field not defined in model
3. Module not installed/updated
4. Database not upgraded

Steps:
1. Check model definition for field '{error_value}'
2. Verify field spelling in views/code
3. Update module if field was added
4. Upgrade database: odoo-bin -u module_name
''',
                'severity': 'HIGH'
            }
        }

    def analyze(self, tail_lines=None, error_filter=None):
        """Analyze log file"""
        print("=" * 80)
        print("ODOO LOG ANALYZER")
        print("=" * 80)
        print(f"\nAnalyzing: {self.log_file}")

        if not self.log_file.exists():
            print(f"[!] Log file not found: {self.log_file}")
            return False

        # Read log file
        try:
            with open(self.log_file, 'r', encoding='utf-8', errors='ignore') as f:
                if tail_lines:
                    # Read last N lines
                    lines = f.readlines()[-tail_lines:]
                else:
                    lines = f.readlines()
        except Exception as e:
            print(f"[!] Error reading log file: {e}")
            return False

        print(f"Lines analyzed: {len(lines)}")

        # Extract errors
        self._extract_errors(lines, error_filter)

        # Print report
        self._print_report()

        return len(self.errors) > 0

    def _extract_errors(self, lines, error_filter=None):
        """Extract errors from log lines"""
        print("\n[*] Extracting errors...")

        current_error = None
        error_lines = []

        for line in lines:
            # Check if this is an error line
            if 'ERROR' in line or 'Traceback' in line or 'Exception' in line:
                if current_error:
                    # Save previous error
                    self.errors.append({
                        'type': current_error,
                        'lines': error_lines.copy()
                    })

                current_error = 'ERROR'
                error_lines = [line]

            elif current_error and (line.startswith(' ') or line.startswith('File') or 'Error:' in line):
                # Continuation of current error
                error_lines.append(line)

            elif current_error:
                # End of error block
                if error_lines:
                    self.errors.append({
                        'type': current_error,
                        'lines': error_lines.copy()
                    })
                current_error = None
                error_lines = []

        # Add last error if exists
        if current_error and error_lines:
            self.errors.append({
                'type': current_error,
                'lines': error_lines.copy()
            })

        # Filter errors if requested
        if error_filter:
            self.errors = [e for e in self.errors
                          if error_filter.lower() in ''.join(e['lines']).lower()]

        # Analyze each error
        for error in self.errors:
            error['analysis'] = self._analyze_error(error)

    def _analyze_error(self, error):
        """Analyze single error and find solution"""
        error_text = ''.join(error['lines'])

        # Check against known patterns
        for error_type, pattern_info in self.error_patterns.items():
            match = re.search(pattern_info['pattern'], error_text, re.IGNORECASE)
            if match:
                error_value = match.group(1) if match.groups() else 'Unknown'
                return {
                    'type': error_type,
                    'title': pattern_info['title'],
                    'solution': pattern_info['solution'].format(error_value=error_value),
                    'severity': pattern_info['severity'],
                    'value': error_value
                }

        # Unknown error
        return {
            'type': 'unknown',
            'title': 'Unknown Error',
            'solution': 'No automatic solution available. Review the error traceback.',
            'severity': 'MEDIUM',
            'value': None
        }

    def _print_report(self):
        """Print analysis report"""
        print("\n" + "=" * 80)
        print("ANALYSIS REPORT")
        print("=" * 80)

        if not self.errors:
            print("\n[OK] No errors found in log file!")
            return

        print(f"\n[!] Found {len(self.errors)} error(s)\n")

        # Group errors by type
        grouped = defaultdict(list)
        for error in self.errors:
            error_type = error['analysis']['type']
            grouped[error_type].append(error)

        # Print each error type
        for i, (error_type, errors) in enumerate(grouped.items(), 1):
            first_error = errors[0]
            analysis = first_error['analysis']

            print(f"\n{'-' * 80}")
            print(f"ERROR #{i}: {analysis['title']}")
            print(f"Severity: {analysis['severity']}")
            print(f"Occurrences: {len(errors)}")
            print(f"{'-' * 80}")

            if analysis['value']:
                print(f"\nValue: {analysis['value']}")

            print(f"\nSOLUTION:")
            print(analysis['solution'])

            # Show first few lines of first occurrence
            print(f"\nFirst occurrence preview:")
            for line in first_error['lines'][:5]:
                print(f"  {line.rstrip()}")

            if len(first_error['lines']) > 5:
                print(f"  ... ({len(first_error['lines']) - 5} more lines)")


def main():
    parser = argparse.ArgumentParser(description="Odoo Log Analyzer")
    parser.add_argument("--log", required=True, help="Path to odoo.log file")
    parser.add_argument("--tail", type=int, help="Analyze last N lines only")
    parser.add_argument("--filter", help="Filter errors containing this text")

    args = parser.parse_args()

    analyzer = OdooLogAnalyzer(args.log)
    success = analyzer.analyze(tail_lines=args.tail, error_filter=args.filter)

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())


```
