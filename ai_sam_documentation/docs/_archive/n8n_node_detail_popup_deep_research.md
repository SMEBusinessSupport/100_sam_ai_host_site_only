# n8n Node Detail Popup - Deep Research Report

## Executive Summary

This document provides comprehensive research on how n8n stores and manages their "Node Detail Popup" (officially called **NDV - Node Details View** in n8n's codebase). This research was conducted for The AI Automator Odoo module development to understand n8n's architecture for node configuration and parameter management.

### 📖 Terminology Note
**NDV = Node Details View** - This is n8n's official term for the modal dialog/popup that appears when editing a node. Throughout this document, "NDV" refers to this popup interface. In your implementation, you may call it:
- "Node Detail Popup" (your original term)
- "Node Configuration Panel"
- "Node Editor Dialog"
- Or simply "NDV" (to align with n8n's codebase)

---

## Table of Contents

1. [Frontend Architecture](#frontend-architecture)
2. [NDV Component Structure](#ndv-component-structure)
3. [Data Storage Model](#data-storage-model)
4. [Workflow JSON Structure](#workflow-json-structure)
5. [Database Schema](#database-schema)
6. [State Management](#state-management)
7. [Node Parameters & Configuration](#node-parameters--configuration)
8. [Key Findings](#key-findings)
9. [Implementation Recommendations](#implementation-recommendations)

---

## 1. Frontend Architecture

### Technology Stack
- **Framework**: Vue.js 3
- **Build Tool**: Vite.js
- **State Management**: Pinia stores
- **UI Components**: Custom design system (@n8n/design-system)
- **Canvas**: Vue Flow for workflow visualization
- **Internationalization**: Vue I18n plugin

### Package Structure
```
n8n/
├── packages/
│   ├── frontend/
│   │   ├── editor-ui/              # Main editor application
│   │   │   ├── src/
│   │   │   │   ├── views/
│   │   │   │   │   └── NodeView.vue           # Main workflow canvas
│   │   │   │   ├── components/
│   │   │   │   │   ├── canvas/                 # Canvas components
│   │   │   │   │   ├── FocusPanel.vue          # Newer panel system
│   │   │   │   │   └── [NDV components]        # Node Detail View components
│   │   │   │   ├── stores/
│   │   │   │   │   ├── ndv.store.ts            # NDV state management
│   │   │   │   │   ├── focusPanel.store.ts     # Focus panel state
│   │   │   │   │   └── [other stores]
│   │   ├── @n8n/design-system/     # Design system & CSS
│   └── cli/                        # Backend/server
│       └── src/
│           └── databases/
│               └── entities/       # TypeORM entities
```

---

## 2. NDV Component Structure

### Component Hierarchy

The NDV (Node Details View) is a modal dialog component that appears when editing a node. Based on the HTML structure analysis:

```
el-dialog.ndv-wrapper
├── header (el-dialog__header)
│   └── Node title and close button
├── body (el-dialog__body)
│   ├── Back to canvas button
│   └── data-display (main NDV container)
│       ├── _modalBackground (backdrop)
│       ├── _inputPanel (left panel)
│       │   ├── run-data container
│       │   ├── header with title "Input"
│       │   ├── display modes (Schema/Table/JSON)
│       │   └── data container
│       ├── _outputPanel (right panel)
│       │   ├── run-data container
│       │   ├── header with title "Output"
│       │   ├── display modes (Schema/Table/JSON)
│       │   ├── edit/pin buttons
│       │   └── data container
│       └── _mainPanel (center panel)
│           ├── resize handles (left/right)
│           ├── drag button container
│           └── _mainPanelInner
│               └── node-settings
│                   ├── header
│                   │   ├── node icon
│                   │   ├── editable node name
│                   │   ├── Execute step button
│                   │   └── tabs (Parameters/Settings/Docs)
│                   └── node-parameters-wrapper
│                       └── parameter-input-list-wrapper
│                           └── [Dynamic parameter inputs]
```

### Key UI Components

**1. Resizable Panels**
- Left panel: Input data display
- Center panel: Node configuration
- Right panel: Output data display
- Draggable dividers for panel resizing

**2. Display Modes**
- Schema view
- Table view
- JSON view
- User preference persisted to localStorage

**3. Parameter Input Types**
Based on `INodeProperties` interface:
- Text inputs
- Dropdowns (select)
- Toggle/checkboxes
- Collections (nested parameters)
- Fixed collections (repeatable parameter groups)
- Multi-parameter groups
- Credential selectors
- Expression editors

---

## 3. Data Storage Model

### Three-Layer Storage Architecture

n8n uses a three-layer approach for storing node detail information:

#### Layer 1: Frontend State (Pinia Store)
**File**: `packages/frontend/editor-ui/src/stores/ndv.store.ts`

**Purpose**: Manages runtime state of the NDV

**Stored Data**:
- Currently active node
- Panel display modes (input/output)
- Panel sizes and positions
- Temporary parameter values during editing
- Validation states

**Persistence**:
- Display mode preferences saved to localStorage:
  - `LOCAL_STORAGE_NDV_INPUT_PANEL_DISPLAY_MODE`
  - `LOCAL_STORAGE_NDV_OUTPUT_PANEL_DISPLAY_MODE`

#### Layer 2: Workflow JSON (In-Memory & Export)
**Purpose**: Complete workflow definition including all nodes

**Structure**:
```json
{
  "name": "Workflow Name",
  "nodes": [
    {
      "id": "unique-node-id",
      "name": "Node Display Name",
      "type": "n8n-nodes-base.nodetype",
      "typeVersion": 1.0,
      "position": [x, y],
      "parameters": {
        "resource": "message",
        "operation": "send",
        "sendTo": "info@example.com",
        "subject": "Test Email",
        "message": "Hello World",
        "emailType": "html",
        "options": {
          "attachmentsUi": {
            "attachmentsBinary": [
              {
                "property": "data"
              }
            ]
          }
        }
      },
      "credentials": {
        "gmailOAuth2": {
          "id": "credential-id",
          "name": "Gmail Account"
        }
      },
      "disabled": false
    }
  ],
  "connections": {
    "Source Node Name": {
      "main": [
        [
          {
            "node": "Target Node Name",
            "type": "main",
            "index": 0
          }
        ]
      ]
    }
  },
  "active": false,
  "settings": {},
  "createdAt": "2025-10-01T00:00:00.000Z",
  "updatedAt": "2025-10-01T00:00:00.000Z",
  "tags": []
}
```

#### Layer 3: Database (Persistent Storage)
**Database**: SQLite (default), PostgreSQL, MySQL, MariaDB supported

**Primary Tables**:
- `workflow_entity`: Stores workflow definitions
- `credentials_entity`: Stores encrypted credentials
- `execution_entity`: Stores workflow execution history
- `tag_entity`: Stores workflow tags
- `shared_workflow`: Workflow sharing permissions

**Key Column (workflow_entity)**:
- `nodes`: JSON column containing the entire nodes array
- This is where the "Node Detail" configuration is permanently stored

---

## 4. Workflow JSON Structure

### Node Object Schema

Every node in the NDV is represented in the workflow JSON with this structure:

```typescript
interface INode {
  id: string;                    // Unique identifier
  name: string;                  // Display name (user editable)
  type: string;                  // Node type identifier
  typeVersion: number;           // Version of node type
  position: [number, number];    // X, Y coordinates on canvas
  parameters: INodeParameters;   // Node-specific parameters
  credentials?: INodeCredentials; // Credential references
  disabled?: boolean;            // Whether node is disabled
  notes?: string;                // User notes
  webhookId?: string;            // Webhook nodes only
  retryOnFail?: boolean;         // Retry settings
  maxTries?: number;             // Max retry attempts
  waitBetweenTries?: number;     // Wait time between retries
  alwaysOutputData?: boolean;    // Output even on failure
  executeOnce?: boolean;         // Execute only once
  continueOnFail?: boolean;      // Continue workflow on error
}
```

### Parameters Structure

The `parameters` object is **completely dynamic** and defined by each node's `INodeProperties[]` configuration:

```typescript
interface INodeProperties {
  displayName: string;           // Label shown in UI
  name: string;                  // Parameter key name
  type: string;                  // Input type (string, number, boolean, options, etc.)
  default: any;                  // Default value
  required?: boolean;            // Whether required
  description?: string;          // Help text
  placeholder?: string;          // Placeholder text
  options?: INodePropertyOptions[]; // For dropdown/select types
  displayOptions?: {             // Conditional display rules
    show?: object;
    hide?: object;
  };
  extractValue?: object;         // Data extraction rules
  validateType?: string;         // Validation rules
}
```

### Real Example (Gmail Node)

```json
{
  "id": "abc123",
  "name": "Send PDF via Gmail",
  "type": "n8n-nodes-base.gmail",
  "typeVersion": 2.1,
  "position": [500, 300],
  "parameters": {
    "resource": "message",
    "operation": "send",
    "sendTo": "sam@sme.ec",
    "subject": "Test PDF",
    "emailType": "html",
    "message": "Here's the PDF you uploaded",
    "options": {
      "attachmentsUi": {
        "attachmentsBinary": [
          {
            "property": "data"
          }
        ]
      }
    }
  },
  "credentials": {
    "gmailOAuth2": {
      "id": "8",
      "name": "Gmail OAuth2 account"
    }
  }
}
```

---

## 5. Database Schema

### workflow_entity Table

While I couldn't directly access the TypeORM entity definition, based on research and database analysis:

**Key Columns**:
```sql
CREATE TABLE workflow_entity (
  id INTEGER PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  active BOOLEAN DEFAULT 0,
  nodes TEXT,                    -- JSON array of nodes
  connections TEXT,              -- JSON object of connections
  settings TEXT,                 -- JSON workflow settings
  staticData TEXT,               -- JSON static workflow data
  tags TEXT,                     -- JSON array of tag IDs
  createdAt DATETIME,
  updatedAt DATETIME,
  versionId VARCHAR(36)          -- UUID for versioning
);
```

**Critical Detail**: The `nodes` column stores the **entire nodes array as JSON**, including all parameters configured in the NDV.

### Data Flow

```
User edits in NDV
  ↓
Pinia Store (ndv.store.ts) - Temporary state
  ↓
Workflow JSON updated in memory
  ↓
Auto-save / Manual save triggers
  ↓
POST to backend API
  ↓
TypeORM WorkflowEntity
  ↓
SQLite database.sqlite
  ↓
workflow_entity.nodes column (JSON)
```

---

## 6. State Management

### NDV Store (ndv.store.ts)

The NDV Pinia store manages the Node Detail View state:

**Key Responsibilities**:
1. **Active Node Tracking**: Which node is currently open in NDV
2. **Panel State**: Input/output panel display modes
3. **Display Mode Persistence**: Saves user preferences to localStorage
4. **Execution State**: Whether node is executing, has results
5. **Validation State**: Parameter validation errors
6. **Keyboard Shortcuts**: Registers/unregisters keyboard listeners when NDV opens/closes

**Store Actions** (inferred):
- `openNDV(nodeId)`: Opens NDV for a specific node
- `closeNDV()`: Closes NDV and cleans up
- `updateParameter(paramName, value)`: Updates a node parameter
- `setDisplayMode(panel, mode)`: Changes display mode (schema/table/json)
- `executeNode()`: Triggers node execution

**Local Storage Keys**:
- `LOCAL_STORAGE_NDV_INPUT_PANEL_DISPLAY_MODE`: 'schema' | 'table' | 'json'
- `LOCAL_STORAGE_NDV_OUTPUT_PANEL_DISPLAY_MODE`: 'schema' | 'table' | 'json'

### Integration with Workflow Store

The NDV store works in conjunction with the main workflow store:

```
workflowStore.nodes[nodeId].parameters ← ndv.store updates this
```

When a parameter is changed in NDV:
1. NDV store receives the change
2. Validates the input
3. Updates the workflow store's node parameters
4. Triggers workflow dirty state (unsaved changes)
5. May trigger auto-save timer

---

## 7. Node Parameters & Configuration

### Parameter Definition System

Each node type defines its parameters using `INodeProperties[]`:

```typescript
// Example from a custom node
properties: [
  {
    displayName: 'Resource',
    name: 'resource',
    type: 'options',
    options: [
      { name: 'Message', value: 'message' },
      { name: 'Draft', value: 'draft' }
    ],
    default: 'message'
  },
  {
    displayName: 'Operation',
    name: 'operation',
    type: 'options',
    displayOptions: {
      show: {
        resource: ['message']
      }
    },
    options: [
      { name: 'Send', value: 'send' },
      { name: 'Get', value: 'get' }
    ],
    default: 'send'
  },
  {
    displayName: 'To',
    name: 'sendTo',
    type: 'string',
    displayOptions: {
      show: {
        resource: ['message'],
        operation: ['send']
      }
    },
    default: '',
    required: true,
    placeholder: 'info@example.com',
    description: 'Email address to send to'
  }
]
```

### Parameter Types

| Type | Description | UI Component |
|------|-------------|--------------|
| string | Text input | `<el-input>` |
| number | Numeric input | `<el-input type="number">` |
| boolean | Checkbox/toggle | `<el-switch>` |
| options | Dropdown select | `<el-select>` |
| multiOptions | Multi-select | `<el-select multiple>` |
| collection | Nested parameters | Collapsible section |
| fixedCollection | Repeatable param groups | Add/remove items UI |
| json | JSON editor | Code editor with validation |
| string (with rows) | Textarea | `<el-input type="textarea">` |
| color | Color picker | Color selector |
| dateTime | Date/time picker | `<el-date-picker>` |
| credentials | Credential selector | Special credential dropdown |

### Expression Support

All parameter inputs support **expression mode** via a toggle button:
- **Fixed mode**: Direct value input
- **Expression mode**: JavaScript expressions with access to:
  - `$input`: Input data from previous node
  - `$json`: Current item JSON
  - `$node`: Node metadata
  - `$workflow`: Workflow metadata
  - `$env`: Environment variables
  - Custom functions and libraries

### Conditional Display

Parameters can show/hide based on other parameter values:

```typescript
displayOptions: {
  show: {
    resource: ['message'],
    operation: ['send']
  },
  hide: {
    useCustomOptions: [true]
  }
}
```

This creates a dynamic UI that adapts based on user selections.

---

## 8. Key Findings

### How n8n Stores Node Detail Popup Data

**Answer**: n8n uses a **three-layer storage approach**:

1. **Runtime State (Pinia Store)**: Temporary NDV state in `ndv.store.ts`
2. **Workflow JSON (In-Memory)**: Complete node configuration in the workflow's nodes array
3. **Database (Persistent)**: JSON stored in `workflow_entity.nodes` column

### Node Configuration Storage Format

Node configurations are stored as **plain JSON objects** with:
- Static properties (id, name, type, position)
- Dynamic `parameters` object (structure defined by node type)
- Credential references (ID and name, not actual credentials)
- Execution settings (optional)

### NDV Component Architecture

The NDV is a **Vue.js modal dialog** with:
- Three resizable panels (input/output/configuration)
- Dynamic parameter inputs based on `INodeProperties`
- Real-time validation
- Expression editor support
- Multiple display modes for data (schema/table/json)

### Data Persistence Strategy

```
Edit → Pinia Store → Workflow JSON → API Call → Database
```

- Changes are tracked in-memory first
- Auto-save or manual save triggers persistence
- Database stores complete workflow JSON
- No separate "node configuration" table - it's embedded in workflow

---

## 9. Implementation Recommendations

### For Odoo Module Development

Based on this research, here are recommendations for implementing similar functionality in The AI Automator:

#### 1. Data Model Structure

**Recommended Approach**:
```python
class WorkflowNode(models.Model):
    _name = 'ai.automator.workflow.node'

    workflow_id = fields.Many2one('ai.automator.workflow')
    node_id = fields.Char(required=True)  # Unique ID
    name = fields.Char(required=True)
    node_type = fields.Char(required=True)
    position_x = fields.Float()
    position_y = fields.Float()
    parameters = fields.Text()  # JSON serialized
    credentials = fields.Text()  # JSON serialized credential refs
    disabled = fields.Boolean(default=False)
```

**Alternative Approach** (more like n8n):
```python
class Workflow(models.Model):
    _name = 'ai.automator.workflow'

    name = fields.Char()
    nodes = fields.Text()  # Entire nodes array as JSON
    connections = fields.Text()  # Connections as JSON
    active = fields.Boolean()
```

#### 2. Frontend Component Structure

**Vue.js Components**:
```
WorkflowCanvas.vue (main canvas)
  ├── NodeDetailDialog.vue (modal similar to NDV)
  │   ├── NodeDetailHeader.vue
  │   ├── NodeDetailTabs.vue
  │   ├── NodeParametersList.vue
  │   │   ├── ParameterInput.vue (generic)
  │   │   ├── ParameterString.vue
  │   │   ├── ParameterSelect.vue
  │   │   ├── ParameterCollection.vue
  │   │   └── ...
  │   ├── NodeInputPanel.vue
  │   └── NodeOutputPanel.vue
  └── Canvas rendering components
```

#### 3. State Management

Use Pinia (or Vuex) with these stores:
- `workflowStore`: Main workflow state
- `nodeDetailStore`: NDV state (active node, parameters being edited)
- `nodeTypesStore`: Available node types and their property definitions
- `credentialsStore`: Available credentials

#### 4. Parameter Definition System

Create a Python-based parameter definition system:

```python
class NodeType(models.Model):
    _name = 'ai.automator.node.type'

    name = fields.Char()
    properties = fields.Text()  # JSON array of INodeProperties-like objects

def get_properties_schema(self):
    return json.loads(self.properties or '[]')
```

#### 5. JSON Schema for Node Parameters

Define a JSON schema similar to n8n's `INodeProperties`:

```json
{
  "displayName": "Email To",
  "name": "sendTo",
  "type": "string",
  "default": "",
  "required": true,
  "placeholder": "info@example.com",
  "description": "Email address of the recipient",
  "displayOptions": {
    "show": {
      "operation": ["send"]
    }
  }
}
```

#### 6. API Endpoints

```python
# In Odoo controller
@http.route('/ai_automator/workflow/<int:workflow_id>/node/<string:node_id>',
            type='json', auth='user')
def update_node_parameters(self, workflow_id, node_id, **kwargs):
    # Update node parameters
    # Return updated workflow JSON
    pass

@http.route('/ai_automator/node/<int:node_id>/execute',
            type='json', auth='user')
def execute_node(self, node_id, **kwargs):
    # Execute single node for testing
    # Return execution result
    pass
```

#### 7. Database Storage Strategy

**Option A: n8n-style (Single JSON column)**
```sql
-- Simpler, more flexible
CREATE TABLE workflow (
    id SERIAL,
    name VARCHAR,
    nodes JSONB,  -- PostgreSQL JSONB for better querying
    connections JSONB
);
```

**Option B: Normalized (Separate node records)**
```sql
-- Better for complex queries and relationships
CREATE TABLE workflow_node (
    id SERIAL,
    workflow_id INTEGER,
    node_id VARCHAR,
    parameters JSONB
);
```

**Recommendation**: Use Option A (n8n-style) for:
- Simpler import/export
- Faster workflow loading
- Easier version control
- Matches n8n's approach for easier integration

#### 8. Expression Support

Implement expression evaluation similar to n8n:
- Use Python's `ast.literal_eval()` for safe evaluation
- Provide context variables ($input, $json, etc.)
- Create expression editor component with syntax highlighting

#### 9. Credential Management

**Never store credentials in workflow JSON**:
```json
{
  "credentials": {
    "gmailOAuth2": {
      "id": "credential-record-id",
      "name": "Gmail Account"
    }
  }
}
```

Store actual credentials encrypted in separate table:
```python
class Credential(models.Model):
    _name = 'ai.automator.credential'

    name = fields.Char()
    credential_type = fields.Char()
    encrypted_data = fields.Binary()  # Encrypted JSON
```

#### 10. UI/UX Considerations

- **Use Vue.js 3** for consistency with n8n research
- **Implement resizable panels** using `vue-resizable` or similar
- **Add multiple display modes** (schema/table/json) for data viewing
- **Support expression mode** for all text inputs
- **Auto-save** workflow changes with debouncing
- **Real-time validation** of parameters
- **Keyboard shortcuts** (Ctrl+S to save, Escape to close)

---

## Conclusion

n8n's Node Detail View is a sophisticated system that balances:
- **Flexibility**: Dynamic parameter system based on node type definitions
- **Simplicity**: Single JSON storage for complete workflow state
- **Performance**: In-memory state management with Pinia
- **User Experience**: Rich UI with multiple data views and expression support

The key insight is that **node configuration is not stored separately** - it's embedded within the workflow's JSON structure, both in memory and in the database. This makes workflows highly portable and simplifies the data model.

For The AI Automator Odoo module, adopting a similar architecture would provide:
- Easy integration with n8n workflows (import/export)
- Flexible node parameter system
- Clear separation between runtime state and persistent storage
- Scalable architecture for adding new node types

---

## References

- n8n GitHub Repository: https://github.com/n8n-io/n8n
- n8n Documentation: https://docs.n8n.io/
- n8n Community Forum: https://community.n8n.io/
- Local n8n Installation: http://localhost:2200
- n8n Version: 1.108.2

---

**Document Created**: October 1, 2025
**Research Conducted By**: Claude Code AI Assistant
**For Project**: The AI Automator - Phase 3 Development
**Local n8n Instance**: Docker container `n8n-existing` on localhost:2200
