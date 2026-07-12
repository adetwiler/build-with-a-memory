<!--
TEMPLATE: wide-network/README.md - the operating note for your personal,
cross-project memory. Copy this into your personal memory directory (the home
your agent tool loads outside any single repo). It explains the two-tier pointer
pattern to any agent that reads it. Delete this comment once it is yours.
-->

# Wide network - personal, cross-project memory

This is the memory that does not belong to any one repo. Facts about how I work,
gotchas about tools I use across projects, and pointers to every per-repo network
I keep. It links to the repo networks. It does not absorb them.

## The one rule: one home per fact, signposts everywhere else

A fact lives in exactly one place. Everywhere else that needs it holds a POINTER
to that place, never a copy. Two copies drift. A pointer cannot. When a repo needs
a fact that lives here, the repo links here. When this network needs a project
detail, it links into that repo. No fact is written twice.

## What goes here vs. in a repo

- **Here (wide):** who I am and how I work, preferences that follow me into every
  project, and gotchas that span projects (a tool-level quirk, an email-rendering
  rule, an API-key location).
- **In a repo:** anything specific to that one project (its schema, its
  conventions, its decisions). That commits with the code and ships with it.

When unsure, ask "personal or project?" before writing. Getting the home right at
write time is far cheaper than untangling a misplaced fact later.

## How it is organized

- `MEMORY-NETWORKS.md`: the top-level map. One line per network (this one and
  every per-repo network), each pointing at where it lives. Read it to LOCATE the
  right network, then open only that one.
- `memory/` (or wherever your tool keeps notes): one file per fact or topic,
  short, linked to related notes rather than duplicating them.
