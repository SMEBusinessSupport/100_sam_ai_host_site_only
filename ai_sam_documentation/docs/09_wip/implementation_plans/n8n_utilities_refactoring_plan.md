# N8N Utilities Refactoring Plan

**Date:** 2025-12-17
**Author:** Anthony & Claude AI
**Status:** Phase 1 & 2 Complete - Ready for Testing

---

## Strategic Goal

Centralize scattered utility functions into reusable modules, improving:
- **Maintainability**: Single source of truth for each algorithm
- **Testability**: Pure functions are easier to unit test
- **Discoverability**: Developers find utilities in one place
- **Performance**: Potential for optimization in one location

---

## Phase 1: Utility Extraction (COMPLETE)

Created `utils/` folder with pure function modules:

### coordinate_utils.js
Screen/canvas coordinate transformations.

| Function | Purpose | Used By |
|----------|---------|---------|
| `screenToCanvas()` | Convert mouse position to canvas coords | canvas_manager, node_manager, connection_system |
| `canvasToScreen()` | Convert canvas coords to screen position | connection_system, connection_manager |
| `snapToGrid()` | Align coordinates to grid | canvas_manager, node_manager |
| `distanceBetween()` | Euclidean distance | (new - for hit detection) |
| `midpoint()` | Calculate center point | (new - for labels) |
| `isPointInRect()` | Point collision | canvas_manager (selection) |
| `doRectsOverlap()` | Rectangle collision | canvas_manager (lasso select) |
| `getSelectionBounds()` | Normalize selection box | canvas_manager |
| `clamp()` | Constrain value to range | (new - for zoom limits) |
| `lerp()` | Linear interpolation | (new - for animations) |

### graph_utils.js
Graph algorithms for workflow analysis.

| Function | Purpose | Used By |
|----------|---------|---------|
| `buildGraph()` | Create adjacency list from N8N connections | workflow_analyzer |
| `topologicalSort()` | Order nodes by dependencies | workflow_analyzer (assembly sequence) |
| `detectLoops()` | Find cycles in workflow | workflow_analyzer |
| `countParallelBranches()` | Count branching paths | workflow_analyzer |
| `calculateMaxDepth()` | Longest path length | workflow_analyzer |
| `dfsDepth()` | DFS traversal helper | workflow_analyzer |
| `findRootNodes()` | Entry points (no incoming) | (new) |
| `findLeafNodes()` | Exit points (no outgoing) | (new) |
| `getDownstreamNodes()` | All reachable nodes | workflow_analyzer |
| `countConnections()` | Total connection count | workflow_analyzer |
| `calculateComplexityScore()` | 0-1 complexity metric | workflow_analyzer |

### svg_path_utils.js
SVG path generation for bezier connections.

| Function | Purpose | Used By |
|----------|---------|---------|
| `generateN8NCurvedPath()` | N8N-style horizontal bezier | connection_system, connection_manager |
| `generateCurvedPath()` | Configurable curve factor | (new variant) |
| `generateStraightPath()` | Direct line path | (new - for debugging) |
| `generateSteppedPath()` | Right-angle path | (new - flowchart style) |
| `generateBackwardsPath()` | S-curve for loops | (new - backwards connections) |
| `generateArrowHead()` | Arrow marker path | (new - directional arrows) |
| `calculateLineAngle()` | Angle between points | (new - for arrow rotation) |
| `getPointOnBezier()` | Point at t parameter | (new - for labels on curves) |
| `getBezierLength()` | Approximate curve length | (new - for animation timing) |

### index.js
Unified namespace providing `window.N8NUtils` with all functions.

---

## Phase 2: Update Managers to Use Utilities (COMPLETE)

### Strategy: Non-Breaking Migration

The utilities are loaded BEFORE the managers (per __manifest__.py). We:

1. **Keep existing methods** as thin wrappers calling utilities
2. **Deprecate inline implementations** with comments
3. **Test thoroughly** before removing old code
4. **Maintain backward compatibility** for any external callers

### Files to Update

#### 1. canvas_manager.js
**Current:** Has inline `screenToCanvas()`, `canvasToScreen()`, `snapToGrid()` methods

**Change to:**
```javascript
// REFACTORED (2025-12-17): Now delegates to centralized utilities
screenToCanvas(screenX, screenY) {
    const rect = this.canvasContainer.getBoundingClientRect();
    return window.CoordinateUtils.screenToCanvas(
        screenX, screenY,
        this.currentZoom,
        this.panOffset,
        rect
    );
}

canvasToScreen(canvasX, canvasY) {
    const rect = this.canvasContainer.getBoundingClientRect();
    return window.CoordinateUtils.canvasToScreen(
        canvasX, canvasY,
        this.currentZoom,
        this.panOffset,
        rect
    );
}

snapToGrid(x, y) {
    if (!this.config.snapToGrid) return { x, y };
    return window.CoordinateUtils.snapToGrid(x, y, this.config.gridSize);
}
```

#### 2. workflow_analyzer.js
**Current:** Has all graph algorithms inline (buildGraph, topologicalSort, detectLoops, etc.)

**Change to:**
```javascript
// REFACTORED (2025-12-17): Now uses centralized graph utilities
analyzeComplexity(workflow) {
    const nodes = workflow.nodes || [];
    const connections = workflow.connections || {};

    const graph = window.GraphUtils.buildGraph(nodes, connections);
    const maxDepth = window.GraphUtils.calculateMaxDepth(graph, nodes);
    const parallelBranches = window.GraphUtils.countParallelBranches(graph);
    const hasLoops = window.GraphUtils.detectLoops(graph);
    const connectionCount = window.GraphUtils.countConnections(connections);

    return {
        node_count: nodes.length,
        connection_count: connectionCount,
        max_depth: maxDepth,
        parallel_branches: parallelBranches,
        has_loops: hasLoops,
        complexity_score: window.GraphUtils.calculateComplexityScore(
            nodes.length, connectionCount, maxDepth, parallelBranches, hasLoops
        )
    };
}
```

#### 3. connection_system.js
**Current:** Has inline `generateN8NCurvedPath()` method

**Change to:**
```javascript
// REFACTORED (2025-12-17): Now uses centralized SVG utilities
generateN8NCurvedPath(startX, startY, endX, endY) {
    return window.SvgPathUtils.generateN8NCurvedPath(startX, startY, endX, endY);
}
```

#### 4. connection_manager.js
**Current:** Has inline `createCurvedPath()` method

**Change to:**
```javascript
// REFACTORED (2025-12-17): Now uses centralized SVG utilities
createCurvedPath(startX, startY, endX, endY) {
    return window.SvgPathUtils.generateCurvedPath(startX, startY, endX, endY, 0.5);
}
```

---

## Phase 3: Future Enhancements (Optional)

Once Phase 2 is stable, consider:

1. **Remove Wrapper Methods**: After confirming no external dependencies, remove the thin wrapper methods and call utilities directly throughout the codebase

2. **Add Unit Tests**: Create test files for each utility module
   ```
   utils/
   ├── coordinate_utils.js
   ├── coordinate_utils.test.js  # Unit tests
   ├── graph_utils.js
   ├── graph_utils.test.js
   └── ...
   ```

3. **ES Module Migration**: When Odoo 18+ supports ES modules better, convert from `window.X` pattern to proper imports:
   ```javascript
   // Future
   import { screenToCanvas, snapToGrid } from './utils/coordinate_utils.js';
   ```

4. **TypeScript Definitions**: Add JSDoc or .d.ts files for better IDE support

---

## Testing Checklist

Before considering Phase 2 complete:

- [ ] Canvas pan/zoom works correctly
- [ ] Node dragging snaps to grid
- [ ] Lasso selection captures correct nodes
- [ ] Connection bezier curves render properly
- [ ] Workflow paste/assembly works (theatrical mode)
- [ ] Node tooltips appear on hover
- [ ] Delete selected nodes clears perimeter
- [ ] All console.log statements show utility loading

---

## Risk Assessment

| Risk | Mitigation |
|------|------------|
| Breaking existing functionality | Keep methods as wrappers, don't remove inline code yet |
| Load order issues | Utilities load before managers in manifest |
| Missing window.X reference | Index.js verifies all utilities loaded |
| Performance regression | Pure functions should be same or faster |

---

## Success Metrics

- **Code Reduction**: ~200 lines moved to utilities (estimate)
- **Single Source**: Each algorithm defined once
- **Discoverability**: New developers find utilities easily
- **Future-Proof**: Ready for ES module migration
