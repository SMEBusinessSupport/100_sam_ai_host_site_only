# Developer Prompt: SAM AI Funnels - Phase 2 (Core Snippets)

**Date:** 2025-12-31
**Phase:** 2 of 7
**Scope:** FUNNELS tab in website builder + 15 MVP snippets
**Prerequisite:** Phase 1 complete and validated

---

## CONTEXT

Phase 1 created the module foundation with 5 data models. Now we add the website builder integration - a new "FUNNELS" tab with 15 core snippets that enable all funnel types.

**Architecture Document:** `D:\SAMAI-18-SaaS\ai_sam\ai_sam_docs\plans\2025-12-31_sam-ai-funnels-architecture.md`

**Odoo 18 Snippet Pattern Reference:**
- Snippets defined in XML templates
- Registered via `options.xml` inheriting `website.snippets`
- Customize options use `<we-*>` components
- JS/SCSS in `static/src/snippets/s_<name>/`

---

## GOAL

Add a FUNNELS tab to the Odoo 18 website builder sidebar with 15 draggable snippets covering all essential funnel components.

---

## 15 MVP SNIPPETS

These 15 snippets enable building ANY of the 6 funnel types:

| # | Snippet | Category | Purpose |
|---|---------|----------|---------|
| 1 | `hero_minimal` | Hero | Opening headline + CTA |
| 2 | `hero_full` | Hero | Full hero with media |
| 3 | `problem_agitation` | Problem & Story | PAS framework section |
| 4 | `benefits_stack` | Solution & Benefits | Bullet benefits list |
| 5 | `testimonial_single` | Social Proof | Single testimonial quote |
| 6 | `opt_in_form` | CTAs & Forms | Email capture form |
| 7 | `cta_inline` | CTAs & Forms | Mid-page CTA |
| 8 | `final_cta` | CTAs & Forms | Bottom page CTA |
| 9 | `offer_breakdown` | Offers & Pricing | What's included list |
| 10 | `price_reveal` | Offers & Pricing | Price with anchor |
| 11 | `guarantee` | Offers & Pricing | Risk reversal badge |
| 12 | `countdown_timer` | Urgency & Trust | Deadline timer |
| 13 | `objection_handler` | Urgency & Trust | FAQ accordion |
| 14 | `spacer` | Utility | Vertical spacing |
| 15 | `video_embed` | Utility | Video player |

---

## DELIVERABLES

### 1. Update __manifest__.py

Add snippet assets to the manifest:

```python
{
    'name': 'SAM AI Funnels',
    'version': '18.0.1.0.0',
    # ... existing fields ...
    'data': [
        # Security
        'security/ir.model.access.csv',

        # Views
        'views/funnel_definition_views.xml',
        'views/funnel_page_views.xml',
        'views/funnel_template_views.xml',
        'views/funnel_snippet_views.xml',
        'views/funnel_menus.xml',

        # Snippets (NEW)
        'views/snippets/options.xml',
        'views/snippets/s_hero_minimal.xml',
        'views/snippets/s_hero_full.xml',
        'views/snippets/s_problem_agitation.xml',
        'views/snippets/s_benefits_stack.xml',
        'views/snippets/s_testimonial_single.xml',
        'views/snippets/s_opt_in_form.xml',
        'views/snippets/s_cta_inline.xml',
        'views/snippets/s_final_cta.xml',
        'views/snippets/s_offer_breakdown.xml',
        'views/snippets/s_price_reveal.xml',
        'views/snippets/s_guarantee.xml',
        'views/snippets/s_countdown_timer.xml',
        'views/snippets/s_objection_handler.xml',
        'views/snippets/s_spacer.xml',
        'views/snippets/s_video_embed.xml',

        # Data
        'data/funnel_snippet_data.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            # Snippet styles
            'sam_ai_funnels/static/src/snippets/s_hero_minimal/000.scss',
            'sam_ai_funnels/static/src/snippets/s_hero_full/000.scss',
            'sam_ai_funnels/static/src/snippets/s_problem_agitation/000.scss',
            'sam_ai_funnels/static/src/snippets/s_benefits_stack/000.scss',
            'sam_ai_funnels/static/src/snippets/s_testimonial_single/000.scss',
            'sam_ai_funnels/static/src/snippets/s_opt_in_form/000.scss',
            'sam_ai_funnels/static/src/snippets/s_cta_inline/000.scss',
            'sam_ai_funnels/static/src/snippets/s_final_cta/000.scss',
            'sam_ai_funnels/static/src/snippets/s_offer_breakdown/000.scss',
            'sam_ai_funnels/static/src/snippets/s_price_reveal/000.scss',
            'sam_ai_funnels/static/src/snippets/s_guarantee/000.scss',
            'sam_ai_funnels/static/src/snippets/s_countdown_timer/000.scss',
            'sam_ai_funnels/static/src/snippets/s_objection_handler/000.scss',
            'sam_ai_funnels/static/src/snippets/s_spacer/000.scss',
            'sam_ai_funnels/static/src/snippets/s_video_embed/000.scss',
            # Countdown timer JS
            'sam_ai_funnels/static/src/snippets/s_countdown_timer/000.js',
            # FAQ accordion JS
            'sam_ai_funnels/static/src/snippets/s_objection_handler/000.js',
        ],
        'website.assets_wysiwyg': [
            # Editor-specific JS for snippet options
            'sam_ai_funnels/static/src/js/funnel_snippet_options.js',
        ],
    },
    # ... rest of manifest ...
}
```

---

### 2. options.xml - FUNNELS Tab Registration

**File:** `views/snippets/options.xml`

```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <!-- ============================================
         FUNNELS TAB - Register in Website Builder
         ============================================ -->

    <!-- Register FUNNELS as a snippet group (creates the tab) -->
    <template id="snippet_groups" inherit_id="website.snippets">
        <xpath expr="//snippets[@id='snippet_groups']" position="inside">
            <t t-snippet="website.s_snippet_group"
               snippet-group="funnels"
               string="Funnels"/>
        </xpath>
    </template>

    <!-- Register all funnel snippets into the FUNNELS tab -->
    <template id="snippets" inherit_id="website.snippets">
        <xpath expr="//snippets[@id='snippet_structure']" position="inside">

            <!-- ===== HERO SECTIONS ===== -->
            <t t-snippet="sam_ai_funnels.s_hero_minimal"
               string="Minimal Hero"
               group="funnels">
                <keywords>hero, headline, minimal, funnel, opening</keywords>
            </t>

            <t t-snippet="sam_ai_funnels.s_hero_full"
               string="Full Hero"
               group="funnels">
                <keywords>hero, headline, video, image, full, media</keywords>
            </t>

            <!-- ===== PROBLEM & STORY ===== -->
            <t t-snippet="sam_ai_funnels.s_problem_agitation"
               string="Problem Agitation"
               group="funnels">
                <keywords>problem, pain, agitation, PAS, story</keywords>
            </t>

            <!-- ===== SOLUTION & BENEFITS ===== -->
            <t t-snippet="sam_ai_funnels.s_benefits_stack"
               string="Benefits Stack"
               group="funnels">
                <keywords>benefits, bullets, features, stack, checkmarks</keywords>
            </t>

            <!-- ===== SOCIAL PROOF ===== -->
            <t t-snippet="sam_ai_funnels.s_testimonial_single"
               string="Single Testimonial"
               group="funnels">
                <keywords>testimonial, quote, review, social proof</keywords>
            </t>

            <!-- ===== CTAs & FORMS ===== -->
            <t t-snippet="sam_ai_funnels.s_opt_in_form"
               string="Opt-in Form"
               group="funnels">
                <keywords>form, email, opt-in, capture, lead, subscribe</keywords>
            </t>

            <t t-snippet="sam_ai_funnels.s_cta_inline"
               string="Inline CTA"
               group="funnels">
                <keywords>cta, button, call to action, inline</keywords>
            </t>

            <t t-snippet="sam_ai_funnels.s_final_cta"
               string="Final CTA"
               group="funnels">
                <keywords>cta, final, bottom, closing, last chance</keywords>
            </t>

            <!-- ===== OFFERS & PRICING ===== -->
            <t t-snippet="sam_ai_funnels.s_offer_breakdown"
               string="Offer Breakdown"
               group="funnels">
                <keywords>offer, breakdown, included, features, value</keywords>
            </t>

            <t t-snippet="sam_ai_funnels.s_price_reveal"
               string="Price Reveal"
               group="funnels">
                <keywords>price, pricing, reveal, anchor, cost</keywords>
            </t>

            <t t-snippet="sam_ai_funnels.s_guarantee"
               string="Guarantee"
               group="funnels">
                <keywords>guarantee, risk, reversal, money back, refund</keywords>
            </t>

            <!-- ===== URGENCY & TRUST ===== -->
            <t t-snippet="sam_ai_funnels.s_countdown_timer"
               string="Countdown Timer"
               group="funnels">
                <keywords>countdown, timer, deadline, urgency, scarcity</keywords>
            </t>

            <t t-snippet="sam_ai_funnels.s_objection_handler"
               string="FAQ / Objections"
               group="funnels">
                <keywords>faq, objection, questions, accordion, answers</keywords>
            </t>

            <!-- ===== UTILITY ===== -->
            <t t-snippet="sam_ai_funnels.s_spacer"
               string="Spacer"
               group="funnels">
                <keywords>spacer, space, gap, divider, utility</keywords>
            </t>

            <t t-snippet="sam_ai_funnels.s_video_embed"
               string="Video Embed"
               group="funnels">
                <keywords>video, embed, youtube, vimeo, player</keywords>
            </t>

        </xpath>
    </template>

    <!-- ============================================
         CUSTOMIZE OPTIONS FOR EACH SNIPPET
         ============================================ -->

    <template id="snippet_options" inherit_id="website.snippet_options">
        <xpath expr="." position="inside">

            <!-- ===== HERO MINIMAL OPTIONS ===== -->
            <div data-selector=".s_hero_minimal">
                <we-input string="Headline" data-attribute-name="data-headline"/>
                <we-input string="Subheadline" data-attribute-name="data-subheadline"/>
                <we-input string="CTA Text" data-attribute-name="data-cta-text"/>
                <we-input string="CTA URL" data-attribute-name="data-cta-url"/>
                <we-select string="CTA Style">
                    <we-button data-select-class="s_btn_primary">Primary</we-button>
                    <we-button data-select-class="s_btn_secondary">Secondary</we-button>
                    <we-button data-select-class="s_btn_outline">Outline</we-button>
                </we-select>
                <we-button-group string="Text Align">
                    <we-button data-select-class="text-start" title="Left"/>
                    <we-button data-select-class="text-center" title="Center"/>
                    <we-button data-select-class="text-end" title="Right"/>
                </we-button-group>
                <we-colorpicker string="Background" data-css-property="background-color"/>
                <we-colorpicker string="Text Color" data-css-property="color"/>
                <we-select string="Padding">
                    <we-button data-select-class="py-3">Small</we-button>
                    <we-button data-select-class="py-5">Medium</we-button>
                    <we-button data-select-class="py-7">Large</we-button>
                </we-select>
            </div>

            <!-- ===== HERO FULL OPTIONS ===== -->
            <div data-selector=".s_hero_full">
                <we-input string="Headline" data-attribute-name="data-headline"/>
                <we-input string="Subheadline" data-attribute-name="data-subheadline"/>
                <we-select string="Media Type">
                    <we-button data-select-class="s_media_none">None</we-button>
                    <we-button data-select-class="s_media_image">Image</we-button>
                    <we-button data-select-class="s_media_video">Video</we-button>
                </we-select>
                <we-select string="Media Position">
                    <we-button data-select-class="s_media_left">Left</we-button>
                    <we-button data-select-class="s_media_right">Right</we-button>
                    <we-button data-select-class="s_media_bg">Background</we-button>
                </we-select>
                <we-input string="CTA Text" data-attribute-name="data-cta-text"/>
                <we-input string="CTA URL" data-attribute-name="data-cta-url"/>
                <we-input string="Secondary CTA" data-attribute-name="data-cta2-text"/>
                <we-input string="Secondary URL" data-attribute-name="data-cta2-url"/>
                <we-colorpicker string="Background" data-css-property="background-color"/>
                <we-select string="Padding">
                    <we-button data-select-class="py-3">Small</we-button>
                    <we-button data-select-class="py-5">Medium</we-button>
                    <we-button data-select-class="py-7">Large</we-button>
                </we-select>
            </div>

            <!-- ===== PROBLEM AGITATION OPTIONS ===== -->
            <div data-selector=".s_problem_agitation">
                <we-input string="Headline" data-attribute-name="data-headline"/>
                <we-colorpicker string="Background" data-css-property="background-color"/>
                <we-colorpicker string="Text Color" data-css-property="color"/>
                <we-select string="Padding">
                    <we-button data-select-class="py-3">Small</we-button>
                    <we-button data-select-class="py-5">Medium</we-button>
                    <we-button data-select-class="py-7">Large</we-button>
                </we-select>
            </div>

            <!-- ===== BENEFITS STACK OPTIONS ===== -->
            <div data-selector=".s_benefits_stack">
                <we-input string="Headline" data-attribute-name="data-headline"/>
                <we-select string="Columns">
                    <we-button data-select-class="s_cols_1">1 Column</we-button>
                    <we-button data-select-class="s_cols_2">2 Columns</we-button>
                    <we-button data-select-class="s_cols_3">3 Columns</we-button>
                </we-select>
                <we-select string="Icon Style">
                    <we-button data-select-class="s_icon_check">Checkmarks</we-button>
                    <we-button data-select-class="s_icon_bullet">Bullets</we-button>
                    <we-button data-select-class="s_icon_arrow">Arrows</we-button>
                </we-select>
                <we-colorpicker string="Icon Color" data-css-property="--icon-color"/>
                <we-colorpicker string="Background" data-css-property="background-color"/>
                <we-select string="Padding">
                    <we-button data-select-class="py-3">Small</we-button>
                    <we-button data-select-class="py-5">Medium</we-button>
                    <we-button data-select-class="py-7">Large</we-button>
                </we-select>
            </div>

            <!-- ===== TESTIMONIAL SINGLE OPTIONS ===== -->
            <div data-selector=".s_testimonial_single">
                <we-select string="Style">
                    <we-button data-select-class="s_style_card">Card</we-button>
                    <we-button data-select-class="s_style_minimal">Minimal</we-button>
                    <we-button data-select-class="s_style_featured">Featured</we-button>
                </we-select>
                <we-checkbox string="Show Rating" data-attribute-name="data-show-rating"/>
                <we-checkbox string="Show Photo" data-attribute-name="data-show-photo"/>
                <we-colorpicker string="Background" data-css-property="background-color"/>
                <we-select string="Padding">
                    <we-button data-select-class="py-3">Small</we-button>
                    <we-button data-select-class="py-5">Medium</we-button>
                    <we-button data-select-class="py-7">Large</we-button>
                </we-select>
            </div>

            <!-- ===== OPT-IN FORM OPTIONS ===== -->
            <div data-selector=".s_opt_in_form">
                <we-input string="Headline" data-attribute-name="data-headline"/>
                <we-input string="Button Text" data-attribute-name="data-button-text"/>
                <we-select string="Form Fields">
                    <we-button data-select-class="s_fields_email">Email Only</we-button>
                    <we-button data-select-class="s_fields_name_email">Name + Email</we-button>
                    <we-button data-select-class="s_fields_full">Name + Email + Phone</we-button>
                </we-select>
                <we-input string="Redirect URL" data-attribute-name="data-redirect-url"/>
                <we-select string="Integration">
                    <we-button data-set-attribute="data-integration" data-value="crm">CRM Lead</we-button>
                    <we-button data-set-attribute="data-integration" data-value="mailing">Mailing List</we-button>
                    <we-button data-set-attribute="data-integration" data-value="both">Both</we-button>
                </we-select>
                <we-input string="Lead Tag" data-attribute-name="data-lead-tag"/>
                <we-colorpicker string="Button Color" data-css-property="--btn-color"/>
                <we-colorpicker string="Background" data-css-property="background-color"/>
                <we-select string="Padding">
                    <we-button data-select-class="py-3">Small</we-button>
                    <we-button data-select-class="py-5">Medium</we-button>
                    <we-button data-select-class="py-7">Large</we-button>
                </we-select>
            </div>

            <!-- ===== CTA INLINE OPTIONS ===== -->
            <div data-selector=".s_cta_inline">
                <we-input string="Headline" data-attribute-name="data-headline"/>
                <we-input string="Subheadline" data-attribute-name="data-subheadline"/>
                <we-input string="CTA Text" data-attribute-name="data-cta-text"/>
                <we-input string="CTA URL" data-attribute-name="data-cta-url"/>
                <we-select string="CTA Style">
                    <we-button data-select-class="s_btn_primary">Primary</we-button>
                    <we-button data-select-class="s_btn_secondary">Secondary</we-button>
                    <we-button data-select-class="s_btn_outline">Outline</we-button>
                </we-select>
                <we-button-group string="Alignment">
                    <we-button data-select-class="text-start"/>
                    <we-button data-select-class="text-center"/>
                    <we-button data-select-class="text-end"/>
                </we-button-group>
                <we-colorpicker string="Background" data-css-property="background-color"/>
                <we-select string="Padding">
                    <we-button data-select-class="py-3">Small</we-button>
                    <we-button data-select-class="py-5">Medium</we-button>
                    <we-button data-select-class="py-7">Large</we-button>
                </we-select>
            </div>

            <!-- ===== FINAL CTA OPTIONS ===== -->
            <div data-selector=".s_final_cta">
                <we-input string="Headline" data-attribute-name="data-headline"/>
                <we-input string="Subheadline" data-attribute-name="data-subheadline"/>
                <we-input string="Urgency Text" data-attribute-name="data-urgency-text"/>
                <we-input string="CTA Text" data-attribute-name="data-cta-text"/>
                <we-input string="CTA URL" data-attribute-name="data-cta-url"/>
                <we-select string="CTA Size">
                    <we-button data-select-class="s_btn_md">Medium</we-button>
                    <we-button data-select-class="s_btn_lg">Large</we-button>
                </we-select>
                <we-select string="Background">
                    <we-button data-select-class="s_bg_solid">Solid Color</we-button>
                    <we-button data-select-class="s_bg_gradient">Gradient</we-button>
                </we-select>
                <we-colorpicker string="Background" data-css-property="background-color"/>
                <we-select string="Padding">
                    <we-button data-select-class="py-4">Medium</we-button>
                    <we-button data-select-class="py-6">Large</we-button>
                </we-select>
            </div>

            <!-- ===== OFFER BREAKDOWN OPTIONS ===== -->
            <div data-selector=".s_offer_breakdown">
                <we-input string="Headline" data-attribute-name="data-headline"/>
                <we-checkbox string="Show Values" data-attribute-name="data-show-values"/>
                <we-input string="Total Value" data-attribute-name="data-total-value"/>
                <we-select string="Checkmark Style">
                    <we-button data-select-class="s_check_default">Default</we-button>
                    <we-button data-select-class="s_check_circle">Circle</we-button>
                    <we-button data-select-class="s_check_square">Square</we-button>
                </we-select>
                <we-colorpicker string="Check Color" data-css-property="--check-color"/>
                <we-colorpicker string="Background" data-css-property="background-color"/>
                <we-select string="Padding">
                    <we-button data-select-class="py-3">Small</we-button>
                    <we-button data-select-class="py-5">Medium</we-button>
                    <we-button data-select-class="py-7">Large</we-button>
                </we-select>
            </div>

            <!-- ===== PRICE REVEAL OPTIONS ===== -->
            <div data-selector=".s_price_reveal">
                <we-input string="Headline" data-attribute-name="data-headline"/>
                <we-input string="Anchor Price" data-attribute-name="data-anchor-price"/>
                <we-input string="Actual Price" data-attribute-name="data-actual-price"/>
                <we-input string="Price Period" data-attribute-name="data-price-period"/>
                <we-input string="Value Statement" data-attribute-name="data-value-statement"/>
                <we-input string="CTA Text" data-attribute-name="data-cta-text"/>
                <we-input string="CTA URL" data-attribute-name="data-cta-url"/>
                <we-checkbox string="Show Payment Icons" data-attribute-name="data-show-payment"/>
                <we-colorpicker string="Background" data-css-property="background-color"/>
                <we-select string="Padding">
                    <we-button data-select-class="py-3">Small</we-button>
                    <we-button data-select-class="py-5">Medium</we-button>
                    <we-button data-select-class="py-7">Large</we-button>
                </we-select>
            </div>

            <!-- ===== GUARANTEE OPTIONS ===== -->
            <div data-selector=".s_guarantee">
                <we-input string="Headline" data-attribute-name="data-headline"/>
                <we-input string="Guarantee Period" data-attribute-name="data-period"/>
                <we-select string="Style">
                    <we-button data-select-class="s_style_badge">Badge</we-button>
                    <we-button data-select-class="s_style_card">Card</we-button>
                    <we-button data-select-class="s_style_minimal">Minimal</we-button>
                </we-select>
                <we-colorpicker string="Badge Color" data-css-property="--badge-color"/>
                <we-colorpicker string="Background" data-css-property="background-color"/>
                <we-select string="Padding">
                    <we-button data-select-class="py-3">Small</we-button>
                    <we-button data-select-class="py-5">Medium</we-button>
                    <we-button data-select-class="py-7">Large</we-button>
                </we-select>
            </div>

            <!-- ===== COUNTDOWN TIMER OPTIONS ===== -->
            <div data-selector=".s_countdown_timer">
                <we-input string="Headline" data-attribute-name="data-headline"/>
                <we-select string="Deadline Type">
                    <we-button data-set-attribute="data-deadline-type" data-value="fixed">Fixed Date</we-button>
                    <we-button data-set-attribute="data-deadline-type" data-value="evergreen">Evergreen</we-button>
                </we-select>
                <we-input string="Deadline Date" data-attribute-name="data-deadline-date"/>
                <we-input string="Evergreen Hours" data-attribute-name="data-evergreen-hours"/>
                <we-select string="Expired Action">
                    <we-button data-set-attribute="data-expired-action" data-value="hide">Hide</we-button>
                    <we-button data-set-attribute="data-expired-action" data-value="message">Show Message</we-button>
                    <we-button data-set-attribute="data-expired-action" data-value="redirect">Redirect</we-button>
                </we-select>
                <we-input string="Expired Message" data-attribute-name="data-expired-message"/>
                <we-input string="Expired Redirect" data-attribute-name="data-expired-redirect"/>
                <we-select string="Style">
                    <we-button data-select-class="s_timer_minimal">Minimal</we-button>
                    <we-button data-select-class="s_timer_boxed">Boxed</we-button>
                    <we-button data-select-class="s_timer_flip">Flip</we-button>
                </we-select>
                <we-colorpicker string="Background" data-css-property="background-color"/>
                <we-select string="Padding">
                    <we-button data-select-class="py-3">Small</we-button>
                    <we-button data-select-class="py-5">Medium</we-button>
                    <we-button data-select-class="py-7">Large</we-button>
                </we-select>
            </div>

            <!-- ===== OBJECTION HANDLER OPTIONS ===== -->
            <div data-selector=".s_objection_handler">
                <we-input string="Headline" data-attribute-name="data-headline"/>
                <we-select string="Style">
                    <we-button data-select-class="s_style_accordion">Accordion</we-button>
                    <we-button data-select-class="s_style_list">List</we-button>
                </we-select>
                <we-select string="Default Expanded">
                    <we-button data-set-attribute="data-expanded" data-value="none">None</we-button>
                    <we-button data-set-attribute="data-expanded" data-value="first">First</we-button>
                    <we-button data-set-attribute="data-expanded" data-value="all">All</we-button>
                </we-select>
                <we-colorpicker string="Background" data-css-property="background-color"/>
                <we-select string="Padding">
                    <we-button data-select-class="py-3">Small</we-button>
                    <we-button data-select-class="py-5">Medium</we-button>
                    <we-button data-select-class="py-7">Large</we-button>
                </we-select>
            </div>

            <!-- ===== SPACER OPTIONS ===== -->
            <div data-selector=".s_spacer">
                <we-select string="Height">
                    <we-button data-select-class="s_spacer_sm">Small (32px)</we-button>
                    <we-button data-select-class="s_spacer_md">Medium (64px)</we-button>
                    <we-button data-select-class="s_spacer_lg">Large (96px)</we-button>
                    <we-button data-select-class="s_spacer_xl">Extra Large (128px)</we-button>
                </we-select>
                <we-colorpicker string="Background" data-css-property="background-color"/>
            </div>

            <!-- ===== VIDEO EMBED OPTIONS ===== -->
            <div data-selector=".s_video_embed">
                <we-input string="Video URL" data-attribute-name="data-video-url"/>
                <we-select string="Video Source">
                    <we-button data-set-attribute="data-source" data-value="youtube">YouTube</we-button>
                    <we-button data-set-attribute="data-source" data-value="vimeo">Vimeo</we-button>
                    <we-button data-set-attribute="data-source" data-value="custom">Custom</we-button>
                </we-select>
                <we-input string="Caption" data-attribute-name="data-caption"/>
                <we-checkbox string="Autoplay" data-attribute-name="data-autoplay"/>
                <we-checkbox string="Show Controls" data-attribute-name="data-controls"/>
                <we-select string="Aspect Ratio">
                    <we-button data-select-class="s_ratio_16_9">16:9</we-button>
                    <we-button data-select-class="s_ratio_4_3">4:3</we-button>
                    <we-button data-select-class="s_ratio_1_1">1:1</we-button>
                </we-select>
                <we-select string="Max Width">
                    <we-button data-select-class="s_width_sm">Small</we-button>
                    <we-button data-select-class="s_width_md">Medium</we-button>
                    <we-button data-select-class="s_width_lg">Large</we-button>
                    <we-button data-select-class="s_width_full">Full</we-button>
                </we-select>
                <we-colorpicker string="Background" data-css-property="background-color"/>
                <we-select string="Padding">
                    <we-button data-select-class="py-3">Small</we-button>
                    <we-button data-select-class="py-5">Medium</we-button>
                    <we-button data-select-class="py-7">Large</we-button>
                </we-select>
            </div>

        </xpath>
    </template>
</odoo>
```

---

### 3. Snippet XML Templates

Create each snippet template. Here are all 15:

#### views/snippets/s_hero_minimal.xml
```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <template id="s_hero_minimal" name="Minimal Hero">
        <section class="s_hero_minimal py-5 text-center"
                 data-snippet="sam_ai_funnels.s_hero_minimal"
                 data-name="Minimal Hero">
            <div class="container">
                <div class="row justify-content-center">
                    <div class="col-lg-8">
                        <h1 class="display-4 fw-bold mb-3" data-oe-field="headline">
                            Your Compelling Headline Here
                        </h1>
                        <p class="lead mb-4" data-oe-field="subheadline">
                            A brief, powerful subheadline that expands on your promise
                        </p>
                        <a href="#" class="btn btn-primary btn-lg" data-oe-field="cta">
                            Get Started Now
                        </a>
                    </div>
                </div>
            </div>
        </section>
    </template>
</odoo>
```

#### views/snippets/s_hero_full.xml
```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <template id="s_hero_full" name="Full Hero">
        <section class="s_hero_full s_media_right py-5"
                 data-snippet="sam_ai_funnels.s_hero_full"
                 data-name="Full Hero">
            <div class="container">
                <div class="row align-items-center">
                    <div class="col-lg-6">
                        <h1 class="display-4 fw-bold mb-3" data-oe-field="headline">
                            Transform Your Results Today
                        </h1>
                        <p class="lead mb-4" data-oe-field="subheadline">
                            Discover the proven system that's helped thousands achieve extraordinary results
                        </p>
                        <div class="d-flex gap-3 flex-wrap">
                            <a href="#" class="btn btn-primary btn-lg" data-oe-field="cta">
                                Start Free Trial
                            </a>
                            <a href="#" class="btn btn-outline-secondary btn-lg" data-oe-field="cta2">
                                Watch Demo
                            </a>
                        </div>
                    </div>
                    <div class="col-lg-6 mt-4 mt-lg-0">
                        <div class="s_hero_media ratio ratio-16x9 bg-light rounded">
                            <img src="/web/image/website.s_banner_default_image"
                                 class="img-fluid rounded"
                                 alt="Hero Image"
                                 data-oe-field="media"/>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    </template>
</odoo>
```

#### views/snippets/s_problem_agitation.xml
```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <template id="s_problem_agitation" name="Problem Agitation">
        <section class="s_problem_agitation py-5"
                 data-snippet="sam_ai_funnels.s_problem_agitation"
                 data-name="Problem Agitation">
            <div class="container">
                <div class="row justify-content-center">
                    <div class="col-lg-8">
                        <h2 class="h3 mb-4" data-oe-field="headline">
                            Are You Tired Of...
                        </h2>
                        <ul class="s_pain_points list-unstyled" data-oe-field="pain_points">
                            <li class="mb-3 d-flex align-items-start">
                                <span class="text-danger me-2">&#10007;</span>
                                <span>Struggling to get consistent results despite working harder than ever?</span>
                            </li>
                            <li class="mb-3 d-flex align-items-start">
                                <span class="text-danger me-2">&#10007;</span>
                                <span>Watching competitors succeed while you feel stuck in the same place?</span>
                            </li>
                            <li class="mb-3 d-flex align-items-start">
                                <span class="text-danger me-2">&#10007;</span>
                                <span>Feeling overwhelmed by all the conflicting advice out there?</span>
                            </li>
                        </ul>
                        <div class="s_agitation mt-4 p-4 bg-light rounded" data-oe-field="agitation">
                            <p class="mb-0 fst-italic">
                                And the worst part? Every day that passes, you're falling further behind while the solution might be simpler than you think...
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    </template>
</odoo>
```

#### views/snippets/s_benefits_stack.xml
```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <template id="s_benefits_stack" name="Benefits Stack">
        <section class="s_benefits_stack s_cols_2 s_icon_check py-5"
                 data-snippet="sam_ai_funnels.s_benefits_stack"
                 data-name="Benefits Stack">
            <div class="container">
                <h2 class="text-center mb-5" data-oe-field="headline">
                    What You'll Get
                </h2>
                <div class="row g-4">
                    <div class="col-md-6">
                        <div class="s_benefit d-flex align-items-start">
                            <span class="s_benefit_icon me-3 text-success fs-4">&#10003;</span>
                            <div>
                                <strong>Proven Framework</strong>
                                <p class="mb-0 text-muted">Step-by-step system you can implement today</p>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="s_benefit d-flex align-items-start">
                            <span class="s_benefit_icon me-3 text-success fs-4">&#10003;</span>
                            <div>
                                <strong>Expert Support</strong>
                                <p class="mb-0 text-muted">Direct access to our team whenever you need help</p>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="s_benefit d-flex align-items-start">
                            <span class="s_benefit_icon me-3 text-success fs-4">&#10003;</span>
                            <div>
                                <strong>Time-Saving Templates</strong>
                                <p class="mb-0 text-muted">Done-for-you resources to accelerate results</p>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="s_benefit d-flex align-items-start">
                            <span class="s_benefit_icon me-3 text-success fs-4">&#10003;</span>
                            <div>
                                <strong>Lifetime Updates</strong>
                                <p class="mb-0 text-muted">Always have access to the latest strategies</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    </template>
</odoo>
```

#### views/snippets/s_testimonial_single.xml
```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <template id="s_testimonial_single" name="Single Testimonial">
        <section class="s_testimonial_single s_style_card py-5"
                 data-snippet="sam_ai_funnels.s_testimonial_single"
                 data-name="Single Testimonial">
            <div class="container">
                <div class="row justify-content-center">
                    <div class="col-lg-8">
                        <div class="card border-0 shadow-sm">
                            <div class="card-body p-4 p-md-5">
                                <div class="s_rating mb-3" data-oe-field="rating">
                                    <span class="text-warning">&#9733;&#9733;&#9733;&#9733;&#9733;</span>
                                </div>
                                <blockquote class="mb-4">
                                    <p class="lead fst-italic" data-oe-field="quote">
                                        "This completely transformed how I approach my business. Within 90 days, I doubled my revenue and finally have the freedom I always dreamed of."
                                    </p>
                                </blockquote>
                                <div class="d-flex align-items-center">
                                    <img src="/web/image/website.s_banner_default_image"
                                         class="rounded-circle me-3"
                                         width="60"
                                         height="60"
                                         alt="Author"
                                         data-oe-field="photo"/>
                                    <div>
                                        <strong data-oe-field="name">Sarah Johnson</strong>
                                        <p class="mb-0 text-muted small" data-oe-field="title">
                                            CEO, Growth Marketing Co.
                                        </p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    </template>
</odoo>
```

#### views/snippets/s_opt_in_form.xml
```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <template id="s_opt_in_form" name="Opt-in Form">
        <section class="s_opt_in_form s_fields_name_email py-5"
                 data-snippet="sam_ai_funnels.s_opt_in_form"
                 data-name="Opt-in Form"
                 data-integration="crm">
            <div class="container">
                <div class="row justify-content-center">
                    <div class="col-lg-6">
                        <div class="card border-0 shadow">
                            <div class="card-body p-4 p-md-5">
                                <h3 class="text-center mb-4" data-oe-field="headline">
                                    Get Your Free Guide
                                </h3>
                                <form class="s_funnel_form"
                                      action="/funnel/form/submit"
                                      method="post">
                                    <input type="hidden" name="csrf_token" t-att-value="request.csrf_token()"/>
                                    <div class="s_field_name mb-3">
                                        <input type="text"
                                               name="name"
                                               class="form-control form-control-lg"
                                               placeholder="Your Name"
                                               required="required"/>
                                    </div>
                                    <div class="s_field_email mb-3">
                                        <input type="email"
                                               name="email"
                                               class="form-control form-control-lg"
                                               placeholder="Your Email"
                                               required="required"/>
                                    </div>
                                    <div class="s_field_phone mb-3" style="display: none;">
                                        <input type="tel"
                                               name="phone"
                                               class="form-control form-control-lg"
                                               placeholder="Your Phone"/>
                                    </div>
                                    <button type="submit"
                                            class="btn btn-primary btn-lg w-100"
                                            data-oe-field="button">
                                        Get Instant Access
                                    </button>
                                    <p class="text-center text-muted small mt-3 mb-0" data-oe-field="privacy">
                                        We respect your privacy. Unsubscribe anytime.
                                    </p>
                                </form>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    </template>
</odoo>
```

#### views/snippets/s_cta_inline.xml
```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <template id="s_cta_inline" name="Inline CTA">
        <section class="s_cta_inline s_btn_primary py-4 text-center"
                 data-snippet="sam_ai_funnels.s_cta_inline"
                 data-name="Inline CTA">
            <div class="container">
                <div class="row justify-content-center align-items-center">
                    <div class="col-lg-8">
                        <h3 class="mb-2" data-oe-field="headline">
                            Ready to Get Started?
                        </h3>
                        <p class="mb-3 text-muted" data-oe-field="subheadline">
                            Join thousands who've already transformed their results
                        </p>
                        <a href="#" class="btn btn-primary btn-lg" data-oe-field="cta">
                            Yes, I Want This!
                        </a>
                    </div>
                </div>
            </div>
        </section>
    </template>
</odoo>
```

#### views/snippets/s_final_cta.xml
```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <template id="s_final_cta" name="Final CTA">
        <section class="s_final_cta s_btn_lg s_bg_gradient py-5 text-center text-white"
                 data-snippet="sam_ai_funnels.s_final_cta"
                 data-name="Final CTA"
                 style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
            <div class="container">
                <div class="row justify-content-center">
                    <div class="col-lg-8">
                        <h2 class="display-5 fw-bold mb-3" data-oe-field="headline">
                            Don't Wait Another Day
                        </h2>
                        <p class="lead mb-2" data-oe-field="subheadline">
                            Your transformation starts with a single click
                        </p>
                        <p class="small mb-4 opacity-75" data-oe-field="urgency">
                            Limited spots available - Offer ends soon
                        </p>
                        <a href="#" class="btn btn-light btn-lg px-5 py-3" data-oe-field="cta">
                            Claim My Spot Now
                        </a>
                    </div>
                </div>
            </div>
        </section>
    </template>
</odoo>
```

#### views/snippets/s_offer_breakdown.xml
```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <template id="s_offer_breakdown" name="Offer Breakdown">
        <section class="s_offer_breakdown s_check_default py-5"
                 data-snippet="sam_ai_funnels.s_offer_breakdown"
                 data-name="Offer Breakdown"
                 data-show-values="true">
            <div class="container">
                <div class="row justify-content-center">
                    <div class="col-lg-8">
                        <h2 class="text-center mb-5" data-oe-field="headline">
                            Everything You Get Today
                        </h2>
                        <ul class="list-unstyled" data-oe-field="items">
                            <li class="d-flex justify-content-between align-items-center py-3 border-bottom">
                                <div class="d-flex align-items-center">
                                    <span class="text-success me-3 fs-5">&#10003;</span>
                                    <div>
                                        <strong>Complete Video Training Course</strong>
                                        <p class="mb-0 small text-muted">12 modules of step-by-step instruction</p>
                                    </div>
                                </div>
                                <span class="s_item_value badge bg-secondary">$497 Value</span>
                            </li>
                            <li class="d-flex justify-content-between align-items-center py-3 border-bottom">
                                <div class="d-flex align-items-center">
                                    <span class="text-success me-3 fs-5">&#10003;</span>
                                    <div>
                                        <strong>Done-For-You Templates</strong>
                                        <p class="mb-0 small text-muted">Ready to use, just fill in the blanks</p>
                                    </div>
                                </div>
                                <span class="s_item_value badge bg-secondary">$297 Value</span>
                            </li>
                            <li class="d-flex justify-content-between align-items-center py-3 border-bottom">
                                <div class="d-flex align-items-center">
                                    <span class="text-success me-3 fs-5">&#10003;</span>
                                    <div>
                                        <strong>Private Community Access</strong>
                                        <p class="mb-0 small text-muted">Connect with fellow members</p>
                                    </div>
                                </div>
                                <span class="s_item_value badge bg-secondary">$197 Value</span>
                            </li>
                            <li class="d-flex justify-content-between align-items-center py-3">
                                <div class="d-flex align-items-center">
                                    <span class="text-success me-3 fs-5">&#10003;</span>
                                    <div>
                                        <strong>Lifetime Updates</strong>
                                        <p class="mb-0 small text-muted">Always get the latest version</p>
                                    </div>
                                </div>
                                <span class="s_item_value badge bg-secondary">Priceless</span>
                            </li>
                        </ul>
                        <div class="text-center mt-4 p-3 bg-light rounded">
                            <span class="text-muted">Total Value: </span>
                            <strong class="fs-4" data-oe-field="total">$991+</strong>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    </template>
</odoo>
```

#### views/snippets/s_price_reveal.xml
```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <template id="s_price_reveal" name="Price Reveal">
        <section class="s_price_reveal py-5 text-center"
                 data-snippet="sam_ai_funnels.s_price_reveal"
                 data-name="Price Reveal">
            <div class="container">
                <div class="row justify-content-center">
                    <div class="col-lg-6">
                        <h2 class="mb-4" data-oe-field="headline">
                            Your Investment Today
                        </h2>
                        <div class="s_price_display mb-4">
                            <span class="s_anchor_price text-muted text-decoration-line-through fs-4"
                                  data-oe-field="anchor">$997</span>
                            <div class="s_actual_price">
                                <span class="display-3 fw-bold text-primary" data-oe-field="price">$297</span>
                                <span class="text-muted" data-oe-field="period">/one-time</span>
                            </div>
                        </div>
                        <p class="text-muted mb-4" data-oe-field="value_statement">
                            Less than the cost of one consultation - and you get lifetime access
                        </p>
                        <a href="#" class="btn btn-primary btn-lg px-5" data-oe-field="cta">
                            Get Instant Access
                        </a>
                        <div class="s_payment_icons mt-3" data-oe-field="payment_icons">
                            <small class="text-muted">
                                <i class="fa fa-lock me-1"></i> Secure Payment
                                <span class="mx-2">|</span>
                                <i class="fa fa-credit-card me-1"></i> All Major Cards Accepted
                            </small>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    </template>
</odoo>
```

#### views/snippets/s_guarantee.xml
```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <template id="s_guarantee" name="Guarantee">
        <section class="s_guarantee s_style_badge py-5"
                 data-snippet="sam_ai_funnels.s_guarantee"
                 data-name="Guarantee">
            <div class="container">
                <div class="row justify-content-center">
                    <div class="col-lg-8">
                        <div class="d-flex align-items-center justify-content-center flex-column flex-md-row text-center text-md-start">
                            <div class="s_guarantee_badge mb-3 mb-md-0 me-md-4">
                                <div class="rounded-circle bg-success text-white d-flex align-items-center justify-content-center"
                                     style="width: 100px; height: 100px;">
                                    <div class="text-center">
                                        <div class="fw-bold" data-oe-field="period">30-Day</div>
                                        <small>Guarantee</small>
                                    </div>
                                </div>
                            </div>
                            <div>
                                <h3 class="h4 mb-2" data-oe-field="headline">
                                    100% Money-Back Guarantee
                                </h3>
                                <p class="mb-0 text-muted" data-oe-field="text">
                                    Try it risk-free for 30 days. If you're not completely satisfied with your results, simply let us know and we'll refund every penny. No questions asked, no hard feelings.
                                </p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    </template>
</odoo>
```

#### views/snippets/s_countdown_timer.xml
```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <template id="s_countdown_timer" name="Countdown Timer">
        <section class="s_countdown_timer s_timer_boxed py-4"
                 data-snippet="sam_ai_funnels.s_countdown_timer"
                 data-name="Countdown Timer"
                 data-deadline-type="evergreen"
                 data-evergreen-hours="48"
                 data-expired-action="hide">
            <div class="container">
                <div class="row justify-content-center">
                    <div class="col-lg-8 text-center">
                        <p class="mb-3 fw-bold text-danger" data-oe-field="headline">
                            This Special Offer Expires In:
                        </p>
                        <div class="s_timer_display d-flex justify-content-center gap-3">
                            <div class="s_timer_unit bg-dark text-white rounded p-3">
                                <div class="s_timer_days display-6 fw-bold">00</div>
                                <small>Days</small>
                            </div>
                            <div class="s_timer_unit bg-dark text-white rounded p-3">
                                <div class="s_timer_hours display-6 fw-bold">00</div>
                                <small>Hours</small>
                            </div>
                            <div class="s_timer_unit bg-dark text-white rounded p-3">
                                <div class="s_timer_minutes display-6 fw-bold">00</div>
                                <small>Minutes</small>
                            </div>
                            <div class="s_timer_unit bg-dark text-white rounded p-3">
                                <div class="s_timer_seconds display-6 fw-bold">00</div>
                                <small>Seconds</small>
                            </div>
                        </div>
                        <div class="s_expired_message mt-3" style="display: none;">
                            <p class="text-danger fw-bold" data-oe-field="expired_message">
                                This offer has expired!
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    </template>
</odoo>
```

#### views/snippets/s_objection_handler.xml
```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <template id="s_objection_handler" name="FAQ / Objections">
        <section class="s_objection_handler s_style_accordion py-5"
                 data-snippet="sam_ai_funnels.s_objection_handler"
                 data-name="FAQ / Objections"
                 data-expanded="first">
            <div class="container">
                <div class="row justify-content-center">
                    <div class="col-lg-8">
                        <h2 class="text-center mb-5" data-oe-field="headline">
                            Frequently Asked Questions
                        </h2>
                        <div class="accordion" id="faqAccordion" data-oe-field="faqs">
                            <div class="accordion-item">
                                <h3 class="accordion-header">
                                    <button class="accordion-button" type="button"
                                            data-bs-toggle="collapse" data-bs-target="#faq1">
                                        How quickly will I see results?
                                    </button>
                                </h3>
                                <div id="faq1" class="accordion-collapse collapse show"
                                     data-bs-parent="#faqAccordion">
                                    <div class="accordion-body">
                                        Most customers start seeing improvements within the first week. However, the full transformation typically happens within 30-90 days depending on how consistently you apply the system.
                                    </div>
                                </div>
                            </div>
                            <div class="accordion-item">
                                <h3 class="accordion-header">
                                    <button class="accordion-button collapsed" type="button"
                                            data-bs-toggle="collapse" data-bs-target="#faq2">
                                        What if this doesn't work for me?
                                    </button>
                                </h3>
                                <div id="faq2" class="accordion-collapse collapse"
                                     data-bs-parent="#faqAccordion">
                                    <div class="accordion-body">
                                        We offer a full 30-day money-back guarantee. If you're not satisfied for any reason, just let us know and we'll refund your investment completely.
                                    </div>
                                </div>
                            </div>
                            <div class="accordion-item">
                                <h3 class="accordion-header">
                                    <button class="accordion-button collapsed" type="button"
                                            data-bs-toggle="collapse" data-bs-target="#faq3">
                                        How much time do I need to invest?
                                    </button>
                                </h3>
                                <div id="faq3" class="accordion-collapse collapse"
                                     data-bs-parent="#faqAccordion">
                                    <div class="accordion-body">
                                        We recommend setting aside 30-60 minutes per day to go through the training and implement what you learn. The more consistent you are, the faster you'll see results.
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    </template>
</odoo>
```

#### views/snippets/s_spacer.xml
```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <template id="s_spacer" name="Spacer">
        <section class="s_spacer s_spacer_md"
                 data-snippet="sam_ai_funnels.s_spacer"
                 data-name="Spacer">
            <!-- Empty spacer element -->
        </section>
    </template>
</odoo>
```

#### views/snippets/s_video_embed.xml
```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <template id="s_video_embed" name="Video Embed">
        <section class="s_video_embed s_ratio_16_9 s_width_lg py-5"
                 data-snippet="sam_ai_funnels.s_video_embed"
                 data-name="Video Embed"
                 data-source="youtube"
                 data-controls="true">
            <div class="container">
                <div class="row justify-content-center">
                    <div class="col-lg-10">
                        <div class="s_video_wrapper ratio ratio-16x9 bg-dark rounded overflow-hidden">
                            <iframe src="https://www.youtube.com/embed/dQw4w9WgXcQ"
                                    title="Video"
                                    frameborder="0"
                                    allowfullscreen="allowfullscreen"
                                    data-oe-field="video"></iframe>
                        </div>
                        <p class="text-center text-muted mt-3" data-oe-field="caption">
                            Watch this short video to see how it works
                        </p>
                    </div>
                </div>
            </div>
        </section>
    </template>
</odoo>
```

---

### 4. SCSS Files

Create SCSS files for each snippet. Here are the key ones:

#### static/src/snippets/s_hero_minimal/000.scss
```scss
.s_hero_minimal {
    &.py-3 { padding-top: 1.5rem !important; padding-bottom: 1.5rem !important; }
    &.py-5 { padding-top: 3rem !important; padding-bottom: 3rem !important; }
    &.py-7 { padding-top: 5rem !important; padding-bottom: 5rem !important; }

    h1 {
        line-height: 1.2;
    }

    .btn-lg {
        padding: 0.75rem 2rem;
        font-size: 1.1rem;
    }

    &.s_btn_primary .btn { @extend .btn-primary; }
    &.s_btn_secondary .btn { @extend .btn-secondary; }
    &.s_btn_outline .btn { @extend .btn-outline-primary; }
}
```

#### static/src/snippets/s_opt_in_form/000.scss
```scss
.s_opt_in_form {
    --btn-color: var(--primary);

    .form-control-lg {
        padding: 0.75rem 1rem;
        font-size: 1rem;
    }

    .btn {
        background-color: var(--btn-color);
        border-color: var(--btn-color);
    }

    // Field visibility based on class
    &.s_fields_email {
        .s_field_name, .s_field_phone { display: none !important; }
    }

    &.s_fields_name_email {
        .s_field_phone { display: none !important; }
    }

    &.s_fields_full {
        .s_field_name, .s_field_email, .s_field_phone { display: block !important; }
    }
}
```

#### static/src/snippets/s_countdown_timer/000.scss
```scss
.s_countdown_timer {
    .s_timer_unit {
        min-width: 80px;
    }

    &.s_timer_minimal {
        .s_timer_unit {
            background: transparent !important;
            color: inherit !important;
        }
    }

    &.s_timer_boxed {
        .s_timer_unit {
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
    }

    &.s_timer_flip {
        .s_timer_unit {
            perspective: 200px;
            .display-6 {
                transform-style: preserve-3d;
            }
        }
    }
}
```

#### static/src/snippets/s_spacer/000.scss
```scss
.s_spacer {
    &.s_spacer_sm { height: 32px; }
    &.s_spacer_md { height: 64px; }
    &.s_spacer_lg { height: 96px; }
    &.s_spacer_xl { height: 128px; }
}
```

*(Create similar SCSS files for all 15 snippets)*

---

### 5. JavaScript Files

#### static/src/snippets/s_countdown_timer/000.js
```javascript
/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.FunnelCountdownTimer = publicWidget.Widget.extend({
    selector: '.s_countdown_timer',

    start: function () {
        this._super.apply(this, arguments);
        this._initTimer();
        return Promise.resolve();
    },

    _initTimer: function () {
        const $el = this.$el;
        const deadlineType = $el.data('deadline-type') || 'evergreen';
        const expiredAction = $el.data('expired-action') || 'hide';

        let deadline;

        if (deadlineType === 'fixed') {
            deadline = new Date($el.data('deadline-date')).getTime();
        } else {
            // Evergreen timer - uses localStorage to persist
            const storageKey = 'funnel_timer_' + $el.closest('section').attr('id');
            let stored = localStorage.getItem(storageKey);

            if (stored) {
                deadline = parseInt(stored);
            } else {
                const hours = parseInt($el.data('evergreen-hours')) || 48;
                deadline = Date.now() + (hours * 60 * 60 * 1000);
                localStorage.setItem(storageKey, deadline);
            }
        }

        this._updateTimer(deadline, expiredAction);
        this.timerInterval = setInterval(() => {
            this._updateTimer(deadline, expiredAction);
        }, 1000);
    },

    _updateTimer: function (deadline, expiredAction) {
        const now = Date.now();
        const diff = deadline - now;

        if (diff <= 0) {
            this._handleExpired(expiredAction);
            return;
        }

        const days = Math.floor(diff / (1000 * 60 * 60 * 24));
        const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((diff % (1000 * 60)) / 1000);

        this.$('.s_timer_days').text(String(days).padStart(2, '0'));
        this.$('.s_timer_hours').text(String(hours).padStart(2, '0'));
        this.$('.s_timer_minutes').text(String(minutes).padStart(2, '0'));
        this.$('.s_timer_seconds').text(String(seconds).padStart(2, '0'));
    },

    _handleExpired: function (action) {
        clearInterval(this.timerInterval);

        switch (action) {
            case 'hide':
                this.$el.slideUp();
                break;
            case 'message':
                this.$('.s_timer_display').hide();
                this.$('.s_expired_message').show();
                break;
            case 'redirect':
                const url = this.$el.data('expired-redirect');
                if (url) window.location.href = url;
                break;
        }
    },

    destroy: function () {
        if (this.timerInterval) {
            clearInterval(this.timerInterval);
        }
        this._super.apply(this, arguments);
    },
});

export default publicWidget.registry.FunnelCountdownTimer;
```

#### static/src/snippets/s_objection_handler/000.js
```javascript
/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.FunnelObjectionHandler = publicWidget.Widget.extend({
    selector: '.s_objection_handler',

    start: function () {
        this._super.apply(this, arguments);
        this._initAccordion();
        return Promise.resolve();
    },

    _initAccordion: function () {
        const expanded = this.$el.data('expanded') || 'none';

        if (expanded === 'first') {
            this.$('.accordion-collapse').first().addClass('show');
            this.$('.accordion-button').first().removeClass('collapsed');
        } else if (expanded === 'all') {
            this.$('.accordion-collapse').addClass('show');
            this.$('.accordion-button').removeClass('collapsed');
        } else {
            this.$('.accordion-collapse').removeClass('show');
            this.$('.accordion-button').addClass('collapsed');
        }
    },
});

export default publicWidget.registry.FunnelObjectionHandler;
```

---

## VALIDATION CHECKLIST

After implementation, verify:

- [ ] Module upgrades without errors
- [ ] FUNNELS tab appears in website builder sidebar
- [ ] All 15 snippets appear in FUNNELS tab
- [ ] Snippets can be dragged to page
- [ ] Customize panel shows options when snippet selected
- [ ] All customize options work (colors, text, selections)
- [ ] Countdown timer counts down correctly
- [ ] FAQ accordion expands/collapses
- [ ] Snippets are responsive on mobile
- [ ] No JavaScript errors in console

---

## FILES TO CREATE (Summary)

**XML (17 files):**
1. `views/snippets/options.xml`
2. `views/snippets/s_hero_minimal.xml`
3. `views/snippets/s_hero_full.xml`
4. `views/snippets/s_problem_agitation.xml`
5. `views/snippets/s_benefits_stack.xml`
6. `views/snippets/s_testimonial_single.xml`
7. `views/snippets/s_opt_in_form.xml`
8. `views/snippets/s_cta_inline.xml`
9. `views/snippets/s_final_cta.xml`
10. `views/snippets/s_offer_breakdown.xml`
11. `views/snippets/s_price_reveal.xml`
12. `views/snippets/s_guarantee.xml`
13. `views/snippets/s_countdown_timer.xml`
14. `views/snippets/s_objection_handler.xml`
15. `views/snippets/s_spacer.xml`
16. `views/snippets/s_video_embed.xml`

**SCSS (15 files):**
17-31. `static/src/snippets/s_*/000.scss` (one per snippet)

**JS (2 files):**
32. `static/src/snippets/s_countdown_timer/000.js`
33. `static/src/snippets/s_objection_handler/000.js`

**Update:**
34. `__manifest__.py` (add new files to data and assets)

---

## NEXT PHASE

After Phase 2 is validated, proceed to Phase 3: Form Integration.
Phase 3 will cover:
- Form submission controller
- CRM lead creation
- Mailing list integration
- UTM tracking
- Conversion events

---

**END OF PHASE 2 DEVELOPER PROMPT**
