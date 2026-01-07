# N8N Integration Project Bible - Complete File Reference

## Project Overview
**Goal**: Port N8N workflow automation into Odoo 18 as a native module
**Architecture**: Python backend + Vanilla JavaScript frontend + PostgreSQL database
**Current Phase**: File consolidation and node overlay system

---

## Module Structure Map

### 📁 Root Module Files
```
addons/n8n_integration/
├── __manifest__.py                    # 🎛️ MODULE CONTROL CENTER
├── __init__.py                        # 🚀 MODULE STARTUP
└── README.md                          # 📖 MODULE DOCUMENTATION
```

#### `__manifest__.py` - Module Control Center
**What it does**: Tells Odoo what this module is and how to load it
**Core responsibilities**:
- Lists all JavaScript/CSS files to load (and in what order)
- Defines dependencies on other Odoo modules
- Specifies which XML view files to include
- Controls module metadata (name, version, description)

**When to modify**: When adding new files, changing load order, or updating module info
**Claude Code instruction**: "Only modify __manifest__.py to add new files to assets list"

---

## 📁 Backend (Python) - "Below the Line"

### Models (Database Layer)
```
models/
├── __init__.py                        # 🔌 MODELS CONNECTOR
├── n8n_workflow.py                    # 📋 WORKFLOW DATA
├── n8n_node.py                        # 🔗 NODE DATA
├── n8n_execution.py                   # ▶️ EXECUTION TRACKING
└── n8n_connection.py                  # 🔀 NODE CONNECTIONS
```

#### `n8n_workflow.py` - Workflow Data
**What it does**: Stores complete workflow definitions in PostgreSQL
**Core responsibilities**:
- Workflow name, description, status (active/inactive)
- JSON storage of entire workflow structure
- Relationships to nodes and executions
- Workflow-level settings and permissions

**Key data**: Workflow metadata, node positions, connection mappings
**Claude Code instruction**: "Only modify n8n_workflow.py for workflow-level database operations"

#### `n8n_node.py` - Node Data
**What it does**: Stores individual node information
**Core responsibilities**:
- Node type (trigger, action, core, service)
- Node position on canvas (x, y coordinates)
- Node parameters and configuration (JSON)
- Relationships to workflow and connections

**Key data**: Node configuration, position, parameters, relationships
**Claude Code instruction**: "Only modify n8n_node.py for node-level database operations"

### Controllers (The Bridge)
```
controllers/
├── __init__.py                        # 🔌 CONTROLLERS CONNECTOR
└── n8n_controller.py                  # 🌉 FRONTEND ↔ BACKEND BRIDGE
```

#### `n8n_controller.py` - Frontend ↔ Backend Bridge
**What it does**: Receives JavaScript requests and translates to database operations
**Core responsibilities**:
- `/n8n/add_node` - Create new node from frontend
- `/n8n/save_workflow` - Save entire workflow
- `/n8n/get_workflow` - Load workflow data
- `/n8n/execute_workflow` - Start workflow execution

**Key function**: THE crossing point between frontend and backend
**Claude Code instruction**: "Only modify n8n_controller.py to add new API endpoints"

---

## 📁 Frontend (JavaScript) - "Above the Line"

### Current Target Structure (Post-Consolidation)
```
static/src/js/
├── managers/                          # 🎯 CONSOLIDATED MANAGERS
│   ├── canvas_manager.js              # 🎨 CANVAS OPERATIONS
│   ├── node_manager.js                # 🔗 NODE OPERATIONS
│   ├── overlay_manager.js             # 📋 OVERLAY/UI OPERATIONS
│   └── workflow_coordinator.js       # 🎼 ORCHESTRATES EVERYTHING
└── [legacy files to be consolidated]  # 🗂️ OLD FILES TO MERGE
```

#### `canvas_manager.js` - Canvas Operations
**What it does**: Controls the visual workflow canvas where nodes appear
**Core responsibilities**:
- Canvas rendering (drawing the workspace)
- Canvas interactions (zoom, pan, scroll)
- Canvas positioning and sizing
- Canvas background and grid display
- Node placement on canvas
- Canvas event handling (clicks, drags)

**Key methods**:
- `initCanvas()` - Set up canvas element
- `renderCanvas()` - Draw/redraw canvas
- `addNodeToCanvas(node)` - Place node visually
- `handleCanvasClick(event)` - Process clicks

**Manages**: The visual workspace where everything appears
**Claude Code instruction**: "Only modify canvas_manager.js for canvas-level visual operations"

#### `node_manager.js` - Node Operations
**What it does**: Handles individual node creation, configuration, and behavior
**Core responsibilities**:
- Create new nodes from templates
- Node positioning and movement
- Node configuration and parameters
- Node connections between inputs/outputs
- Node validation and error checking
- Node deletion and cleanup

**Key methods**:
- `createNode(type, position)` - Create new node
- `configureNode(nodeId, params)` - Set node parameters
- `connectNodes(fromNode, toNode)` - Create connections
- `deleteNode(nodeId)` - Remove node

**Manages**: Individual node lifecycle and behavior
**Claude Code instruction**: "Only modify node_manager.js for node-specific operations"

#### `overlay_manager.js` - Overlay/UI Operations
**What it does**: Controls all popup overlays, panels, and UI interactions
**Core responsibilities**:
- Node selection overlay (the popup that shows available nodes)
- Node configuration panels
- Modal dialogs and popups
- UI state management (what's visible/hidden)
- User interaction handling (clicks, selections)
- Overlay positioning and animation

**Key methods**:
- `showNodeOverlay(position)` - Open node selection popup
- `hideOverlay()` - Close current overlay
- `showNodeConfig(nodeId)` - Open node settings
- `handleOverlayClick(event)` - Process overlay interactions

**Manages**: All user interface elements and interactions
**Claude Code instruction**: "Only modify overlay_manager.js for UI/overlay operations"

#### `workflow_coordinator.js` - Orchestrates Everything
**What it does**: Connects all managers together and handles cross-component communication
**Core responsibilities**:
- Initialize all other managers
- Handle communication between managers
- Coordinate complex operations (like adding a node involves canvas + node + overlay)
- Manage overall application state
- Handle workflow-level operations (save, load, execute)
- Integrate with Odoo backend (API calls)

**Key methods**:
- `init()` - Start up entire system
- `addNodeWorkflow(type, position)` - Complete add node process
- `saveWorkflow()` - Save to backend
- `loadWorkflow(id)` - Load from backend

**Manages**: Overall system coordination and backend integration
**Claude Code instruction**: "Only modify workflow_coordinator.js for system-level coordination"

---

## 📁 Views (Odoo Interface)
```
views/
├── n8n_menu.xml                       # 📋 ODOO MENU ITEMS
├── n8n_workflow_views.xml             # 📋 WORKFLOW LIST/FORM VIEWS
└── workflow_editor_template.xml       # 🎨 CANVAS CONTAINER
```

#### `workflow_editor_template.xml` - Canvas Container
**What it does**: Creates the HTML structure where JavaScript canvas lives
**Core responsibilities**:
- Define HTML div where canvas renders
- Include toolbar and buttons
- Set up container layout and styling
- Provide mounting point for JavaScript

**Key elements**: Canvas container div, toolbar area, button placement
**Claude Code instruction**: "Only modify workflow_editor_template.xml for HTML structure changes"

---

## 📁 Styling (CSS)
```
static/src/css/
├── canvas.css                         # 🎨 CANVAS VISUAL STYLES
├── node_overlay.css                   # 📋 OVERLAY VISUAL STYLES
└── workflow_editor.css                # 📋 OVERALL EDITOR STYLES
```

---

## 📁 Development Tools
```
dev_tools/
├── refactor_rename.py                 # 🔧 SAFE FILE RENAMING
├── refactor_function.py               # 🔧 SAFE FUNCTION RENAMING
└── fix_imports.py                     # 🔧 IMPORT STATEMENT FIXER
```

---

## 📁 Git Workflow Tools
```
git_workflows/
├── start_session.sh                   # 🚀 START SAFE EXPERIMENT
├── promote_session.sh                 # ✅ PROMOTE GOOD CHANGES
├── nuclear_rollback.sh                # 💥 DESTROY BAD CHANGES
└── create_milestone.sh                # 📌 CREATE CHECKPOINT
```

---

## File Interaction Map

### When User Clicks "Add Node" Button:
```
1. 🎨 canvas_manager.js - Detects click position
2. 📋 overlay_manager.js - Shows node selection overlay
3. 🔗 node_manager.js - Creates selected node
4. 🎼 workflow_coordinator.js - Coordinates the process
5. 🌉 n8n_controller.py - Saves node to database
6. 📋 n8n_node.py - Stores node data
```

### When User Saves Workflow:
```
1. 🎼 workflow_coordinator.js - Collects all workflow data
2. 🌉 n8n_controller.py - Receives save request
3. 📋 n8n_workflow.py - Updates workflow record
4. 📋 n8n_node.py - Updates all node records
```

---

## Claude Code Instruction Templates

### For Canvas Work:
```
"Work only on canvas_manager.js. This file handles canvas rendering, zooming, and visual workspace operations. Do not modify node_manager.js or overlay_manager.js."
```

### For Node Operations:
```
"Work only on node_manager.js. This file handles node creation, configuration, and connections. Do not modify canvas_manager.js or overlay_manager.js."
```

### For Overlay/UI Work:
```
"Work only on overlay_manager.js. This file handles all popups, overlays, and UI interactions. Do not modify canvas_manager.js or node_manager.js."
```

### For Integration Work:
```
"Work only on workflow_coordinator.js. This file connects all managers together. Only modify other managers if absolutely necessary."
```

### For Backend Work:
```
"Work only on n8n_controller.py for API endpoints, or n8n_node.py for database models. Do not modify frontend JavaScript files."
```

---

## Current Status Tracker

### ✅ Working (Don't Touch)
- Basic canvas rendering
- Node display on canvas
- Basic interactions

### 🔄 In Progress (Consolidation Phase)
- File consolidation into managers
- Overlay system implementation
- Integration between managers

### ❌ Not Started
- Workflow execution engine
- Advanced node connections
- Production deployment

---

## Quick Reference

### "I want to modify how nodes are displayed"
**File**: `node_manager.js`
**Instruction**: "Only modify node_manager.js for node display changes"

### "I want to change the canvas appearance"
**File**: `canvas_manager.js`
**Instruction**: "Only modify canvas_manager.js for canvas visual changes"

### "I want to add new overlay functionality"
**File**: `overlay_manager.js`
**Instruction**: "Only modify overlay_manager.js for overlay/UI changes"

### "I want to add a new API endpoint"
**File**: `n8n_controller.py`
**Instruction**: "Only modify n8n_controller.py to add new API endpoints"

### "I want to change database structure"
**File**: `n8n_node.py` or `n8n_workflow.py`
**Instruction**: "Only modify the specific model file for database changes"