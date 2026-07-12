# ADR 0001: Founding decisions for this method repo

**Status:** Accepted
**Date:** 2026-07-12

This repo eats its own cooking. The method says decisions get recorded as ADRs
that name the alternatives they beat, so the decisions behind the repo itself are
recorded here. This ADR is deliberately generic: it names no private venture, no
numbers, no strategy.

## Context

I wanted to publish the way I work with AI coding agents as authority content for
a public audience: a working developer sharing what works, not a framework vendor.
Several calls had to be settled before writing, and I did not want to re-open any
of them mid-draft.

## Decisions

**1. The name is "Build With a Memory."**
It states the whole idea in three words: the repository remembers so the agent
does not start from nothing.
Alternatives it beat: a tool-style name (implies software you install, which this
is not); a generic "AI memory" title (crowded, says nothing specific).

**2. The lead wedge is decision-cache economics.**
The sharpest, most defensible claim is that accumulated memory lowers the cost of
every future review, because a decision recorded once is never re-derived. That
is the argument the deepest doc is built around.
Alternatives it beat: leading with "organize your docs" (true but unremarkable);
leading with the multi-agent tooling (impressive but not the durable insight).

**3. Personal-GitHub home, local-first until the owner flips it public.**
The repo is built and committed locally, reviewed by the owner, and made public by
the owner by hand. No automated publish, no pushing on the owner's behalf.
Alternatives it beat: publish-on-build (removes the human gate this whole method
insists on); an org home (this is one person's method, stated in one person's
voice).

**4. Day-one scope is the method plus templates.**
Ship the written pillars, clone-able templates, the research shelf, and the
mechanical gates. Nothing more.
Alternatives it beat: shipping a CLI or generator (turns the anti-product into a
product); shipping example projects (heavy, and risks leaking private context).

**5. Proof is anonymized before/after only, each real number owner-approved.**
Anecdotes stay fully generic (a tool I build, my roguelite, research that talked
me out of a product). Any real metric is left as a visible placeholder for the
owner to approve individually, never invented.
Alternatives it beat: concrete numbers written from memory (leak risk, accuracy
risk); no proof at all (weaker, but safer than fabrication).

**6. Written-first serialization.**
The method is delivered as writing, not video or a course. Docs are the artifact.
Alternatives it beat: a video series (higher production cost, harder to keep
current); a paid course (contradicts the anti-product, anti-gatekeeping stance).

**7. Kill criteria fold into an existing periodic review, not a new ritual.**
Whether to keep investing in this is judged at a review the owner already runs,
not a standalone process that would itself need upkeep.
Alternatives it beat: a dedicated cadence (more overhead than the repo is worth);
no review at all (no honest exit).

**8. The scrub gate is three walls: hooks, an adversarial audit, and owner review.**
A pre-commit hook blocks the obvious tells per commit; a full-tree audit script
runs before any publish; the owner reads it before it goes public. Belt, braces,
and a human.
Alternatives it beat: a single check (one gate is one point of failure for a
public repo carrying a private author's context); trust-the-author (the author
moves private context all day and does not trust himself to catch every leak).

**9. The devlog is an in-repo, RSS-subscribable feed, published on accept through a daily review gate.**
Writing in public should be committing a markdown file, not standing up a
separate blog. Posts live in `posts/` as dated markdown; a zero-dependency script
builds `feed.xml` at the repo root; a post reaches the feed only after a daily
human review. The feed is part of the repo, so there is no separate blog service
to run or trust.
Alternatives it beat: a hosted blog or newsletter platform (separate
infrastructure, another account, memory that lives off the repo); auto-publish on
commit (removes the human gate this whole method insists on).

## Consequences

- Every later structural decision about this repo gets its own ADR or an update
  here, so the record stays the source of truth.
- The devlog feed (`feed.xml`) is regenerated from `posts/` by
  `scripts/make-feed.mjs` and committed with the posts. Nothing reaches the feed
  without the daily review.
- The mechanical gates (`.githooks/`, `scripts/leak-audit.sh`) must stay green,
  including on the author's own commits. They are not decoration.
- Nothing publishes without the owner's explicit action. Automation stops at the
  local commit.
