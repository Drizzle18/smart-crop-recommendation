// SmartCrop — About page interactions
// Drop into: app/static/js/about.js

document.addEventListener('DOMContentLoaded', () => {
  // Year in footer
  const yearEl = document.getElementById('year');
  if (yearEl) yearEl.textContent = new Date().getFullYear();

  // Scroll-to-top button
  const scrollBtn = document.getElementById('scrollTopBtn');
  if (scrollBtn) {
    window.addEventListener('scroll', () => {
      scrollBtn.classList.toggle('visible', window.scrollY > 400);
    });
    scrollBtn.addEventListener('click', () => {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  // Reveal-on-scroll animation
  const revealEls = document.querySelectorAll(
    '.glass-card, .step-card, .tech-card, .mini-card, .stat-card, .glass-panel, .cta-band, .workflow'
  );
  revealEls.forEach((el) => el.classList.add('reveal'));

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.12 }
  );
  revealEls.forEach((el) => observer.observe(el));

  // Animated counter for stat numbers
  const counters = document.querySelectorAll('.stat-num');
  const counterObserver = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        const el = entry.target;
        const text = el.textContent.trim();
        const match = text.match(/([\d.]+)/);
        if (!match) return;
        const target = parseFloat(match[1]);
        const suffix = text.replace(match[1], '');
        let current = 0;
        const step = target / 40;
        const tick = () => {
          current += step;
          if (current >= target) {
            el.textContent = (Number.isInteger(target) ? target : target.toFixed(1)) + suffix;
            return;
          }
          el.textContent = (Number.isInteger(target) ? Math.floor(current) : current.toFixed(1)) + suffix;
          requestAnimationFrame(tick);
        };
        tick();
        counterObserver.unobserve(el);
      });
    },
    { threshold: 0.5 }
  );
  counters.forEach((c) => counterObserver.observe(c));
});
