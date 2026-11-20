"""4. Sauna Temperature Conversion chart: a dual °F/°C scale (100-230 °F) with typical ranges by sauna type.
Ranges come straight from ../../dataset/sauna_traditions.json; nothing is typed in by hand."""
import json
import os
import common as C

SLUG = "sauna-temperature-conversion-chart"
TITLE = "Sauna Temperature Conversion Chart (°F to °C)"
DESC = "A printable °F to °C chart for the hot room, 100 to 230 °F, with typical temperature ranges for 13 sauna types marked on the scale."
KEYWORDS = "sauna temperature chart, Fahrenheit to Celsius sauna, sauna temperature conversion, sauna temperature by type, banya temperature, steam room temperature, DIVELUX"
DATA = "/root/divelux/freebies/dataset/sauna_traditions.json"

SHORT = {"North American gym or club sauna": "North American gym sauna", "Bio sauna (soft sauna)": "Bio sauna"}

CSS = """
.page{padding:.52in .62in .34in}
.head{display:grid;grid-template-columns:1fr auto;column-gap:.4in;align-items:end;margin-top:.06in}
h1{font-weight:800;font-stretch:75%;font-size:92pt;line-height:.84;letter-spacing:-.02em;margin:.1in 0 0 -.03in;white-space:nowrap}
h1 small{display:block;font-family:var(--display);font-stretch:100%;font-weight:600;font-size:12.5pt;line-height:1.2;letter-spacing:.01em;color:var(--ink-2);margin:0 0 .1in .03in}
h1 i{font-style:normal;color:var(--ember)}
.formula{font-family:var(--display);font-weight:600;font-size:13pt;line-height:1.5;text-align:right;padding-bottom:.08in;white-space:nowrap}
.formula span{display:block;font-family:var(--body);font-weight:400;font-size:8.6pt;color:var(--muted);line-height:1.4}
.chart{flex:1;min-height:0;margin:.14in 0 .1in;border-top:2px solid var(--ink);padding-top:.08in;display:flex;justify-content:center}
.chart svg{height:100%;width:100%;display:block}
.chart text{font-family:var(--body);fill:var(--ink)}
.chart .f{font-family:var(--display);font-weight:700;font-size:15px;letter-spacing:-.01em}
.chart .c{font-weight:600;font-size:11.5px;fill:var(--ink-2)}
.chart .u{font-family:var(--display);font-weight:700;font-size:13px}
.chart .lab{font-family:var(--display);font-weight:600;font-size:10.6px}
.chart .rng{font-size:7.8px;font-weight:600;fill:var(--ink-2)}
.chart{position:relative}
.how{position:absolute;left:0;top:.1in;width:3.05in;font-size:9.4pt;line-height:1.45;color:var(--ink-2)}
.how b{display:block;font-family:var(--display);font-weight:700;font-size:13pt;line-height:1.2;color:var(--ink);margin-bottom:.04in}
.strip{display:grid;grid-template-columns:auto repeat(14,1fr);border-top:2px solid var(--ink);border-bottom:1px solid var(--line-2);flex:none}
.strip span{padding:.045in 0;text-align:center;font-variant-numeric:tabular-nums}
.strip .h{font-family:var(--display);font-weight:700;font-size:10pt;text-align:left;padding-right:.12in}
.strip .F{font-family:var(--display);font-weight:700;font-size:11pt;border-bottom:1px solid var(--line-2)}
.strip .h.F{border-bottom:1px solid var(--line-2)}
.strip .C{font-size:9.6pt;color:var(--ink-2)}
.fine{font-size:7.6pt;line-height:1.42;color:var(--muted);margin:.09in 0 .1in}
"""


def f2c(f):
    return (f - 32) * 5 / 9


def chart(rows):
    W, k, top, bot = 590, 3.72, 124, 12
    H = top + 130 * k + bot
    y = lambda f: top + (230 - f) * k
    ax = 92
    o = [f'<svg viewBox="0 0 {W} {H:.0f}" role="img" aria-label="Dual scale from 100 to 230 degrees Fahrenheit '
         f'with matching degrees Celsius, and typical ranges for 13 sauna types" preserveAspectRatio="xMinYMid meet">']
    lane0, pitch, bw = 158, 33.4, 24
    # grid
    for f in range(100, 231, 10):
        o.append(f'<line x1="{ax}" y1="{y(f):.1f}" x2="{W}" y2="{y(f):.1f}" stroke="#dcd4c8" stroke-width="1"/>')
    # axis
    o.append(f'<line x1="{ax}" y1="{y(230):.1f}" x2="{ax}" y2="{y(100):.1f}" stroke="#1b1512" stroke-width="2"/>')
    o.append(f'<text class="u" x="{ax - 14}" y="{y(230) - 22:.1f}" text-anchor="end">°F</text>')
    o.append(f'<text class="u" x="{ax + 14}" y="{y(230) - 22:.1f}">°C</text>')
    for f in range(100, 231, 5):
        major = f % 10 == 0
        o.append(f'<line x1="{ax - (12 if major else 6)}" y1="{y(f):.1f}" x2="{ax}" y2="{y(f):.1f}" stroke="#1b1512" stroke-width="{1.4 if major else 1}"/>')
        if major:
            o.append(f'<text class="f" x="{ax - 18}" y="{y(f) + 5.2:.1f}" text-anchor="end">{f}</text>')
    for c in range(40, 111, 5):
        f = c * 9 / 5 + 32
        o.append(f'<line x1="{ax}" y1="{y(f):.1f}" x2="{ax + 9}" y2="{y(f):.1f}" stroke="#1b1512" stroke-width="1.2"/>')
        o.append(f'<text class="c" x="{ax + 14}" y="{y(f) + 4:.1f}">{c}</text>')
    # lanes
    for i, r in enumerate(rows):
        x = lane0 + i * pitch
        lo, hi = r["f_min"], r["f_max"]
        mid = (lo + hi) / 2
        fill = "#f0a877" if mid >= 185 else "#f5c7a0" if mid >= 160 else "#f8dfc6" if mid >= 130 else "#fbf1e5"
        o.append(f'<rect x="{x:.1f}" y="{y(hi):.1f}" width="{bw}" height="{(hi - lo) * k:.1f}" rx="3" fill="{fill}" stroke="#1b1512" stroke-width="1"/>')
        cx = x + bw / 2
        o.append(f'<text class="lab" transform="translate({cx + 3.7:.1f} {y(hi) - 6:.1f}) rotate(-90)">{C.esc(r["name"])}</text>')
        o.append(f'<text class="rng" text-anchor="middle" transform="translate({cx + 2.8:.1f} {y(mid):.1f}) rotate(-90)">{lo}–{hi} °F</text>')
    o.append("</svg>")
    return "".join(o)


def load_rows():
    data = json.load(open(DATA, encoding="utf-8"))
    rows = []
    for d in data:
        if d.get("typical_air_temp_f_min") is None:
            continue
        rows.append(dict(name=SHORT.get(d["name"], d["name"]), f_min=d["typical_air_temp_f_min"], f_max=d["typical_air_temp_f_max"],
                         c_min=d["typical_air_temp_c_min"], c_max=d["typical_air_temp_c_max"]))
    rows.sort(key=lambda r: (r["f_max"], r["f_min"], r["name"]))
    assert all(100 <= r["f_min"] < r["f_max"] <= 230 for r in rows), rows
    return rows


def build():
    rows = load_rows()
    fs = list(range(100, 231, 10))
    strip = '<span class="h F">°F</span>' + "".join(f'<span class="F">{f}</span>' for f in fs)
    strip += '<span class="h C">°C</span>' + "".join(f'<span class="C">{round(f2c(f))}</span>' for f in fs)
    body = f"""<main class="page">
<div class="head"><h1><small>Sauna temperature conversion</small>°F to °C<i>.</i></h1>
<p class="formula">°C = (°F − 32) ÷ 1.8<br>°F = °C × 1.8 + 32<span>Scale: 100 to 230 °F, the range of the hot room</span></p></div>
<figure class="chart">{chart(rows)}<figcaption class="how"><b>How to read it</b>Find your thermometer reading on the scale: °F on the left, °C on the right. Each bar spans the range that type of sauna usually runs.</figcaption></figure>
<div class="strip num" aria-label="Conversion table, every 10 °F, rounded to the nearest degree">{strip}</div>
<p class="fine">Bars show commonly quoted air temperature ranges in the hot room for {len(rows)} sauna types. They are reference figures, not measurements, from the open dataset Sauna Traditions of the World (DIVELUX, 2026). Real rooms vary with the stove, the bench height and local habit. Table values are rounded to the nearest degree. General information, not medical advice.</p>
{C.foot()}
</main>"""
    C.write(os.path.join(C.ROOT, SLUG, SLUG + ".html"), C.doc(TITLE, DESC, KEYWORDS, CSS, body))
    meta = dict(title="Sauna Temperature Conversion Chart: °F to °C with Typical Ranges by Sauna Type", subject=DESC, keywords=KEYWORDS)
    jobs = C.std_jobs(SLUG, SLUG + ".html", SLUG, meta)
    return dict(slug=SLUG, jobs=jobs, preview=dict(pdf=jobs[0]["pdf"]))
