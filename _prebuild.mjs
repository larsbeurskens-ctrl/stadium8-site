// Vercel build step: pull saved content from Upstash KV into content.json, then build.py renders from it.
// Falls back silently to the git-committed content.json if KV is empty/unconfigured. Never fails the build.
import fs from 'node:fs';
const KV_URL = process.env.KV_REST_API_URL || process.env.UPSTASH_REDIS_REST_URL || '';
const KV_TOKEN = process.env.KV_REST_API_TOKEN || process.env.UPSTASH_REDIS_REST_TOKEN || '';
const SITE_KEY = process.env.SITE_KEY || 'stadium8';
const KEY = `${SITE_KEY}:content`;

async function main() {
  if (!KV_URL || !KV_TOKEN) { console.log('[prebuild] KV not configured - using git content.json'); return; }
  try {
    const r = await fetch(`${KV_URL}/get/${encodeURIComponent(KEY)}`, { headers: { Authorization: `Bearer ${KV_TOKEN}` } });
    if (!r.ok) { console.log(`[prebuild] KV ${r.status} - using git content.json`); return; }
    const data = await r.json();
    if (!data || data.result == null) { console.log('[prebuild] no KV content yet - using git content.json'); return; }
    const parsed = JSON.parse(data.result);
    if (!parsed || typeof parsed !== 'object' || parsed.version == null) { console.log('[prebuild] KV content invalid - using git content.json'); return; }
    fs.writeFileSync('content.json', JSON.stringify(parsed, null, 2), 'utf8');
    console.log('[prebuild] wrote content.json from KV');
  } catch (e) {
    console.log('[prebuild] error, using git content.json:', e.message);
  }
}
main();
