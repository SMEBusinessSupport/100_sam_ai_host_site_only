# N8N Node Detail View (NDV) - UI Specification

**Date**: 2025-10-01
**Source**: N8N Screenshot Analysis
**Target**: AI Automator Odoo Module

---

## Screenshot Analysis: "Send PDF via Gmail" Node

### Visual Structure

```
┌────────────────────────────────────────────────────────────────────────────┐
│  ← Back to canvas                                  [Send PDF via Gmail] [X]│
├──────────────────┬─────────────────────────────────┬──────────────────────┤
│                  │                                 │                      │
│   INPUT          │      PARAMETERS                 │      OUTPUT          │
│                  │                                 │                      │
│ No input data    │  [Parameters] [Settings] [Docs] │  Execute this node   │
│ yet              │                                 │  to view data        │
│                  │  Credential to connect with     │  or set mock data    │
│ [Execute         │  [Select Credential      ▼] ⚠  │                      │
│  previous nodes] │                                 │                      │
│                  │  Resource                       │                      │
│ (From earliest   │  [Message                ▼]     │                      │
│  node that needs │                                 │                      │
│  it ⓘ)           │  Operation                      │                      │
│                  │  [Send                   ▼]     │                      │
│                  │                                 │                      │
│                  │  To                             │                      │
│                  │  [sam@sme.ec            ]       │                      │
│                  │                                 │                      │
│                  │  Subject                        │                      │
│                  │  [Test PDF              ]       │                      │
│                  │                                 │                      │
│                  │  Email Type                     │                      │
│                  │  [HTML                   ▼]     │                      │
│                  │                                 │                      │
│                  │  Message                        │                      │
│                  │  [Here's the PDF you uploaded]  │                      │
│                  │                                 │                      │
│                  │  Options                        │                      │
│                  │  ▼ Attachments                  │                      │
│                  │    Attachment Field Name        │                      │
│                  │    [data                ]       │                      │
│                  │    The name of the field with   │                      │
│                  │    the attachment in the node   │                      │
│                  │    input                        │                      │
│                  │    [Add Attachment]             │                      │
│                  │  [Add option             ▼]     │                      │
│                  │                                 │                      │
│                  │  ⚙ I wish this node would...    │                      │
└──────────────────┴─────────────────────────────────┴──────────────────────┘
```

---

## Key UI Features Identified

### 1. Three-Panel Layout
- **Left Panel (INPUT)**: Shows incoming data from previous nodes
- **Center Panel (PARAMETERS)**: Node configuration form
- **Right Panel (OUTPUT)**: Shows node execution results

### 2. Panel Styling
```css
/* Gray background panels */
background: #f5f5f5;
border-right: 1px solid #ddd;

/* Center panel (white) */
background: #ffffff;
padding: 20px;
```

### 3. Header Features
- **Back to canvas** button (top-left)
- **Node title** with icon (centered)
- **Close button** (top-right, X)

### 4. Tab System
- **Parameters** (active, red underline)
- **Settings**
- **Docs** (with external link icon)

### 5. Form Elements

#### Credential Selector
```html
<div class="form-group">
    <label>Credential to connect with</label>
    <select class="credential-select">
        <option>Select Credential</option>
    </select>
    <span class="warning-icon">⚠</span>
</div>
```

#### Dropdown Fields
```html
<div class="form-group">
    <label>Resource</label>
    <select name="resource">
        <option value="message">Message</option>
    </select>
</div>
```

#### Text Inputs
```html
<div class="form-group">
    <label>To</label>
    <input type="email" value="sam@sme.ec">
</div>
```

#### Collapsible Sections (Options)
```html
<div class="collapsible-section">
    <div class="section-header">
        <span class="collapse-icon">▼</span>
        Options
    </div>
    <div class="section-content">
        <!-- Nested parameters -->
    </div>
</div>
```

### 6. Special Components

#### "Add Attachment" Button
```html
<button class="add-item-btn">Add Attachment</button>
```

#### "Add option" Dropdown
```html
<select class="add-option-select">
    <option>Add option</option>
    <option value="cc">CC</option>
    <option value="bcc">BCC</option>
</select>
```

#### Help Text
```html
<small class="help-text">
    The name of the field with the attachment in the node input
</small>
```

### 7. Input Panel Features
- **Empty state**: "No input data yet"
- **Action button**: "Execute previous nodes"
- **Info text**: "(From the earliest node that needs it ⓘ)"

### 8. Output Panel Features
- **Empty state**: "Execute this node to view data"
- **Alternative**: "or set mock data" (link)

---

## Color Scheme

```css
:root {
    /* Primary Colors */
    --ndv-bg-gray: #f5f5f5;
    --ndv-bg-white: #ffffff;
    --ndv-border: #dddddd;
    --ndv-text: #333333;
    --ndv-text-muted: #666666;

    /* Accent Colors */
    --ndv-primary: #ff6d5a;  /* Red/coral for active tab */
    --ndv-warning: #ff9500;  /* Orange for warnings */
    --ndv-link: #007bff;     /* Blue for links */

    /* Input Elements */
    --input-border: #d1d5db;
    --input-focus: #007bff;
    --input-bg: #ffffff;
}
```

---

## CSS Implementation

### Base Structure

```css
/* NDV Wrapper - Full screen overlay */
.ndv-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.5);
    z-index: 10000;
    display: flex;
    align-items: center;
    justify-content: center;
}

/* NDV Container - The dialog box */
.ndv-container {
    width: 90vw;
    height: 90vh;
    background: white;
    border-radius: 8px;
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
    display: flex;
    flex-direction: column;
}

/* NDV Header */
.ndv-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 16px 20px;
    border-bottom: 1px solid var(--ndv-border);
}

.ndv-back-btn {
    display: flex;
    align-items: center;
    gap: 8px;
    color: var(--ndv-text-muted);
    cursor: pointer;
    font-size: 14px;
}

.ndv-back-btn:hover {
    color: var(--ndv-text);
}

.ndv-title {
    display: flex;
    align-items: center;
    gap: 12px;
    font-size: 16px;
    font-weight: 500;
}

.ndv-close-btn {
    width: 32px;
    height: 32px;
    border-radius: 4px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    color: var(--ndv-text-muted);
}

.ndv-close-btn:hover {
    background: var(--ndv-bg-gray);
    color: var(--ndv-text);
}

/* Three-Panel Layout */
.ndv-body {
    flex: 1;
    display: grid;
    grid-template-columns: 300px 1fr 300px;
    overflow: hidden;
}

.ndv-panel {
    display: flex;
    flex-direction: column;
    overflow-y: auto;
}

.ndv-panel-input {
    background: var(--ndv-bg-gray);
    border-right: 1px solid var(--ndv-border);
    padding: 20px;
}

.ndv-panel-parameters {
    background: var(--ndv-bg-white);
    padding: 0;
}

.ndv-panel-output {
    background: var(--ndv-bg-gray);
    border-left: 1px solid var(--ndv-border);
    padding: 20px;
}

/* Resize Handles */
.ndv-resize-handle {
    width: 5px;
    cursor: col-resize;
    background: transparent;
    position: absolute;
    top: 0;
    bottom: 0;
}

.ndv-resize-handle:hover {
    background: var(--ndv-primary);
}

/* Tab System */
.ndv-tabs {
    display: flex;
    gap: 0;
    border-bottom: 1px solid var(--ndv-border);
    padding: 0 20px;
}

.ndv-tab {
    padding: 12px 16px;
    cursor: pointer;
    color: var(--ndv-text-muted);
    border-bottom: 2px solid transparent;
    transition: all 0.2s;
}

.ndv-tab:hover {
    color: var(--ndv-text);
}

.ndv-tab.active {
    color: var(--ndv-primary);
    border-bottom-color: var(--ndv-primary);
}

/* Parameters Form */
.ndv-parameters-content {
    padding: 20px;
}

.ndv-form-group {
    margin-bottom: 20px;
}

.ndv-form-label {
    display: block;
    margin-bottom: 6px;
    font-size: 14px;
    font-weight: 500;
    color: var(--ndv-text);
}

.ndv-form-input,
.ndv-form-select {
    width: 100%;
    padding: 8px 12px;
    border: 1px solid var(--input-border);
    border-radius: 4px;
    font-size: 14px;
    background: var(--input-bg);
    transition: border-color 0.2s;
}

.ndv-form-input:focus,
.ndv-form-select:focus {
    outline: none;
    border-color: var(--input-focus);
    box-shadow: 0 0 0 3px rgba(0, 123, 255, 0.1);
}

.ndv-help-text {
    display: block;
    margin-top: 4px;
    font-size: 12px;
    color: var(--ndv-text-muted);
    line-height: 1.4;
}

/* Credential Warning */
.ndv-credential-warning {
    display: inline-flex;
    align-items: center;
    margin-left: 8px;
    color: var(--ndv-warning);
    font-size: 16px;
}

/* Collapsible Sections */
.ndv-collapsible {
    margin-bottom: 16px;
}

.ndv-collapsible-header {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 12px;
    background: var(--ndv-bg-gray);
    border-radius: 4px;
    cursor: pointer;
    font-weight: 500;
}

.ndv-collapsible-icon {
    transition: transform 0.2s;
}

.ndv-collapsible.collapsed .ndv-collapsible-icon {
    transform: rotate(-90deg);
}

.ndv-collapsible-content {
    padding: 16px 12px;
    border-left: 2px solid var(--ndv-border);
    margin-left: 12px;
}

.ndv-collapsible.collapsed .ndv-collapsible-content {
    display: none;
}

/* Add Item Button */
.ndv-add-btn {
    padding: 8px 16px;
    background: transparent;
    border: 1px dashed var(--ndv-border);
    border-radius: 4px;
    color: var(--ndv-text-muted);
    cursor: pointer;
    font-size: 14px;
    transition: all 0.2s;
}

.ndv-add-btn:hover {
    border-color: var(--ndv-primary);
    color: var(--ndv-primary);
    border-style: solid;
}

/* Add Option Select */
.ndv-add-option {
    width: 100%;
    padding: 8px 12px;
    border: 1px dashed var(--ndv-border);
    border-radius: 4px;
    background: white;
    cursor: pointer;
    color: var(--ndv-text-muted);
}

.ndv-add-option:hover {
    border-color: var(--ndv-primary);
    border-style: solid;
}

/* Empty States */
.ndv-empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 200px;
    text-align: center;
    color: var(--ndv-text-muted);
}

.ndv-empty-state-text {
    font-size: 14px;
    margin-bottom: 16px;
}

.ndv-execute-btn {
    padding: 10px 20px;
    background: var(--ndv-bg-white);
    border: 1px solid var(--ndv-border);
    border-radius: 4px;
    cursor: pointer;
    font-size: 14px;
    transition: all 0.2s;
}

.ndv-execute-btn:hover {
    background: var(--ndv-bg-gray);
}

/* Footer Feedback */
.ndv-footer-feedback {
    padding: 12px 20px;
    border-top: 1px solid var(--ndv-border);
    background: var(--ndv-bg-gray);
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 12px;
    color: var(--ndv-text-muted);
}

.ndv-footer-icon {
    font-size: 16px;
}
```

---

## HTML Structure

```html
<div class="ndv-overlay">
    <div class="ndv-container">
        <!-- Header -->
        <div class="ndv-header">
            <div class="ndv-back-btn">
                <span>←</span>
                <span>Back to canvas</span>
            </div>
            <div class="ndv-title">
                <img src="gmail-icon.svg" width="24" height="24">
                <span>Send PDF via Gmail</span>
            </div>
            <div class="ndv-close-btn">✕</div>
        </div>

        <!-- Body: Three Panels -->
        <div class="ndv-body">
            <!-- Left Panel: Input -->
            <div class="ndv-panel ndv-panel-input">
                <h3>INPUT</h3>
                <div class="ndv-empty-state">
                    <div class="ndv-empty-state-text">No input data yet</div>
                    <button class="ndv-execute-btn">Execute previous nodes</button>
                    <small>(From the earliest node that needs it ⓘ)</small>
                </div>
            </div>

            <!-- Center Panel: Parameters -->
            <div class="ndv-panel ndv-panel-parameters">
                <!-- Tabs -->
                <div class="ndv-tabs">
                    <div class="ndv-tab active">Parameters</div>
                    <div class="ndv-tab">Settings</div>
                    <div class="ndv-tab">Docs 🔗</div>
                </div>

                <!-- Parameters Content -->
                <div class="ndv-parameters-content">
                    <!-- Credential -->
                    <div class="ndv-form-group">
                        <label class="ndv-form-label">
                            Credential to connect with
                            <span class="ndv-credential-warning">⚠</span>
                        </label>
                        <select class="ndv-form-select">
                            <option>Select Credential</option>
                        </select>
                    </div>

                    <!-- Resource -->
                    <div class="ndv-form-group">
                        <label class="ndv-form-label">Resource</label>
                        <select class="ndv-form-select" name="resource">
                            <option value="message">Message</option>
                        </select>
                    </div>

                    <!-- Operation -->
                    <div class="ndv-form-group">
                        <label class="ndv-form-label">Operation</label>
                        <select class="ndv-form-select" name="operation">
                            <option value="send">Send</option>
                        </select>
                    </div>

                    <!-- To -->
                    <div class="ndv-form-group">
                        <label class="ndv-form-label">To</label>
                        <input type="email" class="ndv-form-input"
                               value="sam@sme.ec">
                    </div>

                    <!-- Subject -->
                    <div class="ndv-form-group">
                        <label class="ndv-form-label">Subject</label>
                        <input type="text" class="ndv-form-input"
                               value="Test PDF">
                    </div>

                    <!-- Email Type -->
                    <div class="ndv-form-group">
                        <label class="ndv-form-label">Email Type</label>
                        <select class="ndv-form-select" name="emailType">
                            <option value="html">HTML</option>
                            <option value="text">Text</option>
                        </select>
                    </div>

                    <!-- Message -->
                    <div class="ndv-form-group">
                        <label class="ndv-form-label">Message</label>
                        <textarea class="ndv-form-input" rows="3">Here's the PDF you uploaded</textarea>
                    </div>

                    <!-- Options (Collapsible) -->
                    <div class="ndv-collapsible">
                        <div class="ndv-collapsible-header">
                            <span class="ndv-collapsible-icon">▼</span>
                            <span>Options</span>
                        </div>
                        <div class="ndv-collapsible-content">
                            <!-- Attachments -->
                            <div class="ndv-collapsible">
                                <div class="ndv-collapsible-header">
                                    <span class="ndv-collapsible-icon">▼</span>
                                    <span>Attachments</span>
                                </div>
                                <div class="ndv-collapsible-content">
                                    <div class="ndv-form-group">
                                        <label class="ndv-form-label">Attachment Field Name</label>
                                        <input type="text" class="ndv-form-input" value="data">
                                        <small class="ndv-help-text">
                                            The name of the field with the attachment in the node input
                                        </small>
                                    </div>
                                    <button class="ndv-add-btn">Add Attachment</button>
                                </div>
                            </div>

                            <!-- Add Option -->
                            <select class="ndv-add-option">
                                <option>Add option</option>
                                <option value="cc">CC</option>
                                <option value="bcc">BCC</option>
                            </select>
                        </div>
                    </div>
                </div>

                <!-- Footer Feedback -->
                <div class="ndv-footer-feedback">
                    <span class="ndv-footer-icon">⚙</span>
                    <span>I wish this node would...</span>
                </div>
            </div>

            <!-- Right Panel: Output -->
            <div class="ndv-panel ndv-panel-output">
                <h3>OUTPUT</h3>
                <div class="ndv-empty-state">
                    <div class="ndv-empty-state-text">
                        Execute this node to view data<br>
                        or <a href="#">set mock data</a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
```

---

## JavaScript Implementation

```javascript
class NodeDetailView {
    constructor() {
        this.currentNode = null;
        this.overlay = null;
    }

    async open(nodeId, nodeData) {
        this.currentNode = nodeData;

        // Fetch node schema
        const schema = await this.fetchNodeSchema(nodeData.type);

        // Build HTML
        const html = this.buildNDVHTML(nodeData, schema);

        // Create overlay
        this.overlay = document.createElement('div');
        this.overlay.innerHTML = html;
        document.body.appendChild(this.overlay);

        // Attach event listeners
        this.attachEventListeners();
    }

    buildNDVHTML(nodeData, schema) {
        return `
            <div class="ndv-overlay">
                <div class="ndv-container">
                    ${this.buildHeader(nodeData)}
                    ${this.buildBody(nodeData, schema)}
                </div>
            </div>
        `;
    }

    buildHeader(nodeData) {
        return `
            <div class="ndv-header">
                <div class="ndv-back-btn" data-action="close">
                    <span>←</span>
                    <span>Back to canvas</span>
                </div>
                <div class="ndv-title">
                    <img src="${this.getNodeIcon(nodeData.type)}" width="24" height="24">
                    <span>${nodeData.name}</span>
                </div>
                <div class="ndv-close-btn" data-action="close">✕</div>
            </div>
        `;
    }

    buildBody(nodeData, schema) {
        return `
            <div class="ndv-body">
                ${this.buildInputPanel()}
                ${this.buildParametersPanel(nodeData, schema)}
                ${this.buildOutputPanel()}
            </div>
        `;
    }

    buildInputPanel() {
        return `
            <div class="ndv-panel ndv-panel-input">
                <h3>INPUT</h3>
                <div class="ndv-empty-state">
                    <div class="ndv-empty-state-text">No input data yet</div>
                    <button class="ndv-execute-btn">Execute previous nodes</button>
                    <small>(From the earliest node that needs it ⓘ)</small>
                </div>
            </div>
        `;
    }

    buildParametersPanel(nodeData, schema) {
        return `
            <div class="ndv-panel ndv-panel-parameters">
                <div class="ndv-tabs">
                    <div class="ndv-tab active" data-tab="parameters">Parameters</div>
                    <div class="ndv-tab" data-tab="settings">Settings</div>
                    <div class="ndv-tab" data-tab="docs">Docs 🔗</div>
                </div>
                <div class="ndv-parameters-content">
                    ${this.buildParametersForm(schema, nodeData.parameters)}
                </div>
                <div class="ndv-footer-feedback">
                    <span class="ndv-footer-icon">⚙</span>
                    <span>I wish this node would...</span>
                </div>
            </div>
        `;
    }

    buildOutputPanel() {
        return `
            <div class="ndv-panel ndv-panel-output">
                <h3>OUTPUT</h3>
                <div class="ndv-empty-state">
                    <div class="ndv-empty-state-text">
                        Execute this node to view data<br>
                        or <a href="#">set mock data</a>
                    </div>
                </div>
            </div>
        `;
    }

    buildParametersForm(schema, currentParams) {
        let html = '';
        for (const property of schema.properties) {
            html += this.buildFormField(property, currentParams);
        }
        return html;
    }

    buildFormField(property, currentParams) {
        const value = currentParams[property.name] || property.default;

        switch(property.type) {
            case 'string':
                return `
                    <div class="ndv-form-group">
                        <label class="ndv-form-label">${property.displayName}</label>
                        <input type="text"
                               class="ndv-form-input"
                               name="${property.name}"
                               value="${value || ''}">
                        ${property.description ? `<small class="ndv-help-text">${property.description}</small>` : ''}
                    </div>
                `;

            case 'options':
                const options = property.options.map(opt =>
                    `<option value="${opt.value}" ${value === opt.value ? 'selected' : ''}>
                        ${opt.name}
                    </option>`
                ).join('');

                return `
                    <div class="ndv-form-group">
                        <label class="ndv-form-label">${property.displayName}</label>
                        <select class="ndv-form-select" name="${property.name}">
                            ${options}
                        </select>
                    </div>
                `;

            default:
                return '';
        }
    }

    attachEventListeners() {
        // Close button
        this.overlay.querySelectorAll('[data-action="close"]').forEach(btn => {
            btn.addEventListener('click', () => this.close());
        });

        // Save on change
        this.overlay.querySelectorAll('input, select, textarea').forEach(input => {
            input.addEventListener('change', () => this.saveParameters());
        });
    }

    async saveParameters() {
        // Collect form data
        const form = this.overlay.querySelector('.ndv-parameters-content');
        const formData = new FormData(form);
        const parameters = Object.fromEntries(formData);

        // Save via RPC
        await window.canvasManager.rpc({
            model: 'canvas',
            method: 'update_node_parameters',
            args: [this.currentNode.id, parameters]
        });

        console.log('Parameters saved:', parameters);
    }

    close() {
        if (this.overlay) {
            this.overlay.remove();
            this.overlay = null;
        }
    }

    async fetchNodeSchema(nodeType) {
        return await window.canvasManager.rpc({
            model: 'n8n.simple.node',
            method: 'get_node_parameters_schema',
            args: [nodeType]
        });
    }

    getNodeIcon(nodeType) {
        // Return icon path based on node type
        return '/path/to/node/icons/' + nodeType + '.svg';
    }
}

// Initialize
window.nodeDetailView = new NodeDetailView();
```

---

## Integration with Your Canvas

```javascript
// In your node_manager.js or overlay_manager.js

// When user double-clicks a node:
function onNodeDoubleClick(nodeId) {
    const nodeData = window.canvasManager.getNode(nodeId);
    window.nodeDetailView.open(nodeId, nodeData);
}
```

---

## Next Steps

1. **Add CSS file**: Create `ndv_styles.css` with the styles above
2. **Add JavaScript**: Create `node_detail_view.js` with the NDV class
3. **Test with simple node**: Start with a node that has 2-3 parameters
4. **Add backend method**: Implement `get_node_parameters_schema()` in base module
5. **Enhance gradually**: Add collapsible sections, validation, expression editor

---

## Key Differences from Current Modal

| Current Modal | New NDV |
|--------------|---------|
| Single panel | Three panels (input/config/output) |
| Basic inputs | Dynamic form generation |
| No data preview | Shows input/output data |
| Simple styling | Professional N8N styling |
| No tabs | Parameters/Settings/Docs tabs |
| No collapsible sections | Collapsible Options |

---

**Status**: Specification complete. Ready to implement! 🚀
