# Verify L3 L4 Data

**Original file:** `verify_l3_l4_data.sql`
**Type:** SQL

---

```sql
-- Verify L3 and L4 data was populated

-- Count records in each level
SELECT
    'Parent' as level,
    COUNT(*) as count
FROM n8n_folder_information
UNION ALL
SELECT
    'L1' as level,
    COUNT(*) as count
FROM n8n_nodes_l1
UNION ALL
SELECT
    'L2' as level,
    COUNT(*) as count
FROM n8n_nodes_l2
UNION ALL
SELECT
    'L3' as level,
    COUNT(*) as count
FROM n8n_nodes_l3_resources
UNION ALL
SELECT
    'L4' as level,
    COUNT(*) as count
FROM n8n_nodes_l4_operations;

-- Show specific ActiveCampaign data
SELECT
    'ActiveCampaign resources:' as info,
    COUNT(*) as count
FROM n8n_nodes_l3_resources l3
JOIN n8n_nodes_l2 l2 ON l3.parent_l2_id = l2.id
WHERE l2.display_name LIKE '%ActiveCampaign%';

-- Show ActiveCampaign operations
SELECT
    'ActiveCampaign operations:' as info,
    COUNT(*) as count
FROM n8n_nodes_l4_operations l4
JOIN n8n_nodes_l3_resources l3 ON l4.parent_l3_id = l3.id
JOIN n8n_nodes_l2 l2 ON l3.parent_l2_id = l2.id
WHERE l2.display_name LIKE '%ActiveCampaign%';

-- Show sample L3 resources for ActiveCampaign
SELECT
    l3.display_name as resource_name,
    l3.resource_value,
    COUNT(l4.id) as operation_count
FROM n8n_nodes_l3_resources l3
LEFT JOIN n8n_nodes_l4_operations l4 ON l4.parent_l3_id = l3.id
JOIN n8n_nodes_l2 l2 ON l3.parent_l2_id = l2.id
WHERE l2.display_name LIKE '%ActiveCampaign%'
GROUP BY l3.id, l3.display_name, l3.resource_value
ORDER BY l3.display_name;
```
