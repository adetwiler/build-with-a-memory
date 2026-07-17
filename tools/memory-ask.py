#!/usr/bin/env python3
"""
ASK THE MEMORY. Hybrid retrieval: BM25 (exact terms) + vectors (paraphrase),
fused with Reciprocal Rank Fusion.

  python3 memory-ask.py "what did we decide about pricing?"
  python3 memory-ask.py "why is the retry limit 3" -n 3
  python3 memory-ask.py "auth flow" --json          # for tools/agents

RRF is used rather than score-mixing because BM25 scores and cosine
similarities are not on the same scale; fusing by RANK is the standard fix
and needs no tuning.

Reads the same optional memory-tools.json as memory-index.py (db path, model,
Ollama URL). Run memory-index.py first to build the index.
"""
import argparse, json, pathlib, sqlite3, subprocess, sys
import numpy as np

K = 60          # RRF damping: standard value


def config():
    p = pathlib.Path("memory-tools.json")
    cfg = json.loads(p.read_text()) if p.exists() else {}
    cfg.setdefault("db", ".memory-index.db")
    cfg.setdefault("model", "nomic-embed-text")
    cfg.setdefault("ollama", "http://localhost:11434")
    return cfg


CFG = config()
DB = pathlib.Path(CFG["db"]).expanduser()


def embed(text):
    r = subprocess.run(
        ["curl", "-s", f"{CFG['ollama']}/api/embeddings", "-d",
         json.dumps({"model": CFG["model"], "prompt": text})],
        capture_output=True, text=True, timeout=60)
    return json.loads(r.stdout)["embedding"]


def search(query, n=5, pool=40):
    db = sqlite3.connect(DB)

    # 1. semantic: brute-force cosine. A few thousand chunks is milliseconds
    #    and needs no vector extension (embeddings are stored pre-normalized).
    #    DEGRADE GRACEFULLY when Ollama is down: fall back to keyword-only
    #    instead of crashing.
    vec_hits = []
    try:
        qv = np.asarray(embed(query), dtype=np.float32)
    except Exception:
        print("[ask] Ollama unreachable: keyword-only results (start Ollama for semantic search)", file=sys.stderr)
        qv = None
    rows = db.execute("SELECT id, embedding FROM chunks WHERE embedding IS NOT NULL").fetchall() if qv is not None else []
    if qv is not None and rows:
        ids = np.array([r[0] for r in rows])
        mat = np.frombuffer(b"".join(r[1] for r in rows), dtype=np.float32).reshape(len(rows), -1)
        qv /= (np.linalg.norm(qv) or 1)
        with np.errstate(all="ignore"):
            sims = mat @ qv
        vec_hits = [int(ids[i]) for i in np.argsort(-sims)[:pool]]

    # 2. lexical: BM25. FTS5 chokes on punctuation, so quote each term.
    terms = " OR ".join(f'"{w}"' for w in query.split() if len(w) > 2)
    kw_hits = []
    if terms:
        try:
            kw_hits = [r[0] for r in db.execute(
                "SELECT rowid FROM chunks_fts WHERE chunks_fts MATCH ? "
                "ORDER BY bm25(chunks_fts) LIMIT ?", (terms, pool))]
        except sqlite3.OperationalError:
            pass

    # 3. Reciprocal Rank Fusion
    scores = {}
    for rank, cid in enumerate(vec_hits):
        scores[cid] = scores.get(cid, 0) + 1 / (K + rank + 1)
    for rank, cid in enumerate(kw_hits):
        scores[cid] = scores.get(cid, 0) + 1 / (K + rank + 1)

    out = []
    home = str(pathlib.Path.home())
    for cid, score in sorted(scores.items(), key=lambda x: -x[1])[:n]:
        row = db.execute(
            "SELECT path, tag, heading, body FROM chunks WHERE id=?", (cid,)).fetchone()
        if not row:
            continue
        path, tag, heading, body = row
        out.append({
            "score": round(score, 4),
            "source": str(path).replace(home, "~"),
            "tag": tag,
            "heading": heading,
            "text": body,
            "found_by": ("both" if cid in vec_hits and cid in kw_hits
                         else "meaning" if cid in vec_hits else "exact term"),
        })
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("query", nargs="+")
    ap.add_argument("-n", type=int, default=5)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    q = " ".join(a.query)

    if not DB.exists():
        print("no index yet: python3 memory-index.py", file=sys.stderr)
        sys.exit(1)

    hits = search(q, a.n)
    if a.json:
        print(json.dumps(hits, indent=2))
        return

    if not hits:
        print("nothing found.")
        return
    print(f'\n"{q}"\n')
    for i, h in enumerate(hits, 1):
        print(f"--- {i}. [{h['tag']}] {h['heading'] or '(no heading)'}")
        print(f"    {h['source']}  ·  matched on {h['found_by']}")
        body = h["text"]
        print("    " + (body[:600] + ("..." if len(body) > 600 else "")).replace("\n", "\n    "))
        print()


if __name__ == "__main__":
    main()
