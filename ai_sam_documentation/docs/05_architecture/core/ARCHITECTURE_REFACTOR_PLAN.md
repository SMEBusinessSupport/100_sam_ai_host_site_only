# SAM AI Architecture Refactor Plan

**Document:** ARCHITECTURE_REFACTOR_PLAN.md
**Created:** 2025-12-15
**Status:** IN PROGRESS - Phases 1-4, 6-15 Complete (14/15)
**Authors:** Anthony Gardiner & Claude AI

---

## Executive Summary

Refactor SAM AI's scattered codebase into a clean, human-readable architecture where:
- **One bug = One file to investigate**
- **File names describe their purpose in plain English**
- **Conversation and Workflow share the same structural pattern**

---

## The Problem (Current State)

### Scattered Responsibilities

```
User sends message
        |
        v
sam_chat_controller.py ──────> ai_service.py (2500+ lines!)
        |                           |
        |                           ├── context gathering
        |                           ├── permission checks
overlay_manager.js                  ├── memory search
        |                           ├── AI API calls
        |                           ├── streaming
sam_chat_vanilla_v2.js              └── error handling
        |
        v
   5+ files touched for any bug fix
```

### Real Example: Today's Debugging Session

**Bug:** "folder_file_link not being passed to SAM"

**Files we had to trace:**
1. `overlay_manager.js` - where context is built
2. `sam_chat_vanilla_v2.js` - where context is stored
3. `sam_chat_controller.py` - where request is received
4. `ai_service.py` - where context is processed
5. `ai_service.py` again - `gather_workflow_node_context()`

**Time spent:** Hours

**With new architecture:** Would be in `node_input.py` - **one file**.

---

## The Solution (Target Architecture)

### Core Principle: Human-Readable Names

| Current Name | New Name | Plain English Purpose |
|--------------|----------|----------------------|
| `ai_service.py` | **`ai_brain.py`** | "THE BRAIN - orchestrates everything" |
| `behaviour.py` | **`ai_voice.py`** | "THE VOICE - composes system prompts" |
| `ai_orchestrator.py` | `api_services.py` | "The phone - calls Claude/GPT" |
| `sam_chat_controller.py` | `http_routes.py` | "The front door - receives requests" |
| `ai_memory_config.py` | `memory.py` | "The memory - remembers past chats" |
| (scattered) | `response.py` | "The response - formats & streams answers" |

**Phase 10 (2025-12-15):** Renamed files for clarity:
- `ai_sam_base/models/ai_service.py` → `ai_brain.py` (THE BRAIN)
- `ai_sam_base/api_communications/behaviour.py` → `ai_voice.py` (THE VOICE)

---

## Architecture Diagrams

### Conversation System (Chat)

```
                    ┌─────────────────┐
                    │ http_routes.py  │  "I receive web requests"
                    └────────┬────────┘
                             │
                             v
┌────────────────────────────────────────────────────────────┐
│                    conversation.py                          │
│                "The brain - coordinates everything"         │
│                                                            │
│   ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │
│   │ ai_voice.py  │  │  memory.py   │  │api_services.py│   │
│   │ "THE VOICE"  │  │ "remembers"  │  │ "calls AI"   │    │
│   └──────────────┘  └──────────────┘  └──────────────┘    │
│                                                            │
│                    ┌──────────────┐                        │
│                    │ response.py  │                        │
│                    │"formats reply"│                        │
│                    └──────────────┘                        │
└────────────────────────────────────────────────────────────┘
```

### Workflow System (Automation)

```
                    ┌─────────────────┐
                    │  workflow.py    │  "Orchestrates node execution"
                    └────────┬────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
        v                    v                    v
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│node_input.py │    │   node.py    │    │node_output.py│
│              │    │              │    │              │
│"gathers data"│    │ "processes"  │    │"sends result"│
│              │    │              │    │              │
│ - folders    │    │ - executes   │    │ - next node  │
│ - files      │    │ - transforms │    │ - files      │
│ - prev nodes │    │ - AI calls   │    │ - APIs       │
│ - APIs       │    │              │    │ - Odoo       │
│ - webhooks   │    │              │    │              │
└──────────────┘    └──────────────┘    └──────────────┘
```

### The Shared Pattern

```
CONVERSATION inherits from ──────> BASE PATTERN <────── WORKFLOW inherits from

                              ┌─────────────┐
                              │   CORE.py   │
                              │ orchestrator│
                              └──────┬──────┘
                                     │
                    ┌────────────────┼────────────────┐
                    │                │                │
                    v                v                v
              ┌─────────┐     ┌─────────┐     ┌─────────┐
              │ INPUT   │     │ PROCESS │     │ OUTPUT  │
              │ gather  │     │ execute │     │ format  │
              └─────────┘     └─────────┘     └─────────┘
```

---

## File Structure (Target)

### ai_sam_base Module

```
ai_sam_base/
├── __init__.py
├── __manifest__.py
│
├── models/                      # Odoo ORM models (database)
│   ├── __init__.py
│   ├── ai_conversation.py       # Conversation records (unchanged)
│   ├── ai_message.py            # Message records (unchanged)
│   └── ai_file_permission.py    # Permission records (unchanged)
│
├── services/                    # NEW - Business logic
│   ├── __init__.py
│   │
│   │   # === CORE ORCHESTRATOR ===
│   ├── conversation.py          # THE BRAIN - all chat flows through here
│   │
│   │   # === SUPPORTING SERVICES ===
│   ├── http_routes.py           # Web endpoints (receives requests)
│   ├── api_services.py          # External AI providers (Claude, GPT)
│   ├── memory.py                # Vector search, past conversations
│   ├── ai_voice.py              # THE VOICE - Prompt composer (renamed from behaviour.py)
│   └── response.py              # Streaming, formatting, error handling
│
└── controllers/                 # Odoo HTTP controllers (thin wrappers)
    ├── __init__.py
    └── main.py                  # Routes to services/http_routes.py
```

### ai_sam_workflows Module

```
ai_sam_workflows/
├── __init__.py
├── __manifest__.py
│
├── models/                      # Odoo ORM models (database)
│   ├── __init__.py
│   └── workflow_node.py         # Node records (unchanged)
│
├── services/                    # NEW - Business logic
│   ├── __init__.py
│   │
│   │   # === CORE ORCHESTRATOR ===
│   ├── workflow.py              # THE BRAIN - all workflow flows through here
│   │
│   │   # === NODE LIFECYCLE ===
│   ├── node_input.py            # Gathers data from all sources
│   ├── node.py                  # Processes/executes node logic
│   └── node_output.py           # Sends results to destinations
│
└── controllers/                 # Odoo HTTP controllers (thin wrappers)
    └── main.py
```

---

## Service Specifications

### conversation.py (The Brain)

```python
# ai_sam_base/api_communications/conversation.py
"""
Central orchestrator for all SAM AI chat interactions.
ALL behavior modifications happen here or in its service modules.

This is THE file to start with when debugging any chat issue.
"""

class ConversationCore:
    """
    The brain of SAM AI chat.

    Flow:
        1. Receive message via http_routes.py
        2. Build context via behaviour.py
        3. Search memory via memory.py
        4. Send to AI via api_services.py
        5. Stream response via response.py
    """

    def __init__(self, env):
        self.env = env
        self.voice = Voice(env)  # THE VOICE - prompt composer
        self.memory = Memory(env)
        self.api = APIServices(env)
        self.response = Response(env)

    def process_message(self, user_message, conversation_id, context_data):
        """
        Single entry point for ALL chat messages.

        Args:
            user_message: What the user typed
            conversation_id: Session identifier
            context_data: Frontend context (node_id, folder_file_link, etc.)

        Returns:
            dict: Response with 'content', 'conversation_id', etc.
        """
        # 1. Build full context
        context = self.voice.build_context(context_data)

        # 2. Check permissions
        if permission_needed := self.voice.check_permissions(context):
            return permission_needed

        # 3. Search memory for relevant past conversations
        memories = self.memory.search(user_message, limit=5)

        # 4. Send to AI provider
        ai_response = self.api.send(
            message=user_message,
            context=context,
            memories=memories
        )

        # 5. Format and return response
        return self.response.format(ai_response)
```

### node_input.py (Data Gathering)

```python
# ai_sam_workflows/services/node_input.py
"""
Handles ALL ways a workflow node can receive data.

This is THE file to check when node inputs aren't working.

Supported input sources:
    - folder_file_link: Local files and folders
    - previous_node_id: Output from upstream nodes
    - api_source: External API data
    - odoo_model: Odoo database records
    - webhook_data: Incoming webhook payloads
"""

class NodeInput:
    """
    Gathers data from all input sources for a workflow node.

    Example:
        input_service = NodeInput(env)
        data = input_service.gather(node_data)
        # data = [
        #     {'type': 'folder', 'path': '...', 'files': [...]},
        #     {'type': 'previous_node', 'output': {...}},
        # ]
    """

    def __init__(self, env):
        self.env = env

    def gather(self, node_data):
        """
        Main entry point - gathers all inputs for a node.

        Args:
            node_data: Dict with node configuration
                - folder_file_link: str (optional)
                - previous_node_id: str (optional)
                - api_source: dict (optional)
                - odoo_model: dict (optional)
                - webhook_data: dict (optional)

        Returns:
            list: All gathered inputs with type, source, and content
        """
        inputs = []

        # File/Folder inputs
        if folder_path := node_data.get('folder_file_link'):
            inputs.extend(self.from_folder(folder_path))

        # Previous node outputs
        if prev_node_id := node_data.get('previous_node_id'):
            inputs.extend(self.from_previous_node(prev_node_id))

        # API inputs
        if api_config := node_data.get('api_source'):
            inputs.extend(self.from_api(api_config))

        # Odoo model inputs
        if model_config := node_data.get('odoo_model'):
            inputs.extend(self.from_odoo(model_config))

        # Webhook inputs
        if webhook := node_data.get('webhook_data'):
            inputs.extend(self.from_webhook(webhook))

        return inputs

    # === INPUT SOURCE METHODS ===

    def from_folder(self, path):
        """Read files from a local folder path."""
        # Validation, reading, content extraction
        ...

    def from_previous_node(self, node_id):
        """Get output from an upstream node."""
        ...

    def from_api(self, api_config):
        """Fetch data from an external API."""
        ...

    def from_odoo(self, model_config):
        """Read records from Odoo database."""
        ...

    def from_webhook(self, webhook_data):
        """Process incoming webhook payload."""
        ...
```

---

## Bug Location Guide

### "Where do I look for this bug?"

| Bug Symptom | File to Check | Method to Review |
|-------------|---------------|------------------|
| Message not sending | `http_routes.py` | `send_message()` |
| Context not building | `behaviour.py` | `build_context()` |
| AI not responding | `api_services.py` | `send()` |
| Memory not working | `memory.py` | `search()` |
| Response formatting | `response.py` | `format()` |
| **Node inputs broken** | **`node_input.py`** | **`gather()` or `from_*()`** |
| Node execution fails | `node.py` | `execute()` |
| Node outputs wrong | `node_output.py` | `send()` |
| Workflow orchestration | `workflow.py` | `run()` |

---

## Migration Plan

### Phase 1: Create Structure (No Breaking Changes) ✅ COMPLETE

1. ✅ Create `services/` folders in both modules
2. ✅ Create empty service files with docstrings
3. ✅ Add `__init__.py` files
4. ✅ No functional changes yet

**Completed:** 2025-12-15

### Phase 2: Extract conversation.py ✅ COMPLETE

1. ✅ Created ConversationCore class as central orchestrator
2. ✅ Delegates to ai_service.py for backward compatibility
3. ✅ All major methods wrapped: process_message, streaming, create_conversation, etc.
4. ✅ Added convenience factory function: get_conversation_core(env)

**Completed:** 2025-12-15

### Phase 3: Extract Supporting Services ✅ COMPLETE

1. ✅ Extract `behaviour.py` (context building, system prompts, permissions)
2. ✅ Extract `memory.py` (vector search, past conversation retrieval)
3. ✅ Extract `api_services.py` (AI providers, API format routing)
4. ✅ Extract `response.py` (streaming, formatting, activity messages)

**Completed:** 2025-12-15

### Phase 4: Extract Workflow Services ✅ COMPLETE

1. ✅ Extract `workflow.py` (WorkflowOrchestrator - full execution flow)
2. ✅ Extract `node_input.py` (NodeInput - folder/file extraction, API, Odoo sources)
3. ✅ Extract `node.py` (Node execution with type handlers: AI, transform, condition, action)
4. ✅ Extract `node_output.py` (NodeOutput - file, API, Odoo, notification destinations)

**Completed:** 2025-12-15

### Phase 5: Backend Cleanup

1. Remove dead code from original files
2. Update imports across codebase
3. Update documentation
4. Final testing

### Phase 6: Activity Feedback (chat_interaction.js) ✅ COMPLETE

1. ✅ Create `ai_sam/static/src/js/chat/` folder structure
2. ✅ Create `chat_interaction.js` with activity states (ACTIVITY_STATES, ChatInteraction class)
3. ✅ Create `chat_interaction.css` with pulse animations and color theming
4. ✅ Add `updateActivity()` and `clearActivity()` methods to sam_chat_vanilla_v2.js
5. ✅ Replace generic "Thinking..." with context-aware activities (folder reading, AI calling, etc.)

**Completed:** 2025-12-15

### Phase 7: Compact Message Layout (2-Column) ✅ COMPLETE

1. ✅ Create `compact_messages.css` with CSS Grid 2-column layout
2. ✅ Update `renderMessage()` to support both classic and compact structures
3. ✅ Add `.message-meta` (left column) and `.message-body` (right column) containers
4. ✅ Add toggle button in header with localStorage persistence
5. ✅ Implement responsive stacking on mobile (< 600px)
6. ✅ Actions row hidden by default, shown on hover

**Completed:** 2025-12-15

### Phase 8: Recursive Folder Reading ✅ COMPLETE

Enhanced `node_input.py` to support recursive subfolder scanning.

**Before:** `from_folder()` only read files in the immediate directory (non-recursive)
**After:** `from_folder()` walks entire directory tree with smart file selection

**Key Features:**
1. ✅ Recursive scanning enabled by default (`recursive=True` parameter)
2. ✅ Respects `MAX_DEPTH` (5 levels) to prevent infinite loops
3. ✅ Priority-based file extraction (README, index, main, __init__ first)
4. ✅ Distributed extraction budget across subfolders (10 files total)
5. ✅ User-friendly messaging: "Found X folders and Y total files"
6. ✅ Returns `user_message` field for UI display
7. ✅ Folder structure visualization in AI context

**File Modified:** `ai_sam_workflows/services/node_input.py`

**New Method:** `_extract_folder_recursive(root_path)`

**Return Value Enhancement:**
```python
{
    'type': 'folder',
    'path': '/path/to/shared/folder',
    'stats': {
        'total_folders': 5,
        'total_files': 42,
        'text_files': 28,
        'summary': 'Found 5 folders and 42 files'
    },
    'user_message': 'I can now access 5 folders and 42 total files within the shared link.',
    'subfolders': [...],
    'files': [...],
    'content': '...'  # Human-readable context for AI
}
```

**Completed:** 2025-12-15

### Phase 9: Proactive AI Analysis Instructions ✅ COMPLETE

**The Problem:** SAM had the data but didn't know what to DO with it.

When given a folder like "The SAM Sales System", SAM responded:
> "The folder contains 9 files and 8 text files. Would you like me to summarize the contents?"

This is **passive** - asking permission instead of taking action.

**The Solution:** Added explicit instructions in the workflow context telling SAM to analyze proactively.

**Files Modified:**

1. **`ai_sam_base/models/ai_service.py`** (lines ~917-956)
   - Added "Your Instructions for This Context" section
   - Includes DO/DON'T guidelines with examples
   - Good example: "Looking at 'The SAM Sales System' folder, I see this is your strategic marketing foundation..."
   - Bad example: "The folder contains 9 files. Would you like me to..."

2. **`ai_sam_base/models/ai_service.py`** (lines ~2432-2459)
   - Refactored `gather_workflow_node_context()` to use new `NodeInput` service
   - Removed 130 lines of duplicate folder extraction code
   - Now uses centralized `ai_sam_workflows/services/node_input.py`
   - Gains recursive folder support automatically

**Key Instruction Added:**
```markdown
## Your Instructions for This Context

**CRITICAL: Be Proactive, Not Passive**

1. **READ the extracted content** - It's already provided below
2. **SYNTHESIZE what you find** - Don't just list files
3. **SHARE your perspective** - Like Claude Code does
4. **CONNECT to the user's work** - Relate findings to their needs

**DO NOT:**
- Say "I don't have access" (you do)
- Ask "Would you like me to..." (just do it)
- List files without analyzing them
```

**Expected Behavior Change:**

Before: "9 files found. Would you like detailed information?"
After: "Looking at your SAM Sales System, I see this is your strategic marketing foundation. The core positioning in THE-GOLD-STAR.md captures 'SAM AI remembers you and your business...' What strikes me is how this maps to the technical capabilities we're building..."

**Completed:** 2025-12-15

---

### Phase 10: Brain/Voice Architecture + System Prompt Slimming ✅ COMPLETE

**Goal:** Rename files for clarity + reduce system prompt from 571 lines to ~70 lines.

**Changes:**

1. **File Renames:**
   - `ai_sam_base/models/ai_service.py` → `ai_brain.py` (THE BRAIN - orchestrator)
   - `ai_sam_base/api_communications/behaviour.py` → `ai_voice.py` (intermediate step)

2. **System Prompt Slimming:**
   - OLD: `SAM_AI_MASTER_SYSTEM_PROMPT_V2.md` (571 lines) - personality + execution logic
   - NEW: `SAM_AI_PERSONALITY.md` (69 lines) - personality ONLY

**Completed:** 2025-12-15

---

### Phase 11: Domain-First Naming ✅ COMPLETE

**Goal:** Align chat service naming with workflow pattern.

**The Pattern:**
```
WORKFLOW: node_input.py → node.py → node_output.py
CHAT:     chat_input.py → ai_brain.py (shared) → chat_output.py
```

**File Renames:**
- `ai_sam_base/api_communications/ai_voice.py` → `chat_input.py` (context/prompt builder)
- `ai_sam_base/api_communications/response.py` → `chat_output.py` (response formatter)

**Class Renames:**
- `Voice` → `ChatInput`
- `Response` → `ChatOutput`

**Why ai_brain.py stays:**
- It's the shared AI orchestrator
- Both `node.py` and chat system call into it
- Handles Claude/GPT API calls, streaming, token tracking
- Domain-agnostic - serves any system needing AI

**Completed:** 2025-12-15

---

### Phase 12: Activity Streaming via gather_context() ✅ COMPLETE

**Goal:** Wire up real-time activity feedback so users see what SAM is doing (like Claude Code).

**The Pattern:**
```
User sends message
        ↓
Controller calls chat_input.gather_context()
        ↓
Generator yields activity events as work happens:
    → 📂 Reading folder...
    → 📄 Found 9 files...
    → 🧠 Searching past conversations...
    → 🔧 Building context...
        ↓
Controller forwards events via SSE
        ↓
Frontend displays each activity
        ↓
🤖 Asking Claude...
        ↓
✅ Done
```

**Files Modified:**

1. **`ai_sam_base/api_communications/chat_input.py`** - Added `gather_context()` generator
   ```python
   def gather_context(self, context_data, user_message=None):
       """
       Generator that yields activities as it gathers context.
       Use this when you want real-time feedback like Claude Code.
       """
       # PHASE 1: Folder/File Reading
       if folder_path := context_data.get('folder_file_link'):
           yield {'type': 'activity', 'activity': 'reading_folder', 'message': '📂 Reading folder...'}
           # ... extraction using node_input.py
           yield {'type': 'activity', 'activity': 'counting_files', 'message': '📄 Found N files...'}

       # PHASE 2: Memory Search
       if user_message:
           yield {'type': 'activity', 'activity': 'searching_memory', 'message': '🧠 Searching...'}

       # PHASE 3: Context Building
       yield {'type': 'activity', 'activity': 'building_context', 'message': '🔧 Building context...'}

       # FINAL: Complete context
       yield {'type': 'context_complete', 'context': context}
   ```

2. **`ai_sam_base/controllers/sam_ai_chat_controller.py`** - Integrated activity streaming
   ```python
   # In send_message_streaming():

   # PHASE 0: Activity Streaming via gather_context()
   from odoo.addons.ai_sam_base.api_communications.chat_input import ChatInput

   with registry.cursor() as cr:
       env = api.Environment(cr, uid, user_context)
       chat_input = ChatInput(env)

       for event in chat_input.gather_context(context_data, message):
           if event.get('type') == 'activity':
               yield f"event: activity\ndata: {json.dumps(event)}\n\n"
           elif event.get('type') == 'context_complete':
               gathered_context = event.get('context', {})

   # Later:
   yield f"event: activity\ndata: {json.dumps({'activity': 'calling_ai', 'message': '🤖 Asking Claude...'})}\n\n"
   # ... AI call ...
   yield f"event: activity\ndata: {json.dumps({'activity': 'complete', 'message': '✅ Done'})}\n\n"
   ```

**SSE Event Types:**
- `event: activity` - Progress updates (reading, searching, building)
- `event: status` - Progress percentage updates (existing)
- `event: chunk` - Response text chunks (existing)
- `event: done` - Completion with metadata (existing)

**Benefits:**
- User sees exactly what SAM is doing
- No more "Processing..." anxiety
- Matches Claude Code's activity feedback pattern
- Generator pattern allows easy extension for new activities

**Completed:** 2025-12-15

---

### Phase 13: Access Gate - Permission Control for Shared Links ✅ COMPLETE

**Goal:** Create a centralized permission system for "shared links" (folders/files users share with SAM).

**The Problem:**
- Users share folder links with SAM
- SAM needs explicit permission before accessing external resources
- Previous code referenced `sam.file.permission` and `ai.file.permission` - models that **didn't exist**!
- Permission logic was scattered across multiple files

**The Solution:** `ai.access.gate` - The GATEKEEPER

```
User shares a folder link
        ↓
chat_input.gather_context() runs
        ↓
🔐 Checking access...
        ↓
ai.access.gate.check_access(path)
        ↓
┌─────────────────────────────────────┐
│ Already approved? → ✅ Continue     │
│ Explicitly denied? → ⛔ Stop        │
│ New path? → 🔐 Create pending       │
└─────────────────────────────────────┘
        ↓
If pending → yield permission_required event
        ↓
Frontend shows approval buttons:
  [Yes, Allow] [Yes, Allow All in Folder] [No]
        ↓
User clicks → POST /sam/permission_response
        ↓
ai.access.gate.action_approve() or action_approve_recursive()
        ↓
User re-sends message → Now allowed!
```

**Files Created:**

1. **`ai_sam_base/models/ai_access_gate.py`** - The GATEKEEPER model
   ```python
   class AIAccessGate(models.Model):
       _name = 'ai.access.gate'

       user_id = fields.Many2one('res.users')
       path = fields.Char()
       state = fields.Selection([
           ('pending', 'Pending'),
           ('approved', 'Approved'),
           ('approved_recursive', 'Approved (Recursive)'),
           ('denied', 'Denied'),
       ])

       @api.model
       def check_access(self, path, user_id=None, reason=None):
           """THE method to call before accessing any external resource."""
           # Returns: {allowed, needs_approval, permission_request}

       def action_approve(self):
           """Approve exact path."""

       def action_approve_recursive(self):
           """Approve path and all subfolders (path/**)."""

       def action_deny(self):
           """Explicitly deny access."""
   ```

**Files Modified:**

1. **`ai_sam_base/api_communications/chat_input.py`** - Integrated access gate into `gather_context()`
   ```python
   # PHASE 1: Access Gate Check + Folder/File Reading
   if folder_path:
       yield {'activity': 'checking_access', 'message': '🔐 Checking access...'}

       access_result = self.env['ai.access.gate'].check_access(path=folder_path)

       if access_result.get('needs_approval'):
           yield {'type': 'permission_required', 'permission_request': ...}
           return  # Stop until approved
   ```

2. **`ai_sam_base/controllers/sam_ai_chat_controller.py`**
   - Updated `event_stream()` to handle `permission_required` events
   - Updated `handle_permission_response()` to use `ai.access.gate`

3. **`ai_sam_base/security/ir.model.access.csv`** - Added access rules

**SSE Event Flow:**
```
event: activity      → 🔐 Checking access to: My Folder...
event: permission_required → {permission_request: {id, path, buttons}}
event: done          → {needs_permission: true}
```

**Completed:** 2025-12-15

---

### Phase 14: Provider-Agnostic Streaming ✅ COMPLETE

**Goal:** Make streaming work with ANY AI provider, not just Anthropic SDK.

**The Problem:**
- Streaming was **hardcoded** to Anthropic SDK (`client.messages.stream()`)
- OpenAI users couldn't use streaming at all!
- Provider-specific naming ("Asking Claude...") made SAM seem provider-dependent
- User insight: "SAM is the intelligence - the provider is just the language engine"

**The Solution:** Provider-agnostic streaming via raw HTTP

**Philosophy Shift:**
```
BEFORE: SAM + Claude = Claude-dependent assistant
AFTER:  SAM = Unique intelligence, Provider = Conversational engine

SAM's characteristics, behavior, and intelligence are CONSISTENT
regardless of which AI provider is the "language engine".
```

**Files Modified:**

1. **`ai_sam_base/models/ai_brain.py`** - THE BRAIN
   - Added `_stream_anthropic()` - Extracted Anthropic SDK streaming
   - Added `_stream_openai()` - **NEW** Raw HTTP SSE for OpenAI-compatible APIs
   - Added `_stream_google()` - Placeholder for Google/Gemini (future)
   - Updated `send_message_streaming()` to route by `config.api_format`:
     - `openai` → `_stream_openai()` (raw HTTP SSE)
     - `anthropic` → `_stream_anthropic()` (SDK)
     - `google` → `_stream_google()` (not yet implemented)
   - Updated provider logging to use `api_format` instead of hardcoded names

2. **`ai_sam_base/controllers/sam_ai_chat_controller.py`**
   - Changed "🤖 Asking Claude..." → "🤖 Thinking..."
   - Changed "Routing to Claude API..." → "Connecting to AI..."
   - Changed "Sending to Claude API..." → "Processing your message..."
   - SAM speaks as SAM, not as a Claude wrapper

**OpenAI-Compatible Streaming (Raw HTTP SSE):**
```python
def _stream_openai(self, config, system_prompt, messages):
    """
    Works with ALL OpenAI-compatible providers:
    - OpenAI, Azure OpenAI
    - Groq, Together AI, DeepSeek
    - Ollama, LM Studio (local)
    - Any provider using OpenAI's API format
    """
    with requests.post(url, headers=headers, json=payload, stream=True) as response:
        for line in response.iter_lines(decode_unicode=True):
            if line.startswith('data: '):
                data = json.loads(line[6:])
                content = data['choices'][0]['delta'].get('content', '')
                yield {'type': 'chunk', 'data': {'text': content}}
```

**Why Raw HTTP Instead of OpenAI SDK?**
1. **One less dependency** - No openai package needed
2. **Full control** - See exactly what's happening
3. **Works with ALL OpenAI-compatible APIs** - Not just OpenAI
4. **Consistent with our architecture** - SAM owns the intelligence

**Provider Selection Flow:**
```
User sends message
       |
       v
send_message_streaming()
       |
       ├── api_format = 'openai'  ──> _stream_openai() [RAW HTTP SSE]
       ├── api_format = 'anthropic' ──> _stream_anthropic() [SDK]
       └── api_format = 'google'  ──> _stream_google() [NOT YET]
```

**Completed:** 2025-12-15

---

### Phase 15: Low-Cost Provider Options (Groq + Ollama) ✅ COMPLETE

**Goal:** Add nearly-free and completely-free LLM options to reduce API costs.

**The Insight:**
User question: "What are we really paying for with OpenAI/Anthropic?"

Answer: You're paying for their **default personality** and **safety tuning** - but SAM **overrides** most of that anyway!

```
SAM's Value (YOUR IP):
├── Business Intelligence
├── Odoo Integration
├── Memory System
├── Workflow Automation
└── Power Prompts

Language Engine (REPLACEABLE):
├── Anthropic ($$$) - "Claude personality"
├── OpenAI ($$) - "GPT personality"
├── Groq ($) - Llama at incredible speed
└── Ollama (FREE) - 100% local, 100% private
```

**What This Unlocks:**

| Provider | Cost | Speed | Privacy | Quality |
|----------|------|-------|---------|---------|
| Anthropic | $15-75/M | Good | Cloud | Excellent |
| OpenAI | $10-30/M | Good | Cloud | Excellent |
| **Groq** | $0.05-0.27/M | **FAST** | Cloud | Very Good |
| **Ollama** | **FREE** | Varies | **LOCAL** | Good |

**Files Modified:**

1. **`ai_sam/static/src/vendor_library/_registry/node_metadata.json`**
   - Added `groq` vendor entry with:
     - `api_format: "openai"` (OpenAI-compatible)
     - `api_endpoint: "https://api.groq.com/openai"`
     - `default_model: "llama-3.1-70b-versatile"`
     - `available_models: ["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "mixtral-8x7b-32768"]`
   - Added `ollama` vendor entry with:
     - `api_format: "openai"` (OpenAI-compatible)
     - `api_endpoint: "http://localhost:11434"`
     - `default_model: "llama3.1"`
     - `requires_credentials: false` (no API key needed!)

2. **`ai_sam_base/controllers/vendor_registry_controller.py`**
   - Updated `_populate_vendor_credentials()` to read `api_format`, `api_endpoint`, and `default_model` directly from node_metadata.json
   - Phase 15 enhancement: Vendor metadata takes priority over name-based detection

**Groq Entry:**
```json
"groq": {
  "displayName": "Groq",
  "api_format": "openai",
  "api_endpoint": "https://api.groq.com/openai",
  "default_model": "llama-3.1-70b-versatile",
  "is_ai_nodes": true,
  "is_whitelisted": true,
  "pricing_notes": "Very low cost - ~$0.05-0.27 per million tokens"
}
```

**Ollama Entry:**
```json
"ollama": {
  "displayName": "Ollama",
  "api_format": "openai",
  "api_endpoint": "http://localhost:11434",
  "default_model": "llama3.1",
  "requires_credentials": false,
  "pricing_notes": "FREE - Runs on your own hardware"
}
```

**Why This Matters:**

```
Development/Testing:  Use Groq (nearly free)
Enterprise customers: Let THEM choose (their API key)
Privacy-sensitive:    Use Ollama (100% local)
Maximum quality:      Anthropic/OpenAI (customer pays)
```

**Completed:** 2025-12-15

---

## Phase Summary

| Phase | Focus | Layer | Risk | Status |
|-------|-------|-------|------|--------|
| **1** | Create folder structure | Backend | LOW | ✅ DONE |
| **2** | Extract `conversation.py` | Backend | MEDIUM | ✅ DONE |
| **3** | Extract supporting services | Backend | MEDIUM | ✅ DONE |
| **4** | Extract workflow services | Backend | MEDIUM | ✅ DONE |
| **5** | Backend cleanup | Backend | LOW | Pending |
| **6** | Activity feedback UI | Frontend | LOW | ✅ DONE |
| **7** | Compact message layout | Frontend | LOW | ✅ DONE |
| **8** | Recursive folder reading | Backend | MEDIUM | ✅ DONE |
| **9** | Proactive AI analysis | Backend | HIGH | ✅ DONE |
| **10** | Brain/Voice + Prompt slimming | Backend | MEDIUM | ✅ DONE |
| **11** | Domain-first naming | Backend | LOW | ✅ DONE |
| **12** | Activity streaming | Backend/Frontend | MEDIUM | ✅ DONE |
| **13** | Access Gate (permissions) | Backend | MEDIUM | ✅ DONE |
| **14** | Provider-Agnostic Streaming | Backend | MEDIUM | ✅ DONE |
| **15** | Low-Cost Providers (Groq/Ollama) | Backend | LOW | ✅ DONE |

**Total: 16 Phases** (15 complete, 1 pending)

- Phases 1-5: Backend refactoring
- Phases 6-7: Frontend improvements
- Phases 8-15: AI capability expansion + cost optimization
- Phase 16: ML-powered personalization (in progress)

---

### Phase 16: ML-Powered Personalization (Scikit-Learn) 🚧 IN PROGRESS

**Goal:** Add Machine Learning capabilities to enhance SAM's personalization without being "creepy".

**The Insight:**
As SAM accumulates conversation history, we can use ML to recognize patterns:
- User communication preferences (concise vs detailed)
- Topic clusters (what they typically discuss)
- Optimal response timing and length
- Business domain vocabulary

**Philosophy: Silent Adaptation, Not Surveillance**

```
HELPFUL (Do This):
├── Learn user prefers bullet points → Use bullet points
├── Notice user is technical → Skip basic explanations
├── Recognize recurring topics → Provide deeper context
└── Adapt to communication style → Match their tone

CREEPY (Never Do This):
├── "I noticed you always work late on Thursdays..."
├── "Based on your emotional patterns..."
├── "Your productivity seems lower today..."
└── "I've been tracking your response times..."
```

**Key Components:**

1. **sam_voice.py** (renamed from sam_behavior.py)
   - THE GUARDRAIL - Filters what SAM can say about users
   - Contains `FORBIDDEN_PHRASES` list
   - Silent adaptation: behavior changes without announcing
   - Memory-enhanced prompts respect privacy

2. **Graceful Degradation Pattern:**
   ```python
   # SAM works perfectly without ML - just less personalized
   try:
       from sklearn.feature_extraction.text import TfidfVectorizer
       from sklearn.cluster import KMeans
       ML_AVAILABLE = True
   except ImportError:
       ML_AVAILABLE = False
       _logger.info("Scikit-learn not installed. ML features disabled.")
   ```

3. **ML Features (When Available):**
   - **Topic Clustering:** Group conversations by theme
   - **Style Analysis:** Detect user's preferred communication style
   - **Response Optimization:** Learn optimal response characteristics
   - **Vocabulary Enhancement:** Build user-specific term dictionary

**Files Modified:**

1. **`ai_sam_base/models/sam_voice.py`** (renamed from sam_behavior.py)
   - Renamed to reflect role as SAM's "voice" - personality guardrail
   - Contains memory-enhanced prompts
   - Future: ML-informed prompt adjustments

2. **`D:\SAMAI-18-SaaS\github-repos\14-samai_python_bundle\requirements.txt`**
   - Added scikit-learn dependency

**Dependencies Added:**
```
scikit-learn>=1.3.0    # Machine Learning for user pattern recognition
```

**Architecture Addition:**
```
┌─────────────────────────────────────────────────────────────┐
│                    ML LAYER (Optional)                       │
│                                                             │
│  ┌─────────────────┐  ┌─────────────────┐                   │
│  │ Pattern Analysis │  │ Style Detection │                   │
│  │ (Topic Clusters) │  │ (TF-IDF + KMeans)│                  │
│  └────────┬────────┘  └────────┬────────┘                   │
│           │                    │                            │
│           └──────────┬─────────┘                            │
│                      │                                      │
│                      ▼                                      │
│           ┌─────────────────────┐                           │
│           │    sam_voice.py     │                           │
│           │   (THE GUARDRAIL)   │                           │
│           │                     │                           │
│           │ ├ FORBIDDEN_PHRASES │                           │
│           │ ├ Silent Adaptation │                           │
│           │ └ Privacy-First     │                           │
│           └──────────┬──────────┘                           │
│                      │                                      │
│                      ▼                                      │
│              AI Brain (ai_brain.py)                         │
│              ML insights filtered through sam_voice         │
└─────────────────────────────────────────────────────────────┘
```

**Status:** Partially Complete
- ✅ Renamed sam_behavior.py → sam_voice.py
- ✅ Updated all import references
- ✅ Added scikit-learn to requirements.txt
- ✅ Created SAM_PYTHON_DEPENDENCIES.html documentation
- ✅ Enhanced SAM_ARCHITECTURE_SCHEMA.html with ML layer
- 🔲 Implement ML pattern analysis (future sprint)
- 🔲 Add FORBIDDEN_PHRASES enforcement
- 🔲 Build style detection algorithms

**Completed:** 2025-12-15 (Foundation)

---

## Chat UI Entry Points - Consistency Audit (2025-12-15)

### Current State: 2 of 4 Entry Points Use Master Class

| Entry Point | File | Class Used | Master Styling | Phase 6/7 Applied |
|-------------|------|------------|----------------|-------------------|
| **Menu Action** (fullscreen) | `sam_chat_vanilla_v2_action.js` | `SamChatVanilla` | ✅ `.sam-ai-chat-app` | ✅ YES |
| **Bubble Overlay** (modal) | `sam_ai_chat_widget.js` | `SamChatVanilla` | ✅ `.sam-ai-chat-app` | ✅ YES |
| **Workflow Chat** (sidebar) | `sam_workflow_chat.js` | `SAMWorkflowChat` | ❌ `.sam-chat-sidebar` | ❌ NO |
| **Creatives Chat** | `creatives_ai_chat_panel.js` | `CreativesAIChatPanel` | ❌ inline CSS | ❌ NO |

### Issues Identified

1. **Workflow Chat** (`ai_sam_workflows/static/src/chat_ui/sam_workflow_chat.js`)
   - Uses different class: `SAMWorkflowChat` instead of `SamChatVanilla`
   - Different container: `.sam-chat-sidebar` (missing `-ai-` in naming)
   - Hardcoded colors instead of CSS variables
   - Will NOT receive Phase 6 activity feedback or Phase 7 compact layout

2. **Creatives Chat** (`ai_sam_creatives/static/src/js/creatives_ai_chat_panel.js`)
   - Completely isolated implementation: `CreativesAIChatPanel`
   - Zero integration with master styling system
   - Duplicate functionality

### Potential Future Task: Unify Chat Entry Points

**Option A: Refactor to use SamChatVanilla**
- Add `mode: 'sidebar'` option to `SamChatVanilla`
- Update Workflow Chat to instantiate `SamChatVanilla` instead of `SAMWorkflowChat`
- Benefits: Unified styling, all Phase 6/7 features, reduced code duplication

**Option B: Share Design Tokens**
- Create `sam_design_tokens.css` with CSS variables
- Import into all chat implementations
- Benefits: Less risky, preserves existing functionality

**Decision: TBD** - Consider after observing Phase 6/7 in production.

---

## User Interaction Layer (Frontend)

### The Problem: "Processing..." Tells Humans Nothing

Current SAM shows generic messages while working:
- "Processing..."
- "Working on it..."
- "Analyzing..."

**The human has no idea what's happening.** They wonder: "Is it stuck? What is it doing?"

### The Solution: Real-Time Activity Feedback

Like Claude Code shows "Reading file: ai_service.py..." - SAM should show **what it's actually doing**.

### JavaScript File Structure

```
ai_sam/static/src/js/chat/
├── chat_ui.js              ← Renders the chat interface
├── chat_state.js           ← Manages messages, sessions, context
├── chat_api.js             ← Makes RPC calls to backend
├── chat_input.js           ← Handles user input, attachments
│
└── chat_interaction.js     ← NEW: Real-time activity feedback
                               "The eyes" - Shows what SAM is doing
```

### chat_interaction.js Specification

```javascript
// ai_sam/static/src/js/chat/chat_interaction.js
/**
 * Real-time activity feedback for SAM AI chat.
 * Shows the human WHAT SAM is doing, not just "Processing..."
 *
 * Philosophy: The human should never wonder "Is it stuck?"
 * They should always see meaningful, changing activity messages.
 */

class ChatInteraction {

    // Activity states with human-readable messages
    static ACTIVITIES = {
        // === INPUT GATHERING ===
        'reading_folder':     '📂 Reading folder: {folder}...',
        'counting_files':     '📄 Found {count} files...',
        'extracting_file':    '📝 Reading: {filename}...',
        'validating_path':    '🔍 Checking path access...',

        // === CONTEXT BUILDING ===
        'searching_memory':   '🧠 Searching past conversations...',
        'found_memories':     '💡 Found {count} relevant memories...',
        'building_context':   '🔧 Building context...',

        // === AI INTERACTION ===
        'calling_ai':         '🤖 Asking Claude...',
        'thinking':           '💭 Thinking...',
        'composing':          '✍️ Composing response...',

        // === RESPONSE ===
        'streaming':          '💬 Responding...',
        'complete':           '✅ Done',

        // === ERRORS ===
        'path_not_found':     '⚠️ Cannot access: {path}',
        'permission_needed':  '🔐 Permission required...',
    };

    constructor(displayElement) {
        this.display = displayElement;
        this.currentActivity = null;
        this.activityHistory = [];
    }

    /**
     * Show an activity to the user
     * @param {string} activity - Key from ACTIVITIES
     * @param {object} params - Values to interpolate ({folder}, {count}, etc.)
     */
    show(activity, params = {}) {
        let message = ChatInteraction.ACTIVITIES[activity] || activity;

        // Interpolate parameters
        Object.keys(params).forEach(key => {
            message = message.replace(`{${key}}`, params[key]);
        });

        this.currentActivity = { activity, message, timestamp: Date.now() };
        this.activityHistory.push(this.currentActivity);
        this.updateDisplay(message);
    }

    /**
     * Update the visual display
     */
    updateDisplay(message) {
        if (this.display) {
            this.display.textContent = message;
            this.display.classList.add('activity-pulse');  // CSS animation
        }
    }

    /**
     * Clear the activity display
     */
    clear() {
        if (this.display) {
            this.display.textContent = '';
            this.display.classList.remove('activity-pulse');
        }
    }

    /**
     * Get activity history (for debugging/logging)
     */
    getHistory() {
        return this.activityHistory;
    }
}

// Export for use in chat modules
window.ChatInteraction = ChatInteraction;
```

### Backend Integration (Python yields activities)

```python
# ai_sam_base/api_communications/conversation.py

def process_message(self, user_message, context_data):
    """
    Process a chat message with real-time activity feedback.
    Yields activity updates that frontend displays to user.
    """

    # === INPUT GATHERING ===
    if folder_path := context_data.get('folder_file_link'):
        yield {'activity': 'reading_folder', 'folder': os.path.basename(folder_path)}

        files = self.list_files(folder_path)
        yield {'activity': 'counting_files', 'count': len(files)}

        for file in files[:5]:  # Show first 5
            yield {'activity': 'extracting_file', 'filename': file.name}
            content = self.extract_content(file)

    # === CONTEXT BUILDING ===
    yield {'activity': 'searching_memory'}
    memories = self.memory.search(user_message)
    if memories:
        yield {'activity': 'found_memories', 'count': len(memories)}

    yield {'activity': 'building_context'}
    context = self.voice.build(context_data, memories)

    # === AI INTERACTION ===
    yield {'activity': 'calling_ai'}
    response_stream = self.api.send_streaming(user_message, context)

    # === RESPONSE STREAMING ===
    yield {'activity': 'streaming'}
    for chunk in response_stream:
        yield {'type': 'content', 'content': chunk}

    yield {'activity': 'complete'}
```

### CSS for Activity Animation

```css
/* ai_sam/static/src/css/chat_interaction.css */

.chat-activity-display {
    font-size: 13px;
    color: #666;
    padding: 8px 12px;
    min-height: 24px;
    transition: all 0.2s ease;
}

.activity-pulse {
    animation: pulse 1.5s infinite;
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.6; }
}

/* Activity-specific colors */
.activity-reading { color: #3498db; }   /* Blue - reading */
.activity-thinking { color: #9b59b6; }  /* Purple - AI thinking */
.activity-error { color: #e74c3c; }     /* Red - errors */
.activity-success { color: #27ae60; }   /* Green - complete */
```

### User Experience: Before vs After

| Before | After |
|--------|-------|
| "Processing..." | "📂 Reading folder: The SAM Sales System..." |
| (3 seconds of nothing) | "📄 Found 9 files..." |
| (user wonders if stuck) | "📝 Reading: foundation-positioning.md..." |
| (anxiety builds) | "🧠 Searching past conversations..." |
| (finally) Response appears | "🤖 Asking Claude..." → Response streams |

**The human is informed at every step. No anxiety. No wondering.**

---

## Chat Message Layout (Compact 2-Column)

### The Problem: Wasted Vertical Space

Current layout uses **3 rows per message**:
1. Row 1: Name only (● You)
2. Row 2: Message content
3. Row 3: Hidden actions (copy, regenerate)

**Result:** Only 4-5 messages visible at once. Wasteful.

### The Solution: 2-Column Grid Layout

```
┌──────────┬──────────────────────────────────────┐
│ ● You    │ can you tell me about my files please│
├──────────┼──────────────────────────────────────┤
│ ● Sam    │ To provide you with information...   │
├──────────┼──────────────────────────────────────┤
│ ● You    │ what can you tell me about them?     │
└──────────┴──────────────────────────────────────┘

Column 1: Names (fixed ~80px, left-aligned)
Column 2: Messages (flexible width)
```

### Design Decisions

| Element | Decision | Rationale |
|---------|----------|-----------|
| Actions row | **REMOVE** | Clutters UI, rarely used |
| Timestamps | **KEEP** | Useful for context |
| Avatar/dot | **KEEP** | Enhance later with real avatars |

### CSS Implementation

```css
/* ai_sam/static/src/css/chat_messages.css */

/* Compact 2-column message layout */
.sam-messages-container {
    display: flex;
    flex-direction: column;
    gap: 8px;  /* Tighter spacing between messages */
}

.sam-message {
    display: grid;
    grid-template-columns: 80px 1fr;  /* Name | Message */
    gap: 12px;
    align-items: start;
    padding: 8px 12px;
}

.sam-message.user {
    background: rgba(102, 126, 234, 0.08);
    border-radius: 8px;
}

.sam-message.assistant {
    background: transparent;
}

/* Column 1: Name */
.message-header {
    font-weight: 600;
    font-size: 13px;
    color: #333;
    white-space: nowrap;
    display: flex;
    align-items: center;
    gap: 6px;
}

.message-header .status-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #27ae60;  /* Green = online */
}

.message-header.user .status-dot {
    background: #3498db;  /* Blue for user */
}

/* Column 2: Message content */
.message-content {
    font-size: 14px;
    line-height: 1.5;
    color: #333;
}

/* Timestamp - subtle, inline */
.message-timestamp {
    font-size: 11px;
    color: #999;
    margin-left: 8px;
}

/* REMOVED: Actions row */
.message-actions {
    display: none !important;
}
```

### Before vs After

| Metric | Before | After |
|--------|--------|-------|
| Rows per message | 3 | 1 |
| Visible messages | 4-5 | 10-12 |
| Screen efficiency | ~30% | ~80% |
| Visual clutter | High | Low |

### JavaScript Changes

```javascript
// In chat_ui.js - Updated message rendering

renderMessage(message) {
    return `
        <div class="sam-message ${message.role}">
            <div class="message-header ${message.role}">
                <span class="status-dot"></span>
                ${message.role === 'user' ? 'You' : 'Sam'}
            </div>
            <div class="message-content">
                ${this.formatContent(message.content)}
                <span class="message-timestamp">${this.formatTime(message.timestamp)}</span>
            </div>
        </div>
    `;
    // NOTE: No .message-actions row - removed for cleaner UI
}
```

---

## Success Criteria

After refactoring:

1. **Any chat bug** → Start in `conversation.py`, follow to specific service
2. **Any node input bug** → Go directly to `node_input.py`
3. **Any AI response bug** → Go directly to `api_services.py`
4. **Any UI feedback bug** → Go directly to `chat_interaction.js`
5. **File names are self-documenting** → New developers understand immediately
6. **Each file < 500 lines** → Focused, readable, maintainable
7. **User never sees generic "Processing..."** → Always specific activity messages

---

## Risks and Mitigations

| Risk | Mitigation |
|------|------------|
| Breaking existing functionality | Thin wrappers first, migrate gradually |
| Import errors | Careful `__init__.py` management |
| Odoo ORM integration | Services receive `env`, models stay separate |
| Testing gaps | Write tests before each extraction |

---

## Approval

- [ ] Architecture approved by Anthony
- [ ] Phase 1 structure approved
- [ ] Migration timeline agreed
- [ ] Testing strategy confirmed

---

## Next Steps

1. **Review this document**
2. **Approve or modify the structure**
3. **Begin Phase 1** (create empty structure)
4. **Migrate incrementally** with testing at each phase

---

*This refactoring will transform hours of debugging into minutes.*
*One bug = One file.*
