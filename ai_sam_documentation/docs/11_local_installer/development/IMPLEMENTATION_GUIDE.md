# Enhanced Logging & Process Hierarchy - Implementation Guide
**Created:** 2025-11-18
**Purpose:** Step-by-step guide to implement enhanced logging and validation
**Estimated Implementation Time:** 4-6 hours

---

## What We Created

### 1. **ISS Processing Hierarchy Documentation** ([ISS_Processing_Hierarchy.md](ISS_Processing_Hierarchy.md))
   - Complete process flow from installer start to finish
   - Every step numbered (1.0, 1.1, 1.2, etc.)
   - Break points identified (where failures occur)
   - Success criteria for each step
   - Rollback actions documented

### 2. **Enhanced Logging Module** (`scripts\00_00_enhanced_logging.ps1`)
   - Centralized logging for all PowerShell scripts
   - Validation helper functions (Test-PostgreSQLReady, Test-OdooModuleInstalled, etc.)
   - Rollback helper functions (Invoke-RollbackPostgreSQL, Invoke-RollbackWindowsService)
   - Consistent log format with timestamps and severity levels

### 3. **Example Enhanced Script** (`scripts\01_00_postgresql_setup_ENHANCED_EXAMPLE.ps1`)
   - Shows how to convert existing scripts to use enhanced logging
   - Implements GAP 3 (PostgreSQL validation)
   - Implements GAP 4 (Database validation)
   - Implements GAP 7 (Rollback mechanism)

---

## Implementation Roadmap

### Phase 1: Setup Enhanced Logging (30 minutes)

#### Step 1.1: Copy Enhanced Logging Module
```powershell
# File already created at:
D:\SAMAI-18-SaaS\github-repos\100-samai-desktop-installer\scripts\00_00_enhanced_logging.ps1

# No action needed - file is ready to use
```

#### Step 1.2: Test Logging Module
```powershell
# Run this test script to verify logging works:
cd D:\SAMAI-18-SaaS\github-repos\100-samai-desktop-installer\scripts

# Create test script
@'
. .\00_00_enhanced_logging.ps1
Initialize-Logging
Log-Step "Test Process 1.0"
Log-Info "1.1" "Test Step" "STARTED"
Log-Command "1.1" "echo Hello World"
Log-Output "1.1" "Hello World"
Log-Success "1.1" "Test Step" "PASSED"
Log-Validation "1.2" "Test validation" $true "Details here"
'@ | Out-File test_logging.ps1

# Run test
powershell -ExecutionPolicy Bypass -File .\test_logging.ps1

# Check output log
Get-Content D:\SAMAI-18-SaaS\github-repos\100-samai-desktop-installer\Output\SAM_AI_Installer_Log.txt -Tail 10
```

**Expected Output:**
```
[2025-11-18 HH:MM:SS] [STEP] Test Process 1.0
[2025-11-18 HH:MM:SS] [INFO]   1.1 Test Step: STARTED
[2025-11-18 HH:MM:SS] [INFO]   1.1 Command: echo Hello World
[2025-11-18 HH:MM:SS] [INFO]   1.1 Output: Hello World
[2025-11-18 HH:MM:SS] [OK]     1.1 Test Step: PASSED
[2025-11-18 HH:MM:SS] [OK]     1.2 Validation: Test validation PASSED - Details here
```

---

### Phase 2: Convert Existing Scripts (2-3 hours)

#### Conversion Template

**Before (Old Style):**
```powershell
Write-Host "[2/4] Initializing PostgreSQL..." -ForegroundColor Yellow
& "$pgPath\bin\initdb.exe" -D $pgData -U postgres -E UTF8 --locale=C

if ($LASTEXITCODE -ne 0) {
    Write-Host "  ERROR: PostgreSQL failed to start" -ForegroundColor Red
    throw "PostgreSQL startup failed"
}

Write-Host "  PostgreSQL initialized" -ForegroundColor Green
```

**After (Enhanced Style):**
```powershell
. "$PSScriptRoot\00_00_enhanced_logging.ps1"
Initialize-Logging -InstallDir $InstallDir

Log-Info "4.2" "Initialize Database Cluster" "STARTED"

$command = "`"$pgPath\bin\initdb.exe`" -D `"$pgData`" -U postgres -E UTF8 --locale=C"
Log-Command "4.2" $command

$output = & "$pgPath\bin\initdb.exe" -D $pgData -U postgres -E UTF8 --locale=C 2>&1
$exitCode = $LASTEXITCODE

Log-Output "4.2" ($output | Out-String)
Log-ExitCode "4.2" $exitCode

if ($exitCode -ne 0) {
    Log-Error "4.2" "initdb failed with exit code $exitCode"
    Log-ProcessFailed "4.0 PostgreSQL Setup" "4.2"
    Invoke-RollbackPostgreSQL -InstallDir $InstallDir
    exit 1
}

# Validation
if (!(Test-Path $pgData)) {
    Log-Error "4.2" "PostgreSQL data directory not created"
    Log-ProcessFailed "4.0 PostgreSQL Setup" "4.2"
    exit 1
}

Log-Validation "4.2" "Data directory created" $true "$pgData"
Log-Success "4.2" "Initialize Database Cluster" "PASSED"
```

#### Scripts to Convert (Priority Order)

1. **HIGH PRIORITY:** `post_install.ps1` → Rename to `01_00_postgresql_setup.ps1`
   - Implement GAP 3 (PostgreSQL validation)
   - Implement GAP 4 (Database validation)
   - Use example script as template
   - **Time:** 60 minutes

2. **HIGH PRIORITY:** `configure_odoo.ps1` → Rename to `02_00_odoo_database_init.ps1`
   - Implement GAP 5 (Module validation)
   - Add validation for all 8 SAM AI modules
   - **Time:** 45 minutes

3. **HIGH PRIORITY:** `register_service.ps1` → Rename to `03_00_windows_service_registration.ps1`
   - Implement GAP 6 (Service validation)
   - Validate service is RUNNING before exiting
   - **Time:** 30 minutes

4. **MEDIUM PRIORITY:** `auto_repair_dependencies.ps1` → Keep name (utility script)
   - Add enhanced logging
   - **Time:** 15 minutes

5. **MEDIUM PRIORITY:** `cleanup_before_uninstall.ps1` → Keep name (utility script)
   - Add enhanced logging
   - **Time:** 15 minutes

---

### Phase 3: Update ISS File (30 minutes)

#### Step 3.1: Update [Run] Section
Change from calling old scripts to calling new numbered scripts:

**Before:**
```pascal
Filename: "powershell.exe";
    Parameters: "-ExecutionPolicy Bypass -File ""{app}\sam\scripts\post_install.ps1"" -InstallDir ""{app}"" ...";
    StatusMsg: "Configuring PostgreSQL and Odoo..."; Flags: runhidden waituntilterminated
```

**After:**
```pascal
Filename: "powershell.exe";
    Parameters: "-ExecutionPolicy Bypass -File ""{app}\scripts\01_00_postgresql_setup.ps1"" -InstallDir ""{app}"" ...";
    StatusMsg: "Process 4.0: PostgreSQL Setup..."; Flags: runhidden waituntilterminated;
    Check: CheckExitCode('Process 4.0 failed. See log for details.')
```

#### Step 3.2: Add Exit Code Checking (GAP 7 - Rollback)
Add Pascal function to check exit codes and trigger rollback:

```pascal
[Code]
function CheckExitCode(ErrorMsg: String): Boolean;
var
  ResultCode: Integer;
begin
  Result := True;

  // Get last exit code from PowerShell script
  if GetLastError() <> 0 then
  begin
    CustomLog('ERROR: ' + ErrorMsg);
    CustomLog('Exit code: ' + IntToStr(ResultCode));

    if MsgBox(ErrorMsg + #13#10#13#10 +
              'Would you like to rollback the installation?',
              mbError, MB_YESNO) = IDYES then
    begin
      // Trigger rollback here
      Result := False;
    end;
  end;
end;
```

---

### Phase 4: Testing (1-2 hours)

#### Test 1: Fresh Installation (Happy Path)
```powershell
# Prerequisites:
# - No existing SAM AI installation
# - No existing PostgreSQL
# - Run as Administrator

# Run installer
D:\SAMAI-18-SaaS\github-repos\100-samai-desktop-installer\Output\SAM_AI_Premium_Business_Suite_Setup.exe

# Expected Result:
# - All processes complete successfully
# - Log file shows all [OK] markers
# - Odoo starts and http://localhost:8069 responds

# Verify log file
Get-Content "D:\SAMAI-18-SaaS\github-repos\100-samai-desktop-installer\Output\SAM_AI_Installer_Log.txt"

# Expected log entries:
# [STEP] Process 4.0: PostgreSQL Setup
# [INFO]   4.2 Initialize Database Cluster: STARTED
# [OK]     4.2 Initialize Database Cluster: PASSED
# [INFO]   4.3 Start PostgreSQL Server: STARTED
# [OK]     4.3 Validation: PostgreSQL accepting connections on port 5432 PASSED
# [OK]     4.3 Start PostgreSQL Server: PASSED
# ... (all steps pass)
# [STEP] Process 4.0: PostgreSQL Setup COMPLETE
```

#### Test 2: Installation with Existing Database (Failure + Rollback)
```powershell
# Prerequisites:
# - SAM AI already installed
# - PostgreSQL running with sam_ai database
# - DO NOT drop database manually

# Run installer again
D:\SAMAI-18-SaaS\github-repos\100-samai-desktop-installer\Output\SAM_AI_Premium_Business_Suite_Setup.exe

# Expected Result (OLD BEHAVIOR - BAD):
# - Installer shows "Complete!" but SAM AI is broken

# Expected Result (NEW BEHAVIOR - GOOD):
# - Step 4.5 (Create Database) detects database exists
# - Log shows: [ERROR] 4.5 createdb failed with exit code 1
# - Log shows: [ERROR] Process 4.0: PostgreSQL Setup FAILED at step 4.5
# - Log shows: [STEP] ROLLBACK: PostgreSQL
# - Installer exits with error message
# - User sees: "Process 4.0 failed. See log for details."

# Verify log file
Get-Content "D:\SAMAI-18-SaaS\github-repos\100-samai-desktop-installer\Output\SAM_AI_Installer_Log.txt" -Tail 20

# Expected log entries:
# [ERROR]  4.5 Create PostgreSQL Database: FAILED
# [ERROR]  4.5 Exit Code: 1
# [ERROR]  4.5 Output: createdb: error: database "sam_ai" already exists
# [ERROR]  Process 4.0: PostgreSQL Setup FAILED at step 4.5
# [STEP]   ROLLBACK: PostgreSQL
# [INFO]   Rollback: Stopping PostgreSQL server
# [OK]     ROLLBACK: PostgreSQL stopped
# [INFO]   Rollback: Dropping database 'sam_ai'
# [OK]     ROLLBACK: Database dropped
# [OK]     ROLLBACK: PostgreSQL rollback complete
```

#### Test 3: Not Run as Administrator (GAP 1 - Admin Check)
```powershell
# Prerequisites:
# - DO NOT run as Administrator

# Run installer (double-click, NOT right-click "Run as Administrator")
D:\SAMAI-18-SaaS\github-repos\100-samai-desktop-installer\Output\SAM_AI_Premium_Business_Suite_Setup.exe

# Expected Result (OLD BEHAVIOR - BAD):
# - Service registration fails with "Access denied"
# - Installer shows "Complete!" but service not created

# Expected Result (NEW BEHAVIOR - GOOD):
# - Installer shows error message BEFORE any files are copied:
#   "SAM AI requires administrator privileges. Please right-click and select 'Run as Administrator'"
# - Installer exits immediately
# - No files copied, no rollback needed

# This requires GAP 1 fix in InitializeSetup (Pascal code)
```

#### Test 4: PostgreSQL Fails to Start (GAP 3 - PostgreSQL Validation)
```powershell
# Prerequisites:
# - System-wide PostgreSQL already running on port 5432

# Run installer
D:\SAMAI-18-SaaS\github-repos\100-samai-desktop-installer\Output\SAM_AI_Premium_Business_Suite_Setup.exe

# Expected Result (OLD BEHAVIOR - BAD):
# - PostgreSQL fails to start (port 5432 already in use)
# - Script continues, tries to create user → fails
# - Installer shows "Complete!" but PostgreSQL never started

# Expected Result (NEW BEHAVIOR - GOOD):
# - Step 4.3 (Start PostgreSQL) detects failure
# - Log shows: [ERROR] 4.3 pg_ctl start failed with exit code 1
# - Validation detects PostgreSQL not accepting connections
# - Log shows: [ERROR] 4.3 Validation: PostgreSQL accepting connections on port 5432 FAILED
# - Rollback triggered
# - Installer exits with error

# Verify log file
Get-Content "D:\SAMAI-18-SaaS\github-repos\100-samai-desktop-installer\Output\SAM_AI_Installer_Log.txt" -Tail 20
```

---

## Expected Log File Format

After full implementation, a successful installation log should look like this:

```
[2025-11-18 07:00:00] [INFO] === SAM AI Premium Business Suite Installer ===
[2025-11-18 07:00:00] [INFO] Starting installer initialization...
[2025-11-18 07:00:00] [INFO] Log file location: D:\...\SAM_AI_Installer_Log.txt

[2025-11-18 07:00:01] [STEP] Process 1.0: Installer Initialization
[2025-11-18 07:00:01] [INFO]   1.1 Logging Setup: Log file created
[2025-11-18 07:00:01] [INFO]   1.2 Windows Version: 10.0 (Build 26100)
[2025-11-18 07:00:01] [OK]     1.2 Windows version check: PASSED
[2025-11-18 07:00:01] [INFO]   1.3 .NET Framework: 4.8 detected
[2025-11-18 07:00:01] [OK]     1.3 .NET Framework check: PASSED
[2025-11-18 07:00:01] [WARN]   1.4 Smart Detection: Script not found, using defaults
[2025-11-18 07:00:01] [INFO]   1.5 Existing Database Check: No database found
[2025-11-18 07:00:01] [OK]     Process 1.0: Installer Initialization COMPLETE

[2025-11-18 07:00:02] [STEP] Process 4.0: PostgreSQL Setup
[2025-11-18 07:00:02] [INFO]   4.0 Install Directory: C:\Program Files\SAM AI
[2025-11-18 07:00:02] [INFO]   4.0 Database Name: sam_ai
[2025-11-18 07:00:02] [INFO]   4.0 PostgreSQL Port: 5432

[2025-11-18 07:00:02] [INFO]   4.1 Cleanup Existing Processes: STARTED
[2025-11-18 07:00:02] [INFO]   4.1 No Python processes found
[2025-11-18 07:00:02] [INFO]   4.1 No PostgreSQL processes found
[2025-11-18 07:00:02] [OK]     4.1 Cleanup Existing Processes: PASSED

[2025-11-18 07:00:03] [INFO]   4.2 Initialize Database Cluster: STARTED
[2025-11-18 07:00:03] [INFO]   4.2 Command: "C:\Program Files\SAM AI\postgresql\bin\initdb.exe" -D "C:\Program Files\SAM AI\postgresql\data" -U postgres -E UTF8 --locale=C
[2025-11-18 07:00:05] [INFO]   4.2 Output: Success. You can now start the database server using: pg_ctl start
[2025-11-18 07:00:05] [INFO]   4.2 Exit Code: 0
[2025-11-18 07:00:05] [OK]     4.2 Validation: Data directory created PASSED - C:\Program Files\SAM AI\postgresql\data
[2025-11-18 07:00:05] [OK]     4.2 Validation: Configuration files created PASSED - postgresql.conf, pg_hba.conf
[2025-11-18 07:00:05] [OK]     4.2 Initialize Database Cluster: PASSED

[2025-11-18 07:00:06] [INFO]   4.3 Start PostgreSQL Server: STARTED
[2025-11-18 07:00:06] [INFO]   4.3 Command: "C:\Program Files\SAM AI\postgresql\bin\pg_ctl.exe" -D "C:\Program Files\SAM AI\postgresql\data" -l "C:\Program Files\SAM AI\logs\postgresql.log" start -w -t 30
[2025-11-18 07:00:10] [INFO]   4.3 Output: waiting for server to start.... done. Server started.
[2025-11-18 07:00:10] [INFO]   4.3 Exit Code: 0
[2025-11-18 07:00:10] [INFO]   4.3 Validation: PostgreSQL Server Readiness: Testing...
[2025-11-18 07:00:12] [OK]     4.3 Validation: PostgreSQL accepting connections on port 5432 PASSED - Waited 2 seconds
[2025-11-18 07:00:12] [OK]     4.3 Start PostgreSQL Server: PASSED

[2025-11-18 07:00:12] [INFO]   4.4 Create PostgreSQL User: STARTED
[2025-11-18 07:00:12] [INFO]   4.4 Command: "C:\Program Files\SAM AI\postgresql\bin\psql.exe" -U postgres -c "CREATE USER sam_ai_user WITH PASSWORD 'samai_secure_pass' CREATEDB;"
[2025-11-18 07:00:13] [INFO]   4.4 Output: CREATE ROLE
[2025-11-18 07:00:13] [INFO]   4.4 Exit Code: 0
[2025-11-18 07:00:13] [INFO]   4.4 Validation: PostgreSQL User Exists: Querying pg_roles...
[2025-11-18 07:00:13] [OK]     4.4 Validation: User 'sam_ai_user' exists PASSED
[2025-11-18 07:00:13] [OK]     4.4 Create PostgreSQL User: PASSED

[2025-11-18 07:00:14] [INFO]   4.5 Create PostgreSQL Database: STARTED
[2025-11-18 07:00:14] [INFO]   4.5 Command: "C:\Program Files\SAM AI\postgresql\bin\createdb.exe" -U sam_ai_user -E UTF8 -O sam_ai_user sam_ai
[2025-11-18 07:00:15] [INFO]   4.5 Exit Code: 0
[2025-11-18 07:00:15] [INFO]   4.5 Validation: PostgreSQL Database Exists: Querying pg_database...
[2025-11-18 07:00:15] [OK]     4.5 Validation: Database 'sam_ai' exists PASSED
[2025-11-18 07:00:15] [OK]     4.5 Create PostgreSQL Database: PASSED

[2025-11-18 07:00:16] [INFO]   4.6 Validate PostgreSQL Setup: STARTED
[2025-11-18 07:00:16] [INFO]   4.6 Validation: PostgreSQL Connection: Testing user can connect to database...
[2025-11-18 07:00:16] [OK]     4.6 Validation: User 'sam_ai_user' can connect to 'sam_ai' PASSED
[2025-11-18 07:00:16] [OK]     4.6 Validate PostgreSQL Setup: PASSED

[2025-11-18 07:00:16] [STEP] Process 4.0: PostgreSQL Setup COMPLETE
[2025-11-18 07:00:16] [INFO]   4.0 PostgreSQL server is running and accepting connections
[2025-11-18 07:00:16] [INFO]   4.0 Database 'sam_ai' is ready for Odoo initialization
[2025-11-18 07:00:16] [OK]     4.0 PostgreSQL Setup: PASSED

[2025-11-18 07:00:17] [STEP] Process 5.0: Odoo Database Initialization
... (continues for all processes)
```

---

## Maintenance Guidelines

### When to Update Documentation
1. **New process step added** → Update ISS_Processing_Hierarchy.md
2. **Validation function added** → Update 00_00_enhanced_logging.ps1
3. **Break point discovered** → Add to ISS_Processing_Hierarchy.md "Break Point Analysis" section
4. **Rollback mechanism changed** → Update both documentation and logging module

### How to Add New Validation Function
```powershell
# Template for new validation function in 00_00_enhanced_logging.ps1

function Test-<YourValidation> {
    param(
        [string]$Parameter1,
        [int]$TimeoutSeconds = 30
    )

    Log-Info "VALIDATE" "<Validation Name>" "Testing..."

    try {
        # Your validation logic here
        $validationResult = $false

        # Example: Check if something exists
        if (Test-Path $Parameter1) {
            $validationResult = $true
        }

        Log-Validation "VALIDATE" "<Validation Name>" $validationResult "Details here"
        return $validationResult
    } catch {
        Log-Validation "VALIDATE" "<Validation Name>" $false "Query failed: $($_.Exception.Message)"
        return $false
    }
}
```

### How to Add New Rollback Function
```powershell
# Template for new rollback function in 00_00_enhanced_logging.ps1

function Invoke-Rollback<Component> {
    param(
        [string]$InstallDir
    )

    Log-Step "ROLLBACK: <Component Name>"

    # Step 1: Stop processes
    try {
        Log-Rollback "Stopping <component> processes"
        # Your stop logic here
        Log-Success "ROLLBACK" "<Component> stopped"
    } catch {
        Log-Warning "ROLLBACK" "Failed to stop <component>: $($_.Exception.Message)"
    }

    # Step 2: Delete resources
    try {
        Log-Rollback "Deleting <component> resources"
        # Your delete logic here
        Log-Success "ROLLBACK" "<Component> resources deleted"
    } catch {
        Log-Warning "ROLLBACK" "Failed to delete resources: $($_.Exception.Message)"
    }

    Log-Success "ROLLBACK" "<Component> rollback complete"
}
```

---

## Benefits of This Implementation

### For Developers:
1. **Debugging is trivial** - Log file shows exact failure point with command, output, exit code
2. **No more guessing** - Every step validated, no assumptions
3. **Rollback works** - Partial installations cleaned up automatically
4. **Consistent structure** - All scripts follow same pattern

### For Users:
1. **Clear error messages** - "Process 4.0 failed at step 4.3: PostgreSQL not accepting connections"
2. **No broken installations** - Rollback returns system to pre-install state
3. **Faster support** - User can send log file, support can instantly see what failed
4. **Confidence** - Every [OK] marker means that step actually worked

### For AI Agents:
1. **Self-documenting** - Process numbers match documentation exactly
2. **Can't break order** - Numbered files sort correctly
3. **Validation catches mistakes** - If AI writes buggy code, validation fails loudly
4. **Log file is truth** - No more "did it work?" uncertainty

---

## Troubleshooting

### Issue: "Initialize-Logging: File not found"
**Cause:** Script can't find 00_00_enhanced_logging.ps1

**Fix:**
```powershell
# Ensure script is dot-sourced with correct path
. "$PSScriptRoot\00_00_enhanced_logging.ps1"

# If that fails, use absolute path
. "D:\SAMAI-18-SaaS\github-repos\100-samai-desktop-installer\scripts\00_00_enhanced_logging.ps1"
```

### Issue: "Log file not created"
**Cause:** Permission denied or directory doesn't exist

**Fix:**
```powershell
# Manually create logs directory
New-Item -ItemType Directory -Path "C:\Program Files\SAM AI\logs" -Force

# Or specify alternate log location
Initialize-Logging -InstallDir "C:\Temp"
```

### Issue: "Validation functions always return false"
**Cause:** PostgreSQL not running or incorrect credentials

**Fix:**
```powershell
# Test PostgreSQL manually
& "C:\Program Files\SAM AI\postgresql\bin\psql.exe" -U sam_ai_user -d sam_ai

# If fails, check PostgreSQL log
Get-Content "C:\Program Files\SAM AI\logs\postgresql.log" -Tail 50
```

---

## Next Steps

1. **Complete Phase 1** - Test enhanced logging module (30 minutes)
2. **Complete Phase 2** - Convert post_install.ps1 first (1 hour)
3. **Test converted script** - Verify logs look correct (30 minutes)
4. **Iterate** - Convert remaining scripts one at a time

**Total Time to Full Implementation:** 4-6 hours spread over 2-3 days

---

**Document Owner:** SAM AI Installer Team
**Last Updated:** 2025-11-18
**Status:** Ready for implementation

---

*"With great logging comes great debuggability."*
