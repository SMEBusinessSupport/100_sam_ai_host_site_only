# N8N Categorization System - Complete Documentation

## Overview

This document captures the complete understanding of N8N's node categorization and UI filtering system, discovered through analysis of the N8N installation and node metadata files.

---

## 1. Three-Level Categorization System

N8N uses a 3-level categorization system defined in each `.node.json` file:

### 1.1 Categories (Main Categories)
- **Field**: `categories` (array)
- **Purpose**: Primary classification of nodes
- **Example**: `["Development", "Core Nodes"]`
- **Common Values**:
  - Core Nodes
  - Development
  - Communication
  - Data & Storage
  - Marketing & Content
  - Sales & CRM
  - Productivity
  - Finance & Accounting

### 1.2 Subcategories (UI Grouping)
- **Field**: `subcategories` (object)
- **Purpose**: Hierarchical UI placement within categories
- **Structure**: `{"Parent Category": ["subcategory1", "subcategory2"]}`
- **Example**: `{"Core Nodes": ["Helpers", "Flow"]}`
- **Statistics**: 72 out of 428 nodes (17%) have subcategories defined

### 1.3 Alias (Search Terms)
- **Field**: `alias` (array)
- **Purpose**: Alternative search terms for finding nodes
- **Example**: `["HTTP", "API", "Build", "WH"]`
- **Statistics**: 96 out of 428 nodes (22%) have aliases defined

---

## 2. UI Subcategory Display Names

N8N's UI uses hardcoded display name mappings found in the editor-ui code. These map internal subcategory keys to user-facing labels.

### Location in N8N Installation
```
/usr/local/lib/node_modules/n8n/node_modules/.pnpm/n8n-editor-ui@file+packages+frontend+editor-ui/node_modules/n8n-editor-ui/dist/assets/index-DuT-FIl1.js
```

### Complete Subcategory Mappings

| Internal Key | UI Display Name |
|-------------|----------------|
| `appTriggerNodes` | "On app event" |
| `appRegularNodes` | "Action in an app" |
| `helpers` | "Core" |
| `dataTransformation` | "Data transformation" |
| `flow` | "Flow" |
| `files` | "Files" |
| `miscellaneous` | "Miscellaneous" |
| `humanInTheLoop` | "Human in the loop" |
| `otherTriggerNodes` | "Other trigger nodes" |

### AI-Related Subcategories
| Internal Key | UI Display Name |
|-------------|----------------|
| `agents` | "Agents" |
| `chains` | "Chains" |
| `embeddings` | "Embeddings" |
| `languageModels` | "Language models" |
| `memory` | "Memory" |
| `outputParsers` | "Output parsers" |
| `retrievers` | "Retrievers" |
| `textSplitters` | "Text splitters" |
| `tools` | "Tools" |
| `vectorStores` | "Vector stores" |

---

## 3. Node Classification: Trigger vs Action

### Critical Discovery
**Node classification (Trigger vs Action) is determined SOLELY by the filename pattern, NOT by metadata in the .node.json file.**

### Filename Pattern Rules
```
*Trigger.node.json → Trigger
*.node.json         → Action
```

### Examples
- `WebhookTrigger.node.json` → Trigger
- `Webhook.node.json` → Action
- `GmailTrigger.node.json` → Trigger
- `Gmail.node.json` → Action

### Statistics (from analysis)
- **Total nodes**: 460
- **Actions**: 356 (77%)
- **Triggers**: 104 (23%)

---

## 4. Node Structure Types

N8N nodes follow two distinct directory structures:

### Type 1: Nested Structure (21 suppliers)
```
nodes_path/
  └── SupplierName/
      └── L1_Service/
          ├── ServiceName.node.js
          ├── ServiceName.node.json
          └── ServiceNameTrigger.node.json (optional)
```

**Example**: Google → Gmail, Google → Drive

**Characteristics**:
- Supplier has L1 service subfolders
- Each service contains its own .node.js/.node.json files
- Allows multiple services per supplier

### Type 2: Flat Structure (284 suppliers)
```
nodes_path/
  └── SupplierName/
      ├── SupplierName.node.js
      ├── SupplierName.node.json
      └── SupplierNameTrigger.node.json (optional)
```

**Example**: ActiveCampaign, Webhook

**Characteristics**:
- Supplier contains direct .node.js/.node.json files
- No service subdivision
- Simpler structure for single-purpose integrations

---

## 5. File Versioning

### Version Folders
N8N maintains version history using `v1/`, `v2/`, `v3/` subfolders.

### Version Handling Rules
- **Current version**: Parent folder (no version suffix)
- **Old versions**: v1/, v2/, v3/ subfolders
- **Analysis rule**: IGNORE versioned folders, only use current version

### Statistics
- **Total .node.js files**: 528
- **Total .node.json files**: 433
- **Versioned files (ignored)**: 95
- **Active nodes**: 433

---

## 6. Real-World Example: Webhook Node

### File Location
```
n8n_nodes/Webhook/Webhook.node.json
```

### Complete Categorization Data
```json
{
  "node": "n8n-nodes-base.webhook",
  "nodeVersion": "2.0",
  "displayName": "Webhook",
  "description": "Receive data sent to a webhook URL",
  "categories": ["Core Nodes"],
  "subcategories": {
    "Core Nodes": ["Helpers"]
  },
  "alias": ["HTTP", "API", "Build", "WH"]
}
```

### UI Rendering
- **Main Category**: Core Nodes
- **Subcategory**: "Core" (from `helpers` mapping)
- **Search Terms**: Webhook, HTTP, API, Build, WH
- **Classification**: Action (filename doesn't contain "Trigger")

---

## 7. Data Files Generated

### Master Knowledge Report
**File**: `C:\Users\total\n8n_master_knowledge_report.csv`

**Columns**:
- supplier
- supplier_actions (count)
- supplier_triggers (count)
- supplier_services (comma-separated L1 services)
- structure_type (Nested/Flat)
- l1_service
- l2_node_name
- l2_classification (Trigger/Action)
- l2_display_name
- l2_node_type
- l2_categories
- l2_has_json
- l3_resource
- l4_operation
- file_path
- notes

**Statistics**:
- 460 rows (all nodes)
- 305 suppliers
- 356 actions, 104 triggers
- 21 suppliers with nested services

### Categorization Analysis
**File**: `C:\Users\total\n8n_categorization_analysis.csv`

**Columns**:
- supplier
- l1_service
- file_name
- filename_classification (Trigger/Action)
- node_id
- categories
- subcategories (formatted as "Parent: sub1, sub2")
- alias
- file_path

**Statistics**:
- 428 nodes analyzed
- 72 nodes with subcategories (17%)
- 96 nodes with aliases (22%)

---

## 8. Key Insights for Implementation

### For UI Development
1. **Use filename pattern** to determine Trigger vs Action display
2. **Map subcategory keys** to UI display names using the hardcoded mappings
3. **Parse subcategories object** to understand nested UI placement
4. **Index alias fields** for search functionality

### For Data Processing
1. **Ignore v1/v2/v3 folders** - they contain outdated versions
2. **Check for both structure types** when scanning suppliers
3. **Extract categories array** for main categorization
4. **Parse subcategories object** for UI grouping

### For Search Implementation
1. Combine `displayName`, `alias`, and `node_id` for search index
2. Allow searching by category and subcategory
3. Filter by Trigger/Action based on filename pattern
4. Consider supplier name as additional search term

---

## 9. Source Code References

### Python Analysis Scripts
- `C:\Users\total\analyze_node_categorization.py` - Extracts categorization metadata
- `C:\Users\total\create_master_report.py` - Generates comprehensive CSV report
- `C:\Users\total\find_missing_json.py` - Identifies versioned/missing files

### N8N Installation Paths
- **Node definitions**: `C:\Working With AI\Odoo Projects\custom-modules-v18\the_ai_automator\static\src\n8n\n8n_nodes`
- **Docker container**: `n8n-existing`
- **N8N modules**: `/usr/local/lib/node_modules/n8n`
- **UI mappings**: `/usr/local/lib/node_modules/n8n/node_modules/.pnpm/n8n-editor-ui@file+packages+frontend+editor-ui/node_modules/n8n-editor-ui/dist/assets/index-DuT-FIl1.js`

---

## 10. Critical Implementation Notes

### What's in the JSON Files
✅ Categories (main)
✅ Subcategories (UI grouping)
✅ Alias (search terms)
✅ Display name
✅ Node version
✅ Description

### What's NOT in the JSON Files
❌ Trigger/Action classification (determined by filename)
❌ UI display names for subcategories (hardcoded in editor-ui)
❌ Active/inactive status (determined by folder structure)

### Golden Rule
**The filename pattern is the source of truth for Trigger vs Action classification, not the JSON metadata.**

---

---

## 11. UI Click-Through Flow & Subcategory Logic

### The Golden Discovery: How "Action in an app" Works

When a user clicks "Action in an app" in the N8N UI, the system uses a sophisticated filtering mechanism to determine which nodes to show.

### Core Logic Location
```
/usr/local/lib/node_modules/n8n/node_modules/.pnpm/n8n-editor-ui@file+packages+frontend+editor-ui/node_modules/n8n-editor-ui/dist/assets/index-DuT-FIl1.js
```

### Key Constants Discovered
```javascript
const CORE_NODES_CATEGORY = "Core Nodes";
const HUMAN_IN_THE_LOOP_CATEGORY = "HITL";
const DEFAULT_SUBCATEGORY = "*";
const AI_SUBCATEGORY = "AI";

// Subcategory constants
const HELPERS_SUBCATEGORY = "Helpers";
const TRANSFORM_DATA_SUBCATEGORY = "Data Transformation";
const FLOWS_CONTROL_SUBCATEGORY = "Flow";
const OTHER_TRIGGER_NODES_SUBCATEGORY = "Other Trigger Nodes";
const HITL_SUBCATEGORY = "Human in the Loop";
```

### The Whitelisting System

N8N uses a **whitelist approach** for explicit subcategories:

```javascript
const WHITE_LISTED_SUBCATEGORIES = [
    CORE_NODES_CATEGORY,    // "Core Nodes"
    AI_SUBCATEGORY,         // "AI"
    HUMAN_IN_THE_LOOP_CATEGORY  // "HITL"
];
```

### How Subcategory Assignment Works

#### Step 1: Check Whitelisted Categories
```javascript
function subcategorizeItems(items) {
  return items.reduce((acc, item) => {
    let subcategories = [DEFAULT_SUBCATEGORY];  // Default: "*"

    const matchedSubcategories = WHITE_LISTED_SUBCATEGORIES.flatMap((category) => {
      if (item.codex?.categories?.includes(category)) {
        return item.codex?.subcategories?.[category] ?? [];
      }
      return [];
    });

    if (matchedSubcategories.length > 0) {
      subcategories = matchedSubcategories;
    }

    // ... rest of logic
  }, {});
}
```

#### Step 2: Default Subcategory Fallback
- **If node has whitelisted category WITH subcategories**: Use those subcategories
- **If node has whitelisted category WITHOUT subcategories**: Falls back to `DEFAULT_SUBCATEGORY` (`"*"`)
- **If node has NO whitelisted categories**: Uses `DEFAULT_SUBCATEGORY` (`"*"`)

### The Critical Insight: appRegularNodes vs appTriggerNodes

Based on the code analysis, here's how N8N categorizes nodes:

#### For Regular Nodes (Actions)
```javascript
visibleNodeTypes.filter((node) => !node.group.includes("trigger")).forEach((app) => {
  // These become candidates for "appRegularNodes" (Action in an app)
  const appActions = generateNodeActions(app);
  actions[app.name] = appActions;
  mergedNodes.push(getSimplifiedNodeType(app));
});
```

**Result**: Nodes that:
- Do NOT have "trigger" in their group array
- Do NOT have explicit whitelisted subcategories
- Get assigned to `DEFAULT_SUBCATEGORY` (`"*"`)
- Are displayed under **"Action in an app"** (`appRegularNodes`)

#### For Trigger Nodes
```javascript
visibleNodeTypes.filter((node) => node.group.includes("trigger")).forEach((trigger) => {
  // These become candidates for "appTriggerNodes" (On app event)
  const triggerActions = generateNodeActions(trigger);
  // ... merge logic with regular actions if same base name
});
```

**Result**: Nodes that:
- HAVE "trigger" in their group array
- Do NOT have explicit whitelisted subcategories
- Get displayed under **"On app event"** (`appTriggerNodes`)

### Complete Flow Diagram

```
User clicks "Action in an app"
    ↓
UI looks for subcategory: "appRegularNodes"
    ↓
System filters nodes where:
    ✓ node.group does NOT include "trigger"
    ✓ node has DEFAULT_SUBCATEGORY ("*")
    ✓ node is NOT in CORE_NODES_CATEGORY
    ✓ node is NOT in AI_SUBCATEGORY
    ✓ node is NOT in HUMAN_IN_THE_LOOP_CATEGORY
    ↓
Display filtered nodes sorted alphabetically
```

### Real-World Examples

#### Example 1: Google Sheets (Action in an app)
```json
{
  "node": "n8n-nodes-base.googleSheets",
  "categories": ["Marketing & Content"],
  "subcategories": {}  // No explicit subcategories
}
```
- Not in whitelist → Uses `DEFAULT_SUBCATEGORY`
- Not a trigger → Goes to **"Action in an app"**

#### Example 2: Gmail Trigger (On app event)
```json
{
  "node": "n8n-nodes-base.gmailTrigger",
  "categories": ["Communication"],
  "subcategories": {}  // No explicit subcategories
}
```
- Not in whitelist → Uses `DEFAULT_SUBCATEGORY`
- Is a trigger → Goes to **"On app event"**

#### Example 3: Webhook (Core)
```json
{
  "node": "n8n-nodes-base.webhook",
  "categories": ["Core Nodes"],
  "subcategories": {
    "Core Nodes": ["Helpers"]
  }
}
```
- In whitelist with explicit subcategory → Goes to **"Core"** (Helpers)
- Does NOT appear in "Action in an app"

### The Mapping Table

| Node Characteristics | UI Subcategory | Internal Key |
|---------------------|----------------|--------------|
| Not trigger + No explicit subcategory | "Action in an app" | `appRegularNodes` |
| Is trigger + No explicit subcategory | "On app event" | `appTriggerNodes` |
| Has "Core Nodes" → "Helpers" | "Core" | `helpers` |
| Has "Core Nodes" → "Flow" | "Flow" | `flow` |
| Has "Core Nodes" → "Data Transformation" | "Data transformation" | `dataTransformation` |
| Has "Core Nodes" → "Files" | "Files" | `files` |
| Has "AI" → (any AI subcategory) | Various AI categories | `agents`, `chains`, etc. |
| Has "HITL" | "Human in the loop" | `humanInTheLoop` |

### Implementation Rule of Thumb

**To determine where a node appears in the UI:**

1. **Check categories array** - Is it in whitelist (Core Nodes, AI, HITL)?
   - YES → Check subcategories object for specific placement
   - NO → Go to step 2

2. **Check if trigger** (from filename or group property)
   - YES → Node goes to "On app event" (`appTriggerNodes`)
   - NO → Node goes to "Action in an app" (`appRegularNodes`)

3. **Nodes can appear in multiple subcategories** if they have multiple subcategories defined

---

## Document History
- **Created**: 2025-09-30
- **Updated**: 2025-09-30 (Added UI click-through flow analysis)
- **Purpose**: Capture comprehensive understanding of N8N's categorization system
- **Source**: Analysis of 433 N8N nodes and N8N editor-ui source code