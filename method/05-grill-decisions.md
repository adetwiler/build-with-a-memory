# 5. Grill the decisions

## What it is

Instead of the agent nodding along to your plan, it interviews you. One open question at a time, each with a recommended answer attached, until the fuzzy parts are sharp. You answer, it moves to the next branch. When the plan is settled, each real decision lands as an ADR that names the alternatives it beat. Risky ideas go in as their own separate, revertable commits.

The grilling is adversarial on purpose. The agent's job in this mode is not to help you feel good about your plan. It is to find the soft spots before the code does.

## Why it works

Most bad builds trace back to a decision nobody actually made. Something was assumed, never questioned, and the code inherited the assumption. Grilling drags those assumptions into the open while they are still cheap to change (words, not code).

One branch at a time matters. A wall of ten questions gets a rushed wall of ten half-answers. One sharp question, with the agent's recommended answer next to it, gets a real decision, because you are only deciding one thing and you have a starting point to react to. Reacting to a proposal is easier than generating an answer from nothing, so you get further, faster, with less staring.

Recording each decision as an ADR that names its alternatives is what makes the grilling pay off later. The ADR is not just "we chose A." It is "we chose A over B and C, for these reasons." That is the artifact that stops the same debate from reopening in three weeks, and it is the raw material for the decision cache (pillar 7).

Risky ideas as separate commits is a small thing that saves real pain. If an experiment goes bad, you revert one commit instead of untangling it from three unrelated changes.

## How to do it today

1. Before building anything non-trivial, tell the agent to grill the plan: surface every open question, one at a time, each with its recommended answer, and not to proceed until the branch is settled.
2. Answer honestly, including "I do not know." "I do not know" is a finding: it means that branch needs research (pillar 4) before it needs code.
3. As decisions settle, write each as an ADR naming the alternatives. See [templates/adr-template.md](../templates/adr-template.md).
4. Land anything risky or speculative as its own commit with a clear message, so reverting it is one command.

Minimal example of the interview shape:

```
Q: When two jobs race for the same session, who wins?
   Recommended: an atomic guarded update (claim the row, act only if you got it).
   Alternative: a lock (simpler to read, adds a dependency and a failure mode).
Your call?
```

## Failure modes

- **The agent grills to look thorough, not to decide.** Questions that do not change the build are noise. Every question should have a decision hanging off it.
- **You rubber-stamp the recommended answers.** The recommendation is a starting point, not a verdict. If you never override one, you are not really being grilled.
- **Decisions never get recorded.** A grilling that does not end in ADRs is a conversation you will have again. The write-down is the deliverable.

## The cheap way to run this

A grilling is words, not code, which already makes it the cheapest place to find a hole in a plan. Keep it that way: grill against the plan and the relevant docs, not the whole repository, and let one-branch-at-a-time keep the context small. The ADRs it produces are the real saving, because each one is a debate you never pay to have again (pillar 7 does that math).

## Where this came from

The interview-instead-of-agree shape here is adapted from Matt Pocock's `grill-with-docs` skill, reshaped to fit how I build. Full credit and what I changed: [CREDITS.md](../CREDITS.md).

## What it costs honestly

It is uncomfortable, and it is slower up front. Being questioned about a plan you were excited to start is not fun, and a good grilling will occasionally show you that your idea has a hole you cannot fill yet. That sting is the cost. The return is that the holes show up in a conversation instead of in a half-built feature. You spend words now so you do not spend days later.
