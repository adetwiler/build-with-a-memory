# CONTEXT - glossary for this repo

The terms that mean something specific in "Build With a Memory." One line each. Read this first so the words below carry their intended meaning everywhere else.

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
