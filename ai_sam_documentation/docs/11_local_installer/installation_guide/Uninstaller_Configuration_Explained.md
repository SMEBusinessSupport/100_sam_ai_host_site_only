# Uninstaller Configuration - Inno Setup Script

**Date:** 2025-01-11
**Installer Script:** `D:\SAMAI-18-SaaS\github-repos\100-samai-desktop-installer\odoo_samai_installer.iss`

---

## 🎯 Answer: Where the Uninstaller Gets Created

### **The Uninstaller Filename is AUTOMATIC**

Inno Setup **automatically creates** the uninstaller executable. You **cannot directly name it** in the script.

### **Default Uninstaller Name:**
```
unins000.exe
```

**Location After Installation:**
```
C:\Program Files\SAM AI\unins000.exe
```

---

## 📋 Uninstaller Configuration in Script

### **Line 36 - Display Name:**
```ini
UninstallDisplayName=SAM AI Premium Business Suite
```
**Purpose:** This is the name shown in Windows "Programs and Features" (Add/Remove Programs)
**Note:** This does NOT change the uninstaller filename

### **Line 53 - Display Icon:**
```ini
UninstallDisplayIcon={app}\sam\assets\sam_ai.ico
```
**Purpose:** Icon shown in Windows "Programs and Features" list
**Result:** SAM AI icon appears next to the program name

### **Line 54 - Icon File (UNUSED):**
```ini
UninstallIconFile=D:\SAMAI-18-SaaS\github-repos\100-samai-desktop-installer\assets\sam_ai.ico
```
**Status:** This directive is **deprecated** in modern Inno Setup
**Note:** Use `UninstallDisplayIcon` instead (line 53)

---

## 🔧 How Inno Setup Creates the Uninstaller

### **Automatic Process:**

**Step 1:** During installation, Inno Setup:
- Creates `unins000.exe` in the installation directory
- Creates `unins000.dat` (uninstall data file)
- Registers the uninstaller in Windows registry

**Step 2:** The uninstaller executable name follows this pattern:
```
unins000.exe  ← First installation
unins001.exe  ← If unins000 already exists
unins002.exe  ← And so on...
```

**Step 3:** Registry entry is created at:
```
HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\{8F9B3A2C-1E4D-4F5B-9C6A-7D8E9F0A1B2C}_is1
```

---

## 📂 Installed Uninstaller Files

After installation, the following files are created:

```
C:\Program Files\SAM AI\
├── unins000.exe          ← Uninstaller executable
└── unins000.dat          ← Uninstall data (file list, registry keys, etc.)
```

**File Sizes:**
- `unins000.exe` - ~700 KB (standard Inno Setup uninstaller)
- `unins000.dat` - Varies based on installation (contains file/registry information)

---

## 🔍 Uninstaller Configuration Details

### **Line 36 - UninstallDisplayName:**
```ini
UninstallDisplayName=SAM AI Premium Business Suite
```

**What it controls:**
- ✅ Name in Windows "Programs and Features"
- ✅ Name in "Apps & Features" (Windows 10/11)
- ✅ Name in Start Menu uninstall shortcut (line 225)
- ❌ Does NOT control the .exe filename

**Example in Windows:**
```
Programs and Features:
└── SAM AI Premium Business Suite
    └── Uninstall: C:\Program Files\SAM AI\unins000.exe
```

### **Line 225 - Start Menu Shortcut:**
```ini
[Icons]
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}";
Filename: "{uninstallexe}"
```

**Result:**
```
Start Menu\Programs\SAM AI Premium Business Suite\
└── Uninstall SAM AI Premium Business Suite.lnk
    → Points to: C:\Program Files\SAM AI\unins000.exe
```

---

## ❌ Why You Can't Rename It

### **Inno Setup Design:**
Inno Setup **hardcodes** the uninstaller naming scheme:
- Always starts with `unins`
- Always uses sequential numbers (000, 001, etc.)
- Always uses `.exe` extension

### **Reasons:**
1. **Conflict Prevention** - Multiple versions can coexist
2. **Standard Behavior** - Users expect this pattern
3. **Windows Compatibility** - Registry entries use this pattern
4. **Upgrade Support** - Old uninstallers remain functional

---

## 🎨 What You CAN Customize

### **1. Display Name (Line 36):**
```ini
UninstallDisplayName=SAM AI Premium Business Suite
```
Change to:
```ini
UninstallDisplayName=SAM AI Business Suite
UninstallDisplayName=SAM AI v18.1
UninstallDisplayName=Your Custom Name Here
```

### **2. Display Icon (Line 53):**
```ini
UninstallDisplayIcon={app}\sam\assets\sam_ai.ico
```
Change to point to any `.ico` file

### **3. Start Menu Shortcut Name (Line 225):**
```ini
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}";
```
Change to:
```ini
Name: "{group}\Remove SAM AI";
Name: "{group}\Uninstall";
Name: "{group}\Remove Application";
```

---

## 🔄 Uninstall Process Configuration

### **Lines 268-271 - Pre-Uninstall Cleanup:**
```ini
[UninstallRun]
Filename: "powershell.exe";
Parameters: "-ExecutionPolicy Bypass -WindowStyle Hidden -File ""{app}\scripts\cleanup_before_uninstall.ps1"" -InstallDir ""{app}""";
Flags: runhidden waituntilterminated
```

**Purpose:** Runs a PowerShell script BEFORE uninstalling files
**Script:** `cleanup_before_uninstall.ps1`
**Actions:**
- Stops SAM AI processes
- Closes file handles
- Cleans up temporary files

### **Lines 276+ - Post-Uninstall Cleanup:**
```ini
[UninstallDelete]
Type: files; Name: "{app}\*.log"
Type: files; Name: "{app}\*.tmp"
Type: filesandordirs; Name: "{app}\filestore"
Type: filesandordirs; Name: "{app}\sessions"
```

**Purpose:** Deletes additional files/folders after standard uninstall

---

## 📊 Complete Uninstaller File Path Map

| Configuration | Script Line | Result |
|---------------|-------------|--------|
| **Executable Name** | (Automatic) | `C:\Program Files\SAM AI\unins000.exe` |
| **Data File** | (Automatic) | `C:\Program Files\SAM AI\unins000.dat` |
| **Display Name** | Line 36 | "SAM AI Premium Business Suite" |
| **Display Icon** | Line 53 | SAM AI icon in Programs list |
| **Start Menu Link** | Line 225 | "Uninstall SAM AI Premium Business Suite" |
| **Registry Key** | Line 20 (AppId) | `{8F9B3A2C-1E4D-4F5B-9C6A-7D8E9F0A1B2C}_is1` |

---

## ✅ Summary

### **Q: Where is the uninstaller.exe filename defined?**
**A:** It's **NOT defined** in the script. Inno Setup automatically creates it as `unins000.exe`.

### **Q: Can I change the uninstaller filename?**
**A:** No, the filename is hardcoded by Inno Setup.

### **Q: What CAN I customize?**
**A:** You can customize:
- **Display Name** (Line 36) - Name in Programs and Features
- **Display Icon** (Line 53) - Icon in Programs list
- **Start Menu Shortcut** (Line 225) - Shortcut name
- **Uninstall Behavior** (Lines 268-276) - Pre/post cleanup scripts

### **Q: Where will it be created?**
**A:** `C:\Program Files\SAM AI\unins000.exe` (automatically)

---

## 🔧 If You Want a Custom Uninstaller Name

### **Workaround (Not Recommended):**

You could create a wrapper script that renames it, but this would:
- ❌ Break Windows uninstall registry
- ❌ Break Start Menu shortcuts
- ❌ Break "Programs and Features" functionality
- ❌ Violate Windows installer standards

**Better Solution:** Accept the standard `unins000.exe` name and customize the **display name** instead.

---

**Script Location:** [odoo_samai_installer.iss](D:\SAMAI-18-SaaS\github-repos\100-samai-desktop-installer\odoo_samai_installer.iss)
**Key Lines:** 36 (display name), 53 (icon), 225 (shortcut)
**Analysis By:** CTO via Claude Code
