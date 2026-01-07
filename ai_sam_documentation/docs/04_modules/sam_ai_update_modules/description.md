# SAM AI Update Modules

**Technical Name**: `sam_ai_update_modules`
**Version**: 18.0.1.8

Sequential module upgrade queue - One-click SAM ecosystem updates

## Description


SAM AI Update Modules
=====================

A standalone module for batch Odoo module upgrades.

Features:
---------
* Configure up to 20 modules in upgrade queue
* One-click "Activate Upgrade" to start batch upgrades
* Direct upgrade: all modules upgraded in single server restart
* Full-screen gold star progress overlay
* Survives server restarts (queue state persisted)
* Progress tracking with status indicators
* Error handling with detailed messages
* Smooth refresh UX with early-load dark background

How It Works:
-------------
1. Configure modules via Apps > SAM Apps Upgrade > Configure Apps to Upgrade
2. Click "Activate Upgrade" to start
3. All modules are marked for upgrade and server restarts once
4. After restart, overlay shows completion status
5. Click to continue to Odoo

Technical:
----------
* Depends on sam_ui_theme for consistent overlay styling
* Single-phase upgrade (direct from user action)
* localStorage persists overlay state across restarts
* Early-load script prevents white flash on refresh
* Admin-only access by default
    

## Dependencies

- `base`
- `web`
- `sam_ui_theme`
