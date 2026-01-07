# AI SAM Suite - Python Dependencies Analysis

**Date:** 2025-11-04
**Location:** C:\Working With AI\ai_sam\ai_sam\

---

## Complete Dependency List

### CRITICAL (Required for Core Features)

| Package | Version | Used By | Purpose |
|---------|---------|---------|---------|
| **anthropic** | >=0.18.0 | ai_brain, ai_sam | Claude AI API integration |
| **openai** | >=1.0.0 | ai_youtube_transcribe | OpenAI GPT + Whisper API |
| **requests** | >=2.28.0 | ai_sam_lead_generator | HTTP requests, web scraping |

### IMPORTANT (Memory System Features)

| Package | Version | Used By | Purpose |
|---------|---------|---------|---------|
| **chromadb** | >=0.4.0 | ai_brain | Vector database (semantic search) |
| **sentence-transformers** | >=2.2.0 | ai_brain | Text embeddings (all-mpnet-base-v2) |
| **psycopg2-binary** | >=2.9.0 | ai_brain | PostgreSQL + Apache AGE graph DB |

### OPTIONAL (Specific Modules)

| Package | Version | Used By | Purpose |
|---------|---------|---------|---------|
| **beautifulsoup4** | >=4.11.0 | ai_sam_lead_generator | HTML parsing (web scraping) |
| **lxml** | >=4.9.0 | ai_sam_lead_generator | XML/HTML parser |
| **GitPython** | >=3.1.0 | github_app | Git repository operations |
| **yt-dlp** | >=2023.0.0 | ai_youtube_transcribe | YouTube video downloading (commented out) |

---

## Dependencies by Module

### ai_brain (Core Data Layer)
```python
# Core AI
import anthropic           # Claude API
import openai             # OpenAI API (optional)

# Memory System
import chromadb           # Vector DB
from sentence_transformers import SentenceTransformer  # Embeddings
import psycopg2           # Graph DB (Apache AGE)

# Standard library (already in Python)
import requests
import json
import logging
```

### ai_sam (Core Framework)
```python
import anthropic          # Claude API
# (Mostly uses Odoo's built-in libraries)
```

### ai_sam_workflows (N8N Workflows)
```python
# No external Python dependencies
# (Uses JavaScript on frontend)
```

### ai_sam_lead_generator (Web Scraping)
```python
import requests           # HTTP requests
from bs4 import BeautifulSoup4  # HTML parsing
import lxml               # XML parser
```

### github_app (GitHub Integration)
```python
import git                # GitPython
```

### ai_youtube_transcribe (YouTube)
```python
import openai             # Whisper API
# import yt_dlp          # YouTube downloader (optional)
```

---

## How Odoo Detects Dependencies

### In __manifest__.py:
```python
{
    'name': 'Module Name',
    'external_dependencies': {
        'python': ['anthropic', 'chromadb', 'sentence-transformers'],
        'bin': []  # System binaries (e.g., wkhtmltopdf)
    },
}
```

**What Odoo does:**
1. Checks if packages in `external_dependencies` are installed
2. If missing, shows warning in Apps menu
3. Module install fails with error message

**User needs to:**
```bash
pip install anthropic chromadb sentence-transformers
```

---

## Installation Instructions for Users

### Option 1: Install All at Once (Recommended)
```bash
pip install -r C:\Working With AI\ai_sam\ai_sam\requirements.txt
```

### Option 2: Install Individual Packages
```bash
# Core AI APIs
pip install anthropic openai

# Memory System (optional but recommended)
pip install chromadb sentence-transformers psycopg2-binary

# Web Scraping (if using lead generator)
pip install beautifulsoup4 lxml

# Git Integration (if using GitHub app)
pip install GitPython
```

### Option 3: Minimal Install (Just AI Chat)
```bash
pip install anthropic
# Only Claude AI chat will work
# Memory, workflows, scraping disabled
```

---

## For Installer (What to Bundle)

### Must Include (Core Features):
```
anthropic-0.18.0.whl
openai-1.0.0.whl
requests-2.28.0.whl
```

### Recommended (Memory Features):
```
chromadb-0.4.0.whl
sentence-transformers-2.2.0.whl
psycopg2-binary-2.9.0.whl
```

### Optional (Advanced Features):
```
beautifulsoup4-4.11.0.whl
lxml-4.9.0.whl
GitPython-3.1.0.whl
```

---

## Size Estimation

| Package | Wheel Size | With Dependencies |
|---------|------------|-------------------|
| anthropic | ~50KB | ~500KB |
| openai | ~100KB | ~800KB |
| chromadb | ~5MB | ~50MB |
| sentence-transformers | ~500KB | ~2GB (models!) |
| psycopg2-binary | ~3MB | ~3MB |
| beautifulsoup4 | ~100KB | ~200KB |
| lxml | ~5MB | ~5MB |
| GitPython | ~500KB | ~2MB |
| **TOTAL** | **~14MB** | **~2.5GB** |

**Note:** sentence-transformers downloads ML models (~2GB) on first use!

---

## Installer Strategy

### Strategy 1: Bundle Python Wheels
**Pros:**
✅ Offline installation
✅ Faster setup
✅ No internet required

**Cons:**
❌ Larger installer (~2.5GB with models)
❌ Platform-specific (Windows only)

### Strategy 2: Download During Install
**Pros:**
✅ Smaller installer (~320MB)
✅ Always latest versions

**Cons:**
❌ Requires internet
❌ Slower installation
❌ Can fail if PyPI down

### Strategy 3: Hybrid (Recommended)
**Include in installer:**
- anthropic, openai (essential, small)
- psycopg2-binary (essential, medium)

**Download during install:**
- chromadb (optional, large)
- sentence-transformers (optional, huge)
- beautifulsoup4, lxml (optional, small)

**Result:**
- Installer: ~350MB
- Basic features work offline
- Advanced features download on-demand

---

## For public_ai_sam (Free Version)

**Minimal dependencies:**
```python
# requirements_basic.txt
anthropic>=0.18.0          # Claude API only
```

**Size:** ~500KB total

---

## For ai_sam_enterprise (Paid Version)

**Full dependencies:**
```python
# requirements_enterprise.txt
anthropic>=0.18.0
openai>=1.0.0
chromadb>=0.4.0
sentence-transformers>=2.2.0
psycopg2-binary>=2.9.0
beautifulsoup4>=4.11.0
lxml>=4.9.0
GitPython>=3.1.0
```

**Size:** ~2.5GB total (with ML models)

---

## Detection Script for Installer

**Check what's already installed:**

```python
# check_dependencies.py
import sys

def check_package(package_name):
    try:
        __import__(package_name)
        return True
    except ImportError:
        return False

packages = {
    'anthropic': 'Claude AI',
    'openai': 'OpenAI API',
    'chromadb': 'Vector Database',
    'sentence_transformers': 'Text Embeddings',
    'psycopg2': 'PostgreSQL',
    'bs4': 'BeautifulSoup',
    'git': 'GitPython',
}

print("Checking dependencies...")
missing = []
for pkg, name in packages.items():
    if check_package(pkg):
        print(f"✅ {name} ({pkg})")
    else:
        print(f"❌ {name} ({pkg}) - MISSING")
        missing.append(pkg)

if missing:
    print(f"\nMissing {len(missing)} packages. Install with:")
    print(f"pip install {' '.join(missing)}")
else:
    print("\n✅ All dependencies installed!")
```

---

## Recommended for Installer

### Phase 1: Basic Installer (Portable ZIP)
**Bundle:**
- anthropic (essential, 500KB)
- No other dependencies

**User can:**
- Basic AI chat works
- Download optional packages later

### Phase 2: Full Installer (.exe)
**Bundle:**
- anthropic, openai (1.5MB)
- psycopg2-binary (3MB)

**Download during install:**
- chromadb (50MB) - optional checkbox
- sentence-transformers (2GB) - optional checkbox

**Wizard page:**
```
┌────────────────────────────────────┐
│  Optional Features                 │
│                                    │
│  □ Memory System (50MB download)   │
│     • Semantic search              │
│     • Conversation history         │
│                                    │
│  □ ML Models (2GB download)        │
│     • Text embeddings              │
│     • Advanced search              │
│                                    │
│         [Back]    [Next]           │
└────────────────────────────────────┘
```

---

## Summary

**Core dependencies (must have):**
- anthropic (Claude API)

**Important dependencies (recommended):**
- chromadb (memory system)
- psycopg2 (graph database)

**Optional dependencies:**
- sentence-transformers (advanced search)
- beautifulsoup4 (web scraping)
- GitPython (GitHub integration)

**Total size range:**
- Minimal: ~500KB (just anthropic)
- Full: ~2.5GB (all packages + ML models)

**Created:**
- ✅ requirements.txt in ai_sam folder
- ✅ This analysis document

---

**Want me to update the installer plan to include dependency installation?**
