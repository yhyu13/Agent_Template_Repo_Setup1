# Autonomy Levels — Do / Don't MVP

This template uses levels to describe how much an agent may do without asking a human.
Levels are not a substitute for branch protection, required checks, or review.

Default MVP enablement: **L0–L3 are usable now; L4–L5 are documented but disabled until the owner explicitly enables them.**

Exception reporting is allowed at every level because it writes to the control plane (GitHub issue), not to product code.

## Level table

| Level | Name | Do | Don't |
|---|---|---|---|
| L0 | Observe | Read repo/docs/issues; inspect CI; draft a plan; open/update an exception issue when blocked. | Edit product files; commit; push; open PR; merge; change repo settings. |
| L1 | Local draft | Create isolated worktree/branch; edit local files; run local tests; update exception issue. | Commit; push; open PR; merge; touch main; change governance. |
| L2 | Branch + PR | Commit and push feature branch; open draft PR; run CI; attach evidence; update exception issue. | Merge PR; close task issue; force-push main; bypass checks; change governance. |
| L3 | Green auto-merge | Merge a PR only when all required checks pass, evidence is complete, and the task is green; comment result on issue. | Merge yellow/red without approval; bypass checks; force-push main; expand scope. |
| L4 | Bounded repair | Retry failed tests; rebase and resolve non-semantic conflicts; update branch; re-run CI; merge green after repair. | Change scope, credentials, budget, governance, or protected settings; self-approve red. |
| L5 | Policy proposal | Propose governance/level changes via PR; improve exception taxonomy; prioritize issues. | Self-approve red changes; disable checks; expand own permissions; merge without required approval. |

## Green / Yellow / Red overlay

Levels describe autonomy. Risk/approval is still classified separately:

- **Green**: no critical path, no unresolved conflict, complete automated acceptance, same-version/same-platform verification. May merge without human approval only if the current level allows merge.
- **Yellow**: not red, but evidence is incomplete or shared-canonical impact exists. Agent should first try to complete evidence. If it cannot, open/update a `needs-human` exception issue and wait for one human decision.
- **Red**: critical governance/distribution paths, permission/release risk, unresolved ownership conflict, or unsafe/unrecoverable state. Agent must not merge. Open/update a `needs-human` exception issue and wait for admin decision.

Ordinary text merge conflicts are not automatically red. An agent at L4 may try to resolve them inside its own worktree and re-run verification. Ownership conflicts, governance conflicts, or failed automatic resolution escalate.

## Level transitions

An agent must not promote itself to a higher level. A human or protected policy must record the allowed level for the task.

If a task exceeds the current level:

1. Stop the out-of-scope action.
2. Open or update an exception issue using `scripts/exception_inbox.py`.
3. Continue only after an explicit issue comment or task instruction authorizes the next step.
