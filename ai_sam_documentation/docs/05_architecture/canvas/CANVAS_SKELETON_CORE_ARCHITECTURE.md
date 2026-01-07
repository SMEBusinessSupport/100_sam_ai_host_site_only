# SAM AI Canvas Skeleton Core Architecture
**Universal Canvas Platform with Dynamic Renderer System**

**Date:** October 9, 2025
**Status:** Production - Documented
**Author:** Better Business Builders
**Purpose:** Factual knowledge base for AI agents and development team

---

## Executive Summary

The SAM AI Canvas Skeleton is a **universal, polymorphic canvas framework** that provides a common core for all platform types (Automator, SAM Creative, Memory, Knowledge) while supporting platform-specific "skins" (renderers) that inject unique tools, node types, and behaviors.

**Key Principle:** ONE canvas core + MANY platform skins = Infinite extensibility

```
┌──────────────────────────────────────────────────────┐
│         SKELETON CANVAS CORE (Universal)             │
│  - Full-screen sizing (CanvasSizer)                  │
│  - Canvas engine (pan/zoom/grid)                     │
│  - Node manager (CRUD operations)                    │
│  - Connection system (bezier lines)                  │
│  - Platform loader (dynamic renderer injection)      │
└──────────────────────────────────────────────────────┘
                         ↓
         ┌───────────────┴───────────────┐
         ↓               ↓               ↓
  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
  │SAM CREATIVE │ │  AUTOMATOR  │ │   MEMORY    │
  │  RENDERER   │ │  RENDERER   │ │  RENDERER   │
  │  (Skin)     │ │  (Skin)     │ │  (Skin)     │
  ├─────────────┤ ├─────────────┤ ├─────────────┤
  │ Multimedia  │ │ N8N Nodes   │ │ Knowledge   │
  │ AI Chat     │ │ Workflows   │ │ Graph Viz   │
  │ Content     │ │ APIs        │ │ Entities    │
  └─────────────┘ └─────────────┘ └─────────────┘
```

---

## Part 1: The Skeleton Core

### 1.1 What is the Skeleton?

The **Skeleton Canvas Core** is the foundational layer that ALL platforms share. It provides:

1. **Canvas Container** - Full-screen HTML5 canvas element
2. **Sizing System** - Responsive viewport-based dimensions
3. **Rendering Engine** - Base drawing utilities (grid, connections, coordinates)
4. **Node Manager** - Generic node CRUD operations
5. **Platform Loader** - Dynamic renderer injection system

**File Locations:**
```
ai_sam/static/src/core/
├── canvas_sizer.js             # Universal sizing (ALL platforms)
├── skeleton_canvas_engine.js   # Base rendering utilities
├── skeleton_node_manager.js    # Generic node operations
└── platform_loader.js          # Dynamic platform loading
```

### 1.2 Skeleton Canvas Engine

**File:** `skeleton_canvas_engine.js`

**Purpose:** Platform-agnostic canvas rendering utilities

**Key Features:**
```javascript
class SkeletonCanvasEngine {
    // Canvas initialization
    setupCanvas()           // Setup HTML5 canvas
    resizeCanvas()          // Handle viewport changes

    // Drawing utilities
    clear()                 // Clear canvas
    drawGrid(gridSize)      // Draw background grid
    drawConnection(x1,y1,x2,y2)  // Bezier curves

    // Coordinate conversion
    screenToCanvas(x, y)    // Convert screen → canvas coords
    canvasToScreen(x, y)    // Convert canvas → screen coords
}
```

**What it does:**
- Sets up HTML5 2D rendering context
- Handles HiDPI screen scaling
- Provides coordinate transformation utilities
- Draws grid and connection lines
- **Does NOT know about specific node types** (platform-agnostic!)

### 1.3 Canvas Sizer (Universal Sizing)

**File:** `canvas_sizer.js`

**Purpose:** ONE sizing method for ALL platforms

**Architecture Decision:**
> All platforms inherit full-screen sizing from CanvasSizer. NO platform should override canvas dimensions. Platforms add tools, not size!

**Key Features:**
```javascript
class CanvasSizer {
    // Full-screen initialization
    initializeFullScreen()  // Called FIRST (before platform loads)

    // Automatic resizing
    resizeToFullScreen()    // Auto-called on window resize

    // Dimension queries
    getDimensions()         // { width, height }

    // Debug tools
    diagnose()             // Check for size overrides
}
```

**Default Sizing:**
- **Width:** `100vw` (full viewport width)
- **Height:** `calc(100vh - 50px)` (viewport minus toolbar)
- **Responsive:** Listens to window resize events

**Initialization Order:**
```
0. CanvasSizer.initializeFullScreen()  ← Runs FIRST!
1. Platform Loader detects branch_type
2. Platform Renderer loads
3. Platform adds tools (sidebar, toolbar, etc.)
4. Platform uses canvas dimensions (reads, not sets!)
```

### 1.4 Skeleton Node Manager

**File:** `skeleton_node_manager.js`

**Purpose:** Generic node CRUD operations (platform-agnostic)

**Key Features:**
```javascript
class SkeletonNodeManager {
    // Node lifecycle
    addNode(nodeData)       // Create new node
    updateNode(id, data)    // Modify existing node
    removeNode(id)          // Delete node

    // Renderer integration
    setRenderer(renderer)   // Inject platform renderer

    // Node queries
    getNode(id)            // Retrieve node by ID
    getAllNodes()          // Get all nodes
}
```

**What it does:**
- Maintains node collection
- Delegates rendering to platform-specific renderer
- Provides generic CRUD operations
- **Does NOT render nodes itself** (uses renderer!)

### 1.5 Platform Loader (Dynamic Renderer Injection)

**File:** `platform_loader.js`

**Purpose:** Dynamically load platform-specific renderers at runtime

**How It Works:**

```javascript
class SkeletonPlatformLoader {
    async loadPlatform(platformId) {
        // 1. Fetch platform config from backend
        const config = await fetchPlatformConfig(platformId);

        // 2. Load JavaScript module
        await loadRendererModule(config.renderer_module);

        // 3. Instantiate renderer class
        const RendererClass = window[config.renderer_class];
        this.renderer = new RendererClass();

        // 4. Inject into node manager
        window.skeletonNodeManager.setRenderer(this.renderer);

        return this.renderer;
    }
}
```

**Platform Configuration (Backend):**

Platform definitions are stored in `canvas.platform` model:

| Field | Purpose | Example |
|-------|---------|---------|
| `technical_name` | Unique platform ID | `"poppy"` |
| `name` | Display name | `"SAM Creative Platform"` |
| `renderer_class` | JS class name | `"PoppyNodeRenderer"` |
| `renderer_module` | JS file path | `"preloaded"` or `/path/to/module.js` |
| `icon` | FontAwesome icon | `"fa-magic"` |

**Example Platform Record:**
```xml
<record id="platform_poppy" model="canvas.platform">
    <field name="name">SAM Creative Platform</field>
    <field name="technical_name">poppy</field>
    <field name="renderer_class">PoppyNodeRenderer</field>
    <field name="renderer_module">preloaded</field>
    <field name="icon">fa-magic</field>
    <field name="sequence">10</field>
</record>
```

---

## Part 2: Platform Skins (Renderers)

### 2.1 What is a Platform Skin?

A **Platform Skin** (Renderer) is a JavaScript class that provides:

1. **Node Rendering** - How nodes look and behave
2. **Toolbars/Sidebars** - Platform-specific UI elements
3. **Node Types** - What kinds of nodes are available
4. **Interactions** - Drag, drop, resize, edit behaviors

**Key Principle:** The renderer **uses** the skeleton canvas, it doesn't replace it!

### 2.2 Renderer Interface

All platform renderers must implement this interface:

```javascript
class YourPlatformRenderer {
    constructor() {
        // Renderer initialization
    }

    // REQUIRED: Initialize with canvas context
    initialize(canvasElement, canvasContext) {
        this.canvasElement = canvasElement;
        this.ctx = canvasContext;
        // Setup platform-specific UI
    }

    // REQUIRED: Render a single node
    renderNode(node) {
        // Draw node on canvas or create DOM element
    }

    // REQUIRED: Update existing node
    updateNode(node) {
        // Re-render node with new data
    }

    // REQUIRED: Remove node
    removeNode(nodeId) {
        // Clean up node from canvas/DOM
    }

    // REQUIRED: Clear all nodes
    clearCanvas() {
        // Remove all nodes
    }

    // OPTIONAL: Render entire graph
    renderGraph(graphData) {
        // Render {nodes: [], edges: []}
    }
}
```

### 2.3 Existing Platform Renderers

#### 2.3.1 Poppy Node Renderer

**File:** `ai_sam/static/src/js/poppy_node_renderer.js`

**Platform Type:** Creative multimedia canvas

**Node Types:**
- `text_block` - Rich text editing
- `image_block` - Image display
- `video_block` - YouTube embeds
- `ai_chat_block` - Embedded AI conversation

**Rendering Approach:**
- **DOM-based** (creates `<div>` elements)
- **Card style** (rounded corners, shadows)
- **Draggable** (via mouse events)
- **Positioned absolutely** (x/y coordinates)

**Example Node:**
```html
<div class="poppy-node-card text_block" style="left: 100px; top: 200px;">
    <div class="poppy-card-header">
        <i class="fa fa-font"></i> Text Block
        <button class="delete-node-btn">×</button>
    </div>
    <div class="poppy-card-content" contenteditable="true">
        <p>User's content here...</p>
    </div>
</div>
```

**Special Features:**
- Integrated AI chat panel (`PoppyAIChatPanel`)
- Multimedia toolbar (`PoppyToolbar`)
- Content editing (inline `contenteditable`)

**UI Components:**
```
ai_sam/static/src/js/
├── poppy_node_renderer.js      # Node rendering
├── poppy_sidebar.js            # Element palette
├── poppy_toolbar.js            # Top toolbar
├── poppy_ai_chat_panel.js      # AI integration
└── poppy_canvas_styles.css     # Card styling
```

#### 2.3.2 Memory Graph Renderer

**File:** `ai_sam/static/src/js/memory/memory_graph_renderer.js`

**Platform Type:** Knowledge graph visualization

**Node Types:**
- Graph nodes (entities from knowledge base)
- Edges (relationships between entities)

**Rendering Approach:**
- **Canvas-based** (uses 2D context)
- **Circle nodes** (with labels)
- **Line edges** (connecting nodes)
- **Force-directed layout** (future: vis.js integration)

**Example Rendering:**
```javascript
renderNode(node) {
    // Draw circle
    ctx.arc(node.x, node.y, node.size || 15, 0, 2 * Math.PI);
    ctx.fillStyle = node.color || '#3498db';
    ctx.fill();

    // Draw label
    ctx.fillText(node.label, node.x, node.y + 30);
}
```

**Special Features:**
- Memory sidebar (`memory_sidebar.js`)
- Search functionality
- Domain-colored nodes (different colors per entity type)
- Relationship visualization

**Data Source:**
- Nodes loaded from `ai.graph.service`
- Connected to SAM AI knowledge base
- Real-time graph updates

#### 2.3.3 Automator Renderer (N8N)

**Platform Type:** Workflow automation

**Node Types:**
- Trigger nodes (webhooks, schedules)
- Action nodes (HTTP, database, API)
- Logic nodes (IF, Switch, Merge)
- 1,500+ service connectors

**Rendering Approach:**
- **N8N-compatible** node styling
- **Workflow connections** (bezier curves)
- **Execution visualization** (show data flow)

**UI Components:**
```
ai_sam/static/src/automator/n8n/
├── overlays/overlay_manager.js     # Node palette overlay
├── nodes/node_manager.js           # N8N node CRUD
├── canvas/canvas_manager.js        # Pan/zoom
└── lines/connection_manager.js     # Connections
```

**Special Features:**
- 1,500+ pre-built node types
- N8N node type registry integration
- Workflow execution tracking
- API connector library

---

## Part 3: The Unified Template

### 3.1 Skeleton Canvas Container

**File:** `ai_sam/views/skeleton_canvas_container.xml`

**Purpose:** Unified template for ALL platforms

**Template Structure:**
```xml
<template id="skeleton_canvas_container">
    <!-- Header (platform selector, canvas name) -->
    <div class="skeleton-platform-header">
        <h4>{{ canvas.name }} - {{ platform.name }}</h4>
    </div>

    <!-- Main canvas area -->
    <div id="skeletonCanvasArea" class="skeleton-canvas-area">
        <canvas id="nodeCanvas"></canvas>
    </div>

    <!-- Platform UI container (injected by renderer) -->
    <div id="skeletonPlatformUIContainer"></div>

    <!-- Initialization script -->
    <script>
        // STEP 0: Initialize canvas sizer (FIRST!)
        window.canvasSizer = new CanvasSizer(nodeCanvas);
        window.canvasSizer.initializeFullScreen();

        // STEP 1: Initialize skeleton engine
        window.skeletonEngine = new SkeletonCanvasEngine(nodeCanvas);

        // STEP 2: Initialize node manager
        window.skeletonNodeManager = new SkeletonNodeManager(nodeCanvas);

        // STEP 3: Load platform renderer
        const platformId = {{ current_platform.id }};
        window.platformLoader = new SkeletonPlatformLoader();
        await platformLoader.loadPlatform(platformId);

        // STEP 4: Load canvas nodes
        await loadCanvasNodes({{ canvas.id }});
    </script>
</template>
```

### 3.2 Controller Routes

**File:** `ai_sam/controllers/skeleton_canvas_controller.py`

**Key Endpoints:**

| Route | Purpose | Returns |
|-------|---------|---------|
| `/canvas/skeleton/open` | Open canvas with platform | Renders skeleton template |
| `/canvas/platform/config` | Get platform config | JSON (renderer class, module) |
| `/canvas/platform/list` | List all platforms | JSON (platform registry) |
| `/canvas/load_nodes` | Load nodes for canvas | JSON (nodes array) |
| `/canvas/skeleton/set_platform` | Switch platform | JSON (success/error) |

**Example Controller Method:**
```python
@http.route('/canvas/skeleton/open', type='http', auth='user')
def open_skeleton_canvas(self, canvas_id, platform_id=None):
    canvas = request.env['canvas'].browse(int(canvas_id))

    # Get platform (or use default)
    if platform_id:
        platform = request.env['canvas.platform'].browse(int(platform_id))
    else:
        platform = canvas.skeleton_platform_id or \
                   request.env['canvas.platform'].search([('active', '=', True)], limit=1)

    # Render unified template
    return request.render('ai_sam.skeleton_canvas_container', {
        'canvas': canvas,
        'current_platform': platform,
        'platforms': all_active_platforms,
    })
```

---

## Part 4: Platform-Specific Customizations

### 4.1 Unified Sidebar Architecture

**File:** `ai_sam/PLATFORM_SIDEBAR_ARCHITECTURE.md`

**Design Principle:**
> ONE sidebar container (`.platform-sidebar`) used by ALL platforms. Platform-specific content classes customize the interior.

**Shared CSS:**
```css
/* ai_sam/static/src/css/platform_sidebar.css */

.platform-sidebar {
    position: fixed;
    left: 0;
    top: 50px;
    width: 280px;
    height: calc(100vh - 50px);
    background: #ffffff;
    z-index: 100;
}

.platform-sidebar-header {
    padding: 16px;
    border-bottom: 1px solid #dee2e6;
}

.platform-sidebar-section {
    padding: 12px;
}
```

**Platform-Specific Content:**
```css
/* Poppy customizations */
.poppy-sidebar-content .poppy-add-btn {
    /* Poppy-specific button styling */
}

/* Memory customizations */
.memory-sidebar-content .memory-search {
    /* Memory-specific search styling */
}
```

**Benefits:**
1. Consistent positioning across platforms
2. No code duplication
3. Easy to maintain (one CSS file)
4. Platform flexibility (custom interior content)

### 4.2 Platform-Specific CSS

Each platform can have custom styling for its nodes/tools:

| Platform | CSS File | Purpose |
|----------|----------|---------|
| Poppy | `poppy_canvas_styles.css` | Card styling, content blocks |
| Automator | `n8n_node_canvas_styles.css` | N8N node styling |
| Memory | Shared styles (no custom CSS) | Uses base skeleton styles |

**Load Order in Manifest:**
```python
'web.assets_backend': [
    # Skeleton core (loaded FIRST)
    'ai_sam/static/src/css/skeleton_base.css',
    'ai_sam/static/src/css/platform_sidebar.css',

    # Platform-specific (loaded AFTER)
    'ai_sam/static/src/css/poppy_canvas_styles.css',
    'ai_sam/static/src/automator/n8n/n8n_styles/n8n_node_canvas_styles.css',
]
```

---

## Part 5: Data Flow & Node Storage

### 5.1 How Nodes are Loaded

**Platform Detection Flow:**

```
1. User opens canvas
   ↓
2. Controller checks canvas.skeleton_platform_id
   ↓
3. Platform config fetched: { technical_name: "poppy", renderer_class: "PoppyNodeRenderer" }
   ↓
4. Platform Loader dynamically loads renderer
   ↓
5. Controller routes node loading based on platform:

   IF platform = "poppy":
       Load from canvas.node model

   ELSE IF platform = "ai_sam_memory_graph":
       Load from ai.graph.service (knowledge base)

   ELSE IF platform = "automator":
       Load from workflow.node model
```

### 5.2 Node Storage Models

**Poppy Nodes:**
```python
Model: canvas.node
Fields:
- canvas_id (Many2one to canvas)
- x, y (Float - position)
- type (Selection: text_block, image_block, etc.)
- data (JSON - node parameters)
```

**Memory Nodes:**
```python
Model: ai.graph.entity (knowledge base)
Fields:
- name (Char)
- entity_type (Selection: person, company, concept)
- domain (Selection: color-coded)
- relationships (One2many to ai.graph.relationship)
```

**Automator Nodes:**
```python
Model: workflow.node
Fields:
- workflow_id (Many2one to canvas)
- node_type (Char - N8N node type)
- position_x, position_y (Float)
- parameters (JSON - N8N node config)
```

### 5.3 Backend Node Loading

**Controller Method:**
```python
@http.route('/canvas/load_nodes', type='json', auth='user')
def load_canvas_nodes(self, canvas_id):
    canvas = request.env['canvas'].browse(int(canvas_id))
    platform = canvas.skeleton_platform_id

    if not platform:
        return {'success': True, 'nodes': []}

    # Route to platform-specific loading
    if platform.technical_name == 'ai_sam_memory_graph':
        # Load from knowledge graph
        return request.env['ai.graph.service'].get_graph_nodes_for_canvas(canvas_id)

    elif platform.technical_name == 'poppy':
        # Load from canvas.node model
        nodes = request.env['canvas.node'].search([('canvas_id', '=', canvas_id)])
        return {
            'success': True,
            'nodes': [{
                'id': node.id,
                'x': node.x,
                'y': node.y,
                'type': node.type,
                'data': json.loads(node.data) if node.data else {}
            } for node in nodes]
        }

    else:
        # Default: no nodes
        return {'success': True, 'nodes': []}
```

---

## Part 6: Creating New Platforms

### 6.1 Platform Creation Checklist

To add a new platform (e.g., "MindMap"):

**Step 1: Create Platform Record**
```xml
<!-- ai_sam/data/mindmap/mindmap_platform.xml -->
<record id="platform_mindmap" model="canvas.platform">
    <field name="name">Mind Map</field>
    <field name="technical_name">mindmap</field>
    <field name="renderer_class">MindMapRenderer</field>
    <field name="renderer_module">preloaded</field>
    <field name="icon">fa-brain</field>
    <field name="sequence">30</field>
</record>
```

**Step 2: Create Renderer Class**
```javascript
// ai_sam/static/src/js/mindmap_renderer.js

class MindMapRenderer {
    constructor() {
        this.nodes = new Map();
    }

    initialize(canvasElement, canvasContext) {
        this.canvas = canvasElement;
        this.ctx = canvasContext;
        this.initializeMindMapToolbar();
    }

    renderNode(node) {
        // Draw circular bubble
        const bubble = document.createElement('div');
        bubble.className = 'mindmap-bubble';
        bubble.style.left = `${node.x}px`;
        bubble.style.top = `${node.y}px`;
        bubble.innerHTML = `<span>${node.label}</span>`;

        this.canvas.parentElement.appendChild(bubble);
        this.nodes.set(node.id, bubble);
    }

    updateNode(node) {
        const bubble = this.nodes.get(node.id);
        if (bubble) {
            bubble.style.left = `${node.x}px`;
            bubble.style.top = `${node.y}px`;
        }
    }

    removeNode(nodeId) {
        const bubble = this.nodes.get(nodeId);
        if (bubble) {
            bubble.remove();
            this.nodes.delete(nodeId);
        }
    }

    clearCanvas() {
        this.nodes.forEach(bubble => bubble.remove());
        this.nodes.clear();
    }
}

window.MindMapRenderer = MindMapRenderer;
```

**Step 3: Add to Manifest**
```python
# ai_sam/__manifest__.py
'data': [
    'data/mindmap/mindmap_platform.xml',
],
'assets': {
    'web.assets_backend': [
        'ai_sam/static/src/js/mindmap_renderer.js',
        'ai_sam/static/src/css/mindmap_styles.css',
    ]
}
```

**Step 4: Create Canvas with Platform**
```python
canvas = env['canvas'].create({
    'name': 'My Mind Map',
    'skeleton_platform_id': env.ref('ai_sam.platform_mindmap').id,
})
```

**Step 5: Open Canvas**
```
/canvas/skeleton/open?canvas_id={canvas.id}
```

**Result:** Canvas opens with MindMapRenderer loaded!

---

## Part 7: Architecture Benefits

### 7.1 Why This Design is Brilliant

**1. Single Source of Truth**
- ONE canvas template (`skeleton_canvas_container.xml`)
- ONE sizing system (`CanvasSizer`)
- ONE rendering engine (`SkeletonCanvasEngine`)
- ONE node manager (`SkeletonNodeManager`)

**2. Platform Extensibility**
- Add new platform = Create renderer class + XML record
- NO changes to canvas core required
- Clean separation of concerns

**3. Code Reuse**
- Canvas manager shared
- Node CRUD shared
- Connection system shared
- Sizing logic shared
- Only node rendering differs

**4. Consistent UX**
- Same canvas UI across all platforms
- Familiar pan/zoom/save controls
- Only node palette differs

**5. Maintainability**
- Fix canvas bug → Fixed for ALL platforms
- Update sizing → Updated for ALL platforms
- Add new feature → Available to ALL platforms

**6. Scalability**
- Adding 10th platform as easy as 1st
- No exponential code growth
- Renderer pattern enforces consistency

### 7.2 Real-World Example

**Before Skeleton (Old Architecture):**
```
Poppy has its own canvas code (500 lines)
Automator has its own canvas code (500 lines)
Memory has its own canvas code (500 lines)
---
Total: 1,500 lines of duplicated code
Bug in canvas? Fix in 3 places!
```

**After Skeleton (Current Architecture):**
```
Skeleton core: 300 lines (shared)
Poppy renderer: 200 lines (unique)
Automator renderer: 200 lines (unique)
Memory renderer: 200 lines (unique)
---
Total: 900 lines (40% reduction!)
Bug in canvas? Fix in ONE place!
```

---

## Part 8: Debug & Troubleshooting

### 8.1 Console Debug Commands

**Check Canvas Sizer:**
```javascript
window.debugCanvasSize()
// Output: { initialized: true, isFullScreen: true, warnings: [] }
```

**Check Platform Loader:**
```javascript
console.log(window.platformLoader.getCurrentPlatform())
// Output: { name: "Poppy", technical_name: "poppy", renderer_class: "PoppyNodeRenderer" }
```

**Check Node Manager:**
```javascript
console.log(window.skeletonNodeManager.getAllNodes())
// Output: [{ id: 1, x: 100, y: 200, type: "text_block" }, ...]
```

**Check Current Renderer:**
```javascript
console.log(window.platformLoader.getRenderer())
// Output: PoppyNodeRenderer { canvasElement: canvas#nodeCanvas, ... }
```

### 8.2 Common Issues

**Issue: Canvas not full-screen**
```javascript
// Check if CanvasSizer initialized
console.log(window.canvasSizer.initialized)  // Should be true

// Force resize
window.canvasSizer.forceResize()

// Diagnose
window.canvasSizer.diagnose()  // Check for warnings
```

**Issue: Platform not loading**
```javascript
// Check platform config
await fetch('/canvas/platform/config', {
    method: 'POST',
    body: JSON.stringify({ jsonrpc: '2.0', params: { platform_id: 1 } })
})

// Check renderer class exists
console.log(window.PoppyNodeRenderer)  // Should be function
```

**Issue: Nodes not appearing**
```javascript
// Check node manager has nodes
console.log(window.skeletonNodeManager.nodes)

// Check renderer is set
console.log(window.skeletonNodeManager.renderer)  // Should not be null

// Manually trigger render
window.skeletonNodeManager.renderer.renderGraph({
    nodes: window.skeletonNodeManager.nodes,
    edges: []
})
```

### 8.3 Browser Console Expected Output

**Successful Initialization:**
```
🖼️ [CANVAS SIZER] Module loaded
🎨 [SKELETON] CanvasEngine initialized
🔌 [SKELETON] PlatformLoader created
🔄 [SKELETON] Loading platform: 1
📋 [SKELETON] Platform config: { name: "Poppy", ... }
✅ [SKELETON] Renderer instantiated: PoppyNodeRenderer
✅ [SKELETON] Platform loaded: Poppy
🎨 [POPPY] Renderer created
✅ [POPPY] Renderer initialized
✅ [POPPY] Toolbar initialized
✅ [POPPY] AI Chat Panel initialized
```

---

## Part 9: File Reference Map

### 9.1 Core Skeleton Files

```
ai_sam/
├── static/src/core/
│   ├── canvas_sizer.js              # Universal sizing (ALL platforms)
│   ├── skeleton_canvas_engine.js    # Base rendering engine
│   ├── skeleton_node_manager.js     # Generic node CRUD
│   └── platform_loader.js           # Dynamic renderer loading
│
├── static/src/css/
│   ├── skeleton_base.css            # Base canvas styles
│   └── platform_sidebar.css         # Unified sidebar (ALL platforms)
│
├── controllers/
│   └── skeleton_canvas_controller.py # Canvas routes & platform config
│
└── views/
    └── skeleton_canvas_container.xml # Unified canvas template
```

### 9.2 Platform Renderer Files

**SAM Creative Platform (Poppy):**
```
ai_sam/static/src/js/
├── poppy_node_renderer.js           # Node rendering
├── poppy_sidebar.js                 # Element palette
├── poppy_toolbar.js                 # Top toolbar
├── poppy_ai_chat_panel.js           # AI integration
└── poppy_canvas_styles.css          # Card styling
```

**Memory Platform:**
```
ai_sam/static/src/js/memory/
├── memory_graph_renderer.js         # Graph visualization
├── memory_sidebar.js                # Memory tools
└── memory_graph_renderer_debug.js   # Debug utilities
```

**Automator Platform:**
```
ai_sam/static/src/automator/n8n/
├── overlays/overlay_manager.js      # Node palette
├── nodes/node_manager.js            # N8N node CRUD
├── canvas/canvas_manager.js         # Pan/zoom
└── lines/connection_manager.js      # Connections
```

### 9.3 Data Registration Files

```
ai_sam/data/
├── memory/
│   └── memory_graph_platform.xml    # Memory platform record
└── (future platforms)
    └── mindmap_platform.xml         # Example
```

### 9.4 Model Files

```
ai_brain/models/
├── canvas_platform.py               # Platform registry model
├── canvas_extension.py              # Canvas.skeleton_platform_id field
└── canvas.py                        # Base canvas model
```

---

## Part 10: Migration & Version History

### 10.1 Evolution of Canvas Architecture

**V1: Module-Specific Canvases (Pre-2025)**
- Each module had own canvas template
- `the_ai_automator` had automator canvas
- Poppy had separate poppy canvas
- Memory had separate memory canvas
- **Problem:** Code duplication, inconsistent UX

**V2: Template Consolidation (Early 2025)**
- Moved all templates to `ai_sam` module
- Created `canvas_page_views.xml` as unified template
- Updated controller references (`the_ai_automator` → `ai_sam`)
- **Problem:** Still platform-specific rendering logic in core

**V3: Skeleton + Platform System (Current - Oct 2025)**
- Created skeleton core (platform-agnostic)
- Introduced `canvas.platform` model (platform registry)
- Built `SkeletonPlatformLoader` (dynamic renderer injection)
- Created `CanvasSizer` (universal sizing)
- Established renderer interface contract
- **Result:** True platform extensibility!

### 10.2 Breaking Changes (V2 → V3)

**Controllers:**
```python
# OLD (V2)
return request.render('the_ai_automator.canvas_page', values)

# NEW (V3)
return request.render('ai_sam.skeleton_canvas_container', values)
```

**Canvas Opening:**
```python
# OLD (V2)
canvas.action_open_canvas()  # Hard-coded route

# NEW (V3)
canvas.action_open_skeleton_canvas()  # Uses skeleton_platform_id
```

**Renderer Loading:**
```javascript
// OLD (V2)
// Hard-coded renderer instantiation in template

// NEW (V3)
const platformLoader = new SkeletonPlatformLoader();
await platformLoader.loadPlatform(platformId);  // Dynamic!
```

---

## Part 11: Future Enhancements

### 11.1 Planned Improvements

**Phase 1: Mobile Support**
- Responsive breakpoints in `CanvasSizer`
- Touch gesture support (pinch zoom, pan)
- Mobile-optimized sidebars (collapsible)

**Phase 2: Advanced Rendering**
- WebGL rendering option (for large graphs)
- Canvas layer system (background/foreground)
- Zoom level persistence

**Phase 3: Collaboration**
- Real-time multi-user editing
- Cursor tracking (see other users)
- Change conflict resolution

**Phase 4: Platform Marketplace**
- Community-contributed platforms
- Platform versioning
- Hot-reloading renderers (dev mode)

### 11.2 Potential New Platforms

**Mind Map Platform**
- Radial tree layout
- Collapsible branches
- Export to Markdown

**BPMN Process Designer**
- Swimlane layouts
- BPMN node types
- Process validation

**Kanban Board**
- Column-based layout
- Drag-drop cards
- WIP limits

**Timeline/Gantt**
- Time-based X-axis
- Task dependencies
- Resource allocation

---

## Conclusion

The SAM AI Canvas Skeleton architecture represents a **mature, extensible platform system** that achieves:

✅ **Code Reusability** - ONE core, MANY platforms
✅ **Consistent UX** - Same canvas experience everywhere
✅ **Clean Architecture** - Separation of concerns (core vs. skin)
✅ **Easy Maintenance** - Fix once, apply everywhere
✅ **Future-Proof** - Add platforms without touching core

**Core Philosophy:**
> The skeleton provides the bones. The platform provides the soul.

**For AI Agents:**
This document serves as **factual knowledge** for:
- Understanding canvas architecture decisions
- Implementing new platforms
- Debugging canvas issues
- Maintaining code consistency
- Explaining design rationale to developers

---

**Document Version:** 1.0
**Last Updated:** October 9, 2025
**Maintained By:** Better Business Builders
**Related Docs:**
- `PLATFORM_SIDEBAR_ARCHITECTURE.md`
- `CANVAS_CONSOLIDATION_STRATEGY.md`
- `SESSION_REPORT_2025-10-09_Canvas_Unification.md`

**End of Architecture Documentation**
