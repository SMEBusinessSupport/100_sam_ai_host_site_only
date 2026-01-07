# Sam Ai V3 Database Schema

**Original file:** `SAM_AI_V3_DATABASE_SCHEMA.sql`
**Type:** SQL

---

```sql
-- ============================================================================
-- SAM AI V3 - COMPREHENSIVE DATABASE SCHEMA
-- PostgreSQL DDL Documentation
-- Version: 3.5.0
-- Date: 2025-10-09
-- Architecture: ai_brain (data) → ai_sam (framework) → branches
-- ============================================================================

-- ============================================================================
-- CORE SAM AI MODELS (ai_brain module)
-- ============================================================================

-- ============================================================================
-- AI SERVICE CONFIGURATION
-- ============================================================================
CREATE TABLE IF NOT EXISTS ai_service_config (
    id SERIAL PRIMARY KEY,

    -- Basic Configuration
    name VARCHAR(255) NOT NULL,
    active BOOLEAN DEFAULT TRUE,

    -- API Provider
    api_provider VARCHAR(50) DEFAULT 'anthropic', -- anthropic, openai, local
    api_endpoint VARCHAR(500) DEFAULT 'https://api.anthropic.com/v1/messages',
    api_key TEXT, -- Encrypted

    -- Model Configuration
    claude_model VARCHAR(100) DEFAULT 'claude-3-5-sonnet-20241022',
    openai_model VARCHAR(100),
    local_model_name VARCHAR(100),
    model_name VARCHAR(100), -- Active model (computed)

    -- Generation Parameters
    max_tokens INTEGER DEFAULT 4096,
    temperature FLOAT DEFAULT 0.7,
    top_p FLOAT DEFAULT 1.0,

    -- System Prompt
    system_prompt TEXT,

    -- Usage Statistics
    total_requests INTEGER DEFAULT 0,
    total_tokens_used BIGINT DEFAULT 0,
    total_cost FLOAT DEFAULT 0.0,
    last_request_date TIMESTAMP,

    -- Credit Balance Tracking
    credit_balance FLOAT DEFAULT 0.0,
    remaining_balance FLOAT DEFAULT 0.0,
    balance_percentage FLOAT DEFAULT 0.0,

    -- Odoo System Fields
    create_uid INTEGER,
    create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    write_uid INTEGER,
    write_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_ai_service_config_active ON ai_service_config(active);
CREATE INDEX idx_ai_service_config_provider ON ai_service_config(api_provider);

-- ============================================================================
-- AI SERVICE PROVIDER (Multi-AI Orchestration)
-- ============================================================================
CREATE TABLE IF NOT EXISTS ai_service_provider (
    id SERIAL PRIMARY KEY,

    -- Provider Information
    name VARCHAR(255) NOT NULL,
    provider_type VARCHAR(50) NOT NULL, -- whisper, heygen, neo3, etc.
    api_endpoint VARCHAR(500),
    api_key TEXT, -- Encrypted

    -- Configuration
    config_json TEXT, -- Provider-specific config
    active BOOLEAN DEFAULT TRUE,

    -- Capabilities
    capabilities TEXT, -- JSON: ["transcription", "translation"]
    supported_formats TEXT, -- JSON: ["mp3", "wav", "m4a"]

    -- Usage Statistics
    total_requests INTEGER DEFAULT 0,
    total_cost FLOAT DEFAULT 0.0,
    last_used TIMESTAMP,

    -- Odoo System Fields
    create_uid INTEGER,
    create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    write_uid INTEGER,
    write_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_ai_service_provider_type ON ai_service_provider(provider_type);
CREATE INDEX idx_ai_service_provider_active ON ai_service_provider(active);

-- ============================================================================
-- AI CONVERSATION (Chat Threads)
-- ============================================================================
CREATE TABLE IF NOT EXISTS ai_conversation (
    id SERIAL PRIMARY KEY,

    -- Basic Information
    name VARCHAR(255) NOT NULL DEFAULT 'New Conversation',
    active BOOLEAN DEFAULT TRUE,

    -- User & Ownership
    user_id INTEGER NOT NULL REFERENCES res_users(id),
    company_id INTEGER REFERENCES res_company(id),

    -- Polymorphic Context (can link to ANY Odoo model)
    context_model VARCHAR(100), -- e.g., 'canvas', 'res.partner'
    context_id INTEGER, -- Record ID
    context_description VARCHAR(500), -- Computed description

    -- Conversation Type
    conversation_type VARCHAR(50) DEFAULT 'general',
    -- general, help, debug, build, analysis, explain

    -- Status
    status VARCHAR(50) DEFAULT 'active',
    -- active, waiting, completed, archived

    -- Statistics (computed)
    message_count INTEGER DEFAULT 0,
    total_tokens INTEGER DEFAULT 0,
    total_cost FLOAT DEFAULT 0.0,
    last_message_date TIMESTAMP,

    -- Odoo System Fields
    create_uid INTEGER,
    create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    write_uid INTEGER,
    write_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_ai_conversation_user ON ai_conversation(user_id);
CREATE INDEX idx_ai_conversation_context ON ai_conversation(context_model, context_id);
CREATE INDEX idx_ai_conversation_type ON ai_conversation(conversation_type);
CREATE INDEX idx_ai_conversation_status ON ai_conversation(status);

-- ============================================================================
-- AI MESSAGE (Individual Chat Messages)
-- ============================================================================
CREATE TABLE IF NOT EXISTS ai_message (
    id SERIAL PRIMARY KEY,

    -- Conversation Link
    conversation_id INTEGER NOT NULL REFERENCES ai_conversation(id) ON DELETE CASCADE,

    -- Message Content
    role VARCHAR(50) NOT NULL, -- user, assistant, system
    content TEXT NOT NULL,

    -- AI Model Used (for assistant messages)
    ai_model VARCHAR(100),
    ai_provider VARCHAR(50),

    -- Performance Metrics
    token_count INTEGER DEFAULT 0,
    response_time_ms INTEGER, -- Response time in milliseconds

    -- Artifacts (for code/diagrams generated)
    has_artifact BOOLEAN DEFAULT FALSE,
    artifact_type VARCHAR(50), -- code, diagram, table, etc.
    artifact_content TEXT,

    -- Odoo System Fields
    create_uid INTEGER,
    create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    write_uid INTEGER,
    write_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_ai_message_conversation ON ai_message(conversation_id);
CREATE INDEX idx_ai_message_role ON ai_message(role);
CREATE INDEX idx_ai_message_created ON ai_message(create_date);

-- ============================================================================
-- AI TOKEN USAGE (Usage Tracking)
-- ============================================================================
CREATE TABLE IF NOT EXISTS ai_token_usage (
    id SERIAL PRIMARY KEY,

    -- Provider & Model
    provider VARCHAR(50) NOT NULL,
    model_name VARCHAR(100) NOT NULL,

    -- Token Counts
    input_tokens INTEGER DEFAULT 0,
    output_tokens INTEGER DEFAULT 0,
    total_tokens INTEGER DEFAULT 0,

    -- Cost Calculation
    cost_usd FLOAT DEFAULT 0.0,

    -- Context Information
    conversation_id INTEGER REFERENCES ai_conversation(id),
    context_model VARCHAR(100),
    context_id INTEGER,

    -- Performance
    response_time_ms INTEGER,

    -- Timestamp
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- Odoo System Fields
    create_uid INTEGER,
    create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_ai_token_usage_provider ON ai_token_usage(provider);
CREATE INDEX idx_ai_token_usage_conversation ON ai_token_usage(conversation_id);
CREATE INDEX idx_ai_token_usage_timestamp ON ai_token_usage(timestamp);

-- ============================================================================
-- AI ARTIFACT VERSION (Version History)
-- ============================================================================
CREATE TABLE IF NOT EXISTS ai_artifact_version (
    id SERIAL PRIMARY KEY,

    -- Artifact Information
    artifact_id VARCHAR(100) NOT NULL,
    version INTEGER NOT NULL,

    -- Content
    artifact_type VARCHAR(50), -- code, diagram, document
    content TEXT,
    language VARCHAR(50), -- python, javascript, mermaid, etc.

    -- Associated Message
    message_id INTEGER REFERENCES ai_message(id),
    conversation_id INTEGER REFERENCES ai_conversation(id),

    -- Metadata
    title VARCHAR(255),
    description TEXT,

    -- Odoo System Fields
    create_uid INTEGER,
    create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT unique_artifact_version UNIQUE(artifact_id, version)
);

CREATE INDEX idx_ai_artifact_version_id ON ai_artifact_version(artifact_id);
CREATE INDEX idx_ai_artifact_version_type ON ai_artifact_version(artifact_type);

-- ============================================================================
-- SAM USER PROFILE (Multi-User Relationship Layer)
-- ============================================================================
CREATE TABLE IF NOT EXISTS sam_user_profile (
    id SERIAL PRIMARY KEY,

    -- Core Identity
    user_id INTEGER NOT NULL REFERENCES res_users(id) ON DELETE CASCADE,
    display_name VARCHAR(255), -- Computed
    preferred_name VARCHAR(100), -- e.g., "AG", "Tony"

    -- Relationship Level
    relationship_level VARCHAR(50) DEFAULT 'stranger',
    -- stranger, acquaintance, colleague, friend, close_friend
    trust_score INTEGER DEFAULT 0, -- 0-100
    interaction_count INTEGER DEFAULT 0,

    -- Personal Context (What SAM Knows)
    personal_facts TEXT, -- JSON: learned facts
    family_info TEXT,
    interests VARCHAR(500),
    work_role VARCHAR(255),

    -- User Preferences
    preferred_tone VARCHAR(50) DEFAULT 'adaptive',
    emoji_preference VARCHAR(50) DEFAULT 'normal',
    working_style VARCHAR(50) DEFAULT 'balanced',

    -- Memory Permissions
    memory_permission VARCHAR(50) DEFAULT 'basic',
    -- none, basic, full
    can_access_personal_memory BOOLEAN DEFAULT FALSE,

    -- Statistics
    first_interaction TIMESTAMP,
    last_interaction TIMESTAMP,
    total_conversations INTEGER DEFAULT 0,

    -- Odoo System Fields
    create_uid INTEGER,
    create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    write_uid INTEGER,
    write_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT unique_user_profile UNIQUE(user_id)
);

CREATE INDEX idx_sam_user_profile_user ON sam_user_profile(user_id);
CREATE INDEX idx_sam_user_profile_relationship ON sam_user_profile(relationship_level);

-- ============================================================================
-- SAM USER SETTINGS (User Preferences & Configuration)
-- ============================================================================
CREATE TABLE IF NOT EXISTS sam_user_settings (
    id SERIAL PRIMARY KEY,

    -- User Reference
    user_id INTEGER NOT NULL REFERENCES res_users(id) ON DELETE CASCADE,

    -- Active Mode
    active_mode VARCHAR(50) DEFAULT 'general',
    -- dev, sales, marketing, support, general

    -- Creator Mode
    creator_mode BOOLEAN DEFAULT FALSE,

    -- Whitelisted Paths (for local file access)
    whitelisted_paths TEXT, -- JSON array

    -- UI Preferences
    theme VARCHAR(50) DEFAULT 'light',
    show_token_counter BOOLEAN DEFAULT TRUE,
    auto_save BOOLEAN DEFAULT TRUE,

    -- Odoo System Fields
    create_uid INTEGER,
    create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    write_uid INTEGER,
    write_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT unique_user_settings UNIQUE(user_id)
);

CREATE INDEX idx_sam_user_settings_user ON sam_user_settings(user_id);

-- ============================================================================
-- SAM MODE CONTEXT (Power Prompts)
-- ============================================================================
CREATE TABLE IF NOT EXISTS sam_mode_context (
    id SERIAL PRIMARY KEY,

    -- Mode Information
    mode_key VARCHAR(50) NOT NULL UNIQUE,
    mode_name VARCHAR(255) NOT NULL,
    description TEXT,

    -- Power Prompt
    system_prompt TEXT,
    context_rules TEXT, -- JSON: additional rules

    -- Visual
    icon VARCHAR(100),
    color VARCHAR(7), -- Hex color

    -- Availability
    active BOOLEAN DEFAULT TRUE,
    requires_local BOOLEAN DEFAULT FALSE,
    requires_creator_mode BOOLEAN DEFAULT FALSE,

    -- Ordering
    sequence INTEGER DEFAULT 10,

    -- Odoo System Fields
    create_uid INTEGER,
    create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    write_uid INTEGER,
    write_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_sam_mode_context_key ON sam_mode_context(mode_key);
CREATE INDEX idx_sam_mode_context_active ON sam_mode_context(active);

-- ============================================================================
-- AI BRANCH REGISTRY (Meta-Architecture)
-- ============================================================================
CREATE TABLE IF NOT EXISTS ai_branch (
    id SERIAL PRIMARY KEY,

    -- Basic Information
    name VARCHAR(255) NOT NULL,
    technical_name VARCHAR(100) NOT NULL UNIQUE,
    code VARCHAR(10) NOT NULL,

    -- Display & UI
    icon VARCHAR(100) DEFAULT '📊',
    color VARCHAR(7) DEFAULT '#1a73e8',
    description TEXT,

    -- Ordering & Availability
    sequence INTEGER DEFAULT 10,
    active BOOLEAN DEFAULT TRUE,
    is_core BOOLEAN DEFAULT FALSE,

    -- Module Information
    module_name VARCHAR(100),
    module_installed BOOLEAN, -- Computed

    -- Canvas Configuration
    canvas_type VARCHAR(50) DEFAULT 'node_based',
    -- node_based, freeform, grid, timeline, board

    platform_renderer VARCHAR(100),
    -- Name of JS renderer (e.g., 'poppy_node_renderer')

    -- Features
    supports_ai_chat BOOLEAN DEFAULT TRUE,
    supports_export BOOLEAN DEFAULT TRUE,
    supports_collaboration BOOLEAN DEFAULT FALSE,

    -- Odoo System Fields
    create_uid INTEGER,
    create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    write_uid INTEGER,
    write_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_ai_branch_technical ON ai_branch(technical_name);
CREATE INDEX idx_ai_branch_active ON ai_branch(active);

-- ============================================================================
-- CANVAS (Universal Canvas - Polymorphic Workflows)
-- ============================================================================
CREATE TABLE IF NOT EXISTS canvas (
    id SERIAL PRIMARY KEY,

    -- Basic Information
    name VARCHAR(255) NOT NULL DEFAULT 'New Workflow',
    description TEXT,
    active BOOLEAN DEFAULT TRUE,

    -- Branch System (Meta-Architecture)
    branch_type VARCHAR(100) DEFAULT 'workflow',
    branch_id INTEGER REFERENCES ai_branch(id),
    canvas_type VARCHAR(50) DEFAULT 'node_based',

    -- Business Unit
    business_unit_id INTEGER REFERENCES workflow_business_unit(id),

    -- Workflow Type
    workflow_type_id INTEGER REFERENCES workflow_types(id),

    -- JSON Definition (N8N-compatible)
    json_definition TEXT,

    -- Generated Code
    generated_python_code TEXT,
    generated_javascript_code TEXT,

    -- Execution Configuration
    execution_mode VARCHAR(50) DEFAULT 'manual',
    -- manual, trigger, scheduled, webhook

    -- Scheduling
    cron_expression VARCHAR(255),
    next_execution TIMESTAMP,

    -- Webhook Configuration
    webhook_url VARCHAR(255),
    webhook_method VARCHAR(10) DEFAULT 'POST',

    -- Canvas Visual Configuration
    canvas_settings TEXT, -- JSON

    -- Template
    template_id INTEGER REFERENCES workflow_template(id),

    -- Statistics (computed)
    total_executions INTEGER DEFAULT 0,
    successful_executions INTEGER DEFAULT 0,
    failed_executions INTEGER DEFAULT 0,
    last_execution_date TIMESTAMP,

    -- Access Control
    visibility VARCHAR(50) DEFAULT 'private',
    -- private, team, company, public

    -- Visual
    color INTEGER DEFAULT 0,

    -- Odoo System Fields
    create_uid INTEGER,
    create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    write_uid INTEGER,
    write_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_canvas_active ON canvas(active);
CREATE INDEX idx_canvas_branch_type ON canvas(branch_type);
CREATE INDEX idx_canvas_business_unit ON canvas(business_unit_id);

-- ============================================================================
-- NODES (Canvas Nodes)
-- ============================================================================
CREATE TABLE IF NOT EXISTS nodes (
    id SERIAL PRIMARY KEY,

    -- Basic Information
    node_id VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    type VARCHAR(255),
    sequence INTEGER DEFAULT 10,

    -- Canvas Relationship
    canvas_id INTEGER NOT NULL REFERENCES canvas(id) ON DELETE CASCADE,

    -- Node Type
    node_type_id INTEGER REFERENCES n8n_node_types(id),

    -- Credential
    credential_id INTEGER REFERENCES api_credentials(id),

    -- Node Parameters (JSON)
    parameters TEXT,

    -- Visual Position
    x_cord FLOAT DEFAULT 0,
    y_cord FLOAT DEFAULT 0,

    -- State
    active BOOLEAN DEFAULT TRUE,
    disabled BOOLEAN DEFAULT FALSE,

    -- Execution Configuration
    retry_on_failure BOOLEAN DEFAULT FALSE,
    max_retries INTEGER DEFAULT 3,
    retry_interval INTEGER DEFAULT 30,
    continue_on_fail BOOLEAN DEFAULT FALSE,

    -- Connections (N8N-style)
    input_connections TEXT, -- JSON
    output_connections TEXT, -- JSON

    -- Notes
    notes TEXT,

    -- Odoo System Fields
    create_uid INTEGER,
    create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    write_uid INTEGER,
    write_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT unique_node_per_canvas UNIQUE(canvas_id, node_id)
);

CREATE INDEX idx_nodes_canvas ON nodes(canvas_id);
CREATE INDEX idx_nodes_node_type ON nodes(node_type_id);
CREATE INDEX idx_nodes_active ON nodes(active);

-- ============================================================================
-- CONNECTIONS (Node Connections)
-- ============================================================================
CREATE TABLE IF NOT EXISTS connections (
    id SERIAL PRIMARY KEY,

    -- Core Fields
    canvas_id INTEGER NOT NULL REFERENCES canvas(id) ON DELETE CASCADE,
    from_node_id INTEGER NOT NULL REFERENCES nodes(id) ON DELETE CASCADE,
    to_node_id INTEGER NOT NULL REFERENCES nodes(id) ON DELETE CASCADE,

    cnct_from VARCHAR(50) DEFAULT 'output',
    cnct_to VARCHAR(50) DEFAULT 'input',

    -- Connection Type
    connection_type VARCHAR(50) DEFAULT 'data',
    -- data, trigger, error

    -- Metadata
    active BOOLEAN DEFAULT TRUE,
    properties TEXT, -- JSON

    -- Odoo System Fields
    create_uid INTEGER,
    create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    write_uid INTEGER,
    write_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_connections_canvas ON connections(canvas_id);
CREATE INDEX idx_connections_from ON connections(from_node_id);
CREATE INDEX idx_connections_to ON connections(to_node_id);

-- ============================================================================
-- EXECUTIONS (Workflow Execution History)
-- ============================================================================
CREATE TABLE IF NOT EXISTS executions (
    id SERIAL PRIMARY KEY,

    -- Workflow Relationship
    canvas_id INTEGER NOT NULL REFERENCES canvas(id) ON DELETE CASCADE,

    -- Execution Status
    state VARCHAR(50) NOT NULL DEFAULT 'pending',
    -- pending, running, completed, failed, cancelled

    -- Timing
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    duration FLOAT, -- Seconds (computed)

    -- Trigger Information
    trigger_type VARCHAR(50) DEFAULT 'manual',
    -- manual, webhook, schedule, database, email
    triggered_by INTEGER REFERENCES res_users(id),
    trigger_data TEXT, -- JSON

    -- Execution Data
    input_data TEXT, -- JSON
    output_data TEXT, -- JSON
    execution_log TEXT, -- JSON

    -- Error Handling
    error_message TEXT,
    error_node_id VARCHAR(255),
    error_details TEXT,

    -- Statistics
    nodes_executed INTEGER DEFAULT 0,
    nodes_total INTEGER DEFAULT 0,

    -- Odoo System Fields
    create_uid INTEGER,
    create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    write_uid INTEGER,
    write_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_executions_canvas ON executions(canvas_id);
CREATE INDEX idx_executions_state ON executions(state);
CREATE INDEX idx_executions_start_time ON executions(start_time);

-- ============================================================================
-- MEMORY SYSTEM (Graph + Vector Databases)
-- ============================================================================

-- ============================================================================
-- AI MEMORY CONFIG (Memory System Configuration)
-- ============================================================================
CREATE TABLE IF NOT EXISTS ai_memory_config (
    id SERIAL PRIMARY KEY,

    -- Graph Database (Apache AGE)
    graph_enabled BOOLEAN DEFAULT FALSE,
    graph_host VARCHAR(255) DEFAULT 'localhost',
    graph_port INTEGER DEFAULT 5432,
    graph_database VARCHAR(100) DEFAULT 'sam_ai_memory',
    graph_name VARCHAR(100) DEFAULT 'sam_ai_knowledge',

    -- Vector Database (ChromaDB)
    vector_enabled BOOLEAN DEFAULT FALSE,
    vector_host VARCHAR(255) DEFAULT 'localhost',
    vector_port INTEGER DEFAULT 8000,
    collection_name VARCHAR(100) DEFAULT 'sam_conversations',

    -- Embedding Model
    embedding_model VARCHAR(100) DEFAULT 'all-MiniLM-L6-v2',
    embedding_dimensions INTEGER DEFAULT 384,

    -- Usage Statistics
    total_nodes INTEGER DEFAULT 0,
    total_edges INTEGER DEFAULT 0,
    total_vectors INTEGER DEFAULT 0,

    -- Status
    active BOOLEAN DEFAULT TRUE,
    last_sync TIMESTAMP,

    -- Odoo System Fields
    create_uid INTEGER,
    create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    write_uid INTEGER,
    write_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- AI EXTRACTOR PLUGIN (Learned Extraction Patterns)
-- ============================================================================
CREATE TABLE IF NOT EXISTS ai_extractor_plugin (
    id SERIAL PRIMARY KEY,

    -- Plugin Information
    name VARCHAR(255) NOT NULL,
    description TEXT,

    -- Entity Type
    entity_type VARCHAR(100) NOT NULL,
    -- person, company, project, concept, etc.

    -- Extraction Pattern
    extraction_prompt TEXT,
    sample_text TEXT,
    expected_output TEXT, -- JSON schema

    -- Performance
    success_rate FLOAT DEFAULT 0.0,
    usage_count INTEGER DEFAULT 0,

    -- Status
    active BOOLEAN DEFAULT TRUE,
    is_system BOOLEAN DEFAULT FALSE,

    -- Odoo System Fields
    create_uid INTEGER,
    create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    write_uid INTEGER,
    write_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_ai_extractor_plugin_type ON ai_extractor_plugin(entity_type);
CREATE INDEX idx_ai_extractor_plugin_active ON ai_extractor_plugin(active);

-- ============================================================================
-- SUPPORTING TABLES
-- ============================================================================

-- ============================================================================
-- WORKFLOW BUSINESS UNIT
-- ============================================================================
CREATE TABLE IF NOT EXISTS workflow_business_unit (
    id SERIAL PRIMARY KEY,

    name VARCHAR(255) NOT NULL,
    code VARCHAR(50) UNIQUE,
    description TEXT,
    active BOOLEAN DEFAULT TRUE,

    -- Odoo System Fields
    create_uid INTEGER,
    create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    write_uid INTEGER,
    write_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- WORKFLOW TYPES
-- ============================================================================
CREATE TABLE IF NOT EXISTS workflow_types (
    id SERIAL PRIMARY KEY,

    name VARCHAR(255) NOT NULL UNIQUE,
    display_name VARCHAR(255) NOT NULL,
    description TEXT,
    category VARCHAR(100),

    -- Configuration
    default_settings TEXT, -- JSON
    allowed_triggers TEXT, -- JSON array
    template_json TEXT, -- JSON

    -- Visual
    icon_class VARCHAR(100),
    color VARCHAR(7),

    active BOOLEAN DEFAULT TRUE,

    -- Odoo System Fields
    create_uid INTEGER,
    create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    write_uid INTEGER,
    write_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- WORKFLOW TEMPLATE
-- ============================================================================
CREATE TABLE IF NOT EXISTS workflow_template (
    id SERIAL PRIMARY KEY,

    name VARCHAR(255) NOT NULL,
    display_name VARCHAR(255),
    description TEXT,
    category VARCHAR(100),

    -- Template Data
    json_definition TEXT,
    default_parameters TEXT, -- JSON

    -- Metadata
    author_id INTEGER REFERENCES res_users(id),
    version VARCHAR(50) DEFAULT '1.0',
    tags TEXT, -- JSON array

    -- Usage
    usage_count INTEGER DEFAULT 0,
    last_used TIMESTAMP,

    -- Status
    active BOOLEAN DEFAULT TRUE,
    is_public BOOLEAN DEFAULT FALSE,

    -- Odoo System Fields
    create_uid INTEGER,
    create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    write_uid INTEGER,
    write_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- N8N NODE TYPES (Simplified 2-Table Design)
-- ============================================================================
CREATE TABLE IF NOT EXISTS n8n_node_types (
    id SERIAL PRIMARY KEY,

    -- Basic Information
    display_name VARCHAR(255) NOT NULL,
    folder_name VARCHAR(255) NOT NULL,
    n8n_type VARCHAR(255),

    -- Categorization
    category VARCHAR(100),
    description TEXT,

    -- File System
    has_icon BOOLEAN DEFAULT FALSE,
    icon_path VARCHAR(500),
    has_node_json BOOLEAN DEFAULT FALSE,

    -- Visual
    icon_class VARCHAR(100),
    color VARCHAR(7),

    -- Credentials
    requires_credentials BOOLEAN DEFAULT FALSE,
    credential_types TEXT, -- JSON

    -- Status
    active BOOLEAN DEFAULT TRUE,

    -- Odoo System Fields
    create_uid INTEGER,
    create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    write_uid INTEGER,
    write_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_n8n_node_types_category ON n8n_node_types(category);
CREATE INDEX idx_n8n_node_types_active ON n8n_node_types(active);

-- ============================================================================
-- API CREDENTIALS
-- ============================================================================
CREATE TABLE IF NOT EXISTS api_credentials (
    id SERIAL PRIMARY KEY,

    -- Basic Information
    name VARCHAR(255) NOT NULL,
    credential_type VARCHAR(100) NOT NULL,
    -- oauth2, api_key, username_password, certificate
    service_name VARCHAR(100),
    description TEXT,

    -- Encrypted Credential Data
    credential_data TEXT, -- Encrypted JSON

    -- OAuth2
    client_id VARCHAR(255),
    client_secret TEXT, -- Encrypted
    access_token TEXT, -- Encrypted
    refresh_token TEXT, -- Encrypted
    token_expires_at TIMESTAMP,
    scope VARCHAR(500),
    auth_url VARCHAR(500),
    token_url VARCHAR(500),

    -- API Key
    api_key TEXT, -- Encrypted
    api_secret TEXT, -- Encrypted
    api_endpoint VARCHAR(500),

    -- Username/Password
    username VARCHAR(255),
    password TEXT, -- Encrypted
    host VARCHAR(255),
    port INTEGER,

    -- Additional Configuration
    additional_config TEXT, -- JSON
    custom_headers TEXT, -- JSON

    -- Status
    active BOOLEAN DEFAULT TRUE,
    is_valid BOOLEAN DEFAULT FALSE,
    last_tested TIMESTAMP,

    -- Odoo System Fields
    create_uid INTEGER,
    create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    write_uid INTEGER,
    write_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_api_credentials_service ON api_credentials(service_name);
CREATE INDEX idx_api_credentials_type ON api_credentials(credential_type);

-- ============================================================================
-- MANY-TO-MANY RELATIONSHIP TABLES
-- ============================================================================

-- Canvas Team Members
CREATE TABLE IF NOT EXISTS canvas_res_users_rel (
    canvas_id INTEGER NOT NULL REFERENCES canvas(id) ON DELETE CASCADE,
    res_users_id INTEGER NOT NULL,
    PRIMARY KEY (canvas_id, res_users_id)
);

-- ============================================================================
-- SAM AI V3 ARCHITECTURE VIEWS
-- ============================================================================

-- Unified Conversation View
CREATE OR REPLACE VIEW v_sam_conversations AS
SELECT
    c.id,
    c.name,
    c.conversation_type,
    c.status,
    u.name as user_name,
    p.display_name as profile_name,
    p.relationship_level,
    c.message_count,
    c.total_tokens,
    c.total_cost,
    c.last_message_date,
    c.create_date
FROM ai_conversation c
JOIN res_users u ON c.user_id = u.id
LEFT JOIN sam_user_profile p ON u.id = p.user_id
WHERE c.active = TRUE;

-- User Activity Summary
CREATE OR REPLACE VIEW v_user_ai_activity AS
SELECT
    u.id as user_id,
    u.name as user_name,
    p.relationship_level,
    p.interaction_count,
    COUNT(DISTINCT c.id) as total_conversations,
    SUM(c.message_count) as total_messages,
    SUM(c.total_tokens) as total_tokens,
    SUM(c.total_cost) as total_cost,
    MAX(c.last_message_date) as last_activity
FROM res_users u
LEFT JOIN sam_user_profile p ON u.id = p.user_id
LEFT JOIN ai_conversation c ON u.id = c.user_id
GROUP BY u.id, u.name, p.relationship_level, p.interaction_count;

-- ============================================================================
-- VERIFICATION QUERIES
-- ============================================================================

-- Check all SAM AI tables exist:
/*
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
AND table_name IN (
    'ai_service_config',
    'ai_conversation',
    'ai_message',
    'ai_token_usage',
    'sam_user_profile',
    'sam_user_settings',
    'sam_mode_context',
    'ai_branch',
    'canvas',
    'nodes',
    'connections',
    'executions',
    'ai_memory_config'
)
ORDER BY table_name;
*/

-- Count records in core tables:
/*
SELECT
    'ai_conversation' as table_name, COUNT(*) as records FROM ai_conversation
UNION ALL SELECT
    'ai_message' as table_name, COUNT(*) FROM ai_message
UNION ALL SELECT
    'sam_user_profile' as table_name, COUNT(*) FROM sam_user_profile
UNION ALL SELECT
    'canvas' as table_name, COUNT(*) FROM canvas
UNION ALL SELECT
    'nodes' as table_name, COUNT(*) FROM nodes
UNION ALL SELECT
    'executions' as table_name, COUNT(*) FROM executions;
*/

-- ============================================================================
-- END OF SAM AI V3 DATABASE SCHEMA
-- Architecture: ai_brain (data) → ai_sam (framework) → branches
-- ============================================================================

```
