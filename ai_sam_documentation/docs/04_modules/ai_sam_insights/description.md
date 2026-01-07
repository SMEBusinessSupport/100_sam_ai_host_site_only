# SAM AI Insights

**Technical Name**: `ai_sam_insights`
**Version**: 18.0.1.0

Ecosystem Intelligence - Track, Trace, and Analyze the SAM AI Codebase

## Description


SAM AI Insights - Ecosystem Intelligence Tool
==============================================

A comprehensive analysis tool that knows EVERYTHING about your SAM AI ecosystem.

**What It Detects:**

Dangling References:
- Views referencing non-existent fields
- Actions pointing to deleted models
- Menu items with broken actions
- JS components calling undefined Python methods

Redundant Code:
- Multiple models doing similar things (similarity scoring)
- Duplicate utility functions across modules
- CSS classes defined multiple times
- JS functions with same logic, different names

Orphaned Assets:
- JS files not in any asset bundle
- CSS not imported anywhere
- Python files not imported in __init__.py
- XML views never rendered

Relationship Mapping:
- Model → Views → Actions → Menus (full trace)
- Field usage across all views
- JS ↔ Python controller mappings
- Module dependency graph

**Features:**
- Static analysis (AST parsing for Python, XML parsing for views)
- Runtime analysis (queries Odoo registry)
- Duplicate detection with similarity scoring
- HTML/JSON report generation
- Dashboard with ecosystem health metrics
- Scheduled weekly scans
- Integration with SAM Chat for natural language queries

**Architecture:**
Scanner → Analyzer → Reporter → Dashboard
    

## Module Details

# SAM AI Insights 

**Ecosystem Intelligence Tool **- Know EVERYTHING about your SAM AI codebase 
## What It Detects 
### Duplicate Code 
- Similar models with high overlap 
- Duplicate functions across modules 
- CSS classes defined multiple times 
- Renamed components (_old, _v2, backup) 
### Orphaned Components 
- Models with no views 
- Actions with no menus 
- JS/CSS files not in bundles 
- Python files not imported 
### Dangling References 
- Views referencing missing fields 
- Actions pointing to deleted models 
- Broken menu item references 
- Invalid model relations 
### Relationship Mapping 
- Model → View → Action → Menu traces 
- Field usage across all views 
- Module dependency graph 
- Inheritance chains 
## Features 
- **Static Analysis: **Python AST parsing, XML view parsing, JS/CSS scanning 
- **Runtime Analysis: **Odoo registry queries for live validation 
- **Health Score: **0-100 ecosystem health metric 
- **HTML Reports: **Beautiful, shareable reports 
- **JSON Export: **Full data export for external tools 
- **Scheduled Scans: **Weekly automated analysis 
- **Dashboard: **Kanban-style overview of scan results 
## Usage 
- Install the `ai_sam_insights `module 
- Navigate to **SAM Insights → Ecosystem Health **
- Click **Run Quick Scan **to analyze SAM AI modules 
- Review findings and recommendations 
- Click **View Report **for the full HTML report 
## Architecture ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│ SCANNER │───▶│ ANALYZER │───▶│ REPORTER │───▶│ DASHBOARD │
└─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘
 │ │ │ │
 ▼ ▼ ▼ ▼
 • Python AST • Duplicates • HTML Report • Kanban View
 • XML Parser • Orphans • JSON Export • Health Score
 • JS/CSS Scan • Relations • Findings List • Issue Tracking

## Dependencies

- `base`
- `web`
- `ai_sam_base`
