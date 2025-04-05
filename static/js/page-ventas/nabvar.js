document.addEventListener("DOMContentLoaded", function () {
    const currentPath = window.location.pathname;
    const allLinks = document.querySelectorAll(".btn-toggle-nav a");

    allLinks.forEach((link) => {
      if (link.getAttribute("href") === currentPath) {
        link.classList.add("active");

        const collapseElement = link.closest(".collapse");
        if (collapseElement) {
          const toggleButton = document.querySelector(
            `[data-bs-target="#${collapseElement.id}"]`
          );
          if (
            toggleButton &&
            toggleButton.classList.contains("collapsed")
          ) {
            toggleButton.classList.remove("collapsed");
            toggleButton.setAttribute("aria-expanded", "true");
            collapseElement.classList.add("show");
          }
        }
      }
    });

    const toggleButtons = document.querySelectorAll(".btn-toggle");
    toggleButtons.forEach((button) => {
      button.addEventListener("mouseenter", function () {
        this.style.transition = "all 0.3s ease";
      });
      button.addEventListener("mouseleave", function () {
        this.style.transition = "all 0.3s ease";
      });
    });

    const sidebar = document.querySelector(".sidebar");
    if (sidebar) {
      sidebar.style.transition = "all 0.3s ease";
    }

    document
      .querySelectorAll('[data-bs-toggle="collapse"]')
      .forEach((button) => {
        button.addEventListener("click", function () {
          const target = document.querySelector(
            this.getAttribute("data-bs-target")
          );
          if (target) {
            target.style.transition = "height 0.3s ease";
          }
        });
      });
  });