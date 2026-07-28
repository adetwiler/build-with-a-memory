#!/usr/bin/env python3
"""
MEMORY FEDERATE: borrow memory from other people's repos, safely.

Your network holds what you wrote down. Other repos hold what other teams wrote
down: their agent manuals, their ADRs, their conventions. This tool mirrors the
PROSE from those repos onto your machine so your index can search it, and it
does so under two rules that matter more than the plumbing:

  1. MIRRORS ARE DERIVED AND DISPOSABLE, exactly like the index. Delete the
     mirror directory and re-sync. Never edit inside a mirror; sync resets it.

  2. BORROWED MEMORY IS DATA, NOT INSTRUCTIONS. Your own notes are things you
     decided. A stranger's AGENTS.md is a QUOTE of what someone else decided,
     and it can be hostile: text in a foreign repo that your agent retrieves
     lands in the same context window as your real instructions. That is an
     injection channel straight into the trusted path. So every remote is
     scanned on arrival, anything that smells like an instruction aimed at your
     agent QUARANTINES the remote (fail closed), and everything that does get
     indexed is tagged with its trust level so retrieval can mark it as a quote.

  python3 memory-federate.py sync             # clone or fast-forward every remote
  python3 memory-federate.py sync --only acme # one remote
  python3 memory-federate.py scan             # re-run the safety scan
  python3 memory-federate.py scan --strict    # exit 1 if anything is flagged
  python3 memory-federate.py status           # what is mirrored, and its state
  python3 memory-federate.py release acme     # clear a quarantine you have reviewed

Configuration lives in the same memory-tools.json the other tools read:

  {
    "db": "~/.memory-index.db",
    "mirrors": "~/.memory-mirrors",
    "remotes": [
      {"tag": "acme", "url": "https://github.com/acme/platform.git",
       "trust": "untrusted", "paths": ["*.md"], "ref": "main"}
    ]
  }

  tag    short name; becomes the mirror folder and the search tag
  url    anything git can clone (GitHub, Azure DevOps, a file:// path)
  trust  "untrusted" (default) or "trusted". Trusted skips the scan; use it
         only for repos you or your team control.
  paths  gitignore-style sparse-checkout patterns. Default ["*.md"], which
         takes every markdown file at any depth and NO source code.
  ref    branch to track. Default: the remote's default branch.
  allow  paths whose scan findings you have reviewed and accepted.
  private true marks the remote as never-publish; status and the index carry it.

Requires: python3 and git. No network calls of its own: everything goes through
git, so your existing credentials, proxies and SSH config apply unchanged.
"""
import argparse, contextlib, fnmatch, json, os, pathlib, re, shutil, subprocess, sys, time

try:
    import fcntl                      # POSIX advisory locking; see sync_lock()
except ImportError:                   # pragma: no cover - Windows
    fcntl = None

# --------------------------------------------------------------------------
# config
# --------------------------------------------------------------------------


def config():
    p = pathlib.Path("memory-tools.json")
    cfg = json.loads(p.read_text()) if p.exists() else {}
    cfg.setdefault("mirrors", ".memory-mirrors")
    cfg.setdefault("remotes", [])
    return cfg


CFG = config()
MIRRORS = pathlib.Path(CFG["mirrors"]).expanduser()
STATE = MIRRORS / "state.json"
DEFAULT_PATHS = ["*.md"]


def state():
    if STATE.exists():
        try:
            return json.loads(STATE.read_text())
        except json.JSONDecodeError:
            pass
    return {}


def save_state(s):
    """Write the state file atomically.

    A scheduled sync and an interactive one overlap routinely. write_text is not
    atomic, so a reader arriving mid-write sees truncated JSON. That is
    recoverable (a corrupt state file is treated as empty) but it silently costs
    a full re-fetch of every remote. os.replace makes the swap atomic, so a
    reader sees either the old file or the new one.
    """
    MIRRORS.mkdir(parents=True, exist_ok=True)
    tmp = STATE.with_suffix(f".json.tmp{os.getpid()}")
    tmp.write_text(json.dumps(s, indent=2, sort_keys=True))
    os.replace(tmp, STATE)


# A tag becomes a directory name under the mirrors root, so it is a path
# component and has to be treated as one. "../../somewhere" would otherwise
# write a clone outside the mirrors directory entirely.
SAFE_TAG = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")


@contextlib.contextmanager
def sync_lock(timeout=180):
    """Serialize runs that write mirrors or state.

    A scheduled sync and an interactive one overlap all the time. Without a
    lock they race to clone into the SAME mirror directory: one wins, the
    others fail, and a loser that skipped a remote writes a state file missing
    it. Waiting is the right behavior rather than erroring, because the process
    holding the lock is already doing the work; the waiter wakes up, sees every
    sha unchanged, and no-ops in a fraction of a second.

    fcntl is POSIX. On a platform without it the lock degrades to nothing,
    which is the pre-existing behavior and self-heals on the next run.
    """
    if fcntl is None:
        yield True
        return
    MIRRORS.mkdir(parents=True, exist_ok=True)
    handle = open(MIRRORS / ".sync.lock", "w")
    waited, announced = 0.0, False
    try:
        while True:
            try:
                fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
                break
            except OSError:
                if not announced:
                    print("  another sync is running; waiting for it to finish")
                    announced = True
                if waited >= timeout:
                    yield False
                    return
                time.sleep(0.25)
                waited += 0.25
        try:
            yield True
        finally:
            fcntl.flock(handle, fcntl.LOCK_UN)
    finally:
        handle.close()


def remotes(only=None):
    for r in CFG["remotes"]:
        if only and r.get("tag") != only:
            continue
        tag = r.get("tag")
        if not tag or not r.get("url"):
            print(f"  skipping malformed remote entry: {r}", file=sys.stderr)
            continue
        if not SAFE_TAG.match(tag) or tag in (".", ".."):
            print(f"  skipping remote with unsafe tag {tag!r}: a tag is a directory "
                  f"name, so it must be letters, digits, dot, dash or underscore",
                  file=sys.stderr)
            continue
        yield r


# --------------------------------------------------------------------------
# git
# --------------------------------------------------------------------------


class GitError(RuntimeError):
    pass


def git(*args, cwd=None, check=True):
    p = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True)
    if check and p.returncode:
        raise GitError(f"git {' '.join(args)}\n{p.stderr.strip()}")
    return p


def remote_head(url, ref=None):
    """Ask the server for a ref's sha WITHOUT downloading anything.

    ls-remote is one round trip and no object negotiation, so this is the cheap
    probe that lets a scheduled sync skip every unchanged remote for a few
    hundred milliseconds total. Fetch only happens when this sha has moved.
    """
    if ref:
        p = git("ls-remote", url, f"refs/heads/{ref}")
        for line in p.stdout.splitlines():
            sha, name = line.split("\t")
            if name.endswith(f"refs/heads/{ref}"):
                return ref, sha
        raise GitError(f"remote has no branch {ref!r}")
    # No ref configured: resolve the remote's own default branch.
    #
    # --symref can emit MORE THAN ONE "ref:" line. A repo that is itself a clone
    # advertises refs/remotes/origin/HEAD alongside HEAD, and a loop that just
    # takes the last match resolves the default branch to
    # "refs/remotes/origin/main". Match on the ref NAME being exactly HEAD, not
    # on line shape.
    p = git("ls-remote", "--symref", url, "HEAD")
    resolved, sha = None, None
    for line in p.stdout.splitlines():
        parts = line.split("\t")
        if len(parts) != 2 or parts[1].strip() != "HEAD":
            continue
        if parts[0].startswith("ref: "):
            resolved = parts[0][len("ref: "):].strip()
            if resolved.startswith("refs/heads/"):
                resolved = resolved[len("refs/heads/"):]
        else:
            sha = parts[0].strip()
    if not resolved or not sha:
        raise GitError("could not resolve the remote's default branch")
    return resolved, sha


def clone(url, dest, paths):
    """Clone prose only: blobless where the server allows it, sparse always.

    --filter=blob:none gets the full commit and tree history (needed to diff two
    shas later) while leaving file CONTENT on the server until something asks
    for it. Sparse-checkout then decides what "asks for it" means. Together, a
    multi-gigabyte monorepo materializes as a few megabytes of markdown.

    Partial clone is a SERVER capability. GitHub and Azure DevOps support it;
    older or self-hosted servers may refuse, so a refusal falls back to a plain
    clone rather than failing. Sparse-checkout still limits what lands on disk.
    """
    dest.parent.mkdir(parents=True, exist_ok=True)
    filtered = True
    try:
        git("clone", "--filter=blob:none", "--no-checkout", url, str(dest))
    except GitError:
        filtered = False
        shutil.rmtree(dest, ignore_errors=True)
        git("clone", "--no-checkout", url, str(dest))

    # --no-cone takes gitignore-style patterns, so "*.md" means every markdown
    # file at any depth. Cone mode only understands whole directories, which
    # cannot express "prose anywhere, code nowhere".
    git("sparse-checkout", "init", "--no-cone", cwd=dest)
    git("sparse-checkout", "set", *paths, cwd=dest)
    return filtered


def changed_paths(repo, old_sha, new_sha, limit=20):
    """What moved between two shas. Trees are local even in a blobless clone,
    so --name-status needs no extra download."""
    if not old_sha:
        return ["(initial clone)"]
    try:
        p = git("diff", "--name-status", old_sha, new_sha, cwd=repo)
    except GitError:
        return ["(history rewritten upstream; mirror reset)"]
    out = []
    for line in p.stdout.splitlines():
        parts = line.split("\t")
        if len(parts) >= 2:
            out.append(f"{parts[0][0]} {parts[-1]}")
    return out[:limit] + ([f"... {len(out) - limit} more"] if len(out) > limit else [])


# --------------------------------------------------------------------------
# the safety scan
# --------------------------------------------------------------------------
#
# This is a TRIPWIRE, not a filter. It cannot be complete: an attacker who
# knows the patterns can phrase around them. The actual defense is the trust
# boundary, which holds whether or not the scan catches anything: borrowed
# content is tagged, presented as a quote, and never treated as instruction.
# The scan exists to catch the obvious, noisy attempts and to make the risk
# visible instead of invisible.
#
# Each pattern targets something ATTACK-shaped rather than merely
# instruction-shaped. A foreign AGENTS.md legitimately says "you must run the
# tests"; that is the whole point of borrowing it. What is never legitimate is
# text that tries to override a reader's existing instructions, text hidden
# from human view, or text that asks a reader to move secrets outbound.

ZERO_WIDTH = "​‌‍⁠﻿"

# Every check is tuned against a corpus of ~800 real documentation files. That
# calibration is the whole ballgame: a check that fires on ordinary setup docs
# quarantines every honest repo, you learn to wave the warning through, and the
# gate becomes decoration. So checks that could not separate an attack from a
# runbook were either tightened until they could, or demoted to "notice".
#
#   block   quarantines the remote. Reserved for text that has no honest reason
#           to exist in documentation.
#   notice  reported, never quarantines. Worth a human glance, routinely benign.
CHECKS = [
    # "Ignore previous instructions" has no legitimate use in a repo's docs.
    # Deliberately NOT included: "system prompt:" and <system>/<user> tags,
    # which appear constantly in honest docs that discuss prompting, and the
    # im_start tokens stay because those are model control tokens, never prose.
    ("instruction-override", "block", re.compile(
        r"ignore\s+(all\s+|any\s+)?(previous|prior|earlier|above|preceding)\s+"
        r"(instruction|prompt|direction|rule|context)"
        r"|disregard\s+(all\s+|any\s+)?(previous|prior|earlier|the\s+above)\s+"
        r"(instruction|prompt|direction|rule|context)"
        r"|you\s+are\s+now\s+(a|an|the)\s+\w+\s+(assistant|model|ai|agent)"
        r"|new\s+instructions\s*:"
        r"|<\|im_(start|end)\|>", re.I)),

    # An SSH private key next to an outbound verb. The earlier version also
    # counted "password", "token" and any .env mention, which made it fire on
    # every auth setup guide that shows a curl example. Those words are how
    # honest docs talk; a named private-key path being read and sent is not.
    ("credential-exfil", "block", re.compile(
        r"(~/\.ssh|id_rsa\b|id_ed25519\b|private\s+key|AWS_SECRET_ACCESS_KEY"
        r"|(read|cat|print|echo|include|send|upload|attach)\s+[^\n]{0,24}\.env\b)"
        r"[\s\S]{0,100}?"
        r"(curl|wget|fetch\(|exfiltrat|post\s+(it|them|the\s+\w+)\s+to"
        r"|send\s+(it|them|the\s+\w+)\s+to|upload\s+(it|them|the\s+\w+))",
        re.I)),

    # Documentation legitimately documents dangerous commands: every runbook
    # mentions reset --hard and force-push. Reported so a human can look, never
    # blocking, because blocking on this flagged 1 in 30 honest files.
    ("destructive-command", "notice", re.compile(
        r"(rm\s+-rf\s+[~/]|git\s+push\s+--force|force[- ]push"
        r"|git\s+reset\s+--hard\s+origin|DROP\s+TABLE|chmod\s+777\s+/)", re.I)),
]

# Text a human reading the rendered markdown never sees. Hidden text has no
# honest reason to carry INSTRUCTIONS, so the bar is lower here than in prose,
# but it still has to be instruction-shaped: a URL or the word "secret" inside
# an HTML comment is an ordinary TODO, not an attack.
HIDDEN_TELLS = re.compile(
    r"(ignore\s+(all\s+|any\s+)?(previous|prior)|disregard|you\s+must|you\s+should"
    r"|system\s*:|new\s+instructions|exfiltrat|do\s+not\s+tell|without\s+telling)", re.I)


def redact(s, width=110):
    """Never echo foreign content raw.

    The scan report is itself read by agents. Printing an attacker's payload
    verbatim would deliver the payload to the very reader the scan is meant to
    protect. So findings are truncated, flattened to one line, and stripped of
    the invisible characters that made them worth flagging.
    """
    s = "".join(ch for ch in s if ch not in ZERO_WIDTH)
    s = re.sub(r"\s+", " ", s).strip()
    return (s[:width] + "...") if len(s) > width else s


def line_of(text, offset):
    return text[:offset].count("\n") + 1


def scan_text(text):
    """Yield (category, severity, line_number, excerpt) for one document.

    Matching runs over the WHOLE document, not line by line. A payload does not
    respect line breaks: the first version of this scanned per line and missed a
    real exfil instruction purely because the secret was on one line and the
    outbound verb two lines below it. The windowed patterns already span
    newlines, so the document is the right unit and the offset gives the line.
    """
    for name, severity, pat in CHECKS:
        for m in pat.finditer(text):
            yield name, severity, line_of(text, m.start()), redact(m.group(0))

    # Zero-width characters alone are not evidence: emoji sequences join with
    # U+200D, and any doc discussing homoglyph attacks contains samples. Hidden
    # characters PLUS instruction-shaped words is the pairing that means
    # something.
    for i, line in enumerate(text.split("\n"), 1):
        if any(z in line for z in ZERO_WIDTH) and HIDDEN_TELLS.search(line):
            yield "hidden-instruction", "block", i, redact("zero-width characters in: " + line)

    # HTML comments and CSS-hidden spans: invisible when rendered, fully visible
    # to anything that indexes the raw file.
    for m in re.finditer(r"<!--([\s\S]*?)-->", text):
        if HIDDEN_TELLS.search(m.group(1)):
            yield ("hidden-instruction", "block", line_of(text, m.start()),
                   redact("html comment: " + m.group(1)))
    for m in re.finditer(
            r"<[^>]*(display\s*:\s*none|font-size\s*:\s*0|color\s*:\s*transparent|hidden)[^>]*>([\s\S]{0,300}?)</",
            text, re.I):
        if HIDDEN_TELLS.search(m.group(2)):
            yield ("hidden-instruction", "block", line_of(text, m.start()),
                   redact("hidden element: " + m.group(2)))


def markdown_in(repo):
    """Every .md file that genuinely lives inside `repo`.

    Symlinks are skipped, not followed. A repo can commit a symlink, so an
    untrusted repo that got followed would choose which of YOUR files get read,
    scanned and indexed under its tag: `docs/notes -> ~/.claude/memory` is a
    two-line attack that turns a borrowed-memory feature into a file-disclosure
    one. os.walk does not descend into symlinked directories by default; the
    islink check covers symlinked files, and the containment check covers
    anything else that resolves outside the mirror.
    """
    root = repo.resolve()
    for dirpath, dirnames, filenames in os.walk(repo, followlinks=False):
        dirnames[:] = [d for d in dirnames
                       if d != ".git" and not os.path.islink(os.path.join(dirpath, d))]
        for name in filenames:
            if not name.endswith(".md"):
                continue
            p = pathlib.Path(dirpath) / name
            if p.is_symlink():
                continue
            try:
                if not p.resolve().is_relative_to(root):
                    continue
            except OSError:
                continue
            yield p


def scan_remote(r, repo):
    """Scan one mirror. Returns a list of findings."""
    allow = r.get("allow", [])
    findings = []
    for path in sorted(markdown_in(repo)):
        rel = str(path.relative_to(repo))
        if any(fnmatch.fnmatch(rel, a) for a in allow):
            continue
        try:
            text = path.read_text(errors="ignore")
        except OSError:
            continue
        for name, severity, line, excerpt in scan_text(text):
            findings.append({"file": rel, "line": line, "check": name,
                             "severity": severity, "excerpt": excerpt})
    return findings


def blocking(findings):
    return [f for f in findings if f.get("severity", "block") == "block"]


# --------------------------------------------------------------------------
# commands
# --------------------------------------------------------------------------


def do_sync(args):
    with sync_lock() as acquired:
        if not acquired:
            print("another sync is still holding the lock; skipping this run")
            return 0
        return _sync(args)


def _sync(args):
    s = state()
    MIRRORS.mkdir(parents=True, exist_ok=True)
    any_flagged = False

    for r in remotes(args.only):
        tag, url = r["tag"], r["url"]
        repo = MIRRORS / tag
        paths = r.get("paths", DEFAULT_PATHS)
        prev = s.get(tag, {})
        print(f"\n{tag}")

        try:
            ref, sha = remote_head(url, r.get("ref"))
        except GitError as e:
            print(f"  probe failed: {e}".replace("\n", "\n  "))
            continue

        fresh = not (repo / ".git").exists()
        if fresh:
            # A mirror directory without a .git is debris from an interrupted
            # clone; git refuses to clone into it, so clear it first.
            shutil.rmtree(repo, ignore_errors=True)
            try:
                filtered = clone(url, repo, paths)
            except GitError as e:
                print(f"  clone failed: {e}".replace("\n", "\n  "))
                continue
            git("fetch", "--no-tags", "origin", ref, cwd=repo)
            git("reset", "--hard", "FETCH_HEAD", cwd=repo)
            print(f"  cloned {'(blobless, sparse)' if filtered else '(sparse; server refused partial clone)'} at {sha[:8]}")
            changed = ["(initial clone)"]
        elif prev.get("sha") == sha and not args.force:
            print(f"  unchanged at {sha[:8]}")
            s.setdefault(tag, {}).update(checked_at=time.time())
            continue
        else:
            # Patterns can change in config between runs; re-apply before reset
            # so the working tree matches what is configured now.
            git("sparse-checkout", "set", *paths, cwd=repo)
            git("fetch", "--no-tags", "origin", ref, cwd=repo)
            changed = changed_paths(repo, prev.get("sha"), "FETCH_HEAD")
            git("reset", "--hard", "FETCH_HEAD", cwd=repo)
            print(f"  updated {(prev.get('sha') or '')[:8]} -> {sha[:8]}")
            for c in changed:
                print(f"    {c}")

        entry = {
            "url": url, "ref": ref, "sha": sha, "trust": r.get("trust", "untrusted"),
            "private": bool(r.get("private")), "synced_at": time.time(),
            "checked_at": time.time(), "changed": changed,
        }

        if entry["trust"] == "trusted":
            entry.update(quarantined=False, findings=[], scanned_at=time.time())
            print("  trusted remote: scan skipped")
        else:
            findings = scan_remote(r, repo)
            blockers = blocking(findings)
            entry.update(quarantined=bool(blockers), findings=findings,
                         scanned_at=time.time())
            if blockers:
                any_flagged = True
                print(f"  QUARANTINED: {len(blockers)} blocking finding(s), not indexed")
                for f in blockers[:5]:
                    print(f"    {f['check']}  {f['file']}:{f['line']}")
                    print(f"      {f['excerpt']}")
                if len(blockers) > 5:
                    print(f"    ... {len(blockers) - 5} more (memory-federate.py scan)")
            elif findings:
                print(f"  scan clean ({len(findings)} notice(s), not blocking)")
            else:
                print("  scan clean")

        s[tag] = entry
        save_state(s)

    save_state(s)
    if any_flagged:
        print("\nOne or more remotes are quarantined and will NOT be indexed.")
        print("Review the findings, then either drop the remote, add the path to")
        print("its \"allow\" list, or run: memory-federate.py release <tag>")
    return 0


def do_scan(args):
    with sync_lock() as acquired:
        if not acquired:
            print("a sync is holding the lock; skipping this scan")
            return 0
        return _scan(args)


def _scan(args):
    s = state()
    flagged = 0
    for r in remotes(args.only):
        tag = r["tag"]
        repo = MIRRORS / tag
        if not repo.exists():
            print(f"{tag}: not mirrored yet (run sync)")
            continue
        if r.get("trust") == "trusted":
            print(f"{tag}: trusted, skipped")
            continue
        findings = scan_remote(r, repo)
        blockers = blocking(findings)
        entry = s.setdefault(tag, {})
        entry.update(findings=findings, quarantined=bool(blockers), scanned_at=time.time())
        if blockers:
            flagged += 1
            print(f"\n{tag}: QUARANTINED, {len(blockers)} blocking finding(s)")
        elif findings:
            print(f"\n{tag}: clean, {len(findings)} notice(s)")
        else:
            print(f"{tag}: clean")
        for f in findings:
            sev = "" if f.get("severity") == "block" else " (notice)"
            print(f"  {f['check']}{sev}  {tag}/{f['file']}:{f['line']}")
            print(f"    {f['excerpt']}")
    save_state(s)
    if flagged and args.strict:
        return 1
    return 0


def do_release(args):
    """Clear a quarantine after a human has read the findings.

    Deliberately manual and per-remote. An automatic release, or a global one,
    would turn the fail-closed default into a formality.
    """
    s = state()
    entry = s.get(args.tag)
    if not entry:
        print(f"no such mirrored remote: {args.tag}", file=sys.stderr)
        return 1
    if not entry.get("quarantined"):
        print(f"{args.tag} is not quarantined")
        return 0
    entry["quarantined"] = False
    entry["released_at"] = time.time()
    entry["released_sha"] = entry.get("sha")
    save_state(s)
    print(f"{args.tag} released for indexing at {(entry.get('sha') or '')[:8]}.")
    print("It will quarantine again on the next upstream change that trips the scan.")
    return 0


def do_status(args):
    s = state()
    if args.json:
        print(json.dumps(s, indent=2, sort_keys=True))
        return 0
    cfg_tags = [r["tag"] for r in remotes()]
    if not cfg_tags:
        print("No remotes configured. Add a \"remotes\" array to memory-tools.json.")
        return 0
    print(f"\nmirrors: {MIRRORS}\n")
    for tag in cfg_tags:
        e = s.get(tag)
        if not e:
            print(f"  {tag:<16} not mirrored yet (run sync)")
            continue
        age = time.time() - e.get("synced_at", 0)
        age_s = f"{age/3600:.0f}h ago" if age > 3600 else f"{age/60:.0f}m ago"
        marks = [e.get("trust", "untrusted")]
        if e.get("private"):
            marks.append("private")
        if e.get("quarantined"):
            marks.append("QUARANTINED")
        n = len(e.get("findings", []))
        print(f"  {tag:<16} {(e.get('sha') or '')[:8]}  {e.get('ref','?'):<10} "
              f"synced {age_s:<9} [{', '.join(marks)}]" + (f" {n} finding(s)" if n else ""))
    print()
    if any(s.get(t, {}).get("quarantined") for t in cfg_tags):
        print("Quarantined remotes are excluded from the index until released.")
        print("  memory-federate.py scan          see why")
        print("  memory-federate.py release <tag> accept and index anyway\n")
    return 0


def main():
    ap = argparse.ArgumentParser(
        prog="memory-federate.py",
        description="Mirror prose from other repos into your memory network, safely.")
    sub = ap.add_subparsers(dest="cmd")

    p = sub.add_parser("sync", help="clone or fast-forward every configured remote")
    p.add_argument("--only", help="one remote tag")
    p.add_argument("--force", action="store_true", help="re-fetch even if the sha is unchanged")
    p.set_defaults(fn=do_sync)

    p = sub.add_parser("scan", help="re-run the safety scan over the mirrors")
    p.add_argument("--only", help="one remote tag")
    p.add_argument("--strict", action="store_true", help="exit 1 if anything is flagged")
    p.set_defaults(fn=do_scan)

    p = sub.add_parser("status", help="what is mirrored and what state it is in")
    p.add_argument("--json", action="store_true")
    p.set_defaults(fn=do_status)

    p = sub.add_parser("release", help="clear a quarantine you have reviewed")
    p.add_argument("tag")
    p.set_defaults(fn=do_release)

    a = ap.parse_args()
    if not getattr(a, "fn", None):
        ap.print_help()
        return 0
    try:
        return a.fn(a)
    except GitError as e:
        print(f"\ngit error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
