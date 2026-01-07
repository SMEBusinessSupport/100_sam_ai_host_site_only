# SAM Chat UI Styles - Location-Based Design

**Created:** 2025-11-02
**Purpose:** 3 different chat UI styles based on where SAM bubble is clicked

---

## Problem Statement

SAM chat bubbles appear in different locations throughout the app. When clicked, they should open DIFFERENT chat interfaces depending on context:

**Example Locations:**
1. **Canvas** - User working on workflow → Full sidebar chat (current `sam_workflow_chat.js`)
2. **Quick Help** - User needs quick answer → Compact popup chat
3. **Settings** - User configuring system → Modal dialog chat with settings context

---

## Proposed 3 Chat UI Styles

### Style 1: **Full Sidebar** (Existing - Workflow Builder)

**Use Case:** Canvas, workflow editing, complex interactions
**Current Implementation:** `sam_workflow_chat.js`
**Size:** 30% of screen width (minimum 400px)
**Position:** Fixed right side, full height
**Features:**
- Conversation history
- Quick actions
- Theatre mode integration
- Persistent state when collapsed

**Locations:**
- `canvas` - Workflow canvas
- `workflows` - Workflow management

**Visual:**
```
┌─────────────────────────────┬──────────────┐
│                             │   SAM AI     │
│       Main Canvas           │  ┌─────────┐ │
│                             │  │ Message │ │
│                             │  │ Message │ │
│                             │  │ Message │ │
│                             │  └─────────┘ │
│                             │  [Input Box] │
└─────────────────────────────┴──────────────┘
```

---

### Style 2: **Compact Popup** (NEW - Quick Help)

**Use Case:** Quick questions, tooltips, contextual help
**Size:** 400px × 500px
**Position:** Floating near click location
**Features:**
- Single question/answer
- No history (ephemeral)
- Auto-close after answer
- Lightweight

**Locations:**
- `connector` - Node selection help
- `toolbar` - Feature explanations
- `help-icon` - General help

**Visual:**
```
┌─────────────────────┐
│ SAM AI - Quick Help │
├─────────────────────┤
│                     │
│ You: What does...?  │
│                     │
│ SAM: This feature   │
│ allows you to...    │
│                     │
├─────────────────────┤
│ [Ask question]      │
└─────────────────────┘
```

---

### Style 3: **Modal Dialog** (NEW - Deep Dive / Settings)

**Use Case:** Complex configuration, tutorials, guided workflows
**Size:** 600px × 700px (centered)
**Position:** Center of screen with backdrop
**Features:**
- Multi-step dialogs
- Form integration
- Rich media support
- Action buttons (Save, Cancel, Next)

**Locations:**
- `settings` - Configuration help
- `tutorial` - Guided onboarding
- `wizard` - Multi-step processes

**Visual:**
```
     ┌─────────────────────────────────┐
     │ SAM AI - Workflow Configuration │
     ├─────────────────────────────────┤
     │                                 │
     │  Step 1 of 3                    │
     │  ┌───────────────────────────┐  │
     │  │ Configuration options...  │  │
     │  └───────────────────────────┘  │
     │                                 │
     │  ┌─────────────────┐            │
     │  │ Chat messages   │            │
     │  └─────────────────┘            │
     │                                 │
     ├─────────────────────────────────┤
     │ [Cancel] [Back] [Next] [Finish] │
     └─────────────────────────────────┘
```

---

## Implementation Strategy

### 1. Location-to-Style Mapping

```javascript
const CHAT_STYLE_MAP = {
    // Full Sidebar (Existing)
    'canvas': 'sidebar',
    'workflows': 'sidebar',

    // Compact Popup (NEW)
    'connectors': 'popup',
    'toolbar': 'popup',
    'help': 'popup',
    'node-config': 'popup',

    // Modal Dialog (NEW)
    'settings': 'modal',
    'tutorial': 'modal',
    'wizard': 'modal',
    'onboarding': 'modal'
};
```

### 2. Updated SAMChatBubble Click Handler

```javascript
SAMChatBubble.create({
    location: 'canvas',
    onClick: (data) => {
        // Get appropriate UI style for location
        const style = SAMChatManager.getStyleForLocation(data.location);

        // Open chat with correct UI
        SAMChatManager.open(style, {
            location: data.location,
            context: data.context,
            systemPrompt: SAMChatBubble.getLocationPrompt(data.location)
        });
    }
});
```

### 3. SAMChatManager (NEW Component)

Central manager that routes to appropriate chat UI:

```javascript
class SAMChatManager {
    static open(style, options) {
        switch(style) {
            case 'sidebar':
                return this.openSidebar(options);  // Use existing sam_workflow_chat.js
            case 'popup':
                return this.openPopup(options);    // NEW: Compact popup
            case 'modal':
                return this.openModal(options);    // NEW: Modal dialog
            default:
                return this.openSidebar(options);  // Default to sidebar
        }
    }
}
```

---

## Migration Path

### Phase 1: Preserve Existing (NO CHANGES)
- Keep `sam_workflow_chat.js` as-is (Sidebar style)
- SAM bubbles in canvas continue to work exactly as before
- ZERO breaking changes

### Phase 2: Add Compact Popup
- Create `sam_chat_popup.js` (new file)
- Add mapping for toolbar/connectors locations
- Test in isolation

### Phase 3: Add Modal Dialog
- Create `sam_chat_modal.js` (new file)
- Add mapping for settings/tutorial locations
- Test guided workflows

### Phase 4: Centralize with Manager
- Create `sam_chat_manager.js`
- Route all SAM bubble clicks through manager
- Manager decides which UI to open

---

## CSS Namespace Safety

All 3 styles use DIFFERENT class namespaces:

| Style | Class Prefix | Example |
|-------|--------------|---------|
| Sidebar | `.sam-chat-sidebar-*` | `.sam-chat-sidebar-header` |
| Popup | `.sam-chat-popup-*` | `.sam-chat-popup-container` |
| Modal | `.sam-chat-modal-*` | `.sam-chat-modal-backdrop` |

**NO CONFLICTS** - Each style is isolated!

---

## Recommended Approach

**Start with what you have:**
1. Your existing sidebar chat works perfectly - don't touch it
2. SAM bubbles on canvas open the sidebar (current behavior)
3. Add new styles ONLY when needed for other locations

**When you need popup/modal:**
1. Tell me the specific location (e.g., "I need quick help in connector overlay")
2. I'll build the appropriate UI style
3. We wire it up through SAMChatManager

---

## Question for You

What are your **3 specific locations and desired chat styles**?

Example answer:
1. **Canvas** → Sidebar (already have this)
2. **Connector overlay** → Popup (need compact help)
3. **Settings page** → Modal (need guided configuration)

Tell me your 3 scenarios and I'll build the exact system you need!
