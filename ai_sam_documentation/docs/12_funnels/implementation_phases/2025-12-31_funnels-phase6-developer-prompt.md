# Developer Prompt: SAM AI Funnels - Phase 6 (SAM AI Integration)

**Date:** 2025-12-31
**Phase:** 6 of 7
**Scope:** SAM AI chat integration for funnel building and copy generation
**Prerequisite:** Phase 5 complete, SAM AI chat infrastructure stable

---

## CONTEXT

With the complete snippet library and funnel templates in place, we now integrate SAM AI so it can:
1. Build funnels conversationally ("Build me a webinar funnel for my coaching business")
2. Generate copy for each snippet type using direct response frameworks
3. Understand funnel structure and recommend appropriate snippets

---

## GOAL

1. Create API endpoint for SAM to build funnels programmatically
2. Add funnel copywriting knowledge to SAM's context
3. Enable SAM to detect funnel-building intent and respond appropriately
4. Generate copy that follows proven direct response patterns

---

## DELIVERABLES

### 1. SAM Funnel API Controller

**File:** `controllers/sam_funnel_api.py`

```python
import json
import logging
from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class SamFunnelAPIController(http.Controller):
    """API endpoints for SAM AI to create and manage funnels."""

    @http.route('/sam_ai_funnels/create', type='json', auth='user', methods=['POST'])
    def create_funnel_from_sam(self, funnel_spec, **kwargs):
        """
        Create a funnel from SAM AI's specification.

        Args:
            funnel_spec: {
                'name': 'Q1 Webinar Funnel',
                'funnel_type': 'webinar',
                'template_id': 5,  # Optional - use template as base
                'crm_team_id': 2,
                'mailing_list_id': 3,
                'pages': [
                    {
                        'name': 'Registration',
                        'page_type': 'webinar_registration',
                        'url_slug': 'webinar-jan-2025',
                        'snippets': [
                            {
                                'type': 'hero_full',
                                'content': {
                                    'headline': 'Free Live Training...',
                                    'subheadline': 'Learn how to...',
                                    'cta_text': 'Save My Seat'
                                }
                            },
                            {
                                'type': 'benefits_stack',
                                'content': {
                                    'headline': 'In This Training You Will Discover:',
                                    'items': [
                                        'The 3-step system for...',
                                        'How to avoid the #1 mistake...',
                                        'Why most people fail and how you won\'t'
                                    ]
                                }
                            },
                            {
                                'type': 'opt_in_form',
                                'content': {
                                    'headline': 'Reserve Your Spot',
                                    'button_text': 'Yes! Save My Seat'
                                }
                            }
                        ]
                    },
                    # ... more pages
                ]
            }

        Returns:
            {
                'success': True,
                'funnel_id': 42,
                'funnel_url': '/webinar-jan-2025',
                'pages': [
                    {'name': 'Registration', 'url': '/webinar-jan-2025'},
                    {'name': 'Confirmation', 'url': '/webinar-confirmed'}
                ]
            }
        """
        try:
            # Validate required fields
            if not funnel_spec.get('name'):
                return {'success': False, 'error': 'Funnel name is required'}

            if not funnel_spec.get('pages'):
                return {'success': False, 'error': 'At least one page is required'}

            # Create funnel definition
            funnel_vals = {
                'name': funnel_spec['name'],
                'funnel_type': funnel_spec.get('funnel_type', 'custom'),
                'ai_generated_copy': True,
                'state': 'draft',
            }

            if funnel_spec.get('template_id'):
                funnel_vals['template_id'] = funnel_spec['template_id']
            if funnel_spec.get('crm_team_id'):
                funnel_vals['crm_team_id'] = funnel_spec['crm_team_id']
            if funnel_spec.get('mailing_list_id'):
                funnel_vals['mailing_list_id'] = funnel_spec['mailing_list_id']

            funnel = request.env['funnel.definition'].create(funnel_vals)

            # Create pages with AI-generated content
            created_pages = []
            for idx, page_spec in enumerate(funnel_spec['pages']):
                page = self._create_page_with_content(funnel, page_spec, idx)
                created_pages.append({
                    'name': page.name,
                    'url': page.full_url or f'/{page.page_url}',
                    'page_id': page.id
                })

            # Link pages for redirects
            self._link_pages(created_pages, funnel_spec['pages'])

            return {
                'success': True,
                'funnel_id': funnel.id,
                'funnel_url': created_pages[0]['url'] if created_pages else None,
                'pages': created_pages
            }

        except Exception as e:
            _logger.error(f"SAM funnel creation error: {str(e)}")
            return {'success': False, 'error': str(e)}

    def _create_page_with_content(self, funnel, page_spec, sequence):
        """Create a funnel page with AI-generated snippet content."""
        page = request.env['funnel.page'].create({
            'funnel_id': funnel.id,
            'name': page_spec.get('name', f'Page {sequence + 1}'),
            'page_type': page_spec.get('page_type', 'custom'),
            'sequence': (sequence + 1) * 10,
            'page_url': page_spec.get('url_slug', f'page-{sequence + 1}'),
            'snippet_config': json.dumps(page_spec.get('snippets', [])),
        })

        # Generate website page with content
        self._generate_website_page(funnel, page, page_spec.get('snippets', []))

        return page

    def _generate_website_page(self, funnel, funnel_page, snippets):
        """Generate the actual website page with snippet HTML."""
        html_content = self._build_page_html(funnel, funnel_page, snippets)

        website = request.env['website'].get_current_website()

        view = request.env['ir.ui.view'].create({
            'name': f"SAM Funnel: {funnel.name} - {funnel_page.name}",
            'type': 'qweb',
            'arch': f'''
                <t t-name="sam_funnel_page_{funnel_page.id}">
                    <t t-call="website.layout">
                        <div id="wrap" class="oe_structure">
                            {html_content}
                        </div>
                    </t>
                </t>
            ''',
            'key': f'sam_ai_funnels.sam_page_{funnel_page.id}',
        })

        page = request.env['website.page'].create({
            'name': funnel_page.name,
            'url': f'/{funnel_page.page_url}',
            'view_id': view.id,
            'website_id': website.id,
            'is_published': False,
        })

        funnel_page.website_page_id = page.id

    def _build_page_html(self, funnel, funnel_page, snippets):
        """Build HTML from snippet specifications with AI content."""
        html_parts = []

        for snippet in snippets:
            snippet_html = self._render_snippet_with_content(
                snippet['type'],
                snippet.get('content', {}),
                funnel,
                funnel_page
            )
            html_parts.append(snippet_html)

        return '\n'.join(html_parts)

    def _render_snippet_with_content(self, snippet_type, content, funnel, funnel_page):
        """Render a snippet template with AI-generated content."""
        # Get base template
        template_map = {
            'hero_minimal': self._render_hero_minimal,
            'hero_full': self._render_hero_full,
            'problem_agitation': self._render_problem_agitation,
            'benefits_stack': self._render_benefits_stack,
            'testimonial_single': self._render_testimonial_single,
            'opt_in_form': self._render_opt_in_form,
            'cta_inline': self._render_cta_inline,
            'final_cta': self._render_final_cta,
            'offer_breakdown': self._render_offer_breakdown,
            'price_reveal': self._render_price_reveal,
            'guarantee': self._render_guarantee,
            'countdown_timer': self._render_countdown_timer,
            'objection_handler': self._render_objection_handler,
            'video_embed': self._render_video_embed,
            # Add more as needed
        }

        renderer = template_map.get(snippet_type)
        if renderer:
            return renderer(content, funnel, funnel_page)
        else:
            _logger.warning(f"Unknown snippet type for SAM: {snippet_type}")
            return f'<!-- Unknown snippet: {snippet_type} -->'

    def _render_hero_minimal(self, content, funnel, funnel_page):
        """Render hero_minimal with AI content."""
        headline = content.get('headline', 'Your Compelling Headline')
        subheadline = content.get('subheadline', 'Your powerful subheadline')
        cta_text = content.get('cta_text', 'Get Started')
        cta_url = content.get('cta_url', '#')

        return f'''
        <section class="s_hero_minimal py-5 text-center"
                 data-funnel-id="{funnel.id}"
                 data-page-id="{funnel_page.id}">
            <div class="container">
                <div class="row justify-content-center">
                    <div class="col-lg-8">
                        <h1 class="display-4 fw-bold mb-3">{headline}</h1>
                        <p class="lead mb-4">{subheadline}</p>
                        <a href="{cta_url}" class="btn btn-primary btn-lg">{cta_text}</a>
                    </div>
                </div>
            </div>
        </section>
        '''

    def _render_hero_full(self, content, funnel, funnel_page):
        """Render hero_full with AI content."""
        headline = content.get('headline', 'Transform Your Results')
        subheadline = content.get('subheadline', 'Discover the proven system')
        cta_text = content.get('cta_text', 'Start Now')
        cta_url = content.get('cta_url', '#')
        cta2_text = content.get('secondary_cta_text', '')
        cta2_url = content.get('secondary_cta_url', '#')

        secondary_cta = ''
        if cta2_text:
            secondary_cta = f'<a href="{cta2_url}" class="btn btn-outline-secondary btn-lg">{cta2_text}</a>'

        return f'''
        <section class="s_hero_full py-5"
                 data-funnel-id="{funnel.id}"
                 data-page-id="{funnel_page.id}">
            <div class="container">
                <div class="row align-items-center">
                    <div class="col-lg-6">
                        <h1 class="display-4 fw-bold mb-3">{headline}</h1>
                        <p class="lead mb-4">{subheadline}</p>
                        <div class="d-flex gap-3 flex-wrap">
                            <a href="{cta_url}" class="btn btn-primary btn-lg">{cta_text}</a>
                            {secondary_cta}
                        </div>
                    </div>
                    <div class="col-lg-6 mt-4 mt-lg-0">
                        <div class="ratio ratio-16x9 bg-light rounded">
                            <img src="/web/image/website.s_banner_default_image" class="img-fluid rounded" alt=""/>
                        </div>
                    </div>
                </div>
            </div>
        </section>
        '''

    def _render_benefits_stack(self, content, funnel, funnel_page):
        """Render benefits_stack with AI content."""
        headline = content.get('headline', 'What You Will Get')
        items = content.get('items', ['Benefit 1', 'Benefit 2', 'Benefit 3'])

        items_html = ''
        for item in items:
            items_html += f'''
            <div class="col-md-6">
                <div class="d-flex align-items-start mb-3">
                    <span class="text-success me-3 fs-4">✓</span>
                    <span>{item}</span>
                </div>
            </div>
            '''

        return f'''
        <section class="s_benefits_stack py-5"
                 data-funnel-id="{funnel.id}"
                 data-page-id="{funnel_page.id}">
            <div class="container">
                <h2 class="text-center mb-5">{headline}</h2>
                <div class="row">{items_html}</div>
            </div>
        </section>
        '''

    def _render_opt_in_form(self, content, funnel, funnel_page):
        """Render opt_in_form with AI content and integration."""
        headline = content.get('headline', 'Get Instant Access')
        button_text = content.get('button_text', 'Get Access Now')
        fields = content.get('fields', 'name_email')

        integration = 'both' if funnel.mailing_list_id else 'crm'
        redirect_url = funnel_page.redirect_url or '/thank-you'

        name_field = ''
        if fields in ['name_email', 'name_email_phone']:
            name_field = '<input type="text" name="name" class="form-control form-control-lg mb-3" placeholder="Your Name" required/>'

        phone_field = ''
        if fields == 'name_email_phone':
            phone_field = '<input type="tel" name="phone" class="form-control form-control-lg mb-3" placeholder="Your Phone"/>'

        return f'''
        <section class="s_opt_in_form py-5"
                 data-funnel-id="{funnel.id}"
                 data-page-id="{funnel_page.id}"
                 data-integration="{integration}"
                 data-redirect-url="{redirect_url}"
                 data-mailing-list-id="{funnel.mailing_list_id.id if funnel.mailing_list_id else ''}">
            <div class="container">
                <div class="row justify-content-center">
                    <div class="col-lg-6">
                        <div class="card border-0 shadow">
                            <div class="card-body p-4">
                                <h3 class="text-center mb-4">{headline}</h3>
                                <form class="s_funnel_form" action="/funnel/form/submit" method="post">
                                    {name_field}
                                    <input type="email" name="email" class="form-control form-control-lg mb-3" placeholder="Your Email" required/>
                                    {phone_field}
                                    <button type="submit" class="btn btn-primary btn-lg w-100">{button_text}</button>
                                </form>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>
        '''

    # Add more render methods for each snippet type...

    def _link_pages(self, created_pages, page_specs):
        """Link pages for redirect flow."""
        for idx, page_info in enumerate(created_pages[:-1]):
            page = request.env['funnel.page'].browse(page_info['page_id'])
            next_page = created_pages[idx + 1]

            if page_specs[idx].get('redirect_to_next', True):
                page.write({
                    'next_page_id': next_page['page_id'],
                    'redirect_url': next_page['url']
                })

    @http.route('/sam_ai_funnels/generate_copy', type='json', auth='user', methods=['POST'])
    def generate_snippet_copy(self, snippet_type, context, **kwargs):
        """
        Generate copy for a specific snippet type.

        Args:
            snippet_type: 'hero_minimal', 'benefits_stack', etc.
            context: {
                'business_name': 'ACME Corp',
                'product': 'Online Course',
                'target_audience': 'Entrepreneurs',
                'main_benefit': 'Save time',
                'pain_points': ['Overwhelm', 'Lack of clarity'],
                'tone': 'professional but friendly'
            }

        Returns:
            {
                'success': True,
                'copy': {
                    'headline': '...',
                    'subheadline': '...',
                    ...
                }
            }
        """
        try:
            # Get snippet definition for copywriting hints
            snippet = request.env['funnel.snippet'].search([
                ('technical_name', '=', snippet_type)
            ], limit=1)

            if not snippet:
                return {'success': False, 'error': f'Unknown snippet type: {snippet_type}'}

            # Build prompt for Claude
            prompt = self._build_copy_prompt(snippet, context)

            # Call SAM AI service to generate copy
            ai_service = request.env['ai.service']
            response = ai_service.send_message(
                user_message=prompt,
                conversation_id=None,
                context_data={'model': 'funnel.snippet', 'record_id': snippet.id}
            )

            # Parse response into structured copy
            copy = self._parse_copy_response(response, snippet_type)

            return {'success': True, 'copy': copy}

        except Exception as e:
            _logger.error(f"Copy generation error: {str(e)}")
            return {'success': False, 'error': str(e)}

    def _build_copy_prompt(self, snippet, context):
        """Build prompt for generating copy."""
        hints = snippet.copywriting_hints or ''

        return f"""Generate compelling copy for a {snippet.name} section.

COPYWRITING GUIDELINES:
{hints}

BUSINESS CONTEXT:
- Business: {context.get('business_name', 'N/A')}
- Product/Service: {context.get('product', 'N/A')}
- Target Audience: {context.get('target_audience', 'N/A')}
- Main Benefit: {context.get('main_benefit', 'N/A')}
- Pain Points: {', '.join(context.get('pain_points', []))}
- Tone: {context.get('tone', 'professional')}

Generate copy that:
1. Speaks directly to the target audience
2. Addresses their pain points
3. Highlights the main benefit
4. Uses proven direct response formulas
5. Matches the specified tone

Return the copy as JSON with appropriate field names for this snippet type."""

    def _parse_copy_response(self, response, snippet_type):
        """Parse AI response into structured copy."""
        # Attempt to extract JSON from response
        try:
            import re
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except:
            pass

        # Fallback: return response as headline
        return {'headline': response}

    @http.route('/sam_ai_funnels/get_available_templates', type='json', auth='user')
    def get_available_templates(self, **kwargs):
        """Get list of available funnel templates for SAM."""
        templates = request.env['funnel.template'].search([
            ('visibility', 'in', ['company', 'public'])
        ])

        return {
            'templates': [{
                'id': t.id,
                'name': t.name,
                'funnel_type': t.funnel_type,
                'description': t.description,
                'page_count': len(json.loads(t.template_structure or '{}').get('pages', []))
            } for t in templates]
        }

    @http.route('/sam_ai_funnels/get_snippet_library', type='json', auth='user')
    def get_snippet_library(self, **kwargs):
        """Get complete snippet library for SAM."""
        snippets = request.env['funnel.snippet'].search([('active', '=', True)])

        library = {}
        for snippet in snippets:
            category = snippet.category
            if category not in library:
                library[category] = []

            library[category].append({
                'technical_name': snippet.technical_name,
                'name': snippet.name,
                'description': snippet.description,
                'copywriting_hints': snippet.copywriting_hints,
            })

        return {'library': library}
```

---

### 2. SAM Funnel Knowledge File

**File:** `data/sam_funnel_knowledge.xml`

```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <data noupdate="1">

        <!-- SAM AI Knowledge: Funnel Building -->
        <record id="sam_knowledge_funnel_building" model="ai.agent.knowledge">
            <field name="name">Funnel Building Knowledge</field>
            <field name="agent_id" ref="ai_sam.sam_agent_definition"/>
            <field name="category">funnel_building</field>
            <field name="content">
# SAM AI - Funnel Building Knowledge

## INTENT DETECTION

When user mentions any of these, they want to build a funnel:
- "build me a funnel"
- "create a landing page"
- "I need a sales page"
- "set up email capture"
- "lead magnet page"
- "webinar registration"
- "quiz funnel"
- "opt-in page"

## AVAILABLE FUNNEL TYPES

1. **Simple Opt-in** (opt_in)
   - 2 pages: Squeeze + Thank You
   - Use for: Quick email list building
   - Best when: Simple offer, fast launch

2. **Lead Magnet** (lead_magnet)
   - 2 pages: Lead Page + Thank You with tripwire
   - Use for: Free resource offers
   - Best when: Have PDF/guide/checklist to give

3. **Quiz Funnel** (quiz)
   - 5 pages: Intro + Questions + Gate + Results + Offer
   - Use for: Qualifying and segmenting leads
   - Best when: Multiple customer types

4. **Expression of Interest** (eoi)
   - 2 pages: Interest + Confirmation
   - Use for: Pre-launch list building
   - Best when: Product not ready yet

5. **Product Launch** (product_launch)
   - 5 pages: Opt-in + Sales + Order + Upsell + Thank You
   - Use for: Full product sales
   - Best when: Selling courses, programs, products

6. **Webinar** (webinar)
   - 4 pages: Registration + Confirmation + Replay + Sales
   - Use for: Event-based selling
   - Best when: Need to educate before selling

## HOW TO BUILD A FUNNEL

When asked to build a funnel:

1. **Gather context** (ask if not provided):
   - What are you selling?
   - Who is your target audience?
   - What problem do you solve?
   - What's your main benefit?
   - Do you have a lead magnet?

2. **Recommend funnel type** based on their answers

3. **Call the API** to create funnel:
   ```
   POST /sam_ai_funnels/create
   {
     "name": "...",
     "funnel_type": "...",
     "pages": [...]
   }
   ```

4. **Generate copy** for each page section

5. **Return the funnel URL** and next steps

## SNIPPET LIBRARY

### Hero Sections
- hero_minimal: Clean opening, headline + CTA
- hero_full: Hero with media (video/image)
- hero_video: Background video hero

### Problem &amp; Story
- problem_agitation: PAS framework
- story_bridge: Origin story
- before_after: Transformation comparison

### Solution &amp; Benefits
- solution_reveal: Introduce the offer
- benefits_stack: Bullet benefits
- features_grid: Feature cards
- how_it_works: Step-by-step

### Social Proof
- testimonial_single: Single quote
- testimonial_grid: Multiple testimonials
- testimonial_video: Video testimonial
- trust_badges: Logo grid
- case_study_preview: Mini case study
- stats_bar: Impressive numbers

### Offers &amp; Pricing
- offer_breakdown: What's included
- bonus_stack: Additional value
- price_reveal: Pricing display
- pricing_table: Tier comparison
- guarantee: Risk reversal

### CTAs &amp; Forms
- opt_in_form: Email capture
- cta_inline: Mid-page CTA
- cta_button_block: Large button
- final_cta: Bottom CTA
- ps_section: P.S. urgency

### Quiz Elements
- quiz_intro: Start quiz
- quiz_question: Question + answers
- quiz_progress: Progress bar
- quiz_gate: Email before results
- quiz_results: Personalized outcome

### Urgency &amp; Trust
- countdown_timer: Deadline
- urgency_bar: Scarcity message
- objection_handler: FAQ accordion
- risk_reversal: Address fears

### Utility
- spacer: Vertical space
- video_embed: Video player
- divider_styled: Visual separator
- image_text_split: Side-by-side
- bullet_list: Styled list

## COPYWRITING FRAMEWORKS

### Headlines (hero_minimal, hero_full)
- Formula: "[Outcome] Without [Pain Point]"
- Power words: Free, New, Proven, Secret, Discover
- Keep under 10 words

### Problem Agitation (PAS)
1. Problem: "Tired of...", "Frustrated with..."
2. Agitate: "And the worst part?"
3. Solution bridge: "What if there was a way..."

### Benefits (benefits_stack)
- Transform features → outcomes
- Use "So you can..." bridge
- 5-7 bullets optimal

### CTAs
- Action + Outcome
- NOT: "Submit", "Sign Up"
- YES: "Get My Free Guide", "Start My Trial"

### Testimonials
- Include: Name, title, company, photo
- Format: "[Result] + [Timeframe] + [Emotion]"

## API ENDPOINTS

- POST /sam_ai_funnels/create - Create complete funnel
- POST /sam_ai_funnels/generate_copy - Generate snippet copy
- GET /sam_ai_funnels/get_available_templates - List templates
- GET /sam_ai_funnels/get_snippet_library - Get all snippets
            </field>
        </record>

    </data>
</odoo>
```

---

### 3. Update SAM Context Builder

Add funnel awareness to SAM's context builder. Create or update:

**File:** `models/sam_funnel_context.py`

```python
from odoo import models, api


class SamFunnelContext(models.AbstractModel):
    _name = 'sam.funnel.context'
    _description = 'SAM Funnel Building Context'

    @api.model
    def get_funnel_context(self):
        """Get context for SAM when building funnels."""
        return {
            'funnel_types': [
                {'id': 'opt_in', 'name': 'Simple Opt-in', 'pages': 2},
                {'id': 'lead_magnet', 'name': 'Lead Magnet', 'pages': 2},
                {'id': 'quiz', 'name': 'Quiz Funnel', 'pages': 5},
                {'id': 'eoi', 'name': 'Expression of Interest', 'pages': 2},
                {'id': 'product_launch', 'name': 'Product Launch', 'pages': 5},
                {'id': 'webinar', 'name': 'Webinar', 'pages': 4},
            ],
            'snippet_categories': self._get_snippet_categories(),
            'api_endpoint': '/sam_ai_funnels/create',
            'copy_endpoint': '/sam_ai_funnels/generate_copy',
        }

    def _get_snippet_categories(self):
        """Get organized snippet library."""
        snippets = self.env['funnel.snippet'].search([('active', '=', True)])

        categories = {}
        for s in snippets:
            if s.category not in categories:
                categories[s.category] = []
            categories[s.category].append(s.technical_name)

        return categories

    @api.model
    def detect_funnel_intent(self, message):
        """Detect if user message is about building funnels."""
        funnel_keywords = [
            'funnel', 'landing page', 'sales page', 'opt-in',
            'lead magnet', 'webinar', 'quiz', 'squeeze page',
            'email capture', 'conversion', 'signup form'
        ]

        message_lower = message.lower()
        return any(kw in message_lower for kw in funnel_keywords)
```

---

### 4. Update Manifest

```python
{
    # ... existing ...
    'data': [
        # ... existing ...
        'data/sam_funnel_knowledge.xml',
    ],
}
```

Update controllers/__init__.py:
```python
from . import funnel_controller
from . import funnel_form_controller
from . import sam_funnel_api
```

Update models/__init__.py:
```python
# ... existing ...
from . import sam_funnel_context
```

---

## VALIDATION CHECKLIST

- [ ] `/sam_ai_funnels/create` endpoint works
- [ ] `/sam_ai_funnels/generate_copy` generates copy
- [ ] `/sam_ai_funnels/get_available_templates` returns templates
- [ ] `/sam_ai_funnels/get_snippet_library` returns snippets
- [ ] SAM can build funnel via API
- [ ] Generated pages have correct content
- [ ] Form integrations work on AI-created pages
- [ ] SAM knowledge file loaded

---

## NEXT PHASE

After Phase 6 is validated, proceed to Phase 7: Quiz Logic.

---

**END OF PHASE 6 DEVELOPER PROMPT**
