# Enhanced Auto-Login System - Technical Guide

## Overview

The enhanced auto-login system provides a seamless onboarding experience where users:
1. Watch a training video
2. Create their account with a custom password
3. Are automatically logged into Odoo with their new credentials

## Architecture

### Components

1. **`auto_login.py`** - Python HTTP server + Database updater
2. **`welcome_landing.html`** - Frontend form with video
3. **PostgreSQL** - Odoo database (direct access)

### Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│ 1. Installer finishes → auto_login.py starts               │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. Python starts HTTP server on localhost:5000             │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. Python waits for Odoo to start (localhost:8069)         │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. Python opens welcome_landing.html in browser            │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ 5. User watches training video (https://sme.ec/onboarding) │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ 6. After 3 minutes, form reveals automatically             │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ 7. User fills form:                                         │
│    • First Name, Last Name, Email                           │
│    • Password (NEW!) + Confirm Password                     │
│    • Company Name, Phone, Mobile (optional)                 │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ 8. Browser POSTs data to http://localhost:5000/setup       │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ 9. Python receives data, updates PostgreSQL:               │
│    • UPDATE res_users (name, email, password hash)          │
│    • UPDATE res_company (company name)                      │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ 10. Python sends success response with redirect URL        │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ 11. Browser redirects to http://localhost:8069/web/login   │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ 12. User logs in with:                                      │
│     • Username: their.email@example.com                     │
│     • Password: [password they created]                     │
└─────────────────────────────────────────────────────────────┘
```

## New Features

### 1. Password Creation
- Users create their own password during onboarding
- 8 character minimum requirement
- Password confirmation validation
- SHA512 hashing before storage

### 2. Direct Database Access
- Python connects directly to PostgreSQL
- Updates happen server-side (no browser CORS issues)
- More reliable than JavaScript API calls

### 3. HTTP Server
- Runs on `localhost:5000`
- Handles CORS for local file access
- Processes form submissions
- Returns JSON responses

## Database Updates

### Tables Modified

**`res_users` table:**
```sql
UPDATE res_users
SET
    name = 'John Doe',
    login = 'john@example.com',
    email = 'john@example.com',
    password = '[SHA512 hash]',
    phone = '+1 555-123-4567',
    mobile = '+1 555-987-6543',
    write_date = NOW()
WHERE id = 2  -- Admin user
```

**`res_company` table:**
```sql
UPDATE res_company
SET name = 'Acme Corporation'
WHERE id = 1  -- Default company
```

## Security Notes

### Password Handling
1. **Frontend:** Password sent over HTTP (localhost only - safe)
2. **Backend:** Password hashed with SHA512 before database storage
3. **Odoo:** Will rehash with proper PBKDF2 on first login

**Why this works:**
- Odoo detects the password hash format
- On first login, Odoo re-hashes using its own algorithm
- Subsequent logins use Odoo's secure hash

### Database Connection
- Uses `psycopg2` library (Python PostgreSQL adapter)
- Credentials stored in script (could be moved to config file)
- Connection only from localhost

## Dependencies

The enhanced script requires:

```python
# Standard library (included with Python)
import urllib.request
import webbrowser
import time
import sys
import os
import json
import hashlib
import base64
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs

# External library (needs installation)
import psycopg2  # pip install psycopg2-binary
```

### Installing Dependencies

Add to installer setup:
```bash
pip install psycopg2-binary
```

Or bundle `psycopg2` with installer.

## Testing

### Manual Test
1. Run `auto_login.py`
2. Wait for browser to open
3. Watch video (or wait 3 minutes)
4. Fill form with test data:
   - Name: Test User
   - Email: test@example.com
   - Password: password123
5. Submit form
6. Check console for "✓ Setup completed successfully!"
7. Verify redirect to login page
8. Login with test@example.com / password123

### Database Verification

Check if user was updated:
```sql
SELECT id, name, login, email, phone, mobile
FROM res_users
WHERE login != 'admin';
```

Check if company was updated:
```sql
SELECT id, name
FROM res_company
WHERE id = 1;
```

## Future Enhancements

### True Auto-Login (No Manual Entry)

Currently, users must manually enter their new credentials on the login page.

To achieve true auto-login:

1. **Generate Odoo session token** in Python
2. **Set session cookie** in browser
3. **Redirect to dashboard** (not login page)

This requires:
- Calling Odoo's `/web/session/authenticate` endpoint from Python
- Extracting session cookie
- Injecting cookie into browser before redirect

**Code example:**
```python
def create_auto_login_session(email, password):
    """Generate Odoo session and return auto-login URL"""
    import requests

    # Authenticate with Odoo
    response = requests.post('http://localhost:8069/web/session/authenticate', json={
        'jsonrpc': '2.0',
        'params': {
            'db': 'odoo',
            'login': email,
            'password': password
        }
    })

    session_id = response.cookies.get('session_id')

    # Return URL with session token embedded
    return f'http://localhost:8069/web?session_id={session_id}'
```

This is Phase 2 of the enhancement.

## Troubleshooting

### "Connection refused" error
- Check if Odoo is running on port 8069
- Verify `wait_for_odoo()` completed successfully

### "Database connection failed"
- Verify PostgreSQL is running
- Check DB credentials in script
- Ensure `odoo_user` has write permissions

### "Form submission fails"
- Check browser console for errors
- Verify HTTP server started on port 5000
- Check CORS headers in response

### "Password too short" error
- Minimum 8 characters required
- Update HTML `minlength` attribute if needed

## Configuration

### Database Credentials

Edit in `auto_login.py`:
```python
DB_NAME = 'odoo'
DB_USER = 'odoo_user'
DB_PASSWORD = 'odoo_password'
DB_HOST = 'localhost'
DB_PORT = '5432'
```

### HTTP Server Port

Change port 5000 to something else:
```python
# In start_http_server()
server = HTTPServer(('localhost', 5000), SetupHandler)

# And in welcome_landing.html JavaScript:
fetch('http://localhost:5000/setup', {...})
```

### Video Duration Timer

Adjust in `welcome_landing.html`:
```javascript
const estimatedDuration = videoDuration || 180; // 3 minutes default
```

## Summary

This enhanced system provides:
- ✅ Seamless onboarding with video training
- ✅ Custom password creation during setup
- ✅ Direct database updates (no CORS issues)
- ✅ Reliable form submission via HTTP server
- ✅ All user data collected in one step
- ✅ Professional branded experience

**Next step:** Implement true auto-login with session token injection.
