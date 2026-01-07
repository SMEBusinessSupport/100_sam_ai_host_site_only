# Canvas & Node Overlay Research - Milestone 3

## The Node Overlay Challenge

### What You're Trying to Achieve
- Visual workflow editor similar to N8N's canvas
- Drag-and-drop nodes onto canvas
- Connect nodes with flow lines
- Interactive node configuration
- Integration within Odoo's interface

### N8N Canvas Architecture (Research Needed)

#### Key Components to Investigate
1. **Canvas Container**: How N8N renders the workspace
2. **Node Rendering**: How individual nodes are drawn and positioned
3. **Connection Lines**: How nodes are connected visually
4. **Interaction Layer**: Mouse events, drag/drop, selection
5. **Data Flow**: How canvas state syncs with workflow data

#### Research Tasks
- [ ] Examine N8N's frontend source code
- [ ] Identify the main canvas component
- [ ] Document the node overlay implementation
- [ ] Understand the event handling system
- [ ] Map out the data structures used

### Odoo OWL Canvas Options

#### Option 1: Custom OWL Canvas Component
**Pros**: Full control, native Odoo integration
**Cons**: Complex to build from scratch
**Research**: Study existing Odoo diagram components

#### Option 2: Embed N8N Canvas (iframe)
**Pros**: Reuse existing functionality
**Cons**: Limited integration, styling challenges
**Research**: Test iframe embedding feasibility

#### Option 3: Third-Party Canvas Library
**Pros**: Proven solution, faster development
**Cons**: Additional dependency, integration work
**Libraries to Research**:
- Fabric.js
- Konva.js
- Paper.js
- D3.js

#### Option 4: SVG-Based Custom Solution
**Pros**: Lightweight, web-native
**Cons**: Manual implementation of all interactions
**Research**: SVG manipulation in OWL

## Immediate Research Session Plan

### Session 1: N8N Canvas Deep Dive (2 hours)
1. **Setup**: Get N8N running in development mode
2. **Explore**: Navigate to workflow editor, open browser dev tools
3. **Document**:
   - Main canvas element structure
   - Node rendering approach
   - Event listeners and handlers
   - CSS classes and styling approach
4. **Extract**: Key JavaScript/TypeScript files responsible for canvas

### Session 2: Odoo OWL Canvas Capabilities (1 hour)
1. **Research**: Existing Odoo components with diagram/canvas features
2. **Test**: Create simple OWL component with SVG or Canvas element
3. **Document**: OWL's capabilities for interactive graphics
4. **Prototype**: Basic draggable element proof of concept

### Session 3: Integration Decision (30 minutes)
1. **Compare**: Pros/cons of each approach based on research
2. **Decide**: Choose primary approach and backup option
3. **Plan**: Next steps for implementation

## Key Questions to Answer
1. How complex is N8N's canvas implementation?
2. Can we reasonably recreate core functionality in OWL?
3. What's the minimum viable canvas we need for v1?
4. How will this integrate with Odoo's existing UI patterns?

## Success Criteria for This Milestone
- [ ] Clear understanding of N8N's canvas architecture
- [ ] Documented approach for Odoo integration
- [ ] Working proof of concept for basic node display
- [ ] Decision on implementation strategy
- [ ] Plan for Milestone 4 (actual implementation)