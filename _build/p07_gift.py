"""7. Sauna Evening gift certificate (two per sheet) and a sheet of eight gift tags."""
import os
import common as C

SLUG = "sauna-evening-gift-certificate"
TITLE = "Sauna Evening Gift Certificate and Gift Tags"
DESC = "A printable gift certificate for a sauna evening, two per sheet, plus a sheet of eight gift tags. Fill in the names, tick what is included, cut and give."
KEYWORDS = "sauna gift certificate, sauna evening voucher printable, gift tags printable, sauna lover gift, sauna gift idea, last-minute gift coupon, DIVELUX"

TAGS = [
    ("For your next sauna", ""),
    ("Warm wishes", ""),
    ("Good steam to you", ""),
    ("Hyviä löylyjä!", "Finnish for “enjoy the steam”"),
    ("S lyogkim parom!", "A Russian banya wish: “enjoy your steam”"),
    ("Stay warm", ""),
    ("Open before the sauna", ""),
    ("Heat, steam, rest", ""),
]

CSS = """
.page{padding:.3in .5in .3in;background:#fff}
.how{display:flex;justify-content:space-between;font-size:7.6pt;color:var(--muted);flex:none;padding-bottom:.08in}
.how b{color:var(--ink);font-weight:600}
.certs{flex:1;display:grid;grid-template-rows:1fr 1fr;row-gap:.3in;min-height:0;padding-bottom:.14in}
.cert{position:relative;background:var(--paper);outline:1px dashed #8d8378;display:grid;grid-template-columns:.62in 1fr;min-height:0}
.cert .band{display:grid;grid-template-rows:repeat(4,1fr);border-right:2px solid var(--ink)}
.cert .band i:nth-child(1){background:var(--t1)}.cert .band i:nth-child(2){background:var(--t2)}
.cert .band i:nth-child(3){background:var(--t3)}.cert .band i:nth-child(4){background:var(--t4)}
.cert .in{padding:.28in .38in .2in .36in;display:flex;flex-direction:column;min-width:0}
.cert .top{display:flex;justify-content:space-between;align-items:center}
.cert .top span{font-size:7.4pt;letter-spacing:.18em;text-transform:uppercase;font-weight:600;color:var(--ink-2)}
.cert .top img{height:.12in;display:block}
.cert h1,.cert .h1{font-family:var(--display);font-weight:800;font-stretch:75%;font-size:78pt;line-height:.86;letter-spacing:-.02em;margin:.16in 0 0 -.035in;white-space:nowrap}
.cert h1 i,.cert .h1 i{font-style:normal;color:var(--ember)}
.cert .sub{font-family:var(--display);font-weight:500;font-size:14pt;line-height:1.3;color:var(--ink-2);margin-top:.12in}
.cert .msg{margin-top:auto}
.cert .msg .field{height:.5in}
.cert .fields{display:grid;grid-template-columns:1fr 1fr .8fr;column-gap:.24in;margin-top:.04in}
.field{display:flex;align-items:flex-end;gap:.08in;font-size:9pt;color:var(--ink-2);height:.4in}
.field span{white-space:nowrap;padding-bottom:.03in}
.field i{flex:1;border-bottom:1px solid var(--ink-2);display:block;height:100%}
.cert .inc{display:grid;grid-template-columns:auto auto auto 1fr;gap:.05in .26in;align-items:center;font-size:9pt;color:var(--ink-2);margin-top:.16in}
.cert .inc b{font-family:var(--display);font-weight:700;color:var(--ink);font-size:10pt;grid-row:1 / span 2;align-self:start}
.box{display:inline-block;width:.13in;height:.13in;border:1.2px solid var(--ink-2);border-radius:2px;margin-right:.05in;vertical-align:-.02in}
.cert .cf{margin-top:.12in;padding-top:.06in;border-top:1px solid var(--line-2);font-size:6.6pt;color:var(--muted);display:flex;justify-content:space-between}
.cert .cf a{color:var(--ink);text-decoration:none;font-weight:600}
.tags{flex:1;display:grid;grid-template-columns:3.5in 3.5in;grid-template-rows:repeat(4,2.25in);justify-content:center;align-content:center;gap:0;min-height:0}
.tag{outline:1px dashed #8d8378;background:var(--paper);display:grid;grid-template-columns:.62in 1fr;min-width:0}
.tag .hole{display:flex;align-items:center;justify-content:center;border-right:2px solid var(--ink)}
.tag:nth-child(4n+1) .hole{background:var(--t1)}.tag:nth-child(4n+2) .hole{background:var(--t2)}
.tag:nth-child(4n+3) .hole{background:var(--t3)}.tag:nth-child(4n+4) .hole{background:var(--t2)}
.tag .hole i{width:.2in;height:.2in;border-radius:50%;border:1.2px solid var(--ink);background:#fff;display:block}
.tag .in{padding:.2in .24in .16in .22in;display:flex;flex-direction:column;min-width:0}
.tag .ph{font-family:var(--display);font-weight:800;font-stretch:75%;font-size:25pt;line-height:.92;letter-spacing:-.015em}
.tag .gl{font-size:7.2pt;line-height:1.3;color:var(--muted);margin-top:.05in}
.tag .tf{margin-top:auto}
.tag .field{height:.3in;font-size:8.4pt}
"""


def field(label):
    return f'<div class="field"><span>{label}</span><i></i></div>'


def cert(tag):
    logo = C.logo_data_uri()
    inc = "".join(f'<span><i class="box"></i>{x}</span>' for x in
                  ["Hot sauna", "Cold plunge or cool shower", "Fresh towels", "Tea", "Snacks", "A hat to borrow"])
    return f"""<section class="cert"><div class="band"><i></i><i></i><i></i><i></i></div><div class="in">
<div class="top"><span>Gift certificate</span><img src="{logo}" alt="DIVELUX"></div>
<{tag} class="h1">A sauna evening<i>.</i></{tag}>
<p class="sub">Good for one unhurried evening of heat, steam and rest.</p>
<div class="msg">{field("A few words")}</div>
<div class="fields">{field("For")}{field("From")}{field("Good until")}</div>
<div class="inc"><b>Included</b>{inc}</div>
<div class="cf"><span>To redeem: pick a date together and bring this card.</span><span>Free printable from <a href="{C.SITE}">diveluxsaunahat.com</a></span></div>
</div></section>"""


def build():
    tags = "".join(
        f'<div class="tag"><div class="hole"><i></i></div><div class="in"><p class="ph">{C.esc(p)}</p>'
        f'{f"<p class=gl>{C.esc(g)}</p>" if g else ""}<div class="tf">{field("To")}{field("From")}</div></div></div>'
        for p, g in TAGS)
    body = f"""<main class="page">
<div class="how"><span><b>Sauna evening gift certificate</b> · two per sheet</span><span>Print at 100% on heavy paper. Cut along the dashed lines.</span></div>
<div class="certs">{cert("h1")}{cert("div")}</div>
{C.foot()}
</main>
<main class="page">
<div class="how"><span><b>Gift tags</b> · eight per sheet, 3.5 × 2.25 in</span><span>Print at 100% on heavy paper. Cut along the dashed lines and punch the hole.</span></div>
<div class="tags">{tags}</div>
{C.foot()}
</main>"""
    C.write(os.path.join(C.ROOT, SLUG, SLUG + ".html"), C.doc(TITLE, DESC, KEYWORDS, CSS, body))
    meta = dict(title="Sauna Evening Gift Certificate and Gift Tags (Printable)", subject=DESC, keywords=KEYWORDS)
    jobs = C.std_jobs(SLUG, SLUG + ".html", SLUG, meta)
    return dict(slug=SLUG, jobs=jobs, preview=dict(pdf=jobs[0]["pdf"], pages=[1, 2], dpi=75))
