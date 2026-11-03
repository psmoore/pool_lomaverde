#!/usr/bin/env python3
"""Build the Loma Verde Aquatic Center preview: the center's page, Lap & Open Swim, Swim Lessons, Water Fitness and
Rentals, with every swim, lesson and class time read live from Pool Relay by finder.js (#today, #week, data-live).
Nothing about WHEN the pools are open is typed here; only rates, temperatures, policies and facts about the water.
Run: python3 build.py"""
import hashlib, html, json

E = html.escape
V = {"lv": "1Ublex83fFwpSt76BzsRaI"}  # Pool Relay share token: Loma Verde Aquatic Center, lane by lane
SITE = "https://www.chulavistaca.gov/departments/parks-and-recreation/community-centers/loma-verde-aquatic-center"
CATALOG = "https://secure.rec1.com/CA/chula-vista-ca/catalog"
POOLS = [
    dict(slug="lv", name="Loma Verde Aquatic Center", short="Loma Verde", facility="Loma Verde Aquatic Center",
         area="Chula Vista", kind="yearRound", address="1420 Loma Lane, Chula Vista, CA 91911", phone="(619) 409-1988", href="index.html"),
]

def live(mode, **kw):
    attrs = "".join(f' data-{k.replace("_", "-")}="{E(str(v))}"' for k, v in kw.items())
    return f'data-live="{mode}" data-view="{V["lv"]}" data-pool="lv"{attrs}'

MENU = [("Parks and Recreation", None, 0), ("Park Updates", None, 1), ("Park Reservations", None, 1), ("Community Centers", None, 1),
        ("Heritage Community Center", None, 2), ("Loma Verde Aquatic Center", "index.html", 2), ("Lap & Open Swim", "swim.html", 3),
        ("Swim Lessons", "lessons.html", 3), ("Water Fitness", "fitness.html", 3), ("Rentals", "rentals.html", 3),
        ("Loma Verde Community Center", None, 2), ("Norman Park Senior Center", None, 2), ("Parkway Aquatic Center", None, 2)]

VER = hashlib.sha1((open("finder.js").read() + open("style.css").read()).encode()).hexdigest()[:8]  # cache-busts both on change

def page(file, title, body, contact):
    menu = "".join(f'<a class="{"sub" if lvl else ""}{" here" if href == file else ""}" href="{href or "#"}"'
                   f' style="padding-left:{14 + 10 * lvl}px">{E(label)}</a>' for label, href, lvl in MENU)
    doc = f"""<!doctype html>
<!-- UNOFFICIAL PREVIEW. Not a City of Chula Vista website. A mock-up of {SITE}
     with both Loma Verde pools on one live Pool Relay schedule. -->
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>{E(title)} | City of Chula Vista preview</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&family=Montserrat:wght@500;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="style.css?v={VER}">
</head>
<body>
<div class="preview-note"><b>Unofficial preview.</b> Not a City of Chula Vista page &mdash; a mock-up of <a href="{SITE}" target="_blank" rel="noopener noreferrer">the Loma Verde Aquatic Center page</a> with both pools on one live schedule.</div>
<header class="site"><div class="hdr">
  <a class="brand" href="index.html"><small>City of</small><span>Chula Vista</span></a>
  <div class="right"><div class="util"><span>Jobs</span><span>eNotification</span><span>Calendar</span></div>
    <nav aria-label="Main"><span>Our City</span><span>Businesses</span><span>Departments</span><span>I Want To…</span></nav></div>
</div></header>
<div class="page">
  <aside class="side"><h2>Parks and Recreation</h2><nav aria-label="Parks and Recreation">{menu}</nav></aside>
  <main class="main"><p class="small muted" style="margin:0 0 6px">Departments » Parks and Recreation » Community Centers</p><h1>{E(title)}</h1>{body}</main>
  <aside class="contact"><h2>Contact</h2>{contact}</aside>
</div>
<footer class="site"><div class="in">
  <div><h4>City of Chula Vista</h4><p>276 Fourth Avenue, Chula Vista, CA 91910<br>Parks and Recreation</p></div>
  <div><h4>About this preview</h4><p>Built to demonstrate embedded <a href="https://www.poolrelay.com" target="_blank" rel="noopener">Pool Relay</a> schedules. Not operated by or affiliated with the City of Chula Vista. Schedule entered from the city's Rec1 catalog on November 2, 2026; which pool and lanes open swim and fitness classes use is our estimate.</p></div>
</div></footer>
<script>window.POOLS = {json.dumps(POOLS)};</script>
<script src="finder.js?v={VER}"></script>
</body>
</html>
"""
    open(file, "w").write(doc)

CONTACT = """<p><b>Loma Verde Aquatic Center</b>1420 Loma Lane<br>Chula Vista, CA 91911</p>
<p><b>Carolyn Lechner</b>Aquatics Supervisor II<br>(619) 409-1988</p>
<p><b>Office hours</b>Monday–Friday<br>10:00 AM–12:00 PM<br>4:00 PM–7:00 PM</p>"""

WEEK = f'<div id="week" data-view="{V["lv"]}" data-pool="lv" data-pools="Competition Pool|Recreation Pool"><p class="muted">Loading the week…</p></div>'
LANES = (f'<div class="frame"><iframe src="https://www.poolrelay.com/embed/{V["lv"]}" height="760" '
         f'title="Loma Verde Aquatic Center, lane by lane" loading="lazy"></iframe></div>')
REGISTER = f'Passes and classes are sold in the city\'s <a href="{CATALOG}" target="_blank" rel="noopener">online catalog</a>.'

# ── Loma Verde Aquatic Center ────────────────────────────────────────────────
page("index.html", "Loma Verde Aquatic Center", f"""
    <h2 style="margin-top:0">1420 Loma Lane Chula Vista, CA 91911</h2>
    <p class="lede">Loma Verde has served the Chula Vista community since 1971, and reopened in 2023 after a full-facility renovation. It
      has a splash pad and two pools heated year-round, indoor changing rooms, family changing rooms and an event space. Every time on
      these pages comes from the pools' live schedule, so when the staff change it, these pages change with it.</p>
    <div class="top2">
      <section class="now" aria-live="polite"><h2>Right now</h2>
        <div id="today" data-view="{V['lv']}" data-pool="lv"><p class="muted">Loading today’s schedule…</p></div></section>
      <aside class="hours"><h2>Swim times</h2>
        <p class="small" style="margin:0 0 6px"><b>Lap swim:</b> <span {live("when", title="Lap Swim")}>…</span></p>
        <p class="small" style="margin:0 0 6px"><b>Open swim:</b> <span {live("when", title="Open Swim")}>…</span></p>
        <p class="small" style="margin:0 0 6px"><b>Water fitness:</b> <span {live("when", title="Water Fitness|Aqua Zumba", gap=-1)}>…</span></p>
        <p class="small" style="margin:0"><b>Swim lessons:</b> <span {live("when", title="Swim Lessons", gap=-1)}>…</span></p>
        <div class="adjusted" {live("closures")} hidden></div>
      </aside>
    </div>
    <h2>This week, pool by pool</h2>
    {WEEK}
    <h2>Lane by lane</h2>
    <p class="small muted">Pick a day to see who is in each of the competition pool's 22 short-course lanes and the recreation pool's 5 lanes.</p>
    {LANES}
    <h2>Amenities</h2>
    <div class="facts">
      <div><h3>Competition Pool</h3><ul><li>Olympic-sized, 25 yards × 50 meters, 7–12.5 feet deep</li><li>79–81°F</li>
        <li>22 short-course or 10 long-course lane lines, with backstroke flags</li>
        <li>25-yard, 25-meter or 30-meter water polo course with floating cages</li>
        <li>Lap swim, deep water fitness, and team rentals: high school teams, a youth swim team and a youth water polo team</li></ul></div>
      <div><h3>Recreation Pool</h3><ul><li>Instructional pool, 25 yards × 11 meters, 2.5–5 feet deep</li><li>85–87°F</li>
        <li>5 short-course lanes with backstroke flags</li><li>Lap swim for casual or beginner swimmers, shallow water fitness, swim lessons,
        open swim and therapy rentals</li></ul></div>
    </div>
    <p><b>Splash pad:</b> 9 features and 24 fountains for children up to 12; adult supervision required.</p>
    <p class="small">Kickboards, pull buoys, water dumbbells, pool noodles, Coast Guard approved lifejackets and cubbies with combination locks
      are free to use. Team lockers, touch pads, a scoreboard/video screen and timing equipment can be rented. Digital pace clock, pool lift
      and ADA-accessible stairs, a shaded spectator area with bleachers, and chaise lounges and umbrellas.</p>

    <div class="replaces">
      <h2>What this replaces</h2>
      <ul>
        <li><b>"See online catalog for schedule and availability."</b> The city page describes the pools but sends you to the Rec1 catalog for
          every time, and the catalog lists each pass and class separately. Here the whole center is one schedule.</li>
        <li><b>A flyer from another season.</b> The schedule PDF linked for Loma Verde is a Fall 2024 flyer. Here the times are the ones in
          the water this week.</li>
        <li><b>"Pool space and lanes are not guaranteed."</b> Lap swim passes don't say how much water is left when classes, lessons or team
          rentals are in. Here every booking holds its lanes, so you can see what's open.</li>
        <li><b>Lesson times one listing at a time.</b> Each level, day and time is its own catalog entry. Here every lesson block is on one
          calendar, by pool.</li>
        <li><b>Team rentals out of sight.</b> High school teams and the local youth swim and water polo teams rent the competition pool, but
          none of that is posted. Here it can be, so swimmers know before they drive over.</li>
      </ul>
    </div>
""", CONTACT)

# ── Lap & Open Swim ──────────────────────────────────────────────────────────
page("swim.html", "Lap & Open Swim", f"""
    <p class="lede">Lap swim is in the competition pool for ages 16 and up; casual and beginner swimmers can also swim laps in the
      recreation pool. Open swim is for youth, adults and seniors. {REGISTER}</p>
    <div class="top2">
      <aside class="hours"><h2>Lap swim</h2>
        <div {live("hours", format="dl", title="Lap Swim", whole=0)}><p class="muted">…</p></div>
        <div class="adjusted" {live("exceptions", title="Lap Swim")} hidden></div>
      </aside>
      <aside class="hours"><h2>Open swim</h2>
        <div {live("hours", format="dl", title="Open Swim", whole=0)}><p class="muted">…</p></div>
        <div class="adjusted" {live("exceptions", title="Open Swim")} hidden></div>
      </aside>
    </div>
    <div class="adjusted" {live("closures")} hidden></div>
    <h2>Lane by lane</h2>
    <p class="small muted">Who else is in the water during lap and open swim, and how many lanes are left.</p>
    {LANES}
""", CONTACT)

# ── Swim Lessons ─────────────────────────────────────────────────────────────
LEVELS = [("Parent & Tot", "6 months to 3 years, with a parent"), ("Preschool, Levels 1–3", "Ages 4–5"),
          ("Youth, Levels 1–4", "Ages 6–15"), ("Private lessons", "Ages 2 and up, 30 minutes")]
levels = "".join(f"<tr><th>{E(n)}</th><td>{E(a)}</td></tr>" for n, a in LEVELS)
page("lessons.html", "Swim Lessons", f"""
    <p class="lede">Group and private lessons in the warm recreation pool, in monthly sessions of 30-minute classes. {REGISTER}</p>
    <div class="top2">
      <aside class="hours"><h2>Lesson times</h2>
        <div {live("hours", format="dl", title="Swim Lessons", whole=0)}><p class="muted">…</p></div>
        <p class="small muted" style="margin:6px 0 0">Classes run back to back inside these blocks; pick a level and time in the catalog.</p>
      </aside>
      <aside class="hours"><h2>Coming dates</h2>
        <div class="small" {live("dates", title="Swim Lessons")}>…</div>
      </aside>
    </div>
    <h2>Levels</h2>
    <div class="tblwrap"><table class="prog">{levels}</table></div>
    <h2>Lane by lane</h2>
    {LANES}
""", CONTACT)

# ── Water Fitness ────────────────────────────────────────────────────────────
page("fitness.html", "Water Fitness", f"""
    <p class="lede">Deep water fitness in the competition pool and shallow water fitness in the recreation pool, for adults and seniors.
      {REGISTER}</p>
    <div class="tblwrap"><table class="prog">
      <tr><th>Water Fitness<div class="small muted" style="font-weight:400">Adults and seniors</div></th><td class="when" {live("when", title="Water Fitness", gap=-1)}>…</td></tr>
      <tr><th>Aqua Zumba<div class="small muted" style="font-weight:400">Ages 16+</div></th><td class="when" {live("when", title="Aqua Zumba", gap=-1)}>…</td></tr>
    </table></div>
    <div class="adjusted" {live("exceptions", title="Water Fitness|Aqua Zumba")} hidden></div>
    <h2>This week, pool by pool</h2>
    {WEEK}
""", CONTACT)

# ── Rentals ──────────────────────────────────────────────────────────────────
RATES = [("Shared use", "$45", "$89", "$89", "$177"), ("Exclusive use", "$48", "$94", "$94", "$189"), ("Swim lane", "$9", "$20", "$20", "$37")]
rates = "".join(f"<tr><th>{E(a)}</th><td>{b}</td><td>{c}</td><td>{d}</td><td>{e}</td></tr>" for a, b, c, d, e in RATES)
page("rentals.html", "Rentals", f"""
    <p class="lede">Loma Verde Aquatic Center has many opportunities to meet your facility use needs, from a few swim lanes to the whole
      pool, swim meets and water polo games.</p>
    <h2>Check what's open</h2>
    <p class="small muted" style="margin-top:0">Every booking holds its lanes, so the empty water below is what's available.</p>
    {LANES}
    <h2>Rental fees</h2>
    <p class="small muted" style="margin-top:0">Hourly; staff fees not included.</p>
    <div class="tblwrap"><table class="prog">
      <tr><th></th><td><b>Resident / non-profit, non-prime</b></td><td><b>Resident / non-profit, prime</b></td><td><b>Non-resident / for-profit, non-prime</b></td><td><b>Non-resident / for-profit, prime</b></td></tr>
      {rates}
    </table></div>
    <p class="small">Non-prime time: Monday–Friday open to 5:00 PM, and Sunday all day. Prime time: Monday–Friday 5:00 PM to close, Saturday
      all day, and city-recognized holidays.</p>
    <h2>Reserving</h2>
    <p>Fill out the Application for Facility Use – Aquatics and bring it to the Loma Verde office when you make your reservation. Once the
      application is approved, secure your date with a $100 non-refundable payment toward your rental fees; the final payment is due 21
      days before your event. Include setup and takedown times in your request. Tables and chairs are included.</p>
""", CONTACT)
print("built 5 pages, assets", VER)
