# -*- coding: utf-8 -*-
"""
Insights Scan Module Model

Stores discovered modules from a scan path for selection.
"""
from odoo import models, fields, api


class InsightsScanModule(models.Model):
    _name = 'insights.scan.module'
    _description = 'Discovered Module for Scanning'
    _order = 'name'
    _rec_name = 'name'

    settings_id = fields.Many2one(
        'insights.scan.settings',
        string='Settings',
        required=True,
        ondelete='cascade',
    )
    name = fields.Char(string='Module Name', required=True, readonly=True)
    technical_name = fields.Char(string='Technical Name', required=True, readonly=True)
    path = fields.Char(string='Module Path', readonly=True)
    selected = fields.Boolean(string='Include in Scan', default=False)

    # Module info from manifest
    version = fields.Char(string='Version', readonly=True)
    summary = fields.Char(string='Summary', readonly=True)
    author = fields.Char(string='Author', readonly=True)
    category = fields.Char(string='Category', readonly=True)
    installable = fields.Boolean(string='Installable', default=True, readonly=True)

    _sql_constraints = [
        ('unique_module_per_settings',
         'UNIQUE(settings_id, technical_name)',
         'Module already exists in these settings!')
    ]
