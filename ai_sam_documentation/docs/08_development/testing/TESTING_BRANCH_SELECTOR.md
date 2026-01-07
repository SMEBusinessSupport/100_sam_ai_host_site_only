# 🧪 Testing the Branch Selector Dropdown

**Quick Start Guide for Testing the New Branch Meta-Architecture**

---

## 📋 Prerequisites

Before testing, ensure:

1. ✅ Odoo server is running
2. ✅ Both modules installed:
   - `ai_automator_base` (for ai.branch model)
   - `the_ai_automator` (for UI)
3. ✅ Browser cache cleared (Ctrl+Shift+R)

---

## 🔄 Step 1: Restart Odoo

The new files need to be loaded:

```bash
# Stop Odoo
# Restart Odoo with:
python odoo-bin -c odoo.conf -u ai_automator_base,the_ai_automator
```

Or via Windows service:
```powershell
# Stop service
sc stop OdooService

# Start service
sc start OdooService
```

---

## 🎯 Step 2: Initialize Core Branches

The `ai.branch` model needs initial data. Run this Python code in Odoo shell or create a simple wizard:

```python
# Option 1: Via Odoo Shell
# python odoo-bin shell -c odoo.conf

env['ai.branch'].create([
    {
        'name': 'Workflow Automation',
        'technical_name': 'workflow',
        'code': 'WF',
        'icon': '⚡',
        'color': '#1a73e8',
        'description': 'N8N-style workflow automation with 2,700+ nodes',
        'canvas_type': 'node_based',
        'js_class': 'WorkflowCanvas',
        'canvas_model': 'canvas',
        'node_model': 'nodes',
        'module_name': 'the_ai_automator',
        'module_installed': True,
        'is_premium': False,
        'is_core': True,
        'sequence': 10,
    },
    {
        'name': 'Mind Map',
        'technical_name': 'mind_map',
        'code': 'MM',
        'icon': '🧠',
        'color': '#e91e63',
        'description': 'Visual mind mapping for brainstorming and planning',
        'canvas_type': 'freeform',
        'js_class': 'MindMapCanvas',
        'canvas_model': 'mindmap.canvas',
        'node_model': 'mindmap.node',
        'module_name': 'sam_ai_mind_map',
        'module_installed': False,  # Not installed yet
        'is_premium': True,
        'monthly_price': 29.00,
        'sequence': 20,
    },
    {
        'name': 'Workflow Diagram',
        'technical_name': 'process_designer',
        'code': 'PD',
        'icon': '📊',
        'color': '#4caf50',
        'description': 'BPMN-style process design and documentation',
        'canvas_type': 'node_based',
        'js_class': 'ProcessCanvas',
        'canvas_model': 'process.canvas',
        'node_model': 'process.node',
        'module_name': 'sam_ai_process_designer',
        'module_installed': False,
        'is_premium': True,
        'monthly_price': 39.00,
        'sequence': 30,
    },
    {
        'name': 'Knowledge Board',
        'technical_name': 'knowledge_board',
        'code': 'KB',
        'icon': '📚',
        'color': '#ff9800',
        'description': 'Organize and visualize knowledge connections',
        'canvas_type': 'board',
        'js_class': 'KnowledgeCanvas',
        'canvas_model': 'knowledge.canvas',
        'node_model': 'knowledge.node',
        'module_name': 'sam_ai_knowledge_board',
        'module_installed': False,
        'is_premium': True,
        'monthly_price': 29.00,
        'sequence': 40,
    }
])
env.cr.commit()
print("✅ Core branches initialized!")
```

**Or** use the API endpoint (easier):
```bash
curl -X POST http://localhost:8069/canvas/api/branches/init \
  -H "Content-Type: application/json" \
  -u admin:admin
```

---

## 🧪 Step 3: Test the Dropdown

### 3.1 Open Canvas Page

Navigate to:
```
The AI Automator → Workflows → [Any Workflow] → Open Canvas
```

Or directly:
```
http://localhost:8069/canvas/<workflow_id>
```

### 3.2 Check Console Logs

Open browser console (F12) and look for:
```
📱 Branch Selector Dropdown initialized
✅ Fetched 4 branches from database
✅ Dropdown menu created with 4 branch options
```

### 3.3 Click "Add Node" Button

The button should now be a **dropdown toggle** with a ▼ arrow.

**Expected behavior:**
1. Click button
2. Dropdown menu appears below button
3. Shows header: "Select Canvas Type"
4. Shows 4 options:
   - ⚡ Workflow Automation
   - 🧠 Mind Map [Module Required]
   - 📊 Workflow Diagram [Module Required]
   - 📚 Knowledge Board [Module Required]

### 3.4 Select "Workflow Automation"

**Expected behavior:**
1. Dropdown closes
2. N8N node selector overlay opens
3. Shows 2,700+ available nodes
4. Can select a node (e.g., HTTP Request)
5. Node appears on canvas

### 3.5 Check Branch Context

In browser console, check:
```javascript
window.selectedBranchType
// Should show: "workflow"

window.selectedBranchData
// Should show: { name: "Workflow Automation", ... }
```

---

## ✅ Success Checklist

Mark each as you verify:

### Visual Tests
- [ ] "Add Node" button has dropdown arrow (▼)
- [ ] Clicking button opens dropdown (not modal)
- [ ] Dropdown shows 4 canvas types
- [ ] Icons display correctly (⚡, 🧠, 📊, 📚)
- [ ] "Workflow Automation" is clickable
- [ ] Other 3 show "Module Required" badge
- [ ] Hover effect works (background changes)
- [ ] Dropdown has rounded corners and shadow

### Functional Tests
- [ ] Selecting "Workflow" opens N8N selector
- [ ] N8N selector shows all nodes
- [ ] Can select and add a node
- [ ] Node appears on canvas
- [ ] Save workflow works
- [ ] Reload page shows saved node

### Database Tests
- [ ] `ai_branch` table exists
- [ ] Contains 4 records
- [ ] Canvas record has `branch_type` = 'workflow'
- [ ] Canvas has `branch_id` linked to workflow branch

### API Tests
```bash
# Test 1: List branches
curl http://localhost:8069/canvas/api/branches/available

# Test 2: Get workflow config
curl http://localhost:8069/canvas/api/branches/workflow/config

# Test 3: Create canvas
curl -X POST http://localhost:8069/canvas/api/create \
  -H "Content-Type: application/json" \
  -d '{"branch_type": "workflow", "name": "Test"}'
```

---

## 🐛 Troubleshooting

### Issue: Dropdown doesn't appear

**Check:**
1. Browser console for errors
2. Network tab: branch_dropdown.css loaded?
3. Network tab: branch_selector_dropdown.js loaded?
4. Console log: "Branch Selector Dropdown initialized"?

**Fix:**
- Clear browser cache (Ctrl+Shift+R)
- Restart Odoo
- Check file paths in canvas_page_views.xml

---

### Issue: "No branches found"

**Check:**
1. Database: `SELECT * FROM ai_branch;`
2. API endpoint: `/canvas/api/branches/available`
3. Console log: "Fetched X branches"

**Fix:**
- Run initialization script (Step 2)
- Check model access rights
- Verify user permissions

---

### Issue: N8N selector doesn't open

**Check:**
1. Console: `window.overlayManager` exists?
2. Console: `window.selectedBranchType` set?
3. Error messages in console?

**Fix:**
- Ensure overlay_manager.js loaded
- Check overlayManager.showN8nNodeSelection() method
- Verify branch data passed correctly

---

### Issue: Dropdown styling broken

**Check:**
1. Network tab: branch_dropdown.css status 200?
2. Elements tab: `.branch-dropdown-menu` class present?
3. Bootstrap 5 loaded?

**Fix:**
- Check CSS file path
- Ensure Bootstrap 5.1.3+ loaded
- Clear browser cache

---

## 📊 Database Verification

After testing, verify database state:

```sql
-- Check branches exist
SELECT id, name, technical_name, module_installed
FROM ai_branch
ORDER BY sequence;

-- Check canvas has branch link
SELECT id, name, branch_type, branch_id, canvas_type
FROM canvas
LIMIT 5;

-- Check branch relationship
SELECT
    c.id,
    c.name AS canvas_name,
    c.branch_type,
    b.name AS branch_name,
    b.module_installed
FROM canvas c
LEFT JOIN ai_branch b ON c.branch_id = b.id
LIMIT 5;
```

---

## 🎯 Expected Results

**Perfect Test Run:**
1. ✅ 4 branches in database
2. ✅ Dropdown appears on "Add Node" click
3. ✅ 4 options visible (1 available, 3 locked)
4. ✅ "Workflow Automation" opens N8N selector
5. ✅ Node can be added to canvas
6. ✅ Canvas saved with branch_type = 'workflow'
7. ✅ No console errors
8. ✅ UI smooth and responsive

---

## 📸 Screenshots to Take

For documentation:
1. Dropdown closed (button with arrow)
2. Dropdown open (showing 4 options)
3. "Workflow Automation" hovered
4. "Module Required" badge visible
5. N8N selector opened after selection
6. Node added to canvas
7. Browser console showing logs
8. Database records showing branch data

---

## 🎓 Testing Tips

1. **Always check console first** - Most issues show there
2. **Test in incognito mode** - Eliminates cache issues
3. **Use Network tab** - See if files load
4. **Check database directly** - Verify data exists
5. **Test on mobile** - Ensure responsive design works

---

## ✅ Sign-Off

Once all tests pass:

```
[ ] Visual tests: 8/8 passed
[ ] Functional tests: 6/6 passed
[ ] Database tests: 4/4 passed
[ ] API tests: 3/3 passed
[ ] Total: 21/21 passed ✅

Tested by: _______________
Date: _______________
Status: READY FOR PRODUCTION / NEEDS WORK
```

---

## 🚀 Next Steps After Testing

If all tests pass:
1. Document any issues found
2. Create first extension module (Mind Map)
3. Test with actual extension installed
4. Deploy to staging environment
5. User acceptance testing

---

*"Test early, test often, test thoroughly."*

**End of Testing Guide**
