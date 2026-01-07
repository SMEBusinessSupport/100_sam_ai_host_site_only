# SAM AI Installer - Phase 1 Testing Instructions

**Date:** 2025-11-18
**Version:** Phase 1 Complete (Install + Uninstall Gaps)
**Status:** Ready to Test

---

## 🎯 WHAT TO TEST

Phase 1 implements:
- ✅ 6 critical INSTALL gaps (1, 3, 4, 5, 6, 7)
- ✅ 4 critical UNINSTALL gaps (1, 2, 3, 7)

Total gaps fixed: **10 out of 17** (59% coverage, 100% of critical gaps)

---

## 📋 PRE-REQUISITES

### Before Testing:
1. **Clean Machine State:**
   - No existing SAM AI installation
   - No existing SAM AI services
   - No existing `sam_ai` PostgreSQL database
   - Port 5432 available (not in use by system PostgreSQL)
   - Port 8069 available (not in use by other web servers)

2. **Verify Clean State:**
   ```powershell
   # Check for existing services
   Get-Service -Name "*odoo*","*samai*" -ErrorAction SilentlyContinue

   # Check for existing databases (if you have system PostgreSQL)
   # psql -U postgres -l | findstr sam_ai

   # Check ports
   netstat -ano | findstr ":5432"
   netstat -ano | findstr ":8069"
   ```

3. **If NOT Clean:**
   - Uninstall SAM AI from Control Panel
   - Manually drop `sam_ai` database if it exists
   - Reboot machine to ensure all processes stopped

---

## 🧪 TEST 1: HAPPY PATH (FULL CYCLE)

**Purpose:** Verify the complete install → verify → uninstall → verify → reinstall cycle works flawlessly.

### Step 1: Build Installer (if not already built)

```powershell
cd D:\SAMAI-18-SaaS\github-repos\100-samai-desktop-installer\scripts
.\discover_modules.ps1
cd ..\dev_files
.\build_installer_final.ps1
```

**Wait for build to complete** (5-10 minutes). You should see:
```
Successful compile
```

**Installer Location:**
```
D:\SAMAI-18-SaaS\github-repos\100-samai-desktop-installer\Output\SAM_AI_Premium_Business_Suite_Setup.exe
```

### Step 2: Install SAM AI

1. **Right-click installer** → **Run as Administrator**
2. **Follow prompts** (accept defaults)
3. **Wait for completion** (5-10 minutes)

**Expected:**
- Installer completes without errors
- Shows "Installation Complete!" message
- Browser opens to `http://localhost:8069`

### Step 3: Verify Installation

```powershell
# Check logs
Get-Content "C:\Program Files\SAM AI\logs\SAM_AI_Installer_Log.txt" -Tail 100

# Expected: All [OK] markers, no [ERROR] markers
```

**Validate 6 Installation Gaps Fixed:**

#### GAP 1: Admin Rights Check
```powershell
# This was checked BEFORE installation started
# If you got this far without error, GAP 1 PASSED
```
✅ Expected: Installer runs without "Access denied" errors

#### GAP 3: PostgreSQL Validation
```powershell
# Check PostgreSQL is running and accepting connections
& "C:\Program Files\SAM AI\postgresql\bin\pg_isready.exe" -h localhost -p 5432
```
✅ Expected: "accepting connections"

#### GAP 4: Database Validation
```powershell
# Check database exists
$env:PGPASSWORD='samai_secure_pass'
& "C:\Program Files\SAM AI\postgresql\bin\psql.exe" -U sam_ai_user -d postgres -c "SELECT 1 FROM pg_database WHERE datname='sam_ai'"
Remove-Item Env:\PGPASSWORD
```
✅ Expected: Returns "1"

#### GAP 5: Module Validation
```powershell
# Check all 11 modules installed
$env:PGPASSWORD='samai_secure_pass'
& "C:\Program Files\SAM AI\postgresql\bin\psql.exe" -U sam_ai_user -d sam_ai -c "SELECT name, state FROM ir_module_module WHERE name IN ('base', 'web', 'mail', 'ai_brain', 'ai_sam', 'ai_sam_cache_manager', 'ai_sam_github_installer', 'ai_sam_intelligence', 'ai_sam_memory', 'ai_sam_messenger', 'github_app')"
Remove-Item Env:\PGPASSWORD
```
✅ Expected: All 11 modules with state='installed'

#### GAP 6: Service Validation
```powershell
# Check service is RUNNING
Get-Service -Name "SAMAI-Odoo" | Select-Object Name, Status, StartType
```
✅ Expected: Status=Running, StartType=Automatic

#### GAP 7: Rollback Mechanism
```
# This gap is tested in failure scenarios (Test 2-6)
# If install succeeded without errors, rollback wasn't needed
```

### Step 4: Verify Odoo Works

1. **Open browser:** `http://localhost:8069`
2. **Login:**
   - Username: `admin`
   - Password: `admin`
3. **Navigate to Apps**
4. **Verify SAM AI modules visible**

✅ Expected: Odoo loads, can login, SAM AI modules present

### Step 5: Uninstall SAM AI

1. **Control Panel** → **Programs and Features**
2. **Find "SAM AI Premium Business Suite"**
3. **Uninstall**
4. **Wait for completion** (2-3 minutes)

**Expected:**
- Uninstaller completes without errors
- Shows completion message

### Step 6: Verify Uninstallation

```powershell
# Check uninstall logs
Get-Content "C:\Program Files\SAM AI\logs\uninstall.log" -Tail 100

# Expected: All [OK] markers, no [ERROR] markers
```

**Validate 4 Uninstallation Gaps Fixed:**

#### UNINSTALL GAP 1: Service Stop Validation
```powershell
# Check service deleted
Get-Service -Name "SAMAI-Odoo" -ErrorAction SilentlyContinue
```
✅ Expected: No service found

#### UNINSTALL GAP 2: PostgreSQL Stop Validation
```powershell
# Check no PostgreSQL processes running
Get-Process -Name "postgres","pg_ctl" -ErrorAction SilentlyContinue | Where-Object { $_.Path -like "C:\Program Files\SAM AI*" }
```
✅ Expected: No processes found

#### UNINSTALL GAP 3: Database Drop Validation (CRITICAL!)
```powershell
# This is the CRITICAL gap that prevents Issue #27

# If you have system PostgreSQL, check database dropped:
# $env:PGPASSWORD='samai_secure_pass'
# psql -U sam_ai_user -d postgres -c "SELECT 1 FROM pg_database WHERE datname='sam_ai'"
# Remove-Item Env:\PGPASSWORD

# Expected: No rows returned (database does not exist)

# If no system PostgreSQL, skip this check
```
✅ Expected: Database 'sam_ai' does NOT exist

#### UNINSTALL GAP 7: Uninstall Logging
```powershell
# Check uninstall log exists and has content
Test-Path "C:\Program Files\SAM AI\logs\uninstall.log"
```
✅ Expected: Log file exists with detailed uninstall actions

### Step 7: Verify Clean State

```powershell
# Check installation directory removed
Test-Path "C:\Program Files\SAM AI"

# Check no SAM AI services
Get-Service -Name "*odoo*","*samai*" -ErrorAction SilentlyContinue

# Check ports released
netstat -ano | findstr ":5432"
netstat -ano | findstr ":8069"
```

✅ Expected:
- Installation directory removed (except user_addons if it exists)
- No SAM AI services
- Ports 5432 and 8069 not in use

### Step 8: Immediate Reinstall (Tests Issue #27 Fix!)

**This is the CRITICAL test for UNINSTALL GAP 3!**

1. **Right-click installer** → **Run as Administrator** (AGAIN)
2. **Follow prompts** (accept defaults)
3. **Watch for database initialization step**

✅ Expected:
- Installer does NOT hang at "Initializing database..."
- Installer does NOT show "database already exists" error
- Installer completes successfully

**If installer hangs or fails → UNINSTALL GAP 3 FAILED (Issue #27 reproduced)**

### Step 9: Verify Reinstallation

Repeat **Step 3** (Verify Installation) and **Step 4** (Verify Odoo Works)

✅ Expected: Everything works exactly as it did in the first install

---

## 📊 TEST 1 SUCCESS CRITERIA

**PASS if:**
1. ✅ Install completes without errors
2. ✅ All 6 install gap validations pass
3. ✅ Odoo accessible at `http://localhost:8069`
4. ✅ Can login with admin/admin
5. ✅ SAM AI modules visible in Apps
6. ✅ Uninstall completes without errors
7. ✅ All 4 uninstall gap validations pass
8. ✅ Clean state verified (no services, no databases, no processes)
9. ✅ **Immediate reinstall completes without errors (NO Issue #27!)**
10. ✅ Reinstalled Odoo works perfectly

**FAIL if ANY:**
- ❌ Installer fails or hangs
- ❌ Any [ERROR] markers in install log
- ❌ PostgreSQL not accepting connections
- ❌ Database not created or modules not installed
- ❌ Service not running
- ❌ Odoo not accessible
- ❌ Uninstaller fails or hangs
- ❌ Any [ERROR] markers in uninstall log
- ❌ Service or database remains after uninstall
- ❌ **Reinstall hangs at database initialization (Issue #27)**
- ❌ Reinstall fails with "database already exists" error

---

## 🧪 TEST 2: NO ADMIN RIGHTS (GAP 1 Test)

**Purpose:** Verify installer detects missing admin rights and fails gracefully.

### Steps:

1. **Double-click installer** (do NOT right-click → Run as Administrator)
2. **Observe behavior**

✅ Expected:
- Installer shows error message:
  ```
  SAM AI requires administrator privileges to install.

  Please right-click the installer and select "Run as Administrator".

  Installation cannot continue without admin rights because:
    - Windows service registration requires admin access
    - PostgreSQL initialization requires admin access
    - System PATH modifications require admin access
  ```
- Installer exits immediately
- No files copied to `C:\Program Files\SAM AI`
- No services created
- No databases created

❌ FAIL if:
- Installer starts copying files
- Installer attempts to create service without admin rights
- Generic "Access denied" error without explanation

---

## 🧪 TEST 3: POSTGRESQL PORT IN USE (GAP 3 Test)

**Purpose:** Verify installer detects PostgreSQL port conflict and fails gracefully.

### Pre-requisites:
- System PostgreSQL installed and running on port 5432
- OR another application using port 5432

### Steps:

1. **Start system PostgreSQL** (or other application on port 5432)
2. **Verify port in use:**
   ```powershell
   netstat -ano | findstr ":5432"
   ```
3. **Run installer as admin**
4. **Wait for PostgreSQL setup step**

✅ Expected:
- Installer detects port conflict
- Error message:
  ```
  PostgreSQL server failed to accept connections within 30 seconds
  Check PostgreSQL log: C:\Program Files\SAM AI\logs\postgresql.log
  ```
- Rollback triggered (GAP 7):
  ```
  ROLLBACK: PostgreSQL stopped
  ROLLBACK: Database dropped
  ROLLBACK: PostgreSQL rollback complete
  ```
- Installer exits cleanly
- No partial installation remains

❌ FAIL if:
- Installer continues despite port conflict
- Installer hangs indefinitely
- Partial installation remains (files, services, databases)

---

## 🧪 TEST 4: DATABASE DROP FAILS ON UNINSTALL (GAP 3 Test - CRITICAL!)

**Purpose:** Verify uninstaller detects database drop failure and warns user about Issue #27.

### Steps:

1. **Install SAM AI successfully**
2. **Simulate database lock:**
   ```powershell
   # Open a connection to the database and keep it open
   $env:PGPASSWORD='samai_secure_pass'
   & "C:\Program Files\SAM AI\postgresql\bin\psql.exe" -U sam_ai_user -d sam_ai
   # Leave this window open
   ```
3. **In another PowerShell window, uninstall SAM AI**
4. **Observe uninstall log**

✅ Expected:
- Uninstaller attempts to drop database
- Validation fails
- Error message in log:
  ```
  [ERROR] VALIDATION FAILED: Database 'sam_ai' still exists after drop
  [ERROR] CRITICAL: This will cause Issue #27 on reinstall!
  [ERROR] The installer will hang because the database already exists.
  [ERROR] Manual fix required:
  [ERROR]   Option 1: Drop database manually:
  [ERROR]     $env:PGPASSWORD='samai_secure_pass'
  [ERROR]     & 'C:\Program Files\SAM AI\postgresql\bin\dropdb.exe' -U sam_ai_user sam_ai
  ```
- Uninstaller continues (doesn't exit)
- User warned about manual cleanup needed

❌ FAIL if:
- Uninstaller reports success despite database remaining
- No warning about Issue #27
- No manual fix instructions

---

## 📝 LOGGING AND DEBUGGING

### Install Logs:
```
C:\Program Files\SAM AI\logs\SAM_AI_Installer_Log.txt
C:\Program Files\SAM AI\logs\service_registration.log
C:\Program Files\SAM AI\logs\postgresql.log
C:\Program Files\SAM AI\logs\odoo.log
```

### Uninstall Logs:
```
C:\Program Files\SAM AI\logs\uninstall.log
```

### Log Format:
```
[2025-11-18 07:00:00] [INFO] === SAM AI Premium Business Suite Installer ===
[2025-11-18 07:00:00] [OK]   Administrator privileges check: PASSED
[2025-11-18 07:00:14] [OK]   4.3 Validation: PostgreSQL accepting connections on port 5432 PASSED
[2025-11-18 07:05:08] [OK]   5.5 Validation: Module 'ai_sam' installed PASSED
[2025-11-18 07:05:14] [OK]   6.4 Validation: Service 'SAMAI-Odoo' is RUNNING PASSED
```

### What to Look For:
- ✅ `[OK]` markers = validation passed
- ❌ `[ERROR]` markers = failure point
- ⚠️ `[WARN]` markers = potential issue
- 📝 `[INFO]` markers = informational

---

## 🏆 PHASE 1 SUCCESS DEFINITION

**Phase 1 is successful if:**

1. ✅ **Test 1 (Happy Path Full Cycle) passes completely**
   - Install works
   - All 6 install gaps validated
   - Odoo accessible and functional
   - Uninstall works
   - All 4 uninstall gaps validated
   - Clean state verified
   - **Immediate reinstall works (no Issue #27!)**

2. ✅ **Test 2 (No Admin) passes**
   - Clear error message
   - No partial installation

3. ✅ **Test 3 (Port Conflict) passes**
   - Detects failure
   - Triggers rollback
   - Clean exit

4. ✅ **Test 4 (Database Drop Fails) passes**
   - Detects failure
   - Warns about Issue #27
   - Provides manual fix instructions

**If all 4 tests pass → Phase 1 COMPLETE! 🎉**

**Next Step:** Decide whether to move to Phase 2 (build quality) or Phase 3 (perfect outcome)

---

## 🐛 WHAT TO DO IF TESTS FAIL

### If Install Fails:

1. **Check install log** for exact failure point
2. **Note the step number** (e.g., "4.3 Start PostgreSQL Server")
3. **Capture error message**
4. **Check if rollback occurred**
5. **Report back with:**
   - Failure step
   - Error message
   - Log file excerpt (10 lines before and after error)

### If Uninstall Fails:

1. **Check uninstall log** for exact failure point
2. **Check if database still exists**
3. **Check if service still running**
4. **Report back with:**
   - Failure step
   - Error message
   - Database status (exists or not)
   - Service status (running or not)
   - Log file excerpt

### If Reinstall Fails (Issue #27):

1. **THIS IS CRITICAL - UNINSTALL GAP 3 FAILED**
2. **Check if database was dropped** in uninstall log
3. **Report back with:**
   - Uninstall log (full)
   - Reinstall error message
   - Database status before reinstall

---

## ⏱️ EXPECTED TEST TIME

- **Test 1 (Happy Path Full Cycle):** 30 minutes
  - Build: 5-10 minutes
  - Install: 5-10 minutes
  - Verify: 5 minutes
  - Uninstall: 2-3 minutes
  - Verify: 2 minutes
  - Reinstall: 5-10 minutes

- **Test 2 (No Admin):** 2 minutes
- **Test 3 (Port Conflict):** 10 minutes
- **Test 4 (Database Drop Fails):** 15 minutes

**Total:** ~1 hour for all 4 tests

---

*"From bullshit bugs and Issue #27 to bulletproof installer in 3.5 hours of development. Now let's see if it actually works!"* 🚀
