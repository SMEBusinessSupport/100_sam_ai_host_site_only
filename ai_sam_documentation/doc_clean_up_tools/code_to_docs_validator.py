#!/usr/bin/env python3
"""
Code-to-Documentation Validator

Analyzes code in SAM AI modules and compares against documentation
to identify gaps, orphans, and coverage issues.

Usage:
    python code_to_docs_validator.py [--modules PATH] [--docs PATH] [--layers PATH]

Example:
    python code_to_docs_validator.py --modules "D:/SAMAI-18-SaaS/github-repos/05-samai-core" --docs "./docs"
"""

import os
import re
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, field
from typing import Dict, List, Set, Optional, Tuple
from collections import defaultdict

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')


@dataclass
class CodeElement:
    """Represents a discovered code element"""
    name: str
    element_type: str  # 'model', 'controller', 'method', 'class', 'file'
    file_path: str
    line_number: int
    layer: Optional[str] = None
    keywords: Set[str] = field(default_factory=set)


@dataclass
class DocReference:
    """Represents a documentation reference"""
    name: str
    file_path: str
    section: str
    keywords: Set[str] = field(default_factory=set)


@dataclass
class LayerDefinition:
    """Represents a layer from SYSTEM_LAYERS.md"""
    name: str
    number: int
    responsibility: str
    code_patterns: List[str] = field(default_factory=list)
    doc_sections: List[str] = field(default_factory=list)
    keywords: Set[str] = field(default_factory=set)


class CodeAnalyzer:
    """Analyzes Python code to extract structure"""

    # Patterns for Odoo models
    MODEL_PATTERN = re.compile(r'class\s+(\w+)\s*\([^)]*models\.(Model|TransientModel|AbstractModel)')
    CONTROLLER_PATTERN = re.compile(r'class\s+(\w+)\s*\([^)]*Controller')
    ROUTE_PATTERN = re.compile(r'@(?:http\.)?route\s*\(\s*[\'"]([^\'"]+)[\'"]')
    METHOD_PATTERN = re.compile(r'def\s+(\w+)\s*\(')
    FIELD_PATTERN = re.compile(r'(\w+)\s*=\s*fields\.(Char|Text|Integer|Float|Boolean|Many2one|One2many|Many2many|Selection|Date|Datetime|Binary|Html)')

    def __init__(self, modules_path: str):
        self.modules_path = Path(modules_path)
        self.elements: List[CodeElement] = []
        self.stats = {
            'models': 0,
            'controllers': 0,
            'routes': 0,
            'methods': 0,
            'files_scanned': 0
        }

    def scan(self) -> List[CodeElement]:
        """Scan all Python files in modules"""
        print(f"\n[CODE ANALYZER] Scanning: {self.modules_path}")

        # Find all SAM AI related modules
        sam_modules = [
            'ai_sam',
            'ai_sam_base',
            'ai_sam_intelligence',
            'ai_sam_workflows',
            'ai_sam_workflows_base',
            'sam_ai_page_builder'
        ]

        for module_name in sam_modules:
            module_path = self.modules_path / module_name
            if module_path.exists():
                self._scan_module(module_path, module_name)

        print(f"  Scanned {self.stats['files_scanned']} files")
        print(f"  Found: {self.stats['models']} models, {self.stats['controllers']} controllers, {self.stats['routes']} routes")

        return self.elements

    def _scan_module(self, module_path: Path, module_name: str):
        """Scan a single module"""
        for py_file in module_path.rglob('*.py'):
            # Skip __pycache__ and migrations
            if '__pycache__' in str(py_file) or 'migrations' in str(py_file):
                continue

            self.stats['files_scanned'] += 1
            self._analyze_file(py_file, module_name)

    def _analyze_file(self, file_path: Path, module_name: str):
        """Analyze a single Python file"""
        try:
            content = file_path.read_text(encoding='utf-8', errors='replace')
            lines = content.split('\n')

            for i, line in enumerate(lines, 1):
                # Find models
                model_match = self.MODEL_PATTERN.search(line)
                if model_match:
                    self.elements.append(CodeElement(
                        name=model_match.group(1),
                        element_type='model',
                        file_path=str(file_path),
                        line_number=i,
                        keywords=self._extract_keywords(model_match.group(1))
                    ))
                    self.stats['models'] += 1

                # Find controllers
                controller_match = self.CONTROLLER_PATTERN.search(line)
                if controller_match:
                    self.elements.append(CodeElement(
                        name=controller_match.group(1),
                        element_type='controller',
                        file_path=str(file_path),
                        line_number=i,
                        keywords=self._extract_keywords(controller_match.group(1))
                    ))
                    self.stats['controllers'] += 1

                # Find routes
                route_match = self.ROUTE_PATTERN.search(line)
                if route_match:
                    self.elements.append(CodeElement(
                        name=route_match.group(1),
                        element_type='route',
                        file_path=str(file_path),
                        line_number=i,
                        keywords=self._extract_keywords(route_match.group(1))
                    ))
                    self.stats['routes'] += 1

        except Exception as e:
            print(f"  Warning: Could not read {file_path}: {e}")

    def _extract_keywords(self, name: str) -> Set[str]:
        """Extract keywords from a name (split CamelCase and snake_case)"""
        # Split CamelCase
        words = re.sub('([A-Z])', r' \1', name).split()
        # Split snake_case
        words = [w for word in words for w in word.split('_')]
        # Lowercase and filter
        return {w.lower() for w in words if len(w) > 2}


class DocAnalyzer:
    """Analyzes documentation files"""

    HEADER_PATTERN = re.compile(r'^(#{1,4})\s+(.+)$', re.MULTILINE)
    CODE_REF_PATTERN = re.compile(r'`([A-Za-z_][A-Za-z0-9_]*)`')
    CLASS_REF_PATTERN = re.compile(r'\b([A-Z][a-z]+(?:[A-Z][a-z]+)+)\b')  # CamelCase

    def __init__(self, docs_path: str):
        self.docs_path = Path(docs_path)
        self.references: List[DocReference] = []
        self.stats = {
            'files_scanned': 0,
            'sections_found': 0,
            'references_found': 0
        }

    def scan(self) -> List[DocReference]:
        """Scan all markdown files in docs"""
        print(f"\n[DOC ANALYZER] Scanning: {self.docs_path}")

        for md_file in self.docs_path.rglob('*.md'):
            # Skip _README files and archive
            if md_file.name == '_README.md':
                continue
            if '_archive' in str(md_file):
                continue

            self.stats['files_scanned'] += 1
            self._analyze_file(md_file)

        print(f"  Scanned {self.stats['files_scanned']} files")
        print(f"  Found: {self.stats['sections_found']} sections, {self.stats['references_found']} code references")

        return self.references

    def _analyze_file(self, file_path: Path):
        """Analyze a single markdown file"""
        try:
            content = file_path.read_text(encoding='utf-8', errors='replace')

            # Find all headers
            current_section = file_path.stem
            for match in self.HEADER_PATTERN.finditer(content):
                level = len(match.group(1))
                title = match.group(2).strip()

                if level <= 2:
                    current_section = title
                    self.stats['sections_found'] += 1

            # Find code references
            for match in self.CODE_REF_PATTERN.finditer(content):
                ref_name = match.group(1)
                self.references.append(DocReference(
                    name=ref_name,
                    file_path=str(file_path),
                    section=current_section,
                    keywords=self._extract_keywords(ref_name)
                ))
                self.stats['references_found'] += 1

            # Find CamelCase class references
            for match in self.CLASS_REF_PATTERN.finditer(content):
                ref_name = match.group(1)
                # Avoid common words
                if ref_name not in ['CamelCase', 'JavaScript', 'Python', 'PostgreSQL']:
                    self.references.append(DocReference(
                        name=ref_name,
                        file_path=str(file_path),
                        section=current_section,
                        keywords=self._extract_keywords(ref_name)
                    ))

        except Exception as e:
            print(f"  Warning: Could not read {file_path}: {e}")

    def _extract_keywords(self, name: str) -> Set[str]:
        """Extract keywords from a name"""
        words = re.sub('([A-Z])', r' \1', name).split()
        words = [w for word in words for w in word.split('_')]
        return {w.lower() for w in words if len(w) > 2}


class LayerParser:
    """Parses SYSTEM_LAYERS.md to extract layer definitions"""

    def __init__(self, layers_path: str):
        self.layers_path = Path(layers_path)
        self.layers: Dict[str, LayerDefinition] = {}

    def parse(self) -> Dict[str, LayerDefinition]:
        """Parse the SYSTEM_LAYERS.md file"""
        if not self.layers_path.exists():
            print(f"[LAYER PARSER] Warning: {self.layers_path} not found")
            return self._default_layers()

        print(f"\n[LAYER PARSER] Parsing: {self.layers_path}")

        try:
            content = self.layers_path.read_text(encoding='utf-8')

            # Extract layer sections
            layer_pattern = re.compile(
                r'### LAYER (\d+): ([A-Z &]+)\n\*\*Responsibility:\*\* (.+?)(?=\n\n|\n###|\Z)',
                re.DOTALL
            )

            for match in layer_pattern.finditer(content):
                num = int(match.group(1))
                name = match.group(2).strip()
                responsibility = match.group(3).strip()

                # Extract keywords from layer name
                keywords = {w.lower() for w in name.split() if len(w) > 2}
                keywords.add(name.lower().replace(' ', '_'))

                self.layers[name] = LayerDefinition(
                    name=name,
                    number=num,
                    responsibility=responsibility,
                    keywords=keywords
                )

            print(f"  Found {len(self.layers)} layers")

        except Exception as e:
            print(f"  Error parsing layers: {e}")
            return self._default_layers()

        return self.layers

    def _default_layers(self) -> Dict[str, LayerDefinition]:
        """Return default layers if file not found"""
        return {
            'API MANAGEMENT': LayerDefinition('API MANAGEMENT', 1, 'External API interfaces', keywords={'api', 'provider', 'key'}),
            'LOCATION MANAGEMENT': LayerDefinition('LOCATION MANAGEMENT', 2, 'Context detection', keywords={'location', 'context', 'page'}),
            'DYNAMIC SYSTEM PROMPT CREATION': LayerDefinition('DYNAMIC SYSTEM PROMPT CREATION', 3, 'Prompt assembly', keywords={'prompt', 'mode', 'personality'}),
            'RESPONSE MANAGEMENT': LayerDefinition('RESPONSE MANAGEMENT', 4, 'Response handling', keywords={'response', 'stream', 'format'}),
            'SESSION & CONVERSATION': LayerDefinition('SESSION & CONVERSATION', 5, 'Conversation state', keywords={'session', 'message', 'history', 'conversation'}),
            'MEMORY & KNOWLEDGE': LayerDefinition('MEMORY & KNOWLEDGE', 6, 'Long-term memory', keywords={'memory', 'knowledge', 'vector', 'chroma'}),
            'AUTHENTICATION & SECURITY': LayerDefinition('AUTHENTICATION & SECURITY', 7, 'Access control', keywords={'auth', 'oauth', 'credential', 'security', 'permission'}),
            'UI & FRONTEND': LayerDefinition('UI & FRONTEND', 8, 'User interface', keywords={'ui', 'chat', 'bubble', 'css', 'component', 'frontend'}),
        }


class GapAnalyzer:
    """Compares code and docs to find gaps"""

    def __init__(self, code_elements: List[CodeElement], doc_references: List[DocReference], layers: Dict[str, LayerDefinition]):
        self.code_elements = code_elements
        self.doc_references = doc_references
        self.layers = layers
        self.results = {
            'documented': [],      # Code with matching docs
            'undocumented': [],    # Code with no docs
            'orphan_docs': [],     # Docs referencing non-existent code
            'layer_coverage': {},  # Coverage per layer
        }

    def analyze(self) -> dict:
        """Run the gap analysis"""
        print("\n[GAP ANALYZER] Comparing code to documentation...")

        # Create lookup sets
        doc_names = {ref.name.lower() for ref in self.doc_references}
        code_names = {elem.name.lower() for elem in self.code_elements}

        # Assign layers to code elements
        for elem in self.code_elements:
            elem.layer = self._assign_layer(elem)

        # Find documented vs undocumented code
        for elem in self.code_elements:
            if elem.name.lower() in doc_names:
                self.results['documented'].append(elem)
            else:
                self.results['undocumented'].append(elem)

        # Find orphan docs (reference things that don't exist)
        for ref in self.doc_references:
            if ref.name.lower() not in code_names:
                # Check if it's a common word or pattern
                if not self._is_common_word(ref.name):
                    self.results['orphan_docs'].append(ref)

        # Calculate layer coverage
        self._calculate_layer_coverage()

        return self.results

    def _assign_layer(self, elem: CodeElement) -> str:
        """Assign a code element to a layer based on keywords and path"""
        best_layer = 'UNKNOWN'
        best_score = 0

        # Extract keywords from path
        path_keywords = set()
        path_parts = elem.file_path.lower().replace('\\', '/').split('/')
        for part in path_parts:
            path_keywords.update(part.replace('.py', '').replace('_', ' ').split())

        all_keywords = elem.keywords | path_keywords

        for layer_name, layer in self.layers.items():
            score = len(all_keywords & layer.keywords)
            if score > best_score:
                best_score = score
                best_layer = layer_name

        return best_layer

    def _is_common_word(self, name: str) -> bool:
        """Check if a name is a common word (not actual code)"""
        common = {'self', 'true', 'false', 'none', 'name', 'type', 'value', 'data', 'result', 'error'}
        return name.lower() in common

    def _calculate_layer_coverage(self):
        """Calculate documentation coverage per layer"""
        layer_counts = defaultdict(lambda: {'total': 0, 'documented': 0})

        for elem in self.code_elements:
            layer = elem.layer or 'UNKNOWN'
            layer_counts[layer]['total'] += 1
            if elem in self.results['documented']:
                layer_counts[layer]['documented'] += 1

        for layer_name in self.layers.keys():
            counts = layer_counts.get(layer_name, {'total': 0, 'documented': 0})
            if counts['total'] > 0:
                coverage = (counts['documented'] / counts['total']) * 100
            else:
                coverage = 0

            self.results['layer_coverage'][layer_name] = {
                'total': counts['total'],
                'documented': counts['documented'],
                'coverage_pct': round(coverage, 1)
            }


class ReportGenerator:
    """Generates the validation report"""

    def __init__(self, results: dict, layers: Dict[str, LayerDefinition], output_path: str):
        self.results = results
        self.layers = layers
        self.output_path = Path(output_path)

    def generate(self):
        """Generate markdown and JSON reports"""
        timestamp = datetime.now().strftime('%Y-%m-%d_%H%M%S')

        # Markdown report
        md_path = self.output_path / f'validation_report_{timestamp}.md'
        self._write_markdown_report(md_path)

        # JSON report (for programmatic use)
        json_path = self.output_path / f'validation_report_{timestamp}.json'
        self._write_json_report(json_path)

        print(f"\n[REPORT] Generated:")
        print(f"  Markdown: {md_path}")
        print(f"  JSON: {json_path}")

        return md_path, json_path

    def _write_markdown_report(self, path: Path):
        """Write the markdown report"""
        lines = [
            "# Code-to-Documentation Validation Report",
            f"\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "\n---\n",
            "## Summary\n",
            f"| Metric | Count |",
            f"|--------|-------|",
            f"| Total Code Elements | {len(self.results['documented']) + len(self.results['undocumented'])} |",
            f"| Documented | {len(self.results['documented'])} |",
            f"| **Undocumented** | **{len(self.results['undocumented'])}** |",
            f"| Orphan Doc References | {len(self.results['orphan_docs'])} |",
            "\n---\n",
            "## Layer Coverage\n",
            "| Layer | Total | Documented | Coverage |",
            "|-------|-------|------------|----------|",
        ]

        for layer_name in sorted(self.layers.keys(), key=lambda x: self.layers[x].number):
            cov = self.results['layer_coverage'].get(layer_name, {'total': 0, 'documented': 0, 'coverage_pct': 0})
            status = "✅" if cov['coverage_pct'] >= 70 else "⚠️" if cov['coverage_pct'] >= 30 else "❌"
            lines.append(f"| {layer_name} | {cov['total']} | {cov['documented']} | {status} {cov['coverage_pct']}% |")

        lines.extend([
            "\n---\n",
            "## Undocumented Code (Priority Gaps)\n",
        ])

        # Group undocumented by layer
        by_layer = defaultdict(list)
        for elem in self.results['undocumented']:
            by_layer[elem.layer].append(elem)

        for layer_name in sorted(by_layer.keys()):
            lines.append(f"\n### {layer_name}\n")
            for elem in by_layer[layer_name][:10]:  # Limit to 10 per layer
                rel_path = elem.file_path.split('05-samai-core')[-1] if '05-samai-core' in elem.file_path else elem.file_path
                lines.append(f"- `{elem.name}` ({elem.element_type}) - {rel_path}:{elem.line_number}")
            if len(by_layer[layer_name]) > 10:
                lines.append(f"- ... and {len(by_layer[layer_name]) - 10} more")

        lines.extend([
            "\n---\n",
            "## Orphan Documentation References\n",
            "These are referenced in docs but may not exist in code:\n",
        ])

        for ref in self.results['orphan_docs'][:20]:
            rel_path = ref.file_path.split('docs')[-1] if 'docs' in ref.file_path else ref.file_path
            lines.append(f"- `{ref.name}` in {rel_path}")

        if len(self.results['orphan_docs']) > 20:
            lines.append(f"\n... and {len(self.results['orphan_docs']) - 20} more")

        lines.extend([
            "\n---\n",
            "## Recommendations\n",
            "1. Focus on layers with <30% coverage first",
            "2. Document models and controllers before methods",
            "3. Review orphan references - may indicate outdated docs",
            "4. Re-run this validator after documentation updates",
        ])

        path.write_text('\n'.join(lines), encoding='utf-8')

    def _write_json_report(self, path: Path):
        """Write the JSON report"""
        data = {
            'generated': datetime.now().isoformat(),
            'summary': {
                'total_code_elements': len(self.results['documented']) + len(self.results['undocumented']),
                'documented': len(self.results['documented']),
                'undocumented': len(self.results['undocumented']),
                'orphan_references': len(self.results['orphan_docs']),
            },
            'layer_coverage': self.results['layer_coverage'],
            'undocumented': [
                {'name': e.name, 'type': e.element_type, 'layer': e.layer, 'file': e.file_path, 'line': e.line_number}
                for e in self.results['undocumented']
            ],
            'orphan_docs': [
                {'name': r.name, 'file': r.file_path, 'section': r.section}
                for r in self.results['orphan_docs']
            ]
        }

        path.write_text(json.dumps(data, indent=2), encoding='utf-8')


def main():
    parser = argparse.ArgumentParser(description='Code-to-Documentation Validator')
    parser.add_argument('--modules', default='D:/SAMAI-18-SaaS/github-repos/05-samai-core',
                        help='Path to modules directory')
    parser.add_argument('--docs', default='D:/SAMAI-18-SaaS/github-repos/05-samai-core/ai_sam_documentation/docs',
                        help='Path to docs directory')
    parser.add_argument('--layers', default='D:/SAMAI-18-SaaS/github-repos/05-samai-core/ai_sam_documentation/docs/05_architecture/SYSTEM_LAYERS.md',
                        help='Path to SYSTEM_LAYERS.md')
    parser.add_argument('--output', default='D:/SAMAI-18-SaaS/github-repos/05-samai-core/ai_sam_documentation/doc_clean_up_tools',
                        help='Output directory for reports')

    args = parser.parse_args()

    print("=" * 60)
    print("CODE-TO-DOCUMENTATION VALIDATOR")
    print("=" * 60)

    # Step 1: Parse layer definitions
    layer_parser = LayerParser(args.layers)
    layers = layer_parser.parse()

    # Step 2: Analyze code
    code_analyzer = CodeAnalyzer(args.modules)
    code_elements = code_analyzer.scan()

    # Step 3: Analyze docs
    doc_analyzer = DocAnalyzer(args.docs)
    doc_references = doc_analyzer.scan()

    # Step 4: Gap analysis
    gap_analyzer = GapAnalyzer(code_elements, doc_references, layers)
    results = gap_analyzer.analyze()

    # Step 5: Generate report
    report_gen = ReportGenerator(results, layers, args.output)
    md_path, json_path = report_gen.generate()

    # Summary
    print("\n" + "=" * 60)
    print("VALIDATION COMPLETE")
    print("=" * 60)

    total = len(results['documented']) + len(results['undocumented'])
    if total > 0:
        doc_pct = (len(results['documented']) / total) * 100
    else:
        doc_pct = 0

    print(f"\nOverall Documentation Coverage: {doc_pct:.1f}%")
    print(f"Undocumented Elements: {len(results['undocumented'])}")
    print(f"Orphan References: {len(results['orphan_docs'])}")

    print("\nLayer Coverage:")
    for layer_name in sorted(layers.keys(), key=lambda x: layers[x].number):
        cov = results['layer_coverage'].get(layer_name, {'coverage_pct': 0})
        bar = "█" * int(cov['coverage_pct'] / 10) + "░" * (10 - int(cov['coverage_pct'] / 10))
        print(f"  {layer_name[:30]:<30} [{bar}] {cov['coverage_pct']}%")


if __name__ == '__main__':
    main()
