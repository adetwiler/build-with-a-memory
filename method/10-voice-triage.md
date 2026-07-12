# 10. Voice to typed work

## What it is

You think out loud. You brain-dump, by voice or in a rambling message, everything on your mind: half-formed ideas, three bugs, a feature, a worry. That raw dump goes into a cheap triage lane that turns it into typed, human-approved work items. The agent shapes each thought into a proper item (a bug, a task, a decision to make) and hands them back for you to approve, edit, or drop.

The lane is cheap on purpose. Its whole job is to be low-friction enough that you actually use it, so the thoughts get captured instead of lost.

## Why it works

The moment you have the thought is almost never the moment you can sit down and write a clean ticket for it. So the thought evaporates, or it clutters your head until you forget it. A brain-dump lane meets you where the thinking actually happens: messy, spoken, out of order. It removes the friction between having the idea and capturing it.

Triage is what makes the mess useful. A raw dump is not actionable; a typed, scoped work item is. Putting an agent in the middle (dump goes in, structured items come out) means you get the low friction of talking and the structure of a tracked task, without doing the shaping yourself. That shaping is exactly the kind of mechanical work an agent is good at and you find tedious.

The human-approved part is not optional, and it ties back to pillar 8. The lane proposes items. You approve them. A thought you muttered is not a committed task until you say so, because half of what you say out loud is thinking, not deciding. The approval step is the filter between the two.

There is a real trap this pillar guards against, and it is worth naming: dictation gets words wrong. Spoken input arrives with transcription errors, and some of them are silent (a plausible wrong word, not an obvious garble). So the triage agent's job includes noticing when a thought reads oddly or contradicts itself and asking, rather than shaping the literal wrong words into a confident wrong task. When the text is strange, the answer is a question, not an action.

## How to do it today

1. Make one low-friction inbox for raw thoughts: a voice memo you drop in, a scratch file, a single chat you talk into. Whatever you will actually use.
2. Give an agent the triage job: read the dump, split it into candidate work items (bug, task, decision, question), each scoped and typed, and hand them back as proposals.
3. Tell it to flag anything that reads oddly instead of guessing. Odd or contradictory wording is often a transcription slip, so the right move is to ask what you meant, not to build the literal text.
4. Approve, edit, or drop each proposed item. Only the approved ones become tracked work.

Minimal example of the lane's output:

```
From your dump, I pulled these. Approve, edit, or drop each:
1. BUG: the results page shows stale data after a refresh. (scoped)
2. TASK: add the export button we talked about. (needs a size)
3. QUESTION: you said "three credits" but the context reads like "free
   credits" - which did you mean? Not filing until you confirm.
```

## Failure modes

- **A lane you do not use.** If capturing a thought is any friction at all, you will not do it in the moment, and the whole pillar is dead. Lower the friction until you actually use it.
- **Auto-filing the raw dump.** Turning every muttered thought into a committed task, transcription errors and all, buries you in noise and wrong work. The approval step is mandatory.
- **Shaping the literal wrong words.** Building the task the transcription says instead of the one you meant. When the text is strange, ask.

## What it costs honestly

Very little to run, which is the point, but it has one real failure cost: if you skip the approval step to go faster, you get a task list full of half-thoughts and mis-heard words that costs more to clean up than it saved. The lane is only cheap if you keep the human filter on it. Kept honest, it is close to free and it stops the specific, common loss of a good idea you had at the wrong moment and never wrote down.
