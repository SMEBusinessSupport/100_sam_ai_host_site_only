# SAM AI License Management - Technical Design

## Overview

A subscription-based module licensing system for SAM AI addons. Modules are enabled/disabled based on real-time payment status.

---

## Core Concept

**Free Core:**
- `ai_sam_intelligence` (always accessible)
- `ai_sam_chat` (always accessible)
- `base`, `web`, `mail` (Odoo core)

**Paid Addons (Subscription):**
- `ai_sam_lead_generator` (€29/month)
- `ai_sam_workflows` (€49/month)
- `ai_sam_advanced_crm` (€79/month)
- **Package Deals:** All addons (€99/month)

**Licensing:** API-based validation with 7-day grace period.

---

## Technical Implementation

### Module 1: `ai_sam_license` (Core License Manager)

**Location:** `ai_sam/ai_sam_license/`

**Purpose:**
- Check licensing server every 24 hours
- Enable/disable addon modules based on subscription status
- Show subscription status in UI

**Key Files:**

#### `models/license_manager.py`
```python
from odoo import models, fields, api
import requests
from datetime import datetime, timedelta

class LicenseManager(models.Model):
    _name = 'samai.license'
    _description = 'SAM AI License Manager'

    # License details
    license_key = fields.Char(string='License Key', required=True)
    instance_id = fields.Char(string='Instance ID', readonly=True, default=lambda self: self._generate_instance_id())

    # Status
    status = fields.Selection([
        ('active', 'Active'),
        ('grace', 'Grace Period'),
        ('expired', 'Expired'),
        ('invalid', 'Invalid')
    ], default='invalid', readonly=True)

    last_check = fields.Datetime(string='Last Validation', readonly=True)
    next_check = fields.Datetime(string='Next Validation', readonly=True)
    grace_until = fields.Datetime(string='Grace Period Until', readonly=True)

    # Subscription info
    customer_email = fields.Char(string='Customer Email', readonly=True)
    subscription_tier = fields.Selection([
        ('free', 'Free'),
        ('starter', 'Starter - €29/mo'),
        ('professional', 'Professional - €79/mo'),
        ('enterprise', 'Enterprise - €149/mo')
    ], readonly=True)

    # Enabled modules
    enabled_modules = fields.Text(string='Enabled Modules', readonly=True)

    # API settings
    LICENSE_API_URL = 'https://license.samai.io/api/v1/validate'
    GRACE_PERIOD_DAYS = 7

    def _generate_instance_id(self):
        """Generate unique instance identifier"""
        import uuid
        return str(uuid.uuid4())

    @api.model
    def validate_license(self, force=False):
        """
        Validate license with SAM AI licensing server
        Called automatically every 24 hours via cron job
        """
        license_record = self.search([], limit=1)

        if not license_record:
            # No license configured
            return {'status': 'invalid', 'modules': []}

        # Check if validation is due
        now = fields.Datetime.now()
        if not force and license_record.next_check and now < license_record.next_check:
            # Not time to validate yet
            return {'status': license_record.status, 'modules': self._parse_enabled_modules(license_record.enabled_modules)}

        # Call licensing API
        try:
            response = requests.post(
                self.LICENSE_API_URL,
                json={
                    'license_key': license_record.license_key,
                    'instance_id': license_record.instance_id,
                    'odoo_version': self.env['ir.module.module'].get_odoo_version()
                },
                timeout=10
            )

            if response.status_code == 200:
                data = response.json()

                # Update license record
                license_record.write({
                    'status': data.get('status', 'invalid'),
                    'customer_email': data.get('customer_email'),
                    'subscription_tier': data.get('subscription_tier'),
                    'enabled_modules': ','.join(data.get('modules', [])),
                    'last_check': now,
                    'next_check': now + timedelta(hours=24),
                    'grace_until': fields.Datetime.from_string(data.get('grace_until')) if data.get('grace_until') else None
                })

                # Enable/disable modules
                self._apply_module_access(data.get('modules', []))

                return {'status': data.get('status'), 'modules': data.get('modules', [])}

            else:
                # API error, enter grace period
                return self._enter_grace_period(license_record)

        except requests.exceptions.RequestException as e:
            # Network error, enter grace period
            return self._enter_grace_period(license_record)

    def _enter_grace_period(self, license_record):
        """Enter grace period if API is unreachable"""
        now = fields.Datetime.now()

        if not license_record.grace_until:
            # Start grace period
            grace_until = now + timedelta(days=self.GRACE_PERIOD_DAYS)
            license_record.write({
                'status': 'grace',
                'grace_until': grace_until,
                'last_check': now,
                'next_check': now + timedelta(hours=24)
            })
            return {'status': 'grace', 'modules': self._parse_enabled_modules(license_record.enabled_modules)}

        elif now > license_record.grace_until:
            # Grace period expired
            license_record.write({
                'status': 'expired',
                'last_check': now,
                'next_check': now + timedelta(hours=24)
            })
            self._disable_all_paid_modules()
            return {'status': 'expired', 'modules': []}

        else:
            # Still in grace period
            return {'status': 'grace', 'modules': self._parse_enabled_modules(license_record.enabled_modules)}

    def _parse_enabled_modules(self, modules_string):
        """Parse comma-separated module names"""
        if not modules_string:
            return []
        return [m.strip() for m in modules_string.split(',') if m.strip()]

    def _apply_module_access(self, allowed_modules):
        """Enable/disable modules based on subscription"""
        ModuleObj = self.env['ir.module.module']

        # All paid SAM AI modules
        paid_modules = [
            'ai_sam_lead_generator',
            'ai_sam_workflows',
            'ai_sam_advanced_crm',
            'ai_sam_analytics',
            'ai_sam_automation'
        ]

        for module_name in paid_modules:
            module = ModuleObj.search([('name', '=', module_name)], limit=1)

            if not module:
                continue

            if module_name in allowed_modules:
                # Enable module
                if module.state in ['uninstalled', 'to install']:
                    module.button_immediate_install()
            else:
                # Disable module
                if module.state == 'installed':
                    module.button_immediate_uninstall()

    def _disable_all_paid_modules(self):
        """Disable all paid modules (subscription expired)"""
        self._apply_module_access([])

    @api.model
    def get_subscription_status(self):
        """Get current subscription status for UI"""
        license_record = self.search([], limit=1)

        if not license_record:
            return {
                'status': 'no_license',
                'message': 'No license configured. Click to activate.',
                'color': 'danger'
            }

        status_map = {
            'active': {'message': 'Subscription Active', 'color': 'success'},
            'grace': {'message': f'Grace Period (until {license_record.grace_until})', 'color': 'warning'},
            'expired': {'message': 'Subscription Expired - Renew Now', 'color': 'danger'},
            'invalid': {'message': 'Invalid License Key', 'color': 'danger'}
        }

        return {
            'status': license_record.status,
            'tier': license_record.subscription_tier,
            'email': license_record.customer_email,
            'modules': self._parse_enabled_modules(license_record.enabled_modules),
            **status_map.get(license_record.status, {})
        }
```

#### `data/cron_jobs.xml`
```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <!-- Cron job: Validate license every 24 hours -->
    <record id="cron_validate_license" model="ir.cron">
        <field name="name">SAM AI: Validate License</field>
        <field name="model_id" ref="model_samai_license"/>
        <field name="state">code</field>
        <field name="code">model.validate_license()</field>
        <field name="interval_number">1</field>
        <field name="interval_type">days</field>
        <field name="numbercall">-1</field>
        <field name="active" eval="True"/>
    </record>
</odoo>
```

#### `views/license_views.xml`
```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <!-- License Configuration Form -->
    <record id="view_samai_license_form" model="ir.ui.view">
        <field name="name">samai.license.form</field>
        <field name="model">samai.license</field>
        <field name="arch" type="xml">
            <form string="SAM AI License">
                <sheet>
                    <div class="oe_title">
                        <h1>
                            <field name="license_key" placeholder="Enter your license key..."/>
                        </h1>
                    </div>

                    <group>
                        <group string="Subscription Info">
                            <field name="status" widget="badge"/>
                            <field name="subscription_tier"/>
                            <field name="customer_email"/>
                        </group>

                        <group string="Validation">
                            <field name="last_check"/>
                            <field name="next_check"/>
                            <field name="grace_until" attrs="{'invisible': [('status', '!=', 'grace')]}"/>
                        </group>
                    </group>

                    <group string="Enabled Modules">
                        <field name="enabled_modules" readonly="1"/>
                    </group>

                    <group string="Instance Info">
                        <field name="instance_id" readonly="1"/>
                    </group>

                    <footer>
                        <button name="validate_license" type="object" string="Validate Now" class="btn-primary"/>
                        <button string="Upgrade Subscription" type="object" name="open_upgrade_portal" class="btn-secondary"/>
                    </footer>
                </sheet>
            </form>
        </field>
    </record>

    <!-- Menu Item -->
    <menuitem id="menu_samai_license"
              name="License"
              parent="base.menu_administration"
              action="action_samai_license"
              sequence="99"/>
</odoo>
```

---

## Module 2: License Enforcement Decorator

**Purpose:** Wrap addon functionality to check license before execution

#### `models/license_decorator.py`
```python
from odoo import api
from functools import wraps

def requires_license(module_name):
    """
    Decorator to enforce license for module methods

    Usage:
        @requires_license('ai_sam_lead_generator')
        def generate_leads(self):
            # This code only runs if module is licensed
            pass
    """
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            # Check if module is licensed
            license_manager = self.env['samai.license']
            status = license_manager.validate_license()

            if module_name not in status.get('modules', []):
                raise UserError(
                    f"Module '{module_name}' requires an active subscription.\n\n"
                    f"Current status: {status.get('status')}\n\n"
                    f"Please upgrade your subscription at: https://samai.io/pricing"
                )

            # License valid, execute function
            return func(self, *args, **kwargs)

        return wrapper
    return decorator
```

**Usage in Protected Modules:**

```python
# In ai_sam_lead_generator/models/lead_generator.py

from odoo import models
from odoo.addons.ai_sam_license.models.license_decorator import requires_license

class LeadGenerator(models.Model):
    _name = 'samai.lead.generator'

    @requires_license('ai_sam_lead_generator')
    def scrape_leads(self, url):
        """This method only works with active subscription"""
        # Protected functionality
        pass
```

---

## Licensing Server API

### Endpoint: `POST /api/v1/validate`

**Request:**
```json
{
  "license_key": "SAMAI-1234-5678-ABCD",
  "instance_id": "550e8400-e29b-41d4-a716-446655440000",
  "odoo_version": "18.0"
}
```

**Response (Active Subscription):**
```json
{
  "status": "active",
  "customer_email": "customer@example.com",
  "subscription_tier": "professional",
  "modules": [
    "ai_sam_lead_generator",
    "ai_sam_workflows",
    "ai_sam_advanced_crm"
  ],
  "grace_until": null
}
```

**Response (Expired):**
```json
{
  "status": "expired",
  "customer_email": "customer@example.com",
  "subscription_tier": "free",
  "modules": [],
  "grace_until": null,
  "message": "Subscription expired. Please renew at https://samai.io/billing"
}
```

---

## Payment Integration (Stripe)

### Webhook Handler

When Stripe sends payment events:

```python
# licensing_server/webhooks.py

@app.route('/webhooks/stripe', methods=['POST'])
def stripe_webhook():
    payload = request.data
    sig_header = request.headers.get('Stripe-Signature')

    event = stripe.Webhook.construct_event(
        payload, sig_header, STRIPE_WEBHOOK_SECRET
    )

    if event.type == 'invoice.paid':
        # Payment successful - activate subscription
        subscription_id = event.data.object.subscription
        activate_license(subscription_id)

    elif event.type == 'invoice.payment_failed':
        # Payment failed - start grace period
        subscription_id = event.data.object.subscription
        start_grace_period(subscription_id, days=7)

    elif event.type == 'customer.subscription.deleted':
        # Subscription cancelled - revoke license
        subscription_id = event.data.object.id
        revoke_license(subscription_id)

    return {'status': 'success'}
```

---

## User Experience Flow

### First-Time Setup:
1. User installs SAM AI (free core)
2. Wants to use Lead Generator addon
3. Clicks module → Gets license prompt
4. Redirected to https://samai.io/pricing
5. Pays for subscription → Gets license key
6. Enters license key in Odoo
7. Modules unlock instantly

### Subscription Renewal:
1. Stripe auto-charges monthly
2. If payment succeeds → No interruption
3. If payment fails:
   - Day 1-7: Grace period (modules still work)
   - Day 8+: Modules disabled, user gets notification
   - User updates payment → Modules re-enable immediately

### Module Access:
```
User clicks "Generate Leads" button
  ↓
Odoo checks: Is ai_sam_lead_generator licensed?
  ↓
YES → Function executes
NO  → Show upgrade dialog
```

---

## Implementation Complexity

### Effort Estimate:
- **License Module (`ai_sam_license`):** 2-3 days
- **Licensing Server API:** 2-3 days
- **Stripe Integration:** 1-2 days
- **Testing & Deployment:** 2-3 days
- **Total:** ~1-2 weeks

### Complexity Level: **Medium**

---

## Security Considerations

### Anti-Piracy Measures:
1. ✅ License key tied to instance_id (can't share)
2. ✅ Daily validation (can't use offline forever)
3. ✅ Grace period (prevents accidental disruption)
4. ✅ API rate limiting (prevents brute force)
5. ✅ Encrypted communication (HTTPS only)

### Fail-Safe:
- Grace period ensures temporary API outages don't disrupt customers
- Manual override option for support emergencies

---

## Pricing Tiers (Suggested)

### Free (€0/month):
- SAM AI Chat
- Basic Intelligence
- Community Support

### Starter (€29/month):
- + Lead Generator
- + Basic Workflows
- Email Support

### Professional (€79/month):
- + All Addons
- + Advanced CRM
- + Priority Support

### Enterprise (€149/month):
- + Custom Modules
- + White-label
- + Dedicated Support

---

## Next Steps

1. **Decide:** Is this the right approach for your SaaS model?
2. **Build:** Create `ai_sam_license` module (I can help)
3. **Server:** Set up licensing API (Node.js/Python/PHP)
4. **Stripe:** Integrate payment webhooks
5. **Test:** Verify subscription flow works

**Want me to create the full `ai_sam_license` module code?**
