# L5 — Policy proposal

Module: `L5-policy-proposal` · Label: `level/L5` · Status: documented, disabled by default (owner must enable)

The agent participates in governing the system itself — by proposal only.
Every policy change still flows through the normal PR + approval gates.

## Do

- Propose governance / level-boundary changes via PR.
- Improve the exception taxonomy (labels, kinds, routing).
- Prioritize and triage exception inbox issues with recommendations.

## Don't

- Self-approve red changes.
- Disable checks or required workflows.
- Expand own permissions.
- Merge policy changes without the required approval.

## Escalate / exit

- Policy PRs follow the standard merge gates; nothing at L5 bypasses review.

## Exceptions

Reporting is allowed at every level: it writes to the control plane
(GitHub issue), never to product code.
