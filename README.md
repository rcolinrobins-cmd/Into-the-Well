# Into The Well Collective — Rebuilt Site

This is a from-scratch rebuild of intothewellcollective.com as a plain, dependency-free HTML/CSS/JS site — no build step, no framework, no vendor lock-in. Open any `.html` file in a browser and it works; upload the whole folder to any web host and it works.

The one exception is checkout and booking: `gift-card.html` and `pricing.html` charge real cards through the Square Web Payments SDK, and `book-online.html` embeds Square's hosted Appointments booking page — both need the small serverless backend in `api/` (see **Square setup** below), which means those two features specifically need a host that runs Node serverless functions (this was built for Vercel). Every other page is still exactly what it's always been: flat HTML you can host anywhere.

## Why a rebuild instead of a copy

The live site is built on Wix. Wix doesn't let you export the underlying source, and its booking, membership billing, and gift-card checkout are Wix-hosted services that can't move to another server. So instead of scraping unusable, proprietary code, this rebuild captures the site's actual content — copy, pricing, class list, instructor names, FAQs, partner info, contact details — pulled from every page of the live site, and rebuilds it as clean, editable code with a documented design system (see `design-system.md`), ready to host anywhere.

## What's here

The deployable site lives at the **repo root** — index.html and friends sit
at the top level (not in a subfolder), so Vercel/Netlify/GitHub Pages all
pick it up with zero configuration.

```
Into-the-Well/
  index.html                   Home
  classes.html
  instructors.html
  book-online.html
  pricing.html
  gift-card.html
  workshops-events.html
  free-for-members.html
  womens-wellness.html
  partnership-programs.html
  partnership-workshops.html
  current-partners.html
  rent-the-space.html
  faqs.html
  contact.html
  css/tokens.css              design tokens (colors, type, spacing)
  css/styles.css              base styles + components
  js/main.js                  mobile nav, FAQ accordion, hosted booking embed
  js/checkout.js              Square Web Payments SDK checkout modal
  api/                        Vercel serverless functions (Node, no npm deps)
    config.js                   GET  — public Square config for the browser
    create-payment.js           POST — charges a tokenized card via Square
  lib/square.js                thin fetch() wrapper around Square's REST API
  data/checkout-items.json    generated: item key -> {label, amountCents} —
                               the server-side source of truth for prices
  assets/                     empty — real photos go here
  design-system.md            full design system documentation
  ux-audit-report.md          UX/UI + accessibility audit and fixes
  generator/                  the Python scripts that generate the HTML above
    build_site.py                also writes data/checkout-items.json
    pages.py
  package.json                 no dependencies — api/ uses only Node builtins
  .env.example                 copy to .env.local for `vercel dev`
```

## What you need to do before this can replace the live site

1. **Add real photography.** Every dashed/striped box on the site (search any `.html` file for `img-placeholder`) marks where a photo belongs. The old site's images live on Wix's asset CDN, which this rebuild couldn't reach from its sandbox — log into the Wix dashboard → Media Manager → select all → download as a starting point, or use new photos entirely.

   **Every one of these spots has a working drop-in path already** — save a correctly-named file into the matching folder below and run `python3 generator/pages.py`. `image_or_placeholder()` in `generator/build_site.py` checks for a matching file at generate time (trying `.jpg`, `.jpeg`, `.png`, `.webp` in that order) and swaps in a real `<img>` automatically; anything without a file yet just keeps the placeholder. No code change needed either way — this works for one photo or fifty, added incrementally over time.

   | Folder | Filename | Feeds |
   |---|---|---|
   | `assets/images/instructors/` | `<slugified-name>.jpg` (e.g. `ellen-james.jpg`) | that instructor's card on `instructors.html` **and** their bio modal |
   | `assets/images/classes/` | `<slugified-class-name>.jpg` (e.g. `vinyasa.jpg`) | that class's card on `classes.html` **and** the homepage "Class Schedule" teaser, if it's one of the 4 featured there |
   | `assets/images/events/` | `<slugified-event-name>.jpg` (e.g. `new-moon-sound-bath.jpg`) | that event's card on `workshops-events.html`, `womens-wellness.html`, `free-for-members.html`, or `partnership-workshops.html` — whichever page(s) mention that exact event name |
   | `assets/images/partners/` | `<slugified-business-name>.jpg` | that partner's card on `current-partners.html` |
   | `assets/images/home/` | `hero.jpg`, `membership.jpg` | the homepage's top hero photo and the "Unlimited classes, one simple monthly plan" section photo |
   | `assets/images/studio/` | `storefront.jpg`, `rent-the-space.jpg` | the homepage "Find the studio" photo, and the `rent-the-space.html` hero photo |

   "Slugified" = lowercase, spaces and punctuation turned into hyphens — exactly what `generator/build_site.py`'s `slugify()` does, so when in doubt, match what's already in `generator/pages.py` for that name (e.g. `CLASSES`, `EVENTS`, `PARTNERS`). The booking-calendar placeholder (`book-online.html`) and the map placeholder (`contact.html`) are deliberately not on this list — those become a real Square booking embed / a real Google Maps embed respectively, not a static photo.

   Source photos are almost always far larger than needed for a small on-page image (a phone photo can easily be 10+ MB at 4000px+ wide, for something that renders as a 128px avatar or a modest card photo) — resize to a sensible max dimension (a few hundred px for avatars, ~1600px for hero/wide shots) and compress before dropping them in, both for page-load speed and because a git repo isn't the place to accumulate tens of megabytes of source photography. `sips` (built into macOS) handles this from the command line, e.g. `sips -Z 800 --setProperty formatOptions 70 photo.jpg`.
2. **Add the real logo, if you want one.** The nav currently shows text only ("Into the Well", no icon/mark). If you want to bring back a logo image, export it from Wix Media Manager (there were two logo files on the live site) and add it into `.nav__brand` in `build_site.py`'s nav markup, then rebuild — see below.
3. ~~Pick a booking/scheduling provider~~ **Done** — `book-online.html` embeds your Square Appointments booking page once `SQUARE_BOOKING_URL` is set. See **Square setup** below.
4. ~~Pick a payment provider~~ **Done for one-time charges** — every plan on `pricing.html` charges its listed price through Square when clicked. The `/month, auto-renews` plans only charge the *first* payment this way; real auto-renewal needs Square's Subscriptions API wired on top (a Catalog subscription plan per tier + card-on-file), which isn't built yet. See **Square setup**.
5. **Gift card sales are wired for payment, not for issuance.** Clicking an amount on `gift-card.html` charges a real card via Square — but it doesn't yet create an actual redeemable Square gift card (a GAN). That needs Square's separate Gift Cards API (create + activate) added to `api/create-payment.js`'s success path.
6. **Wire up the contact form** on `contact.html` to an email or form service (Formspree, Netlify Forms, etc.) — right now it doesn't submit anywhere.
7. **Fill in placeholder copy**: instructor bios and individual class descriptions weren't published as text on the live site, so those sections currently have neutral placeholder drafts — swap in the studio's real voice. Each instructor's bio modal (click "Read more" on `instructors.html`) also shows a sample "Upcoming Classes" schedule computed from a made-up weekly time slot per instructor, not real booking data (that's cosmetic/independent of the real Square booking embed on `book-online.html`) — see the `.notice` on that page. Studio hours also aren't published anywhere and need to be added.
8. **Verify address/phone/hours** are current, then deploy.

All of these are also flagged inline as dashed `.notice` boxes directly on the relevant pages, so nothing here is hidden — just search each file for `class="notice"`.

## How the pages were generated

Rather than hand-writing 15 nearly-identical HTML files, they're generated from two Python scripts (`generator/build_site.py` + `generator/pages.py`) so the header/footer/nav stay perfectly consistent. If you want to make a change that touches **every page** (e.g. nav links, footer, logo), it's easiest to edit those scripts and regenerate rather than hand-editing 15 files:

```
cd generator && python3 pages.py
```

That writes the regenerated HTML/CSS/JS straight to the repo root. If you'd rather just hand-edit the HTML directly going forward (no Python needed), that's completely fine too — the generator is a convenience, not a requirement. The output files are ordinary static HTML with nothing generator-specific in them.

## Square setup

Checkout (`gift-card.html`, `pricing.html`) and the booking embed (`book-online.html`) read their configuration entirely from environment variables — nothing Square-specific is hardcoded anywhere in the code.

1. Create/open an application at the [Square Developer Dashboard](https://developer.squareup.com/apps).
2. Copy `.env.example` to `.env.local` (for local testing with `vercel dev`) and fill in real values, **or** set the same names in your host's environment variable settings (Vercel: Project Settings → Environment Variables). Never commit real values — `.env*` is already gitignored.
   - `SQUARE_ENVIRONMENT` — `sandbox` while testing, `production` when ready for real cards.
   - `SQUARE_APPLICATION_ID` / `SQUARE_LOCATION_ID` — not secret, safe in client-side code (the Web Payments SDK needs both in the browser).
   - `SQUARE_ACCESS_TOKEN` — **secret**, server-side only. `api/create-payment.js` is the only place that reads it.
   - `SQUARE_BOOKING_URL` — optional, your Square Appointments booking-site link (Dashboard → Appointments → Online Booking). Set it and `book-online.html` embeds it automatically on next page load — no rebuild needed, since it's fetched at runtime from `/api/config`, not baked into the static HTML.
3. Test with a [Square sandbox test card](https://developer.squareup.com/docs/testing/test-values) before ever setting `SQUARE_ENVIRONMENT=production`.
4. `api/create-payment.js` validates the charge amount server-side against `data/checkout-items.json` (regenerated by `python3 generator/pages.py` from the same prices shown on the page) — it never trusts an amount sent from the browser, only an item key.

What's *not* built yet, so you don't discover it by surprise: real Square gift card issuance (payment works, the redeemable code doesn't yet) and Square Subscriptions for auto-renewing memberships (the first charge works, automatic monthly rebilling doesn't yet) — see items 4–5 above.

## Hosting

The static pages work on any host — Netlify, Vercel, GitHub Pages, Cloudflare Pages, or a traditional server (upload via FTP/cPanel to serve `index.html`). Checkout and the booking embed are the exception: they call `/api/config` and `/api/create-payment`, which need a host that runs the Node functions in `api/` — this was built for **Vercel** specifically. Porting `api/` to Netlify Functions (or another provider) would mean moving those two files and adjusting the request/response shape to match that platform's function signature; the logic inside (`lib/square.js`, the price lookup) stays the same either way.

Because `index.html` sits at the repo root, connecting this repo to Vercel needs **no configuration** — leave "Root Directory" as the default (repo root), Framework Preset as "Other", and no build command; Vercel auto-detects the `api/` folder. If a deploy still 404s, double-check those three settings weren't changed, and confirm the deployment picked up the latest commit on `main`. If you deploy to a host that *doesn't* run `api/` (GitHub Pages, a plain FTP host, etc.), every page still works — the checkout modal will just show "Online payments aren't set up yet" and the booking section stays a placeholder, both by design (see `js/checkout.js` / `js/main.js`).

## Accessibility & mobile

Built mobile-first, with a WCAG-AA color palette, visible keyboard focus states, a skip-to-content link, 44px-minimum touch targets, and a fully keyboard-operable nav and FAQ accordion. See `design-system.md` for details.
