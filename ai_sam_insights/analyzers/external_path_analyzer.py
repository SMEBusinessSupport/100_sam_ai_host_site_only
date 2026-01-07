# -*- coding: utf-8 -*-
"""
External Path Analyzer for SAM AI Insights

Detects code that references files OUTSIDE the scanned modules.
This is a critical architectural violation in Odoo module design.

A well-designed Odoo module should ONLY reference:
1. Its own files (within its module directory)
2. Files from modules declared in its 'depends' list
3. Standard Odoo/Python paths

RED FLAGS detected by this analyzer:
- Hardcoded absolute paths to other repositories
- Relative paths escaping the module (../..)
- File operations targeting external locations
- Path constructions pointing outside module boundaries

Author: SAM AI Development Team
Created: 2025-12-26
"""
import os
import re
import ast
from pathlib import Path
from typing import Dict, List, Any, Optional, Set
import logging

_logger = logging.getLogger(__name__)


class ExternalPathAnalyzer:
    """Analyzes code for external path references - architectural violations"""

    # Patterns that indicate external path references
    EXTERNAL_PATH_PATTERNS = [
        # Absolute paths to other repos (Windows)
        r'[A-Za-z]:\\[^"\']*github-repos\\(?!05-samai-core)',
        # Absolute paths to other repos (Unix)
        r'/[^"\']*github-repos/(?!05-samai-core)',
        # Parent directory traversal that might escape module
        r'\.\./\.\.',  # Going up 2+ levels is suspicious
        r'\.\.[/\\]\.\.[/\\]',  # Windows variant
        # Common external repo patterns
        r'samai-workflow-automator',
        r'06-samai',
        r'07-samai',
        r'08-samai',
    ]

    # File operation functions to check
    FILE_OPERATIONS = [
        'open', 'read', 'write', 'read_text', 'write_text',
        'read_bytes', 'write_bytes', 'mkdir', 'rmdir', 'unlink',
        'copy', 'move', 'rename', 'exists', 'is_file', 'is_dir',
        'glob', 'rglob', 'iterdir', 'listdir', 'walk',
    ]

    # Path construction functions
    PATH_CONSTRUCTIONS = [
        'Path', 'os.path.join', 'os.path.abspath', 'os.path.dirname',
        'os.path.realpath', 'pathlib.Path', 'join',
    ]

    def __init__(self, base_path: str, module_filter: Optional[List[str]] = None):
        """
        Initialize the analyzer.

        Args:
            base_path: Root path being scanned (e.g., 05-samai-core)
            module_filter: List of module names being scanned
        """
        self.base_path = Path(base_path)
        self.module_filter = module_filter or []
        self.findings = {
            'hardcoded_external_paths': [],
            'relative_path_escapes': [],
            'suspicious_file_operations': [],
            'external_imports': [],
            'summary': {},
        }
        # Build set of allowed paths (scanned modules)
        self._allowed_modules = set(self.module_filter) if self.module_filter else set()

    def analyze(self, python_scan: Dict = None) -> Dict[str, Any]:
        """
        Run external path analysis on Python files.

        Args:
            python_scan: Optional pre-scanned Python data (not used currently)

        Returns:
            Dict containing all findings
        """
        _logger.info("Starting external path analysis")
        _logger.info(f"Base path: {self.base_path}")
        _logger.info(f"Allowed modules: {self._allowed_modules}")

        # Scan all Python files
        for py_file in self.base_path.rglob('*.py'):
            # Apply module filter
            if self.module_filter:
                try:
                    rel_path = py_file.relative_to(self.base_path)
                    top_module = rel_path.parts[0] if rel_path.parts else ''
                    if top_module not in self.module_filter:
                        continue
                except ValueError:
                    continue

            # Skip common non-code directories
            if any(skip in str(py_file) for skip in ['.git', 'node_modules', '__pycache__', '.venv']):
                continue

            self._analyze_file(py_file)

        # Also scan XML files for path references
        for xml_file in self.base_path.rglob('*.xml'):
            if self.module_filter:
                try:
                    rel_path = xml_file.relative_to(self.base_path)
                    top_module = rel_path.parts[0] if rel_path.parts else ''
                    if top_module not in self.module_filter:
                        continue
                except ValueError:
                    continue

            if any(skip in str(xml_file) for skip in ['.git', 'node_modules']):
                continue

            self._analyze_xml_file(xml_file)

        # Also scan JS files
        for js_file in self.base_path.rglob('*.js'):
            if self.module_filter:
                try:
                    rel_path = js_file.relative_to(self.base_path)
                    top_module = rel_path.parts[0] if rel_path.parts else ''
                    if top_module not in self.module_filter:
                        continue
                except ValueError:
                    continue

            if any(skip in str(js_file) for skip in ['.git', 'node_modules', 'PREPARE_FOR_DELETION']):
                continue

            self._analyze_js_file(js_file)

        self._generate_summary()

        _logger.info(f"External path analysis complete: {self.findings['summary']}")

        return self.findings

    def _analyze_file(self, file_path: Path):
        """Analyze a single Python file for external path references."""
        try:
            content = file_path.read_text(encoding='utf-8', errors='ignore')
            rel_path = str(file_path.relative_to(self.base_path))

            # Method 1: Pattern-based detection (fast, catches string literals)
            self._check_patterns(content, rel_path, file_path)

            # Method 2: AST-based detection (accurate, catches path constructions)
            self._check_ast(content, rel_path, file_path)

        except Exception as e:
            _logger.debug(f"Error analyzing {file_path}: {e}")

    def _check_patterns(self, content: str, rel_path: str, file_path: Path):
        """Check for external path patterns in file content."""
        lines = content.split('\n')

        for line_num, line in enumerate(lines, 1):
            # Skip comments
            stripped = line.strip()
            if stripped.startswith('#'):
                continue

            for pattern in self.EXTERNAL_PATH_PATTERNS:
                matches = re.finditer(pattern, line, re.IGNORECASE)
                for match in matches:
                    # Determine severity
                    if 'github-repos' in match.group().lower():
                        severity = 'critical'
                        finding_type = 'hardcoded_external_paths'
                    elif '..' in match.group():
                        severity = 'warning'
                        finding_type = 'relative_path_escapes'
                    else:
                        severity = 'warning'
                        finding_type = 'hardcoded_external_paths'

                    self.findings[finding_type].append({
                        'file': rel_path,
                        'line_number': line_num,
                        'line_content': line.strip()[:200],
                        'matched_pattern': match.group()[:100],
                        'severity': severity,
                        'recommendation': self._get_recommendation(finding_type, match.group()),
                    })

    def _check_ast(self, content: str, rel_path: str, file_path: Path):
        """Use AST to find path constructions and file operations."""
        try:
            tree = ast.parse(content)
        except SyntaxError:
            return

        for node in ast.walk(tree):
            # Check function calls
            if isinstance(node, ast.Call):
                func_name = self._get_func_name(node)

                # Check if it's a file operation or path construction
                if any(op in func_name for op in self.FILE_OPERATIONS + self.PATH_CONSTRUCTIONS):
                    # Look at arguments for external paths
                    for arg in node.args:
                        if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
                            path_arg = arg.value
                            if self._is_external_path(path_arg):
                                self.findings['suspicious_file_operations'].append({
                                    'file': rel_path,
                                    'line_number': node.lineno,
                                    'function': func_name,
                                    'path_argument': path_arg[:200],
                                    'severity': 'critical' if 'github-repos' in path_arg.lower() else 'warning',
                                    'recommendation': f"File operation '{func_name}' references external path. "
                                                     f"Refactor to use module-relative paths or Odoo attachments.",
                                })

            # Check for suspicious imports
            if isinstance(node, ast.ImportFrom):
                if node.module and self._is_external_import(node.module):
                    self.findings['external_imports'].append({
                        'file': rel_path,
                        'line_number': node.lineno,
                        'import_module': node.module,
                        'severity': 'warning',
                        'recommendation': f"Import from '{node.module}' may reference external module. "
                                         f"Ensure it's declared in manifest depends.",
                    })

    def _analyze_xml_file(self, file_path: Path):
        """Analyze XML file for external path references."""
        try:
            content = file_path.read_text(encoding='utf-8', errors='ignore')
            rel_path = str(file_path.relative_to(self.base_path))
            lines = content.split('\n')

            for line_num, line in enumerate(lines, 1):
                for pattern in self.EXTERNAL_PATH_PATTERNS:
                    matches = re.finditer(pattern, line, re.IGNORECASE)
                    for match in matches:
                        self.findings['hardcoded_external_paths'].append({
                            'file': rel_path,
                            'line_number': line_num,
                            'line_content': line.strip()[:200],
                            'matched_pattern': match.group()[:100],
                            'file_type': 'xml',
                            'severity': 'critical',
                            'recommendation': "XML file contains hardcoded external path. "
                                            "Use Odoo's file reference system instead.",
                        })
        except Exception as e:
            _logger.debug(f"Error analyzing XML {file_path}: {e}")

    def _analyze_js_file(self, file_path: Path):
        """Analyze JavaScript file for external path references."""
        try:
            content = file_path.read_text(encoding='utf-8', errors='ignore')
            rel_path = str(file_path.relative_to(self.base_path))
            lines = content.split('\n')

            for line_num, line in enumerate(lines, 1):
                # Skip comments
                stripped = line.strip()
                if stripped.startswith('//') or stripped.startswith('/*'):
                    continue

                for pattern in self.EXTERNAL_PATH_PATTERNS:
                    matches = re.finditer(pattern, line, re.IGNORECASE)
                    for match in matches:
                        self.findings['hardcoded_external_paths'].append({
                            'file': rel_path,
                            'line_number': line_num,
                            'line_content': line.strip()[:200],
                            'matched_pattern': match.group()[:100],
                            'file_type': 'javascript',
                            'severity': 'critical',
                            'recommendation': "JavaScript file contains hardcoded external path. "
                                            "Use Odoo's web asset system for file references.",
                        })
        except Exception as e:
            _logger.debug(f"Error analyzing JS {file_path}: {e}")

    def _get_func_name(self, node: ast.Call) -> str:
        """Extract function name from AST Call node."""
        if isinstance(node.func, ast.Name):
            return node.func.id
        elif isinstance(node.func, ast.Attribute):
            parts = []
            current = node.func
            while isinstance(current, ast.Attribute):
                parts.append(current.attr)
                current = current.value
            if isinstance(current, ast.Name):
                parts.append(current.id)
            return '.'.join(reversed(parts))
        return ''

    def _is_external_path(self, path_str: str) -> bool:
        """Check if a path string references an external location."""
        path_lower = path_str.lower()

        # Check for other github repos
        if 'github-repos' in path_lower and '05-samai-core' not in path_lower:
            return True

        # Check for specific external repo patterns
        external_patterns = ['06-samai', '07-samai', '08-samai', 'workflow-automator']
        if any(pattern in path_lower for pattern in external_patterns):
            return True

        # Check for excessive parent traversal
        if path_str.count('..') >= 3:
            return True

        return False

    def _is_external_import(self, module_path: str) -> bool:
        """Check if an import might reference an external module."""
        # This is a basic check - could be enhanced with manifest parsing
        external_patterns = ['workflow_automator', 'samai_automator']
        return any(pattern in module_path.lower() for pattern in external_patterns)

    def _get_recommendation(self, finding_type: str, matched: str) -> str:
        """Get recommendation text based on finding type."""
        if 'github-repos' in matched.lower():
            return ("CRITICAL: Hardcoded path to external git repository detected. "
                   "This breaks module portability. Refactor to use: "
                   "1) Module-relative paths, 2) Odoo attachments, or "
                   "3) Proper module dependencies via manifest.")
        elif '..' in matched:
            return ("Relative path escaping module boundary detected. "
                   "Use odoo.modules.get_module_path() or __file__ based paths instead.")
        else:
            return ("External path reference detected. "
                   "Ensure this path is portable across environments.")

    def _generate_summary(self):
        """Generate summary statistics."""
        total_critical = 0
        total_warning = 0

        for category in ['hardcoded_external_paths', 'relative_path_escapes',
                        'suspicious_file_operations', 'external_imports']:
            for item in self.findings.get(category, []):
                if item.get('severity') == 'critical':
                    total_critical += 1
                else:
                    total_warning += 1

        self.findings['summary'] = {
            'hardcoded_external_paths': len(self.findings['hardcoded_external_paths']),
            'relative_path_escapes': len(self.findings['relative_path_escapes']),
            'suspicious_file_operations': len(self.findings['suspicious_file_operations']),
            'external_imports': len(self.findings['external_imports']),
            'total_findings': (
                len(self.findings['hardcoded_external_paths']) +
                len(self.findings['relative_path_escapes']) +
                len(self.findings['suspicious_file_operations']) +
                len(self.findings['external_imports'])
            ),
            'critical_count': total_critical,
            'warning_count': total_warning,
        }
