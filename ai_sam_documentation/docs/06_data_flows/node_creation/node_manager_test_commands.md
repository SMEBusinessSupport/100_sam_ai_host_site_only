# Node Manager Test Commands

**Purpose:** Test the new n8n bridge methods in node_manager.js
**Status:** Ready to test
**Date:** 2025-09-30

---

## Browser Console Test Commands

Copy and paste these commands into your browser console to test the bridge methods.

### Pre-Test: Verify Node Manager is Ready

```javascript
// Check if NodeManager is initialized
console.log('NodeManager initialized?', window.nodeManager?.initialized);

// Check if canvas viewport is available
console.log('Canvas viewport?', window.nodeManager?.canvasViewport);

// Check current node count
console.log('Current nodes:', window.nodeManager?.nodes.size);
```

**Expected Results:**
- `NodeManager initialized? true`
- `Canvas viewport? HTMLDivElement` (or similar)
- `Current nodes: 0` (or current count)

---

## Test 1: Single Action Node (Gmail)

```javascript
// Test data: Gmail Send Message action node
const gmailNode = {
    id: "test-gmail-001",
    name: "Send Email",
    type: "n8n-nodes-base.gmail",
    typeVersion: 1,
    position: [150, 150],
    parameters: {
        resource: "message",
        operation: "send"
    }
};

// Call bridge method
const node1 = window.nodeManager.addNodeFromN8nJSON(gmailNode);

// Verify
console.log('Created node:', node1);
console.log('Total nodes:', window.nodeManager.nodes.size);
```

**Expected Results:**
- Console shows: `✅ [N8N Bridge] Successfully added n8n node: Send Email`
- Console shows: `📊 [N8N Bridge] Detected type: action from n8n type: n8n-nodes-base.gmail`
- Blue action node appears on canvas at position [150, 150]
- Node header shows: "⚡ ACTION"
- Node content shows: "Send Email"
- Node description shows: "Resource: message | Operation: send"

---

## Test 2: Trigger Node (Webhook)

```javascript
// Test data: Webhook trigger node
const webhookNode = {
    id: "test-webhook-001",
    name: "Webhook Trigger",
    type: "n8n-nodes-base.webhook",
    typeVersion: 1,
    position: [150, 350],
    parameters: {
        path: "/webhook",
        method: "POST"
    }
};

// Call bridge method
const node2 = window.nodeManager.addNodeFromN8nJSON(webhookNode);

// Verify
console.log('Created node:', node2);
console.log('Node type:', node2.type);
```

**Expected Results:**
- Console shows: `✅ [N8N Bridge] Successfully added n8n node: Webhook Trigger`
- Console shows: `📊 [N8N Bridge] Detected type: trigger from n8n type: n8n-nodes-base.webhook`
- Green trigger node appears on canvas at position [150, 350]
- Node header shows: "🔄 TRIGGER"
- Node content shows: "Webhook Trigger"
- Node description shows: "Path: /webhook | Method: POST"

---

## Test 3: Multiple Nodes (Different Types)

```javascript
// Test data: Mix of action and trigger nodes
const slackNode = {
    id: "test-slack-001",
    name: "Send Slack Message",
    type: "n8n-nodes-base.slack",
    typeVersion: 1,
    position: [400, 150],
    parameters: {
        resource: "message",
        operation: "post"
    }
};

const scheduleNode = {
    id: "test-schedule-001",
    name: "Every 5 Minutes",
    type: "n8n-nodes-base.scheduleTrigger",
    typeVersion: 1,
    position: [400, 350],
    parameters: {
        rule: {
            interval: [{
                field: "minutes",
                minutesInterval: 5
            }]
        }
    }
};

// Add both nodes
const node3 = window.nodeManager.addNodeFromN8nJSON(slackNode);
const node4 = window.nodeManager.addNodeFromN8nJSON(scheduleNode);

// Verify
console.log('Total nodes now:', window.nodeManager.nodes.size);
console.log('All nodes:', window.nodeManager.getAllNodes().map(n => ({
    name: n.name,
    type: n.type,
    n8nType: n.n8nType
})));
```

**Expected Results:**
- 2 more nodes appear on canvas
- Slack node: Blue action node at [400, 150]
- Schedule node: Green trigger node at [400, 350]
- Console shows: `Total nodes now: 4`

---

## Test 4: Batch Import (Full Workflow)

```javascript
// Test data: Complete n8n workflow
const workflow = {
    nodes: [
        {
            id: "workflow-node-1",
            name: "HTTP Request",
            type: "n8n-nodes-base.httpRequest",
            typeVersion: 1,
            position: [650, 150],
            parameters: {
                method: "GET",
                url: "https://api.example.com/data"
            }
        },
        {
            id: "workflow-node-2",
            name: "Set Variables",
            type: "n8n-nodes-base.set",
            typeVersion: 1,
            position: [650, 300],
            parameters: {
                operation: "set",
                values: {}
            }
        },
        {
            id: "workflow-node-3",
            name: "Condition",
            type: "n8n-nodes-base.if",
            typeVersion: 1,
            position: [650, 450],
            parameters: {
                conditions: {}
            }
        }
    ],
    connections: {},
    meta: {
        instanceId: "test-workflow-001"
    }
};

// Call batch method
const createdNodes = window.nodeManager.addNodesFromN8nWorkflow(workflow);

// Verify
console.log('Created nodes from workflow:', createdNodes.length);
console.log('Total nodes now:', window.nodeManager.nodes.size);
```

**Expected Results:**
- Console shows: `✅ [N8N Bridge] Added 3 of 3 nodes from workflow`
- 3 new nodes appear on canvas
- All at different vertical positions (150, 300, 450)
- All at same horizontal position (650)

---

## Test 5: Edge Cases

### Test 5a: Invalid Data
```javascript
// Test with invalid data
const invalidNode = window.nodeManager.addNodeFromN8nJSON({});
console.log('Invalid node result:', invalidNode);  // Should be null

const invalidNode2 = window.nodeManager.addNodeFromN8nJSON(null);
console.log('Null node result:', invalidNode2);  // Should be null
```

**Expected Results:**
- Console shows: `❌ [N8N Bridge] Invalid n8n node data`
- Returns `null`
- No node added to canvas

### Test 5b: Missing Position (Use Default)
```javascript
// Test with missing position
const nodeNoPosition = {
    id: "test-no-pos-001",
    name: "No Position Node",
    type: "n8n-nodes-base.httpRequest",
    typeVersion: 1,
    // position omitted
    parameters: {}
};

const node5 = window.nodeManager.addNodeFromN8nJSON(nodeNoPosition);
console.log('Node position:', node5.position);
```

**Expected Results:**
- Node appears at default position {x: 100, y: 100}
- Console shows: `📍 [N8N Bridge] Position converted: undefined → {x: 100, y: 100}`

### Test 5c: Position as Object (Already Correct Format)
```javascript
// Test with position as object instead of array
const nodeObjectPosition = {
    id: "test-obj-pos-001",
    name: "Object Position Node",
    type: "n8n-nodes-base.httpRequest",
    typeVersion: 1,
    position: { x: 900, y: 200 },  // Object format instead of array
    parameters: {}
};

const node6 = window.nodeManager.addNodeFromN8nJSON(nodeObjectPosition);
console.log('Node position:', node6.position);
```

**Expected Results:**
- Node appears at position {x: 900, y: 200}
- Position conversion handles both formats correctly

---

## Test 6: Node Interactions (After Creation)

```javascript
// Test that created nodes are interactive

// Get a node
const testNode = window.nodeManager.getAllNodes()[0];

// Test selection
console.log('Selecting node:', testNode.name);
window.nodeManager.selectNode(testNode.id);
// Expected: Node border turns blue

// Test getting selected nodes
console.log('Selected nodes:', window.nodeManager.getSelectedNodes());

// Test state export
const state = window.nodeManager.getNodesState();
console.log('Current state:', state);
```

---

## Test 7: Type Detection Verification

```javascript
// Test various n8n types to verify trigger detection
const typeTests = [
    { type: 'n8n-nodes-base.webhook', expected: 'trigger' },
    { type: 'n8n-nodes-base.webhookTrigger', expected: 'trigger' },
    { type: 'n8n-nodes-base.scheduleTrigger', expected: 'trigger' },
    { type: 'n8n-nodes-base.manualTrigger', expected: 'trigger' },
    { type: 'n8n-nodes-base.cronTrigger', expected: 'trigger' },
    { type: 'n8n-nodes-base.pollTrigger', expected: 'trigger' },
    { type: 'n8n-nodes-base.gmail', expected: 'action' },
    { type: 'n8n-nodes-base.httpRequest', expected: 'action' },
    { type: 'n8n-nodes-base.set', expected: 'action' },
    { type: 'n8n-nodes-base.if', expected: 'action' },
];

console.log('Testing type detection:');
typeTests.forEach((test, index) => {
    const node = {
        id: `type-test-${index}`,
        name: `Type Test ${index}`,
        type: test.type,
        position: [1000 + (index * 50), 150 + (index * 100)],
        parameters: {}
    };

    const created = window.nodeManager.addNodeFromN8nJSON(node);
    const actualType = created.type;
    const passed = actualType === test.expected;

    console.log(`${passed ? '✅' : '❌'} ${test.type} → Expected: ${test.expected}, Got: ${actualType}`);
});
```

**Expected Results:**
- All tests pass (✅)
- Webhook, schedule, cron, poll triggers detected correctly
- Regular nodes detected as actions

---

## Cleanup Commands

```javascript
// Clear all nodes
window.nodeManager.clearAllNodes();
console.log('Cleared all nodes. Count:', window.nodeManager.nodes.size);

// Verify canvas is empty
console.log('Remaining DOM nodes:', document.querySelectorAll('.canvas-node').length);
```

---

## Quick Test Suite (All-in-One)

```javascript
// Run all basic tests in sequence
(async function testNodeManager() {
    console.log('🧪 Starting Node Manager Test Suite...\n');

    // Clear existing nodes
    window.nodeManager.clearAllNodes();

    // Test 1: Action node
    console.log('Test 1: Action node (Gmail)');
    const gmail = window.nodeManager.addNodeFromN8nJSON({
        id: "test-1",
        name: "Send Email",
        type: "n8n-nodes-base.gmail",
        position: [100, 100],
        parameters: { resource: "message", operation: "send" }
    });
    console.log(gmail ? '✅ PASS' : '❌ FAIL', '\n');

    // Test 2: Trigger node
    console.log('Test 2: Trigger node (Webhook)');
    const webhook = window.nodeManager.addNodeFromN8nJSON({
        id: "test-2",
        name: "Webhook",
        type: "n8n-nodes-base.webhook",
        position: [100, 250],
        parameters: { path: "/webhook" }
    });
    console.log(webhook && webhook.type === 'trigger' ? '✅ PASS' : '❌ FAIL', '\n');

    // Test 3: Batch import
    console.log('Test 3: Batch import (3 nodes)');
    const batch = window.nodeManager.addNodesFromN8nWorkflow({
        nodes: [
            { id: "b1", name: "Node 1", type: "n8n-nodes-base.httpRequest", position: [300, 100], parameters: {} },
            { id: "b2", name: "Node 2", type: "n8n-nodes-base.set", position: [300, 250], parameters: {} },
            { id: "b3", name: "Node 3", type: "n8n-nodes-base.if", position: [300, 400], parameters: {} }
        ]
    });
    console.log(batch.length === 3 ? '✅ PASS' : '❌ FAIL', '\n');

    // Test 4: Invalid data
    console.log('Test 4: Invalid data handling');
    const invalid = window.nodeManager.addNodeFromN8nJSON(null);
    console.log(invalid === null ? '✅ PASS' : '❌ FAIL', '\n');

    // Summary
    const totalNodes = window.nodeManager.nodes.size;
    console.log(`\n📊 Test Summary:`);
    console.log(`Total nodes created: ${totalNodes} (expected: 5)`);
    console.log(`Test suite: ${totalNodes === 5 ? '✅ PASSED' : '❌ FAILED'}`);

    return totalNodes === 5;
})();
```

---

## Debugging Commands

```javascript
// If something doesn't work, use these to debug:

// 1. Check NodeManager state
console.log('NodeManager:', window.nodeManager);
console.log('Initialized:', window.nodeManager?.initialized);
console.log('Nodes:', window.nodeManager?.nodes);

// 2. Check canvas viewport
console.log('Viewport:', window.nodeManager?.canvasViewport);
console.log('Viewport parent:', window.nodeManager?.canvasViewport?.parentElement);

// 3. Check for errors in last operation
// (Look in console for red error messages)

// 4. List all nodes
console.table(window.nodeManager.getAllNodes().map(n => ({
    id: n.id,
    name: n.name,
    type: n.type,
    n8nType: n.n8nType,
    x: n.position.x,
    y: n.position.y
})));

// 5. Check DOM elements
console.log('Canvas nodes in DOM:', document.querySelectorAll('.canvas-node').length);
document.querySelectorAll('.canvas-node').forEach(el => {
    console.log('- Node:', el.querySelector('.node-name')?.textContent);
});
```

---

## Integration Test with Overlay Manager

```javascript
// Simulate what overlay_manager.js will do

// Mock the overlay JSON output
const overlayOutput = {
    nodes: [{
        parameters: { resource: "message", operation: "send" },
        type: "n8n-nodes-base.gmail",
        typeVersion: 1,
        position: [250, 250],
        id: "overlay-test-001",
        name: "Send Email from Overlay"
    }],
    connections: {},
    pinData: {},
    meta: { instanceId: "integration-test" }
};

// This is what overlay_manager.js line 3401 will do:
const nodeData = overlayOutput.nodes[0];
const result = window.nodeManager.addNodeFromN8nJSON(nodeData);

console.log('Integration test result:', result ? '✅ SUCCESS' : '❌ FAILED');
console.log('Node visible on canvas?', document.querySelector(`[data-node-id="${result.id}"]`) !== null);
```

**Expected Results:**
- Console shows: `✅ [N8N Bridge] Successfully added n8n node: Send Email from Overlay`
- Node appears on canvas
- Integration test: ✅ SUCCESS

---

## Performance Test

```javascript
// Test creating many nodes quickly
console.time('Create 20 nodes');

const nodes = [];
for (let i = 0; i < 20; i++) {
    const node = {
        id: `perf-test-${i}`,
        name: `Node ${i}`,
        type: "n8n-nodes-base.httpRequest",
        position: [100 + (i % 5) * 200, 100 + Math.floor(i / 5) * 150],
        parameters: {}
    };
    nodes.push(window.nodeManager.addNodeFromN8nJSON(node));
}

console.timeEnd('Create 20 nodes');
console.log('All nodes created:', nodes.filter(n => n !== null).length);
console.log('Performance: Should complete in < 1 second');
```

---

## Status Report

After running tests, generate a status report:

```javascript
console.log('\n📋 Node Manager Status Report\n' + '='.repeat(50));
console.log(`Initialized: ${window.nodeManager?.initialized ? '✅' : '❌'}`);
console.log(`Canvas Viewport: ${window.nodeManager?.canvasViewport ? '✅' : '❌'}`);
console.log(`Total Nodes: ${window.nodeManager?.nodes.size || 0}`);
console.log(`Bridge Method Available: ${typeof window.nodeManager?.addNodeFromN8nJSON === 'function' ? '✅' : '❌'}`);
console.log(`Helper Method Available: ${typeof window.nodeManager?.buildNodeDescription === 'function' ? '✅' : '❌'}`);
console.log(`Batch Method Available: ${typeof window.nodeManager?.addNodesFromN8nWorkflow === 'function' ? '✅' : '❌'}`);
console.log('='.repeat(50));
```

---

## Next Step: Test Your Overlay Integration

Once these tests pass, test with your actual overlay:

1. Click the "N8N Node" button
2. Select a platform (e.g., Gmail)
3. Select an operation (e.g., Send Message)
4. Check if node appears on canvas
5. Open console and look for: `✅ [N8N Bridge] Successfully added n8n node`

If you see that message and the node appears → **SUCCESS! Integration complete!** 🎉