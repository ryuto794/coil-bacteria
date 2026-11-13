// Release builds (v29.5). The game itself is ../index.html and runs as it is; this only makes the copies that are handed out.
//   node build.mjs demo            -> ../dist/demo/index.html   (the web demo: stage 1 and the basic skins)
//   node build.mjs full            -> ../dist/full/index.html   (everything; for the Steam build)
//   add --keep-debug               -> ../dist/<edition>-debug/  (keeps window.__g, for checking the build with the tests)
// What it does:
//   1. demo: cuts out every //#FULL ... //#/FULL block (the full game's stages, creatures, drawings and skins) and switches on //#DEMO lines
//      (stand-ins: the full game's stage names, shown as "in the full game"). What is not in the file cannot be lifted from it.
//   2. cuts out //#DEV ... //#/DEV (window.__g, the hooks the tests drive the game with), unless --keep-debug
//   3. writes EDITION into the code
//   4. minifies the script with terser: comments gone, local names shortened, one long line
// The site lock (SITE_HOSTS in index.html) stays in. Publishing somewhere new means adding its host there first.
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { execSync } from 'node:child_process';
import { minify } from 'terser';

const ed = process.argv[2] || 'demo', keep = process.argv.includes('--keep-debug');
if (!['demo', 'full'].includes(ed)) { console.error('edition must be demo or full'); process.exit(1); }
const root = new URL('../', import.meta.url);
let src = readFileSync(new URL('index.html', root), 'utf8');

const cut = (s, tag) => {
  const re = new RegExp(`^[ \\t]*//#${tag}\\b[^\\n]*\\n[\\s\\S]*?^[ \\t]*//#/${tag}\\b[^\\n]*\\n`, 'gm');
  const n = (s.match(re) || []).length; return [s.replace(re, ''), n];
};
let n;
if (ed === 'demo') { [src, n] = cut(src, 'FULL'); console.log(`cut ${n} full-game blocks`); src = src.replace(/^([ \t]*)\/\/#DEMO /gm, '$1'); }
if (!keep) { [src, n] = cut(src, 'DEV'); console.log(`cut ${n} debug blocks`); }
for (const tag of ['FULL', 'DEV']) if (new RegExp(`//#/?${tag}\\b`).test(src) && (tag === 'DEV' ? !keep : ed === 'demo')) { console.error(`unmatched //#${tag} marker left`); process.exit(1); }
if (!src.includes("EDITION='full'")) { console.error("EDITION='full' not found"); process.exit(1); }
src = src.replace("EDITION='full'", `EDITION='${ed}'`);

const m = src.match(/<script>([\s\S]*)<\/script>/);
if (!m) { console.error('no <script> found'); process.exit(1); }
const out = await minify(m[1], { ecma: 2020, compress: { passes: 2 }, mangle: true, format: { comments: false } });
let head = src.slice(0, m.index), tail = src.slice(m.index + m[0].length);
head = head.replace(/\/\*[\s\S]*?\*\//g, '').replace(/\n\s*/g, '');
tail = tail.replace(/\n\s*/g, '');
let rev = 'local'; try { rev = execSync('git rev-parse --short HEAD', { cwd: root }).toString().trim(); } catch (e) {}
const stamp = `${ed}-${new Date().toISOString().slice(0, 10)}-${rev}`;
head = head.replace('<meta charset="utf-8">', `<meta charset="utf-8"><meta name="build" content="${stamp}">`);
const html = head + '<script>' + out.code + '</script>' + tail;

const dir = new URL(`dist/${ed}${keep ? '-debug' : ''}/`, root);
mkdirSync(dir, { recursive: true });
writeFileSync(new URL('index.html', dir), html);
console.log(`wrote dist/${ed}${keep ? '-debug' : ''}/index.html  ${(html.length / 1024).toFixed(0)} KB (source ${(readFileSync(new URL('index.html', root)).length / 1024).toFixed(0)} KB)  build ${stamp}`);
