# Installer Testing Guide

## Your Question: Testing on Multiple Machines

You asked about testing on:
1. Your dev PC (has Odoo installed with many components)
2. Your other PC
3. Your Windows laptop

Here's the strategy:

---

## Testing Strategy

### Phase 1: Pre-Installation Check (Current Dev PC)

**Run the diagnostic first - NO CHANGES:**

```powershell
powershell -ExecutionPolicy Bypass -File "C:\Users\total\installer\scripts\pre_install_check.ps1"
```

This will show you:
- Existing Python installations
- Existing PostgreSQL
- Existing Odoo
- Port conflicts
- Disk space
- Everything that might conflict

**Save the output** - it's valuable documentation.

---

### Phase 2: Laptop Testing (RECOMMENDED FIRST)

**Why start here:**
- Cleanest environment
- No dev clutter
- Real "customer experience"
- Can retry easily

**Steps:**

1. **Document baseline:**
```powershell
# Check what's installed
python --version 2>&1
pg_config --version 2>&1
git --version 2>&1

# Save to file
systeminfo > laptop_baseline.txt
```

2. **Run installer**
   - Install to `C:\Program Files\Odoo 18\`
   - Let it complete
   - Watch for errors

3. **Verify installation:**
```powershell
# Check Python isolation
"C:\Program Files\Odoo 18\Python312\python.exe" --version

# Check package location
"C:\Program Files\Odoo 18\Python312\python.exe" -c "import sys; print('\n'.join(sys.path))"

# Should show ONLY paths under C:\Program Files\Odoo 18\

# Verify critical packages
"C:\Program Files\Odoo 18\Python312\python.exe" -c "import psycopg2; print(f'psycopg2: {psycopg2.__file__}')"
"C:\Program Files\Odoo 18\Python312\python.exe" -c "import lxml; print(f'lxml: {lxml.__file__}')"

# Start Odoo
"C:\Program Files\Odoo 18\scripts\start_odoo.bat"
```

4. **Test functionality:**
   - Access http://localhost:8069
   - Create database
   - Login
   - Check App Store menu
   - Browse module catalog
   - Try installing one small module from GitHub

5. **Document issues:**
```powershell
# Save logs
copy "C:\Program Files\Odoo 18\logs\odoo.log" laptop_test_log.txt

# Save installation check
powershell -ExecutionPolicy Bypass -File "C:\Program Files\Odoo 18\scripts\pre_install_check.ps1" > laptop_post_install_check.txt
```

---

### Phase 3: Other PC Testing (SECOND)

**Why second:**
- Different hardware
- Unknown baseline
- Good second data point

**Follow same steps as laptop**

Compare results:
- Installation time
- Package verification
- Any errors/warnings
- Performance differences

---

### Phase 4: Dev PC Testing (LAST - If at all)

**Options:**

#### Option A: Side-by-Side Install (SAFEST)

Install to different location with different ports:

```
Existing: C:\Program Files\Odoo 18\     (port 8069)
New:      C:\Program Files\Odoo 18 Test\ (port 8070)
```

Modify installer to use:
- Different install dir
- Port 8070 (Odoo)
- Port 5433 (PostgreSQL if bundling)

#### Option B: VM Install (RECOMMENDED)

1. Create Windows VM
2. Snapshot before install
3. Test installer
4. Can rollback and retry

#### Option C: Uninstall Current Odoo (HIGH RISK)

**Only do this AFTER successful laptop + other PC tests**

**Before uninstalling:**

1. **Backup everything:**
```powershell
# Document current setup
"C:\Program Files\Odoo 18\Python312\python.exe" --version > dev_pc_python.txt
"C:\Program Files\Odoo 18\Scripts\pip.exe" list > dev_pc_packages.txt
copy "C:\Program Files\Odoo 18\config\odoo.conf" dev_pc_odoo.conf

# Backup databases
pg_dump -U odoo_user -d your_database -f dev_pc_database_backup.sql

# Backup custom modules
xcopy "C:\Program Files\Odoo 18\user_addons" "D:\Backups\odoo_user_addons\" /E /I /H

# Backup filestore
xcopy "C:\Program Files\Odoo 18\filestore" "D:\Backups\odoo_filestore\" /E /I /H
```

2. **Uninstall cleanly:**
```powershell
# Stop Odoo service
Stop-Service odoo* -ErrorAction SilentlyContinue

# Uninstall via Control Panel or:
# Remove installation directory
Remove-Item "C:\Program Files\Odoo 18" -Recurse -Force

# Leave PostgreSQL if you want to keep databases
# Or uninstall PostgreSQL too for complete clean slate
```

3. **Clean environment:**
```powershell
# Remove from PATH if added
# (Check: sysdm.cpl → Advanced → Environment Variables)

# Clear temp files
Remove-Item "$env:TEMP\odoo*" -Recurse -Force -ErrorAction SilentlyContinue
```

4. **Install new version**

5. **Restore data if needed:**
```powershell
# Restore database
psql -U odoo_user -d new_database -f dev_pc_database_backup.sql

# Restore custom modules
copy "D:\Backups\odoo_user_addons\*" "C:\Program Files\Odoo 18\user_addons\"

# Restore filestore
copy "D:\Backups\odoo_filestore\*" "C:\Program Files\Odoo 18\filestore\"
```

---

## What to Test

### 1. Installation

- [ ] Installer runs without admin prompt issues
- [ ] Pre-install check runs and shows results
- [ ] All files extracted correctly
- [ ] Python bundle in correct location
- [ ] PostgreSQL configured
- [ ] Odoo config file created
- [ ] Services created (if applicable)
- [ ] Desktop shortcuts created
- [ ] Start menu entries created

### 2. Python Isolation

- [ ] Bundled Python at `C:\Program Files\Odoo 18\Python312\`
- [ ] Python version is 3.12.x
- [ ] No PATH pollution (system python vs bundled)
- [ ] All packages in bundled Python's site-packages
- [ ] psycopg2 found in bundled Python
- [ ] lxml found in bundled Python
- [ ] Pillow found in bundled Python

**Test script:**
```powershell
# This should ONLY show paths under C:\Program Files\Odoo 18\
"C:\Program Files\Odoo 18\Python312\python.exe" -c "import sys; [print(p) for p in sys.path]"

# This should show bundled package locations
"C:\Program Files\Odoo 18\Python312\python.exe" -c "import psycopg2; import lxml; import PIL; print('OK')"
```

### 3. Odoo Functionality

- [ ] Odoo starts without errors
- [ ] Web interface accessible (http://localhost:8069)
- [ ] Can create database
- [ ] Can login
- [ ] 16 full modules available immediately
- [ ] App Store menu visible
- [ ] Module Catalog shows 641 modules
- [ ] Can sync registry
- [ ] Placeholder modules show "Install from GitHub" button
- [ ] Full modules show "Installed" status

### 4. GitHub Integration

- [ ] GitHub CLI installed and in path
- [ ] Can authenticate: `gh auth status`
- [ ] Can clone private repo (test with one module)
- [ ] Module downloads to `user_addons/`
- [ ] Module registers in Odoo
- [ ] Module installs successfully
- [ ] Module works as expected

### 5. Performance

- [ ] Installation time (target: <20 minutes)
- [ ] Odoo startup time (target: <30 seconds)
- [ ] Database creation time (target: <5 minutes)
- [ ] Module installation time (target: 1-2 minutes)
- [ ] Web interface responsiveness

---

## Common Issues & Solutions

### Issue: Python Package Not Found

**Symptom:**
```
ModuleNotFoundError: No module named 'psycopg2'
```

**Diagnosis:**
```powershell
# Which Python is running?
where python

# What's in sys.path?
python -c "import sys; print(sys.path)"
```

**Solution:**
- Ensure start script uses explicit path:
  `"C:\Program Files\Odoo 18\Python312\python.exe"`
- NOT just `python` (which might find system Python)

---

### Issue: PostgreSQL Connection Failed

**Symptom:**
```
psycopg2.OperationalError: could not connect to server
```

**Diagnosis:**
```powershell
# Is PostgreSQL running?
Get-Service postgresql*

# Can we connect?
& "C:\Program Files\PostgreSQL\15\bin\psql.exe" -U odoo_user -d postgres
```

**Solution:**
- Check PostgreSQL service is running
- Verify connection details in odoo.conf
- Check firewall (allow localhost)

---

### Issue: Port Already in Use

**Symptom:**
```
OSError: [WinError 10048] Only one usage of each socket address
```

**Diagnosis:**
```powershell
# What's using port 8069?
netstat -ano | findstr :8069
```

**Solution:**
- Stop other Odoo instance
- OR change port in odoo.conf
- OR use Task Manager to kill process

---

### Issue: GitHub Authentication Failed

**Symptom:**
```
fatal: could not read Username for 'https://github.com'
```

**Solution:**
```powershell
# Authenticate GitHub CLI
gh auth login

# Or configure git credentials
git config --global credential.helper manager
```

---

## Test Results Template

```markdown
# Installation Test Results

**Machine:** [Laptop / Other PC / Dev PC]
**Date:** [Date]
**Tester:** [Name]

## Environment Baseline
- Windows Version:
- Existing Python: Yes/No - Version:
- Existing PostgreSQL: Yes/No - Version:
- Existing Odoo: Yes/No - Version:
- Disk Space: XX GB free

## Installation
- Installer ran: ✓/✗
- Installation time: XX minutes
- Errors during install: None / [List]
- Warnings: None / [List]

## Python Verification
- Bundled Python location: ✓/✗
- Python version: 3.12.x ✓/✗
- psycopg2 found: ✓/✗
- lxml found: ✓/✗
- PATH pollution: None/[List issues]

## Odoo Functionality
- Odoo starts: ✓/✗
- Web accessible: ✓/✗
- Database created: ✓/✗
- Login works: ✓/✗
- App Store visible: ✓/✗
- Module count: 641 ✓/✗

## GitHub Integration
- gh CLI works: ✓/✗
- Can authenticate: ✓/✗
- Test module installed: ✓/✗
- Installation time: XX minutes

## Performance
- Odoo startup: XX seconds
- Page load time: XX seconds
- Overall responsiveness: Good/Fair/Poor

## Issues Found
1. [Issue description]
2. [Issue description]

## Recommendations
- [What worked well]
- [What needs improvement]
- [Blockers for production use]
```

---

## Recommendation for You

Based on your situation:

1. **First:** Run `pre_install_check.ps1` on your dev PC
   - See what conflicts exist
   - Document current state
   - NO changes yet

2. **Second:** Test on your Windows laptop (cleanest environment)
   - Full installation
   - Complete testing
   - Document everything

3. **Third:** Test on your other PC
   - Verify results consistent
   - Different hardware validation

4. **Fourth:** Decide on dev PC:
   - If laptop + other PC = success → Consider dev PC install
   - If issues found → Fix first
   - Option: VM on dev PC instead of uninstall

**Don't uninstall your dev Odoo until you have working installations on at least 2 other machines!**

---

## Next Steps After Testing

Once testing passes:

1. **Document the process**
   - What worked
   - What failed
   - How long each step took

2. **Create troubleshooting guide**
   - Based on real issues encountered
   - Solutions that worked

3. **Refine installer**
   - Fix identified issues
   - Add more checks
   - Improve error messages

4. **Prepare for production**
   - Final installer build
   - User documentation
   - Support materials