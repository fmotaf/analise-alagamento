import ast
import os
from pathlib import Path
from typing import List, Dict, Tuple, Optional
import datetime

class ModuleDocstring(ast.NodeVisitor):
    def __init__(self):
        self.name = ""
        self.docstring = ""
        self.classes: List[Dict] = []
        self.functions: List[Dict] = []
        self.imports: List[str] = []
        self.node_stack = []

    def visit_Module(self, node):
        self.docstring = ast.get_docstring(node) or ""
        self.generic_visit(node)
    
    def visit_ClassDef(self, node):
        self.node_stack.append(('class', node.name))
        docstring = ast.get_docstring(node) or ""
        methods = []
        
        # Process methods
        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                method_doc = ast.get_docstring(item) or ""
                methods.append({
                    'name': item.name,
                    'docstring': method_doc,
                    'args': self._get_args(item)
                })
        
        self.classes.append({
            'name': node.name,
            'docstring': docstring,
            'methods': methods
        })
        self.node_stack.pop()
        self.generic_visit(node)
    
    def visit_FunctionDef(self, node):
        if not self.node_stack or self.node_stack[-1][0] != 'class':
            self.functions.append({
                'name': node.name,
                'docstring': ast.get_docstring(node) or "",
                'args': self._get_args(node)
            })
        self.generic_visit(node)
    
    def visit_Import(self, node):
        for name in node.names:
            self.imports.append(f"import {name.name}")
    
    def visit_ImportFrom(self, node):
        module = node.module or ""
        for name in node.names:
            self.imports.append(f"from {module} import {name.name}")
    
    def _get_args(self, node) -> List[Dict]:
        args = []
        
        # Handle positional arguments
        for arg in node.args.posonlyargs + node.args.args:
            args.append({
                'name': arg.arg,
                'type': 'positional',
                'annotation': self._get_annotation(arg.annotation)
            })
        
        # Handle keyword-only arguments
        for kwonly in node.args.kwonlyargs:
            args.append({
                'name': kwonly.arg,
                'type': 'keyword-only',
                'annotation': self._get_annotation(kwonly.annotation),
                'default': 'default'  # This is simplified
            })
        
        # Handle vararg and kwarg
        if node.args.vararg:
            args.append({
                'name': f"*{node.args.vararg.arg}",
                'type': 'varargs',
                'annotation': self._get_annotation(node.args.vararg.annotation)
            })
            
        if node.args.kwarg:
            args.append({
                'name': f"**{node.args.kwarg.arg}",
                'type': 'kwargs',
                'annotation': self._get_annotation(node.args.kwarg.annotation)
            })
            
        return args
    
    def _get_annotation(self, node) -> str:
        if node is None:
            return "Any"
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            return f"{node.value.id}.{node.attr}"
        elif isinstance(node, ast.Subscript):
            return f"{self._get_annotation(node.value)}[{self._get_annotation(node.slice)}]"
        elif isinstance(node, ast.Constant):
            return str(node.value)
        return "Any"

def parse_python_file(file_path: Path) -> Optional[ModuleDocstring]:
    """Parse a Python file and extract its documentation."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            tree = ast.parse(f.read(), filename=str(file_path))
        
        visitor = ModuleDocstring()
        visitor.visit(tree)
        return visitor
    except Exception as e:
        print(f"Error parsing {file_path}: {e}")
        return None

def generate_markdown_docs(module_path: Path, output_dir: Path, root_dir: Path):
    """Generate markdown documentation for a Python module."""
    relative_path = module_path.relative_to(root_dir)
    module_name = str(relative_path.with_suffix('')).replace(os.sep, '.')
    
    visitor = parse_python_file(module_path)
    if not visitor:
        return
    
    # Create output directory structure
    output_path = output_dir / relative_path.with_suffix('.md')
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        # Module header
        f.write(f"# {module_name}\n\n")
        f.write(f"*File*: `{relative_path}`  \n")
        f.write(f"*Last updated*: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        # Module docstring
        if visitor.docstring:
            f.write("## Overview\n\n")
            f.write(f"{visitor.docstring}\n\n")
        
        # Imports
        if visitor.imports:
            f.write("## Imports\n\n")
            for imp in sorted(set(visitor.imports)):
                f.write(f"- `{imp}`  \n")
            f.write("\n")
        
        # Classes
        if visitor.classes:
            f.write("## Classes\n\n")
            for cls in visitor.classes:
                f.write(f"### {cls['name']}\n\n")
                if cls['docstring']:
                    f.write(f"{cls['docstring']}\n\n")
                
                if cls['methods']:
                    f.write("#### Methods\n\n")
                    for method in cls['methods']:
                        f.write(f"- `{method['name']}({', '.join(arg['name'] for arg in method['args'])})`  \n")
                        if method['docstring']:
                            f.write(f"  > {method['docstring'].split('\n')[0]}  \n")
                    f.write("\n")
        
        # Functions
        if visitor.functions:
            f.write("## Functions\n\n")
            for func in visitor.functions:
                f.write(f"### {func['name']}\n\n")
                
                # Function signature
                args_str = []
                for arg in func['args']:
                    arg_str = arg['name']
                    if arg['annotation']:
                        arg_str += f": {arg['annotation']}"
                    if arg['type'] == 'keyword-only':
                        arg_str = f"{arg_str} = ..."
                    args_str.append(arg_str)
                
                f.write(f"```python\ndef {func['name']}({', '.join(args_str)})\n```\n\n")
                
                # Docstring
                if func['docstring']:
                    f.write(f"{func['docstring']}\n\n")

def main():
    project_root = Path(__file__).parent.resolve()
    src_dir = project_root / 'src'
    docs_dir = project_root / 'docs' / 'api'
    
    print(f"Generating documentation in {docs_dir}")
    
    # Clear existing API docs
    if docs_dir.exists():
        import shutil
        shutil.rmtree(docs_dir)
    docs_dir.mkdir(parents=True)
    
    # Process all Python files
    python_files = list(src_dir.rglob('*.py'))
    
    for py_file in python_files:
        if py_file.name == '__init__.py':
            continue
        print(f"Processing {py_file.relative_to(project_root)}")
        generate_markdown_docs(py_file, docs_dir, project_root)
    
    # Generate index
    with open(docs_dir / 'README.md', 'w', encoding='utf-8') as f:
        f.write("# API Reference\n\n")
        f.write("Auto-generated API documentation for the project.\n\n")
        
        # Group by directory
        modules = {}
        for md_file in docs_dir.rglob('*.md'):
            if md_file.name == 'README.md':
                continue
            rel_path = md_file.relative_to(docs_dir).with_suffix('')
            parts = list(rel_path.parts[:-1])
            mod_name = rel_path.stem
            
            current = modules
            for part in parts:
                if part not in current:
                    current[part] = {}
                current = current[part]
            current[mod_name] = str(rel_path)
        
        # Generate TOC
        def write_toc(modules_dict, level=0):
            indent = '  ' * level
            for name, value in sorted(modules_dict.items()):
                if isinstance(value, dict):
                    f.write(f"{indent}- **{name}**\n")
                    write_toc(value, level + 1)
                else:
                    f.write(f"{indent}- [{name}]({value}.md)\n")
        
        write_toc(modules)
    
    print("\nDocumentation generated successfully!")

if __name__ == "__main__":
    main()
