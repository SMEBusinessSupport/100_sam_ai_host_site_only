# AI Automator Docs - Installation & Testing Guide

**Quick guide to install and verify the new documentation branch module**

---

## 🚀 Installation Steps

### 1. Verify Module Structure

Check that the new module exists:
```
C:\Working With AI\Odoo Projects\custom-modules-v18\ai_automator_docs\
├── __init__.py ✓
├── __manifest__.py ✓
├── README.md ✓
├── controllers/ ✓
├── views/ ✓
├── docs/ ✓ (70+ files)
└── tools/ ✓ (7 Python scripts)
```

### 2. Restart Odoo

```bash
# Stop Odoo service
# Restart with both modules updated:
python odoo-bin -c odoo.conf -u ai_automator_base,the_ai_automator

# Then install the new docs module:
python odoo-bin -c odoo.conf -i ai_automator_docs
```

Or via UI:
1. Apps → Update Apps List
2. Search "AI Automator Documentation"
3. Click Install

### 3. Verify Installation

Check that module appears in installed modules:
```
Settings → Apps → Installed
Search: "ai_automator_docs"
Status: Should show as installed
```

---

## ✅ Testing Checklist

### Test 1: Menu Appears
- [ ] Navigate to AI Automator app
- [ ] See "📖 Documentation" menu
- [ ] Submenu shows:
  - [ ] 📄 View Documents
  - [ ] 🔄 Scan Documentation

### Test 2: Scan Documentation Works
- [ ] Click "🔄 Scan Documentation"
- [ ] System scans `docs/` folder
- [ ] Should find 70+ documentation files
- [ ] Categorized properly

### Test 3: View Documentation
- [ ] Click "📄 View Documents"
- [ ] List shows all scanned docs
- [ ] Click "View" button on any doc
- [ ] Opens in browser/viewer
- [ ] Click "Path" button
- [ ] Shows file path
- [ ] Click "Download" button
- [ ] File downloads

### Test 4: Search & Filter
- [ ] Search for "architecture"
- [ ] Results filtered
- [ ] Click "HTML Files" filter
- [ ] Shows only HTML docs
- [ ] Click "Architecture Docs" filter
- [ ] Shows architecture category
- [ ] Group by "Category"
- [ ] Docs grouped correctly

### Test 5: Tools Accessible
- [ ] Navigate to module folder
- [ ] Open `tools/` directory
- [ ] Run: `python analyze_module_quality.py`
- [ ] Should execute without errors
- [ ] Run: `python validate_module_split.py`
- [ ] Should validate modules
- [ ] Other tools present and accessible

---

## 🔍 Verification Queries

### Check Model Access
```python
# In Odoo shell
env['ai.automator.documentation'].search([])
# Should return documentation records
```

### Check Menu
```sql
-- In PostgreSQL
SELECT id, name, parent_id, action
FROM ir_ui_menu
WHERE name LIKE '%Documentation%';
-- Should show documentation menus
```

### Check Views
```sql
SELECT id, name, model
FROM ir_ui_view
WHERE model = 'ai.automator.documentation';
-- Should show 3 views (list, form, search)
```

---

## 🐛 Troubleshooting

### Issue: Module Not Found
**Symptom:** Can't find ai_automator_docs in app list
**Fix:**
1. Check module is in correct addons path
2. Restart Odoo completely
3. Update apps list
4. Check Odoo logs for errors

### Issue: Documentation Not Scanning
**Symptom:** Scan button does nothing
**Fix:**
1. Check `docs/` folder exists in module
2. Check file permissions (read access)
3. Check Odoo logs for Python errors
4. Verify documentation_manager model exists in base

### Issue: Views Not Loading
**Symptom:** Menu shows but clicking gives error
**Fix:**
1. Check view IDs don't conflict
2. Verify model reference: `ai.automator.documentation`
3. Check ai_automator_base is installed
4. Upgrade both base and docs modules

### Issue: Menu Not Appearing
**Symptom:** No documentation menu visible
**Fix:**
1. Check dependency on the_ai_automator
2. Verify menu parent reference
3. Check user permissions
4. Clear browser cache

---

## 📊 Expected Results

### After Installation
- ✅ Module status: Installed
- ✅ Menu: "📖 Documentation" visible
- ✅ Submenus: 2 items
- ✅ Model: `ai.automator.documentation` accessible
- ✅ Views: 3 views registered
- ✅ Docs folder: 70+ files present
- ✅ Tools folder: 7 Python scripts

### After Scanning
- ✅ Database records: 70+ documentation entries
- ✅ Categories: architecture, development, research, etc.
- ✅ File types: markdown, HTML, SQL
- ✅ All files accessible via UI

---

## 🎯 Success Criteria

Module is successfully installed and working when:

1. ✅ Can install without errors
2. ✅ Documentation menu appears
3. ✅ Scan discovers all 70+ files
4. ✅ Can view documents in browser
5. ✅ Can download documents
6. ✅ Search and filters work
7. ✅ Python tools accessible
8. ✅ No console errors
9. ✅ Models reference base correctly
10. ✅ Branch architecture working

---

## 🔄 Rollback Plan

If issues occur:

1. **Uninstall docs module:**
   ```
   Apps → AI Automator Documentation → Uninstall
   ```

2. **Restore frontend module:**
   - Uncomment documentation lines in `the_ai_automator/__manifest__.py`
   - Uncomment import in `the_ai_automator/controllers/__init__.py`
   - Restart and upgrade the_ai_automator

3. **Keep files:**
   - ai_automator_docs folder remains
   - Can reinstall anytime
   - No data loss

---

## 📝 Next Steps After Installation

### Immediate
1. Scan documentation to populate database
2. Test all menu functions
3. Verify tools work correctly

### Short-term
1. Update file paths in AI prompts
2. Use new path format: `ai_automator_docs/docs/[path]`
3. Test session continuity with AI

### Long-term
1. Consider creating more branch modules
2. Extract other components (reporting, analytics, etc.)
3. Build out SAM AI ecosystem

---

## 🎉 Benefits Realized

Once installed and working:

### For Development
- ✅ Clean module separation
- ✅ Documentation centralized
- ✅ Tools co-located with docs
- ✅ Easy to maintain

### For AI Assistance
- ✅ Single file path for all docs
- ✅ Fast context loading
- ✅ Consistent locations
- ✅ Session continuity enabled

### For Architecture
- ✅ First branch module working!
- ✅ Meta-architecture proven
- ✅ Pattern established for future branches
- ✅ Tree growing successfully 🌳

---

*Ready to install? Let's test the branch architecture!*

---

**End of Installation Guide**
