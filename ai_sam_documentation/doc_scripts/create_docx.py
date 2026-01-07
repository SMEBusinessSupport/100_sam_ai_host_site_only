from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT

def create_questionnaire_docx():
    doc = Document()

    # Title
    title = doc.add_heading('AI Voice & Content Tone Questionnaire', 0)
    title.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER

    # Section 1
    doc.add_heading('Section 1: My Work Philosophy', 1)

    doc.add_paragraph('1. Speed vs. Perfection: Where do I naturally sit?')
    doc.add_paragraph('   • 1 = Ship it now, iterate later', style='List Bullet')
    doc.add_paragraph('   • 10 = Perfect or nothing', style='List Bullet')
    doc.add_paragraph('   • My score: ___')
    doc.add_paragraph('   • Why this number?')
    doc.add_paragraph()

    doc.add_paragraph('2. When facing a customer deliverable, I prioritize (rank 1-5):')
    doc.add_paragraph('   ___ Speed to market')
    doc.add_paragraph('   ___ Technical excellence')
    doc.add_paragraph('   ___ Customer perception of value')
    doc.add_paragraph('   ___ Long-term maintainability')
    doc.add_paragraph('   ___ Revenue generation')
    doc.add_paragraph()

    doc.add_paragraph('3. "Good enough" means to me:')
    doc.add_paragraph('   (Write your definition in 2-3 sentences)')
    doc.add_paragraph()

    doc.add_paragraph('4. The biggest risk in our business is:')
    doc.add_paragraph('   ☐ Moving too slowly and missing opportunities')
    doc.add_paragraph('   ☐ Delivering subpar work and damaging reputation')
    doc.add_paragraph('   ☐ Not automating/scaling properly')
    doc.add_paragraph('   ☐ Not differentiating from competitors')
    doc.add_paragraph('   ☐ Not having clear customer value proposition')
    doc.add_paragraph('   ☐ Other: ___________')
    doc.add_paragraph()

    # Section 2
    doc.add_heading('Section 2: My Decision-Making Process', 1)

    doc.add_paragraph('5. I struggle to move forward when (check all that apply):')
    doc.add_paragraph('   ☐ I don\'t have enough technical detail')
    doc.add_paragraph('   ☐ The customer value isn\'t crystal clear')
    doc.add_paragraph('   ☐ I haven\'t validated the approach thoroughly')
    doc.add_paragraph('   ☐ The solution isn\'t automated/scalable')
    doc.add_paragraph('   ☐ The output doesn\'t meet my quality standards')
    doc.add_paragraph('   ☐ We\'re distracted by new opportunities instead of executing')
    doc.add_paragraph('   ☐ I don\'t have confidence in the approach')
    doc.add_paragraph('   ☐ Other: ___________')
    doc.add_paragraph()

    doc.add_paragraph('6. Complete this sentence: "I trust AI-generated content when..."')
    doc.add_paragraph()

    doc.add_paragraph('7. What holds me back from moving faster:')
    doc.add_paragraph()

    doc.add_paragraph('8. What frustrates me about moving too slowly:')
    doc.add_paragraph()

    doc.add_paragraph('9. I make my best decisions when:')
    doc.add_paragraph()

    # Section 3
    doc.add_heading('Section 3: Customer Communication Values', 1)

    doc.add_paragraph('10. Our customer content MUST be (rank 1-5):')
    doc.add_paragraph('    ___ Technically accurate above all')
    doc.add_paragraph('    ___ Action-oriented and concise')
    doc.add_paragraph('    ___ Builds trust through detail')
    doc.add_paragraph('    ___ Demonstrates clear ROI/value')
    doc.add_paragraph('    ___ Differentiated from competitors')
    doc.add_paragraph()

    doc.add_paragraph('11. When customers read our content, I want them to feel:')
    doc.add_paragraph('    (One sentence)')
    doc.add_paragraph()

    doc.add_paragraph('12. The worst thing our content could do is:')
    doc.add_paragraph('    ☐ Sound generic/AI-generated')
    doc.add_paragraph('    ☐ Lack technical credibility')
    doc.add_paragraph('    ☐ Fail to drive action/revenue')
    doc.add_paragraph('    ☐ Overpromise')
    doc.add_paragraph('    ☐ Waste their time')
    doc.add_paragraph('    ☐ Be incomplete or unclear')
    doc.add_paragraph('    ☐ Other: ___________')
    doc.add_paragraph()

    doc.add_paragraph('13. A customer should choose us because:')
    doc.add_paragraph('    (2-3 sentences in your own words)')
    doc.add_paragraph()

    # Section 4
    doc.add_heading('Section 4: My Ideal AI Voice', 1)

    doc.add_paragraph('14. Our AI voice should sound like (pick your top 3):')
    doc.add_paragraph('    ☐ Expert advisor')
    doc.add_paragraph('    ☐ Trusted partner')
    doc.add_paragraph('    ☐ Efficient consultant')
    doc.add_paragraph('    ☐ Technical authority')
    doc.add_paragraph('    ☐ Results-driven hustler')
    doc.add_paragraph('    ☐ Detail-oriented specialist')
    doc.add_paragraph('    ☐ No-nonsense problem solver')
    doc.add_paragraph('    ☐ Innovative thought leader')
    doc.add_paragraph('    ☐ Other: ___________')
    doc.add_paragraph()

    doc.add_paragraph('15. Tone elements I value (rate each 1-10, where 10 = maximum):')
    doc.add_paragraph('    ___ Professional formality')
    doc.add_paragraph('    ___ Casual friendliness')
    doc.add_paragraph('    ___ Urgency/action-orientation')
    doc.add_paragraph('    ___ Technical depth')
    doc.add_paragraph('    ___ Brevity/conciseness')
    doc.add_paragraph('    ___ Warmth/personality')
    doc.add_paragraph('    ___ Authority/confidence')
    doc.add_paragraph()

    doc.add_paragraph('16. Words/phrases I want in our content:')
    doc.add_paragraph('    (List 5-7 words or short phrases)')
    doc.add_paragraph()

    doc.add_paragraph('17. Words/phrases I never want to see:')
    doc.add_paragraph('    (List 5-7 words or short phrases)')
    doc.add_paragraph()

    doc.add_paragraph('18. Write a 3-sentence pitch for our services in YOUR authentic voice:')
    doc.add_paragraph()

    # Section 5
    doc.add_heading('Section 5: Quality & Standards', 1)

    doc.add_paragraph('19. Before any content goes to a customer, it MUST (check your non-negotiables):')
    doc.add_paragraph('    ☐ Be technically accurate')
    doc.add_paragraph('    ☐ Have clear call-to-action')
    doc.add_paragraph('    ☐ Demonstrate specific value/ROI')
    doc.add_paragraph('    ☐ Sound professional')
    doc.add_paragraph('    ☐ Be free of obvious AI patterns')
    doc.add_paragraph('    ☐ Be concise (no fluff)')
    doc.add_paragraph('    ☐ Have proper structure/formatting')
    doc.add_paragraph('    ☐ Be proofread for errors')
    doc.add_paragraph('    ☐ Other: ___________')
    doc.add_paragraph()

    doc.add_paragraph('20. If I only had time for ONE quality check, it would be:')
    doc.add_paragraph()

    doc.add_paragraph('21. Content is ready to ship when:')
    doc.add_paragraph('    (Your personal definition)')
    doc.add_paragraph()

    # Section 6
    doc.add_heading('Section 6: Success & Values', 1)

    doc.add_paragraph('22. In 6 months, success looks like:')
    doc.add_paragraph('    • Revenue-wise: ___')
    doc.add_paragraph('    • Customer-wise: ___')
    doc.add_paragraph('    • Efficiency-wise: ___')
    doc.add_paragraph()

    doc.add_paragraph('23. My core value that should be reflected in our AI voice:')
    doc.add_paragraph('    (One word or short phrase, then explain why in 1-2 sentences)')
    doc.add_paragraph()

    doc.add_paragraph('24. When I see new opportunities, my instinct is to:')
    doc.add_paragraph('    ☐ Jump on them immediately (that\'s how we find gold)')
    doc.add_paragraph('    ☐ Document them for later (finish what we started first)')
    doc.add_paragraph('    ☐ Evaluate them with strict criteria before deciding')
    doc.add_paragraph('    ☐ Other: ___________')
    doc.add_paragraph()

    doc.add_paragraph('25. The balance I want to strike:')
    doc.add_paragraph('    (Describe the tension you feel and what the ideal middle ground is)')
    doc.add_paragraph()

    # Section 7
    doc.add_heading('Section 7: My Honest Concerns', 1)

    doc.add_paragraph('26. What I\'m afraid of in our business:')
    doc.add_paragraph()

    doc.add_paragraph('27. What I\'m most confident about:')
    doc.add_paragraph()

    doc.add_paragraph('28. If our AI voice could solve ONE problem for me, it would be:')
    doc.add_paragraph()

    doc.add_paragraph('29. My definition of "cutting through the noise":')
    doc.add_paragraph()

    doc.add_paragraph('30. The final check: Write 2-3 sentences about our services right now, in whatever style feels most natural to you. Don\'t overthink it.')
    doc.add_paragraph()

    # Completion section
    doc.add_page_break()
    doc.add_heading('Completion', 1)
    doc.add_paragraph('Once you\'ve filled this out, save it as a separate file with your name (e.g., "Dennis_AI_Voice.docx" or "John_AI_Voice.docx").')
    doc.add_paragraph()
    doc.add_paragraph('The AI will analyze both individual responses independently and create a synthesized voice that honors both perspectives without either person having to see the other\'s raw answers (unless you choose to share them).')

    doc.save('C:\\Users\\total\\AI_Voice_Questionnaire.docx')
    print("Created: AI_Voice_Questionnaire.docx")

def create_synthesis_prompt_docx():
    doc = Document()

    # Title
    title = doc.add_heading('AI Voice Synthesis Prompt', 0)
    title.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER

    # Instructions
    doc.add_heading('Instructions for Use', 1)
    doc.add_paragraph('After both individuals have completed their questionnaires independently:')
    doc.add_paragraph('1. Save each person\'s completed questionnaire as separate files', style='List Number')
    doc.add_paragraph('2. Use the prompt below, inserting both completed questionnaires', style='List Number')
    doc.add_paragraph('3. The AI will create a unified voice guideline', style='List Number')
    doc.add_paragraph()

    # Main Prompt
    doc.add_heading('Prompt to Feed the AI', 1)

    prompt_text = """I need you to analyze two independently completed questionnaires about AI voice, content tone, and work values. These are from business partners who need to create a unified content voice that works for both.

Your job is to:
1. Identify the shared core values (the foundation)
2. Identify complementary strengths (where differences are assets)
3. Identify potential friction points (where compromise is needed)
4. Create a practical, actionable AI Voice Guide

Do NOT show the raw comparison or call out individuals. Create the synthesis as if it's a third, independent voice that naturally honors both perspectives."""

    doc.add_paragraph(prompt_text)
    doc.add_paragraph()

    # Questionnaire placeholders
    doc.add_heading('QUESTIONNAIRE RESPONSE SET 1:', 2)
    doc.add_paragraph('[PASTE FIRST PERSON\'S COMPLETED QUESTIONNAIRE HERE]')
    doc.add_paragraph()

    doc.add_heading('QUESTIONNAIRE RESPONSE SET 2:', 2)
    doc.add_paragraph('[PASTE SECOND PERSON\'S COMPLETED QUESTIONNAIRE HERE]')
    doc.add_paragraph()

    # What to create
    doc.add_heading('Please Create:', 2)

    sections = [
        ('1. Core Values Foundation (3-5 principles)',
         'What both perspectives agree on, stated as principles for all content.\n\nExample format:\n• [Principle Name]: [What this means in practice]'),

        ('2. Our AI Voice Profile',
         'Synthesize into a cohesive voice description including:\n• Personality: [3-4 adjectives that work for both]\n• Tone: [Describe the balanced tone]\n• Style: [How this voice communicates]\n• What makes us different: [Unique positioning]'),

        ('3. Content Quality Framework',
         'Create clear "done" criteria that satisfy both perspectives:\n\nMust Have (Non-Negotiables):\n• [List items both marked as critical]\n\nShould Have (Strong Preference):\n• [List items valued by both]\n\nSpeed vs Polish Protocol:\n• [Create if/then rules for when to optimize for speed vs when to optimize for quality]'),

        ('4. Practical Writing Guidelines',
         'Always Include:\n• [Elements both value]\n\nNever Include:\n• [Things both want to avoid]\n\nPreferred Language:\n• Use: [Words/phrases both selected]\n• Avoid: [Words/phrases both rejected]\n\nStructure:\n• [How content should be organized]'),

        ('5. The Compromise Protocol',
         'Create specific scenarios with decision rules:\n\nCustomer-facing content:\n• Standard: [What\'s the baseline]\n• Review trigger: [When extra review is needed]\n• Timeline: [Default turnaround]\n\nInternal/marketing content:\n• Standard: [What\'s the baseline]\n• Review trigger: [When extra review is needed]\n• Timeline: [Default turnaround]\n\nNew opportunity evaluation:\n• [Rules for when to pursue vs when to defer]'),

        ('6. Voice Examples',
         'Rewrite this sample message in YOUR synthesized voice:\n\nGeneric version: "We provide Odoo consulting services to help businesses implement ERP solutions that improve efficiency."\n\nOur Voice Version: [Rewrite this in the synthesized voice that balances both perspectives]\n\nThen create 2 more examples:\n• Email to potential customer: [Write 3-4 sentences]\n• Social media post: [Write 2-3 sentences]'),

        ('7. Red Flags Checklist',
         'Before shipping any content, check for these red flags:\n☐ [List specific things that would concern either perspective]\n☐ [Include both "sounds too generic" AND "too slow to ship" type concerns]'),

        ('8. The Success Metrics',
         'Based on both 6-month visions, our content is working when:\n• [Synthesized success criteria]'),

        ('9. Ready-to-Use Content Approval Questions',
         'When reviewing AI-generated content, ask:\n1. [Question that addresses perspective 1\'s core concern]\n2. [Question that addresses perspective 2\'s core concern]\n3. [Question about customer value]\n4. [Question about action/revenue]\n5. [Final gut-check question]\n\nIf YES to all 5, ship it.'),

        ('10. The Partnership Agreement',
         'Based on the concerns and values expressed:\n\nWhen to prioritize speed: [Specific conditions]\nWhen to prioritize precision: [Specific conditions]\nWhen you\'re stuck: [Tiebreaker rule]')
    ]

    for heading, content in sections:
        doc.add_heading(heading, 3)
        doc.add_paragraph(content)
        doc.add_paragraph()

    doc.add_paragraph('Make this practical, specific, and immediately usable. This is not theoretical—they need to make money together using this voice starting today.')
    doc.add_paragraph()

    # After section
    doc.add_page_break()
    doc.add_heading('After You Get the AI Output', 1)
    doc.add_paragraph('1. Review the synthesized voice guide together', style='List Number')
    doc.add_paragraph('2. Test it on 2-3 pieces of existing content', style='List Number')
    doc.add_paragraph('3. Adjust any guidelines that don\'t feel right', style='List Number')
    doc.add_paragraph('4. Save the final version as your official "AI Voice Guide"', style='List Number')
    doc.add_paragraph('5. Use it as the prompt foundation for all future AI content generation', style='List Number')
    doc.add_paragraph()
    doc.add_paragraph('This becomes your shared source of truth.')

    doc.save('C:\\Users\\total\\AI_Voice_Synthesis_Prompt.docx')
    print("Created: AI_Voice_Synthesis_Prompt.docx")

if __name__ == '__main__':
    create_questionnaire_docx()
    create_synthesis_prompt_docx()
    print("\nBoth Word documents created successfully!")
