# SAM AI System Layers - Defining Lines Document

## Purpose
This document defines the horizontal architectural layers of SAM AI. Each layer represents a distinct responsibility boundary. Code and documentation should map cleanly to these layers.

Use this document to:
- Validate documentation covers all layers
- Identify orphan code that doesn't fit any layer
- Guide new development into the correct layer
- Audit system completeness

---

## Layer Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         LAYER 1: API MANAGEMENT                     │
│  External API interfaces, provider abstraction, key management      │
├─────────────────────────────────────────────────────────────────────┤
│                      LAYER 2: LOCATION MANAGEMENT                   │
│  Context detection, page awareness, Odoo location introspection     │
├─────────────────────────────────────────────────────────────────────┤
│                LAYER 3: DYNAMIC SYSTEM PROMPT CREATION              │
│  Prompt assembly, mode selection, personality injection             │
├─────────────────────────────────────────────────────────────────────┤
│                     LAYER 4: RESPONSE MANAGEMENT                    │
│  AI response handling, streaming, formatting, error recovery        │
├─────────────────────────────────────────────────────────────────────┤
│                   LAYER 5: SESSION & CONVERSATION                   │
│  Chat history, session state, conversation threading                │
├─────────────────────────────────────────────────────────────────────┤
│                    LAYER 6: MEMORY & KNOWLEDGE                      │
│  Persistent storage, vector DB, knowledge retrieval                 │
├─────────────────────────────────────────────────────────────────────┤
│                  LAYER 7: AUTHENTICATION & SECURITY                 │
│  OAuth, credentials, API key storage, user permissions              │
├─────────────────────────────────────────────────────────────────────┤
│                      LAYER 8: UI & FRONTEND                         │
│  Chat bubble, OWL components, CSS, user interactions                │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Layer Definitions

### LAYER 1: API MANAGEMENT
**Responsibility:** External AI provider communication

**Includes:**
- API key validation and storage
- Provider abstraction (Anthropic, OpenAI, etc.)
- Request/response transformation
- Rate limiting, retry logic
- Provider health checking

**Expected Code Locations:**
- `ai_sam_base/models/api_*.py`
- `ai_sam_base/models/ai_provider*.py`
- `ai_sam/controllers/api_*.py`

**Documentation Section:** `05_architecture/api_*.md`

---

### LAYER 2: LOCATION MANAGEMENT
**Responsibility:** Understanding WHERE in Odoo the user is

**Includes:**
- Current page/view detection
- Active record context
- Menu/app awareness
- Breadcrumb extraction
- Action context parsing

**Expected Code Locations:**
- `ai_sam_base/models/location_*.py`
- `ai_sam/static/src/*/location*.js`

**Documentation Section:** `05_architecture/location_*.md`

---

### LAYER 3: DYNAMIC SYSTEM PROMPT CREATION
**Responsibility:** Building the right prompt for the context

**Includes:**
- Mode selection (general, page_builder, workflow)
- Personality injection
- Context-aware prompt assembly
- System knowledge inclusion
- Prompt templates

**Expected Code Locations:**
- `ai_sam_base/models/prompt_*.py`
- `ai_sam_base/models/sam_mode*.py`
- `ai_sam_base/data/*.md` (prompt templates)

**Documentation Section:** `03_prompt_engineering/`

---

### LAYER 4: RESPONSE MANAGEMENT
**Responsibility:** Handling what comes back from AI

**Includes:**
- Response streaming
- Markdown rendering
- Error handling and recovery
- Response formatting
- Action extraction (if AI suggests actions)

**Expected Code Locations:**
- `ai_sam/controllers/chat*.py`
- `ai_sam/static/src/chat_ui/*.js`

**Documentation Section:** `05_architecture/response_*.md`

---

### LAYER 5: SESSION & CONVERSATION
**Responsibility:** Maintaining conversation state

**Includes:**
- Chat session creation/retrieval
- Message history storage
- Conversation threading
- Session cleanup/archival
- Cross-tab session sync

**Expected Code Locations:**
- `ai_sam_base/models/sam_session*.py`
- `ai_sam_base/models/sam_message*.py`

**Documentation Section:** `05_architecture/session_*.md`, `06_data_flows/`

---

### LAYER 6: MEMORY & KNOWLEDGE
**Responsibility:** Long-term memory and retrieval

**Includes:**
- Vector database integration (ChromaDB)
- Knowledge embedding
- Semantic search
- Memory persistence
- Knowledge graph (future)

**Expected Code Locations:**
- `ai_sam_intelligence/models/*.py`
- `ai_sam_base/models/memory*.py`

**Documentation Section:** `05_architecture/memory_*.md`, `05_architecture/knowledge_*.md`

---

### LAYER 7: AUTHENTICATION & SECURITY
**Responsibility:** Access control and credential management

**Includes:**
- OAuth provider integration
- API key encryption/storage
- User permission checking
- Secure credential retrieval
- Audit logging

**Expected Code Locations:**
- `ai_sam_base/models/credentials*.py`
- `ai_sam_base/models/oauth*.py`
- `ai_sam/security/*.xml`

**Documentation Section:** `05_architecture/auth_*.md`, `05_architecture/oauth_*.md`

---

### LAYER 8: UI & FRONTEND
**Responsibility:** User-facing interface

**Includes:**
- Chat bubble component
- Message rendering
- Input handling
- CSS/styling
- Menu integration
- Animations/UX

**Expected Code Locations:**
- `ai_sam/static/src/chat_ui/`
- `ai_sam/static/src/components/`
- `ai_sam/static/src/css/`
- `ai_sam/views/*.xml`

**Documentation Section:** `04_modules/ai_sam/`

---

## Validation Checklist

For each layer, verify:

| Layer | Code Exists | Docs Exist | Docs Accurate | Coverage % |
|-------|-------------|------------|---------------|------------|
| 1. API Management | ⬜ | ⬜ | ⬜ | ___% |
| 2. Location Management | ⬜ | ⬜ | ⬜ | ___% |
| 3. Dynamic Prompts | ⬜ | ⬜ | ⬜ | ___% |
| 4. Response Management | ⬜ | ⬜ | ⬜ | ___% |
| 5. Session/Conversation | ⬜ | ⬜ | ⬜ | ___% |
| 6. Memory/Knowledge | ⬜ | ⬜ | ⬜ | ___% |
| 7. Auth/Security | ⬜ | ⬜ | ⬜ | ___% |
| 8. UI/Frontend | ⬜ | ⬜ | ⬜ | ___% |

---

## Orphan Detection

Code that doesn't fit any layer may indicate:
- Missing layer definition (add new layer)
- Misplaced code (refactor needed)
- Dead code (delete candidate)

---

## Version History

| Date | Author | Changes |
|------|--------|---------|
| 2026-01-03 | Claude | Initial 8-layer architecture defined |

---

## Notes for Auditors

When auditing this document:
1. Run the `code_to_docs_validator.py` tool
2. Review the gap analysis report
3. Update coverage percentages
4. Flag any orphan code or missing layers
5. Update this document if layers need adjustment
