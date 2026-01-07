# Sam Python Dependencies

**Original file:** `SAM_PYTHON_DEPENDENCIES.html`
**Type:** HTML

---

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SAM AI Python Dependencies</title>
    <style>
        :root {
            --bg-dark: #1a1a2e;
            --bg-card: #16213e;
            --bg-hover: #1f3460;
            --accent-blue: #4a9eff;
            --accent-green: #4ade80;
            --accent-purple: #a78bfa;
            --accent-orange: #fb923c;
            --accent-pink: #f472b6;
            --accent-cyan: #22d3ee;
            --accent-yellow: #facc15;
            --accent-red: #f87171;
            --text-primary: #e2e8f0;
            --text-secondary: #94a3b8;
            --border-color: #334155;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
            background: var(--bg-dark);
            color: var(--text-primary);
            line-height: 1.6;
            padding: 20px;
            min-height: 100vh;
        }

        .container {
            max-width: 1400px;
            margin: 0 auto;
        }

        header {
            text-align: center;
            margin-bottom: 40px;
            padding: 30px;
            background: linear-gradient(135deg, var(--bg-card), #1e3a5f);
            border-radius: 16px;
            border: 1px solid var(--border-color);
        }

        header h1 {
            font-size: 2.5rem;
            margin-bottom: 10px;
            background: linear-gradient(135deg, var(--accent-green), var(--accent-cyan));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        header p {
            color: var(--text-secondary);
            font-size: 1.1rem;
        }

        .updated {
            font-size: 0.85rem;
            color: var(--accent-green);
            margin-top: 10px;
        }

        /* Category Sections */
        .category {
            background: var(--bg-card);
            border-radius: 16px;
            padding: 25px;
            margin-bottom: 25px;
            border: 1px solid var(--border-color);
        }

        .category-header {
            display: flex;
            align-items: center;
            gap: 15px;
            margin-bottom: 20px;
            padding-bottom: 15px;
            border-bottom: 1px solid var(--border-color);
        }

        .category-icon {
            width: 48px;
            height: 48px;
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5rem;
        }

        .category-title {
            flex: 1;
        }

        .category-title h2 {
            font-size: 1.4rem;
            margin-bottom: 4px;
        }

        .category-title p {
            font-size: 0.9rem;
            color: var(--text-secondary);
        }

        .status-badge {
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 600;
            text-transform: uppercase;
        }

        .status-critical { background: rgba(248, 113, 113, 0.2); color: var(--accent-red); }
        .status-important { background: rgba(251, 146, 60, 0.2); color: var(--accent-orange); }
        .status-optional { background: rgba(74, 222, 128, 0.2); color: var(--accent-green); }

        /* Dependency Table */
        .dep-table {
            width: 100%;
            border-collapse: collapse;
        }

        .dep-table th,
        .dep-table td {
            padding: 14px 16px;
            text-align: left;
            border-bottom: 1px solid var(--border-color);
        }

        .dep-table th {
            background: var(--bg-hover);
            font-weight: 600;
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            color: var(--accent-blue);
        }

        .dep-table tr:hover {
            background: var(--bg-hover);
        }

        .dep-table tr:last-child td {
            border-bottom: none;
        }

        .package-name {
            font-family: 'Consolas', 'Monaco', monospace;
            color: var(--accent-cyan);
            font-weight: 600;
        }

        .version {
            font-family: 'Consolas', 'Monaco', monospace;
            color: var(--accent-purple);
            font-size: 0.85rem;
        }

        .used-by {
            display: flex;
            flex-wrap: wrap;
            gap: 6px;
        }

        .used-by-tag {
            font-size: 0.75rem;
            padding: 3px 8px;
            border-radius: 4px;
            background: rgba(74, 158, 255, 0.15);
            color: var(--accent-blue);
            font-family: monospace;
        }

        .fallback-note {
            font-size: 0.8rem;
            color: var(--accent-yellow);
            display: flex;
            align-items: center;
            gap: 6px;
        }

        /* Installation Section */
        .install-section {
            background: var(--bg-card);
            border-radius: 16px;
            padding: 25px;
            margin-bottom: 25px;
            border: 1px solid var(--border-color);
        }

        .install-header {
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 20px;
        }

        .install-header h2 {
            font-size: 1.3rem;
        }

        .code-block {
            background: #0d1117;
            border-radius: 10px;
            padding: 20px;
            font-family: 'Consolas', 'Monaco', monospace;
            font-size: 0.9rem;
            overflow-x: auto;
            border: 1px solid var(--border-color);
            margin-bottom: 15px;
        }

        .code-comment {
            color: #6a737d;
        }

        .code-command {
            color: var(--accent-green);
        }

        /* Graceful Degradation */
        .graceful-section {
            background: linear-gradient(135deg, rgba(74, 222, 128, 0.1), rgba(34, 211, 238, 0.1));
            border-radius: 16px;
            padding: 25px;
            margin-bottom: 25px;
            border: 1px solid rgba(74, 222, 128, 0.3);
        }

        .graceful-header {
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 15px;
        }

        .graceful-header h2 {
            color: var(--accent-green);
        }

        .graceful-content {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
        }

        .graceful-card {
            background: var(--bg-card);
            border-radius: 12px;
            padding: 20px;
        }

        .graceful-card h3 {
            font-size: 1.1rem;
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .graceful-card ul {
            list-style: none;
            padding-left: 0;
        }

        .graceful-card li {
            padding: 6px 0;
            padding-left: 20px;
            position: relative;
            color: var(--text-secondary);
            font-size: 0.9rem;
        }

        .graceful-card li::before {
            content: '✓';
            position: absolute;
            left: 0;
            color: var(--accent-green);
        }

        /* Python Version Matrix */
        .version-matrix {
            background: var(--bg-card);
            border-radius: 16px;
            padding: 25px;
            margin-bottom: 25px;
            border: 1px solid var(--border-color);
        }

        .matrix-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 0.9rem;
        }

        .matrix-table th,
        .matrix-table td {
            padding: 12px;
            text-align: center;
            border: 1px solid var(--border-color);
        }

        .matrix-table th {
            background: var(--bg-hover);
        }

        .matrix-check {
            color: var(--accent-green);
            font-size: 1.2rem;
        }

        .matrix-warning {
            color: var(--accent-yellow);
            font-size: 1.2rem;
        }

        /* Footer */
        footer {
            text-align: center;
            padding: 20px;
            color: var(--text-secondary);
            font-size: 0.9rem;
        }

        /* Responsive */
        @media (max-width: 768px) {
            header h1 {
                font-size: 1.8rem;
            }

            .category-header {
                flex-direction: column;
                text-align: center;
            }

            .dep-table {
                font-size: 0.85rem;
            }

            .dep-table th,
            .dep-table td {
                padding: 10px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>SAM AI Python Dependencies</h1>
            <p>Complete reference for all Python packages used by the SAM AI ecosystem</p>
            <div class="updated">Last Updated: December 16, 2025 | Phase 16 (ML Layer)</div>
        </header>

        <!-- Graceful Degradation Section -->
        <div class="graceful-section">
            <div class="graceful-header">
                <span style="font-size: 1.5rem;">🛡️</span>
                <h2>Graceful Degradation Philosophy</h2>
            </div>
            <p style="margin-bottom: 20px; color: var(--text-secondary);">
                SAM AI is designed to work with minimal dependencies. Optional packages enhance functionality but are never required for core operations.
            </p>
            <div class="graceful-content">
                <div class="graceful-card">
                    <h3><span style="color: var(--accent-green);">✓</span> Always Works</h3>
                    <ul>
                        <li>Chat conversations with AI</li>
                        <li>Message streaming</li>
                        <li>Conversation history</li>
                        <li>Basic mode switching</li>
                        <li>API provider routing</li>
                    </ul>
                </div>
                <div class="graceful-card">
                    <h3><span style="color: var(--accent-cyan);">⚡</span> Enhanced With ML</h3>
                    <ul>
                        <li>User pattern recognition</li>
                        <li>Topic clustering</li>
                        <li>Communication style detection</li>
                        <li>Response optimization</li>
                        <li>Vocabulary enhancement</li>
                    </ul>
                </div>
                <div class="graceful-card">
                    <h3><span style="color: var(--accent-purple);">🔮</span> Enhanced With Memory</h3>
                    <ul>
                        <li>Semantic conversation search</li>
                        <li>Context from past conversations</li>
                        <li>Long-term user preferences</li>
                        <li>Related conversation retrieval</li>
                    </ul>
                </div>
            </div>
        </div>

        <!-- CRITICAL Dependencies -->
        <div class="category">
            <div class="category-header">
                <div class="category-icon" style="background: rgba(248, 113, 113, 0.2);">🔴</div>
                <div class="category-title">
                    <h2>Core AI APIs</h2>
                    <p>Required for SAM to communicate with AI providers</p>
                </div>
                <span class="status-badge status-critical">Critical</span>
            </div>
            <table class="dep-table">
                <thead>
                    <tr>
                        <th>Package</th>
                        <th>Version</th>
                        <th>Purpose</th>
                        <th>Used By</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><span class="package-name">anthropic</span></td>
                        <td><span class="version">>=0.18.0</span></td>
                        <td>Claude AI SDK integration - streaming, messages, tool use</td>
                        <td>
                            <div class="used-by">
                                <span class="used-by-tag">ai_brain.py</span>
                                <span class="used-by-tag">_chat_via_sdk()</span>
                            </div>
                        </td>
                    </tr>
                    <tr>
                        <td><span class="package-name">openai</span></td>
                        <td><span class="version">>=1.0.0</span></td>
                        <td>OpenAI GPT integration + Whisper transcription</td>
                        <td>
                            <div class="used-by">
                                <span class="used-by-tag">ai_youtube_transcribe</span>
                                <span class="used-by-tag">audio processing</span>
                            </div>
                        </td>
                    </tr>
                    <tr>
                        <td><span class="package-name">requests</span></td>
                        <td><span class="version">>=2.25.1</span></td>
                        <td>HTTP client for OpenAI-compatible API streaming (raw SSE)</td>
                        <td>
                            <div class="used-by">
                                <span class="used-by-tag">ai_brain.py</span>
                                <span class="used-by-tag">_chat_via_http()</span>
                            </div>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>

        <!-- Memory System -->
        <div class="category">
            <div class="category-header">
                <div class="category-icon" style="background: rgba(251, 146, 60, 0.2);">🧠</div>
                <div class="category-title">
                    <h2>Memory System</h2>
                    <p>Semantic search and conversation history</p>
                </div>
                <span class="status-badge status-important">Important</span>
            </div>
            <table class="dep-table">
                <thead>
                    <tr>
                        <th>Package</th>
                        <th>Version</th>
                        <th>Purpose</th>
                        <th>Fallback</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><span class="package-name">chromadb</span></td>
                        <td><span class="version">>=0.4.22</span></td>
                        <td>Vector database for semantic conversation search</td>
                        <td><span class="fallback-note">⚠️ Memory search disabled</span></td>
                    </tr>
                    <tr>
                        <td><span class="package-name">sentence-transformers</span></td>
                        <td><span class="version">>=2.2.0</span></td>
                        <td>Text embeddings for semantic similarity (downloads ~2GB models)</td>
                        <td><span class="fallback-note">⚠️ Falls back to keyword search</span></td>
                    </tr>
                </tbody>
            </table>
        </div>

        <!-- Machine Learning -->
        <div class="category">
            <div class="category-header">
                <div class="category-icon" style="background: rgba(74, 222, 128, 0.2);">🤖</div>
                <div class="category-title">
                    <h2>Machine Learning (Phase 16)</h2>
                    <p>Pattern recognition and personalization - SAM works perfectly without these</p>
                </div>
                <span class="status-badge status-optional">Optional</span>
            </div>
            <table class="dep-table">
                <thead>
                    <tr>
                        <th>Package</th>
                        <th>Version</th>
                        <th>Purpose</th>
                        <th>Fallback</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><span class="package-name">scikit-learn</span></td>
                        <td><span class="version">>=1.3.0</span></td>
                        <td>
                            <strong>TF-IDF Vectorization:</strong> Convert text to numerical features<br>
                            <strong>KMeans Clustering:</strong> Group conversations by topic<br>
                            <strong>Classification:</strong> Detect communication styles
                        </td>
                        <td><span class="fallback-note">✓ SAM works, just less personalized</span></td>
                    </tr>
                </tbody>
            </table>
            <div class="code-block" style="margin-top: 20px;">
<span class="code-comment"># Graceful degradation pattern in sam_voice.py</span>
try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.cluster import KMeans
    <span class="code-command">ML_AVAILABLE = True</span>
except ImportError:
    <span class="code-command">ML_AVAILABLE = False</span>
    _logger.info("Scikit-learn not installed. ML features disabled - SAM works normally.")
            </div>
        </div>

        <!-- Web Scraping -->
        <div class="category">
            <div class="category-header">
                <div class="category-icon" style="background: rgba(167, 139, 250, 0.2);">🕸️</div>
                <div class="category-title">
                    <h2>Web Scraping</h2>
                    <p>For ai_sam_lead_generator module</p>
                </div>
                <span class="status-badge status-optional">Optional</span>
            </div>
            <table class="dep-table">
                <thead>
                    <tr>
                        <th>Package</th>
                        <th>Version</th>
                        <th>Purpose</th>
                        <th>Used By</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><span class="package-name">beautifulsoup4</span></td>
                        <td><span class="version">>=4.11.0</span></td>
                        <td>HTML parsing for web scraping</td>
                        <td>
                            <div class="used-by">
                                <span class="used-by-tag">ai_sam_lead_generator</span>
                            </div>
                        </td>
                    </tr>
                    <tr>
                        <td><span class="package-name">lxml</span></td>
                        <td><span class="version">>=4.8.0</span></td>
                        <td>Fast XML/HTML processing (included in Odoo core)</td>
                        <td>
                            <div class="used-by">
                                <span class="used-by-tag">Odoo core</span>
                                <span class="used-by-tag">ai_sam_lead_generator</span>
                            </div>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>

        <!-- Git Operations -->
        <div class="category">
            <div class="category-header">
                <div class="category-icon" style="background: rgba(244, 114, 182, 0.2);">📦</div>
                <div class="category-title">
                    <h2>Git Operations</h2>
                    <p>For github_app module</p>
                </div>
                <span class="status-badge status-important">Important</span>
            </div>
            <table class="dep-table">
                <thead>
                    <tr>
                        <th>Package</th>
                        <th>Version</th>
                        <th>Purpose</th>
                        <th>Used By</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><span class="package-name">GitPython</span></td>
                        <td><span class="version">>=3.1.43</span></td>
                        <td>Git repository operations (clone, pull, commit, push)</td>
                        <td>
                            <div class="used-by">
                                <span class="used-by-tag">github_app</span>
                            </div>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>

        <!-- Installation Commands -->
        <div class="install-section">
            <div class="install-header">
                <span style="font-size: 1.5rem;">💻</span>
                <h2>Installation Commands</h2>
            </div>

            <h3 style="margin-bottom: 10px; color: var(--accent-blue);">Full Installation (All Features)</h3>
            <div class="code-block">
<span class="code-comment"># Install all SAM AI dependencies</span>
<span class="code-command">pip install anthropic openai chromadb sentence-transformers scikit-learn beautifulsoup4 GitPython</span>
            </div>

            <h3 style="margin-bottom: 10px; color: var(--accent-green);">Minimal Installation (Core Only)</h3>
            <div class="code-block">
<span class="code-comment"># Just the essentials - SAM will work with limited features</span>
<span class="code-command">pip install anthropic requests</span>
            </div>

            <h3 style="margin-bottom: 10px; color: var(--accent-purple);">From Requirements File</h3>
            <div class="code-block">
<span class="code-comment"># Using the python_bundle requirements</span>
<span class="code-command">pip install -r D:\SAMAI-18-SaaS\github-repos\14-samai_python_bundle\requirements.txt</span>
            </div>
        </div>

        <!-- Python Version Matrix -->
        <div class="version-matrix">
            <h2 style="margin-bottom: 20px;">Python Version Compatibility</h2>
            <table class="matrix-table">
                <thead>
                    <tr>
                        <th>Package</th>
                        <th>Python 3.10</th>
                        <th>Python 3.11</th>
                        <th>Python 3.12</th>
                        <th>Python 3.13</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><span class="package-name">anthropic</span></td>
                        <td><span class="matrix-check">✓</span></td>
                        <td><span class="matrix-check">✓</span></td>
                        <td><span class="matrix-check">✓</span></td>
                        <td><span class="matrix-check">✓</span></td>
                    </tr>
                    <tr>
                        <td><span class="package-name">openai</span></td>
                        <td><span class="matrix-check">✓</span></td>
                        <td><span class="matrix-check">✓</span></td>
                        <td><span class="matrix-check">✓</span></td>
                        <td><span class="matrix-check">✓</span></td>
                    </tr>
                    <tr>
                        <td><span class="package-name">chromadb</span></td>
                        <td><span class="matrix-check">✓</span></td>
                        <td><span class="matrix-check">✓</span></td>
                        <td><span class="matrix-check">✓</span></td>
                        <td><span class="matrix-warning">⚠️</span></td>
                    </tr>
                    <tr>
                        <td><span class="package-name">scikit-learn</span></td>
                        <td><span class="matrix-check">✓</span></td>
                        <td><span class="matrix-check">✓</span></td>
                        <td><span class="matrix-check">✓</span></td>
                        <td><span class="matrix-check">✓</span></td>
                    </tr>
                    <tr>
                        <td><span class="package-name">sentence-transformers</span></td>
                        <td><span class="matrix-check">✓</span></td>
                        <td><span class="matrix-check">✓</span></td>
                        <td><span class="matrix-check">✓</span></td>
                        <td><span class="matrix-warning">⚠️</span></td>
                    </tr>
                </tbody>
            </table>
            <p style="margin-top: 15px; font-size: 0.85rem; color: var(--text-secondary);">
                ⚠️ = May require specific version pins or have limited support
            </p>
        </div>

        <!-- Dependency Graph -->
        <div class="install-section">
            <div class="install-header">
                <span style="font-size: 1.5rem;">🔗</span>
                <h2>Dependency Relationships</h2>
            </div>
            <div class="code-block" style="font-size: 0.8rem; line-height: 1.3;">
<span style="color: var(--accent-cyan);">SAM AI Ecosystem</span>
│
├── <span style="color: var(--accent-red);">CRITICAL (Required)</span>
│   ├── anthropic        → Claude SDK streaming
│   └── requests         → OpenAI-compatible HTTP streaming
│
├── <span style="color: var(--accent-orange);">IMPORTANT (Recommended)</span>
│   ├── chromadb         → Vector database
│   │   └── numpy        (auto-installed)
│   ├── sentence-transformers → Text embeddings
│   │   └── torch        (auto-installed, ~2GB)
│   └── GitPython        → Git operations
│
├── <span style="color: var(--accent-green);">OPTIONAL (Enhanced Features)</span>
│   ├── scikit-learn     → ML personalization
│   │   ├── numpy        (shared with chromadb)
│   │   ├── scipy        (auto-installed)
│   │   └── joblib       (auto-installed)
│   ├── beautifulsoup4   → Web scraping
│   └── openai           → Whisper transcription
│
└── <span style="color: var(--text-secondary);">ODOO CORE (Already included)</span>
    ├── lxml             → XML/HTML parsing
    ├── Pillow           → Image processing
    ├── psycopg2         → PostgreSQL
    └── Werkzeug         → HTTP utilities
            </div>
        </div>

        <footer>
            <p>SAM AI Python Dependencies Documentation | Part of the SAM AI Architecture Schema</p>
            <p>Source: <code>D:\SAMAI-18-SaaS\github-repos\14-samai_python_bundle\requirements.txt</code></p>
        </footer>
    </div>
</body>
</html>

```
