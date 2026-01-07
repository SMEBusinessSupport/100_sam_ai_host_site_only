# ai_sam_insights - Database Schema

Auto-generated model documentation.

## Models (8 total)

### `insights.finding`

_SAM AI Insights Finding_

**Key Fields**:
- `fingerprint` (Char)
- `scan_id` (Many2one)
- `first_seen_scan_id` (Many2one)
- `first_seen_date` (Date)
- `last_seen_date` (Date)
- `occurrence_count` (Integer)
- `status` (Selection)
- `severity` (Selection)
- `severity_order` (Integer)
- `category` (Selection)

### ` - `

_SAM AI Insights Relationship_

**Key Fields**:
- `fingerprint` (Char)
- `scan_id` (Many2one)
- `first_seen_scan_id` (Many2one)
- `first_seen_date` (Date)
- `last_seen_date` (Date)
- `occurrence_count` (Integer)
- `status` (Selection)
- `severity` (Selection)
- `severity_order` (Integer)
- `category` (Selection)

### `insights.relationship`

**Key Fields**:
- `fingerprint` (Char)
- `scan_id` (Many2one)
- `first_seen_scan_id` (Many2one)
- `first_seen_date` (Date)
- `last_seen_date` (Date)
- `occurrence_count` (Integer)
- `status` (Selection)
- `severity` (Selection)
- `severity_order` (Integer)
- `category` (Selection)

### `insights.scan`

_SAM AI Ecosystem Scan_

**Key Fields**:
- `display_name` (Char)
- `scan_date` (Date)
- `default` (Date)
- `state` (Selection)
- `base_path` (Char)
- `module_filter` (Char)
- `include_registry` (Boolean)
- `use_default_settings` (Boolean)
- `health_score` (Integer)
- `health_status` (Char)

### `display_name`

**Key Fields**:
- `display_name` (Char)
- `scan_date` (Date)
- `default` (Date)
- `state` (Selection)
- `base_path` (Char)
- `module_filter` (Char)
- `include_registry` (Boolean)
- `use_default_settings` (Boolean)
- `health_score` (Integer)
- `health_status` (Char)

### `insights.scan.module`

_Discovered Module for Scanning_

**Key Fields**:
- `settings_id` (Many2one)
- `name` (Char)
- `technical_name` (Char)
- `path` (Char)
- `selected` (Boolean)
- `version` (Char)
- `summary` (Char)
- `author` (Char)
- `category` (Char)
- `installable` (Boolean)

### `name`

**Key Fields**:
- `settings_id` (Many2one)
- `name` (Char)
- `technical_name` (Char)
- `path` (Char)
- `selected` (Boolean)
- `version` (Char)
- `summary` (Char)
- `author` (Char)
- `category` (Char)
- `installable` (Boolean)

### `insights.scan.settings`

_Scan Default Settings_

**Key Fields**:
- `name` (Char)
- `default_scan_path` (Char)
- `include_registry` (Boolean)
- `module_ids` (One2many)
- `total_modules` (Integer)
- `selected_modules` (Integer)
- `last_path_scan` (Date)
- `last_path_scan` (Date)
