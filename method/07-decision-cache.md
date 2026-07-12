# 7. The decision cache

This is the pillar that makes the other nine pay for themselves. Read it slowly.

## What it is

Every settled decision, recorded as an ADR, becomes a cache entry. Once a thing is decided and written down, future work does not re-open it. The judges skip it. The reviewers do not re-derive it. A new change is reviewed against the scoped diff plus a small index of what is already decided, not against the whole repository from scratch every time.

Put plainly: **memory is a decision cache that pays for itself in tokens.** The accumulated ADRs are not documentation you file and forget. They are a lookup table that makes every future review cheaper than the last.

## Why it works: the token economics

Think about what a thorough review actually costs, and how that cost scales.

**The naive way.** Each time you review a change, you (or the reviewing agent) load the whole repo's context to understand it: the architecture, the conventions, the reasons things are the way they are. Then you review the change against all of it. Do this on every change and the cost per review is roughly the size of the whole project, every round. As the project grows, each review gets more expensive, because there is more context to reload. Your review cost rises with the size of what you have built. That is backwards. The more you have built, the more it should cost to review a small change? No.

**The cached way.** The decided things live in ADRs. A reviewer does not reload and re-reason about them. It reads two things: the scoped diff (what actually changed) and a compact index of settled decisions (the research shelf plus the ADR list). Everything already decided is a cache hit: looked up in one line, not re-derived. Only the genuinely new part of the change (the cache miss) gets full attention. Your review cost tracks the size of the change and the size of the index, not the size of the whole project.

The difference compounds. Early on, the two approaches cost about the same, because there is not much decided yet. But every ADR you add is a permanent subtraction from all future reviews. Decision number fifty is not re-argued on change number five hundred. It is a line in the index. So the naive cost curve climbs with project size, and the cached curve stays flat, tracking only the diff. The gap between them is the value of the memory, and it widens for as long as the project lives.

That is the whole argument. **Accumulated memory makes every future review cheaper, because a decision recorded once is a decision never re-derived.** The network is not overhead you carry. It is a cache whose hit rate rises as you work.

## A worked example: an ADR as a cache entry

Say early in a project you decide how money moves through the job pipeline. You grill it (pillar 5), you research the concurrency model (pillar 4), and you write:

```
# ADR 0012: Guard the money pipeline against races

Status: Accepted. Date: <date>.

Decision: Any status write or credit debit uses an atomic guarded update
(claim the row with a precondition, act only on the rows returned). Debits
carry an idempotency key. Never read-then-write across a gap.

Alternatives it beat:
- Application-level lock: adds a dependency and a new failure mode.
- Optimistic retry without a guard: still double-bills under redelivery.

Consequences: every new dispatch/status/debit path must follow this shape.
Reviewers check new pipeline code against this ADR, not against first
principles.
```

Now, three months later, someone (maybe an agent, maybe you) adds a new job type. Without the cache, reviewing that change means re-reasoning about concurrency from scratch: is there a race here? what happens under retry? how do double-debits get prevented? That is a full, expensive derivation, every time, and it is exactly the kind of reasoning that is easy to get subtly wrong under time pressure.

With the cache, the review is short. The reviewer reads the diff and reads ADR 0012. The question is no longer "how should concurrency work here?" It is "does this diff follow ADR 0012?" That is a cache lookup. A yes-or-no check against a decided standard, not a fresh derivation. The hard thinking was done once, when the ADR was written, and it is reused for free on every pipeline change forever after.

That is a cache entry doing its job: the expensive computation (the reasoning) happens once, the result is stored (the ADR), and every future access is a cheap lookup instead of a recomputation.

## How to do it today

1. Write ADRs for decisions, not just for architecture. Any call you would hate to re-argue is a cache entry waiting to be written. Use [templates/adr-template.md](../templates/adr-template.md).
2. Keep an index the reviewers can read fast: the ADR list plus the research shelf, each entry one line. This index is what a review loads instead of the whole repo.
3. When you review, review against the index. Ask "does this follow what we decided?" not "what should we decide?" for anything already in the cache.
4. Tell your judges (pillar 6) to skip settled ADRs. Their attention goes to the cache misses: the genuinely new part of the change.
5. When a decision actually changes, supersede the ADR (mark the old one, write the new one). A cache you never invalidate goes stale, so record reversals as first-class events.

## Failure modes

- **ADRs that do not name alternatives.** "We chose A" is a note. "We chose A over B and C, because" is a cache entry: it answers the re-derivation, which is the whole point.
- **A stale cache.** A decision changed but the ADR was not superseded, so reviewers check against a rule that no longer holds. Invalidate on change, always.
- **Reviewing against the repo anyway.** If your judges keep reloading the whole project instead of trusting the index, you never get the savings. The discipline is to trust the cache for the hits and spend attention only on the misses.
- **Writing ADRs nobody reads.** The cache only pays off if reviews actually consult it. An ADR folder that reviewers ignore is cost with no return.

## What it costs honestly

Writing the ADR costs you the ten minutes it takes to record a decision properly, at the exact moment you would rather move on to code. That is the entire up-front cost, and it is why the cache is the pillar people skip: the bill comes now and the payoff comes later. The other honest cost is invalidation. A cache is only trustworthy if you keep it current, so every time a decision changes you owe the supersede. Skip that and the cache quietly starts lying, which is worse than no cache. But if you pay those two costs (write it down, keep it current), the return is the one thing every growing project needs and almost none get: a review cost that stops rising with the size of what you have built.
