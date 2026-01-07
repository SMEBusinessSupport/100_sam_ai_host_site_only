# N8N Simple Implementation Guide

## What We Built

A **simplified 2-table Odoo model** that extracts N8N node data directly from the filesystem and applies **N8N's actual categorization logic** (not our own invented logic).

---

## The Strategy

### BEFORE (What We Were Doing Wrong):
- ❌ Created complex L1/L2/L3/L4 hierarchy tables
- ❌ Invented our own categorization rules
- ❌ Imported from CSV files we manually created
- ❌ Didn't understand how N8N actually works

### AFTER (What We Do Now):
- ✅ Simple 2-table design (suppliers + nodes)
- ✅ Use **N8N's actual logic** from their source code
- ✅ Extract **directly from filesystem** (.node.js and .node.json files)
- ✅ Apply N8N's whitelist system and default subcategory logic
- ✅ Compute `ui_placement` using N8N's exact algorithm

---

## The 2 Tables

### Table 1: `n8n.simple.supplier`
**Purpose**: Track suppliers/vendors

**Fields**:
- `name` - Supplier name (e.g., "Google", "Slack")
- `has_services` - TRUE for nested (Google→Gmail), FALSE for flat (Slack)
- `action_count`, `trigger_count`, `total_nodes` - Computed statistics

### Table 2: `n8n.simple.node`
**Purpose**: Store all node data (denormalized for speed)

**Fields**:

**Identity**:
- `node_id` - N8N identifier (e.g., "n8n-nodes-base.gmail")
- `display_name` - Human name (e.g., "Gmail")
- `description`

**Hierarchy** (denormalized):
- `supplier` - Supplier name as TEXT
- `service` - Service name as TEXT (NULL for flat)

**Classification** (computed from filename):
- `is_trigger` - TRUE if filename contains "Trigger"
- `node_type` - "Action" or "Trigger"

**N8N Categories** (raw from .node.json):
- `categories` - Comma-separated (e.g., "Communication,Marketing")
- `subcategories` - JSON string (e.g., `{"Core Nodes": ["Helpers"]}`)
- `alias` - Comma-separated search terms

**N8N Whitelist Flags** (computed):
- `is_core_nodes` - Categories contains "Core Nodes"
- `is_ai_nodes` - Categories contains "AI"
- `is_hitl_nodes` - Categories contains "HITL"
- `is_whitelisted` - Any of the above

**UI Placement** (computed using N8N's logic):
- `ui_placement` - Display name (e.g., "Action in an app")
- `ui_placement_key` - Internal key (e.g., "appRegularNodes")

---

## The Golden Logic (N8N's Algorithm)

```python
def calculate_ui_placement(node):
    """Where does this node appear in N8N's UI?"""

    # Step 1: Core Nodes with explicit subcategory?
    if node.is_core_nodes and node.subcategories:
        subcat = parse_json(node.subcategories)["Core Nodes"][0]
        if subcat == "Helpers": return "Core"
        if subcat == "Flow": return "Flow"
        if subcat == "Data Transformation": return "Data transformation"
        if subcat == "Files": return "Files"

    # Step 2: AI?
    if node.is_ai_nodes:
        return "AI"

    # Step 3: HITL?
    if node.is_hitl_nodes:
        return "Human in the loop"

    # Step 4: Default (uses DEFAULT_SUBCATEGORY = "*")
    if node.is_trigger:
        return "On app event"        # appTriggerNodes
    else:
        return "Action in an app"     # appRegularNodes
```

---

## How It Works

### 1. Extraction Process

**File**: `n8n_simple_extractor.py`

**Process**:
1. Scans `static/src/n8n/n8n_nodes/` directory
2. For each supplier folder:
   - Check if it has direct `.node.js` files → **Flat structure**
   - Otherwise, scan subfolders for `.node.js` files → **Nested structure**
3. For each `.node.js` file:
   - Determine `is_trigger` from **filename only** (contains "Trigger"?)
   - Look for matching `.node.json` file
   - Extract `categories`, `subcategories`, `alias` from JSON
   - Store raw JSON for reference

### 2. Computed Fields

**File**: `n8n_simple_nodes.py`

**Auto-computed on save**:
- `node_type` ← from `is_trigger`
- `is_core_nodes`, `is_ai_nodes`, `is_hitl_nodes` ← from `categories`
- `is_whitelisted` ← OR of above
- `ui_placement` ← using N8N's algorithm
- `search_text` ← combined display_name + alias + categories

---

## Files Created

### Models:
1. `models/n8n_simple_nodes.py` - The 2 table definitions with computed fields
2. `models/n8n_simple_extractor.py` - Extraction wizard (reads filesystem)
3. `models/__init__.py` - Updated to import new models

### Security:
4. `security/n8n_simple_nodes_security.xml` - Access rights

### Views:
5. `views/n8n_simple_nodes_views.xml` - Tree/form views, menus, actions

### Manifest:
6. `__manifest__.py` - Updated to load new files

### Documentation:
7. `docs/n8n_categorization_system_documentation.md` - N8N's logic explained
8. `docs/n8n_database_schema_design.md` - Original detailed schema
9. `docs/n8n_database_schema_simplified.md` - Simplified explanation
10. `docs/n8n_database_schema_FINAL.md` - 2-table final design
11. `docs/n8n_simple_implementation_guide.md` - This file

---

## How to Use

### Step 1: Upgrade Module
```bash
# Restart Odoo and upgrade the module
odoo-bin -u the_ai_automator
```

### Step 2: Extract Nodes
1. Go to Odoo
2. Navigate to: **The AI Automator → N8N Nodes (Simple) → 🔄 Extract Nodes**
3. Click the menu item
4. Wait for extraction to complete

### Step 3: View Results

**Suppliers**:
- Menu: **N8N Nodes (Simple) → Suppliers**
- Shows all 305 suppliers with counts

**Nodes**:
- Menu: **N8N Nodes (Simple) → Nodes**
- Default view: Grouped by UI Placement
- Filters available:
  - Actions vs Triggers
  - "Action in an app"
  - "On app event"
  - Core Nodes
  - AI Nodes

---

## Key Queries

### Get all "Action in an app" nodes:
```python
nodes = env['n8n.simple.node'].search([
    ('ui_placement_key', '=', 'appRegularNodes')
])
```

### Get all Core nodes:
```python
nodes = env['n8n.simple.node'].search([
    ('is_core_nodes', '=', True)
])
```

### Search nodes:
```python
nodes = env['n8n.simple.node'].search_nodes('gmail')
```

### Get supplier stats:
```python
stats = env['n8n.simple.node'].get_supplier_stats()
```

---

## What's Next?

### Phase 1: Validate Data ✅ (Current)
- Extract nodes from filesystem
- Verify UI placement matches N8N
- Check statistics are correct

### Phase 2: Update Overlay
- Modify overlay to read from `n8n.simple.node`
- Filter by `ui_placement_key` instead of inventing categories
- Use N8N's exact menu structure

### Phase 3: Node Browser
- Build node selection UI
- Categories: "Action in an app", "On app event", "Core", etc.
- Search using `search_text` field
- Filter by `ui_placement_key`

### Phase 4: Node Details Panel
- Show node properties from `n8n.simple.node`
- Display resources/operations (can add later if needed)
- Use `subcategories` to show grouping

---

## Critical Insights

### 1. Trigger vs Action
**Source**: Filename ONLY
- File named `*Trigger.node.js` → Trigger
- File named `*.node.js` → Action
- NOT stored in JSON metadata

### 2. The Whitelist System
**Only 3 categories get special treatment**:
- "Core Nodes"
- "AI"
- "HITL"

All others use DEFAULT_SUBCATEGORY (`"*"`)

### 3. Default Subcategory Logic
Nodes without whitelisted categories:
- Triggers → "On app event" (`appTriggerNodes`)
- Actions → "Action in an app" (`appRegularNodes`)

### 4. Subcategories Only Matter for Whitelisted
If node has "Core Nodes" in categories AND has subcategories defined:
```json
{
  "categories": ["Core Nodes"],
  "subcategories": {"Core Nodes": ["Helpers"]}
}
```
→ Goes to "Core" (helpers)

If no subcategories or not whitelisted:
→ Goes to "Action in an app" or "On app event"

---

## Validation Checklist

After extraction, verify:

- [ ] Supplier count = 305
- [ ] Node count = 460 (or close)
- [ ] Nodes with `ui_placement = "Action in an app"` are NOT triggers
- [ ] Nodes with `ui_placement = "On app event"` ARE triggers
- [ ] Webhook node has `ui_placement = "Core"`
- [ ] Gmail node has `ui_placement = "Action in an app"`
- [ ] GmailTrigger has `ui_placement = "On app event"`

---

## Troubleshooting

### Issue: No nodes extracted
**Check**: Does `static/src/n8n/n8n_nodes/` exist?
**Solution**: Verify path in `n8n_simple_extractor.py`

### Issue: All nodes show same ui_placement
**Check**: Are computed fields working?
**Solution**: Check Odoo logs for errors in `_compute_ui_placement`

### Issue: is_trigger is always False
**Check**: Filename pattern matching
**Solution**: Verify `'Trigger' in node_name` logic

### Issue: Wrong category assignments
**Check**: Is `categories` field populated from JSON?
**Solution**: Verify JSON parsing in `_extract_node_from_file`

---

## Success Criteria

✅ **We succeeded when**:
1. Extraction completes without errors
2. Supplier/node counts match expected (~305/460)
3. UI placements match N8N's actual UI
4. We can filter nodes by `ui_placement_key`
5. Overlay can use this data instead of old tables
6. No more inventing our own categorization!

---

## The Win

**We finally understand how N8N works and can follow their footsteps instead of making up our own logic!**

This is the foundation for building an overlay that ACTUALLY works like N8N.