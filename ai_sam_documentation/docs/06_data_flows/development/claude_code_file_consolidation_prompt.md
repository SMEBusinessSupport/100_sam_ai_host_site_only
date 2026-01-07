# Claude Code Prompt - File Consolidation & Cleanup

## Project Context
I'm working on an Odoo 18 module (`addons/n8n_integration/`) that ports N8N workflow automation into Odoo. The module uses:
- **Backend**: Python/Odoo models and controllers
- **Frontend**: Vanilla JavaScript (not OWL framework)
- **Database**: PostgreSQL (Odoo models)
- **Canvas System**: Working canvas with node display and interactions

## Current Problem
I have multiple JavaScript files with overlapping responsibilities and duplicate functions. I need to **consolidate and reorganize** these files into a clean, maintainable structure.

## Objective
**Consolidate existing files into 4 clean manager classes:**
1. `CanvasManager` - All canvas operations
2. `NodeManager` - All node operations
3. `OverlayManager` - All overlay/UI operations
4. `WorkflowCoordinator` - Connects all managers together

## Current File Structure Analysis Needed
Please examine my current JavaScript files in `addons/n8n_integration/static/src/js/` and:

1. **Audit existing files** - What files do I currently have?
2. **Map functions** - What does each file actually do?
3. **Identify duplicates** - Which functions are repeated across files?
4. **Plan consolidation** - Which files should merge together?

## Target Architecture
```
static/src/js/
├── managers/
│   ├── canvas_manager.js        # Consolidated canvas operations
│   ├── node_manager.js          # Consolidated node operations
│   ├── overlay_manager.js       # Consolidated overlay operations
│   └── workflow_coordinator.js  # Integration layer
└── [remove old scattered files]
```

## Consolidation Requirements

### CanvasManager Responsibilities
- Canvas rendering and display
- Canvas interactions (drag/drop, zoom, pan)
- Canvas data management
- Canvas positioning and sizing

### NodeManager Responsibilities
- Node creation and deletion
- Node positioning and movement
- Node configuration and parameters
- Node templates and types
- Node connections and relationships

### OverlayManager Responsibilities
- Overlay display/hide (node selection panels, popups)
- Overlay content management
- Overlay interactions and events
- Modal and popup handling

### WorkflowCoordinator Responsibilities
- Initialize all managers
- Connect manager events and communications
- Handle cross-manager data flow
- Manage overall application state

## Implementation Strategy
1. **Don't break existing functionality** - Current canvas system must keep working
2. **Consolidate gradually** - One manager at a time
3. **Remove duplicates** - Merge similar functions, keep the best implementation
4. **Test each step** - Verify consolidated manager works before removing old files
5. **Update references** - Update imports and function calls to use new managers

## Technical Specifications
- **Module path**: `addons/n8n_integration/`
- **JavaScript location**: `static/src/js/`
- **Class pattern**: ES6 classes with clear method organization
- **Integration**: Managers should communicate through coordinator, not directly
- **Error handling**: Maintain existing error handling patterns
- **Dependencies**: Minimize external dependencies, use vanilla JavaScript

## Deliverables Requested
1. **File audit report** - Current files and their functions
2. **Consolidation plan** - Which files merge into which managers
3. **Implementation of consolidated managers** - Working manager classes
4. **Integration coordinator** - Connects all managers
5. **Updated file structure** - Clean, organized directory structure
6. **Migration guide** - How to update existing references

## Success Criteria
- ✅ Fewer files with clear responsibilities
- ✅ No duplicate functions
- ✅ Existing canvas functionality preserved
- ✅ Easy to understand and maintain
- ✅ Clean separation of concerns
- ✅ All managers work together seamlessly

## Current Working System
My existing canvas system works for:
- Displaying nodes on canvas
- Basic interactions (drag/drop)
- Canvas rendering
- Data management

**The goal is to organize and consolidate this working code, not rebuild it.**

Please start by analyzing my current file structure and providing a consolidation plan before implementing any changes.