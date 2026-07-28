#!/usr/bin/env bash
#
# release-check.sh: the one command to run before this repo ships anywhere
# public (the public flip, a batch push, a release). It answers two questions
# the per-commit hook cannot answer alone:
#
#   SAFE:     does the whole tracked tree leak anything private?
#   ACCURATE: do the docs still agree with themselves and with the files
#             they point at?
#
# The pre-commit hook checks each commit's additions. This checks everything,
# at once, right before the moment that matters. Run from anywhere in the
# repo: bash scripts/release-check.sh
#
# Checks, in order:
#   1. Leak audit (scripts/leak-audit.sh): denylist terms, emails, home paths.
#   2. Dash scan: no em or en dash anywhere in the tracked tree.
#   3. Prompt sync: the prompt embedded in README.md is byte-identical to
#      prompt.txt. Two copies of the hero prompt that drift is the most
#      embarrassing inaccuracy this repo could ship.
#   4. Dead links: every relative markdown link in every tracked .md file
#      points at a file that exists.
#   5. Feed freshness: feed.xml is not older than the newest post in posts/.
#   6. Feed link shape: every post has an item link at the site's devlog path.
#
# See method/09-safety-nets.md: each gate is a mistake class turned into a
# guard. A green run is not a promise of perfection; it is proof the known
# failure modes were checked mechanically instead of by eye.

set -euo pipefail

repo_root="$(git rev-parse --show-toplevel)"
cd "$repo_root"

fail=0
say_fail() { echo "FAIL: $*"; fail=1; }

# --- 1. Leak audit -----------------------------------------------------------
if bash scripts/leak-audit.sh; then
  :
else
  say_fail "leak audit found private tells (see above)"
fi

# --- 2. Whole-tree dash scan -------------------------------------------------
# Byte escapes so this file never contains the characters it bans.
EMDASH="$(printf '\342\200\224')"
ENDASH="$(printf '\342\200\223')"
dash_hits="$(git grep -I -n -F -e "$EMDASH" -e "$ENDASH" -- . 2>/dev/null || true)"
if [ -n "$dash_hits" ]; then
  say_fail "em or en dash in the tracked tree:"
  printf '%s\n' "$dash_hits" | sed 's/^/  /'
fi

# --- 3. Prompt sync ----------------------------------------------------------
# Extract the first fenced code block from README.md and compare to prompt.txt.
readme_prompt="$(awk '/^```$/{if(inblk){exit}} /^```/{inblk=1;next} inblk{print}' README.md)"
if ! printf '%s\n' "$readme_prompt" | diff -q - prompt.txt >/dev/null 2>&1; then
  say_fail "README.md's embedded prompt differs from prompt.txt:"
  printf '%s\n' "$readme_prompt" | diff - prompt.txt | head -20 | sed 's/^/  /'
fi

# --- 4. Dead relative markdown links ----------------------------------------
# Links inside fenced code blocks are examples, not links; skip those lines.
dead_links=""
while IFS= read -r md; do
  targets="$(awk '
    /^```/ { fence = !fence; next }
    !fence { print }
  ' "$md" | grep -oE '\]\([^)#]+[^)]*\)' | sed 's/^](//; s/)$//; s/#.*//' || true)"
  while IFS= read -r t; do
    [ -z "$t" ] && continue
    case "$t" in
      http://*|https://*|mailto:*) continue ;;
    esac
    dir="$(dirname "$md")"
    if [ ! -e "$dir/$t" ] && [ ! -e "$t" ]; then
      dead_links="${dead_links}
  $md -> $t"
    fi
  done <<< "$targets"
done < <(git ls-files '*.md')
if [ -n "$dead_links" ]; then
  say_fail "dead relative links:${dead_links}"
fi

# --- 5. Feed freshness -------------------------------------------------------
# README.md is excluded to mirror make-feed.mjs: it is folder documentation,
# not a post, so editing it must not demand a feed rebuild.
if [ -d posts ] && [ -f feed.xml ]; then
  newest_post="$(ls -t posts/*.md 2>/dev/null | grep -v '/README\.md$' | head -1 || true)"
  if [ -n "$newest_post" ] && [ "$newest_post" -nt feed.xml ]; then
    say_fail "feed.xml is older than $newest_post (run: node scripts/make-feed.mjs)"
  fi
fi

# --- 6. Feed link shape ------------------------------------------------------
# Freshness is a timestamp. It says nothing about whether the links POINT
# anywhere, and for four days every item in feed.xml returned 404 while check 5
# reported the feed fresh: the base URL had been swapped to the site per the
# 2026-07-27 audition while the path still built the old GitHub blob layout.
#
# So this asserts the SHAPE the audition decided on: one item per post, at the
# site's /devlog/<slug>/ path. Deliberately offline. A gate that needs the
# network is a gate that gets skipped, and the failure this catches is a wrong
# URL, not a down server.
if [ -d posts ] && [ -f feed.xml ]; then
  bad_feed_links=""
  for post in posts/*.md; do
    [ -e "$post" ] || continue
    case "$post" in */README.md) continue ;; esac
    slug="$(basename "$post" .md)"
    if ! grep -q "<link>https://buildwithamemory.com/devlog/${slug}/</link>" feed.xml; then
      bad_feed_links="${bad_feed_links}
  - ${slug} has no /devlog/${slug}/ item link"
    fi
  done
  if [ -n "$bad_feed_links" ]; then
    say_fail "feed.xml item links are wrong (run: node scripts/make-feed.mjs):${bad_feed_links}"
  fi
fi

echo ""
if [ "$fail" -ne 0 ]; then
  echo "RELEASE CHECK FAILED. Fix the items above before anything ships."
  exit 1
fi
echo "Release check clean: no leaks, no dashes, prompt in sync, links resolve, feed fresh and pointing at real pages."
exit 0
