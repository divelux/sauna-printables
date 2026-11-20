"""13. Sauna and Cold Plunge Journal: undated, eight pages. Cover, how to use, year at a glance,
a week spread (two pages), lined notes, dot-grid notes, places to try.
The typical temperature ranges on the "how to use" page are read from the open dataset."""
import csv
import os
import common as C
import w2

SLUG = "sauna-cold-plunge-journal"
TITLE = "Sauna and Cold Plunge Journal"
DESC = "An undated printable journal for sauna and cold plunge sessions: cover, year at a glance, a weekly spread with seven day blocks and a review, notes pages and a places-to-try list. Eight pages."
KEYWORDS = "sauna journal printable, cold plunge log, sauna log book, undated journal pages, contrast therapy tracker, sauna tracker printable, DIVELUX"
DATA = "/root/divelux/freebies/dataset/sauna_traditions.csv"

CSS = w2.CSS + """
.page{padding:.55in .6in .34in .8in}
.cover{padding:.55in .6in .34in .8in}
.cover .logo{width:1.45in;display:block}
.cover h1{font-size:112pt;line-height:.83;margin:1.1in 0 0 -.045in;white-space:normal}
.cover h1 small{display:block;font-family:var(--display);font-stretch:100%;font-weight:600;font-size:14pt;line-height:1.2;letter-spacing:.01em;color:var(--ink-2);margin:0 0 .16in .04in}
.cover .sub{font-family:var(--display);font-weight:500;font-size:16pt;line-height:1.28;color:var(--ink-2);margin-top:.3in;max-width:4.6in}
.cover .fields{margin-top:auto;max-width:4.4in}
.cover .field{height:.44in;font-size:10pt}
.cover .foot{margin-top:0}
.cover .band{display:grid;grid-template-columns:repeat(4,1fr);height:2in;margin:.45in -.6in .32in -.8in;border-top:2px solid var(--ink);border-bottom:2px solid var(--ink);flex:none}
.cover .band i{display:block;border-left:1px solid rgba(27,21,18,.22)}
.cover .band i:first-child{border-left:0}
.cover .band i:nth-child(1){background:var(--t4)}.cover .band i:nth-child(2){background:var(--t3)}
.cover .band i:nth-child(3){background:var(--t2)}.cover .band i:nth-child(4){background:var(--t1)}
.body{flex:1;display:flex;flex-direction:column;min-height:0;padding:.16in 0 .16in}
.cols3{display:grid;grid-template-columns:repeat(3,1fr);column-gap:.3in}
.blk{border-top:2px solid var(--ink);padding-top:.08in}
.blk b.t{display:block;font-family:var(--display);font-weight:700;font-size:14pt;line-height:1.15;letter-spacing:-.01em;margin-bottom:.05in}
.blk p,.blk li{font-size:9.2pt;line-height:1.45;color:var(--ink-2)}
.blk li{padding:.035in 0;border-bottom:1px solid var(--line)}
.blk li:last-child{border-bottom:0}
.blk li b{color:var(--ink);font-weight:600}
.ranges{width:100%;border-collapse:collapse;margin-top:.02in}
.ranges td{font-size:9.2pt;line-height:1.3;color:var(--ink-2);padding:.045in 0;border-bottom:1px solid var(--line)}
.ranges td:last-child{text-align:right;font-weight:600;color:var(--ink);white-space:nowrap}
.setup{margin-top:.3in}
.lab{font-family:var(--display);font-weight:700;font-size:13pt;margin:0 0 .02in}
.grid2{display:grid;grid-template-columns:1fr 1fr;column-gap:.35in}
.tip{background:var(--paper);border-radius:6px;padding:.15in .2in;font-size:9.4pt;line-height:1.5;color:var(--ink-2);margin-top:auto}
.tip b{font-family:var(--display);font-weight:700;font-size:12pt;color:var(--ink);display:block;margin-bottom:.03in}
.year{flex:1;display:grid;grid-template-rows:auto repeat(12,1fr);min-height:0}
.year .r{display:grid;grid-template-columns:1.05in repeat(31,1fr) .5in;align-items:center;border-bottom:1px solid var(--line)}
.year .r.hd{border-bottom:1px solid var(--ink);font-size:6.6pt;color:var(--muted);padding-bottom:.04in;align-items:end}
.year .r.hd span{text-align:center}
.year .r.hd span:first-child,.year .r .m{text-align:left}
.year .r.hd span:last-child{text-align:right}
.year .m{border-bottom:1px solid var(--ink-2);height:.26in;margin-right:.12in}
.year .o{width:.135in;height:.135in;border:1px solid var(--ink-2);border-radius:50%;justify-self:center;background:#fff}
.year .tot{border-bottom:1px solid var(--ink-2);height:.26in;margin-left:.1in}
.key{display:flex;gap:.3in;font-size:8.6pt;color:var(--ink-2);padding-top:.12in;align-items:center;flex:none}
.key .o{display:inline-block;width:.135in;height:.135in;border:1px solid var(--ink-2);border-radius:50%;vertical-align:-.02in;margin-right:.05in;background:#fff}
.key .o.f{background:var(--ink)}.key .o.h{background:linear-gradient(90deg,var(--ink) 50%,#fff 50%)}
.wk{display:flex;gap:.3in;align-items:flex-end;flex:none;padding-bottom:.06in}
.wk .field{flex:1;height:.34in}
.days{flex:1;display:grid;row-gap:.13in;min-height:0}
.day{border:1px solid var(--ink-2);border-radius:6px;padding:.07in .16in .12in;display:flex;flex-direction:column;background:#fff}
.day .row{display:grid;column-gap:.16in}
.day .r1{grid-template-columns:1.1fr 1.1fr 2fr 1fr}
.day .r2{grid-template-columns:.9fr 1.1fr 1.5fr 1fr 2.1fr}
.day .field{height:.33in;font-size:8.2pt}
.day .chk{display:flex;align-items:flex-end;gap:.06in;font-size:8.2pt;color:var(--ink-2);height:.33in;padding-bottom:.03in;white-space:nowrap}
.day .felt{display:flex;align-items:flex-end;gap:.055in;font-size:8.2pt;color:var(--ink-2);height:.33in;padding-bottom:.02in;white-space:nowrap}
.day .felt i{display:inline-flex;width:.17in;height:.17in;border:1px solid var(--ink-2);border-radius:50%;align-items:center;justify-content:center;font-style:normal;font-size:6.6pt;color:var(--muted)}
.day .lines i{max-height:.34in}
.review{border-top:2px solid var(--ink);padding-top:.08in;display:flex;flex-direction:column;min-height:0}
.review b.t{font-family:var(--display);font-weight:700;font-size:14.5pt;letter-spacing:-.01em}
.review .tot{display:grid;grid-template-columns:repeat(3,1fr);column-gap:.2in}
.review .field{font-size:8.6pt;height:.46in}
.dots{flex:1;background-image:radial-gradient(circle,#a79d91 .011in,transparent .0125in);background-size:.2in .2in;background-position:.1in .1in;margin:.06in 0 0}
table.places{flex:1}
table.places td.c{text-align:center}
"""


def ranges():
    rows = {r["name"]: r for r in csv.DictReader(open(DATA, encoding="utf-8"))}
    out = []
    for name, label in [("Finnish sauna", "Finnish sauna"), ("Russian banya", "Russian banya"), ("Infrared sauna", "Infrared sauna"),
                        ("Steam room", "Steam room")]:
        r = rows[name]
        out.append(f'<tr><td>{label}</td><td class="num">{r["typical_air_temp_f_min"]}–{r["typical_air_temp_f_max"]} °F</td></tr>')
    return "".join(out)


def day(lines=1):
    felt = "".join(f"<i>{n}</i>" for n in range(1, 6))
    return f"""<div class="day">
<div class="row r1">{w2.field("Day")}{w2.field("Date")}{w2.field("Sauna type")}{w2.field("Temp")}</div>
<div class="row r2">{w2.field("Rounds")}{w2.field("Min each")}<div class="chk"><i class="box"></i>Cold plunge</div>{w2.field("Sec in cold")}<div class="felt">How I felt {felt}</div></div>
{w2.lines(lines)}
</div>"""


def build():
    logo = C.logo_data_uri()
    months = "".join('<div class="r"><i class="m"></i>' + '<i class="o"></i>' * 31 + '<i class="tot"></i></div>' for _ in range(12))
    hd = '<div class="r hd"><span>Month</span>' + "".join(f"<span>{n}</span>" for n in range(1, 32)) + "<span>Total</span></div>"
    places = "<tr>" + "<td></td>" * 4 + '<td class="c"><i class="box"></i></td></tr>'
    body = f"""<main class="page cover">
<img class="logo" src="{logo}" alt="DIVELUX">
<h1><small>Undated · print what you need</small>Sauna &amp; cold plunge journal<i>.</i></h1>
<p class="sub">A place to write down the heat, the cold and how the day felt.</p>
<div class="fields">{w2.field("This journal belongs to")}{w2.field("Started on")}</div>
<div class="band"><i></i><i></i><i></i><i></i></div>
{C.foot()}
</main>
<main class="page white">
{w2.ph("How to use it", "Print the weekly spread as many times as you like. Punch the pages and keep them in a binder.")}
<div class="body">
<div class="cols3">
<div class="blk"><b class="t">One block per session</b><ul>
<li><b>Temp:</b> air temperature at bench level, °F or °C.</li>
<li><b>Rounds:</b> how many times you went into the heat.</li>
<li><b>Min each:</b> average minutes per round.</li>
<li><b>Cold plunge:</b> tick it, then note total seconds in the cold.</li>
</ul></div>
<div class="blk"><b class="t">How I felt, 1 to 5</b><ul>
<li><b>1</b> rough, cut it short</li><li><b>2</b> not my day</li><li><b>3</b> fine</li><li><b>4</b> good</li><li><b>5</b> great</li>
</ul></div>
<div class="blk"><b class="t">Typical air temperatures</b>
<table class="ranges">{ranges()}</table>
<p style="font-size:7.6pt;color:var(--muted);margin-top:.06in">From the open dataset Sauna Traditions of the World. Your room may run cooler or hotter.</p></div>
</div>
<div class="setup"><p class="lab">My setup</p>
<div class="grid2"><div>{w2.field("Where I sauna")}{w2.field("Sauna type")}{w2.field("Usual temperature")}</div>
<div>{w2.field("Cold plunge, shower or lake")}{w2.field("Usual days")}{w2.field("Sauna partner")}</div></div></div>
<div class="setup" style="flex:1;display:flex;flex-direction:column;min-height:0"><p class="lab">What I want from this journal</p>{w2.lines(5)}</div>
<div class="tip" style="margin-top:.24in"><b>A logbook, not a training plan</b>Leave the heat or the cold as soon as you feel dizzy, numb or unwell. Do not plunge alone, and skip alcohol. General information, not medical advice: talk to your doctor before you start heat or cold exposure.</div>
</div>
{C.foot("Sauna and Cold Plunge Journal · How to use it")}
</main>
<main class="page white">
{w2.ph("Year at a glance", "One row per month. Fill a circle for every sauna day and watch the habit take shape.")}
<div class="body">
<div class="year">{hd}{months}</div>
<div class="key"><span><i class="o f"></i>Sauna</span><span><i class="o h"></i>Sauna and cold plunge</span><span><i class="o"></i>Rest day</span></div>
</div>
{C.foot("Sauna and Cold Plunge Journal · Year at a glance")}
</main>
<main class="page white">
{w2.ph("This week", "Left page of the weekly spread. One block per session or per day.")}
<div class="body">
<div class="wk">{w2.field("Week of")}{w2.field("Plan for the week")}</div>
<div class="days" style="grid-template-rows:repeat(4,1fr)">{day(2) * 4}</div>
</div>
{C.foot("Sauna and Cold Plunge Journal · Week, page 1")}
</main>
<main class="page white">
{w2.ph("This week", "Right page of the weekly spread, with a short review at the end.")}
<div class="body">
<div class="days" style="grid-template-rows:repeat(3,1fr) 1.25fr">{day(2) * 3}
<div class="review"><b class="t">Week in review</b>
<div class="tot">{w2.field("Sessions")}{w2.field("Minutes in the heat")}{w2.field("Cold plunges")}</div>
{w2.field("Best moment")}{w2.field("Next week")}</div></div>
</div>
{C.foot("Sauna and Cold Plunge Journal · Week, page 2")}
</main>
<main class="page white">
{w2.ph("Notes", "Lined page. Print as many as you need.")}
<div class="body">{w2.lines(26)}</div>
{C.foot("Sauna and Cold Plunge Journal · Notes")}
</main>
<main class="page white">
{w2.ph("Sketches", "Dot grid for bench layouts, build ideas and doodles.")}
<div class="body"><div class="dots"></div></div>
{C.foot("Sauna and Cold Plunge Journal · Dot grid")}
</main>
<main class="page white">
{w2.ph("Places to try", "Saunas, bathhouses, lakes and cold plunges you want to visit.")}
<div class="body"><table class="log places"><colgroup><col style="width:27%"><col style="width:17%"><col style="width:17%"><col><col style="width:9%"></colgroup>
<thead><tr><th>Place</th><th>Type</th><th>Where</th><th>Notes</th><th>Been</th></tr></thead><tbody>{places * 16}</tbody></table></div>
{C.foot("Sauna and Cold Plunge Journal · Places to try")}
</main>"""
    C.write(os.path.join(C.ROOT, SLUG, SLUG + ".html"), C.doc(TITLE, DESC, KEYWORDS, CSS, body))
    meta = dict(title="Sauna and Cold Plunge Journal (Undated Printable)", subject=DESC, keywords=KEYWORDS)
    jobs = C.std_jobs(SLUG, SLUG + ".html", SLUG, meta)
    return dict(slug=SLUG, jobs=jobs, preview=dict(pdf=jobs[0]["pdf"], pages=[1, 4, 5], dpi=75))
