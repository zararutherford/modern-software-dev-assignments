async function fetchJSON(url, options) {
  const res = await fetch(url, options);
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

let page = 1;
let pageSize = 5;
let currentQuery = '';
let currentSort = 'created_desc';

async function loadNotes() {
  const list = document.getElementById('notes');
  list.innerHTML = '';
  const meta = document.getElementById('search-meta');
  const url = new URL('/notes/search/', window.location.origin);
  if (currentQuery) url.searchParams.set('q', currentQuery);
  url.searchParams.set('page', String(page));
  url.searchParams.set('page_size', String(pageSize));
  url.searchParams.set('sort', currentSort);
  const res = await fetchJSON(url.toString());
  meta.textContent = `Total: ${res.total} • Page ${res.page} / ${Math.ceil(res.total / res.page_size) || 1}`;
  for (const n of res.items) {
    const li = document.createElement('li');
    const tags = (n.tags || []).length ? ` [#${(n.tags || []).join(', #')}]` : '';
    li.textContent = `${n.title}: ${n.content}${tags}`;
    const btn = document.createElement('button');
    btn.textContent = 'Extract';
    btn.onclick = async () => {
      const r = await fetchJSON(`/notes/${n.id}/extract?apply=true`, { method: 'POST' });
      alert(`Extracted tags: ${r.tags.join(', ')}\nAction items: ${r.action_items.join('\n')}`);
      loadNotes();
      loadActions();
    };
    li.appendChild(btn);
    list.appendChild(li);
  }
}

async function loadActions() {
  const list = document.getElementById('actions');
  list.innerHTML = '';
  const items = await fetchJSON('/action-items/');
  for (const a of items) {
    const li = document.createElement('li');
    li.textContent = `${a.description} [${a.completed ? 'done' : 'open'}]`;
    if (!a.completed) {
      const btn = document.createElement('button');
      btn.textContent = 'Complete';
      btn.onclick = async () => {
        await fetchJSON(`/action-items/${a.id}/complete`, { method: 'PUT' });
        loadActions();
      };
      li.appendChild(btn);
    }
    list.appendChild(li);
  }
}

window.addEventListener('DOMContentLoaded', () => {
  document.getElementById('note-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const title = document.getElementById('note-title').value;
    const content = document.getElementById('note-content').value;
    await fetchJSON('/notes/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title, content }),
    });
    e.target.reset();
    loadNotes();
  });

  document.getElementById('action-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const description = document.getElementById('action-desc').value;
    await fetchJSON('/action-items/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ description }),
    });
    e.target.reset();
    loadActions();
  });

  document.getElementById('search-btn').addEventListener('click', (e) => {
    e.preventDefault();
    currentQuery = document.getElementById('search-q').value.trim();
    currentSort = document.getElementById('search-sort').value;
    page = 1;
    loadNotes();
  });

  document.getElementById('prev-page').addEventListener('click', (e) => {
    e.preventDefault();
    if (page > 1) {
      page -= 1;
      loadNotes();
    }
  });

  document.getElementById('next-page').addEventListener('click', (e) => {
    e.preventDefault();
    page += 1;
    loadNotes();
  });

  loadNotes();
  loadActions();
});
