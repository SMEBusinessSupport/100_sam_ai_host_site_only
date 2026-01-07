# Clear Bad Data

**Original file:** `clear_bad_data.sql`
**Type:** SQL

---

```sql
-- =================================================================
-- CLEAR BAD N8N DATA FROM DATABASE TABLES
-- Run this script to clear incorrect schema data and prepare for proper discovery
-- =================================================================

-- WARNING: This will delete ALL existing N8N node data from the database
-- Make sure to backup any important data before running this script

BEGIN;

-- =================================================================
-- STEP 1: Clear all hierarchical N8N tables
-- =================================================================

-- Clear L2 nodes first (child tables first due to foreign key constraints)
DELETE FROM n8n_nodes_l2;
SELECT 'Cleared n8n_nodes_l2 table' as status;

-- Clear L1 services
DELETE FROM n8n_nodes_l1;
SELECT 'Cleared n8n_nodes_l1 table' as status;

-- Clear parent folder information
DELETE FROM n8n_folder_information;
SELECT 'Cleared n8n_folder_information table' as status;

-- =================================================================
-- STEP 2: Clear legacy/duplicate tables if they exist
-- =================================================================

-- Clear the old filesystem table (the wrong one that was causing conflicts)
DELETE FROM n8n_node_filesystem WHERE 1=1;
SELECT 'Cleared n8n_node_filesystem table' as status;

-- Clear any node structure data (if this table exists)
DELETE FROM n8n_node_structure WHERE 1=1;
SELECT 'Cleared n8n_node_structure table (if exists)' as status;

-- =================================================================
-- STEP 3: Reset auto-increment sequences (optional)
-- =================================================================

-- Reset the ID sequences to start fresh
SELECT setval(pg_get_serial_sequence('n8n_folder_information', 'id'), 1, false);
SELECT setval(pg_get_serial_sequence('n8n_nodes_l1', 'id'), 1, false);
SELECT setval(pg_get_serial_sequence('n8n_nodes_l2', 'id'), 1, false);

-- =================================================================
-- STEP 4: Verify all tables are empty
-- =================================================================

-- Check parent table
SELECT 'n8n_folder_information' as table_name, COUNT(*) as remaining_records FROM n8n_folder_information
UNION ALL
SELECT 'n8n_nodes_l1' as table_name, COUNT(*) as remaining_records FROM n8n_nodes_l1
UNION ALL
SELECT 'n8n_nodes_l2' as table_name, COUNT(*) as remaining_records FROM n8n_nodes_l2
UNION ALL
SELECT 'n8n_node_filesystem' as table_name, COUNT(*) as remaining_records FROM n8n_node_filesystem;

-- =================================================================
-- STEP 5: Show table structure for verification
-- =================================================================

-- Verify the table structures are correct
\d n8n_folder_information;
\d n8n_nodes_l1;
\d n8n_nodes_l2;

SELECT 'Database cleanup completed successfully!' as final_status;
SELECT 'Ready for fresh discovery run via discover_hierarchical_n8n_nodes()' as next_step;

COMMIT;

-- =================================================================
-- NOTES FOR NEXT STEPS:
-- =================================================================

-- After running this script:
-- 1. Go to Odoo Admin → AI Automator → N8N Configuration
-- 2. Click "Refresh Discovery" to run discover_hierarchical_n8n_nodes()
-- 3. Check the logs to verify proper data population
-- 4. Test the overlay system to confirm "48 actions" are showing

-- Expected results after fresh discovery:
-- - n8n_folder_information: ~305 parent records (one per top-level folder)
-- - n8n_nodes_l1: Variable L1 services (Google → Gmail, Sheets, etc.)
-- - n8n_nodes_l2: Variable L2 nodes (individual operations)

-- The key indicator of success:
-- ActiveCampaign should show "1 trigger, 48 actions" in the overlay popup
```
