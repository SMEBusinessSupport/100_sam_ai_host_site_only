# ✅ PHASE 1: Safe Model Deprecation COMPLETE
## CTO Infrastructure Optimization - Dependency Discovery Phase

**Date**: 2025-10-31
**Status**: ✅ RENAMED (Awaiting Odoo Restart Test)
**Strategy**: Rename → Test → Delete (CTO-Approved Safe Method)

---

## What Was Done

### ✅ Step 1: Models Renamed (6 Total)

All models successfully renamed with `_PREPARE_TO_DELETE_` prefix:

| Original File | Renamed To | Backup Location |
|---------------|------------|-----------------|
| `nodes.py` | `_PREPARE_TO_DELETE_nodes.py` | `.deprecation_backup/nodes.py.backup_20251031_063442` |
| `connections.py` | `_PREPARE_TO_DELETE_connections.py` | `.deprecation_backup/connections.py.backup_20251031_063442` |
| `n8n_node_types.py` | `_PREPARE_TO_DELETE_n8n_node_types.py` | `.deprecation_backup/n8n_node_types.py.backup_20251031_063442` |
| `n8n_simple_nodes.py` | `_PREPARE_TO_DELETE_n8n_simple_nodes.py` | `.deprecation_backup/n8n_simple_nodes.py.backup_20251031_063442` |
| `n8n_simple_extractor.py` | `_PREPARE_TO_DELETE_n8n_simple_extractor.py` | `.deprecation_backup/n8n_simple_extractor.py.backup_20251031_063442` |
| `workflow_types.py` | `_PREPARE_TO_DELETE_workflow_types.py` | `.deprecation_backup/workflow_types.py.backup_20251031_063442` |

### ✅ Step 2: __init__.py Updated

Imports commented out with deprecation notices:

```python
# BEFORE:
from . import nodes
from . import connections
from . import n8n_node_types
from . import n8n_simple_nodes
from . import n8n_simple_extractor
from . import workflow_types

# AFTER:
# from . import connections      # DEPRECATED 2025-10-31 Phase 1 - Use canvas.json_definition
# from . import nodes            # DEPRECATED 2025-10-31 Phase 1 - Use canvas.json_definition
# from . import n8n_node_types   # DEPRECATED 2025-10-31 Phase 1 - Use node_metadata.json
# from . import n8n_simple_nodes # DEPRECATED 2025-10-31 Phase 1 - Use node_metadata.json
# from . import n8n_simple_extractor # DEPRECATED 2025-10-31 Phase 1 - Replaced by enhance_node_metadata_v2.py
# from . import workflow_types   # DEPRECATED 2025-10-31 Phase 1 - N8N has built-in types
```

---

## Known Dependencies (Will Break on Odoo Restart)

### 1. **canvas.py**
```python
# Line 100:
node_ids = fields.One2many('nodes', 'canvas_id', string='Canvas Nodes')
# ❌ WILL FAIL: Model 'nodes' no longer exists

# Line ~102 (estimated):
connection_ids = fields.One2many('connections', 'canvas_id', string='Connections')
# ❌ WILL FAIL: Model 'connections' no longer exists

# Line ~50 (estimated):
workflow_type_id = fields.Many2one('workflow_types', string='Workflow Type')
# ❌ WILL FAIL: Model 'workflow_types' no longer exists
```

### 2. **nodes.py** (deprecated model itself)
```python
# Line 26 (estimated):
node_type_id = fields.Many2one('node_types', string='Node Type')
# ❌ WILL FAIL: Model 'node_types' no longer exists
```

### 3. **ai_sam_workflows/controllers/node_type_mapper.py**
```python
# Line 41:
node_type = env['node_types'].search([('n8n_type', '=', node_type_string)])
# ❌ WILL FAIL: Model 'node_types' no longer exists
```

### 4. **ai_sam_workflows/controllers/transition_control.py**
```python
# Line 91:
nodes_model = request.env['nodes']
existing_nodes = nodes_model.search([('canvas_id', '=', workflow_id)])
# ❌ WILL FAIL: Model 'nodes' no longer exists
```

### 5. **executions.py**
```python
# Possible reference to connections (to be verified on restart)
```

### 6. **n8n_simple_extractor.py** (deprecated model)
```python
# References n8n.simple.node model (also deprecated)
```

---

## Next Steps

### IMMEDIATE: Test Odoo Server Restart

**Command**:
```bash
cd "C:\Working With AI\ai_sam\ai_sam"
python odoo-bin -c odoo.conf
```

**Watch For**:
```
ImportError: cannot import name 'nodes'
ImportError: cannot import name 'connections'
ImportError: cannot import name 'node_types'
KeyError: 'nodes'  # Model registry errors
KeyError: 'node_types'
```

**Expected Behavior**: ❌ Server will crash with import errors

---

## Phase 2: Fix Dependencies (After Discovery)

### Fix 1: Update canvas.py

**BEFORE**:
```python
node_ids = fields.One2many('nodes', 'canvas_id', string='Canvas Nodes')
connection_ids = fields.One2many('connections', 'canvas_id', string='Connections')
workflow_type_id = fields.Many2one('workflow_types', string='Workflow Type')
```

**AFTER** (Use json_definition instead):
```python
# DELETE One2many fields

# ADD computed fields:
@api.depends('json_definition')
def _compute_nodes_from_json(self):
    """Extract nodes from JSON definition"""
    for canvas in self:
        if canvas.json_definition:
            data = json.loads(canvas.json_definition)
            canvas.node_count = len(data.get('nodes', []))
            canvas.connection_count = len(data.get('connections', []))

node_count = fields.Integer('Node Count', compute='_compute_nodes_from_json', store=True)
connection_count = fields.Integer('Connection Count', compute='_compute_nodes_from_json', store=True)

# Workflow type - use simple Char field:
workflow_type = fields.Char('Workflow Type', help='Type of workflow (automation, integration, etc.)')
```

### Fix 2: Update ai_sam_workflows Controllers

**Create helper module**:
```python
# ai_sam_workflows/utils/node_metadata_loader.py

import json
from odoo.modules.module import get_module_resource

_METADATA_CACHE = None

def get_node_metadata():
    """Load node_metadata.json (cached)"""
    global _METADATA_CACHE
    if _METADATA_CACHE is None:
        path = get_module_resource('ai_sam', 'static/src/vendor_library/_registry/node_metadata.json')
        with open(path, 'r', encoding='utf-8') as f:
            _METADATA_CACHE = json.load(f)
    return _METADATA_CACHE

def find_node_by_n8n_type(n8n_type):
    """Find node by N8N type identifier"""
    metadata = get_node_metadata()
    for node_key, node_data in metadata.items():
        if node_data.get('n8n_type') == n8n_type:
            return node_data
    return None

def search_nodes(category=None, is_trigger=None, is_whitelisted=None):
    """Search nodes by criteria"""
    metadata = get_node_metadata()
    results = []

    for node_key, node_data in metadata.items():
        # Apply filters
        if category and node_data.get('category') != category:
            continue
        if is_trigger is not None and node_data.get('is_trigger') != is_trigger:
            continue
        if is_whitelisted is not None and node_data.get('is_whitelisted') != is_whitelisted:
            continue

        results.append(node_data)

    return results
```

**Update node_type_mapper.py**:
```python
# BEFORE:
def get_node_type_id(env, node_type_string):
    node_type = env['node_types'].search([('n8n_type', '=', node_type_string)])
    return node_type.id

# AFTER:
from ..utils.node_metadata_loader import find_node_by_n8n_type

def get_node_type_id(env, node_type_string):
    """Now returns node data dict instead of database ID"""
    node_data = find_node_by_n8n_type(node_type_string)
    return node_data  # Return full metadata!
```

**Update transition_control.py**:
```python
# BEFORE:
nodes_model = request.env['nodes']
existing_nodes = nodes_model.search([('canvas_id', '=', workflow_id)])

# AFTER:
canvas = request.env['canvas'].browse(workflow_id)
canvas_data = json.loads(canvas.json_definition or '{}')
existing_nodes = canvas_data.get('nodes', [])
```

---

## Rollback Instructions (If Needed)

**If Odoo crashes and you need to revert**:

```bash
cd "C:\Working With AI\ai_sam\ai_sam\ai_brain"
python PHASE1_SAFE_DEPRECATION.py --rollback
```

**This will**:
1. Rename files back to original names
2. Restore from backups
3. Uncomment imports in __init__.py (manual)
4. Restart Odoo

---

## Files Affected

### ai_brain Module:
- ✅ `models/__init__.py` - Imports commented out
- ✅ `models/_PREPARE_TO_DELETE_*.py` - 6 renamed files
- ✅ `.deprecation_backup/*.py.backup_*` - 6 backup files
- ⚠️ `models/canvas.py` - HAS DEPENDENCIES (will break)
- ⚠️ `models/executions.py` - POSSIBLE DEPENDENCIES

### ai_sam_workflows Module:
- ⚠️ `controllers/node_type_mapper.py` - HAS DEPENDENCIES (will break)
- ⚠️ `controllers/transition_control.py` - HAS DEPENDENCIES (will break)
- ⚠️ Views/templates - MAY HAVE DEPENDENCIES

---

## Success Criteria

### Phase 1 (Current): ✅ COMPLETE
- [x] 6 models renamed with _PREPARE_TO_DELETE_ prefix
- [x] Backups created in .deprecation_backup/
- [x] __init__.py imports commented out
- [x] Deprecation notices added

### Phase 2 (Next): ⏳ PENDING
- [ ] Odoo server restart attempted
- [ ] Import errors documented
- [ ] Dependencies cataloged
- [ ] ai_sam_workflows controllers updated
- [ ] canvas.py fields updated
- [ ] Migration script created

### Phase 3 (Final): ⏳ PENDING
- [ ] Odoo server restarts successfully
- [ ] All dependencies resolved
- [ ] Permanent deletion executed
- [ ] Rollback scripts validated

---

## CTO Decision Points

### After Odoo Restart Test:

**Option A: Continue with Fixes**
- Update canvas.py (remove One2many fields)
- Update ai_sam_workflows controllers (use node_metadata.json)
- Create migration script
- Test again

**Option B: Rollback and Re-plan**
- Discovered dependencies too complex
- Need more analysis before proceeding
- Run rollback script
- Create detailed migration plan first

**Option C: Partial Deprecation**
- Keep some models (e.g., nodes/connections) temporarily
- Delete others (n8n_node_types, n8n_simple_nodes)
- Gradual migration approach

---

## Storage Impact So Far

**Models Renamed** (not deleted yet):
- 6 models × ~10 KB each = ~60 KB

**Backups Created**:
- 6 backups × ~10 KB each = ~60 KB

**Net Storage Change**: +60 KB (temporary backups)

**After Permanent Deletion**: -60 KB (models deleted, backups kept)

---

## What's Next

1. **Test Odoo Server Restart** (discover all dependencies)
2. **Document All Errors** (create dependency map)
3. **Update Controllers** (use node_metadata.json)
4. **Update Models** (remove One2many fields)
5. **Test Again** (verify fixes)
6. **Permanent Delete** (run --delete option)

---

**Status**: ✅ Phase 1 Complete - Ready for Odoo Restart Test

**Next Command**:
```bash
cd "C:\Working With AI\ai_sam\ai_sam"
python odoo-bin -c odoo.conf
```

Watch logs carefully and document ALL errors! 🚀

---

**End of Phase 1 Report**
