# SAM AI Business Suite - Versioning Scheme

## Version Format: `18.1.0.0`

### Smart Versioning that Tells the Story

Our version numbers are designed to instantly tell you what's inside:

```
18 . 1 . 0 . 0
│    │   │   │
│    │   │   └─── Build/Revision Number (bug fixes, patches)
│    │   └─────── Minor SAM AI Version (new features, improvements)
│    └─────────── Major SAM AI Version (significant releases)
└──────────────── Odoo Base Version (engine version)
```

## Version Number Breakdown

### Position 1: Odoo Base Version (18)
**What it tells you:** Which Odoo engine version powers SAM AI

- `18.x.x.x` = Built on Odoo 18
- `17.x.x.x` = Built on Odoo 17 (if we backport)
- `19.x.x.x` = Built on Odoo 19 (future)

**Why it matters:**
- Module compatibility
- Feature availability
- API compatibility
- Migration planning

### Position 2: SAM AI Major Version (1)
**What it tells you:** Major SAM AI release number

- `18.1.x.x` = First major SAM AI release on Odoo 18
- `18.2.x.x` = Second major SAM AI release (significant new features)
- `18.3.x.x` = Third major SAM AI release

**When to increment:**
- Major new SAM AI modules added
- Significant architectural changes
- Breaking changes to SAM AI features
- Major milestones (SAM AI Brain, SAM AI Core, etc.)

### Position 3: SAM AI Minor Version (0)
**What it tells you:** Minor updates and feature additions

- `18.1.0.x` = Initial release
- `18.1.1.x` = First feature update
- `18.1.2.x` = Second feature update

**When to increment:**
- New SAM AI features added
- New modules in app store
- Installer improvements
- Non-breaking enhancements

### Position 4: Build/Revision (0)
**What it tells you:** Bug fixes and patches

- `18.1.0.0` = Initial build
- `18.1.0.1` = First patch
- `18.1.0.2` = Second patch

**When to increment:**
- Bug fixes
- Security patches
- Documentation updates
- Minor tweaks

## Version History

### 18.1.0.0 - Initial Release (Current)
**Release Date:** [TBD]

**What's Included:**
- SAM AI Business Suite installer
- Odoo 18 engine
- Lightweight-core (16 full + 641 placeholders)
- SAM AI App Store (`ai_sam_github_installer`)
- Intelligent installation wizard
- Smart detection system
- PostgreSQL 15 database
- Python 3.12 isolated environment

**Features:**
- ✅ Hybrid installer architecture
- ✅ GitHub-powered app ecosystem
- ✅ Minimal footprint (50MB)
- ✅ On-demand module installation
- ✅ Automatic system detection
- ✅ Database preservation
- ✅ Port conflict resolution
- ✅ Side-by-side installation support

## Future Versioning Examples

### 18.1.1.0 - First Feature Update
**Potential additions:**
- Enhanced SAM AI App Store UI
- New app categories
- Improved search functionality
- Additional SAM AI modules

### 18.2.0.0 - SAM AI Core Release
**Major milestone:**
- SAM AI Core module integration
- AI-powered automation features
- Enhanced intelligence layer
- New SAM AI capabilities

### 18.3.0.0 - SAM AI Brain Release
**Major milestone:**
- SAM AI Brain module integration
- Advanced AI features
- Workflow automation
- Learning capabilities

### 19.1.0.0 - Odoo 19 Migration
**Major upgrade:**
- Updated to Odoo 19 engine
- SAM AI 1.x features maintained
- Enhanced compatibility
- New Odoo 19 capabilities

## Reading Version Numbers

### Quick Reference
| Version | Meaning |
|---------|---------|
| `18.1.0.0` | Initial SAM AI release on Odoo 18 |
| `18.1.0.5` | Fifth patch to initial release |
| `18.1.1.0` | First feature update |
| `18.2.0.0` | Major SAM AI update (new major features) |
| `19.1.0.0` | SAM AI on Odoo 19 |

### Real-World Scenarios

**Scenario 1: Bug Fix**
- Current: `18.1.0.0`
- Fix installer port detection bug
- New: `18.1.0.1`

**Scenario 2: New App Store Feature**
- Current: `18.1.0.1`
- Add app ratings and reviews
- New: `18.1.1.0`

**Scenario 3: SAM AI Core Launch**
- Current: `18.1.5.3`
- Release SAM AI Core module
- New: `18.2.0.0`

**Scenario 4: Odoo 19 Upgrade**
- Current: `18.3.2.5`
- Upgrade to Odoo 19
- New: `19.1.0.0`

## Benefits of This Scheme

### For Users
✓ **Instant Recognition**: See what Odoo version you're on
✓ **Clear Updates**: Know if it's a bug fix or new feature
✓ **Compatibility**: Understand module compatibility at a glance
✓ **Migration Planning**: Know when major upgrades are needed

### For Developers
✓ **Semantic Meaning**: Each number tells a story
✓ **Support Clarity**: Quickly identify what's installed
✓ **Change Tracking**: Clear upgrade paths
✓ **Compatibility Management**: Easy version comparison

### For Support
✓ **Quick Diagnosis**: Version number reveals configuration
✓ **Issue Tracking**: Link bugs to specific builds
✓ **Feature Availability**: Know what features exist in each version
✓ **Upgrade Guidance**: Clear upgrade paths

## Compatibility Matrix

| SAM AI Version | Odoo Version | Python | PostgreSQL | Status |
|----------------|--------------|--------|------------|--------|
| `18.1.x.x` | Odoo 18.0 | 3.12 | 15 | Current |
| `18.2.x.x` | Odoo 18.0 | 3.12 | 15 | Planned |
| `19.1.x.x` | Odoo 19.0 | 3.12 | 15 | Future |

## Version Comparison

### How to Compare Versions

**Example 1:**
- `18.1.0.0` vs `18.1.0.5` → Newer has 5 patches
- **Upgrade?** Optional (bug fixes)

**Example 2:**
- `18.1.0.0` vs `18.1.5.0` → Newer has 5 feature updates
- **Upgrade?** Recommended (new features)

**Example 3:**
- `18.1.x.x` vs `18.2.0.0` → Major SAM AI update
- **Upgrade?** Recommended (significant improvements)

**Example 4:**
- `18.x.x.x` vs `19.x.x.x` → Odoo engine upgrade
- **Upgrade?** Plan carefully (major migration)

## Release Cadence (Planned)

- **Patches** (`x.x.x.N`): As needed (bug fixes)
- **Minor Updates** (`x.x.N.0`): Monthly (features)
- **Major Updates** (`x.N.0.0`): Quarterly (major features)
- **Engine Upgrades** (`N.x.x.x`): Annually (Odoo version)

## Summary

The version number `18.1.0.0` instantly tells you:
- ✅ Built on Odoo 18 (`18`)
- ✅ First major SAM AI release (`1`)
- ✅ Initial feature set (`0`)
- ✅ Original build (`0`)

No guesswork. No confusion. Just clarity.

---

**Current Version:** `18.1.0.0`
**Installer Filename:** `SAM_AI_Premium_Business_Suite_Setup.exe`
**Last Updated:** 2025-01-07
