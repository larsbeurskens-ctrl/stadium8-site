import { requireAuth, loadSchema, loadContent, kvSetRaw, triggerDeploy, CONTENT_KEY } from './_utils.js';
export default async function handler(req, res) {
  const session = requireAuth(req, res);
  if (!session) return;

  if (req.method === 'GET') {
    const [schema, content] = [loadSchema(), await loadContent()];
    res.status(200).json({ schema, content });
    return;
  }
  if (req.method === 'POST') {
    let body = req.body;
    if (typeof body === 'string') { try { body = JSON.parse(body); } catch { body = {}; } }
    const content = body && body.content;
    if (!content || typeof content !== 'object' || Array.isArray(content)) {
      res.status(400).json({ error: 'Invalid content payload' }); return;
    }
    if (content.version == null) content.version = 1;
    const serialized = JSON.stringify(content);
    if (serialized.length > 600000) { res.status(413).json({ error: 'Content too large' }); return; }
    try {
      await kvSetRaw(CONTENT_KEY, serialized);
    } catch (e) {
      res.status(500).json({ error: 'Could not save (KV): ' + e.message }); return;
    }
    const deployed = await triggerDeploy();
    res.status(200).json({ ok: true, deployed });
    return;
  }
  res.status(405).json({ error: 'Method not allowed' });
}
