// ====== main.js — Common UI helpers ======
function toast(msg, type = '') {
  const t = document.createElement('div');
  t.className = 'toast ' + type; t.textContent = msg;
  document.body.appendChild(t); setTimeout(() => t.remove(), 3000);
}
// Mobile nav toggle
document.addEventListener('click', e => {
  if (e.target.closest('.nav-toggle')) document.querySelector('.nav-links').classList.toggle('open');
  if (e.target.closest('.menu-btn')) document.querySelector('.sidebar').classList.toggle('open');
});
// Active link highlight
(function () {
  const here = location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.nav-links a, .sidebar a').forEach(a => {
    if (a.getAttribute('href') === here) a.classList.add('active');
  });
})();
// Table search
function tableSearch(inputId, tableId) {
  const input = document.getElementById(inputId), rows = document.querySelectorAll('#' + tableId + ' tbody tr');
  if (!input) return;
  input.addEventListener('input', () => {
    const q = input.value.toLowerCase();
    rows.forEach(r => r.style.display = r.textContent.toLowerCase().includes(q) ? '' : 'none');
  });
}
// Export table to CSV
function exportCSV(tableId, filename = 'export.csv') {
  const rows = [...document.querySelectorAll('#' + tableId + ' tr')].map(tr =>
    [...tr.children].map(td => '"' + td.textContent.trim().replace(/"/g, '""') + '"').join(','));
  const a = document.createElement('a');
  a.href = URL.createObjectURL(new Blob([rows.join('\n')], { type: 'text/csv' }));
  a.download = filename; a.click();
}
// Simple form validation
function validateForm(form) {
  let ok = true;
  form.querySelectorAll('[required]').forEach(f => {
    const err = f.parentElement.querySelector('.error');
    if (err) err.remove();
    if (!f.value.trim()) {
      ok = false; const e = document.createElement('div'); e.className = 'error'; e.textContent = 'Ye field zaroori hai';
      f.parentElement.appendChild(e);
    }
  });
  return ok;
}
document.addEventListener('submit', e => {
  const f = e.target;
  if (f.matches('form[data-demo]')) {
    e.preventDefault();
    if (validateForm(f)) { toast(f.dataset.demo || 'Submit ho gaya!', 'success'); f.reset(); }
  }
});
