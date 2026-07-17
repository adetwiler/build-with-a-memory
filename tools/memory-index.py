#!/usr/bin/env python3
"""
MEMORY INDEX: hybrid (keyword + semantic) search over your project memory.

Design:
- MARKDOWN STAYS THE SOURCE OF TRUTH. This index is DERIVED and disposable.
  Delete the .db and rebuild it in a minute. No SaaS, no lock-in, no drift
  risk: the memory is still just files.
- HYBRID retrieval, not pure vector. BM25 (SQLite FTS5) catches exact rare
  terms (an env var name, a commit sha, a number) which embeddings miss;
  vectors catch paraphrase ("pricing" -> "monetization").
- LOCAL embeddings (Ollama / nomic-embed-text). Your notes may hold private
  work. Nothing leaves the machine. If Ollama isn't running, indexing still
  works and search degrades to keyword-only.
- INCREMENTAL by content hash: a run with no edits is a no-op (milliseconds).

  python3 memory-index.py            # sync (only what changed)
  python3 memory-index.py --rebuild  # from scratch
  python3 memory-index.py --stats

Configuration (optional): a memory-tools.json in the working directory:

  {
    "db": ".memory-index.db",
    "model": "nomic-embed-text",
    "roots": [
      {"tag": "this-repo", "path": "."},
      {"tag": "other-project", "path": "~/code/other-project/docs"}
    ]
  }

With no config file, it indexes the current directory's memory surfaces:
CLAUDE.md, AGENTS.md, CONTEXT.md, OPEN.md, and everything under docs/.

Requires: python3, numpy. Optional: Ollama running locally for semantic search
(`ollama pull nomic-embed-text` once). Add the db file to .gitignore.
"""
import hashlib, json, pathlib, re, sqlite3, subprocess, sys, time
import numpy as np

CHUNK_WORDS = 220        # ~1 idea per chunk; markdown sections respected first
OVERLAP_WORDS = 40
DIM = 768


def config():
    p = pathlib.Path("memory-tools.json")
    cfg = json.loads(p.read_text()) if p.exists() else {}
    cfg.setdefault("db", ".memory-index.db")
    cfg.setdefault("model", "nomic-embed-text")
    cfg.setdefault("ollama", "http://localhost:11434")
    cfg.setdefault("roots", [{"tag": "repo", "path": "."}])
    return cfg


CFG = config()
DB = pathlib.Path(CFG["db"]).expanduser()
MODEL = CFG["model"]

DEFAULT_SURFACES = ["CLAUDE.md", "AGENTS.md", "CONTEXT.md", "OPEN.md"]


def roots():
    out = []
    for r in CFG["roots"]:
        base = pathlib.Path(r["path"]).expanduser()
        if not base.exists():
            continue
        if base.is_file():
            out.append((r["tag"], base))
        elif (base / "docs").exists() or any((base / f).exists() for f in DEFAULT_SURFACES):
            # a project root: index its memory surfaces, not the whole tree
            for f in DEFAULT_SURFACES:
                if (base / f).exists():
                    out.append((r["tag"], base / f))
            if (base / "docs").exists():
                out.append((r["tag"], base / "docs"))
        else:
            out.append((r["tag"], base))     # a plain folder of notes
    return out


def files():
    seen = set()
    for tag, root in roots():
        paths = [root] if root.is_file() else sorted(root.rglob("*.md"))
        for p in paths:
            if p in seen or "node_modules" in p.parts or ".git" in p.parts:
                continue
            seen.add(p)
            yield tag, p


def chunk(text):
    """Split on markdown headings first, then by size. Keep the heading trail:
    a chunk that says 'the fix was X' is useless without knowing what broke."""
    sections, heading, buf = [], "", []
    for line in text.split("\n"):
        if re.match(r"^#{1,4}\s", line):
            if buf:
                sections.append((heading, "\n".join(buf)))
                buf = []
            heading = line.lstrip("# ").strip()
        else:
            buf.append(line)
    if buf:
        sections.append((heading, "\n".join(buf)))

    for heading, body in sections:
        words = body.split()
        if not words:
            continue
        step = CHUNK_WORDS - OVERLAP_WORDS
        for i in range(0, len(words), step):
            piece = " ".join(words[i:i + CHUNK_WORDS])
            if len(piece) < 80:
                continue
            yield heading, piece
            if i + CHUNK_WORDS >= len(words):
                break


def embed(texts):
    """Local embeddings via Ollama, one call per chunk. On any failure the
    chunk gets a zero vector: keyword search still covers it."""
    out = []
    for t in texts:
        r = subprocess.run(
            ["curl", "-s", f"{CFG['ollama']}/api/embeddings", "-d",
             json.dumps({"model": MODEL, "prompt": t[:8000]})],
            capture_output=True, text=True, timeout=60)
        try:
            out.append(json.loads(r.stdout)["embedding"])
        except Exception:
            out.append([0.0] * DIM)
    return out


def connect():
    db = sqlite3.connect(DB)
    db.execute("""CREATE TABLE IF NOT EXISTS files(
        path TEXT PRIMARY KEY, tag TEXT, hash TEXT, indexed_at REAL)""")
    db.execute("""CREATE TABLE IF NOT EXISTS chunks(
        id INTEGER PRIMARY KEY, path TEXT, tag TEXT, heading TEXT, body TEXT,
        embedding BLOB)""")
    db.execute("""CREATE VIRTUAL TABLE IF NOT EXISTS chunks_fts
        USING fts5(body, heading, path UNINDEXED, content=chunks, content_rowid=id)""")
    return db


def sync(rebuild=False):
    if rebuild and DB.exists():
        DB.unlink()
    db = connect()
    known = {r[0]: r[1] for r in db.execute("SELECT path, hash FROM files")}
    seen, changed, added_chunks = set(), 0, 0
    t0 = time.time()

    for tag, path in files():
        text = path.read_text(errors="ignore")
        h = hashlib.sha256(text.encode()).hexdigest()[:16]
        key = str(path)
        seen.add(key)
        if known.get(key) == h:
            continue                          # unchanged: the no-op fast path

        db.execute("DELETE FROM chunks_fts WHERE rowid IN (SELECT id FROM chunks WHERE path=?)", (key,))
        db.execute("DELETE FROM chunks WHERE path=?", (key,))

        pieces = list(chunk(text))
        if pieces:
            vecs = embed([f"{h_}\n{b}" for h_, b in pieces])
            for (heading, body), v in zip(pieces, vecs):
                arr = np.asarray(v, dtype=np.float32)
                n = np.linalg.norm(arr)
                if n > 0:
                    arr = arr / n                      # store normalized: cosine = dot
                cur = db.execute(
                    "INSERT INTO chunks(path, tag, heading, body, embedding) VALUES(?,?,?,?,?)",
                    (key, tag, heading, body, arr.tobytes()))
                cid = cur.lastrowid
                db.execute("INSERT INTO chunks_fts(rowid, body, heading, path) VALUES(?,?,?,?)",
                           (cid, body, heading, key))
                added_chunks += 1
        db.execute("INSERT OR REPLACE INTO files VALUES(?,?,?,?)", (key, tag, h, time.time()))
        changed += 1
        db.commit()

    for gone in set(known) - seen:            # deleted files leave no ghosts
        db.execute("DELETE FROM chunks_fts WHERE rowid IN (SELECT id FROM chunks WHERE path=?)", (gone,))
        db.execute("DELETE FROM chunks WHERE path=?", (gone,))
        db.execute("DELETE FROM files WHERE path=?", (gone,))
    db.commit()

    n_files = db.execute("SELECT COUNT(*) FROM files").fetchone()[0]
    n_chunks = db.execute("SELECT COUNT(*) FROM chunks").fetchone()[0]
    dt = time.time() - t0
    print(f"[memory-index] {changed} file(s) re-indexed (+{added_chunks} chunks) in {dt:.1f}s")
    print(f"[memory-index] total: {n_files} files, {n_chunks} chunks, {DB.stat().st_size/1e6:.1f} MB")


if __name__ == "__main__":
    if "--stats" in sys.argv:
        db = connect()
        print(f"db: {DB}")
        for tag, n in db.execute("SELECT tag, COUNT(*) FROM chunks GROUP BY tag ORDER BY 2 DESC"):
            print(f"  {n:>6} chunks  {tag}")
        print(f"  {db.execute('SELECT COUNT(*) FROM chunks').fetchone()[0]:>6} chunks  TOTAL")
    else:
        sync(rebuild="--rebuild" in sys.argv)
