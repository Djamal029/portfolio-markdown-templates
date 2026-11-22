/* Petit script sans dépendance : thème clair/sombre, filtres de projets,
   menu mobile et surlignage de la section visible. Le site reste lisible sans JavaScript. */
(function () {
  "use strict";
  var root = document.documentElement;

  // Thème : le choix est mémorisé dans le navigateur du visiteur.
  function currentTheme() {
    var forced = root.getAttribute("data-theme");
    if (forced) return forced;
    return window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
  }
  var toggles = document.querySelectorAll("[data-theme-toggle]");
  function syncToggles() {
    toggles.forEach(function (t) { t.setAttribute("aria-pressed", currentTheme() === "dark" ? "true" : "false"); });
  }
  syncToggles();
  toggles.forEach(function (toggle) {
    toggle.addEventListener("click", function () {
      var next = currentTheme() === "dark" ? "light" : "dark";
      root.setAttribute("data-theme", next);
      syncToggles();
      try { localStorage.setItem("theme", next); } catch (e) { /* stockage indisponible */ }
    });
  });

  // Filtres Académique / Personnel.
  var filters = document.querySelector("[data-filters]");
  var grid = document.querySelector("[data-project-grid]");
  if (filters && grid) {
    var empty = document.querySelector("[data-empty]");
    filters.addEventListener("click", function (event) {
      var button = event.target.closest("[data-filter]");
      if (!button) return;
      var value = button.getAttribute("data-filter");
      filters.querySelectorAll("[data-filter]").forEach(function (b) {
        b.setAttribute("aria-pressed", b === button ? "true" : "false");
      });
      var shown = 0;
      grid.querySelectorAll("[data-category]").forEach(function (card) {
        var visible = value === "all" || card.getAttribute("data-category") === value;
        card.hidden = !visible;
        if (visible) shown += 1;
      });
      if (empty) empty.hidden = shown > 0;
    });
  }

  // Menu mobile (modèle B).
  var menuButton = document.querySelector("[data-menu-toggle]");
  var menu = document.getElementById("site-menu");
  if (menuButton && menu) {
    menuButton.addEventListener("click", function () {
      var open = menuButton.getAttribute("aria-expanded") === "true";
      menuButton.setAttribute("aria-expanded", open ? "false" : "true");
      menu.classList.toggle("is-open", !open);
    });
    // Ferme le menu après un clic sur un lien (pages à une seule section).
    menu.addEventListener("click", function (event) {
      if (event.target.closest("a")) {
        menuButton.setAttribute("aria-expanded", "false");
        menu.classList.remove("is-open");
      }
    });
    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape" && menu.classList.contains("is-open")) {
        menuButton.setAttribute("aria-expanded", "false");
        menu.classList.remove("is-open");
        menuButton.focus();
      }
    });
  }

  // Surligne dans la navigation la section en cours de lecture (modèles A et C).
  var spyLinks = document.querySelectorAll("[data-spy]");
  if (spyLinks.length && "IntersectionObserver" in window) {
    var byId = {};
    spyLinks.forEach(function (link) {
      var key = link.getAttribute("data-spy");
      (byId[key] = byId[key] || []).push(link);
    });
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        spyLinks.forEach(function (l) { l.removeAttribute("aria-current"); });
        (byId[entry.target.id] || []).forEach(function (link) {
          link.setAttribute("aria-current", "true");
          var nav = link.closest("nav");
          if (nav && nav.scrollWidth > nav.clientWidth) nav.scrollLeft = link.offsetLeft - 16;
        });
      });
    }, { rootMargin: "-45% 0px -50% 0px" });
    var hero = document.getElementById("home");
    if (hero) observer.observe(hero);
    Object.keys(byId).forEach(function (id) {
      var section = document.getElementById(id);
      if (section) observer.observe(section);
    });
  }
})();

/* Apparitions douces au défilement (désactivées si l'utilisateur réduit les animations). */
(function () {
  if (!("IntersectionObserver" in window)) return;
  if (window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
  var items = document.querySelectorAll(".section-head, .tl-item, .project-card, .skill-group, .edu-item, .contact-panel, .about-grid > *");
  document.documentElement.classList.add("js-reveal");
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); } });
  }, { rootMargin: "0px 0px -6% 0px" });
  items.forEach(function (el) { el.classList.add("reveal"); io.observe(el); });
})();
