# SAM AI Chat Data Workflow
**Date:** 2025-12-11
**Version:** 18.0.2.23
**Status:** WORKING

## Overview

This document describes the complete data flow for SAM AI chat functionality, from user message to AI response.

---

## Architecture Diagram

```
USER BROWSER                           ODOO SERVER
============                           ============

[Chat UI]
    |
    | POST /sam_ai/chat/send
    | {message, session_id}
    v
[sam_ai_chat_controller.py]
    |
    | Creates/loads conversation
    v
[ai.service.send_message()]
    |
    +---> [Cost Optimizer] ---------> Selects cheapest provider
    |         |                        based on quality/cost ratio
    |         v
    |     [api.service.provider]
    |         |
    +---> [Memory Search] ----------> Semantic search in ChromaDB
    |         |                        (SentenceTransformers)
    |         v
    |     [ai.vector.service]
    |
    +---> [Token Counting] ----------> Estimates tokens (fallback for non-Anthropic)
    |
    +---> [Budget Check] ------------> Validates within budget limits
    |
    +---> [API Router] --------------> Routes to correct API format
    |         |
    |         +---> _call_openai_api()     (OpenAI format)
    |         +---> _call_claude_api()     (Anthropic format)
    |
    +---> [Response Processing] -----> Normalize, save message, log usage
    |
    v
[JSON Response]
    |
    | {success, message, tokens, cost}
    v
[Chat UI] --------------------------> Display response to user
```

---

## Detailed Flow

### 1. Frontend (JavaScript)

**File:** `ai_sam/static/src/js/sam_chat_v2.js`

```javascript
// User sends message
sendMessage() {
    payload = {message: "test", session_id: null}
    rpc("/sam_ai/chat/send", payload)
}
```

### 2. Controller

**File:** `ai_sam_base/controllers/sam_ai_chat_controller.py`

```python
@http.route('/sam_ai/chat/send', type='json', auth='user')
def send_message(self, message, session_id=None, ...):
    # Get or create conversation
    conversation = self._get_or_create_conversation(session_id)

    # Call AI service
    result = env['ai.service'].send_message(
        conversation_id=conversation.id,
        message=message
    )
    return result
```

### 3. AI Service - Main Entry Point

**File:** `ai_sam_base/models/ai_service.py` - `send_message()`

#### Step 3.1: Get User Profile
```python
profile = self.env['sam.user.profile'].get_or_create_profile()
```

#### Step 3.2: Cost Optimizer (Provider Selection)
```python
CostOptimizer = self.env['ai.cost.optimizer']
recommendation = CostOptimizer.recommend_provider(
    task_type='chat',
    context_size_tokens=estimated_input_tokens,
    quality_required='medium'
)
# Returns: provider_id, model_identifier, estimated_cost
```

#### Step 3.3: Build Provider Config Adapter
```python
class ProviderConfigAdapter:
    # Wraps api.service.provider to match old config interface
    self.api_key = provider.api_key
    self.api_endpoint = provider.api_endpoint
    self.model_name = model_identifier  # From cost optimizer!
    self.api_provider = 'openai'  # Detected from supplier field
```

#### Step 3.4: Memory Search (Semantic)
```python
vector_service = self.env['ai.vector.service']
memory_results = vector_service.search_similar(message, limit=5)
# Uses: SentenceTransformers (all-mpnet-base-v2) + ChromaDB
# WARNING: First call takes 4-5 seconds (model loading from HuggingFace)
```

#### Step 3.5: Build Messages with History
```python
history = conversation.get_history_by_strategy(strategy='token_based')
messages = history + [{'role': 'user', 'content': message}]
```

#### Step 3.6: Token Counting
```python
# For non-Anthropic providers, use fallback estimation
if config.api_provider != 'anthropic':
    return self._count_tokens_fallback(messages, system_prompt)
    # ~4 chars per token estimate
```

#### Step 3.7: Budget Check
```python
budget_check = self.env['ai.cost.budget'].check_budget(estimated_cost)
# Warns or blocks if over budget
```

#### Step 3.8: API Router
```python
api_format = self._get_api_format(config.api_provider)
# Maps 30+ providers to 2 formats: 'anthropic' or 'openai'

if api_format == 'anthropic':
    return self._call_claude_api(config, messages, ...)
elif api_format == 'openai':
    return self._call_openai_api(config, messages, ...)
```

### 4. OpenAI API Call

**File:** `ai_sam_base/models/ai_service.py` - `_call_openai_api()`

```python
headers = {
    'Authorization': f'Bearer {config.api_key}',
    'Content-Type': 'application/json',
}

payload = {
    'model': config.model_name,  # e.g., 'gpt-3.5-turbo'
    'max_tokens': config.max_tokens,
    'temperature': config.temperature,
    'messages': [
        {'role': 'system', 'content': system_prompt},
        {'role': 'user', 'content': 'test'}
    ]
}

response = requests.post(
    'https://api.openai.com/v1/chat/completions',
    headers=headers,
    json=payload
)

# Normalize to Anthropic format for compatibility
return {
    'content': [{'type': 'text', 'text': response['choices'][0]['message']['content']}],
    'usage': {
        'input_tokens': response['usage']['prompt_tokens'],
        'output_tokens': response['usage']['completion_tokens']
    }
}
```

### 5. Response Processing

```python
# Save assistant message
assistant_msg = conversation.add_message('assistant', response_text)

# Log token usage
token_usage = self.env['ai.token.usage'].log_usage(
    provider=config.api_provider,
    model_name=config.model_name,
    input_tokens=input_tokens,
    output_tokens=output_tokens,
    cost_usd=calculated_cost
)

# Update provider statistics
config.increment_usage(tokens_used, cost)

# Return to frontend
return {
    'success': True,
    'message': response_text,
    'input_tokens': input_tokens,
    'output_tokens': output_tokens,
    'cost': cost,
    'conversation_id': conversation_id
}
```

---

## Key Models

| Model | Purpose |
|-------|---------|
| `ai.service` | Main service orchestrator |
| `ai.conversation` | Chat session storage |
| `ai.message` | Individual messages |
| `ai.cost.optimizer` | Provider selection by cost/quality |
| `api.service.provider` | Provider credentials & config |
| `ai.provider.model` | Available models per provider |
| `ai.token.usage` | Usage logging |
| `ai.vector.service` | Semantic memory search |
| `sam.user.profile` | Multi-user context |

---

## API Format Mapping

The system supports 30+ providers with only 2 API format handlers:

```python
API_FORMAT_MAP = {
    # Anthropic format
    'anthropic': 'anthropic',
    'claude': 'anthropic',

    # OpenAI-compatible format (most providers)
    'openai': 'openai',
    'azure_openai': 'openai',
    'groq': 'openai',
    'together': 'openai',
    'mistral': 'openai',
    'deepseek': 'openai',
    'ollama': 'openai',
    'openrouter': 'openai',
    # ... 20+ more
}
```

---

## Performance Bottlenecks Identified

| Issue | Time | Solution |
|-------|------|----------|
| SentenceTransformer loading | 4-5s first call | Cache model in memory |
| HuggingFace HEAD requests | 3-4s | Use local cache / disable online check |
| ChromaDB init | ~0.5s | Keep client alive |
| Provider benchmark logging | HUNG | Disabled (needs investigation) |

---

## Fixes Applied (Session 2025-12-11)

| Version | Fix |
|---------|-----|
| 18.0.2.14 | Fixed invalid `quality_required='intermediate'` parameter |
| 18.0.2.15 | Replaced emojis with ASCII markers for Windows |
| 18.0.2.16 | Added 12 missing ACL entries |
| 18.0.2.17 | Added debug logging for hang tracing |
| 18.0.2.18 | Fixed token counting hang (skip Anthropic SDK for OpenAI) |
| 18.0.2.19 | Added `_call_openai_api()` method |
| 18.0.2.20 | Added API format routing (30+ providers) |
| 18.0.2.21 | Fixed `model_name` being False (use `model_identifier` from cost optimizer) |
| 18.0.2.22 | Added detailed debug logging |
| 18.0.2.23 | Disabled provider benchmark logging (was hanging) |
| 18.0.2.24 | User-level provider config caching (skips cost optimizer on subsequent calls) |

---

## Provider Config Caching (18.0.2.24)

### Architecture

```
FIRST CHAT REQUEST                      SUBSEQUENT REQUESTS
==================                      ===================

[ai.service.send_message()]             [ai.service.send_message()]
        |                                       |
        v                                       v
[Check sam.user.settings cache] -----> [CACHE HIT!]
        |                                       |
        | (cache miss)                          | (use cached config)
        v                                       v
[CostOptimizer.recommend_provider()]    [ProviderConfigAdapter]
        |                                       |
        v                                       |
[Cache provider config] <----------------------|
        |
        v
[ProviderConfigAdapter]
```

### Cache Fields (sam.user.settings)

| Field | Type | Purpose |
|-------|------|---------|
| `cached_provider_config` | Text (JSON) | Provider ID, model name, API type |
| `cache_generated_at` | Datetime | When cache was created |
| `cache_version` | Char | Module version (invalidate on upgrade) |

### Cache Invalidation Triggers

1. **Module Upgrade** - `cache_version` mismatch invalidates cache
2. **Provider Settings Change** - `api.service.provider.write()` invalidates all user caches when:
   - `api_key` changes
   - `api_endpoint` changes
   - `model_name` changes
   - `supplier` changes
   - `is_default` changes
   - `active` changes
   - `max_tokens` changes
   - `temperature` changes

### Expected Performance Improvement

| Scenario | Before | After |
|----------|--------|-------|
| First request | ~2-3s (cost optimizer) | ~2-3s (same) |
| Subsequent requests | ~2-3s (cost optimizer) | ~0.5s (cache hit) |

---

## Next Steps

1. **Cache SentenceTransformer Model**
   - Currently loads on first memory search (4-5s)
   - Cache in memory after first load

2. **Re-enable Provider Benchmarking**
   - Investigate why `api.service.provider.search()` hangs
   - Likely missing index or field mismatch

3. **Data-Driven API Formats**
   - Move API format configs to database/JSON
   - Allow UI-based provider configuration
