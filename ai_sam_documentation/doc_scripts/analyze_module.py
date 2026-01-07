import os
from pathlib import Path
from collections import defaultdict

def analyze_directory(root_path):
    """
    Analyze a directory structure counting folders, files, lines of code, and words.
    """
    root = Path(root_path)

    if not root.exists():
        print(f"Error: Path does not exist: {root_path}")
        return

    # Statistics per folder
    folder_stats = defaultdict(lambda: {
        'files': 0,
        'lines': 0,
        'words': 0,
        'file_details': []
    })

    # Global totals
    total_folders = 0
    total_files = 0
    total_lines = 0
    total_words = 0

    # Walk through directory
    for dirpath, dirnames, filenames in os.walk(root):
        # Count this folder
        total_folders += 1
        current_folder = Path(dirpath)

        # Process files in this folder
        for filename in filenames:
            filepath = current_folder / filename

            try:
                # Try to read file as text
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    lines = content.split('\n')
                    line_count = len(lines)
                    word_count = len(content.split())

                    # Update folder stats
                    folder_stats[str(current_folder)]['files'] += 1
                    folder_stats[str(current_folder)]['lines'] += line_count
                    folder_stats[str(current_folder)]['words'] += word_count
                    folder_stats[str(current_folder)]['file_details'].append({
                        'name': filename,
                        'lines': line_count,
                        'words': word_count
                    })

                    # Update totals
                    total_files += 1
                    total_lines += line_count
                    total_words += word_count

            except Exception as e:
                # Skip files that can't be read
                print(f"Warning: Could not read {filepath}: {e}")

    # Print results
    print("=" * 80)
    print(f"ANALYSIS FOR: {root_path}")
    print("=" * 80)
    print()

    # Print per-folder statistics
    for folder_path in sorted(folder_stats.keys()):
        stats = folder_stats[folder_path]
        if stats['files'] > 0:  # Only show folders with files
            print(f"\nFolder: {folder_path}")
            print(f"  Total Files: {stats['files']}")
            print(f"  Total Lines: {stats['lines']:,}")
            print(f"  Total Words: {stats['words']:,}")
            print(f"  Files:")

            for file_detail in sorted(stats['file_details'], key=lambda x: x['name']):
                print(f"    - {file_detail['name']}")
                print(f"      Lines: {file_detail['lines']:,}")
                print(f"      Words: {file_detail['words']:,}")

    # Print summary
    print("\n" + "=" * 80)
    print("SUMMARY TOTALS")
    print("=" * 80)
    print(f"Total Folders: {total_folders}")
    print(f"Total Files: {total_files}")
    print(f"Total Lines of Code: {total_lines:,}")
    print(f"Total Words: {total_words:,}")
    print("=" * 80)

if __name__ == "__main__":
    target_path = r"C:\Working With AI\ai_sam\ai_sam\ai_sam_workflows"
    analyze_directory(target_path)
