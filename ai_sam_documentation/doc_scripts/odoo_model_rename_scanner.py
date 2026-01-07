#!/usr/bin/env python3
"""
Odoo Module Rename Scanner - Phase 1 & 2 Combined
Safe diagnostic tool for finding all occurrences of model names before renaming.

Usage: python odoo_model_rename_scanner.py

This tool will:
1. Scan the entire module for all references to 'workflow_template_v2'
2. Generate a comprehensive CSV report for review
3. Provide risk assessment and recommendations

Author: Claude Code Assistant
Date: 2025-09-07
"""

import os
import re
import csv
import json
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import List, Dict, Tuple
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class OdooModelRenameScanner:
    def __init__(self, module_path: str, old_name: str, new_name: str):
        self.module_path = Path(module_path)
        self.old_name = old_name
        self.new_name = new_name
        self.results = []
        
        # Define file extensions to scan
        self.extensions = {
            '.py': 'Python',
            '.xml': 'XML',
            '.csv': 'CSV',
            '.js': 'JavaScript',
            '.css': 'CSS',
            '.scss': 'SCSS',
            '.yml': 'YAML',
            '.json': 'JSON',
            '.md': 'Markdown',
            '.rst': 'RestructuredText'
        }
        
        # Define search patterns with their risk levels
        self.patterns = [
            # High Risk - Critical Odoo Model References
            (r'_name\s*=\s*["\']([^"\']*' + re.escape(old_name) + r'[^"\']*)["\']', 'HIGH', 'Model _name definition'),
            (r'_inherit\s*=\s*["\']([^"\']*' + re.escape(old_name) + r'[^"\']*)["\']', 'HIGH', 'Model _inherit definition'),
            (r'comodel_name\s*=\s*["\']([^"\']*' + re.escape(old_name) + r'[^"\']*)["\']', 'HIGH', 'Field comodel_name'),
            (r'relation\s*=\s*["\']([^"\']*' + re.escape(old_name) + r'[^"\']*)["\']', 'HIGH', 'Many2many relation'),
            (r'res_model\s*=\s*["\']([^"\']*' + re.escape(old_name) + r'[^"\']*)["\']', 'HIGH', 'XML res_model (Action/View)'),
            (r'model\s*=\s*["\']([^"\']*' + re.escape(old_name) + r'[^"\']*)["\']', 'HIGH', 'XML model attribute'),
            
            # Medium Risk - References that need updating
            (r'self\.env\[["\']([^"\']*' + re.escape(old_name) + r'[^"\']*)["\']\]', 'MEDIUM', 'Environment reference self.env[]'),
            (r'search\(["\']([^"\']*' + re.escape(old_name) + r'[^"\']*)["\']', 'MEDIUM', 'XML search domain'),
            (r'ref\(["\']([^"\']*' + re.escape(old_name) + r'[^"\']*)["\']', 'MEDIUM', 'XML ref() function'),
            (r'class\s+\w*' + re.escape(old_name.replace('_', '').replace('.', '').title()) + r'\w*', 'MEDIUM', 'Python class name'),
            
            # Low Risk - Comments, strings, documentation
            (re.escape(old_name), 'LOW', 'General text occurrence'),
        ]
    
    def scan_file(self, file_path: Path) -> List[Dict]:
        """Scan a single file for all patterns"""
        results = []
        
        try:
            # Handle different file encodings
            encodings = ['utf-8', 'latin-1', 'cp1252']
            content = None
            
            for encoding in encodings:
                try:
                    with open(file_path, 'r', encoding=encoding) as f:
                        content = f.read()
                    break
                except UnicodeDecodeError:
                    continue
            
            if content is None:
                logger.warning(f"Could not read file with any encoding: {file_path}")
                return results
            
            lines = content.split('\n')
            
            # Apply all patterns to the content
            for pattern, risk_level, description in self.patterns:
                try:
                    matches = re.finditer(pattern, content, re.IGNORECASE | re.MULTILINE)
                    for match in matches:
                        # Find line number
                        line_num = content[:match.start()].count('\n') + 1
                        
                        # Get context (3 lines before and after)
                        start_line = max(0, line_num - 4)
                        end_line = min(len(lines), line_num + 3)
                        context_lines = lines[start_line:end_line]
                        
                        # Highlight the matching line
                        highlight_index = line_num - start_line - 1
                        if 0 <= highlight_index < len(context_lines):
                            context_lines[highlight_index] = f">>> {context_lines[highlight_index]} <<<"
                        
                        context = '\n'.join(context_lines)
                        
                        results.append({
                            'file_path': str(file_path.relative_to(self.module_path)),
                            'line_number': line_num,
                            'match_text': match.group(0),
                            'context': context,
                            'risk_level': risk_level,
                            'reference_type': description,
                            'file_type': self.extensions.get(file_path.suffix, 'Unknown'),
                            'pattern_matched': pattern
                        })
                except re.error as e:
                    logger.warning(f"Regex error in pattern '{pattern}': {e}")
                    
        except Exception as e:
            logger.error(f"Error scanning file {file_path}: {e}")
            
        return results
    
    def scan_xml_specific(self, file_path: Path) -> List[Dict]:
        """Additional XML-specific scanning for Odoo patterns"""
        results = []
        
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
            
            # Look for specific Odoo XML patterns
            xml_patterns = [
                ('.//record[@model]', 'model', 'HIGH', 'XML record model'),
                ('.//field[@comodel_name]', 'comodel_name', 'HIGH', 'XML field comodel_name'),
                ('.//field[@relation]', 'relation', 'HIGH', 'XML field relation'),
                ('.//menuitem[@action]', 'action', 'MEDIUM', 'XML menuitem action'),
                ('.//act_window[@res_model]', 'res_model', 'HIGH', 'XML act_window res_model'),
            ]
            
            for xpath, attr, risk, desc in xml_patterns:
                elements = root.findall(xpath)
                for elem in elements:
                    attr_value = elem.get(attr, '')
                    if self.old_name in attr_value:
                        # Try to get line number (approximate)
                        line_num = getattr(elem, 'sourceline', 0) or 1
                        
                        results.append({
                            'file_path': str(file_path.relative_to(self.module_path)),
                            'line_number': line_num,
                            'match_text': f'{attr}="{attr_value}"',
                            'context': f'XML element: {elem.tag} with {attr}="{attr_value}"',
                            'risk_level': risk,
                            'reference_type': desc,
                            'file_type': 'XML',
                            'pattern_matched': f'XML:{xpath}[@{attr}]'
                        })
                        
        except ET.ParseError as e:
            logger.warning(f"Could not parse XML file {file_path}: {e}")
        except Exception as e:
            logger.error(f"Error in XML-specific scan of {file_path}: {e}")
            
        return results
    
    def scan_csv_specific(self, file_path: Path) -> List[Dict]:
        """Scan CSV files (often used for security rules)"""
        results = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                csv_reader = csv.reader(f)
                for line_num, row in enumerate(csv_reader, 1):
                    for col_num, cell in enumerate(row):
                        if self.old_name in cell:
                            results.append({
                                'file_path': str(file_path.relative_to(self.module_path)),
                                'line_number': line_num,
                                'match_text': cell,
                                'context': f'CSV row {line_num}, column {col_num + 1}: {row}',
                                'risk_level': 'HIGH' if 'access' in file_path.name else 'MEDIUM',
                                'reference_type': 'CSV security/data file',
                                'file_type': 'CSV',
                                'pattern_matched': 'CSV cell content'
                            })
        except Exception as e:
            logger.error(f"Error scanning CSV file {file_path}: {e}")
            
        return results
    
    def scan_module(self) -> None:
        """Scan the entire module"""
        logger.info(f"Starting scan of module: {self.module_path}")
        logger.info(f"Looking for references to: {self.old_name}")
        
        total_files = 0
        scanned_files = 0
        
        # Walk through all files in the module
        for file_path in self.module_path.rglob('*'):
            if file_path.is_file():
                total_files += 1
                
                # Skip certain directories/files
                if any(part in str(file_path) for part in ['.git', '__pycache__', '.pyc', '.log']):
                    continue
                
                file_results = []
                
                # Regular pattern scanning for all files
                if file_path.suffix in self.extensions:
                    file_results.extend(self.scan_file(file_path))
                    scanned_files += 1
                
                # Special handling for specific file types
                if file_path.suffix == '.xml':
                    file_results.extend(self.scan_xml_specific(file_path))
                elif file_path.suffix == '.csv':
                    file_results.extend(self.scan_csv_specific(file_path))
                
                self.results.extend(file_results)
                
                if file_results:
                    logger.info(f"Found {len(file_results)} matches in {file_path.name}")
        
        logger.info(f"Scan complete: {scanned_files}/{total_files} files scanned")
        logger.info(f"Total matches found: {len(self.results)}")
    
    def generate_report(self, output_file: str = 'workflow_template_v2_rename_analysis.csv') -> None:
        """Generate comprehensive CSV report"""
        
        # Sort results by risk level and file path
        risk_order = {'HIGH': 0, 'MEDIUM': 1, 'LOW': 2}
        self.results.sort(key=lambda x: (risk_order.get(x['risk_level'], 3), x['file_path']))
        
        # Write CSV report
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = [
                'risk_level', 'reference_type', 'file_path', 'file_type', 
                'line_number', 'match_text', 'context', 'pattern_matched'
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for result in self.results:
                # Clean context for CSV (remove newlines, limit length)
                context = result['context'].replace('\n', ' | ').replace('\r', '')
                if len(context) > 200:
                    context = context[:200] + '...'
                
                writer.writerow({
                    'risk_level': result['risk_level'],
                    'reference_type': result['reference_type'],
                    'file_path': result['file_path'],
                    'file_type': result['file_type'],
                    'line_number': result['line_number'],
                    'match_text': result['match_text'],
                    'context': context,
                    'pattern_matched': result['pattern_matched']
                })
        
        logger.info(f"Report generated: {output_file}")
        
        # Generate summary
        self.generate_summary(output_file.replace('.csv', '_summary.txt'))
    
    def generate_summary(self, output_file: str) -> None:
        """Generate a summary report"""
        
        # Count by risk level
        risk_counts = {'HIGH': 0, 'MEDIUM': 0, 'LOW': 0}
        file_counts = {}
        type_counts = {}
        
        for result in self.results:
            risk_counts[result['risk_level']] += 1
            
            file_path = result['file_path']
            if file_path not in file_counts:
                file_counts[file_path] = 0
            file_counts[file_path] += 1
            
            ref_type = result['reference_type']
            if ref_type not in type_counts:
                type_counts[ref_type] = 0
            type_counts[ref_type] += 1
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("ODOO MODEL RENAME ANALYSIS SUMMARY\n")
            f.write("="*50 + "\n\n")
            
            f.write(f"Target: {self.old_name} → {self.new_name}\n")
            f.write(f"Module Path: {self.module_path}\n")
            f.write(f"Total Matches: {len(self.results)}\n\n")
            
            f.write("RISK LEVEL BREAKDOWN:\n")
            f.write("-" * 25 + "\n")
            for risk, count in risk_counts.items():
                f.write(f"{risk:8}: {count:4} matches\n")
            
            f.write("\nTOP FILES WITH MATCHES:\n")
            f.write("-" * 25 + "\n")
            sorted_files = sorted(file_counts.items(), key=lambda x: x[1], reverse=True)[:10]
            for file_path, count in sorted_files:
                f.write(f"{count:3} matches: {file_path}\n")
            
            f.write("\nREFERENCE TYPE BREAKDOWN:\n")
            f.write("-" * 30 + "\n")
            sorted_types = sorted(type_counts.items(), key=lambda x: x[1], reverse=True)
            for ref_type, count in sorted_types:
                f.write(f"{count:3}: {ref_type}\n")
            
            f.write("\nHIGH RISK ITEMS (REQUIRE CAREFUL REVIEW):\n")
            f.write("-" * 45 + "\n")
            high_risk = [r for r in self.results if r['risk_level'] == 'HIGH']
            for result in high_risk[:20]:  # Show first 20 high risk items
                f.write(f"• {result['file_path']}:{result['line_number']} - {result['reference_type']}\n")
                f.write(f"  Match: {result['match_text']}\n\n")
            
            if len(high_risk) > 20:
                f.write(f"... and {len(high_risk) - 20} more high risk items (see CSV for full list)\n")
            
            f.write("\nRECOMMENDATIONS:\n")
            f.write("-" * 15 + "\n")
            f.write("1. Review all HIGH risk items first - these are critical Odoo model references\n")
            f.write("2. MEDIUM risk items need updating but are less likely to break the module\n")
            f.write("3. LOW risk items are mostly comments/docs - update for consistency\n")
            f.write("4. Test in a development environment first\n")
            f.write("5. Consider database migration if _name is changed\n")
        
        logger.info(f"Summary generated: {output_file}")

def main():
    """Main execution function"""
    
    # Configuration - you can modify these
    MODULE_PATH = r"C:\Working With AI\Odoo Projects\custom-modules-v18\the_ai_automator"
    OLD_NAME = "workflow_template_v2"
    NEW_NAME = "workflow_templates"  # What we want to rename to
    
    print("ODOO MODEL RENAME SCANNER")
    print("=" * 40)
    print(f"Module: {MODULE_PATH}")
    print(f"Target: {OLD_NAME} -> {NEW_NAME}")
    print(f"Starting comprehensive scan...\n")
    
    # Create scanner and run
    scanner = OdooModelRenameScanner(MODULE_PATH, OLD_NAME, NEW_NAME)
    scanner.scan_module()
    
    # Generate reports
    scanner.generate_report()
    
    print(f"\nScan complete!")
    print(f"Found {len(scanner.results)} total matches")
    print(f"Reports generated:")
    print(f"   - workflow_template_v2_rename_analysis.csv (detailed)")
    print(f"   - workflow_template_v2_rename_analysis_summary.txt (summary)")
    print(f"\nIMPORTANT: Review the reports before making any changes!")
    print(f"Focus on HIGH risk items first - these could break your module")

if __name__ == "__main__":
    main()