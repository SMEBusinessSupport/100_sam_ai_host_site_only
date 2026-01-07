# -*- coding: utf-8 -*-
"""
Ecosystem Analyzer for SAM AI Insights

The main orchestrator that runs all scanners and analyzers,
then produces a comprehensive ecosystem health report.
"""
import os
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
import logging

from ..scanners.python_scanner import PythonScanner
from ..scanners.xml_scanner import XMLScanner
from ..scanners.asset_scanner import AssetScanner
from .duplicate_analyzer import DuplicateAnalyzer
from .orphan_analyzer import OrphanAnalyzer
from .relationship_mapper import RelationshipMapper
from .commented_code_analyzer import CommentedCodeAnalyzer
from .integration_reference_analyzer import IntegrationReferenceAnalyzer
from .external_path_analyzer import ExternalPathAnalyzer

_logger = logging.getLogger(__name__)


class EcosystemAnalyzer:
    """
    Main analyzer that orchestrates all scans and analyses.

    This is the entry point for running a complete ecosystem analysis.
    """

    def __init__(self, base_path: str, module_filter: Optional[List[str]] = None):
        """
        Initialize the ecosystem analyzer.

        :param base_path: Root directory to scan (usually the addons path)
        :param module_filter: Optional list of module names to include
        """
        self.base_path = Path(base_path)
        self.module_filter = module_filter or []

        # Results storage
        self.python_scan = {}
        self.xml_scan = {}
        self.asset_scan = {}
        self.registry_scan = {}
        self.duplicate_findings = {}
        self.orphan_findings = {}
        self.commented_code_findings = {}
        self.integration_references = {}
        self.external_path_findings = {}
        self.relationships = {}

        # Final report
        self.report = {
            'scan_date': None,
            'base_path': str(self.base_path),
            'modules_analyzed': [],
            'health_score': 0,
            'summary': {},
            'critical_issues': [],
            'warnings': [],
            'recommendations': [],
            'statistics': {},
        }

    def analyze(self, include_registry: bool = False, env=None) -> Dict[str, Any]:
        """
        Run the complete ecosystem analysis.

        :param include_registry: Whether to include Odoo runtime registry scan
        :param env: Odoo environment (required if include_registry is True)
        :return: Complete analysis report
        """
        start_time = datetime.now()
        _logger.info(f"Starting ecosystem analysis of {self.base_path}")

        # Phase 1: Static Scanning
        self._run_python_scan()
        self._run_xml_scan()
        self._run_asset_scan()

        # Phase 2: Runtime Scanning (optional)
        if include_registry and env:
            self._run_registry_scan(env)

        # Phase 3: Analysis
        self._run_duplicate_analysis()
        self._run_orphan_analysis()
        self._run_commented_code_analysis()
        self._run_integration_reference_analysis()
        self._run_external_path_analysis()
        self._run_relationship_mapping()

        # Phase 4: Report Generation
        self._generate_report()

        # Calculate duration
        duration = (datetime.now() - start_time).total_seconds()
        self.report['analysis_duration_seconds'] = duration

        _logger.info(f"Ecosystem analysis complete in {duration:.2f}s. Health score: {self.report['health_score']}/100")

        return self.report

    def _run_python_scan(self):
        """Run Python AST scanner"""
        _logger.info("Phase 1a: Scanning Python files...")
        scanner = PythonScanner(str(self.base_path), self.module_filter)
        self.python_scan = scanner.scan()

    def _run_xml_scan(self):
        """Run XML scanner"""
        _logger.info("Phase 1b: Scanning XML files...")
        scanner = XMLScanner(str(self.base_path), self.module_filter)
        self.xml_scan = scanner.scan()

    def _run_asset_scan(self):
        """Run JS/CSS asset scanner"""
        _logger.info("Phase 1c: Scanning JS/CSS assets...")
        scanner = AssetScanner(str(self.base_path), self.module_filter)
        self.asset_scan = scanner.scan()

    def _run_registry_scan(self, env):
        """Run Odoo registry scanner"""
        from ..scanners.registry_scanner import RegistryScanner
        _logger.info("Phase 2: Scanning Odoo registry...")
        scanner = RegistryScanner(env)
        self.registry_scan = scanner.scan(self.module_filter)

    def _run_duplicate_analysis(self):
        """Run duplicate detection"""
        _logger.info("Phase 3a: Analyzing duplicates...")
        analyzer = DuplicateAnalyzer(self.python_scan, self.xml_scan, self.asset_scan)
        self.duplicate_findings = analyzer.analyze()

    def _run_orphan_analysis(self):
        """Run orphan detection"""
        _logger.info("Phase 3b: Analyzing orphans...")
        analyzer = OrphanAnalyzer(
            self.python_scan, self.xml_scan, self.asset_scan, self.registry_scan
        )
        self.orphan_findings = analyzer.analyze()

    def _run_commented_code_analysis(self):
        """Run commented code detection"""
        _logger.info("Phase 3c: Analyzing commented code...")
        analyzer = CommentedCodeAnalyzer(str(self.base_path), self.module_filter)
        self.commented_code_findings = analyzer.analyze()

    def _run_integration_reference_analysis(self):
        """Run integration reference detection (N8N, ai_automator)"""
        _logger.info("Phase 3d: Analyzing integration references...")
        analyzer = IntegrationReferenceAnalyzer(str(self.base_path), self.module_filter)
        self.integration_references = analyzer.analyze()

    def _run_external_path_analysis(self):
        """Run external path reference detection - finds architectural violations"""
        _logger.info("Phase 3e: Analyzing external path references...")
        analyzer = ExternalPathAnalyzer(str(self.base_path), self.module_filter)
        self.external_path_findings = analyzer.analyze()

    def _run_relationship_mapping(self):
        """Run relationship mapping"""
        _logger.info("Phase 3e: Mapping relationships...")
        mapper = RelationshipMapper(
            self.python_scan, self.xml_scan, self.asset_scan, self.registry_scan
        )
        self.relationships = mapper.map()

    def _generate_report(self):
        """Generate the final report"""
        _logger.info("Phase 4: Generating report...")

        self.report['scan_date'] = datetime.now().isoformat()
        self.report['modules_analyzed'] = self._get_modules_analyzed()

        # Gather statistics
        self.report['statistics'] = self._gather_statistics()

        # Gather issues by severity
        self._categorize_issues()

        # Generate recommendations
        self._generate_recommendations()

        # Calculate health score
        self.report['health_score'] = self._calculate_health_score()

        # Generate summary
        self.report['summary'] = self._generate_summary()

    def _get_modules_analyzed(self) -> List[str]:
        """Get list of modules that were analyzed"""
        modules = set()

        for model in self.python_scan.get('models', []):
            path = model.get('relative_path', '')
            parts = path.replace('\\', '/').split('/')
            if parts:
                modules.add(parts[0])

        return sorted(list(modules))

    def _gather_statistics(self) -> Dict[str, Any]:
        """Gather all statistics"""
        return {
            'python': {
                'files_scanned': self.python_scan.get('files_scanned', 0),
                'models': len(self.python_scan.get('models', [])),
                'functions': len(self.python_scan.get('functions', [])),
                'total_fields': sum(
                    len(m.get('fields', [])) for m in self.python_scan.get('models', [])
                ),
                'total_methods': sum(
                    len(m.get('methods', [])) for m in self.python_scan.get('models', [])
                ),
                'errors': len(self.python_scan.get('errors', [])),
            },
            'xml': {
                'files_scanned': self.xml_scan.get('files_scanned', 0),
                'views': len(self.xml_scan.get('views', [])),
                'actions': len(self.xml_scan.get('actions', [])),
                'menus': len(self.xml_scan.get('menus', [])),
                'templates': len(self.xml_scan.get('templates', [])),
                'inherited_views': len(self.xml_scan.get('inherited_views', [])),
                'errors': len(self.xml_scan.get('errors', [])),
            },
            'assets': {
                'files_scanned': self.asset_scan.get('files_scanned', 0),
                'js_files': len(self.asset_scan.get('js_files', [])),
                'css_files': len(self.asset_scan.get('css_files', [])),
                'owl_components': len(self.asset_scan.get('owl_components', [])),
                'css_classes': len(self.asset_scan.get('css_classes', [])),
                'orphaned_assets': len(self.asset_scan.get('orphaned_assets', [])),
            },
            'duplicates': self.duplicate_findings.get('summary', {}),
            'orphans': self.orphan_findings.get('summary', {}),
            'commented_code': self.commented_code_findings.get('summary', {}),
            'integration_references': self.integration_references.get('summary', {}),
            'relationships': self.relationships.get('summary', {}),
        }

    def _categorize_issues(self):
        """Categorize all issues by severity"""
        critical = []
        warnings = []

        # Process duplicate findings
        for category in ['duplicate_models', 'duplicate_functions', 'duplicate_methods',
                        'duplicate_css_classes', 'duplicate_views', 'renamed_components']:
            for item in self.duplicate_findings.get(category, []):
                severity = item.get('severity', 'info')
                issue = {
                    'category': 'duplicate',
                    'type': category,
                    'details': item,
                }
                if severity == 'error':
                    critical.append(issue)
                elif severity == 'warning':
                    warnings.append(issue)

        # Process orphan findings
        for category in ['orphaned_python_files', 'orphaned_models', 'orphaned_views',
                        'orphaned_actions', 'orphaned_menus', 'dangling_field_refs',
                        'dangling_model_refs', 'orphaned_assets']:
            for item in self.orphan_findings.get(category, []):
                severity = item.get('severity', 'info')
                issue = {
                    'category': 'orphan',
                    'type': category,
                    'details': item,
                }
                if severity == 'error':
                    critical.append(issue)
                elif severity == 'warning':
                    warnings.append(issue)

        # Process commented code findings
        for file_type in ['python', 'javascript', 'xml']:
            for item in self.commented_code_findings.get(file_type, []):
                severity = item.get('severity', 'info')
                issue = {
                    'category': 'commented_code',
                    'type': item.get('finding_type', f'commented_{file_type}'),
                    'details': item,
                }
                if severity == 'error':
                    critical.append(issue)
                elif severity == 'warning':
                    warnings.append(issue)

        # Process external path findings - CRITICAL architectural violations
        for category in ['hardcoded_external_paths', 'relative_path_escapes',
                        'suspicious_file_operations', 'external_imports']:
            for item in self.external_path_findings.get(category, []):
                severity = item.get('severity', 'warning')
                issue = {
                    'category': 'external_path',
                    'type': category,
                    'details': item,
                }
                # External path references are always serious
                if severity == 'critical':
                    critical.append(issue)
                else:
                    warnings.append(issue)

        self.report['critical_issues'] = critical
        self.report['warnings'] = warnings

    def _generate_recommendations(self):
        """Generate actionable recommendations"""
        recommendations = []

        # Based on duplicates
        dup_summary = self.duplicate_findings.get('summary', {})
        if dup_summary.get('duplicate_functions', 0) > 5:
            recommendations.append({
                'priority': 'high',
                'category': 'code_quality',
                'type': 'duplicate_functions',
                'title': 'Consolidate Duplicate Functions',
                'description': f"Found {dup_summary['duplicate_functions']} duplicate functions. "
                             "Consider creating shared utility modules.",
                'effort': 'medium',
                'impact': 'Reduced code maintenance burden',
            })

        if dup_summary.get('similar_models', 0) > 3:
            recommendations.append({
                'priority': 'medium',
                'category': 'architecture',
                'type': 'similar_models',
                'title': 'Review Similar Models',
                'description': f"Found {dup_summary['similar_models']} pairs of similar models. "
                             "Consider using inheritance or mixins.",
                'effort': 'high',
                'impact': 'Cleaner data model, easier maintenance',
            })

        if dup_summary.get('renamed_components', 0) > 5:
            recommendations.append({
                'priority': 'low',
                'category': 'cleanup',
                'type': 'renamed_components',
                'title': 'Clean Up Renamed Components',
                'description': f"Found {dup_summary['renamed_components']} components with "
                             "rename patterns (_old, _v2, etc.). Review and remove if unused.",
                'effort': 'low',
                'impact': 'Cleaner codebase',
            })

        # Based on orphans
        orphan_summary = self.orphan_findings.get('summary', {})
        if orphan_summary.get('dangling_model_refs', 0) > 0:
            recommendations.append({
                'priority': 'critical',
                'category': 'bug_fix',
                'type': 'dangling_model_refs',
                'title': 'Fix Dangling Model References',
                'description': f"Found {orphan_summary['dangling_model_refs']} references to "
                             "non-existent models. These will cause runtime errors.",
                'effort': 'medium',
                'impact': 'Prevent runtime errors',
            })

        if orphan_summary.get('orphaned_assets', 0) > 10:
            recommendations.append({
                'priority': 'low',
                'category': 'cleanup',
                'type': 'orphaned_assets',
                'title': 'Clean Up Orphaned Assets',
                'description': f"Found {orphan_summary['orphaned_assets']} JS/CSS files not in "
                             "any asset bundle. Add to bundles or remove.",
                'effort': 'low',
                'impact': 'Smaller codebase, clearer asset management',
            })

        if orphan_summary.get('orphaned_python_files', 0) > 5:
            recommendations.append({
                'priority': 'medium',
                'category': 'cleanup',
                'type': 'orphaned_python',
                'title': 'Review Orphaned Python Files',
                'description': f"Found {orphan_summary['orphaned_python_files']} Python files not "
                             "imported in __init__.py. Verify if intentional or dead code.",
                'effort': 'low',
                'impact': 'Cleaner codebase, reduced confusion',
            })

        # Based on relationships
        rel_summary = self.relationships.get('summary', {})
        incomplete_traces = rel_summary.get('incomplete_traces', 0)
        if incomplete_traces > 5:
            recommendations.append({
                'priority': 'medium',
                'category': 'ux',
                'type': 'incomplete_traces',
                'title': 'Complete Model UI Traces',
                'description': f"Found {incomplete_traces} models with incomplete UI paths "
                             "(missing views, actions, or menus).",
                'effort': 'medium',
                'impact': 'Better user experience, complete features',
            })

        # Based on commented code
        cc_summary = self.commented_code_findings.get('summary', {})
        total_commented = cc_summary.get('total_commented_blocks', 0)
        deletion_markers = cc_summary.get('deletion_markers_found', 0)

        if deletion_markers > 0:
            recommendations.append({
                'priority': 'high',
                'category': 'cleanup',
                'type': 'commented_code_deletion',
                'title': 'Remove Code Marked for Deletion',
                'description': f"Found {deletion_markers} comments with deletion markers "
                             "(TODO delete, DEPRECATED, OLD, etc.). Review and remove dead code.",
                'effort': 'low',
                'impact': 'Cleaner codebase, reduced technical debt',
            })

        if total_commented > 10:
            recommendations.append({
                'priority': 'medium',
                'category': 'cleanup',
                'type': 'commented_code',
                'title': 'Review Commented Code Blocks',
                'description': f"Found {total_commented} blocks of commented-out code across "
                             f"{cc_summary.get('files_with_commented_code', 0)} files. "
                             "Review and remove if no longer needed.",
                'effort': 'low',
                'impact': 'Cleaner codebase, easier maintenance',
            })

        # Based on integration references
        int_summary = self.integration_references.get('summary', {})
        n8n_refs = int_summary.get('total_n8n_references', 0)
        automator_refs = int_summary.get('total_automator_references', 0)

        if n8n_refs > 0:
            recommendations.append({
                'priority': 'low',
                'category': 'documentation',
                'type': 'n8n_references',
                'title': 'Document N8N Integration Points',
                'description': f"Found {n8n_refs} N8N references across "
                             f"{int_summary.get('files_with_n8n_refs', 0)} files. "
                             "Review integration points for proper documentation.",
                'effort': 'low',
                'impact': 'Better integration visibility and maintenance',
            })

        if automator_refs > 0:
            recommendations.append({
                'priority': 'low',
                'category': 'documentation',
                'type': 'automator_references',
                'title': 'Document ai_automator Integration Points',
                'description': f"Found {automator_refs} ai_automator references across "
                             f"{int_summary.get('files_with_automator_refs', 0)} files. "
                             "Review integration points for proper documentation.",
                'effort': 'low',
                'impact': 'Better integration visibility and maintenance',
            })

        # Based on external path references - CRITICAL architectural violations
        ext_summary = self.external_path_findings.get('summary', {})
        hardcoded_paths = ext_summary.get('hardcoded_external_paths', 0)
        relative_escapes = ext_summary.get('relative_path_escapes', 0)
        suspicious_ops = ext_summary.get('suspicious_file_operations', 0)
        external_imports = ext_summary.get('external_imports', 0)

        if hardcoded_paths > 0:
            recommendations.append({
                'priority': 'critical',
                'category': 'architecture',
                'type': 'external_path_hardcoded',
                'title': 'CRITICAL: Remove Hardcoded External Paths',
                'description': f"Found {hardcoded_paths} hardcoded paths to external repositories. "
                             "This breaks module portability and violates Odoo architecture. "
                             "Refactor to use module dependencies or Odoo's file system.",
                'effort': 'high',
                'impact': 'Module portability, proper architecture, deployment safety',
            })

        if relative_escapes > 0:
            recommendations.append({
                'priority': 'high',
                'category': 'architecture',
                'type': 'external_path_relative',
                'title': 'Fix Relative Path Escapes',
                'description': f"Found {relative_escapes} relative paths that escape module boundaries. "
                             "Use odoo.modules.get_module_path() or __file__ based paths instead.",
                'effort': 'medium',
                'impact': 'Module isolation, predictable behavior',
            })

        if suspicious_ops > 0:
            recommendations.append({
                'priority': 'high',
                'category': 'architecture',
                'type': 'external_file_operations',
                'title': 'Review Suspicious File Operations',
                'description': f"Found {suspicious_ops} file operations targeting external locations. "
                             "Verify these are intentional and properly scoped.",
                'effort': 'medium',
                'impact': 'Security, module isolation',
            })

        self.report['recommendations'] = sorted(
            recommendations,
            key=lambda x: {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}[x['priority']]
        )

    def _calculate_health_score(self) -> int:
        """Calculate overall ecosystem health score (0-100)"""
        score = 100

        # Deduct for critical issues
        score -= len(self.report['critical_issues']) * 10

        # Deduct for warnings
        score -= len(self.report['warnings']) * 2

        # Deduct for duplicates
        dup_summary = self.duplicate_findings.get('summary', {})
        score -= dup_summary.get('total_issues', 0) * 0.5

        # Deduct for orphans
        orphan_summary = self.orphan_findings.get('summary', {})
        score -= orphan_summary.get('total_issues', 0) * 0.3

        # Deduct HEAVILY for external path violations - these are architecture red flags
        ext_summary = self.external_path_findings.get('summary', {})
        score -= ext_summary.get('hardcoded_external_paths', 0) * 15  # Very serious
        score -= ext_summary.get('relative_path_escapes', 0) * 10     # Serious
        score -= ext_summary.get('suspicious_file_operations', 0) * 8 # Concerning
        score -= ext_summary.get('external_imports', 0) * 5           # Moderate

        # Deduct for scan errors
        stats = self.report.get('statistics', {})
        score -= stats.get('python', {}).get('errors', 0) * 2
        score -= stats.get('xml', {}).get('errors', 0) * 2

        # Ensure score is between 0 and 100
        return max(0, min(100, int(score)))

    def _generate_summary(self) -> Dict[str, Any]:
        """Generate executive summary"""
        stats = self.report['statistics']

        return {
            'total_files_scanned': (
                stats.get('python', {}).get('files_scanned', 0) +
                stats.get('xml', {}).get('files_scanned', 0) +
                stats.get('assets', {}).get('files_scanned', 0)
            ),
            'total_models': stats.get('python', {}).get('models', 0),
            'total_views': stats.get('xml', {}).get('views', 0),
            'total_issues': (
                len(self.report['critical_issues']) +
                len(self.report['warnings'])
            ),
            'critical_count': len(self.report['critical_issues']),
            'warning_count': len(self.report['warnings']),
            'recommendation_count': len(self.report['recommendations']),
            'health_status': self._get_health_status(),
        }

    def _get_health_status(self) -> str:
        """Get health status label based on score"""
        score = self.report['health_score']
        if score >= 90:
            return 'Excellent'
        elif score >= 75:
            return 'Good'
        elif score >= 60:
            return 'Fair'
        elif score >= 40:
            return 'Poor'
        else:
            return 'Critical'

    def export_json(self, output_path: str) -> str:
        """Export the report to JSON file"""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.report, f, indent=2, default=str)
        return output_path

    def get_full_results(self) -> Dict[str, Any]:
        """Get all raw results for detailed analysis"""
        return {
            'report': self.report,
            'python_scan': self.python_scan,
            'xml_scan': self.xml_scan,
            'asset_scan': self.asset_scan,
            'registry_scan': self.registry_scan,
            'duplicate_findings': self.duplicate_findings,
            'orphan_findings': self.orphan_findings,
            'commented_code_findings': self.commented_code_findings,
            'integration_references': self.integration_references,
            'external_path_findings': self.external_path_findings,
            'relationships': self.relationships,
        }
