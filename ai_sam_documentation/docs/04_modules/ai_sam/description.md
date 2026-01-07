# SAM AI UI

**Technical Name**: `ai_sam`
**Version**: 18.0.7.13

SAM AI Core Framework - Intelligence, Memory, Canvas, Workflow Automation & MCP Server Generation

## Description


SAM AI Core - V3 Architecture
==============================

🤖 SAM AI - The Intelligence Framework

This module provides the core SAM AI infrastructure that ALL branches depend on:

Canvas Framework:
-----------------
* Platform registry and loader system
* Core canvas engine (rendering, CRUD)
* Platform router and API
* Dynamic platform loading

SAM AI Core:
------------
* Claude API integration service
* All-knowing context builder (Odoo registry awareness)
* Token counter system (top-level UI)
* Module/branch registry watcher
* Base AI infrastructure

Memory System (Complete - Merged from ai_sam_memory 2025-10-24):
----------------------------------------------------------------
* Memory search integrated into chat
* Memory dashboard with statistics
* Graph visualization (vector-to-graph bridge)
* Conversation import and export
* Apache AGE graph database integration (Docker)
* ChromaDB vector database for semantic search
* Self-aware knowledge network visualization
* AI-powered document extraction engine

Workflow Automation Platform:
------------------------------
* Extracted to ai_sam_workflows module (Phase 3 - 2025-10-11)
* Install ai_sam_workflows for N8N workflow automation features

MCP Server Generation (Added 2025-11-04):
------------------------------------------
* Generate standalone MCP servers for Claude Desktop
* Expose Odoo data via Model Context Protocol (Anthropic standard)
* Support for Projects, CRM, Sales, Invoices, HR, Inventory
* Custom model exposure for any Odoo model
* OAuth-ready architecture for future API integration
* Download server script (.py) or manifest (.json)

SAM AI knows EVERYTHING about your Odoo system:
* All installed modules (ir.module.module)
* All models and fields (ir.model, ir.model.fields)
* All branches registered (ai.branch)
* What the user is looking at right now
* Complete system architecture

Architecture:
-------------
ai_sam_base (essential models) → ai_sam (framework + UI) → branches (ai_creatives, ai_odoo_blogger, etc.)

This is the core SAM AI framework - ALL branches depend on this.

**Note:** ai_brain module has been split into ai_sam_base (2025-11-27) to resolve installation issues.
    

## Module Details

# 🤖 SAM AI 

Complete AI Interface for Odoo 18 Version 1.0.0 | UI Module | Platform Skin Architecture 
## 📋 Overview 

**SAM AI **is the comprehensive UI layer for SAM AI - a sophisticated AI-powered framework for Odoo 18.
 Following the **Platform Skin Architecture **, this module contains NO Python business logic
 (all models/controllers moved to `ai_sam_base `) and focuses exclusively on delivering an exceptional user experience. **🏗️ Architecture Note: **This is a **UI-only module **. All Python models, controllers,
 and business logic are in the `ai_sam_base `module (67 HTTP endpoints, 43 models).
 This separation enables independent updates and better maintainability. 
## 📊 Module Statistics 629 Total Files 18 View XML Files 18 JavaScript Files 9,056 Lines in Chat JS 8 CSS Files 203 API Vendor Icons 301 SVG Icons Total 0 Python Models 
(UI-Only) 
## ✨ Key Features 💬 Chat Interface V2 
- Vanilla JavaScript (9,056 lines) 
- Multi-tab conversations 
- Real-time streaming (SSE) 
- Memory-enhanced responses 
- Token counter widget 
- Chat bubble launcher 
- Markdown + syntax highlighting 🧠 Memory System 
- Dual database (ChromaDB + Apache AGE) 
- Vector embeddings (768-dim) 
- Graph relationships 
- Vis.js visualization 
- Team memory sharing 
- Access auditing 
- Semantic search 🎨 Canvas Framework 
- Platform-agnostic design 
- HTML5 Canvas rendering 
- Coordinate transformations 
- Node CRUD with undo/redo 
- N8N JSON compatibility 
- Drag-and-drop interface 
- Visual workflow builder 🔌 API Management 
- 203 vendor integrations 
- 301 SVG provider icons 
- 8-tab progressive disclosure 
- Encrypted API keys 
- Live connection testing 
- Cost intelligence tracking 
- Multi-provider orchestration 🚀 MCP Server Generation 
- Standalone Python servers 
- Claude Desktop integration 
- Model Context Protocol 
- Odoo data exposure 
- Automatic deployment 
- Permission configuration 
- Systemd service creation 🤖 Hierarchical AI Agents 
- Power Prompts system 
- Master → Child → Grandchild 
- Visual indentation 
- Context inheritance 
- Prompt chaining 
- Template library 
- Sequential execution 💰 Cost Intelligence 
- Per-model cost tracking 
- Per-user allocation 
- Budget alerts 
- Pivot/graph analysis 
- Optimization recommendations 
- Token usage analytics 
- Multi-dimensional reports 👥 Team Collaboration 
- Shared workspaces 
- Role-based permissions 
- Conversation templates 
- Team analytics 
- Real-time collaboration 
- Activity notifications 
- Usage statistics 
## 🏗️ Platform Skin Architecture 

SAM AI follows the **Platform Skin Architecture **pattern with clear separation between UI and business logic: Component ai_sam (THIS MODULE) ai_sam_base (SEPARATE) **View XML Files **✓ 18 files ✗ None **JavaScript Files **✓ 18 files (9,056 lines) ✗ None **CSS Files **✓ 8 files ✗ None **QWeb Templates **✓ Chat, Memory, Canvas ✗ None **Vendor Icons **✓ 203 providers, 301 SVGs ✗ None **Menu Definitions **✓ Consolidated structure ✗ None **Python Models **✗ None (UI-only) ✓ 43 models **HTTP Controllers **✗ None (UI-only) ✓ 10 controllers (67 endpoints) **Business Logic **✗ None (UI-only) ✓ All business logic **Security/ACL **✓ UI-related rules (20) ✓ Model access rules **⚡ Benefits of Separation: **
- ✓ Update UI without Python restarts 
- ✓ Independent versioning and releases 
- ✓ Clearer dependency management 
- ✓ Easier testing and debugging 
- ✓ Better code maintainability 
## 🛠️ Technology Stack 
### Frontend Technologies Vanilla JavaScript HTML5 Canvas CSS3 (Custom Properties) Proxy-Based Reactivity Server-Sent Events (SSE) Marked.js (Markdown) Prism.js (Syntax) Vis.js (Graphs) 
### Integration Layer Odoo JSON-RPC REST HTTP WebSocket Support N8N JSON Format MCP Protocol 
### Backend Systems (ai_sam_base) Python 3.10+ Odoo 18 Framework PostgreSQL + AGE ChromaDB Claude API OpenAI API Google AI APIs 
## 🆚 SAM AI vs. Alternatives Feature SAM AI ChatGPT Claude Web Generic Odoo Chat **Odoo Integration **✓ Native ✗ ✗ ✓ Basic **Memory System **✓ Dual DB (Vector + Graph) ✓ Limited ✓ Projects ✗ **Multi-Provider Support **✓ 203 providers ✗ OpenAI only ✗ Anthropic only ✓ Limited **Cost Intelligence **✓ Per-model tracking ✓ Basic ✓ Basic ✗ **Visual Workflows **✓ N8N-compatible canvas ✗ ✗ ✗ **Team Collaboration **✓ Workspaces + Roles ✓ Team plans ✓ Team plans ✗ **MCP Server Generation **✓ Automatic ✗ ✗ ✗ **Hierarchical Agents **✓ Power Prompts ✗ ✗ ✗ **Self-Hosted **✓ Full control ✗ Cloud only ✗ Cloud only ✓ If Odoo self-hosted **Open Source **✓ LGPL-3 ✗ Proprietary ✗ Proprietary ✓ Depends 
## 🚀 Getting Started 
### Installation Steps 
- Install `ai_sam_base `module first (data layer) 
- Install `ai_sam_workflows_base `module (workflow data layer) 
- Install `ai_sam `module (UI layer - this module) 
- Configure external databases (ChromaDB + Apache AGE) 
- Add at least one API provider (Claude, OpenAI, or Google) 
- Test API connection in Configuration → API Providers **📦 Module Installation Order: **
1. ai_sam_base (data layer) 
2. ai_sam_workflows_base (workflow data) 
3. ai_sam (UI layer - this module) 
### First Steps After Installation 
- **Configure API Provider: **SAM AI → Configuration → API Providers → Create 
- Select provider (Claude, OpenAI, Google, etc.) 
- Enter API key (encrypted storage) 
- Test connection 
- **Start First Conversation: **Click chat bubble or navigate to SAM AI → Chat 
- Type your first message 
- Watch AI respond with streaming 
- Conversation automatically saved to memory 
- **Explore Memory System: **SAM AI → Memory → Dashboard 
- View memory statistics 
- Explore graph visualization 
- Search past conversations 
## Ready to Get Started? 

Transform your Odoo experience with SAM AI's comprehensive AI interface. 📖 Read Full Documentation 🎥 Watch Video Tutorial 💬 Get Support 
## 📞 Support & Resources 
### 📚 Documentation 
- `README.md `- Developer guide 
- `ARCHITECTURE.mermaid `- System diagrams 
- `API_DOCUMENTATION.yaml `- API reference 
- `ai_sam_base/ `- Backend documentation 
### 🌐 Links 
- Website: samai.com 
- Email: support@samai.com 
- GitHub: Your repository 
- Community: Discussion forums 
### 🛠️ Development 
- Platform Skin Architecture 
- Vanilla JavaScript (no OWL) 
- Proxy-based reactivity 
- Odoo 18 framework 

**SAM AI **- Version 1.0.0 | UI Module 
Licensed under LGPL-3 | Odoo 18 Compatible 
© 2025 SAM AI Team | samai.com

## Dependencies

- `base`
- `web`
- `ai_sam_base`
- `sam_ui_theme`
