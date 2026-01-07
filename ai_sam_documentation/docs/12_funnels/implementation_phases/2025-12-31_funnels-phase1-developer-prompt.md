# Developer Prompt: SAM AI Funnels - Phase 1 (Foundation)

**Date:** 2025-12-31
**Phase:** 1 of 7
**Scope:** Module skeleton, core models, basic views, security

---

## CONTEXT

You are implementing Phase 1 of the SAM AI Funnels module. This module adds a "FUNNELS" tab to Odoo 18's website builder, enabling drag-and-drop sales funnel creation with SAM AI integration.

**Architecture Document:** `D:\SAMAI-18-SaaS\ai_sam\ai_sam_docs\plans\2025-12-31_sam-ai-funnels-architecture.md`

**Requirements Document:** `D:\SAMAI-18-SaaS\The SAM Sales System\Gold Star Direction\FUNNELS-TAB-REQUIREMENTS.md`

---

## GOAL

Create the foundational module structure with 5 core data models, basic views, menus, and security rules. No snippets or website builder integration yet - that's Phase 2.

---

## MODULE LOCATION

```
D:\SAMAI-18-SaaS\ai_sam\sam_ai_funnels\
```

This is a NEW module in the SAM AI ecosystem, alongside:
- ai_brain (data layer)
- ai_sam (framework)
- ai_sam_workflows (workflow automation)
- etc.

---

## DELIVERABLES

### 1. Module Structure

Create this file structure:

```
sam_ai_funnels/
├── __manifest__.py
├── __init__.py
├── models/
│   ├── __init__.py
│   ├── funnel_definition.py
│   ├── funnel_page.py
│   ├── funnel_template.py
│   ├── funnel_snippet.py
│   └── funnel_conversion.py
├── controllers/
│   ├── __init__.py
│   └── funnel_controller.py      # Placeholder for now
├── views/
│   ├── funnel_definition_views.xml
│   ├── funnel_page_views.xml
│   ├── funnel_template_views.xml
│   ├── funnel_snippet_views.xml
│   └── funnel_menus.xml
├── data/
│   └── funnel_snippet_data.xml   # Initial snippet registry
├── static/
│   └── description/
│       └── icon.png              # Copy from ai_sam module
└── security/
    └── ir.model.access.csv
```

### 2. __manifest__.py

```python
{
    'name': 'SAM AI Funnels',
    'version': '18.0.1.0.0',
    'category': 'Website',
    'summary': 'Sales funnel builder with SAM AI integration',
    'description': """
SAM AI Funnels - Sales Funnel Builder
=====================================

Adds a FUNNELS tab to the Odoo 18 website builder with:
- 46 drag-and-drop funnel snippets
- 6 complete funnel templates
- Native CRM and mailing integration
- SAM AI powered copy generation

Part of the SAM AI ecosystem.
    """,
    'author': 'Anthony Gardiner - Odoo Consulting & Claude AI',
    'maintainer': 'Anthony Gardiner <anthony@sme.ec>',
    'website': 'https://sme.ec',
    'license': 'LGPL-3',
    'depends': [
        'website',
        'crm',
        'mass_mailing',
        'ai_brain',
        'ai_sam',
    ],
    'data': [
        # Security
        'security/ir.model.access.csv',

        # Views
        'views/funnel_definition_views.xml',
        'views/funnel_page_views.xml',
        'views/funnel_template_views.xml',
        'views/funnel_snippet_views.xml',
        'views/funnel_menus.xml',

        # Data
        'data/funnel_snippet_data.xml',
    ],
    'assets': {
        # Will be added in Phase 2
    },
    'images': ['static/description/icon.png'],
    'installable': True,
    'auto_install': False,
    'application': True,
}
```

### 3. Models

#### models/__init__.py
```python
from . import funnel_definition
from . import funnel_page
from . import funnel_template
from . import funnel_snippet
from . import funnel_conversion
```

#### models/funnel_definition.py
```python
from odoo import models, fields, api


class FunnelDefinition(models.Model):
    _name = 'funnel.definition'
    _description = 'Sales Funnel Definition'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc'

    # Core Identity
    name = fields.Char('Funnel Name', required=True, tracking=True)
    description = fields.Text('Description')
    funnel_type = fields.Selection([
        ('opt_in', 'Simple Opt-in'),
        ('lead_magnet', 'Lead Magnet'),
        ('quiz', 'Quiz Funnel'),
        ('eoi', 'Expression of Interest'),
        ('product_launch', 'Product Launch'),
        ('webinar', 'Webinar'),
        ('custom', 'Custom'),
    ], string='Funnel Type', default='custom', tracking=True)

    # Pages
    page_ids = fields.One2many('funnel.page', 'funnel_id', string='Pages')
    page_count = fields.Integer('Page Count', compute='_compute_page_count', store=True)

    # Template Source
    template_id = fields.Many2one('funnel.template', string='Based on Template')

    # CRM Integration
    crm_team_id = fields.Many2one('crm.team', string='Sales Team')
    default_tag_ids = fields.Many2many('crm.tag', string='Lead Tags')

    # Mailing Integration
    mailing_list_id = fields.Many2one('mailing.list', string='Mailing List')

    # Analytics (computed from conversions)
    total_views = fields.Integer('Total Views', compute='_compute_analytics', store=True)
    total_conversions = fields.Integer('Total Conversions', compute='_compute_analytics', store=True)
    conversion_rate = fields.Float('Conversion Rate (%)', compute='_compute_analytics', store=True)

    # State
    state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('paused', 'Paused'),
        ('archived', 'Archived'),
    ], string='Status', default='draft', tracking=True)

    # SAM AI Integration
    canvas_id = fields.Many2one('canvas', string='Workflow Canvas')
    ai_generated_copy = fields.Boolean('AI Generated Copy', default=False)

    # Company
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company)

    @api.depends('page_ids')
    def _compute_page_count(self):
        for record in self:
            record.page_count = len(record.page_ids)

    @api.depends('page_ids.view_count', 'page_ids.form_submissions')
    def _compute_analytics(self):
        for record in self:
            record.total_views = sum(record.page_ids.mapped('view_count'))
            record.total_conversions = sum(record.page_ids.mapped('form_submissions'))
            record.conversion_rate = (
                (record.total_conversions / record.total_views * 100)
                if record.total_views > 0 else 0.0
            )

    def action_activate(self):
        self.write({'state': 'active'})

    def action_pause(self):
        self.write({'state': 'paused'})

    def action_archive(self):
        self.write({'state': 'archived'})

    def action_draft(self):
        self.write({'state': 'draft'})
```

#### models/funnel_page.py
```python
from odoo import models, fields, api


class FunnelPage(models.Model):
    _name = 'funnel.page'
    _description = 'Funnel Page'
    _order = 'sequence, id'

    # Core Identity
    name = fields.Char('Page Name', required=True)
    funnel_id = fields.Many2one('funnel.definition', string='Funnel', required=True, ondelete='cascade')
    sequence = fields.Integer('Sequence', default=10)

    # Page Type
    page_type = fields.Selection([
        ('squeeze', 'Squeeze Page'),
        ('lead_magnet', 'Lead Magnet Page'),
        ('sales', 'Sales Page'),
        ('order', 'Order/Checkout'),
        ('upsell', 'Upsell Page'),
        ('thank_you', 'Thank You Page'),
        ('quiz_intro', 'Quiz Introduction'),
        ('quiz_questions', 'Quiz Questions'),
        ('quiz_gate', 'Quiz Email Gate'),
        ('quiz_results', 'Quiz Results'),
        ('webinar_registration', 'Webinar Registration'),
        ('webinar_confirmation', 'Webinar Confirmation'),
        ('webinar_replay', 'Webinar Replay'),
        ('custom', 'Custom Page'),
    ], string='Page Type', default='custom')

    # Website Integration
    website_page_id = fields.Many2one('website.page', string='Website Page')
    page_url = fields.Char('URL Slug')
    full_url = fields.Char('Full URL', compute='_compute_full_url')

    # Snippet Configuration (JSON)
    snippet_config = fields.Text('Snippet Configuration', default='[]')

    # Redirect After Action
    next_page_id = fields.Many2one('funnel.page', string='Next Page', domain="[('funnel_id', '=', funnel_id)]")
    redirect_url = fields.Char('External Redirect URL')

    # Analytics
    view_count = fields.Integer('Views', default=0)
    unique_visitors = fields.Integer('Unique Visitors', default=0)
    form_submissions = fields.Integer('Form Submissions', default=0)
    conversion_rate = fields.Float('Conversion Rate (%)', compute='_compute_conversion_rate')

    @api.depends('page_url')
    def _compute_full_url(self):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url', '')
        for record in self:
            if record.page_url:
                record.full_url = f"{base_url}/{record.page_url}"
            elif record.website_page_id:
                record.full_url = f"{base_url}{record.website_page_id.url}"
            else:
                record.full_url = False

    @api.depends('view_count', 'form_submissions')
    def _compute_conversion_rate(self):
        for record in self:
            record.conversion_rate = (
                (record.form_submissions / record.view_count * 100)
                if record.view_count > 0 else 0.0
            )
```

#### models/funnel_template.py
```python
from odoo import models, fields, api
import json


class FunnelTemplate(models.Model):
    _name = 'funnel.template'
    _description = 'Funnel Template'
    _order = 'usage_count desc, name'

    name = fields.Char('Template Name', required=True)
    description = fields.Text('Description')
    funnel_type = fields.Selection([
        ('opt_in', 'Simple Opt-in'),
        ('lead_magnet', 'Lead Magnet'),
        ('quiz', 'Quiz Funnel'),
        ('eoi', 'Expression of Interest'),
        ('product_launch', 'Product Launch'),
        ('webinar', 'Webinar'),
        ('custom', 'Custom'),
    ], string='Funnel Type', required=True)

    # Template Structure (JSON)
    template_structure = fields.Text('Template Structure', default='{"pages": []}')

    # Preview
    thumbnail = fields.Binary('Thumbnail')
    preview_url = fields.Char('Preview URL')

    # Usage Stats
    usage_count = fields.Integer('Times Used', default=0)

    # Visibility
    visibility = fields.Selection([
        ('private', 'Private'),
        ('company', 'Company'),
        ('public', 'Public'),
    ], string='Visibility', default='company')

    # Owner
    author_id = fields.Many2one('res.users', string='Author', default=lambda self: self.env.user)
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company)

    def action_create_funnel_from_template(self):
        """Create new funnel.definition from this template"""
        self.ensure_one()

        # Parse template structure
        structure = json.loads(self.template_structure or '{"pages": []}')

        # Create funnel
        funnel = self.env['funnel.definition'].create({
            'name': f"{self.name} - Copy",
            'description': self.description,
            'funnel_type': self.funnel_type,
            'template_id': self.id,
        })

        # Create pages from template
        for idx, page_spec in enumerate(structure.get('pages', [])):
            self.env['funnel.page'].create({
                'funnel_id': funnel.id,
                'name': page_spec.get('name', f'Page {idx + 1}'),
                'page_type': page_spec.get('page_type', 'custom'),
                'sequence': (idx + 1) * 10,
                'snippet_config': json.dumps(page_spec.get('snippets', [])),
            })

        # Increment usage count
        self.usage_count += 1

        # Return action to open the new funnel
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'funnel.definition',
            'res_id': funnel.id,
            'view_mode': 'form',
            'target': 'current',
        }
```

#### models/funnel_snippet.py
```python
from odoo import models, fields


class FunnelSnippet(models.Model):
    _name = 'funnel.snippet'
    _description = 'Funnel Snippet Definition'
    _order = 'category, sequence, name'

    name = fields.Char('Snippet Name', required=True)
    technical_name = fields.Char('Technical Name', required=True)
    sequence = fields.Integer('Sequence', default=10)

    category = fields.Selection([
        ('complete_funnel', 'Complete Funnels'),
        ('hero', 'Hero Sections'),
        ('problem_story', 'Problem & Story'),
        ('solution_benefits', 'Solution & Benefits'),
        ('social_proof', 'Social Proof'),
        ('offers_pricing', 'Offers & Pricing'),
        ('cta_forms', 'CTAs & Forms'),
        ('quiz', 'Quiz Elements'),
        ('urgency_trust', 'Urgency & Trust'),
        ('utility', 'Utility'),
    ], string='Category', required=True)

    # XML Template Reference
    template_xml_id = fields.Char('XML Template ID')

    # Field Schema (JSON)
    field_schema = fields.Text('Field Schema', default='{"fields": []}')

    # Preview
    thumbnail = fields.Binary('Thumbnail')
    description = fields.Text('Description')

    # SAM AI Knowledge
    copywriting_hints = fields.Text('Copywriting Hints for SAM')

    # Active
    active = fields.Boolean('Active', default=True)
```

#### models/funnel_conversion.py
```python
from odoo import models, fields


class FunnelConversion(models.Model):
    _name = 'funnel.conversion'
    _description = 'Funnel Conversion Event'
    _order = 'timestamp desc'

    # Context
    funnel_id = fields.Many2one('funnel.definition', string='Funnel', required=True, ondelete='cascade')
    page_id = fields.Many2one('funnel.page', string='Page', required=True, ondelete='cascade')

    # Visitor
    visitor_id = fields.Char('Visitor ID')
    partner_id = fields.Many2one('res.partner', string='Contact')

    # Event
    event_type = fields.Selection([
        ('page_view', 'Page View'),
        ('form_submit', 'Form Submission'),
        ('cta_click', 'CTA Click'),
        ('quiz_start', 'Quiz Started'),
        ('quiz_complete', 'Quiz Completed'),
        ('purchase', 'Purchase'),
    ], string='Event Type', required=True)

    # Metadata
    timestamp = fields.Datetime('Timestamp', default=fields.Datetime.now)
    session_data = fields.Text('Session Data')
    user_agent = fields.Char('User Agent')
    ip_address = fields.Char('IP Address')

    # UTM Tracking
    utm_source = fields.Char('UTM Source')
    utm_medium = fields.Char('UTM Medium')
    utm_campaign = fields.Char('UTM Campaign')
    utm_term = fields.Char('UTM Term')
    utm_content = fields.Char('UTM Content')

    # CRM Link
    lead_id = fields.Many2one('crm.lead', string='Created Lead')
```

### 4. Views

#### views/funnel_definition_views.xml
```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <!-- Tree View -->
    <record id="funnel_definition_view_tree" model="ir.ui.view">
        <field name="name">funnel.definition.tree</field>
        <field name="model">funnel.definition</field>
        <field name="arch" type="xml">
            <tree string="Funnels">
                <field name="name"/>
                <field name="funnel_type"/>
                <field name="page_count"/>
                <field name="total_views"/>
                <field name="conversion_rate" widget="progressbar"/>
                <field name="state" widget="badge" decoration-success="state == 'active'" decoration-warning="state == 'paused'" decoration-muted="state == 'draft'"/>
            </tree>
        </field>
    </record>

    <!-- Form View -->
    <record id="funnel_definition_view_form" model="ir.ui.view">
        <field name="name">funnel.definition.form</field>
        <field name="model">funnel.definition</field>
        <field name="arch" type="xml">
            <form string="Funnel">
                <header>
                    <button name="action_activate" string="Activate" type="object" class="btn-primary" invisible="state != 'draft'"/>
                    <button name="action_pause" string="Pause" type="object" invisible="state != 'active'"/>
                    <button name="action_draft" string="Set to Draft" type="object" invisible="state not in ['paused', 'archived']"/>
                    <button name="action_archive" string="Archive" type="object" invisible="state == 'archived'"/>
                    <field name="state" widget="statusbar" statusbar_visible="draft,active,paused,archived"/>
                </header>
                <sheet>
                    <div class="oe_title">
                        <h1>
                            <field name="name" placeholder="Funnel Name"/>
                        </h1>
                    </div>
                    <group>
                        <group>
                            <field name="funnel_type"/>
                            <field name="template_id"/>
                            <field name="ai_generated_copy"/>
                        </group>
                        <group>
                            <field name="crm_team_id"/>
                            <field name="default_tag_ids" widget="many2many_tags"/>
                            <field name="mailing_list_id"/>
                        </group>
                    </group>
                    <group string="Analytics" col="4">
                        <field name="total_views"/>
                        <field name="total_conversions"/>
                        <field name="conversion_rate" widget="progressbar"/>
                        <field name="page_count"/>
                    </group>
                    <notebook>
                        <page string="Pages" name="pages">
                            <field name="page_ids">
                                <tree editable="bottom">
                                    <field name="sequence" widget="handle"/>
                                    <field name="name"/>
                                    <field name="page_type"/>
                                    <field name="page_url"/>
                                    <field name="view_count"/>
                                    <field name="form_submissions"/>
                                    <field name="conversion_rate" widget="progressbar"/>
                                </tree>
                            </field>
                        </page>
                        <page string="Description" name="description">
                            <field name="description" placeholder="Describe this funnel..."/>
                        </page>
                    </notebook>
                </sheet>
                <chatter/>
            </form>
        </field>
    </record>

    <!-- Search View -->
    <record id="funnel_definition_view_search" model="ir.ui.view">
        <field name="name">funnel.definition.search</field>
        <field name="model">funnel.definition</field>
        <field name="arch" type="xml">
            <search string="Search Funnels">
                <field name="name"/>
                <field name="funnel_type"/>
                <filter string="Active" name="active" domain="[('state', '=', 'active')]"/>
                <filter string="Draft" name="draft" domain="[('state', '=', 'draft')]"/>
                <separator/>
                <filter string="AI Generated" name="ai_generated" domain="[('ai_generated_copy', '=', True)]"/>
                <group expand="0" string="Group By">
                    <filter string="Type" name="group_type" context="{'group_by': 'funnel_type'}"/>
                    <filter string="Status" name="group_state" context="{'group_by': 'state'}"/>
                </group>
            </search>
        </field>
    </record>

    <!-- Action -->
    <record id="funnel_definition_action" model="ir.actions.act_window">
        <field name="name">Funnels</field>
        <field name="res_model">funnel.definition</field>
        <field name="view_mode">tree,form</field>
        <field name="context">{'search_default_active': 1}</field>
        <field name="help" type="html">
            <p class="o_view_nocontent_smiling_face">
                Create your first sales funnel
            </p>
            <p>
                Build high-converting funnels with drag-and-drop snippets.
                Let SAM AI help you write compelling copy.
            </p>
        </field>
    </record>
</odoo>
```

#### views/funnel_template_views.xml
```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <!-- Tree View -->
    <record id="funnel_template_view_tree" model="ir.ui.view">
        <field name="name">funnel.template.tree</field>
        <field name="model">funnel.template</field>
        <field name="arch" type="xml">
            <tree string="Funnel Templates">
                <field name="name"/>
                <field name="funnel_type"/>
                <field name="usage_count"/>
                <field name="visibility"/>
                <field name="author_id"/>
            </tree>
        </field>
    </record>

    <!-- Form View -->
    <record id="funnel_template_view_form" model="ir.ui.view">
        <field name="name">funnel.template.form</field>
        <field name="model">funnel.template</field>
        <field name="arch" type="xml">
            <form string="Funnel Template">
                <sheet>
                    <div class="oe_button_box" name="button_box">
                        <button name="action_create_funnel_from_template" type="object" class="oe_stat_button" icon="fa-copy">
                            <span>Use Template</span>
                        </button>
                    </div>
                    <field name="thumbnail" widget="image" class="oe_avatar"/>
                    <div class="oe_title">
                        <h1>
                            <field name="name" placeholder="Template Name"/>
                        </h1>
                    </div>
                    <group>
                        <group>
                            <field name="funnel_type"/>
                            <field name="visibility"/>
                        </group>
                        <group>
                            <field name="usage_count"/>
                            <field name="author_id"/>
                        </group>
                    </group>
                    <notebook>
                        <page string="Description" name="description">
                            <field name="description"/>
                        </page>
                        <page string="Template Structure" name="structure">
                            <field name="template_structure" widget="ace" options="{'mode': 'json'}"/>
                        </page>
                    </notebook>
                </sheet>
            </form>
        </field>
    </record>

    <!-- Action -->
    <record id="funnel_template_action" model="ir.actions.act_window">
        <field name="name">Funnel Templates</field>
        <field name="res_model">funnel.template</field>
        <field name="view_mode">tree,form</field>
    </record>
</odoo>
```

#### views/funnel_snippet_views.xml
```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <!-- Tree View -->
    <record id="funnel_snippet_view_tree" model="ir.ui.view">
        <field name="name">funnel.snippet.tree</field>
        <field name="model">funnel.snippet</field>
        <field name="arch" type="xml">
            <tree string="Funnel Snippets">
                <field name="sequence" widget="handle"/>
                <field name="name"/>
                <field name="technical_name"/>
                <field name="category"/>
                <field name="template_xml_id"/>
                <field name="active"/>
            </tree>
        </field>
    </record>

    <!-- Form View -->
    <record id="funnel_snippet_view_form" model="ir.ui.view">
        <field name="name">funnel.snippet.form</field>
        <field name="model">funnel.snippet</field>
        <field name="arch" type="xml">
            <form string="Funnel Snippet">
                <sheet>
                    <field name="thumbnail" widget="image" class="oe_avatar"/>
                    <div class="oe_title">
                        <h1>
                            <field name="name" placeholder="Snippet Name"/>
                        </h1>
                    </div>
                    <group>
                        <group>
                            <field name="technical_name"/>
                            <field name="category"/>
                            <field name="sequence"/>
                        </group>
                        <group>
                            <field name="template_xml_id"/>
                            <field name="active"/>
                        </group>
                    </group>
                    <notebook>
                        <page string="Description" name="description">
                            <field name="description"/>
                        </page>
                        <page string="Field Schema" name="schema">
                            <field name="field_schema" widget="ace" options="{'mode': 'json'}"/>
                        </page>
                        <page string="SAM AI Hints" name="ai_hints">
                            <field name="copywriting_hints" placeholder="Enter copywriting hints for SAM AI..."/>
                        </page>
                    </notebook>
                </sheet>
            </form>
        </field>
    </record>

    <!-- Action -->
    <record id="funnel_snippet_action" model="ir.actions.act_window">
        <field name="name">Snippet Library</field>
        <field name="res_model">funnel.snippet</field>
        <field name="view_mode">tree,form</field>
    </record>
</odoo>
```

#### views/funnel_page_views.xml
```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <!-- Form View (for popup editing) -->
    <record id="funnel_page_view_form" model="ir.ui.view">
        <field name="name">funnel.page.form</field>
        <field name="model">funnel.page</field>
        <field name="arch" type="xml">
            <form string="Funnel Page">
                <sheet>
                    <group>
                        <group>
                            <field name="name"/>
                            <field name="page_type"/>
                            <field name="sequence"/>
                        </group>
                        <group>
                            <field name="page_url"/>
                            <field name="full_url" widget="url"/>
                            <field name="website_page_id"/>
                        </group>
                    </group>
                    <group>
                        <group string="Navigation">
                            <field name="next_page_id"/>
                            <field name="redirect_url"/>
                        </group>
                        <group string="Analytics">
                            <field name="view_count"/>
                            <field name="unique_visitors"/>
                            <field name="form_submissions"/>
                            <field name="conversion_rate" widget="progressbar"/>
                        </group>
                    </group>
                    <notebook>
                        <page string="Snippet Configuration" name="snippets">
                            <field name="snippet_config" widget="ace" options="{'mode': 'json'}"/>
                        </page>
                    </notebook>
                </sheet>
            </form>
        </field>
    </record>
</odoo>
```

#### views/funnel_menus.xml
```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <!-- Top-level menu under SAM AI -->
    <menuitem id="funnel_menu_root"
              name="Funnels"
              parent="ai_sam.menu_sam_ai_root"
              sequence="30"/>

    <!-- Funnels submenu -->
    <menuitem id="funnel_menu_funnels"
              name="My Funnels"
              parent="funnel_menu_root"
              action="funnel_definition_action"
              sequence="10"/>

    <!-- Templates submenu -->
    <menuitem id="funnel_menu_templates"
              name="Templates"
              parent="funnel_menu_root"
              action="funnel_template_action"
              sequence="20"/>

    <!-- Configuration menu -->
    <menuitem id="funnel_menu_config"
              name="Configuration"
              parent="funnel_menu_root"
              sequence="90"/>

    <!-- Snippet Library (under Configuration) -->
    <menuitem id="funnel_menu_snippets"
              name="Snippet Library"
              parent="funnel_menu_config"
              action="funnel_snippet_action"
              sequence="10"/>
</odoo>
```

### 5. Security

#### security/ir.model.access.csv
```csv
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_funnel_definition_user,funnel.definition.user,model_funnel_definition,base.group_user,1,1,1,0
access_funnel_definition_manager,funnel.definition.manager,model_funnel_definition,base.group_system,1,1,1,1
access_funnel_page_user,funnel.page.user,model_funnel_page,base.group_user,1,1,1,0
access_funnel_page_manager,funnel.page.manager,model_funnel_page,base.group_system,1,1,1,1
access_funnel_template_user,funnel.template.user,model_funnel_template,base.group_user,1,1,1,0
access_funnel_template_manager,funnel.template.manager,model_funnel_template,base.group_system,1,1,1,1
access_funnel_snippet_user,funnel.snippet.user,model_funnel_snippet,base.group_user,1,0,0,0
access_funnel_snippet_manager,funnel.snippet.manager,model_funnel_snippet,base.group_system,1,1,1,1
access_funnel_conversion_user,funnel.conversion.user,model_funnel_conversion,base.group_user,1,0,0,0
access_funnel_conversion_manager,funnel.conversion.manager,model_funnel_conversion,base.group_system,1,1,1,1
```

### 6. Initial Data

#### data/funnel_snippet_data.xml
```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <data noupdate="1">
        <!-- Hero Snippets -->
        <record id="snippet_hero_minimal" model="funnel.snippet">
            <field name="name">Minimal Hero</field>
            <field name="technical_name">hero_minimal</field>
            <field name="category">hero</field>
            <field name="sequence">10</field>
            <field name="description">Clean, focused opening with headline, subheadline, and single CTA</field>
            <field name="copywriting_hints">Headline: ONE powerful promise, 5-10 words. Use power words: Free, New, Proven, Secret, Discover. Formula: "[Outcome] Without [Pain Point]"</field>
        </record>

        <record id="snippet_hero_full" model="funnel.snippet">
            <field name="name">Full Hero</field>
            <field name="technical_name">hero_full</field>
            <field name="category">hero</field>
            <field name="sequence">20</field>
            <field name="description">Complete hero with headline, subheadline, video/image, and CTA</field>
        </record>

        <record id="snippet_hero_video" model="funnel.snippet">
            <field name="name">Video Hero</field>
            <field name="technical_name">hero_video</field>
            <field name="category">hero</field>
            <field name="sequence">30</field>
            <field name="description">Video-focused hero with background video, overlay text, and CTA</field>
        </record>

        <!-- Problem & Story Snippets -->
        <record id="snippet_problem_agitation" model="funnel.snippet">
            <field name="name">Problem Agitation</field>
            <field name="technical_name">problem_agitation</field>
            <field name="category">problem_story</field>
            <field name="sequence">10</field>
            <field name="description">Paint the pain using the PAS (Problem-Agitate-Solution) framework</field>
            <field name="copywriting_hints">1. PROBLEM: State pain clearly ("Tired of...", "Frustrated with..."). 2. AGITATE: Make it worse ("And the worst part?", "Every day it gets harder..."). 3. BRIDGE: Hint at hope ("What if there was a way...")</field>
        </record>

        <!-- CTA & Forms Snippets -->
        <record id="snippet_opt_in_form" model="funnel.snippet">
            <field name="name">Opt-in Form</field>
            <field name="technical_name">opt_in_form</field>
            <field name="category">cta_forms</field>
            <field name="sequence">10</field>
            <field name="description">Email capture form with CRM integration</field>
            <field name="copywriting_hints">Button text: Action + Outcome. NOT: "Submit" or "Sign Up". YES: "Get My Free Guide", "Start My Trial", "Show Me How"</field>
        </record>

        <!-- Add more snippets as needed... -->
    </data>
</odoo>
```

### 7. Controllers (Placeholder)

#### controllers/__init__.py
```python
from . import funnel_controller
```

#### controllers/funnel_controller.py
```python
from odoo import http
from odoo.http import request
import json


class FunnelController(http.Controller):
    """
    Placeholder controller for Phase 1.
    Form submission and API endpoints will be added in Phase 3.
    """

    @http.route('/funnel/health', type='json', auth='public')
    def health_check(self):
        """Simple health check endpoint"""
        return {'status': 'ok', 'module': 'sam_ai_funnels', 'phase': 1}
```

---

## VALIDATION CHECKLIST

After implementation, verify:

- [ ] Module installs without errors
- [ ] Can create a new funnel definition
- [ ] Can add pages to a funnel
- [ ] Can view funnel templates list
- [ ] Can view snippet library
- [ ] Menus appear under SAM AI > Funnels
- [ ] Security rules allow user CRUD operations
- [ ] Form fields render correctly
- [ ] Computed fields (page_count, conversion_rate) work

---

## DO NOT IMPLEMENT (Deferred to Later Phases)

- Website builder snippets (Phase 2)
- Form submission handling (Phase 3)
- CRM/Mailing integration (Phase 3)
- Complete funnel generation (Phase 4)
- SAM AI integration (Phase 6)
- Quiz logic (Phase 7)

---

## FILES TO CREATE (Summary)

1. `__manifest__.py`
2. `__init__.py`
3. `models/__init__.py`
4. `models/funnel_definition.py`
5. `models/funnel_page.py`
6. `models/funnel_template.py`
7. `models/funnel_snippet.py`
8. `models/funnel_conversion.py`
9. `controllers/__init__.py`
10. `controllers/funnel_controller.py`
11. `views/funnel_definition_views.xml`
12. `views/funnel_page_views.xml`
13. `views/funnel_template_views.xml`
14. `views/funnel_snippet_views.xml`
15. `views/funnel_menus.xml`
16. `data/funnel_snippet_data.xml`
17. `security/ir.model.access.csv`
18. `static/description/icon.png` (copy from ai_sam)

---

## NEXT PHASE

After Phase 1 is validated, proceed to Phase 2: Core Snippets (15).
The Phase 2 prompt will cover:
- FUNNELS tab registration in website builder
- 15 MVP snippet XML templates
- Snippet SCSS styling
- Customize panel options

---

**END OF PHASE 1 DEVELOPER PROMPT**
