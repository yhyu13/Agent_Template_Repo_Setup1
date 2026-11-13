# Invariants — constraints that must not drift

One bullet per rule that a confident refactor could silently break. Each bullet
carries three things: the rule, why it exists, and how to check it.

## Format

```
- **<rule>** — because <the incident or reason>; check: <command or code path>
```

## Rules

- Verified facts only. A suspected invariant goes to `.agent/inbox/` first.
- No history, no story. A bullet that needs a paragraph to explain belongs in
  `docs/`, not here.
- When a deliberate decision breaks a bullet, **rewrite the bullet in the same
  PR**. Leaving the old claim in place is how an invariants file becomes noise.
- Fewer and sharper beats complete. Fifteen bullets is already a lot; past that,
  the file stops being read.

## Entries

<!-- Replace this example with real bullets; delete the example as soon as one real bullet exists. -->
- **Every read of a soft-deleted entity filters the deleted flag** — because
  deleted rows resurface in counts and lists; check: `grep -rn "findMany" src/`
  for reads that omit the filter.
