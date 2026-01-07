# SAM AI System Prompt Architecture

## Overview

SAM's system prompt is now built from a **single source of truth**: `system_prompt_builder.py`

Like writing a system prompt in n8n's AI Agent node, but built dynamically with Python.

## Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                    system_prompt_builder.py                          │
│                    (Single Source of Truth)                          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  STEP 1: Tool Mandate (static)                                      │
│  "YOU HAVE TOOLS. USE THEM. DO NOT JUST TALK."                      │
│                                                                      │
│  STEP 2: Identity (static)                                          │
│  SAM's personality and voice                                         │
│                                                                      │
│  STEP 3: Platform Context (dynamic)                                 │
│  ← ai.location.introspector                                         │
│  "You have access to canvas model with 505 nodes..."                │
│                                                                      │
│  STEP 4: Available Tools (dynamic)                                  │
│  ← tools list passed from ai_brain.py                               │
│  "canvas_read, canvas_edit, canvas_node_types..."                   │
│                                                                      │
│  STEP 5: User Context (dynamic)                                     │
│  ← sam.user.profile                                                 │
│  User preferences, relationship level, tone                          │
│                                                                      │
│  STEP 6: Mode Instructions (dynamic)                                │
│  ← ai.mode.registry                                                 │
│  Workflow builder, page builder, etc.                                │
│                                                                      │
├─────────────────────────────────────────────────────────────────────┤
│                           OUTPUT                                     │
│                                                                      │
│  ONE clean system prompt string → sent to AI API                    │
│  + Debug file saved to ai_sam_base/data/debug_last_prompt.md        │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

## n8n Comparison

| n8n AI Agent | SAM AI |
|--------------|--------|
| System Prompt field | STEP 1-2: Static identity + mandate |
| Dynamic context | STEP 3-6: Platform, tools, user, mode |
| User Message | Passed separately (not in system prompt) |
| Tools | Passed to API alongside system prompt |

## File Structure

```
ai_sam_base/
├── services/
│   └── system_prompt_builder.py   ← NEW: Single source of truth
├── models/
│   ├── ai_brain.py                ← Uses builder (or legacy _build_system_prompt)
│   └── ai_location_introspector.py ← Provides platform context
├── data/
│   ├── debug_last_prompt.md       ← Auto-generated debug output
│   └── SAM_AI_MASTER_SYSTEM_PROMPT_V2.md  ← DEPRECATED (legacy)
```

## Usage

```python
from odoo.addons.ai_sam_base.api_communications.system_prompt_builder import build_system_prompt

# Build system prompt
prompt = build_system_prompt(
    env=self.env,
    context_data={'canvas_id': 35, 'is_workflow_chat': True},
    tools=[{'name': 'canvas_read', 'description': '...'}],
    user_id=self.env.user.id,
)

# Send to AI API
response = client.messages.create(
    model="claude-3-5-sonnet",
    system=prompt,
    messages=[...],
    tools=tools,
)
```

## Debug Output

Every prompt build saves debug info to `ai_sam_base/data/debug_last_prompt.md`:

- Build timestamp
- Context data (JSON)
- Steps executed with character counts
- Tools passed to API
- Full system prompt text

## Migration Path

1. **Current**: `ai_brain._build_system_prompt()` - scattered, 400+ lines
2. **New**: `system_prompt_builder.build()` - consolidated, step-based
3. **Transition**: Both exist, gradually move to new builder
4. **Final**: Remove legacy `_build_system_prompt`, deprecate old prompt files

## Key Principles

1. **Single Source of Truth**: All prompt logic in ONE file
2. **Step-Based**: Clear, ordered components
3. **Static + Dynamic**: Identity is constant, context is injected
4. **Always Debuggable**: Every build saves debug output
5. **Tool Mandate First**: "USE YOUR TOOLS" is STEP 1, not buried in text

## The Problem We Solved

Before:
- Prompts scattered across 3+ files
- Unclear which file was used when
- Missing context due to code path differences
- SAM talked instead of using tools

After:
- ONE builder assembles everything
- Clear step sequence
- Tool mandate is first thing AI reads
- Debug output always available
