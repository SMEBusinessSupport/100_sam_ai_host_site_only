# Docker SaaS Infrastructure Session Report
**Date:** 2026-01-06
**Session Focus:** Local SaaS simulation environment setup

---

## Executive Summary

This session established a complete local Docker-based SaaS simulation environment on the developer's Windows desktop. The setup allows testing the full Webkul SaaS Kit provisioning flow before deploying to production (Hetzner).

---

## Infrastructure Created

### Docker Images Built

| Image | Tag | Purpose |
|-------|-----|---------|
| `samai-host` | 18.0 | SaaS Host - Control server with Webkul SaaS Kit |
| `samai` | 18.0 | SAM AI Client - Template image for provisioned clients |

### Running Containers

| Container | Port | Image | Role |
|-----------|------|-------|------|
| `saas-host-odoo` | **8071** | samai-host:18.0 | SaaS Admin Panel (SaaS Kit, Plans, Contracts) |
| `saas-host-db` | 5432 (internal) | postgres:15 | Host PostgreSQL database |
| `samai-odoo` | **8070** | samai:18.0 | Standalone SAM AI test client |
| `samai-db` | 5432 (internal) | postgres:15 | Client test PostgreSQL database |

### Access URLs

- **http://localhost:8071** - SaaS Host Admin (create database, install SaaS Kit)
- **http://localhost:8070** - SAM AI Client test instance
- **http://localhost:8069** - Reserved for Windows Odoo desktop

---

## Repository Structure Created

### 101-samai-docker (SAM AI Client Image)
```
D:\SAMAI-18-SaaS\github-repos\101-samai-docker\
├── Dockerfile           # Odoo 18 + SAM AI modules + Python bundle
├── docker-compose.yml   # Standalone client testing (port 8070)
├── build.ps1           # Build script (copies ai_sam, ai_sam_base, sam_ui_theme)
└── samai-modules/      # Staged modules for Docker build
```

**Modules included:** `ai_sam`, `ai_sam_base`, `sam_ui_theme`

### 102-saas-host-docker (SaaS Host Image)
```
D:\SAMAI-18-SaaS\github-repos\102-saas-host-docker\
├── Dockerfile           # Odoo 18 + SaaS Kit + Full Python bundle
├── docker-compose.yml   # Host environment with dev mounts (port 8071)
├── build.ps1           # Build script (copies odoo_saas_kit)
└── host-modules/       # Staged modules for Docker build
```

**Modules included:** `odoo_saas_kit` (Webkul SaaS Kit)

---

## 4-Path Architecture Implementation

Both Docker images follow the desktop installer's proven 4-path architecture pattern (learned from `build_new_exe_file.iss`):

### SaaS Host addons_path:
```
1. /mnt/dev/saas-setup      ← LIVE: D:\...\99-saas-setup (development mount)
2. /mnt/dev/samai-core      ← LIVE: D:\...\05-samai-core (development mount)
3. /mnt/saas-host/samai_core ← Bundled fallback
4. /usr/lib/.../odoo/addons  ← Odoo core
5. /mnt/saas-host/odoo_extras
6. /mnt/saas-host/member_addons
7. /mnt/extra-addons
```

### Development Mounts (Live Editing)
Changes to these Windows folders are **instantly visible** in the container:
- `D:\SAMAI-18-SaaS\github-repos\05-samai-core` → `/mnt/dev/samai-core`
- `D:\SAMAI-18-SaaS\github-repos\99-saas-setup` → `/mnt/dev/saas-setup`

---

## Python Bundle Dependencies

Both images include the full SAM AI Python bundle:

```
# SaaS Kit requirements
docker>=6.0.0
paramiko>=3.0.0

# Core AI APIs
anthropic>=0.18.0
openai>=1.0.0

# Memory System
chromadb>=0.4.22
sentence-transformers>=2.2.0

# Data Processing
pandas>=2.0.0
numpy>=1.24.0
Pillow>=10.0.0

# Web Operations
requests>=2.31.0
httpx>=0.24.0
beautifulsoup4>=4.11.0

# Other
GitPython>=3.1.43
scikit-learn>=1.3.0
```

---

## SaaS Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    DEVELOPER DESKTOP                         │
│  ┌─────────────────────────────────────────────────────────┐│
│  │ Windows Folders (LIVE development)                      ││
│  │  • D:\...\05-samai-core    (SAM AI modules)            ││
│  │  • D:\...\99-saas-setup    (SaaS Kit + configs)        ││
│  └─────────────────────────────────────────────────────────┘│
│                           │                                  │
│                    Docker Desktop                            │
│  ┌─────────────────────────────────────────────────────────┐│
│  │           SaaS HOST (saas-host-odoo:8071)               ││
│  │  • Webkul SaaS Kit                                      ││
│  │  • Manages subscriptions, plans, contracts              ││
│  │  • Provisions new client containers                     ││
│  │  • Dev mounts for live code editing                     ││
│  └──────────────────────┬──────────────────────────────────┘│
│                         │ Spawns via Docker API              │
│           ┌─────────────┼─────────────┐                      │
│           ▼             ▼             ▼                      │
│     ┌──────────┐  ┌──────────┐  ┌──────────┐                │
│     │ Client 1 │  │ Client 2 │  │ Client N │                │
│     │ samai:   │  │ samai:   │  │ samai:   │                │
│     │ 18.0     │  │ 18.0     │  │ 18.0     │                │
│     │ Port:    │  │ Port:    │  │ Port:    │                │
│     │ 8072     │  │ 8073     │  │ 807X     │                │
│     └──────────┘  └──────────┘  └──────────┘                │
│                                                              │
│  ┌─────────────────────────────────────────────────────────┐│
│  │        Test Client (samai-odoo:8070) - Standalone       ││
│  └─────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────┘
```

---

## Current State & Next Steps

### Completed
- [x] Created SaaS Host Docker setup (Dockerfile + compose)
- [x] Built `samai-host:18.0` image with SaaS Kit + Python bundle
- [x] Built `samai:18.0` client image with SAM AI modules
- [x] Started host container with development mounts
- [x] Verified live code editing capability from Windows

### Pending (Next Session)
- [ ] Access http://localhost:8071 and create SaaS Host database
- [ ] Install `odoo_saas_kit` module from Apps
- [ ] Configure SaaS Server to use `samai:18.0` as client template
- [ ] Create a test SaaS Plan
- [ ] Test client provisioning flow (trigger new container creation)

---

## Quick Start Commands

### Start SaaS Host Environment
```powershell
cd D:\SAMAI-18-SaaS\github-repos\102-saas-host-docker
docker-compose up -d
```

### Rebuild After Code Changes
```powershell
# For host image (if Dockerfile changed)
cd D:\SAMAI-18-SaaS\github-repos\102-saas-host-docker
.\build.ps1
docker-compose down && docker-compose up -d

# For client image
cd D:\SAMAI-18-SaaS\github-repos\101-samai-docker
.\build.ps1
```

### View Container Logs
```powershell
docker logs -f saas-host-odoo
docker logs -f samai-odoo
```

### Stop All SaaS Containers
```powershell
docker-compose -f D:\SAMAI-18-SaaS\github-repos\102-saas-host-docker\docker-compose.yml down
docker-compose -f D:\SAMAI-18-SaaS\github-repos\101-samai-docker\docker-compose.yml down
```

---

## Key Files Reference

| File | Purpose |
|------|---------|
| `102-saas-host-docker/Dockerfile` | SaaS Host image definition |
| `102-saas-host-docker/docker-compose.yml` | Host container + dev mounts |
| `102-saas-host-docker/build.ps1` | Build script for host image |
| `101-samai-docker/Dockerfile` | SAM AI Client image definition |
| `101-samai-docker/docker-compose.yml` | Standalone client testing |
| `101-samai-docker/build.ps1` | Build script for client image |
| `99-saas-setup/odoo_saas_kit/` | Webkul SaaS Kit module |
| `05-samai-core/` | All SAM AI modules |

---

## Notes for Next Session

1. **Database Creation Required**: First access to http://localhost:8071 will show Odoo database creation form. Create a database named `saas_host`.

2. **Module Installation**: After database creation, go to Apps → Update Apps List, then search and install `odoo_saas_kit`.

3. **SaaS Server Configuration**: In SaaS Kit settings, configure:
   - Docker image: `samai:18.0`
   - Base port: 8072 (or next available)
   - Database template settings

4. **Live Development**: Any changes to files in `05-samai-core` or `99-saas-setup` are immediately visible in the container. Restart Odoo service or update module to apply Python changes.

5. **Port Conflicts**: Ensure ports 8070, 8071, and 8072+ are not used by other applications.
