# Developer Prompt: SAM AI Funnels - Phase 7 (Quiz Logic)

**Date:** 2025-12-31
**Phase:** 7 of 7 (FINAL)
**Scope:** Interactive quiz functionality with branching, scoring, and personalization
**Prerequisite:** Phase 6 complete

---

## CONTEXT

This final phase implements the interactive quiz system. Quiz funnels are powerful for lead qualification and segmentation. We need JavaScript state management, branching logic, scoring, and personalized results.

---

## GOAL

1. Quiz state management (track answers across questions)
2. Progress indicator updates
3. Branching logic (skip questions based on answers)
4. Score calculation
5. Email gate before showing results
6. Personalized results based on answers
7. Quiz data stored in conversion events

---

## DELIVERABLES

### 1. Quiz Controller

**File:** `controllers/quiz_controller.py`

```python
import json
from odoo import http
from odoo.http import request


class QuizController(http.Controller):
    """Handle quiz submissions and result calculations."""

    @http.route('/funnel/quiz/submit', type='json', auth='public', methods=['POST'])
    def submit_quiz(self, funnel_id, page_id, answers, email=None, name=None, **kwargs):
        """
        Submit quiz answers and get result.

        Args:
            funnel_id: The funnel ID
            page_id: The quiz gate page ID
            answers: List of {question_id, answer_value}
            email: User's email (captured at gate)
            name: User's name (optional)

        Returns:
            {
                'success': True,
                'result_type': 'achiever',
                'result_headline': 'You are an Achiever!',
                'result_description': '...',
                'redirect_url': '/your-results?type=achiever'
            }
        """
        try:
            # Calculate quiz result
            result = self._calculate_result(answers)

            # Store quiz data
            partner = None
            lead = None

            if email:
                # Get or create partner
                Partner = request.env['res.partner'].sudo()
                partner = Partner.search([('email', '=ilike', email)], limit=1)
                if not partner:
                    partner = Partner.create({
                        'name': name or email.split('@')[0],
                        'email': email,
                    })

                # Create lead with quiz results
                funnel = request.env['funnel.definition'].sudo().browse(int(funnel_id))
                lead = request.env['crm.lead'].sudo().create({
                    'name': f"Quiz Lead: {name or email}",
                    'email_from': email,
                    'partner_id': partner.id,
                    'type': 'lead',
                    'description': self._format_quiz_results(answers, result),
                    'team_id': funnel.crm_team_id.id if funnel.crm_team_id else False,
                })

                # Add to mailing list if configured
                if funnel.mailing_list_id:
                    self._add_to_mailing(email, name, funnel.mailing_list_id.id)

            # Track conversion
            request.env['funnel.conversion'].sudo().create({
                'funnel_id': int(funnel_id),
                'page_id': int(page_id),
                'event_type': 'quiz_complete',
                'partner_id': partner.id if partner else False,
                'lead_id': lead.id if lead else False,
                'session_data': json.dumps({
                    'answers': answers,
                    'result': result
                }),
            })

            # Build redirect URL with result
            redirect_url = f"/your-results?type={result['type']}"
            if name:
                redirect_url += f"&name={name}"

            return {
                'success': True,
                'result_type': result['type'],
                'result_headline': result['headline'],
                'result_description': result['description'],
                'redirect_url': redirect_url
            }

        except Exception as e:
            return {'success': False, 'error': str(e)}

    def _calculate_result(self, answers):
        """Calculate quiz result based on answer scoring."""
        # Simple scoring: count answer types
        scores = {}
        for answer in answers:
            value = answer.get('answer_value', 'a')
            scores[value] = scores.get(value, 0) + 1

        # Determine result type by highest score
        if not scores:
            result_type = 'general'
        else:
            result_type = max(scores, key=scores.get)

        # Map result types to outcomes
        result_map = {
            'a': {
                'type': 'achiever',
                'headline': 'You are an Achiever!',
                'description': 'You thrive on goals and results. Your ideal solution focuses on measurable outcomes.'
            },
            'b': {
                'type': 'explorer',
                'headline': 'You are an Explorer!',
                'description': 'You love discovering new approaches. Flexibility and variety are key for you.'
            },
            'c': {
                'type': 'connector',
                'headline': 'You are a Connector!',
                'description': 'Relationships matter most to you. Community and support drive your success.'
            },
            'd': {
                'type': 'strategist',
                'headline': 'You are a Strategist!',
                'description': 'You think long-term and plan carefully. Systems and frameworks work best for you.'
            },
            'general': {
                'type': 'general',
                'headline': 'Your Results Are Ready!',
                'description': 'Based on your answers, here is your personalized recommendation.'
            }
        }

        return result_map.get(result_type, result_map['general'])

    def _format_quiz_results(self, answers, result):
        """Format quiz results for lead description."""
        lines = [
            f"Quiz Result: {result['headline']}",
            f"Result Type: {result['type']}",
            "",
            "Answers:"
        ]
        for i, answer in enumerate(answers, 1):
            lines.append(f"  Q{answer.get('question_id', i)}: {answer.get('answer_value', 'N/A')}")

        return '\n'.join(lines)

    def _add_to_mailing(self, email, name, mailing_list_id):
        """Add contact to mailing list."""
        MailingContact = request.env['mailing.contact'].sudo()
        existing = MailingContact.search([
            ('email', '=ilike', email),
            ('list_ids', 'in', [mailing_list_id])
        ], limit=1)

        if not existing:
            contact = MailingContact.search([('email', '=ilike', email)], limit=1)
            if contact:
                contact.write({'list_ids': [(4, mailing_list_id)]})
            else:
                MailingContact.create({
                    'name': name or email.split('@')[0],
                    'email': email,
                    'list_ids': [(4, mailing_list_id)],
                })

    @http.route('/funnel/quiz/track_start', type='json', auth='public', methods=['POST'])
    def track_quiz_start(self, funnel_id, page_id, **kwargs):
        """Track when user starts a quiz."""
        request.env['funnel.conversion'].sudo().create({
            'funnel_id': int(funnel_id),
            'page_id': int(page_id),
            'event_type': 'quiz_start',
            'visitor_id': request.httprequest.cookies.get('funnel_visitor_id', ''),
        })
        return {'success': True}
```

---

### 2. Quiz JavaScript

**File:** `static/src/js/quiz_manager.js`

```javascript
/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";
import { jsonrpc } from "@web/core/network/rpc_service";

/**
 * Quiz Manager - Handles complete quiz flow
 */
publicWidget.registry.FunnelQuizManager = publicWidget.Widget.extend({
    selector: '.s_quiz_intro, .s_quiz_question, .s_quiz_progress, .s_quiz_gate, .s_quiz_results',

    init: function () {
        this._super.apply(this, arguments);
        this.quizState = this._loadState();
    },

    start: function () {
        this._super.apply(this, arguments);
        this._initQuizElement();
        return Promise.resolve();
    },

    _loadState: function () {
        const stored = sessionStorage.getItem('funnel_quiz_state');
        return stored ? JSON.parse(stored) : {
            started: false,
            currentQuestion: 0,
            answers: [],
            totalQuestions: 5,
        };
    },

    _saveState: function () {
        sessionStorage.setItem('funnel_quiz_state', JSON.stringify(this.quizState));
    },

    _initQuizElement: function () {
        const $el = this.$el;

        if ($el.hasClass('s_quiz_intro')) {
            this._initQuizIntro();
        } else if ($el.hasClass('s_quiz_question')) {
            this._initQuizQuestion();
        } else if ($el.hasClass('s_quiz_progress')) {
            this._updateProgress();
        } else if ($el.hasClass('s_quiz_gate')) {
            this._initQuizGate();
        } else if ($el.hasClass('s_quiz_results')) {
            this._initQuizResults();
        }
    },

    _initQuizIntro: function () {
        this.$('.s_quiz_start').on('click', (ev) => {
            ev.preventDefault();

            // Track quiz start
            const funnelId = this.$el.data('funnel-id');
            const pageId = this.$el.data('page-id');

            if (funnelId && pageId) {
                jsonrpc('/funnel/quiz/track_start', { funnel_id: funnelId, page_id: pageId });
            }

            // Initialize state
            this.quizState = {
                started: true,
                currentQuestion: 0,
                answers: [],
                totalQuestions: parseInt(this.$el.data('total-questions')) || 5,
            };
            this._saveState();

            // Navigate to first question
            const nextUrl = this.$el.data('next-url') || '/quiz-questions';
            window.location.href = nextUrl;
        });
    },

    _initQuizQuestion: function () {
        const questionId = this.$el.data('question-id') || this.quizState.currentQuestion + 1;

        // Show correct question based on state
        this._showQuestion(questionId);

        // Handle answer clicks
        this.$('.s_answer').on('click', (ev) => {
            ev.preventDefault();
            const $answer = $(ev.currentTarget);
            const answerValue = $answer.data('value');

            // Visual feedback
            this.$('.s_answer').removeClass('active btn-primary').addClass('btn-outline-primary');
            $answer.removeClass('btn-outline-primary').addClass('active btn-primary');

            // Store answer
            this.quizState.answers.push({
                question_id: questionId,
                answer_value: answerValue,
            });

            // Check for branching
            const skipTo = $answer.data('skip-to');
            const nextQuestion = skipTo || (this.quizState.currentQuestion + 2);

            this.quizState.currentQuestion++;
            this._saveState();

            // Delay then navigate
            setTimeout(() => {
                if (this.quizState.currentQuestion >= this.quizState.totalQuestions) {
                    // Go to gate page
                    const gateUrl = this.$el.data('gate-url') || '/quiz-results-gate';
                    window.location.href = gateUrl;
                } else {
                    // Next question (or reload for SPA behavior)
                    this._showQuestion(nextQuestion);
                    this._updateProgress();
                }
            }, 300);
        });
    },

    _showQuestion: function (questionId) {
        // Update question display
        const current = this.quizState.currentQuestion + 1;
        const total = this.quizState.totalQuestions;
        this.$('.s_question_counter').text(`Question ${current} of ${total}`);
    },

    _updateProgress: function () {
        const current = this.quizState.currentQuestion;
        const total = this.quizState.totalQuestions;
        const percent = (current / total) * 100;

        this.$('.s_progress_bar').css('width', percent + '%');
        this.$('.s_progress_text').text(`Step ${current + 1} of ${total}`);
    },

    _initQuizGate: function () {
        this.$('.s_quiz_gate_form').on('submit', (ev) => {
            ev.preventDefault();

            const $form = $(ev.currentTarget);
            const $button = $form.find('button[type="submit"]');
            const originalText = $button.text();

            // Disable button
            $button.prop('disabled', true).text('Processing...');

            const name = $form.find('input[name="name"]').val();
            const email = $form.find('input[name="email"]').val();

            const funnelId = this.$el.data('funnel-id');
            const pageId = this.$el.data('page-id');

            // Submit quiz
            jsonrpc('/funnel/quiz/submit', {
                funnel_id: funnelId,
                page_id: pageId,
                answers: this.quizState.answers,
                email: email,
                name: name,
            }).then(response => {
                if (response.success) {
                    // Store result for results page
                    sessionStorage.setItem('quiz_result', JSON.stringify(response));

                    // Clear quiz state
                    sessionStorage.removeItem('funnel_quiz_state');

                    // Redirect to results
                    window.location.href = response.redirect_url;
                } else {
                    $button.prop('disabled', false).text(originalText);
                    alert(response.error || 'Something went wrong. Please try again.');
                }
            }).catch(error => {
                $button.prop('disabled', false).text(originalText);
                alert('An error occurred. Please try again.');
            });
        });
    },

    _initQuizResults: function () {
        // Load result from session storage
        const resultData = sessionStorage.getItem('quiz_result');
        if (resultData) {
            const result = JSON.parse(resultData);
            this._displayResult(result);
            sessionStorage.removeItem('quiz_result');
        } else {
            // Try to get from URL params
            const params = new URLSearchParams(window.location.search);
            const resultType = params.get('type');
            const name = params.get('name');

            if (resultType) {
                this._displayResultByType(resultType, name);
            }
        }
    },

    _displayResult: function (result) {
        this.$('.s_result_type').text(result.result_type);
        this.$('.s_result_headline').text(result.result_headline);
        this.$('.s_result_description').text(result.result_description);
    },

    _displayResultByType: function (resultType, name) {
        // Personalize with name if available
        if (name) {
            const $headline = this.$('.s_result_headline');
            const currentText = $headline.text();
            $headline.text(currentText.replace('You are', `${name}, you are`));
        }

        // Show result-specific content
        this.$(`[data-result-type]`).hide();
        this.$(`[data-result-type="${resultType}"]`).show();
    },
});

export default publicWidget.registry.FunnelQuizManager;
```

---

### 3. Enhanced Quiz Snippets

Update quiz snippet XMLs to support the JavaScript:

**views/snippets/s_quiz_question.xml** (updated):
```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <template id="s_quiz_question" name="Quiz Question">
        <section class="s_quiz_question py-5"
                 data-snippet="sam_ai_funnels.s_quiz_question"
                 data-name="Quiz Question"
                 data-question-id="1"
                 data-gate-url="/quiz-results-gate">
            <div class="container">
                <div class="row justify-content-center">
                    <div class="col-lg-8">
                        <p class="text-center text-muted s_question_counter">Question 1 of 5</p>
                        <h2 class="h3 mb-4 text-center" data-oe-field="question">
                            What is your biggest challenge right now?
                        </h2>
                        <div class="s_answers d-grid gap-3" data-oe-field="answers">
                            <button class="btn btn-outline-primary btn-lg text-start s_answer"
                                    data-value="a">
                                <span class="me-2">A.</span> I struggle with time management
                            </button>
                            <button class="btn btn-outline-primary btn-lg text-start s_answer"
                                    data-value="b">
                                <span class="me-2">B.</span> I need more clients
                            </button>
                            <button class="btn btn-outline-primary btn-lg text-start s_answer"
                                    data-value="c">
                                <span class="me-2">C.</span> I'm overwhelmed with choices
                            </button>
                            <button class="btn btn-outline-primary btn-lg text-start s_answer"
                                    data-value="d">
                                <span class="me-2">D.</span> I lack clarity on my goals
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    </template>
</odoo>
```

---

### 4. Quiz Results with Personalization

**views/snippets/s_quiz_results.xml** (updated):
```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <template id="s_quiz_results" name="Quiz Results">
        <section class="s_quiz_results py-5"
                 data-snippet="sam_ai_funnels.s_quiz_results"
                 data-name="Quiz Results">
            <div class="container">
                <div class="row justify-content-center">
                    <div class="col-lg-8 text-center">
                        <p class="text-muted mb-2">Based on your answers...</p>
                        <h1 class="display-5 fw-bold mb-4 s_result_headline">
                            You are a <span class="text-primary s_result_type">[Result Type]</span>
                        </h1>

                        <!-- Result-specific content blocks -->
                        <div class="s_result_content" data-result-type="achiever">
                            <div class="card mb-4 border-primary">
                                <div class="card-body">
                                    <p class="lead">As an Achiever, you thrive on goals and measurable results.</p>
                                    <p>Your ideal solution focuses on clear outcomes, tracking progress, and celebrating wins.</p>
                                </div>
                            </div>
                        </div>

                        <div class="s_result_content" data-result-type="explorer" style="display:none;">
                            <div class="card mb-4 border-success">
                                <div class="card-body">
                                    <p class="lead">As an Explorer, you love discovering new approaches.</p>
                                    <p>Flexibility and variety are key for you. You need room to experiment.</p>
                                </div>
                            </div>
                        </div>

                        <div class="s_result_content" data-result-type="connector" style="display:none;">
                            <div class="card mb-4 border-warning">
                                <div class="card-body">
                                    <p class="lead">As a Connector, relationships matter most to you.</p>
                                    <p>Community and support drive your success. You thrive with others.</p>
                                </div>
                            </div>
                        </div>

                        <div class="s_result_content" data-result-type="strategist" style="display:none;">
                            <div class="card mb-4 border-info">
                                <div class="card-body">
                                    <p class="lead">As a Strategist, you think long-term and plan carefully.</p>
                                    <p>Systems and frameworks work best for you. You see the big picture.</p>
                                </div>
                            </div>
                        </div>

                        <h3 class="h5 mb-3">Your Personalized Recommendation:</h3>
                        <a href="#" class="btn btn-primary btn-lg">See Your Solution</a>
                    </div>
                </div>
            </div>
        </section>
    </template>
</odoo>
```

---

### 5. Quiz Customize Options

Add to `views/snippets/options.xml`:

```xml
<!-- Quiz Question Options -->
<div data-selector=".s_quiz_question">
    <we-input string="Question" data-attribute-name="data-question"/>
    <we-input string="Question ID" data-attribute-name="data-question-id"/>
    <we-input string="Gate URL" data-attribute-name="data-gate-url"/>
    <we-select string="Answer Layout">
        <we-button data-select-class="s_answers_list">List</we-button>
        <we-button data-select-class="s_answers_grid">Grid (2 col)</we-button>
    </we-select>
    <we-colorpicker string="Background" data-css-property="background-color"/>
</div>

<!-- Quiz Results Options -->
<div data-selector=".s_quiz_results">
    <we-select string="Result Display">
        <we-button data-select-class="s_result_single">Single Result</we-button>
        <we-button data-select-class="s_result_multi">Multiple Outcomes</we-button>
    </we-select>
    <we-checkbox string="Show Score" data-attribute-name="data-show-score"/>
    <we-colorpicker string="Background" data-css-property="background-color"/>
</div>
```

---

### 6. Update Manifest

```python
'assets': {
    'web.assets_frontend': [
        # ... existing ...
        'sam_ai_funnels/static/src/js/quiz_manager.js',
    ],
},
```

Update controllers/__init__.py:
```python
from . import quiz_controller
```

---

## VALIDATION CHECKLIST

- [ ] Quiz intro "Start Quiz" button works
- [ ] Quiz tracks start event
- [ ] Answer selection stores in session
- [ ] Progress bar updates correctly
- [ ] Branching/skip logic works
- [ ] Email gate captures before results
- [ ] Quiz submission creates lead with answers
- [ ] Lead has quiz results in description
- [ ] Results page shows personalized content
- [ ] Result type from URL works
- [ ] Name personalization works
- [ ] Mailing list integration works

---

## COMPLETE MODULE STRUCTURE (Final)

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
│   ├── funnel_conversion.py
│   └── sam_funnel_context.py
├── controllers/
│   ├── __init__.py
│   ├── funnel_controller.py
│   ├── funnel_form_controller.py
│   ├── sam_funnel_api.py
│   └── quiz_controller.py
├── wizards/
│   ├── __init__.py
│   └── funnel_generator_wizard.py
├── views/
│   ├── funnel_definition_views.xml
│   ├── funnel_page_views.xml
│   ├── funnel_template_views.xml
│   ├── funnel_snippet_views.xml
│   ├── funnel_conversion_views.xml
│   ├── funnel_dashboard.xml
│   ├── funnel_menus.xml
│   ├── funnel_form_error.xml
│   └── snippets/
│       ├── options.xml
│       └── s_*.xml (46 files)
├── wizards/
│   └── funnel_generator_wizard_views.xml
├── data/
│   ├── funnel_snippet_data.xml
│   ├── funnel_templates.xml
│   └── sam_funnel_knowledge.xml
├── static/
│   └── src/
│       ├── snippets/
│       │   └── s_*/
│       │       ├── 000.js
│       │       └── 000.scss
│       ├── js/
│       │   ├── funnel_form.js
│       │   ├── funnel_tracking.js
│       │   ├── funnel_snippet_options.js
│       │   └── quiz_manager.js
│       └── img/
│           └── thumbnails/
└── security/
    └── ir.model.access.csv
```

---

## MODULE COMPLETE

With Phase 7 complete, the SAM AI Funnels module is fully implemented with:

- FUNNELS tab in website builder (46 snippets)
- 6 complete funnel templates
- CRM and mailing list integration
- Conversion analytics
- SAM AI integration for automated funnel building
- Interactive quiz functionality

---

**END OF PHASE 7 DEVELOPER PROMPT**

**END OF IMPLEMENTATION PHASES**
