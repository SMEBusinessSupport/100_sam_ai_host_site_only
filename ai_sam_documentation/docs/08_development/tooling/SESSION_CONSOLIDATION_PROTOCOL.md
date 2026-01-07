# 🚨 **SESSION CONSOLIDATION PROTOCOL** 🚨
## Mandatory AI Session Lifecycle Management for The AI Automator

### **📋 WHEN TO EXECUTE THIS PROTOCOL**

**MANDATORY TRIGGERS:**
- [ ] Claude session is about to compact due to size
- [ ] Major context shift or architectural decision point
- [ ] Before starting significant new feature work
- [ ] When AI suggests "improvements" to working systems
- [ ] Every 2 hours of active development
- [ ] When switching between Strategic Claude and Dev Claude

---

## **🎯 CONSOLIDATION CHECKLIST - STRATEGIC CLAUDE RESPONSIBILITIES**

### **1. Architectural Integrity Audit**
- [ ] **Above/Below Line Architecture**: Confirm no suggestions to change proven N8N integration strategy
- [ ] **Model Name Compliance**: Verify use of correct names: `canvas`, `nodes`, `connections`, `executions` (NOT workflow.definition.v2)
- [ ] **External Dependency Check**: No external N8N server installations or framework additions suggested
- [ ] **Vanilla JS Compliance**: No React, Vue, OWL, or bundling suggestions made
- [ ] **Current Focus Maintained**: Still focused on fixing N8N overlay popup issue

### **2. Documentation Currency Review**
- [ ] **Technical Documentation**: Is `/docs/architecture/above_below_line_odoo_architecture.md` still accurate?
- [ ] **Session Introduction**: Does `/docs/aaa_module_introduction.md` reflect current state?
- [ ] **Consolidation Plan**: Is `/docs/development/250928_existing_consolidation_and_regroup_of_files.md` being followed?
- [ ] **New Documentation**: Any new architectural decisions that need documenting?

### **3. Strategic Alignment Verification**
- [ ] **Primary Objective**: Still focused on fixing broken overlay popup (open_overlay.js)
- [ ] **Scope Creep Check**: No unrelated features or "nice-to-haves" introduced
- [ ] **Architecture Drift**: No deviation from proven working components
- [ ] **Decision Consistency**: All decisions align with established architectural principles

---

## **🛠️ CONSOLIDATION CHECKLIST - DEV CLAUDE RESPONSIBILITIES**

### **4. File Hygiene Audit**
- [ ] **Redundant Files**: Identify any duplicate or unnecessary files created
- [ ] **Uncertain Files Triage**: Move experimental/broken files to `uncertain_files/` directory
- [ ] **File Consolidation**: Check if new files should have been part of existing files
- [ ] **Asset Manifest**: Verify all new files are properly declared in `__manifest__.py`

### **5. Code Quality Standards Verification**
- [ ] **NO FALLBACKS**: Verify ZERO fallback mechanisms or default values created
- [ ] **Debug Lines**: Confirm ALL functions have mandatory debug logging (entry/exit)
- [ ] **Error Handling**: No generic try/catch blocks - all errors are specific and explicit
- [ ] **State Verification**: All functions verify state before proceeding
- [ ] **Silent Operations**: No operations that can fail without explicit logging

### **6. Implementation Integrity Check**
- [ ] **Working Code Protection**: No changes made to working components
- [ ] **Model References**: All database operations use correct model names
- [ ] **Asset Loading**: All CSS/JS properly loaded in manifest
- [ ] **Controller Compliance**: All endpoints follow established patterns

---

## **🚨 CRITICAL VIOLATION INDICATORS**

**STOP ALL WORK AND RESET IF ANY OF THESE OCCURRED:**

### **Strategic Violations:**
- Suggested external N8N server installation
- Recommended framework additions (React, Vue, etc.)
- Proposed changing above/below line architecture
- Lost focus on overlay popup issue
- Suggested breaking working components

### **Development Violations:**
- Created fallback mechanisms or default values
- Added generic error handling without specific identification
- Created files without proper debug logging
- Made silent operations that can fail without logging
- Modified working code without explicit user request

---

## **📊 SESSION METRICS TRACKING**

### **Progress Indicators**
- [ ] **Primary Issue**: Overlay popup investigation status
- [ ] **File Count**: Number of files added/modified/removed
- [ ] **Debug Coverage**: Percentage of functions with proper logging
- [ ] **Documentation Updated**: Number of docs requiring updates
- [ ] **Technical Debt**: Files moved to uncertain_files directory

### **Quality Indicators**
- [ ] **Zero Fallbacks**: Confirm no fallback code created
- [ ] **Explicit Errors**: All error handling is specific and logged
- [ ] **Architecture Compliance**: No architectural drift detected
- [ ] **Working Code Preserved**: No working components broken

---

## **🔄 CONSOLIDATION HANDOVER PROCESS**

### **For Strategic Claude → Dev Claude Handover:**
1. **Share this protocol** + above_below_line_odoo_architecture.md
2. **Confirm current focus**: Fix overlay popup in open_overlay.js
3. **Specify constraints**: No fallbacks, debug everything, preserve working code
4. **Define success**: Overlay opens, shows N8N nodes, allows selection

### **For Dev Claude → Strategic Claude Handover:**
1. **Report file changes**: List all files created/modified/moved
2. **Confirm code quality**: No fallbacks, full debug coverage
3. **Document issues**: Any problems discovered or blockers encountered
4. **Request guidance**: Specific architectural questions or decisions needed

---

## **📝 CONSOLIDATION DOCUMENTATION TEMPLATE**

**Session ID**: [Date-Time-Claude-Type]
**Duration**: [Start-End Time]
**Focus Area**: [Primary objective worked on]

### **Completed Actions:**
- [ ] Files modified: [List with brief description]
- [ ] Debug coverage: [Functions updated with logging]
- [ ] Issues resolved: [Specific problems fixed]
- [ ] Architecture compliance: [Adherence verified]

### **Quality Assurance:**
- [ ] Zero fallbacks created
- [ ] All functions have debug logging
- [ ] No working code broken
- [ ] Proper error handling implemented

### **Handover Notes:**
- **Next Priority**: [Specific next action needed]
- **Blocking Issues**: [Problems requiring resolution]
- **Architectural Questions**: [Decisions needed from Strategic Claude]

---

## **⚡ QUICK REFERENCE - SESSION RESET COMMANDS**

**For Strategic Claude:**
```
"Please read SESSION_CONSOLIDATION_PROTOCOL.md and above_below_line_odoo_architecture.md before proceeding. Confirm understanding of: 1) Current focus on overlay popup fix, 2) Above/below line architecture, 3) No fallbacks policy, 4) Correct model names usage."
```

**For Dev Claude:**
```
"Please read SESSION_CONSOLIDATION_PROTOCOL.md and implement the overlay popup fix in open_overlay.js. Requirements: 1) Full debug logging, 2) No fallbacks, 3) Specific error handling, 4) Preserve working code, 5) Use correct model names."
```

---

**This protocol ensures consistent quality and prevents AI-generated technical debt across all sessions.**