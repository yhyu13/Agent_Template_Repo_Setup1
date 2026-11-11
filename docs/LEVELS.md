# Autonomy Levels — Do / Don't MVP

This template uses levels to describe how much an agent may do without asking a human.
Levels are not a substitute for branch protection, required checks, or review.

Default MVP enablement: **L0–L3 are usable now; L4–L5 are documented but disabled until the owner explicitly enables them.**

Exception reporting is allowed at every level because it writes to the control plane (GitHub issue), not to product code.

## Level table

Every level lives under `levels/` as its own module with an independent,
unique leaf name. The full Do / Don't / escalation content for a level is in
its module README — this table is only the index.

| Level | Module | One-line scope |
|---|---|---|
| L0 | [levels/L0-observe](../levels/L0-observe/README.md) | Read and plan only; no mutation of the repository. |
| L1 | [levels/L1-local-draft](../levels/L1-local-draft/README.md) | Local worktree / branch edits and local tests; nothing leaves the machine. |
| L2 | [levels/L2-branch-pr](../levels/L2-branch-pr/README.md) | Push feature branch, open draft PR, run CI, attach evidence. |
| L3 | [levels/L3-green-merge](../levels/L3-green-merge/README.md) | Merge only fully green, in-scope PRs with complete evidence. |
| L4 | [levels/L4-bounded-repair](../levels/L4-bounded-repair/README.md) | Bounded autonomous recovery: retries, rebase, mechanical fixes. |
| L5 | [levels/L5-policy-proposal](../levels/L5-policy-proposal/README.md) | Propose governance changes; nothing bypasses review. |

Module naming rule: `<level>-<slug>` (for example `L2-branch-pr`). The leaf
name is the module's unique identity across the template; any module may later
be promoted to its own repository and attached as a submodule, following
[docs/SPEC_SUBMODULES.md](SPEC_SUBMODULES.md).

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
