/* ========================================
   FORGOT PASSWORD & RESET PASSWORD SCRIPTS
   CropAI Smart Crop Recommendation System
   ======================================== */

document.addEventListener('DOMContentLoaded', function () {

  // ================================
  // 1. PASSWORD TOGGLE (Reset Page)
  // ================================
  const togglePassword = document.getElementById('togglePassword');
  const passwordInput = document.getElementById('password');
  const toggleConfirmPassword = document.getElementById('toggleConfirmPassword');
  const confirmPasswordInput = document.getElementById('confirmPassword');

  if (togglePassword && passwordInput) {
    togglePassword.addEventListener('click', function () {
      const type = passwordInput.type === 'password' ? 'text' : 'password';
      passwordInput.type = type;
      this.querySelector('i').classList.toggle('fa-eye');
      this.querySelector('i').classList.toggle('fa-eye-slash');
    });
  }

  if (toggleConfirmPassword && confirmPasswordInput) {
    toggleConfirmPassword.addEventListener('click', function () {
      const type = confirmPasswordInput.type === 'password' ? 'text' : 'password';
      confirmPasswordInput.type = type;
      this.querySelector('i').classList.toggle('fa-eye');
      this.querySelector('i').classList.toggle('fa-eye-slash');
    });
  }

  // ================================
  // 2. PASSWORD STRENGTH METER
  // ================================
  const strengthBar = document.getElementById('strengthFill');
  const strengthText = document.getElementById('strengthText');
  const passwordStrength = document.getElementById('passwordStrength');
  const passwordRequirements = document.getElementById('passwordRequirements');

  if (passwordInput && strengthBar && strengthText) {
    passwordInput.addEventListener('focus', function () {
      passwordStrength.classList.add('visible');
      passwordRequirements.classList.add('visible');
    });

    passwordInput.addEventListener('input', function () {
      const val = this.value;
      const reqs = {
        length: val.length >= 8,
        upper: /[A-Z]/.test(val),
        lower: /[a-z]/.test(val),
        number: /\d/.test(val),
        special: /[^A-Za-z0-9]/.test(val)
      };

      // Update requirement indicators
      updateRequirement('reqLength', reqs.length);
      updateRequirement('reqUpper', reqs.upper);
      updateRequirement('reqLower', reqs.lower);
      updateRequirement('reqNumber', reqs.number);
      updateRequirement('reqSpecial', reqs.special);

      // Calculate score
      let score = 0;
      if (reqs.length) score++;
      if (reqs.upper) score++;
      if (reqs.lower) score++;
      if (reqs.number) score++;
      if (reqs.special) score++;

      // Update strength bar
      strengthBar.className = 'strength-fill';
      strengthText.className = 'strength-text';

      if (val.length === 0) {
        strengthBar.style.width = '0%';
        strengthText.textContent = 'Password strength';
      } else if (score <= 2) {
        strengthBar.classList.add('weak');
        strengthText.classList.add('weak');
        strengthText.textContent = 'Weak — keep going!';
      } else if (score === 3) {
        strengthBar.classList.add('fair');
        strengthText.classList.add('fair');
        strengthText.textContent = 'Fair — add more variety';
      } else if (score === 4) {
        strengthBar.classList.add('good');
        strengthText.classList.add('good');
        strengthText.textContent = 'Good — almost there!';
      } else {
        strengthBar.classList.add('strong');
        strengthText.classList.add('strong');
        strengthText.textContent = 'Strong password!';
      }

      // Re-check password match
      checkPasswordMatch();
    });
  }

  function updateRequirement(id, met) {
    const el = document.getElementById(id);
    if (el) {
      el.classList.toggle('met', met);
    }
  }

  // ================================
  // 3. CONFIRM PASSWORD MATCH CHECK
  // ================================
  const passwordMatch = document.getElementById('passwordMatch');

  function checkPasswordMatch() {
    if (!confirmPasswordInput || !passwordInput || !passwordMatch) return;

    const pwd = passwordInput.value;
    const confirm = confirmPasswordInput.value;

    if (confirm.length > 0) {
      passwordMatch.classList.add('visible');
      if (pwd === confirm) {
        passwordMatch.classList.add('match');
        passwordMatch.querySelector('span').textContent = 'Passwords match!';
      } else {
        passwordMatch.classList.remove('match');
        passwordMatch.querySelector('span').textContent = 'Passwords do not match';
      }
    } else {
      passwordMatch.classList.remove('visible');
    }
  }

  if (confirmPasswordInput) {
    confirmPasswordInput.addEventListener('input', checkPasswordMatch);
  }

  // ================================
  // 4. FORM SUBMIT LOADER
  // ================================
  const forgotForm = document.getElementById('forgotForm');
  const resetForm = document.getElementById('resetForm');
  const submitBtn = document.getElementById('submitBtn');

  function handleSubmit(form, btn) {
    if (!form || !btn) return;
    form.addEventListener('submit', function () {
      btn.classList.add('loading');
      btn.disabled = true;
    });
  }

  handleSubmit(forgotForm, submitBtn);
  handleSubmit(resetForm, submitBtn);

  // ================================
  // 5. ORB PARALLAX (mouse move)
  // ================================
  const orbs = document.querySelectorAll('.orb');
  let mouseX = 0, mouseY = 0;

  document.addEventListener('mousemove', function (e) {
    mouseX = e.clientX / window.innerWidth - 0.5;
    mouseY = e.clientY / window.innerHeight - 0.5;

    orbs.forEach(function (orb, index) {
      const speed = (index + 1) * 15;
      const x = mouseX * speed;
      const y = mouseY * speed;
      orb.style.transform = 'translate(' + x + 'px, ' + y + 'px)';
    });
  });

});
