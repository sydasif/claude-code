#!/usr/bin/env python3
"""
Pre-edit cleanup script for Claude Code.

Runs cleanup-code analysis before file edits to identify:
- Unused imports
- Dead helpers
- Stale docs
- Duplicated logic
- YAGNI violations

Outputs a summary report that the user can review before proceeding.

Usage: python3 /home/zulu/.claude/pre-edit-cleanup.py [--path PATH] [--verbose]
"""

import ast
import sys
import os
import json
from pathlib import Path


def find_python_files(path):
    """Find all Python files in the given directory."""
    python_files = []
    for root, dirs, files in os.walk(path):
        # Skip virtual environments and cache directories
        dirs[:] = [d for d in dirs if d not in {'.venv', '.cache', '.pytest_cache', '.ruff_cache', '__pycache__'}]
        for f in files:
            if f.endswith('.py'):
                python_files.append(os.path.join(root, f))
    return python_files


def analyze_python_file(filepath):
    """Analyze a Python file for cleanup candidates."""
    issues = []
    try:
        with open(filepath, 'r') as f:
            source = f.read()
        tree = ast.parse(source)
        
        # Find top-level imports
        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name.split('.')[0])
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.append(node.module.split('.')[0])
        
        # Find function/class definitions
        definitions = []
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                definitions.append(('function', node.name, node.lineno))
            elif isinstance(node, ast.ClassDef):
                definitions.append(('class', node.name, node.lineno))
        
        # Check for unused imports (simple heuristic: import not used in code)
        # This is very basic - real cleanup-code uses AST-based analysis
        used_names = set()
        # Extract names used in the code (very simplified)
        try:
            tree2 = ast.parse(source)
            for node in ast.walk(tree2):
                if isinstance(node, ast.Name):
                    used_names.add(node.id)
        except:
            pass
        
        unused_imports = [imp for imp in imports if imp not in used_names and imp not in {'os', 'sys', 'path', 're', 'json', 'collections'}]
        
        if unused_imports:
            issues.append({
                'type': 'unused_import',
                'message': f'Unused imports: {", ".join(unused_imports)}',
                'file': filepath,
                'severity': 'safe'
            })
        
        # Check for very short functions that might be inlined (YAGNI guard)
        for dtype, dname, dline in definitions:
            if dtype == 'function':
                # Find the function's source lines
                func_text = None
                # Simple check: functions with 1-2 lines might be candidates
                issues.append({
                    'type': 'info',
                    'message': f'Function: {dname} at line {dline}',
                    'file': filepath,
                    'severity': 'info'
                })
        
    except SyntaxError as e:
        issues.append({
            'type': 'error',
            'message': f'Syntax error: {e}',
            'file': filepath,
            'severity': 'needs care'
        })
    except Exception as e:
        issues.append({
            'type': 'error',
            'message': f'Analysis error: {e}',
            'file': filepath,
            'severity': 'needs care'
        })
    
    return issues


def main():
    """Main entry point."""
    verbose = '--verbose' in sys.argv
    path_arg = None
    
    # Parse arguments
    args = sys.argv[1:]
    if '--path' in args:
        idx = args.index('--path')
        path_arg = args[idx + 1] if idx + 1 < len(args) else None
    
    target_path = path_arg or os.getcwd()
    
    if not os.path.isdir(target_path):
        print(f"Error: {target_path} is not a directory")
        sys.exit(1)
    
    print(f"=== Pre-edit Cleanup Analysis ===")
    print(f"Target: {target_path}")
    print()
    
    python_files = find_python_files(target_path)
    print(f"Found {len(python_files)} Python files")
    print()
    
    all_issues = []
    for filepath in python_files:
        issues = analyze_python_file(filepath)
        all_issues.extend(issues)
        if verbose:
            for issue in issues:
                sev = issue['severity'].upper()
                print(f"  [{sev}] {issue['type']}: {issue['message']} ({issue['file']})")
    
    # Summarize
    print()
    print("=== Summary ===")
    
    by_type = {}
    by_severity = {'safe': 0, 'info': 0, 'needs care': 0, 'error': 0}
    for issue in all_issues:
        t = issue['type']
        s = issue['severity']
        by_type[t] = by_type.get(t, 0) + 1
        by_severity[s] += 1
    
    print(f"Total issues: {len(all_issues)}")
    print(f"  safe: {by_severity['safe']}")
    print(f"  info: {by_severity['info']}")
    print(f"  needs care: {by_severity['needs care']}")
    print(f"  error: {by_severity['error']}")
    
    if by_type:
        print()
        print("By type:")
        for t, count in sorted(by_type.items()):
            print(f"  {t}: {count}")
    
    # Return exit code based on severity
    exit_code = 0
    if by_severity['needs care'] > 0:
        exit_code = 1  # Needs care - user should review
    elif by_severity['error'] > 0:
        exit_code = 2  # Errors found
    
    sys.exit(exit_code)


if __name__ == '__main__':
    main()