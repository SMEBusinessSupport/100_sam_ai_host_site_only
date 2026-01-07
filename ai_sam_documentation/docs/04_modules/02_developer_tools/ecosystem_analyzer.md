# Ecosystem Analyzer

**Original file:** `ecosystem_analyzer.py`
**Type:** PYTHON

---

```python
#!/usr/bin/env python3
"""
SAM AI Ecosystem Analyzer
==========================
Comprehensive analysis tool that measures:
1. Odoo modules (module count, lines of code per module, total LOC)
2. Claude agents (agent count, word count per agent, total words)
3. Commented/redundant code detection (cleanup candidates)

Output: Markdown report saved to reports/ directory

Author: SAM AI Team
Created: 2025-10-13
"""

import os
import re
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Set
from collections import defaultdict


class EcosystemAnalyzer:
    """Analyzes SAM AI Odoo modules and Claude agents ecosystem"""

    # File extensions to analyze for code
    CODE_EXTENSIONS = {
        '.py', '.xml', '.js', '.css', '.scss', '.html',
        '.json', '.yml', '.yaml', '.sql', '.sh', '.bat'
    }

    # Directories to exclude from analysis
    EXCLUDE_DIRS = {
        '__pycache__', '.git', '.pytest_cache', 'node_modules',
        '.vscode', '.idea', '__init__.pyc', 'reports'
    }

    # Agent shared files (to avoid double counting)
    AGENT_SHARED_FILES = {
        'AGENT_STARTUP_PROTOCOL.md',
        'README.md',
        'CHANGELOG.md'
    }

    def __init__(self, odoo_path: str, agent_path: str, output_path: str):
        """
        Initialize analyzer

        Args:
            odoo_path: Path to Odoo modules (e.g., C:/Working With AI/ai_sam/ai_sam/)
            agent_path: Path to Claude agents (e.g., C:/Users/total/.claude/agents/)
            output_path: Path to save reports (e.g., C:/Working With AI/ai_sam/ai_toolbox/reports/)
        """
        self.odoo_path = Path(odoo_path)
        self.agent_path = Path(agent_path)
        self.output_path = Path(output_path)
        self.output_path.mkdir(exist_ok=True)

        # Results storage
        self.module_stats = {}
        self.agent_stats = {}
        self.commented_code_report = []

    def analyze_all(self) -> Dict:
        """Run complete ecosystem analysis"""
        print("[ROCKET] SAM AI Ecosystem Analyzer Starting...")
        print("=" * 70)

        # Analyze Odoo modules
        print("\n[PACKAGE] Analyzing Odoo Modules...")
        self.analyze_odoo_modules()

        # Analyze Claude agents
        print("\n[ROBOT] Analyzing Claude Agents...")
        self.analyze_agents()

        # Generate report
        print("\n[DOCUMENT] Generating Report...")
        report_path = self.generate_markdown_report()

        print(f"\n[CHECK] Analysis Complete!")
        print(f"[FILE] Report saved to: {report_path}")

        return {
            'modules': self.module_stats,
            'agents': self.agent_stats,
            'commented_code': self.commented_code_report
        }

    def analyze_odoo_modules(self):
        """Analyze all Odoo modules in ecosystem"""
        total_modules = 0
        total_lines = 0
        total_files = 0

        # Find all modules (directories with __manifest__.py)
        for item in self.odoo_path.iterdir():
            if not item.is_dir():
                continue

            manifest_path = item / '__manifest__.py'
            if not manifest_path.exists():
                continue

            # Found a module!
            total_modules += 1
            module_name = item.name

            print(f"  [FOLDER] Scanning {module_name}...")

            # Analyze module
            stats = self._analyze_module(item)
            self.module_stats[module_name] = stats

            total_lines += stats['total_lines']
            total_files += stats['total_files']

        # Add summary
        self.module_stats['_SUMMARY'] = {
            'total_modules': total_modules,
            'total_lines': total_lines,
            'total_files': total_files
        }

        print(f"\n  [CHECK] Found {total_modules} modules")
        print(f"  [CHART] Total lines: {total_lines:,}")
        print(f"  [FILES] Total files: {total_files:,}")

    def _analyze_module(self, module_path: Path) -> Dict:
        """Analyze single Odoo module"""
        stats = {
            'total_lines': 0,
            'total_files': 0,
            'files_by_type': defaultdict(int),
            'lines_by_type': defaultdict(int),
            'commented_lines': 0,
            'blank_lines': 0,
            'code_lines': 0,
            'commented_blocks': []
        }

        # Walk through module directory
        for root, dirs, files in os.walk(module_path):
            # Skip excluded directories
            dirs[:] = [d for d in dirs if d not in self.EXCLUDE_DIRS]

            for file in files:
                file_path = Path(root) / file
                ext = file_path.suffix.lower()

                # Only analyze code files
                if ext not in self.CODE_EXTENSIONS:
                    continue

                stats['total_files'] += 1
                stats['files_by_type'][ext] += 1

                # Analyze file content
                file_stats = self._analyze_file(file_path)

                stats['total_lines'] += file_stats['total_lines']
                stats['lines_by_type'][ext] += file_stats['total_lines']
                stats['commented_lines'] += file_stats['commented_lines']
                stats['blank_lines'] += file_stats['blank_lines']
                stats['code_lines'] += file_stats['code_lines']

                # Store commented blocks for cleanup report
                if file_stats['commented_blocks']:
                    stats['commented_blocks'].extend(file_stats['commented_blocks'])

        return stats

    def _analyze_file(self, file_path: Path) -> Dict:
        """Analyze single file for lines of code and comments"""
        stats = {
            'total_lines': 0,
            'commented_lines': 0,
            'blank_lines': 0,
            'code_lines': 0,
            'commented_blocks': []
        }

        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
                stats['total_lines'] = len(lines)

                in_multiline_comment = False
                comment_block_start = None
                comment_block_lines = []

                for i, line in enumerate(lines, 1):
                    stripped = line.strip()

                    # Blank line
                    if not stripped:
                        stats['blank_lines'] += 1
                        continue

                    # Python/JS multiline comment detection
                    if file_path.suffix in ['.py', '.js']:
                        # Start of multiline comment
                        if '"""' in stripped or "'''" in stripped or '/*' in stripped:
                            if not in_multiline_comment:
                                in_multiline_comment = True
                                comment_block_start = i
                                comment_block_lines = [line]
                            else:
                                # End of multiline comment
                                in_multiline_comment = False
                                comment_block_lines.append(line)

                                # Check if this looks like commented-out code (not docs)
                                if self._is_commented_code_block(comment_block_lines):
                                    stats['commented_blocks'].append({
                                        'file': str(file_path),
                                        'start_line': comment_block_start,
                                        'end_line': i,
                                        'lines': len(comment_block_lines),
                                        'preview': ''.join(comment_block_lines[:3])
                                    })

                                comment_block_lines = []

                            stats['commented_lines'] += 1
                            continue

                        if in_multiline_comment:
                            stats['commented_lines'] += 1
                            comment_block_lines.append(line)
                            continue

                    # Single line comments
                    if file_path.suffix == '.py' and stripped.startswith('#'):
                        stats['commented_lines'] += 1

                        # Check if it's commented-out code
                        if self._is_commented_code_line(stripped):
                            stats['commented_blocks'].append({
                                'file': str(file_path),
                                'start_line': i,
                                'end_line': i,
                                'lines': 1,
                                'preview': line.strip()
                            })
                        continue

                    if file_path.suffix in ['.js', '.css'] and (stripped.startswith('//') or stripped.startswith('*')):
                        stats['commented_lines'] += 1
                        continue

                    if file_path.suffix == '.xml' and '<!--' in stripped:
                        stats['commented_lines'] += 1
                        continue

                    # Otherwise it's code
                    stats['code_lines'] += 1

        except Exception as e:
            print(f"    [WARNING] Error reading {file_path}: {e}")

        return stats

    def _is_commented_code_line(self, line: str) -> bool:
        """Detect if commented line is likely code (not documentation)"""
        # Remove comment marker
        content = line.lstrip('#').strip()

        # Code indicators
        code_patterns = [
            r'^\s*def\s+\w+',           # def function_name
            r'^\s*class\s+\w+',         # class ClassName
            r'^\s*import\s+\w+',        # import module
            r'^\s*from\s+\w+',          # from module
            r'^\s*if\s+.+:',            # if condition:
            r'^\s*for\s+.+:',           # for loop:
            r'^\s*while\s+.+:',         # while loop:
            r'^\s*return\s+',           # return statement
            r'^\s*\w+\s*=\s*',          # variable assignment
            r'^\s*\w+\(.*\)',           # function call
            r'^\s*print\(',             # print statement
        ]

        for pattern in code_patterns:
            if re.match(pattern, content):
                return True

        return False

    def _is_commented_code_block(self, lines: List[str]) -> bool:
        """Detect if multiline comment block is likely code (not docstring)"""
        # Join lines and check for code patterns
        content = ''.join(lines)

        # If it starts like a docstring, it's probably documentation
        if lines[0].strip().startswith('"""') and 'Args:' in content or 'Returns:' in content:
            return False

        # Count code-like patterns
        code_indicators = 0
        for line in lines:
            if re.search(r'(def|class|import|from|if|for|while|return)\s+', line):
                code_indicators += 1

        # If more than 30% of lines look like code, flag it
        return code_indicators > len(lines) * 0.3

    def analyze_agents(self):
        """Analyze all Claude agents"""
        total_agents = 0
        total_words = 0
        total_files = 0

        # Track shared files (only count once)
        shared_files_processed = set()

        # Find all agent directories
        for item in self.agent_path.iterdir():
            if not item.is_dir():
                continue

            # Found an agent!
            total_agents += 1
            agent_name = item.name

            print(f"  [AGENT] Scanning {agent_name}...")

            # Analyze agent
            stats = self._analyze_agent(item, shared_files_processed)
            self.agent_stats[agent_name] = stats

            total_words += stats['total_words']
            total_files += stats['total_files']

        # Add summary
        self.agent_stats['_SUMMARY'] = {
            'total_agents': total_agents,
            'total_words': total_words,
            'total_files': total_files,
            'shared_files_count': len(shared_files_processed)
        }

        print(f"\n  [CHECK] Found {total_agents} agents")
        print(f"  [CHART] Total words: {total_words:,}")
        print(f"  [FILES] Total files: {total_files:,}")

    def _analyze_agent(self, agent_path: Path, shared_files_processed: Set[str]) -> Dict:
        """Analyze single Claude agent"""
        stats = {
            'total_words': 0,
            'total_files': 0,
            'files': [],
            'shared_files': [],
            'unique_files': []
        }

        # Find all markdown files in agent directory
        for file_path in agent_path.glob('*.md'):
            file_name = file_path.name

            # Check if this is a shared file
            is_shared = file_name in self.AGENT_SHARED_FILES

            # Only count shared files once
            if is_shared and file_name in shared_files_processed:
                stats['shared_files'].append({
                    'name': file_name,
                    'counted': False
                })
                continue

            # Analyze file
            word_count = self._count_words(file_path)

            file_info = {
                'name': file_name,
                'words': word_count,
                'is_shared': is_shared
            }

            stats['files'].append(file_info)
            stats['total_files'] += 1
            stats['total_words'] += word_count

            if is_shared:
                shared_files_processed.add(file_name)
                stats['shared_files'].append(file_info)
            else:
                stats['unique_files'].append(file_info)

        return stats

    def _count_words(self, file_path: Path) -> int:
        """Count words in markdown file (including code blocks)"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

                # Split on whitespace and count
                words = content.split()
                return len(words)

        except Exception as e:
            print(f"    [WARNING] Error reading {file_path}: {e}")
            return 0

    def generate_markdown_report(self) -> str:
        """Generate comprehensive markdown report"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_path = self.output_path / f'ecosystem_analysis_{timestamp}.md'

        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(self._generate_report_content())

        # Also save JSON version for programmatic access
        json_path = self.output_path / f'ecosystem_analysis_{timestamp}.json'
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump({
                'modules': self.module_stats,
                'agents': self.agent_stats,
                'commented_code': self.commented_code_report,
                'timestamp': timestamp
            }, f, indent=2)

        return report_path

    def _generate_report_content(self) -> str:
        """Generate markdown report content"""
        module_summary = self.module_stats.get('_SUMMARY', {})
        agent_summary = self.agent_stats.get('_SUMMARY', {})

        report = f"""# SAM AI Ecosystem Analysis Report

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## 📊 Executive Summary

### Odoo Modules
- **Total Modules:** {module_summary.get('total_modules', 0)}
- **Total Lines of Code:** {module_summary.get('total_lines', 0):,}
- **Total Files:** {module_summary.get('total_files', 0):,}

### Claude Agents
- **Total Agents:** {agent_summary.get('total_agents', 0)}
- **Total Words:** {agent_summary.get('total_words', 0):,}
- **Total Knowledge Files:** {agent_summary.get('total_files', 0):,}
- **Shared Files:** {agent_summary.get('shared_files_count', 0)}

---

## 📦 Odoo Module Analysis

### Module Breakdown

"""

        # Module details
        for module_name, stats in sorted(self.module_stats.items()):
            if module_name == '_SUMMARY':
                continue

            report += f"""#### {module_name}
- **Total Lines:** {stats['total_lines']:,}
- **Total Files:** {stats['total_files']:,}
- **Code Lines:** {stats['code_lines']:,}
- **Commented Lines:** {stats['commented_lines']:,}
- **Blank Lines:** {stats['blank_lines']:,}
- **Commented Code Blocks:** {len(stats['commented_blocks'])}

**Files by Type:**
"""

            for ext, count in sorted(stats['files_by_type'].items()):
                report += f"- `{ext}`: {count} files, {stats['lines_by_type'][ext]:,} lines\n"

            report += "\n"

        # Agent details
        report += """---

## 🤖 Claude Agent Analysis

### Agent Breakdown

"""

        for agent_name, stats in sorted(self.agent_stats.items()):
            if agent_name == '_SUMMARY':
                continue

            report += f"""#### {agent_name}
- **Total Words:** {stats['total_words']:,}
- **Total Files:** {stats['total_files']:,}
- **Unique Files:** {len(stats['unique_files'])}
- **Shared Files:** {len(stats['shared_files'])}

**Knowledge Files:**
"""

            for file_info in stats['files']:
                shared_marker = " *(shared)*" if file_info['is_shared'] else ""
                report += f"- `{file_info['name']}`: {file_info['words']:,} words{shared_marker}\n"

            report += "\n"

        # Commented code report
        report += """---

## 🧹 Cleanup Candidates (Commented/Redundant Code)

"""

        # Collect all commented blocks from all modules
        all_commented_blocks = []
        for module_name, stats in self.module_stats.items():
            if module_name == '_SUMMARY':
                continue

            for block in stats['commented_blocks']:
                all_commented_blocks.append({
                    'module': module_name,
                    **block
                })

        if all_commented_blocks:
            report += f"**Total Commented Code Blocks Found:** {len(all_commented_blocks)}\n\n"

            # Group by module
            blocks_by_module = defaultdict(list)
            for block in all_commented_blocks:
                blocks_by_module[block['module']].append(block)

            for module_name, blocks in sorted(blocks_by_module.items()):
                report += f"### {module_name} ({len(blocks)} blocks)\n\n"

                for block in blocks:
                    file_path = Path(block['file']).name
                    report += f"""**{file_path}** (Lines {block['start_line']}-{block['end_line']})
```
{block['preview']}
```

"""
        else:
            report += "✅ No commented-out code blocks detected!\n\n"

        report += """---

## 📈 Statistics Summary

### Code Distribution by File Type

"""

        # Aggregate file types across all modules
        total_by_type = defaultdict(lambda: {'files': 0, 'lines': 0})

        for module_name, stats in self.module_stats.items():
            if module_name == '_SUMMARY':
                continue

            for ext, count in stats['files_by_type'].items():
                total_by_type[ext]['files'] += count
                total_by_type[ext]['lines'] += stats['lines_by_type'][ext]

        for ext, data in sorted(total_by_type.items(), key=lambda x: x[1]['lines'], reverse=True):
            report += f"- **{ext}**: {data['files']} files, {data['lines']:,} lines\n"

        report += f"""

---

## 🎯 Key Insights

### Codebase Health
- **Code Density:** {(module_summary.get('total_lines', 1) / module_summary.get('total_files', 1)):.1f} lines per file (average)
- **Comment Ratio:** {(sum(s['commented_lines'] for s in self.module_stats.values() if isinstance(s, dict) and 'commented_lines' in s) / module_summary.get('total_lines', 1) * 100):.1f}% of lines are comments
- **Cleanup Opportunity:** {len(all_commented_blocks)} commented code blocks identified for review

### Agent Knowledge Base
- **Knowledge Density:** {(agent_summary.get('total_words', 1) / agent_summary.get('total_files', 1)):.0f} words per file (average)
- **Total Knowledge:** {agent_summary.get('total_words', 0):,} words of specialized agent instructions
- **Agents per Module:** {(agent_summary.get('total_agents', 1) / module_summary.get('total_modules', 1)):.2f} (agent-to-module ratio)

---

**Report Generated by SAM AI Ecosystem Analyzer**
**Tool Location:** `C:\\Working With AI\\ai_sam\\ai_toolbox\\ecosystem_analyzer.py`

"""

        return report


def main():
    """Main entry point"""
    # Configuration
    ODOO_PATH = r"C:\Working With AI\ai_sam\ai_sam"
    AGENT_PATH = r"C:\Users\total\.claude\agents"
    OUTPUT_PATH = r"C:\Working With AI\ai_sam\ai_toolbox\reports"

    # Run analysis
    analyzer = EcosystemAnalyzer(ODOO_PATH, AGENT_PATH, OUTPUT_PATH)
    results = analyzer.analyze_all()

    print("\n" + "=" * 70)
    print("[SPARKLES] Analysis complete! Check the reports directory for full details.")
    print("=" * 70)


if __name__ == '__main__':
    main()

```
