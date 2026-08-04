// Unit tests for the setup wizard package. Zero dependencies: node --test.
// Run: node --test tests/
//
// These test the CONTRACTS the wizard's documents must hold (the two-exits
// rule from memory-system ADR 0001, the machine-question-first rule, package
// integrity) and the scaffold validator itself against fixtures.

import { test } from 'node:test'
import assert from 'node:assert/strict'
import { execFileSync } from 'node:child_process'
import { mkdtempSync, mkdirSync, writeFileSync, readFileSync, rmSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { join, dirname, resolve } from 'node:path'
import { fileURLToPath } from 'node:url'

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..')
const read = (p) => readFileSync(join(ROOT, p), 'utf8')

const PACKAGE_FILES = [
  'START-HERE.md',
  'wizard/interview.md',
  'wizard/scaffold.md',
  'wizard/platforms.md',
  'wizard/entries/from-buildwiththememory.md',
  'scripts/validate-scaffold.mjs',
]

// The direct-install surface: everything a person handed the repo will read.
// Per ADR 0001 (one artifact, two exits) none of it may mention the
// newsletter; only the buildwiththememory.com entry file may, and only after
// the wizard has finished.
const DIRECT_SURFACE = ['START-HERE.md', 'wizard/interview.md', 'wizard/scaffold.md', 'wizard/platforms.md']

test('package integrity: every wizard file exists and is non-trivial', () => {
  for (const f of PACKAGE_FILES) {
    const body = read(f)
    assert.ok(body.length > 200, `${f} exists and has real content`)
  }
})

test('package integrity: every relative markdown link resolves', () => {
  for (const f of PACKAGE_FILES.filter((p) => p.endsWith('.md'))) {
    const body = read(f)
    for (const [, target] of body.matchAll(/\]\(([^)#\s]+)(?:#[^)]*)?\)/g)) {
      if (/^[a-z]+:/i.test(target)) continue // absolute URL
      const full = resolve(join(ROOT, dirname(f)), target)
      assert.doesNotThrow(() => readFileSync(full), `${f} links to ${target}, which must exist`)
    }
  }
})

test('no em or en dashes anywhere in the wizard package', () => {
  for (const f of PACKAGE_FILES) {
    assert.ok(!/[\u2013\u2014]/.test(read(f)), `${f} contains no em/en dashes`)
  }
})

test('the machine question is Question 0 and comes before every other question', () => {
  const body = read('wizard/interview.md')
  const q0 = body.indexOf('## Question 0')
  assert.ok(q0 !== -1, 'interview has a Question 0')
  assert.match(body.slice(q0, q0 + 200), /whose machine/i, 'Question 0 is the machine question')
  for (const [m] of body.matchAll(/## Question [1-9]/g)) {
    assert.ok(body.indexOf(m) > q0, `${m} comes after Question 0`)
  }
  const employerBlock = body.slice(q0, body.indexOf('## Question 1'))
  assert.match(employerBlock, /standalone mode/i, 'employer answer routes to standalone mode')
  assert.match(employerBlock, /safe\s+direction/i, 'the shrug default is the employer treatment')
})

test('two exits: the direct-install surface never mentions the newsletter', () => {
  for (const f of DIRECT_SURFACE) {
    assert.ok(!/newsletter|subscribe|mailing/i.test(read(f)), `${f} is clean of opt-in language`)
  }
})

test('two exits: the BWAM entry appends the offer strictly after the wizard finishes', () => {
  const body = read('wizard/entries/from-buildwiththememory.md')
  assert.match(body, /After the wizard has finished/, 'offer is gated on completion')
  assert.match(body, /Never repeat the offer/, 'offer is once, ever')
  assert.match(body, /never gate anything on it/i, 'offer is not load-bearing')
  const runsInterview = body.indexOf('interview.md')
  const offer = body.search(/newsletter/i)
  assert.ok(runsInterview !== -1 && offer > runsInterview, 'the interview instruction precedes the offer')
})

test('standalone rule text in scaffold.md matches what the validator checks for', () => {
  const scaffold = read('wizard/scaffold.md')
  const validator = read('scripts/validate-scaffold.mjs')
  const rule = 'never add memory files, hooks, or'
  assert.match(scaffold.toLowerCase(), new RegExp(rule), 'scaffold.md carries the employer rule verbatim')
  assert.ok(validator.toLowerCase().includes(rule), 'validator greps for the same phrase')
})

// ---- validator behavior against fixtures ------------------------------------

const VALIDATOR = join(ROOT, 'scripts', 'validate-scaffold.mjs')
const runValidator = (args) => {
  try {
    execFileSync(process.execPath, [VALIDATOR, ...args], { encoding: 'utf8' })
    return 0
  } catch (e) {
    return e.status ?? 1
  }
}

function goodScaffold(home, { standalone = false } = {}) {
  const claude = join(home, '.claude')
  mkdirSync(join(claude, 'memory', 'handoffs'), { recursive: true })
  mkdirSync(join(claude, 'memory', 'ideas'), { recursive: true })
  writeFileSync(join(claude, 'CLAUDE.md'), `# Jordan

Solo web developer. Ships small tools.

## Rules
- Keep replies short.
${standalone ? `- This machine belongs to my employer/client. Keep all personal memory
  machinery inside my own user folder. Never add memory files, hooks, or
  agent config to a repo I do not personally own.\n` : ''}
## Memory
- My memory lives in ~/.claude/memory. Read MEMORY.md there at the start of a
  session when context would help; it is the index.

## One-word habits
- If I say just "handoff": write a dated file in ~/.claude/memory/handoffs/.
- If I say "pick up": read the newest handoff and continue.
- If I start a message with "idea": record it in ~/.claude/memory/ideas/.
`)
  writeFileSync(join(claude, 'memory', 'MEMORY.md'), '# Memory index\n- [focus](focus.md)\n')
  writeFileSync(join(claude, 'memory', 'focus.md'), '# Focus\n2026-07-28: shipping the widget.\n')
  writeFileSync(join(claude, 'memory', 'ideas', 'INDEX.md'), '# Ideas\n')
}

test('validator passes a correct scaffold', () => {
  const home = mkdtempSync(join(tmpdir(), 'wiz-good-'))
  goodScaffold(home)
  assert.equal(runValidator([home]), 0)
  rmSync(home, { recursive: true, force: true })
})

test('validator passes a correct standalone scaffold', () => {
  const home = mkdtempSync(join(tmpdir(), 'wiz-standalone-'))
  goodScaffold(home, { standalone: true })
  assert.equal(runValidator([home, '--standalone']), 0)
  rmSync(home, { recursive: true, force: true })
})

test('validator fails when the index is missing', () => {
  const home = mkdtempSync(join(tmpdir(), 'wiz-noindex-'))
  goodScaffold(home)
  rmSync(join(home, '.claude', 'memory', 'MEMORY.md'))
  assert.equal(runValidator([home]), 1)
  rmSync(home, { recursive: true, force: true })
})

test('validator fails a standalone run missing the employer rule', () => {
  const home = mkdtempSync(join(tmpdir(), 'wiz-norule-'))
  goodScaffold(home, { standalone: false })
  assert.equal(runValidator([home, '--standalone']), 1)
  rmSync(home, { recursive: true, force: true })
})

test('validator fails when the personal file smuggles in the newsletter', () => {
  const home = mkdtempSync(join(tmpdir(), 'wiz-smuggle-'))
  goodScaffold(home)
  const p = join(home, '.claude', 'CLAUDE.md')
  writeFileSync(p, readFileSync(p, 'utf8') + '\n- Subscribe to the newsletter!\n')
  assert.equal(runValidator([home]), 1)
  rmSync(home, { recursive: true, force: true })
})

test('validator respects reduced habit selection', () => {
  const home = mkdtempSync(join(tmpdir(), 'wiz-habits-'))
  const claude = join(home, '.claude')
  mkdirSync(join(claude, 'memory'), { recursive: true })
  writeFileSync(join(claude, 'CLAUDE.md'), `# Sam

Builds data pipelines.

## Rules
- Ask before deleting.

## Memory
- My memory lives in ~/.claude/memory. MEMORY.md is the index.

## One-word habits
- If I start a message with "idea": record it in ~/.claude/memory/ideas/.
`)
  writeFileSync(join(claude, 'memory', 'MEMORY.md'), '# Memory index\n- [focus](focus.md)\n')
  writeFileSync(join(claude, 'memory', 'focus.md'), '2026-07-28: quarter close.\n')
  mkdirSync(join(claude, 'memory', 'ideas'), { recursive: true })
  writeFileSync(join(claude, 'memory', 'ideas', 'INDEX.md'), '# Ideas\n')
  assert.equal(runValidator([home, '--habits', 'idea']), 0, 'idea-only scaffold passes when asked for idea only')
  assert.equal(runValidator([home, '--habits', 'handoff,idea']), 1, 'same scaffold fails if handoff was expected')
  rmSync(home, { recursive: true, force: true })
})
