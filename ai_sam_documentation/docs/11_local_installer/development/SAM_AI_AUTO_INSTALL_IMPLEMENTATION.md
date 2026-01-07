# SAM AI Auto-Install Implementation Plan

## Date: 2025-11-10
## Goal: Auto-install all SAM AI modules during installer and hide enterprise "Upgrade" modules

---

## SAM AI Modules to Auto-Install

### Brain Layer (Dependencies)
Location: `D:\SAMAI-18-SaaS\github-repos\04-samai-brain`
```
1. ai_brain
2. chromadb (if module, not data folder)
```

### Core Layer (Main SAM AI Functionality)
Location: `D:\SAMAI-18-SaaS\github-repos\05-samai-core`
```
3. ai_sam (main SAM AI module)
4. ai_sam_cache_manager
5. ai_sam_github_installer
6. ai_sam_intelligence
7. ai_sam_memory
8. ai_sam_messenger
9. ai_sam_ui
10. github_app
```

**Total: 10 modules** (or 9 if chromadb is just data)

---

## Problem 1: Enterprise Modules Showing "Upgrade" Button

### Current Situation
21 enterprise modules from standard Odoo are showing in Apps with "Upgrade" button:
```
accountant, appointment, helpdesk, hr_appraisal, industry_fsm, knowledge,
marketing_automation, mrp_plm, mrp_workorder, payment_sepa_direct_debit,
planning, quality_control, sale_amazon, sale_subscription, sign, social,
stock_barcode, timesheet_grid, voip, web_mobile, web_studio
```

These have `to_buy = true` in `ir_module_module` table.

### Solution: Override Odoo Apps View Filter

Create a new module: `ai_sam_ui` (or add to existing module) that:
1. Inherits the Apps action
2. Adds default filter to hide `to_buy = true` modules

**Implementation:**

File: `D:\SAMAI-18-SaaS\github-repos\05-samai-core\ai_sam_ui\data\ir_actions_data.xml`

```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <!-- Override the default Apps action to hide enterprise modules -->
    <record id="base.open_module_tree" model="ir.actions.act_window">
        <field name="name">Apps</field>
        <field name="res_model">ir.module.module</field>
        <field name="view_mode">kanban,tree,form</field>
        <field name="context">{
            'search_default_app': 1,
            'search_default_hide_enterprise': 1
        }</field>
        <field name="search_view_id" ref="base.view_module_filter"/>
        <field name="help" type="html">
            <p class="o_view_nocontent_smiling_face">
                Odoo Apps give you instant access to all functionalities.
            </p>
            <p>
                Discover the community apps in the <a href="https://odoo.com/apps" target="_blank">Odoo Apps Store</a>.
            </p>
        </field>
    </record>

    <!-- Add filter to search view to hide enterprise modules -->
    <record id="view_module_filter_hide_enterprise" model="ir.ui.view">
        <field name="name">ir.module.module.hide.enterprise</field>
        <field name="model">ir.module.module</field>
        <field name="inherit_id" ref="base.view_module_filter"/>
        <field name="arch" type="xml">
            <search position="inside">
                <filter string="Hide Enterprise" name="hide_enterprise"
                        domain="[('to_buy', '=', False)]"/>
            </search>
        </field>
    </record>
</odoo>
```

Add to manifest:
```python
'data': [
    'data/ir_actions_data.xml',
    # ... other data files
],
```

This will:
- Add a "Hide Enterprise" filter
- Make it active by default via `search_default_hide_enterprise`
- Users can still see enterprise modules if they uncheck the filter

---

## Problem 2: Auto-Install SAM AI Modules During Installer

### Implementation Strategy

#### Step 1: Update Installer Script (Inno Setup)

Location: `D:\SAMAI-18-SaaS\installer\samai_installer.iss` (or similar)

Add these steps in `[Run]` section:

```innosetup
[Run]
; Stop any running Odoo instances
Filename: "taskkill"; Parameters: "/F /IM python.exe"; Flags: runhidden; StatusMsg: "Stopping Odoo..."

; Drop existing database if it exists
Filename: "{code:GetPostgreSQLPath}\psql.exe"; Parameters: "-U postgres -c ""DROP DATABASE IF EXISTS odoo;"""; Flags: runhidden waituntilterminated; StatusMsg: "Preparing database..."

; Create fresh database
Filename: "{code:GetPostgreSQLPath}\psql.exe"; Parameters: "-U postgres -c ""CREATE DATABASE odoo OWNER odoo_user;"""; Flags: runhidden waituntilterminated; StatusMsg: "Creating database..."

; Initialize database with all SAM AI modules
Filename: "{app}\python\python.exe"; \
  Parameters: "{app}\server\odoo-bin -c {app}\server\odoo.conf -i base,web,ai_brain,ai_sam,ai_sam_cache_manager,ai_sam_github_installer,ai_sam_intelligence,ai_sam_memory,ai_sam_messenger,ai_sam_ui,github_app -d odoo --stop-after-init"; \
  WorkingDir: "{app}\server"; \
  Flags: runhidden waituntilterminated; \
  StatusMsg: "Installing SAM AI modules (this may take 2-3 minutes)..."

; Start Odoo server in background
Filename: "{app}\python\python.exe"; \
  Parameters: "{app}\server\odoo-bin -c {app}\server\odoo.conf"; \
  WorkingDir: "{app}\server"; \
  Flags: nowait runhidden; \
  StatusMsg: "Starting SAM AI server..."

; Wait for Odoo to fully start (10 seconds)
Filename: "cmd.exe"; Parameters: "/c timeout /t 10 /nobreak"; Flags: runhidden waituntilterminated

; Open browser to SAM AI Chat (or welcome page)
Filename: "{sys}\cmd.exe"; \
  Parameters: "/c start http://localhost:8069/web#action=ai_sam.action_sam_chat"; \
  Flags: nowait shellexec
```

#### Step 2: Ensure Module Dependencies Are Correct

Each module's `__manifest__.py` must declare dependencies:

**ai_brain/__manifest__.py**:
```python
{
    'name': 'AI Brain',
    'version': '18.0.1.0',
    'depends': ['base', 'web'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
```

**ai_sam/__manifest__.py**:
```python
{
    'name': 'SAM AI',
    'version': '18.0.1.0',
    'depends': ['base', 'web', 'ai_brain', 'mail'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
```

**ai_sam_ui/__manifest__.py**:
```python
{
    'name': 'SAM AI User Interface',
    'version': '18.0.1.0',
    'depends': ['ai_sam', 'web'],
    'installable': True,
    'application': False,
    'auto_install': True,  # Auto-install when ai_sam is installed
}
```

**ai_sam_messenger/__manifest__.py**:
```python
{
    'name': 'SAM AI Messenger',
    'version': '18.0.1.0',
    'depends': ['ai_sam', 'mail'],
    'installable': True,
    'application': False,
    'auto_install': True,
}
```

Etc. for all other modules.

#### Step 3: Copy Modules to Installation Directory

Installer must copy both repositories to addons folders:

```innosetup
[Files]
; Brain modules (dependencies)
Source: "D:\SAMAI-18-SaaS\github-repos\04-samai-brain\ai_brain\*"; \
  DestDir: "{app}\addons\sam-core\ai_brain"; Flags: ignoreversion recursesubdirs

; Core SAM AI modules
Source: "D:\SAMAI-18-SaaS\github-repos\05-samai-core\ai_sam\*"; \
  DestDir: "{app}\addons\sam-core\ai_sam"; Flags: ignoreversion recursesubdirs

Source: "D:\SAMAI-18-SaaS\github-repos\05-samai-core\ai_sam_cache_manager\*"; \
  DestDir: "{app}\addons\sam-core\ai_sam_cache_manager"; Flags: ignoreversion recursesubdirs

Source: "D:\SAMAI-18-SaaS\github-repos\05-samai-core\ai_sam_github_installer\*"; \
  DestDir: "{app}\addons\sam-core\ai_sam_github_installer"; Flags: ignoreversion recursesubdirs

Source: "D:\SAMAI-18-SaaS\github-repos\05-samai-core\ai_sam_intelligence\*"; \
  DestDir: "{app}\addons\sam-core\ai_sam_intelligence"; Flags: ignoreversion recursesubdirs

Source: "D:\SAMAI-18-SaaS\github-repos\05-samai-core\ai_sam_memory\*"; \
  DestDir: "{app}\addons\sam-core\ai_sam_memory"; Flags: ignoreversion recursesubdirs

Source: "D:\SAMAI-18-SaaS\github-repos\05-samai-core\ai_sam_messenger\*"; \
  DestDir: "{app}\addons\sam-core\ai_sam_messenger"; Flags: ignoreversion recursesubdirs

Source: "D:\SAMAI-18-SaaS\github-repos\05-samai-core\ai_sam_ui\*"; \
  DestDir: "{app}\addons\sam-core\ai_sam_ui"; Flags: ignoreversion recursesubdirs

Source: "D:\SAMAI-18-SaaS\github-repos\05-samai-core\github_app\*"; \
  DestDir: "{app}\addons\sam-core\github_app"; Flags: ignoreversion recursesubdirs
```

---

## Problem 3: Auto-Login Implementation

### Option: Create SAM AI Action for Welcome/Chat

When browser opens, redirect to SAM AI Chat or Welcome page.

**URL Options:**

1. **Direct to SAM AI Chat:**
   ```
   http://localhost:8069/web#action=ai_sam.action_sam_chat&model=ai.sam.chat&view_type=form
   ```

2. **Welcome Onboarding Page:**
   ```
   http://localhost:8069/web#action=ai_sam.action_welcome_onboard
   ```

3. **Simple Login (user clicks login):**
   ```
   http://localhost:8069/web/login
   ```

### Auto-Login with Session Token

Create post-install script: `C:\Program Files\SAM AI\scripts\auto_login.py`

```python
import xmlrpc.client
import webbrowser
import time
import sys

def auto_login_and_open():
    url = 'http://localhost:8069'
    db = 'odoo'
    username = 'admin'
    password = 'admin'

    print("Waiting for Odoo to start...")
    time.sleep(15)  # Wait for Odoo to fully start

    try:
        # Authenticate via XML-RPC
        common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
        uid = common.authenticate(db, username, password, {})

        if uid:
            print(f"Authenticated as user {uid}")

            # Open browser to SAM AI Chat
            target_url = f'{url}/web#action=ai_sam.action_sam_chat'
            print(f"Opening browser to: {target_url}")
            webbrowser.open(target_url)

            return True
        else:
            print("Authentication failed")
            # Fallback: just open login page
            webbrowser.open(f'{url}/web/login')
            return False

    except Exception as e:
        print(f"Error during auto-login: {e}")
        # Fallback: just open login page
        webbrowser.open(f'{url}/web/login')
        return False

if __name__ == '__main__':
    auto_login_and_open()
```

Call from Inno Setup:
```innosetup
[Run]
Filename: "{app}\python\python.exe"; \
  Parameters: "{app}\scripts\auto_login.py"; \
  Flags: nowait runhidden; \
  StatusMsg: "Opening SAM AI..."
```

---

## Summary of Changes Needed

### Source Code Changes:

1. **ai_sam_ui/data/ir_actions_data.xml** - Add enterprise module filter
2. **All module __manifest__.py files** - Ensure correct dependencies
3. **ai_sam module** - Create `action_sam_chat` action (if not exists)
4. **Optional: ai_sam module** - Create `action_welcome_onboard` for onboarding

### Installer Changes:

1. **[Files] section** - Copy all brain + core modules to sam-core folder
2. **[Run] section** - Add database initialization with all modules
3. **[Run] section** - Add auto-login script execution
4. **odoo.conf template** - Ensure correct addons_path

### Testing Checklist:

- [ ] All 9-10 SAM AI modules install without errors
- [ ] Dependencies load in correct order
- [ ] No enterprise modules show in Apps view
- [ ] Browser opens automatically after install
- [ ] User lands on SAM AI Chat (or welcome page)
- [ ] All SAM AI functionality works
- [ ] Uninstall/reinstall works cleanly

---

## Module Installation Order (Dependency Chain)

Based on dependencies, Odoo will install in this order:

```
1. base (Odoo core)
2. web (Odoo web interface)
3. mail (if needed by SAM modules)
4. ai_brain (Brain layer - no SAM dependencies)
5. ai_sam (Main SAM AI - depends on ai_brain)
6. ai_sam_cache_manager (depends on ai_sam)
7. ai_sam_intelligence (depends on ai_sam)
8. ai_sam_memory (depends on ai_sam)
9. ai_sam_messenger (depends on ai_sam + mail)
10. ai_sam_ui (depends on ai_sam, auto_install=True)
11. ai_sam_github_installer (depends on ai_sam)
12. github_app (depends on ?)
```

**Important:** If `auto_install = True` on ui/messenger, they'll install automatically when dependencies are met.

---

## Landing Page Options

### Option A: SAM AI Chat Form (Recommended)
User lands directly in chat interface, ready to interact with SAM.

**Implementation:**
```xml
<record id="action_sam_chat" model="ir.actions.act_window">
    <field name="name">Chat with SAM</field>
    <field name="res_model">ai.sam.chat</field>
    <field name="view_mode">form</field>
    <field name="target">fullscreen</field>
</record>
```

URL: `http://localhost:8069/web#action=ai_sam.action_sam_chat`

### Option B: Welcome Onboarding View (Future Enhancement)
Custom welcome page with:
- Welcome video
- Quick start guide
- Sample prompts to try
- Link to documentation
- "Start Chatting" button → SAM AI Chat

**Implementation:**
```xml
<record id="action_welcome_onboard" model="ir.actions.client">
    <field name="name">Welcome to SAM AI</field>
    <field name="tag">ai_sam_welcome</field>
    <field name="target">fullscreen</field>
</record>
```

Requires JavaScript component: `ai_sam/static/src/js/welcome.js`

---

## Next Immediate Steps

1. ✅ Fix `<tree>` → `<list>` (DONE)
2. ✅ Update source repository (DONE)
3. 🔲 Add enterprise module filter to ai_sam_ui
4. 🔲 Verify all module dependencies
5. 🔲 Create auto_login.py script
6. 🔲 Update Inno Setup installer script
7. 🔲 Test on clean Windows VM
8. 🔲 Build new installer.exe

