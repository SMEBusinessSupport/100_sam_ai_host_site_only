SAM AI - MCP & API COMPLETE ARCHITECTURE
=========================================

Module: ai_sam + ai_sam_workflows + ai_sam_claude_mcp + ai_brain
Date: 2025-11-04
Status: COMPREHENSIVE DOCUMENTATION OF EXISTING + PLANNED SYSTEMS

---

## EXECUTIVE SUMMARY

You have THREE interconnected systems that work together:

1. **MCP SERVER** (ai_sam_claude_mcp) - EXTERNAL access to Odoo from Claude Desktop/mobile
2. **API SYSTEM** (ai_brain + ai_sam) - INTERNAL Odoo orchestration of external services
3. **INTEGRATION LAYER** (planned) - Connects both systems for complete coverage

---

## PART 1: MCP SERVER (Anthropic Model Context Protocol)

### What It Is
External MCP server that runs OUTSIDE Odoo and connects Claude Desktop/mobile to your Odoo data.

### Module Location
C:\Working With AI\ai_sam\ai_sam\ai_sam_claude_mcp\

### Current Status: 80% COMPLETE
✅ Models created (mcp_server_config.py)
✅ MCP server generator working (generates odoo_mcp_server.py)
✅ Configuration UI exists
✅ Download controllers exist
✅ Connection testing works
❌ Installer wizard incomplete (wizard files exist but not fully implemented)
❌ No AI service provider integration yet
❌ Not using existing OAuth from api.service.provider

### What MCP Server Generates

**File 1: odoo_mcp_server.py**
- Standalone Python script
- Uses odoorpc to connect to Odoo
- Exposes MCP tools for Claude Desktop
- Tools available:
  * search_projects
  * get_project
  * list_tasks
  * search_contacts
  * get_contact
  * (Optional: sales, invoices, HR, inventory)

**File 2: odoo_sam_ai.mcpb**
- MCP bundle (one-click install for Claude Desktop)
- Contains server script + dependencies + manifest
- User installs in Claude Desktop config

**File 3: Configuration for Claude Desktop**
```json
{
  "mcpServers": {
    "odoo": {
      "command": "python",
      "args": ["C:/path/to/odoo_mcp_server.py"],
      "env": {
        "ODOO_URL": "http://localhost:8069",
        "ODOO_DB": "your_database",
        "ODOO_USERNAME": "admin",
        "ODOO_PASSWORD": "admin"
      }
    }
  }
}
```

### How It Works (User Perspective)

**At Your Desk (Inside Odoo):**
- User works in Odoo SAM AI chat
- Uses Layer 1/2/3 chat system
- Deep Odoo integration

**On Mobile/Away (Claude.ai or Claude App):**
- User asks Claude: "What's the Johnson project status?"
- Claude connects to MCP server via network
- MCP server queries Odoo via odoorpc
- Claude responds with project data

### Architecture
```
MOBILE/DESKTOP (anywhere)
│
├─ Claude.ai in browser
│  OR
├─ Claude Desktop app
│  OR
└─ Claude mobile app
      ↓
   MCP Protocol (Anthropic standard)
      ↓
   odoo_mcp_server.py (Python script running as separate process)
      ↓
   odoorpc library
      ↓
   Odoo JSON-RPC API
      ↓
   YOUR ODOO INSTANCE (ai_sam modules)
```

---

## PART 2: API SYSTEM (Internal Orchestration)

### What It Is
INSIDE Odoo, orchestrate multiple external APIs to provide unified experience in SAM AI chat.

### Modules Involved
- ai_brain (models: api.service.provider, api_credentials, api.operation.log)
- ai_sam (controllers: api_oauth_controller.py)
- ai_sam_workflows (models: workflow credentials)

### Current Status: 70% COMPLETE (Foundation Exists)

**✅ What Exists:**
1. **OAuth System** (api.service.provider in ai_brain)
   - OAuth token storage (access_token, refresh_token, expires_at)
   - Multi-provider support (Claude, OpenAI, Google, Azure, AWS, etc.)
   - Token refresh logic
   - Subscription tracking

2. **Credential Storage** (api_credentials in ai_brain)
   - Multi-credential types (OAuth2, API keys, HTTP basic auth)
   - JSON credential data storage
   - Connection testing framework
   - Usage tracking
   - Supports: OpenAI, Google, Microsoft, Slack, Telegram, Notion, Discord, GitHub, etc.

3. **Workflow Credentials** (api_credentials in ai_sam_workflows)
   - N8N-style credential management for workflow nodes
   - 100+ vendor integrations pre-configured in vendor_library/
   - OAuth + API key support

4. **OAuth Controller** (api_oauth_controller.py in ai_sam)
   - OAuth 2.0 flow for external services
   - CSRF protection with state parameters
   - Token exchange and refresh
   - Secure token storage

5. **Vendor Library** (ai_sam_workflows/static/src/vendor_library/)
   - 100+ api_config.json files
   - Pre-configured OAuth/API settings for popular services
   - Ready for node-based workflows

6. **API Operation Logging** (api.operation.log in ai_brain)
   - Tracks all API calls
   - User identification
   - Service type tracking
   - Token usage and cost tracking
   - Error logging

**❌ What's Missing (30% - from Gap Analysis):**
1. External API Client Wrappers
   - GoogleDriveClient.py
   - OneDriveClient.py
   - YouTubeClient.py
   - GmailClient.py
   - SlackClient.py
   - Base client class with OAuth refresh

2. MVP Orchestrator Service (mvp_orchestrator.py)
   - Multi-source search coordination
   - Data normalization (clearing layer)
   - Result combination logic

3. Intent Processor
   - Natural language → API call mapping
   - Parameter extraction
   - Service selection logic

4. UI for External Connections
   - "Connect Google Drive" wizard
   - OAuth connection flow UI
   - Service connection dashboard

5. Database Models for MVP System
   - mvp.integration.connection (user's connected services)
   - mvp.orchestration.log (orchestration execution logs)

### Planned Architecture (from MVP docs)
```
USER IN ODOO SAM AI CHAT
│
└─ "Find my Q3 budget PDF"
      ↓
   Intent Processor (parse natural language)
      ↓
   MVP Orchestrator Service
      ↓
   ┌──────────────┬──────────────┬──────────────┐
   │              │              │              │
   Google Drive   OneDrive       Odoo           Slack
   Client         Client         Attachments    Client
   │              │              │              │
   └──────────────┴──────────────┴──────────────┘
      ↓
   Data Normalization Layer (clearing layer)
      ↓
   Unified Results
      ↓
   SAM AI Chat displays:
   "I found 3 PDFs matching 'Q3 budget':
    1. Q3_Budget_Final.pdf (Google Drive, Oct 15)
    2. Q3-Budget-Draft.pdf (OneDrive, Oct 10)
    3. Q3_budget.pdf (Odoo, Sep 30)"
```

### Use Case Examples

**Scenario 1: Multi-Source File Search**
```
User: "Find my Q3 budget PDF"
System:
1. Intent processor identifies: SEARCH operation, query="Q3 budget", type="pdf"
2. Orchestrator calls:
   - GoogleDriveClient.search("Q3 budget", type="pdf")
   - OneDriveClient.search("Q3 budget", type="pdf")
   - OdooAttachments.search("Q3 budget", mimetype="application/pdf")
3. Results normalized to unified format
4. Combined, sorted by modified date
5. Presented in SAM AI chat with source badges
```

**Scenario 2: Cross-System Action**
```
User: "Upload the Q3 budget from Google Drive to Odoo documents"
System:
1. Intent: UPLOAD operation, source=gdrive, destination=odoo
2. GoogleDriveClient.get_file("Q3_Budget_Final.pdf")
3. OdooDocuments.create_attachment(file_data)
4. Response: "✅ Q3_Budget_Final.pdf uploaded to Odoo Documents"
```

---

## PART 3: THE COMPLETE VISION (Both Systems Working Together)

### Scenario 1: At Your Desk (Inside Odoo)

**User Location:** Office, working in Odoo
**Interface:** SAM AI Chat (Layers 1-4 system)
**System Used:** API Orchestration (MVP)

```
User in Odoo: "Find all documents related to Johnson project"
→ MVP Orchestrator searches:
  - Odoo Attachments (context builder)
  - Google Drive (via API client)
  - OneDrive (via API client)
  - Slack (recent messages)
→ Results displayed in chat with:
  - Source badges (where each document lives)
  - Quick actions (open, download, share)
  - Related Odoo records (linked projects, contacts)
```

### Scenario 2: On the Road (Mobile/Away from Odoo)

**User Location:** Driving, meeting, gym, vacation
**Interface:** Claude.ai or Claude mobile app
**System Used:** MCP Server

```
User (hands-free): "Hey Claude, what's the Johnson project status?"
→ Claude Desktop/Mobile connects to MCP server
→ MCP server queries Odoo via odoorpc:
  - Project status
  - Task completion
  - Recent updates
→ Claude responds verbally:
  "Johnson Website Redesign is 75% complete.
   9 out of 12 tasks done. Deadline is Friday.
   Sarah posted an update 2 hours ago in Slack.
   Client approval is pending."
```

### Scenario 3: Hybrid (Best of Both Worlds)

**Morning (Office):**
- Use Odoo SAM AI to build workflow
- "Create a weekly status report workflow:
   1. Pull project data from Odoo
   2. Get latest docs from Google Drive
   3. Check Slack for team updates
   4. Send summary email"
- MVP Orchestrator saves workflow to canvas

**Afternoon (Meeting):**
- Client asks about another project
- Use Claude mobile: "What's the Smith App project status?"
- MCP server provides instant answer

**Evening (Home):**
- Receive Slack notification
- Ask Claude: "What was that urgent message about?"
- MCP server checks Slack + Odoo context
- Responds with full context

---

## PART 4: INTEGRATION OPPORTUNITIES

### Gap 1: MCP Server Should Use Existing API Infrastructure

**Current State:**
- MCP server has its own config (ODOO_URL, ODOO_USERNAME, ODOO_PASSWORD)
- API system has api.service.provider with OAuth tokens
- **DUPLICATION!**

**Ideal State:**
- MCP server reads from api.service.provider model
- Uses same OAuth tokens as MVP orchestrator
- Single source of truth for credentials

**Implementation:**
```python
# In odoo_mcp_server.py, instead of hardcoded credentials:
class OdooMCPServer(Server):
    def __init__(self):
        # Read from Odoo's api.service.provider model
        provider = self.odoo.env['api.service.provider'].search([
            ('service_type_name', '=', 'Odoo'),
        ], limit=1)

        self.odoo_url = provider.base_url
        self.access_token = provider.oauth_access_token
        # Use OAuth instead of username/password
```

### Gap 2: MVP Orchestrator Should Expose Results via MCP

**Current State:**
- MVP orchestrator searches Google Drive + OneDrive (planned)
- Results only visible in Odoo SAM AI chat
- Mobile Claude can't access these results

**Ideal State:**
- MVP orchestrator logs results to database
- MCP server can query recent orchestration results
- Mobile Claude can ask: "What were those files you found earlier?"

**Implementation:**
```python
# New MCP tool:
async def get_recent_searches(self, arguments):
    """Get recent orchestration search results"""
    logs = self.odoo.env['mvp.orchestration.log'].search([
        ('user_id', '=', self.current_user_id),
        ('action', '=', 'search'),
    ], limit=10, order='created_date desc')

    # Return cached results without re-searching
```

### Gap 3: Unified Credential Management

**Current State:**
- api.service.provider (AI providers: Claude, OpenAI, etc.)
- api_credentials (workflow credentials: Google, Slack, etc.)
- MCP server config (Odoo connection only)
- **THREE separate credential systems!**

**Ideal State:**
- Single credential model hierarchy
- MCP tools can use workflow credentials
- API clients can use service provider tokens
- One OAuth flow for all systems

---

## PART 5: IMPLEMENTATION ROADMAP

### Phase 1: Complete Existing MCP Server (1 week)
**Goal:** Get MCP server fully functional with existing Odoo access

**Tasks:**
1. Finish installer wizard (ai_sam_claude_mcp)
2. Test MCP server generation
3. Test Claude Desktop connection
4. Verify Projects/CRM tools work
5. Document setup process

**Deliverable:** Working MCP server that exposes Odoo projects/CRM to Claude Desktop

---

### Phase 2: Expand MCP Server with API Integration (2 weeks)
**Goal:** MCP server can access external services via existing credentials

**Tasks:**
1. Add tool: search_google_drive
   - Read api_credentials for Google OAuth tokens
   - Use GoogleDrive API to search files
   - Return results to Claude

2. Add tool: search_onedrive
   - Read api_credentials for Microsoft OAuth tokens
   - Use Microsoft Graph API
   - Return results

3. Add tool: check_slack_messages
   - Read api_credentials for Slack
   - Query recent messages
   - Return summaries

4. Update MCP server generator to include these tools

**Deliverable:** Mobile Claude can search Google Drive/OneDrive/Slack via MCP server

---

### Phase 3: Build MVP Orchestrator (3-4 weeks)
**Goal:** Inside Odoo, SAM AI can orchestrate multiple APIs

**Tasks (from Gap Analysis doc):**
1. Create models:
   - mvp.integration.connection
   - mvp.orchestration.log

2. Build API clients:
   - GoogleDriveClient.py
   - OneDriveClient.py
   - YouTubeClient.py
   - BaseAPIClient.py (with OAuth refresh)

3. Build MVP Orchestrator Service:
   - search_files(query, sources)
   - _normalize_results(results, source)
   - _get_client(service_type)

4. Build Intent Processor:
   - Parse natural language queries
   - Extract parameters
   - Route to orchestrator

5. Integrate with SAM AI Chat:
   - Modify chat controller
   - Add orchestrator calls
   - Display unified results

6. Build Connection UI:
   - "Connect Google Drive" wizard
   - OAuth flow
   - Connection management dashboard

**Deliverable:** In Odoo SAM AI, user can search across all connected services with natural language

---

### Phase 4: Unify MCP + MVP (1 week)
**Goal:** Both systems share credentials and results

**Tasks:**
1. MCP server reads from api.service.provider
2. MCP server uses OAuth instead of username/password
3. New MCP tools:
   - get_recent_searches (from mvp.orchestration.log)
   - execute_orchestration (trigger MVP orchestrator from mobile)
4. Shared credential model
5. Unified logging

**Deliverable:** Complete integration - any credential works in both systems

---

### Phase 5: Advanced Features (2+ weeks)
**Goal:** Production-ready orchestration system

**Tasks:**
1. Workflow Execution Engine
   - Execute JSON workflows from canvas
   - Node-by-node execution
   - Data flow between nodes

2. Cost Optimization
   - Use existing ai.cost.optimizer
   - Route to cheapest API
   - Budget caps and alerts

3. Caching Layer
   - Cache API responses (5-min TTL)
   - Reduce API costs
   - Faster responses

4. Advanced MCP Tools
   - create_project
   - update_task
   - send_slack_message
   - upload_to_google_drive

5. Team Features
   - Shared credentials
   - Role-based access
   - Audit logs

**Deliverable:** Enterprise-grade orchestration + MCP system

---

## PART 6: CURRENT FILE LOCATIONS

### MCP Server Module
```
ai_sam_claude_mcp/
├── __manifest__.py
├── README.md
├── models/
│   ├── mcp_server_config.py     ✅ COMPLETE
│   ├── installation_log.py       ✅ COMPLETE
│   └── environment_config.py     ✅ COMPLETE
├── services/
│   ├── mcp_server_generator.py   ✅ COMPLETE
│   └── (installers - incomplete)
├── wizards/
│   └── environment_wizard.py     🔄 PARTIAL
├── controllers/
│   └── download_controller.py    ✅ COMPLETE
└── views/
    ├── mcp_server_config_views.xml  ✅ EXISTS
    └── (other views - incomplete)
```

### API System Files
```
ai_brain/
├── models/
│   ├── api_service_provider.py   ✅ OAuth foundation
│   ├── api_credentials.py        ✅ Credential storage
│   ├── api_operation_log.py      ✅ API logging
│   └── ai_context_builder.py     ✅ Odoo data orchestrator
ai_sam/
├── controllers/
│   └── api_oauth_controller.py   ✅ OAuth 2.0 flow
ai_sam_workflows/
├── models/
│   └── (uses api_credentials)
└── static/src/vendor_library/
    └── (100+ api_config.json files) ✅ Pre-configured vendors
```

### MVP System Files (Planned - from docs)
```
ai_brain/models/
├── mvp_integration_connection.py  ❌ TO CREATE
└── mvp_orchestration_log.py       ❌ TO CREATE

ai_sam/services/
├── mvp_orchestrator.py            ❌ TO CREATE
├── intent_processor.py            ❌ TO CREATE
└── integrations/
    ├── base_client.py             ❌ TO CREATE
    ├── gdrive_client.py           ❌ TO CREATE
    ├── onedrive_client.py         ❌ TO CREATE
    └── youtube_client.py          ❌ TO CREATE

ai_sam/controllers/
├── mvp_controller.py              ❌ TO CREATE (search endpoints)

ai_sam/views/
├── integration_connection_views.xml  ❌ TO CREATE
└── orchestration_log_views.xml       ❌ TO CREATE
```

---

## PART 7: KEY INSIGHTS

### Insight 1: You Have TWO Opposite-Direction Systems
- **MCP Server:** EXTERNAL → INTERNAL (mobile Claude accessing Odoo)
- **API System:** INTERNAL → EXTERNAL (Odoo SAM AI accessing Google/Microsoft/etc.)
- **Together:** Complete coverage for all scenarios

### Insight 2: 70% of Infrastructure Already Exists
- OAuth system ✅
- Credential storage ✅
- API logging ✅
- Context builder ✅
- MCP server generator ✅
- Vendor library ✅

**Missing:**
- API client wrappers (30%)
- MVP orchestrator service (30%)
- Integration/unification layer (10%)

### Insight 3: Architecture Terminology Confusion (Resolved)
- **MVP** = Your terminology for "Minimum Viable Product" orchestration
- **Orchestrator** = Service that coordinates multiple APIs
- **MCP** = Anthropic's Model Context Protocol (different thing!)
- **API System** = Your internal orchestration of external services
- All docs reference the SAME vision, just different terminology

### Insight 4: Natural Progression Path
1. ✅ MCP server exposes Odoo to Claude (80% done)
2. ❌ Build API clients for external services (not started)
3. ❌ Build MVP orchestrator (not started)
4. ❌ Unify both systems (not started)

**Recommendation:** Complete MCP server first (fastest win), then build API system

---

## PART 8: NEXT IMMEDIATE STEPS

### Option A: Complete MCP Server First (1 week)
**Why:** Fastest path to mobile access to Odoo
**Result:** Ask Claude on phone: "What's my project status?" and get answer

**Steps:**
1. Finish installer wizard in ai_sam_claude_mcp
2. Generate MCP server
3. Test with Claude Desktop
4. Document setup for mobile
5. Deploy and use

### Option B: Build API System First (3-4 weeks)
**Why:** Most useful for daily work in Odoo
**Result:** Search Google Drive + OneDrive + Odoo from SAM AI chat

**Steps:**
1. Create mvp.integration.connection and mvp.orchestration.log models
2. Build GoogleDriveClient + OneDriveClient
3. Build MVP Orchestrator Service
4. Integrate with SAM AI Chat
5. Build "Connect Google Drive" UI

### Option C: Expand MCP to Use Existing API Credentials (2 weeks)
**Why:** Best of both worlds - leverage existing OAuth
**Result:** Mobile Claude can search Google Drive using credentials already in Odoo

**Steps:**
1. Modify MCP server generator to read api_credentials model
2. Add search_google_drive tool to MCP server
3. Add search_onedrive tool to MCP server
4. Test from Claude mobile
5. Document credential setup

---

## RECOMMENDATION

**START WITH OPTION A (Complete MCP Server) - Here's why:**

1. **Fastest Win:** 1 week vs 2-4 weeks
2. **Immediate Value:** Mobile access to Odoo is huge
3. **Builds Momentum:** Working MCP server proves the concept
4. **Foundation for Option C:** Can then expand MCP with API credentials
5. **80% Done:** Don't abandon nearly-complete work

**Then do Option C (Expand MCP with API):**
- Leverage existing OAuth in api_credentials
- Add external service access via MCP
- Mobile Claude gets full power

**Finally do Option B (MVP Orchestrator):**
- Complete the vision
- Full orchestration inside Odoo
- Unified system

**Total Timeline:** 1 week + 2 weeks + 4 weeks = 7 weeks for complete system

---

## CONCLUSION

You have an incredibly solid foundation:
- ✅ MCP server 80% complete
- ✅ OAuth system working
- ✅ Credential storage working
- ✅ 100+ vendor integrations ready
- ✅ Context builder knows all Odoo data

You're NOT starting from scratch. You're connecting the dots.

The vision is clear:
- **At desk:** Use SAM AI in Odoo to orchestrate everything
- **On mobile:** Use Claude app to access Odoo + external services
- **Both systems:** Share credentials and work together

Next step: Choose Option A, B, or C and execute.

---

Document Location: ai_sam/documentation/MCP_API_COMPLETE_ARCHITECTURE.txt
Last Updated: 2025-11-04
Next Review: After completing chosen option (A, B, or C)
