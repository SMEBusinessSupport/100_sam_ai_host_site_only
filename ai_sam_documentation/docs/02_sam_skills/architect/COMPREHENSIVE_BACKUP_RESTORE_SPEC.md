# Comprehensive Backup/Restore System - Technical Specification

**Created**: 2025-10-16
**Author**: SAM AI
**Status**: Planning Phase
**Target Module**: `ai_brain`
**Assigned To**: TBD (Recommendation: `/developer` + `/cto` review)

---

## 🎯 Executive Summary

**Problem**: Current backup system only exports Odoo metadata (configs, import records) but **NOT the actual data** (conversations, messages, workflows, PostgreSQL graph, ChromaDB vectors).

**Solution**: Comprehensive ZIP bundle backup containing:
- ALL Odoo models (65+ models, 60+ data tables)
- PostgreSQL graph database (Apache AGE dump)
- ChromaDB vector embeddings (directory copy)
- Metadata and restore instructions

**Outcome**: Single-file backup that is **100% restorable** to recreate entire SAM AI system.

---

## 📊 Current State Analysis

### What's Currently Backed Up (Partial)
| Component | Status | Method | File |
|-----------|--------|--------|------|
| Memory configs | ✅ Backed up | Excel export | `ai_memory_config.py:169-360` |
| Conversation imports | ✅ Backed up | Excel export | Same |
| Extractor plugins | ✅ Backed up | Excel export | Same |
| **Conversations** | ❌ NOT backed up | - | - |
| **Messages** | ❌ NOT backed up | - | - |
| **Canvas workflows** | ❌ NOT backed up | - | - |
| **Nodes/Executions** | ❌ NOT backed up | - | - |
| **SAM personality** | ❌ NOT backed up | - | - |
| **User profiles** | ❌ NOT backed up | - | - |
| **PostgreSQL graph** | ❌ NOT backed up | - | - |
| **ChromaDB vectors** | ❌ NOT backed up | - | - |

### Current Import Capability
| Component | Status | Method | File |
|-----------|--------|--------|------|
| Memory configs | ✅ Can restore | Excel import | `ai_memory_import_wizard.py:109-146` |
| Conversation imports | ✅ Can restore | Excel import | `ai_memory_import_wizard.py:148-189` |
| Extractor plugins | ✅ Can restore | Excel import | `ai_memory_import_wizard.py:191-225` |
| **Everything else** | ❌ Cannot restore | - | - |

**Gap**: Only 3% of actual data is backed up and restorable.

---

## 🏗️ Architecture: ZIP Bundle Format

### File Structure
```
sam_ai_complete_backup_20250116_143022.zip
│
├── metadata.json                          # Backup metadata
├── restore_instructions.md                # Human-readable restore guide
│
├── odoo_data/                             # All Odoo models
│   ├── ai_brain_backup.xlsx              # All models in multi-sheet Excel
│   └── model_list.json                   # Model inventory
│
├── databases/                             # External databases
│   ├── postgres_graph_dump.sql           # Apache AGE graph database
│   └── chroma_data.zip                   # ChromaDB vector embeddings (zipped)
│
└── logs/                                  # Export logs
    └── export_log.txt                    # Detailed export process log
```

### Metadata JSON Schema
```json
{
  "backup_version": "1.0.0",
  "timestamp": "2025-01-16T14:30:22Z",
  "backup_type": "complete",
  "odoo_version": "18.0",
  "module_versions": {
    "ai_brain": "18.0.3.12.0",
    "ai_sam": "18.0.5.3.0",
    "ai_sam_memory": "18.0.1.0.0"
  },
  "database_info": {
    "postgres_version": "15.x",
    "graph_database": "sam_ai_memory",
    "graph_name": "sam_ai_knowledge",
    "chroma_persist_directory": "./chroma_data"
  },
  "model_counts": {
    "ai.conversation": 1234,
    "ai.message": 45678,
    "canvas": 89,
    "nodes": 456,
    "sam.user.profile": 23,
    "...": "..."
  },
  "file_sizes": {
    "odoo_data_xlsx": "45.2 MB",
    "postgres_dump": "123.5 MB",
    "chroma_data": "678.9 MB",
    "total_zip": "847.6 MB"
  },
  "export_duration_seconds": 127,
  "export_status": "success",
  "export_errors": [],
  "checksum": "sha256:abc123..."
}
```

---

## 📋 Complete Model Inventory (65 Models)

### Category 1: Core SAM AI Models (18 models)

| Model | Description | Priority | Sensitive Data? |
|-------|-------------|----------|-----------------|
| `ai.conversation` | AI conversation threads | 🔴 Critical | Yes (user content) |
| `ai.message` | Individual messages | 🔴 Critical | Yes (user content) |
| `ai.token.usage` | Token consumption tracking | 🟡 Important | No |
| `ai.service` | Claude API service | 🔴 Critical | No |
| `ai.service.config` | API keys, model configs | 🔴 Critical | Yes (API keys) |
| `ai.service.provider` | Multi-AI providers | 🟡 Important | Possibly (API keys) |
| `ai.agent.registry` | Agent definitions | 🔴 Critical | No |
| `ai.agent.knowledge` | Agent knowledge chunks | 🔴 Critical | No |
| `ai.agent.execution` | Execution audit trail | 🟡 Important | No |
| `ai.context.builder` | Context building system | 🟡 Important | No |
| `ai.artifact.version` | Artifact version history | 🟢 Nice-to-have | No |
| `ai.knowledge.domain` | Knowledge domain hubs | 🟡 Important | No |
| `ai.knowledge.subcategory` | AI-detected subcategories | 🟡 Important | No |
| `ai.conversation.tag` | Conversation tags | 🟢 Nice-to-have | No |
| `ai.voice.service` | Voice-to-text service | 🟡 Important | No |
| `ai.workspace` | Team workspace | 🟡 Important | No |
| `ai.qr.code` | QR code generation | 🟢 Nice-to-have | No |
| `ai.registry.watcher` | Module monitor | 🟢 Nice-to-have | No |

### Category 2: Memory System Models (6 models)

| Model | Description | Priority | Sensitive Data? |
|-------|-------------|----------|-----------------|
| `ai.memory.config` | Memory system config | 🔴 Critical | Yes (DB credentials) |
| `ai.graph.service` | Apache AGE service | 🔴 Critical | No |
| `ai.vector.service` | ChromaDB service | 🔴 Critical | No |
| `ai.conversation.import` | Conversation imports | 🟡 Important | No |
| `ai.document.extractor` | Document extraction | 🟡 Important | No |
| `ai.extractor.plugin` | AI-learned extractors | 🟡 Important | No |

### Category 3: Canvas/Workflow Models (11 models)

| Model | Description | Priority | Sensitive Data? |
|-------|-------------|----------|-----------------|
| `canvas` | Workflow definitions | 🔴 Critical | No |
| `nodes` | Node definitions | 🔴 Critical | No |
| `connections` | Node connections | 🔴 Critical | No |
| `executions` | Execution history | 🟡 Important | No |
| `workflow_types` | Workflow types | 🟡 Important | No |
| `workflow.template` | Workflow templates | 🟡 Important | No |
| `workflow.business.unit` | Business units | 🟢 Nice-to-have | No |
| `api_credentials` | API credentials | 🔴 Critical | Yes (credentials) |
| `canvas.platform` | Platform registry | 🟡 Important | No |
| `canvas_pan_move` | Canvas interaction | 🟢 Nice-to-have | No |
| `settings` | Workflow settings | 🟡 Important | No |

### Category 4: SAM Personality Models (8 models)

| Model | Description | Priority | Sensitive Data? |
|-------|-------------|----------|-----------------|
| `sam.personality` | SAM's personality DNA | 🔴 Critical | No |
| `sam.user.profile` | User relationship profiles | 🔴 Critical | Yes (user data) |
| `sam.user.settings` | User-specific settings | 🔴 Critical | Yes (user data) |
| `sam.member` | Member management | 🔴 Critical | Yes (user data) |
| `sam.environment` | Environment detection | 🟡 Important | No |
| `sam.mode.context` | Mode-specific context | 🟡 Important | No |
| `sam.brain.modes` | Brain modes | 🟡 Important | No |
| `sam.knowledge.doc` | Knowledge documents | 🟡 Important | No |

### Category 5: Chat Models (2 models)

| Model | Description | Priority | Sensitive Data? |
|-------|-------------|----------|-----------------|
| `sam.chat.session` | Chat sessions | 🔴 Critical | Yes (user content) |
| `sam.chat.message` | Chat messages | 🔴 Critical | Yes (user content) |

### Category 6: N8N Integration Models (7 models)

| Model | Description | Priority | Sensitive Data? |
|-------|-------------|----------|-----------------|
| `n8n_node_types` | N8N node catalog | 🟡 Important | No |
| `node_types` | Node type registry | 🟡 Important | No |
| `n8n.simple.supplier` | Simple suppliers | 🟢 Nice-to-have | No |
| `n8n.simple.node` | Simple nodes | 🟢 Nice-to-have | No |
| `n8n.simple.extractor` | Simple extractors | 🟢 Nice-to-have | No |
| `n8n.node.category` | Node categories | 🟢 Nice-to-have | No |
| `dynamic_menus` | Dynamic menus | 🟢 Nice-to-have | No |

### Category 7: Utility/Support Models (8 models)

| Model | Description | Priority | Sensitive Data? |
|-------|-------------|----------|-----------------|
| `ai.branch` | Branch registry | 🟡 Important | No |
| `ai.categorization.service` | Categorization AI | 🟢 Nice-to-have | No |
| `ai.subcategory.detection.service` | Subcategory detection | 🟢 Nice-to-have | No |
| `ai.automator.config` | Automator config | 🟢 Nice-to-have | No |
| `ai.automator.documentation` | Documentation data | 🟢 Nice-to-have | No |
| `documentation_intelligence` | Doc intelligence | 🟢 Nice-to-have | No |
| `business_unit` | Business units | 🟢 Nice-to-have | No |
| `creatives_landing_card` | Landing cards | 🟢 Nice-to-have | No |

### Category 8: Blog/Social Models (3 models)

| Model | Description | Priority | Sensitive Data? |
|-------|-------------|----------|-----------------|
| `odoo.blog.post` | Blog posts | 🟡 Important | No |
| `odoo.blog.image` | Blog images | 🟡 Important | No |
| `odoo.blog.story` | Blog stories | 🟡 Important | No |

### Category 9: External Database Models (2 services)

| Component | Description | Priority | Backup Method |
|-----------|-------------|----------|---------------|
| **Apache AGE Graph** | PostgreSQL graph database | 🔴 Critical | `pg_dump` SQL export |
| **ChromaDB Vectors** | Vector embeddings | 🔴 Critical | Directory copy + zip |

---

## 🔧 Implementation Plan

### Phase 1: Export System (New Function)

**File**: `ai_brain/models/ai_memory_config.py`
**New Method**: `action_export_complete_backup()`

#### Export Workflow Steps

```python
def action_export_complete_backup(self):
    """
    Export complete SAM AI system backup to ZIP bundle.

    Returns:
        dict: Download action for ZIP file
    """
    # Step 1: Create temp directory
    temp_dir = self._create_temp_export_directory()

    # Step 2: Export all Odoo models to Excel
    odoo_xlsx_path = self._export_all_odoo_models(temp_dir)

    # Step 3: Dump PostgreSQL graph database
    postgres_dump_path = self._export_postgres_graph(temp_dir)

    # Step 4: Copy ChromaDB directory
    chroma_zip_path = self._export_chroma_data(temp_dir)

    # Step 5: Generate metadata JSON
    metadata_path = self._generate_metadata(temp_dir, {
        'odoo_xlsx': odoo_xlsx_path,
        'postgres_dump': postgres_dump_path,
        'chroma_zip': chroma_zip_path,
    })

    # Step 6: Generate restore instructions
    instructions_path = self._generate_restore_instructions(temp_dir)

    # Step 7: Create ZIP bundle
    zip_path = self._create_zip_bundle(temp_dir)

    # Step 8: Create Odoo attachment
    attachment = self._create_download_attachment(zip_path)

    # Step 9: Cleanup temp directory
    self._cleanup_temp_directory(temp_dir)

    # Step 10: Return download action
    return {
        'type': 'ir.actions.act_url',
        'url': f'/web/content/{attachment.id}?download=true',
        'target': 'new',
    }
```

#### Detailed Sub-Methods

##### 1. `_export_all_odoo_models(temp_dir)` - Export to Excel

```python
def _export_all_odoo_models(self, temp_dir):
    """
    Export ALL Odoo models to multi-sheet Excel file.

    Strategy:
    - One sheet per model (65+ sheets)
    - Column headers = field names
    - Handle Many2one (store ID + name)
    - Handle One2many/Many2many (store IDs as comma-separated)
    - Handle Binary fields (base64 encode)
    - Handle Date/Datetime (ISO format)

    Returns:
        str: Path to Excel file
    """
    output = BytesIO()
    workbook = xlsxwriter.Workbook(output, {'in_memory': True})

    # Model list to export (in dependency order)
    models_to_export = [
        # Core models first (no dependencies)
        'ai.service.provider',
        'ai.service.config',
        'ai.service',
        # Then models that depend on core
        'ai.conversation',
        'ai.message',
        'ai.token.usage',
        # Canvas models
        'canvas',
        'nodes',
        'connections',
        'executions',
        # SAM personality
        'sam.personality',
        'sam.user.profile',
        'sam.member',
        # Memory system
        'ai.memory.config',
        'ai.conversation.import',
        'ai.extractor.plugin',
        # ... ALL 65 models in dependency order
    ]

    for model_name in models_to_export:
        self._export_model_to_sheet(workbook, model_name)

    workbook.close()
    output.seek(0)

    # Write to temp directory
    xlsx_path = os.path.join(temp_dir, 'odoo_data', 'ai_brain_backup.xlsx')
    os.makedirs(os.path.dirname(xlsx_path), exist_ok=True)
    with open(xlsx_path, 'wb') as f:
        f.write(output.read())

    return xlsx_path
```

##### 2. `_export_postgres_graph(temp_dir)` - PostgreSQL Dump

```python
def _export_postgres_graph(self, temp_dir):
    """
    Export Apache AGE graph database using pg_dump.

    Requirements:
    - PostgreSQL client tools installed
    - pg_dump accessible in PATH
    - Database credentials from ai.memory.config

    Returns:
        str: Path to SQL dump file
    """
    config = self.search([], limit=1)
    if not config or not config.graph_enabled:
        _logger.warning("Graph database not enabled, skipping export")
        return None

    dump_path = os.path.join(temp_dir, 'databases', 'postgres_graph_dump.sql')
    os.makedirs(os.path.dirname(dump_path), exist_ok=True)

    # Set PostgreSQL password environment variable
    env = os.environ.copy()
    env['PGPASSWORD'] = config.graph_password

    # Run pg_dump
    cmd = [
        'pg_dump',
        '-h', config.graph_host,
        '-p', str(config.graph_port),
        '-U', config.graph_user,
        '-d', config.graph_database,
        '-f', dump_path,
        '--no-owner',  # Don't include ownership commands
        '--no-acl',    # Don't include ACL commands
    ]

    try:
        result = subprocess.run(
            cmd,
            env=env,
            capture_output=True,
            text=True,
            timeout=600  # 10 minute timeout
        )

        if result.returncode != 0:
            raise Exception(f"pg_dump failed: {result.stderr}")

        _logger.info(f"PostgreSQL graph exported: {os.path.getsize(dump_path)} bytes")
        return dump_path

    except subprocess.TimeoutExpired:
        raise Exception("PostgreSQL export timed out (>10 minutes)")
    except FileNotFoundError:
        raise Exception("pg_dump not found. Install PostgreSQL client tools.")
```

##### 3. `_export_chroma_data(temp_dir)` - ChromaDB Copy

```python
def _export_chroma_data(self, temp_dir):
    """
    Copy and zip ChromaDB persist directory.

    ChromaDB stores data in a directory structure:
    - chroma.sqlite3 (metadata)
    - Parquet files (embeddings)
    - Index files

    Returns:
        str: Path to zipped ChromaDB directory
    """
    config = self.search([], limit=1)
    if not config or not config.vector_enabled:
        _logger.warning("Vector database not enabled, skipping export")
        return None

    chroma_source = config.chroma_persist_directory
    if not os.path.exists(chroma_source):
        _logger.warning(f"ChromaDB directory not found: {chroma_source}")
        return None

    chroma_zip_path = os.path.join(temp_dir, 'databases', 'chroma_data.zip')
    os.makedirs(os.path.dirname(chroma_zip_path), exist_ok=True)

    # Create ZIP of ChromaDB directory
    shutil.make_archive(
        chroma_zip_path.replace('.zip', ''),  # base name
        'zip',                                 # format
        chroma_source                          # root directory
    )

    _logger.info(f"ChromaDB exported: {os.path.getsize(chroma_zip_path)} bytes")
    return chroma_zip_path
```

##### 4. `_generate_metadata(temp_dir, exported_files)` - Metadata JSON

```python
def _generate_metadata(self, temp_dir, exported_files):
    """
    Generate metadata JSON with backup information.

    Args:
        temp_dir (str): Temp export directory
        exported_files (dict): Paths to exported files

    Returns:
        str: Path to metadata.json
    """
    # Count records for each model
    model_counts = {}
    for model_name in self._get_all_model_names():
        try:
            count = self.env[model_name].search_count([])
            model_counts[model_name] = count
        except:
            model_counts[model_name] = 0

    # Get file sizes
    file_sizes = {}
    for key, path in exported_files.items():
        if path and os.path.exists(path):
            size_bytes = os.path.getsize(path)
            file_sizes[key] = self._format_file_size(size_bytes)

    # Build metadata
    metadata = {
        'backup_version': '1.0.0',
        'timestamp': datetime.now().isoformat(),
        'backup_type': 'complete',
        'odoo_version': self.env['ir.config_parameter'].sudo().get_param('base.version_info', 'unknown'),
        'module_versions': self._get_module_versions(),
        'database_info': self._get_database_info(),
        'model_counts': model_counts,
        'file_sizes': file_sizes,
        'export_status': 'success',
        'export_errors': [],
    }

    # Write to file
    metadata_path = os.path.join(temp_dir, 'metadata.json')
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=2)

    return metadata_path
```

##### 5. `_create_zip_bundle(temp_dir)` - Create ZIP

```python
def _create_zip_bundle(self, temp_dir):
    """
    Create final ZIP bundle from temp directory.

    Returns:
        str: Path to ZIP file
    """
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    zip_filename = f"sam_ai_complete_backup_{timestamp}.zip"
    zip_path = os.path.join(tempfile.gettempdir(), zip_filename)

    # Create ZIP
    shutil.make_archive(
        zip_path.replace('.zip', ''),  # base name
        'zip',                          # format
        temp_dir                        # root directory
    )

    _logger.info(f"ZIP bundle created: {zip_path} ({os.path.getsize(zip_path)} bytes)")
    return zip_path
```

---

### Phase 2: Import System (New Function)

**File**: `ai_brain/models/ai_memory_import_wizard.py`
**Enhanced Method**: `action_import_complete_backup()`

#### Import Workflow Steps

```python
def action_import_complete_backup(self):
    """
    Import complete SAM AI backup from ZIP bundle.

    Steps:
    1. Upload and validate ZIP
    2. Extract to temp directory
    3. Read and validate metadata
    4. Import Odoo models (with dependency order)
    5. Import PostgreSQL graph
    6. Import ChromaDB data
    7. Verify data integrity
    8. Cleanup temp directory

    Returns:
        dict: Notification with results
    """
    self.ensure_one()

    if not self.backup_file:
        raise ValidationError(_('Please upload a backup file.'))

    try:
        # Step 1: Extract ZIP to temp directory
        temp_dir = self._extract_zip_to_temp(self.backup_file)

        # Step 2: Read and validate metadata
        metadata = self._read_and_validate_metadata(temp_dir)

        # Step 3: Check version compatibility
        self._check_version_compatibility(metadata)

        # Step 4: Import Odoo models (Excel)
        odoo_results = self._import_all_odoo_models(temp_dir, metadata)

        # Step 5: Import PostgreSQL graph (SQL)
        postgres_results = self._import_postgres_graph(temp_dir, metadata)

        # Step 6: Import ChromaDB data (unzip)
        chroma_results = self._import_chroma_data(temp_dir, metadata)

        # Step 7: Verify data integrity
        verification = self._verify_data_integrity(metadata)

        # Step 8: Cleanup
        self._cleanup_temp_directory(temp_dir)

        # Step 9: Build results message
        results_message = self._build_results_message({
            'odoo': odoo_results,
            'postgres': postgres_results,
            'chroma': chroma_results,
            'verification': verification,
        })

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Backup Restored Successfully'),
                'message': results_message,
                'type': 'success',
                'sticky': True,
            }
        }

    except Exception as e:
        _logger.exception("Failed to import backup")
        raise UserError(_('Import failed: %s') % str(e))
```

#### Detailed Sub-Methods

##### 1. `_import_all_odoo_models(temp_dir, metadata)` - Import from Excel

```python
def _import_all_odoo_models(self, temp_dir, metadata):
    """
    Import all Odoo models from Excel file.

    Strategy:
    - Import in dependency order (defined in metadata)
    - Handle Many2one (resolve by name/ID)
    - Handle One2many/Many2many (restore relationships)
    - Handle Binary fields (decode base64)
    - Skip system fields (create_uid, write_uid, create_date, write_date)

    Args:
        temp_dir (str): Temp directory
        metadata (dict): Backup metadata

    Returns:
        dict: Import results per model
    """
    xlsx_path = os.path.join(temp_dir, 'odoo_data', 'ai_brain_backup.xlsx')
    workbook = openpyxl.load_workbook(xlsx_path, data_only=True)

    results = {}

    # Import models in dependency order
    for model_name in metadata.get('model_import_order', []):
        try:
            sheet = workbook[model_name]
            count = self._import_model_from_sheet(model_name, sheet)
            results[model_name] = {'status': 'success', 'count': count}
        except Exception as e:
            results[model_name] = {'status': 'error', 'error': str(e)}
            _logger.exception(f"Failed to import model {model_name}")

    return results
```

##### 2. `_import_postgres_graph(temp_dir, metadata)` - PostgreSQL Restore

```python
def _import_postgres_graph(self, temp_dir, metadata):
    """
    Import PostgreSQL graph database from SQL dump.

    Requirements:
    - PostgreSQL client tools installed
    - psql accessible in PATH
    - Database credentials from ai.memory.config

    Args:
        temp_dir (str): Temp directory
        metadata (dict): Backup metadata

    Returns:
        dict: Import results
    """
    config = self.env['ai.memory.config'].search([], limit=1)
    if not config or not config.graph_enabled:
        return {'status': 'skipped', 'reason': 'Graph database not enabled'}

    dump_path = os.path.join(temp_dir, 'databases', 'postgres_graph_dump.sql')
    if not os.path.exists(dump_path):
        return {'status': 'skipped', 'reason': 'SQL dump not found'}

    # Set PostgreSQL password
    env = os.environ.copy()
    env['PGPASSWORD'] = config.graph_password

    # Run psql to restore
    cmd = [
        'psql',
        '-h', config.graph_host,
        '-p', str(config.graph_port),
        '-U', config.graph_user,
        '-d', config.graph_database,
        '-f', dump_path,
        '--quiet',
    ]

    try:
        result = subprocess.run(
            cmd,
            env=env,
            capture_output=True,
            text=True,
            timeout=600
        )

        if result.returncode != 0:
            return {'status': 'error', 'error': result.stderr}

        return {'status': 'success', 'message': 'Graph database restored'}

    except Exception as e:
        return {'status': 'error', 'error': str(e)}
```

##### 3. `_import_chroma_data(temp_dir, metadata)` - ChromaDB Restore

```python
def _import_chroma_data(self, temp_dir, metadata):
    """
    Import ChromaDB data from zipped directory.

    Args:
        temp_dir (str): Temp directory
        metadata (dict): Backup metadata

    Returns:
        dict: Import results
    """
    config = self.env['ai.memory.config'].search([], limit=1)
    if not config or not config.vector_enabled:
        return {'status': 'skipped', 'reason': 'Vector database not enabled'}

    chroma_zip_path = os.path.join(temp_dir, 'databases', 'chroma_data.zip')
    if not os.path.exists(chroma_zip_path):
        return {'status': 'skipped', 'reason': 'ChromaDB zip not found'}

    # Unzip to configured persist directory
    chroma_target = config.chroma_persist_directory

    # Backup existing ChromaDB data (if exists)
    if os.path.exists(chroma_target):
        backup_path = f"{chroma_target}_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        shutil.move(chroma_target, backup_path)
        _logger.info(f"Existing ChromaDB backed up to: {backup_path}")

    # Unzip restored data
    shutil.unpack_archive(chroma_zip_path, chroma_target, 'zip')

    return {'status': 'success', 'message': 'ChromaDB data restored'}
```

---

### Phase 3: Safety Mechanisms

#### 1. Version Compatibility Check

```python
def _check_version_compatibility(self, metadata):
    """
    Verify backup is compatible with current system.

    Checks:
    - Odoo version match (major version)
    - Module versions (warn if different)
    - Backup format version

    Raises:
        ValidationError: If incompatible
    """
    # Check backup format version
    backup_version = metadata.get('backup_version', '0.0.0')
    if not backup_version.startswith('1.'):
        raise ValidationError(_('Unsupported backup format version: %s') % backup_version)

    # Check Odoo version
    current_odoo_version = self.env['ir.config_parameter'].sudo().get_param('base.version_info', 'unknown')
    backup_odoo_version = metadata.get('odoo_version', 'unknown')

    if current_odoo_version.split('.')[0] != backup_odoo_version.split('.')[0]:
        raise ValidationError(_(
            'Odoo version mismatch!\n'
            'Backup: %s\n'
            'Current: %s'
        ) % (backup_odoo_version, current_odoo_version))

    # Warn about module version differences
    backup_modules = metadata.get('module_versions', {})
    current_modules = self._get_module_versions()

    mismatches = []
    for module, backup_ver in backup_modules.items():
        current_ver = current_modules.get(module)
        if current_ver and current_ver != backup_ver:
            mismatches.append(f"{module}: {backup_ver} → {current_ver}")

    if mismatches:
        _logger.warning(f"Module version mismatches: {mismatches}")
```

#### 2. Dry-Run Mode (Preview Import)

```python
dry_run = fields.Boolean(
    string='Dry Run (Preview Only)',
    default=False,
    help='Preview import without making changes'
)

def action_import_complete_backup(self):
    """Import with optional dry-run"""
    if self.dry_run:
        # Read metadata and show what WOULD be imported
        return self._preview_import()
    else:
        # Actually perform import
        return self._perform_import()
```

#### 3. Rollback on Failure

```python
def _perform_import(self):
    """Import with automatic rollback on failure"""
    savepoint = self.env.cr.savepoint()

    try:
        # Perform all imports
        results = self._import_all_data()

        # If any critical import failed, rollback
        if self._has_critical_failures(results):
            savepoint.rollback()
            raise UserError(_('Import failed, all changes rolled back'))
        else:
            savepoint.commit()
            return results

    except Exception as e:
        savepoint.rollback()
        raise
```

---

## 🚀 Implementation Checklist

### Pre-Implementation

- [ ] Review this spec with `/cto` (infrastructure review)
- [ ] Verify PostgreSQL client tools installed on server
- [ ] Verify ChromaDB directory accessible
- [ ] Test database credentials (PostgreSQL + ChromaDB)
- [ ] Estimate disk space requirements
- [ ] Plan backup storage location

### Development Phase

#### Export System
- [ ] Create `_export_all_odoo_models()` method
- [ ] Create `_export_postgres_graph()` method
- [ ] Create `_export_chroma_data()` method
- [ ] Create `_generate_metadata()` method
- [ ] Create `_create_zip_bundle()` method
- [ ] Add error handling and logging
- [ ] Add progress tracking

#### Import System
- [ ] Create `_import_all_odoo_models()` method
- [ ] Create `_import_postgres_graph()` method
- [ ] Create `_import_chroma_data()` method
- [ ] Create version compatibility check
- [ ] Add dry-run preview mode
- [ ] Add rollback mechanism
- [ ] Add progress tracking

#### Safety & Validation
- [ ] Implement checksum verification
- [ ] Implement version compatibility checks
- [ ] Implement data integrity verification
- [ ] Add comprehensive error messages
- [ ] Add detailed logging

### Testing Phase

- [ ] Test export on small dataset
- [ ] Test export on production-size dataset
- [ ] Test import on fresh database
- [ ] Test import with existing data (merge mode)
- [ ] Test version mismatch handling
- [ ] Test PostgreSQL connection failures
- [ ] Test ChromaDB access issues
- [ ] Test disk space exhaustion
- [ ] Test corrupted ZIP handling
- [ ] Test partial backup/restore scenarios

### Documentation Phase

- [ ] Create user guide (how to backup/restore)
- [ ] Create troubleshooting guide
- [ ] Document system requirements
- [ ] Document backup best practices
- [ ] Create video walkthrough

---

## 🎯 Success Criteria

**Export**:
- ✅ Single ZIP file contains ALL data
- ✅ Export completes in < 10 minutes (for 1GB dataset)
- ✅ ZIP is < 1GB (compressed)
- ✅ No data loss during export
- ✅ Clear error messages on failure

**Import**:
- ✅ Restore completes in < 15 minutes
- ✅ 100% data restored (verified by counts)
- ✅ Relationships preserved (Many2one, One2many)
- ✅ PostgreSQL graph intact
- ✅ ChromaDB vectors intact
- ✅ Version mismatch detected and handled
- ✅ Rollback works on failure

---

## ⚠️ Known Limitations & Risks

### Limitations

1. **Large Dataset Performance**:
   - Export/import time scales with data size
   - ZIP compression can be slow for large ChromaDB

2. **PostgreSQL Dependency**:
   - Requires `pg_dump` and `psql` installed
   - May fail if PostgreSQL version mismatch

3. **Disk Space**:
   - Requires 2-3x data size for temp files
   - ZIP compression may not help if data already compressed

4. **Binary Fields**:
   - Excel has 32,767 character limit per cell
   - Very large binary fields may be truncated

### Risks & Mitigation

| Risk | Impact | Mitigation |
|------|--------|------------|
| Export timeout (large dataset) | High | Add progress tracking, split into chunks |
| Disk space exhaustion | High | Check available space before export |
| PostgreSQL connection failure | Medium | Add connection test, clear error messages |
| Version incompatibility | Medium | Add version check, migration logic |
| Corrupted ZIP | Low | Add checksum verification |
| Partial restore failure | High | Add rollback mechanism |

---

## 📞 Questions for Infrastructure Review

**For `/cto` Agent**:

1. **PostgreSQL Access**:
   - Are PostgreSQL client tools installed on the server?
   - What version of PostgreSQL is running?
   - Are credentials stored securely (not in code)?

2. **ChromaDB Access**:
   - Where is ChromaDB persist directory?
   - Is directory writable by Odoo process?
   - What's current size of ChromaDB data?

3. **Disk Space**:
   - How much disk space available for temp files?
   - Where should we store temp export files?
   - Should we implement cleanup on failure?

4. **Performance**:
   - What's acceptable export/import time?
   - Should we implement async export (background job)?
   - Should we implement progress bar?

5. **Security**:
   - Should backup ZIP be encrypted?
   - Should we include API keys in backup?
   - How to handle sensitive credentials?

6. **Backup Strategy**:
   - Where should backups be stored long-term?
   - Should we implement automated scheduled backups?
   - What's retention policy?

---

## 🎯 Recommended Assignment

**Primary Developer**: `/developer` agent
**Infrastructure Review**: `/cto` agent
**Testing**: `/qa-guardian` agent
**Documentation**: `/docs` agent

**Estimated Effort**: 2-3 days (with testing)

---

**Next Steps**:
1. `/cto` reviews infrastructure questions
2. `/developer` implements Phase 1 (Export)
3. Test export on staging environment
4. `/developer` implements Phase 2 (Import)
5. Test import on fresh database
6. `/qa-guardian` runs full test suite
7. `/docs` creates user documentation

---

**End of Specification** ✅
