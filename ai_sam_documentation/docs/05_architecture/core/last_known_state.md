# Last Known State

**Original file:** `last_known_state.json`
**Type:** JSON

---

```json
{
  "timestamp": "2025-10-13T15:30:00",
  "scan_type": "full_discovery",
  "entrypoint": "C:\\Working With AI\\ai_sam\\ai_sam",

  "modules": {
    "sam_ai_core": {
      "ai_brain": {
        "version": "18.0.3.8.0",
        "depends": ["base", "mail", "web"],
        "application": true,
        "model_count": 40,
        "summary": "Core data layer - ALL models live here (The Brain)"
      },
      "ai_sam": {
        "version": "18.0.5.3.0",
        "depends": ["base", "web", "ai_brain"],
        "application": true,
        "model_count": 10,
        "summary": "SAM AI Core Framework - Canvas, AI services, intelligence"
      },
      "ai_sam_memory": {
        "version": "18.0.1.0.0",
        "depends": ["ai_brain", "ai_sam"],
        "application": false,
        "model_count": 7,
        "summary": "Knowledge graph platform (Apache AGE + ChromaDB)"
      },
      "ai_sam_workflows": {
        "version": "18.0.1.0.1",
        "depends": ["ai_brain", "ai_sam"],
        "application": false,
        "summary": "N8N workflow platform skin (1,500+ connectors)"
      },
      "ai_sam_creatives": {
        "version": "18.0.1.0.1",
        "depends": ["ai_brain", "ai_sam"],
        "application": false,
        "summary": "Creative content generation platform"
      },
      "ai_sam_socializer": {
        "version": "18.0.2.0.0",
        "depends": ["base", "web", "website_blog", "ai_brain", "ai_sam"],
        "application": false,
        "model_count": 3,
        "summary": "Social media & blogging platform"
      },
      "ai_sam_messenger": {
        "version": "18.0.1.0.0",
        "depends": ["web", "mail"],
        "application": false,
        "summary": "Messenger toggle utility"
      },
      "ai_sam_members": {
        "version": "18.0.1.0.0",
        "depends": ["base", "base_automation", "portal", "website", "mail"],
        "application": true,
        "model_count": 2,
        "summary": "Member signup and management"
      },
      "ai_sam_intelligence": {
        "version": "18.0.1.0.0",
        "depends": ["base", "ai_brain", "ai_sam"],
        "application": true,
        "model_count": 3,
        "summary": "Agent registry and knowledge management"
      },
      "ai_sam_docs": {
        "version": "18.0.2.0.0",
        "depends": ["base", "web", "ai_brain", "ai_sam"],
        "application": false,
        "model_count": 1,
        "summary": "Documentation & development tools"
      },
      "ai_sam_ui": {
        "version": "18.0.1.0.0",
        "depends": ["website", "ai_sam", "ai_brain"],
        "application": false,
        "summary": "Public chat interface for website"
      },
      "github_app": {
        "version": "18.0.1.0.0",
        "depends": ["base"],
        "application": true,
        "model_count": 3,
        "summary": "GitHub module manager integration"
      }
    }
  },

  "agents": {
    "total_count": 10,
    "agents": [
      {"name": "canvas-core-guardian", "knowledge_files": 6, "summary": "Architecture boundary enforcer"},
      {"name": "cmo", "knowledge_files": 5, "summary": "Chief Marketing Officer"},
      {"name": "cto", "knowledge_files": 5, "summary": "Chief Technical Officer"},
      {"name": "documentation-master", "knowledge_files": 5, "summary": "Ecosystem truth keeper"},
      {"name": "github", "knowledge_files": 5, "summary": "GitHub workflow expert"},
      {"name": "odoo-architect", "knowledge_files": 4, "summary": "Solutions architect"},
      {"name": "odoo-audit", "knowledge_files": 4, "summary": "Code quality auditor"},
      {"name": "odoo-debugger", "knowledge_files": 5, "summary": "Debug expert"},
      {"name": "odoo-developer", "knowledge_files": 4, "summary": "Elite Odoo 18 developer"},
      {"name": "recruiter", "knowledge_files": 6, "summary": "Knowledge extraction specialist"},
      {"name": "sam", "knowledge_files": 7, "summary": "SAM AI personality agent"}
    ]
  },

  "excluded_paths": [
    {
      "path": "ai_sam_desktop",
      "reason": "FUTURE - Desktop app (post-MVP)",
      "status": "exists_no_manifest",
      "note": "Folder exists but no __manifest__.py - not an Odoo module yet"
    },
    {
      "path": "ai_sam_mobile",
      "reason": "FUTURE - Mobile app (future roadmap)",
      "status": "exists_no_manifest",
      "note": "Folder exists but no __manifest__.py - not an Odoo module yet"
    },
    {
      "path": "ai_onboarding",
      "reason": "INCOMPLETE - Onboarding workflows",
      "status": "exists_no_manifest",
      "note": "Folder exists but no __manifest__.py - not an Odoo module yet"
    },
    {
      "path": "ai_toolbox",
      "reason": "INCOMPLETE - Utility tools",
      "status": "exists_no_manifest",
      "note": "Folder exists but no __manifest__.py - not an Odoo module yet"
    }
  ],

  "scope_correction": {
    "issue": "Previous state incorrectly referenced two entrypoints",
    "old_entrypoint_1": "C:\\Working With AI\\ai_sam\\ai_sam_odoo",
    "old_entrypoint_1_status": "PATH DOES NOT EXIST",
    "old_entrypoint_2": "C:\\Working With AI\\Odoo Projects\\custom-modules-v18",
    "old_entrypoint_2_status": "OUT OF SCOPE (dev environment, not SAM ecosystem)",
    "corrected_entrypoint": "C:\\Working With AI\\ai_sam\\ai_sam",
    "correction_date": "2025-10-13",
    "correction_reason": "SAM AI ecosystem ONLY lives at ai_sam\\ai_sam\\"
  },

  "misalignments": {
    "wrong_references": [],
    "redundant_files": [],
    "future_leaks": [
      {
        "path": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_sam_desktop",
        "status": "EXISTS but NO MANIFEST",
        "action": "documented_as_excluded",
        "note": "Not an Odoo module yet - safe to ignore"
      },
      {
        "path": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_sam_mobile",
        "status": "EXISTS but NO MANIFEST",
        "action": "documented_as_excluded",
        "note": "Not an Odoo module yet - safe to ignore"
      }
    ],
    "scope_violations": []
  },

  "health_summary": {
    "total_modules": 12,
    "active_modules": 12,
    "incomplete_modules": 4,
    "total_models": "60+",
    "total_agents": 11,
    "misalignments_detected": 0,
    "auto_fixes_applied": 1,
    "requires_manual_action": 0,
    "system_status": "healthy",
    "notes": "Corrected scope - SAM AI ecosystem ONLY at C:\\Working With AI\\ai_sam\\ai_sam\\"
  }
}

```
