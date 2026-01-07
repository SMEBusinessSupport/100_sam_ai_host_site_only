AI SAM BASE MODULE - CHAT OWNERSHIP
====================================

Module: ai_sam (base)
Created: 2025-11-04
Purpose: Define what chat components THIS MODULE owns and provides

Related Documentation:
    - SAM_CHAT_ARCHITECTURE.txt (master architecture - in this folder)

---

MODULE IDENTITY
===============

Module Name: ai_sam
Type: Base/Platform Module
Chat Ownership: LAYER 1 - Platform Chat (site-wide)
Dependencies: None (this is the base)
Provides To: ALL other modules (ai_sam_workflows, ai_sam_email, etc.)

---

WHAT THIS MODULE OWNS
======================

Layer 1: Platform Chat
-----------------------

1.1 SYSTRAY CHAT
    Purpose: Traditional Odoo messaging integration
    Location: Odoo systray (top bar)
    Files:
        - views/sam_chat_vanilla_v2_action.xml
        - static/src/js/sam_chat_systray.js (if exists)

1.2 SAM BUBBLE CHAT (Location-Aware Teacher)
    Purpose: Universal AI assistant that adapts to user's location
    Location: Site-wide (follows user across all Odoo pages)
    Behavior: Location-aware expertise (CRM expert, Accounting expert, etc.)

    Files:
        - static/src/chat_ui/sam_chat_bubble.js ← CORE COMPONENT
        - static/src/chat_ui/SAM_CHAT_BUBBLE_USAGE.md
        - static/src/chat_ui/CHAT_UI_STYLES_DESIGN.md

---

FILE INVENTORY
==============

Chat-Related Files in ai_sam Module:
-------------------------------------

views/
    sam_chat_vanilla_v2_action.xml              ← Chat action definition

static/src/chat_ui/
    sam_chat_bubble.js                          ← Universal bubble (location-aware routing)
    SAM_CHAT_BUBBLE_USAGE.md                    ← Usage documentation
    CHAT_UI_STYLES_DESIGN.md                    ← UI design patterns
    [other platform chat files]

static/src/js/
    [general Odoo integration files]

---

__MANIFEST__.PY CONFIGURATION
==============================

Chat Assets That SHOULD Be in ai_sam/__manifest__.py:
------------------------------------------------------

'web.assets_backend': [
    # Layer 1: Platform Chat
    'ai_sam/views/sam_chat_vanilla_v2_action.xml',
    'ai_sam/static/src/chat_ui/sam_chat_bubble.js',
    'ai_sam/static/src/chat_ui/[other chat UI files]',

    # DO NOT include workflow chat here (that's in ai_sam_workflows)
    # DO NOT include design system CSS here (that's in ai_sam_workflows)
],

Critical Rules:
    ✓ Include all platform chat files (Layer 1)
    ✗ Do NOT include workflow sidebar chat (Layer 2 - different module)
    ✗ Do NOT include canvas design system (belongs in ai_sam_workflows)

---

WHAT THIS MODULE PROVIDES
==========================

To Other Modules:
-----------------

1. SAMChatBubble Class
    - Exported JavaScript class
    - Used by ALL modules for consistent chat entry point
    - Handles location detection and routing

2. Location-Aware Routing
    - Detects current Odoo page/module
    - Routes to appropriate chat UI:
        * Standard chat (most locations)
        * Workflow sidebar (when on canvas) → Routes to ai_sam_workflows Layer 2
        * Email agent (when on email) → Routes to ai_sam_email Layer 4
        * Website agent (when on website) → Routes to ai_sam_website Layer 4

3. Expert Prompt System
    - Location-based prompt engineering
    - Makes SAM appear as domain expert:
        * CRM page → "CRM Expert Sam"
        * Accounting → "Accounting Expert Sam"
        * Inventory → "Inventory Expert Sam"

Usage Example (Other Modules):
-------------------------------
// In ai_sam_workflows or any other module:
const bubble = SAMChatBubble.create({
    location: 'canvas',
    context: { workflow_id: 455 },
    onClick: (data) => {
        // Layer 1 handles routing to Layer 2 UI
    }
});

---

WHAT THIS MODULE CONSUMES
==========================

From Other Modules:
-------------------

NONE - This is the base module. All other modules depend on THIS module.

---

DEPENDENCIES
============

Odoo Core Dependencies:
    - web (standard Odoo web module)
    - base (standard Odoo base)

SAM Module Dependencies:
    - NONE (this is the foundation)

Other Modules That Depend On This:
    - ai_sam_workflows (requires Layer 1 bubble for routing)
    - ai_sam_email (future - will use bubble routing)
    - ai_sam_website (future - will use bubble routing)
    - [all future SAM modules]

Installation Order:
    1. ai_sam ← Install FIRST (base)
    2. ai_sam_workflows (depends on ai_sam)
    3. [specialized agents depend on ai_sam]

---

CHAT BOUNDARIES
===============

What Belongs in ai_sam (This Module):
--------------------------------------
    ✓ Platform-wide chat bubble (SAMChatBubble class)
    ✓ Systray chat integration
    ✓ Location detection logic
    ✓ Routing logic (to other layers/modules)
    ✓ Expert prompt system
    ✓ Site-wide chat UI components

What Does NOT Belong Here:
---------------------------
    ✗ Workflow sidebar chat (that's ai_sam_workflows Layer 2)
    ✗ Canvas chat node (that's ai_sam_workflows Layer 3)
    ✗ Email agent UI (that's ai_sam_email Layer 4)
    ✗ Website agent UI (that's ai_sam_website Layer 4)
    ✗ Canvas design system (node shapes, dimensions - that's ai_sam_workflows)

---

COMMON MISTAKES TO AVOID
=========================

Mistake 1: "Let's add workflow chat to ai_sam"
-----------------------------------------------
NO! Workflow chat (sidebar) belongs in ai_sam_workflows.
ai_sam only provides the BUBBLE that routes to workflow chat.

Mistake 2: "Design system CSS should be in ai_sam"
---------------------------------------------------
NO! Design system is for canvas/nodes (ai_sam_workflows).
Chat UI has its own styling (separate concern).

Mistake 3: "Move all chat files to ai_sam for simplicity"
----------------------------------------------------------
NO! Each layer has architectural reason for its location.
Don't break module boundaries for "simplicity."

Mistake 4: "Workflow chat depends on ai_sam, so merge them"
------------------------------------------------------------
NO! Dependencies are correct. Workflows extends base functionality.
Keep modules separate for clean architecture.

---

CURRENT STATUS (2025-11-04)
===========================

Migration Status:
-----------------
    During nuclear restructure, SAMChatBubble was incorrectly moved to ai_sam_workflows.

    WRONG LOCATION:
        ai_sam_workflows/static/src/chat_ui/sam_chat_bubble.js ✗

    CORRECT LOCATION:
        ai_sam/static/src/chat_ui/sam_chat_bubble.js ✓

    Action Required:
        1. Move chat_ui/ folder from ai_sam_workflows → ai_sam
        2. Keep sam_workflow_chat.js in ai_sam_workflows (Layer 2)
        3. Update __manifest__.py in both modules

Files to Move TO ai_sam:
    FROM: ai_sam_workflows/static/src/chat_ui/
    TO:   ai_sam/static/src/chat_ui/

    Files:
        - sam_chat_bubble.js ← CRITICAL (platform component)
        - SAM_CHAT_BUBBLE_USAGE.md
        - CHAT_UI_STYLES_DESIGN.md

Files to KEEP in ai_sam_workflows:
    - sam_workflow_chat.js (Layer 2 - workflow sidebar)

---

TESTING CHECKLIST
=================

When Testing ai_sam Module Chat:
---------------------------------

Layer 1 - Platform Chat:
    [ ] SAM Bubble appears on ALL Odoo pages
    [ ] Bubble detects location correctly (CRM, Accounting, Canvas, etc.)
    [ ] Expert prompts load based on location:
        [ ] CRM page → CRM expert prompt
        [ ] Accounting → Accounting expert prompt
        [ ] Inventory → Inventory expert prompt
    [ ] Routing to other layers works:
        [ ] On canvas → Routes to ai_sam_workflows sidebar (Layer 2)
        [ ] On email → Routes to email agent (Layer 4, if installed)
    [ ] Systray chat accessible from top bar
    [ ] No errors in browser console
    [ ] Works with ai_sam_workflows NOT installed (graceful fallback)

---

VERSION HISTORY
===============

2025-11-04: Initial document created
            - Defined ai_sam module chat ownership
            - Documented Layer 1 components
            - Identified files to move back from ai_sam_workflows
            - Established module boundaries

---

END OF DOCUMENT

For master architecture overview, see: SAM_CHAT_ARCHITECTURE.txt (in this folder)
For workflows module chat, see: ai_sam_workflows/documentation/ai_sam_workflows_chats.txt
