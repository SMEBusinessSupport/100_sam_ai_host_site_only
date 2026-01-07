# Force Odoo to Reload JavaScript/CSS Assets

## The Problem

Odoo caches JavaScript and CSS files in "asset bundles". Even after restarting Odoo, the old cached versions are served to the browser.

Your changes to `sam_ai_chat_widget.js` and `sam_ai_chat_widget.css` exist in the files, but Odoo is still serving the OLD cached version.

## Solution: Force Asset Regeneration

### Method 1: Enable Debug Mode with Assets (FASTEST)

1. **Add `?debug=assets` to your URL:**
   ```
   http://localhost:8069/odoo?debug=assets
   ```

2. **Hard refresh browser:**
   - Windows: `Ctrl + Shift + R`
   - Mac: `Cmd + Shift + R`

3. **Verify in browser:**
   - Open DevTools (F12)
   - Go to Elements tab
   - Search for `sam-model-indicator`
   - Should now appear in the header

### Method 2: Delete Asset Cache & Restart

1. **Stop Odoo:**
   ```bash
   sudo systemctl stop odoo
   # OR
   pkill -f odoo-bin
   ```

2. **Delete asset cache database records:**
   ```bash
   psql -U odoo_user -d your_database_name
   DELETE FROM ir_attachment WHERE name LIKE 'web.assets%';
   \q
   ```

3. **Restart Odoo:**
   ```bash
   sudo systemctl start odoo
   ```

4. **Hard refresh browser:** `Ctrl + Shift + R`

### Method 3: Update Module with Assets Flag

1. **Go to Apps menu in Odoo**

2. **Search for "SAM AI"**

3. **Click "Upgrade"** (this forces asset rebuild)

4. **Hard refresh browser:** `Ctrl + Shift + R`

### Method 4: Command Line Update (MOST RELIABLE)

```bash
# Stop Odoo first
sudo systemctl stop odoo

# Update module with assets cleared
./odoo-bin -d your_database_name -u ai_sam --stop-after-init

# Start Odoo
sudo systemctl start odoo
```

Then hard refresh browser.

## Verify It Worked

After forcing asset reload, you should see this in browser Elements panel:

```html
<div class="sam-chat-header">
    <div class="sam-chat-header-left">
        <i class="fa fa-robot"></i>
        <span class="sam-chat-title">SAM AI Assistant</span>
        <span class="sam-chat-status">
            <i class="fa fa-circle" style="color: #10b981;"></i>
            Online
        </span>
    </div>

    <!-- THIS SHOULD NOW BE VISIBLE -->
    <div class="sam-chat-header-center">
        <div class="sam-model-indicator" id="sam-model-indicator">
            <i class="fa fa-bolt"></i>
            <span class="sam-model-name">Sonnet 4</span>
            <span class="sam-model-provider">Anthropic</span>
        </div>
    </div>

    <div class="sam-chat-header-right">
        <button class="sam-chat-split-btn" title="Split Screen">
            <i class="fa fa-columns"></i>
        </button>
        <!-- ... -->
    </div>
</div>
```

## Visual Result

The model indicator badge should appear **centered in the header** between the title and close buttons:

```
┌─────────────────────────────────────────────────┐
│ 🤖 SAM AI  ●Online   ⚡ Sonnet 4 | ANTHROPIC   │
│                                      🗙  ➖  ✕  │
└─────────────────────────────────────────────────┘
```

## If Still Not Working

If after ALL these methods the badge still doesn't appear:

1. **Check browser console for errors:**
   ```
   F12 → Console tab
   Look for JavaScript errors
   ```

2. **Verify file was actually modified:**
   ```bash
   grep -n "sam-model-indicator" "C:\Working With AI\ai_sam\ai_sam\ai_sam\static\src\js\sam_ai_chat_widget.js"
   ```
   Should return line 281.

3. **Check if Odoo is loading from a different location:**
   ```
   In browser DevTools → Sources tab
   Search for sam_ai_chat_widget.js
   Check which file path it's loading from
   ```

## Current Status

✅ **Code IS in the files:**
- sam_ai_chat_widget.js line 279-286 (model indicator HTML)
- sam_ai_chat_widget.js lines 1029-1092 (update methods)
- sam_ai_chat_widget.css lines 1175-1253 (styling)

❌ **Odoo is serving OLD cached assets**

**You need to force asset regeneration using one of the methods above.**
