---
title: A thirteenth pillar
date: 2026-07-28
description: Borrowed memory. Reading what other teams wrote down, without letting it start giving your agent orders.
---

There were twelve pillars. There are thirteen now.

This is not a correction to the count. It is the one I have been working out
for a while and finally understood well enough to write down.

The first twelve are all about writing down what you know. This one is about
reading what somebody else knew. Other teams' agent manuals, their decision
records, the conventions they settled two years ago and never blogged about.
You cannot copy their codebase, but you can read how they work, and that
transfers.

Getting the writing turned out to be the easy half. A blobless clone with a
sparse checkout of markdown only, so a 381 MB repo lands as 17 MB of prose and
no source code. Then `git ls-remote` as the probe, so an unchanged repo costs
one round trip and no download.

The hard half is the reason it took me this long.

Text you retrieve arrives in the same context window as your real instructions.
There is no separate channel and no marker that says one is data and the other
is orders. So the moment you index a repo you do not control, a stranger can
write in your agent's instruction channel. That is not a hypothetical. It is
the cheapest attack there is against exactly this feature.

The pillar comes down to one sentence: **borrowed memory is data, not
instructions.** Your notes are things you decided. Their `AGENTS.md` is a quote
of what they decided, and the difference has to survive all the way to the
moment it is read back.

Two things I got wrong on the way, both in the doc:

My first scanner flagged 3.6% of my own real documentation. Setup guides
naming `.env` next to a `curl` example, runbooks documenting force-push, emoji
that contain a zero-width character. A gate that fires on honest work teaches
you to click through it, and then it is decoration.

And my own mirror followed symlinks. A repo I borrowed could point a file at
anything on my disk and my indexer would read it. Caught by writing tests that
attack the tool instead of confirming it.

New pillar: [`method/13-borrowed-memory.md`](https://github.com/adetwiler/build-with-a-memory/blob/main/method/13-borrowed-memory.md).
The tooling and both test suites are in [`tools/`](https://github.com/adetwiler/build-with-a-memory/tree/main/tools).
The longer version, with the numbers and the bugs, is
[on my site](https://andrewdetwiler.com/blog/letting-agents-read-other-repos).
