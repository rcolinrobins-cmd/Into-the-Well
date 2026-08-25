#!/usr/bin/env python3
"""
Static-site generator for Into The Well Collective.
Produces plain, dependency-free HTML files from shared header/footer
templates + per-page content, so the whole site stays consistent and
easy to hand-edit afterward (each output file is just flat HTML).
"""
import json
import os
import re

# Output directory: the repo root (one level up from this script), so the
# deployable site sits at the top of the repo — Vercel/Netlify/GitHub Pages
# all expect index.html at the repo root by default with no extra config.
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

SITE_NAME = "Into The Well Collective"
PHONE = "214-726-5218"
PHONE_TEL = "+12147265218"
EMAIL = "bewell@intothewellcollective.com"
ADDRESS = "604 West State Street, Garland, TX 75040"
MAPS_URL = "https://maps.google.com/?q=604+West+State+Street,+Garland,+TX+75040"
INSTAGRAM = "https://www.instagram.com/intothewell_collective/"
FACEBOOK = "https://www.facebook.com/intothewellcollective"
TAGLINE = "You are loved. You are really, really loved."

NAV = [
    ("index.html", "Home"),
    ("classes.html", "Classes"),
    ("instructors.html", "Instructors"),
    ("pricing.html", "Pricing"),
    ("workshops-events.html", "Events"),
    ("rent-the-space.html", "Rent The Space"),
    ("contact.html", "Contact"),
]
CTA = ("book-online.html", "Book a Class")

ICON_CHEVRON = '<svg class="accordion-trigger__icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M12 5v14M5 12h14"/></svg>'
ICON_PIN = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0Z"/><circle cx="12" cy="10" r="3"/></svg>'
ICON_PHONE = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.127.96.362 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.338 1.85.573 2.81.7A2 2 0 0 1 22 16.92Z"/></svg>'
ICON_MAIL = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 6L2 7"/></svg>'
ICON_INSTAGRAM = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><rect x="2" y="2" width="20" height="20" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37Z"/><line x1="17.5" y1="6.5" x2="17.51" y2="6.5"/></svg>'
ICON_FACEBOOK = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"/></svg>'


def placeholder(label, ratio="16/10", radius="var(--radius-md)"):
    return (
        f'<div class="img-placeholder" role="img" aria-label="Placeholder: {label}" '
        f'style="aspect-ratio:{ratio}; border-radius:{radius};">'
        f'<span>📷 {label}<br><small>Replace with real photo</small></span></div>'
    )


def image_path_or_none(rel_path_no_ext, extensions=("jpg", "jpeg", "png", "webp")):
    """Looks for assets/<rel_path_no_ext>.<ext> on disk, in that extension
    order, and returns the relative path if found, else None. Lets photos
    be added one at a time — drop a correctly-named file into assets/ and
    regenerate, no code change needed — rather than requiring every image
    to land before any of them can go live."""
    for ext in extensions:
        rel = f"{rel_path_no_ext}.{ext}"
        if os.path.exists(os.path.join(ROOT, "assets", rel)):
            return f"assets/{rel}"
    return None


def image_or_placeholder(label, rel_path_no_ext, ratio="16/10", radius="var(--radius-md)", size=None):
    """Drop-in replacement for placeholder() that renders a real <img> if
    a matching file exists in assets/ (see image_path_or_none), falling
    back to the dashed placeholder box otherwise. `size` sets a fixed
    width/height in px (for fixed-size avatars); omit it to fill the
    parent's width instead (for content-width photos)."""
    src = image_path_or_none(rel_path_no_ext)
    if not src:
        return placeholder(label, ratio=ratio, radius=radius)
    size_style = f"width:{size}px; height:{size}px;" if size else "width:100%;"
    return (
        f'<img src="{src}" alt="{label}" loading="lazy" '
        f'style="{size_style} aspect-ratio:{ratio}; border-radius:{radius}; object-fit:cover; display:block;">'
    )


def checkout_modal_markup(items):
    """Shared Square checkout dialog — append this to the body of any page
    with a [data-checkout-item] trigger button (see js/checkout.js). Only
    needed on gift-card.html and pricing.html today; not a big enough
    chunk of markup to bother making conditional per-page in base_page().

    `items` (CHECKOUT_ITEMS from pages.py) is embedded as window data so
    the client can show a label/price without re-deriving it — same
    pattern as window.INSTRUCTOR_DATA on instructors.html. This is the
    display copy only; api/create-payment.js re-looks-up the real price
    server-side from data/checkout-items.json rather than trusting it."""
    return f"""
<script>window.CHECKOUT_ITEMS = {json.dumps(items)};</script>
<dialog class="checkout-modal" data-checkout-modal aria-labelledby="checkout-modal-title">
  <div class="checkout-modal__inner">
    <button type="button" class="checkout-modal__close btn btn--sm btn--secondary" data-checkout-close autofocus aria-label="Close">Close &#10005;</button>
    <h2 id="checkout-modal-title" data-checkout-title></h2>
    <p class="plan-card__price" data-checkout-price></p>
    <form data-checkout-form novalidate>
      <div class="form-field">
        <label for="checkout-email">Email <span class="text-muted">(for your receipt)</span></label>
        <input type="email" id="checkout-email" name="email" data-checkout-email required autocomplete="email">
      </div>
      <div class="form-field">
        <label id="checkout-card-label">Card details</label>
        <div class="checkout-modal__card" id="checkout-card-container" data-checkout-card-container aria-labelledby="checkout-card-label"></div>
      </div>
      <p class="checkout-modal__status" data-checkout-status role="status" aria-live="polite"></p>
      <button type="submit" class="btn btn--primary btn--block" data-checkout-submit>Pay</button>
    </form>
  </div>
</dialog>"""


def base_page(filename, title, description, body, extra_head=""):
    nav_links = "\n".join(
        f'<li><a href="{href}">{label}</a></li>' for href, label in NAV
    )
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} | {SITE_NAME}</title>
<meta name="description" content="{description}">
<meta property="og:title" content="{title} | {SITE_NAME}">
<meta property="og:description" content="{description}">
<meta property="og:type" content="website">
<meta name="theme-color" content="#B85C3E">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600&family=Work+Sans:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="css/tokens.css">
<link rel="stylesheet" href="css/styles.css">
{extra_head}</head>
<body data-page="{filename}">
<a class="skip-link" href="#main">Skip to content</a>

<header class="site-header">
  <div class="container nav">
    <a class="nav__brand" href="index.html">
      <span class="nav__brand-text">Into the Well</span>
    </a>
    <button class="nav__toggle" data-nav-toggle aria-expanded="false" aria-controls="primary-nav" aria-label="Open menu">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg>
    </button>
    <nav class="nav__menu" id="primary-nav" data-nav-menu aria-label="Primary">
      <span class="nav__indicator" aria-hidden="true"></span>
      <button class="nav__close btn btn--sm btn--secondary" data-nav-close aria-label="Close menu">Close ✕</button>
      <ul data-nav-links style="display:contents;">
        {nav_links}
      </ul>
      <a class="btn btn--primary btn--sm nav__cta" href="{CTA[0]}">{CTA[1]}</a>
    </nav>
    <div class="nav__scrim" data-nav-scrim></div>
  </div>
</header>

<main id="main">
{body}
</main>

<footer class="site-footer">
  <div class="container">
    <h2 class="visually-hidden">Site footer</h2>
    <div class="footer-grid">
      <div>
        <p class="footer-tagline">{TAGLINE}</p>
        <p class="footer-seo">Into The Well Collective is a yoga, pilates, and barre studio in Garland, TX, serving Garland, Dallas, and the greater Dallas-Fort Worth area with inclusive yoga classes, pilates, barre, and strength training for every body and every level, plus wellness workshops and community events.</p>
        <div class="footer-social">
          <a href="{INSTAGRAM}" aria-label="Into The Well Collective on Instagram" target="_blank" rel="noopener">{ICON_INSTAGRAM}</a>
          <a href="{FACEBOOK}" aria-label="Into The Well Collective on Facebook" target="_blank" rel="noopener">{ICON_FACEBOOK}</a>
        </div>
      </div>
      <div>
        <h3>Explore</h3>
        <ul>
          <li><a href="classes.html">Classes</a></li>
          <li><a href="instructors.html">Instructors</a></li>
          <li><a href="pricing.html">Pricing &amp; Membership</a></li>
          <li><a href="gift-card.html">Gift Cards</a></li>
          <li><a href="book-online.html">Book a Class</a></li>
        </ul>
      </div>
      <div>
        <h3>Studio</h3>
        <ul>
          <li><a href="workshops-events.html">Workshops &amp; Events</a></li>
          <li><a href="womens-wellness.html">Women's Wellness Series</a></li>
          <li><a href="rent-the-space.html">Rent The Space</a></li>
          <li><a href="partnership-programs.html">Partner With Us</a></li>
          <li><a href="current-partners.html">Current Partners</a></li>
          <li><a href="faqs.html">FAQs</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>&copy; 2026 {SITE_NAME}. {ADDRESS} &middot; {PHONE} &middot; {EMAIL}</span>
    </div>
  </div>
</footer>

<script src="js/main.js"></script>
<script src="js/checkout.js"></script>
</body>
</html>
"""


def write(filename, title, description, body, extra_head=""):
    html = base_page(filename, title, description, body, extra_head)
    path = os.path.join(ROOT, filename)
    with open(path, "w") as f:
        f.write(html)
    print("wrote", filename)


def slugify(text):
    """'Unlimited Monthly Membership' -> 'unlimited-monthly-membership' —
    used to build stable checkout item keys from display names, so a plan
    renamed later gets a new (not silently mismatched) key rather than a
    hand-picked one going stale next to it."""
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug


def price_to_cents(price):
    """'$109' -> 10900. Only called on the fixed-price gift card/plan
    strings above, never on user input."""
    return round(float(price.replace("$", "").replace(",", "")) * 100)


def write_checkout_items(items, rel_path="data/checkout-items.json"):
    """Writes the single source of truth for what the Square checkout
    modal is allowed to charge: item key -> {label, amountCents, recurring}.
    Generated from the same GIFT_AMOUNTS/TIER_PLANS/LIST_PLANS tuples that
    render the on-page prices, so this can never drift from what a visitor
    actually sees. Read at request time by api/create-payment.js, which
    looks up the authoritative amount server-side rather than trusting
    whatever the client posts — see that file for why."""
    path = os.path.join(ROOT, rel_path)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(items, f, indent=2)
        f.write("\n")
    print("wrote", rel_path)
