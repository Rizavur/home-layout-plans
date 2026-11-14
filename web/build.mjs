// Bundles web/src into ../assets/app.js + app.css and writes ../index.html.
//   npm run build        one-off production build
//   npm run dev          rebuild on every change and serve the site on http://localhost:8000
// three.js is not bundled: the page loads it from a CDN through the import map in index.html.
import * as esbuild from 'esbuild';
import { readFileSync, writeFileSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const root = resolve(here, '..');
const watch = process.argv.includes('--watch');
const build = String(Date.now());

const options = {
  entryPoints: [resolve(here, 'src/main.jsx')],
  bundle: true,
  format: 'esm',
  outfile: resolve(root, 'assets/app.js'),
  jsx: 'automatic',
  external: ['three', 'three/addons/*'],
  loader: { '.json': 'json' },
  define: { 'process.env.NODE_ENV': watch ? '"development"' : '"production"', __BUILD__: JSON.stringify(build) },
  minify: !watch,
  sourcemap: true,
  target: ['es2020', 'safari15'],
  logLevel: 'info',
};

// index.html: the source shell with a cache-busting build number on the bundle
writeFileSync(resolve(root, 'index.html'), readFileSync(resolve(here, 'index.html'), 'utf8').replaceAll('__BUILD__', build));

if (watch) {
  const ctx = await esbuild.context(options);
  await ctx.watch();
  const { port } = await ctx.serve({ servedir: root, port: 8000 });
  console.log(`Serving http://localhost:${port}/`);
} else {
  await esbuild.build(options);
}
