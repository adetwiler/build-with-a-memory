# 4. Research first

## What it is

Before a decision you cannot un-make cheaply, you research it, and the research gets committed. A researcher agent (or you) gathers findings onto a `research/` shelf: what the options are, what other people found, what the tradeoffs actually are, with links. Then the decision cites the shelf instead of resting on a hunch.

The shelf is a real folder in the repo, not a chat you will lose. Findings are facts with sources. The decision that follows points back at them.

## Why it works

The expensive decisions are the ones that are hard to reverse: a data model, a core dependency, a "we are going to be the kind of product that does X." Getting one of those wrong is not a quick fix. Spending an hour on evidence before you commit is cheap insurance against a month of building the wrong thing.

Committing the research is what separates this from "I looked into it once." A chat window is gone tomorrow. A `research/landscape.md` with links is there when a future session asks "did we consider Y?" and can read the answer instead of re-searching. Research once talked me out of an entire product. That finding was worth keeping, because the temptation to rebuild the same idea comes back, and the shelf answers it before I waste the week again.

Separating research from decision also keeps the two honest. Research is allowed to be open-ended and cite competitors freely. The decision is a commitment. Keeping them in different files means the decision stays crisp and the evidence stays browsable.

## How to do it today

1. Make a `research/` folder with a `README.md` that says what it is: public-facts-only findings that decisions cite. See [research/README.md](../research/README.md) for the shape.
2. Before a hard-to-reverse call, write (or have an agent write) a findings file: the question, the options, what each costs, links to real sources. Keep opinions labeled as opinions.
3. When you make the decision, cite the file. The ADR (pillar 5) names the research it rested on.
4. Keep the shelf public-safe if the repo might ever go public: facts and links, not strategy or numbers you would not say out loud.

Minimal example of a shelf entry's head:

```
# Findings: which queue for the job pipeline

Question: durable job delivery, at-least-once, no self-hosting.
Options considered: A (managed HTTP delivery), B (self-hosted broker), C (cron).
Sources: <link>, <link>, <link>.
Leaning: A. B adds ops we do not want; C cannot retry cleanly.
```

## Failure modes

- **Research theater.** Gathering links to justify a decision already made. The shelf only helps if it can actually change your mind.
- **Uncommitted research.** Findings that live in a chat are findings you will re-derive. Land them in the folder.
- **Research everything.** Not every call needs a shelf entry. Reserve it for the ones that are expensive to reverse. A one-line change does not need a landscape review.

## The cheap way to run this

Committed research is the cheap path: the shelf is written once and cited forever, while re-searching the same question is the expensive one. The gathering itself is also a fine job for a cheaper model or a background agent, because collecting sources is mechanical. Save the strong model (and yourself) for weighing the findings and making the call.

## What it costs honestly

The hour up front, and the discipline to write findings down when you would rather just start building. Sometimes the research says "the thing you were excited about is a bad idea," and that is a real cost: it can kill momentum on something you wanted to be true. That is also the point. The shelf is worth most exactly when it tells you something you did not want to hear, because that is the decision that would have hurt to get wrong.
