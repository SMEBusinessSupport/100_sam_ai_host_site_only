# SAM AI - UI Module Architecture Diagrams

## System Architecture Overview

```mermaid
---
title: SAM AI - UI Module System Architecture
---

graph TB
    subgraph "User Layer"
        Browser[Web Browser]
        ClaudeDesktop[Claude Desktop<br/>MCP Client]
    end

    subgraph "ai_sam Module (UI Layer - THIS MODULE)"
        Views[18 View XML Files<br/>Form, Tree, Kanban, Client Actions]
        ChatJS[sam_chat_vanilla_v2.js<br/>9,056 lines Vanilla JS]
        CanvasJS[Canvas Framework<br/>4 JavaScript files]
        WidgetsJS[Widgets & Components<br/>6 JavaScript files]
        UtilsJS[Utilities & State<br/>8 JavaScript files]
        CSS[8 CSS Files<br/>Purple Branding]
        VendorLib[Vendor Library<br/>203 API Provider Icons]
        Templates[QWeb Templates<br/>Chat, Memory, Canvas]
        Menus[Consolidated Menus<br/>Single Source of Truth]
    end

    subgraph "ai_sam_base Module (Data Layer - SEPARATE)"
        Controllers[10 HTTP Controllers<br/>67 REST Endpoints]
        Models[43 Python Models<br/>Business Logic]
        Security[Access Control<br/>20 Rules]
    end

    subgraph "ai_sam_workflows_base Module (Workflow Data)"
        WorkflowModels[15 Workflow Models<br/>Canvas, Executions, Templates]
        N8NIntegration[N8N Integration<br/>195 Node Types]
    end

    subgraph "External Systems"
        ChromaDB[(ChromaDB<br/>Vector Storage)]
        ApacheAGE[(PostgreSQL + AGE<br/>Graph Database)]
        ClaudeAPI[Claude API]
        OpenAIAPI[OpenAI API]
        GoogleAPI[Google AI APIs]
        MCPServers[Generated MCP Servers<br/>Standalone Python]
    end

    %% User interactions
    Browser --> Views
    Browser --> ChatJS
    Browser --> CanvasJS
    ClaudeDesktop -.->|MCP Protocol| MCPServers

    %% UI Layer connections
    Views --> Menus
    Views --> Templates
    ChatJS --> WidgetsJS
    ChatJS --> UtilsJS
    CanvasJS --> UtilsJS
    ChatJS --> CSS
    Views --> VendorLib

    %% Backend connections
    ChatJS -->|AJAX/RPC| Controllers
    CanvasJS -->|AJAX/RPC| Controllers
    WidgetsJS -->|AJAX/RPC| Controllers
    Controllers --> Models
    Controllers --> Security
    Models --> WorkflowModels

    %% External connections
    Models -.->|Vector Search| ChromaDB
    Models -.->|Graph Queries| ApacheAGE
    Models -.->|AI Requests| ClaudeAPI
    Models -.->|AI Requests| OpenAIAPI
    Models -.->|AI Requests| GoogleAPI
    MCPServers -.->|Odoo RPC| Models

    %% Styling
    classDef uiLayer fill:#e1f5ff,stroke:#01579b,stroke-width:2px
    classDef dataLayer fill:#e8f5e9,stroke:#1b5e20,stroke-width:2px
    classDef workflowLayer fill:#fff9c4,stroke:#f57f17,stroke-width:2px
    classDef external fill:#ffebee,stroke:#b71c1c,stroke-width:1px,stroke-dasharray: 5 5
    classDef user fill:#f3e5f5,stroke:#4a148c,stroke-width:2px

    class Views,ChatJS,CanvasJS,WidgetsJS,UtilsJS,CSS,VendorLib,Templates,Menus uiLayer
    class Controllers,Models,Security dataLayer
    class WorkflowModels,N8NIntegration workflowLayer
    class ChromaDB,ApacheAGE,ClaudeAPI,OpenAIAPI,GoogleAPI,MCPServers external
    class Browser,ClaudeDesktop user
```

---

## Platform Skin Architecture (Migration 2025-11-30)

```mermaid
---
title: Platform Skin Architecture - UI/Data Layer Separation
---

flowchart LR
    subgraph "Before Migration (Legacy)"
        OldModule[ai_sam<br/>Monolithic Module]
        OldModule --> OldPython[43 Python Models]
        OldModule --> OldControllers[10 Controllers]
        OldModule --> OldViews[18 View Files]
        OldModule --> OldJS[JavaScript Assets]
    end

    subgraph "After Migration (Current - 2025-11-30)"
        direction TB

        subgraph "ai_sam (UI-Only Layer)"
            UIViews[18 View XML Files<br/>ONLY UI DEFINITIONS]
            UIStatic[Static Assets<br/>JavaScript, CSS, Icons]
            UITemplates[QWeb Templates]
            UIMenus[Menu Definitions]

            UIViews --> UIStatic
            UIViews --> UITemplates
            UIViews --> UIMenus
        end

        subgraph "ai_sam_base (Data Layer)"
            DataModels[43 Python Models<br/>ALL BUSINESS LOGIC]
            DataControllers[10 HTTP Controllers<br/>ALL ENDPOINTS]
            DataSecurity[Access Control]

            DataModels --> DataControllers
            DataModels --> DataSecurity
        end

        UIViews -->|Depends on| DataModels
        UIStatic -->|AJAX/RPC Calls| DataControllers
    end

    OldModule ==>|Migration| UIViews
    OldModule ==>|Migration| DataModels

    style OldModule fill:#ffcdd2,stroke:#c62828,stroke-width:2px
    style UIViews fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px
    style DataModels fill:#81c784,stroke:#1b5e20,stroke-width:2px
```

**Benefits:**
- **Separation of Concerns**: UI changes don't require Python restarts
- **Independent Updates**: Update views without affecting business logic
- **Clearer Dependencies**: ai_sam depends on ai_sam_base (unidirectional)
- **Easier Testing**: Test business logic without UI complexity

---

## View Layer Architecture (18 XML Files)

```mermaid
---
title: SAM AI - View Layer Structure
---

graph TB
    Root[sam_ai_menus_consolidated.xml<br/>Root Menu Structure]

    subgraph "Main Views (13 Files)"
        ChatView[sam_ai_chat_v2_action.xml<br/>Client Action - Chat Interface]
        APIProviderView[api_service_provider_views.xml<br/>8-Tab Progressive Disclosure]
        MemoryDashView[ai_memory_dashboard_simple.xml<br/>Client Action - Memory Stats]
        MCPView[mcp_server_config_views.xml<br/>MCP Server Generation]
        PowerPromptsView[sam_mode_context_view.xml<br/>Hierarchical AI Agents]
        CostView[ai_service_cost_comparison_views.xml<br/>Pivot/Graph Cost Analysis]
        WorkspaceView[ai_workspace_views.xml<br/>Team Collaboration]
        ConvReaderView[ai_conversation_reader_views.xml<br/>Conversation Browser]
        ProviderModelView[ai_provider_model_views.xml<br/>AI Model Config]
        ConvView[ai_conversation_views.xml<br/>Conversation Management]
        MessageView[ai_conversation_message_views.xml<br/>Message Display]
        ServiceView[ai_service_views.xml<br/>AI Service Config]
        CredsView[api_credentials_views.xml<br/>Encrypted API Keys]
    end

    subgraph "Memory Views (5 Files)"
        MemoryGraphView[memory_graph_simple.xml<br/>Vis.js Graph Template]
        VectorView[ai_memory_vector_views.xml<br/>ChromaDB Vectors]
        ConnectionView[ai_memory_connection_views.xml<br/>Graph Connections]
        EntityView[ai_memory_entity_views.xml<br/>Graph Entities]
        AccessLogView[ai_memory_access_log_views.xml<br/>Access Auditing]
    end

    Root --> ChatView
    Root --> APIProviderView
    Root --> MemoryDashView
    Root --> MCPView
    Root --> PowerPromptsView
    Root --> CostView
    Root --> WorkspaceView
    Root --> ConvReaderView

    APIProviderView --> CredsView
    ChatView --> ConvView
    ConvView --> MessageView
    ChatView --> ServiceView
    ServiceView --> ProviderModelView

    MemoryDashView --> MemoryGraphView
    MemoryDashView --> VectorView
    MemoryDashView --> ConnectionView
    MemoryDashView --> EntityView
    MemoryDashView --> AccessLogView

    classDef mainView fill:#e1f5ff,stroke:#01579b,stroke-width:2px
    classDef memoryView fill:#f3e5f5,stroke:#4a148c,stroke-width:2px
    classDef rootView fill:#fff9c4,stroke:#f57f17,stroke-width:2px

    class ChatView,APIProviderView,MCPView,PowerPromptsView,CostView,WorkspaceView,ConvReaderView,ProviderModelView,ConvView,MessageView,ServiceView,CredsView mainView
    class MemoryDashView,MemoryGraphView,VectorView,ConnectionView,EntityView,AccessLogView memoryView
    class Root rootView
```

---

## JavaScript Architecture (18 Files)

```mermaid
---
title: SAM AI - JavaScript Module Structure
---

graph TB
    subgraph "Entry Point"
        ChatMain[sam_chat_vanilla_v2.js<br/>9,056 lines<br/>Main Chat Interface]
    end

    subgraph "Core Frameworks (4 Files)"
        CanvasEngine[canvas_engine.js<br/>HTML5 Canvas Rendering]
        CanvasSizer[canvas_sizer.js<br/>Coordinate Transforms]
        CanvasNodeMgr[canvas_node_manager.js<br/>Node CRUD Operations]
        PlatformLoader[platform_loader.js<br/>Platform Adapters]
    end

    subgraph "Widgets & Components (6 Files)"
        ChatBubble[chat_bubble_widget.js<br/>Chat Launcher<br/>Re-enabled 2025-12-04]
        TokenCounter[token_counter_widget.js<br/>Token Display<br/>Re-enabled 2025-12-04]
        CostAnalysis[cost_analysis.js<br/>Cost Intelligence]
        WorkspaceMgr[workspace_manager.js<br/>Team Collaboration]
        ConvReader[conversation_reader.js<br/>Conversation Browser]
        HierarchicalAgents[hierarchical_agents.js<br/>Power Prompts UI]
    end

    subgraph "Utilities & State (8 Files)"
        MCPGen[mcp_server_generator.js<br/>MCP Server Generation]
        MemoryGraphVis[memory_graph_vis.js<br/>Vis.js Integration]
        APIProviderTabs[api_provider_tabs.js<br/>8-Tab Progressive Disclosure]
        MemoryDash[memory_dashboard.js<br/>Memory Statistics]
        DebugLogger[debug_logger.js<br/>Frontend Logging]
        StateMgr[state_manager.js<br/>Proxy-Based Reactivity]
        Utils[utils.js<br/>Utility Functions]
    end

    %% Entry point connections
    ChatMain --> ChatBubble
    ChatMain --> TokenCounter
    ChatMain --> StateMgr
    ChatMain --> Utils

    %% Canvas framework connections
    CanvasEngine --> CanvasSizer
    CanvasEngine --> CanvasNodeMgr
    CanvasEngine --> PlatformLoader
    PlatformLoader --> Utils

    %% Widget connections
    ChatBubble --> StateMgr
    TokenCounter --> StateMgr
    CostAnalysis --> Utils
    WorkspaceMgr --> StateMgr
    ConvReader --> Utils
    HierarchicalAgents --> Utils

    %% Utility connections
    MCPGen --> Utils
    MemoryGraphVis --> MemoryDash
    APIProviderTabs --> StateMgr
    MemoryDash --> StateMgr
    DebugLogger --> Utils

    %% Styling
    classDef entryPoint fill:#714B67,color:#fff,stroke:#4a148c,stroke-width:3px
    classDef framework fill:#e1f5ff,stroke:#01579b,stroke-width:2px
    classDef widget fill:#fff9c4,stroke:#f57f17,stroke-width:2px
    classDef utility fill:#e8f5e9,stroke:#1b5e20,stroke-width:2px

    class ChatMain entryPoint
    class CanvasEngine,CanvasSizer,CanvasNodeMgr,PlatformLoader framework
    class ChatBubble,TokenCounter,CostAnalysis,WorkspaceMgr,ConvReader,HierarchicalAgents widget
    class MCPGen,MemoryGraphVis,APIProviderTabs,MemoryDash,DebugLogger,StateMgr,Utils utility
```

---

## Vanilla JavaScript State Management (Proxy-Based Reactivity)

```mermaid
---
title: Reactive State Management - Proxy Pattern
---

sequenceDiagram
    actor User
    participant DOM as DOM Elements
    participant Proxy as State Proxy
    participant StateMap as STATE_TO_DOM_MAP
    participant Updaters as DOM Updaters

    User->>DOM: Interacts (e.g., sends message)
    DOM->>Proxy: Update state property<br/>chatState.messages = [...]

    activate Proxy
    Note over Proxy: Proxy set trap intercepts
    Proxy->>Proxy: target[property] = value
    Proxy->>StateMap: Lookup updaters for 'messages'

    StateMap-->>Proxy: [renderMessages, updateTokenCount, ...]

    loop For each updater
        Proxy->>Updaters: Execute updater(value)
        Updaters->>DOM: Update DOM elements
    end

    deactivate Proxy

    DOM-->>User: Visual feedback (updated UI)

    Note over Proxy,StateMap: Automatic reactivity<br/>No manual DOM manipulation needed
```

**Implementation Example:**

```javascript
// state_manager.js
const STATE_TO_DOM_MAP = {
    messages: [
        (messages) => renderMessageList(messages),
        (messages) => updateTokenCount(messages),
        (messages) => updateScrollPosition()
    ],
    isStreaming: [
        (streaming) => toggleSpinner(streaming),
        (streaming) => disableSendButton(streaming)
    ],
    activeConversationId: [
        (id) => switchConversationTab(id),
        (id) => loadConversationHistory(id)
    ]
};

const chatState = new Proxy({
    messages: [],
    isStreaming: false,
    activeConversationId: null,
    tokenCount: 0
}, {
    set(target, property, value) {
        target[property] = value;

        // Automatically trigger all registered updaters
        STATE_TO_DOM_MAP[property]?.forEach(updater => {
            try {
                updater(value);
            } catch (error) {
                console.error(`Error updating ${property}:`, error);
            }
        });

        return true;
    }
});
```

---

## Chat Interface User Flow

```mermaid
---
title: Chat Interface V2 - User Interaction Flow
---

stateDiagram-v2
    [*] --> ChatBubble: User opens page

    state ChatBubble {
        [*] --> Minimized: Bubble visible
        Minimized --> Expanded: Click bubble
        Expanded --> Minimized: Click minimize
    }

    ChatBubble --> ChatInterface: Click bubble

    state ChatInterface {
        [*] --> SelectConversation: Load conversations

        state SelectConversation {
            [*] --> ConversationList: Display tabs
            ConversationList --> NewConversation: Click "New"
            ConversationList --> ExistingConversation: Click tab
        }

        SelectConversation --> ComposeMessage

        state ComposeMessage {
            [*] --> TypeMessage: User types
            TypeMessage --> AttachFiles: Optional
            AttachFiles --> TokenCounter: Auto-calculate
            TokenCounter --> ReadyToSend: Show cost estimate
        }

        ComposeMessage --> SendMessage: Click send

        state SendMessage {
            [*] --> StreamResponse: SSE connection
            StreamResponse --> RenderMarkdown: Chunk received
            RenderMarkdown --> UpdateMemory: Save to memory
            UpdateMemory --> Complete: Stream ends
        }

        SendMessage --> ComposeMessage: Continue conversation
        SendMessage --> SelectConversation: Switch conversation
    }

    ChatInterface --> [*]: Close chat

    note right of ChatBubble
        Re-enabled 2025-12-04
        Floating launcher
        Minimize/Maximize
    end note

    note right of TokenCounter
        Re-enabled 2025-12-04
        Shows input/output tokens
        Estimates cost before send
    end note

    note right of StreamResponse
        Real-time SSE streaming
        Markdown rendered as received
        Syntax highlighting applied
    end note
```

---

## Memory System Architecture

```mermaid
---
title: Dual Database Memory System
---

graph TB
    subgraph "Frontend (ai_sam)"
        ChatUI[Chat Interface]
        MemoryDashUI[Memory Dashboard]
        GraphVisUI[Vis.js Graph Visualization]
    end

    subgraph "Backend (ai_sam_base)"
        MemoryService[Memory Service<br/>Python Business Logic]
        VectorEmbedder[Vector Embedder<br/>Sentence Transformers]
        GraphBuilder[Graph Builder<br/>Entity Extraction]
    end

    subgraph "ChromaDB (Vector Database)"
        Collections[Collections<br/>Per-User/Workspace]
        Vectors[Vector Embeddings<br/>768-dimensional]
        VectorSearch[Similarity Search<br/>Cosine Distance]
    end

    subgraph "PostgreSQL + Apache AGE (Graph Database)"
        Entities[Entities<br/>Users, Concepts, Topics]
        Connections[Connections<br/>Relationships with Weights]
        GraphQueries[Graph Traversal<br/>Cypher Queries]
    end

    %% Frontend connections
    ChatUI -->|Create memory| MemoryService
    ChatUI -->|Search memory| MemoryService
    MemoryDashUI -->|Load statistics| MemoryService
    GraphVisUI -->|Load graph data| MemoryService

    %% Backend processing
    MemoryService --> VectorEmbedder
    MemoryService --> GraphBuilder

    VectorEmbedder -->|Store embeddings| Collections
    VectorEmbedder -->|Query| VectorSearch
    VectorSearch -->|Return similar| Vectors

    GraphBuilder -->|Create entities| Entities
    GraphBuilder -->|Create connections| Connections
    GraphBuilder -->|Query relationships| GraphQueries
    GraphQueries -->|Return paths| Connections

    %% Retrieval flow
    Vectors -->|Semantic results| MemoryService
    Connections -->|Relationship results| MemoryService
    MemoryService -->|Merged results| ChatUI

    classDef frontend fill:#e1f5ff,stroke:#01579b,stroke-width:2px
    classDef backend fill:#e8f5e9,stroke:#1b5e20,stroke-width:2px
    classDef vectorDB fill:#fff9c4,stroke:#f57f17,stroke-width:2px
    classDef graphDB fill:#f3e5f5,stroke:#4a148c,stroke-width:2px

    class ChatUI,MemoryDashUI,GraphVisUI frontend
    class MemoryService,VectorEmbedder,GraphBuilder backend
    class Collections,Vectors,VectorSearch vectorDB
    class Entities,Connections,GraphQueries graphDB
```

**Memory Creation Flow:**

```mermaid
---
title: Memory Creation and Storage
---

sequenceDiagram
    actor User
    participant Chat as Chat Interface
    participant MemSvc as Memory Service
    participant Embedder as Vector Embedder
    participant GraphBuilder as Graph Builder
    participant ChromaDB
    participant ApacheAGE

    User->>Chat: Sends message
    Chat->>MemSvc: Store conversation

    par Vector Processing
        MemSvc->>Embedder: Generate embedding
        Embedder->>Embedder: Sentence Transformers<br/>768-dim vector
        Embedder->>ChromaDB: Store vector + metadata
        ChromaDB-->>MemSvc: Vector ID
    and Graph Processing
        MemSvc->>GraphBuilder: Extract entities
        GraphBuilder->>GraphBuilder: NER + Relationship Extraction
        GraphBuilder->>ApacheAGE: Create entities + connections
        ApacheAGE-->>MemSvc: Graph node IDs
    end

    MemSvc-->>Chat: Memory stored successfully
    Chat-->>User: Confirmation
```

**Memory Retrieval Flow:**

```mermaid
---
title: Memory Retrieval with Dual Search
---

sequenceDiagram
    actor User
    participant Chat as Chat Interface
    participant MemSvc as Memory Service
    participant ChromaDB
    participant ApacheAGE

    User->>Chat: Asks question about past
    Chat->>MemSvc: Search memory(query)

    par Semantic Search
        MemSvc->>ChromaDB: Vector similarity search
        ChromaDB-->>MemSvc: Top 10 similar memories
    and Graph Search
        MemSvc->>ApacheAGE: Graph traversal query
        ApacheAGE-->>MemSvc: Connected entities
    end

    MemSvc->>MemSvc: Merge + Rank results
    MemSvc-->>Chat: Ranked memory list
    Chat->>Chat: Inject into prompt context
    Chat-->>User: AI response with memory context
```

---

## Canvas Framework Architecture

```mermaid
---
title: Canvas Framework - Platform-Agnostic Design
---

graph TB
    subgraph "Platform Adapters"
        OdooPlatform[Odoo Platform Adapter]
        N8NPlatform[N8N Platform Adapter]
        FuturePlatform[Future Platform Adapter]
    end

    subgraph "Canvas Core (Platform-Agnostic)"
        CanvasEngine[Canvas Engine<br/>HTML5 Canvas Rendering]
        CoordSystem[Coordinate System<br/>World-Screen Transforms]
        NodeManager[Node Manager<br/>CRUD + Undo/Redo]
        ConnectionMgr[Connection Manager<br/>Edge Routing]
        EventHandler[Event Handler<br/>Mouse/Touch/Keyboard]
    end

    subgraph "Rendering Pipeline"
        DrawNodes[Draw Nodes]
        DrawConnections[Draw Connections]
        DrawLabels[Draw Labels]
        DrawPorts[Draw Ports]
    end

    subgraph "Storage Formats"
        OdooJSON[Odoo Workflow JSON]
        N8NJSON[N8N Workflow JSON]
        GenericJSON[Generic Canvas JSON]
    end

    %% Platform loading
    PlatformLoader[platform_loader.js] --> OdooPlatform
    PlatformLoader --> N8NPlatform
    PlatformLoader --> FuturePlatform

    %% Adapter connections
    OdooPlatform --> CanvasEngine
    N8NPlatform --> CanvasEngine
    FuturePlatform --> CanvasEngine

    %% Core connections
    CanvasEngine --> CoordSystem
    CanvasEngine --> NodeManager
    CanvasEngine --> ConnectionMgr
    CanvasEngine --> EventHandler

    %% Rendering pipeline
    CanvasEngine --> DrawNodes
    CanvasEngine --> DrawConnections
    DrawNodes --> DrawLabels
    DrawNodes --> DrawPorts

    %% Storage connections
    NodeManager --> OdooJSON
    NodeManager --> N8NJSON
    NodeManager --> GenericJSON

    classDef platform fill:#e1f5ff,stroke:#01579b,stroke-width:2px
    classDef core fill:#e8f5e9,stroke:#1b5e20,stroke-width:2px
    classDef render fill:#fff9c4,stroke:#f57f17,stroke-width:2px
    classDef storage fill:#f3e5f5,stroke:#4a148c,stroke-width:2px

    class OdooPlatform,N8NPlatform,FuturePlatform,PlatformLoader platform
    class CanvasEngine,CoordSystem,NodeManager,ConnectionMgr,EventHandler core
    class DrawNodes,DrawConnections,DrawLabels,DrawPorts render
    class OdooJSON,N8NJSON,GenericJSON storage
```

**Coordinate Transformation System:**

```mermaid
---
title: Canvas Coordinate Transformations
---

flowchart LR
    MouseEvent[Mouse Event<br/>Screen Coordinates<br/>x: 500, y: 300]

    ScreenToWorld[canvas_sizer.js<br/>screenToWorld]

    WorldCoords[World Coordinates<br/>x: 1000, y: 600<br/>Scaled by zoom]

    NodeCheck{Node at<br/>coordinates?}

    MouseEvent --> ScreenToWorld
    ScreenToWorld --> WorldCoords
    WorldCoords --> NodeCheck

    NodeCheck -->|Yes| SelectNode[Select Node]
    NodeCheck -->|No| Pan[Pan Canvas]

    SelectNode --> Render
    Pan --> Render

    Render[Render Loop] --> WorldToScreen[worldToScreen<br/>Convert back for drawing]
    WorldToScreen --> DrawCanvas[Draw on HTML5 Canvas]

    style MouseEvent fill:#e1f5ff
    style WorldCoords fill:#fff9c4
    style DrawCanvas fill:#c8e6c9
```

---

## API Provider Configuration (8-Tab Progressive Disclosure)

```mermaid
---
title: API Provider 8-Tab Wizard Flow
---

stateDiagram-v2
    [*] --> Tab1General: Open wizard

    state Tab1General {
        [*] --> EnterName: Name field
        EnterName --> SelectProvider: Choose from 203 vendors
        SelectProvider --> SetStatus: Active/Inactive
    }

    Tab1General --> Tab2Authentication: Next

    state Tab2Authentication {
        [*] --> SelectAuthType: API Key / OAuth / Custom
        SelectAuthType --> EnterCredentials: Encrypted storage
        EnterCredentials --> TestConnection: Validate
    }

    Tab2Authentication --> Tab3Models: Next

    state Tab3Models {
        [*] --> LoadAvailableModels: Fetch from provider
        LoadAvailableModels --> SelectModels: GPT-4, Claude, etc.
        SelectModels --> SetDefaultModel: Choose default
    }

    Tab3Models --> Tab4Endpoints: Next

    state Tab4Endpoints {
        [*] --> ConfigureBaseURL: Base API URL
        ConfigureBaseURL --> ConfigureEndpoints: Chat, Embeddings, etc.
        ConfigureEndpoints --> SetHeaders: Custom headers
    }

    Tab4Endpoints --> Tab5RateLimits: Next

    state Tab5RateLimits {
        [*] --> SetRequestLimit: Requests per period
        SetRequestLimit --> SetPeriod: Minute/Hour/Day
        SetPeriod --> SetRetry: Retry logic
    }

    Tab5RateLimits --> Tab6Cost: Next

    state Tab6Cost {
        [*] --> EnterInputCost: Cost per million input tokens
        EnterInputCost --> EnterOutputCost: Cost per million output tokens
        EnterOutputCost --> SetBudget: Optional budget alerts
    }

    Tab6Cost --> Tab7Advanced: Next

    state Tab7Advanced {
        [*] --> SetTimeout: Request timeout
        SetTimeout --> ConfigureProxy: Optional proxy
        ConfigureProxy --> CustomParams: Custom parameters
    }

    Tab7Advanced --> Tab8Testing: Next

    state Tab8Testing {
        [*] --> WriteSampleRequest: Test prompt
        WriteSampleRequest --> SendTestRequest: Execute
        SendTestRequest --> ViewResponse: Check result
        ViewResponse --> ValidationResult: Success/Failure
    }

    Tab8Testing --> Save: Save provider
    Save --> [*]: Provider configured

    note right of Tab1General
        203 vendor icons loaded from
        static/vendor_library/_registry/
    end note

    note right of Tab2Authentication
        API keys encrypted using
        Odoo's encryption system
    end note

    note right of Tab8Testing
        Live API testing before save
        Validates credentials and configuration
    end note
```

---

## MCP Server Generation Flow

```mermaid
---
title: MCP Server Generation and Deployment
---

sequenceDiagram
    actor User
    participant UI as MCP Config UI
    participant MCPGen as mcp_server_generator.js
    participant Backend as ai_sam_base Controller
    participant MCPServer as Generated Python Server
    participant ClaudeDesktop as Claude Desktop

    User->>UI: Create MCP Server Config
    UI->>User: Show wizard (model selection, permissions)
    User->>UI: Select Odoo models (res.partner, sale.order)
    User->>UI: Configure permissions (read-only, CRUD)
    User->>MCPGen: Click "Generate Server"

    MCPGen->>Backend: POST /generate_mcp_server
    Backend->>Backend: Generate Python code<br/>Using MCP SDK templates
    Backend->>Backend: Include selected models<br/>Apply permission rules
    Backend-->>MCPGen: Python server code

    MCPGen->>UI: Display generated code
    UI->>User: Download or deploy options

    alt Local Deployment
        User->>MCPGen: Click "Deploy Locally"
        MCPGen->>Backend: Deploy to systemd
        Backend->>Backend: Create systemd service<br/>Start server
        Backend-->>UI: Server running on localhost:8080
    else Download
        User->>UI: Click "Download"
        UI->>User: mcp_server_odoo.py downloaded
        User->>MCPServer: Manual deployment
    end

    User->>ClaudeDesktop: Configure MCP server URL
    ClaudeDesktop->>MCPServer: Connect via MCP protocol
    MCPServer-->>ClaudeDesktop: Available tools listed

    User->>ClaudeDesktop: Query Odoo data
    ClaudeDesktop->>MCPServer: MCP tool call
    MCPServer->>Backend: Odoo RPC call
    Backend-->>MCPServer: Query results
    MCPServer-->>ClaudeDesktop: Formatted response
    ClaudeDesktop-->>User: Answer with Odoo data
```

**Generated MCP Server Structure:**

```mermaid
---
title: Generated MCP Server Architecture
---

graph TB
    subgraph "Generated Server (Python)"
        MCPMain[main.py<br/>MCP Server Entry Point]
        ToolRegistry[tool_registry.py<br/>Registered Tools]
        OdooConnector[odoo_connector.py<br/>Odoo RPC Client]
        PermissionLayer[permissions.py<br/>Access Control]
    end

    subgraph "MCP SDK (Anthropic)"
        MCPServer[MCP Server Class]
        MCPTools[Tool Decorators]
        MCPProtocol[MCP Protocol Handler]
    end

    subgraph "Odoo Backend"
        OdooRPC[Odoo JSON-RPC<br/>Port 8069]
        Models[Odoo Models<br/>res.partner, sale.order]
    end

    subgraph "Claude Desktop"
        ClaudeUI[Claude UI]
        MCPClient[MCP Client]
    end

    %% Server structure
    MCPMain --> ToolRegistry
    MCPMain --> OdooConnector
    MCPMain --> PermissionLayer

    %% MCP SDK integration
    MCPMain --> MCPServer
    ToolRegistry --> MCPTools
    MCPServer --> MCPProtocol

    %% Odoo connection
    OdooConnector --> OdooRPC
    OdooRPC --> Models
    PermissionLayer --> OdooConnector

    %% Claude connection
    ClaudeUI --> MCPClient
    MCPClient --> MCPProtocol
    MCPProtocol --> ToolRegistry

    classDef server fill:#e1f5ff,stroke:#01579b,stroke-width:2px
    classDef sdk fill:#fff9c4,stroke:#f57f17,stroke-width:2px
    classDef odoo fill:#e8f5e9,stroke:#1b5e20,stroke-width:2px
    classDef claude fill:#f3e5f5,stroke:#4a148c,stroke-width:2px

    class MCPMain,ToolRegistry,OdooConnector,PermissionLayer server
    class MCPServer,MCPTools,MCPProtocol sdk
    class OdooRPC,Models odoo
    class ClaudeUI,MCPClient claude
```

---

## Deployment Architecture

```mermaid
---
title: SAM AI - Production Deployment
---

graph TB
    subgraph "CDN Layer"
        CDN[CDN<br/>Static Assets<br/>JS, CSS, Icons]
    end

    subgraph "Load Balancer"
        LB[Nginx / HAProxy<br/>SSL Termination]
    end

    subgraph "Odoo Application Servers"
        Odoo1[Odoo Instance 1<br/>ai_sam + ai_sam_base]
        Odoo2[Odoo Instance 2<br/>ai_sam + ai_sam_base]
        Odoo3[Odoo Instance 3<br/>ai_sam + ai_sam_base]
    end

    subgraph "Database Layer"
        PGPrimary[(PostgreSQL Primary<br/>+ Apache AGE)]
        PGReplica1[(PostgreSQL Replica 1)]
        PGReplica2[(PostgreSQL Replica 2)]
    end

    subgraph "Memory Systems"
        ChromaDB[(ChromaDB Cluster<br/>Vector Storage)]
        RedisCache[(Redis Cache<br/>Session + State)]
    end

    subgraph "Background Workers"
        Worker1[Celery Worker 1<br/>Async Tasks]
        Worker2[Celery Worker 2<br/>Async Tasks]
        Cron[Odoo Cron<br/>Scheduled Tasks]
    end

    subgraph "External APIs"
        ClaudeAPI[Claude API<br/>Anthropic]
        OpenAIAPI[OpenAI API]
        GoogleAPI[Google AI APIs]
    end

    subgraph "MCP Servers"
        MCPServer1[MCP Server 1<br/>Odoo Contacts]
        MCPServer2[MCP Server 2<br/>Odoo Sales]
        MCPServer3[MCP Server 3<br/>Custom Integration]
    end

    subgraph "Monitoring"
        Prometheus[Prometheus<br/>Metrics]
        Grafana[Grafana<br/>Dashboards]
        Sentry[Sentry<br/>Error Tracking]
    end

    %% User connections
    Users[Web Users<br/>Chat Interface] --> CDN
    Users --> LB
    CDN -.->|Static Assets| Users

    %% Load balancing
    LB --> Odoo1
    LB --> Odoo2
    LB --> Odoo3

    %% Database connections
    Odoo1 --> PGPrimary
    Odoo2 --> PGPrimary
    Odoo3 --> PGPrimary
    PGPrimary --> PGReplica1
    PGPrimary --> PGReplica2

    %% Memory systems
    Odoo1 --> ChromaDB
    Odoo2 --> ChromaDB
    Odoo3 --> ChromaDB
    Odoo1 --> RedisCache
    Odoo2 --> RedisCache
    Odoo3 --> RedisCache

    %% Background workers
    Odoo1 --> Worker1
    Odoo2 --> Worker2
    Odoo1 --> Cron

    %% External APIs
    Worker1 -.->|AI Requests| ClaudeAPI
    Worker1 -.->|AI Requests| OpenAIAPI
    Worker2 -.->|AI Requests| GoogleAPI

    %% MCP servers
    MCPServer1 -.->|Odoo RPC| Odoo1
    MCPServer2 -.->|Odoo RPC| Odoo2
    MCPServer3 -.->|Odoo RPC| Odoo3
    Claude[Claude Desktop] -.->|MCP Protocol| MCPServer1
    Claude -.->|MCP Protocol| MCPServer2
    Claude -.->|MCP Protocol| MCPServer3

    %% Monitoring
    Odoo1 -.->|Metrics| Prometheus
    Odoo2 -.->|Metrics| Prometheus
    Odoo3 -.->|Metrics| Prometheus
    Prometheus --> Grafana
    Odoo1 -.->|Errors| Sentry
    Odoo2 -.->|Errors| Sentry
    Odoo3 -.->|Errors| Sentry

    classDef frontend fill:#e1f5ff,stroke:#01579b,stroke-width:2px
    classDef backend fill:#e8f5e9,stroke:#1b5e20,stroke-width:2px
    classDef database fill:#fff9c4,stroke:#f57f17,stroke-width:2px
    classDef external fill:#ffebee,stroke:#b71c1c,stroke-width:1px,stroke-dasharray: 5 5
    classDef monitoring fill:#f3e5f5,stroke:#4a148c,stroke-width:2px

    class Users,CDN,LB frontend
    class Odoo1,Odoo2,Odoo3,Worker1,Worker2,Cron backend
    class PGPrimary,PGReplica1,PGReplica2,ChromaDB,RedisCache database
    class ClaudeAPI,OpenAIAPI,GoogleAPI,MCPServer1,MCPServer2,MCPServer3,Claude external
    class Prometheus,Grafana,Sentry monitoring
```

---

## File Permission System (ai.access.gate)

```mermaid
---
title: AI Access Gate - File Permission Flow (2025-12-17)
---

sequenceDiagram
    actor User
    participant Chat as Chat Interface
    participant Brain as ai_brain.py
    participant Gate as ai.access.gate
    participant Tools as SAM Tools
    participant FileSystem as Local Files

    User->>Chat: What is in D:/MyFolder?
    Chat->>Brain: send_message_streaming()
    Brain->>Brain: Detect file keyword → Load tools

    Brain->>Gate: check_path_access(path, user_id)

    alt Path Already Approved
        Gate-->>Brain: {allowed: true, approved_path: "D:\MyFolder/**"}
        Brain->>Tools: Execute list_directory
        Tools->>FileSystem: Read directory
        FileSystem-->>Tools: File listing
        Tools-->>Brain: Tool result
        Brain-->>Chat: Stream response with file list
    else Path Not Approved
        Gate->>Gate: Create pending permission
        Gate-->>Brain: {needs_approval: true, permission_request: {...}}
        Brain-->>Chat: permission_required event
        Chat->>User: Show permission popup
        User->>Chat: Click "Allow All in Folder"
        Chat->>Gate: action_approve_recursive()
        Gate->>Gate: Save path/** with state=approved_recursive
        Gate-->>Chat: {success: true}
        Note over Chat,Brain: User resends message or continues
    end
```

**Key Components:**

```mermaid
---
title: ai.access.gate Model Structure
---

classDiagram
    class AIAccessGate {
        +Many2one user_id
        +Char path
        +Selection state
        +Datetime approved_at
        +Datetime denied_at
        +check_path_access(path, user_id)
        +action_approve()
        +action_approve_recursive()
        +action_deny()
        +get_approved_paths(user_id)
        -_find_approved_path(path, user_id)
        -_normalize_path(path)
    }

    class State {
        <<enumeration>>
        pending
        approved
        approved_recursive
        denied
        expired
    }

    AIAccessGate --> State : state

    note for AIAccessGate "Uses sudo() throughout to avoid\nOdoo permission check recursion"
```

**Permission Matching Logic:**
- Exact match: `D:\MyFolder` matches `D:\MyFolder`
- Recursive match: `D:\MyFolder\sub\file.txt` matches `D:\MyFolder/**`
- Wildcard match: Uses `fnmatch` for pattern matching

---

## Agent System Architecture (2025-12-17)

```mermaid
---
title: Agent Selection and Behavior Flow
---

flowchart TB
    subgraph "Frontend (sam_chat_vanilla_v2.js)"
        AgentSelector[Agent Selector Dropdown]
        ChatInput[Chat Input]
    end

    subgraph "Controller (sam_ai_chat_controller.py)"
        GetAgent[Load agent_id from conversation]
        PassAgent[Pass agent_id to brain]
    end

    subgraph "Brain (ai_brain.py)"
        LoadAgent[Load ai.agent.registry record]
        BuildPrompt[_build_system_prompt]
        LoadTools[Load tools]
    end

    subgraph "Agent Components"
        AgentPrompt[Agent System Prompt]
        AgentKnowledge[Agent Knowledge Base]
        AgentTools[Agent Tool Config]
    end

    subgraph "Output"
        CustomBehavior[Agent-Specific AI Response]
    end

    AgentSelector -->|Select "Sales"| ChatInput
    ChatInput -->|conversation_id| GetAgent
    GetAgent -->|agent_id| PassAgent
    PassAgent -->|agent_id| LoadAgent

    LoadAgent --> BuildPrompt
    LoadAgent --> LoadTools

    BuildPrompt --> AgentPrompt
    BuildPrompt --> AgentKnowledge
    LoadTools --> AgentTools

    AgentPrompt --> CustomBehavior
    AgentKnowledge --> CustomBehavior
    AgentTools --> CustomBehavior

    classDef frontend fill:#e1f5ff,stroke:#01579b,stroke-width:2px
    classDef controller fill:#fff9c4,stroke:#f57f17,stroke-width:2px
    classDef brain fill:#e8f5e9,stroke:#1b5e20,stroke-width:2px
    classDef agent fill:#f3e5f5,stroke:#4a148c,stroke-width:2px

    class AgentSelector,ChatInput frontend
    class GetAgent,PassAgent controller
    class LoadAgent,BuildPrompt,LoadTools brain
    class AgentPrompt,AgentKnowledge,AgentTools,CustomBehavior agent
```

**Agent Registry Model:**

```mermaid
---
title: ai.agent.registry Structure
---

classDiagram
    class AIAgentRegistry {
        +Char name
        +Char display_name
        +Text description
        +Selection archetype
        +Selection category
        +Char slash_command
        +Char color
        +Char model_name
        +Text tools (JSON)
        +Text capabilities (JSON)
        +Text system_prompt
        +One2many knowledge_ids
        +get_relevant_knowledge(query, max_chunks)
    }

    class AIAgentKnowledge {
        +Many2one agent_id
        +Char name
        +Text content
        +Selection content_type
        +Char source_file
        +Integer sequence
    }

    class Archetype {
        <<enumeration>>
        advisor
        implementer
        gatekeeper
        automator
        enforcer
    }

    AIAgentRegistry "1" --> "*" AIAgentKnowledge : knowledge_ids
    AIAgentRegistry --> Archetype : archetype
```

**What Changes Per Agent:**

| Component | User-Wide | Agent-Specific |
|-----------|-----------|----------------|
| File Access Permissions | ✅ Shared via ai.access.gate | |
| System Prompt | | ✅ agent.system_prompt |
| Knowledge Base | | ✅ agent.knowledge_ids |
| Tool Configuration | ✅ Base tools (read/write/list) | Future: Additional specialized tools |
| AI Model | | ✅ agent.model_name (optional) |

---

## Tool Execution Flow (2025-12-17)

```mermaid
---
title: Tool Execution with Permission Checking
---

sequenceDiagram
    participant Brain as ai_brain.py
    participant OpenAI as OpenAI API
    participant Gate as ai.access.gate
    participant Tools as Tool Executor
    participant FS as File System

    Brain->>OpenAI: Chat request with tools
    OpenAI-->>Brain: tool_use: list_directory(path)

    Brain->>Brain: _execute_tool(list_directory, {path})

    Brain->>Gate: check_path_access(path)

    alt Permission Granted
        Gate-->>Brain: {allowed: true}
        Brain->>Tools: Execute list_directory
        Tools->>FS: os.listdir(path)
        FS-->>Tools: [files...]
        Tools-->>Brain: Tool result JSON
        Brain->>OpenAI: Continue with tool result
        OpenAI-->>Brain: Final response
    else Permission Needed
        Gate-->>Brain: {needs_approval: true}
        Brain-->>Brain: Yield permission_required event
        Note over Brain: Wait for user approval
    end
```

**OpenAI vs Anthropic Tool Format:**

```mermaid
---
title: Provider-Specific Tool Message Formats
---

flowchart LR
    subgraph "Anthropic Format"
        A1[role: assistant<br/>content: tool_use blocks]
        A2[role: user<br/>content: tool_result blocks]
        A1 --> A2
    end

    subgraph "OpenAI Format"
        O1[role: assistant<br/>content: null<br/>tool_calls: array]
        O2[role: tool<br/>tool_call_id: xxx<br/>content: result]
        O1 --> O2
    end

    Detect{api_format?}
    Detect -->|anthropic| A1
    Detect -->|openai| O1
```

---

## Streaming Architecture (SSE)

```mermaid
---
title: SSE Streaming with Transaction Management
---

sequenceDiagram
    participant Browser
    participant Controller as Controller
    participant Cursor as DB Cursor
    participant Brain as Brain
    participant API as AI API

    Browser->>Controller: POST /sam_ai/chat/send_streaming
    Controller->>Controller: Create SSE response

    Controller->>Cursor: with registry.cursor() as cr
    activate Cursor

    Cursor->>Brain: send_message_streaming()
    Brain->>Brain: Load profile, conversation, agent
    Brain->>Brain: Build system prompt

    Note over Brain,Cursor: CRITICAL: Commit before HTTP call
    Brain->>Cursor: env.cr.commit()

    Brain->>API: HTTP request (streaming)

    loop For each chunk
        API-->>Brain: SSE chunk
        Brain-->>Controller: yield {type: chunk}
        Controller-->>Browser: event: chunk
    end

    Brain-->>Controller: yield {type: done}
    Controller->>Cursor: cr.commit()
    deactivate Cursor
    Controller-->>Browser: event: done
```

**Key Fix (2025-12-17):** Added `self.env.cr.commit()` before making HTTP calls to prevent "idle in transaction" deadlocks where the database transaction stayed open while waiting for API responses.

---

**Last Updated:** December 17, 2025
**Module:** ai_sam (UI Layer)
**Version:** 1.0.0

**Recent Updates (2025-12-17):**
- Added ai.access.gate file permission system
- Integrated agent system (custom prompts, knowledge, tools)
- Fixed OpenAI tool format handling
- Fixed transaction deadlock in streaming

These diagrams can be rendered in:
- GitHub/GitLab (automatic Mermaid rendering)
- VS Code (Mermaid Preview extension)
- Online: https://mermaid.live
