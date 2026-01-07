# -*- coding: utf-8 -*-
import logging

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    """Run build_courses on module upgrade."""
    _logger.info("Running SAM AI Documentation migration...")

    # Import here to avoid issues during migration
    from odoo import api, SUPERUSER_ID

    env = api.Environment(cr, SUPERUSER_ID, {})

    # Import and run build_courses
    try:
        from odoo.addons.ai_sam_documentation.scripts.build_courses import build_courses
        build_courses(env)
        _logger.info("SAM AI Documentation migration complete!")
    except Exception as e:
        _logger.error(f"Migration failed: {e}")
        raise
