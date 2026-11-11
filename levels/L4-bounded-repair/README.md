# L4 — Bounded repair

Module: `L4-bounded-repair` · Label: `level/L4` · Status: documented, disabled by default (owner must enable)

Autonomous recovery inside the task's own boundary: retry, rebase, fix
mechanical breakage — without widening scope.

## Do

- Retry failed tests and transient CI failures.
- Rebase and resolve non-semantic (ordinary text) conflicts inside the
  agent's own worktree, then re-run verification.
- Update the branch and re-run CI.
- Merge green after repair (subject to the same L3 green rule).

## Don't

- Change scope, credentials, budget, governance, or protected settings.
- Self-approve red changes.

## Conflict policy

Ordinary text merge conflicts are not automatically red: an agent at L4 may
resolve them in its own worktree and re-run verification. Ownership conflicts,
governance conflicts, or failed automatic resolution escalate to `needs-human`.

## Escalate / exit

- Anything outside the repair boundary → stop, open `kind/scope` exception,
  wait for human decision.

## Exceptions

Reporting is allowed at every level: it writes to the control plane
(GitHub issue), never to product code.
