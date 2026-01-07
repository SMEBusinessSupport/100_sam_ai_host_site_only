# -*- coding: utf-8 -*-
"""
Report Controller for SAM AI Insights

Provides HTTP endpoints for:
- Viewing HTML reports
- Exporting JSON results
- Dashboard data API
"""
import json
from odoo import http
from odoo.http import request, Response


class InsightsReportController(http.Controller):

    @http.route('/insights/report/<int:scan_id>', type='http', auth='user')
    def view_report(self, scan_id, **kwargs):
        """Render HTML report for a scan"""
        scan = request.env['insights.scan'].browse(scan_id)
        if not scan.exists():
            return request.not_found()

        # Parse the report JSON
        report = {}
        if scan.report_json:
            try:
                report = json.loads(scan.report_json)
            except json.JSONDecodeError:
                pass

        # Render the HTML report
        html = self._generate_html_report(scan, report)
        return Response(html, content_type='text/html')

    @http.route('/insights/export/<int:scan_id>', type='http', auth='user')
    def export_json(self, scan_id, **kwargs):
        """Export full results as JSON download"""
        scan = request.env['insights.scan'].browse(scan_id)
        if not scan.exists():
            return request.not_found()

        content = scan.full_results_json or '{}'
        filename = f"ecosystem_scan_{scan.scan_date.strftime('%Y%m%d_%H%M%S')}.json"

        return Response(
            content,
            content_type='application/json',
            headers=[
                ('Content-Disposition', f'attachment; filename="{filename}"'),
            ]
        )

    @http.route('/insights/api/health', type='json', auth='user')
    def api_health(self, **kwargs):
        """API endpoint for health dashboard data"""
        Scan = request.env['insights.scan']
        return Scan.get_latest_health_score()

    @http.route('/insights/api/findings/<int:scan_id>', type='json', auth='user')
    def api_findings(self, scan_id, **kwargs):
        """API endpoint for scan findings"""
        scan = request.env['insights.scan'].browse(scan_id)
        if not scan.exists():
            return {'error': 'Scan not found'}

        findings = []
        for finding in scan.finding_ids:
            findings.append({
                'id': finding.id,
                'severity': finding.severity,
                'category': finding.category,
                'type': finding.finding_type,
                'title': finding.title,
                'description': finding.description,
                'file_path': finding.file_path,
                'model_name': finding.model_name,
                'xml_id': finding.xml_id,
                'is_resolved': finding.is_resolved,
                'details': finding.get_details(),
            })

        return findings

    @http.route('/insights/orphaned-assets/<int:scan_id>', type='http', auth='user')
    def view_orphaned_assets(self, scan_id, page=1, **kwargs):
        """View paginated list of orphaned assets"""
        scan = request.env['insights.scan'].browse(scan_id)
        if not scan.exists():
            return request.not_found()

        # Parse full results to get orphaned assets
        orphaned_assets = []
        if scan.full_results_json:
            try:
                full_results = json.loads(scan.full_results_json)
                orphaned_assets = full_results.get('asset_scan', {}).get('orphaned_assets', [])
            except json.JSONDecodeError:
                pass

        # Pagination
        page = int(page)
        per_page = 50
        total = len(orphaned_assets)
        total_pages = (total + per_page - 1) // per_page
        start = (page - 1) * per_page
        end = start + per_page
        current_assets = orphaned_assets[start:end]

        html = self._generate_orphaned_assets_html(scan, current_assets, page, total_pages, total)
        return Response(html, content_type='text/html')

    @http.route('/insights/integration-refs/<int:scan_id>', type='http', auth='user')
    def view_integration_references(self, scan_id, page=1, integration='all', category='all', **kwargs):
        """View paginated list of integration references (N8N, ai_automator)"""
        scan = request.env['insights.scan'].browse(scan_id)
        if not scan.exists():
            return request.not_found()

        # Parse full results to get integration references
        references = []
        if scan.full_results_json:
            try:
                full_results = json.loads(scan.full_results_json)
                int_refs = full_results.get('integration_references', {})

                # Collect references based on filter
                for int_type in ['n8n', 'ai_automator']:
                    if integration != 'all' and integration != int_type:
                        continue

                    int_data = int_refs.get(int_type, {})
                    for cat, refs in int_data.items():
                        if cat == 'summary':
                            continue
                        if category != 'all' and category != cat:
                            continue

                        for ref in refs:
                            ref_copy = ref.copy()
                            ref_copy['integration'] = int_type
                            references.append(ref_copy)

                # Sort by file and line number
                references.sort(key=lambda x: (x.get('relative_path', ''), x.get('line_number', 0)))
            except json.JSONDecodeError:
                pass

        # Pagination
        page = int(page)
        per_page = 50
        total = len(references)
        total_pages = max(1, (total + per_page - 1) // per_page)
        start = (page - 1) * per_page
        end = start + per_page
        current_items = references[start:end]

        html = self._generate_integration_refs_html(scan, current_items, page, total_pages, total, integration, category)
        return Response(html, content_type='text/html')

    def _generate_integration_refs_html(self, scan, items, page, total_pages, total, integration, category):
        """Generate HTML for integration references page"""
        # Build item rows
        rows_html = ''
        for i, item in enumerate(items, start=(page - 1) * 50 + 1):
            int_type = item.get('integration', 'unknown')
            cat = item.get('category', 'reference')
            rel_path = item.get('relative_path', '')
            line_num = item.get('line_number', 0)
            line_content = item.get('line_content', '').replace('<', '&lt;').replace('>', '&gt;')
            file_type = item.get('file_type', 'unknown')

            # Color by integration
            int_colors = {'n8n': '#ff6d00', 'ai_automator': '#00bcd4'}
            int_color = int_colors.get(int_type, '#888')

            # File type colors
            type_colors = {'python': '#3776ab', 'javascript': '#f7df1e', 'xml': '#e34c26', 'json': '#888', 'yaml': '#cb171e'}
            type_color = type_colors.get(file_type, '#888')

            rows_html += f'''
            <div class="ref-item">
                <div class="ref-header">
                    <span class="integration-badge" style="background: {int_color}22; color: {int_color};">{int_type.upper()}</span>
                    <span class="category-badge">{cat}</span>
                    <span class="file-path">{rel_path}</span>
                    <span class="line-info">Line {line_num}</span>
                    <span class="type-badge" style="background: {type_color}22; color: {type_color};">{file_type}</span>
                </div>
                <pre class="code-preview">{line_content}</pre>
            </div>'''

        # Build filter tabs for integration
        int_tabs = ''
        for int_type, label in [('all', 'All'), ('n8n', 'N8N'), ('ai_automator', 'ai_automator')]:
            active = 'active' if integration == int_type else ''
            int_tabs += f'<a href="/insights/integration-refs/{scan.id}?integration={int_type}&category={category}" class="filter-tab {active}">{label}</a>'

        # Build filter tabs for category
        cat_tabs = ''
        categories = [('all', 'All Categories'), ('webhook', 'Webhooks'), ('workflow', 'Workflows'),
                     ('api', 'API'), ('config', 'Config'), ('module', 'Module'), ('model', 'Model'),
                     ('import', 'Import'), ('reference', 'Reference')]
        for cat_type, label in categories:
            active = 'active' if category == cat_type else ''
            cat_tabs += f'<a href="/insights/integration-refs/{scan.id}?integration={integration}&category={cat_type}" class="filter-tab small {active}">{label}</a>'

        # Build pagination
        pagination_html = ''
        if total_pages > 1:
            pagination_html = '<div class="pagination">'
            if page > 1:
                pagination_html += f'<a href="/insights/integration-refs/{scan.id}?page={page-1}&integration={integration}&category={category}" class="page-link">&laquo; Previous</a>'

            for p in range(1, total_pages + 1):
                if p == page:
                    pagination_html += f'<span class="page-link current">{p}</span>'
                elif p <= 3 or p > total_pages - 3 or abs(p - page) <= 2:
                    pagination_html += f'<a href="/insights/integration-refs/{scan.id}?page={p}&integration={integration}&category={category}" class="page-link">{p}</a>'
                elif abs(p - page) == 3:
                    pagination_html += '<span class="page-link">...</span>'

            if page < total_pages:
                pagination_html += f'<a href="/insights/integration-refs/{scan.id}?page={page+1}&integration={integration}&category={category}" class="page-link">Next &raquo;</a>'
            pagination_html += '</div>'

        return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Integration References - SAM AI Insights</title>
    <style>
        :root {{
            --sam-gold: #D4AF37;
            --sam-dark: #1a1a2e;
            --sam-darker: #0f0f1a;
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            font-family: 'Segoe UI', system-ui, sans-serif;
            background: var(--sam-darker);
            color: #e0e0e0;
            line-height: 1.6;
            padding: 2rem;
        }}
        .container {{ max-width: 1400px; margin: 0 auto; }}
        header {{
            margin-bottom: 2rem;
            padding-bottom: 1rem;
            border-bottom: 2px solid var(--sam-gold);
        }}
        h1 {{ color: var(--sam-gold); font-size: 1.8rem; margin-bottom: 0.5rem; }}
        .subtitle {{ color: #888; font-size: 0.9rem; }}
        .back-link {{
            display: inline-block;
            margin-bottom: 1rem;
            color: var(--sam-gold);
            text-decoration: none;
        }}
        .back-link:hover {{ text-decoration: underline; }}
        .summary {{
            background: var(--sam-dark);
            padding: 1rem 1.5rem;
            border-radius: 8px;
            margin-bottom: 1.5rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 1rem;
        }}
        .summary-stat {{ font-size: 1.1rem; }}
        .summary-stat strong {{ color: var(--sam-gold); }}
        .filter-section {{
            margin-bottom: 1rem;
        }}
        .filter-label {{
            color: #888;
            font-size: 0.85rem;
            margin-bottom: 0.5rem;
        }}
        .filter-tabs {{
            display: flex;
            gap: 0.5rem;
            flex-wrap: wrap;
        }}
        .filter-tab {{
            padding: 0.5rem 1rem;
            background: var(--sam-dark);
            color: #e0e0e0;
            text-decoration: none;
            border-radius: 4px;
            border: 1px solid #333;
            font-size: 0.9rem;
        }}
        .filter-tab.small {{
            padding: 0.3rem 0.8rem;
            font-size: 0.8rem;
        }}
        .filter-tab:hover {{ background: #252542; border-color: var(--sam-gold); }}
        .filter-tab.active {{ background: var(--sam-gold); color: #000; font-weight: bold; border-color: var(--sam-gold); }}
        .ref-item {{
            background: var(--sam-dark);
            border-radius: 8px;
            margin-bottom: 1rem;
            overflow: hidden;
            border-left: 3px solid #17a2b8;
        }}
        .ref-header {{
            padding: 0.75rem 1rem;
            background: #252542;
            display: flex;
            align-items: center;
            gap: 0.75rem;
            flex-wrap: wrap;
        }}
        .integration-badge {{
            padding: 3px 10px;
            border-radius: 4px;
            font-size: 0.8rem;
            font-weight: 600;
        }}
        .category-badge {{
            padding: 2px 8px;
            border-radius: 3px;
            font-size: 0.75rem;
            background: #333;
            color: #aaa;
        }}
        .file-path {{
            font-family: monospace;
            font-size: 0.9rem;
            color: #e0e0e0;
            flex-grow: 1;
        }}
        .line-info {{
            font-size: 0.8rem;
            color: #888;
        }}
        .type-badge {{
            padding: 2px 8px;
            border-radius: 3px;
            font-size: 0.75rem;
            font-weight: 600;
        }}
        .code-preview {{
            padding: 1rem;
            font-family: 'Consolas', 'Monaco', monospace;
            font-size: 0.85rem;
            overflow-x: auto;
            white-space: pre-wrap;
            color: #aaa;
            background: #1a1a2e;
            border-top: 1px solid #333;
            max-height: 150px;
            overflow-y: auto;
        }}
        .pagination {{
            display: flex;
            justify-content: center;
            gap: 0.5rem;
            margin-top: 1.5rem;
        }}
        .page-link {{
            padding: 0.5rem 1rem;
            background: var(--sam-dark);
            color: #e0e0e0;
            text-decoration: none;
            border-radius: 4px;
            border: 1px solid #333;
        }}
        .page-link:hover {{ background: #252542; border-color: var(--sam-gold); }}
        .page-link.current {{ background: var(--sam-gold); color: #000; font-weight: bold; }}
        .note {{
            background: #252542;
            padding: 1rem;
            border-radius: 6px;
            margin-top: 1.5rem;
            border-left: 4px solid var(--sam-gold);
            font-size: 0.9rem;
            color: #aaa;
        }}
        .empty-state {{
            text-align: center;
            padding: 3rem;
            color: #666;
        }}
    </style>
</head>
<body>
    <div class="container">
        <a href="/insights/report/{scan.id}" class="back-link">&larr; Back to Full Report</a>

        <header>
            <h1>Integration References</h1>
            <p class="subtitle">N8N workflow and ai_automator references across the codebase</p>
        </header>

        <div class="summary">
            <span class="summary-stat">Total: <strong>{total}</strong> references</span>
            <span class="summary-stat">Showing: <strong>{(page-1)*50 + 1 if total > 0 else 0} - {min(page*50, total)}</strong></span>
            <span class="summary-stat">Page: <strong>{page}</strong> of <strong>{total_pages}</strong></span>
        </div>

        <div class="filter-section">
            <div class="filter-label">Integration:</div>
            <div class="filter-tabs">
                {int_tabs}
            </div>
        </div>

        <div class="filter-section">
            <div class="filter-label">Category:</div>
            <div class="filter-tabs">
                {cat_tabs}
            </div>
        </div>

        {rows_html if rows_html else '<div class="empty-state">No integration references found for this filter.</div>'}

        {pagination_html}

        <div class="note">
            <strong>What are integration references?</strong><br>
            This report identifies all references to external integrations in your codebase:
            <ul style="margin-top: 0.5rem; margin-left: 1.5rem;">
                <li><strong style="color: #ff6d00;">N8N</strong> - Webhook URLs, workflow IDs, API endpoints, configurations</li>
                <li><strong style="color: #00bcd4;">ai_automator</strong> - Module imports, model references, API calls</li>
            </ul>
            <br>
            Use this to understand integration points, document dependencies, and prepare for upgrades.
        </div>
    </div>
</body>
</html>'''

    @http.route('/insights/commented-code/<int:scan_id>', type='http', auth='user')
    def view_commented_code(self, scan_id, page=1, file_type='all', **kwargs):
        """View paginated list of commented code blocks"""
        scan = request.env['insights.scan'].browse(scan_id)
        if not scan.exists():
            return request.not_found()

        # Parse full results to get commented code findings
        commented_code = []
        if scan.full_results_json:
            try:
                full_results = json.loads(scan.full_results_json)
                cc_findings = full_results.get('commented_code_findings', {})

                # Collect findings based on filter
                if file_type == 'all' or file_type == 'python':
                    commented_code.extend(cc_findings.get('python', []))
                if file_type == 'all' or file_type == 'javascript':
                    commented_code.extend(cc_findings.get('javascript', []))
                if file_type == 'all' or file_type == 'xml':
                    commented_code.extend(cc_findings.get('xml', []))

                # Sort by severity (warnings first), then by file
                commented_code.sort(key=lambda x: (
                    0 if x.get('has_deletion_marker') else 1,
                    x.get('relative_path', '')
                ))
            except json.JSONDecodeError:
                pass

        # Pagination
        page = int(page)
        per_page = 50
        total = len(commented_code)
        total_pages = max(1, (total + per_page - 1) // per_page)
        start = (page - 1) * per_page
        end = start + per_page
        current_items = commented_code[start:end]

        html = self._generate_commented_code_html(scan, current_items, page, total_pages, total, file_type)
        return Response(html, content_type='text/html')

    def _generate_commented_code_html(self, scan, items, page, total_pages, total, file_type):
        """Generate HTML for commented code page"""
        # Build item rows
        rows_html = ''
        for i, item in enumerate(items, start=(page - 1) * 50 + 1):
            code_type = item.get('code_type', 'unknown')
            rel_path = item.get('relative_path', '')
            line_start = item.get('line_start', 0)
            line_end = item.get('line_end', 0)
            preview = item.get('preview', '').replace('<', '&lt;').replace('>', '&gt;')
            has_deletion = item.get('has_deletion_marker', False)
            finding_type = item.get('finding_type', '')

            # Color by type
            type_colors = {'python': '#3776ab', 'javascript': '#f7df1e', 'xml': '#e34c26'}
            type_color = type_colors.get(code_type, '#888')

            # Severity indicator
            severity_badge = ''
            if has_deletion:
                severity_badge = '<span style="background: #dc354522; color: #dc3545; padding: 2px 6px; border-radius: 3px; font-size: 0.75rem; margin-left: 0.5rem;">DELETION MARKER</span>'

            rows_html += f'''
            <div class="code-item {'has-marker' if has_deletion else ''}">
                <div class="code-header">
                    <span class="file-path">{rel_path}</span>
                    <span class="line-info">Lines {line_start}-{line_end}</span>
                    <span class="type-badge" style="background: {type_color}22; color: {type_color};">{code_type.upper()}</span>
                    {severity_badge}
                </div>
                <pre class="code-preview">{preview}</pre>
            </div>'''

        # Build filter tabs
        filter_tabs = ''
        filters = [('all', 'All'), ('python', 'Python'), ('javascript', 'JavaScript'), ('xml', 'XML')]
        for ftype, label in filters:
            active = 'active' if file_type == ftype else ''
            filter_tabs += f'<a href="/insights/commented-code/{scan.id}?file_type={ftype}" class="filter-tab {active}">{label}</a>'

        # Build pagination
        pagination_html = ''
        if total_pages > 1:
            pagination_html = '<div class="pagination">'
            if page > 1:
                pagination_html += f'<a href="/insights/commented-code/{scan.id}?page={page-1}&file_type={file_type}" class="page-link">&laquo; Previous</a>'

            for p in range(1, total_pages + 1):
                if p == page:
                    pagination_html += f'<span class="page-link current">{p}</span>'
                elif p <= 3 or p > total_pages - 3 or abs(p - page) <= 2:
                    pagination_html += f'<a href="/insights/commented-code/{scan.id}?page={p}&file_type={file_type}" class="page-link">{p}</a>'
                elif abs(p - page) == 3:
                    pagination_html += '<span class="page-link">...</span>'

            if page < total_pages:
                pagination_html += f'<a href="/insights/commented-code/{scan.id}?page={page+1}&file_type={file_type}" class="page-link">Next &raquo;</a>'
            pagination_html += '</div>'

        return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Commented Code - SAM AI Insights</title>
    <style>
        :root {{
            --sam-gold: #D4AF37;
            --sam-dark: #1a1a2e;
            --sam-darker: #0f0f1a;
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            font-family: 'Segoe UI', system-ui, sans-serif;
            background: var(--sam-darker);
            color: #e0e0e0;
            line-height: 1.6;
            padding: 2rem;
        }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        header {{
            margin-bottom: 2rem;
            padding-bottom: 1rem;
            border-bottom: 2px solid var(--sam-gold);
        }}
        h1 {{ color: var(--sam-gold); font-size: 1.8rem; margin-bottom: 0.5rem; }}
        .subtitle {{ color: #888; font-size: 0.9rem; }}
        .back-link {{
            display: inline-block;
            margin-bottom: 1rem;
            color: var(--sam-gold);
            text-decoration: none;
        }}
        .back-link:hover {{ text-decoration: underline; }}
        .summary {{
            background: var(--sam-dark);
            padding: 1rem 1.5rem;
            border-radius: 8px;
            margin-bottom: 1.5rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 1rem;
        }}
        .summary-stat {{ font-size: 1.1rem; }}
        .summary-stat strong {{ color: var(--sam-gold); }}
        .filter-tabs {{
            display: flex;
            gap: 0.5rem;
            margin-bottom: 1.5rem;
        }}
        .filter-tab {{
            padding: 0.5rem 1rem;
            background: var(--sam-dark);
            color: #e0e0e0;
            text-decoration: none;
            border-radius: 4px;
            border: 1px solid #333;
        }}
        .filter-tab:hover {{ background: #252542; border-color: var(--sam-gold); }}
        .filter-tab.active {{ background: var(--sam-gold); color: #000; font-weight: bold; border-color: var(--sam-gold); }}
        .code-item {{
            background: var(--sam-dark);
            border-radius: 8px;
            margin-bottom: 1rem;
            overflow: hidden;
            border-left: 3px solid #17a2b8;
        }}
        .code-item.has-marker {{ border-left-color: #dc3545; }}
        .code-header {{
            padding: 0.75rem 1rem;
            background: #252542;
            display: flex;
            align-items: center;
            gap: 1rem;
            flex-wrap: wrap;
        }}
        .file-path {{
            font-family: monospace;
            font-size: 0.9rem;
            color: #e0e0e0;
        }}
        .line-info {{
            font-size: 0.8rem;
            color: #888;
        }}
        .type-badge {{
            padding: 2px 8px;
            border-radius: 3px;
            font-size: 0.75rem;
            font-weight: 600;
        }}
        .code-preview {{
            padding: 1rem;
            font-family: 'Consolas', 'Monaco', monospace;
            font-size: 0.85rem;
            overflow-x: auto;
            white-space: pre-wrap;
            color: #aaa;
            background: #1a1a2e;
            border-top: 1px solid #333;
            max-height: 200px;
            overflow-y: auto;
        }}
        .pagination {{
            display: flex;
            justify-content: center;
            gap: 0.5rem;
            margin-top: 1.5rem;
        }}
        .page-link {{
            padding: 0.5rem 1rem;
            background: var(--sam-dark);
            color: #e0e0e0;
            text-decoration: none;
            border-radius: 4px;
            border: 1px solid #333;
        }}
        .page-link:hover {{ background: #252542; border-color: var(--sam-gold); }}
        .page-link.current {{ background: var(--sam-gold); color: #000; font-weight: bold; }}
        .note {{
            background: #252542;
            padding: 1rem;
            border-radius: 6px;
            margin-top: 1.5rem;
            border-left: 4px solid var(--sam-gold);
            font-size: 0.9rem;
            color: #aaa;
        }}
        .empty-state {{
            text-align: center;
            padding: 3rem;
            color: #666;
        }}
    </style>
</head>
<body>
    <div class="container">
        <a href="/insights/report/{scan.id}" class="back-link">&larr; Back to Full Report</a>

        <header>
            <h1>Commented Code Blocks</h1>
            <p class="subtitle">Dead code, code marked for deletion, and commented-out implementations</p>
        </header>

        <div class="summary">
            <span class="summary-stat">Total: <strong>{total}</strong> commented code blocks</span>
            <span class="summary-stat">Showing: <strong>{(page-1)*50 + 1 if total > 0 else 0} - {min(page*50, total)}</strong></span>
            <span class="summary-stat">Page: <strong>{page}</strong> of <strong>{total_pages}</strong></span>
        </div>

        <div class="filter-tabs">
            {filter_tabs}
        </div>

        {rows_html if rows_html else '<div class="empty-state">No commented code blocks found for this filter.</div>'}

        {pagination_html}

        <div class="note">
            <strong>What is commented code?</strong><br>
            This report identifies code that has been commented out, which may indicate:
            <ul style="margin-top: 0.5rem; margin-left: 1.5rem;">
                <li>Dead code that should be removed</li>
                <li>Code marked for deletion (TODO delete, DEPRECATED, etc.)</li>
                <li>Old implementations kept "just in case"</li>
                <li>Debugging code left behind</li>
            </ul>
            <br>
            <strong style="color: #dc3545;">Items marked with DELETION MARKER</strong> contain explicit comments indicating
            they should be removed (like TODO delete, DEPRECATED, OLD, etc.).
        </div>
    </div>
</body>
</html>'''

    def _generate_orphaned_assets_html(self, scan, assets, page, total_pages, total):
        """Generate HTML for orphaned assets page"""
        # Build asset rows
        rows_html = ''
        for i, asset in enumerate(assets, start=(page - 1) * 50 + 1):
            asset_type = asset.get('type', 'unknown')
            path = asset.get('path', '')
            # Make path more readable - show relative portion
            display_path = path.replace('\\', '/')
            if 'static/' in display_path:
                display_path = display_path[display_path.find('static/'):]

            type_color = '#ffc107' if asset_type == 'js' else '#17a2b8'
            rows_html += f'''
            <tr>
                <td style="color: #888;">{i}</td>
                <td><span style="background: {type_color}22; color: {type_color}; padding: 2px 8px; border-radius: 3px; font-size: 0.8rem;">{asset_type.upper()}</span></td>
                <td style="font-family: monospace; font-size: 0.85rem; word-break: break-all;">{display_path}</td>
            </tr>'''

        # Build pagination
        pagination_html = ''
        if total_pages > 1:
            pagination_html = '<div class="pagination">'
            if page > 1:
                pagination_html += f'<a href="/insights/orphaned-assets/{scan.id}?page={page-1}" class="page-link">&laquo; Previous</a>'

            # Show page numbers
            for p in range(1, total_pages + 1):
                if p == page:
                    pagination_html += f'<span class="page-link current">{p}</span>'
                elif p <= 3 or p > total_pages - 3 or abs(p - page) <= 2:
                    pagination_html += f'<a href="/insights/orphaned-assets/{scan.id}?page={p}" class="page-link">{p}</a>'
                elif abs(p - page) == 3:
                    pagination_html += '<span class="page-link">...</span>'

            if page < total_pages:
                pagination_html += f'<a href="/insights/orphaned-assets/{scan.id}?page={page+1}" class="page-link">Next &raquo;</a>'
            pagination_html += '</div>'

        return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Orphaned Assets - SAM AI Insights</title>
    <style>
        :root {{
            --sam-gold: #D4AF37;
            --sam-dark: #1a1a2e;
            --sam-darker: #0f0f1a;
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            font-family: 'Segoe UI', system-ui, sans-serif;
            background: var(--sam-darker);
            color: #e0e0e0;
            line-height: 1.6;
            padding: 2rem;
        }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        header {{
            margin-bottom: 2rem;
            padding-bottom: 1rem;
            border-bottom: 2px solid var(--sam-gold);
        }}
        h1 {{ color: var(--sam-gold); font-size: 1.8rem; margin-bottom: 0.5rem; }}
        .subtitle {{ color: #888; font-size: 0.9rem; }}
        .back-link {{
            display: inline-block;
            margin-bottom: 1rem;
            color: var(--sam-gold);
            text-decoration: none;
        }}
        .back-link:hover {{ text-decoration: underline; }}
        .summary {{
            background: var(--sam-dark);
            padding: 1rem 1.5rem;
            border-radius: 8px;
            margin-bottom: 1.5rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .summary-stat {{ font-size: 1.1rem; }}
        .summary-stat strong {{ color: var(--sam-gold); }}
        table {{
            width: 100%;
            border-collapse: collapse;
            background: var(--sam-dark);
            border-radius: 8px;
            overflow: hidden;
        }}
        th, td {{ padding: 0.75rem 1rem; text-align: left; border-bottom: 1px solid #333; }}
        th {{ background: #252542; color: var(--sam-gold); font-weight: 600; }}
        tr:hover {{ background: #252542; }}
        .pagination {{
            display: flex;
            justify-content: center;
            gap: 0.5rem;
            margin-top: 1.5rem;
        }}
        .page-link {{
            padding: 0.5rem 1rem;
            background: var(--sam-dark);
            color: #e0e0e0;
            text-decoration: none;
            border-radius: 4px;
            border: 1px solid #333;
        }}
        .page-link:hover {{ background: #252542; border-color: var(--sam-gold); }}
        .page-link.current {{ background: var(--sam-gold); color: #000; font-weight: bold; }}
        .note {{
            background: #252542;
            padding: 1rem;
            border-radius: 6px;
            margin-top: 1.5rem;
            border-left: 4px solid var(--sam-gold);
            font-size: 0.9rem;
            color: #aaa;
        }}
    </style>
</head>
<body>
    <div class="container">
        <a href="/insights/report/{scan.id}" class="back-link">&larr; Back to Full Report</a>

        <header>
            <h1>Orphaned Assets</h1>
            <p class="subtitle">JS/CSS files not registered in any asset bundle</p>
        </header>

        <div class="summary">
            <span class="summary-stat">Total: <strong>{total}</strong> orphaned assets</span>
            <span class="summary-stat">Showing: <strong>{(page-1)*50 + 1} - {min(page*50, total)}</strong></span>
            <span class="summary-stat">Page: <strong>{page}</strong> of <strong>{total_pages}</strong></span>
        </div>

        <table>
            <thead>
                <tr>
                    <th style="width: 60px;">#</th>
                    <th style="width: 80px;">Type</th>
                    <th>File Path</th>
                </tr>
            </thead>
            <tbody>
                {rows_html}
            </tbody>
        </table>

        {pagination_html}

        <div class="note">
            <strong>What are orphaned assets?</strong><br>
            These are JavaScript and CSS files that exist in your modules but are not included in any
            Odoo asset bundle (defined in <code>__manifest__.py</code>). This means they won't be loaded
            by Odoo and may be dead code, or they may need to be added to an appropriate bundle.
        </div>
    </div>
</body>
</html>'''

    def _generate_html_report(self, scan, report):
        """Generate the HTML report"""
        # Get findings by severity
        findings_by_severity = {
            'critical': [],
            'warning': [],
            'info': [],
            'recommendation': [],
        }
        for finding in scan.finding_ids:
            if finding.severity in findings_by_severity:
                findings_by_severity[finding.severity].append(finding)

        stats = report.get('statistics', {})
        summary = report.get('summary', {})

        html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SAM AI Ecosystem Health Report</title>
    <style>
        :root {{
            --sam-gold: #D4AF37;
            --sam-dark: #1a1a2e;
            --sam-darker: #0f0f1a;
            --sam-accent: #4a90d9;
            --success: #28a745;
            --warning: #ffc107;
            --danger: #dc3545;
            --info: #17a2b8;
        }}

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}

        body {{
            font-family: 'Segoe UI', system-ui, sans-serif;
            background: var(--sam-darker);
            color: #e0e0e0;
            line-height: 1.6;
            padding: 2rem;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}

        header {{
            text-align: center;
            margin-bottom: 2rem;
            padding-bottom: 1rem;
            border-bottom: 2px solid var(--sam-gold);
        }}

        h1 {{
            color: var(--sam-gold);
            font-size: 2rem;
            margin-bottom: 0.5rem;
        }}

        .subtitle {{
            color: #888;
            font-size: 0.9rem;
        }}

        .health-score {{
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 2rem;
            margin: 2rem 0;
        }}

        .score-circle {{
            width: 150px;
            height: 150px;
            border-radius: 50%;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            background: var(--sam-dark);
            border: 4px solid {self._get_score_color(scan.health_score)};
        }}

        .score-value {{
            font-size: 3rem;
            font-weight: bold;
            color: {self._get_score_color(scan.health_score)};
        }}

        .score-label {{
            font-size: 0.8rem;
            color: #888;
        }}

        .status-badge {{
            padding: 0.5rem 1.5rem;
            border-radius: 20px;
            font-weight: bold;
            background: {self._get_score_color(scan.health_score)}22;
            color: {self._get_score_color(scan.health_score)};
            border: 1px solid {self._get_score_color(scan.health_score)};
        }}

        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
            margin: 2rem 0;
        }}

        .stat-card {{
            background: var(--sam-dark);
            padding: 1.5rem;
            border-radius: 8px;
            text-align: center;
        }}

        .stat-value {{
            font-size: 2rem;
            font-weight: bold;
            color: var(--sam-gold);
        }}

        .stat-label {{
            color: #888;
            font-size: 0.85rem;
        }}

        .section {{
            margin: 2rem 0;
        }}

        .section-title {{
            color: var(--sam-gold);
            font-size: 1.3rem;
            margin-bottom: 1rem;
            padding-bottom: 0.5rem;
            border-bottom: 1px solid #333;
        }}

        .finding-list {{
            list-style: none;
        }}

        .finding-item {{
            background: var(--sam-dark);
            margin-bottom: 0.5rem;
            padding: 1rem;
            border-radius: 6px;
            border-left: 4px solid;
        }}

        .finding-item.critical {{
            border-left-color: var(--danger);
        }}

        .finding-item.warning {{
            border-left-color: var(--warning);
        }}

        .finding-item.info {{
            border-left-color: var(--info);
        }}

        .finding-item.recommendation {{
            border-left-color: var(--success);
        }}

        .finding-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 0.5rem;
        }}

        .finding-type {{
            font-weight: bold;
            color: #fff;
        }}

        .finding-severity {{
            font-size: 0.75rem;
            padding: 0.2rem 0.6rem;
            border-radius: 3px;
            text-transform: uppercase;
        }}

        .finding-severity.critical {{
            background: var(--danger);
            color: white;
        }}

        .finding-severity.warning {{
            background: var(--warning);
            color: #000;
        }}

        .finding-file {{
            font-family: monospace;
            font-size: 0.85rem;
            color: #888;
        }}

        .recommendation-card {{
            background: var(--sam-dark);
            padding: 1.5rem;
            border-radius: 8px;
            margin-bottom: 1rem;
            border-left: 4px solid var(--sam-gold);
        }}

        .recommendation-title {{
            font-weight: bold;
            color: #fff;
            margin-bottom: 0.5rem;
        }}

        .recommendation-meta {{
            display: flex;
            gap: 1rem;
            margin-top: 0.5rem;
            font-size: 0.8rem;
        }}

        .meta-tag {{
            padding: 0.2rem 0.5rem;
            border-radius: 3px;
            background: #333;
        }}

        .meta-tag.priority-critical {{ color: var(--danger); }}
        .meta-tag.priority-high {{ color: var(--warning); }}
        .meta-tag.priority-medium {{ color: var(--info); }}
        .meta-tag.priority-low {{ color: #888; }}

        .action-link {{
            display: inline-block;
            margin: 0.75rem 0;
            padding: 0.5rem 1rem;
            background: var(--sam-gold);
            color: #000;
            text-decoration: none;
            border-radius: 4px;
            font-weight: 600;
            font-size: 0.9rem;
            transition: background 0.2s;
        }}

        .action-link:hover {{
            background: #e5c04a;
        }}

        footer {{
            text-align: center;
            margin-top: 3rem;
            padding-top: 1rem;
            border-top: 1px solid #333;
            color: #666;
            font-size: 0.85rem;
        }}

        .empty-state {{
            text-align: center;
            padding: 2rem;
            color: #666;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>SAM AI Ecosystem Health Report</h1>
            <p class="subtitle">
                Generated: {scan.scan_date.strftime('%Y-%m-%d %H:%M:%S')} |
                Duration: {scan.duration_seconds:.2f}s |
                Path: {scan.base_path}
            </p>
        </header>

        <div class="health-score">
            <div class="score-circle">
                <span class="score-value">{scan.health_score}</span>
                <span class="score-label">/ 100</span>
            </div>
            <div class="status-badge">{scan.health_status}</div>
        </div>

        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-value">{scan.files_scanned}</div>
                <div class="stat-label">Files Scanned</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{scan.models_found}</div>
                <div class="stat-label">Models</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{scan.views_found}</div>
                <div class="stat-label">Views</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{scan.js_files_found + scan.css_files_found}</div>
                <div class="stat-label">Assets</div>
            </div>
            <div class="stat-card">
                <div class="stat-value" style="color: var(--danger)">{scan.critical_count}</div>
                <div class="stat-label">Critical Issues</div>
            </div>
            <div class="stat-card">
                <div class="stat-value" style="color: var(--warning)">{scan.warning_count}</div>
                <div class="stat-label">Warnings</div>
            </div>
        </div>

        {self._render_findings_section('Critical Issues', findings_by_severity['critical'], 'critical')}
        {self._render_findings_section('Warnings', findings_by_severity['warning'], 'warning')}
        {self._render_recommendations_section(findings_by_severity['recommendation'], scan.id)}

        <footer>
            <p>SAM AI Insights - Ecosystem Intelligence Tool</p>
            <p>Powered by ai_sam_insights module</p>
        </footer>
    </div>
</body>
</html>'''
        return html

    def _get_score_color(self, score):
        """Get color based on health score"""
        if score >= 90:
            return '#28a745'  # Green
        elif score >= 75:
            return '#8bc34a'  # Light green
        elif score >= 60:
            return '#ffc107'  # Yellow
        elif score >= 40:
            return '#ff9800'  # Orange
        else:
            return '#dc3545'  # Red

    def _render_findings_section(self, title, findings, severity):
        """Render a findings section"""
        if not findings:
            return ''

        items_html = ''
        for finding in findings[:20]:  # Limit to 20 items
            details = finding.get_details()
            file_path = finding.file_path or ''
            description = finding.description or details.get('recommendation', '')

            items_html += f'''
            <li class="finding-item {severity}">
                <div class="finding-header">
                    <span class="finding-type">{finding.finding_type or finding.category}</span>
                    <span class="finding-severity {severity}">{severity}</span>
                </div>
                <div class="finding-description">{description}</div>
                {f'<div class="finding-file">{file_path}</div>' if file_path else ''}
            </li>'''

        return f'''
        <section class="section">
            <h2 class="section-title">{title} ({len(findings)})</h2>
            <ul class="finding-list">
                {items_html}
            </ul>
        </section>'''

    def _render_recommendations_section(self, recommendations, scan_id):
        """Render recommendations section"""
        if not recommendations:
            return ''

        items_html = ''
        for rec in recommendations:
            priority_class = f'priority-{rec.priority}' if rec.priority else ''

            # Add clickable link for specific finding types
            action_link = ''
            if rec.finding_type == 'orphaned_assets':
                action_link = f'''
                <a href="/insights/orphaned-assets/{scan_id}" class="action-link">
                    View all orphaned assets &rarr;
                </a>'''
            elif rec.finding_type == 'orphaned_python':
                action_link = f'''
                <a href="/insights/orphaned-python/{scan_id}" class="action-link">
                    View orphaned Python files &rarr;
                </a>'''
            elif rec.finding_type == 'duplicate_functions':
                action_link = f'''
                <a href="/insights/duplicate-functions/{scan_id}" class="action-link">
                    View duplicate functions &rarr;
                </a>'''
            elif rec.finding_type in ('commented_code', 'commented_code_deletion'):
                action_link = f'''
                <a href="/insights/commented-code/{scan_id}" class="action-link">
                    View commented code blocks &rarr;
                </a>'''
            elif rec.finding_type == 'n8n_references':
                action_link = f'''
                <a href="/insights/integration-refs/{scan_id}?integration=n8n" class="action-link">
                    View N8N references &rarr;
                </a>'''
            elif rec.finding_type == 'automator_references':
                action_link = f'''
                <a href="/insights/integration-refs/{scan_id}?integration=ai_automator" class="action-link">
                    View ai_automator references &rarr;
                </a>'''

            items_html += f'''
            <div class="recommendation-card">
                <div class="recommendation-title">{rec.title}</div>
                <div class="recommendation-description">{rec.description}</div>
                {action_link}
                <div class="recommendation-meta">
                    <span class="meta-tag {priority_class}">Priority: {rec.priority or 'N/A'}</span>
                    <span class="meta-tag">Effort: {rec.effort or 'N/A'}</span>
                    <span class="meta-tag">Impact: {rec.impact or 'N/A'}</span>
                </div>
            </div>'''

        return f'''
        <section class="section">
            <h2 class="section-title">Recommendations ({len(recommendations)})</h2>
            {items_html}
        </section>'''
