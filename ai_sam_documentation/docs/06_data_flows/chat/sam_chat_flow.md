# SAM AI Chat Flow - Complete Message Journey

This diagram traces the complete flow from user input to SAM AI response.

## Overview Sequence Diagram

```mermaid
sequenceDiagram
    autonumber
    participant User as 👤 User
    participant JS as 📱 sam_chat_vanilla_v2.js
    participant SSE as 🔄 SSE Stream
    participant Ctrl as 🎮 SamAIChatController
    participant Brain as 🧠 ai_brain.py (AIService)
    participant Voice as 🎤 ai_voice.py (System Prompt)
    participant Provider as 🤖 API Provider
    participant Gate as 🔐 ai.access.gate
    participant Tools as 🔧 SAM Tools

    User->>JS: Types message + Enter
    JS->>JS: sendMessage()
    JS->>JS: addMessage({role: 'user'})
    JS->>JS: addMessage({isThinking: true})

    JS->>SSE: POST /sam_ai/chat/send_streaming
    SSE->>Ctrl: send_message_streaming()

    Note over Ctrl: Parse context_data<br/>(node_id vs record_id)

    alt Existing Conversation
        Ctrl->>Brain: send_message_streaming()
    else New Conversation
        Ctrl->>Brain: create_conversation_streaming()
    end

    Brain->>Brain: Load user profile
    Brain->>Brain: Load conversation
    Brain->>Brain: Get provider config

    alt Workflow Node Context
        Brain->>Brain: gather_workflow_node_context()
        Brain->>Brain: Extract folder contents
    end

    Brain->>Voice: _build_system_prompt()
    Voice-->>Brain: System prompt (22k+ chars)

    alt File-related query detected
        Brain->>Brain: _get_sam_tools()
        Note over Brain: Load read_file, list_directory,<br/>glob_files, write_file
    end

    Brain->>Brain: Build messages array
    Brain->>Brain: env.cr.commit()

    loop Tool Loop (max 10 iterations)
        Brain->>Provider: _chat_via_http() or _chat_via_anthropic()
        Provider-->>Brain: Response / Tool Request

        alt Tool Requested
            Brain->>Gate: check_path_access()
            alt Permission Granted
                Gate-->>Brain: {allowed: true}
                Brain->>Tools: Execute tool
                Tools-->>Brain: Tool result
            else Permission Needed
                Gate-->>Brain: {needs_approval: true}
                Brain-->>SSE: permission_required event
                SSE-->>JS: Show permission popup
                JS-->>User: "Allow access to X?"
            end
        else Text Response
            Brain-->>SSE: chunk events
            SSE-->>JS: Update UI
        end
    end

    Brain-->>SSE: done event
    SSE-->>Ctrl: Stream complete
    Ctrl-->>JS: Final response
    JS->>JS: Remove thinking message
    JS->>JS: addMessage({role: 'assistant'})
    JS-->>User: Display response
```

## Detailed Component Flow

```mermaid
flowchart TB
    subgraph "Frontend Layer (ai_sam module)"
        UI[sam_chat_vanilla_v2.js<br/>9,056 lines]
        UI --> |"sendMessage()"| SSE_Client[SSE Client<br/>EventSource]
    end

    subgraph "HTTP Layer"
        SSE_Client --> |"POST /sam_ai/chat/send_streaming"| Endpoint[HTTP Endpoint]
    end

    subgraph "Controller Layer (ai_sam_base)"
        Endpoint --> Controller[SamAIChatController<br/>sam_ai_chat_controller.py:155]

        Controller --> ParseContext{Parse Context}
        ParseContext --> |"node_id present"| WorkflowContext[Workflow Node Context<br/>context_model=None]
        ParseContext --> |"record_id present"| OdooContext[Odoo Record Context<br/>context_id=int]
        ParseContext --> |"neither"| GenericContext[Generic Context]

        WorkflowContext --> RouteConv
        OdooContext --> RouteConv
        GenericContext --> RouteConv

        RouteConv{Conversation<br/>Exists?}
        RouteConv --> |"Yes"| ExistingConv[send_message_streaming<br/>:340]
        RouteConv --> |"No"| NewConv[create_conversation_streaming<br/>:420]
    end

    subgraph "Brain Layer (ai_brain.py - THE BRAIN)"
        ExistingConv --> Brain[AIService Model<br/>ai.service]
        NewConv --> Brain

        Brain --> LoadProfile[Load sam.user.profile<br/>:2054]
        LoadProfile --> LoadConv[Load ai.conversation<br/>:2070]
        LoadConv --> GetProvider[_get_default_provider_config<br/>:86]

        GetProvider --> CheckWorkflow{Is Workflow<br/>Node?}
        CheckWorkflow --> |"Yes"| GatherContext[gather_workflow_node_context<br/>:3230]
        CheckWorkflow --> |"No"| SkipGather[Skip]

        GatherContext --> ExtractFolder[Extract folder_file_link<br/>contents]
        ExtractFolder --> BuildPrompt
        SkipGather --> BuildPrompt

        BuildPrompt[_build_system_prompt<br/>:1767]

        BuildPrompt --> CheckTools{File keywords<br/>in message?}
        CheckTools --> |"Yes"| LoadTools[_get_sam_tools<br/>:2271]
        CheckTools --> |"No"| NoTools[No tools]

        LoadTools --> RouteAPI
        NoTools --> RouteAPI

        RouteAPI{api_format?}
        RouteAPI --> |"openai"| HTTPChat[_chat_via_http<br/>:2688]
        RouteAPI --> |"anthropic"| AnthropicChat[_chat_via_anthropic<br/>SDK streaming]
        RouteAPI --> |"google"| GoogleChat[_chat_via_google<br/>:2298]
    end

    subgraph "API Communication"
        HTTPChat --> |"HTTP POST"| OpenAI[OpenAI API<br/>api.openai.com]
        AnthropicChat --> |"SDK"| Anthropic[Anthropic API<br/>api.anthropic.com]
        GoogleChat --> |"HTTP POST"| Google[Google AI API]

        OpenAI --> |"SSE Stream"| ProcessChunks
        Anthropic --> |"SDK Stream"| ProcessChunks
        Google --> |"SSE Stream"| ProcessChunks
    end

    subgraph "Tool Execution Loop"
        ProcessChunks{Response<br/>Type?}
        ProcessChunks --> |"tool_use"| ToolRequest[Tool Request<br/>:2341]
        ProcessChunks --> |"text"| YieldChunk[Yield chunk event]

        ToolRequest --> CheckPermission[check_path_access<br/>ai.access.gate]

        CheckPermission --> PermResult{Permission?}
        PermResult --> |"Granted"| ExecTool[Execute Tool<br/>sam_voice.py]
        PermResult --> |"Needs Approval"| YieldPermission[Yield permission_required]

        ExecTool --> |"Result"| AddToMessages[Add to messages]
        AddToMessages --> |"Continue loop"| RouteAPI

        YieldChunk --> |"Continue"| ProcessChunks
    end

    subgraph "Response Finalization"
        ProcessChunks --> |"stop/end"| FinalizeResponse[Finalize Response]
        FinalizeResponse --> SaveMessage[Save ai.message<br/>:2541]
        SaveMessage --> LogTokens[Log ai.token.usage<br/>:2550]
        LogTokens --> YieldDone[Yield done event]
    end

    YieldDone --> Controller
    YieldPermission --> Controller
    Controller --> SSE_Client
    SSE_Client --> UI

    classDef frontend fill:#e1f5ff,stroke:#01579b,stroke-width:2px
    classDef controller fill:#fff9c4,stroke:#f57f17,stroke-width:2px
    classDef brain fill:#e8f5e9,stroke:#1b5e20,stroke-width:2px
    classDef api fill:#f3e5f5,stroke:#4a148c,stroke-width:2px
    classDef tools fill:#ffebee,stroke:#c62828,stroke-width:2px

    class UI,SSE_Client frontend
    class Controller,ParseContext,RouteConv,ExistingConv,NewConv,WorkflowContext,OdooContext,GenericContext controller
    class Brain,LoadProfile,LoadConv,GetProvider,CheckWorkflow,GatherContext,ExtractFolder,BuildPrompt,CheckTools,LoadTools,NoTools,RouteAPI,HTTPChat,AnthropicChat,GoogleChat brain
    class OpenAI,Anthropic,Google api
    class ProcessChunks,ToolRequest,CheckPermission,PermResult,ExecTool,YieldPermission,AddToMessages,YieldChunk tools
```

## Files Involved (In Order of Execution)

```mermaid
flowchart LR
    subgraph "1. Frontend"
        A[ai_sam/static/src/js/<br/>sam_chat_vanilla_v2.js]
    end

    subgraph "2. Controller"
        B[ai_sam_base/controllers/<br/>sam_ai_chat_controller.py]
    end

    subgraph "3. Brain (Core)"
        C[ai_sam_base/models/<br/>ai_brain.py]
    end

    subgraph "4. Supporting Models"
        D1[ai_sam_base/models/<br/>ai_conversation.py]
        D2[ai_sam_base/models/<br/>sam_user_profile.py]
        D3[ai_sam_base/models/<br/>api_service_provider.py]
        D4[ai_sam_base/models/<br/>ai_access_gate.py]
    end

    subgraph "5. Voice (Prompts)"
        E[ai_sam_base/api_communications/<br/>ai_voice.py]
        E2[ai_sam_base/data/<br/>sam_ai_master_system_prompt_v2.md]
    end

    subgraph "6. Tools"
        F[ai_sam_base/api_communications/<br/>sam_voice.py]
    end

    A --> B --> C
    C --> D1
    C --> D2
    C --> D3
    C --> D4
    C --> E
    E --> E2
    C --> F
```

## Key Functions Trace

| Step | File | Function | Line | Purpose |
|------|------|----------|------|---------|
| 1 | sam_chat_vanilla_v2.js | `sendMessage()` | 1315 | User triggers send |
| 2 | sam_chat_vanilla_v2.js | `processStream()` | 1442 | SSE event handling |
| 3 | sam_ai_chat_controller.py | `send_message_streaming()` | 155 | HTTP endpoint |
| 4 | sam_ai_chat_controller.py | Parse context | 219-256 | node_id vs record_id |
| 5 | ai_brain.py | `send_message_streaming()` | 1974 | Main orchestrator |
| 6 | ai_brain.py | Load profile | 2054 | Get user context |
| 7 | ai_brain.py | Load conversation | 2070 | Get conversation history |
| 8 | ai_brain.py | `_get_default_provider_config()` | 86 | Get API provider |
| 9 | ai_brain.py | `gather_workflow_node_context()` | 3230 | Extract folder contents |
| 10 | ai_brain.py | `_build_system_prompt()` | 1767 | Build system prompt |
| 11 | ai_brain.py | `_get_sam_tools()` | 2271 | Load file tools |
| 12 | ai_brain.py | `_chat_via_http()` | 2688 | OpenAI API call |
| 13 | ai_brain.py | Tool execution loop | 2341-2465 | Handle tool_use |
| 14 | ai_access_gate.py | `check_path_access()` | - | Permission check |
| 15 | sam_voice.py | Tool functions | - | read_file, list_directory |
| 16 | ai_brain.py | Save message | 2541 | Persist to DB |
| 17 | sam_chat_vanilla_v2.js | Handle done event | 1629 | Update UI |

## State During Flow

```mermaid
stateDiagram-v2
    [*] --> Idle: Page loaded

    state "Frontend State" as Frontend {
        Idle --> Composing: User types
        Composing --> Processing: Enter pressed
        Processing --> WaitingPermission: permission_required
        WaitingPermission --> Processing: Permission granted
        Processing --> Streaming: chunk received
        Streaming --> Streaming: More chunks
        Streaming --> Complete: done event
        Complete --> Idle: Ready for next
    }

    state "Backend State" as Backend {
        state "Controller" as Ctrl {
            ReceiveRequest --> ParseContext
            ParseContext --> RouteToExisting: conversation_id
            ParseContext --> RouteToNew: no conversation_id
        }

        state "Brain" as BrainState {
            LoadProfile --> LoadConversation
            LoadConversation --> GetConfig
            GetConfig --> BuildContext
            BuildContext --> BuildPrompt
            BuildPrompt --> APICall
            APICall --> ProcessResponse
            ProcessResponse --> ToolLoop: tool_use
            ToolLoop --> APICall: Continue
            ProcessResponse --> FinalizeResponse: text complete
        }
    }
```

## Error Handling Points

```mermaid
flowchart TB
    subgraph "Error Checkpoints"
        E1[No message provided] --> |"400"| ERR1[error event: Message required]
        E2[No API key] --> |"Config error"| ERR2[error event: API key not configured]
        E3[Permission denied] --> |"Access denied"| ERR3[permission_required event]
        E4[API timeout] --> |"HTTP error"| ERR4[Streaming error logged]
        E5[Tool execution fails] --> |"Tool error"| ERR5[Error in tool result]
        E6[JSON parse error] --> |"UnboundLocalError"| ERR6[Fixed: json import issue]
    end

    ERR1 --> UI[Frontend shows error]
    ERR2 --> UI
    ERR3 --> PermPopup[Permission popup]
    ERR4 --> UI
    ERR5 --> ContinueWithError[Continue with error message]
    ERR6 --> ContinueWithError
```

---

## Recent Fixes (2025-12-17)

1. **`invalid literal for int()` error**: Fixed by properly parsing `node_id` vs `record_id` in controller
2. **`UnboundLocalError: json`**: Fixed by removing redundant local `import json` that shadowed module import
3. **Workflow context not loaded**: Fixed by adding `gather_workflow_node_context()` to streaming method
4. **"Thinking..." indicator persisting**: Fixed by setting `isProcessing=false` before `addMessage()`

---

*Last Updated: December 17, 2025*
*Module: ai_sam + ai_sam_base*
