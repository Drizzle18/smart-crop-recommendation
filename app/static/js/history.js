// Menu toggle for responsive
const menuToggle = document.getElementById('menuToggle');
const sidebar = document.getElementById('sidebar');

menuToggle?.addEventListener('click', () => {
  sidebar?.classList.toggle('open');
});

// Close sidebar when clicking a nav item
document.querySelectorAll('.nav-item').forEach(item => {
  item.addEventListener('click', () => {
    if (window.innerWidth <= 820) {
      sidebar?.classList.remove('open');
    }
  });
});

// Close sidebar when clicking outside
document.addEventListener('click', (e) => {
  if (!sidebar?.contains(e.target) && !menuToggle?.contains(e.target)) {
    sidebar?.classList.remove('open');
  }
});

// Parallax orbs
document.addEventListener('mousemove', (e) => {
  const x = (e.clientX / window.innerWidth - 0.5) * 20;
  const y = (e.clientY / window.innerHeight - 0.5) * 20;
  document.querySelectorAll('.orb').forEach((orb, i) => {
    const f = i === 0 ? 1 : -1;
    orb.style.transform = `translate(${x * f}px, ${y * f}px)`;
  });
});

// Search
const search = document.getElementById('search');
const filter = document.getElementById('filter');
const rows = () => document.querySelectorAll('.history-table tbody tr');

function applyFilters() {
  const q = (search?.value || '').toLowerCase().trim();
  const range = filter?.value || 'all';
  const now = Date.now();
  const ms = range === 'week' ? 7 * 864e5 : range === 'month' ? 30 * 864e5 : Infinity;

  rows().forEach(r => {
    const crop = r.dataset.crop || '';
    const date = Date.parse(r.dataset.date || '') || 0;
    const matchText = !q || crop.includes(q);
    const matchDate = ms === Infinity || (now - date) <= ms;
    r.style.display = matchText && matchDate ? '' : 'none';
  });
}

search?.addEventListener('input', applyFilters);
filter?.addEventListener('change', applyFilters);
