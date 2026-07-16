#!/usr/bin/env node
//
// make-feed.mjs: build a valid RSS 2.0 feed.xml from posts/*.md.
//
// Plain node, zero dependencies. Reads the front matter (title, date,
// description) from every post, sorts newest first, and writes feed.xml at the
// repo root. Run it after adding or editing a post:  node scripts/make-feed.mjs
//
// See posts/README.md for the post shape and docs/adr/0001 for why the feed is a
// plain file in the repo instead of separate blog infrastructure.

import { readdirSync, readFileSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

// OWNER: base URL for the channel <link> and each item's link/guid. Points at
// the GitHub blob view of the repo, which renders each post's markdown and
// resolves the moment the repo is public. Swap it for buildwithamemory.com (or a
// GitHub Pages URL) if the devlog later gets a dedicated home. No trailing slash.
const FEED_BASE_URL = 'https://buildwithamemory.com';

const CHANNEL_TITLE = 'Build With a Memory';
const CHANNEL_DESCRIPTION =
  "A working developer's devlog on building with AI coding agents: committed markdown memory networks and a self-improving loop.";

const here = dirname(fileURLToPath(import.meta.url));
const repoRoot = join(here, '..');
const postsDir = join(repoRoot, 'posts');

// Escape the five XML special characters for use in element text.
function xmlEscape(s) {
  return String(s)
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&apos;');
}

// Parse a leading `---` front-matter block. Returns { data, body }.
function parseFrontMatter(raw) {
  const text = raw.replace(/^﻿/, '');
  if (!text.startsWith('---')) return { data: {}, body: text };
  const end = text.indexOf('\n---', 3);
  if (end === -1) return { data: {}, body: text };
  const block = text.slice(3, end).trim();
  const body = text.slice(end + 4).replace(/^\s*\n/, '');
  const data = {};
  for (const line of block.split('\n')) {
    const m = line.match(/^([A-Za-z0-9_-]+):\s*(.*)$/);
    if (!m) continue;
    let value = m[2].trim();
    if (
      (value.startsWith('"') && value.endsWith('"')) ||
      (value.startsWith("'") && value.endsWith("'"))
    ) {
      value = value.slice(1, -1);
    }
    data[m[1]] = value;
  }
  return { data, body };
}

// RFC 822 date (RSS pubDate) at UTC midnight for a YYYY-MM-DD string.
function toRfc822(dateStr) {
  const d = new Date(`${dateStr}T00:00:00Z`);
  if (Number.isNaN(d.getTime())) return null;
  return d.toUTCString();
}

const files = readdirSync(postsDir)
  .filter((f) => f.endsWith('.md') && f !== 'README.md')
  .sort()
  .reverse(); // filenames start with YYYY-MM-DD, so reverse = newest first

const items = [];
for (const file of files) {
  const raw = readFileSync(join(postsDir, file), 'utf8');
  const { data } = parseFrontMatter(raw);
  const missing = ['title', 'date', 'description'].filter((k) => !data[k]);
  if (missing.length) {
    console.error(`Skipping ${file}: missing front matter (${missing.join(', ')}).`);
    continue;
  }
  const pubDate = toRfc822(data.date);
  if (!pubDate) {
    console.error(`Skipping ${file}: unparseable date "${data.date}".`);
    continue;
  }
  // Keep the .md so the GitHub blob view resolves the file directly.
  const link = `${FEED_BASE_URL}/posts/${file}`;
  items.push({ ...data, pubDate, link });
}

const now = new Date().toUTCString();

const itemXml = items
  .map(
    (it) => `    <item>
      <title>${xmlEscape(it.title)}</title>
      <link>${xmlEscape(it.link)}</link>
      <guid isPermaLink="true">${xmlEscape(it.link)}</guid>
      <pubDate>${xmlEscape(it.pubDate)}</pubDate>
      <description>${xmlEscape(it.description)}</description>
    </item>`,
  )
  .join('\n');

const xml = `<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>${xmlEscape(CHANNEL_TITLE)}</title>
    <link>${xmlEscape(FEED_BASE_URL)}</link>
    <description>${xmlEscape(CHANNEL_DESCRIPTION)}</description>
    <language>en</language>
    <lastBuildDate>${xmlEscape(now)}</lastBuildDate>
${itemXml}
  </channel>
</rss>
`;

writeFileSync(join(repoRoot, 'feed.xml'), xml);
console.log(`Wrote feed.xml with ${items.length} item(s).`);
