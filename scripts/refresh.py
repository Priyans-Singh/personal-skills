#!/usr/bin/env python3
"""Preview or mirror local non-system skill installations into this repository."""

import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parent.parent
IGNORE = shutil.ignore_patterns(
    ".DS_Store", ".git", "__pycache__", "*.pyc", "*.pyo",
    ".venv", "venv", "node_modules", ".env", ".env.*",
)


def files(folder):
    return {
        str(p.relative_to(folder)): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in folder.rglob("*") if p.is_file()
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="Apply the previewed mirror changes")
    args = parser.parse_args()
    if args.apply:
        status = subprocess.check_output(
            ["git", "status", "--porcelain"], cwd=ROOT, text=True,
        )
        if status.strip():
            parser.error("Commit or stash repository changes before refreshing.")

    with tempfile.TemporaryDirectory(prefix="personal-skills-") as staging:
        stage = Path(staging)
        inventory = {}
        for label in ("agents", "codex"):
            source = Path.home() / f".{label}" / "skills"
            if not source.is_dir():
                parser.error(f"Source folder is missing: {source}")
            inventory[label] = []
            target = stage / label / "skills"
            target.mkdir(parents=True)
            for skill in sorted(source.iterdir()):
                if skill.name.startswith(".") or not skill.is_dir():
                    continue
                if not (skill / "SKILL.md").is_file():
                    parser.error(f"Missing SKILL.md: {skill}")
                if skill.is_symlink() or any(p.is_symlink() for p in skill.rglob("*")):
                    parser.error(f"Symlinks require manual review: {skill}")
                shutil.copytree(skill, target / skill.name, ignore=IGNORE)
                inventory[label].append(skill.name)

        (stage / "skill-inventory.json").write_text(json.dumps(inventory, indent=2) + "\n")
        changes = []
        for label in ("agents", "codex"):
            old, new = files(ROOT / label), files(stage / label)
            for name in sorted(old.keys() | new.keys()):
                if old.get(name) != new.get(name):
                    kind = "added" if name not in old else "removed" if name not in new else "changed"
                    changes.append(f"{kind}: {label}/{name}")
        if (ROOT / "skill-inventory.json").read_bytes() != (stage / "skill-inventory.json").read_bytes():
            changes.append("changed: skill-inventory.json")
        print("\n".join(changes) if changes else "Skills are up to date.")
        if args.apply and changes:
            for label in ("agents", "codex"):
                destination = ROOT / label / "skills"
                if destination.exists():
                    shutil.rmtree(destination)
                shutil.copytree(stage / label / "skills", destination)
            shutil.copy2(stage / "skill-inventory.json", ROOT / "skill-inventory.json")
            print("Refreshed. Review git diff before committing.")


if __name__ == "__main__":
    main()
