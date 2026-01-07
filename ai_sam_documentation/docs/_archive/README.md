# SAM AI V3 - Architecture Documentation

**Version:** 3.5.0 | **Last Updated:** October 9, 2025

---

## 📚 Documentation Index

### Core Documentation

#### 1. [SAM_AI_V3_ARCHITECTURE.md](./SAM_AI_V3_ARCHITECTURE.md)
**Complete system architecture overview**

- Executive summary
- Three-layer architecture (ai_brain → ai_sam → branches)
- Module breakdown and responsibilities
- Data flow patterns
- Key features & capabilities
- API endpoints reference
- File structure
- Performance & security considerations
- Future roadmap

**Start here** for understanding the entire SAM AI system.

#### 2. [SAM_AI_V3_DATABASE_SCHEMA.sql](./SAM_AI_V3_DATABASE_SCHEMA.sql)
**Comprehensive PostgreSQL database schema**

- All 40+ table definitions
- Complete field documentation
- Indexes and foreign keys
- Materialized views
- Verification queries
- Data types and constraints

**Use this** for database development, migrations, and schema understanding.

---

## 🏗️ Quick Architecture Reference

### Module Structure

```
ai_brain (Data Layer)
  └── 40+ pure data models, NO views, NO controllers

ai_sam (Framework Layer)
  ├── Controllers (API endpoints)
  ├── JavaScript (Frontend)
  └── Views (UI definitions)

Branches (Specialized Features)
  ├── Poppy (Mind Maps) - merged into ai_sam
  ├── Memory System - merged into ai_sam
  └── Automator (Workflows) - merged into ai_sam
```

### Core Models Quick Reference

**AI Service & Conversations:**
- `ai.service.config` - API configuration (Claude, OpenAI, local)
- `ai.conversation` - Chat threads
- `ai.message` - Individual messages
- `ai.token.usage` - Usage tracking

**User System:**
- `sam.user.profile` - User relationships & learned facts
- `sam.user.settings` - User preferences & active mode
- `sam.mode.context` - Power Prompts (dev, sales, marketing, etc.)

**Canvas Platform:**
- `ai.branch` - Branch registry (meta-architecture)
- `canvas` - Universal workflows/mind-maps
- `nodes` - Node definitions
- `connections` - Node connections
- `executions` - Execution history

**Memory System:**
- `ai.memory.config` - Graph/Vector DB config
- `ai.extractor.plugin` - Learned extraction patterns

---

## 🚀 Quick Start Guide

### For Developers

1. **Understand the architecture:**
   - Read [SAM_AI_V3_ARCHITECTURE.md](./SAM_AI_V3_ARCHITECTURE.md)
   - Study the three-layer design

2. **Review the database:**
   - Open [SAM_AI_V3_DATABASE_SCHEMA.sql](./SAM_AI_V3_DATABASE_SCHEMA.sql)
   - Run verification queries

3. **Explore the code:**
   - Data models: `ai_brain/models/`
   - Services: `ai_sam/controllers/`
   - Frontend: `ai_sam/static/src/js/`

4. **File creation policy:**
   - New files go to: `claudes floating files/` organized by type
   - No random files in module directories

### For New Contributors

**Key Principles:**
- `ai_brain` = Data only (models, security, data files)
- `ai_sam` = Framework (controllers, views, JS, CSS)
- Branches = Specialized features (registered via `ai.branch`)

**Adding a new branch:**
1. Create `ai.branch` record (no code changes!)
2. Optionally create dedicated module
3. Register platform renderer in JavaScript
4. Canvas system automatically loads it

---

## 🔄 Architecture Evolution

### V3.5.0 (October 2025) - Current
- ✅ Multi-user relationship system
- ✅ Power Prompts (mode-based AI)
- ✅ Environment-aware system prompts
- ✅ Memory system (Graph + Vector DB)
- ✅ Universal canvas platform
- ✅ Merged all branches into core

### V3.0.0 (September 2025)
- Merged ai_sam_memory into ai_sam
- Merged the_ai_automator into ai_sam
- Merged ai_poppy into ai_sam
- Unified canvas platform

### V2.0.0
- Initial SAM AI framework
- Basic Claude integration
- Separate branch modules

---

## 📊 System Metrics

**Current Implementation:**
- **40+ Data Models** (ai_brain)
- **15+ Controllers** (ai_sam)
- **20+ JavaScript Files** (Frontend)
- **30+ Views** (UI definitions)
- **1,500+ N8N Node Types** (Automator platform)
- **Multi-User Support** (Relationship-based AI)

---

## 🔗 Related Resources

### Internal Documentation
- System Prompt: `ai_brain/data/SAM_AI_MASTER_SYSTEM_PROMPT_V2.md`
- Manifest: `ai_sam/__manifest__.py`
- Security: `ai_brain/security/ir.model.access.csv`

### External Links
- [Odoo 18 Documentation](https://www.odoo.com/documentation/18.0/)
- [Claude API Docs](https://docs.anthropic.com/)
- [Apache AGE](https://age.apache.org/)
- [ChromaDB](https://www.trychroma.com/)

---

## 🗂️ Outdated Documentation

**Moved to:** `C:\Working With AI\ai_sam\ai_sam_odoo\claudes floating files\outdated_architecture_docs\`

The following files were **outdated and moved:**
- `above_below_line_odoo_architecture.md` - Referenced old "the_ai_automator" module
- `AI_Automator_Architecture.html` - N8N integration docs (pre-merge)
- `complete_system_architecture.md` - V2 architecture
- `database_schema.sql` - Old schema (pre-V3)
- `database_schema_visual.html` - Outdated visualization
- `field_alignment_tracker.html` - V2 field tracker
- `n8n_database_schema_*.md` - Pre-merge N8N docs
- `tech_stack_consolidation_analysis.md` - V2 analysis

**Why moved:**
- Referenced deleted modules ("the_ai_automator")
- Described pre-merge architecture
- Contained outdated model names
- No longer accurate after V3 refactor

---

## 🛠️ Development Guidelines

### Module Responsibilities

**ai_brain (Data Layer):**
- ✅ Data models only
- ✅ Security rules
- ✅ Data files
- ❌ NO views
- ❌ NO controllers
- ❌ NO JavaScript

**ai_sam (Framework Layer):**
- ✅ Controllers (API)
- ✅ Views (UI)
- ✅ JavaScript (Frontend)
- ✅ CSS (Styling)
- ❌ NO data models (use ai_brain)

### Code Review Priorities

From recent architecture review, these need attention:

1. **Token Management**
   - Integrate tiktoken for pre-call estimation
   - Smart context window (token-based, not message count)

2. **API Reliability**
   - Add retry logic with exponential backoff
   - Implement rate limiting per user
   - Response caching (Redis/memcached)

3. **Security**
   - SQL injection audit (all `cr.execute()`)
   - Validate file path access
   - Trust score feature implementation

4. **Performance**
   - Batch operations in context builder
   - JSON Schema validation for workflows
   - Database query optimization

---

## 📝 Notes

**System Prompt Location:**
The master system prompt is loaded from:
1. `ai_brain/data/SAM_AI_MASTER_SYSTEM_PROMPT_V2.md` (primary)
2. Fallback to database if file not found

**Power Prompts:**
Mode-specific prompts are appended from `sam.mode.context` table based on user's active mode.

**Environment Detection:**
- Local mode: File access, developer tools
- Production mode: Restricted access, security focus

**Branch System:**
New canvas types = new database records, NOT code changes.

---

## 🤝 Support & Contact

**Maintainer:** Anthony Gardiner
**AI Partner:** Claude (Anthropic)
**Project:** SAM AI - Intelligent Odoo Framework

For questions or contributions, refer to the main architecture document.

---

**Last Updated:** October 9, 2025
**Documentation Version:** 3.5.0
