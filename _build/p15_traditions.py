"""15. Sauna Traditions of the World poster: an infographic table by region (landscape).
Every word and number in the table is read from ../dataset/sauna_traditions.csv; only the grouping
into regions and the column layout are decided here. No map: a table reads better than rough cartography."""
import csv
import os
import re
import common as C
import w2

SLUG = "sauna-traditions-of-the-world-poster"
TITLE = "Sauna Traditions of the World Poster"
DESC = "A printable poster that lays out 28 sauna and bathing traditions by region: where they come from, what kind of bath they are, typical temperatures, steam and felt hats."
KEYWORDS = "sauna traditions of the world, sauna poster, banya, hammam, onsen, jjimjilbang, temazcal, bathing culture infographic, sauna types by country, DIVELUX"
DATA = "/root/divelux/freebies/dataset/sauna_traditions.csv"

REGIONS = [
    ("Nordic countries", ["Finnish sauna", "Finnish smoke sauna", "Swedish bastu", "Norwegian badstue",
                          "Icelandic geothermal pool and hot tub"]),
    ("Baltic states", ["Estonian sauna", "Estonian smoke sauna (Võromaa)", "Latvian pirts", "Lithuanian pirtis"]),
    ("Eastern Europe", ["Russian banya", "Russian black banya"]),
    ("Western and Central Europe", ["German Aufguss sauna", "Bio sauna (soft sauna)", "Irish sweat house (historical)"]),
    ("Mediterranean and Caucasus", ["Roman baths (historical)", "Turkish hammam", "Moroccan hammam", "Georgian sulfur bath"]),
    ("East Asia", ["Japanese sento", "Japanese onsen", "Japanese sauna", "Korean jjimjilbang", "Korean hanjeungmak"]),
    ("The Americas", ["Native American sweat lodge", "Temazcal", "North American gym or club sauna"]),
    ("Worldwide, modern", ["Infrared sauna", "Steam room"]),
]
LO, HI = 35, 100          # bar scale, °C

CSS = w2.CSS + """
.page{padding:.42in .55in .32in}
.top{display:flex;justify-content:space-between;align-items:flex-end;gap:.4in;flex:none}
h1{font-size:50pt;line-height:.86;margin:.04in 0 0 -.03in}
.top .lead{font-size:10.5pt;max-width:2.4in;padding-bottom:.03in;text-align:right}
table.t{width:100%;border-collapse:collapse;table-layout:fixed;flex:1;margin-top:.13in}
table.t th{font-family:var(--body);font-weight:600;font-size:6.4pt;letter-spacing:.1em;text-transform:uppercase;text-align:left;color:var(--ink);
border-top:2px solid var(--ink);border-bottom:1px solid var(--ink);padding:.045in .1in .045in 0;line-height:1.2;vertical-align:bottom}
table.t td{border-bottom:1px solid var(--line);padding:.008in .1in .008in 0;vertical-align:middle;font-size:7pt;line-height:1.16;color:var(--ink-2)}
table.t tr.g td{border-top:1.5px solid var(--ink)}
table.t tr.last td{border-bottom:0}
table.t tbody:last-child tr.last td{border-bottom:2px solid var(--ink)}
table.t td.r{vertical-align:top;padding-top:.045in;font-family:var(--display);font-weight:700;font-size:8.8pt;line-height:1.1;letter-spacing:-.005em;color:var(--ink);border-bottom:0;padding-right:.06in}
table.t td.n b{font-family:var(--display);font-weight:700;font-size:8.8pt;letter-spacing:-.008em;color:var(--ink);margin-right:.05in}
table.t td.n span{font-size:6.5pt;color:var(--muted)}
table.t td.n em{font-style:normal;font-size:5.4pt;font-weight:600;letter-spacing:.06em;border:1px solid var(--ink-2);border-radius:3px;padding:0 .03in;margin-left:.04in;color:var(--ink-2);white-space:nowrap;vertical-align:.01in}
table.t td.h{white-space:nowrap}
table.t td.h b{font-weight:600;color:var(--ink)}
table.t td.h small{font-size:6.6pt;color:var(--muted)}
.bar{position:relative;height:.07in;background:var(--paper-2);border-radius:2px;margin-right:.08in}
.bar i{position:absolute;top:0;bottom:0;background:var(--ink);border-radius:2px}
.bar.w i{background:transparent;border:1.3px solid var(--ink)}
.d{display:inline-block;width:.1in;height:.1in;border-radius:50%;border:1.2px solid var(--ink);vertical-align:-.012in}
.d.y{background:var(--ink)}.d.s{background:linear-gradient(90deg,var(--ink) 50%,transparent 50%)}
.dash{color:var(--line-2)}
.legend{font-size:6.7pt;line-height:1.45;color:var(--muted);margin:.06in 0 .07in;flex:none}
.legend b{color:var(--ink-2);font-weight:600}
.legend .d{width:.085in;height:.085in}
"""


def local(s):
    """Local names in Latin or Cyrillic script. Other scripts are shown by the romanization the dataset gives in brackets."""
    out = []
    for part in s.split(";"):
        part = part.strip()
        if re.search(r"[^\u0000-ɏЀ-ӿ]", part):
            m = re.search(r"\(([^)]+)\)", part)
            part = m.group(1) if m else ""
        if part:
            out.append(part)
    return "; ".join(out)


def dot(v):
    return {"yes": '<i class="d y"></i>', "sometimes": '<i class="d s"></i>', "no": '<i class="d"></i>'}.get(v, '<span class="dash">–</span>')


def heat(r):
    a0, a1, w0, w1 = (r[k] for k in ("typical_air_temp_c_min", "typical_air_temp_c_max", "typical_water_temp_c_min", "typical_water_temp_c_max"))
    if a0:
        f0, f1, c0, c1, cls, lab = r["typical_air_temp_f_min"], r["typical_air_temp_f_max"], a0, a1, "", ""
    elif w0:
        f0, f1, c0, c1, cls, lab = r["typical_water_temp_f_min"], r["typical_water_temp_f_max"], w0, w1, " w", " water"
    else:
        return '<td class="h"><small>not given</small></td><td></td>'
    left = (float(c0) - LO) / (HI - LO) * 100
    width = (float(c1) - float(c0)) / (HI - LO) * 100
    return (f'<td class="h num"><b>{f0}–{f1} °F</b> <small>{c0}–{c1} °C</small></td>'
            f'<td><div class="bar{cls}"><i style="left:{left:.1f}%;width:{width:.1f}%"></i></div></td>')


def build():
    rows = {r["name"]: r for r in csv.DictReader(open(DATA, encoding="utf-8"))}
    used = [n for _, names in REGIONS for n in names]
    assert sorted(used) == sorted(rows), set(rows) ^ set(used)
    body_rows = []
    for region, names in REGIONS:
        trs = []
        for i, n in enumerate(names):
            r = rows[n]
            m = re.search(r"inscribed (\d{4})", r["unesco_status"])
            un = f"<em>UNESCO {m.group(1)}</em>" if m else ""
            loc = local(r["local_name"])
            cls = " ".join(c for c in ("g" if i == 0 else "", "last" if i == len(names) - 1 else "") if c)
            first = f'<td class="r" data-bleed rowspan="{len(names)}">{C.esc(region)}</td>' if i == 0 else ""
            trs.append(f'<tr class="{cls}">{first}<td class="n"><b>{C.esc(n)}</b><span>{C.esc(loc)}</span>{un}</td>'
                       f'<td>{C.esc(r["country_or_region"])}</td><td>{C.esc(r["category"])}</td>{heat(r)}'
                       f'<td>{dot(r["water_on_stones"])}</td><td>{dot(r["headwear_traditionally_worn"])}</td></tr>')
        body_rows.append("<tbody>" + "".join(trs) + "</tbody>")
    lodge = rows["Native American sweat lodge"]["notes"].split(". Listed")[0]
    body = f"""<main class="page">
<div class="top"><div><span class="kicker">{len(rows)} bathing traditions, region by region</span>
<h1>Sauna traditions of the world<i>.</i></h1></div>
<p class="lead">Where people sweat, steam and soak, and how hot it gets.</p></div>
<table class="t"><colgroup><col style="width:.98in"><col style="width:3.05in"><col style="width:2.05in"><col style="width:1.42in"><col style="width:1.2in"><col style="width:.48in"><col style="width:.44in"><col style="width:.28in"></colgroup>
<thead><tr><th>Region</th><th>Tradition and local name</th><th>Where</th><th>Kind of bath</th><th colspan="2">Typical temperature</th><th>Steam</th><th>Hat</th></tr></thead>
{"".join(body_rows)}</table>
<p class="legend"><b>Bar:</b> typical air temperature on a 95–212 °F (35–100 °C) scale. <b>Outline bar:</b> water temperature of a bath. <b>Steam:</b> water is poured on hot stones. <b>Hat:</b> a felt hat is traditionally worn. <i class="d y"></i> yes &nbsp;<i class="d s"></i> sometimes &nbsp;<i class="d"></i> no &nbsp;– does not apply or unknown. “Not given”: published figures disagree, so the dataset leaves them blank. Native American sweat lodge: {C.esc(lodge[0].lower() + lodge[1:])}. Data: Sauna Traditions of the World, an open dataset by DIVELUX (CC BY 4.0). General information, not medical advice.</p>
{C.foot()}
</main>"""
    C.write(os.path.join(C.ROOT, SLUG, SLUG + ".html"), C.doc(TITLE, DESC, KEYWORDS, CSS, body, ext=True, land=True))
    meta = dict(title="Sauna Traditions of the World: A Printable Poster", subject=DESC, keywords=KEYWORDS)
    jobs = C.std_jobs(SLUG, SLUG + ".html", SLUG, meta, land=True)
    return dict(slug=SLUG, jobs=jobs, preview=dict(pdf=jobs[0]["pdf"]))
