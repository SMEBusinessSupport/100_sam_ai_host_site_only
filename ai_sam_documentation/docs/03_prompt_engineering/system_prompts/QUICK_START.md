# AI Toolbox - Quick Start Guide

**Get started with SAM AI V3 in 5 minutes!**

---

## 🚀 **Step 1: Start Odoo Server**

```bash
cd "C:\Working With AI\Odoo Projects\custom-modules-v18\ai_automator_docs\ai_toolbox"

# Test startup (verify no errors)
python start_odoo.py --test

# Start server
python start_odoo.py
```

**Or use the batch file on Windows:**
```bash
start_odoo.bat
```

---

## 📦 **Step 2: Install V3 Modules**

**Method A: Using Startup Script (Recommended)**
```bash
# Install ai_base (The Roots)
python start_odoo.py --install ai_base

# Install ai_trunk (The Trunk + SAM AI Core)
python start_odoo.py --install ai_trunk
```

**Method B: Via Web Interface**
1. Access: http://localhost:8069
2. Login with your credentials
3. Go to: Apps → Update Apps List
4. Remove search filter
5. Search: "AI Base" → Install
6. Search: "AI Trunk" → Install

---

## ⚙️ **Step 3: Configure Claude API**

1. Go to: Settings → Technical → SAM AI Configuration
2. Click: Create
3. Fill in:
   - **Provider:** Claude (Anthropic)
   - **API Key:** Your Claude API key from https://console.anthropic.com/
   - **Model:** claude-3-5-sonnet-20241022
   - **Max Tokens:** 8192
4. Click: Save
5. Click: Test Connection (should show success)

---

## ✅ **Step 4: Run QA Check**

Before doing any work, verify everything is clean:

```bash
# Run comprehensive QA
python claude_qa.py

# Should show:
# [OK] No critical errors found.
```

---

## 💻 **Daily Development Workflow**

### **Morning (Start Development):**
```bash
# 1. Start Odoo
python start_odoo.py

# 2. Check status
python odoo_toolbox.py sql --check model --name "ai.conversation"
```

### **During Development:**
```bash
# Interactive debugging
python odoo_toolbox.py interactive

# Check logs if errors occur
python odoo_log_analyzer.py --log "C:\Program Files\Odoo 18\server\odoo.log" --tail 50
```

### **After Changes:**
```bash
# Update module
python start_odoo.py --update ai_trunk

# Or use dev mode (auto-reload)
python start_odoo.py --dev xml
```

### **Before Commit:**
```bash
# RECOMMENDED: Full workflow - QA + Report + Auto-Upgrade
python claude_qa.py --report --upgrade --yes

# OR Interactive (prompts before upgrade):
python claude_qa.py --report --upgrade

# OR Just QA checks:
python claude_qa.py --report

# Review reports in: ai_toolbox/reports/

# Generate documentation
python module_tools.py docs --module ../ai_trunk
```

---

## 🔧 **Common Commands**

### **Server Management:**
```bash
# Normal startup
python start_odoo.py

# Test startup (verify no errors)
python start_odoo.py --test

# Development mode (auto-reload XML/JS)
python start_odoo.py --dev xml

# Open Odoo shell
python start_odoo.py --shell

# Debug logging
python start_odoo.py --log-level debug
```

### **Module Operations:**
```bash
# Install module
python start_odoo.py --install ai_base

# Update module
python start_odoo.py --update ai_trunk

# Update all modules
python start_odoo.py --upgrade all
```

### **Quality Assurance:**
```bash
# QA + Auto-Upgrade (ONE COMMAND!)
python claude_qa.py --upgrade --yes

# QA + Report + Upgrade
python claude_qa.py --report --upgrade

# Just QA checks
python claude_qa.py

# Check specific modules
python claude_qa.py --modules ai_base ai_trunk --upgrade

# Analyze logs
python odoo_log_analyzer.py --log "C:\Program Files\Odoo 18\server\odoo.log"

# Check specific menu
python odoo_toolbox.py sql --check menu --name "SAM AI"

# Generate module docs
python module_tools.py docs --module ../ai_base
```

---

## 🎯 **Troubleshooting**

### **Problem: Server won't start**
```bash
# 1. Check logs
python odoo_log_analyzer.py --log "C:\Program Files\Odoo 18\server\odoo.log" --tail 100

# 2. Test startup
python start_odoo.py --test

# 3. Run QA
python claude_qa.py
```

### **Problem: Menu not showing**
```bash
# Check menu exists
python odoo_toolbox.py sql --check menu --name "Your Menu"

# Interactive debugging
python odoo_toolbox.py interactive
```

### **Problem: Module errors**
```bash
# Validate module
python claude_qa.py

# Check dependencies
python module_tools.py validate --module ../ai_base --other ../ai_trunk
```

### **Problem: Version format error**
```bash
# QA tool will catch this automatically
python claude_qa.py

# Look for:
# [!] Manifest: Version '3.0.0.0' MUST start with '18.0.' for Odoo 18
```

---

## 📚 **Key Files**

| File | Purpose |
|------|---------|
| `start_odoo.py` | Server startup script |
| `claude_qa.py` | Code quality checks |
| `odoo_log_analyzer.py` | Log analysis |
| `odoo_toolbox.py` | Debugging tools |
| `module_tools.py` | Module utilities |
| `VERIFICATION_REPORT.md` | Latest verification status |
| `README.md` | Full toolbox documentation |

---

## 🎓 **Learn More**

- **Full Documentation:** [README.md](README.md)
- **Verification Report:** [VERIFICATION_REPORT.md](VERIFICATION_REPORT.md)
- **Error Resolution:** [ERROR_FIX_REPORT.md](ERROR_FIX_REPORT.md)

---

## ⚡ **Quick Tips**

1. **Always run `--test` first** to verify no errors before full startup
2. **Use `--dev xml`** when working on views (auto-reload)
3. **Run QA before every commit** to catch issues early
4. **Check logs immediately** if you see errors
5. **Use interactive mode** for quick debugging

---

**Ready to build with SAM AI V3!** 🎉
