# SAM AI Page Builder - Architecture Documentation

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         Odoo 18 Backend                         │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                    sam.ai.page Model                       │  │
│  │  • name, description                                       │  │
│  │  • page_html, page_css, page_js                           │  │
│  │  • ai_prompt_history (JSON)                               │  │
│  │  • state (draft/generated/published)                      │  │
│  │  • Methods: add_prompt_to_history(), get_prompt_history() │  │
│  └───────────────────────────────────────────────────────────┘  │
│                              ↕                                   │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                    XML Views & Menus                       │  │
│  │  • Tree View (list of pages)                              │  │
│  │  • Form View (page details)                               │  │
│  │  • Search View (filters)                                  │  │
│  │  • Client Action (builder interface)                      │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                               ↕
┌─────────────────────────────────────────────────────────────────┐
│                      Odoo Web Client (OWL 2)                    │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │              AIPageBuilderAction (Main)                    │  │
│  │  • Loads page data                                         │  │
│  │  • Orchestrates components                                 │  │
│  │  • Handles save/close                                      │  │
│  └───────────────────────────────────────────────────────────┘  │
│                               ↓                                  │
│  ┌──────────────────────┐  ┌──────────────────────────────────┐ │
│  │   SplitLayout        │  │   Services                       │ │
│  │  • Resizable panels  │  │  • aiStubService                 │ │
│  │  • Drag handling     │  │    - generatePage()              │ │
│  └──────────────────────┘  │    - refinePage()                │ │
│           ↓                 └──────────────────────────────────┘ │
│  ┌──────────────────────┐  ┌──────────────────────────────────┐ │
│  │   ChatPanel          │  │   PageBuilderPanel               │ │
│  │  • Message history   │  │  • Preview iframe                │ │
│  │  • Prompt input      │  │  • Code tabs (HTML/CSS/JS)       │ │
│  │  • AI interaction    │  │  • Zoom, save, export            │ │
│  └──────────────────────┘  └──────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

## Component Architecture

### 1. Backend Layer (Python)

```python
# models/sam_ai_page.py

class SamAiPage(models.Model):
    _name = 'sam.ai.page'
    
    # Data Fields
    name = fields.Char()
    page_html = fields.Text()
    page_css = fields.Text()
    page_js = fields.Text()
    ai_prompt_history = fields.Text()  # JSON
    state = fields.Selection()
    
    # Computed Fields
    prompt_count = fields.Integer(compute='_compute_prompt_count')
    has_content = fields.Boolean(compute='_compute_has_content')
    
    # Methods
    def add_prompt_to_history(prompt, response)
    def get_prompt_history()
    def action_generate()
```

**Responsibilities:**
- Store page data
- Manage AI prompt history
- Handle state transitions
- Provide computed fields
- Enforce data validation

### 2. View Layer (XML)

```xml
<!-- views/sam_ai_page_views.xml -->

<tree>        <!-- List of pages -->
<form>        <!-- Page details -->
<search>      <!-- Filters and search -->

<!-- views/sam_ai_page_menus.xml -->

<menuitem>    <!-- Top-level menu -->
<menuitem>    <!-- AI Pages submenu -->
```

**Responsibilities:**
- Define standard Odoo views
- Create menu structure
- Configure filters and actions
- Register client action

### 3. Frontend Layer (OWL Components)

#### Main Action

```javascript
// views/ai_page_builder_action.js

class AIPageBuilderAction extends Component {
    setup() {
        // Load page data
        // Initialize state
        // Setup components
    }
    
    onGenerate(content) {
        // Handle AI generation
        // Update preview
    }
    
    onSave(content) {
        // Save to database
    }
}
```

**Responsibilities:**
- Entry point for builder interface
- Load/save page data
- Coordinate components
- Handle navigation

#### Split Layout Component

```javascript
// components/split_layout/split_layout.js

class SplitLayout extends Component {
    setup() {
        // Initialize resizer
        // Handle drag events
    }
    
    _setupResizer() {
        // Mouse down/move/up handlers
        // Calculate panel widths
    }
}
```

**Responsibilities:**
- Render left and right panels
- Handle resizing
- Maintain panel proportions
- Enforce min/max widths

#### Chat Panel Component

```javascript
// components/chat_panel/chat_panel.js

class ChatPanel extends Component {
    setup() {
        // Initialize AI service
        // Load message history
    }
    
    async onSubmitPrompt(ev) {
        // Send to AI service
        // Update message history
        // Notify parent
    }
}
```

**Responsibilities:**
- Display message history
- Handle prompt input
- Call AI service
- Show loading states
- Manage conversation flow

#### Page Builder Panel Component

```javascript
// components/page_builder_panel/page_builder_panel.js

class PageBuilderPanel extends Component {
    setup() {
        // Initialize view mode
        // Setup iframe
    }
    
    updateContent(content) {
        // Update preview
        // Refresh iframe
    }
    
    async onSave() {
        // Save to database
    }
}
```

**Responsibilities:**
- Render preview iframe
- Display code tabs
- Handle zoom controls
- Save content
- Export functionality

### 4. Service Layer

```javascript
// services/ai_stub_service.js

class AIStubService {
    async generatePage(prompt) {
        // Simulate AI call
        // Return mock HTML/CSS/JS
    }
    
    async refinePage(prompt, currentContent) {
        // Simulate refinement
        // Return updated content
    }
}
```

**Responsibilities:**
- Provide AI interface
- Return mock responses (stub)
- Simulate network delay
- Easy to swap for real AI

## Data Flow

### Page Creation Flow

```
User clicks "Create"
    ↓
Odoo creates sam.ai.page record
    ↓
User clicks "Open Builder"
    ↓
AIPageBuilderAction loads
    ↓
Fetches page data from backend
    ↓
Renders SplitLayout with ChatPanel + PageBuilderPanel
    ↓
User ready to interact
```

### AI Generation Flow

```
User types prompt in ChatPanel
    ↓
User presses Enter
    ↓
ChatPanel.onSubmitPrompt()
    ↓
Calls aiStubService.generatePage(prompt)
    ↓
Service returns { html, css, js }
    ↓
ChatPanel adds to message history
    ↓
ChatPanel calls props.onGenerate(content)
    ↓
AIPageBuilderAction.onGenerate()
    ↓
Updates state.content
    ↓
Calls PageBuilderPanel.updateContent()
    ↓
PageBuilderPanel renders in iframe
    ↓
User sees preview
```

### Save Flow

```
User clicks "Save" in PageBuilderPanel
    ↓
PageBuilderPanel.onSave()
    ↓
Calls orm.write() with content
    ↓
Backend updates sam.ai.page record
    ↓
Sets state = 'generated'
    ↓
Returns success
    ↓
Shows notification
    ↓
Updates lastSaved timestamp
```

## State Management

### Component State

Each component manages its own state using `useState`:

**ChatPanel:**
```javascript
state = {
    messages: [],           // Chat history
    currentPrompt: "",      // Input value
    isGenerating: false,    // Loading state
    error: null            // Error message
}
```

**PageBuilderPanel:**
```javascript
state = {
    viewMode: "preview",    // preview/html/css/js
    content: {},           // HTML/CSS/JS
    isSaving: false,       // Save in progress
    lastSaved: null,       // Timestamp
    scale: 100            // Preview zoom
}
```

**SplitLayout:**
```javascript
state = {
    leftWidth: 40,         // Percentage
    isDragging: false      // Resize in progress
}
```

### Global State

Managed by `AIPageBuilderAction`:

```javascript
state = {
    pageId: null,          // Current page ID
    pageName: "",          // Page name
    content: {},           // Current HTML/CSS/JS
    promptHistory: [],     // All prompts/responses
    isLoading: true       // Initial load
}
```

## Communication Patterns

### Parent → Child (Props)

```javascript
// Parent passes data and callbacks
<ChatPanel 
    pageId={state.pageId}
    onGenerate={this.onGenerate.bind(this)}
    promptHistory={state.promptHistory}
/>
```

### Child → Parent (Callbacks)

```javascript
// Child calls parent method
if (this.props.onGenerate) {
    this.props.onGenerate({ html, css, js });
}
```

### Component → Service

```javascript
// Component uses service
this.aiService = useService("aiStubService");
const result = await this.aiService.generatePage(prompt);
```

### Component → Backend

```javascript
// Component calls ORM
this.orm = useService("orm");
await this.orm.write("sam.ai.page", [id], { page_html: html });
```

## Styling Architecture

### CSS Variables (Theme)

```css
:root {
    /* Colors */
    --sam-primary: #667eea;
    --sam-secondary: #764ba2;
    
    /* Backgrounds */
    --sam-bg-dark: #1e1e1e;
    --sam-bg-medium: #252526;
    
    /* Text */
    --sam-text-primary: #cccccc;
    
    /* Effects */
    --sam-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
    --sam-transition: all 0.2s ease;
}
```

### Component Styles

Each component has its own CSS namespace:

- `.sam-split-*` - Split layout
- `.sam-chat-*` - Chat panel
- `.sam-builder-*` - Builder panel
- `.sam-ai-page-builder` - Main container

### Responsive Design

```css
@media (max-width: 768px) {
    .sam-split-layout {
        flex-direction: column;
    }
}
```

## Security Model

### Access Control

```csv
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_sam_ai_page_user,sam.ai.page.user,model_sam_ai_page,base.group_user,1,1,1,1
access_sam_ai_page_public,sam.ai.page.public,model_sam_ai_page,base.group_public,1,0,0,0
```

**Rules:**
- Internal users: Full access
- Public users: Read-only

### Data Validation

```python
@api.model
def create(self, vals):
    # Ensure valid JSON
    if 'ai_prompt_history' not in vals:
        vals['ai_prompt_history'] = '[]'
    return super().create(vals)

def write(self, vals):
    # Validate JSON
    if 'ai_prompt_history' in vals:
        try:
            json.loads(vals['ai_prompt_history'])
        except:
            raise ValidationError('Invalid JSON')
    return super().write(vals)
```

## Extension Points

### Adding New Features

**1. New Model Fields:**
```python
# models/sam_ai_page.py
custom_field = fields.Char()
```

**2. New View Modes:**
```javascript
// page_builder_panel.js
setViewMode('custom') {
    this.state.viewMode = 'custom';
}
```

**3. New AI Capabilities:**
```javascript
// ai_stub_service.js
async customAIMethod(params) {
    // Your logic
}
```

**4. New Components:**
```javascript
// components/custom/custom.js
export class CustomComponent extends Component {
    static template = "sam_ai_page_builder.Custom";
}
```

## Performance Considerations

### Optimizations

1. **Lazy Loading**: Components load only when needed
2. **Debouncing**: Input events are debounced
3. **Virtual Scrolling**: Long message lists (future)
4. **Code Splitting**: Assets loaded on demand
5. **Caching**: Prompt history cached in memory

### Best Practices

- Use `useRef` for DOM access (not `querySelector`)
- Use `useState` for reactive data
- Cleanup in `onWillUnmount`
- Avoid unnecessary re-renders
- Use CSS transforms for animations

## Testing Strategy

### Manual Testing

1. **Installation**: Module installs cleanly
2. **Navigation**: Menu and views work
3. **Creation**: Can create pages
4. **Builder**: Interface opens correctly
5. **AI**: Prompts return responses
6. **Preview**: Content renders
7. **Save**: Data persists
8. **Export**: Copy/download works

### Future: Automated Testing

```python
# tests/test_sam_ai_page.py
class TestSamAiPage(TransactionCase):
    def test_create_page(self):
        page = self.env['sam.ai.page'].create({
            'name': 'Test Page'
        })
        self.assertTrue(page.id)
```

## Deployment

### Production Checklist

- [ ] Test in staging environment
- [ ] Verify all assets load
- [ ] Check browser compatibility
- [ ] Review access rights
- [ ] Backup database
- [ ] Update documentation
- [ ] Train users

### Monitoring

- Odoo logs: `docker-compose logs -f odoo`
- Browser console: F12 → Console
- Network tab: F12 → Network
- Database queries: Odoo debug mode

---

## Summary

The SAM AI Page Builder uses a **clean, layered architecture**:

1. **Backend** (Python): Data model and business logic
2. **Views** (XML): Standard Odoo interface
3. **Components** (OWL): Modern reactive UI
4. **Services** (JS): AI and business logic
5. **Styling** (CSS): Modern, themeable design

This architecture is:
- ✅ **Modular**: Easy to extend
- ✅ **Maintainable**: Clear separation of concerns
- ✅ **Scalable**: Ready for growth
- ✅ **Testable**: Components are isolated
- ✅ **Future-proof**: Easy to swap AI service

---

**Architecture v1.0 | SAM AI Page Builder for Odoo 18**

