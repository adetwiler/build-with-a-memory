# Posts

The devlog. Each post is one markdown file, and the whole thing is subscribable
by RSS, so writing in public is just committing a file, not standing up a blog.

## The shape

One file per post, named `YYYY-MM-DD-slug.md`. Minimal front matter at the top,
then the body in markdown:

```
---
title: A short, plain title
date: 2026-07-12
description: One sentence that shows up in the feed and the preview.
---

The body. Same voice rules as everything else in this repo: plain words, short
sentences, no em dashes, no hype, honest before polished.
```

Three front-matter fields, all required: `title`, `date` (ISO `YYYY-MM-DD`), and
`description` (one sentence, used as the feed item summary). Nothing else is
needed. The filename date and the front-matter date should match.

## How a post becomes public

Posts land after a daily human review. Write the file, commit it, and it goes
into the feed on the next reviewed pass. There is no auto-publish: a person reads
it first.

Drafts stage outside `posts/`. A file in this folder is expected to be in the
feed, so the release check fails on a draft sitting here with a stale
`feed.xml`. Keep work-in-progress elsewhere and move it in when it's ready to
ship (regenerating the feed in the same pass).

## The feed

`scripts/make-feed.mjs` reads every `posts/*.md`, sorts newest first, and writes
`feed.xml` at the repo root. Run it after adding or editing a post:

```
node scripts/make-feed.mjs
```

The feed is a plain file in the repo, so there is no separate blog service to run.
Subscribers point their reader at the published `feed.xml` URL.
