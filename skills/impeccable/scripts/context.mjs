/**
 * Context loader: prints PRODUCT.md (and DESIGN.md if present) as one
 * markdown block on stdout. Reports missing product context without imposing
 * setup; DESIGN.md remains usable on its own. Discovery is read-only and local.
 * Plugin refresh belongs to the marketplace release workflow.
 *
 * Path resolution (first match wins):
 *   1. cwd, if PRODUCT.md or DESIGN.md is there
 *   2. .agents/context/ then docs/
 *   3. $IMPECCABLE_CONTEXT_DIR (absolute or cwd-relative) — power-user
 *      escape hatch, only consulted when defaults are empty
 *   4. cwd as a "nothing found" default
 *
 * `resolveContextDir()` and `loadContext()` are also exported for the
 * server-side scripts (live.mjs, live-server.mjs) that need the structured
 * shape rather than the markdown block.
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const PRODUCT_NAMES = ['PRODUCT.md', 'Product.md', 'product.md'];
const DESIGN_NAMES = ['DESIGN.md', 'Design.md', 'design.md'];
const FALLBACK_DIRS = ['.agents/context', 'docs'];

export function resolveContextDir(cwd = process.cwd()) {
  if (firstExisting(cwd, [...PRODUCT_NAMES, ...DESIGN_NAMES])) {
    return cwd;
  }
  for (const rel of FALLBACK_DIRS) {
    const candidate = path.resolve(cwd, rel);
    if (firstExisting(candidate, [...PRODUCT_NAMES, ...DESIGN_NAMES])) {
      return candidate;
    }
  }
  const envDir = process.env.IMPECCABLE_CONTEXT_DIR;
  if (envDir && envDir.trim()) {
    const trimmed = envDir.trim();
    return path.isAbsolute(trimmed) ? trimmed : path.resolve(cwd, trimmed);
  }
  return cwd;
}

export function loadContext(cwd = process.cwd()) {
  const contextDir = resolveContextDir(cwd);
  const productPath = firstExisting(contextDir, PRODUCT_NAMES);
  const designPath = firstExisting(contextDir, DESIGN_NAMES);
  const product = productPath ? safeRead(productPath) : null;
  const design = designPath ? safeRead(designPath) : null;
  return {
    hasProduct: !!product,
    product,
    productPath: productPath ? path.relative(cwd, productPath) : null,
    hasDesign: !!design,
    design,
    designPath: designPath ? path.relative(cwd, designPath) : null,
    contextDir,
  };
}

function firstExisting(dir, names) {
  for (const name of names) {
    const abs = path.join(dir, name);
    if (fs.existsSync(abs)) return abs;
  }
  return null;
}

function safeRead(p) {
  try {
    return fs.readFileSync(p, 'utf-8');
  } catch {
    return null;
  }
}

/**
 * Pull the register (`brand` or `product`) out of PRODUCT.md by looking
 * for a `## Register` section and reading the first non-empty line that
 * follows it. Returns null when the file is legacy / register-less.
 */
export function extractRegister(product) {
  if (!product) return null;
  const lines = product.split('\n');
  for (let i = 0; i < lines.length; i++) {
    if (/^##\s+Register\b/i.test(lines[i].trim())) {
      for (let j = i + 1; j < lines.length; j++) {
        const next = lines[j].trim();
        if (!next) continue;
        const word = next.toLowerCase();
        if (word === 'brand' || word === 'product') return word;
        return null;
      }
    }
  }
  return null;
}

function cli() {
  const ctx = loadContext(process.cwd());
  const parts = [];
  if (ctx.hasProduct) {
    parts.push(`# PRODUCT.md\n\n${ctx.product.trim()}`);
  } else {
    parts.push('NO_PRODUCT_MD: No PRODUCT.md found. Use the task brief and existing project evidence; run init only when project-context setup is requested.');
  }
  if (ctx.hasDesign) {
    parts.push(`# DESIGN.md\n\n${ctx.design.trim()}`);
  }
  const register = extractRegister(ctx.product);
  if (register) parts.push(`REGISTER: ${register}`);
  process.stdout.write(parts.join('\n\n---\n\n') + '\n');
}

// Run cli() only when this module is the entry point. Compare realpaths
// rather than endsWith(): a loose suffix match also fires for unrelated
// scripts like `load-context.mjs`, and realpath tolerates symlinked
// invocation (the test harness symlinks the skill dir).
function invokedAsScript() {
  const arg = process.argv[1];
  if (!arg) return false;
  try {
    return fs.realpathSync(arg) === fs.realpathSync(fileURLToPath(import.meta.url));
  } catch {
    return false;
  }
}

if (invokedAsScript()) {
  cli();
}
