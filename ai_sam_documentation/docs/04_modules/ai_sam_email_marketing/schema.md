# ai_sam_email_marketing - Database Schema

Auto-generated model documentation.

## Models (6 total)

### `ai.email.campaign`

_AI Email Campaign_

**Key Fields**:
- `name` (Char)
- `description` (Text)
- `campaign_type` (Selection)
- `target_audience` (Text)
- `tone` (Selection)
- `campaign_goals` (Text)
- `ai_instructions` (Text)
- `brand_voice` (Text)
- `template_ids` (One2many)
- `generation_request_ids` (One2many)

### `name`

**Key Fields**:
- `name` (Char)
- `description` (Text)
- `campaign_type` (Selection)
- `target_audience` (Text)
- `tone` (Selection)
- `campaign_goals` (Text)
- `ai_instructions` (Text)
- `brand_voice` (Text)
- `template_ids` (One2many)
- `generation_request_ids` (One2many)

### `ai.email.generation.request`

_AI Email Generation Request_

**Key Fields**:
- `request_type` (Selection)
- `prompt` (Text)
- `uploaded_file_name` (Char)
- `uploaded_file_content` (Binary)
- `uploaded_file_type` (Selection)
- `campaign_id` (Many2one)
- `previous_template_id` (Many2one)
- `ai_response` (Text)
- `generated_subject` (Char)
- `generated_preheader` (Char)

### `request_type`

**Key Fields**:
- `request_type` (Selection)
- `prompt` (Text)
- `uploaded_file_name` (Char)
- `uploaded_file_content` (Binary)
- `uploaded_file_type` (Selection)
- `campaign_id` (Many2one)
- `previous_template_id` (Many2one)
- `ai_response` (Text)
- `generated_subject` (Char)
- `generated_preheader` (Char)

### `ai.email.template`

_AI Generated Email Template_

**Key Fields**:
- `subject` (Char)
- `preheader` (Char)
- `body_html` (Html)
- `body_text` (Text)
- `campaign_id` (Many2one)
- `generation_request_id` (Many2one)
- `prompt_used` (Text)
- `ai_model_used` (Char)
- `generation_metadata` (Text)
- `version` (Integer)

### `subject`

**Key Fields**:
- `subject` (Char)
- `preheader` (Char)
- `body_html` (Html)
- `body_text` (Text)
- `campaign_id` (Many2one)
- `generation_request_id` (Many2one)
- `prompt_used` (Text)
- `ai_model_used` (Char)
- `generation_metadata` (Text)
- `version` (Integer)
