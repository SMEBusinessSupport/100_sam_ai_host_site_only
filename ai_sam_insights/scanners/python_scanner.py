# -*- coding: utf-8 -*-
"""
Python AST Scanner for SAM AI Insights

Scans Python files to extract:
- Model definitions (class Name(models.Model))
- Field definitions (field_name = fields.Char())
- Method definitions (def method_name())
- Imports and dependencies
- Decorators (@api.model, @api.depends, etc.)
"""
import ast
import os
import re
import hashlib
from pathlib import Path
from typing import Dict, List, Any, Optional, Set, Tuple
import logging

_logger = logging.getLogger(__name__)


class OdooModelVisitor(ast.NodeVisitor):
    """AST visitor that extracts Odoo model information"""

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.models = []
        self.functions = []
        self.imports = []
        self.current_class = None
        self.current_class_bases = []

    def visit_Import(self, node):
        for alias in node.names:
            self.imports.append({
                'type': 'import',
                'module': alias.name,
                'alias': alias.asname,
                'line': node.lineno,
            })
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        module = node.module or ''
        for alias in node.names:
            self.imports.append({
                'type': 'from',
                'module': module,
                'name': alias.name,
                'alias': alias.asname,
                'line': node.lineno,
            })
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        # Check if this is an Odoo model
        base_names = []
        is_odoo_model = False

        for base in node.bases:
            base_name = self._get_name(base)
            base_names.append(base_name)
            if base_name in ('models.Model', 'models.TransientModel', 'models.AbstractModel',
                           'Model', 'TransientModel', 'AbstractModel'):
                is_odoo_model = True

        if is_odoo_model:
            model_info = self._extract_model_info(node, base_names)
            self.models.append(model_info)

        # Store current class context for method extraction
        old_class = self.current_class
        old_bases = self.current_class_bases
        self.current_class = node.name
        self.current_class_bases = base_names

        self.generic_visit(node)

        self.current_class = old_class
        self.current_class_bases = old_bases

    def visit_FunctionDef(self, node):
        func_info = self._extract_function_info(node)
        self.functions.append(func_info)
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node):
        func_info = self._extract_function_info(node, is_async=True)
        self.functions.append(func_info)
        self.generic_visit(node)

    def _get_name(self, node) -> str:
        """Extract name from various AST node types"""
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            return f"{self._get_name(node.value)}.{node.attr}"
        elif isinstance(node, ast.Call):
            return self._get_name(node.func)
        elif isinstance(node, ast.Subscript):
            return self._get_name(node.value)
        return ''

    def _extract_model_info(self, node: ast.ClassDef, base_names: List[str]) -> Dict[str, Any]:
        """Extract all information from an Odoo model class"""
        model_info = {
            'class_name': node.name,
            'bases': base_names,
            'line_start': node.lineno,
            'line_end': node.end_lineno,
            'file_path': self.file_path,
            '_name': None,
            '_inherit': [],
            '_description': None,
            '_order': None,
            '_rec_name': None,
            '_sql_constraints': [],
            'fields': [],
            'methods': [],
            'decorators': [self._get_decorator_name(d) for d in node.decorator_list],
        }

        for item in node.body:
            # Extract _name, _inherit, etc.
            if isinstance(item, ast.Assign):
                for target in item.targets:
                    if isinstance(target, ast.Name):
                        attr_name = target.id
                        value = self._extract_value(item.value)

                        if attr_name == '_name':
                            model_info['_name'] = value
                        elif attr_name == '_inherit':
                            if isinstance(value, list):
                                model_info['_inherit'] = value
                            elif value:
                                model_info['_inherit'] = [value]
                        elif attr_name == '_description':
                            model_info['_description'] = value
                        elif attr_name == '_order':
                            model_info['_order'] = value
                        elif attr_name == '_rec_name':
                            model_info['_rec_name'] = value
                        elif attr_name == '_sql_constraints':
                            model_info['_sql_constraints'] = self._extract_constraints(item.value)
                        elif self._is_field_definition(item.value):
                            field_info = self._extract_field_info(attr_name, item.value, item.lineno)
                            model_info['fields'].append(field_info)

            # Extract methods
            elif isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                method_info = self._extract_method_info(item)
                model_info['methods'].append(method_info)

        return model_info

    def _is_field_definition(self, node) -> bool:
        """Check if a node is a field definition"""
        if isinstance(node, ast.Call):
            func_name = self._get_name(node.func)
            return func_name.startswith('fields.') or func_name in (
                'Char', 'Text', 'Html', 'Integer', 'Float', 'Boolean',
                'Date', 'Datetime', 'Binary', 'Selection', 'Many2one',
                'One2many', 'Many2many', 'Reference', 'Monetary'
            )
        return False

    def _extract_field_info(self, name: str, node: ast.Call, line: int) -> Dict[str, Any]:
        """Extract field information from a field definition"""
        func_name = self._get_name(node.func)
        field_type = func_name.replace('fields.', '')

        field_info = {
            'name': name,
            'type': field_type,
            'line': line,
            'attributes': {},
        }

        # Extract keyword arguments
        for keyword in node.keywords:
            if keyword.arg:
                field_info['attributes'][keyword.arg] = self._extract_value(keyword.value)

        # Extract positional arguments (usually string for Char, Text, etc.)
        if node.args:
            first_arg = self._extract_value(node.args[0])
            if isinstance(first_arg, str):
                field_info['attributes']['string'] = first_arg

        # Special handling for relational fields
        if field_type in ('Many2one', 'One2many', 'Many2many'):
            if node.args:
                field_info['attributes']['comodel_name'] = self._extract_value(node.args[0])

        return field_info

    def _extract_method_info(self, node) -> Dict[str, Any]:
        """Extract method information"""
        decorators = []
        decorator_details = []

        for dec in node.decorator_list:
            dec_name = self._get_decorator_name(dec)
            decorators.append(dec_name)

            # Extract decorator arguments
            if isinstance(dec, ast.Call):
                args = [self._extract_value(a) for a in dec.args]
                decorator_details.append({'name': dec_name, 'args': args})

        # Calculate method signature hash for duplicate detection
        signature = self._get_method_signature(node)

        return {
            'name': node.name,
            'line_start': node.lineno,
            'line_end': node.end_lineno,
            'decorators': decorators,
            'decorator_details': decorator_details,
            'is_private': node.name.startswith('_'),
            'is_compute': 'api.depends' in decorators or 'depends' in decorators,
            'is_onchange': 'api.onchange' in decorators or 'onchange' in decorators,
            'is_constraint': 'api.constrains' in decorators or 'constrains' in decorators,
            'args': [arg.arg for arg in node.args.args if arg.arg != 'self'],
            'signature_hash': signature,
            'body_hash': self._hash_method_body(node),
        }

    def _extract_function_info(self, node, is_async: bool = False) -> Dict[str, Any]:
        """Extract standalone function information"""
        return {
            'name': node.name,
            'class_name': self.current_class,
            'class_bases': self.current_class_bases,
            'line_start': node.lineno,
            'line_end': node.end_lineno,
            'file_path': self.file_path,
            'is_async': is_async,
            'decorators': [self._get_decorator_name(d) for d in node.decorator_list],
            'args': [arg.arg for arg in node.args.args if arg.arg != 'self'],
            'signature_hash': self._get_method_signature(node),
            'body_hash': self._hash_method_body(node),
        }

    def _get_decorator_name(self, node) -> str:
        """Extract decorator name"""
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            return f"{self._get_name(node.value)}.{node.attr}"
        elif isinstance(node, ast.Call):
            return self._get_name(node.func)
        return ''

    def _extract_value(self, node) -> Any:
        """Extract literal value from AST node"""
        if isinstance(node, ast.Constant):
            return node.value
        elif isinstance(node, ast.Str):  # Python 3.7 compatibility
            return node.s
        elif isinstance(node, ast.Num):
            return node.n
        elif isinstance(node, ast.Name):
            if node.id in ('True', 'False'):
                return node.id == 'True'
            return node.id
        elif isinstance(node, ast.List):
            return [self._extract_value(elt) for elt in node.elts]
        elif isinstance(node, ast.Tuple):
            return tuple(self._extract_value(elt) for elt in node.elts)
        elif isinstance(node, ast.Dict):
            return {
                self._extract_value(k): self._extract_value(v)
                for k, v in zip(node.keys, node.values) if k is not None
            }
        elif isinstance(node, ast.Attribute):
            return self._get_name(node)
        elif isinstance(node, ast.Call):
            # For lambda, _() translations, etc.
            return f"<call:{self._get_name(node.func)}>"
        return None

    def _extract_constraints(self, node) -> List[Dict[str, str]]:
        """Extract SQL constraints"""
        constraints = []
        if isinstance(node, ast.List):
            for elt in node.elts:
                if isinstance(elt, ast.Tuple) and len(elt.elts) >= 3:
                    constraints.append({
                        'name': self._extract_value(elt.elts[0]),
                        'definition': self._extract_value(elt.elts[1]),
                        'message': self._extract_value(elt.elts[2]),
                    })
        return constraints

    def _get_method_signature(self, node) -> str:
        """Create a signature hash for method comparison"""
        sig_parts = [
            node.name,
            str(len(node.args.args)),
            ','.join(arg.arg for arg in node.args.args if arg.arg != 'self'),
        ]
        return hashlib.md5('|'.join(sig_parts).encode()).hexdigest()[:8]

    def _hash_method_body(self, node) -> str:
        """Create a hash of the method body for duplicate detection"""
        try:
            body_str = ast.dump(ast.Module(body=node.body, type_ignores=[]))
            return hashlib.md5(body_str.encode()).hexdigest()[:12]
        except Exception:
            return ''


class PythonScanner:
    """Main Python file scanner"""

    def __init__(self, base_path: str, module_filter: Optional[List[str]] = None):
        self.base_path = Path(base_path)
        self.module_filter = module_filter or []
        self.scan_results = {
            'models': [],
            'functions': [],
            'imports': [],
            'files_scanned': 0,
            'errors': [],
            'init_files': {},
        }

    def scan(self) -> Dict[str, Any]:
        """Scan all Python files in the base path"""
        _logger.info(f"Starting Python scan of {self.base_path}")

        for py_file in self.base_path.rglob('*.py'):
            # Skip if module filter is set and file is not in allowed modules
            if self.module_filter:
                # Get the relative path and extract the top-level module name
                try:
                    rel_path = py_file.relative_to(self.base_path)
                    # The first part of the path is the module name
                    top_module = rel_path.parts[0] if rel_path.parts else ''
                    # Check for exact module match (not substring)
                    if top_module not in self.module_filter:
                        continue
                except ValueError:
                    continue

            # Skip __pycache__ and virtual environments
            if '__pycache__' in str(py_file) or 'venv' in str(py_file) or '.git' in str(py_file):
                continue

            self._scan_file(py_file)

        # Analyze __init__.py files for import tracking
        self._analyze_init_files()

        _logger.info(f"Python scan complete: {self.scan_results['files_scanned']} files, "
                    f"{len(self.scan_results['models'])} models, "
                    f"{len(self.scan_results['functions'])} functions")

        return self.scan_results

    def _scan_file(self, file_path: Path):
        """Scan a single Python file"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                source = f.read()

            tree = ast.parse(source, filename=str(file_path))
            visitor = OdooModelVisitor(str(file_path))
            visitor.visit(tree)

            # Add relative path for easier reference
            rel_path = str(file_path.relative_to(self.base_path))

            for model in visitor.models:
                model['relative_path'] = rel_path
                self.scan_results['models'].append(model)

            for func in visitor.functions:
                func['relative_path'] = rel_path
                self.scan_results['functions'].append(func)

            for imp in visitor.imports:
                imp['file_path'] = str(file_path)
                imp['relative_path'] = rel_path
                self.scan_results['imports'].append(imp)

            # Track __init__.py files - use relative path as key for consistency
            if file_path.name == '__init__.py':
                rel_dir = str(file_path.parent.relative_to(self.base_path))
                self.scan_results['init_files'][rel_dir] = {
                    'imports': visitor.imports,
                    'path': str(file_path),
                    'relative_path': rel_dir,
                }

            self.scan_results['files_scanned'] += 1

        except SyntaxError as e:
            self.scan_results['errors'].append({
                'file': str(file_path),
                'error': f'Syntax error: {e}',
                'line': getattr(e, 'lineno', None),
            })
        except Exception as e:
            self.scan_results['errors'].append({
                'file': str(file_path),
                'error': str(e),
            })

    def _analyze_init_files(self):
        """Analyze __init__.py files to find orphaned modules"""
        imported_modules = set()

        for init_info in self.scan_results['init_files'].values():
            for imp in init_info['imports']:
                if imp['type'] == 'from' and imp.get('module') == '.':
                    # from . import module_name
                    if imp.get('name'):
                        imported_modules.add(imp['name'])
                elif imp['type'] == 'from' and imp.get('module', '').startswith('.'):
                    # from .submodule import something
                    if imp.get('name'):
                        imported_modules.add(imp['name'])
                elif imp['type'] == 'import':
                    # import module_name - use 'module' key instead of 'name'
                    if imp.get('module'):
                        imported_modules.add(imp['module'])

        self.scan_results['imported_modules'] = list(imported_modules)

    def get_model_by_name(self, model_name: str) -> Optional[Dict]:
        """Find a model by its _name attribute"""
        for model in self.scan_results['models']:
            if model.get('_name') == model_name:
                return model
        return None

    def get_models_inheriting(self, model_name: str) -> List[Dict]:
        """Find all models that inherit from a specific model"""
        result = []
        for model in self.scan_results['models']:
            if model_name in model.get('_inherit', []):
                result.append(model)
        return result

    def get_field_usages(self, field_name: str) -> List[Dict]:
        """Find all models that define a specific field"""
        result = []
        for model in self.scan_results['models']:
            for field in model.get('fields', []):
                if field['name'] == field_name:
                    result.append({
                        'model': model.get('_name') or model['class_name'],
                        'field': field,
                        'file': model['relative_path'],
                    })
        return result
