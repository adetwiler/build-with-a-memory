# The method behind Build With a Memory

> New here? Start with the [README](README.md) and the one-paste prompt. This file is the deeper version: how I actually run this across my own projects once the one-paste setup is in place.

Every AI coding session wakes up with amnesia. It has no idea what you decided last week, why you named things the way you did, or which approach you already tried and threw away. So you re-explain. Every time. The agent re-derives context you paid for once, gets it slightly wrong, and you review the same ground again.

The fix is not a bigger model or a smarter prompt. It is a place to remember.

**The one idea: the repository is the memory.** Context, decisions, and conventions live in committed markdown, indexed by a map, so any fresh session (Claude, Cursor, Codex, whatever comes next) navigates to what it needs instead of re-deriving it. Plain text. No service to sign up for. No framework to adopt. It works with any agent because it is just files in your repo.

This is the method I use to build with AI agents. I am an indie developer. I make a playtest tool and some small games, mostly alone. I do not have all the answers. I have a way of working that stopped me from losing the same context over and over, and it is written down here so you can take the parts that fit.

## Why this is the anti-product

There is no SaaS here. No hosted memory. No lock-in. The whole point is that your context lives in your repo as plain files you own. If a tool wants to store your project's memory on their servers behind an API, they have made your memory their product. This makes it yours.

I would rather show you the method and have you keep the files than sell you a subscription to your own context.

## The ten pillars

Read the ones you need. Start with the first, then the seventh (that one is the reason the rest pays off).

| # | Pillar | When to read |
|---|--------|--------------|
| 1 | [The repo is the memory](method/01-repo-memory.md) | You are tired of re-explaining your project every session |
| 2 | [The wide personal network](method/02-wide-network.md) | You have facts that span projects and no home for them |
| 3 | [Capture as you go](method/03-capture-as-you-go.md) | You keep re-discovering the same gotcha |
| 4 | [Research first](method/04-research-first.md) | You are about to make a call you cannot un-make cheaply |
| 5 | [Grill the decisions](method/05-grill-decisions.md) | You want the agent to interview you, not agree with you |
| 6 | [Judge panels](method/06-judge-panels.md) | One reviewer keeps missing things |
| 7 | [The decision cache](method/07-decision-cache.md) | You want your review cost to fall as the project grows |
| 8 | [Human checkpoints](method/08-human-checkpoints.md) | Agents are moving faster than you can verify |
| 9 | [Safety nets from mistakes](method/09-safety-nets.md) | You made a mistake and do not want to make it twice |
| 10 | [Voice to typed work](method/10-voice-triage.md) | You think out loud and lose half of it |

## Quick start

You do not adopt ten pillars on a Tuesday. You start with one file, one record, one rule.

1. **One context file.** Make a `CONTEXT.md` in your repo. Put the glossary in it: the five or ten terms that mean something specific in your project, each with one line. That is it. Next session, tell your agent to read it first. See [templates/CONTEXT.md](templates/CONTEXT.md).

2. **One decision record.** Next time you make a call you might second-guess later (a library choice, a schema shape, a "we will not do X" line), write it down: the decision, the date, the alternatives it beat, the consequence you accept. One short file in `docs/adr/`. See [templates/adr-template.md](templates/adr-template.md).

3. **One rule.** When you lose an hour to something (a config that fought you, a race you did not see, a limit you hit), turn that hour into three lines written where the next session will find them. An hour lost becomes three lines saved. That is the whole loop.

Do that for a month. The context file grows into a network. The decisions grow into a cache. You will feel the review get cheaper before you can explain why.

## Follow along

I write about this in public as I go. The devlog lives in [`posts/`](posts/) and is subscribable by RSS: point your reader at `feed.xml`. Posts land after a daily human review, so the feed is a considered record, not a firehose.

## License

Dual license, both permissive:

- The **templates** (everything in `templates/`, the hooks, the scripts) are MIT. Copy them into your work, commercial or not, no attribution required.
- The **method docs** (`README.md`, `method/`, `research/`, the ADR) are CC-BY-4.0. Share and adapt them, just credit the source.

See [LICENSE](LICENSE) for the exact terms.

## Contributing

If you scrub before you share, share. This repo carries two mechanical gates that run before anything ships: a pre-commit hook (see `.githooks/`) and a full-tree audit (`scripts/leak-audit.sh`). Run the audit before you publish anything derived from a private project. The gates exist because I move private context around all day and I do not trust myself to catch every leak by eye.
