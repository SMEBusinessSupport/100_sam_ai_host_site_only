# Windows Service Registration for SAM AI Odoo

**Date:** 2025-01-11
**Issue:** SAM AI Odoo is not registered as a Windows service
**Impact:** Users must manually start Odoo, no auto-start on boot

---

## 🔴 Current Problem

### **What's Missing:**
- ❌ No Windows service registration
- ❌ Odoo doesn't start automatically on Windows boot
- ❌ No "Services" management interface
- ❌ Users must manually run `odoo-bin` or batch scripts
- ❌ Odoo stops when user logs out

### **What Users Experience:**
```
Windows boots → Odoo is NOT running
User must: Click Start Menu → SAM AI → Start Odoo
User logs out → Odoo stops
```

---

## ✅ Solution: Register Odoo as Windows Service

### **Goal:**
```
Windows boots → Odoo starts automatically
User can manage via: Services → SAM AI Odoo → Start/Stop/Restart
User logs out → Odoo keeps running
```

---

## 🔧 Implementation Options

### **Option 1: Use Odoo's Built-in Service Installer (RECOMMENDED)**

Odoo includes a `--install-service` command that registers itself as a Windows service.

**Advantages:**
- ✅ Built into Odoo
- ✅ No external dependencies
- ✅ Official Odoo method
- ✅ Easy to implement

**Command:**
```bash
odoo-bin.exe --install-service --config odoo.conf
```

---

### **Option 2: Use NSSM (Non-Sucking Service Manager)**

NSSM is a popular tool for wrapping applications as Windows services.

**Advantages:**
- ✅ More control over service behavior
- ✅ Better logging
- ✅ Restart on failure
- ✅ Dependency management

**Disadvantages:**
- ❌ Requires bundling NSSM.exe
- ❌ Extra ~500 KB in installer
- ❌ More complex setup

---

### **Option 3: Use Windows SC.EXE**

Native Windows service control command.

**Advantages:**
- ✅ Built into Windows
- ✅ No external dependencies

**Disadvantages:**
- ❌ More complex syntax
- ❌ Less user-friendly
- ❌ Harder to configure

---

## 🎯 RECOMMENDED: Option 1 (Odoo Built-in)

---

## 📋 Step-by-Step Implementation

### **Step 1: Create Service Registration Script**

**Create new file:** `D:\SAMAI-18-SaaS\github-repos\100-samai-desktop-installer\scripts\register_service.ps1`

```powershell
# Register SAM AI Odoo as Windows Service
param(
    [string]$InstallDir = "C:\Program Files\SAM AI"
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Registering SAM AI Odoo Windows Service" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$odooBin = Join-Path $InstallDir "server\odoo-bin"
$odooConf = Join-Path $InstallDir "server\odoo.conf"
$pythonExe = Join-Path $InstallDir "python\python.exe"

# Check if files exist
if (-not (Test-Path $pythonExe)) {
    Write-Host "ERROR: Python not found at: $pythonExe" -ForegroundColor Red
    exit 1
}

if (-not (Test-Path $odooBin)) {
    Write-Host "ERROR: odoo-bin not found at: $odooBin" -ForegroundColor Red
    exit 1
}

if (-not (Test-Path $odooConf)) {
    Write-Host "ERROR: odoo.conf not found at: $odooConf" -ForegroundColor Red
    exit 1
}

Write-Host "Python: $pythonExe" -ForegroundColor Gray
Write-Host "Odoo: $odooBin" -ForegroundColor Gray
Write-Host "Config: $odooConf" -ForegroundColor Gray
Write-Host ""

# Stop existing service if running
Write-Host "Checking for existing service..." -ForegroundColor Yellow
$existingService = Get-Service -Name "odoo-server-*" -ErrorAction SilentlyContinue

if ($existingService) {
    Write-Host "Stopping existing service..." -ForegroundColor Yellow
    Stop-Service -Name $existingService.Name -Force -ErrorAction SilentlyContinue
    Write-Host "Removing existing service..." -ForegroundColor Yellow
    & sc.exe delete $existingService.Name
    Start-Sleep -Seconds 2
}

# Register new service using Odoo's built-in method
Write-Host "Registering SAM AI Odoo service..." -ForegroundColor White

try {
    # Change to server directory
    Set-Location (Join-Path $InstallDir "server")

    # Register service
    $registerArgs = @(
        $odooBin,
        "--install-service",
        "--config=$odooConf",
        "--log-level=info"
    )

    & $pythonExe @registerArgs

    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Service registered successfully!" -ForegroundColor Green

        # Get the service name (Odoo creates it as "odoo-server-odoo.conf")
        $serviceName = "odoo-server-odoo"

        # Rename to SAM AI Odoo
        Write-Host "Renaming service to 'SAM AI Odoo'..." -ForegroundColor White

        # Set display name
        & sc.exe config $serviceName DisplayName= "SAM AI Premium Business Suite"
        & sc.exe description $serviceName "SAM AI intelligent business platform powered by Odoo 18"

        # Set to automatic start
        & sc.exe config $serviceName start= auto

        # Set recovery options (restart on failure)
        & sc.exe failure $serviceName reset= 86400 actions= restart/60000/restart/60000/restart/60000

        Write-Host ""
        Write-Host "✓ Service configured!" -ForegroundColor Green
        Write-Host ""
        Write-Host "Service Details:" -ForegroundColor Cyan
        Write-Host "  Name: $serviceName" -ForegroundColor White
        Write-Host "  Display Name: SAM AI Premium Business Suite" -ForegroundColor White
        Write-Host "  Status: Stopped (will start on next boot)" -ForegroundColor White
        Write-Host "  Startup Type: Automatic" -ForegroundColor White
        Write-Host ""
        Write-Host "To start the service now:" -ForegroundColor Yellow
        Write-Host "  net start $serviceName" -ForegroundColor White
        Write-Host "  OR" -ForegroundColor Gray
        Write-Host "  Services → SAM AI Premium Business Suite → Start" -ForegroundColor White

    } else {
        throw "Service registration failed with exit code: $LASTEXITCODE"
    }

} catch {
    Write-Host "✗ Service registration failed: $_" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Service Registration Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
```

---

### **Step 2: Create Service Unregistration Script**

**Create new file:** `D:\SAMAI-18-SaaS\github-repos\100-samai-desktop-installer\scripts\unregister_service.ps1`

```powershell
# Unregister SAM AI Odoo Windows Service
param(
    [string]$InstallDir = "C:\Program Files\SAM AI"
)

Write-Host "===========================================" -ForegroundColor Cyan
Write-Host "Unregistering SAM AI Odoo Windows Service" -ForegroundColor Cyan
Write-Host "===========================================" -ForegroundColor Cyan
Write-Host ""

# Find and stop service
Write-Host "Looking for SAM AI Odoo service..." -ForegroundColor Yellow

$services = Get-Service -Name "odoo-server-*" -ErrorAction SilentlyContinue

if ($services) {
    foreach ($service in $services) {
        Write-Host "Found service: $($service.Name)" -ForegroundColor White

        # Stop service
        if ($service.Status -eq 'Running') {
            Write-Host "Stopping service..." -ForegroundColor Yellow
            Stop-Service -Name $service.Name -Force -ErrorAction SilentlyContinue
            Start-Sleep -Seconds 3
        }

        # Delete service
        Write-Host "Removing service..." -ForegroundColor Yellow
        & sc.exe delete $service.Name

        if ($LASTEXITCODE -eq 0) {
            Write-Host "✓ Service removed successfully!" -ForegroundColor Green
        } else {
            Write-Host "⚠ Service removal may have failed" -ForegroundColor Yellow
        }
    }
} else {
    Write-Host "ℹ No SAM AI Odoo service found" -ForegroundColor Gray
}

Write-Host ""
Write-Host "===========================================" -ForegroundColor Cyan
Write-Host "Service Unregistration Complete!" -ForegroundColor Green
Write-Host "===========================================" -ForegroundColor Cyan
```

---

### **Step 3: Update Installer Script**

**File:** `D:\SAMAI-18-SaaS\github-repos\100-samai-desktop-installer\odoo_samai_installer.iss`

**Add to [Files] section (after line 168):**
```ini
; Service Registration Scripts
Source: "D:\SAMAI-18-SaaS\github-repos\100-samai-desktop-installer\scripts\register_service.ps1"; DestDir: "{app}\scripts"; Flags: ignoreversion
Source: "D:\SAMAI-18-SaaS\github-repos\100-samai-desktop-installer\scripts\unregister_service.ps1"; DestDir: "{app}\scripts"; Flags: ignoreversion
```

**Add to [Run] section (after line 235):**
```ini
; Register Odoo as Windows Service
Filename: "powershell.exe"; Parameters: "-ExecutionPolicy Bypass -File ""{app}\scripts\register_service.ps1"" -InstallDir ""{app}"""; StatusMsg: "Registering SAM AI as Windows service..."; Flags: runhidden waituntilterminated; Check: IsAdminInstallMode
```

**Add to [UninstallRun] section (before line 271):**
```ini
; Unregister Windows Service
Filename: "powershell.exe"; Parameters: "-ExecutionPolicy Bypass -File ""{app}\scripts\unregister_service.ps1"" -InstallDir ""{app}"""; Flags: runhidden waituntilterminated
```

---

## 🎯 What This Does

### **During Installation:**
1. ✅ Copies service registration scripts
2. ✅ Runs `register_service.ps1`
3. ✅ Odoo registers itself as Windows service
4. ✅ Service named "SAM AI Premium Business Suite"
5. ✅ Set to automatic startup
6. ✅ Configured to restart on failure

### **After Installation:**
```
Windows Services:
└── SAM AI Premium Business Suite
    ├── Status: Stopped (or Running if started)
    ├── Startup Type: Automatic
    ├── Service Name: odoo-server-odoo
    └── Path: C:\Program Files\SAM AI\python\python.exe "C:\Program Files\SAM AI\server\odoo-bin"
```

### **During Uninstallation:**
1. ✅ Runs `unregister_service.ps1`
2. ✅ Stops the service
3. ✅ Removes the service registration
4. ✅ Cleans up registry entries

---

## 📊 Service Management

### **Users Can Manage Via:**

**Option 1: Windows Services**
```
Win + R → services.msc → Enter
Find: SAM AI Premium Business Suite
Right-click → Start/Stop/Restart
```

**Option 2: Command Line**
```bash
# Start service
net start odoo-server-odoo

# Stop service
net stop odoo-server-odoo

# Restart service
net stop odoo-server-odoo && net start odoo-server-odoo

# Check status
sc query odoo-server-odoo
```

**Option 3: PowerShell**
```powershell
# Start
Start-Service "odoo-server-odoo"

# Stop
Stop-Service "odoo-server-odoo"

# Restart
Restart-Service "odoo-server-odoo"

# Status
Get-Service "odoo-server-odoo"
```

---

## 🔒 Service Configuration Details

### **Service Properties:**
- **Name:** `odoo-server-odoo`
- **Display Name:** SAM AI Premium Business Suite
- **Description:** SAM AI intelligent business platform powered by Odoo 18
- **Startup Type:** Automatic
- **Log On As:** Local System
- **Recovery:** Restart service on failure (3 attempts)

### **Dependencies:**
The service will automatically depend on:
- ✅ PostgreSQL service (if running as service)
- ✅ Network services

---

## ⚠️ Important Considerations

### **1. PostgreSQL Must Be Running First**
If PostgreSQL is also a service, ensure it starts before Odoo:
```powershell
# Set dependency
sc config odoo-server-odoo depend= postgresql-x64-15
```

### **2. Service Account Permissions**
The service runs as Local System, which:
- ✅ Can access `C:\Program Files\SAM AI\`
- ✅ Can write to logs
- ✅ Can access PostgreSQL

### **3. Firewall Rules**
The service needs port 8069 open:
```powershell
# Add firewall rule during install
New-NetFirewallRule -DisplayName "SAM AI Odoo" -Direction Inbound -Protocol TCP -LocalPort 8069 -Action Allow
```

---

## 🎨 Optional: Add Start Menu Service Controls

**Add to [Icons] section:**
```ini
Name: "{group}\Start SAM AI Service"; Filename: "net.exe"; Parameters: "start odoo-server-odoo"; IconFilename: "{app}\sam\assets\sam_ai.ico"
Name: "{group}\Stop SAM AI Service"; Filename: "net.exe"; Parameters: "stop odoo-server-odoo"; IconFilename: "{app}\sam\assets\sam_ai.ico"
Name: "{group}\Restart SAM AI Service"; Filename: "powershell.exe"; Parameters: "-Command ""Restart-Service odoo-server-odoo"""; IconFilename: "{app}\sam\assets\sam_ai.ico"
Name: "{group}\SAM AI Service Manager"; Filename: "services.msc"; Parameters: "/s"; IconFilename: "{app}\sam\assets\sam_ai.ico"
```

---

## ✅ Benefits After Implementation

### **User Experience:**
- ✅ Odoo starts automatically on Windows boot
- ✅ No manual startup required
- ✅ Works in background (user can log out)
- ✅ Managed via standard Windows Services
- ✅ Automatic restart on crashes
- ✅ Professional installation

### **System Integration:**
- ✅ Standard Windows service behavior
- ✅ Logging to Event Viewer
- ✅ Proper shutdown/restart handling
- ✅ Dependency management
- ✅ Recovery on failure

---

## 📋 Implementation Checklist

- [ ] Create `register_service.ps1`
- [ ] Create `unregister_service.ps1`
- [ ] Add scripts to installer [Files] section
- [ ] Add service registration to [Run] section
- [ ] Add service unregistration to [UninstallRun] section
- [ ] Test installation on clean VM
- [ ] Verify service appears in Services
- [ ] Verify service starts automatically on boot
- [ ] Test uninstallation removes service
- [ ] Test service restart after crash

---

## 🚀 Next Steps

1. **Create the two PowerShell scripts** (`register_service.ps1`, `unregister_service.ps1`)
2. **Update `odoo_samai_installer.iss`** with the new sections
3. **Test on clean Windows VM**
4. **Verify service behavior**

---

**Priority:** HIGH - This is a critical missing feature for production deployments

**Created By:** CTO Analysis via Claude Code
