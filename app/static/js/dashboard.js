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
const orbs = document.querySelectorAll('.orb');
document.addEventListener('mousemove', (e) => {
  const x = (e.clientX / window.innerWidth - 0.5) * 20;
  const y = (e.clientY / window.innerHeight - 0.5) * 20;
  orbs.forEach((orb, i) => {
    const factor = (i + 1) * 0.6;
    orb.style.transform = `translate(${x * factor}px, ${y * factor}px)`;
  });
});

// Logout spinner
const dashboardLogoutLinks = document.querySelectorAll('.nav-item.logout');
dashboardLogoutLinks.forEach((link) => {
  link.addEventListener('click', (event) => {
    event.preventDefault();
    const spinner = link.querySelector('.logout-spinner');
    const text = link.querySelector('.nav-text');
    if (spinner) {
      spinner.hidden = false;
    }
    if (text) {
      text.textContent = 'Logging out...';
    }
    link.style.pointerEvents = 'none';
    window.location.href = link.href;
  });
});

// Animate stat numbers
document.querySelectorAll('.stat-card h2').forEach((el) => {
  const text = el.textContent.trim();
  const match = text.match(/^([\d.]+)(.*)$/);
  if (!match) return;
  const end = parseFloat(match[1]);
  const suffix = match[2] || '';
  let start = 0;
  const dur = 1200;
  const t0 = performance.now();
  const step = (t) => {
    const p = Math.min((t - t0) / dur, 1);
    const eased = 1 - Math.pow(1 - p, 3);
    const val = end % 1 === 0 ? Math.round(end * eased) : (end * eased).toFixed(1);
    el.textContent = val + suffix;
    if (p < 1) requestAnimationFrame(step);
  };
  requestAnimationFrame(step);
});

// Animate confidence bars
setTimeout(() => {
  document.querySelectorAll('.bar span').forEach((b) => {
    const w = b.style.width;
    b.style.width = '0';
    requestAnimationFrame(() => {
      b.style.transition = 'width 1s ease';
      b.style.width = w;
    });
  });
}, 200);
