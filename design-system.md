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
| `--color-cream` | `#FCFAF6` | Page background |
| `--color-cream-deep` | `#F3EDE2` | Alternating section background |
| `--color-black` | `#1A1A1A` | Headings (`h1`–`h3`, `.font-display`) — a web-friendly near-black, deliberately not pure `#000` |
| `--color-charcoal` | `#003562` | Primary text (13.7:1 on cream) |
| `--color-charcoal-soft` | `#2E5675` | Secondary text (7.8:1 on cream, 4.8:1 on blush) |
| `--color-terracotta` | `#D03D11` | Primary accent / CTAs (4.8:1 on cream) |
| `--color-terracotta-dk` | `#9B2A08` | Hover/active state, small text, badges, price accents (7.7:1 on cream, 4.7:1 on blush) |
| `--color-sage` | `#6E7B5C` | Secondary accent (5.3:1 on cream) |
| `--color-gold` | `#B08A3E` | Sparing highlight (badges) |
| `--color-header-bg` | `#F8F8F7` | Nav header background — very light neutral grey |
| `--color-blush` | `#ECE0D2` | Hero gradient start color, soft section/notice backgrounds |
| `--color-sage-pale` | `#E4E9DD` | Soft accent background |

All text/background pairings above meet WCAG AA (4.5:1 for normal text, 3:1 for large text) at the sizes they're actually used at. If you change any of these hex values, re-check contrast — a contrast checker takes 30 seconds and prevents an accessibility regression.

**This palette started out calibrated to match the real intothewellcollective.com** (a Wix site — see README on why we couldn't just copy its code). Its live CSS exposes the brand's actual theme colors as CSS custom properties (`--color_NN: r,g,b`), which is how these were originally sourced: navy `rgb(0,53,98)` for body copy, nav "active" state, and buttons; coral `rgb(255,141,107)` for headline emphasis; a near-white page background; and a dusty blush `rgb(233,194,184)` used for soft section backgrounds.

`--color-charcoal` still uses that exact source-site navy value for body copy. Headings (`h1`–`h3`, `.font-display`) no longer follow the source site's coral, though — they use `--color-black`, a plain web-friendly near-black, by explicit request (the coral read as "red" and wasn't wanted for heading text). `--color-terracotta`/`--color-terracotta-dk` (the coral family) are still used for buttons, hover/active states, badges, price accents, and the `.eyebrow` label — kept intentionally darker/more saturated than the raw source-site coral (`rgb(255,141,107)` is only ~2.3:1 against white, failing WCAG AA even at large-text size) so every one of those uses stays AA-safe. `--color-blush` no longer matches the source site's exact dusty-pink value either — it's now `#ECE0D2` by explicit request, used as the hero gradient's start color.

## Typography

- **Display** (`--font-display`): Fraunces — a warm serif for headlines, brand voice.
- **Body** (`--font-body`): Work Sans — a clean humanist sans for readability at small sizes.
- Loaded from Google Fonts in each page's `<head>`. For self-hosting without a Google Fonts dependency, download the two families and swap the `<link>` tags for local `@font-face` rules.
- Type scale runs from `--fs-xs` (13px) to `--fs-3xl` (60px, hero only), all defined in `tokens.css`.

## Spacing

4px base unit, scaling: 4 / 8 / 12 / 16 / 24 / 32 / 48 / 64 / 96px (`--space-1` through `--space-9`). Use these tokens instead of arbitrary pixel values so spacing stays consistent as the site grows.

## Components

- **Buttons** (`.btn`, `.btn--primary`, `.btn--secondary`, `.btn--on-dark`) — pill-shaped, 44px minimum height for touch targets, horizontal padding driven by the `--btn-padding-x`/`--btn-padding-y` custom properties (32px/12px by default, never below the 8–12px floor — see the button bug note below). `flex-shrink: 0` and `white-space: nowrap` are permanent on `.btn` — a button's label never wraps or gets compressed, in a flex row or anywhere else.
- **Cards** (`.card`) — used for classes, instructors, pricing plans (`.plan-card`), events, and partners. All are grid children with `min-width: 0` set deliberately — removing that can reintroduce the overflow bug described below.
- **Class cards** (`.class-card`, e.g. `classes.html`) — photo, name, price, description, CTA, always in that order and always lining up across every card regardless of row. CSS Grid's default row-stretch only equalizes height *within one row*, so `.class-card h3` reserves 2 lines and `.class-card .text-muted` reserves 3 lines (`min-height`, in `em`s tied to `--lh-tight`/`--lh-normal` so it stays correct if type scale changes) — that's what keeps the price/description/CTA starting at the same height on every card, not just neighbors in the same row. `.class-card .btn` gets `margin-top: auto` (the card is a flex column) to pin the CTA to the bottom, and `width: 100%` to span the card edge-to-edge. Keep class descriptions to 3 lines or under at the narrowest 3-up desktop width — anything longer overflows the reserved space and throws off that card's own row.
- **Nav** (`.site-header`, `.nav__menu`) — solid header at rest, filled with `--color-header-bg` (`#F8F8F7`), a very light neutral grey kept deliberately separate from the warm `--color-cream` page background so the header always reads as distinct chrome, not just another section. `main.js` adds `.is-scrolled` past a small scroll offset, which now only adds a light `box-shadow` for depth — the background itself no longer changes on scroll (see the "transparent header" note below for why that's a change from how this used to work). Off-canvas slide-in menu below 1180px, inline row above it (raised from an earlier 960px — that width couldn't fit the brand, all 7 nav links, and the CTA without cramping or wrapping; see the nav breakpoint note below). Current nav item is marked via `data-page` on `<body>` + JS. Desktop nav links share a single animated underline (`.nav__indicator`) that `main.js` slides/resizes to whichever link is hovered or focused, and glides back to the current page's link on mouseleave — see `js/main.js`. Brand mark in the nav is text-only ("Into the Well" — no icon/mark); the full name "Into The Well Collective" (`SITE_NAME` in `generator/build_site.py`) is still used everywhere else — page titles, meta description, footer, social `aria-label`s. The nav's "Book a Class" CTA (`.nav__cta`) uses `.btn--sm` to stay visually secondary to the header itself.
- **Accordion** (`.accordion-item`, used on `faqs.html`) — accessible via `aria-expanded`, keyboard-operable (native `<button>`).
- **Image placeholders** (`.img-placeholder`) — the diagonal-striped boxes throughout the site mark where a real photo should go. Search for `img-placeholder` across the HTML files to find every spot.
- **Notices** (`.notice`) — dashed terracotta boxes flagging things that need a decision or integration before launch (payment provider, booking widget, form backend, etc.). Search for `class="notice"` to find every one and resolve them before going live.

## A layout bug worth knowing about (if you edit the grids)

Any `.grid` with cards containing `.img-placeholder` (which uses `aspect-ratio`) can silently blow out past its container — a classic CSS Grid issue where a grid item's implicit `min-width: auto` lets its content force the column wider than its fair share, overflowing the page horizontally. The fix already in place is `.grid > * { min-width: 0; }` plus the same on `.card` and `.img-placeholder`. If you add a new card-grid section and see unexpected horizontal scroll, this is almost certainly why — make sure the new grid items also get `min-width: 0`.

## A button bug worth knowing about (if you put buttons in a flex row)

The nav's "Book a Class" button once looked cramped — its label crowded right up against the edges of the pill. The cause wasn't insufficient padding (32px horizontal was already generous); it was that the button sat in a flex row (`.nav__menu`, `display:flex`) with no `flex-shrink: 0`, so once the row ran short on space the browser shrank the button's box below what its own padding wanted, squeezing the label toward the edges — and without `white-space: nowrap`, a squeezed button could wrap its label instead of just holding its size. Both are now permanent rules on `.btn` itself, so no button anywhere in this system — nav, card, form, anywhere — can be compressed or wrap its label again. If a future button still looks tight, raise `--btn-padding-x`/`--btn-padding-y` (or a size-specific override like `.btn--sm` does) rather than touching the base padding logic.

## A "white nav bar" bug worth knowing about (historical — `.site-header` is no longer transparent)

`.site-header` used to be `background: transparent` at rest, with `.hero` pulled up underneath it (negative `margin-top`) via a `--header-height` token so the hero's own gradient would show through the header immediately, rather than a gap of plain background. Within that setup, the header looked solid white even though it was supposedly transparent, because `.nav__menu` — the same element used as the mobile off-canvas drawer — has its own `background: var(--color-white)` (the drawer needs an opaque panel to slide in). The `min-width: 1180px` media query that turns that drawer back into an inline desktop row reset its position/size/shadow/padding, but never reset `background`, so the drawer's white fill kept showing through as a solid box behind the desktop links and CTA. Fixed at the time by explicitly setting `background: transparent` on `.nav__menu` inside that desktop media query.

`.site-header` is no longer transparent at all — it's now a permanent `--color-header-bg` grey (see Nav under Components), so this exact bug can't recur, and the `.hero` negative-margin/`--header-height` machinery was removed as dead weight along with it. The lesson still holds for anything similar: a component reused across two visual contexts (like `.nav__menu` as both a mobile drawer and a desktop row) needs every context-specific property explicitly undone in the other context, not assumed to fall away on its own.

## A silently-broken sticky header worth knowing about

`.site-header` has `position: sticky; top: 0;`, but it wasn't actually sticking — it scrolled away with the rest of the page like any normal element. The cause: `html, body { overflow-x: hidden; }` (to stop the off-canvas mobile drawer from adding a phantom horizontal scrollbar). Setting `overflow-x` to anything other than `visible` forces the browser to compute the *other* axis (`overflow-y`) as `auto` too, per the CSS Overflow spec — on **both** `html` and `body` at once, that makes `body` its own independent scrolling box instead of the actual viewport. `.site-header`'s sticky positioning was then anchored to the wrong scroll container, so it never stuck to the visible viewport.

Fixed by moving the rule to `body` only, using `overflow-x: clip` instead of `hidden` — `clip` (unlike `hidden`) doesn't force the other axis's computed overflow to `auto`, so `body` never becomes a separate scroll container in the first place. If you ever need `overflow-x: hidden` again on `html` or `body` for browser-compat reasons, apply it to exactly one of the two, and check `.site-header` still sticks after — this bug produces no console warning or visual break at the top of the page, only once you scroll.

## A cramped desktop nav worth knowing about

The desktop nav (brand + 7 links + CTA button) used to switch on at `min-width: 960px`, but there isn't enough room for all of that in one row until closer to 1180px — between those two widths the links were squeezed tight enough that "Rent The Space" wrapped onto two lines and the gap after the brand text collapsed. Fixed by raising the breakpoint to `1180px` in both `styles.css` (two `@media` blocks: the `.nav__toggle` visibility rule and the desktop `.nav__menu` layout rule) and `main.js` (the `matchMedia` call driving the hover/focus underline). If you add or remove a nav link, these three spots need to move together, and it's worth re-checking the nav at a few widths just above and below the breakpoint.

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
