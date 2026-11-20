"""Shared pieces for the DIVELUX printables: fonts, design tokens, page shell, footer.

Every product module exposes build() -> dict(slug, jobs=[...], pages_for_preview=...).
HTML sources are self-contained (fonts embedded) and switch paper size with ?paper=a4.
"""
import base64
import html
import os
import re

ROOT = "/root/divelux/freebies/printables"
B = os.path.join(ROOT, "_build")
SITE = "https://diveluxsaunahat.com"
TOOLS = "https://diveluxsaunahat.com/pages/sauna-tools"
FOOT_TEXT = "Free to print and share — DIVELUX wool sauna hats — diveluxsaunahat.com"

LETTER = ("8.5in", "11in")
A4 = ("210mm", "297mm")
LETTER_L = ("11in", "8.5in")
A4_L = ("297mm", "210mm")


def esc(s):
    return html.escape(str(s), quote=True)


def b64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


def _face(fam, name, weight, extra=""):
    p = os.path.join(B, "fonts", name + ".woff2")
    rng = open(p + ".range").read().strip()
    return (f'@font-face{{font-family:"{fam}";src:url(data:font/woff2;base64,{b64(p)}) format("woff2");'
            f"font-weight:{weight};{extra}font-display:block;unicode-range:{rng}}}")


def font_css(ext=False):
    """Bricolage Grotesque (variable: opsz, wght, wdth) + Inter (variable wght), SIL OFL 1.1.
    ext=True adds Latin Extended and Cyrillic (Inter only) for the multilingual sheets."""
    out = [
        _face("Bricolage Grotesque", "BricolageGrotesque-latin", "200 800", "font-stretch:75% 100%;"),
        _face("Inter", "Inter-latin", "100 900"),
    ]
    if ext:
        out += [
            _face("Bricolage Grotesque", "BricolageGrotesque-latin-ext", "200 800", "font-stretch:75% 100%;"),
            _face("Inter", "Inter-latin-ext", "100 900"),
            _face("Inter", "Inter-cyrillic", "100 900"),
        ]
    return "\n".join(out)


BASE_CSS = """
:root{--paper:#f6f3ee;--paper-2:#ede8df;--card:#fffdf9;--ink:#1b1512;--ink-2:#3d332c;--muted:#6f655c;--line:#dcd4c8;
--line-2:#b9afa2;--wood:#c99b6c;--ember:#f0762e;--t1:#f0a877;--t2:#f5c7a0;--t3:#f8dfc6;--t4:#fbf1e5;--r:6px;
--display:"Bricolage Grotesque","Arial Narrow",Arial,sans-serif;--body:"Inter",Arial,sans-serif;--pw:8.5in;--ph:11in}
html.a4{--pw:210mm;--ph:297mm}
html.land{--pw:11in;--ph:8.5in}
html.land.a4{--pw:297mm;--ph:210mm}
@page{size:8.5in 11in;margin:0}
*{box-sizing:border-box}
html,body{margin:0;padding:0}
body{font-family:var(--body);color:var(--ink);font-size:10pt;line-height:1.4;-webkit-print-color-adjust:exact;print-color-adjust:exact}
h1,h2,h3,p,ul,ol,figure{margin:0;padding:0}
ul,ol{list-style:none}
h1,h2,h3,.d{font-family:var(--display);font-optical-sizing:auto}
a{color:inherit}
.page{position:relative;width:var(--pw);height:var(--ph);padding:.55in .6in .34in;display:flex;flex-direction:column;
background:var(--paper);overflow:hidden;break-after:page;page-break-after:always}
.page:last-of-type{break-after:auto;page-break-after:auto}
.page.white{background:#fff}
.foot{margin-top:auto;display:flex;justify-content:space-between;align-items:baseline;gap:.25in;padding-top:.085in;
border-top:1px solid var(--line-2);font-size:7pt;line-height:1.3;color:var(--muted);flex:none}
.foot a{color:var(--ink);text-decoration:none;font-weight:600}
.foot b{font-weight:600;color:var(--ink)}
.foot .free{white-space:nowrap}
.foot .dot{display:inline-block;width:.07in;height:.07in;border-radius:50%;background:var(--ember);margin-right:.06in}
.foot .note{text-align:right}
.ladder{display:grid;grid-template-columns:repeat(4,1fr);height:.13in;flex:none}
.ladder i{display:block}.ladder i:nth-child(1){background:var(--t4)}.ladder i:nth-child(2){background:var(--t3)}
.ladder i:nth-child(3){background:var(--t2)}.ladder i:nth-child(4){background:var(--t1)}
.kicker{font-family:var(--display);font-weight:600;font-size:11pt;color:var(--ink-2);letter-spacing:.01em}
.num{font-variant-numeric:tabular-nums lining-nums}
nw-r{white-space:nowrap}
@media screen{
  html{background:#cfc9c0}
  body{padding:18px 0}
  .page{margin:0 auto 18px;box-shadow:0 2px 14px rgba(27,21,18,.25)}
}
@media print{.screen-only{display:none!important}}
"""

PAPER_JS = ("<script>(function(){var d=document.documentElement,p=(new URLSearchParams(location.search).get('paper')||'')"
            ".toLowerCase();if(p==='a4'){d.classList.add('a4');var s=document.createElement('style');"
            "s.textContent='@page{size:'+(d.classList.contains('land')?'297mm 210mm':'210mm 297mm')+';margin:0}';"
            "document.head.appendChild(s)}})();</script>")


def foot(note=""):
    """Footer line required on every sheet; the site name is a live link in the PDF."""
    n = f'<span class="note">{note}</span>' if note else ""
    return (f'<footer class="foot"><span class="free"><i class="dot"></i>Free to print and share — '
            f'<b>DIVELUX</b> wool sauna hats — <a href="{SITE}">diveluxsaunahat.com</a></span>{n}</footer>')


def _nowrap(body):
    """Keep '158–212 °F' and '100 °C' on one line. Only text nodes are touched: never attributes, never SVG."""
    parts = re.split(r"(<svg\b.*?</svg>|<script\b.*?</script>|<[^>]+>)", body, flags=re.S)
    for i in range(0, len(parts), 2):
        p = re.sub(r"(\d+(?:–\d+)?) (°[CF])", r"<nw-r>\1&nbsp;\2</nw-r>", parts[i])
        parts[i] = re.sub(r"(?<![\d>;])(\d+–\d+)(?![\d&])", r"<nw-r>\1</nw-r>", p)
    return "".join(parts)


def doc(title, desc, keywords, css, body, ext=False, land=False, head_extra="", html_class=""):
    body = _nowrap(body)
    cls = " ".join(c for c in (("land" if land else ""), html_class) if c)
    land_css = "@page{size:11in 8.5in;margin:0}" if land else ""
    return f"""<!doctype html>
<html lang="en-US"{f' class="{cls}"' if cls else ''}><head><meta charset="utf-8">
<title>{esc(title)}</title>
<meta name="author" content="DIVELUX">
<meta name="description" content="{esc(desc)}">
<meta name="keywords" content="{esc(keywords)}">
<meta name="viewport" content="width=device-width, initial-scale=1">
<!-- Print: US Letter by default. Add ?paper=a4 to the address for A4. Print at 100% (actual size), no margins. -->
<style>
{BASE_CSS}{land_css}
{css}
</style>
<style>/* Fonts: Bricolage Grotesque and Inter, SIL Open Font License 1.1 */
{font_css(ext)}
</style>
{PAPER_JS}{head_extra}
</head><body>
{body}
</body></html>
"""


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def std_jobs(slug, htmlname, base, meta, land=False, extra_query=""):
    """Letter + A4 jobs for one HTML source."""
    d = os.path.join(ROOT, slug)
    q = ("&" + extra_query) if extra_query else ""
    L, A = (LETTER_L, A4_L) if land else (LETTER, A4)
    return [
        dict(html=os.path.join(d, htmlname), query="paper=letter" + q, pdf=os.path.join(d, base + "-letter.pdf"),
             width=L[0], height=L[1], meta=meta),
        dict(html=os.path.join(d, htmlname), query="paper=a4" + q, pdf=os.path.join(d, base + "-a4.pdf"),
             width=A[0], height=A[1], meta=meta),
    ]


def logo_data_uri():
    return "data:image/png;base64," + b64("/root/divelux/brand/logo-dark.png")
