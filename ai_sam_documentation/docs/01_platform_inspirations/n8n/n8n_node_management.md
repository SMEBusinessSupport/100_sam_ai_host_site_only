# N8N Node Management

**Original file:** `n8n_node_management.html`
**Type:** HTML

---

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>N8N Node Management Methodology - Analysis Report</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            line-height: 1.6;
            background-color: #f5f5f5;
        }
        .container {
            background-color: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
            margin-bottom: 30px;
        }
        h2 {
            color: #34495e;
            margin-top: 30px;
            margin-bottom: 15px;
            padding-left: 10px;
            border-left: 4px solid #3498db;
        }
        h3 {
            color: #7f8c8d;
            margin-top: 20px;
        }
        .info-box {
            background-color: #e7f3ff;
            border: 1px solid #b8daff;
            color: #004085;
            padding: 15px;
            border-radius: 5px;
            margin: 20px 0;
        }
        .warning-box {
            background-color: #fff3cd;
            border: 1px solid #ffeaa7;
            color: #856404;
            padding: 15px;
            border-radius: 5px;
            margin: 20px 0;
        }
        .code-block {
            background-color: #f8f9fa;
            border: 1px solid #dee2e6;
            padding: 15px;
            border-radius: 5px;
            font-family: 'Courier New', monospace;
            margin: 10px 0;
            overflow-x: auto;
        }
        .file-structure {
            background-color: #2d3748;
            color: #e2e8f0;
            padding: 20px;
            border-radius: 8px;
            font-family: 'Courier New', monospace;
            margin: 15px 0;
            overflow-x: auto;
        }
        .path-highlight {
            background-color: #ffffcc;
            padding: 2px 5px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
            font-weight: bold;
        }
        table {
            border-collapse: collapse;
            width: 100%;
            margin: 20px 0;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }
        th {
            background-color: #f2f2f2;
            font-weight: bold;
        }
        .checklist {
            list-style-type: none;
            padding: 0;
        }
        .checklist li {
            padding: 5px 0;
            position: relative;
            padding-left: 25px;
        }
        .checklist li:before {
            content: '✅';
            position: absolute;
            left: 0;
        }
        .phase-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 30px;
            text-align: center;
        }
        .json-example {
            background-color: #2d3748;
            color: #e2e8f0;
            padding: 20px;
            border-radius: 8px;
            font-family: 'Courier New', monospace;
            margin: 15px 0;
            overflow-x: auto;
        }
        .key {
            color: #81c784;
        }
        .string {
            color: #ffcc80;
        }
        .number {
            color: #90caf9;
        }
        .category-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }
        .category-item {
            background-color: #f8f9fa;
            padding: 10px;
            border-radius: 5px;
            border-left: 4px solid #17a2b8;
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="phase-header">
            <h1>📁 N8N Node Management Methodology</h1>
            <p>Complete analysis of N8N's file storage, naming conventions, and organizational structure</p>
        </div>

        <div class="info-box">
            <strong>📊 Analysis Source:</strong><br>
            • Local N8N nodes directory: <code>C:\Working With AI\Odoo Projects\custom-modules-v18\the_ai_automator\static\src\n8n\n8n_nodes</code><br>
            • N8N Docker installation: <code>http://localhost:2200</code><br>
            • Analysis performed: September 20, 2025
        </div>

        <h2>🏗️ Directory Structure Overview</h2>

        <h3>Root Organization</h3>
        <div class="file-structure">
n8n_nodes/
├── ActionNetwork/
├── ActiveCampaign/
├── Airtable/
├── OpenAi/
├── Slack/
├── ManualTrigger/
├── ... (150+ node directories)
        </div>

        <div class="info-box">
            <strong>Key Insight:</strong> Each service/integration gets its own directory named in <strong>PascalCase</strong> (e.g., <code>OpenAi</code>, <code>SlackTrigger</code>, <code>ManualTrigger</code>)
        </div>

        <h2>📋 File Naming Conventions</h2>

        <h3>Core Required Files</h3>
        <table>
            <tr>
                <th>File Pattern</th>
                <th>Purpose</th>
                <th>Example</th>
                <th>Required</th>
            </tr>
            <tr>
                <td><code>{NodeName}.node.json</code></td>
                <td>Node metadata and configuration</td>
                <td><code>Slack.node.json</code></td>
                <td>✅ Yes</td>
            </tr>
            <tr>
                <td><code>{NodeName}.node.js</code></td>
                <td>Compiled JavaScript implementation</td>
                <td><code>Slack.node.js</code></td>
                <td>✅ Yes</td>
            </tr>
            <tr>
                <td><code>{NodeName}.node.d.ts</code></td>
                <td>TypeScript type definitions</td>
                <td><code>Slack.node.d.ts</code></td>
                <td>✅ Yes</td>
            </tr>
            <tr>
                <td><code>{NodeName}.node.js.map</code></td>
                <td>Source map for debugging</td>
                <td><code>Slack.node.js.map</code></td>
                <td>🔄 Auto-generated</td>
            </tr>
            <tr>
                <td><code>{NodeName}.node.d.ts.map</code></td>
                <td>TypeScript source map</td>
                <td><code>Slack.node.d.ts.map</code></td>
                <td>🔄 Auto-generated</td>
            </tr>
        </table>

        <h3>Trigger Node Files</h3>
        <div class="warning-box">
            <strong>Special Pattern:</strong> Services that support triggers follow the <code>{NodeName}Trigger.node.*</code> naming pattern
        </div>

        <table>
            <tr>
                <th>File Pattern</th>
                <th>Example</th>
                <th>Purpose</th>
            </tr>
            <tr>
                <td><code>{NodeName}Trigger.node.json</code></td>
                <td><code>SlackTrigger.node.json</code></td>
                <td>Trigger-specific metadata</td>
            </tr>
            <tr>
                <td><code>{NodeName}Trigger.node.js</code></td>
                <td><code>SlackTrigger.node.js</code></td>
                <td>Trigger implementation logic</td>
            </tr>
            <tr>
                <td><code>{NodeName}Trigger.node.d.ts</code></td>
                <td><code>SlackTrigger.node.d.ts</code></td>
                <td>Trigger TypeScript definitions</td>
            </tr>
        </table>

        <h3>Supporting Files</h3>
        <table>
            <tr>
                <th>File Pattern</th>
                <th>Purpose</th>
                <th>Example</th>
            </tr>
            <tr>
                <td><code>{NodeName}.svg</code></td>
                <td>Light theme icon</td>
                <td><code>slack.svg</code></td>
            </tr>
            <tr>
                <td><code>{NodeName}.dark.svg</code></td>
                <td>Dark theme icon</td>
                <td><code>openAi.dark.svg</code></td>
            </tr>
            <tr>
                <td><code>{Feature}Description.js</code></td>
                <td>Feature-specific logic</td>
                <td><code>ChatDescription.js</code></td>
            </tr>
            <tr>
                <td><code>GenericFunctions.js</code></td>
                <td>Shared utility functions</td>
                <td><code>GenericFunctions.js</code></td>
            </tr>
            <tr>
                <td><code>{NodeName}Helpers.js</code></td>
                <td>Node-specific helpers</td>
                <td><code>SlackTriggerHelpers.js</code></td>
            </tr>
        </table>

        <h3>Directory-Based Organization</h3>
        <table>
            <tr>
                <th>Directory</th>
                <th>Purpose</th>
                <th>Example Location</th>
            </tr>
            <tr>
                <td><code>V1/</code>, <code>V2/</code></td>
                <td>API version management</td>
                <td><code>Slack/V1/</code>, <code>Slack/V2/</code></td>
            </tr>
            <tr>
                <td><code>__schema__/</code></td>
                <td>Schema definitions</td>
                <td><code>Slack/__schema__/</code></td>
            </tr>
        </table>

        <h2>📄 JSON Metadata Structure</h2>

        <h3>Standard Node Metadata Pattern</h3>
        <div class="json-example">
{
  <span class="key">"node"</span>: <span class="string">"n8n-nodes-base.{nodeName}"</span>,
  <span class="key">"nodeVersion"</span>: <span class="string">"1.0"</span>,
  <span class="key">"codexVersion"</span>: <span class="string">"1.0"</span>,
  <span class="key">"categories"</span>: [<span class="string">"Communication"</span>, <span class="string">"Utility"</span>, <span class="string">"Core Nodes"</span>],
  <span class="key">"subcategories"</span>: {
    <span class="key">"HITL"</span>: [<span class="string">"Human in the Loop"</span>]
  },
  <span class="key">"alias"</span>: [<span class="string">"alternative"</span>, <span class="string">"names"</span>, <span class="string">"keywords"</span>],
  <span class="key">"resources"</span>: {
    <span class="key">"credentialDocumentation"</span>: [
      {<span class="key">"url"</span>: <span class="string">"https://docs.n8n.io/integrations/..."</span>}
    ],
    <span class="key">"primaryDocumentation"</span>: [
      {<span class="key">"url"</span>: <span class="string">"https://docs.n8n.io/integrations/..."</span>}
    ],
    <span class="key">"generic"</span>: [
      {
        <span class="key">"label"</span>: <span class="string">"Tutorial title"</span>,
        <span class="key">"icon"</span>: <span class="string">"🚀"</span>,
        <span class="key">"url"</span>: <span class="string">"https://n8n.io/blog/..."</span>
      }
    ]
  }
}
        </div>

        <h3>Available Categories</h3>
        <div class="category-grid">
            <div class="category-item">Communication</div>
            <div class="category-item">Core Nodes</div>
            <div class="category-item">Utility</div>
            <div class="category-item">CRM</div>
            <div class="category-item">Marketing</div>
            <div class="category-item">Development</div>
            <div class="category-item">E-commerce</div>
            <div class="category-item">File Management</div>
            <div class="category-item">Analytics</div>
            <div class="category-item">Cloud Services</div>
            <div class="category-item">Database</div>
            <div class="category-item">HITL</div>
        </div>

        <h2>🔍 Analysis Examples</h2>

        <h3>Example 1: Slack Node Structure</h3>
        <div class="file-structure">
Slack/
├── __schema__/                    # Schema definitions
├── V1/                           # Version 1 implementation
├── V2/                           # Version 2 implementation
├── Slack.node.json              # Main node metadata
├── Slack.node.js                # Main node implementation
├── Slack.node.d.ts              # Main node TypeScript definitions
├── SlackTrigger.node.json       # Trigger node metadata
├── SlackTrigger.node.js         # Trigger implementation
├── SlackTrigger.node.d.ts       # Trigger TypeScript definitions
├── SlackTriggerHelpers.js       # Trigger-specific helpers
├── slack.svg                    # Light theme icon
└── *.map files                  # Source maps (auto-generated)
        </div>

        <h3>Example 2: OpenAI Node Structure</h3>
        <div class="file-structure">
OpenAi/
├── __schema__/                   # Schema definitions
├── OpenAi.node.json             # Main node metadata
├── OpenAi.node.js               # Main node implementation
├── OpenAi.node.d.ts             # TypeScript definitions
├── ChatDescription.js           # Chat-specific logic
├── ImageDescription.js          # Image generation logic
├── TextDescription.js           # Text processing logic
├── GenericFunctions.js          # Shared utilities
├── openAi.svg                   # Light theme icon
├── openAi.dark.svg              # Dark theme icon
└── *.map files                  # Source maps
        </div>

        <h3>Example 3: Simple Node Structure (ManualTrigger)</h3>
        <div class="file-structure">
ManualTrigger/
├── ManualTrigger.node.json      # Node metadata
├── ManualTrigger.node.js        # Implementation
├── ManualTrigger.node.d.ts      # TypeScript definitions
└── *.map files                  # Source maps
        </div>

        <h2>🎯 Key Insights for Odoo Module Development</h2>

        <h3>1. Consistent Naming Strategy</h3>
        <ul class="checklist">
            <li>Use PascalCase for directory names (e.g., <code>OdooAutomator</code>)</li>
            <li>Follow <code>{NodeName}.node.{extension}</code> pattern</li>
            <li>Use <code>{NodeName}Trigger.node.*</code> for trigger variants</li>
            <li>Include both light and dark theme SVG icons</li>
        </ul>

        <h3>2. Metadata-First Approach</h3>
        <ul class="checklist">
            <li>JSON file defines node identity and discoverability</li>
            <li>Categories determine where nodes appear in N8N UI</li>
            <li>Aliases improve searchability</li>
            <li>Resources provide documentation links</li>
        </ul>

        <h3>3. Version Management</h3>
        <ul class="checklist">
            <li>Use subdirectories for API version separation</li>
            <li>Maintain backward compatibility through versioning</li>
            <li>Schema directory for complex data structures</li>
        </ul>

        <h3>4. Modular Architecture</h3>
        <ul class="checklist">
            <li>Separate complex features into description files</li>
            <li>Use helper files for shared functionality</li>
            <li>Maintain clean separation of concerns</li>
            <li>Include TypeScript definitions for type safety</li>
        </ul>

        <h2>🚀 Implementation Recommendations</h2>

        <h3>For Your Odoo Module:</h3>
        <div class="info-box">
            <strong>Suggested Node Structure:</strong><br><br>

            <code>OdooAutomator/</code><br>
            ├── <code>OdooAutomator.node.json</code> (main node metadata)<br>
            ├── <code>OdooAutomator.node.js</code> (implementation)<br>
            ├── <code>OdooAutomator.node.d.ts</code> (TypeScript definitions)<br>
            ├── <code>OdooTrigger.node.json</code> (trigger variant)<br>
            ├── <code>OdooTrigger.node.js</code> (trigger implementation)<br>
            ├── <code>GenericFunctions.js</code> (Odoo API helpers)<br>
            ├── <code>RecordOperations.js</code> (CRUD operations)<br>
            ├── <code>WorkflowDescription.js</code> (workflow logic)<br>
            ├── <code>odoo.svg</code> (light icon)<br>
            ├── <code>odoo.dark.svg</code> (dark icon)<br>
            └── <code>V1/</code> (version-specific implementations)
        </div>

        <h3>Recommended Categories for Odoo Nodes:</h3>
        <div class="code-block">
            "categories": ["CRM", "Development", "Database"]
        </div>

        <h3>Suggested Aliases:</h3>
        <div class="code-block">
            "alias": ["ERP", "business", "automation", "workflow", "database"]
        </div>

        <h2>📚 Learning Summary</h2>

        <div class="warning-box">
            <strong>Critical Understanding:</strong><br>
            When you copy/paste N8N nodes in the canvas, you're actually working with JSON-based workflow definitions that reference these structured node files. The file organization enables N8N's auto-discovery, categorization, and execution engine.
        </div>

        <ul class="checklist">
            <li>N8N uses a convention-over-configuration approach</li>
            <li>File names and structure directly impact functionality</li>
            <li>JSON metadata drives UI presentation and categorization</li>
            <li>TypeScript support is mandatory for professional development</li>
            <li>Icon theming enhances user experience</li>
            <li>Version management enables API evolution</li>
            <li>Modular architecture supports complex integrations</li>
        </ul>

        <div class="phase-header" style="margin-top: 40px;">
            <h2>🎯 Next Steps for Integration</h2>
            <p>Apply these learnings to create professional N8N nodes for your Odoo automation module</p>
        </div>

        <hr>
        <p><em>Generated: September 20, 2025 | Analysis of N8N Node Management for The AI Automator Phase 3</em></p>
    </div>
</body>
</html>
```
