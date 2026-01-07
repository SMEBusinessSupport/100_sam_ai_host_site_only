-- =================================================================
-- N8N DATABASE EXPORT QUERIES FOR DEBUGGING
-- Run these queries in your PostgreSQL to export CSV files
-- =================================================================

-- 1. EXPORT PARENT FOLDER INFORMATION TABLE
\copy (
    SELECT
        id,
        folder_name,
        display_name,
        has_node_json,
        icon,
        description,
        category,
        platform_type,
        node_count,
        created_date,
        last_updated
    FROM n8n_folder_information
    WHERE folder_name IN ('ActiveCampaign', 'Google')
    ORDER BY folder_name
) TO 'C:\Working With AI\Odoo Projects\custom-modules-v18\the_ai_automator\docs\overlay\parent_folders.csv' WITH CSV HEADER;

-- 2. EXPORT ALL PARENT FOLDERS (to see full structure)
\copy (
    SELECT
        id,
        folder_name,
        display_name,
        has_node_json,
        icon,
        description,
        category,
        platform_type,
        node_count,
        created_date,
        last_updated
    FROM n8n_folder_information
    ORDER BY folder_name
) TO 'C:\Working With AI\Odoo Projects\custom-modules-v18\the_ai_automator\docs\overlay\all_parent_folders.csv' WITH CSV HEADER;

-- 3. EXPORT L1 CHILDREN (Google sub-services)
\copy (
    SELECT
        id,
        parent_id,
        folder_name,
        display_name,
        parent_folder,
        icon,
        description,
        has_triggers,
        has_actions,
        trigger_count,
        action_count,
        created_date,
        last_updated
    FROM n8n_l1_children
    WHERE parent_folder = 'Google'
    ORDER BY display_name
) TO 'C:\Working With AI\Odoo Projects\custom-modules-v18\the_ai_automator\docs\overlay\google_l1_children.csv' WITH CSV HEADER;

-- 4. EXPORT ALL L1 CHILDREN
\copy (
    SELECT
        id,
        parent_id,
        folder_name,
        display_name,
        parent_folder,
        icon,
        description,
        has_triggers,
        has_actions,
        trigger_count,
        action_count,
        created_date,
        last_updated
    FROM n8n_l1_children
    ORDER BY parent_folder, display_name
) TO 'C:\Working With AI\Odoo Projects\custom-modules-v18\the_ai_automator\docs\overlay\all_l1_children.csv' WITH CSV HEADER;

-- 5. EXPORT NODE STRUCTURE DATA (ActiveCampaign triggers/actions)
\copy (
    SELECT
        id,
        folder_name,
        parent_id,
        node_type,
        operation_name,
        display_name,
        description,
        is_trigger,
        is_action,
        parameters,
        created_date,
        last_updated
    FROM n8n_node_structure
    WHERE folder_name = 'ActiveCampaign'
    ORDER BY is_trigger DESC, operation_name
) TO 'C:\Working With AI\Odoo Projects\custom-modules-v18\the_ai_automator\docs\overlay\activecampaign_nodes.csv' WITH CSV HEADER;

-- 6. EXPORT ALL NODE STRUCTURE DATA
\copy (
    SELECT
        id,
        folder_name,
        parent_id,
        node_type,
        operation_name,
        display_name,
        description,
        is_trigger,
        is_action,
        parameters,
        created_date,
        last_updated
    FROM n8n_node_structure
    ORDER BY folder_name, is_trigger DESC, operation_name
) TO 'C:\Working With AI\Odoo Projects\custom-modules-v18\the_ai_automator\docs\overlay\all_node_structures.csv' WITH CSV HEADER;

-- =================================================================
-- DEBUGGING QUERIES - Run these to check data counts
-- =================================================================

-- Check ActiveCampaign parent folder
SELECT
    id,
    folder_name,
    has_node_json,
    node_count,
    'PARENT FOLDER' as type
FROM n8n_folder_information
WHERE folder_name = 'ActiveCampaign';

-- Count ActiveCampaign triggers and actions
SELECT
    folder_name,
    COUNT(*) as total_nodes,
    SUM(CASE WHEN is_trigger = true THEN 1 ELSE 0 END) as trigger_count,
    SUM(CASE WHEN is_action = true THEN 1 ELSE 0 END) as action_count
FROM n8n_node_structure
WHERE folder_name = 'ActiveCampaign'
GROUP BY folder_name;

-- Check Google parent folder and children
SELECT
    nfi.id,
    nfi.folder_name,
    nfi.has_node_json,
    COUNT(nl1.id) as children_count,
    'GOOGLE DATA' as type
FROM n8n_folder_information nfi
LEFT JOIN n8n_l1_children nl1 ON nfi.folder_name = nl1.parent_folder
WHERE nfi.folder_name = 'Google'
GROUP BY nfi.id, nfi.folder_name, nfi.has_node_json;

-- List all Google L1 children
SELECT
    id,
    folder_name,
    display_name,
    trigger_count,
    action_count
FROM n8n_l1_children
WHERE parent_folder = 'Google'
ORDER BY display_name;

-- =================================================================
-- ALTERNATIVE: If table names are different, try these variations
-- =================================================================

-- If tables have different names, uncomment and try these:
-- SELECT table_name FROM information_schema.tables WHERE table_name LIKE '%n8n%';
-- SELECT table_name FROM information_schema.tables WHERE table_name LIKE '%node%';
-- SELECT table_name FROM information_schema.tables WHERE table_name LIKE '%folder%';