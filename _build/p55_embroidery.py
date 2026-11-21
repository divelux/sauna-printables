"""55. Sauna hat embroidery and monogram patterns: two alphabets, eight motifs and a wreath at true size, placement
guides for the bell and the bucket hat, and a transfer sheet. Art is vector code in art3.py.
Care rules follow the brief: the hat is worn dry and never goes in a bowl or under the tap. If a wash-away
stabilizer is used, only the leftover bits are dabbed off with cool, room-temperature water, as the stabilizer
maker describes, and the hat air-dries. Water-free methods come first."""
import math
import os

import art
import art3
import common as C
import w2
from art import f

SLUG = "sauna-hat-embroidery-monogram-patterns"
TITLE = "Sauna Hat Embroidery and Monogram Patterns"
DESC = ("Printable embroidery patterns for wool felt sauna hats: a single-line and an outline monogram alphabet, eight sauna motifs "
        "and a leaf wreath at true size, placement guides for bell and bucket hats, and water-free transfer methods.")
KEYWORDS = ("sauna hat embroidery, monogram alphabet, embroidery pattern printable, felt hat embroidery, hand embroidery motifs, "
            "snowflake embroidery, birch leaf embroidery, stem stitch letters, DIVELUX")
NAME = "Sauna Hat Embroidery Patterns"

CSS = w2.CSS + """
.page{padding:.5in .6in .34in}
h1{font-size:70pt}
.lead{max-width:4.6in}
.intro{display:grid;grid-template-columns:1fr 2.3in;column-gap:.32in;margin-top:.16in;flex:none}
.sec li.r{display:block;font-size:9pt;line-height:1.38;color:var(--ink-2);padding:.042in 0;border-bottom:1px solid var(--line)}
.sec li.r:last-child{border-bottom:0}
.sec li.r b{font-family:var(--display);font-weight:700;font-size:10.4pt;color:var(--ink);margin-right:.05in;letter-spacing:-.005em}
.stitches{display:grid;grid-template-columns:repeat(4,1fr);gap:.12in .16in;margin-top:.12in;flex:none}
.st{border-top:1.5px solid var(--ink);padding-top:.05in}
.st svg{display:block;width:100%;height:.78in;margin:.03in 0 .04in}
.st b{display:block;font-family:var(--display);font-weight:700;font-size:10.6pt;line-height:1.1;letter-spacing:-.005em}
.st span{display:block;font-size:7.6pt;line-height:1.32;color:var(--ink-2)}
.felt{margin-top:.16in;flex:none}
.notes{margin-top:.14in}.notes p{border-top:1px solid var(--line);padding:.06in 0}
.ph.small{margin-top:.22in}.ph.small h2{font-size:28pt}
.felt .grid{display:grid;grid-template-columns:repeat(3,1fr);column-gap:.24in}
.felt p{font-size:8.6pt;line-height:1.4;color:var(--ink-2);padding:.05in 0}
.felt p b{display:block;font-family:var(--display);font-weight:700;font-size:10.4pt;color:var(--ink);margin-bottom:.01in}
.ts{display:flex;justify-content:center;margin-top:.14in;flex:none}
.ts svg{display:block}
.cap{font-size:8pt;line-height:1.38;color:var(--muted);text-align:center;margin-top:.05in}
.scale{display:flex;align-items:center;gap:.14in;font-size:7.2pt;color:var(--muted);flex:none;margin-top:.1in;letter-spacing:.02em}
.scale svg{display:block}
.scale b{color:var(--ink);font-weight:600}
.mono3{display:grid;grid-template-columns:2.3in 1fr 1fr;column-gap:.24in;align-items:end;margin-top:.14in;flex:none;border-top:2px solid var(--ink);padding-top:.12in}
.mono3 figure{display:flex;flex-direction:column;align-items:center;justify-content:flex-end}
.mono3 figcaption{font-size:7.8pt;line-height:1.36;color:var(--ink-2);text-align:center;margin-top:.06in}
.mono3 figcaption b{display:block;font-family:var(--display);font-weight:700;font-size:10pt;color:var(--ink)}
.motifs{display:grid;grid-template-columns:repeat(3,1fr);gap:.04in .2in;margin-top:.1in;flex:none}
.motifs figure{display:flex;flex-direction:column;align-items:center;justify-content:flex-end;border-bottom:1px solid var(--line);padding-bottom:.06in}
.motifs figcaption{text-align:center;font-size:7.6pt;line-height:1.3;color:var(--ink-2);margin-top:.04in}
.motifs figcaption b{display:block;font-family:var(--display);font-weight:700;font-size:10pt;color:var(--ink)}
.place{display:grid;grid-template-columns:1fr 1fr;column-gap:.3in;margin-top:.14in;flex:none}
.place figure svg{display:block;width:100%;height:2.3in}
.place figcaption{font-size:8.4pt;line-height:1.4;color:var(--ink-2);margin-top:.06in}
.place figcaption b{display:block;font-family:var(--display);font-weight:700;font-size:12pt;color:var(--ink);letter-spacing:-.005em}
.place ul{margin-top:.04in}
.place li{font-size:8.4pt;line-height:1.38;color:var(--ink-2);padding:.03in 0 .03in .14in;position:relative}
.place li::before{content:"";position:absolute;left:0;top:.075in;width:.05in;height:.05in;border-radius:50%;background:var(--ink)}
.tools{display:grid;grid-template-columns:6.05in 1fr;column-gap:.2in;align-items:start;margin-top:.16in;flex:none;border-top:2px solid var(--ink);padding-top:.12in}
.tools .txt{grid-column:1 / -1;display:grid;grid-template-columns:auto 1fr;column-gap:.24in;align-items:baseline;margin-bottom:.1in}
.tools h3{font-family:var(--display);font-weight:700;font-size:12pt;letter-spacing:-.005em}
.tools p{font-size:8.4pt;line-height:1.4;color:var(--ink-2);margin-top:.04in;max-width:2.9in}
.methods{display:grid;grid-template-columns:1fr 1fr;gap:.14in .3in;margin-top:.14in;flex:none}
.m{border-top:2px solid var(--ink);padding-top:.07in}
.m .tag{display:inline-block;font-size:6.6pt;letter-spacing:.14em;text-transform:uppercase;font-weight:600;color:var(--ink);background:var(--t3);padding:.02in .06in;border-radius:3px}
.m.best .tag{background:var(--t1)}
.m h3{font-family:var(--display);font-weight:700;font-size:14pt;line-height:1.05;letter-spacing:-.01em;margin:.05in 0 .04in}
.m ol{counter-reset:s}
.m ol li{counter-increment:s;display:grid;grid-template-columns:.2in 1fr;font-size:8.6pt;line-height:1.38;color:var(--ink-2);padding:.025in 0}
.m ol li::before{content:counter(s);font-family:var(--display);font-weight:700;font-size:10pt;color:var(--ink)}
.m p{font-size:8.6pt;line-height:1.4;color:var(--ink-2)}
.warn{margin-top:.14in;flex:none;display:grid;grid-template-columns:1.5in 1fr;column-gap:.24in;background:var(--card);border:1.5px solid var(--ink);border-radius:var(--r);padding:.12in .16in}
.warn h3{font-family:var(--display);font-weight:800;font-stretch:75%;font-size:22pt;line-height:.95;letter-spacing:-.01em}
.warn p{font-size:8.8pt;line-height:1.42;color:var(--ink-2)}
.warn p+p{margin-top:.05in}
.fine{margin-top:.1in}
"""


def scale_check():
    """True-size check squares: 1 in and 2 cm, drawn in CSS pixels (96 per inch). verify_true_size.py measures them in the PDF."""
    one, cm2 = 96, 96 * 2 / 2.54
    W = math.ceil(one + cm2 + 29)
    s = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="96" viewBox="0 0 {W} 96" '
         f'style="width:{W}px;height:96px;flex:none;max-width:none" aria-hidden="true">'
         f'<rect x="0" y="0" width="{one}" height="{one}" fill="#f5c7a0" stroke="none"/>'
         f'<rect x="{one + 29}" y="{one - cm2:.4f}" width="{cm2:.4f}" height="{cm2:.4f}" fill="#fbf1e5" stroke="none"/>'
         f'<text x="48" y="53" text-anchor="middle" font-family="Inter" font-size="12.5" font-weight="600" fill="#1b1512">1 in</text>'
         f'<text x="{one + 29 + cm2 / 2:.2f}" y="{one - cm2 / 2 + 5:.2f}" text-anchor="middle" font-family="Inter" font-size="12.5" font-weight="600" fill="#1b1512">2 cm</text></svg>')
    return (f'<div class="scale">{s}<span><b>True size.</b> Print at 100% (“Actual size”), not “Fit to page”. '
            f'The squares should measure exactly 1 in and 2 cm. If they do, every pattern on this page is true to size.</span></div>')


def mono_sheet(cell=100, cap=88, rows=(7, 7, 6, 6), sw=1.5):
    letters = list(art3.MONO)
    o, i, y = [], 0, 8
    for n in rows:
        x0 = (7 - n) * cell / 2
        for k in range(n):
            ch = letters[i]
            w = art3.MONO[ch][0] * cap / 100
            m, _ = art3.mono_letter(ch, x0 + k * cell + (cell - w) / 2, y, cap, sw)
            o.append(m)
            i += 1
        y += cap + 30
    return art3.tsvg(7 * cell, y - 22, "".join(o), sw)


def outline_sheet(cell=100, cap=64, rows=(7, 7, 6, 6)):
    size = cap / .66
    letters = list(art3.MONO)
    o, i, base = [], 0, 8 + cap
    for n in rows:
        x0 = (7 - n) * cell / 2
        for k in range(n):
            o.append(art3.outline_letter(letters[i], x0 + k * cell + cell / 2, base, size))
            i += 1
        base += cap + 32
    for k, ch in enumerate("0123456789"):
        o.append(art3.outline_letter(ch, 35 + k * 70, base, size))
    base += cap + 32
    return art3.tsvg(7 * cell, base - cap - 22, "".join(o), 1.2)


def monogram_examples():
    w, h, wr = art3.m_wreath(84)
    ch = "M"
    lw = art3.MONO[ch][0] * .74
    m, _ = art3.mono_letter(ch, w / 2 - lw / 2, h / 2 - 37 - 4, 74, 1.5)
    wreath = art3.tsvg(w, h, wr + m, 1.4)
    trio, x = [], 4
    for ch, cap in (("E", 52), ("W", 78), ("L", 52)):
        lw = art3.MONO[ch][0] * cap / 100
        trio.append(art3.mono_letter(ch, x, 4 + (78 - cap) / 2, cap, 1.5)[0])
        x += lw + 16
    three = art3.tsvg(x - 12, 86, "".join(trio), 1.5)
    duo, x = [], 4
    for ch in ("A", "K"):
        m, adv = art3.mono_letter(ch, x, 4, 60, 1.5)
        duo.append(m)
        x += adv + 34
        if ch == "A":
            duo.append(f'<circle cx="{f(x - 17)}" cy="34" r="4.5" fill="#1b1512" stroke="none"/>')
    two = art3.tsvg(x - 30, 68, "".join(duo), 1.5)
    return f"""<div class="mono3">
<figure>{wreath}<figcaption><b>One initial in a wreath</b>Wreath in lazy daisy or satin leaves, letter in stem stitch.</figcaption></figure>
<figure>{three}<figcaption><b>Classic three-letter monogram</b>First initial, last-name initial in the middle and larger, middle initial. Emma Lee Ward: E&nbsp;W&nbsp;L.</figcaption></figure>
<figure>{two}<figcaption><b>Two initials and a dot</b>Quick and clear. The dot is one French knot or a few tiny satin stitches.</figcaption></figure>
</div>"""


STITCHES = [
    ("Running stitch", "Up, down, leave a gap. For dotted lines and steam.", art3.stitch_running),
    ("Back stitch", "Each stitch goes back to meet the last one. Crisp lines and letters.", art3.stitch_back),
    ("Stem stitch", "Small slanted stitches that overlap like a rope. Smooth curves.", art3.stitch_stem),
    ("Split stitch", "Come up through the middle of the last stitch. Good outlines for satin.", art3.stitch_split),
    ("Satin stitch", "Close side-by-side stitches that fill a small shape. Keep shapes under 1/2 in wide.", art3.stitch_satin),
    ("French knot", "Wrap the thread twice around the needle, go down next to where you came up.", art3.stitch_french),
    ("Lazy daisy", "A small loop held down by one tiny stitch. Leaves and petals.", art3.stitch_daisy),
    ("Whip stitch", "Slanted stitches over an edge. For sewing on a felt patch.", art3.stitch_whip),
]


def page1():
    need = "<ul>" + "".join(f'<li class="r"><b>{a}</b>{b}</li>' for a, b in [
        ("Thread:", "six-strand cotton floss (use 2 or 3 strands), pearl cotton or fine crewel wool."),
        ("Needle:", "a sharp embroidery or chenille needle with an eye big enough for your thread."),
        ("Thimble", "and small pliers or a rubber grip, to pull the needle through thick felt."),
        ("Transfer:", "tracing paper or tissue paper, tear-away stabilizer, or a chalk pencil. See page 6."),
        ("Small scissors", "and a few pins or clips."),
    ]) + "</ul>"
    sts = "".join(f'<div class="st">{art3.stitch_box(fn())}<b>{a}</b><span>{b}</span></div>' for a, b, fn in STITCHES)
    return f"""<main class="page">
<span class="kicker">Embroidery and monogram patterns for wool felt hats</span>
<div class="head"><h1>Stitch your hat<i>.</i></h1></div>
<div class="intro"><div><p class="lead">Two alphabets, eight sauna motifs and a leaf wreath, all at true size. Trace, stitch, and your hat is easy to find on the peg.</p>
<div class="felt notes">
<p><b>Thick felt is kind to beginners</b>Sauna hat felt is about 4–5 mm thick and does not fray. Stitches sit on top and hold their shape.</p>
<p><b>Keep the inside smooth</b>The inside of the hat touches your head. Where you can, take shallow stitches that stay in the outer part of the felt, and keep knots small.</p>
<p><b>Go slow, pull gently</b>Pull each stitch just snug: tight stitches pucker felt. Push the needle with a thimble rather than forcing it.</p>
</div></div>
{w2.sec("What you need", "", need, 2)}</div>
{w2.ph("Eight stitches", "All you need for the patterns in this pack.").replace('class="ph"', 'class="ph small"')}
<div class="stitches">{sts}</div>
<p class="fine">Inside: stitches (this page) · single-line alphabet (2) · outline alphabet (3) · motifs (4) · where to place them (5) · transfer and finishing (6) · transfer sheet (7)</p>
{C.foot(NAME + " · 1 of 7")}
</main>"""


def page2():
    return f"""<main class="page">
{w2.ph("Single-line alphabet", "Letters about 7/8 in tall. Stitch them in back stitch or stem stitch, 2 or 3 strands.")}
<div class="ts">{mono_sheet()}</div>
{monogram_examples()}
{scale_check()}
{C.foot(NAME + " · 2 of 7")}
</main>"""


def page3():
    return f"""<main class="page">
{w2.ph("Outline alphabet", "Letters and numbers about 5/8 in tall. Outline in split stitch, then fill with satin stitch across the stroke.")}
<div class="ts">{outline_sheet()}</div>
<p class="cap">Letters drawn from Bricolage Grotesque Bold (SIL Open Font License 1.1). For a raised letter, fill it first with a few long stitches, then cover them with satin stitch.</p>
<div class="felt" style="margin-top:.2in"><div class="grid">
<p><b>Size it up or down</b>Print at 125% or 75% for bigger or smaller letters. The check squares change with them, so ignore them then.</p>
<p><b>Satin on felt</b>Keep satin areas narrow, under about 1/2 in. Long satin stitches snag. Wide letters look better in split stitch rows.</p>
<p><b>Mirror for the back?</b>No need. Every transfer method in this pack keeps the letters the right way round.</p>
</div></div>
{scale_check()}
{C.foot(NAME + " · 3 of 7")}
</main>"""


def motif_figs():
    figs = []
    for name, how, fn in art3.MOTIFS:
        w, h, b = fn()
        figs.append(f'<figure>{art3.tsvg(w, h, b, 1.5)}<figcaption><b>{name}</b>{how}</figcaption></figure>')
    return "".join(figs)


def page4():
    w, h, wr = art3.m_wreath(92)
    return f"""<main class="page">
{w2.ph("Sauna motifs", "True size. Small dots mark French knots. Mix them with a letter, or stitch a row around the hat.")}
<div class="motifs">{motif_figs()}<figure>{art3.tsvg(w, h, wr, 1.4)}<figcaption><b>Leaf wreath</b>Frame for one initial, inner space about 1.6 in</figcaption></figure></div>
{scale_check()}
{C.foot(NAME + " · 4 of 7")}
</main>"""


def zone_bell():
    o = [art.bell_hat(40, 20, .9, pattern=False, uid="zb")]
    o.append('<path d="M118 140C150 110 245 110 277 140L292 278H103Z" fill="#f5c7a0" fill-opacity=".55" stroke="#1b1512" stroke-width="2" stroke-dasharray="7 6"/>')
    o.append('<path d="M70 300H325" fill="none" stroke="#1b1512" stroke-width="2" stroke-dasharray="3 6"/>')
    o.append('<text x="197" y="214" text-anchor="middle" font-family="Inter" font-size="17" font-weight="600" fill="#1b1512" stroke="none">front zone</text>')
    o.append('<text x="400" y="300" font-family="Inter" font-size="15" fill="#3d332c" stroke="none">fold-up line</text>')
    o.append('<path d="M330 300H392" stroke="#3d332c" stroke-width="1.5" fill="none"/>')
    return art.svg(520, 420, "".join(o), 3)


def zone_bucket():
    o = [art.bucket_hat(30, 110, .8, pattern=False)]
    o.append('<path d="M172 192C172 124 202 104 246 104C290 104 320 124 320 192C290 200 202 200 172 192Z" fill="#f5c7a0" fill-opacity=".55" stroke="#1b1512" stroke-width="2" stroke-dasharray="7 6"/>')
    p = ((66, 270), (110, 238), (172, 226), (246, 226))
    q = ((246, 226), (320, 226), (382, 238), (426, 270))
    o.append(f'<path d="M66 270C110 238 172 226 246 226C320 226 382 238 426 270" fill="none" stroke="#1b1512" stroke-width="2" stroke-dasharray="7 6"/>')
    pts = art3._bez(*p, 3) + art3._bez(*q, 3) + [q[3]]
    for x, y in pts[1:-1]:
        o.append(f'<circle cx="{f(x)}" cy="{f(y)}" r="7" fill="#f0a877" stroke="#1b1512" stroke-width="2"/>')
    o.append('<text x="246" y="166" text-anchor="middle" font-family="Inter" font-size="17" font-weight="600" fill="#1b1512" stroke="none">crown front</text>')
    o.append('<text x="246" y="330" text-anchor="middle" font-family="Inter" font-size="15" fill="#3d332c" stroke="none">small motifs around the brim</text>')
    return art.svg(500, 340, "".join(o), 3)


def spacing_strip():
    """True-size strip, 6 in long: marks every 2 in and every 3 in for spacing motifs around the hat."""
    L = 600
    o = [f'<rect x="0" y="0" width="{L}" height="64" fill="#fffdf9" stroke="#1b1512" stroke-width="1.2"/>']
    for i in range(0, L + 1, 25):
        hh = 16 if i % 100 == 0 else 8
        o.append(f'<path d="M{i} 0V{hh}" stroke="#1b1512" stroke-width="{1.2 if i % 100 == 0 else .7}"/>')
        if i % 100 == 0:
            o.append(f'<text x="{i + (5 if i == 0 else 0)}" y="29" text-anchor="{"start" if i == 0 else "end" if i == L else "middle"}" font-family="Inter" font-size="10" fill="#1b1512">{i // 100}</text>')
    for i in range(0, L + 1, 200):
        o.append(f'<circle cx="{i if 0 < i < L else (6 if i == 0 else L - 6)}" cy="44" r="5" fill="#f0762e"/>')
    for i in range(0, L + 1, 300):
        o.append(f'<rect x="{(i if 0 < i < L else (0 if i == 0 else L - 9)) - (4.5 if 0 < i < L else 0)}" y="50" width="9" height="9" fill="#1b1512"/>')
    o.append(f'<text x="{L / 2}" y="62" text-anchor="middle" font-family="Inter" font-size="8" fill="#6f655c" dx="0" dy="0"></text>')
    return art3.tsvg(L, 64, "".join(o), 1)


def page5():
    return f"""<main class="page">
{w2.ph("Where to stitch", "Drawings are not to scale. Hold your design against your own hat before you start.")}
<div class="place">
<figure>{zone_bell()}<figcaption><b>Bell hat</b>
<ul><li>Center the design on the front, away from any seam. Mark the center with a pin.</li>
<li>Many people fold the edge up. Keep your design above the fold so it still shows; try the fold on first and mark it.</li>
<li>Letters about 3/4–1 in tall read well from across the room. A wreath with one initial fills the front nicely.</li></ul></figcaption></figure>
<figure>{zone_bucket()}<figcaption><b>Bucket hat</b>
<ul><li>The crown front takes a monogram or one motif, like on the bell hat.</li>
<li>The brim is curved. Use small motifs, about 1 in or less: snowflakes, dots of steam, leaves.</li>
<li>Stitch brim motifs on the top side only and keep the stitches shallow.</li></ul></figcaption></figure>
</div>
<div class="tools"><div class="txt"><h3>Spacing a ring of motifs</h3><p style="max-width:none">DIVELUX hats measure about 24 in around. That fits 12 motifs 2 in apart, or 8 motifs 3 in apart. Cut out the strip, lay it along the hat and mark each spot with chalk or a pin.</p></div>
<div>{spacing_strip()}<p style="font-size:7.4pt;color:var(--muted);margin-top:.05in;max-width:none">Spacing strip, true size, 6 in: inch marks · <b style="color:var(--ember)">●</b> every 2 in · <b>■</b> every 3 in</p></div></div>
<div class="felt" style="margin-top:.18in"><div class="grid">
<p><b>Mark the center first</b>Fold a strip of paper around the hat, find the halfway point, and pin it opposite the seam.</p>
<p><b>Test on a scrap</b>Try your thread and stitch on a scrap of felt or on the inside of the folded edge.</p>
<p><b>Less is more</b>One clear initial or one motif looks better than a crowded front, and it stitches in an evening.</p>
</div></div>
{scale_check()}
{C.foot(NAME + " · 5 of 7")}
</main>"""


def page6():
    return f"""<main class="page">
{w2.ph("Transfer and finish", "Your hat stays dry. Start with a water-free method.")}
<div class="methods">
<div class="m best"><span class="tag">Water-free · recommended</span><h3>Tissue or tracing paper</h3><ol>
<li><span>Trace the design onto tissue paper or thin tracing paper with a pencil.</span></li>
<li><span>Pin or baste it in place on the hat.</span></li>
<li><span>Stitch right through the paper and the felt.</span></li>
<li><span>Tear the paper away gently, holding the stitches with a thumb. Pick out small bits with tweezers.</span></li></ol></div>
<div class="m best"><span class="tag">Water-free</span><h3>Tear-away stabilizer</h3><ol>
<li><span>Print or trace the design onto tear-away embroidery stabilizer. Some brands go through a home printer: check the package.</span></li>
<li><span>Pin, baste or stick it on, stitch through it.</span></li>
<li><span>Tear it off along the stitches, as the package describes.</span></li></ol></div>
<div class="m"><span class="tag">Water-free</span><h3>Template and chalk</h3><ol>
<li><span>Cut the motif out of the page, or glue it to thin card first.</span></li>
<li><span>Hold it on the hat and draw around it with a chalk pencil (dark felt) or an air-erasable fabric pen (light felt).</span></li>
<li><span>Stitch over the line. Brush leftover chalk off with a dry brush.</span></li></ol></div>
<div class="m"><span class="tag">Uses a little water</span><h3>Wash-away stabilizer</h3><ol>
<li><span>Stitch through it like the tear-away kind.</span></li>
<li><span>Tear and trim away as much as you can, dry.</span></li>
<li><span>Most wash-away stabilizers need water to dissolve. Follow the stabilizer maker’s directions, but only dab the leftover bits with a cotton swab dipped in cool, room-temperature water (about 68–75 °F / 20–24 °C).</span></li>
<li><span>Never hold the hat under the tap or put it in a bowl. Press with a dry towel, squeeze, don’t wring, and let it air-dry flat.</span></li></ol></div>
</div>
<div class="warn"><h3>Finishing and care</h3><div>
<p>Weave thread tails under a few stitches on the inside instead of tying big knots. Skip beads, sequins, metal charms and metallic thread: metal gets hot in the sauna, and beads can snag. Natural-fiber threads (cotton, wool) suit wool felt.</p>
<p>Wear the hat dry, as always. If it ever needs a wash, hand-wash only in cool, room-temperature water (about 68–75 °F / 20–24 °C, never warm or hot), squeeze, don’t wring, and air-dry. No washing machine, no dryer.</p></div></div>

<div class="felt" style="margin-top:.18in"><div class="grid">
<p><b>Pick a contrast</b>Light thread on dark felt, dark thread on light felt. Hold the skein against the hat in daylight first.</p>
<p><b>One or two colors</b>A single color looks calm and modern. Add a second only for small accents like knots or leaves.</p>
<p><b>Thread length</b>Work with about 18 in (45 cm) of thread at a time. Longer pieces tangle and wear thin.</p>
</div></div>
<p class="fine" style="margin-top:.16in">Made for wool felt sauna hats like the ones DIVELUX sells, but the patterns work on any thick felt, a tote bag or a pillow. More free sauna printables: <a href="{C.TOOLS}">diveluxsaunahat.com/pages/sauna-tools</a></p>
{C.foot(NAME + " · 6 of 7")}
</main>"""


def page7():
    """Compact transfer sheet: everything again at true size, ready to print on tear-away stabilizer or tissue."""
    o, x, y, rowh = [], 0, 0, 0
    W = 700
    pieces = [fn() for _, _, fn in art3.MOTIFS] + [art3.m_wreath(80)]
    for w, h, b in pieces:
        if x + w > W:
            x, y, rowh = 0, y + rowh + 16, 0
        o.append(f'<g transform="translate({f(x)} {f(y)})">{b}</g>')
        x += w + 18
        rowh = max(rowh, h)
    y += rowh + 20
    letters = list(art3.MONO)
    x = 0
    for ch in letters:
        w = art3.MONO[ch][0] * .46
        if x + w > W:
            x, y = 0, y + 62
        o.append(art3.mono_letter(ch, x, y, 46, 1.5)[0])
        x += w + 20
    y += 50
    return f"""<main class="page white">
{w2.ph("Transfer sheet", "Print this page on tear-away stabilizer or trace it onto tissue paper. Cut out what you need.")}
<div class="ts">{art3.tsvg(W, y, "".join(o), 1.5)}</div>
{scale_check()}
{C.foot(NAME + " · 7 of 7")}
</main>"""


def build():
    body = "\n".join([page1(), page2(), page3(), page4(), page5(), page6(), page7()])
    C.write(os.path.join(C.ROOT, SLUG, SLUG + ".html"), C.doc(TITLE, DESC, KEYWORDS, CSS, body))
    meta = dict(title="Sauna Hat Embroidery and Monogram Patterns (Printable, True Size)", subject=DESC, keywords=KEYWORDS)
    jobs = C.std_jobs(SLUG, SLUG + ".html", SLUG, meta)
    return dict(slug=SLUG, jobs=jobs, preview=dict(pdf=jobs[0]["pdf"], pages=[1, 2, 4], dpi=75))
