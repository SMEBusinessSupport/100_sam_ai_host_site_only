# Windows Installer (.exe) for Odoo Lightweight

**Date:** 2025-11-04
**Goal:** Create user-friendly installer - just double-click and go!

---

## User Experience We Want:

### Current (Too Hard):
```
❌ User downloads repo
❌ Installs Python
❌ Installs PostgreSQL
❌ Runs scripts
❌ Edits config files
❌ Troubleshoots errors
```

### Target (Easy):
```
✅ User downloads: odoo-lightweight-setup.exe
✅ Double-clicks installer
✅ Clicks "Next, Next, Install"
✅ Odoo running automatically
✅ Browser opens to http://localhost:8069
```

---

## Best Installer Tools for Windows

### Option 1: Inno Setup ⭐ RECOMMENDED

**Why it's best:**
- ✅ Free and open source
- ✅ Creates professional Windows installers
- ✅ Can bundle Python + PostgreSQL + Odoo
- ✅ Creates Start Menu shortcuts
- ✅ Adds to Windows Programs list
- ✅ Creates uninstaller automatically
- ✅ Custom wizard pages

**Used by:** Python, PostgreSQL, many professional apps

**Example result:**
```
odoo-lightweight-setup.exe  (200MB download)
├── Includes Python 3.10
├── Includes PostgreSQL 15 portable
├── Includes Odoo lightweight
├── Auto-configures everything
└── Creates desktop shortcut
```

**Download:** https://jrsoftware.org/isinfo.php

---

### Option 2: NSIS (Nullsoft Scriptable Install System)

**Why consider it:**
- ✅ Free and open source
- ✅ Very powerful
- ✅ Used by WinAmp, VLC, etc.

**Why maybe not:**
- ❌ More complex scripting
- ❌ Steeper learning curve

---

### Option 3: Advanced Installer

**Why consider it:**
- ✅ Professional GUI
- ✅ Easy to use

**Why maybe not:**
- ❌ Paid ($500+)
- ❌ Overkill for this project

---

## Recommended: Inno Setup Strategy

### What the Installer Will Do:

**Step 1: Welcome Screen**
```
┌────────────────────────────────────┐
│  Welcome to Odoo Lightweight Setup │
│                                    │
│  This will install:                │
│  ✓ Python 3.10                     │
│  ✓ PostgreSQL 15                   │
│  ✓ Odoo 18 Lightweight             │
│  ✓ 15 Essential Modules            │
│                                    │
│         [Next]    [Cancel]         │
└────────────────────────────────────┘
```

**Step 2: Choose Installation Folder**
```
┌────────────────────────────────────┐
│  Select Installation Location      │
│                                    │
│  C:\Program Files\Odoo Lightweight │
│                                    │
│         [Browse...]                │
│                                    │
│         [Back]    [Next]           │
└────────────────────────────────────┘
```

**Step 3: Installing Progress**
```
┌────────────────────────────────────┐
│  Installing Odoo Lightweight...    │
│                                    │
│  ▓▓▓▓▓▓▓▓▓▓░░░░░░░░░░ 50%          │
│                                    │
│  Installing PostgreSQL...          │
│                                    │
│         [Cancel]                   │
└────────────────────────────────────┘
```

**Step 4: Completion**
```
┌────────────────────────────────────┐
│  Installation Complete!            │
│                                    │
│  ✓ Odoo installed successfully     │
│  ✓ Database created                │
│  ✓ Service started                 │
│                                    │
│  □ Launch Odoo now                 │
│  □ Open Odoo in browser            │
│                                    │
│         [Finish]                   │
└────────────────────────────────────┘
```

---

## Inno Setup Script Example

**File:** `installer\odoo-lightweight-setup.iss`

```ini
; Odoo Lightweight Installer Script
; Created with Inno Setup

[Setup]
AppName=Odoo Lightweight
AppVersion=18.0
DefaultDirName={autopf}\Odoo Lightweight
DefaultGroupName=Odoo Lightweight
OutputBaseFilename=odoo-lightweight-setup
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
SetupIconFile=installer\odoo-icon.ico

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "Create desktop shortcut"; GroupDescription: "Additional icons:"
Name: "startservice"; Description: "Start Odoo service after installation"; GroupDescription: "Service:"

[Files]
; Python 3.10 portable
Source: "bundled\python-3.10-embed\*"; DestDir: "{app}\python"; Flags: recursesubdirs

; PostgreSQL 15 portable
Source: "bundled\postgresql-15-portable\*"; DestDir: "{app}\postgresql"; Flags: recursesubdirs

; Odoo Lightweight
Source: "C:\odoo-lightweight\*"; DestDir: "{app}\odoo"; Flags: recursesubdirs

[Icons]
; Desktop shortcut
Name: "{autoprograms}\Odoo Lightweight"; Filename: "{app}\start-odoo.bat"; IconFilename: "{app}\odoo-icon.ico"
Name: "{autodesktop}\Odoo Lightweight"; Filename: "{app}\start-odoo.bat"; Tasks: desktopicon; IconFilename: "{app}\odoo-icon.ico"

; Start menu items
Name: "{group}\Start Odoo"; Filename: "{app}\start-odoo.bat"
Name: "{group}\Stop Odoo"; Filename: "{app}\stop-odoo.bat"
Name: "{group}\Open Odoo (Browser)"; Filename: "http://localhost:8069"
Name: "{group}\Uninstall"; Filename: "{uninstallexe}"

[Run]
; Initialize PostgreSQL
Filename: "{app}\postgresql\bin\initdb.exe"; Parameters: "-D ""{app}\postgresql\data"" -U postgres"; StatusMsg: "Initializing database..."; Flags: runhidden

; Create Odoo database user
Filename: "{app}\postgresql\bin\psql.exe"; Parameters: "-U postgres -c ""CREATE USER odoo_user WITH PASSWORD 'odoo_password' CREATEDB;"""; StatusMsg: "Creating database user..."; Flags: runhidden

; Install Python dependencies
Filename: "{app}\python\python.exe"; Parameters: "-m pip install -r ""{app}\odoo\server\requirements.txt"""; StatusMsg: "Installing dependencies..."; Flags: runhidden

; Create odoo.conf
Filename: "{app}\create-config.bat"; StatusMsg: "Creating configuration..."; Flags: runhidden

; Start Odoo service (if selected)
Filename: "{app}\start-odoo.bat"; Description: "Start Odoo now"; Flags: postinstall skipifsilent nowait; Tasks: startservice

; Open browser
Filename: "http://localhost:8069"; Description: "Open Odoo in browser"; Flags: postinstall shellexec skipifsilent; Tasks: startservice

[UninstallRun]
; Stop Odoo before uninstalling
Filename: "{app}\stop-odoo.bat"; RunOnceId: "StopOdoo"

[Code]
// Custom Pascal script for advanced logic
procedure InitializeWizard();
begin
  // Check if PostgreSQL already installed
  // Show custom pages
  // Validate system requirements
end;
```

---

## What Gets Bundled in the Installer

### 1. Python 3.10 Embedded (~50MB)
**Download:** https://www.python.org/ftp/python/3.10.11/python-3.10.11-embed-amd64.zip

**Why embedded?**
- ✅ No system-wide installation
- ✅ Self-contained
- ✅ Won't conflict with user's Python

---

### 2. PostgreSQL 15 Portable (~150MB)
**Download:** https://www.enterprisedb.com/download-postgresql-binaries

**Why portable?**
- ✅ No system installation
- ✅ Runs from installation folder
- ✅ Easy to uninstall (just delete folder)

---

### 3. Odoo Lightweight (~118MB)
- Your `C:\odoo-lightweight\` folder
- 15 essential modules
- Placeholder catalog

---

### 4. Helper Scripts

**`start-odoo.bat`:**
```batch
@echo off
cd /d "%~dp0"
start "" postgresql\bin\pg_ctl.exe -D postgresql\data start
timeout /t 3
start "" python\python.exe odoo\server\odoo-bin -c odoo\server\odoo.conf
start http://localhost:8069
```

**`stop-odoo.bat`:**
```batch
@echo off
cd /d "%~dp0"
taskkill /F /IM python.exe
postgresql\bin\pg_ctl.exe -D postgresql\data stop
```

**`create-config.bat`:**
```batch
@echo off
cd /d "%~dp0"
set INSTALL_DIR=%~dp0
(
echo [options]
echo addons_path = %INSTALL_DIR%odoo\server\odoo\addons,%INSTALL_DIR%odoo\optional-modules\_catalog
echo db_host = localhost
echo db_port = 5432
echo db_user = odoo_user
echo db_password = odoo_password
echo data_dir = %INSTALL_DIR%sessions
) > odoo\server\odoo.conf
```

---

## Total Installer Size

| Component | Size |
|-----------|------|
| Python 3.10 Embedded | 50MB |
| PostgreSQL 15 Portable | 150MB |
| Odoo Lightweight | 118MB |
| Helper Scripts | 1MB |
| **Total** | **~320MB** |

**Result:** `odoo-lightweight-setup.exe` (~320MB download)

---

## Building the Installer

### Prerequisites:
1. **Install Inno Setup** (free)
   - Download: https://jrsoftware.org/isdl.php
   - Install: Just click through wizard

2. **Prepare bundled components:**
   ```
   installer\
   ├── bundled\
   │   ├── python-3.10-embed\     (Download Python embedded)
   │   └── postgresql-15\         (Download PostgreSQL portable)
   ├── odoo-lightweight\          (Your C:\odoo-lightweight)
   ├── scripts\
   │   ├── start-odoo.bat
   │   ├── stop-odoo.bat
   │   └── create-config.bat
   ├── odoo-icon.ico
   └── odoo-lightweight-setup.iss (Inno Setup script)
   ```

3. **Compile installer:**
   - Open `odoo-lightweight-setup.iss` in Inno Setup
   - Click "Compile"
   - Result: `odoo-lightweight-setup.exe` created!

---

## Advanced Features We Can Add

### Custom Wizard Page: License Selection

```
┌────────────────────────────────────┐
│  Choose Installation Type          │
│                                    │
│  ○ Free Version (Basic)            │
│     • 15 core modules              │
│     • 641 optional modules         │
│                                    │
│  ○ SAM AI Basic ($49/month)        │
│     • Everything in Free           │
│     • + AI Chat                    │
│                                    │
│  ○ SAM AI Enterprise ($249/month)  │
│     • Everything in Basic          │
│     • + Workflows + Memory         │
│     • Enter license key: ________  │
│                                    │
│         [Back]    [Next]           │
└────────────────────────────────────┘
```

### Auto-Update Feature
- Check for updates on GitHub
- Download and install updates
- One-click upgrade

### Module Installer Integration
- GUI for downloading optional modules
- Browse module catalog
- Click to install (downloads from GitHub)

---

## Alternative: Portable ZIP Version

**For users who don't want to "install":**

Create `odoo-lightweight-portable.zip`:
```
odoo-lightweight-portable\
├── python\                  (Python embedded)
├── postgresql\              (PostgreSQL portable)
├── odoo\                    (Your lightweight)
├── START-ODOO.bat           (Double-click to start)
└── README.txt
```

**User experience:**
1. Download ZIP
2. Extract anywhere (USB drive, Desktop, etc.)
3. Double-click `START-ODOO.bat`
4. Odoo runs!

**No installation needed!**

---

## Comparison: Installer vs Portable

| Feature | .exe Installer | .zip Portable |
|---------|----------------|---------------|
| **Ease of Use** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Professional** | ⭐⭐⭐⭐⭐ | ⭐⭐ |
| **Start Menu** | ✅ Yes | ❌ No |
| **Uninstaller** | ✅ Yes | ❌ Manual |
| **Service Integration** | ✅ Yes | ❌ No |
| **User Trust** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Development Time** | 2-3 days | 2-3 hours |

---

## Recommended Approach

### Phase 1: Create Portable Version (Quick)
**Time:** 2-3 hours
**Purpose:** Test everything works

1. Bundle Python + PostgreSQL + Odoo
2. Create START-ODOO.bat
3. Test on clean Windows machine
4. Create ZIP file

**Output:** `odoo-lightweight-portable.zip`

### Phase 2: Create Installer (Professional)
**Time:** 2-3 days
**Purpose:** Production release

1. Write Inno Setup script
2. Bundle components
3. Create custom wizard pages
4. Test installation
5. Sign installer (optional, for Windows SmartScreen)

**Output:** `odoo-lightweight-setup.exe`

---

## Next Steps

**Option A:** Create portable ZIP first (fastest way to test)
**Option B:** Jump straight to Inno Setup installer (professional)
**Option C:** I'll create both versions for you

Which would you prefer?

---

**Key Insight:** You're absolutely right - **scripts are too hard for users!**

A proper installer makes it:
- ✅ One-click installation
- ✅ Professional looking
- ✅ Windows-friendly
- ✅ Easy to distribute
- ✅ Trustworthy

**Want me to start building the portable version or the full installer?**
