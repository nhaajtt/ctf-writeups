// Rebuilds the write-up index in README.md from the header of every file under writeups/.
import { readFileSync, writeFileSync, readdirSync, statSync } from 'node:fs';
import { join, relative, sep } from 'node:path';

const ROOT = new URL('..', import.meta.url).pathname.replace(/^\/([A-Za-z]:)/, '$1');
const START = '<!-- index:start -->';
const END = '<!-- index:end -->';

function walk(dir) {
  const out = [];
  for (const name of readdirSync(dir)) {
    const p = join(dir, name);
    if (statSync(p).isDirectory()) out.push(...walk(p));
    else if (name.endsWith('.md')) out.push(p);
  }
  return out;
}

function header(text) {
  const m = text.match(/^---\r?\n([\s\S]*?)\r?\n---/);
  const meta = {};
  if (!m) return meta;
  for (const line of m[1].split(/\r?\n/)) {
    const i = line.indexOf(':');
    if (i > 0) meta[line.slice(0, i).trim()] = line.slice(i + 1).trim();
  }
  return meta;
}

const esc = (s) => String(s || '').replace(/\|/g, '\\|');

const rows = walk(join(ROOT, 'writeups'))
  .map((file) => ({ file, meta: header(readFileSync(file, 'utf8')) }))
  .filter((r) => r.meta.title)
  .sort((a, b) => String(b.meta.date).localeCompare(String(a.meta.date)))
  .map(({ file, meta }) => {
    const link = relative(ROOT, file).split(sep).join('/');
    return `| ${esc(meta.date)} | ${esc(meta.event)} | [${esc(meta.title)}](${link}) | ${esc(meta.category)} |`;
  });

const table = rows.length
  ? ['| Date | Event | Challenge | Category |', '|---|---|---|---|', ...rows].join('\n')
  : 'No write-ups yet.';

const readmePath = join(ROOT, 'README.md');
const readme = readFileSync(readmePath, 'utf8');
const a = readme.indexOf(START);
const b = readme.indexOf(END);
if (a === -1 || b === -1) {
  console.error('Index markers not found in README.md');
  process.exit(1);
}
const next = `${readme.slice(0, a + START.length)}\n${table}\n${readme.slice(b)}`;
if (next !== readme) writeFileSync(readmePath, next);
console.log(`Indexed ${rows.length} write-up${rows.length === 1 ? '' : 's'}.`);
