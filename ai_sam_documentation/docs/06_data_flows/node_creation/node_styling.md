# Node Styling System Documentation

**Purpose:** Document how our node styling system detects node types and applies visual differentiation
**Date:** 2025-10-01
**Status:** Active Development

---

## Overview

Our node styling system uses a **two-layer approach**:

1. **Type Detection** - JavaScript analyzes n8n node type string to determine category
2. **CSS Application** - Category-specific styles are applied via CSS classes

---

## Type Detection System

### Location
`node_manager.js` - `getNodeClassFromN8nType(n8nType)` method (lines 727-781)

### Detection Logic

The method analyzes the n8n type string (e.g., `"n8n-nodes-base.webhook"`) and returns a category:

| Category | Detection Keywords | CSS Class | Border Color | Example n8n Types |
|----------|-------------------|-----------|--------------|-------------------|
| **trigger** | trigger, webhook, schedule, poll, cron | `.trigger` | Purple `#885577` | webhook, scheduleTrigger, cronTrigger |
| **ai-agent** | agent (not .tool) | `.ai-agent` | Teal `#1ABC9C` | n8n-nodes-langchain.agent |
| **ai-tool** | ends with .tool | `.ai-tool` | Cyan `#16A085` | calculator.tool, search.tool |
| **conditional** | if, switch, condition | `.conditional` | Orange `#E67E22` | if, switch |
| **code** | code, function, javascript, python | `.code` | Dark Green `#27AE60` | code, function |
| **transform** | set, edit, transform, merge, split | `.transform` | Green `#2ECC71` | set, merge, split |
| **action** | (default/fallback) | `.action` | Blue `#4A90E2` | gmail, slack, httpRequest |

### Code Example

```javascript
getNodeClassFromN8nType(n8nType) {
    const lowerType = n8nType.toLowerCase();

    // AI Agent detection (NOT tools)
    if (lowerType.includes('agent') && !lowerType.includes('tool')) {
        return 'ai-agent';
    }

    // AI Tool detection (nodes ending in .tool)
    if (lowerType.includes('.tool') || lowerType.endsWith('tool')) {
        return 'ai-tool';
    }

    // Trigger detection
    if (lowerType.includes('trigger') ||
        lowerType.includes('webhook') ||
        lowerType.includes('schedule') ||
        lowerType.includes('poll') ||
        lowerType.includes('cron')) {
        return 'trigger';
    }

    // Conditional detection
    if (lowerType.includes('if') ||
        lowerType.includes('switch') ||
        lowerType.includes('condition')) {
        return 'conditional';
    }

    // Code detection
    if (lowerType.includes('code') ||
        lowerType.includes('function') ||
        lowerType.includes('javascript') ||
        lowerType.includes('python')) {
        return 'code';
    }

    // Transform detection
    if (lowerType.includes('set') ||
        lowerType.includes('edit') ||
        lowerType.includes('transform') ||
        lowerType.includes('merge') ||
        lowerType.includes('split')) {
        return 'transform';
    }

    // Default to action
    return 'action';
}
```

---

## CSS Styling System

### Location
- **Current:** `node_manager.js` - `NODE_STYLES` constant (lines 40-380)
- **Future:** Separate CSS file at `static/src/n8n/n8n_styles/n8n_node_styles.css`

### CSS Selectors

All selectors use `#nodeCanvas` prefix for specificity:

```css
/* Base node styling */
#nodeCanvas .canvas-node {
    position: absolute;
    background: #ffffff;
    border: 1px solid #e0e0e0;
    border-left: 3px solid #999999;  /* Default - overridden by type */
    border-radius: 6px;
    padding: 0;
    min-width: 200px;
    max-width: 240px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.08);
}

/* Type-specific border colors */
#nodeCanvas .canvas-node.trigger {
    border-left-color: #885577 !important;  /* Purple */
}

#nodeCanvas .canvas-node.action {
    border-left-color: #4A90E2 !important;  /* Blue */
}

#nodeCanvas .canvas-node.transform {
    border-left-color: #2ECC71 !important;  /* Green */
}

#nodeCanvas .canvas-node.conditional {
    border-left-color: #E67E22 !important;  /* Orange */
}

#nodeCanvas .canvas-node.ai-agent {
    border-left-color: #1ABC9C !important;  /* Teal */
}

#nodeCanvas .canvas-node.ai-tool {
    border-left-color: #16A085 !important;  /* Cyan */
}

#nodeCanvas .canvas-node.code {
    border-left-color: #27AE60 !important;  /* Dark Green */
}
```

---

## Usage Flow

### When a node is added to canvas:

1. **User selects node** in overlay (e.g., "Webhook")
2. **Overlay generates n8n JSON** with type: `"n8n-nodes-base.webhook"`
3. **Bridge method called**: `addNodeFromN8nJSON(nodeData)`
4. **Type detection runs**: `getNodeClassFromN8nType("n8n-nodes-base.webhook")` → returns `"trigger"`
5. **Node element created** with class: `<div class="canvas-node trigger">`
6. **CSS applies**: Purple left border from `.canvas-node.trigger` rule
7. **Node renders** with visual differentiation

### HTML Output Example

```html
<div class="canvas-node trigger"
     data-node-id="node-abc123"
     data-node-type="trigger"
     data-n8n-type="n8n-nodes-base.webhook">
    <div class="node-header">
        <span class="node-icon">🌐</span>
        <span class="node-type-label">TRIGGER</span>
    </div>
    <div class="node-content">
        <div class="node-name">Webhook</div>
        <div class="node-description">Path: /webhook | Method: POST</div>
    </div>
</div>
```

---

## Known Issues & Improvements Needed

### 1. **Node Shapes** (TO DO)
- **Current:** All nodes have same rectangular shape with rounded corners
- **n8n Standard:**
  - Triggers have **curved left edge** (half-circle cutout)
  - Tools have **fully rounded shape** (circle/pill)
  - Actions have **standard rounded rectangle**

### 2. **Node Sizes** (TO DO)
- **Current:** Fixed `min-width: 200px, max-width: 240px`
- **Issue:** Nodes appear different physical sizes
- **Need:** Consistent sizing or dynamic sizing based on content

### 3. **Header Styling** (TO DO)
- **Current:** Simple gray background with uppercase text
- **n8n Standard:** May use different header treatments per type
- **Improvement:** Enhance header visual design

### 4. **Labels/Typography** (TO DO)
- Review font sizes, weights, colors
- Ensure consistency with n8n's typography system

### 5. **CSS File Separation** (TO DO)
- **Current:** CSS embedded in `NODE_STYLES` constant in node_manager.js
- **Better:** Extract to separate file `n8n_node_styles.css`
- **Benefits:** Easier editing, better caching, cleaner code

### 6. **Save Functionality** (BUG)
- **Issue:** Nodes not saving to database correctly
- **Status:** Under investigation

---

## CSS File Structure (Proposed)

### Recommended File Organization

```
static/src/n8n/n8n_styles/
├── n8n_node_styles.css          # Base node styling
├── n8n_node_types.css           # Type-specific styles (trigger, action, etc.)
├── n8n_node_shapes.css          # Shape variations (rounded, curved edges)
├── n8n_node_animations.css      # Hover, pulse, transitions
└── n8n_canvas_styles.css        # Canvas-specific styles
```

---

## Next Steps

### Phase 1: Visual Parity with n8n
- [ ] Implement curved left edge for trigger nodes
- [ ] Implement rounded shape for tool nodes
- [ ] Fix node sizing inconsistencies
- [ ] Extract CSS to separate file(s)

### Phase 2: Enhanced Styling
- [ ] Add node type icons (replace generic emoji)
- [ ] Implement proper hover/active states
- [ ] Add execution status indicators
- [ ] Implement connection line styling

### Phase 3: Polish
- [ ] Add smooth animations
- [ ] Implement dark mode support
- [ ] Add accessibility features
- [ ] Performance optimization

---

## Color Palette Reference

```scss
// Type Colors
$trigger-color: #885577;    // Purple
$action-color: #4A90E2;     // Blue
$transform-color: #2ECC71;  // Green
$conditional-color: #E67E22; // Orange
$ai-agent-color: #1ABC9C;   // Teal
$ai-tool-color: #16A085;    // Cyan
$code-color: #27AE60;       // Dark Green
$core-color: #7F8C8D;       // Gray

// State Colors
$error-color: #f44336;      // Red
$warning-color: #ffc107;    // Yellow
$success-color: #27ae60;    // Green
$disabled-color: #999999;   // Gray
```

---

## Testing Checklist

When testing node styling:

- [ ] Add each node type (trigger, action, transform, etc.)
- [ ] Verify correct border color appears
- [ ] Check that CSS class matches expected type
- [ ] Test hover effects
- [ ] Test selection state
- [ ] Verify sizing consistency
- [ ] Check on different screen sizes
- [ ] Test with multiple nodes on canvas

---

**Last Updated:** 2025-10-01
**Maintained By:** Development Team
