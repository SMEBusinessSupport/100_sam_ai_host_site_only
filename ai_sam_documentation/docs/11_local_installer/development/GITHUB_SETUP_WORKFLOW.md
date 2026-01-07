# GitHub Setup Workflow

Complete workflow for setting up 12 GitHub repositories for the unified module structure.

## Prerequisites

1. **GitHub CLI installed** - Download from https://cli.github.com/
2. **Authenticated** - Run `gh auth login` if not already authenticated
3. **Modules migrated** - Run `migrate_to_unified_structure.ps1` first (already completed)

## Step-by-Step Workflow

### Step 1: Create GitHub Repositories

```powershell
cd C:\Users\total\installer
powershell -ExecutionPolicy Bypass -File .\create_github_repos.ps1
```

**What it does:**
- Creates 12 GitHub repositories (paths 00-11)
- Public repos: 00, 01, 02, 04, 05 (free tier + Odoo components)
- Private repos: 03, 06-11 (paid tiers)
- Initializes local Git repos in each path folder
- Sets up remote origins

**You'll be prompted for:**
- Your GitHub username or organization name

### Step 2: Push Modules to GitHub

```powershell
powershell -ExecutionPolicy Bypass -File .\push_modules_to_github.ps1
```

**What it does:**
- Stages all files in each path (00-11)
- Creates initial commit with descriptive message
- Creates `main`, `dev`, and `staging` branches
- Pushes all branches to GitHub

### Step 3: Set Up Branch Protection (Manual)

Follow the guide in `GITHUB_GUARDIAN_SETUP.md` to configure branch protection rules via GitHub web interface.

**Required settings:**
- **Main branch:** 2 approvals required, no direct pushes
- **Staging branch:** 1 approval required
- **Dev branch:** No restrictions (active development)

## Repository Structure Created

```
00 → odoo-18-lightweight-core (public)
01 → odoo-18-standard-modules (public)
02 → odoo-18-community-extras (public)
03 → odoo-18-user-apps-manager (private)
04 → samai-brain (public)
05 → samai-core-free (public)
06 → samai-starter (private)
07 → samai-professional (private)
08 → samai-enterprise (private)
09 → samai-memory-chromadb (private)
10 → samai-vector-store (private)
11 → samai-graph-memory (private)
```

## Workflow Diagram

```
Local: D:\Odoo-18-SaaS\modules\00-11\
           ↓
    [create_github_repos.ps1]
           ↓
    GitHub: 12 repos created + local git init
           ↓
    [push_modules_to_github.ps1]
           ↓
    GitHub: All modules pushed with branches
           ↓
    [Manual: Set up branch protection]
           ↓
    ✅ Production-ready repository structure
```

## Branching Strategy

Each repository will have 3 branches:

- **`main`** - Production code (protected, requires 2 approvals)
- **`staging`** - Pre-production testing (protected, requires 1 approval)
- **`dev`** - Active development (no restrictions)

## Development Workflow

```
Developer makes changes
    ↓
Commit to `dev` branch
    ↓
Create PR: dev → staging
    ↓
QA tests on staging (1 approval needed)
    ↓
Create PR: staging → main
    ↓
Production release (2 approvals needed)
```

## Custom Customer Repos (Future)

For per-customer custom modules (discussed in architecture):

```
Standard Product Repos: paths 00-11 (fixed structure)
           +
Custom Customer Repos: samai-custom-{customer-name}
           ↓
Dynamic addon paths loaded from database at runtime
           ↓
No config file editing required
```

## Logs Generated

All scripts create timestamped logs:
- `github_repos_log_YYYYMMDD_HHMMSS.txt`
- `github_push_log_YYYYMMDD_HHMMSS.txt`

Check these logs if any issues occur.

## Troubleshooting

### "GitHub CLI not authenticated"
```powershell
gh auth login
```

### "Repository already exists"
Script will skip and continue with others. No action needed.

### "No changes to commit"
Path is empty or already committed. Normal for paths 02, 03, 10, 11 (reserved for future).

### Push fails with "403 Forbidden"
Check repository visibility settings and your GitHub permissions.

## Next Steps After Setup

1. **Update installer configuration** - Point to GitHub repos instead of local paths
2. **Notify team members** - Share new repository URLs
3. **Create GitHub Actions** - Automate testing/deployment (optional)
4. **Set up webhooks** - Auto-update user instances when repos update (optional)

---

*Generated: 2025-11-07*
