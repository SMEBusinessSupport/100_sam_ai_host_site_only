# SAM AI Ecosystem - Current State Documentation

**Last Updated**: 2025-10-27 (CRITICAL SYNC - New modules & agents discovered)
**Purpose**: Master reference for all agents - The single source of truth about SAM AI's current state
**Maintained By**: Documentation Master (`/docs` agent)

---

## 🎯 Executive Summary

**✅ CORRECTED SCOPE** (2025-10-27):

**SAM AI Ecosystem Path**: `C:\Working With AI\ai_sam\ai_sam\`
**This is the ONLY path /docs scans**

**Total Active Modules**: 15 (all with `__manifest__.py`, excluding backup folders)
**Total Models**: 60+ unique Odoo models
**Total Agents**: 17 active Claude agents
**Agent Knowledge**: 80+ .md files total (includes new module specialists)

---

## ⚠️ CRITICAL SCOPE CORRECTION

**Previous State (WRONG)**:
- ❌ Referenced: `C:\Working With AI\ai_sam\ai_sam_odoo` (PATH DOES NOT EXIST!)
- ❌ Included: `C:\Working With AI\Odoo Projects\custom-modules-v18` (OUT OF SCOPE - dev environment)

**Current State (CORRECT)**:
- ✅ **ONLY PATH**: `C:\Working With AI\ai_sam\ai_sam\`
- ✅ This is the SAM AI ecosystem entrypoint
- ✅ /docs agent scans ONLY this path
- ✅ Agents reference ONLY modules in this path

**Why This Matters**:
The `/docs` agent's mission is to maintain truth about the **SAM AI ecosystem ONLY**. The `custom-modules-v18` folder is Anthony's separate development workspace and is NOT part of SAM AI ecosystem documentation.

---

## 📁 SAM AI Core Modules

All modules are located at: `C:\Working With AI\ai_sam\ai_sam\`

### Foundation Layer

1. **ai_brain** (v18.0.7.0.0) **[VERSION UPDATED!]**
   - **Role**: Core data layer - ALL models live here
   - **Dependencies**: base, mail, web
   - **Key Models**: canvas, nodes, executions, connections, ai.conversation, ai.message, ai.service, ai.token.usage
   - **Philosophy**: "The Brain" - permanent data storage, never uninstall
   - **Model Count**: ~40 models
   - **Recent Change**: Stage 2 complete - Chat session consolidation (sam.chat.session → ai.conversation)

2. **ai_sam** (v18.0.6.1.0) **[VERSION UPDATED!]**
   - **Role**: SAM AI Core Framework - Intelligence engine
   - **Dependencies**: base, web, ai_brain
   - **Key Features**: Canvas framework, Claude API integration, context builder, memory system (merged from ai_sam_memory 2025-10-24)
   - **Philosophy**: The framework that all branches depend on
   - **Model Count**: ~10 models

### Platform Skins (Branch Modules)

3. **ai_sam_memory** (v18.0.1.0.0)
   - **Role**: Knowledge graph visualization platform
   - **Dependencies**: ai_brain, ai_sam
   - **Features**: Apache AGE graph DB, ChromaDB vector search, conversation import
   - **Model Count**: 7 models

4. **ai_sam_workflows** (v18.0.1.0.5) **[VERSION UPDATED!]**
   - **Role**: Workflow automation platform (N8N integration)
   - **Dependencies**: ai_brain, ai_sam
   - **Features**: N8N node library (1,500+ connectors), workflow designer, execution engine
   - **Note**: Platform skin - data stays in ai_brain

5. **ai_sam_creatives** (v18.0.1.0.1)
   - **Role**: Creative content generation platform
   - **Dependencies**: ai_brain, ai_sam
   - **Features**: Multimedia canvas, AI chat integration
   - **Note**: Platform skin - data stays in ai_brain

6. **ai_sam_socializer** (v18.0.2.0.0)
   - **Role**: Social media and blogging platform
   - **Dependencies**: base, web, website_blog, ai_brain, ai_sam
   - **Key Models**: odoo.blog.post, odoo.blog.image, odoo.blog.story
   - **Model Count**: 3 models

7. **ai_sam_messenger** (v18.0.1.0.0)
   - **Role**: Messenger toggle utility
   - **Dependencies**: web, mail
   - **Features**: Collapse/expand chatter panel

8. **ai_sam_members** (v18.0.1.0.0)
   - **Role**: Member management system
   - **Dependencies**: base, base_automation, portal, website, mail
   - **Key Models**: sam.member, res.partner (extended)
   - **Model Count**: 2 models

9. **ai_sam_intelligence** (v18.0.1.0.0)
   - **Role**: Agent registry and knowledge management
   - **Dependencies**: base, ai_brain, ai_sam
   - **Key Models**: ai.agent.registry, ai.agent.knowledge, documentation.intelligence
   - **Model Count**: 3 models

10. **ai_sam_docs** (v18.0.2.0.0)
    - **Role**: Documentation management and tools
    - **Dependencies**: base, web, ai_brain, ai_sam
    - **Key Models**: documentation.intelligence
    - **Model Count**: 1 model

11. **ai_sam_ui** (v18.0.1.0.0)
    - **Role**: Public chat interface for website
    - **Dependencies**: website, ai_sam, ai_brain
    - **Features**: Public-facing chat widget (no login required)

### Supporting Modules

12. **github_app** (v18.0.1.0.0)
    - **Role**: GitHub integration
    - **Dependencies**: base
    - **Key Models**: git.hub, git.hub.app, version.check
    - **Model Count**: 3 models

### New Modules (Added 2025-10-27)

13. **ai_sam_qrcodes** (v18.0.1.0.0) **[NEW!]**
    - **Role**: QR Code generator with custom branding
    - **Dependencies**: ai_brain, ai_sam
    - **Features**: QR code generation, custom colors, center logo overlay, download as PNG
    - **Note**: Platform skin - menu under SAM AI → Extras

14. **ai_youtube_transcribe** (v18.0.1.2.0) **[NEW!]**
    - **Role**: YouTube video transcription using OpenAI Whisper
    - **Dependencies**: base, web
    - **Features**: Download YouTube videos, transcribe with Whisper API
    - **Note**: Standalone module OR integrates with SAM AI if installed

15. **ai_sam_lead_generator** (v18.0.1.0.0) **[NEW!]**
    - **Role**: AI-powered lead generation for Odoo consultancy
    - **Dependencies**: base, crm, ai_sam
    - **Features**: Google search scraping, Odoo website detection, lead scoring, CRM integration
    - **Note**: Find companies using Odoo for consultancy outreach

---

## 🚫 Excluded Paths (DO NOT REFERENCE)

### Future State (Folders Exist but NO __manifest__.py)

These folders exist at `C:\Working With AI\ai_sam\ai_sam\` but are NOT Odoo modules yet:

- **ai_sam_desktop** - Desktop app (post-MVP) - NO __manifest__.py
- **ai_sam_mobile** - Mobile app (future roadmap) - NO __manifest__.py
- **ai_onboarding** - Onboarding workflows (incomplete) - NO __manifest__.py
- **ai_toolbox** - Utility tools (incomplete) - NO __manifest__.py
- **ai_sam_introduction** - Documentation/training folder (NOT a module) - NO __manifest__.py
- **the_ai_automator** - Old name/moved out (DO NOT REFERENCE) - NO __manifest__.py

**Agent Rule**: IGNORE these folders until they have `__manifest__.py` files

### Backup/Temporary Folders (EXCLUDE from Active Count)

- **ai_sam_memory_BACKUP_2025-10-24** - Backup folder (HAS manifest but NOT active module)
- **chromadb**, **chroma_data**, **chroma_data - Copy** - Database/data folders
- **MERGE_SCRIPTS**, **reports**, **Messy Claude Documents Consolidated** - Utility folders

**Agent Rule**: DO NOT count backup folders as active modules, even if they have `__manifest__.py`

### Out of Scope (NOT SAM AI Ecosystem)

- **`C:\Working With AI\Odoo Projects\custom-modules-v18\`** - Anthony's dev environment, NOT part of SAM ecosystem documentation

### Build Artifacts (Always Ignore)

- `__pycache__` (Python bytecode)
- `.git` (version control)
- `node_modules` (JS dependencies)
- `.pytest_cache` (test artifacts)

---

## 🗄️ Database Schema Summary

### Core SAM AI Models (ai_brain)

**Workflow System:**
- canvas
- nodes
- connections
- executions
- workflow_types
- workflow.template
- workflow.business.unit
- api_credentials

**AI Services:**
- ai.service
- ai.service.config
- ai.service.provider
- ai.voice.service
- ai.context.builder

**Conversation System:**
- ai.conversation
- ai.message
- ai.token.usage
- ai.artifact.version
- sam.chat.session
- sam.chat.message

**Memory System:**
- ai.graph.service
- ai.vector.service
- ai.document.extractor
- ai.extractor.plugin
- ai.conversation.import
- ai.memory.config
- ai.memory.import.wizard

**Agent System:**
- ai.agent.definition
- ai.agent.execution
- ai.agent.knowledge
- ai.agent.registry

**SAM Personality & Settings:**
- sam.personality
- sam.user.profile
- sam.user.settings
- sam.environment
- sam.mode.context
- sam.brain.modes
- sam.knowledge.doc
- sam.member

**N8N Integration:**
- node_types
- n8n.simple.supplier
- n8n.simple.node
- n8n.simple.extractor
- n8n.node.category
- workflow.n8n.import.wizard

**Utilities:**
- ai.branches
- canvas.platform
- canvas_pan_move
- dynamic_menus
- documentation_intelligence
- ai.automator.documentation

---

## 🤖 Claude Agent Ecosystem

### Active Agents (17 total) **[6 NEW AGENTS!]**

Located at: `C:\Users\total\.claude\agents\`

**Core Team:**
1. **sam** (7 files) - SAM AI personality agent
2. **odoo-developer** (4+ files) - Elite Odoo 18 developer
3. **odoo-architect** (4+ files) - Solutions architect
4. **odoo-debugger** (5+ files) - Debug expert
5. **odoo-audit** (4+ files) - Code quality auditor
6. **odoo-qa-guardian** **[NEW!]** - Pre-commit quality gate (Odoo 18 error prevention)

**Documentation & Operations:**
7. **documentation-master** (5+ files) - This agent (ecosystem truth keeper)
8. **github** (5+ files) - GitHub workflow expert
9. **recruiter** (6+ files) - Knowledge extraction specialist

**Boardroom (C-Level):**
10. **cto** (5+ files) - Chief Technical Officer (infrastructure strategy)
11. **cmo** (5+ files) - Chief Marketing Officer (strategic marketing)

**Architecture & Quality:**
12. **canvas-core-guardian** (6+ files) - Architecture boundary enforcer

**Module Specialists (NEW!):**
13. **mod-intelligence** **[NEW!]** - ai_sam_intelligence module specialist
14. **mod-sam** **[NEW!]** - SAM AI Core (ai_sam) module specialist
15. **mod-scrapper** **[NEW!]** - ai_sam_lead_generator module specialist

**Sales & Communication:**
16. **sam-sales-support** **[NEW!]** - Sales support & landing page creator
17. **sam-core-chat** **[NEW!]** - Communication experience specialist (voice + behavior)

**Total Knowledge Files**: 80+ .md files across all agents (up from 56)

---

## 🏗️ Architecture Overview

### V3 Architecture Philosophy

```
Ground Layer: ai_brain (data stays here forever)
     ↓
Framework: ai_sam (canvas core, AI services, intelligence)
     ↓
Branches: Platform skins (memory, workflows, creatives, etc.)
```

**Platform Skin Model:**
- ALL data models live in `ai_brain`
- Platform skins provide UI-only components
- Uninstalling platforms does NOT delete data
- Data remains protected in The Brain

### Dependency Flow

```
ai_brain (foundation)
  ├─→ ai_sam (framework)
  │    ├─→ ai_sam_memory
  │    ├─→ ai_sam_workflows
  │    ├─→ ai_sam_creatives
  │    ├─→ ai_sam_socializer
  │    ├─→ ai_sam_messenger
  │    ├─→ ai_sam_members
  │    ├─→ ai_sam_intelligence
  │    ├─→ ai_sam_docs
  │    └─→ ai_sam_ui
  │
  └─→ github_app (standalone)
```

---

## 📊 Current State Snapshot

### System Health
- ✅ 15 active SAM AI modules installed (excluding backups)
- ✅ 60+ models registered
- ✅ 17 agents with updated knowledge (6 new agents!)
- ⚠️ **27 agent knowledge files** still reference `the_ai_automator` (NEEDS CLEANUP)
- ⚠️ **8 agent knowledge files** still reference `ai_sam_odoo` path (DOESN'T EXIST)
- ⚠️ **6 agent knowledge files** reference `custom-modules-v18` (OUT OF SCOPE)
- ✅ All excluded paths documented
- ✅ Scope corrected (SAM ecosystem ONLY)
- ✅ All manifests standardized (author, maintainer, website, icon)

### Recent Changes (2025-10-27) **[CRITICAL SYNC]**
- **NEW MODULES DISCOVERED**: 3 modules not in previous docs!
  - `ai_sam_qrcodes` v18.0.1.0.0 (QR code generator)
  - `ai_youtube_transcribe` v18.0.1.2.0 (YouTube transcription)
  - `ai_sam_lead_generator` v18.0.1.0.0 (Lead generation system)
- **NEW AGENTS DISCOVERED**: 6 agents not in previous docs!
  - `mod-intelligence`, `mod-sam`, `mod-scrapper` (module specialists)
  - `sam-sales-support`, `sam-core-chat` (sales & communication)
  - `odoo-qa-guardian` (quality gate)
- **VERSION BUMPS**:
  - `ai_brain`: 18.0.3.8.0 → 18.0.7.0.0 (Stage 2: Chat consolidation complete)
  - `ai_sam`: 18.0.5.3.0 → 18.0.6.1.0 (Memory system merged)
  - `ai_sam_workflows`: 18.0.1.0.1 → 18.0.1.0.5 (Multiple improvements)
- **EXCLUSIONS ADDED**:
  - `ai_sam_introduction` (docs folder, not a module)
  - `the_ai_automator` (old name, no manifest)
  - `ai_sam_memory_BACKUP_2025-10-24` (backup, not active)

### Previous Changes (2025-10-16)
- **MANIFEST STANDARDIZATION**: All modules aligned with standards
- Automation script: `C:\Users\total\update_manifests.py`

### Previous Changes (2025-10-13)
- **SCOPE CORRECTION**: Fixed entrypoint path
- Confirmed: `ai_sam\ai_sam\` is correct path

### Known Issues (REQUIRES ACTION)
- ⚠️ **27 files** reference `the_ai_automator` (should be excluded)
- ⚠️ **8 files** reference `ai_sam_odoo` (path doesn't exist)
- ⚠️ **6 files** reference `custom-modules-v18` (out of scope)
- **ACTION NEEDED**: Agent knowledge files need cleanup pass

---

## 🔑 Key Rules for Agents

### Module Reference Rules

**✅ ALLOWED to reference (15 active modules):**
- **Foundation**: ai_brain, ai_sam
- **Platform Skins**: ai_sam_memory, ai_sam_workflows, ai_sam_creatives, ai_sam_socializer
- **Tools**: ai_sam_messenger, ai_sam_members, ai_sam_intelligence, ai_sam_docs, ai_sam_ui
- **Utilities**: ai_sam_qrcodes, ai_youtube_transcribe, ai_sam_lead_generator
- **Supporting**: github_app

**❌ FORBIDDEN to reference:**
- **Future (no manifest)**: `ai_sam_desktop`, `ai_sam_mobile`, `ai_onboarding`, `ai_toolbox`, `ai_sam_introduction`
- **Old/Moved**: `the_ai_automator`, `th_ai_automator` (DO NOT REFERENCE - no manifest)
- **Backups**: `ai_sam_memory_BACKUP_2025-10-24` (has manifest but NOT active)
- **Wrong paths**: `ai_sam_odoo` (path doesn't exist!)
- **Out of scope**: `custom-modules-v18` (Anthony's dev environment)
- **Build artifacts**: `__pycache__`, `.git`, `node_modules`, `chromadb`, `chroma_data`

### Manifest Standards (NEW - 2025-10-16)

When creating or updating ANY SAM AI module manifest, use these standardized fields:

```python
'author': 'Anthony Gardiner - Odoo Consulting & Claude AI',
'maintainer': 'Anthony Gardiner <anthony@sme.ec>',
'website': 'https://sme.ec',
'images': ['static/description/icon.png'],  # SAM icon - use this exact path
'license': 'LGPL-3',
```

**Full documentation**: [manifest_standards.md](file://C:/Users/total/.claude/agents/odoo-developer/manifest_standards.md)

**Automation script**: `C:\Users\total\update_manifests.py`

### Validation Checklist

Before referencing any module:
- [ ] Is it in `C:\Working With AI\ai_sam\ai_sam\`?
- [ ] Does `__manifest__.py` exist?
- [ ] Is it NOT in the excluded list?
- [ ] Is it documented in this current_state.md?

If all YES → SAFE TO REFERENCE ✅
If any NO → DO NOT REFERENCE ❌

---

## 🔄 Update Protocol

This file is automatically maintained by the `/docs` agent:
- **Scheduled**: Daily at 8 AM
- **Event-Driven**: After module upgrades
- **Manual**: On-demand via `/docs` command

**Last Scan**: 2025-10-27 (CRITICAL SYNC - found 3 new modules, 6 new agents)
**Next Scheduled Scan**: 2025-10-28 08:00

**Scan Results**:
- Discovered: 15 active modules (up from 13)
- Discovered: 17 agents (up from 12)
- Version updates: ai_brain, ai_sam, ai_sam_workflows
- Misalignments: 41 agent knowledge files need cleanup

---

## 📞 Questions?

- **Agent Question**: Ask `/docs` agent for clarification
- **Infrastructure Question**: Ask `/cto` agent
- **Module Question**: Ask `/developer` or `/odoo-architect`

**Remember**: Current state = Truth. Always verify against this file before making assumptions.

---

**End of Current State Documentation** ✅
