# Cost Optimization Intelligence System - Implementation Guide

**For Agent:** `/mod_sam`
**Date:** 2025-10-17
**Status:** 🔴 READY TO IMPLEMENT
**Estimated Time:** 3-4 weeks (4 phases)

---

## 🎯 Mission

Transform SAM AI from "Claude API integration" to "Cost-Effective Quality-Based Multi-Provider AI Intelligence"

**Expected Result:** 30-50% cost reduction ($75/month savings on $150 baseline)

---

## 📋 What /mod_sam Needs to Do

### Phase 1: Core Intelligence (Week 1) - START HERE!

#### Task 1.1: Create `ai.cost.optimizer` Model

**File:** `C:\Working With AI\ai_sam\ai_sam\ai_brain\models\ai_cost_optimizer.py`

**Purpose:** Recommend best provider based on cost + quality + context

**Key Methods:**
```python
@api.model
def recommend_provider(self, task_type, context_size_tokens, quality_required='medium', max_budget_usd=None):
    """
    Recommend best provider for task

    Args:
        task_type (str): 'chat', 'voice_to_text', etc.
        context_size_tokens (int): Estimated input tokens
        quality_required (str): 'low', 'medium', 'high'
        max_budget_usd (float): Optional budget constraint

    Returns:
        dict: {
            'provider_id': int,
            'provider_name': str,
            'estimated_cost': float,
            'reasoning': str,
            'alternatives': list,
        }
    """
    # 1. Get all active providers for task_type
    # 2. Calculate cost for each based on context_size_tokens
    # 3. Filter by quality_required
    # 4. Filter by max_budget_usd if provided
    # 5. Rank by cost_per_quality_point
    # 6. Return best match + alternatives
```

**Fields:**
- `name` (Char): Description
- `task_type` (Selection): From ai.service.provider
- `quality_required` (Selection): low/medium/high
- `recommended_provider_id` (Many2one): ai.service.provider
- `estimated_cost_usd` (Float): Cost estimate
- `reasoning` (Text): Why this provider
- `created_at` (Datetime): When recommendation made
- `user_id` (Many2one): res.users

**Business Logic:**
- Query `ai.provider.benchmark` for historical performance
- Calculate cost based on provider pricing + context_size
- Filter by quality threshold (from benchmarks)
- Return best cost/quality ratio

---

#### Task 1.2: Create `ai.token.analytics` Model

**File:** `C:\Working With AI\ai_sam\ai_sam\ai_brain\models\ai_token_analytics.py`

**Purpose:** Analyze token usage patterns and detect waste

**Key Methods:**
```python
@api.model
def analyze_waste(self, token_usage_id):
    """
    Analyze token usage for waste

    Returns:
        dict: {
            'waste_detected': bool,
            'waste_score': int (0-100),
            'findings': list of dicts,
            'potential_savings_usd': float,
        }
    """
    usage = self.env['ai.token.usage'].browse(token_usage_id)

    findings = []

    # Rule 1: Redundant Context
    if self._detect_redundant_context(usage):
        findings.append({
            'type': 'redundant_context',
            'description': 'Context included unused models',
            'tokens_wasted': ...,
            'recommendation': 'Use selective context'
        })

    # Rule 2: Duplicate Query
    if self._detect_duplicate_query(usage):
        findings.append({...})

    # Rule 3: Oversized Context
    # Rule 4: Wrong Model
    # Rule 5: Unnecessary History

    return {
        'waste_detected': len(findings) > 0,
        'waste_score': self._calculate_waste_score(findings),
        'findings': findings,
        'potential_savings_usd': sum([f['cost_wasted'] for f in findings]),
    }

@api.model
def get_cost_breakdown(self, period_type='month', user_id=None):
    """
    Get cost breakdown by module, context_model, user

    Returns:
        dict: {
            'total_cost': float,
            'by_module': {...},
            'by_context': {...},
            'by_user': {...},
            'trends': {...},
        }
    """
```

**Fields:**
- `name` (Char): Analytics period
- `period_start` (Date)
- `period_end` (Date)
- `total_tokens` (Integer)
- `total_cost_usd` (Float)
- `waste_detected_count` (Integer)
- `potential_savings_usd` (Float)
- `top_cost_driver` (Char): e.g., "context_builder"
- `recommendations` (Text): JSON list of recommendations

---

#### Task 1.3: Enhance `ai.service` Model

**File:** `C:\Working With AI\ai_sam\ai_sam\ai_brain\models\ai_service.py`

**Changes:**

1. **Add method: `_recommend_provider_before_call()`**
```python
def _recommend_provider_before_call(self, config, messages, environment):
    """Get provider recommendation before API call"""

    # Estimate tokens
    token_count = self._count_tokens_api(config, messages)
    input_tokens = token_count.get('input_tokens', 0)

    # Get recommendation
    CostOptimizer = self.env['ai.cost.optimizer']
    recommendation = CostOptimizer.recommend_provider(
        task_type='chat',
        context_size_tokens=input_tokens,
        quality_required='medium',  # Could be from config
    )

    _logger.info(f"💡 Recommended: {recommendation['provider_name']} (${recommendation['estimated_cost']:.4f})")

    return recommendation
```

2. **Add method: `_analyze_waste_after_call()`**
```python
def _analyze_waste_after_call(self, token_usage_id):
    """Analyze token usage for waste"""

    TokenAnalytics = self.env['ai.token.analytics']
    waste_report = TokenAnalytics.analyze_waste(token_usage_id)

    if waste_report['waste_detected']:
        _logger.warning(f"💸 Waste detected: ${waste_report['potential_savings_usd']:.4f} could have been saved")
        _logger.warning(f"   Reason: {waste_report['findings'][0]['description']}")

    return waste_report
```

3. **Modify `send_message()` to include cost optimization**
```python
# In send_message() method, after line ~456 (token preview):

# COST OPTIMIZATION: Get provider recommendation
if config.enable_cost_optimization:  # New config flag
    recommendation = self._recommend_provider_before_call(config, messages, environment)

    # Could switch provider here if configured
    if config.auto_switch_provider and recommendation['provider_id'] != config.id:
        _logger.info(f"🔄 Auto-switching to {recommendation['provider_name']} for cost optimization")
        # Use recommended provider instead

# ... after API call and token logging (line ~540) ...

# COST OPTIMIZATION: Analyze waste
if config.enable_waste_detection:  # New config flag
    waste_report = self._analyze_waste_after_call(token_usage.id)
    response['waste_report'] = waste_report
```

---

#### Task 1.4: Enhance `ai.token.usage` Model

**File:** `C:\Working With AI\ai_sam\ai_sam\ai_brain\models\ai_token_usage.py`

**Add Fields:**
```python
# Waste Detection
waste_detected = fields.Boolean(
    string='Waste Detected',
    default=False,
    help='True if token waste was detected'
)

waste_reason = fields.Text(
    string='Waste Reason',
    help='Description of why tokens were wasted'
)

could_have_saved_usd = fields.Float(
    string='Could Have Saved (USD)',
    digits=(12, 6),
    help='Estimated savings if optimized'
)

optimization_score = fields.Integer(
    string='Optimization Score',
    help='0-100, higher = more efficient token usage'
)

# Context Analysis
context_size_tokens = fields.Integer(
    string='Context Size (tokens)',
    help='Size of context in tokens'
)

context_type = fields.Selection([
    ('full', 'Full Context'),
    ('selective', 'Selective Context'),
    ('minimal', 'Minimal Context'),
], string='Context Type')
```

**Add Method:**
```python
def analyze_waste(self):
    """Analyze this usage record for waste"""
    self.ensure_one()

    TokenAnalytics = self.env['ai.token.analytics']
    waste_report = TokenAnalytics.analyze_waste(self.id)

    if waste_report['waste_detected']:
        self.write({
            'waste_detected': True,
            'waste_reason': waste_report['findings'][0]['description'],
            'could_have_saved_usd': waste_report['potential_savings_usd'],
            'optimization_score': 100 - waste_report['waste_score'],
        })
    else:
        self.write({
            'optimization_score': 100,
        })

    return waste_report
```

---

#### Task 1.5: Update Security Rules

**File:** `C:\Working With AI\ai_sam\ai_sam\ai_brain\security\ir.model.access.csv`

Add lines:
```csv
access_ai_cost_optimizer_user,AI Cost Optimizer User,model_ai_cost_optimizer,base.group_user,1,0,0,0
access_ai_cost_optimizer_manager,AI Cost Optimizer Manager,model_ai_cost_optimizer,base.group_system,1,1,1,1
access_ai_token_analytics_user,AI Token Analytics User,model_ai_token_analytics,base.group_user,1,0,0,0
access_ai_token_analytics_manager,AI Token Analytics Manager,model_ai_token_analytics,base.group_system,1,1,1,1
```

---

#### Task 1.6: Run QA Tool

```bash
cd "C:\Working With AI\ai_sam\ai_sam"
python ..\ai_toolbox\ai_sam_odoo_dev_qa.py
```

**Required Score:** ≥8/10

**If Failed:** Fix CRITICAL and HIGH issues, re-run until passing

---

#### Task 1.7: Update BUILD_HISTORY.md

After implementation, add entry:
```markdown
### 2025-10-XX: Phase 1 - Core Cost Optimization Intelligence

**Context:** Strategic pivot to cost-effective multi-provider AI

**Changes:**
- Created `ai.cost.optimizer` model (provider recommendation)
- Created `ai.token.analytics` model (waste detection)
- Enhanced `ai.service` with cost optimization hooks
- Enhanced `ai.token.usage` with waste tracking fields
- Added security rules for new models

**Impact:**
- Provider recommendations based on cost + quality
- Real-time waste detection
- Estimated savings: $30/month

**Status:** ✅ COMPLETED (Phase 1 of 4)
```

---

### Phase 2: Provider Benchmarking (Week 2)

#### Task 2.1: Create `ai.provider.benchmark` Model

**File:** `C:\Working With AI\ai_sam\ai_sam\ai_brain\models\ai_provider_benchmark.py`

**Purpose:** Track provider performance over time

**Fields:**
- `provider_id` (Many2one): ai.service.provider
- `task_type` (Selection): chat, voice_to_text, etc.
- `task_complexity` (Selection): low, medium, high
- `input_tokens` (Integer)
- `output_tokens` (Integer)
- `cost_usd` (Float)
- `response_time_ms` (Integer)
- `quality_score` (Integer): 0-100
- `error_occurred` (Boolean)
- `timestamp` (Datetime)
- `user_id` (Many2one)

**Key Methods:**
```python
@api.model
def log_benchmark(self, provider_id, task_type, ...):
    """Log benchmark data after API call"""

@api.model
def compare_providers(self, task_type, period_days=30):
    """Compare providers for task type"""
    # Return cost, quality, speed comparison

@api.model
def get_ab_test_group(self, task_type):
    """Get A/B test group for provider comparison"""
```

---

### Phase 3: Budget Management (Week 3)

#### Task 3.1: Create `ai.cost.budget` Model

**File:** `C:\Working With AI\ai_sam\ai_sam\ai_brain\models\ai_cost_budget.py`

**Purpose:** Budget tracking and alerts

**Fields:**
- `name` (Char)
- `period_type` (Selection): daily, weekly, monthly
- `budget_amount` (Float)
- `current_spend` (Float, computed)
- `percentage_used` (Float, computed)
- `alert_thresholds` (Char): JSON list of thresholds
- `auto_switch_at_threshold` (Integer)
- `block_at_threshold` (Integer)
- `forecast_monthly` (Float, computed)

**Key Methods:**
```python
def check_budget(self):
    """Check if budget allows API call"""

def send_alert(self, threshold):
    """Send budget alert to user"""

def forecast(self):
    """Forecast spending based on trends"""
```

---

### Phase 4: Dashboard & UI (Week 4)

#### Task 4.1: Create Cost Analytics Dashboard

**File:** `C:\Working With AI\ai_sam\ai_sam\ai_sam\views\ai_cost_dashboard_views.xml`

**Components:**
- Total cost this month
- Cost breakdown by module/context/user
- Waste detection report
- Provider comparison chart
- Budget progress bar
- Optimization recommendations

---

## 📊 Success Metrics

After each phase, verify:

**Phase 1:**
- [ ] Provider recommendations working
- [ ] Waste detection identifying issues
- [ ] QA score ≥8/10
- [ ] Estimated savings: $30/month

**Phase 2:**
- [ ] Provider benchmarking tracking
- [ ] A/B testing framework operational
- [ ] Cost comparison reports accurate
- [ ] Estimated savings: +$20/month

**Phase 3:**
- [ ] Budget alerts firing correctly
- [ ] Auto-switching working
- [ ] Forecasting accurate
- [ ] Estimated savings: +$15/month

**Phase 4:**
- [ ] Dashboard showing real data
- [ ] User can see cost insights
- [ ] Recommendations actionable
- [ ] Estimated savings: +$10/month

**Total Expected Savings:** $75/month (50% reduction!)

---

## 🚀 How to Start

**Step 1:** Invoke `/mod_sam`
```bash
/mod_sam Implement Phase 1 of Cost Optimization Intelligence System
```

**Step 2:** /mod_sam will:
1. Read BUILD_HISTORY.md (see the plan)
2. Read TECHNIQUES.md (see the patterns)
3. Create `ai.cost.optimizer` model
4. Create `ai.token.analytics` model
5. Enhance existing models
6. Update security
7. Run QA tool
8. Update BUILD_HISTORY.md

**Step 3:** Test
```bash
/mod_sam Test cost optimization - run a chat query and verify provider recommendation + waste detection works
```

**Step 4:** Move to Phase 2
```bash
/mod_sam Implement Phase 2 of Cost Optimization Intelligence System
```

---

## 💡 Tips for /mod_sam

1. **Read dev docs first** - BUILD_HISTORY.md has full context
2. **Follow patterns** - TECHNIQUES.md shows code examples
3. **Data in ai_brain** - ALL models go in ai_brain, not ai_sam
4. **Run QA after each phase** - Score must be ≥8/10
5. **Update BUILD_HISTORY.md** - Document what you did
6. **Ask for clarification** - If unclear, ask user before implementing

---

## 🔗 Related Documents

**Dev Docs (READ THESE FIRST):**
- `ai_sam/dev docs/01_BUILD_HISTORY.md` - Strategic pivot detailed here
- `ai_sam/dev docs/03_TECHNIQUES.md` - Cost optimization patterns (Pattern 7)
- `ai_sam/dev docs/02_MODELS_DATA.md` - Existing models reference

**Existing Models (TO ENHANCE):**
- `ai_brain/models/ai_service.py` - Add cost optimization hooks
- `ai_brain/models/ai_token_usage.py` - Add waste tracking fields
- `ai_brain/models/ai_service_provider.py` - Already supports multi-provider

**Shared Foundation (CONTEXT):**
- `~/.claude/agents/recruiter/sam_ai_foundation.md` - Architecture
- `~/.claude/agents/recruiter/odoo_18_tech_stack.md` - Odoo 18 requirements
- `~/.claude/agents/recruiter/qa_integration_protocol.md` - QA workflow

---

## ✅ Final Checklist

Before marking Phase 1 complete:

- [ ] `ai_cost_optimizer.py` created with `recommend_provider()` method
- [ ] `ai_token_analytics.py` created with `analyze_waste()` method
- [ ] `ai_service.py` enhanced with cost optimization hooks
- [ ] `ai_token_usage.py` enhanced with waste detection fields
- [ ] Security rules updated (`ir.model.access.csv`)
- [ ] QA tool run (score ≥8/10)
- [ ] BUILD_HISTORY.md updated with Phase 1 completion
- [ ] Tested with real chat query
- [ ] Provider recommendation working
- [ ] Waste detection working
- [ ] User can see cost insights in response

**When complete:** Move to Phase 2!

---

**Status:** 🔴 READY - Waiting for /mod_sam to implement

**Estimated Time:** 1 week per phase (4 weeks total)

**Expected ROI:** $75/month savings = pays for itself immediately!

---

**Questions?** Ask `/cos` or read the dev docs!

**Ready to start?** Invoke `/mod_sam` with Phase 1 task!

---

**End of Implementation Guide** ✅
