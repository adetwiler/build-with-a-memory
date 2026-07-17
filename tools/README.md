# Layer 2: search, graph, and link health

The [seed prompt](../prompt.txt) gives a project plain-file memory: a short
main file, `docs/now.md`, `docs/decisions.md`, `docs/notes.md`. That is layer
1, and it needs nothing installed.

These tools are layer 2, for when the network outgrows grep: you have notes
across several projects, you can't remember which file holds a decision, or
links have started to rot. Everything here keeps the same rule as the rest of
the method: **markdown stays the source of truth.** The index is derived and
disposable; delete it and rebuild in a minute. Nothing leaves your machine.

## What's here

| Tool | What it does |
|---|---|
| `memory-index.py` | Builds one SQLite index over your notes: BM25 keyword (FTS5) + local embeddings (Ollama). Incremental by content hash; a run with no edits is a no-op. |
| `memory-ask.py` | Queries the index. Hybrid retrieval fused by rank (RRF): exact tokens AND paraphrase. Answers in fractions of a second. `--json` for agents. |
| `memory-graph.mjs` | Renders your network as an interactive force graph (one self-contained HTML file). Nodes are notes, edges are `[[wikilinks]]`. |
| `memory-check.sh` | Link health: dangling `[[links]]`, missing markdown link targets, orphan notes no index references. `--fix` heals orphan index pointers only; it never deletes or creates notes. |

## Setup

Prerequisites: `python3` with `numpy` (`pip install numpy`), `node` 18+ (for
the graph), and optionally [Ollama](https://ollama.com) for semantic search:

```bash
ollama pull nomic-embed-text
```

Without Ollama everything still works; search is keyword-only.

Copy the tools anywhere (or run them from a clone of this repo). Then, from
the project you want indexed:

```bash
python3 tools/memory-index.py      # build / sync the index
python3 tools/memory-ask.py "why did we pick postgres"
node tools/memory-graph.mjs ./docs # writes ./memory-graph/index.html
bash tools/memory-check.sh         # link health report
```

Add `.memory-index.db` and `memory-graph/` to your `.gitignore`.

## Indexing more than one project

Drop a `memory-tools.json` next to where you run the tools:

```json
{
  "db": "~/.memory-index.db",
  "roots": [
    {"tag": "app", "path": "~/code/my-app"},
    {"tag": "notes", "path": "~/notes"},
    {"tag": "game", "path": "~/code/my-game/docs"}
  ]
}
```

A root that looks like a project (it has `docs/` or a `CLAUDE.md`-style main
file) gets its memory surfaces indexed, not its whole tree. A plain folder of
markdown gets indexed as-is. Tags show up in results so you know which
network answered.

## Wiring it into an agent

Two lines in your main memory file are enough:

```
Before starting substantive work, run:
  python3 tools/memory-ask.py "<the task topic>" --json
and read what comes back before deciding anything.
```

The habit matters more than the tooling: the index only knows what you wrote
down. The [method docs](../method/) cover the writing-down half.

## Notes

- The first `memory-graph.mjs` run downloads `force-graph.min.js` (MIT) from
  unpkg into the output folder; after that the page works fully offline.
- `memory-check.sh` treats dangling `[[links]]` as deliberate "note worth
  writing" markers, not errors. It reports them; it never auto-creates stubs.
- Embeddings run locally so private notes stay private. If you point the
  tools at notes containing secrets, the index file contains them too; treat
  `.memory-index.db` with the same care as the notes themselves.
