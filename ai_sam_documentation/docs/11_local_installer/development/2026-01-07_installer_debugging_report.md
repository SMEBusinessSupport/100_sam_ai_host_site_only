# SAM AI Installer Debugging Report

**Date:** 2026-01-07
**Version:** 18.1.33.0
**Status:** RESOLVED - All critical issues fixed

---

## Executive Summary

This report documents the debugging session for the SAM AI Premium Business Suite installer. Multiple issues were identified and resolved, culminating in the creation of a modular PowerShell script system for reliable database and Odoo initialization.

---

## Issues Identified and Resolved

### Issue 1: PostgreSQL User Password Mismatch
**Symptom:** Database user `sam_ai_user` existed with a different password from a previous installation.
**Root Cause:** Installer checked if user exists but didn't handle password mismatch.
**Resolution:** Added `ALTER USER` command to reset password when user already exists.

### Issue 2: File Locks During Reinstall
**Symptom:** "Access is denied" error when replacing `python3.dll`.
**Root Cause:** Previous SAM AI Python processes still running.
**Resolution:** Added `KillExistingProcesses()` procedure in `PrepareToInstall()` to terminate all SAM AI processes before file operations.

### Issue 3: Port 5432 Conflict
**Symptom:** PostgreSQL failed to start on machines with existing Odoo 13 installation.
**Root Cause:** Port 5432 already in use by Odoo 13's PostgreSQL.
**Resolution:** Implemented dynamic port detection (5432-5442 range) that finds the first available port.

### Issue 4: Multi-Machine Path Configuration
**Symptom:** Installer failed to compile on different development machines.
**Root Cause:** Hardcoded paths in .iss file.
**Resolution:** Created `paths_config.iss` include file for machine-specific configuration.

### Issue 5: Uninstaller Errors
**Symptom:** "Runtime error (at 59:753): Could not call proc" during uninstall.
**Root Cause:** Python processes running when uninstaller tried to remove files.
**Resolution:** Added Python process cleanup to `[UninstallRun]` section.

### Issue 6: User/Database Existence Check Bug (ROOT CAUSE)
**Symptom:** Database and user creation always failed on fresh install.
**Root Cause:** Inno Setup's `Exec()` function returns the command's exit code, not the query result. The code checked `if ResultCode = 0` which meant "command ran successfully", not "user exists". PostgreSQL's psql returns exit code 0 regardless of query results.
**Resolution:** Created external PowerShell scripts that check query OUTPUT instead of exit codes.

### Issue 7: Missing Enterprise Module Categories
**Symptom:** Odoo initialization failed with `ParseError` referencing `base.module_category_services_timesheets`.
**Root Cause:** Odoo 18 Community Edition's `ir_module_module.xml` contains Enterprise module placeholders that reference categories not defined in Community Edition.
**Resolution:** Created patch script to add missing category definitions before Odoo initialization.

---

## Solution Architecture

### Modular Script System

A series of PowerShell scripts were created to handle each installation step independently, allowing for:
- Individual testing of each step
- Clear error identification
- Idempotent operations (safe to re-run)
- Detailed logging

### Script Locations

**Development Repository:**
```
H:\GitHub\100-samai-desktop-installer\build_new_exe_file\scripts\
```

**Live System (after deployment):**
```
C:\Program Files\SAM AI\scripts\
```

---

## Scripts Created

### Step 0: Patch Missing Categories
**File:** `00_patch_missing_categories.ps1`
**Purpose:** Adds missing Enterprise module category definitions to base module
**Exit Codes:**
- 0 = Success (patched or already patched)
- 1 = File not found
- 2 = Patch failed

**Categories Added:**
| Category ID | Name | Parent |
|-------------|------|--------|
| `module_category_services_timesheets` | Timesheets | Services |
| `module_category_services_project` | Project | Services |
| `module_category_marketing_email_marketing` | Email Marketing | Marketing |
| `module_category_manufacturing_manufacturing` | Manufacturing | Manufacturing |
| `module_category_sales_sales` | Sales | Sales |
| `module_category_inventory_inventory` | Inventory | Inventory |

---

### Step 1: PostgreSQL Service Check
**File:** `01_check_postgresql_service.ps1`
**Purpose:** Verify PostgreSQL-SAMAI service exists and is running
**Parameters:**
- `-Port` : PostgreSQL port (default: 5433)
- `-LogFile` : Log output path

**Exit Codes:**
- 0 = Success (service running)
- 1 = Service not found
- 2 = Service failed to start
- 3 = Connection test failed

---

### Step 2: Database Setup
**File:** `02_setup_database.ps1`
**Purpose:** Create database user and database for SAM AI
**Parameters:**
- `-Port` : PostgreSQL port (default: 5433)
- `-PgBin` : Path to PostgreSQL bin folder
- `-LogFile` : Log output path

**Key Feature:** Checks query OUTPUT (not exit code) to determine if user/database exists.

**Exit Codes:**
- 0 = Success
- 1 = User creation failed
- 2 = Database creation failed
- 3 = Connection failed

---

### Step 3: Odoo Initialization
**File:** `03_initialize_odoo.ps1`
**Purpose:** Initialize Odoo database with base module
**Parameters:**
- `-InstallDir` : SAM AI installation directory
- `-Database` : Database name (default: sam_ai)
- `-LogFile` : Log output path

**Features:**
- Checks if already initialized (idempotent)
- Stops Odoo service before init
- Verifies base module installed after init

**Exit Codes:**
- 0 = Success
- 1 = Prerequisites missing
- 2 = Odoo initialization failed
- 3 = Database connection failed

---

### Step 4: Odoo Service Registration
**File:** `04_register_odoo_service.ps1`
**Purpose:** Register and start Odoo as a Windows service
**Parameters:**
- `-InstallDir` : SAM AI installation directory
- `-LogFile` : Log output path

**Exit Codes:**
- 0 = Success
- 1 = Prerequisites missing
- 2 = Service registration failed
- 3 = Service start failed

---

### Master Runner
**File:** `RUN_ALL_STEPS.ps1`
**Purpose:** Execute all steps in sequence with validation
**Parameters:**
- `-Port` : PostgreSQL port (default: 5433)
- `-InstallDir` : SAM AI installation directory
- `-SkipStep3` : Skip Odoo initialization
- `-SkipStep4` : Skip service registration

**Batch Launcher:** `RUN_ALL_STEPS.bat` (run as Administrator)

---

## Test Results (2026-01-07)

| Step | Status | Duration | Notes |
|------|--------|----------|-------|
| Step 0 | **PASSED** | <1s | 6 categories patched |
| Step 1 | **PASSED** | <1s | PostgreSQL running on 5433 |
| Step 2 | **PASSED** | <1s | User & database verified |
| Step 3 | **PASSED** | 21.3s | Base module installed |
| Step 4 | SKIPPED | - | Service already registered |
| **Service** | **RUNNING** | - | Listening on port 8069 |

---

## Log File Locations

All logs are written to:
```
C:\Program Files\SAM AI\logs\
```

| Log File | Description |
|----------|-------------|
| `00_patch_categories.log` | Category patch operations |
| `01_postgresql_service.log` | PostgreSQL service check |
| `02_database_setup.log` | User and database creation |
| `03_odoo_init.log` | Odoo initialization |
| `04_odoo_service.log` | Service registration |
| `odoo.log` | Main Odoo application log |
| `db_setup.log` | Legacy database setup log |

---

## Port Configuration

| Service | Port | Notes |
|---------|------|-------|
| PostgreSQL-SAMAI | 5433 | Dynamic detection (5432 used by Odoo 13) |
| Odoo-SAMAI HTTP | 8069 | Configured in odoo.conf |
| Auto-login Server | 5000 | Welcome page during install |

---

## File Modifications

### Patched File
**Path:** `C:\Program Files\SAM AI\server\odoo\addons\base\data\ir_module_category_data.xml`
**Backup:** `ir_module_category_data.xml.bak`
**Change:** Added 6 missing module category records before closing `</data>` tag.

---

## Next Steps

1. **Integrate scripts into .iss file** - Replace inline Pascal code with calls to external PowerShell scripts
2. **Version bump** - Update to 18.1.34.0 for next release
3. **Test full installation** - Fresh install on clean machine
4. **Document in user guide** - Add troubleshooting section

---

## Repository Locations

| Repository | Path | Purpose |
|------------|------|---------|
| Installer | `H:\GitHub\100-samai-desktop-installer\build_new_exe_file\` | Inno Setup source |
| Python Bundle | `H:\GitHub\14-samai_python_bundle\` | Python + dependencies |
| Documentation | `H:\GitHub\05-samai-core\ai_sam_documentation\` | This documentation |

---

## Conclusion

The installer debugging session successfully identified and resolved all critical issues preventing SAM AI from initializing properly. The key breakthrough was discovering that Inno Setup's exit code checking was fundamentally flawed for database existence queries - the solution of using external PowerShell scripts that check query output provides a robust and maintainable approach.

The modular script system allows for:
- Independent testing of each component
- Clear separation of concerns
- Detailed logging for troubleshooting
- Idempotent operations safe for re-runs

SAM AI is now fully operational at `http://localhost:8069`.

---

*Report generated: 2026-01-07*
*Author: Claude Code (Opus 4.5)*
