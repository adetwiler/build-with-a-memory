#!/usr/bin/env bash
# memory-check.sh [--fix] [dir ...] - memory-network link health.
# Reports (and with --fix, heals ONLY the safe one):
#   1. DANGLING [[links]]   - a [[name]] with no matching <name>.md node anywhere
#   2. MISSING md links     - a markdown [text](path.md) whose target file is absent
#   3. ORPHANS              - a note not referenced by its folder's index file
#                             (MEMORY.md or INDEX.md, if one exists)
# Never deletes anything, never CREATES a node. Dangling links are intentional
# "note worth writing" TODOs (start with a link) - they are SURFACED, never
# auto-stubbed. --fix heals ONLY missing index pointers for orphans (harmless);
# everything else is report-only. A checker with false positives just trains
# you to ignore the report, so resolution is deliberately generous (it tries
# both hyphen and underscore spellings before calling a link dangling).
#
# Usage: bash memory-check.sh            # checks ./docs and . (top level)
#        bash memory-check.sh ~/notes ~/code/project/docs
set -uo pipefail
FIX=0; [ "${1:-}" = "--fix" ] && { FIX=1; shift; }

dirs=("$@")
if [ ${#dirs[@]} -eq 0 ]; then
  [ -d "./docs" ] && dirs+=("./docs")
  dirs+=(".")
fi

# Build ONE global node index across every given dir. A [[link]] is only truly
# dangling if the node exists NOWHERE: the network is one graph, resolve it
# like one graph.
NODE_INDEX=$(mktemp)
trap 'rm -f "$NODE_INDEX"' EXIT
for d in "${dirs[@]}"; do
  [ -d "$d" ] || continue
  while IFS= read -r f; do
    b=$(basename "$f" .md)
    case "$b" in MEMORY|INDEX) continue;; esac
    printf '%s\n' "$b"
  done < <(find "$d" -type f -name '*.md' -not -path '*/.git/*' -not -path '*/node_modules/*' 2>/dev/null)
done | sort -u > "$NODE_INDEX"

dangling=0; orphan=0; broken=0
for d in "${dirs[@]}"; do
  [ -d "$d" ] || continue
  idx=""
  for cand in "$d/MEMORY.md" "$d/INDEX.md"; do
    [ -f "$cand" ] && { idx="$cand"; break; }
  done
  short="$d"

  # 1) dangling [[links]] (ignore literal syntax examples in prose)
  for t in $(grep -rIhoE '\[\[[a-z0-9][a-z0-9_-]+\]\]' "$d" 2>/dev/null | sed 's/\[\[//;s/\]\]//' | sort -u); do
    case "$t" in link|links|linked|wiki-link|wikilink|wikilinks|name|their-name|slug|that-slug) continue;; esac
    # Try the other naming convention (hyphen<->underscore) before declaring dangling.
    t_us=${t//-/_}; t_hy=${t//_/-}; resolved=0
    for cand in "$t" "$t_us" "$t_hy"; do
      grep -qxF "$cand" "$NODE_INDEX" && { resolved=1; break; }
    done
    if [ "$resolved" = 0 ]; then
      echo "DANGLING  $short  ->  [[$t]] (no node - write it, or leave as a TODO)"
      dangling=$((dangling+1))
    fi
  done

  # 2) MISSING markdown [text](path.md) targets - relative (resolved against
  #    the linking file), ~-prefixed, or absolute. Ignore http(s) + anchors.
  while IFS= read -r f; do
    [ -f "$f" ] || continue
    fdir="$(dirname "$f")"
    while IFS= read -r target; do
      [ -z "$target" ] && continue
      case "$target" in
        http://*|https://*|\#*) continue;;
      esac
      target="${target%%#*}"
      [ -z "$target" ] && continue
      case "$(basename "$target")" in
        file.md|path.md|name.md|slug.md|target.md|example.md|foo.md|their-name.md) continue;;
      esac
      case "$target" in
        \~*)  resolved_p="${target/#\~/$HOME}";;
        /*)   resolved_p="$target";;
        *)    resolved_p="$fdir/$target";;
      esac
      if [ ! -e "$resolved_p" ]; then
        echo "MISSING   $f  ->  ($target) (link target not found)"
        broken=$((broken+1))
      fi
    done < <(grep -oE '\]\([^)]+\.md(#[^)]*)?\)' "$f" 2>/dev/null | sed -E 's/^\]\(//; s/\)$//')
  done < <(find "$d" -maxdepth 3 -name '*.md' -not -path '*/.git/*' -not -path '*/node_modules/*' 2>/dev/null)

  # 3) orphans - a note not named in the folder's index (only if one exists)
  [ -n "$idx" ] || continue
  idxname=$(basename "$idx")
  for f in "$d"/*.md; do
    [ -f "$f" ] || continue
    b=$(basename "$f"); [ "$b" = "$idxname" ] && continue
    if ! grep -qF "$b" "$idx"; then
      echo "ORPHAN    $short  ->  $b (not in $idxname)"
      orphan=$((orphan+1))
      if [ "$FIX" = 1 ]; then
        title=$(sed -n 's/^description: //p' "$f" | head -1)
        printf -- '- [%s](%s) - %s\n' "${b%.md}" "$b" "${title:-(add a hook)}" >> "$idx"
        echo "  -> added index pointer"
      fi
    fi
  done
done

echo
echo "memory-check: $dangling dangling link(s), $orphan orphan(s), $broken missing md-link(s).$([ "$FIX" = 1 ] && echo ' (orphan index pointers healed; dangling/missing are report-only TODOs)' || echo ' Run with --fix to heal orphan index pointers only.')"
