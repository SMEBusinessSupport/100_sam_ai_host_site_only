# Api Documentation

**Original file:** `API_DOCUMENTATION.yaml`
**Type:** YAML

---

```yaml
openapi: 3.0.3
info:
  title: SAM AI Base API
  description: |
    Complete API documentation for SAM AI Base module (ai_sam_base).

    SAM AI is an AI assistant with perfect memory built into Odoo 18, featuring:
    - Multi-user conversation management with per-user memory
    - Multi-provider API orchestration (Claude, OpenAI, Google, Azure)
    - Context intelligence (SAM knows where you are in Odoo)
    - Cost optimization and budget management
    - Agent ecosystem for specialized tasks
    - Canvas platform for visual workflows

    **Authentication:** All endpoints require Odoo session authentication (`auth='user'`).

    **Base URL:** `https://your-odoo-instance.com`

    **Content Type:** All endpoints use `type='json'` (Odoo JSON-RPC format).
  version: 1.0.0
  contact:
    name: SAM AI Support
    url: https://samai.com
    email: support@samai.com
  license:
    name: LGPL-3
    url: https://www.gnu.org/licenses/lgpl-3.0.html

servers:
  - url: https://your-odoo-instance.com
    description: Production server
  - url: http://localhost:8069
    description: Local development server

tags:
  - name: Chat
    description: Main chat interface and messaging
  - name: Voice
    description: Voice transcription and audio processing
  - name: Conversations
    description: Conversation management and history
  - name: Context
    description: Context detection and intelligence
  - name: Modes
    description: AI modes and permissions
  - name: Agents
    description: Agent management and execution
  - name: Canvas
    description: Canvas platform and artifacts
  - name: Environment
    description: Environment detection and configuration
  - name: Menu
    description: Menu and module intelligence
  - name: Knowledge
    description: Knowledge extraction and training
  - name: Sessions
    description: Session persistence and management
  - name: File Permissions
    description: File access control
  - name: OAuth
    description: OAuth 2.0 authentication flows
  - name: Vendor Registry
    description: Vendor registry management
  - name: Services
    description: Service population and templates
  - name: Developer Mode
    description: Developer tools and QA integration
  - name: MCP
    description: MCP server downloads and configuration
  - name: Memory
    description: Memory graph visualization and diagnostics

paths:
  # ========================================================================
  # CHAT CONTROLLER (18 endpoints)
  # ========================================================================

  /sam_ai/chat/send:
    post:
      tags: [Chat]
      summary: Send message to SAM AI
      description: |
        Send a message to SAM AI and receive a response.

        - Creates or continues a conversation
        - Detects context from `context_data`
        - Tracks token usage and costs
        - Respects user's memory permissions
      operationId: sendMessage
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - message
              properties:
                message:
                  type: string
                  description: User's message to SAM
                  example: "Help me create a sales order"
                conversation_id:
                  type: integer
                  description: Existing conversation ID (optional)
                  example: 42
                session_id:
                  type: integer
                  description: Alias for conversation_id (frontend compatibility)
                  example: 42
                context_data:
                  type: object
                  description: Odoo context information
                  properties:
                    model:
                      type: string
                      example: "sale.order"
                    record_id:
                      type: integer
                      example: 123
                    node_id:
                      type: integer
                      description: Workflow node ID
                      example: 5
                environment:
                  type: object
                  description: Environment information
                  properties:
                    is_local:
                      type: boolean
                      example: false
                    active_mode:
                      type: string
                      example: "chat"
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                type: object
                properties:
                  success:
                    type: boolean
                    example: true
                  message:
                    type: string
                    description: SAM's response message
                    example: "I'll help you create a sales order. What customer is this for?"
                  conversation_id:
                    type: integer
                    example: 42
                  context_detected:
                    type: object
                    description: Detected context information
                    properties:
                      model:
                        type: string
                        example: "sale.order"
                      menu_name:
                        type: string
                        example: "Sales"
        '400':
          description: Bad request (missing required parameters)
        '500':
          description: Server error (API provider failure, etc.)

  /sam_ai/chat/send_streaming:
    post:
      tags: [Chat]
      summary: Send message with streaming response
      description: |
        Send a message and receive a streaming response (Server-Sent Events).

        Use this for long responses to show progress to users.
      operationId: sendMessageStreaming
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - message
              properties:
                message:
                  type: string
                  example: "Explain how the sales order workflow works"
                conversation_id:
                  type: integer
                  example: 42
                context_data:
                  type: object
                  properties:
                    model:
                      type: string
                      example: "sale.order"
      responses:
        '200':
          description: Streaming response (SSE)
          content:
            text/event-stream:
              schema:
                type: string
                description: Server-Sent Events stream
                example: |
                  data: {"type": "start"}
                  data: {"type": "content", "text": "The sales order workflow..."}
                  data: {"type": "content", "text": " begins with..."}
                  data: {"type": "end"}

  /sam_ai/voice/transcribe:
    post:
      tags: [Voice]
      summary: Transcribe voice to text
      description: |
        Transcribe audio to text using Whisper API.

        Supports multiple audio formats (mp3, wav, m4a, etc.).
      operationId: transcribeVoice
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - audio_data
                - format
              properties:
                audio_data:
                  type: string
                  format: byte
                  description: Base64-encoded audio data
                format:
                  type: string
                  enum: [mp3, wav, m4a, webm]
                  example: mp3
      responses:
        '200':
          description: Transcription successful
          content:
            application/json:
              schema:
                type: object
                properties:
                  success:
                    type: boolean
                    example: true
                  transcription:
                    type: string
                    example: "Create a new sales order for Acme Corp"
        '400':
          description: Invalid audio format or data

  /sam_ai/voice/check_provider:
    post:
      tags: [Voice]
      summary: Check voice provider availability
      description: Check if a voice transcription provider is configured and available.
      operationId: checkVoiceProvider
      responses:
        '200':
          description: Provider status
          content:
            application/json:
              schema:
                type: object
                properties:
                  available:
                    type: boolean
                    example: true
                  provider:
                    type: string
                    example: "openai"
                  model:
                    type: string
                    example: "whisper-1"

  /sam_ai/chat/conversations:
    post:
      tags: [Conversations]
      summary: Get user's conversation list
      description: |
        Get all conversations for the current user.

        Supports pagination via `limit` and `offset`.
      operationId: getUserConversations
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                limit:
                  type: integer
                  default: 50
                  example: 20
                offset:
                  type: integer
                  default: 0
                  example: 0
      responses:
        '200':
          description: List of conversations
          content:
            application/json:
              schema:
                type: object
                properties:
                  success:
                    type: boolean
                    example: true
                  conversations:
                    type: array
                    items:
                      type: object
                      properties:
                        id:
                          type: integer
                          example: 42
                        name:
                          type: string
                          example: "Sales Order Discussion"
                        last_message:
                          type: string
                          example: "Thank you for the help!"
                        created_date:
                          type: string
                          format: date-time
                          example: "2025-12-10T14:30:00Z"
                        message_count:
                          type: integer
                          example: 15

  /sam_ai/chat/new:
    post:
      tags: [Conversations]
      summary: Create new conversation
      description: Create a new conversation thread.
      operationId: createConversation
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                title:
                  type: string
                  example: "Invoice Questions"
                context_model:
                  type: string
                  example: "account.move"
                context_id:
                  type: integer
                  example: 456
      responses:
        '200':
          description: Conversation created
          content:
            application/json:
              schema:
                type: object
                properties:
                  success:
                    type: boolean
                    example: true
                  conversation_id:
                    type: integer
                    example: 43

  /sam_ai/chat/history:
    post:
      tags: [Conversations]
      summary: Get conversation history
      description: Get all messages in a conversation thread.
      operationId: getConversationHistory
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - conversation_id
              properties:
                conversation_id:
                  type: integer
                  example: 42
      responses:
        '200':
          description: Conversation messages
          content:
            application/json:
              schema:
                type: object
                properties:
                  success:
                    type: boolean
                    example: true
                  messages:
                    type: array
                    items:
                      type: object
                      properties:
                        role:
                          type: string
                          enum: [user, assistant]
                          example: user
                        content:
                          type: string
                          example: "How do I create a sales order?"
                        timestamp:
                          type: string
                          format: date-time
                          example: "2025-12-10T14:30:00Z"

  /sam_ai/chat/health:
    post:
      tags: [Chat]
      summary: Health check endpoint
      description: Check if the SAM AI chat service is healthy and responsive.
      operationId: healthCheck
      responses:
        '200':
          description: Service is healthy
          content:
            application/json:
              schema:
                type: object
                properties:
                  status:
                    type: string
                    example: "healthy"
                  timestamp:
                    type: string
                    format: date-time
                    example: "2025-12-10T14:30:00Z"

  /sam/user/set_mode:
    post:
      tags: [Modes]
      summary: Set user mode
      description: |
        Set the active AI mode for the user (chat, canvas, developer, etc.).

        Each mode has different capabilities and context.
      operationId: setUserMode
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - mode
              properties:
                mode:
                  type: string
                  enum: [chat, canvas, developer, code]
                  example: developer
      responses:
        '200':
          description: Mode set successfully
          content:
            application/json:
              schema:
                type: object
                properties:
                  success:
                    type: boolean
                    example: true
                  mode:
                    type: string
                    example: developer

  /sam/permission_response:
    post:
      tags: [Modes]
      summary: Handle permission responses
      description: Handle user's response to a permission request (file access, memory save, etc.).
      operationId: handlePermissionResponse
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - permission_type
                - response
              properties:
                permission_type:
                  type: string
                  enum: [file_access, memory_save, code_execution]
                  example: memory_save
                response:
                  type: string
                  enum: [yes, no, always]
                  example: yes
                context:
                  type: object
                  description: Additional context for the permission
      responses:
        '200':
          description: Permission response recorded
          content:
            application/json:
              schema:
                type: object
                properties:
                  success:
                    type: boolean
                    example: true

  /sam/modes/get_available:
    post:
      tags: [Modes]
      summary: Get available modes
      description: Get all available AI modes for the current user.
      operationId: getAvailableModes
      responses:
        '200':
          description: List of available modes
          content:
            application/json:
              schema:
                type: object
                properties:
                  success:
                    type: boolean
                    example: true
                  modes:
                    type: array
                    items:
                      type: object
                      properties:
                        name:
                          type: string
                          example: developer
                        display_name:
                          type: string
                          example: "Developer Mode"
                        description:
                          type: string
                          example: "Code assistance with QA integration"

  /sam_ai/context/parse:
    post:
      tags: [Context]
      summary: Parse context from URL
      description: Parse Odoo context from current URL path.
      operationId: parseContext
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - url
              properties:
                url:
                  type: string
                  example: "/web#model=sale.order&id=123"
      responses:
        '200':
          description: Parsed context
          content:
            application/json:
              schema:
                type: object
                properties:
                  success:
                    type: boolean
                    example: true
                  context:
                    type: object
                    properties:
                      model:
                        type: string
                        example: "sale.order"
                      record_id:
                        type: integer
                        example: 123
                      menu_name:
                        type: string
                        example: "Sales Orders"

  /sam_ai/context/handle_choice:
    post:
      tags: [Context]
      summary: Handle context shift choice
      description: |
        Handle user's choice when context shift is detected.

        When SAM detects user moved from one Odoo area to another, ask if conversation should follow.
      operationId: handleContextChoice
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - choice
              properties:
                choice:
                  type: string
                  enum: [follow, stay, new_conversation]
                  example: follow
                conversation_id:
                  type: integer
                  example: 42
      responses:
        '200':
          description: Choice handled
          content:
            application/json:
              schema:
                type: object
                properties:
                  success:
                    type: boolean
                    example: true

  /sam/agent/scan_directory:
    post:
      tags: [Agents]
      summary: Scan agent directory
      description: Scan directory for agent definition files and load them into registry.
      operationId: scanAgentDirectory
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - directory_path
              properties:
                directory_path:
                  type: string
                  example: "C:/Working With AI/agents"
      responses:
        '200':
          description: Agents scanned and loaded
          content:
            application/json:
              schema:
                type: object
                properties:
                  success:
                    type: boolean
                    example: true
                  agents_found:
                    type: integer
                    example: 5
                  agents_loaded:
                    type: integer
                    example: 5

  /sam/agent/create_from_config:
    post:
      tags: [Agents]
      summary: Create agent from config
      description: Create an AI agent definition from a configuration file.
      operationId: createAgentFromConfig
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - config
              properties:
                config:
                  type: object
                  description: Agent configuration
                  properties:
                    name:
                      type: string
                      example: "Custom QA Agent"
                    technical_name:
                      type: string
                      example: "custom_qa"
                    system_prompt:
                      type: string
                      example: "You are a QA agent specializing in..."
                    capabilities:
                      type: array
                      items:
                        type: string
                      example: ["code_review", "test_generation"]
      responses:
        '200':
          description: Agent created
          content:
            application/json:
              schema:
                type: object
                properties:
                  success:
                    type: boolean
                    example: true
                  agent_id:
                    type: integer
                    example: 10

  /ai/workflow/generate:
    post:
      tags: [Agents]
      summary: Generate workflow from description
      description: Generate an N8N workflow from natural language description.
      operationId: generateWorkflow
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - description
              properties:
                description:
                  type: string
                  example: "When a sale order is confirmed, send an email to the customer and create a task in project management"
      responses:
        '200':
          description: Workflow generated
          content:
            application/json:
              schema:
                type: object
                properties:
                  success:
                    type: boolean
                    example: true
                  workflow:
                    type: object
                    description: N8N workflow JSON

  # ========================================================================
  # CANVAS CONTROLLER (15 endpoints)
  # ========================================================================

  /sam/environment/config:
    get:
      tags: [Environment]
      summary: Get SAM environment config
      description: |
        Get SAM environment configuration for frontend.

        Detects installation type (local vs. SaaS) and available capabilities.
      operationId: getSamEnvironmentConfig
      responses:
        '200':
          description: Environment configuration
          content:
            application/json:
              schema:
                type: object
                properties:
                  success:
                    type: boolean
                    example: true
                  environment:
                    type: object
                    properties:
                      installation_type:
                        type: string
                        enum: [local, saas, enterprise]
                        example: local
                      sam_mode:
                        type: string
                        enum: [standard, developer, enterprise]
                        example: developer
                      capabilities:
                        type: object
                        properties:
                          filesystem:
                            type: boolean
                            example: true
                          git:
                            type: boolean
                            example: true
                          vscode:
                            type: boolean
                            example: true
                          python:
                            type: boolean
                            example: true
                          npm:
                            type: boolean
                            example: false
    post:
      tags: [Environment]
      summary: Get SAM environment config (POST)
      description: Same as GET but accepts POST requests for consistency.
      operationId: getSamEnvironmentConfigPost
      responses:
        '200':
          description: Environment configuration
          content:
            application/json:
              schema:
                $ref: '#/paths/~1sam~1environment~1config/get/responses/200/content/application~1json/schema'

  /canvas/platform/config:
    get:
      tags: [Canvas]
      summary: Get platform configuration
      description: Get canvas platform configuration.
      operationId: getCanvasPlatformConfig
      responses:
        '200':
          description: Platform configuration
          content:
            application/json:
              schema:
                type: object
                properties:
                  success:
                    type: boolean
                    example: true
                  platform:
                    type: object
                    properties:
                      name:
                        type: string
                        example: "Desktop"
                      type:
                        type: string
                        enum: [desktop, saas]
                        example: desktop
    post:
      tags: [Canvas]
      summary: Get platform configuration (POST)
      operationId: getCanvasPlatformConfigPost
      responses:
        '200':
          description: Platform configuration
          content:
            application/json:
              schema:
                $ref: '#/paths/~1canvas~1platform~1config/get/responses/200/content/application~1json/schema'

  /canvas/platform/list:
    get:
      tags: [Canvas]
      summary: List canvas platforms
      description: Get all available canvas platforms.
      operationId: listCanvasPlatforms
      responses:
        '200':
          description: List of platforms
          content:
            application/json:
              schema:
                type: object
                properties:
                  success:
                    type: boolean
                    example: true
                  platforms:
                    type: array
                    items:
                      type: object
                      properties:
                        id:
                          type: integer
                          example: 1
                        name:
                          type: string
                          example: "Desktop Platform"
                        type:
                          type: string
                          example: desktop
    post:
      tags: [Canvas]
      summary: List canvas platforms (POST)
      operationId: listCanvasPlatformsPost
      responses:
        '200':
          description: List of platforms
          content:
            application/json:
              schema:
                $ref: '#/paths/~1canvas~1platform~1list/get/responses/200/content/application~1json/schema'

  /canvas/open:
    get:
      tags: [Canvas]
      summary: Open canvas by ID
      description: Open a specific canvas by ID.
      operationId: openCanvas
      parameters:
        - name: canvas_id
          in: query
          required: true
          schema:
            type: integer
          example: 5
      responses:
        '200':
          description: Canvas data
          content:
            application/json:
              schema:
                type: object
                properties:
                  success:
                    type: boolean
                    example: true
                  canvas:
                    type: object
                    description: Canvas data

  /canvas/set_platform:
    get:
      tags: [Canvas]
      summary: Set canvas platform
      description: Set the active canvas platform for the user.
      operationId: setCanvasPlatform
      parameters:
        - name: platform_id
          in: query
          required: true
          schema:
            type: integer
          example: 1
      responses:
        '200':
          description: Platform set
          content:
            application/json:
              schema:
                type: object
                properties:
                  success:
                    type: boolean
                    example: true
    post:
      tags: [Canvas]
      summary: Set canvas platform (POST)
      operationId: setCanvasPlatformPost
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - platform_id
              properties:
                platform_id:
                  type: integer
                  example: 1
      responses:
        '200':
          description: Platform set
          content:
            application/json:
              schema:
                $ref: '#/paths/~1canvas~1set_platform/get/responses/200/content/application~1json/schema'

  /canvas/load_nodes:
    get:
      tags: [Canvas]
      summary: Load canvas nodes
      description: Load all nodes for a canvas.
      operationId: loadCanvasNodes
      parameters:
        - name: canvas_id
          in: query
          required: true
          schema:
            type: integer
          example: 5
      responses:
        '200':
          description: Canvas nodes
          content:
            application/json:
              schema:
                type: object
                properties:
                  success:
                    type: boolean
                    example: true
                  nodes:
                    type: array
                    items:
                      type: object
                      description: Node data
    post:
      tags: [Canvas]
      summary: Load canvas nodes (POST)
      operationId: loadCanvasNodesPost
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - canvas_id
              properties:
                canvas_id:
                  type: integer
                  example: 5
      responses:
        '200':
          description: Canvas nodes
          content:
            application/json:
              schema:
                $ref: '#/paths/~1canvas~1load_nodes/get/responses/200/content/application~1json/schema'

  /sam/create_conversation:
    get:
      tags: [Conversations]
      summary: Create conversation (Canvas)
      description: Create a new conversation from canvas interface.
      operationId: createConversationCanvas
      responses:
        '200':
          description: Conversation created
          content:
            application/json:
              schema:
                type: object
                properties:
                  success:
                    type: boolean
                    example: true
                  conversation_id:
                    type: integer
                    example: 44
    post:
      tags: [Conversations]
      summary: Create conversation (Canvas POST)
      operationId: createConversationCanvasPost
      responses:
        '200':
          description: Conversation created
          content:
            application/json:
              schema:
                $ref: '#/paths/~1sam~1create_conversation/get/responses/200/content/application~1json/schema'

  /sam/get_all_conversations:
    get:
      tags: [Conversations]
      summary: Get all conversations (Canvas)
      description: Get all conversations for current user from canvas interface.
      operationId: getAllConversationsCanvas
      responses:
        '200':
          description: List of conversations
          content:
            application/json:
              schema:
                type: object
                properties:
                  success:
                    type: boolean
                    example: true
                  conversations:
                    type: array
                    items:
                      type: object
    post:
      tags: [Conversations]
      summary: Get all conversations (Canvas POST)
      operationId: getAllConversationsCanvasPost
      responses:
        '200':
          description: List of conversations
          content:
            application/json:
              schema:
                $ref: '#/paths/~1sam~1get_all_conversations/get/responses/200/content/application~1json/schema'

  /sam/get_conversation_messages:
    get:
      tags: [Conversations]
      summary: Get conversation messages (Canvas)
      description: Get all messages in a conversation.
      operationId: getConversationMessagesCanvas
      parameters:
        - name: conversation_id
          in: query
          required: true
          schema:
            type: integer
          example: 42
      responses:
        '200':
          description: Conversation messages
          content:
            application/json:
              schema:
                type: object
                properties:
                  success:
                    type: boolean
                    example: true
                  messages:
                    type: array
                    items:
                      type: object
    post:
      tags: [Conversations]
      summary: Get conversation messages (Canvas POST)
      operationId: getConversationMessagesCanvasPost
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - conversation_id
              properties:
                conversation_id:
                  type: integer
                  example: 42
      responses:
        '200':
          description: Conversation messages
          content:
            application/json:
              schema:
                $ref: '#/paths/~1sam~1get_conversation_messages/get/responses/200/content/application~1json/schema'

  /sam/send_message:
    get:
      tags: [Chat]
      summary: Send message (Canvas)
      description: Send a message in a conversation from canvas interface.
      operationId: sendMessageCanvas
      parameters:
        - name: conversation_id
          in: query
          required: true
          schema:
            type: integer
          example: 42
        - name: message
          in: query
          required: true
          schema:
            type: string
          example: "Help me with this"
      responses:
        '200':
          description: Message sent
          content:
            application/json:
              schema:
                type: object
                properties:
                  success:
                    type: boolean
                    example: true
                  message:
                    type: string
    post:
      tags: [Chat]
      summary: Send message (Canvas POST)
      operationId: sendMessageCanvasPost
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - conversation_id
                - message
              properties:
                conversation_id:
                  type: integer
                  example: 42
                message:
                  type: string
                  example: "Help me with this"
      responses:
        '200':
          description: Message sent
          content:
            application/json:
              schema:
                $ref: '#/paths/~1sam~1send_message/get/responses/200/content/application~1json/schema'

  /sam/widget/open_sidebar:
    get:
      tags: [Canvas]
      summary: Open sidebar widget
      description: Open the SAM sidebar widget.
      operationId: openSidebar
      responses:
        '200':
          description: Sidebar opened
          content:
            application/json:
              schema:
                type: object
                properties:
                  success:
                    type: boolean
                    example: true
    post:
      tags: [Canvas]
      summary: Open sidebar widget (POST)
      operationId: openSidebarPost
      responses:
        '200':
          description: Sidebar opened
          content:
            application/json:
              schema:
                $ref: '#/paths/~1sam~1widget~1open_sidebar/get/responses/200/content/application~1json/schema'

  /sam/widget/close_sidebar:
    get:
      tags: [Canvas]
      summary: Close sidebar widget
      description: Close the SAM sidebar widget.
      operationId: closeSidebar
      responses:
        '200':
          description: Sidebar closed
          content:
            application/json:
              schema:
                type: object
                properties:
                  success:
                    type: boolean
                    example: true
    post:
      tags: [Canvas]
      summary: Close sidebar widget (POST)
      operationId: closeSidebarPost
      responses:
        '200':
          description: Sidebar closed
          content:
            application/json:
              schema:
                $ref: '#/paths/~1sam~1widget~1close_sidebar/get/responses/200/content/application~1json/schema'

  /sam/widget/toggle_artifacts:
    get:
      tags: [Canvas]
      summary: Toggle artifacts display
      description: Toggle visibility of canvas artifacts.
      operationId: toggleArtifacts
      responses:
        '200':
          description: Artifacts toggled
          content:
            application/json:
              schema:
                type: object
                properties:
                  success:
                    type: boolean
                    example: true
                  visible:
                    type: boolean
                    example: true
    post:
      tags: [Canvas]
      summary: Toggle artifacts display (POST)
      operationId: toggleArtifactsPost
      responses:
        '200':
          description: Artifacts toggled
          content:
            application/json:
              schema:
                $ref: '#/paths/~1sam~1widget~1toggle_artifacts/get/responses/200/content/application~1json/schema'

  /sam/artifact/save_version:
    get:
      tags: [Canvas]
      summary: Save artifact version
      description: Save a version of a canvas artifact.
      operationId: saveArtifactVersion
      parameters:
        - name: artifact_id
          in: query
          required: true
          schema:
            type: integer
          example: 10
      responses:
        '200':
          description: Version saved
          content:
            application/json:
              schema:
                type: object
                properties:
                  success:
                    type: boolean
                    example: true
                  version_id:
                    type: integer
                    example: 1
    post:
      tags: [Canvas]
      summary: Save artifact version (POST)
      operationId: saveArtifactVersionPost
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - artifact_id
              properties:
                artifact_id:
                  type: integer
                  example: 10
      responses:
        '200':
          description: Version saved
          content:
            application/json:
              schema:
                $ref: '#/paths/~1sam~1artifact~1save_version/get/responses/200/content/application~1json/schema'

  /sam/artifact/get_history:
    get:
      tags: [Canvas]
      summary: Get artifact history
      description: Get version history for a canvas artifact.
      operationId: getArtifactHistory
      parameters:
        - name: artifact_id
          in: query
          required: true
          schema:
            type: integer
          example: 10
      responses:
        '200':
          description: Artifact history
          content:
            application/json:
              schema:
                type: object
                properties:
                  success:
                    type: boolean
                    example: true
                  versions:
                    type: array
                    items:
                      type: object
    post:
      tags: [Canvas]
      summary: Get artifact history (POST)
      operationId: getArtifactHistoryPost
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - artifact_id
              properties:
                artifact_id:
                  type: integer
                  example: 10
      responses:
        '200':
          description: Artifact history
          content:
            application/json:
              schema:
                $ref: '#/paths/~1sam~1artifact~1get_history/get/responses/200/content/application~1json/schema'

  # ========================================================================
  # MENU CONTEXT CONTROLLER (7 endpoints)
  # ========================================================================

  /sam_ai/menu/get_modules:
    post:
      tags: [Menu]
      summary: Get available modules
      description: Get list of all installed Odoo modules.
      operationId: getModules
      responses:
        '200':
          description: List of modules
          content:
            application/json:
              schema:
                type: object
                properties:
                  success:
                    type: boolean
                    example: true
                  modules:
                    type: array
                    items:
                      type: object
                      properties:
                        name:
                          type: string
                          example: "sale"
                        display_name:
                          type: string
                          example: "Sales"
                        description:
                          type: string
                          example: "Manage sales orders and quotations"

  /sam_ai/menu/get_tree:
    post:
      tags: [Menu]
      summary: Get menu tree structure
      description: Get full Odoo menu tree structure.
      operationId: getMenuTree
      responses:
        '200':
          description: Menu tree
          content:
            application/json:
              schema:
                type: object
                properties:
                  success:
                    type: boolean
                    example: true
                  menu_tree:
                    type: array
                    items:
                      type: object
                      description: Menu item with children

  /sam_ai/module/ask:
    post:
      tags: [Menu]
      summary: Ask question about module
      description: Ask SAM a question about a specific Odoo module.
      operationId: askAboutModule
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - module_name
                - question
              properties:
                module_name:
                  type: string
                  example: "sale"
                question:
                  type: string
                  example: "How do I create a sales order?"
      responses:
        '200':
          description: Answer from SAM
          content:
            application/json:
              schema:
                type: object
                properties:
                  success:
                    type: boolean
                    example: true
                  answer:
                    type: string
                    example: "To create a sales order..."

  /sam_ai/module/train:
    post:
      tags: [Menu]
      summary: Train module intelligence
      description: Train SAM's knowledge about a specific module.
      operationId: trainModuleIntelligence
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - module_name
                - training_data
              properties:
                module_name:
                  type: string
                  example: "sale"
                training_data:
                  type: object
                  description: Module training data
      responses:
        '200':
          description: Training complete
          content:
            application/json:
              schema:
                type: object
                properties:
                  success:
                    type: boolean
                    example: true

  /sam_ai/module/save_training:
    post:
      tags: [Menu]
      summary: Save training data
      description: Save module training data to database.
      operationId: saveTrainingData
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - module_name
                - training_data
              properties:
                module_name:
                  type: string
                  example: "sale"
                training_data:
                  type: object
      responses:
        '200':
          description: Training data saved
          content:
            application/json:
              schema:
                type: object
                properties:
                  success:
                    type: boolean
                    example: true

  /sam_ai/knowledge/extract:
    post:
      tags: [Knowledge]
      summary: Extract knowledge from content
      description: Extract structured knowledge from documentation or content.
      operationId: extractKnowledge
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - content
              properties:
                content:
                  type: string
                  example: "The sales order workflow begins with..."
                content_type:
                  type: string
                  enum: [documentation, code, conversation]
                  example: documentation
      responses:
        '200':
          description: Extracted knowledge
          content:
            application/json:
              schema:
                type: object
                properties:
                  success:
                    type: boolean
                    example: true
                  knowledge:
                    type: object
                    description: Extracted knowledge structure

  /sam_ai/knowledge/save_extracted:
    post:
      tags: [Knowledge]
      summary: Save extracted knowledge
      description: Save extracted knowledge to the knowledge base.
      operationId: saveExtractedKnowledge
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - knowledge
              properties:
                knowledge:
                  type: object
                  description: Knowledge to save
                domain:
                  type: string
                  example: "Sales"
                subcategory:
                  type: string
                  example: "Sales Orders"
      responses:
        '200':
          description: Knowledge saved
          content:
            application/json:
              schema:
                type: object
                properties:
                  success:
                    type: boolean
                    example: true
                  knowledge_id:
                    type: integer
                    example: 25

  # ========================================================================
  # SESSION CONTROLLER (12 endpoints)
  # ========================================================================

  /sam/session/get_history:
    get:
      tags: [Sessions]
      summary: Get session history
      description: Get all saved sessions for current user.
      operationId: getSessionHistory
      responses:
        '200':
          description: Session history
          content:
            application/json:
              schema:
                type: object
                properties:
                  success:
                    type: boolean
                    example: true
                  sessions:
                    type: array
                    items:
                      type: object
                      properties:
                        id:
                          type: integer
                          example: 1
                        name:
                          type: string
                          example: "Development Session 2025-12-10"
                        created_date:
                          type: string
                          format: date-time
    post:
      tags: [Sessions]
      summary: Get session history (POST)
      operationId: getSessionHistoryPost
      responses:
        '200':
          description: Session history
          content:
            application/json:
              schema:
                $ref: '#/paths/~1sam~1session~1get_history/get/responses/200/content/application~1json/schema'

  /sam/session/load:
    get:
      tags: [Sessions]
      summary: Load session
      description: Load a saved session by ID.
      operationId: loadSession
      parameters:
        - name: session_id
          in: query
          required: true
          schema:
            type: integer
          example: 1
      responses:
        '200':
          description: Session loaded
          content:
            application/json:
              schema:
                type: object
                properties:
                  success:
                    type: boolean
                    example: true
                  session:
                    type: object
                    description: Session data
    post:
      tags: [Sessions]
      summary: Load session (POST)
      operationId: loadSessionPost
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - session_id
              properties:
                session_id:
                  type: integer
                  example: 1
      responses:
        '200':
          description: Session loaded
          content:
            application/json:
              schema:
                $ref: '#/paths/~1sam~1session~1load/get/responses/200/content/application~1json/schema'

  /sam/session/save:
    get:
      tags: [Sessions]
      summary: Save session
      description: Save current session state.
      operationId: saveSession
      parameters:
        - name: session_name
          in: query
          schema:
            type: string
          example: "My Dev Session"
      responses:
        '200':
          description: Session saved
          content:
            application/json:
              schema:
                type: object
                properties:
                  success:
                    type: boolean
                    example: true
                  session_id:
                    type: integer
                    example: 5
    post:
      tags: [Sessions]
      summary: Save session (POST)
      operationId: saveSessionPost
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                session_name:
                  type: string
                  example: "My Dev Session"
      responses:
        '200':
          description: Session saved
          content:
            application/json:
              schema:
                $ref: '#/paths/~1sam~1session~1save/get/responses/200/content/application~1json/schema'

  /sam/session/delete:
    get:
      tags: [Sessions]
      summary: Delete session
      description: Delete a saved session.
      operationId: deleteSession
      parameters:
        - name: session_id
          in: query
          required: true
          schema:
            type: integer
          example: 3
      responses:
        '200':
          description: Session deleted
          content:
            application/json:
              schema:
                type: object
                properties:
                  success:
                    type: boolean
                    example: true
    post:
      tags: [Sessions]
      summary: Delete session (POST)
      operationId: deleteSessionPost
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - session_id
              properties:
                session_id:
                  type: integer
                  example: 3
      responses:
        '200':
          description: Session deleted
          content:
            application/json:
              schema:
                $ref: '#/paths/~1sam~1session~1delete/get/responses/200/content/application~1json/schema'

  /sam/session/clear_all:
    get:
      tags: [Sessions]
      summary: Clear all sessions
      description: Delete all saved sessions for current user.
      operationId: clearAllSessions
      responses:
        '200':
          description: All sessions cleared
          content:
            application/json:
              schema:
                type: object
                properties:
                  success:
                    type: boolean
                    example: true
                  deleted_count:
                    type: integer
                    example: 5
    post:
      tags: [Sessions]
      summary: Clear all sessions (POST)
      operationId: clearAllSessionsPost
      responses:
        '200':
          description: All sessions cleared
          content:
            application/json:
              schema:
                $ref: '#/paths/~1sam~1session~1clear_all/get/responses/200/content/application~1json/schema'

  /sam/session/export:
    get:
      tags: [Sessions]
      summary: Export session data
      description: Export session data as JSON.
      operationId: exportSession
      parameters:
        - name: session_id
          in: query
          required: true
          schema:
            type: integer
          example: 1
      responses:
        '200':
          description: Session exported
          content:
            application/json:
              schema:
                type: object
                properties:
                  success:
                    type: boolean
                    example: true
                  export_data:
                    type: object
                    description: Session data
    post:
      tags: [Sessions]
      summary: Export session data (POST)
      operationId: exportSessionPost
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - session_id
              properties:
                session_id:
                  type: integer
                  example: 1
      responses:
        '200':
          description: Session exported
          content:
            application/json:
              schema:
                $ref: '#/paths/~1sam~1session~1export/get/responses/200/content/application~1json/schema'

  /sam/session/auto_save:
    get:
      tags: [Sessions]
      summary: Auto-save session
      description: Automatically save current session state.
      operationId: autoSaveSession
      responses:
        '200':
          description: Session auto-saved
          content:
            application/json:
              schema:
                type: object
                properties:
                  success:
                    type: boolean
                    example: true
    post:
      tags: [Sessions]
      summary: Auto-save session (POST)
      operationId: autoSaveSessionPost
      responses:
        '200':
          description: Session auto-saved
          content:
            application/json:
              schema:
                $ref: '#/paths/~1sam~1session~1auto_save/get/responses/200/content/application~1json/schema'

  /sam/knowledge/domains:
    get:
      tags: [Knowledge]
      summary: Get knowledge domains
      description: Get all knowledge domains.
      operationId: getKnowledgeDomains
      responses:
        '200':
          description: Knowledge domains
          content:
            application/json:
              schema:
                type: object
                properties:
                  success:
                    type: boolean
                    example: true
                  domains:
                    type: array
                    items:
                      type: object
                      properties:
                        id:
                          type: integer
                          example: 1
                        name:
                          type: string
                          example: "Sales"
    post:
      tags: [Knowledge]
      summary: Get knowledge domains (POST)
      operationId: getKnowledgeDomainsPost
      responses:
        '200':
          description: Knowledge domains
          content:
            application/json:
              schema:
                $ref: '#/paths/~1sam~1knowledge~1domains/get/responses/200/content/application~1json/schema'

  /sam/session/get_by_domain:
    get:
      tags: [Sessions]
      summary: Get sessions by domain
      description: Get all sessions for a specific knowledge domain.
      operationId: getSessionsByDomain
      parameters:
        - name: domain_id
          in: query
          required: true
          schema:
            type: integer
          example: 1
      responses:
        '200':
          description: Sessions by domain
          content:
            application/json:
              schema:
                type: object
                properties:
                  success:
                    type: boolean
                    example: true
                  sessions:
                    type: array
                    items:
                      type: object
    post:
      tags: [Sessions]
      summary: Get sessions by domain (POST)
      operationId: getSessionsByDomainPost
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - domain_id
              properties:
                domain_id:
                  type: integer
                  example: 1
      responses:
        '200':
          description: Sessions by domain
          content:
            application/json:
              schema:
                $ref: '#/paths/~1sam~1session~1get_by_domain/get/responses/200/content/application~1json/schema'

  /sam/settings/add_path:
    get:
      tags: [File Permissions]
      summary: Add file path to settings
      description: Add an approved file path to user settings.
      operationId: addFilePath
      parameters:
        - name: path
          in: query
          required: true
          schema:
            type: string
          example: "C:/Working With AI/ai_sam"
        - name: recursive
          in: query
          schema:
            type: boolean
          example: true
      responses:
        '200':
          description: Path added
          content:
            application/json:
              schema:
                type: object
                properties:
                  success:
                    type: boolean
                    example: true
    post:
      tags: [File Permissions]
      summary: Add file path to settings (POST)
      operationId: addFilePathPost
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - path
              properties:
                path:
                  type: string
                  example: "C:/Working With AI/ai_sam"
                recursive:
                  type: boolean
                  example: true
      responses:
        '200':
          description: Path added
          content:
            application/json:
              schema:
                $ref: '#/paths/~1sam~1settings~1add_path/get/responses/200/content/application~1json/schema'

  /sam/file/permission/allow:
    get:
      tags: [File Permissions]
      summary: Allow file permission
      description: Grant SAM permission to access a file or folder.
      operationId: allowFilePermission
      parameters:
        - name: path
          in: query
          required: true
          schema:
            type: string
          example: "C:/Projects/myproject"
        - name: recursive
          in: query
          schema:
            type: boolean
          example: false
      responses:
        '200':
          description: Permission granted
          content:
            application/json:
              schema:
                type: object
                properties:
                  success:
                    type: boolean
                    example: true
    post:
      tags: [File Permissions]
      summary: Allow file permission (POST)
      operationId: allowFilePermissionPost
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - path
              properties:
                path:
                  type: string
                  example: "C:/Projects/myproject"
                recursive:
                  type: boolean
                  example: false
      responses:
        '200':
          description: Permission granted
          content:
            application/json:
              schema:
                $ref: '#/paths/~1sam~1file~1permission~1allow/get/responses/200/content/application~1json/schema'

  /sam/file/permission/deny:
    get:
      tags: [File Permissions]
      summary: Deny file permission
      description: Deny SAM permission to access a file or folder.
      operationId: denyFilePermission
      parameters:
        - name: path
          in: query
          required: true
          schema:
            type: string
          example: "C:/Sensitive/data"
      responses:
        '200':
          description: Permission denied
          content:
            application/json:
              schema:
                type: object
                properties:
                  success:
                    type: boolean
                    example: true
    post:
      tags: [File Permissions]
      summary: Deny file permission (POST)
      operationId: denyFilePermissionPost
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - path
              properties:
                path:
                  type: string
                  example: "C:/Sensitive/data"
      responses:
        '200':
          description: Permission denied
          content:
            application/json:
              schema:
                $ref: '#/paths/~1sam~1file~1permission~1deny/get/responses/200/content/application~1json/schema'

  # ========================================================================
  # OAUTH CONTROLLER (3 endpoints)
  # ========================================================================

  /oauth/{vendor}/authorize:
    get:
      tags: [OAuth]
      summary: OAuth authorize endpoint
      description: Initiate OAuth 2.0 authorization flow for a vendor.
      operationId: oauthAuthorize
      parameters:
        - name: vendor
          in: path
          required: true
          schema:
            type: string
          example: anthropic
      responses:
        '302':
          description: Redirect to vendor OAuth page
        '400':
          description: Invalid vendor

  /oauth/{vendor}/callback:
    get:
      tags: [OAuth]
      summary: OAuth callback handler
      description: Handle OAuth 2.0 callback from vendor.
      operationId: oauthCallback
      parameters:
        - name: vendor
          in: path
          required: true
          schema:
            type: string
          example: anthropic
        - name: code
          in: query
          required: true
          schema:
            type: string
          description: Authorization code from vendor
        - name: state
          in: query
          schema:
            type: string
          description: State parameter for CSRF protection
      responses:
        '200':
          description: OAuth flow completed
          content:
            application/json:
              schema:
                type: object
                properties:
                  success:
                    type: boolean
                    example: true
                  access_token:
                    type: string
                    description: Access token (encrypted)
        '400':
          description: OAuth flow failed

  /oauth/refresh:
    post:
      tags: [OAuth]
      summary: Refresh OAuth token
      description: Refresh an expired OAuth access token.
      operationId: refreshOAuthToken
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - vendor
                - refresh_token
              properties:
                vendor:
                  type: string
                  example: anthropic
                refresh_token:
                  type: string
                  description: Refresh token
      responses:
        '200':
          description: Token refreshed
          content:
            application/json:
              schema:
                type: object
                properties:
                  success:
                    type: boolean
                    example: true
                  access_token:
                    type: string
                  expires_in:
                    type: integer
                    example: 3600

  # ========================================================================
  # VENDOR REGISTRY CONTROLLER (2 endpoints)
  # ========================================================================

  /vendor_registry/populate:
    post:
      tags: [Vendor Registry]
      summary: Manually populate vendor registry
      description: Manually trigger vendor registry population from node_metadata.json.
      operationId: populateVendorRegistry
      responses:
        '200':
          description: Registry populated
          content:
            application/json:
              schema:
                type: object
                properties:
                  success:
                    type: boolean
                    example: true
                  vendors_loaded:
                    type: integer
                    example: 25

  /vendor_registry/status:
    get:
      tags: [Vendor Registry]
      summary: Get vendor registry status
      description: Get status of vendor registry (how many vendors loaded).
      operationId: getVendorRegistryStatus
      responses:
        '200':
          description: Registry status
          content:
            application/json:
              schema:
                type: object
                properties:
                  success:
                    type: boolean
                    example: true
                  vendor_count:
                    type: integer
                    example: 25
                  last_updated:
                    type: string
                    format: date-time
    post:
      tags: [Vendor Registry]
      summary: Get vendor registry status (POST)
      operationId: getVendorRegistryStatusPost
      responses:
        '200':
          description: Registry status
          content:
            application/json:
              schema:
                $ref: '#/paths/~1vendor_registry~1status/get/responses/200/content/application~1json/schema'

  # ========================================================================
  # SERVICE POPULATOR CONTROLLER (1 endpoint)
  # ========================================================================

  /ai_sam/populate_services:
    post:
      tags: [Services]
      summary: Populate services from templates
      description: Populate API service providers from template data.
      operationId: populateServices
      responses:
        '200':
          description: Services populated
          content:
            application/json:
              schema:
                type: object
                properties:
                  success:
                    type: boolean
                    example: true
                  services_created:
                    type: integer
                    example: 10

  # ========================================================================
  # DEVELOPER MODE CONTROLLER (7 endpoints)
  # ========================================================================

  /sam/developer_mode/activate:
    post:
      tags: [Developer Mode]
      summary: Activate developer mode
      description: Activate developer mode for the current user.
      operationId: activateDeveloperMode
      responses:
        '200':
          description: Developer mode activated
          content:
            application/json:
              schema:
                type: object
                properties:
                  success:
                    type: boolean
                    example: true

  /sam/developer_mode/run_qa:
    post:
      tags: [Developer Mode]
      summary: Run QA checks
      description: Run QA Guardian checks on code.
      operationId: runQAChecks
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - file_path
              properties:
                file_path:
                  type: string
                  example: "C:/Projects/mymodule/models/mymodel.py"
      responses:
        '200':
          description: QA checks completed
          content:
            application/json:
              schema:
                type: object
                properties:
                  success:
                    type: boolean
                    example: true
                  issues_found:
                    type: integer
                    example: 3
                  issues:
                    type: array
                    items:
                      type: object

  /sam/developer_mode/session_start:
    post:
      tags: [Developer Mode]
      summary: Start developer session
      description: Start a new developer session.
      operationId: startDeveloperSession
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                session_name:
                  type: string
                  example: "Bug Fix Session"
      responses:
        '200':
          description: Session started
          content:
            application/json:
              schema:
                type: object
                properties:
                  success:
                    type: boolean
                    example: true
                  session_id:
                    type: integer
                    example: 10

  /sam/developer_mode/add_path:
    post:
      tags: [Developer Mode]
      summary: Add code path
      description: Add a code path to developer mode for SAM to access.
      operationId: addDeveloperPath
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - path
              properties:
                path:
                  type: string
                  example: "C:/Projects/myproject"
                recursive:
                  type: boolean
                  example: true
      responses:
        '200':
          description: Path added
          content:
            application/json:
              schema:
                type: object
                properties:
                  success:
                    type: boolean
                    example: true

  /sam/developer_mode/remove_path:
    post:
      tags: [Developer Mode]
      summary: Remove code path
      description: Remove a code path from developer mode.
      operationId: removeDeveloperPath
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - path
              properties:
                path:
                  type: string
                  example: "C:/Projects/oldproject"
      responses:
        '200':
          description: Path removed
          content:
            application/json:
              schema:
                type: object
                properties:
                  success:
                    type: boolean
                    example: true

  /sam/developer_mode/get_paths:
    post:
      tags: [Developer Mode]
      summary: Get code paths
      description: Get all code paths accessible in developer mode.
      operationId: getDeveloperPaths
      responses:
        '200':
          description: Code paths
          content:
            application/json:
              schema:
                type: object
                properties:
                  success:
                    type: boolean
                    example: true
                  paths:
                    type: array
                    items:
                      type: string
                    example:
                      - "C:/Projects/myproject/**"
                      - "C:/Working With AI/ai_sam/**"

  /sam/developer_mode/session_end:
    post:
      tags: [Developer Mode]
      summary: End developer session
      description: End the current developer session.
      operationId: endDeveloperSession
      responses:
        '200':
          description: Session ended
          content:
            application/json:
              schema:
                type: object
                properties:
                  success:
                    type: boolean
                    example: true

  # ========================================================================
  # MCP DOWNLOAD CONTROLLER (3 endpoints)
  # ========================================================================

  /mcp/download/script/{config_id}:
    get:
      tags: [MCP]
      summary: Download MCP server script
      description: Download the MCP server script file.
      operationId: downloadMCPScript
      parameters:
        - name: config_id
          in: path
          required: true
          schema:
            type: integer
          example: 1
      responses:
        '200':
          description: Script file
          content:
            application/octet-stream:
              schema:
                type: string
                format: binary

  /mcp/download/bundle/{config_id}:
    get:
      tags: [MCP]
      summary: Download MCPB bundle
      description: Download the complete MCP bundle (zip file).
      operationId: downloadMCPBundle
      parameters:
        - name: config_id
          in: path
          required: true
          schema:
            type: integer
          example: 1
      responses:
        '200':
          description: Bundle zip file
          content:
            application/zip:
              schema:
                type: string
                format: binary

  /mcp/download/manifest/{config_id}:
    get:
      tags: [MCP]
      summary: Download manifest
      description: Download the MCP manifest file.
      operationId: downloadMCPManifest
      parameters:
        - name: config_id
          in: path
          required: true
          schema:
            type: integer
          example: 1
      responses:
        '200':
          description: Manifest JSON file
          content:
            application/json:
              schema:
                type: object

  # ========================================================================
  # MEMORY GRAPH CONTROLLER (9 endpoints)
  # ========================================================================

  /memory/graph/view:
    get:
      tags: [Memory]
      summary: View memory graph visualization
      description: View memory graph visualization UI.
      operationId: viewMemoryGraph
      responses:
        '200':
          description: Memory graph HTML page
          content:
            text/html:
              schema:
                type: string

  /memory/graph/diagnostic:
    post:
      tags: [Memory]
      summary: Get memory diagnostic data
      description: Get diagnostic data about memory system health.
      operationId: getMemoryDiagnostic
      responses:
        '200':
          description: Diagnostic data
          content:
            application/json:
              schema:
                type: object
                properties:
                  success:
                    type: boolean
                    example: true
                  vector_db_status:
                    type: string
                    example: "healthy"
                  graph_db_status:
                    type: string
                    example: "healthy"
                  total_memories:
                    type: integer
                    example: 1523

  /memory/graph/test/checkpoint1:
    get:
      tags: [Memory]
      summary: Test checkpoint 1
      description: Test memory graph checkpoint 1 (basic connectivity).
      operationId: testCheckpoint1
      responses:
        '200':
          description: Test results
          content:
            application/json:
              schema:
                type: object
                properties:
                  success:
                    type: boolean
                    example: true

  /memory/graph/test/checkpoint2:
    get:
      tags: [Memory]
      summary: Test checkpoint 2
      description: Test memory graph checkpoint 2 (node creation).
      operationId: testCheckpoint2
      responses:
        '200':
          description: Test results
          content:
            application/json:
              schema:
                type: object
                properties:
                  success:
                    type: boolean
                    example: true

  /memory/graph/test/checkpoint3:
    get:
      tags: [Memory]
      summary: Test checkpoint 3
      description: Test memory graph checkpoint 3 (relationship creation).
      operationId: testCheckpoint3
      responses:
        '200':
          description: Test results
          content:
            application/json:
              schema:
                type: object
                properties:
                  success:
                    type: boolean
                    example: true

  /memory/graph/test/simple-line:
    post:
      tags: [Memory]
      summary: Test simple-line graph
      description: Test simple line graph rendering.
      operationId: testSimpleLine
      responses:
        '200':
          description: Graph data
          content:
            application/json:
              schema:
                type: object
                properties:
                  success:
                    type: boolean
                    example: true
                  graph_data:
                    type: object

  /memory/graph/test/hub-connection:
    post:
      tags: [Memory]
      summary: Test hub-connection graph
      description: Test hub-and-spoke graph rendering.
      operationId: testHubConnection
      responses:
        '200':
          description: Graph data
          content:
            application/json:
              schema:
                type: object
                properties:
                  success:
                    type: boolean
                    example: true
                  graph_data:
                    type: object

  /memory/graph/test/multi-hub:
    post:
      tags: [Memory]
      summary: Test multi-hub graph
      description: Test multi-hub graph rendering.
      operationId: testMultiHub
      responses:
        '200':
          description: Graph data
          content:
            application/json:
              schema:
                type: object
                properties:
                  success:
                    type: boolean
                    example: true
                  graph_data:
                    type: object

  /memory/graph/data:
    post:
      tags: [Memory]
      summary: Get graph data
      description: Get memory graph data for visualization.
      operationId: getMemoryGraphData
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                user_id:
                  type: integer
                  example: 1
                depth:
                  type: integer
                  description: How many relationship hops to include
                  example: 3
      responses:
        '200':
          description: Graph data
          content:
            application/json:
              schema:
                type: object
                properties:
                  success:
                    type: boolean
                    example: true
                  nodes:
                    type: array
                    items:
                      type: object
                  edges:
                    type: array
                    items:
                      type: object

components:
  securitySchemes:
    odooSessionAuth:
      type: apiKey
      in: cookie
      name: session_id
      description: Odoo session cookie authentication

security:
  - odooSessionAuth: []

```
