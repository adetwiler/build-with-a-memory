# 3. Capture as you go

## What it is

When something durable surfaces mid-work (a gotcha, a settled convention, a fact a future session would otherwise re-derive), you write it down in the same pass, routed to its one home. Not later. Not in a cleanup sprint. Now, while it is in front of you.

Gotchas especially. The moment you lose time to a non-obvious thing, that lost time becomes a few lines of documentation before you move on. The agent does this automatically, without being asked, as part of "done."

## Why it works

The knowledge you most want to keep is the knowledge that is hardest to recover: the thing that fought you for an hour and then worked. In the moment you understand exactly why. A week later you remember that it was annoying and nothing else. Capture closes that gap while the understanding is still whole.

Doing it in the same pass matters because a separate "documentation phase" never happens. It gets deferred, then skipped, then the knowledge is gone. Folding capture into the work itself (part of finishing, not a chore after finishing) is the only version that survives contact with a busy week.

The reason it can be automatic is that routing is mechanical once the network exists. Each kind of fact has a home: a convention goes to the topic doc, a decision to an ADR, a loose end to an open-items list, a homeless fact to a small overflow file. The agent does not have to decide whether to capture. It has to decide where.

## How to do it today

1. Give your agent a standing instruction: when a durable, reusable fact surfaces that is not already written down, route it to its one home in the same session. See [templates/CAPTURE.md](../templates/CAPTURE.md) for a drop-in version.
2. Name the homes so routing is unambiguous: conventions to topic docs, decisions to ADRs, small loose ends to an `OPEN.md`, homeless facts to a `docs/notes.md`.
3. Keep the bar sane. This is not a checklist on every trivial edit. It is for the thing a future session would otherwise re-derive, including a convention you have now repeated twice.
4. Keep each capture short and linked, not duplicated. A capture that restates three other docs is noise.

Minimal example of a captured gotcha, dropped into the relevant topic doc:

```
> Gotcha: the build strips a plain space after an inline tag, so text glues
> to the previous word. Use the explicit-space escape your framework provides.
> Cost us an afternoon before we saw it. Always eyeball rendered output.
```

## Failure modes

- **Capture everything.** Over-capture buries the load-bearing facts under trivia. The bar is "a future session would re-derive this," not "this happened."
- **Capture nowhere.** A fact dropped into the chat instead of a file is not captured. It has to land in a committed home.
- **Duplicate capture.** The same gotcha in four files is the drift problem again. Check for an existing home before making a new one.

## What it costs honestly

A minute or two per capture, in the middle of doing something else, which is exactly when you least want to stop. That friction is the whole cost, and it is why most people do not do it. The trade is that minute now against the hour later when a future session (maybe yours) hits the same wall with no memory of the first time. The method only compounds if capture is a reflex. If it is a someday task, you get a pile of code and no memory of why any of it is the way it is.
