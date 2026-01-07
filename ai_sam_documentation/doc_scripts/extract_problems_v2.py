import json
import re
from collections import defaultdict

files = [
    r'C:\Users\total\.claude\projects\SALES_MARKETING\222c3c85-098c-4244-8537-4264060a0a8b.jsonl',
    r'C:\Users\total\.claude\projects\SALES_MARKETING\a795670d-6150-42fd-a9c3-ba86d9497ba0.jsonl',
    r'C:\Users\total\.claude\projects\SALES_MARKETING\89a96141-85f2-4124-9a30-d68ef0ebf679.jsonl'
]

all_user_content = []
all_assistant_content = []

print("Extracting all conversation content...")

for file_path in files:
    file_name = file_path.split('\\')[-1]
    print(f"\nProcessing {file_name}...")

    with open(file_path, 'r', encoding='utf-8') as f:
        line_count = 0
        user_count = 0
        assistant_count = 0

        for line in f:
            line_count += 1
            try:
                data = json.loads(line)

                # Check if this has a message field
                if 'message' in data and isinstance(data['message'], dict):
                    msg = data['message']
                    role = msg.get('role', '')
                    content_raw = msg.get('content', '')

                    # Extract text content
                    text_content = ''
                    if isinstance(content_raw, str):
                        text_content = content_raw
                    elif isinstance(content_raw, list):
                        for item in content_raw:
                            if isinstance(item, dict):
                                if item.get('type') == 'text':
                                    text_content += item.get('text', '')

                    # Store based on role
                    if role == 'user' and text_content.strip():
                        # Skip meta/system messages
                        if not text_content.startswith('<command-') and not text_content.startswith('# '):
                            all_user_content.append({
                                'file': file_name,
                                'content': text_content,
                                'timestamp': data.get('timestamp', '')
                            })
                            user_count += 1
                    elif role == 'assistant' and text_content.strip():
                        all_assistant_content.append({
                            'file': file_name,
                            'content': text_content,
                            'timestamp': data.get('timestamp', '')
                        })
                        assistant_count += 1

            except json.JSONDecodeError as e:
                continue

        print(f"  Lines: {line_count}")
        print(f"  User messages: {user_count}")
        print(f"  Assistant messages: {assistant_count}")

print(f"\n{'='*80}")
print(f"TOTAL USER MESSAGES: {len(all_user_content)}")
print(f"TOTAL ASSISTANT MESSAGES: {len(all_assistant_content)}")
print(f"{'='*80}")

# Write all user content to a file for analysis
with open(r'C:\Users\total\all_user_messages.txt', 'w', encoding='utf-8') as f:
    f.write("="*80 + "\n")
    f.write(f"ALL USER MESSAGES FROM SALES/MARKETING CONVERSATIONS\n")
    f.write(f"Total: {len(all_user_content)} messages\n")
    f.write("="*80 + "\n\n")

    for i, msg in enumerate(all_user_content, 1):
        f.write(f"\n{'='*80}\n")
        f.write(f"MESSAGE {i} | File: {msg['file']}\n")
        f.write(f"{'='*80}\n")
        f.write(msg['content'])
        f.write(f"\n")

print(f"\nAll user messages written to: C:\\Users\\total\\all_user_messages.txt")

# Now extract problem patterns
problem_keywords = {
    'people_problems': [
        'hire', 'hiring', 'find people', 'finding people', 'employee', 'staff', 'team',
        'quit', 'leave', 'turnover', 'retention', 'rely on people', 'depend on',
        'training', 'onboard', 'teaching', 'can\'t find', 'hard to find'
    ],
    'system_problems': [
        'disconnected', 'chaos', 'scattered', 'disorganized', 'manual', 'spreadsheet',
        'tool', 'software', 'integrate', 'sync', 'too many tools', 'switching',
        'different systems', 'nothing talks', 'complicated', 'complex', 'overwhelming'
    ],
    'money_problems': [
        'cash flow', 'money', 'revenue', 'profit', 'expense', 'cost', 'waste', 'wasted',
        'spending', 'budget', 'afford', 'pay for', 'expensive', 'cheap', 'ROI', 'return'
    ],
    'time_problems': [
        'time', 'waiting', 'slow', 'manual', 'repeat', 'redo', 'again', 'daily',
        'hours', 'waste time', 'busy', 'overwhelmed', 'too much work', 'can\'t keep up',
        'automate', 'automation', 'faster', 'bottleneck'
    ],
    'knowledge_problems': [
        'forget', 'remember', 'knowledge', 'document', 'notes', 'memory', 'information',
        'lose', 'lost', 'when people leave', 'institutional knowledge', 'tribal knowledge',
        'don\'t know', 'can\'t find', 'where is', 'who knows'
    ]
}

problem_evidence = defaultdict(lambda: {'count': 0, 'mentions': []})

# Search through user messages for problem mentions
for msg in all_user_content:
    content_lower = msg['content'].lower()

    for category, keywords in problem_keywords.items():
        for keyword in keywords:
            if keyword.lower() in content_lower:
                problem_evidence[category]['count'] += 1
                # Extract context around the keyword
                idx = content_lower.find(keyword.lower())
                start = max(0, idx - 150)
                end = min(len(msg['content']), idx + 150)
                context = msg['content'][start:end].strip()

                problem_evidence[category]['mentions'].append({
                    'file': msg['file'],
                    'context': context,
                    'keyword': keyword
                })
                break  # Count each message once per category

# Write problem analysis
with open(r'C:\Users\total\problem_analysis.txt', 'w', encoding='utf-8') as f:
    f.write("="*80 + "\n")
    f.write("PROBLEM HIERARCHY ANALYSIS\n")
    f.write("="*80 + "\n\n")

    # Sort by frequency
    sorted_problems = sorted(problem_evidence.items(), key=lambda x: x[1]['count'], reverse=True)

    f.write("PROBLEM FREQUENCY (Ranked):\n")
    f.write("-"*80 + "\n")
    for category, data in sorted_problems:
        f.write(f"{category.upper().replace('_', ' ')}: {data['count']} mentions\n")

    f.write("\n\n")

    # Detailed evidence for each category
    for category, data in sorted_problems:
        f.write(f"\n{'='*80}\n")
        f.write(f"{category.upper().replace('_', ' ')} ({data['count']} mentions)\n")
        f.write(f"{'='*80}\n\n")

        # Show up to 30 unique contexts per category
        seen_contexts = set()
        shown = 0
        for mention in data['mentions']:
            context_key = mention['context'][:100]
            if context_key not in seen_contexts and shown < 30:
                seen_contexts.add(context_key)
                f.write(f"File: {mention['file']}\n")
                f.write(f"Keyword: '{mention['keyword']}'\n")
                f.write(f"Context: ...{mention['context']}...\n")
                f.write("-"*80 + "\n")
                shown += 1

print(f"Problem analysis written to: C:\\Users\\total\\problem_analysis.txt")
print("\nPROBLEM FREQUENCY:")
for category, data in sorted(problem_evidence.items(), key=lambda x: x[1]['count'], reverse=True):
    print(f"  {category.replace('_', ' ').upper()}: {data['count']} mentions")
