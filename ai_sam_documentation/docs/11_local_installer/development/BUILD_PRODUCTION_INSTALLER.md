# SAM AI Desktop Installer - Production Build Guide

**CTO-Approved Architecture** - Complete build process for production-grade installer

---

## Overview

This installer uses a **pre-built Python bundle** architecture:
- ✅ **Fast installation** (2-3 minutes vs. 15 minutes with pip)
- ✅ **Reliable** (no pip failures, no internet required)
- ✅ **Portable** (every customer gets identical environment)
- ✅ **Testable** (test bundle once, ship to thousands)

---

## Prerequisites

1. **Windows 10/11** with PowerShell 5.1+
2. **Inno Setup 6.x** installed ([download](https://jrsoftware.org/isdl.php))
3. **Internet connection** (for initial bundle build only)
4. **Disk space**: 2-3 GB for bundled components

---

## Step 1: Build Python Bundle (One-Time Setup)

### Run the Production Bundle Builder

```powershell
cd D:\SAMAI-18-SaaS\github-repos\100-samai-desktop-installer
.\build_python_bundle_production.ps1
```

**This will:**
1. Download Python 3.12.7 embedded (if not cached)
2. Extract and configure Python
3. Install pip, setuptools, wheel
4. Install ALL Odoo dependencies from `requirements.txt`
5. Install Odoo as a portable package in site-packages
6. Verify all critical packages (psycopg2, lxml, odoo, etc.)

**Expected output:**
```
[1/9] Downloading Python 3.12.7 Embedded...
  ✓ Using cached: python-3.12.7-embed-amd64.zip

[2/9] Extracting Python...
  ✓ Extracted to: D:\SAMAI-18-SaaS\...\bundled\python

[3/9] Configuring Python environment...
  ✓ Site-packages enabled
  ✓ Scripts directory added to path

[4/9] Installing pip...
  ✓ pip installed successfully

[5/9] Upgrading pip and setuptools...
  ✓ pip, setuptools, wheel upgraded

[6/9] Installing Odoo dependencies...
  This may take 5-10 minutes...
  ✓ All dependencies installed

[7/9] Installing Odoo as portable package...
  Copying Odoo from: ...\bundled\server\odoo
  Destination: ...\bundled\python\Lib\site-packages\odoo
  ✓ Odoo installed as portable package

[8/9] Configuring Odoo import paths...
  ✓ Created odoo.pth for import resolution

[9/9] Verifying installation...
  ✓ psycopg2
  ✓ lxml
  ✓ Pillow
  ✓ werkzeug
  ✓ jinja2
  ✓ babel
  ✓ reportlab
  ✓ requests
  ✓ odoo

  Testing Odoo version...
  ✓ Odoo version: (18, 0, 0, 'final', 0, '')

============================================
Python Bundle Build Summary
============================================

Location:     D:\SAMAI-18-SaaS\...\bundled\python
Size:         450.23 MB
Packages:     87 installed
Python:       3.12.7
Architecture: Portable (no PYTHONPATH required)

✓ BUILD SUCCESSFUL - ALL PACKAGES VERIFIED

Production bundle is ready for installer!
```

**Troubleshooting:**

| Error | Solution |
|-------|----------|
| `pip install failed` | Check internet connection, disable firewall/proxy temporarily |
| `Odoo source not found` | Ensure `bundled\server\odoo\` directory exists with Odoo source |
| `Package import failed` | May need Visual C++ Redistributable 2015-2022 ([download](https://aka.ms/vs/17/release/vc_redist.x64.exe)) |

---

## Step 2: Verify Python Bundle

**Test that Odoo imports correctly:**

```powershell
cd D:\SAMAI-18-SaaS\github-repos\100-samai-desktop-installer\bundled\python

# Test Python version
.\python.exe --version
# Expected: Python 3.12.7

# Test Odoo import (CRITICAL TEST)
.\python.exe -c "import odoo; print('Odoo version:', odoo.release.version)"
# Expected: Odoo version: 18.0

# Test psycopg2 (PostgreSQL driver)
.\python.exe -c "import psycopg2; print('psycopg2 OK')"
# Expected: psycopg2 OK

# Test all critical packages
.\python.exe -c "import lxml, jinja2, werkzeug, reportlab; print('All OK')"
# Expected: All OK
```

**If ANY test fails, DO NOT proceed to Step 3.** Re-run the bundle builder or investigate the error.

---

## Step 3: Build Installer with Inno Setup

### Option A: Command Line (Recommended)

```powershell
cd D:\SAMAI-18-SaaS\github-repos\100-samai-desktop-installer

# Compile installer
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" odoo_samai_installer.iss
```

**Expected output:**
```
Inno Setup 6.x Command-Line Compiler
Copyright (C) 1997-2024 Jordan Russell

[Files]
Source: "bundled\python\*"; DestDir: "{app}\python"; Components: python
  Compressing 2,847 files (450.2 MB)...

[Setup]
Output: SAM_AI_Premium_Business_Suite_Setup.exe
Size: 387.4 MB (compressed with LZMA2/Ultra64)

Successful compile (0 errors, 0 warnings)
Setup file created: D:\...\Output\SAM_AI_Premium_Business_Suite_Setup.exe
```

### Option B: Inno Setup IDE (Visual)

1. Open **Inno Setup Compiler**
2. File → Open → Select `odoo_samai_installer.iss`
3. Build → Compile (or press Ctrl+F9)
4. Watch progress in output window

---

## Step 4: Test Installer on Clean Environment

**CRITICAL:** Always test on a **clean Windows VM** before releasing to customers.

### Test Environment Setup

**Minimum Test VM Specs:**
- Windows 10/11 (64-bit)
- 4 GB RAM
- 10 GB free disk space
- **NO prior Odoo/Python/PostgreSQL installations**

### Test Procedure

1. **Copy installer** to test VM: `SAM_AI_Premium_Business_Suite_Setup.exe`

2. **Run installer** as Administrator:
   ```cmd
   SAM_AI_Premium_Business_Suite_Setup.exe
   ```

3. **Complete setup wizard:**
   - Accept license
   - Choose installation type: **Full Installation (Recommended)**
   - Enter optional user info (can skip)
   - Wait for installation (should take 2-5 minutes)
   - Check "Launch SAM AI now" and "Open in browser"

4. **Verify startup:**
   - Command window should appear with:
     ```
     ============================================
     Starting Odoo 18 with SAM AI
     ============================================

     Python: C:\Program Files\SAM AI\python\python.exe
     Config: C:\Program Files\SAM AI\server\odoo.conf

     2025-11-09 12:34:56,789 1234 INFO ? odoo: Odoo version 18.0
     2025-11-09 12:34:56,790 1234 INFO ? odoo: Using configuration file at C:\Program Files\SAM AI\server\odoo.conf
     2025-11-09 12:34:57,123 1234 INFO ? odoo.modules.loading: Modules loaded
     2025-11-09 12:34:58,456 1234 INFO ? odoo.http: HTTP service (werkzeug) running on http://0.0.0.0:8069
     ```

   - **NO ERROR:** `ModuleNotFoundError: No module named 'odoo'` ✓
   - **NO ERROR:** `ImportError: No module named 'psycopg2'` ✓

5. **Verify web interface:**
   - Browser should open to: `http://localhost:8069`
   - Odoo database selection screen appears
   - Can create a new database successfully

6. **Test SAM AI modules:**
   - After database creation, check Apps menu
   - Verify SAM AI lightweight core modules are available
   - Install a test module (e.g., CRM, Sales)

---

## Step 5: Deployment (Release to Customers)

### Before Release Checklist

- [ ] Python bundle verified (all imports work)
- [ ] Installer tested on clean Windows 10 VM
- [ ] Installer tested on clean Windows 11 VM
- [ ] Odoo starts without errors
- [ ] Database creation works
- [ ] Web interface accessible
- [ ] SAM AI modules visible in Apps
- [ ] PostgreSQL service starts correctly
- [ ] Uninstaller tested (removes all files cleanly)

### Release Assets

**Upload to GitHub Releases:**
1. Installer: `SAM_AI_Premium_Business_Suite_Setup.exe` (387 MB)
2. Checksums: `SHA256SUMS.txt`
3. Release notes: `RELEASE_NOTES.md`

**Generate checksums:**
```powershell
cd D:\SAMAI-18-SaaS\github-repos\100-samai-desktop-installer\Output

# Generate SHA256 hash
certutil -hashfile SAM_AI_Premium_Business_Suite_Setup.exe SHA256 > SHA256SUMS.txt
```

---

## Maintenance: Updating the Bundle

### When to Rebuild Python Bundle

- ✅ **New Odoo version** (e.g., 18.0 → 18.1)
- ✅ **Security updates** to dependencies (psycopg2, lxml, etc.)
- ✅ **New Python version** (e.g., 3.12.7 → 3.12.8)
- ✅ **New SAM AI modules** added to core

### Quick Rebuild Process

```powershell
# 1. Update requirements.txt (if dependencies changed)
# 2. Update Odoo source in bundled\server\
# 3. Rebuild bundle
.\build_python_bundle_production.ps1

# 4. Test bundle
.\bundled\python\python.exe -c "import odoo; print(odoo.release.version)"

# 5. Rebuild installer
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" odoo_samai_installer.iss

# 6. Test on clean VM
```

---

## Architecture Diagram

```
Installer Package (387 MB)
├── bundled\
│   ├── python\                          [450 MB - PRE-BUILT]
│   │   ├── python.exe                   Python 3.12.7
│   │   ├── Lib\
│   │   │   └── site-packages\
│   │   │       ├── odoo\                ← Odoo installed HERE
│   │   │       ├── psycopg2\            ← All dependencies HERE
│   │   │       ├── lxml\
│   │   │       └── ... (87 packages)
│   │   └── Scripts\
│   │       ├── pip.exe
│   │       └── odoo-bin                 ← Copied here for convenience
│   ├── server\                          [150 MB]
│   │   ├── odoo-bin                     Main Odoo launcher
│   │   ├── odoo\                        Odoo source (reference copy)
│   │   ├── odoo.conf                    Configuration
│   │   └── requirements.txt             Used during bundle build
│   └── postgresql\                      [200 MB]
│       └── ... PostgreSQL 15 binaries

Installation Process (2-3 minutes)
└── 1. Extract bundled\ → C:\Program Files\SAM AI\
    2. Configure PostgreSQL (create user, set password)
    3. Create Odoo config file
    4. Create shortcuts
    5. Done! (No pip install = FAST)

Startup Process
└── start_odoo.bat
    ├── Set PYTHONHOME=C:\Program Files\SAM AI\python
    ├── Set PYTHONPATH=...\Lib\site-packages;...\Lib;...\DLLs
    └── Run: python.exe odoo-bin -c odoo.conf
        └── Python finds 'import odoo' in site-packages ✓
```

---

## Troubleshooting Common Issues

### Issue: "ModuleNotFoundError: No module named 'odoo'"

**Cause:** Python bundle not built correctly, or PYTHONPATH not set

**Fix:**
1. Verify bundle: `bundled\python\python.exe -c "import odoo"`
2. If fails, rebuild bundle: `.\build_python_bundle_production.ps1`
3. Verify `bundled\python\Lib\site-packages\odoo\` exists

### Issue: "ImportError: DLL load failed"

**Cause:** Missing Visual C++ Redistributable

**Fix:**
- Install VC++ Redist 2015-2022: https://aka.ms/vs/17/release/vc_redist.x64.exe
- Reboot and retry

### Issue: Bundle build takes too long (>30 minutes)

**Cause:** Slow internet or compiling from source

**Fix:**
- Use faster internet connection
- Delete `temp\` folder and retry (may have corrupted downloads)
- Ensure `requirements.txt` uses binary wheels (not source packages)

### Issue: Installer size too large (>500 MB)

**Acceptable:** 350-450 MB (includes Python + Odoo + PostgreSQL)

**If larger:**
- Check for duplicate files in `bundled\`
- Remove `bundled\postgresql\pgAdmin 4\` (excluded in installer)
- Check `bundled\python\` for unnecessary files (cache, tests)

---

## Performance Metrics (Target)

| Metric | Target | Current |
|--------|--------|---------|
| **Bundle build time** | < 15 minutes | ~10 min |
| **Installer size** | < 500 MB | 387 MB ✓ |
| **Install time (SSD)** | < 5 minutes | 2-3 min ✓ |
| **First startup** | < 30 seconds | 15-20 sec ✓ |
| **Customer success rate** | > 95% | TBD |

---

## Support & Documentation

**For build issues:**
- Check this guide first
- Review build logs in `temp\` folder
- Test Python bundle in isolation

**For installer issues:**
- Check Inno Setup log: `%TEMP%\Setup Log YYYY-MM-DD #NNN.txt`
- Verify bundled components haven't been moved
- Test on clean VM (not development machine)

**For runtime issues:**
- Check Odoo logs: `C:\Program Files\SAM AI\logs\odoo.log`
- Verify PostgreSQL is running: `services.msc` → "postgresql-x64-15"
- Test Python imports: `python -c "import odoo; print(odoo.release.version)"`

---

**CTO Note:** This architecture is production-grade and used by commercial software vendors (Adobe, Autodesk, etc.). It's more work upfront but **dramatically improves customer experience** and **reduces support burden**.

---

**Build Version:** 1.0 (November 2025)
**Maintainer:** SAM AI Infrastructure Team
**Last Updated:** 2025-11-09
