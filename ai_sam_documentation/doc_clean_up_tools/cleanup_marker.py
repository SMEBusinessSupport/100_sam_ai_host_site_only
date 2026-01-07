#!/usr/bin/env python3
"""
Cleanup Marker Tool
===================

Injects color-coded cleanup annotations into Python files based on audit findings.
Enables AI-to-human delegation of code cleanup tasks.

Usage:
    # Apply markers from audit report
    python cleanup_marker.py --audit audit_report.json --path ./models

    # Generate report only (no modifications)
    python cleanup_marker.py --audit audit_report.json --report-only

    # Remove all cleanup markers
    python cleanup_marker.py --clean --path ./models

    # Count markers by severity
    python cleanup_marker.py --count --path ./models

Author: CTO Auditor Agent
Version: 1.0
Date: 2025-12-19
"""

import argparse
import json
import os
import re
from pathlib import Path
from datetime import datetime
from collections import defaultdict


# ============================================================
# ANNOTATION TEMPLATES
# ============================================================

TEMPLATES = {
    'RED': {
        'border': '=' * 60,
        'prefix': '# ',
        'color_name': 'CRITICAL',
    },
    'ORANGE': {
        'border': '-' * 60,
        'prefix': '# ',
        'color_name': 'HIGH PRIORITY',
    },
    'YELLOW': {
        'border': '.' * 60,
        'prefix': '# ',
        'color_name': 'MEDIUM PRIORITY',
    },
    'GREEN': {
        'border': '. ' * 30,
        'prefix': '# ',
        'color_name': 'LOW PRIORITY',
    },
    'BLUE': {
        'border': '~' * 60,
        'prefix': '# ',
        'color_name': 'INFO',
    },
}


def generate_annotation(finding: dict) -> str:
    """Generate a cleanup annotation block from a finding."""
    severity = finding.get('severity', 'YELLOW')
    cleanup_type = finding.get('type', 'REFACTOR')
    title = finding.get('title', 'Cleanup required')
    reason = finding.get('reason', '')
    actions = finding.get('action', [])
    ticket = finding.get('id', 'CLEANUP-XXX')
    audit_date = finding.get('audit_date', datetime.now().strftime('%Y-%m-%d'))
    score_impact = finding.get('score_impact', 0)
    verification = finding.get('verification', '')

    template = TEMPLATES.get(severity, TEMPLATES['YELLOW'])
    border = template['border']
    prefix = template['prefix']

    lines = []
    lines.append(f"{prefix}{border}")
    lines.append(f"{prefix}[CLEANUP:{severity}:{cleanup_type}] {title}")
    lines.append(f"{prefix}{border}")

    if reason:
        lines.append(f"{prefix}Reason: {reason}")
        lines.append(f"{prefix}")

    if actions:
        lines.append(f"{prefix}Action:")
        for i, action in enumerate(actions, 1):
            lines.append(f"{prefix}  {i}. {action}")
        lines.append(f"{prefix}")

    if verification:
        lines.append(f"{prefix}Verify: {verification}")
        lines.append(f"{prefix}")

    meta_parts = [f"Ticket: {ticket}", f"Audit: {audit_date}"]
    if score_impact:
        meta_parts.append(f"Score Impact: {score_impact:+d}")
    lines.append(f"{prefix}{' | '.join(meta_parts)}")

    lines.append(f"{prefix}{border}")

    return '\n'.join(lines)


def inject_annotation(file_path: str, line_number: int, annotation: str, scope: str = 'line') -> str:
    """Inject annotation into file content at specified line."""
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Convert 1-indexed line number to 0-indexed
    idx = max(0, line_number - 1)

    # Add annotation lines
    annotation_lines = [line + '\n' for line in annotation.split('\n')]

    if scope == 'file':
        # Insert at very top of file
        lines = annotation_lines + ['\n'] + lines
    else:
        # Insert before the specified line
        lines = lines[:idx] + annotation_lines + lines[idx:]

    return ''.join(lines)


def remove_annotations(content: str) -> str:
    """Remove all cleanup annotations from file content."""
    # Pattern to match annotation blocks
    patterns = [
        # Multi-line blocks with borders
        r'# [=\-\.~]{20,}\n(?:# \[CLEANUP:.*?\n)+(?:# .*?\n)*# [=\-\.~]{20,}\n\n?',
        # Single line annotations
        r'# \[CLEANUP:[A-Z]+:[A-Z_]+\].*?\n',
    ]

    result = content
    for pattern in patterns:
        result = re.sub(pattern, '', result, flags=re.MULTILINE)

    return result


def count_annotations(path: str) -> dict:
    """Count cleanup annotations by severity in a directory."""
    counts = defaultdict(int)
    files_with_markers = defaultdict(list)

    path = Path(path)
    pattern = r'\[CLEANUP:([A-Z]+):([A-Z_]+)\]'

    for py_file in path.rglob('*.py'):
        try:
            content = py_file.read_text(encoding='utf-8')
            matches = re.findall(pattern, content)
            for severity, cleanup_type in matches:
                counts[severity] += 1
                files_with_markers[str(py_file)].append(f"{severity}:{cleanup_type}")
        except Exception as e:
            print(f"Warning: Could not read {py_file}: {e}")

    return {
        'counts': dict(counts),
        'files': dict(files_with_markers),
        'total': sum(counts.values())
    }


def apply_audit_markers(audit_file: str, base_path: str, dry_run: bool = False) -> dict:
    """Apply markers from an audit JSON file."""
    with open(audit_file, 'r', encoding='utf-8') as f:
        audit = json.load(f)

    results = {
        'modified_files': [],
        'skipped_files': [],
        'errors': [],
        'counts': defaultdict(int)
    }

    audit_date = audit.get('audit_date', datetime.now().strftime('%Y-%m-%d'))

    for finding in audit.get('findings', []):
        finding['audit_date'] = audit_date
        file_rel = finding.get('file', '')
        file_path = os.path.join(base_path, file_rel)

        if not os.path.exists(file_path):
            results['errors'].append(f"File not found: {file_path}")
            continue

        try:
            annotation = generate_annotation(finding)
            line = finding.get('line', 1)
            scope = finding.get('scope', 'line')

            new_content = inject_annotation(file_path, line, annotation, scope)

            if not dry_run:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                results['modified_files'].append(file_path)
            else:
                results['skipped_files'].append(file_path)

            severity = finding.get('severity', 'YELLOW')
            results['counts'][severity] += 1

        except Exception as e:
            results['errors'].append(f"Error processing {file_path}: {e}")

    return results


def clean_markers(path: str, dry_run: bool = False) -> dict:
    """Remove all cleanup markers from files in path."""
    results = {
        'cleaned_files': [],
        'unchanged_files': [],
        'errors': []
    }

    path = Path(path)

    for py_file in path.rglob('*.py'):
        try:
            content = py_file.read_text(encoding='utf-8')
            cleaned = remove_annotations(content)

            if content != cleaned:
                if not dry_run:
                    py_file.write_text(cleaned, encoding='utf-8')
                results['cleaned_files'].append(str(py_file))
            else:
                results['unchanged_files'].append(str(py_file))

        except Exception as e:
            results['errors'].append(f"Error cleaning {py_file}: {e}")

    return results


def print_report(title: str, data: dict):
    """Print a formatted report."""
    border = '=' * 50
    print(f"\n{border}")
    print(f"  {title}")
    print(border)

    if 'counts' in data:
        counts = data.get('counts', {})
        print("\nMARKERS BY SEVERITY:")
        for severity in ['RED', 'ORANGE', 'YELLOW', 'GREEN', 'BLUE']:
            count = counts.get(severity, 0)
            if count > 0:
                color_desc = TEMPLATES.get(severity, {}).get('color_name', severity)
                print(f"  {severity:8} ({color_desc:15}): {count}")
        print(f"  {'-' * 30}")
        print(f"  {'TOTAL':24}: {data.get('total', sum(counts.values()))}")

    if 'files' in data and data['files']:
        print("\nFILES WITH MARKERS:")
        for file_path, markers in data['files'].items():
            # Show relative path if possible
            display_path = file_path.split('ai_sam_base')[-1] if 'ai_sam_base' in file_path else file_path
            print(f"  {display_path}")
            for marker in markers:
                print(f"    -> [{marker}]")

    if 'modified_files' in data and data['modified_files']:
        print("\nFILES MODIFIED:")
        for f in data['modified_files']:
            print(f"  [OK] {f}")

    if 'cleaned_files' in data and data['cleaned_files']:
        print("\nFILES CLEANED:")
        for f in data['cleaned_files']:
            print(f"  [OK] {f}")

    if 'errors' in data and data['errors']:
        print("\nERRORS:")
        for e in data['errors']:
            print(f"  [X] {e}")

    print(f"\n{border}\n")


def generate_sample_audit() -> dict:
    """Generate a sample audit report for testing/documentation."""
    return {
        "audit_date": datetime.now().strftime('%Y-%m-%d'),
        "module": "example_module",
        "score": 6,
        "findings": [
            {
                "id": "CLEANUP-001",
                "severity": "RED",
                "type": "DELETE",
                "file": "models/old_file.py",
                "line": 1,
                "scope": "file",
                "title": "ENTIRE FILE FLAGGED FOR DELETION",
                "reason": "Class collision with another file",
                "action": [
                    "DELETE this entire file",
                    "Edit __init__.py - remove import",
                    "Test module upgrade"
                ],
                "score_impact": -1
            },
            {
                "id": "CLEANUP-002",
                "severity": "ORANGE",
                "type": "DEPRECATED",
                "file": "models/user_profile.py",
                "line": 50,
                "scope": "block",
                "title": "Field replaced by new model",
                "reason": "Deprecated 2025-12-17, replacement model now active",
                "action": [
                    "Verify replacement is working",
                    "Search for usages",
                    "DELETE if safe"
                ],
                "verification": "env['new.model'].search_count([]) > 0"
            },
            {
                "id": "CLEANUP-003",
                "severity": "YELLOW",
                "type": "DRY",
                "file": "models/calculations.py",
                "line": 100,
                "scope": "method",
                "title": "Duplicated logic in multiple files",
                "reason": "Same formula repeated in 5 files",
                "action": [
                    "Create shared utility function",
                    "Refactor callers to use utility",
                    "Test functionality"
                ]
            },
            {
                "id": "CLEANUP-004",
                "severity": "GREEN",
                "type": "SPLIT",
                "file": "models/large_file.py",
                "line": 1,
                "scope": "file",
                "title": "File too large - consider splitting",
                "reason": "File has 3000+ lines, hard to maintain",
                "action": [
                    "Consider extracting related code",
                    "Move to separate module files"
                ]
            }
        ]
    }


def main():
    parser = argparse.ArgumentParser(
        description='Cleanup Marker Tool - Inject/remove cleanup annotations',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Apply markers from audit
  python cleanup_marker.py --audit audit.json --path ./models

  # Preview without modifying (dry run)
  python cleanup_marker.py --audit audit.json --path ./models --dry-run

  # Count existing markers
  python cleanup_marker.py --count --path ./models

  # Remove all markers after cleanup
  python cleanup_marker.py --clean --path ./models

  # Generate sample audit JSON
  python cleanup_marker.py --sample > audit.json
        """
    )

    parser.add_argument('--audit', help='Path to audit JSON file')
    parser.add_argument('--path', default='.', help='Base path for file operations')
    parser.add_argument('--count', action='store_true', help='Count markers by severity')
    parser.add_argument('--clean', action='store_true', help='Remove all cleanup markers')
    parser.add_argument('--dry-run', action='store_true', help='Preview changes without modifying files')
    parser.add_argument('--sample', action='store_true', help='Output sample audit JSON')
    parser.add_argument('--report-only', action='store_true', help='Generate report without modifying files')

    args = parser.parse_args()

    if args.sample:
        print(json.dumps(generate_sample_audit(), indent=2))
        return

    if args.count:
        result = count_annotations(args.path)
        print_report('CLEANUP MARKER COUNT', result)
        return

    if args.clean:
        result = clean_markers(args.path, dry_run=args.dry_run)
        action = 'PREVIEW' if args.dry_run else 'COMPLETE'
        print_report(f'MARKER CLEANUP {action}', result)
        return

    if args.audit:
        dry_run = args.dry_run or args.report_only
        result = apply_audit_markers(args.audit, args.path, dry_run=dry_run)
        action = 'PREVIEW' if dry_run else 'COMPLETE'
        print_report(f'MARKER APPLICATION {action}', result)
        return

    parser.print_help()


if __name__ == '__main__':
    main()
