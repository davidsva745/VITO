document.addEventListener("DOMContentLoaded", function () {

  if (window.AOS) AOS.init();

  window.toggleAll = function (open) {
    document.querySelectorAll("details").forEach((detail) => {
      detail.open = open;
    });
  };

  const hamburger = document.querySelector(".hamburger");
  const navLinks = document.querySelector(".nav-links");

  if (hamburger && navLinks) {
    hamburger.addEventListener("click", () => {
      navLinks.classList.toggle("open");
    });
  }
});
