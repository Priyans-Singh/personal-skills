"""Read-only final structural audit across all remaining A2A root folders/files."""
import ast
import hashlib
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
WORKSPACE = HERE.parent


def declarations(tree):
    found = []
    def visit(node, parents=()):
        if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            parents = (*parents, node.name)
            found.append(('.'.join(parents), node.lineno, type(node).__name__))
        for child in ast.iter_child_nodes(node):
            visit(child, parents)
    visit(tree)
    return found


def main():
    inventory = json.loads((HERE / 'source_inventory.json').read_text())
    source = WORKSPACE / inventory['source']
    expected_folders = set(inventory['folders'])
    assert {p.name for p in source.iterdir() if p.is_dir() and p.name not in inventory['excluded']} == expected_folders
    assert {p.name for p in source.iterdir() if p.is_file()} == set(inventory['root_files'])
    total_files = 0
    total_decl = 0
    for group, entries in [*inventory['folders'].items(), ('root', inventory['root_files'])]:
        group_source = source if group == 'root' else source / group
        docs = WORKSPACE / ('a2a-' + group)
        assert (docs / 'README.md').exists(), group
        actual_files = sorted(p.relative_to(group_source).as_posix() for p in
                             (group_source.iterdir() if group == 'root' else group_source.rglob('*'))
                             if p.is_file() and '__pycache__' not in p.parts)
        assert actual_files == sorted(entries), group
        actual_declarations = set()
        for relative, entry in entries.items():
            path = group_source / relative
            assert hashlib.sha256(path.read_bytes()).hexdigest() == entry['sha256'], str(path)
            if path.suffix in {'.py', '.pyi'}:
                for name, line, kind in declarations(ast.parse(path.read_text())):
                    actual_declarations.add((relative, name, line, kind))
        index_path = docs / 'callable_index.json'
        if index_path.exists():
            index = json.loads(index_path.read_text())
            indexed = {(row.get('file', row.get('source')), row['name'], row['line'], row['kind']) for row in index}
            assert actual_declarations == indexed, f'Declaration mismatch: {group}: {actual_declarations ^ indexed}'
            for row in index:
                assert (docs / row['guide']).exists(), row
        else:
            manifest = json.loads((docs / 'source_inventory.json').read_text())
            indexed = {(relative, name, line, kind) for relative, entry in manifest['files'].items()
                       for name, line, kind in entry['declarations']}
            assert indexed == actual_declarations, group
        markdown = sorted(docs.glob('*.md'))
        for path in markdown:
            value = path.read_text()
            assert value.endswith('\n'), str(path)
            assert all(line == line.rstrip() for line in value.splitlines()), str(path)
            assert value.count('```') % 2 == 0, str(path)
            for target in re.findall(r'\]\(([^)]+)\)', value):
                if target.startswith(('http:', 'https:', '#')): continue
                target = re.sub(r':\d+$', '', target.split('#', 1)[0])
                assert (path.parent / target).exists(), f'Broken link {path}: {target}'
        total_files += len(entries)
        total_decl += len(actual_declarations)
        print(f'PASS {group}: {len(entries)} source files, {len(actual_declarations)} AST declarations incl. stubs, {len(markdown)} Markdown references')
    print(f'PASS whole scope: {len(expected_folders)} root folders + loose root files, {total_files} source files, {total_decl} declarations')


if __name__ == '__main__':
    main()
