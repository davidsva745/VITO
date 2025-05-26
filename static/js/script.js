document.addEventListener("DOMContentLoaded", function () {
  // Inicializace AOS animací (pokud jsou dostupné)
  if (window.AOS) AOS.init();

  // Funkce pro rozbalení / sbalení všech <details>
  window.toggleAll = function (open) {
    document.querySelectorAll("details").forEach((detail) => {
      detail.open = open;
    });
  };

  // Hamburger menu pro mobilní zařízení
  const hamburger = document.querySelector(".hamburger");
  const navLinks = document.querySelector(".nav-links");

  if (hamburger && navLinks) {
    hamburger.addEventListener("click", () => {
      navLinks.classList.toggle("open");
    });
  }

  // Plynulé sbalování/rozbalování details (volitelné – efekt)
  document.querySelectorAll('details').forEach(detail => {
    const content = detail.querySelector('ul');
    if (!content) return;

    content.style.transition = 'max-height 0.4s ease';
    content.style.overflow = 'hidden';
    if (!detail.open) content.style.maxHeight = '0';

    detail.addEventListener('toggle', () => {
      if (detail.open) {
        content.style.maxHeight = content.scrollHeight + 'px';
      } else {
        content.style.maxHeight = '0';
      }
    });
  });
});
