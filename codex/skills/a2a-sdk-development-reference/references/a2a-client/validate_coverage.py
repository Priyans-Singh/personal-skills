"""Read-only checks for the documented local a2a.client snapshot."""

import ast
import hashlib
import json
import re
from pathlib import Path


def declarations(path):
    """Enumerate classes/functions, including conditional and nested declarations."""
    result = []

    class Visitor(ast.NodeVisitor):
        def __init__(self):
            self.scope = []

        def record(self, node, kind):
            name = ".".join([*self.scope, node.name])
            result.append({"name": name, "kind": kind, "line": node.lineno})
            self.scope.append(node.name)
            self.generic_visit(node)
            self.scope.pop()

        def visit_ClassDef(self, node):
            self.record(node, "class")

        def visit_FunctionDef(self, node):
            self.record(node, "function")

        def visit_AsyncFunctionDef(self, node):
            kind = "async generator" if any(
                isinstance(item, (ast.Yield, ast.YieldFrom))
                for item in ast.walk(node)
            ) else "async function"
            self.record(node, kind)

    Visitor().visit(ast.parse(path.read_text()))
    return result


def main():
    folder = Path(__file__).resolve().parent
    source = folder.parent / ".venv/lib/python3.11/site-packages/a2a/client"
    manifest = json.loads((folder / "source_inventory.json").read_text())
    errors = []
    files = {str(path.relative_to(source)): path for path in source.rglob("*.py")}
    if set(files) != set(manifest["files"]):
        errors.append("Source file inventory changed")
    total = 0
    for relative, entry in manifest["files"].items():
        path = files.get(relative)
        if path is None:
            errors.append(f"Missing source: {relative}")
            continue
        if hashlib.sha256(path.read_bytes()).hexdigest() != entry["sha256"]:
            errors.append(f"Source changed: {relative}")
        actual = declarations(path)
        if actual != entry["declarations"]:
            errors.append(f"Declarations changed: {relative}")
        guide = folder / entry["guide"]
        if not guide.is_file():
            errors.append(f"Missing guide: {guide}")
            continue
        prose = guide.read_text()
        # This checks omissions only; behavior was manually traced and documented.
        # coverage_knowledge.md deliberately does not participate in this test.
        for item in actual:
            leaf = item["name"].split(".")[-1]
            if not re.search(r"(?<!\w)" + re.escape(leaf) + r"(?!\w)", prose):
                errors.append(f"Undocumented declaration: {relative}:{item['name']}")
        total += len(actual)
    for relative, digest in manifest["supporting_files"].items():
        path = source.parent / relative
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != digest:
            errors.append(f"Supporting source changed/missing: {relative}")
    for path in folder.rglob("*.md"):
        prose = path.read_text()
        if not prose.endswith("\n"):
            errors.append(f"Missing final newline: {path.name}")
        for number, line in enumerate(prose.splitlines(), 1):
            if line.rstrip() != line:
                errors.append(f"Trailing whitespace: {path.name}:{number}")
        if prose.count("```") % 2:
            errors.append(f"Unbalanced fences: {path.name}")
        for target in re.findall(r"\]\(([^)]+)\)", prose):
            if "://" in target or target.startswith("#"):
                continue
            clean = target.split("#", 1)[0]
            clean = re.sub(r":\d+$", "", clean)
            if not (path.parent / clean).exists():
                errors.append(f"Broken local link: {path.name} -> {target}")
    if errors:
        raise SystemExit("\n".join(errors))
    print(f"PASS: {len(files)} source files, {total} declarations; "
          f"{len(manifest['supporting_files'])} supporting fingerprints; "
          "guide routing, links, fences and whitespace checked.")


if __name__ == "__main__":
    main()
