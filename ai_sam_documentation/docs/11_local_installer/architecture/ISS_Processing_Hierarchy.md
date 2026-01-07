# SAM AI Installer - Process Hierarchy Documentation
**Version:** 18.1.0.0
**Last Updated:** 2025-11-18 (Evening - Session 2)
**Purpose:** Complete process flow documentation for installer execution
**Owner:** SME Business Support
**Recent Changes:**
- Added Process 0.1.1 (Python Bundle Build) - automated integration into build process
- Updated GAP 2 (Smart Detection) - documented failed fix attempt and revert
- Added GAP 8 (Python Bundle Missing Odoo) - fixed by integrating bundle build into compilation workflow

---

## Document Purpose

This document provides a **numbered, sequential process map** of every step the SAM AI installer executes, from launch to completion. Each process step is documented with:

- **Numbered hierarchy** (e.g., 1.0, 1.1, 1.1.1)
- **Process file** (.ps1, .py, Pascal code, or ISS directive)
- **Break points** (where failures commonly occur)
- **Success criteria** (how to validate the step succeeded)
- **Rollback actions** (what to do if step fails)

This document is the **single source of truth** for installation workflow and serves as a **future-proofing mechanism** to prevent AI-generated file churn from breaking the installer.

---

## Process Hierarchy - Complete Flow

### 0.0 PRE-INSTALLATION (Before Installer Runs)

#### 0.1 Build Process
- **Process File:** `dev_files\build_installer_final.ps1`
- **Purpose:** Compile installer EXE from ISS source
- **Success Criteria:** `SAM_AI_Premium_Business_Suite_Setup.exe` created in Output directory
- **Common Break Points:**
  - Python bundle missing or Odoo module not in bundle (GAP 8 - FIXED 2025-11-18)
  - temp_modules.iss missing or stale
  - PowerShell script syntax errors
  - Inno Setup compiler not found

#### 0.1.1 Python Bundle Build (Automated Pre-Check)
- **Process File:** `dev_files\build_python_bundle.ps1` (auto-called by build_installer_final.ps1)
- **Purpose:** Build embedded Python 3.12 with all Odoo dependencies and Odoo module
- **Trigger:** Automatically runs if Python bundle missing OR Odoo module not in site-packages
- **Integration:** Lines 54-91 of build_installer_final.ps1 (✅ FIXED 2025-11-18 - GAP 8)
- **Success Criteria:**
  - `bundled\python\python.exe` exists
  - `bundled\python\Lib\site-packages\odoo` exists (critical - was missing before fix)
  - All dependencies installed (psycopg2, lxml, Pillow, werkzeug, etc.)
- **Common Break Points:**
  - pip dependency conflicts
  - Network issues during download
  - Disk space insufficient (~500MB required)
- **Note:** Before GAP 8 fix, this was manual step causing "ModuleNotFoundError: No module named 'odoo'"

#### 0.1.2 Module Discovery (Pre-Build)
- **Process File:** `scripts\discover_modules.ps1`
- **Purpose:** Scan GitHub repos for SAM AI modules, generate temp_modules.iss and temp_modules.txt
- **Success Criteria:**
  - `temp_modules.iss` created with 8 modules
  - `temp_modules.txt` created with module list
- **Common Break Points:**
  - GitHub repo not cloned
  - Module __manifest__.py syntax errors
  - ChromaDB folders not excluded

---

### 1.0 INSTALLER INITIALIZATION (InitializeSetup Function)
**Process File:** `odoo_samai_installer.iss` lines 657-838 (Pascal code)

#### 1.1 Logging Setup
- **Purpose:** Create custom log file in installer directory
- **Process File:** `CustomLog()` function (line 415-430)
- **Output File:** `D:\SAMAI-18-SaaS\github-repos\100-samai-desktop-installer\Output\SAM_AI_Installer_Log.txt`
- **Success Criteria:** Log file created and writable
- **Common Break Points:**
  - Installer directory read-only
  - Antivirus blocking file creation

#### 1.2 Windows Version Check
- **Purpose:** Validate Windows 10+ (build 10.0+)
- **Process File:** Pascal code, line 673-686
- **Success Criteria:** Version.Major >= 10
- **Common Break Points:**
  - Windows 7/8 detected → ABORT INSTALLATION
- **Logged Output:** "Windows version check: PASSED" or "ERROR: This installer requires Windows 10 or higher"

#### 1.3 .NET Framework Check
- **Purpose:** Validate .NET 4.5+ installed (required for some dependencies)
- **Process File:** Pascal code, line 689-704
- **Success Criteria:** `IsDotNetInstalled(net45, 0)` returns True
- **Common Break Points:**
  - .NET not installed → ABORT INSTALLATION
- **Logged Output:** ".NET Framework check: PASSED" or "ERROR: .NET Framework 4.5 or higher is required"

#### 1.4 Smart Detection (Optional - Fallback Enabled)
- **Process File:** `scripts\smart_detection.ps1` (extracted to {tmp}, deleted after install)
- **Purpose:** Detect existing PostgreSQL, Odoo, databases
- **Success Criteria:**
  - Script runs without errors
  - `install_config.json` created in {tmp}
- **Common Break Points:**
  - ⚠️ **KNOWN ISSUE (GAP 2 - ACCEPTED RISK):** Windows Defender may delete .ps1 from {tmp}
  - **Why Not Fixed:** Script runs during InitializeSetup BEFORE {app} directory exists
  - **Attempted Fix (2025-11-18):** Tried moving to {app}\scripts → Caused runtime error "{app} constant not initialized"
  - **Resolution (2025-11-18):** Reverted to {tmp} extraction, accept deletion risk
  - **Current State:** Smart detection is OPTIONAL - installer uses safe defaults if script missing
- **Logged Output:** "Detection script found, attempting to run..." OR "WARNING: Detection script not found"
- **Fallback:** Installer continues with default values (sam_ai database, port 8069, port 5432)

#### 1.4.1 Load Configuration (From Smart Detection)
- **Process File:** `LoadInstallConfig()` function (line 446-510)
- **Purpose:** Parse install_config.json from smart detection
- **Success Criteria:** JSON parsed, values loaded into variables
- **Common Break Points:**
  - Config file not found (smart detection failed) → Use defaults
- **Logged Output:** "Loaded configuration from smart detection wizard" OR "No config file found, using default values"

#### 1.5 Existing Database Check
- **Purpose:** Detect if "sam_ai" database exists from previous install (prevents hangs - Issue #27)
- **Process File:** Pascal code, line 791-834
- **Success Criteria:**
  - PowerShell query succeeds
  - If database exists, user prompted to drop it
- **Common Break Points:**
  - PostgreSQL not installed → Logged as "Could not check" and continues
  - User cancels drop → ABORT INSTALLATION
- **Logged Output:**
  - "No existing database found - clean install" (exit code 0)
  - "WARNING: Database 'sam_ai' already exists from previous installation" (exit code 1)
  - "User chose to drop existing database" → "Successfully dropped existing database"

---

### 2.0 WIZARD UI INTERACTION (InitializeWizard Function)
**Process File:** `odoo_samai_installer.iss` lines 512-558 (Pascal code)

#### 2.1 User Information Page
- **Purpose:** Collect user full name, email, company name for Odoo setup
- **Process File:** `CreateInputQueryPage()` (line 519-539)
- **Success Criteria:** Page created, fields populated
- **Common Break Points:** None (UI creation very stable)
- **Logged Output:** "User information page created"

#### 2.2 Progress Page
- **Purpose:** Show installation progress to user
- **Process File:** `CreateOutputProgressPage()` (line 542-543)
- **Success Criteria:** Page created
- **Logged Output:** "Progress page created"

#### 2.3 Capture User Inputs
- **Process File:** `NextButtonClick()` function (line 610-621)
- **Purpose:** Save user-entered values to variables
- **Success Criteria:** Variables populated (UserFullName, UserEmail, CompanyName)
- **Common Break Points:** None (always succeeds, fields can be blank)

---

### 3.0 FILE EXTRACTION (ssInstall Step)
**Process File:** `[Files]` section (lines 99-195) executed by Inno Setup engine

#### 3.1 Extract Python 3.12 Runtime
- **Source:** `bundled\python\*`
- **Destination:** `{app}\python`
- **Size:** ~500 MB
- **Success Criteria:** Python.exe present at `{app}\python\python.exe`
- **Common Break Points:**
  - Disk space insufficient
  - Antivirus blocking extraction
- **Logged Output:** Inno Setup internal log (not in custom log)

#### 3.2 Extract PostgreSQL 15 Database
- **Source:** `bundled\postgresql\*`
- **Destination:** `{app}\postgresql`
- **Size:** ~300 MB (pgAdmin excluded to avoid path length issues)
- **Success Criteria:** postgres.exe present at `{app}\postgresql\bin\postgres.exe`
- **Common Break Points:**
  - Path length >260 characters (old Windows installs)
  - Antivirus blocking PostgreSQL binaries
- **Logged Output:** Inno Setup internal log

#### 3.3 Extract Odoo 18 Server
- **Source:** `bundled\server\*`
- **Destination:** `{app}\server`
- **Size:** ~200 MB
- **Success Criteria:** odoo-bin present at `{app}\server\odoo-bin`
- **Common Break Points:**
  - Python dependencies missing (should be pre-installed in bundled Python)
- **Logged Output:** Inno Setup internal log

#### 3.4 Extract Odoo Core Modules (21 modules)
- **Source:** `00-odoo-core-15-modules\*`
- **Destination:** `{app}\server\odoo\addons`
- **Modules:** base, web, mail, auth_signup, portal, hr, hr_contract, etc. (21 total)
- **Success Criteria:** `{app}\server\odoo\addons\base` folder exists
- **Common Break Points:**
  - None (very stable)
- **Logged Output:** Inno Setup internal log

#### 3.5 Extract Lightweight Core Placeholders (641 modules)
- **Source:** `01-samai-odoo-18-lightweight-core\*`
- **Destination:** `{app}\catalogs\lightweight-core` (NOT in addons_path)
- **Purpose:** App catalog for GitHub installer (not loaded by Odoo)
- **Success Criteria:** `{app}\catalogs\lightweight-core` folder exists with module_registry.json
- **Common Break Points:**
  - None (placeholders are metadata only)
- **Logged Output:** Inno Setup internal log

#### 3.6 Extract SAM AI Core Modules (8 modules - DYNAMIC)
- **Source:** Defined in `temp_modules.iss` (generated by discover_modules.ps1)
- **Destination:** `{app}\addons\samai_core\[module_name]`
- **Modules:**
  1. ai_brain (04-samai-brain)
  2. ai_sam (05-samai-core)
  3. ai_sam_cache_manager (05-samai-core)
  4. ai_sam_github_installer (05-samai-core)
  5. ai_sam_intelligence (05-samai-core)
  6. ai_sam_memory (05-samai-core)
  7. ai_sam_messenger (05-samai-core)
  8. github_app (05-samai-core)
- **Success Criteria:** All 8 module folders exist in `{app}\addons\samai_core\`
- **Common Break Points:** ⚠️ **CRITICAL DEPENDENCY**
  - temp_modules.iss missing → INSTALLER COMPILATION FAILS
  - temp_modules.iss stale → Wrong modules installed
- **Logged Output:** Inno Setup internal log

#### 3.7 Extract PowerShell Scripts
- **Source:** `scripts\*.ps1`
- **Destinations:**
  - `{tmp}` (smart_detection.ps1, convert_to_lightweight.ps1) - **DELETED AFTER INSTALL**
  - `{app}\sam\scripts` (post_install.ps1, configure_odoo.ps1, start_odoo.bat, stop_odoo.bat, temp_modules.txt)
  - `{app}\scripts` (register_service.ps1, auto_repair_dependencies.ps1, cleanup_before_uninstall.ps1, etc.)
- **Success Criteria:** Critical scripts present:
  - `{app}\sam\scripts\post_install.ps1`
  - `{app}\sam\scripts\configure_odoo.ps1`
  - `{app}\scripts\register_service.ps1`
- **Common Break Points:**
  - Scripts in {tmp} deleted before use (smart_detection.ps1 - known issue)
- **Logged Output:** Inno Setup internal log

#### 3.8 Extract Assets
- **Source:** `assets\*`
- **Destination:** `{app}\sam\assets`
- **Files:** sam_ai.ico, welcome_landing.html
- **Success Criteria:** `{app}\sam\assets\sam_ai.ico` exists
- **Common Break Points:** None
- **Logged Output:** Inno Setup internal log

#### 3.9 Create Empty Directories
- **Purpose:** 4-path architecture (samai_core | odoo\addons | odoo_extras | member_addons)
- **Directories Created:**
  - `{app}\addons\user_addons`
  - `{app}\catalogs`
  - `{app}\filestore`
  - `{app}\sessions`
  - `{app}\logs`
  - `{app}\backups`
  - `{app}\data\chroma`
  - `{app}\server\odoo_extras`
  - `{app}\addons\member_addons`
- **Success Criteria:** All directories exist with write permissions
- **Common Break Points:**
  - Permission denied (requires admin rights)
- **Logged Output:** "CurStepChanged: Starting installation (ssInstall)"

#### 3.10 Update Windows Registry (PATH variables)
- **Purpose:** Add Python, PostgreSQL, Git, GitHub CLI to system PATH
- **Registry Keys Modified:**
  - `HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment\Path`
- **Additions:**
  - `{app}\python`
  - `{app}\python\Scripts`
  - `{app}\postgresql\bin`
- **Success Criteria:** PATH updated (requires system restart or new shell to take effect)
- **Common Break Points:**
  - Requires admin rights (fails silently if not admin)
- **Logged Output:** Inno Setup internal log

---

### 4.0 POST-INSTALLATION PHASE 1: POSTGRESQL SETUP (ssPostInstall Step)
**Process File:** `scripts\post_install.ps1` (line 262-263 in ISS triggers it)
**Triggered By:** `[Run]` section, line 261-263

#### 4.1 Cleanup Existing Processes ⚠️ **NEW ADDITION NEEDED**
- **Purpose:** Stop any hanging Python/PostgreSQL/conhost processes from previous failed installs
- **Process File:** `post_install.ps1` lines (would need to be added - currently in configure_odoo.ps1)
- **Success Criteria:** No conflicting processes running
- **Common Break Points:**
  - Processes from previous install still running → Database initialization fails
- **Logged Output:** "[0/3] Cleaning up existing processes..."
- **Recommendation:** ⚠️ **MOVE THIS TO post_install.ps1 as first step**

#### 4.2 Initialize PostgreSQL Database Cluster
- **Process File:** `post_install.ps1` (line numbers TBD - need to read file)
- **Command:** `initdb -D "{app}\postgresql\data" -U postgres -E UTF8 --locale=en_US.UTF8`
- **Purpose:** Create PostgreSQL data directory and configuration
- **Success Criteria:**
  - `{app}\postgresql\data` folder created
  - `pg_hba.conf` and `postgresql.conf` files exist
- **Common Break Points:** ⚠️ **HIGH FAILURE RATE**
  - Data directory already exists → initdb fails
  - Locale not available → Falls back to system locale
- **Logged Output:** "Initializing PostgreSQL database cluster..."
- **Validation Needed:** ✅ **Check data directory exists before continuing**

#### 4.3 Start PostgreSQL Server
- **Process File:** `post_install.ps1`
- **Command:** `pg_ctl -D "{app}\postgresql\data" -l "{app}\logs\postgresql.log" start`
- **Purpose:** Launch PostgreSQL server process
- **Success Criteria:**
  - PostgreSQL process running
  - Server accepting connections on port 5432
- **Common Break Points:** ⚠️ **CRITICAL FAILURE POINT**
  - Server starts but doesn't accept connections (needs 5-10 seconds to initialize)
  - Port 5432 already in use (system-wide PostgreSQL installed)
  - No validation that server is ready
- **Logged Output:** "Starting PostgreSQL server..."
- **Validation Needed:** ✅ **Run pg_isready -h localhost -p 5432 with 30-second timeout (GAP 3)**

#### 4.4 Create PostgreSQL User (sam_ai_user)
- **Process File:** `post_install.ps1` line 94
- **Command:** `psql -U postgres -c "CREATE USER sam_ai_user WITH PASSWORD 'samai_secure_pass' CREATEDB;"`
- **Purpose:** Create Odoo database user with CREATEDB privilege
- **Success Criteria:** User exists in pg_roles
- **Common Break Points:**
  - PostgreSQL not accepting connections yet (step 4.3 didn't validate)
  - User already exists from previous install
- **Logged Output:** "Creating PostgreSQL user: sam_ai_user"
- **Validation Needed:** ✅ **Query pg_roles to confirm user created (GAP 4)**
- **Security Issue:** ⚠️ Hardcoded password "samai_secure_pass" (accepted for dev, must fix for production)

#### 4.5 Create PostgreSQL Database (sam_ai)
- **Process File:** `post_install.ps1` line 129
- **Command:** `createdb -U sam_ai_user -O sam_ai_user sam_ai`
- **Purpose:** Create Odoo database owned by sam_ai_user
- **Success Criteria:** Database exists in pg_database
- **Common Break Points:** ⚠️ **HIGH FAILURE RATE**
  - Database already exists from previous install (Issue #27)
  - sam_ai_user doesn't have CREATEDB privilege (step 4.4 failed)
- **Logged Output:** "Creating database: sam_ai"
- **Validation Needed:** ✅ **Query pg_database to confirm database created (GAP 4)**

#### 4.6 Validate PostgreSQL Setup (NOT IMPLEMENTED)
- **Purpose:** Confirm PostgreSQL is running and sam_ai database is accessible
- **Process File:** ⚠️ **MISSING - NEEDS TO BE ADDED (GAP 3 + GAP 4)**
- **Recommended Commands:**
  - `pg_isready -h localhost -p 5432` (server accepting connections)
  - `psql -U sam_ai_user -d sam_ai -c "\q"` (user can connect to database)
- **Success Criteria:**
  - pg_isready returns 0
  - psql connection succeeds
- **Failure Action:**
  - Log error with exact failure point
  - Return exit code 1 to installer
  - Installer triggers rollback (GAP 7)
- **Logged Output:** ⚠️ **NOT LOGGED - NEEDS IMPLEMENTATION**

---

### 5.0 POST-INSTALLATION PHASE 2: ODOO DATABASE INITIALIZATION
**Process File:** `scripts\configure_odoo.ps1` (line 279-281 in ISS triggers it)
**Triggered By:** `[Run]` section, line 278-281

#### 5.1 Cleanup Existing Processes
- **Process File:** `configure_odoo.ps1` lines 22-104
- **Purpose:** Stop Python/PostgreSQL/conhost processes from previous installs
- **Success Criteria:** No conflicting processes found or all stopped
- **Common Break Points:**
  - Processes can't be stopped (requires admin rights)
- **Logged Output:** "[0/3] Cleaning up existing processes... [OK] Cleanup complete"
- **Recommendation:** ⚠️ **This should be in post_install.ps1 BEFORE PostgreSQL setup**

#### 5.2 Drop Existing Database (Phase 0 - Clean Slate)
- **Process File:** `configure_odoo.ps1` lines 122-138
- **Purpose:** Drop sam_ai database if it exists (ensures fresh start)
- **Command:** `dropdb -U sam_ai_user --if-exists sam_ai`
- **Success Criteria:** Database does not exist
- **Common Break Points:**
  - Database has active connections (Odoo still running)
- **Logged Output:** "Phase 0: Ensuring clean database state... Database dropped successfully" OR "No existing database found"
- **Note:** This contradicts step 4.5 (create database) - creates → drops → initializes (inefficient, but ensures clean state)

#### 5.3 Initialize Database with Base Module (Phase 1)
- **Process File:** `configure_odoo.ps1` lines 142-228
- **Command:** `python.exe odoo-bin -c odoo.conf -d sam_ai -i base --stop-after-init --no-http`
- **Purpose:** Initialize Odoo database schema, install base module
- **Success Criteria:**
  - Database populated with Odoo tables (ir_module_module, res_users, etc.)
  - Base module state = 'installed'
  - Exit code 0
- **Common Break Points:** ⚠️ **CRITICAL FAILURE POINT**
  - Python dependencies missing (should be bundled, but can fail)
  - PostgreSQL not running (step 4.3 or 4.6 validation missing)
  - Database doesn't exist (step 4.5 failed, step 5.2 dropped it)
  - Module import errors (circular dependencies, syntax errors)
- **Logged Output:** "Phase 1: Initializing database with base module... Base module initialized successfully!"
- **Failure Handling:** ✅ **HAS AUTO-REPAIR** (lines 168-226)
  - Runs `auto_repair_dependencies.ps1`
  - Retries base module installation
  - If retry fails → exit code 1 (but installer shows "Complete!" anyway - BUG)

#### 5.3.1 Auto-Repair Layer 3 (If Phase 1 Fails)
- **Process File:** `scripts\auto_repair_dependencies.ps1` (triggered by configure_odoo.ps1 line 181)
- **Purpose:** Parse odoo.log for missing dependencies, attempt pip install
- **Success Criteria:** Missing dependencies installed, retry succeeds
- **Common Break Points:**
  - Dependency not available in PyPI
  - pip installation fails (network issue, permission denied)
- **Logged Output:** "Attempting auto-repair of missing dependencies... AUTO-REPAIR SUCCESSFUL"
- **Failure Handling:** Exit code 1 → "You can initialize the database manually later"

#### 5.4 Install SAM AI Modules (Phase 2)
- **Process File:** `configure_odoo.ps1` lines 232-276
- **Purpose:** Install all SAM AI modules (dynamic list from temp_modules.txt)
- **Module List Source:**
  - Primary: `{app}\sam\scripts\temp_modules.txt` (generated by discover_modules.ps1)
  - Fallback: Hardcoded list in line 249 (web,mail,ai_brain,ai_sam,ai_sam_cache_manager,ai_sam_github_installer,ai_sam_intelligence,ai_sam_memory,ai_sam_messenger,github_app)
- **Command:** `python.exe odoo-bin -c odoo.conf -d sam_ai -i [module_list] --stop-after-init --no-http`
- **Success Criteria:**
  - All modules state = 'installed' in ir_module_module table
  - Exit code 0
- **Common Break Points:** ⚠️ **HIGH FAILURE RATE**
  - temp_modules.txt missing (falls back to hardcoded list)
  - Module dependencies not met (e.g., web module needs core modules)
  - Module __manifest__.py syntax errors
  - Module import errors (missing Python dependencies)
  - **OLD BUG (FIXED):** ai_sam_ui referenced but doesn't exist (removed from fallback list line 249)
- **Logged Output:** "Phase 2: Installing ALL SAM AI modules (this may take 2-3 minutes)... SAM AI modules installed successfully!"
- **Failure Handling:** ⚠️ **WEAK HANDLING**
  - Exit code != 0 → Logs warning "SAM AI module installation encountered errors"
  - Installer continues (base Odoo installed, SAM AI not functional)
  - No rollback, no validation, user must troubleshoot manually

#### 5.5 Validate Odoo Module Installation (NOT IMPLEMENTED)
- **Purpose:** Confirm all expected modules are in 'installed' state
- **Process File:** ⚠️ **MISSING - NEEDS TO BE ADDED (GAP 5)**
- **Recommended Query:**
  ```sql
  SELECT COUNT(*) FROM ir_module_module
  WHERE name='base' AND state='installed';
  ```
  Repeat for all 8 SAM AI modules
- **Success Criteria:** All queries return 1
- **Failure Action:**
  - Log which modules failed to install
  - Return exit code 1
  - Installer triggers rollback (GAP 7)
- **Logged Output:** ⚠️ **NOT LOGGED - NEEDS IMPLEMENTATION**

#### 5.6 Display Installation Summary
- **Process File:** `configure_odoo.ps1` lines 281-300
- **Purpose:** Show user the installed modules and default credentials
- **Logged Output:**
  ```
  Database initialization complete!
  Database: sam_ai
  Admin user: admin
  Admin password: admin
  Installed modules:
    - base, web, mail (Odoo core)
    - ai_brain (SAM AI brain layer)
    - ai_sam (SAM AI orchestrator)
    - ... (all 8 SAM AI modules)
  ```
- **Common Break Points:** None (informational only)

---

### 6.0 POST-INSTALLATION PHASE 3: WINDOWS SERVICE REGISTRATION
**Process File:** `scripts\register_service.ps1` (line 292-297 in ISS triggers it)
**Triggered By:** `[Run]` section, line 289-297
**Flags:** runascurrentuser postinstall (preserves admin privileges)
**✅ FIXED (2025-11-18 - GAP 6):** Added `runascurrentuser` flag to prevent Error 5: Access Denied

#### 6.1 Check for Existing Services
- **Process File:** `register_service.ps1` (need to read file for line numbers)
- **Command:** `sc.exe query | findstr /i "odoo"`
- **Purpose:** Detect if Odoo service already registered (from previous install)
- **Success Criteria:** No existing services found
- **Common Break Points:**
  - Service exists from previous install → User prompted to remove
- **Logged Output:** "Checking for existing service... No existing Odoo services found"

#### 6.2 Register Windows Service
- **Process File:** `register_service.ps1` line 150
- **Command:** `sc.exe create SAMAI-Odoo binPath= "C:\Program Files\SAM AI\python\python.exe C:\Program Files\SAM AI\server\odoo-bin -c C:\Program Files\SAM AI\server\odoo.conf" start= auto`
- **Purpose:** Register Odoo as Windows service for auto-start
- **Success Criteria:**
  - Service created (sc.exe exit code 0)
  - Service queryable with `sc.exe query SAMAI-Odoo`
- **Common Break Points:**
  - ✅ **FIXED (GAP 6):** Error 5 "Access Denied" - PowerShell was de-elevating from admin context
  - Previously: Missing `runascurrentuser` flag → PowerShell ran as standard user → sc.exe failed
  - Now: `runascurrentuser` preserves installer's admin privileges → sc.exe succeeds
  - Service name already exists (from previous install)
- **Logged Output:** "Registering SAM AI Odoo service using sc.exe... Service Name: SAMAI-Odoo"
- **Error Output:** "[ERROR] Service registration failed: Failed to create service. Exit code: 5. [SC] OpenSCManager FAILED 5: Access is denied."

#### 6.3 Validate Service Registration (NOT IMPLEMENTED)
- **Purpose:** Confirm service was created and can start
- **Process File:** ⚠️ **MISSING - NEEDS TO BE ADDED (GAP 6)**
- **Recommended Commands:**
  - `sc.exe query SAMAI-Odoo` (service exists)
  - `sc.exe start SAMAI-Odoo` (service can start)
  - Wait 5 seconds, then `sc.exe query SAMAI-Odoo | findstr "RUNNING"` (service is running)
- **Success Criteria:** Service state = RUNNING
- **Failure Action:**
  - Log error with exact failure point
  - Return exit code 1
  - Installer triggers rollback (GAP 7)
- **Logged Output:** ⚠️ **NOT LOGGED - NEEDS IMPLEMENTATION**

---

### 7.0 POST-INSTALLATION PHASE 4: OPTIONAL TASKS
**Process File:** Multiple, all triggered by `[Run]` section flags: postinstall skipifsilent
**User Selectable:** Checkboxes in installer UI

#### 7.1 Launch SAM AI (Start Odoo)
- **Process File:** `{app}\sam\scripts\start_odoo.bat`
- **Triggered By:** Line 293-295 (if user checks "Launch SAM AI now")
- **Purpose:** Start Odoo server in background
- **Command:** `start /B python.exe odoo-bin -c odoo.conf`
- **Success Criteria:** Odoo process running, HTTP server on port 8069
- **Common Break Points:**
  - Odoo already running from service registration (step 6.2)
  - Port 8069 already in use
  - PostgreSQL not running (step 4.3 failed)
- **Logged Output:** None (runs in background)
- **Validation Needed:** ✅ **Test http://localhost:8069 responds before opening browser (GAP 9)**

#### 7.2 Auto-Login and Open Browser
- **Process File:** `scripts\auto_login.py` (line 297-301 in ISS triggers it)
- **Purpose:** Open web browser to http://localhost:8069 with auto-login
- **Command:** `python.exe auto_login.py`
- **Success Criteria:** Browser opens to Odoo login page
- **Common Break Points:** ⚠️ **COMMON FAILURE**
  - Odoo not ready yet (takes 30-60 seconds to start)
  - Browser opens to "Connection refused"
  - User sees error instead of SAM AI login
- **Logged Output:** None
- **Validation Needed:** ✅ **Wait for http://localhost:8069 to respond before opening browser (GAP 9)**

#### 7.3 Close Orphaned CMD Windows
- **Process File:** `scripts\close_cmds.ps1` (line 303-307 in ISS triggers it)
- **Purpose:** Clean up any hanging CMD windows from installation scripts
- **Command:** `powershell.exe -ExecutionPolicy Bypass -WindowStyle Hidden -File close_cmds.ps1`
- **Success Criteria:** All CMD windows closed
- **Common Break Points:** None
- **Logged Output:** None (runs hidden)

---

### 8.0 INSTALLATION COMPLETE (ssDone Step)
**Process File:** `odoo_samai_installer.iss` line 652-653 (Pascal code)

#### 8.1 Log Installation Complete
- **Purpose:** Mark end of installation in log
- **Process File:** Pascal code, line 653
- **Logged Output:** "CurStepChanged: Installation complete (ssDone)"

#### 8.2 Show Completion Message
- **Purpose:** Display "Setup Successful" wizard page
- **Success Criteria:** Installer UI shows completion screen
- **Common Break Points:** None

---

## Break Point Analysis

### Most Common Failure Points (Ranked by Frequency)

1. **✅ FIXED: Admin Rights Check Added (GAP 1)** - COMPLETED (Pre-2025-11-18)
   - **Location:** Process 1.0 (InitializeSetup, lines 688-709)
   - **Fix Applied:** Added `IsAdminInstallMode()` check at installer startup
   - **Result:** Installer exits gracefully if not run as admin with clear error message
   - **Note:** This prevented installers from starting, but GAP 6 was needed to preserve admin rights during execution

2. **✅ FIXED: PostgreSQL Not Ready (GAP 3)** - COMPLETED (Pre-2025-11-18)
   - **Location:** Process 4.3 (Start PostgreSQL)
   - **Fix Applied:** Added `Test-PostgreSQLReady` function with 30s timeout (post_install.ps1:195-206)
   - **Result:** PostgreSQL connection validated before proceeding to user creation
   - **Validation:** pg_isready-style polling with error logging if timeout occurs

3. **✅ FIXED: Database Creation Failures (GAP 4)** - COMPLETED (Pre-2025-11-18)
   - **Location:** Process 4.5 (Create Database)
   - **Fixes Applied:**
     - Line 300: Check if database exists before creation (skip if exists)
     - Line 325: Validate database was created (query pg_database)
     - Line 343: Test connection to database (validate credentials work)
   - **Result:** Database creation idempotent, validated, and connection-tested

4. **⚠️ ACCEPTED RISK: Smart Detection Script Deleted (GAP 2)** - ATTEMPTED 2025-11-18, REVERTED
   - **Location:** Process 1.4 (Smart Detection)
   - **Symptom:** "WARNING: Detection script not found"
   - **Root Cause:** Windows Defender deletes .ps1 from {tmp} before execution
   - **Fix Attempted:** Changed extraction from {tmp} to {app}\scripts (line 173 in .iss)
   - **Result of Attempt:** Runtime error - "{app} constant not initialized" during InitializeSetup
   - **Why Failed:** InitializeSetup runs BEFORE user selects install directory, {app} doesn't exist yet
   - **Resolution:** Reverted to {tmp} extraction, accepted Windows Defender deletion risk
   - **Current State:** Smart detection is OPTIONAL, installer uses safe defaults if script missing

5. **✅ FIXED: Module Installation Failures (GAP 5)** - COMPLETED (Pre-2025-11-18)
   - **Location:** Process 5.5 (Validate Module Installation)
   - **Fix Applied:** Added module validation section (configure_odoo.ps1:259+)
   - **Result:** Queries ir_module_module table to verify all modules installed
   - **Behavior:** Fails loudly if critical modules missing, provides clear error message

6. **✅ FIXED: Service Registration Access Denied (GAP 6)** - COMPLETED 2025-11-18
   - **Location:** Process 6.2 (Register Windows Service)
   - **Symptom:** "[SC] OpenSCManager FAILED 5: Access is denied"
   - **Root Cause:** PowerShell de-elevated from admin context (missing runascurrentuser flag)
   - **Fix Applied:** Added `runascurrentuser` flag to preserve admin privileges (line 296 in .iss)
   - **Result:** sc.exe now succeeds with admin rights, service registers correctly
   - **Remaining:** Add service state validation after registration (verify it's running)

7. **✅ FIXED: Browser Opens Too Early (GAP 9)** - COMPLETED (Pre-2025-11-18)
   - **Location:** Process 7.2 (Auto-Login)
   - **Fix Applied:** Added `wait_for_odoo()` function with HTTP polling (auto_login.py:198-214)
   - **Result:** Polls http://localhost:8069 up to 30 times (60 seconds) before opening browser
   - **Behavior:** Opens browser only when Odoo HTTP server responds with 200 OK

8. **✅ FIXED: Python Bundle Missing Odoo Module (GAP 8)** - COMPLETED 2025-11-18
   - **Location:** Process 0.1.1 (Python Bundle Build)
   - **Symptom:** "ModuleNotFoundError: No module named 'odoo'" when installer tries to start Odoo
   - **Root Cause:** `build_python_bundle.ps1` was never executed, bundled Python missing Odoo in site-packages
   - **Why This Happened:** Build workflow required manual execution of Python bundle builder
   - **Fix Applied:** Integrated Python bundle build into `build_installer_final.ps1` (lines 54-91)
   - **How It Works:**
     - Check if `bundled\python\python.exe` exists → Build if missing
     - Check if `bundled\python\Lib\site-packages\odoo` exists → Rebuild if missing
     - Only compile installer after Python bundle is complete and validated
   - **Result:** Installer now automatically builds Python bundle with Odoo module before compilation
   - **Benefit:** One-command build process, no manual steps required

---

## Rollback Actions (NOT IMPLEMENTED - GAP 7)

### Current State (No Rollback)
If any step fails, installer continues and shows "Installation Complete!" even though SAM AI is broken.

### Recommended Rollback Flow

#### Rollback Trigger Points
- Process 1.2 (Windows Version) → Exit (no rollback needed, nothing installed)
- Process 1.3 (.NET Framework) → Exit (no rollback needed, nothing installed)
- Process 4.6 (PostgreSQL Validation) → **Rollback PostgreSQL**
- Process 5.5 (Odoo Module Validation) → **Rollback Odoo + PostgreSQL**
- Process 6.3 (Service Validation) → **Rollback Service + Odoo + PostgreSQL**

#### Rollback Steps
1. **Stop Windows Service** (if created)
   - `sc.exe stop SAMAI-Odoo`
   - `sc.exe delete SAMAI-Odoo`
2. **Drop PostgreSQL Database** (if created)
   - `dropdb -U sam_ai_user --if-exists sam_ai`
3. **Drop PostgreSQL User** (if created)
   - `psql -U postgres -c "DROP USER IF EXISTS sam_ai_user;"`
4. **Stop PostgreSQL Server** (if running)
   - `pg_ctl -D "{app}\postgresql\data" stop`
5. **Remove Files** (handled by Inno Setup uninstall)
   - Inno Setup tracks all installed files, removes them automatically
6. **Show Error Message**
   - Display exact failure point and error message
   - Provide log file location for troubleshooting

---

## Enhanced Logging Requirements (GAP Analysis Item)

### Current Logging (Insufficient)
- **Log File:** `D:\SAMAI-18-SaaS\github-repos\100-samai-desktop-installer\Output\SAM_AI_Installer_Log.txt`
- **Coverage:** Only high-level steps (InitializeSetup, Windows version check, smart detection)
- **Missing:** No PowerShell script output, no PostgreSQL command output, no Odoo output

### Recommended Enhanced Logging

#### Required Log Entries (Every Process Step)
```
[2025-11-18 HH:MM:SS] [STEP] Process 1.0: Installer Initialization
[2025-11-18 HH:MM:SS] [INFO]   1.1 Logging Setup: Log file created
[2025-11-18 HH:MM:SS] [INFO]   1.2 Windows Version: 10.0 (Build 26100) - PASSED
[2025-11-18 HH:MM:SS] [INFO]   1.3 .NET Framework: 4.8 detected - PASSED
[2025-11-18 HH:MM:SS] [WARN]   1.4 Smart Detection: Script not found, using defaults
[2025-11-18 HH:MM:SS] [INFO]   1.5 Existing Database Check: No database found

[2025-11-18 HH:MM:SS] [STEP] Process 4.0: PostgreSQL Setup
[2025-11-18 HH:MM:SS] [INFO]   4.2 Initialize Database Cluster: STARTED
[2025-11-18 HH:MM:SS] [INFO]   4.2 Command: initdb -D "C:\Program Files\SAM AI\postgresql\data" -U postgres -E UTF8
[2025-11-18 HH:MM:SS] [INFO]   4.2 Output: Success. You can now start the database server using: pg_ctl start
[2025-11-18 HH:MM:SS] [OK]     4.2 Initialize Database Cluster: PASSED

[2025-11-18 HH:MM:SS] [INFO]   4.3 Start PostgreSQL Server: STARTED
[2025-11-18 HH:MM:SS] [INFO]   4.3 Command: pg_ctl -D "C:\Program Files\SAM AI\postgresql\data" start
[2025-11-18 HH:MM:SS] [INFO]   4.3 Output: waiting for server to start.... done. Server started.
[2025-11-18 HH:MM:SS] [INFO]   4.3 Validation: Running pg_isready (timeout 30s)
[2025-11-18 HH:MM:SS] [OK]     4.3 Validation: PostgreSQL accepting connections on port 5432
[2025-11-18 HH:MM:SS] [OK]     4.3 Start PostgreSQL Server: PASSED

[2025-11-18 HH:MM:SS] [INFO]   4.4 Create PostgreSQL User: STARTED
[2025-11-18 HH:MM:SS] [INFO]   4.4 Command: psql -U postgres -c "CREATE USER sam_ai_user ..."
[2025-11-18 HH:MM:SS] [INFO]   4.4 Output: CREATE ROLE
[2025-11-18 HH:MM:SS] [INFO]   4.4 Validation: Querying pg_roles for sam_ai_user
[2025-11-18 HH:MM:SS] [OK]     4.4 Validation: User sam_ai_user exists with CREATEDB privilege
[2025-11-18 HH:MM:SS] [OK]     4.4 Create PostgreSQL User: PASSED

[2025-11-18 HH:MM:SS] [ERROR]  4.5 Create PostgreSQL Database: FAILED
[2025-11-18 HH:MM:SS] [ERROR]  4.5 Command: createdb -U sam_ai_user sam_ai
[2025-11-18 HH:MM:SS] [ERROR]  4.5 Exit Code: 1
[2025-11-18 HH:MM:SS] [ERROR]  4.5 Output: createdb: error: database "sam_ai" already exists
[2025-11-18 HH:MM:SS] [ERROR]  Process 4.0: PostgreSQL Setup FAILED at step 4.5
[2025-11-18 HH:MM:SS] [INFO]   Initiating rollback...
[2025-11-18 HH:MM:SS] [INFO]   Rollback: Stopping PostgreSQL server
[2025-11-18 HH:MM:SS] [INFO]   Rollback: Dropping PostgreSQL user
[2025-11-18 HH:MM:SS] [OK]     Rollback: Complete
[2025-11-18 HH:MM:SS] [ERROR]  INSTALLATION ABORTED: PostgreSQL database creation failed
```

#### Log Level Meanings
- `[STEP]` - Major process step (1.0, 2.0, 3.0, etc.)
- `[INFO]` - Informational message (command executed, output received)
- `[OK]` - Success marker (step passed validation)
- `[WARN]` - Warning (non-critical issue, using fallback)
- `[ERROR]` - Failure (step failed, installation may abort)

#### Implementation Requirements
1. **All PowerShell Scripts Must Log:**
   - Start of execution
   - Each command executed (with full command line)
   - Command output (stdout + stderr)
   - Exit codes
   - Validation results
   - End of execution

2. **All Pascal Code Must Log:**
   - Function entry/exit
   - Conditional branches (if/else results)
   - User choices (checkbox selections, input values)
   - Error conditions

3. **Centralized Log File:**
   - All scripts write to same log file (append mode)
   - PowerShell: Add-Content to log file at each step
   - Pascal: CustomLog() function (already implemented)

4. **Timestamp Format:**
   - `[YYYY-MM-DD HH:MM:SS]` for chronological sorting

---

## Process Step Naming Convention (Recommended)

### Current State (No Convention)
Scripts are named descriptively but not numbered:
- `post_install.ps1`
- `configure_odoo.ps1`
- `register_service.ps1`

### Recommended Convention

#### Format: `[Phase]_[Step]_[Description].ps1`

**Examples:**
- `01_00_initialize_postgresql.ps1` (Process 4.0)
- `01_01_validate_postgresql.ps1` (Process 4.6)
- `02_00_initialize_odoo_database.ps1` (Process 5.0)
- `02_01_install_base_module.ps1` (Process 5.3)
- `02_02_install_samai_modules.ps1` (Process 5.4)
- `02_03_validate_modules.ps1` (Process 5.5)
- `03_00_register_windows_service.ps1` (Process 6.0)
- `03_01_validate_service.ps1` (Process 6.3)

#### Benefits:
1. **Clear execution order** - Scripts sort alphabetically in correct sequence
2. **Easy to reference** - "Check step 02_02" instead of "check configure_odoo.ps1 Phase 2"
3. **AI-proof** - New scripts must follow convention, can't accidentally break order
4. **Self-documenting** - Script name tells you where in process it runs

#### Migration Path:
1. Keep existing scripts working (don't rename immediately)
2. Create new numbered scripts that call existing scripts
3. Update ISS [Run] section to use numbered scripts
4. Test thoroughly
5. Deprecate old script names

---

## Document Maintenance

### When to Update This Document
1. **New process step added** - Add numbered section with full details
2. **Process step removed** - Mark as deprecated, don't renumber (preserve history)
3. **Process step modified** - Update break points, validation criteria
4. **New break point discovered** - Add to Break Point Analysis section
5. **Rollback mechanism changed** - Update Rollback Actions section

### Version Control
- This document should be committed to Git with installer source
- Update "Last Updated" date at top of document
- Add changelog section for major revisions

### Review Schedule
- **After every installer compilation** - Verify process flow is accurate
- **After every installation failure** - Add failure to Break Point Analysis
- **Monthly** - Review for completeness, add missing details

---

## Appendix A: File Reference

### ISS Source Files
- **Main ISS File:** `D:\SAMAI-18-SaaS\github-repos\100-samai-desktop-installer\dev_files\odoo_samai_installer.iss`
- **Dynamic Module List:** `D:\SAMAI-18-SaaS\github-repos\100-samai-desktop-installer\scripts\temp_modules.iss` (generated)

### PowerShell Scripts (Installation)
- **Pre-Build:**
  - `discover_modules.ps1` - Generate temp_modules.iss and temp_modules.txt
  - `build_installer_final.ps1` - Compile installer EXE
- **Runtime (Extracted to {tmp}, deleted after):**
  - `smart_detection.ps1` - Detect existing installations (OFTEN FAILS - GAP 2)
  - `convert_to_lightweight.ps1` - Convert existing Odoo to lightweight
- **Runtime (Permanent in {app}\sam\scripts):**
  - `post_install.ps1` - Initialize PostgreSQL (Process 4.0)
  - `configure_odoo.ps1` - Initialize Odoo database (Process 5.0)
  - `start_odoo.bat` - Start Odoo server
  - `stop_odoo.bat` - Stop Odoo server
- **Runtime (Permanent in {app}\scripts):**
  - `register_service.ps1` - Register Windows service (Process 6.0)
  - `unregister_service.ps1` - Unregister Windows service (uninstall)
  - `auto_repair_dependencies.ps1` - Fix missing Python dependencies (Process 5.3.1)
  - `cleanup_before_uninstall.ps1` - Stop processes before uninstall
  - `close_cmds.ps1` - Close orphaned CMD windows (Process 7.3)
  - `stop_odoo.ps1` - Stop Odoo server (PowerShell version)

### Python Scripts
- **Runtime:**
  - `auto_login.py` - Auto-login and open browser (Process 7.2)

### Log Files
- **Installer Log:** `D:\SAMAI-18-SaaS\github-repos\100-samai-desktop-installer\Output\SAM_AI_Installer_Log.txt`
- **PostgreSQL Log:** `{app}\logs\postgresql.log`
- **Odoo Log:** `{app}\logs\odoo.log`
- **Service Registration Log:** `{app}\logs\service_registration.log`

### Configuration Files
- **Odoo Config:** `{app}\server\odoo.conf` (defines addons_path, database settings, ports)
- **PostgreSQL Config:** `{app}\postgresql\data\postgresql.conf` (auto-generated by initdb)

---

## Appendix B: Success Criteria Checklist

Use this checklist to validate a successful installation:

### PostgreSQL Validation
- [ ] Process `postgres.exe` is running
- [ ] `pg_isready -h localhost -p 5432` returns 0
- [ ] User `sam_ai_user` exists in `pg_roles`
- [ ] Database `sam_ai` exists in `pg_database`
- [ ] `psql -U sam_ai_user -d sam_ai -c "\q"` succeeds (can connect)

### Odoo Validation
- [ ] Database `sam_ai` contains tables: `ir_module_module`, `res_users`, `res_company`
- [ ] Module `base` is in state 'installed'
- [ ] Module `web` is in state 'installed'
- [ ] Module `mail` is in state 'installed'
- [ ] All 8 SAM AI modules are in state 'installed':
  - [ ] `ai_brain`
  - [ ] `ai_sam`
  - [ ] `ai_sam_cache_manager`
  - [ ] `ai_sam_github_installer`
  - [ ] `ai_sam_intelligence`
  - [ ] `ai_sam_memory`
  - [ ] `ai_sam_messenger`
  - [ ] `github_app`

### Windows Service Validation
- [ ] Service `SAMAI-Odoo` exists (query with `sc.exe query SAMAI-Odoo`)
- [ ] Service is in `RUNNING` state
- [ ] Service startup type is `AUTO_START`

### HTTP Endpoint Validation
- [ ] `http://localhost:8069` responds (not "Connection refused")
- [ ] Response contains "Odoo" in HTML
- [ ] Login page loads without errors

### File System Validation
- [ ] `{app}\python\python.exe` exists
- [ ] `{app}\postgresql\bin\postgres.exe` exists
- [ ] `{app}\server\odoo-bin` exists
- [ ] `{app}\server\odoo\addons\base\__manifest__.py` exists (core modules)
- [ ] `{app}\addons\samai_core\ai_sam\__manifest__.py` exists (SAM AI modules)
- [ ] `{app}\logs\odoo.log` exists and is being written to

---

## 9.0 FILE DISCIPLINE MAP (AGENT GUARD RAILS)

**Purpose:** Prevent agents from creating new files and breaking hardcoded paths in .iss

**Last Updated:** 2025-11-18

---

### 🔵 CONSTANT FILES (SACRED - EDIT ONLY, NEVER CREATE NEW)

These files are **HARDCODED** in `odoo_samai_installer.iss`. Creating new files breaks the installer.

#### 🟦 Tier 1: SOURCE OF TRUTH (Touch with Extreme Caution)

**File:** `dev_files/odoo_samai_installer.iss`
- **Output:** `SAM_AI_Premium_Business_Suite_Setup.exe`
- **Purpose:** Inno Setup source that defines entire installation process
- **Referenced By:** `build_installer_final.ps1` (line 53: compiles this file)
- **Agent Rules:**
  - ✅ **CAN:** Edit process steps (lines 264-312 `[Run]` section)
  - ✅ **CAN:** Edit file extraction paths (lines 99-195 `[Files]` section)
  - ❌ **NEVER:** Create `odoo_samai_installer_v2.iss` or similar
  - ❌ **NEVER:** Duplicate or rename this file
- **Common Edits:** Add validation steps (5-10 lines), change StatusMsg text
- **Referenced in ISS_Processing_Hierarchy.md:** Sections 1.0-8.0 (entire process flow)

---

#### 🟦 Tier 2: CORE INSTALLATION SCRIPTS (Edit 5-20 Lines Max)

These scripts are called by the .iss file's `[Run]` section. Paths are hardcoded.

**1. post_install.ps1** (Process 4.0)
- **Hardcoded Path:** `{app}\sam\scripts\post_install.ps1` (line 268 in .iss)
- **Purpose:** Initialize PostgreSQL (cluster, user, database)
- **Current State:** ~300 lines (too long, needs refactoring - GAP 11)
- **Agent Rules:**
  - ✅ **CAN:** Edit validation logic (add `pg_isready` check - GAP 3)
  - ✅ **CAN:** Edit logging output (5-10 lines)
  - ❌ **NEVER:** Create `post_install_enhanced.ps1` or similar
  - ❌ **NEVER:** Rename this file
- **Typical Edit:** Add `pg_isready` validation after `pg_ctl start` (5 lines)
- **Referenced in ISS_Processing_Hierarchy.md:** Section 4.0 (PostgreSQL Setup)

**2. configure_odoo.ps1** (Process 5.0)
- **Hardcoded Path:** `{app}\sam\scripts\configure_odoo.ps1` (line 286 in .iss)
- **Purpose:** Initialize Odoo database, install modules
- **Current State:** ~300 lines (includes auto-repair logic)
- **Agent Rules:**
  - ✅ **CAN:** Edit module list (lines 249-255 - fallback modules)
  - ✅ **CAN:** Edit validation queries (add module existence check - GAP 5)
  - ❌ **NEVER:** Create `configure_odoo_v2.ps1` or similar
  - ❌ **NEVER:** Split into multiple files without updating .iss
- **Typical Edit:** Add module validation query after installation (10 lines)
- **Referenced in ISS_Processing_Hierarchy.md:** Section 5.0 (Odoo Database Initialization)

**3. register_service.ps1** (Process 6.0)
- **Hardcoded Path:** `{app}\scripts\register_service.ps1` (line 292 in .iss)
- **Purpose:** Register SAMAI-Odoo Windows service
- **Current State:** ~200 lines
- **Agent Rules:**
  - ✅ **CAN:** Edit service validation (add `sc.exe query` check - GAP 6)
  - ✅ **CAN:** Edit error messages (5 lines)
  - ❌ **NEVER:** Create `register_service_nssm.ps1` (use existing or edit this)
  - ❌ **NEVER:** Rename this file
- **Typical Edit:** Add service state validation (5-10 lines)
- **Referenced in ISS_Processing_Hierarchy.md:** Section 6.0 (Windows Service Registration)

**4. start_odoo.bat** (Process 7.1)
- **Hardcoded Path:** `{app}\sam\scripts\start_odoo.bat` (line 299 in .iss)
- **Purpose:** Start Odoo server in background
- **Current State:** ~10 lines (simple batch file)
- **Agent Rules:**
  - ✅ **CAN:** Edit startup command parameters (2-3 lines)
  - ❌ **NEVER:** Create `start_odoo.ps1` (use .bat only)
  - ❌ **NEVER:** Rename this file
- **Typical Edit:** Change from `/B` (background) to visible window (1 line)
- **Referenced in ISS_Processing_Hierarchy.md:** Section 7.1 (Launch SAM AI)

**5. auto_login.py** (Process 7.2)
- **Hardcoded Path:** `{app}\scripts\auto_login.py` (line 304 in .iss)
- **Purpose:** Auto-login and open browser to http://localhost:8069
- **Current State:** ~100 lines (Python script)
- **Agent Rules:**
  - ✅ **CAN:** Edit browser wait logic (add HTTP polling - GAP 9)
  - ❌ **NEVER:** Create `auto_login_enhanced.py`
  - ❌ **NEVER:** Rename this file
- **Typical Edit:** Add `requests.get('http://localhost:8069')` polling with 30s timeout (10 lines)
- **Referenced in ISS_Processing_Hierarchy.md:** Section 7.2 (Auto-Login)

**6. close_cmds.ps1** (Process 7.3)
- **Hardcoded Path:** `{app}\scripts\close_cmds.ps1` (line 310 in .iss)
- **Purpose:** Close orphaned CMD windows from installation
- **Current State:** ~50 lines
- **Agent Rules:**
  - ✅ **CAN:** Edit process detection logic (5 lines)
  - ❌ **NEVER:** Create `close_cmds_enhanced.ps1`
  - ❌ **NEVER:** Rename this file
- **Typical Edit:** Add additional process names to close (2-3 lines)
- **Referenced in ISS_Processing_Hierarchy.md:** Section 7.3 (Close Orphaned CMD Windows)

**7. cleanup_before_uninstall.ps1** (Uninstall Process)
- **Hardcoded Path:** `{app}\scripts\cleanup_before_uninstall.ps1` (line 325 in .iss)
- **Purpose:** Stop processes, drop database before uninstall
- **Current State:** ~200 lines
- **Agent Rules:**
  - ✅ **CAN:** Edit cleanup logic (validation checks)
  - ❌ **NEVER:** Create `cleanup_before_uninstall_v2.ps1`
  - ❌ **NEVER:** Rename this file
- **Typical Edit:** Add database drop validation (5 lines)
- **Referenced in ISS_Processing_Hierarchy.md:** Uninstall section (not documented yet - GAP 10)

**8. unregister_service.ps1** (Uninstall Process)
- **Hardcoded Path:** `{app}\scripts\unregister_service.ps1` (line 330 in .iss)
- **Purpose:** Stop and delete Windows service
- **Current State:** ~100 lines
- **Agent Rules:**
  - ✅ **CAN:** Edit service stop validation
  - ❌ **NEVER:** Create `unregister_service_v2.ps1`
  - ❌ **NEVER:** Rename this file
- **Typical Edit:** Add service state check after deletion (5 lines)
- **Referenced in ISS_Processing_Hierarchy.md:** Uninstall section (not documented yet - GAP 10)

---

#### 🟦 Tier 3: SUPPORTING SCRIPTS (Edit if Needed, But Low Priority)

These files exist but are **NOT referenced in the .iss file**. They can be edited or deleted without breaking the installer.

**Build-Time Scripts (Pre-Compilation):**
- `build_installer_final.ps1` - Compiles .iss → .exe (NOT run during install)
- `discover_modules.ps1` - Generates temp_modules.iss (NOT run during install)

**Utility Scripts (Optional, Not Currently Used):**
- `stop_odoo.bat` - Manual Odoo stop (NOT called by installer)
- `stop_odoo.ps1` - PowerShell version (NOT called by installer)
- `auto_repair_dependencies.ps1` - Called by configure_odoo.ps1 (NOT directly by .iss)
- `validate_odoo_structure.ps1` - NOT called by installer (manual validation)
- `check_odoo_logs.ps1` - NOT called by installer (manual debugging)

**Agent Rules for Tier 3:**
- ✅ **CAN:** Edit these freely (not hardcoded in .iss)
- ✅ **CAN:** Create new files in this category (e.g., `validate_installation.ps1`)
- ⚠️ **BUT:** If you create a new file, it won't run automatically (must add to .iss `[Run]` section)

---

### 🔴 INLINE COMMANDS (NO SEPARATE FILE - EDIT .ISS DIRECTLY)

These processes are executed **directly in the .iss file** using inline commands. Creating separate .ps1 files is unnecessary and breaks the installer.

**Process 4.3: Start PostgreSQL (INLINE)**
- **Location:** Line 268 in .iss (embedded in post_install.ps1 parameters)
- **Command:** `pg_ctl -D "{app}\postgresql\data" start`
- **Agent Rules:**
  - ✅ **CAN:** Edit parameters (e.g., add `-w -t 30` for timeout)
  - ❌ **NEVER:** Create `start_postgresql.ps1` (already inline in post_install.ps1)

**Process 4.4: Create Database User (INLINE)**
- **Location:** Line 268 in .iss (embedded in post_install.ps1 parameters)
- **Command:** `psql -U postgres -c "CREATE USER sam_ai_user ..."`
- **Agent Rules:**
  - ✅ **CAN:** Edit SQL command (change password, privileges)
  - ❌ **NEVER:** Create `create_db_user.ps1` (already inline in post_install.ps1)

**Process 4.5: Create Database (INLINE)**
- **Location:** Line 268 in .iss (embedded in post_install.ps1 parameters)
- **Command:** `createdb -U sam_ai_user sam_ai`
- **Agent Rules:**
  - ✅ **CAN:** Edit database name via parameters
  - ❌ **NEVER:** Create `create_database.ps1` (already inline in post_install.ps1)

**Process 5.3: Install Base Module (INLINE)**
- **Location:** Line 286 in .iss (embedded in configure_odoo.ps1 parameters)
- **Command:** `python.exe odoo-bin -c odoo.conf -d sam_ai -i base --stop-after-init`
- **Agent Rules:**
  - ✅ **CAN:** Edit module list (e.g., `-i base,web,mail`)
  - ❌ **NEVER:** Create `install_base_module.ps1` (already inline in configure_odoo.ps1)

---

### ⚠️ ROGUE FILES (AGENTS CREATED - SHOULD NOT EXIST)

These files were **created by agents** when they should have **edited existing files**. They are NOT referenced in the .iss and do nothing.

**Evidence of Rogue Creation:** 43 .ps1/.bat files in `scripts/` folder, but only **8 files** are referenced in .iss

#### Category 1: Enhanced/Example Files (Delete Immediately)
- `00_00_enhanced_logging.ps1` ← Agent created "enhanced" version instead of editing post_install.ps1
- `01_00_postgresql_setup_ENHANCED_EXAMPLE.ps1` ← Agent created example instead of editing post_install.ps1
- **Problem:** These files don't run. Installer still uses original files.
- **Fix:** Delete files, apply edits to original files (post_install.ps1, configure_odoo.ps1)

#### Category 2: Version 2 Files (Delete Immediately)
- Any file ending in `_v2.ps1`, `_enhanced.ps1`, `_improved.ps1`
- **Problem:** Creating new versions instead of editing originals
- **Example:** If `register_service_v2.ps1` exists, delete it and edit `register_service.ps1`

#### Category 3: NSSM Service Files (Deprecated, Keep for Reference)
- `register_service_nssm.ps1` - Alternative service registration using NSSM
- `test_nssm_service.ps1` - NSSM testing script
- `download_nssm.ps1` - Download NSSM utility
- `clean_and_register_nssm.ps1` - NSSM cleanup
- `fix_nssm_service.ps1` - NSSM fixes
- **Status:** NOT used in current installer (uses `sc.exe` instead)
- **Action:** Keep for historical reference, but mark as deprecated
- **If needed:** Edit `register_service.ps1` to use NSSM, don't create new files

#### Category 4: Transition/Migration Files (Delete After Use)
- `github_transition_plan.ps1` - Migration script (one-time use)
- `github_transition_with_logging.ps1` - Migration with logging
- `github_transition_log_*.txt` - Migration logs
- **Status:** Migration complete, files no longer needed
- **Action:** Archive to `scripts/archive/` folder, delete from active scripts

#### Category 5: Analysis/Documentation Files (Move to docs/)
- `how_odoo_app_cards_work.md` - Documentation (NOT a script)
- `ENHANCED_AUTO_LOGIN_GUIDE.md` - Documentation
- `deep_problem_analysis.py` - One-time analysis script
- **Problem:** Documentation files mixed with installation scripts
- **Action:** Move to `docs/` folder

#### Category 6: Module Discovery Files (Keep, But Review)
- `discover_modules.ps1` - ✅ **KEEP** (generates temp_modules.iss)
- `export_full_modules.ps1` - Review if needed
- `check_module_completeness.ps1` - Review if needed
- `analyze_lightweight_core.ps1` - Review if needed
- **Status:** Some files duplicate functionality
- **Action:** Consolidate into `discover_modules.ps1` if possible

#### Recommended Cleanup Actions:

**Immediate (Delete - High Confidence):**
```bash
# Category 1: Enhanced/Example files
rm scripts/00_00_enhanced_logging.ps1
rm scripts/01_00_postgresql_setup_ENHANCED_EXAMPLE.ps1

# Category 4: Transition files (archive first)
mkdir scripts/archive
mv scripts/github_transition*.ps1 scripts/archive/
mv scripts/github_transition*.txt scripts/archive/

# Category 5: Documentation (move to docs/)
mv scripts/how_odoo_app_cards_work.md docs/
mv scripts/ENHANCED_AUTO_LOGIN_GUIDE.md docs/
```

**Review & Delete (Medium Confidence):**
```bash
# List all files NOT referenced in .iss
# Compare against 8 CONSTANT files above
# If not in CONSTANT list AND not referenced in .iss → candidate for deletion
```

**Keep for Reference (Low Risk):**
```bash
# Category 3: NSSM files (deprecated, but may be useful later)
# Keep in scripts/ but mark as deprecated in filename
mv scripts/register_service_nssm.ps1 scripts/DEPRECATED_register_service_nssm.ps1
mv scripts/test_nssm_service.ps1 scripts/DEPRECATED_test_nssm_service.ps1
```

---

### 📋 AGENT WORKFLOW (When Asked to "Fix Installer Issue")

**WRONG WORKFLOW (Creates Rogue Files):**
```
1. Agent reads post_install.ps1
2. Agent thinks: "This file is 300 lines, too messy"
3. Agent creates: 01_00_postgresql_setup_CLEAN.ps1 (200 lines)
4. Agent thinks: "This is cleaner!"
5. User runs installer → Still uses old post_install.ps1 → Bug not fixed
```

**CORRECT WORKFLOW (Edits CONSTANT Files):**
```
1. Agent reads post_install.ps1
2. Agent identifies specific bug (e.g., missing pg_isready validation)
3. Agent reads ISS_Processing_Hierarchy.md Section 4.0
4. Agent identifies EXACT location to edit (after line 94: pg_ctl start)
5. Agent edits post_install.ps1:
   - Add 5 lines: pg_isready validation with 30s timeout
   - Update logging: "[OK] PostgreSQL accepting connections"
6. Agent reads odoo_samai_installer.iss line 268
7. Agent confirms: post_install.ps1 path is correct
8. User runs installer → Uses updated post_install.ps1 → Bug fixed
```

**Agent Rules Summary:**
1. ✅ **ALWAYS:** Read ISS_Processing_Hierarchy.md first (identify CONSTANT file)
2. ✅ **ALWAYS:** Edit CONSTANT files (post_install.ps1, configure_odoo.ps1, etc.)
3. ✅ **ALWAYS:** Verify file path matches .iss hardcoded path
4. ❌ **NEVER:** Create new .ps1 files with similar names (_v2, _enhanced, _clean)
5. ❌ **NEVER:** Rename CONSTANT files
6. ❌ **NEVER:** Split CONSTANT files into multiple files without updating .iss

---

### 🔧 FILE DISCIPLINE ENFORCEMENT (For Agents)

When agent is asked to "improve installation process":

**Step 1: Identify the Process Step**
- Read ISS_Processing_Hierarchy.md
- Find process number (e.g., Process 4.3: Start PostgreSQL)
- Identify CONSTANT file (e.g., post_install.ps1)

**Step 2: Check if File is CONSTANT**
- Is file in Section 9.0 "Tier 1" or "Tier 2" list? → YES = CONSTANT
- Is file hardcoded in odoo_samai_installer.iss [Run] section? → YES = CONSTANT

**Step 3: Edit CONSTANT File (5-20 Lines Max)**
- Open CONSTANT file for editing
- Identify EXACT line to modify
- Add validation logic (5-10 lines)
- Update logging output (2-5 lines)
- **Total edits:** <20 lines

**Step 4: Verify .iss Path (CRITICAL)**
- Open odoo_samai_installer.iss
- Find Filename: parameter for this process step
- Confirm path matches CONSTANT file location
- **If path doesn't match:** STOP, do not create new file

**Step 5: Test Installer**
- Recompile installer: `build_installer_final.ps1`
- Run installer
- Verify CONSTANT file is executed (check log)
- Verify edits work as expected

**If agent violates these rules:**
- **Penalty:** Rogue file created, installer unchanged, user frustrated
- **Correction:** Delete rogue file, edit CONSTANT file, retest

---

### 📊 CONSTANT FILES CHECKLIST (Quick Reference)

Copy this checklist when editing files:

**Before Editing:**
- [ ] File is in Section 9.0 Tier 1 or Tier 2 list
- [ ] File path matches odoo_samai_installer.iss [Run] section
- [ ] ISS_Processing_Hierarchy.md documents this process step
- [ ] Identified exact line number to edit

**During Editing:**
- [ ] Editing CONSTANT file (not creating new file)
- [ ] Edits are <20 lines
- [ ] Added validation logic (if needed)
- [ ] Updated logging output
- [ ] No file rename, no file duplication

**After Editing:**
- [ ] Verified file path still matches .iss
- [ ] Recompiled installer (build_installer_final.ps1)
- [ ] Tested installer end-to-end
- [ ] Verified log shows updated output
- [ ] No rogue files created

---

**End of File Discipline Map**

---

**End of ISS Processing Hierarchy Documentation**
