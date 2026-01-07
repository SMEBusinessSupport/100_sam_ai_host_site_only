import json
import re
from collections import defaultdict

# Problem keywords and phrases to search for
problem_patterns = {
    'people': [
        r'\b(hiring|finding|keeping|retain|employee|staff|team|rely|depend on people|quit|leave|turnover)\b',
        r'\b(can\'t find|hard to find|difficult to hire|lose people|people leave)\b',
        r'\b(training|onboard|teach)\b'
    ],
    'systems': [
        r'\b(disconnected|chaos|scattered|disorganized|manual|spreadsheet|tool|software|integrate|sync)\b',
        r'\b(too many tools|switching between|different systems|nothing talks)\b',
        r'\b(complicated|complex|overwhelming)\b'
    ],
    'money': [
        r'\b(cash flow|money|revenue|profit|expense|cost|waste|spending|budget)\b',
        r'\b(afford|pay for|expensive|cheap)\b',
        r'\b(ROI|return|investment)\b'
    ],
    'time': [
        r'\b(time|waiting|slow|manual|repeat|redo|again|daily|hours|waste time)\b',
        r'\b(busy|overwhelmed|too much work|can\'t keep up)\b',
        r'\b(automate|automation|faster)\b'
    ],
    'knowledge': [
        r'\b(forget|remember|knowledge|document|notes|memory|information|lose|lost)\b',
        r'\b(when people leave|institutional knowledge|tribal knowledge)\b',
        r'\b(don\'t know|can\'t find|where is|who knows)\b'
    ]
}

files = [
    r'C:\Users\total\.claude\projects\SALES_MARKETING\222c3c85-098c-4244-8537-4264060a0a8b.jsonl',
    r'C:\Users\total\.claude\projects\SALES_MARKETING\a795670d-6150-42fd-a9c3-ba86d9497ba0.jsonl',
    r'C:\Users\total\.claude\projects\SALES_MARKETING\89a96141-85f2-4124-9a30-d68ef0ebf679.jsonl'
]

problem_mentions = defaultdict(list)
problem_counts = defaultdict(int)
all_user_messages = []

for file_path in files:
    print(f"\nProcessing {file_path.split('\\')[-1]}...")
    with open(file_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            try:
                data = json.loads(line)
                # Extract user messages (Anthony's words)
                if 'role' in data and data['role'] == 'user':
                    content = ''
                    if isinstance(data.get('content'), str):
                        content = data['content']
                    elif isinstance(data.get('content'), list):
                        for item in data['content']:
                            if isinstance(item, dict) and item.get('type') == 'text':
                                content += item.get('text', '')

                    if content:
                        all_user_messages.append({
                            'file': file_path.split('\\')[-1],
                            'line': line_num,
                            'content': content
                        })

                        # Check for problem patterns
                        content_lower = content.lower()
                        for category, patterns in problem_patterns.items():
                            for pattern in patterns:
                                if re.search(pattern, content_lower, re.IGNORECASE):
                                    problem_counts[category] += 1
                                    # Store snippet of the problem mention
                                    matches = re.finditer(pattern, content_lower, re.IGNORECASE)
                                    for match in matches:
                                        start = max(0, match.start() - 100)
                                        end = min(len(content), match.end() + 100)
                                        snippet = content[start:end]
                                        problem_mentions[category].append({
                                            'file': file_path.split('\\')[-1],
                                            'snippet': snippet.strip()
                                        })
                                    break  # Count once per message per category
            except json.JSONDecodeError:
                continue

# Write summary
print("\n" + "="*80)
print("PROBLEM FREQUENCY ANALYSIS")
print("="*80)
for category, count in sorted(problem_counts.items(), key=lambda x: x[1], reverse=True):
    print(f"{category.upper()}: {count} mentions")

# Write detailed output
output_file = r'C:\Users\total\problem_extraction.txt'
with open(output_file, 'w', encoding='utf-8') as out:
    out.write("="*80 + "\n")
    out.write("PROBLEM HIERARCHY EXTRACTION FROM ANTHONY'S CONVERSATIONS\n")
    out.write("="*80 + "\n\n")

    out.write(f"Total user messages analyzed: {len(all_user_messages)}\n\n")

    out.write("PROBLEM FREQUENCY:\n")
    out.write("-"*80 + "\n")
    for category, count in sorted(problem_counts.items(), key=lambda x: x[1], reverse=True):
        out.write(f"{category.upper()}: {count} mentions\n")

    out.write("\n\n")
    out.write("="*80 + "\n")
    out.write("PROBLEM MENTIONS BY CATEGORY (with context)\n")
    out.write("="*80 + "\n\n")

    for category in sorted(problem_counts.keys(), key=lambda x: problem_counts[x], reverse=True):
        out.write(f"\n{'='*80}\n")
        out.write(f"CATEGORY: {category.upper()} ({problem_counts[category]} mentions)\n")
        out.write(f"{'='*80}\n\n")

        # Show first 50 unique snippets for each category
        seen = set()
        count = 0
        for mention in problem_mentions[category]:
            snippet_key = mention['snippet'][:100]
            if snippet_key not in seen and count < 50:
                seen.add(snippet_key)
                out.write(f"File: {mention['file']}\n")
                out.write(f"Context: ...{mention['snippet']}...\n")
                out.write("-"*80 + "\n")
                count += 1

print(f"\nDetailed output written to: {output_file}")
print(f"Total user messages analyzed: {len(all_user_messages)}")
