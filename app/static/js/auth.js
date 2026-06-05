/* SmartCrop Auth — Login & Signup interactions */

document.addEventListener('DOMContentLoaded', () => {

  // ===== Toggle password visibility =====
  document.querySelectorAll('.toggle-password').forEach(btn => {
    btn.addEventListener('click', () => {
      const input = btn.parentElement.querySelector('input');
      const icon = btn.querySelector('i');
      if (input.type === 'password') {
        input.type = 'text';
        icon.classList.replace('fa-eye', 'fa-eye-slash');
      } else {
        input.type = 'password';
        icon.classList.replace('fa-eye-slash', 'fa-eye');
      }
    });
  });

  // ===== Password strength meter (signup) =====
  const pwd = document.getElementById('password');
  const fill = document.querySelector('.strength-fill');
  const label = document.querySelector('.strength-label');

  if (pwd && fill && label) {
    pwd.addEventListener('input', () => {
      const v = pwd.value;
      let score = 0;
      if (v.length >= 8) score++;
      if (/[A-Z]/.test(v)) score++;
      if (/[0-9]/.test(v)) score++;
      if (/[^A-Za-z0-9]/.test(v)) score++;

      const levels = [
        { w: '0%',   c: '#ef476f', t: 'Password strength' },
        { w: '25%',  c: '#ef476f', t: 'Weak' },
        { w: '50%',  c: '#f4a261', t: 'Fair' },
        { w: '75%',  c: '#74c69d', t: 'Good' },
        { w: '100%', c: '#52b788', t: 'Strong' },
      ];
      const lvl = levels[score];
      fill.style.width = lvl.w;
      fill.style.background = lvl.c;
      label.textContent = lvl.t;
      label.style.color = lvl.c;
    });
  }

  // ===== Confirm password match (signup) =====
  const confirm = document.getElementById('confirm_password');
  if (confirm && pwd) {
    const validate = () => {
      if (confirm.value && confirm.value !== pwd.value) {
        confirm.style.borderColor = '#ef476f';
      } else {
        confirm.style.borderColor = '';
      }
    };
    confirm.addEventListener('input', validate);
    pwd.addEventListener('input', validate);
  }

  // ===== Form submit loading state =====
  document.querySelectorAll('.auth-form').forEach(form => {
    form.addEventListener('submit', (e) => {
      const btn = form.querySelector('.btn-glass-primary');
      if (btn && form.checkValidity()) {
        btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Please wait...';
        btn.disabled = true;
      }
    });
  });

  // ===== Subtle parallax on orbs =====
  document.addEventListener('mousemove', (e) => {
    const x = (e.clientX / window.innerWidth - 0.5) * 20;
    const y = (e.clientY / window.innerHeight - 0.5) * 20;
    document.querySelectorAll('.orb').forEach((orb, i) => {
      const factor = (i + 1) * 0.5;
      orb.style.transform = `translate(${x * factor}px, ${y * factor}px)`;
    });
  });
});
