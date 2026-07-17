# 1. The repo is the memory

## What it is

Your project's context does not live in your head, in a chat history, or in a hosted service. It lives in the repository, as committed markdown, next to the code it describes. A fresh agent session reads a small set of files and knows where it is.

The shape has four parts:

- **A lean always-loaded manual.** One short file the agent reads every session (a `CLAUDE.md`, an `AGENTS.md`, whatever your tool loads by default). Only load-bearing rules go here. Keep it small on purpose.
- **A context map.** A "map of maps" that lists every context surface with a one-line "when to read" and a public or internal tag. The agent reads this to locate the one file it needs, then opens only that file.
- **Lazy topic docs.** One file per system or convention, read only when you touch that area. Depth lives here, not in the manual.
- **ADRs.** Numbered decision records that hold the "why" behind the choices, so nobody re-litigates a settled call.

## Why it works

A model has a context window, not a memory. Anything not in the window this turn is gone. If your project knowledge is committed and indexed, the agent can pull exactly the slice it needs and skip the rest. You are not paying to re-derive the schema every session. You are not re-explaining why the auth path is the way it is.

It also survives the thing hosted memory cannot promise: tool changes. Plain markdown works with any agent today and any agent next year. When you switch tools, your memory comes with you because it never left your repo.

The always-loaded manual has to stay lean for a real reason. It is in the window every single turn, so every line you add there is a tax on every interaction forever. The context map exists so the manual can stay small: instead of front-loading forty files, you load one index and navigate.

## How to do it today

1. Make one file your tool auto-loads (`CLAUDE.md` or `AGENTS.md`). Put in it: what the project is (two sentences), the tech stack, and the three or four rules that, if broken, cause real damage. Nothing else.
2. Make a `docs/context-map.md`. List each doc you have with a one-line "when to read." Tag each `public` or `internal`. See [templates/context-map.md](../templates/context-map.md).
3. The first time you explain a subsystem to an agent, write it to `docs/<topic>.md` instead of explaining it again next week. Add a row to the map.
4. Tell the agent, in the manual: "orient by the map, do not grep."

Minimal example of the manual's topic index:

```
| Working on…        | Read                    |
|--------------------|-------------------------|
| The database       | docs/db.md              |
| Auth               | docs/auth.md            |
| Any decision's why | docs/adr/               |
```

## Failure modes

- **The manual bloats.** Every agent wants to add "one more rule." Move detail to a topic doc and leave a one-line rule behind. If the manual is longer than a screen or two, it has drifted.
- **The map goes stale.** A doc gets written and never indexed, so no session finds it. Folding the map update into "done" fixes this.
- **Docs contradict code.** The worst outcome, because now the memory lies. The rule that saves you: when you notice drift, fix it in the same pass, or flag it if you are not sure which side is wrong.

## The cheap way to run this

This pillar is already the efficiency move; run it as designed and it pays for itself. The lean manual matters because it is a tax on every single turn, so audit it occasionally and evict anything that stopped earning its line. And hold the "orient by the map" rule firmly: a session that front-loads ten topic docs to answer a one-doc question is spending your money on nothing.

## What it costs honestly

It costs discipline, not much else. You write the doc the first time you would have explained the thing anyway, so the marginal cost is small. The real cost is the habit of routing each new fact to a home instead of letting it evaporate into a chat log. If you skip that, the network hollows out and you are back to re-explaining. The upkeep is real. It is also the cheapest part of the whole method.
