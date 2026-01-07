# Provider Adapter Architecture Blueprint

**Version:** 1.0.0
**Date:** December 2025
**Author:** CTO Advisory Session
**Status:** BLUEPRINT (Not Implemented)

---

## Executive Summary

This document defines the Provider Adapter architecture for SAM AI. The goal is to create a clean abstraction layer that allows switching between AI providers (Claude, OpenAI, Google, etc.) without code changes - only configuration.

**Key Insight:** Only 3 adapters needed to support 100+ providers:
- `AnthropicAdapter` - Claude (~5% of market)
- `OpenAIAdapter` - GPT, Groq, Mistral, Ollama, +90 more (~90% of market)
- `GoogleAdapter` - Gemini (~5% of market)

---

## File Structure

```
ai_sam_base/
├── adapters/
│   ├── __init__.py              # Registry and factory function
│   ├── base_adapter.py          # Abstract base class
│   ├── openai_adapter.py        # OpenAI-compatible (90% of providers)
│   ├── anthropic_adapter.py     # Anthropic/Claude
│   └── google_adapter.py        # Google/Gemini (future)
├── models/
│   └── api_service_provider.py  # Add get_adapter() method
└── schemas/
    └── universal_tool_schema.py # Universal tool definitions
```

---

## 1. Universal Tool Schema

Define tools ONCE in a universal format. Adapters convert automatically.

```python
# schemas/universal_tool_schema.py
"""
Universal Tool Schema - Provider-Agnostic Tool Definitions

Tools are defined in a universal JSON Schema format.
Each adapter converts to provider-specific format automatically.

Universal Format (based on JSON Schema, similar to OpenAI's):
{
    "name": "tool_name",
    "description": "What the tool does",
    "parameters": {
        "type": "object",
        "properties": {
            "param1": {"type": "string", "description": "..."},
            "param2": {"type": "integer", "description": "..."}
        },
        "required": ["param1"]
    }
}

Adapters convert to:
- Anthropic: input_schema instead of parameters
- OpenAI: Wraps in {"type": "function", "function": {...}}
- Google: Uses functionDeclarations format
"""

# Universal tool definitions for SAM AI
UNIVERSAL_TOOLS = [
    {
        "name": "read_file",
        "description": "Read the contents of a file from the filesystem. Use this when you need to access actual file contents.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Full absolute path to the file (e.g., C:\\Users\\total\\.claude\\agents\\cmo\\system_prompt.md)"
                },
                "reason": {
                    "type": "string",
                    "description": "Why you need to read this file (shown to user in permission request)"
                }
            },
            "required": ["path", "reason"]
        }
    },
    {
        "name": "list_directory",
        "description": "List files and folders in a directory. Use this to explore folder contents before reading specific files.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Full absolute path to the directory to list"
                },
                "pattern": {
                    "type": "string",
                    "description": "Optional glob pattern to filter results (e.g., '*.md', '*.json')"
                }
            },
            "required": ["path"]
        }
    },
    {
        "name": "glob_files",
        "description": "Find files matching a glob pattern. Use this to search for files by name/extension across directories.",
        "parameters": {
            "type": "object",
            "properties": {
                "pattern": {
                    "type": "string",
                    "description": "Glob pattern (e.g., '*.js', '**/*.py', 'test_*.py')"
                },
                "path": {
                    "type": "string",
                    "description": "Starting directory (searches recursively from here)"
                }
            },
            "required": ["pattern", "path"]
        }
    },
    {
        "name": "write_file",
        "description": "Write content to a file. Creates new file or overwrites existing file.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Full absolute path where to write the file"
                },
                "content": {
                    "type": "string",
                    "description": "Content to write to the file"
                },
                "reason": {
                    "type": "string",
                    "description": "Why you need to write this file (shown to user in permission request)"
                }
            },
            "required": ["path", "content", "reason"]
        }
    }
]


def get_universal_tools():
    """Return the universal tool definitions."""
    return UNIVERSAL_TOOLS.copy()
```

---

## 2. Base Adapter (Abstract Class)

```python
# adapters/base_adapter.py
"""
Base Adapter - Abstract Interface for AI Provider Adapters

All provider adapters must implement this interface.
This ensures consistent behavior across Claude, OpenAI, Google, etc.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Generator, Optional
import logging

_logger = logging.getLogger(__name__)


class BaseAdapter(ABC):
    """
    Abstract base class for AI provider adapters.

    Each adapter handles:
    1. Tool format conversion (universal -> provider-specific)
    2. Message format conversion (internal -> provider-specific)
    3. API calls (HTTP requests to provider)
    4. Response parsing (provider-specific -> internal)
    5. Tool call extraction and result formatting
    6. Streaming support

    Implementing a new adapter:
    1. Inherit from BaseAdapter
    2. Implement all abstract methods
    3. Register in adapters/__init__.py
    """

    # Override in subclass
    FORMAT_NAME = "base"  # e.g., "openai", "anthropic", "google"

    # =========================================================================
    # TOOL FORMATTING
    # =========================================================================

    @abstractmethod
    def format_tools(self, universal_tools: List[Dict]) -> List[Dict]:
        """
        Convert universal tool definitions to provider-specific format.

        Args:
            universal_tools: List of tools in universal format
                [{
                    "name": "read_file",
                    "description": "...",
                    "parameters": {"type": "object", "properties": {...}}
                }]

        Returns:
            List of tools in provider-specific format

        Example (OpenAI):
            [{"type": "function", "function": {"name": "...", "parameters": {...}}}]

        Example (Anthropic):
            [{"name": "...", "description": "...", "input_schema": {...}}]
        """
        pass

    # =========================================================================
    # MESSAGE FORMATTING
    # =========================================================================

    @abstractmethod
    def format_messages(self, messages: List[Dict], system_prompt: Optional[str] = None) -> Dict:
        """
        Convert internal message format to provider-specific API payload.

        Args:
            messages: List of messages in internal format
                [{"role": "user", "content": "Hello"}, ...]
            system_prompt: Optional system prompt (handled differently per provider)

        Returns:
            Dict ready for API call (may include system prompt, messages, etc.)

        Note: Different providers handle system prompts differently:
            - Anthropic: Separate 'system' parameter
            - OpenAI: System message in messages array
            - Google: System instruction parameter
        """
        pass

    @abstractmethod
    def format_tool_results(self, tool_results: List[Dict], tool_calls: List[Dict]) -> List[Dict]:
        """
        Format tool execution results for the next API call.

        Args:
            tool_results: List of tool execution results
                [{"tool_id": "...", "tool_name": "read_file", "result": "file contents..."}]
            tool_calls: Original tool calls from AI response

        Returns:
            Messages to append to conversation for next API call

        Note: Format differs significantly:
            - Anthropic: user message with tool_result content blocks
            - OpenAI: separate messages with role="tool"
        """
        pass

    # =========================================================================
    # API CALLS
    # =========================================================================

    @abstractmethod
    def call_api(
        self,
        provider: Any,  # api.service.provider record
        messages: List[Dict],
        tools: Optional[List[Dict]] = None,
        system_prompt: Optional[str] = None,
        max_tokens: int = 4096,
        temperature: float = 1.0,
        **kwargs
    ) -> Dict:
        """
        Make synchronous API call to provider.

        Args:
            provider: api.service.provider Odoo record with credentials
            messages: Conversation messages (internal format)
            tools: Tool definitions (universal format, will be converted)
            system_prompt: System prompt
            max_tokens: Maximum tokens in response
            temperature: Sampling temperature
            **kwargs: Provider-specific options

        Returns:
            Normalized response dict:
            {
                "content": "Response text",
                "tool_calls": [  # Optional, if AI requested tools
                    {
                        "id": "call_123",
                        "name": "read_file",
                        "input": {"path": "/some/file", "reason": "..."}
                    }
                ],
                "usage": {
                    "input_tokens": 100,
                    "output_tokens": 50
                },
                "stop_reason": "end_turn" | "tool_use" | "max_tokens",
                "model": "claude-3-5-sonnet-20241022"
            }
        """
        pass

    @abstractmethod
    def call_api_streaming(
        self,
        provider: Any,
        messages: List[Dict],
        tools: Optional[List[Dict]] = None,
        system_prompt: Optional[str] = None,
        max_tokens: int = 4096,
        temperature: float = 1.0,
        **kwargs
    ) -> Generator[Dict, None, None]:
        """
        Make streaming API call to provider.

        Args:
            Same as call_api()

        Yields:
            Event dicts:
            - {"type": "chunk", "data": {"text": "partial response"}}
            - {"type": "tool_use", "data": {"id": "...", "name": "...", "input": {...}}}
            - {"type": "usage", "data": {"input_tokens": 100, "output_tokens": 50}}
            - {"type": "done", "data": {"stop_reason": "end_turn"}}
            - {"type": "error", "data": {"message": "error details"}}
        """
        pass

    # =========================================================================
    # RESPONSE PARSING
    # =========================================================================

    @abstractmethod
    def parse_response(self, raw_response: Dict) -> Dict:
        """
        Parse raw API response into normalized internal format.

        Args:
            raw_response: Raw response from provider API

        Returns:
            Normalized response (same format as call_api return value)
        """
        pass

    @abstractmethod
    def extract_tool_calls(self, response: Dict) -> List[Dict]:
        """
        Extract tool calls from API response.

        Args:
            response: Normalized response dict

        Returns:
            List of tool calls:
            [{"id": "...", "name": "tool_name", "input": {...}}]
        """
        pass

    # =========================================================================
    # UTILITY METHODS (with default implementations)
    # =========================================================================

    def get_auth_headers(self, provider: Any) -> Dict[str, str]:
        """
        Get authentication headers for API request.

        Override if provider uses non-standard auth.

        Args:
            provider: api.service.provider record

        Returns:
            Headers dict
        """
        # Default implementation - override in subclass
        return {}

    def get_api_endpoint(self, provider: Any) -> str:
        """
        Get API endpoint URL.

        Args:
            provider: api.service.provider record

        Returns:
            API endpoint URL
        """
        return provider.api_endpoint

    def should_retry(self, error: Exception, attempt: int) -> bool:
        """
        Determine if request should be retried.

        Args:
            error: The exception that occurred
            attempt: Current attempt number (1-based)

        Returns:
            True if should retry, False otherwise
        """
        # Default: retry up to 3 times on connection errors
        if attempt >= 3:
            return False

        error_str = str(error).lower()
        retryable = ['timeout', 'connection', '429', '503', '502', 'overloaded']
        return any(r in error_str for r in retryable)

    def calculate_retry_delay(self, attempt: int) -> float:
        """
        Calculate delay before retry (exponential backoff).

        Args:
            attempt: Current attempt number (1-based)

        Returns:
            Delay in seconds
        """
        import random
        base_delay = 1.0
        max_delay = 60.0
        delay = min(base_delay * (2 ** (attempt - 1)), max_delay)
        jitter = delay * random.random() * 0.25
        return delay + jitter
```

---

## 3. OpenAI Adapter (Covers 90% of Providers)

```python
# adapters/openai_adapter.py
"""
OpenAI Adapter - Handles OpenAI and OpenAI-Compatible APIs

This adapter covers ~90% of AI providers because most have adopted
OpenAI's API format as a de facto standard.

Supported providers (partial list):
- OpenAI (GPT-4, GPT-4o, o1)
- Groq (Llama, Mixtral)
- Together AI
- Mistral AI
- Perplexity
- DeepSeek
- Fireworks AI
- Ollama (local)
- LM Studio (local)
- vLLM (self-hosted)
- Azure OpenAI
- OpenRouter
- +80 more providers
"""

import json
import logging
import requests
from typing import List, Dict, Any, Generator, Optional

from .base_adapter import BaseAdapter

_logger = logging.getLogger(__name__)


class OpenAIAdapter(BaseAdapter):
    """
    Adapter for OpenAI and OpenAI-compatible APIs.

    API Reference: https://platform.openai.com/docs/api-reference/chat
    """

    FORMAT_NAME = "openai"

    # Default endpoint (can be overridden per provider)
    DEFAULT_ENDPOINT = "https://api.openai.com/v1/chat/completions"

    # =========================================================================
    # TOOL FORMATTING
    # =========================================================================

    def format_tools(self, universal_tools: List[Dict]) -> List[Dict]:
        """
        Convert universal tools to OpenAI function calling format.

        Universal format:
            {"name": "...", "description": "...", "parameters": {...}}

        OpenAI format:
            {"type": "function", "function": {"name": "...", "description": "...", "parameters": {...}}}
        """
        if not universal_tools:
            return []

        openai_tools = []
        for tool in universal_tools:
            openai_tools.append({
                "type": "function",
                "function": {
                    "name": tool["name"],
                    "description": tool.get("description", ""),
                    "parameters": tool.get("parameters", {"type": "object", "properties": {}})
                }
            })

        return openai_tools

    # =========================================================================
    # MESSAGE FORMATTING
    # =========================================================================

    def format_messages(self, messages: List[Dict], system_prompt: Optional[str] = None) -> Dict:
        """
        Format messages for OpenAI API.

        OpenAI includes system prompt as first message in array.
        """
        formatted_messages = []

        # System prompt goes first as a message
        if system_prompt:
            formatted_messages.append({
                "role": "system",
                "content": system_prompt
            })

        # Add conversation messages
        for msg in messages:
            formatted_messages.append({
                "role": msg.get("role", "user"),
                "content": msg.get("content", "")
            })

        return {"messages": formatted_messages}

    def format_tool_results(self, tool_results: List[Dict], tool_calls: List[Dict]) -> List[Dict]:
        """
        Format tool results for OpenAI.

        OpenAI format: Each tool result is a separate message with role="tool"
        """
        messages = []

        # First, add assistant message with the tool calls
        messages.append({
            "role": "assistant",
            "content": None,
            "tool_calls": [
                {
                    "id": tc["id"],
                    "type": "function",
                    "function": {
                        "name": tc["name"],
                        "arguments": json.dumps(tc.get("input", {}))
                    }
                }
                for tc in tool_calls
            ]
        })

        # Then add tool result messages
        for result in tool_results:
            messages.append({
                "role": "tool",
                "tool_call_id": result["tool_id"],
                "content": result.get("result", "")
            })

        return messages

    # =========================================================================
    # API CALLS
    # =========================================================================

    def get_auth_headers(self, provider: Any) -> Dict[str, str]:
        """OpenAI uses Bearer token authentication."""
        return {
            "Authorization": f"Bearer {provider.api_key}",
            "Content-Type": "application/json"
        }

    def call_api(
        self,
        provider: Any,
        messages: List[Dict],
        tools: Optional[List[Dict]] = None,
        system_prompt: Optional[str] = None,
        max_tokens: int = 4096,
        temperature: float = 1.0,
        **kwargs
    ) -> Dict:
        """
        Make synchronous API call to OpenAI-compatible endpoint.
        """
        endpoint = self.get_api_endpoint(provider) or self.DEFAULT_ENDPOINT
        headers = self.get_auth_headers(provider)

        # Format messages (includes system prompt)
        payload = self.format_messages(messages, system_prompt)

        # Add model and parameters
        payload["model"] = provider.model_name or "gpt-4"
        payload["max_tokens"] = max_tokens
        payload["temperature"] = temperature

        # Add tools if provided
        if tools:
            payload["tools"] = self.format_tools(tools)
            payload["tool_choice"] = "auto"

        _logger.info(f"[OpenAIAdapter] Calling {endpoint} with model {payload['model']}")

        # Make request with retry logic
        attempt = 0
        last_error = None

        while attempt < 3:
            attempt += 1
            try:
                response = requests.post(
                    endpoint,
                    headers=headers,
                    json=payload,
                    timeout=120
                )

                if response.status_code == 200:
                    return self.parse_response(response.json())

                # Handle rate limiting
                if response.status_code == 429:
                    if self.should_retry(Exception("429"), attempt):
                        import time
                        delay = self.calculate_retry_delay(attempt)
                        _logger.warning(f"[OpenAIAdapter] Rate limited, retrying in {delay:.1f}s")
                        time.sleep(delay)
                        continue

                # Non-retryable error
                error_msg = response.text
                _logger.error(f"[OpenAIAdapter] API error {response.status_code}: {error_msg}")
                raise Exception(f"OpenAI API error {response.status_code}: {error_msg}")

            except requests.exceptions.Timeout as e:
                last_error = e
                if self.should_retry(e, attempt):
                    import time
                    delay = self.calculate_retry_delay(attempt)
                    _logger.warning(f"[OpenAIAdapter] Timeout, retrying in {delay:.1f}s")
                    time.sleep(delay)
                    continue
                raise

            except requests.exceptions.ConnectionError as e:
                last_error = e
                if self.should_retry(e, attempt):
                    import time
                    delay = self.calculate_retry_delay(attempt)
                    _logger.warning(f"[OpenAIAdapter] Connection error, retrying in {delay:.1f}s")
                    time.sleep(delay)
                    continue
                raise

        raise last_error or Exception("Max retries exceeded")

    def call_api_streaming(
        self,
        provider: Any,
        messages: List[Dict],
        tools: Optional[List[Dict]] = None,
        system_prompt: Optional[str] = None,
        max_tokens: int = 4096,
        temperature: float = 1.0,
        **kwargs
    ) -> Generator[Dict, None, None]:
        """
        Make streaming API call to OpenAI-compatible endpoint.
        """
        endpoint = self.get_api_endpoint(provider) or self.DEFAULT_ENDPOINT
        headers = self.get_auth_headers(provider)

        payload = self.format_messages(messages, system_prompt)
        payload["model"] = provider.model_name or "gpt-4"
        payload["max_tokens"] = max_tokens
        payload["temperature"] = temperature
        payload["stream"] = True

        if tools:
            payload["tools"] = self.format_tools(tools)
            payload["tool_choice"] = "auto"

        _logger.info(f"[OpenAIAdapter] Streaming from {endpoint}")

        try:
            response = requests.post(
                endpoint,
                headers=headers,
                json=payload,
                stream=True,
                timeout=120
            )

            if response.status_code != 200:
                yield {"type": "error", "data": {"message": f"API error {response.status_code}"}}
                return

            # Track tool calls being assembled (OpenAI streams them in pieces)
            pending_tool_calls = {}  # index -> {id, name, arguments}
            accumulated_text = ""
            finish_reason = None
            input_tokens = 0
            output_tokens = 0

            for line in response.iter_lines():
                if not line:
                    continue

                line = line.decode('utf-8')
                if not line.startswith('data: '):
                    continue

                data = line[6:]  # Remove 'data: ' prefix
                if data == '[DONE]':
                    break

                try:
                    chunk = json.loads(data)

                    # Extract usage if present
                    if 'usage' in chunk:
                        input_tokens = chunk['usage'].get('prompt_tokens', 0)
                        output_tokens = chunk['usage'].get('completion_tokens', 0)

                    choices = chunk.get('choices', [])
                    if not choices:
                        continue

                    choice = choices[0]
                    delta = choice.get('delta', {})
                    finish_reason = choice.get('finish_reason')

                    # Text content
                    if 'content' in delta and delta['content']:
                        accumulated_text += delta['content']
                        yield {"type": "chunk", "data": {"text": delta['content']}}

                    # Tool calls (streamed in pieces)
                    if 'tool_calls' in delta:
                        for tc in delta['tool_calls']:
                            idx = tc.get('index', 0)
                            if idx not in pending_tool_calls:
                                pending_tool_calls[idx] = {'id': '', 'name': '', 'arguments': ''}

                            if 'id' in tc:
                                pending_tool_calls[idx]['id'] = tc['id']
                            if 'function' in tc:
                                if 'name' in tc['function']:
                                    pending_tool_calls[idx]['name'] = tc['function']['name']
                                if 'arguments' in tc['function']:
                                    pending_tool_calls[idx]['arguments'] += tc['function']['arguments']

                except json.JSONDecodeError:
                    continue

            # Emit completed tool calls
            if pending_tool_calls and finish_reason == 'tool_calls':
                for idx, tc_data in pending_tool_calls.items():
                    try:
                        input_args = json.loads(tc_data['arguments']) if tc_data['arguments'] else {}
                    except json.JSONDecodeError:
                        input_args = {}

                    yield {
                        "type": "tool_use",
                        "data": {
                            "id": tc_data['id'],
                            "name": tc_data['name'],
                            "input": input_args
                        }
                    }

            # Final usage
            yield {
                "type": "usage",
                "data": {
                    "input_tokens": input_tokens,
                    "output_tokens": output_tokens
                }
            }

            # Done
            yield {
                "type": "done",
                "data": {
                    "stop_reason": finish_reason or "end_turn",
                    "content": accumulated_text
                }
            }

        except Exception as e:
            _logger.error(f"[OpenAIAdapter] Streaming error: {e}")
            yield {"type": "error", "data": {"message": str(e)}}

    # =========================================================================
    # RESPONSE PARSING
    # =========================================================================

    def parse_response(self, raw_response: Dict) -> Dict:
        """
        Parse OpenAI API response to normalized format.
        """
        choices = raw_response.get('choices', [])
        if not choices:
            return {
                "content": "",
                "tool_calls": [],
                "usage": {"input_tokens": 0, "output_tokens": 0},
                "stop_reason": "error",
                "model": raw_response.get('model', '')
            }

        choice = choices[0]
        message = choice.get('message', {})

        # Extract content
        content = message.get('content', '') or ''

        # Extract tool calls
        tool_calls = []
        if 'tool_calls' in message:
            for tc in message['tool_calls']:
                func = tc.get('function', {})
                try:
                    input_args = json.loads(func.get('arguments', '{}'))
                except json.JSONDecodeError:
                    input_args = {}

                tool_calls.append({
                    "id": tc.get('id', ''),
                    "name": func.get('name', ''),
                    "input": input_args
                })

        # Extract usage
        usage = raw_response.get('usage', {})

        # Map finish reason
        finish_reason = choice.get('finish_reason', 'stop')
        stop_reason_map = {
            'stop': 'end_turn',
            'tool_calls': 'tool_use',
            'length': 'max_tokens',
            'content_filter': 'content_filter'
        }

        return {
            "content": content,
            "tool_calls": tool_calls,
            "usage": {
                "input_tokens": usage.get('prompt_tokens', 0),
                "output_tokens": usage.get('completion_tokens', 0)
            },
            "stop_reason": stop_reason_map.get(finish_reason, finish_reason),
            "model": raw_response.get('model', '')
        }

    def extract_tool_calls(self, response: Dict) -> List[Dict]:
        """Extract tool calls from normalized response."""
        return response.get('tool_calls', [])
```

---

## 4. Anthropic Adapter

```python
# adapters/anthropic_adapter.py
"""
Anthropic Adapter - Handles Claude API

Anthropic has a unique API format, distinct from OpenAI.
Key differences:
- System prompt is separate parameter (not in messages)
- Tools use 'input_schema' instead of 'parameters'
- Tool results use content blocks, not separate messages
- Supports prompt caching for cost reduction
"""

import json
import logging
import requests
from typing import List, Dict, Any, Generator, Optional

from .base_adapter import BaseAdapter

_logger = logging.getLogger(__name__)


class AnthropicAdapter(BaseAdapter):
    """
    Adapter for Anthropic Claude API.

    API Reference: https://docs.anthropic.com/en/api/messages
    """

    FORMAT_NAME = "anthropic"

    DEFAULT_ENDPOINT = "https://api.anthropic.com/v1/messages"
    API_VERSION = "2023-06-01"

    # =========================================================================
    # TOOL FORMATTING
    # =========================================================================

    def format_tools(self, universal_tools: List[Dict]) -> List[Dict]:
        """
        Convert universal tools to Anthropic format.

        Universal format:
            {"name": "...", "description": "...", "parameters": {...}}

        Anthropic format:
            {"name": "...", "description": "...", "input_schema": {...}}
        """
        if not universal_tools:
            return []

        anthropic_tools = []
        for tool in universal_tools:
            anthropic_tools.append({
                "name": tool["name"],
                "description": tool.get("description", ""),
                "input_schema": tool.get("parameters", {"type": "object", "properties": {}})
            })

        return anthropic_tools

    # =========================================================================
    # MESSAGE FORMATTING
    # =========================================================================

    def format_messages(self, messages: List[Dict], system_prompt: Optional[str] = None) -> Dict:
        """
        Format messages for Anthropic API.

        Anthropic keeps system prompt separate from messages.
        Also supports prompt caching via cache_control.
        """
        formatted_messages = []

        for msg in messages:
            content = msg.get("content", "")

            # Handle content that's already a list (e.g., with tool results)
            if isinstance(content, list):
                formatted_messages.append({
                    "role": msg.get("role", "user"),
                    "content": content
                })
            else:
                formatted_messages.append({
                    "role": msg.get("role", "user"),
                    "content": content
                })

        result = {"messages": formatted_messages}

        # System prompt is separate in Anthropic
        if system_prompt:
            # Enable prompt caching for system prompt (90% cost reduction on cache hits)
            result["system"] = [
                {
                    "type": "text",
                    "text": system_prompt,
                    "cache_control": {"type": "ephemeral"}
                }
            ]

        return result

    def format_tool_results(self, tool_results: List[Dict], tool_calls: List[Dict]) -> List[Dict]:
        """
        Format tool results for Anthropic.

        Anthropic format:
        1. Assistant message with tool_use content blocks
        2. User message with tool_result content blocks
        """
        messages = []

        # Assistant message with tool_use blocks
        assistant_content = []
        for tc in tool_calls:
            assistant_content.append({
                "type": "tool_use",
                "id": tc["id"],
                "name": tc["name"],
                "input": tc.get("input", {})
            })

        messages.append({
            "role": "assistant",
            "content": assistant_content
        })

        # User message with tool_result blocks
        user_content = []
        for result in tool_results:
            user_content.append({
                "type": "tool_result",
                "tool_use_id": result["tool_id"],
                "content": result.get("result", "")
            })

        messages.append({
            "role": "user",
            "content": user_content
        })

        return messages

    # =========================================================================
    # API CALLS
    # =========================================================================

    def get_auth_headers(self, provider: Any) -> Dict[str, str]:
        """Anthropic uses x-api-key header."""
        return {
            "x-api-key": provider.api_key,
            "anthropic-version": self.API_VERSION,
            "anthropic-beta": "prompt-caching-2024-07-31",  # Enable prompt caching
            "Content-Type": "application/json"
        }

    def call_api(
        self,
        provider: Any,
        messages: List[Dict],
        tools: Optional[List[Dict]] = None,
        system_prompt: Optional[str] = None,
        max_tokens: int = 4096,
        temperature: float = 1.0,
        **kwargs
    ) -> Dict:
        """
        Make synchronous API call to Anthropic.
        """
        endpoint = self.get_api_endpoint(provider) or self.DEFAULT_ENDPOINT
        headers = self.get_auth_headers(provider)

        # Format messages and system prompt
        payload = self.format_messages(messages, system_prompt)

        # Add model and parameters
        payload["model"] = provider.model_name or "claude-3-5-sonnet-20241022"
        payload["max_tokens"] = max_tokens
        payload["temperature"] = temperature

        # Add tools if provided
        if tools:
            payload["tools"] = self.format_tools(tools)

        _logger.info(f"[AnthropicAdapter] Calling {endpoint} with model {payload['model']}")

        # Make request with retry logic
        attempt = 0
        last_error = None

        while attempt < 3:
            attempt += 1
            try:
                response = requests.post(
                    endpoint,
                    headers=headers,
                    json=payload,
                    timeout=120
                )

                if response.status_code == 200:
                    return self.parse_response(response.json())

                # Handle rate limiting and overloaded
                if response.status_code in [429, 529]:
                    if self.should_retry(Exception(str(response.status_code)), attempt):
                        import time
                        delay = self.calculate_retry_delay(attempt)
                        _logger.warning(f"[AnthropicAdapter] Rate limited/overloaded, retrying in {delay:.1f}s")
                        time.sleep(delay)
                        continue

                error_msg = response.text
                _logger.error(f"[AnthropicAdapter] API error {response.status_code}: {error_msg}")
                raise Exception(f"Anthropic API error {response.status_code}: {error_msg}")

            except requests.exceptions.Timeout as e:
                last_error = e
                if self.should_retry(e, attempt):
                    import time
                    delay = self.calculate_retry_delay(attempt)
                    _logger.warning(f"[AnthropicAdapter] Timeout, retrying in {delay:.1f}s")
                    time.sleep(delay)
                    continue
                raise

            except requests.exceptions.ConnectionError as e:
                last_error = e
                if self.should_retry(e, attempt):
                    import time
                    delay = self.calculate_retry_delay(attempt)
                    _logger.warning(f"[AnthropicAdapter] Connection error, retrying in {delay:.1f}s")
                    time.sleep(delay)
                    continue
                raise

        raise last_error or Exception("Max retries exceeded")

    def call_api_streaming(
        self,
        provider: Any,
        messages: List[Dict],
        tools: Optional[List[Dict]] = None,
        system_prompt: Optional[str] = None,
        max_tokens: int = 4096,
        temperature: float = 1.0,
        **kwargs
    ) -> Generator[Dict, None, None]:
        """
        Make streaming API call to Anthropic.

        Uses Anthropic's SSE streaming format.
        """
        endpoint = self.get_api_endpoint(provider) or self.DEFAULT_ENDPOINT
        headers = self.get_auth_headers(provider)

        payload = self.format_messages(messages, system_prompt)
        payload["model"] = provider.model_name or "claude-3-5-sonnet-20241022"
        payload["max_tokens"] = max_tokens
        payload["temperature"] = temperature
        payload["stream"] = True

        if tools:
            payload["tools"] = self.format_tools(tools)

        _logger.info(f"[AnthropicAdapter] Streaming from {endpoint}")

        try:
            response = requests.post(
                endpoint,
                headers=headers,
                json=payload,
                stream=True,
                timeout=120
            )

            if response.status_code != 200:
                yield {"type": "error", "data": {"message": f"API error {response.status_code}"}}
                return

            accumulated_text = ""
            current_tool_use = None
            tool_input_json = ""
            input_tokens = 0
            output_tokens = 0
            stop_reason = None

            for line in response.iter_lines():
                if not line:
                    continue

                line = line.decode('utf-8')
                if not line.startswith('data: '):
                    continue

                data = line[6:]
                try:
                    event = json.loads(data)
                    event_type = event.get('type', '')

                    if event_type == 'message_start':
                        # Extract input tokens from usage
                        usage = event.get('message', {}).get('usage', {})
                        input_tokens = usage.get('input_tokens', 0)

                    elif event_type == 'content_block_start':
                        block = event.get('content_block', {})
                        if block.get('type') == 'tool_use':
                            current_tool_use = {
                                'id': block.get('id', ''),
                                'name': block.get('name', ''),
                                'input': {}
                            }
                            tool_input_json = ""

                    elif event_type == 'content_block_delta':
                        delta = event.get('delta', {})
                        delta_type = delta.get('type', '')

                        if delta_type == 'text_delta':
                            text = delta.get('text', '')
                            accumulated_text += text
                            yield {"type": "chunk", "data": {"text": text}}

                        elif delta_type == 'input_json_delta':
                            # Tool input comes in pieces
                            tool_input_json += delta.get('partial_json', '')

                    elif event_type == 'content_block_stop':
                        if current_tool_use:
                            # Parse accumulated tool input
                            try:
                                current_tool_use['input'] = json.loads(tool_input_json) if tool_input_json else {}
                            except json.JSONDecodeError:
                                current_tool_use['input'] = {}

                            yield {"type": "tool_use", "data": current_tool_use}
                            current_tool_use = None
                            tool_input_json = ""

                    elif event_type == 'message_delta':
                        delta = event.get('delta', {})
                        stop_reason = delta.get('stop_reason')
                        usage = event.get('usage', {})
                        output_tokens = usage.get('output_tokens', 0)

                    elif event_type == 'message_stop':
                        pass  # End of stream

                except json.JSONDecodeError:
                    continue

            # Final usage
            yield {
                "type": "usage",
                "data": {
                    "input_tokens": input_tokens,
                    "output_tokens": output_tokens
                }
            }

            # Done
            yield {
                "type": "done",
                "data": {
                    "stop_reason": stop_reason or "end_turn",
                    "content": accumulated_text
                }
            }

        except Exception as e:
            _logger.error(f"[AnthropicAdapter] Streaming error: {e}")
            yield {"type": "error", "data": {"message": str(e)}}

    # =========================================================================
    # RESPONSE PARSING
    # =========================================================================

    def parse_response(self, raw_response: Dict) -> Dict:
        """
        Parse Anthropic API response to normalized format.
        """
        content_blocks = raw_response.get('content', [])

        # Extract text content
        text_content = ""
        tool_calls = []

        for block in content_blocks:
            if block.get('type') == 'text':
                text_content += block.get('text', '')
            elif block.get('type') == 'tool_use':
                tool_calls.append({
                    "id": block.get('id', ''),
                    "name": block.get('name', ''),
                    "input": block.get('input', {})
                })

        # Extract usage (includes cache stats)
        usage = raw_response.get('usage', {})

        return {
            "content": text_content,
            "tool_calls": tool_calls,
            "usage": {
                "input_tokens": usage.get('input_tokens', 0),
                "output_tokens": usage.get('output_tokens', 0),
                "cache_creation_input_tokens": usage.get('cache_creation_input_tokens', 0),
                "cache_read_input_tokens": usage.get('cache_read_input_tokens', 0)
            },
            "stop_reason": raw_response.get('stop_reason', 'end_turn'),
            "model": raw_response.get('model', '')
        }

    def extract_tool_calls(self, response: Dict) -> List[Dict]:
        """Extract tool calls from normalized response."""
        return response.get('tool_calls', [])
```

---

## 5. Adapter Registry

```python
# adapters/__init__.py
"""
Provider Adapter Registry

Factory for getting the appropriate adapter based on API format.
"""

from .base_adapter import BaseAdapter
from .openai_adapter import OpenAIAdapter
from .anthropic_adapter import AnthropicAdapter
# from .google_adapter import GoogleAdapter  # Future

import logging

_logger = logging.getLogger(__name__)


# Registry of available adapters
ADAPTERS = {
    'openai': OpenAIAdapter,
    'anthropic': AnthropicAdapter,
    # 'google': GoogleAdapter,  # Future
}

# Singleton instances (adapters are stateless)
_adapter_instances = {}


def get_adapter(api_format: str) -> BaseAdapter:
    """
    Get adapter instance for the given API format.

    Args:
        api_format: API format string ('openai', 'anthropic', 'google')

    Returns:
        Adapter instance

    Example:
        adapter = get_adapter('openai')
        response = adapter.call_api(provider, messages, tools)
    """
    # Normalize format
    api_format = (api_format or 'openai').lower().strip()

    # Return cached instance if exists
    if api_format in _adapter_instances:
        return _adapter_instances[api_format]

    # Get adapter class (default to OpenAI for unknown formats)
    adapter_class = ADAPTERS.get(api_format, OpenAIAdapter)

    if api_format not in ADAPTERS:
        _logger.warning(f"[Adapters] Unknown API format '{api_format}', defaulting to OpenAI adapter")

    # Create and cache instance
    instance = adapter_class()
    _adapter_instances[api_format] = instance

    _logger.info(f"[Adapters] Created {adapter_class.__name__} for format '{api_format}'")
    return instance


def list_adapters() -> list:
    """List all available adapter formats."""
    return list(ADAPTERS.keys())


__all__ = [
    'BaseAdapter',
    'OpenAIAdapter',
    'AnthropicAdapter',
    'get_adapter',
    'list_adapters'
]
```

---

## 6. Provider Model Integration

Add this method to `api.service.provider`:

```python
# In api_service_provider.py, add to APIServiceProvider class:

def get_adapter(self):
    """
    Get the appropriate adapter for this provider's API format.

    Returns:
        BaseAdapter instance

    Example:
        provider = env['api.service.provider'].browse(1)
        adapter = provider.get_adapter()
        response = adapter.call_api(provider, messages, tools)
    """
    from ..adapters import get_adapter
    return get_adapter(self.api_format or 'openai')

def call_api(self, messages, tools=None, system_prompt=None, **kwargs):
    """
    Convenience method to call AI API using this provider's configuration.

    Delegates to the appropriate adapter based on api_format.

    Args:
        messages: List of conversation messages
        tools: Optional list of tools (universal format)
        system_prompt: Optional system prompt
        **kwargs: Additional options (max_tokens, temperature, etc.)

    Returns:
        Normalized response dict

    Example:
        provider = env['api.service.provider'].browse(1)
        response = provider.call_api(
            messages=[{"role": "user", "content": "Hello"}],
            tools=UNIVERSAL_TOOLS,
            system_prompt="You are a helpful assistant."
        )
        print(response['content'])
    """
    adapter = self.get_adapter()
    return adapter.call_api(
        provider=self,
        messages=messages,
        tools=tools,
        system_prompt=system_prompt,
        **kwargs
    )

def call_api_streaming(self, messages, tools=None, system_prompt=None, **kwargs):
    """
    Streaming version of call_api.

    Yields:
        Event dicts (chunk, tool_use, usage, done, error)
    """
    adapter = self.get_adapter()
    return adapter.call_api_streaming(
        provider=self,
        messages=messages,
        tools=tools,
        system_prompt=system_prompt,
        **kwargs
    )
```

---

## 7. Usage Example

```python
# Example: Using the adapter system

from odoo.addons.ai_sam_base.adapters import get_adapter
from odoo.addons.ai_sam_base.schemas.universal_tool_schema import UNIVERSAL_TOOLS

# Get a provider (could be Claude, GPT, Groq, etc.)
provider = env['api.service.provider'].search([
    ('vendor_key', '=', 'anthropic'),
    ('is_template', '=', False)
], limit=1)

# Option 1: Use provider's convenience method
response = provider.call_api(
    messages=[{"role": "user", "content": "Read the file /tmp/test.txt"}],
    tools=UNIVERSAL_TOOLS,
    system_prompt="You are SAM AI, a helpful assistant."
)

if response['tool_calls']:
    # Handle tool calls
    for tc in response['tool_calls']:
        print(f"AI wants to call: {tc['name']} with {tc['input']}")

# Option 2: Use adapter directly (more control)
adapter = get_adapter(provider.api_format)
response = adapter.call_api(
    provider=provider,
    messages=messages,
    tools=UNIVERSAL_TOOLS,
    max_tokens=8192,
    temperature=0.7
)

# Streaming example
for event in provider.call_api_streaming(messages, tools=UNIVERSAL_TOOLS):
    if event['type'] == 'chunk':
        print(event['data']['text'], end='', flush=True)
    elif event['type'] == 'tool_use':
        print(f"\n[Tool call: {event['data']['name']}]")
    elif event['type'] == 'done':
        print(f"\n[Done: {event['data']['stop_reason']}]")
```

---

## 8. Migration Path

### Step 1: Create adapter files (Day 1)
- Create `adapters/` directory
- Add `__init__.py`, `base_adapter.py`, `openai_adapter.py`, `anthropic_adapter.py`

### Step 2: Add provider methods (Day 1)
- Add `get_adapter()`, `call_api()`, `call_api_streaming()` to `api.service.provider`

### Step 3: Update ai_brain.py (Day 2-3)
- Replace `_call_openai_api()` calls with `provider.call_api()`
- Replace `_call_claude_api()` calls with `provider.call_api()`
- Remove inline bifurcation code

### Step 4: Update tool definitions (Day 3)
- Convert `SAM_TOOLS_V1` to universal format
- Update references in `sam_voice.py`

### Step 5: Test (Day 4)
- Test with OpenAI provider
- Test with Anthropic provider
- Test tool calling with both
- Test streaming with both

---

## 9. Benefits Summary

| Before | After |
|--------|-------|
| 182 hardcoded provider references | 3 adapter classes |
| Inline `if api_format == 'anthropic'` everywhere | Single dispatch via `get_adapter()` |
| Tool definitions in Anthropic format only | Universal format, auto-converted |
| Adding new provider = touch 10+ files | Adding new provider = 1 adapter file |
| Testing requires mocking both formats | Each adapter testable in isolation |

---

## 10. Future Extensions

### Google Adapter (When Needed)
```python
class GoogleAdapter(BaseAdapter):
    FORMAT_NAME = "google"
    # Implement for Gemini API
```

### AWS Bedrock Adapter (When Needed)
```python
class BedrockAdapter(BaseAdapter):
    FORMAT_NAME = "bedrock"
    # Implement for AWS Bedrock (Claude, Titan, etc.)
```

### MCP Server (Phase 2)
Once adapters are in place, building an MCP server becomes trivial because:
- Tool definitions already in universal format
- Response format already normalized
- MCP just becomes another "adapter" on the client side
