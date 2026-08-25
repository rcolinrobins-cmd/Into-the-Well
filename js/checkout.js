/**
 * Into The Well Collective — Square checkout modal
 * Loads the Square Web Payments SDK, attaches a tokenizable card input to
 * the shared checkout dialog (see generator/build_site.py's
 * checkout_modal_markup), and charges it via /api/create-payment. No
 * dependency beyond Square's own SDK, and that's only loaded on pages
 * that actually have the modal in the DOM (gift-card.html, pricing.html),
 * and only once someone actually opens it.
 */
(function () {
  "use strict";

  var modal = document.querySelector("[data-checkout-modal]");
  var items = window.CHECKOUT_ITEMS;
  if (!modal || !items) return;

  var titleEl = modal.querySelector("[data-checkout-title]");
  var priceEl = modal.querySelector("[data-checkout-price]");
  var form = modal.querySelector("[data-checkout-form]");
  var emailInput = modal.querySelector("[data-checkout-email]");
  var cardContainer = modal.querySelector("[data-checkout-card-container]");
  var statusEl = modal.querySelector("[data-checkout-status]");
  var submitBtn = modal.querySelector("[data-checkout-submit]");
  var closeBtn = modal.querySelector("[data-checkout-close]");

  var lastTrigger = null;
  var currentItemKey = null;
  var card = null; // Square's attached, tokenizable card element
  var configPromise = null;
  var cardSetupPromise = null;

  function formatDollars(cents) {
    var amount = cents / 100;
    var hasCents = Math.round(cents) % 100 !== 0;
    return "$" + amount.toFixed(hasCents ? 2 : 0);
  }

  function setStatus(message, tone) {
    statusEl.textContent = message || "";
    if (tone) {
      statusEl.setAttribute("data-tone", tone);
    } else {
      statusEl.removeAttribute("data-tone");
    }
  }

  function setSubmitting(isSubmitting) {
    submitBtn.disabled = isSubmitting;
    var item = currentItemKey && items[currentItemKey];
    submitBtn.textContent = isSubmitting
      ? "Processing…"
      : "Pay" + (item ? " " + formatDollars(item.amountCents) : "");
  }

  function loadConfig() {
    if (!configPromise) {
      configPromise = fetch("/api/config").then(function (res) {
        return res.json();
      });
    }
    return configPromise;
  }

  function loadSquareScript(environment) {
    if (window.Square) return Promise.resolve(window.Square);
    return new Promise(function (resolve, reject) {
      var script = document.createElement("script");
      script.src =
        environment === "production"
          ? "https://web.squarecdn.com/v1/square.js"
          : "https://sandbox.web.squarecdn.com/v1/square.js";
      script.onload = function () { resolve(window.Square); };
      script.onerror = function () {
        reject(new Error("Couldn't load the Square payment library."));
      };
      document.head.appendChild(script);
    });
  }

  // Lazily sets up the Square card input the first time the modal is
  // actually opened, and only once (memoized) — most visits to
  // gift-card.html/pricing.html won't click a checkout button, no reason
  // to load Square's SDK and stand up a payment form before they do.
  function ensureCardAttached() {
    if (cardSetupPromise) return cardSetupPromise;
    cardSetupPromise = loadConfig()
      .then(function (config) {
        if (!config.configured) {
          throw new Error("NOT_CONFIGURED");
        }
        return loadSquareScript(config.environment).then(function (Square) {
          var payments = Square.payments(config.applicationId, config.locationId);
          return payments.card();
        });
      })
      .then(function (cardInstance) {
        return cardInstance.attach(cardContainer).then(function () {
          // Square's card fields render in a cross-origin iframe, so the
          // container can't pick up a normal CSS :focus-within — Square
          // fires these two events specifically so the outer page can
          // still show a focus state on the container around it.
          cardInstance.addEventListener("focusClassAdded", function () {
            cardContainer.classList.add("is-focused");
          });
          cardInstance.addEventListener("focusClassRemoved", function () {
            cardContainer.classList.remove("is-focused");
          });
          card = cardInstance;
          return card;
        });
      });
    return cardSetupPromise;
  }

  function openCheckout(key, trigger) {
    var item = items[key];
    if (!item) return;
    currentItemKey = key;
    lastTrigger = trigger;

    titleEl.textContent = item.label;
    priceEl.textContent = formatDollars(item.amountCents);
    emailInput.disabled = false;
    emailInput.value = "";
    setStatus("");
    setSubmitting(false);

    modal.showModal();

    ensureCardAttached().catch(function (err) {
      var message =
        err && err.message === "NOT_CONFIGURED"
          ? "Online payments aren't set up yet — please contact us to complete this purchase."
          : "We couldn't load the payment form. Please try again shortly.";
      setStatus(message, "error");
      submitBtn.disabled = true;
    });
  }

  document.querySelectorAll("[data-checkout-item]").forEach(function (trigger) {
    trigger.addEventListener("click", function () {
      openCheckout(trigger.getAttribute("data-checkout-item"), trigger);
    });
  });

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    if (!card) {
      setStatus("The payment form hasn't finished loading yet — try again in a second.", "error");
      return;
    }
    if (!emailInput.checkValidity()) {
      emailInput.reportValidity();
      return;
    }

    setStatus("");
    setSubmitting(true);

    card
      .tokenize()
      .then(function (result) {
        if (result.status !== "OK") {
          var detail = result.errors && result.errors[0] && result.errors[0].message;
          throw new Error(detail || "That card couldn't be verified — check the details and try again.");
        }
        return fetch("/api/create-payment", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            itemKey: currentItemKey,
            sourceId: result.token,
            buyerEmail: emailInput.value,
          }),
        }).then(function (res) {
          return res.json().then(function (data) {
            return { ok: res.ok, data: data };
          });
        });
      })
      .then(function (outcome) {
        if (!outcome.ok || !outcome.data.success) {
          throw new Error((outcome.data && outcome.data.error) || "That payment couldn't be completed.");
        }
        // Deliberately left disabled after success (not re-enabled) — this
        // is a one-shot form. A second click of a now-relabeled "Pay"
        // button would tokenize and charge the card again.
        setStatus("Payment successful — thank you! A receipt is on its way to your email.", "success");
        submitBtn.textContent = "Paid";
        emailInput.disabled = true;
      })
      .catch(function (err) {
        setStatus(err.message || "Something went wrong. Please try again.", "error");
        setSubmitting(false);
      });
  });

  function closeCheckout() {
    modal.close();
  }
  closeBtn.addEventListener("click", closeCheckout);
  // Click on the ::backdrop registers as a click on the <dialog> element
  // itself (its only child, .checkout-modal__inner, fills the whole box
  // with padding, so any in-content click targets that instead) — same
  // pattern as the instructor modal in main.js.
  modal.addEventListener("click", function (e) {
    if (e.target === modal) closeCheckout();
  });
  modal.addEventListener("close", function () {
    if (lastTrigger) lastTrigger.focus();
  });
})();
