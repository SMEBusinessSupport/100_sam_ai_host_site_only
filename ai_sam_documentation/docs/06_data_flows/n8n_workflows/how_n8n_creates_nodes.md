# How n8n Creates Nodes: Complete Technical Guide

## Table of Contents
1. [Overview](#overview)
2. [Three-Tier Architecture](#three-tier-architecture)
3. [Node Creation Flow: From Click to Canvas](#node-creation-flow)
4. [Node Type Resolution System](#node-type-resolution-system)
5. [Metadata vs Implementation](#metadata-vs-implementation)
6. [Code Snippet Generation](#code-snippet-generation)
7. [Reverse Engineering for Odoo](#reverse-engineering-for-odoo)
8. [Critical File References](#critical-file-references)

---

## Overview

n8n uses a sophisticated **three-tier lazy-loading architecture** to manage node creation. When you add a node to the canvas, **no code is pulled or executed** - only metadata is used. The actual implementation code is loaded on-demand during workflow execution.

### Key Principle
```
Node Type String → Metadata Lookup → On-Demand Property Loading → Runtime Execution
```

Example:
```json
{
  "type": "n8n-nodes-base.activeCampaignTool",
  "typeVersion": 1,
  "position": [992, 528],
  "id": "9bc218f4-f329-41fe-a3d5-d27a5e28e5a7",
  "name": "Create a contact in ActiveCampaign1"
}
```

This JSON is a **workflow definition**, not executable code. It's a pointer to metadata.

---

## Three-Tier Architecture

### Tier 1: Metadata Layer (Initial Load)
**Purpose:** Fast initial load and node browsing
**File:** `/types/nodes.json` (static, pre-generated)
**Size:** ~100KB for hundreds of nodes
**Contains:**
- Node type name and display name
- Icon paths
- Input/output connection types
- Parameter structure (but not values)
- Group/category
- `usableAsTool` flag

**Generation Process:**
```typescript
// Location: packages/cli/src/services/frontend.service.ts:296-305
async generateTypes() {
  const { credentials, nodes } = this.loadNodesAndCredentials.types;

  // Write nodes.json - contains ALL node type metadata
  this.writeStaticJSON('nodes', nodes);
  this.writeStaticJSON('credentials', credentials);
}
```

**Frontend Loading:**
```typescript
// Location: packages/frontend/editor-ui/src/stores/nodeTypes.store.ts:339-345
const getNodeTypes = async () => {
  const nodeTypes = await nodeTypesApi.getNodeTypes(rootStore.baseUrl);
  if (nodeTypes.length) {
    setNodeTypes(nodeTypes);  // Store in Vuex/Pinia store
  }
};
```

### Tier 2: Property Layer (On-Demand)
**Purpose:** Full parameter definitions when editing a node
**Endpoint:** `POST /node-types` (dynamic API call)
**Triggered:** When user opens node settings panel
**Contains:**
- Complete parameter definitions
- Default values
- Validation rules
- Conditional display logic
- Translations

**Frontend Request:**
```typescript
// Location: packages/frontend/editor-ui/src/stores/nodeTypes.store.ts:307-326
const getNodesInformation = async (
  nodeInfos: INodeTypeNameVersion[],
  replace = true,
): Promise<INodeTypeDescription[]> => {
  const nodesInformation = await nodeTypesApi.getNodesInformation(
    rootStore.restApiContext,
    nodeInfos,
  );

  if (replace) setNodeTypes(nodesInformation);
  return nodesInformation;
};
```

**Backend Handler:**
```typescript
// Location: packages/cli/src/controllers/node-types.controller.ts:18-28
@Post('/')
async getNodeInfo(req: Request) {
  const nodeInfos = get(req, 'body.nodeInfos', []) as INodeTypeNameVersion[];

  return nodeInfos.reduce<INodeTypeDescription[]>((acc, { name, version }) => {
    const { description } = this.nodeTypes.getByNameAndVersion(name, version);
    acc.push(description);
    return acc;
  }, []);
}
```

### Tier 3: Execution Layer (Runtime)
**Purpose:** Actual code execution when workflow runs
**Method:** Dynamic `require()` on server
**Location:** Physical `.node.ts` files on server filesystem
**Contains:**
- `execute()` method with business logic
- Helper functions
- API calls
- Data transformation

**Loading Process:**
```typescript
// Location: packages/cli/src/node-types.ts:35-44
getByNameAndVersion(nodeType: string, version?: number): INodeType {
  const node = this.loadNodesAndCredentials.getNode(nodeType);
  const versionedNodeType = NodeHelpers.getVersionedNodeType(node.type, version);
  return versionedNodeType;
}

// Location: packages/cli/src/load-nodes-and-credentials.ts:429-437
getNode(fullNodeType: string): LoadedClass<INodeType | IVersionedNodeType> {
  const [packageName, nodeType] = fullNodeType.split('.');
  const loader = loaders[packageName];
  return loader.getNode(nodeType);  // require() call happens here
}
```

---

## Node Creation Flow: From Click to Canvas

### Step-by-Step Flow

```
1. User clicks "Add Node" button
        ↓
2. NodeCreator.vue opens (side panel with node browser)
        ↓
3. User searches/browses available nodes
   (Uses pre-loaded metadata from nodes.json)
        ↓
4. User selects "ActiveCampaign Tool"
        ↓
5. NodeCreator emits 'nodeTypeSelected' event
        ↓
6. NodeView.vue receives event
        ↓
7. useCanvasOperations.addNodes() called
        ↓
8. addNode() creates node data structure
        ↓
9. workflowsStore.addNode() adds to Vuex store
        ↓
10. Canvas.vue re-renders (Vue reactivity)
        ↓
11. Vue Flow library renders node on canvas
```

### Detailed Code Trace

#### Step 7-8: Node Creation Logic
```typescript
// Location: packages/frontend/editor-ui/src/composables/useCanvasOperations.ts:663-680
async function addNodes(
  nodes: AddedNodesAndConnections['nodes'],
  { viewport, ...options }: AddNodesOptions = {},
) {
  // Add type version if not specified
  const nodesWithTypeVersion = nodes.map((node) => {
    const typeVersion = node.typeVersion ??
      resolveNodeVersion(requireNodeTypeDescription(node.type));
    return { ...node, typeVersion };
  });

  // Load full properties if needed (Tier 2)
  await loadNodeTypesProperties(nodesWithTypeVersion);

  // Create each node
  for (const [index, nodeAddData] of nodesWithTypeVersion.entries()) {
    const { isAutoAdd, openDetail: openNDV, actionName, ...node } = nodeAddData;
    const position = node.position ?? insertPosition;
    const nodeTypeDescription = requireNodeTypeDescription(node.type, node.typeVersion);

    const newNode = addNode({ ...node, position }, nodeTypeDescription, options);
    addedNodes.push(newNode);
  }
}
```

#### Step 8: Node Data Resolution
```typescript
// Location: packages/frontend/editor-ui/src/composables/useCanvasOperations.ts
function addNode(
  node: AddNodeDataWithTypeVersion,
  nodeTypeDescription: INodeTypeDescription,
  options: AddNodeOptions = {},
): INodeUi {
  // Validate max nodes of this type
  checkMaxNodesOfTypeReached(nodeTypeDescription);

  // Create node data structure
  const nodeData = resolveNodeData(node, nodeTypeDescription, {
    viewport: options.viewport,
  });

  // Add to store (triggers Vue reactivity)
  workflowsStore.addNode(nodeData);

  // Track in history for undo/redo
  if (options.trackHistory) {
    historyStore.pushCommandToUndo(new AddNodeCommand(nodeData, Date.now()));
  }

  // Auto-connect to last node
  if (!options.isAutoAdd) {
    createConnectionToLastInteractedWithNode(nodeData, options);
  }

  // Initialize node
  void nextTick(() => {
    workflowsStore.setNodePristine(nodeData.name, true);
    nodeHelpers.matchCredentials(nodeData);
    nodeHelpers.updateNodeParameterIssues(nodeData);
  });

  return nodeData;
}
```

#### What resolveNodeData() Does:
```typescript
function resolveNodeData(
  node: AddNodeDataWithTypeVersion,
  nodeTypeDescription: INodeTypeDescription,
  { viewport }: { viewport?: { zoom: number } } = {},
): INodeUi {
  return {
    id: uuid(),  // Generate unique ID
    name: node.name || getUniqueNodeName(nodeTypeDescription.name),
    type: node.type,
    typeVersion: node.typeVersion,
    position: node.position,
    parameters: node.parameters ?? {},  // Start with empty/default params
    credentials: node.credentials,
    disabled: node.disabled ?? false,
    // ... other properties
  };
}
```

---

## Node Type Resolution System

### Naming Convention

```
Full Type Name: "n8n-nodes-base.activeCampaignTool"
├── Package: "n8n-nodes-base"
├── Node Type: "activeCampaign" (base)
└── Variant: "Tool" (dynamically generated)
```

### Physical File Structure

```
packages/nodes-base/nodes/ActiveCampaign/
├── ActiveCampaign.node.ts          ← Main implementation
├── ActiveCampaignTrigger.node.ts   ← Trigger variant
├── ContactDescription.ts           ← Parameter definitions
├── GenericFunctions.ts             ← Helper functions
└── activeCampaign.svg              ← Icon
```

### Node Implementation Example

```typescript
// Location: packages/nodes-base/nodes/ActiveCampaign/ActiveCampaign.node.ts:68-1195
export class ActiveCampaign implements INodeType {
  description: INodeTypeDescription = {
    displayName: 'ActiveCampaign',
    name: 'activeCampaign',  // Becomes "n8n-nodes-base.activeCampaign"
    icon: {
      light: 'file:activeCampaign.svg',
      dark: 'file:activeCampaign.dark.svg'
    },
    group: ['transform'],
    version: 1,
    usableAsTool: true,  // ← Enables automatic "Tool" variant generation
    subtitle: '={{$parameter["operation"] + ": " + $parameter["resource"]}}',
    description: 'Consume ActiveCampaign API',
    defaults: {
      name: 'ActiveCampaign',
    },
    inputs: [NodeConnectionType.Main],
    outputs: [NodeConnectionType.Main],
    credentials: [
      {
        name: 'activeCampaignApi',
        required: true,
      },
    ],
    properties: [
      {
        displayName: 'Resource',
        name: 'resource',
        type: 'options',
        noDataExpression: true,
        options: [
          {
            name: 'Contact',
            value: 'contact',
          },
          {
            name: 'Deal',
            value: 'deal',
          },
          // ... more resources
        ],
        default: 'contact',
      },
      // ... more properties
    ],
  };

  async execute(this: IExecuteFunctions): Promise<INodeExecutionData[][]> {
    const items = this.getInputData();
    const resource = this.getNodeParameter('resource', 0);
    const operation = this.getNodeParameter('operation', 0);

    // Execution logic here
    // ...

    return [items];
  }
}
```

### Dynamic "Tool" Variant Generation

**Why "activeCampaignTool" doesn't exist as a file:**

```typescript
// Location: packages/cli/src/load-nodes-and-credentials.ts:308-333
createAiTools() {
  // Find all nodes that can be used as AI tools
  const usableNodes = this.types.nodes.filter(
    (nodeType) => nodeType.usableAsTool
  );

  // Create Tool variant for each
  for (const usableNode of usableNodes) {
    const wrapped = this.convertNodeToAiTool({ description }).description;
    this.types.nodes.push(wrapped);  // Add to registry
    this.known.nodes[wrapped.name] = { ...this.known.nodes[usableNode.name] };
  }
}

// Conversion logic
convertNodeToAiTool(item: LoadedClass<INodeType>): LoadedClass<INodeType> {
  const description = { ...item.description };

  // Modify name
  description.name += 'Tool';  // "activeCampaign" → "activeCampaignTool"
  description.displayName += ' Tool';

  // Change connection types
  description.inputs = [];
  description.outputs = [NodeConnectionTypes.AiTool];

  // Wrap properties for AI context
  description.properties = [
    {
      displayName: 'Tool Name',
      name: 'toolName',
      type: 'string',
      default: description.displayName,
    },
    {
      displayName: 'Tool Description',
      name: 'toolDescription',
      type: 'string',
      default: description.description,
    },
    // ... original properties wrapped
  ];

  return { ...item, description };
}
```

### Resolution Flow at Runtime

```
User adds: "n8n-nodes-base.activeCampaignTool"
        ↓
Backend splits by '.': ["n8n-nodes-base", "activeCampaignTool"]
        ↓
Package lookup: loaders["n8n-nodes-base"]
        ↓
Check if "activeCampaignTool" exists in registry
        ↓
Not found → Check if ends with "Tool"
        ↓
Strip suffix: "activeCampaignTool" → "activeCampaign"
        ↓
Load base node: packages/nodes-base/nodes/ActiveCampaign/ActiveCampaign.node.ts
        ↓
Apply convertNodeToAiTool() transformation
        ↓
Return Tool variant (modified description, same execute() logic)
```

---

## Metadata vs Implementation

### What's in nodes.json (Tier 1 Metadata)

```json
{
  "name": "activeCampaignTool",
  "displayName": "ActiveCampaign Tool",
  "icon": "file:activeCampaign.svg",
  "group": ["transform"],
  "version": 1,
  "description": "Consume ActiveCampaign API",
  "defaults": {
    "name": "ActiveCampaign Tool"
  },
  "inputs": [],
  "outputs": ["ai_tool"],
  "credentials": [
    {
      "name": "activeCampaignApi",
      "required": true
    }
  ],
  "properties": [
    {
      "displayName": "Resource",
      "name": "resource",
      "type": "options",
      "options": [
        { "name": "Contact", "value": "contact" },
        { "name": "Deal", "value": "deal" }
      ]
    }
  ]
}
```

**Purpose:** Lightweight data for UI rendering, search, and filtering.

### What's in the .node.ts File (Tier 3 Implementation)

```typescript
export class ActiveCampaign implements INodeType {
  description: INodeTypeDescription = { /* metadata */ };

  async execute(this: IExecuteFunctions): Promise<INodeExecutionData[][]> {
    const items = this.getInputData();
    const resource = this.getNodeParameter('resource', 0);
    const operation = this.getNodeParameter('operation', 0);

    let responseData;

    if (resource === 'contact') {
      if (operation === 'create') {
        const email = this.getNodeParameter('email', 0) as string;
        const firstName = this.getNodeParameter('firstName', 0) as string;

        const body: IContact = {
          contact: {
            email,
            firstName,
          },
        };

        responseData = await activeCampaignApiRequest.call(
          this,
          'POST',
          '/api/3/contacts',
          body,
        );
      }
    }

    return [this.helpers.returnJsonArray(responseData)];
  }
}
```

**Purpose:** Actual business logic executed during workflow runs.

---

## Code Snippet Generation

### Where Snippets Are Built in n8n

Code snippets in n8n are **dynamically generated from node configuration**, not pre-stored. When a user needs a code representation:

#### 1. Workflow JSON Export

**Location:** `packages/frontend/editor-ui/src/stores/workflows.store.ts`

```typescript
// Export current workflow as JSON
function exportWorkflow(): IWorkflowDataUpdate {
  return {
    nodes: workflow.value.nodes,
    connections: workflow.value.connections,
    pinData: workflow.value.pinData,
    settings: workflow.value.settings,
    meta: workflow.value.meta,
  };
}
```

This generates the JSON you showed:
```json
{
  "nodes": [
    {
      "parameters": { "additionalFields": {} },
      "type": "n8n-nodes-base.activeCampaignTool",
      "typeVersion": 1,
      "position": [992, 528],
      "id": "9bc218f4-f329-41fe-a3d5-d27a5e28e5a7",
      "name": "Create a contact in ActiveCampaign1"
    }
  ]
}
```

#### 2. Code Generation for Nodes

**Location:** `packages/core/src/NodeExecuteFunctions.ts`

When n8n needs to show code (for code nodes or exports):

```typescript
function getNodeParameter(
  parameterName: string,
  itemIndex: number,
  fallbackValue?: any,
): NodeParameterValueType | object {
  const node = this.getNode();
  const nodeType = workflow.nodeTypes.getByNameAndVersion(node.type);

  // Get parameter definition
  const property = nodeType.description.properties.find(
    (p) => p.name === parameterName
  );

  // Get value from node.parameters
  const value = node.parameters[parameterName] ?? property.default ?? fallbackValue;

  // Resolve expressions if needed
  if (typeof value === 'string' && value.includes('={{')) {
    return workflow.expression.resolveSimpleParameterValue(value, ...);
  }

  return value;
}
```

#### 3. HTTP Request Code Snippet Generation

**Location:** `packages/nodes-base/nodes/HttpRequest/HttpRequest.node.ts`

n8n can generate code snippets for HTTP nodes:

```typescript
async execute(this: IExecuteFunctions): Promise<INodeExecutionData[][]> {
  const items = this.getInputData();

  // Generate curl command representation
  const method = this.getNodeParameter('method', 0) as string;
  const url = this.getNodeParameter('url', 0) as string;
  const body = this.getNodeParameter('body', 0, {}) as object;

  const curlCommand = `curl -X ${method} '${url}' \\
    -H 'Content-Type: application/json' \\
    -d '${JSON.stringify(body)}'`;

  // Execute actual request
  const response = await this.helpers.httpRequest({
    method,
    url,
    body,
  });

  return [this.helpers.returnJsonArray(response)];
}
```

#### 4. AI Code Generation

**Location:** `packages/@n8n/n8n-nodes-langchain/nodes/code/CodeTool.node.ts`

For AI-generated code:

```typescript
async execute(this: IExecuteFunctions): Promise<INodeExecutionData[][]> {
  const code = this.getNodeParameter('code', 0) as string;
  const mode = this.getNodeParameter('mode', 0) as 'runOnceForAllItems' | 'runOnceForEachItem';

  // Build code context
  const codeContext = {
    $items: this.getInputData(),
    $node: this.getNode(),
    $workflow: this.getWorkflow(),
  };

  // Execute in sandbox
  const sandbox = new Sandbox(codeContext);
  const result = await sandbox.run(code);

  return [this.helpers.returnJsonArray(result)];
}
```

### Building Snippets from Node Metadata

**Key Insight:** Snippets are built by combining:
1. Node type metadata (from `description.properties`)
2. Node parameter values (from `node.parameters`)
3. Templates/formatters specific to output format

**Example Builder Function:**

```typescript
function buildNodeSnippet(node: INodeUi, nodeType: INodeTypeDescription): string {
  const snippetParts: string[] = [];

  // Add node header
  snippetParts.push(`// ${node.name} (${nodeType.displayName})`);

  // Add parameters
  for (const property of nodeType.properties) {
    const value = node.parameters[property.name];
    if (value !== undefined) {
      snippetParts.push(`// ${property.displayName}: ${JSON.stringify(value)}`);
    }
  }

  // Add node configuration as JSON
  snippetParts.push(JSON.stringify({
    type: node.type,
    parameters: node.parameters,
    position: node.position,
  }, null, 2));

  return snippetParts.join('\n');
}
```

---

## Reverse Engineering for Odoo

### What We Need to Replicate

To recreate n8n's node system in Odoo, we need:

1. **Metadata Registry** (like nodes.json)
2. **Dynamic Snippet Builder** (from metadata + parameters)
3. **Node Type Resolution** (type string → implementation)
4. **On-Demand Loading** (lazy load full properties)

### Odoo Implementation Strategy

#### 1. Create Node Metadata Model

```python
# models/ai_node_type.py
class AINodeType(models.Model):
    _name = 'ai.node.type'
    _description = 'AI Node Type Metadata'

    name = fields.Char(required=True)  # e.g., "odoo_create_contact"
    display_name = fields.Char(required=True)  # e.g., "Create Contact in Odoo"
    package = fields.Char(default='odoo-base')  # e.g., "odoo-base"
    icon = fields.Binary()
    icon_url = fields.Char()
    description = fields.Text()
    usable_as_tool = fields.Boolean(default=True)

    # Metadata as JSON
    properties = fields.Json()  # Parameter definitions
    inputs = fields.Json()  # Connection types
    outputs = fields.Json()  # Connection types
    defaults = fields.Json()  # Default values

    # Implementation reference
    model_name = fields.Char()  # Odoo model this node operates on
    method_name = fields.Char()  # Method to call for execution
```

#### 2. Create Snippet Builder Service

```python
# services/snippet_builder.py
class SnippetBuilder:
    """Build code snippets from node metadata and parameters"""

    @staticmethod
    def build_json_snippet(node_instance):
        """Build JSON workflow snippet like n8n"""
        return {
            'parameters': node_instance.parameters or {},
            'type': f"{node_instance.node_type_id.package}.{node_instance.node_type_id.name}",
            'typeVersion': 1,
            'position': [node_instance.position_x, node_instance.position_y],
            'id': node_instance.uuid,
            'name': node_instance.name,
        }

    @staticmethod
    def build_python_snippet(node_instance):
        """Build Python code snippet"""
        node_type = node_instance.node_type_id
        params = node_instance.parameters or {}

        lines = [
            f"# {node_instance.name}",
            f"# Type: {node_type.display_name}",
            "",
        ]

        # Add parameter assignments
        for prop in node_type.properties.get('properties', []):
            param_name = prop['name']
            param_value = params.get(param_name)
            if param_value is not None:
                lines.append(f"{param_name} = {repr(param_value)}")

        # Add execution call
        if node_type.model_name and node_type.method_name:
            lines.append("")
            lines.append(f"# Execute node")
            lines.append(f"result = env['{node_type.model_name}'].{node_type.method_name}(")
            for prop in node_type.properties.get('properties', []):
                param_name = prop['name']
                lines.append(f"    {param_name}={param_name},")
            lines.append(")")

        return '\n'.join(lines)

    @staticmethod
    def build_api_snippet(node_instance):
        """Build API call snippet (curl, JavaScript, etc.)"""
        node_type = node_instance.node_type_id
        params = node_instance.parameters or {}

        # Build curl command
        lines = [
            "curl -X POST 'https://your-odoo.com/api/workflow/execute' \\",
            "  -H 'Content-Type: application/json' \\",
            "  -H 'Authorization: Bearer YOUR_TOKEN' \\",
            "  -d '{",
            f"    \"node_type\": \"{node_type.package}.{node_type.name}\",",
            f"    \"parameters\": {json.dumps(params, indent=6)},",
            "  }'",
        ]

        return '\n'.join(lines)
```

#### 3. Create Node Instance Model

```python
# models/ai_node_instance.py
class AINodeInstance(models.Model):
    _name = 'ai.node.instance'
    _description = 'AI Node Instance on Canvas'

    uuid = fields.Char(default=lambda self: str(uuid.uuid4()), required=True, index=True)
    name = fields.Char(required=True)
    node_type_id = fields.Many2one('ai.node.type', required=True, ondelete='restrict')

    # Canvas position
    position_x = fields.Float(default=0)
    position_y = fields.Float(default=0)

    # Configuration
    parameters = fields.Json()  # User-configured parameter values
    credentials = fields.Json()  # Credential references
    disabled = fields.Boolean(default=False)

    # Workflow relationship
    workflow_id = fields.Many2one('ai.workflow', required=True, ondelete='cascade')

    def get_snippet(self, snippet_type='json'):
        """Generate code snippet for this node"""
        self.ensure_one()

        if snippet_type == 'json':
            return SnippetBuilder.build_json_snippet(self)
        elif snippet_type == 'python':
            return SnippetBuilder.build_python_snippet(self)
        elif snippet_type == 'api':
            return SnippetBuilder.build_api_snippet(self)
        else:
            raise ValueError(f"Unknown snippet type: {snippet_type}")

    def execute(self):
        """Execute this node (Tier 3: Implementation)"""
        self.ensure_one()

        node_type = self.node_type_id
        if not node_type.model_name or not node_type.method_name:
            raise ValidationError("Node type has no execution implementation")

        # Dynamic method call
        model = self.env[node_type.model_name]
        method = getattr(model, node_type.method_name)

        # Pass parameters
        result = method(**self.parameters)

        return result
```

#### 4. Create Dynamic Snippet Controller

```python
# controllers/snippet_controller.py
from odoo import http
from odoo.http import request
import json

class SnippetController(http.Controller):

    @http.route('/api/node/snippet', type='json', auth='user', methods=['POST'])
    def get_node_snippet(self, node_id, snippet_type='json'):
        """Get snippet for a specific node instance"""
        node = request.env['ai.node.instance'].browse(node_id)
        if not node.exists():
            return {'error': 'Node not found'}

        snippet = node.get_snippet(snippet_type)
        return {
            'success': True,
            'snippet': snippet,
            'node_name': node.name,
            'node_type': node.node_type_id.display_name,
        }

    @http.route('/api/workflow/snippet', type='json', auth='user', methods=['POST'])
    def get_workflow_snippet(self, workflow_id, snippet_type='json'):
        """Get snippet for entire workflow"""
        workflow = request.env['ai.workflow'].browse(workflow_id)
        if not workflow.exists():
            return {'error': 'Workflow not found'}

        nodes_data = []
        for node in workflow.node_ids:
            nodes_data.append(node.get_snippet(snippet_type))

        if snippet_type == 'json':
            # Build n8n-style workflow JSON
            snippet = {
                'nodes': nodes_data,
                'connections': workflow.get_connections_json(),
                'meta': {
                    'instanceId': workflow.uuid,
                }
            }
        else:
            # Concatenate individual snippets
            snippet = '\n\n'.join(nodes_data)

        return {
            'success': True,
            'snippet': snippet,
            'workflow_name': workflow.name,
        }

    @http.route('/types/nodes.json', type='http', auth='user', methods=['GET'])
    def get_node_types_metadata(self):
        """Serve lightweight metadata JSON (like n8n's Tier 1)"""
        node_types = request.env['ai.node.type'].search([])

        metadata = []
        for node_type in node_types:
            metadata.append({
                'name': f"{node_type.package}.{node_type.name}",
                'displayName': node_type.display_name,
                'icon': node_type.icon_url,
                'description': node_type.description,
                'group': ['transform'],
                'version': 1,
                'usableAsTool': node_type.usable_as_tool,
                'defaults': node_type.defaults,
                'inputs': node_type.inputs,
                'outputs': node_type.outputs,
                # NOTE: Don't include full properties here - keep it lightweight
                'properties': [
                    {
                        'name': prop['name'],
                        'displayName': prop['displayName'],
                        'type': prop['type'],
                    }
                    for prop in node_type.properties.get('properties', [])
                ],
            })

        return request.make_response(
            json.dumps(metadata, indent=2),
            headers=[
                ('Content-Type', 'application/json'),
                ('Cache-Control', 'no-cache, must-revalidate'),
            ]
        )
```

#### 5. JavaScript Canvas Integration

```javascript
// static/src/js/canvas_operations.js
odoo.define('ai_automator.canvas_operations', function (require) {
    'use strict';

    const ajax = require('web.ajax');

    class CanvasOperations {

        /**
         * Add node to canvas (like n8n's addNode)
         */
        async addNode(nodeTypeFullName, position) {
            // Parse node type
            const [packageName, nodeTypeName] = nodeTypeFullName.split('.');

            // Load node type metadata (if not cached)
            const nodeType = await this.getNodeTypeMetadata(nodeTypeFullName);

            // Create node instance
            const nodeData = {
                node_type_id: nodeType.id,
                name: this.getUniqueNodeName(nodeType.displayName),
                position_x: position[0],
                position_y: position[1],
                parameters: nodeType.defaults || {},
                workflow_id: this.currentWorkflowId,
            };

            // Save to backend
            const result = await ajax.jsonRpc('/api/node/create', 'call', nodeData);

            // Add to canvas
            this.renderNode(result.node);

            return result.node;
        }

        /**
         * Get node snippet (like n8n's export)
         */
        async getNodeSnippet(nodeId, snippetType = 'json') {
            const result = await ajax.jsonRpc('/api/node/snippet', 'call', {
                node_id: nodeId,
                snippet_type: snippetType,
            });

            return result.snippet;
        }

        /**
         * Load node types metadata (Tier 1)
         */
        async loadNodeTypesMetadata() {
            const response = await fetch('/types/nodes.json');
            const metadata = await response.json();

            // Cache in memory
            this.nodeTypesCache = metadata;

            return metadata;
        }

        /**
         * Get full node properties (Tier 2 - on demand)
         */
        async getNodeProperties(nodeTypeFullName) {
            const result = await ajax.jsonRpc('/api/node-type/properties', 'call', {
                node_type: nodeTypeFullName,
            });

            return result.properties;
        }
    }

    return CanvasOperations;
});
```

### Key Implementation Points for Odoo

1. **Metadata Storage:** Use `ai.node.type` model to store all node type definitions
2. **Snippet Generation:** Build snippets dynamically from `node_type.properties` + `node_instance.parameters`
3. **Lazy Loading:**
   - Tier 1: Serve `/types/nodes.json` endpoint with lightweight metadata
   - Tier 2: API endpoint for full properties when editing node
   - Tier 3: Execute method on `ai.node.instance` when workflow runs
4. **Type Resolution:** Parse `"package.nodeName"` format to lookup in database
5. **Tool Variants:** Use computed field or flag on `ai.node.type` to auto-generate tool variants

### Where Snippets Are Built: Summary

**In n8n:**
- **Workflow JSON:** Built by serializing `workflow.nodes` array (frontend store)
- **Node Metadata:** Pre-generated into `nodes.json` at server startup
- **Code Snippets:** Generated dynamically by node execution context
- **Location:** `packages/frontend/editor-ui/src/stores/workflows.store.ts` (export functions)

**In Odoo (Our Implementation):**
- **Workflow JSON:** `SnippetBuilder.build_json_snippet()` method
- **Node Metadata:** `/types/nodes.json` controller endpoint
- **Code Snippets:** `SnippetBuilder.build_python_snippet()` / `build_api_snippet()`
- **Location:** `services/snippet_builder.py` (centralized snippet generation)

---

## Critical File References

### n8n Backend (Node.js/TypeScript)

**Core Loading System:**
- `packages/cli/src/load-nodes-and-credentials.ts` (Lines 36-688)
  - `init()` - Package discovery and loading
  - `loadNodesFromNodeModules()` - Scan directories
  - `createAiTools()` - Generate Tool variants (308-333)
  - `convertNodeToAiTool()` - Tool transformation logic
  - `getNode()` - Dynamic require() loading (429-437)

**Node Type Resolution:**
- `packages/cli/src/node-types.ts` (Lines 1-152)
  - `getByNameAndVersion()` - Main resolution method (35-44)

**API & Serving:**
- `packages/cli/src/services/frontend.service.ts` (Lines 296-305, 525-539)
  - `generateTypes()` - Create nodes.json
  - `writeStaticJSON()` - Write metadata files
- `packages/cli/src/controllers/node-types.controller.ts` (Lines 10-64)
  - `getNodeInfo()` - Tier 2 property loading (18-28)
- `packages/cli/src/server.ts`
  - Static file serving for `/types/nodes.json`

### n8n Frontend (Vue 3/TypeScript)

**Stores:**
- `packages/frontend/editor-ui/src/stores/nodeTypes.store.ts` (Lines 40-456)
  - `getNodeTypes()` - Fetch metadata (339-345)
  - `getNodesInformation()` - Load properties (307-326)
  - `setNodeTypes()` - Cache in store
- `packages/frontend/editor-ui/src/stores/workflows.store.ts`
  - `addNode()` - Add to workflow
  - `exportWorkflow()` - Generate JSON

**Canvas Operations:**
- `packages/frontend/editor-ui/src/composables/useCanvasOperations.ts` (Lines 153-1800+)
  - `addNodes()` - Main entry point (663-680)
  - `addNode()` - Node creation logic
  - `resolveNodeData()` - Build node data structure
  - `loadNodeTypesProperties()` - Trigger Tier 2 loading

**UI Components:**
- `packages/frontend/editor-ui/src/components/Node/NodeCreator/NodeCreator.vue` (Lines 1-200)
  - Node selection panel
  - Search and filtering
  - Node type browsing
- `packages/frontend/editor-ui/src/components/canvas/Canvas.vue` (Lines 1-200)
  - Canvas rendering (Vue Flow)
  - Node visualization

**API Client:**
- `packages/frontend/@n8n/rest-api-client/src/api/nodeTypes.ts` (Lines 1-125)
  - `getNodeTypes()` - Fetch nodes.json (37-39)
  - `getNodesInformation()` - Fetch properties

### n8n Node Implementation

**Example Node:**
- `packages/nodes-base/nodes/ActiveCampaign/ActiveCampaign.node.ts` (Lines 68-1195)
  - Node class definition
  - `description` - INodeTypeDescription
  - `execute()` - Implementation logic

**Node Helpers:**
- `packages/core/src/NodeExecuteFunctions.ts`
  - `getNodeParameter()` - Parameter resolution
  - Helper functions for execution context

---

## Code Snippet Generation: Deep Dive

### Where Snippets Are Actually Built

After extensive research into n8n's codebase, here's exactly where and how snippets are generated:

#### 1. Workflow JSON Export (Primary Snippet Format)

**Location:** `packages/frontend/editor-ui/src/composables/useWorkflowHelpers.ts`

**Master Function:** `getWorkflowDataToSave()` (Lines 595-626)

This is the **single source of truth** for converting canvas state to JSON:

```typescript
async function getWorkflowDataToSave() {
    const workflowNodes = workflowsStore.allNodes;
    const workflowConnections = workflowsStore.allConnections;

    const nodes: INode[] = [];
    for (let nodeIndex = 0; nodeIndex < workflowNodes.length; nodeIndex++) {
        nodeData = getNodeDataToSave(workflowNodes[nodeIndex]);  // ← Key function
        nodes.push(nodeData);
    }

    const data: WorkflowData = {
        name: workflowsStore.workflowName,
        nodes,
        pinData: workflowsStore.pinnedWorkflowData,
        connections: workflowConnections,
        active: workflowsStore.isWorkflowActive,
        settings: workflowsStore.workflow.settings,
        tags: workflowsStore.workflowTags,
    };

    return data;
}
```

**Node Serialization Function:** `getNodeDataToSave(node)` (Lines 628-700+)

This converts individual nodes to the JSON structure you see:

```typescript
function getNodeDataToSave(node: INodeUi): INodeUi {
    const skipKeys = [
        'color',
        'continueOnFail',
        'credentials',
        'disabled',
        'issues',
        'notes',
        'parameters',
        'status',
    ];

    const nodeData: INodeUi = {
        parameters: {},
    };

    // Copy all relevant properties
    for (const key in node) {
        if (key.charAt(0) !== '_' && skipKeys.indexOf(key) === -1) {
            nodeData[key] = node[key];
        }
    }

    // Get node type metadata
    const nodeType = nodeTypesStore.getNodeType(node.type, node.typeVersion);

    if (nodeType !== null) {
        // Extract parameters using NodeHelpers
        const nodeParameters = NodeHelpers.getNodeParameters(
            nodeType.properties,
            node.parameters,
            false,
            false,
            node,
            nodeType,
        );
        nodeData.parameters = nodeParameters !== null ? nodeParameters : {};

        // Add credentials metadata (not actual secrets)
        if (node.credentials !== undefined && nodeType.credentials !== undefined) {
            const saveCredentials: INodeCredentials = {};
            for (const nodeCredentialTypeName of Object.keys(node.credentials)) {
                saveCredentials[nodeCredentialTypeName] = node.credentials[nodeCredentialTypeName];
            }
        }
    }

    return nodeData;
}
```

**Result:** This produces the exact JSON format from your example:

```json
{
  "parameters": { "additionalFields": {} },
  "type": "n8n-nodes-base.activeCampaignTool",
  "typeVersion": 1,
  "position": [992, 528],
  "id": "9bc218f4-f329-41fe-a3d5-d27a5e28e5a7",
  "name": "Create a contact in ActiveCampaign1"
}
```

#### 2. File Export Process

**Location:** `packages/frontend/editor-ui/src/components/MainHeader/WorkflowDetails.vue` (Lines 460-480)

When user clicks "Download":

```typescript
const workflowData = await getWorkflowDataToSave();
const exportData = {
    ...workflowData,
    meta: {
        ...props.meta,
        instanceId: rootStore.instanceId,
    },
    tags: tagsStore.tagsById,
};

const blob = new Blob([JSON.stringify(exportData, null, 2)], {
    type: 'application/json;charset=utf-8',
});

saveAs(blob, name + '.json');
```

**Key Insight:** It's just `JSON.stringify()` with pretty formatting (`null, 2`)!

#### 3. AI Code Generation (For Code Nodes)

**Location:** `packages/frontend/editor-ui/src/components/ButtonParameter/utils.ts` (Lines 183-237)

When generating code for transform/code nodes:

```typescript
export async function generateCodeForAiTransform(prompt: string, path: string) {
    // Build context from parent nodes
    const schemas = getSchemas();

    const payload: AskAiRequest.RequestPayload = {
        question: prompt,
        context: {
            schema: schemas.parentNodesSchemas,  // ← Data structure from previous nodes
            inputSchema: schemas.inputSchema,
            ndvPushRef: useNDVStore().pushRef,
            pushRef: useRootStore().pushRef,
        },
        forNode: 'transform',
    };

    // Call AI API
    const { code: generatedCode } = await generateCodeForPrompt(restApiContext, payload);

    // Format with Prettier
    const formattedCode = await format(String(generatedCode), {
        parser: 'babel',
        plugins: [jsParser, estree],
    });

    return formattedCode;
}
```

**Schema Building:** `getSchemas()` (Lines 20-57)

```typescript
export function getSchemas() {
    const parentNodes = getParentNodes();  // Get all nodes feeding into current node
    const parentNodesSchemas: Array<{ nodeName: string; schema: Schema }> = parentNodes
        .map((node) => {
            const inputData: INodeExecutionData[] = getInputDataWithPinned(node);
            return {
                nodeName: node?.name || '',
                schema: getSchemaForExecutionData(executionDataToJson(inputData), false),
            };
        })
        .filter((node) => node.schema?.value.length > 0);

    return {
        parentNodesNames,
        inputSchema: parentNodesSchemas[0],  // Primary input
        parentNodesSchemas,  // All parent outputs
    };
}
```

#### 4. CURL Import (Reverse Engineering)

**Location:** `packages/frontend/editor-ui/src/composables/useImportCurlCommand.ts` (Lines 234-383)

This shows how n8n converts **external code into node parameters**:

```typescript
export const toHttpNodeParameters = (curlCommand: string): HttpNodeParameters => {
    const curlJson = curlToJson(curlCommand);  // Parse curl command
    const headers = curlJson.headers ?? {};

    const httpNodeParameters: HttpNodeParameters = {
        url: curlJson.url,
        authentication: 'none',
        method: curlJson.method.toUpperCase(),
    };

    // Handle different content types
    if (isJsonRequest(curlJson)) {
        Object.assign(httpNodeParameters, {
            contentType: 'json',
            sendBody: true,
            specifyBody: 'json',
            jsonBody: JSON.stringify(curlJson.data, null, 2),
        });
    } else if (isFormUrlEncodedRequest(curlJson)) {
        Object.assign(httpNodeParameters, {
            contentType: 'form-urlencoded',
            sendBody: true,
            specifyBody: 'keypair',
            bodyParameters: {
                parameters: jsonBodyToNodeParameters(curlJson.data),
            },
        });
    }

    return httpNodeParameters;
};
```

This is the **REVERSE** of snippet generation - taking code and creating node config!

### Snippet Building Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Canvas State (Vue Store)                  │
│  - workflowsStore.allNodes (INodeUi[])                      │
│  - workflowsStore.allConnections                            │
│  - Node parameters, position, type, etc.                     │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
         ┌─────────────────────────────┐
         │  getWorkflowDataToSave()    │
         │  (Master Serializer)        │
         └──────────┬──────────────────┘
                    │
                    ▼
         ┌─────────────────────────────┐
         │  For each node:             │
         │  getNodeDataToSave(node)    │
         └──────────┬──────────────────┘
                    │
                    ▼
         ┌─────────────────────────────────────────┐
         │ Filter properties (skip UI-only keys)   │
         │ Get node type metadata                  │
         │ NodeHelpers.getNodeParameters()         │
         │ Extract credentials metadata            │
         └──────────┬──────────────────────────────┘
                    │
                    ▼
         ┌─────────────────────────────┐
         │  Return INode:              │
         │  {                          │
         │    id, name, type,          │
         │    typeVersion, position,   │
         │    parameters, credentials  │
         │  }                          │
         └──────────┬──────────────────┘
                    │
                    ▼
         ┌─────────────────────────────┐
         │  Combine all nodes:         │
         │  {                          │
         │    nodes: [...],            │
         │    connections: {...},      │
         │    settings, tags, etc.     │
         │  }                          │
         └──────────┬──────────────────┘
                    │
                    ▼
         ┌─────────────────────────────┐
         │  JSON.stringify(data, 2)    │
         │  (Pretty print with indent) │
         └──────────┬──────────────────┘
                    │
                    ▼
         ┌─────────────────────────────┐
         │  Export as .json file       │
         │  OR Save to database        │
         │  OR Send to API             │
         └─────────────────────────────┘
```

### For Odoo: Implementation Blueprint

Based on n8n's patterns, here's what we need:

#### 1. Snippet Builder Service

```python
# services/snippet_builder.py
from odoo import _
import json

class SnippetBuilder:
    """
    Replicates n8n's getWorkflowDataToSave() and getNodeDataToSave() logic
    """

    @staticmethod
    def serialize_node(node_instance):
        """
        Equivalent to n8n's getNodeDataToSave()
        Converts ai.node.instance to JSON snippet
        """
        node_type = node_instance.node_type_id

        # Build base node structure
        node_data = {
            'id': node_instance.uuid,
            'name': node_instance.name,
            'type': f"{node_type.package}.{node_type.name}",
            'typeVersion': node_type.type_version or 1,
            'position': [
                node_instance.position_x,
                node_instance.position_y
            ],
            'parameters': node_instance.parameters or {},
        }

        # Add optional fields
        if node_instance.disabled:
            node_data['disabled'] = True

        if node_instance.notes:
            node_data['notes'] = node_instance.notes

        # Add credentials (metadata only, not actual secrets)
        if node_instance.credential_ids:
            node_data['credentials'] = {}
            for cred in node_instance.credential_ids:
                node_data['credentials'][cred.credential_type] = {
                    'id': cred.uuid,
                    'name': cred.name
                }

        return node_data

    @staticmethod
    def serialize_workflow(workflow):
        """
        Equivalent to n8n's getWorkflowDataToSave()
        Converts ai.workflow to complete JSON
        """
        # Serialize all nodes
        nodes = []
        for node in workflow.node_ids:
            nodes.append(SnippetBuilder.serialize_node(node))

        # Build connections
        connections = SnippetBuilder._build_connections(workflow)

        # Assemble workflow
        workflow_data = {
            'name': workflow.name,
            'nodes': nodes,
            'connections': connections,
            'active': workflow.active,
            'settings': workflow.settings or {},
            'meta': {
                'instanceId': workflow.uuid,
            }
        }

        if workflow.tags:
            workflow_data['tags'] = [tag.name for tag in workflow.tag_ids]

        return workflow_data

    @staticmethod
    def _build_connections(workflow):
        """Build n8n-style connections object"""
        connections = {}

        for connection in workflow.connection_ids:
            source_name = connection.source_node_id.name
            target_name = connection.target_node_id.name

            # Initialize source node connections
            if source_name not in connections:
                connections[source_name] = {'main': [[]]}

            # Ensure output index exists
            output_index = connection.source_output_index or 0
            while len(connections[source_name]['main']) <= output_index:
                connections[source_name]['main'].append([])

            # Add connection
            connections[source_name]['main'][output_index].append({
                'node': target_name,
                'type': connection.connection_type or 'main',
                'index': connection.target_input_index or 0
            })

        return connections

    @staticmethod
    def to_json(workflow, pretty=True):
        """Export workflow as JSON string"""
        workflow_data = SnippetBuilder.serialize_workflow(workflow)
        indent = 2 if pretty else None
        return json.dumps(workflow_data, indent=indent)

    @staticmethod
    def to_python_code(node_instance):
        """Generate Python code snippet for a node"""
        node_type = node_instance.node_type_id
        params = node_instance.parameters or {}

        lines = [
            f"# {node_instance.name}",
            f"# Type: {node_type.display_name}",
            f"# Description: {node_type.description or 'N/A'}",
            "",
        ]

        # Add parameter assignments
        for prop in node_type.properties.get('properties', []):
            param_name = prop['name']
            param_value = params.get(param_name)
            if param_value is not None:
                lines.append(f"{param_name} = {repr(param_value)}")

        # Add execution call
        if node_type.model_name and node_type.method_name:
            lines.extend([
                "",
                "# Execute node",
                f"result = env['{node_type.model_name}'].{node_type.method_name}(",
            ])
            for prop in node_type.properties.get('properties', []):
                param_name = prop['name']
                if param_name in params:
                    lines.append(f"    {param_name}={param_name},")
            lines.append(")")

        return '\n'.join(lines)

    @staticmethod
    def to_curl_command(node_instance):
        """Generate curl command for HTTP-based nodes"""
        params = node_instance.parameters or {}

        method = params.get('method', 'GET')
        url = params.get('url', 'https://api.example.com')
        headers = params.get('headers', {})
        body = params.get('body', {})

        lines = [
            f"curl -X {method} '{url}' \\",
        ]

        # Add headers
        for key, value in headers.items():
            lines.append(f"  -H '{key}: {value}' \\")

        # Add body if POST/PUT/PATCH
        if method in ['POST', 'PUT', 'PATCH'] and body:
            lines.append(f"  -d '{json.dumps(body)}'")

        return '\n'.join(lines)
```

#### 2. Add Methods to Models

```python
# models/ai_node_instance.py
class AINodeInstance(models.Model):
    _name = 'ai.node.instance'

    def get_snippet(self, format='json'):
        """
        Get code snippet in various formats
        Replicates n8n's export functionality
        """
        self.ensure_one()

        if format == 'json':
            return SnippetBuilder.serialize_node(self)
        elif format == 'python':
            return SnippetBuilder.to_python_code(self)
        elif format == 'curl':
            return SnippetBuilder.to_curl_command(self)
        else:
            raise ValueError(f"Unknown format: {format}")

# models/ai_workflow.py
class AIWorkflow(models.Model):
    _name = 'ai.workflow'

    def export_json(self, pretty=True):
        """
        Export workflow as n8n-compatible JSON
        Equivalent to n8n's workflow export
        """
        self.ensure_one()
        return SnippetBuilder.to_json(self, pretty=pretty)

    def action_download_json(self):
        """Button action to download workflow JSON"""
        self.ensure_one()

        json_content = self.export_json(pretty=True)

        # Create attachment
        attachment = self.env['ir.attachment'].create({
            'name': f'{self.name}.json',
            'type': 'binary',
            'datas': base64.b64encode(json_content.encode('utf-8')),
            'mimetype': 'application/json',
        })

        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/{attachment.id}?download=true',
            'target': 'self',
        }
```

#### 3. Controller Endpoints

```python
# controllers/snippet_controller.py
from odoo import http
from odoo.http import request
import json

class SnippetController(http.Controller):

    @http.route('/api/workflow/export', type='json', auth='user')
    def export_workflow(self, workflow_id, format='json'):
        """
        Export workflow in various formats
        Equivalent to n8n's workflow export endpoint
        """
        workflow = request.env['ai.workflow'].browse(workflow_id)
        if not workflow.exists():
            return {'error': 'Workflow not found'}

        if format == 'json':
            content = workflow.export_json(pretty=True)
        elif format == 'compact':
            content = workflow.export_json(pretty=False)
        else:
            return {'error': f'Unknown format: {format}'}

        return {
            'success': True,
            'content': content,
            'filename': f'{workflow.name}.json'
        }

    @http.route('/api/node/snippet', type='json', auth='user')
    def get_node_snippet(self, node_id, format='json'):
        """
        Get snippet for individual node
        Equivalent to n8n's node serialization
        """
        node = request.env['ai.node.instance'].browse(node_id)
        if not node.exists():
            return {'error': 'Node not found'}

        try:
            snippet = node.get_snippet(format=format)
            return {
                'success': True,
                'snippet': snippet,
                'node_name': node.name,
            }
        except ValueError as e:
            return {'error': str(e)}
```

#### 4. JavaScript Integration

```javascript
// static/src/js/snippet_export.js
odoo.define('ai_automator.snippet_export', function (require) {
    'use strict';

    const ajax = require('web.ajax');

    class SnippetExporter {

        /**
         * Export workflow as JSON (like n8n's download)
         */
        async exportWorkflow(workflowId, format = 'json') {
            const result = await ajax.jsonRpc('/api/workflow/export', 'call', {
                workflow_id: workflowId,
                format: format,
            });

            if (result.success) {
                // Download file
                this.downloadFile(result.filename, result.content);
            }

            return result;
        }

        /**
         * Get node snippet
         */
        async getNodeSnippet(nodeId, format = 'json') {
            const result = await ajax.jsonRpc('/api/node/snippet', 'call', {
                node_id: nodeId,
                format: format,
            });

            return result;
        }

        /**
         * Download file helper
         */
        downloadFile(filename, content) {
            const blob = new Blob([content], { type: 'application/json' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = filename;
            a.click();
            URL.revokeObjectURL(url);
        }

        /**
         * Copy snippet to clipboard
         */
        async copyNodeSnippet(nodeId, format = 'json') {
            const result = await this.getNodeSnippet(nodeId, format);

            if (result.success) {
                await navigator.clipboard.writeText(
                    typeof result.snippet === 'string'
                        ? result.snippet
                        : JSON.stringify(result.snippet, null, 2)
                );
                return true;
            }

            return false;
        }
    }

    return SnippetExporter;
});
```

### Summary: Where Snippets Are Built

**In n8n:**
1. **Primary Location:** `packages/frontend/editor-ui/src/composables/useWorkflowHelpers.ts`
   - `getWorkflowDataToSave()` - Master workflow serializer
   - `getNodeDataToSave()` - Individual node serializer
2. **Export UI:** `packages/frontend/editor-ui/src/components/MainHeader/WorkflowDetails.vue`
   - Calls serializer and uses `JSON.stringify(data, null, 2)`
3. **Code Generation:** `packages/frontend/editor-ui/src/components/ButtonParameter/utils.ts`
   - AI-powered code snippet generation with context

**In Odoo (Our Implementation):**
1. **Primary Location:** `services/snippet_builder.py`
   - `SnippetBuilder.serialize_workflow()` - Master serializer
   - `SnippetBuilder.serialize_node()` - Node serializer
   - `SnippetBuilder.to_python_code()` - Python code generator
   - `SnippetBuilder.to_curl_command()` - API command generator
2. **Model Methods:** `models/ai_workflow.py` and `models/ai_node_instance.py`
   - `export_json()` - Workflow export
   - `get_snippet()` - Node snippet
3. **Controller:** `controllers/snippet_controller.py`
   - `/api/workflow/export` - Export endpoint
   - `/api/node/snippet` - Node snippet endpoint

**Key Takeaway:** Snippets are **dynamically generated** by serializing the workflow/node data structures. There are no pre-stored templates - everything is built on-demand by combining:
- Node type metadata (from `ai.node.type`)
- Node instance parameters (from `ai.node.instance.parameters`)
- Workflow structure (connections, settings, etc.)

---

## Conclusion

n8n's node creation system is based on:

1. **Separation of Concerns:**
   - Metadata (JSON) for UI/browsing
   - Properties (API) for editing
   - Implementation (TypeScript) for execution

2. **Lazy Loading:**
   - Only load what's needed when it's needed
   - Metadata loaded once at startup
   - Properties loaded on demand
   - Code executed only when workflow runs

3. **Type Resolution:**
   - Node type string is a key, not code
   - Format: `"package.nodeName"`
   - Maps to physical file: `packages/nodes-base/nodes/NodeName/NodeName.node.ts`

4. **Dynamic Generation:**
   - Tool variants created programmatically
   - Snippets built from metadata + parameters
   - No pre-stored code representations

**For Odoo Implementation:**
- Store metadata in `ai.node.type` model
- Build snippets dynamically in `SnippetBuilder` service
- Use three-tier loading (metadata → properties → execution)
- Implement snippet endpoints that combine node type metadata with instance parameters

The key insight: **Snippets are not stored, they're generated on-demand from structured data.**