# SAM AI Page Builder - Usage Guide

## Getting Started

### Creating Your First Page

1. **Navigate to the module**
   - Click **SAM AI Page Builder** in the top menu
   - Click **AI Pages**

2. **Create a new page**
   - Click the **Create** button
   - Enter a page name (e.g., "Landing Page")
   - Optionally add a description
   - Click **Save**

3. **Open the builder**
   - Click the **Open Builder** button in the form header
   - The AI Page Builder interface will open

## The Builder Interface

The builder has three main areas:

### 1. Top Bar
- **Back button** (←): Return to the page list
- **Page name**: Shows current page name
- **AI Page Builder badge**: Indicates you're in the builder

### 2. Left Panel: AI Chat

This is where you interact with the AI assistant.

**Features:**
- **Chat history**: See all your prompts and AI responses
- **Prompt input**: Type your requests at the bottom
- **Send button**: Click or press Enter to send
- **Clear button**: Remove all chat history

**Tips:**
- Be specific in your prompts
- You can refine results with follow-up prompts
- Use Shift+Enter for multi-line prompts

### 3. Right Panel: Preview & Code

This shows your generated content.

**Tabs:**
- **Preview**: Live rendered page
- **HTML**: View HTML code
- **CSS**: View CSS styles
- **JavaScript**: View JS code

**Controls:**
- **Zoom controls** (Preview tab): Adjust preview scale
- **Refresh**: Reload the preview
- **Save**: Save content to database
- **Copy**: Copy code to clipboard
- **Download**: Download code as file

## Using the AI Assistant

### Example Prompts

#### Landing Pages
```
Build a landing page with:
- Hero section with headline and CTA button
- 3 feature cards with icons
- Call-to-action section at the bottom
```

#### Product Pages
```
Create a product showcase page with:
- Large product image
- Product details and pricing
- Add to cart button
- Customer reviews section
```

#### Pricing Pages
```
Design a pricing page with 3 tiers:
- Basic, Pro, and Enterprise
- Feature comparison
- Highlight the Pro tier
- Modern card design
```

#### Contact Pages
```
Make a contact page with:
- Contact form (name, email, message)
- Company address and phone
- Social media links
- Modern, clean layout
```

### Refining Generated Content

After the initial generation, you can refine:

**Change Colors:**
```
Change the color scheme to blue and white
```

**Add Sections:**
```
Add a testimonials section with 3 customer quotes
```

**Modify Layout:**
```
Make the hero section taller and center the content
```

**Add Animations:**
```
Add smooth scroll animations to the feature cards
```

**Adjust Styling:**
```
Make the design more modern and minimalist
```

### Understanding AI Responses

When the AI generates content, you'll see:
- ✅ **Success message**: "Generated page based on: [your prompt]"
- 📦 **Content badges**: HTML, CSS, JS indicators
- ⏱️ **Timestamp**: When the response was generated

The generated content automatically appears in the preview panel.

## Working with Generated Content

### Preview Mode

**Features:**
- Live rendering of HTML/CSS/JS
- Interactive (buttons, links work)
- Zoom controls (25% - 200%)
- Responsive preview

**Controls:**
- **Zoom In** (+): Increase preview size
- **Zoom Out** (−): Decrease preview size
- **Reset** (⤢): Return to 100%
- **Refresh** (↻): Reload preview

### Code Viewing

Switch to HTML, CSS, or JavaScript tabs to:
- **View** the generated code
- **Copy** to clipboard (click Copy button)
- **Download** as file (click Download button)

**Code Features:**
- Syntax highlighting
- Scrollable code view
- Monospace font for readability
- Line wrapping for long lines

### Saving Your Work

**Auto-save**: Content is NOT automatically saved.

**Manual save**:
1. Click the **Save** button (top-right)
2. Wait for "Page saved successfully!" notification
3. The page state updates to "Generated"

**When to save:**
- After generating content you like
- Before closing the builder
- After making refinements

## Managing Pages

### Page List View

From **SAM AI Page Builder → AI Pages**, you see:

**Columns:**
- **Page Name**: Click to open form view
- **State**: Draft / Generated / Published
- **Prompts**: Number of AI prompts sent
- **Has Content**: Whether page has HTML/CSS/JS
- **Created By**: User who created the page
- **Last Updated**: Most recent modification time

**Filters:**
- **Draft**: Pages without generated content
- **Generated**: Pages with AI-generated content
- **Published**: Pages marked as published
- **Has Content** / **No Content**
- **Archived**: Inactive pages

**Actions:**
- **Create**: Make a new page
- **Open**: View/edit page details
- **Delete**: Remove page permanently

### Page Form View

The standard form view shows:

**Header:**
- **Open Builder**: Launch the AI builder interface
- **Set to Draft**: Change state to draft
- **Mark as Generated**: Change state to generated
- **Publish**: Change state to published
- **State bar**: Visual state indicator

**Main Fields:**
- **Page Name**: Required
- **Description**: Optional
- **Active**: Archive toggle
- **Has Content**: Computed field
- **Created By** / **Last Updated**: Metadata

**Tabs:**
- **Generated Content**: View HTML, CSS, JS in code editors
- **AI History**: View raw JSON prompt history

**Chatter:**
- Log notes
- Track changes
- Send messages

### Page States

**Draft** (Blue):
- Initial state for new pages
- No generated content yet
- Can be edited freely

**Generated** (Green):
- Has AI-generated content
- Content has been saved
- Ready for review

**Published** (Purple):
- Marked as final/published
- (Future: Will publish to Website module)

## Tips & Best Practices

### Writing Good Prompts

✅ **Do:**
- Be specific about what you want
- Mention layout, sections, and features
- Describe the style (modern, minimal, bold, etc.)
- Include color preferences if you have them

❌ **Don't:**
- Be too vague ("make a website")
- Ask for multiple unrelated things at once
- Expect perfect results on first try

### Iterative Refinement

The AI works best with iteration:

1. **Start broad**: "Create a landing page"
2. **Review result**: Check the preview
3. **Refine specifics**: "Make the hero taller"
4. **Add features**: "Add a testimonials section"
5. **Polish**: "Adjust colors to match brand"

### Organizing Pages

**Naming convention:**
- Use descriptive names: "Homepage v2", "Product Launch Page"
- Include version numbers for iterations
- Add dates for time-sensitive pages

**Using descriptions:**
- Note the page purpose
- List key features
- Add client/project name

**States:**
- Keep drafts as "Draft" until content is good
- Mark as "Generated" when ready for review
- Use "Published" for final versions

### Performance

**For best performance:**
- Don't keep too many pages open at once
- Save regularly to avoid losing work
- Clear old/unused pages periodically
- Archive instead of delete for history

## Advanced Features

### Prompt History

The AI tracks all your prompts and responses:
- **View in chat**: Scroll up to see past messages
- **View in form**: AI History tab shows raw JSON
- **Clear history**: Click trash icon in chat header

**Use cases:**
- Review what prompts worked well
- Understand how the page evolved
- Copy prompts for similar pages

### Exporting Content

**To use generated content elsewhere:**

1. Switch to HTML/CSS/JS tabs
2. Click **Copy** to copy code
3. Or click **Download** to save as file
4. Paste/upload to your target system

**File names:**
- HTML: `page.html`
- CSS: `page.css`
- JavaScript: `page.js`

### Archiving Pages

Instead of deleting, archive old pages:

1. Open the page form view
2. Toggle **Active** to off
3. The page is hidden from default list view
4. Use "Archived" filter to find it later

## Keyboard Shortcuts

**In Chat:**
- `Enter`: Send prompt
- `Shift+Enter`: New line in prompt

**In Builder:**
- `Ctrl+S` / `Cmd+S`: Save (if browser allows)
- `Esc`: Focus chat input

**In Browser:**
- `Ctrl+F5` / `Cmd+Shift+R`: Hard refresh
- `F12`: Open developer tools

## Troubleshooting

### Preview Not Updating

1. Click the **Refresh** button
2. Switch to another tab and back
3. Check browser console for errors

### Can't Send Prompts

1. Make sure input field has text
2. Wait for previous prompt to finish
3. Check that AI service is responding

### Content Not Saving

1. Check for error notifications
2. Verify you have write permissions
3. Check Odoo logs for database errors

### Builder Interface Glitches

1. Refresh the browser page
2. Clear browser cache
3. Try a different browser
4. Check browser console for errors

## Next Steps

- Experiment with different prompt styles
- Try building various page types
- Explore the code to learn HTML/CSS/JS
- Share your best prompts with the team

---

**Happy Building! 🚀**

