# New Installer Testing Checklist (Version 18.1.19.0)

**Date**: 2025-11-25
**Installer Version**: 18.1.19.0 (Database Locale Fix)

---

## Pre-Installation Steps

### 1. Uninstall Current SAM AI
- [ ] Uninstall SAM AI via Windows Settings
- [ ] Stop and remove SAMAI-Odoo service (should happen automatically)

### 2. Clean PostgreSQL Data
- [ ] Delete: `C:\Program Files\SAM AI\postgresql\data`
- [ ] This forces fresh PostgreSQL initialization with correct locale

### 3. Optional: Stop Existing PostgreSQL 15
- [ ] If you have PostgreSQL 15 at `C:\Program Files\PostgreSQL\15`
- [ ] Stop the service (installer will detect wrong locale and skip it)

---

## Installation Steps

### 4. Run New Installer
- [ ] Launch new SAM_AI_Setup_18.1.19.0.exe
- [ ] Watch for Step 0: Welcome page should open **ONCE** (not twice!)
- [ ] Watch installation progress (PostgreSQL, Python, Service registration)
- [ ] Installation should complete without errors

---

## Post-Installation Validation

### 5. Check Database Locale (CRITICAL!)
Run this command:
```powershell
powershell -ExecutionPolicy Bypass -File "C:\Users\total\check_locale.ps1"
```

**Expected Result**:
```
datname | datcollate | datctype
--------+------------+----------
sam_ai  | C          | C         ✅
```

**BOTH must be 'C'** (not English_Australia.1252)

---

### 6. Check PostgreSQL Cluster Locale
Create this script: `C:\Users\total\check_cluster_locale.ps1`
```powershell
$env:PGPASSWORD = "postgres"
& "C:\Program Files\SAM AI\postgresql\bin\psql.exe" -U postgres -d postgres -c "SHOW lc_collate;"
& "C:\Program Files\SAM AI\postgresql\bin\psql.exe" -U postgres -d postgres -c "SHOW lc_ctype;"
Remove-Item Env:\PGPASSWORD -ErrorAction SilentlyContinue
```

Run it:
```powershell
powershell -ExecutionPolicy Bypass -File "C:\Users\total\check_cluster_locale.ps1"
```

**Expected Result**:
```
lc_collate: C
lc_ctype: C
```

---

### 7. Check Template Databases
Create this script: `C:\Users\total\check_templates.ps1`
```powershell
$env:PGPASSWORD = "postgres"
& "C:\Program Files\SAM AI\postgresql\bin\psql.exe" -U postgres -d postgres -c "SELECT datname, datcollate, datctype FROM pg_database WHERE datname LIKE 'template%' ORDER BY datname;"
Remove-Item Env:\PGPASSWORD -ErrorAction SilentlyContinue
```

Run it:
```powershell
powershell -ExecutionPolicy Bypass -File "C:\Users\total\check_templates.ps1"
```

**Expected Result**:
```
   datname   | datcollate | datctype
-------------+------------+----------
 template0   | C          | C
 template1   | C          | C
```

---

### 8. Test Module Installation Speed (THE BIG TEST!)

Once SAM AI is running, install a standard Odoo module:

1. Open browser: `http://localhost:8069`
2. Log in to Odoo
3. Go to Apps
4. Search for "hr" (Human Resources)
5. Click Install
6. **Time it** ⏱️

**Expected Result**:
- ✅ Installation completes in **30-60 seconds**
- ❌ If it takes 11+ minutes, database locale is still wrong

---

### 9. Test ai_sam Module Installation

1. Go to Apps
2. Update Apps List
3. Search for "SAM AI"
4. Click Install on `ai_sam` module
5. **Time it** ⏱️

**Expected Result**:
- ✅ Installation completes in **< 1 minute**
- ✅ No filesystem hangs
- ✅ No database deadlocks
- ✅ Clean installation with minimal logging

---

### 10. Check Installation Logs

Review the installation log at:
`C:\Program Files\SAM AI\scripts\post_install.log`

**Look for these log entries**:

✅ **PostgreSQL Initialization**:
```
[4.2] Command: "C:\Program Files\SAM AI\postgresql\bin\initdb.exe" -D "C:\Program Files\SAM AI\postgresql\data" -U postgres -E UTF8 --lc-collate=C --lc-ctype=C
```

✅ **Database Creation**:
```
[4.5] Command: "C:\Program Files\SAM AI\postgresql\bin\createdb.exe" -U sam_ai_user -E UTF8 -O sam_ai_user -T template0 -l C sam_ai
```

✅ **If you had PostgreSQL 15 with wrong locale**:
```
[4.5] PostgreSQL at C:\Program Files\PostgreSQL\15 has wrong locale: English_Australia.1252
[4.5] This will cause severe performance issues - skipping
[4.5] Using bundled PostgreSQL with correct locale settings
```

---

## Success Criteria

- [x] Welcome page opens **once** (not twice)
- [x] Database locale: `datctype = C` ✅
- [x] Cluster locale: `lc_ctype = C` ✅
- [x] Module installations: **30-60 seconds** ✅
- [x] ai_sam installation: **< 1 minute** ✅
- [x] No 11+ minute hangs ✅

---

## If Something Goes Wrong

### Database still has wrong locale
**Symptom**: `datctype = English_Australia.1252`

**Fix**:
1. The installer detected and used existing PostgreSQL with wrong locale
2. Manually delete: `C:\Program Files\SAM AI\postgresql\data`
3. Re-run: `C:\Program Files\SAM AI\scripts\post_install.ps1` (if available)
4. Or uninstall and reinstall

### Module installations still hang
**Symptom**: Module installs take 11+ minutes

**Diagnosis**:
1. Check database locale (Step 5 above)
2. If locale is wrong, database needs to be recreated
3. If locale is correct, check Odoo logs for other issues

---

**Good luck with the test!** 🍀

If everything passes, your installer is **PRODUCTION READY** with the database locale fix! 🚀
