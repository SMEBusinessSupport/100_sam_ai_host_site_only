# SAM AI Odoo Modules

**Technical Name**: `sam_ai_odoo_modules`
**Version**: 18.0.2.0.0

Download and Install Modules from GitHub

## Description


SAM AI Odoo Modules - Unified Module Discovery
===============================================

This module extends Odoo's native Apps menu to support "Download to Install"
workflow for modules from GitHub and other sources.

**How It Works:**
- Extends ir.module.module with GitHub source fields
- Remote modules appear in the standard Apps menu
- Click Install → module downloads automatically → then installs
- One unified experience - no separate catalog

**Features:**
- Repository configuration (GitHub public/private, local filesystem)
- One-click scan to discover available modules
- Automatic download on install for remote modules
- Source type tracking (OCA, SAM AI, custom, etc.)

**Architecture:**
- Extends ir.module.module (not a separate catalog)
- Uses native Apps menu and views
- Repository scanning populates ir.module.module

Author: Better Business Builders
License: LGPL-3
    

## Module Details

# SAM AI Odoo Modules 

Lightweight Module Catalog - Download to Install **What is this module? **
A catalog system that stores metadata about available Odoo modules. Browse modules, download them from GitHub on demand, and install them into your Odoo instance. 
## Installation 1 **Add to Addons Path **

Ensure this module's parent directory is in your Odoo addons path: D:\SAMAI-18-SaaS\github-repos\05-samai-core\ 2 **Update Apps List **

In Odoo, go to **Apps **→ Click **Update Apps List **3 **Install Module **

Search for `sam_ai_odoo_modules `or "Module Catalog" and click **Install **
## Quick Start Guide 📋 **1. Browse **View catalog → ⬇️ **2. Download **Pull from GitHub → ▶️ **3. Install **Activate module → ✅ **4. Running **Ready to use 
## Configuration 
### Adding Repositories (Self-Building Catalog) **How it works: **

The catalog self-builds by scanning GitHub repositories. It discovers all Odoo modules automatically by reading their `__manifest__.py `files. No static JSON configuration needed! 1 **Add a Repository **

Go to **Module Catalog → Configuration → Repositories **

Click **Create **and fill in: 
- **Name: **Descriptive name (e.g., "SAM AI Core") 
- **GitHub Organization: **e.g., "odoo", "OCA", or your org 
- **Repository Name: **e.g., "odoo", "web", "custom-addons" 
- **Branch: **e.g., "18.0" or "main" 
- **Private Repository: **Check if private, then add your GitHub token 2 **Scan the Repository **

Click the **Scan Repository **button 

The module will: 
- Connect to GitHub API 
- Find all `__manifest__.py `files 
- Parse and cache module metadata 
- Create catalog entries automatically 3 **Browse Your Catalog **

Go to **Module Catalog → Catalog → All Modules **

All discovered modules are now available to download and install! 
### For Private GitHub Repositories **GitHub Token Required **

For private repositories, add your token directly in the repository configuration: 
- When creating/editing a repository, check **Private Repository **
- Enter your GitHub Personal Access Token in the **GitHub Token **field 
- The token needs `repo `scope for private repository access 

*Tokens are stored securely and never exposed to regular users. *
## Using the Catalog 
### Browsing Modules 

Navigate to **Module Catalog → Catalog → All Modules **
- Use **Kanban view **for visual browsing by category 
- Use **List view **for detailed information 
- Use **Filters **to find modules by state, source, or category 
### Downloading a Module 
- Find the module you want 
- Click the **Download **button 
- Wait for the download to complete 
- The module is now in your addons path 
### Installing a Module 
- After downloading, click the **Install **button 
- Or use **Download & Install **to do both in one click 
- The module will be activated in your Odoo instance 
## Module States State Meaning Available Actions `Available `In catalog, not downloaded Download, Download & Install `Downloading `Currently being pulled from GitHub Wait... `Downloaded `Code exists locally, not installed Install, View on GitHub `Installing `Being installed by Odoo Wait... `Installed `Active in Odoo Uninstall, View on GitHub `Error `Something went wrong Reset State, View error details 
## Troubleshooting **Download Failed: 404 Not Found **

Check that the GitHub organization, repository, and branch are correct in the catalog. **Download Failed: 401 Unauthorized **

For private repos, ensure your GitHub token is configured and has the correct permissions. **Module Not Found After Download **

The module may have been downloaded to a path not in your addons_path. Check your Odoo configuration. **Installation Failed: Missing Dependencies **

Use the **Download Dependencies **button to get required modules first. 
## Technical Details Item Details Models `odoo.module.catalog `, `module.catalog.repository `, `odoo.module.catalog.category `Repository Scanning GitHub Trees API (recursive), Contents API for manifest parsing Manifest Parsing Python `ast.literal_eval() `for safe parsing Download Method GitHub ZIP API (no git required) Install Method `ir.module.module.button_immediate_install() `Catalog Source Self-building from repository scans (no static JSON) 
## For SaaS Deployments **Using with SAM AI SaaS? **

If you're running this as part of a SaaS deployment, install the companion module `sam_ai_odoo_modules_saas `on your master server. It provides: 
- Proxy downloads (clients never see GitHub tokens) 
- Membership tier access control 
- Usage tracking and metering 

Location: `D:\SAMAI-18-SaaS\github-repos\99-saas-setup\sam_ai_odoo_modules_saas\ `

**SAM AI Odoo Modules **v18.0.1.0.0 
© 2025 Better Business Builders 
License: LGPL-3

## Dependencies

- `base`
