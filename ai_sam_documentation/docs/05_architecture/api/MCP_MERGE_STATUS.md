MCP SERVER MERGE TO AI_SAM CORE - STATUS
==========================================

Date: 2025-11-04
Decision: Merge ai_sam_claude_mcp into ai_sam core module
Reason: MCP generation is core framework functionality, desktop installer handles environment setup

## FILES MOVED (COMPLETED ✅)

### 1. Model
✅ ai_sam_claude_mcp/models/mcp_server_config.py
   → ai_sam/models/mcp_server_config.py

### 2. Service
✅ ai_sam_claude_mcp/services/mcp_server_generator.py
   → ai_sam/services/mcp_server_generator.py

### 3. Controller
✅ ai_sam_claude_mcp/controllers/download_controller.py
   → ai_sam/controllers/mcp_download_controller.py

## REMAINING TASKS (TO COMPLETE)

### 4. Views (PENDING ❌)
Need to move:
- ai_sam_claude_mcp/views/mcp_server_config_views.xml
  → ai_sam/views/mcp_server_config_views.xml

### 5. Security Rules (PENDING ❌)
Need to copy access rules from:
- ai_sam_claude_mcp/security/ir.model.access.csv
  → ai_sam/security/ir.model.access.csv (merge, don't overwrite)

Add these lines:
```csv
sam.mcp.server.config,access_sam_mcp_server_config,model_sam_mcp_server_config,base.group_user,1,1,1,1
sam.mcp.feature,access_sam_mcp_feature,model_sam_mcp_feature,base.group_user,1,1,1,1
```

### 6. Update ai_sam/__manifest__.py (PENDING ❌)

Add to 'depends' section (no change needed, already has ai_brain):
```python
'depends': [
    'base',
    'web',
    'ai_brain',  # Already present
],
```

Add to 'data' section:
```python
'data': [
    'security/ir.model.access.csv',  # Already present, will merge MCP rules
    # ... existing entries ...
    'views/mcp_server_config_views.xml',  # ADD THIS LINE
    # ... rest of views ...
],
```

Update description in manifest to mention MCP:
```python
'summary': 'SAM AI Core Framework - Intelligence, Memory, Canvas, Workflow Automation & MCP Server Generation',
```

Add to description text:
```python
MCP Server Generation:
----------------------
* Generate standalone MCP servers for Claude Desktop
* Expose Odoo data via Model Context Protocol
* Projects, CRM, Sales, Custom Models support
* OAuth-ready architecture
```

### 7. Update ai_sam/__init__.py Files (PENDING ❌)

**ai_sam/models/__init__.py** - Add:
```python
from . import mcp_server_config
```

**ai_sam/services/__init__.py** - Create if doesn't exist, add:
```python
# -*- coding: utf-8 -*-
from . import mcp_server_generator
```

**ai_sam/controllers/__init__.py** - Add:
```python
from . import mcp_download_controller
```

### 8. Update Documentation (PENDING ❌)

Update ai_sam/documentation/MCP_API_COMPLETE_ARCHITECTURE.txt:
- Change references from ai_sam_claude_mcp → ai_sam
- Note that installer components removed (handled by desktop installer)
- Update module count from 5 to 4

### 9. Test (PENDING ❌)

1. Upgrade ai_sam module in Odoo
2. Verify "MCP Server" menu appears
3. Create new MCP server config
4. Generate server script
5. Download and test generated odoo_mcp_server.py
6. Verify no errors in Odoo log

### 10. Cleanup (PENDING ❌)

After successful testing:
1. Uninstall ai_sam_claude_mcp module from Odoo
2. Delete ai_sam_claude_mcp folder
3. Update any documentation referencing the old module

---

## FILES TO DELETE (from ai_sam_claude_mcp)

These installer-related files are NO LONGER NEEDED (desktop installer handles this):

❌ models/environment_config.py
❌ models/installation_log.py
❌ services/claude_installer.py
❌ services/vscode_installer.py
❌ services/python_installer.py
❌ services/installer_service.py
❌ services/config_generator.py
❌ services/bundle_creator.py
❌ wizards/environment_wizard.py
❌ All installer-related views

---

## NEXT SESSION CHECKLIST

To complete the merge, execute in order:

[ ] 1. Copy views/mcp_server_config_views.xml to ai_sam/views/
[ ] 2. Merge security rules into ai_sam/security/ir.model.access.csv
[ ] 3. Update ai_sam/__manifest__.py (add view, update description)
[ ] 4. Update ai_sam/__init__.py files (models, services, controllers)
[ ] 5. Restart Odoo
[ ] 6. Upgrade ai_sam module
[ ] 7. Test MCP server generation
[ ] 8. If successful, uninstall ai_sam_claude_mcp
[ ] 9. Delete ai_sam_claude_mcp folder
[ ] 10. Update MCP_API_COMPLETE_ARCHITECTURE.txt documentation

---

## ESTIMATED TIME REMAINING

- Tasks 1-4: 30 minutes (file operations + manifest updates)
- Task 5-7: 30 minutes (testing)
- Task 8-10: 15 minutes (cleanup + docs)
**Total: ~75 minutes**

---

## BENEFITS OF THIS MERGE

✅ Simpler architecture (4 modules instead of 5)
✅ MCP generation available in base ai_sam install
✅ Desktop installer handles environment setup
✅ Odoo module focused purely on Odoo features
✅ MCP generator reusable by orchestrator (future)
✅ No duplication between modules
✅ Easier maintenance

---

Status: 30% Complete (3 of 10 tasks done)
Next: Complete remaining 7 tasks in next session
