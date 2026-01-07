# -*- coding: utf-8 -*-
"""
Relationship Mapper for SAM AI Insights

Maps relationships between:
- Models → Views → Actions → Menus (full trace)
- Model inheritance chains
- Field relations (Many2one, One2many, Many2many)
- JS components → Python controllers
- Module dependencies
"""
from typing import Dict, List, Any, Set, Optional, Tuple
from collections import defaultdict
import logging

_logger = logging.getLogger(__name__)


class RelationshipMapper:
    """Maps relationships between all ecosystem components"""

    def __init__(self, python_scan: Dict, xml_scan: Dict, asset_scan: Dict,
                 registry_scan: Optional[Dict] = None):
        self.python_scan = python_scan
        self.xml_scan = xml_scan
        self.asset_scan = asset_scan
        self.registry_scan = registry_scan or {}

        self.relationships = {
            'model_to_views': {},       # model -> [view_ids]
            'model_to_actions': {},     # model -> [action_ids]
            'model_to_menus': {},       # model -> [menu_ids] (via actions)
            'model_inheritance': {},     # model -> [parent_models]
            'model_relations': {},       # model -> {field: related_model}
            'view_inheritance': {},      # view -> [parent_view_ids]
            'action_to_menus': {},       # action -> [menu_ids]
            'js_to_python': {},          # js_component -> [python_models/controllers]
            'module_dependencies': {},   # module -> [dependent_modules]
            'full_traces': [],           # Complete model->view->action->menu traces
            'dependency_graph': {},      # Full dependency graph
            'summary': {},
        }

    def map(self) -> Dict[str, Any]:
        """Build all relationship maps"""
        _logger.info("Starting relationship mapping")

        self._map_model_to_views()
        self._map_model_to_actions()
        self._map_model_inheritance()
        self._map_model_relations()
        self._map_view_inheritance()
        self._map_action_to_menus()
        self._map_model_to_menus()
        self._map_js_to_python()
        self._build_full_traces()
        self._build_dependency_graph()
        self._generate_summary()

        _logger.info(f"Relationship mapping complete: {self.relationships['summary']}")

        return self.relationships

    def _map_model_to_views(self):
        """Map models to their views"""
        model_views = defaultdict(list)

        for view in self.xml_scan.get('views', []):
            model = view.get('view_model')
            if model:
                model_views[model].append({
                    'xml_id': view['xml_id'],
                    'type': view.get('view_type'),
                    'inherit_id': view.get('inherit_id'),
                    'file': view.get('relative_path'),
                    'priority': view.get('priority', 16),
                })

        self.relationships['model_to_views'] = dict(model_views)

    def _map_model_to_actions(self):
        """Map models to their actions"""
        model_actions = defaultdict(list)

        for action in self.xml_scan.get('actions', []):
            model = action.get('res_model')
            if model:
                model_actions[model].append({
                    'xml_id': action['xml_id'],
                    'type': action.get('action_type'),
                    'file': action.get('relative_path'),
                })

        self.relationships['model_to_actions'] = dict(model_actions)

    def _map_model_inheritance(self):
        """Map model inheritance chains"""
        inheritance = {}

        for model in self.python_scan.get('models', []):
            model_name = model.get('_name')
            if not model_name:
                continue

            parents = []

            # Direct _inherit
            for inherit in model.get('_inherit', []):
                parents.append({
                    'model': inherit,
                    'type': 'inherit',
                })

            # Class bases (Python inheritance)
            for base in model.get('bases', []):
                if base not in ('models.Model', 'models.TransientModel', 'models.AbstractModel',
                               'Model', 'TransientModel', 'AbstractModel'):
                    parents.append({
                        'model': base,
                        'type': 'class_base',
                    })

            if parents:
                inheritance[model_name] = parents

        self.relationships['model_inheritance'] = inheritance

    def _map_model_relations(self):
        """Map relational fields between models"""
        relations = defaultdict(dict)

        for model in self.python_scan.get('models', []):
            model_name = model.get('_name')
            if not model_name:
                continue

            for field in model.get('fields', []):
                if field['type'] in ('Many2one', 'One2many', 'Many2many'):
                    comodel = field.get('attributes', {}).get('comodel_name')
                    if comodel:
                        relations[model_name][field['name']] = {
                            'type': field['type'],
                            'comodel': comodel,
                            'inverse': field.get('attributes', {}).get('inverse_name'),
                        }

        self.relationships['model_relations'] = dict(relations)

    def _map_view_inheritance(self):
        """Map view inheritance chains"""
        inheritance = {}

        for view in self.xml_scan.get('views', []):
            if view.get('inherit_id'):
                inheritance[view['xml_id']] = {
                    'parent': view['inherit_id'],
                    'model': view.get('view_model'),
                    'xpath_count': len(view.get('xpath_operations', [])),
                }

        self.relationships['view_inheritance'] = inheritance

    def _map_action_to_menus(self):
        """Map actions to menus that reference them"""
        action_menus = defaultdict(list)

        for menu in self.xml_scan.get('menus', []):
            action_ref = menu.get('action')
            if action_ref:
                action_menus[action_ref].append({
                    'xml_id': menu.get('xml_id'),
                    'name': menu.get('name'),
                    'parent_id': menu.get('parent_id'),
                    'sequence': menu.get('sequence'),
                })

        self.relationships['action_to_menus'] = dict(action_menus)

    def _map_model_to_menus(self):
        """Map models to menus (via actions)"""
        model_menus = defaultdict(list)

        # Build action -> model map
        action_models = {}
        for action in self.xml_scan.get('actions', []):
            if action.get('xml_id') and action.get('res_model'):
                action_models[action['xml_id']] = action['res_model']

        # Map menus to models via actions
        for action_id, menus in self.relationships['action_to_menus'].items():
            model = action_models.get(action_id)
            if model:
                for menu in menus:
                    model_menus[model].append({
                        **menu,
                        'via_action': action_id,
                    })

        self.relationships['model_to_menus'] = dict(model_menus)

    def _map_js_to_python(self):
        """Map JS components to Python models/controllers they interact with"""
        js_python = defaultdict(list)

        # Find RPC calls and model references in JS
        for js_file in self.asset_scan.get('js_files', []):
            # Check imports for model references
            for imp in js_file.get('imports', []):
                module = imp.get('module', '')
                if 'models' in module.lower() or 'service' in module.lower():
                    js_python[js_file['relative_path']].append({
                        'type': 'import',
                        'target': module,
                    })

            # Check registry additions (often model-related)
            pass  # Would need content analysis

        # Check controller endpoints
        for func in self.python_scan.get('functions', []):
            decorators = func.get('decorators', [])
            if any('route' in d.lower() for d in decorators):
                # This is a controller endpoint
                route_info = {
                    'controller': func.get('class_name'),
                    'method': func['name'],
                    'file': func.get('relative_path'),
                }
                # Would need to match with JS fetch/RPC calls
                pass

        self.relationships['js_to_python'] = dict(js_python)

    def _build_full_traces(self):
        """Build complete Model → View → Action → Menu traces"""
        traces = []

        for model in self.python_scan.get('models', []):
            model_name = model.get('_name')
            if not model_name:
                continue

            trace = {
                'model': model_name,
                'model_file': model.get('relative_path'),
                'model_class': model['class_name'],
                'views': [],
                'actions': [],
                'menus': [],
                'complete': False,
            }

            # Add views
            views = self.relationships['model_to_views'].get(model_name, [])
            trace['views'] = views

            # Add actions
            actions = self.relationships['model_to_actions'].get(model_name, [])
            trace['actions'] = actions

            # Add menus
            menus = self.relationships['model_to_menus'].get(model_name, [])
            trace['menus'] = menus

            # Check if trace is complete (has at least one of each)
            trace['complete'] = bool(views and actions and menus)

            # Only include models that have at least one UI component
            if views or actions or menus:
                traces.append(trace)

        self.relationships['full_traces'] = traces

    def _build_dependency_graph(self):
        """Build a complete dependency graph"""
        graph = {
            'models': {},
            'views': {},
            'actions': {},
            'menus': {},
        }

        # Model dependencies
        for model_name, relations in self.relationships['model_relations'].items():
            deps = set()
            for field_name, rel_info in relations.items():
                deps.add(rel_info['comodel'])
            graph['models'][model_name] = {
                'depends_on': list(deps),
                'inherited_by': [],
            }

        # Add inheritance to model graph
        for model_name, parents in self.relationships['model_inheritance'].items():
            if model_name not in graph['models']:
                graph['models'][model_name] = {'depends_on': [], 'inherited_by': []}
            for parent in parents:
                parent_model = parent['model']
                graph['models'][model_name]['depends_on'].append(parent_model)
                if parent_model not in graph['models']:
                    graph['models'][parent_model] = {'depends_on': [], 'inherited_by': []}
                graph['models'][parent_model]['inherited_by'].append(model_name)

        # View dependencies
        for view_id, inherit_info in self.relationships['view_inheritance'].items():
            graph['views'][view_id] = {
                'inherits': inherit_info['parent'],
                'model': inherit_info['model'],
            }

        # Action to menu mapping
        for action_id, menus in self.relationships['action_to_menus'].items():
            graph['actions'][action_id] = {
                'menus': [m['xml_id'] for m in menus],
            }

        self.relationships['dependency_graph'] = graph

    def _generate_summary(self):
        """Generate summary statistics"""
        self.relationships['summary'] = {
            'models_with_views': len(self.relationships['model_to_views']),
            'models_with_actions': len(self.relationships['model_to_actions']),
            'models_with_menus': len(self.relationships['model_to_menus']),
            'models_with_inheritance': len(self.relationships['model_inheritance']),
            'models_with_relations': len(self.relationships['model_relations']),
            'inherited_views': len(self.relationships['view_inheritance']),
            'complete_traces': len([t for t in self.relationships['full_traces'] if t['complete']]),
            'incomplete_traces': len([t for t in self.relationships['full_traces'] if not t['complete']]),
        }

    def get_model_trace(self, model_name: str) -> Optional[Dict]:
        """Get the complete trace for a specific model"""
        for trace in self.relationships['full_traces']:
            if trace['model'] == model_name:
                return trace
        return None

    def get_related_models(self, model_name: str) -> List[str]:
        """Get all models related to a given model"""
        related = set()

        # Through relations
        relations = self.relationships['model_relations'].get(model_name, {})
        for rel_info in relations.values():
            related.add(rel_info['comodel'])

        # Through inheritance
        parents = self.relationships['model_inheritance'].get(model_name, [])
        for parent in parents:
            related.add(parent['model'])

        # Models that inherit from this one
        for child_model, parents in self.relationships['model_inheritance'].items():
            if any(p['model'] == model_name for p in parents):
                related.add(child_model)

        return list(related)

    def get_view_chain(self, view_xml_id: str) -> List[str]:
        """Get the inheritance chain for a view"""
        chain = [view_xml_id]
        current = view_xml_id

        while current in self.relationships['view_inheritance']:
            parent = self.relationships['view_inheritance'][current]['parent']
            if parent in chain:  # Avoid infinite loop
                break
            chain.append(parent)
            current = parent

        return chain

    def find_circular_dependencies(self) -> List[Dict]:
        """Find circular dependencies in models"""
        circular = []
        visited = set()
        rec_stack = set()

        def dfs(model: str, path: List[str]) -> Optional[List[str]]:
            if model in rec_stack:
                # Found cycle
                cycle_start = path.index(model)
                return path[cycle_start:] + [model]

            if model in visited:
                return None

            visited.add(model)
            rec_stack.add(model)

            deps = self.relationships['dependency_graph'].get('models', {}).get(model, {})
            for dep in deps.get('depends_on', []):
                result = dfs(dep, path + [model])
                if result:
                    return result

            rec_stack.remove(model)
            return None

        for model in self.relationships['dependency_graph'].get('models', {}):
            cycle = dfs(model, [])
            if cycle and tuple(sorted(cycle)) not in [tuple(sorted(c['cycle'])) for c in circular]:
                circular.append({
                    'type': 'model',
                    'cycle': cycle,
                    'severity': 'warning',
                })

        return circular
