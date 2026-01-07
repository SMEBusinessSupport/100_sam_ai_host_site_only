# Workflows Static/Src Consolidation Audit

**Status:** WIP - Needs Review
**Location:** `ai_sam_workflows/static/src/`
**Objective:** Clean up, consolidate, and potentially remove unused components. Organize better.

---

## Current Structure (27 files)

```
static/src/
├── components/
│   ├── workflow_canvas_registry.js
│   └── workflow_canvas_template.xml
├── css/
│   ├── branch_selector.css
│   ├── canvas_manager_styles.css
│   └── node_chat_ui.css
├── html/
│   └── (empty or minimal)
├── js/
│   └── odoo_services_bridge.js
├── services/
│   ├── icon_service.js
│   └── WorkflowParser.js
├── xml/
│   └── workflow_templates.xml
└── n8n/
    ├── canvas/
    │   └── canvas_manager.js
    ├── lines/
    │   ├── connection_manager.js
    │   └── connection_system.js
    ├── nodes/
    │   ├── group_to_visual_map.js
    │   ├── node_manager.js
    │   ├── node_style_manager.js
    │   ├── node_type_registry.js
    │   ├── node_type_registry.json
    │   └── node_types.js
    ├── overlays/
    │   └── overlay_manager.js
    ├── theater/
    │   ├── theater_director.js
    │   └── workflow_analyzer.js
    ├── utils/
    │   ├── coordinate_utils.js
    │   ├── graph_utils.js
    │   ├── index.js
    │   └── svg_path_utils.js
    ├── n8n_styles/
    │   └── nodes.css
    └── n8n_node_metadata_simplified.json
```

---

## Folder Analysis

### `components/` (2 files)
| File | Purpose | Status |
|------|---------|--------|
| `workflow_canvas_registry.js` | OWL component registration | Review |
| `workflow_canvas_template.xml` | OWL template | Review |

### `css/` (3 files)
| File | Purpose | Status |
|------|---------|--------|
| `branch_selector.css` | Branch selection UI | Review |
| `canvas_manager_styles.css` | Canvas styling | Review |
| `node_chat_ui.css` | Node chat styling | Review |

**Question:** Should CSS be consolidated with `n8n/n8n_styles/`?

### `js/` (1 file)
| File | Purpose | Status |
|------|---------|--------|
| `odoo_services_bridge.js` | Bridge to Odoo services | Review |

### `services/` (2 files)
| File | Purpose | Status |
|------|---------|--------|
| `icon_service.js` | Icon loading/management | Review |
| `WorkflowParser.js` | Parse workflow data | Review |

### `xml/` (1 file)
| File | Purpose | Status |
|------|---------|--------|
| `workflow_templates.xml` | QWeb templates | Review |

### `n8n/` (18 files) - THE BIG ONE
This is the N8N visual canvas system. See detailed breakdown below.

---

## N8N Folder Deep Dive

### `n8n/canvas/` (1 file)
| File | Purpose | Status |
|------|---------|--------|
| `canvas_manager.js` | Main canvas rendering | Active? |

### `n8n/lines/` (2 files)
| File | Purpose | Status |
|------|---------|--------|
| `connection_manager.js` | Connection CRUD | Active? |
| `connection_system.js` | Connection rendering | Active? |

**Question:** Are both needed? Redundant?

### `n8n/nodes/` (6 files)
| File | Purpose | Status |
|------|---------|--------|
| `group_to_visual_map.js` | Group visualization | Review |
| `node_manager.js` | Node CRUD | Active? |
| `node_style_manager.js` | Node styling | Active? |
| `node_type_registry.js` | Type definitions (JS) | **POSSIBLE DUPLICATE** |
| `node_type_registry.json` | Type definitions (JSON) | **POSSIBLE DUPLICATE** |
| `node_types.js` | Type enums | **POSSIBLE DUPLICATE** |

**Question:** Node registry was consolidated elsewhere - are these still needed?

### `n8n/overlays/` (1 file)
| File | Purpose | Status |
|------|---------|--------|
| `overlay_manager.js` | Overlay rendering | Active? |

### `n8n/theater/` (2 files)
| File | Purpose | Status |
|------|---------|--------|
| `theater_director.js` | Animation/presentation | Review |
| `workflow_analyzer.js` | Workflow analysis | Active? |

### `n8n/utils/` (4 files)
| File | Purpose | Status |
|------|---------|--------|
| `coordinate_utils.js` | Coord transforms | Active (refactored) |
| `graph_utils.js` | Graph algorithms | Active (refactored) |
| `index.js` | Export barrel | Active |
| `svg_path_utils.js` | SVG path generation | Active? |

**Note:** Utils were refactored per `n8n_utilities_refactoring_plan.md`

### `n8n/n8n_styles/` (1 file)
| File | Purpose | Status |
|------|---------|--------|
| `nodes.css` | Node styling | Active? |

### `n8n/` root (1 file)
| File | Purpose | Status |
|------|---------|--------|
| `n8n_node_metadata_simplified.json` | Node metadata | Review |

---

## Key Questions

### 1. Node Registry Duplication
- `node_type_registry.js` vs centralized node registry?
- `node_type_registry.json` - is this the source of truth?
- `node_types.js` - still needed?

### 2. CSS Organization
- 3 CSS files in `css/`
- 1 CSS file in `n8n/n8n_styles/`
- Should these be consolidated?

### 3. Connection System
- `connection_manager.js` vs `connection_system.js`
- What's the difference? Both needed?

### 4. Dead Code
- Which files have no imports elsewhere?
- Which files are deprecated but not removed?

---

## Action Plan

### Phase 1: Discovery
- [ ] Grep for imports of each file across codebase
- [ ] Identify files with 0 imports = dead code candidates
- [ ] Compare node registry with centralized version

### Phase 2: Document
- [ ] Mark each file as ACTIVE / DEPRECATED / DEAD
- [ ] Document dependencies between files

### Phase 3: Cleanup
- [ ] Remove confirmed dead files
- [ ] Consolidate CSS into single location
- [ ] Consolidate node type definitions

### Phase 4: Reorganize
- [ ] Consider flatter structure if n8n/ is simplified
- [ ] Update imports across codebase

---

## Suggested Target Structure

```
static/src/
├── components/           # OWL components
├── css/                  # All CSS consolidated
├── js/                   # Core JS (bridge, services)
│   ├── odoo_services_bridge.js
│   ├── icon_service.js
│   └── workflow_parser.js
├── xml/                  # All QWeb templates
└── canvas/               # Canvas system (simplified from n8n/)
    ├── canvas_manager.js
    ├── connection_system.js  # Consolidated
    ├── node_manager.js
    ├── overlay_manager.js
    └── utils/
        ├── coordinate_utils.js
        ├── graph_utils.js
        └── svg_path_utils.js
```

**Goal:** 18 n8n files → ~8-10 essential canvas files

---

## Related Documents

- `09_wip/n8n_utilities_refactoring_plan.md` - Utils refactoring (Phase 1 & 2 complete)
- `09_wip/adapters/provider_adapter_architecture_blueprint.md` - Related architecture

---

*Created: 2026-01-03*
*Last Updated: 2026-01-03*
