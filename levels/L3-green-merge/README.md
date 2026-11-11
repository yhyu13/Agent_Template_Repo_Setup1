# L3 — Green auto-merge

Module: `L3-green-merge` · Label: `level/L3` · Status: enabled by default

The agent may merge — but only on a fully green, in-scope task.
The Green / Yellow / Red overlay decides what "green" means here.

## Do

- Merge a PR only when **all** of the following hold:
  - every required check passes;
  - evidence is complete (command output, test summary);
  - the task is green and within the agreed scope.
- Comment the merge result on the task issue.

## Don't

- Merge yellow or red tasks without explicit human approval.
- Bypass or disable checks.
- Force-push `main`.
- Expand scope beyond the task issue.

## Risk overlay (quick rule)

- Green: may merge if the current level allows merge (it does at L3).
- Yellow: complete evidence first; if impossible, open a `needs-human`
  exception issue and wait for one human decision.
- Red: never merge. Open a `needs-human` exception issue and wait for
  admin decision.

## Escalate / exit

- Failed tests or non-trivial conflicts → request L4 (bounded repair),
  which is disabled by default and must be enabled by the owner.

## Exceptions

Reporting is allowed at every level: it writes to the control plane
(GitHub issue), never to product code.
