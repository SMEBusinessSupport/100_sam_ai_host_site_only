SAM AI CHAT ARCHITECTURE - 4-LAYER SYSTEM
==========================================

Created: 2025-11-04
Purpose: Define the CORRECT architecture for all chat systems in SAM AI
Status: AUTHORITATIVE - This is the source of truth for all future development

CRITICAL: Read this document BEFORE touching any chat-related code!

---

OVERVIEW
========

SAM AI has FOUR distinct chat layers, each with specific purpose, location, and ownership.
DO NOT confuse these layers - they serve different purposes and live in different modules.

---

LAYER 1: PLATFORM CHAT (ai_sam base module)
============================================

Module Owner: ai_sam (base module)
Purpose: Platform-wide AI assistance, location-aware expertise
Visibility: Site-wide (available everywhere in Odoo)

Components:
-----------

1.1 SYSTRAY CHAT
    UI: Traditional Odoo messaging integration
    Location: Odoo systray (top bar)
    Purpose: Standard Odoo messaging pattern
    Styling: Odoo-aligned UI
    Files:
        - ai_sam/views/sam_chat_vanilla_v2_action.xml
        - ai_sam/static/src/js/[systray chat files]

1.2 SAM BUBBLE CHAT (Location-Aware "Teacher Sam")
    UI: Floating bubble that follows user
    Location: Any page in Odoo system
    Purpose: Context-aware AI teacher/expert
    Behavior: Changes expertise based on CURRENT LOCATION

    Location-Based Personas:
        At CRM page → "Odoo CRM Superstar" (CRM expert prompts)
        At Accounting → "Accounting Expert" (accounting context)
        At Inventory → "Inventory Specialist" (inventory context)
        At Sales → "Sales Expert" (sales process knowledge)
        At Canvas → "Workflow Expert" (triggers Layer 2 UI!)
        At Settings → "Configuration Expert" (system setup help)
        [Any Odoo app] → Specialized expert for that domain

    Key Concept: SAME BUBBLE, DIFFERENT PERSONA/KNOWLEDGE PER LOCATION

    Routing Logic:
        - Detects current page/module
        - Loads appropriate expert prompt
        - Opens appropriate UI (standard chat OR Layer 2/4)

    Files:
        - ai_sam/static/src/chat_ui/sam_chat_bubble.js ← MUST BE IN ai_sam!
        - ai_sam/static/src/chat_ui/SAM_CHAT_BUBBLE_USAGE.md
        - ai_sam/static/src/chat_ui/CHAT_UI_STYLES_DESIGN.md

Critical Rule: SAMChatBubble class MUST live in ai_sam (platform-level component)

---

LAYER 2: WORKFLOW SIDEBAR CHAT (ai_sam_workflows module)
=========================================================

Module Owner: ai_sam_workflows
Purpose: Deep workflow building assistance
Visibility: ONLY on workflow canvas page
Trigger: SAM Bubble clicked while on canvas (Layer 1 routes to Layer 2)

UI Characteristics:
    Position: Slides in from RIGHT side of screen
    Size: 30% of screen width (minimum 400px)
    Height: Full screen height
    Behavior: Persistent state when collapsed
    Integration: Theatre mode aware

Features:
    - Conversation history
    - Quick actions (node suggestions, etc.)
    - Canvas context awareness (workflow_id, nodes, connections)
    - Theatre mode integration
    - Persistent state

User Journey:
    1. User is on workflow canvas
    2. Clicks SAM Bubble (Layer 1 component)
    3. Layer 1 detects location = 'canvas'
    4. Layer 1 routes to Layer 2 UI
    5. Sidebar slides in from right
    6. Chat has full workflow context

Files:
    - ai_sam_workflows/static/src/workflow/sam_workflow_chat.js
    - ai_sam_workflows/static/src/workflow/[workflow chat UI files]

Critical Rule: This is NOT a separate chat system - it's the UI that Layer 1 routes to when on canvas!

---

LAYER 3: WORKFLOW NODE CHAT (ai_sam_workflows module)
======================================================

Module Owner: ai_sam_workflows
Purpose: Information aggregation node within workflow execution
Visibility: On canvas as draggable node
Type: Canvas node component (like HttpRequest node, but for chat)

UI Characteristics:
    Appearance: Standard canvas node (96x96px, follows node styling)
    Shape: Likely square or custom chat icon shape
    Behavior: Draggable, connectable to other nodes
    Data Flow: Can receive input from nodes, send output to nodes

Features:
    - Conversation history tied to THIS SPECIFIC NODE
    - Information aggregation (multiple inputs → one chat context)
    - Part of workflow execution (not just UI)
    - Data persistence with workflow

User Journey:
    1. User drags "Chat Node" from node picker onto canvas
    2. Node appears like any other workflow node
    3. User configures node (which info to aggregate, prompts, etc.)
    4. Node executes as part of workflow
    5. Conversation/data tied to this node instance

Files:
    - ai_sam_workflows/static/src/sam_agent_nodes/[chat node files]
    - ai_sam_workflows/models/[chat node models]

Critical Rule: This is a WORKFLOW COMPONENT, not a UI chat - it's executable!

---

LAYER 4: SPECIALIZED AGENT CHATS (future/separate modules)
===========================================================

Module Owner: Separate modules per agent (ai_sam_email, ai_sam_website, etc.)
Purpose: Domain-specific AI agents with custom UIs
Visibility: Context-specific (email marketing, website builder, etc.)
Trigger: SAM Bubble routing OR direct access from specialized app

Agents (Current/Planned):
--------------------------

4.1 EMAIL MARKETING AGENT
    Module: ai_sam_email (future)
    Purpose: Email campaign creation, list management, template design
    UI: Email-specific interface (preview pane, template editor)
    Context: Campaign data, audience segments, analytics

4.2 WEBSITE BUILDER AGENT
    Module: ai_sam_website (in progress)
    Purpose: Website page creation, layout assistance, content generation
    UI: Page builder interface (drag-drop, live preview)
    Context: Site structure, pages, content blocks

4.3 [FUTURE AGENTS]
    Module: TBD per domain
    Purpose: Specialized domains (HR, Inventory, Manufacturing, etc.)
    UI: Domain-specific interfaces
    Context: Domain data and workflows

Routing from Layer 1:
    SAM Bubble detects:
        - On email campaign page → Route to Email Agent (Layer 4)
        - On website builder → Route to Website Agent (Layer 4)
        - On [specialized app] → Route to appropriate agent

Critical Rule: Each agent is SELF-CONTAINED module with own UI, but triggered via Layer 1 bubble routing!

---

ARCHITECTURAL PATTERNS
======================

Pattern 1: Location-Aware Routing (Layer 1 → Layers 2/4)
---------------------------------------------------------
SAM Bubble (Layer 1) acts as UNIVERSAL ENTRY POINT:

    User clicks SAM Bubble
        ↓
    Layer 1 detects location via JavaScript:
        - window.location.href
        - Odoo action context
        - Menu ID
        ↓
    Layer 1 determines appropriate UI:
        - Standard chat (most locations)
        - Workflow Sidebar (canvas) → Layer 2
        - Email Agent UI (email app) → Layer 4
        - Website Agent UI (website builder) → Layer 4
        ↓
    Layer 1 routes to appropriate interface
        - Opens correct UI
        - Passes location context
        - Loads specialized prompts

Pattern 2: Specialized Expertise (Same AI, Different Prompts)
--------------------------------------------------------------
Layer 1 uses LOCATION-BASED PROMPT ENGINEERING:

    Base AI Model (same for all)
        ↓
    Location detected (e.g., "CRM Contacts page")
        ↓
    Load CRM expert prompt:
        "You are an Odoo CRM expert. User is on Contacts page.
         Available actions: create contact, import, filters, etc.
         Help with CRM-specific tasks."
        ↓
    User perceives: "CRM Expert Sam"

    Different location = Different prompt = Different expertise

    This is WHY Sam is called "Teacher" - adapts to what user is learning!

Pattern 3: Canvas Node Execution (Layer 3)
-------------------------------------------
Layer 3 is NOT just UI - it's EXECUTABLE workflow component:

    Workflow executes
        ↓
    Reaches Chat Node (Layer 3)
        ↓
    Node aggregates input data
        ↓
    Node uses AI to process/respond
        ↓
    Node outputs result to next node
        ↓
    Workflow continues

    Example Workflow:
        HTTP Request Node → Extract Data Node → Chat Node (analyze) → Send Email Node

Pattern 4: Module Independence (Layers 2-4)
--------------------------------------------
Each specialized layer is MODULE-INDEPENDENT:

    Layer 2 (Workflow Chat):
        - Can be uninstalled without breaking Layer 1
        - Layer 1 gracefully handles missing Layer 2 (fallback to standard chat)

    Layer 4 (Email Agent):
        - Separate module, separate install
        - Layer 1 detects if module installed
        - If not installed: opens standard chat with email context
        - If installed: routes to specialized Email Agent UI

---

FILE ORGANIZATION
=================

ai_sam (base module) - LAYER 1 ONLY
------------------------------------
static/src/
    chat_ui/                                      ← Platform chat components
        sam_chat_bubble.js                        ← Universal bubble (location-aware routing)
        SAM_CHAT_BUBBLE_USAGE.md                  ← Usage documentation
        CHAT_UI_STYLES_DESIGN.md                  ← UI design patterns
        sam_chat_systray.js                       ← Systray chat integration
        [other platform chat files]

    js/                                           ← General JavaScript
        [odoo integration files]

views/
    sam_chat_vanilla_v2_action.xml                ← Chat action definition
    [other chat views]


ai_sam_workflows (workflow module) - LAYERS 2 & 3
--------------------------------------------------
static/src/
    workflow/                                     ← Layer 2 files
        sam_workflow_chat.js                      ← Workflow sidebar chat UI
        [workflow chat UI files]

    sam_agent_nodes/                              ← Layer 3 files
        chat_node.js                              ← Canvas chat node
        [chat node components]

    design_system/                                ← Canvas/node styling (NOT chat)
        [canvas styles - separate from chat!]

views/
    workflow/
        [workflow-specific views]


ai_sam_email (future module) - LAYER 4
---------------------------------------
static/src/
    email_agent/
        email_agent_ui.js                         ← Email agent interface
        [email-specific files]

models/
    email_agent.py                                ← Email agent logic


ai_sam_website (in progress module) - LAYER 4
----------------------------------------------
static/src/
    website_agent/
        website_builder_ui.js                     ← Website builder interface
        [website-specific files]

models/
    website_agent.py                              ← Website agent logic

---

CRITICAL RULES FOR AI AGENTS
=============================

Rule 1: SAMChatBubble Lives in ai_sam ONLY
-------------------------------------------
The SAMChatBubble class MUST reside in ai_sam (base module).
It is a PLATFORM-LEVEL component used site-wide.

WRONG:
    ai_sam_workflows/static/src/chat_ui/sam_chat_bubble.js ✗

CORRECT:
    ai_sam/static/src/chat_ui/sam_chat_bubble.js ✓

Rule 2: Don't Confuse Layers
-----------------------------
When user says "chat", ask WHICH layer:
    - "Platform chat" (Layer 1 - SAM Bubble)
    - "Workflow chat" (Layer 2 - Sidebar)
    - "Chat node" (Layer 3 - Canvas node)
    - "Email agent chat" (Layer 4 - Specialized)

Each has DIFFERENT files, DIFFERENT purposes, DIFFERENT modules!

Rule 3: Layer 1 Routes, Doesn't Duplicate
------------------------------------------
Layer 1 (SAM Bubble) routes to other layers - it doesn't contain their UI.

WRONG: SAM Bubble has workflow sidebar UI ✗
CORRECT: SAM Bubble detects canvas → Opens Layer 2 UI ✓

Rule 4: Layer 3 Is Executable, Not Just UI
-------------------------------------------
Chat node (Layer 3) is a WORKFLOW COMPONENT that executes.
It's not just a UI element - it processes data in workflow execution.

Don't treat it as "just another chat interface" - it's part of workflow engine!

Rule 5: Specialized Agents Are Self-Contained
----------------------------------------------
Each Layer 4 agent is a SEPARATE MODULE with own UI/logic.
Layer 1 detects and routes, but doesn't contain agent code.

WRONG: Email agent UI in ai_sam module ✗
CORRECT: Email agent UI in ai_sam_email module ✓

Rule 6: Location-Aware ≠ Multiple Bubbles
------------------------------------------
There is ONE SAM Bubble (Layer 1) that adapts to location.
NOT multiple different bubbles per location.

WRONG: CRM bubble, Accounting bubble, Workflow bubble ✗
CORRECT: ONE bubble that knows context ✓

---

COMMON PITFALLS
===============

Pitfall 1: "I'll add chat to ai_sam_workflows"
-----------------------------------------------
Question: WHICH chat? Layer 2/3 is OK, Layer 1 belongs in ai_sam!

Pitfall 2: "User is on canvas, so workflow chat is Layer 1"
------------------------------------------------------------
NO! Layer 1 is the BUBBLE. Layer 2 is the SIDEBAR that opens.
Layer 1 detects canvas → routes to Layer 2.

Pitfall 3: "Design system in ai_sam because chat uses it"
----------------------------------------------------------
NO! Design system is for CANVAS/NODES (workflow), not chat UI.
Chat has its own styling (separate from node shapes/dimensions).

Pitfall 4: "Let's create chat_v3.js in ai_sam_workflows"
---------------------------------------------------------
Question: Is this Layer 2 (workflow sidebar) or Layer 1 (platform)?
Layer 1 belongs in ai_sam, Layer 2 in ai_sam_workflows!

Pitfall 5: "Move all chat files to one place for simplicity"
-------------------------------------------------------------
NO! Each layer has ARCHITECTURAL REASON for its location:
    - Layer 1: Platform-wide (ai_sam)
    - Layer 2: Workflow-specific (ai_sam_workflows)
    - Layer 3: Workflow component (ai_sam_workflows)
    - Layer 4: Domain module (ai_sam_email, etc.)

Don't "simplify" by breaking architecture!

---

TESTING CHECKLIST
=================

When testing chat functionality, verify ALL layers:

Layer 1 (Platform Chat):
    [ ] SAM Bubble appears on all Odoo pages
    [ ] Bubble detects location correctly (CRM, Accounting, etc.)
    [ ] Appropriate expert prompts load per location
    [ ] Routing to Layer 2/4 works when on canvas/specialized pages
    [ ] Systray chat accessible from top bar

Layer 2 (Workflow Sidebar):
    [ ] Sidebar opens when SAM Bubble clicked on canvas
    [ ] Sidebar slides from right (not modal or popup)
    [ ] Workflow context passed correctly (workflow_id, nodes)
    [ ] Conversation history persists during session
    [ ] Theatre mode integration works

Layer 3 (Chat Node):
    [ ] Chat node draggable onto canvas
    [ ] Node renders like other nodes (96x96px, correct styling)
    [ ] Node execution works in workflow
    [ ] Data flows in/out of chat node correctly
    [ ] Conversation tied to specific node instance

Layer 4 (Specialized Agents):
    [ ] Email agent opens when on email campaign page
    [ ] Website agent opens when on website builder
    [ ] Specialized UI loads correctly
    [ ] Context passed to agent (campaign data, page data, etc.)
    [ ] Graceful fallback if agent module not installed

---

MIGRATION NOTES
===============

Current State (2025-11-04):
    - During nuclear restructure, SAMChatBubble was moved to ai_sam_workflows
    - This is INCORRECT - it belongs in ai_sam (platform)
    - Need to move back: ai_sam_workflows/chat_ui → ai_sam/chat_ui

Files to Move:
    FROM: ai_sam_workflows/static/src/chat_ui/
    TO:   ai_sam/static/src/chat_ui/

    Files:
        - sam_chat_bubble.js ← CRITICAL (platform component)
        - SAM_CHAT_BUBBLE_USAGE.md
        - CHAT_UI_STYLES_DESIGN.md

Files to KEEP in ai_sam_workflows:
    - sam_workflow_chat.js (Layer 2 - workflow sidebar)
    - [Any workflow-specific chat files]

Files to KEEP in ai_sam:
    - sam_chat_vanilla_v2_action.xml (Layer 1 action)
    - [Systray chat files]

---

FUTURE EXPANSION
================

Adding New Specialized Agent (Layer 4):
    1. Create new module (e.g., ai_sam_crm_agent)
    2. Build specialized UI in that module
    3. Update Layer 1 routing logic to detect new location
    4. Add routing rule: "If on CRM reports → Open CRM Agent UI"
    5. Test graceful fallback if module not installed

Adding New Location Expertise (Layer 1):
    1. Identify new Odoo app/page (e.g., "Project Management")
    2. Create specialized prompt for that domain
    3. Update Layer 1 location detection to recognize page
    4. Add prompt mapping: "Project page → Project Expert prompt"
    5. No new files needed (just prompt configuration!)

Extending Workflow Chat (Layer 2):
    1. Keep changes in ai_sam_workflows module
    2. Add features to sam_workflow_chat.js
    3. Don't touch Layer 1 (routing stays the same)
    4. Test sidebar functionality on canvas

Adding New Chat Node Type (Layer 3):
    1. Create new node in ai_sam_workflows/sam_agent_nodes/
    2. Register node type in node picker
    3. Ensure node follows workflow execution pattern
    4. Test data flow in/out of node

---

VERSION HISTORY
===============

2025-11-04: Initial document created during nuclear restructure
            - Defined 4-layer architecture
            - Identified SAMChatBubble misplacement
            - Documented routing patterns
            - Established file organization rules

---

END OF DOCUMENT

This is the AUTHORITATIVE definition of SAM AI chat architecture.
Any future changes to chat functionality MUST reference this document.
Any AI agent working on chat MUST read this document FIRST.

If this document is wrong, UPDATE IT - don't work around it!
