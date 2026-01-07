# SAM Chat Bubble Component - Usage Guide

**Created:** 2025-11-02
**Purpose:** Site-wide consistent SAM AI branding with context awareness

## Overview

The SAM Chat Bubble component provides a centralized, consistent way to display SAM AI chat icons throughout the application. Instead of hardcoding file paths to `Sam.png` everywhere, use this class-based system that supports:

- **One icon path** - Change once, updates everywhere
- **Context awareness** - Bubbles know where they are in the app
- **Location prompts** - AI training data based on current page
- **Consistent styling** - Purple gradient, shadows, animations
- **Size variants** - Small (32px), Medium (48px), Large (64px)

---

## Quick Start

### 1. Basic Usage

```javascript
// Create a simple SAM chat bubble
const bubble = SAMChatBubble.create({
    size: 'md',
    onClick: () => {
        console.log('SAM bubble clicked!');
    }
});

// Add it to the DOM
document.body.appendChild(bubble);
```

### 2. Context-Aware Bubble (Recommended)

```javascript
// Create bubble with location and context awareness
const bubble = SAMChatBubble.create({
    size: 'md',
    location: 'canvas',                    // Current page
    context: {                              // Additional context
        workflow_id: 455,
        workflow_name: 'Customer Onboarding'
    },
    onClick: (data) => {
        console.log('Location:', data.location);  // 'canvas'
        console.log('Context:', data.context);    // {workflow_id: 455, ...}

        // Get AI training prompt for this location
        const prompt = SAMChatBubble.getLocationPrompt(data.location);
        console.log('AI Prompt:', prompt);
    }
});

document.querySelector('#toolbar').appendChild(bubble);
```

### 3. Replace Existing Icons (Use for chevrons, arrows, etc.)

```javascript
// Replace a hardcoded icon/chevron with SAM bubble
SAMChatBubble.replace('#someChevronButton', {
    size: 'sm',
    location: 'sidebar',
    onClick: () => {
        // Toggle sidebar, etc.
    }
});
```

---

## API Reference

### `SAMChatBubble.create(options)`

Creates a new SAM chat bubble element.

**Options:**

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `size` | string | `'md'` | Size variant: `'sm'` (32px), `'md'` (48px), `'lg'` (64px) |
| `location` | string | `null` | Current location in app (e.g., `'canvas'`, `'workflows'`, `'settings'`) |
| `context` | object | `null` | Additional context data for AI training |
| `pulse` | boolean | `false` | Enable pulsing animation |
| `fixedRight` | boolean | `false` | Fix to right side of screen |
| `onClick` | function | `null` | Click handler `(data) => {}` |
| `badge` | string | `null` | Badge text (e.g., `'3'` for notification count) |

**Returns:** `HTMLElement` - SAM chat bubble element

---

### `SAMChatBubble.createIn(container, options)`

Creates bubble and appends to container.

```javascript
SAMChatBubble.createIn('#toolbar', {
    size: 'md',
    location: 'canvas'
});
```

---

### `SAMChatBubble.replace(target, options)`

Replaces an existing element with SAM bubble.

```javascript
// Before: <i class="fa fa-chevron-left" id="backBtn"></i>
// After:  SAM chat bubble

SAMChatBubble.replace('#backBtn', {
    size: 'sm',
    location: 'overlay',
    onClick: () => { closeOverlay(); }
});
```

---

### `SAMChatBubble.getLocationPrompt(location)`

Returns AI training prompt for a specific location.

```javascript
const prompt = SAMChatBubble.getLocationPrompt('canvas');
// Returns: "You are assisting with workflow canvas operations..."
```

**Available Locations:**

- `canvas` - Workflow canvas operations
- `workflows` - Workflow management
- `connectors` - Connector selection
- `settings` - System settings
- `content` - Content node management
- `agents` - AI agent configuration
- `default` - Generic SAM AI assistant

---

### `SAMChatBubble.updateBadge(bubble, badge)`

Update or remove badge on existing bubble.

```javascript
const bubble = document.querySelector('.sam-chat-bubble');

// Add badge
SAMChatBubble.updateBadge(bubble, '5');

// Remove badge
SAMChatBubble.updateBadge(bubble, null);
```

---

### `SAMChatBubble.setPulse(bubble, enable)`

Enable/disable pulse animation.

```javascript
const bubble = document.querySelector('.sam-chat-bubble');

// Start pulsing
SAMChatBubble.setPulse(bubble, true);

// Stop pulsing
SAMChatBubble.setPulse(bubble, false);
```

---

## Real-World Examples

### Example 1: Replace Sidebar Toggle Arrow

**Before:**
```html
<button id="toggleSidebar" class="btn-toggle">
    <i class="fa fa-chevron-left"></i>
</button>
```

**After:**
```javascript
// Remove old button, add SAM bubble
document.querySelector('#toggleSidebar').remove();

SAMChatBubble.createIn('#sidebar-container', {
    size: 'sm',
    location: 'sidebar',
    fixedRight: true,
    onClick: () => {
        toggleSidebar();
    }
});
```

---

### Example 2: Fixed Right Chat Button

```javascript
// Create floating SAM chat button (always visible)
const chatBubble = SAMChatBubble.create({
    size: 'lg',
    location: 'global',
    fixedRight: true,
    pulse: true,               // Pulse to get attention
    badge: '3',                // Show unread count
    onClick: (data) => {
        openChatPanel();
        SAMChatBubble.setPulse(chatBubble, false);  // Stop pulsing
        SAMChatBubble.updateBadge(chatBubble, null); // Clear badge
    }
});

document.body.appendChild(chatBubble);
```

---

### Example 3: Context-Aware Workflow Help

```javascript
// Add SAM help button to workflow canvas
const workflowId = document.querySelector('#workflowCanvas').dataset.workflowId;

SAMChatBubble.createIn('#canvas-toolbar', {
    size: 'md',
    location: 'canvas',
    context: {
        workflow_id: workflowId,
        node_count: nodeManager.getNodeCount(),
        connected_nodes: nodeManager.getConnectedCount()
    },
    onClick: (data) => {
        // SAM knows: location='canvas', context has workflow stats
        const prompt = SAMChatBubble.getLocationPrompt(data.location);

        openAIChatWithContext({
            systemPrompt: prompt,
            userContext: data.context
        });
    }
});
```

---

### Example 4: Dynamic Badge Updates

```javascript
// Create bubble with notification badge
const bubble = SAMChatBubble.create({
    size: 'md',
    badge: '0'
});

document.querySelector('#toolbar').appendChild(bubble);

// Update badge when new messages arrive
window.addEventListener('newChatMessage', (event) => {
    const unreadCount = event.detail.unreadCount;
    SAMChatBubble.updateBadge(bubble, unreadCount > 0 ? String(unreadCount) : null);

    // Pulse if new messages
    if (unreadCount > 0) {
        SAMChatBubble.setPulse(bubble, true);
    }
});
```

---

## CSS Classes Available

All styling is centralized in `sam_design_tokens.css`:

| Class | Description |
|-------|-------------|
| `.sam-chat-bubble` | Base SAM bubble (48px) |
| `.sam-chat-bubble-sm` | Small variant (32px) |
| `.sam-chat-bubble-lg` | Large variant (64px) |
| `.sam-chat-bubble-pulse` | Pulsing animation |
| `.sam-chat-bubble-fixed-right` | Fixed to right side of screen |
| `.sam-badge` | Notification badge overlay |

---

## Data Attributes for Context

SAM bubbles automatically set these data attributes for tracking and AI training:

```html
<div class="sam-chat-bubble"
     data-location="canvas"
     data-context='{"workflow_id":455,"node_count":8}'
     title="SAM AI Assistant - canvas">
</div>
```

These attributes enable:
- **Analytics** - Track where users click SAM bubbles
- **AI Training** - Location-specific system prompts
- **Context Passing** - Pass workflow/page state to AI
- **Debugging** - See context in dev tools

---

## Migration Guide

### Replacing Hardcoded Icons

**Old Way (Hardcoded):**
```html
<img src="/ai_sam/static/description/Sam.png" width="48" />
```

**New Way (Class-based):**
```javascript
const bubble = SAMChatBubble.create({ size: 'md' });
```

**Benefits:**
- Change icon path once in CSS → all bubbles update
- Automatic hover effects, shadows, animations
- Context awareness built-in
- Consistent sizing across app

---

### Replacing Chevrons/Arrows

**Old Way:**
```html
<button onclick="goBack()">
    <i class="fa fa-chevron-left"></i>
</button>
```

**New Way:**
```javascript
SAMChatBubble.replace('#backButton', {
    size: 'sm',
    location: 'overlay',
    onClick: () => { goBack(); }
});
```

---

## Best Practices

1. **Always set location** - Enables AI training and analytics
2. **Use context for dynamic data** - Workflow IDs, user state, etc.
3. **Prefer `replace()` for existing icons** - Cleaner than manual DOM manipulation
4. **Use badges sparingly** - Only for important notifications
5. **Pulse for attention only** - Don't overuse pulsing animation

---

## Configuration

To change the SAM icon globally, edit `sam_design_tokens.css`:

```css
:root {
    --sam-icon-path: url('/ai_sam/static/description/Sam.png');  /* Change here */
    --sam-bubble-bg: linear-gradient(135deg, #7c3aed 0%, #a855f7 100%);
    --sam-bubble-size: 48px;
}
```

One change updates ALL SAM bubbles across the entire application!

---

## Browser Support

- Chrome/Edge: ✅ Full support
- Firefox: ✅ Full support
- Safari: ✅ Full support
- IE11: ❌ Not supported (CSS variables required)

---

## Troubleshooting

**Bubble not appearing:**
```javascript
// Make sure sam_chat_bubble.js is loaded
if (typeof SAMChatBubble === 'undefined') {
    console.error('SAMChatBubble not loaded!');
}
```

**Icon not showing:**
- Check `--sam-icon-path` in sam_design_tokens.css
- Verify Sam.png exists at `/ai_sam/static/description/Sam.png`
- Check browser console for 404 errors

**Bubble too small/large:**
```javascript
// Use size variants
SAMChatBubble.create({ size: 'sm' });  // 32px
SAMChatBubble.create({ size: 'md' });  // 48px
SAMChatBubble.create({ size: 'lg' });  // 64px
```

---

## Questions?

This component is designed to replace ALL hardcoded SAM icons and create a unified, context-aware chat bubble system across the entire SAM AI platform.

**Key Principle:** One class to rule them all. Never hardcode Sam.png paths again!
