"""1. Home Sauna Rules poster."""
import os
import common as C

SLUG = "home-sauna-rules-poster"
TITLE = "Home Sauna Rules Poster"
DESC = "A calm, printable poster of ten house rules for a home sauna: shower first, sit on a towel, ask before you pour, cool down and rest."
KEYWORDS = "home sauna rules, sauna house rules poster, sauna sign, sauna etiquette, printable sauna poster, sauna decor, DIVELUX"

RULES = [
    ("Shower first", "Come in rinsed and clean. The wood and the air stay fresh."),
    ("Sit on a towel", "A towel under you keeps the benches dry and clean."),
    ("Close the door fast", "In or out, quickly. The heat belongs inside."),
    ("Ask before you pour", "More steam reaches everyone at once. Check with the bench first."),
    ("Sit where it feels right", "The top bench is the hottest. Lower is always fine."),
    ("Step out any time", "Nobody is counting minutes. Leave as soon as you have had enough."),
    ("Cool down, then rest", "Fresh air, a cool rinse, a seat. Take your time before the next round."),
    ("Drink water", "Before, between rounds, and after. No alcohol in the heat."),
    ("Quiet is welcome", "Phones stay outside. Talk softly, or not at all."),
    ("Last one out airs it out", "Prop the door open and hang up the ladle so the room can dry."),
]

CSS = """
.page{padding:.58in .66in .34in}
.top{display:flex;justify-content:space-between;align-items:baseline}
.top .kicker{font-size:12.5pt}
.head{display:grid;grid-template-columns:1fr 2.55in;column-gap:.3in;align-items:end;margin-top:.14in}
h1{font-weight:800;font-stretch:75%;font-size:112pt;line-height:.83;letter-spacing:-.022em;margin:0 0 0 -.045in;white-space:nowrap}
.heat{display:grid;grid-template-rows:repeat(4,1fr);height:2.5in;border-left:2px solid var(--ink);margin-bottom:.06in}
.heat div{display:flex;flex-direction:column;justify-content:center;padding:0 .16in;border-top:1px solid rgba(27,21,18,.22)}
.heat div:first-child{border-top:0}
.heat b{font-family:var(--display);font-weight:700;font-size:13pt;line-height:1.1;letter-spacing:-.005em}
.heat span{font-size:8.6pt;line-height:1.3;color:var(--ink-2)}
.heat .a{background:var(--t1)}.heat .b{background:var(--t2)}.heat .c{background:var(--t3)}.heat .d{background:var(--t4)}
h1 i{font-style:normal;color:var(--ember)}
.lead{font-family:var(--display);font-weight:500;font-size:15.5pt;line-height:1.25;color:var(--ink-2);margin:.2in 0 .2in;max-width:5.6in}
.rules{display:grid;grid-template-columns:1fr 1fr;grid-template-rows:repeat(5,1fr);grid-auto-flow:column;column-gap:.42in;flex:1;
border-bottom:2px solid var(--ink)}
.rule{display:grid;grid-template-columns:.7in 1fr;align-content:center;border-top:1px solid var(--line-2);padding:.04in 0}
.rule:nth-child(1),.rule:nth-child(6){border-top:2px solid var(--ink)}
.rule .n{font-family:var(--display);font-weight:700;font-stretch:75%;font-size:39pt;line-height:.9;letter-spacing:-.02em;color:var(--ink)}
.rule h2{font-size:17.5pt;line-height:1.08;font-weight:700;letter-spacing:-.012em}
.rule p{font-size:10.4pt;line-height:1.38;color:var(--ink-2);margin-top:.05in;text-wrap:balance}
.end{display:flex;justify-content:space-between;align-items:flex-end;gap:.3in;margin:.17in 0 .17in}
.end .wish{font-family:var(--display);font-weight:700;font-size:21pt;line-height:1;letter-spacing:-.015em}
.end .aside{font-size:8.6pt;line-height:1.4;color:var(--muted);text-align:right;max-width:3.5in}
"""


def build():
    rules = "".join(
        f'<li class="rule"><span class="n num">{i:02d}</span><div><h2>{C.esc(t)}</h2><p>{C.esc(b)}</p></div></li>'
        for i, (t, b) in enumerate(RULES, 1))
    body = f"""<main class="page">
<div class="top"><span class="kicker">Home sauna</span></div>
<div class="head"><h1>House<br>rules<i>.</i></h1>
<div class="heat"><div class="a"><b>Under the ceiling</b><span>the hottest air</span></div><div class="b"><b>Top bench</b><span>hot</span></div><div class="c"><b>Lower bench</b><span>milder</span></div><div class="d"><b>Floor</b><span>the coolest air</span></div></div></div>
<p class="lead">Ten small habits that keep the heat good for everyone on the bench.</p>
<ol class="rules">{rules}</ol>
<div class="end"><p class="wish">Good steam to you.</p>
<p class="aside">Hats welcome: wool felt, worn dry. General information, not medical advice. If you feel dizzy or unwell, leave the heat.</p></div>
{C.foot()}
</main>"""
    C.write(os.path.join(C.ROOT, SLUG, SLUG + ".html"), C.doc(TITLE, DESC, KEYWORDS, CSS, body))
    meta = dict(title="Home Sauna Rules: A Printable House Rules Poster", subject=DESC, keywords=KEYWORDS)
    jobs = C.std_jobs(SLUG, SLUG + ".html", SLUG, meta)
    return dict(slug=SLUG, jobs=jobs, preview=dict(pdf=jobs[0]["pdf"]))
