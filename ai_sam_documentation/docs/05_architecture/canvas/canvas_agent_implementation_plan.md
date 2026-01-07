# Canvas Agent Implementation Plan

## SAM AI Workflow Builder Agent

**Date:** 2025-12-21
**Status:** ALL PHASES COMPLETE ✅
**Author:** Anthony Gardiner & Claude AI (SAM Core Chat Agent)

---

## Implementation Progress

| Phase | Status | Completed |
|-------|--------|-----------|
| Phase 1: Canvas Read Tools | ✅ COMPLETE | 2025-12-21 |
| Phase 2: Canvas Edit Tools | ✅ COMPLETE | 2025-12-21 |
| Phase 3: Canvas Create Tools | ✅ COMPLETE | 2025-12-21 |
| Phase 4: Real-time Updates | ✅ COMPLETE | 2025-12-21 |
| Phase 5: Undo/Redo System | ✅ COMPLETE | 2025-12-21 |

### Phase 1 Implementation Details

**Files Created/Modified:**
- `ai_sam_base/models/canvas_tools.py` - Canvas tool definitions and executor
- `ai_sam_base/models/__init__.py` - Registered canvas_tools module
- `ai_sam_base/models/ai_brain.py` - Integrated canvas tool execution
- `ai_sam/static/src/js/chat/chat_interaction.js` - Canvas activity states
- `ai_sam/static/src/js/sam_chat_vanilla_v2.js` - Fallback activity states

**Tool Implemented:**
- `canvas_read` - Query workflow canvas (nodes, connections, metadata, summary)

### Phase 1.1: Voice & Personality Enhancement (2025-12-21)

**Problem:** SAM's responses were technically accurate but "bland and very contextual" - lacking the personality and enthusiasm of Claude and ChatGPT.

**Solution:** Enhanced SAM's core voice prompt with:
- **Personality section** - Warm, curious, confident, proactive traits
- **Voice examples** - Concrete before/after examples (❌ vs ✅)
- **Enthusiasm calibration** - Right tone for different contexts
- **Conversational formatting** - Templates that sound human

**Files Modified:**
- `ai_sam_base/models/sam_voice.py` - Added personality framework to core prompt
- `ai_sam_base/models/canvas_tools.py` - Improved with:
  - Conversational summary generation
  - Friendly node type names
  - Purpose descriptions ("talks to your database")
  - Actionable suggestions with emojis
  - Fixed flow description (no longer mixes external file names)

### Phase 2 Implementation Details (2025-12-21)

**Tools Implemented:**
- `canvas_edit` - Modify workflow canvas (add/remove/update nodes and connections)
- `canvas_node_types` - Search for available N8N node types

**Edit Actions Available:**
- `add_node` - Add a new node to the canvas with auto-positioning
- `remove_node` - Remove a node and all its connections
- `update_node` - Update node name or parameters
- `add_connection` - Connect two nodes together
- `remove_connection` - Disconnect two nodes
- `move_node` - Move a node to a new position

**Features:**
- Node lookup by ID or name (flexible input)
- Auto-position calculation for new nodes
- Friendly result messages with emojis
- Connection validation (prevents duplicates)
- Uses `canvas.save_canvas_state()` for persistence
- Console logging with emoji prefixes for debugging

**Files Modified:**
- `ai_sam_base/models/canvas_tools.py` - Added:
  - `canvas_edit` tool definition
  - `canvas_node_types` tool definition
  - `_execute_canvas_edit()` with 6 action handlers
  - `_execute_canvas_node_types()` for node search
  - `_edit_add_node()`, `_edit_remove_node()`, `_edit_update_node()`
  - `_edit_add_connection()`, `_edit_remove_connection()`, `_edit_move_node()`
  - `_calculate_next_position()` for auto-positioning
  - `_generate_edit_message()` for friendly feedback

- `ai_sam/static/src/js/chat/chat_interaction.js` - Added Phase 2 activity states:
  - `adding_node`, `removing_node`, `updating_node`
  - `connecting_nodes`, `disconnecting_nodes`, `moving_node`
  - `saving_canvas`, `searching_nodes`
  - `node_added`, `node_removed`, `nodes_connected`

### Phase 3 Implementation Details (2025-12-21)

**Tool Implemented:**
- `canvas_create` - Create complete workflows from natural language descriptions

**Workflow Pattern Templates (7 patterns):**
- `email_to_spreadsheet` - Gmail → Extract → Google Sheets
- `api_to_notification` - HTTP Request → Process → Slack/Discord
- `webhook_processing` - Webhook → Validate → Transform → Respond
- `data_sync` - Schedule → Fetch → Compare → Update
- `lead_automation` - Form → Enrich → CRM → Email
- `content_pipeline` - RSS → AI Process → Format → Publish
- `simple_trigger` - Manual Trigger → Action (fallback)

**Features:**
- Pattern matching with keyword scoring (requires 2+ keyword matches)
- Auto-generates nodes with proper N8N types
- Auto-positions nodes horizontally with 250px spacing
- Auto-wires connections between nodes
- Falls back to custom workflow builder for unmatched descriptions
- Records history for undo support

**Files Modified:**
- `ai_sam_base/models/canvas_tools.py` - Added:
  - `canvas_create` tool definition
  - `WORKFLOW_PATTERNS` dictionary with 7 templates
  - `_execute_canvas_create()` method
  - `_find_matching_pattern()` for keyword matching
  - `_apply_workflow_pattern()` for template instantiation
  - `_build_custom_workflow()` for unmatched descriptions

### Phase 4 Implementation Details (2025-12-21)

**Feature Implemented:**
- Real-time WebSocket updates via Odoo's `bus.bus`

**Real-time Events:**
- `canvas.node_added` - Node was added to canvas
- `canvas.node_removed` - Node was removed
- `canvas.node_updated` - Node was modified
- `canvas.connection_added` - Connection created
- `canvas.connection_removed` - Connection removed
- `canvas.workflow_created` - New workflow generated
- `canvas.state_restored` - Undo/redo state change

**Files Modified:**
- `ai_sam_base/models/canvas_tools.py` - Added:
  - `_push_canvas_update()` - Push events to bus.bus channel
  - `_notify_canvas_change()` - Wrapper for common notifications
  - Integration in all edit operations

- `ai_sam/static/src/js/chat/chat_interaction.js` - Added Phase 4 activity states:
  - `pushing_update`, `canvas_synced`

### Phase 5 Implementation Details (2025-12-21)

**Model Created:**
- `canvas.history` - Tracks all canvas edit actions for undo/redo

**Tools Implemented:**
- `canvas_undo` - Undo the last canvas edit action(s)
- `canvas_redo` - Redo the last undone action(s)

**History Model Fields:**
- `canvas_id` - Link to canvas (cascade delete)
- `action_type` - Type of edit (add_node, remove_node, etc.)
- `previous_state` - Complete canvas JSON before action (for undo)
- `action_data` - Action details JSON (for audit)
- `performed_by` - 'user' or 'sam'
- `user_id` - User who triggered the action
- `is_undone` - Flag for redo support

**Files Created:**
- `ai_sam_workflows_base/models/canvas_history.py` - New history model with:
  - `undo()` method - Restores previous_state
  - `redo()` method - Re-marks action as not undone
  - `get_canvas_history()` - Query history for a canvas
  - `cleanup_old_history()` - Prune old entries (keeps 50)

**Files Modified:**
- `ai_sam_workflows_base/models/__init__.py` - Registered canvas_history
- `ai_sam_base/models/canvas_tools.py` - Added:
  - `canvas_undo` and `canvas_redo` tool definitions
  - `_record_history()` - Records each action
  - `_execute_canvas_undo()` - Undo implementation
  - `_execute_canvas_redo()` - Redo implementation

- `ai_sam/static/src/js/chat/chat_interaction.js` - Added Phase 5 activity states:
  - `undoing_action`, `redoing_action`
  - `action_undone`, `action_redone`
  - `recording_history`, `no_history`

---

## Executive Summary

Enable SAM AI to **read, edit, and create workflows** on the canvas through natural language conversation. Users will be able to describe what they want, and SAM will build/modify workflows in real-time.

**Vision:**
```
User: "Create a workflow that monitors my Gmail for invoices,
       extracts the data, and saves it to a Google Sheet"

SAM:  ✨ Creating workflow...
      ✨ Adding Gmail Trigger node...
      ✨ Adding Code node for extraction...
      ✨ Adding Google Sheets node...
      ✨ Connecting nodes...
      ✨ Done

      [Canvas updates in real-time as nodes appear]
```

---

## Current State Analysis

### What Exists

| Component | Status | Location |
|-----------|--------|----------|
| Canvas Model | ✅ Complete | `ai_sam_workflows_base/models/canvas.py` |
| Nodes Model | ✅ Complete | `ai_sam_workflows_base/models/nodes.py` |
| Connections Model | ✅ Complete | `ai_sam_workflows_base/models/workflow_connection.py` |
| N8N Node Types | ✅ 505+ nodes | `n8n.simple.node` table |
| Node Metadata | ✅ 195 types | `node_metadata.json` (781KB) |
| Canvas JS Manager | ✅ Complete | `canvas_manager.js`, `node_manager.js` |
| Save/Load Controllers | ✅ Complete | `/canvas/<id>/nodes/save`, `/canvas/<id>/nodes/load` |
| Canvas-level Chat | ✅ Partial | `chat_input.py` - `is_workflow_chat` detection |
| Workflow Context | ✅ Partial | `_gather_canvas_context()` reads `json_definition` |
| Canvas Tools | ❌ Missing | No tool definitions for SAM to manipulate canvas |
| Real-time Updates | ❌ Missing | No WebSocket push for canvas changes |
| Undo/Redo | ❌ Missing | No undo/redo system |

### Key Architecture Insight

**Single Source of Truth:** `canvas.json_definition` (Text field)
- Complete N8N-compatible JSON structure
- Frontend saves directly via `save_canvas_state()`
- No dual-storage complexity

---

## Implementation Phases

### Phase 1: Canvas Read Tools (Foundation)
**Goal:** SAM can intelligently query and understand workflows

### Phase 2: Canvas Edit Tools (Manipulation)
**Goal:** SAM can add, remove, modify nodes and connections

### Phase 3: Canvas Create Tools (Generation)
**Goal:** SAM can create complete workflows from descriptions

### Phase 4: Real-time Canvas Updates (UX Polish)
**Goal:** Canvas updates visually as SAM works

### Phase 5: Undo/Redo System (Safety)
**Goal:** Users and SAM can undo/redo changes

---

## Phase 1: Canvas Read Tools

### 1.1 Tool Definition: `canvas_read`

```python
# File: ai_sam_base/tools/canvas_tools.py

CANVAS_READ_TOOL = {
    "name": "canvas_read",
    "description": """Read and analyze the current workflow on the canvas.

    Use this tool to:
    - Get a list of all nodes in the workflow
    - Understand what each node does
    - See how nodes are connected
    - Find nodes by name or type
    - Analyze the workflow flow

    Returns structured information about the workflow that you can use
    to answer questions or plan modifications.""",

    "input_schema": {
        "type": "object",
        "properties": {
            "query_type": {
                "type": "string",
                "enum": ["full", "nodes", "connections", "node_by_id", "nodes_by_type", "flow_analysis"],
                "description": "Type of query to perform"
            },
            "node_id": {
                "type": "string",
                "description": "Node ID for node_by_id query"
            },
            "node_type": {
                "type": "string",
                "description": "Node type filter for nodes_by_type query (e.g., 'httpRequest', 'gmail')"
            }
        },
        "required": ["query_type"]
    }
}
```

### 1.2 Tool Handler Implementation

```python
# File: ai_sam_base/tools/canvas_tools.py

class CanvasReadTool:
    """Tool for reading and analyzing canvas workflows."""

    def __init__(self, env, canvas_id):
        self.env = env
        self.canvas_id = canvas_id
        self.canvas = env['canvas'].browse(canvas_id)

    def execute(self, query_type, node_id=None, node_type=None):
        """Execute a canvas read query."""

        if not self.canvas.exists():
            return {"error": f"Canvas {self.canvas_id} not found"}

        # Parse json_definition
        try:
            workflow = json.loads(self.canvas.json_definition or '{}')
        except json.JSONDecodeError:
            return {"error": "Invalid workflow JSON"}

        nodes = workflow.get('nodes', [])
        connections = workflow.get('connections', {})

        if query_type == "full":
            return self._get_full_analysis(nodes, connections)
        elif query_type == "nodes":
            return self._get_nodes_summary(nodes)
        elif query_type == "connections":
            return self._get_connections_summary(connections)
        elif query_type == "node_by_id":
            return self._get_node_by_id(nodes, node_id)
        elif query_type == "nodes_by_type":
            return self._get_nodes_by_type(nodes, node_type)
        elif query_type == "flow_analysis":
            return self._analyze_flow(nodes, connections)
        else:
            return {"error": f"Unknown query_type: {query_type}"}

    def _get_full_analysis(self, nodes, connections):
        """Get complete workflow analysis."""
        return {
            "workflow_name": self.canvas.name,
            "node_count": len(nodes),
            "connection_count": self._count_connections(connections),
            "nodes": self._get_nodes_summary(nodes)["nodes"],
            "connections": self._get_connections_summary(connections)["connections"],
            "triggers": [n for n in nodes if self._is_trigger(n)],
            "endpoints": self._find_endpoints(nodes, connections)
        }

    def _get_nodes_summary(self, nodes):
        """Get summary of all nodes."""
        return {
            "nodes": [
                {
                    "id": n.get("id"),
                    "name": n.get("name"),
                    "type": n.get("type", "").replace("n8n-nodes-base.", ""),
                    "position": n.get("position"),
                    "description": n.get("parameters", {}).get("description", "")[:100]
                }
                for n in nodes
            ]
        }

    def _get_connections_summary(self, connections):
        """Get summary of all connections."""
        result = []
        for source_id, targets in connections.items():
            if isinstance(targets, dict) and 'main' in targets:
                for output_idx, output_group in enumerate(targets['main']):
                    if isinstance(output_group, list):
                        for conn in output_group:
                            result.append({
                                "from": source_id,
                                "to": conn.get("node"),
                                "output_index": output_idx
                            })
        return {"connections": result}

    def _get_node_by_id(self, nodes, node_id):
        """Get detailed info for a specific node."""
        for node in nodes:
            if node.get("id") == node_id:
                return {"node": node}
        return {"error": f"Node {node_id} not found"}

    def _get_nodes_by_type(self, nodes, node_type):
        """Get all nodes of a specific type."""
        matching = [
            n for n in nodes
            if node_type.lower() in n.get("type", "").lower()
        ]
        return {"nodes": matching, "count": len(matching)}

    def _analyze_flow(self, nodes, connections):
        """Analyze the workflow execution flow."""
        # Build adjacency list
        graph = {}
        for source_id, targets in connections.items():
            if isinstance(targets, dict) and 'main' in targets:
                graph[source_id] = []
                for output_group in targets['main']:
                    if isinstance(output_group, list):
                        for conn in output_group:
                            graph[source_id].append(conn.get("node"))

        # Find triggers (nodes with no incoming connections)
        all_targets = set()
        for targets in graph.values():
            all_targets.update(targets)

        node_ids = {n.get("id") for n in nodes}
        triggers = node_ids - all_targets

        # Find endpoints (nodes with no outgoing connections)
        endpoints = node_ids - set(graph.keys())

        return {
            "triggers": list(triggers),
            "endpoints": list(endpoints),
            "graph": graph,
            "execution_order": self._topological_sort(graph, triggers)
        }

    def _topological_sort(self, graph, triggers):
        """Get execution order via topological sort."""
        visited = set()
        order = []

        def dfs(node_id):
            if node_id in visited:
                return
            visited.add(node_id)
            for next_node in graph.get(node_id, []):
                dfs(next_node)
            order.append(node_id)

        for trigger in triggers:
            dfs(trigger)

        return list(reversed(order))

    def _is_trigger(self, node):
        """Check if a node is a trigger."""
        node_type = node.get("type", "").lower()
        return "trigger" in node_type or "webhook" in node_type

    def _find_endpoints(self, nodes, connections):
        """Find workflow endpoint nodes."""
        all_targets = set()
        for targets in connections.values():
            if isinstance(targets, dict) and 'main' in targets:
                for output_group in targets['main']:
                    if isinstance(output_group, list):
                        for conn in output_group:
                            all_targets.add(conn.get("node"))

        node_ids = {n.get("id") for n in nodes}
        sources = set(connections.keys())
        endpoints = node_ids - sources

        return [n for n in nodes if n.get("id") in endpoints]

    def _count_connections(self, connections):
        """Count total connections."""
        count = 0
        for targets in connections.values():
            if isinstance(targets, dict) and 'main' in targets:
                for output_group in targets['main']:
                    if isinstance(output_group, list):
                        count += len(output_group)
        return count
```

### 1.3 Integration with AI Brain

```python
# File: ai_sam_base/models/ai_brain.py (modification)

# Add to available tools when in canvas context
def _get_available_tools(self, context_data):
    """Get tools available for this context."""
    tools = []

    # ... existing tools ...

    # Canvas tools when in workflow chat mode
    if context_data.get('is_workflow_chat') or context_data.get('canvas_id'):
        from odoo.addons.ai_sam_base.tools.canvas_tools import CANVAS_READ_TOOL
        tools.append(CANVAS_READ_TOOL)

    return tools
```

### 1.4 Activity States for Canvas Operations

```javascript
// File: ai_sam/static/src/js/chat/chat_interaction.js (addition)

// === CANVAS OPERATIONS ===
'reading_workflow':   { emoji: GOLD_STAR, message: 'Reading workflow...', color: GOLD_COLOR, isGoldStar: true },
'analyzing_nodes':    { emoji: GOLD_STAR, message: 'Analyzing nodes...', color: GOLD_COLOR, isGoldStar: true },
'tracing_connections': { emoji: GOLD_STAR, message: 'Tracing connections...', color: GOLD_COLOR, isGoldStar: true },
```

---

## Phase 2: Canvas Edit Tools

### 2.1 Tool Definition: `canvas_edit`

```python
CANVAS_EDIT_TOOL = {
    "name": "canvas_edit",
    "description": """Modify the workflow on the canvas.

    Use this tool to:
    - Add new nodes to the workflow
    - Remove existing nodes
    - Update node parameters
    - Add connections between nodes
    - Remove connections
    - Move nodes to new positions

    Changes are applied immediately and visible on the canvas.""",

    "input_schema": {
        "type": "object",
        "properties": {
            "action": {
                "type": "string",
                "enum": ["add_node", "remove_node", "update_node",
                         "add_connection", "remove_connection", "move_node"],
                "description": "Action to perform"
            },
            "node_type": {
                "type": "string",
                "description": "For add_node: N8N node type (e.g., 'n8n-nodes-base.httpRequest')"
            },
            "node_name": {
                "type": "string",
                "description": "Display name for the node"
            },
            "node_id": {
                "type": "string",
                "description": "Node ID for update/remove/move operations"
            },
            "position": {
                "type": "object",
                "properties": {
                    "x": {"type": "number"},
                    "y": {"type": "number"}
                },
                "description": "Canvas position [x, y] for add/move"
            },
            "parameters": {
                "type": "object",
                "description": "Node-specific parameters"
            },
            "connection": {
                "type": "object",
                "properties": {
                    "from_node": {"type": "string"},
                    "to_node": {"type": "string"},
                    "from_output": {"type": "integer", "default": 0},
                    "to_input": {"type": "integer", "default": 0}
                },
                "description": "For add/remove_connection"
            }
        },
        "required": ["action"]
    }
}
```

### 2.2 Tool Handler Implementation

```python
class CanvasEditTool:
    """Tool for editing canvas workflows."""

    def __init__(self, env, canvas_id):
        self.env = env
        self.canvas_id = canvas_id
        self.canvas = env['canvas'].browse(canvas_id)

    def execute(self, action, **kwargs):
        """Execute a canvas edit action."""

        if not self.canvas.exists():
            return {"error": f"Canvas {self.canvas_id} not found"}

        # Parse current workflow
        try:
            workflow = json.loads(self.canvas.json_definition or '{"nodes": [], "connections": {}}')
        except json.JSONDecodeError:
            workflow = {"nodes": [], "connections": {}}

        # Execute action
        if action == "add_node":
            result = self._add_node(workflow, **kwargs)
        elif action == "remove_node":
            result = self._remove_node(workflow, **kwargs)
        elif action == "update_node":
            result = self._update_node(workflow, **kwargs)
        elif action == "add_connection":
            result = self._add_connection(workflow, **kwargs)
        elif action == "remove_connection":
            result = self._remove_connection(workflow, **kwargs)
        elif action == "move_node":
            result = self._move_node(workflow, **kwargs)
        else:
            return {"error": f"Unknown action: {action}"}

        if result.get("error"):
            return result

        # Save updated workflow
        self.canvas.write({
            'json_definition': json.dumps(workflow)
        })

        # Push update to frontend (Phase 4)
        self._push_canvas_update(action, result)

        return result

    def _add_node(self, workflow, node_type, node_name, position=None, parameters=None, **kwargs):
        """Add a new node to the workflow."""

        # Generate unique node ID
        node_id = f"node-{uuid.uuid4().hex[:8]}"

        # Default position if not specified
        if not position:
            # Find a good position based on existing nodes
            position = self._calculate_next_position(workflow.get('nodes', []))

        # Create node structure (N8N compatible)
        new_node = {
            "id": node_id,
            "name": node_name,
            "type": node_type,
            "position": [position.get('x', 0), position.get('y', 0)],
            "typeVersion": 1,
            "parameters": parameters or {}
        }

        # Add to workflow
        if 'nodes' not in workflow:
            workflow['nodes'] = []
        workflow['nodes'].append(new_node)

        return {
            "success": True,
            "action": "add_node",
            "node": new_node
        }

    def _remove_node(self, workflow, node_id, **kwargs):
        """Remove a node and its connections."""

        nodes = workflow.get('nodes', [])
        original_count = len(nodes)

        # Remove node
        workflow['nodes'] = [n for n in nodes if n.get('id') != node_id]

        if len(workflow['nodes']) == original_count:
            return {"error": f"Node {node_id} not found"}

        # Remove connections involving this node
        connections = workflow.get('connections', {})

        # Remove outgoing connections
        if node_id in connections:
            del connections[node_id]

        # Remove incoming connections
        for source_id, targets in list(connections.items()):
            if isinstance(targets, dict) and 'main' in targets:
                for output_group in targets['main']:
                    if isinstance(output_group, list):
                        output_group[:] = [
                            conn for conn in output_group
                            if conn.get('node') != node_id
                        ]

        return {
            "success": True,
            "action": "remove_node",
            "node_id": node_id
        }

    def _update_node(self, workflow, node_id, parameters=None, node_name=None, **kwargs):
        """Update an existing node's parameters or name."""

        for node in workflow.get('nodes', []):
            if node.get('id') == node_id:
                if node_name:
                    node['name'] = node_name
                if parameters:
                    node['parameters'] = {**node.get('parameters', {}), **parameters}
                return {
                    "success": True,
                    "action": "update_node",
                    "node": node
                }

        return {"error": f"Node {node_id} not found"}

    def _add_connection(self, workflow, connection, **kwargs):
        """Add a connection between two nodes."""

        from_node = connection.get('from_node')
        to_node = connection.get('to_node')
        from_output = connection.get('from_output', 0)
        to_input = connection.get('to_input', 0)

        # Validate nodes exist
        node_ids = {n.get('id') for n in workflow.get('nodes', [])}
        if from_node not in node_ids:
            return {"error": f"Source node {from_node} not found"}
        if to_node not in node_ids:
            return {"error": f"Target node {to_node} not found"}

        # Initialize connections structure
        if 'connections' not in workflow:
            workflow['connections'] = {}

        if from_node not in workflow['connections']:
            workflow['connections'][from_node] = {'main': []}

        # Ensure enough output slots
        main = workflow['connections'][from_node]['main']
        while len(main) <= from_output:
            main.append([])

        # Add connection
        main[from_output].append({
            'node': to_node,
            'type': 'main',
            'index': to_input
        })

        return {
            "success": True,
            "action": "add_connection",
            "connection": {
                "from": from_node,
                "to": to_node,
                "from_output": from_output,
                "to_input": to_input
            }
        }

    def _remove_connection(self, workflow, connection, **kwargs):
        """Remove a connection between two nodes."""

        from_node = connection.get('from_node')
        to_node = connection.get('to_node')

        connections = workflow.get('connections', {})

        if from_node in connections:
            targets = connections[from_node]
            if isinstance(targets, dict) and 'main' in targets:
                for output_group in targets['main']:
                    if isinstance(output_group, list):
                        original_len = len(output_group)
                        output_group[:] = [
                            conn for conn in output_group
                            if conn.get('node') != to_node
                        ]
                        if len(output_group) < original_len:
                            return {
                                "success": True,
                                "action": "remove_connection",
                                "from": from_node,
                                "to": to_node
                            }

        return {"error": f"Connection from {from_node} to {to_node} not found"}

    def _move_node(self, workflow, node_id, position, **kwargs):
        """Move a node to a new position."""

        for node in workflow.get('nodes', []):
            if node.get('id') == node_id:
                node['position'] = [position.get('x', 0), position.get('y', 0)]
                return {
                    "success": True,
                    "action": "move_node",
                    "node_id": node_id,
                    "new_position": node['position']
                }

        return {"error": f"Node {node_id} not found"}

    def _calculate_next_position(self, nodes):
        """Calculate a good position for a new node."""
        if not nodes:
            return {'x': 250, 'y': 300}

        # Find rightmost node and add offset
        max_x = max(n.get('position', [0, 0])[0] for n in nodes)
        avg_y = sum(n.get('position', [0, 0])[1] for n in nodes) / len(nodes)

        return {'x': max_x + 250, 'y': avg_y}

    def _push_canvas_update(self, action, result):
        """Push update to frontend via WebSocket (Phase 4)."""
        # TODO: Implement in Phase 4
        pass
```

### 2.3 Node Type Lookup Tool

```python
CANVAS_NODE_TYPES_TOOL = {
    "name": "canvas_node_types",
    "description": """Search for available node types to add to the workflow.

    Use this to find the correct node type when you need to add a node.
    For example, to find email-related nodes, search for "email" or "gmail".""",

    "input_schema": {
        "type": "object",
        "properties": {
            "search": {
                "type": "string",
                "description": "Search term (e.g., 'gmail', 'http', 'spreadsheet')"
            },
            "category": {
                "type": "string",
                "description": "Category filter (e.g., 'Communication', 'Data', 'AI')"
            },
            "limit": {
                "type": "integer",
                "default": 10,
                "description": "Maximum results to return"
            }
        },
        "required": ["search"]
    }
}
```

---

## Phase 3: Canvas Create Tools

### 3.1 Tool Definition: `canvas_create`

```python
CANVAS_CREATE_TOOL = {
    "name": "canvas_create",
    "description": """Create a complete workflow from a description.

    Use this tool when the user describes a workflow they want to build.
    The tool will generate an appropriate workflow structure with nodes
    and connections based on the description.

    For complex workflows, this may create multiple nodes and connect them.""",

    "input_schema": {
        "type": "object",
        "properties": {
            "description": {
                "type": "string",
                "description": "Natural language description of the workflow"
            },
            "clear_existing": {
                "type": "boolean",
                "default": False,
                "description": "If true, clears existing nodes before creating"
            }
        },
        "required": ["description"]
    }
}
```

### 3.2 Workflow Generator Service

```python
# File: ai_sam_base/api_communications/workflow_generator.py

class WorkflowGenerator:
    """
    Generates workflow structures from natural language descriptions.

    Uses pattern matching and templates to create appropriate node configurations.
    """

    # Common workflow patterns
    PATTERNS = {
        'api_to_storage': {
            'triggers': ['monitor', 'watch', 'when', 'on'],
            'actions': ['save', 'store', 'write', 'add'],
            'template': 'api_fetch_transform_store'
        },
        'email_processing': {
            'triggers': ['email', 'gmail', 'outlook', 'inbox'],
            'actions': ['process', 'extract', 'analyze'],
            'template': 'email_trigger_process'
        },
        'data_transformation': {
            'triggers': ['transform', 'convert', 'map'],
            'actions': ['format', 'clean', 'normalize'],
            'template': 'data_transform_chain'
        },
        'notification': {
            'triggers': ['notify', 'alert', 'send'],
            'actions': ['slack', 'email', 'sms'],
            'template': 'trigger_notify'
        }
    }

    # Node templates
    TEMPLATES = {
        'api_fetch_transform_store': {
            'nodes': [
                {'type': 'n8n-nodes-base.httpRequest', 'name': 'Fetch Data'},
                {'type': 'n8n-nodes-base.code', 'name': 'Transform Data'},
                {'type': 'n8n-nodes-base.googleSheets', 'name': 'Save to Sheets'}
            ],
            'connections': [[0, 1], [1, 2]]
        },
        'email_trigger_process': {
            'nodes': [
                {'type': 'n8n-nodes-base.gmailTrigger', 'name': 'Email Trigger'},
                {'type': 'n8n-nodes-base.code', 'name': 'Extract Data'},
                {'type': 'n8n-nodes-base.set', 'name': 'Format Output'}
            ],
            'connections': [[0, 1], [1, 2]]
        }
    }

    def generate(self, description, env, canvas_id):
        """Generate a workflow from a description."""

        # Detect pattern
        pattern = self._detect_pattern(description)

        if pattern:
            return self._apply_template(pattern, description, env, canvas_id)
        else:
            # Fall back to AI-generated structure
            return self._generate_with_ai(description, env, canvas_id)

    def _detect_pattern(self, description):
        """Detect which workflow pattern matches the description."""
        description_lower = description.lower()

        for pattern_name, pattern in self.PATTERNS.items():
            trigger_match = any(t in description_lower for t in pattern['triggers'])
            action_match = any(a in description_lower for a in pattern['actions'])
            if trigger_match and action_match:
                return pattern['template']

        return None

    def _apply_template(self, template_name, description, env, canvas_id):
        """Apply a workflow template."""
        template = self.TEMPLATES.get(template_name)
        if not template:
            return {"error": f"Template {template_name} not found"}

        edit_tool = CanvasEditTool(env, canvas_id)
        created_nodes = []

        # Create nodes
        for i, node_def in enumerate(template['nodes']):
            position = {'x': 250 + (i * 250), 'y': 300}
            result = edit_tool.execute(
                action='add_node',
                node_type=node_def['type'],
                node_name=node_def['name'],
                position=position
            )
            if result.get('success'):
                created_nodes.append(result['node'])
            else:
                return result

        # Create connections
        for from_idx, to_idx in template['connections']:
            edit_tool.execute(
                action='add_connection',
                connection={
                    'from_node': created_nodes[from_idx]['id'],
                    'to_node': created_nodes[to_idx]['id']
                }
            )

        return {
            "success": True,
            "action": "create_workflow",
            "nodes_created": len(created_nodes),
            "nodes": created_nodes,
            "template_used": template_name
        }

    def _generate_with_ai(self, description, env, canvas_id):
        """Generate workflow structure using AI reasoning."""
        # This would use the AI to reason about the workflow structure
        # For now, return a message suggesting manual creation
        return {
            "success": False,
            "message": "Complex workflow detected. I'll help you build it step by step.",
            "suggested_approach": "manual_guided"
        }
```

---

## Phase 4: Real-time Canvas Updates

### 4.1 WebSocket Channel

```python
# File: ai_sam_workflows/channels/canvas_channel.py

from odoo.addons.bus.websocket import WebSocket

class CanvasChannel:
    """WebSocket channel for real-time canvas updates."""

    @staticmethod
    def get_channel_name(canvas_id):
        return f'canvas.{canvas_id}'

    @staticmethod
    def push_update(env, canvas_id, event_type, data):
        """Push an update to all clients viewing this canvas."""
        channel = CanvasChannel.get_channel_name(canvas_id)
        env['bus.bus']._sendone(channel, event_type, data)
```

### 4.2 Frontend Canvas Listener

```javascript
// File: ai_sam_workflows/static/src/n8n/canvas/canvas_realtime.js

class CanvasRealtimeSync {
    constructor(canvasId, canvasManager, nodeManager) {
        this.canvasId = canvasId;
        this.canvasManager = canvasManager;
        this.nodeManager = nodeManager;
        this.channel = `canvas.${canvasId}`;

        this._subscribe();
    }

    _subscribe() {
        // Subscribe to Odoo bus
        this.busService = this.env.services.bus_service;
        this.busService.addChannel(this.channel);
        this.busService.addEventListener('notification', this._onNotification.bind(this));
    }

    _onNotification(event) {
        const { type, payload } = event.detail;

        switch (type) {
            case 'canvas.node_added':
                this._handleNodeAdded(payload);
                break;
            case 'canvas.node_removed':
                this._handleNodeRemoved(payload);
                break;
            case 'canvas.node_updated':
                this._handleNodeUpdated(payload);
                break;
            case 'canvas.connection_added':
                this._handleConnectionAdded(payload);
                break;
            case 'canvas.connection_removed':
                this._handleConnectionRemoved(payload);
                break;
        }
    }

    _handleNodeAdded(payload) {
        const { node } = payload;

        // Add node with animation
        this.nodeManager.createNodeFromData(node, {
            animate: true,
            highlight: true,
            source: 'sam'  // Visual indicator that SAM added this
        });
    }

    _handleNodeRemoved(payload) {
        const { node_id } = payload;

        // Remove with fade-out animation
        this.nodeManager.removeNode(node_id, {
            animate: true
        });
    }

    _handleNodeUpdated(payload) {
        const { node } = payload;

        // Update with flash animation
        this.nodeManager.updateNode(node.id, node, {
            animate: true,
            flash: true
        });
    }

    _handleConnectionAdded(payload) {
        const { connection } = payload;

        // Draw connection with animation
        this.canvasManager.connectionManager.addConnection(
            connection.from,
            connection.to,
            { animate: true, color: 'gold' }  // Gold to show SAM's work
        );
    }

    _handleConnectionRemoved(payload) {
        const { from, to } = payload;

        // Remove with fade animation
        this.canvasManager.connectionManager.removeConnection(from, to, {
            animate: true
        });
    }
}
```

### 4.3 Activity States for Canvas Edits

```javascript
// Additional activity states for canvas manipulation
'adding_node':        { emoji: GOLD_STAR, message: 'Adding {node_name}...', color: GOLD_COLOR, isGoldStar: true },
'removing_node':      { emoji: GOLD_STAR, message: 'Removing {node_name}...', color: GOLD_COLOR, isGoldStar: true },
'connecting_nodes':   { emoji: GOLD_STAR, message: 'Connecting nodes...', color: GOLD_COLOR, isGoldStar: true },
'updating_node':      { emoji: GOLD_STAR, message: 'Updating {node_name}...', color: GOLD_COLOR, isGoldStar: true },
'creating_workflow':  { emoji: GOLD_STAR, message: 'Creating workflow...', color: GOLD_COLOR, isGoldStar: true },
```

---

## Phase 5: Undo/Redo System

### 5.1 Canvas History Model

```python
# File: ai_sam_workflows_base/models/canvas_history.py

class CanvasHistory(models.Model):
    _name = 'canvas.history'
    _description = 'Canvas Edit History'
    _order = 'create_date desc'

    canvas_id = fields.Many2one('canvas', required=True, ondelete='cascade')
    action_type = fields.Selection([
        ('add_node', 'Add Node'),
        ('remove_node', 'Remove Node'),
        ('update_node', 'Update Node'),
        ('add_connection', 'Add Connection'),
        ('remove_connection', 'Remove Connection'),
        ('move_node', 'Move Node'),
        ('bulk_edit', 'Bulk Edit'),
        ('create_workflow', 'Create Workflow'),
    ], required=True)

    # Snapshot of state before this action
    previous_state = fields.Text('Previous State (JSON)')

    # The action data (for replay)
    action_data = fields.Text('Action Data (JSON)')

    # Who performed the action
    performed_by = fields.Selection([
        ('user', 'User'),
        ('sam', 'SAM AI'),
    ], default='user')

    user_id = fields.Many2one('res.users', default=lambda self: self.env.user)

    # Undo state
    is_undone = fields.Boolean(default=False)

    def undo(self):
        """Undo this action by restoring previous state."""
        if self.is_undone:
            return {"error": "Already undone"}

        # Restore previous state
        self.canvas_id.write({
            'json_definition': self.previous_state
        })

        self.is_undone = True

        # Push update to canvas
        CanvasChannel.push_update(
            self.env,
            self.canvas_id.id,
            'canvas.state_restored',
            {'reason': 'undo', 'action_id': self.id}
        )

        return {"success": True, "action": "undo"}

    def redo(self):
        """Redo this action by re-applying it."""
        if not self.is_undone:
            return {"error": "Not undone, cannot redo"}

        # Re-apply the action
        action_data = json.loads(self.action_data)
        edit_tool = CanvasEditTool(self.env, self.canvas_id.id)
        result = edit_tool.execute(**action_data)

        if result.get('success'):
            self.is_undone = False

        return result
```

### 5.2 History Recording in Edit Tool

```python
# Modification to CanvasEditTool.execute()

def execute(self, action, performed_by='sam', **kwargs):
    """Execute a canvas edit action with history recording."""

    # Capture previous state
    previous_state = self.canvas.json_definition

    # Execute the action (existing code)
    result = self._execute_action(action, **kwargs)

    if result.get('success'):
        # Record in history
        self.env['canvas.history'].create({
            'canvas_id': self.canvas_id,
            'action_type': action,
            'previous_state': previous_state,
            'action_data': json.dumps({'action': action, **kwargs}),
            'performed_by': performed_by
        })

    return result
```

### 5.3 Undo/Redo Tools for SAM

```python
CANVAS_UNDO_TOOL = {
    "name": "canvas_undo",
    "description": "Undo the last canvas edit action.",
    "input_schema": {
        "type": "object",
        "properties": {
            "steps": {
                "type": "integer",
                "default": 1,
                "description": "Number of steps to undo"
            }
        }
    }
}

CANVAS_REDO_TOOL = {
    "name": "canvas_redo",
    "description": "Redo the last undone canvas edit action.",
    "input_schema": {
        "type": "object",
        "properties": {
            "steps": {
                "type": "integer",
                "default": 1,
                "description": "Number of steps to redo"
            }
        }
    }
}
```

---

## File Structure

```
ai_sam_base/
├── tools/
│   ├── __init__.py
│   ├── canvas_tools.py          # Tool definitions & handlers
│   └── tool_registry.py         # Tool registration
│
├── services/
│   └── workflow_generator.py    # Workflow generation from descriptions

ai_sam_workflows_base/
├── models/
│   └── canvas_history.py        # Undo/redo history model

ai_sam_workflows/
├── channels/
│   └── canvas_channel.py        # WebSocket real-time sync
│
├── static/src/n8n/canvas/
│   └── canvas_realtime.js       # Frontend real-time listener
```

---

## API Summary

### Canvas Tools for SAM

| Tool | Purpose | Phase |
|------|---------|-------|
| `canvas_read` | Query workflow structure | 1 |
| `canvas_node_types` | Search available node types | 2 |
| `canvas_edit` | Add/remove/update nodes & connections | 2 |
| `canvas_create` | Create complete workflow from description | 3 |
| `canvas_undo` | Undo last action | 5 |
| `canvas_redo` | Redo last undone action | 5 |

### Real-time Events

| Event | Payload | Purpose |
|-------|---------|---------|
| `canvas.node_added` | `{node: {...}}` | Node was added |
| `canvas.node_removed` | `{node_id: "..."}` | Node was removed |
| `canvas.node_updated` | `{node: {...}}` | Node was modified |
| `canvas.connection_added` | `{connection: {...}}` | Connection created |
| `canvas.connection_removed` | `{from: "...", to: "..."}` | Connection removed |
| `canvas.state_restored` | `{reason: "undo"}` | State was restored |

---

## Testing Strategy

### Phase 1 Tests
- [ ] `canvas_read` returns correct node count
- [ ] `canvas_read` finds nodes by type
- [ ] `canvas_read` traces connections correctly
- [ ] Flow analysis identifies triggers and endpoints

### Phase 2 Tests
- [ ] `canvas_edit` add_node creates valid node
- [ ] `canvas_edit` remove_node cleans up connections
- [ ] `canvas_edit` add_connection validates nodes exist
- [ ] Position calculation works for new nodes

### Phase 3 Tests
- [ ] Pattern detection identifies common workflows
- [ ] Templates create correct node structures
- [ ] Connections are created in correct order

### Phase 4 Tests
- [ ] WebSocket events reach frontend
- [ ] Canvas updates without page refresh
- [ ] Multiple viewers see same updates

### Phase 5 Tests
- [ ] Undo restores previous state
- [ ] Redo reapplies action correctly
- [ ] History records all actions
- [ ] SAM-initiated actions are labeled

---

## Success Metrics

1. **User Experience**
   - SAM can answer "What does this workflow do?" accurately
   - SAM can add nodes within 2 seconds of request
   - Canvas updates visually in real-time
   - Undo works reliably for all edit types

2. **Reliability**
   - No data loss on concurrent edits
   - Graceful handling of invalid requests
   - Clear error messages when operations fail

3. **Performance**
   - Read operations < 100ms
   - Edit operations < 500ms
   - Real-time updates < 200ms latency

---

## Next Steps

1. **Review this plan** - Confirm architecture decisions
2. **Implement Phase 1** - Canvas read tools (foundation)
3. **Test with users** - Validate the read experience
4. **Proceed to Phase 2** - Canvas edit tools
5. **Iterate based on feedback**

---

*Plan created: 2025-12-21*
*Last updated: 2025-12-21*
