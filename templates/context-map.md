<!--
TEMPLATE: context-map.md - the map of maps.
Copy this to docs/context-map.md. It lists every context surface in your repo so
an agent LOCATES the one file it needs instead of grepping or loading everything.
Each row: where to read, a one-line "when to read," and a public/internal tag so
a scrub pass knows what can ever go public. Keep it current: an unlisted doc is a
doc no session finds. Delete this comment and the examples once it is yours.
-->

# Context map

The index of every context surface in this repo. Scan this to find what is
documented; open only the file you need. Tag key: `public` = safe to publish,
`internal` = never leaves the repo.

| Surface | When to read | Visibility |
|---------|--------------|------------|
| `CONTEXT.md` | You need the project's specific vocabulary | internal |
| `docs/context-map.md` | You need to locate any other surface (this file) | internal |
| `docs/<topic>.md` | You are working in <that subsystem> | internal |
| `docs/adr/` | You need the "why" behind a decision, or are about to reopen one | internal |
| `research/` | You are about to make a hard-to-reverse call | internal |
| `README.md` | You are a newcomer, or writing public copy | public |

## Capturing new context

When a durable fact surfaces, route it to ONE home and add or update its row here:

- A convention or subsystem detail → a `docs/<topic>.md` (add a row above).
- A decision → a new ADR in `docs/adr/`.
- A small loose end → `OPEN.md`.
- A homeless cross-cutting fact → `docs/notes.md`.

When unsure whether a fact is personal or project, ask "personal or project?"
before writing. Project facts commit here; personal ones go to your wide network.
