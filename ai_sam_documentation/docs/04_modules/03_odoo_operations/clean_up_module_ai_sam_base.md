# ai_sam_base Module Cleanup Guide

**Audit Date:** 2025-12-19
**Auditor:** CTO Auditor Agent
**Module Version:** 18.0.2.37
**Overall Score:** 6/10 (Good - Acceptable with Notes)

---

## Executive Summary

This document catalogs technical debt and cleanup patterns identified in the `ai_sam_base` module. Use this as a roadmap for systematic cleanup before adding major new features.

| Category | Issues Found | Priority |
|----------|--------------|----------|
| Class Collisions | 1 | HIGH |
| Deprecated Code | 6 locations | HIGH |
| DRY Violations | 5 files | MEDIUM |
| Auth Pattern Scatter | 6 files | MEDIUM |
| Import Wizard Overlap | 3 files | LOW |
| Model Type Errors | 1 | MEDIUM |

**Estimated Cleanup Time:** 2-4 hours for critical issues, 1-2 days for full cleanup

---

## Table of Contents

1. [Critical Issues (Must Fix)](#1-critical-issues-must-fix)
2. [Medium Priority (Tech Debt)](#2-medium-priority-tech-debt)
3. [Low Priority (Nice to Have)](#3-low-priority-nice-to-have)
4. [Cleanup Patterns Catalog](#4-cleanup-patterns-catalog)
5. [Module Statistics](#5-module-statistics)
6. [Verification Checklist](#6-verification-checklist)

---

## 1. Critical Issues (Must Fix)

### 1.1 Class Name Collision: ResConfigSettings

**Severity:** HIGH
**Risk:** Python import order determines which class wins; confusing for developers

**Problem:**
Two files define the same class with the same `_inherit`:

| File | Lines | Status |
|------|-------|--------|
| `models/res_config_settings.py` | 16 | EMPTY (commented out code) |
| `models/settings.py` | 34 | ACTIVE (4 settings fields) |

**Root Cause:**
`res_config_settings.py` was gutted but never deleted when `settings.py` was added.

**Fix Steps:**

```bash
# Step 1: Verify settings.py has all needed fields
# (It does - ai_automator_enabled, canvas_auto_layout, workflow_execution_timeout, enable_debug_logging)

# Step 2: Delete the empty file
rm models/res_config_settings.py

# Step 3: Update __init__.py - remove this line:
# from . import res_config_settings  # Line 26
```

**Files to Modify:**
- DELETE: `models/res_config_settings.py`
- EDIT: `models/__init__.py` (remove line 26)

---

### 1.2 Deprecated Code: sam_user_profile.py

**Severity:** HIGH
**Deprecated Since:** 2025-12-17 (2 days ago)
**Replacement:** `ai.access.gate` model

**Deprecated Items:**

| Location | What | Replacement |
|----------|------|-------------|
| Line 169-175 | `approved_file_paths` field | `ai.access.gate` records |
| Line 504-536 | `approve_file_path()` method | `ai.access.gate.action_approve()` |
| Line 538-552 | `check_path_permission()` method | `ai.access.gate.check_path_access()` |

**Fix Steps:**

```python
# Step 1: Verify ai.access.gate is working
# Run this in Odoo shell:
env['ai.access.gate'].search_count([])  # Should return records

# Step 2: Verify no code calls deprecated methods
# Search codebase for:
#   - .approve_file_path(
#   - .check_path_permission(
#   - .approved_file_paths

# Step 3: If safe, remove deprecated code blocks
# Lines 169-175: Remove field definition
# Lines 504-552: Remove both deprecated methods
```

**Files to Modify:**
- EDIT: `models/sam_user_profile.py`

---

### 1.3 Deprecated Code: api_service_provider.py

**Severity:** MEDIUM
**Multiple deprecated items with "REMOVED" comments**

| Line | Comment | Action |
|------|---------|--------|
| 116 | `# REMOVED 2025-12-12: supplier field removed` | Remove comment (field already gone) |
| 288 | `# DEPRECATED: Single service type` | Document or remove backwards compat |
| 1111 | `# REMOVED 2025-12-12: _onchange_supplier()` | Remove comment |
| 1356 | `# REMOVED 2025-12-12: _onchange_supplier_connector()` | Remove comment |
| 1869, 1932 | `# self.env.cr.commit()  # REMOVED` | Remove commented code |

**Fix Steps:**

```python
# These are just cleanup comments - search and remove:
# "# REMOVED 2025-12-12"
# "# self.env.cr.commit()  # REMOVED"
```

---

### 1.4 Deprecated Code: canvas_controller.py

**Severity:** LOW
**Location:** Lines 153-155

```python
# DEPRECATED 2025-10-31 Phase 1 - Creatives now uses canvas.json_definition instead
# TODO: Remove this entire elif block once creatives frontend is updated
```

**Action:** Verify frontend updated, then remove the elif block.

---

## 2. Medium Priority (Tech Debt)

### 2.1 Cost Calculation Duplication (DRY Violation)

**Severity:** MEDIUM
**Files Affected:** 5

The same cost calculation formula appears in multiple places:

```python
# This pattern repeated 5+ times:
input_cost = (tokens / 1_000_000) * cost_per_1m_input_tokens
output_cost = (tokens / 1_000_000) * cost_per_1m_output_tokens
total_cost = input_cost + output_cost
```

**Locations:**

| File | Method | Line |
|------|--------|------|
| `ai_agent_execution.py` | `_compute_cost()` | 141 |
| `ai_cost_optimizer.py` | inline calculation | 336-385 |
| `ai_provider_model.py` | `_compute_cost_summary()` | 108 |
| `ai_provider_model.py` | `_compute_cost_per_quality_point()` | 207 |
| `ai_service_cost_comparison.py` | `_compute_cost_quality_ratio()` | 220-247 |
| `ai_token_usage.py` | `_compute_cost()` | 221-260 |

**Fix: Create Shared Utility**

Add to `ai_cost_optimizer.py`:

```python
@api.model
def calculate_token_cost(self, input_tokens, output_tokens, cost_per_1m_input, cost_per_1m_output):
    """
    Centralized cost calculation for AI token usage.

    Args:
        input_tokens: Number of input tokens
        output_tokens: Number of output tokens
        cost_per_1m_input: Cost per million input tokens (USD)
        cost_per_1m_output: Cost per million output tokens (USD)

    Returns:
        dict: {'input_cost': float, 'output_cost': float, 'total_cost': float}
    """
    input_cost = (input_tokens / 1_000_000) * cost_per_1m_input
    output_cost = (output_tokens / 1_000_000) * cost_per_1m_output
    return {
        'input_cost': input_cost,
        'output_cost': output_cost,
        'total_cost': input_cost + output_cost
    }
```

Then refactor other models to use:
```python
costs = self.env['ai.cost.optimizer'].calculate_token_cost(
    input_tokens, output_tokens,
    provider.cost_per_1m_input_tokens,
    provider.cost_per_1m_output_tokens
)
```

---

### 2.2 Credential/Auth Pattern Scattering

**Severity:** MEDIUM
**Files Affected:** 6

Authentication configuration scattered across multiple models with no single source of truth:

| Model | Auth-Related Fields |
|-------|---------------------|
| `api_credentials.py` | `credential_type`, `credential_data`, `service_type`, OAuth status |
| `api_service_provider.py` | `api_key`, `auth_type`, `oauth_*` fields, `temp_api_key` |
| `ai_service_type.py` | `auth_method`, `auth_required`, `required_credentials` |
| `ai_brain.py` | Provider key lookup logic |
| `mcp_server_config.py` | API key reference |

**Recommendation:**

Consolidate into clear responsibilities:
1. **`api_credentials.py`** - Secret storage (keys, tokens, OAuth data)
2. **`api_service_provider.py`** - Provider configuration (which auth method to use)
3. **Remove** auth fields from `ai_service_type.py` (metadata only, not config)

---

### 2.3 Model Type Error: ai_conversation_import

**Severity:** MEDIUM
**File:** `models/ai_conversation_import.py`

**Problem:**
This wizard is defined as `models.Model` (persistent) instead of `models.TransientModel` (temporary).

```python
# Current (WRONG for a wizard):
class AIConversationImport(models.Model):
    _name = 'ai.conversation.import'

# Should be:
class AIConversationImport(models.TransientModel):
    _name = 'ai.conversation.import'
```

**Impact:**
- Records accumulate in database forever
- Wastes storage
- Violates Odoo wizard pattern

**Fix:**

```python
# Change line 20 from:
class AIConversationImport(models.Model):
# To:
class AIConversationImport(models.TransientModel):
```

**Note:** After changing, existing records will remain. Consider a migration to clean them or leave them (harmless but wasteful).

---

### 2.4 Unresolved TODOs

**Severity:** LOW-MEDIUM

| File | Line | TODO | Priority |
|------|------|------|----------|
| `services/api_services.py` | 175 | Extract streaming logic from ai_service.py | LOW |
| `services/http_routes.py` | 75, 91 | Phase 3 - Extract from sam_chat_controller.py | LOW |
| `models/ai_branches.py` | 238 | Implement actual statistics when canvas types tracked | LOW |
| `models/ai_brain.py` | 1319 | Investigate why benchmark logging hangs | MEDIUM |
| `models/ai_brain.py` | 2891 | Implement Google Gemini streaming | MEDIUM |
| `models/ai_memory_config.py` | 388 | Query actual graph node count | LOW |
| `models/mcp_server_generator.py` | 499 | Implement sales tools | LOW |
| `models/sam_mode_context.py` | 437 | Get server URL from system config | LOW |

---

## 3. Low Priority (Nice to Have)

### 3.1 Import Wizard Consolidation

**Severity:** LOW
**Files:** 3 similar wizards

| Wizard | Purpose | Format |
|--------|---------|--------|
| `ai_conversation_history_importer.py` | Import conversations | JSON |
| `ai_conversation_import.py` | Import conversations | ZIP/JSON/Directory |
| `ai_memory_import_wizard.py` | Restore backup | XLSX |

**Consideration:**
Could merge first two into single wizard with format auto-detection. However, they work independently, so this is optimization not bug fix.

---

### 3.2 Large File Refactoring Candidates

Files over 1,000 lines that could benefit from splitting:

| File | Lines | Potential Split |
|------|-------|-----------------|
| `api_service_provider.py` | 3,629 | Vendor templates → separate file |
| `ai_brain.py` | 3,581 | Streaming logic → separate file |
| `sam_ai_chat_controller.py` | 1,991 | Route groups → multiple controllers |

---

## 4. Cleanup Patterns Catalog

### Pattern 1: Delete File with Import Cleanup

```python
{
    'action': 'DELETE_FILE_WITH_IMPORT',
    'file': 'models/res_config_settings.py',
    'init_file': 'models/__init__.py',
    'import_line': 'from . import res_config_settings',
    'reason': 'Class collision with settings.py'
}
```

### Pattern 2: Remove Deprecated Block

```python
{
    'action': 'REMOVE_DEPRECATED_BLOCK',
    'file': 'models/sam_user_profile.py',
    'markers': {
        'field': {
            'start': '# DEPRECATED (2025-12-17): File path permissions',
            'field_name': 'approved_file_paths'
        },
        'methods': ['approve_file_path', 'check_path_permission']
    },
    'replacement_model': 'ai.access.gate',
    'verify_before_delete': True
}
```

### Pattern 3: Extract to Utility (DRY)

```python
{
    'action': 'EXTRACT_TO_UTILITY',
    'source_files': [
        'ai_agent_execution.py',
        'ai_cost_optimizer.py',
        'ai_provider_model.py',
        'ai_token_usage.py'
    ],
    'pattern': r'(input_tokens|tokens)\s*/\s*1_000_000\s*\*\s*cost',
    'target_file': 'ai_cost_optimizer.py',
    'utility_name': 'calculate_token_cost'
}
```

### Pattern 4: Change Model Type

```python
{
    'action': 'CHANGE_MODEL_TYPE',
    'file': 'models/ai_conversation_import.py',
    'line': 20,
    'from': 'models.Model',
    'to': 'models.TransientModel',
    'reason': 'Wizard should not persist records permanently'
}
```

### Pattern 5: Remove Dead Comments

```python
{
    'action': 'REMOVE_DEAD_COMMENTS',
    'file': 'models/api_service_provider.py',
    'patterns': [
        '# REMOVED 2025-12-12',
        '# self.env.cr.commit()  # REMOVED'
    ]
}
```

---

## 5. Module Statistics

### File Counts

| Type | Count |
|------|-------|
| Python Files | 72 |
| Total Lines of Code | 30,651 |
| Models (Regular) | 35 |
| Models (Abstract) | 5 |
| Models (Transient) | 3 |
| Controllers | 10 |
| Services | 6 |
| API Endpoints | 67+ |

### Code Smell Markers

| Marker | Count |
|--------|-------|
| `# DEPRECATED` | 6 |
| `# TODO` | 8 |
| `# REMOVED` | 6 |
| `# FIXME` | 0 |
| `# HACK` | 0 |
| `pass` statements | 11 |
| `raise NotImplementedError` | 1 |

### Largest Files

| File | Lines |
|------|-------|
| api_service_provider.py | 3,629 |
| ai_brain.py | 3,581 |
| sam_ai_chat_controller.py | 1,991 |
| ai_conversation.py | 877 |
| ai_conversation_import.py | 733 |

---

## 6. Verification Checklist

### Before Starting Cleanup

- [ ] Backup database
- [ ] Run existing tests: `python -m pytest`
- [ ] Note current module version: 18.0.2.37
- [ ] Create git branch: `git checkout -b cleanup/ai_sam_base`

### After Each Fix

- [ ] Module installs: `odoo -u ai_sam_base`
- [ ] No Python errors in logs
- [ ] Basic functionality works (SAM chat responds)
- [ ] Run tests if available

### After All Fixes

- [ ] Full module upgrade test
- [ ] Test conversation import wizard
- [ ] Test cost calculations display correctly
- [ ] Test ai.access.gate permissions work
- [ ] Update module version in `__manifest__.py`
- [ ] Commit with descriptive message

---

## Cleanup Execution Order

**Recommended sequence for minimal risk:**

1. **DELETE res_config_settings.py** (5 min) - No dependencies, immediate win
2. **Remove dead comments in api_service_provider.py** (10 min) - Safe cleanup
3. **Fix ai_conversation_import model type** (5 min) - Low risk
4. **Remove deprecated sam_user_profile code** (30 min) - Verify ai.access.gate first
5. **Extract cost calculation utility** (1 hour) - Refactoring, needs testing
6. **Address TODOs** (varies) - Pick high-value items

---

## Appendix: CTO Principles Applied

| Principle | Application |
|-----------|-------------|
| **Measure First** | Counted issues before proposing fixes |
| **Boring Patterns** | Recommend standard Odoo patterns (TransientModel, shared utilities) |
| **Build for 10x** | Cleanup enables sustainable growth |
| **Optimize User Time** | Prioritized by developer impact |
| **File Discipline** | Identified unauthorized file accumulation |

---

*Document generated by CTO Auditor Agent - 2025-12-19*
