import ast
import os
import sys
import stdlib_list

# Note: we don't have stdlib_list installed probably, so I'll just use a basic heuristic.
stdlib = set(sys.builtin_module_names)
stdlib.update(['os', 'sys', 'datetime', 'json', 'io', 'base64', 'pathlib', 'urllib', 're', 'logging', 'collections', 'typing', 'subprocess', 'random', 'hashlib', 'math', 'string', 'time', 'functools', 'itertools', 'mimetypes', 'shutil', 'tempfile', 'uuid', 'warnings', 'decimal'])

project_modules = set(['config', 'core', 'users', 'hr', 'organization', 'workflow', 'academic', 'documents'])

for root, dirs, files in os.walk('.'):
    if 'venv' in root or '.git' in root or 'migrations' in root:
        continue
    for file in files:
        if file.endswith('.py'):
            project_modules.add(file[:-3])

external_modules = set()

for root, dirs, files in os.walk('.'):
    if 'venv' in root or '.git' in root:
        continue
    for file in files:
        if file.endswith('.py'):
            filepath = os.path.join(root, file)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    tree = ast.parse(f.read())
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            base = alias.name.split('.')[0]
                            if base not in stdlib and base not in project_modules:
                                external_modules.add(base)
                    elif isinstance(node, ast.ImportFrom):
                        if node.module:
                            base = node.module.split('.')[0]
                            if node.level == 0 and base not in stdlib and base not in project_modules:
                                external_modules.add(base)
            except Exception as e:
                pass

print("External modules found:")
for m in sorted(list(external_modules)):
    print(m)
