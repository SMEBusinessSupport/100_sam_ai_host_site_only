# SAM AI Smart Detection & Installation

## 🎯 Problem Solved

**Before:** Installer would blindly overwrite existing installations, losing custom settings, commands, and agents.

**After:** Installer intelligently detects what's installed, backs up important data, and offers appropriate actions.

---

## 🔍 What Gets Detected

### **1. VS Code**
```
✓ Installed: Yes/No
✓ Version: 1.85.0
✓ Has custom settings: Yes/No
✓ Settings path: C:\Users\...\settings.json

Action:
- If NOT installed → Install
- If installed WITHOUT custom settings → Apply SAM AI settings
- If installed WITH custom settings → Backup first, then apply
```

### **2. Claude Code Extension**
```
✓ Installed: Yes/No

Action:
- If NOT installed → Install from marketplace
- If installed → Skip (no reinstall needed)
```

### **3. Claude Desktop**
```
✓ Installed: Yes/No
✓ Version: 0.14.10
✓ Has custom config: Yes/No
✓ Has MCP servers: Yes/No
✓ Config path: C:\Users\...\claude_desktop_config.json

Action:
- If NOT installed → Install
- If installed WITHOUT MCP servers → Update config
- If installed WITH MCP servers → Backup first, preserve MCP servers
```

### **4. SAM AI Commands**
```
✓ Installed: Yes/No
✓ Count: 20 commands
✓ Is SAM AI: Yes/No (checks for sam.md, developer.md, etc.)
✓ Version: 1.0.0
✓ Commands: [sam, developer, cto, ...]

Action:
- If NOT installed → Install all 20 commands
- If installed (SAM AI) → Backup first, then upgrade
- If installed (other) → Merge (keep existing + add SAM AI)
```

### **5. SAM AI Agents**
```
✓ Installed: Yes/No
✓ Count: 20 agents
✓ Is SAM AI: Yes/No
✓ Agents: [sam, cto, cmo, ...]

Action:
- If NOT installed → Install all 20 agents
- If installed (SAM AI) → Backup first, then upgrade
- If installed (other) → Merge
```

### **6. SAM AI Launcher**
```
✓ Installed: Yes/No
✓ Path: C:\Program Files\SAM AI\sam_ai_launcher.exe

Action:
- If NOT installed → Install
- If installed → Skip
```

---

## 🎭 Installation Modes

Based on detection, installer determines the mode:

### **Mode 1: Fresh Installation**
```
Detection:
- Nothing installed

User sees:
┌─────────────────────────────────────────┐
│ ✓ Fresh Installation Detected           │
│                                          │
│ All components will be installed:        │
│ • VS Code                                │
│ • Claude Code Extension                  │
│ • Claude Desktop                         │
│ • 20 SAM AI Commands                     │
│ • 20 SAM AI Agents                       │
│ • SAM AI Launcher                        │
│                                          │
│ [Install SAM AI (Fresh)]                 │
└─────────────────────────────────────────┘

Action: Install everything
```

### **Mode 2: Upgrade Installation**
```
Detection:
- Most things installed (VS Code, Claude, Commands, Agents)
- Detected as SAM AI installation

User sees:
┌─────────────────────────────────────────┐
│ ⚠ Existing Installation Detected        │
│                                          │
│ Recommendations:                         │
│ ⚠ VS Code has custom settings           │
│   → Will backup before applying          │
│ ⚠ Claude has MCP servers configured      │
│   → Will preserve your servers           │
│ ℹ Found 20 existing commands             │
│   → Will backup and upgrade              │
│                                          │
│ Components:                              │
│ ✓ VS Code (v1.85.0)                      │
│   Has custom settings (will backup)      │
│   → Will backup and apply SAM AI         │
│                                          │
│ ✓ Claude Desktop (v0.14.10)              │
│   Has MCP servers (will preserve)        │
│   → Will skip                            │
│                                          │
│ ✓ SAM AI Commands (20)                   │
│   Version: 1.0.0                         │
│   → Will backup and upgrade              │
│                                          │
│ [Upgrade SAM AI (Backup & Update)]       │
└─────────────────────────────────────────┘

Action: Backup first, then upgrade
```

### **Mode 3: Partial Installation**
```
Detection:
- Some things installed (e.g., VS Code but no Claude)

User sees:
┌─────────────────────────────────────────┐
│ ℹ Partial Installation Detected         │
│                                          │
│ Missing components will be installed     │
│                                          │
│ Components:                              │
│ ✓ VS Code (v1.85.0) → Will skip          │
│ ✗ Claude Code Extension → Will install   │
│ ✗ Claude Desktop → Will install          │
│ ✗ SAM AI Commands → Will install         │
│ ✗ SAM AI Agents → Will install           │
│                                          │
│ [Complete Installation]                  │
└─────────────────────────────────────────┘

Action: Install only missing components
```

---

## 🛡️ Backup Strategy

Before overwriting ANY existing data, installer creates backups:

```
C:\Users\{user}\.claude\backups\20251031_143022\
├── vscode_settings.json        (if has custom settings)
├── claude_desktop_config.json  (if has MCP servers)
├── commands/                   (if has SAM AI commands)
│   ├── sam.md
│   ├── developer.md
│   └── ... (all 20)
└── agents/                     (if has SAM AI agents)
    ├── sam/
    ├── cto/
    └── ... (all 20)
```

**Timestamp format:** `YYYYMMDD_HHMMSS`

Users can restore from backups if needed.

---

## 📊 Example Scenarios

### **Scenario 1: Anthony's Current PC**
```
Detection:
✓ VS Code installed (custom settings)
✓ Claude Code installed
✓ Claude Desktop installed (has MCP servers)
✓ 20 commands (SAM AI v1.0.0)
✓ 20 agents (SAM AI v1.0.0)

Mode: Upgrade

Actions:
1. Backup VS Code settings
2. Backup Claude config (preserve MCP servers!)
3. Backup commands
4. Backup agents
5. Apply new SAM AI settings (merged with backup)
6. Upgrade commands to latest
7. Upgrade agents to latest
8. Preserve Claude MCP servers
9. Skip launcher (already installed)

Result: ✅ Upgraded safely, no data lost
```

### **Scenario 2: Anthony's Other PC**
```
Detection:
✓ VS Code installed
✓ Claude Desktop installed
✗ Claude Code NOT installed
✗ Commands NOT installed
✗ Agents NOT installed

Mode: Partial

Actions:
1. Skip VS Code (already installed)
2. Install Claude Code extension
3. Skip Claude Desktop (already installed)
4. Install 20 commands
5. Install 20 agents
6. Install launcher

Result: ✅ Completed missing components
```

### **Scenario 3: Anthony's Laptop**
```
Detection:
✓ VS Code installed (different custom settings)
✗ Claude NOT installed
✗ Commands NOT installed
✗ Agents NOT installed

Mode: Partial

Actions:
1. Backup VS Code settings (different from main PC)
2. Apply SAM AI settings (merged)
3. Install Claude Desktop
4. Install Claude Code extension
5. Install 20 commands
6. Install 20 agents
7. Install launcher

Result: ✅ Laptop has SAM AI, custom settings preserved
```

### **Scenario 4: Friend's Clean PC**
```
Detection:
✗ Nothing installed

Mode: Fresh

Actions:
1. Install VS Code with SAM AI settings
2. Install Claude Code extension
3. Install Claude Desktop
4. Install 20 commands
5. Install 20 agents
6. Install launcher

Result: ✅ Complete SAM AI environment from scratch
```

---

## 🔧 How to Use

### **Option 1: Use Smart Installer (Recommended)**
```bash
# Build smart installer
python build.py --smart

# Output: dist/SAM_AI_Setup_Smart.exe
```

### **Option 2: Use Original Installer**
```bash
# Build original installer (no detection)
python build.py

# Output: dist/SAM_AI_Setup.exe
# WARNING: Will overwrite without asking!
```

---

## 🎯 Benefits

✅ **Safe on any PC** - Detects what's there first
✅ **Preserves custom settings** - Backups before overwriting
✅ **Preserves MCP servers** - Doesn't lose Claude Desktop config
✅ **Upgrades intelligently** - Only updates what's needed
✅ **No data loss** - Everything backed up with timestamps
✅ **User choice** - Shows what will happen before doing it

---

## 🚀 Next Steps

1. **Test both versions:**
   - `SAM_AI_Setup.exe` - Original (fast, no detection)
   - `SAM_AI_Setup_Smart.exe` - Smart (safe, detects first)

2. **Recommend Smart version for:**
   - Users with existing installations
   - Anthony's multiple PCs
   - Anyone with custom configs

3. **Recommend Original version for:**
   - Fresh/clean PCs
   - CI/CD automated deployments
   - When you WANT to overwrite everything

---

**Status:** ✅ Smart Detection Complete
**Files:** `environment_detector.py`, `main_smart.py`
**Ready to build:** `python build.py --smart`
