"""22. Printable hat-size measuring tape: three 9 in strips that join into a 27 in (68.5 cm) tape, inches on the
top edge and centimeters on the bottom edge, with a scale check line. Landscape.
The strips are SVG drawn 1:1 in CSS pixels (96 per inch), so they are exact when printed at 100%;
build-time check: verify_tape.py measures the finished PDFs.
Hat facts are the brand brief's: one size, about 24 in around, a loose fit is a plus, too big = fold the edge up."""
import os
import common as C
import w2

SLUG = "sauna-hat-size-measuring-tape"
TITLE = "Printable Hat Size Measuring Tape"
DESC = "A printable paper measuring tape for head size, in inches and centimeters: three strips that join into a 27 in tape, with a scale check line so you know it printed at 100%."
KEYWORDS = "printable measuring tape, head circumference tape, hat size measuring tape printable, how to measure head for hat, sauna hat size, inches and centimeters, DIVELUX"
INK = "#1b1512"
LEN = 9            # inches per strip
U = 96             # SVG units per inch = CSS px per inch, so the SVG is drawn 1:1 and never rescaled
TAB = 48           # glue tab, units (0.5 in)
H = 84             # strip height, units (0.875 in)


def strip(k):
    """Strip k (0, 1, 2) covers LEN*k .. LEN*(k+1) inches. Left edge = start of the scale.
    Width and height are whole CSS pixels on purpose: Chromium snaps an SVG box to whole pixels, and a box of
    82.56 px was drawn 0.7% too small. With whole pixels the viewBox maps 1:1."""
    start_in = LEN * k
    W = LEN * U
    last = k == 2
    total = W + (0 if last else TAB)
    o = [f'<rect x="0" y="0" width="{total}" height="{H}" fill="#f6f3ee" stroke="none"/>']
    if not last:
        o.append(f'<rect x="{W}" y="0" width="{TAB}" height="{H}" fill="#f5c7a0" stroke="none"/>')
    # inch ticks along the top edge, every 1/8 in (12 units)
    d = []
    for i in range(0, LEN * 8 + 1):
        ln = 21 if i % 8 == 0 else 14 if i % 4 == 0 else 10 if i % 2 == 0 else 6
        d.append(f"M{i * 12} 0V{ln}")
    o.append(f'<path d="{"".join(d)}" stroke="{INK}" stroke-width="1" fill="none"/>')
    for i in range(0, LEN + 1):
        if i == 0 and k > 0:
            continue
        anchor, dx = ("start", 3) if i == 0 else ("end", -4) if i == LEN else ("middle", 0)
        o.append(f'<text x="{i * U + dx}" y="34" text-anchor="{anchor}" font-size="12.5" font-weight="700" fill="{INK}">{start_in + i}</text>')
    # centimeter ticks along the bottom edge, every millimeter
    d = []
    mm = -(-start_in * 254 // 10)          # first whole millimeter on this strip
    while True:
        x = (mm / 25.4 - start_in) * U
        if x > W + 1e-6:
            break
        ln = 19 if mm % 10 == 0 else 13 if mm % 5 == 0 else 7
        d.append(f"M{x:.3f} {H}V{H - ln}")
        if mm % 10 == 0 and 8 < x < W - 8:
            o.append(f'<text x="{x:.2f}" y="{H - 23}" text-anchor="middle" font-size="9" font-weight="500" fill="#3d332c">{mm // 10}</text>')
        mm += 1
    o.append(f'<path d="{"".join(d)}" stroke="{INK}" stroke-width=".8" fill="none"/>')
    if k == 0:
        o.append('<text x="32" y="48" font-size="6.4" font-weight="600" letter-spacing=".9" fill="#6f655c">INCHES ON TOP · CENTIMETERS BELOW · START AT THIS END</text>')
    # the DIVELUX hat mark at 24 in
    if start_in <= 24 <= start_in + LEN:
        x = (24 - start_in) * U
        o.append(f'<circle cx="{x}" cy="45.5" r="4.3" fill="#f0762e" stroke="none"/>')
        o.append(f'<text x="{x + 9}" y="48.5" font-size="8.2" font-weight="600" fill="{INK}">DIVELUX hat: about 24 in</text>')
    if not last:
        o.append(f'<path d="M{W} 0V{H}" stroke="{INK}" stroke-width="1.6" fill="none"/>')
        for n, word in enumerate(("TAPE", f"STRIP {k + 2}", "HERE")):
            o.append(f'<text x="{W + TAB / 2:g}" y="{36 + 9 * n}" text-anchor="middle" font-size="6.4" font-weight="600" fill="{INK}">{word}</text>')
    o.append(f'<rect x="0" y="0" width="{total}" height="{H}" fill="none" stroke="#8d8378" stroke-width="1" stroke-dasharray="5 4"/>')
    o.append(f'<path d="M0 0V{H}" stroke="{INK}" stroke-width="1.6" fill="none"/>')
    return (f'<svg class="strip" xmlns="http://www.w3.org/2000/svg" width="{total}" height="{H}" viewBox="0 0 {total} {H}" '
            f'style="width:{total}px;height:{H}px;flex:none" font-family="Inter, Arial, sans-serif" '
            f'aria-label="Measuring tape strip {k + 1}: {start_in} to {start_in + LEN} inches">{"".join(o)}</svg>')


def check():
    """Scale check: a 4 in line, a 10 cm line and the width of a bank card (ISO/IEC 7810 ID-1: 85.60 mm)."""
    def bar(y, length, label):
        x0, x1 = 3, 3 + length
        return (f'<path d="M{x0} {y}H{x1:.3f}M{x0} {y - 7}V{y + 7}M{x1:.3f} {y - 7}V{y + 7}" stroke="{INK}" stroke-width="1.4" fill="none"/>'
                f'<text x="{x1 + 10:.1f}" y="{y + 3.5}" font-size="9.6" font-weight="600" fill="{INK}">{label}</text>')
    b = bar(12, 4 * U, "4 in exactly") + bar(42, 100 / 25.4 * U, "10 cm exactly") + bar(72, 85.6 / 25.4 * U, "bank card width, 85.6 mm")
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="504" height="84" viewBox="0 0 504 84" style="width:504px;height:84px;display:block" '
            f'font-family="Inter, Arial, sans-serif" aria-label="Scale check lines">{b}</svg>')


STEPS = [
    ("Print at 100%", "Choose “Actual size” or 100% in the print dialog, not “Fit to page”."),
    ("Check the scale", "Lay a ruler or a bank card on the check lines below. If they match, the tape is true."),
    ("Cut and join", "Cut out the three strips. Tape strip 2 onto the tab of strip 1, edge on the line, then strip 3 onto strip 2."),
    ("Measure", "Wrap the tape around your head: across the middle of the forehead, just above the ears, around the widest part at the back. Snug, not tight. Read the number that meets the zero end."),
]

CSS = w2.CSS + """
.page{padding:.4in .5in .3in;background:#fff}
.top{display:flex;justify-content:space-between;align-items:flex-end;gap:.4in;flex:none}
h1{font-size:54pt;margin:.04in 0 0 -.025in}
.top .lead{font-size:11.5pt;max-width:3.6in;text-align:right;padding-bottom:.03in}
.strips{display:flex;flex-direction:column;align-items:flex-start;row-gap:.13in;margin:.15in 0 .15in;flex:none}
.strip{display:block}
.low{flex:1;display:grid;grid-template-columns:1.2fr 1fr;column-gap:.4in;min-height:0}
.steps{counter-reset:s;display:grid;grid-template-columns:1fr 1fr;column-gap:.3in;align-content:start}
.steps li{counter-increment:s;display:grid;grid-template-columns:.34in 1fr;border-top:1px solid var(--line-2);padding:.055in 0;font-size:8.6pt;line-height:1.36;color:var(--ink-2)}
.steps li:nth-child(-n+2){border-top:2px solid var(--ink)}
.steps li::before{content:counter(s);font-family:var(--display);font-weight:700;font-stretch:75%;font-size:24pt;line-height:.92;color:var(--ink)}
.steps b{display:block;font-family:var(--display);font-weight:700;font-size:12pt;line-height:1.15;color:var(--ink);letter-spacing:-.008em}
.chk{grid-column:1 / -1;border-top:1px solid var(--line-2);padding-top:.07in}
.chk .t{font-family:var(--body);font-size:6.4pt;letter-spacing:.16em;text-transform:uppercase;font-weight:600;color:var(--muted);margin-bottom:.05in}
.fit{background:var(--paper);border-radius:6px;padding:.16in .2in;display:flex;flex-direction:column;align-self:start}
.fit .t{font-family:var(--display);font-weight:800;font-stretch:75%;font-size:25pt;line-height:.92;letter-spacing:-.015em;margin-bottom:.08in}
.fit li{font-size:9.2pt;line-height:1.42;color:var(--ink-2);padding:.055in 0;border-top:1px solid var(--line-2)}
.fit li b{color:var(--ink);font-weight:600}
"""


def build():
    steps = "".join(f"<li><span><b>{C.esc(t)}</b>{C.esc(x)}</span></li>" for t, x in STEPS)
    body = f"""<main class="page">
<div class="top"><div><span class="kicker">Print at 100% · inches and centimeters</span>
<h1>Hat size tape<i>.</i></h1></div>
<p class="lead">A paper tape measure for your head. Three strips make 27 in (68.5 cm).</p></div>
<div class="strips">{strip(0)}{strip(1)}{strip(2)}</div>
<div class="low">
<div><ol class="steps">{steps}</ol>
<div class="chk"><p class="t">Scale check · measure these before you cut</p>{check()}</div></div>
<div class="fit"><p class="t">What your number means</p><ul>
<li><b>DIVELUX wool sauna hats come in one size,</b> about 24 in (61 cm) around. The orange dot on the tape marks it.</li>
<li><b>Under 24 in:</b> the hat sits loose. In a sauna hat a loose fit is a plus.</li>
<li><b>Feels too big?</b> Fold the edge up.</li>
<li><b>About 24 in or more:</b> the hat sits close to the head.</li>
<li><b>Buying another hat?</b> Most makers size by this same number, in inches or centimeters.</li>
</ul></div>
</div>
{C.foot("Cut along the dashed lines. Solid end lines are the exact start of each strip.")}
</main>"""
    C.write(os.path.join(C.ROOT, SLUG, SLUG + ".html"), C.doc(TITLE, DESC, KEYWORDS, CSS, body, land=True))
    meta = dict(title="Printable Hat Size Measuring Tape (Inches and Centimeters)", subject=DESC, keywords=KEYWORDS)
    jobs = C.std_jobs(SLUG, SLUG + ".html", SLUG, meta, land=True)
    return dict(slug=SLUG, jobs=jobs, preview=dict(pdf=jobs[0]["pdf"]))
