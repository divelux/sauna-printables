"""23. Spa and gym sauna signs: eight landscape signs, one per page, plus two sheets with four small signs each.
Pictograms come from the DIVELUX Sauna & Banya Icon Set (../icons/svg, CC BY 4.0); three are drawn here."""
import os
import common as C
import w2

SLUG = "spa-sauna-signs-set"
TITLE = "Spa and Sauna Signs Set"
DESC = "Eight printable signs for spas, gyms and clubs: Quiet zone, Shower before sauna, Sit on a towel, No phones, Keep the door closed, Shoes off, Sauna in use, Sauna free. Full-page and four-per-sheet."
KEYWORDS = "spa signs printable, sauna signs, quiet zone sign, shower before sauna sign, no phones sign, sauna in use sign, gym locker room signage, DIVELUX"

NO = '<line x1="3" y1="21" x2="21" y2="3" stroke="#f0762e" stroke-width="2"/>'


def ic(inner):
    return (f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" '
            f'stroke-linejoin="round" aria-hidden="true">{inner}</svg>')


QUIET = ic('<path d="M3.5 9.5H7l4.5-4v13L7 14.5H3.5z"/><path d="M15 9.6a3.4 3.4 0 0 1 0 4.8"/><path d="M17.6 7a7 7 0 0 1 0 10"/>' + NO)
PHONE = ic('<rect x="7" y="2.5" width="10" height="19" rx="2"/><path d="M10.8 18.3h2.4"/>' + NO)


def icon(name, no=False):
    s = w2.icon(name)
    return s.replace("</svg>", NO + "</svg>") if no else s


SIGNS = [  # kicker, headline, line, icon, tint
    ("Please", "Quiet zone", "Soft voices, or none at all.", QUIET, "t3"),
    ("Please", "Shower before sauna", "Rinse off first. It keeps the room fresh for everyone.", icon("shower"), "t3"),
    ("Please", "Sit on a towel", "Keep a towel between you and the bench.", icon("towel"), "t3"),
    ("Please", "No phones", "No calls, no photos, no video. Leave it in your locker.", PHONE, "t3"),
    ("Please", "Keep the door closed", "In or out quickly. The heat stays inside.", icon("sauna-door"), "t3"),
    ("Please", "Shoes off", "Leave shoes and sandals outside the hot room.", icon("slippers", no=True), "t3"),
    ("Right now", "Sauna in use", "Please knock, or wait for the next round.", icon("loyly"), "t1"),
    ("Right now", "Sauna free", "Come in. Close the door behind you.", icon("sauna-bench"), "t4"),
]

CSS = w2.CSS + """
.page{padding:.4in .5in .3in}
.wrap{flex:1;display:flex;align-items:center;justify-content:center;min-height:0}
.sign{width:9.9in;height:7.05in;display:grid;grid-template-columns:3.3in 1fr;border:3px solid var(--ink);border-radius:6px;overflow:hidden;background:var(--paper);flex:none}
.sign .pic{display:flex;align-items:center;justify-content:center;border-right:3px solid var(--ink)}
.sign .pic.t1{background:var(--t1)}.sign .pic.t3{background:var(--t3)}.sign .pic.t4{background:var(--t4)}
.sign .pic svg{width:2.5in;height:2.5in;display:block;color:var(--ink)}
.sign .txt{display:flex;flex-direction:column;justify-content:center;padding:.3in .5in .3in .55in;min-width:0}
.sign .k{font-family:var(--display);font-weight:600;font-size:22pt;color:var(--ink-2);letter-spacing:.005em}
.sign h1,.sign .h1{font-family:var(--display);font-weight:800;font-stretch:75%;font-size:128pt;line-height:.84;letter-spacing:-.022em;margin:.14in 0 .3in -.05in;white-space:normal}
.sign .h1.long{font-size:104pt}
.sign p{font-family:var(--display);font-weight:500;font-size:25pt;line-height:1.22;color:var(--ink-2);text-wrap:balance}
.four{padding:.3in .4in .3in;background:#fff}
.four .how{padding-bottom:.06in}
.four .cards{flex:1;display:grid;grid-template-columns:auto auto;grid-template-rows:auto auto;justify-content:center;align-content:center;gap:.16in;min-height:0}
.four .cut{outline:1px dashed #8d8378;outline-offset:.05in}
.four .sign{zoom:.475;border-width:5px}
.four .sign .pic{border-right-width:5px}
"""


def sign(i, tag="div"):
    k, h, line, svg, tint = SIGNS[i]
    long = " long" if len(h) > 12 else ""
    return (f'<div class="sign"><div class="pic {tint}">{svg}</div><div class="txt"><span class="k">{C.esc(k)}</span>'
            f'<{tag} class="h1{long}">{C.esc(h)}<i>.</i></{tag}><p>{C.esc(line)}</p></div></div>')


def build():
    pages = []
    for i in range(len(SIGNS)):
        pages.append(f"""<main class="page"><div class="wrap">{sign(i, "h1" if i == 0 else "div")}</div>
{C.foot(f"Spa and Sauna Signs · {i + 1} of {len(SIGNS)}")}</main>""")
    for a in (0, 4):
        cards = "".join(f'<div class="cut">{sign(i)}</div>' for i in range(a, a + 4))
        pages.append(f"""<main class="page four">
<div class="how"><span><b>Spa and Sauna Signs</b> · small size, four per sheet, 4.7 × 3.35 in</span><span>Print at 100% on heavy paper. Cut along the dashed lines.</span></div>
<div class="cards">{cards}</div>
{C.foot()}</main>""")
    C.write(os.path.join(C.ROOT, SLUG, SLUG + ".html"), C.doc(TITLE, DESC, KEYWORDS, CSS, "\n".join(pages), land=True))
    meta = dict(title="Spa and Sauna Signs Set (8 Printable Signs)", subject=DESC, keywords=KEYWORDS)
    jobs = C.std_jobs(SLUG, SLUG + ".html", SLUG, meta, land=True)
    return dict(slug=SLUG, jobs=jobs, preview=dict(pdf=jobs[0]["pdf"], pages=[1, 2, 7, 9], dpi=60, cols=2))
