# Odoo.conf Addons Path Configuration Guide

**Date:** 2025-01-11
**Config File Location:** `D:\SAMAI-18-SaaS\github-repos\100-samai-desktop-installer\bundled\odoo-conf\odoo.conf`

---

## 📍 Where to Add/Edit Addons Path

### **File to Edit:**
```
D:\SAMAI-18-SaaS\github-repos\100-samai-desktop-installer\bundled\odoo-conf\odoo.conf
```

### **Current Configuration (Line 20):**
```ini
addons_path = __INSTALL_DIR__\server\odoo\addons,__INSTALL_DIR__\addons\sam-core,__INSTALL_DIR__\addons\user_addons
```

---

## 🔧 How to Add/Modify Addons Path

### **Current Paths:**
1. `__INSTALL_DIR__\server\odoo\addons` ← 638 Odoo core modules + 15 core modules
2. `__INSTALL_DIR__\addons\sam-core` ← SAM AI modules
3. `__INSTALL_DIR__\addons\user_addons` ← User custom modules

### **To Add a New Path:**

**Edit Line 20 and add your path (comma-separated):**

```ini
addons_path = __INSTALL_DIR__\server\odoo\addons,__INSTALL_DIR__\addons\sam-core,__INSTALL_DIR__\addons\user_addons,__INSTALL_DIR__\addons\your_new_folder
```

**Important:** Separate paths with commas (no spaces after comma in Windows paths)

---

## 📋 Installation Variable Replacement

### **What `__INSTALL_DIR__` Means:**

During installation, the installer **automatically replaces** `__INSTALL_DIR__` with the actual installation path.

**Example:**
```ini
Before (in bundled\odoo-conf\odoo.conf):
addons_path = __INSTALL_DIR__\server\odoo\addons

After installation (in C:\Program Files\SAM AI\server\odoo.conf):
addons_path = C:\Program Files\SAM AI\server\odoo\addons
```

### **How Replacement Works:**

**Installer Script (Line 114):**
```ini
Source: "D:\SAMAI-18-SaaS\github-repos\100-samai-desktop-installer\bundled\odoo-conf\odoo.conf";
DestDir: "{app}\server";
Components: core;
Flags: ignoreversion
```

**Then a post-install script replaces placeholders:**
- `__INSTALL_DIR__` → `C:\Program Files\SAM AI`
- `__ODOO_PORT__` → `8069` (or configured port)
- `__POSTGRESQL_PORT__` → `5432`
- `__DATABASE_NAME__` → `odoo` (or configured name)

---

## 🎯 Current Addons Path Breakdown

### **Path 1: `__INSTALL_DIR__\server\odoo\addons`**
**Contains:**
- 638 Odoo core modules (account, sale, mrp, etc.)
- 15 additional core modules (base, web, mail, bus, etc.) ← Added by our update

**Purpose:** Core Odoo functionality

**Installed to:** `C:\Program Files\SAM AI\server\odoo\addons\`

---

### **Path 2: `__INSTALL_DIR__\addons\sam-core`**
**Contains:**
- `ai_brain` - SAM AI Brain module
- `ai_sam` - SAM AI Framework
- `ai_sam_cache_manager` - Cache management
- `ai_sam_github_installer` - GitHub installer
- `ai_sam_intelligence` - Intelligence module
- `ai_sam_memory` - Memory management
- `ai_sam_messenger` - Messaging
- `ai_sam_ui` - User interface

**Purpose:** SAM AI core functionality

**Installed to:** `C:\Program Files\SAM AI\addons\sam-core\`

---

### **Path 3: `__INSTALL_DIR__\addons\user_addons`**
**Contains:**
- (Empty initially)
- User can add custom modules here

**Purpose:** User custom modules

**Installed to:** `C:\Program Files\SAM AI\addons\user_addons\`

---

## ⚠️ What is NOT in addons_path

### **lightweight-core Folder:**
```
C:\Program Files\SAM AI\addons\lightweight-core\
```

**NOT included in addons_path** because:
- Contains only placeholder modules (641)
- Used as catalog for GitHub installer
- Not meant to be loaded by Odoo
- Would cause errors if Odoo tried to load placeholders

---

## 🔄 How to Modify for Your Needs

### **Scenario 1: Add a New Module Folder**

**Edit Line 20:**
```ini
addons_path = __INSTALL_DIR__\server\odoo\addons,__INSTALL_DIR__\addons\sam-core,__INSTALL_DIR__\addons\user_addons,__INSTALL_DIR__\addons\custom_modules
```

**Then add to installer script:**
```ini
[Dirs]
Name: "{app}\addons\custom_modules"; Permissions: users-full
```

---

### **Scenario 2: Change Module Load Order**

**Odoo loads modules from LEFT to RIGHT**, so order matters:

**Current (Correct):**
```ini
addons_path = __INSTALL_DIR__\server\odoo\addons,__INSTALL_DIR__\addons\sam-core,__INSTALL_DIR__\addons\user_addons
```
- ✅ Core modules first (base, web, mail)
- ✅ SAM AI modules second (can extend core)
- ✅ User modules last (can extend everything)

**Wrong Order:**
```ini
addons_path = __INSTALL_DIR__\addons\user_addons,__INSTALL_DIR__\addons\sam-core,__INSTALL_DIR__\server\odoo\addons
```
- ❌ User modules can't find core dependencies

---

### **Scenario 3: Add External Module Path**

**If you want to load modules from outside the installation directory:**

```ini
addons_path = __INSTALL_DIR__\server\odoo\addons,__INSTALL_DIR__\addons\sam-core,__INSTALL_DIR__\addons\user_addons,D:\My_Custom_Modules
```

**Important:** Use absolute paths for external locations

---

## 📝 Step-by-Step: Adding a New Addons Path

### **Step 1: Edit odoo.conf Template**
**File:** `D:\SAMAI-18-SaaS\github-repos\100-samai-desktop-installer\bundled\odoo-conf\odoo.conf`

**Line 20:**
```ini
addons_path = __INSTALL_DIR__\server\odoo\addons,__INSTALL_DIR__\addons\sam-core,__INSTALL_DIR__\addons\user_addons,__INSTALL_DIR__\addons\NEW_FOLDER
```

### **Step 2: Create Directory in Installer**
**File:** `D:\SAMAI-18-SaaS\github-repos\100-samai-desktop-installer\odoo_samai_installer.iss`

**Add to `[Dirs]` section (around line 182):**
```ini
Name: "{app}\addons\NEW_FOLDER"; Permissions: users-full
```

### **Step 3: (Optional) Package Modules**
**Add to `[Files]` section:**
```ini
Source: "D:\path\to\your\modules\*";
DestDir: "{app}\addons\NEW_FOLDER";
Components: your_component_name;
Flags: ignoreversion recursesubdirs createallsubdirs
```

### **Step 4: Rebuild Installer**
```bash
iscc "D:\SAMAI-18-SaaS\github-repos\100-samai-desktop-installer\odoo_samai_installer.iss"
```

---

## ✅ Current Configuration is Correct

### **Analysis:**
Your current `addons_path` (Line 20) is **correctly configured** for:
- ✅ Loading 638 Odoo core modules
- ✅ Loading 15 additional core modules (after our update)
- ✅ Loading SAM AI modules
- ✅ Supporting user custom modules
- ✅ Correct load order (core → SAM AI → user)

### **No Changes Needed Unless:**
- You want to add additional module folders
- You want to load modules from external locations
- You have specific custom requirements

---

## 📊 Summary

| Item | Value |
|------|-------|
| **Config File** | `bundled\odoo-conf\odoo.conf` |
| **Edit Line** | Line 20 |
| **Current Paths** | 3 paths (server\odoo\addons, sam-core, user_addons) |
| **Path Separator** | Comma (`,`) |
| **Variable Placeholder** | `__INSTALL_DIR__` |
| **Replacement** | Done by post-install script |
| **Installed Location** | `C:\Program Files\SAM AI\server\odoo.conf` |

---

**File to Edit:** [bundled\odoo-conf\odoo.conf:20](D:\SAMAI-18-SaaS\github-repos\100-samai-desktop-installer\bundled\odoo-conf\odoo.conf#L20)

**Guide By:** CTO via Claude Code
