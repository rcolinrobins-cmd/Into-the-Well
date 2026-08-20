# Into The Well Collective — Design System

This is a hand-coded, dependency-free HTML/CSS/JS site — no build step, no framework. Every page is a flat `.html` file that shares two stylesheets and one script. All design decisions live in `css/tokens.css` so re-theming means editing values in one place.

Built **mobile-first**: every layout starts as a single column and adds columns/rows only at wider breakpoints (`min-width` media queries). Always test and judge a change on a phone-width viewport (~375–390px) first, then confirm it still holds up wider.

## Files

- `css/tokens.css` — design tokens: color, type, spacing, radius, shadow, motion. Change values here to re-theme the whole site.
- `css/styles.css` — base styles + reusable components (buttons, cards, nav, accordion, forms, footer) built from those tokens.
- `js/main.js` — mobile nav toggle + accessible FAQ accordion. No dependencies, progressive enhancement (content works even if this fails to load).
- `*.html` — one file per page, sharing the same header/footer markup.

## Color

| Token | Hex | Use |
|---|---|---|
| `--color-cream` | `#FAF6F0` | Page background |
| `--color-cream-deep` | `#F1E9DC` | Alternating section background |
| `--color-charcoal` | `#2E2A26` | Primary text (13.6:1 on cream) |
| `--color-charcoal-soft` | `#5C554D` | Secondary text (6.8:1 on cream) |
| `--color-terracotta` | `#B85C3E` | Primary accent / CTAs (4.6:1 on cream) |
| `--color-sage` | `#6E7B5C` | Secondary accent (5.3:1 on cream) |
| `--color-gold` | `#B08A3E` | Sparing highlight (badges) |
| `--color-blush` / `--color-sage-pale` | — | Soft section/callout backgrounds |

All text/background pairings above meet WCAG AA (4.5:1) at body text size. If you swap in real brand colors, re-check contrast — a contrast checker takes 30 seconds and prevents an accessibility regression.

**This palette is a placeholder**, chosen to fit a warm, inclusive wellness-studio feel since the real brand colors weren't recoverable from the old Wix site (see README). Swap the hex values in `tokens.css` for your actual brand palette whenever you have it — every component will re-theme automatically.

## Typography

- **Display** (`--font-display`): Fraunces — a warm serif for headlines, brand voice.
- **Body** (`--font-body`): Work Sans — a clean humanist sans for readability at small sizes.
- Loaded from Google Fonts in each page's `<head>`. For self-hosting without a Google Fonts dependency, download the two families and swap the `<link>` tags for local `@font-face` rules.
- Type scale runs from `--fs-xs` (13px) to `--fs-3xl` (60px, hero only), all defined in `tokens.css`.

## Spacing

4px base unit, scaling: 4 / 8 / 12 / 16 / 24 / 32 / 48 / 64 / 96px (`--space-1` through `--space-9`). Use these tokens instead of arbitrary pixel values so spacing stays consistent as the site grows.

## Components

- **Buttons** (`.btn`, `.btn--primary`, `.btn--secondary`, `.btn--on-dark`) — pill-shaped, 44px minimum height for touch targets.
- **Cards** (`.card`) — used for classes, instructors, pricing plans (`.plan-card`), events, and partners. All are grid children with `min-width: 0` set deliberately — removing that can reintroduce the overflow bug described below.
- **Nav** (`.site-header`, `.nav__menu`) — sticky header, off-canvas slide-in menu below 960px, inline row above it. Current nav item is marked via `data-page` on `<body>` + JS.
- **Accordion** (`.accordion-item`, used on `faqs.html`) — accessible via `aria-expanded`, keyboard-operable (native `<button>`).
- **Image placeholders** (`.img-placeholder`) — the diagonal-striped boxes throughout the site mark where a real photo should go. Search for `img-placeholder` across the HTML files to find every spot.
- **Notices** (`.notice`) — dashed terracotta boxes flagging things that need a decision or integration before launch (payment provider, booking widget, form backend, etc.). Search for `class="notice"` to find every one and resolve them before going live.

## A layout bug worth knowing about (if you edit the grids)

Any `.grid` with cards containing `.img-placeholder` (which uses `aspect-ratio`) can silently blow out past its container — a classic CSS Grid issue where a grid item's implicit `min-width: auto` lets its content force the column wider than its fair share, overflowing the page horizontally. The fix already in place is `.grid > * { min-width: 0; }` plus the same on `.card` and `.img-placeholder`. If you add a new card-grid section and see unexpected horizontal scroll, this is almost certainly why — make sure the new grid items also get `min-width: 0`.

## Known placeholders / not-yet-wired functionality

- **Booking**: `book-online.html` has a placeholder for a booking calendar. The old Wix booking system doesn't transfer — pick a provider (Momence, Mindbody, Vagaro, Acuity, etc.) and embed its widget.
- **Membership checkout**: `pricing.html`'s "Choose Plan" buttons don't charge anything yet. Needs a payment/subscription provider (Stripe Billing or your booking provider's built-in billing).
- **Gift cards**: `gift-card.html` needs an e-commerce integration to actually sell and deliver codes.
- **Contact form**: `contact.html`'s form has no backend. Wire it to a form service (Formspree, Netlify Forms) or your own email handler.
- **Photography**: every `.img-placeholder` box needs a real photo. See README for how to get them out of the old Wix site.
- **Instructor bios & class descriptions**: the live site didn't expose these to the page text we could extract — the one-line descriptions on `classes.html`/`instructors.html` are neutral placeholder drafts, not the studio's real copy.
- **Studio hours**: not published anywhere on the old site — add them to the homepage and contact page.

## Navigation structure

The primary nav was trimmed to 7 items (Home, Classes, Instructors, Pricing, Events, Rent The Space, Contact) plus a "Book a Class" CTA button, with everything else (Gift Cards, Free for Members, Women's Wellness Series, Partnership Workshops/Programs, Current Partners, FAQs) reachable from the footer sitemap and in-page cross-links. The original site exposed most of these as top-level nav items — a nav that long doesn't fit comfortably even on a 1200px-wide screen without shrinking or wrapping. This is a deliberate information-architecture change; see the upcoming UX audit for the full reasoning.
