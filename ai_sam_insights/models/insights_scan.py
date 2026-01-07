# -*- coding: utf-8 -*-
"""
Insights Scan Model

Stores ecosystem scan results and provides methods to run analyses.
"""
import json
import os
from datetime import datetime
from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)


class InsightsScan(models.Model):
    _name = 'insights.scan'
    _description = 'SAM AI Ecosystem Scan'
    _order = 'create_date desc'
    _rec_name = 'display_name'

    # Basic Info
    display_name = fields.Char(compute='_compute_display_name', store=True)
    scan_date = fields.Datetime(default=fields.Datetime.now, readonly=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('running', 'Running'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ], default='draft', readonly=True)

    # Configuration
    base_path = fields.Char(
        string='Scan Path',
        help='Root directory to scan (leave empty to use default settings)'
    )
    module_filter = fields.Char(
        string='Module Filter',
        help='Comma-separated list of module names to include (leave empty to use default settings)'
    )
    include_registry = fields.Boolean(
        string='Include Registry Scan',
        default=True,
        help='Query Odoo runtime registry for additional validation'
    )
    use_default_settings = fields.Boolean(
        string='Use Default Settings',
        default=True,
        help='Pull configuration from Scan Default Settings'
    )

    # Results
    health_score = fields.Integer(readonly=True)
    health_status = fields.Char(readonly=True)
    duration_seconds = fields.Float(readonly=True)

    # Statistics
    files_scanned = fields.Integer(readonly=True)
    models_found = fields.Integer(readonly=True)
    views_found = fields.Integer(readonly=True)
    actions_found = fields.Integer(readonly=True)
    js_files_found = fields.Integer(readonly=True)
    css_files_found = fields.Integer(readonly=True)

    # Issue counts
    critical_count = fields.Integer(readonly=True)
    warning_count = fields.Integer(readonly=True)
    info_count = fields.Integer(readonly=True)

    # Finding tracking (new vs recurring)
    findings_new = fields.Integer(string='New Findings', readonly=True)
    findings_recurring = fields.Integer(string='Recurring Findings', readonly=True)

    # Related findings
    finding_ids = fields.One2many('insights.finding', 'scan_id', string='Findings')
    relationship_ids = fields.One2many('insights.relationship', 'scan_id', string='Relationships')

    # Full report (JSON)
    report_json = fields.Text(readonly=True)
    full_results_json = fields.Text(readonly=True)

    # Error tracking
    error_message = fields.Text(readonly=True)

    @api.depends('scan_date', 'health_score', 'state')
    def _compute_display_name(self):
        for record in self:
            date_str = record.scan_date.strftime('%Y-%m-%d %H:%M') if record.scan_date else 'New'
            if record.state == 'completed':
                record.display_name = f"Scan {date_str} (Score: {record.health_score}/100)"
            else:
                record.display_name = f"Scan {date_str} ({record.state})"

    def action_run_scan(self):
        """Run the ecosystem scan"""
        self.ensure_one()

        if self.state not in ('draft', 'failed'):
            raise UserError(_("Can only run scans in draft or failed state"))

        self.write({'state': 'running', 'error_message': False})

        try:
            # Import here to avoid circular imports
            from ..analyzers.ecosystem_analyzer import EcosystemAnalyzer

            # Get configuration (from defaults or this record)
            scan_path = self.base_path
            module_filter_str = self.module_filter
            include_registry = self.include_registry

            # Apply default settings if enabled
            if self.use_default_settings:
                Settings = self.env['insights.scan.settings']
                settings = Settings.get_settings()
                if settings.default_scan_path and not scan_path:
                    scan_path = settings.default_scan_path
                if settings.module_ids and not module_filter_str:
                    module_filter_str = settings.get_selected_module_filter()
                include_registry = settings.include_registry

            if not scan_path:
                raise UserError(_("No scan path configured. Please set a default scan path in Settings or enter one manually."))

            # Parse module filter
            module_filter = None
            if module_filter_str:
                module_filter = [m.strip() for m in module_filter_str.split(',') if m.strip()]

            # Run the analysis
            analyzer = EcosystemAnalyzer(scan_path, module_filter)
            report = analyzer.analyze(
                include_registry=include_registry,
                env=self.env if include_registry else None
            )

            # Store results
            self._store_results(report, analyzer.get_full_results())

            self.write({'state': 'completed'})
            _logger.info(f"Scan {self.id} completed with health score {self.health_score}")

        except Exception as e:
            _logger.exception(f"Scan {self.id} failed")
            self.write({
                'state': 'failed',
                'error_message': str(e),
            })
            raise UserError(_("Scan failed: %s") % str(e))

        return True

    def _store_results(self, report: dict, full_results: dict):
        """Store scan results in the database"""
        stats = report.get('statistics', {})
        summary = report.get('summary', {})

        self.write({
            'health_score': report.get('health_score', 0),
            'health_status': summary.get('health_status', 'Unknown'),
            'duration_seconds': report.get('analysis_duration_seconds', 0),
            'files_scanned': summary.get('total_files_scanned', 0),
            'models_found': stats.get('python', {}).get('models', 0),
            'views_found': stats.get('xml', {}).get('views', 0),
            'actions_found': stats.get('xml', {}).get('actions', 0),
            'js_files_found': stats.get('assets', {}).get('js_files', 0),
            'css_files_found': stats.get('assets', {}).get('css_files', 0),
            'critical_count': summary.get('critical_count', 0),
            'warning_count': summary.get('warning_count', 0),
            'info_count': stats.get('duplicates', {}).get('severity_counts', {}).get('info', 0) +
                         stats.get('orphans', {}).get('severity_counts', {}).get('info', 0),
            'report_json': json.dumps(report, indent=2, default=str),
            'full_results_json': json.dumps(full_results, indent=2, default=str),
        })

        # Create findings records
        self._create_findings(report, full_results)

        # Create relationship records
        self._create_relationships(full_results)

    def _create_findings(self, report: dict, full_results: dict):
        """Create or update finding records from analysis results.

        Uses find_or_create pattern to avoid duplicates:
        - Existing findings are updated (occurrence count, last seen date)
        - New findings are created with first seen tracking
        - Resolved/acknowledged findings retain their status
        """
        Finding = self.env['insights.finding']

        # Track which findings were seen in this scan
        new_count = 0
        recurring_count = 0

        # Add critical issues
        for issue in report.get('critical_issues', []):
            finding = Finding.find_or_create(self.id, {
                'severity': 'critical',
                'category': issue.get('category'),
                'finding_type': issue.get('type'),
                'details_json': json.dumps(issue.get('details', {}), default=str),
            })
            if finding.occurrence_count == 1:
                new_count += 1
            else:
                recurring_count += 1

        # Add warnings
        for issue in report.get('warnings', []):
            finding = Finding.find_or_create(self.id, {
                'severity': 'warning',
                'category': issue.get('category'),
                'finding_type': issue.get('type'),
                'details_json': json.dumps(issue.get('details', {}), default=str),
            })
            if finding.occurrence_count == 1:
                new_count += 1
            else:
                recurring_count += 1

        # Add recommendations
        for rec in report.get('recommendations', []):
            finding = Finding.find_or_create(self.id, {
                'severity': 'recommendation',
                'category': rec.get('category'),
                'finding_type': rec.get('type', 'recommendation'),
                'title': rec.get('title'),
                'description': rec.get('description'),
                'priority': rec.get('priority'),
                'effort': rec.get('effort'),
                'impact': rec.get('impact'),
            })
            if finding.occurrence_count == 1:
                new_count += 1
            else:
                recurring_count += 1

        # Update counts on scan record
        self.write({
            'findings_new': new_count,
            'findings_recurring': recurring_count,
        })

    def _create_relationships(self, full_results: dict):
        """Create relationship records from analysis results"""
        Relationship = self.env['insights.relationship']

        # Clear existing relationships
        self.relationship_ids.unlink()

        relationships = full_results.get('relationships', {})

        # Create full trace records
        for trace in relationships.get('full_traces', []):
            Relationship.create({
                'scan_id': self.id,
                'relationship_type': 'model_trace',
                'source_type': 'model',
                'source_name': trace.get('model'),
                'source_file': trace.get('model_file'),
                'is_complete': trace.get('complete', False),
                'details_json': json.dumps({
                    'views': trace.get('views', []),
                    'actions': trace.get('actions', []),
                    'menus': trace.get('menus', []),
                }, default=str),
            })

    def action_view_report(self):
        """Open the HTML report viewer"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_url',
            'url': f'/insights/report/{self.id}',
            'target': 'new',
        }

    def action_export_json(self):
        """Export full results as JSON download"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_url',
            'url': f'/insights/export/{self.id}',
            'target': 'new',
        }

    @api.model
    def action_run_quick_scan(self):
        """Run a quick scan of the SAM AI modules"""
        # Get the addons path
        import odoo
        addons_paths = odoo.addons.__path__

        # Find the SAM AI addons path
        sam_path = None
        for path in addons_paths:
            if os.path.exists(os.path.join(path, 'ai_sam')):
                sam_path = path
                break

        if not sam_path:
            raise UserError(_("Could not find SAM AI modules in addons path"))

        # Create and run scan
        scan = self.create({
            'base_path': sam_path,
            'module_filter': 'ai_sam,ai_sam_base,ai_sam_workflows,ai_sam_insights',
            'include_registry': True,
        })

        scan.action_run_scan()

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'insights.scan',
            'res_id': scan.id,
            'view_mode': 'form',
            'target': 'current',
        }

    @api.model
    def get_latest_health_score(self):
        """Get the health score from the most recent completed scan"""
        latest = self.search([('state', '=', 'completed')], limit=1)
        if latest:
            return {
                'score': latest.health_score,
                'status': latest.health_status,
                'date': latest.scan_date,
                'critical': latest.critical_count,
                'warnings': latest.warning_count,
            }
        return None
