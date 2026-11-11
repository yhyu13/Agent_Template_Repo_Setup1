# L1 — Local draft

Module: `L1-local-draft` · Label: `level/L1` · Status: enabled by default

Everything stays on the local machine inside an isolated worktree or branch.
Nothing leaves the workstation; `main` is never touched.

## Do

- Create an isolated worktree / feature branch.
- Edit local files freely within the agreed scope.
- Run local tests and linters.
- Update the exception issue with findings or blockers.

## Don't

- Commit or push anything.
- Open a PR.
- Merge, or touch `main` in any way.
- Change governance files or repo settings.

## Escalate / exit

- When the draft is ready for review, ask for L2 via the exception issue
  (`kind/approval`) or the task instruction; a human authorizes push + PR.

## Exceptions

Reporting is allowed at every level: it writes to the control plane
(GitHub issue), never to product code.
