# Spec Submodules

Local specs may live in their own Git repositories and be attached to this template as nested submodules under `specs/`.

This keeps the spec history independent while the template records an exact spec commit.

## Layout

```text
TEMPLATE/
  specs/
    <spec-name>/      # nested submodule pointing to a spec repository
  docs/
    LEVELS.md
    EXCEPTIONS.md
```

## Add a spec repository

If the spec is only local, first create a remote Git repository and push it. A submodule needs a remote URL.

```bash
# inside the template repository
git submodule add <spec-repo-url> specs/<spec-name>
git add .gitmodules specs/<spec-name>
git commit -m "feat(spec): add <spec-name> spec submodule"
```

## Update a spec

```bash
git -C specs/<spec-name> fetch origin
git -C specs/<spec-name> checkout <commit-or-branch>
git add specs/<spec-name>
git commit -m "chore(spec): bump <spec-name> to <short-sha>"
```

## Parent vault pointer

If this template is itself a submodule of a parent vault, the parent only tracks the template commit.
After the template PR is merged, update the parent submodule pointer in a separate parent PR.

## Rules

- Do not copy spec files into the template as a replacement for pinning a submodule.
- Do not point a submodule at an unpushed local commit.
- Do not rewrite a published spec commit used by the template.
- If the spec contains secrets or private data, do not attach it to a public template repository.
