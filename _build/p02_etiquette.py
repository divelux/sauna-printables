"""2. Sauna Etiquette poster for gyms and spas: branded, neutral, and an editable HTML version."""
import json
import os
import common as C

SLUG = "sauna-etiquette-poster"
TITLE = "Sauna Etiquette Poster for Gyms and Spas"
DESC = "A printable sauna etiquette poster for gyms, spas and clubs: ten short courtesies for a shared sauna. Includes a neutral version and an editable version with your venue name."
KEYWORDS = "sauna etiquette poster, gym sauna rules, spa sauna sign, sauna rules sign printable, shared sauna etiquette, sauna signage, DIVELUX"

RULES = [
    ("Shower first", "Rinse off sweat, lotion and chlorine before you come in."),
    ("Sit on a towel", "Keep your own towel between you and the bench."),
    ("Dress as posted", "Swimsuit or towel: follow the dress code of this venue."),
    ("Close the door quickly", "Every open second lets the heat out for everyone."),
    ("Check before you pour", "Water on the heater only if this venue allows it. Ask the room first."),
    ("Keep it quiet", "Low voices, short conversations. Many people come here to rest."),
    ("No phones or cameras", "Leave devices in your locker. Everyone here deserves privacy."),
    ("The bench is for sitting", "No workouts, shaving, scrubbing, or drying clothes in the sauna."),
    ("Share the space", "Make room for others. Keep bags and bottles off the benches."),
    ("Listen to your body", "Leave when you have had enough. If you feel dizzy or unwell, step out and tell staff."),
]
WATER = {
    "ask": RULES[4],
    "staff": ("Leave the heater to staff", "Only staff add water to the stones. Please do not pour anything on the heater."),
    "none": ("No water on the heater", "Please do not pour water or oils on this heater."),
}
DEFAULT_VENUE = "Please read before you enter"

CSS = """
.page{padding:.5in .55in .34in}
.band{background:#241812;color:#f6f3ee;border-radius:6px;padding:.3in .4in .36in;flex:none}
.band .row{display:flex;justify-content:space-between;align-items:center;min-height:.2in}
.venue{font-family:var(--display);font-weight:600;font-size:14pt;letter-spacing:.01em;line-height:1.15}
.band img{height:.15in;display:block}
html.nobrand .band img{display:none}
.band .main{display:grid;grid-template-columns:auto 1fr;column-gap:.4in;align-items:end;margin-top:.22in}
h1{font-weight:800;font-stretch:75%;font-size:104pt;line-height:.83;letter-spacing:-.02em;margin:0 0 0 -.04in}
h1 i{font-style:normal;color:var(--ember)}
.band .lead{font-family:var(--display);font-weight:500;font-size:14.5pt;line-height:1.28;color:#eadfd2;padding-bottom:.05in;text-wrap:balance}
.list{flex:1;display:grid;grid-template-rows:repeat(10,1fr);margin-top:.1in}
.item{display:grid;grid-template-columns:.66in 2.72in 1fr;column-gap:.1in;align-items:center;border-bottom:1px solid var(--line-2)}
.item:last-child{border-bottom:2px solid var(--ink)}
.item .n{font-family:var(--display);font-weight:700;font-stretch:75%;font-size:30pt;line-height:1;letter-spacing:-.02em;padding-left:.06in}
.item h2{font-size:16.5pt;line-height:1.1;font-weight:700;letter-spacing:-.012em}
.item p{font-size:10.6pt;line-height:1.36;color:var(--ink-2);text-wrap:balance}
.end{display:flex;justify-content:space-between;align-items:center;gap:.3in;margin:.15in 0 .15in}
.end .wish{font-family:var(--display);font-weight:700;font-size:17pt;line-height:1.1;letter-spacing:-.012em}
.end .aside{font-size:8.4pt;line-height:1.4;color:var(--muted);text-align:right;max-width:2.6in}
@media screen{
  .bar{position:sticky;top:0;z-index:5;background:#fffdf9;border-bottom:1px solid #b9afa2;margin:-18px 0 18px;padding:12px 18px;
    display:flex;flex-wrap:wrap;gap:12px 20px;align-items:flex-end;font:14px/1.3 var(--body);color:#1b1512}
  .bar label{display:flex;flex-direction:column;gap:4px;font-weight:600;font-size:12px}
  .bar input,.bar select{font:14px var(--body);padding:8px 10px;border:1px solid #6f655c;border-radius:6px;background:#fff;color:#1b1512;min-width:170px}
  .bar input{min-width:280px}
  .bar button{font:600 14px var(--body);padding:10px 16px;border:0;border-radius:6px;background:#f0762e;color:#1b1512;cursor:pointer}
  .bar button:focus-visible,.bar input:focus-visible,.bar select:focus-visible{outline:2px solid #1b1512;outline-offset:2px}
  .bar .tip{flex-basis:100%;font-size:12.5px;color:#3d332c;margin:0}
  [contenteditable]:hover{outline:1px dashed #b9afa2;outline-offset:3px}
  [contenteditable]:focus{outline:2px solid #f0762e;outline-offset:3px}
}
"""

VIEW_JS = """<script>(function(){var q=new URLSearchParams(location.search),d=document.documentElement;
if(q.get('brand')==='0')d.classList.add('nobrand');
document.addEventListener('DOMContentLoaded',function(){var v=q.get('venue');if(v)document.getElementById('venue').textContent=v;});})();</script>"""

EDIT_JS = """<script>(function(){
var WATER=%s, DEF=%s, d=document.documentElement;
function paper(a4){d.classList.toggle('a4',a4);var s=document.getElementById('pagesize');
  if(!s){s=document.createElement('style');s.id='pagesize';document.head.appendChild(s);}
  s.textContent='@page{size:'+(a4?'210mm 297mm':'8.5in 11in')+';margin:0}';}
document.addEventListener('DOMContentLoaded',function(){
  var venue=document.getElementById('venue'),name=document.getElementById('f-venue'),pp=document.getElementById('f-paper'),w=document.getElementById('f-water');
  name.addEventListener('input',function(){venue.textContent=name.value.trim()||DEF;});
  pp.addEventListener('change',function(){paper(pp.value==='a4');});
  w.addEventListener('change',function(){var r=WATER[w.value],it=document.getElementById('rule-water');
    it.querySelector('h2').textContent=r[0];it.querySelector('p').textContent=r[1];});
  document.getElementById('f-print').addEventListener('click',function(){window.print();});
  if(d.classList.contains('a4'))pp.value='a4';
});})();</script>"""

BAR = """<form class="bar screen-only" onsubmit="return false" aria-label="Poster settings">
<label for="f-venue">Venue name<input id="f-venue" type="text" maxlength="48" placeholder="e.g. Northside Athletic Club" autocomplete="off"></label>
<label for="f-water">Water on the heater<select id="f-water"><option value="ask">Allowed: ask the room first</option><option value="staff">Staff only</option><option value="none">Not allowed</option></select></label>
<label for="f-paper">Paper<select id="f-paper"><option value="letter">US Letter</option><option value="a4">A4</option></select></label>
<button id="f-print" type="button">Print or save as PDF</button>
<p class="tip">Type your venue name, pick the heater rule and paper size, then print. You can also click any rule on the poster and rewrite it. In the print dialog choose the same paper size, scale 100%, margins "None", and turn on "Background graphics".</p>
</form>"""

EDITING_MD = """# How to make the poster yours

`sauna-etiquette-poster-editable.html` is a single file. It works offline in Chrome, Edge, Safari or Firefox. Nothing is uploaded anywhere.

1. Open the file in your browser (double-click it).
2. Type your venue name in **Venue name**. It replaces the line at the top of the poster.
3. Pick the rule for **Water on the heater**: allowed if the room agrees, staff only, or not allowed.
4. Pick the **Paper** size: US Letter or A4.
5. Optional: click any rule on the poster and rewrite it in your own words. Keep each line short so the poster stays on one page.
6. Press **Print or save as PDF**. In the print dialog set:
   - Paper size: the same size you picked in step 4
   - Scale: 100% (actual size)
   - Margins: None
   - Background graphics: on (this prints the dark title band)
7. Print, or choose "Save as PDF" as the destination to keep a file.

Tips

- For a larger wall sign, send the saved PDF to a print shop and ask for 11 x 17 in (US) or A3; the layout scales cleanly.
- Laminate the print or put it in a frame outside the hot room. Paper and tape do not last inside a sauna.
- The poster is general information, not medical advice. Your own posted safety rules and local regulations come first.

The small line at the bottom ("Free to print and share - DIVELUX wool sauna hats - diveluxsaunahat.com") is the credit required by the CC BY 4.0 license. Please keep it.
"""


def page(editable):
    items = []
    for i, (t, b) in enumerate(RULES, 1):
        ce = ' contenteditable="true" spellcheck="false"' if editable else ""
        rid = ' id="rule-water"' if i == 5 else ""
        items.append(f'<li class="item"{rid}><span class="n num">{i:02d}</span><h2{ce}>{C.esc(t)}</h2><p{ce}>{C.esc(b)}</p></li>')
    logo = "data:image/png;base64," + C.b64("/root/divelux/brand/logo-light.png")
    return f"""<main class="page">
<header class="band"><div class="row"><span class="venue" id="venue">{DEFAULT_VENUE}</span><img src="{logo}" alt="DIVELUX"></div>
<div class="main"><h1>Sauna<br>etiquette<i>.</i></h1><p class="lead">Ten courtesies that keep this room calm, clean and hot for everyone.</p></div></header>
<ol class="list">{''.join(items)}</ol>
<div class="end"><p class="wish">Thank you for sharing the heat kindly.</p>
<p class="aside">General information, not medical advice. Posted venue rules always come first.</p></div>
{C.foot()}
</main>"""


def build():
    d = os.path.join(C.ROOT, SLUG)
    C.write(os.path.join(d, SLUG + ".html"), C.doc(TITLE, DESC, KEYWORDS, CSS, page(False), head_extra=VIEW_JS))
    edit_js = EDIT_JS % (json.dumps(WATER), json.dumps(DEFAULT_VENUE))
    C.write(os.path.join(d, SLUG + "-editable.html"),
            C.doc(TITLE + " (editable)", DESC, KEYWORDS, CSS, BAR + page(True), head_extra=edit_js, html_class="nobrand"))
    C.write(os.path.join(d, "EDITING.md"), EDITING_MD)
    meta = dict(title="Sauna Etiquette: A Printable Poster for Gyms and Spas", subject=DESC, keywords=KEYWORDS)
    jobs = C.std_jobs(SLUG, SLUG + ".html", SLUG, meta)
    jobs += C.std_jobs(SLUG, SLUG + ".html", SLUG + "-neutral", meta, extra_query="brand=0")
    return dict(slug=SLUG, jobs=jobs, preview=dict(pdf=jobs[0]["pdf"]))
