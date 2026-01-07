# Developer Prompt: SAM AI Funnels - Phase 3 (Form Integration)

**Date:** 2025-12-31
**Phase:** 3 of 7
**Scope:** Form submission handling, CRM integration, mailing list integration, conversion tracking
**Prerequisite:** Phase 2 complete and validated

---

## CONTEXT

Phase 2 created the FUNNELS tab with 15 draggable snippets. Now we make the `s_opt_in_form` snippet actually work - submitting to Odoo CRM and mailing lists, tracking conversions, and handling redirects.

**Architecture Document:** `D:\SAMAI-18-SaaS\ai_sam\ai_sam_docs\plans\2025-12-31_sam-ai-funnels-architecture.md`

---

## GOAL

Make funnel forms functional:
1. Form submissions create CRM leads
2. Form submissions add contacts to mailing lists
3. Track all conversion events
4. Capture UTM parameters
5. Handle redirects after submission

---

## DELIVERABLES

### 1. Form Submission Controller

**File:** `controllers/funnel_form_controller.py`

```python
import json
import logging
from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class FunnelFormController(http.Controller):
    """Handle funnel form submissions with CRM and mailing integration."""

    @http.route('/funnel/form/submit', type='http', auth='public', methods=['POST'], csrf=True)
    def submit_form(self, **post):
        """
        Handle funnel form submission.

        Expects:
            - name (optional): Contact name
            - email (required): Contact email
            - phone (optional): Contact phone
            - integration: 'crm', 'mailing', or 'both'
            - lead_tag: Tag to apply to CRM lead
            - mailing_list_id: ID of mailing list
            - funnel_id: ID of the funnel
            - page_id: ID of the funnel page
            - redirect_url: Where to redirect after submission

        Returns:
            Redirect to thank you page or specified URL
        """
        try:
            # Extract form data
            name = post.get('name', '').strip()
            email = post.get('email', '').strip()
            phone = post.get('phone', '').strip()

            # Validate email
            if not email:
                return self._error_response('Email is required')

            # Get integration settings from form data attributes
            integration = post.get('integration', 'crm')
            lead_tag = post.get('lead_tag', '')
            mailing_list_id = post.get('mailing_list_id')
            funnel_id = post.get('funnel_id')
            page_id = post.get('page_id')
            redirect_url = post.get('redirect_url', '/thank-you')

            # Extract UTM parameters
            utm_data = self._extract_utm_params(post)

            # Get or create partner
            partner = self._get_or_create_partner(name, email, phone)

            lead = None
            mailing_contact = None

            # Create CRM lead if integration includes CRM
            if integration in ('crm', 'both'):
                lead = self._create_crm_lead(
                    name=name or email,
                    email=email,
                    phone=phone,
                    partner=partner,
                    lead_tag=lead_tag,
                    funnel_id=funnel_id,
                    page_id=page_id,
                    utm_data=utm_data
                )

            # Add to mailing list if integration includes mailing
            if integration in ('mailing', 'both'):
                mailing_contact = self._add_to_mailing_list(
                    name=name,
                    email=email,
                    mailing_list_id=mailing_list_id,
                    partner=partner
                )

            # Track conversion event
            self._track_conversion(
                funnel_id=funnel_id,
                page_id=page_id,
                event_type='form_submit',
                partner=partner,
                lead=lead,
                utm_data=utm_data
            )

            # Update page analytics
            self._update_page_analytics(page_id)

            # Handle redirect
            return request.redirect(redirect_url)

        except Exception as e:
            _logger.error(f"Funnel form submission error: {str(e)}")
            return self._error_response('An error occurred. Please try again.')

    @http.route('/funnel/form/submit/ajax', type='json', auth='public', methods=['POST'])
    def submit_form_ajax(self, **post):
        """
        AJAX version of form submission.
        Returns JSON response instead of redirect.
        """
        try:
            # Same logic as submit_form but return JSON
            name = post.get('name', '').strip()
            email = post.get('email', '').strip()
            phone = post.get('phone', '').strip()

            if not email:
                return {'success': False, 'error': 'Email is required'}

            integration = post.get('integration', 'crm')
            lead_tag = post.get('lead_tag', '')
            mailing_list_id = post.get('mailing_list_id')
            funnel_id = post.get('funnel_id')
            page_id = post.get('page_id')
            redirect_url = post.get('redirect_url', '/thank-you')

            utm_data = self._extract_utm_params(post)
            partner = self._get_or_create_partner(name, email, phone)

            lead = None
            if integration in ('crm', 'both'):
                lead = self._create_crm_lead(
                    name=name or email,
                    email=email,
                    phone=phone,
                    partner=partner,
                    lead_tag=lead_tag,
                    funnel_id=funnel_id,
                    page_id=page_id,
                    utm_data=utm_data
                )

            if integration in ('mailing', 'both'):
                self._add_to_mailing_list(
                    name=name,
                    email=email,
                    mailing_list_id=mailing_list_id,
                    partner=partner
                )

            self._track_conversion(
                funnel_id=funnel_id,
                page_id=page_id,
                event_type='form_submit',
                partner=partner,
                lead=lead,
                utm_data=utm_data
            )

            self._update_page_analytics(page_id)

            return {
                'success': True,
                'redirect_url': redirect_url,
                'lead_id': lead.id if lead else None,
                'partner_id': partner.id if partner else None
            }

        except Exception as e:
            _logger.error(f"Funnel AJAX form error: {str(e)}")
            return {'success': False, 'error': str(e)}

    # ==========================================
    # HELPER METHODS
    # ==========================================

    def _get_or_create_partner(self, name, email, phone):
        """Get existing partner by email or create new one."""
        Partner = request.env['res.partner'].sudo()

        # Search for existing partner by email
        partner = Partner.search([('email', '=ilike', email)], limit=1)

        if partner:
            # Update name/phone if provided and missing
            updates = {}
            if name and not partner.name:
                updates['name'] = name
            if phone and not partner.phone:
                updates['phone'] = phone
            if updates:
                partner.write(updates)
            return partner

        # Create new partner
        partner_vals = {
            'name': name or email.split('@')[0],
            'email': email,
            'phone': phone or False,
            'type': 'contact',
        }

        return Partner.create(partner_vals)

    def _create_crm_lead(self, name, email, phone, partner, lead_tag, funnel_id, page_id, utm_data):
        """Create a CRM lead from form submission."""
        Lead = request.env['crm.lead'].sudo()

        # Get funnel info for context
        funnel = None
        page = None
        if funnel_id:
            funnel = request.env['funnel.definition'].sudo().browse(int(funnel_id))
        if page_id:
            page = request.env['funnel.page'].sudo().browse(int(page_id))

        # Build lead name
        lead_name = name
        if funnel:
            lead_name = f"{name} - {funnel.name}"

        # Prepare lead values
        lead_vals = {
            'name': lead_name,
            'email_from': email,
            'phone': phone or False,
            'partner_id': partner.id if partner else False,
            'type': 'lead',
            'description': self._build_lead_description(funnel, page, utm_data),
        }

        # Set CRM team from funnel if configured
        if funnel and funnel.crm_team_id:
            lead_vals['team_id'] = funnel.crm_team_id.id

        # Add UTM tracking
        if utm_data.get('source'):
            lead_vals['source_id'] = self._get_or_create_utm_source(utm_data['source'])
        if utm_data.get('medium'):
            lead_vals['medium_id'] = self._get_or_create_utm_medium(utm_data['medium'])
        if utm_data.get('campaign'):
            lead_vals['campaign_id'] = self._get_or_create_utm_campaign(utm_data['campaign'])

        # Create the lead
        lead = Lead.create(lead_vals)

        # Add tags
        tag_ids = []
        if lead_tag:
            tag = self._get_or_create_lead_tag(lead_tag)
            tag_ids.append(tag.id)
        if funnel and funnel.default_tag_ids:
            tag_ids.extend(funnel.default_tag_ids.ids)
        if tag_ids:
            lead.write({'tag_ids': [(6, 0, tag_ids)]})

        return lead

    def _build_lead_description(self, funnel, page, utm_data):
        """Build lead description with funnel and UTM context."""
        lines = []

        if funnel:
            lines.append(f"Funnel: {funnel.name}")
        if page:
            lines.append(f"Page: {page.name} ({page.page_type})")

        if utm_data:
            lines.append("\n--- UTM Tracking ---")
            if utm_data.get('source'):
                lines.append(f"Source: {utm_data['source']}")
            if utm_data.get('medium'):
                lines.append(f"Medium: {utm_data['medium']}")
            if utm_data.get('campaign'):
                lines.append(f"Campaign: {utm_data['campaign']}")
            if utm_data.get('term'):
                lines.append(f"Term: {utm_data['term']}")
            if utm_data.get('content'):
                lines.append(f"Content: {utm_data['content']}")

        return '\n'.join(lines) if lines else False

    def _get_or_create_lead_tag(self, tag_name):
        """Get or create a CRM lead tag."""
        Tag = request.env['crm.tag'].sudo()
        tag = Tag.search([('name', '=ilike', tag_name)], limit=1)
        if not tag:
            tag = Tag.create({'name': tag_name})
        return tag

    def _get_or_create_utm_source(self, source_name):
        """Get or create UTM source."""
        Source = request.env['utm.source'].sudo()
        source = Source.search([('name', '=ilike', source_name)], limit=1)
        if not source:
            source = Source.create({'name': source_name})
        return source.id

    def _get_or_create_utm_medium(self, medium_name):
        """Get or create UTM medium."""
        Medium = request.env['utm.medium'].sudo()
        medium = Medium.search([('name', '=ilike', medium_name)], limit=1)
        if not medium:
            medium = Medium.create({'name': medium_name})
        return medium.id

    def _get_or_create_utm_campaign(self, campaign_name):
        """Get or create UTM campaign."""
        Campaign = request.env['utm.campaign'].sudo()
        campaign = Campaign.search([('name', '=ilike', campaign_name)], limit=1)
        if not campaign:
            campaign = Campaign.create({'name': campaign_name})
        return campaign.id

    def _add_to_mailing_list(self, name, email, mailing_list_id, partner):
        """Add contact to mailing list."""
        if not mailing_list_id:
            return None

        MailingContact = request.env['mailing.contact'].sudo()
        MailingList = request.env['mailing.list'].sudo()

        # Get the mailing list
        mailing_list = MailingList.browse(int(mailing_list_id))
        if not mailing_list.exists():
            _logger.warning(f"Mailing list {mailing_list_id} not found")
            return None

        # Check if contact already exists in this list
        existing = MailingContact.search([
            ('email', '=ilike', email),
            ('list_ids', 'in', [mailing_list.id])
        ], limit=1)

        if existing:
            return existing

        # Check if contact exists but not in this list
        contact = MailingContact.search([('email', '=ilike', email)], limit=1)

        if contact:
            # Add to list
            contact.write({'list_ids': [(4, mailing_list.id)]})
            return contact

        # Create new mailing contact
        contact_vals = {
            'name': name or email.split('@')[0],
            'email': email,
            'list_ids': [(4, mailing_list.id)],
        }

        return MailingContact.create(contact_vals)

    def _extract_utm_params(self, post):
        """Extract UTM parameters from form submission."""
        return {
            'source': post.get('utm_source', ''),
            'medium': post.get('utm_medium', ''),
            'campaign': post.get('utm_campaign', ''),
            'term': post.get('utm_term', ''),
            'content': post.get('utm_content', ''),
        }

    def _track_conversion(self, funnel_id, page_id, event_type, partner, lead, utm_data):
        """Track conversion event."""
        if not funnel_id or not page_id:
            return

        Conversion = request.env['funnel.conversion'].sudo()

        # Get visitor ID from cookie
        visitor_id = request.httprequest.cookies.get('funnel_visitor_id', '')

        conversion_vals = {
            'funnel_id': int(funnel_id),
            'page_id': int(page_id),
            'event_type': event_type,
            'visitor_id': visitor_id,
            'partner_id': partner.id if partner else False,
            'lead_id': lead.id if lead else False,
            'utm_source': utm_data.get('source', ''),
            'utm_medium': utm_data.get('medium', ''),
            'utm_campaign': utm_data.get('campaign', ''),
            'utm_term': utm_data.get('term', ''),
            'utm_content': utm_data.get('content', ''),
            'user_agent': request.httprequest.user_agent.string if request.httprequest.user_agent else '',
            'ip_address': request.httprequest.remote_addr,
        }

        return Conversion.create(conversion_vals)

    def _update_page_analytics(self, page_id):
        """Update page form submission counter."""
        if not page_id:
            return

        Page = request.env['funnel.page'].sudo()
        page = Page.browse(int(page_id))
        if page.exists():
            page.write({
                'form_submissions': page.form_submissions + 1
            })

    def _error_response(self, message):
        """Return error response."""
        return request.render('sam_ai_funnels.funnel_form_error', {
            'error_message': message
        })


class FunnelTrackingController(http.Controller):
    """Track page views and other funnel events."""

    @http.route('/funnel/track/pageview', type='json', auth='public', methods=['POST'])
    def track_pageview(self, funnel_id, page_id, **kwargs):
        """Track a page view event."""
        try:
            if not funnel_id or not page_id:
                return {'success': False, 'error': 'Missing funnel or page ID'}

            # Get or set visitor ID
            visitor_id = request.httprequest.cookies.get('funnel_visitor_id', '')
            if not visitor_id:
                import uuid
                visitor_id = str(uuid.uuid4())

            # Extract UTM from referrer or stored session
            utm_data = {
                'source': kwargs.get('utm_source', ''),
                'medium': kwargs.get('utm_medium', ''),
                'campaign': kwargs.get('utm_campaign', ''),
                'term': kwargs.get('utm_term', ''),
                'content': kwargs.get('utm_content', ''),
            }

            # Create conversion record
            Conversion = request.env['funnel.conversion'].sudo()
            Conversion.create({
                'funnel_id': int(funnel_id),
                'page_id': int(page_id),
                'event_type': 'page_view',
                'visitor_id': visitor_id,
                'utm_source': utm_data.get('source', ''),
                'utm_medium': utm_data.get('medium', ''),
                'utm_campaign': utm_data.get('campaign', ''),
                'user_agent': request.httprequest.user_agent.string if request.httprequest.user_agent else '',
                'ip_address': request.httprequest.remote_addr,
            })

            # Update page view count
            Page = request.env['funnel.page'].sudo()
            page = Page.browse(int(page_id))
            if page.exists():
                page.write({
                    'view_count': page.view_count + 1
                })

            return {
                'success': True,
                'visitor_id': visitor_id
            }

        except Exception as e:
            _logger.error(f"Page view tracking error: {str(e)}")
            return {'success': False, 'error': str(e)}

    @http.route('/funnel/track/cta', type='json', auth='public', methods=['POST'])
    def track_cta_click(self, funnel_id, page_id, cta_id=None, **kwargs):
        """Track a CTA click event."""
        try:
            visitor_id = request.httprequest.cookies.get('funnel_visitor_id', '')

            Conversion = request.env['funnel.conversion'].sudo()
            Conversion.create({
                'funnel_id': int(funnel_id),
                'page_id': int(page_id),
                'event_type': 'cta_click',
                'visitor_id': visitor_id,
                'session_data': json.dumps({'cta_id': cta_id}) if cta_id else False,
            })

            return {'success': True}

        except Exception as e:
            _logger.error(f"CTA tracking error: {str(e)}")
            return {'success': False, 'error': str(e)}
```

---

### 2. Update controllers/__init__.py

```python
from . import funnel_controller
from . import funnel_form_controller
```

---

### 3. Form JavaScript (AJAX Submission)

**File:** `static/src/js/funnel_form.js`

```javascript
/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";
import { jsonrpc } from "@web/core/network/rpc_service";

publicWidget.registry.FunnelOptInForm = publicWidget.Widget.extend({
    selector: '.s_opt_in_form',
    events: {
        'submit .s_funnel_form': '_onFormSubmit',
    },

    start: function () {
        this._super.apply(this, arguments);
        this._initForm();
        this._trackPageView();
        return Promise.resolve();
    },

    _initForm: function () {
        const $form = this.$('.s_funnel_form');
        const $section = this.$el;

        // Add hidden fields from data attributes
        const integration = $section.data('integration') || 'crm';
        const redirectUrl = $section.data('redirect-url') || '/thank-you';
        const leadTag = $section.data('lead-tag') || '';
        const funnelId = $section.data('funnel-id') || '';
        const pageId = $section.data('page-id') || '';
        const mailingListId = $section.data('mailing-list-id') || '';

        // Add hidden inputs
        this._addHiddenField($form, 'integration', integration);
        this._addHiddenField($form, 'redirect_url', redirectUrl);
        this._addHiddenField($form, 'lead_tag', leadTag);
        this._addHiddenField($form, 'funnel_id', funnelId);
        this._addHiddenField($form, 'page_id', pageId);
        this._addHiddenField($form, 'mailing_list_id', mailingListId);

        // Add UTM parameters from URL
        const urlParams = new URLSearchParams(window.location.search);
        this._addHiddenField($form, 'utm_source', urlParams.get('utm_source') || '');
        this._addHiddenField($form, 'utm_medium', urlParams.get('utm_medium') || '');
        this._addHiddenField($form, 'utm_campaign', urlParams.get('utm_campaign') || '');
        this._addHiddenField($form, 'utm_term', urlParams.get('utm_term') || '');
        this._addHiddenField($form, 'utm_content', urlParams.get('utm_content') || '');
    },

    _addHiddenField: function ($form, name, value) {
        if (!$form.find(`input[name="${name}"]`).length) {
            $form.append(`<input type="hidden" name="${name}" value="${value}"/>`);
        }
    },

    _onFormSubmit: function (ev) {
        // Check if AJAX submission is enabled
        const useAjax = this.$el.data('ajax-submit') !== false;

        if (!useAjax) {
            // Let form submit normally
            return true;
        }

        ev.preventDefault();
        ev.stopPropagation();

        const $form = $(ev.currentTarget);
        const $button = $form.find('button[type="submit"]');
        const originalText = $button.text();

        // Disable button and show loading
        $button.prop('disabled', true).text('Submitting...');

        // Collect form data
        const formData = {};
        $form.serializeArray().forEach(item => {
            formData[item.name] = item.value;
        });

        // Submit via AJAX
        jsonrpc('/funnel/form/submit/ajax', formData)
            .then(response => {
                if (response.success) {
                    // Show success message briefly then redirect
                    $button.removeClass('btn-primary').addClass('btn-success').text('Success!');

                    setTimeout(() => {
                        window.location.href = response.redirect_url;
                    }, 500);
                } else {
                    // Show error
                    $button.prop('disabled', false).text(originalText);
                    this._showError(response.error || 'Submission failed. Please try again.');
                }
            })
            .catch(error => {
                console.error('Form submission error:', error);
                $button.prop('disabled', false).text(originalText);
                this._showError('An error occurred. Please try again.');
            });

        return false;
    },

    _showError: function (message) {
        // Remove existing error
        this.$('.s_form_error').remove();

        // Add error message
        const $error = $(`<div class="s_form_error alert alert-danger mt-3">${message}</div>`);
        this.$('.s_funnel_form').append($error);

        // Auto-remove after 5 seconds
        setTimeout(() => $error.fadeOut(() => $error.remove()), 5000);
    },

    _trackPageView: function () {
        const funnelId = this.$el.data('funnel-id');
        const pageId = this.$el.data('page-id');

        if (funnelId && pageId) {
            const urlParams = new URLSearchParams(window.location.search);

            jsonrpc('/funnel/track/pageview', {
                funnel_id: funnelId,
                page_id: pageId,
                utm_source: urlParams.get('utm_source') || '',
                utm_medium: urlParams.get('utm_medium') || '',
                utm_campaign: urlParams.get('utm_campaign') || '',
            }).then(response => {
                if (response.visitor_id) {
                    // Store visitor ID in cookie
                    document.cookie = `funnel_visitor_id=${response.visitor_id}; path=/; max-age=31536000`;
                }
            });
        }
    },
});

export default publicWidget.registry.FunnelOptInForm;
```

---

### 4. CTA Tracking JavaScript

**File:** `static/src/js/funnel_tracking.js`

```javascript
/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";
import { jsonrpc } from "@web/core/network/rpc_service";

/**
 * Track CTA clicks on funnel pages
 */
publicWidget.registry.FunnelCTATracking = publicWidget.Widget.extend({
    selector: '.s_cta_inline, .s_final_cta, .s_hero_minimal, .s_hero_full',
    events: {
        'click .btn': '_onCTAClick',
    },

    _onCTAClick: function (ev) {
        const $section = this.$el;
        const funnelId = $section.data('funnel-id');
        const pageId = $section.data('page-id');

        if (funnelId && pageId) {
            // Track asynchronously - don't block the click
            jsonrpc('/funnel/track/cta', {
                funnel_id: funnelId,
                page_id: pageId,
                cta_id: $(ev.currentTarget).attr('id') || null,
            });
        }

        // Don't prevent default - let the link work
        return true;
    },
});

/**
 * Track page views on all funnel sections
 */
publicWidget.registry.FunnelPageTracking = publicWidget.Widget.extend({
    selector: '[data-funnel-id][data-page-id]',

    start: function () {
        this._super.apply(this, arguments);

        // Only track once per page load
        if (window._funnelPageTracked) {
            return Promise.resolve();
        }
        window._funnelPageTracked = true;

        const funnelId = this.$el.data('funnel-id');
        const pageId = this.$el.data('page-id');

        if (funnelId && pageId) {
            const urlParams = new URLSearchParams(window.location.search);

            jsonrpc('/funnel/track/pageview', {
                funnel_id: funnelId,
                page_id: pageId,
                utm_source: urlParams.get('utm_source') || '',
                utm_medium: urlParams.get('utm_medium') || '',
                utm_campaign: urlParams.get('utm_campaign') || '',
            }).then(response => {
                if (response.visitor_id) {
                    document.cookie = `funnel_visitor_id=${response.visitor_id}; path=/; max-age=31536000`;
                }
            });
        }

        return Promise.resolve();
    },
});

export default {
    FunnelCTATracking: publicWidget.registry.FunnelCTATracking,
    FunnelPageTracking: publicWidget.registry.FunnelPageTracking,
};
```

---

### 5. Error Template

**File:** `views/funnel_form_error.xml`

```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <template id="funnel_form_error" name="Funnel Form Error">
        <t t-call="website.layout">
            <div class="container py-5">
                <div class="row justify-content-center">
                    <div class="col-md-6 text-center">
                        <div class="alert alert-danger">
                            <h4 class="alert-heading">Oops!</h4>
                            <p t-esc="error_message"/>
                        </div>
                        <a href="javascript:history.back()" class="btn btn-primary">
                            Go Back
                        </a>
                    </div>
                </div>
            </div>
        </t>
    </template>
</odoo>
```

---

### 6. Update s_opt_in_form Snippet

Update `views/snippets/s_opt_in_form.xml` to include funnel/page data attributes:

```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <template id="s_opt_in_form" name="Opt-in Form">
        <section class="s_opt_in_form s_fields_name_email py-5"
                 data-snippet="sam_ai_funnels.s_opt_in_form"
                 data-name="Opt-in Form"
                 data-integration="crm"
                 data-redirect-url="/thank-you"
                 data-lead-tag=""
                 data-funnel-id=""
                 data-page-id=""
                 data-mailing-list-id=""
                 data-ajax-submit="true">
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

---

### 7. Update options.xml - Add Mailing List Selector

Add to the opt_in_form options in `views/snippets/options.xml`:

```xml
<!-- ===== OPT-IN FORM OPTIONS (UPDATED) ===== -->
<div data-selector=".s_opt_in_form" data-js="FunnelOptInFormOptions">
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
    <we-input string="Mailing List ID" data-attribute-name="data-mailing-list-id"/>
    <we-input string="Funnel ID" data-attribute-name="data-funnel-id"/>
    <we-input string="Page ID" data-attribute-name="data-page-id"/>
    <we-checkbox string="AJAX Submit" data-attribute-name="data-ajax-submit"/>
    <we-colorpicker string="Button Color" data-css-property="--btn-color"/>
    <we-colorpicker string="Background" data-css-property="background-color"/>
    <we-select string="Padding">
        <we-button data-select-class="py-3">Small</we-button>
        <we-button data-select-class="py-5">Medium</we-button>
        <we-button data-select-class="py-7">Large</we-button>
    </we-select>
</div>
```

---

### 8. Update __manifest__.py

Add new files to manifest:

```python
{
    # ... existing fields ...
    'data': [
        # ... existing data ...

        # Error template (NEW)
        'views/funnel_form_error.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            # ... existing assets ...

            # Form handling (NEW)
            'sam_ai_funnels/static/src/js/funnel_form.js',
            'sam_ai_funnels/static/src/js/funnel_tracking.js',
        ],
        # ... rest of assets ...
    },
}
```

---

### 9. Conversion Analytics View

**File:** `views/funnel_conversion_views.xml`

```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <!-- Conversion Tree View -->
    <record id="funnel_conversion_view_tree" model="ir.ui.view">
        <field name="name">funnel.conversion.tree</field>
        <field name="model">funnel.conversion</field>
        <field name="arch" type="xml">
            <tree string="Conversions" default_order="timestamp desc">
                <field name="timestamp"/>
                <field name="funnel_id"/>
                <field name="page_id"/>
                <field name="event_type" widget="badge"
                       decoration-success="event_type == 'form_submit'"
                       decoration-info="event_type == 'page_view'"
                       decoration-warning="event_type == 'cta_click'"/>
                <field name="partner_id"/>
                <field name="lead_id"/>
                <field name="utm_source"/>
                <field name="utm_campaign"/>
            </tree>
        </field>
    </record>

    <!-- Conversion Search View -->
    <record id="funnel_conversion_view_search" model="ir.ui.view">
        <field name="name">funnel.conversion.search</field>
        <field name="model">funnel.conversion</field>
        <field name="arch" type="xml">
            <search string="Search Conversions">
                <field name="funnel_id"/>
                <field name="page_id"/>
                <field name="partner_id"/>
                <field name="utm_source"/>
                <field name="utm_campaign"/>
                <filter string="Form Submissions" name="form_submit" domain="[('event_type', '=', 'form_submit')]"/>
                <filter string="Page Views" name="page_view" domain="[('event_type', '=', 'page_view')]"/>
                <filter string="CTA Clicks" name="cta_click" domain="[('event_type', '=', 'cta_click')]"/>
                <separator/>
                <filter string="Today" name="today" domain="[('timestamp', '>=', datetime.datetime.combine(context_today(), datetime.time(0,0,0)))]"/>
                <filter string="This Week" name="this_week" domain="[('timestamp', '>=', (context_today() - datetime.timedelta(days=7)))]"/>
                <group expand="0" string="Group By">
                    <filter string="Funnel" name="group_funnel" context="{'group_by': 'funnel_id'}"/>
                    <filter string="Page" name="group_page" context="{'group_by': 'page_id'}"/>
                    <filter string="Event Type" name="group_event" context="{'group_by': 'event_type'}"/>
                    <filter string="UTM Source" name="group_source" context="{'group_by': 'utm_source'}"/>
                    <filter string="Date" name="group_date" context="{'group_by': 'timestamp:day'}"/>
                </group>
            </search>
        </field>
    </record>

    <!-- Conversion Pivot View -->
    <record id="funnel_conversion_view_pivot" model="ir.ui.view">
        <field name="name">funnel.conversion.pivot</field>
        <field name="model">funnel.conversion</field>
        <field name="arch" type="xml">
            <pivot string="Conversion Analytics">
                <field name="funnel_id" type="row"/>
                <field name="event_type" type="col"/>
                <field name="id" type="measure" string="Count"/>
            </pivot>
        </field>
    </record>

    <!-- Conversion Graph View -->
    <record id="funnel_conversion_view_graph" model="ir.ui.view">
        <field name="name">funnel.conversion.graph</field>
        <field name="model">funnel.conversion</field>
        <field name="arch" type="xml">
            <graph string="Conversions Over Time" type="line">
                <field name="timestamp" interval="day"/>
                <field name="id" type="measure" string="Events"/>
            </graph>
        </field>
    </record>

    <!-- Conversion Action -->
    <record id="funnel_conversion_action" model="ir.actions.act_window">
        <field name="name">Conversion Analytics</field>
        <field name="res_model">funnel.conversion</field>
        <field name="view_mode">tree,pivot,graph</field>
        <field name="context">{'search_default_form_submit': 1}</field>
    </record>

    <!-- Add to menu -->
    <menuitem id="funnel_menu_analytics"
              name="Analytics"
              parent="funnel_menu_root"
              action="funnel_conversion_action"
              sequence="30"/>
</odoo>
```

---

## VALIDATION CHECKLIST

After implementation, verify:

- [ ] Form submission creates CRM lead
- [ ] Lead has correct name, email, phone
- [ ] Lead has UTM source/medium/campaign populated
- [ ] Lead has tags from form + funnel defaults
- [ ] Lead has correct CRM team assignment
- [ ] Form submission adds contact to mailing list
- [ ] Mailing contact created if new email
- [ ] Existing contact added to list if exists
- [ ] Conversion event tracked with event_type='form_submit'
- [ ] Page view tracking works
- [ ] CTA click tracking works
- [ ] UTM parameters captured from URL
- [ ] Redirect works after submission
- [ ] AJAX submission works without page reload
- [ ] Error handling shows user-friendly messages
- [ ] Analytics menu shows conversion data
- [ ] Pivot/graph views render correctly

---

## FILES TO CREATE/UPDATE

**Create:**
1. `controllers/funnel_form_controller.py`
2. `static/src/js/funnel_form.js`
3. `static/src/js/funnel_tracking.js`
4. `views/funnel_form_error.xml`
5. `views/funnel_conversion_views.xml`

**Update:**
6. `controllers/__init__.py`
7. `views/snippets/s_opt_in_form.xml`
8. `views/snippets/options.xml`
9. `views/funnel_menus.xml`
10. `__manifest__.py`

---

## NEXT PHASE

After Phase 3 is validated, proceed to Phase 4: Complete Funnels.
Phase 4 will cover:
- 6 funnel templates (pre-defined structures)
- Multi-page generation from templates
- Page linking and redirects
- Funnel dashboard

---

**END OF PHASE 3 DEVELOPER PROMPT**
