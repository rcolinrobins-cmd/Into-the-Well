#!/usr/bin/env python3
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
CLASSES = [
    ("Pilates", "$30", "Low-impact, core-strengthening mat work that builds control and stability."),
    ("Barre", "$30", "Ballet-inspired micro-movements that sculpt and strengthen using light resistance."),
    ("Yin/Vin", "$30", "A blend of slow, deep-holding Yin postures and flowing Vinyasa sequences."),
    ("Strength", "$30", "Full-body resistance training to build functional strength."),
    ("Yoga Sculpt", "$30", "A high-energy blend of vinyasa flow and light weights."),
    ("Slow Flow", "$30", "An unhurried, breath-led vinyasa practice."),
    ("Deep Stretch Yoga", "$30", "Long-held stretches to release tension and improve mobility."),
    ("Beginner's Yoga", "$30", "A welcoming introduction to foundational yoga poses and breathing."),
    ("Moon Flow Yoga", "$30", "An evening flow designed to help you unwind and reset."),
    ("Soulful Stretch", "$30", "Gentle stretching paired with mindful breathwork."),
    ("Community Yoga", "Free", "An all-levels class open to the whole community."),
    ("Naptime: A Restorative Practice", "$30", "Supported, restorative poses for deep relaxation."),
    ("Sun Flow Yoga", "$30", "An energizing morning flow to start your day."),
    ("Yogi Flow", "$30", "A steady, well-rounded vinyasa practice for all levels."),
    ("Power Flow", "$30", "A dynamic, strength-building vinyasa flow."),
    ("Weekend Barre", "$30", "Weekend barre session, open to all levels."),
    ("Weekend Pilates", "$30", "Weekend pilates session, open to all levels."),
    ("Vinyasa", "$30", "Breath-synchronized movement linking one pose to the next."),
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
    <h2 class="visually-hidden">All classes</h2>
    <div class="grid grid--3 mt-6">
      {"".join(f'''<article class="card class-card">
        {placeholder(name, ratio="4/3")}
        <h3>{name}</h3>
        <p class="class-card__meta">{price}</p>
        <p class="text-muted">{desc}</p>
        <a class="btn btn--sm btn--secondary" href="book-online.html" aria-label="Book {name}">Book This Class</a>
      </article>''' for name, price, desc in CLASSES)}
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
INSTRUCTORS = [
    ("Ellen James", "Founder / Owner & Instructor"),
    ("Christina Robins", "Owner / Operations"),
    ("Chelsea B", "Instructor"),
    ("Patti C", "Instructor"),
    ("Danielle T", "Instructor"),
    ("Sydney F", "Instructor"),
    ("Ashtyn N", "Instructor"),
    ("Trisha K", "Instructor"),
    ("Hannah F", "Instructor"),
    ("Jamie R", "Guest Instructor"),
    ("Meredith S", "Guest Instructor"),
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
    {NOTICE.format("Individual bios weren't published on the live site beyond name and role &mdash; add a short bio for each instructor below.")}
    <h2 class="visually-hidden">Meet the team</h2>
    <div class="grid grid--4 mt-6">
      {"".join(f'''<article class="card instructor-card">
        {placeholder(name, ratio="1/1")}
        <h3>{name}</h3>
        <p class="badge">{role}</p>
        <p class="text-muted">Bio coming soon.</p>
      </article>''' for name, role in INSTRUCTORS)}
    </div>
    {membership_nudge("Found your favorite instructor? <strong>Unlimited classes start at $69/mo</strong>, plus 20% off every workshop.")}
  </div>
</section>
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
