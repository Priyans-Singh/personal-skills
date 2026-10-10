"""Validate the five parent-owned A2A references without importing migrations."""
import ast
import hashlib
import json
import re
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent.parent
GROUPS = ['auth', 'extensions', 'helpers', 'migrations', 'root']


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
    count = 0
    definitions = 0
    for group in GROUPS:
        destination = WORKSPACE / ('a2a-' + group)
        manifest = json.loads((destination / 'source_inventory.json').read_text())
        source = WORKSPACE / manifest['source']
        paths = (sorted(p for p in source.iterdir() if p.is_file()) if group == 'root'
                 else sorted(p for p in source.rglob('*') if p.is_file() and '__pycache__' not in p.parts))
        assert sorted(p.relative_to(source).as_posix() for p in paths) == sorted(manifest['files']), group
        index = (destination / 'callable_index_knowledge.md').read_text()
        local_count = 0
        for relative, entry in manifest['files'].items():
            path = source / relative
            assert hashlib.sha256(path.read_bytes()).hexdigest() == entry['sha256'], str(path)
            actual = declarations(ast.parse(path.read_text())) if path.suffix == '.py' else []
            assert actual == [tuple(x) for x in entry['declarations']], relative
            narrative = (destination / entry['guide']).read_text()
            assert Path(relative).name in narrative, f'No source section: {relative}'
            for name, line, kind in actual:
                assert f'<!-- declaration:{relative}:{line}:{name} -->' in index, name
                assert name.split('.')[-1] in narrative, f'No narrative mention: {relative}:{name}'
            local_count += len(actual)
        for doc in destination.glob('*.md'):
            text = doc.read_text()
            assert text.endswith('\n') and all(line == line.rstrip() for line in text.splitlines()), str(doc)
            assert text.count('```') % 2 == 0, str(doc)
            for target in re.findall(r'\]\(([^)]+)\)', text):
                if target.startswith(('http:', 'https:', '#')): continue
                target = re.sub(r':\d+$', '', target.split('#', 1)[0])
                assert (doc.parent / target).exists(), f'Broken link: {doc}: {target}'
        count += len(paths)
        definitions += local_count
        print(f'PASS {group}: {len(paths)} files, {local_count} declarations; hashes, source sections, narrative names, index, Markdown links/format')
    print(f'TOTAL {count} files, {definitions} declarations')


if __name__ == '__main__':
    main()
