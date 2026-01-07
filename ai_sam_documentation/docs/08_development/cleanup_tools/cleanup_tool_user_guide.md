# Cleanup Marker Tool - User Guide

**Version:** 1.0
**Created:** 2025-12-19
**Purpose:** AI-to-Human delegation of code cleanup tasks

---

## Table of Contents

1. [Overview](#1-overview)
2. [Quick Start](#2-quick-start)
3. [The Workflow](#3-the-workflow)
4. [Understanding Severity Levels](#4-understanding-severity-levels)
5. [Understanding Cleanup Types](#5-understanding-cleanup-types)
6. [Creating Audit Reports](#6-creating-audit-reports)
7. [Tool Commands](#7-tool-commands)
8. [Reading Annotations](#8-reading-annotations)
9. [Developer Workflow](#9-developer-workflow)
10. [IDE Integration](#10-ide-integration)
11. [Best Practices](#11-best-practices)
12. [Troubleshooting](#12-troubleshooting)

---

## 1. Overview

### What is this tool?

The Cleanup Marker Tool is a Python utility that:

1. **Injects** color-coded cleanup annotations into code files
2. **Enables** AI auditors to delegate cleanup tasks to human developers
3. **Standardizes** how cleanup tasks are communicated
4. **Tracks** technical debt with searchable markers

### Why use it?

| Problem | Solution |
|---------|----------|
| AI finds issues but humans must fix | Annotations tell developers exactly what to do |
| Cleanup tasks get lost | Searchable markers in code |
| No prioritization | Color-coded severity levels |
| Context switching | Each annotation is self-contained |

### The Big Picture

```
[AI Auditor] --> [Audit Report JSON] --> [Cleanup Marker Tool] --> [Annotated Code]
                                                                        |
                                                                        v
                                                               [Human Developer]
                                                                        |
                                                                        v
                                                                 [Clean Code]
```

---

## 2. Quick Start

### Prerequisites

- Python 3.7+
- No external dependencies (uses only standard library)

### Installation

```bash
# Copy cleanup_marker.py to your project or tools directory
# No pip install needed - it's a standalone script
```

### Your First Cleanup

```bash
# Step 1: Generate a sample audit to see the format
python cleanup_marker.py --sample > my_audit.json

# Step 2: Preview what would be marked (dry run)
python cleanup_marker.py --audit my_audit.json --path ./my_module --dry-run

# Step 3: Apply markers to actual files
python cleanup_marker.py --audit my_audit.json --path ./my_module

# Step 4: Search for tasks
grep -rn "CLEANUP:RED" --include="*.py" ./my_module

# Step 5: After cleanup, remove markers
python cleanup_marker.py --clean --path ./my_module
```

---

## 3. The Workflow

### For AI Auditors (Creating Tasks)

```
1. Audit the codebase
2. Create audit JSON file with findings
3. Run: python cleanup_marker.py --audit audit.json --path ./module
4. Commit annotated code to branch
5. Assign to developer
```

### For Human Developers (Executing Tasks)

```
1. Pull code with markers
2. Search: grep -rn "CLEANUP:RED" .
3. Read annotation (tells you exactly what to do)
4. Execute the action
5. Test changes
6. Delete the annotation comment
7. Commit with ticket reference
```

### For Project Managers (Tracking)

```
1. Run: python cleanup_marker.py --count --path ./module
2. See breakdown by severity
3. Track progress as markers are removed
```

---

## 4. Understanding Severity Levels

### Color-Coded System

| Color | Search Term | When to Use | Action Timeline |
|-------|-------------|-------------|-----------------|
| **RED** | `CLEANUP:RED` | Critical/Blocking issues | Fix immediately |
| **ORANGE** | `CLEANUP:ORANGE` | High priority debt | Fix this sprint |
| **YELLOW** | `CLEANUP:YELLOW` | Medium priority | Plan for backlog |
| **GREEN** | `CLEANUP:GREEN` | Low priority/nice-to-have | When time permits |
| **BLUE** | `CLEANUP:BLUE` | Information only | Read for context |

### Visual Borders

Each severity has a distinct visual pattern:

```python
# RED (Critical):
# ============================================================
# [CLEANUP:RED:DELETE] ...
# ============================================================

# ORANGE (High Priority):
# ------------------------------------------------------------
# [CLEANUP:ORANGE:DEPRECATED] ...
# ------------------------------------------------------------

# YELLOW (Medium Priority):
# ............................................................
# [CLEANUP:YELLOW:DRY] ...
# ............................................................

# GREEN (Low Priority):
# . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
# [CLEANUP:GREEN:SPLIT] ...
# . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
```

---

## 5. Understanding Cleanup Types

### Critical Types (Usually RED)

| Type | Meaning | Example |
|------|---------|---------|
| `DELETE` | Remove file/block entirely | Duplicate class definition |
| `COLLISION` | Name/class collision | Two files define same class |
| `SECURITY` | Security vulnerability | Exposed credentials |
| `BREAKING` | Will break in future | Deprecated API usage |

### High Priority Types (Usually ORANGE)

| Type | Meaning | Example |
|------|---------|---------|
| `DEPRECATED` | Old code to remove | Replaced by new implementation |
| `MIGRATE` | Needs migration | Old field to new model |
| `DEAD_CODE` | Unreachable code | Commented blocks |
| `WRONG_TYPE` | Incorrect type | Model should be Transient |

### Medium Priority Types (Usually YELLOW)

| Type | Meaning | Example |
|------|---------|---------|
| `DRY` | Duplicated logic | Same formula in 5 files |
| `EXTRACT` | Should be utility | Repeated pattern |
| `REFACTOR` | Needs restructuring | God method |
| `CONSOLIDATE` | Merge patterns | Multiple auth approaches |
| `TODO` | Pending implementation | Unfinished feature |

### Low Priority Types (Usually GREEN)

| Type | Meaning | Example |
|------|---------|---------|
| `OPTIMIZE` | Performance improvement | N+1 query |
| `SPLIT` | File too large | 3000+ line file |
| `MERGE` | Combine similar code | Similar wizards |
| `DOCUMENT` | Needs better docs | Complex logic |
| `STYLE` | Code style issue | Inconsistent naming |

---

## 6. Creating Audit Reports

### JSON Structure

```json
{
  "audit_date": "2025-12-19",
  "module": "my_module",
  "score": 6,
  "findings": [
    {
      "id": "CLEANUP-001",
      "severity": "RED",
      "type": "DELETE",
      "file": "models/old_file.py",
      "line": 1,
      "scope": "file",
      "title": "Delete this file",
      "reason": "Why it needs to be deleted",
      "action": [
        "Step 1 to fix",
        "Step 2 to fix",
        "Step 3 to verify"
      ],
      "score_impact": -1,
      "verification": "Optional verification command"
    }
  ]
}
```

### Field Reference

| Field | Required | Description |
|-------|----------|-------------|
| `id` | Yes | Unique ticket ID (e.g., CLEANUP-001) |
| `severity` | Yes | RED, ORANGE, YELLOW, GREEN, or BLUE |
| `type` | Yes | Cleanup type (DELETE, DRY, etc.) |
| `file` | Yes | Relative path from module root |
| `line` | Yes | Line number to annotate |
| `scope` | No | "file", "block", "line", or "method" |
| `title` | Yes | Brief description |
| `reason` | No | Why this is flagged |
| `action` | Yes | Array of steps to fix |
| `score_impact` | No | How this affects audit score |
| `verification` | No | Command to verify fix worked |
| `estimated_time` | No | How long the fix should take |
| `related_files` | No | Other files affected |

### Generating Sample Audit

```bash
# Output sample JSON structure
python cleanup_marker.py --sample

# Save to file
python cleanup_marker.py --sample > template_audit.json
```

---

## 7. Tool Commands

### Apply Markers

```bash
# Apply to module
python cleanup_marker.py --audit audit.json --path ./my_module

# Preview without modifying (dry run)
python cleanup_marker.py --audit audit.json --path ./my_module --dry-run

# Report only (same as dry-run)
python cleanup_marker.py --audit audit.json --path ./my_module --report-only
```

### Count Markers

```bash
# Count all markers in directory
python cleanup_marker.py --count --path ./my_module

# Output:
# ==================================================
#   CLEANUP MARKER COUNT
# ==================================================
#
# MARKERS BY SEVERITY:
#   RED      (CRITICAL       ): 1
#   ORANGE   (HIGH PRIORITY  ): 4
#   YELLOW   (MEDIUM PRIORITY): 5
#   GREEN    (LOW PRIORITY   ): 3
#   ------------------------------
#   TOTAL                   : 13
```

### Remove Markers

```bash
# Remove all markers (after cleanup complete)
python cleanup_marker.py --clean --path ./my_module

# Preview removal (dry run)
python cleanup_marker.py --clean --path ./my_module --dry-run
```

### Search Markers (using grep)

```bash
# Find all cleanup tasks
grep -rn "CLEANUP:" --include="*.py" .

# Find by severity
grep -rn "CLEANUP:RED" --include="*.py" .
grep -rn "CLEANUP:ORANGE" --include="*.py" .

# Find by type
grep -rn "CLEANUP:.*:DELETE" --include="*.py" .
grep -rn "CLEANUP:.*:DRY" --include="*.py" .

# Count by severity
grep -c "CLEANUP:RED" --include="*.py" -r . | grep -v ":0"
```

---

## 8. Reading Annotations

### Anatomy of an Annotation

```python
# ============================================================    <-- Border (indicates severity)
# [CLEANUP:RED:DELETE] ENTIRE FILE FLAGGED FOR DELETION          <-- Tag + Title
# ============================================================    <-- Border
# Reason: Class collision with settings.py                        <-- Why flagged
#
# Action:                                                          <-- What to do
#   1. DELETE this entire file
#   2. Edit __init__.py - remove import
#   3. Test module upgrade
#
# Verify: odoo -u my_module --stop-after-init                     <-- How to verify (optional)
#
# Ticket: CLEANUP-001 | Audit: 2025-12-19 | Score Impact: -1      <-- Metadata
# ============================================================    <-- Border
```

### What Each Part Tells You

| Part | Purpose |
|------|---------|
| **Border** | Visual severity (= for RED, - for ORANGE, . for YELLOW) |
| **Tag** | Searchable marker `[CLEANUP:SEVERITY:TYPE]` |
| **Title** | Brief description of issue |
| **Reason** | Context - why this is a problem |
| **Action** | Numbered steps to fix |
| **Verify** | Optional command to confirm fix worked |
| **Ticket** | Reference ID for tracking |
| **Audit** | When this was flagged |
| **Score Impact** | How fixing this improves audit score |

---

## 9. Developer Workflow

### Step-by-Step Process

```
1. PULL CODE
   git pull origin cleanup-branch

2. FIND YOUR TASKS
   grep -rn "CLEANUP:RED" --include="*.py" .

3. PICK A TASK
   Open file, go to line number shown in grep output

4. READ THE ANNOTATION
   - Title tells you what's wrong
   - Reason tells you why
   - Action tells you exactly what to do

5. EXECUTE THE FIX
   Follow the numbered action steps

6. VERIFY (if provided)
   Run the verification command

7. DELETE THE ANNOTATION
   Remove the entire comment block

8. COMMIT
   git commit -m "CLEANUP-001: Delete duplicate ResConfigSettings"

9. REPEAT
   Move to next task
```

### Example Session

```bash
# Find critical issues
$ grep -rn "CLEANUP:RED" --include="*.py" .
./models/res_config_settings.py:1:# [CLEANUP:RED:DELETE]

# Open file, see annotation:
# ============================================================
# [CLEANUP:RED:DELETE] ENTIRE FILE FLAGGED FOR DELETION
# ============================================================
# Reason: Class collision with settings.py
#
# Action:
#   1. DELETE this entire file
#   2. Edit __init__.py - remove 'from . import res_config_settings'
#   3. Test: odoo -u ai_sam_base --stop-after-init
#
# Ticket: CLEANUP-001 | Audit: 2025-12-19 | Score Impact: -1
# ============================================================

# Execute:
$ rm models/res_config_settings.py
$ # Edit __init__.py, remove import line
$ odoo -u ai_sam_base --stop-after-init  # verify

# Commit:
$ git add -A
$ git commit -m "CLEANUP-001: Delete duplicate res_config_settings.py"
```

---

## 10. IDE Integration

### VS Code - Todo Highlight Extension

Install "Todo Highlight" extension, then add to `.vscode/settings.json`:

```json
{
  "todohighlight.keywords": [
    {
      "text": "CLEANUP:RED",
      "color": "white",
      "backgroundColor": "#FF0000",
      "overviewRulerColor": "#FF0000"
    },
    {
      "text": "CLEANUP:ORANGE",
      "color": "black",
      "backgroundColor": "#FFA500",
      "overviewRulerColor": "#FFA500"
    },
    {
      "text": "CLEANUP:YELLOW",
      "color": "black",
      "backgroundColor": "#FFFF00",
      "overviewRulerColor": "#FFFF00"
    },
    {
      "text": "CLEANUP:GREEN",
      "color": "white",
      "backgroundColor": "#228B22",
      "overviewRulerColor": "#228B22"
    },
    {
      "text": "CLEANUP:BLUE",
      "color": "white",
      "backgroundColor": "#4169E1",
      "overviewRulerColor": "#4169E1"
    }
  ]
}
```

### PyCharm - TODO Settings

1. Go to Settings > Editor > TODO
2. Add patterns:
   - `\bCLEANUP:RED\b` - Red highlighting
   - `\bCLEANUP:ORANGE\b` - Orange highlighting
   - etc.

### Sublime Text

Add to Preferences > Settings:

```json
{
  "highlight_line": true,
  "word_highlight_patterns": [
    "CLEANUP:RED",
    "CLEANUP:ORANGE",
    "CLEANUP:YELLOW",
    "CLEANUP:GREEN"
  ]
}
```

---

## 11. Best Practices

### For AI Auditors

1. **Be specific** - Include exact line numbers and file paths
2. **Be actionable** - Each action step should be executable
3. **Prioritize correctly** - RED is for blocking issues only
4. **Include verification** - How can developer confirm fix worked?
5. **Reference related files** - If change affects multiple files, list them

### For Developers

1. **Start with RED** - Always fix critical issues first
2. **Read the whole annotation** - Don't skip the reason/context
3. **Follow all steps** - Don't skip verification
4. **Delete annotation after fix** - Don't leave stale markers
5. **Reference ticket in commit** - Makes tracking easier

### For Teams

1. **One audit per sprint** - Regular cadence
2. **Track cleanup velocity** - How many markers resolved?
3. **Don't let RED linger** - Critical issues block releases
4. **Celebrate cleanup** - Reducing tech debt is valuable work

---

## 12. Troubleshooting

### "File not found" errors

```
[X] File not found: ./models/missing_file.py
```

**Cause:** Audit JSON references a file that doesn't exist
**Fix:** Update audit JSON with correct file path, or remove the finding

### Markers not showing in search

```bash
$ grep -rn "CLEANUP:" .
# (no output)
```

**Cause:** Markers weren't applied, or wrong directory
**Fix:**
1. Verify markers were applied: `python cleanup_marker.py --count --path .`
2. Check you're in the right directory

### Unicode errors on Windows

```
UnicodeEncodeError: 'charmap' codec can't encode character
```

**Cause:** Windows console can't display Unicode characters
**Fix:** The tool uses ASCII-safe characters. If you see this, update to latest version.

### Annotation appears in wrong place

**Cause:** Line number in audit JSON doesn't match current file
**Fix:** Update line numbers in audit JSON after file changes

### Clean command doesn't remove all markers

**Cause:** Non-standard marker format
**Fix:** Manually search and remove: `grep -rn "CLEANUP:" --include="*.py" .`

---

## Quick Reference Card

```
APPLY MARKERS:    python cleanup_marker.py --audit audit.json --path ./module
PREVIEW:          python cleanup_marker.py --audit audit.json --path ./module --dry-run
COUNT:            python cleanup_marker.py --count --path ./module
REMOVE:           python cleanup_marker.py --clean --path ./module
SAMPLE:           python cleanup_marker.py --sample > audit.json

SEARCH:           grep -rn "CLEANUP:RED" --include="*.py" .
                  grep -rn "CLEANUP:ORANGE" --include="*.py" .
                  grep -rn "CLEANUP:YELLOW" --include="*.py" .
                  grep -rn "CLEANUP:GREEN" --include="*.py" .

SEVERITY:         RED    = Critical (fix now)
                  ORANGE = High (fix this sprint)
                  YELLOW = Medium (backlog)
                  GREEN  = Low (nice to have)
                  BLUE   = Info only

TYPES:            DELETE, COLLISION, SECURITY, BREAKING
                  DEPRECATED, MIGRATE, DEAD_CODE, WRONG_TYPE
                  DRY, EXTRACT, REFACTOR, CONSOLIDATE, TODO
                  OPTIMIZE, SPLIT, MERGE, DOCUMENT, STYLE
```

---

*User Guide v1.0 - Created 2025-12-19*
