import { clearSessionCookie } from './_utils.js';
export default async function handler(req, res) {
  clearSessionCookie(res);
  res.status(200).json({ ok: true });
}
