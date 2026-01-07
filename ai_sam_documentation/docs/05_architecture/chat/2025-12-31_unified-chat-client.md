# Developer Prompt: Unified SamChatClient Implementation

**Created**: 2025-12-31
**Author**: CTO Architect Session
**Status**: READY FOR IMPLEMENTATION
**Priority**: HIGH (Architectural Debt)

---

## Context (Why)

The SAM AI chat system has **4 separate entry points** that each instantiate `SamChatVanilla` differently, making debugging painful and maintenance a nightmare:

1. **Fullscreen Chat Page** (`sam_chat_vanilla_v2_action.js`) - OWL wrapper
2. **Bubble/Widget Overlay** (`sam_ai_chat_widget.js`) - Service + overlay
3. **Canvas Node Chat** (`node_manager.js:1472`) - Direct instantiation
4. **Widget Fallback** (`node_manager.js:962`) - Different class entirely

The `sendMessage()` function is buried in a 9000-line file (`sam_chat_vanilla_v2.js` line 1398) with no way to test the transport layer independently.

---

## Phase 0: Cleanup Preparation (Comment Before Delete)

**CRITICAL DISCIPLINE**: Before removing ANY redundant code, follow this two-stage approach:

### Stage 1: Comment Out + Mark
```javascript
// DEPRECATED - Phase X: To be removed after verification
// Replaced by: [new class/method name] in [file path]
// Date: YYYY-MM-DD
/*
    [original code block]
*/
```

### Stage 2: Verify Nothing Breaks
- Test all 4 entry points: fullscreen, overlay, canvas, widget
- Check console for errors
- Verify functionality still works
- Wait at least one development cycle before final removal

### Stage 3: Final Removal (Later Pass)
Only after verification passes:
- Remove commented code blocks
- Remove any orphaned imports
- Update line references in documentation

### Why This Matters
1. **Rollback Safety**: If new code breaks, uncomment old code immediately
2. **Discovery Path**: Future developers can trace where code went
3. **Gradual Confidence**: Build trust in new architecture before burning bridges
4. **Git History**: Single commit shows what was deprecated vs what replaced it

### Deprecation Log Template

Create a section in each file being cleaned up:

```javascript
/**
 * DEPRECATION LOG - sam_chat_vanilla_v2.js
 * =========================================
 *
 * 2025-12-31 | Phase 4.1
 *   - updateActivity() → ChatInteraction.show()
 *   - _displayActivity() → ChatInteraction._show()
 *   - _getDefaultActivityStates() → ChatInteraction.ACTIVITY_STATES
 *
 * 2025-12-31 | Phase 3.2
 *   - showContextShiftDialog() → SamModal
 *   - showTrainingModal() → SamModal
 *   - showKnowledgeReviewModal() → SamModal
 */
```

---

## Goal (What)

Create a **unified transport layer** (`SamChatClient`) that all chat entry points use, separating transport from UI:

```
┌─────────────────────────────────────────────┐
│  SamChatClient (Transport Layer - ~200 LOC) │
│  • send(message) → Starts SSE stream        │
│  • onActivity / onToken / onDone callbacks  │
│  • Context handling standardized            │
└─────────────────────────────────────────────┘
                    │
    ┌───────────────┼───────────────┐
    ▼               ▼               ▼
┌─────────┐   ┌─────────┐   ┌─────────┐
│Fullscreen│   │ Overlay │   │ Canvas  │
│   UI    │   │   UI    │   │   UI    │
└─────────┘   └─────────┘   └─────────┘
```

---

## Approach (How)

### Phase 1: Create SamChatClient

**Create file**: `ai_sam/static/src/js/chat/sam_chat_client.js`

```javascript
/**
 * SamChatClient - Unified Transport Layer for SAM AI Chat
 *
 * SINGLE RESPONSIBILITY: Handle SSE communication with backend.
 * NO UI CODE. NO DOM MANIPULATION. JUST TRANSPORT.
 */
class SamChatClient {

    constructor(options = {}) {
        this.endpoint = options.endpoint || '/sam_ai/chat/send_streaming';
        this.context = options.context || {};
        this.conversationId = null;

        // State
        this.isProcessing = false;
        this.abortController = null;

        // Callbacks
        this.onActivity = options.onActivity || (() => {});
        this.onToken = options.onToken || (() => {});
        this.onDone = options.onDone || (() => {});
        this.onError = options.onError || ((e) => console.error('SamChatClient error:', e));
        this.onPermissionRequired = options.onPermissionRequired || (() => {});
    }

    setContext(contextData) {
        this.context = { ...this.context, ...contextData };
    }

    setConversationId(id) {
        this.conversationId = id;
    }

    async send(message, attachments = []) {
        if (this.isProcessing) {
            throw new Error('Already processing a message');
        }

        this.isProcessing = true;
        this.abortController = new AbortController();

        try {
            const payload = {
                jsonrpc: '2.0',
                method: 'call',
                params: {
                    message,
                    conversation_id: this.conversationId || '',
                    context_data: this.context,
                    attachments: attachments.length > 0 ? attachments : undefined,
                },
                id: Math.floor(Math.random() * 1000000),
            };

            console.log('[SamChatClient] Sending:', message.substring(0, 50));

            const response = await fetch(this.endpoint, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                credentials: 'include',
                body: JSON.stringify(payload),
                signal: this.abortController.signal,
            });

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }

            return await this._processStream(response);

        } catch (error) {
            if (error.name === 'AbortError') {
                return { aborted: true };
            }
            this.onError(error);
            throw error;
        } finally {
            this.isProcessing = false;
            this.abortController = null;
        }
    }

    async _processStream(response) {
        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let buffer = '';
        let fullResponse = '';
        let result = {};

        while (true) {
            const { done, value } = await reader.read();
            if (done) break;

            buffer += decoder.decode(value, { stream: true });
            const lines = buffer.split('\n');
            buffer = lines.pop() || '';

            for (const line of lines) {
                if (line.startsWith('data: ')) {
                    try {
                        const data = JSON.parse(line.substring(6));

                        // Activity event
                        if (data.activity || data.state) {
                            this.onActivity(data.state || data.activity, data.params || {});
                        }

                        // Token event
                        if (data.text || data.chunk) {
                            const text = data.text || data.chunk;
                            fullResponse += text;
                            this.onToken(text);
                        }

                        // Permission required
                        if (data.permission_required || data.needs_permission) {
                            this.onPermissionRequired(data.permission_request || data);
                        }

                        // Conversation ID
                        if (data.conversation_id) {
                            this.conversationId = data.conversation_id;
                        }

                        // Final result
                        if (data.success !== undefined) {
                            result = data;
                        }

                        // Error
                        if (data.error) {
                            this.onError(new Error(data.error));
                        }

                    } catch (e) {
                        // Ignore parse errors for incomplete chunks
                    }
                }
            }
        }

        const finalResult = {
            ...result,
            response: fullResponse,
            conversation_id: this.conversationId,
        };
        this.onDone(finalResult);
        return finalResult;
    }

    abort() {
        if (this.abortController) {
            this.abortController.abort();
        }
    }

    destroy() {
        this.abort();
        this.onActivity = null;
        this.onToken = null;
        this.onDone = null;
        this.onError = null;
        this.onPermissionRequired = null;
    }
}

// Export for both module and global use
export { SamChatClient };
if (typeof window !== 'undefined') {
    window.SamChatClient = SamChatClient;
}
```

---

### Phase 2: Integrate with Fullscreen Chat

**Modify file**: `ai_sam/static/src/js/sam_chat_vanilla_v2.js`

1. Add import at top:
```javascript
// Import unified chat client
import { SamChatClient } from '@ai_sam/js/chat/sam_chat_client';
```

2. Create client in constructor (around line 188):
```javascript
constructor(container, options = {}) {
    // ... existing code ...

    // Create unified chat client
    this.chatClient = new SamChatClient({
        context: options.context || {},
        onActivity: (state, params) => this._handleActivity(state, params),
        onToken: (text) => this._handleToken(text),
        onDone: (result) => this._handleDone(result),
        onError: (error) => this._handleError(error),
        onPermissionRequired: (data) => this._handlePermissionRequired(data),
    });
}
```

3. Refactor `sendMessage()` (around line 1398) to use client:
```javascript
async sendMessage() {
    const text = this.state.inputText?.trim();
    if (!text || this.chatClient.isProcessing) return;

    // Clear input
    this.state.inputText = '';

    // Add user message to UI
    this._addMessage('user', text);

    // Start assistant message placeholder
    this._startAssistantMessage();

    // Update context before sending
    this.chatClient.setContext(this._buildContextData());
    this.chatClient.setConversationId(this.state.activeConversationId);

    // Send via unified client
    try {
        await this.chatClient.send(text, this.state.attachments || []);
    } catch (error) {
        // Error already handled by onError callback
    }
}
```

4. Add handler methods:
```javascript
_handleActivity(state, params) {
    // Use existing ChatInteraction display
    if (this.activityDisplay) {
        this.activityDisplay.show(state, params);
    }
}

_handleToken(text) {
    // Append to current assistant message
    this._appendToCurrentMessage(text);
}

_handleDone(result) {
    // Finalize response
    this._finalizeAssistantMessage(result.response);

    // Update conversation ID if new
    if (result.conversation_id && !this.state.activeConversationId) {
        this.state.activeConversationId = result.conversation_id;
    }

    // Clear activity
    if (this.activityDisplay) {
        this.activityDisplay.clear();
    }
}

_handleError(error) {
    console.error('[SAM Chat] Error:', error);
    this._showError(error.message);
}

_handlePermissionRequired(data) {
    // Render permission popup
    this.renderFilePermissionPopup(data);
}
```

---

### Phase 3: Update Manifest

**Modify file**: `ai_sam/__manifest__.py`

Add new file to assets:
```python
'assets': {
    'web.assets_backend': [
        # ... existing files ...
        'ai_sam/static/src/js/chat/sam_chat_client.js',  # ADD THIS
    ],
},
```

---

## Implementation Details

### Files Affected

| File | Action |
|------|--------|
| `ai_sam/static/src/js/chat/sam_chat_client.js` | CREATE (new file) |
| `ai_sam/static/src/js/sam_chat_vanilla_v2.js` | MODIFY (use client) |
| `ai_sam/__manifest__.py` | MODIFY (add asset) |

### Files NOT Changed (Phase 2+)

| File | Why |
|------|-----|
| `sam_ai_chat_widget.js` | Phase 3 work |
| `node_manager.js` | Phase 4 work |
| Backend controllers | No changes needed |

---

## Validation Checklist

- [ ] `SamChatClient` class created and exported
- [ ] Class handles SSE parsing correctly
- [ ] onActivity called for activity events
- [ ] onToken called for each streaming chunk
- [ ] onDone called with complete response
- [ ] onError called on failures
- [ ] abort() stops current request
- [ ] Fullscreen chat works as before
- [ ] No visual changes to existing UI
- [ ] Console shows "[SamChatClient]" log prefix for transport events

---

## Success Criteria

1. **Single Transport Layer**: All SSE handling in `SamChatClient`
2. **No Breaking Changes**: Existing chat UI works exactly as before
3. **Testable**: Can create `SamChatClient` instance and test independently
4. **Debuggable**: Clear log messages show client state

---

## Testing

```javascript
// Manual test in browser console:
const client = new SamChatClient({
    onActivity: (s, p) => console.log('Activity:', s, p),
    onToken: (t) => console.log('Token:', t),
    onDone: (r) => console.log('Done:', r),
});

await client.send('Hello SAM');
```

Expected output:
```
[SamChatClient] Sending: Hello SAM
Activity: thinking {}
Token: Hi
Token:  there
Token: !
Done: {response: "Hi there!", success: true, ...}
```

---

## Notes for Developer

1. **Don't refactor UI code** - Only extract transport logic
2. **Keep existing sendMessage()** - Just delegate to client internally
3. **Preserve all callbacks** - Activity display, message rendering, etc.
4. **Test incrementally** - Ensure chat works after each change
5. **Use console.log prefix** - `[SamChatClient]` for all client logs

---

## Phase 3: Overlay & Menu Consolidation

**Priority**: MEDIUM (Technical Debt - Do after Phase 1-2 working)

### Problem Analysis

The `sam_chat_vanilla_v2.js` file:
1. **Ignores the existing `sam-overlay` framework** - Creates 5 modals with raw `document.createElement()`
2. **Has 3 different menu systems** across files - Each renders menus differently
3. **Mode handling is broken** - `popup`/`sidebar` modes not recognized (bug!)
4. **Duplicate RPC calls** - Both chat files call `/sam_ai/menu/get_modules`

### Existing Overlay Framework (NOT USED by chat)

```css
/* sam_ui_theme/static/src/css/sam_overlay_base.css */
.sam-overlay { /* Full-screen backdrop with blur */ }
.sam-overlay__panel { /* 90% width/height, 16px radius */ }
.sam-overlay__panel--light { /* White background variant */ }
.sam-overlay__panel--dark { /* Dark background variant */ }
```

```javascript
/* ai_sam_system_overlay/static/src/js/system_overlay.js */
window.SamSystemOverlay.show(message, title);
window.SamSystemOverlay.hide();
window.SamSystemOverlay.setProgress(percent);
```

### Current Mess: 5 Modals Reinventing the Wheel

| Method | Lines | Custom CSS | Should Use |
|--------|-------|------------|------------|
| `showContextShiftDialog()` | 2057-2138 | 60 lines inline | `sam-overlay` |
| `showTrainingModal()` | 3067-3159 | 50 lines inline | `sam-overlay` |
| `showKnowledgeReviewModal()` | 3267-3358 | 60 lines inline | `sam-overlay` |
| `showVoiceAPINotConfiguredDialog()` | 4894-4988 | 40 lines inline | `sam-overlay` |
| `renderFilePermissionPopup()` | 4676-4730 | 30 lines inline | `sam-overlay` |

**Total duplicate CSS**: ~240 lines that could be 0 lines

### Current Mess: 3 Menu Systems

| File | System | Classes Used |
|------|--------|--------------|
| `sam_chat_vanilla_v2.js` | Icon sidebar | `.sidebar-icon`, `.sidebar-menu-icon` |
| `sam_ai_chat_widget.js` | List menu | `.menu-item` |
| `node_manager.js` | Context menu | `.node-context-menu-item` |

### Mode Handling Bug

```javascript
// node_manager.js line 1473 - Passes 'popup' or 'sidebar'
new window.SamChatVanilla(content, {
    mode: mode === 'floating' ? 'popup' : 'sidebar',
});

// sam_chat_vanilla_v2.js line 379 - Doesn't recognize these modes!
this.hideSidebar = this.mode === 'overlay' || this.mode === 'embedded';
// BUG: 'popup' and 'sidebar' fall through → hideSidebar = false
```

---

### Phase 3.1: Fix Mode Handling

**File**: `sam_chat_vanilla_v2.js`

```javascript
// BEFORE (broken):
this.hideSidebar = this.mode === 'overlay' || this.mode === 'embedded';

// AFTER (fixed):
const MODES_WITHOUT_SIDEBAR = ['overlay', 'embedded', 'popup', 'sidebar', 'floating'];
this.hideSidebar = MODES_WITHOUT_SIDEBAR.includes(this.mode);
```

**Effort**: 5 minutes | **Impact**: Fixes canvas chat showing sidebar incorrectly

---

### Phase 3.2: Migrate Modals to sam-overlay Framework

**Goal**: Replace 5 raw modal implementations with consistent `sam-overlay` classes.

**Create helper**: `ai_sam/static/src/js/ui/sam_modal.js`

```javascript
/**
 * SamModal - Unified modal system using sam-overlay framework
 *
 * Usage:
 *   const modal = new SamModal({
 *       title: 'Permission Required',
 *       content: '<p>Allow access to files?</p>',
 *       variant: 'light',  // 'light', 'dark', 'dark-gradient'
 *       buttons: [
 *           { label: 'Allow', action: () => allow(), primary: true },
 *           { label: 'Deny', action: () => deny() },
 *       ],
 *   });
 *   modal.show();
 */
class SamModal {
    constructor(options = {}) {
        this.title = options.title || '';
        this.content = options.content || '';
        this.variant = options.variant || 'light';
        this.buttons = options.buttons || [];
        this.onClose = options.onClose || (() => {});
        this.element = null;
    }

    show() {
        this.element = document.createElement('div');
        this.element.className = 'sam-overlay';
        this.element.innerHTML = `
            <div class="sam-overlay__panel sam-overlay__panel--${this.variant}">
                <div class="sam-modal__header">
                    <h3 class="sam-overlay__title">${this.title}</h3>
                    <button class="sam-modal__close" data-action="close">&times;</button>
                </div>
                <div class="sam-modal__content">
                    ${this.content}
                </div>
                <div class="sam-modal__footer">
                    ${this._renderButtons()}
                </div>
            </div>
        `;

        document.body.appendChild(this.element);
        this._attachEvents();

        // Trigger animation
        requestAnimationFrame(() => {
            this.element.classList.add('active');
        });
    }

    hide() {
        if (this.element) {
            this.element.classList.remove('active');
            setTimeout(() => {
                this.element.remove();
                this.element = null;
            }, 300);  // Match CSS transition
        }
        this.onClose();
    }

    _renderButtons() {
        return this.buttons.map((btn, i) => `
            <button class="sam-modal__btn ${btn.primary ? 'sam-modal__btn--primary' : ''}"
                    data-action="button" data-index="${i}">
                ${btn.label}
            </button>
        `).join('');
    }

    _attachEvents() {
        this.element.addEventListener('click', (e) => {
            const action = e.target.dataset.action;
            if (action === 'close') {
                this.hide();
            } else if (action === 'button') {
                const index = parseInt(e.target.dataset.index);
                if (this.buttons[index]?.action) {
                    this.buttons[index].action();
                }
                this.hide();
            }
        });

        // Close on backdrop click
        this.element.addEventListener('click', (e) => {
            if (e.target === this.element) {
                this.hide();
            }
        });

        // Close on Escape
        this._escHandler = (e) => {
            if (e.key === 'Escape') this.hide();
        };
        document.addEventListener('keydown', this._escHandler);
    }
}

export { SamModal };
if (typeof window !== 'undefined') {
    window.SamModal = SamModal;
}
```

**Then refactor each modal**:

```javascript
// BEFORE: showContextShiftDialog() - 80 lines of inline HTML/CSS
showContextShiftDialog(shiftData) {
    const dialogHTML = `
        <div class="context-shift-dialog-overlay">
            <style>/* 60 lines of CSS */</style>
            <div class="context-shift-dialog">...</div>
        </div>
    `;
    // ... 40 more lines
}

// AFTER: Using SamModal - 15 lines
showContextShiftDialog(shiftData) {
    const modal = new SamModal({
        title: 'Context Change Detected',
        content: `
            <p>You're now in <strong>${shiftData.newDomain}</strong>.</p>
            <p>Would you like to start a new conversation or continue here?</p>
        `,
        variant: 'light',
        buttons: [
            { label: 'New Session', action: () => this.createNewConversation(), primary: true },
            { label: 'Continue Here', action: () => {} },
        ],
    });
    modal.show();
}
```

**Effort**: 2-3 hours | **Impact**: ~300 lines removed, consistent UX

---

### Phase 3.3: Create Shared SamMenuManager

**Goal**: Unify the 3 menu systems into one reusable class.

**Create**: `ai_sam/static/src/js/ui/sam_menu_manager.js`

```javascript
/**
 * SamMenuManager - Unified menu system
 *
 * Supports:
 * - Icon sidebar (fullscreen chat)
 * - List menu (overlay chat)
 * - Context menu (right-click)
 */
class SamMenuManager {
    constructor(options = {}) {
        this.mode = options.mode || 'icons';  // 'icons', 'list', 'context'
        this.position = options.position || 'left';
        this.container = options.container || null;
        this.items = [];
        this._cache = null;
    }

    /**
     * Load Odoo menu modules (cached)
     */
    async loadModules() {
        if (this._cache) return this._cache;

        try {
            const response = await fetch('/sam_ai/menu/get_modules', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                credentials: 'include',
                body: JSON.stringify({ jsonrpc: '2.0', method: 'call', params: {}, id: 1 }),
            });
            const data = await response.json();
            this._cache = data.result || [];
            return this._cache;
        } catch (error) {
            console.error('[SamMenuManager] Failed to load modules:', error);
            return [];
        }
    }

    /**
     * Render menu in container
     */
    render() {
        if (!this.container) return;

        const html = this.mode === 'icons'
            ? this._renderIconSidebar()
            : this.mode === 'list'
            ? this._renderListMenu()
            : this._renderContextMenu();

        this.container.innerHTML = html;
        this._attachEvents();
    }

    _renderIconSidebar() {
        return `
            <div class="sam-menu sam-menu--icons">
                ${this.items.map(item => `
                    <div class="sam-menu__icon ${item.active ? 'active' : ''}"
                         data-menu-id="${item.id}"
                         title="${item.name}">
                        ${item.icon ? `<i class="${item.icon}"></i>` : ''}
                        ${item.image ? `<img src="${item.image}" alt="${item.name}"/>` : ''}
                    </div>
                `).join('')}
            </div>
        `;
    }

    _renderListMenu() {
        return `
            <div class="sam-menu sam-menu--list">
                ${this.items.map(item => `
                    <div class="sam-menu__item ${item.active ? 'active' : ''}"
                         data-menu-id="${item.id}">
                        <i class="${item.icon || 'fa fa-circle'}"></i>
                        <span>${item.name}</span>
                    </div>
                `).join('')}
            </div>
        `;
    }

    _renderContextMenu() {
        return `
            <div class="sam-menu sam-menu--context">
                ${this.items.map(item =>
                    item.separator
                        ? '<div class="sam-menu__separator"></div>'
                        : `<div class="sam-menu__item ${item.danger ? 'danger' : ''}"
                                data-action="${item.action}">
                               <i class="${item.icon}"></i>
                               <span>${item.label}</span>
                           </div>`
                ).join('')}
            </div>
        `;
    }

    _attachEvents() {
        this.container?.addEventListener('click', (e) => {
            const item = e.target.closest('[data-menu-id], [data-action]');
            if (item) {
                const menuId = item.dataset.menuId;
                const action = item.dataset.action;
                this.onSelect?.(menuId || action, item);
            }
        });
    }

    setItems(items) {
        this.items = items;
    }

    setActiveItem(id) {
        this.items = this.items.map(item => ({
            ...item,
            active: item.id === id,
        }));
    }
}

export { SamMenuManager };
if (typeof window !== 'undefined') {
    window.SamMenuManager = SamMenuManager;
}
```

**Effort**: 2-3 hours | **Impact**: ~200 lines removed, consistent menus

---

### Phase 3.4: Add sam-menu CSS to sam_overlay_base.css

**File**: `sam_ui_theme/static/src/css/sam_overlay_base.css`

```css
/* ============================================================================
   SAM MENU SYSTEM - Shared menu styles
   ============================================================================ */

/* Base menu container */
.sam-menu {
    display: flex;
    gap: 4px;
}

/* Icon sidebar variant */
.sam-menu--icons {
    flex-direction: column;
    padding: 8px;
    background: var(--sam-sidebar-bg, #f8f9fa);
    border-right: 1px solid var(--sam-border, #e9ecef);
}

.sam-menu__icon {
    width: 40px;
    height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 8px;
    cursor: pointer;
    transition: background 0.2s, transform 0.2s;
}

.sam-menu__icon:hover {
    background: var(--sam-hover-bg, #e9ecef);
    transform: scale(1.05);
}

.sam-menu__icon.active {
    background: var(--sam-active-bg, #714B67);
    color: white;
}

.sam-menu__icon img {
    width: 24px;
    height: 24px;
    object-fit: contain;
}

/* List menu variant */
.sam-menu--list {
    flex-direction: column;
    padding: 8px 0;
}

.sam-menu__item {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 10px 16px;
    cursor: pointer;
    transition: background 0.2s;
}

.sam-menu__item:hover {
    background: var(--sam-hover-bg, #f1f3f4);
}

.sam-menu__item.active {
    background: var(--sam-active-bg, #e8f0fe);
    color: var(--sam-primary, #1a73e8);
}

.sam-menu__item.danger {
    color: var(--sam-danger, #dc3545);
}

/* Context menu variant */
.sam-menu--context {
    flex-direction: column;
    position: absolute;
    background: white;
    border-radius: 8px;
    box-shadow: 0 4px 16px rgba(0,0,0,0.15);
    min-width: 160px;
    padding: 4px 0;
    z-index: 10000;
}

.sam-menu__separator {
    height: 1px;
    background: var(--sam-border, #e9ecef);
    margin: 4px 0;
}

/* Modal additions */
.sam-modal__header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 16px 20px;
    border-bottom: 1px solid var(--sam-border, #e9ecef);
}

.sam-modal__close {
    background: none;
    border: none;
    font-size: 24px;
    cursor: pointer;
    color: #666;
    padding: 4px;
    border-radius: 4px;
}

.sam-modal__close:hover {
    background: #f5f5f5;
}

.sam-modal__content {
    padding: 20px;
    flex: 1;
    overflow-y: auto;
}

.sam-modal__footer {
    display: flex;
    justify-content: flex-end;
    gap: 12px;
    padding: 16px 20px;
    border-top: 1px solid var(--sam-border, #e9ecef);
}

.sam-modal__btn {
    padding: 8px 16px;
    border-radius: 6px;
    border: 1px solid var(--sam-border, #d1d5db);
    background: white;
    cursor: pointer;
    font-size: 14px;
    transition: background 0.2s;
}

.sam-modal__btn:hover {
    background: #f5f5f5;
}

.sam-modal__btn--primary {
    background: var(--sam-primary, #714B67);
    color: white;
    border-color: var(--sam-primary, #714B67);
}

.sam-modal__btn--primary:hover {
    background: var(--sam-primary-dark, #5a3d52);
}
```

**Effort**: 1 hour | **Impact**: Consistent styling everywhere

---

### Phase 3 Summary

| Task | File | Effort | Lines Saved |
|------|------|--------|-------------|
| 3.1 Fix mode handling | `sam_chat_vanilla_v2.js` | 5 min | 0 (bug fix) |
| 3.2 Create SamModal | `sam_modal.js` (new) | 1 hour | - |
| 3.2 Migrate 5 modals | `sam_chat_vanilla_v2.js` | 2 hours | ~300 |
| 3.3 Create SamMenuManager | `sam_menu_manager.js` (new) | 2 hours | - |
| 3.3 Migrate menu code | Multiple files | 2 hours | ~200 |
| 3.4 Add menu CSS | `sam_overlay_base.css` | 1 hour | 0 (new shared) |

**Total Effort**: ~8 hours
**Total Lines Saved**: ~500+ (plus consistent UX)

---

### Phase 3 Validation Checklist

- [ ] Mode handling recognizes `popup`, `sidebar`, `floating`
- [ ] Canvas chat no longer shows sidebar incorrectly
- [ ] All modals use `SamModal` class
- [ ] Modals have consistent 90% sizing, 16px radius
- [ ] Modals use `sam-overlay__panel--light` or `--dark`
- [ ] All menus use `SamMenuManager` class
- [ ] Menu styles consistent across all entry points
- [ ] `/sam_ai/menu/get_modules` called once and cached
- [ ] No inline `<style>` blocks in modal HTML

---

## Phase 4: Message Rendering Consolidation

**Priority**: MEDIUM (Technical Debt - Enhances user experience consistency)

### Problem Analysis

Message rendering is **duplicated across files** with inconsistent implementations:

| Feature | sam_chat_vanilla_v2.js | sam_ai_chat_widget.js |
|---------|------------------------|----------------------|
| Render message | `renderMessage()` (50 lines) | `addMessageToUI()` (different) |
| Format content | `formatMessageContent()` (45 lines) | `escapeHtml()` (different) |
| Add message | `addMessage()` | Different pattern |
| Streaming | `_updateStreamingContent()` | Not implemented |

Additionally, **activity display is duplicated** from `ChatInteraction`:
- `sam_chat_vanilla_v2.js` lines 3528-3610: Duplicates `ChatInteraction.show()`
- `sam_chat_vanilla_v2.js` lines 3717-3778: Duplicates `ACTIVITY_STATES` entirely

**Total duplicated code**: ~235 lines

### The Clean Architecture (Your Vision)

```
┌─────────────────────────────────────────────────────────────────────────┐
│  SamMessageRenderer (Isolated Component - ~150 lines)                   │
├─────────────────────────────────────────────────────────────────────────┤
│  RENDERING:                                                             │
│    • renderMessage(message) → HTML                                      │
│    • formatContent(content) → Markdown → HTML                           │
│    • renderChoiceButtons(choices) → Interactive buttons                 │
│                                                                         │
│  STREAMING:                                                             │
│    • startStreaming(container) → Creates placeholder                    │
│    • appendToken(text) → Efficient DOM update                           │
│    • finalize() → Cleanup streaming state                               │
│                                                                         │
│  CONFIGURATION:                                                         │
│    • layout: 'classic' | 'compact'                                      │
│    • showTimestamps: boolean                                            │
│    • showActions: boolean (copy, regenerate)                            │
└─────────────────────────────────────────────────────────────────────────┘
```

---

### Phase 4.1: Remove Duplicated Activity Display

**File**: `sam_chat_vanilla_v2.js`

**DELETE** these methods (use `ChatInteraction` instead):
- `updateActivity()` (lines 3528-3550) - 22 lines
- `_displayActivity()` (lines 3557-3610) - 53 lines
- `_getDefaultActivityStates()` (lines 3717-3778) - 61 lines

**REPLACE with**:
```javascript
// In constructor, create ChatInteraction instance
this.activityDisplay = new ChatInteraction(
    this.container.querySelector('.sam-activity-status'),
    { autoHideDelay: 0 }
);

// Replace updateActivity() calls:
// BEFORE: this.updateActivity('thinking', {});
// AFTER:  this.activityDisplay.show('thinking', {});

// Replace clearActivity() calls:
// BEFORE: this.clearActivity();
// AFTER:  this.activityDisplay.clear();
```

**Effort**: 30 minutes | **Impact**: ~136 lines removed

---

### Phase 4.2: Create SamMessageRenderer

**Create file**: `ai_sam/static/src/js/ui/sam_message_renderer.js`

```javascript
/**
 * SamMessageRenderer - Unified message rendering for all chat UIs
 *
 * SINGLE RESPONSIBILITY: Convert message objects to HTML.
 * Used by all chat entry points for consistent message display.
 */
class SamMessageRenderer {
    constructor(options = {}) {
        this.layout = options.layout || 'classic';
        this.showTimestamps = options.showTimestamps !== false;
        this.showActions = options.showActions !== false;
        this.onChoiceSelected = options.onChoiceSelected || (() => {});
        this.onCopy = options.onCopy || (() => {});
        this.onRegenerate = options.onRegenerate || (() => {});

        // Streaming state
        this._streamingElement = null;
        this._streamingContent = '';
    }

    renderMessage(message) {
        const { role, content, timestamp, isStreaming } = message;
        const formattedContent = this.formatContent(content);
        const timeStr = this.showTimestamps ? this._formatTime(timestamp) : '';

        return `
            <div class="sam-message sam-message--${role}" data-message-id="${message.id || ''}">
                <div class="sam-message__header">
                    <span class="sam-message__avatar">${role === 'user' ? '👤' : '✨'}</span>
                    <span class="sam-message__label">${role === 'user' ? 'You' : 'SAM'}</span>
                    ${timeStr ? `<span class="sam-message__time">${timeStr}</span>` : ''}
                </div>
                <div class="sam-message__content">${formattedContent}</div>
                ${isStreaming ? '<span class="sam-message__cursor">▊</span>' : ''}
                ${this.showActions && role === 'assistant' && !isStreaming ? this._renderActions() : ''}
            </div>
        `;
    }

    formatContent(content) {
        if (!content) return '';

        let formatted = content;

        // Strip code blocks
        formatted = formatted.replace(/```[\s\S]*?```/g, '');

        // Detect and render interactive choices
        const choices = this._extractChoices(formatted);
        if (choices.length > 0) {
            choices.forEach(choice => {
                formatted = formatted.replace(choice.fullMatch, '');
            });
            formatted += this._renderChoices(choices);
        }

        // Basic markdown
        return formatted
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            .replace(/`(.*?)`/g, '<code>$1</code>')
            .replace(/\n/g, '<br>');
    }

    _extractChoices(content) {
        const choicePattern = /^- ['"]([^'"]+)['"] \(([^)]+)\)/gm;
        const choices = [];
        let match;
        while ((match = choicePattern.exec(content)) !== null) {
            choices.push({ value: match[1], description: match[2], fullMatch: match[0] });
        }
        return choices;
    }

    _renderChoices(choices) {
        const buttons = choices.map(c => `
            <button class="sam-choice-btn" data-choice="${c.value}">
                <span class="sam-choice-btn__value">${c.value}</span>
                <span class="sam-choice-btn__desc">(${c.description})</span>
            </button>
        `).join('');
        return `<div class="sam-message__choices">${buttons}</div>`;
    }

    _renderActions() {
        return `
            <div class="sam-message__actions">
                <button class="sam-message__action" data-action="copy" title="Copy"><i class="fa fa-copy"></i></button>
                <button class="sam-message__action" data-action="regenerate" title="Regenerate"><i class="fa fa-refresh"></i></button>
            </div>
        `;
    }

    _formatTime(timestamp) {
        if (!timestamp) return '';
        return new Date(timestamp).toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });
    }

    // Streaming support
    startStreaming(container) {
        this._streamingContent = '';
        const streamEl = document.createElement('div');
        streamEl.className = 'sam-message sam-message--assistant sam-message--streaming';
        streamEl.innerHTML = `
            <div class="sam-message__header">
                <span class="sam-message__avatar">✨</span>
                <span class="sam-message__label">SAM</span>
            </div>
            <div class="sam-message__content"></div>
            <span class="sam-message__cursor">▊</span>
        `;
        container.appendChild(streamEl);
        this._streamingElement = streamEl;

        return {
            append: (text) => this._appendToken(text),
            finalize: () => this._finalizeStreaming(),
            getContent: () => this._streamingContent,
        };
    }

    _appendToken(text) {
        if (!this._streamingElement) return;
        this._streamingContent += text;
        const contentEl = this._streamingElement.querySelector('.sam-message__content');
        if (contentEl) contentEl.innerHTML = this.formatContent(this._streamingContent);
    }

    _finalizeStreaming() {
        if (!this._streamingElement) return;
        this._streamingElement.classList.remove('sam-message--streaming');
        this._streamingElement.querySelector('.sam-message__cursor')?.remove();
        if (this.showActions) {
            this._streamingElement.insertAdjacentHTML('beforeend', this._renderActions());
        }
        this._streamingElement = null;
    }

    attachEvents(container) {
        container.addEventListener('click', (e) => {
            const action = e.target.closest('[data-action]');
            const choice = e.target.closest('[data-choice]');

            if (action) {
                const messageEl = action.closest('.sam-message');
                const content = messageEl?.querySelector('.sam-message__content')?.textContent;
                if (action.dataset.action === 'copy') {
                    navigator.clipboard.writeText(content || '');
                    this.onCopy(content);
                } else if (action.dataset.action === 'regenerate') {
                    this.onRegenerate(messageEl?.dataset.messageId);
                }
            }

            if (choice) {
                this.onChoiceSelected(choice.dataset.choice);
            }
        });
    }
}

export { SamMessageRenderer };
if (typeof window !== 'undefined') {
    window.SamMessageRenderer = SamMessageRenderer;
}
```

**Effort**: 2 hours | **Impact**: Unified message rendering

---

### Phase 4.3: Add Message CSS to sam_overlay_base.css

**File**: `sam_ui_theme/static/src/css/sam_overlay_base.css`

```css
/* SAM MESSAGE SYSTEM */
.sam-message {
    display: flex;
    flex-direction: column;
    padding: 12px 16px;
    margin: 8px 0;
    border-radius: 12px;
    animation: sam-message-appear 0.2s ease;
}

@keyframes sam-message-appear {
    from { opacity: 0; transform: translateY(8px); }
    to { opacity: 1; transform: translateY(0); }
}

.sam-message--user {
    background: var(--sam-user-bg, #714B67);
    color: white;
    margin-left: 20%;
    border-bottom-right-radius: 4px;
}

.sam-message--assistant {
    background: var(--sam-assistant-bg, #f8f9fa);
    color: var(--sam-text, #1f2937);
    margin-right: 20%;
    border-bottom-left-radius: 4px;
}

.sam-message__header {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 8px;
    font-size: 13px;
}

.sam-message__cursor {
    animation: sam-cursor-blink 1s step-end infinite;
}

@keyframes sam-cursor-blink {
    0%, 100% { opacity: 1; }
    50% { opacity: 0; }
}

.sam-message__actions {
    display: flex;
    gap: 8px;
    margin-top: 8px;
    opacity: 0;
    transition: opacity 0.2s;
}

.sam-message:hover .sam-message__actions {
    opacity: 1;
}

.sam-choice-btn {
    padding: 8px 12px;
    background: white;
    border: 1px solid var(--sam-border, #e5e7eb);
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.2s;
}

.sam-choice-btn:hover {
    background: var(--sam-primary, #714B67);
    color: white;
}
```

**Effort**: 1 hour | **Impact**: Consistent message styling

---

### Phase 4.4: Integrate with sam_chat_vanilla_v2.js

1. Import renderer and ChatInteraction
2. Create instances in constructor
3. Replace `renderMessage()` → `this.messageRenderer.renderMessage()`
4. Replace `formatMessageContent()` → `this.messageRenderer.formatContent()`
5. DELETE duplicated activity methods (use `ChatInteraction`)

**Effort**: 2 hours | **Impact**: ~200 lines removed

---

### Phase 4 Summary

| Task | File | Effort | Lines Saved |
|------|------|--------|-------------|
| 4.1 Remove duplicated activity | `sam_chat_vanilla_v2.js` | 30 min | ~136 |
| 4.2 Create SamMessageRenderer | `sam_message_renderer.js` (new) | 2 hours | - |
| 4.3 Add message CSS | `sam_overlay_base.css` | 1 hour | 0 (shared) |
| 4.4 Integrate with vanilla chat | `sam_chat_vanilla_v2.js` | 2 hours | ~100 |

**Total Effort**: ~5.5 hours
**Total Lines Saved**: ~236 (plus consistent UX across all entry points)

---

### Phase 4 Validation Checklist

- [ ] `ChatInteraction` used instead of duplicated activity code
- [ ] `SamMessageRenderer` handles all message rendering
- [ ] Message styling consistent across fullscreen/overlay/canvas
- [ ] Streaming works with new renderer
- [ ] Interactive choices work with new renderer
- [ ] Copy/regenerate actions work
- [ ] No duplicated `ACTIVITY_STATES` in vanilla file

---

## Complete Implementation Order

| Phase | Focus | Effort | Dependencies | Cleanup Action |
|-------|-------|--------|--------------|----------------|
| **0** | Cleanup discipline setup | 10 min | None | Add DEPRECATION LOG header to files |
| **1** | `SamChatClient` - Transport layer | 2-3 hours | None | New file - no cleanup |
| **2** | Integrate with fullscreen chat | 2-3 hours | Phase 1 | COMMENT OUT old `sendMessage()` body |
| **3.1** | Fix mode handling bug | 5 min | None | Bug fix - no cleanup |
| **3.2** | `SamModal` + migrate modals | 3-4 hours | Phase 3.4 CSS | COMMENT OUT 5 modal methods |
| **3.3** | `SamMenuManager` + migrate menus | 4 hours | Phase 3.4 CSS | COMMENT OUT menu render code |
| **3.4** | Add menu/modal CSS | 1 hour | None | New CSS - no cleanup |
| **4.1** | Remove duplicated activity | 30 min | None | COMMENT OUT `updateActivity()`, `_displayActivity()`, `_getDefaultActivityStates()` |
| **4.2** | `SamMessageRenderer` | 2 hours | Phase 4.3 CSS | New file - no cleanup |
| **4.3** | Add message CSS | 1 hour | None | New CSS - no cleanup |
| **4.4** | Integrate renderer | 2 hours | Phase 4.2 | COMMENT OUT `renderMessage()`, `formatMessageContent()` |
| **5** | Final Cleanup Pass | 2 hours | All phases verified | REMOVE all commented blocks |

**Total Estimated Effort**: ~18-20 hours
**Total Lines Saved**: ~700+ lines
**Result**: Clean, modular, testable architecture

---

## Phase 5: Final Cleanup Pass

**ONLY EXECUTE AFTER ALL PHASES VERIFIED WORKING**

### Pre-Cleanup Checklist
- [ ] All 4 entry points tested and working
- [ ] No console errors in any mode
- [ ] User testing completed on all modals
- [ ] Menu functionality verified in fullscreen + overlay
- [ ] Message rendering looks correct everywhere
- [ ] Streaming works without issues
- [ ] Activity states display properly

### Cleanup Actions
1. Search for `// DEPRECATED - Phase` comments
2. Remove the commented code blocks
3. Remove orphaned imports
4. Update DEPRECATION LOG with removal date
5. Run linter/formatter
6. Final test of all entry points

### Commit Message Format
```
refactor(chat): Phase 5 - Remove deprecated code

Removes code deprecated in Phases 2-4:
- Old sendMessage() transport logic (replaced by SamChatClient)
- 5 inline modal implementations (replaced by SamModal)
- Duplicated menu rendering (replaced by SamMenuManager)
- Duplicated activity/message code (using ChatInteraction + SamMessageRenderer)

Total lines removed: ~700
```

---

**Ready for implementation!** Start with Phase 0 (add DEPRECATION LOG headers), then Phase 1 (create SamChatClient), then Phase 2 (integrate with fullscreen chat).
