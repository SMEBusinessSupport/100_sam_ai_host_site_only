# N8N Local Installation Guide

**Original file:** `n8n_local_installation_guide.html`
**Type:** HTML

---

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>N8N Local Installation Guide - Phase 3 User Guide</title>
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
        .status-box {
            background-color: #d4edda;
            border: 1px solid #c3e6cb;
            color: #155724;
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
        .info-box {
            background-color: #e7f3ff;
            border: 1px solid #b8daff;
            color: #004085;
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
        .access-link {
            display: inline-block;
            background-color: #3498db;
            color: white;
            padding: 10px 20px;
            text-decoration: none;
            border-radius: 5px;
            margin: 10px 0;
            font-weight: bold;
        }
        .access-link:hover {
            background-color: #2980b9;
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
        .docker-details {
            background-color: #f8f9fa;
            border-left: 4px solid #007bff;
            padding: 20px;
            margin: 20px 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="phase-header">
            <h1>🐳 N8N Local Installation Guide - Phase 3 Integration</h1>
            <p>Complete reference for your N8N Docker setup and Phase 3 development</p>
        </div>

        <div class="status-box">
            <strong>✅ Current Status: N8N is RUNNING and ACCESSIBLE</strong><br>
            Your N8N instance has been running successfully for 5+ days
        </div>

        <h2>🚀 Quick Access</h2>
        <a href="http://localhost:2200" class="access-link" target="_blank">Open N8N Interface → http://localhost:2200</a>
        
        <div class="info-box">
            <strong>Primary Access URL:</strong> <code>http://localhost:2200</code><br>
            <strong>Default N8N Port:</strong> 5678 (mapped to host port 2200)<br>
            <strong>Status:</strong> Running since September 2, 2025
        </div>

        <h2>🐳 Docker Container Information</h2>
        <div class="docker-details">
            <table>
                <tr>
                    <th>Property</th>
                    <th>Value</th>
                </tr>
                <tr>
                    <td><strong>Container Name</strong></td>
                    <td><code>n8n-existing</code></td>
                </tr>
                <tr>
                    <td><strong>Container ID</strong></td>
                    <td><code>54cf8d3ebd49</code></td>
                </tr>
                <tr>
                    <td><strong>Image</strong></td>
                    <td><code>n8nio/n8n:latest</code> (v1.108.2)</td>
                </tr>
                <tr>
                    <td><strong>Status</strong></td>
                    <td>Running (Auto-restart: unless-stopped)</td>
                </tr>
                <tr>
                    <td><strong>Host Port</strong></td>
                    <td>2200 → 5678 (container)</td>
                </tr>
                <tr>
                    <td><strong>Network</strong></td>
                    <td>n8n-existing_n8n-existing-network</td>
                </tr>
                <tr>
                    <td><strong>Internal IP</strong></td>
                    <td>172.20.0.2</td>
                </tr>
            </table>
        </div>

        <h2>📁 File System Locations</h2>

        <h3>Windows Host Paths</h3>
        <div class="code-block">
            <strong>Docker Compose Project Directory:</strong><br>
            <span class="path-highlight">C:\Users\total\.docker\n8n-existing\</span><br><br>
            
            <strong>Custom Nodes Directory:</strong><br>
            <span class="path-highlight">C:\Users\total\.docker\n8n-existing\custom-nodes\</span><br><br>
            
            <strong>Docker Compose File:</strong><br>
            <span class="path-highlight">C:\Users\total\.docker\n8n-existing\docker-compose.yml</span>
        </div>

        <h3>Container Internal Paths</h3>
        <div class="code-block">
            <strong>N8N Data Directory (inside container):</strong><br>
            <span class="path-highlight">/home/node/.n8n</span><br><br>
            
            <strong>Custom Nodes (inside container):</strong><br>
            <span class="path-highlight">/home/node/.n8n/custom</span><br><br>
            
            <strong>Working Directory:</strong><br>
            <span class="path-highlight">/home/node</span>
        </div>

        <h3>Docker Volume Information</h3>
        <div class="code-block">
            <strong>Main Data Volume:</strong><br>
            Name: <span class="path-highlight">n8n-docker_n8n_data</span><br>
            Mount Point: <span class="path-highlight">/var/lib/docker/volumes/n8n-docker_n8n_data/_data</span><br><br>
            
            <strong>Available Volumes:</strong><br>
            • n8n-docker_n8n_data (main data)<br>
            • n8n-clean_n8n_clean_data<br>
            • n8n_data<br>
            • n8n_n8n_data
        </div>

        <h2>⚙️ Environment Configuration</h2>
        <div class="code-block">
            <strong>Environment Variables:</strong><br>
            N8N_HOST=localhost<br>
            N8N_PORT=5678<br>
            N8N_PROTOCOL=http<br>
            WEBHOOK_URL=http://localhost:2200<br>
            NODE_VERSION=22.17.0<br>
            N8N_RELEASE_TYPE=stable<br>
            NODE_ENV=production
        </div>

        <h2>🔧 Docker Management Commands</h2>

        <h3>Container Control</h3>
        <div class="code-block">
            <strong>View Container Status:</strong><br>
            docker ps -a<br><br>
            
            <strong>Stop N8N:</strong><br>
            docker stop n8n-existing<br><br>
            
            <strong>Start N8N:</strong><br>
            docker start n8n-existing<br><br>
            
            <strong>Restart N8N:</strong><br>
            docker restart n8n-existing<br><br>
            
            <strong>View Logs:</strong><br>
            docker logs n8n-existing<br>
            docker logs -f n8n-existing  # Follow logs
        </div>

        <h3>Container Access</h3>
        <div class="code-block">
            <strong>Execute Commands in Container:</strong><br>
            docker exec -it n8n-existing /bin/sh<br><br>
            
            <strong>Check Container Details:</strong><br>
            docker inspect n8n-existing
        </div>

        <h2>🔄 Alternative Installation Options</h2>

        <div class="warning-box">
            <strong>Note:</strong> No standalone Windows executable (.exe) exists for N8N. All installations require either Docker or Node.js/npm.
        </div>

        <h3>Node.js/NPM Installation (Alternative)</h3>
        <div class="info-box">
            Your system has Node.js v22.18.0 and npm v10.9.3 installed, so you could optionally install N8N via npm as well.
        </div>

        <div class="code-block">
            <strong>Install N8N globally via npm:</strong><br>
            npm install n8n -g<br><br>
            
            <strong>Run N8N (would use port 5678):</strong><br>
            n8n<br>
            # or<br>
            n8n start
        </div>

        <h2>🎯 Phase 3 Integration Checklist</h2>

        <ul class="checklist">
            <li>N8N Docker container is running and accessible</li>
            <li>Web interface available at http://localhost:2200</li>
            <li>Custom nodes directory is mounted and accessible</li>
            <li>Docker volumes are properly configured for data persistence</li>
            <li>Environment variables are set for webhook integration</li>
            <li>Container has auto-restart policy (unless-stopped)</li>
            <li>Network configuration allows Odoo module communication</li>
        </ul>

        <h2>🔗 Integration Points for Odoo Module</h2>

        <div class="info-box">
            <strong>Key Integration Details for Phase 3:</strong><br><br>
            
            <strong>API Endpoint Base:</strong> <code>http://localhost:2200/api/v1/</code><br>
            <strong>Webhook Base URL:</strong> <code>http://localhost:2200</code><br>
            <strong>N8N Version:</strong> 1.108.2<br>
            <strong>Node.js Version:</strong> 22.17.0 (inside container)<br>
            <strong>Custom Nodes Path:</strong> Mounted to host for easy development
        </div>

        <h3>Workflow Export/Import</h3>
        <div class="code-block">
            <strong>N8N workflows can be exported as JSON and imported into Odoo module</strong><br>
            <strong>Custom nodes directory:</strong> C:\Users\total\.docker\n8n-existing\custom-nodes\<br>
            <strong>Data persistence:</strong> Via Docker volume n8n-docker_n8n_data
        </div>

        <h2>🚨 Troubleshooting</h2>

        <h3>If N8N is Not Accessible</h3>
        <div class="code-block">
            1. Check container status: docker ps -a<br>
            2. Start if stopped: docker start n8n-existing<br>
            3. Check logs: docker logs n8n-existing<br>
            4. Verify port mapping: Should show 0.0.0.0:2200->5678/tcp
        </div>

        <h3>If Data is Missing</h3>
        <div class="code-block">
            1. Check volume: docker volume inspect n8n-docker_n8n_data<br>
            2. Verify mounts: docker inspect n8n-existing | findstr Mounts<br>
            3. Check permissions in custom-nodes directory
        </div>

        <div class="phase-header" style="margin-top: 40px;">
            <h2>📋 Phase 3 Development Summary</h2>
            <p>Your N8N environment is ready for integration with The AI Automator Odoo module</p>
        </div>

        <div class="status-box">
            <strong>✅ Ready for Phase 3:</strong><br>
            • N8N is running and stable<br>
            • All file paths documented<br>
            • Docker configuration understood<br>
            • Integration endpoints identified<br>
            • Custom nodes directory accessible<br><br>
            
            <strong>Next Steps:</strong> Begin N8N API integration with Odoo module workflow execution engine
        </div>

        <hr>
        <p><em>Generated: September 7, 2025 | For: The AI Automator Phase 3 Development</em></p>
    </div>
</body>
</html>
```
