# SAM AI Platform Registry - Complete Reference
**Date:** October 9, 2025
**Status:** Production
**Purpose:** Complete list of all registered canvas platforms

---

## Platform Registry Overview

The SAM AI Canvas Skeleton supports multiple platforms through the `canvas.platform` model. Each platform is registered with:

- **Display Name** - User-facing name shown in menus/UI
- **Technical Name** - Internal identifier used in code
- **Renderer Class** - JavaScript class that renders nodes
- **Renderer Module** - JS file path (or "preloaded")
- **Icon** - FontAwesome icon class
- **Sequence** - Display order (lower = first)

---

## Registered Platforms

### 1. SAM Creative Platform (Poppy)

**File:** `ai_sam/data/poppy/poppy_platform.xml`

```xml
<record id="platform_poppy" model="canvas.platform">
    <field name="name">SAM Creative Platform</field>
    <field name="technical_name">poppy</field>
    <field name="renderer_class">PoppyNodeRenderer</field>
    <field name="renderer_module">preloaded</field>
    <field name="icon">fa-magic</field>
    <field name="description">Creative multimedia canvas with AI chat, rich text, images, video, and interactive content blocks</field>
    <field name="active" eval="True"/>
    <field name="sequence">10</field>
</record>
```

**Features:**
- Multimedia content blocks (text, image, video)
- AI chat integration
- Rich text editing
- Card-style DOM rendering

**Menu:** SAM AI → SAM Creative
**Renderer:** `PoppyNodeRenderer` (DOM-based)
**Files:** `ai_sam/static/src/js/poppy_*.js`

---

### 2. Memory Knowledge Graph

**File:** `ai_sam/data/memory/memory_graph_platform.xml`

```xml
<record id="platform_memory_graph" model="canvas.platform">
    <field name="name">Memory Knowledge Graph</field>
    <field name="technical_name">ai_sam_memory_graph</field>
    <field name="renderer_class">MemoryGraphRenderer</field>
    <field name="renderer_module">preloaded</field>
    <field name="icon">fa-project-diagram</field>
    <field name="description">Interactive knowledge graph visualization with domain-colored nodes and relationship mapping</field>
    <field name="active" eval="True"/>
    <field name="sequence">20</field>
</record>
```

**Features:**
- Knowledge graph visualization
- Entity nodes with relationships
- Domain-colored nodes
- Graph database integration (Apache AGE)

**Menu:** SAM AI → Memory
**Renderer:** `MemoryGraphRenderer` (Canvas2D-based)
**Files:** `ai_sam/static/src/js/memory/memory_graph_renderer.js`

---

### 3. SAM Automator Platform

**File:** `ai_sam/data/automator/automator_platform.xml`

```xml
<record id="platform_automator" model="canvas.platform">
    <field name="name">SAM Automator Platform</field>
    <field name="technical_name">automator</field>
    <field name="renderer_class">AutomatorRenderer</field>
    <field name="renderer_module">preloaded</field>
    <field name="icon">fa-project-diagram</field>
    <field name="description">N8N workflow automation with 1,500+ service connectors, visual canvas, and professional node rendering</field>
    <field name="active" eval="True"/>
    <field name="sequence">30</field>
</record>
```

**Features:**
- N8N workflow automation
- 1,500+ service connectors
- Visual workflow canvas
- Bezier connection lines
- N8N JSON import/export

**Menu:** SAM AI → Automator
**Renderer:** `AutomatorRenderer` (to be created)
**Files:** `ai_sam/static/src/automator/n8n/*.js`

---

## Platform Manifest Loading Order

In `ai_sam/__manifest__.py`:

```python
'data': [
    ...
    'data/memory/memory_graph_platform.xml',     # Sequence: 20
    'data/poppy/poppy_platform.xml',             # Sequence: 10
    'data/automator/automator_platform.xml',     # Sequence: 30
    ...
]
```

**Display Order (by sequence):**
1. SAM Creative (10)
2. Memory (20)
3. Automator (30)

---

## Platform Renderer Files

### SAM Creative Platform
```
ai_sam/static/src/js/
├── poppy_node_renderer.js       # Main renderer
├── poppy_sidebar.js             # Element palette
├── poppy_toolbar.js             # Top toolbar
├── poppy_ai_chat_panel.js       # AI chat integration
├── poppy_multimedia.js          # Media handling
└── poppy_canvas_styles.css      # Styling
```

### Memory Platform
```
ai_sam/static/src/js/memory/
├── memory_graph_renderer.js     # Main renderer
├── memory_sidebar.js            # Graph controls
└── memory_graph_renderer_debug.js  # Debug tools
```

### Automator Platform
```
ai_sam/static/src/automator/n8n/
├── canvas/canvas_manager.js     # Canvas manager
├── nodes/node_manager.js        # N8N node CRUD
├── overlays/overlay_manager.js  # Node palette
├── lines/connection_manager.js  # Bezier connections
└── n8n_styles/n8n_node_canvas_styles.css
```

---

## How Platform Loading Works

1. **User opens canvas** (`/canvas/skeleton/open?canvas_id=X`)
2. **Controller checks** `canvas.skeleton_platform_id`
3. **Platform config fetched** from `canvas.platform` registry
4. **Platform Loader** (`platform_loader.js`) dynamically loads renderer
5. **Renderer instantiated** and injected into node manager
6. **Canvas loads** with platform-specific tools

**Code Flow:**
```javascript
// Step 1: Fetch platform config
const config = await platformLoader.fetchPlatformConfig(platformId);
// Result: { name: "SAM Creative Platform", renderer_class: "PoppyNodeRenderer", ... }

// Step 2: Load renderer module (if needed)
await platformLoader.loadRendererModule(config.renderer_module);

// Step 3: Instantiate renderer
const RendererClass = window[config.renderer_class];
const renderer = new RendererClass();

// Step 4: Inject into node manager
window.skeletonNodeManager.setRenderer(renderer);
```

---

## Adding a New Platform

To add a new platform (e.g., "Mind Map"):

### Step 1: Create Platform XML
```xml
<!-- ai_sam/data/mindmap/mindmap_platform.xml -->
<record id="platform_mindmap" model="canvas.platform">
    <field name="name">Mind Map Platform</field>
    <field name="technical_name">mindmap</field>
    <field name="renderer_class">MindMapRenderer</field>
    <field name="renderer_module">preloaded</field>
    <field name="icon">fa-brain</field>
    <field name="sequence">40</field>
</record>
```

### Step 2: Create Renderer
```javascript
// ai_sam/static/src/js/mindmap_renderer.js
class MindMapRenderer {
    initialize(canvasElement, canvasContext) { ... }
    renderNode(node) { ... }
    updateNode(node) { ... }
    removeNode(nodeId) { ... }
    clearCanvas() { ... }
}
window.MindMapRenderer = MindMapRenderer;
```

### Step 3: Add to Manifest
```python
'data': [
    ...
    'data/mindmap/mindmap_platform.xml',
],
'assets': {
    'web.assets_backend': [
        ...
        'ai_sam/static/src/js/mindmap_renderer.js',
    ]
}
```

### Step 4: Create Canvas
```python
canvas = env['canvas'].create({
    'name': 'My Mind Map',
    'skeleton_platform_id': env.ref('ai_sam.platform_mindmap').id,
})
```

---

## Platform Comparison Table

| Platform | Technical Name | Renderer | Rendering Type | Primary Use |
|----------|---------------|----------|----------------|-------------|
| **SAM Creative** | `poppy` | `PoppyNodeRenderer` | DOM (divs) | Multimedia content |
| **Memory** | `ai_sam_memory_graph` | `MemoryGraphRenderer` | Canvas2D | Knowledge graphs |
| **Automator** | `automator` | `AutomatorRenderer` | Canvas2D | N8N workflows |

---

## Current Status

✅ **Memory Platform** - Fully registered and functional
✅ **SAM Creative Platform** - Fully registered and functional
✅ **Automator Platform** - Newly registered (Oct 9, 2025)

**Next Steps:**
- Create `AutomatorRenderer` class (currently uses legacy N8N rendering)
- Migrate N8N canvas to use unified skeleton system
- Test all three platforms with skeleton canvas

---

**Document Version:** 1.0
**Last Updated:** October 9, 2025
**Related Docs:**
- `CANVAS_SKELETON_CORE_ARCHITECTURE.md`
- `PLATFORM_SIDEBAR_ARCHITECTURE.md`
