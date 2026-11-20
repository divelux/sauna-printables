"""17. Wood stove lighting checklist for a wood-burning sauna stove.
Only steps that stove makers publish themselves (checked against Harvia's wood-burning stove manual, 2016 edition)
and general fire-safety practice. Model-specific numbers are left to the stove manual on purpose."""
import os
import common as C
import w2

SLUG = "wood-sauna-stove-lighting-checklist"
TITLE = "Wood Sauna Stove Lighting Checklist"
DESC = "A printable one-page checklist for lighting a wood-burning sauna stove: before you light, building the fire, while it burns and when you are done. Follow your stove manual."
KEYWORDS = "wood burning sauna stove, how to light a sauna stove, sauna stove checklist, wood fired sauna safety, top-down fire, sauna fire safety, printable checklist, DIVELUX"

BLOCKS = [
    ("Before you light", "Two minutes", 1, [
        "Read the stove manual once. Its wood amounts, air settings and safety distances beat any general list.",
        "Clear the area. Nothing that can burn on the stove or inside its safety distances: no towels, clothes or spare firewood.",
        "Empty the ash box, once the ashes are cold, into a metal container.",
        "Open the flue damper, if your chimney has one.",
        "Make sure the room’s fresh-air vent is open.",
        "Check that smoke and carbon monoxide alarms in the building work.",
    ]),
    ("Build and light the fire", "Top-down", 2, [
        "Use dry, split firewood. Dry pieces ring when you knock two together.",
        "Stack the wood loosely in the firebox, bigger pieces at the bottom, smaller on top. Leave gaps for air.",
        "Put kindling on top: birch bark, small sticks or plain newspaper. Light it from the top. It smokes less.",
        "Close the stove door. A sauna stove is not built to burn with the door open.",
        "Set the draft the way your manual says. Many stoves want the ash box slightly open until the fire catches.",
    ]),
    ("While it burns", "Stay nearby", 3, [
        "Add a few pieces when the fire has burned down to embers. A couple of logs usually holds the heat.",
        "Do not overfire. If the stove body starts to glow red, there is too much draft or too much wood.",
        "Handles get hot. Use the stove tool or a glove.",
        "Keep children away from the stove.",
        "Pour water on the stones only, never on the steel body.",
        "Never hang clothes or towels to dry over the stove.",
    ]),
    ("When you are done", "Until it is cold", 4, [
        "Let the fire burn out on its own.",
        "Leave the flue damper open until the embers are fully out. Closing it early can push carbon monoxide into the room.",
        "Take ashes out only when they are cold. They can hide live embers for days.",
        "Keep ashes in a metal container with a lid, outdoors, away from anything that can burn.",
        "Have the chimney and flue swept and inspected regularly by a professional.",
    ]),
]
ALWAYS = [
    ("The stove manual comes first", "Clearances, floor protection, chimney type and wood amounts are set by the maker and your local code. Follow the manufacturer’s manual."),
    ("Never burn", "Gasoline or any liquid fuel. Painted or treated wood, chipboard, plastic, trash, garden waste, coal. Only clean, dry firewood."),
    ("New stove?", "Most makers ask for a first firing outdoors or with full ventilation, without stones, to cure the paint. Check your manual before the first sauna."),
]

CSS = w2.CSS + """
.page{padding:.5in .58in .34in}
.blocks{flex:1;display:grid;grid-template-columns:1fr 1fr;grid-template-rows:auto auto;gap:.14in .34in;margin-top:.16in;min-height:0;align-content:space-between}
.always{margin-top:.14in}
.fine{margin:.1in 0 .1in}
"""


def build():
    blocks = "".join(w2.sec(t, s, w2.checks([C.esc(x) for x in items]), n) for t, s, n, items in BLOCKS)
    always = "".join(f"<div><b>{C.esc(t)}</b><p>{C.esc(x)}</p></div>" for t, x in ALWAYS)
    body = f"""<main class="page">
<span class="kicker">Wood-burning sauna stove</span>
<div class="head"><h1>Light the fire<i>.</i></h1><p class="lead">A calm routine for a wood-fired sauna, from the first match to cold ashes.</p></div>
<div class="blocks">{blocks}</div>
<div class="always">{always}</div>
<p class="fine">General guidance for wood-burning sauna stoves with a chimney, based on what stove makers publish in their manuals and on common fire-safety practice. Stoves, chimneys and local codes differ: follow the manufacturer’s manual. General information, not professional or medical advice.</p>
{C.foot()}
</main>"""
    C.write(os.path.join(C.ROOT, SLUG, SLUG + ".html"), C.doc(TITLE, DESC, KEYWORDS, CSS, body))
    meta = dict(title="Wood Sauna Stove Lighting Checklist (Printable)", subject=DESC, keywords=KEYWORDS)
    jobs = C.std_jobs(SLUG, SLUG + ".html", SLUG, meta)
    return dict(slug=SLUG, jobs=jobs, preview=dict(pdf=jobs[0]["pdf"]))
