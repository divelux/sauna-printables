"""19. Ready-made sauna buying checklist: questions for the seller plus a three-way comparison page.
Questions only; no claims about any product. Electrical work is deferred to a licensed electrician and
heater details to the manufacturer's manual."""
import os
import common as C
import w2

SLUG = "sauna-buying-checklist"
TITLE = "Sauna Buying Checklist"
DESC = "A printable checklist for buying a ready-made sauna: questions to ask the seller about size, wood, heater, power, delivery, warranty and the real price, plus a page to compare three models."
KEYWORDS = "sauna buying guide, questions to ask before buying a sauna, home sauna kit checklist, barrel sauna buying, sauna comparison worksheet, printable checklist, DIVELUX"

BLOCKS = [
    ("Size and fit", "Measure twice", 1, [
        "What are the outside size and the inside size of the hot room?",
        "How many adults can sit at once? Can one person lie down on the top bench?",
        "What is the ceiling height inside, and how high are the benches?",
        "Will the boxes or panels fit through my gate, door or stairs?",
        "Is it made for indoors, outdoors or both? What base does it need?",
    ]),
    ("Wood and build", "What it is made of", 2, [
        "Which wood are the walls and the benches made of?",
        "How thick are the walls? Are they insulated?",
        "Is the glass tempered, and how much glass is there?",
        "Where does fresh air come in and where does it go out?",
        "Are any glues, stains or finishes used inside the hot room?",
    ]),
    ("Heater and power", "Ask for the manual", 3, [
        "Which heater brand and model comes with it, and how many kW?",
        "Does the heater manual list this room volume, glass included?",
        "What voltage and breaker does it need? Is it hardwired on its own circuit?",
        "Which safety listing do the heater and controls carry?",
        "Can I pour water on the stones? What is the top temperature?",
    ]),
    ("Delivery and setup", "Plan ahead", 3, [
        "Is delivery curbside or to the spot? What does the heaviest piece weigh?",
        "How long does assembly take, with how many people and which tools?",
        "Can I read the assembly manual before I buy?",
        "Who connects the heater? Plan on a licensed electrician.",
        "What is the lead time from order to delivery?",
    ]),
    ("Warranty and support", "In writing", 4, [
        "How long is the warranty on the cabin, the heater, the controls and the glass?",
        "Who handles a claim: the seller or the maker? Where do parts ship from?",
        "What is the return policy? Who pays return freight?",
        "How long have you sold this model?",
        "Can I see one in person or talk to an owner?",
    ]),
    ("The real price", "Add it all up", 4, [
        "Does the price include heater, stones, controls, benches, door and lights?",
        "What do shipping, tax and liftgate service add?",
        "What will the electrician and any permit cost? Get your own quote.",
        "What do the base, the roof kit or weather cover add for outdoors?",
        "What else will I want: bucket, ladle, thermometer, sauna hats?",
    ]),
]
ROWS = ["Model", "Seller", "Price, delivered", "Outside size", "Inside size", "Seats", "Wood", "Heater model and kW", "Power it needs",
        "Warranty", "Lead time", "Electrician’s quote", "Other costs", "Total"]
PAY = ["I have read the heater manual and the assembly manual.", "A licensed electrician has seen the heater’s power needs and given a quote.",
       "I measured the spot and the way in.", "Warranty and return terms are in writing.",
       "I checked permit and HOA rules with the local building department."]

CSS = w2.CSS + """
.page{padding:.5in .58in .34in}
h1{font-size:70pt}
.blocks{flex:1;display:grid;grid-template-columns:1fr 1fr;grid-template-rows:repeat(3,auto);gap:.13in .34in;margin-top:.16in;min-height:0;align-content:space-between}
.cl li{font-size:9.2pt;padding:.043in 0}
.fine{margin:.1in 0 .1in}
.page.white{padding:.55in .6in .34in .8in}
.body{flex:1;display:flex;flex-direction:column;min-height:0;padding:.16in 0 .16in}
table.cmp{flex:1}
table.cmp td:first-child{color:var(--ink);font-size:9pt;font-weight:600;background:var(--paper)!important}
table.cmp tr:last-child td{border-top:2px solid var(--ink);border-bottom:0}
.lab{font-family:var(--display);font-weight:700;font-size:13pt;margin:.18in 0 .03in}
"""


def build():
    blocks = "".join(w2.sec(t, s, w2.checks([C.esc(x) for x in items]), n) for t, s, n, items in BLOCKS)
    rows = "".join(f"<tr><td>{C.esc(r)}</td><td></td><td></td><td></td></tr>" for r in ROWS)
    body = f"""<main class="page">
<span class="kicker">Ready-made sauna · questions for the seller</span>
<div class="head"><h1>Buying a sauna<i>.</i></h1><p class="lead">Thirty questions to ask before you pay for a sauna kit, cabin or barrel.</p></div>
<div class="blocks">{blocks}</div>
<p class="fine">A list of questions, not a product recommendation. Heater sizing, clearances and wiring are decided by the heater manufacturer’s manual and your local code; electrical work is a job for a licensed electrician.</p>
{C.foot()}
</main>
<main class="page white">
{w2.ph("Compare three", "One column per model. Fill it in as the answers come back.")}
<div class="body">
<table class="log cmp"><colgroup><col style="width:25%"><col><col><col></colgroup>
<thead><tr><th></th><th>Option A</th><th>Option B</th><th>Option C</th></tr></thead><tbody>{rows}</tbody></table>
<p class="lab">Before you pay</p>
{w2.checks([C.esc(x) for x in PAY])}
</div>
{C.foot("Sauna Buying Checklist · Compare three")}
</main>"""
    C.write(os.path.join(C.ROOT, SLUG, SLUG + ".html"), C.doc(TITLE, DESC, KEYWORDS, CSS, body))
    meta = dict(title="Sauna Buying Checklist: Questions to Ask the Seller (Printable)", subject=DESC, keywords=KEYWORDS)
    jobs = C.std_jobs(SLUG, SLUG + ".html", SLUG, meta)
    return dict(slug=SLUG, jobs=jobs, preview=dict(pdf=jobs[0]["pdf"], pages=[1, 2], dpi=75))
