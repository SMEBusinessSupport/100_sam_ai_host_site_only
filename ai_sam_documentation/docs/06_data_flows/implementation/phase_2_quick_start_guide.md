# Phase 2 Quick Start Guide - JavaScript Overlay Conversion

**Last Updated:** 2025-09-30
**Status:** Ready to begin
**Prerequisites:** Phase 1.5 complete ✅

---

## 🎯 What is Phase 2?

Convert the static HTML overlay (Python dev preview) to a fully interactive JavaScript overlay in the canvas view.

**Goal:** Users can click "+ N8N Node" button in canvas → Overlay opens → Click node → Node added to canvas

---

## 📋 Before You Start

### 1. Verify Phase 1.5 Complete
```bash
# Check database has data
# Go to: http://localhost:8069/odoo/action-5687/X (N8N Node Manager)
# Click "Extract Nodes from Filesystem"
# Verify: ActiveCampaign shows Actions: 48, Triggers: 1
```

### 2. Key Files You'll Work With
- **Target File:** `static/src/n8n/overlays/overlay_manager.js` (line ~2338+)
- **Reference:** `models/n8n_simple_extractor.py` → `_generate_new_overlay()` method (lines 504-700)
- **Canvas View:** `static/src/n8n/canvas/canvas_manager.js` (button integration)
- **Test URL:** `http://localhost:8069/canvas/<workflow_id>/nodes`

### 3. Documentation to Review
- `overlay_implementation_status_and_risks.md` - Full status and architecture options
- `n8n_categorization_system_documentation.md` - Data structure reference

---

## 🚀 Step-by-Step Implementation Plan

### Step 1: Add Method Skeleton (15 mins)

**File:** `static/src/n8n/overlays/overlay_manager.js`

**Add after line 2337:**
```javascript
/**
 * Open N8N Node Selector Overlay with real database data
 * Phase 2 implementation - replaces Python dev preview
 */
async openN8nNodeSelector() {
    console.log('🎯 Phase 2: Opening N8N Node Selector');

    try {
        // Step 1: Load data from database
        const nodes = await this.loadN8nNodes();
        console.log(`✅ Loaded ${nodes.length} nodes from database`);

        // Step 2: Generate overlay HTML
        const html = this.generateN8nOverlayHTML(nodes);

        // Step 3: Insert into DOM
        this.showOverlay(html);

        // Step 4: Attach event handlers
        this.attachN8nEventHandlers();

    } catch (error) {
        console.error('❌ Error opening N8N overlay:', error);
        alert('Failed to load N8N nodes. Check console for details.');
    }
}
```

**Test:** Call `window.overlayManager.openN8nNodeSelector()` from browser console

---

### Step 2: Load Data via RPC (30 mins)

**Add this method:**
```javascript
/**
 * Load N8N nodes from database via RPC
 * @returns {Promise<Array>} Array of node objects
 */
async loadN8nNodes() {
    console.log('📡 Fetching N8N nodes from database...');

    const response = await fetch('/web/dataset/call_kw', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            jsonrpc: '2.0',
            method: 'call',
            params: {
                model: 'n8n.simple.node',
                method: 'search_read',
                args: [[]],  // Empty domain = all records
                kwargs: {
                    fields: [
                        'id',
                        'display_name',
                        'supplier',
                        'service',
                        'is_trigger',
                        'operation_count',
                        'resource_count',
                        'categories',
                        'ui_placement_key',
                        'node_id'
                    ],
                    order: 'supplier, display_name'
                }
            }
        })
    });

    const data = await response.json();

    if (data.error) {
        throw new Error(data.error.data.message);
    }

    return data.result || [];
}
```

**Test:**
```javascript
const nodes = await window.overlayManager.loadN8nNodes();
console.log('Nodes:', nodes);
```

---

### Step 3: Generate HTML (1 hour)

**Reference:** Copy HTML structure from `models/n8n_simple_extractor.py` lines 661-700

**Add this method:**
```javascript
/**
 * Generate overlay HTML with node cards
 * @param {Array} nodes - Array of node objects from database
 * @returns {string} HTML string
 */
generateN8nOverlayHTML(nodes) {
    console.log('🎨 Generating overlay HTML...');

    // Group nodes by UI placement
    const nodesByPlacement = this.groupNodesByPlacement(nodes);

    // Calculate supplier counts
    const supplierCounts = this.calculateSupplierCounts(nodes);

    // Generate HTML (convert from Python template)
    const html = `
        <div class="n8n-overlay-backdrop" style="position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: rgba(0,0,0,0.5); z-index: 9999; display: flex; align-items: center; justify-content: center;">
            <div class="n8n-overlay-modal" style="background: white; border-radius: 8px; width: 90%; max-width: 1200px; max-height: 90vh; overflow: hidden; box-shadow: 0 8px 32px rgba(0,0,0,0.3);">

                <!-- Header -->
                <div style="display: flex; justify-content: space-between; align-items: center; padding: 1.5rem; border-bottom: 1px solid #e9ecef;">
                    <h4 style="margin: 0; font-size: 1.25rem; font-weight: 600;">
                        ⚡ N8N Node Selection (<span>${nodes.length}</span> Total Integrations)
                    </h4>
                    <button class="n8n-overlay-close" style="padding: 0.25rem 0.5rem; font-size: 12px; border: 1px solid #6c757d; background: white; color: #6c757d; border-radius: 4px; cursor: pointer;">
                        ✖ Close
                    </button>
                </div>

                <!-- Tabs -->
                <div class="n8n-tabs" style="display: flex; background: #f8f9fa; padding: 0 20px; border-bottom: 1px solid #e9ecef;">
                    <button class="n8n-tab active" data-tab="services" style="background: none; border: none; padding: 12px 16px; cursor: pointer; font-size: 14px; color: #007acc; border-bottom: 3px solid #007acc; font-weight: 600;">
                        🔌 Services
                    </button>
                    <button class="n8n-tab" data-tab="triggers" style="background: none; border: none; padding: 12px 16px; cursor: pointer; font-size: 14px; color: #666; border-bottom: 3px solid transparent;">
                        ⚡ Triggers
                    </button>
                    <button class="n8n-tab" data-tab="actions" style="background: none; border: none; padding: 12px 16px; cursor: pointer; font-size: 14px; color: #666; border-bottom: 3px solid transparent;">
                        🎬 Actions
                    </button>
                    <button class="n8n-tab" data-tab="core" style="background: none; border: none; padding: 12px 16px; cursor: pointer; font-size: 14px; color: #666; border-bottom: 3px solid transparent;">
                        ⚙️ Core
                    </button>
                </div>

                <!-- Content -->
                <div style="padding: 20px; max-height: 70vh; overflow-y: auto;">
                    <div class="n8n-tab-content active" data-tab-content="services">
                        ${this.generateNodeCards(nodesByPlacement.appRegularNodes || [], supplierCounts)}
                    </div>
                    <div class="n8n-tab-content" data-tab-content="triggers" style="display: none;">
                        ${this.generateNodeCards(nodesByPlacement.appTriggerNodes || [], supplierCounts)}
                    </div>
                    <div class="n8n-tab-content" data-tab-content="actions" style="display: none;">
                        ${this.generateNodeCards(nodesByPlacement.appRegularNodes || [], supplierCounts)}
                    </div>
                    <div class="n8n-tab-content" data-tab-content="core" style="display: none;">
                        ${this.generateNodeCards(nodesByPlacement.helpers || [], supplierCounts)}
                    </div>
                </div>

            </div>
        </div>
    `;

    return html;
}

/**
 * Group nodes by UI placement key
 */
groupNodesByPlacement(nodes) {
    const grouped = {};
    nodes.forEach(node => {
        const placement = node.ui_placement_key || 'unknown';
        if (!grouped[placement]) {
            grouped[placement] = [];
        }
        grouped[placement].push(node);
    });
    return grouped;
}

/**
 * Calculate supplier counts (actions/triggers per supplier)
 */
calculateSupplierCounts(nodes) {
    const counts = {};

    nodes.forEach(node => {
        const supplier = node.supplier;
        if (!counts[supplier]) {
            counts[supplier] = { actions: 0, triggers: 0, total: 0 };
        }

        if (node.is_trigger) {
            counts[supplier].triggers += 1;
        } else {
            const count = node.operation_count > 0 ? node.operation_count : 1;
            counts[supplier].actions += count;
        }

        counts[supplier].total = counts[supplier].actions + counts[supplier].triggers;
    });

    return counts;
}

/**
 * Generate node cards HTML
 */
generateNodeCards(nodes, supplierCounts) {
    // Group by supplier to avoid duplicates
    const nodesBySupplier = {};
    nodes.forEach(node => {
        if (!nodesBySupplier[node.supplier]) {
            nodesBySupplier[node.supplier] = [];
        }
        nodesBySupplier[node.supplier].push(node);
    });

    // Generate cards
    return Object.keys(nodesBySupplier).map(supplier => {
        const supplierNodes = nodesBySupplier[supplier];
        const counts = supplierCounts[supplier] || { actions: 0, triggers: 0, total: 0 };

        return `
            <div class="n8n-node-card" data-supplier="${supplier}" style="border: 1px solid #dee2e6; border-radius: 6px; padding: 0.5rem; cursor: pointer; margin-bottom: 0.5rem; background: white;">
                <div style="display: flex; align-items: flex-start; gap: 0.5rem;">
                    <span style="font-size: 1.5rem;">⚙️</span>
                    <div style="flex: 1;">
                        <div style="font-weight: bold; font-size: 0.875rem;">${supplier}</div>
                        <div style="margin-top: 4px;">
                            <span style="background: #007bff; color: white; padding: 1px 4px; border-radius: 3px; font-size: 9px; margin-right: 2px;">
                                Actions: ${counts.actions}
                            </span>
                            <span style="background: #28a745; color: white; padding: 1px 4px; border-radius: 3px; font-size: 9px;">
                                Triggers: ${counts.triggers}
                            </span>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }).join('');
}

/**
 * Show overlay in DOM
 */
showOverlay(html) {
    document.body.insertAdjacentHTML('beforeend', html);
}
```

**Test:** Should see overlay with real data

---

### Step 4: Attach Event Handlers (30 mins)

```javascript
/**
 * Attach event handlers to overlay elements
 */
attachN8nEventHandlers() {
    console.log('🔗 Attaching event handlers...');

    // Close button
    document.querySelector('.n8n-overlay-close')?.addEventListener('click', () => {
        this.closeN8nOverlay();
    });

    // Close on backdrop click
    document.querySelector('.n8n-overlay-backdrop')?.addEventListener('click', (e) => {
        if (e.target.classList.contains('n8n-overlay-backdrop')) {
            this.closeN8nOverlay();
        }
    });

    // ESC key to close
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            this.closeN8nOverlay();
        }
    });

    // Tab switching
    document.querySelectorAll('.n8n-tab').forEach(tab => {
        tab.addEventListener('click', () => {
            const tabName = tab.dataset.tab;
            this.switchN8nTab(tabName);
        });
    });

    // Node card clicks
    document.querySelectorAll('.n8n-node-card').forEach(card => {
        card.addEventListener('click', () => {
            const supplier = card.dataset.supplier;
            this.selectN8nNode(supplier);
        });
    });
}

/**
 * Switch between tabs
 */
switchN8nTab(tabName) {
    console.log(`🔄 Switching to tab: ${tabName}`);

    // Update tab buttons
    document.querySelectorAll('.n8n-tab').forEach(tab => {
        if (tab.dataset.tab === tabName) {
            tab.style.color = '#007acc';
            tab.style.borderBottomColor = '#007acc';
            tab.style.fontWeight = '600';
            tab.classList.add('active');
        } else {
            tab.style.color = '#666';
            tab.style.borderBottomColor = 'transparent';
            tab.style.fontWeight = 'normal';
            tab.classList.remove('active');
        }
    });

    // Update tab content
    document.querySelectorAll('.n8n-tab-content').forEach(content => {
        if (content.dataset.tabContent === tabName) {
            content.style.display = 'block';
            content.classList.add('active');
        } else {
            content.style.display = 'none';
            content.classList.remove('active');
        }
    });
}

/**
 * Handle node selection
 */
selectN8nNode(supplier) {
    console.log(`✅ Node selected: ${supplier}`);

    // TODO: Add node to canvas
    // window.canvasManager.addNodeFromOverlay(nodeData);

    // Close overlay
    this.closeN8nOverlay();
}

/**
 * Close overlay
 */
closeN8nOverlay() {
    console.log('❌ Closing N8N overlay');
    document.querySelector('.n8n-overlay-backdrop')?.remove();
}
```

---

### Step 5: Wire Up Canvas Button (15 mins)

**File:** `static/src/n8n/canvas/canvas_manager.js`

**Find the button handler (search for `showAllNodes2`):**
```javascript
document.getElementById('showAllNodes2')?.addEventListener('click', function() {
    console.log('🎯 N8N Button clicked - Opening overlay');

    if (window.overlayManager) {
        window.overlayManager.openN8nNodeSelector();
    } else {
        console.error('❌ overlayManager not available');
    }
});
```

---

## ✅ Testing Checklist

- [ ] Overlay opens when clicking "+ N8N Node" button
- [ ] All 460+ nodes load from database
- [ ] ActiveCampaign shows correct counts (48 actions, 1 trigger)
- [ ] Tabs switch correctly (Services, Triggers, Actions, Core)
- [ ] Close button works
- [ ] ESC key closes overlay
- [ ] Backdrop click closes overlay
- [ ] Node cards are clickable
- [ ] Console shows no errors

---

## 🐛 Common Issues & Solutions

### Issue: RPC call fails
**Solution:** Check CSRF token, use Odoo's built-in RPC helper if available

### Issue: Overlay doesn't close
**Solution:** Check event listener attachment, use `?.remove()` for safety

### Issue: Tabs don't switch
**Solution:** Verify `data-tab` and `data-tab-content` attributes match

### Issue: Node counts wrong
**Solution:** Verify operation_count field exists in database, check calculation logic

---

## 📚 Key Reference Files

1. **Current HTML Template:** `models/n8n_simple_extractor.py` lines 504-700
2. **Data Structure:** `models/n8n_simple_nodes.py` lines 53-147
3. **Risk Assessment:** `docs/overlay_implementation_status_and_risks.md`
4. **N8N Categorization:** `docs/n8n_categorization_system_documentation.md`

---

## 🎯 Success Criteria

**Phase 2 is complete when:**
1. ✅ Overlay opens from canvas button
2. ✅ Real data loads from database
3. ✅ Tabs work
4. ✅ Close mechanisms work
5. ✅ Node selection triggers (even if just console.log for now)
6. ✅ No JavaScript errors
7. ✅ UX is smooth and responsive

---

## 💡 Pro Tips

1. **Test incrementally** - Don't write everything at once
2. **Use browser console** - `window.overlayManager.openN8nNodeSelector()` for quick testing
3. **Check Network tab** - Verify RPC calls are succeeding
4. **Start simple** - Get basic overlay showing first, add features incrementally
5. **Keep Python version** - Don't delete it until JavaScript version is proven

---

## 🚀 Next Steps After Phase 2

- Phase 3: Canvas integration (add node to canvas on selection)
- Phase 4: Polish (search, favorites, keyboard shortcuts)

---

**Good luck! You've got this. All the hard work (data layer) is done. Phase 2 is just UI plumbing! 🎉**