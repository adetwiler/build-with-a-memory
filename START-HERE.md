# Start here: the setup wizard

The [prompt](README.md) gives one repo a memory. This wizard gives **you** one.

It sets up your personal layer: a small file of rules your agent reads every
session, a memory folder it writes to as you work, and three one-word habits
(`handoff`, `pick up`, `idea`) that make sessions resumable. Everything it
creates is plain text on your machine, built from your answers. Nothing is
installed, nothing phones home, and nothing here needs an account.

It is a prompt, not a program. Your own AI coding agent runs it.

## Run it

1. Get this repo onto your machine (clone it, or download the zip):

   ```
   git clone https://github.com/adetwiler/build-with-a-memory.git
   cd build-with-a-memory
   ```

2. Open your agent (Claude Code, Cursor, whatever you use) in this folder and
   say:

   ```
   Read wizard/interview.md and run the interview.
   ```

3. Answer the questions. Plain talk is fine; rambling is fine. If you have a
   voice tool (Wispr Flow or similar), talking beats typing here, because the
   best answers are the ones you would say out loud.

That is the whole thing. It takes about ten minutes, and the wizard reports
exactly what it created before it finishes.

## What you end up with

- A short personal instructions file your agent loads every session: who you
  are, what you build, the rules that matter to you.
- A personal memory folder with an index, so facts have a home and future
  sessions find them.
- The three habits, written as plain instructions your agent follows:
  - **`handoff`**: one word files a note about where you left off.
  - **`pick up`**: one word resumes from the newest one.
  - **`idea`**: one word captures a thought without derailing the session.

No daemons, no schedulers, no scripts to keep alive. Files only. It works the
same on Windows and macOS; the wizard handles the path differences.

## On a work machine?

Say so when the wizard asks; it is the first question. On a machine your
employer or a client owns, the wizard keeps everything inside your own user
folder and never touches a repo you do not own. The reasoning is
[pillar 13](method/13-borrowed-memory.md) in reverse: the question is not only
what borrowed machinery does to you, it is what your machinery does in someone
else's tree.

## After the wizard

Your personal layer remembers you. To make a *project* remember itself, run
[the prompt](README.md) in that repo. The two halves are independent; either
works alone, and they are better together.
