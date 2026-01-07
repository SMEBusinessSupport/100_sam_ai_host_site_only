# Developer Prompt: SAM AI Funnels - Phase 4 (Complete Funnels)

**Date:** 2025-12-31
**Phase:** 4 of 7
**Scope:** Funnel templates, multi-page generation, page linking
**Prerequisite:** Phase 3 complete and validated

---

## CONTEXT

Phases 1-3 created the foundation, snippets, and form integration. Now we implement "Complete Funnels" - pre-built templates that create entire multi-page funnel sequences with one action.

**Architecture Document:** `D:\SAMAI-18-SaaS\ai_sam\ai_sam_docs\plans\2025-12-31_sam-ai-funnels-architecture.md`

---

## GOAL

1. Define 6 funnel template structures
2. Create wizard for generating funnels from templates
3. Generate multiple linked website pages
4. Auto-configure page redirects
5. Build funnel analytics dashboard

---

## THE 6 FUNNEL TEMPLATES

| ID | Template | Pages | Use Case |
|----|----------|-------|----------|
| 1 | Simple Opt-in | 2 | Quick email list building |
| 2 | Lead Magnet | 2 | Free resource offer + tripwire |
| 3 | Quiz Funnel | 5 | Qualify + segment leads |
| 4 | Expression of Interest | 2 | Pre-launch list building |
| 5 | Product Launch | 5 | Full sales sequence |
| 6 | Webinar | 4 | Event-based selling |

---

## DELIVERABLES

### 1. Template Data File

**File:** `data/funnel_templates.xml`

```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <data noupdate="1">

        <!-- ================================
             TEMPLATE 1: SIMPLE OPT-IN
             ================================ -->
        <record id="template_opt_in" model="funnel.template">
            <field name="name">Simple Opt-in Funnel</field>
            <field name="funnel_type">opt_in</field>
            <field name="description">Quick 2-page funnel for email list building. Squeeze page captures email, thank you page confirms subscription.</field>
            <field name="visibility">public</field>
            <field name="template_structure">{
    "pages": [
        {
            "name": "Squeeze Page",
            "page_type": "squeeze",
            "url_slug": "get-started",
            "snippets": [
                {"type": "hero_minimal", "config": {"headline": "Get Your Free [Resource]", "subheadline": "Enter your email to get instant access", "cta_text": ""}},
                {"type": "opt_in_form", "config": {"headline": "Join [X]+ Others", "button_text": "Get Instant Access", "fields": "email_only"}}
            ],
            "redirect_to_next": true
        },
        {
            "name": "Thank You",
            "page_type": "thank_you",
            "url_slug": "thank-you",
            "snippets": [
                {"type": "hero_minimal", "config": {"headline": "You're In!", "subheadline": "Check your inbox for your free [resource]", "cta_text": ""}},
                {"type": "cta_inline", "config": {"headline": "While You Wait...", "cta_text": "Follow Us", "cta_url": "#"}}
            ],
            "redirect_to_next": false
        }
    ]
}</field>
        </record>

        <!-- ================================
             TEMPLATE 2: LEAD MAGNET
             ================================ -->
        <record id="template_lead_magnet" model="funnel.template">
            <field name="name">Lead Magnet Funnel</field>
            <field name="funnel_type">lead_magnet</field>
            <field name="description">2-page funnel with lead magnet delivery and optional tripwire offer on thank you page.</field>
            <field name="visibility">public</field>
            <field name="template_structure">{
    "pages": [
        {
            "name": "Lead Magnet Page",
            "page_type": "lead_magnet",
            "url_slug": "free-guide",
            "snippets": [
                {"type": "hero_full", "config": {"headline": "Free Guide: [Title]", "subheadline": "Discover the [X] secrets to [outcome]"}},
                {"type": "benefits_stack", "config": {"headline": "Inside This Guide You'll Learn:", "items": ["Secret #1", "Secret #2", "Secret #3"]}},
                {"type": "testimonial_single", "config": {"quote": "This guide changed everything for me!", "name": "Happy Customer"}},
                {"type": "opt_in_form", "config": {"headline": "Get Your Free Copy", "button_text": "Download Now", "fields": "name_email"}},
                {"type": "guarantee", "config": {"headline": "100% Free, No Catch", "text": "We respect your privacy. Unsubscribe anytime."}}
            ],
            "redirect_to_next": true
        },
        {
            "name": "Thank You + Tripwire",
            "page_type": "thank_you",
            "url_slug": "thank-you-special",
            "snippets": [
                {"type": "hero_minimal", "config": {"headline": "Your Guide Is On The Way!", "subheadline": "Check your email (and spam folder)"}},
                {"type": "video_embed", "config": {"caption": "Watch this while you wait..."}},
                {"type": "offer_breakdown", "config": {"headline": "Special One-Time Offer", "items": ["Bonus #1", "Bonus #2"]}},
                {"type": "price_reveal", "config": {"anchor": "$97", "price": "$27", "cta_text": "Yes! Add This To My Order"}},
                {"type": "countdown_timer", "config": {"headline": "This offer expires in:", "type": "evergreen", "hours": 24}}
            ],
            "redirect_to_next": false
        }
    ]
}</field>
        </record>

        <!-- ================================
             TEMPLATE 3: QUIZ FUNNEL
             ================================ -->
        <record id="template_quiz" model="funnel.template">
            <field name="name">Quiz Funnel</field>
            <field name="funnel_type">quiz</field>
            <field name="description">5-page quiz funnel that qualifies leads, captures email before showing results, then presents personalized offer.</field>
            <field name="visibility">public</field>
            <field name="template_structure">{
    "pages": [
        {
            "name": "Quiz Introduction",
            "page_type": "quiz_intro",
            "url_slug": "quiz",
            "snippets": [
                {"type": "hero_full", "config": {"headline": "Discover Your [X] Type", "subheadline": "Take this 2-minute quiz to get personalized recommendations", "cta_text": "Start Quiz"}}
            ],
            "redirect_to_next": true
        },
        {
            "name": "Quiz Questions",
            "page_type": "quiz_questions",
            "url_slug": "quiz-questions",
            "snippets": [
                {"type": "quiz_progress", "config": {"style": "bar"}},
                {"type": "quiz_question", "config": {"questions": [
                    {"q": "Question 1?", "answers": ["A", "B", "C", "D"]},
                    {"q": "Question 2?", "answers": ["A", "B", "C", "D"]},
                    {"q": "Question 3?", "answers": ["A", "B", "C", "D"]}
                ]}}
            ],
            "redirect_to_next": true
        },
        {
            "name": "Email Gate",
            "page_type": "quiz_gate",
            "url_slug": "quiz-results-gate",
            "snippets": [
                {"type": "hero_minimal", "config": {"headline": "Your Results Are Ready!", "subheadline": "Enter your email to see your personalized results"}},
                {"type": "opt_in_form", "config": {"headline": "", "button_text": "See My Results", "fields": "name_email"}}
            ],
            "redirect_to_next": true
        },
        {
            "name": "Quiz Results",
            "page_type": "quiz_results",
            "url_slug": "your-results",
            "snippets": [
                {"type": "hero_full", "config": {"headline": "Your Type: [Result]", "subheadline": "Based on your answers, here's what we recommend..."}},
                {"type": "benefits_stack", "config": {"headline": "What This Means For You:"}},
                {"type": "cta_inline", "config": {"headline": "Ready For The Next Step?", "cta_text": "See Your Solution"}}
            ],
            "redirect_to_next": true
        },
        {
            "name": "Personalized Offer",
            "page_type": "sales",
            "url_slug": "your-solution",
            "snippets": [
                {"type": "hero_full", "config": {"headline": "The Perfect Solution For Your [Type]"}},
                {"type": "benefits_stack", "config": {}},
                {"type": "testimonial_single", "config": {}},
                {"type": "offer_breakdown", "config": {}},
                {"type": "price_reveal", "config": {}},
                {"type": "guarantee", "config": {}},
                {"type": "final_cta", "config": {}}
            ],
            "redirect_to_next": false
        }
    ]
}</field>
        </record>

        <!-- ================================
             TEMPLATE 4: EXPRESSION OF INTEREST
             ================================ -->
        <record id="template_eoi" model="funnel.template">
            <field name="name">Expression of Interest Funnel</field>
            <field name="funnel_type">eoi</field>
            <field name="description">Pre-launch list building funnel. Tease upcoming offer, capture interested prospects.</field>
            <field name="visibility">public</field>
            <field name="template_structure">{
    "pages": [
        {
            "name": "Interest Page",
            "page_type": "squeeze",
            "url_slug": "coming-soon",
            "snippets": [
                {"type": "hero_full", "config": {"headline": "Something Big Is Coming...", "subheadline": "Be the first to know when we launch"}},
                {"type": "problem_agitation", "config": {"headline": "Tired of [problem]?"}},
                {"type": "benefits_stack", "config": {"headline": "What's Coming:"}},
                {"type": "opt_in_form", "config": {"headline": "Get Early Access", "button_text": "Yes, I'm Interested!", "fields": "name_email"}},
                {"type": "countdown_timer", "config": {"headline": "Launching In:", "type": "fixed"}}
            ],
            "redirect_to_next": true
        },
        {
            "name": "Thank You",
            "page_type": "thank_you",
            "url_slug": "youre-on-the-list",
            "snippets": [
                {"type": "hero_minimal", "config": {"headline": "You're On The List!", "subheadline": "We'll notify you the moment we launch"}},
                {"type": "cta_inline", "config": {"headline": "Spread The Word", "subheadline": "Share with friends who might be interested", "cta_text": "Share Now"}}
            ],
            "redirect_to_next": false
        }
    ]
}</field>
        </record>

        <!-- ================================
             TEMPLATE 5: PRODUCT LAUNCH
             ================================ -->
        <record id="template_product_launch" model="funnel.template">
            <field name="name">Product Launch Funnel</field>
            <field name="funnel_type">product_launch</field>
            <field name="description">Full 5-page sales funnel with opt-in, sales page, order form, upsell, and thank you.</field>
            <field name="visibility">public</field>
            <field name="template_structure">{
    "pages": [
        {
            "name": "Opt-in Page",
            "page_type": "squeeze",
            "url_slug": "free-training",
            "snippets": [
                {"type": "hero_full", "config": {"headline": "Free Training: [Title]", "subheadline": "Learn [outcome] in this free video"}},
                {"type": "opt_in_form", "config": {"button_text": "Watch Free Training", "fields": "name_email"}}
            ],
            "redirect_to_next": true
        },
        {
            "name": "Sales Page",
            "page_type": "sales",
            "url_slug": "special-offer",
            "snippets": [
                {"type": "hero_full", "config": {"headline": "[Product Name]", "subheadline": "[Main promise]"}},
                {"type": "video_embed", "config": {}},
                {"type": "problem_agitation", "config": {}},
                {"type": "benefits_stack", "config": {"headline": "What You'll Get:"}},
                {"type": "testimonial_single", "config": {}},
                {"type": "offer_breakdown", "config": {"headline": "Everything Included:"}},
                {"type": "price_reveal", "config": {}},
                {"type": "guarantee", "config": {}},
                {"type": "objection_handler", "config": {}},
                {"type": "final_cta", "config": {}}
            ],
            "redirect_to_next": true
        },
        {
            "name": "Order Form",
            "page_type": "order",
            "url_slug": "checkout",
            "snippets": [
                {"type": "hero_minimal", "config": {"headline": "Complete Your Order"}},
                {"type": "offer_breakdown", "config": {"headline": "Order Summary"}},
                {"type": "opt_in_form", "config": {"headline": "", "button_text": "Complete Purchase", "fields": "name_email_phone"}},
                {"type": "guarantee", "config": {}},
                {"type": "testimonial_single", "config": {}}
            ],
            "redirect_to_next": true
        },
        {
            "name": "Upsell",
            "page_type": "upsell",
            "url_slug": "special-upgrade",
            "snippets": [
                {"type": "hero_full", "config": {"headline": "Wait! Special One-Time Upgrade"}},
                {"type": "offer_breakdown", "config": {}},
                {"type": "price_reveal", "config": {}},
                {"type": "countdown_timer", "config": {"type": "evergreen", "hours": 1}},
                {"type": "cta_inline", "config": {"cta_text": "Yes, Upgrade My Order!"}}
            ],
            "redirect_to_next": true
        },
        {
            "name": "Thank You",
            "page_type": "thank_you",
            "url_slug": "order-confirmed",
            "snippets": [
                {"type": "hero_minimal", "config": {"headline": "Order Confirmed!", "subheadline": "Welcome to [Product Name]"}},
                {"type": "video_embed", "config": {"caption": "Here's what to do next..."}},
                {"type": "cta_inline", "config": {"headline": "Access Your Purchase", "cta_text": "Go To Member Area"}}
            ],
            "redirect_to_next": false
        }
    ]
}</field>
        </record>

        <!-- ================================
             TEMPLATE 6: WEBINAR
             ================================ -->
        <record id="template_webinar" model="funnel.template">
            <field name="name">Webinar Funnel</field>
            <field name="funnel_type">webinar</field>
            <field name="description">4-page webinar funnel with registration, confirmation, replay access, and sales page.</field>
            <field name="visibility">public</field>
            <field name="template_structure">{
    "pages": [
        {
            "name": "Registration",
            "page_type": "webinar_registration",
            "url_slug": "webinar-registration",
            "snippets": [
                {"type": "hero_full", "config": {"headline": "Free Live Training: [Title]", "subheadline": "Learn [outcome] in this exclusive webinar"}},
                {"type": "benefits_stack", "config": {"headline": "In This Training You'll Discover:"}},
                {"type": "countdown_timer", "config": {"headline": "Webinar Starts In:", "type": "fixed"}},
                {"type": "opt_in_form", "config": {"headline": "Reserve Your Spot", "button_text": "Save My Seat", "fields": "name_email"}},
                {"type": "testimonial_single", "config": {}}
            ],
            "redirect_to_next": true
        },
        {
            "name": "Confirmation",
            "page_type": "webinar_confirmation",
            "url_slug": "webinar-confirmed",
            "snippets": [
                {"type": "hero_minimal", "config": {"headline": "You're Registered!", "subheadline": "Mark your calendar for [date/time]"}},
                {"type": "cta_inline", "config": {"headline": "Add To Calendar", "cta_text": "Add To Google Calendar"}},
                {"type": "video_embed", "config": {"caption": "Watch this short intro before the webinar..."}}
            ],
            "redirect_to_next": false
        },
        {
            "name": "Replay Page",
            "page_type": "webinar_replay",
            "url_slug": "webinar-replay",
            "snippets": [
                {"type": "hero_full", "config": {"headline": "Watch The Replay", "subheadline": "Available for limited time only"}},
                {"type": "countdown_timer", "config": {"headline": "Replay Expires In:", "type": "evergreen", "hours": 48}},
                {"type": "video_embed", "config": {}},
                {"type": "cta_inline", "config": {"headline": "Ready to Take Action?", "cta_text": "Get Special Offer"}}
            ],
            "redirect_to_next": true
        },
        {
            "name": "Sales Page",
            "page_type": "sales",
            "url_slug": "webinar-offer",
            "snippets": [
                {"type": "hero_full", "config": {"headline": "Webinar-Only Special Offer"}},
                {"type": "problem_agitation", "config": {}},
                {"type": "benefits_stack", "config": {}},
                {"type": "testimonial_single", "config": {}},
                {"type": "offer_breakdown", "config": {}},
                {"type": "price_reveal", "config": {}},
                {"type": "guarantee", "config": {}},
                {"type": "countdown_timer", "config": {"headline": "Offer Expires:", "type": "evergreen", "hours": 24}},
                {"type": "objection_handler", "config": {}},
                {"type": "final_cta", "config": {}}
            ],
            "redirect_to_next": false
        }
    ]
}</field>
        </record>

    </data>
</odoo>
```

---

### 2. Funnel Generation Wizard

**File:** `wizards/funnel_generator_wizard.py`

```python
import json
import logging
from odoo import models, fields, api, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class FunnelGeneratorWizard(models.TransientModel):
    _name = 'funnel.generator.wizard'
    _description = 'Funnel Generator Wizard'

    # Step 1: Select template
    template_id = fields.Many2one(
        'funnel.template',
        string='Funnel Template',
        required=True,
        domain=[('visibility', 'in', ['company', 'public'])]
    )
    template_description = fields.Text(
        related='template_id.description',
        readonly=True
    )

    # Step 2: Configure funnel
    name = fields.Char(
        string='Funnel Name',
        required=True,
        help='Name for this funnel instance'
    )
    url_prefix = fields.Char(
        string='URL Prefix',
        help='Optional prefix for page URLs (e.g., "launch-2025")'
    )

    # CRM Integration
    crm_team_id = fields.Many2one(
        'crm.team',
        string='Sales Team',
        help='Assign leads from this funnel to this team'
    )
    default_tag_ids = fields.Many2many(
        'crm.tag',
        string='Lead Tags',
        help='Tags to apply to all leads from this funnel'
    )

    # Mailing Integration
    mailing_list_id = fields.Many2one(
        'mailing.list',
        string='Mailing List',
        help='Add subscribers to this mailing list'
    )

    # Preview
    page_preview = fields.Text(
        string='Pages to Create',
        compute='_compute_page_preview'
    )

    @api.depends('template_id')
    def _compute_page_preview(self):
        for wizard in self:
            if not wizard.template_id or not wizard.template_id.template_structure:
                wizard.page_preview = ''
                continue

            try:
                structure = json.loads(wizard.template_id.template_structure)
                pages = structure.get('pages', [])
                preview_lines = []
                for i, page in enumerate(pages, 1):
                    preview_lines.append(
                        f"{i}. {page.get('name', 'Unnamed')} ({page.get('page_type', 'custom')})"
                    )
                wizard.page_preview = '\n'.join(preview_lines)
            except json.JSONDecodeError:
                wizard.page_preview = 'Error parsing template'

    @api.onchange('template_id')
    def _onchange_template_id(self):
        if self.template_id:
            self.name = f"{self.template_id.name} - {fields.Date.today()}"

    def action_generate_funnel(self):
        """Generate the complete funnel from template."""
        self.ensure_one()

        if not self.template_id or not self.template_id.template_structure:
            raise UserError(_('Please select a valid template'))

        try:
            structure = json.loads(self.template_id.template_structure)
        except json.JSONDecodeError:
            raise UserError(_('Template structure is invalid'))

        # Create the funnel definition
        funnel = self.env['funnel.definition'].create({
            'name': self.name,
            'funnel_type': self.template_id.funnel_type,
            'template_id': self.template_id.id,
            'crm_team_id': self.crm_team_id.id if self.crm_team_id else False,
            'default_tag_ids': [(6, 0, self.default_tag_ids.ids)] if self.default_tag_ids else False,
            'mailing_list_id': self.mailing_list_id.id if self.mailing_list_id else False,
            'state': 'draft',
        })

        # Create pages
        pages = structure.get('pages', [])
        created_pages = []

        for idx, page_spec in enumerate(pages):
            page = self._create_funnel_page(funnel, page_spec, idx)
            created_pages.append(page)

        # Link pages (set redirect to next page)
        for idx, page in enumerate(created_pages):
            if idx < len(created_pages) - 1:
                page_spec = pages[idx]
                if page_spec.get('redirect_to_next', False):
                    page.write({
                        'next_page_id': created_pages[idx + 1].id,
                        'redirect_url': created_pages[idx + 1].full_url,
                    })

        # Increment template usage count
        self.template_id.usage_count += 1

        # Return action to view the funnel
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'funnel.definition',
            'res_id': funnel.id,
            'view_mode': 'form',
            'target': 'current',
        }

    def _create_funnel_page(self, funnel, page_spec, sequence):
        """Create a single funnel page with its website page."""
        # Build URL slug
        url_slug = page_spec.get('url_slug', f'page-{sequence + 1}')
        if self.url_prefix:
            url_slug = f"{self.url_prefix}/{url_slug}"

        # Create funnel page record
        funnel_page = self.env['funnel.page'].create({
            'funnel_id': funnel.id,
            'name': page_spec.get('name', f'Page {sequence + 1}'),
            'page_type': page_spec.get('page_type', 'custom'),
            'sequence': (sequence + 1) * 10,
            'page_url': url_slug,
            'snippet_config': json.dumps(page_spec.get('snippets', [])),
        })

        # Create actual website page
        website_page = self._create_website_page(funnel, funnel_page, page_spec)
        if website_page:
            funnel_page.website_page_id = website_page.id

        return funnel_page

    def _create_website_page(self, funnel, funnel_page, page_spec):
        """Create the website page with snippet HTML."""
        try:
            # Generate page HTML from snippets
            html_content = self._generate_page_html(funnel, funnel_page, page_spec)

            # Create website.page
            website = self.env['website'].get_current_website()

            # Create the view for this page
            view = self.env['ir.ui.view'].create({
                'name': f"Funnel: {funnel.name} - {funnel_page.name}",
                'type': 'qweb',
                'arch': f'''
                    <t t-name="funnel_page_{funnel_page.id}">
                        <t t-call="website.layout">
                            <div id="wrap" class="oe_structure oe_empty">
                                {html_content}
                            </div>
                        </t>
                    </t>
                ''',
                'key': f'sam_ai_funnels.funnel_page_{funnel_page.id}',
            })

            # Create the page
            page = self.env['website.page'].create({
                'name': funnel_page.name,
                'url': f'/{funnel_page.page_url}',
                'view_id': view.id,
                'website_id': website.id,
                'is_published': False,  # Start unpublished
            })

            return page

        except Exception as e:
            _logger.error(f"Error creating website page: {str(e)}")
            return None

    def _generate_page_html(self, funnel, funnel_page, page_spec):
        """Generate HTML content from snippet specifications."""
        snippets = page_spec.get('snippets', [])
        html_parts = []

        for snippet_spec in snippets:
            snippet_type = snippet_spec.get('type')
            snippet_config = snippet_spec.get('config', {})

            # Get the base snippet HTML
            snippet_html = self._get_snippet_html(snippet_type, snippet_config, funnel, funnel_page)
            if snippet_html:
                html_parts.append(snippet_html)

        return '\n'.join(html_parts)

    def _get_snippet_html(self, snippet_type, config, funnel, funnel_page):
        """Get HTML for a specific snippet type with config applied."""
        # Map snippet types to their XML templates
        snippet_map = {
            'hero_minimal': 's_hero_minimal',
            'hero_full': 's_hero_full',
            'problem_agitation': 's_problem_agitation',
            'benefits_stack': 's_benefits_stack',
            'testimonial_single': 's_testimonial_single',
            'opt_in_form': 's_opt_in_form',
            'cta_inline': 's_cta_inline',
            'final_cta': 's_final_cta',
            'offer_breakdown': 's_offer_breakdown',
            'price_reveal': 's_price_reveal',
            'guarantee': 's_guarantee',
            'countdown_timer': 's_countdown_timer',
            'objection_handler': 's_objection_handler',
            'spacer': 's_spacer',
            'video_embed': 's_video_embed',
            'quiz_progress': 's_quiz_progress',
            'quiz_question': 's_quiz_question',
        }

        template_name = snippet_map.get(snippet_type)
        if not template_name:
            _logger.warning(f"Unknown snippet type: {snippet_type}")
            return ''

        try:
            # Render the snippet template
            template_xml_id = f'sam_ai_funnels.{template_name}'
            html = self.env['ir.qweb']._render(template_xml_id, {
                'funnel': funnel,
                'page': funnel_page,
                'config': config,
            })

            # Add funnel/page data attributes for tracking
            html = self._inject_tracking_attributes(html, funnel, funnel_page, config)

            return html

        except Exception as e:
            _logger.error(f"Error rendering snippet {template_name}: {str(e)}")
            return ''

    def _inject_tracking_attributes(self, html, funnel, funnel_page, config):
        """Inject funnel/page tracking attributes into snippet HTML."""
        # This is a simplified version - in production you'd parse and modify the HTML properly
        tracking_attrs = f'data-funnel-id="{funnel.id}" data-page-id="{funnel_page.id}"'

        # For opt_in_form, also inject integration settings
        if 'opt_in_form' in str(html) or 's_opt_in_form' in str(html):
            integration = config.get('integration', 'crm')
            redirect_url = funnel_page.redirect_url or '/thank-you'
            tracking_attrs += f' data-integration="{integration}" data-redirect-url="{redirect_url}"'

            if funnel.mailing_list_id:
                tracking_attrs += f' data-mailing-list-id="{funnel.mailing_list_id.id}"'

        # Inject attributes into the first section tag
        html = str(html)
        if '<section' in html:
            html = html.replace('<section', f'<section {tracking_attrs}', 1)

        return html
```

---

### 3. Wizard Views

**File:** `wizards/funnel_generator_wizard_views.xml`

```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <!-- Wizard Form View -->
    <record id="funnel_generator_wizard_view_form" model="ir.ui.view">
        <field name="name">funnel.generator.wizard.form</field>
        <field name="model">funnel.generator.wizard</field>
        <field name="arch" type="xml">
            <form string="Create Funnel from Template">
                <group>
                    <group string="Select Template">
                        <field name="template_id" widget="selection"/>
                        <field name="template_description" readonly="1" nolabel="1" colspan="2"/>
                    </group>
                    <group string="Pages to Create">
                        <field name="page_preview" readonly="1" nolabel="1" widget="text"/>
                    </group>
                </group>
                <group>
                    <group string="Funnel Settings">
                        <field name="name"/>
                        <field name="url_prefix" placeholder="e.g., launch-jan-2025"/>
                    </group>
                    <group string="Integrations">
                        <field name="crm_team_id"/>
                        <field name="default_tag_ids" widget="many2many_tags"/>
                        <field name="mailing_list_id"/>
                    </group>
                </group>
                <footer>
                    <button name="action_generate_funnel"
                            string="Create Funnel"
                            type="object"
                            class="btn-primary"/>
                    <button string="Cancel" class="btn-secondary" special="cancel"/>
                </footer>
            </form>
        </field>
    </record>

    <!-- Wizard Action -->
    <record id="funnel_generator_wizard_action" model="ir.actions.act_window">
        <field name="name">Create Funnel from Template</field>
        <field name="res_model">funnel.generator.wizard</field>
        <field name="view_mode">form</field>
        <field name="target">new</field>
    </record>
</odoo>
```

---

### 4. Update Funnel Definition Views

Add "Create from Template" button to `views/funnel_definition_views.xml`:

```xml
<!-- Add to the tree view actions -->
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
            Start with a template or build from scratch.
        </p>
        <p>
            <a type="action" name="%(funnel_generator_wizard_action)d">
                Create from Template
            </a>
        </p>
    </field>
</record>

<!-- Add button to form view header -->
<!-- In funnel_definition_view_form, add after header buttons: -->
<button name="%(funnel_generator_wizard_action)d"
        string="Create from Template"
        type="action"
        class="btn-secondary"
        invisible="id"/>
```

---

### 5. Dashboard View

**File:** `views/funnel_dashboard.xml`

```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <!-- Funnel Kanban View -->
    <record id="funnel_definition_view_kanban" model="ir.ui.view">
        <field name="name">funnel.definition.kanban</field>
        <field name="model">funnel.definition</field>
        <field name="arch" type="xml">
            <kanban class="o_kanban_mobile" default_group_by="state">
                <field name="name"/>
                <field name="funnel_type"/>
                <field name="state"/>
                <field name="page_count"/>
                <field name="total_views"/>
                <field name="total_conversions"/>
                <field name="conversion_rate"/>
                <templates>
                    <t t-name="kanban-box">
                        <div class="oe_kanban_card oe_kanban_global_click">
                            <div class="oe_kanban_content">
                                <div class="o_kanban_record_top mb-2">
                                    <div class="o_kanban_record_headings">
                                        <strong class="o_kanban_record_title">
                                            <field name="name"/>
                                        </strong>
                                    </div>
                                    <field name="funnel_type" widget="badge"/>
                                </div>
                                <div class="row g-0 mb-2">
                                    <div class="col-4 text-center">
                                        <div class="fw-bold" style="font-size: 1.5em;">
                                            <field name="page_count"/>
                                        </div>
                                        <small class="text-muted">Pages</small>
                                    </div>
                                    <div class="col-4 text-center">
                                        <div class="fw-bold" style="font-size: 1.5em;">
                                            <field name="total_views"/>
                                        </div>
                                        <small class="text-muted">Views</small>
                                    </div>
                                    <div class="col-4 text-center">
                                        <div class="fw-bold" style="font-size: 1.5em;">
                                            <field name="total_conversions"/>
                                        </div>
                                        <small class="text-muted">Leads</small>
                                    </div>
                                </div>
                                <div class="o_kanban_record_bottom">
                                    <div class="oe_kanban_bottom_left">
                                        <span class="text-success">
                                            <field name="conversion_rate" widget="float" digits="[3,1]"/>% CVR
                                        </span>
                                    </div>
                                    <div class="oe_kanban_bottom_right">
                                        <field name="state" widget="label_selection" options="{'classes': {'draft': 'secondary', 'active': 'success', 'paused': 'warning', 'archived': 'dark'}}"/>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </t>
                </templates>
            </kanban>
        </field>
    </record>

    <!-- Update action to include kanban -->
    <record id="funnel_definition_action" model="ir.actions.act_window">
        <field name="name">Funnels</field>
        <field name="res_model">funnel.definition</field>
        <field name="view_mode">kanban,tree,form</field>
        <field name="context">{'search_default_active': 1}</field>
    </record>

    <!-- Dashboard Action (Pivot/Graph focused) -->
    <record id="funnel_dashboard_action" model="ir.actions.act_window">
        <field name="name">Funnel Dashboard</field>
        <field name="res_model">funnel.conversion</field>
        <field name="view_mode">pivot,graph,tree</field>
        <field name="context">{
            'search_default_this_week': 1,
            'pivot_measures': ['__count'],
            'pivot_column_groupby': ['event_type'],
            'pivot_row_groupby': ['funnel_id']
        }</field>
    </record>

    <!-- Add Dashboard to menu -->
    <menuitem id="funnel_menu_dashboard"
              name="Dashboard"
              parent="funnel_menu_root"
              action="funnel_dashboard_action"
              sequence="5"/>
</odoo>
```

---

### 6. Update __manifest__.py

```python
{
    # ... existing fields ...
    'data': [
        # Security
        'security/ir.model.access.csv',

        # Wizards
        'wizards/funnel_generator_wizard_views.xml',

        # Views
        'views/funnel_definition_views.xml',
        'views/funnel_page_views.xml',
        'views/funnel_template_views.xml',
        'views/funnel_snippet_views.xml',
        'views/funnel_conversion_views.xml',
        'views/funnel_dashboard.xml',
        'views/funnel_menus.xml',
        'views/funnel_form_error.xml',

        # Snippets
        'views/snippets/options.xml',
        # ... all snippet xml files ...

        # Data (load AFTER views)
        'data/funnel_snippet_data.xml',
        'data/funnel_templates.xml',
    ],
    # ... rest of manifest ...
}
```

---

### 7. Update wizards/__init__.py

```python
from . import funnel_generator_wizard
```

---

### 8. Update Security

Add to `security/ir.model.access.csv`:

```csv
access_funnel_generator_wizard,funnel.generator.wizard,model_funnel_generator_wizard,base.group_user,1,1,1,0
```

---

## VALIDATION CHECKLIST

After implementation, verify:

- [ ] All 6 funnel templates appear in template list
- [ ] "Create from Template" wizard opens correctly
- [ ] Template preview shows correct pages
- [ ] Generating funnel creates funnel.definition record
- [ ] Correct number of funnel.page records created
- [ ] Website pages created with correct URLs
- [ ] Page redirects link to next page correctly
- [ ] Funnel/page IDs injected into snippet HTML
- [ ] Template usage_count increments
- [ ] Kanban view shows funnel cards with stats
- [ ] Dashboard pivot/graph views work
- [ ] CRM team and tags applied to funnel

---

## FILES TO CREATE/UPDATE

**Create:**
1. `data/funnel_templates.xml`
2. `wizards/__init__.py`
3. `wizards/funnel_generator_wizard.py`
4. `wizards/funnel_generator_wizard_views.xml`
5. `views/funnel_dashboard.xml`

**Update:**
6. `__init__.py` (add wizards import)
7. `__manifest__.py` (add new files)
8. `views/funnel_definition_views.xml` (add kanban, template button)
9. `views/funnel_menus.xml` (add dashboard menu)
10. `security/ir.model.access.csv` (add wizard access)

---

## NEXT PHASE

After Phase 4 is validated, proceed to Phase 5: Remaining Snippets.
Phase 5 will complete the full 46-snippet library.

---

**END OF PHASE 4 DEVELOPER PROMPT**
