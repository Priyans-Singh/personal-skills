# Personal skills

Versioned snapshots of my locally installed personal skills, including scaffolded library references, supporting scripts, assets, and agent metadata.

## Layout

- `agents/skills/`: skills from `~/.agents/skills`.
- `codex/skills/`: skills from `~/.codex/skills`.
- `skill-inventory.json`: skill names grouped by installation location.

Both installations are preserved independently, including skills that exist in both. Bundled `.system` skills, plugin caches, environment files, and generated caches are excluded. The installed folders remain in place; edits there must be refreshed into this repository before committing.

## Save future edits

From this repository:

```sh
python3 scripts/refresh.py
python3 scripts/refresh.py --apply
git diff
git add .
git commit -m "Update personal skills"
git push
```

The first command previews changes. `--apply` mirrors installed skills into the repository, including deletions. It refuses to overwrite uncommitted repository changes. Review the diff before committing, especially because the GitHub repository is public.

## Personal GitHub identity

The remote uses the local SSH alias configured for my personal key:

```text
git@github.com-personal:Priyans-Singh/personal-skills.git
```

If the key is locked on macOS:

```sh
ssh-add --apple-use-keychain ~/.ssh/id_ed25519_github_personal
```

Source locations and versions in individual library references describe the machine and library installation used to create them. They may need updating on another machine. Individual skills retain any existing attribution and licensing information.
