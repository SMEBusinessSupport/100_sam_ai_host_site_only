# SAM AI Architecture Decisions
**Date:** 2025-12-06
**Status:** ✅ Decisions Made by Anthony

---

## 📋 Strategic Decisions

### **Q1: What happens to ai_brain?**
**Decision:** ✅ **DEPRECATE**

**Action Items:**
- [ ] Audit models still in `04-samai-brain` repo
- [ ] Create migration plan to move remaining models to base modules
- [ ] Archive ai_brain module once empty
- [ ] Update documentation to mark ai_brain as deprecated

---

### **Q2: Where should vendor_library live?**
**Decision:** ✅ **Keep in ai_sam**

**Rationale (Anthony's words):**
> "The challenge we had with many api/suppliers originally was where to 'put that knowledge'. As it worked out, ai_sam was '1st module needed', workflow depended on it, so it was concluded we would manage primary supplier knowledge in there."

**Translation:**
- ai_sam = **Supplier Knowledge Repository**
- vendor_library = supplier-specific assets (icons, API configs, metadata)
- Workflows module depends on ai_sam for supplier knowledge
- This is working as intended ✅

**Action Items:**
- [ ] Keep `ai_sam/static/src/vendor_library/` where it is
- [ ] Document ai_sam's role as "Supplier Knowledge Hub"
- [ ] Create clear rules: "New supplier assets → always ai_sam"

---

### **Q3: Is ai_sam a "skin" or a "framework"?**
**Decision:** ✅ **ai_sam is the "Supplier Knowledge Hub" (not pure skin)**

**Anthony's Clarification:**
> "Node shapes etc, execute, things that were not api specific would reside in workflows."

**Roles Defined:**

| Module | Role | Contains |
|--------|------|----------|
| **ai_sam** | Supplier Knowledge Hub | Supplier-specific assets (icons, API configs, metadata), core views |
| **ai_sam_workflows** | Workflow Execution Engine | Workflow-agnostic logic (node shapes, execution, canvas) |

**Translation:**
- **Supplier-specific** (API knowledge, icons, credentials) → ai_sam
- **Workflow-generic** (canvas, execution, node rendering) → ai_sam_workflows

---

### **Q4: Two-layer or three-layer architecture?**
**Decision:** ✅ **Two-layer (with dependency chain)**

**Anthony's Description:**
> "I think it is 2 layer, YET, workflows depends on ai_sam and ai_sam_base also?"

**Clarified Architecture:**

```
LAYER 1: DATA (Base Modules - "Core Intelligence")
├── ai_sam_base/              # Core SAM data models
│   └── "Preserve this - it's the intelligence"
│
└── ai_sam_workflows_base/    # Workflow data models
    └── "Preserve this - it's the intelligence"

LAYER 2: PRESENTATION ("Skins" - Evolve/Break/Rebuild)
├── ai_sam/                   # Core SAM UI + Supplier Knowledge
│   ├── Depends on: ai_sam_base
│   └── Contains: Views, supplier assets (vendor_library)
│
└── ai_sam_workflows/         # Workflow UI + Execution
    ├── Depends on: ai_sam_workflows_base
    ├── Depends on: ai_sam (for supplier knowledge)
    └── Contains: Views, controllers, overlay UI
```

**Dependency Chain:**
```
ai_sam_workflows (skin)
    │
    ├──→ ai_sam_workflows_base (data) ✅ Normal dependency
    │
    └──→ ai_sam (skin) ⚠️ Skin depends on skin
            │
            └──→ ai_sam_base (data) ✅ Normal dependency
```

**The Key Insight:**
- This is **NOT** a pure two-layer pattern (skin-depends-on-skin exists)
- This is a **dependency chain** where workflows needs supplier knowledge from ai_sam
- This is **intentional and correct** given the supplier knowledge centralization

---

## 🎯 Final Architecture Definition

### **The "Core Intelligence + Evolving Skins" Pattern**

**Principle:** Preserve data, allow skins to evolve/break/rebuild

```
┌─────────────────────────────────────────────────────────────┐
│ PROTECTED LAYER: Core Intelligence (Don't Break This!)      │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ai_sam_base/                  ai_sam_workflows_base/       │
│  ├── 44 data models            ├── 15 data models           │
│  ├── Core SAM intelligence     ├── Workflow intelligence    │
│  └── STABLE (preserve always)  └── STABLE (preserve always) │
│                                                              │
└─────────────────────────────────────────────────────────────┘
                   ▲                         ▲
                   │                         │
                   │ (depends on)            │ (depends on)
                   │                         │
┌──────────────────┴─────────────────────────┴───────────────┐
│ EVOLVING LAYER: Skins (Can Break/Rebuild)                  │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ai_sam/                       ai_sam_workflows/            │
│  ├── Role: Supplier Knowledge  ├── Role: Workflow Execution│
│  ├── Views for ai_sam_base     ├── Views for workflows_base│
│  ├── vendor_library/ ✅        ├── Controllers             │
│  │   (Supplier assets)         ├── Overlay UI              │
│  └── Can evolve/break          └── Depends on ai_sam ✅    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 📐 Module Ownership Rules

### **ai_sam (Supplier Knowledge Hub)**

**OWNS:**
- ✅ Supplier-specific assets (icons, API configs, metadata)
- ✅ vendor_library folder
- ✅ Core SAM views
- ✅ Shared UI components

**FORBIDDEN:**
- ❌ Data models (those go in ai_sam_base)
- ❌ Workflow execution logic (that's ai_sam_workflows)

**AI Agent Guidance:**
> "Adding a new API supplier? Put icons/metadata in ai_sam/static/src/vendor_library/"

---

### **ai_sam_base (Core SAM Data)**

**OWNS:**
- ✅ Core SAM data models (conversations, messages, agents, memory, etc.)
- ✅ SAM behavior/personality models
- ✅ Provider/service definitions

**FORBIDDEN:**
- ❌ Views (those go in ai_sam)
- ❌ Static assets (those go in ai_sam)
- ❌ Workflow-specific models (those go in ai_sam_workflows_base)

---

### **ai_sam_workflows (Workflow Execution Engine)**

**OWNS:**
- ✅ Workflow UI (canvas, overlays)
- ✅ Controllers (HTTP endpoints)
- ✅ Workflow-agnostic execution logic
- ✅ Node rendering (shapes, positioning)

**DEPENDS ON:**
- ai_sam_workflows_base (for workflow data models)
- ai_sam (for supplier knowledge - icons, API configs)

**FORBIDDEN:**
- ❌ Data models (those go in workflows_base)
- ❌ Duplicate supplier assets (use ai_sam's vendor_library)
- ❌ Supplier-specific code (that's ai_sam's job)

---

### **ai_sam_workflows_base (Workflow Data)**

**OWNS:**
- ✅ Workflow data models (canvas, nodes, executions)
- ✅ N8N node definitions
- ✅ Business unit management

**READS FROM:**
- ai_sam/static/src/vendor_library/ (computes icon URLs)

**FORBIDDEN:**
- ❌ Views (those go in ai_sam_workflows)
- ❌ Controllers (those go in ai_sam_workflows)
- ❌ Duplicate supplier assets

---

## 🚨 The Skin-on-Skin Dependency (INTENTIONAL)

### **Why ai_sam_workflows depends on ai_sam:**

**Problem:**
- Workflows need to display supplier icons (ActiveCampaign, Google, etc.)
- Workflows need supplier API configurations
- Workflows need supplier metadata (node types, operations)

**Options Considered:**
1. ❌ Duplicate assets in ai_sam_workflows (violates DRY)
2. ❌ Move assets to shared library module (over-engineering)
3. ✅ **ai_sam_workflows depends on ai_sam** (centralized supplier knowledge)

**Decision:** Option 3 is CORRECT

**Why it works:**
- ai_sam is the "Supplier Knowledge Hub" (intentional role)
- All modules needing supplier info depend on ai_sam
- Single source of truth for supplier assets
- ai_sam is foundational (loaded before workflows)

**This is NOT a violation** - it's the intended architecture!

---

## 🎯 AI Agent Guidance Rules

### **When adding a new supplier (e.g., "Stripe"):**

```markdown
1. Add icon files → ai_sam/static/src/vendor_library/Stripe/
   - stripe.svg
   - stripe.png (optional)
   - api_config.json

2. Update metadata → ai_sam/static/src/vendor_library/_registry/node_metadata.json
   - Add Stripe entry

3. Add N8N node definition → ai_sam_workflows_base/models/n8n_simple_nodes.py
   - Database will auto-compute icon URLs pointing to ai_sam

4. Add UI for Stripe nodes → ai_sam_workflows/static/src/automator/
   - Overlay will fetch icon URLs from database
   - Icons load from ai_sam vendor_library ✅
```

---

### **When adding workflow-agnostic logic:**

```markdown
Examples: Node shapes, canvas rendering, execution engine

→ Add to: ai_sam_workflows_base (data) or ai_sam_workflows (UI)
→ Do NOT add supplier-specific code here
→ If you need supplier info, read from ai_sam
```

---

### **When adding core SAM features:**

```markdown
Examples: Conversation management, agent definitions, memory system

→ Data models: ai_sam_base/models/
→ Views/UI: ai_sam/views/ or ai_sam/static/
→ Do NOT add workflow-specific code here
```

---

## 📊 Validation: Icon Bug (Retrospective)

### **The Bug We Just Fixed:**

**Problem:** Icons showing emoji fallbacks instead of SVG files

**Root Cause:** Frontend constructing wrong paths instead of using database URLs

**Why it happened:** Unclear architecture guidance
- Frontend developer didn't know icons lived in ai_sam
- Tried to construct paths pointing to ai_sam_workflows
- Database correctly computed URLs pointing to ai_sam
- Frontend ignored database, used hardcoded logic

**How architecture clarity prevents this:**
- ✅ "Supplier assets always in ai_sam" (documented rule)
- ✅ "Use database-provided URLs" (single source of truth)
- ✅ "Don't construct paths in frontend" (boring pattern)

**Fix validated the architecture:**
- Database (workflows_base) computes URLs → ai_sam/vendor_library ✅
- Frontend (workflows) uses database URLs ✅
- Icons load correctly ✅

---

## ✅ Summary of Decisions

| Question | Decision | Action |
|----------|----------|--------|
| Q1: ai_brain endgame | Deprecate | Migrate remaining models, archive module |
| Q2: vendor_library location | Stay in ai_sam | Document as "Supplier Knowledge Hub" |
| Q3: ai_sam role | Supplier Knowledge Hub | Not pure skin, intentional data repository |
| Q4: Architecture layers | Two-layer + dependency chain | ai_sam_workflows → ai_sam is CORRECT |

---

## 📝 Next Steps

### **Phase 1: Document Current Architecture** (Priority 1)
- [ ] Create `ARCHITECTURE_GUIDE.md` in ai_sam_docs
- [ ] Define module ownership matrix
- [ ] Write AI agent placement rules
- [ ] Document dependency chain (with diagrams)

### **Phase 2: Audit ai_brain** (Priority 2)
- [ ] List models still in 04-samai-brain repo
- [ ] Categorize: Core SAM or Workflow?
- [ ] Create migration plan
- [ ] Schedule migration sprints

### **Phase 3: Enforce Architecture** (Priority 3)
- [ ] Add validation checks (forbidden patterns)
- [ ] Update agent prompts with ownership rules
- [ ] Create architecture decision log (this document!)

---

**Decisions approved by:** Anthony
**Documented by:** Claude (CTO Architect)
**Date:** 2025-12-06
**Status:** ✅ Ready to implement
