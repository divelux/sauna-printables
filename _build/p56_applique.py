"""56. Felt appliqué templates for hats: ten cut-out shapes at true size (solid line = cut, dashed line = stitch),
how-to with stitch diagrams, ideas. Shapes are built with shapely in art3.py.
No glue or iron-on on the hat: heat can soften adhesives, and ironing would mean heat and steam on the hat. Sew instead."""
import os

import art
import art3
import common as C
import w2
from art import f
from p55_embroidery import scale_check

SLUG = "felt-applique-templates-for-hats"
TITLE = "Felt Appliqué Templates for Hats"
DESC = ("Ten printable felt appliqué templates at true size (birch leaf, spruce, snowflake, star, heart, flame, steam cloud, "
        "ladle, drop, name patch) with cut and stitch lines, plus how to sew them onto a wool felt hat.")
KEYWORDS = ("felt applique templates, felt shapes printable, applique patterns, felt crafts, sauna hat decoration, "
            "blanket stitch applique, felt snowflake template, felt leaf template, DIVELUX")
NAME = "Felt Appliqué Templates"

CSS = w2.CSS + """
.page{padding:.5in .6in .34in}
h1{font-size:66pt}
.intro{display:grid;grid-template-columns:1fr 2.4in;column-gap:.32in;margin-top:.14in;flex:none}
.sec li.r{display:block;font-size:9pt;line-height:1.38;color:var(--ink-2);padding:.042in 0;border-bottom:1px solid var(--line)}
.sec li.r:last-child{border-bottom:0}
.sec li.r b{font-family:var(--display);font-weight:700;font-size:10.4pt;color:var(--ink);margin-right:.05in}
.steps{counter-reset:s;margin-top:.12in}
.steps li{counter-increment:s;display:grid;grid-template-columns:.34in 1fr;padding:.06in 0;border-top:1px solid var(--line)}
.steps li::before{content:counter(s);font-family:var(--display);font-weight:700;font-stretch:75%;font-size:22pt;line-height:.9;color:var(--ink)}
.steps li span{font-size:9pt;line-height:1.4;color:var(--ink-2)}
.steps li b{display:block;font-family:var(--display);font-weight:700;font-size:11pt;color:var(--ink);letter-spacing:-.005em}
.key{display:flex;gap:.3in;align-items:center;font-size:8.4pt;color:var(--ink-2);margin-top:.12in;flex:none}
.key svg{display:block;width:.5in;height:.16in}
.stitches{display:grid;grid-template-columns:repeat(3,1fr);gap:.16in;margin-top:.12in;flex:none}
.st{border-top:1.5px solid var(--ink);padding-top:.05in}
.st svg{display:block;width:100%;height:.72in;margin:.03in 0 .04in}
.st b{display:block;font-family:var(--display);font-weight:700;font-size:10.6pt;line-height:1.1}
.st span{display:block;font-size:7.8pt;line-height:1.34;color:var(--ink-2)}
.ts{display:flex;justify-content:center;margin-top:.12in;flex:none}
.ts svg{display:block}
.scale{display:flex;align-items:center;gap:.14in;font-size:7.2pt;color:var(--muted);flex:none;margin-top:.08in}
.scale b{color:var(--ink);font-weight:600}
.ideas{display:grid;grid-template-columns:repeat(3,1fr);column-gap:.22in;margin-top:.14in;flex:none}
.ideas figure svg{display:block;width:100%;height:1.9in}
.ideas figcaption{font-size:8.4pt;line-height:1.4;color:var(--ink-2);margin-top:.04in}
.ideas figcaption b{display:block;font-family:var(--display);font-weight:700;font-size:11pt;color:var(--ink)}
.always{margin-top:.18in}
.fine{margin-top:.12in}
"""

# (name, note, geometry function); geometry is in 100 units = 1 in
SHAPES_A = [
    ("Birch leaf, large", "cut 1 or 2", lambda: art3.g_leaf(220, 72)),
    ("Birch leaf, small", "cut 2 or 3", lambda: art3.g_leaf(132, 44)),
    ("Star", "cut 1", lambda: art3.g_star(104, 47)),
    ("Spruce", "cut 1", art3.g_tree),
    ("Snowflake", "cut 1, sharp scissors", lambda: art3.g_snowflake(96)),
    ("Heart", "cut 1", lambda: art3.g_heart(.95)),
]
SHAPES_B = [
    ("Flame", "cut 1", lambda: art3.g_flame(.8)),
    ("Flame center", "cut 1, contrast color", lambda: __import__("shapely").affinity.scale(art3.g_flame_inner(), .8, .8, origin=(0, 0))),
    ("Steam cloud", "cut 1", art3.g_cloud),
    ("Water drop", "cut 1–3", lambda: art3.g_drop(.95)),
    ("Ladle", "cut 1", lambda: __import__("shapely").affinity.scale(art3.g_ladle(), .82, .82, origin=(0, 0))),
    ("Name patch, round", "cut 1, add a letter", lambda: art3.g_circle(80)),
    ("Name patch, scalloped", "cut 1", lambda: art3.g_scallop(90)),
]


def sheet(shapes, rows, W=700, gap=34):
    """Lay shapes out in rows (list of index lists), centered, each with a label. Returns a true-size SVG."""
    o, y = [], 0
    fills = ["#fbf1e5", "#f8dfc6", "#fbf1e5", "#f8dfc6"]
    for r in rows:
        items = []
        for i in r:
            name, note, fn = shapes[i]
            g, w, h = art3.norm(fn(), 3)
            items.append((name, note, g, w, h))
        tot = sum(it[3] for it in items) + gap * (len(items) - 1)
        assert tot <= W, f"row too wide: {tot}"
        x = (W - tot) / 2
        rh = max(it[4] for it in items)
        for k, (name, note, g, w, h) in enumerate(items):
            yy = y + (rh - h)
            o.append(f'<g transform="translate({f(x)} {f(yy)})">{art3.cut_piece(g, fill=fills[k % 4])}</g>')
            gw, gh = w - 6, h - 6
            o.append(f'<text x="{f(x + w / 2)}" y="{f(y + rh + 17)}" text-anchor="middle" font-family="Bricolage Grotesque" '
                     f'font-weight="700" font-size="12" fill="#1b1512" stroke="none">{C.esc(name)}</text>')
            o.append(f'<text x="{f(x + w / 2)}" y="{f(y + rh + 31)}" text-anchor="middle" font-family="Inter" font-size="9.5" '
                     f'fill="#6f655c" stroke="none">{gw / 100:.1f} × {gh / 100:.1f} in · {C.esc(note)}</text>')
            x += w + gap
        y += rh + 52
    return art3.tsvg(W, y - 10, "".join(o), 1.5)


def key():
    cut = '<svg viewBox="0 0 50 16"><path d="M2 8H48" stroke="#1b1512" stroke-width="1.6"/></svg>'
    sew = '<svg viewBox="0 0 50 16"><path d="M2 8H48" stroke="#6f655c" stroke-width="1.2" stroke-dasharray="5 4"/></svg>'
    return (f'<div class="key"><span style="display:flex;gap:.08in;align-items:center">{cut}<b>Solid line:</b> cut here</span>'
            f'<span style="display:flex;gap:.08in;align-items:center">{sew}<b>Dashed line:</b> stitch here, about 1/8 in in from the edge</span></div>')


def page1():
    need = "<ul>" + "".join(f'<li class="r"><b>{a}</b>{b}</li>' for a, b in [
        ("Felt:", "wool or wool-blend craft felt, about 1–2 mm thick. It cuts cleanly and does not fray."),
        ("Thread:", "cotton embroidery floss (2 or 3 strands) or pearl cotton, matching or contrasting."),
        ("Needle:", "sharp embroidery or chenille needle, plus a thimble."),
        ("Also:", "small sharp scissors, pins or clips, a pencil or chalk pencil."),
    ]) + "</ul>"
    steps = "".join(f"<li><span><b>{a}</b>{b}</span></li>" for a, b in [
        ("Print at 100%", "Check the squares on the template pages: 1 in and 2 cm exactly."),
        ("Cut the paper template", "Cut on the solid line. For small or pointy shapes, glue the page to thin card first."),
        ("Trace and cut the felt", "Hold the template on the felt and draw around it, or pin the paper on and cut through both."),
        ("Pin it on the hat", "Try a few spots. Pin or clip the piece in place, away from any seam."),
        ("Sew around the edge", "Blanket stitch or whip stitch along the dashed line. Keep stitches shallow in the hat felt."),
        ("Add details", "Veins, stars or a letter in back stitch or stem stitch on top of the piece."),
    ])
    sts = "".join(f'<div class="st">{art3.stitch_box(fn())}<b>{a}</b><span>{b}</span></div>' for a, b, fn in [
        ("Blanket stitch", "Neat ladder edge. Needle in through the piece, out at the edge, over the thread loop.", art3.stitch_blanket),
        ("Whip stitch", "Fast and almost invisible in matching thread. Small slanted stitches over the edge.", art3.stitch_whip),
        ("Running stitch", "A dotted line just inside the edge. Also good for leaf veins and steam.", art3.stitch_running),
    ])
    return f"""<main class="page">
<span class="kicker">Cut, pin, stitch</span>
<div class="head"><h1>Felt appliqué<i>.</i></h1></div>
<div class="intro"><div><p class="lead">Ten shapes at true size for decorating a wool felt hat, a bag or a sauna gift: birch leaves, spruce, snowflake, star, heart, flame, steam, ladle, drop and a name patch.</p>
<ol class="steps">{steps}</ol></div>
{w2.sec("What you need", "", need, 2)}</div>
<div class="stitches">{sts}</div>
<div class="always">
<div><b>Sew, don’t glue</b><p>Hot glue and iron-on adhesive can soften in sauna heat, and ironing means heat and steam on the hat. A few stitches hold for years.</p></div>
<div><b>Keep the inside smooth</b><p>Hat felt is about 4–5 mm thick. Take shallow stitches through the outer part where you can, and keep knots small and flat.</p></div>
<div><b>No metal</b><p>Skip metal charms, sequins and metallic thread. Metal gets hot in the sauna.</p></div>
</div>
{C.foot(NAME + " · 1 of 4")}
</main>"""


def page_tpl(n, title, note, shapes, rows):
    return f"""<main class="page white">
{w2.ph(title, note)}
{key()}
<div class="ts">{sheet(shapes, rows)}</div>
{scale_check()}
{C.foot(NAME + f" · {n} of 4")}
</main>"""


def idea_bell():
    o = [art.bell_hat(60, 20, .82, pattern=False, uid="ib")]
    from shapely import affinity
    g = affinity.scale(art3.g_leaf(220, 72), .42, .42, origin=(0, 0))
    o.append(f'<g transform="translate(150 160) rotate(-30)">{art3.cut_piece(g, inset=4, fill="#f0a877")}</g>')
    o.append(f'<g transform="translate(176 172) rotate(-80)">{art3.cut_piece(g, inset=4, fill="#f5c7a0")}</g>')
    c = art3.g_circle(36)
    o.append(f'<g transform="translate(196 176)">{art3.cut_piece(c, inset=4, fill="#fbf1e5")}</g>')
    o.append(art3.mono_letter("A", 220, 192, 30, 2.4)[0])
    return art.svg(420, 380, "".join(o), 3)


def idea_bucket():
    from shapely import affinity
    o = [art.bucket_hat(20, 120, .7, pattern=False)]
    sf = affinity.scale(art3.g_snowflake(96), .17, .17, origin=(0, 0))
    for x, y in ((92, 248), (150, 260), (210, 266), (270, 266), (330, 260), (388, 248)):
        o.append(f'<g transform="translate({x - 19} {y - 19})">{art3.cut_piece(sf, inset=2, fill="#fbf1e5")}</g>')
    st = affinity.scale(art3.g_star(104, 47), .3, .3, origin=(0, 0))
    o.append(f'<g transform="translate(176 150)">{art3.cut_piece(st, inset=3, fill="#f0a877")}</g>')
    return art.svg(420, 380, "".join(o), 3)


def idea_gift():
    from shapely import affinity
    o = ['<rect x="60" y="80" width="300" height="260" rx="10" fill="#fff"/>', '<path d="M60 130H360" fill="none"/>',
         '<path d="M150 80C150 30 270 30 270 80" fill="none"/>']
    fl = affinity.scale(art3.g_flame(1), .55, .55, origin=(0, 0))
    o.append(f'<g transform="translate(160 160)">{art3.cut_piece(fl, inset=4, fill="#f0a877")}</g>')
    fi = affinity.scale(art3.g_flame_inner(), .55, .55, origin=(0, 0))
    o.append(f'<g transform="translate(160 160)">{art3.cut_piece(fi, inset=3, fill="#f8dfc6")}</g>')
    return art.svg(420, 380, "".join(o), 3)


def page4():
    return f"""<main class="page">
{w2.ph("Ideas", "Drawings are not to scale. Start with one piece; you can always add another.")}
<div class="ideas">
<figure>{idea_bell()}<figcaption><b>Leaves and a name patch</b>Two birch leaves tucked behind a round patch with one stitched letter. Use the single-line alphabet from our embroidery patterns, or write the letter in chalk and stitch over it.</figcaption></figure>
<figure>{idea_bucket()}<figcaption><b>Snow on the brim</b>Print the snowflake at 25–40% for small brim pieces, or stitch French knots instead. Add one star on the crown.</figcaption></figure>
<figure>{idea_gift()}<figcaption><b>Not just hats</b>A flame with its center on a tote bag, a towel tag or a gift box. The same templates work on any felt or tightly woven fabric.</figcaption></figure>
</div>
<div class="always">
<div><b>Mix two colors</b><p>Light pieces on dark hats, dark on light. The flame and its center look best in two warm colors.</p></div>
<div><b>Mark your hat</b><p>In a busy sauna a leaf or an initial makes your hat easy to find on the peg.</p></div>
<div><b>Small at the edge</b><p>Keep pieces clear of the bottom edge if you like to fold it up, so the fold stays soft.</p></div>
</div>
<div class="always" style="margin-top:.14in">
<div><b>Wear it dry</b><p>A sauna hat is worn dry. If it ever needs a wash: by hand only, in cool, room-temperature water (about 68–75 °F / 20–24 °C, never warm or hot), squeeze, don’t wring, air-dry.</p></div>
<div><b>No machine, no dryer</b><p>Never machine-wash or tumble-dry a felt hat, decorated or not. Brush off lint with a dry clothes brush.</p></div>
<div><b>Loose stitch?</b><p>Fix it right away with a few stitches in matching thread, before the piece starts to lift.</p></div>
</div>
<p class="fine">Templates by DIVELUX, makers of wool sauna hats. More free sauna printables and tools: <a href="{C.TOOLS}">diveluxsaunahat.com/pages/sauna-tools</a></p>
{C.foot(NAME + " · 4 of 4")}
</main>"""


def build():
    body = "\n".join([
        page1(),
        page_tpl(2, "Templates 1", "Leaves, star, spruce, snowflake, heart. True size.", SHAPES_A, [[0, 1, 2], [3, 4, 5]]),
        page_tpl(3, "Templates 2", "Flame, steam, drop, ladle, name patches. True size.", SHAPES_B, [[0, 1, 3, 5], [2, 6], [4]]),
        page4(),
    ])
    C.write(os.path.join(C.ROOT, SLUG, SLUG + ".html"), C.doc(TITLE, DESC, KEYWORDS, CSS, body))
    meta = dict(title="Felt Appliqué Templates for Hats (Printable, True Size)", subject=DESC, keywords=KEYWORDS)
    jobs = C.std_jobs(SLUG, SLUG + ".html", SLUG, meta)
    return dict(slug=SLUG, jobs=jobs, preview=dict(pdf=jobs[0]["pdf"], pages=[1, 2, 3], dpi=75))
