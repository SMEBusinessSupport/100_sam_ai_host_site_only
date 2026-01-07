# DEBUG: Idle-In-Transaction Hang Investigation

**Date:** 2025-12-28
**Status:** UNRESOLVED - Server currently hung, needs restart after investigation
**Investigator:** Claude Code (sam_chat specialist)

---

## Executive Summary

The SAM AI Odoo server is hung due to two PostgreSQL connections stuck in `idle in transaction` state. The hang occurred during canvas page load (workflow builder), BEFORE the user attempted to use the chat feature. The root cause appears to be a Python-level blocking issue when two concurrent HTTP requests are processed by Odoo's threaded server mode.

---

## The Problem

**User Experience:**
- User opened AI Builder (workflow canvas) at `/canvas/35/nodes`
- Attempted to chat with SAM AI
- Chat shows "Processing..." indefinitely
- Server is unresponsive to all requests

**Timeline:**
| Time | Event |
|------|-------|
| 07:20:48.804 | Transaction 1 started (canvas query) |
| 07:20:48.805 | Transaction 2 started (res_partner query) |
| 07:20:48.806 | Both queries executed in PostgreSQL |
| 07:20:48.806 | Last Odoo log entry - server hung after this |
| 07:23:12 | User attempted chat (request never processed) |
| 07:36+ | Investigation began |

---

## Current Server State

### PostgreSQL Connections (as of investigation)
```sql
SELECT pid, state, wait_event, xact_start, substring(query,1,80)
FROM pg_stat_activity WHERE state = 'idle in transaction';
```

| PID | State | Wait Event | Transaction Start | Query |
|-----|-------|------------|-------------------|-------|
| 1089816 | idle in transaction | ClientRead | 07:20:48.804381 | SELECT "canvas"."id", "canvas"."name"... |
| 1097512 | idle in transaction | ClientRead | 07:20:48.805458 | SELECT "res_partner"."id", "res_partner"."website_meta_og_img"... |

**Key observation:** Both connections show `wait_event = ClientRead`
- This means PostgreSQL executed the queries successfully
- PostgreSQL sent results back to the client
- PostgreSQL is waiting for Python/psycopg2 to READ the results
- Python never read them - the threads are blocked somewhere

### Odoo Process
- PID: 1094328
- Threads: 45
- Memory: ~545MB
- Running with `workers = 0` (threaded mode via Werkzeug's ThreadedWSGIServer)

### No Database-Level Issues
- No PostgreSQL locks or lock contention
- No long-running queries (both completed instantly)
- Connection pool not exhausted (7 of 64 connections used)

---

## Root Cause Analysis

### What Triggered the Hang

The canvas page (`/canvas/35/nodes`) initialization fires TWO parallel HTTP requests:

**File:** `ai_sam_workflows/views/canvas_page_views.xml` (lines 634, 669)

```javascript
// Request 1: Load canvas state (line 634)
window.nodeManager.loadFromDatabase(WORKFLOW_ID).then(...)

// Request 2: Load menu sidebar (line 669) - fires immediately, doesn't wait
window.workflowMenuSidebar.initialize().then(...)
```

Both use `.then()` (fire-and-forget), meaning they run IN PARALLEL.

### The Request Flow

**Request A: `load_canvas_state(35)`**
- Endpoint: `/web/dataset/call_kw`
- Controller: `canvas.load_canvas_state()`
- Query issued: `SELECT "canvas".*`

**Request B: `get_modules()`**
- Endpoint: `/sam_ai/menu/get_modules`
- Controller: `MenuContextController.get_modules()`
- During authentication, Odoo loads user's partner record
- Query issued: `SELECT "res_partner".*` (includes website fields)

### Why Concurrent Requests Are Problematic

With `workers = 0`, Odoo uses `ThreadedWSGIServer`:
- Each HTTP request gets its own Python thread
- Threads share the same Python process (GIL)
- Threads share the same Odoo registry
- Threads share the same database connection pool

**The blocking occurs at the Python level**, not PostgreSQL:
1. Thread A executes `SELECT "canvas"...` - PostgreSQL returns results
2. Thread B executes `SELECT "res_partner"...` - PostgreSQL returns results
3. Both threads are now stuck BEFORE they can read (fetch) the results
4. Since neither thread progresses, neither transaction commits/closes

### Suspected Blocking Mechanisms

We investigated but couldn't definitively identify:

1. **GIL Contention**: One thread holding GIL during C extension call
2. **Connection Pool Lock**: `ConnectionPool._lock` is a non-reentrant `threading.Lock()`
3. **Registry Lock**: `Registry._lock` is a `threading.RLock()` (reentrant)
4. **ORM-level Lock**: Some internal Odoo synchronization

The `ConnectionPool.borrow()` and `ConnectionPool.give_back()` methods use `@locked` decorator which acquires a non-reentrant lock. If one thread is mid-borrow and another tries to borrow/give_back, contention occurs.

---

## Key Files Investigated

### Odoo Core
- `C:\Program Files\SAM AI\server\odoo\http.py` - Request handling, `_serve_db()`, `_transactioning()`
- `C:\Program Files\SAM AI\server\odoo\sql_db.py` - Cursor, ConnectionPool (line 658: `_lock = threading.Lock()`)
- `C:\Program Files\SAM AI\server\odoo\modules\registry.py` - Registry._lock (line 82: RLock)
- `C:\Program Files\SAM AI\server\odoo\service\security.py` - `check_session()` loads user/partner

### SAM AI Code
- `D:\SAMAI-18-SaaS\github-repos\05-samai-core\ai_sam_workflows\views\canvas_page_views.xml` - Page init (parallel requests)
- `D:\SAMAI-18-SaaS\github-repos\05-samai-core\ai_sam_workflows_base\models\canvas.py` - `load_canvas_state()`
- `D:\SAMAI-18-SaaS\github-repos\05-samai-core\ai_sam_base\controllers\menu_context_controller.py` - `get_modules()`

### Configuration
- `C:\Program Files\SAM AI\server\odoo.conf`:
  - `workers = 0` (threaded mode, NOT multi-process)
  - `db_maxconn = 64`
  - Multi-worker mode problematic on Windows

---

## Proposed Solutions

### Option 1: Sequence Frontend Requests (Recommended)
Modify `canvas_page_views.xml` to await requests sequentially:

```javascript
// BEFORE (parallel):
window.nodeManager.loadFromDatabase(WORKFLOW_ID).then(...)
window.workflowMenuSidebar.initialize().then(...)

// AFTER (sequential):
try {
    await window.nodeManager.loadFromDatabase(WORKFLOW_ID);
    console.log('Canvas loaded');
} catch (e) {
    console.warn('Canvas load failed:', e);
}
try {
    await window.workflowMenuSidebar.initialize();
    console.log('Menu loaded');
} catch (e) {
    console.warn('Menu load failed:', e);
}
```

**Pros:** Safe, simple, works regardless of backend cause
**Cons:** Slightly slower page load (~200-500ms)

### Option 2: Add Database Timeouts
In `odoo.conf`:
```ini
limit_time_cpu = 60
limit_time_real = 120
```

In PostgreSQL:
```sql
ALTER SYSTEM SET statement_timeout = '30s';
ALTER SYSTEM SET idle_in_transaction_session_timeout = '60s';
```

**Pros:** Prevents infinite hangs
**Cons:** Doesn't fix root cause, just limits damage

### Option 3: Investigate Multi-Worker on Windows
Research if `workers = 2` is feasible on Windows with proper configuration.

**Pros:** True parallelism, process isolation
**Cons:** Known issues on Windows, may introduce other problems

### Option 4: Add Request Queuing Middleware
Implement server-side request queuing for specific endpoints.

**Pros:** Backend solution, transparent to frontend
**Cons:** Complex, performance impact

---

## Diagnostic Commands

### Check stuck transactions
```sql
SELECT pid, state, wait_event_type, wait_event,
       now() - xact_start as duration,
       substring(query, 1, 100) as query
FROM pg_stat_activity
WHERE state = 'idle in transaction'
ORDER BY xact_start;
```

### Kill stuck connections (to unblock server)
```sql
SELECT pg_terminate_backend(1097512);
SELECT pg_terminate_backend(1089816);
```

### Check Odoo process
```powershell
wmic process where "processid=1094328" get commandline,threadcount,workingsetsize
netstat -ano | findstr "1094328"
```

### Check connection pool status (in Odoo shell)
```python
from odoo.sql_db import _Pool, _Pool_readonly
print(_Pool)  # Shows: ConnectionPool(read/write;used=X/count=Y/max=64)
print(_Pool_readonly)
```

---

## Questions for Fresh Eyes

1. **Why does `ClientRead` wait event occur?** Both queries completed but Python never read results. What in the Odoo/psycopg2 stack could block between `execute()` and `fetch*()`?

2. **Is there a lock we missed?** We checked ConnectionPool._lock and Registry._lock. Are there other locks in the request path?

3. **Could this be GIL-related?** If a C extension holds GIL, both threads would block. What C extensions are in the critical path?

4. **Why specifically these two requests?** The canvas query and partner query - is there something about their intersection that causes the issue?

5. **Is the issue reproducible?** We haven't restarted the server yet to preserve state. Once restarted, can we reproduce by rapidly loading the canvas page?

---

## Files to Review

Priority order for investigation:

1. `odoo/sql_db.py` - ConnectionPool locking, cursor lifecycle
2. `odoo/http.py` - `_serve_db()`, `_transactioning()`, request threading
3. `odoo/models.py` - ORM query execution, lazy loading
4. `ai_sam_workflows/views/canvas_page_views.xml` - Frontend request triggering
5. `ai_sam_base/controllers/menu_context_controller.py` - `get_modules()` code path

---

## Next Steps

1. **Decision needed:** Fix frontend (sequence requests) vs continue backend investigation
2. **If continuing investigation:** Attach Python debugger or add extensive logging
3. **To unblock server:** Terminate stuck connections (loses debug state)
4. **To test fix:** Implement sequential requests, monitor for recurrence

---

## Contact

This investigation was conducted via `/sam_chat` specialist agent. The user can resume by sharing this document with a new session and asking to continue the investigation or implement a fix.
