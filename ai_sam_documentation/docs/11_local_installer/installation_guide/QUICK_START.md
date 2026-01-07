# SAM AI GitHub Setup - Quick Start

## One Command to Rule Them All

```powershell
cd C:\Users\total\installer
powershell -ExecutionPolicy Bypass -File .\setup_github_complete.ps1
```

This handles everything automatically with prompts at each step.

## What It Does

1. ✅ Checks if GitHub CLI installed (installs if needed)
2. ✅ Authenticates with GitHub
3. ✅ Creates 12 repositories (00-11)
4. ✅ Pushes all modules with 3 branches each
5. ✅ Full logging for troubleshooting

## Alternative: Step-by-Step

If you prefer manual control:

### 1. Install GitHub CLI
```powershell
powershell -ExecutionPolicy Bypass -File .\install_github_cli_alternative.ps1
```
*Uses winget (fastest) or opens browser for manual download*

### 2. Authenticate
```powershell
gh auth login
```
*Opens browser, follow prompts*

### 3. Create Repos
```powershell
powershell -ExecutionPolicy Bypass -File .\create_github_repos.ps1
```
*Creates 12 repos on GitHub*

### 4. Push Modules
```powershell
powershell -ExecutionPolicy Bypass -File .\push_modules_to_github.ps1
```
*Commits and pushes all code*

### 5. Set Branch Protection
*Follow: `GITHUB_GUARDIAN_SETUP.md` (web interface, 5 minutes)*

## Your Repository Structure

```
Public Repos (Free Access):
  00 → odoo-18-lightweight-core (15 modules)
  01 → odoo-18-standard-modules (643 modules)
  02 → odoo-18-community-extras (reserved)
  04 → samai-brain (foundation)
  05 → samai-core-free (free tier)

Private Repos (Paid Tiers):
  03 → odoo-18-user-apps-manager (dynamic)
  06 → samai-starter (€97/month)
  07 → samai-professional (€497/month)
  08 → samai-enterprise (€1147/month)
  09 → samai-memory-chromadb (€49/month, NO Docker)
  10 → samai-vector-store (€79/month, reserved)
  11 → samai-graph-memory (€99/month, Docker)
```

## After Setup

Your local structure stays the same:
```
D:\Odoo-18-SaaS\modules\00-11\
```

Each path becomes a Git repo connected to GitHub with 3 branches:
- **main** - Production (2 approvals required)
- **staging** - Pre-production (1 approval required)
- **dev** - Active development (no restrictions)

## Team Workflow

```
Developer → commit to dev
         → PR: dev → staging (QA tests, 1 approval)
         → PR: staging → main (Production, 2 approvals)
```

## Future: Custom Customer Repos

When you need per-customer modules:

```powershell
# Create custom repo
gh repo create samai-custom-acme-corp --private

# Clone to modules folder
cd D:\Odoo-18-SaaS\modules
git clone https://github.com/YOUR-ORG/samai-custom-acme-corp.git custom-acme-corp

# Add to database (not config file!)
# Addon paths loaded dynamically from database at runtime
```

No config editing needed - paths managed via database for infinite scalability.

## Logs

All scripts create timestamped logs:
```
C:\Users\total\installer\*_log_YYYYMMDD_HHMMSS.txt
```

Check logs if anything goes wrong.

## Help

- GitHub CLI docs: https://cli.github.com/manual/
- Full workflow: [GITHUB_SETUP_WORKFLOW.md](GITHUB_SETUP_WORKFLOW.md)
- Branch protection: [GITHUB_GUARDIAN_SETUP.md](GITHUB_GUARDIAN_SETUP.md)
- Architecture: [README_GITHUB_SETUP.md](README_GITHUB_SETUP.md)

---

*Last updated: 2025-11-07*
