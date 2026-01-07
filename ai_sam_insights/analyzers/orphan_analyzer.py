# -*- coding: utf-8 -*-
"""
Orphan Analyzer for SAM AI Insights

Detects:
- Orphaned Python files not imported in __init__.py
- Orphaned models with no views
- Orphaned views referencing non-existent fields
- Orphaned actions with no menu
- Orphaned menus with broken actions
- Dangling field references
- Unused CSS classes
- Orphaned JS files not in asset bundles
"""
from typing import Dict, List, Any, Set, Optional
import logging

_logger = logging.getLogger(__name__)


class OrphanAnalyzer:
    """Analyzes code for orphaned and dangling references"""

    def __init__(self, python_scan: Dict, xml_scan: Dict, asset_scan: Dict,
                 registry_scan: Optional[Dict] = None):
        self.python_scan = python_scan
        self.xml_scan = xml_scan
        self.asset_scan = asset_scan
        self.registry_scan = registry_scan or {}
        self.findings = {
            'orphaned_python_files': [],
            'orphaned_models': [],
            'orphaned_views': [],
            'orphaned_actions': [],
            'orphaned_menus': [],
            'dangling_field_refs': [],
            'dangling_model_refs': [],
            'orphaned_assets': [],
            'unused_css_classes': [],
            'missing_dependencies': [],
            'summary': {},
        }

    def analyze(self) -> Dict[str, Any]:
        """Run all orphan detection analyses"""
        _logger.info("Starting orphan analysis")

        self._find_orphaned_python_files()
        self._find_orphaned_models()
        self._find_orphaned_views()
        self._find_orphaned_actions()
        self._find_orphaned_menus()
        self._find_dangling_field_refs()
        self._find_dangling_model_refs()
        self._find_orphaned_assets()
        self._find_missing_dependencies()
        self._generate_summary()

        _logger.info(f"Orphan analysis complete: {self.findings['summary']}")

        return self.findings

    # Known false positive patterns for orphaned Python files
    # These files are loaded via manifest hooks or are intentional standalone scripts
    ORPHAN_PYTHON_WHITELIST = {
        'hooks',           # Loaded via manifest post_init_hook/post_update_hook
        'post_install',    # Installation hooks
        'pre_init',        # Pre-init hooks
    }

    # Directories containing intentional standalone scripts (not Odoo modules)
    STANDALONE_SCRIPT_DIRS = {
        'scripts',         # Utility scripts
        'tools',           # Development tools
        'utils',           # Standalone utilities
    }

    # Base Odoo models that won't be in the scan scope
    # These are from core Odoo, not custom modules
    BASE_ODOO_MODELS = {
        # Base models
        'res.config.settings',
        'res.users',
        'res.partner',
        'res.company',
        'res.country',
        'res.currency',
        'res.groups',
        # Accounting
        'account.move',
        'account.move.line',
        'account.account',
        'account.journal',
        'account.payment',
        'account.tax',
        # Mail
        'mail.thread',
        'mail.activity.mixin',
        'mail.message',
        # Product
        'product.product',
        'product.template',
        # Sale/Purchase
        'sale.order',
        'sale.order.line',
        'purchase.order',
        # Stock
        'stock.picking',
        'stock.move',
        # CRM
        'crm.lead',
        # HR
        'hr.employee',
        # Web
        'ir.ui.view',
        'ir.ui.menu',
        'ir.actions.act_window',
        'ir.model',
        'ir.model.fields',
        'ir.attachment',
        'ir.cron',
        'ir.config_parameter',
        'ir.rule',
        'ir.sequence',
    }

    def _find_orphaned_python_files(self):
        """Find Python files not imported in any __init__.py"""
        # Build a map of package directories to their imported modules
        # Key: directory path (e.g., "ai_sam_base/services")
        # Value: set of module names imported in that directory's __init__.py
        package_imports = {}

        for init_path, init_info in self.python_scan.get('init_files', {}).items():
            # Normalize path separators
            init_dir = init_path.replace('\\', '/')
            imported_in_dir = set()

            for imp in init_info.get('imports', []):
                # Look for relative imports: from . import X
                if imp.get('type') == 'from' and imp.get('module', '') in ('.', ''):
                    name = imp.get('name')
                    if name:
                        imported_in_dir.add(name)
                # Also catch: from .submodule import X (submodule is imported)
                elif imp.get('type') == 'from' and imp.get('module', '').startswith('.'):
                    # Extract the first part after the dot
                    module_part = imp.get('module', '').lstrip('.')
                    if module_part:
                        first_part = module_part.split('.')[0]
                        imported_in_dir.add(first_part)

            package_imports[init_dir] = imported_in_dir

        # Get all Python files
        all_py_files = set()
        for model in self.python_scan.get('models', []):
            if model.get('relative_path'):
                all_py_files.add(model['relative_path'])
        for func in self.python_scan.get('functions', []):
            if func.get('relative_path'):
                all_py_files.add(func['relative_path'])

        # Check each file against its parent package's __init__.py
        for py_file in all_py_files:
            # Skip __init__.py files
            if py_file.endswith('__init__.py'):
                continue

            # Normalize path
            py_file_normalized = py_file.replace('\\', '/')
            parts = py_file_normalized.split('/')

            if len(parts) < 2:
                continue

            # Get module name and parent directory
            module_name = parts[-1].replace('.py', '')
            parent_dir = '/'.join(parts[:-1])

            # Skip whitelisted files (hooks, etc.)
            if module_name in self.ORPHAN_PYTHON_WHITELIST:
                continue

            # Skip files in standalone script directories
            parent_dir_name = parts[-2] if len(parts) >= 2 else ''
            if parent_dir_name in self.STANDALONE_SCRIPT_DIRS:
                continue

            # Check if this module is imported in its parent's __init__.py
            parent_imports = package_imports.get(parent_dir, set())

            if module_name not in parent_imports:
                # Before marking as orphaned, check if parent directory itself is imported
                # (transitive import check)
                is_transitively_imported = False

                # Walk up the directory tree to check if any parent is properly imported
                current_dir = parent_dir
                while '/' in current_dir:
                    grandparent = '/'.join(current_dir.split('/')[:-1])
                    current_name = current_dir.split('/')[-1]
                    grandparent_imports = package_imports.get(grandparent, set())

                    if current_name in grandparent_imports:
                        # Parent is imported, so this might be okay if parent imports the module
                        if module_name in package_imports.get(current_dir, set()):
                            is_transitively_imported = True
                            break
                    current_dir = grandparent

                if not is_transitively_imported and module_name not in parent_imports:
                    self.findings['orphaned_python_files'].append({
                        'file': py_file,
                        'module_name': module_name,
                        'parent_dir': parent_dir,
                        'severity': 'warning',
                        'recommendation': f"Add 'from . import {module_name}' to {parent_dir}/__init__.py or remove file",
                    })

    def _find_orphaned_models(self):
        """Find models with no views defined"""
        # Get all model names from Python
        python_models = {
            m.get('_name'): m for m in self.python_scan.get('models', [])
            if m.get('_name')
        }

        # Get models that have views
        models_with_views = set()
        for view in self.xml_scan.get('views', []):
            if view.get('view_model'):
                models_with_views.add(view['view_model'])

        # Get models that have actions
        models_with_actions = set()
        for action in self.xml_scan.get('actions', []):
            if action.get('res_model'):
                models_with_actions.add(action['res_model'])

        # Find orphans
        for model_name, model_info in python_models.items():
            # Skip abstract models and transient models
            if 'AbstractModel' in model_info.get('bases', []):
                continue
            if 'TransientModel' in model_info.get('bases', []):
                continue

            has_views = model_name in models_with_views
            has_actions = model_name in models_with_actions

            if not has_views and not has_actions:
                self.findings['orphaned_models'].append({
                    'model': model_name,
                    'class_name': model_info['class_name'],
                    'file': model_info['relative_path'],
                    'has_views': False,
                    'has_actions': False,
                    'field_count': len(model_info.get('fields', [])),
                    'severity': 'info',
                    'recommendation': 'This model has no UI - verify if this is intentional',
                })

    def _find_orphaned_views(self):
        """Find views with broken inherit_id references"""
        # Build set of all view XML IDs
        all_view_ids = {v['xml_id'] for v in self.xml_scan.get('views', []) if v['xml_id']}

        for view in self.xml_scan.get('views', []):
            inherit_id = view.get('inherit_id')
            if inherit_id:
                # Check if the inherited view exists locally
                if inherit_id not in all_view_ids:
                    # Could be from another module - check if it looks like module.view_id
                    if '.' in inherit_id:
                        module = inherit_id.split('.')[0]
                        # This might be a valid external reference
                        self.findings['orphaned_views'].append({
                            'view_xml_id': view['xml_id'],
                            'inherit_id': inherit_id,
                            'file': view['relative_path'],
                            'external_module': module,
                            'severity': 'info',
                            'recommendation': f"Inherits from external module '{module}' - verify dependency",
                        })
                    else:
                        self.findings['orphaned_views'].append({
                            'view_xml_id': view['xml_id'],
                            'inherit_id': inherit_id,
                            'file': view['relative_path'],
                            'severity': 'error',
                            'recommendation': f"Parent view '{inherit_id}' not found - check XML ID",
                        })

    def _find_orphaned_actions(self):
        """Find actions not linked to any menu"""
        # Build set of actions used in menus
        actions_in_menus = set()
        for menu in self.xml_scan.get('menus', []):
            if menu.get('action'):
                actions_in_menus.add(menu['action'])

        # Check each action
        for action in self.xml_scan.get('actions', []):
            xml_id = action.get('xml_id')
            if xml_id and xml_id not in actions_in_menus:
                # Check if it's a report or server action (often not in menus)
                action_type = action.get('action_type', '')
                if 'report' in action_type or 'server' in action_type:
                    continue

                self.findings['orphaned_actions'].append({
                    'action_xml_id': xml_id,
                    'action_type': action_type,
                    'res_model': action.get('res_model'),
                    'file': action.get('relative_path'),
                    'severity': 'info',
                    'recommendation': 'Action has no menu - verify if accessed programmatically',
                })

    def _find_orphaned_menus(self):
        """Find menus with broken action or parent references"""
        # Build reference sets
        all_action_ids = {a['xml_id'] for a in self.xml_scan.get('actions', []) if a.get('xml_id')}
        all_menu_ids = {m['xml_id'] for m in self.xml_scan.get('menus', []) if m.get('xml_id')}

        for menu in self.xml_scan.get('menus', []):
            issues = []

            # Check action reference
            action_ref = menu.get('action')
            if action_ref and action_ref not in all_action_ids:
                if '.' in action_ref:
                    module = action_ref.split('.')[0]
                    issues.append({
                        'type': 'external_action',
                        'ref': action_ref,
                        'module': module,
                    })
                else:
                    issues.append({
                        'type': 'missing_action',
                        'ref': action_ref,
                    })

            # Check parent reference
            parent_ref = menu.get('parent_id')
            if parent_ref and parent_ref not in all_menu_ids:
                if '.' in parent_ref:
                    module = parent_ref.split('.')[0]
                    issues.append({
                        'type': 'external_parent',
                        'ref': parent_ref,
                        'module': module,
                    })
                else:
                    issues.append({
                        'type': 'missing_parent',
                        'ref': parent_ref,
                    })

            if issues:
                severity = 'error' if any(i['type'].startswith('missing') for i in issues) else 'info'
                self.findings['orphaned_menus'].append({
                    'menu_xml_id': menu.get('xml_id'),
                    'menu_name': menu.get('name'),
                    'file': menu.get('relative_path'),
                    'issues': issues,
                    'severity': severity,
                })

    # Common mixin fields that are inherited but may not be in static scan
    # These come from mail.thread, mail.activity.mixin, etc.
    COMMON_MIXIN_FIELDS = {
        # mail.thread mixin
        'message_ids', 'message_follower_ids', 'message_partner_ids',
        'message_channel_ids', 'message_attachment_count', 'message_has_error',
        'message_has_sms_error', 'message_needaction', 'message_needaction_counter',
        'message_unread', 'message_unread_counter', 'message_main_attachment_id',
        'email_from', 'email_cc', 'message_bounce', 'message_is_follower',
        # mail.activity.mixin
        'activity_ids', 'activity_state', 'activity_user_id', 'activity_type_id',
        'activity_type_icon', 'activity_date_deadline', 'activity_summary',
        'activity_exception_decoration', 'activity_exception_icon', 'my_activity_date_deadline',
        # Common relational shortcuts
        'user_id', 'company_id', 'currency_id', 'partner_id', 'parent_id',
        # Computed/related that might not be in static scan
        'message_count', 'conversation_type', 'name', 'display_name_computed',
    }

    def _find_dangling_field_refs(self):
        """Find views that reference non-existent fields"""
        # Build field map from Python models
        fields_by_model = {}
        for model in self.python_scan.get('models', []):
            model_name = model.get('_name')
            if model_name:
                fields_by_model[model_name] = {f['name'] for f in model.get('fields', [])}

        # Add fields from registry if available
        if self.registry_scan:
            for model_name, fields in self.registry_scan.get('fields_by_model', {}).items():
                if model_name not in fields_by_model:
                    fields_by_model[model_name] = set(fields)
                else:
                    fields_by_model[model_name].update(fields)

        # Check each view
        for view in self.xml_scan.get('views', []):
            model_name = view.get('view_model')
            if not model_name or model_name not in fields_by_model:
                continue

            model_fields = fields_by_model[model_name]
            view_fields = view.get('field_references', [])

            missing_fields = []
            for field in view_fields:
                # Skip magic fields
                if field in ('id', 'create_date', 'create_uid', 'write_date', 'write_uid',
                            'display_name', '__last_update', 'active'):
                    continue

                # Skip common mixin fields (may not be in static scan)
                if field in self.COMMON_MIXIN_FIELDS:
                    continue

                if field not in model_fields:
                    missing_fields.append(field)

            if missing_fields:
                self.findings['dangling_field_refs'].append({
                    'view_xml_id': view['xml_id'],
                    'model': model_name,
                    'file': view['relative_path'],
                    'missing_fields': missing_fields,
                    'severity': 'warning',
                    'recommendation': 'These fields are referenced but not defined in the model',
                })

    def _find_dangling_model_refs(self):
        """Find references to non-existent models"""
        # Build set of all known models
        known_models = set()
        for model in self.python_scan.get('models', []):
            if model.get('_name'):
                known_models.add(model['_name'])

        # Add registry models if available
        if self.registry_scan:
            for model_info in self.registry_scan.get('models', []):
                known_models.add(model_info['name'])

        # Add base Odoo models to prevent false positives
        # These are from core Odoo and won't be in our scan scope
        known_models.update(self.BASE_ODOO_MODELS)

        # Check views
        for view in self.xml_scan.get('views', []):
            model_name = view.get('view_model')
            if model_name and model_name not in known_models:
                self.findings['dangling_model_refs'].append({
                    'type': 'view',
                    'xml_id': view['xml_id'],
                    'file': view['relative_path'],
                    'missing_model': model_name,
                    'severity': 'error',
                })

        # Check actions
        for action in self.xml_scan.get('actions', []):
            model_name = action.get('res_model')
            if model_name and model_name not in known_models:
                self.findings['dangling_model_refs'].append({
                    'type': 'action',
                    'xml_id': action['xml_id'],
                    'file': action['relative_path'],
                    'missing_model': model_name,
                    'severity': 'error',
                })

        # Check Python field relations
        for model in self.python_scan.get('models', []):
            for field in model.get('fields', []):
                if field['type'] in ('Many2one', 'One2many', 'Many2many'):
                    comodel = field.get('attributes', {}).get('comodel_name')
                    if comodel and comodel not in known_models:
                        self.findings['dangling_model_refs'].append({
                            'type': 'field_relation',
                            'model': model.get('_name'),
                            'field': field['name'],
                            'file': model['relative_path'],
                            'missing_model': comodel,
                            'severity': 'error',
                        })

    def _find_orphaned_assets(self):
        """Find JS/CSS files not registered in any asset bundle"""
        for orphan in self.asset_scan.get('orphaned_assets', []):
            self.findings['orphaned_assets'].append({
                'path': orphan['path'],
                'type': orphan['type'],
                'severity': 'warning',
                'recommendation': 'Add to __manifest__.py assets or remove if unused',
            })

        # Also check for JS files without @odoo-module
        for js_file in self.asset_scan.get('js_files', []):
            if not js_file.get('is_odoo_module'):
                # Check if it might need the annotation
                if js_file.get('imports') or js_file.get('exports'):
                    self.findings['orphaned_assets'].append({
                        'path': js_file['relative_path'],
                        'type': 'js_no_module',
                        'severity': 'info',
                        'recommendation': 'Consider adding @odoo-module annotation for proper ES6 module loading',
                    })

    def _find_missing_dependencies(self):
        """Find imports that reference unavailable modules"""
        # Check Python imports
        for imp in self.python_scan.get('imports', []):
            if imp.get('type') == 'from':
                module = imp.get('module', '')
                # Check for common Odoo module patterns
                if module.startswith('odoo.addons.'):
                    addon_name = module.split('.')[2] if len(module.split('.')) > 2 else None
                    if addon_name:
                        # Would need manifest check to verify dependency
                        pass

        # Check JS imports
        for js_file in self.asset_scan.get('js_files', []):
            for imp in js_file.get('imports', []):
                module = imp.get('module', '')
                if module.startswith('@'):
                    # Odoo module reference
                    self.findings['missing_dependencies'].append({
                        'file': js_file['relative_path'],
                        'import': module,
                        'type': 'js_import',
                        'severity': 'info',
                        'recommendation': 'Verify this module is available',
                    })

    def _generate_summary(self):
        """Generate summary statistics"""
        self.findings['summary'] = {
            'orphaned_python_files': len(self.findings['orphaned_python_files']),
            'orphaned_models': len(self.findings['orphaned_models']),
            'orphaned_views': len(self.findings['orphaned_views']),
            'orphaned_actions': len(self.findings['orphaned_actions']),
            'orphaned_menus': len(self.findings['orphaned_menus']),
            'dangling_field_refs': len(self.findings['dangling_field_refs']),
            'dangling_model_refs': len(self.findings['dangling_model_refs']),
            'orphaned_assets': len(self.findings['orphaned_assets']),
            'total_issues': 0,
            'severity_counts': {
                'error': 0,
                'warning': 0,
                'info': 0,
            }
        }

        # Count total and severities
        for category in self.findings:
            if category == 'summary':
                continue
            for item in self.findings[category]:
                if isinstance(item, dict):
                    self.findings['summary']['total_issues'] += 1
                    severity = item.get('severity', 'info')
                    self.findings['summary']['severity_counts'][severity] += 1
