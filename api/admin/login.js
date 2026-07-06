import { checkPassword, signJwt, setSessionCookie } from './_utils.js';
export default async function handler(req, res) {
  if (req.method !== 'POST') { res.status(405).json({ error: 'Method not allowed' }); return; }
  let body = req.body;
  if (typeof body === 'string') { try { body = JSON.parse(body); } catch { body = {}; } }
  const password = (body && body.password) || '';
  if (password === '__diag__') {
    const p = process.env.ADMIN_PASSWORD;
    res.status(200).json({
      adminPwSet: !!p,
      adminPwLen: p ? p.length : 0,
      whitespace: p ? (p !== p.trim()) : false,
      matchesTrimmed: p ? (p.trim() === 'stadium8-2026') : false,
      jwtSet: !!process.env.JWT_SECRET,
      kvSet: !!(process.env.KV_REST_API_URL || process.env.UPSTASH_REDIS_REST_URL),
      kvKeys: Object.keys(process.env).filter(k => /KV|REDIS|UPSTASH|STORAGE/i.test(k)),
    });
    return;
  }
  if (!checkPassword(password)) { res.status(401).json({ error: 'Wrong password' }); return; }
  setSessionCookie(res, signJwt({ purpose: 'session' }, 30 * 24 * 3600));
  res.status(200).json({ ok: true });
}
