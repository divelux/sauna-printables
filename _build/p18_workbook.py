"""18. Home Sauna Planning Workbook: seven pages. Cover, big picture, the room, heater size worksheet,
budget, questions to ask, timeline. The heater sizing rule and its caveats are the ones documented with sources
in ../tools/sauna-heater-calculator/README.md (Harvia and HUUM guidance); nothing else is asserted about power."""
import os
import common as C
import w2

SLUG = "home-sauna-planning-workbook"
TITLE = "Home Sauna Planning Workbook"
DESC = "A printable workbook for planning a home sauna: goals, room size and site checks, a heater size worksheet, a budget table, questions for a licensed electrician and a contractor, and a timeline. Seven pages."
KEYWORDS = "home sauna planning, sauna build planner, sauna heater size worksheet, sauna budget worksheet, questions for electrician sauna, DIY sauna checklist, printable workbook, DIVELUX"
CALC = "https://divelux.github.io/sauna-heater-calculator/"

BUDGET = ["Design, permits and inspection fees", "Base, floor and drainage", "Framing, walls and roof", "Insulation and foil vapor barrier",
          "Interior wood: walls and ceiling", "Benches and backrests", "Door and glass", "Heater or stove, stones, guard",
          "Controls, sensors and wiring materials", "Licensed electrician: labor", "Chimney and flue (wood stove)", "Ventilation",
          "Lighting", "Ready-made kit or cabin, with delivery", "Tools and hardware", "Accessories: bucket, ladle, thermometer, hats", ""]
Q_ELEC = [
    "Can my panel take this heater, or does it need an upgrade?",
    "What voltage, breaker and wire size does the heater manual call for at my wire run?",
    "Does the heater need its own dedicated circuit and a disconnect?",
    "Where will the control panel and the temperature sensor go?",
    "Is a permit or an inspection required where I live? Who pulls it?",
    "Outdoor sauna: how will power get there, and how deep is the trench?",
    "What will the full job cost, permit included, and how long will it take?",
    "Will you connect and test the heater according to the manufacturer’s manual?",
]
Q_BUILD = [
    "Have you built or installed a sauna before? Can I see one?",
    "Which wood for walls and benches, and what goes behind it (insulation, foil vapor barrier)?",
    "Where does fresh air come in and go out, and does that match the heater manual?",
    "How are the heater’s safety distances to walls, benches and ceiling kept?",
    "What base or floor does it need, and where does water go?",
    "What is in the price, and what is not (electrical, heater, delivery, permits)?",
    "What is the warranty on the work, the wood and the heater?",
    "What is the schedule, and what could delay it?",
]
STEPS = ["Settle on the place and the type of sauna", "Measure the room and sketch the layout", "Work out the heater size and pick a model",
         "Read the heater manual: clearances, vents, power", "Get a quote from a licensed electrician", "Check permit rules with the local building department",
         "Get quotes for the build or the kit", "Order heater, wood or kit", "Build or assemble", "Electrical hookup by a licensed electrician",
         "First heating, the way the manual says", "First real sauna"]

CSS = w2.CSS + """
.page{padding:.55in .6in .34in .8in}
.cover{padding-right:3.05in}
.cover .band{position:absolute;right:0;top:0;bottom:0;width:2.55in;display:grid;grid-template-rows:repeat(4,1fr);border-left:2px solid var(--ink)}
.cover .band i{display:flex;align-items:flex-end;padding:.16in .2in;border-top:1px solid rgba(27,21,18,.22);font-style:normal;font-family:var(--display);font-weight:700;font-size:13pt;line-height:1.15}
.cover .band i:first-child{border-top:0}
.cover .band i:nth-child(1){background:var(--t1)}.cover .band i:nth-child(2){background:var(--t2)}
.cover .band i:nth-child(3){background:var(--t3)}.cover .band i:nth-child(4){background:var(--t4)}
.cover .logo{width:1.45in;display:block}
.cover h1{font-size:104pt;line-height:.83;margin:1.2in 0 0 -.045in;white-space:normal}
.cover h1 small{display:block;font-family:var(--display);font-stretch:100%;font-weight:600;font-size:14pt;line-height:1.2;letter-spacing:.01em;color:var(--ink-2);margin:0 0 .16in .04in}
.cover .sub{font-family:var(--display);font-weight:500;font-size:16pt;line-height:1.28;color:var(--ink-2);margin-top:.3in;max-width:3.9in}
.cover .fields{margin-top:auto;margin-bottom:.5in}
.cover .field{height:.44in;font-size:10pt}
.body{flex:1;display:flex;flex-direction:column;min-height:0;padding:.16in 0 .16in}
.grid2{display:grid;grid-template-columns:1fr 1fr;column-gap:.35in}
.lab{font-family:var(--display);font-weight:700;font-size:13pt;margin:.2in 0 .03in}
.lab:first-child{margin-top:0}
.opts{display:flex;flex-wrap:wrap;gap:.07in .24in;font-size:9.4pt;color:var(--ink-2);padding:.05in 0}
.opts span{display:inline-flex;align-items:center;gap:.06in;white-space:nowrap}
.lines i{max-height:.36in}
.free .lines i{max-height:none}
.tip{background:var(--paper);border-radius:6px;padding:.14in .2in;font-size:9.2pt;line-height:1.5;color:var(--ink-2)}
.tip b{font-family:var(--display);font-weight:700;font-size:12pt;color:var(--ink);display:block;margin-bottom:.03in}
.tip a{color:var(--ink);font-weight:600}
.dims{display:grid;grid-template-columns:repeat(4,1fr);column-gap:.2in}
.sketch{flex:1;min-height:1.6in;border:1px solid var(--ink-2);border-radius:6px;margin-top:.06in;
background-image:linear-gradient(#e6dfd4 1px,transparent 1px),linear-gradient(90deg,#e6dfd4 1px,transparent 1px);background-size:.25in .25in;background-position:-1px -1px}
.cl li{font-size:9.2pt;padding:.04in 0}
.calc{counter-reset:c;display:flex;flex-direction:column}
.step{counter-increment:c;display:grid;grid-template-columns:.42in 1fr 2.55in;column-gap:.1in;align-items:center;border-top:1px solid var(--line-2);padding:.15in 0}
.step:first-child{border-top:2px solid var(--ink)}
.step::before{content:counter(c);font-family:var(--display);font-weight:700;font-stretch:75%;font-size:30pt;line-height:.9}
.step b{display:block;font-family:var(--display);font-weight:700;font-size:14pt;line-height:1.15;letter-spacing:-.008em}
.step p{font-size:9.4pt;line-height:1.42;color:var(--ink-2);margin-top:.03in}
.fx{display:flex;align-items:center;gap:.05in;font-size:8.6pt;color:var(--ink-2);justify-content:flex-end;white-space:nowrap}
.fx u{display:inline-block;text-decoration:none;border:1px solid var(--ink-2);border-radius:4px;background:#fff;width:.56in;height:.36in}
.fx u.w{width:.72in;border-width:1.6px}
.ex{display:grid;grid-template-columns:1fr 1fr;column-gap:.3in;margin-top:.2in}
.ex .tip{font-size:9.6pt}
table.bud{flex:1}
table.bud td{height:.33in}
table.bud td:first-child{color:var(--ink);font-size:9pt}
table.bud tfoot td{border-top:2px solid var(--ink);border-bottom:0;font-family:var(--display);font-weight:700;font-size:12pt;color:var(--ink);height:.42in;background:var(--paper)}
.q{border-top:2px solid var(--ink);padding-top:.07in}
.q b.t{display:block;font-family:var(--display);font-weight:700;font-size:15pt;line-height:1.15;letter-spacing:-.01em;margin-bottom:.02in}
.q{display:flex;flex-direction:column}
.q .cl{flex:1;display:flex;flex-direction:column}
.q .cl li{font-size:9.4pt;line-height:1.38;padding:.06in 0 .2in;flex:1;align-content:start}
table.tl{flex:none}
table.tl td{height:.3in}
table.tl td:first-child{text-align:center;color:var(--muted);font-family:var(--display);font-weight:700}
table.tl td:nth-child(2){color:var(--ink);font-size:9pt}
"""


def opts(items):
    return '<div class="opts">' + "".join(f'<span><i class="box"></i>{x}</span>' for x in items) + "</div>"


def fx(*parts):
    """A fill-in formula: strings are printed, '_' is an empty box, '#' is the wide result box."""
    out = []
    for p in parts:
        out.append("<u></u>" if p == "_" else '<u class="w"></u>' if p == "#" else f"<span>{p}</span>")
    return '<div class="fx">' + "".join(out) + "</div>"


def build():
    logo = C.logo_data_uri()
    bud = "".join(f"<tr><td>{C.esc(x)}</td><td></td><td></td><td></td><td></td></tr>" for x in BUDGET)
    tl = "".join(f'<tr><td>{i}</td><td>{C.esc(x)}</td><td></td><td></td><td></td></tr>' for i, x in enumerate(STEPS, 1))
    body = f"""<main class="page cover">
<div class="band" data-bleed><i>Place</i><i>Size</i><i>Heat</i><i>Budget</i></div>
<img class="logo" src="{logo}" alt="DIVELUX">
<h1><small>Planning workbook</small>Plan your home sauna<i>.</i></h1>
<p class="sub">Seven pages to fill in before you buy wood, a heater or a kit.</p>
<div class="fields">{w2.field("Project")}{w2.field("Started")}</div>
{C.foot()}
</main>
<main class="page white">
{w2.ph("The big picture", "Decide what you want before you price anything. Pencil is fine.")}
<div class="body">
<p class="lab">Who and how often</p>
<div class="grid2"><div>{w2.field("Who will use it")}{w2.field("People at one time")}</div><div>{w2.field("Sessions per week")}{w2.field("Target date")}</div></div>
<p class="lab">Where</p>
{opts(["Basement", "Bathroom", "Garage", "Spare room", "Backyard cabin", "Barrel sauna", "Deck or patio", "Other"])}
<p class="lab">Heat</p>
{opts(["Electric heater with stones", "Wood-burning stove", "Infrared cabin", "Not sure yet"])}
<p class="lab">Route</p>
{opts(["Ready-made kit or cabin", "Built by a contractor", "Build it myself", "A mix"])}
<div class="grid2 free" style="flex:1;min-height:0;margin-top:.2in">
<div style="display:flex;flex-direction:column;min-height:0"><p class="lab">Must have</p>{w2.lines(9)}</div>
<div style="display:flex;flex-direction:column;min-height:0"><p class="lab">Nice to have</p>{w2.lines(9)}</div></div>
<div class="grid2" style="margin-top:.16in"><div>{w2.field("Budget ceiling")}</div><div>{w2.field("Money already set aside")}</div></div>
</div>
{C.foot("Home Sauna Planning Workbook · The big picture")}
</main>
<main class="page white">
{w2.ph("The room", "Measure the inside of the hot room. You will need these numbers on the next page.")}
<div class="body">
<p class="lab">Inside size</p>
<div class="dims">{w2.field("Length")}{w2.field("Width")}{w2.field("Ceiling height")}{w2.field("Door size")}</div>
<div class="dims">{w2.field("Glass area")}{w2.field("Bare stone, tile or concrete")}{w2.field("Bench length")}{w2.field("Bench heights")}</div>
{opts(["Walls are bare log", "Walls are insulated and paneled", "Feet and inches", "Meters"])}
<p class="lab">Site checks</p>
<div class="grid2">{w2.checks(["The floor can take water, and I know where the water goes.", "There is a path for fresh air in and used air out, as the heater manual shows.", "The heater’s safety distances to walls, benches and ceiling fit this room.", "The door opens outward and has no lock."])}
{w2.checks(["A licensed electrician has looked at the power supply for this spot.", "Outdoors: the base is level and firm.", "Outdoors: I checked setbacks, permits and any HOA rules with the local building department.", "There is a place nearby to cool down and to hang towels and hats."])}</div>
<p class="lab">Sketch <span style="font:400 8.4pt var(--body);color:var(--muted)">one square = ______</span></p>
<div class="sketch"></div>
</div>
{C.foot("Home Sauna Planning Workbook · The room")}
</main>
<main class="page white">
{w2.ph("Heater size", "The rule of thumb heater makers publish, as a worksheet. Feet and cubic feet throughout.")}
<div class="body">
<div class="calc">
<div class="step"><div><b>Room volume</b><p>Length × width × ceiling height, inside the hot room.</p></div>{fx("_", "×", "_", "×", "_", "=", "#", "cu ft")}</div>
<div class="step"><div><b>Bare log walls?</b><p>If the inside walls are bare log, multiply by 1.5. If not, copy the number.</p></div>{fx("_", "× 1.5 or × 1", "=", "#", "cu ft")}</div>
<div class="step"><div><b>Cold surfaces</b><p>Glass, stone, tile, brick or concrete with no insulation behind it. Each sq ft counts as 3.9 cu ft of extra room.</p></div>{fx("_", "sq ft × 3.9", "=", "#", "cu ft")}</div>
<div class="step"><div><b>Calculated volume</b><p>Step 2 plus step 3. This is the number you shop by.</p></div>{fx("_", "+", "_", "=", "#", "cu ft")}</div>
<div class="step"><div><b>Electric heater: power range</b><p>Low end: calculated volume ÷ 50. High end: calculated volume ÷ 35.3 (1 kW per cubic meter).</p></div>{fx("#", "to", "#", "kW")}</div>
<div class="step"><div><b>Wood-burning stove</b><p>Stoves are sold by the room volume they suit. Calculated volume ÷ 35.3 gives cubic meters.</p></div>{fx("#", "m³")}</div>
</div>
<div class="ex">
<div class="tip"><b>Worked example</b>A 6 × 5 ft room with a 7 ft ceiling is 210 cu ft. Paneled walls, so it stays 210. A glass door of 12 sq ft adds 12 × 3.9 = 47 cu ft. Calculated volume: 257 cu ft (7.3 m³). Electric heater: about 5.1 to 7.3 kW.</div>
<div class="tip"><b>Then check the model</b>Every heater model lists the room volume range it is made for. Pick one whose range has your calculated volume near the middle. The online calculator does the same sums in feet or meters: <a href="{CALC}">divelux.github.io/sauna-heater-calculator</a></div>
</div>
<div class="tip" style="margin-top:.2in;background:var(--t4);font-size:9.6pt"><b>Always confirm with the heater manufacturer and a licensed electrician</b>This is a rule-of-thumb estimate. It cannot see your insulation, vents, climate or wiring. The manual of the heater you buy has the final say on room volume, clearances, breaker and wire size: follow the manufacturer’s manual. Infrared cabins are sized differently and are not covered here.</div>
<p class="fine" style="margin-top:auto;padding-top:.1in">Where the numbers come from: Harvia counts 1.2 m³ of extra volume per m² of uninsulated glass or stone (3.9 cu ft per sq ft) and multiplies by 1.5 for bare log walls. Harvia and HUUM both size at 1 kW per calculated m³; “1 kW per 50 cu ft” is the common North American shortcut and matches Harvia’s own minimum-output example. Sources are listed with the calculator.</p>
</div>
{C.foot("Home Sauna Planning Workbook · Heater size")}
</main>
<main class="page white">
{w2.ph("Budget", "Write an estimate first, then real quotes, then what you paid.")}
<div class="body">
<table class="log bud"><colgroup><col><col style="width:14%"><col style="width:14%"><col style="width:14%"><col style="width:19%"></colgroup>
<thead><tr><th>Item</th><th>My estimate</th><th>Quote</th><th>Paid</th><th>Notes</th></tr></thead><tbody>{bud}</tbody>
<tfoot><tr><td>Total</td><td></td><td></td><td></td><td></td></tr></tfoot></table>
<div class="grid2" style="margin-top:.12in"><div>{w2.field("Cushion for surprises")}</div><div>{w2.field("Total with cushion")}</div></div>
</div>
{C.foot("Home Sauna Planning Workbook · Budget")}
</main>
<main class="page white">
{w2.ph("Questions to ask", "Take this page to the meeting. Tick each question once you have an answer in writing.")}
<div class="body">
<div class="grid2" style="flex:1">
<div class="q"><b class="t">A licensed electrician</b>{w2.checks([C.esc(x) for x in Q_ELEC])}</div>
<div class="q"><b class="t">A contractor or kit seller</b>{w2.checks([C.esc(x) for x in Q_BUILD])}</div>
</div>
<div class="tip" style="margin-top:.1in"><b>Two rules that save trouble</b>All electrical work on a sauna heater is a job for a licensed electrician. And the heater’s own manual decides clearances, vents and wiring, so ask for the manual before you sign anything.</div>
</div>
{C.foot("Home Sauna Planning Workbook · Questions to ask")}
</main>
<main class="page white">
{w2.ph("Timeline", "A usual order of work. Cross out what does not apply and add your own dates.")}
<div class="body">
<table class="log tl"><colgroup><col style="width:6%"><col><col style="width:15%"><col style="width:15%"><col style="width:9%"></colgroup>
<thead><tr><th></th><th>Step</th><th>Planned</th><th>Done</th><th>OK</th></tr></thead><tbody>{tl}</tbody></table>
<p class="lab">Decisions and notes</p>
<div class="free" style="flex:1;display:flex;flex-direction:column;min-height:0">{w2.lines(10)}</div>
</div>
{C.foot("Home Sauna Planning Workbook · Timeline")}
</main>"""
    C.write(os.path.join(C.ROOT, SLUG, SLUG + ".html"), C.doc(TITLE, DESC, KEYWORDS, CSS, body))
    meta = dict(title="Home Sauna Planning Workbook (Printable, 7 Pages)", subject=DESC, keywords=KEYWORDS)
    jobs = C.std_jobs(SLUG, SLUG + ".html", SLUG, meta)
    return dict(slug=SLUG, jobs=jobs, preview=dict(pdf=jobs[0]["pdf"], pages=[1, 4, 5], dpi=75))
