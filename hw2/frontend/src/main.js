import { addParty, listParties, updateParty } from './api.js';
import './style.css';

const root = document.querySelector('#app');
root.innerHTML = `
  <main class="layout">
    <header class="topbar"><div class="brand-mark">T<span>·</span></div><div class="brand">TABLETURN <small>HOST DESK</small></div><span class="live">● &nbsp;LIVE WAITLIST</span></header>
    <section class="intro"><div class="eyebrow">SERVICE DASHBOARD <span> / </span> TODAY</div><h1>Make room for<br><em>everyone.</em></h1><p>A calmer way to welcome your guests. Keep your queue moving, one table at a time.</p></section>
    <section class="workspace">
      <aside class="panel add-panel"><div class="section-kicker">01 / ARRIVALS</div><h2>Add a party<span class="period">.</span></h2><p class="sub">Add guests as they arrive at the door.</p>
        <form id="add-form"><label for="name">GUEST NAME</label><input id="name" name="name" placeholder="e.g. Jordan Lee" maxlength="80" required autofocus />
        <label for="size">PARTY SIZE</label><input id="size" name="size" type="number" min="1" max="20" value="2" required />
        <button class="primary" type="submit">Add to waitlist <span>↗</span></button></form>
        <div class="note"><span class="note-icon">✳</span> A warm welcome starts with an organized door.</div>
      </aside>
      <section class="panel queue-panel"><div class="queue-header"><div><div class="section-kicker">02 / THE QUEUE</div><h2>Waiting list<span class="period">.</span></h2></div><span id="count" class="count">0 waiting</span></div>
        <div id="error" role="alert" hidden></div><div id="queue" aria-live="polite"></div>
        <details class="history"><summary>Recent activity <span>⌄</span></summary><div id="history"></div></details>
      </section>
    </section><footer>TABLETURN <span>·</span> GOOD HOSPITALITY, WELL ORGANIZED</footer>
  </main>`;

const form = document.querySelector('#add-form');
const error = document.querySelector('#error');
let parties = [];

function showError(message) { error.textContent = message; error.hidden = !message; }
function escapeHtml(value) { return String(value).replace(/[&<>"']/g, char => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[char]); }
function elapsed(iso) {
  const minutes = Math.max(0, Math.floor((Date.now() - new Date(iso).getTime()) / 60000));
  return minutes < 1 ? 'Just arrived' : `${minutes} min waiting`;
}
function render() {
  const waiting = parties.filter(p => p.status === 'waiting');
  const done = parties.filter(p => p.status !== 'waiting').reverse();
  document.querySelector('#count').textContent = `${waiting.length} waiting`;
  document.querySelector('#queue').innerHTML = waiting.length ? waiting.map((p, i) => `
    <article class="party"><div class="number">${String(i + 1).padStart(2, '0')}</div><div class="party-main"><strong>${escapeHtml(p.name)}</strong><span>${p.size} ${p.size === 1 ? 'guest' : 'guests'} <b>·</b> ${elapsed(p.created_at)}</span></div>
      <button type="button" class="seat" data-id="${p.id}" data-status="seated">Seat ↗</button><button type="button" class="remove" data-id="${p.id}" data-status="removed" aria-label="Remove ${escapeHtml(p.name)}">×</button></article>`).join('') : '<div class="empty"><div class="empty-icon">✳</div><strong>The door is clear.</strong><p>New arrivals will appear here.</p></div>';
  document.querySelector('#history').innerHTML = done.length ? done.map(p => `<div class="history-row"><span>${escapeHtml(p.name)} · ${p.size} ${p.size === 1 ? 'guest' : 'guests'}</span><span class="tag ${p.status}">${p.status}</span></div>`).join('') : '<p class="muted">No completed parties yet.</p>';
}
async function refresh() {
  try { parties = await listParties(); showError(''); render(); }
  catch (err) { showError(err.message); }
}
form.addEventListener('submit', async event => {
  event.preventDefault();
  const button = form.querySelector('button');
  button.disabled = true;
  try {
    await addParty(form.elements.namedItem('name').value.trim(), Number(form.elements.namedItem('size').value));
    form.reset(); form.elements.namedItem('size').value = '2'; form.elements.namedItem('name').focus();
    await refresh();
  } catch (err) { showError(err.message); }
  finally { button.disabled = false; }
});
document.querySelector('#queue').addEventListener('click', async event => {
  const button = event.target.closest('button[data-id]');
  if (!button) return;
  button.disabled = true;
  try { await updateParty(Number(button.dataset.id), button.dataset.status); await refresh(); }
  catch (err) { showError(err.message); button.disabled = false; }
});
refresh();
setInterval(() => { if (!document.hidden) refresh(); }, 30000);
