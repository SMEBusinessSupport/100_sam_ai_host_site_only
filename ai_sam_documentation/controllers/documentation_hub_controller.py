# -*- coding: utf-8 -*-
"""
Documentation Hub Controller - GitBook-style /documentation/ interface.

Reads directly from the docs/ folder structure to provide a standalone
documentation experience. No eLearning dependency for viewing.

Folder Structure Mapping:
    docs/
        00_vision/              -> Section (sidebar group)
            strategy/           -> Subsection
                roadmap.md      -> Article
        04_modules/             -> Section
            ai_sam/             -> Subsection
                overview.md     -> Article
"""

import logging
import re
from pathlib import Path

from markupsafe import Markup
from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)
_logger.info("=== DOCUMENTATION HUB CONTROLLER LOADED ===")

# Optional markdown - fallback to basic if not available
try:
    import markdown
    MARKDOWN_AVAILABLE = True
except ImportError:
    MARKDOWN_AVAILABLE = False


class DocumentationHubController(http.Controller):
    """
    Main controller for /documentation/ routes.

    Reads directly from docs/ folder - no database dependency.
    """

    # =========================================================================
    # Configuration
    # =========================================================================

    # Folders to exclude from navigation
    EXCLUDED_FOLDERS = {'_archive', '_assets', '_unsorted', '__pycache__', '.git'}

    # Files to exclude
    EXCLUDED_FILES = {'_README.md', '_course_config.md', '_course_config.json', '_url_registry.json'}

    # =========================================================================
    # Path Utilities
    # =========================================================================

    def _get_docs_path(self):
        """Get the docs/ folder path with proper case preserved."""
        from odoo.modules.module import get_module_path
        module_path = get_module_path('ai_sam_documentation')
        docs_path = Path(module_path) / 'docs'
        # Resolve to get actual filesystem path with correct case
        try:
            return docs_path.resolve(strict=True)
        except (OSError, FileNotFoundError):
            return docs_path

    def _slugify(self, text):
        """Convert text to URL-safe slug."""
        # Remove number prefix (00_, 01_, etc.)
        text = re.sub(r'^\d{2}_', '', text)
        text = text.lower().strip()
        text = re.sub(r'[^\w\s-]', '', text)
        text = re.sub(r'[-\s]+', '-', text)
        return text

    def _display_name(self, folder_name):
        """Convert folder name to display name."""
        # Remove number prefix
        name = re.sub(r'^\d{2}_', '', folder_name)
        # Convert to title case
        return name.replace('_', ' ').replace('-', ' ').title()

    def _is_valid_section(self, path):
        """Check if path is a valid documentation section."""
        if not path.is_dir():
            return False
        if path.name.startswith('.'):
            return False
        if path.name in self.EXCLUDED_FOLDERS:
            return False
        return True

    def _is_valid_file(self, path):
        """Check if path is a valid documentation file."""
        if not path.is_file():
            return False
        if path.name.startswith('_'):
            return False
        if path.name in self.EXCLUDED_FILES:
            return False
        if path.suffix.lower() not in {'.md', '.html', '.txt'}:
            return False
        return True

    # =========================================================================
    # Content Processing
    # =========================================================================

    def _convert_md_to_html(self, content):
        """Convert markdown content to HTML."""
        if MARKDOWN_AVAILABLE:
            return markdown.markdown(
                content,
                extensions=['tables', 'fenced_code', 'toc', 'nl2br', 'codehilite']
            )
        else:
            # Basic conversion fallback
            html = content
            html = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
            html = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
            html = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
            html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
            html = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html)
            html = re.sub(r'```(\w*)\n(.*?)```', r'<pre><code class="language-\1">\2</code></pre>', html, flags=re.DOTALL)
            html = re.sub(r'`(.+?)`', r'<code>\1</code>', html)
            # Convert line breaks to paragraphs
            paragraphs = html.split('\n\n')
            html = ''.join(f'<p>{p}</p>' for p in paragraphs if p.strip())
            return f'<div class="markdown-content">{html}</div>'

    def _extract_title(self, content, filename):
        """Extract title from markdown content or filename."""
        # Try to find # Title at start
        match = re.match(r'^#\s+(.+)$', content.strip(), re.MULTILINE)
        if match:
            return match.group(1).strip()
        # Fall back to filename
        return filename.replace('.md', '').replace('.html', '').replace('_', ' ').replace('-', ' ').title()

    def _read_file_content(self, file_path):
        """Read and process a documentation file."""
        try:
            content = file_path.read_text(encoding='utf-8')
            title = self._extract_title(content, file_path.name)

            if file_path.suffix.lower() == '.md':
                html_content = self._convert_md_to_html(content)
            elif file_path.suffix.lower() == '.html':
                html_content = content
            else:
                html_content = f'<pre>{content}</pre>'

            return {
                'title': title,
                'content': Markup(html_content),  # Mark as safe HTML for QWeb t-out
                'raw': content,
                'path': file_path,
                'modified': file_path.stat().st_mtime,
            }
        except Exception as e:
            _logger.error(f"Error reading {file_path}: {e}")
            return None

    # =========================================================================
    # Sidebar Structure Building
    # =========================================================================

    def _build_sidebar_structure(self):
        """
        Build hierarchical sidebar navigation from docs/ folder.

        Returns list of sections:
        [
            {
                'name': 'Vision',
                'slug': 'vision',
                'path': Path(...),
                'subsections': [
                    {
                        'name': 'Strategy',
                        'slug': 'strategy',
                        'path': Path(...),
                        'articles': [
                            {'name': 'Roadmap', 'slug': 'roadmap', 'path': Path(...)}
                        ]
                    }
                ],
                'articles': []  # Direct articles in section
            }
        ]
        """
        docs_path = self._get_docs_path()
        if not docs_path.exists():
            return []

        structure = []

        # Get top-level sections (00_vision, 01_platform_inspirations, etc.)
        sections = sorted([
            d for d in docs_path.iterdir()
            if self._is_valid_section(d) and re.match(r'^\d{2}_', d.name)
        ])

        for section_path in sections:
            section_data = {
                'name': self._display_name(section_path.name),
                'slug': self._slugify(section_path.name),
                'folder': section_path.name,
                'path': section_path,
                'subsections': [],
                'articles': [],
            }

            # Get subsections and articles
            for item in sorted(section_path.iterdir()):
                if self._is_valid_section(item):
                    # It's a subsection folder
                    subsection_data = {
                        'name': self._display_name(item.name),
                        'slug': self._slugify(item.name),
                        'folder': item.name,
                        'path': item,
                        'articles': [],
                    }

                    # Get articles in subsection
                    for file in sorted(item.iterdir()):
                        if self._is_valid_file(file):
                            subsection_data['articles'].append({
                                'name': self._display_name(file.stem),
                                'slug': self._slugify(file.stem),
                                'filename': file.name,
                                'path': file,
                            })

                    if subsection_data['articles']:  # Only add if has content
                        section_data['subsections'].append(subsection_data)

                elif self._is_valid_file(item):
                    # It's a direct article in the section
                    section_data['articles'].append({
                        'name': self._display_name(item.stem),
                        'slug': self._slugify(item.stem),
                        'filename': item.name,
                        'path': item,
                    })

            # Only add sections that have content
            if section_data['subsections'] or section_data['articles']:
                structure.append(section_data)

        return structure

    def _find_article(self, structure, section_slug, subsection_slug=None, article_slug=None):
        """Find an article in the structure by slugs."""
        for section in structure:
            if section['slug'] == section_slug:
                if article_slug and not subsection_slug:
                    # Direct article in section
                    for article in section['articles']:
                        if article['slug'] == article_slug:
                            return section, None, article
                elif subsection_slug:
                    for subsection in section['subsections']:
                        if subsection['slug'] == subsection_slug:
                            if article_slug:
                                for article in subsection['articles']:
                                    if article['slug'] == article_slug:
                                        return section, subsection, article
                            else:
                                # Return first article in subsection
                                if subsection['articles']:
                                    return section, subsection, subsection['articles'][0]
                return section, None, None
        return None, None, None

    # =========================================================================
    # Search
    # =========================================================================

    def _search_documentation(self, query, limit=20):
        """Search across documentation content."""
        if not query or len(query) < 2:
            return []

        docs_path = self._get_docs_path()
        results = []
        query_lower = query.lower()

        def search_folder(folder_path, section_name=''):
            for item in folder_path.iterdir():
                if self._is_valid_section(item):
                    search_folder(item, section_name or self._display_name(item.name))
                elif self._is_valid_file(item):
                    try:
                        content = item.read_text(encoding='utf-8')
                        title = self._extract_title(content, item.name)

                        # Search in title and content
                        if query_lower in title.lower() or query_lower in content.lower():
                            # Extract snippet
                            snippet = self._extract_snippet(content, query)

                            # Build URL path
                            rel_path = item.relative_to(docs_path)
                            parts = list(rel_path.parts)

                            results.append({
                                'title': title,
                                'snippet': snippet,
                                'section': section_name,
                                'path': item,
                                'url_parts': parts,
                            })

                            if len(results) >= limit:
                                return
                    except Exception as e:
                        _logger.debug(f"Error searching {item}: {e}")

        search_folder(docs_path)
        return results[:limit]

    def _extract_snippet(self, text, query, context_chars=100):
        """Extract text snippet around query match."""
        if not text:
            return ''

        # Remove markdown formatting for snippet
        text = re.sub(r'[#*`\[\]]', '', text)

        lower_text = text.lower()
        lower_query = query.lower()
        pos = lower_text.find(lower_query)

        if pos == -1:
            return text[:context_chars * 2] + '...' if len(text) > context_chars * 2 else text

        start = max(0, pos - context_chars)
        end = min(len(text), pos + len(query) + context_chars)
        snippet = text[start:end]

        if start > 0:
            snippet = '...' + snippet
        if end < len(text):
            snippet = snippet + '...'

        return snippet

    # =========================================================================
    # Context Helpers
    # =========================================================================

    def _is_dev_mode(self):
        """Check if SAM AI dev mode is enabled."""
        ICP = request.env['ir.config_parameter'].sudo()
        return ICP.get_param('sam.dev_mode', 'False').lower() == 'true'

    def _get_base_context(self):
        """Base context for all documentation pages."""
        return {
            'user': request.env.user,
            'is_public_user': request.website.is_public_user(),
            'is_dev_mode': self._is_dev_mode(),
        }

    # =========================================================================
    # Routes - Dev Share (for Claude sessions)
    # =========================================================================

    @http.route('/documentation/dev/share', type='json', auth='user', website=True)
    def documentation_dev_share(self, path='', **kwargs):
        """
        Dev Share API - Returns file system path for sharing with Claude.
        Only available in dev mode.

        Usage: Click "Share with Claude" button on any doc page.
        Returns the actual file/folder path that Claude can access directly.
        """
        if not self._is_dev_mode():
            return {'error': 'Dev mode not enabled'}

        docs_path = self._get_docs_path()

        # Parse path: /documentation/section/subsection/article
        parts = [p for p in path.strip('/').split('/') if p and p != 'documentation']

        if not parts:
            # Share the docs folder path
            return {
                'success': True,
                'type': 'folder',
                'title': 'Documentation Root',
                'file_path': str(docs_path),
            }

        # Find the specific article or folder
        structure = self._build_sidebar_structure()

        if len(parts) == 1:
            # Section folder
            section, _, _ = self._find_article(structure, parts[0])
            if section and section.get('path'):
                return {
                    'success': True,
                    'type': 'folder',
                    'title': section['name'],
                    'file_path': str(section['path']),
                }

        elif len(parts) == 2:
            # Could be subsection folder or direct article
            section, subsection, article = self._find_article(structure, parts[0], parts[1])
            if subsection and subsection.get('path'):
                return {
                    'success': True,
                    'type': 'folder',
                    'title': f"{section['name']} > {subsection['name']}",
                    'file_path': str(subsection['path']),
                }
            # Try as direct article
            section, _, article = self._find_article(structure, parts[0], article_slug=parts[1])
            if article and article.get('path'):
                return {
                    'success': True,
                    'type': 'file',
                    'title': article['name'],
                    'file_path': str(article['path']),
                }

        elif len(parts) >= 3:
            # Full article path
            section, subsection, article = self._find_article(structure, parts[0], parts[1], parts[2])
            if article and article.get('path'):
                return {
                    'success': True,
                    'type': 'file',
                    'title': article['name'],
                    'file_path': str(article['path']),
                }

        return {'error': 'Content not found', 'path': path}

    def _format_structure_for_share(self, structure):
        """Format full documentation structure for sharing."""
        lines = ['# SAM AI Documentation Structure\n']
        for section in structure:
            lines.append(f"## {section['name']}")
            for article in section.get('articles', []):
                lines.append(f"  - {article['name']}")
            for subsection in section.get('subsections', []):
                lines.append(f"  ### {subsection['name']}")
                for article in subsection.get('articles', []):
                    lines.append(f"    - {article['name']}")
            lines.append('')
        return '\n'.join(lines)

    def _format_section_for_share(self, section):
        """Format section overview for sharing."""
        lines = [f"# {section['name']}\n"]
        lines.append('## Contents\n')
        for article in section.get('articles', []):
            lines.append(f"- {article['name']}")
        for subsection in section.get('subsections', []):
            lines.append(f"\n### {subsection['name']}")
            for article in subsection.get('articles', []):
                lines.append(f"- {article['name']}")
        return '\n'.join(lines)

    def _format_subsection_for_share(self, section, subsection):
        """Format subsection overview for sharing."""
        lines = [f"# {section['name']} > {subsection['name']}\n"]
        lines.append('## Articles\n')
        for article in subsection.get('articles', []):
            lines.append(f"- {article['name']}")
        return '\n'.join(lines)

    # =========================================================================
    # Routes - Search (defined first to avoid slug collision)
    # =========================================================================

    @http.route(['/documentation/search', '/documentation/search/'], type='http', auth='public', website=True, methods=['GET'])
    def documentation_search(self, q='', **kwargs):
        """Documentation search results page."""
        _logger.info(f"=== DOCUMENTATION SEARCH ROUTE HIT: q={q} ===")
        structure = self._build_sidebar_structure()
        results = self._search_documentation(q) if q else []

        values = self._get_base_context()
        values.update({
            'page_title': f'Search: {q}' if q else 'Search',
            'sidebar_structure': structure,
            'current_section': None,
            'current_subsection': None,
            'current_article': None,
            'search_query': q,
            'search_results': results,
            'result_count': len(results),
        })

        return request.render('ai_sam_documentation.documentation_hub_search', values)

    @http.route('/documentation/api/search', type='json', auth='public', website=True)
    def documentation_api_search(self, query='', **kwargs):
        """JSON API for live search."""
        results = self._search_documentation(query, limit=10)

        return [{
            'title': r['title'],
            'snippet': r['snippet'],
            'section': r['section'],
            'url': '/documentation/' + '/'.join(self._slugify(p) for p in r['url_parts'][:-1]) + '/' + self._slugify(r['url_parts'][-1].replace('.md', '').replace('.html', '')),
        } for r in results]

    # =========================================================================
    # Routes - Main Pages
    # =========================================================================

    @http.route(['/documentation', '/documentation/'], type='http', auth='public', website=True, methods=['GET'])
    def documentation_index(self, **kwargs):
        """Documentation hub landing page."""
        _logger.info("=== DOCUMENTATION INDEX ROUTE HIT ===")
        structure = self._build_sidebar_structure()
        _logger.info(f"=== DOCUMENTATION: Found {len(structure)} sections ===")


        values = self._get_base_context()
        values.update({
            'page_title': 'Documentation',
            'sidebar_structure': structure,
            'current_section': None,
            'current_subsection': None,
            'current_article': None,
            'search_query': '',
        })

        return request.render('ai_sam_documentation.documentation_hub_index', values)

    @http.route(['/documentation/<string:section>', '/documentation/<string:section>/'], type='http', auth='public', website=True, methods=['GET'])
    def documentation_section(self, section, **kwargs):
        """Documentation section overview."""
        structure = self._build_sidebar_structure()
        current_section, _, _ = self._find_article(structure, section)

        if not current_section:
            return request.redirect('/documentation')

        values = self._get_base_context()
        values.update({
            'page_title': current_section['name'],
            'sidebar_structure': structure,
            'current_section': current_section,
            'current_subsection': None,
            'current_article': None,
            'search_query': '',
        })

        return request.render('ai_sam_documentation.documentation_hub_section', values)

    @http.route(['/documentation/<string:section>/<string:subsection>', '/documentation/<string:section>/<string:subsection>/'], type='http', auth='public', website=True, methods=['GET'])
    def documentation_subsection(self, section, subsection, **kwargs):
        """Documentation subsection - shows first article or list."""
        structure = self._build_sidebar_structure()
        current_section, current_subsection, first_article = self._find_article(
            structure, section, subsection
        )

        if not current_section:
            return request.redirect('/documentation')

        if not current_subsection:
            # Maybe it's a direct article in the section
            current_section, _, current_article = self._find_article(
                structure, section, article_slug=subsection
            )
            if current_article:
                # Read the article content
                content_data = self._read_file_content(current_article['path'])
                if content_data:
                    values = self._get_base_context()
                    values.update({
                        'page_title': content_data['title'],
                        'sidebar_structure': structure,
                        'current_section': current_section,
                        'current_subsection': None,
                        'current_article': current_article,
                        'article_content': content_data,
                        'search_query': '',
                    })
                    return request.render('ai_sam_documentation.documentation_hub_article', values)

            return request.redirect(f'/documentation/{section}')

        # Show subsection overview or first article
        if first_article:
            content_data = self._read_file_content(first_article['path'])
        else:
            content_data = None

        values = self._get_base_context()
        values.update({
            'page_title': current_subsection['name'],
            'sidebar_structure': structure,
            'current_section': current_section,
            'current_subsection': current_subsection,
            'current_article': first_article,
            'article_content': content_data,
            'search_query': '',
        })

        return request.render('ai_sam_documentation.documentation_hub_article', values)

    @http.route(['/documentation/<string:section>/<string:subsection>/<string:article>', '/documentation/<string:section>/<string:subsection>/<string:article>/'], type='http', auth='public', website=True, methods=['GET'])
    def documentation_article(self, section, subsection, article, **kwargs):
        """Individual documentation article page."""
        structure = self._build_sidebar_structure()
        current_section, current_subsection, current_article = self._find_article(
            structure, section, subsection, article
        )

        if not current_article:
            return request.redirect(f'/documentation/{section}/{subsection}')

        # Read the article content
        content_data = self._read_file_content(current_article['path'])
        if not content_data:
            return request.redirect(f'/documentation/{section}/{subsection}')

        # Find prev/next articles for navigation
        prev_article = None
        next_article = None

        if current_subsection:
            articles = current_subsection['articles']
            for i, art in enumerate(articles):
                if art['slug'] == article:
                    if i > 0:
                        prev_article = articles[i - 1]
                    if i < len(articles) - 1:
                        next_article = articles[i + 1]
                    break

        values = self._get_base_context()
        values.update({
            'page_title': content_data['title'],
            'sidebar_structure': structure,
            'current_section': current_section,
            'current_subsection': current_subsection,
            'current_article': current_article,
            'article_content': content_data,
            'prev_article': prev_article,
            'next_article': next_article,
            'search_query': '',
        })

        return request.render('ai_sam_documentation.documentation_hub_article', values)
