# Exception Inbox — GitHub Issues, Not Email

The source of truth for exceptions is a GitHub issue in the task repository.

Do not use email, mobile push, chat-only messages, or local-only files as the exception inbox.
Humans may receive notifications, but agents must be able to reconstruct the exception from GitHub issue data.

## Labels

| Label | Meaning |
|---|---|
| `agent-exception` | Base label for all exception issues. |
| `agent-actionable` | An agent may inspect and attempt the next step within its level. |
| `needs-human` | A human decision is required. Silence is not approval. |
| `kind/evidence` | Missing or invalid verification evidence. |
| `kind/conflict` | Merge or ownership conflict. |
| `kind/approval` | Approval is required or expired. |
| `kind/tooling` | Tool, runner, auth, or environment failure. |
| `kind/scope` | Task exceeds allowed scope or level. |
| `kind/other` | Other exception. |
| `level/L0` … `level/L5` | Autonomy level associated with the exception. |

## Issue identity and dedupe

Every exception issue body must contain a stable marker:

```markdown
<!-- agent-exception-key: <sha256> -->
```

The key is derived from repository, task id, kind, and scope. It does not include head SHA or timestamp.
When the same exception happens again, update the existing issue with a comment instead of creating a duplicate.

## Agent loop

```bash
python scripts/exception_inbox.py watch --repo owner/repo --actionable agent --once
```

For each returned issue:

1. Read the issue body and latest comments.
2. Check the current task level and scope.
3. If the action is allowed, perform the smallest next step.
4. Comment on the issue with command, result, evidence, and next state.
5. Do not close the issue unless the user explicitly authorizes closure.

## Human decision format

A human can reply in the issue with a structured comment:

```markdown
decision: approve | reject | retry | needs-info
scope: <paths or task scope>
head_sha: <sha if approval is bound to a commit>
reason: <why>
```

Agents must verify that the decision covers the current head/scope before acting.

## Report command

```bash
python scripts/exception_inbox.py report \
  --repo owner/repo \
  --task-id task-123 \
  --agent-id cindy \
  --session-id session-abc \
  --level L2 \
  --kind evidence \
  --summary "Missing iPad evidence" \
  --details "Same-version iPad verification is missing." \
  --actionable human
```

Use `--dry-run` to inspect the issue payload without writing to GitHub.
