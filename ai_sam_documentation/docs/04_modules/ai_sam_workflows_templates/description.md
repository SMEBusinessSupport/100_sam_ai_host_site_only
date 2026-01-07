# SAM AI Workflow Templates

**Technical Name**: `ai_sam_workflows_templates`
**Version**: 18.0.1.0.0

Reusable Workflow Template Library for SAM AI

## Description


SAM AI Workflow Templates
=========================

Standalone module providing reusable workflow templates for SAM AI Workflows.

Features
--------
* Template creation and management
* Template categories (CRM, Marketing, Project, etc.)
* Template tags for organization
* Template validation
* Template marketplace visibility
* N8N workflow import as templates
* Usage tracking and statistics

Architecture
------------
This module:
* Defines workflow.template and workflow.template.tag models
* Extends canvas model with template_id field
* Provides create_from_template() method on canvas
* Integrates into Workflows menu structure

Dependencies
------------
* ai_sam_workflows_base: Provides canvas model
* ai_sam_workflows: Provides menu structure (for menu integration)
* mail: For mail.thread inheritance

Extraction History
------------------
* Extracted from ai_sam_workflows_base (models) and ai_sam_workflows (views)
* Date: 2024-12-19
* Purpose: Standalone template library that can be installed/uninstalled independently
    

## Dependencies

- `ai_sam_workflows_base`
- `ai_sam_workflows`
- `mail`
