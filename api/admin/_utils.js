// Shared utilities for the Stadium 8 admin (password auth + KV content store).
// No npm deps — Node built-in crypto + fetch. HS256 JWT session, Upstash KV REST.
import crypto from 'crypto';

const JWT_SECRET     = process.env.JWT_SECRET || '';
const KV_URL         = process.env.KV_REST_API_URL || '';
const KV_TOKEN       = process.env.KV_REST_API_TOKEN || '';
const ADMIN_PASSWORD = process.env.ADMIN_PASSWORD || '';
const SITE_KEY       = process.env.SITE_KEY || 'stadium8';
const DEPLOY_HOOK    = process.env.DEPLOY_HOOK_URL || '';

export const ENV = { JWT_SECRET, KV_URL, KV_TOKEN, ADMIN_PASSWORD, SITE_KEY, DEPLOY_HOOK };
export const CONTENT_KEY = `${SITE_KEY}:content`;
const COOKIE = 'stadium8_session';

// ----- JWT (HS256, base64url) -----
const b64url = (buf) => Buffer.from(buf).toString('base64').replace(/=+$/, '').replace(/\+/g, '-').replace(/\//g, '_');
const b64urlDecode = (s) => Buffer.from(s.replace(/-/g, '+').replace(/_/g, '/'), 'base64');

export function signJwt(payload, ttlSeconds) {
  if (!JWT_SECRET) throw new Error('JWT_SECRET not configured');
  const now = Math.floor(Date.now() / 1000);
  const h = b64url(JSON.stringify({ alg: 'HS256', typ: 'JWT' }));
  const p = b64url(JSON.stringify({ ...payload, iat: now, exp: now + ttlSeconds }));
  const sig = b64url(crypto.createHmac('sha256', JWT_SECRET).update(`${h}.${p}`).digest());
  return `${h}.${p}.${sig}`;
}

export function verifyJwt(token) {
  if (!JWT_SECRET || !token || typeof token !== 'string') return null;
  const parts = token.split('.');
  if (parts.length !== 3) return null;
  const [h, p, sig] = parts;
  const expected = b64url(crypto.createHmac('sha256', JWT_SECRET).update(`${h}.${p}`).digest());
  try {
    if (sig.length !== expected.length || !crypto.timingSafeEqual(Buffer.from(sig), Buffer.from(expected))) return null;
    const payload = JSON.parse(b64urlDecode(p).toString('utf8'));
    if (payload.exp && payload.exp < Math.floor(Date.now() / 1000)) return null;
    return payload;
  } catch { return null; }
}

// ----- Password (constant-time compare via sha256) -----
export function checkPassword(pw) {
  if (!ADMIN_PASSWORD || !pw) return false;
  const a = crypto.createHash('sha256').update(String(pw)).digest();
  const b = crypto.createHash('sha256').update(ADMIN_PASSWORD).digest();
  return crypto.timingSafeEqual(a, b);
}

// ----- Upstash KV REST -----
async function kvFetch(path, init = {}) {
  if (!KV_URL || !KV_TOKEN) throw new Error('KV not configured');
  const res = await fetch(`${KV_URL}${path}`, { ...init, headers: { Authorization: `Bearer ${KV_TOKEN}`, ...(init.headers || {}) } });
  if (!res.ok) throw new Error(`KV ${path} -> ${res.status}`);
  return res.json();
}
export async function kvGet(key) {
  try { const d = await kvFetch(`/get/${encodeURIComponent(key)}`); return d.result ?? null; } catch { return null; }
}
export async function kvSetRaw(key, value) {
  // POST body form so large JSON values are fine
  await kvFetch(`/set/${encodeURIComponent(key)}`, { method: 'POST', headers: { 'Content-Type': 'text/plain' }, body: value });
  return true;
}

// ----- Cookie helpers -----
export function setSessionCookie(res, token, maxAge = 30 * 24 * 3600) {
  res.setHeader('Set-Cookie', `${COOKIE}=${token}; Max-Age=${maxAge}; Path=/; HttpOnly; Secure; SameSite=Lax`);
}
export function clearSessionCookie(res) {
  res.setHeader('Set-Cookie', `${COOKIE}=; Max-Age=0; Path=/; HttpOnly; Secure; SameSite=Lax`);
}
export function readSession(req) {
  const m = (req.headers.cookie || '').match(new RegExp(`${COOKIE}=([^;]+)`));
  return m ? verifyJwt(m[1]) : null;
}
export function requireAuth(req, res) {
  const s = readSession(req);
  if (!s || s.purpose !== 'session') { res.status(401).json({ error: 'Not authenticated' }); return null; }
  setSessionCookie(res, signJwt({ purpose: 'session' }, 30 * 24 * 3600)); // rolling expiry
  return s;
}

// ----- Content + schema (cwd = repo root in Vercel functions) -----
import fs from 'node:fs';
import path from 'node:path';
export function loadSchema() {
  try { return JSON.parse(fs.readFileSync(path.join(process.cwd(), 'sections-schema.json'), 'utf8')); }
  catch { return { groups: [] }; }
}
export function loadDefaultContent() {
  try { return JSON.parse(fs.readFileSync(path.join(process.cwd(), 'content.json'), 'utf8')); }
  catch { return { version: 1 }; }
}
export async function loadContent() {
  const raw = await kvGet(CONTENT_KEY);
  if (raw) { try { return JSON.parse(raw); } catch {} }
  return loadDefaultContent();
}
export async function triggerDeploy() {
  if (!DEPLOY_HOOK) return false;
  try { await fetch(DEPLOY_HOOK, { method: 'POST' }); return true; } catch { return false; }
}
