# SAM AI Cache Manager Enhanced

**Technical Name**: `ai_sam_cache_manager`
**Version**: 18.0.2.8

Comprehensive cache/log clearing + Python process cleanup with real-time progress tracking

## Description


        SAM AI Cache Manager - Enhanced Edition
        ========================================

        A professional developer utility that provides comprehensive cache clearing
        across ALL 9 Odoo cache layers + Python process cleanup + log files with real-time progress tracking.

        **Features:**

        * **Complete Cache Clearing** - Clears ALL 9 cache layers + processes:
          1. Python bytecode (.pyc, __pycache__) - ALL addons paths
          2. Odoo registry caches (internal ORM cache)
          3. ORM method caches (@ormcache decorated methods)
          4. Database asset cache (ir_attachment)
          5. QWeb template cache (compiled views)
          6. Translation cache
          7. Filestore session cache
          8. **Manifest LRU cache** (_get_manifest_cached) - Critical for version updates!
          9. Odoo log files (odoo.log truncated to empty)

        * **Proper Service Restart Sequence** (v2.6 fix):
          1. STOP service first (graceful shutdown)
          2. KILL remaining Python workers (eliminates stale LRU caches)
          3. START service (fresh workers with no cached data)

        * **Real-Time Progress Modal** - Beautiful progress dialog showing:
          - Overall progress with percentage
          - Current stage being processed
          - Detailed breakdown by cache layer
          - Items cleared count for each layer

        * **Smart Discovery** - Automatically finds all cache locations using:
          - odoo.tools.config for all addons paths
          - Internal registry cache APIs
          - Database queries for assets

        * **Production Ready** - Enhanced with:
          - Comprehensive error handling
          - Detailed logging
          - Admin-only access control
          - Async background processing

        **Use Cases:**

        - Static assets (CSS/JS) not reflecting changes
        - Module upgrades not taking effect
        - Testing requires clean cache state
        - Debugging cache-related issues

        **WARNING**: This module will restart the Odoo server. All users will be disconnected briefly.

        Author: Anthony Gardiner - Odoo Consulting & Claude AI
        License: LGPL-3
        Version: 2.3 (Enhanced with cache clearing + Python process cleanup + Odoo log truncation)
    

## Dependencies

- `base`
- `web`
