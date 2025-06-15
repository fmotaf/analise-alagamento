import os
from datetime import datetime

def format_file_info(file_path):
    try:
        stats = os.stat(file_path)
        mod_time = datetime.fromtimestamp(stats.st_mtime)
        size = stats.st_size
        return f"{mod_time.strftime('%Y-%m-%d %H:%M:%S')} {size} {file_path}"
    except Exception as e:
        return f"Error processing {file_path}: {str(e)}"

def main():
    root_dir = os.path.dirname(os.path.abspath(__file__))
    all_files = []
    
    for root, _, files in os.walk(root_dir):
        # Skip .venv and .git directories
        if '.venv' in root or '.git' in root:
            continue
        
        for file in files:
            file_path = os.path.join(root, file)
            # Skip this script and other .py files
            if not file_path.endswith('.py') or file == os.path.basename(__file__):
                all_files.append(file_path)
    
    # Sort files by modification time
    all_files.sort(key=lambda x: os.path.getmtime(x))
    
    with open('file_timeline.txt', 'w', encoding='utf-8') as f:
        f.write("# Project File Timeline - Oldest to Newest\n")
        f.write(f"# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("# Format:\n")
        f.write("# [Modification Date] [Size in bytes] [Relative Path]\n\n")
        f.write("# Files:\n\n")
        
        for file_path in all_files:
            relative_path = os.path.relpath(file_path, root_dir)
            f.write(f"{format_file_info(relative_path)}\n")

if __name__ == "__main__":
    main()
