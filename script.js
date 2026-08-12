document.addEventListener('DOMContentLoaded', () => {

  /* Nav panel ------------------------------------------------------------ */
  const burger = document.querySelector('.nav-burger');
  const panel = document.querySelector('.nav-panel');

  if (burger && panel) {
    burger.addEventListener('click', () => {
      const open = !panel.classList.contains('open');
      panel.classList.toggle('open', open);
      burger.setAttribute('aria-expanded', String(open));
      document.body.classList.toggle('nav-open', open);
    });

    panel.querySelectorAll('a').forEach((link) => {
      link.addEventListener('click', () => {
        panel.classList.remove('open');
        burger.setAttribute('aria-expanded', 'false');
        document.body.classList.remove('nav-open');
      });
    });

    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && panel.classList.contains('open')) burger.click();
    });
  }

  /* Accordions ----------------------------------------------------------- */
  document.querySelectorAll('.accordion-trigger').forEach((trigger) => {
    trigger.addEventListener('click', () => {
      const item = trigger.closest('.accordion-item');
      const open = !item.classList.contains('open');
      item.classList.toggle('open', open);
      trigger.setAttribute('aria-expanded', String(open));
    });
  });

  /* Carousels ------------------------------------------------------------ */
  document.querySelectorAll('.carousel').forEach((carousel) => {
    const track = carousel.querySelector('.carousel-track');
    const slides = Array.from(carousel.querySelectorAll('.carousel-slide'));
    const prev = carousel.querySelector('.carousel-prev');
    const next = carousel.querySelector('.carousel-next');
    const dots = Array.from(carousel.querySelectorAll('.carousel-dot'));
    if (!track || slides.length < 2) return;

    let index = 0;

    const render = () => {
      track.style.transform = `translateX(-${index * 100}%)`;
      slides.forEach((slide, i) => {
        slide.setAttribute('aria-hidden', String(i !== index));
        // Keep off-screen slides out of the tab order
        slide.querySelectorAll('a, button').forEach((el) => {
          el.tabIndex = i === index ? 0 : -1;
        });
      });
      dots.forEach((dot, i) => dot.setAttribute('aria-selected', String(i === index)));
      if (prev) prev.disabled = index === 0;
      if (next) next.disabled = index === slides.length - 1;
    };

    const goTo = (i) => {
      index = Math.max(0, Math.min(i, slides.length - 1));
      render();
    };

    if (prev) prev.addEventListener('click', () => goTo(index - 1));
    if (next) next.addEventListener('click', () => goTo(index + 1));
    dots.forEach((dot, i) => dot.addEventListener('click', () => goTo(i)));

    carousel.addEventListener('keydown', (e) => {
      if (e.key === 'ArrowLeft') { e.preventDefault(); goTo(index - 1); }
      if (e.key === 'ArrowRight') { e.preventDefault(); goTo(index + 1); }
    });

    // Touch swipe
    let startX = null;
    track.addEventListener('touchstart', (e) => { startX = e.touches[0].clientX; }, { passive: true });
    track.addEventListener('touchend', (e) => {
      if (startX === null) return;
      const dx = e.changedTouches[0].clientX - startX;
      if (Math.abs(dx) > 45) goTo(dx < 0 ? index + 1 : index - 1);
      startX = null;
    }, { passive: true });

    render();
  });

  /* Reveal on scroll ----------------------------------------------------- */
  const revealEls = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window && revealEls.length) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('in');
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12 });
    revealEls.forEach((el) => io.observe(el));
  } else {
    revealEls.forEach((el) => el.classList.add('in'));
  }

  /* Footer year ---------------------------------------------------------- */
  const year = document.getElementById('year');
  if (year) year.textContent = new Date().getFullYear();

  /* Contact form --------------------------------------------------------- */
  const form = document.querySelector('.form');
  if (form) {
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      const note = form.querySelector('.form-note');
      if (note) note.textContent = 'Thank you — your enquiry has been recorded. We will be in touch shortly.';
      form.reset();
    });
  }
});
