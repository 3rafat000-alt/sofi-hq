#!/usr/bin/env node
// port-agents.mjs — porting SOFI agents from opencode to Kilo
// The sole source: .opencode/agent/ ← generated: .kilo/agent/
// Rule: drop the model: line (identifiers tied to the opencode environment) — the rest ports verbatim.
// Fails deliberately if the count does not match the official registry registry.yaml (106).
import { readdirSync, readFileSync, writeFileSync, mkdirSync, rmSync } from 'node:fs';
import { join } from 'node:path';

const SRC = '.opencode/agent';
const DST = '.kilo/agent';
// The guard reads the count from the official registry meta at runtime (INT-GTW-024 + brd-ceo verdict ج-4) — no hard-coded constant
const registryText = readFileSync('hq/core/nexus/registry.yaml', 'utf8');
const metaAgents = registryText.match(/^\s*total_agents:\s*(\d+)\s*$/m);
const EXPECTED = metaAgents ? Number(metaAgents[1]) : (() => { throw new Error('registry.yaml: meta.total_agents not found'); })();

let files;
try {
  files = readdirSync(SRC).filter(f => f.endsWith('.md'));
} catch {
  console.error(`FAIL: source directory missing: ${SRC}`);
  process.exit(1);
}

if (files.length !== EXPECTED) {
  console.error(`ABORT: ${SRC} has ${files.length} agents, registry expects ${EXPECTED}.`);
  console.error('Fix the gap first (a missing or extra agent), then run again.');
  process.exit(1);
}

rmSync(DST, { recursive: true, force: true });
mkdirSync(DST, { recursive: true });

let ok = 0, skipped = [];
for (const f of files) {
  const raw = readFileSync(join(SRC, f), 'utf8');
  const m = raw.match(/^---\n([\s\S]*?)\n---\n?([\s\S]*)$/);
  if (!m) { skipped.push(f); continue; }
  const fm = m[1].split('\n').filter(l => !/^model:/i.test(l)).join('\n');
  const name = /^name:\s*(.+)$/im.exec(fm)?.[1]?.trim().replace(/\s+/g, '-');
  const dstName = (!name || name === f.replace(/\.md$/, '')) ? f : `${name}.md`;
  writeFileSync(join(DST, dstName), `---\n${fm}\n---\n${m[2]}`);
  ok++;
}

console.log(`OK: ${ok}/${EXPECTED} agents -> ${DST}`);
if (skipped.length) {
  console.error(`SKIPPED (no frontmatter): ${skipped.join(', ')}`);
  process.exit(1);
}
