# SAM AI Page Builder - Installation Guide

## Quick Start

### Step 1: Restart Odoo

```bash
cd /Users/app/05-samai-core
docker-compose restart odoo
```

Wait 10-15 seconds for Odoo to fully restart.

### Step 2: Access Odoo

Open your browser and go to: **http://localhost:8069**

Login with:
- **Email**: `admin@samai.com`
- **Password**: `admin123`

### Step 3: Update Apps List

1. Click the **Apps** menu (grid icon in top-left)
2. Click the **⋮** (three dots) menu in the top-right
3. Select **Update Apps List**
4. Click **Update** in the confirmation dialog

### Step 4: Install SAM AI Page Builder

1. In the Apps page, use the search box
2. Type: **SAM AI Page Builder**
3. Click the **Install** button on the module card

The module will install along with its dependencies (`base`, `web`, `website`).

### Step 5: Access the Page Builder

After installation:
1. You'll see a new top-level menu: **SAM AI Page Builder**
2. Click it, then click **AI Pages**
3. Click **Create** to make your first AI page
4. Click **Open Builder** to launch the editor interface

## Verification

### Check Module is Installed

1. Go to **Apps** menu
2. Remove the "Apps" filter (click the ✕ on the filter chip)
3. Search for "SAM AI Page Builder"
4. You should see it marked as **Installed**

### Check Menu Appears

Look for **SAM AI Page Builder** in the top menu bar (between other top-level menus).

### Check Logs (Optional)

```bash
docker-compose logs -f odoo | grep sam_ai_page_builder
```

You should see no errors related to the module.

## Troubleshooting

### Module Not Showing in Apps List

**Problem**: Can't find "SAM AI Page Builder" in the Apps page.

**Solution**:
1. Make sure you clicked **Update Apps List**
2. Remove all search filters
3. Try searching for just "SAM" or "Page Builder"
4. Check that the module files exist:
   ```bash
   ls -la sam_ai_page_builder/
   ```

### Installation Fails

**Problem**: Error during installation.

**Solution**:
1. Check Odoo logs:
   ```bash
   docker-compose logs -f odoo
   ```
2. Look for Python errors or missing dependencies
3. Verify the `website` module is installed (it's a dependency)
4. Try restarting Odoo and installing again

### Menu Not Appearing

**Problem**: Module installed but menu doesn't show.

**Solution**:
1. Refresh the browser page (Ctrl+F5 / Cmd+Shift+R)
2. Clear browser cache
3. Log out and log back in
4. Check that you have the right permissions (admin user should see it)

### Builder Interface Not Loading

**Problem**: Clicking "Open Builder" shows blank page or error.

**Solution**:
1. Open browser Developer Tools (F12)
2. Check Console tab for JavaScript errors
3. Check Network tab for failed asset loads
4. Verify all static files exist:
   ```bash
   ls -la sam_ai_page_builder/static/src/
   ```
5. Try clearing Odoo's asset cache:
   - Go to Settings → Technical → Assets
   - Delete all assets
   - Refresh the page

### AI Not Generating Content

**Problem**: Chat panel doesn't respond to prompts.

**Solution**:
1. This is expected - the module uses a **stub AI service**
2. The stub has a 1.5 second delay to simulate network calls
3. Check browser console for errors
4. Verify the prompt was sent (should see loading animation)

## Post-Installation

### Recommended: Install Dependencies

If not already installed, install these modules:
- **Website** (required dependency)
- **Website Mail** (optional, for future features)

### Optional: Configure Access Rights

By default, all internal users can create and edit AI pages.

To restrict access:
1. Go to **Settings** → **Users & Companies** → **Groups**
2. Create a custom group (e.g., "AI Page Builder Users")
3. Edit `security/ir.model.access.csv` to reference your group
4. Upgrade the module

### Optional: Customize Theme

Edit `static/src/css/page_builder.css` to change colors, fonts, or layout.

After editing CSS:
1. Refresh the browser with cache clear (Ctrl+F5)
2. Or restart Odoo to regenerate assets

## Uninstallation

To remove the module:

1. Go to **Apps** menu
2. Remove the "Apps" filter
3. Search for "SAM AI Page Builder"
4. Click **Uninstall**

**Note**: This will delete all AI pages and their data. Export any important pages first.

## Next Steps

After installation, check out:
- [README.md](README.md) - Full feature documentation
- [USAGE.md](USAGE.md) - Detailed usage guide
- Try creating your first AI page!

---

**Need Help?** Contact the SAM AI development team.
