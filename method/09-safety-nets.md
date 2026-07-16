# 9. Safety nets from mistakes

## What it is

Every mistake becomes a guardrail, automatically. When something goes wrong (a leak, a race, a broken build, a limit you did not know about), you do two things in the same pass: you write the lesson down as a line in the docs, and you add a machine check that catches it next time. A hook. A version guard. A smoke test. A grep in a pre-commit gate.

Put simply: your mistakes become guardrails automatically. The incident is not just fixed. It is converted into something that cannot happen the same way again.

## Why it works

A lesson that lives only in a doc depends on someone reading the doc at the right moment. They will not, eventually. Memory (yours or an agent's) is not a reliable gate. A machine check does not depend on anyone remembering: it runs every time, whether or not the person is thinking about that failure that day.

But the doc still matters, which is why you write both. The check catches the recurrence; the doc explains *why the check exists*, so a future you does not delete a guardrail that looks paranoid without understanding what it is guarding against. The line in the docs is the check's reason for living. The check is the line's enforcement. Neither is enough alone.

Two checks worth the trouble illustrate the pattern. This very repo has a pre-commit hook that blocks any staged line containing an em dash, because the author does not want them and cannot be trusted to catch every one by eye. It also has a leak-audit script that greps the whole tree for a denylist of private terms before anything publishes, because moving private context around all day means a leak by hand is a matter of when, not if. Both are mistakes-turned-guardrails: a preference and a risk, each made mechanical so no one has to remember them.

## How to do it today

1. When something bites you, fix it, then immediately ask: what would have caught this automatically? Build that.
2. Write the lesson as a short line where the relevant work happens (the topic doc, the manual's rule block if it is load-bearing).
3. Add the check to a place that runs on its own: a pre-commit hook, a CI step, a startup guard, a test. See `.githooks/pre-commit`, `scripts/leak-audit.sh`, and `scripts/release-check.sh` in this repo for working examples: per-commit gates for the mistakes that arrive one line at a time, and a whole-tree release check for the moment the stakes jump.
4. Make the check's message name the failure clearly, so when it fires, the person understands what they almost did and why the guard is there.

Minimal example of a guard's error message:

```
BLOCKED: staged change contains an em dash (line 12 of notes.md).
Use a period, comma, colon, or parentheses. This guard exists because
em dashes slip in by hand and we remove them by policy, not by eye.
```

## Failure modes

- **Doc without check.** The lesson is written, nobody reads it at the right time, the mistake recurs. The check is the half that actually gates.
- **Check without doc.** A guard fires and nobody knows why, so someone deletes it as noise. The doc is the guard's explanation and its defense.
- **Over-guarding.** A check for every conceivable failure turns commits into an obstacle course and trains people to bypass the gate. Guard the mistakes that actually happened or would actually hurt, not every hypothetical.

## What it costs honestly

Each net costs a little to build (a few lines of shell, a test, a hook) at the worst possible moment, right after something already went wrong and you are tired of it. That is the friction. And guards accumulate, so if you never prune them, the gate gets slow and people start reaching for the bypass, which defeats the purpose. So the honest cost is not just building the nets; it is maintaining a sane set of them and cutting the ones that stopped earning their place. Done with restraint, the trade is excellent: a mistake you make once becomes a mistake you cannot make twice, and you stop spending attention guarding against your own known failures by hand.
