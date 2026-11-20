"""6. Home Sauna Guest Book: cover plus six inside pages. Print the log pages as many times as needed."""
import os
import common as C

SLUG = "home-sauna-guest-book"
TITLE = "Home Sauna Guest Book"
DESC = "A printable guest book for a home sauna: cover, visit log with date, guests, temperature and notes, guest entry pages, sauna records and a regulars tally. Seven pages."
KEYWORDS = "sauna guest book, home sauna logbook, sauna visitor book printable, sauna journal pages, sauna log template, cabin guest book, DIVELUX"

CSS = """
.page{padding:.55in .6in .34in .8in}
.cover{padding-right:3.05in}
.cover .band{position:absolute;right:0;top:0;bottom:0;width:2.55in;display:grid;grid-template-rows:repeat(4,1fr);border-left:2px solid var(--ink)}
.cover .band i{display:block;border-top:1px solid rgba(27,21,18,.22)}
.cover .band i:first-child{border-top:0}
.cover .band i:nth-child(1){background:var(--t1)}.cover .band i:nth-child(2){background:var(--t2)}
.cover .band i:nth-child(3){background:var(--t3)}.cover .band i:nth-child(4){background:var(--t4)}
.cover .logo{width:1.45in;display:block}
h1{font-weight:800;font-stretch:75%;font-size:118pt;line-height:.83;letter-spacing:-.022em;margin:1.35in 0 0 -.045in}
h1 small{display:block;font-family:var(--display);font-stretch:100%;font-weight:600;font-size:14pt;line-height:1.2;letter-spacing:.01em;color:var(--ink-2);margin:0 0 .16in .04in}
h1 i{font-style:normal;color:var(--ember)}
.cover .sub{font-family:var(--display);font-weight:500;font-size:16pt;line-height:1.28;color:var(--ink-2);margin-top:.3in;max-width:3.9in}
.cover .fields{margin-top:auto;margin-bottom:.5in}
.field{display:flex;align-items:flex-end;gap:.1in;font-size:10pt;color:var(--ink-2);height:.44in}
.field span{white-space:nowrap;padding-bottom:.03in}
.field i{flex:1;border-bottom:1px solid var(--ink-2);display:block;height:100%}
.ph{border-bottom:2px solid var(--ink);padding-bottom:.12in;display:flex;justify-content:space-between;align-items:flex-end;gap:.3in;flex:none}
.ph h2{font-weight:800;font-stretch:75%;font-size:42pt;line-height:.9;letter-spacing:-.018em;white-space:nowrap}
.ph p{font-size:9pt;line-height:1.4;color:var(--muted);max-width:2.9in;text-align:right}
.body{flex:1;display:flex;flex-direction:column;min-height:0;padding:.14in 0 .16in}
.grid2{display:grid;grid-template-columns:1fr 1fr;column-gap:.35in}
.checks{display:flex;gap:.22in;align-items:center;font-size:10pt;color:var(--ink-2);height:.44in}
.checks b{font-weight:400}
.box{display:inline-block;width:.15in;height:.15in;border:1.2px solid var(--ink-2);border-radius:2px;margin-right:.06in;vertical-align:-.025in}
.lab{font-family:var(--display);font-weight:700;font-size:13pt;margin:.24in 0 .02in}
.rule-lines{flex:1;display:flex;flex-direction:column;min-height:0}
.rule-lines i{flex:1;border-bottom:1px solid var(--line-2);display:block;max-height:.42in}
.tip{background:var(--paper);border-radius:6px;padding:.16in .2in;font-size:9.6pt;line-height:1.5;color:var(--ink-2);margin-top:.22in}
.tip b{font-family:var(--display);font-weight:700;font-size:12pt;color:var(--ink);display:block;margin-bottom:.03in}
table.log{width:100%;border-collapse:collapse;table-layout:fixed;flex:1}
table.log th{font-weight:600;font-size:8pt;text-align:left;color:#fff;background:#2a1b13;padding:.07in .09in;line-height:1.15}
table.log th small{display:block;font-weight:400;font-size:6.8pt;opacity:.85}
table.log td{border-bottom:1px solid var(--line-2);border-right:1px solid var(--line)}
table.log td:last-child{border-right:0}
table.log tbody tr:nth-child(even) td{background:#f8f5f0}
.entries{flex:1;display:grid;grid-template-rows:repeat(4,1fr);row-gap:.16in;min-height:0}
.entry{border:1px solid var(--ink-2);border-radius:6px;padding:.1in .18in .16in;display:flex;flex-direction:column}
.entry .row{display:grid;grid-template-columns:1.25fr 2.6fr 1fr;column-gap:.2in}
.entry .field{height:.36in;font-size:8.6pt}
.entry .rule-lines i{max-height:none}
.records{flex:1;display:grid;grid-template-columns:1fr 1fr;grid-template-rows:repeat(4,1fr);gap:.16in .3in;min-height:0}
.rec{border-top:2px solid var(--ink);padding-top:.08in;display:flex;flex-direction:column}
.rec b{font-family:var(--display);font-weight:700;font-size:14.5pt;line-height:1.15;letter-spacing:-.01em}
.rec .field{font-size:8.6pt;height:.5in}
table.reg{width:100%;border-collapse:collapse;flex:1;table-layout:fixed}
table.reg td{border-bottom:1px solid var(--line-2);vertical-align:bottom;padding-bottom:.07in}
table.reg td.ticks{text-align:right;white-space:nowrap}
table.reg .box{margin:0 0 0 .055in;width:.14in;height:.14in}
table.reg .box:nth-child(5n+1){margin-left:.14in}
table.reg th{font-weight:600;font-size:8pt;text-align:left;color:var(--ink-2);border-bottom:1px solid var(--ink);padding-bottom:.05in}
table.reg th:last-child{text-align:right}
"""


def field(label, cls=""):
    return f'<div class="field {cls}"><span>{label}</span><i></i></div>'


def lines(n):
    return '<div class="rule-lines">' + "<i></i>" * n + "</div>"


def ph(title, text):
    return f'<header class="ph"><h2>{title}</h2><p>{text}</p></header>'


def build():
    logo = C.logo_data_uri()
    note = "Home Sauna Guest Book"
    cover = f"""<main class="page cover">
<div class="band" data-bleed><i></i><i></i><i></i><i></i></div>
<img class="logo" src="{logo}" alt="DIVELUX">
<h1><small>Home sauna</small>Guest<br>book<i>.</i></h1>
<p class="sub">Who came, how hot it was, and what everyone will remember.</p>
<div class="fields">{field("This book belongs to the sauna at")}{field("First entry")}</div>
{C.foot()}
</main>"""
    about = f"""<main class="page white">
{ph("About this sauna", "Fill this page in once. It turns a stack of printed sheets into your book.")}
<div class="body">
<div class="grid2"><div>{field("Name of the sauna")}{field("Built or first heated")}{field("Benches seat")}</div>
<div>{field("Where")}{field("Favorite temperature")}{field("Keeper of the stove")}</div></div>
<div class="checks"><span>Heated by</span><b><i class="box"></i>wood</b><b><i class="box"></i>electric</b><b><i class="box"></i>infrared</b><b><i class="box"></i>other</b></div>
<p class="lab">House traditions</p>
{lines(7)}
<div class="tip"><b>For our guests</b>Welcome. After the sauna, write the date, your names, and a line about the evening. The temperature is optional, but it is fun to look back on.</div>
<div class="tip"><b>How to print this book</b>Print the cover and this page once. Print the visit log and the guest entry pages as many times as you need, single- or double-sided. Punch the left margin for a binder, or staple along the left edge. Keep the book in the lounge, not in the hot room.</div>
</div>
{C.foot(note + " · About this sauna")}
</main>"""
    rows = "<tr><td></td><td></td><td></td><td></td><td></td></tr>" * 12
    log = f"""<main class="page white">
{ph("Visit log", "One line per sauna night. Print this page as many times as you need.")}
<div class="body">
<table class="log"><colgroup><col style="width:14%"><col style="width:31%"><col style="width:11%"><col style="width:10%"><col></colgroup>
<thead><tr><th>Date</th><th>Guests</th><th>Temp<small>°F or °C</small></th><th>Rounds</th><th>Note<small>weather, steam, the best moment</small></th></tr></thead>
<tbody>{rows}</tbody></table>
</div>
{C.foot(note + " · Visit log")}
</main>"""
    entry = f"""<div class="entry"><div class="row">{field("Date")}{field("Guests")}{field("Temp")}</div>{lines(3)}</div>"""
    entries = f"""<main class="page white">
{ph("Guest entries", "Room for a few sentences, a drawing, or a thank-you. Print as many as you need.")}
<div class="body"><div class="entries">{entry * 4}</div></div>
{C.foot(note + " · Guest entries")}
</main>"""
    recs = ["Hottest session", "Coldest plunge", "Most guests on the benches", "Longest sauna evening",
            "First snow sauna of the year", "Guest who traveled farthest", "Best sauna snack", "Best story told on the bench"]
    records = f"""<main class="page white">
{ph("Sauna records", "The friendly kind. Update a line whenever a record falls.")}
<div class="body"><div class="records">{''.join(f'<div class="rec"><b>{r}</b>{field("Who")}{field("When")}{field("Details")}</div>' for r in recs)}</div></div>
{C.foot(note + " · Sauna records")}
</main>"""
    ticks = "".join('<i class="box"></i>' for _ in range(20))
    regrows = f'<tr><td></td><td class="ticks">{ticks}</td></tr>' * 15
    regulars = f"""<main class="page white">
{ph("Regulars", "One box per visit. Twenty visits earns a name on the bench, or whatever your house decides.")}
<div class="body"><table class="reg"><colgroup><col><col style="width:4.25in"></colgroup>
<thead><tr><th>Name</th><th>Visits</th></tr></thead><tbody>{regrows}</tbody></table></div>
{C.foot(note + " · Regulars")}
</main>"""
    notes = f"""<main class="page white">
{ph("Notes and stories", "Recipes for the steam, repairs, plans for next winter.")}
<div class="body">{lines(22)}</div>
{C.foot(note + " · Notes and stories")}
</main>"""
    body = cover + about + log + entries + records + regulars + notes
    C.write(os.path.join(C.ROOT, SLUG, SLUG + ".html"), C.doc(TITLE, DESC, KEYWORDS, CSS, body))
    meta = dict(title="Home Sauna Guest Book: Printable Cover and Log Pages", subject=DESC, keywords=KEYWORDS)
    jobs = C.std_jobs(SLUG, SLUG + ".html", SLUG, meta)
    return dict(slug=SLUG, jobs=jobs, preview=dict(pdf=jobs[0]["pdf"], pages=[1, 3, 4], dpi=75))
