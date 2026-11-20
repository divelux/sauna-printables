"""14. Sauna party invitations: three designs, four cards per sheet (3.9 x 5 in, fits an A2 envelope),
plus a sheet with an open writing space instead of labeled fields."""
import os
import common as C
import w2
import art

SLUG = "sauna-party-invitations"
TITLE = "Sauna Party Invitations"
DESC = "Printable sauna party invitations: three designs with fill-in lines for when, where and RSVP, plus an open version for your own words. Four cards per sheet."
KEYWORDS = "sauna party invitation, sauna night invite printable, sauna birthday invitation, spa party invitation, printable invitations, fill in invitation, DIVELUX"

CSS = w2.CSS + """
.page{padding:.16in .2in .26in;background:#fff}
.how{padding:0 .15in .05in;white-space:nowrap}
.foot{margin-left:.15in;margin-right:.15in}
.cards{flex:1;display:grid;grid-template-columns:3.9in 3.9in;grid-template-rows:5in 5in;justify-content:center;align-content:center;min-height:0}
.inv{outline:1px dashed #8d8378;background:var(--paper);display:flex;flex-direction:column;min-width:0;overflow:hidden;position:relative}
.inv .in{flex:1;display:flex;flex-direction:column;padding:.26in .3in .12in;min-height:0}
.inv .k{font-size:6.6pt;letter-spacing:.18em;text-transform:uppercase;font-weight:600;color:var(--ink-2)}
.inv h1,.inv .h1{font-family:var(--display);font-weight:800;font-stretch:75%;letter-spacing:-.02em;white-space:normal;margin:0}
.inv .sub{font-family:var(--display);font-weight:500;font-size:11.5pt;line-height:1.28;color:var(--ink-2)}
.inv .fields{margin-top:auto}
.inv .field{margin-top:.03in}
.inv .field{height:.39in;font-size:8.6pt}
.inv .hint{font-size:7pt;line-height:1.35;color:var(--muted);margin-top:.09in}
.inv .cfoot{margin-top:.08in;padding-top:.045in;border-top:1px solid var(--line-2);font-size:5pt;line-height:1.25;color:var(--muted);white-space:nowrap}
.inv .cfoot a{color:var(--ink);text-decoration:none;font-weight:600}
.inv .cfoot b{color:var(--ink);font-weight:600}
.inv .lines i{max-height:.4in}
/* A: type only */
.a h1,.a .h1{font-size:78pt;line-height:.83;margin:.2in 0 .14in -.03in}
.a .ladder{height:.12in;margin-bottom:.15in}
/* B: cabin */
.b .art{background:var(--t4);border-bottom:2px solid var(--ink);height:1.78in;display:flex;justify-content:center;align-items:flex-end;flex:none}
.b .art svg{height:1.62in;display:block}
.b .in{padding-top:.17in}
.b h1,.b .h1{font-size:40pt;line-height:.88;margin:.08in 0 .09in -.015in}
/* C: bucket */
.c{display:grid;grid-template-columns:1.12in minmax(0,1fr)}
.c .side{background:var(--t2);border-right:2px solid var(--ink);display:flex;flex-direction:column;align-items:center;justify-content:center}
.c .side svg{width:.98in;display:block}
.c .in{padding-left:.22in;padding-right:.24in}
.c h1,.c .h1{font-size:48pt;line-height:.85;margin:.16in 0 .12in -.02in}
/* open version */
.o h1,.o .h1{font-size:56pt;line-height:.84;margin:.18in 0 .12in -.02in}
.o .ladder{height:.08in;margin-bottom:.06in}
"""

HINT = "Bring a towel to sit on, a water bottle and flip-flops. Hats welcome."


def fields(names):
    return '<div class="fields">' + "".join(w2.field(n) for n in names) + "</div>"


def card_a(tag):
    return f"""<div class="inv a"><div class="in"><span class="k">You are invited</span>
<{tag} class="h1">Sauna night<i>.</i></{tag}>
<div class="ladder"><i></i><i></i><i></i><i></i></div>
<p class="sub">An evening of heat, steam and good company.</p>
{fields(["When", "Where", "RSVP"])}
<p class="hint">{HINT}</p>{w2.cfoot()}</div></div>"""


def cabin_svg():
    b = (art.ln("M6 372H474") + art.pine(46, 372, 190, 84) + art.pine(436, 372, 236, 104) + art.cabin(92, 90, .78)
         + '<circle cx="62" cy="62" r="26"/>')
    return art.svg(480, 380, b, 3.4)


def card_b():
    return f"""<div class="inv b"><div class="art">{cabin_svg()}</div><div class="in"><span class="k">You are invited</span>
<div class="h1">Come get warm<i>.</i></div>
<p class="sub">The sauna is on. Stay for the cool-down.</p>
{fields(["When", "Where", "RSVP"])}
<p class="hint">{HINT}</p>{w2.cfoot()}</div></div>"""


def bucket_svg():
    b = art.steam(95, -62, 80, 12) + art.steam(150, -74, 80, 12) + art.steam(205, -62, 80, 12) + art.bucket(0, 0, 1.0)
    return art.svg(390, 500, b, 9, extra=' style="overflow:visible"').replace('viewBox="0 0 390 500"', 'viewBox="-22 -160 390 500"')


def card_c():
    return f"""<div class="inv c"><div class="side">{bucket_svg()}</div><div class="in"><span class="k">You are invited</span>
<div class="h1">Steam &amp; friends<i>.</i></div>
<p class="sub">Sauna, cold drinks and a long sit on the bench.</p>
{fields(["When", "Where", "Bring", "RSVP"])}
<div class="cfoot"><b>DIVELUX</b> wool sauna hats — <a href="{C.SITE}">diveluxsaunahat.com</a></div></div></div>"""


def card_o():
    return f"""<div class="inv o"><div class="in"><span class="k">You are invited</span>
<div class="h1">Sauna party<i>.</i></div>
<div class="ladder"><i></i><i></i><i></i><i></i></div>
{w2.lines(8)}
{w2.cfoot()}</div></div>"""


def sheet(name, cards, note="Print at 100% on heavy paper. Cut along the dashed lines. 3.9 × 5 in, fits an A2 envelope."):
    return f"""<main class="page">
<div class="how"><span><b>Sauna party invitations</b> · {name}</span><span>{note}</span></div>
<div class="cards">{cards}</div>
{C.foot()}
</main>"""


def build():
    body = (sheet("design 1", card_a("h1") + card_a("div") * 3) + sheet("design 2", card_b() * 4)
            + sheet("design 3", card_c() * 4) + sheet("open version", card_o() * 4))
    C.write(os.path.join(C.ROOT, SLUG, SLUG + ".html"), C.doc(TITLE, DESC, KEYWORDS, CSS, body))
    meta = dict(title="Sauna Party Invitations (Printable, 4 per Sheet)", subject=DESC, keywords=KEYWORDS)
    jobs = C.std_jobs(SLUG, SLUG + ".html", SLUG, meta)
    return dict(slug=SLUG, jobs=jobs, preview=dict(pdf=jobs[0]["pdf"], pages=[1, 2, 3], dpi=75))
