# Into The Well Collective — Rebuilt Site

This is a from-scratch rebuild of intothewellcollective.com as a plain, dependency-free HTML/CSS/JS site — no build step, no framework, no vendor lock-in. Open any `.html` file in a browser and it works; upload the whole folder to any web host and it works.

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
  js/main.js                  mobile nav + FAQ accordion
  assets/                     empty — real photos go here
  design-system.md            full design system documentation
  ux-audit-report.md          UX/UI + accessibility audit and fixes
  generator/                  the Python scripts that generate the HTML above
    build_site.py
    pages.py
```

## What you need to do before this can replace the live site

1. **Add real photography.** Every dashed/striped box on the site (search any `.html` file for `img-placeholder`) marks where a photo belongs — hero shots, class photos, instructor headshots, the event space. The old site's images live on Wix's asset CDN, which this rebuild couldn't reach from its sandbox. Easiest path: log into the Wix dashboard → Media Manager → select all → download, then drop the files into `assets/images/` and swap the placeholder `<div>`s for `<img>` tags.
2. **Add the real logo, if you want one.** The nav currently shows text only ("Into the Well", no icon/mark). If you want to bring back a logo image, export it from Wix Media Manager (there were two logo files on the live site) and add it into `.nav__brand` in `build_site.py`'s nav markup, then rebuild — see below.
3. **Pick a booking/scheduling provider** (e.g. Momence, Mindbody, Vagaro, Acuity) and embed its widget on `book-online.html` in place of the placeholder.
4. **Pick a payment provider** for membership billing (Stripe Billing, or your booking provider's built-in billing) and wire it to the "Choose Plan" buttons on `pricing.html`.
5. **Wire up gift card sales** on `gift-card.html` (Stripe, Square, or your booking provider).
6. **Wire up the contact form** on `contact.html` to an email or form service (Formspree, Netlify Forms, etc.) — right now it doesn't submit anywhere.
7. **Fill in placeholder copy**: instructor bios and individual class descriptions weren't published as text on the live site, so those sections currently have neutral placeholder drafts — swap in the studio's real voice. Each instructor's bio modal (click "Read more" on `instructors.html`) also shows a sample "Upcoming Classes" schedule computed from a made-up weekly time slot per instructor, not real booking data — see the `.notice` on that page, and connect a real booking calendar before launch. Studio hours also aren't published anywhere and need to be added.
8. **Verify address/phone/hours** are current, then deploy.

All of these are also flagged inline as dashed `.notice` boxes directly on the relevant pages, so nothing here is hidden — just search each file for `class="notice"`.

## How the pages were generated

Rather than hand-writing 15 nearly-identical HTML files, they're generated from two Python scripts (`generator/build_site.py` + `generator/pages.py`) so the header/footer/nav stay perfectly consistent. If you want to make a change that touches **every page** (e.g. nav links, footer, logo), it's easiest to edit those scripts and regenerate rather than hand-editing 15 files:

```
cd generator && python3 pages.py
```

That writes the regenerated HTML/CSS/JS straight to the repo root. If you'd rather just hand-edit the HTML directly going forward (no Python needed), that's completely fine too — the generator is a convenience, not a requirement. The output files are ordinary static HTML with nothing generator-specific in them.

## Hosting

Any static host works: Netlify, Vercel, GitHub Pages, Cloudflare Pages, or a traditional server (upload via FTP/cPanel to serve `index.html`). No server-side code, database, or build step is required for the pages themselves — only for whichever booking/payment/form providers you choose above.

Because `index.html` sits at the repo root, connecting this repo to Vercel (or Netlify) needs **no configuration** — leave "Root Directory" as the default (repo root), Framework Preset as "Other", and no build command. If a deploy still 404s, double-check those three settings weren't changed, and confirm the deployment picked up the latest commit on `main`.

## Accessibility & mobile

Built mobile-first, with a WCAG-AA color palette, visible keyboard focus states, a skip-to-content link, 44px-minimum touch targets, and a fully keyboard-operable nav and FAQ accordion. See `design-system.md` for details.
