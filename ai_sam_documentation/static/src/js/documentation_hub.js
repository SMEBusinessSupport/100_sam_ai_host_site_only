/**
 * Documentation Hub - JavaScript functionality
 *
 * Features:
 * - Sidebar toggle (mobile)
 * - Keyboard shortcuts (Ctrl+K for search)
 * - Live search with debounce
 * - Code syntax highlighting initialization
 * - Smooth scroll for anchor links
 * - Sidebar expand/collapse
 */

(function () {
    'use strict';

    // ==========================================================================
    // Configuration
    // ==========================================================================

    const CONFIG = {
        searchDebounceMs: 300,
        animationDuration: 200,
    };

    // ==========================================================================
    // DOM Ready Handler
    // ==========================================================================

    function initAll() {
        console.log('[DocsHub] Initializing documentation hub JS...');
        initSidebarToggle();
        initSidebarNavigation();
        initKeyboardShortcuts();
        initSmoothScroll();
        initCodeHighlighting();
        initSearchFocus();
        initDevShare();  // Dev Share for Claude sessions
        console.log('[DocsHub] Initialization complete');
    }

    // Try multiple initialization strategies for Odoo compatibility
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initAll);
    } else {
        // DOM already loaded, init immediately
        initAll();
    }

    // Also try after a short delay as fallback for Odoo's lazy loading
    setTimeout(initAll, 500);

    // ==========================================================================
    // Sidebar Toggle (Mobile)
    // ==========================================================================

    function initSidebarToggle() {
        const sidebar = document.querySelector('.o_docs_sidebar');
        const toggle = document.querySelector('.o_docs_sidebar_toggle');

        if (!sidebar || !toggle) return;

        toggle.addEventListener('click', function (e) {
            e.preventDefault();
            sidebar.classList.toggle('show');

            // Update icon
            const icon = toggle.querySelector('i');
            if (sidebar.classList.contains('show')) {
                icon.classList.remove('fa-bars');
                icon.classList.add('fa-times');
            } else {
                icon.classList.remove('fa-times');
                icon.classList.add('fa-bars');
            }
        });

        // Close sidebar when clicking outside
        document.addEventListener('click', function (e) {
            if (sidebar.classList.contains('show') &&
                !sidebar.contains(e.target) &&
                !toggle.contains(e.target)) {
                sidebar.classList.remove('show');
                const icon = toggle.querySelector('i');
                icon.classList.remove('fa-times');
                icon.classList.add('fa-bars');
            }
        });
    }

    // ==========================================================================
    // Sidebar Navigation (Expand/Collapse)
    // ==========================================================================

    function initSidebarNavigation() {
        const navHeaders = document.querySelectorAll('.o_docs_nav_header');

        navHeaders.forEach(function (header) {
            header.addEventListener('click', function (e) {
                // Allow link navigation if not just toggling
                if (e.target.closest('.o_docs_nav_chevron')) {
                    e.preventDefault();
                }

                const section = header.closest('.o_docs_nav_section');
                const items = section.querySelector('.o_docs_nav_items');

                if (items) {
                    items.classList.toggle('collapsed');
                    items.classList.toggle('expanded');
                }
            });
        });
    }

    // ==========================================================================
    // Keyboard Shortcuts
    // ==========================================================================

    function initKeyboardShortcuts() {
        document.addEventListener('keydown', function (e) {
            // Ctrl+K or Cmd+K - Focus search
            if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
                e.preventDefault();
                const searchInput = document.querySelector('.o_docs_search_input');
                if (searchInput) {
                    searchInput.focus();
                    searchInput.select();
                }
            }

            // Escape - Close sidebar on mobile
            if (e.key === 'Escape') {
                const sidebar = document.querySelector('.o_docs_sidebar.show');
                if (sidebar) {
                    sidebar.classList.remove('show');
                    const toggle = document.querySelector('.o_docs_sidebar_toggle');
                    if (toggle) {
                        const icon = toggle.querySelector('i');
                        icon.classList.remove('fa-times');
                        icon.classList.add('fa-bars');
                    }
                }
            }
        });
    }

    // ==========================================================================
    // Search Focus
    // ==========================================================================

    function initSearchFocus() {
        const searchInput = document.querySelector('.o_docs_search_input');
        if (!searchInput) return;

        // Show keyboard shortcut hint
        searchInput.addEventListener('focus', function () {
            const kbd = document.querySelector('.o_docs_search_kbd');
            if (kbd) kbd.style.opacity = '0';
        });

        searchInput.addEventListener('blur', function () {
            const kbd = document.querySelector('.o_docs_search_kbd');
            if (kbd) kbd.style.opacity = '1';
        });
    }

    // ==========================================================================
    // Smooth Scroll for Anchor Links
    // ==========================================================================

    function initSmoothScroll() {
        document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
            anchor.addEventListener('click', function (e) {
                const targetId = this.getAttribute('href');
                if (targetId === '#') return;

                const target = document.querySelector(targetId);
                if (target) {
                    e.preventDefault();
                    const topOffset = document.querySelector('.o_docs_topbar').offsetHeight + 20;

                    window.scrollTo({
                        top: target.offsetTop - topOffset,
                        behavior: 'smooth'
                    });

                    // Update URL without scrolling
                    history.pushState(null, null, targetId);
                }
            });
        });
    }

    // ==========================================================================
    // Code Syntax Highlighting
    // ==========================================================================

    function initCodeHighlighting() {
        // Check if Prism.js or Highlight.js is available
        if (typeof Prism !== 'undefined') {
            Prism.highlightAll();
        } else if (typeof hljs !== 'undefined') {
            document.querySelectorAll('pre code').forEach(function (block) {
                hljs.highlightBlock(block);
            });
        } else {
            // Fallback: Add basic language detection classes
            document.querySelectorAll('pre code').forEach(function (block) {
                addLanguageClass(block);
            });
        }
    }

    function addLanguageClass(block) {
        const content = block.textContent.trim();

        // Basic language detection heuristics
        const patterns = {
            python: [/^(import|from|def |class |if __name__|print\()/m, /:\s*$/m],
            javascript: [/^(const|let|var|function|import|export|=>)/m, /console\./],
            xml: [/^<\?xml|^<odoo|^<template|^<record/m],
            html: [/^<!DOCTYPE|^<html|^<div|^<span/im],
            sql: [/^(SELECT|INSERT|UPDATE|DELETE|CREATE|ALTER|DROP)/im],
            bash: [/^(#!\/bin\/|sudo |apt |npm |pip |git )/m],
            json: [/^\s*[\[{]/],
        };

        for (const [lang, regexList] of Object.entries(patterns)) {
            for (const regex of regexList) {
                if (regex.test(content)) {
                    block.classList.add('language-' + lang);
                    return;
                }
            }
        }
    }

    // ==========================================================================
    // Utility Functions
    // ==========================================================================

    function debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    // ==========================================================================
    // Live Search (Optional - can be enabled for async search)
    // ==========================================================================

    function initLiveSearch() {
        const searchInput = document.querySelector('.o_docs_search_input');
        if (!searchInput) return;

        const performSearch = debounce(async function (query) {
            if (query.length < 2) return;

            try {
                const response = await fetch('/documentation/api/search', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        jsonrpc: '2.0',
                        method: 'call',
                        params: { query: query },
                        id: Date.now(),
                    }),
                });

                const data = await response.json();
                if (data.result) {
                    displaySearchResults(data.result);
                }
            } catch (error) {
                console.error('Search error:', error);
            }
        }, CONFIG.searchDebounceMs);

        searchInput.addEventListener('input', function (e) {
            performSearch(e.target.value);
        });
    }

    function displaySearchResults(results) {
        // This could show a dropdown with live results
        // For now, we use the form submission to the search page
        console.log('Search results:', results);
    }

    // ==========================================================================
    // Dev Share - Share with Claude (Dev Mode Only)
    // ==========================================================================

    // Initialize dev share - called from main DOMContentLoaded above
    function initDevShare() {
        const shareBtn = document.querySelector('.o_docs_dev_share_btn');
        if (!shareBtn) {
            console.log('[DevShare] Button not found - dev mode may be disabled');
            return;
        }

        // Prevent double initialization
        if (shareBtn.dataset.initialized === 'true') {
            console.log('[DevShare] Already initialized, skipping');
            return;
        }
        shareBtn.dataset.initialized = 'true';

        console.log('[DevShare] Button found, attaching click handler');

        shareBtn.addEventListener('click', async function (e) {
            e.preventDefault();
            e.stopPropagation();

            console.log('[DevShare] Button clicked');

            // Get current path from URL
            const currentPath = window.location.pathname;
            console.log('[DevShare] Current path:', currentPath);

            try {
                // Get CSRF token from Odoo
                const csrfToken = odoo?.csrf_token || document.querySelector('input[name="csrf_token"]')?.value || '';

                // Call the dev share API
                const response = await fetch('/documentation/dev/share', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        jsonrpc: '2.0',
                        method: 'call',
                        params: { path: currentPath },
                        id: Date.now(),
                    }),
                    credentials: 'same-origin',  // Include cookies for session
                });

                console.log('[DevShare] API response status:', response.status);
                const data = await response.json();
                console.log('[DevShare] API response:', JSON.stringify(data, null, 2));

                if (data.result && data.result.success) {
                    // Format the shareable content
                    const shareContent = formatShareContent(data.result);
                    console.log('[DevShare] Content to copy:', shareContent.substring(0, 200) + '...');

                    // Copy to clipboard
                    await navigator.clipboard.writeText(shareContent);
                    console.log('[DevShare] Copied to clipboard!');

                    // Show success feedback
                    showShareFeedback(shareBtn, 'Copied!', 'success');
                } else {
                    const errorMsg = data.result?.error || data.error?.message || 'Failed to generate share content';
                    console.error('[DevShare] API error:', errorMsg);
                    showShareFeedback(shareBtn, errorMsg, 'error');
                }
            } catch (error) {
                console.error('[DevShare] Error:', error);
                showShareFeedback(shareBtn, 'Error: ' + error.message, 'error');
            }
        });
    }

    function formatShareContent(result) {
        // Format as a simple file/folder path for Claude to access directly
        // Example output: See this file "D:\path\to\file.md"
        const pathType = result.type === 'folder' ? 'folder' : 'file';
        return `See this ${pathType} "${result.file_path}"`;
    }

    function showShareFeedback(btn, message, type) {
        const originalIcon = btn.innerHTML;
        const iconClass = type === 'success' ? 'fa-check' : 'fa-times';
        const colorClass = type === 'success' ? 'text-success' : 'text-danger';

        btn.innerHTML = `<i class="fa ${iconClass} ${colorClass}"></i>`;
        btn.title = message;

        setTimeout(() => {
            btn.innerHTML = originalIcon;
            btn.title = 'Share with Claude (Dev Mode)';
        }, 2000);
    }

})();
