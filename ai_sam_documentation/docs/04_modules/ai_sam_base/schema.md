# ai_sam_base - Database Schema

Auto-generated model documentation.

## Models (69 total)

### `ai.access.gate`

_AI Access Gate - Permission Control_

**Key Fields**:
- `user_id` (Many2one)
- `path` (Char)
- `state` (Selection)
- `requested_reason` (Text)
- `conversation_id` (Many2one)
- `approved_at` (Date)
- `denied_at` (Date)
- `expires_at` (Date)

### `ai.agent.registry`

_AI Agent Registry_

**Key Fields**:
- `name` (Char)
- `display_name` (Char)
- `description` (Text)
- `active` (Boolean)
- `sequence` (Integer)
- `archetype` (Selection)
- `category` (Selection)
- `version` (Char)
- `slash_command` (Char)
- `color` (Char)

### `ai.agent.execution`

_AI Agent Execution Log_

**Key Fields**:
- `agent_id` (Many2one)
- `conversation_id` (Many2one)
- `session_id` (Many2one)
- `user_id` (Many2one)
- `user_message` (Text)
- `agent_response` (Text)
- `memory_used` (Boolean)
- `past_conversations_referenced` (Integer)
- `knowledge_chunks_used` (Integer)
- `response_time_ms` (Integer)

### `ai.agent.knowledge`

_AI Agent Knowledge Base_

**Key Fields**:
- `agent_id` (Many2one)
- `name` (Char)
- `sequence` (Integer)
- `content` (Text)
- `content_type` (Selection)
- `source_file` (Char)
- `source_path` (Char)
- `chunk_index` (Integer)
- `embedding_id` (Char)
- `embedding_collection` (Char)

### `ai.service`

_AI Brain - Central Orchestrator_

**Key Fields**:
- `last_request_date` (Date)

### `ai.branch`

_AI Branch Registry - Defines Available Canvas Types_

**Key Fields**:
- `name` (Char)
- `technical_name` (Char)
- `code` (Char)
- `icon` (Char)
- `color` (Char)
- `description` (Text)
- `sequence` (Integer)
- `active` (Boolean)
- `is_core` (Boolean)
- `module_name` (Char)

### `ai.context.analyzer`

_AI Context Analyzer - Detects Context Shifts_

### `ai.context.builder`

_AI Context Builder - The All-Knowing Brain_

### `ai.conversation`

_AI Conversation Thread_

**Key Fields**:
- `name` (Char)
- `active` (Boolean)
- `user_id` (Many2one)
- `company_id` (Many2one)
- `workspace_ids` (Many2many)
- `is_shared` (Boolean)
- `context_model` (Char)
- `context_id` (Integer)
- `node_id` (Char)
- `context_description` (Char)

### `claude-sonnet-4-20250514`

_General Conversation_

**Key Fields**:
- `name` (Char)
- `active` (Boolean)
- `user_id` (Many2one)
- `company_id` (Many2one)
- `workspace_ids` (Many2many)
- `is_shared` (Boolean)
- `context_model` (Char)
- `context_id` (Integer)
- `node_id` (Char)
- `context_description` (Char)

### `claude-3-opus-20240229`

**Key Fields**:
- `name` (Char)
- `active` (Boolean)
- `user_id` (Many2one)
- `company_id` (Many2one)
- `workspace_ids` (Many2many)
- `is_shared` (Boolean)
- `context_model` (Char)
- `context_id` (Integer)
- `node_id` (Char)
- `context_description` (Char)

### `claude-3-haiku-20240307`

**Key Fields**:
- `name` (Char)
- `active` (Boolean)
- `user_id` (Many2one)
- `company_id` (Many2one)
- `workspace_ids` (Many2many)
- `is_shared` (Boolean)
- `context_model` (Char)
- `context_id` (Integer)
- `node_id` (Char)
- `context_description` (Char)

### `odoo-intelligence`

**Key Fields**:
- `name` (Char)
- `active` (Boolean)
- `user_id` (Many2one)
- `company_id` (Many2one)
- `workspace_ids` (Many2many)
- `is_shared` (Boolean)
- `context_model` (Char)
- `context_id` (Integer)
- `node_id` (Char)
- `context_description` (Char)

### `ai.conversation.history.importer`

_AI Conversation History Importer_

**Key Fields**:
- `file_data` (Binary)
- `file_name` (Char)
- `folder_path` (Char)
- `import_method` (Selection)
- `recent_file_count` (Integer)
- `embed_vectors` (Boolean)
- `skip_duplicates` (Boolean)
- `preview_text` (Text)
- `total_conversations` (Integer)
- `total_messages` (Integer)

### `ai.conversation.import`

_AI Conversation Import Wizard_

**Key Fields**:
- `name` (Char)
- `source_path` (Char)
- `source_type` (Selection)
- `state` (Selection)
- `validation_message` (Text)
- `is_valid` (Boolean)
- `extracted_path` (Char)
- `total_conversations` (Integer)
- `total_messages` (Integer)
- `date_range_start` (Date)

### `Untitled Conversation`

**Key Fields**:
- `name` (Char)
- `source_path` (Char)
- `source_type` (Selection)
- `state` (Selection)
- `validation_message` (Text)
- `is_valid` (Boolean)
- `extracted_path` (Char)
- `total_conversations` (Integer)
- `total_messages` (Integer)
- `date_range_start` (Date)

### `ai.conversation.tag`

_Conversation Tag_

**Key Fields**:
- `name` (Char)
- `color` (Integer)
- `conversation_count` (Integer)

### `ai.cost.budget`

_AI Cost Budget Management_

**Key Fields**:
- `name` (Char)
- `period_type` (Selection)
- `start_date` (Date)
- `default` (Date)
- `end_date` (Date)
- `budget_amount` (Float)
- `current_spend` (Float)
- `remaining_budget` (Float)
- `percentage_used` (Float)
- `alert_thresholds` (Char)

### `ai.cost.optimizer`

_AI Cost Optimizer - Provider Recommendation Engine_

**Key Fields**:
- `name` (Char)
- `task_type` (Selection)
- `context_size_tokens` (Integer)
- `quality_required` (Selection)
- `max_budget_usd` (Float)
- `recommended_provider_id` (Many2one)
- `estimated_cost_usd` (Float)
- `reasoning` (Text)
- `alternatives` (Text)
- `user_id` (Many2one)

### `ai.document.extractor`

_AI-Powered Document Extraction Engine_

**Key Fields**:
- `name` (Char)
- `file_extension` (Char)
- `extractor_code` (Text)
- `analysis` (Text)
- `test_file_path` (Char)
- `is_active` (Boolean)
- `success_count` (Integer)
- `failure_count` (Integer)
- `success_rate` (Float)

### `ai.extractor.plugin`

_AI-Learned Document Extractor Plugin_

**Key Fields**:
- `name` (Char)
- `file_extension` (Char)
- `extractor_code` (Text)
- `analysis` (Text)
- `test_file_path` (Char)
- `is_active` (Boolean)
- `success_count` (Integer)
- `failure_count` (Integer)
- `success_rate` (Float)

### `ai.graph.service`

_AI Graph Database Service (Apache AGE)_

### `sam_ai_knowledge`

### `ai.knowledge.domain`

_Knowledge Domain Hub_

**Key Fields**:
- `name` (Char)
- `code` (Char)
- `color` (Char)
- `sequence` (Integer)
- `agent_command` (Char)
- `description` (Text)
- `active` (Boolean)
- `conversation_count` (Integer)
- `graph_size` (Integer)
- `graph_shape` (Selection)

### `ai.knowledge.subcategory`

_Knowledge Subcategory (AI-Detected)_

**Key Fields**:
- `name` (Char)
- `domain_id` (Many2one)
- `code` (Char)
- `description` (Text)
- `conversation_ids` (Many2many)
- `conversation_count` (Integer)
- `color` (Char)
- `confidence` (Float)
- `active` (Boolean)
- `graph_size` (Integer)

### `ai.location.introspector`

_AI Location Introspector - Platform-Aware Context_

### `ai.memory.config`

_AI Memory Configuration_

**Key Fields**:
- `name` (Char)
- `graph_enabled` (Boolean)
- `graph_host` (Char)
- `graph_port` (Integer)
- `graph_database` (Char)
- `graph_user` (Char)
- `graph_password` (Char)
- `graph_name` (Char)
- `vector_enabled` (Boolean)
- `chroma_persist_directory` (Char)

### `ai.memory.import.wizard`

_Import Memory Backup_

**Key Fields**:
- `backup_file` (Binary)
- `backup_filename` (Char)
- `import_configs` (Boolean)
- `import_conversation_imports` (Boolean)
- `import_extractors` (Boolean)
- `overwrite_existing` (Boolean)
- `state` (Selection)
- `result_message` (Text)

### `ai.memory.search.log`

_AI Memory Search Log_

**Key Fields**:
- `query` (Text)
- `results_count` (Integer)
- `avg_similarity` (Float)
- `max_similarity` (Float)
- `search_time_ms` (Float)
- `conversation_id` (Many2one)
- `user_id` (Many2one)
- `has_results` (Boolean)
- `create_date` (Date)

### `ai.memory.uninstall.wizard`

_Uninstall SAM AI Memory Module_

**Key Fields**:
- `import_record_count` (Integer)
- `extractor_count` (Integer)
- `config_count` (Integer)
- `has_data` (Boolean)

### `ai.message`

_AI Message_

**Key Fields**:
- `conversation_id` (Many2one)
- `role` (Selection)
- `content` (Text)
- `token_count` (Integer)
- `cost` (Float)
- `is_system` (Boolean)
- `create_date` (Date)
- `user_id` (Many2one)
- `ai_model` (Char)
- `ai_provider` (Selection)

### `ai.mode.registry`

_AI Mode Registry_

**Key Fields**:
- `name` (Char)
- `display_name_custom` (Char)
- `version` (Char)
- `description` (Text)
- `prompt_file` (Char)
- `tools_module` (Char)
- `prompt_content` (Text)
- `triggers_json` (Text)
- `active` (Boolean)
- `sequence` (Integer)

### `ai.module.intelligence`

_AI Module Intelligence - Module-Specific Training Data_

**Key Fields**:
- `module_id` (Many2one)
- `module_name` (Char)
- `module_display_name` (Char)
- `training_data` (Text)
- `common_questions` (Text)
- `common_tasks` (Text)
- `workflows` (Text)
- `knowledge_json` (Text)
- `icon` (Char)
- `color` (Char)

### `ai.provider.benchmark`

_AI Provider Benchmark - Performance Tracking_

**Key Fields**:
- `provider_id` (Many2one)
- `task_type` (Selection)
- `task_complexity` (Selection)
- `input_tokens` (Integer)
- `output_tokens` (Integer)
- `cost_usd` (Float)
- `response_time_ms` (Integer)
- `quality_score` (Integer)
- `error_occurred` (Boolean)
- `error_message` (Text)

### `ai.provider.model`

_AI Model within Provider_

**Key Fields**:
- `provider_id` (Many2one)
- `name` (Char)
- `model_identifier` (Char)
- `description` (Text)
- `capability_level` (Selection)
- `max_context_tokens` (Integer)
- `cost_per_1m_input_tokens` (Float)
- `cost_per_1m_output_tokens` (Float)
- `cost_summary` (Char)
- `is_enabled` (Boolean)

### `ai.service.cost.comparison`

_AI Service Cost Comparison_

**Key Fields**:
- `service_type_id` (Many2one)
- `service_type_name` (Char)
- `service_technical_name` (Char)
- `provider_id` (Many2one)
- `provider_name` (Char)
- `vendor_key` (Char)
- `model_count` (Integer)
- `cost_per_1m_input_tokens_min` (Float)
- `cost_per_1m_output_tokens_min` (Float)
- `cost_per_1m_tokens_avg` (Float)

### `api_service_provider`

**Key Fields**:
- `service_type_id` (Many2one)
- `service_type_name` (Char)
- `service_technical_name` (Char)
- `provider_id` (Many2one)
- `provider_name` (Char)
- `vendor_key` (Char)
- `model_count` (Integer)
- `cost_per_1m_input_tokens_min` (Float)
- `cost_per_1m_output_tokens_min` (Float)
- `cost_per_1m_tokens_avg` (Float)

### `ai.service.type`

_AI Service Type_

**Key Fields**:
- `name` (Char)
- `technical_name` (Char)
- `description` (Text)
- `icon` (Char)
- `sequence` (Integer)
- `active` (Boolean)
- `vendor_key` (Char)
- `service_key` (Char)
- `service_category` (Selection)
- `api_base_url` (Char)

### `ai.token.usage`

_AI Token Usage Tracking_

**Key Fields**:
- `user_id` (Many2one)
- `company_id` (Many2one)
- `conversation_id` (Many2one)
- `service_provider_id` (Many2one)
- `provider` (Selection)
- `model_name` (Char)
- `input_tokens` (Integer)
- `output_tokens` (Integer)
- `total_tokens` (Integer)
- `input_cost_per_token` (Float)

### `ai.vector.service`

_AI Vector Database Service (ChromaDB)_

### `sam_ai_conversations`

### `ai.workspace`

_AI Workspace - Team Knowledge Sharing_

**Key Fields**:
- `name` (Char)
- `description` (Text)
- `owner_id` (Many2one)
- `member_ids` (Many2many)
- `member_count` (Integer)
- `conversation_ids` (Many2many)
- `conversation_count` (Integer)
- `auto_add_new_conversations` (Boolean)
- `visibility` (Selection)
- `active` (Boolean)

### `api_credentials`

_API Credential for N8N-style Workflows_

**Key Fields**:
- `name` (Char)
- `credential_type` (Selection)
- `description` (Text)
- `credential_data` (Text)
- `is_active` (Boolean)
- `is_tested` (Boolean)
- `last_tested` (Date)
- `test_result` (Text)
- `usage_count` (Integer)
- `last_used` (Date)

### `name`

**Key Fields**:
- `name` (Char)
- `credential_type` (Selection)
- `description` (Text)
- `credential_data` (Text)
- `is_active` (Boolean)
- `is_tested` (Boolean)
- `last_tested` (Date)
- `test_result` (Text)
- `usage_count` (Integer)
- `last_used` (Date)

### `api.provider.identity`

_API Provider Identity (Who Sends/Receives)_

**Key Fields**:
- `provider_id` (Many2one)
- `identity` (Char)
- `identity_type` (Selection)
- `display_name` (Char)
- `description` (Text)
- `user_id` (Many2one)
- `is_default` (Boolean)
- `active` (Boolean)
- `company_id` (Many2one)

### `display_name`

**Key Fields**:
- `provider_id` (Many2one)
- `identity` (Char)
- `identity_type` (Selection)
- `display_name` (Char)
- `description` (Text)
- `user_id` (Many2one)
- `is_default` (Boolean)
- `active` (Boolean)
- `company_id` (Many2one)

### `New Identity`

**Key Fields**:
- `provider_id` (Many2one)
- `identity` (Char)
- `identity_type` (Selection)
- `display_name` (Char)
- `description` (Text)
- `user_id` (Many2one)
- `is_default` (Boolean)
- `active` (Boolean)
- `company_id` (Many2one)

### `api.service.provider`

_API Service Provider Configuration_

**Key Fields**:
- `setup_step` (Integer)
- `edit_mode` (Boolean)
- `available_auth_types` (Char)
- `available_services` (Char)
- `default_model_display` (Char)
- `is_template` (Boolean)
- `vendor_key` (Char)
- `template_id` (Many2one)
- `icon_filename` (Char)
- `icon_folder` (Char)

### `api_service_provider`

_editable_

**Key Fields**:
- `setup_step` (Integer)
- `edit_mode` (Boolean)
- `available_auth_types` (Char)
- `available_services` (Char)
- `default_model_display` (Char)
- `is_template` (Boolean)
- `vendor_key` (Char)
- `template_id` (Many2one)
- `icon_filename` (Char)
- `icon_folder` (Char)

### `ai_provider_model`

**Key Fields**:
- `setup_step` (Integer)
- `edit_mode` (Boolean)
- `available_auth_types` (Char)
- `available_services` (Char)
- `default_model_display` (Char)
- `is_template` (Boolean)
- `vendor_key` (Char)
- `template_id` (Many2one)
- `icon_filename` (Char)
- `icon_folder` (Char)

### `Enabled`

**Key Fields**:
- `setup_step` (Integer)
- `edit_mode` (Boolean)
- `available_auth_types` (Char)
- `available_services` (Char)
- `default_model_display` (Char)
- `is_template` (Boolean)
- `vendor_key` (Char)
- `template_id` (Many2one)
- `icon_filename` (Char)
- `icon_folder` (Char)

### `canvas.platform`

_Canvas Platform Registry_

**Key Fields**:
- `name` (Char)
- `technical_name` (Char)
- `renderer_class` (Char)
- `renderer_module` (Char)
- `ui_template` (Char)
- `icon` (Char)
- `description` (Text)
- `active` (Boolean)
- `sequence` (Integer)

### `canvas.tool.executor`

_Canvas Tool Executor_

### `external.tool.executor`

_External Tool Executor_

### `sam.mcp.server.config`

_MCP Server Configuration_

**Key Fields**:
- `server_name` (Char)
- `version` (Char)
- `description` (Text)
- `odoo_url` (Char)
- `odoo_database` (Char)
- `auth_method` (Selection)
- `default_username` (Char)
- `feature_ids` (One2many)
- `enable_projects` (Boolean)
- `enable_crm` (Boolean)

### `server_name`

_MCP Feature_

**Key Fields**:
- `server_name` (Char)
- `version` (Char)
- `description` (Text)
- `odoo_url` (Char)
- `odoo_database` (Char)
- `auth_method` (Selection)
- `default_username` (Char)
- `feature_ids` (One2many)
- `enable_projects` (Boolean)
- `enable_crm` (Boolean)

### `sam.mcp.feature`

**Key Fields**:
- `server_name` (Char)
- `version` (Char)
- `description` (Text)
- `odoo_url` (Char)
- `odoo_database` (Char)
- `auth_method` (Selection)
- `default_username` (Char)
- `feature_ids` (One2many)
- `enable_projects` (Boolean)
- `enable_crm` (Boolean)

### `mcp.server.generator`

_MCP Server Script Generator_

### `odoo.data.tool.executor`

_Odoo Data Tool Executor_

### `sam.environment`

_SAM AI Environment Detection_

**Key Fields**:
- `installation_type` (Selection)
- `has_filesystem_access` (Boolean)
- `has_git_access` (Boolean)
- `has_vscode_access` (Boolean)
- `has_python_shell` (Boolean)
- `has_npm_access` (Boolean)
- `odoo_config_path` (Char)
- `addons_path` (Char)
- `data_dir` (Char)
- `sam_mode` (Selection)

### `sam.mode.context`

_SAM AI Agent Context & Prompts (Hierarchical)_

**Key Fields**:
- `mode_key` (Char)
- `mode_name` (Char)
- `mode_icon` (Char)
- `mode_color` (Char)
- `description` (Text)
- `parent_id` (Many2one)
- `child_ids` (One2many)
- `parent_path` (Char)
- `is_master` (Boolean)
- `hierarchy_level` (Integer)

### `mode_name`

**Key Fields**:
- `mode_key` (Char)
- `mode_name` (Char)
- `mode_icon` (Char)
- `mode_color` (Char)
- `description` (Text)
- `parent_id` (Many2one)
- `child_ids` (One2many)
- `parent_path` (Char)
- `is_master` (Boolean)
- `hierarchy_level` (Integer)

### `parent_id`

**Key Fields**:
- `mode_key` (Char)
- `mode_name` (Char)
- `mode_icon` (Char)
- `mode_color` (Char)
- `description` (Text)
- `parent_id` (Many2one)
- `child_ids` (One2many)
- `parent_path` (Char)
- `is_master` (Boolean)
- `hierarchy_level` (Integer)

### `sam.personality`

_SAM AI Personality & Conversational Rules_

### `sam.user.profile`

_SAM AI User Relationship Profile_

**Key Fields**:
- `user_id` (Many2one)
- `display_name` (Char)
- `preferred_name` (Char)
- `relationship_level` (Selection)
- `trust_score` (Integer)
- `interaction_count` (Integer)
- `personal_facts` (Text)
- `family_info` (Text)
- `interests` (Char)
- `work_role` (Char)

### `Friend`

**Key Fields**:
- `user_id` (Many2one)
- `display_name` (Char)
- `preferred_name` (Char)
- `relationship_level` (Selection)
- `trust_score` (Integer)
- `interaction_count` (Integer)
- `personal_facts` (Text)
- `family_info` (Text)
- `interests` (Char)
- `work_role` (Char)

### `AG`

**Key Fields**:
- `user_id` (Many2one)
- `display_name` (Char)
- `preferred_name` (Char)
- `relationship_level` (Selection)
- `trust_score` (Integer)
- `interaction_count` (Integer)
- `personal_facts` (Text)
- `family_info` (Text)
- `interests` (Char)
- `work_role` (Char)

### `sam.user.settings`

_SAM AI User Settings_

**Key Fields**:
- `user_id` (Many2one)
- `active_mode` (Char)
- `creator_mode` (Boolean)
- `whitelisted_paths` (Text)
- `dev_mode_enabled` (Boolean)
- `auto_start_session` (Boolean)
- `cached_provider_config` (Text)
- `cache_generated_at` (Date)
- `cache_version` (Char)

### `user_id`

**Key Fields**:
- `user_id` (Many2one)
- `active_mode` (Char)
- `creator_mode` (Boolean)
- `whitelisted_paths` (Text)
- `dev_mode_enabled` (Boolean)
- `auto_start_session` (Boolean)
- `cached_provider_config` (Text)
- `cache_generated_at` (Date)
- `cache_version` (Char)
