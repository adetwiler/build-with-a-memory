# 11. The session handoff

## What it is

When a work session ends, you say one word. The agent writes a handoff (what happened, what is open and needs your call, where the next session should start), runs a short set of close-out sweeps, and files the handoff in a dated store keyed by the work. The next session that picks up that work reads the handoff first and starts oriented instead of starting cold.

The one-word trigger is the design, not a convenience. A close that takes effort does not happen, so the whole close has to cost you one word. Everything else is the agent's job.

The sweeps that run before filing:

- **Unfinished work.** Scan the session for something that should have been finished but was not: a promised change never made, a verify never run, a decision that was made but never applied. If something is found, finish it or surface it loudly before filing. A handoff is not a rug to sweep half-done work under.
- **Capture misses.** Anything durable that surfaced this session (a gotcha, a settled convention, a decision) that never landed in its home per pillar 3. File only the misses. If the same-pass habit held, this sweep is a no-op.
- **Public drift.** Only if the session touched public-bound content: did a decision made here leave a public doc or repo stale? File the gap where it will be seen; do not silently fix public surfaces at midnight.
- **Fail closed on anything shareable.** If the close-out feeds anything public (a devlog, a shared changelog, a list of lessons), a candidate you are not sure is public-safe stays in the private handoff, flagged for the human. Capturing is automatic. Publishing never is.

## Why it works

Real numbers from my own transcripts: over a stretch of weeks I asked the tool to compress a long conversation so I could keep going 106 times, ended a session 65 times, and wrote a proper handoff 4 times. I was stretching sessions past their useful life because ending one meant losing the thread, and writing the handoff by hand was work I kept skipping. The lesson was not that I needed more discipline. It was that the close cost too much. When the close became one word, it started happening.

The dated store matters because a handoff you overwrite is a handoff you lose. One file per close, keyed by the work, means parallel efforts do not clobber each other and an old thread can be picked up weeks later. Keying by the work (not by the machine or the tool that wrote it) means "pick up the billing rework" finds the right handoff no matter where the last session ran.

The sweeps are backstops, and that word is doing real work. Same-pass capture (pillar 3) stays the primary habit; the close-out exists to catch what slipped. Sweeps that run once, at the end, against a session the agent already has in front of it, are cheap. A close that tried to be the primary capture mechanism would just be batch documentation with a shorter batch.

## How to do it today

1. Pick one trigger word and make it the whole instruction, as a standing rule in your manual or a custom command: "when I say handoff, write the handoff, run the sweeps, file it, and tell me in one line. No questions."
2. Use a fixed shape so every handoff reads the same: the story, the open calls, what is next. See [templates/HANDOFF.md](../templates/HANDOFF.md) for a drop-in version.
3. File to one dated store (a `handoffs/` folder with `YYYY-MM-DD-<work>.md` names is enough), and give "pick up" the matching meaning: read the newest open handoff for this work and start at its "what's next."
4. Surface open handoffs at session start (a session-start hook, or a line in the manual telling the agent to check the store) so a filed handoff cannot rot silently.
5. Keep the fail-closed rule written down where the agent will see it: unsure a line is public-safe, it stays private and flagged.

## Failure modes

- **A close that costs effort.** If ending a session takes more than a word, you will stretch the session instead, and the context dies with it. The numbers above are what that looks like.
- **The sweep replaces the habit.** If capture waits for the close, you are batch-documenting again, and the end-of-session sweep becomes long, lossy, and skippable. Same-pass capture stays primary.
- **Overwrite-in-place.** One rolling handoff file per repo feels tidy and silently destroys history the moment two efforts overlap. Dated files in one store.
- **Handoffs nobody reads.** If the next session does not read the handoff first, the close was theater. Wire the pickup side too.

## The cheap way to run this

The close runs once per session, not on every turn, so it is already on the cheap side of the ledger. Keep it that way: let deterministic checks do the first pass (git can say what changed; a grep can say whether a marker was written) and spend model attention only on the judgment calls, like whether something should have been finished. The handoff itself is written from context the agent already holds, so filing it costs far less than the re-orientation it saves.

## What it costs honestly

From you, one word, and the habit change behind it: actually ending sessions instead of stretching them, which takes a while to trust. From the agent, a few minutes of close-out work you have to be able to rely on, and you should spot-check the early ones until you do. The store also needs occasional weeding, because open handoffs that are genuinely done should get marked, or the pickup signal drowns. Against that, every session that starts oriented instead of cold is re-explaining you did not do. That was the whole point of the method, applied to the gap between sessions.
