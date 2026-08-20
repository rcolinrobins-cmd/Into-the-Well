/**
 * Into The Well Collective — shared site behavior
 * Mobile nav toggle + accessible accordion (FAQ page).
 * No dependencies. Progressive enhancement: all content is
 * visible/usable in the HTML even if this file fails to load.
 */
(function () {
  "use strict";

  /* ---------- Mobile nav ---------- */
  var toggle = document.querySelector("[data-nav-toggle]");
  var menu = document.querySelector("[data-nav-menu]");
  var closeBtn = document.querySelector("[data-nav-close]");
  var scrim = document.querySelector("[data-nav-scrim]");
  // The page content sitting under the dimmed scrim while the menu is open
  // (the header's brand/toggle stay above the scrim and stay usable) —
  // hidden from keyboard/screen-reader users so Tab can't silently leave
  // the menu and land on content stacked underneath it.
  var outsideMenu = document.querySelectorAll("main, .site-footer");
  var focusableSelector = 'a[href], button:not([disabled]), input, textarea, select, [tabindex]:not([tabindex="-1"])';

  function openNav() {
    menu.classList.add("is-open");
    scrim.classList.add("is-open");
    toggle.setAttribute("aria-expanded", "true");
    outsideMenu.forEach(function (el) { el.setAttribute("inert", ""); });
    menu.querySelector("a")?.focus();
    document.body.style.overflow = "hidden";
  }
  function closeNav() {
    menu.classList.remove("is-open");
    scrim.classList.remove("is-open");
    toggle.setAttribute("aria-expanded", "false");
    outsideMenu.forEach(function (el) { el.removeAttribute("inert"); });
    document.body.style.overflow = "";
    toggle.focus(); // return focus to the control that opened the menu
  }
  if (toggle && menu) {
    toggle.addEventListener("click", function () {
      var isOpen = menu.classList.contains("is-open");
      isOpen ? closeNav() : openNav();
    });
    closeBtn && closeBtn.addEventListener("click", closeNav);
    scrim && scrim.addEventListener("click", closeNav);
    document.addEventListener("keydown", function (e) {
      if (e.key !== "Escape" && e.key !== "Tab") return;
      if (!menu.classList.contains("is-open")) return;
      if (e.key === "Escape") { closeNav(); return; }
      // Trap Tab/Shift+Tab inside the open menu (it's the only unhidden
      // region of the page while open, but belt-and-suspenders for browsers
      // without `inert` support).
      var focusable = menu.querySelectorAll(focusableSelector);
      if (!focusable.length) return;
      var first = focusable[0], last = focusable[focusable.length - 1];
      if (e.shiftKey && document.activeElement === first) {
        e.preventDefault(); last.focus();
      } else if (!e.shiftKey && document.activeElement === last) {
        e.preventDefault(); first.focus();
      }
    });
    // Close menu when a link is chosen (mobile)
    menu.querySelectorAll("a").forEach(function (a) {
      a.addEventListener("click", closeNav);
    });
  }

  /* ---------- Accessible accordion (FAQs) ---------- */
  document.querySelectorAll("[data-accordion] .accordion-trigger").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var item = btn.closest(".accordion-item");
      var expanded = btn.getAttribute("aria-expanded") === "true";
      btn.setAttribute("aria-expanded", String(!expanded));
      item.classList.toggle("is-open", !expanded);
    });
  });

  /* ---------- Mark current nav link for a11y + styling ---------- */
  var current = document.body.getAttribute("data-page");
  if (current) {
    document.querySelectorAll('.nav__menu a[href="' + current + '"]').forEach(function (a) {
      a.setAttribute("aria-current", "page");
    });
  }
})();
