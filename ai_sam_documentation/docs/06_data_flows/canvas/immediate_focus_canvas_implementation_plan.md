# Immediate Focus: Canvas Implementation Plan

## The Core Problem You're Solving Right Now
**"I'm having a lot of trouble with the node overlay area"**

This makes perfect sense - you're essentially rebuilding one of the most complex parts of N8N: the visual workflow editor.

## Today's Coding Session Goal
**Create a working proof-of-concept canvas that can display and move nodes**

### File Structure for This Session
```
addons/n8n_integration/
├── static/src/
│   ├── js/
│   │   ├── canvas/
│   │   │   ├── canvas_component.js        ← Main focus
│   │   │   ├── node_component.js          ← Node rendering
│   │   │   └── connection_manager.js      ← Connections (later)
│   │   └── views/
│   │       └── workflow_view.js
│   ├── xml/
│   │   └── canvas_templates.xml           ← OWL templates
│   └── scss/
│       └── canvas.scss                    ← Canvas styling
```

## Step-by-Step Implementation

### Step 1: Basic Canvas Container (30 minutes)
**File**: `canvas_component.js`
```javascript
// Simple OWL component that renders an SVG canvas
// Goal: Show empty workspace where nodes can be placed
```

### Step 2: Node Rendering (45 minutes)
**File**: `node_component.js`
```javascript
// Create simple node representation
// Goal: Render nodes as draggable SVG rectangles with labels
```

### Step 3: Drag and Drop (45 minutes)
```javascript
// Implement basic drag functionality
// Goal: Click and drag nodes around the canvas
```

### Step 4: Canvas Integration (30 minutes)
```javascript
// Connect canvas to Odoo data
// Goal: Load nodes from workflow model and display them
```

## Simplified Node Overlay Approach

### Instead of Complex Canvas Library
**Use Simple SVG + HTML5 Drag API**

```xml
<!-- Basic node template -->
<svg class="canvas-workspace">
    <g class="node" transform="translate(100,100)">
        <rect width="150" height="80" fill="#f0f0f0" stroke="#333"/>
        <text x="75" y="45" text-anchor="middle">HTTP Request</text>
    </g>
</svg>
```

### Benefits of This Approach
- **Native browser support** - No external libraries
- **OWL compatible** - Works well with Odoo's framework
- **Performant** - SVG is optimized for this use case
- **Debuggable** - Easy to inspect and troubleshoot

## Canvas Data Flow

### 1. Load Workflow Data
```python
# In Python model
workflow_data = {
    'nodes': [
        {'id': 'node1', 'type': 'trigger', 'x': 100, 'y': 100},
        {'id': 'node2', 'type': 'http', 'x': 300, 'y': 100},
    ],
    'connections': [
        {'from': 'node1', 'to': 'node2'}
    ]
}
```

### 2. Render in Canvas
```javascript
// In OWL component
this.nodes.forEach(node => {
    this.renderNode(node.id, node.type, node.x, node.y);
});
```

### 3. Handle Interactions
```javascript
// Drag event handlers
onNodeDrag(nodeId, newX, newY) {
    // Update node position
    // Save to database if needed
}
```

## Success Criteria for Today
- [ ] Canvas component renders in Odoo view
- [ ] At least one dummy node displays
- [ ] Node can be dragged to new position
- [ ] Position changes are captured in JavaScript

## Next Session Preview
Once you have basic canvas working:
1. **Node connections** - Draw lines between nodes
2. **Node library** - Sidebar with available node types
3. **Node configuration** - Edit node parameters
4. **Data persistence** - Save canvas state to database

## Debugging Strategy
Since this is complex frontend work:
1. **Browser dev tools** - Use extensively for DOM inspection
2. **Console logging** - Log every interaction and state change
3. **Incremental building** - Get each piece working before adding more
4. **Simple first** - Don't worry about polish, focus on functionality