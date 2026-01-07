# The SAM AI SaaS Onboarding Experience

## Philosophy

> **"Our biggest competitor is CONFUSION in the buyer's mind."**

SAM AI's onboarding is designed to eliminate confusion by progressively revealing features only after the user has been trained to use them. This "simplify to amplify" approach ensures users aren't overwhelmed by Odoo's 600+ apps on day one.

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│  MAIN SITE (sme.ec)                                         │
│  ├── Marketing website                                      │
│  ├── eLearning: "30 Steps To Success"                       │
│  ├── User signup / payment                                  │
│  └── Central user database (tracks training progress)       │
└─────────────────────────────────────────────────────────────┘
                           │
                           │ Webhook/API: "User completed Step X"
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  SAAS CLIENT INSTANCE (client1.samai.software)              │
│  ├── ai_sam (SAM AI chat) ← Always visible                  │
│  ├── ai_sam_base ← Always visible                           │
│  ├── CRM ← Unlocks after Step 10                            │
│  ├── Sales ← Unlocks after Step 15                          │
│  └── Invoicing ← Unlocks after Step 20                      │
└─────────────────────────────────────────────────────────────┘
```

---

## The User Journey

### Step 1: Signup on sme.ec

User visits the main website, signs up, and begins the "30 Steps To Your Success" eLearning course.

```
User signs up on sme.ec
└── Creates account
└── Starts "30 Steps" course
└── Credentials stored in central database
```

### Step 2: SaaS Instance Created

The Webkul SaaS Kit automatically provisions their own Odoo instance.

```
SaaS Kit creates their instance (client1.samai.software)
└── ai_sam_client_onboarding module installed
└── User auto-logged in (credentials from signup)
└── Only SAM AI + ai_sam_base visible
└── Clean, uncluttered interface
```

### Step 3: Progressive Unlocking

As the user completes training stages on sme.ec, their SaaS instance unlocks new features.

```
User completes Stage 1 on sme.ec
└── Webhook fires to client1.samai.software
└── ai_sam_client_onboarding updates their progress
└── CRM menu unlocks
└── User notified: "You've unlocked CRM!"
```

### Step 4: Continued Growth

Each stage reveals more of Odoo's power, but only when the user is ready.

```
User logs into their instance
└── Sees SAM AI + CRM (newly unlocked)
└── Dashboard shows "Stage 1 Complete! 29 more to go"
└── Clear path forward, no confusion
```

---

## Progressive Feature Unlock Schedule

| Training Stage | What Unlocks | Estimated Timeline |
|----------------|--------------|-------------------|
| Signup | SAM AI Chat, ai_sam_base | Day 1 |
| Stage 1 (Steps 1-5) | CRM Basics (Contacts) | Week 1 |
| Stage 2 (Steps 6-10) | CRM Advanced (Leads, Pipeline) | Week 2 |
| Stage 3 (Steps 11-15) | Sales Module | Week 3 |
| Stage 4 (Steps 16-20) | Invoicing Basics | Week 4 |
| Stage 5 (Steps 21-25) | Inventory (if applicable) | Week 5 |
| Stage 6 (Steps 26-30) | Full Access | Week 6+ |

*Note: Timeline is flexible - users can progress faster or slower based on their pace.*

---

## Key Modules

### On Client Instance

| Module | Purpose |
|--------|---------|
| `ai_sam` | SAM AI chat interface - always visible |
| `ai_sam_base` | Core infrastructure - always visible |
| `sam_ui_theme` | Clean UI, hides Odoo clutter |
| `sam_ai_access_manager` | Department-based user permissions |
| `ai_sam_client_onboarding` | **Tracks training progress, unlocks features** |

### On Main Site (sme.ec)

| Module | Purpose |
|--------|---------|
| `website_slides` | Odoo eLearning - hosts "30 Steps" course |
| `odoo_saas_kit` | Provisions client instances |
| Custom webhook module | Notifies client instances of progress |

---

## Technical Implementation

### Shared Authentication ("Collective Sign In")

Users have ONE account that works on:
- sme.ec (training, account management, support)
- Their SaaS instance (actual business system)

This is achieved via:
1. OAuth2/OpenID Connect between instances, OR
2. API-based credential sync at instance creation

### Training Progress Sync

```
sme.ec                          client1.samai.software
   │                                      │
   │  User completes lesson               │
   │  ─────────────────────────────────►  │
   │  POST /api/onboarding/progress       │
   │  {user_id, stage: 5, completed: true}│
   │                                      │
   │                              ai_sam_client_onboarding
   │                              updates user record
   │                              triggers menu refresh
   │                              shows unlock notification
```

### Menu Visibility Control

The `ai_sam_client_onboarding` module overrides Odoo's menu visibility:

```python
class OnboardingProgress(models.Model):
    _name = 'onboarding.progress'

    user_id = fields.Many2one('res.users')
    current_stage = fields.Integer(default=0)

    def get_visible_menus(self):
        """Return menu IDs user can see based on their stage"""
        stage = self.current_stage
        visible = ['ai_sam', 'ai_sam_base']  # Always visible

        if stage >= 1:
            visible.append('crm')
        if stage >= 2:
            visible.append('sale')
        if stage >= 3:
            visible.append('account')
        # ... etc

        return visible
```

---

## Benefits of This Approach

### For Users
- No overwhelm on day one
- Clear progression path
- Training tied to actual features they'll use
- Confidence builds with each unlock

### For SAM AI Business
- Higher activation rates (users don't abandon due to confusion)
- Better trained users = fewer support tickets
- Natural upsell path (unlock more = see more value)
- Engagement metrics via training completion

### For Reducing Confusion
- Only see what you know how to use
- "Bright shiny objects" hidden until appropriate
- Guided journey, not a maze
- SAM AI as companion throughout

---

## Phase Implementation

### Phase 1: Basic SaaS (Current)
- Docker image with core SAM AI modules
- SaaS Kit configured on Hetzner
- Manual client creation

### Phase 2: Onboarding Module
- Build `ai_sam_client_onboarding`
- Webhook integration with sme.ec
- Progressive menu unlocking

### Phase 3: Full Automation
- Signup → Instance creation → Auto-login
- Training progress sync
- Unlock notifications
- Progress dashboard

---

## Related Documentation

- [SaaS Kit Setup Guide](../saas_kit_setup.md)
- [Docker Image Build](../docker_build.md)
- [Module Dependencies](../module_dependencies.md)

---

*Document Version: 1.0*
*Last Updated: 2026-01-05*
*Author: SAM AI Development Team*
