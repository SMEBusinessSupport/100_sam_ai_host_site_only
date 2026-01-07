# -*- coding: utf-8 -*-
"""
XML Scanner for SAM AI Insights

Scans XML files to extract:
- View definitions (form, tree, kanban, search, graph, pivot, calendar)
- Actions (ir.actions.act_window, ir.actions.server, etc.)
- Menu items (ir.ui.menu)
- Data records (any model records defined in XML)
- Field references within views
- Inherited views and XPath modifications
"""
import os
import re
from pathlib import Path
from typing import Dict, List, Any, Optional, Set
from xml.etree import ElementTree as ET
import logging

_logger = logging.getLogger(__name__)


class XMLScanner:
    """Scanner for Odoo XML files (views, actions, menus, data)"""

    # Odoo view types
    VIEW_TYPES = ('form', 'tree', 'kanban', 'search', 'graph', 'pivot',
                  'calendar', 'gantt', 'cohort', 'activity', 'qweb')

    # Action types
    ACTION_MODELS = (
        'ir.actions.act_window',
        'ir.actions.server',
        'ir.actions.report',
        'ir.actions.client',
        'ir.actions.act_url',
    )

    def __init__(self, base_path: str, module_filter: Optional[List[str]] = None):
        self.base_path = Path(base_path)
        self.module_filter = module_filter or []
        self.scan_results = {
            'views': [],
            'actions': [],
            'menus': [],
            'records': [],
            'templates': [],
            'field_references': [],
            'inherited_views': [],
            'files_scanned': 0,
            'errors': [],
        }
        # Track field references for dangling detection
        self._field_refs = {}  # model -> set of field names

    def scan(self) -> Dict[str, Any]:
        """Scan all XML files in the base path"""
        _logger.info(f"Starting XML scan of {self.base_path}")

        for xml_file in self.base_path.rglob('*.xml'):
            # Skip if module filter is set
            if self.module_filter:
                # Get the relative path and extract the top-level module name
                try:
                    rel_path = xml_file.relative_to(self.base_path)
                    top_module = rel_path.parts[0] if rel_path.parts else ''
                    # Check for exact module match (not substring)
                    if top_module not in self.module_filter:
                        continue
                except ValueError:
                    continue

            # Skip common non-Odoo XML
            if '.git' in str(xml_file) or 'node_modules' in str(xml_file):
                continue

            self._scan_file(xml_file)

        # Build field reference summary
        self.scan_results['field_usage_by_model'] = {
            model: list(fields) for model, fields in self._field_refs.items()
        }

        _logger.info(f"XML scan complete: {self.scan_results['files_scanned']} files, "
                    f"{len(self.scan_results['views'])} views, "
                    f"{len(self.scan_results['actions'])} actions, "
                    f"{len(self.scan_results['menus'])} menus")

        return self.scan_results

    def _scan_file(self, file_path: Path):
        """Scan a single XML file"""
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
            rel_path = str(file_path.relative_to(self.base_path))

            # Handle different root elements
            if root.tag == 'odoo':
                self._process_odoo_root(root, rel_path, file_path)
            elif root.tag == 'openerp':
                # Legacy format
                for data in root.findall('.//data'):
                    self._process_data_element(data, rel_path, file_path)
            elif root.tag == 'templates':
                self._process_templates(root, rel_path, file_path)

            self.scan_results['files_scanned'] += 1

        except ET.ParseError as e:
            self.scan_results['errors'].append({
                'file': str(file_path),
                'error': f'XML parse error: {e}',
            })
        except Exception as e:
            self.scan_results['errors'].append({
                'file': str(file_path),
                'error': str(e),
            })

    def _process_odoo_root(self, root: ET.Element, rel_path: str, file_path: Path):
        """Process <odoo> root element"""
        # Process direct children and data elements
        for child in root:
            if child.tag == 'data':
                self._process_data_element(child, rel_path, file_path)
            elif child.tag == 'record':
                self._process_record(child, rel_path, file_path)
            elif child.tag == 'menuitem':
                self._process_menuitem(child, rel_path, file_path)
            elif child.tag == 'template':
                self._process_template(child, rel_path, file_path)
            elif child.tag == 'function':
                self._process_function_call(child, rel_path, file_path)
            elif child.tag == 'delete':
                self._process_delete(child, rel_path, file_path)

    def _process_data_element(self, data: ET.Element, rel_path: str, file_path: Path):
        """Process <data> element containing records"""
        noupdate = data.get('noupdate', '0') == '1'

        for child in data:
            if child.tag == 'record':
                self._process_record(child, rel_path, file_path, noupdate)
            elif child.tag == 'menuitem':
                self._process_menuitem(child, rel_path, file_path)
            elif child.tag == 'template':
                self._process_template(child, rel_path, file_path)
            elif child.tag == 'function':
                self._process_function_call(child, rel_path, file_path)
            elif child.tag == 'delete':
                self._process_delete(child, rel_path, file_path)

    def _process_record(self, record: ET.Element, rel_path: str, file_path: Path,
                       noupdate: bool = False):
        """Process a <record> element"""
        model = record.get('model', '')
        xml_id = record.get('id', '')

        record_info = {
            'xml_id': xml_id,
            'model': model,
            'file_path': str(file_path),
            'relative_path': rel_path,
            'noupdate': noupdate,
            'fields': {},
        }

        # Extract field values
        for field in record.findall('field'):
            field_name = field.get('name', '')
            field_info = self._extract_field_value(field)
            record_info['fields'][field_name] = field_info

        # Categorize by type
        if model == 'ir.ui.view':
            view_info = self._process_view_record(record, record_info)
            if view_info:
                self.scan_results['views'].append(view_info)
        elif model in self.ACTION_MODELS:
            action_info = self._process_action_record(record, record_info)
            self.scan_results['actions'].append(action_info)
        elif model == 'ir.ui.menu':
            menu_info = self._process_menu_record(record, record_info)
            self.scan_results['menus'].append(menu_info)
        else:
            self.scan_results['records'].append(record_info)

    def _extract_field_value(self, field: ET.Element) -> Dict[str, Any]:
        """Extract field value from XML field element"""
        result = {
            'name': field.get('name', ''),
            'value': None,
            'ref': field.get('ref'),
            'eval': field.get('eval'),
            'type': field.get('type'),
        }

        # Text content
        if field.text:
            result['value'] = field.text.strip()

        # Embedded XML (for arch fields)
        if len(field) > 0:
            # This is likely an arch field with embedded view definition
            result['has_arch'] = True
            result['arch_elements'] = len(field)

        return result

    def _process_view_record(self, record: ET.Element, record_info: Dict) -> Optional[Dict]:
        """Process an ir.ui.view record"""
        view_info = {
            **record_info,
            'type': 'view',
            'view_type': None,
            'view_model': None,
            'inherit_id': None,
            'priority': 16,
            'field_references': [],
            'xpath_operations': [],
        }

        for field in record.findall('field'):
            name = field.get('name', '')

            if name == 'type':
                view_info['view_type'] = field.text or field.get('eval', '').strip("'\"")
            elif name == 'model':
                view_info['view_model'] = field.text
            elif name == 'inherit_id':
                view_info['inherit_id'] = field.get('ref')
            elif name == 'priority':
                try:
                    view_info['priority'] = int(field.text or field.get('eval', '16'))
                except ValueError:
                    pass
            elif name == 'arch':
                # Parse the arch to extract field references
                arch_info = self._parse_view_arch(field)
                view_info['field_references'] = arch_info.get('fields', [])
                view_info['xpath_operations'] = arch_info.get('xpaths', [])
                view_info['view_type'] = view_info['view_type'] or arch_info.get('view_type')

                # Track field references by model
                if view_info['view_model']:
                    if view_info['view_model'] not in self._field_refs:
                        self._field_refs[view_info['view_model']] = set()
                    self._field_refs[view_info['view_model']].update(arch_info.get('fields', []))

        # Track inherited views
        if view_info['inherit_id']:
            self.scan_results['inherited_views'].append({
                'xml_id': view_info['xml_id'],
                'inherit_id': view_info['inherit_id'],
                'model': view_info['view_model'],
                'file': view_info['relative_path'],
                'xpath_count': len(view_info['xpath_operations']),
            })

        return view_info

    def _parse_view_arch(self, arch_field: ET.Element) -> Dict[str, Any]:
        """Parse view architecture to extract field references and structure"""
        result = {
            'fields': [],
            'xpaths': [],
            'view_type': None,
            'buttons': [],
            'groups': [],
        }

        def extract_from_element(elem):
            # Determine view type from root element
            if elem.tag in self.VIEW_TYPES:
                result['view_type'] = elem.tag

            # Extract field references
            if elem.tag == 'field':
                field_name = elem.get('name')
                if field_name:
                    result['fields'].append(field_name)

            # Extract XPath operations (for inherited views)
            if elem.tag == 'xpath':
                result['xpaths'].append({
                    'expr': elem.get('expr', ''),
                    'position': elem.get('position', 'inside'),
                })

            # Extract buttons
            if elem.tag == 'button':
                result['buttons'].append({
                    'name': elem.get('name'),
                    'type': elem.get('type'),
                    'string': elem.get('string'),
                })

            # Extract groups (access control)
            groups = elem.get('groups')
            if groups:
                result['groups'].extend(groups.split(','))

            # Also check for field references in attrs and domain attributes
            # NOTE: Exclude 'context' and 'options' - these contain config keys like
            # 'group_by', 'mode', 'json' which are NOT field names
            for attr in ('attrs', 'domain'):
                attr_val = elem.get(attr, '')
                # Find field references in domain/attrs expressions
                # Domain format: [('field_name', '=', value)]
                # Attrs format: {'invisible': [('field_name', '=', value)]}
                field_refs = re.findall(r"'(\w+)'", attr_val)
                # Filter out operators and common non-field values
                excluded_values = {
                    # Operators
                    '=', '!=', '<', '>', '<=', '>=', 'in', 'not in', 'like', 'ilike',
                    'child_of', 'parent_of', '=?', '=like', '=ilike',
                    # Domain combinators
                    'and', 'or', '&', '|', '!',
                    # Common context/option keys (not fields)
                    'group_by', 'mode', 'json', 'tree_view_ref', 'form_view_ref',
                    'default_provider_id', 'default_is_template', 'force_no_record_check',
                    'default_vendor_key', 'no_open', 'no_create', 'no_edit', 'no_delete',
                    # Boolean values
                    'True', 'False', 'true', 'false', 'None',
                }
                result['fields'].extend(
                    f for f in field_refs
                    if not f.startswith('_') and f not in excluded_values
                )

            for child in elem:
                extract_from_element(child)

        for child in arch_field:
            extract_from_element(child)

        # Deduplicate
        result['fields'] = list(set(result['fields']))
        result['groups'] = list(set(result['groups']))

        return result

    def _process_action_record(self, record: ET.Element, record_info: Dict) -> Dict:
        """Process an action record"""
        action_info = {
            **record_info,
            'type': 'action',
            'action_type': record_info['model'],
            'res_model': None,
            'view_id': None,
            'view_ids': [],
            'domain': None,
            'context': None,
            'target': 'current',
        }

        for field in record.findall('field'):
            name = field.get('name', '')

            if name == 'res_model':
                action_info['res_model'] = field.text
            elif name == 'view_id':
                action_info['view_id'] = field.get('ref')
            elif name == 'view_ids':
                # Parse view_ids eval
                eval_str = field.get('eval', '')
                refs = re.findall(r"ref\(['\"]([^'\"]+)['\"]\)", eval_str)
                action_info['view_ids'] = refs
            elif name == 'domain':
                action_info['domain'] = field.text or field.get('eval')
            elif name == 'context':
                action_info['context'] = field.text or field.get('eval')
            elif name == 'target':
                action_info['target'] = field.text

        return action_info

    def _process_menu_record(self, record: ET.Element, record_info: Dict) -> Dict:
        """Process an ir.ui.menu record"""
        menu_info = {
            **record_info,
            'type': 'menu',
            'name': None,
            'parent_id': None,
            'action': None,
            'sequence': 10,
            'groups': [],
        }

        for field in record.findall('field'):
            name = field.get('name', '')

            if name == 'name':
                menu_info['name'] = field.text
            elif name == 'parent_id':
                menu_info['parent_id'] = field.get('ref')
            elif name == 'action':
                menu_info['action'] = field.get('ref')
            elif name == 'sequence':
                try:
                    menu_info['sequence'] = int(field.text or field.get('eval', '10'))
                except ValueError:
                    pass
            elif name == 'groups_id':
                eval_str = field.get('eval', '')
                refs = re.findall(r"ref\(['\"]([^'\"]+)['\"]\)", eval_str)
                menu_info['groups'] = refs

        return menu_info

    def _process_menuitem(self, menuitem: ET.Element, rel_path: str, file_path: Path):
        """Process a <menuitem> shortcut element"""
        menu_info = {
            'xml_id': menuitem.get('id', ''),
            'model': 'ir.ui.menu',
            'file_path': str(file_path),
            'relative_path': rel_path,
            'type': 'menu',
            'name': menuitem.get('name'),
            'parent_id': menuitem.get('parent'),
            'action': menuitem.get('action'),
            'sequence': int(menuitem.get('sequence', '10')),
            'groups': menuitem.get('groups', '').split(',') if menuitem.get('groups') else [],
            'web_icon': menuitem.get('web_icon'),
        }

        self.scan_results['menus'].append(menu_info)

    def _process_template(self, template: ET.Element, rel_path: str, file_path: Path):
        """Process a <template> (QWeb) element"""
        template_info = {
            'xml_id': template.get('id', ''),
            't_name': template.get('t-name'),
            'inherit_id': template.get('inherit_id'),
            'priority': template.get('priority', '16'),
            'file_path': str(file_path),
            'relative_path': rel_path,
            'type': 'template',
        }

        self.scan_results['templates'].append(template_info)

    def _process_templates(self, templates: ET.Element, rel_path: str, file_path: Path):
        """Process a <templates> root element"""
        for template in templates:
            if template.tag in ('t', 'template'):
                self._process_template(template, rel_path, file_path)

    def _process_function_call(self, func: ET.Element, rel_path: str, file_path: Path):
        """Process a <function> element (model method call)"""
        self.scan_results['records'].append({
            'type': 'function_call',
            'model': func.get('model'),
            'name': func.get('name'),
            'file_path': str(file_path),
            'relative_path': rel_path,
        })

    def _process_delete(self, delete: ET.Element, rel_path: str, file_path: Path):
        """Process a <delete> element"""
        self.scan_results['records'].append({
            'type': 'delete',
            'model': delete.get('model'),
            'id': delete.get('id'),
            'search': delete.get('search'),
            'file_path': str(file_path),
            'relative_path': rel_path,
        })

    def get_view_by_xml_id(self, xml_id: str) -> Optional[Dict]:
        """Find a view by its XML ID"""
        for view in self.scan_results['views']:
            if view['xml_id'] == xml_id:
                return view
        return None

    def get_views_for_model(self, model_name: str) -> List[Dict]:
        """Get all views for a specific model"""
        return [v for v in self.scan_results['views'] if v.get('view_model') == model_name]

    def get_actions_for_model(self, model_name: str) -> List[Dict]:
        """Get all actions for a specific model"""
        return [a for a in self.scan_results['actions'] if a.get('res_model') == model_name]

    def get_orphaned_menus(self) -> List[Dict]:
        """Find menu items with missing actions or parents"""
        action_ids = {a['xml_id'] for a in self.scan_results['actions']}
        menu_ids = {m['xml_id'] for m in self.scan_results['menus']}

        orphaned = []
        for menu in self.scan_results['menus']:
            issues = []
            if menu.get('action') and menu['action'] not in action_ids:
                issues.append(f"Missing action: {menu['action']}")
            if menu.get('parent_id') and menu['parent_id'] not in menu_ids:
                # Could be from another module, so just flag it
                issues.append(f"Parent from other module: {menu['parent_id']}")

            if issues:
                orphaned.append({**menu, 'issues': issues})

        return orphaned
