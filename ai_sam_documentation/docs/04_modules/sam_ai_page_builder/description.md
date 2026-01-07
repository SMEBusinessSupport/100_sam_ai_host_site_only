# SAM AI Page Builder

**Technical Name**: `sam_ai_page_builder`
**Version**: 18.0.1.0.0

AI-Powered Internal Page Builder for Odoo 18

## Description


        SAM AI Page Builder
        ===================

        An AI-powered page builder system embedded in the Odoo backend.
        Uses Claude AI to generate and refine web pages through natural conversation.

        Features:
        ---------
        * Modern editor-style interface with split-pane layout
        * AI chat panel for natural language page generation
        * Live preview panel for generated content
        * Real Claude AI integration via ai_sam_base
        * Store HTML, CSS, and JS separately
        * Track AI prompt history
        * State management (draft, generated, published)
        * Publish to Odoo website (self-contained)

        Integration (2025-12-24):
        * page_builder_tools.py - AI tools for page generation/refinement
        * sam_ai_page_controller.py - HTTP endpoints for frontend
        * ai_page_service.js - Real AI service (replaces stub)
        * website_publisher.py - Publish pages to Odoo website
    

## Dependencies

- `base`
- `web`
- `website`
- `sam_ui_theme`
- `ai_sam`
- `ai_sam_base`
