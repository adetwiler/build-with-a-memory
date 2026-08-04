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
# feed.xml is GENERATED. On 2026-07-27 it was hand-edited to the /devlog/<slug>/
# shape the audition decided on, and make-feed.mjs was left emitting the old
# GitHub blob layout. So the artifact was right and its generator was wrong, and
# the next regeneration silently reverted the hand-edit: every item 404'd while
# check 5 called the feed fresh, because freshness compares timestamps and says
# nothing about where a link points.
#
# The root bug is hand-editing a generated file. This check is the backstop that
# notices when the artifact and the decision disagree, whichever one drifted.
# Deliberately offline: a gate that needs the network is a gate that gets
# skipped, and the failure this catches is a wrong URL, not a down server.
if [ -d posts ] && [ -f feed.xml ]; then
  bad_feed_links=""
  for post in posts/*.md; do
    [ -e "$post" ] || continue
    case "$post" in */README.md) continue ;; esac
    slug="$(basename "$post" .md)"
    if ! grep -q "<link>https://buildwiththememory.com/devlog/${slug}/</link>" feed.xml; then
      bad_feed_links="${bad_feed_links}
  - ${slug} has no /devlog/${slug}/ item link"
    fi
  done
  if [ -n "$bad_feed_links" ]; then
    say_fail "feed.xml item links are wrong (run: node scripts/make-feed.mjs):${bad_feed_links}"
  fi
fi

# --- 7. Pillar integrity ---------------------------------------------------
# Every method/NN-*.md must have a row in THE-METHOD.md, and the written-out
# pillar count must match the file count. This exists because the count HAS
# drifted (the site said twelve while the repo had thirteen), and pillar 14's
# own corollary applies to this repo too: a lesson that matters becomes a
# check, not a comment.
#
# 2026-07-28: an earlier edit appended this section AFTER the script's exit
# statements, so the gate the devlog post describes never ran. A gate that is
# never executed is a comment. It now runs with the other checks; do not move
# it below the summary block again.
if [ -d method ] && [ -f THE-METHOD.md ]; then
  pillar_missing=""
  pillar_count=0
  for m in method/[0-9][0-9]-*.md; do
    pillar_count=$((pillar_count + 1))
    grep -q "](${m})" THE-METHOD.md || pillar_missing="${pillar_missing} ${m}"
  done
  if [ -n "$pillar_missing" ]; then
    say_fail "pillar file(s) missing from THE-METHOD.md table:${pillar_missing}"
  fi
  count_word=""
  case $pillar_count in
    12) count_word="twelve" ;; 13) count_word="thirteen" ;; 14) count_word="fourteen" ;;
    15) count_word="fifteen" ;; 16) count_word="sixteen" ;; 17) count_word="seventeen" ;;
    18) count_word="eighteen" ;; 19) count_word="nineteen" ;; 20) count_word="twenty" ;;
  esac
  if [ -n "$count_word" ] && ! grep -qi "The ${count_word} pillars" THE-METHOD.md; then
    say_fail "method/ holds ${pillar_count} pillars but THE-METHOD.md does not say 'The ${count_word} pillars'."
  else
    echo "Pillar integrity: ${pillar_count} pillar files, all in the table, count word matches."
  fi
fi

# --- 8. Prose lint (reads-like-a-person check) -------------------------------
# Every published .md in posts/ and method/ passes the local prose lint, which
# blocks the mechanical tells of generated writing (broken idioms, hype words,
# narration adverbs, banned constructions). This exists because the pillar 14
# post shipped with lines like "Honest label on the tin" and a narration adverb
# that no human pass caught. The lint is a machine-local tool; when it is not
# installed the check says so out loud instead of silently passing.
VOICE_LINT="${HOME}/.claude/scripts/voice-lint.mjs"
if [ -f "$VOICE_LINT" ]; then
  prose_files="$(git ls-files 'posts/*.md' 'method/*.md' | grep -v '/README\.md$' || true)"
  if [ -n "$prose_files" ]; then
    # shellcheck disable=SC2086
    if ! node "$VOICE_LINT" $prose_files; then
      say_fail "prose lint found blocking tells in published posts/method files (see above)"
    fi
  fi
else
  echo "SKIP: prose lint not installed on this machine (voice-lint.mjs); prose was not checked."
fi

echo ""
if [ "$fail" -ne 0 ]; then
  echo "RELEASE CHECK FAILED. Fix the items above before anything ships."
  exit 1
fi
echo "Release check clean: no leaks, no dashes, prompt in sync, links resolve, feed fresh and pointing at real pages, pillars counted, prose linted."
exit 0
