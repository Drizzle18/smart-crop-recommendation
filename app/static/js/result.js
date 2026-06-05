// Sidebar toggle (mobile)
const toggle = document.getElementById('menuToggle');
const sidebar = document.getElementById('sidebar');
if (toggle && sidebar) {
  toggle.addEventListener('click', (e) => {
    e.stopPropagation();
    sidebar.classList.toggle('open');
  });
  document.addEventListener('click', (e) => {
    if (window.innerWidth <= 820 && !sidebar.contains(e.target) && !toggle.contains(e.target)) {
      sidebar.classList.remove('open');
    }
  });
}

// Parallax orbs
document.addEventListener('mousemove', (e) => {
  const x = (e.clientX / window.innerWidth - 0.5) * 20;
  const y = (e.clientY / window.innerHeight - 0.5) * 20;
  document.querySelectorAll('.orb').forEach((orb, i) => {
    const f = (i + 1) * 0.5;
    orb.style.transform = `translate(${x * f}px, ${y * f}px)`;
  });
});

// Animate confidence bar
window.addEventListener('load', () => {
  const fill = document.getElementById('confFill');
  if (fill) {
    const val = Math.max(0, Math.min(100, parseFloat(fill.dataset.value) || 0));
    requestAnimationFrame(() => { fill.style.width = val + '%'; });
  }

  // Animate chart bars
  document.querySelectorAll('.chart .bar').forEach((bar) => {
    const val = parseFloat(bar.dataset.value) || 0;
    const max = parseFloat(bar.dataset.max) || 100;
    const pct = Math.max(2, Math.min(100, (val / max) * 100));
    setTimeout(() => { bar.style.height = pct + '%'; }, 150);
  });
});
