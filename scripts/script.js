document.addEventListener('DOMContentLoaded', function () {
  if (window.AOS) {
    AOS.init({ once: true, duration: 700 });
  }

  const hamburger = document.getElementById('hamburger');
  const navOptions = document.getElementById('navbar-option');

  if (hamburger && navOptions) {
    hamburger.addEventListener('click', function () {
      const isOpen = navOptions.classList.toggle('responsive');
      hamburger.classList.toggle('is-active', isOpen);
      hamburger.setAttribute('aria-expanded', String(isOpen));
    });

    navOptions.querySelectorAll('a').forEach(function (link) {
      link.addEventListener('click', function () {
        navOptions.classList.remove('responsive');
        hamburger.classList.remove('is-active');
        hamburger.setAttribute('aria-expanded', 'false');
      });
    });
  }
});
