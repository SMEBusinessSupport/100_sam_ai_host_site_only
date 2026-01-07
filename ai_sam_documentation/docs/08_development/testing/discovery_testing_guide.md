# N8N Discovery Testing Guide
## Complete Process to Fix "0 actions" Issue

### Overview
This guide walks you through the complete process to fix the overlay showing "1 trigger, 0 actions" instead of "1 trigger, 48 actions" for ActiveCampaign.

---

## What We've Fixed

- Removed duplicate discovery method from n8n_node_filesystem.py
- Renamed correct discovery method to discover_hierarchical_n8n_nodes()
- Fixed parsing logic to handle modular N8N structure (.node.js + Description files)
- Created SQL script to clear bad schema data

---

## Step-by-Step Testing Process

### STEP 1: Check Current Database Status

The database is: ai_automator_db
Current table counts: 305 parent records, 321 L1 records, 304 L2 records

1. Check ActiveCampaign status:
   ```cmd
   set PGPASSWORD=odoo_password && "C:\Program Files\PostgreSQL\15\bin\psql.exe" -U odoo_user -d ai_automator_db -c "SELECT id, folder_name, display_name, has_node_json FROM n8n_folder_information WHERE folder_name = 'ActiveCampaign';"
   ```

   Expected Result: Should show ActiveCampaign with has_node_json = t

   Note: DO NOT clear the data - we'll test with existing data first!

---

### STEP 2: Run Fresh Discovery from Odoo Admin

1. Access Odoo Admin Interface:
   - Log into Odoo as administrator
   - Go to Apps → AI Automator

2. Navigate to N8N Configuration:
   - Apps → AI Automator → Configuration → N8N Folder Information
   - Or search for "N8N Folder" in the search bar

3. Run Discovery:
   - Click the "Action" button (gear icon)
   - Select "Refresh Discovery" from the dropdown
   - This will call discover_hierarchical_n8n_nodes() method

4. Monitor the Process:
   - Watch for success notification: "Hierarchical Node Discovery Complete"
   - Check Odoo logs for detailed progress:
     ```bash
     tail -f /var/log/odoo/odoo.log | grep "DEBUG\|ERROR\|Exception"
     ```

---

### STEP 3: Verify Data Population

1. Check Database Results:
   ```sql
   -- Check parent records
   SELECT COUNT(*) as parent_count FROM n8n_folder_information;

   -- Check ActiveCampaign specifically
   SELECT * FROM n8n_folder_information WHERE folder_name = 'ActiveCampaign';

   -- Check L1 and L2 populations
   SELECT COUNT(*) as l1_count FROM n8n_nodes_l1;
   SELECT COUNT(*) as l2_count FROM n8n_nodes_l2;
   ```

2. Expected Results:
   - Parent count: ~305 records (one per N8N folder)
   - ActiveCampaign record: Should exist with proper has_node_json field
   - L1/L2 counts: Should have hierarchical data

---

### STEP 4: Test Overlay System

1. Access Canvas Interface:
   - Go to AI Automator → Canvas → Workflow Canvas

2. Test Node Selection:
   - Click the "+ Add Node" button
   - Click on "N8N Nodes" tab
   - Click on "ActiveCampaign" node

3. Verify Results:
   - Expected: Overlay shows "Triggers (1)" and "Actions (48)"
   - Not: "Triggers (1)" and "Actions (0)"

4. Test Hierarchical Navigation:
   - Click on "Google" node
   - Should show sub-folders: Gmail, Sheets, Drive, Calendar, etc.
   - Click on "Gmail" → Should show Gmail-specific triggers and actions

---

## Debugging Failed Results

### If Discovery Fails:

1. Check Odoo Logs:
   ```bash
   grep "ERROR\|Exception" /var/log/odoo/odoo.log | tail -20
   ```

2. Verify File Paths:
   - Ensure N8N nodes exist at: static/src/n8n/n8n_nodes/
   - Check ActiveCampaign folder contains: ActiveCampaign.node.js

3. Manual Debug:
   ```python
   # In Odoo shell
   folder_info = env['n8n.folder.information']
   result = folder_info.discover_hierarchical_n8n_nodes()
   print(f"Discovery result: {result}")
   ```

### If Overlay Still Shows 0 Actions:

1. Check API Endpoints:
   - Test: /canvas/n8n/node_structure
   - Verify ActiveCampaign ID in database matches API calls

2. Check Browser Console:
   - F12 → Console → Look for JavaScript errors
   - Check network tab for failed API calls

3. Verify Database Data:
   ```sql
   -- Check if ActiveCampaign has parsed operations
   SELECT folder_name, has_node_json FROM n8n_folder_information
   WHERE folder_name = 'ActiveCampaign';
   ```

---

## Success Criteria

The system is working correctly when:

- Discovery completes without errors
- Database populated with ~305 parent records
- ActiveCampaign shows "Triggers (1) Actions (48)"
- Google shows hierarchical sub-folders
- API endpoints return correct data
- Overlay navigation works smoothly

---

## If You Need Help

If any step fails:

1. Check the logs for specific error messages
2. Verify file permissions on N8N folders
3. Ensure database connectivity is working
4. Test with a single node first (ActiveCampaign)

---

KEY TEST: ActiveCampaign should show "1 trigger, 48 actions" instead of "1 trigger, 0 actions"