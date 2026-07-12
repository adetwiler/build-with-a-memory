# 6. Judge panels

## What it is

When a change needs review, you do not ask one agent "is this good?" You convene a panel: several independent agents, each given a distinct lens, each reviewing the same change once. They return one verdict round. No debate loop, no agents arguing with each other across five turns. One pass, distinct angles, collected verdicts.

The lenses are the point. One judge reads for correctness. Another for security. Another for whether it matches the documented conventions. Another for the thing you always forget. Different questions, not the same question asked louder.

## Why it works

A single reviewer has a single blind spot, and asking it twice does not help, because it misses the same things both times. Redundancy (the same lens repeated) catches nothing new. Diversity (different lenses) catches what any one of them alone would miss.

There is a real, published reason to force the lenses apart rather than just running more reviewers. When multiple judges share the same framing, their errors correlate: they tend to be wrong about the same things in the same direction, so stacking them gives you false confidence, not real coverage. Assigning each judge a distinct lens de-correlates the errors. You are not buying more of the same opinion. You are buying coverage of angles the others cannot see.

One verdict round, no debate, is a deliberate limit. Left to argue, agents will happily loop, converging on a confident consensus that is often just the loudest framing winning. A single round keeps each verdict independent, which is the whole source of the coverage. You, the human, integrate the verdicts. That is your job, not theirs.

## How to do it today

1. For a change worth real review, spawn two to four reviewers, each with a written lens: "you review only for correctness bugs," "you review only for security and data exposure," "you review only against `docs/conventions.md`," "you review only for missing tests."
2. Run them independently, in parallel. Do not let them see each other's output. Correlated input produces correlated error.
3. Collect the verdicts in one round. Read them yourself. Where they agree, trust it more. Where they diverge, that divergence is a signal worth your attention.
4. Do not send them back to argue. If a verdict needs follow-up, that is a decision for you, not a debate for them.

Minimal example of a lens brief:

```
You are the isolation reviewer. Read this diff for one thing only: does any
query or write reach data that belongs to a different tenant/user/workspace
than the one acting? Report only that class of finding. Ignore style.
```

## Failure modes

- **Same lens, more agents.** Three "review this" prompts are one reviewer in a trench coat. The lenses have to differ.
- **Letting them debate.** A debate loop launders correlated error into false consensus. One round, then you decide.
- **No human integrator.** The panel produces verdicts, not a decision. If you auto-merge on "all green," you have handed the call to the agents, which pillar 8 says you should not.

## What it costs honestly

It costs more tokens and more of your attention than a single review, because now you are reading three or four verdicts and reconciling them. For a typo fix that is overkill and you should not bother. For a change that touches money, or data isolation, or anything hard to walk back, the extra cost is small next to the cost of shipping the bug that one reviewer would have missed. Match the panel to the stakes.
