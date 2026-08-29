const express = require('express');
const fs = require('fs');
const path = require('path');
const { marked } = require('marked');

const app = express();
const PORT = 3001;

const WIKI_PATH = '/home/kizamladjanijebac/wiki/notebooks_verified_registry.md';
const WORK_LOG_PATH = '/home/kizamladjanijebac/WORK_LOG.md';

app.use(express.static(path.join(__dirname, 'public')));
app.use(express.json());

app.get('/api/notebooks', (req, res) => {
  try {
    const md = fs.readFileSync(WIKI_PATH, 'utf8');
    const notebooks = parseNotebooks(md);
    res.json({ success: true, notebooks });
  } catch (e) {
    res.json({ success: false, error: e.message, notebooks: [] });
  }
});

app.get('/api/worklog', (req, res) => {
  try {
    const content = fs.readFileSync(WORK_LOG_PATH, 'utf8');
    res.json({ success: true, content });
  } catch (e) {
    res.json({ success: false, content: '' });
  }
});

app.get('/api/stats', (req, res) => {
  try {
    const md = fs.readFileSync(WIKI_PATH, 'utf8');
    const notebooks = parseNotebooks(md);
    const verified = notebooks.filter(n => n.verified).length;
    const owned = notebooks.filter(n => n.ownership === 'owned').length;
    const shared = notebooks.filter(n => n.ownership === 'shared_with_me').length;
    const totalSources = notebooks.reduce((sum, n) => sum + (n.sourceCount || 0), 0);
    res.json({ success: true, total: notebooks.length, verified, owned, shared, totalSources });
  } catch (e) {
    res.json({ success: false });
  }
});

app.get('/api/notebook/:id/html', (req, res) => {
  try {
    const md = fs.readFileSync(WIKI_PATH, 'utf8');
    const notebooks = parseNotebooks(md);
    const nb = notebooks.find(n => n.id === parseInt(req.params.id));
    if (!nb) return res.json({ success: false, html: '' });
    const html = marked.parse(nb.fullMd);
    res.json({ success: true, html });
  } catch (e) {
    res.json({ success: false, html: '' });
  }
});

function parseNotebooks(md) {
  const sections = md.split(/\n### /);
  const notebooks = [];

  const tagColors = {
    '🧠': '#7c3aed', '🤖': '#2563eb', '💓': '#dc2626', '🚀': '#d97706',
    '⚙️': '#0891b2', '❓': '#16a34a', '🎨': '#db2777', '📚': '#ea580c', '🛡️': '#4f46e5',
    '🔬': '#7c3aed', '🏢': '#2563eb', '🧘': '#16a34a',
  };

  for (let i = 1; i < sections.length; i++) {
    const section = sections[i];
    const lines = section.split('\n');
    const titleLine = lines[0] || '';

    let icon = '📓';
    for (const emoji of Object.keys(tagColors)) {
      if (titleLine.startsWith(emoji)) { icon = emoji; break; }
    }

    const title = titleLine.replace(/^(\S+ )?/, '').replace(/[:*]/g, '').trim();
    const uuidMatch = section.match(/`([0-9a-f]{8}-[0-9a-f-]+)`/);
    const uuid = uuidMatch ? uuidMatch[1] : '';
    const ownershipMatch = section.match(/`(owned|shared_with_me)`/);
    const ownership = ownershipMatch ? ownershipMatch[1] : 'unknown';
    const sourceMatch = section.match(/\*\*Broj izvora:\*\* (\d+)/);
    const sourceCount = sourceMatch ? parseInt(sourceMatch[1]) : 0;
    const verified = section.includes('✅') && section.includes('VERIFIKOVANO');
    const noteIdMatch = section.match(/beleška ID: `([^`]+)`/);
    const noteId = noteIdMatch ? noteIdMatch[1] : null;

    const factsSection = section.match(/####[^\n]*\n([\s\S]*?)(?=\n---|$)/);
    let facts = [];
    if (factsSection) {
      const lines2 = factsSection[1].split('\n').filter(l => l.trim().length > 10);
      facts = lines2.slice(0, 5).map(l =>
        l.trim()
          .replace(/^\*{1,2}/, '').replace(/\*{1,2}$/, '')
          .replace(/\*\*/g, '')
          .replace(/^[0-9]+\.\s*/, '')
          .replace(/^\-\s*/, '')
          .substring(0, 120)
      ).filter(f => f.length > 5);
    }

    notebooks.push({
      id: i, icon,
      color: tagColors[icon] || '#6b7280',
      title, uuid, ownership, sourceCount, verified, noteId, facts,
      fullMd: '### ' + section,
      batch: i <= 5 ? 1 : i <= 10 ? 2 : 3,
      index: i,
    });
  }
  return notebooks;
}

app.listen(PORT, () => {
  console.log(`\n🚀 Antigravity Wiki UI running at http://localhost:${PORT}\n`);
});
