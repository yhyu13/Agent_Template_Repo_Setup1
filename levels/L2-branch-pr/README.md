# L2 — Branch + PR

Module: `L2-branch-pr` · Label: `level/L2` · Status: enabled by default

The work becomes visible: feature branch is pushed and a draft PR is open.
Merging stays a human (or higher-level) decision.

## Do

- Commit and push the feature branch.
- Open a draft PR referencing the task issue (`Refs #N`).
- Run CI and attach evidence (command output, test summary) to the PR.
- Update the exception issue with progress and blockers.

## Don't

- Merge the PR.
- Close the task issue (issues are closed by the owner only).
- Force-push `main`, or bypass / disable checks.
- Change governance files or repo settings.

## Escalate / exit

- When all required checks pass and evidence is complete, request merge
  authorization (L3) via the exception issue or task instruction.

## Exceptions

Reporting is allowed at every level: it writes to the control plane
(GitHub issue), never to product code.
