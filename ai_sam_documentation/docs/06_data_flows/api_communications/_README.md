# API Communications

## Purpose
How SAM talks to AI providers (Claude, GPT) - the v2 architecture for all AI API interactions.

## Criteria
- Documents the 2-core-file architecture (system_prompt.py, sam_chat.py)
- Explains session lifecycle and context building
- Shows chat entry points (menu, bubble, canvas, node)
- Documents tool execution patterns
- Covers domain detection and tool loading

## Subfolders
- None yet (single-topic section)

## Examples
- "How a chat message flows through sam_chat.py"
- "Session context building on first message"
- "Tool execution with SAM user audit trail"
- "Domain detection for canvas vs CRM vs sales"
- "Streaming vs non-streaming response handling"

## Does NOT Include
- Frontend UI components (go to 04_modules/ai_sam)
- High-level architecture decisions (go to 05_architecture)
- Prompt writing guidelines (go to 03_prompt_engineering)
