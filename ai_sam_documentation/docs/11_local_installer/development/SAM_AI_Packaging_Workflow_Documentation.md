# SAM AI Packaging & Installer Architecture Documentation

## 🎯 Overview

SAM AI uses a **hybrid installer architecture** that combines:
1. **Lightweight placeholder modules** (641 modules) - minimal footprint
2. **Full core modules** (15 modules) - pre-installed essentials
3. **On-demand GitHub installation** - download full modules when needed

---

## 📦 Key Components

###  1. Module Registry (`module_registry.json`)

**Location:** `D:\SAMAI-18-SaaS\github-repos\01-samai-odoo-18-lightweight-core\module_registry.json`

**Purpose:** Central catalog of all available Odoo modules with metadata

**Structure:**
```json
{
  "module_technical_name": {
    "name": "Human Readable Name",
    "version": "18.0.1.0",
    "summary": "Short description",
    "description": "Full description",
    "author": "Author name",
    "category": "Category/Subcategory",
    "depends": ["dep1", "dep2"],
    "installable": true,
    "application": false,
    "auto_install": false,
    "license": "LGPL-3",
    "source_repo": "github-repo-name",
    "is_placeholder": true
  }
}
```

**Key Fields:**
- `is_placeholder`: `true` = lightweight card, `false` = full module
- `source_repo`: GitHub repository name for on-demand installation
- `depends`: List of module dependencies

---

### 2. GitHub Module Installer (Odoo Module)

**Location:** `C:\Program Files\SAM AI\addons\sam-core\ai_sam_github_installer\`

**Files:**
- `models/github_module_installer.py` - Core installer logic
- `views/module_installer_views.xml` - UI for browsing/installing modules
- `__manifest__.py` - Module metadata

**Key Functions:**

#### `sync_from_registry()`
**Purpose:** Load module catalog from `module_registry.json` into Odoo database

**Process:**
1. Locate `module_registry.json` in addons_path
2. Parse JSON and extract module metadata
3. Create/update `github.module.installer` records in database
4. Mark modules as placeholder or full based on `is_placeholder` field

#### `action_install_from_github()`
**Purpose:** Download and install a full module from GitHub

**Process:**
1. Validate module is a placeholder (not already full)
2. Clone GitHub repository to temp location
3. Extract module folder from repo
4. Copy module to target addons_path
5. Trigger Odoo module list update (`update_list()`)
6. Install module via `button_immediate_install()`

**GitHub Cloning Strategy:**
- Tries GitHub CLI (`gh repo clone`) first
- Falls back to `git clone` if gh not available
- Supports repos where module is at root or in subdirectory
- Cleans up temp directory after copy

---

### 3. Installer Build Script

**Location:** `D:\SAMAI-18-SaaS\github-repos\100-samai-desktop-installer\build.py`

**Purpose:** Package SAM AI into a single-file Windows installer

**Build Process:**

#### Step 1: Build Launcher
```python
pyinstaller --onefile --windowed --name=sam_ai_launcher launcher/sam_ai_launcher.py
```
Creates: `launcher/dist/sam_ai_launcher.exe`

#### Step 2: Build Installer
```python
pyinstaller --onefile --windowed
    --name=SAM_AI_Setup
    --add-data=ecosystem;ecosystem
    --add-data=launcher/dist/sam_ai_launcher.exe;launcher
    installer/main.py
```
Creates: `dist/SAM_AI_Setup.exe`

**Bundled Components:**
- `ecosystem/` folder - Contains core components
- `sam_ai_launcher.exe` - Launcher executable
- Installer logic from `installer/main.py`

---

## 🔧 File Collection & Packaging Mechanisms

### **Current Workflow (Based on Code Analysis)**

There is **NO automatic script** currently generating `module_registry.json`. The registry appears to be **manually maintained** or generated through an undiscovered process.

### **How Files Are Identified:**

#### 1. Placeholder Detection
**Logic:** `_is_placeholder_module()` in `github_module_installer.py:94-120`

A module is considered a placeholder if:
- ❌ Does NOT have `models/`, `views/`, or `controllers/` directories
- ✅ Has minimal `__init__.py` (empty or comment only)
- ✅ Only contains `__manifest__.py`, `__init__.py`, and `static/description/`

#### 2. Full Module Structure
A full module contains:
- `__manifest__.py` - Module metadata
- `__init__.py` - Python imports
- `models/` - Data models (Python files)
- `views/` - UI definitions (XML files)
- `controllers/` - HTTP controllers (Python files)
- `static/` - JavaScript, CSS, images
- `data/` - XML data files
- `security/` - Access control rules

---

## 📂 Current Folder Structure

```
D:\SAMAI-18-SaaS\github-repos\
├── 00-odoo-core-15-modules/          # 15 full core modules (JUST MOVED)
│   ├── auth_signup/
│   ├── base/
│   ├── bus/
│   ├── mail/
│   ├── web/
│   └── ... (10 more)
│
├── 01-samai-odoo-18-lightweight-core/ # 641 placeholder modules
│   ├── module_registry.json          # Central catalog
│   ├── account/                      # Placeholder (only manifest + icon)
│   ├── sale/                         # Placeholder
│   └── ... (639 more)
│
├── 100-samai-desktop-installer/      # Installer build system
│   ├── build.py                      # Main build script
│   ├── installer/main.py             # Installer logic
│   ├── launcher/sam_ai_launcher.py   # Launcher app
│   ├── ecosystem/                    # Bundled components
│   └── dist/SAM_AI_Setup.exe         # Final installer
│
└── C:\Program Files\SAM AI\          # Deployed installation
    ├── server/odoo/addons/           # Odoo core (632 full modules)
    ├── addons/
    │   ├── sam-core/                 # SAM AI core modules
    │   │   └── ai_sam_github_installer/  # Installer module
    │   ├── lightweight-core/         # 641 placeholders (DUPLICATE)
    │   └── user_addons/              # User custom modules
    └── logs/odoo.log
```

---

## 🔄 Recommended Packaging Workflow

### **Step 1: Identify Files to Package**

**Script to Generate `module_registry.json`:**
```python
import os
import json
from pathlib import Path

def generate_module_registry(source_paths, output_file):
    """
    Scan multiple source paths and generate module_registry.json

    Args:
        source_paths: List of paths to scan for modules
        output_file: Path to write module_registry.json
    """
    registry = {}

    for source_path in source_paths:
        for module_dir in Path(source_path).iterdir():
            if not module_dir.is_dir():
                continue

            manifest_file = module_dir / '__manifest__.py'
            if not manifest_file.exists():
                continue

            # Read manifest
            manifest = {}
            with open(manifest_file, 'r', encoding='utf-8') as f:
                exec(f.read(), manifest)

            # Detect if placeholder
            is_placeholder = is_placeholder_module(module_dir)

            # Build registry entry
            registry[module_dir.name] = {
                'name': manifest.get('name', module_dir.name),
                'version': manifest.get('version', '18.0.1.0'),
                'summary': manifest.get('summary', ''),
                'description': manifest.get('description', '').strip(),
                'author': manifest.get('author', ''),
                'category': manifest.get('category', 'Uncategorized'),
                'depends': manifest.get('depends', []),
                'installable': manifest.get('installable', True),
                'application': manifest.get('application', False),
                'auto_install': manifest.get('auto_install', False),
                'license': manifest.get('license', 'LGPL-3'),
                'source_repo': determine_source_repo(module_dir.name),
                'is_placeholder': is_placeholder
            }

    # Write registry
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(registry, f, indent=2)

    print(f"Generated registry with {len(registry)} modules")
    return registry

def is_placeholder_module(module_path):
    """Check if module is a placeholder"""
    has_models = (module_path / 'models').exists()
    has_views = (module_path / 'views').exists()
    has_controllers = (module_path / 'controllers').exists()

    if has_models or has_views or has_controllers:
        return False

    init_file = module_path / '__init__.py'
    if init_file.exists():
        content = init_file.read_text().strip()
        if not content or content == "# Placeholder module":
            return True

    return False

def determine_source_repo(module_name):
    """Determine GitHub repo for module"""
    # Logic to determine which repo contains this module
    # Could check against known mappings or patterns
    return "odoo-18-standard-modules"

# Usage
source_paths = [
    "D:/SAMAI-18-SaaS/github-repos/00-odoo-core-15-modules",
    "D:/SAMAI-18-SaaS/github-repos/01-samai-odoo-18-lightweight-core"
]

generate_module_registry(
    source_paths,
    "D:/SAMAI-18-SaaS/github-repos/01-samai-odoo-18-lightweight-core/module_registry.json"
)
```

---

### **Step 2: Package for Installer**

**Files to Include:**

1. **15 Core Modules** (from `00-odoo-core-15-modules/`)
   - Total: ~3,000 files, ~50-80 MB

2. **641 Placeholder Modules** (from `01-samai-odoo-18-lightweight-core/`)
   - Total: ~1,900 files (manifests + icons), ~10-15 MB

3. **SAM AI Core Modules** (from `sam-core/`)
   - Includes `ai_sam_github_installer`

4. **Module Registry**
   - `module_registry.json`

5. **Odoo Server** (from `C:\Program Files\SAM AI\server\`)
   - Python, PostgreSQL bindings, core addons

---

### **Step 3: Build Installer**

Run `build.py`:
```bash
python build.py --smart
```

Output: `SAM_AI_Setup_Smart.exe` (~500-800 MB with all dependencies)

---

## 🎯 Missing Piece: Registry Generation

**You asked:** "How do we capture/get which files and package them?"

**Answer:** Currently, there's NO automated script to:
1. Scan module folders
2. Detect placeholder vs full
3. Generate `module_registry.json`

**Recommendation:** Create `generate_registry.py` script (provided above) to:
- Scan `00-odoo-core-15-modules/` (15 full)
- Scan `01-samai-odoo-18-lightweight-core/` (641 placeholders)
- Auto-detect which are placeholders using file structure
- Generate `module_registry.json` with all metadata
- Run this script BEFORE building installer

---

## 🚀 Complete Build Process (Recommended)

```bash
# Step 1: Generate module registry
python scripts/generate_registry.py

# Step 2: Build installer
cd D:\SAMAI-18-SaaS\github-repos\100-samai-desktop-installer
python build.py --smart

# Step 3: Test on clean VM
# Run SAM_AI_Setup_Smart.exe on Windows test machine

# Step 4: Distribute
# Upload to GitHub releases or distribution server
```

---

## 📊 Summary

**What Gets Packaged:**
- ✅ 15 full core modules (base, web, mail, etc.)
- ✅ 641 placeholder modules (lightweight cards)
- ✅ Module registry JSON
- ✅ GitHub installer module
- ✅ Odoo server + dependencies

**How It's Detected:**
- ✅ `_is_placeholder_module()` checks for models/views/controllers
- ✅ Reads `__manifest__.py` for metadata
- ❌ NO automated registry generation (manual process currently)

**Build Output:**
- 📦 `SAM_AI_Setup.exe` - Single-file installer
- 📦 `SAM_AI_Setup_Smart.exe` - Smart installer with detection

**User Experience:**
1. Run installer → Installs 15 core modules + 641 placeholders
2. Open SAM AI → Browse module catalog
3. Click "Install" on placeholder → Downloads full module from GitHub
4. Module installed and ready to use

---

**Created:** 2025-01-11
**Author:** CTO Analysis via Claude Code
