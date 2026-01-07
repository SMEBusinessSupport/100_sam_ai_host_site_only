# Ecosystem Analysis 20251013 235651

**Original file:** `ecosystem_analysis_20251013_235651.json`
**Type:** JSON

---

```json
{
  "modules": {
    "ai_brain": {
      "total_lines": 16840,
      "total_files": 63,
      "files_by_type": {
        ".py": 59,
        ".xml": 4
      },
      "lines_by_type": {
        ".py": 16670,
        ".xml": 170
      },
      "commented_lines": 7403,
      "blank_lines": 2655,
      "code_lines": 6782,
      "commented_blocks": [
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_brain\\models\\ai_artifact_version.py",
          "start_line": 39,
          "end_line": 59,
          "lines": 18,
          "preview": "        \"\"\"Create a new artifact version from parsed artifact data\"\"\"\n        # Get the latest version for this conversation\n        latest = self.search([\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_brain\\models\\ai_automator_config.py",
          "start_line": 18,
          "end_line": 27,
          "lines": 9,
          "preview": "        \"\"\"Load current settings from config parameters\"\"\"\n        res = super().default_get(fields_list)\n        if 'knowledge_visualizer_enabled' in fields_list:\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_brain\\models\\ai_branches.py",
          "start_line": 224,
          "end_line": 236,
          "lines": 12,
          "preview": "        \"\"\"Check if the required module is installed\"\"\"\n        for record in self:\n            if record.module_name:\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_brain\\models\\ai_branches.py",
          "start_line": 255,
          "end_line": 264,
          "lines": 9,
          "preview": "        \"\"\"Ensure technical name is lowercase and valid\"\"\"\n        for record in self:\n            if not record.technical_name.islower() or ' ' in record.technical_name:\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_brain\\models\\ai_branches.py",
          "start_line": 336,
          "end_line": 338,
          "lines": 3,
          "preview": "        \"\"\"\n        Open canvas creation wizard for this branch type\n        \"\"\"\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_brain\\models\\ai_claude_history_importer.py",
          "start_line": 227,
          "end_line": 271,
          "lines": 36,
          "preview": "        \"\"\"Import conversations from uploaded JSON file\"\"\"\n        if not self.file_data:\n            raise ValidationError(_('Please upload a JSON file first'))\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_brain\\models\\ai_context_builder.py",
          "start_line": 103,
          "end_line": 116,
          "lines": 12,
          "preview": "        \"\"\"Get list of installed modules\"\"\"\n        Module = self.env['ir.module.module']\n        modules = Module.search([\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_brain\\models\\ai_context_builder.py",
          "start_line": 128,
          "end_line": 135,
          "lines": 7,
          "preview": "        \"\"\"Format module list for prompt\"\"\"\n        lines = []\n        for module in modules:\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_brain\\models\\ai_context_builder.py",
          "start_line": 196,
          "end_line": 242,
          "lines": 37,
          "preview": "        \"\"\"Get important fields from record\"\"\"\n        lines = []\n        # Get field definitions\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_brain\\models\\ai_conversation.py",
          "start_line": 180,
          "end_line": 186,
          "lines": 6,
          "preview": "        \"\"\"Check if conversation is shared in any workspace\"\"\"\n        for record in self:\n            record.is_shared = bool(record.workspace_ids)\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_brain\\models\\ai_conversation_import.py",
          "start_line": 153,
          "end_line": 165,
          "lines": 12,
          "preview": "        \"\"\"Auto-detect if path is file or directory\"\"\"\n        for record in self:\n            if record.source_path and os.path.exists(record.source_path):\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_brain\\models\\ai_conversation_import.py",
          "start_line": 639,
          "end_line": 651,
          "lines": 11,
          "preview": "        \"\"\"Create ai.conversation record\"\"\"\n        # Claude export uses 'name', fallback to 'title' for other formats\n        conv_name = conv_data.get('name') or conv_data.get('title') or 'Untitled Conversation'\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_brain\\models\\ai_document_extractor.py",
          "start_line": 36,
          "end_line": 50,
          "lines": 11,
          "preview": "        \"\"\"Register built-in extractors on first use\"\"\"\n        if AIDocumentExtractor._initialized:\n            return\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_brain\\models\\ai_document_extractor.py",
          "start_line": 96,
          "end_line": 102,
          "lines": 6,
          "preview": "        \"\"\"\n        cls._extractors[extension.lower()] = handler\n        _logger.debug(f\"Registered extractor for {extension}\")\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_brain\\models\\ai_document_extractor.py",
          "start_line": 220,
          "end_line": 227,
          "lines": 7,
          "preview": "        \"\"\"Extract JSON files\"\"\"\n        with open(file_path, 'r', encoding='utf-8') as f:\n            data = json.load(f)\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_brain\\models\\ai_document_extractor.py",
          "start_line": 237,
          "end_line": 251,
          "lines": 14,
          "preview": "        \"\"\"Extract PDF files\"\"\"\n        try:\n            import PyPDF2\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_brain\\models\\ai_document_extractor.py",
          "start_line": 261,
          "end_line": 278,
          "lines": 17,
          "preview": "        \"\"\"Extract Excel files\"\"\"\n        try:\n            import openpyxl\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_brain\\models\\ai_document_extractor.py",
          "start_line": 396,
          "end_line": 397,
          "lines": 2,
          "preview": "        \"\"\"\n        prompt = f\"\"\"Generate a Python function to extract content from {extension} files.\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_brain\\models\\ai_document_extractor.py",
          "start_line": 411,
          "end_line": 428,
          "lines": 13,
          "preview": "\"\"\"\n        conversation = self.env['ai.conversation'].create({\n            'name': f'Extractor Generation: {extension}'\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_brain\\models\\ai_graph_service.py",
          "start_line": 242,
          "end_line": 246,
          "lines": 4,
          "preview": "        \"\"\"\n        Get the graph structure for a conversation (nodes + relationships)\n        Returns visualization data for the conversation and its connections\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_brain\\models\\ai_message.py",
          "start_line": 100,
          "end_line": 108,
          "lines": 8,
          "preview": "        \"\"\"Override create to estimate tokens if not provided\"\"\"\n        for vals in vals_list:\n            if not vals.get('token_count') and vals.get('content'):\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_brain\\models\\ai_registry_watcher.py",
          "start_line": 26,
          "end_line": 45,
          "lines": 15,
          "preview": "        \"\"\"Override write to detect module state changes\"\"\"\n        # Store old states\n        old_states = {module.id: module.state for module in self}\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_brain\\models\\ai_registry_watcher.py",
          "start_line": 51,
          "end_line": 72,
          "lines": 19,
          "preview": "        \"\"\"\n        # Log the change\n        if new_state == 'installed':\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_brain\\models\\ai_registry_watcher.py",
          "start_line": 77,
          "end_line": 99,
          "lines": 18,
          "preview": "        \"\"\"\n        # Check if there's a branch registered for this module\n        Branch = self.env['ai.branch'].sudo()\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_brain\\models\\ai_service.py",
          "start_line": 144,
          "end_line": 185,
          "lines": 32,
          "preview": "        \"\"\"\n        if not config.api_key:\n            _logger.warning(\"Cannot count tokens: API key not configured\")\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_brain\\models\\ai_service.py",
          "start_line": 192,
          "end_line": 217,
          "lines": 21,
          "preview": "        \"\"\"\n        total_chars = 0\n        # Count system prompt\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_brain\\models\\ai_service.py",
          "start_line": 223,
          "end_line": 229,
          "lines": 6,
          "preview": "        \"\"\"\n        # Rough approximation: 1 token \u2248 4 characters\n        # Claude actually uses ~3.5 chars/token on average, but 4 is safer\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_brain\\models\\ai_service.py",
          "start_line": 276,
          "end_line": 290,
          "lines": 11,
          "preview": "        \"\"\"\n        # Exponential backoff: base_delay * (2 ^ (attempt - 1))\n        delay = config.retry_base_delay * (2 ** (attempt - 1))\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_brain\\models\\ai_service.py",
          "start_line": 297,
          "end_line": 331,
          "lines": 29,
          "preview": "        \"\"\"\n        # Rate limit errors (429) - always retry with backoff\n        if status_code == 429:\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_brain\\models\\ai_service.py",
          "start_line": 337,
          "end_line": 360,
          "lines": 20,
          "preview": "        \"\"\"\n        try:\n            # Try to parse JSON error response\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_brain\\models\\ai_service_config.py",
          "start_line": 134,
          "end_line": 148,
          "lines": 14,
          "preview": "        \"\"\"Set model_name based on provider on create\"\"\"\n        for vals in vals_list:\n            if 'api_provider' in vals:\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_brain\\models\\ai_service_config.py",
          "start_line": 418,
          "end_line": 435,
          "lines": 15,
          "preview": "        \"\"\"\n        config = self.search([('active', '=', True)], limit=1)\n        if not config:\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_brain\\models\\ai_service_config.py",
          "start_line": 518,
          "end_line": 530,
          "lines": 12,
          "preview": "        \"\"\"Create default configuration if none exists\"\"\"\n        existing = self.search([], limit=1)\n        if not existing:\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_brain\\models\\ai_service_config.py",
          "start_line": 611,
          "end_line": 618,
          "lines": 7,
          "preview": "        \"\"\"Validate token limits\"\"\"\n        for record in self:\n            if record.daily_token_limit < 0 or record.user_token_limit < 0:\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_brain\\models\\ai_service_config.py",
          "start_line": 625,
          "end_line": 632,
          "lines": 7,
          "preview": "        \"\"\"Validate max tokens\"\"\"\n        for record in self:\n            if record.max_tokens < 1 or record.max_tokens > 200000:\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_brain\\models\\ai_service_config.py",
          "start_line": 645,
          "end_line": 654,
          "lines": 9,
          "preview": "        \"\"\"Validate token counting configuration\"\"\"\n        for record in self:\n            if record.token_warning_threshold < 0 or record.token_warning_threshold > 200000:\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_brain\\models\\ai_service_provider.py",
          "start_line": 172,
          "end_line": 186,
          "lines": 13,
          "preview": "        \"\"\"Compute API key status for display\"\"\"\n        for record in self:\n            if record.api_key and len(record.api_key) > 10:\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_brain\\models\\ai_service_provider.py",
          "start_line": 352,
          "end_line": 359,
          "lines": 7,
          "preview": "        \"\"\"Validate priority is positive\"\"\"\n        for record in self:\n            if record.priority < 0:\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_brain\\models\\ai_token_usage.py",
          "start_line": 166,
          "end_line": 172,
          "lines": 6,
          "preview": "        \"\"\"Calculate total tokens\"\"\"\n        for record in self:\n            record.total_tokens = record.input_tokens + record.output_tokens\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_brain\\models\\ai_workspace.py",
          "start_line": 98,
          "end_line": 104,
          "lines": 6,
          "preview": "        \"\"\"Compute member count\"\"\"\n        for workspace in self:\n            workspace.member_count = len(workspace.member_ids)\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_brain\\models\\api_credentials.py",
          "start_line": 88,
          "end_line": 98,
          "lines": 10,
          "preview": "        \"\"\"Override create to validate credential data\"\"\"\n        for vals in vals_list:\n            if 'credential_data' in vals and vals['credential_data']:\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_brain\\models\\business_unit.py",
          "start_line": 26,
          "end_line": 37,
          "lines": 11,
          "preview": "        \"\"\"Display name with code if available\"\"\"\n        result = []\n        for record in self:\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_brain\\models\\canvas.py",
          "start_line": 113,
          "end_line": 126,
          "lines": 13,
          "preview": "        \"\"\"Compute branch_id from branch_type\"\"\"\n        for record in self:\n            if record.branch_type:\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_brain\\models\\canvas.py",
          "start_line": 138,
          "end_line": 155,
          "lines": 17,
          "preview": "        \"\"\"Validate JSON structure\"\"\"\n        for record in self:\n            if record.json_definition:\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_brain\\models\\canvas.py",
          "start_line": 245,
          "end_line": 267,
          "lines": 19,
          "preview": "            '        \"\"\"Execute the complete workflow\"\"\"',\n            \"        try:\",\n        ]\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_brain\\models\\canvas.py",
          "start_line": 301,
          "end_line": 307,
          "lines": 6,
          "preview": "        \"\"\"Generate Python code for a specific node\"\"\"\n        node_type = node.get('type', 'unknown')\n        node_name = node.get('name', 'Unnamed Node')\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_brain\\models\\canvas.py",
          "start_line": 316,
          "end_line": 318,
          "lines": 3,
          "preview": "\"\"\"\n        elif node_type == 'n8n-nodes-base.emailSend':\n            return f\"\"\"\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_brain\\models\\canvas.py",
          "start_line": 325,
          "end_line": 330,
          "lines": 5,
          "preview": "\"\"\"\n        else:\n            return f\"# Unknown node type: {node_type} ({node_name})\"\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_brain\\models\\canvas.py",
          "start_line": 745,
          "end_line": 773,
          "lines": 22,
          "preview": "        \"\"\"\n        _logger.info(f'\ud83d\udcc2 [Canvas Load] Loading canvas state for workflow {workflow_id}')\n        try:\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_brain\\models\\canvas.py",
          "start_line": 776,
          "end_line": 781,
          "lines": 5,
          "preview": "        \"\"\"\n        return self.write_sam_debug_log(log_data)\n    @api.model\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_brain\\models\\canvas_pan_move.py",
          "start_line": 30,
          "end_line": 36,
          "lines": 6,
          "preview": "        \"\"\"Override create to set last_saved timestamp\"\"\"\n        for vals in vals_list:\n            vals['last_saved'] = fields.Datetime.now()\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_brain\\models\\canvas_pan_move.py",
          "start_line": 41,
          "end_line": 62,
          "lines": 19,
          "preview": "        \"\"\"Save canvas viewport state\"\"\"\n        self.ensure_one()\n        update_vals = {}\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_brain\\models\\connections.py",
          "start_line": 6,
          "end_line": 9,
          "lines": 4,
          "preview": "    \"\"\"\n    Canvas Connections Model for Knowledge Visualizer V2\n    Stores node-to-node connections for workflow canvas\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_brain\\models\\documentation_manager.py",
          "start_line": 60,
          "end_line": 84,
          "lines": 21,
          "preview": "        \"\"\"Scan docs folder and update records\"\"\"\n        docs_path = self._get_docs_path()\n        if not docs_path.exists():\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_brain\\models\\documentation_manager.py",
          "start_line": 143,
          "end_line": 186,
          "lines": 33,
          "preview": "        \"\"\"Determine category from filename and path\"\"\"\n        filename_lower = filename.lower()\n        # Architecture & System Design\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_brain\\models\\documentation_manager.py",
          "start_line": 210,
          "end_line": 217,
          "lines": 7,
          "preview": "        \"\"\"Generate user-friendly title from filename\"\"\"\n        name = file_path.stem\n        # Convert underscores/hyphens to spaces and title case\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_brain\\models\\documentation_manager.py",
          "start_line": 248,
          "end_line": 254,
          "lines": 6,
          "preview": "        \"\"\"Get the full file path for the document\"\"\"\n        self.ensure_one()\n        docs_path = self._get_docs_path()\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_brain\\models\\executions.py",
          "start_line": 172,
          "end_line": 190,
          "lines": 15,
          "preview": "        \"\"\"Execute workflow nodes\"\"\"\n        # Create node lookup\n        node_lookup = {node['id']: node for node in nodes}\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_brain\\models\\executions.py",
          "start_line": 197,
          "end_line": 229,
          "lines": 26,
          "preview": "        \"\"\"Execute a chain of connected nodes\"\"\"\n        node_id = node['id']\n        # Skip if already executed\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_brain\\models\\executions.py",
          "start_line": 326,
          "end_line": 340,
          "lines": 11,
          "preview": "        \"\"\"Get nodes connected to the output of given node\"\"\"\n        connected_nodes = []\n        for connection in connections:\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_brain\\models\\n8n_dynamic_menus.py",
          "start_line": 15,
          "end_line": 62,
          "lines": 41,
          "preview": "        \"\"\"Remove all dynamically generated N8N menu items that polluted the main menu\"\"\"\n        _logger.info('\ud83e\uddf9 CLEANUP: Removing all dynamic N8N menu items from main Odoo menu...')\n        # Find all menu items with N8N node names or emojis\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_brain\\models\\n8n_node_category.py",
          "start_line": 35,
          "end_line": 35,
          "lines": 1,
          "preview": "# node_l2_ids = fields.Many2many('n8n.nodes.l2', 'n8n_l2_category_rel', 'category_id', 'node_l2_id', string='L2 Nodes')"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_brain\\models\\n8n_node_category.py",
          "start_line": 48,
          "end_line": 48,
          "lines": 1,
          "preview": "# def _compute_node_count(self):"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_brain\\models\\n8n_simple_extractor.py",
          "start_line": 2,
          "end_line": 9,
          "lines": 6,
          "preview": "\"\"\"\nN8N Node Extractor - Direct from Filesystem Using N8N's Logic\nThis extracts node data DIRECTLY from the N8N node files and applies\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_brain\\models\\n8n_simple_extractor.py",
          "start_line": 21,
          "end_line": 24,
          "lines": 4,
          "preview": "    \"\"\"\n    Wizard to extract N8N nodes directly from filesystem.\n    Uses N8N's actual logic for categorization.\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_brain\\models\\n8n_simple_extractor.py",
          "start_line": 40,
          "end_line": 48,
          "lines": 8,
          "preview": "        \"\"\"Load all data for display - suppliers, nodes, and overlay preview\"\"\"\n        for record in self:\n            record.supplier_ids = self.env['n8n.simple.supplier'].search([])\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_brain\\models\\n8n_simple_extractor.py",
          "start_line": 505,
          "end_line": 656,
          "lines": 126,
          "preview": "        \"\"\"Generate the new beautiful N8N Node Selection Overlay with REAL DATA\"\"\"\n        _logger.info('Computing new overlay with real N8N data...')\n        # Get node data from database\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_brain\\models\\n8n_simple_extractor.py",
          "start_line": 670,
          "end_line": 674,
          "lines": 4,
          "preview": "                '''\n            return cards_html\n        # Simplified version without script tags for Odoo sanitization\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_brain\\models\\n8n_simple_extractor.py",
          "start_line": 781,
          "end_line": 787,
          "lines": 5,
          "preview": "        '''\n        return html\n    @api.model\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_brain\\models\\n8n_simple_nodes.py",
          "start_line": 164,
          "end_line": 170,
          "lines": 6,
          "preview": "        \"\"\"Compute node type from is_trigger flag\"\"\"\n        for node in self:\n            node.node_type = 'Trigger' if node.is_trigger else 'Action'\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_brain\\models\\n8n_simple_nodes.py",
          "start_line": 200,
          "end_line": 246,
          "lines": 38,
          "preview": "        \"\"\"\n        # Step 1: Check if Core Nodes with explicit subcategory\n        if node.is_core_nodes and node.subcategories:\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_brain\\models\\n8n_simple_nodes.py",
          "start_line": 260,
          "end_line": 280,
          "lines": 17,
          "preview": "        \"\"\"Custom display name\"\"\"\n        result = []\n        for node in self:\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_brain\\models\\n8n_simple_nodes.py",
          "start_line": 320,
          "end_line": 325,
          "lines": 5,
          "preview": "        \"\"\"\n        Parse trigger operations from .node.js files.\n        For triggers, we return 1 card representing the trigger itself (not config options).\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_brain\\models\\nodes.py",
          "start_line": 83,
          "end_line": 96,
          "lines": 13,
          "preview": "        \"\"\"Validate connection JSON\"\"\"\n        for record in self:\n            for field_name in ['input_connections', 'output_connections']:\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_brain\\models\\nodes.py",
          "start_line": 106,
          "end_line": 111,
          "lines": 5,
          "preview": "        \"\"\"Set parameters from dictionary\"\"\"\n        self.ensure_one()\n        self.parameters = json.dumps(params_dict, indent=2)\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_brain\\models\\nodes.py",
          "start_line": 121,
          "end_line": 131,
          "lines": 10,
          "preview": "        \"\"\"Get output connections as list\"\"\"\n        self.ensure_one()\n        if self.output_connections:\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_brain\\models\\nodes.py",
          "start_line": 193,
          "end_line": 206,
          "lines": 13,
          "preview": "        \"\"\"Execute trigger node\"\"\"\n        if self.node_type == 'trigger_manual':\n            return {'status': 'success', 'data': input_data or {}}\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_brain\\models\\nodes.py",
          "start_line": 217,
          "end_line": 228,
          "lines": 11,
          "preview": "        \"\"\"Execute Odoo-specific node\"\"\"\n        if self.node_type == 'odoo_create_record':\n            return self._execute_odoo_create(params, input_data)\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_brain\\models\\nodes.py",
          "start_line": 239,
          "end_line": 248,
          "lines": 9,
          "preview": "        \"\"\"Execute data processing node\"\"\"\n        if self.node_type == 'data_transform':\n            return self._execute_data_transform(params, input_data)\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_brain\\models\\nodes.py",
          "start_line": 293,
          "end_line": 300,
          "lines": 6,
          "preview": "        \"\"\"Execute notification\"\"\"\n        message = params.get('message', 'Workflow notification')\n        self.env.user.notify_info(message)\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_brain\\models\\nodes.py",
          "start_line": 314,
          "end_line": 330,
          "lines": 14,
          "preview": "        \"\"\"Execute Odoo record update\"\"\"\n        model = params.get('model', '')\n        record_id = params.get('record_id', 0)\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_brain\\models\\res_config_settings.py",
          "start_line": 11,
          "end_line": 11,
          "lines": 1,
          "preview": "# knowledge_visualizer_enabled = fields.Boolean("
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_brain\\models\\res_config_settings.py",
          "start_line": 12,
          "end_line": 12,
          "lines": 1,
          "preview": "#     string='Enable AI Automator Features',"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_brain\\models\\res_config_settings.py",
          "start_line": 13,
          "end_line": 13,
          "lines": 1,
          "preview": "#     config_parameter='the_ai_automator.knowledge_visualizer_enabled',"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_brain\\models\\res_config_settings.py",
          "start_line": 14,
          "end_line": 14,
          "lines": 1,
          "preview": "#     help='Enable the AI Automator workflow and visualization features',"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_brain\\models\\res_config_settings.py",
          "start_line": 15,
          "end_line": 15,
          "lines": 1,
          "preview": "#     groups='base.group_no_one'  # Hide from main settings menu"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_brain\\models\\sam_brain_modes.py",
          "start_line": 451,
          "end_line": 501,
          "lines": 44,
          "preview": "        \"\"\"\n        message_lower = user_message.lower()\n        # Check for explicit brain requests\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_brain\\models\\sam_brain_modes.py",
          "start_line": 511,
          "end_line": 543,
          "lines": 28,
          "preview": "        \"\"\"\n        # Get user context\n        user_ctx = user_profile.get_user_context_for_sam()\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_brain\\models\\sam_chat_session.py",
          "start_line": 2,
          "end_line": 8,
          "lines": 6,
          "preview": "\"\"\"\nSAM AI Chat Session & Messages\n================================\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_brain\\models\\sam_knowledge_doc.py",
          "start_line": 269,
          "end_line": 282,
          "lines": 13,
          "preview": "        \"\"\"Compute file size and type from uploaded file\"\"\"\n        for record in self:\n            if record.file_data and record.file_name:\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_brain\\models\\sam_knowledge_doc.py",
          "start_line": 291,
          "end_line": 305,
          "lines": 13,
          "preview": "        \"\"\"Generate preview from content\"\"\"\n        for record in self:\n            if record.content:\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_brain\\models\\sam_mode_context.py",
          "start_line": 319,
          "end_line": 319,
          "lines": 1,
          "preview": "# server_url = self.env['ir.config_parameter'].sudo().get_param('sam.power_prompts_server')"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_brain\\models\\sam_personality.py",
          "start_line": 247,
          "end_line": 263,
          "lines": 15,
          "preview": "        prompt += f\"\"\"\nYOUR BOUNDARIES WITH {name}:\n- Personal topics: {'\u2705 Allowed' if user_ctx['boundaries']['can_discuss_personal'] else '\u274c Keep professional'}\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_brain\\models\\sam_personality.py",
          "start_line": 268,
          "end_line": 284,
          "lines": 12,
          "preview": "        \"\"\"Add SAM's context to the message before sending to AI\"\"\"\n        enriched = f\"{system_prompt}\\n\\n\"\n        # Add Odoo context if available\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_brain\\models\\sam_personality.py",
          "start_line": 293,
          "end_line": 310,
          "lines": 14,
          "preview": "        \"\"\"Extract what actions user is requesting\"\"\"\n        actions = []\n        message_lower = message.lower()\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_brain\\models\\sam_user_profile.py",
          "start_line": 242,
          "end_line": 257,
          "lines": 14,
          "preview": "        \"\"\"How SAM addresses the user\"\"\"\n        for record in self:\n            if record.preferred_name:\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_brain\\models\\sam_user_profile.py",
          "start_line": 390,
          "end_line": 426,
          "lines": 29,
          "preview": "        \"\"\"\n        self.ensure_one()\n        pending = []\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_brain\\models\\sam_user_profile.py",
          "start_line": 470,
          "end_line": 488,
          "lines": 16,
          "preview": "        \"\"\"Record an interaction and update trust score\"\"\"\n        self.interaction_count += 1\n        self.last_interaction = fields.Datetime.now()\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_brain\\models\\sam_user_profile.py",
          "start_line": 494,
          "end_line": 516,
          "lines": 18,
          "preview": "        \"\"\"\n        self.ensure_one()\n        approved = []\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_brain\\models\\sam_user_profile.py",
          "start_line": 524,
          "end_line": 545,
          "lines": 17,
          "preview": "        \"\"\"\n        self.ensure_one()\n        if not self.approved_file_paths:\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_brain\\models\\workflow_templates.py",
          "start_line": 80,
          "end_line": 106,
          "lines": 24,
          "preview": "        \"\"\"Validate template JSON structure\"\"\"\n        for record in self:\n            if record.json_definition:\n"
        }
      ]
    },
    "ai_sam": {
      "total_lines": 12466,
      "total_files": 44,
      "files_by_type": {
        ".py": 9,
        ".xml": 14,
        ".html": 1,
        ".js": 13,
        ".scss": 1,
        ".css": 6
      },
      "lines_by_type": {
        ".py": 2307,
        ".xml": 1558,
        ".html": 863,
        ".js": 4979,
        ".scss": 125,
        ".css": 2634
      },
      "commented_lines": 3908,
      "blank_lines": 1659,
      "code_lines": 6899,
      "commented_blocks": [
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_sam\\controllers\\canvas_controller.py",
          "start_line": 39,
          "end_line": 60,
          "lines": 18,
          "preview": "        \"\"\"Get platform configuration for dynamic loading\"\"\"\n        if not platform_id:\n            return {'error': 'platform_id is required'}\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_sam\\controllers\\canvas_controller.py",
          "start_line": 72,
          "end_line": 95,
          "lines": 19,
          "preview": "        \"\"\"Render canvas container with platform\"\"\"\n        canvas = request.env['canvas'].browse(int(canvas_id))\n        if not canvas.exists():\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_sam\\controllers\\canvas_controller.py",
          "start_line": 107,
          "end_line": 154,
          "lines": 40,
          "preview": "        \"\"\"Load nodes for a canvas based on its platform\"\"\"\n        import logging\n        _logger = logging.getLogger(__name__)\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_sam\\controllers\\sam_developer_mode.py",
          "start_line": 23,
          "end_line": 26,
          "lines": 3,
          "preview": "    \"\"\"Controller for SAM AI Developer Mode features.\"\"\"\n    def _get_tool_paths(self):\n        \"\"\"\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_sam\\controllers\\sam_orchestrator.py",
          "start_line": 167,
          "end_line": 188,
          "lines": 18,
          "preview": "        \"\"\"Get existing session or create new one\"\"\"\n        Session = request.env['sam.chat.session'].sudo()\n        if session_id:\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_sam\\controllers\\sam_session_controller.py",
          "start_line": 17,
          "end_line": 21,
          "lines": 4,
          "preview": "    \"\"\"Controller for SAM AI chat session management.\"\"\"\n    @http.route('/sam/session/get_history', type='json', auth='user')\n    def get_session_history(self, mode=None, limit=20, **kwargs):\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_sam\\static\\src\\components\\sam_ai_chat_interface.js",
          "start_line": 1236,
          "end_line": 1256,
          "lines": 19,
          "preview": "    /**\n     * Get relative time string (e.g., \"2 hours ago\", \"Yesterday\")\n     */\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_sam\\static\\src\\components\\sam_permission_handler.js",
          "start_line": 1,
          "end_line": 6,
          "lines": 4,
          "preview": "/** @odoo-module **/\nimport { Component, useState } from \"@odoo/owl\";\nimport { rpc } from \"@web/core/network/rpc\";\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_sam\\static\\src\\components\\sam_permission_handler.js",
          "start_line": 90,
          "end_line": 102,
          "lines": 12,
          "preview": "    /**\n     * Get icon for permission type\n     */\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_sam\\static\\src\\components\\sam_profile_settings.js",
          "start_line": 1,
          "end_line": 6,
          "lines": 4,
          "preview": "/** @odoo-module **/\nimport { Component, useState, onMounted } from \"@odoo/owl\";\nimport { rpc } from \"@web/core/network/rpc\";\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_sam\\static\\src\\js\\sam_ai_artifacts_manager.js",
          "start_line": 47,
          "end_line": 93,
          "lines": 38,
          "preview": "    /**\n     * Detect artifact type based on language and content\n     */\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_sam\\static\\src\\js\\sam_code_mode_button.js",
          "start_line": 1,
          "end_line": 6,
          "lines": 4,
          "preview": "/** @odoo-module **/\nimport { Component, useState, onWillStart } from \"@odoo/owl\";\nimport { useService } from \"@web/core/utils/hooks\";\n"
        }
      ]
    },
    "ai_sam_creatives": {
      "total_lines": 2458,
      "total_files": 17,
      "files_by_type": {
        ".sql": 1,
        ".py": 7,
        ".xml": 3,
        ".css": 1,
        ".js": 5
      },
      "lines_by_type": {
        ".sql": 12,
        ".py": 287,
        ".xml": 313,
        ".css": 737,
        ".js": 1109
      },
      "commented_lines": 1027,
      "blank_lines": 311,
      "code_lines": 1120,
      "commented_blocks": [
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_sam_creatives\\controllers\\creatives_controller.py",
          "start_line": 11,
          "end_line": 14,
          "lines": 3,
          "preview": "    \"\"\"\n    Creatives Platform Controller\n    Handles all /creatives/* routes for the SAM Creative platform.\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_sam_creatives\\models\\creatives_landing_card.py",
          "start_line": 2,
          "end_line": 9,
          "lines": 6,
          "preview": "\"\"\"\nPlaceholder file for ai_sam_creatives module.\nThe actual creatives.landing.card model is defined in ai_brain module\n"
        }
      ]
    },
    "ai_sam_docs": {
      "total_lines": 8113,
      "total_files": 21,
      "files_by_type": {
        ".py": 5,
        ".json": 1,
        ".html": 8,
        ".sql": 3,
        ".xml": 4
      },
      "lines_by_type": {
        ".py": 375,
        ".json": 178,
        ".html": 5789,
        ".sql": 1260,
        ".xml": 511
      },
      "commented_lines": 160,
      "blank_lines": 974,
      "code_lines": 6979,
      "commented_blocks": [
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_sam_docs\\controllers\\documentation_controller.py",
          "start_line": 68,
          "end_line": 107,
          "lines": 35,
          "preview": "        \"\"\"Open file directly in browser\"\"\"\n        try:\n            doc = request.env['ai.automator.documentation'].browse(doc_id)\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_sam_docs\\controllers\\documentation_controller.py",
          "start_line": 139,
          "end_line": 145,
          "lines": 6,
          "preview": "        \"\"\"Get full path to documentation file\"\"\"\n        from odoo.modules.module import get_module_path\n        module_path = Path(get_module_path('the_ai_automator'))\n"
        }
      ]
    },
    "ai_sam_intelligence": {
      "total_lines": 1312,
      "total_files": 11,
      "files_by_type": {
        ".py": 6,
        ".xml": 5
      },
      "lines_by_type": {
        ".py": 1003,
        ".xml": 309
      },
      "commented_lines": 428,
      "blank_lines": 190,
      "code_lines": 694,
      "commented_blocks": [
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_sam_intelligence\\models\\ai_agent_knowledge.py",
          "start_line": 44,
          "end_line": 53,
          "lines": 9,
          "preview": "        \"\"\"Show first 500 characters as preview\"\"\"\n        for record in self:\n            if record.content:\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_sam_intelligence\\models\\ai_agent_knowledge.py",
          "start_line": 62,
          "end_line": 70,
          "lines": 8,
          "preview": "        \"\"\"Compute MD5 hash for change detection\"\"\"\n        for record in self:\n            if record.content:\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_sam_intelligence\\models\\ai_agent_registry.py",
          "start_line": 93,
          "end_line": 102,
          "lines": 9,
          "preview": "        \"\"\"Build rich system prompt from agent knowledge for SAM chat\"\"\"\n        for agent in self:\n            # Build knowledge summary\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_sam_intelligence\\models\\ai_agent_registry.py",
          "start_line": 120,
          "end_line": 124,
          "lines": 4,
          "preview": "\"\"\"\n    @api.depends('archetype', 'category')\n    def _compute_capabilities(self):\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_sam_intelligence\\models\\ai_agent_registry.py",
          "start_line": 208,
          "end_line": 225,
          "lines": 15,
          "preview": "        \"\"\"Determine agent archetype from name and config\"\"\"\n        name_lower = agent_name.lower()\n        if any(x in name_lower for x in ['architect', 'cto', 'cmo', 'cfo', 'cos']):\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_sam_intelligence\\models\\ai_agent_registry.py",
          "start_line": 234,
          "end_line": 255,
          "lines": 18,
          "preview": "        \"\"\"Determine slash command from agent name\"\"\"\n        # Map known agents to their slash commands\n        command_map = {\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_sam_intelligence\\models\\ai_agent_registry.py",
          "start_line": 265,
          "end_line": 309,
          "lines": 36,
          "preview": "        \"\"\"\n        self.ensure_one()\n        if not self.knowledge_file_ids:\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_sam_intelligence\\models\\documentation_intelligence.py",
          "start_line": 68,
          "end_line": 76,
          "lines": 8,
          "preview": "        \"\"\"Get SAM AI base path\"\"\"\n        # Traverse up from this module to ai_sam_odoo directory\n        current_file = os.path.abspath(__file__)\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_sam_intelligence\\models\\documentation_intelligence.py",
          "start_line": 79,
          "end_line": 105,
          "lines": 22,
          "preview": "        \"\"\"\n        base_path = self._get_base_path()\n        modules = []\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_sam_intelligence\\models\\documentation_intelligence.py",
          "start_line": 138,
          "end_line": 140,
          "lines": 3,
          "preview": "        Scan models/*.py for Odoo model definitions (_name = 'model.name')\n        Returns list of model names\n        \"\"\"\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_sam_intelligence\\models\\documentation_intelligence.py",
          "start_line": 284,
          "end_line": 294,
          "lines": 10,
          "preview": "        \"\"\"Load previous state from JSON file\"\"\"\n        if os.path.exists(self.state_file_path):\n            try:\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_sam_intelligence\\models\\documentation_intelligence.py",
          "start_line": 459,
          "end_line": 464,
          "lines": 4,
          "preview": "        \"\"\")\n        return analysis\n    def action_view_report(self):\n"
        }
      ]
    },
    "ai_sam_members": {
      "total_lines": 950,
      "total_files": 15,
      "files_by_type": {
        ".py": 7,
        ".xml": 7,
        ".css": 1
      },
      "lines_by_type": {
        ".py": 355,
        ".xml": 543,
        ".css": 52
      },
      "commented_lines": 94,
      "blank_lines": 87,
      "code_lines": 769,
      "commented_blocks": [
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_sam_members\\controllers\\portal.py",
          "start_line": 123,
          "end_line": 140,
          "lines": 15,
          "preview": "        \"\"\"SAM AI Chat Portal (paid members only)\"\"\"\n        user = request.env.user\n        # Check if user is paid member\n"
        }
      ]
    },
    "ai_sam_memory": {
      "total_lines": 3719,
      "total_files": 24,
      "files_by_type": {
        ".py": 12,
        ".xml": 9,
        ".js": 3
      },
      "lines_by_type": {
        ".py": 2678,
        ".xml": 855,
        ".js": 186
      },
      "commented_lines": 1521,
      "blank_lines": 500,
      "code_lines": 1698,
      "commented_blocks": [
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_sam_memory\\controllers\\memory_graph_controller.py",
          "start_line": 16,
          "end_line": 19,
          "lines": 4,
          "preview": "        \"\"\"\n        Get graph visualization data from ai.conversation\n        Returns nodes and edges for vis.js rendering\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_sam_memory\\uncertain_files\\models_moved_to_ai_brain\\models\\ai_conversation_import.py",
          "start_line": 153,
          "end_line": 165,
          "lines": 12,
          "preview": "        \"\"\"Auto-detect if path is file or directory\"\"\"\n        for record in self:\n            if record.source_path and os.path.exists(record.source_path):\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_sam_memory\\uncertain_files\\models_moved_to_ai_brain\\models\\ai_conversation_import.py",
          "start_line": 639,
          "end_line": 651,
          "lines": 11,
          "preview": "        \"\"\"Create ai.conversation record\"\"\"\n        # Claude export uses 'name', fallback to 'title' for other formats\n        conv_name = conv_data.get('name') or conv_data.get('title') or 'Untitled Conversation'\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_sam_memory\\uncertain_files\\models_moved_to_ai_brain\\models\\ai_document_extractor.py",
          "start_line": 36,
          "end_line": 50,
          "lines": 11,
          "preview": "        \"\"\"Register built-in extractors on first use\"\"\"\n        if AIDocumentExtractor._initialized:\n            return\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_sam_memory\\uncertain_files\\models_moved_to_ai_brain\\models\\ai_document_extractor.py",
          "start_line": 96,
          "end_line": 102,
          "lines": 6,
          "preview": "        \"\"\"\n        cls._extractors[extension.lower()] = handler\n        _logger.debug(f\"Registered extractor for {extension}\")\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_sam_memory\\uncertain_files\\models_moved_to_ai_brain\\models\\ai_document_extractor.py",
          "start_line": 220,
          "end_line": 227,
          "lines": 7,
          "preview": "        \"\"\"Extract JSON files\"\"\"\n        with open(file_path, 'r', encoding='utf-8') as f:\n            data = json.load(f)\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_sam_memory\\uncertain_files\\models_moved_to_ai_brain\\models\\ai_document_extractor.py",
          "start_line": 237,
          "end_line": 251,
          "lines": 14,
          "preview": "        \"\"\"Extract PDF files\"\"\"\n        try:\n            import PyPDF2\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_sam_memory\\uncertain_files\\models_moved_to_ai_brain\\models\\ai_document_extractor.py",
          "start_line": 261,
          "end_line": 278,
          "lines": 17,
          "preview": "        \"\"\"Extract Excel files\"\"\"\n        try:\n            import openpyxl\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_sam_memory\\uncertain_files\\models_moved_to_ai_brain\\models\\ai_document_extractor.py",
          "start_line": 396,
          "end_line": 397,
          "lines": 2,
          "preview": "        \"\"\"\n        prompt = f\"\"\"Generate a Python function to extract content from {extension} files.\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_sam_memory\\uncertain_files\\models_moved_to_ai_brain\\models\\ai_document_extractor.py",
          "start_line": 411,
          "end_line": 428,
          "lines": 13,
          "preview": "\"\"\"\n        conversation = self.env['ai.conversation'].create({\n            'name': f'Extractor Generation: {extension}'\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_sam_memory\\uncertain_files\\models_moved_to_ai_brain\\models\\ai_graph_service.py",
          "start_line": 242,
          "end_line": 246,
          "lines": 4,
          "preview": "        \"\"\"\n        Get the graph structure for a conversation (nodes + relationships)\n        Returns visualization data for the conversation and its connections\n"
        }
      ]
    },
    "ai_sam_messenger": {
      "total_lines": 158,
      "total_files": 4,
      "files_by_type": {
        ".py": 2,
        ".css": 1,
        ".js": 1
      },
      "lines_by_type": {
        ".py": 38,
        ".css": 56,
        ".js": 64
      },
      "commented_lines": 29,
      "blank_lines": 22,
      "code_lines": 107,
      "commented_blocks": [
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_sam_messenger\\static\\src\\js\\messenger_toggle.js",
          "start_line": 1,
          "end_line": 7,
          "lines": 5,
          "preview": "/** @odoo-module **/\nimport { patch } from \"@web/core/utils/patch\";\nimport { FormController } from \"@web/views/form/form_controller\";\n"
        }
      ]
    },
    "ai_sam_socializer": {
      "total_lines": 607,
      "total_files": 9,
      "files_by_type": {
        ".py": 4,
        ".css": 1,
        ".js": 2,
        ".xml": 2
      },
      "lines_by_type": {
        ".py": 238,
        ".css": 72,
        ".js": 34,
        ".xml": 263
      },
      "commented_lines": 132,
      "blank_lines": 67,
      "code_lines": 408,
      "commented_blocks": []
    },
    "ai_sam_ui": {
      "total_lines": 733,
      "total_files": 8,
      "files_by_type": {
        ".py": 3,
        ".html": 1,
        ".js": 1,
        ".scss": 1,
        ".xml": 2
      },
      "lines_by_type": {
        ".py": 57,
        ".html": 91,
        ".js": 230,
        ".scss": 274,
        ".xml": 81
      },
      "commented_lines": 147,
      "blank_lines": 92,
      "code_lines": 494,
      "commented_blocks": [
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_sam_ui\\static\\src\\snippets\\s_sam_chat\\000.js",
          "start_line": 1,
          "end_line": 6,
          "lines": 4,
          "preview": "/** @odoo-module **/\nimport publicWidget from \"@web/legacy/js/public/public_widget\";\nimport { rpc } from \"@web/core/network/rpc\";\n"
        }
      ]
    },
    "ai_sam_workflows": {
      "total_lines": 661073,
      "total_files": 4018,
      "files_by_type": {
        ".py": 8,
        ".xml": 27,
        ".css": 4,
        ".html": 1,
        ".js": 2646,
        ".scss": 1,
        ".json": 1331
      },
      "lines_by_type": {
        ".py": 2037,
        ".xml": 4680,
        ".css": 2091,
        ".html": 3425,
        ".js": 560880,
        ".scss": 911,
        ".json": 87049
      },
      "commented_lines": 138016,
      "blank_lines": 3104,
      "code_lines": 519953,
      "commented_blocks": [
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_sam_workflows\\controllers\\branch_api.py",
          "start_line": 22,
          "end_line": 26,
          "lines": 4,
          "preview": "    \"\"\"API endpoints for branch/canvas type selection\"\"\"\n    @http.route('/canvas/api/branches/available', type='http', auth='user', methods=['GET'])\n    def get_available_branches(self, **kwargs):\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_sam_workflows\\controllers\\documentation_controller.py",
          "start_line": 68,
          "end_line": 107,
          "lines": 35,
          "preview": "        \"\"\"Open file directly in browser\"\"\"\n        try:\n            doc = request.env['ai.automator.documentation'].browse(doc_id)\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_sam_workflows\\controllers\\documentation_controller.py",
          "start_line": 139,
          "end_line": 145,
          "lines": 6,
          "preview": "        \"\"\"Get full path to documentation file\"\"\"\n        from odoo.modules.module import get_module_path\n        module_path = Path(get_module_path('the_ai_automator'))\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_sam_workflows\\controllers\\transition_control.py",
          "start_line": 172,
          "end_line": 175,
          "lines": 4,
          "preview": "        \"\"\"\n        Save/update canvas connections for a workflow\n        JSON API endpoint for AJAX calls\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_sam_workflows\\controllers\\transition_control.py",
          "start_line": 216,
          "end_line": 219,
          "lines": 4,
          "preview": "        \"\"\"\n        Load canvas connections for a workflow\n        JSON API endpoint for AJAX calls\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_sam_workflows\\controllers\\transition_control.py",
          "start_line": 348,
          "end_line": 351,
          "lines": 4,
          "preview": "        \"\"\"\n        Get available Odoo apps for canvas menu dropdown\n        Returns simplified menu data for Service Bridge\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_sam_workflows\\controllers\\transition_control.py",
          "start_line": 422,
          "end_line": 425,
          "lines": 4,
          "preview": "        \"\"\"\n        Get N8N nodes from n8n.simple.node model grouped by UI placement\n        HTTP API endpoint for the node selector overlay - Uses new simplified model\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_sam_workflows\\controllers\\transition_control.py",
          "start_line": 570,
          "end_line": 573,
          "lines": 4,
          "preview": "        \"\"\"\n        Get operations for a specific n8n.simple.node\n        Returns triggers/actions parsed from Description.js files on-demand\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_sam_workflows\\controllers\\transition_control.py",
          "start_line": 788,
          "end_line": 792,
          "lines": 5,
          "preview": "        \"\"\"\n        \ud83c\udfaf JSON Node Structure API - Get triggers and actions for nodes with has_node_json=True\n        Called when user clicks a parent node that has actual .node.json files\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_sam_workflows\\controllers\\transition_control.py",
          "start_line": 1012,
          "end_line": 1015,
          "lines": 4,
          "preview": "        \"\"\"\n        \ud83d\udcc4 Get metadata for a single N8N node\n        Used for detailed node information on-demand\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_sam_workflows\\controllers\\transition_control.py",
          "start_line": 1062,
          "end_line": 1066,
          "lines": 5,
          "preview": "        \"\"\"\n        \ud83d\udcc1 Get L1 children for hierarchical nodes like Google, Microsoft\n        Called when user clicks a parent node that has sub-folders (has_node_json=False)\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_sam_workflows\\static\\src\\automator\\n8n\\lines\\connection_system.js",
          "start_line": 713,
          "end_line": 727,
          "lines": 14,
          "preview": "    /**\n     * Find node by name (for loading connections from database)\n     */\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_sam_workflows\\static\\src\\automator\\n8n\\n8n_nodes\\FunctionItem\\FunctionItem.node.js",
          "start_line": 84,
          "end_line": 91,
          "lines": 8,
          "preview": "                    /** @deprecated for removal - replaced by getBinaryDataAsync() */\n                    getBinaryData: () => {\n                        if (mode === 'manual') {\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_sam_workflows\\static\\src\\automator\\n8n\\n8n_nodes\\Google\\Sheet\\v1\\GoogleSheet.js",
          "start_line": 111,
          "end_line": 133,
          "lines": 23,
          "preview": "    /**\n     * Returns the given sheet data in a structured way\n     */\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_sam_workflows\\static\\src\\automator\\n8n\\n8n_nodes\\Onfleet\\Onfleet.js",
          "start_line": 62,
          "end_line": 63,
          "lines": 2,
          "preview": "            /* -------------------------------------------------------------------------- */\n            /*               Get fields for create and update a destination               */\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_sam_workflows\\static\\src\\automator\\n8n\\n8n_nodes\\Onfleet\\Onfleet.js",
          "start_line": 106,
          "end_line": 107,
          "lines": 2,
          "preview": "            /* -------------------------------------------------------------------------- */\n            /*                         Get fields for create admin                        */\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_sam_workflows\\static\\src\\automator\\n8n\\n8n_nodes\\Onfleet\\Onfleet.js",
          "start_line": 119,
          "end_line": 120,
          "lines": 2,
          "preview": "            /*                         Get fields for update admin                        */\n            /* -------------------------------------------------------------------------- */\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_sam_workflows\\static\\src\\automator\\n8n\\n8n_nodes\\Onfleet\\Onfleet.js",
          "start_line": 140,
          "end_line": 141,
          "lines": 2,
          "preview": "            /*                          Get fields for create hub                         */\n            /* -------------------------------------------------------------------------- */\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_sam_workflows\\static\\src\\automator\\n8n\\n8n_nodes\\Onfleet\\Onfleet.js",
          "start_line": 151,
          "end_line": 152,
          "lines": 2,
          "preview": "            /* -------------------------------------------------------------------------- */\n            /*                          Get fields for update hub                         */\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_sam_workflows\\static\\src\\automator\\n8n\\n8n_nodes\\Onfleet\\Onfleet.js",
          "start_line": 175,
          "end_line": 176,
          "lines": 2,
          "preview": "            /* -------------------------------------------------------------------------- */\n            /*                        Get fields for create worker                        */\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_sam_workflows\\static\\src\\automator\\n8n\\n8n_nodes\\Onfleet\\Onfleet.js",
          "start_line": 194,
          "end_line": 195,
          "lines": 2,
          "preview": "            /*                        Get fields for update worker                        */\n            /* -------------------------------------------------------------------------- */\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_sam_workflows\\static\\src\\automator\\n8n\\n8n_nodes\\Onfleet\\Onfleet.js",
          "start_line": 218,
          "end_line": 219,
          "lines": 2,
          "preview": "            /* -------------------------------------------------------------------------- */\n            /*                    Get fields for get and getAll workers                   */\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_sam_workflows\\static\\src\\automator\\n8n\\n8n_nodes\\Onfleet\\Onfleet.js",
          "start_line": 269,
          "end_line": 270,
          "lines": 2,
          "preview": "            /*                        Get fields for create webhook                       */\n            /* -------------------------------------------------------------------------- */\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_sam_workflows\\static\\src\\automator\\n8n\\n8n_nodes\\Onfleet\\Onfleet.js",
          "start_line": 376,
          "end_line": 391,
          "lines": 16,
          "preview": "            /* -------------------------------------------------------------------------- */\n            const updateFields = this.getNodeParameter('updateFields', item);\n            const taskData = {};\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_sam_workflows\\static\\src\\automator\\n8n\\n8n_nodes\\Onfleet\\Onfleet.js",
          "start_line": 426,
          "end_line": 450,
          "lines": 25,
          "preview": "            /* -------------------------------------------------------------------------- */\n            const filters = this.getNodeParameter('filters', item);\n            const listTaskData = {};\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_sam_workflows\\static\\src\\automator\\n8n\\n8n_nodes\\Onfleet\\Onfleet.js",
          "start_line": 497,
          "end_line": 498,
          "lines": 2,
          "preview": "            /*      Get driver time estimates for tasks that haven't been created yet     */\n            /* -------------------------------------------------------------------------- */\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_sam_workflows\\static\\src\\automator\\n8n\\n8n_nodes\\Onfleet\\Onfleet.js",
          "start_line": 1181,
          "end_line": 1182,
          "lines": 2,
          "preview": "                    /* -------------------------------------------------------------------------- */\n                    /*      Get driver time estimates for tasks that haven't been created yet     */\n"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\ai_sam_workflows\\static\\src\\automator\\n8n\\n8n_nodes\\Redis\\utils.js",
          "start_line": 40,
          "end_line": 51,
          "lines": 12,
          "preview": "/** Parses the given value in a number if it is one else returns a string */\nfunction getParsedValue(value) {\n    if (value.match(/^[\\d\\.]+$/) === null) {\n"
        }
      ]
    },
    "github_app": {
      "total_lines": 562,
      "total_files": 12,
      "files_by_type": {
        ".py": 7,
        ".xml": 4,
        ".html": 1
      },
      "lines_by_type": {
        ".py": 247,
        ".xml": 157,
        ".html": 158
      },
      "commented_lines": 64,
      "blank_lines": 65,
      "code_lines": 433,
      "commented_blocks": [
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\github_app\\models\\github_view_app.py",
          "start_line": 5,
          "end_line": 5,
          "lines": 1,
          "preview": "# from github import Github"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\github_app\\models\\github_view_app.py",
          "start_line": 50,
          "end_line": 50,
          "lines": 1,
          "preview": "# print(repo.remotes.origin.pull())"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\github_app\\models\\github_view_app.py",
          "start_line": 52,
          "end_line": 52,
          "lines": 1,
          "preview": "# print(repo.remotes.origin.push())"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\github_app\\models\\github_view_settings.py",
          "start_line": 103,
          "end_line": 103,
          "lines": 1,
          "preview": "# print(repo.remotes.origin.pull())"
        },
        {
          "file": "C:\\Working With AI\\ai_sam\\ai_sam\\github_app\\models\\github_view_settings.py",
          "start_line": 105,
          "end_line": 105,
          "lines": 1,
          "preview": "# print(repo.remotes.origin.push())"
        }
      ]
    },
    "_SUMMARY": {
      "total_modules": 12,
      "total_lines": 708991,
      "total_files": 4246
    }
  },
  "agents": {
    "canvas-core-guardian": {
      "total_words": 9968,
      "total_files": 6,
      "files": [
        {
          "name": "agent_protocol.md",
          "words": 1797,
          "is_shared": false
        },
        {
          "name": "canvas_core_rules.md",
          "words": 1610,
          "is_shared": false
        },
        {
          "name": "forbidden_patterns.md",
          "words": 1720,
          "is_shared": false
        },
        {
          "name": "naming_standards.md",
          "words": 1641,
          "is_shared": false
        },
        {
          "name": "QUICKSTART.md",
          "words": 1496,
          "is_shared": false
        },
        {
          "name": "README.md",
          "words": 1704,
          "is_shared": true
        }
      ],
      "shared_files": [
        {
          "name": "README.md",
          "words": 1704,
          "is_shared": true
        }
      ],
      "unique_files": [
        {
          "name": "agent_protocol.md",
          "words": 1797,
          "is_shared": false
        },
        {
          "name": "canvas_core_rules.md",
          "words": 1610,
          "is_shared": false
        },
        {
          "name": "forbidden_patterns.md",
          "words": 1720,
          "is_shared": false
        },
        {
          "name": "naming_standards.md",
          "words": 1641,
          "is_shared": false
        },
        {
          "name": "QUICKSTART.md",
          "words": 1496,
          "is_shared": false
        }
      ]
    },
    "cmo": {
      "total_words": 8943,
      "total_files": 5,
      "files": [
        {
          "name": "cmo_protocol.md",
          "words": 2348,
          "is_shared": false
        },
        {
          "name": "direct_response_mastery.md",
          "words": 1858,
          "is_shared": false
        },
        {
          "name": "marketing_strategy_frameworks.md",
          "words": 2076,
          "is_shared": false
        },
        {
          "name": "market_positioning_methodology.md",
          "words": 1939,
          "is_shared": false
        },
        {
          "name": "sam_ai_product_context.md",
          "words": 722,
          "is_shared": false
        }
      ],
      "shared_files": [],
      "unique_files": [
        {
          "name": "cmo_protocol.md",
          "words": 2348,
          "is_shared": false
        },
        {
          "name": "direct_response_mastery.md",
          "words": 1858,
          "is_shared": false
        },
        {
          "name": "marketing_strategy_frameworks.md",
          "words": 2076,
          "is_shared": false
        },
        {
          "name": "market_positioning_methodology.md",
          "words": 1939,
          "is_shared": false
        },
        {
          "name": "sam_ai_product_context.md",
          "words": 722,
          "is_shared": false
        }
      ]
    },
    "cto": {
      "total_words": 12823,
      "total_files": 5,
      "files": [
        {
          "name": "cost_management.md",
          "words": 2843,
          "is_shared": false
        },
        {
          "name": "cto_protocol.md",
          "words": 2608,
          "is_shared": false
        },
        {
          "name": "infrastructure_strategy.md",
          "words": 2091,
          "is_shared": false
        },
        {
          "name": "performance_optimization_playbook.md",
          "words": 2487,
          "is_shared": false
        },
        {
          "name": "scaling_roadmap.md",
          "words": 2794,
          "is_shared": false
        }
      ],
      "shared_files": [],
      "unique_files": [
        {
          "name": "cost_management.md",
          "words": 2843,
          "is_shared": false
        },
        {
          "name": "cto_protocol.md",
          "words": 2608,
          "is_shared": false
        },
        {
          "name": "infrastructure_strategy.md",
          "words": 2091,
          "is_shared": false
        },
        {
          "name": "performance_optimization_playbook.md",
          "words": 2487,
          "is_shared": false
        },
        {
          "name": "scaling_roadmap.md",
          "words": 2794,
          "is_shared": false
        }
      ]
    },
    "documentation-master": {
      "total_words": 5337,
      "total_files": 5,
      "files": [
        {
          "name": "boardroom_context_protocol.md",
          "words": 987,
          "is_shared": false
        },
        {
          "name": "current_state_rules.md",
          "words": 983,
          "is_shared": false
        },
        {
          "name": "docs_agent_workflow.md",
          "words": 1362,
          "is_shared": false
        },
        {
          "name": "documentation_intelligence.md",
          "words": 1215,
          "is_shared": false
        },
        {
          "name": "misalignment_detection.md",
          "words": 790,
          "is_shared": false
        }
      ],
      "shared_files": [],
      "unique_files": [
        {
          "name": "boardroom_context_protocol.md",
          "words": 987,
          "is_shared": false
        },
        {
          "name": "current_state_rules.md",
          "words": 983,
          "is_shared": false
        },
        {
          "name": "docs_agent_workflow.md",
          "words": 1362,
          "is_shared": false
        },
        {
          "name": "documentation_intelligence.md",
          "words": 1215,
          "is_shared": false
        },
        {
          "name": "misalignment_detection.md",
          "words": 790,
          "is_shared": false
        }
      ]
    },
    "github": {
      "total_words": 3404,
      "total_files": 5,
      "files": [
        {
          "name": "commit_message_template.md",
          "words": 666,
          "is_shared": false
        },
        {
          "name": "github_config.md",
          "words": 269,
          "is_shared": false
        },
        {
          "name": "github_expertise.md",
          "words": 1178,
          "is_shared": false
        },
        {
          "name": "pre_push_checklist.md",
          "words": 773,
          "is_shared": false
        },
        {
          "name": "workflow_patterns.md",
          "words": 518,
          "is_shared": false
        }
      ],
      "shared_files": [],
      "unique_files": [
        {
          "name": "commit_message_template.md",
          "words": 666,
          "is_shared": false
        },
        {
          "name": "github_config.md",
          "words": 269,
          "is_shared": false
        },
        {
          "name": "github_expertise.md",
          "words": 1178,
          "is_shared": false
        },
        {
          "name": "pre_push_checklist.md",
          "words": 773,
          "is_shared": false
        },
        {
          "name": "workflow_patterns.md",
          "words": 518,
          "is_shared": false
        }
      ]
    },
    "odoo-architect": {
      "total_words": 4873,
      "total_files": 4,
      "files": [
        {
          "name": "brainstorming_framework.md",
          "words": 1388,
          "is_shared": false
        },
        {
          "name": "odoo_patterns.md",
          "words": 918,
          "is_shared": false
        },
        {
          "name": "planning_methodology.md",
          "words": 1359,
          "is_shared": false
        },
        {
          "name": "prompt_writing_guide.md",
          "words": 1208,
          "is_shared": false
        }
      ],
      "shared_files": [],
      "unique_files": [
        {
          "name": "brainstorming_framework.md",
          "words": 1388,
          "is_shared": false
        },
        {
          "name": "odoo_patterns.md",
          "words": 918,
          "is_shared": false
        },
        {
          "name": "planning_methodology.md",
          "words": 1359,
          "is_shared": false
        },
        {
          "name": "prompt_writing_guide.md",
          "words": 1208,
          "is_shared": false
        }
      ]
    },
    "odoo-audit": {
      "total_words": 1978,
      "total_files": 4,
      "files": [
        {
          "name": "common_mistakes.md",
          "words": 553,
          "is_shared": false
        },
        {
          "name": "quality_standards.md",
          "words": 450,
          "is_shared": false
        },
        {
          "name": "scoring_rubric.md",
          "words": 364,
          "is_shared": false
        },
        {
          "name": "session_optimization.md",
          "words": 611,
          "is_shared": false
        }
      ],
      "shared_files": [],
      "unique_files": [
        {
          "name": "common_mistakes.md",
          "words": 553,
          "is_shared": false
        },
        {
          "name": "quality_standards.md",
          "words": 450,
          "is_shared": false
        },
        {
          "name": "scoring_rubric.md",
          "words": 364,
          "is_shared": false
        },
        {
          "name": "session_optimization.md",
          "words": 611,
          "is_shared": false
        }
      ]
    },
    "odoo-debugger": {
      "total_words": 11252,
      "total_files": 5,
      "files": [
        {
          "name": "architecture_compliance.md",
          "words": 1942,
          "is_shared": false
        },
        {
          "name": "bug_history_protocol.md",
          "words": 1798,
          "is_shared": false
        },
        {
          "name": "debug_protocol.md",
          "words": 3507,
          "is_shared": false
        },
        {
          "name": "odoo_error_patterns.md",
          "words": 1955,
          "is_shared": false
        },
        {
          "name": "qa_tool_guardian.md",
          "words": 2050,
          "is_shared": false
        }
      ],
      "shared_files": [],
      "unique_files": [
        {
          "name": "architecture_compliance.md",
          "words": 1942,
          "is_shared": false
        },
        {
          "name": "bug_history_protocol.md",
          "words": 1798,
          "is_shared": false
        },
        {
          "name": "debug_protocol.md",
          "words": 3507,
          "is_shared": false
        },
        {
          "name": "odoo_error_patterns.md",
          "words": 1955,
          "is_shared": false
        },
        {
          "name": "qa_tool_guardian.md",
          "words": 2050,
          "is_shared": false
        }
      ]
    },
    "odoo-developer": {
      "total_words": 7006,
      "total_files": 5,
      "files": [
        {
          "name": "architecture_mastery.md",
          "words": 1154,
          "is_shared": false
        },
        {
          "name": "development_standards.md",
          "words": 1526,
          "is_shared": false
        },
        {
          "name": "file_management.md",
          "words": 1238,
          "is_shared": false
        },
        {
          "name": "odoo_18_error_prevention.md",
          "words": 2055,
          "is_shared": false
        },
        {
          "name": "qa_integration.md",
          "words": 1033,
          "is_shared": false
        }
      ],
      "shared_files": [],
      "unique_files": [
        {
          "name": "architecture_mastery.md",
          "words": 1154,
          "is_shared": false
        },
        {
          "name": "development_standards.md",
          "words": 1526,
          "is_shared": false
        },
        {
          "name": "file_management.md",
          "words": 1238,
          "is_shared": false
        },
        {
          "name": "odoo_18_error_prevention.md",
          "words": 2055,
          "is_shared": false
        },
        {
          "name": "qa_integration.md",
          "words": 1033,
          "is_shared": false
        }
      ]
    },
    "odoo-qa-guardian": {
      "total_words": 8042,
      "total_files": 5,
      "files": [
        {
          "name": "auto_fix_patterns.md",
          "words": 1607,
          "is_shared": false
        },
        {
          "name": "detection_commands.md",
          "words": 1606,
          "is_shared": false
        },
        {
          "name": "education_framework.md",
          "words": 1697,
          "is_shared": false
        },
        {
          "name": "qa_guardian_protocol.md",
          "words": 1580,
          "is_shared": false
        },
        {
          "name": "scoring_rubric.md",
          "words": 1552,
          "is_shared": false
        }
      ],
      "shared_files": [],
      "unique_files": [
        {
          "name": "auto_fix_patterns.md",
          "words": 1607,
          "is_shared": false
        },
        {
          "name": "detection_commands.md",
          "words": 1606,
          "is_shared": false
        },
        {
          "name": "education_framework.md",
          "words": 1697,
          "is_shared": false
        },
        {
          "name": "qa_guardian_protocol.md",
          "words": 1580,
          "is_shared": false
        },
        {
          "name": "scoring_rubric.md",
          "words": 1552,
          "is_shared": false
        }
      ]
    },
    "recruiter": {
      "total_words": 13612,
      "total_files": 6,
      "files": [
        {
          "name": "agent_creation_workflow.md",
          "words": 2260,
          "is_shared": false
        },
        {
          "name": "agent_design_patterns.md",
          "words": 1977,
          "is_shared": false
        },
        {
          "name": "existing_agents_analysis.md",
          "words": 2323,
          "is_shared": false
        },
        {
          "name": "knowledge_extraction.md",
          "words": 1773,
          "is_shared": false
        },
        {
          "name": "session_memory.md",
          "words": 3711,
          "is_shared": false
        },
        {
          "name": "session_memory_protocol.md",
          "words": 1568,
          "is_shared": false
        }
      ],
      "shared_files": [],
      "unique_files": [
        {
          "name": "agent_creation_workflow.md",
          "words": 2260,
          "is_shared": false
        },
        {
          "name": "agent_design_patterns.md",
          "words": 1977,
          "is_shared": false
        },
        {
          "name": "existing_agents_analysis.md",
          "words": 2323,
          "is_shared": false
        },
        {
          "name": "knowledge_extraction.md",
          "words": 1773,
          "is_shared": false
        },
        {
          "name": "session_memory.md",
          "words": 3711,
          "is_shared": false
        },
        {
          "name": "session_memory_protocol.md",
          "words": 1568,
          "is_shared": false
        }
      ]
    },
    "sam": {
      "total_words": 17341,
      "total_files": 7,
      "files": [
        {
          "name": "controller_architecture.md",
          "words": 1773,
          "is_shared": false
        },
        {
          "name": "graph_memory_protocol.md",
          "words": 2482,
          "is_shared": false
        },
        {
          "name": "sam_conversation_engine.md",
          "words": 2497,
          "is_shared": false
        },
        {
          "name": "sam_personality_framework.md",
          "words": 2483,
          "is_shared": false
        },
        {
          "name": "sam_protocol.md",
          "words": 3673,
          "is_shared": false
        },
        {
          "name": "session_history_research_protocol.md",
          "words": 1878,
          "is_shared": false
        },
        {
          "name": "specialist_routing.md",
          "words": 2555,
          "is_shared": false
        }
      ],
      "shared_files": [],
      "unique_files": [
        {
          "name": "controller_architecture.md",
          "words": 1773,
          "is_shared": false
        },
        {
          "name": "graph_memory_protocol.md",
          "words": 2482,
          "is_shared": false
        },
        {
          "name": "sam_conversation_engine.md",
          "words": 2497,
          "is_shared": false
        },
        {
          "name": "sam_personality_framework.md",
          "words": 2483,
          "is_shared": false
        },
        {
          "name": "sam_protocol.md",
          "words": 3673,
          "is_shared": false
        },
        {
          "name": "session_history_research_protocol.md",
          "words": 1878,
          "is_shared": false
        },
        {
          "name": "specialist_routing.md",
          "words": 2555,
          "is_shared": false
        }
      ]
    },
    "_SUMMARY": {
      "total_agents": 12,
      "total_words": 104579,
      "total_files": 62,
      "shared_files_count": 1
    }
  },
  "commented_code": [],
  "timestamp": "20251013_235651"
}
```
