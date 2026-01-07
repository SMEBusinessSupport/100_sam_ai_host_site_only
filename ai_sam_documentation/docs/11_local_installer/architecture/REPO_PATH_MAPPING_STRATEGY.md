# SAM AI Repository & Path Mapping Strategy

**Date:** 2025-11-06
**Purpose:** Map numeric paths (01-10) to GitHub repositories and tier levels

---

## The Problem

You have:
1. **Numeric paths** (01-10) - Stable, typo-proof folder structure
2. **GitHub repositories** - Need clear naming and organization
3. **Tier levels** - Free, Starter, Professional, Enterprise
4. **Special environments** - ChromaDB, Vector DB, Graph Memory (Apache AGE)

How do these all connect?

---

## Proposed Mapping System

### Path 01: Core Lightweight (Bundled in Installer)
**Repository:** `odoo-18-core-lightweight`
**Location:** `C:\odoo-lightweight\`
**GitHub URL:** `https://github.com/yourorg/odoo-18-core-lightweight.git`
**Visibility:** Public
**Contains:**
- Base Odoo 18 modules (mail, web, etc.)
- Lightweight modifications
- Essential dependencies
**Tier Access:** ALL (bundled in installer)
**Environment:** Standard Odoo

---

### Path 02: SAM AI Core (Free Tier)
**Repository:** `samai-core-free`
**Location:** `custom-addons/02/`
**GitHub URL:** `https://github.com/yourorg/samai-core-free.git`
**Visibility:** Public
**Contains:**
```
02/
├── ai_brain/              # Foundation data layer
├── ai_sam/                # Core SAM AI framework
├── ai_sam_intelligence/   # Agent registry
└── ai_sam_ui/             # Basic UI components
```
**Tier Access:** ALL (Free)
**Environment:** Standard Odoo
**Dependencies:** None (uses standard library only)

---

### Path 03: SAM AI Starter Pack (€97/month)
**Repository:** `samai-starter-tier`
**Location:** `custom-addons/03/`
**GitHub URL:** `https://github.com/yourorg/samai-starter-tier.git`
**Visibility:** Private
**Contains:**
```
03/
├── ai_sam_lead_generator/  # Lead generation & scraping
├── ai_sam_workflows/       # N8N workflow automation
├── ai_sam_qrcodes/         # QR code generation
└── github_app/             # GitHub integration
```
**Tier Access:** Starter, Professional, Enterprise
**Environment:** Standard Odoo
**Dependencies:**
- requests, beautifulsoup4, lxml (web scraping)
- GitPython (GitHub integration)
- Pillow, qrcode (QR codes)

---

### Path 04: SAM AI Professional Pack (€497/month)
**Repository:** `samai-professional-tier`
**Location:** `custom-addons/04/`
**GitHub URL:** `https://github.com/yourorg/samai-professional-tier.git`
**Visibility:** Private
**Contains:**
```
04/
├── ai_sam_creatives/       # Creative content generation
├── ai_sam_docs/            # Documentation intelligence
├── ai_sam_socializer/      # Social media management
├── ai_sam_messenger/       # Multi-channel messaging
└── ai_youtube_transcribe/  # YouTube transcript processing
```
**Tier Access:** Professional, Enterprise
**Environment:** Standard Odoo
**Dependencies:**
- openpyxl (Excel support)
- selenium, webdriver-manager (advanced scraping - optional)

---

### Path 05: SAM AI Enterprise Pack (€1147/month)
**Repository:** `samai-enterprise-tier`
**Location:** `custom-addons/05/`
**GitHub URL:** `https://github.com/yourorg/samai-enterprise-tier.git`
**Visibility:** Private
**Contains:**
```
05/
├── ai_sam_members/         # Team collaboration
├── ai_sam_claude_mcp/      # MCP server generation
├── odoo_cache_manager/     # Performance optimization
└── [custom modules]/       # Client-specific customizations
```
**Tier Access:** Enterprise only
**Environment:** Standard Odoo
**Dependencies:**
- None additional (all covered in lower tiers)

---

### Path 06: Memory System - ChromaDB (OPTIONAL Add-on)
**Repository:** `samai-memory-chromadb`
**Location:** `custom-addons/06/`
**GitHub URL:** `https://github.com/yourorg/samai-memory-chromadb.git`
**Visibility:** Private
**Contains:**
```
06/
├── ai_sam_memory/          # Memory system module
└── docker-compose.yml      # ChromaDB container config
```
**Tier Access:** Professional, Enterprise (paid add-on €49/month)
**Environment:** **Docker Required** (ChromaDB container)
**Dependencies:**
- chromadb (Python library)
- Docker Desktop (for ChromaDB server)
- sentence-transformers (ML models ~1.5GB)

**Installation:**
```bash
# Docker setup
docker run -d -p 8000:8000 \
  -v chroma-data:/chroma/chroma \
  chromadb/chroma:latest

# Python deps
pip install chromadb sentence-transformers
```

---

### Path 07: Vector Database - Qdrant/Weaviate (OPTIONAL Add-on)
**Repository:** `samai-vector-store`
**Location:** `custom-addons/07/`
**GitHub URL:** `https://github.com/yourorg/samai-vector-store.git`
**Visibility:** Private
**Contains:**
```
07/
├── ai_sam_vector_search/   # Vector search module
└── docker-compose.yml      # Vector DB container
```
**Tier Access:** Enterprise only (paid add-on €79/month)
**Environment:** **Docker Required** (Qdrant/Weaviate container)
**Dependencies:**
- qdrant-client OR weaviate-client
- Docker Desktop

**Alternative Vector Stores:**
```yaml
# Qdrant (Rust-based, fast)
docker run -p 6333:6333 qdrant/qdrant

# Weaviate (GraphQL API)
docker run -p 8080:8080 semitechnologies/weaviate
```

---

### Path 08: Graph Memory - Apache AGE (OPTIONAL Add-on)
**Repository:** `samai-graph-memory`
**Location:** `custom-addons/08/`
**GitHub URL:** `https://github.com/yourorg/samai-graph-memory.git`
**Visibility:** Private
**Contains:**
```
08/
├── ai_sam_graph_memory/    # Graph database integration
├── migrations/             # Apache AGE schema
└── docker-compose.yml      # PostgreSQL + AGE extension
```
**Tier Access:** Enterprise only (paid add-on €99/month)
**Environment:** **Docker Required** (PostgreSQL + Apache AGE extension)
**Dependencies:**
- psycopg2 (already included)
- age-graph library
- Docker Desktop

**Installation:**
```yaml
# docker-compose.yml
services:
  postgres-age:
    image: apache/age
    ports:
      - "5433:5432"
    environment:
      POSTGRES_DB: graph_db
      POSTGRES_USER: odoo
      POSTGRES_PASSWORD: SamAI2025
    volumes:
      - age-data:/var/lib/postgresql/data
```

---

### Path 09-10: Reserved for Future Expansion
**Repository:** TBD
**Location:** `custom-addons/09/` and `custom-addons/10/`
**Purpose:** Future products, industry verticals, partner integrations

**Potential Uses:**
- **Path 09:** Industry-specific modules (Healthcare, Manufacturing, etc.)
- **Path 10:** Partner ecosystem (3rd-party integrations)

---

## Repository Creation Checklist

### Step 1: Create GitHub Repositories

```bash
# Create all repos at once (using GitHub CLI)
gh repo create yourorg/odoo-18-core-lightweight --public
gh repo create yourorg/samai-core-free --public
gh repo create yourorg/samai-starter-tier --private
gh repo create yourorg/samai-professional-tier --private
gh repo create yourorg/samai-enterprise-tier --private
gh repo create yourorg/samai-memory-chromadb --private
gh repo create yourorg/samai-vector-store --private
gh repo create yourorg/samai-graph-memory --private
```

**Or via Web UI:**
1. Go to https://github.com/new
2. Create each repo with descriptions below

---

### Step 2: Repository Descriptions

**odoo-18-core-lightweight**
> Lightweight Odoo 18 core - Essential modules for SAM AI platform

**samai-core-free**
> SAM AI Core Framework (Free Tier) - Intelligence, Agent Registry, Basic UI

**samai-starter-tier**
> SAM AI Starter Pack (€97/month) - Lead Generation, Workflows, QR Codes, GitHub Integration

**samai-professional-tier**
> SAM AI Professional Pack (€497/month) - Creatives, Docs, Social Media, Messaging, YouTube

**samai-enterprise-tier**
> SAM AI Enterprise Pack (€1147/month) - Team Collaboration, MCP Servers, Cache Management, Custom Modules

**samai-memory-chromadb**
> SAM AI Memory System (Add-on €49/month) - ChromaDB Vector Database Integration

**samai-vector-store**
> SAM AI Vector Search (Add-on €79/month) - Qdrant/Weaviate Integration

**samai-graph-memory**
> SAM AI Graph Memory (Add-on €99/month) - Apache AGE Knowledge Graph

---

## Module Organization Script

### Organize Existing Modules into Paths

```powershell
# organize_modules.ps1
$BasePath = "C:\Working With AI\ai_sam\ai_sam"
$TargetBase = "D:\Odoo-18-SaaS\modules"

# Path 02: Core (Free)
$Path02 = @('ai_brain', 'ai_sam', 'ai_sam_intelligence', 'ai_sam_ui')
foreach ($module in $Path02) {
    Copy-Item "$BasePath\$module" -Destination "$TargetBase\02\" -Recurse -Force
}

# Path 03: Starter
$Path03 = @('ai_sam_lead_generator', 'ai_sam_workflows', 'ai_sam_qrcodes', 'github_app')
foreach ($module in $Path03) {
    Copy-Item "$BasePath\$module" -Destination "$TargetBase\03\" -Recurse -Force
}

# Path 04: Professional
$Path04 = @('ai_sam_creatives', 'ai_sam_docs', 'ai_sam_socializer', 'ai_sam_messenger', 'ai_youtube_transcribe')
foreach ($module in $Path04) {
    Copy-Item "$BasePath\$module" -Destination "$TargetBase\04\" -Recurse -Force
}

# Path 05: Enterprise
$Path05 = @('ai_sam_members', 'ai_sam_claude_mcp', 'odoo_cache_manager')
foreach ($module in $Path05) {
    Copy-Item "$BasePath\$module" -Destination "$TargetBase\05\" -Recurse -Force
}

# Path 06: Memory System
$Path06 = @('ai_sam_memory')
foreach ($module in $Path06) {
    if (Test-Path "$BasePath\$module") {
        Copy-Item "$BasePath\$module" -Destination "$TargetBase\06\" -Recurse -Force
    }
}

Write-Host "Modules organized into tier-based paths!" -ForegroundColor Green
```

---

## Configuration Mapping Table

### odoo.conf Path Configuration by Tier

**Free Tier:**
```ini
addons_path = /opt/odoo/addons,
              /opt/odoo/custom-addons/01,
              /opt/odoo/custom-addons/02
```

**Starter Tier (€97/month):**
```ini
addons_path = /opt/odoo/addons,
              /opt/odoo/custom-addons/01,
              /opt/odoo/custom-addons/02,
              /opt/odoo/custom-addons/03
```

**Professional Tier (€497/month):**
```ini
addons_path = /opt/odoo/addons,
              /opt/odoo/custom-addons/01,
              /opt/odoo/custom-addons/02,
              /opt/odoo/custom-addons/03,
              /opt/odoo/custom-addons/04
```

**Enterprise Tier (€1147/month):**
```ini
addons_path = /opt/odoo/addons,
              /opt/odoo/custom-addons/01,
              /opt/odoo/custom-addons/02,
              /opt/odoo/custom-addons/03,
              /opt/odoo/custom-addons/04,
              /opt/odoo/custom-addons/05
```

**Enterprise + Memory System:**
```ini
addons_path = /opt/odoo/addons,
              /opt/odoo/custom-addons/01,
              /opt/odoo/custom-addons/02,
              /opt/odoo/custom-addons/03,
              /opt/odoo/custom-addons/04,
              /opt/odoo/custom-addons/05,
              /opt/odoo/custom-addons/06
```

**Enterprise + All Add-ons:**
```ini
addons_path = /opt/odoo/addons,
              /opt/odoo/custom-addons/01,
              /opt/odoo/custom-addons/02,
              /opt/odoo/custom-addons/03,
              /opt/odoo/custom-addons/04,
              /opt/odoo/custom-addons/05,
              /opt/odoo/custom-addons/06,
              /opt/odoo/custom-addons/07,
              /opt/odoo/custom-addons/08
```

---

## Database Registry (Odoo Model)

### Create Mapping Table in Odoo

```python
# models/saas_addon_path.py
class SaasAddonPath(models.Model):
    _name = 'saas.addon.path'
    _description = 'SAM AI Addon Path Registry'
    _order = 'path_id'

    path_id = fields.Integer(string='Path ID', required=True)
    path_number = fields.Char(string='Path', compute='_compute_path_number', store=True)

    # Repository Info
    name = fields.Char(string='Display Name', required=True)
    description = fields.Text(string='Description')
    github_repo = fields.Char(string='GitHub Repository')
    github_branch = fields.Char(string='Branch', default='main')
    is_public = fields.Boolean(string='Public Repository', default=False)

    # Access Control
    tier_ids = fields.Many2many('saas.membership.tier', string='Available to Tiers')
    requires_docker = fields.Boolean(string='Requires Docker', default=False)
    docker_compose_url = fields.Char(string='Docker Compose URL')

    # Environment
    environment_type = fields.Selection([
        ('standard', 'Standard Odoo'),
        ('chromadb', 'ChromaDB Vector Store'),
        ('vector', 'Vector Database (Qdrant/Weaviate)'),
        ('graph', 'Graph Database (Apache AGE)'),
    ], default='standard')

    # Status
    active = fields.Boolean(string='Active', default=True)
    is_bundled = fields.Boolean(string='Bundled in Installer', default=False)

    @api.depends('path_id')
    def _compute_path_number(self):
        for record in self:
            record.path_number = str(record.path_id).zfill(2)
```

### Seed Data

```xml
<odoo>
    <data noupdate="1">
        <!-- Path 01: Core Lightweight -->
        <record id="path_01_core" model="saas.addon.path">
            <field name="path_id">1</field>
            <field name="name">Core Lightweight</field>
            <field name="description">Base Odoo 18 lightweight modules</field>
            <field name="github_repo">https://github.com/yourorg/odoo-18-core-lightweight.git</field>
            <field name="is_public" eval="True"/>
            <field name="is_bundled" eval="True"/>
            <field name="environment_type">standard</field>
        </record>

        <!-- Path 02: SAM AI Core -->
        <record id="path_02_core_free" model="saas.addon.path">
            <field name="path_id">2</field>
            <field name="name">SAM AI Core (Free)</field>
            <field name="description">ai_brain, ai_sam, ai_sam_intelligence, ai_sam_ui</field>
            <field name="github_repo">https://github.com/yourorg/samai-core-free.git</field>
            <field name="is_public" eval="True"/>
            <field name="environment_type">standard</field>
        </record>

        <!-- Path 03: Starter Pack -->
        <record id="path_03_starter" model="saas.addon.path">
            <field name="path_id">3</field>
            <field name="name">Starter Pack (€97/month)</field>
            <field name="description">Lead Generation, Workflows, QR Codes, GitHub</field>
            <field name="github_repo">https://github.com/yourorg/samai-starter-tier.git</field>
            <field name="is_public" eval="False"/>
            <field name="environment_type">standard</field>
        </record>

        <!-- Path 06: Memory System -->
        <record id="path_06_memory" model="saas.addon.path">
            <field name="path_id">6</field>
            <field name="name">Memory System (€49/month add-on)</field>
            <field name="description">ChromaDB Vector Database Integration</field>
            <field name="github_repo">https://github.com/yourorg/samai-memory-chromadb.git</field>
            <field name="is_public" eval="False"/>
            <field name="requires_docker" eval="True"/>
            <field name="docker_compose_url">https://raw.githubusercontent.com/yourorg/samai-memory-chromadb/main/docker-compose.yml</field>
            <field name="environment_type">chromadb</field>
        </record>

        <!-- Path 08: Graph Memory -->
        <record id="path_08_graph" model="saas.addon.path">
            <field name="path_id">8</field>
            <field name="name">Graph Memory (€99/month add-on)</field>
            <field name="description">Apache AGE Knowledge Graph</field>
            <field name="github_repo">https://github.com/yourorg/samai-graph-memory.git</field>
            <field name="is_public" eval="False"/>
            <field name="requires_docker" eval="True"/>
            <field name="docker_compose_url">https://raw.githubusercontent.com/yourorg/samai-graph-memory/main/docker-compose.yml</field>
            <field name="environment_type">graph</field>
        </record>
    </data>
</odoo>
```

---

## Summary

**Path-to-Repo-to-Tier Mapping:**

| Path | GitHub Repo | Tier | Environment | Docker? |
|------|-------------|------|-------------|---------|
| 01 | odoo-18-core-lightweight | ALL (bundled) | Standard | No |
| 02 | samai-core-free | ALL (free) | Standard | No |
| 03 | samai-starter-tier | €97+ | Standard | No |
| 04 | samai-professional-tier | €497+ | Standard | No |
| 05 | samai-enterprise-tier | €1147 | Standard | No |
| 06 | samai-memory-chromadb | Add-on €49 | ChromaDB | Yes |
| 07 | samai-vector-store | Add-on €79 | Vector DB | Yes |
| 08 | samai-graph-memory | Add-on €99 | Graph DB | Yes |
| 09-10 | Reserved | Future | TBD | TBD |

**Next Steps:**
1. Create the 8 GitHub repositories
2. Run the module organization script
3. Push modules to respective repos
4. Generate access tokens for private repos
5. Test the provisioning system

Ready to create the repositories?
