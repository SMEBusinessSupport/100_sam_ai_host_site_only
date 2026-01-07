# Centralized Logging System Documentation

## Overview

The AI Automator module includes a comprehensive, automatic logging system that intercepts all console output and persists it to external files without requiring manual intervention. This system takes users "out of the loop" by automatically capturing, storing, and flushing debug information.

---

## Architecture

### Three-Layer System

1. **Frontend Logger** (`logger.js`) - JavaScript console interception and buffering
2. **Backend Receiver** (`canvas.py`) - Python RPC endpoint for log persistence
3. **File Storage** (`console.log`) - External log file in module root directory

### Data Flow

```
JavaScript Console
    ↓ (intercepted)
Logger System
    ↓ (buffered in memory)
LocalStorage Backup (every 10s)
    ↓ (auto-flush every 5s)
Backend RPC Call
    ↓ (write_debug_log method)
File: console.log
```

---

## Key File Locations

### 1. Frontend Logger
**Path:** `C:\Working With AI\Odoo Projects\custom-modules-v18\the_ai_automator\static\src\n8n\utils\logger.js`

**Lines:** 384 lines

**Purpose:**
- Intercepts console.log, console.error, console.warn
- Buffers logs in memory (max 5000 entries)
- Auto-saves to localStorage every 10 seconds
- Auto-flushes to backend every 5 seconds
- Provides manual download capability

**Key Methods:**
- `interceptConsoleMethods()` - Overrides native console methods
- `addLog(level, args)` - Stores log entry with timestamp, level, message
- `flushToBackend()` - Sends pending logs via RPC to Python backend
- `saveToLocalStorage()` - Persists logs for page refresh recovery
- `download(format='txt')` - Manual download to Downloads folder
- `getStats()` - View log statistics
- `search(keyword)` - Search logs by keyword
- `filterByLevel(level)` - Filter by INFO/WARN/ERROR
- `clear()` - Clear all logs

### 2. Backend Receiver
**Path:** `C:\Working With AI\Odoo Projects\custom-modules-v18\the_ai_automator\models\canvas.py`

**Lines:** 728-783 (56 lines, `write_debug_log` method)

**Purpose:**
- Receives log data from frontend via JSON-RPC
- Formats logs with session ID and timestamps
- Appends to external console.log file
- Silently fails to prevent frontend breakage

**Method Signature:**
```python
@api.model
def write_debug_log(self, log_data):
    """
    Args:
        log_data (dict): {
            'session_id': str,
            'logs': [
                {
                    'timestamp': ISO datetime,
                    'level': 'INFO'|'WARN'|'ERROR',
                    'message': str,
                    'module': str,
                    'sessionId': str
                }
            ],
            'timestamp': ISO datetime
        }
    Returns:
        bool: True if successful, False on error (silent failure)
    """
```

### 3. Log File Output
**Path:** `C:\Working With AI\Odoo Projects\custom-modules-v18\the_ai_automator\console.log`

**Format:**
```
================================================================================
Session: session_1696123456789_abc123def
Flushed at: 2025-10-01T12:34:56.789Z
Log count: 15
================================================================================

[2025-10-01T12:34:55.123Z] [INFO] [Odoo-N8N-Canvas]
📝 Logger System initialized - Direct file writing enabled
--------------------------------------------------------------------------------
[2025-10-01T12:34:55.456Z] [INFO] [Odoo-N8N-Canvas]
🎨 Canvas Manager initialized
--------------------------------------------------------------------------------
...
```

### 4. Manifest Registration
**Path:** `C:\Working With AI\Odoo Projects\custom-modules-v18\the_ai_automator\__manifest__.py`

**Lines:** 104 (in `assets` section)

**Critical:** Logger MUST load as FIRST JavaScript file to intercept all console output

```python
'assets': {
    'web.assets_backend': [
        # JavaScript - Utilities (MUST load first to intercept console)
        'the_ai_automator/static/src/n8n/utils/logger.js',

        # All other JavaScript files load AFTER logger
        'the_ai_automator/static/src/n8n/n8n_data_reader.js',
        'the_ai_automator/static/src/n8n/canvas/canvas_manager.js',
        # ...
    ],
}
```

---

## How It Works

### Console Interception

The logger overrides native console methods to capture all output:

```javascript
const originalLog = console.log;
console.log = function(...args) {
    self.addLog('INFO', args);
    originalLog.apply(console, args); // Still shows in browser console
};
```

### Auto-Flush Mechanism

Every 5 seconds, pending logs are sent to backend:

```javascript
this.autoFlushInterval = setInterval(() => {
    if (this.pendingLogs.length > 0) {
        this.flushToBackend();
    }
}, 5000);
```

### RPC Communication

Logs are sent via Odoo's JSON-RPC protocol:

```javascript
const response = await fetch('/web/dataset/call_kw', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'X-Requested-With': 'XMLHttpRequest'
    },
    credentials: 'same-origin',
    body: JSON.stringify({
        jsonrpc: '2.0',
        method: 'call',
        params: {
            model: 'canvas',
            method: 'write_debug_log',
            args: [{
                session_id: this.sessionId,
                logs: logsToSend,
                timestamp: new Date().toISOString()
            }],
            kwargs: {}
        },
        id: Math.random()
    })
});
```

### File Writing

Backend appends to log file with formatted sections:

```python
module_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
log_file_path = os.path.join(module_path, 'console.log')

with open(log_file_path, 'a', encoding='utf-8') as f:
    f.writelines(log_lines)
```

---

## Usage

### Automatic (No User Action Required)

The system works automatically once initialized:

1. Logger loads on page load
2. All console output is intercepted
3. Logs auto-save to localStorage every 10s
4. Logs auto-flush to backend every 5s
5. Backend writes to `console.log` file

### Manual Commands (Browser Console)

```javascript
// Download logs as TXT file
Logger.download()

// Download logs as JSON
Logger.download('json')

// View statistics
Logger.getStats()

// Search logs
Logger.search('error')
Logger.search('node')

// Filter by level
Logger.filterByLevel('ERROR')
Logger.filterByLevel('WARN')

// Get recent logs (last 5 minutes)
Logger.getRecent(5)

// Clear all logs
Logger.clear()
```

---

## Enhancement Guide

### Adding Module-Specific Loggers

The current logger is **universal** - it captures all console output from all modules. To add module-specific logging:

#### Option 1: Use Existing Logger with Module Tags

**Already supported!** Just call console.log from your module:

```javascript
// In your module file
console.log('🎨 My Module: Doing something');
console.error('❌ My Module: Error occurred');
```

The logger automatically captures these with:
- `module: 'Odoo-N8N-Canvas'` (default)
- `timestamp`
- `level`
- `sessionId`

#### Option 2: Create Named Logger Instances

Extend logger.js to support multiple named instances:

**File:** `logger.js` (lines 12-22)

**Current:**
```javascript
constructor() {
    this.logs = [];
    this.moduleName = 'Odoo-N8N-Canvas';
    this.sessionId = this.generateSessionId();
    // ...
}
```

**Enhanced:**
```javascript
constructor(moduleName = 'Odoo-N8N-Canvas') {
    this.logs = [];
    this.moduleName = moduleName;
    this.sessionId = this.generateSessionId();
    // ...
}

// Create multiple instances
window.Logger = new LoggerSystem('Odoo-N8N-Canvas');
window.NodeLogger = new LoggerSystem('NodeManager');
window.ConnectionLogger = new LoggerSystem('ConnectionSystem');
```

#### Option 3: Add Log Filtering to Backend

Modify `write_debug_log` to write to separate files based on module:

**File:** `canvas.py` (lines 728-783)

**Current:**
```python
log_file_path = os.path.join(module_path, 'console.log')
```

**Enhanced:**
```python
# Extract module name from first log entry
module_name = logs[0].get('module', 'general') if logs else 'general'
sanitized_name = module_name.lower().replace(' ', '_').replace('-', '_')
log_file_path = os.path.join(module_path, f'console_{sanitized_name}.log')
```

This would create:
- `console_odoo_n8n_canvas.log`
- `console_nodemanager.log`
- `console_connectionsystem.log`

### Adding Log Rotation

To prevent infinite file growth, add log rotation to backend:

**File:** `canvas.py` (add before writing)

```python
import os
from datetime import datetime

def rotate_log_if_needed(log_file_path, max_size_mb=10):
    """Rotate log file if it exceeds max size"""
    if os.path.exists(log_file_path):
        size_mb = os.path.getsize(log_file_path) / (1024 * 1024)
        if size_mb > max_size_mb:
            # Rename old log with timestamp
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_path = f"{log_file_path}.{timestamp}.bak"
            os.rename(log_file_path, backup_path)
            _logger.info(f'📦 Rotated log file: {backup_path}')

# Call before writing
rotate_log_if_needed(log_file_path)
with open(log_file_path, 'a', encoding='utf-8') as f:
    f.writelines(log_lines)
```

### Adding Log Levels Configuration

Allow users to configure which log levels to capture:

**File:** `logger.js` (add to constructor)

```javascript
constructor(moduleName = 'Odoo-N8N-Canvas', options = {}) {
    this.moduleName = moduleName;
    this.enabledLevels = options.enabledLevels || ['INFO', 'WARN', 'ERROR'];
    this.minLevel = options.minLevel || 'INFO'; // INFO, WARN, ERROR
    // ...
}

addLog(level, args) {
    // Filter by enabled levels
    if (!this.enabledLevels.includes(level)) {
        return;
    }

    // Filter by minimum level
    const levelPriority = { INFO: 0, WARN: 1, ERROR: 2 };
    if (levelPriority[level] < levelPriority[this.minLevel]) {
        return;
    }

    // Continue with existing addLog logic...
}
```

Usage:
```javascript
// Only capture errors
window.Logger = new LoggerSystem('MyModule', {
    enabledLevels: ['ERROR']
});

// Capture warnings and errors only
window.Logger = new LoggerSystem('MyModule', {
    minLevel: 'WARN'
});
```

### Adding Remote Log Streaming

For real-time debugging, add WebSocket streaming:

**File:** `logger.js` (add method)

```javascript
startRemoteStreaming(websocketUrl) {
    this.ws = new WebSocket(websocketUrl);

    this.ws.onopen = () => {
        console.log('🌐 Remote log streaming enabled');
    };

    // Override addLog to stream in real-time
    const originalAddLog = this.addLog.bind(this);
    this.addLog = (level, args) => {
        originalAddLog(level, args);

        // Stream to remote server
        if (this.ws && this.ws.readyState === WebSocket.OPEN) {
            this.ws.send(JSON.stringify({
                level,
                message: args.join(' '),
                timestamp: new Date().toISOString()
            }));
        }
    };
}
```

---

## Manifest Registration Details

### Why Logger Loads First

**Critical:** Logger MUST be the first JavaScript file loaded to intercept all console output from subsequent modules.

**Manifest location:** `__manifest__.py` line 104

```python
'assets': {
    'web.assets_backend': [
        # CSS/SCSS Styling
        'the_ai_automator/static/src/n8n/canvas/canvas_styles.scss',
        'the_ai_automator/static/src/n8n/n8n_styles/n8n_node_details.css',
        'the_ai_automator/static/src/n8n/n8n_styles/n8n_node_canvas_styles.css',

        # Templates
        'the_ai_automator/static/src/xml/workflow_templates.xml',

        # JavaScript - Utilities (MUST load first to intercept console)
        'the_ai_automator/static/src/n8n/utils/logger.js',  # ← FIRST JS FILE

        # All other JavaScript files
        'the_ai_automator/static/src/n8n/n8n_data_reader.js',
        'the_ai_automator/static/src/n8n/canvas/canvas_manager.js',
        'the_ai_automator/static/src/n8n/nodes/node_style_manager.js',
        'the_ai_automator/static/src/n8n/nodes/node_manager.js',
        'the_ai_automator/static/src/n8n/overlays/overlay_manager.js',
        'the_ai_automator/static/src/n8n/lines/connection_manager.js',
        'the_ai_automator/static/src/n8n/lines/connection_system.js',
    ],
}
```

### Adding New Loggers to Manifest

To add a new logger file:

1. Create logger file in `static/src/n8n/utils/`
2. Add to manifest AFTER main logger but BEFORE other modules
3. Initialize in global scope

**Example:**
```python
'assets': {
    'web.assets_backend': [
        # Utilities
        'the_ai_automator/static/src/n8n/utils/logger.js',
        'the_ai_automator/static/src/n8n/utils/node_logger.js',     # New
        'the_ai_automator/static/src/n8n/utils/connection_logger.js', # New

        # Other modules
        'the_ai_automator/static/src/n8n/canvas/canvas_manager.js',
    ],
}
```

---

## Troubleshooting

### Logs Not Appearing in File

**Check:**
1. Backend method registered: `canvas.py` line 728
2. RPC endpoint accessible: Check browser network tab for `/web/dataset/call_kw` calls
3. File permissions: Ensure Odoo process can write to module directory
4. Python logging: Check Odoo server logs for `[Debug Logger]` messages

**Debug:**
```javascript
// In browser console
Logger.flushToBackend().then(result => console.log('Flush result:', result));
```

### Logs Not Captured

**Check:**
1. Logger loads first: Verify manifest order
2. Console interception active: `console.log('test')` should appear in `Logger.logs`
3. Browser console shows logger initialization: Look for "📝 Logger System initialized"

**Debug:**
```javascript
// Check if logger is intercepting
console.log('Test message');
Logger.logs.length // Should increase
```

### Auto-Flush Not Working

**Check:**
1. Interval running: `Logger.autoFlushInterval` should not be null
2. Network connectivity: Check browser network tab
3. Backend responding: Check Odoo logs for RPC errors

**Debug:**
```javascript
// Manually trigger flush
Logger.flushToBackend();

// Check pending logs
Logger.pendingLogs.length
```

---

## Performance Considerations

### Memory Usage

- **Max 5000 log entries** in memory (configurable via `maxLogs`)
- Oldest entries automatically removed when limit reached
- LocalStorage has ~5-10MB limit per domain

### Network Usage

- Auto-flush every 5 seconds (configurable)
- Only sends if pending logs exist
- Failed flushes retry on next interval

### File Size

- Log file grows indefinitely (add rotation for production)
- Recommendation: Implement log rotation at 10MB

---

## Future Enhancements

### Potential Improvements

1. **Log Rotation** - Automatic file rotation when size limit reached
2. **Multiple Output Targets** - Write to file, database, remote server
3. **Module-Specific Loggers** - Separate log files per module
4. **Log Level Filtering** - Configure which levels to capture
5. **Real-Time Streaming** - WebSocket-based live log viewing
6. **Log Compression** - Gzip old log files
7. **Log Viewer UI** - Odoo view to browse logs in-app
8. **Alert System** - Email/notification on ERROR level logs
9. **Performance Metrics** - Track execution time, memory usage
10. **Stack Traces** - Capture full error stack traces

---

## Summary

The logging system provides automatic, zero-configuration debug logging for the AI Automator module. It intercepts all console output, buffers it in memory and localStorage, and automatically flushes to an external file every 5 seconds. This takes users "out of the loop" and provides persistent debugging information without manual intervention.

**Key Files:**
- Frontend: `static/src/n8n/utils/logger.js`
- Backend: `models/canvas.py` (line 728)
- Output: `console.log` (module root)
- Manifest: `__manifest__.py` (line 104)

**Key Principle:** Logger must load first in manifest to intercept all subsequent console output.

**Ouput file location** C:\Working With AI\Odoo Projects\custom-modules-v18\the_ai_automator\docs\error logging