# Developer Prompt: SAM AI Funnels - Phase 5 (Remaining Snippets)

**Date:** 2025-12-31
**Phase:** 5 of 7
**Scope:** Complete remaining 31 snippets to reach full 46-snippet library
**Prerequisite:** Phase 4 complete

---

## CONTEXT

Phases 1-4 created the foundation, 15 core snippets, form integration, and funnel templates. Now we complete the full snippet library by adding the remaining 31 snippets.

---

## GOAL

Add all remaining snippets to complete the 46-snippet library as defined in the requirements.

---

## REMAINING SNIPPETS (31 Total)

### Hero Sections (1 remaining)
| Snippet | Description |
|---------|-------------|
| `hero_video` | Video hero with background video, overlay text, CTA |

### Problem & Story (2 remaining)
| Snippet | Description |
|---------|-------------|
| `story_bridge` | Founder/origin story section |
| `before_after` | Two-column before/after comparison |

### Solution & Benefits (3 remaining)
| Snippet | Description |
|---------|-------------|
| `solution_reveal` | Introduce the solution/offer |
| `features_grid` | Feature cards in grid layout |
| `how_it_works` | Numbered step-by-step process |

### Social Proof (5 remaining)
| Snippet | Description |
|---------|-------------|
| `testimonial_grid` | Multiple testimonials in grid |
| `testimonial_video` | Video testimonial with name/context |
| `trust_badges` | Logo grid for certifications/partners |
| `case_study_preview` | Mini case study card |
| `stats_bar` | Impressive numbers bar |

### Offers & Pricing (2 remaining)
| Snippet | Description |
|---------|-------------|
| `bonus_stack` | Additional bonuses section |
| `pricing_table` | Multi-tier pricing comparison |

### CTAs & Forms (2 remaining)
| Snippet | Description |
|---------|-------------|
| `cta_button_block` | Standalone large CTA button |
| `ps_section` | P.S. urgency section |

### Quiz Elements (5 - all new)
| Snippet | Description |
|---------|-------------|
| `quiz_intro` | Quiz hook + start button |
| `quiz_question` | Single question with answer options |
| `quiz_progress` | Progress bar/step indicator |
| `quiz_gate` | Email capture before results |
| `quiz_results` | Personalized outcome display |

### Urgency & Trust (2 remaining)
| Snippet | Description |
|---------|-------------|
| `urgency_bar` | Scarcity message banner |
| `risk_reversal` | Address "what if" objections |

### Utility (3 remaining)
| Snippet | Description |
|---------|-------------|
| `divider_styled` | Styled visual separator |
| `image_text_split` | Side-by-side image + text |
| `bullet_list` | Styled bullet list |

---

## IMPLEMENTATION PATTERN

Follow the same pattern established in Phase 2:

### 1. XML Template (per snippet)
```xml
<!-- views/snippets/s_[snippet_name].xml -->
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <template id="s_[snippet_name]" name="[Display Name]">
        <section class="s_[snippet_name] py-5"
                 data-snippet="sam_ai_funnels.s_[snippet_name]"
                 data-name="[Display Name]">
            <!-- HTML content -->
        </section>
    </template>
</odoo>
```

### 2. Register in options.xml
```xml
<t t-snippet="sam_ai_funnels.s_[snippet_name]"
   string="[Display Name]"
   group="funnels">
    <keywords>[relevant, search, terms]</keywords>
</t>
```

### 3. Customize Options in options.xml
```xml
<div data-selector=".s_[snippet_name]">
    <!-- we-input, we-select, we-colorpicker, etc. -->
</div>
```

### 4. SCSS File
```scss
/* static/src/snippets/s_[snippet_name]/000.scss */
.s_[snippet_name] {
    /* styles */
}
```

### 5. JS File (if interactive)
```javascript
/* static/src/snippets/s_[snippet_name]/000.js */
/** @odoo-module **/
import publicWidget from "@web/legacy/js/public/public_widget";
// Widget code
```

---

## SNIPPET SPECIFICATIONS

### hero_video
```xml
<section class="s_hero_video py-0 position-relative overflow-hidden"
         data-snippet="sam_ai_funnels.s_hero_video"
         data-name="Video Hero"
         data-autoplay="true"
         data-loop="true">
    <video class="s_video_bg position-absolute w-100 h-100" style="object-fit: cover;" autoplay muted loop playsinline>
        <source src="" type="video/mp4"/>
    </video>
    <div class="s_overlay position-absolute w-100 h-100" style="background: rgba(0,0,0,0.5);"></div>
    <div class="container position-relative py-5">
        <div class="row justify-content-center text-center text-white">
            <div class="col-lg-8 py-5">
                <h1 class="display-4 fw-bold mb-3">Your Video Hero Headline</h1>
                <p class="lead mb-4">Compelling subheadline over background video</p>
                <a href="#" class="btn btn-primary btn-lg">Get Started</a>
            </div>
        </div>
    </div>
</section>
```

### story_bridge
```xml
<section class="s_story_bridge py-5">
    <div class="container">
        <div class="row align-items-center">
            <div class="col-lg-4 mb-4 mb-lg-0">
                <img src="/web/image/website.s_banner_default_image" class="img-fluid rounded" alt="Author"/>
            </div>
            <div class="col-lg-8">
                <h2 class="h4 mb-3">My Story</h2>
                <p class="lead">I used to be just like you...</p>
                <p>Tell your origin story here. Connect emotionally with your audience.</p>
                <p class="fst-italic">— Your Name, Founder</p>
            </div>
        </div>
    </div>
</section>
```

### before_after
```xml
<section class="s_before_after py-5">
    <div class="container">
        <h2 class="text-center mb-5">The Transformation</h2>
        <div class="row">
            <div class="col-md-6 mb-4 mb-md-0">
                <div class="card border-danger h-100">
                    <div class="card-header bg-danger text-white">
                        <strong>Before</strong>
                    </div>
                    <div class="card-body">
                        <ul class="list-unstyled">
                            <li class="mb-2">❌ Pain point 1</li>
                            <li class="mb-2">❌ Pain point 2</li>
                            <li class="mb-2">❌ Pain point 3</li>
                        </ul>
                    </div>
                </div>
            </div>
            <div class="col-md-6">
                <div class="card border-success h-100">
                    <div class="card-header bg-success text-white">
                        <strong>After</strong>
                    </div>
                    <div class="card-body">
                        <ul class="list-unstyled">
                            <li class="mb-2">✅ Benefit 1</li>
                            <li class="mb-2">✅ Benefit 2</li>
                            <li class="mb-2">✅ Benefit 3</li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>
```

### quiz_intro
```xml
<section class="s_quiz_intro py-5 text-center">
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-lg-8">
                <h1 class="display-5 fw-bold mb-3">Discover Your [X] Type</h1>
                <p class="lead mb-4">Take this quick 2-minute quiz to get personalized recommendations</p>
                <p class="text-muted mb-4"><i class="fa fa-clock-o"></i> Takes about 2 minutes</p>
                <button class="btn btn-primary btn-lg s_quiz_start">Start Quiz</button>
                <p class="small text-muted mt-3">Join 50,000+ who've taken this quiz</p>
            </div>
        </div>
    </div>
</section>
```

### quiz_question
```xml
<section class="s_quiz_question py-5" data-question-id="1">
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-lg-8">
                <h2 class="h3 mb-4 text-center">Question 1 of 5</h2>
                <p class="lead text-center mb-4">What is your biggest challenge right now?</p>
                <div class="s_answers d-grid gap-3">
                    <button class="btn btn-outline-primary btn-lg text-start s_answer" data-value="a">
                        Option A: I struggle with time management
                    </button>
                    <button class="btn btn-outline-primary btn-lg text-start s_answer" data-value="b">
                        Option B: I need more clients
                    </button>
                    <button class="btn btn-outline-primary btn-lg text-start s_answer" data-value="c">
                        Option C: I'm overwhelmed with choices
                    </button>
                    <button class="btn btn-outline-primary btn-lg text-start s_answer" data-value="d">
                        Option D: I lack clarity on my goals
                    </button>
                </div>
            </div>
        </div>
    </div>
</section>
```

### quiz_progress
```xml
<section class="s_quiz_progress py-3">
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-lg-8">
                <div class="d-flex justify-content-between mb-2">
                    <span class="small text-muted">Progress</span>
                    <span class="small text-muted s_progress_text">Step 1 of 5</span>
                </div>
                <div class="progress" style="height: 8px;">
                    <div class="progress-bar s_progress_bar" style="width: 20%;"></div>
                </div>
            </div>
        </div>
    </div>
</section>
```

### quiz_gate
```xml
<section class="s_quiz_gate py-5 text-center">
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-lg-6">
                <h2 class="h3 mb-3">Your Results Are Ready!</h2>
                <p class="text-muted mb-4">Enter your email to see your personalized results</p>
                <form class="s_quiz_gate_form">
                    <input type="text" name="name" class="form-control form-control-lg mb-3" placeholder="Your Name"/>
                    <input type="email" name="email" class="form-control form-control-lg mb-3" placeholder="Your Email" required/>
                    <button type="submit" class="btn btn-primary btn-lg w-100">See My Results</button>
                </form>
                <p class="small text-muted mt-3">We respect your privacy. Unsubscribe anytime.</p>
            </div>
        </div>
    </div>
</section>
```

### quiz_results
```xml
<section class="s_quiz_results py-5">
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-lg-8 text-center">
                <p class="text-muted mb-2">Based on your answers...</p>
                <h1 class="display-5 fw-bold mb-4">You are a <span class="text-primary">[Result Type]</span></h1>
                <div class="card mb-4">
                    <div class="card-body">
                        <p class="lead">What this means for you:</p>
                        <p>Personalized description based on quiz results...</p>
                    </div>
                </div>
                <h3 class="h5 mb-3">Your Personalized Recommendation:</h3>
                <a href="#" class="btn btn-primary btn-lg">See Your Solution</a>
            </div>
        </div>
    </div>
</section>
```

### stats_bar
```xml
<section class="s_stats_bar py-4 bg-light">
    <div class="container">
        <div class="row text-center">
            <div class="col-md-3 col-6 mb-3 mb-md-0">
                <div class="display-5 fw-bold text-primary">500+</div>
                <p class="text-muted mb-0">Happy Customers</p>
            </div>
            <div class="col-md-3 col-6 mb-3 mb-md-0">
                <div class="display-5 fw-bold text-primary">99%</div>
                <p class="text-muted mb-0">Satisfaction Rate</p>
            </div>
            <div class="col-md-3 col-6">
                <div class="display-5 fw-bold text-primary">24/7</div>
                <p class="text-muted mb-0">Support Available</p>
            </div>
            <div class="col-md-3 col-6">
                <div class="display-5 fw-bold text-primary">10+</div>
                <p class="text-muted mb-0">Years Experience</p>
            </div>
        </div>
    </div>
</section>
```

### pricing_table
```xml
<section class="s_pricing_table py-5">
    <div class="container">
        <h2 class="text-center mb-5">Choose Your Plan</h2>
        <div class="row justify-content-center">
            <div class="col-lg-4 col-md-6 mb-4">
                <div class="card h-100">
                    <div class="card-header text-center py-3">
                        <h3 class="h5 mb-0">Basic</h3>
                    </div>
                    <div class="card-body text-center">
                        <div class="display-4 fw-bold mb-3">$29</div>
                        <p class="text-muted">/month</p>
                        <ul class="list-unstyled mb-4">
                            <li class="mb-2">✓ Feature 1</li>
                            <li class="mb-2">✓ Feature 2</li>
                            <li class="mb-2 text-muted">✗ Feature 3</li>
                        </ul>
                        <a href="#" class="btn btn-outline-primary w-100">Get Started</a>
                    </div>
                </div>
            </div>
            <div class="col-lg-4 col-md-6 mb-4">
                <div class="card h-100 border-primary">
                    <div class="card-header text-center py-3 bg-primary text-white">
                        <h3 class="h5 mb-0">Pro <span class="badge bg-warning">Popular</span></h3>
                    </div>
                    <div class="card-body text-center">
                        <div class="display-4 fw-bold mb-3">$79</div>
                        <p class="text-muted">/month</p>
                        <ul class="list-unstyled mb-4">
                            <li class="mb-2">✓ Feature 1</li>
                            <li class="mb-2">✓ Feature 2</li>
                            <li class="mb-2">✓ Feature 3</li>
                        </ul>
                        <a href="#" class="btn btn-primary w-100">Get Started</a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>
```

*(Similar patterns for remaining snippets - use requirements document for field specifications)*

---

## UPDATE MANIFEST

Add all new snippet files to `__manifest__.py`:

```python
'data': [
    # ... existing files ...

    # New snippets
    'views/snippets/s_hero_video.xml',
    'views/snippets/s_story_bridge.xml',
    'views/snippets/s_before_after.xml',
    'views/snippets/s_solution_reveal.xml',
    'views/snippets/s_features_grid.xml',
    'views/snippets/s_how_it_works.xml',
    'views/snippets/s_testimonial_grid.xml',
    'views/snippets/s_testimonial_video.xml',
    'views/snippets/s_trust_badges.xml',
    'views/snippets/s_case_study_preview.xml',
    'views/snippets/s_stats_bar.xml',
    'views/snippets/s_bonus_stack.xml',
    'views/snippets/s_pricing_table.xml',
    'views/snippets/s_cta_button_block.xml',
    'views/snippets/s_ps_section.xml',
    'views/snippets/s_quiz_intro.xml',
    'views/snippets/s_quiz_question.xml',
    'views/snippets/s_quiz_progress.xml',
    'views/snippets/s_quiz_gate.xml',
    'views/snippets/s_quiz_results.xml',
    'views/snippets/s_urgency_bar.xml',
    'views/snippets/s_risk_reversal.xml',
    'views/snippets/s_divider_styled.xml',
    'views/snippets/s_image_text_split.xml',
    'views/snippets/s_bullet_list.xml',
],
'assets': {
    'web.assets_frontend': [
        # ... existing assets ...

        # New SCSS
        'sam_ai_funnels/static/src/snippets/s_hero_video/000.scss',
        'sam_ai_funnels/static/src/snippets/s_story_bridge/000.scss',
        # ... all new snippet SCSS files ...

        # Quiz JS (interactive)
        'sam_ai_funnels/static/src/snippets/s_quiz_intro/000.js',
        'sam_ai_funnels/static/src/snippets/s_quiz_question/000.js',
        'sam_ai_funnels/static/src/snippets/s_quiz_gate/000.js',
    ],
},
```

---

## VALIDATION CHECKLIST

- [ ] All 31 new snippets appear in FUNNELS tab
- [ ] Snippets draggable to page
- [ ] Customize options work for each
- [ ] Quiz snippets have JS interaction
- [ ] Responsive on mobile
- [ ] Total snippet count = 46

---

## FILES TO CREATE

**XML (25 files):**
1-25. `views/snippets/s_[snippet_name].xml` for each remaining snippet

**SCSS (25 files):**
26-50. `static/src/snippets/s_[snippet_name]/000.scss`

**JS (4 files - quiz interactive):**
51. `static/src/snippets/s_quiz_intro/000.js`
52. `static/src/snippets/s_quiz_question/000.js`
53. `static/src/snippets/s_quiz_progress/000.js`
54. `static/src/snippets/s_quiz_gate/000.js`

**Update:**
55. `views/snippets/options.xml` (register all + customize options)
56. `__manifest__.py`

---

**END OF PHASE 5 DEVELOPER PROMPT**
