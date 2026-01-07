# n8n Visual Styling Implementation Guide for Odoo

**Purpose:** Replicate n8n's visual node styling in our Odoo module
**Date:** 2025-09-30
**Status:** Ready to Implement

---

## Executive Summary

**Key Discovery:** n8n does NOT use type-based colors! Each node uses its **service's brand color** (Gmail = Google blue, Slack = Slack purple, etc.). The only visual type differentiation is a **bolt icon** for triggers in the search panel.

**This gives us freedom to create a BETTER system** with actual type-based visual differentiation!

---

## 1. n8n's Actual System (What They Do)

### Visual Differentiation

| Element | Purpose | Implementation |
|---------|---------|----------------|
| **Icon** | Primary identifier | Service logo (SVG/PNG 60x60px) |
| **Color** | Service branding | Hex color from service brand |
| **Name** | Node label | Display name on canvas |
| **Bolt Icon** | Trigger indicator | Only in search panel, not on canvas |
| **Shape** | N/A | All nodes identical shape |

**Key Insight:** On the canvas, you cannot tell if a node is a trigger or action just by looking at it (except for the icon).

### Node Types in n8n

1. **Trigger Nodes** - Start workflows (`group: ['trigger']`)
2. **Action Nodes** - Perform operations (`group: ['input']`, `['transform']`, `['output']`)
3. **Core Nodes** - Generic functionality (IF, Code, Set, etc.)
4. **AI Nodes** - Cluster nodes (AI Agent root + sub-nodes)
5. **Tool Nodes** - Nodes with `.tool` suffix for AI agents

### Icon System

```typescript
// Single icon (works light & dark)
icon: 'file:servicename.svg'

// Separate light/dark icons
icon: {
  light: 'file:github.svg',
  dark: 'file:github.dark.svg'
}
```

**Storage:** Icons stored alongside node TypeScript files in `packages/nodes-base/nodes/[NodeName]/`

### Color System

```typescript
defaults: {
  name: 'Node Name',
  color: '#885577'  // Service brand color
}
```

**Examples Found:**
- Webhook: `#885577`
- Transform example: `#772244`
- Each service chooses their own color

---

## 2. Our Improved System (What We'll Build)

### Visual Differentiation Strategy

**Principle:** Use **left border color bars** to indicate node type, making it instantly recognizable.

| Node Type | Left Border | Icon | Badge |
|-----------|-------------|------|-------|
| **Trigger** | Purple `#885577` | 🔄 | None |
| **Action** | Blue `#4A90E2` | ⚡ | None |
| **Transform** | Green `#2ECC71` | ⚙️ | None |
| **Conditional** | Orange `#E67E22` | 🔀 | None |
| **AI Agent** | Teal `#1ABC9C` | 🤖 | "AI" |
| **AI Tool** | Cyan `#16A085` | 🔧 | "TOOL" |
| **Code** | Dark Green `#27AE60` | 💻 | None |
| **Core/Utility** | Gray `#7F8C8D` | 📦 | None |

### Color Palette

```scss
// Color System - Type-Based (Our Innovation)
$trigger-color: #885577;        // Purple
$action-color: #4A90E2;         // Blue
$transform-color: #2ECC71;      // Green
$conditional-color: #E67E22;    // Orange
$ai-agent-color: #1ABC9C;       // Teal
$ai-tool-color: #16A085;        // Cyan
$code-color: #27AE60;           // Dark Green
$core-color: #7F8C8D;           // Gray

// State Colors
$error-color: #E74C3C;          // Red
$warning-color: #F39C12;        // Orange
$success-color: #27AE60;        // Green
$disabled-color: #BDC3C7;       // Light Gray

// Dark Mode Adjustments
$dark-bg: #2C3E50;
$dark-text: #ECF0F1;
$dark-border: #34495E;
```

---

## 3. Complete CSS Implementation

### Base Node Styles

```scss
/* Node Manager Styles Enhancement - Visual Type Differentiation */

.canvas-node {
  position: absolute;
  background: white;
  border: 2px solid #dee2e6;
  border-left: 4px solid #7F8C8D;  // Default gray
  border-radius: 8px;
  min-width: 200px;
  max-width: 280px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: all 0.2s ease;
  cursor: move;
  user-select: none;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  overflow: hidden;

  /* Hover Effect */
  &:hover {
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    transform: translateY(-1px);
    z-index: 10;
  }

  /* Selected State */
  &.selected {
    border-color: #4A90E2;
    border-left-color: inherit;  // Keep type color
    box-shadow: 0 0 0 3px rgba(74, 144, 226, 0.2);
    z-index: 15;
  }

  /* Dragging State */
  &.dragging {
    transform: rotate(2deg);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.25);
    z-index: 20;
    opacity: 0.9;
  }

  /* Error State */
  &.error, &.has-error {
    border-color: #E74C3C;

    .node-header {
      background-color: #E74C3C !important;
    }

    .node-status {
      background: #E74C3C;
      animation: pulse 2s ease-in-out infinite;
    }
  }

  /* Disabled State */
  &.disabled {
    opacity: 0.5;
    filter: grayscale(50%);
    cursor: not-allowed;

    &:hover {
      transform: none;
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }
  }

  /* Warning State */
  &.warning {
    border-left-color: #F39C12;

    .node-status {
      background: #F39C12;
    }
  }

  /* Type-Specific Border Colors */
  &.trigger {
    border-left-color: #885577;
  }

  &.action {
    border-left-color: #4A90E2;
  }

  &.transform {
    border-left-color: #2ECC71;
  }

  &.conditional, &.condition {
    border-left-color: #E67E22;
  }

  &.ai-agent, &.agent {
    border-left-color: #1ABC9C;
  }

  &.ai-tool, &.tool {
    border-left-color: #16A085;
  }

  &.code {
    border-left-color: #27AE60;
  }

  &.core, &.utility {
    border-left-color: #7F8C8D;
  }
}

/* Node Header */
.node-header {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  border-bottom: 1px solid #dee2e6;
  font-weight: 500;
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: #495057;

  .node-icon {
    font-size: 14px;
    width: 16px;
    height: 16px;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .node-type-label {
    flex: 1;
    font-weight: 600;
  }

  /* Type-Specific Header Colors */
  .canvas-node.trigger & {
    background: linear-gradient(135deg, #885577 0%, #774466 100%);
    color: white;
    border-bottom-color: #663355;
  }

  .canvas-node.action & {
    background: linear-gradient(135deg, #4A90E2 0%, #3A7BC8 100%);
    color: white;
    border-bottom-color: #2A6BAE;
  }

  .canvas-node.transform & {
    background: linear-gradient(135deg, #2ECC71 0%, #27AE60 100%);
    color: white;
    border-bottom-color: #229954;
  }

  .canvas-node.conditional & {
    background: linear-gradient(135deg, #E67E22 0%, #D68910 100%);
    color: white;
    border-bottom-color: #CA6F1E;
  }

  .canvas-node.ai-agent & {
    background: linear-gradient(135deg, #1ABC9C 0%, #16A085 100%);
    color: white;
    border-bottom-color: #138D75;
  }

  .canvas-node.ai-tool & {
    background: linear-gradient(135deg, #16A085 0%, #138D75 100%);
    color: white;
    border-bottom-color: #117A65;
  }

  .canvas-node.code & {
    background: linear-gradient(135deg, #27AE60 0%, #229954 100%);
    color: white;
    border-bottom-color: #1E8449;
  }
}

/* Node Content */
.node-content {
  padding: 10px 12px;
  display: flex;
  flex-direction: column;
  gap: 6px;

  .node-name {
    font-size: 14px;
    font-weight: 500;
    color: #333;
    line-height: 1.4;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  .node-description {
    font-size: 12px;
    color: #666;
    line-height: 1.3;
    overflow: hidden;
    text-overflow: ellipsis;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
  }

  .node-id {
    font-size: 10px;
    color: #999;
    font-family: 'Courier New', monospace;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
}

/* Node Status Indicator */
.node-status {
  position: absolute;
  top: 8px;
  right: 8px;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #27AE60;  // Default: Ready
  border: 1px solid white;

  &.ready { background: #27AE60; }
  &.running {
    background: #3498DB;
    animation: pulse 1s ease-in-out infinite;
  }
  &.success { background: #27AE60; }
  &.error { background: #E74C3C; }
  &.warning { background: #F39C12; }
  &.disabled { background: #BDC3C7; }
}

/* AI/Tool Badge */
.node-badge {
  position: absolute;
  top: -8px;
  right: -8px;
  background: linear-gradient(135deg, #1ABC9C 0%, #16A085 100%);
  color: white;
  border-radius: 12px;
  padding: 2px 6px;
  font-size: 9px;
  font-weight: bold;
  letter-spacing: 0.5px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  border: 2px solid white;
  z-index: 5;

  &.tool-badge {
    background: linear-gradient(135deg, #16A085 0%, #138D75 100%);
  }

  &.agent-badge {
    background: linear-gradient(135deg, #1ABC9C 0%, #16A085 100%);
  }
}

/* Connection Ports */
.node-ports {
  position: absolute;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
  pointer-events: none;
}

.node-port {
  position: absolute;
  width: 12px;
  height: 12px;
  border: 2px solid white;
  border-radius: 50%;
  background: #7F8C8D;
  pointer-events: all;
  cursor: crosshair;
  transition: all 0.2s ease;
  z-index: 10;

  &.input {
    left: -6px;
    top: 50%;
    transform: translateY(-50%);
  }

  &.output {
    right: -6px;
    top: 50%;
    transform: translateY(-50%);
  }

  &:hover {
    background: #4A90E2;
    transform: translateY(-50%) scale(1.3);
    box-shadow: 0 0 0 3px rgba(74, 144, 226, 0.3);
  }

  /* Type-Specific Port Colors */
  .canvas-node.trigger &.output {
    background: #885577;
    border-color: #AA6699;

    &:hover {
      background: #AA6699;
      box-shadow: 0 0 0 3px rgba(136, 85, 119, 0.3);
    }
  }

  .canvas-node.action &.output,
  .canvas-node.transform &.output {
    background: #4A90E2;
    border-color: #5B9BD5;

    &:hover {
      background: #5B9BD5;
      box-shadow: 0 0 0 3px rgba(74, 144, 226, 0.3);
    }
  }
}

/* Service Icon (Large Icon in Node) */
.node-service-icon {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 8px auto;
  background: #f8f9fa;
  border-radius: 6px;
  border: 1px solid #dee2e6;

  img, svg {
    width: 32px;
    height: 32px;
    object-fit: contain;
  }

  /* Emoji fallback */
  &.emoji {
    font-size: 28px;
    background: transparent;
    border: none;
  }
}

/* Animations */
@keyframes pulse {
  0%, 100% {
    opacity: 1;
    transform: scale(1);
  }
  50% {
    opacity: 0.7;
    transform: scale(1.1);
  }
}

/* Dark Mode */
.dark-mode {
  .canvas-node {
    background: #2C3E50;
    border-color: #34495E;
    color: #ECF0F1;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);

    &:hover {
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5);
    }

    &.selected {
      box-shadow: 0 0 0 3px rgba(74, 144, 226, 0.4);
    }

    .node-content {
      .node-name {
        color: #ECF0F1;
      }

      .node-description {
        color: #BDC3C7;
      }

      .node-id {
        color: #7F8C8D;
      }
    }

    .node-port {
      background: #BDC3C7;
      border-color: #2C3E50;
    }

    .node-service-icon {
      background: #34495E;
      border-color: #4A5F7F;
    }
  }

  .node-header {
    // Dark mode headers keep their colored gradients
    // They look better with color in dark mode
  }
}

/* Responsive Adjustments */
@media (max-width: 768px) {
  .canvas-node {
    min-width: 160px;
    max-width: 220px;

    .node-content {
      padding: 8px 10px;

      .node-name {
        font-size: 13px;
      }

      .node-description {
        font-size: 11px;
      }
    }
  }
}
```

---

## 4. JavaScript Enhancement for Node Manager

Add this to your existing `node_manager.js` to support the new styling:

```javascript
// Add after line 382 (after addNodeFromN8nJSON method)

/**
 * Get node icon based on n8n type or service
 * Maps n8n types to visual icons
 */
getNodeIconFromN8nType(n8nType) {
    // Icon mapping for common n8n node types
    const iconMap = {
        // Triggers
        'webhook': '🌐',
        'webhookTrigger': '🌐',
        'scheduleTrigger': '⏰',
        'cronTrigger': '⏰',
        'manualTrigger': '👆',
        'formTrigger': '📝',
        'chatTrigger': '💬',

        // Actions - Common Services
        'gmail': '📧',
        'googleDrive': '📁',
        'googleSheets': '📊',
        'slack': '💬',
        'discord': '💬',
        'telegram': '✈️',
        'twitter': '🐦',
        'facebook': '📘',
        'linkedin': '💼',
        'github': '🐙',
        'gitlab': '🦊',

        // Core Nodes
        'if': '🔀',
        'switch': '🔀',
        'merge': '🔗',
        'split': '✂️',
        'loop': '🔄',
        'code': '💻',
        'function': '⚡',
        'set': '⚙️',
        'httpRequest': '🌐',

        // AI Nodes
        'aiAgent': '🤖',
        'aiTool': '🔧',
        'langchain': '🔗',
        'openai': '🧠',
        'anthropic': '🤖',
    };

    // Extract service name from n8n type
    // e.g., "n8n-nodes-base.gmail" → "gmail"
    const serviceName = n8nType.toLowerCase()
        .replace('n8n-nodes-base.', '')
        .replace('n8n-nodes-langchain.', '')
        .replace('trigger', '')
        .replace('tool', '')
        .trim();

    return iconMap[serviceName] || '📦';  // Default icon
}

/**
 * Get visual node class based on n8n type
 * Determines CSS class for styling
 */
getNodeClassFromN8nType(n8nType) {
    const lowerType = n8nType.toLowerCase();

    // AI/Tool detection
    if (lowerType.includes('agent')) return 'ai-agent';
    if (lowerType.includes('.tool') || lowerType.endsWith('tool')) return 'ai-tool';

    // Trigger detection
    if (lowerType.includes('trigger') ||
        lowerType.includes('webhook') ||
        lowerType.includes('schedule') ||
        lowerType.includes('cron') ||
        lowerType.includes('poll')) {
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

/**
 * Create AI/Tool badge element
 */
createNodeBadge(nodeType, n8nType) {
    const badge = document.createElement('div');
    badge.className = 'node-badge';

    if (n8nType.includes('agent')) {
        badge.className += ' agent-badge';
        badge.textContent = 'AI';
    } else if (n8nType.includes('.tool') || n8nType.endsWith('Tool')) {
        badge.className += ' tool-badge';
        badge.textContent = 'TOOL';
    } else {
        return null;  // No badge needed
    }

    return badge;
}
```

Now update the `createNodeElement` method to use these new functions:

```javascript
// Modify createNodeElement method (around line 474)
createNodeElement(nodeConfig) {
    const element = document.createElement('div');

    // Add base class
    element.className = 'canvas-node';

    // Add type-specific class (NEW!)
    if (nodeConfig.n8nType) {
        const nodeClass = this.getNodeClassFromN8nType(nodeConfig.n8nType);
        element.classList.add(nodeClass);
    } else {
        element.classList.add(nodeConfig.type);  // Fallback to internal type
    }

    element.setAttribute('data-node-id', nodeConfig.id);
    element.setAttribute('data-node-type', nodeConfig.type);
    if (nodeConfig.n8nType) {
        element.setAttribute('data-n8n-type', nodeConfig.n8nType);
    }

    // Position node
    element.style.left = nodeConfig.position.x + 'px';
    element.style.top = nodeConfig.position.y + 'px';

    // Get type configuration
    const typeConfig = this.config.types[nodeConfig.type] || this.config.types.action;

    // Get icon (NEW! - use n8n type if available)
    const icon = nodeConfig.n8nType
        ? this.getNodeIconFromN8nType(nodeConfig.n8nType)
        : typeConfig.icon;

    // Build node HTML
    element.innerHTML = `
        <div class="node-header">
            <span class="node-icon">${icon}</span>
            <span class="node-type-label">${typeConfig.label}</span>
        </div>
        <div class="node-content">
            <div class="node-name">${nodeConfig.name}</div>
            ${nodeConfig.description ? `<div class="node-description">${nodeConfig.description}</div>` : ''}
            <div class="node-id">${nodeConfig.id}</div>
        </div>
        <div class="node-status ${nodeConfig.status}"></div>
        <div class="node-ports">
            <div class="node-port input" data-port="input"></div>
            <div class="node-port output" data-port="output"></div>
        </div>
    `;

    // Add badge if AI/Tool node (NEW!)
    if (nodeConfig.n8nType) {
        const badge = this.createNodeBadge(nodeConfig.type, nodeConfig.n8nType);
        if (badge) {
            element.appendChild(badge);
        }
    }

    // Add node event listeners
    this.addNodeEventListeners(element, nodeConfig.id);

    return element;
}
```

---

## 5. Icon System Implementation

### Option 1: Emoji Icons (Quick & Easy)

Already implemented in the JavaScript above! Just use emoji characters.

**Pros:**
- ✅ No image files needed
- ✅ Works immediately
- ✅ Scales perfectly
- ✅ Color in dark/light mode

**Cons:**
- ❌ Limited selection
- ❌ Platform-dependent appearance
- ❌ Not as professional

### Option 2: SVG Icon System (Professional)

**Step 1: Create icon directory**
```
static/src/img/n8n-icons/
├── services/
│   ├── gmail.svg
│   ├── slack.svg
│   ├── github.svg
│   └── ...
├── types/
│   ├── trigger.svg
│   ├── action.svg
│   ├── code.svg
│   └── ...
└── sprite.svg  (Optional: combined sprite sheet)
```

**Step 2: Icon component in JavaScript**
```javascript
getNodeIconHTML(n8nType) {
    const serviceName = this.extractServiceName(n8nType);
    const iconPath = `/the_ai_automator/static/src/img/n8n-icons/services/${serviceName}.svg`;

    return `
        <div class="node-service-icon">
            <img src="${iconPath}"
                 alt="${serviceName}"
                 onerror="this.parentElement.classList.add('emoji'); this.parentElement.textContent='${this.getNodeIconFromN8nType(n8nType)}'">
        </div>
    `;
}
```

**Step 3: Download/create icons**
- Use service brand icons (check brand guidelines)
- Or use free icon packs: [Feather Icons](https://feathericons.com/), [Heroicons](https://heroicons.com/)
- Or extract from n8n repository: `packages/nodes-base/nodes/*/`

### Option 3: Icon Font (Best Balance)

Use [Codicons](https://microsoft.github.io/vscode-codicons/dist/codicon.html) (VSCode icons):

**Step 1: Add to template**
```html
<link rel="stylesheet" href="https://unpkg.com/@vscode/codicons@0.0.35/dist/codicon.css">
```

**Step 2: Use in JavaScript**
```javascript
getNodeIconHTML(n8nType) {
    const iconClass = this.getCodiconClass(n8nType);
    return `<i class="codicon ${iconClass}"></i>`;
}

getCodiconClass(n8nType) {
    const map = {
        'webhook': 'codicon-globe',
        'schedule': 'codicon-watch',
        'gmail': 'codicon-mail',
        'code': 'codicon-code',
        'if': 'codicon-git-branch',
        // ... more mappings
    };

    const serviceName = this.extractServiceName(n8nType);
    return map[serviceName] || 'codicon-symbol-event';
}
```

---

## 6. Type Detection Enhancement

Add this to `addNodeFromN8nJSON` method to improve type detection:

```javascript
// Enhanced type detection (replace lines 337-348)
let nodeType = 'action';  // Default
const lowerType = n8nType.toLowerCase();

// AI/Tool detection (highest priority)
if (lowerType.includes('agent')) {
    nodeType = 'ai-agent';
} else if (lowerType.includes('.tool') || lowerType.endsWith('tool')) {
    nodeType = 'ai-tool';
}
// Trigger detection
else if (lowerType.includes('trigger') ||
         lowerType.includes('webhook') ||
         lowerType.includes('schedule') ||
         lowerType.includes('poll') ||
         lowerType.includes('cron')) {
    nodeType = 'trigger';
}
// Code detection
else if (lowerType.includes('code') ||
         lowerType.includes('function')) {
    nodeType = 'code';
}
// Conditional detection
else if (lowerType.includes('if') ||
         lowerType.includes('switch')) {
    nodeType = 'conditional';
}
// Transform detection
else if (lowerType.includes('set') ||
         lowerType.includes('edit') ||
         lowerType.includes('merge') ||
         lowerType.includes('split')) {
    nodeType = 'transform';
}
```

---

## 7. Testing Your New Styles

### Test Commands

```javascript
// Test different node types with new styling

// 1. Trigger node (purple border, purple header)
const trigger = window.nodeManager.addNodeFromN8nJSON({
    id: "style-test-trigger",
    name: "Webhook Trigger",
    type: "n8n-nodes-base.webhook",
    position: [100, 100],
    parameters: {}
});

// 2. Action node (blue border, blue header)
const action = window.nodeManager.addNodeFromN8nJSON({
    id: "style-test-action",
    name: "Send Email",
    type: "n8n-nodes-base.gmail",
    position: [350, 100],
    parameters: { resource: "message", operation: "send" }
});

// 3. AI Tool node (cyan border, cyan header, "TOOL" badge)
const aiTool = window.nodeManager.addNodeFromN8nJSON({
    id: "style-test-aitool",
    name: "Custom Code Tool",
    type: "n8n-nodes-langchain.toolCode",
    position: [600, 100],
    parameters: {}
});

// 4. Code node (dark green border, dark green header)
const code = window.nodeManager.addNodeFromN8nJSON({
    id: "style-test-code",
    name: "Run JavaScript",
    type: "n8n-nodes-base.code",
    position: [100, 300],
    parameters: {}
});

// 5. Conditional node (orange border, orange header)
const conditional = window.nodeManager.addNodeFromN8nJSON({
    id: "style-test-if",
    name: "IF Condition",
    type: "n8n-nodes-base.if",
    position: [350, 300],
    parameters: {}
});

// Check styling
console.log('Trigger classes:', document.querySelector('[data-node-id="style-test-trigger"]').className);
console.log('Action classes:', document.querySelector('[data-node-id="style-test-action"]').className);
```

**Expected Results:**
- ✅ Purple left border and header for trigger
- ✅ Blue left border and header for action
- ✅ Cyan left border and header + "TOOL" badge for AI tool
- ✅ Dark green for code node
- ✅ Orange for conditional
- ✅ Emojis displayed in headers
- ✅ Hover effects work
- ✅ Selection highlights work

---

## 8. Implementation Checklist

### Phase 1: Basic Styling (30 min)
- [ ] Copy enhanced CSS to your styles file or `node_manager.js`
- [ ] Refresh page and check if existing nodes have new styles
- [ ] Test hover, selection, disabled states
- [ ] Verify colors match design

### Phase 2: Type Detection (20 min)
- [ ] Add helper methods to `node_manager.js`
- [ ] Update `createNodeElement` to use new classes
- [ ] Test with various n8n node types
- [ ] Verify correct colors apply

### Phase 3: Icons (30-60 min)
- [ ] Choose icon system (emoji/SVG/icon font)
- [ ] Implement icon loading in `createNodeElement`
- [ ] Test icon display for common services
- [ ] Add fallback for unknown services

### Phase 4: Badges (15 min)
- [ ] Add `createNodeBadge` method
- [ ] Integrate badge creation in `createNodeElement`
- [ ] Test AI and Tool badges appear correctly
- [ ] Style badge positioning

### Phase 5: Dark Mode (Optional, 30 min)
- [ ] Add dark mode toggle
- [ ] Test all colors in dark mode
- [ ] Adjust contrast if needed
- [ ] Ensure icons visible in both modes

### Phase 6: Polish (30 min)
- [ ] Add animations (pulse for running, etc.)
- [ ] Refine spacing and padding
- [ ] Test responsive behavior
- [ ] Cross-browser testing

**Total Time: 2.5 - 3.5 hours**

---

## 9. Summary

### What n8n Does
- ❌ No type-based visual differentiation
- ✅ Service-based colors
- ✅ Icon-driven identification
- ❌ Bolt icon only in search panel

### What We're Building (Better!)
- ✅ **Color-coded left borders** by type
- ✅ **Colored headers** matching node type
- ✅ **AI/Tool badges** for instant recognition
- ✅ **Rich icon system** (emoji/SVG/font)
- ✅ **Clear visual hierarchy**
- ✅ **Professional styling** with gradients and shadows

**Result:** Your nodes will be MORE visually organized than n8n's actual system, while maintaining their professional aesthetic!

---

**Next Step:** Copy the CSS to your project and update the JavaScript methods. Then test with the commands above to see your beautiful, color-coded nodes! 🎨