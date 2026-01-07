# Business Categorization Feature - Design Document

## Overview

Automatically categorize conversations by business domain (Sales, Marketing, Development, etc.) to enable:
- Visual clustering in memory graph
- Domain-specific filtering
- Business intelligence insights
- Semantic connections WITHIN domains

---

## Architecture

### Layer 1: Technical Chunking (Current - ✅ Working)
```
Purpose: Enable semantic search
Method: Split by 512 tokens
Output: Vector embeddings in ChromaDB
```

### Layer 2: Business Categorization (New - 💡 To Build)
```
Purpose: Business context organization
Method: AI-powered domain detection
Output: business_domain field on ai.conversation
```

### Layer 3: Visual Clustering (New - 💡 To Build)
```
Purpose: Graph visualization
Method: Group by business_domain + semantic edges
Output: Color-coded clusters in memory graph
```

---

## Database Schema Changes

### 1. Add Business Domain Field

**File**: `ai_brain/models/ai_conversation.py`

```python
# Add after line 106 (after conversation_type)

# Business Domain (for categorization & visualization)
business_domain = fields.Selection([
    ('sales', 'Sales & Revenue'),
    ('marketing', 'Marketing & Growth'),
    ('development', 'Software Development'),
    ('operations', 'Operations & Processes'),
    ('strategy', 'Business Strategy'),
    ('finance', 'Finance & Accounting'),
    ('hr', 'Human Resources'),
    ('support', 'Customer Support'),
    ('product', 'Product Management'),
    ('uncategorized', 'Uncategorized'),
], string='Business Domain',
   default='uncategorized',
   index=True,
   help='Primary business domain this conversation relates to')

# Domain confidence score (how confident is the AI categorization?)
domain_confidence = fields.Float(
    string='Domain Confidence',
    default=0.0,
    help='AI confidence score (0.0-1.0) for the detected domain'
)

# Secondary domains (conversations can span multiple domains)
secondary_domains = fields.Many2many(
    'ai.conversation.domain',
    string='Related Domains',
    help='Other business domains this conversation touches on'
)
```

### 2. Create Domain Tag Model

**New File**: `ai_brain/models/ai_conversation_domain.py`

```python
# -*- coding: utf-8 -*-
from odoo import models, fields

class AIConversationDomain(models.Model):
    _name = 'ai.conversation.domain'
    _description = 'Business Domain Tags'

    name = fields.Char('Domain Name', required=True)
    code = fields.Char('Code', required=True, index=True)
    color = fields.Integer('Color Index', default=0)
    description = fields.Text('Description')

    # For graph visualization
    graph_color = fields.Char('Graph Color (Hex)', default='#95a5a6')
    graph_group = fields.Integer('Graph Group ID', help='vis.js group ID')

    _sql_constraints = [
        ('code_unique', 'unique(code)', 'Domain code must be unique!')
    ]
```

---

## AI Categorization Service

### New Service Model

**File**: `ai_brain/models/ai_categorization_service.py`

```python
# -*- coding: utf-8 -*-
"""
AI Categorization Service
==========================

Automatically detects business domain for conversations using Claude AI.

Author: Better Business Builders
Date: October 2025
"""

from odoo import models, api
import logging

_logger = logging.getLogger(__name__)


class AICategorization(models.AbstractModel):
    _name = 'ai.categorization.service'
    _description = 'AI-Powered Business Domain Categorization'

    @api.model
    def categorize_conversation(self, conversation_id):
        """
        Analyze conversation and detect business domain

        Returns:
            {
                'domain': 'sales',
                'confidence': 0.85,
                'secondary_domains': ['marketing', 'strategy'],
                'reasoning': 'Conversation focuses on pricing strategy...'
            }
        """
        conversation = self.env['ai.conversation'].browse(conversation_id)

        if not conversation.exists():
            return {'error': 'Conversation not found'}

        # Build analysis prompt
        prompt = self._build_categorization_prompt(conversation)

        # Call Claude AI
        ai_service = self.env['ai.service']
        response = ai_service.generate_completion(prompt)

        # Parse response
        result = self._parse_categorization_response(response)

        # Update conversation
        if result.get('domain'):
            conversation.write({
                'business_domain': result['domain'],
                'domain_confidence': result.get('confidence', 0.0),
            })

            _logger.info(
                f"Categorized conversation {conversation.id} as '{result['domain']}' "
                f"(confidence: {result['confidence']})"
            )

        return result

    def _build_categorization_prompt(self, conversation):
        """Build Claude prompt for domain detection"""

        # Get first 10 messages for analysis (representative sample)
        messages = conversation.ai_message_ids[:10]
        message_text = "\n\n".join([
            f"{msg.role}: {msg.content[:500]}"
            for msg in messages
        ])

        prompt = f"""Analyze this business conversation and categorize it by primary business domain.

CONVERSATION TITLE: {conversation.name}

CONVERSATION MESSAGES:
{message_text}

AVAILABLE DOMAINS:
- sales: Sales strategy, pricing, deals, revenue, sales funnel, lead generation
- marketing: Marketing campaigns, branding, content, SEO, social media, advertising
- development: Software development, coding, debugging, architecture, technical implementation
- operations: Business operations, processes, workflows, efficiency, automation
- strategy: Business strategy, planning, vision, goals, competitive analysis
- finance: Finance, accounting, budgets, expenses, financial planning
- hr: Human resources, hiring, team management, culture, training
- support: Customer support, help desk, troubleshooting, customer issues
- product: Product management, roadmap, features, user experience, product strategy

TASK:
1. Identify the PRIMARY business domain (choose ONE from the list above)
2. Provide confidence score (0.0-1.0)
3. Identify up to 2 SECONDARY domains (if applicable)
4. Explain your reasoning (1 sentence)

RESPONSE FORMAT (JSON):
{{
  "domain": "development",
  "confidence": 0.85,
  "secondary_domains": ["operations", "strategy"],
  "reasoning": "Conversation focuses on Odoo module architecture with discussion of workflow automation."
}}

Respond ONLY with valid JSON:"""

        return prompt

    def _parse_categorization_response(self, response):
        """Parse Claude's JSON response"""
        import json

        try:
            # Extract JSON from response
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            json_str = response[json_start:json_end]

            result = json.loads(json_str)

            # Validate domain
            valid_domains = [
                'sales', 'marketing', 'development', 'operations',
                'strategy', 'finance', 'hr', 'support', 'product'
            ]

            if result.get('domain') not in valid_domains:
                result['domain'] = 'uncategorized'
                result['confidence'] = 0.0

            return result

        except Exception as e:
            _logger.error(f"Failed to parse categorization response: {e}")
            return {
                'domain': 'uncategorized',
                'confidence': 0.0,
                'error': str(e)
            }

    @api.model
    def bulk_categorize(self, conversation_ids=None, limit=None):
        """
        Categorize multiple conversations in bulk

        Args:
            conversation_ids: List of conversation IDs (None = all uncategorized)
            limit: Max number to process

        Returns:
            {
                'success': 150,
                'failed': 2,
                'skipped': 10
            }
        """
        if conversation_ids:
            conversations = self.env['ai.conversation'].browse(conversation_ids)
        else:
            # Get uncategorized conversations
            domain = [('business_domain', '=', 'uncategorized')]
            conversations = self.env['ai.conversation'].search(domain, limit=limit)

        success = 0
        failed = 0
        skipped = 0

        total = len(conversations)

        _logger.info(f"Starting bulk categorization of {total} conversations...")

        for idx, conv in enumerate(conversations, 1):
            try:
                # Skip if already categorized (unless forced)
                if conv.business_domain != 'uncategorized':
                    skipped += 1
                    continue

                # Categorize
                result = self.categorize_conversation(conv.id)

                if result.get('error'):
                    failed += 1
                    _logger.warning(f"[{idx}/{total}] Failed: {conv.name} - {result['error']}")
                else:
                    success += 1
                    _logger.info(
                        f"[{idx}/{total}] ✅ {conv.name[:50]} → {result['domain']} "
                        f"(confidence: {result.get('confidence', 0)})"
                    )

                # Commit every 10
                if idx % 10 == 0:
                    self.env.cr.commit()

            except Exception as e:
                failed += 1
                _logger.error(f"[{idx}/{total}] ❌ Error categorizing {conv.id}: {e}")

        # Final commit
        self.env.cr.commit()

        _logger.info(
            f"Bulk categorization complete: "
            f"✅ {success} success, ❌ {failed} failed, ⊘ {skipped} skipped"
        )

        return {
            'success': success,
            'failed': failed,
            'skipped': skipped,
            'total': total
        }
```

---

## Integration with Import Wizard

### Update Import Process

**File**: `ai_brain/models/ai_conversation_import.py`

Add after line 464 (after graph node creation):

```python
# Categorize conversation (if AI service available)
if self.auto_categorize:
    try:
        categorization = self.env['ai.categorization.service'].categorize_conversation(conv.id)
        log_lines.append(f"  → Categorized as: {categorization.get('domain', 'unknown')}")
    except Exception as e:
        _logger.warning(f"Failed to categorize conversation {conv.id}: {e}")
```

Add field to wizard:

```python
# Line ~120 (in wizard model)
auto_categorize = fields.Boolean(
    string='Auto-Categorize',
    default=True,
    help='Automatically detect business domain using AI'
)
```

---

## Graph Visualization Enhancement

### Update Node Colors by Domain

**File**: `ai_sam_memory/static/src/js/memory_graph_renderer.js`

```javascript
// Domain color mapping
const DOMAIN_COLORS = {
    'sales': '#3498db',        // Blue
    'marketing': '#2ecc71',    // Green
    'development': '#e74c3c',  // Red/Orange
    'operations': '#9b59b6',   // Purple
    'strategy': '#f39c12',     // Orange
    'finance': '#1abc9c',      // Teal
    'hr': '#e67e22',           // Dark Orange
    'support': '#34495e',      // Dark Gray
    'product': '#16a085',      // Dark Teal
    'uncategorized': '#95a5a6' // Light Gray
};

// Modify renderNode function
renderNode(node) {
    const domain = node.business_domain || 'uncategorized';

    return {
        id: node.id,
        label: node.name,
        title: `${node.name}\nDomain: ${domain}\nMessages: ${node.message_count}`,
        color: {
            background: DOMAIN_COLORS[domain],
            border: this.darkenColor(DOMAIN_COLORS[domain]),
            highlight: {
                background: this.lightenColor(DOMAIN_COLORS[domain]),
                border: DOMAIN_COLORS[domain]
            }
        },
        group: domain,  // vis.js will cluster by this
        size: Math.min(10 + (node.message_count * 0.5), 50),
    };
}
```

### Add Domain Legend

```javascript
// Add visual legend to graph
createDomainLegend() {
    const legend = document.createElement('div');
    legend.className = 'domain-legend';
    legend.innerHTML = `
        <h4>Business Domains</h4>
        ${Object.entries(DOMAIN_COLORS).map(([domain, color]) => `
            <div class="legend-item">
                <span class="legend-color" style="background: ${color}"></span>
                <span class="legend-label">${domain}</span>
            </div>
        `).join('')}
    `;
    return legend;
}
```

---

## User Interface

### 1. Bulk Categorization Wizard

**New File**: `ai_brain/wizards/ai_bulk_categorize_wizard.py`

```python
class AIBulkCategorizeWizard(models.TransientModel):
    _name = 'ai.bulk.categorize.wizard'
    _description = 'Bulk Categorize Conversations'

    mode = fields.Selection([
        ('all', 'All Uncategorized'),
        ('selected', 'Selected Conversations'),
    ], default='all', required=True)

    conversation_ids = fields.Many2many('ai.conversation')
    limit = fields.Integer('Limit', default=100)

    def action_categorize(self):
        categorization = self.env['ai.categorization.service']

        if self.mode == 'selected':
            result = categorization.bulk_categorize(self.conversation_ids.ids)
        else:
            result = categorization.bulk_categorize(limit=self.limit)

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Categorization Complete',
                'message': f"✅ {result['success']} categorized, ❌ {result['failed']} failed",
                'type': 'success',
            }
        }
```

### 2. Conversation Form View

Add domain field to conversation form:

```xml
<!-- After conversation_type field -->
<field name="business_domain"
       widget="badge"
       decoration-info="business_domain == 'development'"
       decoration-success="business_domain == 'sales'"
       decoration-warning="business_domain == 'marketing'"/>
<field name="domain_confidence"
       widget="progressbar"
       invisible="domain_confidence == 0"/>
```

---

## Menu Structure

```
SAM AI
└── Configuration
    ├── Import Conversations (existing)
    ├── Bulk Categorize Conversations (NEW)
    └── Domain Management (NEW)
```

---

## Implementation Plan

### Phase 1: Database (Week 1)
1. ✅ Add business_domain field
2. ✅ Add domain_confidence field
3. ✅ Create domain tag model
4. ✅ Upgrade module

### Phase 2: AI Service (Week 2)
1. ✅ Create categorization service
2. ✅ Test prompt engineering
3. ✅ Add bulk categorization
4. ✅ Integrate with import wizard

### Phase 3: Visualization (Week 3)
1. ✅ Update graph colors
2. ✅ Add domain legend
3. ✅ Add domain filter
4. ✅ Test clustering

### Phase 4: UI Polish (Week 4)
1. ✅ Add bulk categorize wizard
2. ✅ Add domain management UI
3. ✅ Add domain analytics
4. ✅ Documentation

---

## Expected Results

### Before Categorization
```
Graph: All nodes gray, semantic connections only
Filter: None
Organization: Flat
```

### After Categorization
```
Graph: Color-coded by domain, visual clusters
Filter: "Show only Development conversations"
Organization: Hierarchical (domain → topics → conversations)

Example:
┌─ Development (Red Cluster) ────────┐
│ • Odoo architecture (125 chunks)   │
│ • Python debugging (45 chunks)     │
│ • Database schema (78 chunks)      │←─ Semantic connections
└────────────────────────────────────┘

┌─ Sales (Blue Cluster) ─────────────┐
│ • Pricing strategy (32 chunks)     │
│ • Lead generation (28 chunks)      │←─ Semantic connections
│ • Sales funnel (41 chunks)         │
└────────────────────────────────────┘
```

---

## Performance Considerations

### AI Categorization Cost
- **Per conversation**: ~$0.001 (Claude Haiku)
- **232 conversations**: ~$0.23
- **Time**: ~5-10 seconds per conversation
- **Total**: ~20-40 minutes for 232 conversations

### Optimization
1. Cache categorizations (don't re-categorize)
2. Batch API calls (5 conversations per call)
3. Use cheaper model for initial categorization
4. Allow manual override

---

## Success Metrics

1. **Accuracy**: >85% of conversations correctly categorized
2. **Coverage**: >90% of conversations categorized (not 'uncategorized')
3. **User Satisfaction**: Users can find conversations 50% faster
4. **Graph Clarity**: Visual clusters clearly distinguishable

---

## Next Steps

After embedding generation completes:
1. Review this design
2. Implement Phase 1 (database changes)
3. Test categorization service
4. Enhance graph visualization

---

**Status**: Design Complete ✅
**Ready for Implementation**: After embeddings complete (currently 87/232)
