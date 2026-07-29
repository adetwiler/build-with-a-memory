---
title: The network knew why, but not what
date: 2026-07-29
description: Pillar 14. A memory network records decisions well and current state badly, and the gap is where agents guess.
---

I got the same correction twice in one night.

Two different audit agents told me a game's new version was live on Steam. It
was not. The store was serving last year's build, and the new one was sitting
in the repo waiting on my sign-off. Both agents looked at the repo, saw the
version number, and filled the gap with it, because the repo is where agents
look and nothing anywhere recorded what players were actually being served.

I asked what else had that shape and the answer was: most of my recent agent
confusion. Nothing recorded who else was working in a repo at that moment.
Nothing recorded when a metrics collector started, so "give me three weeks of
trend" was silently unanswerable. Three press kits existed, fully documented,
and zero pages linked any of them, and nothing surfaced that either.

The pattern under all of it: my network records decisions carefully and state
not at all. What I chose and why, written down forever. What is true right
now, assumed. Decisions are durable so they get writing. State is ambient so
it does not.

So there is a fourteenth pillar now:
[State, not just decisions](https://github.com/adetwiler/build-with-a-memory/blob/main/method/14-state-not-just-decisions.md).
The short version: one `NOW.md` at the top of the network, rewritten instead
of appended, every line dated, stale lines deleted on sight. LIVE split from
DRAFT for anything the world can see. Start dates on anything that collects.

The corollary in it is the part I keep chewing on. The night this happened, I
also watched a documented lesson fail to prevent the exact mistake it
documented, six lines below itself, for the second time in three days. A
written warning only fires if someone reads the right file at the right
moment. So the pillar ends with a rule I am trying to hold myself to: if a
lesson matters, it becomes a check, not a comment. This repo now runs a gate
on its own pillar count, because the count has drifted before, and I trust a
gate more than I trust my memory of being wrong.

Honest label on the tin: this pillar is days old and proven on one project.
That is earlier than I usually publish. But the failure is common, the fix is
ten minutes, and if your agent has ever confidently told you something was
deployed when it was not, you already know whether this one is for you.
