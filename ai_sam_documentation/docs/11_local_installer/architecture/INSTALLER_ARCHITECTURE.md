# Odoo 18 + SAM AI Installer Architecture

**Complete Hybrid Installer System**

---

## Overview

This installer implements a **hybrid architecture** that bundles lightweight placeholder modules while enabling on-demand installation of full modules from GitHub.

### Key Innovation

- **Bundle Size:** ~500MB (vs 2GB+ for full Odoo)
- **Available Modules:** 641+ immediately browsable
- **Installation Time:** 15-20 minutes initial, 1-2 minutes per additional module
- **Storage Efficiency:** Install only what you need, when you need it

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    INSTALLER (.EXE)                             │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Core Components (Required)                               │  │
│  ├──────────────────────────────────────────────────────────┤  │
│  │ • Python 3.12                                            │  │
│  │ • PostgreSQL 15                                          │  │
│  │ • Odoo 18 Core                                           │  │
│  │ • Git + GitHub CLI                                       │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Lightweight-Core Repository                              │  │
│  ├──────────────────────────────────────────────────────────┤  │
│  │ 16 Full Modules:                                         │  │
│  │  • base, web, mail, portal, etc.                         │  │
│  │  • ai_sam_github_installer ★                               │  │
│  │                                                          │  │
│  │ 641 Placeholder Modules:                                 │  │
│  │  • account, hr, crm, project, etc.                       │  │
│  │  • Each: __manifest__.py + icon + description            │  │
│  │                                                          │  │
│  │ + module_registry.json (module catalog)                  │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                         │
                         │ Installation completes
                         ↓
┌─────────────────────────────────────────────────────────────────┐
│                  INSTALLED SYSTEM                               │
│                                                                 │
│  C:\Program Files\Odoo 18\                                      │
│  ├── Python312\                                                 │
│  ├── PostgreSQL\15\                                             │
│  ├── server\                         (Odoo core)                │
│  ├── addons\                                                    │
│  │   └── lightweight-core\          (16 full + 641 placeholders)│
│  ├── user_addons\                    (writable - for downloads) │
│  ├── tools\                                                     │
│  │   ├── gh\                         (GitHub CLI)              │
│  │   └── git\                        (Git)                     │
│  └── scripts\                        (start/stop/config)        │
└─────────────────────────────────────────────────────────────────┘
                         │
                         │ User launches Odoo
                         ↓
┌─────────────────────────────────────────────────────────────────┐
│                     ODOO WEB INTERFACE                          │
│                                                                 │
│  User logs in → Sees "App Store" menu                           │
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │ App Store → Module Catalog                                │ │
│  │                                                           │ │
│  │  [account]  [hr]  [crm]  [project]  [inventory]  ...     │ │
│  │   Install    Install  Install   Install      Install      │ │
│  │                                                           │ │
│  │  641 modules available as cards with:                     │ │
│  │  - Icon, name, description                                │ │
│  │  - "Install from GitHub" button                           │ │
│  │  - Category, author, version                              │ │
│  └───────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                         │
                         │ User clicks "Install from GitHub"
                         ↓
┌─────────────────────────────────────────────────────────────────┐
│              GITHUB MODULE INSTALLATION                         │
│                                                                 │
│  1. ai_sam_github_installer module activated                      │
│  2. Clones from https://github.com/SMEBusinessSupport/          │
│         odoo-18-standard-modules                                │
│  3. Extracts module to C:\Program Files\Odoo 18\user_addons\    │
│  4. Updates Odoo module list                                    │
│  5. Installs module automatically                               │
│  6. Module ready to use                                         │
│                                                                 │
│  Time: 1-2 minutes per module                                   │
└─────────────────────────────────────────────────────────────────┘
```

---

## Components Breakdown

### 1. Installer Package (`odoo_samai_installer.iss`)

**Inno Setup script that creates the .exe installer**

Bundles:
- Python 3.12 (embedded)
- PostgreSQL 15 (embedded)
- Odoo 18 core server
- Lightweight-core repository (16 full + 641 placeholders)
- GitHub CLI + Git
- Post-installation scripts
- Documentation

### 2. Lightweight-Core Repository

**Located:** `D:\Odoo-18-SaaS\modules\odoo-18-lightweight-core\`
**GitHub:** `https://github.com/SMEBusinessSupport/odoo-18-lightweight-core`

Contains:
```
odoo-18-lightweight-core/
├── base/                    ← Full module
├── web/                     ← Full module
├── mail/                    ← Full module
├── portal/                  ← Full module
├── [12 more full modules]
├── ai_sam_github_installer/   ← ★ GitHub installer module (full)
├── account/                 ← Placeholder
├── hr/                      ← Placeholder
├── crm/                     ← Placeholder
├── [638 more placeholders]
└── module_registry.json     ← Catalog metadata
```

### 3. ai_sam_github_installer Module

**The critical infrastructure module that enables the hybrid system**

Features:
- App Store menu in Odoo
- Module catalog (kanban cards)
- GitHub clone functionality
- Installation workflow
- Progress tracking
- Error handling

Auto-installed with lightweight-core ✓

### 4. GitHub Repositories (Module Sources)

**Organization:** `SMEBusinessSupport`

Repositories:
- `odoo-18-lightweight-core` (bundled with installer)
- `odoo-18-standard-modules` (641 full modules)
- `odoo-18-community-extras` (community modules)
- `samai-*` (SAM AI modules - coming soon)

All repositories are **private** and require authentication.

---

## Installation Flow

### Phase 1: Initial Installation (15-20 minutes)

```
1. User downloads Odoo18_SAM_AI_Setup.exe
   ↓
2. Runs installer
   ↓
3. Installer extracts and configures:
   - Python 3.12
   - PostgreSQL 15
   - Odoo 18 core
   - Lightweight-core (16 full + 641 placeholders)
   - GitHub CLI + Git
   ↓
4. Post-installation scripts:
   - Create PostgreSQL database user
   - Initialize Odoo database
   - Configure odoo.conf with addon paths
   - Set up Windows services (optional)
   ↓
5. Installation complete
   - Desktop shortcut created
   - Start menu entries created
   - Odoo ready to launch
```

### Phase 2: First Launch

```
1. User clicks "Start Odoo" shortcut
   ↓
2. Odoo server starts (http://localhost:8069)
   ↓
3. User accesses web interface
   ↓
4. Creates master database + admin user
   ↓
5. Sees "App Store" menu (from ai_sam_github_installer)
   ↓
6. 16 full modules available immediately
   641 placeholder modules browsable
```

### Phase 3: On-Demand Module Installation

```
1. User navigates to App Store → Module Catalog
   ↓
2. Browses 641 modules (cards with icons)
   ↓
3. Finds desired module (e.g., "Accounting")
   ↓
4. Clicks "Install from GitHub"
   ↓
5. ai_sam_github_installer module:
   a. Checks GitHub authentication
   b. Clones odoo-18-standard-modules repo
   c. Extracts "account" module
   d. Copies to C:\Program Files\Odoo 18\user_addons\
   e. Updates Odoo module list
   f. Installs module + dependencies
   ↓
6. Module ready in 1-2 minutes
   ↓
7. User can install more modules as needed
```

---

## File Structure (Installed System)

```
C:\Program Files\Odoo 18\
├── Python312\
│   ├── python.exe
│   ├── Scripts\
│   └── Lib\
│
├── PostgreSQL\
│   └── 15\
│       ├── bin\
│       │   ├── psql.exe
│       │   └── pg_ctl.exe
│       └── data\
│
├── server\                           ← Odoo core
│   ├── odoo-bin
│   ├── odoo\
│   │   ├── __init__.py
│   │   ├── addons\                   ← Core Odoo addons (read-only)
│   │   │   ├── base\
│   │   │   ├── web\
│   │   │   └── [other core modules]
│   │   ├── cli\
│   │   ├── http\
│   │   └── [odoo framework]
│   └── requirements.txt
│
├── addons\
│   └── lightweight-core\             ← Lightweight core (bundled)
│       ├── base\                     ← Full (duplicate for convenience)
│       ├── web\                      ← Full
│       ├── mail\                     ← Full
│       ├── portal\                   ← Full
│       ├── [12 more full]
│       ├── ai_sam_github_installer\    ← ★ GitHub installer (full)
│       ├── account\                  ← Placeholder
│       ├── hr\                       ← Placeholder
│       ├── crm\                      ← Placeholder
│       ├── [638 more placeholders]
│       └── module_registry.json      ← Catalog
│
├── user_addons\                      ← Writable (downloaded modules)
│   ├── [downloaded modules appear here]
│   └── [user custom modules]
│
├── tools\
│   ├── gh\                           ← GitHub CLI
│   │   └── bin\
│   │       └── gh.exe
│   └── git\                          ← Git
│       └── bin\
│           └── git.exe
│
├── config\
│   └── odoo.conf                     ← Odoo configuration
│
├── filestore\                        ← Odoo file storage
├── sessions\                         ← Session storage
├── logs\                             ← Log files
├── backups\                          ← Database backups
│
├── scripts\
│   ├── start_odoo.bat                ← Start Odoo service
│   ├── stop_odoo.bat                 ← Stop Odoo service
│   ├── post_install.ps1              ← Post-installation setup
│   └── configure_odoo.ps1            ← Database initialization
│
└── docs\
    ├── README.txt
    ├── GITHUB_INSTALLER_SUMMARY.md
    └── lightweight_odoo_plan.md
```

---

## Key Configuration: `odoo.conf`

```ini
[options]
admin_passwd = admin
db_host = localhost
db_port = 5432
db_user = odoo_user
db_password = odoo_password
db_name = False

; Addon paths - CRITICAL for hybrid system
addons_path = C:\Program Files\Odoo 18\server\odoo\addons,
              C:\Program Files\Odoo 18\addons\lightweight-core,
              C:\Program Files\Odoo 18\user_addons

; Server config
xmlrpc_port = 8069
logfile = C:\Program Files\Odoo 18\logs\odoo.log
log_level = info

; Performance
workers = 4
max_cron_threads = 2
limit_memory_hard = 2684354560
limit_memory_soft = 2147483648
```

**Note:** The `addons_path` includes:
1. Core Odoo addons (server\odoo\addons)
2. Lightweight-core (16 full + 641 placeholders)
3. User addons (where downloaded modules go)

---

## Module Registry Structure

**File:** `module_registry.json`

```json
{
  "account": {
    "name": "Accounting",
    "version": "18.0.1.0",
    "summary": "Financial and accounting management",
    "description": "...",
    "author": "Odoo S.A.",
    "category": "Accounting/Accounting",
    "depends": ["base", "web"],
    "installable": true,
    "application": true,
    "auto_install": false,
    "license": "LGPL-3",
    "source_repo": "odoo-18-standard-modules",
    "is_placeholder": true
  },
  "hr": {
    ...
  },
  ...641 entries
}
```

This registry is read by `ai_sam_github_installer` to populate the App Store catalog.

---

## GitHub Authentication

For the installer to work properly, users need GitHub authentication:

### Option 1: GitHub CLI (Recommended)

```bash
# During installation or first run
gh auth login

# Follow prompts to authenticate
# Grants access to private repositories
```

### Option 2: SSH Keys

```bash
# Generate SSH key
ssh-keygen -t ed25519 -C "your_email@example.com"

# Add to GitHub account
# Copy public key to GitHub Settings → SSH Keys
```

### Option 3: Personal Access Token

```bash
# Create token at GitHub Settings → Developer settings → Personal access tokens
# Save to git config
git config --global credential.helper store
```

---

## Benefits of This Architecture

### For End Users
- **Fast initial setup** - Only 500MB download vs 2GB+
- **Browse everything** - See all 641 modules immediately
- **Install on-demand** - Download only what you need
- **Saves disk space** - Don't store unused modules
- **Easy exploration** - Visual catalog with icons and descriptions

### For Developers/Administrators
- **Modular deployment** - Add modules to repos without rebuilding installer
- **Version control** - All modules in Git
- **Easy updates** - Pull from GitHub for latest versions
- **Scalable** - Add unlimited modules to catalog
- **Debuggable** - Installation logs for troubleshooting

### For Business (SME Business Support)
- **Smaller installer** - Faster downloads, lower bandwidth costs
- **Dynamic catalog** - Update module offerings without new installer
- **Tiered licensing** - Can gate SAM AI modules behind licenses
- **Analytics ready** - Track module popularity
- **Professional image** - Modern app store experience

---

## Future Enhancements

### Phase 2: SAM AI Integration
- Add SAM AI modules to catalog
- License verification before installation
- Tiered access (Free, Starter, Pro, Enterprise)
- Payment gateway integration

### Phase 3: Advanced Features
- Module version management
- Update notifications
- Rollback functionality
- Usage analytics dashboard
- Module marketplace

---

## Building the Installer

### Prerequisites
1. Install Inno Setup 6
2. Prepare bundled components
3. Update paths in ISS script

### Build Command

```bash
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" C:\Users\total\installer\odoo_samai_installer.iss
```

Output: `C:\Users\total\installer\Output\Odoo18_SAM_AI_Setup.exe`

---

## Testing Checklist

- [ ] Installer runs without errors
- [ ] Python 3.12 installed and in PATH
- [ ] PostgreSQL 15 installed and running
- [ ] Odoo core extracted properly
- [ ] Lightweight-core (16 full + 641 placeholders) present
- [ ] `ai_sam_github_installer` module installed
- [ ] `module_registry.json` present
- [ ] GitHub CLI + Git in PATH
- [ ] Odoo starts successfully
- [ ] Web interface accessible at http://localhost:8069
- [ ] App Store menu visible
- [ ] Module Catalog shows 641 modules
- [ ] Can sync registry
- [ ] Can install module from GitHub (test with small module)
- [ ] Desktop shortcut works
- [ ] Start menu entries work

---

## Support and Documentation

- **Installation Guide:** `C:\Program Files\Odoo 18\docs\README.txt`
- **GitHub Installer:** `C:\Program Files\Odoo 18\docs\GITHUB_INSTALLER_SUMMARY.md`
- **Architecture Plan:** `C:\Program Files\Odoo 18\docs\lightweight_odoo_plan.md`
- **GitHub:** `https://github.com/SMEBusinessSupport`

---

**Status:** Ready for assembly and testing
**Next Steps:** Prepare bundled components and build installer

---

*Generated: 2025-11-07*

