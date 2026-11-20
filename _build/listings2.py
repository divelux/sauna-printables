#!/usr/bin/env python3
"""Wave 2: writes LISTING.md into the twelve new product folders and adds their rows to printables/README.md.
Same format and the same limits as listings.py (title <= 60 characters, short description <= 160,
full description 150-220 words with one or two links). Wave 1 files are not touched."""
import os
import re

import common as C
from listings import BANNED, LICENSE

FOOT = ("Made by DIVELUX, makers of wool sauna hats: https://diveluxsaunahat.com\n"
        "More free sauna printables and tools: https://diveluxsaunahat.com/pages/sauna-tools")
P = {}

P["sauna-first-timer-pocket-card"] = dict(
    name="First Sauna pocket card", pages="1 page, 4 fold-in-half cards",
    title="First Sauna Pocket Card (Printable Checklist)",
    short="Free printable pocket card for a first sauna visit: what to pack and five simple steps in the heat. Four fold-in-half cards per sheet, US Letter and A4.",
    full=f"""The first sauna visit raises small questions. What do I bring? Where do I sit? How long do I stay? This pocket card answers them on something the size of a playing card.

Each sheet makes four cards. Cut along the dashed lines, fold each card in half with the print on the outside, and it is ready for a gym bag or a coat pocket. Folded size: 2.4 x 3.6 in.

On the front:

- A packing list with tick boxes: two towels, water bottle, flip-flops, a swimsuit if the place asks for one, and a wool felt sauna hat, worn dry
- A small guide to the benches, from the hottest seat to the mildest

On the back, five steps: shower first, sit on your towel, keep the first round short, ask before you pour water on the stones, cool down and rest. One line stands apart: if you feel dizzy, sick or unwell, leave the heat right away.

Handy for sauna owners who host first-timers, for gyms and spas, and for anyone who wants to give a friend an easy start.

General information, not medical advice.

{FOOT}""",
    tags="sauna for beginners, first sauna, sauna checklist, pocket card, sauna etiquette, what to bring to a sauna, gym sauna, printable card, sauna tips, free printable",
    files=["sauna-first-timer-pocket-card-letter.pdf", "sauna-first-timer-pocket-card-a4.pdf", "sauna-first-timer-pocket-card.html", "preview.png"])

P["sauna-cold-plunge-journal"] = dict(
    name="Sauna and Cold Plunge Journal", pages="8 pages",
    title="Sauna and Cold Plunge Journal (Undated Printable)",
    short="Free undated journal for sauna and cold plunge sessions: weekly spread, year at a glance, notes pages and a places-to-try list. 8 pages, US Letter and A4.",
    full=f"""A paper journal for people who like to write down their sauna days. It is undated, so you can start in any week and print only the pages you use.

Eight pages:

- Cover with a line for your name and start date
- How to use it: what each field means, a 1 to 5 scale for how the session felt, and room for your own setup
- Year at a glance: twelve rows of 31 circles, one to fill for every sauna day
- A weekly spread on two pages: seven session blocks with date, sauna type, temperature, rounds, minutes per round, cold plunge and seconds in the cold, plus a short week in review
- Lined notes page
- Dot grid page for sketches and bench layouts
- Places to try: saunas, bathhouses, lakes and cold plunges on your list

Print the weekly spread as many times as you need, punch the pages and keep them in a binder. The typical temperature ranges on the how-to page come from our open dataset, Sauna Traditions of the World.

A logbook, not a training plan. General information, not medical advice.

{FOOT}""",
    tags="sauna journal, cold plunge log, sauna log book, undated planner, printable journal, habit tracker, contrast therapy, sauna tracker, binder pages, free printable",
    files=["sauna-cold-plunge-journal-letter.pdf", "sauna-cold-plunge-journal-a4.pdf", "sauna-cold-plunge-journal.html", "preview.png"])

P["sauna-party-invitations"] = dict(
    name="Sauna Party Invitations", pages="4 pages, 4 cards per sheet",
    title="Sauna Party Invitations (Printable, 4 per Sheet)",
    short="Free printable sauna party invitations: three designs with fill-in lines plus an open version for your own words. Four cards per sheet, US Letter and A4.",
    full=f"""Inviting friends over for a sauna night is half the fun. These invitations are made for it: print a sheet, cut four cards, write in the details and hand them out.

Four sheets are included:

- Design 1, Sauna night: big type and a small heat ladder
- Design 2, Come get warm: a line drawing of a sauna cabin between two pines
- Design 3, Steam and friends: a wooden bucket and ladle on a warm side band
- Open version, Sauna party: a title and eight blank lines for your own words

The three designs have fill-in lines for when, where and RSVP. Two of them also carry a short packing hint for guests: bring a towel to sit on, a water bottle and flip-flops. Hats welcome.

Each card is 3.9 x 5 in and fits a standard A2 envelope. Print at 100% on heavy paper or card stock and cut along the dashed lines. US Letter and A4 PDFs are included, along with the HTML source if you want to change the wording.

Works for birthdays, cabin weekends, a first heat in a new sauna, or no reason at all.

{FOOT}""",
    tags="sauna party, party invitations, printable invitations, sauna night, sauna birthday, spa party, fill in invitation, cabin weekend, invitation template, free printable",
    files=["sauna-party-invitations-letter.pdf", "sauna-party-invitations-a4.pdf", "sauna-party-invitations.html", "preview.png"])

P["sauna-traditions-of-the-world-poster"] = dict(
    name="Sauna Traditions of the World poster", pages="1 page, landscape",
    title="Sauna Traditions of the World Poster (Printable)",
    short="Free poster: 28 sauna and bathing traditions by region, from Finnish sauna and banya to hammam, onsen and temazcal, with typical temperatures. Letter and A4.",
    full=f"""People have been sweating, steaming and bathing together for a very long time, and almost every region has its own way of doing it. This poster puts 28 of those traditions on one page.

The traditions are grouped by region: Nordic countries, Baltic states, Eastern Europe, Western and Central Europe, the Mediterranean and Caucasus, East Asia, the Americas, and modern rooms found worldwide. For each one the poster shows:

- The name and the local name, such as savusauna, pirtis, hamam or jjimjilbang
- Where it comes from and what kind of bath it is
- The typical temperature in °F and °C, drawn as a bar on a common scale
- Whether water is poured on hot stones
- Whether a felt hat is traditionally worn
- A small mark for traditions on the UNESCO intangible heritage list

Every word and number in the table is read from our open dataset, Sauna Traditions of the World. Where published figures disagree, the dataset leaves the temperature blank and the poster says "not given" instead of guessing.

One landscape page in US Letter and A4. General information, not medical advice.

{FOOT}""",
    tags="sauna traditions, sauna poster, banya, hammam, onsen, jjimjilbang, bathing culture, infographic, world cultures, free printable",
    files=["sauna-traditions-of-the-world-poster-letter.pdf", "sauna-traditions-of-the-world-poster-a4.pdf",
           "sauna-traditions-of-the-world-poster.html", "preview.png"])

P["sauna-coloring-pages"] = dict(
    name="Sauna Coloring Pages", pages="6 pages",
    title="Sauna Coloring Pages for Kids and Grown-Ups",
    short="Six free sauna coloring pages: stove with stones, bucket and ladle, felt hats, a lakeside cabin, a leafy whisk and a mandala. US Letter and A4.",
    full=f"""Six coloring pages for a quiet hour in the lounge, at the cabin table, or while the sauna heats up. Four are simple enough for children. Two have finer detail for older kids and grown-ups.

The pages:

- Sauna stove: a stove with a heap of stones, a fire behind the glass, a bucket, a thermometer and a hat on its peg
- Bucket and ladle: a big wooden bucket with hoops, staves and a few birch leaves
- Sauna hats: two bell-shaped felt hats, one with patterns to color, and a bucket hat
- Sauna by the lake: a log cabin with a smoking chimney, pines, a dock and reeds
- Leafy whisk: a bundle of birch twigs with close to a hundred leaves
- Fire, water, leaf: a round mandala built from flames, stones, leaves and water drops

All the artwork is clean vector line art drawn for this set, so the lines stay sharp at any print size. Each page has a short caption a child can read aloud.

Print on plain paper for crayons and pencils, or on heavier paper for markers. US Letter and A4 PDFs, six pages each, plus the HTML source.

{FOOT}""",
    tags="coloring pages, sauna coloring, kids activity, adult coloring, mandala, cabin coloring page, printable coloring, rainy day activity, line art, free printable",
    files=["sauna-coloring-pages-letter.pdf", "sauna-coloring-pages-a4.pdf", "sauna-coloring-pages.html", "preview.png"])

P["wood-sauna-stove-lighting-checklist"] = dict(
    name="Wood Sauna Stove Lighting checklist", pages="1 page",
    title="Wood Sauna Stove Lighting Checklist (Printable)",
    short="Free one-page checklist for lighting a wood-burning sauna stove: before you light, building the fire, while it burns, when you are done. Letter and A4.",
    full=f"""A wood-fired sauna rewards a calm routine. This one-page checklist walks through it in four blocks, from the first look around the stove to cold ashes.

- Before you light: clear the area, empty the cold ash box, open the flue damper and the fresh-air vent, check the alarms
- Build and light the fire: dry split wood, bigger pieces at the bottom, kindling on top, lit from the top, door closed
- While it burns: add a few pieces at a time, do not overfire, mind the hot handles, water on the stones only
- When you are done: let the fire burn out, keep the damper open until the embers are out, store cold ashes in a lidded metal container outdoors

A strip at the bottom covers three things people ask about most: what never to burn, what to do with a brand-new stove, and why the manual has the last word.

The steps are the ones stove makers print in their own manuals, plus common fire-safety practice. Clearances, floor protection, chimney type and wood amounts differ from stove to stove, so follow the manufacturer's manual and your local code.

{FOOT}""",
    tags="wood burning sauna, sauna stove, fire safety checklist, how to light a stove, wood fired sauna, cabin checklist, chimney safety, sauna maintenance, printable checklist, free printable",
    files=["wood-sauna-stove-lighting-checklist-letter.pdf", "wood-sauna-stove-lighting-checklist-a4.pdf",
           "wood-sauna-stove-lighting-checklist.html", "preview.png"])

P["home-sauna-planning-workbook"] = dict(
    name="Home Sauna Planning Workbook", pages="7 pages",
    title="Home Sauna Planning Workbook (Printable, 7 Pages)",
    short="Free workbook for planning a home sauna: room size, site checks, a heater size worksheet, budget, questions for a licensed electrician and a timeline.",
    full=f"""Building or buying a home sauna means a dozen decisions that depend on each other. This workbook puts them in order so you can work through them with a pencil before you spend anything.

Seven pages, a cover and these six:

- The big picture: who will use it, where it goes, electric, wood or infrared, must-haves and a budget ceiling
- The room: inside dimensions, glass and stone areas, eight site checks and a grid for a sketch
- Heater size: a fill-in worksheet in feet and cubic feet, with a worked example
- Budget: sixteen cost lines with columns for estimate, quote and paid
- Questions to ask: eight for a licensed electrician, eight for a contractor or kit seller
- Timeline: twelve steps with planned and done dates, plus room for notes

The heater worksheet uses the rule of thumb that heater makers Harvia and HUUM publish: room volume, an allowance for uninsulated glass and stone, a multiplier for bare log walls, and a power range in kW. It is an estimate. Always confirm with the heater manufacturer and a licensed electrician, and follow the manufacturer's manual.

Our free online calculator does the same sums.

{FOOT}""",
    tags="home sauna, sauna planning, sauna build, heater sizing, budget worksheet, DIY sauna, home improvement planner, backyard sauna, printable workbook, free printable",
    files=["home-sauna-planning-workbook-letter.pdf", "home-sauna-planning-workbook-a4.pdf", "home-sauna-planning-workbook.html", "preview.png"])

P["sauna-buying-checklist"] = dict(
    name="Sauna Buying Checklist", pages="2 pages",
    title="Sauna Buying Checklist: Questions for the Seller",
    short="Free printable checklist for buying a ready-made sauna: 30 questions for the seller plus a page to compare three models side by side. Letter and A4.",
    full=f"""A ready-made sauna, whether a kit, a cabin or a barrel, is a big purchase, and product pages rarely answer the questions that matter once the truck has left. This checklist collects those questions in one place.

Page one has thirty questions in six groups:

- Size and fit: inside and outside size, seats, ceiling height, the way in
- Wood and build: wood species, wall thickness, glass, vents, finishes
- Heater and power: brand, model and kW, room volume in the heater manual, voltage and breaker, safety listing
- Delivery and setup: curbside or placed, weight, assembly time, who connects the heater
- Warranty and support: length, who handles claims, returns, parts
- The real price: what is included, shipping, electrician, base, extras

Page two is a table for comparing three models line by line, with five things to tick off before you pay.

It is a list of questions, not a product recommendation, and it names no brands. Heater sizing, clearances and wiring are decided by the heater manufacturer's manual and your local code. Electrical work is a job for a licensed electrician.

Take it to the showroom or keep it next to the browser tabs.

{FOOT}""",
    tags="sauna buying guide, home sauna kit, barrel sauna, buying checklist, questions to ask, comparison worksheet, outdoor sauna, home sauna, printable checklist, free printable",
    files=["sauna-buying-checklist-letter.pdf", "sauna-buying-checklist-a4.pdf", "sauna-buying-checklist.html", "preview.png"])

P["sauna-whisk-guide"] = dict(
    name="Sauna Whisk Guide", pages="1 page",
    title="Sauna Whisk Guide: Vihta, Vasta, Venik (Printable)",
    short="Free one-page guide to the sauna whisk: names, how to get a fresh, dried or frozen whisk ready, how to whisk gently, storage. US Letter and A4.",
    full=f"""A leafy whisk is one of the oldest sauna traditions and one of the least explained. This one-page guide covers the basics without the folklore.

What is on the sheet:

- The names: vihta and vasta in Finland, viht in Estonia, venik in the Russian banya, vanta in Lithuania, slota in Latvia
- Getting it ready: what to do with a fresh, a dried and a frozen whisk
- How to whisk in six steps: warm up first, shake off the water, start light, arms and legs before the back, agree on firmness with a partner, rinse and rest
- Looking after it: keep it off the stove and the stones, hang it to dry, store or freeze it
- Making your own from birch twigs in early summer
- Three points of good sense about trees, skin and house rules

We kept only the advice that Finnish and Estonian sources agree on. Where they do not agree, on how long and how warm the water for a dried whisk should be, the sheet says so and points you to the label on your whisk.

General information, not medical advice.

{FOOT}""",
    tags="sauna whisk, vihta, vasta, venik, banya, birch whisk, sauna traditions, Finnish sauna, printable guide, free printable",
    files=["sauna-whisk-guide-letter.pdf", "sauna-whisk-guide-a4.pdf", "sauna-whisk-guide.html", "preview.png"])

P["cold-plunge-safety-card"] = dict(
    name="Cold Plunge Safety card", pages="1 page",
    title="Cold Plunge Safety Card (Printable Sign)",
    short="Free printable safety card to post by a cold plunge: before you get in, when to get out right away, how to warm up after. No health claims. Letter and A4.",
    full=f"""A cold plunge next to the sauna is a simple thing, and cold water is still a real shock to the body. This card puts the plain safety points where people will see them: on the wall by the tub.

The page has four parts:

- Before you get in: never plunge alone, not after alcohol, talk to your doctor first if you have a heart or blood pressure condition or are pregnant, decide your time, ease in feet first
- Get out right away if: you go numb, shiver hard, cannot catch your breath, feel dizzy, your chest hurts, or your hands and legs stop doing what you want
- After: dry off, dress, warm up slowly
- Three short facts about what sudden cold does to breathing and the heart

One line stands out in the box: chest pain, trouble breathing, confusion, or someone who cannot get out means call 911.

The card makes no claims about what cold water does for you. The facts come from two public sources: the U.S. National Weather Service page on cold water hazards and an American Heart Association News article.

General information, not medical advice.

{FOOT}""",
    tags="cold plunge, cold plunge safety, ice bath, safety sign, cold water, sauna and cold plunge, gym signage, spa signage, printable sign, free printable",
    files=["cold-plunge-safety-card-letter.pdf", "cold-plunge-safety-card-a4.pdf", "cold-plunge-safety-card.html", "preview.png"])

P["sauna-hat-size-measuring-tape"] = dict(
    name="Printable Hat Size Measuring Tape", pages="1 page, landscape",
    title="Printable Hat Size Measuring Tape (Inches and cm)",
    short="Free printable paper tape for measuring your head: three strips join into 27 in (68.5 cm), with a scale check line for printing at 100%. Letter and A4.",
    full=f"""No tape measure in the house? Print one. This sheet has three strips that join into a paper tape 27 in (68.5 cm) long, with inches along the top edge and centimeters along the bottom.

How it works:

- Print at 100%, also called actual size
- Check the scale: the sheet has a line that is exactly 4 in, a line that is exactly 10 cm, and a line as wide as a bank card
- Cut out the three strips and tape them together at the marked tabs
- Wrap the tape around your head, across the middle of the forehead, just above the ears and around the widest part at the back

A box on the sheet explains what the number means for a sauna hat. DIVELUX wool sauna hats come in one size, about 24 in around, and the tape marks that point with a dot. A loose fit is a plus in a sauna hat. If a hat feels too big, fold the edge up.

We measured the finished PDFs: the strips and check lines are true to size in both the US Letter and the A4 file.

{FOOT}""",
    tags="printable measuring tape, hat size, head circumference, how to measure head, paper ruler, sauna hat, hat sizing, inches and centimeters, printable tool, free printable",
    files=["sauna-hat-size-measuring-tape-letter.pdf", "sauna-hat-size-measuring-tape-a4.pdf", "sauna-hat-size-measuring-tape.html", "preview.png"])

P["spa-sauna-signs-set"] = dict(
    name="Spa and Sauna Signs set", pages="10 pages, landscape",
    title="Spa and Sauna Signs Set (8 Printable Signs)",
    short="Eight free printable signs for spas, gyms and clubs: Quiet zone, Shower before sauna, Sit on a towel, No phones, Sauna in use and more. Letter and A4.",
    full=f"""Good signs save staff from repeating the same sentence all day. This set has eight of the ones a sauna area needs most, in one calm style that does not shout.

The signs:

- Quiet zone
- Shower before sauna
- Sit on a towel
- No phones
- Keep the door closed
- Shoes off
- Sauna in use
- Sauna free

Each sign has a large pictogram, a headline you can read from across the room and one friendly line of explanation. "Sauna in use" and "Sauna free" work as a pair on a door hook for private or bookable saunas.

The PDF has ten landscape pages: eight full-page signs, then two sheets with four small signs each (4.7 x 3.35 in) for lockers, doors and shelves. US Letter and A4 are both included, with the HTML source if you want to change the wording.

Paper does not last inside a hot room. Hang the signs outside the sauna door, in the changing room or by the showers, and laminate them where it is damp. For a bigger sign, a print shop can scale the PDF to 11 x 17 in or A3.

{FOOT}""",
    tags="spa signs, sauna signs, quiet zone sign, no phones sign, gym signage, locker room signs, shower before sauna, facility signage, printable signs, free printable",
    files=["spa-sauna-signs-set-letter.pdf", "spa-sauna-signs-set-a4.pdf", "spa-sauna-signs-set.html", "preview.png"])

ORDER = list(P)


def main():
    bad = 0
    for slug in ORDER:
        p = P[slug]
        d = os.path.join(C.ROOT, slug)
        words = len(re.findall(r"[A-Za-zÀ-ÿ0-9°'’\-]+", p["full"]))
        links = re.findall(r"https://diveluxsaunahat\.com\S*", p["full"])
        text = (p["full"] + p["short"] + p["title"]).lower()
        checks = [(len(p["title"]) <= 60, f"title {len(p['title'])} chars"), (len(p["short"]) <= 160, f"short {len(p['short'])} chars"),
                  (150 <= words <= 220, f"full {words} words"), (1 <= len(links) <= 2, f"{len(links)} links"),
                  (all(os.path.exists(os.path.join(d, f)) for f in p["files"]), "a listed file is missing"),
                  (not [b for b in BANNED if b in text], "banned word: " + ", ".join(b for b in BANNED if b in text))]
        missing = sorted(set(os.listdir(d)) - set(p["files"]) - {"LISTING.md"})
        ok = all(c for c, _ in checks) and not missing
        bad += not ok
        print(f"{'OK' if ok else '!!'} {slug}: title {len(p['title'])}, short {len(p['short'])}, full {words} words, {len(links)} links",
              [m for c, m in checks if not c], ("unlisted files: " + ", ".join(missing)) if missing else "")
        files = "\n".join(f"- `{f}`" for f in p["files"])
        land = "11 x 8.5 in landscape" if "landscape" in p["pages"] else "8.5 x 11 in"
        C.write(os.path.join(d, "LISTING.md"), f"""# LISTING: {p['name']}

## Title (max 60 characters)
{p['title']}

## Short description (max 160 characters)
{p['short']}

## Full description
{p['full']}

## Tags
{p['tags']}

## License
{LICENSE}

## Files
{files}

## Metadata
- Author / publisher: DIVELUX
- Format: PDF, US Letter ({land}) and A4; {p['pages']}
- Language: English (en-US) · Version 1.0 · 2026-11
- Price: free
""")
    # README: add or refresh the wave 2 rows right after the wave 1 table; nothing else in the file is rewritten
    path = os.path.join(C.ROOT, "README.md")
    txt = open(path, encoding="utf-8").read()
    rows = "\n".join(
        f"| {i} | [{P[s]['name']}]({s}/) | ![{P[s]['name']}]({s}/preview.png) | {P[s]['pages']} | "
        + "<br>".join(f"[`{f}`]({s}/{f})" for f in P[s]["files"] if f != "preview.png") + " |"
        for i, s in enumerate(ORDER, 12))
    if "| 12 | [" in txt:
        a = txt.index("| 12 | [")
        b = txt.index("\n\n", a)
        txt = txt[:a] + rows + txt[b:]
    else:
        a = txt.index("| 11 | [")
        b = txt.index("\n", a)
        txt = txt[:b + 1] + rows + txt[b:]
    open(path, "w", encoding="utf-8").write(txt)
    print("listing problems:", bad)


if __name__ == "__main__":
    main()
