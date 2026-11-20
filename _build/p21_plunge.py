"""21. Cold plunge safety card: one page to post next to the tub.
Same cautious lines as ../tools/cold-plunge-timer (README "Safety text"), and the same two sources, both re-read in
November 2026: U.S. National Weather Service, "Cold Water Hazards and Safety" (weather.gov/safety/coldwater) and
American Heart Association News, "You're not a polar bear: The plunge into cold water comes with risks" (2022).
No benefit claims of any kind."""
import os
import common as C
import w2

SLUG = "cold-plunge-safety-card"
TITLE = "Cold Plunge Safety Card"
DESC = "A printable one-page safety card to post by a cold plunge: what to do before you get in, when to get out right away, and how to warm up after. No health claims."
KEYWORDS = "cold plunge safety, cold plunge rules sign, ice bath safety, cold water shock, cold plunge checklist, sauna cold plunge sign, printable card, DIVELUX"
NWS = "https://www.weather.gov/safety/coldwater"
AHA = "https://www.heart.org/en/news/2022/12/09/youre-not-a-polar-bear-the-plunge-into-cold-water-comes-with-risks"

BEFORE = [
    "<b>Never plunge alone.</b> Have someone within reach who is staying out of the water.",
    "<b>Not after alcohol.</b>",
    "<b>Talk to your doctor first</b> if you have a heart or blood pressure condition, are pregnant, or are unsure.",
    "<b>Decide your time before you get in,</b> and keep it short. Start with less than you think.",
    "<b>Ease in feet first.</b> Keep your head above the water.",
    "<b>Breathe out slowly.</b> The first minute is the hardest part.",
]
OUT = ["You go numb", "You shiver hard", "You cannot catch your breath", "You feel dizzy or light-headed", "Your chest hurts",
       "Your hands or legs stop doing what you want"]
AFTER = [
    "Get out slowly and hold on to something. Wet floors are slippery.",
    "Dry off and put on dry clothes or a robe.",
    "Warm up slowly. A warm drink helps.",
    "Sit down for a few minutes before you do anything else.",
]
FACTS = [
    ("The gasp", "Sudden cold makes you gasp and breathe fast. That alone raises the risk of drowning, even for strong swimmers."),
    ("The heart", "Heart rate and blood pressure jump in the first moments. That is a strain on the heart."),
    ("Not only ice", "Water does not have to be near freezing: 50–60 °F (10–15 °C) water can shock the body as much as 35 °F (2 °C) water."),
]

CSS = w2.CSS + """
.page{padding:.5in .58in .34in}
h1{font-size:68pt}
.grid{flex:1;display:grid;grid-template-columns:1.12fr 1fr;column-gap:.34in;margin-top:.17in;min-height:0}
.col{display:flex;flex-direction:column;row-gap:.14in;min-height:0}
.cl li{font-size:10.8pt;line-height:1.38;padding:.07in 0}
.out{border:2px solid var(--ink);border-radius:6px;background:#fffdf9;padding:.14in .2in .1in;flex:1;display:flex;flex-direction:column}
.out h2{font-weight:800;font-stretch:75%;font-size:24.5pt;line-height:.92;letter-spacing:-.015em;white-space:nowrap}
.out h2 i{font-style:normal;color:var(--ember)}
.out ul{margin-top:.09in;flex:1;display:flex;flex-direction:column}
.out li{flex:1;display:flex;align-items:center;font-family:var(--display);font-weight:700;font-size:15pt;line-height:1.15;letter-spacing:-.008em;border-top:1px solid var(--line-2);padding:.05in 0}
.out p{font-size:9.4pt;line-height:1.4;color:var(--ink);border-top:2px solid var(--ink);padding-top:.08in;margin-top:.02in}
.out p b{font-weight:700}
.facts{display:grid;grid-template-columns:repeat(3,1fr);column-gap:.3in;border-top:2px solid var(--ink);padding-top:.1in;margin-top:.15in;flex:none}
.facts b{display:block;font-family:var(--display);font-weight:700;font-size:12.5pt;line-height:1.15;letter-spacing:-.008em;margin-bottom:.03in}
.facts p{font-size:8.6pt;line-height:1.4;color:var(--ink-2)}
.fine{margin:.1in 0 .1in}
"""


def build():
    out = "".join(f"<li>{C.esc(x)}</li>" for x in OUT)
    facts = "".join(f"<div><b>{C.esc(t)}</b><p>{C.esc(x)}</p></div>" for t, x in FACTS)
    body = f"""<main class="page">
<span class="kicker">Cold plunge · post this by the tub</span>
<div class="head"><h1>Cold water rules<i>.</i></h1><p class="lead">Cold water is a shock to the body. Keep it short, keep it calm, and never do it alone.</p></div>
<div class="grid">
<div class="col">{w2.sec("Before you get in", "Every time", w2.checks(BEFORE), 4)}{w2.sec("After", "Warm up slowly", w2.checks([C.esc(x) for x in AFTER]), 3)}</div>
<div class="col"><div class="out"><h2>Get out right away if<i>:</i></h2><ul>{out}</ul>
<p><b>Chest pain, trouble breathing, confusion, or someone who cannot get out: call 911.</b></p></div></div>
</div>
<div class="facts">{facts}</div>
<p class="fine">General information, not medical advice. This card makes no claims about what cold water does for you; whether cold plunges have health benefits has not been established. Sources: U.S. National Weather Service, “Cold Water Hazards and Safety”, <a href="{NWS}">weather.gov/safety/coldwater</a>; American Heart Association News, “You’re not a polar bear: The plunge into cold water comes with risks” (2022), <a href="{AHA}">heart.org</a>.</p>
{C.foot()}
</main>"""
    C.write(os.path.join(C.ROOT, SLUG, SLUG + ".html"), C.doc(TITLE, DESC, KEYWORDS, CSS, body))
    meta = dict(title="Cold Plunge Safety Card (Printable)", subject=DESC, keywords=KEYWORDS)
    jobs = C.std_jobs(SLUG, SLUG + ".html", SLUG, meta)
    return dict(slug=SLUG, jobs=jobs, preview=dict(pdf=jobs[0]["pdf"]))
