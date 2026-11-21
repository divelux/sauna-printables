#!/usr/bin/env python3
"""Wave 3: writes LISTING.md into the four new printable folders (P055, P056, P057, P059).
Same format and limits as listings2.py: title <= 60 characters, short description <= 160, full description 150-220 words
with one or two links, no banned words. printables/README.md is not touched here."""
import os
import re

import common as C
from listings import BANNED, LICENSE

FOOT = ("Made by DIVELUX, makers of wool sauna hats: https://diveluxsaunahat.com\n"
        "More free sauna printables and tools: https://diveluxsaunahat.com/pages/sauna-tools")
P = {}

P["sauna-hat-embroidery-monogram-patterns"] = dict(
    name="Sauna Hat Embroidery and Monogram Patterns", pages="7 pages, true size",
    title="Sauna Hat Embroidery and Monogram Patterns",
    short="Free hand embroidery patterns for wool felt hats: two monogram alphabets, eight sauna motifs and a leaf wreath, all true size. US Letter and A4.",
    full=f"""Patterns for adding initials or a small sauna motif to a wool felt hat.

Seven pages:

- Eight basic stitches with diagrams
- A single-line alphabet, A to Z, about 7/8 in tall, for back stitch or stem stitch, with three monogram layouts
- An outline alphabet with numbers for satin stitch
- Eight motifs at true size: steam, snowflake, birch sprig, spruce, ladle, sauna stones, flame and a cabin, plus a leaf wreath for one initial
- Where to stitch on a bell hat and a bucket hat, with a 6 in spacing strip
- Water-free ways to transfer a design, and how to finish neatly
- A transfer sheet to print on tear-away stabilizer or trace onto tissue paper

Every pattern page has 1 in and 2 cm check squares, so you can confirm the print is true to size. The hat stays dry. The pack starts with water-free transfer methods, and if you choose a wash-away stabilizer, it shows how to dab off only the leftovers with cool, room-temperature water.

{FOOT}""",
    tags="embroidery pattern, monogram alphabet, hand embroidery, felt hat, sauna hat, stitch guide, embroidery motifs, snowflake embroidery, free printable, DIY gift",
    files=["sauna-hat-embroidery-monogram-patterns-letter.pdf", "sauna-hat-embroidery-monogram-patterns-a4.pdf",
           "sauna-hat-embroidery-monogram-patterns.html", "preview.png"])

P["felt-applique-templates-for-hats"] = dict(
    name="Felt Appliqué Templates for Hats", pages="4 pages, true size",
    title="Felt Appliqué Templates for Hats (Printable)",
    short="Ten free felt appliqué templates at true size: birch leaf, spruce, snowflake, star, heart, flame, steam, ladle, drop and name patches. Letter and A4.",
    full=f"""Cut-out shapes for decorating a wool felt hat, a tote bag, a towel tag or a gift box. Every template is printed at true size with two lines: a solid line to cut on and a dashed line about 1/8 in inside it to stitch along.

Four pages:

- How it works: what you need, six steps from printing to stitching, and diagrams of blanket stitch, whip stitch and running stitch
- Templates 1: birch leaf in two sizes, star, spruce, snowflake and heart
- Templates 2: flame with a separate center piece, steam cloud, water drop, ladle, and a round and a scalloped name patch
- Ideas: leaves behind a name patch, small snowflakes around a brim, and a flame for a bag or a gift box, plus care notes

Each template page carries 1 in and 2 cm check squares and the size of every shape. Print at 100% and measure before you cut.

The pack asks you to sew the pieces on rather than glue them. Hot glue and iron-on adhesives can soften in sauna heat, and a few stitches hold for years. Wool or wool-blend craft felt works best.

{FOOT}""",
    tags="felt applique, applique templates, felt shapes, felt crafts, sewing templates, snowflake template, leaf template, hat decorating, free printable, kids crafts",
    files=["felt-applique-templates-for-hats-letter.pdf", "felt-applique-templates-for-hats-a4.pdf",
           "felt-applique-templates-for-hats.html", "preview.png"])

P["sauna-gnome-story-coloring"] = dict(
    name="The Sauna Tonttu: story and coloring pages", pages="8 pages",
    title="The Sauna Tonttu: A Story and Coloring Book for Kids",
    short="A free read-aloud story inspired by Finnish folklore: Aino and her grandmother visit the lake sauna. With a note for grown-ups and four coloring pages.",
    full=f"""A short picture-book story for children aged about 4 to 8, inspired by Finnish folklore.

On a Saturday evening, Aino and her grandmother, Mummo, walk down to the little sauna by the lake. Before they go in, they say hello to the sauna tonttu, the small keeper who looks after the stove and the benches and likes a sauna where people are calm and kind. Aino learns where to sit, why only grown-ups pour water on the stones, and the most important rule of all: when you feel too hot, you go out.

Eight pages:

- Cover
- The story, about 680 words over two pages
- A page for grown-ups: what the tonttu is in Finnish folk belief, with sources, a few Finnish words, and a short checklist for taking children to the sauna
- Four coloring pages: by the warm stove, tidy benches, night by the lake, and your own tonttu to decorate

The story and the characters are new; it does not claim to retell any one traditional tale. All the artwork is clean vector line art drawn for this book.

General information, not medical advice.

{FOOT}""",
    tags="sauna tonttu, Finnish folklore, kids story, read aloud, coloring pages, gnome coloring, sauna for kids, bedtime story, free printable, Finland",
    files=["sauna-gnome-story-coloring-letter.pdf", "sauna-gnome-story-coloring-a4.pdf",
           "sauna-gnome-story-coloring.html", "preview.png"])

P["sauna-ritual-cards-for-sauna-masters"] = dict(
    name="Sauna Ritual Cards for sauna masters", pages="7 pages, 27 cards",
    title="Sauna Ritual Cards for Sauna Masters (27 Aufguss Cards)",
    short="27 free printable cards for planning an Aufguss or a sauna evening: room, pour, towel waves, scents, music and cool-down. 9 per sheet, duplex backs.",
    full=f"""27 cards for sauna masters, spa staff and home sauna hosts who plan an Aufguss.

Six colors, six parts of a session:

- Prepare (5): heat up in good time, mix the bucket at the label dose, fresh towels, ask about scents and allergies, door closed before the first pour
- Pour (5): three rounds that build gently, slow pours, stones not the heater, an ice ball, reading the room
- Towel (6): the basic wave, the helicopter, one guest at a time, two towels, throw and catch, towel manners
- Scent (5): forest, fresh, herbal infusion, less is more, scent-sensitive guests
- Music and story (3): music, a simple theme, a clear opening and ending
- Cool down (3): fresh air first, then cool water, then rest; water to drink; safety first

The cover sheet explains printing and gives a sample evening. Cards print nine per sheet at 2.5 x 3.5 in with crop marks, with mirrored backs for long-edge duplex printing.

Cards with specific points name their source: the Aufguss WM evaluation catalogue, a German accident-insurance study on sauna infusions (DGUV), and a German health insurer's sauna guide. No medical claims.

{FOOT}""",
    tags="aufguss, sauna master, sauna ritual, towel waving, sauna infusion, essential oils sauna, spa training, sauna host, printable cards, free printable",
    files=["sauna-ritual-cards-for-sauna-masters-letter.pdf", "sauna-ritual-cards-for-sauna-masters-a4.pdf",
           "sauna-ritual-cards-for-sauna-masters.html", "preview.png"])

ORDER = list(P)
EXTRA_BANNED = ["wet the felt", "damp the hat", "soak the hat", "best-selling", "reviews"]


def main():
    bad = 0
    for slug in ORDER:
        p = P[slug]
        d = os.path.join(C.ROOT, slug)
        words = len(re.findall(r"[A-Za-zÀ-ÿ0-9°'’\-]+", p["full"]))
        links = re.findall(r"https://diveluxsaunahat\.com\S*", p["full"])
        text = (p["full"] + p["short"] + p["title"]).lower()
        hits = [b for b in BANNED + EXTRA_BANNED if b in text]
        checks = [(len(p["title"]) <= 60, f"title {len(p['title'])} chars"), (len(p["short"]) <= 160, f"short {len(p['short'])} chars"),
                  (150 <= words <= 220, f"full {words} words"), (1 <= len(links) <= 2, f"{len(links)} links"),
                  (all(os.path.exists(os.path.join(d, f)) for f in p["files"]), "a listed file is missing"),
                  (not hits, "banned word: " + ", ".join(hits))]
        missing = sorted(set(os.listdir(d)) - set(p["files"]) - {"LISTING.md"})
        ok = all(c for c, _ in checks) and not missing
        bad += not ok
        print(f"{'OK' if ok else '!!'} {slug}: title {len(p['title'])}, short {len(p['short'])}, full {words} words, {len(links)} links",
              [m for c, m in checks if not c], ("unlisted files: " + ", ".join(missing)) if missing else "")
        files = "\n".join(f"- `{f}`" for f in p["files"])
        n = re.search(r"(\d+) pages?", p["pages"]).group(1)
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
- Format: PDF, US Letter (8.5 x 11 in) and A4; {n} pages{'; print at 100% (true size)' if 'true size' in p['pages'] else ''}
- Language: English (en-US) · Version 1.0 · 2026-11
- Price: free
""")
    print("listing problems:", bad)


if __name__ == "__main__":
    main()
