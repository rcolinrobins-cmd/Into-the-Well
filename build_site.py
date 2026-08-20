#!/usr/bin/env python3
"""
Static-site generator for Into The Well Collective.
Produces plain, dependency-free HTML files from shared header/footer
templates + per-page content, so the whole site stays consistent and
easy to hand-edit afterward (each output file is just flat HTML).
"""
import os

# Output directory: the deployable "site/" folder next to this script.
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "site")

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


def placeholder(label, ratio="16/10", radius="var(--radius-md)"):
    return (
        f'<div class="img-placeholder" role="img" aria-label="Placeholder: {label}" '
        f'style="aspect-ratio:{ratio}; border-radius:{radius};">'
        f'<span>📷 {label}<br><small>Replace with real photo</small></span></div>'
    )


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
      <span class="nav__logo" aria-hidden="true">ITW</span>
      <span class="nav__brand-text">Into The Well Collective</span>
    </a>
    <button class="nav__toggle" data-nav-toggle aria-expanded="false" aria-controls="primary-nav" aria-label="Open menu">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg>
    </button>
    <nav class="nav__menu" id="primary-nav" data-nav-menu aria-label="Primary">
      <button class="nav__close btn btn--sm btn--secondary" data-nav-close aria-label="Close menu">Close ✕</button>
      <ul style="display:contents;">
        {nav_links}
      </ul>
      <a class="btn btn--primary nav__cta" href="{CTA[0]}">{CTA[1]}</a>
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
        <p style="margin-top:var(--space-3); opacity:.85;">A movement studio, community &amp; event space in Garland, TX &mdash; built for inclusion, whole-body wellness, and self-care for all humans.</p>
        <div class="footer-social">
          <a href="{INSTAGRAM}" aria-label="Into The Well Collective on Instagram" target="_blank" rel="noopener">Instagram</a>
          <a href="{FACEBOOK}" aria-label="Into The Well Collective on Facebook" target="_blank" rel="noopener">Facebook</a>
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
      <span>Site rebuilt for self-hosting &mdash; no longer on Wix.</span>
    </div>
  </div>
</footer>

<script src="js/main.js"></script>
</body>
</html>
"""


def write(filename, title, description, body, extra_head=""):
    html = base_page(filename, title, description, body, extra_head)
    path = os.path.join(ROOT, filename)
    with open(path, "w") as f:
        f.write(html)
    print("wrote", filename)
