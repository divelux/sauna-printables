"""10. Sauna Care and Cleaning schedule: one-page schedule plus a maintenance log page.
Only generally accepted upkeep advice; anything that depends on the product defers to the heater manual,
and anything electrical to a qualified electrician."""
import os
import common as C

SLUG = "sauna-care-cleaning-schedule"
TITLE = "Sauna Care and Cleaning Schedule"
DESC = "A printable cleaning and upkeep schedule for a home sauna: what to do after every session, every week, every month and once a year, plus a maintenance log page."
KEYWORDS = "sauna cleaning schedule, sauna maintenance checklist, how to clean a sauna, home sauna care, sauna upkeep, sauna stones check, printable checklist, DIVELUX"

BLOCKS = [
    ("After every session", "Five minutes", [
        "Prop the door and open the vent so the room can dry.",
        "Wipe sweat off the benches with a clean cloth and plain water.",
        "Empty the bucket and hang up the ladle.",
        "Take towels, seat covers and hats out to air dry.",
        "Lift floor mats or duckboards so the floor dries.",
        "Check that the heater is off and nothing is left on or near it.",
    ]),
    ("Every week", "Or every few sessions", [
        "Sweep or vacuum the floor, then mop it with a mild cleaner.",
        "Wash benches and backrests with warm water and a soft brush.",
        "Rinse the bucket and ladle and let them dry.",
        "Clean the glass door. Spray the cloth, not the wood.",
        "Wash seat towels and bench covers.",
    ]),
    ("Every month", "A slow look around", [
        "Look over the benches for stains and rough spots. Sand lightly with fine sandpaper.",
        "Check that the door opens and closes easily. Tighten loose hinges and handles.",
        "Clear dust from the air vents.",
        "Check the heater guard, benches and backrests for anything loose.",
        "Check the light, its cover and the thermometer.",
    ]),
    ("Once a year", "Before the cold season", [
        "Take the stones out, discard cracked or crumbling ones, rinse the rest and restack loosely. Stone type and timing: follow your heater manual.",
        "Have the wiring, controls and heating elements checked by a qualified electrician.",
        "Wood stove: have the chimney and flue swept and inspected by a professional. Follow your stove manual.",
        "Deep-clean the benches and sand worn spots. Treat wood only with products made for sauna interiors.",
        "Check the floor drain, the door seal and, outdoors, the roof and cladding.",
        "Test smoke and carbon monoxide alarms near the sauna.",
    ]),
]
ALWAYS = [
    ("No harsh chemicals on wood", "No bleach, no ammonia. Plain water, a mild sauna cleaner and a soft brush are enough."),
    ("Heater manual comes first", "Where this sheet and the manual differ, follow your heater manual. Water goes on the stones only if the heater is made for it."),
    ("Electrics: call a professional", "Any electrical inspection or repair is done by a qualified electrician."),
]

CSS = """
.page{padding:.5in .58in .34in}
.head{display:grid;grid-template-columns:auto 1fr;column-gap:.45in;align-items:end}
h1{font-weight:800;font-stretch:75%;font-size:82pt;line-height:.84;letter-spacing:-.022em;margin:.08in 0 0 -.04in;white-space:nowrap}
h1 i{font-style:normal;color:var(--ember)}
.lead{font-family:var(--display);font-weight:500;font-size:13.5pt;line-height:1.3;color:var(--ink-2);padding-bottom:.07in;text-wrap:balance}
.blocks{flex:1;display:grid;grid-template-columns:1fr 1fr;grid-template-rows:auto auto;gap:.14in .34in;margin-top:.16in;min-height:0;align-content:space-between}
.block{border-top:2px solid var(--ink);display:flex;flex-direction:column}
.block header{display:flex;justify-content:space-between;align-items:baseline;gap:.1in;padding:.07in .1in .06in;margin-bottom:.03in}
.block:nth-child(1) header{background:var(--t1)}.block:nth-child(2) header{background:var(--t2)}
.block:nth-child(3) header{background:var(--t3)}.block:nth-child(4) header{background:var(--t4)}
.block h2{font-weight:800;font-stretch:75%;font-size:22pt;line-height:1;letter-spacing:-.012em}
.block header span{font-size:8.2pt;color:var(--ink-2);white-space:nowrap}
.block li{display:grid;grid-template-columns:.25in 1fr;font-size:9.6pt;line-height:1.36;color:var(--ink-2);padding:.047in 0;border-bottom:1px solid var(--line)}
.block li:last-child{border-bottom:0}
.box{display:block;width:.14in;height:.14in;border:1.2px solid var(--ink-2);border-radius:2px;margin-top:.02in;background:#fffdf9}
.always{display:grid;grid-template-columns:repeat(3,1fr);column-gap:.3in;border-top:2px solid var(--ink);padding-top:.1in;margin-top:.14in;flex:none}
.always b{display:block;font-family:var(--display);font-weight:700;font-size:12.5pt;line-height:1.15;letter-spacing:-.008em;margin-bottom:.03in}
.always p{font-size:8.6pt;line-height:1.4;color:var(--ink-2)}
.fine{font-size:7.5pt;line-height:1.42;color:var(--muted);margin:.11in 0 .1in}
.ph{border-bottom:2px solid var(--ink);padding-bottom:.12in;display:flex;justify-content:space-between;align-items:flex-end;gap:.3in;flex:none}
.ph h2{font-weight:800;font-stretch:75%;font-size:42pt;line-height:.9;letter-spacing:-.018em}
.ph p{font-size:9pt;line-height:1.4;color:var(--muted);max-width:3.4in;text-align:right}
.year{display:grid;grid-template-columns:repeat(4,1fr);gap:.14in;margin:.16in 0 .16in;flex:none}
.year div{border:1px solid var(--ink-2);border-radius:6px;padding:.07in .1in .34in;font-size:8.4pt;line-height:1.3;color:var(--ink-2)}
.year b{display:block;font-family:var(--display);font-weight:700;font-size:10.5pt;color:var(--ink)}
table.log{width:100%;border-collapse:collapse;table-layout:fixed;flex:1;margin-bottom:.16in}
table.log th{font-weight:600;font-size:8pt;text-align:left;color:#fff;background:#2a1b13;padding:.07in .09in;line-height:1.15}
table.log td{border-bottom:1px solid var(--line-2);border-right:1px solid var(--line)}
table.log td:last-child{border-right:0}
table.log tbody tr:nth-child(even) td{background:#f8f5f0}
"""


def build():
    blocks = "".join(
        f'<section class="block"><header><h2>{t}</h2><span>{s}</span></header><ul>'
        + "".join(f'<li><i class="box"></i><span>{C.esc(x)}</span></li>' for x in items) + "</ul></section>"
        for t, s, items in BLOCKS)
    always = "".join(f"<div><b>{C.esc(t)}</b><p>{C.esc(x)}</p></div>" for t, x in ALWAYS)
    rows = "<tr><td></td><td></td><td></td><td></td></tr>" * 16
    body = f"""<main class="page">
<span class="kicker">Home sauna upkeep</span>
<div class="head"><h1>Sauna care<i>.</i></h1><p class="lead">A simple cleaning schedule. The small habits after each session do most of the work.</p></div>
<div class="blocks">{blocks}</div>
<div class="always">{always}</div>
<p class="fine">General upkeep guidance for stove-heated home saunas. Saunas, heaters and local codes differ: the instructions from your sauna and heater manufacturer always take priority.</p>
{C.foot()}
</main>
<main class="page white">
<header class="ph"><h2>Maintenance log</h2><p>Write down what was done and when. Next year you will be glad you did.</p></header>
<div class="year"><div><b>Stones restacked</b>Date</div><div><b>Electrician's check</b>Date</div><div><b>Chimney swept</b>Date, if wood-burning</div><div><b>Benches deep-cleaned</b>Date</div></div>
<table class="log"><colgroup><col style="width:15%"><col><col style="width:17%"><col style="width:17%"></colgroup>
<thead><tr><th>Date</th><th>What was done</th><th>Done by</th><th>Next due</th></tr></thead><tbody>{rows}</tbody></table>
{C.foot("Sauna Care and Cleaning Schedule · Maintenance log")}
</main>"""
    C.write(os.path.join(C.ROOT, SLUG, SLUG + ".html"), C.doc(TITLE, DESC, KEYWORDS, CSS, body))
    meta = dict(title="Sauna Care and Cleaning Schedule (Printable Checklist and Log)", subject=DESC, keywords=KEYWORDS)
    jobs = C.std_jobs(SLUG, SLUG + ".html", SLUG, meta)
    return dict(slug=SLUG, jobs=jobs, preview=dict(pdf=jobs[0]["pdf"]))
