# Future-Proof Addon Path Architecture

## The Problem

**Current approach:**
```ini
addons_path = /opt/odoo/addons,
              /opt/odoo/custom-addons/core,
              /opt/odoo/custom-addons/starter,
              /opt/odoo/custom-addons/professional
```

**Issues:**
- Folder names tied to tier names (what if "starter" becomes "basic"?)
- Typos during manual configuration
- Name changes break existing installations
- Hard to maintain consistency across deployments

---

## The Solution: Numeric Path Structure

### Base Installer Structure

```
C:\Odoo-Lightweight\
├── odoo\
│   ├── server\
│   │   └── odoo\
│   │       └── addons\          # Odoo core (always present)
│   └── custom-addons\
│       ├── 01\                  # Reserved: Core lightweight modules (bundled)
│       ├── 02\                  # Reserved: SAM AI Core (free tier)
│       ├── 03\                  # Reserved: Tier 1 addons (€97/month)
│       ├── 04\                  # Reserved: Tier 2 addons (€497/month)
│       ├── 05\                  # Reserved: Tier 3 addons (€1147/month)
│       ├── 06\                  # Reserved: Enterprise custom
│       ├── 07\                  # Reserved: Client-specific
│       ├── 08\                  # Reserved: Future expansion
│       ├── 09\                  # Reserved: Future expansion
│       └── 10\                  # Reserved: Future expansion
```

---

## Mapping System

### Database Table: `saas.addon.path`

```python
class SaasAddonPath(models.Model):
    _name = 'saas.addon.path'
    _description = 'Addon Path Registry'
    _order = 'path_id'

    path_id = fields.Integer(string='Path ID', required=True, readonly=True)
    path_number = fields.Char(string='Path Number', compute='_compute_path_number', store=True)

    # Human-readable info
    display_name = fields.Char(string='Display Name', required=True)
    description = fields.Text(string='Description')

    # Technical info
    repository_url = fields.Char(string='GitHub Repository')
    repository_branch = fields.Char(string='Branch', default='main')
    access_token_env = fields.Char(string='Token Env Var', help='e.g., SAMAI_TIER1_TOKEN')

    # Access control
    tier_ids = fields.Many2many('saas.membership.tier', string='Available to Tiers')
    is_bundled = fields.Boolean(string='Bundled in Installer', default=False)
    is_core = fields.Boolean(string='Core (Always Active)', default=False)

    # Status
    active = fields.Boolean(string='Active', default=True)

    @api.depends('path_id')
    def _compute_path_number(self):
        for record in self:
            record.path_number = str(record.path_id).zfill(2)  # "01", "02", etc.

    def get_full_path(self, base_dir='/opt/odoo/custom-addons'):
        """Returns: /opt/odoo/custom-addons/01"""
        self.ensure_one()
        return f"{base_dir}/{self.path_number}"
```

### Predefined Records (Data File)

```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <data noupdate="1">

        <!-- Path 01: Core Lightweight Modules (Bundled) -->
        <record id="addon_path_01" model="saas.addon.path">
            <field name="path_id">1</field>
            <field name="display_name">Core Lightweight</field>
            <field name="description">Core Odoo lightweight modules (bundled in installer)</field>
            <field name="repository_url">https://github.com/samai/odoo-lightweight.git</field>
            <field name="is_bundled" eval="True"/>
            <field name="is_core" eval="True"/>
        </record>

        <!-- Path 02: SAM AI Core (Free Tier) -->
        <record id="addon_path_02" model="saas.addon.path">
            <field name="path_id">2</field>
            <field name="display_name">SAM AI Core</field>
            <field name="description">SAM AI core modules (ai_sam_intelligence, ai_sam_chat)</field>
            <field name="repository_url">https://github.com/samai/samai-core-modules.git</field>
            <field name="is_core" eval="True"/>
        </record>

        <!-- Path 03: Tier 1 Addons (€97/month) -->
        <record id="addon_path_03" model="saas.addon.path">
            <field name="path_id">3</field>
            <field name="display_name">Starter Add-ons</field>
            <field name="description">Tier 1: Lead Generator, Basic Workflows</field>
            <field name="repository_url">https://github.com/samai/samai-starter-addons.git</field>
            <field name="access_token_env">SAMAI_TIER1_TOKEN</field>
        </record>

        <!-- Path 04: Tier 2 Addons (€497/month) -->
        <record id="addon_path_04" model="saas.addon.path">
            <field name="path_id">4</field>
            <field name="display_name">Professional Add-ons</field>
            <field name="description">Tier 2: Advanced CRM, Analytics, Automation</field>
            <field name="repository_url">https://github.com/samai/samai-professional-addons.git</field>
            <field name="access_token_env">SAMAI_TIER2_TOKEN</field>
        </record>

        <!-- Path 05: Tier 3 Addons (€1147/month) -->
        <record id="addon_path_05" model="saas.addon.path">
            <field name="path_id">5</field>
            <field name="display_name">Enterprise Add-ons</field>
            <field name="description">Tier 3: White-label, API Access, Custom Development</field>
            <field name="repository_url">https://github.com/samai/samai-enterprise-addons.git</field>
            <field name="access_token_env">SAMAI_TIER3_TOKEN</field>
        </record>

        <!-- Path 06-10: Reserved for future use -->
        <record id="addon_path_06" model="saas.addon.path">
            <field name="path_id">6</field>
            <field name="display_name">Reserved: Enterprise Custom</field>
            <field name="description">Reserved for client-specific enterprise customizations</field>
            <field name="active" eval="False"/>
        </record>

        <record id="addon_path_07" model="saas.addon.path">
            <field name="path_id">7</field>
            <field name="display_name">Reserved: Industry Vertical 1</field>
            <field name="description">Reserved for future industry-specific modules</field>
            <field name="active" eval="False"/>
        </record>

        <record id="addon_path_08" model="saas.addon.path">
            <field name="path_id">8</field>
            <field name="display_name">Reserved: Industry Vertical 2</field>
            <field name="description">Reserved for future industry-specific modules</field>
            <field name="active" eval="False"/>
        </record>

        <record id="addon_path_09" model="saas.addon.path">
            <field name="path_id">9</field>
            <field name="display_name">Reserved: Partner Integrations</field>
            <field name="description">Reserved for third-party integration modules</field>
            <field name="active" eval="False"/>
        </record>

        <record id="addon_path_10" model="saas.addon.path">
            <field name="path_id">10</field>
            <field name="display_name">Reserved: Future Expansion</field>
            <field name="description">Reserved for future use</field>
            <field name="active" eval="False"/>
        </record>

    </data>
</odoo>
```

---

## Configuration Generation

### Dynamic odoo.conf Generation

```python
class SaasClient(models.Model):
    _inherit = 'saas.client'

    def _generate_addons_path(self, tier_id):
        """Generate addons_path based on customer tier"""

        # Always include Odoo core
        paths = ['/opt/odoo/addons']

        # Get addon path registry
        AddonPath = self.env['saas.addon.path']

        # Add core paths (always included)
        core_paths = AddonPath.search([('is_core', '=', True), ('active', '=', True)])
        for path in core_paths.sorted('path_id'):
            paths.append(path.get_full_path())

        # Add tier-specific paths
        tier_paths = AddonPath.search([
            ('tier_ids', 'in', tier_id.id),
            ('is_core', '=', False),
            ('active', '=', True)
        ])
        for path in tier_paths.sorted('path_id'):
            paths.append(path.get_full_path())

        return ','.join(paths)

    def _generate_odoo_conf(self):
        """Generate complete odoo.conf for client"""
        addons_path = self._generate_addons_path(self.saas_contract_id.tier_id)

        config = f"""[options]
; Database configuration
db_name = {self.database_name}
db_host = localhost
db_port = 5432
db_user = odoo
db_password = {self.db_password}

; Addon paths (numeric, future-proof)
addons_path = {addons_path}

; Multi-tenancy
dbfilter = ^{self.database_name}$

; Security
admin_passwd = {self.admin_password}
list_db = False

; Performance
workers = 2
max_cron_threads = 1
"""
        return config
```

### Example Generated Config

**For Tier 1 Customer (€97/month):**
```ini
addons_path = /opt/odoo/addons,
              /opt/odoo/custom-addons/01,
              /opt/odoo/custom-addons/02,
              /opt/odoo/custom-addons/03
```

**For Tier 3 Customer (€1147/month):**
```ini
addons_path = /opt/odoo/addons,
              /opt/odoo/custom-addons/01,
              /opt/odoo/custom-addons/02,
              /opt/odoo/custom-addons/03,
              /opt/odoo/custom-addons/04,
              /opt/odoo/custom-addons/05
```

---

## Provisioning Integration

### Clone Repositories to Numeric Paths

```python
def _provision_addons(self, container_path, tier_id):
    """Clone repositories to numeric paths"""

    AddonPath = self.env['saas.addon.path']

    # Get paths to provision (core + tier-specific)
    paths_to_provision = AddonPath.search([
        '|',
        ('is_core', '=', True),
        ('tier_ids', 'in', tier_id.id)
    ]).filtered(lambda p: p.active and not p.is_bundled)

    for addon_path in paths_to_provision.sorted('path_id'):
        target_dir = f"{container_path}/custom-addons/{addon_path.path_number}"

        # Get access token if needed
        token = os.getenv(addon_path.access_token_env) if addon_path.access_token_env else None

        # Build clone URL
        if token:
            clone_url = addon_path.repository_url.replace('https://', f'https://{token}@')
        else:
            clone_url = addon_path.repository_url

        # Clone repository
        _logger.info(f"Cloning {addon_path.display_name} to path {addon_path.path_number}")
        subprocess.run([
            'git', 'clone',
            '--branch', addon_path.repository_branch,
            '--depth', '1',  # Shallow clone for speed
            clone_url,
            target_dir
        ], check=True)
```

---

## Installer Implementation

### Base Installer: Pre-create Folders

```batch
@echo off
REM Create numeric addon path structure

set INSTALL_DIR=%~dp0

echo Creating addon path structure...

REM Create base custom-addons directory
mkdir "%INSTALL_DIR%odoo\custom-addons" 2>nul

REM Create numeric paths 01-10
for /L %%i in (1,1,10) do (
    set "NUM=0%%i"
    set "NUM=!NUM:~-2!"
    mkdir "%INSTALL_DIR%odoo\custom-addons\!NUM!" 2>nul
    echo   Created: custom-addons\!NUM!
)

echo.
echo Addon path structure created successfully!
echo.
```

### odoo.conf Template

```ini
[options]
; Core Odoo addons
addons_path = {INSTALL_DIR}\odoo\server\odoo\addons,
              {INSTALL_DIR}\odoo\custom-addons\01,
              {INSTALL_DIR}\odoo\custom-addons\02

; Database
db_name = samai_production
db_user = odoo
db_password = SamAI2025

; Security
admin_passwd = SamAI

; Note: Paths 03-10 are reserved for future use
; They will be activated when additional modules are installed
```

---

## Benefits

### 1. Future-Proof
- ✅ Path names never change (01, 02, 03, etc.)
- ✅ Rename tiers without breaking configs
- ✅ No typo risk in folder names

### 2. Maintainable
- ✅ Database tracks meaning of each path
- ✅ Easy to understand mapping (Path 03 = Starter tier)
- ✅ Can update repository URLs without changing paths

### 3. Scalable
- ✅ Pre-defined 10 paths (easy to extend to 99 if needed)
- ✅ Reserved paths for future products/verticals
- ✅ Clean separation of concerns

### 4. Version Control
- ✅ Each path can have independent git repo
- ✅ Different branches per path if needed
- ✅ Easy rollback (just re-clone specific path)

### 5. Automation-Friendly
- ✅ Scripts can iterate `01` to `10` easily
- ✅ No string parsing/matching needed
- ✅ Consistent across all environments

---

## Migration Path

### From Current Structure

If you already have:
```
custom-addons/
├── core/
├── starter/
└── professional/
```

**Migration script:**
```bash
#!/bin/bash
mv /opt/odoo/custom-addons/core /opt/odoo/custom-addons/02
mv /opt/odoo/custom-addons/starter /opt/odoo/custom-addons/03
mv /opt/odoo/custom-addons/professional /opt/odoo/custom-addons/04

# Update database registry
echo "UPDATE saas_addon_path SET path_id = 2 WHERE display_name = 'SAM AI Core';"
echo "UPDATE saas_addon_path SET path_id = 3 WHERE display_name = 'Starter Add-ons';"
echo "UPDATE saas_addon_path SET path_id = 4 WHERE display_name = 'Professional Add-ons';"
```

---

## Summary

**Old approach:**
```
/custom-addons/core               ← Name might change
/custom-addons/starter            ← Prone to typos
/custom-addons/professional       ← Hard to script
```

**New approach:**
```
/custom-addons/01                 ← Stable numeric ID
/custom-addons/02                 ← Database maps to "SAM AI Core"
/custom-addons/03                 ← Database maps to "Starter" (€97/mo)
```

**Path-to-Tier mapping lives in database, not filesystem!**

This architecture gives you:
- Stable, typo-proof paths
- Easy automation
- Future extensibility
- Clean separation of identity (01) from meaning (Starter tier)
- Simple installer setup

**Ready to implement this in the installer?**
