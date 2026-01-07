# 🧠 Hierarchical Knowledge Graph - Master Implementation Plan

**Vision**: Transform scattered conversations into a navigable knowledge hierarchy where clicking a domain hub activates the right AI agent with pre-loaded context.

---

## 🎯 The Ultimate Outcome

### What the User Experiences:

**Scenario 1: Strategic Marketing Discussion**
1. User clicks **[MARKETING HUB]** on graph
2. `/cmo` agent activates instantly
3. CMO SAM says: *"I've analyzed your 5 marketing conversations across Copywriting, Social Media, Email, SEO, and Ads. What strategic initiative should we focus on?"*
4. User: "Let's expand our direct response copywriting"
5. CMO SAM: *"Great! I see we discussed that in your Copywriting cluster (2 conversations). Let me pull those insights... [loads conversations #847, #923]... Here's what we learned..."*

**Scenario 2: Tactical Execution**
1. User clicks **[Copywriting]** sub-node under Marketing
2. Focused SAM activates with ONLY copywriting context (2 conversations)
3. SAM: *"Ready to write copy! I have your frameworks from our previous sessions. What are we writing today?"*

**Scenario 3: Deep Dive**
1. User clicks individual conversation: **"Direct Response Framework Session #847"**
2. Opens full conversation thread
3. "Continue this conversation" button → SAM loads THAT exact context
4. SAM: *"Picking up where we left off on landing page headlines..."*

---

## 🏗️ Architecture: 4-Tier Knowledge Hierarchy

```
Tier 1: BUSINESS DOMAINS (Master Hubs)
        ├─ Development (189 convos)
        ├─ Marketing (5 convos)
        ├─ Support (18 convos)
        ├─ Operations (6 convos)
        ├─ Product (3 convos)
        └─ Sales (1 convo)

Tier 2: DOMAIN SUB-CATEGORIES (Auto-detected topics)
        Marketing Hub
        ├─ Copywriting (2 convos)
        ├─ Social Media (1 convo)
        ├─ Email Marketing (1 convo)
        └─ SEO/Ads (1 convo)

Tier 3: CONVERSATION CLUSTERS (Semantic groups)
        Copywriting
        ├─ Direct Response Framework
        └─ Landing Page Optimization

Tier 4: INDIVIDUAL CONVERSATIONS
        "Direct Response Framework Session #847"
        └─ 24 messages, created 2025-10-12
```

---

## 📊 Database Schema Design

### New Models:

#### 1. `ai.knowledge.domain` (Business Domain Hubs)
```python
_name = 'ai.knowledge.domain'
_description = 'Business Domain Knowledge Hubs'

name = fields.Char('Domain Name')  # "Marketing", "Development"
code = fields.Selection([...])  # 'marketing', 'development'
color = fields.Char('Graph Color')  # '#2ecc71'
icon = fields.Char('Icon')  # 'fa-bullhorn'

# Agent configuration
agent_command = fields.Char('Slash Command')  # '/cmo', '/developer'
agent_description = fields.Text('Agent Context Prompt')

# Stats
conversation_count = fields.Integer(compute='_compute_stats')
message_count = fields.Integer(compute='_compute_stats')
last_activity = fields.Datetime(compute='_compute_stats')

# Graph positioning
graph_x = fields.Float('X Position')
graph_y = fields.Float('Y Position')
graph_size = fields.Integer('Node Size', default=50)
```

#### 2. `ai.knowledge.subcategory` (Domain Sub-Topics)
```python
_name = 'ai.knowledge.subcategory'
_description = 'Knowledge Sub-Categories (Auto-detected)'

name = fields.Char('Subcategory Name')  # "Copywriting", "Social Media"
domain_id = fields.Many2one('ai.knowledge.domain', required=True)

# AI-detected or manual
detection_method = fields.Selection([
    ('ai', 'AI Auto-detected'),
    ('manual', 'Manually Created'),
    ('keyword', 'Keyword Clustering')
])

keywords = fields.Text('Defining Keywords')  # "copy, headlines, CTA, conversion"
confidence = fields.Float('Detection Confidence')  # 0.0 - 1.0

conversation_ids = fields.Many2many('ai.conversation', compute='_compute_conversations')
conversation_count = fields.Integer(compute='_compute_stats')
```

#### 3. Update `ai.conversation` with subcategory link
```python
# Add to existing ai.conversation model:

# Tier 1: Business Domain (already exists)
business_domain = fields.Selection([...])

# Tier 2: Subcategory (NEW)
subcategory_id = fields.Many2one('ai.knowledge.subcategory',
    string='Knowledge Subcategory',
    help='AI-detected topic within business domain')

subcategory_confidence = fields.Float('Subcategory Confidence')

# Tier 3: Cluster (for semantic grouping)
cluster_id = fields.Char('Semantic Cluster ID',
    help='UUID for semantically similar conversations')
```

---

## 🤖 AI-Powered Subcategory Detection Service

### New Service: `ai.subcategory.detector`

```python
class AISubcategoryDetector(models.AbstractModel):
    _name = 'ai.subcategory.detector'
    _description = 'Auto-detect knowledge subcategories within domains'

    @api.model
    def analyze_domain_subcategories(self, domain_code, max_subcategories=10):
        """
        Analyze all conversations in a domain and detect natural subcategories

        Args:
            domain_code: 'marketing', 'development', etc.
            max_subcategories: Maximum number of subcategories to detect

        Returns:
            [
                {
                    'name': 'Copywriting',
                    'keywords': ['copy', 'headlines', 'CTA', 'conversion'],
                    'conversation_ids': [847, 923],
                    'confidence': 0.92
                },
                ...
            ]
        """

        # Get all conversations for domain
        conversations = self.env['ai.conversation'].search([
            ('business_domain', '=', domain_code)
        ])

        if len(conversations) < 3:
            return []  # Need at least 3 conversations to cluster

        # Build combined text from all conversations
        conv_texts = []
        conv_ids = []

        for conv in conversations:
            # Get first 500 chars from first 5 messages
            messages = conv.ai_message_ids.sorted('create_date')[:5]
            text = ' '.join([msg.content[:500] for msg in messages])
            conv_texts.append(text)
            conv_ids.append(conv.id)

        # Ask Claude to detect natural topic clusters
        prompt = f"""Analyze these {len(conversations)} {domain_code} conversations and identify natural topic clusters (subcategories).

CONVERSATIONS:
{self._format_conversations_for_analysis(conversations)}

TASK:
1. Identify {min(max_subcategories, len(conversations))} distinct topic clusters
2. For each cluster, provide:
   - Clear subcategory name (2-3 words)
   - 3-5 defining keywords
   - Which conversation IDs belong to this cluster
   - Confidence score (0.0-1.0)

RESPONSE FORMAT (JSON):
{{
  "subcategories": [
    {{
      "name": "Copywriting & Conversion",
      "keywords": ["copy", "headlines", "CTA", "conversion", "landing page"],
      "conversation_ids": [847, 923],
      "confidence": 0.92,
      "reasoning": "These conversations focus on direct response copywriting techniques"
    }},
    ...
  ]
}}

Only return valid JSON.
"""

        # Call Claude API directly
        config = self.env['ai.service.config'].get_config()

        headers = {
            'x-api-key': config.api_key,
            'anthropic-version': '2023-06-01',
            'content-type': 'application/json',
        }

        payload = {
            'model': config.model_name,
            'max_tokens': 2000,
            'temperature': 0.3,
            'messages': [{'role': 'user', 'content': prompt}],
        }

        response = requests.post(config.api_endpoint, headers=headers, json=payload, timeout=120)

        if response.status_code != 200:
            _logger.error(f"Subcategory detection failed: {response.text}")
            return []

        result_text = response.json()['content'][0]['text']

        # Parse JSON
        import json
        result = json.loads(self._extract_json(result_text))

        return result.get('subcategories', [])

    @api.model
    def create_subcategories_for_domain(self, domain_code):
        """
        Detect and create subcategory records for a domain
        """
        domain = self.env['ai.knowledge.domain'].search([('code', '=', domain_code)], limit=1)

        if not domain:
            _logger.warning(f"Domain {domain_code} not found")
            return []

        # Detect subcategories
        subcategories = self.analyze_domain_subcategories(domain_code)

        created_subcats = []

        for subcat_data in subcategories:
            # Create subcategory record
            subcat = self.env['ai.knowledge.subcategory'].create({
                'name': subcat_data['name'],
                'domain_id': domain.id,
                'detection_method': 'ai',
                'keywords': ', '.join(subcat_data['keywords']),
                'confidence': subcat_data.get('confidence', 0.0),
            })

            # Link conversations
            conv_ids = subcat_data.get('conversation_ids', [])
            conversations = self.env['ai.conversation'].browse(conv_ids)

            conversations.write({
                'subcategory_id': subcat.id,
                'subcategory_confidence': subcat_data.get('confidence', 0.0),
            })

            created_subcats.append(subcat)

            _logger.info(
                f"Created subcategory '{subcat.name}' with {len(conv_ids)} conversations "
                f"(confidence: {subcat_data.get('confidence', 0.0):.2f})"
            )

        return created_subcats
```

---

## 🎨 Graph Visualization Updates

### Hierarchical Graph Structure:

```javascript
// Generate hierarchical graph data
function buildHierarchicalGraph(data) {
    const nodes = [];
    const edges = [];

    // Tier 1: Domain Hubs (6 master nodes)
    const domains = [
        {id: 'hub_development', label: 'DEVELOPMENT', color: '#e74c3c', size: 80, x: 0, y: -300},
        {id: 'hub_marketing', label: 'MARKETING', color: '#2ecc71', size: 60, x: -300, y: 0},
        {id: 'hub_support', label: 'SUPPORT', color: '#34495e', size: 65, x: 300, y: 0},
        {id: 'hub_operations', label: 'OPERATIONS', color: '#9b59b6', size: 55, x: -200, y: 250},
        {id: 'hub_product', label: 'PRODUCT', color: '#16a085', size: 50, x: 200, y: 250},
        {id: 'hub_sales', label: 'SALES', color: '#3498db', size: 45, x: 0, y: 300}
    ];

    domains.forEach(domain => {
        nodes.push({
            ...domain,
            shape: 'box',
            font: {size: 18, bold: true, color: '#fff'},
            borderWidth: 3,
            shadow: true,
            data: {type: 'domain_hub'}
        });
    });

    // Tier 2: Subcategory nodes (if detected)
    data.subcategories.forEach(subcat => {
        const hubId = `hub_${subcat.domain_code}`;
        const subcatId = `subcat_${subcat.id}`;

        nodes.push({
            id: subcatId,
            label: subcat.name,
            color: subcat.color,
            size: 30,
            shape: 'ellipse',
            font: {size: 14, bold: true},
            data: {type: 'subcategory', subcat_id: subcat.id}
        });

        // Connect subcategory to domain hub
        edges.push({
            from: hubId,
            to: subcatId,
            width: 3,
            color: {color: subcat.color, opacity: 0.6},
            dashes: false
        });
    });

    // Tier 3 & 4: Conversation nodes
    data.conversations.forEach(conv => {
        const convId = `conv_${conv.id}`;

        // Determine parent (subcategory or domain hub)
        const parentId = conv.subcategory_id
            ? `subcat_${conv.subcategory_id}`
            : `hub_${conv.business_domain}`;

        nodes.push({
            id: convId,
            label: conv.name,
            color: conv.color,
            size: 12,
            shape: 'dot',
            font: {size: 10},
            data: {
                type: 'conversation',
                conversation_id: conv.id,
                domain: conv.business_domain,
                subcategory: conv.subcategory_name
            }
        });

        // Connect conversation to parent
        edges.push({
            from: parentId,
            to: convId,
            width: 1,
            color: {color: '#bdc3c7', opacity: 0.3},
            dashes: true
        });
    });

    // Tier 4: Semantic connections between conversations (optional)
    data.semantic_edges.forEach(edge => {
        edges.push({
            from: `conv_${edge.source}`,
            to: `conv_${edge.target}`,
            width: 0.5,
            color: {color: '#95a5a6', opacity: 0.2},
            dashes: [5, 5],
            title: `${(edge.similarity * 100).toFixed(0)}% similar`
        });
    });

    return {nodes, edges};
}

// Click handler for domain hubs
network.on('click', function(params) {
    if (params.nodes.length > 0) {
        const nodeId = params.nodes[0];
        const node = nodes.get(nodeId);

        if (node.data.type === 'domain_hub') {
            // Extract domain from hub ID (e.g., 'hub_marketing' -> 'marketing')
            const domain = nodeId.replace('hub_', '');
            activateDomainAgent(domain);
        }
        else if (node.data.type === 'subcategory') {
            openSubcategoryView(node.data.subcat_id);
        }
        else if (node.data.type === 'conversation') {
            openConversation(node.data.conversation_id);
        }
    }
});

// Activate domain-specific agent
function activateDomainAgent(domain) {
    const agentMap = {
        'marketing': '/cmo',
        'development': '/developer',
        'support': '/support-agent',
        'operations': '/operations-manager',
        'product': '/product-manager',
        'sales': '/sales-agent'
    };

    const command = agentMap[domain];

    // Redirect to SAM chat with pre-loaded domain context
    window.location.href = `/sam/chat?agent=${command}&domain=${domain}&load_context=true`;
}
```

---

## 🔧 Implementation Phases

### **Phase 1: Foundation (Week 1)**
**Goal**: Create domain hub infrastructure

**Tasks**:
1. ✅ Create `ai.knowledge.domain` model
2. ✅ Create `ai.knowledge.subcategory` model
3. ✅ Add `subcategory_id` field to `ai.conversation`
4. ✅ Seed 6 domain hub records (Development, Marketing, Support, Operations, Product, Sales)
5. ✅ Update graph service to include domain hubs in node data
6. ✅ Update graph visualization to show domain hubs as large central nodes
7. ✅ Test: Graph shows 6 hubs + 227 conversations connected with lines

**Success Criteria**:
- Graph displays hierarchical structure
- Domain hubs are visually distinct (larger, bold labels)
- All conversations connected to parent domain hub

---

### **Phase 2: AI Subcategory Detection (Week 2)**
**Goal**: Auto-detect knowledge subcategories within each domain

**Tasks**:
1. ✅ Create `ai.subcategory.detector` service
2. ✅ Implement `analyze_domain_subcategories()` method
3. ✅ Create bulk detection script: `detect_all_subcategories.py`
4. ✅ Run detection on Marketing domain (5 conversations → expected 2-3 subcategories)
5. ✅ Review/refine detected subcategories
6. ✅ Run detection on Development domain (189 conversations → expected 10-15 subcategories)
7. ✅ Update graph to show subcategory nodes between hubs and conversations

**Success Criteria**:
- Marketing shows subcategories: "Copywriting", "Social Media", "Email Marketing"
- Development shows subcategories: "Odoo Architecture", "Debugging", "Module Development", etc.
- Graph shows 3-tier hierarchy: Hub → Subcategory → Conversations

---

### **Phase 3: Agent Activation System (Week 3)**
**Goal**: Clicking domain hub activates the right agent with context

**Tasks**:
1. ✅ Create domain → agent mapping configuration
2. ✅ Build agent context loader service: `ai.agent.context.loader`
3. ✅ Implement `/cmo` integration with Marketing hub
4. ✅ Implement `/developer` integration with Development hub
5. ✅ Create SAM chat interface enhancement:
   - Show "Domain: Marketing" badge
   - Display conversation count in context
   - Show subcategories loaded
6. ✅ Test workflow: Click Marketing hub → /cmo activates → 5 convos loaded → Ask question

**Agent Context Loading**:
```python
class AgentContextLoader(models.AbstractModel):
    _name = 'ai.agent.context.loader'

    @api.model
    def load_domain_context(self, domain_code):
        """
        Load all conversations for a domain into agent context

        Returns:
            {
                'domain': 'marketing',
                'agent_command': '/cmo',
                'conversations': [...],
                'subcategories': [...],
                'total_messages': 127,
                'insights': 'AI-generated summary of key themes'
            }
        """
        domain = self.env['ai.knowledge.domain'].search([('code', '=', domain_code)])
        conversations = self.env['ai.conversation'].search([
            ('business_domain', '=', domain_code)
        ])

        # Generate domain summary
        summary_prompt = f"""Analyze these {len(conversations)} {domain_code} conversations and provide:
        1. Top 3 themes/topics discussed
        2. Key insights or patterns
        3. Suggested focus areas for future work

        Keep it concise (3-4 sentences).
        """

        # Call AI to generate summary
        summary = self._generate_summary(conversations, summary_prompt)

        return {
            'domain': domain_code,
            'agent_command': domain.agent_command,
            'conversation_ids': conversations.ids,
            'conversation_count': len(conversations),
            'total_messages': sum(len(c.ai_message_ids) for c in conversations),
            'subcategories': self._get_subcategories(domain),
            'insights': summary
        }
```

**Success Criteria**:
- Click Marketing hub → CMO agent opens with context banner
- Agent immediately references marketing conversation history
- User can ask domain-specific questions with accurate responses

---

### **Phase 4: Subcategory Navigation (Week 4)**
**Goal**: Click subcategory to narrow context

**Tasks**:
1. ✅ Make subcategory nodes clickable
2. ✅ Create subcategory detail view showing:
   - Conversation list
   - AI-generated topic summary
   - "Chat about this topic" button
3. ✅ Implement focused context loading (e.g., only "Copywriting" conversations)
4. ✅ Add breadcrumb navigation: Marketing → Copywriting → Conversation #847

**Success Criteria**:
- Click "Copywriting" subcategory → Shows 2 copywriting conversations
- Click "Chat" → SAM loads ONLY copywriting context (not all 5 marketing convos)
- User can drill down from broad (Marketing) to narrow (Copywriting) to specific (Conversation #847)

---

### **Phase 5: Knowledge Synthesis & Search (Week 5)**
**Goal**: SAM can reference consolidated knowledge when answering

**Tasks**:
1. ✅ Create domain knowledge index: `ai.knowledge.index`
2. ✅ Implement smart context injection for SAM queries
3. ✅ Add "Search within domain" functionality
4. ✅ Create "Domain Insights" dashboard showing:
   - AI-generated summaries per domain
   - Top topics/themes
   - Recent activity
   - Quick actions (Chat, Search, Summarize)

**Smart Context Injection**:
```python
# When user asks SAM a question
user_query = "How should I write landing page headlines?"

# Detect relevant domain(s)
domains = self._detect_query_domain(user_query)  # Returns ['marketing']

# Load domain context
context = self.env['ai.agent.context.loader'].load_domain_context('marketing')

# Detect relevant subcategory
subcategory = self._detect_subcategory(user_query, context['subcategories'])  # Returns 'Copywriting'

# Load ONLY relevant conversations
relevant_convos = self.env['ai.conversation'].search([
    ('business_domain', '=', 'marketing'),
    ('subcategory_id.name', '=', 'Copywriting')
])

# Build context-aware prompt
system_prompt = f"""You are the CMO agent. You have access to {len(relevant_convos)} conversations
about copywriting and conversion optimization.

RELEVANT KNOWLEDGE:
{self._format_conversations_as_context(relevant_convos)}

The user is asking about landing page headlines. Reference the specific techniques and frameworks
discussed in the copywriting conversations above.
"""

# Send to Claude with focused context
```

**Success Criteria**:
- User asks marketing question → SAM automatically loads Marketing domain context
- User asks about "copywriting" → SAM narrows to Copywriting subcategory
- Responses reference specific conversation insights
- No generic/hallucinated answers - everything grounded in user's actual knowledge

---

## 🎯 Success Metrics

### Quantitative:
- ✅ 227 conversations organized into 6 domains
- ✅ 10-20 subcategories auto-detected across all domains
- ✅ 100% of conversations linked to parent domain/subcategory
- ⏱️ <2 seconds to activate domain agent with full context
- 🎯 >90% accuracy in AI subcategory detection (user can manually adjust)

### Qualitative:
- 😊 User can find marketing knowledge in <5 seconds (click hub)
- 🧠 SAM gives contextually accurate answers (references actual conversations)
- 🚀 User excitement: "This is my second brain!"
- 💡 Agent feels intelligent (not generic chatbot)

---

## 🎁 Bonus Features (Phase 6+)

### 1. **Cross-Domain Insights**
- "Show me where Marketing and Development overlap"
- Detect conversations that span multiple domains
- Cross-pollinate ideas between domains

### 2. **Temporal Navigation**
- Timeline view: "Show my marketing evolution over time"
- Highlight knowledge gaps: "You haven't discussed email marketing in 3 months"

### 3. **Knowledge Export**
- "Export all Copywriting insights as a PDF playbook"
- Generate domain summary reports
- Create shareable knowledge artifacts

### 4. **Collaborative Knowledge**
- Multi-user: Team members contribute to shared domain knowledge
- Knowledge handoff: "Transfer my Development knowledge to new dev"

### 5. **Predictive Recommendations**
- "Based on your Marketing conversations, you might want to explore X"
- Suggest next questions to expand knowledge in a domain

---

## 🚀 Immediate Next Steps

### What to build FIRST (this session):

**Quick Win: Marketing Hub Prototype**

1. Create domain hub nodes in graph (30 min)
2. Connect Marketing conversations to hub with lines (15 min)
3. Make hub clickable → Opens `/cmo` with context (45 min)
4. Test: Click Marketing hub → CMO activates → Ask marketing question → Get contextual answer

**Then delegate to /developer**:

Copy this entire plan into `/developer` agent with this prompt:

```
/developer

I need you to implement the Hierarchical Knowledge Graph system as detailed in
HIERARCHICAL_KNOWLEDGE_GRAPH_MASTER_PLAN.md.

START WITH PHASE 1 (Foundation):
- Create ai.knowledge.domain model
- Create ai.knowledge.subcategory model
- Update ai.conversation with subcategory_id field
- Seed 6 domain hub records
- Update graph service to show domain hubs as central nodes
- Connect all 227 conversations to parent hubs with lines

FOCUS: Make the graph show hierarchical structure - 6 big domain hubs with
conversations radiating out like spokes.

After Phase 1 works, we'll move to Phase 2 (AI subcategory detection).

Ready?
```

---

**This is the roadmap to turn scattered conversations into organized, accessible, agent-activated knowledge.**

Would you like me to start building Phase 1 now, or refine the plan further?
