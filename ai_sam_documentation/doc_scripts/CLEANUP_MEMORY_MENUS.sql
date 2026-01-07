-- ===========================================================================
-- CLEANUP SCRIPT: Remove Orphaned Memory Menus from Database
-- ===========================================================================
--
-- PROBLEM: Memory-related menus still appear in UI even though:
--   - ai_brain has NO views/menus (data layer only)
--   - ai_sam has all memory references commented out
--   - Only ai_brain module is installed
--
-- CAUSE: Old menu records in database from previous versions
--
-- SOLUTION: Manually delete orphaned memory menu records
--
-- HOW TO RUN THIS SCRIPT:
-- =======================
--
-- Option 1: Via psql command line
-- --------------------------------
-- psql -U odoo_user -d ai_automator_db -f "C:\Working With AI\ai_sam\ai_sam\CLEANUP_MEMORY_MENUS.sql"
--
-- Option 2: Via Odoo shell (safer, respects ORM)
-- ----------------------------------------------
-- See CLEANUP_MEMORY_MENUS.py script
--
-- ===========================================================================

BEGIN;

-- 1. Find and delete memory-related menus
DELETE FROM ir_ui_menu WHERE name IN (
    'Memory View',
    'Memory Configuration',
    'Import Conversations',
    'Learned Extractors'
) OR name LIKE '%Memory%' OR name LIKE '%Uninstall Helper%';

-- 2. Find and delete memory-related actions (act_window)
DELETE FROM ir_act_window WHERE name IN (
    'Memory View',
    'Memory Configuration',
    'Import Conversations',
    'Learned Extractors'
) OR name LIKE '%Memory%';

-- 3. Find and delete memory-related actions (act_url)
DELETE FROM ir_act_url WHERE name IN (
    'Memory View'
) OR url LIKE '%memory%';

-- 4. Show what we found (before deleting - comment out DELETE above first to test)
-- SELECT id, name, parent_id FROM ir_ui_menu WHERE name LIKE '%Memory%' OR name LIKE '%Import Conversation%' OR name LIKE '%Extractor%';
-- SELECT id, name, res_model FROM ir_act_window WHERE name LIKE '%Memory%' OR name LIKE '%Import%' OR name LIKE '%Extractor%';

COMMIT;

-- Verification query (run after cleanup)
-- SELECT id, name, parent_id FROM ir_ui_menu WHERE name LIKE '%Memory%';
-- Should return 0 rows if cleanup successful

