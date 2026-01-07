# API Communications - v2 Architecture

**This folder contains ALL code for SAM talking to AI APIs.**

## v2 Architecture (2025-12-30)

Consolidated from 12+ files to **2 core files + infrastructure**.

```
Frontend Request
       ↓
┌──────────────────────────────────────────────────────────────┐
│                    api_communications/                        │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  CORE FILES (Where the magic happens):                        │
│                                                               │
│  ┌─────────────────────┐    ┌─────────────────────┐          │
│  │  system_prompt.py   │    │    sam_chat.py      │          │
│  │  WHAT SAM KNOWS     │ →  │  HOW SAM TALKS      │          │
│  │  (build ONCE)       │    │  (every message)    │          │
│  └─────────────────────┘    └─────────────────────┘          │
│                                                               │
│  INFRASTRUCTURE:                                              │
│  • session_manager.py  - Session lifecycle (resume + refresh) │
│  • api_services.py     - External AI providers (Claude, GPT)  │
│  • memory.py           - Vector search & conversation history │
│                                                               │
└──────────────────────────────────────────────────────────────┘
       ↓
Frontend Response
```

## The Two Core Files

### 1. system_prompt.py - WHAT SAM KNOWS

Built **ONCE** per session, not on every message. Contains:
- `CORE_TOOLS` - CRUD operations (odoo_read, odoo_search, etc.)
- `CHAT_TOOLS` - Communication tools (memory_recall)
- `DOMAIN_DETECTORS` - Location detection registry
- `SessionContextBuilder` - Main context builder class
- `build_session_context()` - Main entry point

```python
from odoo.addons.ai_sam_base.api_communications.system_prompt import (
    build_session_context,
    CORE_TOOLS,
    CHAT_TOOLS,
)

# Build once at session start
session = build_session_context(env, user_id, context_data)
# session = { system_prompt, tools, location, user, session_id }
```

### 2. sam_chat.py - HOW SAM TALKS

Handles **every message** after session context is built. Contains:
- `SAMChat` class - Main chat handler
- `execute_core_tool()` - CRUD executor (uses SAM user for audit trail)
- `execute_chat_tool()` - Memory recall executor
- `process_chat_message()` - Non-streaming entry point
- `process_chat_message_streaming()` - Streaming entry point

```python
from odoo.addons.ai_sam_base.api_communications.sam_chat import (
    process_chat_message,           # Non-streaming
    process_chat_message_streaming, # Streaming
)

# Simple usage
result = process_chat_message(env, message, user_id, context_data)

# Streaming usage
for chunk in process_chat_message_streaming(env, message, user_id, context_data):
    yield chunk
```

## File Structure

| File | Purpose | Status |
|------|---------|--------|
| **system_prompt.py** | WHAT SAM KNOWS (session context, tools, knowledge) | **v2 CORE** |
| **sam_chat.py** | HOW SAM TALKS (message handling, tool execution) | **v2 CORE** |
| session_manager.py | Session lifecycle (resume + refresh pattern) | Infrastructure |
| api_services.py | External AI provider utilities | Infrastructure |
| memory.py | Vector search and conversation history | Infrastructure |
| chat_input.py | Context gathering (activity streaming) | Infrastructure |
| chat_output.py | Response formatting | Infrastructure |
| http_routes.py | Web endpoints from frontend | Infrastructure |
| vendor_population.py | Vendor template population | Infrastructure |
| dev_utils.py | Dev mode detection (is_dev_mode, should_always_inject_prompt) | Infrastructure |
| conversation.py | OLD orchestrator (deprecated) | Legacy |
| system_prompt_builder.py | OLD prompt builder (deprecated) | Legacy |
| core_tools.py | Consolidated into system_prompt.py | Legacy |
| chat_tools.py | Consolidated into system_prompt.py | Legacy |
| location_insights.py | Consolidated into system_prompt.py | Legacy |
| session_context.py | Consolidated into system_prompt.py | Legacy |

## Key Concepts

### Chat Entry Points (2025-12-31)

SAM has **4 distinct entry points** for chat. Each has different UI, features, and session isolation.

| Entry Point | Description | Sidebar | Tabs | Session Isolation |
|-------------|-------------|---------|------|-------------------|
| **MENU_CHAT** | SAM AI > Chat With Sam menu | No | Yes | General (no isolation) |
| **CHAT_BUBBLE** | Floating chat bubble overlay | **Yes** | No | General (no isolation) |
| **CANVAS_CHAT** | Canvas AI Builder toolbar | No | Yes | By `canvas_id` |
| **NODE_CHAT** | Workflow node-specific chat | No | No | By `node_id` |

**Frontend Configuration**: `ai_sam/static/src/config/sam_config.js`

```javascript
import { CHAT_ENTRY_POINT, ENTRY_POINT_RULES } from '@ai_sam/config/sam_config';

// Detect entry point from context
const entryPoint = detectChatEntryPoint(contextData);

// Get rules for UI rendering
const rules = getEntryPointRules(entryPoint);
console.log(rules.ui.showTabBar);     // true/false
console.log(rules.features.multiTab); // true/false

// Get session isolation params for backend calls
const isolation = getSessionIsolationParams(entryPoint, contextData);
// Returns: { node_id: null, canvas_id: null } or specific IDs
```

**Backend Session Isolation**: `/sam/session/get_history` and `/sam/session/auto_save` both accept `node_id` and `canvas_id` parameters to filter sessions by context.

### Standardized Overlay System (2025-12-31)

All chat entry points use **ONE standardized overlay** for consistent UI behavior.

**Frontend Configuration**: `ai_sam/static/src/config/sam_chat_overlay.js`

```javascript
import { SamChatOverlay } from '@ai_sam/config/sam_chat_overlay';

// Create overlay for specific entry point
const overlay = new SamChatOverlay('chat_bubble', {
    context: { model: 'crm.lead', record_id: 123 },
    onClose: () => console.log('Closed'),
    onOpen: () => console.log('Opened')
});

// Open the overlay
await overlay.open();

// Mount chat inside overlay
const chatInstance = new SamChatVanilla(overlay.getMountPoint(), {
    mode: 'overlay',
    context: overlay.options.context,
    onClose: () => overlay.close()
});
await chatInstance.init();
```

**Overlay Configuration Per Entry Point**:

| Entry Point | Size | Position | Backdrop | Animation |
|-------------|------|----------|----------|-----------|
| `chat_bubble` | 90% viewport | Center | Yes (click to close) | Fade + Scale |
| `canvas_chat` | 400px sidebar | Right | No | Slide Right |
| `node_chat` | 380x500px | Floating | Yes (click to close) | Fade + Scale |
| `menu_chat` | 100% | Full page | No | None |

### Session-Based Architecture

Session context is built **ONCE** at session start:
- When user opens a new location (canvas, CRM, etc.)
- When user starts a new conversation
- When session expires

This is more efficient than rebuilding on every message.

### Domain Detection

SAM automatically detects where the user is:

| Domain | Detection Signals | Tools |
|--------|-------------------|-------|
| workflow | canvas_id, workflow_id, /canvas/ | Canvas tools |
| crm | crm_lead_id, /crm/ | CRM helpers |
| sales | sale_order_id, /sale/ | Sales helpers |
| inventory | stock_picking_id, /stock/ | Inventory helpers |

New domains can be registered:
```python
from odoo.addons.ai_sam_base.api_communications.system_prompt import register_domain

register_domain('my_domain', {
    'url_patterns': ['/my_module/'],
    'context_flags': ['my_flag'],
    'models': ['my.model'],
    'domain_name': 'My Domain',
    'tool_loader': '_load_my_tools',
})
```

### Tool Execution

Tools are executed **AS SAM USER** for proper audit trail:

```python
# In sam_chat.py
Model = env[model_name].with_user(sam_user)  # Audit trail shows SAM
record = Model.create(values)  # create_uid = SAM user
```

## Quick Reference

### Processing a Chat Message (NEW v2)
```python
from odoo.addons.ai_sam_base.api_communications.sam_chat import process_chat_message

result = process_chat_message(
    env=request.env,
    user_message="Show me all open leads",
    user_id=request.env.uid,
    context_data={'model': 'crm.lead'},
    conversation_id=None,  # Or existing conversation ID
)
```

### Processing with Streaming (NEW v2)
```python
from odoo.addons.ai_sam_base.api_communications.sam_chat import process_chat_message_streaming

for chunk in process_chat_message_streaming(env, message, user_id, context_data):
    if chunk['type'] == 'chunk':
        print(chunk['content'], end='')
    elif chunk['type'] == 'done':
        print("Complete!")
```

### Building Session Context Directly
```python
from odoo.addons.ai_sam_base.api_communications.system_prompt import build_session_context

session = build_session_context(
    env=self.env,
    user_id=self.env.user.id,
    context_data={'canvas_id': 35, 'is_workflow_chat': True},
)

# Access components
print(session['system_prompt'])  # Full prompt text
print(session['tools'])          # All tools for this location
print(session['location'])       # Domain info
```

### Getting Tools for a Location
```python
from odoo.addons.ai_sam_base.api_communications.system_prompt import get_tools_for_location

tools = get_tools_for_location(env, {'canvas_id': 35})
# Returns: CORE_TOOLS + CHAT_TOOLS + canvas_tools
```

## Migration from v1

If you have code using the old architecture:

| OLD (v1) | NEW (v2) |
|----------|----------|
| `ConversationCore(env).process_message()` | `process_chat_message()` |
| `build_system_prompt()` | `build_session_context()['system_prompt']` |
| `execute_core_tool()` from core_tools.py | `execute_core_tool()` from sam_chat.py |
| Import from multiple files | Import from 2 files |

## Troubleshooting

### SAM doesn't have the right tools

Check the location detection:
```python
from odoo.addons.ai_sam_base.api_communications.system_prompt import get_location_insights

location = get_location_insights(env, context_data)
print(f"Domain: {location['domain']}")
print(f"Tools: {len(location['tools'])}")
```

### Session not persisting

Check session manager:
```python
from odoo.addons.ai_sam_base.api_communications.session_manager import SessionManager

session = SessionManager.get_or_create_session(env, user_id, context_data)
print(f"Session ID: {session['session_id']}")
```

### Tool execution fails

Check SAM user exists:
```python
sam_user = env.ref('ai_sam_base.sam_user', raise_if_not_found=False)
if not sam_user:
    print("SAM user not configured!")
```

---
*v2 Architecture: 2025-12-30*
*Chat Entry Points: 2025-12-31*
*Standardized Overlay: 2025-12-31*
*Consolidated from 12+ files to 2 core files*
