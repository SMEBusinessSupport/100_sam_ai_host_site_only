# SAM AI System Overlay

**Technical Name**: `ai_sam_system_overlay`
**Version**: 18.0.1.6.0

System-wide loading overlay for module upgrades and asset reloads

## Description


        Provides a clean loading experience during system operations:

        Bootstrap Splash Screen:
        - Displays IMMEDIATELY when HTML loads (before JS/CSS bundles)
        - Eliminates the "white screen" during initial load
        - Shows animated progress with rotating status messages
        - Auto-hides when Odoo WebClient is ready

        System Overlay:
        - Shows during module upgrades
        - Shows during asset bundle recompilation
        - Broadcasts via bus service for real-time updates

        BlockUI Integration (v1.4.0):
        - Patches Odoo's native BlockUI component
        - All ui.block() / ui.unblock() calls show SAM overlay
        - Consistent branding across reports, navigation, RPC
        - Message rotation for long-running operations
    

## Dependencies

- `base`
- `web`
- `bus`
- `sam_ui_theme`
