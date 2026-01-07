# SAM UI Theme

**Technical Name**: `sam_ui_theme`
**Version**: 18.0.19.0.0

SAM AI branded theme with customizable colors and modern styling

## Description


SAM UI Theme
============

A beautiful, modern theme for Odoo 18 that provides:

* **Customizable Colors** - Full control over brand colors, navbar, and bling line
* **Bling Line** - Animated gradient bar on the app menu overlay
* **Modern Styling** - Clean, professional look with SAM brand colors
* **Theme Presets** - Quick presets (SAM Default, Dark, Ocean, Forest, Sunset, Purple)
* **Typography Options** - Choose from multiple font families
* **Card Side Color** - Configurable left border color on kanban cards

Features:
- Customizable animated gradient bling line
- Theme settings page (Settings > SAM AI Theme)
- Modern button and form styling
- Enhanced navbar and dropdown menus
- Beautiful fullscreen app menu overlay
- SAM brand color palette throughout
- Kanban card side color customization
    

## Module Details

## SAM UI Theme 
### A Modern, Customizable Theme for Odoo 18 
## Key Features **Customizable Colors 

Full control over your brand colors including primary, secondary, and accent colors. Customize navbar background and text colors to match your brand identity. **Animated Bling Line 

Eye-catching animated gradient bar on the app menu overlay. Choose your own gradient colors or disable it entirely. **Theme Presets 

Quick-start with beautiful presets: SAM Default (Blue & Gold), SAM Dark, Ocean Blue, Forest Green, Sunset Orange, and Royal Purple. **Typography Options 

Choose from multiple font families for headings and body text: Plus Jakarta Sans, DM Sans, Inter, Roboto, or System Default. 
## Theme Presets **SAM Default **
Blue & Gold **SAM Dark **
Dark Mode **Ocean Blue **
Cool Blues **Forest Green **
Natural Greens **Sunset Orange **
Warm Tones **Royal Purple **
Elegant Purple 
## How to Configure Access Theme Settings 
- Navigate to **Settings **from the main menu 
- Find **SAM AI Theme **in the left sidebar 
- Configure your preferences: 
- **Theme Preset: **Quick-start with a predefined color scheme 
- **Brand Colors: **Customize primary, secondary, and accent colors 
- **Navigation Bar: **Set navbar background and text colors 
- **Bling Line: **Enable/disable and customize the animated gradient 
- **Typography: **Choose display and body fonts 
- **UI Elements: **Adjust button and card corner roundness 
- Click **Save **to apply your changes 
- Refresh your browser (Ctrl+Shift+R) to see the new theme 
## Customization Options Setting Description Default **Primary Color **Main brand color for buttons, links, and active states #4A90E2 **Secondary Color **Accent color for highlights and badges #F4C430 **Accent Color **Third accent color for variety #FF5AC4 **Navbar Background **Navigation bar background color #4A90E2 **Navbar Text **Navigation bar text color #FFFFFF **Bling Line **Animated gradient bar on app menu overlay Enabled (3 customizable colors) **Display Font **Font for headings and titles Plus Jakarta Sans **Body Font **Font for body text and content DM Sans **Button Roundness **Corner radius for buttons 8px (Rounded) **Card Roundness **Corner radius for cards and panels 16px (More Rounded) 
## Technical Details **Architecture 
- Integrates with Odoo 18 Settings framework 
- Uses `ir.config_parameter `for storing preferences 
- Dynamic CSS generation via controller endpoint 
- OWL components for enhanced app menu 
- SCSS variables for consistent theming **Module Structure 
- `models/ `- res.config.settings extension 
- `views/ `- Settings view inheritance 
- `controllers/ `- Dynamic CSS endpoint 
- `static/src/scss/ `- Theme stylesheets 
- `static/src/components/ `- OWL components 
## Dependencies 

This module requires the following Odoo modules: web 
## Support & Contact 

**SAM AI **by Total Lock Solutions 
https://sam-ai.co 

Licensed under LGPL-3.0 or later

## Dependencies

- `web`
