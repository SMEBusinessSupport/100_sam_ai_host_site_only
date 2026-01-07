# Custom Addons Structure for SAM AI Installer

## Overview

The installer is configured to load custom modules from **3 separate GitHub repositories**, each serving a different purpose.

---

## Folder Structure (After Installation)

```
C:\Program Files\Odoo Lightweight\odoo\
├── server\                    (Odoo core - from C:\odoo-lightweight)
│   ├── odoo\
│   ├── addons\               (Built-in Odoo modules)
│   └── odoo-bin
│
└── custom-addons\            (Custom modules from GitHub)
    ├── odoo-lightweight\      Repo 1: Core lightweight modules
    ├── odoo-18-addons\        Repo 2: Standard custom modules
    └── ai_sam\                Repo 3: SAM AI intelligence modules
```

---

## Repository Details

### Repo 1: odoo-lightweight
**Purpose:** Essential lightweight modules (stripped-down Odoo core)

**GitHub URL:** `https://github.com/yourorg/odoo-18-core-lightweight`

**What Goes Here:**
- Minimal required modules
- Core business logic
- Base customizations
- **NO** heavy modules (accounting, manufacturing, etc.)

**Example Modules:**
```
odoo-lightweight/
├── web_lightweight/
├── portal_minimal/
├── crm_simple/
└── contacts_essential/
```

---

### Repo 2: odoo-18-addons
**Purpose:** Standard Odoo custom modules (OCA-style)

**GitHub URL:** `https://github.com/yourorg/odoo-18-custom-addons`

**What Goes Here:**
- Custom business modules
- Industry-specific customizations
- Third-party modules
- Optional enhancements

**Example Modules:**
```
odoo-18-addons/
├── custom_invoicing/
├── project_management_enhanced/
├── sales_automation/
└── custom_reports/
```

---

### Repo 3: ai_sam
**Purpose:** SAM AI intelligence & automation modules

**GitHub URL:** `https://github.com/yourorg/ai_sam`

**What Goes Here:**
- SAM AI chat interface
- Intelligence modules
- Workflow automation
- Lead generation
- Scraping tools

**Current Structure (from your existing repo):**
```
ai_sam/
├── ai_sam_intelligence/      (Agent registry, docs intelligence)
├── ai_sam_lead_generator/    (Web scraping, ScraperAPI)
├── ai_sam_workflows/         (N8N workflow automation)
└── ai_sam_desktop/           (SAM AI launcher)
```

**Location:** `C:\Working With AI\ai_sam\ai_sam`

---

## How the Installer Handles These

### During Installation

The installer **currently** bundles `C:\odoo-lightweight` (baked into the .exe).

**We need to add post-install steps to clone the GitHub repos:**

### Option A: Clone During Installation (Recommended)
The installer runs git clone commands during setup:

```batch
git clone https://github.com/yourorg/odoo-18-core-lightweight.git "%INSTALL_DIR%\odoo\custom-addons\odoo-lightweight"
git clone https://github.com/yourorg/odoo-18-custom-addons.git "%INSTALL_DIR%\odoo\custom-addons\odoo-18-addons"
git clone https://github.com/yourorg/ai_sam.git "%INSTALL_DIR%\odoo\custom-addons\ai_sam"
```

**Pros:** Always gets latest modules from GitHub
**Cons:** Requires internet + git installed

### Option B: Bundle in Installer (Current Approach)
Include all modules in the installer .exe (like `C:\odoo-lightweight`).

**Pros:** Works offline, no git needed
**Cons:** Installer gets larger, modules are static (not auto-updated)

### Option C: Hybrid (Best of Both)
- Bundle `odoo-lightweight` (essential, rarely changes)
- Clone `odoo-18-addons` and `ai_sam` during install (frequently updated)

---

## Odoo Configuration (odoo.conf)

The `addons_path` in `odoo.conf` is set to:

```ini
addons_path = C:\Program Files\Odoo Lightweight\odoo\server\odoo\addons,
              C:\Program Files\Odoo Lightweight\odoo\custom-addons\odoo-lightweight,
              C:\Program Files\Odoo Lightweight\odoo\custom-addons\odoo-18-addons,
              C:\Program Files\Odoo Lightweight\odoo\custom-addons\ai_sam
```

**Order matters!** Odoo searches paths left-to-right.

---

## Your Current Repositories

Based on your existing work, here's what you have:

### 1. odoo-lightweight
**Location:** `C:\odoo-lightweight`
**Status:** ✓ EXISTS
**GitHub:** Not created yet (you mentioned wanting to push to GitHub)

### 2. odoo-18-addons
**Location:** `C:\odoo-18-addons`
**Status:** ✓ EXISTS (you mentioned this)
**GitHub:** Not created yet

### 3. ai_sam
**Location:** `C:\Working With AI\ai_sam\ai_sam`
**Status:** ✓ EXISTS
**GitHub:** Already a repo (needs to be cloned during install)

---

## What You Need to Do

### Before Building the Installer:

1. **Push odoo-lightweight to GitHub:**
   ```bash
   cd C:\odoo-lightweight
   git init
   git add .
   git commit -m "Initial commit: Odoo 18 lightweight core"
   git remote add origin https://github.com/yourorg/odoo-18-core-lightweight
   git push -u origin main
   ```

2. **Push odoo-18-addons to GitHub:**
   ```bash
   cd C:\odoo-18-addons
   git init
   git add .
   git commit -m "Initial commit: Custom Odoo 18 addons"
   git remote add origin https://github.com/yourorg/odoo-18-custom-addons
   git push -u origin main
   ```

3. **ai_sam is already a repo** (just verify URL)

---

## Updated Installer Approach

I recommend **Option C (Hybrid)**:

### What gets bundled in the installer (.exe):
- Python 3.10 embedded
- PostgreSQL 15 binaries
- Odoo core (from `C:\odoo-lightweight\server`)
- **odoo-lightweight modules** (essential, bundled)

### What gets cloned during installation:
- `odoo-18-addons` (git clone)
- `ai_sam` (git clone)

### Why?
- Installer stays reasonable size (~350MB)
- Users get latest AI modules from GitHub
- Offline install still works (just missing optional addons)

---

## Next Steps

1. **Decide:** Bundle everything OR clone from GitHub?
2. **Create GitHub repos** for odoo-lightweight and odoo-18-addons
3. **Update installer script** to clone repos (if using Option C)
4. **Test** that all 3 addon paths work

**Want me to create the updated installer script that clones the GitHub repos?**
