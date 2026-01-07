# SAM AI Page Builder - Quick Reference Card

## 🚀 Installation (3 Steps)

```bash
# 1. Restart Odoo
docker-compose restart odoo

# 2. In Odoo: Apps → Update Apps List

# 3. Search "SAM AI Page Builder" → Install
```

## 🎯 Access

**Menu Path**: `SAM AI Page Builder → AI Pages`  
**URL**: `http://localhost:8069`  
**Login**: `admin@samai.com` / `admin123`

## 💬 Example Prompts

| Type | Prompt |
|------|--------|
| **Landing** | "Build a landing page with hero, features, and CTA" |
| **Product** | "Create a product showcase with image gallery" |
| **Pricing** | "Design a pricing page with 3 tiers" |
| **Contact** | "Make a contact page with form and map" |
| **Refine** | "Add testimonials section" |
| **Style** | "Change colors to blue theme" |

## 🎨 Interface Layout

```
┌─────────────────────────────────────────────────────────┐
│  ← Back    Page Name                    AI Page Builder │ ← Top Bar
├──────────────────┬──────────────────────────────────────┤
│                  │  Preview │ HTML │ CSS │ JS           │
│   AI Chat        ├──────────────────────────────────────┤
│   Assistant      │                                      │
│                  │         Preview / Code View          │
│  ┌────────────┐  │                                      │
│  │  Message   │  │                                      │
│  │  History   │  │                                      │
│  │            │  │                                      │
│  │            │  │          [Zoom] [Refresh] [Save]     │
│  └────────────┘  │                                      │
│                  │                                      │
│  [Input prompt]  │                                      │
│  [Send]          │                                      │
└──────────────────┴──────────────────────────────────────┘
   Left Panel (40%)        Right Panel (60%)
```

## ⌨️ Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `Enter` | Send prompt |
| `Shift+Enter` | New line in prompt |
| `Ctrl+F5` | Hard refresh browser |
| `F12` | Open developer tools |

## 🎛️ Controls

### Chat Panel (Left)
- **Send** (↑): Submit prompt
- **Clear** (🗑️): Delete history
- **Examples**: Click to use

### Builder Panel (Right)
- **Tabs**: Switch view mode
- **Zoom**: +/- buttons (Preview only)
- **Refresh**: Reload preview
- **Save**: Save to database
- **Copy**: Copy code to clipboard
- **Download**: Save as file

## 📊 Page States

| State | Color | Meaning |
|-------|-------|---------|
| **Draft** | Blue | New page, no content |
| **Generated** | Green | Has AI content |
| **Published** | Purple | Final version |

## 🔧 Common Tasks

### Create Page
1. `SAM AI Page Builder → AI Pages`
2. Click `Create`
3. Enter name → `Save`
4. Click `Open Builder`

### Generate Content
1. Type prompt in chat
2. Press `Enter` or click send
3. Wait for AI response (~1.5s)
4. Review in preview panel

### Refine Content
1. Send follow-up prompt
2. AI builds on previous result
3. Preview updates automatically

### Save Content
1. Click `Save` button (top-right)
2. Wait for success notification
3. State changes to "Generated"

### Export Code
1. Switch to HTML/CSS/JS tab
2. Click `Copy` or `Download`
3. Use in external projects

## 🐛 Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| Module not in Apps | Update Apps List |
| Menu not showing | Refresh browser (Ctrl+F5) |
| Builder not loading | Check browser console (F12) |
| AI not responding | Wait 1.5s, check console |
| Preview not updating | Click Refresh button |
| Can't save | Check Odoo logs |

## 📁 File Locations

```
sam_ai_page_builder/
├── models/sam_ai_page.py          ← Data model
├── views/sam_ai_page_views.xml    ← Standard views
├── static/src/
│   ├── components/                ← OWL components
│   ├── services/ai_stub_service.js ← AI service
│   └── css/page_builder.css       ← Styling
└── security/ir.model.access.csv   ← Permissions
```

## 🎨 Customization Quick Wins

### Change Colors
Edit `static/src/css/page_builder.css`:
```css
:root {
    --sam-primary: #667eea;      /* Your color */
    --sam-secondary: #764ba2;    /* Your color */
}
```

### Add Example Prompts
Edit `static/src/components/chat_panel/chat_panel.js`:
```javascript
get examplePrompts() {
    return [
        "Your custom prompt 1",
        "Your custom prompt 2",
    ];
}
```

### Change Default Layout
Edit `static/src/views/ai_page_builder_action.xml`:
```xml
<SplitLayout defaultLeftWidth="50"/>  <!-- 50% instead of 40% -->
```

## 🔗 Documentation Links

- **Full Docs**: [README.md](README.md)
- **Installation**: [INSTALLATION.md](INSTALLATION.md)
- **Usage Guide**: [USAGE.md](USAGE.md)
- **Summary**: [SAM_AI_PAGE_BUILDER_SUMMARY.md](../SAM_AI_PAGE_BUILDER_SUMMARY.md)

## 🆘 Support Checklist

Before asking for help:
- [ ] Checked browser console (F12)
- [ ] Checked Odoo logs (`docker-compose logs -f odoo`)
- [ ] Tried refreshing browser (Ctrl+F5)
- [ ] Verified module is installed
- [ ] Read relevant documentation

## 📞 Get Help

1. Check documentation files
2. Review inline code comments
3. Check Odoo logs for errors
4. Contact SAM AI development team

---

## 🎯 Remember

✅ **Prompts**: Be specific, iterate, refine  
✅ **Save**: Content is NOT auto-saved  
✅ **Export**: Copy or download code  
✅ **AI**: Currently stubbed (mock responses)  
✅ **Docs**: Three comprehensive guides available  

---

**Quick Reference v1.0 | SAM AI Page Builder for Odoo 18**

