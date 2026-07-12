# Findings: the AI-agent memory landscape, mid-2026

**Question.** This method (committed markdown memory networks plus a self-improving
loop) is not the only answer people are building to agent amnesia. What else is out
there, where does this sit, and which of its choices are backed by more than
preference?

**Scope.** Public facts and links only. This is the prior art the method sits next
to, gathered so the founding decisions (see `docs/adr/0001-method-repo-decisions.md`)
can be made with the field in view instead of in a vacuum.

## The conversation this sits in: context engineering

By 2026 the framing had shifted from "prompt engineering" to "context
engineering": the idea that the hard part of building with LLMs is deciding what
goes into the limited context window and what stays out, not wording a single
prompt. That reframing is the whole reason a committed, indexed memory matters. If
context is the scarce resource, then a repo that lets an agent load the exact slice
it needs (and skip the rest) is managing the scarce resource directly.

- Anthropic, "Effective context engineering for AI agents":
  https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- The term was popularized across 2025 by, among others, Andrej Karpathy and
  Simon Willison in public writing. Simon Willison's notes are a running public
  record: https://simonwillison.net/

## The file-based memory approaches (closest neighbors)

These share the core instinct of this method: memory as files the agent reads,
not a service it calls.

- **Cline Memory Bank.** The Cline coding agent documents a "Memory Bank": a set
  of markdown files in the project that the agent reads at the start of a session
  to recover context, because the agent's own memory resets between sessions. Same
  diagnosis (session amnesia), same medicine (committed markdown).
  https://docs.cline.bot/prompting/cline-memory-bank
- **GitHub Spec Kit.** A toolkit for spec-driven development with AI agents: you
  write specs and plans as durable artifacts the agent works from, rather than
  steering purely by chat. Different emphasis (specs and plans over glossary and
  decisions) but the same move of putting the durable intent in the repo.
  https://github.com/github/spec-kit
- **Other repo-memory projects** in the same space (for example projects
  published under names like "ProjectMEM" and "RepoMemory") explore committing an
  agent's working memory into the repository. The space was active and moving in
  2026; treat any single project's specifics as a snapshot.
  <!-- OWNER: confirm exact project names/links before publishing if you want them cited by name -->

**Where this method differs from the neighbors.** Two things. First, the *wide*
network: a personal cross-project layer linked to the repo networks by pointer,
which most repo-only approaches do not address. Second, the *decision-cache*
framing: treating accumulated ADRs as a review-cost cache with an explicit token
economics, rather than as documentation you file and forget.

## The hosted-SaaS contrast (the opposite bet)

A second family answers agent memory as a managed service: your memory lives on
their servers behind an API. This is the bet this method deliberately does not
make (see the "anti-product" stance in the README). Naming the contrast is fair,
and these are real, useful tools for people who want that trade.

- **mem0** (open source core plus a hosted platform), a memory layer for AI
  agents/apps: https://github.com/mem0ai/mem0
- **Zep**, a memory service for agent applications:
  https://www.getzep.com/ and https://github.com/getzep
- Other hosted memory layers marketed through 2026 make similar offers.
  <!-- OWNER: confirm current names/links (e.g. "Forgetful") before citing by name -->

The tradeoff is real and worth stating plainly rather than dismissing: a hosted
layer can offer retrieval, ranking, and cross-session recall you do not have to
build. The cost is that your project's memory now lives in someone else's system,
tied to their API and their business. This method chooses ownership and
tool-portability over managed convenience. That is a preference, not a proof, and
the honest version says so.

## The argument for distinct-lens judge panels (from the literature)

Pillar 6 claims that several reviewers with *distinct* lenses beat several
reviewers with the *same* lens, because same-framing judges make correlated
errors. This is not just intuition. Work on LLM-as-judge reliability has
repeatedly found that judges sharing a model or a framing tend to be wrong in the
same direction, so stacking them inflates confidence without adding real coverage,
while deliberately varying the judges de-correlates their errors.

- Survey and critique of LLM-as-a-judge methods (bias, correlation, reliability):
  search arXiv for recent "LLM-as-a-judge" survey work.
  https://arxiv.org/ (venue) <!-- OWNER: pin the specific paper/IDs you want cited (e.g. the multi-judge correlated-error result) before publishing -->
- The practical takeaway is design guidance, not a headline: assign each judge a
  distinct job, run one round, and integrate the verdicts yourself.

## Prior art on structure-as-context (worth reading, cite carefully)

There is a thread of academic and practitioner writing arguing that how you
*organize* a codebase or a knowledge base is itself context an agent consumes:
folder structure as architecture, ordering and placement as signal. It lines up
with this method's "orient by the map, not by grepping." The specific papers move
fast and titles vary.

- arXiv is the venue for the current work here: https://arxiv.org/
  <!-- OWNER: pin the specific papers you referenced (the "mise en place" and
  "folder-structure-as-architecture" pieces) with their real IDs before citing them
  by name; left generic here to avoid citing a wrong identifier. -->

## What this shelf concludes

- The problem (session amnesia) is widely recognized, and file-based memory is a
  mainstream answer, not a fringe one. This method is in good company on the
  diagnosis.
- The differentiators worth leading with are the ones the neighbors do not cover:
  the wide cross-project pointer network, and the decision-cache economics.
- The judge-panel design (distinct lenses, one round) has support in the
  reliability literature and should be presented as a reasoned choice, not folklore.
- The hosted-SaaS contrast is real and should be stated honestly, including its
  genuine upside, rather than strawmanned.
