# -*- coding: utf-8 -*-
"""
Integration Reference Analyzer for SAM AI Insights

Finds all references to external integrations like N8N and ai_automator
across the codebase. Reports file paths and line numbers for each reference.

This helps track:
- Where integrations are configured
- Which files depend on external services
- Integration points that need attention during upgrades
"""
import re
import os
from pathlib import Path
from typing import Dict, List, Any, Optional, Set
import logging

_logger = logging.getLogger(__name__)


class IntegrationReferenceAnalyzer:
    """
    Analyzes source files to find references to external integrations.

    Tracks:
    - N8N workflow references (webhooks, workflow IDs, API calls)
    - ai_automator references (module imports, API calls, configurations)
    - Custom integration patterns (configurable)
    """

    # N8N patterns to search for
    N8N_PATTERNS = {
        'webhook': [
            r'n8n.*webhook',
            r'webhook.*n8n',
            r'/webhook/',
            r'webhook_url',
            r'webhook[-_]?id',
        ],
        'workflow': [
            r'n8n.*workflow',
            r'workflow.*n8n',
            r'workflow[-_]?id',
            r'workflow[-_]?name',
            r'execute[-_]?workflow',
        ],
        'api': [
            r'n8n[-_.]?api',
            r'n8n[-_.]?url',
            r'n8n[-_.]?host',
            r'n8n[-_.]?endpoint',
            r'n8n[-_.]?base[-_]?url',
        ],
        'config': [
            r'n8n[-_.]?config',
            r'n8n[-_.]?settings',
            r'n8n[-_.]?credentials',
            r'n8n[-_.]?token',
            r'n8n[-_.]?key',
        ],
        'import': [
            r'from.*n8n',
            r'import.*n8n',
            r'require.*n8n',
        ],
        'reference': [
            r'\bn8n\b',
            r'N8N',
        ],
    }

    # ai_automator patterns to search for
    AI_AUTOMATOR_PATTERNS = {
        'module': [
            r'ai[-_.]?automator',
            r'from.*ai_automator',
            r'import.*ai_automator',
        ],
        'model': [
            r'automator\.task',
            r'automator\.workflow',
            r'automator\.trigger',
            r'automator\.action',
            r'automator\.schedule',
        ],
        'api': [
            r'automator[-_.]?api',
            r'automator[-_.]?endpoint',
            r'automator[-_.]?url',
            r'/api/automator',
        ],
        'config': [
            r'automator[-_.]?config',
            r'automator[-_.]?settings',
            r'AUTOMATOR[-_]',
        ],
        'reference': [
            r'\bautomator\b',
            r'Automator',
            r'AUTOMATOR',
        ],
    }

    # File extensions to scan
    SCAN_EXTENSIONS = {
        '.py': 'python',
        '.js': 'javascript',
        '.xml': 'xml',
        '.json': 'json',
        '.yaml': 'yaml',
        '.yml': 'yaml',
        '.html': 'html',
        '.css': 'css',
        '.scss': 'scss',
    }

    def __init__(self, base_path: str, module_filter: Optional[List[str]] = None):
        """
        Initialize the analyzer.

        :param base_path: Root directory to scan
        :param module_filter: Optional list of module names to include
        """
        self.base_path = Path(base_path)
        self.module_filter = module_filter or []
        self.findings = {
            'n8n': {
                'webhook': [],
                'workflow': [],
                'api': [],
                'config': [],
                'import': [],
                'reference': [],
            },
            'ai_automator': {
                'module': [],
                'model': [],
                'api': [],
                'config': [],
                'reference': [],
            },
            'summary': {
                'total_files_scanned': 0,
                'files_with_n8n_refs': 0,
                'files_with_automator_refs': 0,
                'total_n8n_references': 0,
                'total_automator_references': 0,
                'n8n_by_category': {},
                'automator_by_category': {},
            },
        }

    def analyze(self) -> Dict[str, Any]:
        """
        Run the integration reference analysis.

        :return: Analysis results with findings
        """
        _logger.info(f"Starting integration reference analysis of {self.base_path}")

        files_with_n8n = set()
        files_with_automator = set()

        # Scan all relevant files
        for ext, file_type in self.SCAN_EXTENSIONS.items():
            for file_path in self.base_path.rglob(f'*{ext}'):
                if self._should_scan(file_path):
                    n8n_refs, automator_refs = self._analyze_file(file_path, file_type)

                    if n8n_refs:
                        files_with_n8n.add(str(file_path))
                    if automator_refs:
                        files_with_automator.add(str(file_path))

        # Update summary
        self._update_summary(files_with_n8n, files_with_automator)

        _logger.info(
            f"Integration reference analysis complete: "
            f"{self.findings['summary']['total_n8n_references']} N8N refs, "
            f"{self.findings['summary']['total_automator_references']} automator refs"
        )

        return self.findings

    def _should_scan(self, file_path: Path) -> bool:
        """Check if file should be scanned based on filters"""
        path_str = str(file_path)

        # Skip common non-source directories
        if any(skip in path_str for skip in
               ['__pycache__', 'venv', '.git', 'node_modules', '.egg', '.tox']):
            return False

        # Apply module filter
        if self.module_filter:
            try:
                rel_path = file_path.relative_to(self.base_path)
                top_module = rel_path.parts[0] if rel_path.parts else ''
                if top_module not in self.module_filter:
                    return False
            except ValueError:
                return False

        self.findings['summary']['total_files_scanned'] += 1
        return True

    def _analyze_file(self, file_path: Path, file_type: str) -> tuple:
        """
        Analyze a file for integration references.

        :param file_path: Path to file
        :param file_type: Type of file (python, javascript, etc.)
        :return: Tuple of (n8n_found, automator_found) booleans
        """
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
        except Exception as e:
            _logger.warning(f"Could not read {file_path}: {e}")
            return False, False

        rel_path = str(file_path.relative_to(self.base_path))
        n8n_found = False
        automator_found = False

        for line_num, line in enumerate(lines, 1):
            # Check N8N patterns
            for category, patterns in self.N8N_PATTERNS.items():
                for pattern in patterns:
                    if re.search(pattern, line, re.IGNORECASE):
                        self._add_finding(
                            'n8n', category, file_path, rel_path,
                            line_num, line.strip(), file_type, pattern
                        )
                        n8n_found = True
                        break  # Only one match per category per line

            # Check ai_automator patterns
            for category, patterns in self.AI_AUTOMATOR_PATTERNS.items():
                for pattern in patterns:
                    if re.search(pattern, line, re.IGNORECASE):
                        self._add_finding(
                            'ai_automator', category, file_path, rel_path,
                            line_num, line.strip(), file_type, pattern
                        )
                        automator_found = True
                        break  # Only one match per category per line

        return n8n_found, automator_found

    def _add_finding(
        self,
        integration: str,
        category: str,
        file_path: Path,
        rel_path: str,
        line_num: int,
        line_content: str,
        file_type: str,
        matched_pattern: str
    ):
        """Add a finding to the results"""
        # Truncate long lines
        preview = line_content[:150]
        if len(line_content) > 150:
            preview += '...'

        finding = {
            'file_path': str(file_path),
            'relative_path': rel_path,
            'line_number': line_num,
            'line_content': preview,
            'file_type': file_type,
            'category': category,
            'matched_pattern': matched_pattern,
        }

        # Avoid duplicate findings (same file, line, category)
        existing = self.findings[integration][category]
        for existing_finding in existing:
            if (existing_finding['relative_path'] == rel_path and
                existing_finding['line_number'] == line_num):
                return  # Skip duplicate

        self.findings[integration][category].append(finding)

    def _update_summary(self, files_with_n8n: Set[str], files_with_automator: Set[str]):
        """Update summary statistics"""
        summary = self.findings['summary']

        summary['files_with_n8n_refs'] = len(files_with_n8n)
        summary['files_with_automator_refs'] = len(files_with_automator)

        # Count by category
        n8n_by_cat = {}
        total_n8n = 0
        for category, refs in self.findings['n8n'].items():
            n8n_by_cat[category] = len(refs)
            total_n8n += len(refs)

        automator_by_cat = {}
        total_automator = 0
        for category, refs in self.findings['ai_automator'].items():
            automator_by_cat[category] = len(refs)
            total_automator += len(refs)

        summary['n8n_by_category'] = n8n_by_cat
        summary['automator_by_category'] = automator_by_cat
        summary['total_n8n_references'] = total_n8n
        summary['total_automator_references'] = total_automator

    def get_all_n8n_references(self) -> List[Dict[str, Any]]:
        """Get all N8N references as a flat list, sorted by file and line"""
        all_refs = []
        for category, refs in self.findings['n8n'].items():
            for ref in refs:
                ref_copy = ref.copy()
                ref_copy['integration'] = 'n8n'
                all_refs.append(ref_copy)

        return sorted(all_refs, key=lambda x: (x['relative_path'], x['line_number']))

    def get_all_automator_references(self) -> List[Dict[str, Any]]:
        """Get all ai_automator references as a flat list, sorted by file and line"""
        all_refs = []
        for category, refs in self.findings['ai_automator'].items():
            for ref in refs:
                ref_copy = ref.copy()
                ref_copy['integration'] = 'ai_automator'
                all_refs.append(ref_copy)

        return sorted(all_refs, key=lambda x: (x['relative_path'], x['line_number']))

    def get_files_by_integration(self, integration: str) -> Dict[str, List[Dict]]:
        """
        Group references by file for a specific integration.

        :param integration: 'n8n' or 'ai_automator'
        :return: Dict mapping file paths to their references
        """
        files = {}

        if integration not in self.findings:
            return files

        for category, refs in self.findings[integration].items():
            for ref in refs:
                rel_path = ref['relative_path']
                if rel_path not in files:
                    files[rel_path] = []
                files[rel_path].append(ref)

        # Sort references within each file by line number
        for path in files:
            files[path].sort(key=lambda x: x['line_number'])

        return files

    def find_custom_pattern(
        self,
        pattern: str,
        name: str = 'custom'
    ) -> List[Dict[str, Any]]:
        """
        Find custom patterns across the codebase.

        :param pattern: Regex pattern to search for
        :param name: Name for the search (for reporting)
        :return: List of findings
        """
        findings = []

        for ext, file_type in self.SCAN_EXTENSIONS.items():
            for file_path in self.base_path.rglob(f'*{ext}'):
                if not self._should_scan(file_path):
                    continue

                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        lines = f.readlines()

                    rel_path = str(file_path.relative_to(self.base_path))

                    for line_num, line in enumerate(lines, 1):
                        if re.search(pattern, line, re.IGNORECASE):
                            preview = line.strip()[:150]
                            if len(line.strip()) > 150:
                                preview += '...'

                            findings.append({
                                'file_path': str(file_path),
                                'relative_path': rel_path,
                                'line_number': line_num,
                                'line_content': preview,
                                'file_type': file_type,
                                'search_name': name,
                                'matched_pattern': pattern,
                            })

                except Exception as e:
                    _logger.warning(f"Could not read {file_path}: {e}")

        return sorted(findings, key=lambda x: (x['relative_path'], x['line_number']))
