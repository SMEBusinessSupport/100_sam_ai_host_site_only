# Odoo Module Installation Debug Tools
**Created: 2025-11-28**
**Purpose: Debug hanging Odoo module installations**

---

## 📁 Files in This Directory

### 1. `test_ai_sam_simple.bat` ⭐ **START HERE - EASIEST TO USE**
**Best for:** Quick debugging without complexity
**What it does:** Runs Odoo installation with verbose logging to a file

**How to use:**
```batch
# Step 1: Double-click the file in Windows Explorer
# OR run from command line:
cd "D:\SAMAI-18-SaaS\github-repos\Tools & Scripts"
test_ai_sam_simple.bat

# Step 2: Wait until it hangs (or completes)
# Step 3: Press Ctrl+C to kill it when hung
# Step 4: Check the log file at:
#         C:\Users\total\ai_sam_verbose.log
```

**What the log tells you:**
- Last XML/CSV file being loaded before hang
- Last model being initialized
- Any error messages or warnings
- Database operations happening

**Example log output:**
```
2025-11-28 14:23:45,123 INFO odoo.modules.loading: Loading ai_sam
2025-11-28 14:23:46,456 DEBUG odoo.tools.convert: Loading data file: ai_sam/views/memory_configuration.xml
2025-11-28 14:23:47,789 DEBUG odoo.tools.convert: Processing record: view_ai_memory_config_form
[HANGS HERE - this is where you look!]
```

---

### 2. `uninstall_ai_sam.sql`
**Best for:** Cleaning up after a hung/partial installation
**What it does:** Removes ai_sam module from the database so you can retry installation

**How to use:**
```batch
# Open PowerShell or Command Prompt
cd "D:\SAMAI-18-SaaS\github-repos\Tools & Scripts"

# Set PostgreSQL password
set PGPASSWORD=odoo_password

# Run the SQL script
"C:\Program Files\PostgreSQL\15\bin\psql.exe" -U odoo_user -d samai_v3 -f uninstall_ai_sam.sql

# You should see output like:
# UPDATE 1
# DELETE 245
# name    | state       | latest_version
# --------+-------------+----------------
# ai_sam  | uninstalled | 1.0.0
```

**When to use this:**
- Before retrying a failed installation
- After killing a hung installation process
- When you need a clean slate to test changes

---

### 3. `odoo_install_debug.py` (Advanced)
**Best for:** Developers who want detailed step-by-step logging
**What it does:** Patches Odoo's internal functions to log every step

**How to use:**
```python
# This is used BY run_odoo_with_debug.py
# You don't run this directly!

# But if you want to understand what it does:
# - Patches Registry.init_models() to log each model initialization
# - Patches Graph.add_module() to log dependency resolution
# - Patches convert.convert_file() to log XML/CSV file loading
# - Creates C:\Users\total\odoo_install_debug.log
```

---

### 4. `run_odoo_with_debug.py` (Advanced)
**Best for:** Python-savvy users who want maximum detail
**What it does:** Loads the debug hooks and runs Odoo

**How to use:**
```batch
# Open Command Prompt
cd "D:\SAMAI-18-SaaS\github-repos\Tools & Scripts"

# Run with Python
"C:\Program Files\SAM AI\python\python.exe" run_odoo_with_debug.py

# Watch the console for real-time debug output
# Also check: C:\Users\total\odoo_install_debug.log
```

**What you'll see:**
```
===============================================
ODOO INSTALLATION DEBUG MODE
===============================================
Loading debug hooks...
[DEBUG] STEP: PATCHED_REGISTRY | Successfully patched Registry.init_models
[DEBUG] STEP: PATCHED_DATA_LOADING | Successfully patched convert.convert_file
[DEBUG] STEP: LOAD_DATA_FILE | ai_sam/views/memory_configuration.xml
[DEBUG] STEP: LOAD_DATA_FILE | ai_sam/data/memory_graph_platform.xml
[HANGS HERE]
```

---

## 🔍 How to Debug a Hanging Installation

### Step-by-Step Process:

#### 1️⃣ **Run the Simple Test**
```batch
test_ai_sam_simple.bat
```
- Wait 2-3 minutes
- If it doesn't complete, press `Ctrl+C` to kill it

#### 2️⃣ **Check the Log File**
Open `C:\Users\total\ai_sam_verbose.log` in a text editor

Look for the **LAST** lines before the log stops. Example:
```
2025-11-28 14:25:13 DEBUG odoo.tools.convert: Loading data file: ai_sam/views/ai_workspace_views.xml
2025-11-28 14:25:14 DEBUG odoo.tools.convert: Processing record: view_ai_workspace_form
```

This tells you: **ai_workspace_views.xml** is causing the hang!

#### 3️⃣ **Investigate the Problem File**
```
# The problem is in this file:
C:\Program Files\SAM AI\addons\samai_core\ai_sam\views\ai_workspace_views.xml

# Look at line/record mentioned in log
# Common issues:
# - References to models not in ai_sam (still in ai_brain)
# - Missing dependencies
# - Circular references
```

#### 4️⃣ **Fix the Issue**
Common fixes:
- Comment out the problematic XML file in `__manifest__.py`
- Move the referenced model from ai_brain to ai_sam
- Remove the problematic record from the XML file

#### 5️⃣ **Clean Up and Retry**
```batch
# Uninstall from database
cd "D:\SAMAI-18-SaaS\github-repos\Tools & Scripts"
set PGPASSWORD=odoo_password
"C:\Program Files\PostgreSQL\15\bin\psql.exe" -U odoo_user -d samai_v3 -f uninstall_ai_sam.sql

# Try installation again
test_ai_sam_simple.bat
```

---

## 📊 Reading Log Files - Examples

### Example 1: Successful Installation
```
2025-11-28 14:30:01 INFO odoo.modules.loading: Loading module ai_sam
2025-11-28 14:30:02 DEBUG odoo.tools.convert: Loading ai_sam/security/ir.model.access.csv
2025-11-28 14:30:03 DEBUG odoo.tools.convert: Loading ai_sam/views/sam_settings_views.xml
2025-11-28 14:30:04 INFO odoo.modules.loading: Module ai_sam loaded in 3.2s
2025-11-28 14:30:05 INFO odoo: Modules loaded.
```
✅ **Status:** SUCCESS - module loaded completely

---

### Example 2: Hung Installation (Problem File Identified)
```
2025-11-28 14:35:01 INFO odoo.modules.loading: Loading module ai_sam
2025-11-28 14:35:02 DEBUG odoo.tools.convert: Loading ai_sam/security/ir.model.access.csv
2025-11-28 14:35:03 DEBUG odoo.tools.convert: Loading ai_sam/views/ai_workspace_views.xml
2025-11-28 14:35:04 DEBUG odoo.tools.convert: Processing view record: view_ai_workspace_form
[LOG STOPS HERE - NO MORE ENTRIES]
```
❌ **Status:** HUNG
🎯 **Problem:** `ai_workspace_views.xml` at record `view_ai_workspace_form`

**Next step:** Open the XML file and find `view_ai_workspace_form` - likely references a model not in ai_sam

---

### Example 3: Error (Clear Failure)
```
2025-11-28 14:40:01 INFO odoo.modules.loading: Loading module ai_sam
2025-11-28 14:40:02 DEBUG odoo.tools.convert: Loading ai_sam/views/memory_import_wizards.xml
2025-11-28 14:40:03 ERROR odoo.tools.convert: ParseError: Model not found: ai.claude.history.importer
Traceback (most recent call last):
  File "odoo/tools/convert.py", line 234, in parse
    self._tags[rec.tag](rec, **kwargs)
KeyError: 'ai.claude.history.importer'
```
❌ **Status:** ERROR
🎯 **Problem:** Model `ai.claude.history.importer` doesn't exist
✅ **Easy fix:** Check if model was renamed or is missing

---

## 🚨 Common Problems and Solutions

### Problem 1: "Model not found: canvas.platform"
**Cause:** XML file references a model that isn't loaded yet
**Solution:**
```python
# Check if model is imported in:
# C:\Program Files\SAM AI\addons\samai_core\ai_sam\models\__init__.py

# Should contain:
from . import canvas_platform
```

---

### Problem 2: Installation hangs at specific XML file
**Cause:** XML file has circular dependency or infinite loop
**Solution:**
```python
# Comment out the file in __manifest__.py temporarily:
'data': [
    # 'views/problematic_file.xml',  # COMMENTED OUT - causing hang
]
```

---

### Problem 3: Database says module is "installed" but it's not
**Cause:** Partial/hung installation left database in bad state
**Solution:**
```batch
# Use uninstall_ai_sam.sql to clean up
cd "D:\SAMAI-18-SaaS\github-repos\Tools & Scripts"
set PGPASSWORD=odoo_password
"C:\Program Files\PostgreSQL\15\bin\psql.exe" -U odoo_user -d samai_v3 -f uninstall_ai_sam.sql
```

---

## 💡 Pro Tips

### Tip 1: Check Last 50 Lines of Log
```powershell
Get-Content "C:\Users\total\ai_sam_verbose.log" -Tail 50
```

### Tip 2: Watch Log in Real-Time
```powershell
Get-Content "C:\Users\total\ai_sam_verbose.log" -Wait
```

### Tip 3: Search for Specific Model in Log
```powershell
Select-String -Path "C:\Users\total\ai_sam_verbose.log" -Pattern "ai.workspace"
```

### Tip 4: Find All "ERROR" or "WARNING" Lines
```powershell
Select-String -Path "C:\Users\total\ai_sam_verbose.log" -Pattern "ERROR|WARNING"
```

---

## 📞 Quick Reference Card

| Task | Command |
|------|---------|
| **Test installation** | `test_ai_sam_simple.bat` |
| **View log** | Open `C:\Users\total\ai_sam_verbose.log` |
| **Uninstall module** | Run `uninstall_ai_sam.sql` with psql |
| **Kill hung process** | Press `Ctrl+C` or Task Manager → End Task |
| **Check last log lines** | `Get-Content ai_sam_verbose.log -Tail 50` |

---

## 🎓 Learning Resources

### Understanding Odoo Module Installation
1. **Module Loading Order:**
   - Dependencies loaded first
   - Python models compiled
   - Security files (ir.model.access.csv)
   - Data files (XML, CSV)
   - View files (XML)
   - Post-init hooks

2. **Common Hang Points:**
   - Circular model dependencies
   - XML views referencing missing models
   - Data files with foreign key constraints not satisfied
   - Infinite loops in computed fields

3. **How to Read Stack Traces:**
   ```
   Traceback (most recent call last):
     File "odoo/modules/loading.py", line 456  ← Start here
     File "odoo/tools/convert.py", line 234    ← Then here
   KeyError: 'ai.workspace'                    ← Root cause
   ```

---

## 📝 Change Log

**2025-11-28:** Initial creation
- Added test_ai_sam_simple.bat (simple verbose logging)
- Added uninstall_ai_sam.sql (database cleanup)
- Added odoo_install_debug.py (advanced debugging)
- Added run_odoo_with_debug.py (advanced runner)

---

**Need Help?** Check the log file first, then review the "Common Problems" section above.
