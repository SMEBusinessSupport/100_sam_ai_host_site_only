# Python Package Installation Strategy

## The Problem

Odoo requires specific Python packages in specific locations. The pain points:

1. **System Python vs Bundled Python** - Conflicts when multiple Python installations exist
2. **Package Location** - Odoo looks for packages in its own Python environment
3. **Version Conflicts** - Different Odoo/Python versions need different package versions
4. **Path Issues** - Windows PATH pollution causes "which Python?" problems

---

## Our Solution: Isolated Python Environment

### Strategy

**Bundle a COMPLETE, ISOLATED Python 3.12 environment with ALL dependencies pre-installed**

```
C:\Program Files\Odoo 18\
└── Python312\                    ← Bundled, isolated Python
    ├── python.exe                ← 3.12.x
    ├── Scripts\
    │   ├── pip.exe
    │   └── [other scripts]
    ├── Lib\
    │   ├── site-packages\        ← ALL Odoo dependencies pre-installed
    │   │   ├── babel\
    │   │   ├── decorator\
    │   │   ├── docutils\
    │   │   ├── freezegun\
    │   │   ├── gevent\
    │   │   ├── greenlet\
    │   │   ├── idna\
    │   │   ├── Jinja2\
    │   │   ├── lxml\
    │   │   ├── num2words\
    │   │   ├── ofxparse\
    │   │   ├── passlib\
    │   │   ├── Pillow\
    │   │   ├── polib\
    │   │   ├── psutil\
    │   │   ├── psycopg2\           ← CRITICAL for PostgreSQL
    │   │   ├── pydot\
    │   │   ├── pyparsing\
    │   │   ├── PyPDF2\
    │   │   ├── pyserial\
    │   │   ├── python-dateutil\
    │   │   ├── pytz\
    │   │   ├── pyusb\
    │   │   ├── qrcode\
    │   │   ├── reportlab\
    │   │   ├── requests\
    │   │   ├── urllib3\
    │   │   ├── vobject\
    │   │   ├── Werkzeug\
    │   │   ├── xlrd\
    │   │   ├── XlsxWriter\
    │   │   ├── xlwt\
    │   │   └── zeep\
    │   └── [standard library]
    └── DLLs\
```

---

## Implementation

### 1. Pre-Build the Python Environment

Before creating the installer, we prepare Python:

```powershell
# Create clean Python 3.12 installation
$PythonSource = "python-3.12.x-embed-amd64.zip"  # Embedded Python
$PythonDest = "C:\Users\total\installer\bundled\python-3.12"

# Extract embedded Python
Expand-Archive $PythonSource -DestinationPath $PythonDest

# Install pip into embedded Python
Invoke-WebRequest https://bootstrap.pypa.io/get-pip.py -OutFile get-pip.py
& "$PythonDest\python.exe" get-pip.py

# Install ALL Odoo dependencies
& "$PythonDest\Scripts\pip.exe" install -r requirements.txt

# Result: Fully populated site-packages directory
```

### 2. Installer Bundles Complete Python

The Inno Setup installer includes:
- Python 3.12 executable
- Complete Lib/site-packages with ALL dependencies
- No post-installation pip installs needed

### 3. Odoo Configuration Points to Bundled Python

**odoo.conf:**
```ini
[options]
# No python_path needed - Odoo uses its bundled Python
```

**Start script:**
```batch
@echo off
REM Use bundled Python explicitly
"C:\Program Files\Odoo 18\Python312\python.exe" ^
    "C:\Program Files\Odoo 18\server\odoo-bin" ^
    -c "C:\Program Files\Odoo 18\config\odoo.conf"
```

---

## Advantages

1. **Zero Conflicts** - Completely isolated from system Python
2. **No PATH Pollution** - Doesn't add to Windows PATH (optional)
3. **Pre-installed Dependencies** - No pip install during setup
4. **Reproducible** - Every installation identical
5. **Portable** - Can copy entire Odoo folder

---

## Requirements.txt (Odoo 18)

```txt
# Core dependencies
Babel==2.9.1
decorator==4.4.2
docutils==0.17
freezegun==1.1.0
gevent==23.9.1 ; sys_platform != 'win32'
gevent==23.9.1 ; sys_platform == 'win32'
greenlet==3.0.1
idna==2.10
Jinja2==3.1.2
lxml==4.9.3 ; sys_platform != 'win32'
lxml==4.9.3 ; sys_platform == 'win32'
MarkupSafe==2.1.3
num2words==0.5.10
ofxparse==0.21
passlib==1.7.4
Pillow==10.0.1
polib==1.1.1
psutil==5.9.5
psycopg2==2.9.7 ; sys_platform != 'win32'
psycopg2==2.9.7 ; sys_platform == 'win32'
pydot==1.4.2
pyparsing==3.0.9
PyPDF2==3.0.1
pyserial==3.5
python-dateutil==2.8.2
python-ldap==3.4.3 ; sys_platform != 'win32'
python-stdnum==1.18
pytz==2023.3
pyusb==1.2.1
qrcode==7.4.2
reportlab==4.0.6
requests==2.31.0
urllib3==2.0.7
vobject==0.9.6.1
Werkzeug==3.0.1
xlrd==2.0.1
XlsxWriter==3.1.2
xlwt==1.3.0
zeep==4.2.1

# Additional Odoo 18 specific
chardet==5.2.0
cryptography==41.0.5
ebaysdk==2.1.5
html2text==2020.1.16
libsass==0.22.0
oauthlib==3.2.2
paramiko==3.3.1
PyNaCl==1.5.0
python-jose==3.3.0
python-magic-bin==0.4.14 ; sys_platform == 'win32'
pyOpenSSL==23.2.0
```

---

## Build Script

```powershell
# build_python_bundle.ps1
# Prepares Python 3.12 with all Odoo dependencies

$PythonVersion = "3.12.0"
$PythonEmbed = "python-$PythonVersion-embed-amd64.zip"
$PythonURL = "https://www.python.org/ftp/python/$PythonVersion/$PythonEmbed"
$BundleDir = "C:\Users\total\installer\bundled\python-3.12"

Write-Host "Building Python bundle..."

# Download embedded Python
if (-not (Test-Path $PythonEmbed)) {
    Write-Host "Downloading Python $PythonVersion..."
    Invoke-WebRequest $PythonURL -OutFile $PythonEmbed
}

# Extract
Write-Host "Extracting Python..."
if (Test-Path $BundleDir) {
    Remove-Item $BundleDir -Recurse -Force
}
Expand-Archive $PythonEmbed -DestinationPath $BundleDir

# Uncomment import site in python312._pth
$PthFile = "$BundleDir\python312._pth"
(Get-Content $PthFile) -replace '#import site', 'import site' | Set-Content $PthFile

# Install pip
Write-Host "Installing pip..."
Invoke-WebRequest https://bootstrap.pypa.io/get-pip.py -OutFile "$BundleDir\get-pip.py"
& "$BundleDir\python.exe" "$BundleDir\get-pip.py"

# Install all Odoo dependencies
Write-Host "Installing Odoo dependencies..."
& "$BundleDir\Scripts\pip.exe" install -r "C:\Users\total\installer\assets\requirements.txt"

# Verify installation
Write-Host "Verifying installation..."
& "$BundleDir\python.exe" -c "import psycopg2; print('psycopg2 OK')"
& "$BundleDir\python.exe" -c "import lxml; print('lxml OK')"
& "$BundleDir\python.exe" -c "import PIL; print('Pillow OK')"

Write-Host "Python bundle ready at: $BundleDir" -ForegroundColor Green
```

---

## Odoo Startup Script

**start_odoo.bat:**
```batch
@echo off
setlocal

REM ============================================================================
REM Start Odoo 18 with Bundled Python
REM ============================================================================

set ODOO_HOME=C:\Program Files\Odoo 18
set PYTHON_EXE=%ODOO_HOME%\Python312\python.exe
set ODOO_BIN=%ODOO_HOME%\server\odoo-bin
set ODOO_CONF=%ODOO_HOME%\config\odoo.conf

REM Set Python to use bundled environment
set PYTHONHOME=%ODOO_HOME%\Python312
set PYTHONPATH=%ODOO_HOME%\Python312\Lib;%ODOO_HOME%\Python312\DLLs

echo Starting Odoo 18...
echo Python: %PYTHON_EXE%
echo Config: %ODOO_CONF%

"%PYTHON_EXE%" "%ODOO_BIN%" -c "%ODOO_CONF%"

pause
```

---

## Testing on Your Dev PC

### Before Uninstalling Current Odoo

1. **Document your current setup:**
```powershell
# Check what Python is being used
where python
python --version

# Check what packages are installed
pip list > current_packages.txt

# Check Odoo config
type "C:\Program Files\Odoo 18\config\odoo.conf"
```

2. **Backup your databases:**
```bash
pg_dump -U odoo_user your_database > backup.sql
```

### Testing Strategy

**Option A: Side-by-Side Install (Safer)**
- Install new Odoo to `C:\Program Files\Odoo 18 New\`
- Use different ports (8070, 5433)
- Test without breaking current setup

**Option B: Clean Install on Secondary PC (Recommended)**
- Use your Windows laptop
- Clean environment
- Real-world test

**Option C: VM Install (Most Thorough)**
- Create Windows 10/11 VM
- Completely clean environment
- Can snapshot and retry

---

## Your Specific Concern: Python Package Locations

### Current Pain Points (What We're Avoiding)

```
❌ System Python: C:\Python312\
   └── Lib\site-packages\
       └── [packages] ← Odoo can't find these

❌ User Python: C:\Users\total\AppData\Local\Programs\Python\
   └── Lib\site-packages\
       └── [packages] ← Odoo can't find these either

❌ Mixed PATH:
   PATH=C:\Python312;C:\Python311;C:\Users\...\Python310
   └── Which python runs? Which packages? CHAOS!
```

### Our Solution (What We're Doing)

```
✓ Bundled Python: C:\Program Files\Odoo 18\Python312\
   └── Lib\site-packages\
       └── [ALL packages] ← Odoo finds everything here

✓ No PATH pollution:
   - Bundled Python NOT added to PATH
   - Scripts use explicit path
   - No conflicts with other Python installations

✓ Explicit execution:
   start_odoo.bat → "C:\Program Files\Odoo 18\Python312\python.exe" odoo-bin
                    └── Uses ONLY bundled packages
```

---

## Verification Commands

After installation, verify Python isolation:

```powershell
# Should show bundled Python
"C:\Program Files\Odoo 18\Python312\python.exe" --version

# Should show all Odoo packages
"C:\Program Files\Odoo 18\Python312\Scripts\pip.exe" list

# Verify psycopg2 (most problematic package)
"C:\Program Files\Odoo 18\Python312\python.exe" -c "import psycopg2; print(psycopg2.__file__)"

# Should output: C:\Program Files\Odoo 18\Python312\Lib\site-packages\psycopg2\...
```

---

## Recommendation for Your Testing

1. **Don't uninstall your dev Odoo yet**
2. **Test on your laptop first** (clean Windows)
3. **If issues arise:**
   - Check which Python is running: `where python`
   - Check package location: `python -c "import sys; print(sys.path)"`
   - Verify bundled Python used: Check process with Process Explorer

4. **Once verified working:**
   - Then consider clean install on dev PC
   - Or keep both (side-by-side with different ports)

---

**Bottom Line:** The installer bundles a COMPLETE, ISOLATED Python 3.12 environment with ALL dependencies pre-installed. Odoo will ONLY use this bundled Python, avoiding all conflicts with system Python installations.