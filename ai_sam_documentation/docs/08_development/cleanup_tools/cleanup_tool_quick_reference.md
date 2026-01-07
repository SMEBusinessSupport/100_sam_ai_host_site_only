# Cleanup Marker Tool - Quick Reference Card

## Commands

```bash
# Apply markers from audit
python cleanup_marker.py --audit audit.json --path ./module

# Preview (dry run)
python cleanup_marker.py --audit audit.json --path ./module --dry-run

# Count markers
python cleanup_marker.py --count --path ./module

# Remove all markers
python cleanup_marker.py --clean --path ./module

# Generate sample audit JSON
python cleanup_marker.py --sample > audit.json
```

## Search Commands

```bash
# Find all cleanup tasks
grep -rn "CLEANUP:" --include="*.py" .

# Find by severity
grep -rn "CLEANUP:RED" --include="*.py" .      # Critical
grep -rn "CLEANUP:ORANGE" --include="*.py" .   # High
grep -rn "CLEANUP:YELLOW" --include="*.py" .   # Medium
grep -rn "CLEANUP:GREEN" --include="*.py" .    # Low

# Find by type
grep -rn "CLEANUP:.*:DELETE" --include="*.py" .
grep -rn "CLEANUP:.*:DRY" --include="*.py" .
```

## Severity Levels

| Color | Meaning | Action |
|-------|---------|--------|
| RED | Critical/Blocking | Fix NOW |
| ORANGE | High Priority | Fix this sprint |
| YELLOW | Medium Priority | Backlog |
| GREEN | Low Priority | When time permits |
| BLUE | Info only | Read for context |

## Cleanup Types

**Critical (RED):**
`DELETE` `COLLISION` `SECURITY` `BREAKING`

**High Priority (ORANGE):**
`DEPRECATED` `MIGRATE` `DEAD_CODE` `WRONG_TYPE`

**Medium Priority (YELLOW):**
`DRY` `EXTRACT` `REFACTOR` `CONSOLIDATE` `TODO`

**Low Priority (GREEN):**
`OPTIMIZE` `SPLIT` `MERGE` `DOCUMENT` `STYLE`

## Visual Borders

```
RED:    # ============================================================
ORANGE: # ------------------------------------------------------------
YELLOW: # ............................................................
GREEN:  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
```

## Annotation Format

```
# [CLEANUP:SEVERITY:TYPE] Title
# Reason: Why this is flagged
# Action:
#   1. First step
#   2. Second step
# Verify: Optional verification command
# Ticket: ID | Audit: Date
```

## Developer Workflow

1. `grep -rn "CLEANUP:RED" .` - Find critical issues
2. Open file at line number
3. Read annotation
4. Execute actions
5. Delete annotation
6. Commit with ticket ID

## Files in This Package

- `cleanup_marker.py` - The tool
- `USER_GUIDE.md` - Full documentation
- `QUICK_REFERENCE.md` - This card
- `sample_audit.json` - Example audit format
