# Decision Authority — who may decide what

`docs/LEVELS.md` answers *may I act?*. This file answers a different question:
**may I decide this?** The two are independent — an L3 task (auto-merge allowed)
can still contain a Class C decision that nobody authorized.

## Three classes

| Class | Test | Agent may | Must record |
|---|---|---|---|
| **A — code-decidable** | The answer is in the repository: code, tests, schema, logs, existing docs. | Decide and proceed. | One line in the PR: the decision + the `file:line` that settles it. |
| **B — facts not in the repo** | Needs something the repository cannot contain: a real device, the real network, production data, the user's intended wording, a business rule nobody wrote down. | Ask **one** minimal question set, then stop. | The question set in the issue; the answer quoted back before acting. |
| **C — product / experience direction** | Several options are acceptable, and no fact can break the tie. | Present 2–3 options with their consequences. Do not pick. | Options + a recommendation in the issue or PR; the human decides. |

## Four hard rules

1. **Do not demote C to A because the answer "seems obvious".** This is the
   highest-yield source of rework: the copy tone gets reversed, the threshold
   gets re-specified, and the whole direction flips after the work is done.
2. **One round of questions only.** If the answer still does not settle it,
   escalate to Class C (options) instead of asking again. Multi-round
   interrogation in an issue thread is a failure mode, not diligence.
3. **Questions must be answerable with an artifact**: paste the toast text,
   attach a screenshot, name the device and OS, quote the two conflicting rows.
   Never "what do you think?" — that answer cannot be verified.
4. **Silence is not approval.** A Class B stop stays a stop. Class A work may
   continue around it, but nothing that depends on the answer.

## Decision table (paste into the issue or PR)

| # | Decision | Class | Settled by | Owner |
|---|---|---|---|---|
| 1 | <what was decided> | A | `path/to/file.ts:120` | agent |
| 2 | <what is still open> | B | — (question set posted) | user |
| 3 | <what needs a direction> | C | — (options posted) | user |

A reviewer reads this table to check one thing: *was a judgement made that
nobody was authorized to make?*

## Anti-patterns

- Asking in the issue thread round after round instead of posting one question set.
- Picking copy, naming, pricing, or "how strict should this be" alone. Those are C.
- Labelling a product trade-off as a technical choice to keep moving.
- Treating an unanswered Class B/C item as implicitly approved once the PR is green.
