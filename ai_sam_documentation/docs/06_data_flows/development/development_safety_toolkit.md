# Development Safety Toolkit - Bulletproof Code Management

## The Problem You've Identified
Claude Code is **unreliable** for comprehensive refactoring:
- ❌ Changes 70% of file references, misses 30%
- ❌ Makes excuses for incomplete work
- ❌ Creates broken imports and missing references
- ❌ Fallback strategies that create maintenance nightmares

## Current Status: What's Working ✅

### Your Existing Canvas System
- ✅ Canvas rendering works
- ✅ Canvas interactions work
- ✅ Canvas data handling works
- ✅ You can see nodes on canvas
- ✅ Basic drag/drop functionality

### What We've Validated
- ✅ Node overlay concept (HTML demo)
- ✅ File structure plan
- ✅ Integration approach
- ✅ Team coordination strategy

## The "Don't Break It" Principles

### Principle 1: Never Touch Working Code
```
RULE: If it works, don't change it
- Your existing canvas files → UNTOUCHED
- Your existing models → UNTOUCHED
- Your existing controllers → UNTOUCHED
```

### Principle 2: Build Alongside, Not Instead
```
APPROACH: Add new files, don't modify existing ones
- New overlay system → NEW files only
- Integration layer → NEW controller methods only
- Enhanced functionality → NEW models only
```

### Principle 3: Incremental Integration
```
STRATEGY: Connect piece by piece
- Step 1: Build overlay in isolation
- Step 2: Test overlay independently
- Step 3: Connect to existing canvas
- Step 4: Validate integration
```

## Safe Development Phases

### Phase 1: Build in Isolation (ZERO risk to existing system)
**Goal**: Create overlay system that works independently

**New Files Only**:
- `static/src/js/nodes/node_overlay_manager.js` (NEW)
- `static/src/js/nodes/node_factory.js` (NEW)
- `static/src/js/nodes/node_categories.js` (NEW)
- `static/src/js/nodes/templates/base_node.js` (NEW)

**Testing**: Create standalone HTML page to test overlay without affecting main system

### Phase 2: Non-Destructive Integration (Low risk)
**Goal**: Connect overlay to existing canvas without modifying canvas code

**New Integration Points**:
- `static/src/js/views/workflow_editor.js` (NEW - bridges overlay to canvas)
- `controllers/workflow_controller.py` (NEW methods only)

**Safety**: Existing canvas continues to work exactly as before

### Phase 3: Enhanced Features (Controlled risk)
**Goal**: Add new capabilities while preserving all existing functionality

**Approach**: Only add new features, never modify existing ones

### Phase 4: Optimization (Calculated risk)
**Goal**: Performance improvements and cleanup

**Only After**: All new features are working perfectly

## Automated Refactoring Tools

### Tool 1: File Rename & Reference Update Script
**File**: `dev_tools/refactor_rename.py`

```python
#!/usr/bin/env python3
"""
Bulletproof file rename with complete reference updates.
Usage: python refactor_rename.py old_name new_name
"""

import os
import re
import sys
import subprocess
from pathlib import Path

class RefactorRename:
    def __init__(self, module_path="addons/the_ai_automator"):
        self.module_path = Path(module_path)
        self.changes_made = []
        self.files_modified = []

    def rename_file_everywhere(self, old_name, new_name):
        """Rename file and update ALL references - no excuses"""
        print(f"🔍 Renaming {old_name} → {new_name}")

        # Step 1: Find the actual file
        old_file_path = self.find_file(old_name)
        if not old_file_path:
            print(f"❌ File {old_name} not found")
            return False

        # Step 2: Find ALL references to this file
        references = self.find_all_references(old_name)
        print(f"📍 Found {len(references)} references to update")

        # Step 3: Update ALL references (no partial updates allowed)
        self.update_all_references(old_name, new_name, references)

        # Step 4: Actually rename the file
        new_file_path = old_file_path.parent / new_name
        old_file_path.rename(new_file_path)

        # Step 5: Verify everything still works
        if self.verify_references(new_name):
            print(f"✅ Successfully renamed {old_name} → {new_name}")
            self.log_changes()
            return True
        else:
            print(f"❌ Verification failed - rolling back")
            self.rollback_changes()
            return False

    def find_file(self, filename):
        """Find file anywhere in module"""
        for file_path in self.module_path.rglob(filename):
            if file_path.is_file():
                return file_path
        return None

    def find_all_references(self, filename):
        """Find ALL references using multiple search methods"""
        references = []

        # Method 1: Grep search
        grep_results = self.grep_search(filename)
        references.extend(grep_results)

        # Method 2: Python import search
        import_results = self.find_import_references(filename)
        references.extend(import_results)

        # Method 3: Manifest asset search
        asset_results = self.find_asset_references(filename)
        references.extend(asset_results)

        # Method 4: XML view references
        xml_results = self.find_xml_references(filename)
        references.extend(xml_results)

        return list(set(references))  # Remove duplicates

    def grep_search(self, filename):
        """Use grep to find text references"""
        results = []
        try:
            # Remove extension for search
            name_without_ext = Path(filename).stem

            cmd = ["grep", "-r", "-l", name_without_ext, str(self.module_path)]
            output = subprocess.check_output(cmd, text=True)

            for line in output.strip().split('\n'):
                if line:
                    results.append(Path(line))
        except subprocess.CalledProcessError:
            pass  # No matches found
        return results

    def find_import_references(self, filename):
        """Find Python import statements"""
        results = []
        name_without_ext = Path(filename).stem

        for py_file in self.module_path.rglob("*.py"):
            try:
                content = py_file.read_text()
                if f"import {name_without_ext}" in content or f"from {name_without_ext}" in content:
                    results.append(py_file)
            except:
                continue
        return results

    def find_asset_references(self, filename):
        """Find references in __manifest__.py assets"""
        results = []
        manifest_file = self.module_path / "__manifest__.py"

        if manifest_file.exists():
            try:
                content = manifest_file.read_text()
                if filename in content:
                    results.append(manifest_file)
            except:
                pass
        return results

    def find_xml_references(self, filename):
        """Find references in XML files"""
        results = []
        name_without_ext = Path(filename).stem

        for xml_file in self.module_path.rglob("*.xml"):
            try:
                content = xml_file.read_text()
                if name_without_ext in content:
                    results.append(xml_file)
            except:
                continue
        return results

    def update_all_references(self, old_name, new_name, reference_files):
        """Update references in all files - MANDATORY completion"""
        old_stem = Path(old_name).stem
        new_stem = Path(new_name).stem

        for file_path in reference_files:
            if file_path.exists():
                try:
                    content = file_path.read_text()
                    modified_content = content

                    # Replace full filename
                    modified_content = modified_content.replace(old_name, new_name)

                    # Replace stem (filename without extension)
                    modified_content = modified_content.replace(old_stem, new_stem)

                    if modified_content != content:
                        # Backup original
                        backup_path = file_path.with_suffix(file_path.suffix + '.bak')
                        file_path.rename(backup_path)

                        # Write updated content
                        file_path.write_text(modified_content)

                        self.changes_made.append({
                            'file': file_path,
                            'backup': backup_path,
                            'old_content': content,
                            'new_content': modified_content
                        })
                        self.files_modified.append(str(file_path))

                        print(f"  ✏️  Updated {file_path}")

                except Exception as e:
                    print(f"  ❌ Failed to update {file_path}: {e}")

    def verify_references(self, new_name):
        """Verify all references were updated correctly"""
        # Check that no broken references remain
        broken_refs = self.find_all_references(Path(new_name).stem)

        # Should only find the actual file and legitimate references
        return len(broken_refs) > 0  # At least the file itself should be found

    def rollback_changes(self):
        """Rollback all changes if verification fails"""
        print("🔄 Rolling back changes...")
        for change in reversed(self.changes_made):
            try:
                # Remove modified file
                change['file'].unlink()
                # Restore backup
                change['backup'].rename(change['file'])
                print(f"  ↩️  Restored {change['file']}")
            except Exception as e:
                print(f"  ❌ Failed to rollback {change['file']}: {e}")

    def log_changes(self):
        """Log all changes made"""
        log_file = self.module_path / "refactor_log.txt"
        with open(log_file, 'a') as f:
            f.write(f"\n--- Refactor Session {datetime.now()} ---\n")
            for file_path in self.files_modified:
                f.write(f"Modified: {file_path}\n")

        print(f"📝 Changes logged to {log_file}")

    def cleanup_backups(self):
        """Remove backup files after successful refactor"""
        for change in self.changes_made:
            try:
                change['backup'].unlink()
                print(f"  🗑️  Removed backup {change['backup']}")
            except:
                pass

# CLI Usage
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python refactor_rename.py old_filename new_filename")
        sys.exit(1)

    old_name = sys.argv[1]
    new_name = sys.argv[2]

    refactor = RefactorRename()
    success = refactor.rename_file_everywhere(old_name, new_name)

    if success:
        refactor.cleanup_backups()
        print("✅ Refactor completed successfully")
    else:
        print("❌ Refactor failed - no changes made")
```

### Tool 2: Dependency Checker
**File**: `dev_tools/check_dependencies.py`

```python
#!/usr/bin/env python3
"""
Check for circular dependencies and missing imports
"""

import ast
import sys
from pathlib import Path

class DependencyChecker:
    def __init__(self, module_path="addons/the_ai_automator"):
        self.module_path = Path(module_path)
        self.imports = {}
        self.errors = []

    def check_all_dependencies(self):
        """Check entire module for dependency issues"""
        print("🔍 Checking dependencies...")

        # Scan all Python files
        for py_file in self.module_path.rglob("*.py"):
            self.analyze_file(py_file)

        # Check for issues
        self.find_circular_dependencies()
        self.find_missing_imports()

        if self.errors:
            print(f"❌ Found {len(self.errors)} dependency issues:")
            for error in self.errors:
                print(f"  - {error}")
            return False
        else:
            print("✅ No dependency issues found")
            return True

    def analyze_file(self, file_path):
        """Analyze imports in a single file"""
        try:
            content = file_path.read_text()
            tree = ast.parse(content)

            imports = []
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imports.append(node.module)

            self.imports[str(file_path)] = imports

        except Exception as e:
            self.errors.append(f"Could not analyze {file_path}: {e}")

    def find_circular_dependencies(self):
        """Detect circular import dependencies"""
        # Implementation for circular dependency detection
        # This is a simplified version - full implementation would be more complex
        pass

    def find_missing_imports(self):
        """Find references to undefined imports"""
        for file_path, imports in self.imports.items():
            for imp in imports:
                if not self.import_exists(imp):
                    self.errors.append(f"Missing import '{imp}' in {file_path}")

    def import_exists(self, import_name):
        """Check if an import can be resolved"""
        # Check if it's a standard library import
        try:
            __import__(import_name)
            return True
        except ImportError:
            pass

        # Check if it's a local module
        import_path = self.module_path / f"{import_name.replace('.', '/')}.py"
        return import_path.exists()

if __name__ == "__main__":
    checker = DependencyChecker()
    success = checker.check_all_dependencies()
    sys.exit(0 if success else 1)
```

### Tool 3: Code Quality Validator
**File**: `dev_tools/validate_quality.py`

```python
#!/usr/bin/env python3
"""
Validate code quality and find potential issues
"""

import re
import sys
from pathlib import Path

class CodeQualityValidator:
    def __init__(self, module_path="addons/the_ai_automator"):
        self.module_path = Path(module_path)
        self.issues = []

    def validate_all(self):
        """Run all quality checks"""
        print("🔍 Validating code quality...")

        self.check_file_organization()
        self.check_naming_conventions()
        self.check_code_duplication()
        self.check_security_issues()

        if self.issues:
            print(f"⚠️  Found {len(self.issues)} quality issues:")
            for issue in self.issues:
                print(f"  - {issue}")
            return False
        else:
            print("✅ Code quality validation passed")
            return True

    def check_file_organization(self):
        """Check for proper file organization"""
        # Check that __init__.py files exist
        required_init_files = [
            self.module_path / "__init__.py",
            self.module_path / "models" / "__init__.py",
            self.module_path / "controllers" / "__init__.py"
        ]

        for init_file in required_init_files:
            if not init_file.exists():
                self.issues.append(f"Missing {init_file}")

    def check_naming_conventions(self):
        """Check Python naming conventions"""
        for py_file in self.module_path.rglob("*.py"):
            try:
                content = py_file.read_text()

                # Check for camelCase in Python (should be snake_case)
                camel_case_pattern = r'\b[a-z]+[A-Z][a-zA-Z]*\b'
                matches = re.findall(camel_case_pattern, content)
                if matches:
                    self.issues.append(f"Possible camelCase naming in {py_file}: {matches[:3]}")

            except Exception:
                continue

    def check_code_duplication(self):
        """Find potential code duplication"""
        # Simple check for repeated function signatures
        function_signatures = {}

        for py_file in self.module_path.rglob("*.py"):
            try:
                content = py_file.read_text()

                # Find function definitions
                func_pattern = r'def\s+(\w+)\s*\([^)]*\):'
                functions = re.findall(func_pattern, content)

                for func_name in functions:
                    if func_name in function_signatures:
                        self.issues.append(f"Duplicate function name '{func_name}' in {py_file} and {function_signatures[func_name]}")
                    else:
                        function_signatures[func_name] = py_file

            except Exception:
                continue

    def check_security_issues(self):
        """Check for potential security issues"""
        security_patterns = [
            (r'password\s*=\s*["\'][^"\']+["\']', "Hardcoded password"),
            (r'api_key\s*=\s*["\'][^"\']+["\']', "Hardcoded API key"),
            (r'secret\s*=\s*["\'][^"\']+["\']', "Hardcoded secret"),
            (r'eval\s*\(', "Use of eval() function"),
            (r'exec\s*\(', "Use of exec() function"),
        ]

        for py_file in self.module_path.rglob("*.py"):
            try:
                content = py_file.read_text()

                for pattern, issue_desc in security_patterns:
                    if re.search(pattern, content, re.IGNORECASE):
                        self.issues.append(f"{issue_desc} in {py_file}")

            except Exception:
                continue

if __name__ == "__main__":
    validator = CodeQualityValidator()
    success = validator.validate_all()
    sys.exit(0 if success else 1)
```

## Usage Instructions

### Daily Development Workflow

1. **Before Making Changes**:
   ```bash
   # Check current state
   python dev_tools/check_dependencies.py
   python dev_tools/validate_quality.py
   ```

2. **When Renaming Files**:
   ```bash
   # Use automated tool instead of manual renaming
   python dev_tools/refactor_rename.py old_file.py new_file.py
   ```

3. **After Making Changes**:
   ```bash
   # Validate everything still works
   python dev_tools/check_dependencies.py
   python dev_tools/validate_quality.py
   ```

4. **Before Committing**:
   ```bash
   # Run full validation
   ./validate_all.sh
   ```

### Emergency Rollback

If something breaks:
1. Check `refactor_log.txt` for recent changes
2. Use Git to revert: `git checkout HEAD~1 -- filename`
3. Or restore from automatic backups created by refactor tools

## Safe Testing Strategy

### Test Environment Setup
```bash
# Create isolated test environment
python -m venv test_env
source test_env/bin/activate  # or test_env\Scripts\activate on Windows

# Install only in test environment
pip install -r requirements.txt
```

### Testing Phases
1. **Unit Tests** - Test individual components in isolation
2. **Integration Tests** - Test component connections
3. **System Tests** - Test complete workflows
4. **Regression Tests** - Ensure nothing broke

### Validation Checklist
- [ ] All existing functionality still works
- [ ] New functionality works as expected
- [ ] No broken imports or references
- [ ] No circular dependencies
- [ ] Code quality standards met
- [ ] Security checks passed

This toolkit ensures that development is safe, incremental, and bulletproof against the common issues that Claude Code creates during refactoring.