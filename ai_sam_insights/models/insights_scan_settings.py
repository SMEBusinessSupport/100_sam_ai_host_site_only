# -*- coding: utf-8 -*-
"""
Insights Scan Settings Model

Singleton model for default scan configuration.
"""
import os
import ast
from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)


class InsightsScanSettings(models.Model):
    _name = 'insights.scan.settings'
    _description = 'Scan Default Settings'

    name = fields.Char(default='Default Scan Settings', required=True)
    default_scan_path = fields.Char(
        string='Default Scan Path',
        help='Root directory containing Odoo modules to scan',
    )
    include_registry = fields.Boolean(
        string='Include Registry Scan',
        default=True,
        help='Query Odoo runtime registry for additional validation',
    )
    module_ids = fields.One2many(
        'insights.scan.module',
        'settings_id',
        string='Discovered Modules',
    )

    # Computed counts
    total_modules = fields.Integer(compute='_compute_module_counts', string='Total Modules')
    selected_modules = fields.Integer(compute='_compute_module_counts', string='Selected Modules')

    # Last scan info
    last_path_scan = fields.Datetime(string='Last Path Scan', readonly=True)

    @api.depends('module_ids', 'module_ids.selected')
    def _compute_module_counts(self):
        for record in self:
            record.total_modules = len(record.module_ids)
            record.selected_modules = len(record.module_ids.filtered('selected'))

    @api.model
    def get_settings(self):
        """Get or create the singleton settings record"""
        settings = self.search([], limit=1)
        if not settings:
            settings = self.create({'name': 'Default Scan Settings'})
        return settings

    def action_scan_path(self):
        """Scan the configured path for Odoo modules"""
        self.ensure_one()

        if not self.default_scan_path:
            raise UserError(_("Please enter a scan path first"))

        if not os.path.exists(self.default_scan_path):
            raise UserError(_("Path does not exist: %s") % self.default_scan_path)

        if not os.path.isdir(self.default_scan_path):
            raise UserError(_("Path is not a directory: %s") % self.default_scan_path)

        # Clear existing modules
        self.module_ids.unlink()

        # Discover modules
        discovered_modules = self._discover_modules(self.default_scan_path)

        # Create module records
        Module = self.env['insights.scan.module']
        for mod_info in discovered_modules:
            Module.create({
                'settings_id': self.id,
                'name': mod_info.get('name', mod_info['technical_name']),
                'technical_name': mod_info['technical_name'],
                'path': mod_info['path'],
                'version': mod_info.get('version', ''),
                'summary': mod_info.get('summary', ''),
                'author': mod_info.get('author', ''),
                'category': mod_info.get('category', ''),
                'installable': mod_info.get('installable', True),
                'selected': False,  # User must explicitly select
            })

        self.last_path_scan = fields.Datetime.now()

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Path Scanned'),
                'message': _('Found %d modules. Select which ones to include in scans.') % len(discovered_modules),
                'type': 'success',
                'sticky': False,
            }
        }

    def _discover_modules(self, base_path):
        """Discover Odoo modules in the given path"""
        modules = []

        for item in os.listdir(base_path):
            item_path = os.path.join(base_path, item)

            # Skip non-directories
            if not os.path.isdir(item_path):
                continue

            # Check for __manifest__.py (Odoo module indicator)
            manifest_path = os.path.join(item_path, '__manifest__.py')
            if not os.path.exists(manifest_path):
                continue

            # Parse manifest
            try:
                manifest_data = self._parse_manifest(manifest_path)
                modules.append({
                    'technical_name': item,
                    'path': item_path,
                    'name': manifest_data.get('name', item),
                    'version': manifest_data.get('version', ''),
                    'summary': manifest_data.get('summary', ''),
                    'author': manifest_data.get('author', ''),
                    'category': manifest_data.get('category', ''),
                    'installable': manifest_data.get('installable', True),
                })
            except Exception as e:
                _logger.warning(f"Could not parse manifest for {item}: {e}")
                # Still add the module with basic info
                modules.append({
                    'technical_name': item,
                    'path': item_path,
                    'name': item,
                })

        return sorted(modules, key=lambda x: x['technical_name'])

    def _parse_manifest(self, manifest_path):
        """Parse an Odoo manifest file"""
        with open(manifest_path, 'r', encoding='utf-8') as f:
            content = f.read()

        try:
            # Safely evaluate the manifest dict
            manifest_data = ast.literal_eval(content)
            return manifest_data if isinstance(manifest_data, dict) else {}
        except (ValueError, SyntaxError) as e:
            _logger.warning(f"Could not parse {manifest_path}: {e}")
            return {}

    def action_select_all(self):
        """Select all modules"""
        self.ensure_one()
        self.module_ids.write({'selected': True})
        return True

    def action_deselect_all(self):
        """Deselect all modules"""
        self.ensure_one()
        self.module_ids.write({'selected': False})
        return True

    def action_select_sam_modules(self):
        """Select only SAM AI modules (ai_sam*)"""
        self.ensure_one()
        self.module_ids.write({'selected': False})
        sam_modules = self.module_ids.filtered(
            lambda m: m.technical_name.startswith('ai_sam')
        )
        sam_modules.write({'selected': True})
        return True

    def get_selected_module_filter(self):
        """Get comma-separated list of selected modules for scan"""
        self.ensure_one()
        selected = self.module_ids.filtered('selected')
        if selected:
            return ','.join(selected.mapped('technical_name'))
        return ''

    @api.model
    def action_open_settings(self):
        """Open the settings form (creates if needed)"""
        settings = self.get_settings()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'insights.scan.settings',
            'res_id': settings.id,
            'view_mode': 'form',
            'target': 'current',
        }
