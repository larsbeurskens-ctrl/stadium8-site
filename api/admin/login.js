import { checkPassword, signJwt, setSessionCookie } from './_utils.js';
export default async function handler(req, res) {
  if (req.method !== 'POST') { res.status(405).json({ error: 'Method not allowed' }); return; }
  let body = req.body;
  if (typeof body === 'string') { try { body = JSON.parse(body); } catch { body = {}; } }
  const password = (body && body.password) || '';
  if (!checkPassword(password)) { res.status(401).json({ error: 'Wrong password' }); return; }
  setSessionCookie(res, signJwt({ purpose: 'session' }, 30 * 24 * 3600));
  res.status(200).json({ ok: true });
}
