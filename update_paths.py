import os
import re
from pathlib import Path

# Define the project root
PROJECT_ROOT = Path(__file__).parent.resolve()
SRC_DIR = PROJECT_ROOT / 'src'

# Path mappings (old -> new)
PATH_MAPPINGS = {
    'src/data_collection/': 'src/data/collection/',
    'src/data_load/': 'src/data/collection/',
    'src/data_aggregation/': 'src/data/processing/',
    'src/data_transformation/': 'src/data/processing/',
    'src/data_validation/': 'src/data/validation/',
    'src/data_training/': 'src/models/training/',
    'src/data_forecast/': 'src/models/prediction/',
    'src/data_visualization/': 'src/visualization/charts/',
    'src/analysis/plot_': 'src/visualization/charts/plot_',
    'src/analysis/image_': 'src/visualization/maps/image_',
    'src/data_association/': 'src/utils/geo/',
    'static/tiff/': 'data/raw/satellite/',
    'src/flood_features.csv': 'data/processed/features/flood_features.csv'
}

def update_file_paths(file_path):
    """Update paths in a single file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Update paths
        for old_path, new_path in PATH_MAPPINGS.items():
            content = content.replace(old_path, new_path)
            # Also handle path with backslashes for Windows
            content = content.replace(old_path.replace('/', '\\'), new_path.replace('/', '\\'))
        
        # Update relative paths
        content = re.sub(
            r'file_path = Path\(__file__\).*?parent', 
            f'file_path = Path(__file__).resolve().parent.parent', 
            content
        )
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Updated: {file_path}")
            
    except Exception as e:
        print(f"Error processing {file_path}: {str(e)}")

def main():
    # Process all Python files in the src directory
    for root, _, files in os.walk(SRC_DIR):
        for file in files:
            if file.endswith('.py'):
                file_path = Path(root) / file
                update_file_paths(file_path)
    
    print("\nPath updates completed!")

if __name__ == '__main__':
    main()
