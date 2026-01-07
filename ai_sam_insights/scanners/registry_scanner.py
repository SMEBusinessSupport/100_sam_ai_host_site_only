# -*- coding: utf-8 -*-
"""
Registry Scanner for SAM AI Insights

Scans the Odoo runtime registry to extract:
- All installed models and their fields
- View definitions from ir.ui.view
- Actions from ir.actions.*
- Menus from ir.ui.menu
- Compares runtime state with static analysis
"""
from typing import Dict, List, Any, Optional
import logging

_logger = logging.getLogger(__name__)


class RegistryScanner:
    """Scanner that queries Odoo's runtime registry for installed components"""

    def __init__(self, env):
        """
        Initialize with Odoo environment

        :param env: Odoo Environment (from self.env in a model)
        """
        self.env = env
        self.scan_results = {
            'models': [],
            'views': [],
            'actions': [],
            'menus': [],
            'fields_by_model': {},
            'module_info': [],
            'errors': [],
        }

    def scan(self, module_filter: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Scan the Odoo registry

        :param module_filter: Optional list of module names to filter by
        """
        _logger.info("Starting Odoo registry scan")

        try:
            self._scan_models(module_filter)
            self._scan_views(module_filter)
            self._scan_actions(module_filter)
            self._scan_menus(module_filter)
            self._scan_modules(module_filter)
        except Exception as e:
            self.scan_results['errors'].append({
                'stage': 'registry_scan',
                'error': str(e),
            })
            _logger.exception("Error during registry scan")

        _logger.info(f"Registry scan complete: {len(self.scan_results['models'])} models, "
                    f"{len(self.scan_results['views'])} views, "
                    f"{len(self.scan_results['actions'])} actions")

        return self.scan_results

    def _scan_models(self, module_filter: Optional[List[str]] = None):
        """Scan all installed models"""
        IrModel = self.env['ir.model'].sudo()
        IrModelFields = self.env['ir.model.fields'].sudo()

        domain = [('transient', '=', False)]
        if module_filter:
            # Filter by modules that define the model
            domain.append(('modules', 'in', module_filter))

        models = IrModel.search(domain)

        for model in models:
            model_info = {
                'id': model.id,
                'name': model.model,
                'display_name': model.name,
                'is_transient': model.transient,
                'modules': model.modules,
                'state': model.state,
                'field_count': len(model.field_id),
                'fields': [],
            }

            # Get field details
            for field in model.field_id:
                field_info = {
                    'name': field.name,
                    'type': field.ttype,
                    'string': field.field_description,
                    'required': field.required,
                    'readonly': field.readonly,
                    'store': field.store,
                    'relation': field.relation,
                    'relation_field': field.relation_field,
                    'compute': field.compute or None,
                    'depends': field.depends or None,
                    'modules': field.modules,
                }
                model_info['fields'].append(field_info)

            self.scan_results['models'].append(model_info)
            self.scan_results['fields_by_model'][model.model] = [
                f['name'] for f in model_info['fields']
            ]

    def _scan_views(self, module_filter: Optional[List[str]] = None):
        """Scan all views"""
        IrUIView = self.env['ir.ui.view'].sudo()

        domain = []
        if module_filter:
            # Views don't have a direct module field, but we can filter by xml_id
            pass  # Will filter by xml_id prefix

        views = IrUIView.search(domain, order='model, priority')

        for view in views:
            xml_id = view.get_external_id().get(view.id, '')

            # Apply module filter if set
            if module_filter:
                if not any(xml_id.startswith(m + '.') for m in module_filter):
                    continue

            view_info = {
                'id': view.id,
                'xml_id': xml_id,
                'name': view.name,
                'model': view.model,
                'type': view.type,
                'priority': view.priority,
                'inherit_id': view.inherit_id.id if view.inherit_id else None,
                'inherit_xml_id': view.inherit_id.get_external_id().get(view.inherit_id.id, '') if view.inherit_id else None,
                'active': view.active,
                'mode': view.mode,
                'arch_db': view.arch_db[:500] if view.arch_db else None,  # Truncate for storage
            }

            self.scan_results['views'].append(view_info)

    def _scan_actions(self, module_filter: Optional[List[str]] = None):
        """Scan all actions"""
        action_models = [
            'ir.actions.act_window',
            'ir.actions.server',
            'ir.actions.report',
            'ir.actions.client',
            'ir.actions.act_url',
        ]

        for action_model in action_models:
            try:
                Action = self.env[action_model].sudo()
                actions = Action.search([])

                for action in actions:
                    xml_id = action.get_external_id().get(action.id, '')

                    # Apply module filter if set
                    if module_filter:
                        if not any(xml_id.startswith(m + '.') for m in module_filter):
                            continue

                    action_info = {
                        'id': action.id,
                        'xml_id': xml_id,
                        'name': action.name,
                        'type': action_model,
                    }

                    # Add type-specific fields
                    if action_model == 'ir.actions.act_window':
                        action_info.update({
                            'res_model': action.res_model,
                            'view_mode': action.view_mode,
                            'domain': str(action.domain) if action.domain else None,
                            'context': str(action.context) if action.context else None,
                            'target': action.target,
                            'view_id': action.view_id.id if action.view_id else None,
                        })
                    elif action_model == 'ir.actions.server':
                        action_info.update({
                            'model_id': action.model_id.id,
                            'model_name': action.model_id.model,
                            'state': action.state,
                        })
                    elif action_model == 'ir.actions.report':
                        action_info.update({
                            'model': action.model,
                            'report_type': action.report_type,
                            'report_name': action.report_name,
                        })

                    self.scan_results['actions'].append(action_info)

            except Exception as e:
                self.scan_results['errors'].append({
                    'stage': f'scan_{action_model}',
                    'error': str(e),
                })

    def _scan_menus(self, module_filter: Optional[List[str]] = None):
        """Scan all menus"""
        IrUIMenu = self.env['ir.ui.menu'].sudo()

        menus = IrUIMenu.search([], order='parent_id, sequence')

        for menu in menus:
            xml_id = menu.get_external_id().get(menu.id, '')

            # Apply module filter if set
            if module_filter:
                if not any(xml_id.startswith(m + '.') for m in module_filter):
                    continue

            action_info = None
            if menu.action:
                action_info = {
                    'id': menu.action.id,
                    'type': menu.action._name,
                    'xml_id': menu.action.get_external_id().get(menu.action.id, ''),
                }

            menu_info = {
                'id': menu.id,
                'xml_id': xml_id,
                'name': menu.name,
                'sequence': menu.sequence,
                'parent_id': menu.parent_id.id if menu.parent_id else None,
                'parent_xml_id': menu.parent_id.get_external_id().get(menu.parent_id.id, '') if menu.parent_id else None,
                'action': action_info,
                'groups': [g.get_external_id().get(g.id, '') for g in menu.groups_id],
                'active': menu.active if hasattr(menu, 'active') else True,
            }

            self.scan_results['menus'].append(menu_info)

    def _scan_modules(self, module_filter: Optional[List[str]] = None):
        """Scan installed modules"""
        IrModule = self.env['ir.module.module'].sudo()

        domain = [('state', '=', 'installed')]
        if module_filter:
            domain.append(('name', 'in', module_filter))

        modules = IrModule.search(domain)

        for module in modules:
            module_info = {
                'id': module.id,
                'name': module.name,
                'display_name': module.shortdesc,
                'version': module.installed_version,
                'category': module.category_id.name if module.category_id else None,
                'author': module.author,
                'state': module.state,
                'dependencies': [dep.name for dep in module.dependencies_id],
            }

            self.scan_results['module_info'].append(module_info)

    def get_model_fields(self, model_name: str) -> List[str]:
        """Get all field names for a model from registry"""
        return self.scan_results['fields_by_model'].get(model_name, [])

    def get_views_for_model(self, model_name: str) -> List[Dict]:
        """Get all views for a model"""
        return [v for v in self.scan_results['views'] if v['model'] == model_name]

    def find_dangling_view_references(self, python_models: List[str]) -> List[Dict]:
        """
        Find views that reference non-existent models

        :param python_models: List of model names from Python scan
        """
        registry_models = set(self.scan_results['fields_by_model'].keys())
        all_known_models = registry_models | set(python_models)

        dangling = []
        for view in self.scan_results['views']:
            if view['model'] and view['model'] not in all_known_models:
                dangling.append({
                    'view_xml_id': view['xml_id'],
                    'view_name': view['name'],
                    'missing_model': view['model'],
                })

        return dangling

    def find_orphaned_menus(self) -> List[Dict]:
        """Find menus with missing actions or parents"""
        action_ids = {a['id'] for a in self.scan_results['actions']}
        menu_ids = {m['id'] for m in self.scan_results['menus']}

        orphaned = []
        for menu in self.scan_results['menus']:
            issues = []

            if menu['action'] and menu['action']['id'] not in action_ids:
                issues.append(f"Missing action ID: {menu['action']['id']}")

            if menu['parent_id'] and menu['parent_id'] not in menu_ids:
                issues.append(f"Missing parent ID: {menu['parent_id']}")

            if issues:
                orphaned.append({
                    'menu_xml_id': menu['xml_id'],
                    'menu_name': menu['name'],
                    'issues': issues,
                })

        return orphaned
