#!/usr/bin/env python3
"""Writes LISTING.md into every product folder and README.md into printables/. Checks the length limits:
title <= 60 characters, short description <= 160, full description 150-220 words with one or two links."""
import os
import re

import common as C

LICENSE = ("Text and layout: CC BY 4.0 (Creative Commons Attribution 4.0 International). "
           "Credit: DIVELUX, https://diveluxsaunahat.com\n"
           "The DIVELUX name and logo are © DIVELUX Inc. and are not covered by the license. "
           "Fonts in the PDFs: Bricolage Grotesque and Inter (SIL Open Font License 1.1).")

P = {}

P["home-sauna-rules-poster"] = dict(
    name="Home Sauna Rules poster", pages="1 page",
    title="Home Sauna Rules Poster (Free Printable)",
    short="Free printable poster with ten calm house rules for a home sauna: shower first, sit on a towel, ask before you pour, cool down and rest. US Letter and A4.",
    full="""Every home sauna ends up with house rules. Usually they live in the owner's head and get explained again to each new guest at the door. This poster puts them on the wall instead.

Home Sauna Rules is a one-page printable with ten short rules in a calm, friendly tone: shower first, sit on a towel, close the door fast, ask before you pour, sit where it feels right, step out any time, cool down and rest, drink water, keep it quiet, and air the room out when you leave. Each rule has one line that explains why. A small heat ladder at the top shows why the top bench is the hottest seat.

The design is typographic and easy to read from across a changing room. It prints cleanly on a home printer and looks good in a simple frame. Hang it outside the hot room, where paper lasts.

- US Letter and A4 PDF, one page each
- HTML source included
- No sign-up, nothing to pay

The rules are general etiquette, not medical advice.

Made by DIVELUX, makers of wool sauna hats in Irvine, California: https://diveluxsaunahat.com
More free sauna printables and tools: https://diveluxsaunahat.com/pages/sauna-tools""",
    tags="sauna, home sauna, sauna rules, sauna poster, sauna sign, sauna etiquette, printable poster, wall art, cabin decor, free printable",
    files=["home-sauna-rules-poster-letter.pdf", "home-sauna-rules-poster-a4.pdf", "home-sauna-rules-poster.html", "preview.png"])

P["sauna-etiquette-poster"] = dict(
    name="Sauna Etiquette poster for gyms and spas", pages="1 page, 3 versions",
    title="Sauna Etiquette Poster for Gyms and Spas (Editable)",
    short="Free sauna etiquette poster for gyms, spas and clubs. Ten short courtesies, a neutral version, and an editable file where you add your venue name.",
    full="""A shared sauna works when everyone follows the same few courtesies. Most people are glad to, as long as someone tells them what the courtesies are. This poster does that without sounding like a warning label.

Sauna Etiquette lists ten rules for a gym, spa, hotel or club sauna: shower first, sit on a towel, dress as posted, close the door quickly, check before you pour, keep it quiet, no phones or cameras, the bench is for sitting, share the space, and listen to your body.

Three versions are included:

- Standard poster with a small DIVELUX wordmark in the header
- Neutral poster with no logo, only a one-line credit at the bottom
- Editable HTML file: type your venue name, choose the heater rule (ask first, staff only, or no water), pick US Letter or A4, rewrite any line, and print or save as PDF. It works offline in any modern browser. Step-by-step notes are in EDITING.md.

PDFs come in US Letter and A4. For a larger sign, a print shop can scale the PDF to 11 x 17 in or A3.

General information, not medical advice. Your own posted rules and local regulations come first.

Made by DIVELUX, makers of wool sauna hats: https://diveluxsaunahat.com
More free sauna tools: https://diveluxsaunahat.com/pages/sauna-tools""",
    tags="sauna etiquette, gym sauna rules, spa signage, sauna sign, health club, hotel spa, editable poster, printable sign, facility signage, free printable",
    files=["sauna-etiquette-poster-letter.pdf", "sauna-etiquette-poster-a4.pdf", "sauna-etiquette-poster-neutral-letter.pdf",
           "sauna-etiquette-poster-neutral-a4.pdf", "sauna-etiquette-poster-editable.html", "EDITING.md",
           "sauna-etiquette-poster.html", "preview.png"])

P["wool-sauna-hat-care-card"] = dict(
    name="Wool Sauna Hat Care card", pages="2 cards per sheet + 4 x 6 in",
    title="Wool Sauna Hat Care Card (Printable)",
    short="Free printable care card for a wool felt sauna hat: wear it dry, hand wash in cool room-temperature water, squeeze, air dry. Two per sheet plus 4 x 6 in.",
    full="""A wool felt sauna hat needs very little care, but the few rules matter. This card puts the whole routine on one small sheet you can keep with the hat or tuck into a gift.

What the card says:

- Wear the hat dry. Put it on before you step into the heat.
- A loose fit is a plus. If the hat feels too big, fold the edge up.
- After the sauna, hang it by the loop until it is fully dry.
- Wash only when it needs it, by hand, in cool, room-temperature water (about 20–24 °C / 68–75 °F, never warm or hot), with a little mild soap.
- Squeeze the water out. Do not wring.
- Reshape by hand and air dry, away from heaters.
- Never: washing machine, dryer, warm or hot water.

Files included:

- Two cards per sheet on US Letter and A4, with cut lines (each card is 4.72 x 7.08 in)
- A single 4 x 6 in card, ready for a photo printer or a 4 x 6 frame
- HTML source

Print at 100% on heavy paper.

Made by DIVELUX, makers of handmade wool sauna hats: https://diveluxsaunahat.com
More free sauna printables: https://diveluxsaunahat.com/pages/sauna-tools""",
    tags="sauna hat, wool felt care, how to wash a sauna hat, banya hat, care card, care instructions, wool care, gift insert, printable card, free printable",
    files=["wool-sauna-hat-care-card-letter.pdf", "wool-sauna-hat-care-card-a4.pdf", "wool-sauna-hat-care-card-4x6.pdf",
           "wool-sauna-hat-care-card.html", "preview.png"])

P["sauna-temperature-conversion-chart"] = dict(
    name="Sauna Temperature Conversion chart", pages="1 page",
    title="Sauna Temperature Conversion Chart, °F to °C",
    short="Free printable °F to °C chart for the sauna, 100 to 230 °F, with typical temperature ranges for 13 sauna types marked on the scale. Letter and A4.",
    full="""Sauna thermometers, heater manuals and travel guides do not agree on units. A Finnish heater dial reads in Celsius, an American gym posts Fahrenheit, and a friend back from a banya says it was "ninety degrees." This chart settles it at a glance.

The page is a tall dual scale for the hot-room range, 100 to 230 °F, with °F on the left and °C on the right. Next to the scale, thirteen bars show the air temperature range that each type of sauna is usually quoted at: steam room, Turkish hammam, infrared, bio sauna, Korean jjimjilbang, Russian banya, North American gym sauna, Swedish bastu, Norwegian badstue, Finnish and Estonian sauna, German Aufguss sauna and Japanese sauna.

Under the chart there is a small lookup table for every 10 °F and both conversion formulas.

The ranges are commonly quoted reference figures, not measurements. They come from our open dataset, Sauna Traditions of the World, and the chart is generated directly from it. Real rooms vary with the stove, the bench height and local habit. This is general information, not medical advice.

- US Letter and A4 PDF, one page each
- HTML source included

Made by DIVELUX, makers of wool sauna hats: https://diveluxsaunahat.com
More free sauna tools and the dataset: https://diveluxsaunahat.com/pages/sauna-tools""",
    tags="sauna temperature, Fahrenheit to Celsius, temperature conversion chart, sauna chart, banya, steam room, infrared sauna, reference chart, printable chart, free printable",
    files=["sauna-temperature-conversion-chart-letter.pdf", "sauna-temperature-conversion-chart-a4.pdf",
           "sauna-temperature-conversion-chart.html", "preview.png"])

P["sauna-types-cheat-sheet"] = dict(
    name="Sauna Types cheat sheet", pages="1 page",
    title="Sauna Types Cheat Sheet: 12 Types on One Page",
    short="Free one-page cheat sheet comparing 12 sauna types: Finnish, banya, steam room, infrared, hammam and more, with typical temperature and humidity.",
    full="""Finnish sauna, banya, steam room, infrared cabin, hammam: the names get used loosely, and the rooms behind them are very different. This cheat sheet puts twelve of them side by side on one page.

For each type you get where it comes from and how it is heated, the commonly quoted air temperature in °F and °C with a small range bar, the usual humidity, the typical length of one round, whether water goes on the stones, and one line on what to expect.

Types covered: Finnish sauna, smoke sauna, Russian banya, Lithuanian pirtis and Latvian pirts, German Aufguss sauna, bio sauna, infrared sauna, steam room, Turkish hammam, Japanese sauna, Korean jjimjilbang, and the North American gym or club sauna.

Nothing on the sheet is invented. The numbers are read directly from our open dataset, Sauna Traditions of the World. Where published figures disagree, the sheet says "not stated" instead of guessing. The figures are reference ranges, not measurements, and round lengths are typical habits, not recommendations. General information, not medical advice.

- US Letter and A4 PDF, one page each
- HTML source included

Made by DIVELUX, makers of wool sauna hats: https://diveluxsaunahat.com
More free sauna tools: https://diveluxsaunahat.com/pages/sauna-tools""",
    tags="sauna types, types of saunas, Finnish sauna, Russian banya, infrared sauna, steam room, hammam, comparison chart, cheat sheet, free printable",
    files=["sauna-types-cheat-sheet-letter.pdf", "sauna-types-cheat-sheet-a4.pdf", "sauna-types-cheat-sheet.html", "preview.png"])

P["home-sauna-guest-book"] = dict(
    name="Home Sauna Guest Book", pages="7 pages",
    title="Home Sauna Guest Book (Printable, 7 Pages)",
    short="Free printable guest book for a home sauna: cover, visit log with date, guests and temperature, guest entry pages, sauna records. Letter and A4.",
    full="""A home sauna collects stories: the first snow night, the cousin who lasted two minutes, the evening nobody wanted to leave. A guest book keeps them. This one is made to be printed at home and to grow as long as the sauna is in use.

Seven pages are included:

- Cover with a line for the name of your sauna
- About this sauna: built when, heated by what, favorite temperature, house traditions
- Visit log: one line per sauna night with date, guests, temperature, rounds and a note
- Guest entries: four roomy boxes per page for a few sentences or a drawing
- Sauna records: hottest session, coldest plunge, most guests on the benches and other friendly records
- Regulars: a tally of visits for the people who keep coming back
- Notes and stories: a lined page

Print the cover and the "about" page once, and print the log and entry pages as many times as you need. The left margin is wide enough for a hole punch or staples. Keep the book in the lounge, not in the hot room.

- US Letter and A4 PDF, seven pages each
- HTML source included

Made by DIVELUX, makers of wool sauna hats: https://diveluxsaunahat.com
More free sauna printables: https://diveluxsaunahat.com/pages/sauna-tools""",
    tags="sauna guest book, home sauna, sauna log, guest book printable, cabin guest book, sauna journal, logbook pages, sauna gift, planner pages, free printable",
    files=["home-sauna-guest-book-letter.pdf", "home-sauna-guest-book-a4.pdf", "home-sauna-guest-book.html", "preview.png"])

P["sauna-evening-gift-certificate"] = dict(
    name="Sauna Evening gift certificate + gift tags", pages="2 pages",
    title="Sauna Evening Gift Certificate and Gift Tags",
    short="Free printable gift certificate for a sauna evening, two per sheet, plus a sheet of eight gift tags. Fill in the names, cut, and give. Letter and A4.",
    full="""The best sauna gift is often an evening: the stove lit, fresh towels, tea, and nowhere else to be. This printable turns that promise into something you can hand over.

Page one has two gift certificates. Each one reads "A sauna evening: good for one unhurried evening of heat, steam and rest," with lines for who it is for, who it is from, a few words of your own, and a "good until" date. A row of checkboxes shows what is included: hot sauna, cold plunge or cool shower, fresh towels, tea, snacks, a hat to borrow.

Page two has eight gift tags, 3.5 x 2.25 in each, with To and From lines and a marked hole for string. The messages include "For your next sauna," "Warm wishes," "Good steam to you," the Finnish wish "Hyviä löylyjä!" and the Russian banya greeting "S lyogkim parom!" with a short translation under each.

Print at 100% on heavy paper or card stock and cut along the dashed lines. It also works as a card to go with a sauna gift.

- US Letter and A4 PDF, two pages each
- HTML source included

Made by DIVELUX, makers of wool sauna hats: https://diveluxsaunahat.com
More free sauna printables: https://diveluxsaunahat.com/pages/sauna-tools""",
    tags="gift certificate, sauna gift, gift tags, printable voucher, gift coupon, sauna lover gift, last-minute gift, holiday gift tags, experience gift, free printable",
    files=["sauna-evening-gift-certificate-letter.pdf", "sauna-evening-gift-certificate-a4.pdf",
           "sauna-evening-gift-certificate.html", "preview.png"])

P["sauna-words-poster"] = dict(
    name="Sauna Words poster", pages="1 page",
    title="Sauna Words Poster: A Glossary in 7 Languages",
    short="Free printable poster of 47 sauna words in seven languages, from Finnish löyly to German Aufguss, each with a short plain-English meaning.",
    full="""Sauna culture has its own vocabulary, and most of it does not translate into one English word. Löyly is not just "steam." An Aufguss is not just "pouring water." This poster collects the words bathers use and explains each one in a few plain words.

Forty-seven words in seven languages:

- Finnish: sauna, löyly, kiuas, lauteet, vihta and vasta, kiulu, kauha, savusauna, avanto, saunahattu
- Russian, in Latin letters with Cyrillic beside each word: banya, parilka, par, venik, kamenka, polok, shaika, predbannik, and the greeting "S lyogkim parom!"
- German: Aufguss, Saunameister, Saunagang, Saunahut, Ruheraum, Tauchbecken, Dampfbad, textilfrei
- Estonian: saun, leil, keris, viht, saunalava, suitsusaun, saunamüts, "Hüva leili!"
- Swedish, Lithuanian and Latvian: four words each, including bastu, pirtis and pirts

We only included words we could confirm, in our own open dataset of sauna traditions, in dictionary entries, or in published usage. Words we were not sure about were left out. The glosses are short on purpose; usage varies by region and family.

Hang it in the lounge, the changing room or a sauna showroom, or use it as a quiz sheet on sauna night.

- US Letter and A4 PDF, one page each
- HTML source included

Made by DIVELUX, makers of wool sauna hats: https://diveluxsaunahat.com
More free sauna printables: https://diveluxsaunahat.com/pages/sauna-tools""",
    tags="sauna words, sauna glossary, löyly, Aufguss, banya, Finnish sauna, sauna vocabulary, language poster, wall art, free printable",
    files=["sauna-words-poster-letter.pdf", "sauna-words-poster-a4.pdf", "sauna-words-poster.html", "preview.png"])

P["sauna-word-search-crossword"] = dict(
    name="Sauna word search + crossword", pages="3 pages",
    title="Sauna Word Search and Crossword (With Answers)",
    short="Two free printable sauna puzzles: a 28-word word search and a 27-clue crossword, with both answer keys on a separate page. Letter and A4.",
    full="""Something to do in the lounge between rounds, at a sauna party, or on a quiet evening when the stove is heating up.

Page one is a word search: a 15 x 15 grid with 28 sauna words hidden across, down and diagonally, forward and backward. The list runs from SAUNA, BANYA and HAMMAM to LADLE, WHISK and FELT.

Page two is a crossword with 27 clues about the hot room and the bathing traditions around it. A few examples: "The top one is the hottest seat." "German steam ritual led by a sauna master with a towel." The number in brackets after each clue is the length of the answer.

Page three has both answer keys, so you can print the puzzles on their own and keep the answers out of sight.

Both grids were generated by a program and then checked by a second one: every word in the word search appears exactly once, and every run of letters in the crossword matches a numbered clue.

Löyly is spelled LOYLY in the grids.

- US Letter and A4 PDF, three pages each
- HTML source included

Made by DIVELUX, makers of wool sauna hats: https://diveluxsaunahat.com
More free sauna printables: https://diveluxsaunahat.com/pages/sauna-tools""",
    tags="word search, crossword, sauna, printable puzzle, party game, activity sheet, sauna trivia, spa activity, puzzle with answers, free printable",
    files=["sauna-word-search-crossword-letter.pdf", "sauna-word-search-crossword-a4.pdf",
           "sauna-word-search-crossword.html", "puzzles.json", "preview.png"])

P["sauna-care-cleaning-schedule"] = dict(
    name="Sauna Care and Cleaning schedule", pages="2 pages",
    title="Sauna Care and Cleaning Schedule (Printable)",
    short="Free printable cleaning schedule for a home sauna: what to do after every session, weekly, monthly and once a year, plus a maintenance log page.",
    full="""A sauna stays fresh when a few small habits happen on time. This schedule lists them by how often they come up.

Page one is the schedule:

- After every session: air the room out, wipe the benches with plain water, empty the bucket, take towels and hats out to dry, check that the heater is off
- Every week: sweep and mop the floor, wash the benches with warm water and a soft brush, rinse the bucket and ladle, clean the glass door
- Every month: look over the benches and sand rough spots, check the door, vents, heater guard and light
- Once a year: restack the stones and discard cracked ones, have the electrics checked, sweep the chimney of a wood stove, deep-clean the benches, test the alarms

Three standing rules: no harsh chemicals on wood, heater manual first, electrics by a qualified electrician.

Page two is a maintenance log with space for dates, what was done, and when it is due next.

The advice is general. Where your manufacturer's instructions differ, follow them.

- US Letter and A4 PDF, two pages each
- HTML source included

Made by DIVELUX, makers of wool sauna hats: https://diveluxsaunahat.com
More free sauna tools: https://diveluxsaunahat.com/pages/sauna-tools""",
    tags="sauna cleaning, sauna maintenance, home sauna, cleaning schedule, maintenance checklist, sauna care, sauna stones, home maintenance, printable checklist, free printable",
    files=["sauna-care-cleaning-schedule-letter.pdf", "sauna-care-cleaning-schedule-a4.pdf",
           "sauna-care-cleaning-schedule.html", "preview.png"])

P["sauna-bingo"] = dict(
    name="Sauna Bingo", pages="7 pages",
    title="Sauna Bingo: 6 Printable Cards and Rules",
    short="Free printable sauna bingo for a group: six different 5 x 5 cards and a rules page. Friendly things to notice on a sauna night. No dares, no drinking.",
    full="""Sauna bingo is a quiet game for a sauna evening. Nobody has to do anything. You just notice the small things that happen on every good sauna night and mark them on your card between rounds.

The squares are things like "Water hisses on the stones," "Glasses fog up," "Someone says one more round," "A hat gets a compliment," "A full minute of easy silence" and "Plans for the next sauna night." There are 42 of them, mixed differently on each card, with a free square in the middle.

What you get:

- Six different 5 x 5 cards, lettered A to F, one per page; no two share a row or column
- A rules page: how to play, fair play, and a longer "blackout" version for the whole season
- US Letter and A4 PDF, seven pages each, plus the HTML source

The game is built to stay harmless. Squares only count when they happen on their own. There are no dares, no drinking squares, and nothing that rewards staying in the heat longer. Cards and pens stay in the lounge, and anyone can step out whenever they like.

Made by DIVELUX, makers of wool sauna hats: https://diveluxsaunahat.com
More free sauna printables: https://diveluxsaunahat.com/pages/sauna-tools""",
    tags="sauna bingo, bingo cards, party game, sauna night, group game, printable game, family game, spa party, icebreaker, free printable",
    files=["sauna-bingo-letter.pdf", "sauna-bingo-a4.pdf", "sauna-bingo.html", "preview.png"])

ORDER = ["home-sauna-rules-poster", "sauna-etiquette-poster", "wool-sauna-hat-care-card", "sauna-temperature-conversion-chart",
         "sauna-types-cheat-sheet", "home-sauna-guest-book", "sauna-evening-gift-certificate", "sauna-words-poster",
         "sauna-word-search-crossword", "sauna-care-cleaning-schedule", "sauna-bingo"]
BANNED = ["delve", "elevate", "unlock", "seamless", "game-changer", "tapestry", "realm", "embark", "testament", "boost",
          "detox", "toxins", "cure", "heals", "burns fat", "immune", "amazon", "best seller", "wet the hat", "soak"]


def main():
    bad = 0
    for slug in ORDER:
        p = P[slug]
        d = os.path.join(C.ROOT, slug)
        words = len(re.findall(r"[A-Za-zÀ-ÿ0-9°'’\-]+", p["full"]))
        links = re.findall(r"https://diveluxsaunahat\.com\S*", p["full"])
        checks = [(len(p["title"]) <= 60, f"title {len(p['title'])} chars"), (len(p["short"]) <= 160, f"short {len(p['short'])} chars"),
                  (150 <= words <= 220, f"full {words} words"), (1 <= len(links) <= 2, f"{len(links)} links"),
                  (all(os.path.exists(os.path.join(d, f)) for f in p["files"]), "a listed file is missing"),
                  (not [b for b in BANNED if b in (p["full"] + p["short"] + p["title"]).lower()], "banned word")]
        missing = sorted(set(os.listdir(d)) - set(p["files"]) - {"LISTING.md"})
        status = "OK" if all(ok for ok, _ in checks) and not missing else "!!"
        if status != "OK":
            bad += 1
        print(f"{status} {slug}: title {len(p['title'])}, short {len(p['short'])}, full {words} words, {len(links)} links",
              [m for ok, m in checks if not ok], ("unlisted files: " + ", ".join(missing)) if missing else "")
        files = "\n".join(f"- `{f}`" for f in p["files"])
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
- Format: PDF, US Letter (8.5 x 11 in) and A4; {p['pages']}
- Language: English (en-US) · Version 1.0 · 2026-11
- Price: free
""")
    rows = "\n".join(
        f"| {i} | [{P[s]['name']}]({s}/) | ![{P[s]['name']}]({s}/preview.png) | {P[s]['pages']} | "
        + "<br>".join(f"[`{f}`]({s}/{f})" for f in P[s]["files"] if f != "preview.png") + " |"
        for i, s in enumerate(ORDER, 1))
    C.write(os.path.join(C.ROOT, "README.md"), f"""# DIVELUX sauna printables, wave 1

Eleven free printables for sauna owners, guests, gyms and spas. Every product has a US Letter PDF, an A4 PDF,
the HTML source, a `preview.png` and a `LISTING.md` with ready-to-paste title, descriptions, tags and license.

Made by DIVELUX, makers of wool sauna hats: https://diveluxsaunahat.com ·
more free tools: https://diveluxsaunahat.com/pages/sauna-tools

| # | Printable | Preview | Size | Files |
|---|---|---|---|---|
{rows}

## Printing

- Print at 100% (actual size). In a browser print dialog also set margins to "None" and turn on "Background graphics".
- Posters and charts look best on heavier matte paper. Cards, certificates and tags want card stock.
- Paper does not last inside a hot room. Hang posters in the changing room or lounge, or laminate them.
- The HTML sources are self-contained (fonts are embedded). Open one in a browser and add `?paper=a4` to the address for A4.

## License

{LICENSE}

Every sheet carries the credit line "Free to print and share — DIVELUX wool sauna hats — diveluxsaunahat.com".
Please keep it when you share or adapt the files.

## Rebuilding

Sources live in `_build/`. `python3 _build/build.py` writes the HTML, renders the PDFs with Playwright
(one Chromium at a time, under `flock /tmp/freebies-chromium.lock`), adds PDF metadata and checks every page for
overflow, page size, page count and a live link. `python3 _build/build.py p04 p09` rebuilds only some products.
`python3 _build/verify_puzzles.py` re-checks the word search and the crossword against the finished PDFs.
`python3 _build/listings.py` rewrites the LISTING.md files and this README and checks their length limits.

Temperatures and sauna-type facts are read from the open dataset in `../dataset/` (Sauna Traditions of the World);
nothing is typed in by hand. General information, not medical advice.
""")
    print("listing problems:", bad)


if __name__ == "__main__":
    main()
