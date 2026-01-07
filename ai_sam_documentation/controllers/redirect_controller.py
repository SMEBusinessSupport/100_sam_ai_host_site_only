# -*- coding: utf-8 -*-
"""
Redirect controller for stable /sam_insights/ URLs.

Maps stable slugs to actual eLearning URLs.
Allows content to be reorganized without breaking shared links.
"""

import json
import logging
from pathlib import Path

from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class SamInsightsRedirect(http.Controller):

    def _load_registry(self):
        """Load URL registry from JSON file."""
        from odoo.modules.module import get_module_path
        module_path = Path(get_module_path('ai_sam_documentation'))
        registry_path = module_path / 'docs' / '_url_registry.json'

        if registry_path.exists():
            with open(registry_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {'redirects': {}}

    @http.route('/sam_insights', type='http', auth='public', website=True)
    def insights_index(self, **kwargs):
        """Index page - redirect to eLearning courses list."""
        return request.redirect('/slides')

    @http.route('/sam_insights/<string:slug>', type='http', auth='public', website=True)
    def insight_redirect(self, slug, **kwargs):
        """Redirect stable slug to actual eLearning URL."""
        registry = self._load_registry()
        redirects = registry.get('redirects', {})

        if slug in redirects:
            entry = redirects[slug]
            target_channel = entry.get('target_channel', '')
            target_slide = entry.get('target_slide', '')

            # Build eLearning URL
            if target_slide:
                target_url = f'/slides/slide/{target_slide}'
            elif target_channel:
                target_url = f'/slides/{target_channel}'
            else:
                target_url = '/slides'

            _logger.debug(f"Redirecting /sam_insights/{slug} -> {target_url}")
            return request.redirect(target_url)

        # Slug not found - try to find by searching slides
        Slide = request.env['slide.slide'].sudo()
        slide = Slide.search([
            ('name', 'ilike', slug.replace('-', ' ')),
            ('is_category', '=', False)
        ], limit=1)

        if slide:
            return request.redirect(f'/slides/slide/{slide.id}')

        # Not found
        _logger.warning(f"SAM Insights slug not found: {slug}")
        return request.redirect('/slides')

    @http.route('/sam_insights/course/<string:course_slug>', type='http', auth='public', website=True)
    def course_redirect(self, course_slug, **kwargs):
        """Redirect to a course/channel."""
        Channel = request.env['slide.channel'].sudo()

        # Try to find channel by slug pattern
        search_name = course_slug.replace('-', ' ').replace('_', ' ')
        channel = Channel.search([
            ('name', 'ilike', f'%{search_name}%')
        ], limit=1)

        if channel:
            return request.redirect(f'/slides/{channel.id}')

        return request.redirect('/slides')

    # =========================================================================
    # Filtered Routes by Audience
    # =========================================================================
    # Note: These redirect to /slides with tag filter instead of rendering
    # templates directly (eLearning templates require complex context).

    @http.route('/sam_insights/', type='http', auth='user', website=True)
    def sam_insights_index(self, **kwargs):
        """Internal documentation - requires login, redirects to Internal tagged courses."""
        Tag = request.env['slide.channel.tag'].sudo()
        internal_tag = Tag.search([('name', '=', 'Internal')], limit=1)

        if internal_tag:
            return request.redirect(f'/slides/all?tag={internal_tag.id}')
        return request.redirect('/slides')

    @http.route('/learn/', type='http', auth='public', website=True)
    def learn_index(self, **kwargs):
        """Free courses - public access, redirects to Free tagged courses."""
        Tag = request.env['slide.channel.tag'].sudo()
        free_tag = Tag.search([('name', '=', 'Free')], limit=1)

        if free_tag:
            return request.redirect(f'/slides/all?tag={free_tag.id}')
        return request.redirect('/slides')

    @http.route('/training/', type='http', auth='user', website=True)
    def training_index(self, **kwargs):
        """Premium courses - requires login, redirects to Premium tagged courses."""
        Tag = request.env['slide.channel.tag'].sudo()
        premium_tag = Tag.search([('name', '=', 'Premium')], limit=1)

        if premium_tag:
            return request.redirect(f'/slides/all?tag={premium_tag.id}')
        return request.redirect('/slides')
