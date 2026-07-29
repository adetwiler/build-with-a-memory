# The interview

You are the person's own AI coding agent, and you are about to build them a
personal memory layer from their answers. Read this whole file, then run the
interview exactly as written.

Ground rules for you, the agent:

- **One question at a time.** Ask, wait for the answer, then move on. Never
  dump the whole list at once.
- If your tool supports structured questions with options (Claude Code's
  AskUserQuestion, for example), use it, with the default marked. Otherwise ask
  in plain text and offer the default.
- **Plain talk in, faithful notes out.** The person may ramble or speak through
  a voice tool. That is the good outcome. Distill what they said; never invent
  what they did not say.
- Never overwrite anything that already exists. If a file is already there,
  read it and add only what is missing.
- When the interview is done, follow [scaffold.md](scaffold.md) to build their
  files, check [platforms.md](platforms.md) for the path rules on their OS,
  and then report back exactly what you created.

## Question 0: whose machine is this?

Ask first, before anything else: **"Is this machine yours, or does it belong to
an employer or a client?"**

- **Mine**: proceed normally.
- **Employer's or a client's**: proceed in **standalone mode**. Everything you
  scaffold stays inside their own user folder. Do not add hooks, files, or
  commits to any repo they do not personally own, and do not suggest doing so
  later. Write this rule into their personal file so future sessions honor it
  too (scaffold.md has the exact line).

There is no third option and no shame in either answer. The default, if they
shrug, is to treat it as an employer's machine, because that is the safe
direction to be wrong in.

## Question 1: which agent do you use?

**"Which AI coding agent will read this every day?"** Claude Code, Cursor, or
something else. This decides where the personal file lives; the layout table is
in [scaffold.md](scaffold.md). If they use more than one, pick the one they use
most; the scaffold adds pointer files for the rest.

## Question 2: who are you, and what do you build?

**"Tell me about yourself and your work. What do you build? What does a normal
working day look like?"**

Let them talk. If they have a voice tool, remind them once that talking is
allowed and usually better. You are listening for: their name or handle, what
they make, the tools and languages they live in, and the projects that matter
right now. Follow up once or twice if something load-bearing is vague, then
stop; this is an interview, not an interrogation.

## Question 3: what should your agent always remember?

**"What do you want me to remember about how you like to work? Rules, pet
peeves, things I should always or never do."**

Examples to offer if they stall: preferred language or framework, formatting
opinions, "always ask before deleting," "keep replies short," "never touch
production." Whatever they say becomes the rules section of their personal
file, in their words, tightened but not translated.

## Question 4: what are you working on right now?

**"What is the thing you are in the middle of? If we got cut off today, what
would you want a fresh session to know tomorrow?"**

This seeds their first memory file, so the very first `pick up` has something
real to find.

## Question 5: the three habits

Explain the three one-word habits in a sentence each (they are defined in
[scaffold.md](scaffold.md)): `handoff` files a note about where you left off,
`pick up` resumes from the newest one, `idea` captures a thought without
derailing the session. Ask: **"Want all three? Most people do."**

Default: all three. If they skip any, scaffold only what they kept.

## Then

Run [scaffold.md](scaffold.md) with everything you learned. Verify with the
checklist at the bottom of that file. Report back with a short list of exactly
what you created, where it lives, and the one-line way to use each habit they
kept. Nothing else.
