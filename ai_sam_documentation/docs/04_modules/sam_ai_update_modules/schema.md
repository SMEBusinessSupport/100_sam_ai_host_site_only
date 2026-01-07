# sam_ai_update_modules - Database Schema

Auto-generated model documentation.

## Models (1 total)

### `sam.upgrade.queue`

_SAM Module Upgrade Queue_

**Key Fields**:
- `name` (Char)
- `module_id` (Many2one)
- `module_name` (Char)
- `position` (Integer)
- `state` (Selection)
- `started_at` (Date)
- `completed_at` (Date)
- `error_message` (Text)
