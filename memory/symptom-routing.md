# Symptom routing — "the user says X → open these files"

One line per reported problem, written in **the user's own words**. They will
search by their words, not yours. This table is the difference between debugging
once and debugging the same thing every session.

## Format

```
- <symptom as the user phrases it>: `path/to/file`, `path/to/other`
```

## Rules

- **Add the line in the same PR that fixes the symptom.** A fix without a line
  will be re-debugged by the next agent; that is the whole point of the file.
- Order files by likelihood. Three to five is the useful range; ten means the
  symptom is too broad and should be split.
- **Delete stale lines.** When the code a line points at is gone, remove the line.
- Never pre-fill guesses. Only verified routings belong here; uncertain ones go
  to `.agent/inbox/`.

## Entries

<!-- Replace this example with real lines; delete the example as soon as one real line exists. -->
- login redirects to the wrong page: `src/auth/session.ts`, `src/routes/index.ts`
