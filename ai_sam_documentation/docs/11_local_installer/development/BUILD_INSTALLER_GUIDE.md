# Building the Odoo Lightweight Installer

**Date:** 2025-11-04
**Purpose:** Step-by-step guide to build `odoo-lightweight-setup.exe`

---

## Prerequisites

### 1. Install Inno Setup
- **Download:** https://jrsoftware.org/isdl.php
- **Version:** 6.2.2 or later
- **Install:** Run installer, accept defaults
- **Location:** `C:\Program Files (x86)\Inno Setup 6\`

### 2. Download Required Components

You need to download these components and place them in the `installer\bundled\` folder:

#### Python 3.10 Embedded (50MB)
```
Download: https://www.python.org/ftp/python/3.10.11/python-3.10.11-embed-amd64.zip
Extract to: installer\bundled\python-3.10-embed\
```

**What you should see:**
```
installer\bundled\python-3.10-embed\
├── python.exe
├── python310.dll
├── python310.zip
├── pythonw.exe
└── ... (other files)
```

#### PostgreSQL 15 Portable (150MB)
```
Download: https://www.enterprisedb.com/download-postgresql-binaries
Version: PostgreSQL 15.x (Windows x64 binaries)
Extract to: installer\bundled\postgresql-15\
```

**What you should see:**
```
installer\bundled\postgresql-15\
├── bin\
│   ├── postgres.exe
│   ├── psql.exe
│   ├── pg_ctl.exe
│   └── initdb.exe
├── lib\
└── share\
```

---

## Folder Structure

Before building, your `installer\` folder should look like this:

```
C:\Users\total\installer\
├── bundled\
│   ├── python-3.10-embed\          (50MB - Python runtime)
│   └── postgresql-15\              (150MB - PostgreSQL binaries)
├── scripts\
│   ├── start-odoo.bat              ✅ Created
│   ├── stop-odoo.bat               ✅ Created
│   ├── create-config.bat           ✅ Created
│   └── open-browser.bat            ✅ Created
├── assets\
│   ├── odoo-icon.ico               ⚠️ Need to create/download
│   └── README.txt                  ✅ Created
├── odoo-lightweight-setup.iss      ✅ Created
└── BUILD_INSTALLER_GUIDE.md        ✅ This file
```

---

## Step-by-Step Build Process

### Step 1: Prepare Python Embedded

1. **Download Python:**
   ```powershell
   # Open PowerShell
   cd C:\Users\total\installer\bundled

   # Download Python embedded
   Invoke-WebRequest -Uri "https://www.python.org/ftp/python/3.10.11/python-3.10.11-embed-amd64.zip" -OutFile "python-3.10.11-embed-amd64.zip"

   # Extract
   Expand-Archive -Path "python-3.10.11-embed-amd64.zip" -DestinationPath "python-3.10-embed"
   ```

2. **Enable pip in embedded Python:**

   Edit `python-3.10-embed\python310._pth` and uncomment this line:
   ```
   import site
   ```

   (Remove the `#` at the beginning of the line)

3. **Get pip:**
   ```powershell
   cd python-3.10-embed

   # Download get-pip.py
   Invoke-WebRequest -Uri "https://bootstrap.pypa.io/get-pip.py" -OutFile "get-pip.py"

   # Install pip
   .\python.exe get-pip.py
   ```

### Step 2: Prepare PostgreSQL Portable

1. **Download PostgreSQL binaries:**
   - Visit: https://www.enterprisedb.com/download-postgresql-binaries
   - Select: **PostgreSQL 15.x** (Windows x64)
   - Download the ZIP file (not the installer!)

2. **Extract:**
   ```powershell
   cd C:\Users\total\installer\bundled

   # Extract the downloaded ZIP
   Expand-Archive -Path "postgresql-15.x-windows-x64-binaries.zip" -DestinationPath "."

   # Rename folder
   Rename-Item "pgsql" "postgresql-15"
   ```

### Step 3: Create/Download Odoo Icon

**Option 1: Use existing Odoo icon**
```powershell
# If you have Odoo installed, copy its icon
copy "C:\Program Files\Odoo 18\server\odoo\addons\web\static\img\favicon.ico" "C:\Users\total\installer\assets\odoo-icon.ico"
```

**Option 2: Create a simple icon**
- Use an online ICO converter: https://convertio.co/png-ico/
- Upload any Odoo logo PNG
- Download as .ico
- Save to: `C:\Users\total\installer\assets\odoo-icon.ico`

**Option 3: Skip icon (temporary)**
- Comment out icon lines in the `.iss` script:
  ```ini
  ; SetupIconFile=assets\odoo-icon.ico
  ; UninstallDisplayIcon={app}\assets\odoo-icon.ico
  ```

### Step 4: Verify Folder Structure

Run this PowerShell command to check everything is ready:

```powershell
cd C:\Users\total\installer

# Check Python
if (Test-Path "bundled\python-3.10-embed\python.exe") {
    Write-Host "✅ Python found" -ForegroundColor Green
} else {
    Write-Host "❌ Python missing!" -ForegroundColor Red
}

# Check PostgreSQL
if (Test-Path "bundled\postgresql-15\bin\postgres.exe") {
    Write-Host "✅ PostgreSQL found" -ForegroundColor Green
} else {
    Write-Host "❌ PostgreSQL missing!" -ForegroundColor Red
}

# Check Odoo
if (Test-Path "C:\odoo-lightweight\server\odoo-bin") {
    Write-Host "✅ Odoo lightweight found" -ForegroundColor Green
} else {
    Write-Host "❌ Odoo lightweight missing!" -ForegroundColor Red
}

# Check scripts
if (Test-Path "scripts\start-odoo.bat") {
    Write-Host "✅ Scripts found" -ForegroundColor Green
} else {
    Write-Host "❌ Scripts missing!" -ForegroundColor Red
}
```

### Step 5: Build the Installer

**Method 1: Using Inno Setup GUI**
1. Open Inno Setup Compiler
2. File > Open > Select `odoo-lightweight-setup.iss`
3. Build > Compile
4. Wait for compilation (2-5 minutes)
5. Installer created: `installer\Output\odoo-lightweight-setup.exe`

**Method 2: Using Command Line**
```powershell
cd C:\Users\total\installer

# Compile installer
& "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" "odoo-lightweight-setup.iss"
```

### Step 6: Test the Installer

**IMPORTANT:** Test on a clean Windows machine or VM!

1. **Copy installer to test machine:**
   - Copy `Output\odoo-lightweight-setup.exe` to test PC

2. **Run installer:**
   - Double-click `odoo-lightweight-setup.exe`
   - Follow wizard
   - Choose installation type (Standard or Full)
   - Wait for installation (~5-15 minutes depending on components)

3. **Verify installation:**
   - Desktop shortcut created?
   - Start Odoo works?
   - Browser opens to http://localhost:8069?
   - Can create a database?

4. **Test uninstall:**
   - Control Panel > Programs > Uninstall Odoo Lightweight
   - Verify clean removal

---

## Troubleshooting

### Issue: "Cannot find python.exe"
**Solution:** Check that Python is in `bundled\python-3.10-embed\python.exe`

### Issue: "Cannot find PostgreSQL"
**Solution:** Check that PostgreSQL is in `bundled\postgresql-15\bin\postgres.exe`

### Issue: "Icon file not found"
**Solution:** Either create the icon or comment out icon lines in `.iss` file

### Issue: "Pip install fails during installation"
**Solution:**
1. Make sure you enabled `import site` in `python310._pth`
2. Make sure pip was installed in embedded Python

### Issue: "PostgreSQL initdb fails"
**Solution:** Make sure you downloaded PostgreSQL **binaries** (not installer)

### Issue: "Installer size too large (>500MB)"
**Solution:** This is normal! Components are:
- Python: 50MB
- PostgreSQL: 150MB
- Odoo: 118MB
- **Total: ~320MB**

---

## Customization Options

### Change Installation Directory
Edit `.iss` file:
```ini
DefaultDirName={autopf}\Odoo Lightweight
```
Change to:
```ini
DefaultDirName=C:\Odoo
```

### Skip Memory System Component
Users can choose during installation. Default is included in "Full" install.

### Add License Agreement
Add to `.iss` file:
```ini
[Setup]
LicenseFile=assets\LICENSE.txt
```

### Change Default Database Password
Edit `scripts\create-config.bat`:
```batch
echo db_password = odoo_password
```
Change to:
```batch
echo db_password = YourSecurePassword123
```

---

## Distribution

### Upload to GitHub Releases

```powershell
# Create release on GitHub
gh release create v18.0 `
  Output\odoo-lightweight-setup.exe `
  --title "Odoo Lightweight v18.0" `
  --notes "First public release of Odoo Lightweight installer"
```

### Share Download Link
```
https://github.com/yourorg/odoo-18-core-lightweight/releases/download/v18.0/odoo-lightweight-setup.exe
```

---

## Maintenance

### Update Python Version
1. Download new Python embedded version
2. Replace `bundled\python-3.10-embed\` folder
3. Rebuild installer

### Update PostgreSQL Version
1. Download new PostgreSQL binaries
2. Replace `bundled\postgresql-15\` folder
3. Update version in `.iss` file
4. Rebuild installer

### Update Odoo
1. Update `C:\odoo-lightweight\` folder
2. Rebuild installer

---

## Installer Statistics

| Component | Size | Installation Time |
|-----------|------|-------------------|
| Python 3.10 | 50MB | 30 seconds |
| PostgreSQL 15 | 150MB | 1 minute |
| Odoo Core | 118MB | 1 minute |
| Python Dependencies (Standard) | ~5MB download | 2 minutes |
| Python Dependencies (with Memory) | ~2GB download | 10-15 minutes |
| **Total (Standard)** | **~325MB** | **~5 minutes** |
| **Total (Full)** | **~2.3GB** | **~15 minutes** |

---

## Next Steps

After building the installer:

1. ✅ Test on clean Windows 10/11 machine
2. ✅ Test on VM with no internet (verify offline functionality)
3. ✅ Test uninstall process
4. ✅ Create GitHub release
5. ✅ Write installation documentation
6. ✅ Share with test users

---

## File Checklist

Before building, verify these files exist:

- [ ] `bundled\python-3.10-embed\python.exe`
- [ ] `bundled\python-3.10-embed\python310._pth` (with `import site` uncommented)
- [ ] `bundled\postgresql-15\bin\postgres.exe`
- [ ] `bundled\postgresql-15\bin\initdb.exe`
- [ ] `bundled\postgresql-15\bin\pg_ctl.exe`
- [ ] `bundled\postgresql-15\bin\psql.exe`
- [ ] `scripts\start-odoo.bat`
- [ ] `scripts\stop-odoo.bat`
- [ ] `scripts\create-config.bat`
- [ ] `scripts\open-browser.bat`
- [ ] `assets\README.txt`
- [ ] `assets\odoo-icon.ico` (optional)
- [ ] `odoo-lightweight-setup.iss`
- [ ] `C:\odoo-lightweight\server\odoo-bin`

---

**Ready to build? Follow the steps above and create your installer!**
