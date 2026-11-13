# memory/ — the agent's routing layer

The first thing an agent reads, and the only place a lesson survives a session.

This is a *lookup table*, not a history. When a line becomes wrong, rewrite or
delete it — a routing table that lies is worse than no table.

## Hot path

| File | Answers |
|---|---|
| [`symptom-routing.md`](symptom-routing.md) | "The user says *X* — which files do I open?" |
| [`invariants.md`](invariants.md) | "What must not drift, no matter what the refactor wants?" |

## Update rules

- A new symptom → **one line** in `symptom-routing.md`.
- A new non-driftable constraint → **one bullet** in `invariants.md`, carrying
  *why* it exists and *how to check* it.
- Both are written in the **same PR as the fix**. Memory added after acceptance
  is memory lost.
- Bar: if the lesson cannot be stated as one line, it is not memory-worthy —
  it belongs in `docs/`, or nowhere.

## Cold path

- `AGENTS.md` — the rules an agent must obey.
- `docs/` — manuals, workflows, long-form explanation.
- Conflict order is fixed in `AGENTS.md`「事实优先级」: current code > `memory/` > old `docs/`.
