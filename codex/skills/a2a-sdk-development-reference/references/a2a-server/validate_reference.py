"""Check source drift, callable coverage, links, whitespace, and example syntax.

Run from anywhere: .venv/bin/python a2a-server/validate_reference.py
The manifest/index are reference snapshots; validation does not regenerate them.
"""
import ast
import hashlib
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / '.venv/lib/python3.11/site-packages/a2a/server'


def declarations(tree):
    result = []

    def visit(node, parents=()):
        if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            parents = (*parents, node.name)
            result.append(('.'.join(parents), node.lineno, type(node).__name__))
        for child in ast.iter_child_nodes(node):
            visit(child, parents)

    visit(tree)
    return result


def main():
    manifest = json.loads((HERE / 'source_inventory.json').read_text())
    files = sorted(p.relative_to(SOURCE).as_posix() for p in SOURCE.rglob('*.py'))
    assert files == sorted(manifest['files']), 'Source file inventory changed'
    index = (HERE / 'callable_index_knowledge.md').read_text()
    count = 0
    for relative, entry in manifest['files'].items():
        path = SOURCE / relative
        assert hashlib.sha256(path.read_bytes()).hexdigest() == entry['sha256'], relative
        actual = declarations(ast.parse(path.read_text()))
        assert actual == [tuple(item) for item in entry['declarations']], relative
        narrative = (HERE / entry['guide']).read_text()
        assert Path(relative).name in narrative, f'No narrative source section: {relative}'
        for name, line, kind in actual:
            key = f'{relative}:{line}:{name}'
            assert f'<!-- declaration:{key} -->' in index, f'Missing declaration: {key}'
        count += len(actual)
    docs = sorted(HERE.glob('*.md'))
    for path in docs:
        value = path.read_text()
        assert value.endswith('\n'), f'Missing newline: {path.name}'
        assert not any(line.rstrip() != line for line in value.splitlines()), path.name
        assert value.count('```') % 2 == 0, f'Unbalanced code fences: {path.name}'
        for target in re.findall(r'\]\(([^)]+)\)', value):
            if target.startswith(('http:', 'https:', '#')):
                continue
            target = re.sub(r':\d+$', '', target.split('#', 1)[0])
            assert (path.parent / target).exists(), f'Broken link in {path.name}: {target}'
    ast.parse((HERE / 'examples/starlette_server.py').read_text())
    print(f'PASS: {len(files)} source files, {count} declarations, {len(docs)} Markdown files; source hashes, index, source sections, links, whitespace, fences, example syntax')


if __name__ == '__main__':
    main()
