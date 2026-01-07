# SAM AI Workflows Base

**Technical Name**: `ai_sam_workflows_base`
**Version**: 18.0.1.9.3

SAM AI - Workflow Automation & N8N Integration (Data Layer)

## Description


SAM AI Workflows - Data Layer
==============================

This module contains workflow automation models and N8N integration.

**Models:**
- Canvas: N8N-compatible workflow definitions (core model)
- Workflow executions tracking
- N8N dynamic menus
- N8N import wizard
- N8N menu debug tools
- N8N node categories
- Automator configuration

**NOTE:** Workflow templates extracted to ai_sam_workflows_templates module (2024-12-19)

**Architecture:**
Pure data module (models only, no UI).
UI layer should be in ai_sam or separate UI module.

**Dependencies:**
- ai_sam_base: Core SAM AI foundation
    

## Module Details

# SAM AI Workflows Base 

Workflow automation & N8N integration - Data layer Version 1.0.2 
## What is SAM AI Workflows Base? 

SAM AI Workflows Base is the **data persistence layer **for SAM AI's workflow automation system,
 providing seamless **N8N integration **and visual workflow building capabilities. 

**Key Features: **
- **N8N Compatible **- Full import/export support for N8N workflows 
- **Visual Workflow Builder **- Drag-and-drop canvas interface 
- **195+ Node Types **- Triggers, actions, logic, and data transformation 
- **Multi-API Integration **- OpenAI, Slack, GitHub, and 10+ services 
- **Template Marketplace **- Share and reuse workflows 
- **Execution Tracking **- Complete audit trail and logs 
## Module Statistics 15 Data Models 195+ Node Types 45+ RPC Methods 14+ API Integrations 
## Core Capabilities 🔄 
### Workflow Automation 

Build complex automation workflows using visual drag-and-drop canvas.
 Connect triggers, actions, and logic nodes to automate business processes. 🔌 
### N8N Integration 

Full compatibility with N8N workflow format. Import existing N8N workflows
 or export your workflows to use in N8N. 📦 
### Template Library 

Pre-built workflow templates for common use cases: email automation,
 CRM lead processing, inventory reordering, and more. ⚡ 
### Multi-Trigger Support 

Execute workflows manually, via webhooks, on schedule (cron), or
 triggered by Odoo events. 📊 
### Execution Tracking 

Complete execution history with timestamps, duration, success/failure states,
 error logs, and per-node execution details. 🏢 
### Business Units 

Organize workflows by department: Sales, Marketing, Operations, Finance,
 HR, and IT with pre-configured demo workflows. 
## Supported Node Types 
### 195+ N8N Nodes Category Examples Count **Triggers **Webhook, Cron, Email Trigger 15+ **Actions **HTTP Request, Email Send, Database Query 120+ **Logic **IF, Switch, Merge, Split 10+ **Data Transform **Set, Function, Code, Item Lists 20+ **Integrations **Slack, GitHub, Notion, Stripe 30+ 
## Supported API Integrations 

**14+ Pre-Configured Credential Types: **
- **OpenAI API **- GPT-4, ChatGPT integration 
- **Slack API **- Send messages, notifications 
- **Telegram Bot API **- Telegram bot automation 
- **GitHub API **- Repository management 
- **Notion API **- Database and page management 
- **Google Sheets API **- Spreadsheet automation 
- **Stripe API **- Payment processing 
- **HubSpot API **- CRM automation 
- **Salesforce API **- Enterprise CRM 
- **Airtable API **- Database automation 
- **Discord Webhooks **- Discord notifications 
- **HTTP Basic Auth **- Generic HTTP authentication 
- **OAuth 2.0 **- OAuth authentication 
- **Custom APIs **- Bring your own API 
## How It Works 
- **Install Dependencies: **Ensure `ai_sam_base `is installed first 
- **Install This Module: **Apps → SAM AI Workflows Base → Install 
- **Create Workflow: **Open visual canvas and drag-and-drop nodes 
- **Connect Nodes: **Wire nodes together to define workflow logic 
- **Configure Credentials: **Add API keys for external services 
- **Test Execution: **Run workflow manually to test 
- **Set Trigger: **Configure webhook, schedule, or manual trigger 
- **Monitor Executions: **View execution history and logs 
## Architecture - Platform Skin Pattern 

This module follows the **Platform Skin Architecture **: 
- **ai_sam_workflows_base **(this module) - Python data models only 
- **ai_sam **(UI module) - Views, templates, controllers, canvas interface 

**Benefits: **
- ✅ Clean separation of data and UI layers 
- ✅ Independent testing of workflow logic 
- ✅ Simplified model structure 
- ✅ Easier debugging and maintenance 
## Technical Details 
### Key Models Model Purpose `canvas `Core workflow definition (N8N-compatible JSON) `executions `Workflow execution tracking and logs `workflow.template `Reusable workflow templates `api_credentials `API keys and OAuth tokens `workflow.business.unit `Departmental organization `node_types `Node type registry (195+ types) 
### Data Storage - Single Source of Truth 

**Flatline Data Architecture (Phase 1 Migration): **
- `canvas.json_definition `is the **single source of truth **
- Complete N8N-compatible JSON stored in one field 
- No dual storage complexity (deprecated `nodes `table) 
- Direct import/export compatibility with N8N 
## Pre-Loaded Demo Content 
### 6 Business Units 
- **SALES **- Sales Department (3 demo workflows) 
- **MKT **- Marketing (3 demo workflows) 
- **OPS **- Operations (2 demo workflows) 
- **FIN **- Finance & Accounting (2 demo workflows) 
- **HR **- Human Resources (2 demo workflows) 
- **IT **- Information Technology (2 demo workflows) 
### 3 Workflow Templates 
- **Email Automation Template **- Basic email sending workflow 
- **CRM Lead Processing Template **- Lead qualification and assignment 
- **Inventory Reorder Template **- Stock monitoring and auto-reordering 
## Getting Started 
### Prerequisites 
- Odoo 18.0 or higher 
- Python 3.10 or higher 
- **ai_sam_base **module installed 
- API keys for external services (optional) 
### Installation 
- Ensure `ai_sam_base `is installed 
- Navigate to Apps → Search "SAM AI Workflows Base" 
- Click Install 
- Wait for installation to complete 
- Configure API credentials in Settings if needed 
## Documentation Resources 
- **Developer Guide: **See `README.md `in module directory 
- **Architecture Diagrams: **See `ARCHITECTURE.mermaid `(6 diagrams) 
- **API Documentation: **See `API_DOCUMENTATION.yaml `(RPC methods) 
- **N8N Documentation: **https://docs.n8n.io/ 
## Support 
- **Website: **https://samai.com 
- **Author: **SAM AI 
- **License: **LGPL-3 
- **Version: **1.0.2 

**SAM AI Workflows Base **- Workflow automation & N8N integration 

Version 1.0.2 | LGPL-3 License | SAM AI Visit SAM AI Website

## Dependencies

- `base`
- `mail`
- `ai_sam_base`
