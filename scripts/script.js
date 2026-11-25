document.addEventListener('DOMContentLoaded', () => {
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- Reveal on scroll (replaces AOS) ---------- */
  const revealEls = document.querySelectorAll('[data-aos]');
  if ('IntersectionObserver' in window && !reduceMotion) {
    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add('is-visible');
            io.unobserve(entry.target);
          }
        });
      },
      { rootMargin: '0px 0px -8% 0px', threshold: 0.05 },
    );
    // Content already on screen at load (the hero) never waits on the observer.
    const inView = [];
    revealEls.forEach((el) => {
      if (el.getBoundingClientRect().top < window.innerHeight) inView.push(el);
      else io.observe(el);
    });
    const showInView = () => inView.forEach((el) => el.classList.add('is-visible'));
    requestAnimationFrame(() => requestAnimationFrame(showInView));
    setTimeout(showInView, 150);
  } else {
    revealEls.forEach((el) => el.classList.add('is-visible'));
  }

  /* ---------- Navbar: transparent over hero, solid after ---------- */
  const navbar = document.getElementById('navbar');
  const hero = document.getElementById('home');
  const bookBar = document.getElementById('mobile-book-bar');
  const bookSection = document.getElementById('book-now-section');

  let bookSectionVisible = false;
  const onScroll = () => {
    const heroBottom = hero ? hero.offsetHeight - 80 : 200;
    const y = window.scrollY;
    navbar?.classList.toggle('is-scrolled', y > 40);
    bookBar?.classList.toggle('is-visible', y > heroBottom && !bookSectionVisible);
  };

  if (bookSection && 'IntersectionObserver' in window) {
    new IntersectionObserver(([entry]) => {
      bookSectionVisible = entry.isIntersecting;
      onScroll();
    }).observe(bookSection);
  }

  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* ---------- Mobile menu ---------- */
  const hamburger = document.getElementById('hamburger');
  const navOptions = document.getElementById('navbar-option');

  const setMenu = (open) => {
    navOptions.classList.toggle('responsive', open);
    hamburger.classList.toggle('is-active', open);
    navbar.classList.toggle('menu-open', open);
    hamburger.setAttribute('aria-expanded', String(open));
  };

  if (hamburger && navOptions) {
    hamburger.addEventListener('click', () => {
      setMenu(!navOptions.classList.contains('responsive'));
    });
    navOptions.querySelectorAll('a').forEach((link) => {
      link.addEventListener('click', () => setMenu(false));
    });
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && navOptions.classList.contains('responsive')) {
        setMenu(false);
        hamburger.focus();
      }
    });
  }

  /* ---------- Lightbox ---------- */
  const dialog = document.getElementById('lightbox');
  if (!dialog || typeof dialog.showModal !== 'function') return;

  const imgEl = dialog.querySelector('.lightbox__img');
  const caption = dialog.querySelector('.lightbox__caption');
  let photos = [];
  let index = 0;

  const show = (i) => {
    index = (i + photos.length) % photos.length;
    const src = photos[index];
    // Always show the largest version in the viewer, not the grid thumbnail.
    const set = (src.getAttribute('srcset') || '').split(',').map((x) => x.trim().split(' ')[0]);
    imgEl.src = set[set.length - 1] || src.currentSrc || src.src;
    imgEl.alt = src.alt;
    caption.textContent = `${src.alt} · ${index + 1} / ${photos.length}`;
  };

  const open = (group, i) => {
    photos = group;
    show(i);
    dialog.showModal();
    document.body.classList.add('no-scroll');
  };

  // Each gallery (Good To Know grid, main gallery) is its own set.
  document.querySelectorAll('.plan-contents, .grid-images').forEach((gallery) => {
    const group = Array.from(gallery.querySelectorAll('img'));
    group.forEach((photo, i) => {
      const card = photo.parentElement;
      card.setAttribute('role', 'button');
      card.setAttribute('tabindex', '0');
      card.setAttribute('aria-label', `View larger: ${photo.alt}`);
      card.addEventListener('click', () => open(group, i));
      card.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          open(group, i);
        }
      });
    });
  });

  dialog.querySelector('.lightbox__close').addEventListener('click', () => dialog.close());
  dialog.querySelector('.lightbox__nav--prev').addEventListener('click', () => show(index - 1));
  dialog.querySelector('.lightbox__nav--next').addEventListener('click', () => show(index + 1));
  dialog.addEventListener('close', () => document.body.classList.remove('no-scroll'));

  // Click on backdrop closes
  dialog.addEventListener('click', (e) => {
    if (e.target === dialog) dialog.close();
  });

  dialog.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowRight') show(index + 1);
    if (e.key === 'ArrowLeft') show(index - 1);
  });

  // Swipe on touch
  let startX = null;
  dialog.addEventListener('touchstart', (e) => {
    if (e.touches.length === 1) startX = e.touches[0].clientX;
  }, { passive: true });
  dialog.addEventListener('touchend', (e) => {
    if (startX === null) return;
    const dx = e.changedTouches[0].clientX - startX;
    if (Math.abs(dx) > 40) show(index + (dx < 0 ? 1 : -1));
    startX = null;
  });
});
