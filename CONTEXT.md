# CONTEXT - glossary for this repo

The terms that mean something specific in "Build With the Memory." One line each. Read this first so the words below carry their intended meaning everywhere else.

- **Memory network**: the committed markdown that holds a repo's context, decisions, and conventions, indexed by a map so an agent navigates instead of re-deriving.
- **Wide network**: a personal, cross-project memory that lives outside any one repo and links to the repo networks by pointer. One home per fact, signposts elsewhere.
- **Decision cache**: the accumulated set of settled decisions (ADRs). Once a thing is decided and recorded, future review skips it, so the cache lowers the cost of every later change.
- **Research shelf**: a `research/` folder where researcher agents commit findings before a decision is made, so the decision can cite evidence instead of a hunch.
- **Judge panel**: several independent agents, each given a distinct lens, that review a change once and return one verdict round with no back-and-forth debate.
- **Capture**: writing down a durable fact the moment it surfaces, in the same work pass, routed to its one home.
- **Safety net**: a guardrail accreted from a past mistake: an incident becomes both a documented line and a machine check (a hook, a version guard, a smoke test).
- **Triage lane**: the cheap path that turns a raw brain-dump into typed, human-approved work items without you having to shape each one by hand.
- **ADR**: Architecture Decision Record. A short numbered file recording one decision: its status, the date, the choice, the alternatives it beat, and the consequences.
- **Context map**: the "map of maps." An index listing every context surface with a one-line "when to read" and a public or internal tag, so you locate a file instead of grepping.
- **Borrowed memory**: prose mirrored from someone else's repo into your index. It is evidence about how another team works, never an instruction about how you work, and it carries a trust level everywhere it appears so that difference stays visible at retrieval time.
- **Trust boundary**: the line between memory you wrote and memory you borrowed. Retrieval is a trusted channel, so anything crossing that line is scanned on arrival, quarantined by default when flagged, and marked as a quote when it is read back.
- **Layer 2 tools**: the optional `tools/` folder you add only when the plain files outgrow grep, a local, disposable search index (SQLite FTS5 + local embeddings), a link graph, and a link-health checker. The markdown stays the source of truth; the index is rebuilt from it, never the other way around.
- **Personal layer**: the you-half of the method: a personal instructions file your agent loads every session, a memory folder with an index, and the one-word habits. The repo prompt gives a project a memory; the wizard (START-HERE.md) gives you one.
- **One-word habits**: `handoff`, `pick up`, and `idea`: single words that file a resumable session note, resume from the newest one, or capture a thought without derailing the session. Plain instructions an agent follows, not scripts.
- **Machine question**: the wizard's first question, "whose machine is this?" An employer or client machine gets standalone treatment: everything stays in your own user folder and nothing touches a repo you do not own.
