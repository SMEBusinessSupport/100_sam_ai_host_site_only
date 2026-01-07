# SAM AI Platform Skin Architecture Model
**Date:** 2025-10-11
**Version:** 1.0
**Status:** Canonical Architecture Document

---

## 🎯 Executive Summary

SAM AI uses a **three-layer architecture** where data, framework, and UI are completely separated:

1. **ai_brain** = Pure data layer (ALL models, no views)
2. **ai_sam** = Framework + Canvas core + Controllers (business logic, no data models)
3. **Platform Skins** = UI renderers only (views, JS/CSS, specific to each platform)

**Key Principle:**
> **ONE data layer (ai_brain) + ONE framework (ai_sam) + MANY skins (platforms) = Infinite extensibility with data safety**

---

## 📚 Terminology

### **Platform Skin:**
A **Platform Skin** is a UI-only module that provides:
- ✅ Views (XML)
- ✅ Frontend code (JavaScript/CSS)
- ✅ Platform-specific renderers
- ✅ Optional: Platform-specific controllers (if needed for UI logic)
- ❌ **NO DATA MODELS** (all data lives in ai_brain)

**Examples:**
- `ai_sam_workflows` = Workflow automation skin (N8N-style UI)
- `ai_sam_memory` = Knowledge graph visualization skin
- `ai_sam_creatives` = Multimedia canvas skin

**Debug Isolation:**
> "Debug UI issues 1 platform at a time" - Each skin is independent, uninstalling won't affect data

---

## 🏗️ Three-Layer Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│  LAYER 3: PLATFORM SKINS (UI Layer)                             │
│  Purpose: Provide specialized UI/UX for different use cases     │
│                                                                  │
│  ┌──────────────────┐  ┌──────────────────┐  ┌───────────────┐ │
│  │ ai_sam_workflows │  │  ai_sam_memory   │  │ai_sam_creatives│ │
│  │ (N8N Workflows)  │  │ (Knowledge Graph)│  │  (Multimedia) │ │
│  ├──────────────────┤  ├──────────────────┤  ├───────────────┤ │
│  │ ✅ Views (XML)   │  │ ✅ Views (XML)   │  │ ✅ Views (XML)│ │
│  │ ✅ JS Renderer   │  │ ✅ JS Renderer   │  │ ✅ JS Renderer│ │
│  │ ✅ CSS Styles    │  │ ✅ CSS Styles    │  │ ✅ CSS Styles │ │
│  │ ✅ Controllers*  │  │ ✅ Controllers*  │  │ ✅ Controllers*│ │
│  │ ❌ NO MODELS     │  │ ❌ NO MODELS     │  │ ❌ NO MODELS  │ │
│  └──────────────────┘  └──────────────────┘  └───────────────┘ │
│  *Controllers only if platform-specific UI logic required       │
└─────────────────────────────────────────────────────────────────┘
                            ↓ depends on
┌─────────────────────────────────────────────────────────────────┐
│  LAYER 2: AI_SAM (Framework Layer)                              │
│  Purpose: Provide canvas core, services, and universal logic    │
│                                                                  │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │  Canvas Skeleton Core:                                     │ │
│  │  ├── canvas_sizer.js (universal sizing)                   │ │
│  │  ├── canvas_engine.js (pan/zoom/grid)                     │ │
│  │  ├── node_manager.js (CRUD operations)                    │ │
│  │  └── platform_loader.js (dynamic skin injection)          │ │
│  │                                                            │ │
│  │  Services:                                                 │ │
│  │  ├── ai_service.py (Claude API integration)               │ │
│  │  ├── ai_context_builder.py (all-knowing context)          │ │
│  │  ├── ai_voice_service.py (Whisper integration)            │ │
│  │  └── ai_registry_watcher.py (module monitor)              │ │
│  │                                                            │ │
│  │  Universal Controllers (query engines):                   │ │
│  │  ├── canvas_controller.py (canvas API)                    │ │
│  │  ├── sam_ai_chat_controller.py (chat endpoints)           │ │
│  │  ├── sam_session_controller.py (session management)       │ │
│  │  └── [Future: query engine controllers]                   │ │
│  │                                                            │ │
│  │  Site-Wide UI:                                            │ │
│  │  ├── sam_ai_chat_widget.js (global chat)                 │ │
│  │  └── sam_ai_token_counter.js (cost tracking)             │ │
│  │                                                            │ │
│  │  ❌ NO DATA MODELS (framework code only)                  │ │
│  └───────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                            ↓ depends on
┌─────────────────────────────────────────────────────────────────┐
│  LAYER 1: AI_BRAIN (Data Layer)                                 │
│  Purpose: Persistent data storage - ALL models live here        │
│                                                                  │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │  📊 ALL DATA MODELS - PROTECTED AND PERSISTENT             │ │
│  │                                                            │ │
│  │  Core SAM AI Data:                                         │ │
│  │  ├── ai.service.config (API configuration)                │ │
│  │  ├── ai.conversation (chat threads)                       │ │
│  │  ├── ai.message (messages)                                │ │
│  │  ├── ai.token.usage (usage tracking)                      │ │
│  │  ├── sam.user.profile (user profiles)                     │ │
│  │  ├── sam.user.settings (user settings)                    │ │
│  │  ├── sam.mode.context (power prompts)                     │ │
│  │  ├── sam.chat.session (chat sessions)                     │ │
│  │  ├── canvas.platform (platform registry)                  │ │
│  │  └── ai.branch (branch meta-architecture)                 │ │
│  │                                                            │ │
│  │  Workflow Data (for ai_sam_workflows skin):               │ │
│  │  ├── canvas (workflow definitions)                        │ │
│  │  ├── executions (execution history - audit trail)         │ │
│  │  ├── nodes (node instances)                               │ │
│  │  ├── connections (node connections)                       │ │
│  │  ├── business.unit (business units)                       │ │
│  │  ├── api.credentials (API keys - sensitive)               │ │
│  │  └── workflow.template (workflow templates)               │ │
│  │                                                            │ │
│  │  Memory Data (for ai_sam_memory skin):                    │ │
│  │  ├── ai.memory.config (memory system config)              │ │
│  │  ├── ai.conversation.import (imported conversations)      │ │
│  │  ├── ai.document.extractor (document extraction)          │ │
│  │  ├── ai.extractor.plugin (learned extraction patterns)    │ │
│  │  └── ai.graph.service (graph DB interface)                │ │
│  │                                                            │ │
│  │  Creatives Data (for ai_sam_creatives skin):              │ │
│  │  ├── creatives.project (creative projects)                │ │
│  │  ├── creatives.asset (multimedia assets)                  │ │
│  │  └── creatives.landing.card (landing cards)               │ │
│  │                                                            │ │
│  │  ❌ NO VIEWS, NO CONTROLLERS (pure data)                  │ │
│  └───────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📋 What Goes Where

### **ai_brain (Data Layer)**

**Principle:** If losing it would make a customer angry, it belongs here.

**Contains:**
- ✅ **ALL data models** (ir.model records)
- ✅ **User data** (workflows, projects, conversations)
- ✅ **Audit trails** (executions, token usage)
- ✅ **Sensitive data** (API credentials, user profiles)
- ✅ **Configuration data** (settings, templates)

**Does NOT contain:**
- ❌ Views (no XML files)
- ❌ Controllers (no HTTP endpoints)
- ❌ Frontend code (no JS/CSS)

**Example Models:**
```python
# ai_brain/models/__init__.py

# Core SAM AI models
from . import ai_service_config
from . import ai_conversation
from . import ai_message
from . import sam_user_profile

# Workflow data (used by ai_sam_workflows skin)
from . import canvas              # Workflow definitions
from . import executions          # Execution history
from . import nodes               # Node instances
from . import connections         # Node connections
from . import api_credentials     # API keys

# Memory data (used by ai_sam_memory skin)
from . import ai_memory_config
from . import ai_conversation_import

# Creatives data (used by ai_sam_creatives skin)
from . import creatives_project
from . import creatives_asset
```

**Uninstall Safety:**
- ❌ Cannot uninstall ai_brain (base dependency)
- ✅ Data protected forever

---

### **ai_sam (Framework Layer)**

**Principle:** Universal infrastructure that ALL platforms need.

**Contains:**
- ✅ **Canvas Skeleton Core** (universal canvas engine)
- ✅ **Platform Loader** (dynamic skin injection)
- ✅ **Universal Services** (Claude API, context builder)
- ✅ **Universal Controllers** (query engines, chat API)
- ✅ **Site-wide UI** (chat widget, token counter)

**Does NOT contain:**
- ❌ Data models (belongs in ai_brain)
- ❌ Platform-specific UI (belongs in skins)

**Structure:**
```
ai_sam/
├── models/                     ← ❌ SHOULD BE EMPTY (no data models)
├── controllers/                ← ✅ Universal controllers
│   ├── canvas_controller.py        (canvas API - query engine)
│   ├── sam_ai_chat_controller.py   (chat endpoints)
│   ├── sam_session_controller.py   (session management)
│   └── [future query controllers]
├── static/src/
│   ├── core/                   ← ✅ Canvas skeleton core
│   │   ├── canvas_sizer.js
│   │   ├── canvas_engine.js
│   │   ├── node_manager.js
│   │   └── platform_loader.js
│   ├── js/                     ← ✅ Universal UI components
│   │   ├── sam_ai_chat_widget.js
│   │   └── sam_ai_token_counter.js
│   └── css/                    ← ✅ Universal styles
└── views/                      ← ✅ Universal views (menu structure, canvas container)
```

**Controllers in ai_sam (Query Engines):**

Controllers in ai_sam are **universal query engines** that work across all platforms:

```python
# ai_sam/controllers/canvas_controller.py
class CanvasController(http.Controller):
    """
    Universal canvas API - works for ALL platforms
    Queries ai_brain models, returns data to any skin
    """

    @http.route('/sam/canvas/list', type='json', auth='user')
    def list_canvases(self, platform=None):
        # Query ai_brain.canvas model
        # Can filter by platform (workflows, memory, creatives)
        Canvas = request.env['canvas']
        return Canvas.search_read([...])

    @http.route('/sam/canvas/save', type='json', auth='user')
    def save_canvas(self, canvas_id, data):
        # Save to ai_brain.canvas model
        # Works regardless of which skin is using it
        Canvas = request.env['canvas']
        canvas = Canvas.browse(canvas_id)
        canvas.write(data)
        return {'success': True}
```

**Future Query Engines in ai_sam:**
```python
# ai_sam/controllers/sam_query_controller.py
class SamQueryController(http.Controller):
    """
    Universal query engine for web forms, mobile apps, etc.
    Queries ai_brain data regardless of frontend
    """

    @http.route('/sam/query/workflows', type='json', auth='user')
    def query_workflows(self, filters):
        # Query workflow data from ai_brain
        pass

    @http.route('/sam/query/conversations', type='json', auth='user')
    def query_conversations(self, filters):
        # Query conversation data from ai_brain
        pass
```

**Key Insight (Hybrid Approach - Option C):**
> **If 2+ platforms will use it → ai_sam (universal controller)**
> **If only 1 platform uses it → That platform's controller (direct to ai_brain)**
>
> This avoids unnecessary abstraction while preventing code duplication. Platform controllers CAN access ai_brain directly when needed.

---

### **Platform Skins (UI Layer)**

**Principle:** UI-only modules that provide specialized experiences for specific use cases.

**Contains:**
- ✅ **Views (XML)** - Platform-specific forms, kanban, tree views
- ✅ **JavaScript Renderers** - Platform-specific canvas rendering
- ✅ **CSS Styles** - Platform-specific styling
- ✅ **Platform-Specific Controllers** (optional, only if needed for UI logic)
- ✅ **Seed Data (XML)** - Platform registration, demo data (reinstallable)

**Does NOT contain:**
- ❌ Data models (belongs in ai_brain)
- ❌ Universal controllers (belongs in ai_sam)

**Structure:**
```
ai_sam_workflows/              ← Platform Skin (example)
├── models/                    ← ❌ SHOULD BE EMPTY or minimal extensions
├── controllers/               ← ✅ Platform-specific controllers (if needed)
│   └── workflow_import_controller.py  (workflow-specific UI logic)
├── views/                     ← ✅ Platform-specific views
│   ├── workflow_definition_views.xml
│   ├── workflow_execution_views.xml
│   └── workflow_menus.xml
├── static/src/
│   └── workflows/             ← ✅ Platform-specific renderer
│       ├── workflow_renderer.js   (N8N-style node rendering)
│       ├── workflow_toolbar.js    (workflow-specific tools)
│       └── workflow_styles.css
├── data/                      ← ✅ Seed data (reinstallable)
│   ├── workflow_platform.xml      (platform registration)
│   └── workflow_templates.xml     (demo templates)
└── security/                  ← ✅ UI-specific security rules
    └── ir.model.access.csv        (view access only)
```

**Platform-Specific Controllers:**

**Question:** Do platform skins have their own controllers?
**Answer:** YES, but ONLY for platform-specific UI logic.

**Rule:**
- ✅ **Universal query engines** → ai_sam (work across all platforms)
- ✅ **Platform-specific UI logic** → Platform skin (only needed for that skin)

**Example:**
```python
# ai_sam_workflows/controllers/workflow_import_controller.py
class WorkflowImportController(http.Controller):
    """
    Workflow-specific controller for N8N JSON import
    This is UI logic specific to the workflows skin
    """

    @http.route('/workflows/import/n8n', type='http', auth='user')
    def import_n8n_json(self, file):
        # Parse N8N JSON (specific to workflows platform)
        # Create canvas, nodes, connections in ai_brain
        # Return workflow ID
        pass

    @http.route('/workflows/export/n8n', type='http', auth='user')
    def export_n8n_json(self, workflow_id):
        # Read from ai_brain.canvas
        # Convert to N8N JSON format (specific to workflows platform)
        # Return JSON file
        pass
```

**Another Example:**
```python
# ai_sam_memory/controllers/memory_import_controller.py
class MemoryImportController(http.Controller):
    """
    Memory-specific controller for Claude conversation import
    This is UI logic specific to the memory skin
    """

    @http.route('/memory/import/claude', type='http', auth='user')
    def import_claude_conversations(self, project_id):
        # Fetch from Claude API (specific to memory platform)
        # Extract conversations and store in ai_brain
        pass
```

**Key Principle (Hybrid Approach):**
> **Universal operations (used by 2+ platforms)** → ai_sam controller
> **Platform-specific operations (used by 1 platform)** → Platform skin controller (direct to ai_brain)
>
> **Benefits:**
> - ✅ No unnecessary abstraction layers
> - ✅ No code duplication (DRY principle)
> - ✅ Platform controllers can access ai_brain directly
> - ✅ Shared logic centralized where it adds value

---

## 🎯 Benefits of Platform Skin Architecture

### **1. Data Safety:**
✅ Uninstall any platform skin → Data remains safe in ai_brain
✅ Reinstall platform skin → Data is still there
✅ Compliance-friendly (audit trails protected)

### **2. Debug Isolation:**
✅ "Debug UI issues 1 platform at a time"
✅ Workflows broken? Uninstall ai_sam_workflows, debug, reinstall
✅ Other platforms unaffected
✅ Data untouched

### **3. Flexible Frontend Development:**
✅ Build web forms that query ai_brain directly (no ai_sam needed)
✅ Build mobile app that hits ai_sam controllers
✅ Build external dashboard that visualizes ai_brain data
✅ Replace entire platform skin without losing data

### **4. Clean Separation:**
✅ Frontend developers work on skins (no database risk)
✅ Backend developers work on ai_brain (no UI complexity)
✅ Framework developers work on ai_sam (universal infrastructure)

---

## 📊 Module Dependencies

```
ai_sam_workflows  ─┐
ai_sam_memory     ─┤
ai_sam_creatives  ─┼──→  ai_sam  ──→  ai_brain  ──→  base (Odoo core)
[future skins]    ─┘

Dependency Direction:
Skins depend on ai_sam
ai_sam depends on ai_brain
ai_brain depends on base

Data Flow:
Skins (UI) → ai_sam (controllers/query engines) → ai_brain (data)
```

**Installation Order:**
1. `base` (Odoo core)
2. `ai_brain` (data layer)
3. `ai_sam` (framework)
4. Platform skins (optional, any order)

**Uninstallation:**
- ✅ Can uninstall any skin (data safe)
- ✅ Can uninstall ai_sam (if no skins installed)
- ❌ Cannot uninstall ai_brain (base dependency, data layer)

---

## 🔄 Uninstall Strategy

### **Platform Skin Uninstall:**
```python
# ai_sam_workflows/models/workflow_uninstall_wizard.py
class WorkflowUninstallWizard(models.TransientModel):
    _name = 'workflow.uninstall.wizard'

    def check_data_exists(self):
        # Check if workflows exist in ai_brain
        Canvas = self.env['canvas']
        workflow_count = Canvas.search_count([('canvas_type', '=', 'workflow')])

        if workflow_count > 0:
            # Warn user
            return {
                'type': 'ir.actions.act_window',
                'name': 'Workflows Exist',
                'res_model': 'workflow.uninstall.wizard',
                'view_mode': 'form',
                'target': 'new',
            }

    def export_and_uninstall(self):
        # Export workflow data (CSV/JSON)
        # User downloads backup
        # Then allow uninstall
        # Data remains in ai_brain (still accessible if reinstalled)
        pass
```

**Workflow:**
1. User clicks "Uninstall ai_sam_workflows"
2. Wizard checks ai_brain for workflow data
3. If data exists → Offer export option
4. User downloads backup (optional)
5. Uninstall proceeds
6. **Data remains in ai_brain** (not deleted)
7. If user reinstalls → Data is still there!

---

## 🚀 Future: Query Engines and Web Forms

Your vision:
> "Now I could start to build our next step around ai_brain and initiate a simple web form and various query engines"

### **Architecture Enables This:**

```
┌──────────────────────────────────────────────────┐
│  MULTIPLE FRONTENDS (all query same data)       │
│                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌────────┐ │
│  │ Platform     │  │ Web Forms    │  │ Mobile │ │
│  │ Skins        │  │ (Simple UI)  │  │ App    │ │
│  └──────────────┘  └──────────────┘  └────────┘ │
└─────────────┬────────────┬────────────┬──────────┘
              │            │            │
              ↓            ↓            ↓
    ┌─────────────────────────────────────────┐
    │  ai_sam (Query Engines/Controllers)     │
    │  ┌───────────────────────────────────┐  │
    │  │ canvas_controller.py              │  │
    │  │ query_controller.py               │  │
    │  │ workflow_query_controller.py      │  │
    │  │ conversation_query_controller.py  │  │
    │  │ [future controllers]              │  │
    │  └───────────────────────────────────┘  │
    └──────────────────┬──────────────────────┘
                       ↓
              ┌────────────────────┐
              │  ai_brain (Data)   │
              │  ┌──────────────┐  │
              │  │ ALL MODELS   │  │
              │  └──────────────┘  │
              └────────────────────┘
```

**Example: Simple Web Form (No Platform Skin Needed)**
```xml
<!-- simple_web_module/views/simple_form.xml -->
<form string="Query Workflows">
    <field name="date_from"/>
    <field name="date_to"/>
    <button name="query_workflows" string="Search" type="object"/>
</form>
```

```python
# simple_web_module/models/simple_query.py
class SimpleQuery(models.TransientModel):
    _name = 'simple.query'

    date_from = fields.Date()
    date_to = fields.Date()

    def query_workflows(self):
        # Query ai_brain directly!
        Canvas = self.env['canvas']
        workflows = Canvas.search([
            ('create_date', '>=', self.date_from),
            ('create_date', '<=', self.date_to),
        ])

        # Return data (no complex UI needed)
        return {
            'type': 'ir.actions.act_window',
            'name': 'Results',
            'res_model': 'canvas',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', workflows.ids)],
        }
```

**Key Point:**
> Because ALL data is in ai_brain, you can query it from ANYWHERE (platform skins, web forms, mobile apps, external APIs)

---

## 📝 Summary

### **Golden Rules:**

1. **Data Layer (ai_brain):**
   - ALL data models
   - No views, no controllers
   - Protected, persistent, queryable

2. **Framework Layer (ai_sam):**
   - Canvas skeleton core
   - Universal services
   - Universal controllers (query engines)
   - No data models

3. **UI Layer (Platform Skins):**
   - Views (XML)
   - Renderers (JS/CSS)
   - Platform-specific controllers (UI logic only)
   - No data models

4. **Controllers (Hybrid Approach - Option C):**
   - Universal operations (2+ platforms) → ai_sam
   - Platform-specific operations (1 platform) → Platform skin (direct to ai_brain)
   - Optimize for simplicity, not abstraction

### **Test:**
> If losing it would make a customer angry → ai_brain
> If it's UI-specific and safe to remove → Platform skin
> If it's universal infrastructure → ai_sam

---

## 📖 Lessons Learned: Workflows Platform Correction (2025-10-12)

### **The Mistake:**
During Phase 3 extraction (2025-10-11), we initially moved workflow data models to ai_sam_workflows.

**What happened:**
- Moved 20 data models from ai_brain to ai_sam_workflows
- Treated ai_sam_workflows as standalone module instead of Platform Skin
- Followed incorrect pattern from initial extraction

**Impact:**
- ❌ Uninstalling ai_sam_workflows would delete user workflow data
- ❌ Violated data safety principles
- ❌ Broke compliance/audit trail requirements (HIPAA, GDPR, SOX)
- ❌ Contradicted original ai_brain design intent (pure data layer)
- ❌ Broke "debug UI issues 1 platform at a time" strategy
- ❌ Created data loss risk on module uninstall

### **The Fix:**
Moved all 20 workflow data models back to ai_brain (2025-10-12).

**Actions Taken:**
1. Archived current state (safety first)
2. Moved all 20 model files back to ai_brain/models/
3. Updated ai_brain/models/__init__.py with imports
4. Cleared ai_sam_workflows/models/__init__.py (UI-only)
5. Updated security rules (already in ai_brain)
6. Updated both module manifests with Platform Skin documentation
7. Created comprehensive correction summary

**Result:**
- ✅ Data survives module uninstalls
- ✅ Audit trails protected
- ✅ Platform Skin Model correctly implemented
- ✅ "Debug UI issues 1 platform at a time" strategy enabled
- ✅ Compliance requirements met
- ✅ Uninstall wizard strategy now viable

### **Key Insights:**

**The Golden Rule:**
> **"If losing it would make a customer angry, it belongs in ai_brain"** - This rule is non-negotiable.

**Data vs UI Test:**
- Would losing this on uninstall anger customers? → ai_brain
- Is this just a UI preference? → Platform skin
- Is this execution history or audit data? → ai_brain (always!)

**Real-World Scenario:**
```
User: "I want to uninstall the workflows UI to debug issues"
Developer: "Sure, uninstalling ai_sam_workflows..."
User: "Wait, what happened to all my workflows?!"
Developer: "Oh no... they're gone..." ❌ BAD!

CORRECT:
User: "I want to uninstall the workflows UI to debug issues"
Developer: "Sure, uninstalling ai_sam_workflows..."
User: "Great! When I reinstall, will my workflows still be there?"
Developer: "Absolutely! All data is safe in ai_brain" ✅ GOOD!
```

**Compliance Perspective:**
- HIPAA: Audit trails must be immutable and persistent
- GDPR: Data retention policies must be enforced
- SOX: Financial transaction history cannot be deleted
- Platform skins are UI preferences, not data stores

### **Apply to Other Modules:**

**ai_sam_memory:**
- Check if memory data models are in ai_brain ✓ (already correct)
- Ensure ai_sam_memory contains only UI components

**ai_sam_creatives:**
- Check if creatives data models are in ai_brain ✓ (already correct)
- Ensure ai_sam_creatives contains only UI components

**Future Platform Skins:**
- NEVER put data models in platform modules
- ALWAYS put data models in ai_brain
- Platform skins = Views + JS/CSS + Platform-specific controllers only

---

**Status:** ✅ Architecture Defined & Validated
**Correction:** ✅ Applied (2025-10-12)
**Next:** User testing of corrected architecture
