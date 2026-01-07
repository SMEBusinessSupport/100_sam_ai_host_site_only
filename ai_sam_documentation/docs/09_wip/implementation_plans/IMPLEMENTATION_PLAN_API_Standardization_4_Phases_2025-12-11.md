# API Provider Standardization - Implementation Plan
**Date**: 2025-12-11
**Author**: CTO Developer (Claude Code Session)
**Status**: Ready for Implementation
**Reference**: [ARCHITECTURE_API_Provider_Standardization_2025-12-11.md](./ARCHITECTURE_API_Provider_Standardization_2025-12-11.md)

---

## Executive Summary

This document extends the architecture report with a complete implementation plan addressing **two distinct layers**:

1. **Service Metadata Layer** (Phases 1-3) - From architecture doc
2. **Runtime API Format Layer** (Phase 4) - From earlier debugging session

The architecture doc correctly identifies the service metadata standardization needs, but does not address the runtime API calling mechanism that was fixed during the chat debugging session (see [DATA_WORKFLOW_Chat_API_Flow_2025-12-11.md](./DATA_WORKFLOW_Chat_API_Flow_2025-12-11.md)).

---

## Two-Layer Problem Analysis

### Layer 1: Service Metadata (Architecture Doc Scope)

**Problem**: 492 providers in vendor library, only 7 have detailed configs. Missing fields prevent:
- Displaying available models (GPT-4, Claude 3, etc.)
- OAuth scope requirements
- Multi-credential providers (account_name + api_key)
- Onboarding guidance

**Solution**: Extend `ai.service.type` model with new fields, create JSON schema validation.

### Layer 2: Runtime API Format (Earlier Session Scope)

**Problem**: Different providers use different API formats at runtime:
- Anthropic format: `messages` array + separate `system` parameter
- OpenAI format: `messages` array with system as first message

**Current State**: Hardcoded `API_FORMAT_MAP` in `ai_service.py` (30+ providers mapped to 2 formats)

**Solution**: Move format mapping to database/JSON for UI-based configuration.

---

## 4-Phase Implementation Plan

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           PHASE OVERVIEW                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  PHASE 1: Model Enhancement (ai.service.type)                    [1-2 hrs] │
│  ├── Add 6 new fields to Odoo model                                        │
│  ├── Add config_completeness computed field                                │
│  └── Update ACL if needed                                                   │
│                                                                             │
│  PHASE 2: Service Populator Update                               [1 hr]    │
│  ├── Map new JSON fields to Odoo model                                     │
│  ├── Handle missing fields gracefully                                       │
│  └── Set config_completeness based on data                                 │
│                                                                             │
│  PHASE 3: JSON Schema & Validation                               [1-2 hrs] │
│  ├── Create service_config.schema.json                                     │
│  ├── Add schema_version to existing 7 service configs                      │
│  └── Optional: Add schema validation to populator                          │
│                                                                             │
│  PHASE 4: Runtime API Format (Data-Driven)                       [2-3 hrs] │
│  ├── Add api_format field to api.service.provider                          │
│  ├── Remove hardcoded API_FORMAT_MAP from ai_service.py                    │
│  ├── Read format from provider record at runtime                           │
│  └── Update cache to include api_format                                    │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Phase 1: Model Enhancement

**Priority**: HIGH
**Effort**: 1-2 hours
**File**: `ai_sam_base/models/ai_service_type.py`

### New Fields to Add

```python
# ==========================================================================
# PHASE 1: Service Metadata Enhancement (2025-12-11)
# Reference: ARCHITECTURE_API_Provider_Standardization_2025-12-11.md
# ==========================================================================

# Schema Version Tracking
schema_version = fields.Char(
    string='Schema Version',
    default='1.0',
    help='Version of the service config schema this record follows'
)

# Supported Models (for AI providers)
supported_models = fields.Json(
    string='Supported Models',
    help='List of model identifiers (e.g., ["gpt-4", "gpt-3.5-turbo", "claude-3-sonnet"])'
)

# OAuth Scopes (for OAuth providers)
required_scopes = fields.Json(
    string='Required OAuth Scopes',
    help='OAuth scopes required (e.g., ["gmail.send", "gmail.readonly"])'
)

# Multi-Credential Support
required_credentials = fields.Json(
    string='Required Credentials',
    help='Additional credential fields beyond API key (e.g., account_name for ActiveCampaign)'
)

# Configuration Hints (onboarding help)
configuration_hints = fields.Json(
    string='Configuration Hints',
    help='Setup instructions: {auth_setup: "...", common_issues: [...]}'
)

# Config Completeness Tracking
config_completeness = fields.Selection([
    ('none', 'Not Configured'),
    ('basic', 'Basic (Metadata Only)'),
    ('full', 'Full (Ready for Integration)')
], string='Configuration Completeness', default='none',
   compute='_compute_config_completeness', store=True)
```

### Compute Method

```python
@api.depends('api_base_url', 'operations', 'auth_method')
def _compute_config_completeness(self):
    """Determine config completeness based on populated fields"""
    for record in self:
        if record.operations and record.api_base_url and record.auth_method:
            record.config_completeness = 'full'
        elif record.vendor_key and record.service_key:
            record.config_completeness = 'basic'
        else:
            record.config_completeness = 'none'
```

### Success Criteria
- [ ] 6 new fields added to model
- [ ] Module upgrade succeeds without errors
- [ ] Existing data preserved
- [ ] Can filter by `config_completeness = 'full'`

---

## Phase 2: Service Populator Update

**Priority**: HIGH
**Effort**: 1 hour
**File**: `ai_sam_base/controllers/service_populator_controller.py`

### Update service_values Dict

```python
service_values = {
    # ... existing fields ...

    # NEW: Schema version (Phase 1)
    'schema_version': service_data.get('schema_version', '1.0'),

    # NEW: Model support
    'supported_models': service_data.get('supported_models', []),

    # NEW: OAuth scopes
    'required_scopes': service_data.get('required_scopes', []),

    # NEW: Multi-credential support
    'required_credentials': service_data.get('required_credentials', []),

    # NEW: Configuration hints
    'configuration_hints': service_data.get('configuration_hints', {}),
}
```

### Success Criteria
- [ ] Populator handles new fields
- [ ] Missing fields default gracefully (no errors)
- [ ] Re-import existing 7 services works
- [ ] New fields populated where present in JSON

---

## Phase 3: JSON Schema & Validation

**Priority**: MEDIUM
**Effort**: 1-2 hours
**Files**:
- `ai_sam/static/src/vendor_library/_schema/service_config.schema.json` (NEW)
- `ai_sam/static/src/vendor_library/OpenAi/services/*.json` (UPDATE)
- `ai_sam/static/src/vendor_library/Google/services/*.json` (UPDATE)
- `ai_sam/static/src/vendor_library/ActiveCampaign/services/*.json` (UPDATE)

### Create Schema File

See architecture doc for full schema. Key additions:
- `schema_version` (string, default "1.0")
- `supported_models` (array of strings)
- `required_scopes` (array of strings)
- `required_credentials` (array of objects)
- `configuration_hints` (object)

### Update Existing Service Configs

Add to each of the 7 existing service JSON files:
```json
{
  "schema_version": "1.0",
  // ... existing fields ...
}
```

### Success Criteria
- [ ] Schema file created and valid JSON Schema
- [ ] All 7 existing configs validate against schema
- [ ] schema_version added to all existing configs

---

## Phase 4: Runtime API Format (Data-Driven)

**Priority**: HIGH (impacts chat functionality)
**Effort**: 2-3 hours
**Files**:
- `ai_sam_base/models/api_service_provider.py` - Add field
- `ai_sam_base/models/ai_service.py` - Remove hardcoded map, use field
- `ai_sam_base/models/sam_user_settings.py` - Include in cache

### Current State (Hardcoded)

From `ai_service.py`:
```python
API_FORMAT_MAP = {
    'anthropic': 'anthropic',
    'claude': 'anthropic',
    'openai': 'openai',
    'azure_openai': 'openai',
    'groq': 'openai',
    'together': 'openai',
    'mistral': 'openai',
    'deepseek': 'openai',
    'ollama': 'openai',
    'openrouter': 'openai',
    # ... 20+ more providers
}
```

### Target State (Data-Driven)

#### Step 4.1: Add Field to api.service.provider

```python
# In api_service_provider.py
api_format = fields.Selection([
    ('openai', 'OpenAI Compatible'),
    ('anthropic', 'Anthropic/Claude'),
    ('google', 'Google/Gemini'),
    ('custom', 'Custom Handler'),
], string='API Format', default='openai',
   help='Which API format this provider uses for chat completions')
```

#### Step 4.2: Update ai_service.py

Replace:
```python
api_format = self._get_api_format(config.api_provider)  # Uses hardcoded map
```

With:
```python
# Get format from provider record (data-driven)
api_format = config.api_format or self._get_api_format_fallback(config.api_provider)
```

Keep `API_FORMAT_MAP` as fallback for providers without explicit format set.

#### Step 4.3: Update Provider Cache

In `sam_user_settings.py`, the cached config already includes `api_provider`. Add `api_format`:

```python
cache_data = {
    'provider_id': selected_provider.id,
    'provider_name': selected_provider.name,
    'model_name': recommended_model_name,
    'api_provider': config.api_provider,
    'api_format': config.api_format,  # NEW
    'estimated_cost': recommendation.get('estimated_cost', 0),
}
```

#### Step 4.4: Auto-Populate Format from Supplier

When provider is created/updated with a `supplier` value, auto-set `api_format`:

```python
def write(self, vals):
    result = super().write(vals)

    # Auto-set api_format based on supplier if not explicitly set
    if 'supplier' in vals and 'api_format' not in vals:
        for provider in self:
            if not provider.api_format:
                provider.api_format = provider._detect_api_format_from_supplier()

    return result

def _detect_api_format_from_supplier(self):
    """Detect API format from supplier name"""
    supplier = (self.supplier or '').lower()
    if 'anthropic' in supplier or 'claude' in supplier:
        return 'anthropic'
    elif 'google' in supplier or 'gemini' in supplier:
        return 'google'
    else:
        return 'openai'  # Default to OpenAI format (most common)
```

### Success Criteria
- [ ] `api_format` field added to `api.service.provider`
- [ ] Existing providers auto-populated with correct format
- [ ] Chat works with format read from database
- [ ] Hardcoded `API_FORMAT_MAP` only used as fallback
- [ ] Cache includes `api_format`
- [ ] UI allows changing provider's API format

---

## Dependency Graph

```
Phase 1 ──┬── Phase 2 ──── Phase 3
          │
          └── (independent) ── Phase 4
```

- Phases 1-2 are tightly coupled (model + populator)
- Phase 3 depends on Phases 1-2 (needs fields to exist)
- Phase 4 is independent (different model: `api.service.provider` vs `ai.service.type`)

---

## Recommended Execution Order

### Option A: Metadata First (Architecture Doc Path)
1. Phase 1 + Phase 2 together (2-3 hours)
2. Phase 3 (1-2 hours)
3. Phase 4 (2-3 hours)

**Total**: ~6-8 hours

### Option B: Runtime First (Chat Functionality Priority)
1. Phase 4 (2-3 hours) - Immediate benefit to chat
2. Phase 1 + Phase 2 (2-3 hours)
3. Phase 3 (1-2 hours)

**Total**: ~6-8 hours (same, different order)

### Recommendation

**Option B** - Phase 4 first, because:
- Chat is already working with hardcoded map
- Making it data-driven enables UI configuration immediately
- Phases 1-3 are about future-proofing the vendor library (less urgent)

---

## Risk Assessment

| Phase | Risk | Likelihood | Impact | Mitigation |
|-------|------|------------|--------|------------|
| 1 | Field type errors | Low | Medium | Use Json fields for flexibility |
| 2 | Missing field breaks import | Low | High | Default all new fields |
| 3 | Schema too strict | Medium | Low | Start permissive, tighten later |
| 4 | Wrong format breaks chat | Medium | High | Keep fallback map, test thoroughly |

---

## Version Tracking

After each phase, bump module version:

| Phase | Module | Version | Comment |
|-------|--------|---------|---------|
| Current | ai_sam_base | 18.0.2.25 | Defensive caching |
| Phase 1 | ai_sam_base | 18.0.2.26 | Service type model enhancement |
| Phase 2 | ai_sam_base | 18.0.2.27 | Populator new field mapping |
| Phase 3 | ai_sam | TBD | JSON schema validation |
| Phase 4 | ai_sam_base | 18.0.2.28 | Data-driven API format |

---

## Files to Modify (Complete List)

### Phase 1
| File | Action |
|------|--------|
| `ai_sam_base/models/ai_service_type.py` | Add 6 fields + compute method |
| `ai_sam_base/__manifest__.py` | Bump version |

### Phase 2
| File | Action |
|------|--------|
| `ai_sam_base/controllers/service_populator_controller.py` | Map new fields |
| `ai_sam_base/__manifest__.py` | Bump version |

### Phase 3
| File | Action |
|------|--------|
| `ai_sam/static/src/vendor_library/_schema/service_config.schema.json` | CREATE |
| `ai_sam/static/src/vendor_library/OpenAi/services/*.json` | Add schema_version |
| `ai_sam/static/src/vendor_library/Google/services/*.json` | Add schema_version |
| `ai_sam/static/src/vendor_library/ActiveCampaign/services/*.json` | Add schema_version |

### Phase 4
| File | Action |
|------|--------|
| `ai_sam_base/models/api_service_provider.py` | Add api_format field |
| `ai_sam_base/models/ai_service.py` | Use field instead of hardcoded map |
| `ai_sam_base/models/sam_user_settings.py` | Include api_format in cache |
| `ai_sam_base/__manifest__.py` | Bump version |

---

## Related Documents

1. [ARCHITECTURE_API_Provider_Standardization_2025-12-11.md](./ARCHITECTURE_API_Provider_Standardization_2025-12-11.md) - Original architecture analysis
2. [DATA_WORKFLOW_Chat_API_Flow_2025-12-11.md](./DATA_WORKFLOW_Chat_API_Flow_2025-12-11.md) - Chat debugging session that revealed Phase 4 need

---

**Document Status**: Ready for Implementation
**Next Action**: Decide execution order (Option A or B), then begin Phase 1 or Phase 4
**Estimated Total Effort**: 6-8 hours across all phases
