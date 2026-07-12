# 8. Human checkpoints

## What it is

Agents prepare decisions. Humans make them. The whole method is arranged so the machine does the gathering, the drafting, the option-laying-out, and then hands a person a clear choice to make. It never decides the load-bearing things on its own and moves on.

The practical consequence: your throughput is not "how many agents can I run." It is "how many decisions can I make and how many changes can I actually verify." That is the real bottleneck, and the method is built to respect it rather than pretend it away.

## Why it works

AI gets things wrong. Confidently, fluently, in a way that reads correct. That is not a flaw you prompt away; it is the current nature of the tool. So the safe design is not "trust the agent and spot-check." It is "let the agent do everything except the irreversible call, and put a human on that call every time."

This is also why the earlier pillars are shaped the way they are. Grilling (pillar 5) prepares a decision for you to make. Judge panels (pillar 6) prepare verdicts for you to integrate. Research (pillar 4) prepares evidence for you to weigh. None of them decide. They compress the work of deciding down to the moment of judgment, and then they stop and wait for you. That is the design working as intended, not a limitation of it.

Being honest about the bottleneck changes how you scale. Standards and a memory network multiply the *context* an agent has. They do not multiply your judgment or your ability to verify. So you get more leverage by making each decision cheaper to reach (kill criteria written down, prices fixed, ADRs as a decision cache) than by running more agents that produce more things you cannot check. Agents should prepare decisions, not make them. That sentence is the whole pillar.

## How to do it today

1. Draw the line explicitly. Decide which actions an agent may take on its own (reversible, low-stakes, follows from the request) and which always stop for you (destructive, outward-facing, or a genuine change of scope). Write the line down so it is not re-negotiated every session.
2. Make your decisions cheap to reach. Where you can, pre-decide: write kill criteria, fix a price, record a policy as an ADR. Every decision you cache is one the agent does not have to stop and ask about.
3. Have agents present, not act, on the load-bearing calls: here are the options, here is the recommended one, here is why. You pick.
4. Protect your verify cycles. If you cannot check it, do not ship it just because an agent said it was fine. Verification is a human cost you cannot delegate away, so treat it as the scarce resource it is.

Minimal example of the present-do-not-act shape:

```
I can take this one of two ways. A keeps the existing schema and is reversible.
B changes the schema and is a one-way door once data lands. I recommend A.
Which do you want? (I will not touch the schema without a yes.)
```

## Failure modes

- **Checkpoint theater.** Presenting a "decision" so leading that there is really only one answer. If the human always picks the recommendation, the checkpoint is decorative.
- **Silent autonomy creep.** An agent quietly starts making calls it used to surface, because nothing stopped it. The written line is what keeps this from drifting.
- **Scaling the wrong axis.** Running more agents to go faster, then drowning in output you cannot verify. More unverified work is not more progress.

## What it costs honestly

It caps your speed, and that is the uncomfortable truth of it. No matter how many agents you run, you can only make so many real decisions and verify so many changes in a day, and this pillar says to respect that limit instead of routing around it. That feels slow when the tools make it so easy to generate more. But the alternative (letting the agent decide and merge things you did not actually check) is how you end up with a fast pile of code you do not trust. The cap is the price of trusting your own repository. It is worth paying.
