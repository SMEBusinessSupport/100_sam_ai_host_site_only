# SAM AI Chat Package - Architecture Plan

**Created**: 2025-12-30
**Author**: CTO Architect Session
**Status**: IMPLEMENTED (Phases 1-5 Complete)
**Module**: ai_sam_base
**Implementation Date**: 2025-12-30

---

## Executive Summary

This document defines the architecture for SAM AI's "Chat Package" - a clean, scalable system for AI-powered conversations that separates **static foundation** from **dynamic context**.

### Core Principle

```
SESSION START: Build rich context ONCE
EVERY MESSAGE AFTER: Just chat
```

### The Problem We're Solving

Current architecture:
- Rebuilds 3000+ token system prompt on EVERY message
- Mixes location logic, personality, tools, and memory haphazardly
- 10 tangled prompt steps that are hard to maintain
- No clear separation between what's static vs dynamic

New architecture:
- Session context built ONCE at session/location start
- Clear separation: Location Knowledge + SAM Identity + Chat Tools
- Efficient token usage (rich start, lean conversation)
- Scalable (new modules add to location, not core)

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        SESSION START (Built Once)                        │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌────────────────────────────────────────────────────────────────────┐ │
│  │  build_session_context()                                           │ │
│  │  ══════════════════════════════════════════════════════════════════│ │
│  │                                                                     │ │
│  │  ┌─────────────────────┐  ┌─────────────────────┐                  │ │
│  │  │  location_insights()│  │  sam_identity()     │                  │ │
│  │  │  ─────────────────  │  │  ─────────────────  │                  │ │
│  │  │  • Where SAM is     │  │  • SAM User perms   │                  │ │
│  │  │  • Domain context   │  │  • Personality      │                  │ │
│  │  │  • Location tools   │  │  • Core tools       │                  │ │
│  │  │  • Relevant models  │  │  • Business context │                  │ │
│  │  └─────────────────────┘  └─────────────────────┘                  │ │
│  │                                                                     │ │
│  │  OUTPUT: system_prompt + tools (injected once)                     │ │
│  └────────────────────────────────────────────────────────────────────┘ │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                        CONVERSATION (Every Message)                      │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌────────────────────────────────────────────────────────────────────┐ │
│  │  sam_chat()                                                        │ │
│  │  ══════════════════════════════════════════════════════════════════│ │
│  │                                                                     │ │
│  │  • Receives user message                                           │ │
│  │  • Uses session context (already injected)                         │ │
│  │  • Executes tools as needed                                        │ │
│  │  • Returns response                                                │ │
│  │                                                                     │ │
│  │  Chat Tools Available:                                             │ │
│  │  • memory_recall - Search past conversations                       │ │
│  │  • voice_mode - Adjust communication style                         │ │
│  │                                                                     │ │
│  └────────────────────────────────────────────────────────────────────┘ │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Component Specifications

### 1. Session Context Builder

**File**: `ai_sam_base/api_communications/session_context.py`

**Purpose**: Build the complete session context ONCE at session start.

**When Called**:
- User opens a new location (canvas, CRM, etc.)
- User starts a new conversation
- Location/URL changes significantly

**NOT Called**:
- On every message (that's the key change)

```python
class SessionContextBuilder:
    """
    Builds SAM's session context - called ONCE per session/location.

    Combines:
    - Location insights (dynamic - where SAM is)
    - SAM identity (static - who SAM is)
    - Business context (static - who SAM works for)
    - Available tools (location + core + chat)
    """

    def __init__(self, env, user_id):
        self.env = env
        self.user_id = user_id
        self.sam_user = env.ref('ai_sam_base.sam_user', raise_if_not_found=False)

    def build(self, context_data):
        """
        Build complete session context.

        Args:
            context_data: Location context from frontend
                - canvas_id, model, action_id, URL, etc.

        Returns:
            dict: {
                'system_prompt': str,      # Complete prompt (inject once)
                'tools': list,             # All tools for this session
                'session_id': str,         # Unique session identifier
                'location': dict,          # Parsed location info
                'expires_on_location_change': bool,
            }
        """
        # 1. Get location insights (dynamic)
        location = self._get_location_insights(context_data)

        # 2. Get SAM identity (static, but loaded fresh)
        identity = self._get_sam_identity()

        # 3. Get business context (static)
        business = self._get_business_context()

        # 4. Collect all tools
        tools = self._collect_tools(location)

        # 5. Build system prompt
        system_prompt = self._build_system_prompt(
            location=location,
            identity=identity,
            business=business,
            tools=tools,
        )

        return {
            'system_prompt': system_prompt,
            'tools': tools,
            'session_id': self._generate_session_id(),
            'location': location,
            'expires_on_location_change': True,
        }

    def _get_location_insights(self, context_data):
        """Delegate to location_insights module."""
        from .location_insights import get_location_insights
        return get_location_insights(self.env, context_data)

    def _get_sam_identity(self):
        """Load SAM's static identity."""
        return {
            'personality': self._load_personality_file(),
            'permissions': self._get_sam_permissions(),
            'user_id': self.sam_user.id if self.sam_user else None,
        }

    def _get_business_context(self):
        """Load company business context."""
        company = self.env.company
        return {
            'company_name': company.name,
            'business_description': getattr(company, 'sam_business_context', None),
        }

    def _collect_tools(self, location):
        """Combine core + location + chat tools."""
        from .core_tools import CORE_TOOLS
        from .chat_tools import CHAT_TOOLS

        tools = CORE_TOOLS.copy()
        tools.extend(CHAT_TOOLS)
        tools.extend(location.get('tools', []))

        return tools
```

---

### 2. Location Insights

**File**: `ai_sam_base/api_communications/location_insights.py`

**Purpose**: Determine WHERE SAM is and WHAT she should know here.

**This is the ONLY dynamic part.**

```python
"""
Location Insights - The Dynamic Component

Determines:
- What domain SAM is in (workflow, CRM, sales, etc.)
- What models are relevant HERE
- What tools are needed HERE
- What contextual knowledge applies HERE
"""

from odoo.addons.ai_sam_base.models.canvas_tools import get_canvas_tools

# Domain detection rules
DOMAIN_DETECTORS = {
    'workflow': {
        'url_patterns': ['/canvas/', '/workflow/'],
        'context_flags': ['canvas_id', 'workflow_id', 'is_workflow_chat'],
        'models': ['canvas'],
        'tool_loader': get_canvas_tools,
    },
    'crm': {
        'url_patterns': ['/crm/', '/leads/'],
        'context_flags': ['crm_lead_id'],
        'models': ['crm.lead', 'crm.stage'],
        'tool_loader': None,  # Future: get_crm_tools
    },
    # Add more domains as modules are enhanced
}


def get_location_insights(env, context_data):
    """
    Main entry point - analyze context and return location insights.

    Args:
        env: Odoo environment
        context_data: Dict from frontend with URL, action_id, etc.

    Returns:
        dict: {
            'domain': 'workflow',           # Detected domain
            'domain_name': 'Workflow Builder',
            'primary_model': 'canvas',      # Main model for this location
            'related_models': [...],        # Other relevant models
            'current_record': 35,           # Current record ID if any
            'tools': [...],                 # Location-specific tools
            'knowledge': '...',             # Domain-specific context text
        }
    """
    # Detect domain
    domain_key, domain_config = _detect_domain(context_data)

    if not domain_key:
        return _generic_location(env, context_data)

    # Load domain-specific tools
    tools = []
    if domain_config.get('tool_loader'):
        tools = domain_config['tool_loader'](env, context_data)

    # Build domain knowledge
    knowledge = _build_domain_knowledge(env, domain_key, context_data)

    return {
        'domain': domain_key,
        'domain_name': _get_domain_name(domain_key),
        'primary_model': domain_config['models'][0] if domain_config['models'] else None,
        'related_models': domain_config['models'][1:] if len(domain_config['models']) > 1 else [],
        'current_record': _extract_record_id(context_data),
        'tools': tools,
        'knowledge': knowledge,
    }


def _detect_domain(context_data):
    """Detect which domain based on context signals."""
    for domain_key, config in DOMAIN_DETECTORS.items():
        # Check context flags
        for flag in config.get('context_flags', []):
            if context_data.get(flag):
                return domain_key, config

        # Check URL patterns
        url = context_data.get('url', '')
        for pattern in config.get('url_patterns', []):
            if pattern in url:
                return domain_key, config

    return None, None


def _build_domain_knowledge(env, domain_key, context_data):
    """Build domain-specific knowledge text for system prompt."""
    if domain_key == 'workflow':
        return _build_workflow_knowledge(env, context_data)
    elif domain_key == 'crm':
        return _build_crm_knowledge(env, context_data)
    return ""


def _build_workflow_knowledge(env, context_data):
    """Build workflow-specific knowledge."""
    lines = []
    lines.append("## YOU ARE IN: Workflow Builder")
    lines.append("")

    canvas_id = context_data.get('canvas_id')
    if canvas_id:
        try:
            canvas = env['canvas'].browse(int(canvas_id))
            if canvas.exists():
                lines.append(f"**Current Canvas:** {canvas.name} (ID: {canvas_id})")
                # Add node summary, etc.
        except:
            pass

    # Add node catalog info
    try:
        node_count = env['all.node.types'].search_count([])
        supplier_count = env['all.node.suppliers'].search_count([])
        lines.append(f"**Available:** {node_count} integrations from {supplier_count} services")
    except:
        pass

    return '\n'.join(lines)
```

---

### 3. Chat Tools

**File**: `ai_sam_base/api_communications/chat_tools.py`

**Purpose**: Tools available in ALL chat sessions (not location-specific).

```python
"""
Chat Tools - Always Available in sam_chat()

These tools are about COMMUNICATION and MEMORY, not location-specific actions.
"""

CHAT_TOOLS = [
    {
        'name': 'memory_recall',
        'description': 'Search past conversations for relevant information. Use when user asks "do you remember...", "we discussed...", or when context from past conversations would help.',
        'input_schema': {
            'type': 'object',
            'properties': {
                'query': {
                    'type': 'string',
                    'description': 'Natural language search query'
                },
                'limit': {
                    'type': 'integer',
                    'description': 'Maximum results to return',
                    'default': 5
                }
            },
            'required': ['query']
        }
    },
    # Future chat tools:
    # {
    #     'name': 'set_voice_mode',
    #     'description': 'Adjust communication style (concise, detailed, technical, friendly)',
    #     ...
    # },
]


def execute_chat_tool(env, tool_name, params):
    """
    Execute a chat tool.

    Args:
        env: Odoo environment
        tool_name: Name of tool to execute
        params: Tool parameters

    Returns:
        Tool execution result
    """
    executors = {
        'memory_recall': _execute_memory_recall,
        # Add more executors as tools are added
    }

    executor = executors.get(tool_name)
    if not executor:
        raise ValueError(f"Unknown chat tool: {tool_name}")

    return executor(env, **params)


def _execute_memory_recall(env, query, limit=5):
    """
    Execute memory recall using vector search.

    Searches past conversations semantically.
    """
    try:
        vector_service = env['ai.vector.service']
        results = vector_service.semantic_search(query, limit=limit)

        if not results:
            return {
                'found': False,
                'message': f"No past conversations found matching '{query}'"
            }

        return {
            'found': True,
            'count': len(results),
            'conversations': [
                {
                    'id': r['conversation_id'],
                    'name': r['conversation_name'],
                    'relevance': f"{r['similarity'] * 100:.1f}%",
                    'excerpt': r['excerpt'],
                    'date': r['created_at'],
                }
                for r in results
            ]
        }
    except Exception as e:
        return {
            'found': False,
            'error': str(e)
        }
```

---

### 4. Core Tools

**File**: `ai_sam_base/api_communications/core_tools.py`

**Purpose**: Base CRUD tools SAM always has (permission-gated).

```python
"""
Core Tools - SAM's Base Capabilities

These are CRUD operations gated by SAM's ir.model.access.csv permissions.
SAM can only use these on models she has explicit access to.
"""

CORE_TOOLS = [
    {
        'name': 'odoo_read',
        'description': 'Read records from an Odoo model. Returns field values for specified record IDs.',
        'input_schema': {
            'type': 'object',
            'properties': {
                'model': {
                    'type': 'string',
                    'description': 'Odoo model name (e.g., "res.partner", "sale.order")'
                },
                'ids': {
                    'type': 'array',
                    'items': {'type': 'integer'},
                    'description': 'Record IDs to read'
                },
                'fields': {
                    'type': 'array',
                    'items': {'type': 'string'},
                    'description': 'Fields to return (empty = all fields)'
                }
            },
            'required': ['model', 'ids']
        }
    },
    {
        'name': 'odoo_search',
        'description': 'Search for records in an Odoo model using domain filters.',
        'input_schema': {
            'type': 'object',
            'properties': {
                'model': {
                    'type': 'string',
                    'description': 'Odoo model name'
                },
                'domain': {
                    'type': 'array',
                    'description': 'Odoo domain filter (e.g., [["active", "=", true]])'
                },
                'fields': {
                    'type': 'array',
                    'items': {'type': 'string'},
                    'description': 'Fields to return'
                },
                'limit': {
                    'type': 'integer',
                    'description': 'Maximum records to return',
                    'default': 50
                }
            },
            'required': ['model']
        }
    },
    {
        'name': 'odoo_create',
        'description': 'Create a new record in an Odoo model.',
        'input_schema': {
            'type': 'object',
            'properties': {
                'model': {
                    'type': 'string',
                    'description': 'Odoo model name'
                },
                'values': {
                    'type': 'object',
                    'description': 'Field values for the new record'
                }
            },
            'required': ['model', 'values']
        }
    },
    {
        'name': 'odoo_write',
        'description': 'Update existing records in an Odoo model.',
        'input_schema': {
            'type': 'object',
            'properties': {
                'model': {
                    'type': 'string',
                    'description': 'Odoo model name'
                },
                'ids': {
                    'type': 'array',
                    'items': {'type': 'integer'},
                    'description': 'Record IDs to update'
                },
                'values': {
                    'type': 'object',
                    'description': 'Field values to update'
                }
            },
            'required': ['model', 'ids', 'values']
        }
    },
]


def execute_core_tool(env, sam_user, tool_name, params):
    """
    Execute a core tool AS SAM USER.

    Uses .with_user(sam_user) for proper audit trail and permission checking.
    """
    if not sam_user:
        raise ValueError("SAM user not configured")

    model_name = params.get('model')
    if not model_name:
        raise ValueError("Model name required")

    # Execute as SAM user
    Model = env[model_name].with_user(sam_user)

    if tool_name == 'odoo_read':
        return Model.browse(params['ids']).read(params.get('fields', []))

    elif tool_name == 'odoo_search':
        records = Model.search(
            params.get('domain', []),
            limit=params.get('limit', 50)
        )
        return records.read(params.get('fields', []))

    elif tool_name == 'odoo_create':
        record = Model.create(params['values'])
        return {'id': record.id, 'success': True}

    elif tool_name == 'odoo_write':
        Model.browse(params['ids']).write(params['values'])
        return {'success': True, 'updated_ids': params['ids']}

    raise ValueError(f"Unknown core tool: {tool_name}")
```

---

### 5. SAM Chat Core

**File**: `ai_sam_base/api_communications/sam_chat.py`

**Purpose**: The main chat handler - uses session context, handles messages.

```python
"""
SAM Chat Core - The Conversation Handler

This is the SIMPLE part. Session context is already built.
This just handles message in → response out.
"""

import logging
from .chat_tools import execute_chat_tool, CHAT_TOOLS
from .core_tools import execute_core_tool, CORE_TOOLS

_logger = logging.getLogger(__name__)


class SAMChat:
    """
    SAM's chat handler.

    Instantiated with session context, then handles messages.

    Usage:
        # At session start
        session = SessionContextBuilder(env, user_id).build(context_data)
        chat = SAMChat(env, session)

        # For each message
        response = chat.process_message(user_message)
    """

    def __init__(self, env, session_context):
        """
        Initialize chat with session context.

        Args:
            env: Odoo environment
            session_context: Output from SessionContextBuilder.build()
        """
        self.env = env
        self.session = session_context
        self.system_prompt = session_context['system_prompt']
        self.tools = session_context['tools']
        self.sam_user = env.ref('ai_sam_base.sam_user', raise_if_not_found=False)

        # Conversation history for this session
        self.messages = []

    def process_message(self, user_message, conversation_id=None):
        """
        Process a user message and return SAM's response.

        This is the main entry point for chat.

        Args:
            user_message: User's message text
            conversation_id: Optional ai.conversation ID for persistence

        Returns:
            dict: {
                'response': str,           # SAM's response text
                'tool_calls': list,        # Tools that were called
                'conversation_id': int,    # Conversation record ID
            }
        """
        # Add user message to history
        self.messages.append({
            'role': 'user',
            'content': user_message
        })

        # Call AI API
        response = self._call_ai_api()

        # Handle tool calls if any
        tool_results = []
        while response.get('tool_calls'):
            tool_results.extend(self._execute_tools(response['tool_calls']))
            response = self._call_ai_api(tool_results=tool_results)

        # Add assistant response to history
        assistant_message = response.get('content', '')
        self.messages.append({
            'role': 'assistant',
            'content': assistant_message
        })

        # Persist to database if conversation_id provided
        if conversation_id:
            self._persist_messages(conversation_id, user_message, assistant_message)

        return {
            'response': assistant_message,
            'tool_calls': tool_results,
            'conversation_id': conversation_id,
        }

    def _call_ai_api(self, tool_results=None):
        """
        Call the AI API with current context.

        System prompt is injected ONLY on first call (or can be cached by API).
        """
        # Build messages for API
        api_messages = self.messages.copy()

        # Add tool results if any
        if tool_results:
            for result in tool_results:
                api_messages.append({
                    'role': 'tool',
                    'tool_call_id': result['tool_call_id'],
                    'content': str(result['result'])
                })

        # Call API (delegate to ai.service)
        ai_service = self.env['ai.service']
        return ai_service.chat_completion(
            system_prompt=self.system_prompt,
            messages=api_messages,
            tools=self.tools,
        )

    def _execute_tools(self, tool_calls):
        """Execute tool calls and return results."""
        results = []

        for call in tool_calls:
            tool_name = call['name']
            params = call['parameters']

            try:
                # Determine tool type and execute
                if tool_name in [t['name'] for t in CHAT_TOOLS]:
                    result = execute_chat_tool(self.env, tool_name, params)
                elif tool_name in [t['name'] for t in CORE_TOOLS]:
                    result = execute_core_tool(self.env, self.sam_user, tool_name, params)
                else:
                    # Location-specific tool
                    result = self._execute_location_tool(tool_name, params)

                results.append({
                    'tool_call_id': call['id'],
                    'tool_name': tool_name,
                    'result': result,
                    'success': True,
                })
            except Exception as e:
                _logger.error(f"Tool {tool_name} failed: {e}")
                results.append({
                    'tool_call_id': call['id'],
                    'tool_name': tool_name,
                    'result': {'error': str(e)},
                    'success': False,
                })

        return results

    def _execute_location_tool(self, tool_name, params):
        """Execute a location-specific tool (canvas_edit, etc.)."""
        # Import location tool executors dynamically based on session location
        location = self.session.get('location', {})
        domain = location.get('domain')

        if domain == 'workflow':
            from .canvas_tools import execute_canvas_tool
            return execute_canvas_tool(self.env, tool_name, params)

        raise ValueError(f"Unknown tool: {tool_name}")

    def _persist_messages(self, conversation_id, user_message, assistant_message):
        """Save messages to ai.conversation/ai.message."""
        Message = self.env['ai.message']

        # User message
        Message.create({
            'conversation_id': conversation_id,
            'role': 'user',
            'content': user_message,
        })

        # Assistant message
        Message.create({
            'conversation_id': conversation_id,
            'role': 'assistant',
            'content': assistant_message,
        })
```

---

### 6. Business Context Field

**File**: `ai_sam_base/models/res_company.py` (new or extend)

**Purpose**: Allow companies to describe their business for SAM.

```python
from odoo import models, fields

class ResCompany(models.Model):
    _inherit = 'res.company'

    sam_business_context = fields.Text(
        string='SAM Business Context',
        help='Describe your business for SAM AI (up to 1000 words). '
             'Include: what you do, your customers, key products/services, '
             'industry context. SAM will use this to provide more relevant assistance.'
    )
```

---

## File Structure

```
ai_sam_base/
├── api_communications/
│   ├── __init__.py
│   ├── session_manager.py      # NEW - Session lifecycle (resume + refresh)
│   ├── session_context.py      # NEW - Session context builder
│   ├── location_insights.py    # NEW - Location detection & knowledge
│   ├── sam_chat.py             # NEW - Main chat handler
│   ├── chat_tools.py           # NEW - Memory, voice mode tools
│   ├── core_tools.py           # NEW - CRUD tools
│   ├── canvas_tools.py         # EXISTS - Refactor to fit pattern
│   ├── system_prompt_builder.py # DEPRECATE - Replace with session_context
│   └── ...
├── models/
│   ├── res_company.py          # NEW - Business context field
│   ├── ai_vector_service.py    # EXISTS - Memory search
│   ├── ai_conversation.py      # EXISTS - Conversation storage
│   └── ...
├── data/
│   ├── sam_identity_data.xml   # EXISTS - SAM user/partner
│   └── ...
└── security/
    ├── ir.model.access.csv     # EXISTS - SAM permissions
    └── ...
```

---

## Implementation Phases

### Phase 1: Foundation (Do First)
**Goal**: SAM User + Core Tools + Simple Chat

| Task | File | Effort |
|------|------|--------|
| Verify/fix SAM user setup | `data/sam_identity_data.xml` | 1 hour |
| Create core_tools.py | `api_communications/core_tools.py` | 2 hours |
| Create basic sam_chat.py | `api_communications/sam_chat.py` | 3 hours |
| Test SAM can do CRUD as SAM user | - | 1 hour |

**Deliverable**: SAM can chat and do basic Odoo operations with proper audit trail.

---

### Phase 2: Location Insights
**Goal**: Dynamic context based on where user is

| Task | File | Effort |
|------|------|--------|
| Create location_insights.py | `api_communications/location_insights.py` | 3 hours |
| Refactor canvas_tools.py to fit pattern | `api_communications/canvas_tools.py` | 2 hours |
| Create session_context.py | `api_communications/session_context.py` | 3 hours |
| Wire up: location → tools → prompt | - | 2 hours |

**Deliverable**: Session context built once, location-aware tools loaded.

---

### Phase 3: Memory Tools
**Goal**: SAM can recall past conversations

| Task | File | Effort |
|------|------|--------|
| Create chat_tools.py with memory_recall | `api_communications/chat_tools.py` | 2 hours |
| Wire memory_recall to ai.vector.service | - | 1 hour |
| Test "do you remember..." queries | - | 1 hour |

**Deliverable**: SAM can search and recall past conversations.

---

### Phase 4: Business Context
**Goal**: SAM knows who she works for

| Task | File | Effort |
|------|------|--------|
| Add sam_business_context to res.company | `models/res_company.py` | 1 hour |
| Add settings UI for business context | `views/res_config_settings_views.xml` | 1 hour |
| Inject business context at session start | `session_context.py` | 30 min |

**Deliverable**: SAM understands business context.

---

### Phase 5: Cleanup & Deprecation
**Goal**: Remove old complexity

| Task | File | Effort |
|------|------|--------|
| Deprecate system_prompt_builder.py | - | 2 hours |
| Remove redundant prompt steps | - | 2 hours |
| Update all entry points to use new pattern | - | 3 hours |

**Deliverable**: Clean, maintainable codebase.

---

## Success Criteria

1. **Session context built ONCE** - Not rebuilt on every message
2. **Clear separation** - Location vs Identity vs Tools
3. **SAM User permissions** - All operations use SAM user, proper audit trail
4. **Memory works** - "Do you remember..." queries return relevant results
5. **Location tools load** - Canvas tools only when on canvas
6. **Business context injected** - SAM knows company context
7. **Token efficient** - Rich start, lean conversation

---

## Migration Path

**Current state** → **New state**

1. New code lives alongside old (no breaking changes initially)
2. New `/chat/v2` endpoint uses new architecture
3. Test thoroughly
4. Migrate existing endpoints
5. Deprecate old code

---

## Session Lifecycle (Hybrid: Resume + Refresh)

**Decision**: Sessions persist per location and resume with context refresh.

### The Flow

```
┌─────────────────────────────────────────────────────────────────────────┐
│  SESSION LIFECYCLE                                                       │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  1. LOCATION ENTER (first time)                                          │
│     → Full session context build                                         │
│     → System prompt injected                                             │
│     → Session cached by location_key (e.g., "canvas:35")                 │
│     → Location state snapshot saved                                      │
│                                                                          │
│  2. LOCATION RE-ENTER (returning)                                        │
│     → Resume cached session (conversation history intact)                │
│     → Refresh location state (lightweight check)                         │
│     → If changed: inject delta ("Canvas has changed since...")           │
│     → Conversation continues naturally                                   │
│                                                                          │
│  3. SESSION EXPIRE                                                       │
│     → After TTL (e.g., 30 minutes idle)                                  │
│     → Or browser/tab close                                               │
│     → Next visit = fresh session                                         │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### Session Manager

**File**: `ai_sam_base/api_communications/session_manager.py`

```python
"""
Session Manager - Handles session lifecycle per location.

Sessions persist per location_key and resume with context refresh.
"""

import hashlib
import json
from datetime import datetime, timedelta

SESSION_TTL_MINUTES = 30


class SessionManager:
    """
    Manages SAM chat sessions per user per location.

    Key behaviors:
    - Same location = same session (conversation continues)
    - Different location = different session
    - Returning to location = resume + refresh context
    - Session expires after TTL
    """

    # In-memory cache (could be Redis in production)
    _sessions = {}

    @classmethod
    def get_or_create_session(cls, env, user_id, context_data):
        """
        Get existing session for this location, or create new one.

        Args:
            env: Odoo environment
            user_id: Current user ID
            context_data: Location context from frontend

        Returns:
            dict: Session context (new or resumed)
        """
        location_key = cls._get_location_key(context_data)
        cache_key = f"{user_id}:{location_key}"

        existing = cls._sessions.get(cache_key)

        if existing and not cls._is_expired(existing):
            # RESUME with refresh
            return cls._resume_session(env, existing, context_data)
        else:
            # NEW session
            return cls._create_session(env, user_id, context_data, cache_key)

    @classmethod
    def _get_location_key(cls, context_data):
        """
        Generate unique key for this location.

        Examples:
            - "canvas:35"
            - "crm.lead:142"
            - "general"
        """
        if context_data.get('canvas_id'):
            return f"canvas:{context_data['canvas_id']}"
        if context_data.get('workflow_id'):
            return f"canvas:{context_data['workflow_id']}"
        if context_data.get('model') and context_data.get('record_id'):
            return f"{context_data['model']}:{context_data['record_id']}"
        if context_data.get('model'):
            return f"{context_data['model']}:list"
        return "general"

    @classmethod
    def _is_expired(cls, session):
        """Check if session has expired."""
        last_activity = session.get('last_activity')
        if not last_activity:
            return True
        expiry = last_activity + timedelta(minutes=SESSION_TTL_MINUTES)
        return datetime.now() > expiry

    @classmethod
    def _create_session(cls, env, user_id, context_data, cache_key):
        """Create a new session with full context build."""
        from .session_context import SessionContextBuilder

        builder = SessionContextBuilder(env, user_id)
        session = builder.build(context_data)

        # Add session management fields
        session['cache_key'] = cache_key
        session['created_at'] = datetime.now()
        session['last_activity'] = datetime.now()
        session['location_state'] = cls._snapshot_location_state(env, context_data)
        session['conversation_history'] = []

        # Cache it
        cls._sessions[cache_key] = session

        return session

    @classmethod
    def _resume_session(cls, env, session, context_data):
        """
        Resume existing session with context refresh.

        Checks if location state changed and injects delta if needed.
        """
        session['last_activity'] = datetime.now()

        # Check if location state changed
        current_state = cls._snapshot_location_state(env, context_data)
        previous_state = session.get('location_state', {})

        if current_state != previous_state:
            # Compute and inject delta
            delta = cls._compute_state_delta(env, previous_state, current_state, context_data)
            if delta:
                session['pending_context_refresh'] = delta
            session['location_state'] = current_state

        return session

    @classmethod
    def _snapshot_location_state(cls, env, context_data):
        """
        Take a snapshot of current location state for change detection.
        """
        snapshot = {}

        # Canvas state
        canvas_id = context_data.get('canvas_id') or context_data.get('workflow_id')
        if canvas_id:
            try:
                canvas = env['canvas'].browse(int(canvas_id))
                if canvas.exists():
                    snapshot['canvas_id'] = canvas.id
                    snapshot['canvas_name'] = canvas.name
                    snapshot['json_hash'] = hashlib.md5(
                        (canvas.json_definition or '').encode()
                    ).hexdigest()[:8]
            except:
                pass

        return snapshot

    @classmethod
    def _compute_state_delta(cls, env, old_state, new_state, context_data):
        """
        Compute what changed between states.

        Returns a message to inject into conversation.
        """
        changes = []

        # Canvas changes
        if old_state.get('json_hash') != new_state.get('json_hash'):
            canvas_id = context_data.get('canvas_id') or context_data.get('workflow_id')
            if canvas_id:
                try:
                    canvas = env['canvas'].browse(int(canvas_id))
                    # Could compute detailed diff here
                    changes.append(f"The workflow '{canvas.name}' has been modified")
                except:
                    changes.append("The workflow has been modified")

        if not changes:
            return None

        return {
            'type': 'context_refresh',
            'message': "**Context Update:** " + ". ".join(changes) +
                       ". I'll take the current state into account."
        }

    @classmethod
    def update_conversation_history(cls, cache_key, user_message, assistant_message):
        """Update session's conversation history."""
        session = cls._sessions.get(cache_key)
        if session:
            session['conversation_history'].append({
                'role': 'user',
                'content': user_message
            })
            session['conversation_history'].append({
                'role': 'assistant',
                'content': assistant_message
            })
            session['last_activity'] = datetime.now()

    @classmethod
    def clear_session(cls, cache_key):
        """Explicitly clear a session."""
        cls._sessions.pop(cache_key, None)

    @classmethod
    def clear_expired_sessions(cls):
        """Cleanup expired sessions (call periodically)."""
        expired = [
            key for key, session in cls._sessions.items()
            if cls._is_expired(session)
        ]
        for key in expired:
            del cls._sessions[key]
```

### User Experience

```
User: Opens Canvas 35
SAM: [Full session created, rich context]

User: "Add a Gmail trigger"
SAM: "I'll add a Gmail trigger to your workflow..." [uses tools]

User: [Navigates to CRM, does work]
User: [Returns to Canvas 35]

User: "Now connect it to Slack"
SAM: [Session RESUMED - remembers Gmail discussion]
     [Detects canvas changed]
     "**Context Update:** The workflow has been modified. I'll take
      the current state into account.

      Connecting your Gmail trigger to Slack now..."
```

### Integration with sam_chat.py

```python
class SAMChat:
    def process_message(self, user_message, conversation_id=None):
        # Check for pending context refresh
        if self.session.get('pending_context_refresh'):
            refresh = self.session.pop('pending_context_refresh')
            # Inject as system message
            self.messages.append({
                'role': 'system',
                'content': refresh['message']
            })

        # Continue normal processing...
```

---

## Open Questions

1. **Session storage**: In-memory (current) vs Redis vs Database?
   - In-memory is simple but lost on server restart
   - Redis for multi-worker deployments
   - Database for persistence across restarts

2. **Voice modes**: Priority for implementation?
   - Code mode, friendly mode, expert mode

3. **Memory auto-embedding**: Should new conversations auto-embed?
   - Currently configurable in ai.memory.config

---

## Appendix: Current vs New Architecture

### Current (system_prompt_builder.py)

```
EVERY MESSAGE:
  → _build_sam_personality()        # 50 lines
  → _build_sam_system_knowledge()   # load file
  → _build_expertise_identity()     # 60 lines
  → _build_business_intelligence()  # 80 lines
  → _build_platform_context()       # introspector call
  → _build_system_state()           # query modules
  → _build_canvas_state()           # if canvas
  → _build_tools_section()          # list tools
  → _build_user_context()           # user prefs
  → _build_mode_instructions()      # mode file

  = 3000+ tokens rebuilt every time
```

### New (session_context + sam_chat)

```
SESSION START:
  → location_insights()     # where am I
  → sam_identity()          # who is SAM (static)
  → business_context()      # who we work for (static)
  → collect_tools()         # core + location + chat

  = System prompt built ONCE

EVERY MESSAGE:
  → sam_chat.process_message()

  = Just conversation
```

---

## Implementation Log (2025-12-30)

All phases implemented in a single session.

### Files Created

| Phase | File | Purpose |
|-------|------|---------|
| 1 | `api_communications/core_tools.py` | CRUD tools (odoo_read, odoo_search, odoo_create, odoo_write) |
| 1 | `api_communications/sam_chat.py` | Chat handler with session context |
| 2 | `api_communications/location_insights.py` | Domain detection and knowledge |
| 2 | `api_communications/session_context.py` | Session context builder (build ONCE) |
| 2 | `api_communications/session_manager.py` | Session lifecycle (resume + refresh) |
| 3 | `api_communications/chat_tools.py` | Memory recall tool |
| 4 | `models/res_company.py` | sam_business_context field |
| 4 | `views/res_config_settings_views.xml` | Settings UI for business context |

### Files Modified

| Phase | File | Change |
|-------|------|--------|
| 1-4 | `api_communications/__init__.py` | Added imports for new modules |
| 4 | `models/__init__.py` | Added res_company import |
| 4 | `models/res_config_settings.py` | Added related field |
| 4 | `__manifest__.py` | Added views XML |
| 5 | `api_communications/system_prompt_builder.py` | Deprecation notice |
| 5 | `api_communications/conversation.py` | Added process_message_v2() |

### Entry Point

Use the new architecture via:

```python
from odoo.addons.ai_sam_base.api_communications.conversation import get_conversation_core

core = get_conversation_core(env)
result = core.process_message_v2(
    user_message="Hello SAM",
    user_id=user.id,
    context_data={'canvas_id': 35}
)
```

### Testing Checklist

- [ ] Session created on first message
- [ ] Session resumed on subsequent messages (same location)
- [ ] Different location creates different session
- [ ] State change injects delta message
- [ ] memory_recall tool works with ChromaDB
- [ ] Business context appears in system prompt
- [ ] Core tools execute as SAM user (audit trail)

---

**End of Architecture Plan**
