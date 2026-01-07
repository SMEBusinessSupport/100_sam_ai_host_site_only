# -*- coding: utf-8 -*-
# This module only provides data configuration - no models
# Installing = DEV MODE ON, Uninstalling = DEV MODE OFF


def post_init_hook(env):
    """
    Called after module installation.
    Enables SAM AI Dev Mode and scans local repositories.
    """
    import logging
    _logger = logging.getLogger(__name__)

    _logger.info("[SAM DEV MODE] ============================================")
    _logger.info("[SAM DEV MODE] Development Mode ENABLED")
    _logger.info("[SAM DEV MODE] ============================================")

    # Scan local repositories for module catalog
    _logger.info("[SAM DEV MODE] Scanning local repositories...")
    try:
        RepoModel = env['module.catalog.repository'].sudo()
        local_repos = RepoModel.search([
            ('repository_type', '=', 'local_filesystem'),
            ('active', '=', True)
        ])

        for repo in local_repos:
            try:
                _logger.info(f"[SAM DEV MODE] Scanning: {repo.name}")
                repo.action_scan_repository()
            except Exception as e:
                _logger.warning(f"[SAM DEV MODE] Failed to scan {repo.name}: {e}")
    except Exception as e:
        _logger.warning(f"[SAM DEV MODE] Module catalog not available: {e}")

    _logger.info("[SAM DEV MODE] Post-init complete - Dev features active")


def uninstall_hook(env):
    """
    Called when module is uninstalled.
    Resets SAM to production mode by clearing dev parameters.
    """
    import logging
    _logger = logging.getLogger(__name__)

    _logger.info("[SAM DEV MODE] ============================================")
    _logger.info("[SAM DEV MODE] Development Mode DISABLED")
    _logger.info("[SAM DEV MODE] ============================================")

    # Reset SAM chat dev parameters to production defaults
    ICP = env['ir.config_parameter'].sudo()

    # Set production defaults (opposite of dev mode)
    production_params = {
        'sam.dev_mode': 'False',
        'sam.always_inject_prompt': 'False',  # Production: only inject on first message
        'sam.debug_logging': 'False',
        'sam.write_debug_files': 'False',
    }

    for key, value in production_params.items():
        ICP.set_param(key, value)
        _logger.info(f"[SAM DEV MODE] Reset {key} = {value}")

    _logger.info("[SAM DEV MODE] Production mode restored")
