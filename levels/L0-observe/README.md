# L0 — Observe

Module: `L0-observe` · Label: `level/L0` · Status: enabled by default

The entry level for any agent on a new repo or task: understand before touching.
L0 grants read access only; every mutation of the repository is out of scope.

## Do

- Read the repo, docs, issues, and existing PRs.
- Inspect CI runs, logs, and check results.
- Draft a plan (local text only — not committed).
- Open or update an exception issue when blocked, via `scripts/exception_inbox.py`.

## Don't

- Edit product files.
- Commit, push, or open a PR.
- Merge anything.
- Change repo settings or governance files.

## Escalate / exit

- If the task requires any mutation, stop and open an exception issue
  (`kind/scope`). A human grants L1+ explicitly; an agent never promotes itself.

## Exceptions

Reporting is allowed at every level: it writes to the control plane
(GitHub issue), never to product code.
