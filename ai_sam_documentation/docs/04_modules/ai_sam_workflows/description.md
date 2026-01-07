# SAM AI Workflows UI

**Technical Name**: `ai_sam_workflows`
**Version**: 18.0.2.38.1

N8N Workflow Platform Skin - UI Layer Only (Data in ai_sam_workflows_base)

## Description


SAM AI Workflows Platform Skin
==============================

🤖 N8N Workflow Automation UI Layer for SAM AI

Platform Skin Architecture (Updated 2025-10-30):
------------------------------------------------

This module is a PLATFORM SKIN providing UI-only components:
* N8N-style workflow canvas renderer
* Workflow management views (forms, kanban, tree)
* Platform-specific controllers (import/export N8N JSON)
* SAM Theater - Theatrical workflow assembly experience

NOTE: Workflow templates extracted to ai_sam_workflows_templates module (2024-12-19)

VENDOR LIBRARY (2025-10-30 Migration):
--------------------------------------
* Vendor icons/configs moved to ai_sam core (vendor_library/)
* 301 SVG icons organized by supplier (Google, Microsoft, etc.)
* 99.6% size reduction from original N8N library (150MB → 0.7MB)
* Single source of truth for vendor knowledge (APIs + visuals)

DATA SAFETY:
------------
* ALL workflow data models live in ai_sam_workflows_base (not here)
* Uninstalling this module does NOT delete workflow data
* Reinstalling restores UI access to existing workflows
* Audit trails and execution history remain protected

Features:
---------
* 1,500+ service connectors (N8N node library)
* Visual workflow canvas with drag-and-drop
* Professional N8N-style node rendering
* Bezier connection system
* N8N JSON import/export
* Dynamic menu system for node discovery

Architecture:
-------------
* ai_sam_workflows_base = Data layer (workflow models, executions, credentials)
* ai_sam_base = Foundation layer (core AI models, configuration)
* ai_sam = Core layer (canvas framework, vendor library, common components)
* ai_sam_workflows = Skin layer (views, JS/CSS, platform controllers)

Extraction History:
-------------------
* Phase 3 Extraction: 2025-10-11 (models incorrectly moved to this module)
* Phase 3 Correction: 2025-10-12 (models returned to ai_sam_workflows_base - Platform Skin Model)
* Phase 4 Migration: 2025-11-27 (ai_brain split into ai_sam_base + ai_sam_workflows_base)
* Now correctly implements Platform Skin Architecture
    

## Module Details

# SAM AI Workflows Platform 

N8N-Style Workflow Automation for Odoo 18 Version 18.0.2.35.0 Platform Skin Architecture UI-Only Module 
## Overview 

**SAM AI Workflows Platform **brings N8N-style visual workflow automation to Odoo 18.
 Build, visualize, and manage complex automation workflows with a professional drag-and-drop canvas
 featuring 1,500+ service connectors and theatrical assembly animations. **Platform Skin Architecture: **This is a **UI-only module **. All Python models,
 business logic, and data persistence are in `ai_sam_workflows_base `. This separation means
 uninstalling the UI preserves all your workflow data - reinstall anytime to restore access. +------------------+ +------------------+ +------------------+
 | Manual | | HTTP | | Slack |
 | Trigger |---->| Request |---->| Send Message |
 | | | | | |
 +------------------+ +------------------+ +------------------+
 ^ |
 | v
 +------------------+ +------------------+
 | Schedule | | If Condition |
 | Trigger | | (Router) |
 +------------------+ +------------------+
 |
 +---------------+---------------+
 | |
 v v
 +------------------+ +------------------+
 | Google | | Email |
 | Sheets | | Send |
 +------------------+ +------------------+ 
## Module Statistics 12,296 Total Files 306 Vendor Node Types 1,500+ Service Connectors 442 Node Type Registry 20 XML View Files 19 JavaScript Files 5 Python Controllers 3 REST API Endpoints 
## Key Features Visual Workflow Canvas 
- Infinite canvas with pan/zoom (0.1x - 3.0x) 
- Professional N8N-style node rendering 
- Bezier curve connections 
- Drag-and-drop interface 
- Real-time auto-save 
- Undo/redo support 
- Keyboard shortcuts N8N Node Library 
- 306 vendor node types 
- 1,500+ service connectors 
- Searchable node catalog 
- Category organization 
- SVG icons for all vendors 
- Color-coded by type 
- N8N JSON import/export SAM Theater System 
- Theatrical workflow assembly 
- Phase-based node creation 
- Animated connection drawing 
- 4-column hybrid layout 
- Complexity-aware timing 
- Visual assembly planning 
- Dramatic presentation mode Workflow Management 
- Tree, Kanban, Form views 
- Business unit organization 
- Execution history tracking 
- Template library 
- Version control 
- Status management 
- Activity logging API Credential Vault 
- Encrypted key storage 
- Per-vendor credentials 
- OAuth 2.0 support 
- Connection testing 
- Access control 
- Audit logging 
- Multi-environment support Node Context Chat 
- SAM AI integration 
- Node-aware conversations 
- Configuration assistance 
- Error troubleshooting 
- Best practice suggestions 
- Streaming responses 
- Memory-enhanced context 
## Supported Vendors 

The platform includes 306 vendor node types organized by category. Here are some popular integrations: 
### Communication Slack Discord Telegram Microsoft Teams Email (SMTP/IMAP) Twilio 
### Cloud Services AWS (S3, Lambda, SQS) Google Cloud Azure DigitalOcean Cloudflare 
### CRM & Sales Salesforce HubSpot Pipedrive Zoho CRM Freshsales 
### Productivity Google Sheets Notion Airtable Trello Asana Monday.com 
### Development GitHub GitLab Jira Linear HTTP Request Webhook 
### AI Services OpenAI Claude (Anthropic) Hugging Face Stability AI Replicate 
## Platform Skin Architecture 

SAM AI Workflows follows the **Platform Skin Architecture **- a clean separation between UI and data: Component ai_sam_workflows (THIS MODULE) ai_sam_workflows_base (SEPARATE) **Purpose **UI Layer (Views, JS, CSS) Data Layer (Models, Logic) **View XML Files **20 files None **JavaScript Files **19 files (10,000+ lines) None **CSS Files **4 files None **Vue Components **2 components None **HTTP Controllers **5 controllers (3 endpoints) RPC methods only **Python Models **None (UI-only) 15+ models **Database Tables **None All workflow data **Uninstall Impact **UI removed, data preserved All workflow data deleted **Data Safety Guarantee: **Uninstalling `ai_sam_workflows `(this module) removes
 only the UI components. All your workflows, executions, and credentials remain safe in the database.
 Reinstall anytime to restore full UI access. 
## REST API Endpoints 

This module provides 3 HTTP endpoints for workflow operations: Endpoint Method Description `/canvas/api/branches/available `GET Returns available canvas platform/branch types for UI selection `/canvas/{workflow_id}/nodes `GET Serves the workflow canvas HTML page with hierarchical node manager `/canvas/workflow/analyze `POST Analyzes N8N workflow JSON and generates theatrical assembly plan **API Documentation: **Full OpenAPI 3.0 specification available in `API_DOCUMENTATION.yaml `with request/response schemas and examples. 
## Technology Stack 
### Frontend Technologies Vanilla JavaScript Vue.js Components HTML5 Canvas CSS3 Custom Properties SVG Graphics Bezier Curves 
### Core JavaScript Modules canvas_manager.js node_manager.js connection_system.js node_type_registry.js theater_director.js icon_service.js 
### Integration Layer Odoo JSON-RPC REST HTTP N8N JSON Format SAM AI Chat API 
### Backend Systems (ai_sam_workflows_base) Python 3.10+ Odoo 18 ORM PostgreSQL Encrypted Storage 
## Getting Started 
### Installation Order 
- Install `ai_sam_base `- Core SAM AI foundation 
- Install `ai_sam `- SAM AI framework with vendor library 
- Install `ai_sam_workflows_base `- Workflow data models 
- Install `ai_sam_workflows `- This UI module **Module Dependencies: **
`ai_sam_base `-> `ai_sam `-> `ai_sam_workflows_base `-> `ai_sam_workflows `
### First Steps After Installation 
- **Access Workflow Canvas: **SAM AI -> Workflows -> Canvas 
- Create new workflow or import N8N JSON 
- Drag nodes from the sidebar 
- Connect nodes by clicking ports 
- **Configure Credentials: **SAM AI -> Workflows -> Credentials 
- Add API keys for vendors 
- Test connections 
- Organize by business unit 
- **Import N8N Workflow: **Use the Import Wizard 
- Paste N8N JSON export 
- Watch theatrical assembly 
- Customize as needed 
## Keyboard Shortcuts Shortcut Action `Space + Drag `Pan canvas `Scroll Wheel `Zoom in/out `Ctrl/Cmd + Z `Undo `Ctrl/Cmd + Shift + Z `Redo `Delete / Backspace `Delete selected node `Ctrl/Cmd + S `Save workflow `Ctrl/Cmd + F `Search nodes `Double-click `Edit node configuration 
## Ready to Automate? 

Build powerful workflow automations with N8N-style visual design in Odoo 18. Read Documentation View API Reference Get Support 
## Support & Resources 
### Documentation 
- `README.md `- Developer guide 
- `ARCHITECTURE.mermaid `- System diagrams 
- `API_DOCUMENTATION.yaml `- OpenAPI spec 
- `ai_sam_workflows_base/ `- Data layer docs 
### Links 
- Website: sme.ec 
- Email: sam@sme.ec 
- Support: anthony@sme.ec 
### Related Modules 
- `ai_sam_base `- Core foundation 
- `ai_sam `- Framework + UI 
- `ai_sam_workflows_base `- Data layer 
- `ai_sam_creatives `- Creative platform 

**SAM AI Workflows Platform **- Version 18.0.2.35.0 | UI Module 
Licensed under LGPL-3 | Odoo 18 Compatible 
© 2025 Anthony Gardiner | sme.ec

## Dependencies

- `ai_sam_workflows_base`
- `ai_sam`
- `ai_sam_base`
