# The scaffold

Build the person's files from their interview answers. Add-only, everywhere: if
a file exists, read it and add what is missing; never overwrite, never delete.

## Where things live

Pick the row for the agent they named in Question 1. `HOME` means their user
folder; [platforms.md](platforms.md) has the per-OS spelling of every path.

| Agent | Personal file | Memory folder |
|---|---|---|
| Claude Code | `HOME/.claude/CLAUDE.md` | `HOME/.claude/memory/` |
| Cursor | `HOME/.cursor/rules/personal.md` (global rule) | `HOME/.cursor/memory/` |
| Anything else | `HOME/agent-memory/PERSONAL.md` | `HOME/agent-memory/memory/` |

If they use more than one agent, scaffold the main one fully, then create the
other agent's personal file as a two-line pointer to the main one, the same
trick the repo prompt uses for CLAUDE.md and AGENTS.md.

## 1. The personal file

Write it short; a stranger should read it in about a minute. Their words, their
voice, tightened but never translated into jargon they did not use. Sections:

```
# <Their name or handle>

<One or two sentences: who they are, what they build. From Question 2.>

## Rules
<Their answers from Question 3, one bullet each, in their words.>

## Memory
- My memory lives in <memory folder>. Read MEMORY.md there at the start of a
  session when context would help; it is the index.
- When we settle something durable (a decision, a preference, a gotcha), write
  it to a file in the memory folder and add one line to MEMORY.md, in the same
  session it happens. This is part of the work, not a separate chore.
```

**Standalone mode (employer's or client's machine) adds one rule, verbatim:**

```
- This machine belongs to my employer/client. Keep all personal memory
  machinery inside my own user folder. Never add memory files, hooks, or
  agent config to a repo I do not personally own.
```

## 2. The memory folder

Create the folder, plus:

- **`MEMORY.md`**: the index. Start it with a heading, one line per memory
  file. Seed it with a pointer to the focus file below.
- **`focus.md`**: their Question 4 answer, dated. What they are in the middle
  of, written so a fresh session tomorrow could pick it up cold.
- **`handoffs/`**: an empty folder (only if they kept `handoff`).
- **`ideas/`** with an **`ideas/INDEX.md`** one-line header (only if they kept
  `idea`).

## 3. The habits

For each habit they kept, add its block to the personal file under a
`## One-word habits` heading. These are instructions their agent follows; there
are no scripts and nothing to install.

```
## One-word habits
- If I say just "handoff": write a dated file in <memory folder>/handoffs/
  named YYYY-MM-DD-<slug>.md covering: what happened this session, what is
  still open, and what to do next, written for someone who saw none of it.
  Confirm in one line. Do not ask me questions first.
- If I say "pick up": read the newest file in <memory folder>/handoffs/ and
  continue from its "what to do next" section. Tell me in one line where we
  are resuming from.
- If I start a message with "idea": record it faithfully as a dated file in
  <memory folder>/ideas/, add one line to ideas/INDEX.md, confirm in one
  line, and return to whatever was in flight. Ideas are notes, not tasks.
```

Include only the bullets for the habits they kept.

## 4. Verify, then report

Check every box by reading the actual files back:

- [ ] The personal file exists, reads in about a minute, and contains their
      rules, the `## Memory` section, and the habit blocks they kept.
- [ ] The memory folder exists with `MEMORY.md` and a dated `focus.md`, and
      `MEMORY.md` points to `focus.md`.
- [ ] `handoffs/` and `ideas/INDEX.md` exist for the habits they kept.
- [ ] Standalone mode only: the employer-machine rule is present, and you
      created nothing outside their user folder.
- [ ] Nothing that existed before was overwritten or deleted.

If Node.js happens to be available, you can also run the mechanical check
(optional; the checklist above is the requirement):

```
node scripts/validate-scaffold.mjs <their home folder> [--standalone] [--habits handoff,pickup,idea]
```

Then report: a short list of what was created and where, plus one line per
habit showing how to use it. Nothing else.
