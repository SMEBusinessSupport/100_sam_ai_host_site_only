# ai_sam_workflows_templates - Database Schema

Auto-generated model documentation.

## Models (2 total)

### `workflow.template`

_Workflow Template_

**Key Fields**:
- `name` (Char)
- `description` (Text)
- `workflow_type` (Selection)
- `json_definition` (Text)
- `documentation` (Html)
- `category` (Selection)
- `tag_ids` (Many2many)
- `author_id` (Many2one)
- `visibility` (Selection)
- `usage_count` (Integer)

### `workflow.template.tag`

_Workflow Template Tag_

**Key Fields**:
- `name` (Char)
- `color` (Integer)
- `template_ids` (Many2many)
