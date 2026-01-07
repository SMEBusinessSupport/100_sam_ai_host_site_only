# Developer Prompt: Documentation Consolidator Script

## Context

We have 363+ markdown files scattered across multiple `docs/`, `documentation/`, and `dev docs/` folders within the SAM AI codebase (`D:\SAMAI-18-SaaS\ai_sam\`). These need to be consolidated into our new centralized documentation structure at `D:\SAMAI-18-SaaS\github-repos\05-samai-core\ai_sam_documentation\docs\`.

The destination structure has `_README.md` files in each folder that describe:
- **Purpose** - what belongs in this folder
- **Criteria** - decision rules
- **Examples** - concrete examples
- **Does NOT Include** - exclusion rules

The script parses these READMEs to intelligently determine where each source file should go.

## Goal

Create `doc_consolidator.py` that:
1. **AUTO-MOVES all files** to best-match destinations (no human approval needed)
2. **Generates a move log** for post-move review
3. **Flags low-confidence moves** so human knows what to spot-check

This is **pass 1 of many** - 80% accuracy is acceptable. Human reviews the log AFTER and fixes mistakes.

## Technical Approach

Python script using only standard library (pathlib, csv, re, shutil). No external dependencies.

**Philosophy: Do it, report what you did, human cleans up after.**

## Implementation Steps

### Step 1: Create Script File

Create `D:\SAMAI-18-SaaS\github-repos\05-samai-core\ai_sam_documentation\scripts\doc_consolidator.py`

### Step 2: Configuration Section

```python
#!/usr/bin/env python3
"""
Documentation Consolidator Script
Auto-consolidates scattered .md files into organized structure.

Usage:
    python doc_consolidator.py run       # Auto-move all files + generate report
    python doc_consolidator.py --help    # Show help

Reports saved to: clean_up_reports/
"""

import os
import sys
import csv
import re
import shutil
from pathlib import Path
from datetime import datetime
from collections import defaultdict

# ============================================================================
# CONFIGURATION
# ============================================================================

CONFIG = {
    # Source folders to scan for .md files
    'source_dirs': [
        Path(r'D:/SAMAI-18-SaaS/ai_sam/ai_brain/docs'),
        Path(r'D:/SAMAI-18-SaaS/ai_sam/ai_sam/documentation'),
        Path(r'D:/SAMAI-18-SaaS/ai_sam/ai_sam/dev docs'),
        Path(r'D:/SAMAI-18-SaaS/ai_sam/ai_sam_workflows/documentation'),
        Path(r'D:/SAMAI-18-SaaS/ai_sam/ai_sam_intelligence/dev docs'),
    ],

    # Destination root (where _README.md files live)
    'dest_root': Path(r'D:/SAMAI-18-SaaS/github-repos/05-samai-core/ai_sam_documentation/docs'),

    # Where cleanup reports are saved
    'reports_dir': Path(r'D:/SAMAI-18-SaaS/github-repos/05-samai-core/ai_sam_documentation/clean_up_reports'),

    # Fallback for unmatched files (low confidence)
    'unmatched_dest': '_archive/unsorted',

    # Files/patterns to skip entirely
    'skip_patterns': [
        r'^_README\.md$',      # Skip README files
        r'^\..*',              # Skip hidden files
        r'__pycache__',        # Skip cache
    ],

    # Confidence thresholds
    'high_confidence': 0.7,    # 70%+ = high confidence (auto-move, no flag)
    'medium_confidence': 0.4,  # 40-70% = medium confidence (auto-move, flag for review)
                               # Below 40% = low confidence (move to _archive/unsorted, flag)
}
```

### Step 3: Category Parser

Parse `_README.md` files to extract keywords for matching:

```python
class CategoryParser:
    """Parses _README.md files to extract matching keywords."""

    def __init__(self, dest_root: Path):
        self.dest_root = dest_root
        self.categories = {}
        self._parse_all_readmes()

    def _parse_all_readmes(self):
        """Find and parse all _README.md files."""
        for readme_path in self.dest_root.rglob('_README.md'):
            rel_folder = readme_path.parent.relative_to(self.dest_root)
            self.categories[str(rel_folder)] = self._parse_readme(readme_path)

    def _parse_readme(self, path: Path) -> dict:
        """Extract keywords from a _README.md file."""
        content = path.read_text(encoding='utf-8')

        # Extract sections
        purpose = self._extract_section(content, 'Purpose')
        criteria = self._extract_section(content, 'Criteria')
        examples = self._extract_section(content, 'Examples')
        excludes = self._extract_section(content, 'Does NOT Include')
        subfolders = self._extract_section(content, 'Subfolders')

        # Build keyword lists
        include_keywords = self._extract_keywords(purpose + criteria + examples)
        exclude_keywords = self._extract_keywords(excludes)
        subfolder_names = self._extract_subfolder_names(subfolders)

        return {
            'path': path.parent,
            'include_keywords': include_keywords,
            'exclude_keywords': exclude_keywords,
            'subfolders': subfolder_names,
            'raw_purpose': purpose,
        }

    def _extract_section(self, content: str, header: str) -> str:
        """Extract content under a ## header."""
        pattern = rf'## {header}\s*\n(.*?)(?=\n## |\Z)'
        match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
        return match.group(1).strip() if match else ''

    def _extract_keywords(self, text: str) -> list:
        """Extract meaningful keywords from text."""
        # Remove markdown formatting
        text = re.sub(r'[*_`#\[\]()]', ' ', text)
        text = re.sub(r'-\s+', ' ', text)

        # Extract words (3+ chars, lowercase)
        words = re.findall(r'\b[a-zA-Z_]{3,}\b', text.lower())

        # Filter common words
        stopwords = {'the', 'and', 'for', 'that', 'this', 'with', 'are', 'from',
                     'have', 'has', 'how', 'what', 'why', 'when', 'where', 'which',
                     'can', 'will', 'should', 'would', 'could', 'does', 'not',
                     'into', 'about', 'than', 'them', 'then', 'each', 'other'}

        return [w for w in words if w not in stopwords]

    def _extract_subfolder_names(self, text: str) -> list:
        """Extract subfolder names from Subfolders section."""
        # Match patterns like: `folder/` or - `folder/`
        matches = re.findall(r'`([a-zA-Z_]+)/?`', text)
        return matches
```

### Step 4: File Scorer

Score each source file against categories:

```python
class FileScorer:
    """Scores source files against destination categories."""

    def __init__(self, categories: dict):
        self.categories = categories

    def score_file(self, file_path: Path) -> list:
        """
        Score a file against all categories.
        Returns list of (category, score, reason) tuples, sorted by score.
        """
        # Get file info
        filename = file_path.name.lower()
        filename_keywords = self._extract_file_keywords(filename)

        # Read first 1000 chars of content
        try:
            content = file_path.read_text(encoding='utf-8')[:1000].lower()
        except:
            content = ''

        content_keywords = self._extract_content_keywords(content)

        # Get source folder context
        source_folder = file_path.parent.name.lower()

        results = []

        for cat_name, cat_info in self.categories.items():
            score, reasons = self._calculate_score(
                filename_keywords,
                content_keywords,
                source_folder,
                cat_info
            )
            results.append((cat_name, score, reasons))

        # Sort by score descending
        results.sort(key=lambda x: x[1], reverse=True)
        return results

    def _extract_file_keywords(self, filename: str) -> list:
        """Extract keywords from filename."""
        # Remove extension, split on separators
        name = re.sub(r'\.[^.]+$', '', filename)
        words = re.split(r'[_\-\s]+', name)
        return [w.lower() for w in words if len(w) >= 2]

    def _extract_content_keywords(self, content: str) -> list:
        """Extract keywords from file content."""
        # Get first heading
        heading_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        heading = heading_match.group(1).lower() if heading_match else ''

        # Extract words
        words = re.findall(r'\b[a-zA-Z_]{3,}\b', content)
        words = [w.lower() for w in words[:100]]  # First 100 words

        return words + heading.split()

    def _calculate_score(self, filename_kw, content_kw, source_folder, cat_info) -> tuple:
        """Calculate match score and reasons."""
        score = 0.0
        reasons = []

        include_kw = set(cat_info['include_keywords'])
        exclude_kw = set(cat_info['exclude_keywords'])

        # Filename matches (weighted heavily)
        filename_matches = set(filename_kw) & include_kw
        if filename_matches:
            score += len(filename_matches) * 0.15
            reasons.append(f"filename:{','.join(filename_matches)}")

        # Content matches
        content_matches = set(content_kw) & include_kw
        if content_matches:
            score += min(len(content_matches) * 0.05, 0.3)
            top_matches = list(content_matches)[:3]
            reasons.append(f"content:{','.join(top_matches)}")

        # Source folder context
        if source_folder in str(cat_info['path']).lower():
            score += 0.2
            reasons.append(f"folder_match:{source_folder}")

        # Subfolder matches
        for subfolder in cat_info.get('subfolders', []):
            if subfolder.lower() in filename_kw or subfolder.lower() in content_kw:
                score += 0.15
                reasons.append(f"subfolder:{subfolder}")

        # Exclusion penalty
        exclude_matches = (set(filename_kw) | set(content_kw)) & exclude_kw
        if exclude_matches:
            score -= len(exclude_matches) * 0.1
            reasons.append(f"excluded:{','.join(exclude_matches)}")

        # Cap score at 1.0
        score = max(0, min(1.0, score))

        return score, reasons
```

### Step 5: Consolidator (Auto-Move + Report)

The main engine that moves files and logs everything:

```python
class Consolidator:
    """Auto-moves files and generates cleanup report."""

    def __init__(self, config: dict):
        self.config = config
        self.parser = CategoryParser(config['dest_root'])
        self.scorer = FileScorer(self.parser.categories)
        self.move_log = []
        self.stats = {'moved': 0, 'skipped': 0, 'errors': 0, 'high': 0, 'medium': 0, 'low': 0}

    def run(self):
        """Scan all source files, auto-move, and generate report."""
        print("\n=== Documentation Consolidator: AUTO-MOVE Mode ===\n")
        print("Philosophy: Move everything, report what we did, human cleans up after.\n")

        for source_dir in self.config['source_dirs']:
            if not source_dir.exists():
                print(f"  [SKIP] Source not found: {source_dir}")
                continue

            print(f"  Processing: {source_dir}")
            self._process_directory(source_dir)

        # Generate report
        report_path = self._write_report()

        # Print summary
        self._print_summary(report_path)

        return report_path

    def _process_directory(self, source_dir: Path):
        """Process all .md files in a directory."""
        for md_file in source_dir.rglob('*.md'):
            # Skip based on patterns
            if self._should_skip(md_file):
                continue

            # Score the file
            scores = self.scorer.score_file(md_file)
            best_match = scores[0] if scores else (self.config['unmatched_dest'], 0, ['no_match'])

            dest_folder = best_match[0]
            score = best_match[1]
            reasons = best_match[2]

            # Determine confidence
            confidence = self._get_confidence(score)

            # If low confidence, send to unsorted
            if confidence == 'LOW':
                dest_folder = self.config['unmatched_dest']

            # Build destination path
            dest_path = self.config['dest_root'] / dest_folder / md_file.name

            # Execute move
            status, final_dest = self._move_file(md_file, dest_path)

            # Log the move
            self.move_log.append({
                'source_path': str(md_file),
                'filename': md_file.name,
                'source_folder': md_file.parent.name,
                'destination': str(final_dest) if final_dest else dest_folder,
                'confidence': confidence,
                'score': f"{score:.2f}",
                'match_reason': '; '.join(reasons),
                'status': status,
                'needs_review': 'YES' if confidence in ('LOW', 'MEDIUM') else '',
            })

            # Update stats
            if status == 'SUCCESS':
                self.stats['moved'] += 1
                self.stats[confidence.lower()] += 1
            elif status == 'SKIPPED':
                self.stats['skipped'] += 1
            else:
                self.stats['errors'] += 1

    def _should_skip(self, file_path: Path) -> bool:
        """Check if file should be skipped."""
        filename = file_path.name
        for pattern in self.config['skip_patterns']:
            if re.match(pattern, filename):
                return True
        return False

    def _get_confidence(self, score: float) -> str:
        """Convert score to confidence level."""
        if score >= self.config['high_confidence']:
            return 'HIGH'
        elif score >= self.config['medium_confidence']:
            return 'MEDIUM'
        else:
            return 'LOW'

    def _move_file(self, source: Path, dest: Path) -> tuple:
        """
        Move a single file.
        Returns (status, final_dest_path)
        """
        try:
            if not source.exists():
                return ('ERROR: Source not found', None)

            # Ensure destination directory exists
            dest.parent.mkdir(parents=True, exist_ok=True)

            # Handle filename conflicts
            final_dest = dest
            if final_dest.exists():
                base = dest.stem
                ext = dest.suffix
                counter = 1
                while final_dest.exists():
                    final_dest = dest.parent / f"{base}_{counter}{ext}"
                    counter += 1

            # Copy file (preserving metadata)
            shutil.copy2(source, final_dest)

            # DELETE ORIGINAL - We're committing to the move
            source.unlink()

            return ('SUCCESS', final_dest)

        except Exception as e:
            return (f'ERROR: {e}', None)

    def _write_report(self) -> Path:
        """Write move log to CSV."""
        timestamp = datetime.now().strftime('%Y-%m-%d_%H%M%S')
        report_path = self.config['reports_dir'] / f'consolidation_run_{timestamp}.csv'

        # Ensure directory exists
        report_path.parent.mkdir(parents=True, exist_ok=True)

        fieldnames = [
            'source_path', 'filename', 'source_folder',
            'destination', 'confidence', 'score', 'match_reason',
            'status', 'needs_review'
        ]

        with open(report_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.move_log)

        return report_path

    def _print_summary(self, report_path: Path):
        """Print summary of what happened."""
        print(f"\n{'='*60}")
        print("CONSOLIDATION COMPLETE")
        print('='*60)
        print(f"\nFiles Processed:")
        print(f"  Moved successfully:  {self.stats['moved']}")
        print(f"    - High confidence:   {self.stats['high']}")
        print(f"    - Medium confidence: {self.stats['medium']} (review recommended)")
        print(f"    - Low confidence:    {self.stats['low']} (sent to _archive/unsorted)")
        print(f"  Skipped:             {self.stats['skipped']}")
        print(f"  Errors:              {self.stats['errors']}")
        print(f"\nReport saved to:")
        print(f"  {report_path}")
        print(f"\nNext steps:")
        print(f"  1. Open the CSV report")
        print(f"  2. Filter by 'needs_review' = YES")
        print(f"  3. Manually move any misplaced files")
        print(f"  4. Check _archive/unsorted/ for low-confidence files")
        print('='*60)
```

### Step 6: Main Entry Point

```python
def print_help():
    """Print usage help."""
    print("""
Documentation Consolidator
==========================

Usage:
    python doc_consolidator.py run       Auto-move all files + generate report
    python doc_consolidator.py --help    Show this help

What it does:
    1. Scans source directories for .md files
    2. Scores each file against destination categories (using _README.md keywords)
    3. AUTO-MOVES all files to best-match destination
    4. Generates a cleanup report (CSV) for post-move review

Confidence levels:
    HIGH (70%+)   - Moved to matched folder, no flag
    MEDIUM (40-70%) - Moved to matched folder, flagged for review
    LOW (<40%)    - Moved to _archive/unsorted/, flagged

Reports saved to:
    {reports_dir}
    """.format(reports_dir=CONFIG['reports_dir']))


def cmd_run():
    """Run full consolidation."""
    consolidator = Consolidator(CONFIG)
    consolidator.run()


def main():
    """Main entry point."""
    if len(sys.argv) < 2 or sys.argv[1] in ('--help', '-h', 'help'):
        print_help()
        sys.exit(0)

    command = sys.argv[1].lower()

    if command == 'run':
        cmd_run()
    else:
        print(f"Unknown command: {command}")
        print_help()
        sys.exit(1)


if __name__ == '__main__':
    main()
```

## Expected Files

**New:**
- `D:\SAMAI-18-SaaS\github-repos\05-samai-core\ai_sam_documentation\scripts\doc_consolidator.py`

**Auto-created on first run:**
- `D:\SAMAI-18-SaaS\github-repos\05-samai-core\ai_sam_documentation\clean_up_reports\` (directory)

## Validation Checklist

- [ ] Script runs without errors: `python doc_consolidator.py --help`
- [ ] RUN mode moves files: `python doc_consolidator.py run`
- [ ] Report generated in `clean_up_reports/`
- [ ] High-confidence files landed in correct folders (spot check 5)
- [ ] Low-confidence files landed in `_archive/unsorted/`
- [ ] Original files deleted from source after successful copy
- [ ] Filename conflicts handled with `_1`, `_2` suffix

## Key Differences from Previous Version

| Aspect | Old (Scan-Approve-Move) | New (Auto-Move) |
|--------|-------------------------|-----------------|
| Human approval | Required before move | Not required |
| Workflow | 3 steps | 1 step |
| Report purpose | Approval queue | Post-move log |
| Default action | Wait | Move immediately |
| Low confidence | Wait for approval | Auto-move to `_archive/unsorted/` |
| Original files | Preserved | Deleted after copy |

## Notes

1. **Commits to moves**: Original files ARE deleted after successful copy. This is intentional - we're consolidating, not duplicating.

2. **Low confidence = unsorted**: Files with <40% confidence go to `_archive/unsorted/` rather than a bad guess. Human can sort these manually.

3. **Report for cleanup, not approval**: The CSV shows what happened. Filter by `needs_review=YES` to find files to spot-check.

4. **Conflict handling**: If `foo.md` already exists at destination, it becomes `foo_1.md`.

5. **Extensible**: Add more source directories to `CONFIG['source_dirs']` as needed.

## Handoff

Run `/cto-developer` and paste this prompt to implement the script.

After implementation, run:
```bash
cd D:\SAMAI-18-SaaS\github-repos\05-samai-core\ai_sam_documentation\scripts
python doc_consolidator.py run
```

Then review the report in `clean_up_reports/`.
