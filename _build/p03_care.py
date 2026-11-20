"""3. Wool Sauna Hat Care card: two cards per sheet (Letter, A4) and a single 4 x 6 in card."""
import os
import common as C

SLUG = "wool-sauna-hat-care-card"
TITLE = "Wool Sauna Hat Care Card"
DESC = "A printable care card for a wool felt sauna hat: wear it dry, hand wash in cool room-temperature water, squeeze, air dry. Two cards per sheet plus a 4 x 6 in card."
KEYWORDS = "wool sauna hat care, how to wash a sauna hat, felt hat care card, wool felt care instructions, sauna hat washing, banya hat care, DIVELUX"

CSS = """
html.p46{--pw:4in;--ph:6in}
.single{display:none}
html.p46 .single{display:flex;padding:0}
html.p46 .sheet{display:none}
.sheet{padding:.26in .4in .3in;background:#fff}
.sheet .how{display:flex;justify-content:space-between;font-size:7.6pt;color:var(--muted);flex:none}
.sheet .how b{color:var(--ink);font-weight:600}
.sheet .cards{flex:1;display:flex;justify-content:center;align-items:center;gap:.5in}
.sheet .cut{outline:1px dashed #8d8378;outline-offset:0;zoom:1.18}
.card{width:4in;height:6in;background:var(--paper);padding:.25in .27in .15in;display:flex;flex-direction:column;position:relative;overflow:hidden}
.card .top{display:flex;justify-content:space-between;align-items:center}
.card .top img{height:.105in;display:block}
.card .top span{font-size:5.8pt;letter-spacing:.16em;text-transform:uppercase;font-weight:600;color:var(--muted)}
.card h1,.card .h1{font-family:var(--display);font-weight:800;font-stretch:75%;font-size:42pt;line-height:.86;letter-spacing:-.02em;margin:.14in 0 .11in -.015in}
.card .ladder{height:.06in}
.card h2,.card .h2{font-family:var(--body);font-size:5.9pt;letter-spacing:.16em;text-transform:uppercase;font-weight:600;color:var(--muted);margin:.14in 0 .06in}
.card .wear li{font-size:8pt;line-height:1.38;color:var(--ink-2);padding:.045in 0;border-top:1px solid var(--line)}
.card .wear li:first-child{border-top:0;padding-top:0}
.card .wear b,.card .wash b{font-family:var(--display);font-weight:700;font-size:10pt;color:var(--ink);letter-spacing:-.005em}
.card .wash{counter-reset:w}
.card .wash li{counter-increment:w;display:grid;grid-template-columns:.23in 1fr;font-size:8pt;line-height:1.38;color:var(--ink-2);padding:.045in 0;border-top:1px solid var(--line)}
.card .wash li:first-child{border-top:0;padding-top:0}
.card .wash li::before{content:counter(w);font-family:var(--display);font-weight:700;font-stretch:75%;font-size:18pt;line-height:.95;color:var(--ink)}
.card .wash b{display:block;line-height:1.2}
.card .never{margin-top:auto;border-top:1.5px solid var(--ink);padding-top:.07in;display:grid;grid-template-columns:auto 1fr 1fr 1fr;column-gap:.1in;align-items:center}
.card .never .lab{font-family:var(--display);font-weight:800;font-stretch:75%;font-size:17pt;line-height:.9;letter-spacing:-.01em}
.card .never div{display:flex;align-items:center;gap:.05in;font-size:6.6pt;line-height:1.2;font-weight:600;color:var(--ink)}
.card .never svg{width:.3in;height:.3in;flex:none}
.card .cfoot{margin-top:.08in;padding-top:.045in;border-top:1px solid var(--line-2);font-size:4.9pt;line-height:1.25;color:var(--muted);text-align:center;white-space:nowrap}
.card .cfoot a{color:var(--ink);text-decoration:none;font-weight:600}
.card .cfoot b{color:var(--ink);font-weight:600}
"""

HEAD_JS = ("<script>(function(){if((new URLSearchParams(location.search).get('paper')||'').toLowerCase()==='4x6'){"
           "var d=document.documentElement;d.classList.add('p46');var s=document.createElement('style');"
           "s.textContent='@page{size:4in 6in;margin:0}';document.head.appendChild(s)}})();</script>")

STROKE = 'fill="none" stroke="#1b1512" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"'
NO = '<line x1="3.2" y1="20.8" x2="20.8" y2="3.2" stroke="#f0762e" stroke-width="2.2" stroke-linecap="round"/>'
ICON_WASHER = (f'<svg viewBox="0 0 24 24" aria-hidden="true"><g {STROKE}><rect x="4" y="2.5" width="16" height="19" rx="1.6"/>'
               f'<circle cx="12" cy="13.2" r="4.6"/><line x1="6.6" y1="5.6" x2="9.4" y2="5.6"/></g>{NO}</svg>')
ICON_DRYER = (f'<svg viewBox="0 0 24 24" aria-hidden="true"><g {STROKE}><rect x="3.5" y="3.5" width="17" height="17" rx="1.2"/>'
              f'<circle cx="12" cy="12" r="5.6"/><circle cx="12" cy="12" r="1" fill="#1b1512"/></g>{NO}</svg>')
ICON_HOT = (f'<svg viewBox="0 0 24 24" aria-hidden="true"><g {STROKE}><path d="M4 13.5h16l-1.6 7H5.6z"/>'
            f'<path d="M8.5 10c-1.2-1.4 1.2-2.4 0-3.8M12 10c-1.2-1.4 1.2-2.4 0-3.8M15.5 10c-1.2-1.4 1.2-2.4 0-3.8"/></g>{NO}</svg>')


def card(tag_h1="div"):
    logo = C.logo_data_uri()
    return f"""<div class="card fit">
<div class="top"><img src="{logo}" alt="DIVELUX"><span>Care card</span></div>
<{tag_h1} class="h1">Wool sauna<br>hat care</{tag_h1}>
<div class="ladder"><i></i><i></i><i></i><i></i></div>
<div class="h2">In the sauna</div>
<ul class="wear">
<li><b>Wear it dry.</b> Put it on dry, before you step into the heat.</li>
<li><b>Loose is good.</b> Roomy is a plus. Too big? Fold the edge up.</li>
<li><b>Air it out after.</b> Hang it by the loop until it is fully dry.</li>
</ul>
<div class="h2">Washing, only when it needs it</div>
<ol class="wash">
<li><span><b>Hand wash only</b>In cool, room-temperature water, about 20–24 °C / 68–75 °F. Never warm or hot.</span></li>
<li><span><b>A little mild soap</b>Press the felt gently. Do not scrub hard.</span></li>
<li><span><b>Squeeze, do not wring</b>Press the water out between your palms or in a towel.</span></li>
<li><span><b>Air dry</b>Reshape by hand. Dry in open air, away from heaters.</span></li>
</ol>
<div class="never"><span class="lab">Never</span><div>{ICON_WASHER}<span>Washing machine</span></div><div>{ICON_DRYER}<span>Dryer</span></div><div>{ICON_HOT}<span>Warm or hot water</span></div></div>
<div class="cfoot">Free to print and share — <b>DIVELUX</b> wool sauna hats — <a href="{C.SITE}">diveluxsaunahat.com</a></div>
</div>"""


def build():
    d = os.path.join(C.ROOT, SLUG)
    body = f"""<main class="page sheet">
<div class="how"><span><b>Wool Sauna Hat Care card</b> · two per sheet</span><span>Print at 100% (actual size) on heavy paper. Cut along the dashed lines.</span></div>
<div class="cards"><div class="cut">{card("h1")}</div><div class="cut">{card()}</div></div>
{C.foot()}
</main>
<main class="page single">{card()}</main>"""
    C.write(os.path.join(d, SLUG + ".html"), C.doc(TITLE, DESC, KEYWORDS, CSS, body, land=True, head_extra=HEAD_JS))
    meta = dict(title="Wool Sauna Hat Care Card", subject=DESC, keywords=KEYWORDS)
    jobs = C.std_jobs(SLUG, SLUG + ".html", SLUG, meta, land=True)
    jobs.append(dict(html=os.path.join(d, SLUG + ".html"), query="paper=4x6", pdf=os.path.join(d, SLUG + "-4x6.pdf"),
                     width="4in", height="6in", meta=meta))
    return dict(slug=SLUG, jobs=jobs, preview=dict(pdf=jobs[0]["pdf"]))
