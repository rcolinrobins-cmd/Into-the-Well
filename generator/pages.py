#!/usr/bin/env python3
import json
from build_site import (
    write, placeholder, ICON_CHEVRON, ICON_PIN, ICON_PHONE, ICON_MAIL,
    PHONE, PHONE_TEL, EMAIL, ADDRESS, MAPS_URL, TAGLINE,
)

NOTICE = '<div class="notice">{}</div>'

def membership_nudge(copy, cta_text="See Membership Plans"):
    """Cross-sell banner pointing every content page at pricing.html —
    keeps the primary revenue path (memberships) one click away from
    anywhere on the site, not just the homepage and pricing page."""
    return f'''<div class="membership-nudge">
        <p>{copy}</p>
        <a class="btn btn--primary btn--sm" href="pricing.html">{cta_text}</a>
      </div>'''

# ---------------------------------------------------------------- HOME
CLASS_TEASERS = [
    ("Vinyasa", "All levels · $30", "Breath-synchronized movement linking one pose to the next."),
    ("Yoga Sculpt", "All levels · $30", "A high-energy blend of vinyasa flow and light weights."),
    ("Deep Stretch Yoga", "All levels · $30", "Long-held stretches to release tension and improve mobility."),
    ("Community Yoga", "All levels · Free", "An all-levels class open to the whole community."),
]

home_body = f"""
<section class="hero">
  <div class="container">
    <p class="eyebrow">Garland, TX</p>
    <h1>A Movement Studio, Community &amp; Event Space</h1>
    <p class="lead">Our mission is to provide an inclusive space where YOU feel welcomed. We believe in creating space for people to thrive — in movement, in connection to yourself and others, in the peaceful studio, and a soft place for you to land.</p>
    <div class="hero__actions">
      <a class="btn btn--primary" href="book-online.html">Book a Class — $30</a>
      <a class="btn btn--secondary" href="pricing.html">View Membership Plans</a>
    </div>
    <div class="hero__image">{placeholder("Hero photo — studio interior / class in session", ratio="16/7", radius="var(--radius-lg)")}</div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="callout">
      <h2>The collective represents inclusion, whole-body wellness, and self-care for all humans.</h2>
      <p class="lead">You were put on this earth to do amazing things, and we're here to sit back and celebrate them with you. We're so glad you're here and we look forward to being in community together.</p>
    </div>
  </div>
</section>

<section class="section section--alt">
  <div class="container">
    <div class="section-head section-head--center">
      <p class="eyebrow">This Week</p>
      <h2>Class Schedule</h2>
      <p class="lead">A sample of what's on the mat this week. See the full calendar and reserve your spot online.</p>
    </div>
    <div class="grid grid--4">
      {"".join(f'''<article class="card class-card">
        <div class="img-placeholder" style="aspect-ratio:4/3;"><span>📷 {name}</span></div>
        <h3>{name}</h3>
        <p class="class-card__meta">{meta}</p>
        <p class="text-muted">{desc}</p>
      </article>''' for name, meta, desc in CLASS_TEASERS)}
    </div>
    <p class="section-cta"><a class="btn btn--secondary" href="classes.html">See All Classes</a></p>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="grid grid--2" style="align-items:center;">
      <div>
        <p class="eyebrow">Membership</p>
        <h2>Unlimited classes, one simple monthly plan.</h2>
        <p class="lead">From drop-ins to unlimited monthly access, we have a plan for wherever you are in your practice. Members also enjoy 20% off events and workshops, free instructor-led workshops, and merch discounts.</p>
        <p class="text-muted"><strong>Members save up to 67% per class</strong> compared to drop-in pricing.</p>
        <a class="btn btn--primary mt-5" href="pricing.html">Explore Plans &amp; Pricing</a>
      </div>
      <div>{placeholder("Members practicing together", ratio="4/3")}</div>
    </div>
  </div>
</section>

<section class="section section--alt">
  <div class="container">
    <div class="section-head section-head--center">
      <p class="eyebrow">Visit Us</p>
      <h2>Find the studio</h2>
    </div>
    <div class="grid grid--2">
      <div class="card">
        <ul class="info-list">
          <li class="info-list__item">{ICON_PIN}<span><a href="{MAPS_URL}" target="_blank" rel="noopener">{ADDRESS}</a></span></li>
          <li class="info-list__item">{ICON_PHONE}<span><a href="tel:{PHONE_TEL}">{PHONE}</a></span></li>
          <li class="info-list__item">{ICON_MAIL}<span><a href="mailto:{EMAIL}">{EMAIL}</a></span></li>
        </ul>
        <div class="mt-5">{NOTICE.format("Studio hours weren't published on the live site — add them here.")}</div>
      </div>
      <div>{placeholder("Map or studio storefront photo", ratio="4/3")}</div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="callout callout--terracotta">
      <h2>Give the gift of wellness</h2>
      <p class="lead">Gift cards are redeemable for memberships, classes, workshops, and more — the perfect way to introduce a friend to their new favorite class.</p>
      <a class="btn btn--on-dark mt-4" href="gift-card.html">Shop Gift Cards</a>
    </div>
  </div>
</section>
"""
write(
    "index.html",
    "A Movement Studio, Community & Event Space",
    "Into The Well Collective is an inclusive movement studio, community, and event space in Garland, TX offering yoga, pilates, barre, and strength classes.",
    home_body,
)

# ---------------------------------------------------------------- CLASSES
# Sorted A-Z by name — that order is what powers the "All A-Z" filter option
# on classes.html (see CLASS_FILTERS below); no separate sort needed there.
# category must be one of CLASS_FILTERS' keys (below) so the filter buttons
# and each card's data-category stay in sync.
CLASSES = [
    ("Barre", "$30", "Ballet-inspired micro-movements that sculpt and strengthen using light resistance.", "barre"),
    ("Beginner's Yoga", "$30", "A welcoming introduction to foundational yoga poses and breathing.", "yoga"),
    ("Community Yoga", "Free", "An all-levels class open to the whole community.", "yoga"),
    ("Deep Stretch Yoga", "$30", "Long-held stretches to release tension and improve mobility.", "yoga"),
    ("Moon Flow Yoga", "$30", "An evening flow designed to help you unwind and reset.", "yoga"),
    ("Naptime: A Restorative Practice", "$30", "Supported, restorative poses for deep relaxation.", "yoga"),
    ("Pilates", "$30", "Low-impact, core-strengthening mat work that builds control and stability.", "pilates"),
    ("Power Flow", "$30", "A dynamic, strength-building vinyasa flow.", "yoga"),
    ("Slow Flow", "$30", "An unhurried, breath-led vinyasa practice.", "yoga"),
    ("Soulful Stretch", "$30", "Gentle stretching paired with mindful breathwork.", "yoga"),
    ("Strength", "$30", "Full-body resistance training to build functional strength.", "strength"),
    ("Sun Flow Yoga", "$30", "An energizing morning flow to start your day.", "yoga"),
    ("Vinyasa", "$30", "Breath-synchronized movement linking one pose to the next.", "yoga"),
    ("Weekend Barre", "$30", "Weekend barre session, open to all levels.", "barre"),
    ("Weekend Pilates", "$30", "Weekend pilates session, open to all levels.", "pilates"),
    ("Yin/Vin", "$30", "A blend of slow, deep-holding Yin postures and flowing Vinyasa sequences.", "yoga"),
    ("Yoga Sculpt", "$30", "A high-energy blend of vinyasa flow and light weights.", "yoga"),
    ("Yogi Flow", "$30", "A steady, well-rounded vinyasa practice for all levels.", "yoga"),
]

# "All A-Z" first, then the rest alphabetized by label.
CLASS_FILTERS = [
    ("all", "All A-Z"),
    ("barre", "Barre"),
    ("pilates", "Pilates"),
    ("strength", "Strength"),
    ("yoga", "Yoga"),
]

classes_body = f"""
<section class="hero hero--sub">
  <div class="container">
    <p class="eyebrow">Yoga · Pilates · Barre · Strength</p>
    <h1>Classes</h1>
    <p class="lead">Our certified instructors teach yoga, pilates, barre, and strength — every class is built for all levels with modifications and accommodations available.</p>
  </div>
</section>
<section class="section">
  <div class="container">
    {NOTICE.format("The live site linked a &ldquo;Read More&rdquo; on each class but didn't expose the detail text to this rebuild. The one-line descriptions below are placeholder drafts by genre &mdash; swap in your studio's own copy for each class.")}
    <div class="class-filter" data-class-filter>
      <p class="class-filter__label" id="class-filter-label">Show me classes:</p>
      <div class="class-filter__options" role="group" aria-labelledby="class-filter-label">
        {"".join(f'''<button type="button" class="chip{" is-active" if key == "all" else ""}" data-filter="{key}" aria-pressed="{"true" if key == "all" else "false"}">{label}</button>''' for key, label in CLASS_FILTERS)}
      </div>
      <p class="class-filter__count" data-class-count aria-live="polite"></p>
    </div>
    <h2 class="visually-hidden">All classes</h2>
    <div class="grid grid--3 mt-6">
      {"".join(f'''<article class="card class-card" data-category="{category}">
        {placeholder(name, ratio="4/3")}
        <div class="class-card__head">
          <h3 title="{name}">{name}</h3>
          <p class="class-card__meta">{price}</p>
        </div>
        <p class="text-muted">{desc}</p>
        <a class="btn btn--sm btn--secondary" href="book-online.html" aria-label="Book {name}">Book This Class</a>
      </article>''' for name, price, desc, category in CLASSES)}
    </div>
    {membership_nudge("Taking class more than once a week? <strong>Unlimited Monthly membership pays for itself in just 4 classes</strong> — plans start at $69/mo.")}
  </div>
</section>
"""
write(
    "classes.html",
    "Classes",
    "Explore yoga, pilates, barre, and strength classes at Into The Well Collective in Garland, TX.",
    classes_body,
)

# ---------------------------------------------------------------- INSTRUCTORS
# bio_full is shown in full in the modal, and truncated to 3 lines by CSS
# (line-clamp) in the card preview — using the same full text for both means
# the preview is always long enough to actually overflow and truncate,
# rather than needing a separately hand-tuned short version. slots are an
# instructor's typical weekly class times, used to
# compute real calendar dates for "the next two weeks" client-side (see
# js/main.js) rather than baking specific dates into the HTML, which would
# go stale the moment the site is deployed. An empty slots list means this
# person doesn't teach a regular weekly class (e.g. ownership/guest roles) —
# the modal shows a different message for those instead of a fake schedule.
INSTRUCTORS = [
    {
        "name": "Ellen James",
        "role": "Founder / Owner & Instructor",
        "bio_full": "Ellen founded Into The Well Collective to build a studio where every body feels welcome, blending years of vinyasa and restorative teaching with a deep love of community. She's passionate about accessible movement, trauma-informed cueing, and creating a space that feels like a soft place to land — on the mat and off it. When she's not teaching, she's usually planning the studio's next community event.",
        "specialties": ["Vinyasa", "Restorative Yoga", "Studio Leadership"],
        "slots": [("Mon", "6:00 PM", "Vinyasa Flow"), ("Thu", "9:30 AM", "Restorative Yoga")],
    },
    {
        "name": "Christina Robins",
        "role": "Owner / Operations",
        "bio_full": "Christina keeps the studio running behind the scenes — from scheduling to community partnerships — so every class feels effortless from the moment you walk in. She works closely with instructors and members alike to make sure Into The Well stays a warm, well-organized home base for movement and connection in Garland.",
        "specialties": ["Operations", "Community Partnerships", "Member Experience"],
        "slots": [],
    },
    {
        "name": "Chelsea B",
        "role": "Instructor",
        "bio_full": "Chelsea brings high energy and a love of rhythm to every barre class, focused on strength, stability, and celebrating what your body can do. Her classes mix ballet-inspired micro-movements with light resistance work, and she's known for playlists that make the burn worth it.",
        "specialties": ["Barre", "Sculpt"],
        "slots": [("Tue", "5:30 PM", "Barre"), ("Sat", "10:00 AM", "Barre Sculpt")],
    },
    {
        "name": "Patti C",
        "role": "Instructor",
        "bio_full": "Patti's pilates classes are all about control, core strength, and moving with intention — approachable for beginners, challenging for anyone ready to go deeper. She draws on classical pilates fundamentals and adapts every sequence to the bodies in the room, with modifications always on offer.",
        "specialties": ["Pilates", "Core Strength"],
        "slots": [("Wed", "8:00 AM", "Pilates"), ("Fri", "12:00 PM", "Pilates")],
    },
    {
        "name": "Danielle T",
        "role": "Instructor",
        "bio_full": "Danielle teaches power-driven vinyasa flows built to build heat, strength, and focus — a class for anyone who wants their yoga practice to feel like a workout. Expect creative sequencing, strong core work, and plenty of encouragement to find your edge, whatever that looks like on a given day.",
        "specialties": ["Power Flow", "Strength"],
        "slots": [("Mon", "5:30 PM", "Power Flow"), ("Thu", "6:30 PM", "Power Flow")],
    },
    {
        "name": "Sydney F",
        "role": "Instructor",
        "bio_full": "Sydney's classes slow things down — long holds, deep stretches, and space to actually feel what's happening in your body instead of rushing past it. Her slow flow and deep stretch classes are a favorite for anyone managing stress, tight hips, or just craving a little quiet.",
        "specialties": ["Slow Flow", "Deep Stretch"],
        "slots": [("Tue", "7:00 PM", "Slow Flow"), ("Sun", "4:00 PM", "Deep Stretch Yoga")],
    },
    {
        "name": "Ashtyn N",
        "role": "Instructor",
        "bio_full": "Ashtyn loves introducing newer students to the practice, and her beginner-friendly yoga and yin/vin classes make space for questions, modifications, and progress at your own pace. She's especially passionate about breathwork and helping first-timers feel confident on the mat.",
        "specialties": ["Beginner's Yoga", "Yin/Vin"],
        "slots": [("Wed", "6:00 PM", "Beginner's Yoga"), ("Sat", "9:00 AM", "Yin/Vin")],
    },
    {
        "name": "Trisha K",
        "role": "Instructor",
        "bio_full": "Trisha's barre classes are equal parts precision and fun — expect tiny pulses, big smiles, and a full-body burn by the final track. She's big on form cues and celebrates every shaky-legs moment as a sign you're doing it right.",
        "specialties": ["Barre"],
        "slots": [("Mon", "9:00 AM", "Barre"), ("Sat", "11:00 AM", "Weekend Barre")],
    },
    {
        "name": "Hannah F",
        "role": "Instructor",
        "bio_full": "Hannah teaches pilates with a focus on breath, alignment, and building strength from the inside out — grounded, precise, and always encouraging. Her classes are a great fit whether you're brand new to pilates or looking to refine your practice.",
        "specialties": ["Pilates"],
        "slots": [("Tue", "9:00 AM", "Pilates"), ("Sun", "10:00 AM", "Weekend Pilates")],
    },
    {
        "name": "Jamie R",
        "role": "Guest Instructor",
        "bio_full": "Jamie joins us for special workshops and sound healing sessions, bringing a calming presence and a gift for helping people slow down and reset. Look for Jamie on the schedule during our seasonal workshop series and Free For Members events.",
        "specialties": ["Workshops", "Sound Healing"],
        "slots": [],
    },
    {
        "name": "Meredith S",
        "role": "Guest Instructor",
        "bio_full": "Meredith leads our Women's Wellness Series, creating space to talk openly about nervous system health, nutrition, and what it really means to care for yourself. Her sessions blend gentle movement with honest conversation — no perfection required.",
        "specialties": ["Women's Wellness", "Nervous System Health"],
        "slots": [],
    },
]

instructor_modal_data = [
    {
        "name": i["name"],
        "role": i["role"],
        "bio": i["bio_full"],
        "specialties": i["specialties"],
        "slots": [{"day": d, "time": t, "className": c} for d, t, c in i["slots"]],
    }
    for i in INSTRUCTORS
]

instructors_body = f"""
<section class="hero hero--sub">
  <div class="container">
    <p class="eyebrow">Meet The Team</p>
    <h1>Instructors</h1>
    <p class="lead">Our certified instructors teach yoga, pilates, HIIT, tabata, and barre. Every class is built for all levels, with modifications and accommodations for individuals.</p>
  </div>
</section>
<section class="section">
  <div class="container">
    {NOTICE.format("Individual bios weren't published on the live site beyond name and role &mdash; the bios below are placeholder drafts, and each instructor's &ldquo;Upcoming Classes&rdquo; is a sample schedule computed from a made-up weekly time slot, not a real booking calendar. Swap in real copy and connect real scheduling data before launch.")}
    <h2 class="visually-hidden">Meet the team</h2>
    <div class="grid grid--3 mt-6">
      {"".join(f'''<article class="card instructor-card">
        {placeholder(i["name"], ratio="1/1")}
        <h3>{i["name"]}</h3>
        <p class="badge">{i["role"]}</p>
        <p class="instructor-card__bio">{i["bio_full"]}</p>
        <button type="button" class="link-more" data-instructor-trigger="{idx}">Read more<span class="visually-hidden"> about {i["name"]}</span></button>
      </article>''' for idx, i in enumerate(INSTRUCTORS))}
    </div>
    {membership_nudge("Found your favorite instructor? <strong>Unlimited classes start at $69/mo</strong>, plus 20% off every workshop.")}
  </div>
</section>

<dialog class="instructor-modal" data-instructor-modal aria-labelledby="instructor-modal-name">
  <div class="instructor-modal__inner">
    <button type="button" class="instructor-modal__close btn btn--sm btn--secondary" data-modal-close autofocus aria-label="Close">Close &#10005;</button>
    <div class="instructor-modal__photo" data-modal-photo></div>
    <h2 id="instructor-modal-name" data-modal-name></h2>
    <p class="badge" data-modal-role></p>
    <p data-modal-bio></p>
    <h3>Specialties</h3>
    <ul class="instructor-modal__tags" data-modal-specialties></ul>
    <h3>Upcoming Classes</h3>
    <p class="text-muted" data-modal-schedule-note></p>
    <ul class="instructor-modal__schedule" data-modal-schedule></ul>
  </div>
</dialog>
<script>window.INSTRUCTOR_DATA = {json.dumps(instructor_modal_data)};</script>
"""
write(
    "instructors.html",
    "Instructors",
    "Meet the certified instructors at Into The Well Collective in Garland, TX.",
    instructors_body,
)

# ---------------------------------------------------------------- BOOK ONLINE
book_body = f"""
<section class="hero hero--sub">
  <div class="container">
    <p class="eyebrow">Reserve Your Spot</p>
    <h1>Book a Class Online</h1>
    <p class="lead">Reserve your spot in yoga, pilates, barre, and strength classes at our Garland, TX studio. New here? Your first class is $30 — no membership required.</p>
  </div>
</section>
<section class="section">
  <div class="container container--narrow">
    {NOTICE.format("The original site used Wix's built-in booking &amp; checkout system, which can't move to a new server. Pick a booking/scheduling provider (e.g. Momence, Mindbody, Vagaro, Acuity Scheduling) and embed its calendar widget here &mdash; this section is a placeholder for that embed.")}
    <div class="card mt-6" style="align-items:center; text-align:center;">
      {placeholder("Booking calendar embed goes here", ratio="16/9")}
      <p class="text-muted">Filter by class type or instructor once your booking provider is connected.</p>
      <a class="btn btn--primary" href="pricing.html">See Membership Plans</a>
    </div>
    {membership_nudge("Coming back for more? <strong>Save with a membership</strong> — plans start at $69/mo, or try a full week unlimited for $40.", "Compare Plans")}
  </div>
</section>
"""
write(
    "book-online.html",
    "Book a Class",
    "Reserve your spot in yoga, pilates, barre, and strength classes at Into The Well Collective in Garland, TX.",
    book_body,
)

# ---------------------------------------------------------------- PRICING
PLANS = [
    ("Drop-In Class", "$30", "one-time", "Reserve the class using the booking calendar. Your charge appears at checkout.", False, "Book a Drop-In", None),
    ("Unlimited Monthly Membership", "$109", "/month, auto-renews", "Enjoy as many classes each month as your heart desires. Space must be reserved online prior.", True, "Start Unlimited Membership", "Pays for itself in 4 classes"),
    ("Membership Lite", "$79", "/month, auto-renews", "8 class credits per month — perfect for someone who only wants to come occasionally.", False, "Start Membership Lite", "As low as $9.88/class"),
    ("Weekend Warrior", "$69", "/month, auto-renews", "Unlimited access to weekend classes, plus all other membership bonuses.", False, "Start Weekend Warrior", "Pays for itself in 3 classes"),
    ("5 Class Pass", "$125", "one-time, valid 3 months", "Take 5 classes for the price of 4.", False, "Buy the 5 Class Pass", "Just $25/class"),
    ("One Week Unlimited", "$40", "one-time, valid 1 week", "A flat fee for one week of unlimited classes. If a membership is purchased right after, $35 is refunded from the first month.", False, "Start My Trial Week", None),
    ("One Month Unlimited", "$149", "one-time, valid 1 month", "One month of unlimited classes, month-to-month — great for a trial.", False, "Start One Month Unlimited", None),
    ("Student Unlimited Membership", "$79", "/month, auto-renews", "Discounted membership plan for anyone enrolled in school. Must use a school email to register.", False, "Get Student Pricing", "Pays for itself in 3 classes"),
]
PERKS = [
    "20% discount on special events, workshops, and partnership programs",
    "Free ITW instructor-led workshops",
    "Merchandise discount",
]

pricing_body = f"""
<section class="hero hero--sub">
  <div class="container">
    <p class="eyebrow">Membership</p>
    <h1>Plans &amp; Pricing</h1>
    <p class="lead">Whether you want to drop in once or practice every day, there's a plan for you — and every membership pays for itself fast. All memberships include the perks below.</p>
  </div>
</section>
<section class="section">
  <div class="container">
    <h2 class="visually-hidden">Plans</h2>
    <div class="grid grid--3">
      {"".join(f'''<article class="card plan-card {"plan-card--featured" if featured else ""}">
        {'<span class="plan-card__badge">Best Value</span>' if featured else ""}
        <h3>{name}</h3>
        <p class="plan-card__price">{price}<span> {terms}</span></p>
        <p class="text-muted">{desc}</p>
        {f'<p class="badge">{hint}</p>' if hint else ""}
        <a class="btn {"btn--primary" if featured else "btn--secondary"} btn--block" href="book-online.html">{cta}</a>
      </article>''' for name, price, terms, desc, featured, cta, hint in PLANS)}
    </div>
  </div>
</section>
<section class="section section--alt">
  <div class="container container--narrow text-center">
    <h2>Every membership includes</h2>
    <ul class="grid grid--3 mt-5">
      {"".join(f'<li class="card">{perk}</li>' for perk in PERKS)}
    </ul>
    <p class="mt-6">Not sure which plan fits? <a href="contact.html">Contact us</a> and we'll help you choose.</p>
    {NOTICE.format("Checkout and recurring billing ran through Wix on the old site. Plans above will need to connect to your new payment/booking provider (e.g. Stripe Billing, Momence, Mindbody) before these buttons can actually charge a card.")}
  </div>
</section>
"""
write(
    "pricing.html",
    "Plans & Pricing",
    "Membership plans and drop-in pricing for Into The Well Collective in Garland, TX.",
    pricing_body,
)

# ---------------------------------------------------------------- GIFT CARD
GIFT_AMOUNTS = ["$25", "$50", "$100", "$150", "$200"]
gift_body = f"""
<section class="hero hero--sub">
  <div class="container">
    <p class="eyebrow">Give Something Meaningful</p>
    <h1>The Gift of Wellness</h1>
    <p class="lead">Give the gift of wellness and community — redeemable for memberships, classes, workshops, and more. {TAGLINE}</p>
  </div>
</section>
<section class="section">
  <div class="container container--narrow">
    <h2 class="visually-hidden">Choose an amount</h2>
    <div class="grid grid--3">
      {"".join(f'''<div class="card text-center">
        <p class="plan-card__price">{amt}</p>
        <a class="btn btn--secondary btn--block" href="contact.html" aria-label="Select {amt} gift card">Select</a>
      </div>''' for amt in GIFT_AMOUNTS)}
    </div>
    {NOTICE.format("Gift card purchase &amp; delivery ran through Wix's e-commerce. Connect a payment processor (e.g. Stripe, Square) to sell and auto-deliver gift card codes here.")}
  </div>
</section>
"""
write(
    "gift-card.html",
    "Gift Cards",
    "Give the gift of wellness — gift cards for Into The Well Collective in Garland, TX.",
    gift_body,
)

# ---------------------------------------------------------------- WORKSHOPS & EVENTS
EVENTS = [
    ("The Well Experience", "$35", ""),
    ("Mommy & Me: Workout + Play", "$25", "45 minutes"),
    ("Garland Girlies Pilates", "$15", ""),
    ("New Moon Sound Bath", "$35", ""),
    ("WWS Drop In: Creative Reset", "$35", "1 hour 30 minutes"),
    ("WWS Drop In: Hack Your Nervous System", "$35", ""),
]
events_body = f"""
<section class="hero hero--sub">
  <div class="container">
    <p class="eyebrow">Beyond The Mat</p>
    <h1>Workshops &amp; Events</h1>
    <p class="lead">Members get 20% off all events and complimentary instructor-led workshops.</p>
  </div>
</section>
<section class="section">
  <div class="container">
    {NOTICE.format("Event dates/times were still loading on the live site at capture time &mdash; add your current schedule to each card below.")}
    <h2 class="visually-hidden">Upcoming workshops &amp; events</h2>
    <div class="grid grid--3 mt-6">
      {"".join(f'''<article class="card">
        {placeholder(name, ratio="4/3")}
        <h3>{name}</h3>
        <p class="class-card__meta">{price}{" · " + dur if dur else ""}</p>
        <a class="btn btn--sm btn--secondary" href="book-online.html" aria-label="Book {name}">Book Now</a>
      </article>''' for name, price, dur in EVENTS)}
    </div>
    <div class="grid grid--3 mt-7">
      <a class="card" href="free-for-members.html"><h3>Free For Members</h3><p class="text-muted">1&ndash;2 workshops a month, included with membership.</p></a>
      <a class="card" href="womens-wellness.html"><h3>Women's Wellness Series</h3><p class="text-muted">Drop-in sessions on creative reset, nervous system health, and nutrition.</p></a>
      <a class="card" href="partnership-workshops.html"><h3>Partnership Workshops</h3><p class="text-muted">Events hosted by our paid partners, often discounted for members.</p></a>
    </div>
    {membership_nudge("Members get 20% off every workshop, plus free monthly sessions. <strong>Plans start at $69/mo.</strong>")}
  </div>
</section>
"""
write(
    "workshops-events.html",
    "Workshops & Events",
    "Workshops and events at Into The Well Collective in Garland, TX.",
    events_body,
)

# ---------------------------------------------------------------- FREE FOR MEMBERS
free_body = f"""
<section class="hero hero--sub">
  <div class="container">
    <p class="eyebrow">Member Benefit</p>
    <h1>Free For Members</h1>
    <p class="lead">We provide 1&ndash;2 workshops per month covering holistic wellness topics &mdash; movement, mindfulness, mental health, yoga, sound healing, and community experiences &mdash; free as a membership benefit.</p>
  </div>
</section>
<section class="section">
  <div class="container container--narrow">
    <div class="card">
      {placeholder("New Moon Sound Bath", ratio="16/9")}
      <h2>New Moon Sound Bath</h2>
      <p class="text-muted">A sound healing session. Members can reserve through the booking calendar.</p>
      <a class="btn btn--primary" href="book-online.html">Reserve Your Spot</a>
    </div>
    {membership_nudge("Not a member yet? Unlock free monthly workshops plus unlimited classes &mdash; <strong>plans start at $69/mo.</strong>", "Become a Member")}
  </div>
</section>
"""
write(
    "free-for-members.html",
    "Free For Members",
    "Free monthly wellness workshops included with membership at Into The Well Collective.",
    free_body,
)

# ---------------------------------------------------------------- WOMEN'S WELLNESS
WWS = [
    ("WWS Drop In: Creative Reset", "A session focused on creative renewal."),
    ("WWS Drop In: Hack Your Nervous System", "A workshop addressing nervous system regulation."),
    ("WWS Drop In: Women's Nutrition", "A nutrition-focused session tailored for women."),
]
wws_body = f"""
<section class="hero hero--sub">
  <div class="container">
    <p class="eyebrow">Community Series</p>
    <h1>Women's Wellness Series</h1>
    <p class="lead">Drop-in workshops for women, $35 each. Book individual sessions through the online calendar.</p>
  </div>
</section>
<section class="section">
  <div class="container">
    <h2 class="visually-hidden">Upcoming sessions</h2>
    <div class="grid grid--3">
      {"".join(f'''<article class="card">
        {placeholder(name, ratio="4/3")}
        <h3>{name}</h3>
        <p class="class-card__meta">$35</p>
        <p class="text-muted">{desc}</p>
        <a class="btn btn--sm btn--secondary" href="book-online.html" aria-label="Book {name}">Book Now</a>
      </article>''' for name, desc in WWS)}
    </div>
  </div>
</section>
"""
write(
    "womens-wellness.html",
    "Women's Wellness Series",
    "Drop-in women's wellness workshops at Into The Well Collective in Garland, TX.",
    wws_body,
)

# ---------------------------------------------------------------- PARTNERSHIP PROGRAMS
partnership_body = f"""
<section class="hero hero--sub">
  <div class="container">
    <p class="eyebrow">For Wellness Professionals</p>
    <h1>Partnership Programs</h1>
    <p class="lead">Are you in the wellness industry and looking for a place to grow your business without investing in your own brick-and-mortar?</p>
  </div>
</section>
<section class="section">
  <div class="container container--narrow">
    <h2>Who it's for</h2>
    <p>Small businesses in the wellness industry seeking a professional venue to run classes, workshops, or client services &mdash; without the overhead of owning a physical location.</p>
    <h2 class="mt-6">How it works</h2>
    <p>Rent hourly or on a regular schedule. Partners keep full control over pricing, availability, and setup. We handle maintenance, cleaning, and stocking.</p>
    <div class="grid grid--2 mt-6">
      <div class="card"><h3>What you get</h3><ul class="stack stack--tight mt-3">
        <li>Dedicated rental space, by the hour or on a regular schedule</li>
        <li>Full operational autonomy</li>
        <li>Professional facility maintenance</li>
        <li>Marketing support via social media &amp; newsletter</li>
        <li>Trial collaboration opportunities before a full rental commitment</li>
      </ul></div>
      <div class="card"><h3>Get in touch</h3>
        <ul class="info-list">
          <li class="info-list__item">{ICON_PHONE}<a href="tel:{PHONE_TEL}">{PHONE}</a></li>
          <li class="info-list__item">{ICON_MAIL}<a href="mailto:{EMAIL}">{EMAIL}</a></li>
        </ul>
        <a class="btn btn--primary mt-4" href="contact.html">Contact Us</a>
      </div>
    </div>
    <p class="mt-6"><a href="current-partners.html">See our current partners &rarr;</a></p>
  </div>
</section>
"""
write(
    "partnership-programs.html",
    "Partnership Programs",
    "Rent studio space as a wellness professional at Into The Well Collective in Garland, TX.",
    partnership_body,
)

# ---------------------------------------------------------------- PARTNERSHIP WORKSHOPS
partnership_workshops_body = f"""
<section class="hero hero--sub">
  <div class="container">
    <p class="eyebrow">Hosted By Our Partners</p>
    <h1>Partnership Events &amp; Workshops</h1>
    <p class="lead">These events and workshops are put on by our paid partnerships and aren't necessarily included in our class packages or membership plans. Many are offered at a discount for members using your member code.</p>
  </div>
</section>
<section class="section">
  <div class="container container--narrow">
    <h2 class="visually-hidden">Featured partner workshop</h2>
    <div class="card">
      {placeholder("WWS Drop In: Creative Reset", ratio="16/9")}
      <h3>WWS Drop In: Creative Reset</h3>
      <p class="class-card__meta">$35</p>
      <a class="btn btn--primary" href="book-online.html" aria-label="Book WWS Drop In: Creative Reset">Book Now</a>
    </div>
    <p class="mt-6"><a href="partnership-programs.html">Learn about becoming a partner &rarr;</a></p>
  </div>
</section>
"""
write(
    "partnership-workshops.html",
    "Partnership Workshops",
    "Workshops hosted by Into The Well Collective's partner businesses in Garland, TX.",
    partnership_workshops_body,
)

# ---------------------------------------------------------------- CURRENT PARTNERS
PARTNERS = [
    ("Valiant School of Arms", "Historical European Martial Arts (HEMA) instruction focused on Renaissance swordsmanship and mindful movement. Meets Tuesdays at 7:30pm.", "Valiantfencing@gmail.com", "valiantfencing.carrd.co"),
    ("Healing Arts with Stefanie Tovar, LLC", "Trauma-informed healing blending wellness, performance, and community-rooted liberation &mdash; curanderismo rituals, yoga, sound practices, and storytelling. Tovar also founded Yena, a nonprofit expanding access to healing practices for historically marginalized communities.", "", "stefanietovar.com"),
    ("Molly Bower Coaching", "Life coaching for those seeking direction &mdash; one-on-one coaching and group workshops, including Crayon Meditation. For creative professionals navigating transitions who want growth without hustle culture.", "molly@mollybowercoaching.com", "mollybowercoaching.com"),
    ("Home Healing with Dina Jones", "Combines emotional support with practical home organization &mdash; decluttering guidance paired with addressing the psychological barriers behind it, to create calm, supportive living spaces.", "", "dinajones.org"),
]
partners_body = f"""
<section class="hero hero--sub">
  <div class="container">
    <p class="eyebrow">Our Partners</p>
    <h1>Current Partners</h1>
    <p class="lead">A variety of wellness professionals offer services at our studio.</p>
  </div>
</section>
<section class="section">
  <div class="container">
    <h2 class="visually-hidden">Our partner businesses</h2>
    <div class="grid grid--2">
      {"".join(f'''<article class="card">
        {placeholder(name, ratio="16/9")}
        <h3>{name}</h3>
        <p class="text-muted">{desc}</p>
        <p>{f'<a href="mailto:{email}">{email}</a> &middot; ' if email else ""}<a href="https://{site}" target="_blank" rel="noopener">{site}</a></p>
      </article>''' for name, desc, email, site in PARTNERS)}
    </div>
    <p class="mt-6"><a href="partnership-programs.html">Interested in partnering with us? &rarr;</a></p>
  </div>
</section>
"""
write(
    "current-partners.html",
    "Current Partners",
    "Meet the wellness professionals partnering with Into The Well Collective in Garland, TX.",
    partners_body,
)

# ---------------------------------------------------------------- RENT THE SPACE
RATES = [
    ("Weekday Hourly (Mon&ndash;Thu)", "$100/hour + fees", "No minimum"),
    ("Weekend Hourly (Fri&ndash;Sun)", "$225/hour + fees", "3-hour minimum"),
    ("Weekend Full Day (Fri&ndash;Sat, 12pm&ndash;12am)", "$2,000 flat rate", "&mdash;"),
]
rent_body = f"""
<section class="hero hero--sub">
  <div class="container">
    <p class="eyebrow">Private Rentals</p>
    <h1>Celebrate life's defining moments</h1>
    <p class="lead">Host a stress-free micro-wedding, baby shower, birthday party, bridal shower, or other celebration in downtown Garland, TX. The space has a charming look, so you don't have to decorate much.</p>
    <div class="hero__actions"><a class="btn btn--primary" href="contact.html">Inquire About Renting</a></div>
  </div>
</section>
<section class="section">
  <div class="container">
    <div class="grid grid--2" style="align-items:start;">
      <div class="card">
        <h2>Rates</h2>
        <table class="rate-table">
          <thead><tr><th>Package</th><th>Rate</th><th>Minimum</th></tr></thead>
          <tbody>
            {"".join(f"<tr><td>{name}</td><td>{rate}</td><td>{min_}</td></tr>" for name, rate, min_ in RATES)}
          </tbody>
        </table>
        <p class="form-hint mt-3">All rates include tables, chairs, and a complimentary setup hour. Additional cleaning, insurance, and admin fees apply.</p>
      </div>
      <div class="card">
        <h2>What's included</h2>
        <ul class="stack stack--tight">
          <li>Fully equipped wellness studio</li>
          <li>Tables and chairs included</li>
          <li>One free hour of setup</li>
          <li>Custom party packages available</li>
        </ul>
        {placeholder("Event space photo", ratio="4/3")}
      </div>
    </div>
    <p class="mt-6"><a href="faqs.html">Read rental FAQs &rarr;</a></p>
  </div>
</section>
"""
write(
    "rent-the-space.html",
    "Rent The Space",
    "Rent Into The Well Collective's studio in downtown Garland, TX for private events and celebrations.",
    rent_body,
)

# ---------------------------------------------------------------- FAQS
FAQS = [
    ("Do you have any seating/tables?", "We currently have ten 6-foot folding tables and 45 folding chairs available for renters, plus multiple lounge areas with couches, tables, and chairs throughout the space."),
    ("Is there audio equipment?", "There's a bluetooth speaker with a sub that can be used. You can connect any bluetooth-compatible device."),
    ("Can you bring in outside food/drink?", "Yes! We can even recommend local restaurants who cater your event &mdash; delicious tacos, BBQ, sandwiches, and more right around the corner. We don't currently require hiring a bartender for events."),
    ("Can I set up before my contracted time starts?", "Your booking comes with one hour of setup. Additional setup hours may be purchased at a reduced rate if available before your event."),
    ("Why do I have to pay a cleaning fee?", "We maintain curated furniture and décor. Given the wood floors, brick walls, and large space size, cleaning costs are substantial even with careful use during events."),
    ("What if I need to cancel my event?", "Cancellations 30+ days before the rental receive a partial refund. Cancellations with less notice may not be refunded."),
    ("What types of decoration are acceptable?", "Go nuts! The bigger the better &mdash; balloons, candles, tablecloths, photo booths, etc. Renters must remove all decorations afterward. Fire is limited to candles and food warmers only."),
]
faqs_body = f"""
<section class="hero hero--sub">
  <div class="container">
    <p class="eyebrow">Good To Know</p>
    <h1>Frequently Asked Questions</h1>
    <p class="lead">Mostly about renting the space &mdash; contact us if you don't see your question here.</p>
  </div>
</section>
<section class="section">
  <div class="container container--narrow">
    <h2 class="visually-hidden">All questions</h2>
    <div data-accordion>
      {"".join(f'''<div class="accordion-item">
        <h3><button class="accordion-trigger" aria-expanded="false">
          <span>{q}</span>{ICON_CHEVRON}
        </button></h3>
        <div class="accordion-panel"><div class="accordion-panel__inner">{a}</div></div>
      </div>''' for q, a in FAQS)}
    </div>
    <p class="section-cta"><a class="btn btn--primary" href="contact.html">Still have questions? Contact us</a></p>
  </div>
</section>
"""
write(
    "faqs.html",
    "FAQs",
    "Frequently asked questions about renting Into The Well Collective's studio space in Garland, TX.",
    faqs_body,
)

# ---------------------------------------------------------------- CONTACT
contact_body = f"""
<section class="hero hero--sub">
  <div class="container">
    <p class="eyebrow">We'd Love To Hear From You</p>
    <h1>Contact</h1>
    <p class="lead">{TAGLINE}</p>
  </div>
</section>
<section class="section">
  <div class="container">
    <div class="grid grid--2" style="align-items:start;">
      <div class="card">
        <h2>Send a message</h2>
        {NOTICE.format("This form has no backend yet &mdash; wire it to your email provider or a form service (e.g. Formspree, Netlify Forms) before launch.")}
        <form class="mt-5" action="#" method="post">
          <div class="form-field"><label for="name">Name</label><input id="name" name="name" type="text" required></div>
          <div class="form-field"><label for="email">Email</label><input id="email" name="email" type="email" required></div>
          <div class="form-field"><label for="phone">Phone</label><input id="phone" name="phone" type="tel"></div>
          <div class="form-field"><label for="message">Message</label><textarea id="message" name="message" rows="5" required></textarea></div>
          <button class="btn btn--primary btn--block" type="submit">Send Message</button>
        </form>
      </div>
      <div class="card">
        <h2>Visit or reach out</h2>
        <ul class="info-list">
          <li class="info-list__item">{ICON_PIN}<span><a href="{MAPS_URL}" target="_blank" rel="noopener">{ADDRESS}</a></span></li>
          <li class="info-list__item">{ICON_PHONE}<span><a href="tel:{PHONE_TEL}">{PHONE}</a></span></li>
          <li class="info-list__item">{ICON_MAIL}<span><a href="mailto:{EMAIL}">{EMAIL}</a></span></li>
        </ul>
        {placeholder("Map embed", ratio="4/3")}
      </div>
    </div>
  </div>
</section>
"""
write(
    "contact.html",
    "Contact",
    "Contact Into The Well Collective, a movement studio in Garland, TX.",
    contact_body,
)

print("Done.")
