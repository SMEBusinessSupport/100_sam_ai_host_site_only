# Claude Code Session Guide - AI Toolbox

**For: Future Claude sessions**
**Purpose: Quick onboarding to the AI Toolbox and Odoo V3 architecture**

---

## 🎯 What You Need to Know

### The Core Tool: claude_qa.py

This is **THE MACHINE** - the QA testing tool that validates everything before code touches Odoo.

**What it does:**
- ✅ Validates XML, Python, JavaScript, manifest files
- ✅ Checks V3 architecture compliance (ai_base → ai_trunk → branches)
- ✅ Validates hook exports (prevents AttributeError at install)
- ✅ Tracks version increments
- ✅ Can auto-upgrade modules if QA passes

**Key command:**
```bash
cd "C:\Working With AI\Odoo Projects\custom-modules-v18\ai_automator_docs\ai_toolbox"
python claude_qa.py --upgrade --yes
```

**This one command:**
1. Runs comprehensive QA validation
2. If PASS: Automatically upgrades modules
3. If FAIL: Shows exactly what to fix

---

## 🌳 Architecture Overview

### V3 Structure (The SAM AI Tree)

```
ai_base (The Roots)
    ↓ provides data models
ai_trunk (The Trunk)
    ↓ provides framework + SAM AI Core
Branch Modules (ai_poppy, ai_sam, etc.)
```

**Critical Rules:**
- ai_trunk MUST depend on ai_base (not ai_automator_base - that's V2!)
- Branch modules depend on ai_trunk or ai_canvas_skeleton
- NO mixing V2 (ai_automator_base) with V3 (ai_base)

**QA enforces these rules automatically.**

---

## 🛠️ The 5 Essential Tools

### 1. claude_qa.py - Pre-flight Testing
```bash
# Quick check
python claude_qa.py

# With version tracking and reports
python claude_qa.py --check-version --report

# Full workflow: QA + auto-upgrade
python claude_qa.py --upgrade --yes

# Specific modules only
python claude_qa.py --modules ai_trunk --upgrade --yes
```

### 2. start_odoo.py - Server Operations
```bash
# Normal start
python start_odoo.py

# Test startup
python start_odoo.py --test

# Install module
python start_odoo.py --install ai_base

# Upgrade module
python start_odoo.py --upgrade ai_trunk

# Dev mode (auto-reload XML)
python start_odoo.py --dev xml
```

### 3. odoo_toolbox.py - Live Debugging
```bash
# Interactive mode (easiest)
python odoo_toolbox.py interactive

# Check specific menu
python odoo_toolbox.py sql --check menu --name "SAM AI"

# Check model
python odoo_toolbox.py sql --check model --name "ai.conversation"
```

### 4. odoo_log_analyzer.py - Post-error Analysis
```bash
# Analyze recent errors (last 200 lines)
python odoo_log_analyzer.py --log "path/to/odoo.log" --tail 200

# Filter specific errors
python odoo_log_analyzer.py --log "path/to/odoo.log" --filter "ValueError"
```

### 5. module_tools.py - Module Documentation
```bash
# Generate docs
python module_tools.py docs --module ../ai_base

# Validate dependencies
python module_tools.py validate --module ../ai_base --other ../ai_trunk
```

---

## 🚨 Common Issues & Solutions

### Issue 1: Module Won't Install (AttributeError Hook)

**Error:** `RPC_ERROR: module 'odoo.addons.MODULE' has no attribute 'hook_function'`

**Solution:**
```python
# __init__.py must export hooks at module level
from . import hooks
from .hooks import post_init_hook  # Add this line!
```

**Prevention:** QA now catches this automatically!

### Issue 2: Invalid Version Format

**Error:** `Version '3.0.0.0' MUST start with '18.0.' for Odoo 18`

**Solution:**
```python
# __manifest__.py
'version': '18.0.3.0.0',  # Must start with 18.0
```

### Issue 3: Wrong Dependencies (V2 vs V3)

**Error:** `ai_trunk should NOT depend on 'ai_automator_base'`

**Solution:**
```python
# Use V3 dependencies
'depends': ['ai_base'],  # Not ai_automator_base!
```

---

## 📋 Daily Workflow

### Morning: Check & Update
```bash
cd "C:\Working With AI\Odoo Projects\custom-modules-v18\ai_automator_docs\ai_toolbox"

# QA + auto-upgrade all modules
python claude_qa.py --check-version --report --upgrade --yes
```

### During Development: Iterate
```bash
# Work on ai_trunk...
# Make changes...

# Quick QA + upgrade just that module
python claude_qa.py --modules ai_trunk --upgrade --yes
```

### Pre-Commit: Validate
```bash
# Full QA with reports
python claude_qa.py --check-version --report

# Review reports in reports/ folder
```

---

## 🎓 User Expectations

### What the user expects:

1. **Self-checking tools** - Code validates itself before deployment
2. **Minimal manual work** - Automation wherever possible
3. **Clear error messages** - Know exactly what's wrong and how to fix it
4. **Version tracking** - Automatic tracking of changes
5. **One-command workflows** - QA + upgrade in single command

### What the user has created:

A **machine** (`claude_qa.py`) that:
- Validates all code quality
- Enforces architecture rules
- Tracks versions automatically
- Can auto-upgrade if validation passes
- Provides clear, actionable error messages

**The goal:** Claude Code can self-check work before user spends hours on "learnt before" issues.

---

## 📁 File Structure

```
ai_toolbox/
├── claude_qa.py ⭐ (THE MACHINE)
├── start_odoo.py
├── odoo_log_analyzer.py
├── odoo_toolbox.py
├── module_tools.py
├── reinstall_v3.py
├── start_odoo.bat
├── README.md (comprehensive tool docs)
├── QUICK_START.md (quick reference)
├── CHANGELOG.md (development history)
└── reports/
    ├── README.md
    ├── module_versions.json (version tracking)
    └── archive/
        ├── history/ (old historical reports)
        └── old_qa_reports/ (timestamped QA runs)
```

---

## ⚡ Quick Reference Card

| Task | Command |
|------|---------|
| **QA Everything** | `python claude_qa.py` |
| **QA + Upgrade** | `python claude_qa.py --upgrade --yes` |
| **QA One Module** | `python claude_qa.py --modules ai_trunk` |
| **Start Odoo** | `python start_odoo.py` |
| **Debug Menu** | `python odoo_toolbox.py interactive` |
| **Analyze Logs** | `python odoo_log_analyzer.py --log "path" --tail 200` |
| **Gen Docs** | `python module_tools.py docs --module ../MODULE` |

---

## 💡 Key Insights for Claude

### 1. Always Run QA First
Before suggesting code changes, run QA to understand current state:
```bash
python claude_qa.py --modules MODULE_NAME
```

### 2. Version Increments Matter
When modifying a module, always increment the version in `__manifest__.py`:
- Bug fix: `18.0.1.0.0` → `18.0.1.0.1`
- Minor feature: `18.0.1.0.0` → `18.0.1.1.0`
- Major feature: `18.0.1.0.0` → `18.0.2.0.0`

### 3. Hook Exports Are Critical
If adding a hook to `__manifest__.py`, ALWAYS export it in `__init__.py`:
```python
# __manifest__.py
'post_init_hook': 'my_hook',

# __init__.py
from .hooks import my_hook  # REQUIRED!
```

### 4. V3 Architecture is Sacred
- ai_base = data models only
- ai_trunk = framework + SAM AI services
- Branches = specific features (ai_poppy, ai_sam, etc.)

Never mix V2 (ai_automator_base) with V3 (ai_base).

### 5. The QA Tool is the Source of Truth
If QA says it's wrong, it IS wrong. Trust the machine.

---

## 🔧 Special Notes

### Reports Location
All QA reports go to: `reports/`
- JSON format for machines
- TXT format for humans
- `module_versions.json` tracks version history

### External Scripts
The user mentioned wanting external pre/post session cleanup scripts. These are planned but not yet created. The QA tool is the foundation for this future automation.

### The Vision
A tool for Claude Code that allows self-check of work before the user spends hours on "learnt before" issues. The QA tool is **that tool** - use it liberally!

---

## 🎯 Success Metrics

**Before starting work:**
- Read this guide
- Understand the V3 architecture
- Know where the tools are

**During work:**
- Run QA frequently
- Follow version increment rules
- Export hooks properly

**Before finishing:**
- Run full QA with reports
- Ensure all validations pass
- Verify module can upgrade

**Completion criteria:**
```bash
python claude_qa.py --check-version --report --upgrade --yes
# Should result in: [OK] All modules upgraded successfully!
```

---

**Remember:** The user values automation, self-checking code, and minimal manual intervention. The AI Toolbox embodies these values. Use it, trust it, and extend it when needed.

**Primary Goal:** Prevent the user from spending hours on issues we've already solved before.

---

**Last Updated:** October 4, 2025
**For:** Future Claude Code sessions
**Toolbox Version:** 3.0 Enhanced
