# Session Handover: SAM AI Page Builder Integration

**Date:** 2025-12-24
**Previous Session Focus:** Canvas connection rendering, workflow JSON format, planning-before-execution
**Next Session Goal:** Integrate SAM Chat Core with sam_ai_page_builder module

---

## Context Summary

### What Was Accomplished This Session

1. **Fixed Streaming Hang Issue**
   - Root cause: Emoji encoding (`🤖`) in logger causing Windows log handler to hang
   - Fix: Changed to `[SAM AI]` prefix in `ai_brain.py:2373`

2. **Canvas Planning-Before-Execution (Phase 6)**
   - Added WORKFLOW BUILDER MODE to system prompt when in canvas context
   - Updated `canvas_edit` and `canvas_create` tool descriptions for conversational approach
   - SAM now describes complete workflows conversationally before building (not node-by-node)
   - File: `ai_sam_base/models/ai_brain.py` (lines 1935-1996)
   - File: `ai_sam_base/models/canvas_tools.py` (tool descriptions updated)

3. **N8N JSON Connection Format Investigation**
   - Identified why connection lines weren't rendering when pasting workflows
   - Root cause: Node IDs must start with `node-` prefix for ID-based connection format
   - Descriptions go in `parameters.description`, not `notes`
   - Timing issues with connection dot rendering (300ms delay needed)

---

## The Vision: Sales Page Builder Workflow

User wants to create an end-to-end automation where:

1. **User prompts SAM** in chat: "Create a sales page for our CRM capabilities"
2. **SAM gathers content** from:
   - Current canvas nodes (content nodes with URLs, docs)
   - Centralized capability statements at `samai.sme.ec/blog/crm_capabilities`
3. **SAM AI processes** the content into sales copy
4. **Page Builder module** generates the HTML/CSS/JS
5. **User reviews** live preview
6. **User decides**: Publish, Revise, or Cancel
7. **If Revise**: Feedback loop back to AI processing

### Workflow JSON Created (12 nodes)
```
User Prompt → [Gather From Canvas + Fetch Capabilities] → Merge → AI Process
→ Page Builder Node → Show Preview → User Decision
    ├→ Publish → Success
    ├→ Revise → (loops back to AI Process)
    └→ Cancel → Confirmation
```

---

## Page Builder Module Status

**Location:** `D:\SAMAI-18-SaaS\github-repos\05-samai-core\sam_ai_page_builder`

### Current State (from sam_ai_page.py)
- Model: `sam.ai.page`
- Fields:
  - `name`, `description` - Basic info
  - `page_html`, `page_css`, `page_js` - Generated content
  - `ai_prompt_history` - JSON-encoded prompt/response history
  - `state` - draft/generated/published
  - `prompt_count`, `has_content` - Computed fields
- Methods:
  - `action_generate()` - Stub returning client action (needs AI integration)
  - `add_prompt_to_history()` - Stores prompt/response pairs
  - `get_prompt_history()`, `clear_prompt_history()` - History management

### What's Missing
1. **AI Integration**: `action_generate()` is a stub - needs real AI service call
2. **Chat Integration**: No connection to SAM Chat for conversational page building
3. **Preview System**: No live preview mechanism
4. **Publishing**: No actual deployment/URL generation
5. **Canvas Node**: No `page_builder_node` type in workflow canvas

---

## Next Session Tasks

### Priority 1: Connect SAM Chat to Page Builder

**Goal:** When user is in page builder context, SAM can generate pages through conversation.

**Approach:**
1. Add page builder context detection (similar to canvas context)
2. Add page builder tools to SAM's toolset:
   - `page_generate` - Generate page from description
   - `page_preview` - Show live preview
   - `page_publish` - Deploy the page
   - `page_revise` - Modify based on feedback
3. Wire up `ai_brain.py` to call page builder methods

### Priority 2: Implement Page Generation

**Goal:** Replace `action_generate()` stub with real AI-powered generation.

**Approach:**
1. Build system prompt for page generation (sales copy expert)
2. Call Claude API with:
   - User's prompt/description
   - Context from capability statements
   - Previous conversation history
3. Parse response into HTML/CSS/JS
4. Store in `sam.ai.page` record
5. Return preview URL

### Priority 3: Canvas Integration (page_builder_node)

**Goal:** Add a Page Builder node type to workflow canvas.

**Approach:**
1. Add to node registry (`node_metadata.json` or agent_nodes.json)
2. Create node that:
   - Accepts content input (from merge/AI nodes)
   - Calls page builder API
   - Outputs page URL or preview

---

## Key Files for Next Session

### Page Builder Module
- `sam_ai_page_builder/models/sam_ai_page.py` - Core model (needs AI integration)
- `sam_ai_page_builder/__manifest__.py` - Module manifest
- `sam_ai_page_builder/views/` - UI views (if any)

### SAM Chat Core
- `ai_sam_base/models/ai_brain.py` - Central orchestrator (add page builder context)
- `ai_sam_base/models/canvas_tools.py` - Tool definitions (add page builder tools)
- `ai_sam/static/src/js/sam_chat_vanilla_v2.js` - Frontend (add page preview handling)

### Capability Statements
- URL: `samai.sme.ec/blog/crm_capabilities`
- Purpose: Centralized knowledge base for all users/agents
- Format: Blog posts with capability descriptions

---

## Architectural Notes

### 4-Layer Learning Architecture (Discussed)
1. **LLM Layer** (Claude) - General intelligence
2. **Odoo Expertise Layer** - Domain knowledge (trained/prompted)
3. **Customization Training** - User-specific workflows
4. **User Learning** (Scikit-learn) - Pattern recognition from user behavior

### Platform Skin Architecture
- All data models in `ai_sam_base`
- UI/experience in `ai_sam` and platform-specific modules
- Page builder follows this pattern

---

## Suggested Starting Point

```
/sam_core_chat

Focus: Integrate SAM Chat with sam_ai_page_builder module.

Tasks:
1. Read sam_ai_page_builder module structure
2. Add page builder context detection to ai_brain.py
3. Create page generation tools (page_generate, page_preview, page_publish)
4. Implement real AI generation in sam_ai_page.py
5. Test end-to-end: User prompt → AI generates → Preview → Publish
```

---

## Reference: Corrected N8N JSON Format

For creating workflows with connections that render properly:

```json
{
  "nodes": [
    {
      "id": "node-001",  // MUST start with "node-"
      "name": "Node Name",
      "type": "n8n-nodes-base.httpRequest",
      "position": [100, 200],
      "parameters": {
        "description": "Description goes here"  // NOT "notes"
      }
    }
  ],
  "connections": {
    "node-001": {  // Use node ID as key
      "main": [[{
        "node": "Target Name",
        "nodeId": "node-002",  // Include both name AND nodeId
        "type": "main",
        "index": 0
      }]]
    }
  }
}
```

---

## Questions for Next Session

1. Should page builder have its own conversation type or use general SAM chat?
2. Where should generated pages be hosted? (Odoo website module? Static files? External?)
3. Should capability statements be fetched live or cached?
4. What's the publish workflow? (Draft → Review → Publish with URL?)

---

*Handover created: 2025-12-24*
*Previous session token usage: ~150-200k (estimated)*
