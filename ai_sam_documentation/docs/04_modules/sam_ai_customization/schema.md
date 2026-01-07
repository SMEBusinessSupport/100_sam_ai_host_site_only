# sam_ai_customization - Database Schema

Auto-generated model documentation.

## Models (4 total)

### `sam.field.creator`

_SAM Field Creator_

**Key Fields**:
- `name` (Char)
- `model_id` (Many2one)
- `model_name` (Char)
- `field_id` (Many2one)
- `field_name` (Char)
- `field_type` (Selection)
- `relation_model_id` (Many2one)
- `relation_field` (Char)
- `selection_options` (Text)
- `field_required` (Boolean)

### `sam.view.customization`

_SAM View Customization_

**Key Fields**:
- `customizer_id` (Many2one)
- `sequence` (Integer)
- `operation` (Selection)
- `field_id` (Many2one)
- `field_name` (Char)
- `model_id` (Many2one)
- `target_type` (Selection)
- `target_field_name` (Char)
- `target_group_string` (Char)
- `target_xpath` (Char)

### `sam.view.customizer`

_SAM View Customizer_

**Key Fields**:
- `display_name` (Char)
- `base_view_id` (Many2one)
- `model_id` (Many2one)
- `model_name` (Char)
- `view_type` (Selection)
- `inherited_view_id` (Many2one)
- `customization_ids` (One2many)
- `customization_count` (Integer)
- `state` (Selection)
- `error_message` (Text)

### `display_name`

**Key Fields**:
- `display_name` (Char)
- `base_view_id` (Many2one)
- `model_id` (Many2one)
- `model_name` (Char)
- `view_type` (Selection)
- `inherited_view_id` (Many2one)
- `customization_ids` (One2many)
- `customization_count` (Integer)
- `state` (Selection)
- `error_message` (Text)
