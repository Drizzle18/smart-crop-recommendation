// ==================================================
// SMART CROP — PREDICT PAGE INTERACTIONS
// ==================================================

(function () {

  // ------------------------------------------
  // SIDEBAR TOGGLE (MOBILE)
  // ------------------------------------------

  const toggle = document.getElementById('menuToggle');
  const sidebar = document.getElementById('sidebar');
  if (toggle && sidebar) {
    toggle.addEventListener('click', (e) => {
      e.stopPropagation();
      sidebar.classList.toggle('open');
    });
    document.addEventListener('click', (e) => {
      if (window.innerWidth <= 720 && !sidebar.contains(e.target) && !toggle.contains(e.target)) {
        sidebar.classList.remove('open');
      }
    });
  }

  // ------------------------------------------
  // FORM SUBMIT LOADING STATE
  // ------------------------------------------

  const form = document.getElementById("predictForm");
  const submitBtn = document.getElementById("submitBtn");

  if (form && submitBtn) {

    const spinner = submitBtn.querySelector(".spinner");
    const btnText = submitBtn.querySelector(".btn-text");

    form.addEventListener("submit", function () {

      submitBtn.disabled = true;

      if (spinner) {
        spinner.hidden = false;
      }

      if (btnText) {
        btnText.textContent = "Analyzing Soil Data...";
      }

    });

  }

  // ------------------------------------------
  // LOGOUT BUTTON SPINNER
  const logoutLinks = document.querySelectorAll('.nav-item.logout');
  logoutLinks.forEach((link) => {
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


  // ------------------------------------------
  // PARALLAX BACKGROUND ORBS
  // ------------------------------------------

  const orbs = document.querySelectorAll(".orb");

  if (orbs.length > 0) {

    document.addEventListener("mousemove", function (e) {

      const x =
        (e.clientX / window.innerWidth - 0.5) * 20;

      const y =
        (e.clientY / window.innerHeight - 0.5) * 20;

      orbs.forEach((orb, index) => {

        const factor = (index + 1) * 0.45;

        orb.style.transform =
          `translate(${x * factor}px, ${y * factor}px)`;

      });

    });

  }


  // ------------------------------------------
  // AUTO-SCROLL TO RESULT CARD
  // AFTER PREDICTION
  // ------------------------------------------

  const resultCard =
    document.querySelector(".result-card");

  if (resultCard) {

    setTimeout(() => {

      resultCard.scrollIntoView({
        behavior: "smooth",
        block: "center"
      });

    }, 300);

  }


  // ------------------------------------------
  // INPUT FOCUS ANIMATION
  // ------------------------------------------

  const inputs =
    document.querySelectorAll(
      ".field input"
    );

  inputs.forEach((input) => {

    input.addEventListener("focus", () => {
      input.parentElement.classList.add(
        "active-field"
      );
    });

    input.addEventListener("blur", () => {
      input.parentElement.classList.remove(
        "active-field"
      );
    });

  });


  // ------------------------------------------
  // RESET BUTTON RESTORES NORMAL STATE
  // ------------------------------------------

  if (form) {

    form.addEventListener("reset", () => {

      setTimeout(() => {

        if (submitBtn) {

          submitBtn.disabled = false;

          const spinner =
            submitBtn.querySelector(".spinner");

          const btnText =
            submitBtn.querySelector(".btn-text");

          if (spinner) {
            spinner.hidden = true;
          }

          if (btnText) {
            btnText.textContent =
              "Get Recommendation";
          }

        }

      }, 50);

    });

  }

  // ------------------------------------------
  // AUTO-DISMISS FLASH MESSAGES (visible + glow)
  // ------------------------------------------
  const flashItems = document.querySelectorAll('.flash');
  if (flashItems.length) {
    flashItems.forEach((f) => {
      // keep visible for 5s, then fade
      const timeout = 5000;
      let hideTimer = setTimeout(() => {
        f.classList.add('hide');
        setTimeout(() => f.remove(), 500);
      }, timeout);

      // pause dismissal when hovered
      f.addEventListener('mouseenter', () => clearTimeout(hideTimer));
      f.addEventListener('mouseleave', () => {
        hideTimer = setTimeout(() => {
          f.classList.add('hide');
          setTimeout(() => f.remove(), 500);
        }, 1500);
      });
    });
  }

})();