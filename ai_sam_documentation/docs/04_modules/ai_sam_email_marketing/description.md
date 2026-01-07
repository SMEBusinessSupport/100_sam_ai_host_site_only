# SAM AI Email Marketing

**Technical Name**: `ai_sam_email_marketing`
**Version**: 18.0.1.0.0

AI-Powered Email Campaign Creation and Management

## Description


        SAM AI Email Marketing
        ======================
        
        AI-powered email marketing module that extends Odoo's native email marketing
        capabilities with intelligent content generation.
        
        Key Features:
        -------------
        * AI-powered email template generation
        * Chat-based interface for iterative email creation
        * File upload support (JSON/HTML/Markdown → Email template)
        * Natural language prompt understanding
        * Auto-generation of subject lines, preheaders, and body content
        * Direct integration with Odoo Email Marketing (mass_mailing)
        * Template history and versioning
        * Campaign context awareness (audience, tone, goals)
        
        Architecture:
        -------------
        * LLM-agnostic AI service layer (plug-and-play)
        * Stub AI service included for development/testing
        * Split-pane UI: Chat (left) + Preview (right)
        * Full integration with Odoo's native email editor
        * Extensible for future analytics and A/B testing
        
        Dependencies:
        -------------
        * mail: Core email functionality
        * mass_mailing: Email marketing campaigns
        * ai_sam: Custom AI core module (SAM AI framework)
    

## Dependencies

- `base`
- `mail`
- `mass_mailing`
- `ai_sam`
