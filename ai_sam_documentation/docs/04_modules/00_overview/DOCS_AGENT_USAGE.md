# `/docs` Agent - Quick Start Guide

## 🚀 What It Does

**The Documentation Master (`/docs`) protects your time by:**
1. Learning SAM AI structure automatically (like Odoo does)
2. Detecting changes since last run (modules, schema, agents)
3. Finding misalignments (wrong module references, redundant files)
4. Auto-correcting safe issues (removes wrong references)
5. Updating master documentation (current_state.md, etc.)
6. Ensuring boardroom agents arrive INFORMED, not naive

---

## 📋 Setup (One-Time)

### Step 1: Upgrade ai_sam_docs Module

```bash
python ai_toolbox/start_odoo.py --upgrade ai_sam_docs
```

This installs:
- `documentation.intelligence` model (Python brain)
- Intelligence views (Odoo UI)
- Security rules

### Step 2: Verify Agent Installation

```bash
# Check agent exists
dir "C:\Users\total\.claude\agents\documentation-master"

# Should show:
#  - agent.json
#  - documentation_intelligence.md
#  - current_state_rules.md
#  - misalignment_detection.md
#  - boardroom_context_protocol.md
#  - docs_agent_workflow.md
```

### Step 3: Verify Slash Command

```bash
# In Claude Code, type:
/docs

# Should invoke Documentation Master agent
```

---

## 🎯 How to Use

### Method 1: Slash Command (Recommended)

**In Claude Code conversation:**
```
/docs
```

**What happens:**
1. Agent discovers current state (modules, schema, agents)
2. Detects changes since last run
3. Finds misalignments (wrong references, etc.)
4. Auto-fixes safe issues
5. Reports what needs your decision
6. Updates all master documentation
7. Pushes to GitHub

**Duration:** ~2-3 minutes

**Output:**
```
📊 SUMMARY

Current State:
  - Modules: 14 active, 3 excluded
  - Models: 23
  - Agents: 11 (87,450 words)

Auto-Fixes Applied: 2
Requires Anthony: 1

REQUIRES YOUR DECISION ⚠️:
  - ai_sam_odoo/index.html (misaligned location)
    Suggestion: Move to static/src/ or delete
    Your call: Keep? Move? Delete?
```

---

### Method 2: Odoo UI (For Reports)

**Access via Odoo:**
1. Navigate to: **SAM AI Docs → Documentation Intelligence**
2. Click "New" or "Run Analysis"
3. System executes 7-phase workflow
4. View detailed report

**Reports include:**
- Current state snapshot
- Changes detected
- Misalignments found
- Auto-fixes applied
- Items needing your decision

---

### Method 3: Python (Programmatic)

**In Odoo shell:**
```python
# Run intelligence analysis
analysis = env['documentation.intelligence'].run_intelligence_analysis()

# View results
print(f"Modules: {analysis.total_modules}")
print(f"Models: {analysis.total_models}")
print(f"Agents: {analysis.total_agents}")
```

---

## 📅 When to Run

### Daily (Recommended)
- **Morning:** `/docs` to see overnight changes
- **Before work:** Ensure boardroom agents have latest state

### After Changes
- **Module upgrade:** Run `/docs` to update schema
- **Agent modification:** Run `/docs` to detect knowledge changes
- **File moves:** Run `/docs` to check for misalignments

### Before Boardroom Sessions
- **Before CTO:** Ensure infrastructure state current
- **Before COS:** Ensure agent ecosystem current
- **Before CMO:** Ensure feature state current

---

## 🔍 What Gets Analyzed

### 1. Modules (Odoo-Aware)
- Discovers via `__manifest__.py` detection
- Learns dependency graph
- Tracks version changes

**Example:**
```
Found 14 modules:
✅ ai_brain (18.0.1.0.0)
✅ ai_sam (18.0.2.1.0)
✅ ai_sam_memory (18.0.1.3.0) ← Updated!
```

### 2. Schema (Database Models)
- Scans `models/*.py` for `_name` declarations
- Tracks model additions/removals
- Counts total per module

**Example:**
```
Schema:
- ai_brain: 3 models
- ai_sam: 5 models
- ai_sam_memory: 4 models (+ ai.memory.config NEW)
```

### 3. Agents (Claude Ecosystem)
- Discovers via `agent.json` detection
- Counts knowledge files and words
- Tracks agent updates

**Example:**
```
Agents:
- cmo: 5 files, 13,200 words (updated +750)
- developer: 7 files, 16,230 words
- cto: 5 files, 8,900 words
```

### 4. Misalignments (Problems)
- Wrong module references in agent knowledge
- Redundant files in wrong locations
- Future state leaks (exists but inactive)

**Example:**
```
Misalignments:
❌ developer/odoo_patterns.md references "th_ai_automator" (moved)
❌ ai_sam_odoo/index.html (should be in static/src/)
⚠️ ai_sam_desktop exists but NOT ACTIVE (future)
```

---

## ✅ What Gets Auto-Fixed

**Safe to auto-fix (no approval needed):**
1. Remove wrong module references from agent knowledge
   - Example: Remove "th_ai_automator" from developer
2. Document future paths as excluded
   - Example: Mark ai_sam_desktop as "IGNORE (future)"
3. Update current_state.md with latest facts

**Requires your approval:**
1. Move files to different locations
   - Example: Move index.html to static/src/
2. Delete files
   - Example: Remove redundant index.html
3. Structural changes to modules

---

## 📊 Generated Documentation

### Files Updated by `/docs`:

**1. `current_state.md`** (Boardroom context)
- Entrypoint (ai_sam_odoo)
- Active modules (14)
- Excluded paths (3)
- Recent changes
- Agent ecosystem state

**2. `module_architecture.md`**
- Dependency graph (ai_brain → ai_sam → branches)
- Module versions
- Architecture diagram

**3. `database_schema.md`**
- Models per module (23 total)
- Model technical names
- Schema evolution

**4. `agent_registry.md`**
- Agent list (11 agents)
- Knowledge file counts
- Total word counts

**5. `excluded_paths.md`**
- Future modules (ai_sam_desktop, ai_sam_mobile)
- Moved modules (th_ai_automator)
- Quarantine (uncertain_files)

---

## 🚨 Troubleshooting

### Issue: "Module not found error"
**Fix:**
```bash
# Ensure ai_sam_docs is upgraded
python ai_toolbox/start_odoo.py --upgrade ai_sam_docs
```

### Issue: "Agent not found"
**Fix:**
```bash
# Check agent folder exists
dir "C:\Users\total\.claude\agents\documentation-master"

# If missing, re-run agent creation
```

### Issue: "Git push failed"
**Fix:**
```bash
# Check GitHub credentials
git config --list | findstr user

# Manually push if needed
cd "C:\Working With AI\ai_sam\ai_sam_odoo\ai_sam_docs"
git add docs/*.md
git commit -m "Update documentation"
git push
```

### Issue: "Boardroom agents still naive"
**Fix:**
```bash
# Verify current_state.md exists
type "C:\Working With AI\ai_sam\ai_sam_odoo\ai_sam_docs\docs\current_state.md"

# Re-run /docs if missing
```

---

## 🎯 Success Indicators

**`/docs` is working when:**
- ✅ Boardroom agents stop asking "what modules do you have?"
- ✅ Agents don't reference `th_ai_automator`, `ai_sam_desktop`, etc.
- ✅ You spend 0 time explaining "what exists"
- ✅ Documentation is always current (< 24 hours old)
- ✅ Auto-fixes > manual fixes (>80%)

**Warning signs:**
- ❌ Agents ask about infrastructure
- ❌ Agents reference excluded modules
- ❌ Documentation is stale (>48 hours)
- ❌ You're manually fixing agent knowledge

---

## 💡 Pro Tips

### Tip 1: Run Before Boardroom Sessions
```
/docs
[Wait 2-3 minutes]
/cto [your question]  ← CTO arrives informed!
```

### Tip 2: Check Reports in Odoo
- Navigate to: SAM AI Docs → Documentation Intelligence
- View historical analyses
- Track ecosystem evolution

### Tip 3: Scheduled Daily Run
**Set up cron (future enhancement):**
```python
# Run every morning at 8 AM
@cron('0 8 * * *')
def run_daily_intelligence():
    env['documentation.intelligence'].run_intelligence_analysis()
```

### Tip 4: Integrate with QA Workflow
```bash
# After code changes
python ai_toolbox/ai_sam_development_qa.py  # QA check
/docs  # Update documentation
```

---

## 📈 Impact Metrics

**Before `/docs`:**
- CTO/COS/CMO asked about infrastructure: ~10 min/session
- Agent naivety: High (frequent "what modules?" questions)
- Documentation: Stale (weeks old)
- Your time spent explaining: ~2-3 hours/week

**After `/docs`:**
- Boardroom context loading: Automatic
- Agent naivety: Zero
- Documentation: Always current (< 24 hours)
- Your time saved: ~2-3 hours/week

**ROI:** 2-3 hours/week saved = **8-12 hours/month = 96-144 hours/year**

---

## 🎉 Quick Win Commands

**Daily routine:**
```
/docs                    # Update ecosystem state
/cto infrastructure     # CTO arrives informed
/cos agent-health       # COS knows current agents
/cmo feature-status     # CMO knows current features
```

**After module work:**
```
python ai_toolbox/ai_sam_development_qa.py --upgrade
/docs
# All documentation now current ✅
```

**Before important decisions:**
```
/docs
# Ensure boardroom has latest state
/cto [strategic question]
/cmo [marketing question]
# Responses based on TRUTH, not assumptions
```

---

## ✅ Checklist: Is `/docs` Working?

- [ ] Can invoke `/docs` in Claude Code
- [ ] 7-phase workflow completes (~2-3 min)
- [ ] `current_state.md` updated
- [ ] Boardroom agents don't ask "what modules?"
- [ ] Auto-fixes applied (check reports)
- [ ] GitHub synced (check commits)
- [ ] Odoo reports accessible

**All checked?** `/docs` is protecting your time! 🎯

---

**Questions?** Ask `/docs` itself - she knows her own capabilities!
