# 2. The wide personal network

## What it is

Some facts do not belong to any one repo. How you like commits worded. A gotcha about a tool you use in five projects. Who you are and how you work. These live in a **wide network**: a personal memory that sits outside every project and links to the per-repo networks by pointer.

The load-bearing rule is **one home per fact, signposts everywhere else.** A fact lives in exactly one place. Every other place that needs it holds a pointer to that place, not a copy. A small top-level map indexes every network you have, personal and per-repo, so you (or an agent) can find the right one.

## Why it works

Duplication is how memory rots. The moment a fact lives in two files, they drift, and now you have two answers and no way to know which is current. One home means one source of truth. Pointers mean the other places still lead you there without holding a stale copy.

The split between wide and per-repo matters because the two kinds of fact have different lifetimes and audiences. "This project uses txn-pooled Postgres on port X" belongs to the project and ships with it. "I hate em dashes" belongs to me and follows me into every project. Mixing them means either your personal preferences leak into a repo other people read, or your cross-project knowledge gets trapped in one repo and you re-learn it everywhere else.

## How to do it today

1. Make a personal memory directory outside your projects (your agent tool almost certainly has a home for this). Put an index file at the top: one line per network, personal and per-repo, each pointing at where it lives. See [templates/wide-network/MEMORY-NETWORKS.md](../templates/wide-network/MEMORY-NETWORKS.md).
2. When a fact is clearly about you or spans projects, write it in the wide network. When it is about one project, write it in that repo's network.
3. When you are less than sure which, ask the question out loud: "personal or project?" Getting this right at write time is cheaper than untangling it later.
4. When a repo needs a wide fact, do not copy it in. Drop a pointer: "voice rules live in `<wide path>`."

Minimal example of a wide index entry:

```
- [Email HTML rules](memory/email-html.md) - no flexbox, tables + inline styles, spans every project
- [My commit style](memory/commit-style.md) - imperative mood, why-not-what, no trailing noise
```

## Failure modes

- **Copy instead of pointer.** The tempting shortcut that guarantees drift. If you find the same paragraph in two files, one of them should be a link.
- **The wrong home.** A project-specific fact in the wide network pollutes every project; a cross-project fact trapped in one repo gets re-learned elsewhere. The "personal or project?" question at write time is the guard.
- **No index.** Without the top-level map, the wide network becomes a pile you cannot navigate, which is the exact failure the whole method exists to prevent.

## The cheap way to run this

Pointers are cheaper than copies in tokens, not just in drift: a fact with one home gets loaded once, when it is actually relevant, instead of riding along in every repo's context. Keep the wide index itself to one line per entry so scanning it stays nearly free, and let sessions open a wide file only when the pointer says it applies.

## What it costs honestly

The wide network is the part people skip, because its payoff is slow. You do not feel it in week one. You feel it in month three, when you start a brand-new project and your agent already knows how you like things because the wide network came along. The cost is remembering to route cross-project facts outward instead of dumping everything into whatever repo you happen to be in. That habit takes a while to form. It is worth forming.
