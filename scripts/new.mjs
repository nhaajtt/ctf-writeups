// Creates writeups/<event>/<challenge>.md from TEMPLATE.md.
//   node scripts/new.mjs "<event>" "<challenge>" [category]
import { readFileSync, writeFileSync, mkdirSync, existsSync } from 'node:fs';
import { join } from 'node:path';

const ROOT = new URL('..', import.meta.url).pathname.replace(/^\/([A-Za-z]:)/, '$1');
const [event, challenge, category = 'rev'] = process.argv.slice(2);
if (!event || !challenge) {
  console.error('Usage: node scripts/new.mjs "<event>" "<challenge>" [category]');
  process.exit(1);
}

const slug = (s) => s.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
const dir = join(ROOT, 'writeups', slug(event));
const file = join(dir, `${slug(challenge)}.md`);
if (existsSync(file)) {
  console.error(`${file} already exists.`);
  process.exit(1);
}

const today = new Date().toISOString().slice(0, 10);
const text = readFileSync(join(ROOT, 'TEMPLATE.md'), 'utf8')
  .replace('title: Challenge name', `title: ${challenge}`)
  .replace('event: Event name and year', `event: ${event}`)
  .replace('category: rev', `category: ${category}`)
  .replace('date: YYYY-MM-DD', `date: ${today}`);

mkdirSync(dir, { recursive: true });
writeFileSync(file, text);
console.log(`Created ${file}`);
