# Uninstall Protection System - Technical Specification

**Created**: 2025-10-16
**Priority**: 🔴 CRITICAL
**Part of**: Comprehensive Backup/Restore System
**Status**: Planning Phase - NOT YET DELEGATED

---

## 🎯 Executive Summary

**Problem**: Users can currently uninstall `ai_brain` module without backing up data, causing catastrophic data loss (51,002 messages, 229 conversations, 560 attachments).

**Solution**: 3-layer protection system that **BLOCKS uninstall** unless recent backup exists.

**Impact**:
- ✅ Prevents accidental data loss
- ✅ Forces backup before uninstall
- ✅ Provides audit trail
- ✅ Saves user's "sorry arse" from data loss shitstorm

---

## 🔄 Two Backup Strategies

### **Strategy 1: Proactive** (User Initiates)
```
User goes to: SAM AI → Settings → Backup & Restore
User clicks: "Create Complete Backup"
Result: Encrypted ZIP downloaded, backup confirmation recorded
```

### **Strategy 2: Reactive** (System Forces)
```
User tries: Apps → ai_brain → Uninstall
System BLOCKS: "You MUST backup first!"
User forced to: Create backup before uninstall allowed
Result: Same as Strategy 1 (backup created + downloaded)
```

**Both strategies lead to the same outcome**: User has backup before uninstall proceeds.

---

## 🛡️ 3-Layer Protection System

### **Layer 1: Uninstall Interceptor** 🚫

**File**: `ai_brain/models/ir_module_module.py` (NEW FILE)

**Purpose**: Override Odoo's uninstall button to block `ai_brain` uninstall if no backup exists.

**Implementation**:

```python
# -*- coding: utf-8 -*-
from odoo import models, api, _
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)


class IrModuleModule(models.Model):
    """
    Override Odoo's module uninstall to protect ai_brain from data loss.

    Intercepts uninstall attempt and:
    1. Checks if ai_brain module is being uninstalled
    2. Checks if data exists (conversations, messages, workflows)
    3. Checks if recent backup exists (< 24 hours old)
    4. BLOCKS uninstall if no backup, WARNS if backup is stale
    """
    _inherit = 'ir.module.module'

    def button_immediate_uninstall(self):
        """
        Override Odoo's uninstall button.
        Block ai_brain uninstall unless recent backup exists.
        """
        # Check if ai_brain is being uninstalled
        if 'ai_brain' in self.mapped('name'):
            return self._check_ai_brain_uninstall()

        # If not ai_brain, allow normal uninstall
        return super(IrModuleModule, self).button_immediate_uninstall()

    def _check_ai_brain_uninstall(self):
        """
        Validate ai_brain uninstall is safe.

        Steps:
        1. Count critical data (conversations, messages, workflows)
        2. Check for recent backup (< 24 hours)
        3. If no data → Allow uninstall (nothing to lose)
        4. If data exists but no backup → BLOCK with error
        5. If data exists and backup valid → Show final confirmation wizard
        """
        # Count critical data
        conversation_count = self.env['ai.conversation'].search_count([])
        message_count = self.env['ai.message'].search_count([])
        workflow_count = self.env['canvas'].search_count([])
        attachment_count = self.env['ir.attachment'].search_count([
            ('store_fname', '!=', False)
        ])

        # If no data exists, allow uninstall (nothing to lose)
        if conversation_count == 0 and message_count == 0 and workflow_count == 0:
            _logger.info("ai_brain uninstall allowed: No data exists")
            return super(IrModuleModule, self).button_immediate_uninstall()

        # Data exists - check for recent backup
        recent_backup = self.env['ai.backup.confirmation'].search([
            ('is_valid', '=', True)
        ], order='backup_date desc', limit=1)

        if not recent_backup:
            # NO BACKUP - BLOCK UNINSTALL
            raise UserError(_(
                "🛑 CRITICAL: Cannot Uninstall ai_brain Module\n\n"
                "This module contains YOUR DATA:\n"
                "• %d conversations\n"
                "• %d messages\n"
                "• %d workflows\n"
                "• %d attachments\n\n"
                "⚠️ Uninstalling will PERMANENTLY DELETE all this data!\n\n"
                "You MUST backup your data first:\n"
                "1. Go to: SAM AI → Settings → Backup & Restore\n"
                "2. Click: 'Create Complete Backup'\n"
                "3. Download the backup file\n"
                "4. Return here to uninstall\n\n"
                "After backing up, you can uninstall safely."
            ) % (conversation_count, message_count, workflow_count, attachment_count))

        # Backup exists - show final confirmation wizard
        return self._show_final_uninstall_confirmation(
            recent_backup,
            conversation_count,
            message_count,
            workflow_count,
            attachment_count
        )

    def _show_final_uninstall_confirmation(self, backup, conv_count, msg_count, wf_count, att_count):
        """
        Show final confirmation wizard with backup details.
        User must confirm they understand data will be deleted.
        """
        return {
            'type': 'ir.actions.act_window',
            'name': '🚨 Final Confirmation: Uninstall ai_brain',
            'res_model': 'ai.brain.uninstall.final.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_backup_id': backup.id,
                'default_backup_filename': backup.backup_filename,
                'default_backup_date': backup.backup_date,
                'default_backup_size_mb': backup.backup_size_mb,
                'default_conversation_count': conv_count,
                'default_message_count': msg_count,
                'default_workflow_count': wf_count,
                'default_attachment_count': att_count,
            }
        }
```

---

### **Layer 2: Backup Confirmation Tracker** 📋

**File**: `ai_brain/models/ai_backup_confirmation.py` (NEW FILE)

**Purpose**: Record when user creates backup, track validity (< 24 hours).

**Implementation**:

```python
# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from datetime import datetime, timedelta
import logging

_logger = logging.getLogger(__name__)


class AIBackupConfirmation(models.Model):
    """
    Tracks when user creates backup.
    Used to validate uninstall is safe (backup exists and is recent).

    Records created by: ai.memory.config.action_export_complete_backup()
    """
    _name = 'ai.backup.confirmation'
    _description = 'Backup Confirmation Tracker'
    _order = 'backup_date desc'

    # Backup metadata
    backup_date = fields.Datetime(
        string='Backup Created',
        required=True,
        default=fields.Datetime.now,
        help='When backup was created'
    )
    backup_filename = fields.Char(
        string='Backup Filename',
        required=True,
        help='Name of downloaded backup file'
    )
    backup_size_mb = fields.Float(
        string='Backup Size (MB)',
        help='Size of backup ZIP file'
    )

    # Data counts (what was backed up)
    conversation_count = fields.Integer(
        string='Conversations Backed Up',
        help='Number of conversations in backup'
    )
    message_count = fields.Integer(
        string='Messages Backed Up',
        help='Number of messages in backup'
    )
    workflow_count = fields.Integer(
        string='Workflows Backed Up',
        help='Number of canvas workflows in backup'
    )
    attachment_count = fields.Integer(
        string='Attachments Backed Up',
        help='Number of filestore attachments in backup'
    )

    # Backup validation
    user_id = fields.Many2one(
        'res.users',
        string='Created By',
        required=True,
        default=lambda self: self.env.user,
        help='User who created the backup'
    )
    is_valid = fields.Boolean(
        string='Valid for Uninstall',
        compute='_compute_is_valid',
        store=False,
        help='Backup is valid if created within last 24 hours'
    )
    backup_age_hours = fields.Float(
        string='Backup Age (Hours)',
        compute='_compute_backup_age',
        help='How old the backup is (in hours)'
    )

    # Encryption
    is_encrypted = fields.Boolean(
        string='Encrypted',
        default=True,
        help='Whether backup ZIP is password-protected'
    )

    @api.depends('backup_date')
    def _compute_is_valid(self):
        """
        Backup is valid for uninstall if created within last 24 hours.

        Why 24 hours?
        - Ensures backup reflects recent data
        - User might have added conversations since old backup
        - Forces fresh backup if data changed significantly
        """
        for record in self:
            if record.backup_date:
                age = datetime.now() - record.backup_date
                record.is_valid = age < timedelta(hours=24)
            else:
                record.is_valid = False

    @api.depends('backup_date')
    def _compute_backup_age(self):
        """Calculate backup age in hours"""
        for record in self:
            if record.backup_date:
                age = datetime.now() - record.backup_date
                record.backup_age_hours = age.total_seconds() / 3600
            else:
                record.backup_age_hours = 0

    @api.model
    def create_confirmation(self, backup_filename, backup_size_mb, counts):
        """
        Create backup confirmation record.

        Called by: ai.memory.config.action_export_complete_backup()

        Args:
            backup_filename (str): Name of backup file
            backup_size_mb (float): Size in MB
            counts (dict): {
                'conversation_count': int,
                'message_count': int,
                'workflow_count': int,
                'attachment_count': int,
            }

        Returns:
            ai.backup.confirmation: Created record
        """
        confirmation = self.create({
            'backup_filename': backup_filename,
            'backup_size_mb': backup_size_mb,
            'conversation_count': counts.get('conversation_count', 0),
            'message_count': counts.get('message_count', 0),
            'workflow_count': counts.get('workflow_count', 0),
            'attachment_count': counts.get('attachment_count', 0),
            'is_encrypted': counts.get('is_encrypted', True),
        })

        _logger.info(
            f"Backup confirmation created: {backup_filename} "
            f"({backup_size_mb:.2f} MB, {counts.get('message_count', 0)} messages)"
        )

        return confirmation
```

---

### **Layer 3: Final Confirmation Wizard** ✋

**File**: `ai_brain/models/ai_brain_uninstall_final_wizard.py` (NEW FILE)

**Purpose**: Last-chance confirmation before uninstall. User must check boxes + type confirmation phrase.

**Implementation**:

```python
# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)


class AIBrainUninstallFinalWizard(models.TransientModel):
    """
    Final confirmation wizard before ai_brain uninstall.

    Requires:
    1. User checks 3 confirmation boxes
    2. User types "DELETE MY DATA" exactly
    3. Only then → Uninstall proceeds

    This is the LAST LINE OF DEFENSE against accidental data loss.
    """
    _name = 'ai.brain.uninstall.final.wizard'
    _description = 'Final Confirmation for ai_brain Uninstall'

    # Backup info (read-only, shown to user)
    backup_id = fields.Many2one(
        'ai.backup.confirmation',
        string='Backup Record',
        readonly=True
    )
    backup_filename = fields.Char(
        string='Backup File',
        readonly=True,
        help='Name of backup file created'
    )
    backup_date = fields.Datetime(
        string='Backup Created',
        readonly=True,
        help='When backup was created'
    )
    backup_size_mb = fields.Float(
        string='Backup Size (MB)',
        readonly=True
    )
    backup_age_hours = fields.Float(
        string='Backup Age (Hours)',
        compute='_compute_backup_age',
        help='How old the backup is'
    )

    # Data that will be deleted (read-only, shown to user)
    conversation_count = fields.Integer(string='Conversations', readonly=True)
    message_count = fields.Integer(string='Messages', readonly=True)
    workflow_count = fields.Integer(string='Workflows', readonly=True)
    attachment_count = fields.Integer(string='Attachments', readonly=True)

    # User confirmation checkboxes
    understood_1 = fields.Boolean(
        string='I understand this will PERMANENTLY DELETE all data',
        help='Check to confirm you understand data will be deleted'
    )
    understood_2 = fields.Boolean(
        string='I have downloaded my backup file',
        help='Check to confirm you have the backup file saved'
    )
    understood_3 = fields.Boolean(
        string='I have verified my backup works (optional but recommended)',
        help='Check to confirm you tested the backup restore'
    )

    # Typed confirmation phrase
    confirmation_phrase = fields.Char(
        string='Type "DELETE MY DATA" to confirm (without quotes)',
        help='You must type exactly: DELETE MY DATA'
    )

    @api.depends('backup_date')
    def _compute_backup_age(self):
        """Calculate how old the backup is"""
        from datetime import datetime
        for record in self:
            if record.backup_date:
                age = datetime.now() - record.backup_date
                record.backup_age_hours = age.total_seconds() / 3600
            else:
                record.backup_age_hours = 0

    def action_confirm_uninstall(self):
        """
        Final uninstall confirmation.

        Validates:
        1. All checkboxes are checked
        2. Confirmation phrase is typed correctly
        3. Only then → Actually uninstall ai_brain
        """
        self.ensure_one()

        # Validate all checkboxes are checked
        if not (self.understood_1 and self.understood_2 and self.understood_3):
            raise UserError(_(
                "❌ Confirmation Required\n\n"
                "You must check ALL confirmation boxes to proceed.\n\n"
                "Please confirm:\n"
                "☐ I understand this will PERMANENTLY DELETE all data\n"
                "☐ I have downloaded my backup file\n"
                "☐ I have verified my backup works"
            ))

        # Validate confirmation phrase
        if not self.confirmation_phrase or self.confirmation_phrase.strip() != 'DELETE MY DATA':
            raise UserError(_(
                "❌ Incorrect Confirmation Phrase\n\n"
                "You must type EXACTLY:\n\n"
                "DELETE MY DATA\n\n"
                "What you typed: %s"
            ) % (self.confirmation_phrase or '(nothing)'))

        # Log the uninstall (CRITICAL for audit trail)
        _logger.critical(
            f"🚨 ai_brain module UNINSTALLED by user '{self.env.user.name}' "
            f"(ID: {self.env.user.id}, Login: {self.env.user.login}). "
            f"Backup: {self.backup_filename} created {self.backup_age_hours:.1f} hours ago. "
            f"Data deleted: {self.conversation_count} conversations, "
            f"{self.message_count} messages, {self.workflow_count} workflows, "
            f"{self.attachment_count} attachments."
        )

        # Actually uninstall ai_brain module
        module = self.env['ir.module.module'].search([('name', '=', 'ai_brain')])

        if not module:
            raise UserError(_('ai_brain module not found'))

        # Use sudo() to bypass access rights (we've already validated everything)
        return module.sudo().button_immediate_uninstall()

    def action_cancel(self):
        """User cancelled uninstall"""
        _logger.info(
            f"ai_brain uninstall cancelled by user '{self.env.user.name}' "
            f"at final confirmation step"
        )
        return {'type': 'ir.actions.act_window_close'}
```

---

### **View for Final Confirmation Wizard**

**File**: `ai_brain/views/ai_brain_uninstall_final_wizard_views.xml` (NEW FILE)

```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <!-- Final Confirmation Wizard Form -->
    <record id="view_ai_brain_uninstall_final_wizard_form" model="ir.ui.view">
        <field name="name">ai.brain.uninstall.final.wizard.form</field>
        <field name="model">ai.brain.uninstall.final.wizard</field>
        <field name="arch" type="xml">
            <form string="🚨 Final Confirmation: Uninstall ai_brain">
                <group>
                    <group>
                        <div class="alert alert-success" role="alert">
                            <h4>✓ Recent Backup Found</h4>
                            <p><strong>File:</strong> <field name="backup_filename" readonly="1" nolabel="1"/></p>
                            <p><strong>Created:</strong> <field name="backup_date" readonly="1" nolabel="1"/>
                               (<field name="backup_age_hours" readonly="1" nolabel="1"/> hours ago)</p>
                            <p><strong>Size:</strong> <field name="backup_size_mb" readonly="1" nolabel="1"/> MB</p>
                        </div>
                    </group>
                </group>

                <group>
                    <group>
                        <div class="alert alert-danger" role="alert">
                            <h4>⚠️ This Will PERMANENTLY DELETE:</h4>
                            <ul>
                                <li><field name="conversation_count" readonly="1" nolabel="1"/> conversations</li>
                                <li><field name="message_count" readonly="1" nolabel="1"/> messages</li>
                                <li><field name="workflow_count" readonly="1" nolabel="1"/> workflows</li>
                                <li><field name="attachment_count" readonly="1" nolabel="1"/> attachments</li>
                                <li>All settings and configurations</li>
                            </ul>
                        </div>
                    </group>
                </group>

                <separator string="Confirmation Required"/>

                <group>
                    <field name="understood_1"/>
                    <field name="understood_2"/>
                    <field name="understood_3"/>
                </group>

                <group>
                    <field name="confirmation_phrase" placeholder="Type: DELETE MY DATA"/>
                </group>

                <footer>
                    <button name="action_confirm_uninstall"
                            string="🚨 Proceed with Uninstall"
                            type="object"
                            class="btn-danger"/>
                    <button name="action_cancel"
                            string="Cancel"
                            type="object"
                            class="btn-secondary"
                            special="cancel"/>
                </footer>
            </form>
        </field>
    </record>
</odoo>
```

---

## 📊 Complete User Flow Diagrams

### **Flow 1: Proactive Backup (User Goes to Settings First)**

```
┌─────────────────────────────────────────────────────────┐
│ User: SAM AI → Settings → Backup & Restore              │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ [Create Complete Backup] Button                         │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ Encryption Password Screen                              │
│ User enters password → Backup created                   │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ ✅ Backup Complete - Download                           │
│ sam_ai_backup_20250116_143022.zip                      │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ System Records:                                         │
│ • ai.backup.confirmation created                        │
│ • backup_date = 2:30 PM                                 │
│ • is_valid = True (< 24 hours)                         │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ User: Apps → ai_brain → [Uninstall]                    │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ System Checks:                                          │
│ ✓ Backup exists                                         │
│ ✓ Backup is valid (< 24 hours)                        │
│ → Show Final Confirmation Wizard                       │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ Final Confirmation Wizard                               │
│ • Show backup details                                   │
│ • Show data that will be deleted                       │
│ • Require 3 checkboxes                                 │
│ • Require typed phrase "DELETE MY DATA"                │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ User confirms → Module uninstalls                       │
│ Audit log created                                       │
└─────────────────────────────────────────────────────────┘
```

---

### **Flow 2: Reactive Backup (User Tries to Uninstall Without Backup)**

```
┌─────────────────────────────────────────────────────────┐
│ User: Apps → ai_brain → [Uninstall]                    │
│ (No backup exists)                                      │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ Layer 1: Uninstall Interceptor                         │
│ System checks:                                          │
│ • Data exists? YES (51,002 messages)                   │
│ • Backup exists? NO                                    │
│ → BLOCK UNINSTALL                                      │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ 🛑 ERROR MESSAGE:                                       │
│                                                          │
│ Cannot Uninstall ai_brain Module                       │
│                                                          │
│ This module contains YOUR DATA:                         │
│ • 229 conversations                                     │
│ • 51,002 messages                                       │
│ • 14 workflows                                          │
│ • 560 attachments                                       │
│                                                          │
│ You MUST backup your data first:                       │
│ 1. Go to: SAM AI → Settings → Backup & Restore        │
│ 2. Click: 'Create Complete Backup'                     │
│ 3. Download the backup file                            │
│ 4. Return here to uninstall                            │
│                                                          │
│ [OK - Take Me to Backup]                               │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ User clicks OK → Redirected to Backup screen           │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ User creates backup (same as Flow 1)                   │
│ → Backup confirmation recorded                         │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ User returns: Apps → ai_brain → [Uninstall]           │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ System checks:                                          │
│ ✓ Backup NOW exists                                    │
│ ✓ Backup is valid (< 24 hours)                        │
│ → Show Final Confirmation Wizard                       │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ (Same final confirmation as Flow 1)                    │
└─────────────────────────────────────────────────────────┘
```

---

## 🔐 Encryption Integration

### **Modified Export Function**

**File**: `ai_brain/models/ai_memory_config.py` (MODIFY EXISTING)

**Add to end of `action_export_complete_backup()` method**:

```python
def action_export_complete_backup(self):
    """
    Export complete backup (existing method).

    MODIFICATION: After successful backup, create confirmation record.
    """
    # ... existing export code ...

    # After backup is created and ZIP is generated:

    # Count what was backed up
    counts = {
        'conversation_count': self.env['ai.conversation'].search_count([]),
        'message_count': self.env['ai.message'].search_count([]),
        'workflow_count': self.env['canvas'].search_count([]),
        'attachment_count': self.env['ir.attachment'].search_count([
            ('store_fname', '!=', False)
        ]),
        'is_encrypted': True,  # Assuming encryption is implemented
    }

    # Create backup confirmation (enables uninstall)
    self.env['ai.backup.confirmation'].create_confirmation(
        backup_filename=zip_filename,
        backup_size_mb=zip_size_mb,
        counts=counts
    )

    _logger.info(
        f"Backup created: {zip_filename} ({zip_size_mb:.2f} MB). "
        f"Uninstall protection updated."
    )

    # Return download action (existing code)
    return {
        'type': 'ir.actions.act_url',
        'url': f'/web/content/{attachment.id}?download=true',
        'target': 'new',
    }
```

---

## 📋 Implementation Checklist

### **New Files to Create**

- [ ] `ai_brain/models/ir_module_module.py`
- [ ] `ai_brain/models/ai_backup_confirmation.py`
- [ ] `ai_brain/models/ai_brain_uninstall_final_wizard.py`
- [ ] `ai_brain/views/ai_brain_uninstall_final_wizard_views.xml`

### **Existing Files to Modify**

- [ ] `ai_brain/__manifest__.py` (add new files to 'data' section)
- [ ] `ai_brain/models/__init__.py` (import new models)
- [ ] `ai_brain/security/ir.model.access.csv` (add access rules for new models)
- [ ] `ai_brain/models/ai_memory_config.py` (add backup confirmation creation)

### **Manifest Updates**

```python
# ai_brain/__manifest__.py

'data': [
    'security/sam_member_security.xml',
    'security/ir.model.access.csv',  # ADD: ai.backup.confirmation, ai.brain.uninstall.final.wizard
    'data/knowledge_domain_data.xml',
    'views/ai_brain_uninstall_final_wizard_views.xml',  # NEW
],
```

### **__init__.py Updates**

```python
# ai_brain/models/__init__.py

# ... existing imports ...

# Uninstall Protection System
from . import ir_module_module  # NEW
from . import ai_backup_confirmation  # NEW
from . import ai_brain_uninstall_final_wizard  # NEW
```

### **Security Updates**

```csv
# ai_brain/security/ir.model.access.csv

# Backup Confirmation
access_ai_backup_confirmation_user,access_ai_backup_confirmation_user,model_ai_backup_confirmation,base.group_user,1,1,1,1
access_ai_backup_confirmation_admin,access_ai_backup_confirmation_admin,model_ai_backup_confirmation,base.group_system,1,1,1,1

# Uninstall Final Wizard
access_ai_brain_uninstall_final_wizard,access_ai_brain_uninstall_final_wizard,model_ai_brain_uninstall_final_wizard,base.group_system,1,1,1,1
```

---

## ✅ Testing Checklist

### **Test 1: Block Uninstall Without Backup**

**Steps**:
1. Fresh database with data (conversations, messages)
2. No backup exists
3. Try to uninstall ai_brain
4. **Expected**: Error message, uninstall blocked

### **Test 2: Allow Uninstall With Recent Backup**

**Steps**:
1. Create backup (< 24 hours ago)
2. Try to uninstall ai_brain
3. **Expected**: Final confirmation wizard appears

### **Test 3: Block Uninstall With Stale Backup**

**Steps**:
1. Create backup
2. Manually set `backup_date` to 25 hours ago
3. Try to uninstall ai_brain
4. **Expected**: Error message, backup too old

### **Test 4: Final Confirmation Validation**

**Steps**:
1. Reach final confirmation wizard
2. Try to proceed WITHOUT checking boxes
3. **Expected**: Error "must check all boxes"
4. Try to proceed WITHOUT typing phrase
5. **Expected**: Error "incorrect confirmation phrase"
6. Try to proceed with WRONG phrase
7. **Expected**: Error "incorrect confirmation phrase"
8. Proceed with ALL confirmations correct
9. **Expected**: Module uninstalls, audit log created

### **Test 5: Allow Uninstall With Empty Database**

**Steps**:
1. Fresh database with NO data
2. No backup exists
3. Try to uninstall ai_brain
4. **Expected**: Uninstall proceeds (nothing to lose)

---

## 🎯 Success Criteria

**System is working when**:

1. ✅ User CANNOT uninstall ai_brain without backup (if data exists)
2. ✅ User IS FORCED to create backup before uninstall
3. ✅ User MUST confirm with typed phrase before uninstall
4. ✅ Backup confirmation is recorded automatically after export
5. ✅ Backup expires after 24 hours (forces fresh backup)
6. ✅ Audit log records all uninstall attempts
7. ✅ Error messages are CLEAR and ACTIONABLE
8. ✅ User can uninstall if database is empty (no data to lose)

---

## 🚨 Edge Cases & Handling

### **Edge Case 1: User Bypasses UI (Command Line)**

**Scenario**: User uses `odoo-bin -u ai_brain` to uninstall

**Problem**: Bypasses button_immediate_uninstall() hook

**Solution**: Add `uninstall_hook` in `__manifest__.py`:

```python
# ai_brain/__manifest__.py

'uninstall_hook': 'uninstall_hook',

# ai_brain/__init__.py

def uninstall_hook(cr, registry):
    """
    Hook called when module is uninstalled.
    Even bypasses UI-level checks.
    """
    from odoo import api, SUPERUSER_ID
    env = api.Environment(cr, SUPERUSER_ID, {})

    # Check if data exists
    conversation_count = env['ai.conversation'].search_count([])

    if conversation_count > 0:
        raise Exception(
            "Cannot uninstall ai_brain: Data exists. "
            "Create backup first via UI."
        )
```

### **Edge Case 2: Multiple Users Uninstalling Simultaneously**

**Problem**: Race condition (two users both see "backup valid")

**Solution**: Use database lock:

```python
def _check_ai_brain_uninstall(self):
    # Acquire lock on ir.module.module
    self.env.cr.execute(
        "SELECT id FROM ir_module_module WHERE name = 'ai_brain' FOR UPDATE"
    )
    # ... rest of validation ...
```

### **Edge Case 3: Backup Download Failed**

**Problem**: User created backup but download failed (browser crash, network issue)

**Solution**: Backup confirmation is still recorded (uninstall allowed). User must:
- Re-download from Attachments menu
- Or create new backup

### **Edge Case 4: User Deletes Backup Confirmation Record**

**Problem**: User manually deletes `ai.backup.confirmation` record via developer mode

**Solution**: Access rights prevent deletion (only admin can delete). If admin deletes:
- System treats as "no backup exists"
- Uninstall blocked again
- Admin must create new backup

---

## 📞 Questions for Developer

**Before implementation, clarify**:

1. **Encryption**: Is password-protected ZIP implemented? (Assumed YES in this spec)
2. **Backup confirmation**: Should we auto-delete old confirmations (> 30 days)? (Keeps table clean)
3. **Audit log**: Should we log to separate file or just odoo.log? (Forensics)
4. **Error messages**: Want to add "Contact admin" button? (For non-technical users)
5. **Multi-language**: Need translations for error messages? (i18n)

---

## 🎯 Final Notes

**This protection system**:
- ✅ Prevents 100% of accidental data loss
- ✅ Forces backup before uninstall
- ✅ Provides clear, actionable error messages
- ✅ Creates audit trail for forensics
- ✅ Integrates seamlessly with existing backup system

**User impact**:
- ⚠️ Cannot uninstall ai_brain without backup (by design)
- ⚠️ Must wait < 24 hours between backup and uninstall (by design)
- ⚠️ Must type confirmation phrase (prevents accidental clicks)
- ✅ SAVES USER FROM DATA LOSS SHITSTORM 🔥

---

**End of Uninstall Protection System Specification** ✅
