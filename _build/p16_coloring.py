"""16. Sauna coloring pages: six pages of hand-drawn vector line art (see art.py). No raster or generated images."""
import os
import common as C
import w2
import art

SLUG = "sauna-coloring-pages"
TITLE = "Sauna Coloring Pages"
DESC = "Six printable sauna coloring pages for kids and grown-ups: a stove with stones, a bucket and ladle, felt sauna hats, a lakeside sauna cabin, a leafy whisk and a mandala."
KEYWORDS = "sauna coloring pages, coloring pages for adults, kids coloring printable, cabin coloring page, mandala coloring page, Finnish sauna activity sheet, DIVELUX"

CSS = w2.CSS + """
.page{padding:.45in .6in .32in;background:#fff}
.ct{display:flex;justify-content:space-between;align-items:flex-end;gap:.3in;border-bottom:2px solid var(--ink);padding-bottom:.09in;flex:none}
.ct h1,.ct h2{font-family:var(--display);font-weight:800;font-stretch:75%;font-size:34pt;line-height:.9;letter-spacing:-.018em;margin:0;white-space:nowrap}
.ct .k{display:block;font-family:var(--body);font-size:6.4pt;letter-spacing:.16em;text-transform:uppercase;font-weight:600;color:var(--muted);margin-bottom:.06in}
.ct p{font-size:9.4pt;line-height:1.4;color:var(--ink-2);max-width:3.5in;text-align:right;text-wrap:balance}
.artw{flex:1;display:flex;align-items:center;justify-content:center;min-height:0}
.artw svg{display:block;width:7.08in;height:8.5in}
"""


def build():
    pages = []
    n = len(art.PAGES)
    for i, (title, cap, fn) in enumerate(art.PAGES, 1):
        tag = "h1" if i == 1 else "h2"
        level = "Detailed" if i > 4 else "Easy"
        pages.append(f"""<main class="page">
<div class="ct"><div><span class="k">Coloring page {i} of {n} · {level}</span><{tag}>{C.esc(title)}</{tag}></div><p>{C.esc(cap)}</p></div>
<div class="artw">{fn()}</div>
{C.foot("Sauna Coloring Pages")}
</main>""")
    C.write(os.path.join(C.ROOT, SLUG, SLUG + ".html"), C.doc(TITLE, DESC, KEYWORDS, CSS, "\n".join(pages)))
    meta = dict(title="Sauna Coloring Pages for Kids and Grown-Ups (6 Printable Pages)", subject=DESC, keywords=KEYWORDS)
    jobs = C.std_jobs(SLUG, SLUG + ".html", SLUG, meta)
    return dict(slug=SLUG, jobs=jobs, preview=dict(pdf=jobs[0]["pdf"], pages=[1, 4, 6], dpi=75))
