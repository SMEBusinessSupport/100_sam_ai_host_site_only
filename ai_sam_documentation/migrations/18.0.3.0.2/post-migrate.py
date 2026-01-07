# -*- coding: utf-8 -*-
"""
Migration 18.0.3.0.2: Fix slide sequencing for correct section assignment.

The category_id field is COMPUTED based on sequence order, not manually set.
This migration re-runs build_courses with corrected sequence logic.
"""
import logging

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    """Run build_courses on module upgrade to fix sequencing."""
    _logger.info("=" * 60)
    _logger.info("Running SAM AI Documentation migration 18.0.3.0.2...")
    _logger.info("Fixing slide sequences for correct section assignment...")
    _logger.info("=" * 60)

    # Import here to avoid issues during migration
    from odoo import api, SUPERUSER_ID

    env = api.Environment(cr, SUPERUSER_ID, {})

    # Import and run build_courses
    try:
        from odoo.addons.ai_sam_documentation.scripts.build_courses import build_courses
        build_courses(env)
        _logger.info("=" * 60)
        _logger.info("SAM AI Documentation migration 18.0.3.0.2 complete!")
        _logger.info("=" * 60)
    except Exception as e:
        _logger.error(f"Migration failed: {e}")
        raise
