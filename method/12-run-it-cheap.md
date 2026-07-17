# 12. Run it cheap

## What it is

Everything in this method runs on whatever agent and plan you already have. This pillar is the set of habits that keeps it that way, because run naively (hooks firing on every turn, a model call for every capture, a judge panel on every commit), a memory system like this can quietly become a top-tier-subscription workload. It does not have to be one, and nothing in this method should ever read as "buy the bigger plan." If a memory method only works on a $200-a-month plan, then "your context lives in files you own" is gated behind a subscription after all, and the whole anti-lock-in point is lost.

Four habits carry most of the savings:

- **Load only what you need.** Navigate by the map (pillar 1) and open one file, instead of front-loading the whole network every turn.
- **Prefer deterministic over model.** Anything a script can answer should never be a model call. What changed recently is `git log`. Whether a fact is already captured starts as a grep.
- **Gate model calls behind a novelty check.** Before a capture or a summary pass runs, a cheap check asks whether there is anything new to process. Most of the time there is not, and the expensive call never fires.
- **Match the model to the job.** Routine mechanical passes (triage, daily summaries, formatting) go to the smallest model that does them well. The strong model is for the work where judgment concentrates: the grilling, the hard review, the decision.

## Why it works

Token cost concentrates in two places: the context you load and the calls you make. The method already attacks the first one by design. The always-loaded manual is kept lean because it taxes every single turn (pillar 1), the map exists so sessions navigate instead of front-loading, and the decision cache (pillar 7) is the biggest saving in the whole system, because a decision recorded once is reasoning you never pay for again. Run properly, the memory is not overhead on top of your plan. It is the thing lowering your per-session cost.

The second one, calls you make, is where naive automation leaks money. A hook that runs a model on every turn, a capture pass with no novelty gate, a judge panel sized for a payments change but fired on a typo fix: each is a small leak that compounds across a working week. The habits above close them, and none of them reduce what the method delivers. They only cut the calls that were not producing anything.

Tool-agnostic is part of the same answer. Plain markdown runs on any agent, which means you can put each job on the cheapest tool that does it well, and when prices or tools change, your memory moves with you. Portability is not just the anti-lock-in principle. It is also the pricing lever.

## How to do it today

1. Audit what loads every turn. Read your always-loaded manual and ask of each line: does this earn its per-turn tax? Move detail to topic docs and leave pointers (pillar 1 has the shape).
2. List your recurring model calls (captures, summaries, review passes) and put a deterministic gate in front of each: skip if nothing new, skip if the diff is trivial, skip if the answer is already in a file.
3. Batch periodic work at day boundaries instead of running it in the hot path. A nightly pass on a small model beats a per-turn hook on a big one, and it does not slow your session down.
4. Pin each routine job to the smallest model that does it well, and write that choice down so sessions do not silently upgrade it back.
5. Size review to stakes (pillar 6 says this too): a full panel for the money path, one pass for the typo.

## Failure modes

- **Efficiency theater.** Trimming context the agent actually needs, so it re-derives things wrong. Re-derivation is the most expensive outcome there is; that is the problem this whole method exists to fix. Cut loads, never load-bearing facts.
- **The hot-path hook.** A check that fires on every turn multiplies by everything you do. Move it to a boundary (commit, session close, nightly) unless it truly has to be live.
- **Reading this pillar backwards.** It names what you do not need. It never names a plan you must buy, and if you catch a version of this method doing that, something has gone wrong with it.

## What it costs honestly

A setup pass to find your leaks, and a little ongoing discipline to keep routine jobs on cheap paths when it would be easier to let the strong model do everything. The small-model choice also has a real edge: push a job too far down-market and the quality drops below useful, so you have to actually check the output the first few times, not just the bill. And the honest caveat on the whole pillar: I run this method heavily, and heavy use of any agent costs real money at any tier. These habits will not make it free. They make the method work seriously on a mid-tier plan instead of demanding the top one, and they keep your costs tracking the work you do instead of the size of what you have built.
