# Sync Agents To Odoo

**Original file:** `sync_agents_to_odoo.py`
**Type:** PYTHON

---

```python
"""
Sync Claude agents from filesystem to Odoo ai.agent.registry
"""
import json
import os
import glob
import xmlrpc.client

# Configuration
ODOO_URL = "http://localhost:8069"
ODOO_DB = "ai_automator_db"
ODOO_USERNAME = "admin"
ODOO_PASSWORD = "admin"  # Update if different
AGENT_PATH = r"C:\Users\total\.claude\agents"

def connect_odoo():
    """Connect to Odoo via XML-RPC"""
    common = xmlrpc.client.ServerProxy(f'{ODOO_URL}/xmlrpc/2/common')
    uid = common.authenticate(ODOO_DB, ODOO_USERNAME, ODOO_PASSWORD, {})

    if not uid:
        raise Exception("Authentication failed!")

    models = xmlrpc.client.ServerProxy(f'{ODOO_URL}/xmlrpc/2/object')
    return models, uid

def get_agent_metadata(agent_dir):
    """Read agent.json and parse metadata"""
    agent_json_path = os.path.join(agent_dir, 'agent.json')

    if not os.path.exists(agent_json_path):
        return None

    with open(agent_json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Count knowledge files (.md files in directory)
    md_files = glob.glob(os.path.join(agent_dir, '*.md'))
    knowledge_files = [os.path.basename(f) for f in md_files]

    # Calculate word count
    total_words = 0
    for md_file in md_files:
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
                total_words += len(content.split())
        except:
            pass

    return {
        'name': data.get('name'),
        'description': data.get('description', ''),
        'tools': json.dumps(data.get('tools', [])),
        'promptFiles': data.get('promptFiles', []),
        'model': data.get('model', 'sonnet'),
        'color': data.get('color', 'blue'),
        'knowledge_files': knowledge_files,
        'knowledge_file_count': len(knowledge_files),
        'total_words': total_words,
        'agent_path': agent_dir
    }

def map_to_archetype(agent_name):
    """Map agent name to archetype"""
    advisor_agents = ['cto', 'cmo', 'sam', 'odoo-architect']
    implementer_agents = ['odoo-developer']
    gatekeeper_agents = ['odoo-qa-guardian', 'odoo-audit']
    enforcer_agents = ['canvas-core-guardian']
    automator_agents = ['documentation-master', 'github', 'recruiter', 'odoo-debugger']

    if agent_name in advisor_agents:
        return 'advisor'
    elif agent_name in implementer_agents:
        return 'implementer'
    elif agent_name in gatekeeper_agents:
        return 'gatekeeper'
    elif agent_name in enforcer_agents:
        return 'enforcer'
    elif agent_name in automator_agents:
        return 'automator'
    return 'advisor'

def map_to_category(agent_name):
    """Map agent name to category"""
    boardroom_agents = ['cto', 'cmo', 'sam']

    if agent_name in boardroom_agents:
        return 'boardroom'
    return 'operator'

def sync_agent_to_odoo(models, uid, agent_metadata):
    """Create or update agent in Odoo registry"""
    agent_name = agent_metadata['name']

    # Check if agent exists
    agent_ids = models.execute_kw(
        ODOO_DB, uid, ODOO_PASSWORD,
        'ai.agent.registry', 'search',
        [[['name', '=', agent_name]]]
    )

    # Prepare values
    vals = {
        'name': agent_name,
        'display_name': agent_metadata['description'][:100],  # First 100 chars
        'description': agent_metadata['description'],
        'archetype': map_to_archetype(agent_name),
        'category': map_to_category(agent_name),
        'color': agent_metadata['color'],
        'model_name': agent_metadata['model'],
        'tools': agent_metadata['tools'],
        'system_prompt': f"You are {agent_metadata['description']}",  # Basic prompt
        'agent_path': agent_metadata['agent_path'],
        'active': True
    }

    if agent_ids:
        # Update existing
        models.execute_kw(
            ODOO_DB, uid, ODOO_PASSWORD,
            'ai.agent.registry', 'write',
            [agent_ids, vals]
        )
        print(f"[OK] Updated: {agent_name}")
        return agent_ids[0]
    else:
        # Create new
        agent_id = models.execute_kw(
            ODOO_DB, uid, ODOO_PASSWORD,
            'ai.agent.registry', 'create',
            [vals]
        )
        print(f"[OK] Created: {agent_name}")
        return agent_id

def sync_agent_knowledge(models, uid, agent_id, agent_metadata):
    """Sync knowledge files for agent"""
    agent_name = agent_metadata['name']
    agent_dir = agent_metadata['agent_path']

    # Get existing knowledge records
    existing_knowledge_ids = models.execute_kw(
        ODOO_DB, uid, ODOO_PASSWORD,
        'ai.agent.knowledge', 'search',
        [[['agent_id', '=', agent_id]]]
    )

    # Delete old knowledge records
    if existing_knowledge_ids:
        models.execute_kw(
            ODOO_DB, uid, ODOO_PASSWORD,
            'ai.agent.knowledge', 'unlink',
            [existing_knowledge_ids]
        )

    # Create new knowledge records
    for md_file in agent_metadata['knowledge_files']:
        md_path = os.path.join(agent_dir, md_file)

        try:
            with open(md_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Determine content type from filename
            content_type = 'guideline'
            if 'pattern' in md_file.lower():
                content_type = 'pattern'
            elif 'example' in md_file.lower():
                content_type = 'example'
            elif 'methodology' in md_file.lower() or 'protocol' in md_file.lower():
                content_type = 'methodology'
            elif 'reference' in md_file.lower():
                content_type = 'reference'

            vals = {
                'agent_id': agent_id,
                'name': md_file.replace('.md', '').replace('_', ' ').title(),
                'content': content,
                'content_type': content_type,
                'source_file': md_file,
                'source_path': md_path,
                'token_count': len(content.split()),
            }

            models.execute_kw(
                ODOO_DB, uid, ODOO_PASSWORD,
                'ai.agent.knowledge', 'create',
                [vals]
            )

        except Exception as e:
            print(f"  [WARN] Failed to sync knowledge file {md_file}: {e}")

    print(f"  [OK] Synced {len(agent_metadata['knowledge_files'])} knowledge files")

def main():
    print("Syncing Claude agents to Odoo registry...")
    print(f"Agent path: {AGENT_PATH}\n")

    # Connect to Odoo
    try:
        models, uid = connect_odoo()
        print("Connected to Odoo\n")
    except Exception as e:
        print(f"Failed to connect to Odoo: {e}")
        return

    # Scan agent directories
    agent_dirs = [
        d for d in glob.glob(os.path.join(AGENT_PATH, '*'))
        if os.path.isdir(d) and os.path.exists(os.path.join(d, 'agent.json'))
    ]

    print(f"Found {len(agent_dirs)} agents\n")

    synced_count = 0
    for agent_dir in agent_dirs:
        agent_metadata = get_agent_metadata(agent_dir)

        if not agent_metadata:
            continue

        try:
            # Sync agent
            agent_id = sync_agent_to_odoo(models, uid, agent_metadata)

            # Sync knowledge
            sync_agent_knowledge(models, uid, agent_id, agent_metadata)

            synced_count += 1
            print()

        except Exception as e:
            print(f"[ERROR] Failed to sync {agent_metadata['name']}: {e}\n")

    print(f"========================================")
    print(f"[OK] Synced {synced_count}/{len(agent_dirs)} agents to Odoo registry")
    print(f"========================================")

if __name__ == '__main__':
    main()

```
