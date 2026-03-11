const API_BASE_URL = 'http://localhost:8000';

const loadingEl     = document.getElementById('loading');
const emptyMsgEl    = document.getElementById('emptyMsg');
const errorEl       = document.getElementById('error');
const tableWrapEl   = document.getElementById('tableWrap');
const slugTableBody = document.getElementById('slugTableBody');
const deleteAllBtn  = document.getElementById('deleteAllBtn');

async function fetchSlugs() {
  showLoading(true);
  hideError();

  try {
    const response = await fetch(`${API_BASE_URL}/slugs`);
    if (!response.ok) throw new Error();
    const pairs = await response.json();
    renderTable(pairs);
  } catch {
    showError('Failed to load links. Check your connection.');
  } finally {
    showLoading(false);
  }
}

function renderTable(pairs) {
  slugTableBody.innerHTML = '';

  if (pairs.length === 0) {
    emptyMsgEl.classList.remove('hidden');
    tableWrapEl.classList.add('hidden');
    return;
  }

  emptyMsgEl.classList.add('hidden');
  tableWrapEl.classList.remove('hidden');

  pairs.forEach(({ slug, original_url }, index) => {
    const shortUrl = `${API_BASE_URL}/${encodeURIComponent(slug)}`;
    const tr = document.createElement('tr');
    tr.dataset.slug = slug;

    tr.innerHTML = `
      <td><span class="index-num">${index + 1}</span></td>
      <td>
        <a class="slug-badge" href="${shortUrl}" target="_blank" rel="noopener">
          ${escapeHtml(slug)}
          <svg width="11" height="11" viewBox="0 0 12 12" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M2.5 9.5L9.5 2.5M9.5 2.5H4.5M9.5 2.5V7.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </a>
      </td>
      <td>
        <div class="original-cell">
          <a class="original-url" href="${escapeHtml(original_url)}" target="_blank" rel="noopener" title="${escapeHtml(original_url)}">
            ${escapeHtml(original_url)}
          </a>
        </div>
      </td>
      <td class="col-action">
        <button class="btn-row-delete" data-slug="${escapeHtml(slug)}">Delete</button>
      </td>
    `;

    tr.querySelector('.btn-row-delete').addEventListener('click', () => handleDeleteOne(slug));
    slugTableBody.appendChild(tr);
  });
}

async function handleDeleteOne(slug) {
  try {
    const response = await fetch(`${API_BASE_URL}/slugs/${encodeURIComponent(slug)}`, {
      method: 'DELETE',
    });
    if (!response.ok) throw new Error();

    const row = slugTableBody.querySelector(`[data-slug="${slug}"]`);
    if (row) {
      row.style.opacity = '0';
      row.style.transition = 'opacity 0.2s';
      setTimeout(() => {
        row.remove();
        reindex();
        if (slugTableBody.children.length === 0) {
          tableWrapEl.classList.add('hidden');
          emptyMsgEl.classList.remove('hidden');
        }
      }, 200);
    }
  } catch {
    showError(`Failed to delete slug "${slug}". Please try again.`);
  }
}

async function handleDeleteAll() {
  if (!confirm('Delete all saved links? This action cannot be undone.')) return;

  try {
    const response = await fetch(`${API_BASE_URL}/slugs`, { method: 'DELETE' });
    if (!response.ok) throw new Error();
    renderTable([]);
  } catch {
    showError('Failed to delete all links. Please try again.');
  }
}

function reindex() {
  slugTableBody.querySelectorAll('tr').forEach((tr, i) => {
    tr.querySelector('.index-num').textContent = i + 1;
  });
}

function showLoading(show) {
  loadingEl.classList.toggle('hidden', !show);
}

function showError(msg) {
  errorEl.textContent = msg;
  errorEl.classList.remove('hidden');
}

function hideError() {
  errorEl.classList.add('hidden');
}

function escapeHtml(str) {
  return str
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

deleteAllBtn.addEventListener('click', handleDeleteAll);
fetchSlugs();
