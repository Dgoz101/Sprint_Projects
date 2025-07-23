// recipes/static/recipes/app.js
document.addEventListener('DOMContentLoaded', () => {

      /* ------------------ PAGE TRANSITIONS ------------------ */
  const pageEl = document.getElementById('page');
  if (pageEl) {
    // Enter animation
    requestAnimationFrame(() => pageEl.classList.add('page-enter'));

    // Intercept internal links
    const internalLinks = Array.from(document.querySelectorAll('a[href]')).filter(a => {
      const url = new URL(a.href, window.location.href);
      return url.origin === window.location.origin &&
             !a.hasAttribute('data-no-transition') &&
             !a.target;
    });

    internalLinks.forEach(link => {
      link.addEventListener('click', e => {
        // Allow ctrl/cmd click to open in new tab
        if (e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;

        e.preventDefault();
        pageEl.classList.remove('page-enter');
        pageEl.classList.add('page-exit');

        // Navigate after animation
        setTimeout(() => {
          window.location.href = link.href;
        }, 280); // match CSS duration (0.32s ~ 320ms)
      });
    });
  }


  /* ------------------ DARK MODE TOGGLE ------------------ */
  const THEME_KEY = 'theme';
  const rootEl = document.documentElement;
  const storedTheme = localStorage.getItem(THEME_KEY);
  if (storedTheme) {
    rootEl.setAttribute('data-theme', storedTheme);
  }
  const themeBtn = document.getElementById('theme-toggle');
  if (themeBtn) {
    themeBtn.addEventListener('click', () => {
      const current = rootEl.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
      rootEl.setAttribute('data-theme', current);
      localStorage.setItem(THEME_KEY, current);
    });
  }

  /* ------------------ RESPONSIVE NAV ------------------ */
  const navToggle = document.getElementById('nav-toggle');
  const siteNav   = document.getElementById('site-nav');
  if (navToggle && siteNav) {
    navToggle.addEventListener('click', () => {
      const open = siteNav.classList.toggle('open');
      navToggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }

  /* ------------------ SCROLL ANIMATIONS ------------------ */
  const observer = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        e.target.classList.add('in-view');
        observer.unobserve(e.target);
      }
    });
  }, { threshold: 0.15 });

  document.querySelectorAll('.fade-up').forEach(el => observer.observe(el));

  /* ------------------ STAR RATING UI ------------------ */
  const ratingForm = document.getElementById('ratingForm');
  if (ratingForm) {
    const stars = ratingForm.querySelectorAll('.star-widget .star');
    const ratingInput = document.getElementById('ratingValue');

    const paint = (val) => {
      stars.forEach(s => s.classList.toggle('filled', parseInt(s.dataset.value, 10) <= val));
    };

    stars.forEach(star => {
      star.addEventListener('mouseenter', () => paint(parseInt(star.dataset.value, 10)));
      star.addEventListener('click', () => {
        const v = parseInt(star.dataset.value, 10);
        ratingInput.value = v;
        paint(v);
      });
    });

    const widget = ratingForm.querySelector('.star-widget');
    widget.addEventListener('mouseleave', () => {
      paint(parseInt(ratingInput.value || 0, 10));
    });
  }

  /* ------------------ DYNAMIC FORMSETS ------------------ */
  function wireAdd(prefix) {
    const addBtn = document.getElementById(`add-${prefix}`);
    if (!addBtn) return;

    const totalFormsInput = document.getElementById(`id_${prefix}-TOTAL_FORMS`);
    const container = document.getElementById(`${prefix}-forms`);
    const emptyDiv = document.getElementById(`empty-${prefix}-form`);

    addBtn.addEventListener('click', () => {
      const formIndex = parseInt(totalFormsInput.value, 10);
      let newFormHtml = emptyDiv.innerHTML.replace(/__prefix__/g, formIndex);
      const wrapper = document.createElement('div');
      wrapper.className = 'form-inline fade-up';
      wrapper.innerHTML = newFormHtml;
      container.appendChild(wrapper);
      totalFormsInput.value = formIndex + 1;
      observer.observe(wrapper); // animate new one
    });
  }

  wireAdd('ing');
  wireAdd('step');
});
