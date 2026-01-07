# SAM AI Architecture Guide
**Version:** 1.0
**Last Updated:** 2025-12-06
**Status:** ✅ Official Architecture Documentation

---

## 📋 Table of Contents
1. [Overview](#overview)
2. [The Core Philosophy](#the-core-philosophy)
3. [Module Structure](#module-structure)
4. [Module Ownership Matrix](#module-ownership-matrix)
5. [Dependency Architecture](#dependency-architecture)
6. [AI Agent Placement Rules](#ai-agent-placement-rules)
7. [Common Scenarios](#common-scenarios)
8. [Forbidden Patterns](#forbidden-patterns)
9. [Migration from ai_brain](#migration-from-ai_brain)
10. [Troubleshooting](#troubleshooting)

---

## 🎯 Overview

SAM AI uses a **two-layer architecture** with a **dependency chain** pattern:

- **Layer 1: Core Intelligence** (Base modules) - Protected data models
- **Layer 2: Evolving Skins** (Presentation modules) - UI, controllers, static assets

**Key Principle:** Preserve the intelligence (data), allow skins to evolve/break/rebuild.

---

## 🧠 The Core Philosophy

### **Why This Architecture?**

**Problem Solved:**
> "ai_brain became too big, debugging was a nightmare. We split models into base modules to preserve core intelligence while allowing UI to evolve."

**Design Goals:**
1. **Protect Data:** Core models in "base" modules, stable and preserved
2. **Allow Evolution:** UI/controllers in "skin" modules, can break/rebuild
3. **Centralize Knowledge:** Supplier-specific assets in one place (ai_sam)
4. **Clear Ownership:** Every file has an obvious home

---

## 🏗️ Module Structure

### **Repository Location**
```
D:\SAMAI-18-SaaS\github-repos\05-samai-core\
```

### **Active Modules**

```
05-samai-core/
│
├── ai_sam_base/              # LAYER 1: Core SAM Intelligence
│   ├── models/               # 44 data models
│   ├── data/                 # Data files
│   ├── security/             # Security rules
│   └── NO views, NO static, NO controllers
│
├── ai_sam/                   # LAYER 2: Supplier Knowledge Hub + Core UI
│   ├── views/                # Views for ai_sam_base models
│   ├── static/
│   │   └── src/
│   │       └── vendor_library/  # 🔑 Supplier assets (icons, metadata)
│   ├── data/                 # UI data (menus, actions)
│   ├── security/             # View-level security
│   └── NO models
│
├── ai_sam_workflows_base/    # LAYER 1: Workflow Intelligence
│   ├── models/               # 15 workflow data models
│   ├── data/                 # Data files
│   ├── security/             # Security rules
│   └── NO views, NO static, NO controllers
│
├── ai_sam_workflows/         # LAYER 2: Workflow Execution Engine + UI
│   ├── models/               # NO models here (use base)
│   ├── controllers/          # HTTP endpoints, RPC handlers
│   ├── views/                # Views for workflows_base models
│   ├── static/
│   │   └── src/
│   │       └── automator/    # Workflow UI (canvas, overlays)
│   └── data/                 # UI data
│
└── ai_sam_cache_manager/     # Utility module
```

### **Deprecated Modules**
```
04-samai-brain/               # ⚠️ DEPRECATED
└── ai_brain/                 # Being migrated to base modules
```

**Status:** Models being migrated to `ai_sam_base` or `ai_sam_workflows_base`

---

## 📊 Module Ownership Matrix

### **ai_sam_base** (Core SAM Intelligence)

| Component | Owns | Forbidden |
|-----------|------|-----------|
| **Purpose** | Core SAM data models | UI, static assets |
| **Models** | ✅ Conversations, messages, agents, memory, providers, services | ❌ Workflow models |
| **Data** | ✅ XML data files, security rules | ❌ Views |
| **Static** | ❌ None | ❌ Icons, JS, CSS |
| **Controllers** | ❌ None | ❌ HTTP endpoints |

**Key Models (44 total):**
- `ai_conversation.py` - Conversation management
- `ai_message.py` - Message storage
- `ai_agent_definition.py` - Agent configurations
- `ai_agent_knowledge.py` - Agent knowledge base
- `ai_workspace.py` - Workspace management
- `ai_context_builder.py` - Context assembly
- `ai_memory_*.py` - Memory system
- `ai_provider_*.py` - AI provider management
- `sam_*.py` - SAM behavior, personality, settings
- `mcp_*.py` - MCP server configurations

**Depends On:** Base Odoo modules only

---

### **ai_sam** (Supplier Knowledge Hub + Core UI)

| Component | Owns | Forbidden |
|-----------|------|-----------|
| **Purpose** | Supplier-specific assets + Core SAM views | Data models |
| **Models** | ❌ None | ❌ All models go to ai_sam_base |
| **Views** | ✅ Views for ai_sam_base models | ❌ Workflow views |
| **Static** | ✅ `vendor_library/` (supplier icons, metadata, API configs) | ❌ Workflow UI |
| **Controllers** | ✅ Minimal (if needed for core SAM) | ❌ Workflow controllers |
| **Data** | ✅ Menus, actions, UI-related data | ❌ Business data |

**vendor_library Structure:**
```
ai_sam/static/src/vendor_library/
├── _registry/
│   └── node_metadata.json      # Centralized supplier metadata
├── [Supplier]/                 # One folder per supplier
│   ├── icon.svg                # Supplier icon
│   ├── icon.png                # Optional PNG
│   ├── icon.dark.svg           # Optional dark mode
│   ├── api_config.json         # API configuration
│   └── services/               # Sub-services (for Google, Microsoft)
```

**Examples:**
- `vendor_library/ActiveCampaign/activeCampaign.svg`
- `vendor_library/Google/Drive/googleDrive.svg`
- `vendor_library/_registry/node_metadata.json`

**Depends On:**
- `ai_sam_base` (for data models)

**Role Clarification:**
> ai_sam is NOT a pure "skin" - it's the **Supplier Knowledge Hub**. All supplier-specific assets (icons, API configs, metadata) live here, making it a foundational dependency for other modules.

---

### **ai_sam_workflows_base** (Workflow Intelligence)

| Component | Owns | Forbidden |
|-----------|------|-----------|
| **Purpose** | Workflow data models | UI, controllers |
| **Models** | ✅ Canvas, nodes, executions, N8N definitions | ❌ Core SAM models |
| **Data** | ✅ XML data files, security rules | ❌ Views |
| **Static** | ❌ None | ❌ Icons, UI assets |
| **Controllers** | ❌ None | ❌ HTTP endpoints |

**Key Models (15 total):**
- `n8n_simple_nodes.py` - N8N node definitions (computes icon URLs → ai_sam)
- `n8n_simple_extractor.py` - N8N node extraction/scanning
- `canvas.py` - Canvas data model
- `nodes.py` - Workflow node definitions
- `executions.py` - Workflow execution tracking
- `workflow_templates.py` - Template storage
- `business_unit.py` - Business unit management

**Depends On:**
- `ai_sam_base` (for core models)
- Reads from `ai_sam/static/src/vendor_library/` (computes icon URLs)

**Critical Pattern:**
```python
# In n8n_simple_nodes.py
@api.depends('icon_svg_path')
def _compute_icon_urls(self):
    base_url = '/ai_sam/static/src/vendor_library'  # ✅ Points to ai_sam
    for node in self:
        if node.icon_svg_path:
            node.icon_svg_url = f"{base_url}/{node.icon_svg_path}"
```

---

### **ai_sam_workflows** (Workflow Execution Engine + UI)

| Component | Owns | Forbidden |
|-----------|------|-----------|
| **Purpose** | Workflow UI, controllers, execution logic | Data models |
| **Models** | ❌ None | ❌ All models go to workflows_base |
| **Views** | ✅ Views for workflows_base models | ❌ Core SAM views |
| **Static** | ✅ Workflow UI (canvas, overlays, node rendering) | ❌ Supplier icons (use ai_sam) |
| **Controllers** | ✅ HTTP endpoints, RPC handlers | ❌ Core SAM controllers |

**Key Components:**
- `controllers/` - Canvas API endpoints, RPC handlers
- `static/src/automator/n8n/overlays/overlay_manager.js` - N8N node overlay UI
- `views/` - Workflow views (canvas, execution logs)

**Depends On:**
- `ai_sam_workflows_base` (for workflow models)
- `ai_sam` (for supplier icons/metadata from vendor_library)

**Critical Pattern:**
```javascript
// In overlay_manager.js
async loadN8nNodes() {
    // Fetch icon URLs from database (computed by workflows_base)
    fields: ['icon_svg_url', 'icon_png_url', ...]
}

getSupplierIcon(nodeData) {
    // Use database-provided URLs (pointing to ai_sam/vendor_library)
    if (nodeData.icon_svg_url) {
        return `<img src="${nodeData.icon_svg_url}" ... />`; // ✅
    }
}
```

---

## 🔗 Dependency Architecture

### **Dependency Chain**

```
┌─────────────────────────────────────────────────────────────┐
│ LAYER 1: CORE INTELLIGENCE (Protected, Stable)              │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ai_sam_base/                  ai_sam_workflows_base/       │
│  ├── 44 models                 ├── 15 models                │
│  ├── Core SAM data             ├── Workflow data            │
│  └── Depends on: Odoo base     └── Depends on: ai_sam_base  │
│                                                              │
└──────────────┬───────────────────────────────────────┬──────┘
               │                                       │
               │ (provides data)                       │ (provides data)
               │                                       │
┌──────────────▼───────────────────────────────────────▼──────┐
│ LAYER 2: EVOLVING SKINS (Can Break/Rebuild)                 │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ai_sam/                       ai_sam_workflows/            │
│  ├── Supplier Knowledge Hub    ├── Workflow Execution       │
│  ├── vendor_library/           ├── Controllers, UI          │
│  ├── Core SAM views            ├── Depends on:              │
│  └── Depends on: ai_sam_base   │   - workflows_base         │
│                                 │   - ai_sam (supplier info)│
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### **The "Skin-Depends-On-Skin" Pattern**

**Question:** Why does `ai_sam_workflows` (skin) depend on `ai_sam` (skin)?

**Answer:** Because `ai_sam` is not a pure skin - it's the **Supplier Knowledge Hub**.

```
ai_sam_workflows needs:
  ├─ Workflow data models → ai_sam_workflows_base ✅
  ├─ Supplier icons → ai_sam/vendor_library/ ✅
  └─ Supplier metadata → ai_sam/vendor_library/_registry/ ✅
```

**This is CORRECT and INTENTIONAL architecture.**

**Alternative (REJECTED):**
- ❌ Duplicate supplier assets in workflows module (violates DRY)
- ❌ Create separate library module (over-engineering)
- ✅ Centralize supplier knowledge in ai_sam (single source of truth)

---

### **Dependency Graph**

```
Odoo Base
    ↓
ai_sam_base (core models)
    ↓
    ├──→ ai_sam (supplier hub + views)
    │       ↑
    └──→ ai_sam_workflows_base (workflow models)
            ↓
        ai_sam_workflows (workflow UI)
            └──→ ai_sam (for supplier assets) ✅
```

**Key Insight:** The dependency `ai_sam_workflows → ai_sam` is a **feature, not a bug**.

---

## 🤖 AI Agent Placement Rules

### **Rule 1: Data Models**

**Question:** Where do I add a new data model?

**Decision Tree:**
```
Is it workflow-specific? (canvas, executions, nodes)
    YES → ai_sam_workflows_base/models/
    NO  → Is it core SAM? (conversations, agents, memory)
        YES → ai_sam_base/models/
        NO  → Check if it belongs in another module
```

**Examples:**
- ✅ New conversation field → `ai_sam_base/models/ai_conversation.py`
- ✅ New workflow execution tracking → `ai_sam_workflows_base/models/executions.py`
- ❌ NEVER add models to skin modules (ai_sam, ai_sam_workflows)

---

### **Rule 2: Supplier Assets**

**Question:** Where do I add supplier-specific assets? (icons, API configs, metadata)

**Answer:** ALWAYS → `ai_sam/static/src/vendor_library/`

**Process:**
1. Create supplier folder: `ai_sam/static/src/vendor_library/[Supplier]/`
2. Add icon files: `icon.svg`, `icon.png` (optional)
3. Add API config: `api_config.json` (if applicable)
4. Update metadata: `ai_sam/static/src/vendor_library/_registry/node_metadata.json`

**Example: Adding "Stripe"**
```bash
ai_sam/static/src/vendor_library/
└── Stripe/
    ├── stripe.svg
    ├── stripe.png
    └── api_config.json
```

Update registry:
```json
// ai_sam/static/src/vendor_library/_registry/node_metadata.json
{
  "stripe": {
    "icon": "file:stripe.svg",
    "n8n_type": "n8n-nodes-base.stripe",
    "folder": "Stripe"
  }
}
```

---

### **Rule 3: Views (XML)**

**Question:** Where do I add views?

**Decision Tree:**
```
View is for which model?
    ai_sam_base model → ai_sam/views/
    ai_sam_workflows_base model → ai_sam_workflows/views/
```

**Examples:**
- ✅ View for `ai_conversation` → `ai_sam/views/ai_conversation_views.xml`
- ✅ View for `canvas` → `ai_sam_workflows/views/canvas_views.xml`

---

### **Rule 4: Controllers (HTTP Endpoints)**

**Question:** Where do I add controllers/RPC endpoints?

**Decision Tree:**
```
Controller is for which feature?
    Core SAM (conversations, agents) → ai_sam/controllers/
    Workflows (canvas, execution) → ai_sam_workflows/controllers/
```

**Examples:**
- ✅ Conversation API → `ai_sam/controllers/conversation_controller.py`
- ✅ Canvas API → `ai_sam_workflows/controllers/canvas_controller.py`

---

### **Rule 5: Frontend JavaScript**

**Question:** Where do I add frontend JavaScript/CSS?

**Decision Tree:**
```
JavaScript is for which feature?
    Supplier-agnostic workflow UI (canvas, overlays) → ai_sam_workflows/static/src/
    Core SAM UI → ai_sam/static/src/
```

**Examples:**
- ✅ Canvas rendering → `ai_sam_workflows/static/src/automator/canvas/`
- ✅ N8N overlay → `ai_sam_workflows/static/src/automator/n8n/overlays/`
- ✅ Core SAM widgets → `ai_sam/static/src/components/`

**IMPORTANT:** Frontend JavaScript should:
- ✅ Use database-provided URLs for icons
- ❌ NEVER construct hardcoded paths to vendor_library
- ✅ Load supplier data from RPC endpoints (which read from models)

---

## 📚 Common Scenarios

### **Scenario 1: Adding a New Supplier (e.g., "Mailchimp")**

**Steps:**

1. **Add supplier assets** → `ai_sam/static/src/vendor_library/`
```bash
ai_sam/static/src/vendor_library/
└── Mailchimp/
    ├── mailchimp.svg
    └── api_config.json
```

2. **Update metadata registry** → `ai_sam/static/src/vendor_library/_registry/node_metadata.json`
```json
{
  "mailchimp": {
    "icon": "file:mailchimp.svg",
    "n8n_type": "n8n-nodes-base.mailchimp",
    "folder": "Mailchimp"
  }
}
```

3. **Add N8N node model** → `ai_sam_workflows_base/models/n8n_simple_nodes.py`
```python
# Database record created via extractor or manually
# Model will auto-compute icon_svg_url pointing to ai_sam
```

4. **Frontend uses database URLs** → `ai_sam_workflows/static/src/`
```javascript
// Frontend loads icon_svg_url from database (already pointing to ai_sam)
// No changes needed if using getSupplierIcon() correctly
```

**Files Modified:**
- `ai_sam/static/src/vendor_library/Mailchimp/` (new folder)
- `ai_sam/static/src/vendor_library/_registry/node_metadata.json` (updated)
- Possibly `ai_sam_workflows_base/models/n8n_simple_extractor.py` (scan trigger)

**Files NOT Modified:**
- ❌ ai_sam_workflows (frontend uses database URLs)
- ❌ No duplication of assets

---

### **Scenario 2: Adding a New Workflow Feature (e.g., "Workflow Templates")**

**Steps:**

1. **Add data model** → `ai_sam_workflows_base/models/workflow_templates.py`
```python
from odoo import models, fields

class WorkflowTemplate(models.Model):
    _name = 'workflow.template'
    _description = 'Workflow Templates'

    name = fields.Char(required=True)
    canvas_data = fields.Text()
```

2. **Add views** → `ai_sam_workflows/views/workflow_template_views.xml`
```xml
<odoo>
    <record id="view_workflow_template_form" model="ir.ui.view">
        <field name="name">workflow.template.form</field>
        <field name="model">workflow.template</field>
        <field name="arch" type="xml">
            <form>
                <field name="name"/>
                <field name="canvas_data"/>
            </form>
        </field>
    </record>
</odoo>
```

3. **Add controller** (if needed) → `ai_sam_workflows/controllers/template_controller.py`
```python
from odoo import http
from odoo.http import request

class TemplateController(http.Controller):
    @http.route('/workflow/templates', type='json', auth='user')
    def get_templates(self):
        templates = request.env['workflow.template'].search([])
        return templates.read(['name', 'canvas_data'])
```

4. **Add frontend UI** → `ai_sam_workflows/static/src/templates/`

**Files Modified:**
- `ai_sam_workflows_base/models/` (data model)
- `ai_sam_workflows/views/` (XML views)
- `ai_sam_workflows/controllers/` (API endpoint)
- `ai_sam_workflows/static/` (frontend UI)

**Files NOT Modified:**
- ❌ ai_sam (this is workflow-specific)
- ❌ ai_sam_base (this is workflow-specific)

---

### **Scenario 3: Adding a Core SAM Feature (e.g., "Agent Tags")**

**Steps:**

1. **Add data model** → `ai_sam_base/models/ai_agent_tag.py`
```python
from odoo import models, fields

class AgentTag(models.Model):
    _name = 'ai.agent.tag'
    _description = 'Agent Tags'

    name = fields.Char(required=True)
    color = fields.Integer()
```

2. **Add views** → `ai_sam/views/ai_agent_tag_views.xml`

3. **Add controller** (if needed) → `ai_sam/controllers/`

4. **Add frontend UI** → `ai_sam/static/src/`

**Files Modified:**
- `ai_sam_base/models/` (data model)
- `ai_sam/views/` (XML views)
- `ai_sam/controllers/` (API endpoint)
- `ai_sam/static/` (frontend UI)

**Files NOT Modified:**
- ❌ ai_sam_workflows (this is core SAM, not workflow-specific)

---

## 🚫 Forbidden Patterns

### **❌ Pattern 1: Models in Skin Modules**

**WRONG:**
```python
# ai_sam/models/my_model.py  ❌ FORBIDDEN
from odoo import models, fields

class MyModel(models.Model):
    _name = 'my.model'
```

**RIGHT:**
```python
# ai_sam_base/models/my_model.py  ✅ CORRECT
from odoo import models, fields

class MyModel(models.Model):
    _name = 'my.model'
```

**Why:** Skins are for presentation (views, controllers, static). Data belongs in base modules.

---

### **❌ Pattern 2: Duplicate Supplier Assets**

**WRONG:**
```
ai_sam/static/src/vendor_library/Stripe/stripe.svg  ✅
ai_sam_workflows/static/icons/stripe.svg  ❌ DUPLICATE!
```

**RIGHT:**
```
ai_sam/static/src/vendor_library/Stripe/stripe.svg  ✅ (only copy)
ai_sam_workflows/ uses database URLs → /ai_sam/...  ✅
```

**Why:** Single source of truth. Duplication leads to sync issues.

---

### **❌ Pattern 3: Hardcoded Paths in Frontend**

**WRONG:**
```javascript
// ai_sam_workflows/static/src/automator/overlay_manager.js
const iconPath = `/ai_sam_workflows/static/icons/${supplier}.svg`; // ❌
```

**RIGHT:**
```javascript
// Load icon URLs from database
async loadN8nNodes() {
    fields: ['icon_svg_url', 'icon_png_url', ...]  // ✅
}

getSupplierIcon(nodeData) {
    if (nodeData.icon_svg_url) {
        return `<img src="${nodeData.icon_svg_url}" ... />`;  // ✅
    }
}
```

**Why:** Paths are computed by backend (`n8n_simple_nodes.py`), frontend uses them. Single source of truth.

---

### **❌ Pattern 4: Cross-Layer Dependencies**

**WRONG:**
```
ai_sam_base/ depends on ai_sam/  ❌ (data depends on skin)
```

**RIGHT:**
```
ai_sam/ depends on ai_sam_base/  ✅ (skin depends on data)
```

**Why:** Data layer must be independent. Skins depend on data, never the reverse.

**Exception:** `ai_sam_workflows` → `ai_sam` is allowed (supplier knowledge hub pattern).

---

### **❌ Pattern 5: Workflow Code in Core SAM**

**WRONG:**
```python
# ai_sam_base/models/workflow_execution.py  ❌
# Workflow-specific model in core SAM base
```

**RIGHT:**
```python
# ai_sam_workflows_base/models/executions.py  ✅
# Workflow models in workflow base
```

**Why:** Clear separation of concerns. Core SAM ≠ Workflows.

---

## 📦 Migration from ai_brain

### **Current Status**
- **ai_brain module:** Located in `04-samai-brain` repo
- **Status:** ⚠️ DEPRECATED (in "debug hold")
- **Goal:** Migrate all models to `ai_sam_base` or `ai_sam_workflows_base`

### **Migration Decision Tree**

**For each model in ai_brain:**

```
Is the model workflow-specific?
    YES → Migrate to ai_sam_workflows_base/models/
    NO  → Migrate to ai_sam_base/models/
```

**Examples:**
- `conversation.py` → `ai_sam_base/models/ai_conversation.py`
- `canvas.py` → `ai_sam_workflows_base/models/canvas.py`
- `agent.py` → `ai_sam_base/models/ai_agent_definition.py`

### **Migration Steps**

1. **Audit:** List all models in ai_brain
2. **Categorize:** Core SAM vs Workflow
3. **Move:** Copy model to appropriate base module
4. **Update:** Fix imports in dependent code
5. **Test:** Verify functionality
6. **Remove:** Delete from ai_brain once verified
7. **Archive:** Mark ai_brain as deprecated

### **Post-Migration**

- [ ] All models migrated
- [ ] No imports from ai_brain
- [ ] ai_brain module archived
- [ ] Documentation updated

---

## 🔧 Troubleshooting

### **Problem: Icons Not Loading (404 Errors)**

**Symptoms:**
- Browser console shows 404 for icon files
- Icons display emoji fallbacks (⚙️)

**Root Cause:**
- Frontend constructing wrong paths (not using database URLs)

**Solution:**
1. Verify icons exist: `ai_sam/static/src/vendor_library/[Supplier]/icon.svg`
2. Verify database model computes URLs: `n8n_simple_nodes.py` → `icon_svg_url`
3. Verify frontend loads URLs: `loadN8nNodes()` includes `icon_svg_url` field
4. Verify frontend uses URLs: `getSupplierIcon()` uses `nodeData.icon_svg_url`

**See:** Icon path fix (2025-12-06) as reference implementation

---

### **Problem: Model Not Found**

**Symptoms:**
- `odoo.exceptions.AccessError: Model 'my.model' not found`

**Root Cause:**
- Model in wrong module or not imported

**Solution:**
1. Check model is in correct base module (`ai_sam_base` or `ai_sam_workflows_base`)
2. Verify `__init__.py` imports the model
3. Verify `__manifest__.py` includes the module in dependencies
4. Restart Odoo, update module

---

### **Problem: Circular Dependency**

**Symptoms:**
- Module fails to load due to circular dependency

**Root Cause:**
- Base module depends on skin module (violates architecture)

**Solution:**
1. Check dependency chain: Base → Skin (not Skin → Base)
2. Move offending code to correct layer
3. Exception: `ai_sam_workflows` → `ai_sam` is allowed (supplier hub pattern)

---

### **Problem: Duplicate Assets**

**Symptoms:**
- Same icon exists in multiple modules
- Sync issues when updating icons

**Root Cause:**
- Violation of single source of truth

**Solution:**
1. Keep ONE copy in `ai_sam/static/src/vendor_library/`
2. Delete duplicates in other modules
3. Update code to use database-provided URLs

---

## 📋 Quick Reference Checklist

### **Before Adding Code, Ask:**

- [ ] **Is this a data model?** → Base module (`ai_sam_base` or `ai_sam_workflows_base`)
- [ ] **Is this a view?** → Skin module (`ai_sam` or `ai_sam_workflows`)
- [ ] **Is this a supplier asset?** → `ai_sam/static/src/vendor_library/`
- [ ] **Is this a controller?** → Skin module (feature-specific)
- [ ] **Is this frontend JS?** → Skin module (feature-specific)
- [ ] **Am I duplicating assets?** → NO! Use single source of truth
- [ ] **Am I hardcoding paths?** → NO! Use database-provided URLs
- [ ] **Am I violating layer dependencies?** → Check dependency graph

---

## 🎯 Summary

### **Core Principles**
1. ✅ **Preserve Intelligence:** Data in base modules (stable)
2. ✅ **Allow Evolution:** UI in skin modules (can break/rebuild)
3. ✅ **Centralize Knowledge:** Supplier assets in ai_sam (single source)
4. ✅ **Clear Ownership:** Every file has an obvious home
5. ✅ **Single Source of Truth:** No duplication, use database URLs

### **Module Roles**
- **ai_sam_base:** Core SAM data models
- **ai_sam:** Supplier Knowledge Hub + Core SAM UI
- **ai_sam_workflows_base:** Workflow data models
- **ai_sam_workflows:** Workflow Execution Engine + UI

### **Dependency Pattern**
```
ai_sam_base ← ai_sam
                ↑
ai_sam_workflows_base ← ai_sam_workflows
```

### **Golden Rule**
> "If you're not sure where to put code, ask: Is it DATA (base) or PRESENTATION (skin)? Is it CORE SAM or WORKFLOW? Is it SUPPLIER-SPECIFIC (ai_sam)?"

---

**Document Version:** 1.0
**Last Updated:** 2025-12-06
**Maintained By:** SAM AI Architecture Team
**Status:** ✅ Official Reference
