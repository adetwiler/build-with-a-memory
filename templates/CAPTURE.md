<!--
TEMPLATE: CAPTURE.md - the capture-as-you-go rule, phrased as a drop-in agent
instruction. Paste this block into your always-loaded manual (CLAUDE.md /
AGENTS.md) so the agent captures durable facts automatically, mid-work, without
being asked. Delete this comment when you paste it.
-->

## Capture as you go (standing rule)

When something durable and reusable surfaces during work that is not already
written down, route it to its ONE home in the same session. This is part of
"done," not a separate chore. Do it automatically. Do not wait to be asked.

**Capture when:** a gotcha cost real time, a convention has now been repeated
twice, a decision was settled, or a fact would otherwise be re-derived by a
future session. Gotchas especially: document them mid-build, on your own.

**Do not capture:** one-off trivia, anything already documented, or a restatement
of an existing doc. Keep the bar high and the noise low.

**Route to one home:**
- A convention or subsystem detail → the relevant `docs/<topic>.md` (add a map row).
- A decision → a new ADR in `docs/adr/`.
- A small loose end or open question → `OPEN.md`.
- A homeless cross-cutting fact → `docs/notes.md`.
- A personal or cross-project fact → the wide network, not this repo.

**Keep it short and linked, never duplicated.** Check for an existing home before
making a new one. Link related notes rather than copying them. If you are less
than sure a fact is personal or project, ask "personal or project?" before writing.

**Structural changes get a heads-up.** A new topic doc or a captured line just
goes in. Renaming or splitting the network, or a new cross-cutting rule, gets a
quick check with the human first.
