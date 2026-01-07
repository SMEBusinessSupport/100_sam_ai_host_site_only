# -*- coding: utf-8 -*-
"""
Insights Finding Model

Stores individual findings from ecosystem scans.
Findings are deduplicated using a fingerprint - same issue won't be re-added.
"""
import json
import hashlib
from odoo import models, fields, api


class InsightsFinding(models.Model):
    _name = 'insights.finding'
    _description = 'SAM AI Insights Finding'
    _order = 'severity_order, category'

    # Deduplication - fingerprint uniquely identifies a finding
    fingerprint = fields.Char(
        string='Fingerprint',
        index=True,
        help='Unique identifier for this finding to prevent duplicates across scans'
    )

    # Scan tracking - findings persist across scans
    scan_id = fields.Many2one(
        'insights.scan',
        string='Last Scan',
        ondelete='set null',
        help='Most recent scan that detected this finding'
    )
    first_seen_scan_id = fields.Many2one(
        'insights.scan',
        string='First Seen In',
        ondelete='set null',
        help='Scan where this finding was first detected'
    )
    first_seen_date = fields.Datetime(string='First Seen', readonly=True)
    last_seen_date = fields.Datetime(string='Last Seen', readonly=True)
    occurrence_count = fields.Integer(
        string='Times Detected',
        default=1,
        help='Number of scans that have detected this finding'
    )

    # Status tracking
    status = fields.Selection([
        ('new', 'New'),
        ('acknowledged', 'Acknowledged'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('wont_fix', "Won't Fix"),
        ('false_positive', 'False Positive'),
    ], default='new', required=True)

    # Classification
    severity = fields.Selection([
        ('critical', 'Critical'),
        ('warning', 'Warning'),
        ('info', 'Info'),
        ('recommendation', 'Recommendation'),
    ], required=True)
    severity_order = fields.Integer(compute='_compute_severity_order', store=True)

    category = fields.Selection([
        ('duplicate', 'Duplicate Code'),
        ('orphan', 'Orphaned Component'),
        ('dangling', 'Dangling Reference'),
        ('commented_code', 'Commented Code'),
        ('external_path', 'External Path Reference'),
        ('architecture', 'Architecture'),
        ('code_quality', 'Code Quality'),
        ('cleanup', 'Cleanup'),
        ('ux', 'User Experience'),
        ('bug_fix', 'Bug Fix'),
        ('documentation', 'Documentation'),
        ('other', 'Other'),
    ])

    finding_type = fields.Char(string='Type')

    # For recommendations
    title = fields.Char()
    description = fields.Text()
    priority = fields.Selection([
        ('critical', 'Critical'),
        ('high', 'High'),
        ('medium', 'Medium'),
        ('low', 'Low'),
    ])
    effort = fields.Selection([
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ])
    impact = fields.Char()

    # Raw details
    details_json = fields.Text()

    # Computed display fields
    display_name = fields.Char(compute='_compute_display_name')
    file_path = fields.Char(compute='_compute_from_details', store=True)
    model_name = fields.Char(compute='_compute_from_details', store=True)
    xml_id = fields.Char(compute='_compute_from_details', store=True)

    # Legacy action tracking (kept for compatibility)
    is_resolved = fields.Boolean(compute='_compute_is_resolved', store=True)
    resolved_date = fields.Datetime()
    resolved_by = fields.Many2one('res.users')
    resolution_note = fields.Text()

    _sql_constraints = [
        ('fingerprint_unique', 'unique(fingerprint)', 'Finding fingerprint must be unique!')
    ]

    @api.depends('status')
    def _compute_is_resolved(self):
        for record in self:
            record.is_resolved = record.status in ('resolved', 'wont_fix', 'false_positive')

    @api.depends('severity')
    def _compute_severity_order(self):
        order_map = {'critical': 1, 'warning': 2, 'info': 3, 'recommendation': 4}
        for record in self:
            record.severity_order = order_map.get(record.severity, 5)

    @api.depends('severity', 'category', 'finding_type', 'title')
    def _compute_display_name(self):
        for record in self:
            if record.title:
                record.display_name = record.title
            else:
                parts = [record.severity or '', record.category or '', record.finding_type or '']
                record.display_name = ' - '.join(p for p in parts if p)

    @api.depends('details_json')
    def _compute_from_details(self):
        for record in self:
            record.file_path = ''
            record.model_name = ''
            record.xml_id = ''

            if record.details_json:
                try:
                    details = json.loads(record.details_json)
                    record.file_path = details.get('file') or details.get('relative_path', '')
                    record.model_name = details.get('model') or details.get('model_name', '')
                    record.xml_id = details.get('xml_id') or details.get('view_xml_id', '')
                except (json.JSONDecodeError, TypeError):
                    pass

    def get_details(self):
        """Parse and return details as dict"""
        self.ensure_one()
        if self.details_json:
            try:
                return json.loads(self.details_json)
            except (json.JSONDecodeError, TypeError):
                pass
        return {}

    def action_mark_resolved(self):
        """Mark finding as resolved"""
        self.write({
            'status': 'resolved',
            'resolved_date': fields.Datetime.now(),
            'resolved_by': self.env.uid,
        })

    def action_acknowledge(self):
        """Mark finding as acknowledged"""
        self.write({'status': 'acknowledged'})

    def action_wont_fix(self):
        """Mark finding as won't fix"""
        self.write({'status': 'wont_fix'})

    def action_false_positive(self):
        """Mark finding as false positive"""
        self.write({'status': 'false_positive'})

    @api.model
    def _generate_fingerprint(self, severity, category, finding_type, details=None, title=None):
        """
        Generate a unique fingerprint for a finding.

        The fingerprint is based on key identifying attributes so the same
        issue detected in multiple scans won't create duplicates.
        """
        # Build fingerprint components
        parts = [
            severity or '',
            category or '',
            finding_type or '',
        ]

        # For recommendations, use title as key identifier
        if severity == 'recommendation' and title:
            parts.append(title)
        # For other findings, use file path and/or model name from details
        elif details:
            if isinstance(details, str):
                try:
                    details = json.loads(details)
                except (json.JSONDecodeError, TypeError):
                    details = {}

            # Key identifying info from details
            file_path = details.get('file') or details.get('relative_path') or ''
            model_name = details.get('model') or details.get('model_name') or ''
            xml_id = details.get('xml_id') or details.get('view_xml_id') or ''

            if file_path:
                parts.append(file_path)
            if model_name:
                parts.append(model_name)
            if xml_id:
                parts.append(xml_id)

        # Create hash
        fingerprint_str = '|'.join(str(p) for p in parts)
        return hashlib.sha256(fingerprint_str.encode()).hexdigest()[:32]

    @api.model
    def find_or_create(self, scan_id, vals):
        """
        Find existing finding by fingerprint or create new one.

        If finding exists:
        - Update last_seen_date and occurrence_count
        - Update scan_id to current scan
        - Don't change status if user has set it

        If finding is new:
        - Create with first_seen tracking
        """
        # Generate fingerprint if not provided
        if not vals.get('fingerprint'):
            vals['fingerprint'] = self._generate_fingerprint(
                vals.get('severity'),
                vals.get('category'),
                vals.get('finding_type'),
                vals.get('details_json'),
                vals.get('title'),
            )

        # Look for existing finding
        existing = self.search([('fingerprint', '=', vals['fingerprint'])], limit=1)

        now = fields.Datetime.now()

        if existing:
            # Update existing finding
            update_vals = {
                'scan_id': scan_id,
                'last_seen_date': now,
                'occurrence_count': existing.occurrence_count + 1,
            }

            # Only update these if they've changed and finding is still 'new'
            if existing.status == 'new':
                if vals.get('severity'):
                    update_vals['severity'] = vals['severity']
                if vals.get('description'):
                    update_vals['description'] = vals['description']

            existing.write(update_vals)
            return existing
        else:
            # Create new finding
            vals.update({
                'scan_id': scan_id,
                'first_seen_scan_id': scan_id,
                'first_seen_date': now,
                'last_seen_date': now,
                'occurrence_count': 1,
                'status': 'new',
            })
            return self.create(vals)

    def action_open_file(self):
        """Open the related file in the code editor (if available)"""
        self.ensure_one()
        file_path = self.file_path
        if file_path:
            # Return action that could be handled by IDE integration
            return {
                'type': 'ir.actions.client',
                'tag': 'insights_open_file',
                'params': {
                    'file_path': file_path,
                    'scan_path': self.scan_id.base_path,
                }
            }
        return False


class InsightsRelationship(models.Model):
    _name = 'insights.relationship'
    _description = 'SAM AI Insights Relationship'
    _order = 'relationship_type, source_name'

    scan_id = fields.Many2one('insights.scan', required=True, ondelete='cascade')

    relationship_type = fields.Selection([
        ('model_trace', 'Model Trace'),
        ('inheritance', 'Inheritance'),
        ('field_relation', 'Field Relation'),
        ('view_inheritance', 'View Inheritance'),
        ('dependency', 'Module Dependency'),
    ], required=True)

    source_type = fields.Selection([
        ('model', 'Model'),
        ('view', 'View'),
        ('action', 'Action'),
        ('menu', 'Menu'),
        ('module', 'Module'),
    ])
    source_name = fields.Char()
    source_file = fields.Char()

    target_type = fields.Selection([
        ('model', 'Model'),
        ('view', 'View'),
        ('action', 'Action'),
        ('menu', 'Menu'),
        ('module', 'Module'),
    ])
    target_name = fields.Char()
    target_file = fields.Char()

    is_complete = fields.Boolean()
    details_json = fields.Text()

    display_name = fields.Char(compute='_compute_display_name')

    @api.depends('relationship_type', 'source_name', 'target_name')
    def _compute_display_name(self):
        for record in self:
            if record.target_name:
                record.display_name = f"{record.source_name} → {record.target_name}"
            else:
                record.display_name = f"{record.relationship_type}: {record.source_name}"

    def get_details(self):
        """Parse and return details as dict"""
        self.ensure_one()
        if self.details_json:
            try:
                return json.loads(self.details_json)
            except (json.JSONDecodeError, TypeError):
                pass
        return {}
