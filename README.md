# Build With a Memory

Your AI coding agent forgets everything between sessions. So it re-derives the same decisions, re-asks what you already answered, and you pay for it every time.

The fix is simple. Make the project remember for you.

## The fix

Paste one prompt into Claude Code, Cursor, or whatever AI coding agent you use, in the repo you want it to remember. It reads your project, writes down what it is and how to run it, and sets up a few small files where decisions and gotchas get saved as you work. Next session, your agent reads those first and picks up where you left off.

No install. No account. Nothing leaves your repo. It is just plain files you own, set up so they stay useful instead of going stale.

## The prompt

Copy this into your agent, in the repo you want it to remember:

```
Set up a simple project memory for THIS repository, so you and any AI coding assistant I use later can pick up where we left off instead of re-learning the project every session.

Follow these steps in order. Write down only what you can confirm from the repo. Never guess, never invent placeholder facts, and never overwrite or delete anything I already have. If a file already exists, read it and add to it.

1. LEARN THE PROJECT FIRST. Before writing anything, read what is actually here: the README, any package or build file (package.json, pyproject.toml, go.mod, Cargo.toml, Gemfile, composer.json, and so on) for the language and the real commands, the top-level folder layout, and the last 20 commits (git log --oneline -20). If the repo is empty or brand new, say so plainly and keep everything short.

2. PICK THE MAIN FILE. If CLAUDE.md exists, that is the main file. Otherwise, if AGENTS.md exists, that is the main file. If neither exists, create CLAUDE.md. Create the other one as a two-line pointer that says the real content lives in the main file, so any assistant finds it.

3. WRITE THE MAIN FILE SHORT. A newcomer should be able to read it in about a minute. Include only: what this project is (one or two plain sentences), how to run it (the real install, dev, test, and build commands you actually found), and the rules that matter (conventions, do-not-do items, gotchas you can see). If the main file already exists, keep everything useful in it and add only what is missing.

4. ADD THREE SMALL FILES in a docs folder (add to them if they exist, do not overwrite):
   - docs/now.md: what I am working on right now. A few dated lines about the current focus. Rewrite this file, do not pile onto it: when a line is done or has gone quiet for about two weeks, move it out (to docs/decisions.md if it was a decision, otherwise delete it). Keep it to what is active.
   - docs/decisions.md: decisions and why. One dated entry per real decision, newest first, each saying what was decided and the reason. Seed it from any clear decisions in the README or commit history. If none are clear, leave one line saying the file is for decisions as they come.
   - docs/notes.md: gotchas worth not re-discovering. Seed it with any traps you noticed while reading the repo, otherwise leave one line saying what it is for.

5. WIRE THE HABIT. Add this section to the main file (adjust the paths if you used AGENTS.md as the main file):

   ## How to use this memory
   - Start each session by reading docs/now.md to see what is active.
   - When we make a decision, write it in docs/decisions.md with the date and the reason, in the same session it happens. This is part of finishing the work, not a separate chore.
   - When we hit a gotcha worth remembering, add it to docs/notes.md the same way.
   - Keep this file short. When a section gets long, move the detail into a docs file and leave a one-line pointer here.

6. REPORT BACK with a short list of exactly what you created or changed. Nothing else.
```

That is the whole thing. Run it once per project. The raw text is in [prompt.txt](prompt.txt) if you want to copy it without the formatting around it.

## What it actually does

- Reads your repo first (the README, your package or build file, the folder layout, recent commits) and writes down what it finds, not made-up filler.
- Creates or extends a short guide file (CLAUDE.md or AGENTS.md, whichever your agent already loads) with what the project is, how to run it, and the rules that matter.
- Adds three small files: one for what you are working on now, one for decisions and why you made them, one for gotchas worth not hitting twice.
- Tells your agent to read the "now" file at the start of each session, and to write down new decisions and gotchas in the same session they happen.
- Never overwrites what you already have. If a file exists, it reads it and adds to it.

It works on a messy old repo and on an empty one.

## What this is not

- It is not a database, and it is not a search engine. It is a handful of plain text files your agent reads.
- There is no install, no server, no account, no dependency to add.
- Nothing leaves your machine. The files live in your repo and go where your repo goes. Your project's memory stays yours, not some service's product.
- It does not promise perfect memory. It just writes things down so you stop re-explaining them.

## Want more?

- **The method behind it.** This is the small front door. The way I actually run this across my own projects (decision records, a map of what lives where, writing things down as I go) is in [THE-METHOD.md](THE-METHOD.md) and the [`method/`](method/) folder. Take the parts that fit.
- **One command instead of a paste.** An `npx` setup that does the same thing across all your repos is coming.
- **Updates and the fuller kit** live at [buildwithamemory.com](https://buildwithamemory.com). I also write about this as I go; the devlog is in [`posts/`](posts/) and subscribable by RSS (`feed.xml`).

## License

Dual license, both permissive. The templates, hooks, and scripts are MIT: copy them into your work, commercial or not, no attribution needed. The written method is CC-BY-4.0: share and adapt it, just credit the source. See [LICENSE](LICENSE).
