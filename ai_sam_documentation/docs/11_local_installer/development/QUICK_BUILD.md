# Quick Build Reference - SAM AI Installer

**30-Second Command Reference**

---

## First Time Setup (15 minutes)

```powershell
# 1. Build Python bundle (one-time, ~10 min)
cd D:\SAMAI-18-SaaS\github-repos\100-samai-desktop-installer
.\build_python_bundle_production.ps1

# 2. Verify bundle
.\bundled\python\python.exe -c "import odoo; print('✓ Odoo OK')"

# 3. Build installer (~5 min)
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" odoo_samai_installer.iss

# 4. Test on clean VM
.\Output\SAM_AI_Premium_Business_Suite_Setup.exe
```

---

## Rebuild Installer (After Code Changes)

```powershell
# Already have Python bundle? Just rebuild installer:
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" odoo_samai_installer.iss
```

---

## Update Python Bundle (When Odoo/Deps Change)

```powershell
# 1. Update files
# - bundled\server\odoo\        (new Odoo version)
# - bundled\server\requirements.txt (new dependencies)

# 2. Rebuild bundle
.\build_python_bundle_production.ps1

# 3. Verify
.\bundled\python\python.exe -c "import odoo; print(odoo.release.version)"

# 4. Rebuild installer
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" odoo_samai_installer.iss
```

---

## Quick Test (No VM Available)

```powershell
# Test bundle in-place
cd .\bundled\python

.\python.exe -c "import odoo, psycopg2, lxml, werkzeug; print('✓ All imports OK')"

.\python.exe -c "import odoo; print(f'Odoo {odoo.release.version}')"
```

---

## Files Changed (Architecture Fix)

| File | Change | Why |
|------|--------|-----|
| `build_python_bundle_production.ps1` | **NEW** | Builds complete portable Python bundle |
| `odoo_samai_installer.iss` | Removed pip install | Dependencies now pre-bundled |
| `scripts\start_odoo.bat` | Fixed PYTHONPATH | Ensures `import odoo` works |

---

## Before/After

### OLD (Broken)
```
Installer → Copy files → Run pip install (10 min) → User waits → Fails sometimes
└─ Error: ModuleNotFoundError: No module named 'odoo'
```

### NEW (Fixed)
```
Build bundle once (10 min) → Installer → Copy pre-built files (2 min) → Done ✓
└─ import odoo works immediately
```

---

## Success Criteria

✅ `bundled\python\python.exe -c "import odoo"` → No error
✅ Installer builds without errors
✅ Installation completes in <5 minutes
✅ SAM AI starts without "ModuleNotFoundError"

---

**For full details:** See `BUILD_PRODUCTION_INSTALLER.md`
