# SAM AI Lightweight Installer - Final Configuration

**Date:** 2025-11-07
**Status:** Ready for Testing

---

## Summary: What We've Built

A fully automated Windows installer that:
- Eliminates "Create Database" prompts (auto-complete setup)
- Uses numeric addon paths (01-10) for future-proof flexibility
- Includes all required dependencies by default
- Offers optional components (Memory System, QR codes, Excel, Advanced Scraping)
- Maps to 8 GitHub repositories for tier-based access control

---

## Installation Types

### Standard Installation (~100MB)
**Includes:**
- Odoo 18 Core
- Python 3.10 Embedded
- PostgreSQL 15 Portable
- SAM AI Core (free tier)
- Basic dependencies (anthropic, openai, requests, psycopg2)
- Web scraping (beautifulsoup4, lxml)
- Git integration (GitPython)
- QR codes (Pillow, qrcode)
- Excel support (openpyxl)

**User experience:**
1. Install → 5 minutes
2. Click "Start Odoo" shortcut
3. Login: admin / SamAI
4. Ready to use

### Full Installation (~2.2GB)
**Everything in Standard PLUS:**
- Memory System (ChromaDB + sentence-transformers)
- Advanced Web Scraping (Selenium + webdriver-manager)

**User experience:**
- Installation: 15-20 minutes (downloads ML models)
- Full AI memory and semantic search
- JavaScript-heavy website scraping

---

## Numeric Path Architecture

### Why Numeric Paths?

**Problem with named folders:**
```
custom-addons/
├── samai-core/              # What if we rename the tier?
├── samai-starter/           # What if user typos "stater"?
└── samai-professional/      # Long, complex names
```

**Solution with numeric paths:**
```
custom-addons/
├── 01/  (odoo-18-core-lightweight)
├── 02/  (samai-core-free)
├── 03/  (samai-starter-tier)
├── 04/  (samai-professional-tier)
├── 05/  (samai-enterprise-tier)
├── 06/  (samai-memory-chromadb)
├── 07/  (samai-vector-store)
├── 08/  (samai-graph-memory)
├── 09/  (reserved)
└── 10/  (reserved)
```

**Benefits:**
- Paths never change (stable configs)
- No typo risk
- Easy automation (loop through 01-10)
- Rename tiers without breaking anything
- Database-managed labels

### Path-to-Tier Mapping

| Path | Repository | Tier | Price | Requires Docker? |
|------|-----------|------|-------|-----------------|
| 01 | odoo-18-core-lightweight | Bundled | Free | No |
| 02 | samai-core-free | Free | €0/month | No |
| 03 | samai-starter-tier | Starter | €97/month | No |
| 04 | samai-professional-tier | Professional | €497/month | No |
| 05 | samai-enterprise-tier | Enterprise | €1147/month | No |
| 06 | samai-memory-chromadb | Memory Add-on | €49/month | ❌ NO |
| 07 | samai-vector-store | Vector Add-on | €79/month | Optional |
| 08 | samai-graph-memory | Graph Add-on | €99/month | ✅ YES |
| 09 | *reserved* | Future | - | - |
| 10 | *reserved* | Future | - | - |

---

## Python Dependencies - Complete Matrix

### CRITICAL (Always Installed)
```python
anthropic>=0.18.0       # Claude AI API
openai>=1.0.0           # OpenAI API
requests>=2.28.0        # HTTP requests
psycopg2-binary>=2.9.0  # PostgreSQL adapter
```

### IMPORTANT (Always Installed)
```python
beautifulsoup4>=4.11.0  # Web scraping (ai_sam_lead_generator)
lxml>=4.9.0             # XML parser (web scraping)
GitPython>=3.1.0        # Git integration (github_app)
```

### RECOMMENDED (User Choice - Default: Yes)
```python
Pillow>=9.0.0           # Image processing (ai_sam_qrcodes, ai_sam_creatives)
qrcode>=7.3.0           # QR code generation (ai_sam_qrcodes)
openpyxl>=3.0.0         # Excel support (various modules)
```

### OPTIONAL - Advanced Scraping (User Choice - Default: No)
```python
selenium>=4.0.0         # Headless browser automation
webdriver-manager>=3.8.0  # Chrome driver management
```

### OPTIONAL - Memory System (User Choice - Default: Full only)
```python
chromadb>=0.4.0                  # Vector database (~500MB)
sentence-transformers>=2.2.0     # ML embeddings (~1.5GB)
```

### NOT INCLUDED (Docker Required - Enterprise Only)
```python
# Apache AGE graph database requires Docker container
# Separate PostgreSQL instance on port 5455
# Only for samai-graph-memory add-on
```

---

## Auto-Complete Configuration

### Problem
Users get confused at "Create Database" screen:
- What database name?
- What username/password?
- What settings?

### Solution
Pre-configure everything during installation:

**Default Configuration:**
```ini
db_name = samai_production
db_user = odoo
db_password = SamAI2025
admin_passwd = SamAI

# Admin login credentials:
Username: admin
Password: SamAI
```

**Installation Process:**
1. Install PostgreSQL → Create user `odoo`
2. Create database `samai_production`
3. Initialize Odoo with base modules
4. Create admin user (username: `admin`, password: `SamAI`)
5. Stop services
6. User clicks "Start Odoo" → Goes straight to login screen

**Result:** Zero configuration needed by end user

---

## Module Organization by Tier

### Path 02: Core Free (Public)
**Modules:**
- `ai_brain` - Foundation data layer
- `ai_sam` - Core framework
- `ai_sam_intelligence` - Agent registry
- `ai_sam_ui` - User interface

**Dependencies:** anthropic, openai, requests
**Size:** ~2MB
**GitHub:** `samai-core-free` (public)

### Path 03: Starter Tier (€97/month)
**Modules:**
- `ai_sam_lead_generator` - Lead generation & web scraping
- `ai_sam_workflows` - N8N workflow automation
- `ai_sam_qrcodes` - QR code generation
- `github_app` - GitHub integration

**Dependencies:** beautifulsoup4, lxml, GitPython, Pillow, qrcode
**Size:** ~5MB
**GitHub:** `samai-starter-tier` (private)

### Path 04: Professional Tier (€497/month)
**Modules:**
- `ai_sam_creatives` - Creative studio
- `ai_sam_docs` - Documentation generator
- `ai_sam_socializer` - Social media management
- `ai_sam_messenger` - Messaging integration
- `ai_youtube_transcribe` - YouTube transcription

**Dependencies:** openpyxl
**Size:** ~8MB
**GitHub:** `samai-professional-tier` (private)

### Path 05: Enterprise Tier (€1147/month)
**Modules:**
- `ai_sam_members` - Team collaboration
- `ai_sam_claude_mcp` - MCP server generation
- `odoo_cache_manager` - Cache optimization

**Dependencies:** None additional
**Size:** ~3MB
**GitHub:** `samai-enterprise-tier` (private)

### Path 06: Memory Add-on (€49/month)
**Modules:**
- Memory system (merged into `ai_sam`, activated via config)

**Dependencies:** chromadb, sentence-transformers
**Size:** ~2GB (ML models)
**Docker Required:** ❌ NO (runs locally)
**GitHub:** `samai-memory-chromadb` (private)

### Path 08: Graph Memory Add-on (€99/month)
**Modules:**
- Graph visualization (merged into `ai_sam`, activated via config)

**Dependencies:** psycopg2 (already included), age-graph
**Docker Required:** ✅ YES (Apache AGE container)
**GitHub:** `samai-graph-memory` (private)

---

## Installer Components Configuration

### Inno Setup Components Section
```ini
[Components]
Name: "core"; Description: "Odoo Core (required)"; Types: full standard custom; Flags: fixed
Name: "postgresql"; Description: "PostgreSQL Database (required)"; Types: full standard custom; Flags: fixed
Name: "python"; Description: "Python Runtime (required)"; Types: full standard custom; Flags: fixed

; Recommended (checked by default in standard and full)
Name: "qrcodes"; Description: "QR Code & Image Processing - 5MB (recommended)"; Types: full standard custom
Name: "excel"; Description: "Excel File Support - 10MB (recommended)"; Types: full standard custom

; Optional (only in full by default)
Name: "scraping"; Description: "Advanced Web Scraping (Selenium) - 50MB (optional)"; Types: full
Name: "memory"; Description: "Memory System (ChromaDB + Embeddings - 2GB download)"; Types: full
```

### Component Selection Guide

**Standard Installation (Recommended):**
- ✅ Core (required)
- ✅ PostgreSQL (required)
- ✅ Python (required)
- ✅ QR Codes (checked by default)
- ✅ Excel (checked by default)
- ☐ Advanced Scraping (unchecked)
- ☐ Memory System (unchecked)

**Full Installation:**
- ✅ Everything checked

**Custom Installation:**
- User chooses individual components

---

## GitHub Repository Strategy

### Repository Structure

```
GitHub Organization: your-org/

PUBLIC REPOS:
├── odoo-18-core-lightweight      (Path 01 - bundled in installer)
└── samai-core-free              (Path 02 - free tier)

PRIVATE REPOS:
├── samai-starter-tier           (Path 03 - €97/month)
├── samai-professional-tier      (Path 04 - €497/month)
├── samai-enterprise-tier        (Path 05 - €1147/month)
├── samai-memory-chromadb        (Path 06 - €49/month add-on, NO Docker)
├── samai-vector-store           (Path 07 - €79/month add-on, Docker optional)
└── samai-graph-memory           (Path 08 - €99/month add-on, Docker required)
```

### Access Control Strategy

**Installation Process:**
1. User installs from public installer (includes Path 01, 02)
2. User subscribes to tier (Starter/Professional/Enterprise)
3. System generates GitHub personal access token (PAT) for their tier
4. Token has read access ONLY to their subscribed tier repos
5. Odoo config stores encrypted token
6. Module updater pulls from authorized repos

**Token Scope Matrix:**
| Subscription | Path 02 | Path 03 | Path 04 | Path 05 | Path 06 | Path 07 | Path 08 |
|--------------|---------|---------|---------|---------|---------|---------|---------|
| Free | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Starter (€97) | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Professional (€497) | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| Enterprise (€1147) | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ |
| + Memory Add-on (€49) | - | - | - | - | ✅ | ❌ | ❌ |
| + Graph Add-on (€99) | - | - | - | - | - | - | ✅ |

---

## Installation Phases (Complete Flow)

### Phase 1-2: Python Setup
1. Ensure pip installed
2. Upgrade pip to latest

### Phase 3: Critical Dependencies (Always)
```bash
pip install anthropic>=0.18.0
pip install openai>=1.0.0
pip install requests>=2.28.0
```

### Phase 4: Important Dependencies (Always)
```bash
pip install psycopg2-binary>=2.9.0
```

### Phase 5: Memory System (Optional - Component: memory)
```bash
pip install chromadb>=0.4.0
pip install sentence-transformers>=2.2.0  # ~1.5GB download
```

### Phase 6: Web Scraping (Always)
```bash
pip install beautifulsoup4>=4.11.0 lxml>=4.9.0
```

### Phase 7: Git Integration (Always)
```bash
pip install GitPython>=3.1.0
```

### Phase 7.5: QR Codes (Optional - Component: qrcodes)
```bash
pip install Pillow>=9.0.0 qrcode>=7.3.0
```

### Phase 7.6: Excel Support (Optional - Component: excel)
```bash
pip install openpyxl>=3.0.0
```

### Phase 7.7: Advanced Scraping (Optional - Component: scraping)
```bash
pip install selenium>=4.0.0 webdriver-manager>=3.8.0
```

### Phase 8-11: PostgreSQL Setup
8. Initialize PostgreSQL data directory
9. Start PostgreSQL temporarily
10. Create `odoo` database user
11. Stop PostgreSQL

### Phase 12-14: Odoo Configuration
12. Create numeric addon paths (01-10)
13. Create `odoo.conf` with auto-complete settings
14. Run auto-complete setup (create DB + admin user)

### Phase 15-16: Post-Install (Optional)
15. Start Odoo service (if selected)
16. Open browser to http://localhost:8069

---

## Testing Checklist

### Pre-Build Tests
- [ ] All bundled components exist:
  - [ ] `bundled\python-3.10-embed\python.exe`
  - [ ] `bundled\postgresql-15\bin\postgres.exe`
  - [ ] `C:\odoo-lightweight\` (Odoo core)
- [ ] All scripts exist in `scripts\` folder
- [ ] Inno Setup 6 installed

### Build Tests
- [ ] Installer compiles without errors
- [ ] Output file size reasonable (~150MB base, ~2.5GB with memory)
- [ ] All files included in installer

### Installation Tests (Standard)
- [ ] Installs without errors (5-10 minutes)
- [ ] PostgreSQL initializes successfully
- [ ] Database `samai_production` created
- [ ] Admin user created (username: `admin`, password: `SamAI`)
- [ ] Numeric paths created (01-10)
- [ ] `odoo.conf` created with correct settings
- [ ] Desktop shortcut created
- [ ] Odoo starts successfully
- [ ] Login works (admin / SamAI)
- [ ] SAM AI chat accessible

### Installation Tests (Full)
- [ ] Memory system components install (~15 minutes)
- [ ] ChromaDB imports successfully: `python -c "import chromadb"`
- [ ] Sentence transformers import: `python -c "import sentence_transformers"`
- [ ] Memory features accessible in SAM AI

### Dependency Validation Tests
```bash
# Run from installed Python
cd "C:\Program Files\Odoo Lightweight\python"

# Critical deps
python -c "import anthropic; print('✅ anthropic')"
python -c "import openai; print('✅ openai')"
python -c "import requests; print('✅ requests')"
python -c "import psycopg2; print('✅ psycopg2')"

# Important deps
python -c "import bs4; print('✅ beautifulsoup4')"
python -c "import lxml; print('✅ lxml')"
python -c "import git; print('✅ GitPython')"

# Recommended deps (if components selected)
python -c "import PIL; print('✅ Pillow')"
python -c "import qrcode; print('✅ qrcode')"
python -c "import openpyxl; print('✅ openpyxl')"

# Optional deps (if components selected)
python -c "import selenium; print('✅ selenium')"
python -c "import chromadb; print('✅ chromadb')"
```

### Module Tests (After organizing)
- [ ] Path 02 modules load successfully
- [ ] No missing Python dependency errors
- [ ] QR code generation works (if component selected)
- [ ] Lead generator scraping works
- [ ] Workflow automation accessible

---

## Next Steps

### 1. Organize Existing Modules
```powershell
cd C:\Users\total\installer
powershell -ExecutionPolicy Bypass -File organize_sam_modules.ps1
```

This will:
- Create directory structure in `D:\Odoo-18-SaaS\modules\`
- Copy modules from `C:\Working With AI\ai_sam\ai_sam\` to tier paths
- Generate README files for each tier

### 2. Create GitHub Repositories
Create 8 repositories with appropriate access:
- 2 public (odoo-18-core-lightweight, samai-core-free)
- 6 private (tier repos + add-on repos)

### 3. Push Modules to GitHub
For each tier path (02-08):
```bash
cd D:\Odoo-18-SaaS\modules\02
git init
git add .
git commit -m "Initial commit - SAM AI Core Free"
git remote add origin https://github.com/your-org/samai-core-free.git
git push -u origin main
```

### 4. Fix Installer Build Error
Current issue: Exit code 2 during compilation
Likely cause: PostgreSQL pgAdmin files

**Solution options:**
- Option A: Exclude pgAdmin from PostgreSQL bundle
- Option B: Use PostgreSQL portable without GUI tools
- Option C: Handle large file count in Inno Setup script

### 5. Test Installation on Clean Machine
- Windows 10/11 VM
- No Python/PostgreSQL pre-installed
- Test all installation types (Standard, Full, Custom)

### 6. Deploy to SaaS Platform (Webkul)
- Configure tier-based module provisioning
- Integrate GitHub token management
- Set up Docker containers for graph memory (optional)

---

## Key Takeaways

### What We Got Right
1. **Auto-complete setup** - Eliminates user confusion
2. **Numeric paths** - Future-proof, typo-proof architecture
3. **Component-based install** - User choice for heavy dependencies
4. **ChromaDB = No Docker** - Simpler than initially thought
5. **Dependency analysis** - Complete picture of requirements

### What's Optional (Not Scary!)
1. **Memory System (ChromaDB)** - Just a big pip install, no Docker
2. **QR Codes, Excel** - Lightweight, high utility
3. **Advanced Scraping** - Only for JavaScript-heavy sites
4. **Graph Memory** - Enterprise only, Docker required (but optional)

### What's Critical
1. **Pillow + qrcode** - MUST add to installer (ai_sam_qrcodes breaks without it)
2. **Database mapping model** - Need `saas.addon.path` model for tier management
3. **GitHub access control** - Token-based repo access per tier
4. **Testing on clean machine** - Validate zero-config installation

---

**Documentation Date:** 2025-11-07
**Installer Version:** 18.0
**Ready for:** Module organization → Repo creation → Testing
