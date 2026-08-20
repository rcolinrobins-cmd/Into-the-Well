# UX/UI Audit — Into The Well Collective (rebuilt site)

**Scope:** all 15 pages, mobile-first (tested 320–1440px). **Method:** automated checks (Chromium/Playwright) for layout overflow, color contrast (WCAG 2.1 AA math), heading hierarchy, and touch-target size, plus a manual pass against the design-critique and accessibility-review checklists (first impression, usability, visual hierarchy, consistency, WCAG Perceivable/Operable/Understandable/Robust).

Every issue below was found, fixed, and re-verified — not just flagged. Fixes were made at the shared template/CSS level (`tokens.css`, `styles.css`, `main.js`, `build_site.py`) so all pages update consistently rather than being patched one at a time.

## Summary

| Category | Found | Fixed |
|---|---|---|
| Layout bugs (horizontal overflow) | 1 systemic | ✅ |
| Color contrast failures (WCAG 1.4.3) | 3 | ✅ |
| Heading hierarchy skips (WCAG 1.3.1 / 2.4.6) | 11 pages | ✅ |
| Touch target size (best practice / WCAG 2.5.8) | Footer links, social icons, phone/email links, nav logo | ✅ |
| Keyboard trap / focus management (WCAG 2.1.1, 2.4.3) | Mobile nav | ✅ |
| Link-purpose ambiguity (WCAG 2.4.4) | Repeated "Book Now" links | ✅ |
| Design-system consistency (spacing drift) | 14+ inline-style repeats | ✅ |
| Ecommerce/CTA clarity (membership sales) | Generic CTAs, no cross-sell | ✅ |

---

## 1. Color contrast — 3 failures, all fixed

Computed against the actual token hex values (WCAG relative-luminance formula), not eyeballed:

| Element | Before | Ratio | After | Ratio | Required |
|---|---|---|---|---|---|
| Eyebrow labels (e.g. "GARLAND, TX", "MEMBERSHIP") — used on every page | `--color-terracotta` on cream | 4.21:1 ❌ | `--color-terracotta-dk` | 5.96:1 ✅ | 4.5:1 |
| Same eyebrow, on the blush hero background | terracotta on blush | 3.48:1 ❌ | terracotta-dk on blush | 4.94:1 ✅ | 4.5:1 |
| Active nav-link text color | terracotta on cream | 4.21:1 ❌ | terracotta-dk | 5.96:1 ✅ | 4.5:1 |
| "Best Value" pricing badge (white text) | white on `--color-gold` | 3.21:1 ❌ | white on new `--color-gold-dk` | 4.97:1 ✅ | 4.5:1 |

These were systemic — the eyebrow label alone appears on all 15 pages — so a low-vision user would have hit a too-faint label on essentially every screen. Fixed once in `tokens.css`/`styles.css`, applied everywhere automatically.

## 2. Layout bug: horizontal overflow on every page, every screen size

**Found:** class/pricing/event card grids were overflowing past their container — cards extended up to ~700px past the right edge of the viewport at mobile widths. Root cause: a classic CSS Grid "blowout," where a grid item's implicit `min-width: auto` let an `aspect-ratio` image-placeholder box force its column wider than its fair share of the row.

**Fixed:** added `min-width: 0` to grid items, cards, and the placeholder boxes. Separately found and fixed a second overflow source: the closed off-canvas mobile menu (sitting just off-screen via `transform`) was still being counted in the page's scrollable area by the browser, adding a phantom horizontal scrollbar on every page below 960px. Fixed with `overflow-x: hidden` on `html`/`body`.

**Verified:** re-tested at 320, 375, 768, 1280, and 1440px on all 15 pages — zero overflow anywhere now.

## 3. Heading hierarchy skips — 11 pages

**Found:** most content pages jumped from `<h1>` straight to `<h3>` for card titles (classes, instructors, events, partners, FAQ questions, pricing plans) with no `<h2>` in between — the shared footer's "Explore"/"Studio" column headings had the same problem on content-light pages. This breaks screen-reader users' ability to navigate by heading level (WCAG 1.3.1, 2.4.6) — it's the accessibility equivalent of a table of contents with page 1 followed by page 1.3.

**Fixed:** added a section-level `<h2>` before every card grid (visually hidden where a visible one would be redundant with the `<h1>`, e.g. "All classes," "Plans," "Upcoming sessions") on: `classes.html`, `instructors.html`, `pricing.html`, `workshops-events.html`, `womens-wellness.html`, `gift-card.html`, `current-partners.html`, `partnership-workshops.html`, `faqs.html`; promoted section headers that already existed but were mistakenly `<h3>` on `rent-the-space.html` and `contact.html`; wrapped the footer nav in a hidden `<h2>Site footer</h2>` landmark.

**Verified:** scripted a heading-level check across all 15 pages — zero skips remain.

## 4. Touch targets

Checked every visible link/button at 375px width against the 44×44px best-practice minimum (the WCAG 2.1 AA requirement is actually 24×24px per 2.5.8 — 44px is AAA/mobile-ergonomics best practice, which matters here since you said this site is mobile-first).

**Found below 44px:** footer nav links and social links (~19–27px tall — plain text with no padding), the phone/email links in every "visit us" info block (~19–27px), and the nav logo (40px).

**Fixed:** footer links, social links, and phone/email links now use `min-height: 44px` (footer links also get `min-width: 44px` so short labels like "FAQs" don't fall short on width); nav logo bumped to 44×44px. Also bumped the small "Book This Class"/"Book Now" buttons from 36px to 40px for better mobile ergonomics, while keeping them visibly smaller than primary buttons (they're a secondary action repeated inside every card).

## 5. Keyboard trap / focus management in the mobile menu

**Found:** opening the off-canvas mobile nav didn't hide the rest of the page from keyboard or screen-reader users — Tab could silently leave the open menu and land on content visually covered by the dimmed background overlay, with no visible focus indicator on screen (WCAG 2.1.1, 2.4.3).

**Fixed:** `main` and the footer are now marked `inert` while the menu is open (removing them from the tab order and screen-reader tree entirely), Tab/Shift+Tab are trapped inside the open menu as a fallback, and closing the menu (via Escape, the scrim, the close button, or picking a link) returns focus to the hamburger button that opened it.

**Verified:** scripted keyboard test — confirmed `inert` is applied, 12 successive Tab presses never leave the menu, and Escape closes it and returns focus correctly.

## 6. Link-purpose ambiguity

**Found:** every class/event card used the identical link text "Book This Class" / "Book Now" — a screen-reader user browsing by link list would hear "Book Now, Book Now, Book Now…" eighteen times on the classes page with no way to tell them apart out of context (WCAG 2.4.4).

**Fixed:** added `aria-label="Book {class/event name}"` to every one of these links (and `aria-label="Select $X gift card"` on the gift-card page), so assistive tech announces "Book Vinyasa," "Book Yoga Sculpt," etc.

## 7. Design-system consistency (spacing drift)

**Found:** the same visual patterns were implemented as one-off inline `style="..."` attributes repeated across pages instead of reusable classes — the sub-page hero padding (`padding-block:var(--space-7)`) was copy-pasted inline 14 times, a "see all / read more" link pattern 10+ times with two different spacing values (6 vs. 7) used inconsistently for the same visual pattern. This is exactly the kind of drift a design system exists to prevent.

**Fixed:** consolidated into reusable classes — `.hero--sub`, `.section-cta`, `.mt-3` through `.mt-7`, `.stack--tight`, `.callout--terracotta` — and replaced every inline occurrence. One place to change the pattern going forward instead of 14.

## 8. Ecommerce / CTA clarity (membership sales)

You flagged that this site exists to sell memberships, so I gave the funnel a real pass:

- **Specific CTA copy, not generic "Choose Plan" ×8.** Every pricing plan now has its own action-oriented button text: "Start Unlimited Membership," "Start Weekend Warrior," "Buy the 5 Class Pass," "Get Student Pricing," etc. This also happens to fix issue #6 for the pricing page — the buttons are self-describing without needing `aria-label`.
- **Honest, computed value-hints on each plan** — not invented numbers, just math on the studio's own published prices: "Pays for itself in 4 classes" (Unlimited Monthly: $109 ÷ $30 drop-in), "As low as $9.88/class" (Membership Lite: $79 ÷ 8 credits), "Just $25/class" (5 Class Pass: $125 ÷ 5). This is the single highest-leverage change on the pricing page — it turns an abstract monthly price into an immediately obvious deal.
- **Cross-sell banners on content pages that weren't pushing membership at all** — Classes, Instructors, Workshops & Events, Book Online, and Free-for-Members now each carry a contextual, one-line nudge toward `pricing.html` (e.g., on Classes: *"Taking class more than once a week? Unlimited Monthly pays for itself in just 4 classes — plans start at $69/mo."*). Previously the only membership pitch on the entire site lived on the homepage and the pricing page itself.
- **Reduced pricing-page decision paralysis** — added *"Not sure which plan fits? Contact us and we'll help you choose"* below the 8-plan grid, a standard pattern for pages with many similar options.
- **Reviewed, no change needed:** checked every page for competing primary CTAs (more than one `.btn--primary` visible in the same viewport, which dilutes urgency) — found none; each page's primary buttons are spaced across distinct sections as the user scrolls, which is standard practice, not a violation.

---

## What I did *not* change

- Didn't touch the underlying business facts (prices, class names, addresses) — this was a UX/UI and accessibility pass, not a content rewrite.
- Didn't invent savings numbers not derivable from the studio's own published prices — every "X per class" or "pays for itself in Y classes" claim above is exact math on the numbers already on `pricing.html`, not a guess about member behavior.
- Left `.btn--sm` (the repeated in-card "Book" buttons) at 40px rather than 44px — a deliberate, documented trade-off to keep them visually secondary to primary buttons; still well above the WCAG AA minimum (24×24px).

## Verification

All fixes were re-tested after applying, not just asserted:
- Horizontal-overflow sweep: 15 pages × 5 widths (320–1440px) → clean.
- Heading-hierarchy sweep: 15 pages → zero level skips.
- Contrast: recomputed all 4 fixed pairs against WCAG's relative-luminance formula → all ≥4.5:1.
- Touch targets: re-measured footer/social/info-list links at 375px → all ≥44×44px.
- Keyboard: scripted Tab-trap and Escape-to-close test on the mobile nav → passes.
