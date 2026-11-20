"""5. Sauna Types cheat sheet: one page, twelve rows. Numbers are read from the dataset; the short notes
are condensed from the dataset's own notes column."""
import json
import os
import common as C

SLUG = "sauna-types-cheat-sheet"
TITLE = "Sauna Types Cheat Sheet"
DESC = "One printable page that compares twelve sauna types: Finnish sauna, banya, steam room, infrared, hammam and more, with typical temperature, humidity and round length."
KEYWORDS = "sauna types, types of saunas compared, Finnish sauna vs banya, infrared vs traditional sauna, steam room vs sauna, hammam, sauna cheat sheet, DIVELUX"
DATA = "/root/divelux/freebies/dataset/sauna_traditions.json"

# (dataset name(s), display name, "where · heat", note, round override)
ROWS = [
    (["Finnish sauna"], "Finnish sauna", "Finland · wood or electric stove (kiuas) with stones",
     "Water on the stones makes a burst of steam called löyly. Many bathers settle around 176–194 °F.", None),
    (["Finnish smoke sauna"], "Smoke sauna", "Finland, Estonia · wood-fired stone stove, no chimney",
     "Heated for hours; the smoke is let out before bathing. Soft, long-lasting heat.", None),
    (["Russian banya"], "Russian banya", "Russia, Ukraine, Belarus · large stove, enclosed stones",
     "Cooler air than a Finnish sauna but much more steam, so it can feel hotter. Leafy whisks and felt hats.", None),
    (["Lithuanian pirtis", "Latvian pirts"], "Pirtis and pirts", "Lithuania, Latvia · wood-burning stove with stones",
     "Generous steam and whisking led by a bath master. A full ritual can last several hours.", None),
    (["German Aufguss sauna"], "Aufguss sauna", "Germany, Austria, Switzerland · stove with stones",
     "A sauna master pours scented water on the stones and moves the hot air with a towel.", None),
    (["Bio sauna (soft sauna)"], "Bio sauna", "Germany, Austria · stove plus an evaporator",
     "A gentler room between a Finnish sauna and a steam room, often with herbal vapor.", None),
    (["Infrared sauna"], "Infrared sauna", "Worldwide · panels that warm the body directly",
     "No stove, stones or steam. Usually one longer session instead of several short rounds.", None),
    (["Steam room"], "Steam room", "Worldwide · steam generator, tiled sealed room",
     "Far cooler air than a sauna, but saturated air slows the body's cooling by evaporation.", None),
    (["Turkish hammam"], "Turkish hammam", "Turkey · furnace-heated floor, walls and marble",
     "A scrub with a coarse mitt and a soap-foam wash. One long visit, not timed rounds.", "one visit"),
    (["Japanese sauna"], "Japanese sauna", "Japan · electric or gas stove, usually with stones",
     "A cycle of sauna, cold-water bath (mizuburo) and seated rest in open air.", None),
    (["Korean jjimjilbang"], "Korean jjimjilbang", "South Korea · heated rooms, kilns, heated floors",
     "A large bathhouse with themed rooms, from mild rooms to hot kilns.", None),
    (["North American gym or club sauna"], "Gym or club sauna", "United States, Canada · electric heater with stones",
     "Often runs drier: many facilities do not allow water on the heater. Check posted rules.", None),
]
WATER = {"yes": "yes", "no": "no", "n-a": "no stones", "sometimes": "sometimes"}

CSS = """
.page{padding:.5in .56in .34in}
.head{display:grid;grid-template-columns:auto 1fr;column-gap:.45in;align-items:end}
h1{font-weight:800;font-stretch:75%;font-size:76pt;line-height:.84;letter-spacing:-.02em;margin:.08in 0 0 -.03in;white-space:nowrap}
h1 i{font-style:normal;color:var(--ember)}
.lead{font-family:var(--display);font-weight:500;font-size:13pt;line-height:1.3;color:var(--ink-2);padding-bottom:.06in;text-wrap:balance}
table{width:100%;border-collapse:collapse;margin-top:.17in;flex:1;table-layout:fixed}
th{font-family:var(--body);font-weight:600;font-size:7.2pt;letter-spacing:.1em;text-transform:uppercase;text-align:left;color:var(--ink);
border-top:2px solid var(--ink);border-bottom:1px solid var(--ink);padding:.06in .1in .06in 0;vertical-align:bottom;line-height:1.25}
td{border-bottom:1px solid var(--line-2);padding:.04in .1in .04in 0;vertical-align:middle;font-size:8.6pt;line-height:1.34;color:var(--ink-2)}
tr:last-child td{border-bottom:2px solid var(--ink)}
td:last-child,th:last-child{padding-right:0}
td.t b{display:block;font-family:var(--display);font-weight:700;font-size:13.5pt;line-height:1.12;letter-spacing:-.012em;color:var(--ink)}
td.t span{display:block;font-size:7.5pt;line-height:1.3;color:var(--muted);margin-top:.02in}
td.a b{display:block;font-family:var(--display);font-weight:700;font-size:12.5pt;line-height:1.1;color:var(--ink);white-space:nowrap}
td.a span{display:block;font-size:7.8pt;color:var(--muted)}
td.a .bar{position:relative;height:.055in;background:var(--paper-2);border-radius:2px;margin-top:.035in;width:1.12in}
td.a .bar i{position:absolute;top:0;bottom:0;background:var(--ink);border-radius:2px}
td.a em{font-style:normal;font-size:8.2pt;color:var(--muted)}
td.s{font-weight:600;color:var(--ink)}
td.s small{display:block;font-weight:400;font-size:7.6pt;color:var(--muted)}
td.n{font-size:8.3pt}
.fine{font-size:7.5pt;line-height:1.42;color:var(--muted);margin:.09in 0 .1in}
.fine b{color:var(--ink-2);font-weight:600}
"""


def cell_temp(rs):
    r = rs[0]
    lo, hi = r["typical_air_temp_f_min"], r["typical_air_temp_f_max"]
    if lo is None:
        return '<td class="a"><em>not stated: published figures vary</em></td>'
    left, width = (lo - 100) / 130 * 100, (hi - lo) / 130 * 100
    return (f'<td class="a num"><b>{lo}–{hi} °F</b><span>{r["typical_air_temp_c_min"]}–{r["typical_air_temp_c_max"]} °C</span>'
            f'<div class="bar"><i style="left:{left:.1f}%;width:{width:.1f}%"></i></div></td>')


def build():
    data = {d["name"]: d for d in json.load(open(DATA, encoding="utf-8"))}
    trs = []
    for names, disp, where, note, round_override in ROWS:
        rs = [data[n] for n in names]
        r = rs[0]
        assert len({(x["typical_relative_humidity"], x["water_on_stones"], x["typical_air_temp_f_min"]) for x in rs}) == 1
        hum = r["typical_relative_humidity"] or "—"
        if r["typical_relative_humidity_pct_min"] is not None:
            hum += f'<small>{r["typical_relative_humidity_pct_min"]}–{r["typical_relative_humidity_pct_max"]}%</small>'
        if round_override:
            rnd = round_override
        elif r["typical_round_minutes_min"] is not None:
            rnd = f'{r["typical_round_minutes_min"]}–{r["typical_round_minutes_max"]}<small>min</small>'
        else:
            rnd = "—"
        trs.append(f'<tr><td class="t"><b>{C.esc(disp)}</b><span>{C.esc(where)}</span></td>{cell_temp(rs)}'
                   f'<td class="s num">{hum}</td><td class="s num">{rnd}</td><td class="s">{WATER[r["water_on_stones"]]}</td>'
                   f'<td class="n">{C.esc(note)}</td></tr>')
    f, e, s, n = data["Finnish sauna"], data["Estonian sauna"], data["Swedish bastu"], data["Norwegian badstue"]
    rel = (f'Estonian saun ({e["typical_air_temp_f_min"]}–{e["typical_air_temp_f_max"]} °F), Swedish bastu and Norwegian badstue '
           f'({s["typical_air_temp_f_min"]}–{s["typical_air_temp_f_max"]} °F)')
    assert (s["typical_air_temp_f_min"], s["typical_air_temp_f_max"]) == (n["typical_air_temp_f_min"], n["typical_air_temp_f_max"])
    body = f"""<main class="page">
<span class="kicker">One-page reference</span>
<div class="head"><h1>Sauna types<i>.</i></h1><p class="lead">Twelve hot rooms side by side: how each one is heated, how hot and how humid it usually runs, and what to expect.</p></div>
<table>
<colgroup><col style="width:29%"><col style="width:17.5%"><col style="width:10.5%"><col style="width:8.5%"><col style="width:10%"><col></colgroup>
<thead><tr><th>Type</th><th>Air temperature</th><th>Humidity</th><th>One round</th><th>Water on stones</th><th>Good to know</th></tr></thead>
<tbody>{''.join(trs)}</tbody></table>
<p class="fine"><b>Close relatives of the Finnish sauna:</b> {rel}. A dash means not stated. The small bar shows the range on a 100–230 °F scale. Figures are commonly quoted reference ranges for the air in the hot room, not measurements; round lengths are typical habits, not recommendations. Source: Sauna Traditions of the World (DIVELUX, 2026), an open dataset. General information, not medical advice.</p>
{C.foot()}
</main>"""
    C.write(os.path.join(C.ROOT, SLUG, SLUG + ".html"), C.doc(TITLE, DESC, KEYWORDS, CSS, body))
    meta = dict(title="Sauna Types Cheat Sheet: Twelve Hot Rooms Compared on One Page", subject=DESC, keywords=KEYWORDS)
    jobs = C.std_jobs(SLUG, SLUG + ".html", SLUG, meta)
    return dict(slug=SLUG, jobs=jobs, preview=dict(pdf=jobs[0]["pdf"]))
