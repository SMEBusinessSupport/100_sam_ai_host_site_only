# NSSM Integration Guide - Windows Service Solution

**Created:** 2025-11-16
**Purpose:** Solve Windows Service registration issues for Odoo 18
**Status:** Ready to implement

---

## Problem Summary

**Current Issue:**
- ✅ Service registers with `sc.exe`
- ❌ Service cannot START (fails immediately)
- ❌ Service doesn't support STOP/PAUSE controls
- ❌ Odoo 18 removed `--install-service` option (was available in Odoo ≤17)

**Root Cause:**
Odoo's `odoo-bin` is a Python script, not a Windows Service executable. It doesn't implement Windows Service Control Manager (SCM) API, so Windows can't manage it properly.

---

## Solution: NSSM (Non-Sucking Service Manager)

**What is NSSM?**
- Industry-standard tool for running ANY application as a Windows Service
- Wraps console applications (like Python scripts) with proper SCM integration
- Used by thousands of Windows applications
- Open source, actively maintained
- **Size:** ~350KB (tiny!)

**What NSSM Provides:**
✅ Proper START/STOP/PAUSE/RESTART controls
✅ Automatic restart on failure
✅ Service dependencies (e.g., wait for PostgreSQL)
✅ Log file rotation
✅ Graceful shutdown handling
✅ Process priority control
✅ GUI configuration editor

**Official Site:** https://nssm.cc/

---

## Implementation Steps

### Step 1: Download NSSM

**Option A: Direct Download**
```powershell
# Download NSSM 2.24 (latest stable)
Invoke-WebRequest -Uri "https://nssm.cc/release/nssm-2.24.zip" -OutFile "nssm-2.24.zip"

# Extract
Expand-Archive -Path "nssm-2.24.zip" -DestinationPath "."

# Copy 64-bit version to installer bundle
New-Item -ItemType Directory -Path "D:\SAMAI-18-SaaS\github-repos\100-samai-desktop-installer\bundled\tools" -Force
Copy-Item "nssm-2.24\win64\nssm.exe" "D:\SAMAI-18-SaaS\github-repos\100-samai-desktop-installer\bundled\tools\nssm.exe"
```

**Option B: Manual Download**
1. Visit: https://nssm.cc/download
2. Download `nssm-2.24.zip`
3. Extract `win64\nssm.exe`
4. Copy to: `D:\SAMAI-18-SaaS\github-repos\100-samai-desktop-installer\bundled\tools\nssm.exe`

**File Size:** ~350KB
**SHA256:** (verify from official site)

---

### Step 2: Update Installer (.iss file)

**File:** `dev_files\odoo_samai_installer.iss`

**Add NSSM to [Files] section:**

Find the section where tools are copied (around line 180-195), add:

```pascal
; ============================================================================
; Windows Service Manager (NSSM)
; ============================================================================
; NSSM wraps Python/Odoo as proper Windows Service (Odoo 18 removed native service support)
Source: "D:\SAMAI-18-SaaS\github-repos\100-samai-desktop-installer\bundled\tools\nssm.exe"; DestDir: "{app}\tools"; Flags: ignoreversion
```

---

### Step 3: Update Service Registration Script Reference

**File:** `dev_files\odoo_samai_installer.iss`

**Find the [Run] section** (around line 289), change:

**BEFORE:**
```pascal
Filename: "powershell.exe"; \
    Parameters: "-ExecutionPolicy Bypass -File ""{app}\scripts\register_service.ps1"" -InstallDir ""{app}"""; \
    Description: "Register SAM AI as Windows service (recommended)"; \
    StatusMsg: "Registering SAM AI as Windows service..."; \
    Flags: postinstall skipifsilent waituntilterminated; \
    Check: IsAdminInstallMode
```

**AFTER:**
```pascal
Filename: "powershell.exe"; \
    Parameters: "-ExecutionPolicy Bypass -File ""{app}\scripts\register_service_nssm.ps1"" -InstallDir ""{app}"""; \
    Description: "Register SAM AI as Windows service (recommended)"; \
    StatusMsg: "Registering SAM AI as Windows service..."; \
    Flags: postinstall skipifsilent waituntilterminated; \
    Check: IsAdminInstallMode
```

---

### Step 4: Copy New Script to Installer Bundle

**Copy the new NSSM-based script:**

```powershell
# The script already exists at:
# D:\SAMAI-18-SaaS\github-repos\100-samai-desktop-installer\scripts\register_service_nssm.ps1

# Verify it's included in .iss file [Files] section:
# Add this line if not already present:
```

**Add to .iss [Files] section:**
```pascal
Source: "D:\SAMAI-18-SaaS\github-repos\100-samai-desktop-installer\scripts\register_service_nssm.ps1"; DestDir: "{app}\scripts"; Flags: ignoreversion
```

---

### Step 5: Update Uninstall Script (Optional Enhancement)

**File:** `scripts\unregister_service.ps1`

**Add NSSM-aware cleanup:**

```powershell
# At the top of the file, add:
$nssmExe = Join-Path $InstallDir "tools\nssm.exe"

# In the service removal section, change to:
if (Test-Path $nssmExe) {
    # NSSM-installed service
    Write-Log "Removing NSSM service: $serviceName"
    & $nssmExe remove $serviceName confirm 2>&1 | Out-Null
} else {
    # Fallback to sc.exe
    & sc.exe delete $serviceName 2>&1 | Out-Null
}
```

---

## Testing the Solution

### Test 1: Manual Installation (Current System)

**Right now, you can test NSSM on your current installation:**

```powershell
# 1. Download NSSM manually and place in:
#    C:\Program Files\SAM AI\tools\nssm.exe

# 2. Run the new script:
cd "C:\Program Files\SAM AI\scripts"
.\register_service_nssm.ps1 -InstallDir "C:\Program Files\SAM AI"

# 3. Verify service:
sc query SAMAI-Odoo
Get-Service SAMAI-Odoo

# 4. Test START:
net start SAMAI-Odoo

# 5. Test STOP:
net stop SAMAI-Odoo

# 6. Test RESTART:
Restart-Service SAMAI-Odoo
```

---

### Test 2: After Building New Installer

**After integrating NSSM into the installer:**

1. Build new `samai_installer.exe`
2. Install on test machine
3. During installation, **check "Register SAM AI as Windows service"**
4. After installation:
   ```powershell
   # Service should be running
   Get-Service SAMAI-Odoo

   # Should show: Status: Running, StartType: Automatic

   # Test controls
   net stop SAMAI-Odoo   # Should work
   net start SAMAI-Odoo  # Should work
   ```

---

## Benefits of NSSM Solution

### Compared to Current `sc.exe` Method:

| Feature | Current (sc.exe) | With NSSM |
|---------|-----------------|-----------|
| Service registers | ✅ Yes | ✅ Yes |
| Service starts | ❌ No (fails) | ✅ Yes |
| START command works | ❌ No | ✅ Yes |
| STOP command works | ❌ No | ✅ Yes |
| PAUSE/RESTART works | ❌ No | ✅ Yes |
| Auto-restart on crash | ❌ No | ✅ Yes |
| Log file rotation | ❌ No | ✅ Yes |
| Service dependencies | ⚠️ Ignored | ✅ Works |
| Graceful shutdown | ❌ No | ✅ Yes |
| GUI configuration | ❌ No | ✅ Yes |

---

## NSSM Configuration (What the Script Does)

The `register_service_nssm.ps1` script configures:

**Basic Setup:**
- Service Name: `SAMAI-Odoo`
- Display Name: `SAM AI - Odoo 18`
- Startup Type: Automatic
- Executable: `{app}\python\python.exe`
- Arguments: `{app}\server\odoo-bin -c {app}\server\odoo.conf`

**Logging:**
- stdout → `C:\Program Files\SAM AI\logs\odoo_stdout.log`
- stderr → `C:\Program Files\SAM AI\logs\odoo_stderr.log`
- Automatic rotation at 10MB
- Keeps old logs

**Recovery:**
- On crash: Restart after 5 seconds
- On any exit: Restart
- Graceful shutdown: 30 second timeout
- Process priority: Normal

**Dependencies:**
- Waits for PostgreSQL service (if found)
- Can start independently if PostgreSQL not registered

---

## Manual NSSM Commands (Advanced Users)

**View all service configuration:**
```powershell
nssm dump SAMAI-Odoo
```

**Edit service with GUI:**
```powershell
nssm edit SAMAI-Odoo
# Opens a GUI window with all settings
```

**View specific setting:**
```powershell
nssm get SAMAI-Odoo AppDirectory
nssm get SAMAI-Odoo DisplayName
nssm get SAMAI-Odoo AppStdout
```

**Change setting:**
```powershell
nssm set SAMAI-Odoo AppStopMethodConsole 60000  # 60 sec shutdown timeout
nssm set SAMAI-Odoo Description "My custom description"
```

**Remove service:**
```powershell
nssm remove SAMAI-Odoo confirm
```

---

## File Locations After Integration

```
Installer Source:
D:\SAMAI-18-SaaS\github-repos\100-samai-desktop-installer\
├── bundled\
│   └── tools\
│       └── nssm.exe                    ← Add this (350KB)
└── scripts\
    ├── register_service.ps1            ← OLD (keep for reference)
    └── register_service_nssm.ps1       ← NEW (use this)

Live Installation:
C:\Program Files\SAM AI\
├── tools\
│   └── nssm.exe                        ← Installed here
├── scripts\
│   ├── register_service.ps1            ← OLD
│   └── register_service_nssm.ps1       ← NEW
└── logs\
    ├── odoo.log                        ← Odoo's own log
    ├── odoo_stdout.log                 ← NSSM stdout capture
    ├── odoo_stderr.log                 ← NSSM stderr capture
    └── service_registration.log        ← Registration script log
```

---

## Troubleshooting

### Service won't start

**Check logs:**
```powershell
# Registration log
Get-Content "C:\Program Files\SAM AI\logs\service_registration.log" -Tail 50

# Service stderr (error output)
Get-Content "C:\Program Files\SAM AI\logs\odoo_stderr.log" -Tail 50

# Service stdout
Get-Content "C:\Program Files\SAM AI\logs\odoo_stdout.log" -Tail 50
```

**Common causes:**
1. PostgreSQL not running (check dependency)
2. Port 8069 already in use
3. Database doesn't exist
4. Python path incorrect

---

### NSSM GUI not opening

```powershell
# Check if NSSM exists
Test-Path "C:\Program Files\SAM AI\tools\nssm.exe"

# Run with full path
& "C:\Program Files\SAM AI\tools\nssm.exe" edit SAMAI-Odoo
```

---

### Antivirus blocking NSSM

Some antivirus software flags NSSM as suspicious (false positive).

**Solution:**
1. Add `C:\Program Files\SAM AI\tools\nssm.exe` to AV exclusions
2. Or download NSSM from official site (verified hash)

---

## Summary - Implementation Checklist

**For AI Agent building next installer:**

- [ ] Download NSSM 2.24 from https://nssm.cc/download
- [ ] Extract `win64\nssm.exe`
- [ ] Copy to: `bundled\tools\nssm.exe`
- [ ] Update `.iss` file: Add NSSM to [Files] section
- [ ] Update `.iss` file: Change [Run] section to use `register_service_nssm.ps1`
- [ ] Verify `scripts\register_service_nssm.ps1` exists (already created)
- [ ] Build new installer
- [ ] Test on clean Windows VM

**Result:** Windows Service will work perfectly with full START/STOP/RESTART support!

---

**NSSM solves all your Windows Service issues. It's the industry-standard solution used by thousands of applications!**
