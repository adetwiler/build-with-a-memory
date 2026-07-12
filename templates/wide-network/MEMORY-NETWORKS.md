<!--
TEMPLATE: MEMORY-NETWORKS.md - the top-level map of every memory network you own.
Copy this into your personal memory directory alongside its README. One row per
network (this wide one and every per-repo one), each with a one-line "when to read"
and where it lives. This is what an agent scans to LOCATE the right network before
opening any of them. Delete this comment and the examples once it is yours.
-->

# Memory networks - the map of maps

Every memory network I keep, personal and per-repo. Read a row to find the right
network, then open only that one. One home per fact: if two rows seem to cover the
same fact, one of them is a pointer, not a copy.

| Network | When to read | Where it lives |
|---------|--------------|----------------|
| Wide (personal) | A fact about how I work, or one that spans projects | this directory |
| `<project-a>` | Working in project A | `<path-to-project-a>` (its `docs/context-map.md`) |
| `<project-b>` | Working in project B | `<path-to-project-b>` (its `docs/context-map.md`) |

<!--
Example rows (delete these):
| Studio games | Building or shipping any game | ~/games/ (README is the chain root) |
| The web app | Anything in the main product repo | ~/sites/app/ (docs/context-map.md) |
-->

## Cross-project facts

A fact that spans projects (a tool quirk, a preference, an integration gotcha)
lives ONCE in the wide network, with a pointer from each repo that needs it. Do
not duplicate it into every repo. One home, many signposts.
