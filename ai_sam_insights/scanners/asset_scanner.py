# -*- coding: utf-8 -*-
"""
Asset Scanner for SAM AI Insights

Scans JavaScript and CSS files to extract:
- OWL components and their dependencies
- JS module definitions (@odoo-module)
- Function definitions and exports
- CSS class definitions
- Asset bundle registrations from manifests
- Orphaned assets not in any bundle
"""
import os
import re
import hashlib
from pathlib import Path
from typing import Dict, List, Any, Optional, Set, Tuple
import logging

_logger = logging.getLogger(__name__)


class AssetScanner:
    """Scanner for JavaScript and CSS assets"""

    # Regex patterns for JS analysis
    PATTERNS = {
        # OWL component definition
        'owl_component': re.compile(
            r'class\s+(\w+)\s+extends\s+(?:owl\.)?Component',
            re.MULTILINE
        ),
        # @odoo-module annotation
        'odoo_module': re.compile(
            r'@odoo-module\s*(?:alias=([^\s*]+))?',
            re.MULTILINE
        ),
        # ES6 imports
        'es6_import': re.compile(
            r'import\s+(?:{([^}]+)}|(\w+))\s+from\s+["\']([^"\']+)["\']',
            re.MULTILINE
        ),
        # Function definitions
        'function_def': re.compile(
            r'(?:async\s+)?function\s+(\w+)\s*\(',
            re.MULTILINE
        ),
        # Arrow function assignments
        'arrow_function': re.compile(
            r'(?:const|let|var)\s+(\w+)\s*=\s*(?:async\s*)?\([^)]*\)\s*=>',
            re.MULTILINE
        ),
        # Method definitions in classes/objects
        'method_def': re.compile(
            r'^\s*(?:async\s+)?(\w+)\s*\([^)]*\)\s*{',
            re.MULTILINE
        ),
        # Export statements
        'export': re.compile(
            r'export\s+(?:default\s+)?(?:class|function|const|let|var)?\s*(\w+)?',
            re.MULTILINE
        ),
        # Registry additions (Odoo pattern)
        'registry_add': re.compile(
            r'registry\.(?:category\(["\']([^"\']+)["\']\)\.)?add\(["\']([^"\']+)["\']',
            re.MULTILINE
        ),
        # patch() calls for monkey patching
        'patch_call': re.compile(
            r'patch\(\s*([^,]+),',
            re.MULTILINE
        ),
        # CSS class definitions
        'css_class': re.compile(
            r'\.([a-zA-Z_][\w-]*)\s*(?:\{|,|\s+\.)',
            re.MULTILINE
        ),
        # CSS ID definitions
        'css_id': re.compile(
            r'#([a-zA-Z_][\w-]*)\s*(?:\{|,|\s+[.#])',
            re.MULTILINE
        ),
        # SCSS variables
        'scss_variable': re.compile(
            r'\$([a-zA-Z_][\w-]*)\s*:',
            re.MULTILINE
        ),
        # CSS custom properties
        'css_variable': re.compile(
            r'--([a-zA-Z_][\w-]*)\s*:',
            re.MULTILINE
        ),
    }

    def __init__(self, base_path: str, module_filter: Optional[List[str]] = None):
        self.base_path = Path(base_path)
        self.module_filter = module_filter or []
        self.scan_results = {
            'js_files': [],
            'css_files': [],
            'owl_components': [],
            'js_functions': [],
            'js_exports': [],
            'registry_additions': [],
            'patches': [],
            'css_classes': [],
            'css_variables': [],
            'asset_bundles': {},
            'orphaned_assets': [],
            'files_scanned': 0,
            'errors': [],
        }
        # Track assets registered in manifests
        self._registered_assets = set()

    def scan(self) -> Dict[str, Any]:
        """Scan all JS and CSS files"""
        _logger.info(f"Starting asset scan of {self.base_path}")

        # First, scan manifests to find registered assets
        self._scan_manifests()

        # Then scan actual asset files
        for file_path in self.base_path.rglob('*'):
            if file_path.suffix in ('.js', '.mjs'):
                self._scan_js_file(file_path)
            elif file_path.suffix in ('.css', '.scss', '.sass', '.less'):
                self._scan_css_file(file_path)

        # Find orphaned assets
        self._find_orphaned_assets()

        _logger.info(f"Asset scan complete: {self.scan_results['files_scanned']} files, "
                    f"{len(self.scan_results['owl_components'])} OWL components, "
                    f"{len(self.scan_results['css_classes'])} CSS classes")

        return self.scan_results

    def _scan_manifests(self):
        """Scan __manifest__.py files for asset bundle definitions"""
        for manifest_path in self.base_path.rglob('__manifest__.py'):
            try:
                with open(manifest_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Parse the manifest (simple eval-based extraction)
                # Find the assets dict
                assets_match = re.search(
                    r"'assets'\s*:\s*(\{[^}]+(?:\{[^}]*\}[^}]*)*\})",
                    content, re.DOTALL
                )

                if assets_match:
                    module_dir = manifest_path.parent
                    module_name = module_dir.name

                    # Extract asset paths from the manifest
                    assets_str = assets_match.group(1)

                    # Find all quoted paths
                    asset_paths = re.findall(r"['\"]([^'\"]+)['\"]", assets_str)

                    for asset_path in asset_paths:
                        # Skip bundle names
                        if asset_path.startswith('web.') or '.' not in asset_path:
                            continue

                        # Handle include directives
                        if asset_path.startswith(('include', 'remove')):
                            continue

                        # Normalize the path
                        if asset_path.startswith(module_name + '/'):
                            full_path = module_dir / asset_path[len(module_name)+1:]
                        else:
                            full_path = module_dir / asset_path

                        self._registered_assets.add(str(full_path))

                        # Track by bundle
                        bundle_match = re.search(
                            rf"['\"]([^'\"]+)['\"]\s*:\s*\[[^\]]*['\"].*?{re.escape(asset_path)}",
                            assets_str, re.DOTALL
                        )
                        bundle_name = bundle_match.group(1) if bundle_match else 'unknown'

                        if bundle_name not in self.scan_results['asset_bundles']:
                            self.scan_results['asset_bundles'][bundle_name] = []

                        self.scan_results['asset_bundles'][bundle_name].append({
                            'path': asset_path,
                            'module': module_name,
                            'full_path': str(full_path),
                        })

            except Exception as e:
                self.scan_results['errors'].append({
                    'file': str(manifest_path),
                    'error': f'Manifest parse error: {e}',
                })

    def _scan_js_file(self, file_path: Path):
        """Scan a JavaScript file"""
        # Skip non-Odoo directories
        if any(skip in str(file_path) for skip in
               ['node_modules', '.git', '__pycache__', 'venv']):
            return

        # Apply module filter - exact match on top-level module name
        if self.module_filter:
            try:
                rel_path = file_path.relative_to(self.base_path)
                top_module = rel_path.parts[0] if rel_path.parts else ''
                if top_module not in self.module_filter:
                    return
            except ValueError:
                return

        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            rel_path = str(file_path.relative_to(self.base_path))

            file_info = {
                'path': str(file_path),
                'relative_path': rel_path,
                'size': len(content),
                'lines': content.count('\n') + 1,
                'is_odoo_module': False,
                'module_alias': None,
                'imports': [],
                'exports': [],
                'functions': [],
                'components': [],
                'hash': hashlib.md5(content.encode()).hexdigest()[:12],
            }

            # Check for @odoo-module
            odoo_module_match = self.PATTERNS['odoo_module'].search(content)
            if odoo_module_match:
                file_info['is_odoo_module'] = True
                file_info['module_alias'] = odoo_module_match.group(1)

            # Extract OWL components
            for match in self.PATTERNS['owl_component'].finditer(content):
                component_name = match.group(1)
                file_info['components'].append(component_name)
                self.scan_results['owl_components'].append({
                    'name': component_name,
                    'file': rel_path,
                    'line': content[:match.start()].count('\n') + 1,
                })

            # Extract imports
            for match in self.PATTERNS['es6_import'].finditer(content):
                named_imports = match.group(1)
                default_import = match.group(2)
                module_path = match.group(3)

                import_info = {
                    'module': module_path,
                    'default': default_import,
                    'named': [n.strip() for n in named_imports.split(',')] if named_imports else [],
                }
                file_info['imports'].append(import_info)

            # Extract function definitions
            for pattern_name in ['function_def', 'arrow_function']:
                for match in self.PATTERNS[pattern_name].finditer(content):
                    func_name = match.group(1)
                    file_info['functions'].append(func_name)
                    self.scan_results['js_functions'].append({
                        'name': func_name,
                        'file': rel_path,
                        'type': pattern_name,
                        'line': content[:match.start()].count('\n') + 1,
                    })

            # Extract exports
            for match in self.PATTERNS['export'].finditer(content):
                export_name = match.group(1)
                if export_name:
                    file_info['exports'].append(export_name)
                    self.scan_results['js_exports'].append({
                        'name': export_name,
                        'file': rel_path,
                    })

            # Extract registry additions
            for match in self.PATTERNS['registry_add'].finditer(content):
                category = match.group(1) or 'default'
                name = match.group(2)
                self.scan_results['registry_additions'].append({
                    'category': category,
                    'name': name,
                    'file': rel_path,
                })

            # Extract patches
            for match in self.PATTERNS['patch_call'].finditer(content):
                target = match.group(1).strip()
                self.scan_results['patches'].append({
                    'target': target,
                    'file': rel_path,
                })

            self.scan_results['js_files'].append(file_info)
            self.scan_results['files_scanned'] += 1

        except Exception as e:
            self.scan_results['errors'].append({
                'file': str(file_path),
                'error': str(e),
            })

    def _scan_css_file(self, file_path: Path):
        """Scan a CSS/SCSS file"""
        # Skip non-Odoo directories
        if any(skip in str(file_path) for skip in
               ['node_modules', '.git', '__pycache__', 'venv']):
            return

        # Apply module filter - exact match on top-level module name
        if self.module_filter:
            try:
                rel_path = file_path.relative_to(self.base_path)
                top_module = rel_path.parts[0] if rel_path.parts else ''
                if top_module not in self.module_filter:
                    return
            except ValueError:
                return

        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            rel_path = str(file_path.relative_to(self.base_path))

            file_info = {
                'path': str(file_path),
                'relative_path': rel_path,
                'size': len(content),
                'lines': content.count('\n') + 1,
                'type': file_path.suffix,
                'classes': [],
                'ids': [],
                'variables': [],
                'hash': hashlib.md5(content.encode()).hexdigest()[:12],
            }

            # Extract CSS classes
            for match in self.PATTERNS['css_class'].finditer(content):
                class_name = match.group(1)
                if class_name not in file_info['classes']:
                    file_info['classes'].append(class_name)
                    self.scan_results['css_classes'].append({
                        'name': class_name,
                        'file': rel_path,
                        'line': content[:match.start()].count('\n') + 1,
                    })

            # Extract CSS IDs
            for match in self.PATTERNS['css_id'].finditer(content):
                id_name = match.group(1)
                if id_name not in file_info['ids']:
                    file_info['ids'].append(id_name)

            # Extract variables (SCSS and CSS custom properties)
            for pattern_name in ['scss_variable', 'css_variable']:
                for match in self.PATTERNS[pattern_name].finditer(content):
                    var_name = match.group(1)
                    if var_name not in file_info['variables']:
                        file_info['variables'].append(var_name)
                        self.scan_results['css_variables'].append({
                            'name': var_name,
                            'file': rel_path,
                            'type': 'scss' if pattern_name == 'scss_variable' else 'css',
                        })

            self.scan_results['css_files'].append(file_info)
            self.scan_results['files_scanned'] += 1

        except Exception as e:
            self.scan_results['errors'].append({
                'file': str(file_path),
                'error': str(e),
            })

    def _find_orphaned_assets(self):
        """Find assets not registered in any bundle"""
        all_asset_files = set()

        for js_file in self.scan_results['js_files']:
            all_asset_files.add(js_file['path'])

        for css_file in self.scan_results['css_files']:
            all_asset_files.add(css_file['path'])

        # Find files not in registered assets
        for asset_path in all_asset_files:
            # Normalize for comparison
            normalized = asset_path.replace('\\', '/')

            is_registered = False
            for registered in self._registered_assets:
                if normalized.endswith(registered.replace('\\', '/')) or \
                   registered.replace('\\', '/').endswith(normalized):
                    is_registered = True
                    break

            # Also check glob patterns in bundles
            for bundle, assets in self.scan_results['asset_bundles'].items():
                for asset in assets:
                    if '**' in asset['path'] or '*' in asset['path']:
                        # This is a glob pattern - do simple check
                        pattern_base = asset['path'].split('*')[0]
                        if pattern_base in normalized:
                            is_registered = True
                            break

            if not is_registered:
                self.scan_results['orphaned_assets'].append({
                    'path': asset_path,
                    'type': 'js' if asset_path.endswith('.js') else 'css',
                })

    def get_component_by_name(self, name: str) -> Optional[Dict]:
        """Find an OWL component by name"""
        for comp in self.scan_results['owl_components']:
            if comp['name'] == name:
                return comp
        return None

    def get_duplicate_classes(self) -> Dict[str, List[str]]:
        """Find CSS classes defined in multiple files"""
        class_files = {}
        for css_class in self.scan_results['css_classes']:
            name = css_class['name']
            if name not in class_files:
                class_files[name] = []
            class_files[name].append(css_class['file'])

        # Return only duplicates
        return {name: files for name, files in class_files.items() if len(files) > 1}

    def get_duplicate_functions(self) -> Dict[str, List[str]]:
        """Find JS functions with same name in multiple files"""
        func_files = {}
        for func in self.scan_results['js_functions']:
            name = func['name']
            if name not in func_files:
                func_files[name] = []
            func_files[name].append(func['file'])

        # Return only duplicates
        return {name: files for name, files in func_files.items() if len(files) > 1}
