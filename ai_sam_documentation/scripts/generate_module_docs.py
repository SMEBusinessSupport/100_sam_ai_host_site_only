"""
Generate Module Documentation from SAM AI Core Modules

This script:
1. Scans 05-samai-core for modules with __manifest__.py
2. Creates folder in docs/03_modules/<module_name>/
3. Converts static/description/index.html → description.md
4. Scans models/ → generates schema.md

Run manually or integrate into build_courses.py
"""

import os
import re
import ast
import logging
from pathlib import Path
from html.parser import HTMLParser

_logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(message)s')


class HTMLTextExtractor(HTMLParser):
    """Extract text content from HTML, preserving some structure."""

    def __init__(self):
        super().__init__()
        self.result = []
        self.current_tag = None
        self.skip_tags = {'style', 'script', 'head'}
        self.in_skip = False

    def handle_starttag(self, tag, attrs):
        self.current_tag = tag
        if tag in self.skip_tags:
            self.in_skip = True
        elif tag == 'h1':
            self.result.append('\n# ')
        elif tag == 'h2':
            self.result.append('\n## ')
        elif tag == 'h3':
            self.result.append('\n### ')
        elif tag == 'li':
            self.result.append('\n- ')
        elif tag == 'p':
            self.result.append('\n\n')
        elif tag == 'br':
            self.result.append('\n')
        elif tag == 'strong' or tag == 'b':
            self.result.append('**')
        elif tag == 'em' or tag == 'i':
            self.result.append('*')
        elif tag == 'code':
            self.result.append('`')

    def handle_endtag(self, tag):
        if tag in self.skip_tags:
            self.in_skip = False
        elif tag == 'strong' or tag == 'b':
            self.result.append('**')
        elif tag == 'em' or tag == 'i':
            self.result.append('*')
        elif tag == 'code':
            self.result.append('`')
        self.current_tag = None

    def handle_data(self, data):
        if not self.in_skip:
            text = data.strip()
            if text:
                self.result.append(text + ' ')

    def get_text(self):
        return ''.join(self.result).strip()


def html_to_markdown(html_content):
    """Convert HTML to basic Markdown."""
    parser = HTMLTextExtractor()
    parser.feed(html_content)
    text = parser.get_text()

    # Clean up multiple newlines
    text = re.sub(r'\n{3,}', '\n\n', text)
    # Clean up spaces
    text = re.sub(r' +', ' ', text)

    return text


def parse_manifest(manifest_path):
    """Parse __manifest__.py and extract metadata."""
    try:
        with open(manifest_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Find the dictionary in the file
        tree = ast.parse(content)
        for node in ast.walk(tree):
            if isinstance(node, ast.Dict):
                # Convert AST dict to Python dict (simplified)
                manifest = {}
                for key, value in zip(node.keys, node.values):
                    if isinstance(key, ast.Constant):
                        key_str = key.value
                        if isinstance(value, ast.Constant):
                            manifest[key_str] = value.value
                        elif isinstance(value, ast.List):
                            manifest[key_str] = [
                                elt.value for elt in value.elts
                                if isinstance(elt, ast.Constant)
                            ]
                return manifest
    except Exception as e:
        _logger.warning(f"Could not parse manifest {manifest_path}: {e}")
    return {}


def extract_model_info(model_file):
    """Extract model name and fields from a Python model file."""
    try:
        with open(model_file, 'r', encoding='utf-8') as f:
            content = f.read()

        models = []

        # Find _name = '...' patterns
        name_matches = re.findall(r"_name\s*=\s*['\"]([^'\"]+)['\"]", content)
        desc_matches = re.findall(r"_description\s*=\s*['\"]([^'\"]+)['\"]", content)
        inherit_matches = re.findall(r"_inherit\s*=\s*['\"]([^'\"]+)['\"]", content)

        # Find field definitions
        field_pattern = r"(\w+)\s*=\s*fields\.(Char|Text|Html|Integer|Float|Boolean|Date|Datetime|Many2one|Many2many|One2many|Selection|Binary)"
        fields_found = re.findall(field_pattern, content)

        for i, name in enumerate(name_matches):
            model_info = {
                'name': name,
                'description': desc_matches[i] if i < len(desc_matches) else '',
                'fields': fields_found[:20] if fields_found else [],  # Limit to 20 fields
                'inherits': inherit_matches[i] if i < len(inherit_matches) else None
            }
            models.append(model_info)

        return models
    except Exception as e:
        _logger.warning(f"Could not parse model {model_file}: {e}")
    return []


def generate_description_md(module_path, module_name, manifest):
    """Generate description.md from index.html or manifest."""
    index_path = module_path / 'static' / 'description' / 'index.html'

    lines = [
        f"# {manifest.get('name', module_name)}",
        "",
        f"**Technical Name**: `{module_name}`",
        f"**Version**: {manifest.get('version', 'N/A')}",
        "",
    ]

    # Add summary if available
    if manifest.get('summary'):
        lines.extend([manifest['summary'], ""])

    # Add description from manifest
    if manifest.get('description'):
        lines.extend(["## Description", "", manifest['description'], ""])

    # Convert index.html if exists
    if index_path.exists():
        try:
            with open(index_path, 'r', encoding='utf-8') as f:
                html_content = f.read()

            md_content = html_to_markdown(html_content)
            if md_content:
                lines.extend([
                    "## Module Details",
                    "",
                    md_content,
                    ""
                ])
        except Exception as e:
            _logger.warning(f"Could not read index.html for {module_name}: {e}")

    # Add dependencies
    if manifest.get('depends'):
        lines.extend([
            "## Dependencies",
            "",
        ])
        for dep in manifest['depends']:
            lines.append(f"- `{dep}`")
        lines.append("")

    return '\n'.join(lines)


def generate_schema_md(module_path, module_name):
    """Generate schema.md from models/ folder."""
    models_path = module_path / 'models'

    if not models_path.exists():
        return None

    lines = [
        f"# {module_name} - Database Schema",
        "",
        "Auto-generated model documentation.",
        "",
    ]

    all_models = []

    # Scan all Python files in models/
    for py_file in models_path.glob('*.py'):
        if py_file.name == '__init__.py':
            continue

        models = extract_model_info(py_file)
        all_models.extend(models)

    if not all_models:
        return None

    lines.extend([
        f"## Models ({len(all_models)} total)",
        "",
    ])

    for model in all_models:
        lines.extend([
            f"### `{model['name']}`",
            "",
        ])

        if model.get('description'):
            lines.extend([f"_{model['description']}_", ""])

        if model.get('inherits'):
            lines.append(f"**Inherits**: `{model['inherits']}`\n")

        if model.get('fields'):
            lines.append("**Key Fields**:")
            for field_name, field_type in model['fields'][:10]:  # Limit to 10
                lines.append(f"- `{field_name}` ({field_type})")
            lines.append("")

    return '\n'.join(lines)


def generate_module_docs(source_dir, docs_dir):
    """Main function to generate all module documentation."""
    source_path = Path(source_dir)
    docs_path = Path(docs_dir) / '03_modules'

    _logger.info("=" * 60)
    _logger.info("Generating Module Documentation")
    _logger.info("=" * 60)
    _logger.info(f"Source: {source_path}")
    _logger.info(f"Output: {docs_path}")
    _logger.info("")

    stats = {'modules': 0, 'descriptions': 0, 'schemas': 0}

    # Find all modules (folders with __manifest__.py)
    for item in sorted(source_path.iterdir()):
        if not item.is_dir():
            continue

        manifest_path = item / '__manifest__.py'
        if not manifest_path.exists():
            continue

        module_name = item.name

        # Skip certain folders
        if module_name in ['backup', 'scripts', 'chroma_data', '__pycache__']:
            continue

        _logger.info(f"Processing: {module_name}")
        stats['modules'] += 1

        # Parse manifest
        manifest = parse_manifest(manifest_path)

        # Create module docs folder
        module_docs_path = docs_path / module_name
        module_docs_path.mkdir(parents=True, exist_ok=True)

        # Generate description.md
        description_content = generate_description_md(item, module_name, manifest)
        description_file = module_docs_path / 'description.md'
        with open(description_file, 'w', encoding='utf-8') as f:
            f.write(description_content)
        _logger.info(f"  ✓ description.md")
        stats['descriptions'] += 1

        # Generate schema.md (if models exist)
        schema_content = generate_schema_md(item, module_name)
        if schema_content:
            schema_file = module_docs_path / 'schema.md'
            with open(schema_file, 'w', encoding='utf-8') as f:
                f.write(schema_content)
            _logger.info(f"  ✓ schema.md")
            stats['schemas'] += 1

    _logger.info("")
    _logger.info("=" * 60)
    _logger.info(f"Complete!")
    _logger.info(f"  Modules processed: {stats['modules']}")
    _logger.info(f"  Descriptions: {stats['descriptions']}")
    _logger.info(f"  Schemas: {stats['schemas']}")
    _logger.info("=" * 60)


if __name__ == '__main__':
    # Default paths
    SOURCE_DIR = r"D:\SAMAI-18-SaaS\github-repos\05-samai-core"
    DOCS_DIR = r"D:\SAMAI-18-SaaS\github-repos\05-samai-core\ai_sam_documentation\docs"

    generate_module_docs(SOURCE_DIR, DOCS_DIR)
