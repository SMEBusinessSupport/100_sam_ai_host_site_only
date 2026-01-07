# SAM AI - Development Mode

**Technical Name**: `sam_ai_odoo_modules_dev`
**Version**: 18.0.1.1.0

Enables SAM AI development mode with enhanced debugging and testing features

## Description


SAM AI - Development Mode
=========================

**Install this module to enable SAM AI Development Mode.**

When installed, this module enables:

**SAM Chat Dev Features:**
- System prompt injected on every message (for testing prompt changes)
- Verbose debug logging in Odoo logs
- Debug files written (debug_last_prompt.md, etc.)
- Enhanced error messages

**Module Catalog Dev Features:**
- Pre-configured local filesystem repository paths
- Prefer local copy over GitHub API
- Auto-scan of local repositories

**System Parameters Set:**
- ``sam.dev_mode`` = True (master dev flag)
- ``sam.always_inject_prompt`` = True
- ``sam.debug_logging`` = True
- ``sam.write_debug_files`` = True

**For Development Only:**
This module should NOT be deployed to production SaaS clients.
Uninstalling this module reverts SAM to production mode behavior.

Author: Better Business Builders
License: LGPL-3
    

## Module Details

# SAM AI Module Catalog - Dev Environment 

Local Development Setup for Testing Module Distribution **Development Only! **
This module is for LOCAL DEVELOPMENT and testing only. Do NOT install this on production SaaS instances.
 It provides local filesystem scanning to simulate what the SaaS proxy would do. 
## What This Module Does **Purpose: **
- Test module catalog functionality without hitting GitHub API 
- Scan local filesystem paths for Odoo modules 
- Simulate the SaaS download behavior locally 
- Pre-configure your development repositories 
## Pre-Configured Repositories 

After installation, these repositories are automatically configured: Repository Local Path Type SAM AI Full Modules `D:\SAMAI-18-SaaS\github-repos\02-samai-odoo-18-full-modules `Local Filesystem SAM AI Core `D:\SAMAI-18-SaaS\github-repos\05-samai-core `Local Filesystem 
## Quick Start 1 **Install the Module **

Install `sam_ai_odoo_modules_dev `from Apps. It will automatically install the base `sam_ai_odoo_modules `module as a dependency. 2 **View Pre-Configured Repositories **

Go to **Module Catalog → Configuration → Repositories **

You'll see the pre-configured local repositories ready to scan. 3 **Scan a Repository **

Click on a repository, then click **Scan Repository **

The system will: 
- Walk through the local filesystem path 
- Find all `__manifest__.py `files 
- Parse and extract module metadata 
- Create catalog entries for each module 4 **Browse the Catalog **

Go to **Module Catalog → Catalog → All Modules **

All discovered modules are now visible with their metadata. 5 **Download a Module **

Click **Download **on any module. In dev mode, this: 
- Copies the module from the local source path 
- Places it in your configured addons directory 
- No GitHub API calls are made 
## Configuration 
### Download Path 

Downloaded modules are placed in: C:\Program Files\SAM AI\server\odoo\addons 

This is configured via System Parameters: 
- `sam_ai_odoo_modules.custom_addons_path `
### Dev Mode Settings Parameter Value Description `sam_ai_odoo_modules.dev_mode `True Enables development mode features `sam_ai_odoo_modules.prefer_local_copy `True Copy from local path instead of GitHub download `sam_ai_odoo_modules.custom_addons_path `C:\Program Files\SAM AI\server\odoo\addons Where to place downloaded modules 
## Adding Your Own Local Repository 1 **Create New Repository **

Go to **Module Catalog → Configuration → Repositories **

Click **Create **2 **Configure as Local Filesystem **
- **Name: **Your descriptive name 
- **Repository Type: **Select `Local Filesystem `
- **Local Path: **Full path to your modules folder 
- **Source Type: **Select appropriate type (SAM AI, Custom, etc.) 3 **Test and Scan **

Click **Test Connection **to verify the path exists 

Click **Scan Repository **to discover modules 
## How It Simulates Production Dev Environment Production SaaS Local filesystem path GitHub repository URL Direct file copy GitHub ZIP download via proxy No authentication needed GitHub token on master server Instant scanning GitHub API rate limits apply 
## Troubleshooting **Path Not Found Error **

Ensure the local path exists and is accessible. Use full absolute paths like: D:\SAMAI-18-SaaS\github-repos\02-samai-odoo-18-full-modules **No Modules Found **

The scanner looks for `__manifest__.py `files in immediate subdirectories. Ensure your path points to a folder containing module folders, not to a single module. **Download Fails **

Check that the target addons path is writable: C:\Program Files\SAM AI\server\odoo\addons 

You may need to run Odoo with administrator privileges or change the path. 

**SAM AI Module Catalog - Dev Environment **v18.0.1.0.0 
© 2025 Better Business Builders 
License: LGPL-3 

*For development and testing only. Not for production deployment. *

## Dependencies

- `ai_sam_base`
- `sam_ai_odoo_modules`
