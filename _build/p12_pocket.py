"""12. First-timer pocket card: four fold-in-half cards per sheet (folded size 2.4 x 3.6 in).
Only common sauna etiquette and comfort advice; nothing medical."""
import os
import common as C
import w2

SLUG = "sauna-first-timer-pocket-card"
TITLE = "First Sauna Pocket Card"
DESC = "A printable pocket checklist for a first sauna visit: what to pack and what to do in the heat. Four fold-in-half cards per sheet."
KEYWORDS = "first time sauna checklist, sauna for beginners, what to bring to a sauna, sauna pocket card, sauna etiquette for beginners, printable card, DIVELUX"

PACK = [
    "<b>Two towels:</b> one to sit on, one to dry off",
    "<b>Water bottle</b>",
    "<b>Flip-flops</b> or shower sandals",
    "<b>Swimsuit,</b> if the place asks for one",
    "<b>Wool felt sauna hat,</b> worn dry",
]
STEPS = [
    ("Shower first", "Take off jewelry and watches. Metal gets hot."),
    ("Sit on your towel", "Start on a lower bench. It is cooler there."),
    ("Keep it short", "A few minutes is fine for a first round. Stay only while it feels good."),
    ("Ask before you pour", "Water on the stones means more steam for everyone."),
    ("Cool down and rest", "Fresh air or a cool rinse, a seat, some water. Go again if you like."),
]

CSS = w2.CSS + """
.page{padding:.2in .4in .26in;background:#fff}
.cards{flex:1;display:grid;grid-template-columns:4.8in 4.8in;grid-template-rows:3.6in 3.6in;justify-content:center;align-content:center;min-height:0}
.piece{position:relative;outline:1px dashed #8d8378;display:grid;grid-template-columns:1fr 1fr;background:var(--paper)}
.piece::after{content:"";position:absolute;left:50%;top:0;bottom:0;border-left:1px dashed #b9afa2}
.pan{padding:.15in .16in .1in;display:flex;flex-direction:column;min-width:0;overflow:hidden}
.pan .top{display:flex;justify-content:space-between;align-items:center}
.pan .top img{height:.085in;display:block}
.pan .top span{font-size:5.2pt;letter-spacing:.16em;text-transform:uppercase;font-weight:600;color:var(--muted)}
.pan h1,.pan .h1{font-family:var(--display);font-weight:800;font-stretch:75%;font-size:35pt;line-height:.84;letter-spacing:-.02em;margin:.13in 0 .07in -.012in;white-space:normal}
.pan .sub{font-family:var(--display);font-weight:500;font-size:8.6pt;line-height:1.25;color:var(--ink-2);margin-bottom:.09in}
.pan .ladder{height:.05in}
.pan .lab{font-family:var(--body);font-size:5.4pt;letter-spacing:.16em;text-transform:uppercase;font-weight:600;color:var(--muted);margin:.1in 0 .03in}
.pan .cl li{grid-template-columns:.17in 1fr;font-size:6.9pt;line-height:1.3;padding:.034in 0}
.pan .cl .box{width:.1in;height:.1in;margin-top:.012in;border-width:1px}
.pan ol{counter-reset:s}
.pan ol li{counter-increment:s;display:grid;grid-template-columns:.2in 1fr;font-size:7.1pt;line-height:1.3;color:var(--ink-2);padding:.037in 0;border-top:1px solid var(--line)}
.pan ol li:first-child{border-top:0;padding-top:0}
.pan ol li::before{content:counter(s);font-family:var(--display);font-weight:700;font-stretch:75%;font-size:15pt;line-height:.95;color:var(--ink)}
.pan ol b{display:block;font-family:var(--display);font-weight:700;font-size:9.2pt;line-height:1.15;color:var(--ink);letter-spacing:-.005em}
.pan .out{margin-top:auto;border-top:1.5px solid var(--ink);padding-top:.05in;font-family:var(--display);font-weight:700;font-size:8.4pt;line-height:1.2;color:var(--ink)}
.pan .fine{font-size:5.3pt;line-height:1.35;margin-top:.035in}
.heat{display:grid;grid-template-rows:repeat(3,1fr);border-left:1.5px solid var(--ink)}
.heat div{display:flex;justify-content:space-between;align-items:baseline;padding:.035in .08in;font-size:6.6pt;color:var(--ink-2)}
.heat b{font-family:var(--display);font-weight:700;font-size:8pt;color:var(--ink)}
.heat .a{background:var(--t1)}.heat .b{background:var(--t2)}.heat .c{background:var(--t4)}
.pan .cfoot{margin-top:auto;padding-top:.04in;border-top:1px solid var(--line-2);font-size:5pt;line-height:1.25;color:var(--muted);white-space:nowrap}
.pan .cfoot a{color:var(--ink);text-decoration:none;font-weight:600}
.pan .cfoot b{color:var(--ink);font-weight:600}
"""


def piece(tag):
    logo = C.logo_data_uri()
    steps = "".join(f"<li><span><b>{C.esc(t)}</b>{C.esc(x)}</span></li>" for t, x in STEPS)
    return f"""<div class="piece">
<div class="pan">
<div class="lab" style="margin-top:0">In the heat</div>
<ol>{steps}</ol>
<p class="out">Dizzy, sick or unwell? Leave the heat right away.</p>
<p class="fine">No alcohol before or in the sauna. Pregnant or have a health condition? Ask your doctor first. General information, not medical advice.</p>
</div>
<div class="pan">
<div class="top"><img src="{logo}" alt="DIVELUX"><span>Pocket card</span></div>
<{tag} class="h1">First sauna<i>?</i></{tag}>
<p class="sub">A short checklist for your first visit.</p>
<div class="ladder"><i></i><i></i><i></i><i></i></div>
<div class="lab">Pack</div>
{w2.checks(PACK)}
<div class="lab">Where to sit</div>
<div class="heat"><div class="a"><b>Top bench</b><span>hottest</span></div><div class="b"><b>Middle bench</b><span>milder</span></div><div class="c"><b>Lower bench</b><span>mildest: start here</span></div></div>
<div class="cfoot"><b>DIVELUX</b> wool sauna hats — <a href="{C.SITE}">diveluxsaunahat.com</a></div>
</div>
</div>"""


def build():
    d = os.path.join(C.ROOT, SLUG)
    body = f"""<main class="page">
<div class="how"><span><b>First Sauna Pocket Card</b> · four per sheet, folded size 2.4 × 3.6 in</span><span>Print at 100% on heavy paper. Cut along the outer dashed lines, then fold each card in half, print side out.</span></div>
<div class="cards">{piece("h1")}{piece("div")}{piece("div")}{piece("div")}</div>
{C.foot()}
</main>"""
    C.write(os.path.join(d, SLUG + ".html"), C.doc(TITLE, DESC, KEYWORDS, CSS, body, land=True))
    meta = dict(title="First Sauna Pocket Card: A Printable Checklist for First-Timers", subject=DESC, keywords=KEYWORDS)
    jobs = C.std_jobs(SLUG, SLUG + ".html", SLUG, meta, land=True)
    return dict(slug=SLUG, jobs=jobs, preview=dict(pdf=jobs[0]["pdf"]))
