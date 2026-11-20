"""20. Sauna whisk guide (vihta, vasta, venik): how to get a whisk ready and how to use it.
Only points on which the sources agree are stated as advice. Where they disagree (how long and how warm to soak
a dried whisk) the sheet says so and points to the label. Names are read from the open dataset.
Checked in November 2026 against: Finnish Sauna Society quality guidelines for sauna whisks (sauna.fi),
Finland Naturally (finlandnaturally.com, "Vasta or vihta"), HUUM (huum.eu, "Sauna whisking")."""
import csv
import os
import common as C
import w2
import art

SLUG = "sauna-whisk-guide"
TITLE = "Sauna Whisk Guide"
DESC = "A printable one-page guide to the sauna whisk (vihta, vasta, venik): what it is, how to get a fresh, dried or frozen whisk ready, how to whisk gently, and how to store it."
KEYWORDS = "sauna whisk, vihta, vasta, venik, how to use a sauna whisk, birch whisk, banya venik, how to soak a sauna whisk, printable guide, DIVELUX"
DATA = "/root/divelux/freebies/dataset/sauna_traditions.csv"

READY = [
    ("Fresh", "Ready to use as it is. Between rounds, keep it in a bucket of cool water."),
    ("Dried", "Soak it in water until the leaves are soft and bend without cracking. Labels differ a lot, from about 15 minutes to 2 hours, so follow the one that came with your whisk."),
    ("Frozen", "Let it thaw at room temperature before the sauna. Then treat it like a fresh one."),
]
HOW = [
    ("Warm up first", "Sit in the heat for a few minutes before you pick up the whisk."),
    ("Shake off the water", "Give the whisk a shake over the floor, away from other bathers."),
    ("Start light", "Brush and tap the skin with the leafy end. It should feel like soft rain, never like a blow."),
    ("Arms and legs, then back", "Work from the arms and legs toward the back and chest. Stay away from the face."),
    ("Whisking someone else", "Agree on how firm before you start. Begin gently and go firmer only if they ask."),
    ("Rinse and rest", "Rinse the leaves off with cool water, then sit and cool down."),
]
CARE = [
    "Keep the whisk off the stove, the stones and the hot bench. Dry leaves scorch.",
    "After the sauna, shake it out and hang it up to dry.",
    "Dried whisks keep best hanging in a cool, dark, airy place.",
    "A fresh whisk can be frozen in a sealed bag with the air pressed out.",
]
MAKE = [
    "Cut leafy birch twigs in early summer, about 20 in (50 cm) long. Ask the landowner first.",
    "Lay the twigs into a flat, even fan with the leafy ends together.",
    "Strip the leaves from the last 4–6 in (10–15 cm) to make a handle.",
    "Tie the handle tightly in two places and trim anything sharp.",
]
SENSE = [
    ("Know your tree", "Use only branches from trees you can name. Birch is the classic; oak and eucalyptus are common too."),
    ("Skin comes first", "Skip the whisk on broken, sunburned or irritated skin. Stop if it hurts."),
    ("House rules", "In a public sauna, ask before you bring a whisk. Leaves on the floor are yours to sweep up."),
]

CSS = w2.CSS + """
.page{padding:.5in .58in .34in}
.top{display:grid;grid-template-columns:1fr 1.9in;column-gap:.3in;align-items:end;flex:none}
h1{font-size:84pt}
.pic{flex:1;min-height:0;display:flex;justify-content:center;align-items:center}
.pic svg{display:block;height:1.75in;width:1.46in}
.top .lead{margin-top:.14in;max-width:4.8in;font-size:13.5pt}
.top svg{display:block;width:1.9in;height:2.28in;margin-bottom:-.04in}
.names{display:grid;grid-template-columns:repeat(5,1fr);border-top:2px solid var(--ink);border-bottom:1px solid var(--ink);margin-top:.14in;flex:none}
.names div{padding:.07in .1in .07in 0;border-left:1px solid var(--line-2);padding-left:.1in}
.names div:first-child{border-left:0;padding-left:0}
.names b{display:block;font-family:var(--display);font-weight:700;font-size:13.5pt;line-height:1.1;letter-spacing:-.01em}
.names span{font-size:7.6pt;color:var(--muted);line-height:1.3;display:block}
.cols{flex:1;display:grid;grid-template-columns:1fr 1.08fr;column-gap:.34in;margin-top:.14in;min-height:0}
.col{display:flex;flex-direction:column;justify-content:space-between;min-height:0;row-gap:.1in}
.sec li.r{display:block;font-size:9.2pt;line-height:1.38;color:var(--ink-2);padding:.045in 0;border-bottom:1px solid var(--line)}
.sec li.r:last-child{border-bottom:0}
.sec li.r b{font-family:var(--display);font-weight:700;font-size:11pt;color:var(--ink);margin-right:.05in;letter-spacing:-.005em}
.sec ol{counter-reset:s}
.sec ol li{counter-increment:s;display:grid;grid-template-columns:.3in 1fr;font-size:9.2pt;line-height:1.36;color:var(--ink-2);padding:.047in 0;border-bottom:1px solid var(--line)}
.sec ol li:last-child{border-bottom:0}
.sec ol li::before{content:counter(s);font-family:var(--display);font-weight:700;font-stretch:75%;font-size:20pt;line-height:.95;color:var(--ink)}
.sec ol b{display:block;font-family:var(--display);font-weight:700;font-size:11pt;line-height:1.15;color:var(--ink);letter-spacing:-.005em}
.cl li{font-size:9.2pt;padding:.036in 0;grid-template-columns:.16in 1fr}
.cl li i.dotm{display:block;width:.05in;height:.05in;border-radius:50%;background:var(--ink);margin-top:.055in}
.always{margin-top:.12in}
.fine{margin:.09in 0 .09in}
"""


def names():
    rows = {r["name"]: r for r in csv.DictReader(open(DATA, encoding="utf-8"))}
    fi, ee, ru, lt, lv = (rows[n]["whisk_or_ritual"] for n in ("Finnish sauna", "Estonian sauna", "Russian banya", "Lithuanian pirtis", "Latvian pirts"))
    assert "vihta (western Finland) or vasta (eastern Finland)" in fi and "called viht" in ee and "(venik)" in ru and "called vanta" in lt and "(slota)" in lv
    return [("vihta, vasta", "Finland: vihta in the west, vasta in the east"), ("viht", "Estonia"), ("venik", "the Russian banya"),
            ("vanta", "Lithuania"), ("slota", "Latvia")]


def bullets(items):
    return '<ul class="cl">' + "".join(f'<li><i class="dotm"></i><span>{C.esc(x)}</span></li>' for x in items) + "</ul>"


def build():
    nm = "".join(f"<div><b>{C.esc(a)}</b><span>{C.esc(b)}</span></div>" for a, b in names())
    ready = "<ul>" + "".join(f'<li class="r"><b>{C.esc(t)}</b>{C.esc(x)}</li>' for t, x in READY) + "</ul>"
    how = "<ol>" + "".join(f"<li><span><b>{C.esc(t)}</b>{C.esc(x)}</span></li>" for t, x in HOW) + "</ol>"
    sense = "".join(f"<div><b>{C.esc(t)}</b><p>{C.esc(x)}</p></div>" for t, x in SENSE)
    body = f"""<main class="page">
<span class="kicker">Vihta, vasta, venik</span>
<div class="head"><h1>The whisk<i>.</i></h1>
<p class="lead">A leafy bundle of twigs for the hot room. It moves the heat around and smells like a summer forest.</p></div>
<div class="names">{nm}</div>
<div class="cols">
<div class="col">{w2.sec("Get it ready", "Fresh, dried or frozen", ready, 1)}<div class="pic">{art.page_whisk()}</div>{w2.sec("Make your own", "Early summer", bullets(MAKE), 4)}</div>
<div class="col">{w2.sec("How to whisk", "Gentle is the whole point", how, 2)}{w2.sec("Look after it", "So it lasts", bullets(CARE), 3)}</div>
</div>
<div class="always">{sense}</div>
<p class="fine">In the banya, a wool felt hat worn dry is part of the kit. Soaking times and water temperature for dried whisks vary by maker, so the label on your whisk comes first. General information, not medical advice.</p>
{C.foot()}
</main>"""
    C.write(os.path.join(C.ROOT, SLUG, SLUG + ".html"), C.doc(TITLE, DESC, KEYWORDS, CSS, body))
    meta = dict(title="Sauna Whisk Guide: Vihta, Vasta, Venik (Printable)", subject=DESC, keywords=KEYWORDS)
    jobs = C.std_jobs(SLUG, SLUG + ".html", SLUG, meta)
    return dict(slug=SLUG, jobs=jobs, preview=dict(pdf=jobs[0]["pdf"]))
