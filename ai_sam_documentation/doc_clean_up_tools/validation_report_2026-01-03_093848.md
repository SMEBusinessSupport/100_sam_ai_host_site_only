# Code-to-Documentation Validation Report

Generated: 2026-01-03 09:38:48

---

## Summary

| Metric | Count |
|--------|-------|
| Total Code Elements | 215 |
| Documented | 22 |
| **Undocumented** | **193** |
| Orphan Doc References | 250584 |

---

## Layer Coverage

| Layer | Total | Documented | Coverage |
|-------|-------|------------|----------|
| API MANAGEMENT | 14 | 0 | ❌ 0.0% |
| LOCATION MANAGEMENT | 1 | 0 | ❌ 0.0% |
| DYNAMIC SYSTEM PROMPT CREATION | 4 | 0 | ❌ 0.0% |
| RESPONSE MANAGEMENT | 1 | 0 | ❌ 0.0% |
| SESSION & CONVERSATION | 22 | 1 | ❌ 4.5% |
| MEMORY & KNOWLEDGE | 17 | 1 | ❌ 5.9% |
| AUTHENTICATION & SECURITY | 0 | 0 | ❌ 0% |
| UI & FRONTEND | 0 | 0 | ❌ 0% |

---

## Undocumented Code (Priority Gaps)


### API MANAGEMENT

- `ApiOAuthController` (controller) - \ai_sam_base\controllers\api_oauth_controller.py:35
- `/oauth/<string:vendor>/authorize` (route) - \ai_sam_base\controllers\api_oauth_controller.py:52
- `/oauth/<string:vendor>/callback` (route) - \ai_sam_base\controllers\api_oauth_controller.py:115
- `/oauth/refresh` (route) - \ai_sam_base\controllers\api_oauth_controller.py:345
- `WorkflowCredential` (model) - \ai_sam_base\models\api_credentials.py:13
- `ApiProviderIdentity` (model) - \ai_sam_base\models\api_provider_identity.py:30
- `APIServiceProvider` (model) - \ai_sam_base\models\api_service_provider.py:24
- `BranchAPIController` (controller) - \ai_sam_workflows\controllers\branch_api.py:21
- `/canvas/api/branches/available` (route) - \ai_sam_workflows\controllers\branch_api.py:24
- `/canvas/api/branches/<string:technical_name>/config` (route) - \ai_sam_workflows\controllers\branch_api.py:53
- ... and 4 more

### DYNAMIC SYSTEM PROMPT CREATION

- `DebugSystemPromptController` (controller) - \ai_sam_base\controllers\debug_system_prompt_controller.py:32
- `/sam_ai/debug/system_prompt` (route) - \ai_sam_base\controllers\debug_system_prompt_controller.py:35
- `/sam_ai/debug/system_prompt/full` (route) - \ai_sam_base\controllers\debug_system_prompt_controller.py:92
- `N8NDynamicMenus` (model) - \ai_sam_workflows_base\models\n8n_dynamic_menus.py:9

### LOCATION MANAGEMENT

- `AILocationIntrospector` (model) - \ai_sam_base\models\ai_location_introspector.py:91

### MEMORY & KNOWLEDGE

- `AIAgentKnowledge` (model) - \ai_sam_base\models\ai_agent_knowledge.py:18
- `AiKnowledgeDomain` (model) - \ai_sam_base\models\ai_knowledge_domain.py:4
- `AiKnowledgeSubcategory` (model) - \ai_sam_base\models\ai_knowledge_subcategory.py:4
- `AIMemoryConfig` (model) - \ai_sam_base\models\ai_memory_config.py:13
- `AIMemoryImportWizard` (model) - \ai_sam_base\models\ai_memory_import_wizard.py:12
- `AIMemorySearchLog` (model) - \ai_sam_base\models\ai_memory_search_log.py:16
- `AIMemoryUninstallWizard` (model) - \ai_sam_base\models\ai_memory_uninstall_wizard.py:9
- `/memory/graph/view` (route) - \ai_sam_base\controllers\memory\memory_graph_controller.py:13
- `/memory/graph/diagnostic` (route) - \ai_sam_base\controllers\memory\memory_graph_controller.py:20
- `/memory/graph/test/checkpoint1` (route) - \ai_sam_base\controllers\memory\memory_graph_controller.py:57
- ... and 6 more

### RESPONSE MANAGEMENT

- `/sam/permission_response` (route) - \ai_sam_base\controllers\sam_ai_chat_controller.py:695

### SESSION & CONVERSATION

- `/sam/create_conversation` (route) - \ai_sam_base\controllers\canvas_controller.py:164
- `/sam/get_conversation_messages` (route) - \ai_sam_base\controllers\canvas_controller.py:213
- `SAMSessionController` (controller) - \ai_sam_base\controllers\sam_session_controller.py:19
- `/sam/session/get_history` (route) - \ai_sam_base\controllers\sam_session_controller.py:22
- `/sam/session/load` (route) - \ai_sam_base\controllers\sam_session_controller.py:125
- `/sam/session/save` (route) - \ai_sam_base\controllers\sam_session_controller.py:174
- `/sam/session/delete` (route) - \ai_sam_base\controllers\sam_session_controller.py:248
- `/sam/session/close` (route) - \ai_sam_base\controllers\sam_session_controller.py:288
- `/sam/session/clear_all` (route) - \ai_sam_base\controllers\sam_session_controller.py:333
- `/sam/session/export` (route) - \ai_sam_base\controllers\sam_session_controller.py:363
- ... and 11 more

### UNKNOWN

- `/sam/environment/config` (route) - \ai_sam_base\controllers\canvas_controller.py:12
- `/canvas/platform/config` (route) - \ai_sam_base\controllers\canvas_controller.py:57
- `/canvas/platform/list` (route) - \ai_sam_base\controllers\canvas_controller.py:78
- `/canvas/open` (route) - \ai_sam_base\controllers\canvas_controller.py:90
- `/canvas/set_platform` (route) - \ai_sam_base\controllers\canvas_controller.py:113
- `/canvas/load_nodes` (route) - \ai_sam_base\controllers\canvas_controller.py:125
- `/sam/get_all_conversations` (route) - \ai_sam_base\controllers\canvas_controller.py:184
- `/sam/send_message` (route) - \ai_sam_base\controllers\canvas_controller.py:244
- `/sam/widget/open_sidebar` (route) - \ai_sam_base\controllers\canvas_controller.py:271
- `/sam/widget/close_sidebar` (route) - \ai_sam_base\controllers\canvas_controller.py:287
- ... and 126 more

---

## Orphan Documentation References

These are referenced in docs but may not exist in code:

- `the_ai_automator` in \00_vision\250928_existing_consolidation_and_regroup_of_files.md
- `n8n_` in \00_vision\250928_existing_consolidation_and_regroup_of_files.md
- `the_ai_automator` in \00_vision\250928_existing_consolidation_and_regroup_of_files_1.md
- `n8n_` in \00_vision\250928_existing_consolidation_and_regroup_of_files_1.md
- `pg_dump` in \00_vision\BACKUP_RESTORE_HANDOVER.md
- `xlsxwriter` in \00_vision\BACKUP_RESTORE_HANDOVER.md
- `openpyxl` in \00_vision\BACKUP_RESTORE_HANDOVER.md
- `subprocess` in \00_vision\BACKUP_RESTORE_HANDOVER.md
- `shutil` in \00_vision\BACKUP_RESTORE_HANDOVER.md
- `zipfile` in \00_vision\BACKUP_RESTORE_HANDOVER.md
- `json` in \00_vision\BACKUP_RESTORE_HANDOVER.md
- `pg_dump` in \00_vision\BACKUP_RESTORE_HANDOVER.md
- `psql` in \00_vision\BACKUP_RESTORE_HANDOVER.md
- `pg_dump` in \00_vision\BACKUP_RESTORE_HANDOVER.md
- `psql` in \00_vision\BACKUP_RESTORE_HANDOVER.md
- `ai_brain` in \00_vision\BACKUP_RESTORE_HANDOVER.md
- `ai_toolbox` in \00_vision\CLEANUP_SUMMARY.md
- `DELETE` in \00_vision\CLEANUP_SYSTEM_README.md
- `COLLISION` in \00_vision\CLEANUP_SYSTEM_README.md
- `DEPRECATED` in \00_vision\CLEANUP_SYSTEM_README.md

... and 250564 more

---

## Recommendations

1. Focus on layers with <30% coverage first
2. Document models and controllers before methods
3. Review orphan references - may indicate outdated docs
4. Re-run this validator after documentation updates