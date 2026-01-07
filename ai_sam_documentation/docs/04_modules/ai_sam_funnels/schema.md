# ai_sam_funnels - Database Schema

Auto-generated model documentation.

## Models (6 total)

### `funnel.conversion`

_Funnel Conversion Event_

**Key Fields**:
- `funnel_id` (Many2one)
- `page_id` (Many2one)
- `visitor_id` (Char)
- `partner_id` (Many2one)
- `event_type` (Selection)
- `timestamp` (Date)
- `default` (Date)
- `session_data` (Text)
- `user_agent` (Char)
- `ip_address` (Char)

### `funnel.definition`

_Sales Funnel Definition_

**Key Fields**:
- `name` (Char)
- `description` (Text)
- `funnel_type` (Selection)
- `page_ids` (One2many)
- `page_count` (Integer)
- `template_id` (Many2one)
- `crm_team_id` (Many2one)
- `default_tag_ids` (Many2many)
- `mailing_list_id` (Many2one)
- `total_views` (Integer)

### `funnel.page`

_Funnel Page_

**Key Fields**:
- `name` (Char)
- `funnel_id` (Many2one)
- `sequence` (Integer)
- `page_type` (Selection)
- `website_page_id` (Many2one)
- `page_url` (Char)
- `full_url` (Char)
- `snippet_config` (Text)
- `next_page_id` (Many2one)
- `redirect_url` (Char)

### `funnel.snippet`

_Funnel Snippet Definition_

**Key Fields**:
- `name` (Char)
- `technical_name` (Char)
- `sequence` (Integer)
- `category` (Selection)
- `template_xml_id` (Char)
- `field_schema` (Text)
- `thumbnail` (Binary)
- `description` (Text)
- `copywriting_hints` (Text)
- `active` (Boolean)

### `funnel.template`

_Funnel Template_

**Key Fields**:
- `name` (Char)
- `description` (Text)
- `funnel_type` (Selection)
- `template_structure` (Text)
- `thumbnail` (Binary)
- `preview_url` (Char)
- `usage_count` (Integer)
- `visibility` (Selection)
- `author_id` (Many2one)
- `company_id` (Many2one)

### `sam.funnel.context`

_SAM Funnel Building Context_
