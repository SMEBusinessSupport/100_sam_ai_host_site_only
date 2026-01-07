# SAM AI V3 - Complete System Architecture

**Version:** 3.5.0
**Date:** October 2025
**Author:** Anthony Gardiner & Claude AI

---

## 🎯 Executive Summary

**SAM AI** is an intelligent framework for Odoo 18 that provides:

- 🤖 **AI Chat Interface** - Claude API integration with context awareness
- 🧠 **Multi-User Profiles** - Relationship-based AI interactions
- 🎨 **Universal Canvas System** - Polymorphic workflow/mind-map platform
- 💾 **Memory System** - Graph database (Apache AGE) + Vector database (ChromaDB)
- 🔄 **Workflow Automation** - N8N-compatible node-based workflows
- 🎯 **Power Prompts** - Context-aware AI modes (dev, sales, marketing, etc.)

---

## 🏗️ Architecture Overview

### Three-Layer Architecture

```
┌─────────────────────────────────────────────────────┐
│              🌿 BRANCHES (Specialized Features)     │
│  ┌──────────┐  ┌──────────┐  ┌──────────────────┐  │
│  │  Poppy   │  │  Memory  │  │   Automator      │  │
│  │ Mind Map │  │  System  │  │  (Workflows)     │  │
│  └──────────┘  └──────────┘  └──────────────────┘  │
└─────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────┐
│       🧠 AI_SAM (Framework - Core Intelligence)     │
│  ┌──────────────────────────────────────────────┐  │
│  │  • Canvas Engine (Universal Platform)        │  │
│  │  • Claude API Integration                    │  │
│  │  • Context Builder (All-Knowing Brain)       │  │
│  │  │  • Controllers & APIs                     │  │
│  │  • Token Counter & Cost Tracking            │  │
│  └──────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────┐
│         💾 AI_BRAIN (Data Layer - Foundation)       │
│  ┌──────────────────────────────────────────────┐  │
│  │  • All Data Models                           │  │
│  │  • Conversation Storage                      │  │
│  │  • User Profiles                             │  │
│  │  • Workflow Definitions                      │  │
│  │  • Node Registry                             │  │
│  └──────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────┘
```

### Module Breakdown

#### 1. **ai_brain** (Data Layer)
**Location:** `C:\Working With AI\ai_sam\ai_sam_odoo\ai_brain`

**Purpose:** Pure data layer - contains ALL data models with NO views

**Key Models:**
- `ai.service.config` - API configuration
- `ai.conversation` - Chat threads
- `ai.message` - Individual messages
- `ai.token.usage` - Usage tracking
- `sam.user.profile` - User relationship profiles
- `sam.user.settings` - User preferences
- `sam.mode.context` - Power Prompts
- `ai.branch` - Branch registry (meta-architecture)
- `canvas` - Universal workflow/canvas storage
- `nodes` - Node definitions
- `connections` - Node connections
- `executions` - Execution history
- `ai.memory.config` - Memory system config
- `ai.extractor.plugin` - Learned extraction patterns

#### 2. **ai_sam** (Framework Layer)
**Location:** `C:\Working With AI\ai_sam\ai_sam_odoo\ai_sam`

**Purpose:** Framework + Intelligence + UI

**Key Components:**

**Controllers:**
- `sam_ai_chat_controller.py` - Chat endpoints
- `sam_session_controller.py` - Session management
- `sam_developer_mode.py` - Developer tools
- `skeleton_canvas_controller.py` - Canvas API
- `memory_graph_controller.py` - Memory system API

**Services:**
- `ai_service.py` - Claude API integration
- `ai_context_builder.py` - All-knowing context builder
- `ai_voice_service.py` - Whisper integration
- `ai_registry_watcher.py` - Module monitor

**JavaScript (Frontend):**
- `sam_ai_chat_widget.js` - Global chat widget
- `sam_ai_token_counter.js` - Token/cost display
- `skeleton_canvas_engine.js` - Canvas core
- `platform_loader.js` - Dynamic platform loading
- `poppy_node_renderer.js` - Poppy platform
- `memory_graph_renderer.js` - Memory visualization

#### 3. **Branches** (Specialized Features)

Branches are dynamically registered via `ai.branch` model:

**Poppy** (Mind Mapping):
- Merged into `ai_sam`
- Freeform canvas with multimedia
- AI chat panel integration

**Memory System**:
- Graph database (Apache AGE)
- Vector database (ChromaDB)
- Conversation import
- Knowledge graph visualization

**Automator** (Workflows):
- N8N-compatible workflows
- 1,500+ service connectors
- Visual workflow canvas
- Execution engine

---

## 💾 Database Schema

### Core SAM AI Tables

#### AI Service & Configuration
```sql
ai_service_config
├── api_provider (anthropic, openai, local)
├── api_key (encrypted)
├── model_name (claude-3-5-sonnet-20241022)
├── max_tokens, temperature, top_p
├── total_requests, total_tokens_used, total_cost
└── credit_balance, remaining_balance

ai_service_provider
├── provider_type (whisper, heygen, neo3)
├── api_endpoint, api_key
├── capabilities (JSON)
└── usage statistics
```

#### Conversations & Messages
```sql
ai_conversation
├── user_id → res_users
├── context_model, context_id (polymorphic link to ANY model)
├── conversation_type (general, help, debug, build, analysis)
├── status (active, waiting, completed, archived)
└── message_count, total_tokens, total_cost

ai_message
├── conversation_id → ai_conversation
├── role (user, assistant, system)
├── content (TEXT)
├── ai_model, ai_provider
├── token_count, response_time_ms
└── artifact_type, artifact_content (for code/diagrams)

ai_token_usage
├── provider, model_name
├── input_tokens, output_tokens, total_tokens
├── cost_usd
├── conversation_id
└── timestamp
```

#### User Profiles & Settings
```sql
sam_user_profile
├── user_id → res_users (UNIQUE)
├── display_name, preferred_name
├── relationship_level (stranger → close_friend)
├── trust_score (0-100)
├── personal_facts (JSON: learned information)
├── preferred_tone, emoji_preference, working_style
└── interaction_count, last_interaction

sam_user_settings
├── user_id → res_users (UNIQUE)
├── active_mode (dev, sales, marketing, general)
├── creator_mode (BOOLEAN)
├── whitelisted_paths (JSON: for local file access)
└── UI preferences (theme, show_token_counter, auto_save)

sam_mode_context (Power Prompts)
├── mode_key (UNIQUE: 'dev', 'sales', 'marketing')
├── mode_name, description
├── system_prompt (TEXT: additional instructions)
├── context_rules (JSON)
├── icon, color
└── requires_local, requires_creator_mode
```

#### Branch System (Meta-Architecture)
```sql
ai_branch
├── name, technical_name (UNIQUE)
├── code (short identifier)
├── icon, color, description
├── sequence, active, is_core
├── module_name, module_installed
├── canvas_type (node_based, freeform, grid, timeline)
├── platform_renderer (JS renderer name)
└── supports_ai_chat, supports_export, supports_collaboration
```

#### Canvas & Workflows
```sql
canvas (Universal Platform)
├── name, description, active
├── branch_type → ai_branch (polymorphic)
├── canvas_type (node_based, freeform, grid, timeline, board)
├── business_unit_id, workflow_type_id
├── json_definition (N8N-compatible JSON)
├── generated_python_code, generated_javascript_code
├── execution_mode (manual, trigger, scheduled, webhook)
├── cron_expression, webhook_url
└── visibility (private, team, company, public)

nodes
├── node_id (VARCHAR: 'node_1', 'node_2')
├── name, type, sequence
├── canvas_id → canvas
├── node_type_id → n8n_node_types
├── parameters (JSON)
├── x_cord, y_cord (position)
├── retry_on_failure, max_retries
└── input_connections, output_connections (JSON)

connections
├── canvas_id → canvas
├── from_node_id → nodes
├── to_node_id → nodes
├── cnct_from, cnct_to (connection points)
├── connection_type (data, trigger, error)
└── properties (JSON)

executions
├── canvas_id → canvas
├── state (pending, running, completed, failed, cancelled)
├── start_time, end_time, duration
├── trigger_type (manual, webhook, schedule)
├── triggered_by → res_users
├── input_data, output_data, execution_log (JSON)
├── error_message, error_node_id
└── nodes_executed, nodes_total
```

#### Memory System
```sql
ai_memory_config
├── graph_enabled (Apache AGE)
├── graph_host, graph_port, graph_database, graph_name
├── vector_enabled (ChromaDB)
├── vector_host, vector_port, collection_name
├── embedding_model, embedding_dimensions
└── total_nodes, total_edges, total_vectors

ai_extractor_plugin (Learned Patterns)
├── name, description
├── entity_type (person, company, project, concept)
├── extraction_prompt, sample_text, expected_output
├── success_rate, usage_count
└── active, is_system
```

#### Supporting Tables
```sql
workflow_business_unit
├── name, code, description

workflow_types
├── name, display_name, category
├── default_settings, allowed_triggers (JSON)
├── template_json

workflow_template
├── name, display_name, category
├── json_definition (N8N template)
├── author_id, version, tags (JSON)
└── usage_count, is_public

n8n_node_types (Simplified)
├── display_name, folder_name, n8n_type
├── category, description
├── has_icon, icon_path
├── requires_credentials, credential_types (JSON)
└── active

api_credentials
├── name, credential_type, service_name
├── credential_data (encrypted JSON)
├── OAuth2 fields (client_id, access_token, refresh_token)
├── API Key fields (api_key, api_secret, api_endpoint)
├── Username/Password fields
└── is_valid, last_tested
```

---

## 🔄 Data Flow Patterns

### 1. User Sends Message to SAM

```
1. Frontend (sam_ai_chat_widget.js)
   └── POST /sam_ai/chat/send
       {message, conversation_id, context_data, environment}

2. Controller (sam_ai_chat_controller.py)
   └── ai.service.send_message()

3. Service Layer (ai_service.py)
   ├── Load sam.user.profile (multi-user)
   ├── Get ai.service.config
   ├── Build context (ai.context.builder)
   ├── Get conversation history (ai.conversation)
   ├── Add user message (ai.message)
   ├── Build system prompt with:
   │   ├── Base system prompt (from file or DB)
   │   ├── User context (profile, preferences, facts)
   │   ├── Power Prompt (if active_mode set)
   │   └── Environment capabilities (local/prod, whitelisted paths)
   ├── Call Claude API
   ├── Save assistant message (ai.message)
   ├── Log token usage (ai.token.usage)
   └── Update profile interaction count

4. Response
   └── {success, message, tokens, cost, user_profile}
```

### 2. Context Builder (All-Knowing Brain)

```
ai.context.builder.build_context_prompt({
    model: 'canvas',
    record_id: 42,
    include_system: True
})

Builds:
┌─────────────────────────────────────┐
│  SYSTEM OVERVIEW                    │
│  ├── Installed modules              │
│  ├── Active AI branches             │
│  └── Database info                  │
├─────────────────────────────────────┤
│  CURRENT CONTEXT                    │
│  ├── Model & record details         │
│  ├── Field values                   │
│  └── Related records                │
├─────────────────────────────────────┤
│  USER CONTEXT                       │
│  ├── Current user info              │
│  ├── Company context                │
│  └── Language & timezone            │
└─────────────────────────────────────┘
```

### 3. Power Prompt System

```
User sets mode: sam.user.settings.active_mode = 'dev'

When sending message:
1. Load base system prompt (SAM_AI_MASTER_SYSTEM_PROMPT_V2.md)
2. Inject user context (profile, preferences, facts)
3. Append Power Prompt for 'dev' mode from sam.mode.context
4. Add environment capabilities
5. Send to Claude API

Result: SAM operates in specialized 'dev' mode with enhanced coding abilities
```

### 4. Canvas Platform Loading (Skeleton System)

```
User opens canvas:
1. skeleton_canvas_engine.js loads
2. Reads canvas.branch_type (e.g., 'poppy')
3. Looks up ai.branch by technical_name
4. Gets platform_renderer (e.g., 'poppy_node_renderer')
5. platform_loader.js dynamically loads:
   ├── poppy_node_renderer.js
   ├── poppy_toolbar.js
   ├── poppy_sidebar.js
   └── poppy_canvas_styles.css
6. Renderer takes over and displays content
```

---

## 🎯 Key Features & Capabilities

### 1. Multi-User Relationship System

SAM builds a relationship with each user over time:

- **Stranger** → **Acquaintance** → **Colleague** → **Friend** → **Close Friend**
- Trust score (0-100) auto-calculated based on interactions
- Personal facts stored (family, interests, work role)
- Preferences learned (tone, emoji, working style)
- Memory permissions (what SAM can remember)

### 2. Environment-Aware AI

SAM adapts behavior based on environment:

**Local Mode:**
- File system access (whitelisted paths)
- Development tools available
- Creator mode for editing Power Prompts

**Production Mode:**
- Restricted file access
- Security-focused responses
- Read-only Power Prompts

### 3. Power Prompts (Mode Context)

Specialized AI modes with enhanced capabilities:

- **Dev Mode:** Code generation, debugging, architecture
- **Sales Mode:** CRM optimization, lead nurturing, proposals
- **Marketing Mode:** Content creation, campaign planning
- **Support Mode:** Customer service, troubleshooting
- **General Mode:** Default SAM behavior

### 4. Universal Canvas System

One canvas platform, multiple content types:

- **Workflows** (node_based): N8N-style automation
- **Mind Maps** (freeform): Poppy platform
- **Process Designer** (grid): Business process modeling
- **Timeline** (timeline): Project planning
- **Board** (board): Kanban-style boards

New types = new `ai.branch` records (no code changes)

### 5. Memory System

**Graph Database (Apache AGE):**
- Knowledge graph of entities and relationships
- Person → works_at → Company
- Project → uses → Technology
- Conversation → mentions → Topic

**Vector Database (ChromaDB):**
- Semantic search across conversations
- Find similar discussions
- Context retrieval for AI

---

## 🚀 API Endpoints

### Chat & Conversations
```
POST   /sam_ai/chat/send              # Send message
POST   /sam_ai/chat/history           # Get conversation history
POST   /sam_ai/chat/conversations     # Get user's conversations
POST   /sam_ai/chat/new               # Create new conversation
POST   /sam_ai/chat/health            # Check system health
```

### Voice & Transcription
```
POST   /sam_ai/voice/transcribe       # Voice to text (Whisper)
```

### Mode Management
```
POST   /sam/user/set_mode             # Set active mode
POST   /sam/modes/get_available       # Get available modes
```

### Context Parsing
```
POST   /sam_ai/context/parse          # Parse Odoo URL for context
```

### Canvas & Platform
```
GET    /canvas/<int:id>/load          # Load canvas data
POST   /canvas/<int:id>/save          # Save canvas
POST   /canvas/<int:id>/nodes/save    # Save nodes
```

### Memory System
```
POST   /memory/graph/query            # Query knowledge graph
POST   /memory/vector/search          # Semantic search
POST   /memory/import/conversations   # Import conversations
```

---

## 📊 Performance & Optimization

### Token Management
- Pre-call token estimation (needs tiktoken integration)
- Smart context window management
- Conversation history pruning based on tokens, not message count
- Cost tracking per conversation

### Caching Strategy
- Redis/memcached for frequent queries
- Conversation history caching
- Node type registry caching
- User profile caching

### Database Optimization
- Indexed foreign keys
- Computed fields for statistics
- Materialized views for reporting
- Batch operations for context building

---

## 🔒 Security Considerations

### API Security
- Encrypted credential storage
- Token-based authentication
- Rate limiting per user (needs implementation)
- Whitelisted file paths for local access

### User Privacy
- Multi-user profile isolation
- Memory permission levels
- Trust-based feature access
- Conversation archiving

### Data Protection
- Encrypted API keys
- Secure credential management
- OAuth2 token refresh
- SSL/TLS for API calls

---

## 📁 File Structure

```
ai_sam_odoo/
├── ai_brain/                           # Data Layer
│   ├── models/
│   │   ├── ai_service.py               # Claude API integration
│   │   ├── ai_context_builder.py       # All-knowing brain
│   │   ├── ai_conversation.py          # Conversations
│   │   ├── ai_message.py               # Messages
│   │   ├── sam_user_profile.py         # User profiles
│   │   ├── sam_user_settings.py        # User settings
│   │   ├── sam_mode_context.py         # Power Prompts
│   │   ├── ai_branches.py              # Branch registry
│   │   ├── canvas.py                   # Canvas model
│   │   ├── nodes.py                    # Nodes
│   │   ├── connections.py              # Connections
│   │   ├── executions.py               # Executions
│   │   ├── ai_memory_config.py         # Memory config
│   │   └── ... (40+ models)
│   ├── data/
│   │   └── SAM_AI_MASTER_SYSTEM_PROMPT_V2.md
│   └── security/
│       └── ir.model.access.csv
│
├── ai_sam/                             # Framework Layer
│   ├── controllers/
│   │   ├── sam_ai_chat_controller.py   # Chat API
│   │   ├── skeleton_canvas_controller.py # Canvas API
│   │   └── memory_graph_controller.py  # Memory API
│   ├── static/src/
│   │   ├── config/
│   │   │   └── sam_config.js           # Global config
│   │   ├── core/
│   │   │   ├── skeleton_canvas_engine.js # Canvas core
│   │   │   └── platform_loader.js      # Dynamic loading
│   │   ├── js/
│   │   │   ├── sam_ai_chat_widget.js   # Global chat
│   │   │   ├── sam_ai_token_counter.js # Token display
│   │   │   ├── poppy_node_renderer.js  # Poppy platform
│   │   │   └── memory_graph_renderer.js # Memory viz
│   │   └── css/
│   │       ├── sam_ai_chat_widget.css
│   │       └── skeleton_base.css
│   ├── views/
│   │   ├── sam_ai_chat_view.xml
│   │   ├── skeleton_canvas_container.xml
│   │   └── ... (20+ views)
│   └── __manifest__.py
│
└── claudes floating files/             # New files go here
    ├── bat/
    ├── json/
    ├── misc/
    ├── py/
    └── xml/
```

---

## 🔮 Future Enhancements

### Immediate Priorities (From Code Review)
1. Implement tiktoken for accurate token estimation
2. Add retry logic with exponential backoff
3. Smart context window management (token-based)
4. Response caching layer (Redis/memcached)
5. Rate limiting on API endpoints
6. Trust score features (file access, context length)
7. JSON Schema validation for workflows
8. Batch operations in context builder
9. SQL injection audit

### Long-term Roadmap
- Real-time collaboration on canvas
- Workflow marketplace
- Multi-language support
- Mobile app integration
- Advanced memory querying
- Custom AI model support
- Workflow versioning & rollback

---

## 📚 Related Documentation

- **Database Schema:** `SAM_AI_V3_DATABASE_SCHEMA.sql`
- **System Prompt:** `ai_brain/data/SAM_AI_MASTER_SYSTEM_PROMPT_V2.md`
- **API Documentation:** (To be created)
- **User Guide:** (To be created)

---

## 🤝 Contributing

**Module Structure:**
- `ai_brain` = Data models only (NO views, NO controllers)
- `ai_sam` = Framework, views, controllers, JavaScript
- New branches = New `ai.branch` records + optional dedicated module

**File Creation Policy:**
- Only create files when absolutely necessary
- New files go to: `claudes floating files/` organized by type
- No random files in module directories

**Code Standards:**
- Follow Odoo coding guidelines
- Use type hints in Python
- Document all models and methods
- Keep controllers thin, business logic in models
- Test before committing

---

**Last Updated:** October 9, 2025
**Architecture Version:** 3.5.0
**Maintained by:** Anthony Gardiner & Claude AI
