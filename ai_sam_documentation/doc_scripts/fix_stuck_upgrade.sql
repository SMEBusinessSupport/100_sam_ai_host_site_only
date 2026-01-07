-- Fix Odoo Stuck Upgrade - SQL Method
-- Run with: psql -U odoo_user -d ai_automator_db -f fix_stuck_upgrade.sql

-- 1. Delete broken model references
DELETE FROM ir_model WHERE model IN ('privacy.log', 'privacy.lookup.wizard', 'privacy.lookup.wizard.line');
DELETE FROM ir_model_fields WHERE model IN ('privacy.log', 'privacy.lookup.wizard', 'privacy.lookup.wizard.line');
DELETE FROM ir_model_data WHERE model IN ('privacy.log', 'privacy.lookup.wizard', 'privacy.lookup.wizard.line');

-- 2. Reset any stuck module states
UPDATE ir_module_module SET state = 'installed' WHERE state = 'to upgrade';
UPDATE ir_module_module SET state = 'uninstalled' WHERE state IN ('to install', 'to remove');

-- 3. Show results
SELECT 'FIXED: Broken models deleted' as status;
SELECT name, state FROM ir_module_module WHERE state NOT IN ('installed', 'uninstalled');
