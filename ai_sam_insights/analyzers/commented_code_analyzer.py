# -*- coding: utf-8 -*-
"""
Commented Code Analyzer for SAM AI Insights

Detects commented-out code that may be:
- Dead code (commented for deletion)
- Redundant code
- Old implementations

Reports file path and line numbers for each finding.
"""
import re
import os
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
import logging

_logger = logging.getLogger(__name__)


class CommentedCodeAnalyzer:
    """
    Analyzes source files to detect commented-out code blocks.

    Supports:
    - Python files (.py)
    - JavaScript files (.js)
    - XML files (.xml)
    """

    # Python code patterns that indicate commented-out code
    PYTHON_CODE_PATTERNS = [
        r'^\s*#\s*(def\s+\w+|class\s+\w+|if\s+|elif\s+|else:|for\s+|while\s+|try:|except|finally:)',
        r'^\s*#\s*(return\s+|raise\s+|yield\s+|import\s+|from\s+)',
        r'^\s*#\s*\w+\s*=\s*',  # Variable assignments
        r'^\s*#\s*(self\.\w+|super\(\))',
        r'^\s*#\s*@(api\.|staticmethod|classmethod|property)',  # Decorators
        r'^\s*#\s*_\w+\s*=',  # Private attributes like _name, _inherit
    ]

    # JavaScript code patterns
    JS_CODE_PATTERNS = [
        r'^\s*//\s*(function\s+\w+|const\s+|let\s+|var\s+)',
        r'^\s*//\s*(return\s+|throw\s+|if\s*\(|else\s*{|for\s*\(|while\s*\()',
        r'^\s*//\s*(import\s+|export\s+|class\s+\w+)',
        r'^\s*//\s*(this\.\w+|super\()',
        r'^\s*//\s*\w+\s*[=:]\s*',
        r'^\s*//\s*(async\s+|await\s+|\.then\(|\.catch\()',
        r'^\s*/\*\*?[\s\S]*?(function|class|const|let|var)\s+\w+',  # Block comments with code
    ]

    # XML code patterns (commented elements)
    XML_CODE_PATTERNS = [
        r'<!--\s*<(record|template|field|button|group|tree|form|kanban)',
        r'<!--\s*<(menuitem|act_window|data|odoo)',
        r'<!--\s*(t-if|t-foreach|t-esc|t-set|t-call)',
    ]

    # Markers that indicate intentionally commented code for removal
    # IMPORTANT: These patterns should match CODE DEPRECATION markers,
    # not functional descriptions like "# Remove oldest entries"
    DELETION_MARKERS = [
        # Task markers with deletion intent
        r'(?i)#\s*(TODO|FIXME|XXX|HACK)\s*:?\s*.*(delete|remove)\s*(this|code|file|method|function|class)',
        # Explicit deprecation/obsolete markers
        r'(?i)#\s*(DEPRECATED|OBSOLETE|DEAD\s*CODE)\s*[-:]',
        # Explicit removal markers (standalone, not part of description)
        r'(?i)#\s*(TO\s*BE\s*REMOVED|REMOVE\s*ME|DELETE\s*ME|MARKED\s*FOR\s*DELETION)',
        # Code moved/replaced markers
        r'(?i)#\s*(MOVED\s*TO|REPLACED\s*BY|MIGRATED\s*TO)',
        # Commented for testing/debugging (explicit markers)
        r'(?i)#\s*commented\s*(out|for|to)\s*(test|debug|review|deletion)',
        # File/function naming patterns indicating deprecation
        r'_old\b|_backup\b|_deprecated\b|_unused\b',
        # Phase/version-based deprecation with date
        r'(?i)#\s*(Phase\s*\d+|v\d+)\s*[-:]?\s*(DEPRECATED|removed|deleted)',
    ]

    # Words that commonly appear in functional comments but should NOT trigger deletion detection
    # These are descriptions of what the code does, not markers for deletion
    DELETION_MARKER_EXCLUSIONS = [
        r'(?i)remove\s*(from|older|expired|duplicate|trailing|spaces|whitespace)',
        r'(?i)delete\s*(from|older|expired|duplicate|all|record|data)',
        r'(?i)clean\s*up\s*(vendor|name|data|cache|old)',
        r'(?i)skip\s*(non|special|empty)',
    ]

    def __init__(self, base_path: str, module_filter: Optional[List[str]] = None):
        """
        Initialize the analyzer.

        :param base_path: Root directory to scan
        :param module_filter: Optional list of module names to include
        """
        self.base_path = Path(base_path)
        self.module_filter = module_filter or []
        self.findings = {
            'python': [],
            'javascript': [],
            'xml': [],
            'summary': {
                'total_files_scanned': 0,
                'files_with_commented_code': 0,
                'total_commented_blocks': 0,
                'python_blocks': 0,
                'javascript_blocks': 0,
                'xml_blocks': 0,
                'deletion_markers_found': 0,
            }
        }

    def analyze(self) -> Dict[str, Any]:
        """
        Run the commented code analysis.

        :return: Analysis results with findings
        """
        _logger.info(f"Starting commented code analysis of {self.base_path}")

        files_with_issues = set()

        # Scan Python files
        for py_file in self.base_path.rglob('*.py'):
            if self._should_scan(py_file):
                findings = self._analyze_python_file(py_file)
                if findings:
                    self.findings['python'].extend(findings)
                    files_with_issues.add(str(py_file))

        # Scan JavaScript files
        for js_file in self.base_path.rglob('*.js'):
            if self._should_scan(js_file):
                findings = self._analyze_javascript_file(js_file)
                if findings:
                    self.findings['javascript'].extend(findings)
                    files_with_issues.add(str(js_file))

        # Scan XML files
        for xml_file in self.base_path.rglob('*.xml'):
            if self._should_scan(xml_file):
                findings = self._analyze_xml_file(xml_file)
                if findings:
                    self.findings['xml'].extend(findings)
                    files_with_issues.add(str(xml_file))

        # Update summary
        self.findings['summary']['files_with_commented_code'] = len(files_with_issues)
        self.findings['summary']['python_blocks'] = len(self.findings['python'])
        self.findings['summary']['javascript_blocks'] = len(self.findings['javascript'])
        self.findings['summary']['xml_blocks'] = len(self.findings['xml'])
        self.findings['summary']['total_commented_blocks'] = (
            len(self.findings['python']) +
            len(self.findings['javascript']) +
            len(self.findings['xml'])
        )

        # Count deletion markers
        deletion_count = sum(
            1 for f in (self.findings['python'] + self.findings['javascript'] + self.findings['xml'])
            if f.get('has_deletion_marker')
        )
        self.findings['summary']['deletion_markers_found'] = deletion_count

        _logger.info(
            f"Commented code analysis complete: {self.findings['summary']['total_commented_blocks']} "
            f"blocks in {len(files_with_issues)} files"
        )

        return self.findings

    def _should_scan(self, file_path: Path) -> bool:
        """Check if file should be scanned based on filters"""
        # Skip common non-source directories
        path_str = str(file_path)
        if any(skip in path_str for skip in ['__pycache__', 'venv', '.git', 'node_modules', '.egg']):
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

    def _analyze_python_file(self, file_path: Path) -> List[Dict[str, Any]]:
        """
        Analyze a Python file for commented-out code.

        :param file_path: Path to Python file
        :return: List of findings
        """
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
        except Exception as e:
            _logger.warning(f"Could not read {file_path}: {e}")
            return []

        findings = []
        rel_path = str(file_path.relative_to(self.base_path))

        # Track consecutive commented lines
        block_start = None
        block_lines = []

        for i, line in enumerate(lines, 1):
            stripped = line.strip()

            # Check if line is a comment
            if stripped.startswith('#'):
                # Check if it looks like code
                is_code = any(re.match(pattern, line) for pattern in self.PYTHON_CODE_PATTERNS)

                if is_code:
                    if block_start is None:
                        block_start = i
                    block_lines.append((i, line.rstrip()))
                else:
                    # End current block if any
                    if block_lines:
                        finding = self._create_finding(
                            file_path, rel_path, block_start, block_lines, 'python'
                        )
                        if finding:
                            findings.append(finding)
                    block_start = None
                    block_lines = []
            else:
                # Non-comment line, end current block
                if block_lines:
                    finding = self._create_finding(
                        file_path, rel_path, block_start, block_lines, 'python'
                    )
                    if finding:
                        findings.append(finding)
                block_start = None
                block_lines = []

        # Handle block at end of file
        if block_lines:
            finding = self._create_finding(
                file_path, rel_path, block_start, block_lines, 'python'
            )
            if finding:
                findings.append(finding)

        # Also check for deletion markers in regular comments
        deletion_findings = self._find_deletion_markers(lines, file_path, rel_path, '#')
        findings.extend(deletion_findings)

        return findings

    def _analyze_javascript_file(self, file_path: Path) -> List[Dict[str, Any]]:
        """
        Analyze a JavaScript file for commented-out code.

        :param file_path: Path to JavaScript file
        :return: List of findings
        """
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                lines = content.split('\n')
        except Exception as e:
            _logger.warning(f"Could not read {file_path}: {e}")
            return []

        findings = []
        rel_path = str(file_path.relative_to(self.base_path))

        # Track consecutive commented lines
        block_start = None
        block_lines = []

        for i, line in enumerate(lines, 1):
            stripped = line.strip()

            # Check single-line comments
            if stripped.startswith('//'):
                is_code = any(re.match(pattern, line) for pattern in self.JS_CODE_PATTERNS)

                if is_code:
                    if block_start is None:
                        block_start = i
                    block_lines.append((i, line.rstrip()))
                else:
                    if block_lines:
                        finding = self._create_finding(
                            file_path, rel_path, block_start, block_lines, 'javascript'
                        )
                        if finding:
                            findings.append(finding)
                    block_start = None
                    block_lines = []
            else:
                if block_lines:
                    finding = self._create_finding(
                        file_path, rel_path, block_start, block_lines, 'javascript'
                    )
                    if finding:
                        findings.append(finding)
                block_start = None
                block_lines = []

        # Handle block at end of file
        if block_lines:
            finding = self._create_finding(
                file_path, rel_path, block_start, block_lines, 'javascript'
            )
            if finding:
                findings.append(finding)

        # Check for block comments with code
        block_comment_findings = self._find_js_block_comments_with_code(content, file_path, rel_path)
        findings.extend(block_comment_findings)

        # Check for deletion markers
        deletion_findings = self._find_deletion_markers(lines, file_path, rel_path, '//')
        findings.extend(deletion_findings)

        return findings

    def _analyze_xml_file(self, file_path: Path) -> List[Dict[str, Any]]:
        """
        Analyze an XML file for commented-out elements.

        :param file_path: Path to XML file
        :return: List of findings
        """
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        except Exception as e:
            _logger.warning(f"Could not read {file_path}: {e}")
            return []

        findings = []
        rel_path = str(file_path.relative_to(self.base_path))

        # Find XML comments
        comment_pattern = r'<!--([\s\S]*?)-->'

        for match in re.finditer(comment_pattern, content):
            comment_content = match.group(1)
            start_pos = match.start()

            # Calculate line number
            line_num = content[:start_pos].count('\n') + 1

            # Check if comment contains code-like patterns
            is_code = any(re.search(pattern, comment_content) for pattern in self.XML_CODE_PATTERNS)

            # Also check for actual XML elements in comment
            if not is_code:
                is_code = bool(re.search(r'<\w+[^>]*>', comment_content))

            if is_code:
                # Calculate end line
                end_line = line_num + comment_content.count('\n')

                # Check for deletion markers
                has_deletion = any(
                    re.search(marker, comment_content, re.IGNORECASE)
                    for marker in self.DELETION_MARKERS
                )

                # Get preview (first 100 chars)
                preview = comment_content.strip()[:100]
                if len(comment_content.strip()) > 100:
                    preview += '...'

                findings.append({
                    'file_path': str(file_path),
                    'relative_path': rel_path,
                    'line_start': line_num,
                    'line_end': end_line,
                    'code_type': 'xml',
                    'preview': preview,
                    'has_deletion_marker': has_deletion,
                    'severity': 'warning' if has_deletion else 'info',
                    'finding_type': 'commented_xml_element',
                })

        return findings

    def _create_finding(
        self,
        file_path: Path,
        rel_path: str,
        block_start: int,
        block_lines: List[Tuple[int, str]],
        code_type: str
    ) -> Optional[Dict[str, Any]]:
        """
        Create a finding record from a block of commented code.

        :param file_path: Absolute file path
        :param rel_path: Relative file path
        :param block_start: Starting line number
        :param block_lines: List of (line_num, line_content) tuples
        :param code_type: Type of code (python, javascript)
        :return: Finding dict or None if block is too small
        """
        # Skip single-line blocks unless they contain deletion markers
        if len(block_lines) < 2:
            full_text = block_lines[0][1] if block_lines else ''
            has_deletion = any(
                re.search(marker, full_text, re.IGNORECASE)
                for marker in self.DELETION_MARKERS
            )
            if not has_deletion:
                return None

        block_end = block_lines[-1][0]

        # Get preview (first 3 lines)
        preview_lines = [line for _, line in block_lines[:3]]
        preview = '\n'.join(preview_lines)
        if len(block_lines) > 3:
            preview += f'\n... ({len(block_lines) - 3} more lines)'

        # Check for deletion markers
        full_text = '\n'.join(line for _, line in block_lines)

        # First check if it's a functional description (excluded)
        is_excluded = any(
            re.search(exclusion, full_text, re.IGNORECASE)
            for exclusion in self.DELETION_MARKER_EXCLUSIONS
        )

        has_deletion = False
        if not is_excluded:
            has_deletion = any(
                re.search(marker, full_text, re.IGNORECASE)
                for marker in self.DELETION_MARKERS
            )

        return {
            'file_path': str(file_path),
            'relative_path': rel_path,
            'line_start': block_start,
            'line_end': block_end,
            'line_count': len(block_lines),
            'code_type': code_type,
            'preview': preview,
            'has_deletion_marker': has_deletion,
            'severity': 'warning' if has_deletion else 'info',
            'finding_type': f'commented_{code_type}_code',
        }

    def _find_deletion_markers(
        self,
        lines: List[str],
        file_path: Path,
        rel_path: str,
        comment_prefix: str
    ) -> List[Dict[str, Any]]:
        """
        Find comments with deletion markers that aren't already captured.

        :param lines: File lines
        :param file_path: Absolute file path
        :param rel_path: Relative file path
        :param comment_prefix: Comment prefix (# or //)
        :return: List of findings
        """
        findings = []

        for i, line in enumerate(lines, 1):
            stripped = line.strip()

            if stripped.startswith(comment_prefix):
                # First check for exclusions (functional descriptions)
                is_excluded = any(
                    re.search(exclusion, stripped, re.IGNORECASE)
                    for exclusion in self.DELETION_MARKER_EXCLUSIONS
                )

                if is_excluded:
                    continue  # Skip functional comments

                # Check for deletion markers
                for marker in self.DELETION_MARKERS:
                    if re.search(marker, stripped, re.IGNORECASE):
                        findings.append({
                            'file_path': str(file_path),
                            'relative_path': rel_path,
                            'line_start': i,
                            'line_end': i,
                            'line_count': 1,
                            'code_type': 'python' if comment_prefix == '#' else 'javascript',
                            'preview': stripped[:100] + ('...' if len(stripped) > 100 else ''),
                            'has_deletion_marker': True,
                            'severity': 'warning',
                            'finding_type': 'deletion_marker',
                        })
                        break  # Only add one finding per line

        return findings

    def _find_js_block_comments_with_code(
        self,
        content: str,
        file_path: Path,
        rel_path: str
    ) -> List[Dict[str, Any]]:
        """
        Find JavaScript block comments that contain code.

        :param content: File content
        :param file_path: Absolute file path
        :param rel_path: Relative file path
        :return: List of findings
        """
        findings = []

        # Match block comments /* ... */ or /** ... */
        block_pattern = r'/\*\*?([\s\S]*?)\*/'

        for match in re.finditer(block_pattern, content):
            comment_content = match.group(1)
            start_pos = match.start()

            # Calculate line number
            line_num = content[:start_pos].count('\n') + 1

            # Check if it looks like code
            code_patterns = [
                r'\b(function|class|const|let|var|return|if|else|for|while)\b',
                r'=>',
                r'this\.\w+',
                r'\w+\s*[=:]\s*\w+',
            ]

            is_code = any(re.search(pattern, comment_content) for pattern in code_patterns)

            # Skip JSDoc-style comments
            if is_code and not comment_content.strip().startswith('*'):
                end_line = line_num + comment_content.count('\n')

                preview = comment_content.strip()[:100]
                if len(comment_content.strip()) > 100:
                    preview += '...'

                has_deletion = any(
                    re.search(marker, comment_content, re.IGNORECASE)
                    for marker in self.DELETION_MARKERS
                )

                findings.append({
                    'file_path': str(file_path),
                    'relative_path': rel_path,
                    'line_start': line_num,
                    'line_end': end_line,
                    'code_type': 'javascript',
                    'preview': preview,
                    'has_deletion_marker': has_deletion,
                    'severity': 'warning' if has_deletion else 'info',
                    'finding_type': 'commented_js_block',
                })

        return findings

    def get_severity_counts(self) -> Dict[str, int]:
        """Get count of findings by severity"""
        counts = {'warning': 0, 'info': 0}

        for file_type in ['python', 'javascript', 'xml']:
            for finding in self.findings.get(file_type, []):
                severity = finding.get('severity', 'info')
                counts[severity] = counts.get(severity, 0) + 1

        return counts
