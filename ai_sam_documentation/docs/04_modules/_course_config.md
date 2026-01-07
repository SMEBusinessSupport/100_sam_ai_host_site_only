#  Course Config

**Original file:** `_course_config.json`
**Type:** JSON

---

```json
{
  "_meta": {
    "description": "Configuration for auto-generated courses",
    "updated": "2025-01-02"
  },
  "courses": {
    "00_sam_skills": {
      "name": "SAM Skills",
      "description": "Agent capabilities and skills documentation",
      "channel_type": "training",
      "sequence": 0,
      "visibility": "members",
      "enroll": "invite"
    },
    "01_modules": {
      "name": "Modules",
      "description": "Per-module reference documentation",
      "channel_type": "training",
      "sequence": 10,
      "visibility": "members",
      "enroll": "invite"
    },
    "02_data_flows": {
      "name": "Data Flows",
      "description": "How data moves through the system",
      "channel_type": "training",
      "sequence": 20,
      "visibility": "members",
      "enroll": "invite"
    },
    "03_platform_skins": {
      "name": "Platform Skins",
      "description": "How platform skins work",
      "channel_type": "training",
      "sequence": 30,
      "visibility": "members",
      "enroll": "invite"
    },
    "04_architecture": {
      "name": "Architecture",
      "description": "High-level patterns and decisions",
      "channel_type": "training",
      "sequence": 40,
      "visibility": "members",
      "enroll": "invite"
    },
    "05_vision": {
      "name": "Vision",
      "description": "Strategic direction",
      "channel_type": "training",
      "sequence": 50,
      "visibility": "members",
      "enroll": "invite"
    }
  },
  "defaults": {
    "channel_type": "training",
    "visibility": "members",
    "enroll": "invite",
    "allow_comment": false
  }
}

```
