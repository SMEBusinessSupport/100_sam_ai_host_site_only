# FIX PLAN: V2 Context Data Not Reaching System Prompt

**Date:** 2025-12-31
**Priority:** HIGH
**Issue:** SAM doesn't know the user's current URL/location

---

## Problem Summary

When user asks "what URL am I at?", SAM cannot answer because:
1. Frontend sends `context_data` with URL correctly
2. V2 architecture (`sam_chat.py`) builds session with URL in system prompt
3. **BUT** the API call falls back to OLD path that ignores session context

## Root Cause

```
EXPECTED PATH (V2):
Controller → sam_chat.py → ai.service._call_provider_api_streaming()
                                       ↓
                         Uses self.system_prompt (contains URL)

ACTUAL PATH (Broken):
Controller → sam_chat.py → ai.service._call_provider_api_streaming()
                                       ↓
                         AttributeError! (method doesn't exist)
                                       ↓
                         Falls back to _call_api_direct()
                                       ↓
                         APIServices.send() → builds NEW prompt (no URL)
```

## Files Involved

| File | Role | Issue |
|------|------|-------|
| `controllers/sam_ai_chat_controller.py` | Entry point | ✅ Passes context_data correctly |
| `api_communications/sam_chat.py` | V2 chat handler | ✅ Builds session with URL, BUT... |
| `api_communications/sam_chat.py:270-278` | API call | ❌ Calls non-existent method |
| `api_communications/api_services.py` | API wrapper | ❌ Ignores passed system_prompt |
| `api_communications/session_context.py` | Context builder | ✅ Includes URL in prompt |

## Fix Options

### Option A: Add Missing Method to ai.service (Clean but larger change)

Add `_call_provider_api_streaming()` to `ai_brain.py` that accepts:
- `system_prompt` (pre-built)
- `messages`
- `tools`

This completes the V2 architecture properly.

### Option B: Fix APIServices to Accept Pre-built Context (Quick fix)

Modify `APIServices.send()` and `send_streaming()` to accept optional:
- `system_prompt` parameter
- `tools` parameter

When provided, skip internal prompt building.

**Recommended: Option B** (less invasive, faster to implement)

---

## Implementation: Option B

### Step 1: Modify APIServices.send()

**File:** `api_communications/api_services.py`

Find the `send()` method signature and add optional parameters:

```python
def send(self, messages, config=None, system_prompt=None, tools=None):
    """
    Send messages to AI provider.

    Args:
        messages: Conversation messages
        config: Provider config (optional, will get default)
        system_prompt: Pre-built system prompt (optional, skips internal build if provided)
        tools: Pre-built tool list (optional, skips internal load if provided)
    """
    if config is None:
        config = self.get_provider_config()

    # NEW: Use provided system_prompt if available, else build internally
    if system_prompt is None:
        system_prompt = self._build_system_prompt()  # Old behavior

    # NEW: Use provided tools if available
    if tools is None:
        tools = self._get_tools()  # Old behavior

    # ... rest of method uses system_prompt and tools ...
```

### Step 2: Same for send_streaming()

Apply same pattern to `send_streaming()` method.

### Step 3: Update sam_chat.py Fallback

**File:** `api_communications/sam_chat.py`

In `_call_api_direct()` (line 288-302), pass the session's system_prompt:

```python
def _call_api_direct(self, messages, tool_results=None):
    """Direct API call fallback when ai.service method not available."""
    try:
        from .api_services import APIServices
        api = APIServices(self.env)
        config = api.get_provider_config()
        return api.send(
            messages=messages,
            config=config,
            system_prompt=self.system_prompt,  # NEW: Pass session's prompt
            tools=self.tools,                   # NEW: Pass session's tools
        )
    except Exception as e:
        _logger.error(f"[SAM-CHAT] Direct API call failed: {e}")
        return {'content': f"I encountered an error: {str(e)}"}
```

### Step 4: Verify Debug File Shows Context

After fix, `debug_last_prompt.md` should show:
```json
{
  "url": "http://localhost:8069/odoo/apps",
  "model": null,
  ...
}
```

---

## Validation Checklist

- [ ] Go to `/odoo/apps`
- [ ] Ask SAM: "what URL am I at?"
- [ ] SAM should respond with `http://localhost:8069/odoo/apps`
- [ ] Check `debug_last_prompt.md` shows context_data with URL
- [ ] Test on canvas page - context should include `canvas_id`

---

## Files to Modify

1. `api_communications/api_services.py` - Add optional params to send/send_streaming
2. `api_communications/sam_chat.py` - Pass session context in fallback

## Estimated Effort

- **Option B:** 30-60 minutes
- **Testing:** 15 minutes

---

## Notes

- The `startswith` NoneType error was already fixed in `location_insights.py`
- The "Understanding current location" activity was added to controller
- This fix completes the V2 migration for context_data flow
