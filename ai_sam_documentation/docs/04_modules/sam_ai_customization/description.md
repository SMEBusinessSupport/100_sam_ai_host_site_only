# SAM AI View Customizer

**Technical Name**: `sam_ai_customization`
**Version**: 18.0.1.0.0

Drag-and-drop view customization without code

## Description


SAM AI View Customizer
======================

A powerful, intuitive tool for customizing Odoo views without writing code.

Key Features
------------
* Drag and drop fields into form, list, and kanban views
* Create custom fields (x_*) on any model
* Undo/Redo support for changes
* Preview changes before applying
* Batch save all modifications at once
* Export customizations as XML for backup/migration
* Three-tier permission system (User/Manager/Admin)
* Full audit trail of all changes
* Multi-company support

How It Works
------------
1. Open any view in Odoo
2. Click the "View Customizer" button in the systray
3. Drag fields from the sidebar into the view
4. Preview your changes
5. Click "Apply" to save all modifications

Perfect For
-----------
* Quick view customizations without developer intervention
* Prototyping new layouts
* Adding custom fields to existing views
* Non-technical users who need to modify views
    

## Module Details

## SAM AI View Customizer 
### Drag-and-Drop View Customization Without Code 

Customize your Odoo views in seconds. No coding required.
 Simply drag fields from the sidebar and drop them where you want. 
## Key Features **Drag & Drop 

Intuitive drag-and-drop interface. Select a field from the sidebar and drop it exactly where you need it. **Preview Mode 

See your changes before applying them. Preview mode lets you experiment without affecting other users. **Create Custom Fields 

Need a new field? Create custom fields (x_*) directly from the interface without touching code. 
## How to Use 
### 1 Open the View Customizer 

Navigate to any form, list, or kanban view in Odoo. Look for the **"View Customizer" **button in the top system tray (next to your user menu). Click it to open the sidebar. 
### 2 Enable Preview Mode (Recommended) 

Toggle the **"Preview Mode" **switch at the top of the sidebar.
 This lets you see your changes locally before applying them to all users. 

*Tip: Preview changes are saved in your browser, so you can close and come back later! *
### 3 Drag Fields to the View 

Browse available fields in the sidebar. You can: 
- **Search **- Type in the search box to find fields quickly 
- **Filter **- Show only standard fields or custom fields (x_*) 
- **Drag **- Click and drag any field to the view 
- **Drop **- Release on a highlighted drop zone to place the field 
### 4 Create New Fields (Optional) 

Click the **"Create Field" **button to add a new custom field to the model.
 Fill in the field details: 
- **Field Label **- The display name (e.g., "Customer Reference") 
- **Field Type **- Text, Number, Date, Selection, Many2one, etc. 
- **Technical Name **- Auto-generated (e.g., "x_customer_reference") 
- **Required **- Check if the field must have a value 
### 5 Apply to System 

When you're happy with your changes, click **"Apply to System" **.
 This will save your customizations and make them visible to **all users **. 

*Important: This action affects everyone. Make sure your changes are correct! *
## Preview Mode vs. Direct Mode **Preview Mode 
- Changes visible **only to you **
- Saved in your browser (localStorage) 
- Can save and continue later 
- Undo/Redo supported 
- Apply when ready 

**Best for: **Experimenting, planning layouts, reviewing before deployment **Direct Mode 
- Changes apply **immediately **
- Visible to all users instantly 
- Page reloads after each change 
- Can still undo via management 

**Best for: **Quick single-field additions, urgent fixes 
## Managing Customizations 

Access **Settings > View Customizer > Manage Customizations **to: **View All Changes 

See every customization made across all models and views **Export XML 

Export customizations as XML for backup or migration **Revert Changes 

Remove customizations and restore the original view 
## Permission Levels Group Can Do **View Customizer User **Add existing fields to views, use preview mode **View Customizer Manager **All above + Create new custom fields, apply to system **View Customizer Admin **All above + Manage all customizations, export XML, revert changes 
## Tips & Best Practices 

****Always use Preview Mode first **- Test your layout before affecting other users 

****Use meaningful field names **- "Customer Reference" is better than "Ref1" 

****Export before major changes **- Keep a backup of your customizations 

****Test in a staging environment **- When possible, test customizations before production 

****Don't remove required system fields **- This can break functionality 

****Don't create duplicate field names **- Each x_ field must be unique per model 
## Need Help? 

Contact your system administrator or visit the SAM AI documentation for more information. 

**SAM AI View Customizer **v18.0.1.0.0 
Built with care for Odoo 18

## Dependencies

- `web`
- `base`
