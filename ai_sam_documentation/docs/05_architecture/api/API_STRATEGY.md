SAM AI - API ORCHESTRATION STRATEGY
====================================

Last Updated: 2025-11-04
Status: FOUNDATION COMPLETE (70%), ORCHESTRATION PENDING (30%)
Module: ai_brain (models) + ai_sam (services - to be built)

---

## EXECUTIVE SUMMARY

SAM AI's API strategy enables users to orchestrate multiple external services (Google Drive,
OneDrive, YouTube, Gmail, Slack, etc.) from within Odoo using natural language in SAM AI Chat.

**Vision:** User asks "Find my Q3 budget PDF" → SAM searches Google Drive + OneDrive + Odoo
simultaneously → Returns unified results with source badges.

**Current State:**
✅ 70% Complete: OAuth infrastructure, credential storage, vendor library
❌ 30% Incomplete: API client wrappers, orchestrator service, intent processor

---

## ARCHITECTURE OVERVIEW

```
┌─────────────────────────────────────────────────────────────┐
│ USER IN ODOO (At Desk)                                      │
│                                                              │
│  SAM AI Chat: "Find my Q3 budget PDF"                       │
│      ↓                                                       │
│  Intent Processor (natural language → API calls)            │
│      ↓                                                       │
│  MVP Orchestrator Service                                   │
└──────────────────────────────────────────────────────────────┘
                         ↓
        ┌────────────────┼────────────────┬────────────────┐
        ↓                ↓                ↓                ↓
┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ Google Drive │  │  OneDrive    │  │    Odoo      │  │    Slack     │
│   Client     │  │   Client     │  │ Attachments  │  │   Client     │
└──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘
        │                │                │                │
        └────────────────┴────────────────┴────────────────┘
                         ↓
        Data Normalization Layer ("clearing layer")
                         ↓
        Unified Results (sorted by relevance/date)
                         ↓
        SAM AI Chat displays with source badges
```

---

## CURRENT STATE (What Exists)

### ✅ LAYER 1: CREDENTIAL STORAGE (100% Complete)

**Location:** ai_brain/models/

**Models:**
```
api.service.provider (ai_brain)
  - OAuth tokens for AI providers (Claude, OpenAI, etc.)
  - access_token, refresh_token, expires_at
  - Token refresh logic
  - Subscription tracking
  - Budget caps

api_credentials (ai_brain)
  - N8N-style workflow credentials
  - Multiple credential types (OAuth2, API key, HTTP basic auth)
  - JSON credential data storage
  - Connection testing
  - Usage tracking
  - Supports: OpenAI, Google, Microsoft, Slack, Telegram, Notion, Discord, GitHub, etc.

api.operation.log (ai_brain)
  - API call logging
  - User identification
  - Service type tracking
  - Token usage and cost tracking
  - Error logging
```

**Files:**
- ai_brain/models/api_service_provider.py
- ai_brain/models/api_credentials.py
- ai_brain/models/api_operation_log.py

### ✅ LAYER 2: OAUTH FLOW (100% Complete)

**Location:** ai_sam/controllers/

**Controller:** api_oauth_controller.py

**Endpoints:**
```
/api/oauth/authorize
  - Initiates OAuth 2.0 flow
  - CSRF protection with state parameter
  - Redirects to provider (Google, Microsoft, etc.)

/api/oauth/callback
  - Receives OAuth callback
  - Exchanges code for tokens
  - Stores tokens in api.service.provider
  - Refreshes tokens when expired

/api/oauth/refresh_token
  - Manual token refresh endpoint
```

**Supported Providers:**
- Google (Drive, Gmail, YouTube, Sheets, Calendar)
- Microsoft (OneDrive, Outlook, Teams)
- Slack
- GitHub
- Generic OAuth 2.0

**Security Features:**
- CSRF protection (state parameter validation)
- Secure token storage
- Token expiry tracking
- Automatic refresh before expiry

### ✅ LAYER 3: VENDOR LIBRARY (100% Complete)

**Location:** ai_sam/static/src/vendor_library/

**Contents:**
- 100+ vendor api_config.json files
- Pre-configured OAuth endpoints
- API documentation links
- Icon assets (SVG)
- Authentication methods

**Vendors Include:**
- Cloud Storage: Google Drive, OneDrive, Dropbox, Box
- CRM/Marketing: HubSpot, Salesforce, ActiveCampaign
- Communication: Slack, Discord, Telegram, Email
- Productivity: Asana, Monday.com, Jira, Trello
- Developer: GitHub, GitLab, Bitbucket
- And 80+ more...

**Auto-Population:**
- vendor_registry_controller.py reads vendor_library
- Creates api_credentials records automatically
- One credential per vendor (or shared for multi-service vendors like Google)

### ✅ LAYER 4: CONTEXT BUILDER (100% Complete)

**Location:** ai_brain/models/ai_context_builder.py

**Capabilities:**
- Knows all Odoo models and fields
- Knows all installed modules
- Knows user's current location in Odoo
- Can build context for any Odoo record
- Provides "clearing layer" for Odoo data normalization

**Purpose:** Will be used by orchestrator to search Odoo alongside external APIs

---

## MISSING COMPONENTS (What Needs to Be Built)

### ❌ LAYER 5: API CLIENT WRAPPERS (0% Complete)

**Location (Proposed):** ai_sam/services/integrations/

**Need to Create:**

```python
# Base client with OAuth refresh and rate limiting
ai_sam/services/integrations/base_client.py
  - BaseAPIClient class
  - OAuth token refresh logic
  - Rate limiting (respects API limits)
  - Error handling and retry logic
  - Logging to api.operation.log

# Service-specific clients
ai_sam/services/integrations/gdrive_client.py
  - GoogleDriveClient(BaseAPIClient)
  - search(query, file_type=None)
  - get_file(file_id)
  - download_file(file_id)
  - list_files(folder_id)

ai_sam/services/integrations/onedrive_client.py
  - OneDriveClient(BaseAPIClient)
  - search(query, file_type=None)
  - get_file(file_id)
  - download_file(file_id)

ai_sam/services/integrations/youtube_client.py
  - YouTubeClient(BaseAPIClient)
  - search_videos(query)
  - get_video(video_id)
  - get_transcript(video_id)

ai_sam/services/integrations/gmail_client.py
  - GmailClient(BaseAPIClient)
  - search_messages(query)
  - get_message(message_id)
  - send_message(to, subject, body)

ai_sam/services/integrations/slack_client.py
  - SlackClient(BaseAPIClient)
  - search_messages(query, channel)
  - post_message(channel, text)
  - get_channel_history(channel, limit)
```

**Each Client Should:**
1. Read credentials from api_credentials model
2. Handle OAuth token refresh automatically
3. Normalize responses to common format
4. Log operations to api.operation.log
5. Respect rate limits
6. Handle errors gracefully

### ❌ LAYER 6: MVP ORCHESTRATOR (0% Complete)

**Location (Proposed):** ai_sam/services/mvp_orchestrator.py

**Purpose:** Coordinate searches across multiple sources

**Class Structure:**
```python
class MVPOrchestrator(models.AbstractModel):
    _name = 'mvp.orchestrator'
    _description = 'Multi-source Orchestration Service'

    @api.model
    def search_files(self, query, sources=None, file_type=None):
        """
        Search for files across multiple sources

        Args:
            query: Search query string
            sources: List of sources ['gdrive', 'onedrive', 'odoo', 'slack']
                    If None, searches all connected sources
            file_type: Filter by file type (pdf, docx, xlsx, etc.)

        Returns:
            List of normalized results with metadata
        """
        results = []

        # Determine which sources to search
        active_sources = self._get_active_sources(sources)

        # Search each source in parallel
        for source in active_sources:
            client = self._get_client(source)
            source_results = client.search(query, file_type)
            results.extend(source_results)

        # Normalize results (clearing layer)
        normalized = self._normalize_results(results)

        # Log orchestration
        self.env['mvp.orchestration.log'].create({
            'user_id': self.env.user.id,
            'action': 'search',
            'request_data': {
                'query': query,
                'sources': sources,
                'file_type': file_type
            },
            'response_data': normalized,
            'result_count': len(normalized),
            'status': 'success'
        })

        return normalized

    def _get_client(self, source):
        """Get API client for source"""
        if source == 'gdrive':
            return self.env['google.drive.client']
        elif source == 'onedrive':
            return self.env['onedrive.client']
        elif source == 'odoo':
            return self.env['ai.context.builder']
        elif source == 'slack':
            return self.env['slack.client']

    def _normalize_results(self, results):
        """Normalize results to unified format"""
        normalized = []
        for result in results:
            normalized.append({
                'name': result.get('title') or result.get('name'),
                'source': result.get('source'),
                'url': result.get('url') or result.get('link'),
                'modified_date': result.get('modified') or result.get('updated_at'),
                'size': result.get('size'),
                'type': result.get('mime_type') or result.get('file_type'),
                'icon': self._get_source_icon(result.get('source')),
                'preview': result.get('snippet') or result.get('description')[:200],
            })

        # Sort by relevance/date
        normalized.sort(key=lambda x: x['modified_date'], reverse=True)

        return normalized
```

**New Model Needed:**
```python
# ai_brain/models/mvp_orchestration_log.py
class MVPOrchestrationLog(models.Model):
    _name = 'mvp.orchestration.log'
    _description = 'Orchestration Execution Log'
    _order = 'created_date desc'

    user_id = fields.Many2one('res.users', required=True)
    action = fields.Selection([
        ('search', 'Search'),
        ('retrieve', 'Retrieve'),
        ('upload', 'Upload'),
    ])
    request_data = fields.Json()
    response_data = fields.Json()
    result_count = fields.Integer()
    execution_time = fields.Float()  # seconds
    status = fields.Selection([
        ('success', 'Success'),
        ('partial', 'Partial Success'),
        ('failed', 'Failed'),
    ])
    error_message = fields.Text()
    created_date = fields.Datetime(default=fields.Datetime.now)
```

### ❌ LAYER 7: INTENT PROCESSOR (0% Complete)

**Location (Proposed):** ai_sam/services/intent_processor.py

**Purpose:** Convert natural language to API calls

**Class Structure:**
```python
class IntentProcessor(models.AbstractModel):
    _name = 'intent.processor'
    _description = 'Natural Language Intent Processor'

    @api.model
    def process(self, user_query):
        """
        Process natural language query into structured API call

        Args:
            user_query: "Find my Q3 budget PDF"

        Returns:
            {
                'action': 'search',
                'query': 'Q3 budget',
                'file_type': 'pdf',
                'sources': ['gdrive', 'onedrive', 'odoo'],
                'filters': {}
            }
        """
        # Extract intent
        intent = self._extract_intent(user_query)

        # Extract entities
        entities = self._extract_entities(user_query)

        # Build structured query
        return {
            'action': intent,
            'query': entities.get('search_term'),
            'file_type': entities.get('file_type'),
            'sources': entities.get('sources') or self._get_default_sources(),
            'filters': entities.get('filters', {})
        }

    def _extract_intent(self, query):
        """Determine user intent"""
        query_lower = query.lower()

        if any(word in query_lower for word in ['find', 'search', 'look for']):
            return 'search'
        elif any(word in query_lower for word in ['upload', 'save', 'store']):
            return 'upload'
        elif any(word in query_lower for word in ['download', 'get', 'retrieve']):
            return 'retrieve'
        else:
            return 'search'  # default

    def _extract_entities(self, query):
        """Extract entities from query"""
        entities = {}

        # File type detection
        if 'pdf' in query.lower():
            entities['file_type'] = 'pdf'
        elif 'docx' in query.lower() or 'document' in query.lower():
            entities['file_type'] = 'docx'
        elif 'xlsx' in query.lower() or 'spreadsheet' in query.lower():
            entities['file_type'] = 'xlsx'

        # Source detection
        if 'google drive' in query.lower():
            entities['sources'] = ['gdrive']
        elif 'onedrive' in query.lower():
            entities['sources'] = ['onedrive']
        elif 'slack' in query.lower():
            entities['sources'] = ['slack']

        # Extract search term (remove intent words and file types)
        search_term = query
        for word in ['find', 'search', 'pdf', 'docx', 'xlsx', 'in', 'my', 'the']:
            search_term = search_term.replace(word, '')
        entities['search_term'] = search_term.strip()

        return entities
```

### ❌ LAYER 8: CHAT INTEGRATION (0% Complete)

**Location:** Modify existing ai_sam/controllers/sam_ai_chat_controller.py

**Changes Needed:**
```python
# In chat controller, add orchestration detection
def process_message(self, message):
    # Check if message needs orchestration
    if self._needs_orchestration(message):
        # Use intent processor
        intent = self.env['intent.processor'].process(message)

        # Use orchestrator
        results = self.env['mvp.orchestrator'].search_files(
            query=intent['query'],
            sources=intent['sources'],
            file_type=intent['file_type']
        )

        # Format results for chat
        return self._format_orchestration_results(results)
    else:
        # Normal Claude AI response
        return self._get_claude_response(message)

def _needs_orchestration(self, message):
    """Detect if message needs API orchestration"""
    keywords = ['find', 'search', 'look for', 'show me', 'where is']
    return any(keyword in message.lower() for keyword in keywords)

def _format_orchestration_results(self, results):
    """Format orchestration results for chat display"""
    if not results:
        return "I couldn't find any files matching your query."

    response = f"I found {len(results)} files:\n\n"
    for result in results[:10]:  # Top 10
        source_badge = f"[{result['source'].upper()}]"
        response += f"{source_badge} {result['name']}\n"
        response += f"  Modified: {result['modified_date']}\n"
        response += f"  {result['preview']}\n\n"

    return response
```

---

## IMPLEMENTATION ROADMAP

### Phase 1: API Client Wrappers (2 weeks)

**Week 1: Base Client + Google Drive**
- Day 1-2: Create base_client.py with OAuth refresh
- Day 3-5: Create gdrive_client.py and test

**Week 2: OneDrive + Slack**
- Day 1-3: Create onedrive_client.py
- Day 4-5: Create slack_client.py

**Deliverable:** Working API clients that can search and retrieve from external services

### Phase 2: MVP Orchestrator (1 week)

**Day 1-2:** Create mvp_orchestrator.py
- search_files() method
- _get_client() routing
- _normalize_results() clearing layer

**Day 3:** Create mvp.orchestration.log model

**Day 4-5:** Testing and refinement

**Deliverable:** Orchestrator can search multiple sources and return unified results

### Phase 3: Intent Processor (3 days)

**Day 1:** Create intent_processor.py
- _extract_intent() method
- _extract_entities() method

**Day 2:** Test with various queries

**Day 3:** Refinement and edge cases

**Deliverable:** Natural language queries converted to structured API calls

### Phase 4: Chat Integration (1 week)

**Day 1-2:** Modify chat controller
- Add orchestration detection
- Add result formatting

**Day 3-4:** UI updates
- Source badges
- Preview snippets
- Click to open functionality

**Day 5:** End-to-end testing

**Deliverable:** Users can search external services from SAM AI chat with natural language

**Total Timeline:** 4-5 weeks for complete API orchestration system

---

## INTEGRATION WITH MCP SERVER

### Current State
MCP server and API orchestration are separate systems.

### Integration Opportunity

**Scenario:** User searches Google Drive in Odoo in the morning, then on mobile in afternoon asks for same results.

**Implementation:**
```python
# MCP server generator adds new tools:

async def get_recent_searches(self, arguments):
    """Get recent orchestration searches from Odoo"""
    logs = self.odoo.env['mvp.orchestration.log'].search([
        ('user_id', '=', self.current_user_id),
        ('action', '=', 'search'),
    ], limit=10, order='created_date desc')

    # Return cached results (no re-searching APIs)
    results = []
    for log in logs:
        results.append({
            'query': log.request_data['query'],
            'result_count': log.result_count,
            'when': log.created_date,
            'results': log.response_data  # Cached!
        })

    return TextContent(type="text", text=format_results(results))

async def execute_search(self, arguments):
    """Trigger orchestration search from mobile"""
    result = self.odoo.env['mvp.orchestrator'].search_files(
        query=arguments['query'],
        sources=arguments.get('sources'),
        file_type=arguments.get('file_type')
    )

    return TextContent(type="text", text=format_results(result))
```

**Benefits:**
- Search once in Odoo (morning)
- Query cached results on mobile (afternoon)
- No duplicate API calls = cost savings
- Seamless bidirectional access

---

## CACHING STRATEGY

### Level 1: In-Memory Cache (Fastest)
```python
# 5-minute TTL for search results
@lru_cache(maxsize=128)
def _cached_search(query, sources, ttl=300):
    # Return cached if exists and fresh
    pass
```

### Level 2: Database Cache (mvp.orchestration.log)
- Persist all orchestration results
- TTL: 1 hour for file searches
- Invalidate on write operations
- Accessible from MCP server

### Level 3: API Rate Limiting
```python
class BaseAPIClient:
    def __init__(self):
        self.rate_limiter = RateLimiter(
            requests_per_minute=60,  # Adjust per API
            burst_size=10
        )
```

---

## COST OPTIMIZATION

### API Call Tracking
```python
# In base_client.py
def _log_api_call(self, service, operation, cost=0):
    self.env['api.operation.log'].create({
        'user_id': self.env.user.id,
        'service_type': service,
        'operation': operation,
        'cost': cost,  # If API charges per call
        'timestamp': fields.Datetime.now()
    })
```

### Budget Caps
```python
# Check budget before API call
provider = self.env['api.service.provider'].search([
    ('service_type_name', '=', 'Google Drive'),
], limit=1)

if provider.monthly_cost >= provider.budget_cap:
    raise UserError('Monthly budget cap reached for Google Drive API')
```

### Smart Caching
- Cache file metadata (names, dates) aggressively
- Cache file content only on user request
- Invalidate cache on known write operations

---

## SECURITY CONSIDERATIONS

### Credential Security
✅ OAuth tokens encrypted at rest (via Odoo's security)
✅ Tokens stored in database, not config files
✅ Per-user credentials (no shared accounts)
⚠️ Token refresh handled automatically

### API Access Control
- User sees only files they have access to in external services
- Odoo's security model applies (user A can't see user B's orchestration logs)
- API clients respect external service permissions

### Audit Trail
- All API operations logged in api.operation.log
- All orchestration logged in mvp.orchestration.log
- Can track: who searched what, when, which services, results count

---

## TESTING STRATEGY

### Unit Tests
```python
class TestGoogleDriveClient(TransactionCase):
    def test_search(self):
        client = self.env['google.drive.client']
        results = client.search('budget', file_type='pdf')
        self.assertTrue(len(results) >= 0)

    def test_oauth_refresh(self):
        # Test token refresh when expired
        pass
```

### Integration Tests
```python
class TestMVPOrchestrator(TransactionCase):
    def test_multi_source_search(self):
        orchestrator = self.env['mvp.orchestrator']
        results = orchestrator.search_files(
            query='Q3 budget',
            sources=['gdrive', 'odoo'],
            file_type='pdf'
        )
        # Verify results from both sources
        self.assertTrue(any(r['source'] == 'gdrive' for r in results))
        self.assertTrue(any(r['source'] == 'odoo' for r in results))
```

### End-to-End Tests
1. User connects Google Drive (OAuth flow)
2. User searches "budget PDF" in SAM AI chat
3. Verify orchestrator called
4. Verify results from both Odoo and Google Drive
5. Verify results logged
6. Verify UI displays source badges

---

## DEPLOYMENT CHECKLIST

### Prerequisites
- [ ] User has Google account
- [ ] User has Microsoft account (for OneDrive)
- [ ] OAuth apps created in Google Cloud Console
- [ ] OAuth apps created in Azure (Microsoft)
- [ ] Redirect URIs configured

### Installation
- [ ] Install ai_sam module (includes MCP generator)
- [ ] API client wrappers available
- [ ] Orchestrator service available
- [ ] Chat integration enabled

### Configuration
- [ ] Navigate to SAM AI → API Settings
- [ ] Click "Connect Google Drive"
- [ ] Complete OAuth flow
- [ ] Click "Connect OneDrive"
- [ ] Complete OAuth flow
- [ ] Test connection for each service

### Testing
- [ ] Search files from chat
- [ ] Verify multi-source results
- [ ] Check orchestration logs
- [ ] Test from mobile (MCP server)

---

## CURRENT FILES STATUS

### ✅ Existing Files (Foundation - 70%)
```
ai_brain/models/
  ✅ api_service_provider.py (OAuth infrastructure)
  ✅ api_credentials.py (credential storage)
  ✅ api_operation_log.py (API logging)
  ✅ ai_context_builder.py (Odoo data access)

ai_sam/controllers/
  ✅ api_oauth_controller.py (OAuth flow)
  ✅ vendor_registry_controller.py (vendor auto-population)

ai_sam/static/src/vendor_library/
  ✅ 100+ vendor config files
```

### ❌ Missing Files (Orchestration - 30%)
```
ai_brain/models/
  ❌ mvp_orchestration_log.py (orchestration logging)
  ❌ mvp_integration_connection.py (connection status)

ai_sam/services/integrations/
  ❌ base_client.py (base API client)
  ❌ gdrive_client.py (Google Drive)
  ❌ onedrive_client.py (OneDrive/Microsoft)
  ❌ youtube_client.py (YouTube)
  ❌ gmail_client.py (Gmail)
  ❌ slack_client.py (Slack)

ai_sam/services/
  ❌ mvp_orchestrator.py (orchestration service)
  ❌ intent_processor.py (natural language processing)

ai_sam/views/
  ❌ integration_connection_views.xml (UI for connections)
  ❌ orchestration_log_views.xml (UI for logs)

ai_sam/controllers/
  ❌ mvp_controller.py (orchestration API endpoints)
```

---

## RELATED DOCUMENTATION

- [MCP_SERVER.txt](./MCP_SERVER.txt) - MCP server (external access)
- [MCP_API_COMPLETE_ARCHITECTURE.txt](./MCP_API_COMPLETE_ARCHITECTURE.txt) - Full system overview
- [SAM_CHAT_ARCHITECTURE.txt](./SAM_CHAT_ARCHITECTURE.txt) - 4-layer chat system

---

## CONCLUSION

SAM AI's API strategy is **70% complete** with solid foundations:
- ✅ OAuth infrastructure working
- ✅ Credential storage working
- ✅ Vendor library comprehensive
- ✅ Odoo context builder ready

**Next milestone:** Build the orchestration layer (30% remaining)
- API client wrappers (2 weeks)
- MVP orchestrator (1 week)
- Intent processor (3 days)
- Chat integration (1 week)

**Total time to completion:** 4-5 weeks of focused development

**Benefits when complete:**
- Natural language searches across all services
- Unified results in SAM AI chat
- Source badges and previews
- Cached results accessible from mobile (MCP)
- Complete audit trail
- Cost tracking and optimization

---

Document maintained by: SAM AI Team
Last reviewed: 2025-11-04
Next review: After orchestration layer implementation
Status: Foundation complete, awaiting orchestration implementation
