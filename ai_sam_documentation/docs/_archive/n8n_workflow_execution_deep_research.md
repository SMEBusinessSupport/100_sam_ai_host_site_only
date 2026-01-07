# 🚀 n8n Workflow Execution - Deep Research Documentation
## For The AI Automator Odoo Module

**Research Date**: October 1, 2025
**n8n Version Studied**: 1.108.2
**Purpose**: Understanding how n8n executes workflows, handles triggers, and manages execution state for implementation in The AI Automator

---

## 📖 Table of Contents

1. [Executive Summary](#executive-summary)
2. [n8n Execution Architecture](#n8n-execution-architecture)
3. [Trigger Types & Trigger Points](#trigger-types--trigger-points)
4. [Execution Modes](#execution-modes)
5. [Execution Lifecycle & Flow](#execution-lifecycle--flow)
6. [Data Flow Between Nodes](#data-flow-between-nodes)
7. [Queue Mode & Worker System](#queue-mode--worker-system)
8. [Execution Database Schema](#execution-database-schema)
9. [Execution State Management](#execution-state-management)
10. [Error Handling & Recovery](#error-handling--recovery)
11. [Wait Node & Execution Resumption](#wait-node--execution-resumption)
12. [Workflow Activation Lifecycle](#workflow-activation-lifecycle)
13. [n8n Source Code Architecture](#n8n-source-code-architecture)
14. [Implementation Recommendations](#implementation-recommendations)

---

## Executive Summary

### 🎯 Key Findings

**n8n's execution system** is a sophisticated workflow orchestration engine that:

1. **Supports Multiple Trigger Types**: Manual, Webhook, Schedule/Cron, Polling, Event-based, Sub-workflow, and Instance triggers
2. **Three Execution Modes**: Manual (testing), Partial (node-level), and Production (automatic)
3. **Distributed Architecture**: Queue mode with Redis + Bull queue for horizontal scaling
4. **Five Execution States**: Running, Waiting, Success, Error, Cancelled
5. **Resumable Executions**: Wait nodes pause execution and resume via webhooks
6. **Data Structure**: Items as JSON objects flow between nodes in standardized format
7. **Error Recovery**: Retry on fail, continue on fail, error workflows, and execution recovery
8. **State Persistence**: Full execution state stored in `execution_entity` table for recovery

### 📊 n8n Execution Performance

- **Single Instance**: Up to 220 workflow executions per second
- **Queue Mode**: Horizontal scaling with unlimited workers
- **Execution Storage**: SQLite (default) or PostgreSQL (production/queue mode)
- **Redis Queue**: Bull queue library for distributed job management

---

## n8n Execution Architecture

### 🏗️ High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    n8n EXECUTION SYSTEM                     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐ │
│  │   TRIGGER    │───▶│   WORKFLOW   │───▶│  EXECUTION   │ │
│  │    LAYER     │    │    ENGINE    │    │    LAYER     │ │
│  └──────────────┘    └──────────────┘    └──────────────┘ │
│         │                    │                    │        │
│         │                    │                    │        │
│         ▼                    ▼                    ▼        │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐ │
│  │   Webhook    │    │WorkflowRunner│    │   Database   │ │
│  │   Schedule   │    │WorkflowExecute│    │execution_entity│
│  │   Polling    │    │ Node Runner  │    │  Redis Queue │ │
│  │   Manual     │    │ Hook System  │    │  State Store │ │
│  └──────────────┘    └──────────────┘    └──────────────┘ │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 🔧 Core Components

#### 1. **WorkflowRunner** (Main Orchestrator)
- **File**: `packages/cli/src/WorkflowRunner.ts`
- **Purpose**: Manages workflow execution lifecycle
- **Responsibilities**:
  - Receives execution requests from triggers
  - Initializes execution environment
  - Routes to appropriate execution mode (direct or queue)
  - Manages execution hooks and events

#### 2. **WorkflowExecute** (Execution Engine)
- **File**: `packages/core/src/WorkflowExecute.ts`
- **Purpose**: Core execution engine that runs workflows
- **Key Methods**:
  ```typescript
  class WorkflowExecute {
    constructor(additionalData, mode, runExecutionData)
    async processRunExecutionData(workflow): Promise<IRun>
    async run(): Promise<IRun>
  }
  ```
- **Responsibilities**:
  - Loads node types and initializes workflow
  - Manages node execution stack
  - Processes run execution data
  - Handles data flow between nodes
  - Emits execution hooks (before/after events)

#### 3. **Node Runner**
- **Purpose**: Executes individual nodes
- **Responsibilities**:
  - Loads node implementation
  - Validates input data
  - Executes node logic
  - Handles node errors
  - Returns output data

#### 4. **Hook System**
- **Purpose**: Event-driven execution monitoring
- **Events**:
  - `workflowExecuteBefore`: Before workflow starts
  - `workflowExecuteAfter`: After workflow completes
  - `nodeExecuteBefore`: Before node runs
  - `nodeExecuteAfter`: After node completes

---

## Trigger Types & Trigger Points

### 🎯 n8n Trigger Types

n8n supports **7 primary trigger types** that initiate workflow executions:

#### 1. **Manual Trigger**
- **Node**: `Manual Trigger` (`n8n-nodes-base.manualWorkflowTrigger`)
- **Purpose**: Start workflow manually from UI
- **Use Case**: Testing workflows before adding automatic triggers
- **Execution Mode**: Manual execution only
- **Characteristics**:
  - Only runs when "Execute Workflow" button is clicked
  - No automatic execution
  - Useful for development and debugging

```json
{
  "id": "node_1",
  "name": "When clicking \"Test workflow\"",
  "type": "n8n-nodes-base.manualTrigger",
  "position": [250, 300],
  "parameters": {},
  "typeVersion": 1
}
```

#### 2. **Webhook Trigger**
- **Node**: `Webhook` (`n8n-nodes-base.webhook`)
- **Purpose**: Receive HTTP requests to trigger workflow
- **Execution Mode**: Production execution
- **URLs**:
  - **Test URL**: Active during manual testing
  - **Production URL**: Active when workflow is activated
- **Characteristics**:
  - Listens for incoming HTTP requests
  - Supports GET, POST, PUT, DELETE, PATCH
  - Can authenticate requests
  - Returns response via "Respond to Webhook" node

**Webhook URL Structure**:
```
Test URL: http://localhost:5678/webhook-test/workflow-id
Production URL: http://localhost:5678/webhook/workflow-id
```

**Webhook Node Configuration**:
```json
{
  "id": "node_1",
  "name": "Webhook",
  "type": "n8n-nodes-base.webhook",
  "parameters": {
    "path": "my-webhook",
    "httpMethod": "POST",
    "authentication": "none",
    "responseMode": "onReceived"
  },
  "typeVersion": 1
}
```

#### 3. **Schedule Trigger (Cron)**
- **Node**: `Schedule Trigger` (`n8n-nodes-base.scheduleTrigger`)
- **Purpose**: Run workflows at fixed intervals/times
- **Execution Mode**: Production execution
- **Scheduling Options**:
  - Seconds, Minutes, Hours, Days
  - Cron expression support
  - Custom intervals
- **Important Notes**:
  - **Activation Required**: Workflow must be activated for schedule to work
  - **Variable Evaluation**: Schedule values evaluated only on activation
  - **Update Behavior**: Changes to schedule require workflow re-activation

**Schedule Trigger Configuration**:
```json
{
  "id": "node_1",
  "name": "Every morning at 9am",
  "type": "n8n-nodes-base.scheduleTrigger",
  "parameters": {
    "rule": {
      "interval": [
        {
          "field": "hours",
          "hoursInterval": 9
        }
      ]
    },
    "cronExpression": "0 9 * * *"
  },
  "typeVersion": 1
}
```

#### 4. **Polling Triggers**
- **Purpose**: Periodically check for new data from services without webhook support
- **Mechanism**: Schedule Trigger + API request to fetch new items
- **Implementation Pattern**:
  ```
  Schedule Trigger → HTTP Request → Filter (new items only) → Process
  ```
- **Common Use Cases**:
  - Email checking (IMAP)
  - RSS feed monitoring
  - Database polling
  - File system monitoring

**Polling Pattern Example**:
```json
{
  "nodes": [
    {
      "id": "schedule_1",
      "name": "Every 5 minutes",
      "type": "n8n-nodes-base.scheduleTrigger",
      "parameters": {
        "rule": {
          "interval": [{"field": "minutes", "minutesInterval": 5}]
        }
      }
    },
    {
      "id": "http_1",
      "name": "Check for new items",
      "type": "n8n-nodes-base.httpRequest",
      "parameters": {
        "url": "https://api.example.com/items",
        "method": "GET"
      }
    }
  ]
}
```

#### 5. **Event-Based Triggers (App-Specific)**
- **Purpose**: Start workflow when specific events occur in connected apps
- **Examples**:
  - Gmail Trigger: New email received
  - Slack Trigger: New message in channel
  - Google Sheets Trigger: New row added
  - GitHub Trigger: New pull request
- **Mechanism**: Most use webhooks registered with the service

**Example - Gmail Trigger**:
```json
{
  "id": "node_1",
  "name": "Gmail Trigger",
  "type": "n8n-nodes-base.gmailTrigger",
  "parameters": {
    "event": "messageReceived",
    "filters": {
      "labelIds": ["INBOX"],
      "includeSpam": false
    }
  },
  "credentials": {
    "gmailOAuth2": {
      "id": "1",
      "name": "Gmail account"
    }
  },
  "typeVersion": 1
}
```

#### 6. **Sub-Workflow Triggers**
- **Node**: `Execute Sub-workflow Trigger` (`n8n-nodes-base.executeWorkflowTrigger`)
- **Purpose**: Start workflow when called by another workflow
- **Parent Node**: `Execute Sub-workflow` node
- **Data Flow**:
  ```
  Parent Workflow → Execute Sub-workflow Node → Sub-workflow Trigger → Sub-workflow Nodes → Return to Parent
  ```
- **Execution Modes**:
  - **Run once with all items**: Pass all items in single execution
  - **Run once for each item**: Execute sub-workflow per item
- **Wait Options**:
  - **Wait for completion**: Parent waits for sub-workflow
  - **Don't wait**: Parent continues immediately

**Sub-Workflow Setup**:
```json
// Parent Workflow
{
  "id": "execute_sub_1",
  "name": "Execute Sub-workflow",
  "type": "n8n-nodes-base.executeWorkflow",
  "parameters": {
    "workflowId": "456",
    "mode": "runOnceForAllItems",
    "waitForCompletion": true
  }
}

// Sub-Workflow
{
  "id": "trigger_1",
  "name": "Execute Sub-workflow Trigger",
  "type": "n8n-nodes-base.executeWorkflowTrigger",
  "parameters": {}
}
```

#### 7. **n8n Instance Triggers**
- **Node**: `n8n Trigger` (`n8n-nodes-base.n8nTrigger`)
- **Purpose**: React to n8n system events
- **Events**:
  - **Instance Started**: n8n starts/restarts
  - **Workflow Activated**: Workflow is activated
  - **Workflow Updated**: Active workflow is updated
- **Use Cases**:
  - Initialization tasks
  - Sending notifications on workflow changes
  - Maintenance workflows

**n8n Trigger Configuration**:
```json
{
  "id": "node_1",
  "name": "n8n Trigger",
  "type": "n8n-nodes-base.n8nTrigger",
  "parameters": {
    "events": ["workflowActivated", "init"]
  },
  "typeVersion": 1
}
```

### 🔄 Trigger Point Summary

| Trigger Type | Execution Mode | Requires Activation | Characteristics |
|-------------|----------------|-------------------|-----------------|
| Manual | Manual | No | On-demand testing |
| Webhook | Production | Yes | HTTP request triggered |
| Schedule (Cron) | Production | Yes | Time-based intervals |
| Polling | Production | Yes | Periodic API checks |
| Event-Based | Production | Yes | App-specific events |
| Sub-Workflow | Both | No (parent triggered) | Called by parent workflow |
| n8n Instance | Production | Yes | System events |

---

## Execution Modes

### 🎮 Three Primary Execution Modes

#### 1. **Manual Execution**
- **Purpose**: Testing workflows during development
- **Characteristics**:
  - Runs entire workflow from trigger to last node
  - Displays data in UI as it flows
  - Can use pinned data for consistent testing
  - Activated by "Execute Workflow" button
  - Does NOT require workflow activation
- **Visibility**: Full execution flow shown in Editor tab
- **Data Display**: Live updates as nodes execute
- **Pinned Data**: Can pin data to nodes for testing

**Use Cases**:
- Workflow development
- Debugging
- Testing parameter changes
- Validating logic flow

#### 2. **Partial Execution**
- **Purpose**: Execute specific node and its dependencies
- **Characteristics**:
  - Runs only selected node + preceding required nodes
  - Fills in input data by executing dependencies
  - Faster than full workflow execution
  - Activated by "Execute Step" button on node
- **Visibility**: Shows execution path to selected node
- **Use Cases**:
  - Testing individual nodes
  - Debugging specific transformations
  - Validating node configuration

**How to Perform Partial Execution**:
1. Select a node
2. Open node detail view
3. Click "Execute Step"
4. n8n executes node + dependencies

#### 3. **Production Execution**
- **Purpose**: Automatic workflow execution in production
- **Characteristics**:
  - Triggered by non-manual triggers (webhook, cron, etc.)
  - Workflow must be activated
  - No live UI updates during execution
  - Execution data saved to database
  - **IGNORES pinned data** (uses live data)
- **Visibility**: View in "Executions" tab after completion
- **Logging**: Full execution log stored in `execution_entity`

**Production Execution Flow**:
```
Trigger Event → Check if Workflow Active → Execute Workflow → Save Execution → Show in Executions Tab
```

### ⚡ Execution Mode Comparison

| Feature | Manual | Partial | Production |
|---------|--------|---------|-----------|
| Trigger | Manual button | Execute Step | Automatic triggers |
| Activation Required | No | No | Yes |
| Pinned Data | Used | Used | Ignored |
| UI Display | Live | Live (partial) | Post-execution |
| Database Storage | Optional | Optional | Always |
| Performance | Slower | Fast | Optimized |

---

## Execution Lifecycle & Flow

### 🔄 Complete Execution Lifecycle

```
┌─────────────────────────────────────────────────────────────────┐
│                   n8n EXECUTION LIFECYCLE                       │
└─────────────────────────────────────────────────────────────────┘

1. TRIGGER EVENT
   └─▶ Webhook, Cron, Manual, Event, etc.
       │
       ▼
2. WORKFLOW VALIDATION
   ├─▶ Check if workflow is active (production mode)
   ├─▶ Check if workflow exists
   ├─▶ Validate workflow structure
   └─▶ Load workflow definition from database
       │
       ▼
3. EXECUTION INITIALIZATION
   ├─▶ Create execution ID
   ├─▶ Initialize execution context (IRunExecutionData)
   ├─▶ Load credentials
   ├─▶ Set execution mode (manual/production)
   └─▶ Create execution record in database (status: 'running')
       │
       ▼
4. WORKFLOW EXECUTION
   ├─▶ workflowExecuteBefore hook
   ├─▶ Build node execution stack
   ├─▶ Execute nodes sequentially/parallel
   │   │
   │   ├─▶ For each node:
   │   │   ├─▶ nodeExecuteBefore hook
   │   │   ├─▶ Load node implementation
   │   │   ├─▶ Prepare input data
   │   │   ├─▶ Execute node logic
   │   │   ├─▶ Handle errors (retry/continue on fail)
   │   │   ├─▶ Store output data
   │   │   └─▶ nodeExecuteAfter hook
   │   │
   │   └─▶ Process connections to next nodes
   │
   └─▶ workflowExecuteAfter hook
       │
       ▼
5. EXECUTION COMPLETION
   ├─▶ Collect final output data
   ├─▶ Determine execution status (success/error/waiting)
   ├─▶ Update execution record in database
   ├─▶ Clean up resources
   └─▶ Return execution result
```

### 📊 Execution Data Structures

#### IRunExecutionData (Main Execution Context)
```typescript
interface IRunExecutionData {
  // Where execution starts
  startData: {
    destinationNode?: string;  // Which node to start from
    runNodeFilter?: string[];  // Which nodes to run (partial execution)
  };

  // Execution results
  resultData: {
    runData: {                 // Output data per node
      [nodeName: string]: ITaskDataConnections[]
    };
    error?: ExecutionError;    // Execution error if failed
    lastNodeExecuted?: string; // Last node that ran
  };

  // Runtime execution data
  executionData: {
    contextData: IExecuteContextData;        // Shared context
    nodeExecutionStack: IExecuteData[];      // Stack of nodes to execute
    waitingExecution: IWaitingForExecution;  // Waiting/paused state
  };
}
```

#### INodeExecutionData (Node Data Format)
```typescript
interface INodeExecutionData {
  json: {                      // JSON data payload
    [key: string]: any;
  };
  binary?: IBinaryKeyData;     // Binary data (files, images)
  pairedItem?: IPairedItemData; // Link to source item
}
```

### 🌊 Data Flow Example

**Scenario**: Gmail → Filter → Slack workflow

```json
{
  "nodes": [
    {"id": "gmail_1", "name": "Gmail Trigger", "type": "gmail"},
    {"id": "filter_1", "name": "Filter", "type": "filter"},
    {"id": "slack_1", "name": "Send to Slack", "type": "slack"}
  ],
  "connections": {
    "Gmail Trigger": {
      "main": [[{"node": "Filter", "type": "main", "index": 0}]]
    },
    "Filter": {
      "main": [[{"node": "Send to Slack", "type": "main", "index": 0}]]
    }
  }
}
```

**Execution Flow**:

1. **Gmail Trigger** receives email:
```json
{
  "runData": {
    "Gmail Trigger": [
      {
        "startTime": 1696118400000,
        "executionTime": 234,
        "data": {
          "main": [
            [
              {
                "json": {
                  "id": "email_123",
                  "subject": "Meeting Request",
                  "from": "john@example.com",
                  "body": "Can we meet tomorrow?"
                }
              }
            ]
          ]
        }
      }
    ]
  }
}
```

2. **Filter Node** processes:
```json
{
  "runData": {
    "Filter": [
      {
        "startTime": 1696118400234,
        "executionTime": 12,
        "data": {
          "main": [
            [
              {
                "json": {
                  "id": "email_123",
                  "subject": "Meeting Request",
                  "from": "john@example.com",
                  "body": "Can we meet tomorrow?"
                },
                "pairedItem": {"item": 0}
              }
            ]
          ]
        }
      }
    ]
  }
}
```

3. **Slack Node** sends message:
```json
{
  "runData": {
    "Send to Slack": [
      {
        "startTime": 1696118400246,
        "executionTime": 567,
        "data": {
          "main": [
            [
              {
                "json": {
                  "ok": true,
                  "channel": "C12345",
                  "ts": "1696118400.123456",
                  "message": {
                    "text": "New email from john@example.com: Meeting Request"
                  }
                },
                "pairedItem": {"item": 0}
              }
            ]
          ]
        }
      }
    ]
  }
}
```

### 🎯 Execution Status States

| Status | Description | Final State | Can Resume |
|--------|-------------|------------|-----------|
| **running** | Workflow is executing | No | No |
| **waiting** | Paused at Wait node | No | Yes |
| **success** | Completed successfully | Yes | No |
| **error** | Failed with error | Yes | Retry possible |
| **cancelled** | Manually cancelled | Yes | No |

---

## Data Flow Between Nodes

### 📦 n8n Data Structure

**Core Concept**: Data flows as an **array of items** between nodes, where each item is a JSON object.

#### Item Structure
```json
[
  {
    "json": {
      "id": 1,
      "name": "Item 1",
      "value": 100
    },
    "binary": {},
    "pairedItem": {"item": 0}
  },
  {
    "json": {
      "id": 2,
      "name": "Item 2",
      "value": 200
    },
    "binary": {},
    "pairedItem": {"item": 1}
  }
]
```

### 🔄 Node Execution Modes for Data Processing

#### 1. **For Each Item** (Default)
- Node executes once per incoming item
- 10 items in → code runs 10 times
- Access current item: `$json`
- **Use Case**: Item-level transformations

**Example - Transform Each Item**:
```javascript
// Code node in "For Each Item" mode
return {
  json: {
    id: $json.id,
    name: $json.name.toUpperCase(),
    doubled: $json.value * 2
  }
};
```

#### 2. **Once for All Items** (Batch Mode)
- Node executes once for all items
- 10 items in → code runs 1 time
- Access all items: `$input.all()`
- **Use Case**: Aggregation, summarization, batch operations

**Example - Aggregate All Items**:
```javascript
// Code node in "Once for All Items" mode
const items = $input.all();
const total = items.reduce((sum, item) => sum + item.json.value, 0);

return {
  json: {
    totalItems: items.length,
    totalValue: total,
    average: total / items.length
  }
};
```

### 🔗 Connection Types

#### 1. **Main Connection** (Standard)
- Primary data flow between nodes
- Most common connection type
- Carries item arrays

```json
{
  "connections": {
    "Node1": {
      "main": [
        [
          {
            "node": "Node2",
            "type": "main",
            "index": 0
          }
        ]
      ]
    }
  }
}
```

#### 2. **Error Connection** (Error Output)
- Activated when node fails with "Continue on Error"
- Carries error details + original data

```json
{
  "connections": {
    "HTTP Request": {
      "main": [[{"node": "Success Node", "type": "main", "index": 0}]],
      "error": [[{"node": "Error Handler", "type": "main", "index": 0}]]
    }
  }
}
```

### 🎨 Data Transformation Patterns

#### Pattern 1: Filter Items
```
Input (5 items) → Filter Node → Output (2 items matching condition)
```

#### Pattern 2: Split Items
```
Input (1 item with array) → Split Out Node → Output (N items)
```

#### Pattern 3: Merge Items
```
Input A (5 items) ─┐
                    ├─→ Merge Node → Output (Combined items)
Input B (3 items) ─┘
```

#### Pattern 4: Transform & Map
```
Input → Code Node → Set Node → Output (Transformed structure)
```

### 📝 Accessing Data in Expressions

| Context | Expression | Description |
|---------|-----------|-------------|
| Current item JSON | `$json.fieldName` | Access field in current item |
| All input items | `$input.all()` | Get array of all items |
| Specific item | `$input.item.json` | Access specific item data |
| Previous node | `$node["Node Name"].json` | Get data from specific node |
| First item | `$items[0].json` | Access first item in array |
| Binary data | `$binary.fileName` | Access binary/file data |

---

## Queue Mode & Worker System

### 🏗️ Queue Mode Architecture

**Queue mode** is n8n's distributed execution system for high-scale production deployments.

```
┌──────────────────────────────────────────────────────────────┐
│                     QUEUE MODE ARCHITECTURE                  │
└──────────────────────────────────────────────────────────────┘

┌─────────────────┐         ┌─────────────────┐
│   MAIN NODE     │         │  REDIS QUEUE    │
│  (UI + API)     │────────▶│   (Bull Jobs)   │
│                 │  Enqueue│                 │
│ - Editor UI     │  Jobs   │ - Job Queue     │
│ - API Endpoints │         │ - Job Status    │
│ - Workflows     │         │ - Rate Limiting │
│ - Credentials   │         └─────────────────┘
└─────────────────┘                │
                                   │ Dequeue Jobs
                    ┌──────────────┴───────────────┐
                    │                              │
                    ▼                              ▼
         ┌─────────────────┐           ┌─────────────────┐
         │  WORKER NODE 1  │           │  WORKER NODE 2  │
         │  (Execution)    │           │  (Execution)    │
         │                 │           │                 │
         │ - Run Workflows │           │ - Run Workflows │
         │ - Process Nodes │           │ - Process Nodes │
         │ - Save Results  │           │ - Save Results  │
         └─────────────────┘           └─────────────────┘
                    │                              │
                    └──────────────┬───────────────┘
                                   ▼
                          ┌─────────────────┐
                          │   POSTGRESQL    │
                          │   (Database)    │
                          │                 │
                          │ - Workflows     │
                          │ - Executions    │
                          │ - Credentials   │
                          └─────────────────┘

┌─────────────────┐
│  WEBHOOK NODE   │ (Optional separate instance)
│  (Webhooks)     │
│                 │
│ - Receives HTTP │
│ - Enqueues Jobs │
└─────────────────┘
```

### 🔧 Queue Mode Components

#### 1. **Main Node / Management Segment**
- **Responsibilities**:
  - Serve Editor UI
  - Handle API requests
  - Manage workflows and credentials
  - Manage triggers (cron, polling)
  - Enqueue workflow executions to Redis
- **Does NOT**: Execute workflows (delegates to workers)
- **Configuration**:
  ```bash
  EXECUTIONS_MODE=queue
  QUEUE_BULL_REDIS_HOST=redis
  QUEUE_BULL_REDIS_PORT=6379
  ```

#### 2. **Worker Nodes / Execution Segment**
- **Responsibilities**:
  - Retrieve jobs from Redis queue
  - Execute workflows
  - Run workflow nodes
  - Save execution results to database
  - Process jobs in parallel (configurable concurrency)
- **Scalability**: Add more workers to increase throughput
- **Configuration**:
  ```bash
  EXECUTIONS_MODE=queue
  EXECUTIONS_PROCESS=worker
  QUEUE_BULL_REDIS_HOST=redis
  QUEUE_BULL_REDIS_PORT=6379
  ```

#### 3. **Redis Queue (Bull Library)**
- **Purpose**: Message broker and job queue
- **Library**: Bull (Node.js Redis queue library)
- **Job Structure**:
  ```json
  {
    "id": "12345",
    "name": "workflow-execution",
    "data": {
      "executionId": "exec_789",
      "workflowId": "workflow_456",
      "mode": "production",
      "executionData": {
        "startData": {},
        "resultData": {},
        "executionData": {}
      }
    },
    "opts": {
      "attempts": 3,
      "backoff": 5000,
      "delay": 0
    },
    "progress": 0,
    "timestamp": 1696118400000
  }
  ```
- **Key Features**:
  - Job persistence
  - Retry logic
  - Rate limiting
  - Priority queues
  - Job status tracking

#### 4. **PostgreSQL Database (Required for Queue Mode)**
- **Purpose**: Persistent storage for workflows and executions
- **Tables**:
  - `workflow_entity`: Workflow definitions
  - `execution_entity`: Execution history
  - `credentials_entity`: Credentials
  - `tag_entity`, `user`, `role`, etc.
- **Note**: **SQLite NOT supported** in queue mode (PostgreSQL or MySQL required)

#### 5. **Webhook Node (Optional Separate Instance)**
- **Purpose**: Dedicated instance for webhook processing
- **Benefits**:
  - Offload webhook traffic from main node
  - Faster webhook response times
  - Better isolation
- **Configuration**:
  ```bash
  EXECUTIONS_MODE=queue
  EXECUTIONS_PROCESS=webhook
  WEBHOOK_URL=https://webhooks.example.com/
  ```

### ⚙️ Concurrency & Performance

#### Concurrency Settings
- **Per Worker**: `QUEUE_WORKER_CONCURRENCY` (default: 10)
  - Number of jobs each worker processes simultaneously
  - Higher = more parallel executions per worker
  - Adjust based on workflow complexity and server resources

#### Performance Metrics
- **Single Instance**: ~220 executions/second
- **Queue Mode**: Scales horizontally with workers
  - 3 workers @ concurrency 10 = 30 parallel executions
  - 10 workers @ concurrency 10 = 100 parallel executions

#### Queue Mode Benefits
1. **Horizontal Scaling**: Add workers as needed
2. **High Availability**: Worker failure doesn't affect others
3. **Load Distribution**: Even distribution across workers
4. **Resource Isolation**: UI separate from execution
5. **Job Persistence**: Redis ensures no lost executions

### 🚀 Queue Mode Setup (Docker Compose Example)

```yaml
version: '3.8'

services:
  # PostgreSQL Database
  postgres:
    image: postgres:14
    environment:
      POSTGRES_USER: n8n
      POSTGRES_PASSWORD: n8n
      POSTGRES_DB: n8n

  # Redis Queue
  redis:
    image: redis:7-alpine

  # Main Node (UI + API)
  n8n-main:
    image: n8nio/n8n:latest
    environment:
      EXECUTIONS_MODE: queue
      QUEUE_BULL_REDIS_HOST: redis
      QUEUE_BULL_REDIS_PORT: 6379
      DB_TYPE: postgresdb
      DB_POSTGRESDB_HOST: postgres
      DB_POSTGRESDB_DATABASE: n8n
    ports:
      - "5678:5678"
    depends_on:
      - postgres
      - redis

  # Worker Node 1
  n8n-worker-1:
    image: n8nio/n8n:latest
    environment:
      EXECUTIONS_MODE: queue
      EXECUTIONS_PROCESS: worker
      QUEUE_BULL_REDIS_HOST: redis
      QUEUE_BULL_REDIS_PORT: 6379
      QUEUE_WORKER_CONCURRENCY: 10
      DB_TYPE: postgresdb
      DB_POSTGRESDB_HOST: postgres
      DB_POSTGRESDB_DATABASE: n8n
    depends_on:
      - postgres
      - redis

  # Worker Node 2
  n8n-worker-2:
    image: n8nio/n8n:latest
    environment:
      EXECUTIONS_MODE: queue
      EXECUTIONS_PROCESS: worker
      QUEUE_BULL_REDIS_HOST: redis
      QUEUE_BULL_REDIS_PORT: 6379
      QUEUE_WORKER_CONCURRENCY: 10
      DB_TYPE: postgresdb
      DB_POSTGRESDB_HOST: postgres
      DB_POSTGRESDB_DATABASE: n8n
    depends_on:
      - postgres
      - redis
```

---

## Execution Database Schema

### 🗄️ n8n Database Tables

n8n uses the following tables to store execution-related data:

#### 1. **execution_entity** (Primary Execution Storage)
- **Purpose**: Stores complete workflow execution history
- **Key Columns**:
  - `id`: Execution ID (primary key)
  - `workflowId`: Reference to workflow
  - `finished`: Whether execution completed
  - `mode`: Execution mode (manual, production, etc.)
  - `retryOf`: ID of execution being retried (null if not retry)
  - `retrySuccessId`: ID of successful retry (null if not retried)
  - `startedAt`: Execution start timestamp
  - `stoppedAt`: Execution end timestamp
  - `workflowData`: Complete workflow JSON at time of execution
  - `data`: Execution result data (IRunExecutionData)
  - `waitTill`: Timestamp for when waiting execution should resume

**Important Notes**:
- **Large Table**: Grows rapidly with frequent executions
- **Performance**: Index on `stoppedAt` for cleanup queries
- **Size Management**: Delete old executions periodically
- **Update Pattern**: Entire row updated at each node execution (high throughput scenarios)

**Sample Record**:
```json
{
  "id": "12345",
  "workflowId": "workflow_456",
  "finished": true,
  "mode": "production",
  "retryOf": null,
  "startedAt": "2025-10-01T10:00:00.000Z",
  "stoppedAt": "2025-10-01T10:00:05.234Z",
  "workflowData": {
    "id": "workflow_456",
    "name": "Email Processor",
    "nodes": [...],
    "connections": {...}
  },
  "data": {
    "startData": {},
    "resultData": {
      "runData": {
        "Gmail Trigger": [...],
        "Process Email": [...],
        "Send to Slack": [...]
      },
      "lastNodeExecuted": "Send to Slack"
    },
    "executionData": {}
  },
  "waitTill": null
}
```

#### 2. **workflow_entity** (Workflow Definitions)
- **Purpose**: Stores workflow configurations
- **Key Columns**:
  - `id`: Workflow ID
  - `name`: Workflow name
  - `active`: Whether workflow is activated
  - `nodes`: JSON array of nodes
  - `connections`: JSON object of connections
  - `settings`: Workflow settings
  - `staticData`: Persistent data between executions
  - `createdAt`, `updatedAt`: Timestamps

#### 3. **credentials_entity** (Credentials Storage)
- **Purpose**: Stores encrypted API credentials
- **Key Columns**:
  - `id`: Credential ID
  - `name`: Credential name
  - `type`: Credential type (gmailOAuth2, slackApi, etc.)
  - `data`: Encrypted credential data
  - `createdAt`, `updatedAt`: Timestamps

### 📊 Database Relationship Diagram

```
┌─────────────────────┐
│  workflow_entity    │
│  (Workflows)        │
├─────────────────────┤
│ id (PK)             │
│ name                │
│ active              │
│ nodes               │◀──────┐
│ connections         │       │
│ settings            │       │
└─────────────────────┘       │
          │                   │
          │ 1:N               │ References
          │                   │
          ▼                   │
┌─────────────────────┐       │
│  execution_entity   │       │
│  (Executions)       │       │
├─────────────────────┤       │
│ id (PK)             │       │
│ workflowId (FK)     │───────┘
│ finished            │
│ mode                │
│ startedAt           │
│ stoppedAt           │
│ workflowData        │ (Snapshot)
│ data                │ (Results)
│ waitTill            │
└─────────────────────┘
```

### 🔍 Common Database Queries

#### Get All Executions for Workflow
```sql
SELECT
  id,
  finished,
  mode,
  startedAt,
  stoppedAt,
  (stoppedAt - startedAt) as duration
FROM execution_entity
WHERE workflowId = 'workflow_456'
ORDER BY startedAt DESC
LIMIT 100;
```

#### Delete Old Executions (Cleanup)
```sql
DELETE FROM execution_entity
WHERE stoppedAt < NOW() - INTERVAL '30 days'
  AND finished = true;
```

#### Get Waiting Executions
```sql
SELECT id, workflowId, waitTill
FROM execution_entity
WHERE waitTill IS NOT NULL
  AND waitTill <= NOW()
  AND finished = false;
```

#### Get Failed Executions
```sql
SELECT
  id,
  workflowId,
  startedAt,
  data->>'resultData'->'error' as error_message
FROM execution_entity
WHERE finished = true
  AND data->'resultData'->'error' IS NOT NULL
ORDER BY startedAt DESC;
```

---

## Execution State Management

### 🔐 State Persistence

n8n maintains execution state for:
1. **Active executions**: In-memory + database updates
2. **Waiting executions**: Full state in database for resumption
3. **Completed executions**: Final state in database

### 🔄 Execution State Flow

```
START
  │
  ├─▶ Create execution record (status: 'running')
  │
  ├─▶ Execute nodes
  │   │
  │   ├─▶ Update execution.data after each node
  │   │
  │   └─▶ If Wait node encountered:
  │       ├─▶ Set waitTill timestamp
  │       ├─▶ Set status to 'waiting'
  │       ├─▶ Save full state to database
  │       └─▶ Pause execution
  │
  ├─▶ If execution completes:
  │   ├─▶ Set finished = true
  │   ├─▶ Set stoppedAt timestamp
  │   ├─▶ Save final results
  │   └─▶ Status: 'success' or 'error'
  │
  └─▶ END
```

### 📦 State Components

#### In-Memory State (Active Execution)
- `nodeExecutionStack`: Queue of nodes to execute
- `contextData`: Shared context across nodes
- `resultData.runData`: Output from executed nodes

#### Persistent State (Database)
- `execution_entity.data`: Complete IRunExecutionData
- `execution_entity.workflowData`: Workflow snapshot
- `execution_entity.waitTill`: Resume timestamp

### 🔄 State Recovery Scenarios

#### 1. **Server Restart with Active Executions**
- Active executions lost (not persisted mid-execution)
- Waiting executions preserved (can resume)
- Completed executions preserved

#### 2. **Worker Failure in Queue Mode**
- Redis job remains in queue
- Another worker picks up job
- Job retry logic handles failure

#### 3. **Wait Node Resumption**
- Execution state loaded from database
- `nodeExecutionStack` reconstructed
- Execution continues from Wait node

---

## Error Handling & Recovery

### 🚨 Error Handling Mechanisms

#### 1. **Retry on Fail** (Node-Level)
- **Purpose**: Automatically retry failed nodes
- **Configuration**:
  - Max Tries: Number of retry attempts
  - Wait Between Tries: Delay in milliseconds
- **Important**: Only works when "On Error" = "Stop Workflow"

**Retry on Fail Settings**:
```json
{
  "id": "http_1",
  "name": "API Request",
  "type": "n8n-nodes-base.httpRequest",
  "parameters": {
    "url": "https://api.example.com/data"
  },
  "retryOnFail": true,
  "maxTries": 3,
  "waitBetweenTries": 5000
}
```

#### 2. **Continue on Fail** (Node-Level)
- **Purpose**: Don't stop workflow on node error
- **Options**:
  - **Stop Workflow**: Halt execution on error (default)
  - **Continue**: Skip error, continue to next node
  - **Continue (using error output)**: Route error to error output connector

**Continue on Fail Settings**:
```json
{
  "id": "http_1",
  "name": "API Request",
  "type": "n8n-nodes-base.httpRequest",
  "parameters": {
    "url": "https://api.example.com/data"
  },
  "continueOnFail": true,
  "onError": "continueErrorOutput"
}
```

**Error Output Pattern**:
```
                     ┌─────────────┐
                     │ HTTP Request│
                     └──────┬──────┘
                            │
                    ┌───────┴───────┐
                    │               │
              Success │             │ Error
                    │               │
                    ▼               ▼
            ┌──────────────┐  ┌──────────────┐
            │ Success Node │  │ Error Handler│
            └──────────────┘  └──────────────┘
```

#### 3. **Error Workflow** (Workflow-Level)
- **Purpose**: Catch all workflow failures
- **Setup**:
  1. Create separate workflow with Error Trigger
  2. Set error workflow in main workflow settings
  3. Error workflow receives execution details

**Error Workflow Setup**:
```json
// Main Workflow Settings
{
  "settings": {
    "errorWorkflow": "error_workflow_id"
  }
}

// Error Workflow
{
  "nodes": [
    {
      "id": "error_trigger",
      "name": "Error Trigger",
      "type": "n8n-nodes-base.errorTrigger"
    },
    {
      "id": "notify_admin",
      "name": "Send Error Notification",
      "type": "n8n-nodes-base.slack"
    }
  ]
}
```

**Error Trigger Output**:
```json
{
  "execution": {
    "id": "exec_123",
    "workflowId": "workflow_456",
    "mode": "production",
    "error": {
      "message": "API request failed",
      "stack": "...",
      "node": "HTTP Request"
    }
  },
  "workflow": {
    "id": "workflow_456",
    "name": "Main Workflow"
  }
}
```

### 🔄 Execution Recovery & Retry

#### Manual Retry from UI
1. Open Executions tab
2. Select failed execution
3. Click "Retry execution"
4. Options:
   - **Retry with currently saved workflow**: Use latest workflow version
   - **Retry with original workflow**: Use workflow version from failed execution
   - **Retry from error node**: Start from failed node (keep successful node outputs)

#### Automatic Retry Patterns

**Pattern 1: Retry with Exponential Backoff**
```json
{
  "retryOnFail": true,
  "maxTries": 5,
  "waitBetweenTries": 1000,  // 1s, then increases
  "retryBackoffStrategy": "exponential"
}
```

**Pattern 2: Auto-Retry Engine Workflow**
```
Schedule Trigger (every 5 min)
  │
  ▼
Get Failed Executions (via n8n API)
  │
  ▼
Filter: Retryable Errors
  │
  ▼
Retry Execution (via n8n API)
  │
  ▼
Log Results
```

### ⚠️ Known Error Handling Issues

1. **Retry + Continue Incompatibility**:
   - If "Retry on Fail" is ON and "On Error" is "Continue", retry settings are ignored
   - Solution: Use "Stop Workflow" for retry to work

2. **Webhook Response Timeout**:
   - Wait nodes > 64 seconds may break webhook responses
   - Solution: Use "Respond to Webhook" before Wait node

---

## Wait Node & Execution Resumption

### ⏸️ Wait Node Overview

The **Wait Node** pauses workflow execution until a specified condition is met.

**Wait Operations**:
1. **After Time Interval**: Resume after X seconds/minutes/hours/days
2. **At Specified Time**: Resume at specific date/time
3. **On Webhook Call**: Resume when webhook receives request
4. **On Form Submitted**: Resume when form is submitted (n8n Form feature)

### 🔄 Wait Node Execution Flow

```
┌─────────────────────────────────────────────────────────────┐
│                  WAIT NODE EXECUTION FLOW                   │
└─────────────────────────────────────────────────────────────┘

Workflow Executing
  │
  ├─▶ Node 1 → Node 2 → Wait Node
  │                         │
  │                         ▼
  │                    ┌─────────────────┐
  │                    │  PAUSE EXECUTION│
  │                    ├─────────────────┤
  │                    │ 1. Save state   │
  │                    │ 2. Set waitTill │
  │                    │ 3. Generate URL │
  │                    │ 4. Status: wait │
  │                    └─────────────────┘
  │                         │
  │      ┌──────────────────┴──────────────────┐
  │      │                                      │
  │      ▼                                      ▼
  │  ⏰ Timer                              🌐 Webhook
  │  Wait 1 hour                          $execution.resumeUrl
  │      │                                      │
  │      │                                      │
  │      └──────────────────┬───────────────────┘
  │                         │
  │                         ▼
  │                  ┌─────────────────┐
  │                  │ RESUME EXECUTION│
  │                  ├─────────────────┤
  │                  │ 1. Load state   │
  │                  │ 2. Restore stack│
  │                  │ 3. Continue     │
  │                  └─────────────────┘
  │                         │
  │                         ▼
  └─▶ Wait Node → Node 4 → Node 5 → Complete
```

### ⏰ Wait Node Configurations

#### 1. After Time Interval
```json
{
  "id": "wait_1",
  "name": "Wait 1 Hour",
  "type": "n8n-nodes-base.wait",
  "parameters": {
    "resume": "timeInterval",
    "amount": 1,
    "unit": "hours"
  }
}
```

**Use Cases**:
- Rate limiting
- Delayed notifications
- Scheduled follow-ups

#### 2. At Specified Time
```json
{
  "id": "wait_2",
  "name": "Wait Until Tomorrow 9am",
  "type": "n8n-nodes-base.wait",
  "parameters": {
    "resume": "specificTime",
    "dateTime": "2025-10-02T09:00:00.000Z"
  }
}
```

**Use Cases**:
- Business hours enforcement
- Scheduled releases
- Time-zone handling

#### 3. On Webhook Call
```json
{
  "id": "wait_3",
  "name": "Wait for Approval",
  "type": "n8n-nodes-base.wait",
  "parameters": {
    "resume": "webhook",
    "httpMethod": "POST",
    "authentication": "headerAuth",
    "responseCode": 200,
    "responseData": "allEntries",
    "options": {
      "maxWaitTime": 86400  // 24 hours
    }
  }
}
```

**Resume Webhook URL**: `$execution.resumeUrl`

**Use Cases**:
- Manual approvals
- External system integration
- User input collection

### 🌐 Wait Node with Webhook Resumption

**Workflow Pattern**:
```
Webhook Trigger
  │
  ▼
Process Request
  │
  ▼
Send $execution.resumeUrl to external system
  │
  ▼
Wait Node (On Webhook Call)
  │
  ├─⏸️ Execution pauses here
  │
  │ ... External system does work ...
  │ ... Calls $execution.resumeUrl ...
  │
  ├─▶ Execution resumes
  │
  ▼
Process Response
  │
  ▼
Respond to Webhook Node
  │
  ▼
Complete
```

**Example - Approval Workflow**:
```json
{
  "nodes": [
    {
      "id": "webhook_1",
      "name": "Webhook",
      "type": "n8n-nodes-base.webhook",
      "parameters": {
        "path": "approval-request",
        "responseMode": "responseNode"
      }
    },
    {
      "id": "email_1",
      "name": "Send Approval Email",
      "type": "n8n-nodes-base.emailSend",
      "parameters": {
        "text": "Click to approve: {{ $execution.resumeUrl }}"
      }
    },
    {
      "id": "wait_1",
      "name": "Wait for Approval",
      "type": "n8n-nodes-base.wait",
      "parameters": {
        "resume": "webhook",
        "options": {
          "maxWaitTime": 86400  // 24 hours timeout
        }
      }
    },
    {
      "id": "process_1",
      "name": "Process Approval",
      "type": "n8n-nodes-base.code"
    },
    {
      "id": "respond_1",
      "name": "Respond to Webhook",
      "type": "n8n-nodes-base.respondToWebhook",
      "parameters": {
        "responseBody": "{ \"status\": \"approved\" }"
      }
    }
  ]
}
```

### 🔑 Resume Webhook Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `$execution.id` | Execution ID | `"12345"` |
| `$execution.resumeUrl` | Full resume URL | `"https://n8n.example.com/webhook/resume/abc123"` |
| `$execution.mode` | Execution mode | `"production"` |

### ⚠️ Wait Node Limitations

1. **Webhook Response Timeout**: Wait > 64 seconds breaks "Respond to Webhook" node
   - **Solution**: Use "Respond to Webhook" BEFORE Wait node

2. **Partial Execution**: `$execution.resumeUrl` changes in partial executions
   - **Solution**: Send resume URL in same execution as Wait node

3. **Max Wait Time**: Configure timeout to prevent indefinite waiting
   - **Default**: No limit (can wait forever)
   - **Recommended**: Set `maxWaitTime` based on use case

---

## Workflow Activation Lifecycle

### 🔄 Activation Lifecycle

```
┌─────────────────────────────────────────────────────────────┐
│              WORKFLOW ACTIVATION LIFECYCLE                  │
└─────────────────────────────────────────────────────────────┘

INACTIVE (Default State)
  │
  │ User clicks "Active" toggle
  │
  ▼
┌──────────────────────┐
│ ACTIVATION PROCESS   │
├──────────────────────┤
│ 1. Validate workflow │
│    - Has trigger?    │
│    - Valid structure?│
│                      │
│ 2. Register triggers │
│    - Webhooks        │
│    - Cron schedules  │
│    - Event listeners │
│                      │
│ 3. Update database   │
│    - active = true   │
│                      │
│ 4. Emit events       │
│    - Workflow        │
│      Activated       │
└──────────────────────┘
  │
  ▼
ACTIVE (Listening for Triggers)
  │
  ├─▶ Webhook receives request → Execute
  ├─▶ Cron schedule fires → Execute
  ├─▶ Event occurs → Execute
  │
  │ User clicks "Inactive" toggle
  │
  ▼
┌──────────────────────┐
│ DEACTIVATION PROCESS │
├──────────────────────┤
│ 1. Stop triggers     │
│    - Unregister      │
│      webhooks        │
│    - Cancel cron     │
│      schedules       │
│    - Remove event    │
│      listeners       │
│                      │
│ 2. Update database   │
│    - active = false  │
│                      │
│ 3. Emit events       │
│    - Workflow        │
│      Deactivated     │
└──────────────────────┘
  │
  ▼
INACTIVE
```

### 🎯 Activation Requirements

#### ✅ Workflow Can Be Activated If:
1. **Has Trigger Node**: At least one non-manual trigger
2. **Valid Structure**: No missing connections
3. **Credentials Valid**: All required credentials configured
4. **No Errors**: No validation errors

#### ❌ Workflow Cannot Be Activated If:
1. **Only Manual Trigger**: No automatic trigger
2. **Invalid Connections**: Missing or broken connections
3. **Missing Credentials**: Required credentials not set
4. **Validation Errors**: Structural problems

### 🔔 Trigger Registration Process

#### Webhook Triggers
1. **Generate Production URL**: `https://n8n.example.com/webhook/{workflowId}`
2. **Register Route**: Add route to Express server
3. **Store Mapping**: workflowId → webhook path
4. **External Registration** (if needed): Register webhook with external service (GitHub, Stripe, etc.)

#### Schedule Triggers (Cron)
1. **Parse Schedule**: Convert to cron expression
2. **Create Cron Job**: Use `node-cron` library
3. **Store Job Reference**: For later cancellation
4. **Evaluate Variables**: Schedule values frozen at activation

#### Polling Triggers
- Same as Schedule Triggers
- Schedule determines polling interval

### ⚙️ Activation Settings

#### Workflow Settings (Affect Activation)
```json
{
  "settings": {
    "executionOrder": "v1",           // Node execution order
    "saveManualExecutions": true,     // Save manual runs
    "saveExecutionProgress": true,    // Save progress during execution
    "saveDataErrorExecution": "all",  // Save error executions
    "saveDataSuccessExecution": "all",// Save success executions
    "executionTimeout": 3600,         // Max execution time (seconds)
    "timezone": "America/New_York",   // Workflow timezone
    "errorWorkflow": "error_wf_id"    // Error workflow ID
  }
}
```

### 🔄 Activation Triggers (n8n Trigger Node)

The **n8n Trigger** node responds to activation events:

```json
{
  "id": "n8n_trigger_1",
  "name": "n8n Trigger",
  "type": "n8n-nodes-base.n8nTrigger",
  "parameters": {
    "events": ["init", "activate", "update"]
  }
}
```

**Events**:
- `init`: n8n instance starts/restarts
- `activate`: Workflow is activated
- `update`: Active workflow is updated

**Use Cases**:
- Initialization workflows (setup on startup)
- Notification on workflow activation
- Configuration sync on workflow update

### 📝 Important Activation Notes

1. **Schedule Variables**: Evaluated only on activation
   - Changing variable after activation doesn't update schedule
   - Must deactivate + reactivate to apply changes

2. **Workflow Updates**: Changes to active workflow take effect immediately
   - Except schedule variables (require re-activation)

3. **Credentials**: Credential updates apply immediately to active workflows

4. **Timezone**: Set in workflow settings, affects all time-based triggers

---

## n8n Source Code Architecture

### 📁 Core Packages & Files

#### 1. **packages/cli/src/** (Main Instance)
- `WorkflowRunner.ts`: Main workflow execution orchestrator
- `WorkflowRunnerProcess.ts`: Forked process execution
- `WebhookHelpers.ts`: Webhook registration/management
- `WorkflowExecuteAdditionalData.ts`: Additional execution context
- `ActiveWorkflowRunner.ts`: Manages active workflows and triggers

#### 2. **packages/core/src/** (Core Engine)
- `WorkflowExecute.ts`: Core workflow execution engine
- `Workflow.ts`: Workflow definition and structure
- `NodeExecuteFunctions.ts`: Node execution utilities
- `ExecutionData.ts`: Execution data management

#### 3. **packages/workflow/src/** (Types & Interfaces)
- `Interfaces.ts`: TypeScript interfaces
  - `IRunExecutionData`
  - `INodeExecutionData`
  - `IWorkflowExecuteAdditionalData`
  - `IRun`, `IRunData`
- `Workflow.ts`: Workflow class definition
- `WorkflowDataProxy.ts`: Expression resolution (`$json`, `$node`, etc.)

### 🔍 Key Execution Flow (Source Code)

#### Step 1: Trigger Receives Event
```typescript
// packages/cli/src/WebhookHelpers.ts
export async function executeWebhook(
  workflow: Workflow,
  webhookData: IWebhookData,
  workflowEntity: WorkflowEntity,
  mode: WorkflowExecuteMode,
  request: express.Request,
  response: express.Response
): Promise<IResponseCallbackData> {
  // Prepare execution data
  const executionMode = 'production';
  const runData: IRunData = {};

  // Enqueue or execute
  return await WorkflowRunner.run(
    executionData,
    true,
    false,
    executionMode
  );
}
```

#### Step 2: WorkflowRunner Initializes Execution
```typescript
// packages/cli/src/WorkflowRunner.ts
export class WorkflowRunner {
  async run(
    data: IWorkflowExecutionDataProcess,
    loadStaticData?: boolean,
    realtime?: boolean,
    executionMode?: string
  ): Promise<string> {
    // Create execution ID
    const executionId = await this.activeExecutions.add(data);

    // Queue mode: Enqueue job
    if (config.getEnv('executions.mode') === 'queue') {
      await Queue.getInstance().add('workflow-execution', {
        executionId,
        workflowData: data.workflowData
      });
      return executionId;
    }

    // Direct mode: Execute immediately
    const workflowExecute = new WorkflowExecute(
      additionalData,
      executionMode,
      runExecutionData
    );

    return await workflowExecute.processRunExecutionData(workflow);
  }
}
```

#### Step 3: WorkflowExecute Runs Workflow
```typescript
// packages/core/src/WorkflowExecute.ts
export class WorkflowExecute {
  async processRunExecutionData(workflow: Workflow): Promise<IRun> {
    // Execute hooks: workflowExecuteBefore
    await this.executeHook('workflowExecuteBefore');

    // Build node execution stack
    const nodeExecutionStack = this.initializeExecutionStack();

    // Execute nodes
    while (nodeExecutionStack.length > 0) {
      const executionData = nodeExecutionStack.shift()!;
      const node = workflow.getNode(executionData.node.name);

      // Execute node
      await this.executeHook('nodeExecuteBefore', [node.name]);
      const nodeResult = await this.runNode(executionData, ...);
      await this.executeHook('nodeExecuteAfter', [node.name, nodeResult]);

      // Add connected nodes to stack
      const connectedNodes = workflow.getChildNodes(node.name);
      nodeExecutionStack.push(...connectedNodes);
    }

    // Execute hooks: workflowExecuteAfter
    await this.executeHook('workflowExecuteAfter', [runData]);

    return runData;
  }
}
```

### 🎣 Hook System

**Available Hooks**:
```typescript
interface IWorkflowExecuteHooks {
  workflowExecuteBefore?: Array<() => Promise<void>>;
  workflowExecuteAfter?: Array<(runData: IRun) => Promise<void>>;
  nodeExecuteBefore?: Array<(nodeName: string) => Promise<void>>;
  nodeExecuteAfter?: Array<(nodeName: string, data: ITaskDataConnections) => Promise<void>>;
}
```

**Hook Usage**:
- Logging execution events
- Metrics collection
- Forwarding events to parent process
- Custom integrations

---

## Implementation Recommendations

### 🎯 For The AI Automator Odoo Module

Based on The AI Automator's "Above/Below the Line" architecture, here are tailored recommendations for implementing n8n-style workflow execution:

---

### 1. **Execution System Architecture**

#### Recommended Architecture
```
┌─────────────────────────────────────────────────────────────┐
│              THE AI AUTOMATOR EXECUTION SYSTEM              │
└─────────────────────────────────────────────────────────────┘

ABOVE THE LINE (n8n Strategy)
├─▶ n8n execution patterns
├─▶ n8n data structures
└─▶ n8n trigger concepts

THE BRIDGE (Translation Layer)
├─▶ execution_controller.py  (Odoo controller for execution API)
├─▶ workflow_executor.py     (Python execution engine)
└─▶ trigger_manager.py       (Trigger registration/management)

BELOW THE LINE (Odoo/PostgreSQL)
├─▶ executions model         (execution_entity equivalent)
├─▶ canvas model             (workflow_entity equivalent)
├─▶ nodes model              (node definitions)
└─▶ execution_logs model     (detailed execution logs)
```

---

### 2. **Database Models**

#### **executions** Model (New)
```python
class WorkflowExecutions(models.Model):
    _name = 'executions'
    _description = 'Workflow Executions (N8N Compatible)'
    _order = 'started_at desc'

    # Basic Information
    execution_id = fields.Char('Execution ID', required=True, index=True)
    canvas_id = fields.Many2one('canvas', string='Workflow', required=True, ondelete='cascade')

    # Execution Metadata
    mode = fields.Selection([
        ('manual', 'Manual'),
        ('production', 'Production'),
        ('partial', 'Partial')
    ], string='Execution Mode', required=True, default='manual')

    # Status
    status = fields.Selection([
        ('running', 'Running'),
        ('waiting', 'Waiting'),
        ('success', 'Success'),
        ('error', 'Error'),
        ('cancelled', 'Cancelled')
    ], string='Status', required=True, default='running', index=True)

    finished = fields.Boolean('Finished', default=False, index=True)

    # Timing
    started_at = fields.Datetime('Started At', required=True, default=fields.Datetime.now, index=True)
    stopped_at = fields.Datetime('Stopped At')
    duration = fields.Float('Duration (seconds)', compute='_compute_duration', store=True)

    # Wait/Resume Support
    wait_till = fields.Datetime('Wait Until', index=True)
    resume_url = fields.Char('Resume URL')

    # Retry Support
    retry_of = fields.Many2one('executions', string='Retry Of')
    retry_success_id = fields.Many2one('executions', string='Successful Retry')

    # Data Storage
    workflow_snapshot = fields.Text('Workflow Snapshot', help='JSON snapshot of workflow at execution time')
    execution_data = fields.Text('Execution Data', help='Complete IRunExecutionData equivalent')
    error_message = fields.Text('Error Message')

    # Relationships
    execution_log_ids = fields.One2many('execution_logs', 'execution_id', string='Execution Logs')

    @api.depends('started_at', 'stopped_at')
    def _compute_duration(self):
        for record in self:
            if record.started_at and record.stopped_at:
                delta = record.stopped_at - record.started_at
                record.duration = delta.total_seconds()
            else:
                record.duration = 0.0

    def to_n8n_format(self):
        """Export execution in n8n format"""
        self.ensure_one()
        return {
            'id': self.execution_id,
            'workflowId': self.canvas_id.workflow_id,
            'finished': self.finished,
            'mode': self.mode,
            'startedAt': self.started_at.isoformat() if self.started_at else None,
            'stoppedAt': self.stopped_at.isoformat() if self.stopped_at else None,
            'waitTill': self.wait_till.isoformat() if self.wait_till else None,
            'workflowData': json.loads(self.workflow_snapshot) if self.workflow_snapshot else {},
            'data': json.loads(self.execution_data) if self.execution_data else {}
        }
```

#### **execution_logs** Model (New)
```python
class ExecutionLogs(models.Model):
    _name = 'execution_logs'
    _description = 'Detailed Execution Logs per Node'
    _order = 'sequence, id'

    execution_id = fields.Many2one('executions', string='Execution', required=True, ondelete='cascade', index=True)
    node_id = fields.Many2one('nodes', string='Node', required=True)
    node_name = fields.Char('Node Name', required=True)

    sequence = fields.Integer('Sequence', required=True)

    # Timing
    started_at = fields.Datetime('Started At', required=True)
    finished_at = fields.Datetime('Finished At')
    duration = fields.Float('Duration (ms)', compute='_compute_duration', store=True)

    # Status
    status = fields.Selection([
        ('success', 'Success'),
        ('error', 'Error')
    ], string='Status', required=True)

    # Data
    input_data = fields.Text('Input Data', help='JSON array of input items')
    output_data = fields.Text('Output Data', help='JSON array of output items')
    error_message = fields.Text('Error Message')

    @api.depends('started_at', 'finished_at')
    def _compute_duration(self):
        for record in self:
            if record.started_at and record.finished_at:
                delta = record.finished_at - record.started_at
                record.duration = delta.total_seconds() * 1000  # milliseconds
            else:
                record.duration = 0.0
```

#### **Enhancement to `canvas` Model**
```python
class Canvas(models.Model):
    _inherit = 'canvas'

    # Activation
    active_workflow = fields.Boolean('Active', default=False, help='Whether workflow is activated')

    # Execution Settings
    execution_timeout = fields.Integer('Execution Timeout (seconds)', default=3600)
    save_execution_progress = fields.Boolean('Save Execution Progress', default=True)
    save_manual_executions = fields.Boolean('Save Manual Executions', default=True)
    save_success_executions = fields.Selection([
        ('all', 'All'),
        ('none', 'None')
    ], string='Save Success Executions', default='all')
    save_error_executions = fields.Selection([
        ('all', 'All'),
        ('none', 'None')
    ], string='Save Error Executions', default='all')

    # Error Workflow
    error_workflow_id = fields.Many2one('canvas', string='Error Workflow')

    # Executions
    execution_ids = fields.One2many('executions', 'canvas_id', string='Executions')
    execution_count = fields.Integer('Execution Count', compute='_compute_execution_count')

    @api.depends('execution_ids')
    def _compute_execution_count(self):
        for record in self:
            record.execution_count = len(record.execution_ids)

    def action_activate(self):
        """Activate workflow"""
        self.ensure_one()
        # Validate workflow has triggers
        # Register triggers (webhooks, cron, etc.)
        self.active_workflow = True
        # Emit activation event

    def action_deactivate(self):
        """Deactivate workflow"""
        self.ensure_one()
        # Unregister triggers
        self.active_workflow = False
        # Emit deactivation event
```

---

### 3. **Workflow Executor (Python)**

#### **workflow_executor.py** (New File)
```python
# -*- coding: utf-8 -*-
import json
import logging
import uuid
from datetime import datetime
from odoo import api, models, fields
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class WorkflowExecutor:
    """
    N8N-style workflow execution engine for Odoo.
    Executes workflows node-by-node, managing data flow and state.
    """

    def __init__(self, env, canvas_id, mode='manual'):
        self.env = env
        self.canvas = env['canvas'].browse(canvas_id)
        self.mode = mode
        self.execution_id = str(uuid.uuid4())
        self.execution_record = None
        self.run_data = {}  # {node_name: [output_data]}
        self.node_execution_stack = []

    def execute(self, trigger_data=None):
        """
        Main execution entry point.
        Returns execution_id.
        """
        try:
            # Step 1: Create execution record
            self._create_execution_record()

            # Step 2: Load workflow nodes and connections
            nodes = self._load_nodes()
            connections = self._load_connections()

            # Step 3: Find starting nodes (triggers or specified nodes)
            starting_nodes = self._find_starting_nodes(nodes)

            # Step 4: Initialize execution stack
            self._initialize_execution_stack(starting_nodes, trigger_data)

            # Step 5: Execute nodes
            self._execute_nodes(nodes, connections)

            # Step 6: Finalize execution
            self._finalize_execution()

            return self.execution_id

        except Exception as e:
            _logger.exception(f"Workflow execution failed: {e}")
            self._handle_execution_error(str(e))
            raise

    def _create_execution_record(self):
        """Create execution record in database"""
        workflow_snapshot = self.canvas.to_n8n_format()

        self.execution_record = self.env['executions'].create({
            'execution_id': self.execution_id,
            'canvas_id': self.canvas.id,
            'mode': self.mode,
            'status': 'running',
            'finished': False,
            'started_at': fields.Datetime.now(),
            'workflow_snapshot': json.dumps(workflow_snapshot)
        })
        self.env.cr.commit()  # Commit so execution appears immediately

    def _load_nodes(self):
        """Load workflow nodes"""
        return self.canvas.node_ids

    def _load_connections(self):
        """Load workflow connections"""
        # Parse connections from canvas
        if self.canvas.connections:
            return json.loads(self.canvas.connections)
        return {}

    def _find_starting_nodes(self, nodes):
        """Find trigger/starting nodes"""
        # For manual execution, start from manual trigger
        # For production, start from webhook/cron trigger
        starting = []
        for node in nodes:
            if 'trigger' in node.type.lower() or 'start' in node.type.lower():
                starting.append(node)
        return starting

    def _initialize_execution_stack(self, starting_nodes, trigger_data):
        """Initialize node execution stack"""
        for node in starting_nodes:
            self.node_execution_stack.append({
                'node': node,
                'input_data': trigger_data or [{'json': {}}]
            })

    def _execute_nodes(self, nodes, connections):
        """Execute nodes sequentially"""
        sequence = 0

        while self.node_execution_stack:
            # Get next node to execute
            execution_data = self.node_execution_stack.pop(0)
            node = execution_data['node']
            input_data = execution_data['input_data']

            sequence += 1

            _logger.info(f"Executing node: {node.name} (type: {node.type})")

            # Execute node
            try:
                output_data = self._execute_node(node, input_data, sequence)

                # Store output in run_data
                self.run_data[node.name] = output_data

                # Find connected nodes and add to stack
                self._add_connected_nodes_to_stack(node, connections, output_data)

            except Exception as e:
                _logger.error(f"Node execution failed: {node.name} - {e}")

                # Handle error based on node settings
                if node.continue_on_fail:
                    _logger.info(f"Continue on fail enabled, skipping error")
                    continue
                else:
                    raise

    def _execute_node(self, node, input_data, sequence):
        """
        Execute single node.
        Returns output data.
        """
        started_at = datetime.now()

        try:
            # Get node parameters
            parameters = node.get_parameters_dict() or {}

            # Execute node based on type
            output_data = self._execute_node_by_type(node, input_data, parameters)

            # Log execution
            finished_at = datetime.now()
            self._log_node_execution(node, sequence, started_at, finished_at,
                                    input_data, output_data, 'success')

            return output_data

        except Exception as e:
            finished_at = datetime.now()
            self._log_node_execution(node, sequence, started_at, finished_at,
                                    input_data, [], 'error', str(e))

            # Retry logic
            if node.retry_on_failure:
                return self._retry_node_execution(node, input_data, parameters)

            raise

    def _execute_node_by_type(self, node, input_data, parameters):
        """
        Execute node based on its type.
        This is where you'd implement node-specific logic.
        """
        node_type = node.type

        # Example implementations:
        if node_type == 'manual':
            # Manual trigger - just pass through
            return input_data

        elif node_type == 'webhook':
            # Webhook trigger - pass through webhook data
            return input_data

        elif node_type == 'code':
            # Execute JavaScript code node
            return self._execute_code_node(node, input_data, parameters)

        elif node_type == 'set':
            # Set/transform data
            return self._execute_set_node(node, input_data, parameters)

        elif node_type == 'filter':
            # Filter items
            return self._execute_filter_node(node, input_data, parameters)

        elif 'gmail' in node_type.lower():
            # Gmail node - send email
            return self._execute_gmail_node(node, input_data, parameters)

        elif 'slack' in node_type.lower():
            # Slack node - send message
            return self._execute_slack_node(node, input_data, parameters)

        else:
            _logger.warning(f"Unknown node type: {node_type}, passing through")
            return input_data

    def _execute_code_node(self, node, input_data, parameters):
        """Execute JavaScript code node (simplified)"""
        # In real implementation, you'd use a JS runtime like PyExecJS
        # For now, just pass through
        _logger.info(f"Code node execution (placeholder): {node.name}")
        return input_data

    def _execute_set_node(self, node, input_data, parameters):
        """Execute Set node (data transformation)"""
        # Transform data based on parameters
        # Example: Add/modify fields
        output = []
        for item in input_data:
            new_item = item.copy()
            # Apply transformations from parameters
            # ... implementation ...
            output.append(new_item)
        return output

    def _execute_filter_node(self, node, input_data, parameters):
        """Execute Filter node"""
        # Filter items based on conditions
        conditions = parameters.get('conditions', {})
        # ... filter logic ...
        return input_data  # Placeholder

    def _execute_gmail_node(self, node, input_data, parameters):
        """Execute Gmail node"""
        # Send email via Gmail API
        # ... implementation using node.credential_id ...
        return [{'json': {'sent': True, 'messageId': '12345'}}]

    def _execute_slack_node(self, node, input_data, parameters):
        """Execute Slack node"""
        # Send message via Slack API
        # ... implementation using node.credential_id ...
        return [{'json': {'ok': True, 'channel': 'C12345'}}]

    def _add_connected_nodes_to_stack(self, node, connections, output_data):
        """Add connected nodes to execution stack"""
        node_connections = connections.get(node.name, {}).get('main', [[]])

        for connection_list in node_connections:
            for connection in connection_list:
                connected_node_name = connection['node']
                connected_node = self.env['nodes'].search([
                    ('canvas_id', '=', self.canvas.id),
                    ('name', '=', connected_node_name)
                ], limit=1)

                if connected_node:
                    self.node_execution_stack.append({
                        'node': connected_node,
                        'input_data': output_data
                    })

    def _log_node_execution(self, node, sequence, started_at, finished_at,
                           input_data, output_data, status, error_message=None):
        """Log node execution details"""
        self.env['execution_logs'].create({
            'execution_id': self.execution_record.id,
            'node_id': node.id,
            'node_name': node.name,
            'sequence': sequence,
            'started_at': started_at,
            'finished_at': finished_at,
            'status': status,
            'input_data': json.dumps(input_data),
            'output_data': json.dumps(output_data),
            'error_message': error_message
        })

    def _retry_node_execution(self, node, input_data, parameters):
        """Retry node execution"""
        max_retries = node.max_retries or 3
        retry_interval = node.retry_interval or 30

        for attempt in range(max_retries):
            try:
                _logger.info(f"Retry attempt {attempt + 1}/{max_retries} for node: {node.name}")
                time.sleep(retry_interval)
                return self._execute_node_by_type(node, input_data, parameters)
            except Exception as e:
                if attempt == max_retries - 1:
                    raise
                continue

    def _finalize_execution(self):
        """Finalize execution (success)"""
        self.execution_record.write({
            'status': 'success',
            'finished': True,
            'stopped_at': fields.Datetime.now(),
            'execution_data': json.dumps({
                'resultData': {
                    'runData': self.run_data
                }
            })
        })
        self.env.cr.commit()

    def _handle_execution_error(self, error_message):
        """Handle execution error"""
        if self.execution_record:
            self.execution_record.write({
                'status': 'error',
                'finished': True,
                'stopped_at': fields.Datetime.now(),
                'error_message': error_message
            })
            self.env.cr.commit()
```

---

### 4. **Execution Controller (HTTP Routes)**

#### **execution_controller.py** (New File)
```python
# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import json
import logging

_logger = logging.getLogger(__name__)


class ExecutionController(http.Controller):

    @http.route('/canvas/<int:canvas_id>/execute', type='json', auth='user', methods=['POST'])
    def execute_workflow(self, canvas_id, mode='manual', trigger_data=None, **kwargs):
        """
        Execute workflow.

        POST /canvas/123/execute
        {
            "mode": "manual",
            "triggerData": [{"json": {"test": true}}]
        }
        """
        try:
            from .workflow_executor import WorkflowExecutor

            executor = WorkflowExecutor(request.env, canvas_id, mode)
            execution_id = executor.execute(trigger_data)

            return {
                'success': True,
                'executionId': execution_id
            }
        except Exception as e:
            _logger.exception("Workflow execution failed")
            return {
                'success': False,
                'error': str(e)
            }

    @http.route('/canvas/<int:canvas_id>/executions', type='json', auth='user')
    def get_executions(self, canvas_id, limit=20, offset=0, **kwargs):
        """
        Get workflow executions.

        GET /canvas/123/executions?limit=20&offset=0
        """
        canvas = request.env['canvas'].browse(canvas_id)
        executions = request.env['executions'].search([
            ('canvas_id', '=', canvas_id)
        ], limit=limit, offset=offset, order='started_at desc')

        return {
            'success': True,
            'data': [exec.to_n8n_format() for exec in executions],
            'total': len(canvas.execution_ids)
        }

    @http.route('/executions/<string:execution_id>', type='json', auth='user')
    def get_execution(self, execution_id, **kwargs):
        """
        Get single execution details.

        GET /executions/abc-123-def
        """
        execution = request.env['executions'].search([
            ('execution_id', '=', execution_id)
        ], limit=1)

        if not execution:
            return {'success': False, 'error': 'Execution not found'}

        # Include execution logs
        logs = []
        for log in execution.execution_log_ids:
            logs.append({
                'nodeName': log.node_name,
                'sequence': log.sequence,
                'startedAt': log.started_at.isoformat() if log.started_at else None,
                'finishedAt': log.finished_at.isoformat() if log.finished_at else None,
                'duration': log.duration,
                'status': log.status,
                'inputData': json.loads(log.input_data) if log.input_data else [],
                'outputData': json.loads(log.output_data) if log.output_data else [],
                'errorMessage': log.error_message
            })

        execution_data = execution.to_n8n_format()
        execution_data['logs'] = logs

        return {
            'success': True,
            'data': execution_data
        }

    @http.route('/executions/<string:execution_id>/retry', type='json', auth='user', methods=['POST'])
    def retry_execution(self, execution_id, **kwargs):
        """
        Retry failed execution.

        POST /executions/abc-123-def/retry
        """
        execution = request.env['executions'].search([
            ('execution_id', '=', execution_id)
        ], limit=1)

        if not execution:
            return {'success': False, 'error': 'Execution not found'}

        # Create new execution as retry
        from .workflow_executor import WorkflowExecutor

        executor = WorkflowExecutor(request.env, execution.canvas_id.id, execution.mode)
        new_execution_id = executor.execute()

        # Link as retry
        new_execution = request.env['executions'].search([
            ('execution_id', '=', new_execution_id)
        ], limit=1)
        new_execution.write({'retry_of': execution.id})

        return {
            'success': True,
            'executionId': new_execution_id
        }

    @http.route('/canvas/<int:canvas_id>/activate', type='json', auth='user', methods=['POST'])
    def activate_workflow(self, canvas_id, **kwargs):
        """
        Activate workflow.

        POST /canvas/123/activate
        """
        canvas = request.env['canvas'].browse(canvas_id)
        canvas.action_activate()

        return {'success': True}

    @http.route('/canvas/<int:canvas_id>/deactivate', type='json', auth='user', methods=['POST'])
    def deactivate_workflow(self, canvas_id, **kwargs):
        """
        Deactivate workflow.

        POST /canvas/123/deactivate
        """
        canvas = request.env['canvas'].browse(canvas_id)
        canvas.action_deactivate()

        return {'success': True}
```

---

### 5. **Frontend Integration (JavaScript)**

#### **workflow_executor.js** (New File)
```javascript
/** @odoo-module **/

import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

export class WorkflowExecutor {
    constructor(env) {
        this.env = env;
        this.rpc = env.services.rpc;
    }

    /**
     * Execute workflow
     */
    async executeWorkflow(canvasId, mode = 'manual', triggerData = null) {
        const result = await this.rpc(`/canvas/${canvasId}/execute`, {
            mode: mode,
            triggerData: triggerData
        });

        if (result.success) {
            return result.executionId;
        } else {
            throw new Error(result.error);
        }
    }

    /**
     * Get workflow executions
     */
    async getExecutions(canvasId, limit = 20, offset = 0) {
        const result = await this.rpc(`/canvas/${canvasId}/executions`, {
            limit: limit,
            offset: offset
        });

        return result.data;
    }

    /**
     * Get single execution
     */
    async getExecution(executionId) {
        const result = await this.rpc(`/executions/${executionId}`, {});
        return result.data;
    }

    /**
     * Retry execution
     */
    async retryExecution(executionId) {
        const result = await this.rpc(`/executions/${executionId}/retry`, {});
        return result.executionId;
    }

    /**
     * Activate workflow
     */
    async activateWorkflow(canvasId) {
        const result = await this.rpc(`/canvas/${canvasId}/activate`, {});
        return result.success;
    }

    /**
     * Deactivate workflow
     */
    async deactivateWorkflow(canvasId) {
        const result = await this.rpc(`/canvas/${canvasId}/deactivate`, {});
        return result.success;
    }
}

// Register service
registry.category("services").add("workflowExecutor", {
    dependencies: ["rpc"],
    start(env) {
        return new WorkflowExecutor(env);
    },
});
```

---

### 6. **Implementation Phases**

#### Phase 1: Core Execution Engine (Week 1-2)
- ✅ Create `executions` and `execution_logs` models
- ✅ Implement `WorkflowExecutor` class
- ✅ Basic node-by-node execution
- ✅ Data flow between nodes
- ✅ Execution logging

#### Phase 2: Execution API & UI (Week 3)
- ✅ Create `execution_controller.py` routes
- ✅ "Execute Workflow" button in canvas
- ✅ Executions list view
- ✅ Execution details view with logs

#### Phase 3: Trigger System (Week 4-5)
- ✅ Manual trigger support
- ✅ Webhook trigger implementation
- ✅ Schedule/Cron trigger
- ✅ Workflow activation/deactivation

#### Phase 4: Error Handling & Recovery (Week 6)
- ✅ Retry on fail logic
- ✅ Continue on fail support
- ✅ Error workflows
- ✅ Execution retry from UI

#### Phase 5: Advanced Features (Week 7-8)
- ✅ Wait node implementation
- ✅ Execution resumption (webhook resume)
- ✅ Sub-workflow execution
- ✅ Queue mode (if needed)

---

### 7. **Key Differences from n8n**

| Feature | n8n | The AI Automator |
|---------|-----|------------------|
| **Language** | TypeScript/Node.js | Python/Odoo |
| **Database** | SQLite/PostgreSQL | PostgreSQL (Odoo) |
| **Queue** | Bull + Redis | Odoo Queue Module (optional) |
| **Node Execution** | JavaScript runtime | Python execution |
| **Frontend** | Vue.js 3 | Odoo Web (Owl.js) |
| **API** | REST + WebSocket | Odoo JSON-RPC |

---

### 8. **Testing Strategy**

#### Unit Tests
```python
# tests/test_workflow_executor.py
from odoo.tests import TransactionCase

class TestWorkflowExecutor(TransactionCase):

    def setUp(self):
        super().setUp()
        # Create test workflow
        self.canvas = self.env['canvas'].create({
            'name': 'Test Workflow',
            'workflow_id': 'test_wf_1'
        })
        # Add test nodes
        # ...

    def test_execute_simple_workflow(self):
        """Test executing workflow with 2 nodes"""
        from ..workflow_executor import WorkflowExecutor

        executor = WorkflowExecutor(self.env, self.canvas.id, 'manual')
        execution_id = executor.execute()

        # Verify execution created
        execution = self.env['executions'].search([
            ('execution_id', '=', execution_id)
        ])
        self.assertTrue(execution)
        self.assertEqual(execution.status, 'success')

    def test_node_error_handling(self):
        """Test continue on fail"""
        # ... test implementation ...
```

---

## 📚 Summary

This deep research document provides a comprehensive understanding of **n8n's workflow execution system**, covering:

✅ **7 Trigger Types**: Manual, Webhook, Schedule, Polling, Event-based, Sub-workflow, Instance
✅ **3 Execution Modes**: Manual, Partial, Production
✅ **5 Execution States**: Running, Waiting, Success, Error, Cancelled
✅ **Queue Mode Architecture**: Redis + Bull queue for distributed execution
✅ **Data Flow**: Item-based JSON structure flowing between nodes
✅ **Error Handling**: Retry on fail, continue on fail, error workflows
✅ **State Management**: Persistent execution state for resumption
✅ **Wait Node**: Pause/resume execution with webhook callbacks
✅ **Activation Lifecycle**: Workflow activation and trigger registration

### 🎯 Implementation Recommendations for The AI Automator

The recommended implementation leverages **The AI Automator's Above/Below the Line architecture**:

- **ABOVE**: n8n execution patterns and data structures
- **BRIDGE**: Python execution engine (`WorkflowExecutor`) + Odoo controllers
- **BELOW**: PostgreSQL models (`executions`, `execution_logs`, enhanced `canvas`)

This approach ensures **n8n compatibility** while maintaining **Odoo-native implementation**, enabling The AI Automator to execute workflows exactly like n8n, but within the Odoo ecosystem.

---

**Document Version**: 1.0
**Last Updated**: October 1, 2025
**Next Update**: After implementation phase 1 completion
