import ast
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple
import importlib.util
import os

class ImportChecker(ast.NodeVisitor):
    def __init__(self, file_path: Path, project_root: Path):
        self.file_path = file_path
        self.project_root = project_root
        self.imports: List[Tuple[str, int, str]] = []
        self.local_imports: List[Tuple[str, int, str]] = []
        self.errors: List[str] = []
        self.relative_imports: Dict[str, List[Tuple[str, int]]] = {}

    def visit_Import(self, node):
        for name in node.names:
            self.imports.append((name.name, node.lineno, 'import'))
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        if node.level > 0:  # Relative import
            module = node.module or ''
            for name in node.names:
                if node.module:
                    full_import = f"{'.' * node.level}{module}.{name.name}"
                else:
                    full_import = f"{'.' * node.level}{name.name}"
                
                if full_import not in self.relative_imports:
                    self.relative_imports[full_import] = []
                self.relative_imports[full_import].append((str(self.file_path), node.lineno))
        
        for name in node.names:
            self.imports.append((f"{node.module}.{name.name}" if node.module else name.name, 
                              node.lineno, 'from'))
        self.generic_visit(node)

def check_imports(file_path: Path, project_root: Path) -> ImportChecker:
    """Check imports in a single Python file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        try:
            tree = ast.parse(f.read(), filename=str(file_path))
        except SyntaxError as e:
            print(f"Syntax error in {file_path}: {e}")
            return ImportChecker(file_path, project_root)
    
    checker = ImportChecker(file_path, project_root)
    checker.visit(tree)
    return checker

def resolve_relative_import(relative_import: str, file_path: Path, project_root: Path) -> Path:
    """Resolve a relative import to an absolute file path."""
    parts = relative_import.split('.')
    levels = 0
    for part in parts:
        if part == '':
            levels += 1
        else:
            break
    
    if levels == 0:
        return project_root / relative_import.replace('.', '/')
    
    parent = file_path.parent
    for _ in range(levels - 1):
        parent = parent.parent
    
    module_parts = parts[levels:]
    module_path = parent / '/'.join(module_parts)
    
    # Try different extensions
    for ext in ['.py', '']:
        test_path = module_path.with_suffix(ext)
        if test_path.exists():
            return test_path
        
        # Handle __init__.py case
        init_path = module_path / '__init__.py'
        if init_path.exists():
            return init_path
    
    return module_path

def check_all_imports(project_root: Path) -> Tuple[Dict[str, List[Tuple[str, int]]], List[str]]:
    """Check all imports in the project."""
    python_files = list(project_root.rglob('*.py'))
    all_relative_imports = {}
    all_errors = []
    
    for py_file in python_files:
        if any(part.startswith(('.', '__')) for part in py_file.parts):
            continue
            
        checker = check_imports(py_file, project_root)
        
        # Check relative imports
        for rel_import, locations in checker.relative_imports.items():
            resolved = resolve_relative_import(rel_import, py_file, project_root)
            if not resolved.exists():
                if rel_import not in all_relative_imports:
                    all_relative_imports[rel_import] = []
                all_relative_imports[rel_import].extend(locations)
        
        # Check for potential import errors
        for imp, lineno, _ in checker.imports:
            if imp.startswith('.'):  # Skip relative imports
                continue
                
            try:
                __import__(imp.split('.')[0])
            except (ImportError, ModuleNotFoundError):
                # Check if it's a local module
                module_path = project_root / imp.replace('.', '/')
                if not any((module_path / f).exists() for f in ['__init__.py', f"{module_path.name}.py"]):
                    all_errors.append(f"{py_file}:{lineno} - Unable to import '{imp}'")
    
    return all_relative_imports, all_errors

def main():
    project_root = Path(__file__).parent.resolve()
    print(f"Checking imports in project: {project_root}")
    
    # Check Python version
    print(f"Python version: {sys.version}")
    
    # Check all imports
    relative_imports, errors = check_all_imports(project_root)
    
    # Report results
    if relative_imports:
        print("\nPotential issues with relative imports:")
        for imp, locations in relative_imports.items():
            print(f"\nRelative import: {imp}")
            for file, line in locations:
                print(f"  - {file}:{line}")
    
    if errors:
        print("\nImport errors found:")
        for error in errors:
            print(f"- {error}")
    
    if not relative_imports and not errors:
        print("\nNo import issues found!")
    else:
        print(f"\nFound {len(relative_imports)} relative import issues and {len(errors)} import errors.")

if __name__ == "__main__":
    main()
