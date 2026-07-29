#!/usr/bin/env node
// validate-scaffold.mjs <home-dir> [--agent claude-code|cursor|other] [--standalone] [--habits handoff,idea]
//
// Checks that a wizard run produced a correct personal layer in <home-dir>.
// Used by tests/wizard.test.mjs against fixtures and by hand against a real
// (or sandboxed) home folder after an end-to-end run. Exit 0 = pass.

import { existsSync, readFileSync, statSync } from 'node:fs'
import { join } from 'node:path'

const args = process.argv.slice(2)
const home = args.find((a) => !a.startsWith('--'))
if (!home) {
  console.error('usage: validate-scaffold.mjs <home-dir> [--agent name] [--standalone] [--habits list]')
  process.exit(2)
}
const opt = (name) => {
  const i = args.indexOf(`--${name}`)
  return i === -1 ? null : (args[i + 1] && !args[i + 1].startsWith('--') ? args[i + 1] : true)
}
const agent = opt('agent') || 'claude-code'
const standalone = args.includes('--standalone')
const habits = (typeof opt('habits') === 'string' ? opt('habits') : 'handoff,pickup,idea')
  .split(',').map((s) => s.trim()).filter(Boolean)

const LAYOUT = {
  'claude-code': { personal: '.claude/CLAUDE.md', memory: '.claude/memory' },
  cursor: { personal: '.cursor/rules/personal.md', memory: '.cursor/memory' },
  other: { personal: 'agent-memory/PERSONAL.md', memory: 'agent-memory/memory' },
}
const layout = LAYOUT[agent]
if (!layout) {
  console.error(`unknown agent "${agent}" (expected: ${Object.keys(LAYOUT).join(', ')})`)
  process.exit(2)
}

const failures = []
const pass = (msg) => console.log(`  ok    ${msg}`)
const fail = (msg) => { failures.push(msg); console.log(`  FAIL  ${msg}`) }
const check = (cond, msg) => (cond ? pass(msg) : fail(msg))

const personalPath = join(home, layout.personal)
const memoryDir = join(home, layout.memory)

console.log(`validate-scaffold: ${home} (agent=${agent}${standalone ? ', standalone' : ''}, habits=${habits.join('+') || 'none'})`)

check(existsSync(personalPath), `personal file exists (${layout.personal})`)
const personal = existsSync(personalPath) ? readFileSync(personalPath, 'utf8') : ''

if (personal) {
  check(personal.length <= 6000, `personal file reads in about a minute (${personal.length} chars <= 6000)`)
  check(/^## Rules$/m.test(personal), 'personal file has a "## Rules" section')
  check(/^## Memory$/m.test(personal), 'personal file has a "## Memory" section')
  check(/MEMORY\.md/.test(personal), 'personal file points at the MEMORY.md index')
  if (habits.length) check(/^## One-word habits$/m.test(personal), 'personal file has the "## One-word habits" section')
  if (habits.includes('handoff')) check(/"handoff"/.test(personal), 'handoff habit block present')
  if (habits.includes('pickup')) check(/"pick up"/.test(personal), 'pick up habit block present')
  if (habits.includes('idea')) check(/"idea"/.test(personal), 'idea habit block present')
  const mentionsList = /newsletter|subscribe|mailing/i.test(personal)
  check(!mentionsList, 'personal file never mentions a newsletter or mailing list')
  if (standalone) {
    check(/employer|client/i.test(personal) && /never add memory files, hooks, or/i.test(personal),
      'standalone mode: the employer-machine rule is present')
  }
}

check(existsSync(memoryDir) && statSync(memoryDir).isDirectory(), `memory folder exists (${layout.memory})`)
const indexPath = join(memoryDir, 'MEMORY.md')
check(existsSync(indexPath), 'MEMORY.md index exists')
if (existsSync(indexPath)) {
  const idx = readFileSync(indexPath, 'utf8')
  check(idx.trim().length > 0, 'MEMORY.md is not empty')
  check(/focus\.md/.test(idx), 'MEMORY.md points to focus.md')
}
const focusPath = join(memoryDir, 'focus.md')
check(existsSync(focusPath), 'focus.md exists (seeded from the interview)')
if (existsSync(focusPath)) {
  check(/\d{4}-\d{2}-\d{2}/.test(readFileSync(focusPath, 'utf8')), 'focus.md is dated')
}
if (habits.includes('handoff')) {
  check(existsSync(join(memoryDir, 'handoffs')), 'handoffs/ folder exists')
}
if (habits.includes('idea')) {
  check(existsSync(join(memoryDir, 'ideas', 'INDEX.md')), 'ideas/INDEX.md exists')
}

if (failures.length) {
  console.log(`\n${failures.length} check(s) FAILED`)
  process.exit(1)
}
console.log('\nall checks passed')
