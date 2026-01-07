# Implementation Bridge: N8N Research → AI Automator Odoo Module

**Date**: 2025-10-01
**Status**: Ready for NDV (Node Detail View) Implementation

---

## Executive Summary

This document bridges your comprehensive N8N research with your current Odoo module architecture, providing specific implementation paths for building an N8N-style node configuration panel.

**Research Source**: `n8n_node_detail_popup_deep_research.md`
**Current Architecture**: Module split complete, data layer stable
**Next Step**: Build NDV (Node Details View) UI component

---

## Current State: What You Already Have

### ✅ Data Layer (ai_automator_base)
```
✓ Canvas model with json_definition field
✓ Nodes model (optional relational storage)
✓ Connections model
✓ n8n_simple_nodes model (node type definitions)
✓ n8n_simple_supplier model (node packages)
✓ api_credentials model (credential storage)
```

### ✅ Storage Architecture
**Matches N8N's approach!**
- Canvas stores workflow as JSON in `json_definition` column
- Node parameters stored inside workflow JSON (not separate tables)
- Database: PostgreSQL (ai_automator_db)
- Current working canvas: ID 59 "Customer Onboarding"

### ✅ Frontend Infrastructure
```
✓ Vanilla JavaScript canvas (working)
✓ Node drag/drop (working)
✓ Pan/Zoom (working)
✓ Connection lines (working)
✓ Save/Load via RPC (working)
```

### ❌ Missing: NDV (Node Configuration Panel)
**This is your next build target**

---

## N8N's NDV Architecture (From Research)

### Storage Layers (N8N)
```
Layer 1: Pinia Store (Runtime)
   ↓
Layer 2: Workflow JSON (In-Memory)
   ↓
Layer 3: Database (workflow_entity.nodes)
```

### Your Equivalent (Odoo)
```
Layer 1: JavaScript State (Your overlay_manager.js)
   ↓
Layer 2: Workflow JSON (Your canvas.json_definition)
   ↓
Layer 3: PostgreSQL (canvas table)
```

**Key Insight**: Your architecture already matches N8N's pattern! You just need to build the UI layer.

---

## Implementation Roadmap

### Phase 1: Basic NDV Modal ✅ (Partially Done)

**Current File**: `static/src/n8n/overlays/overlay_manager.js`

**What You Have**:
```javascript
showNodeConfigModal(nodeData) {
    // Basic modal with name/description inputs
    // Located around line 1000-1200
}
```

**What You Need**:
```javascript
showNodeDetailView(nodeId) {
    // Full N8N-style NDV with:
    // - Three-panel layout (input/config/output)
    // - Dynamic parameter generation
    // - Real-time validation
    // - Expression editor
}
```

---

### Phase 2: Dynamic Parameter System (Next Build)

#### Step 2.1: Fetch Node Schema from Base Module

**N8N Approach** (from research):
```javascript
// N8N fetches node properties definition
const nodeType = getNodeType(node.type);
const properties = nodeType.properties; // INodeProperties[]
```

**Your Implementation**:
```javascript
// RPC call to get node schema
const schema = await this.rpc({
    model: 'n8n.simple.node',
    method: 'get_node_parameters_schema',
    args: [nodeType]  // e.g., 'n8n-nodes-base.activeCampaign'
});

// schema returns:
{
    "properties": [
        {
            "displayName": "Resource",
            "name": "resource",
            "type": "options",
            "options": [
                {"name": "Contact", "value": "contact"},
                {"name": "Deal", "value": "deal"}
            ],
            "default": "contact"
        },
        {
            "displayName": "Operation",
            "name": "operation",
            "type": "options",
            "displayOptions": {
                "show": {"resource": ["contact"]}
            },
            "options": [
                {"name": "Create", "value": "create"},
                {"name": "Update", "value": "update"}
            ],
            "default": "create"
        }
    ]
}
```

#### Step 2.2: Backend Method (Add to ai_automator_base)

**File**: `ai_automator_base/models/n8n_simple_nodes.py`

```python
class N8NSimpleNode(models.Model):
    _name = 'n8n.simple.node'

    def get_node_parameters_schema(self, node_type):
        """
        Returns parameter schema for a node type
        Similar to N8N's INodeProperties[]
        """
        node = self.search([('name', '=', node_type)], limit=1)
        if not node:
            return {'error': 'Node type not found'}

        # Parse node definition (stored in node_json or similar field)
        node_definition = json.loads(node.node_json or '{}')

        return {
            'properties': node_definition.get('properties', []),
            'credentials': node_definition.get('credentials', []),
            'displayName': node_definition.get('displayName', node_type)
        }
```

#### Step 2.3: Dynamic Form Generation (Frontend)

**File**: `static/src/n8n/overlays/overlay_manager.js`

**Add new method**:
```javascript
async renderParameterForm(nodeType, currentParameters) {
    // 1. Fetch schema
    const schema = await this.rpc({
        model: 'n8n.simple.node',
        method: 'get_node_parameters_schema',
        args: [nodeType]
    });

    // 2. Generate HTML form
    let formHTML = '<div class="parameter-list">';

    for (const property of schema.properties) {
        // Check if should display (displayOptions.show logic)
        if (!this.shouldShowParameter(property, currentParameters)) {
            continue;
        }

        // Generate input based on type
        formHTML += this.generateParameterInput(property, currentParameters);
    }

    formHTML += '</div>';
    return formHTML;
}

generateParameterInput(property, currentValues) {
    const value = currentValues[property.name] || property.default;

    switch(property.type) {
        case 'string':
            return `
                <div class="form-group">
                    <label>${property.displayName}</label>
                    <input type="text"
                           name="${property.name}"
                           value="${value}"
                           placeholder="${property.placeholder || ''}"
                           ${property.required ? 'required' : ''}>
                    <small class="help-text">${property.description || ''}</small>
                </div>
            `;

        case 'options':
            const optionsHTML = property.options.map(opt =>
                `<option value="${opt.value}" ${value === opt.value ? 'selected' : ''}>
                    ${opt.name}
                </option>`
            ).join('');

            return `
                <div class="form-group">
                    <label>${property.displayName}</label>
                    <select name="${property.name}" ${property.required ? 'required' : ''}>
                        ${optionsHTML}
                    </select>
                    <small class="help-text">${property.description || ''}</small>
                </div>
            `;

        case 'boolean':
            return `
                <div class="form-group">
                    <label>
                        <input type="checkbox"
                               name="${property.name}"
                               ${value ? 'checked' : ''}>
                        ${property.displayName}
                    </label>
                    <small class="help-text">${property.description || ''}</small>
                </div>
            `;

        case 'number':
            return `
                <div class="form-group">
                    <label>${property.displayName}</label>
                    <input type="number"
                           name="${property.name}"
                           value="${value}"
                           ${property.required ? 'required' : ''}>
                    <small class="help-text">${property.description || ''}</small>
                </div>
            `;

        default:
            return `<!-- Unsupported type: ${property.type} -->`;
    }
}

shouldShowParameter(property, currentValues) {
    if (!property.displayOptions || !property.displayOptions.show) {
        return true; // No display conditions, always show
    }

    // Check if all show conditions are met
    for (const [key, values] of Object.entries(property.displayOptions.show)) {
        const currentValue = currentValues[key];
        if (!values.includes(currentValue)) {
            return false;
        }
    }

    return true;
}
```

---

### Phase 3: Three-Panel Layout (Enhanced NDV)

**N8N Structure** (from research):
```
┌─────────────────────────────────────────────────────┐
│                NDV Dialog                           │
├──────────┬────────────────────┬─────────────────────┤
│  Input   │   Configuration    │      Output         │
│  Panel   │      Panel         │      Panel          │
│          │                    │                     │
│ (Schema/ │  ┌──────────────┐  │  (Schema/Table/     │
│  Table/  │  │ Node Name    │  │   JSON)             │
│  JSON)   │  └──────────────┘  │                     │
│          │  ┌──────────────┐  │  [Pin] [Execute]    │
│          │  │ Parameters   │  │                     │
│          │  │ • Resource   │  │  Result data...     │
│          │  │ • Operation  │  │                     │
│          │  │ • Email To   │  │                     │
│          │  └──────────────┘  │                     │
│          │                    │                     │
└──────────┴────────────────────┴─────────────────────┘
```

**Your CSS Structure**:
```css
/* Add to n8n_node_canvas_styles.css */
.ndv-wrapper {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0,0,0,0.5);
    z-index: 9999;
}

.ndv-container {
    display: grid;
    grid-template-columns: 300px 1fr 300px;
    height: 100vh;
    background: white;
    margin: 20px;
}

.ndv-panel {
    padding: 20px;
    overflow-y: auto;
    border-right: 1px solid #ddd;
}

.ndv-panel-input {
    grid-column: 1;
}

.ndv-panel-config {
    grid-column: 2;
}

.ndv-panel-output {
    grid-column: 3;
    border-right: none;
}

.ndv-resize-handle {
    width: 5px;
    cursor: col-resize;
    background: #eee;
}

.ndv-resize-handle:hover {
    background: #007bff;
}
```

---

### Phase 4: Save Parameters to Workflow JSON

**N8N Approach** (from research):
```javascript
// Updates workflow JSON in memory
workflowStore.nodes[nodeId].parameters = newParameters;
```

**Your Implementation**:
```javascript
async saveNodeParameters(nodeId, parameters) {
    // Get current workflow JSON from canvas
    const workflow = window.canvasManager.getWorkflowJSON();

    // Find node in JSON
    const node = workflow.nodes.find(n => n.id === nodeId);
    if (!node) {
        console.error('Node not found:', nodeId);
        return;
    }

    // Update parameters
    node.parameters = parameters;

    // Save back to database via RPC
    await this.rpc({
        model: 'canvas',
        method: 'write',
        args: [
            [this.canvasId],
            {
                json_definition: JSON.stringify(workflow)
            }
        ]
    });

    console.log('Node parameters saved:', nodeId, parameters);
}
```

---

## Data Structure Mapping

### N8N Workflow JSON (From Research)
```json
{
  "nodes": [
    {
      "id": "abc123",
      "name": "Send Email",
      "type": "n8n-nodes-base.gmail",
      "parameters": {
        "resource": "message",
        "operation": "send",
        "sendTo": "user@example.com"
      }
    }
  ]
}
```

### Your Current Structure (Canvas.json_definition)
```json
{
  "nodes": [
    {
      "id": "node_1",
      "name": "Create",
      "type": "n8n-nodes-base.activeCampaign",
      "position": [100, 200],
      "parameters": {
        "resource": "contact",
        "operation": "create"
      }
    }
  ],
  "connections": [...]
}
```

**Match**: ✅ Your structure already matches N8N's!

---

## Quick Start Implementation Guide

### 1. Test Your RPC Setup

**Add test endpoint** to `ai_automator_base/models/n8n_simple_nodes.py`:
```python
def test_get_schema(self):
    """Test endpoint to verify RPC works"""
    return {
        'status': 'success',
        'message': 'RPC working',
        'sample_schema': {
            'properties': [
                {
                    'displayName': 'Test Input',
                    'name': 'testInput',
                    'type': 'string',
                    'default': 'Hello World'
                }
            ]
        }
    }
```

**Call from JavaScript**:
```javascript
// In browser console or your code
const result = await odoo.__DEBUG__.services.rpc({
    model: 'n8n.simple.node',
    method: 'test_get_schema',
    args: []
});
console.log(result);
```

### 2. Enhance Existing Modal

**File**: `static/src/n8n/overlays/overlay_manager.js`

**Find** (around line 1050):
```javascript
showNodeConfigModal(nodeData) {
    // Current simple modal
}
```

**Replace with**:
```javascript
async showNodeDetailView(nodeId, nodeData) {
    // Fetch node schema
    const schema = await this.fetchNodeSchema(nodeData.type);

    // Generate dynamic form
    const formHTML = await this.renderParameterForm(
        nodeData.type,
        nodeData.parameters || {}
    );

    // Create three-panel layout
    const modalHTML = `
        <div class="ndv-wrapper">
            <div class="ndv-container">
                <div class="ndv-panel ndv-panel-input">
                    <h3>Input</h3>
                    <p>Input data will be shown here</p>
                </div>
                <div class="ndv-panel ndv-panel-config">
                    <h3>${nodeData.name}</h3>
                    ${formHTML}
                    <button class="btn-save">Save</button>
                </div>
                <div class="ndv-panel ndv-panel-output">
                    <h3>Output</h3>
                    <p>Output data will be shown here</p>
                </div>
            </div>
        </div>
    `;

    // Show modal and attach event listeners
    this.showModal(modalHTML, nodeId);
}
```

### 3. Wire Up Events

```javascript
attachNDVEventListeners(modalElement, nodeId) {
    // Save button
    const saveBtn = modalElement.querySelector('.btn-save');
    saveBtn.addEventListener('click', async () => {
        const form = modalElement.querySelector('form');
        const formData = new FormData(form);
        const parameters = Object.fromEntries(formData);

        await this.saveNodeParameters(nodeId, parameters);
        this.closeModal();
    });

    // Dynamic field changes (for displayOptions logic)
    const inputs = modalElement.querySelectorAll('input, select');
    inputs.forEach(input => {
        input.addEventListener('change', () => {
            this.refreshParameterForm(modalElement, nodeId);
        });
    });
}
```

---

## Testing Checklist

### ✅ Phase 1: Basic RPC
- [ ] Test RPC connection from JavaScript to base module
- [ ] Verify node schema can be fetched
- [ ] Check response format matches expected structure

### ✅ Phase 2: Simple Form
- [ ] Generate form for 1 string parameter
- [ ] Generate form for 1 options (dropdown) parameter
- [ ] Save parameters to workflow JSON
- [ ] Reload canvas and verify parameters persist

### ✅ Phase 3: Dynamic Display
- [ ] Implement displayOptions.show logic
- [ ] Test parameter visibility based on other field values
- [ ] Verify conditional fields appear/disappear correctly

### ✅ Phase 4: Full NDV
- [ ] Three-panel layout renders
- [ ] Panels are resizable
- [ ] Input/output panels show placeholder text
- [ ] Configuration panel shows all parameters
- [ ] Save button updates database

---

## Next Steps Priority Order

1. **Immediate**: Add `get_node_parameters_schema()` method to `n8n_simple_nodes` model
2. **Next**: Enhance `overlay_manager.js` with basic dynamic form generation
3. **Then**: Implement displayOptions.show/hide logic
4. **Finally**: Build three-panel layout with resize handles

---

## Reference Files

### Your Research Documents
- `n8n_node_detail_popup_deep_research.md` - Complete N8N analysis
- `n8n_integration_recommendations_for_ai_automator.md` - Integration guide
- `n8n_local_installation_guide.html` - Local N8N setup

### Your Current Implementation
- `static/src/n8n/overlays/overlay_manager.js` - Modal system (enhance this)
- `static/src/n8n/nodes/node_manager.js` - Node CRUD operations
- `ai_automator_base/models/n8n_simple_nodes.py` - Node definitions (add methods here)
- `ai_automator_base/models/canvas.py` - Workflow storage (json_definition)

### Key URLs
- Your Canvas: http://localhost:8069/canvas/59/nodes
- Local N8N: http://localhost:2200 (if running)
- Database: ai_automator_db @ localhost:5432

---

**Status**: Ready to implement! Your architecture perfectly matches N8N's approach. You just need to build the UI layer.

🚀 **Start with adding the RPC method to fetch node schemas, then enhance the modal!**
