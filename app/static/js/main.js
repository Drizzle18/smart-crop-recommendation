
const cards = document.querySelectorAll('.feature-card, .metric-card');

const observer = new IntersectionObserver(entries => {
  entries.forEach(entry => {

    if(entry.isIntersecting) {
      entry.target.style.opacity = '1';
      entry.target.style.transform = 'translateY(0px)';
    }

  });
}, {
  threshold: 0.2
});

cards.forEach(card => {

  card.style.opacity = '0';
  card.style.transform = 'translateY(40px)';
  card.style.transition = 'all 0.8s ease';

  observer.observe(card);
});

const scrollBtn = document.getElementById('scrollTopBtn');

window.addEventListener('scroll', () => {

  if(window.scrollY > 300) {
    scrollBtn.classList.add('active');
  }
  else {
    scrollBtn.classList.remove('active');
  }

});

scrollBtn.addEventListener('click', () => {
  window.scrollTo({
    top: 0,
    behavior: 'smooth'
  });
});
