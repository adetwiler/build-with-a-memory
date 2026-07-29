# 14. State, not just decisions

## What it is

A memory network fills up with decisions. What you chose, why, what it beat, the rule it produced. That is the durable stuff, and if you have been running this method for a while, your network is probably good at it.

Then an agent asks a question about right now. What version are players actually being served? Is that migration deployed? Who else is working in this repo at this moment? When did this metric start being collected? And the network goes quiet, because nobody writes that down. Decisions get recorded carefully. **State is ambient, assumed, and stale the moment after somebody checks it.**

The fix is one small file with different rules than everything else in your network: a `NOW.md`. It holds only what is true today. It gets **rewritten, never appended**. Every line is dated. Anything older than about two weeks is a bug, and gets deleted or demoted to the project's history file.

## Why it works

History and state have opposite lifecycles, and a file can only have one. Your decision records grow forever and that is correct; a decision from last year is still a decision. A state file that grows forever is just history with the wrong name, and an agent reading it cannot tell the current line from the stale one. Splitting them means every file has one honest rule: journals append, NOW replaces.

The test is one question: **what facts about "right now" can your network answer without someone opening a browser, logging into a console, or running `git status`?** Every fact that fails that test is a place an agent will fill with an assumption, and assumptions about state are the most common kind of wrong I have found in my own logs.

I learned this twice in one night. Two separate audit agents reported that a game's new version was live on Steam, because the repo said the version number and the repo is where agents look. The store was serving last year's build. Nothing in the network recorded what players were actually being served, so both agents filled the gap with the repo, and I corrected the same wrong claim twice. The store state block in NOW.md exists because of that night.

## How to do it today

1. **Make `NOW.md` at the top of your network** with the rules in its own header: rewritten not appended, every line dated, stale lines deleted. If a session changes state, it updates the block in the same pass.
2. **Split LIVE from DRAFT for anything outward-facing.** A store page, a deployed service, a published doc. Two lists: what the world sees right now, and what is staged waiting to ship. The gap between your repo and your production surface is exactly where agents guess.
3. **Record the start date of anything that collects.** Analytics, trackers, cron jobs. "Give me three weeks of trend" sounds answerable, but it is not when collection only started ten days ago, and nothing warns you. One dated line makes the question honest.
4. **Track adoption, not just existence.** The network saying "the press kit exists and here is how it works" is a decision record. Whether anything actually links to the press kit is state. I had three fully documented kits and zero pages pointing at any of them, and nothing surfaced it.
5. **When a lesson matters, give it a mechanism.** This is the corollary that took me longest to accept. A warning comment only fires if someone reads that file at the right moment. I watched the identical mistake ship twice in three days with the written lesson sitting six lines above the second one. If a lesson matters, turn it into a check, a test, or a gate. A written lesson does not stop the mistake from happening again. A check does. The count check this repo runs on its own pillars exists because the count drifted once.

## Failure modes

- **NOW.md quietly becomes a journal.** Someone appends instead of replacing, nothing deletes, and six months later it is a second history file that lies about being current. The dated-lines rule is what lets you catch this: the dates go stale visibly.
- **State written once, never on change.** The file is only as good as the habit of updating it in the same pass as the change. This is the same muscle as capture-as-you-go, pointed at a different kind of fact.
- **Recording state you can compute.** Do not mirror what `git log` or your build ledger already answers in one command. NOW.md is for facts that live outside the repo (what is deployed, what is live, who is in here) or that span it (what matters most this week).
- **Trusting the repo as a proxy for production.** The failure that taught me this pillar. The repo records what the code is. It has no idea what anybody is being served.

## What it costs honestly

This pillar is days old as I write it, proven on one project, and it is the newest thing in this method. I am publishing it now because the failure it fixes cost me the same correction twice in one night and the shape of the fix is simple enough to try in ten minutes. But be clear about what you are adopting: a discipline, not a tool. NOW.md is only current if updating it is part of finishing a change, and every fact you put in it is a small standing promise to keep it true. Start with the one state question that has actually burned you, not with a template of twenty.
