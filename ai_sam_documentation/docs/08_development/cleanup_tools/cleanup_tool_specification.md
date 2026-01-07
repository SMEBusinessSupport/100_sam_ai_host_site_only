# Cleanup Annotation Specification

**Version:** 1.0
**Purpose:** Standardized markup system for AI-assisted code cleanup delegation

---

## Overview

This specification defines color-coded comment annotations that AI auditors can safely inject into code. Human developers can then scan for these markers and execute cleanup tasks with minimal context-switching.

**Key Principles:**
1. **Non-Breaking** - Annotations are comments only, never modify executable code
2. **Searchable** - Consistent prefixes for grep/IDE search
3. **Actionable** - Each annotation includes what to do, not just what's wrong
4. **Prioritized** - Color/severity system for triage
5. **Traceable** - Include audit date and ticket reference

---

## Annotation Format

```
# [CLEANUP:{SEVERITY}:{TYPE}] {Brief Description}
# Action: {What developer should do}
# Reason: {Why this is flagged}
# Ticket: {Reference} | Audit: {Date}
```

**Single-line shorthand:**
```
# [CLEANUP:RED:DELETE] Remove this file - class collision with settings.py
```

---

## Severity Levels (Color Coded)

### RED - Critical (Must Fix)
**Search:** `CLEANUP:RED`
**Meaning:** Blocking issues, bugs waiting to happen, or architectural violations

| Type Code | Meaning | Example |
|-----------|---------|---------|
| `DELETE` | Remove file/block entirely | Duplicate class definition |
| `COLLISION` | Name/class collision | Two files define same class |
| `SECURITY` | Security vulnerability | Exposed credentials |
| `BREAKING` | Will break in future | Deprecated API usage |

**Visual in IDE:**
```python
# ============================================================
# [CLEANUP:RED:COLLISION] CLASS NAME COLLISION
# This file conflicts with settings.py (both define ResConfigSettings)
# Action: DELETE this entire file
# Reason: Python import order makes behavior unpredictable
# Ticket: CLEANUP-001 | Audit: 2025-12-19
# ============================================================
```

---

### ORANGE - High Priority (Fix Soon)
**Search:** `CLEANUP:ORANGE`
**Meaning:** Technical debt that impacts development velocity

| Type Code | Meaning | Example |
|-----------|---------|---------|
| `DEPRECATED` | Code marked for removal | Old API still in use |
| `MIGRATE` | Needs migration to new pattern | Old field → new model |
| `DEAD_CODE` | Unreachable/unused code | Commented blocks |
| `WRONG_TYPE` | Incorrect model/field type | Model should be Transient |

**Visual in IDE:**
```python
# ------------------------------------------------------------
# [CLEANUP:ORANGE:DEPRECATED] Field moved to ai.access.gate
# Action: Remove field after verifying migration complete
# Verify: env['ai.access.gate'].search_count([]) > 0
# Ticket: CLEANUP-002 | Audit: 2025-12-19
# ------------------------------------------------------------
approved_file_paths = fields.Text(  # <-- REMOVE THIS
    string='[DEPRECATED] Approved File Paths',
```

---

### YELLOW - Medium Priority (Plan for Sprint)
**Search:** `CLEANUP:YELLOW`
**Meaning:** Code smells, DRY violations, improvement opportunities

| Type Code | Meaning | Example |
|-----------|---------|---------|
| `DRY` | Duplicated logic | Same formula in 5 files |
| `EXTRACT` | Should be utility/mixin | Repeated pattern |
| `REFACTOR` | Needs restructuring | God method, large file |
| `CONSOLIDATE` | Merge similar code | Multiple auth patterns |
| `TODO` | Existing TODO to address | Unimplemented feature |

**Visual in IDE:**
```python
# ............................................................
# [CLEANUP:YELLOW:DRY] Cost calculation duplicated in 5 files
# Action: Use self.env['ai.cost.optimizer'].calculate_token_cost()
# See: ai_cost_optimizer.py for shared implementation
# Ticket: CLEANUP-003 | Audit: 2025-12-19
# ............................................................
input_cost = (tokens / 1_000_000) * cost_per_1m_input_tokens  # <-- REPLACE
```

---

### GREEN - Low Priority (Backlog)
**Search:** `CLEANUP:GREEN`
**Meaning:** Nice-to-have improvements, optimization opportunities

| Type Code | Meaning | Example |
|-----------|---------|---------|
| `OPTIMIZE` | Performance improvement | N+1 query |
| `SPLIT` | File too large | 3000+ line file |
| `MERGE` | Similar files to combine | 3 import wizards |
| `DOCUMENT` | Needs better docs | Complex logic |
| `STYLE` | Code style issue | Inconsistent naming |

**Visual in IDE:**
```python
# . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
# [CLEANUP:GREEN:SPLIT] File has 3629 lines - consider splitting
# Suggestion: Extract vendor templates to api_vendor_templates.py
# Ticket: CLEANUP-004 | Audit: 2025-12-19
# . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
```

---

### BLUE - Information Only
**Search:** `CLEANUP:BLUE`
**Meaning:** Context for developers, not actionable

| Type Code | Meaning | Example |
|-----------|---------|---------|
| `NOTE` | Important context | Why code exists |
| `AUDIT` | Audit metadata | Score, date, auditor |
| `HISTORY` | Change history | When/why deprecated |

---

## Complete Type Reference

| Severity | Type | Action Required |
|----------|------|-----------------|
| RED | `DELETE` | Remove file/block |
| RED | `COLLISION` | Resolve naming conflict |
| RED | `SECURITY` | Fix vulnerability |
| RED | `BREAKING` | Update before it breaks |
| ORANGE | `DEPRECATED` | Remove after verification |
| ORANGE | `MIGRATE` | Move to new pattern |
| ORANGE | `DEAD_CODE` | Remove unused code |
| ORANGE | `WRONG_TYPE` | Change model/field type |
| YELLOW | `DRY` | Use shared implementation |
| YELLOW | `EXTRACT` | Create utility function |
| YELLOW | `REFACTOR` | Restructure code |
| YELLOW | `CONSOLIDATE` | Merge patterns |
| YELLOW | `TODO` | Implement missing feature |
| GREEN | `OPTIMIZE` | Improve performance |
| GREEN | `SPLIT` | Break into smaller files |
| GREEN | `MERGE` | Combine similar code |
| GREEN | `DOCUMENT` | Add documentation |
| GREEN | `STYLE` | Fix code style |
| BLUE | `NOTE` | Read for context |
| BLUE | `AUDIT` | Audit metadata |
| BLUE | `HISTORY` | Change history |

---

## Search Commands

### Find all cleanup tasks
```bash
grep -rn "CLEANUP:" --include="*.py" .
```

### Find by severity
```bash
grep -rn "CLEANUP:RED" --include="*.py" .
grep -rn "CLEANUP:ORANGE" --include="*.py" .
grep -rn "CLEANUP:YELLOW" --include="*.py" .
grep -rn "CLEANUP:GREEN" --include="*.py" .
```

### Find by type
```bash
grep -rn "CLEANUP:.*:DELETE" --include="*.py" .
grep -rn "CLEANUP:.*:DEPRECATED" --include="*.py" .
grep -rn "CLEANUP:.*:DRY" --include="*.py" .
```

### Count by severity
```bash
grep -c "CLEANUP:RED" --include="*.py" -r . | grep -v ":0"
```

---

## IDE Integration

### VS Code - Settings for highlighting

Add to `.vscode/settings.json`:
```json
{
  "todohighlight.keywords": [
    {
      "text": "CLEANUP:RED",
      "color": "white",
      "backgroundColor": "#FF0000",
      "overviewRulerColor": "#FF0000"
    },
    {
      "text": "CLEANUP:ORANGE",
      "color": "black",
      "backgroundColor": "#FFA500",
      "overviewRulerColor": "#FFA500"
    },
    {
      "text": "CLEANUP:YELLOW",
      "color": "black",
      "backgroundColor": "#FFFF00",
      "overviewRulerColor": "#FFFF00"
    },
    {
      "text": "CLEANUP:GREEN",
      "color": "white",
      "backgroundColor": "#228B22",
      "overviewRulerColor": "#228B22"
    },
    {
      "text": "CLEANUP:BLUE",
      "color": "white",
      "backgroundColor": "#4169E1",
      "overviewRulerColor": "#4169E1"
    }
  ]
}
```

---

## Annotation Examples by File

### Example 1: File to Delete
**File:** `models/res_config_settings.py`

```python
# ============================================================
# [CLEANUP:RED:DELETE] ENTIRE FILE FLAGGED FOR DELETION
# ============================================================
# Reason: Class collision with models/settings.py
#         Both define ResConfigSettings with _inherit='res.config.settings'
#         Python import order makes behavior unpredictable
#
# Action:
#   1. DELETE this file
#   2. Edit models/__init__.py - remove "from . import res_config_settings"
#   3. Test module upgrade: odoo -u ai_sam_base
#
# Ticket: CLEANUP-001 | Audit: 2025-12-19 | Score Impact: -1
# ============================================================

# -*- coding: utf-8 -*-
from odoo import api, fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    # ... rest of file
```

---

### Example 2: Deprecated Field
**File:** `models/sam_user_profile.py`

```python
    can_access_files = fields.Boolean(
        string='File Access',
        default=False,
        help='Can SAM read/write local files for this user?'
    )

    # ------------------------------------------------------------
    # [CLEANUP:ORANGE:DEPRECATED] Field replaced by ai.access.gate model
    # ------------------------------------------------------------
    # Deprecated: 2025-12-17
    # Replacement: ai.access.gate records with path-level permissions
    #
    # Action:
    #   1. Verify replacement working: env['ai.access.gate'].search_count([])
    #   2. Search for usages: grep -rn "approved_file_paths" --include="*.py"
    #   3. If no usages found, DELETE this field definition (lines 172-175)
    #
    # Ticket: CLEANUP-002 | Audit: 2025-12-19
    # ------------------------------------------------------------
    approved_file_paths = fields.Text(
        string='[DEPRECATED] Approved File Paths',
        help='DEPRECATED: Use ai.access.gate model instead.'
    )
```

---

### Example 3: DRY Violation
**File:** `models/ai_token_usage.py`

```python
    @api.depends('input_tokens', 'output_tokens', 'input_cost_per_token', 'output_cost_per_token')
    def _compute_cost(self):
        # ............................................................
        # [CLEANUP:YELLOW:DRY] Cost calculation duplicated in 5 files
        # ............................................................
        # Also in: ai_agent_execution.py, ai_cost_optimizer.py,
        #          ai_provider_model.py, ai_service_cost_comparison.py
        #
        # Action: Replace with shared utility call:
        #   costs = self.env['ai.cost.optimizer'].calculate_token_cost(
        #       record.input_tokens, record.output_tokens,
        #       record.input_cost_per_token * 1_000_000,
        #       record.output_cost_per_token * 1_000_000
        #   )
        #   record.cost_usd = costs['total_cost']
        #
        # Ticket: CLEANUP-003 | Audit: 2025-12-19
        # ............................................................
        for record in self:
            input_cost = record.input_tokens * record.input_cost_per_token
            output_cost = record.output_tokens * record.output_cost_per_token
            record.cost_usd = input_cost + output_cost
```

---

### Example 4: Wrong Model Type
**File:** `models/ai_conversation_import.py`

```python
# ------------------------------------------------------------
# [CLEANUP:ORANGE:WRONG_TYPE] Should be TransientModel not Model
# ------------------------------------------------------------
# Problem: Wizard defined as persistent Model
#          Records accumulate forever in database
#
# Action:
#   1. Change line 20: models.Model → models.TransientModel
#   2. Test module upgrade
#   3. Optionally clean old records:
#      DELETE FROM ai_conversation_import WHERE create_date < NOW() - INTERVAL '30 days'
#
# Ticket: CLEANUP-005 | Audit: 2025-12-19
# ------------------------------------------------------------

class AIConversationImport(models.Model):  # <-- CHANGE TO: models.TransientModel
    _name = 'ai.conversation.import'
```

---

### Example 5: Large File
**File:** `models/api_service_provider.py`

```python
# . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
# [CLEANUP:GREEN:SPLIT] File has 3629 lines
# . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
# Suggestion: Consider extracting to separate files:
#   - api_vendor_templates.py (lines 1150-1600) - Vendor configuration templates
#   - api_provider_oauth.py (lines 2800-3100) - OAuth implementation
#
# This is low priority - file works fine, just large for navigation
#
# Ticket: CLEANUP-006 | Audit: 2025-12-19
# . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
```

---

## Python Markup Tool Specification

### Tool: `cleanup_marker.py`

**Purpose:** Automatically inject cleanup annotations based on audit findings

**Input:** JSON audit report
**Output:** Modified Python files with annotations

### JSON Audit Format

```json
{
  "audit_date": "2025-12-19",
  "module": "ai_sam_base",
  "score": 6,
  "findings": [
    {
      "id": "CLEANUP-001",
      "severity": "RED",
      "type": "DELETE",
      "file": "models/res_config_settings.py",
      "line": 1,
      "scope": "file",
      "title": "ENTIRE FILE FLAGGED FOR DELETION",
      "reason": "Class collision with models/settings.py",
      "action": [
        "DELETE this file",
        "Edit models/__init__.py - remove 'from . import res_config_settings'",
        "Test module upgrade: odoo -u ai_sam_base"
      ],
      "score_impact": -1
    },
    {
      "id": "CLEANUP-002",
      "severity": "ORANGE",
      "type": "DEPRECATED",
      "file": "models/sam_user_profile.py",
      "line": 169,
      "scope": "block",
      "end_line": 175,
      "title": "Field replaced by ai.access.gate model",
      "reason": "Deprecated 2025-12-17, replacement model now active",
      "action": [
        "Verify replacement: env['ai.access.gate'].search_count([])",
        "Search for usages: grep -rn 'approved_file_paths'",
        "If safe, DELETE lines 169-175"
      ],
      "verification": "env['ai.access.gate'].search_count([]) > 0"
    }
  ]
}
```

### Tool CLI Interface

```bash
# Mark up files based on audit
python cleanup_marker.py --audit audit_report.json --output-dir ./marked

# Generate report only (no file modification)
python cleanup_marker.py --audit audit_report.json --report-only

# Remove all cleanup markers (post-cleanup)
python cleanup_marker.py --clean --path ./models

# Count markers by severity
python cleanup_marker.py --count --path ./models
```

### Tool Output Report

```
========================================
CLEANUP MARKUP REPORT: ai_sam_base
========================================
Audit Date: 2025-12-19
Module Score: 6/10

MARKERS INJECTED:
  RED:     3 (Critical - Must Fix)
  ORANGE:  4 (High Priority)
  YELLOW:  5 (Medium Priority)
  GREEN:   2 (Low Priority)
  ─────────
  TOTAL:  14 cleanup tasks

FILES MODIFIED:
  models/res_config_settings.py   [RED:DELETE]
  models/sam_user_profile.py      [ORANGE:DEPRECATED x2]
  models/api_service_provider.py  [ORANGE:DEAD_CODE, GREEN:SPLIT]
  models/ai_conversation_import.py [ORANGE:WRONG_TYPE]
  models/ai_token_usage.py        [YELLOW:DRY]
  models/ai_cost_optimizer.py     [YELLOW:DRY]
  ... (8 more files)

DEVELOPER WORKFLOW:
  1. grep -rn "CLEANUP:RED" --include="*.py" .  → Fix these FIRST
  2. grep -rn "CLEANUP:ORANGE" --include="*.py" . → Fix this sprint
  3. grep -rn "CLEANUP:YELLOW" --include="*.py" . → Plan for backlog
  4. grep -rn "CLEANUP:GREEN" --include="*.py" . → Nice to have

After cleanup, run: python cleanup_marker.py --clean --path .
========================================
```

---

## Developer Workflow

### For Developer Receiving Marked Code

1. **Pull latest code** with cleanup markers
2. **Search by severity:**
   ```bash
   grep -rn "CLEANUP:RED" --include="*.py" .
   ```
3. **Read the annotation** - it tells you exactly what to do
4. **Execute the action** - delete, refactor, or migrate
5. **Verify** - run any verification commands in the annotation
6. **Remove the marker** after completing the task
7. **Commit** with reference to ticket ID

### For AI Auditor Generating Markers

1. Run audit analysis
2. Generate JSON findings report
3. Run `cleanup_marker.py` to inject annotations
4. Commit marked code to cleanup branch
5. Create PR/task for developer assignment

---

## Benefits of This System

| Benefit | Description |
|---------|-------------|
| **Delegatable** | Developers don't need full context, annotation has everything |
| **Searchable** | Standard prefixes work with grep, IDE, CI tools |
| **Prioritized** | Color severity enables triage |
| **Verifiable** | Annotations include verification steps |
| **Removable** | Clean removal after task complete |
| **Automatable** | JSON format enables tooling |
| **Non-Breaking** | Comments only, code unchanged until human acts |

---

*Specification v1.0 - 2025-12-19*
