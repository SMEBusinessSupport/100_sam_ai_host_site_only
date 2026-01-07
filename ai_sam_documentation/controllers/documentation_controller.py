from odoo import http
from odoo.http import request, Response
from pathlib import Path
import mimetypes
import logging

# Optional markdown import - fallback to plain text if not available
try:
    import markdown
    MARKDOWN_AVAILABLE = True
except ImportError:
    MARKDOWN_AVAILABLE = False

_logger = logging.getLogger(__name__)

class DocumentationController(http.Controller):

    @http.route('/ai_automator/docs/scan', type='http', auth='user', methods=['GET'])
    def scan_documentation(self):
        """Trigger documentation folder scan"""
        try:
            doc_manager = request.env['ai.automator.documentation']
            doc_manager.scan_documentation_folder()
            return Response("Documentation scan completed", status=200)
        except Exception as e:
            _logger.error(f"Documentation scan error: {e}")
            return Response(f"Scan failed: {e}", status=500)

    @http.route('/ai_automator/docs/view/<int:doc_id>', type='http', auth='user')
    def view_document(self, doc_id):
        """View document in browser"""
        try:
            doc = request.env['ai.automator.documentation'].browse(doc_id)
            if not doc.exists():
                return Response("Document not found", status=404)

            file_path = self._get_full_path(doc.file_path)
            if not file_path.exists():
                return Response("File not found", status=404)

            content = file_path.read_text(encoding='utf-8')

            if doc.file_type == 'markdown':
                # Convert markdown to HTML if available, otherwise show as formatted text
                if MARKDOWN_AVAILABLE:
                    html_content = markdown.markdown(content, extensions=['tables', 'fenced_code'])
                else:
                    # Basic markdown-to-HTML conversion without external library
                    html_content = self._basic_markdown_to_html(content)
                return self._render_document_page(doc.title, html_content, 'markdown')
            elif doc.file_type == 'html':
                return Response(content, content_type='text/html')
            elif doc.file_type == 'sql':
                # Format SQL with syntax highlighting
                formatted_content = f"<pre><code class='language-sql'>{content}</code></pre>"
                return self._render_document_page(doc.title, formatted_content, 'sql')
            else:
                # Plain text with formatting
                formatted_content = f"<pre>{content}</pre>"
                return self._render_document_page(doc.title, formatted_content, 'text')

        except Exception as e:
            _logger.error(f"Error viewing document {doc_id}: {e}")
            return Response(f"Error: {e}", status=500)

    @http.route('/ai_automator/docs/open_file/<int:doc_id>', type='http', auth='user')
    def open_file_in_browser(self, doc_id):
        """Open file directly in browser"""
        try:
            doc = request.env['ai.automator.documentation'].browse(doc_id)
            if not doc.exists():
                return Response("Document not found", status=404)

            file_path = self._get_full_path(doc.file_path)
            if not file_path.exists():
                return Response("File not found", status=404)

            # Read the file content
            content = file_path.read_text(encoding='utf-8')

            # Determine content type and return appropriately
            if doc.file_type == 'markdown':
                # Convert markdown to HTML if available, otherwise show as formatted text
                if MARKDOWN_AVAILABLE:
                    html_content = markdown.markdown(content, extensions=['tables', 'fenced_code'])
                else:
                    # Basic markdown-to-HTML conversion without external library
                    html_content = self._basic_markdown_to_html(content)
                return self._render_document_page(doc.title, html_content, 'markdown')
            elif doc.file_type == 'html':
                return Response(content, content_type='text/html')
            elif doc.file_type == 'sql':
                # Format SQL with syntax highlighting
                formatted_content = f"<pre><code class='language-sql'>{content}</code></pre>"
                return self._render_document_page(doc.title, formatted_content, 'sql')
            else:
                # Plain text with formatting
                formatted_content = f"<pre>{content}</pre>"
                return self._render_document_page(doc.title, formatted_content, 'text')

        except Exception as e:
            _logger.error(f"Error opening file {doc_id}: {e}")
            return Response(f"Error: {e}", status=500)

    @http.route('/ai_automator/docs/download/<int:doc_id>', type='http', auth='user')
    def download_document(self, doc_id):
        """Download document file"""
        try:
            doc = request.env['ai.automator.documentation'].browse(doc_id)
            if not doc.exists():
                return Response("Document not found", status=404)

            file_path = self._get_full_path(doc.file_path)
            if not file_path.exists():
                return Response("File not found", status=404)

            content = file_path.read_bytes()
            filename = file_path.name

            # Determine content type
            content_type, _ = mimetypes.guess_type(filename)
            if not content_type:
                content_type = 'application/octet-stream'

            return Response(
                content,
                content_type=content_type,
                headers=[
                    ('Content-Disposition', f'attachment; filename="{filename}"'),
                    ('Content-Length', str(len(content)))
                ]
            )

        except Exception as e:
            _logger.error(f"Error downloading document {doc_id}: {e}")
            return Response(f"Error: {e}", status=500)

    def _get_full_path(self, relative_path):
        """Get full path to documentation file"""
        from odoo.modules.module import get_module_path
        module_path = Path(get_module_path('the_ai_automator'))
        return module_path / 'docs' / relative_path

    def _basic_markdown_to_html(self, content):
        """Basic markdown to HTML conversion without external library"""
        import re

        # Convert basic markdown elements
        html = content

        # Headers
        html = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
        html = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
        html = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)

        # Bold and italic
        html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
        html = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html)

        # Code blocks
        html = re.sub(r'```(.+?)```', r'<pre><code>\1</code></pre>', html, flags=re.DOTALL)
        html = re.sub(r'`(.+?)`', r'<code>\1</code>', html)

        # Line breaks
        html = html.replace('\n\n', '</p><p>')
        html = f'<p>{html}</p>'

        return html

    def _render_document_page(self, title, content, doc_type):
        """Render document in styled HTML page"""
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>{title} - AI Automator Documentation</title>
            <meta charset="utf-8">
            <style>
                body {{
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                    max-width: 1200px;
                    margin: 0 auto;
                    padding: 20px;
                    line-height: 1.6;
                    background: #f8f9fa;
                }}
                .document-header {{
                    background: white;
                    padding: 20px;
                    border-radius: 8px;
                    margin-bottom: 20px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }}
                .document-content {{
                    background: white;
                    padding: 30px;
                    border-radius: 8px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                    overflow-x: auto;
                }}
                .document-type {{
                    background: #007acc;
                    color: white;
                    padding: 4px 12px;
                    border-radius: 4px;
                    font-size: 12px;
                    text-transform: uppercase;
                }}
                h1 {{ color: #333; margin-top: 0; }}
                h2 {{ color: #444; border-bottom: 2px solid #eee; padding-bottom: 8px; }}
                h3 {{ color: #555; }}
                code {{
                    background: #f4f4f4;
                    padding: 2px 6px;
                    border-radius: 4px;
                    font-family: 'Monaco', 'Consolas', monospace;
                }}
                pre {{
                    background: #f8f8f8;
                    padding: 15px;
                    border-radius: 6px;
                    overflow-x: auto;
                    border-left: 4px solid #007acc;
                }}
                table {{
                    border-collapse: collapse;
                    width: 100%;
                    margin: 15px 0;
                }}
                th, td {{
                    border: 1px solid #ddd;
                    padding: 8px 12px;
                    text-align: left;
                }}
                th {{
                    background: #f8f9fa;
                    font-weight: 600;
                }}
                .back-link {{
                    display: inline-block;
                    margin-top: 20px;
                    color: #007acc;
                    text-decoration: none;
                    padding: 8px 16px;
                    border: 1px solid #007acc;
                    border-radius: 4px;
                }}
                .back-link:hover {{
                    background: #007acc;
                    color: white;
                }}
                .language-sql {{
                    color: #0066cc;
                }}
                /* Enhanced styling to match original spec */
                .document-type.architecture {{ background: #28a745; }}
                .document-type.database {{ background: #6f42c1; }}
                .document-type.guides {{ background: #fd7e14; }}
                .document-type.management {{ background: #20c997; }}
                .document-type.strategy {{ background: #e83e8c; }}
                .document-type.demos {{ background: #17a2b8; }}
                .document-type.reports {{ background: #ffc107; color: #212529; }}
                .document-type.workflows {{ background: #6c757d; }}

                /* File type indicators */
                .file-info {{
                    display: flex;
                    gap: 10px;
                    margin-bottom: 10px;
                }}
                .file-size {{
                    background: #f8f9fa;
                    padding: 4px 8px;
                    border-radius: 4px;
                    font-size: 12px;
                    color: #6c757d;
                }}
                /* Better code highlighting */
                pre code {{
                    background: #2d3748;
                    color: #e2e8f0;
                    border-radius: 6px;
                }}
            </style>
        </head>
        <body>
            <div class="document-header">
                <span class="document-type {doc_type}">{doc_type}</span>
                <h1>{title}</h1>
            </div>
            <div class="document-content">
                {content}
            </div>
            <a href="#" onclick="window.close()" class="back-link">← Close Document</a>
        </body>
        </html>
        """
        return Response(html, content_type='text/html')