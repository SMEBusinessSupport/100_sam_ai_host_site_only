# Intelligent Installer Guide

## Overview

The Odoo 18 with SAM AI installer has been enhanced with intelligent detection and configuration capabilities. The installer automatically detects existing installations, presents user-friendly choices, and configures the system accordingly.

## How It Works

### 1. Smart Detection Wizard

**When:** Runs automatically when the installer starts, before any files are copied.

**What it does:**
- Detects existing Python installations
- Detects existing PostgreSQL installations and databases
- Detects existing Odoo installations
- Checks for port conflicts (8069, 5432)
- Calculates available disk space

**User Experience:**
- Beautiful Windows Forms GUI with clear sections
- Radio button choices for each decision
- Dropdown lists for selecting existing databases
- Visual summary of what will be installed/configured
- Cancellable at any time

### 2. Configuration Choices

The wizard presents users with intelligent choices based on what's detected:

#### PostgreSQL Configuration

**If PostgreSQL is detected:**
- **Option A:** Use existing PostgreSQL installation
  - Installer skips PostgreSQL installation
  - Uses existing PostgreSQL path
  - Can use alternative port if needed
- **Option B:** Install new PostgreSQL
  - Installs bundled PostgreSQL 15
  - Uses alternative port (5433) if 5432 is busy

**If PostgreSQL is NOT detected:**
- Automatically installs bundled PostgreSQL 15
- Uses default port 5432

#### Database Configuration

**If existing databases are found:**
- **Option A:** Use existing database
  - User selects from dropdown of available databases
  - No data initialization needed
  - Preserves all existing data
- **Option B:** Create new database
  - User provides database name
  - Initializes fresh database with base modules

**If no databases are found:**
- Creates new database with user-provided name
- Initializes with base modules

#### Odoo Configuration

**If existing Odoo is detected:**
- **Option A:** Install side-by-side
  - Installs to different directory
  - Uses different ports
  - Both installations can coexist
- **Option B:** Convert existing to lightweight
  - Offers to run conversion wizard
  - Backs up existing installation
  - Removes unused modules
  - Installs placeholders
  - Preserves installed modules and databases

**If no Odoo is detected:**
- Clean installation
- Uses default ports and paths

### 3. Installation Process

After the wizard collects user choices:

1. **Configuration saved:** Wizard saves choices to `install_config.json` in temp directory

2. **Installer proceeds:** Inno Setup reads the configuration and:
   - Skips PostgreSQL installation if using existing
   - Adjusts ports if conflicts detected
   - Configures odoo.conf with correct settings
   - Skips database initialization if using existing

3. **Post-installation:** Scripts configure the system based on choices:
   - `post_install.ps1` - Configures PostgreSQL and Odoo
   - `configure_odoo.ps1` - Initializes database if needed
   - Start/stop scripts with correct paths

### 4. Conversion Mode

If user chooses to convert existing Odoo installation:

**What happens:**
1. **Detection:** Queries PostgreSQL database to find installed modules
2. **Analysis:** Calculates space savings from removing unused modules
3. **Confirmation:** Shows detailed breakdown of what will change
4. **Backup:** Creates complete backup of installation and database
5. **Conversion:**
   - Removes unused module files
   - Installs lightweight-core with placeholders
   - Updates odoo.conf with new addon paths
6. **Summary:** Shows what was changed and preserved
7. **Exit:** Installer exits (conversion is complete, no fresh installation needed)

## Configuration Files

### install_config.json

Created by smart_detection.ps1, consumed by installer:

```json
{
  "UseExistingPostgreSQL": true,
  "PostgreSQLPath": "C:\\Program Files\\PostgreSQL\\15",
  "PostgreSQLPort": 5432,
  "UseExistingDatabase": true,
  "DatabaseName": "my_odoo_db",
  "UseExistingOdoo": true,
  "OdooPath": "C:\\Program Files\\Odoo 18",
  "OdooPort": 8070,
  "OfferConversion": true
}
```

### odoo.conf Template

Uses placeholders replaced during installation:

```ini
db_host = localhost
db_port = __POSTGRESQL_PORT__
db_name = __DATABASE_NAME__
http_port = __ODOO_PORT__
addons_path = __INSTALL_DIR__\server\odoo\addons,__INSTALL_DIR__\addons\lightweight-core,...
```

## User Scenarios

### Scenario 1: Clean Machine

**Detected:**
- No Python
- No PostgreSQL
- No Odoo
- No port conflicts

**Wizard shows:**
- "No existing installations detected"
- "Will install: Python 3.12, PostgreSQL 15, Odoo 18"
- "Default ports: 8069 (Odoo), 5432 (PostgreSQL)"
- Database name input field

**Result:**
- Full installation with all components
- Default configuration
- Fresh database

### Scenario 2: Has PostgreSQL and Database

**Detected:**
- PostgreSQL 15 running on port 5432
- Databases: odoo_prod, odoo_test, postgres

**Wizard shows:**
- PostgreSQL: "Use existing" vs "Install new"
- Database dropdown: [odoo_prod, odoo_test] vs "Create new"

**User chooses:** Use existing PostgreSQL + odoo_prod database

**Result:**
- Skips PostgreSQL installation
- Uses odoo_prod database
- No database initialization
- Existing data preserved

### Scenario 3: Has Odoo Already

**Detected:**
- Odoo 18 at C:\Program Files\Odoo 18
- Using port 8069
- 156 modules installed, 485 not installed

**Wizard shows:**
- "Existing Odoo detected"
- Conversion offer: "Convert to lightweight system?"
  - Will backup everything
  - Remove 485 unused modules
  - Save 340 MB
  - Keep 156 installed modules

**User chooses:** Yes, convert

**Result:**
- Runs convert_to_lightweight.ps1
- Creates backup
- Removes unused files
- Installs placeholders
- Exits installer (done!)

### Scenario 4: Port Conflict

**Detected:**
- Port 8069 in use (existing Odoo running)
- Port 5432 available

**Wizard shows:**
- "Port 8069 is in use"
- "Will use port 8070 for new Odoo"
- "Side-by-side installation"

**Result:**
- Installs to same directory structure
- Uses port 8070
- Both Odoos can run simultaneously

## Testing the Installer

### On Clean Machine (Laptop)

1. Run installer
2. Verify wizard shows "No existing installations"
3. Provide database name
4. Complete installation
5. Verify Odoo starts on port 8069
6. Access http://localhost:8069
7. Create database and login

### On Dev Machine (Existing Odoo)

1. Run installer
2. Verify wizard detects existing Odoo
3. Choose "Convert to lightweight"
4. Review analysis and confirm
5. Wait for backup and conversion
6. Verify conversion summary
7. Start Odoo
8. Verify installed modules still work
9. Check App Store shows placeholders

### On Machine with PostgreSQL

1. Run installer
2. Verify wizard detects PostgreSQL and databases
3. Choose "Use existing PostgreSQL"
4. Select existing database from dropdown
5. Complete installation
6. Verify Odoo connects to existing database
7. Verify data is accessible

## Troubleshooting

### Wizard doesn't appear

**Cause:** PowerShell execution policy or script not extracted

**Solution:**
- Run as Administrator
- Check `%TEMP%` for smart_detection.ps1
- Check Windows Event Viewer for PowerShell errors

### Configuration not applied

**Cause:** install_config.json not created or not found

**Solution:**
- Check `%TEMP%\install_config.json` exists
- Verify JSON is valid
- Re-run installer

### PostgreSQL connection fails

**Cause:** Incorrect credentials or port

**Solution:**
- Check PostgreSQL is running: `Get-Service postgresql*`
- Verify port in odoo.conf matches PostgreSQL
- Check pg_hba.conf allows local connections

### Database not found

**Cause:** Database name mismatch or connection issue

**Solution:**
- Run: `psql -U odoo_user -l` to list databases
- Check database name in odoo.conf
- Verify user permissions

## Advanced Configuration

### Custom Installation Directory

Modify wizard to pass different `-InstallDir`:

```powershell
smart_detection.ps1 -InstallDir "D:\Odoo\18"
```

### Skip Wizard (Silent Install)

For automated deployments, create install_config.json manually:

```powershell
$config = @{
    UseExistingPostgreSQL = $false
    UseExistingDatabase = $false
    DatabaseName = "odoo_auto"
    OdooPort = 8069
    PostgreSQLPort = 5432
}
$config | ConvertTo-Json | Out-File "$env:TEMP\install_config.json"
```

Then run installer with `/SILENT` flag.

### Multi-Instance Setup

For multiple Odoo instances:

1. Install first instance (default ports)
2. Run installer again
3. Wizard detects existing, offers side-by-side
4. Uses alternative ports (8070, 8071, etc.)
5. Each instance has its own configuration

## Benefits

### For Users

- **No technical knowledge required** - Wizard handles complexity
- **Safe** - Always creates backups before changes
- **Flexible** - Choose what to keep, what to install
- **Fast** - Skip unnecessary installations
- **Transparent** - Clear explanations of what will happen

### For Developers

- **Maintainable** - Separation of detection and installation logic
- **Testable** - Each script can be tested independently
- **Extensible** - Easy to add new detection/configuration options
- **Debuggable** - Clear logging and error messages

## Future Enhancements

Potential improvements:

1. **Auto-update detection** - Check for newer Odoo versions
2. **Module migration** - Offer to upgrade installed modules
3. **Configuration import** - Import settings from existing installation
4. **Cloud backup** - Upload backups to cloud storage
5. **Health check** - Verify installation after completion
6. **Rollback** - Automatic rollback on installation failure

---

This intelligent installer transforms the installation experience from a rigid, one-size-fits-all process into a flexible, context-aware system that adapts to each user's unique environment.
