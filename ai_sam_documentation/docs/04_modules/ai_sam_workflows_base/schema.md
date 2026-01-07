# ai_sam_workflows_base - Database Schema

Auto-generated model documentation.

## Models (34 total)

### `ai.automator.config`

_AI Automator Configuration_

**Key Fields**:
- `knowledge_visualizer_enabled` (Boolean)

### `all.node.suppliers`

_N8N Suppliers (Simplified)_

**Key Fields**:
- `name` (Char)
- `has_services` (Boolean)
- `action_count` (Integer)
- `trigger_count` (Integer)
- `total_nodes` (Integer)
- `node_ids` (One2many)
- `created_at` (Date)
- `default` (Date)
- `updated_at` (Date)
- `default` (Date)

### `name`

_N8N Nodes (Simplified - Denormalized)_

**Key Fields**:
- `name` (Char)
- `has_services` (Boolean)
- `action_count` (Integer)
- `trigger_count` (Integer)
- `total_nodes` (Integer)
- `node_ids` (One2many)
- `created_at` (Date)
- `default` (Date)
- `updated_at` (Date)
- `default` (Date)

### `all.node.types`

**Key Fields**:
- `name` (Char)
- `has_services` (Boolean)
- `action_count` (Integer)
- `trigger_count` (Integer)
- `total_nodes` (Integer)
- `node_ids` (One2many)
- `created_at` (Date)
- `default` (Date)
- `updated_at` (Date)
- `default` (Date)

### `display_name`

**Key Fields**:
- `name` (Char)
- `has_services` (Boolean)
- `action_count` (Integer)
- `trigger_count` (Integer)
- `total_nodes` (Integer)
- `node_ids` (One2many)
- `created_at` (Date)
- `default` (Date)
- `updated_at` (Date)
- `default` (Date)

### `workflow.business.unit`

_Business Unit for Workflow Filtering_

**Key Fields**:
- `name` (Char)
- `code` (Char)
- `description` (Text)
- `sequence` (Integer)
- `active` (Boolean)
- `color` (Integer)
- `canvas_ids` (One2many)
- `canvas_count` (Integer)

### `canvas`

_N8N-Compatible Workflow Definition_

**Key Fields**:
- `name` (Char)
- `description` (Text)
- `active` (Boolean)
- `branch_type` (Char)
- `branch_id` (Many2one)
- `canvas_type` (Selection)
- `business_unit_id` (Many2one)
- `workflow_type` (Selection)
- `json_definition` (Text)
- `nodes_cache_valid` (Boolean)

### `canvas.history`

_Canvas Edit History_

**Key Fields**:
- `canvas_id` (Many2one)
- `action_type` (Selection)
- `previous_state` (Text)
- `action_data` (Text)
- `performed_by` (Selection)
- `user_id` (Many2one)
- `is_undone` (Boolean)

### `canvas.nodes`

_Canvas Nodes (N8N Compatible)_

**Inherits**: `nodes.executor.mixin`

**Key Fields**:
- `node_id` (Char)
- `name` (Char)
- `type` (Char)
- `sequence` (Integer)
- `canvas_id` (Many2one)
- `workflow_node_type_id` (Many2one)
- `effective_node_type` (Char)
- `credential_id` (Many2one)
- `identity_id` (Many2one)
- `previous_node_id` (Many2one)

### `sam_ai_website_builder.page_builder`

_Website Page Builder Executor_

**Inherits**: `nodes.executor.mixin`

**Key Fields**:
- `node_id` (Char)
- `name` (Char)
- `type` (Char)
- `sequence` (Integer)
- `canvas_id` (Many2one)
- `workflow_node_type_id` (Many2one)
- `effective_node_type` (Char)
- `credential_id` (Many2one)
- `identity_id` (Many2one)
- `previous_node_id` (Many2one)

### `my_module.my_executor`

_Node Executor Mixin_

**Key Fields**:
- `node_id` (Char)
- `name` (Char)
- `type` (Char)
- `sequence` (Integer)
- `canvas_id` (Many2one)
- `workflow_node_type_id` (Many2one)
- `effective_node_type` (Char)
- `credential_id` (Many2one)
- `identity_id` (Many2one)
- `previous_node_id` (Many2one)

### `nodes.executor.mixin`

**Key Fields**:
- `node_id` (Char)
- `name` (Char)
- `type` (Char)
- `sequence` (Integer)
- `canvas_id` (Many2one)
- `workflow_node_type_id` (Many2one)
- `effective_node_type` (Char)
- `credential_id` (Many2one)
- `identity_id` (Many2one)
- `previous_node_id` (Many2one)

### `executions`

_Workflow Execution Log_

**Key Fields**:
- `name` (Char)
- `canvas_id` (Many2one)
- `state` (Selection)
- `start_time` (Date)
- `end_time` (Date)
- `duration` (Float)
- `trigger_type` (Selection)
- `triggered_by` (Many2one)
- `trigger_data` (Text)
- `input_data` (Text)

### `dynamic_menus`

_N8N Dynamic Menu Generator_

### `workflow.n8n.import.wizard`

_N8N Workflow Import Wizard_

**Key Fields**:
- `n8n_json` (Text)
- `workflow_name` (Char)
- `preview_name` (Char)
- `preview_node_count` (Integer)
- `preview_description` (Text)
- `replace_existing` (Boolean)

### `Invalid JSON`

_No JSON provided_

**Key Fields**:
- `n8n_json` (Text)
- `workflow_name` (Char)
- `preview_name` (Char)
- `preview_node_count` (Integer)
- `preview_description` (Text)
- `replace_existing` (Boolean)

### `Parse Error`

**Key Fields**:
- `n8n_json` (Text)
- `workflow_name` (Char)
- `preview_name` (Char)
- `preview_node_count` (Integer)
- `preview_description` (Text)
- `replace_existing` (Boolean)

### `n8n.menu.debug`

_N8N Menu Debug Helper_

### `n8n.node.category`

_N8N Node Categories_

**Key Fields**:
- `name` (Char)
- `description` (Text)
- `sequence` (Integer)
- `ui_group` (Selection)
- `node_count` (Integer)
- `node_l2_ids` (Many2many)
- `is_active` (Boolean)
- `create_date` (Date)
- `write_date` (Date)
- `create_uid` (Many2one)

### `node_types`

_N8N Node Types Registry (DEPRECATED - use n8n.simple.node)_

**Key Fields**:
- `display_name` (Char)
- `n8n_type` (Char)
- `category` (Selection)
- `description` (Text)
- `icon_class` (Char)
- `color` (Char)
- `requires_credentials` (Boolean)
- `default_credential_id` (Many2one)
- `connection_inputs` (Integer)
- `connection_outputs` (Integer)

### `display_name`

**Key Fields**:
- `display_name` (Char)
- `n8n_type` (Char)
- `category` (Selection)
- `description` (Text)
- `icon_class` (Char)
- `color` (Char)
- `requires_credentials` (Boolean)
- `default_credential_id` (Many2one)
- `connection_inputs` (Integer)
- `connection_outputs` (Integer)

### `n8n.simple.extractor`

_N8N Node Extractor (Direct from Filesystem)_

**Key Fields**:
- `supplier_ids` (Many2many)
- `node_ids` (Many2many)
- `overlay_preview_html` (Html)
- `new_overlay_html` (Html)

### `workflow.connection`

_Workflow Connection_

**Key Fields**:
- `canvas_id` (Many2one)
- `source_node_id` (Many2one)
- `target_node_id` (Many2one)
- `source_handle` (Char)
- `target_handle` (Char)
- `sequence` (Integer)
- `display_name` (Char)
- `field_mapping_ids` (One2many)
- `mapped_field_count` (Integer)
- `unmapped_required_count` (Integer)

### `display_name`

**Key Fields**:
- `canvas_id` (Many2one)
- `source_node_id` (Many2one)
- `target_node_id` (Many2one)
- `source_handle` (Char)
- `target_handle` (Char)
- `sequence` (Integer)
- `display_name` (Char)
- `field_mapping_ids` (One2many)
- `mapped_field_count` (Integer)
- `unmapped_required_count` (Integer)

### `workflow.field.mapping`

_Field Mapping_

**Key Fields**:
- `connection_id` (Many2one)
- `canvas_id` (Many2one)
- `source_node_id` (Many2one)
- `target_node_id` (Many2one)
- `source_field` (Char)
- `target_field` (Char)
- `display_name` (Char)
- `sequence` (Integer)
- `transform_type` (Selection)
- `transform_expression` (Text)

### `display_name`

**Key Fields**:
- `connection_id` (Many2one)
- `canvas_id` (Many2one)
- `source_node_id` (Many2one)
- `target_node_id` (Many2one)
- `source_field` (Char)
- `target_field` (Char)
- `display_name` (Char)
- `sequence` (Integer)
- `transform_type` (Selection)
- `transform_expression` (Text)

### `workflow.field.schema`

_Node Field Schema_

**Key Fields**:
- `node_type_id` (Many2one)
- `field_name` (Char)
- `display_name` (Char)
- `description` (Text)
- `sequence` (Integer)
- `direction` (Selection)
- `field_type` (Selection)
- `is_required` (Boolean)
- `default_value` (Char)
- `is_standard` (Boolean)

### `field_name`

**Key Fields**:
- `node_type_id` (Many2one)
- `field_name` (Char)
- `display_name` (Char)
- `description` (Text)
- `sequence` (Integer)
- `direction` (Selection)
- `field_type` (Selection)
- `is_required` (Boolean)
- `default_value` (Char)
- `is_standard` (Boolean)

### `workflow.node.binary`

_Node Binary Output_

**Key Fields**:
- `output_id` (Many2one)
- `execution_id` (Many2one)
- `node_id` (Char)
- `filename` (Char)
- `sequence` (Integer)
- `mime_type` (Char)
- `file_size` (Integer)
- `file_size_display` (Char)
- `file_category` (Selection)
- `data` (Binary)

### `filename`

**Key Fields**:
- `output_id` (Many2one)
- `execution_id` (Many2one)
- `node_id` (Char)
- `filename` (Char)
- `sequence` (Integer)
- `mime_type` (Char)
- `file_size` (Integer)
- `file_size_display` (Char)
- `file_category` (Selection)
- `data` (Binary)

### `workflow.node.output`

_Node Execution Output_

**Key Fields**:
- `execution_id` (Many2one)
- `node_instance_id` (Many2one)
- `node_type_id` (Many2one)
- `node_id` (Char)
- `node_name` (Char)
- `sequence` (Integer)
- `display_name` (Char)
- `status` (Selection)
- `started_at` (Date)
- `completed_at` (Date)

### `display_name`

**Key Fields**:
- `execution_id` (Many2one)
- `node_instance_id` (Many2one)
- `node_type_id` (Many2one)
- `node_id` (Char)
- `node_name` (Char)
- `sequence` (Integer)
- `display_name` (Char)
- `status` (Selection)
- `started_at` (Date)
- `completed_at` (Date)

### `workflow.standard.field`

_SAM Standard Field Definition_

**Key Fields**:
- `name` (Char)
- `display_name` (Char)
- `description` (Text)
- `category` (Selection)
- `field_type` (Selection)
- `aliases` (Char)

### `name`

**Key Fields**:
- `name` (Char)
- `display_name` (Char)
- `description` (Text)
- `category` (Selection)
- `field_type` (Selection)
- `aliases` (Char)
