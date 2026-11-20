"""Shared CSS and small HTML helpers for the wave 2 printables (p12 and up)."""
import common as C

CSS = """
.head{display:grid;grid-template-columns:auto 1fr;column-gap:.42in;align-items:end;flex:none}
h1{font-weight:800;font-stretch:75%;font-size:76pt;line-height:.84;letter-spacing:-.022em;margin:.08in 0 0 -.035in;white-space:nowrap}
h1 i,.h1 i{font-style:normal;color:var(--ember)}
.lead{font-family:var(--display);font-weight:500;font-size:13pt;line-height:1.3;color:var(--ink-2);padding-bottom:.06in;text-wrap:balance}
.ph{border-bottom:2px solid var(--ink);padding-bottom:.11in;display:flex;justify-content:space-between;align-items:flex-end;gap:.3in;flex:none}
.ph h2{font-weight:800;font-stretch:75%;font-size:40pt;line-height:.9;letter-spacing:-.018em;white-space:nowrap}
.ph p{font-size:9pt;line-height:1.4;color:var(--muted);max-width:3.3in;text-align:right;text-wrap:balance}
.box{display:inline-block;width:.14in;height:.14in;border:1.2px solid var(--ink-2);border-radius:2px;background:#fffdf9;flex:none}
.cl li{display:grid;grid-template-columns:.25in 1fr;font-size:9.6pt;line-height:1.36;color:var(--ink-2);padding:.047in 0;border-bottom:1px solid var(--line)}
.cl li:last-child{border-bottom:0}
.cl li .box{margin-top:.02in}
.cl li b{color:var(--ink);font-weight:600}
.sec{border-top:2px solid var(--ink);display:flex;flex-direction:column;min-height:0}
.sec>header{display:flex;justify-content:space-between;align-items:baseline;gap:.1in;padding:.065in .1in .055in;margin-bottom:.03in;background:var(--t3)}
.sec.s1>header{background:var(--t1)}.sec.s2>header{background:var(--t2)}.sec.s4>header{background:var(--t4)}
.sec h2{font-weight:800;font-stretch:75%;font-size:21pt;line-height:1;letter-spacing:-.012em}
.sec>header span{font-size:8.2pt;color:var(--ink-2);white-space:nowrap}
.field{display:flex;align-items:flex-end;gap:.08in;font-size:9pt;color:var(--ink-2);height:.36in}
.field span{white-space:nowrap;padding-bottom:.03in}
.field i{flex:1;border-bottom:1px solid var(--ink-2);display:block;height:100%}
.fine{font-size:7.5pt;line-height:1.42;color:var(--muted)}
.fine a{color:var(--ink-2)}
.how{display:flex;justify-content:space-between;gap:.3in;font-size:7.6pt;color:var(--muted);flex:none}
.how b{color:var(--ink);font-weight:600}
.lines{flex:1;display:flex;flex-direction:column;min-height:0}
.lines i{flex:1;border-bottom:1px solid var(--line-2);display:block}
table.log{width:100%;border-collapse:collapse;table-layout:fixed}
table.log th{font-weight:600;font-size:8pt;text-align:left;color:#fff;background:#2a1b13;padding:.07in .09in;line-height:1.15}
table.log th small{display:block;font-weight:400;font-size:6.8pt;opacity:.85}
table.log td{border-bottom:1px solid var(--line-2);border-right:1px solid var(--line);font-size:8.6pt;color:var(--ink-2);padding:0 .09in}
table.log td:last-child{border-right:0}
table.log tbody tr:nth-child(even) td{background:#f8f5f0}
.always{display:grid;grid-template-columns:repeat(3,1fr);column-gap:.3in;border-top:2px solid var(--ink);padding-top:.1in;flex:none}
.always b{display:block;font-family:var(--display);font-weight:700;font-size:12.5pt;line-height:1.15;letter-spacing:-.008em;margin-bottom:.03in}
.always p{font-size:8.6pt;line-height:1.4;color:var(--ink-2)}
"""


def field(label, style=""):
    st = f' style="{style}"' if style else ""
    return f'<div class="field"{st}><span>{label}</span><i></i></div>'


def checks(items, cls=""):
    return (f'<ul class="cl {cls}">' + "".join(f'<li><i class="box"></i><span>{x}</span></li>' for x in items) + "</ul>")


def sec(title, sub, inner, n=3):
    return (f'<section class="sec s{n}"><header><h2>{title}</h2><span>{sub}</span></header>{inner}</section>')


def ph(title, note):
    return f'<header class="ph"><h2>{title}</h2><p>{note}</p></header>'


def lines(n):
    return '<div class="lines">' + "<i></i>" * n + "</div>"


def cfoot():
    """Credit line for small cut-out pieces (cards, invitations, signs)."""
    return (f'<div class="cfoot">Free to print and share — <b>DIVELUX</b> wool sauna hats — '
            f'<a href="{C.SITE}">diveluxsaunahat.com</a></div>')


def icon(name, extra=""):
    """Inline one of the DIVELUX sauna icons (24 px grid, CC BY 4.0, ../icons/svg)."""
    import re
    s = open(f"/root/divelux/freebies/icons/svg/{name}.svg").read()
    inner = re.sub(r"<title>.*?</title>", "", s[s.index(">") + 1:s.rindex("</svg>")])
    return (f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" '
            f'stroke-linejoin="round" aria-hidden="true"{extra}>{inner}</svg>')
