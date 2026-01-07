# Data Flows

## Purpose
How data moves through SAM AI - the technical "how" of each major subsystem.

## Criteria
- Explains how data flows from A to B
- Documents APIs, endpoints, message passing
- Shows sequence of operations
- Technical implementation details

## Subfolders
- `canvas/` - Canvas rendering, node management, overlay system
- `chat/` - Chat message flow, conversation handling
- `apis/` - API endpoints, external integrations
- `node_creation/` - How nodes are created and managed
- `system_prompt_builder/` - How dynamic prompts are constructed

## Examples
- How a chat message flows from UI to Claude and back
- Canvas node creation sequence
- System prompt assembly process
- API authentication flow

## Does NOT Include
- High-level architecture (go to 05_architecture)
- Module reference docs (go to 04_modules)
- How to write prompts (go to 03_prompt_engineering)
