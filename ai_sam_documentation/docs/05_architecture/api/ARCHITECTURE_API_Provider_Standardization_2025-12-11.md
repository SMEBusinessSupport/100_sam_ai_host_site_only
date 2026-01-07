# API Provider Standardization Architecture
**Date**: 2025-12-11
**Author**: CTO Auditor
**Status**: Strategic Planning Complete - Ready for Implementation

---

## Executive Summary

SAM AI has a **492-provider vendor library** with metadata ready, but only **7 providers** have detailed service configurations. This document defines the architecture to enable progressive, on-demand population of service configs while maintaining consistency across all providers.

**Key Decision**: Option A (Boring Pattern) - Minimal changes to existing structure, add missing fields, create validation schema.

---

## Current State Analysis

### 3-Tier Architecture (Existing)

```
TIER 1: _registry/node_metadata.json
├── 492 providers with basic metadata
├── Fields: displayName, folder, credential_type, category, n8n_type
├── Purpose: UI listing, search, categorization
└── Status: COMPLETE

TIER 2: vendor_library/{Vendor}/api_config.json
├── 203 vendor folders exist
├── Fields: service, icon, folder, status, api_integration
├── Purpose: Provider-level config, icon references
└── Status: MOSTLY "visual_only" / "planned"

TIER 3: vendor_library/{Vendor}/services/*.json
├── Only 7 services populated
├── Fields: Full API config, operations, auth, rate limits
├── Purpose: Actual API integration configuration
└── Status: CRITICAL GAP - This is where real work lives
```

### Populated Services (Tier 3)

| Vendor | Service | File |
|--------|---------|------|
| OpenAI | Chat | `OpenAi/services/openai_chat.json` |
| OpenAI | Embeddings | `OpenAi/services/openai_embeddings.json` |
| OpenAI | DALL-E | `OpenAi/services/openai_dalle.json` |
| OpenAI | Whisper | `OpenAi/services/openai_whisper.json` |
| Google | Gmail | `Google/services/gmail.json` |
| Google | Drive | `Google/services/google_drive.json` |
| ActiveCampaign | CRM | `ActiveCampaign/services/activecampaign_crm.json` |

### Credential Type Breakdown

| Type | Count | Percentage |
|------|-------|------------|
| `api_key` | 492 | 98% |
| `oauth2` | 12 | 2% |

---

## Gap Analysis

### JSON Fields NOT Captured in Odoo Model

| JSON Field | Present in `ai.service.type`? | Impact |
|------------|-------------------------------|--------|
| `supported_models` | NO | Can't display available models (GPT-4, Claude 3, etc.) |
| `required_scopes` | NO | OAuth providers lose scope requirements |
| `required_credentials` | NO | Multi-credential providers (account_name + api_key) broken |
| `configuration_hints` | NO | Onboarding guidance lost |
| `quota_cost` per operation | Stored in JSON | Not queryable/reportable |

### Missing Infrastructure

| Component | Status | Risk |
|-----------|--------|------|
| JSON Schema Validation | MISSING | Malformed files break populator |
| Config Completeness Flag | MISSING | Can't query "which providers are ready?" |
| Schema Version Tracking | MISSING | Breaking changes hard to manage |

---

## Target Architecture (Option A: Boring Pattern)

### Principle: Extend, Don't Replace

The current structure is 80% correct. We extend it with:

1. **Add missing fields to `ai.service.type` model**
2. **Create JSON schema for validation**
3. **Add config completeness tracking**

### Data Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        EXTERNAL API PROVIDERS                               │
│                                                                             │
│  Every API has different: endpoints, auth methods, rate limits, models     │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                    STANDARDIZATION LAYER (JSON Files)                       │
│                                                                             │
│  vendor_library/                                                            │
│  ├── _schema/                                                               │
│  │   └── service_config.schema.json    ← NEW: JSON Schema validation        │
│  ├── _registry/                                                             │
│  │   └── node_metadata.json            ← Existing: 492 providers            │
│  └── {Vendor}/                                                              │
│      ├── api_config.json               ← Existing: Basic provider info      │
│      └── services/                                                          │
│          └── {service}.json            ← Existing: Detailed service config  │
│                                                                             │
│  STANDARD SCHEMA (enforced):                                                │
│  {                                                                          │
│    "schema_version": "1.0",            ← NEW: Version tracking              │
│    "vendor_key": "string",                                                  │
│    "service_key": "string",                                                 │
│    "auth_method": "api_key|oauth2|...",                                     │
│    "supported_models": ["model1", ...], ← CAPTURED                          │
│    "required_scopes": ["scope1", ...],  ← CAPTURED                          │
│    "required_credentials": [...],       ← CAPTURED                          │
│    "configuration_hints": {...},        ← CAPTURED                          │
│    "operations": [...]                                                      │
│  }                                                                          │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                    PYTHON BRIDGE (service_populator_controller.py)          │
│                                                                             │
│  ENHANCED:                                                                  │
│  1. Validate JSON against schema before processing                          │
│  2. Map ALL JSON fields to Odoo model (including new fields)                │
│  3. Set config_completeness based on populated fields                       │
│  4. Log schema version for migration tracking                               │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                      ODOO MODEL (ai.service.type)                           │
│                                                                             │
│  EXISTING FIELDS:                                                           │
│  ├── name, technical_name, description, icon, sequence, active              │
│  ├── vendor_key, service_key, service_category                              │
│  ├── api_base_url, api_version, auth_required, auth_method                  │
│  ├── operations (JSON), rate_limit_info, docs_url                           │
│  ├── test_endpoint, test_method, is_template                                │
│  └── provider_ids (M2M), provider_count                                     │
│                                                                             │
│  NEW FIELDS:                                                                │
│  ├── schema_version        Char       Track config version                  │
│  ├── supported_models      Json       ["gpt-4", "gpt-3.5-turbo"]            │
│  ├── required_scopes       Json       ["gmail.send", "gmail.readonly"]      │
│  ├── required_credentials  Json       [{key, name, required}]               │
│  ├── configuration_hints   Json       {auth_setup, common_issues}           │
│  └── config_completeness   Selection  none/basic/full                       │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Implementation Plan

### Phase 1: Model Enhancement (ai.service.type)

**File**: `ai_sam_base/models/ai_service_type.py`

**Add Fields**:

```python
# Schema Version Tracking
schema_version = fields.Char(
    string='Schema Version',
    default='1.0',
    help='Version of the service config schema this record follows'
)

# Supported Models (for AI providers)
supported_models = fields.Json(
    string='Supported Models',
    help='List of model identifiers this service supports (e.g., ["gpt-4", "gpt-3.5-turbo"])'
)

# OAuth Scopes (for OAuth providers)
required_scopes = fields.Json(
    string='Required OAuth Scopes',
    help='OAuth scopes required for this service (e.g., ["gmail.send", "gmail.readonly"])'
)

# Multi-Credential Support
required_credentials = fields.Json(
    string='Required Credentials',
    help='Credential fields required beyond API key (e.g., account_name for ActiveCampaign)'
)

# Configuration Hints (onboarding help)
configuration_hints = fields.Json(
    string='Configuration Hints',
    help='Setup instructions and common issues for this service'
)

# Config Completeness Tracking
config_completeness = fields.Selection([
    ('none', 'Not Configured'),
    ('basic', 'Basic (Metadata Only)'),
    ('full', 'Full (Ready for Integration)')
], string='Configuration Completeness', default='none',
   compute='_compute_config_completeness', store=True,
   help='How complete is this service configuration?')
```

**Add Compute Method**:

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

### Phase 2: Update Service Populator

**File**: `ai_sam_base/controllers/service_populator_controller.py`

**Enhance `service_values` dict** to include new fields:

```python
service_values = {
    # ... existing fields ...

    # NEW: Schema version
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

### Phase 3: JSON Schema (Validation)

**File**: `ai_sam/static/src/vendor_library/_schema/service_config.schema.json`

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "service_config.schema.json",
  "title": "SAM AI Service Configuration",
  "description": "Schema for vendor service configuration files",
  "type": "object",
  "required": ["name", "technical_name", "vendor_key", "service_key"],
  "properties": {
    "schema_version": {
      "type": "string",
      "default": "1.0",
      "description": "Schema version for migration tracking"
    },
    "name": {
      "type": "string",
      "description": "Human-readable service name"
    },
    "technical_name": {
      "type": "string",
      "pattern": "^[a-z][a-z0-9_]*$",
      "description": "Code reference (lowercase, underscores)"
    },
    "vendor_key": {
      "type": "string",
      "description": "Vendor identifier (e.g., openai, google)"
    },
    "service_key": {
      "type": "string",
      "description": "Service identifier within vendor (e.g., chat, gmail)"
    },
    "service_category": {
      "type": "string",
      "enum": ["email", "storage", "chat", "crm", "marketing", "analytics", "ai", "productivity", "other"]
    },
    "api_config": {
      "type": "object",
      "required": ["api_base_url", "auth_method"],
      "properties": {
        "api_base_url": { "type": "string", "format": "uri" },
        "api_version": { "type": "string" },
        "auth_required": { "type": "boolean", "default": true },
        "auth_method": {
          "type": "string",
          "enum": ["api_key", "oauth2", "http_basic_auth", "bearer_token", "custom"]
        },
        "docs_url": { "type": "string", "format": "uri" },
        "test_endpoint": { "type": "string" },
        "test_method": { "type": "string", "enum": ["GET", "POST", "HEAD"] }
      }
    },
    "operations": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["key", "name", "endpoint", "method"],
        "properties": {
          "key": { "type": "string" },
          "name": { "type": "string" },
          "description": { "type": "string" },
          "enabled": { "type": "boolean", "default": true },
          "endpoint": { "type": "string" },
          "method": { "type": "string", "enum": ["GET", "POST", "PUT", "PATCH", "DELETE"] },
          "quota_cost": { "type": "integer" }
        }
      }
    },
    "supported_models": {
      "type": "array",
      "items": { "type": "string" },
      "description": "Available models for AI services"
    },
    "required_scopes": {
      "type": "array",
      "items": { "type": "string" },
      "description": "OAuth scopes for OAuth2 providers"
    },
    "required_credentials": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["key", "name", "required"],
        "properties": {
          "key": { "type": "string" },
          "name": { "type": "string" },
          "description": { "type": "string" },
          "required": { "type": "boolean" }
        }
      }
    },
    "rate_limits": {
      "type": "object",
      "properties": {
        "info": { "type": "string" },
        "details": { "type": "string", "format": "uri" }
      }
    },
    "configuration_hints": {
      "type": "object",
      "properties": {
        "auth_setup": { "type": "string" },
        "common_issues": {
          "type": "array",
          "items": { "type": "string" }
        }
      }
    }
  }
}
```

### Phase 4: Update Existing JSON Files

Add `schema_version: "1.0"` to existing service configs for tracking.

---

## Success Criteria

| Metric | Target |
|--------|--------|
| All new fields captured in Odoo | 6 new fields added |
| JSON Schema created | Validates all 7 existing configs |
| Populator handles new fields | No data loss during import |
| Config completeness queryable | Can filter by `full` status |
| Backward compatible | Existing configs work without modification |

---

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Breaking existing imports | Low | High | Schema validation before deploy |
| Field type mismatches | Medium | Medium | JSON fields for flexibility |
| Migration complexity | Low | Low | New fields have defaults |

---

## Files to Modify

| File | Action | Priority |
|------|--------|----------|
| `ai_sam_base/models/ai_service_type.py` | Add 6 new fields | HIGH |
| `ai_sam_base/controllers/service_populator_controller.py` | Map new fields | HIGH |
| `ai_sam/static/src/vendor_library/_schema/service_config.schema.json` | Create new | MEDIUM |
| `ai_sam/static/src/vendor_library/OpenAi/services/*.json` | Add schema_version | LOW |
| `ai_sam/static/src/vendor_library/Google/services/*.json` | Add schema_version | LOW |
| `ai_sam/static/src/vendor_library/ActiveCampaign/services/*.json` | Add schema_version | LOW |

---

## Next Steps

1. **Implement Phase 1**: Add fields to `ai.service.type` model
2. **Implement Phase 2**: Update service populator controller
3. **Implement Phase 3**: Create JSON schema file
4. **Test**: Run module upgrade, verify existing data intact
5. **Validate**: Ensure 7 existing configs import with new fields

---

## Appendix: Current Service Config Examples

### Example 1: OpenAI Chat (API Key Auth)
- **Vendor**: openai
- **Service**: chat
- **Auth**: api_key
- **Models**: gpt-4-turbo, gpt-4, gpt-3.5-turbo
- **Operations**: 3 (chat_completion, function_calling, structured_output)

### Example 2: Gmail (OAuth2 Auth)
- **Vendor**: google
- **Service**: gmail
- **Auth**: oauth2
- **Scopes**: gmail.send, gmail.readonly, gmail.modify
- **Operations**: 8 (send, read, list, search, delete, modify_labels, create_draft, get_attachments)

### Example 3: ActiveCampaign CRM (API Key + Account Name)
- **Vendor**: activecampaign
- **Service**: activecampaign_crm
- **Auth**: api_key
- **Extra Credentials**: account_name (required)
- **Operations**: 12 (CRUD contacts, deals, tags, notes, automations)

---

**Document Status**: Ready for Implementation
**Next Session**: Execute Phase 1-3
**Estimated Effort**: 2-3 hours
