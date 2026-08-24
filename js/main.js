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

  /* ---------- Instructor bio modal (instructors.html) ----------
   * window.INSTRUCTOR_DATA is embedded by generator/pages.py — one entry
   * per instructor, each with a full bio, specialties, and a list of
   * typical weekly class slots (day + time + class name). "Upcoming
   * Classes" isn't baked into the HTML as fixed dates, which would be
   * wrong the day after deploy — instead nextTwoWeekOccurrences() works
   * out the actual calendar dates for each weekly slot, relative to
   * whichever day the page happens to be viewed. An instructor with no
   * slots (an ownership or guest role, not a weekly class) gets a
   * different message instead of a fabricated schedule.
   */
  var instructorModal = document.querySelector("[data-instructor-modal]");
  var instructorData = window.INSTRUCTOR_DATA;
  if (instructorModal && instructorData) {
    var modalPhoto = instructorModal.querySelector("[data-modal-photo]");
    var modalName = instructorModal.querySelector("[data-modal-name]");
    var modalRole = instructorModal.querySelector("[data-modal-role]");
    var modalBio = instructorModal.querySelector("[data-modal-bio]");
    var modalSpecialties = instructorModal.querySelector(
      "[data-modal-specialties]"
    );
    var modalScheduleNote = instructorModal.querySelector(
      "[data-modal-schedule-note]"
    );
    var modalSchedule = instructorModal.querySelector("[data-modal-schedule]");
    var modalCloseBtn = instructorModal.querySelector("[data-modal-close]");
    var lastInstructorTrigger = null;

    var WEEKDAY_INDEX = { Sun: 0, Mon: 1, Tue: 2, Wed: 3, Thu: 4, Fri: 5, Sat: 6 };

    var nextTwoWeekOccurrences = function (dayAbbr) {
      var targetDay = WEEKDAY_INDEX[dayAbbr];
      var today = new Date();
      today.setHours(0, 0, 0, 0);
      var found = [];
      for (var i = 0; i < 14; i++) {
        var d = new Date(today);
        d.setDate(d.getDate() + i);
        if (d.getDay() === targetDay) found.push(d);
      }
      return found;
    };

    var formatClassDate = function (d) {
      return d.toLocaleDateString("en-US", {
        weekday: "short",
        month: "short",
        day: "numeric",
      });
    };

    var openInstructorModal = function (data, trigger) {
      lastInstructorTrigger = trigger;

      modalPhoto.innerHTML =
        '<div class="img-placeholder" role="img" aria-label="Placeholder: ' +
        data.name +
        '" style="aspect-ratio:1/1; border-radius:50%;"><span>📷 ' +
        data.name +
        "<br><small>Replace with real photo</small></span></div>";
      modalName.textContent = data.name;
      modalRole.textContent = data.role;
      modalBio.textContent = data.bio;
      modalSpecialties.innerHTML = data.specialties
        .map(function (s) {
          return '<li><span class="badge">' + s + "</span></li>";
        })
        .join("");

      if (data.slots.length === 0) {
        modalScheduleNote.textContent =
          "No regular weekly classes on the schedule right now — check Workshops & Events for upcoming sessions with " +
          data.name.split(" ")[0] +
          ".";
        modalSchedule.innerHTML = "";
      } else {
        modalScheduleNote.textContent =
          "Sample schedule for the next two weeks, based on a placeholder weekly time slot — connect a real booking calendar to show live class times.";
        var rows = [];
        data.slots.forEach(function (slot) {
          nextTwoWeekOccurrences(slot.day).forEach(function (date) {
            rows.push({ date: date, time: slot.time, className: slot.className });
          });
        });
        rows.sort(function (a, b) {
          return a.date - b.date;
        });
        modalSchedule.innerHTML = rows
          .map(function (r) {
            return (
              '<li><span class="instructor-modal__schedule-date">' +
              formatClassDate(r.date) +
              " · " +
              r.time +
              "</span><span>" +
              r.className +
              "</span></li>"
            );
          })
          .join("");
      }

      instructorModal.showModal();
    };

    document
      .querySelectorAll("[data-instructor-trigger]")
      .forEach(function (trigger) {
        trigger.addEventListener("click", function () {
          var idx = Number(trigger.getAttribute("data-instructor-trigger"));
          openInstructorModal(instructorData[idx], trigger);
        });
      });

    if (modalCloseBtn) {
      modalCloseBtn.addEventListener("click", function () {
        instructorModal.close();
      });
    }
    // Click on the ::backdrop registers as a click on the <dialog> element
    // itself (its only child, .instructor-modal__inner, fills the whole
    // box with padding, so any in-content click targets that instead).
    instructorModal.addEventListener("click", function (e) {
      if (e.target === instructorModal) instructorModal.close();
    });
    instructorModal.addEventListener("close", function () {
      if (lastInstructorTrigger) lastInstructorTrigger.focus();
    });
  }
})();
