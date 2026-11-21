"""59. Sauna ritual cards for sauna masters: 27 cards (2.5 x 3.5 in), nine per sheet with crop marks, backs on their own
sheets in mirrored order for long-edge duplex printing, plus a cover sheet with how-to and sources.
Only widely described practice. Checked in November 2026 against:
  A  Aufguss WM, Evaluation Catalogue 2024 (jury criteria: heat built up over the rounds, classic waving with two hands and
     the helicopter, show techniques, waving to the music, natural aromas, safe use of water, ice and fragrance,
     hygiene: the waving towel never touches a guest, clear opening and ending, theme)
  B  DGUV Sachgebiet Bäder, final report "Gefahrstoffexposition bei Saunaaufgüssen" (24.11.2016): concentrates are mostly
     essential oils dissolved in ethanol or 2-propanol and are diluted with water; room climate about 90-100 °C measured
     1 m above the top bench; dosing above the label and fast "hard" pours gave clearly higher formaldehyde readings;
     sauna masters are trained by the Deutscher Sauna-Bund and supervise guests and give first aid
  C  BARMER, "Sauna: Wie gesund ist sie wirklich?": fresh air first, then water; gentle temperature changes; breaks between
     rounds; two to three rounds; drink in the breaks and afterwards
No medical claims."""
import os

import common as C
import w2

SLUG = "sauna-ritual-cards-for-sauna-masters"
TITLE = "Sauna Ritual Cards for Sauna Masters"
DESC = ("27 printable cards for sauna masters and home sauna hosts: preparing the room, pouring, towel waves, scents, music "
        "and story, and cooling down. Nine per sheet with crop marks and duplex backs.")
KEYWORDS = ("aufguss, sauna master, sauna ritual cards, aufguss towel techniques, sauna infusion, sauna aromas, "
            "sauna session plan, printable cards, spa staff training, DIVELUX")
NAME = "Sauna Ritual Cards"

CATS = {
    "prep": ("Prepare", "#e3ddd3", "thermometer"),
    "pour": ("Pour", "#f0a877", "bucket-ladle"),
    "towel": ("Towel", "#f5c7a0", "towel"),
    "scent": ("Scent", "#d6dcc8", "leaf"),
    "music": ("Music & story", "#ecd6b2", "lamp"),
    "cool": ("Cool down", "#c3d5d8", "cold-plunge"),
}

CARDS = [
    ("prep", "Heat up in good time", ["Give the heater time to bring the room and the stones fully up to heat.",
                                      "A German safety report describes a sauna room at about 90–100 °C (194–212 °F), measured above the top bench.",
                                      "Check your thermometer before guests come in."], "B"),
    ("prep", "Mix the bucket", ["Fresh water in a clean bucket.", "Add the infusion concentrate at the dose on its label and stir.",
                                "Never pour concentrate or neat essential oil straight onto the stones. Many contain alcohol."], "B"),
    ("prep", "Fresh towels", ["A clean, dry waving towel for every session, never one you sat on.", "Keep a spare within reach.",
                              "Hang wet towels outside the hot room."], "A"),
    ("prep", "Ask first", ["Say which scents you will use.", "Ask about allergies and sensitivity to scents.",
                           "Offer the lower benches to anyone who wants it milder.", "Anyone may leave at any time."], ""),
    ("prep", "Door closed, then begin", ["Guests in and seated before the first pour.", "Keep the door closed during each round so steam and scent stay in.",
                                         "Someone feels unwell? Open the door for them right away."], ""),
    ("pour", "Three rounds", ["The classic pattern: pour, wave, pause, three times.", "Build the heat gently from round to round.",
                              "The last round can be the strongest. Too hot from the start leaves nowhere to go."], "A"),
    ("pour", "Pour slowly", ["Spread each ladle over the stones in a slow, even stream, several seconds per ladle.",
                             "In German tests, fast pours and doses above the label gave harsher air."], "B"),
    ("pour", "Stones, not the heater", ["Aim at the stones.", "Keep water off heating elements, controls and the sensor.",
                                        "Step back as the steam rises: the first burst is the hottest."], ""),
    ("pour", "Ice ball", ["Freeze infusion water, mixed at the label dose, into a ball. Or use plain ice.",
                          "Set it on top of the stones and let it melt for a slow, steady steam.", "Place it, don’t throw it."], "A"),
    ("pour", "Read the room", ["Watch faces, not the clock.", "If guests look uncomfortable or start to leave, ease off: smaller pours, gentler waves.",
                               "Good heat feels pleasant, never like a test."], "A"),
    ("towel", "The basic wave", ["Hold the towel by two corners and lift it high.", "Push the hot air from the ceiling down toward the benches.",
                                 "Slow, even strokes. Both hands."], "A"),
    ("towel", "The helicopter", ["Spin the towel in a circle above your head to gather the hot air under the ceiling.",
                                 "Then send it down to the benches with a wave.", "One of the classic Aufguss techniques."], "A"),
    ("towel", "One guest at a time", ["A few strokes toward each guest, row by row.", "Ask before you start.",
                                      "Agree on a sign for “no thanks”, like a raised hand, and respect it."], ""),
    ("towel", "Two towels", ["A towel in each hand, waving in turn, for a steady stream of warm air.",
                             "Practice outside the sauna first. Start slow."], "A"),
    ("towel", "Throw and catch", ["Show moves only with room to move and full control.", "Keep clear of guests, the heater and the lights.",
                                  "A towel hits the floor? Swap it for a fresh one."], "A"),
    ("towel", "Towel manners", ["Never touch a guest with the waving towel.", "Keep it off the heater and the stones.",
                                "Dry towels between sessions and wash them after use."], "A"),
    ("scent", "Forest", ["Birch, pine, spruce, fir.", "Calm, familiar scents that suit a first round."], ""),
    ("scent", "Fresh", ["Citrus, mint, eucalyptus.", "Bright scents for a later round, when the heat is up."], ""),
    ("scent", "Herbal infusion", ["Steep dried herbs in hot water, strain and let it cool.", "Use the infused water in the bucket.",
                                  "Natural aromas such as infusions are part of championship scoring."], "A"),
    ("scent", "Less is more", ["One scent per round, at the label dose.", "More concentrate does not smell nicer. It makes the air sharp."], "B"),
    ("scent", "Scent-sensitive guests", ["Some guests react to scents.", "Offer an unscented round or session now and then.",
                                         "Keep the product at hand so you can show the label."], ""),
    ("music", "Pick the music", ["Quiet, steady music that matches the tempo of your waves.", "Low enough to talk over.",
                                 "Wave on the beat. Silence works too."], "A"),
    ("music", "Tell a small story", ["A theme ties scent, music and moves together: a forest morning, a winter night, a summer lake.",
                                     "Keep it simple. Guests should get it without words."], "A"),
    ("music", "Open and close", ["Welcome everyone. Say how many rounds and what is coming.", "At the end, thank the guests, say it is over and open the door."], "A"),
    ("cool", "Cool down in order", ["1 Fresh air first.", "2 Then cool water: shower, hose or plunge. Many guides start at the feet and hands.",
                                    "3 Then rest. Gentle changes are fine; ice-cold is not required."], "C"),
    ("cool", "Rest and drink", ["Rest between rounds, wrapped up warm.", "Drink water in the breaks and afterwards.",
                                "Two or three rounds are plenty for most people."], "C"),
    ("cool", "Safety first", ["Never leave guests alone in the hot room during a session.", "Know where the first-aid kit and alarm are.",
                              "Dizzy or unwell: out of the heat right away. No alcohol."], "B"),
]
assert len(CARDS) == 27

SOURCES = [
    ("A", "Aufguss WM, Evaluation Catalogue 2024 (jury criteria)",
     "https://thermea.com/uploads/attachments/cm9jyz4wm0ph60jmoeg2gcy1o-aufguss-wm-jury-catalog-2025.pdf"),
    ("B", "DGUV Sachgebiet Bäder, “Gefahrstoffexposition bei Saunaaufgüssen”, final report, 2016",
     "https://dguv.de/medien/inhalt/praevention/fachbereiche_dguv/fb-gesund_wohlfahrt/sg-baeder/ab-sauna.pdf"),
    ("C", "BARMER, “Sauna: Wie gesund ist sie wirklich?”",
     "https://www.barmer.de/gesundheit-verstehen/koerper/vorsorge-und-frueherkennung/sauna-gesund-1485228"),
]

CSS = w2.CSS + """
.page{padding:.5in .6in .34in}
h1{font-size:66pt}
.sheet{padding:0;background:#fff;align-items:center;justify-content:center}
.grid{position:relative;display:grid;grid-template-columns:repeat(3,2.5in);grid-template-rows:repeat(3,3.5in);flex:none}
.crop{position:absolute;background:#1b1512}
.card{position:relative;overflow:hidden;display:flex;flex-direction:column;background:#fffdf9;border:.5px solid #e3ddd3}
.card .band{display:flex;justify-content:space-between;align-items:center;padding:.1in .16in .08in;font-size:6pt;letter-spacing:.16em;text-transform:uppercase;font-weight:600;color:#1b1512}
.card .band span:last-child{font-variant-numeric:tabular-nums;letter-spacing:.06em}
.card .in{flex:1;display:flex;flex-direction:column;padding:.12in .16in .1in;min-height:0}
.card .ico{width:.36in;height:.36in;color:#1b1512;margin-bottom:.06in}
.card .ico svg{width:100%;height:100%;display:block}
.card h2,.card h1{font-family:var(--display);font-weight:800;font-stretch:75%;font-size:21pt;line-height:.92;letter-spacing:-.012em;margin:0 0 .1in;white-space:normal;text-wrap:balance}
.card ul li{position:relative;font-size:8.3pt;line-height:1.36;color:var(--ink-2);padding:.032in 0 .032in .11in;border-top:1px solid var(--line)}
.card ul li::before{content:"";position:absolute;left:0;top:.08in;width:.04in;height:.04in;border-radius:50%;background:var(--ink)}
.card ul li.n{padding-left:0}.card ul li.n::before{display:none}
.card .cf{margin-top:auto;display:flex;justify-content:space-between;align-items:baseline;font-size:5.2pt;color:var(--muted);padding-top:.05in;border-top:1px solid var(--line-2)}
.card .cf a{color:var(--ink);text-decoration:none;font-weight:600}
.back{align-items:center;justify-content:center;border:none}
.back .frame{position:absolute;inset:.16in;border-radius:6px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:.08in}
.back .frame .bi{width:.9in;height:.9in;color:#1b1512}
.back .frame .bi svg{width:100%;height:100%;display:block}
.back .t{font-family:var(--display);font-weight:800;font-stretch:75%;font-size:17pt;line-height:.95;text-align:center;letter-spacing:-.01em}
.back .c{font-size:6.4pt;letter-spacing:.18em;text-transform:uppercase;font-weight:600}
.back .s{position:absolute;bottom:.1in;left:0;right:0;text-align:center;font-size:5.6pt;color:#3d332c}
.back .s a{color:#1b1512;text-decoration:none;font-weight:600}
.legend{display:grid;grid-template-columns:repeat(3,1fr);gap:.1in .2in;margin-top:.14in;flex:none}
.legend div{display:grid;grid-template-columns:.42in 1fr;align-items:center;column-gap:.1in;font-size:8.4pt;color:var(--ink-2)}
.legend i{display:flex;align-items:center;justify-content:center;width:.42in;height:.42in;border-radius:6px;color:#1b1512}
.legend i svg{width:.26in;height:.26in}
.legend b{display:block;font-family:var(--display);font-weight:700;font-size:11pt;color:var(--ink)}
.cols{display:grid;grid-template-columns:1fr 1fr;column-gap:.34in;margin-top:.18in;flex:none}
.sec ol{counter-reset:s}
.sec ol li{counter-increment:s;display:grid;grid-template-columns:.28in 1fr;font-size:8.8pt;line-height:1.38;color:var(--ink-2);padding:.045in 0;border-bottom:1px solid var(--line)}
.sec ol li:last-child{border-bottom:0}
.sec ol li::before{content:counter(s);font-family:var(--display);font-weight:700;font-stretch:75%;font-size:17pt;line-height:.95;color:var(--ink)}
.sec ol b{color:var(--ink);font-weight:600}
.src{margin-top:.16in;flex:none;border-top:2px solid var(--ink);padding-top:.08in}
.src h3{font-family:var(--display);font-weight:700;font-size:12pt;margin-bottom:.04in}
.src li{font-size:7.6pt;line-height:1.4;color:var(--ink-2);padding:.025in 0;display:grid;grid-template-columns:.22in 1fr}
.src li b{font-family:var(--display);font-weight:700;color:var(--ink)}
.src a{color:var(--ink-2);word-break:break-all}
.fine{margin-top:.12in}
.plan{margin-top:.16in;flex:none;display:grid;grid-template-columns:repeat(5,1fr);border-top:2px solid var(--ink)}
.plan div{padding:.07in .1in .06in;border-left:1px solid var(--line-2)}
.plan h3+div{border-left:0;padding-left:0}
.plan b{display:block;font-family:var(--display);font-weight:700;font-size:11.5pt;color:var(--ink);margin-bottom:.03in}
.plan span{display:block;font-size:7.8pt;line-height:1.4;color:var(--ink-2)}
.plan h3{grid-column:1/-1;font-family:var(--display);font-weight:700;font-size:12pt;padding:.07in 0 0}
"""


def note_icon():
    return ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
            '<path d="M9 18V5l11-2v13"/><circle cx="6.5" cy="18" r="2.5"/><circle cx="17.5" cy="16" r="2.5"/><path d="M9 9l11-2"/></svg>')


def icon(cat):
    return note_icon() if cat == "music" else w2.icon(CATS[cat][2])


def crops():
    """Crop marks just outside the 3 x 3 grid, on every cut line."""
    o = []
    L, gap, t = .2, .05, .006
    for k in range(4):
        x = k * 2.5
        o.append(f'<i class="crop" data-bleed style="left:{x - t / 2:.3f}in;top:{-gap - L:.3f}in;width:{t}in;height:{L}in"></i>')
        o.append(f'<i class="crop" data-bleed style="left:{x - t / 2:.3f}in;top:{10.5 + gap:.3f}in;width:{t}in;height:{L}in"></i>')
        y = k * 3.5
        o.append(f'<i class="crop" data-bleed style="top:{y - t / 2:.3f}in;left:{-gap - L:.3f}in;height:{t}in;width:{L}in"></i>')
        o.append(f'<i class="crop" data-bleed style="top:{y - t / 2:.3f}in;left:{7.5 + gap:.3f}in;height:{t}in;width:{L}in"></i>')
    return "".join(o)


def front(i, card):
    cat, title, lines, src = card
    name, col, _ = CATS[cat]
    lis = "".join(f'<li class="n">{C.esc(x)}</li>' if x[:2] in ("1 ", "2 ", "3 ") else f"<li>{C.esc(x)}</li>" for x in lines)
    s = f"Source: {src}" if src else "Common practice"
    return f"""<div class="card"><div class="band" style="background:{col}"><span>{C.esc(name)}</span><span>{i + 1:02d} / 27</span></div>
<div class="in"><div class="ico">{icon(cat)}</div><h2>{C.esc(title)}</h2><ul>{lis}</ul>
<div class="cf"><span><b style="color:var(--ink)">DIVELUX</b> · <a href="{C.SITE}">diveluxsaunahat.com</a></span><span>{s}</span></div></div></div>"""


def back(card):
    cat = card[0]
    name, col, _ = CATS[cat]
    return f"""<div class="card back"><div class="frame" style="background:{col}"><div class="bi">{icon(cat)}</div>
<div class="t">Sauna ritual<br>cards</div><div class="c">{C.esc(name)}</div></div>
<div class="s"><a href="{C.SITE}">diveluxsaunahat.com</a></div></div>"""


def cover():
    counts = {}
    for c in CARDS:
        counts[c[0]] = counts.get(c[0], 0) + 1
    legend = "".join(f'<div><i style="background:{col}">{icon(k)}</i><span><b>{C.esc(n)}</b>{counts[k]} cards</span></div>'
                     for k, (n, col, _) in CATS.items())
    printing = "<ol>" + "".join(f"<li><span>{x}</span></li>" for x in [
        "Print at 100% on card stock, about 80–110 lb cover (216–300 gsm).",
        "<b>Fronts and backs:</b> print pages 2–7 double-sided, “flip on long edge”. Each back page follows its front page, mirrored so the backs line up. Print one test sheet first.",
        "<b>Fronts only:</b> print pages 2, 4 and 6. The cards work without backs.",
        "Cut on the crop marks. A paper trimmer gives the cleanest edges. Round the corners if you like.",
        "Paper does not last in the hot room. Keep the deck in the lounge or laminate it.",
    ]) + "</ol>"
    use = "<ol>" + "".join(f"<li><span>{x}</span></li>" for x in [
        "<b>Plan a session:</b> pick one card from each color. Prepare, Pour, Towel, Scent, Music &amp; story, Cool down.",
        "<b>Train a new host:</b> go through one color per evening.",
        "<b>Home sauna:</b> lay out three cards before guests arrive, one for each round.",
        "<b>Keep it safe:</b> the Safety first card goes on top of every plan.",
    ]) + "</ol>"
    num = {c[1]: f"{i + 1:02d}" for i, c in enumerate(CARDS)}
    steps = [("Before", ["Heat up in good time", "Mix the bucket", "Fresh towels", "Ask first", "Safety first"]),
             ("Round 1", ["Door closed, then begin", "Forest", "Pour slowly", "The basic wave", "Pick the music"]),
             ("Round 2", ["Fresh", "Read the room", "The helicopter", "Tell a small story"]),
             ("Round 3", ["Ice ball", "One guest at a time", "Open and close"]),
             ("After", ["Cool down in order", "Rest and drink", "Towel manners"])]
    plan = "".join(f"<div><b>{a}</b>" + "".join(f"<span>{num[t]} {C.esc(t)}</span>" for t in ts) + "</div>" for a, ts in steps)
    src = "".join(f'<li><b>{a}</b><span>{C.esc(t)} · <a href="{u}">{C.esc(u)}</a></span></li>' for a, t, u in SOURCES)
    return f"""<main class="page">
<span class="kicker">For sauna masters, spa staff and home sauna hosts</span>
<div class="head"><h1>Ritual cards<i>.</i></h1>
<p class="lead">27 cards for planning an Aufguss or a calm sauna evening: the room, the pour, the towel, scent, music and the cool-down.</p></div>
<div class="legend">{legend}</div>
<div class="cols">{w2.sec("How to print", "Pages 2–7", printing, 2)}{w2.sec("How to use the deck", "Ideas", use, 3)}</div>
<div class="plan"><h3>A sample three-round evening</h3>{plan}</div>
<div class="src"><h3>Sources</h3><ul>{src}
<li><b>·</b><span>Cards marked “Common practice” describe widely shared host habits. Every card was checked in November 2026. Follow your sauna’s house rules and your heater maker’s instructions first.</span></li></ul></div>
<p class="fine">General information, not medical advice. Guests who are pregnant or have a health condition should ask their doctor before using a sauna. More free sauna printables and tools: <a href="{C.TOOLS}">diveluxsaunahat.com/pages/sauna-tools</a></p>
{C.foot(NAME + " · page 1 of 7")}
</main>"""


def build():
    pages = [cover()]
    for sh in range(3):
        chunk = CARDS[sh * 9:(sh + 1) * 9]
        fr = "".join(front(sh * 9 + k, c) for k, c in enumerate(chunk))
        # backs: same rows, columns mirrored, so a long-edge flip puts each back behind its front
        order = [r * 3 + (2 - c) for r in range(3) for c in range(3)]
        bk = "".join(back(chunk[k]) for k in order)
        pages.append(f'<main class="page sheet"><div class="grid">{crops()}{fr}</div></main>')
        pages.append(f'<main class="page sheet"><div class="grid">{crops()}{bk}</div></main>')
    body = "\n".join(pages)
    C.write(os.path.join(C.ROOT, SLUG, SLUG + ".html"), C.doc(TITLE, DESC, KEYWORDS, CSS, body))
    meta = dict(title="Sauna Ritual Cards for Sauna Masters (27 Printable Aufguss Cards)", subject=DESC, keywords=KEYWORDS)
    jobs = C.std_jobs(SLUG, SLUG + ".html", SLUG, meta)
    return dict(slug=SLUG, jobs=jobs, preview=dict(pdf=jobs[0]["pdf"], pages=[1, 2, 3], dpi=75))
