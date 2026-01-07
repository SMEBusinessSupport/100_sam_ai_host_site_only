# SAM AI Funnels - Master Implementation Guide

**Date**: 2025-12-31
**Module**: sam_ai_funnels
**Status**: Ready for Implementation
**Total Phases**: 7

---

## Executive Summary

This guide coordinates the implementation of the SAM AI Funnels module - a complete sales funnel builder integrated into Odoo 18's website builder. The module adds a FUNNELS tab with 46 drag-and-drop snippets, 6 funnel templates, and deep SAM AI integration for conversational funnel building and direct response copywriting.

---

## Quick Reference

### Document Locations
All documents are in: `D:\SAMAI-18-SaaS\ai_sam\ai_sam_docs\plans\`

| Document | Purpose |
|----------|---------|
| `2025-12-31_sam-ai-funnels-architecture.md` | Master architecture, models, integration points |
| `2025-12-31_funnels-phase1-developer-prompt.md` | Foundation: module skeleton, all 5 models, views |
| `2025-12-31_funnels-phase2-developer-prompt.md` | FUNNELS tab + 15 MVP snippets |
| `2025-12-31_funnels-phase3-developer-prompt.md` | Form controller, CRM/mailing integration |
| `2025-12-31_funnels-phase4-developer-prompt.md` | 6 funnel templates, wizard, dashboard |
| `2025-12-31_funnels-phase5-developer-prompt.md` | Remaining 31 snippets |
| `2025-12-31_funnels-phase6-developer-prompt.md` | SAM AI API, copy generation, knowledge |
| `2025-12-31_funnels-phase7-developer-prompt.md` | Quiz logic, branching, personalization |

### Requirements Source
`D:\SAMAI-18-SaaS\The SAM Sales System\Gold Star Direction\FUNNELS-TAB-REQUIREMENTS.md`

---

## Implementation Order

```
Phase 1 ──► Phase 2 ──► Phase 3 ──► Phase 4
   │                                    │
   │         CORE FUNCTIONALITY         │
   └────────────────────────────────────┘
                    │
                    ▼
Phase 5 ──► Phase 6 ──► Phase 7
   │                       │
   │    ENHANCEMENT        │
   └───────────────────────┘
```

**CRITICAL**: Phases must be completed in order. Each phase depends on the previous.

---

## Phase-by-Phase Summary

### Phase 1: Foundation (MUST DO FIRST)
**Files**: 18 | **Estimated Effort**: High

Creates:
- Complete module skeleton with `__manifest__.py`
- All 5 Python models:
  - `funnel.definition` - Main funnel entity
  - `funnel.page` - Individual funnel pages
  - `funnel.template` - Reusable templates
  - `funnel.snippet` - Snippet registry
  - `funnel.conversion` - Analytics tracking
- All view XMLs (tree, form, kanban)
- Security rules and access rights
- Menu structure

**Validation**:
- [ ] Module installs without errors
- [ ] All models appear in Settings > Technical > Models
- [ ] Menu "Website > Funnels" accessible
- [ ] Can create/edit funnel records

---

### Phase 2: Core Snippets
**Files**: 21 | **Estimated Effort**: High

Creates:
- FUNNELS tab in website builder (options.xml)
- 15 MVP snippets:
  - `s_funnel_hero` - Hero with headline/CTA
  - `s_funnel_headline_subhead` - Headline section
  - `s_funnel_video_embed` - Video with optional gate
  - `s_funnel_opt_in_form` - Email capture form
  - `s_funnel_bullet_benefits` - Feature list
  - `s_funnel_testimonial_single` - Single testimonial
  - `s_funnel_testimonial_grid` - 3-column testimonials
  - `s_funnel_cta_button` - Call-to-action
  - `s_funnel_guarantee_badge` - Trust badge
  - `s_funnel_countdown_timer` - Urgency timer
  - `s_funnel_about_author` - Credibility section
  - `s_funnel_faq_accordion` - FAQ section
  - `s_funnel_simple_footer` - Minimal footer
  - `s_funnel_progress_bar` - Step indicator
  - `s_funnel_social_proof` - Social proof strip
- SCSS stylesheets
- Customize panel options
- JavaScript for countdown/FAQ

**Validation**:
- [ ] FUNNELS tab appears in website builder
- [ ] All 15 snippets drag onto page
- [ ] Customize panel opens for each
- [ ] Countdown timer counts down
- [ ] FAQ accordion expands/collapses

---

### Phase 3: Form Integration
**Files**: 3 | **Estimated Effort**: Medium

Creates:
- `funnel_form_controller.py` - Form submission handling
- CRM lead creation with:
  - Name, email, phone capture
  - Tag assignment
  - Sales team routing
  - UTM parameter capture
- Mailing list integration:
  - Contact creation
  - List subscription
- Conversion tracking
- AJAX form submission JS

**Validation**:
- [ ] Form submissions create CRM leads
- [ ] Leads have correct tags and team
- [ ] Contacts added to mailing list
- [ ] UTM parameters captured
- [ ] Conversions recorded in funnel.conversion

---

### Phase 4: Complete Funnels
**Files**: 3 | **Estimated Effort**: Medium

Creates:
- 6 funnel templates as XML data:
  1. Simple Opt-in (2 pages)
  2. Lead Magnet (3 pages)
  3. Quiz Funnel (5 pages)
  4. Expression of Interest (3 pages)
  5. Product Launch (4 pages)
  6. Webinar Registration (4 pages)
- Funnel generator wizard
- Dashboard views (kanban, pivot, graph)
- Conversion analytics

**Validation**:
- [ ] 6 templates appear in template list
- [ ] Wizard generates multi-page funnel
- [ ] Generated pages have correct snippets
- [ ] Dashboard shows conversion data

---

### Phase 5: Remaining Snippets
**Files**: 62+ | **Estimated Effort**: High

Creates remaining 31 snippets:
- **Headers (6)**: headline, subhead, pre-head, video, quote, scroll
- **Social Proof (6)**: results, case study, logo bar, counter, rating, media
- **Credibility (5)**: photo bio, founder story, timeline, credentials, values
- **Content (5)**: problem, solution reveal, feature table, comparison, checklist
- **Quiz Elements (5)**: question card, progress, result, branch, score
- **Conversion (4)**: value stack, pricing, order bump, exit popup

**Validation**:
- [ ] All 46 snippets appear in FUNNELS tab
- [ ] Each snippet has customize options
- [ ] Snippets render correctly
- [ ] No JavaScript errors in console

---

### Phase 6: SAM AI Integration
**Files**: 3 | **Estimated Effort**: Medium

Creates:
- `sam_funnel_api.py` - API endpoints:
  - `/sam_ai_funnels/list_templates` - Get available templates
  - `/sam_ai_funnels/create` - Create funnel from spec
  - `/sam_ai_funnels/generate_copy` - Generate direct response copy
  - `/sam_ai_funnels/get_analytics` - Retrieve funnel stats
- SAM funnel knowledge file
- Copy generation with frameworks:
  - PAS (Problem-Agitate-Solution)
  - Before/After/Bridge
  - Value stacking
  - Urgency/scarcity
- Context builder integration

**Validation**:
- [ ] SAM can list available templates
- [ ] SAM can create funnels conversationally
- [ ] Copy generation returns persuasive text
- [ ] Analytics endpoint returns data

---

### Phase 7: Quiz Logic
**Files**: 2 | **Estimated Effort**: Medium

Creates:
- `quiz_controller.py` - Quiz handling:
  - State management
  - Answer tracking
  - Score calculation
  - Email gating
- Quiz JavaScript:
  - Progress tracking
  - Answer selection
  - Branching logic
  - Result personalization
- Quiz models extension

**Validation**:
- [ ] Quiz progresses through questions
- [ ] Branching logic works
- [ ] Email gate captures before results
- [ ] Personalized results display
- [ ] Quiz data saved to lead

---

## Final Module Structure

```
sam_ai_funnels/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   ├── funnel_definition.py
│   ├── funnel_page.py
│   ├── funnel_template.py
│   ├── funnel_snippet.py
│   └── funnel_conversion.py
├── controllers/
│   ├── __init__.py
│   ├── funnel_form_controller.py
│   ├── quiz_controller.py
│   └── sam_funnel_api.py
├── views/
│   ├── funnel_definition_views.xml
│   ├── funnel_page_views.xml
│   ├── funnel_template_views.xml
│   ├── funnel_snippet_views.xml
│   ├── funnel_conversion_views.xml
│   ├── funnel_dashboard.xml
│   └── menu.xml
├── wizards/
│   ├── __init__.py
│   ├── funnel_generator.py
│   └── funnel_generator_views.xml
├── data/
│   ├── funnel_templates.xml
│   └── snippet_registry.xml
├── static/
│   └── src/
│       ├── snippets/
│       │   ├── options.xml
│       │   ├── s_funnel_hero/
│       │   │   ├── 000.xml
│       │   │   ├── 000.scss
│       │   │   └── options.js (if needed)
│       │   └── [45 more snippet folders...]
│       ├── js/
│       │   ├── countdown_timer.js
│       │   ├── faq_accordion.js
│       │   ├── form_submit.js
│       │   └── quiz_logic.js
│       └── scss/
│           └── funnel_snippets.scss
├── security/
│   └── ir.model.access.csv
└── sam_knowledge/
    └── funnel_builder_knowledge.md
```

**Total Files**: ~100+
**Total Snippets**: 46
**Total Templates**: 6

---

## Developer Invocation Commands

Copy-paste these when invoking cto-developer for each phase:

### For Phase 1:
```
/cto-developer Read the Phase 1 developer prompt at D:\SAMAI-18-SaaS\ai_sam\ai_sam_docs\plans\2025-12-31_funnels-phase1-developer-prompt.md and implement the complete module foundation. Create all 18 files as specified. Validate that the module installs correctly.
```

### For Phase 2:
```
/cto-developer Read the Phase 2 developer prompt at D:\SAMAI-18-SaaS\ai_sam\ai_sam_docs\plans\2025-12-31_funnels-phase2-developer-prompt.md and implement all 15 MVP snippets with the FUNNELS tab. Create all 21 files as specified.
```

### For Phase 3:
```
/cto-developer Read the Phase 3 developer prompt at D:\SAMAI-18-SaaS\ai_sam\ai_sam_docs\plans\2025-12-31_funnels-phase3-developer-prompt.md and implement form handling with CRM and mailing list integration.
```

### For Phase 4:
```
/cto-developer Read the Phase 4 developer prompt at D:\SAMAI-18-SaaS\ai_sam\ai_sam_docs\plans\2025-12-31_funnels-phase4-developer-prompt.md and implement all 6 funnel templates with the generator wizard and dashboard.
```

### For Phase 5:
```
/cto-developer Read the Phase 5 developer prompt at D:\SAMAI-18-SaaS\ai_sam\ai_sam_docs\plans\2025-12-31_funnels-phase5-developer-prompt.md and implement all remaining 31 snippets.
```

### For Phase 6:
```
/cto-developer Read the Phase 6 developer prompt at D:\SAMAI-18-SaaS\ai_sam\ai_sam_docs\plans\2025-12-31_funnels-phase6-developer-prompt.md and implement SAM AI integration with all API endpoints.
```

### For Phase 7:
```
/cto-developer Read the Phase 7 developer prompt at D:\SAMAI-18-SaaS\ai_sam\ai_sam_docs\plans\2025-12-31_funnels-phase7-developer-prompt.md and implement quiz logic with branching and personalization.
```

---

## Critical Success Factors

### Do's
- Follow Odoo 18 patterns exactly
- Use existing website builder conventions
- Test each phase before proceeding
- Keep snippets self-contained
- Follow the security model

### Don'ts
- Don't modify core Odoo files
- Don't skip phases
- Don't over-engineer snippets
- Don't add features not in requirements
- Don't forget to register files in `__manifest__.py`

---

## Dependencies

### Odoo Modules Required
- `website` - Website builder
- `website_sale` (optional) - E-commerce integration
- `crm` - Lead management
- `mass_mailing` - Mailing lists
- `mail` - Chatter/activity

### External
- None - pure Odoo implementation

---

## Testing Checklist

### After Each Phase
- [ ] Module upgrades without errors
- [ ] No Python syntax errors
- [ ] No JavaScript console errors
- [ ] New features visible in UI
- [ ] Existing features still work

### Final Acceptance
- [ ] All 46 snippets work
- [ ] All 6 templates generate correctly
- [ ] Form submissions create leads
- [ ] Mailing list integration works
- [ ] SAM can create funnels via API
- [ ] SAM can generate copy
- [ ] Quiz funnels branch correctly
- [ ] Analytics dashboard shows data

---

## Rollback Plan

If a phase fails:
1. Uninstall module: Settings > Apps > sam_ai_funnels > Uninstall
2. Delete module folder: `D:\SAMAI-18-SaaS\ai_sam\sam_ai_funnels\`
3. Restart from last working phase

---

## Support

- Requirements: `FUNNELS-TAB-REQUIREMENTS.md`
- Architecture: `2025-12-31_sam-ai-funnels-architecture.md`
- Each phase prompt contains detailed implementation specs

---

*This guide prepared by CTO Architect Agent*
*Ready for implementation via cto-developer*
