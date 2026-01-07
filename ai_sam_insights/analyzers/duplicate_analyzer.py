# -*- coding: utf-8 -*-
"""
Duplicate Analyzer for SAM AI Insights

Detects:
- Duplicate models (same functionality, different names)
- Duplicate functions (same logic, different names)
- Duplicate CSS classes
- Similar code patterns
- Renamed components (old_, _v2, backup_, etc.)
"""
import re
import hashlib
from typing import Dict, List, Any, Set, Tuple
from difflib import SequenceMatcher
import logging

_logger = logging.getLogger(__name__)


class DuplicateAnalyzer:
    """Analyzes code for duplicates and similarities"""

    # Patterns that suggest renamed/backup code
    RENAME_PATTERNS = [
        r'_old$',
        r'_backup$',
        r'_deprecated$',
        r'_legacy$',
        r'_v\d+$',
        r'^old_',
        r'^backup_',
        r'^deprecated_',
        r'_copy$',
        r'_temp$',
        r'_test$',
        r'Original',
        r'Copy',
    ]

    def __init__(self, python_scan: Dict, xml_scan: Dict, asset_scan: Dict):
        self.python_scan = python_scan
        self.xml_scan = xml_scan
        self.asset_scan = asset_scan
        self.findings = {
            'duplicate_models': [],
            'duplicate_functions': [],
            'duplicate_methods': [],
            'duplicate_css_classes': [],
            'duplicate_views': [],
            'similar_models': [],
            'renamed_components': [],
            'summary': {},
        }

    def analyze(self) -> Dict[str, Any]:
        """Run all duplicate detection analyses"""
        _logger.info("Starting duplicate analysis")

        self._find_duplicate_models()
        self._find_duplicate_functions()
        self._find_duplicate_methods()
        self._find_duplicate_css_classes()
        self._find_duplicate_views()
        self._find_similar_models()
        self._find_renamed_components()
        self._generate_summary()

        _logger.info(f"Duplicate analysis complete: {self.findings['summary']}")

        return self.findings

    def _find_duplicate_models(self):
        """Find models with the same _name defined in multiple places"""
        model_definitions = {}

        for model in self.python_scan.get('models', []):
            model_name = model.get('_name')
            if not model_name:
                continue

            if model_name not in model_definitions:
                model_definitions[model_name] = []

            model_definitions[model_name].append({
                'class_name': model['class_name'],
                'file': model['relative_path'],
                'line': model['line_start'],
                'field_count': len(model.get('fields', [])),
                'method_count': len(model.get('methods', [])),
            })

        # Find duplicates
        for model_name, definitions in model_definitions.items():
            if len(definitions) > 1:
                # Check if these are actual duplicates or inheritance
                is_inheritance = any(
                    model_name in m.get('_inherit', [])
                    for m in self.python_scan.get('models', [])
                    if m.get('_name') == model_name
                )

                self.findings['duplicate_models'].append({
                    'model_name': model_name,
                    'definitions': definitions,
                    'is_inheritance': is_inheritance,
                    'severity': 'warning' if is_inheritance else 'error',
                })

    def _find_duplicate_functions(self):
        """Find functions with identical body hashes"""
        function_hashes = {}

        for func in self.python_scan.get('functions', []):
            body_hash = func.get('body_hash')
            if not body_hash or func.get('class_name'):
                # Skip methods (they're handled separately)
                continue

            if body_hash not in function_hashes:
                function_hashes[body_hash] = []

            function_hashes[body_hash].append({
                'name': func['name'],
                'file': func['relative_path'],
                'line': func['line_start'],
            })

        # Find duplicates
        for body_hash, functions in function_hashes.items():
            if len(functions) > 1:
                self.findings['duplicate_functions'].append({
                    'body_hash': body_hash,
                    'functions': functions,
                    'count': len(functions),
                    'severity': 'warning',
                    'recommendation': 'Consider consolidating into a shared utility function',
                })

    def _find_duplicate_methods(self):
        """Find methods with identical body hashes across models"""
        method_hashes = {}

        for model in self.python_scan.get('models', []):
            model_name = model.get('_name', model['class_name'])

            for method in model.get('methods', []):
                body_hash = method.get('body_hash')
                if not body_hash:
                    continue

                # Skip common Odoo methods
                if method['name'] in ('create', 'write', 'unlink', 'read', 'search',
                                     'name_get', 'name_search', 'default_get'):
                    continue

                if body_hash not in method_hashes:
                    method_hashes[body_hash] = []

                method_hashes[body_hash].append({
                    'model': model_name,
                    'method': method['name'],
                    'file': model['relative_path'],
                    'line': method['line_start'],
                    'decorators': method.get('decorators', []),
                })

        # Find duplicates (excluding self-same methods)
        for body_hash, methods in method_hashes.items():
            if len(methods) > 1:
                # Group by unique method names
                unique_methods = {}
                for m in methods:
                    key = (m['model'], m['method'])
                    unique_methods[key] = m

                if len(unique_methods) > 1:
                    self.findings['duplicate_methods'].append({
                        'body_hash': body_hash,
                        'methods': list(unique_methods.values()),
                        'count': len(unique_methods),
                        'severity': 'warning',
                        'recommendation': 'Consider extracting to a mixin or utility',
                    })

    def _find_duplicate_css_classes(self):
        """Find CSS classes defined in multiple files"""
        class_definitions = {}

        for css_class in self.asset_scan.get('css_classes', []):
            name = css_class['name']

            # Skip common/utility class names
            if name in ('active', 'hidden', 'show', 'hide', 'disabled', 'selected',
                       'error', 'warning', 'success', 'info', 'primary', 'secondary'):
                continue

            if name not in class_definitions:
                class_definitions[name] = []

            class_definitions[name].append({
                'file': css_class['file'],
                'line': css_class['line'],
            })

        # Find duplicates
        for class_name, definitions in class_definitions.items():
            if len(definitions) > 1:
                # Get unique files
                files = list(set(d['file'] for d in definitions))
                if len(files) > 1:  # Same class in different files
                    self.findings['duplicate_css_classes'].append({
                        'class_name': class_name,
                        'files': files,
                        'count': len(files),
                        'severity': 'info',
                        'recommendation': 'Consider using a shared CSS file or CSS variables',
                    })

    def _find_duplicate_views(self):
        """Find views with identical or very similar arch"""
        view_contents = {}

        for view in self.xml_scan.get('views', []):
            # Create a normalized key from view content
            fields = tuple(sorted(view.get('field_references', [])))
            view_type = view.get('view_type')
            model = view.get('view_model')

            if not fields or not view_type:
                continue

            key = (model, view_type, fields)

            if key not in view_contents:
                view_contents[key] = []

            view_contents[key].append({
                'xml_id': view['xml_id'],
                'file': view['relative_path'],
                'inherit_id': view.get('inherit_id'),
            })

        # Find duplicates
        for key, views in view_contents.items():
            if len(views) > 1:
                # Filter out inherited views
                base_views = [v for v in views if not v['inherit_id']]
                if len(base_views) > 1:
                    self.findings['duplicate_views'].append({
                        'model': key[0],
                        'view_type': key[1],
                        'field_count': len(key[2]),
                        'views': base_views,
                        'severity': 'warning',
                        'recommendation': 'Consider consolidating duplicate views',
                    })

    def _find_similar_models(self, similarity_threshold: float = 0.7):
        """Find models with similar field structures"""
        models_by_fields = []

        for model in self.python_scan.get('models', []):
            model_name = model.get('_name') or model.get('class_name', 'Unknown')
            if not model_name:
                continue  # Skip models without a name

            fields = set(f['name'] for f in model.get('fields', []) if f.get('name'))

            if len(fields) < 3:  # Skip tiny models
                continue

            models_by_fields.append({
                'name': model_name,
                'class_name': model.get('class_name', 'Unknown'),
                'fields': fields,
                'file': model.get('relative_path', 'Unknown'),
            })

        # Compare models pairwise
        compared = set()
        for i, model1 in enumerate(models_by_fields):
            for model2 in models_by_fields[i+1:]:
                pair_key = tuple(sorted([model1['name'], model2['name']]))
                if pair_key in compared:
                    continue
                compared.add(pair_key)

                # Calculate Jaccard similarity
                intersection = len(model1['fields'] & model2['fields'])
                union = len(model1['fields'] | model2['fields'])

                if union == 0:
                    continue

                similarity = intersection / union

                if similarity >= similarity_threshold:
                    self.findings['similar_models'].append({
                        'model1': model1['name'],
                        'model1_file': model1['file'],
                        'model2': model2['name'],
                        'model2_file': model2['file'],
                        'similarity': round(similarity * 100, 1),
                        'common_fields': list(model1['fields'] & model2['fields']),
                        'severity': 'info' if similarity < 0.85 else 'warning',
                        'recommendation': 'Consider using inheritance or a common base model',
                    })

    def _find_renamed_components(self):
        """Find components that appear to be renamed versions of others"""
        # Check models - filter out None values
        model_names = [
            m.get('_name') or m.get('class_name')
            for m in self.python_scan.get('models', [])
        ]
        model_names = [n for n in model_names if n]  # Filter out None
        self._check_renames(model_names, 'model')

        # Check functions - filter out None values
        func_names = [
            f.get('name')
            for f in self.python_scan.get('functions', [])
            if not f.get('class_name')
        ]
        func_names = [n for n in func_names if n]  # Filter out None
        self._check_renames(func_names, 'function')

        # Check OWL components - filter out None values
        component_names = [c.get('name') for c in self.asset_scan.get('owl_components', [])]
        component_names = [n for n in component_names if n]  # Filter out None
        self._check_renames(component_names, 'owl_component')

        # Check CSS classes for versioned duplicates - filter out None values
        css_classes = [c.get('name') for c in self.asset_scan.get('css_classes', [])]
        css_classes = [n for n in css_classes if n]  # Filter out None
        self._check_renames(css_classes, 'css_class')

    def _check_renames(self, names: List[str], component_type: str):
        """Check a list of names for rename patterns"""
        for name in names:
            if not name:  # Extra safety check
                continue
            # Check against rename patterns
            for pattern in self.RENAME_PATTERNS:
                if re.search(pattern, name, re.IGNORECASE):
                    # Try to find the "original" version
                    base_name = re.sub(pattern, '', name, flags=re.IGNORECASE)
                    if base_name in names and base_name != name:
                        self.findings['renamed_components'].append({
                            'type': component_type,
                            'renamed': name,
                            'original': base_name,
                            'pattern_matched': pattern,
                            'severity': 'warning',
                            'recommendation': f"Consider removing '{name}' if it's no longer needed",
                        })
                    elif base_name != name:
                        # Potential orphaned renamed version
                        self.findings['renamed_components'].append({
                            'type': component_type,
                            'renamed': name,
                            'original': None,
                            'pattern_matched': pattern,
                            'severity': 'info',
                            'recommendation': f"'{name}' follows a rename pattern but no original found - verify if needed",
                        })
                    break

    def _generate_summary(self):
        """Generate summary statistics"""
        self.findings['summary'] = {
            'duplicate_models': len(self.findings['duplicate_models']),
            'duplicate_functions': len(self.findings['duplicate_functions']),
            'duplicate_methods': len(self.findings['duplicate_methods']),
            'duplicate_css_classes': len(self.findings['duplicate_css_classes']),
            'duplicate_views': len(self.findings['duplicate_views']),
            'similar_models': len(self.findings['similar_models']),
            'renamed_components': len(self.findings['renamed_components']),
            'total_issues': sum([
                len(self.findings['duplicate_models']),
                len(self.findings['duplicate_functions']),
                len(self.findings['duplicate_methods']),
                len(self.findings['duplicate_css_classes']),
                len(self.findings['duplicate_views']),
                len(self.findings['renamed_components']),
            ]),
            'severity_counts': {
                'error': 0,
                'warning': 0,
                'info': 0,
            }
        }

        # Count severities
        for category in ['duplicate_models', 'duplicate_functions', 'duplicate_methods',
                        'duplicate_css_classes', 'duplicate_views', 'similar_models',
                        'renamed_components']:
            for item in self.findings[category]:
                severity = item.get('severity', 'info')
                self.findings['summary']['severity_counts'][severity] += 1


def calculate_code_similarity(code1: str, code2: str) -> float:
    """Calculate similarity ratio between two code strings"""
    # Normalize whitespace
    code1 = re.sub(r'\s+', ' ', code1.strip())
    code2 = re.sub(r'\s+', ' ', code2.strip())

    return SequenceMatcher(None, code1, code2).ratio()
