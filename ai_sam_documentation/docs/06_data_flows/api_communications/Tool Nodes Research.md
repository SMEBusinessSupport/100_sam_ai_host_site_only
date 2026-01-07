# Tool Nodes Research Report

**Date:** September 30, 2025
**Researcher:** Claude (AI Assistant)
**Project:** The AI Automator - N8N Integration Phase 3
**Status:** Investigation Complete - Findings Documented for Future Implementation

---

## Executive Summary

This report documents the investigation into N8N's "Tool" node pattern, specifically the "ActiveCampaign Tool" node observed in the N8N UI. The research aimed to understand the Tool wrapper architecture and determine if we should implement Tool node support in our Odoo module.

**Key Finding:** The "ActiveCampaign Tool" does not exist as a standalone file in the N8N codebase. Tool nodes are part of the `@n8n/n8n-nodes-langchain` package and serve as AI Agent integration wrappers.

---

## Research Context

### Initial Observation

User provided N8N workflow JSON showing:
```json
{
  "nodes": [
    {
      "parameters": {
        "additionalFields": {}
      },
      "type": "n8n-nodes-base.activeCampaignTool",
      "typeVersion": 1,
      "name": "Create a contact in ActiveCampaign1"
    }
  ]
}
```

This indicated a separate "Tool" variant of the ActiveCampaign node exists in N8N's UI.

---

## Investigation Methodology

### 1. Local Module Search
**Location Searched:** `C:\Working With AI\Odoo Projects\custom-modules-v18\the_ai_automator\static\src\n8n\n8n_nodes\ActiveCampaign`

**Commands Executed:**
```bash
find "...\ActiveCampaign" -name "*Tool*" -o -name "*tool*"
grep -r "activeCampaignTool" "...\n8n_nodes" --include="*.js" --include="*.json"
```

**Result:** ❌ No Tool files found in extracted N8N nodes

---

### 2. Docker Container Investigation

**N8N Installation Details:**
- **Container:** `n8n-existing` (ID: 54cf8d3ebd49)
- **Image:** `n8nio/n8n:latest` (v1.108.2)
- **Host:** `http://localhost:2200`
- **Internal Path:** `/usr/local/lib/node_modules/n8n/`

**Search Commands:**
```bash
docker exec n8n-existing find /usr/local/lib/node_modules/n8n -name "*activeCampaign*" -type f
docker exec n8n-existing find . -name '*Tool.node.js' -type f
```

**Findings:**

#### ActiveCampaign Base Files Found:
```
/usr/local/lib/node_modules/n8n/node_modules/.pnpm/n8n-nodes-base@.../dist/nodes/ActiveCampaign/
├── ActiveCampaign.node.js
├── ActiveCampaign.node.json
├── ActiveCampaignTrigger.node.js
└── ActiveCampaignTrigger.node.json
```

#### LangChain Tool Nodes Found:
```
/usr/local/lib/node_modules/n8n/node_modules/.pnpm/@n8n+n8n-nodes-langchain@.../dist/nodes/tools/
├── ToolCalculator/
├── ToolCode/
├── ToolHttpRequest/
├── ToolSearXng/
├── ToolSerpApi/
├── ToolThink/
├── ToolVectorStore/
├── ToolWikipedia/
├── ToolWolframAlpha/
└── ToolWorkflow/
```

**Result:** ❌ NO "ActiveCampaignTool" file exists in N8N installation

---

## Tool Node Architecture Analysis

### Structure of Tool Nodes (Example: ToolCode.node.js)

Examined the ToolCode implementation to understand the pattern:

```javascript
class ToolCode {
  description = {
    displayName: "Code Tool",
    name: "toolCode",
    icon: "fa:code",
    group: ["transform"],
    version: [1, 1.1, 1.2, 1.3],
    outputs: [NodeConnectionTypes.AiTool],  // Key difference!
    outputNames: ["Tool"],
    codex: {
      categories: ["AI"],
      subcategories: {
        AI: ["Tools"],
        Tools: ["Recommended Tools"]
      }
    }
  }
}
```

### Key Characteristics of Tool Nodes:

1. **Output Type:** `NodeConnectionTypes.AiTool` (vs regular nodes)
2. **Group:** `["transform"]` or `["AI"]`
3. **Purpose:** LangChain/AI Agent integration
4. **Location:** `@n8n/n8n-nodes-langchain` package (separate from base)
5. **Connection:** Only connect to AI Agent nodes

---

## Theories on "ActiveCampaign Tool" Origin

### Theory 1: Dynamic Wrapper Generation
N8N may generate Tool wrappers dynamically at runtime by:
- Scanning available base nodes
- Creating AI Agent-compatible wrappers on-the-fly
- Registering them with the node registry

**Evidence:**
- No static Tool files for service-specific nodes
- Generic Tool nodes (ToolCode, ToolWorkflow) exist
- Simplified parameter structure in user's JSON

### Theory 2: Plugin/Extension System
The Tool may be from:
- N8N Community nodes (external package)
- Custom node development
- N8N Cloud-specific features (not in self-hosted)

**Evidence:**
- User saw it in N8N UI but not in codebase
- Tool nodes are modular (langchain package separate)

### Theory 3: Future/Beta Feature
May be:
- In development (post v1.108.2)
- Available in newer versions
- Part of AI features rollout

**Evidence:**
- LangChain integration is relatively new
- Tool ecosystem is expanding

### Theory 4: User Misidentification
Possible the user saw:
- A different node type
- A workflow node (ToolWorkflow wrapping ActiveCampaign)
- An AI Agent configuration screen

**Counter-evidence:**
- User provided specific JSON with exact type name
- User is experienced with N8N interface

---

## File System Locations Reference

### Host (Windows):
```
C:\Users\total\.docker\n8n-existing\
└── custom-nodes/
```

### Container (Docker):
```
/usr/local/lib/node_modules/n8n/
├── node_modules/
│   ├── .pnpm/
│   │   ├── n8n-nodes-base@.../dist/nodes/
│   │   │   └── ActiveCampaign/
│   │   └── @n8n+n8n-nodes-langchain@.../dist/nodes/tools/
```

### Volume:
```
/var/lib/docker/volumes/n8n-docker_n8n_data/_data
```

---

## Current Implementation Status

### What We Have Implemented:

✅ **305 Suppliers** extracted from N8N filesystem
✅ **423 Nodes** parsed (actions + triggers)
✅ **Base ActiveCampaign Node** with 12 Description files
✅ **ActiveCampaign Trigger** webhook node
✅ **Grouped Actions** by resource category (CONTACT ACTIONS, DEAL ACTIONS, etc.)
✅ **3-Column Drill-Down** UI matching N8N UX

### What We Don't Have:

❌ Tool wrapper nodes (`activeCampaignTool`, etc.)
❌ AI Agent integration nodes
❌ LangChain-specific node types
❌ Dynamic Tool generation system

---

## Recommendations for Future Implementation

### Phase 1: Verify User's Source
1. Ask user for screenshot of "ActiveCampaign Tool" in their N8N
2. Check N8N version they're using
3. Verify if it's from N8N Cloud vs self-hosted
4. Check for community nodes in their installation

### Phase 2: Research Dynamic Generation
If Tool exists, investigate:
1. N8N's node registration system
2. Dynamic wrapper creation patterns
3. AI Agent node connection logic
4. LangChain integration requirements

### Phase 3: Implementation Options

**Option A: Static Tool Nodes**
- Create Tool variants for each service
- Store in separate directory structure
- Register with Odoo module

**Option B: Dynamic Generation**
- Build a Tool wrapper generator
- Convert base nodes → Tool nodes on-demand
- Mirror N8N's dynamic approach

**Option C: Hybrid Approach**
- Implement generic Tool wrapper
- Populate with service-specific operations
- Use existing parsed data structure

### Phase 4: Integration Architecture

```
Odoo Module
├── n8n.simple.node (Base Nodes) ✅ Current
├── n8n.simple.tool (Tool Wrappers) 🔮 Future
├── n8n.ai.agent (AI Agents) 🔮 Future
└── n8n.langchain (LangChain Integration) 🔮 Future
```

---

## Technical Debt & Knowledge Gaps

### Questions Remaining:

1. **How does N8N's node registry work?**
   - Where are Tool nodes registered?
   - Is there a dynamic registration API?

2. **What's the Tool wrapper pattern?**
   - Standard code template?
   - Auto-generated from base node metadata?

3. **Do all base nodes have Tool variants?**
   - Is it automatic or manual?
   - Are there criteria for Tool generation?

4. **How do Tool nodes differ functionally?**
   - Just connection type change?
   - Different parameter structure?
   - Different execution flow?

---

## Conclusion

While we successfully identified the Tool node architecture and located the LangChain package, we could **not find evidence of "ActiveCampaign Tool"** as a static file in N8N v1.108.2.

The investigation suggests Tool nodes are either:
- Dynamically generated by N8N
- Part of a plugin system
- Available in different versions/environments
- Or misidentified by initial observation

**User Disagreement Noted:** The user observed "ActiveCampaign Tool" in their N8N instance and disagrees with the conclusion that it doesn't exist. This suggests the Tool may exist in a different context than our Docker container investigation revealed.

**Recommendation:** Further investigation required before implementing Tool node support.

---

## Research Assets

### Files Created:
- `C:\Users\total\ToolCode.node.js` - Extracted example Tool node

### Commands Reference:
```bash
# Access N8N container
docker exec -it n8n-existing /bin/sh

# Find Tool nodes
find /usr/local/lib/node_modules/n8n -name '*Tool.node.js'

# Search for specific service
find . -name '*activeCampaign*' -o -name '*ActiveCampaign*'

# List langchain tools
ls /usr/local/lib/node_modules/n8n/node_modules/.pnpm/@n8n+n8n-nodes-langchain@.../dist/nodes/tools/
```

---

## Next Steps

1. ✅ Document findings (this report)
2. ⏸️ Park Tool node implementation for future phase
3. ✅ Focus on current 423-node implementation
4. 🔮 Revisit when:
   - User provides Tool node evidence
   - N8N updates with new Tool features
   - AI Agent integration becomes priority
   - LangChain support is requested

---

## Appendix: N8N Installation Details

**Environment:**
- **Host OS:** Windows 11
- **Docker Version:** Latest
- **N8N Version:** 1.108.2
- **Node.js:** v22.17.0 (container)
- **Package Manager:** pnpm

**Access:**
- **URL:** http://localhost:2200
- **Container:** n8n-existing
- **Network:** n8n-existing_n8n-existing-network
- **Volume:** n8n-docker_n8n_data

---

**Report End**

*Note: This research was conducted as part of The AI Automator Odoo module development. The findings represent a point-in-time investigation and may not reflect future N8N versions or configurations.*