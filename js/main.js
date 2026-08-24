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

  /* ---------- Desktop nav: sliding hover/focus underline ----------
   * One shared element (.nav__indicator) animates its position and width to
   * sit under whichever primary-nav link is hovered or keyboard-focused,
   * and glides back to the current page's link when the pointer/focus
   * leaves the nav. Deliberately scoped to the links inside [data-nav-links]
   * only — the "Book a Class" pill CTA is a filled button, not a text link,
   * and doesn't want an underline sliding under it too.
   */
  var indicator = document.querySelector(".nav__indicator");
  var navLinks = menu ? Array.prototype.slice.call(menu.querySelectorAll("[data-nav-links] a")) : [];
  if (indicator && navLinks.length) {
    var desktopMq = window.matchMedia("(min-width: 1180px)");

    var moveIndicatorTo = function (el) {
      if (!el || !desktopMq.matches) {
        indicator.classList.remove("is-visible");
        return;
      }
      var menuRect = menu.getBoundingClientRect();
      var elRect = el.getBoundingClientRect();
      indicator.style.transform = "translateX(" + (elRect.left - menuRect.left) + "px)";
      indicator.style.width = elRect.width + "px";
      indicator.classList.add("is-visible");
    };
    var resetToCurrentLink = function () {
      moveIndicatorTo(menu.querySelector('a[aria-current="page"]'));
    };

    navLinks.forEach(function (a) {
      a.addEventListener("mouseenter", function () { moveIndicatorTo(a); });
      a.addEventListener("focus", function () { moveIndicatorTo(a); });
    });
    menu.addEventListener("mouseleave", resetToCurrentLink);
    menu.addEventListener("focusout", function (e) {
      if (!menu.contains(e.relatedTarget)) resetToCurrentLink();
    });
    // Reposition on resize/orientation change and once webfonts finish
    // loading (both can shift link positions out from under the indicator).
    window.addEventListener("resize", resetToCurrentLink);
    desktopMq.addEventListener("change", resetToCurrentLink);
    if (document.fonts && document.fonts.ready) {
      document.fonts.ready.then(resetToCurrentLink);
    }
    resetToCurrentLink();
  }

  /* ---------- Header: light shadow once the page has scrolled ----------
   * The header has a permanent solid background; this just adds a small
   * lift (box-shadow, see styles.css) once content has actually scrolled
   * underneath it, so the header reads as "above" the page instead of
   * just another flat section.
   */
  var header = document.querySelector(".site-header");
  if (header) {
    var applyScrollState = function () {
      header.classList.toggle("is-scrolled", window.scrollY > 24);
    };
    window.addEventListener("scroll", applyScrollState, { passive: true });
    applyScrollState();
  }

  /* ---------- Class filter (classes.html) ----------
   * Every .class-card carries a data-category set at build time (see
   * generator/pages.py). Clicking a filter chip shows only the cards
   * matching that category — "all" shows everything — and updates the
   * live-region count so screen reader users get the result too, not just
   * a visual change. Cards are hidden via the `hidden` attribute rather
   * than a CSS class so they're pulled out of the accessibility tree, not
   * just hidden visually.
   */
  var filterBar = document.querySelector("[data-class-filter]");
  if (filterBar) {
    var filterButtons = Array.prototype.slice.call(
      filterBar.querySelectorAll("[data-filter]")
    );
    var classCards = Array.prototype.slice.call(
      document.querySelectorAll(".class-card")
    );
    var countEl = document.querySelector("[data-class-count]");

    var applyClassFilter = function (filter) {
      var visibleCount = 0;
      classCards.forEach(function (card) {
        var isMatch = filter === "all" || card.dataset.category === filter;
        card.hidden = !isMatch;
        if (isMatch) visibleCount += 1;
      });
      if (countEl) {
        countEl.textContent =
          "Showing " + visibleCount + " of " + classCards.length + " classes";
      }
    };

    filterButtons.forEach(function (button) {
      button.addEventListener("click", function () {
        filterButtons.forEach(function (b) {
          b.classList.remove("is-active");
          b.setAttribute("aria-pressed", "false");
        });
        button.classList.add("is-active");
        button.setAttribute("aria-pressed", "true");
        applyClassFilter(button.dataset.filter);
      });
    });

    applyClassFilter("all");
  }
})();
