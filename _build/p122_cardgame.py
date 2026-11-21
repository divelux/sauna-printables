"""122. Good Steam: an original printable card game for the sauna lounge (2-6 players, 15-20 minutes).
60 game cards + 3 quick-rule cards (2.5 x 3.5 in), nine per sheet with crop marks, backs mirrored for long-edge duplex.
Page 1 rules, page 2 printing + score sheet. Rules tested with ../sauna-card-game/simulation/simulate.py.
Played in the lounge, never in the hot room; nothing in the game rewards time in the heat. No stakes, no drinking."""
import base64
import os
import re

import common as C
import w2

SLUG = "sauna-card-game"
TITLE = "Good Steam: a card game for the sauna lounge"
DESC = ("Good Steam is a free printable card game for 2–6 players and 15–20 minutes. Host sauna rounds, let friends join in "
        "and score the most points. 60 cards, rules and a score sheet.")
KEYWORDS = ("sauna card game, printable card game, sauna party game, card game for groups, family card game, "
            "sauna night, spa party game, print and play, free printable game, DIVELUX")
NAME = "Good Steam"
PAGES = 16
ILL = "/root/divelux/freebies/gfx/sauna-illustrations/svg/"

# ritual: (name, role, colour, illustration, corner icon)
RIT = {
    "stones": ("Stones", "Heat", "#f2b48a", "sauna-stove", "sauna-stove"),
    "ladle": ("Ladle", "Steam", "#e9d3ad", "bucket-and-ladle", "bucket-ladle"),
    "birch": ("Birch", "Whisk", "#cbd7bb", "birch-whisk", "birch-whisk"),
    "lake": ("Lake", "Cool-down", "#bcd2d8", "lakeside-sauna", "lake-dock"),
    "hat": ("Wool Hat", "Wild card", "#d8d3cb", "bell-hat-on-peg", "sauna-hat"),
}
HINT = {
    "stones": "Heat for the round.",
    "ladle": "Water on the stones.",
    "birch": "Leafy whisk, soft steam.",
    "lake": "Every round needs one. Its number is the number guests match.",
}
CARDS = [(r, v) for r in ("stones", "ladle", "birch", "lake") for v in range(1, 8) for _ in range(2)] + [("hat", 0)] * 4
assert len(CARDS) == 60

CSS = w2.CSS + """
.page{padding:.48in .58in .34in}
h1{font-size:70pt}
.sheet{padding:0;background:#fff;align-items:center;justify-content:center}
.grid{position:relative;display:grid;grid-template-columns:repeat(3,2.5in);grid-template-rows:repeat(3,3.5in);flex:none}
.crop{position:absolute;background:#1b1512}
.card{position:relative;overflow:hidden;background:#fffdf9;border:.5px solid #e3ddd3}
.card .pan{position:absolute;left:.13in;right:.13in;top:.13in;height:2.36in;border-radius:6px}
.card .art{position:absolute;left:.5in;right:.5in;top:.42in;height:1.5in;background-size:contain;background-repeat:no-repeat;background-position:center}
.idx{position:absolute;width:.42in;display:flex;flex-direction:column;align-items:center;gap:.03in}
.idx b{font-family:var(--display);font-weight:800;font-stretch:75%;font-size:27pt;line-height:.9;color:#1b1512;font-variant-numeric:lining-nums}
.idx svg{width:.22in;height:.22in;color:#1b1512}
.idx.tl{left:.17in;top:.2in}
.idx.br{right:.17in;bottom:.2in;transform:rotate(180deg)}
.card .role{position:absolute;right:.24in;top:.22in;font-size:6pt;letter-spacing:.16em;text-transform:uppercase;font-weight:600;color:#1b1512}
.card .nm{position:absolute;left:.2in;top:2.56in;font-family:var(--display);font-weight:800;font-stretch:75%;font-size:21pt;line-height:.92;letter-spacing:-.01em}
.card .ht{position:absolute;left:.2in;right:.62in;top:2.9in;font-size:6.8pt;line-height:1.3;color:var(--ink-2)}
.card.hat .pan{height:1.9in}
.card.hat .art{top:.32in;height:1.32in}
.card.hat .nm{top:2.12in}
.card.hat .ht{top:2.44in;right:.2in;font-size:7.2pt;line-height:1.34}
.card.hat .ht b{color:var(--ink)}
.card .cr{position:absolute;left:.2in;bottom:.1in;font-size:5pt;color:var(--muted)}
.card .cr a{color:var(--ink);text-decoration:none;font-weight:600}
.ref{padding:.18in .2in .1in;display:flex;flex-direction:column}
.ref h2{font-family:var(--display);font-weight:800;font-stretch:75%;font-size:17pt;line-height:.95;margin:0 0 .06in}
.ref h2 i{font-style:normal;color:var(--ember)}
.ref dl{margin:0}
.ref dt{font-family:var(--display);font-weight:700;font-size:8.6pt;margin-top:.05in;border-top:1px solid var(--line);padding-top:.04in}
.ref dd{margin:0;font-size:6.6pt;line-height:1.32;color:var(--ink-2)}
.ref .cr{position:static;margin-top:auto}
.back{border:none}
.back .frame{position:absolute;inset:.16in;border-radius:6px;background:#f5c7a0;overflow:hidden}
.back .frame svg.pat{position:absolute;inset:0;width:100%;height:100%}
.back .medal{position:absolute;left:50%;top:50%;width:1.62in;height:1.62in;margin:-.81in 0 0 -.81in;border-radius:50%;background:#fffdf9;
display:flex;flex-direction:column;align-items:center;justify-content:center;gap:.03in;border:2px solid #1b1512}
.back .medal svg{width:.46in;height:.46in;color:#1b1512}
.back .medal .t{font-family:var(--display);font-weight:800;font-stretch:75%;font-size:19pt;line-height:.86;text-align:center;letter-spacing:-.01em}
.back .medal .t i{font-style:normal;color:var(--ember)}
.back .s{position:absolute;bottom:.05in;left:0;right:0;text-align:center;font-size:5.4pt;color:#3d332c}
.back .s a{color:#1b1512;text-decoration:none;font-weight:600}
/* rules page */
.cols{display:grid;grid-template-columns:1fr 1fr;column-gap:.32in;margin-top:.14in;flex:1;min-height:0}
.col{display:flex;flex-direction:column;gap:.1in;min-height:0}
.r h3{font-family:var(--display);font-weight:800;font-stretch:75%;font-size:17pt;line-height:1;letter-spacing:-.01em;border-top:2px solid var(--ink);padding-top:.05in;margin-bottom:.03in}
.r p,.r li{font-size:8.5pt;line-height:1.38;color:var(--ink-2)}
.r p+p{margin-top:.04in}
.r b{color:var(--ink);font-weight:600}
.r ol{counter-reset:s}
.r ol li{counter-increment:s;display:grid;grid-template-columns:.2in 1fr;padding:.018in 0}
.r ol li::before{content:counter(s);font-family:var(--display);font-weight:700;color:var(--ink)}
.r ul li{position:relative;padding:.016in 0 .016in .13in}
.r ul li::before{content:"";position:absolute;left:.01in;top:.075in;width:.045in;height:.045in;border-radius:50%;background:var(--ink)}
.opt{display:grid;grid-template-columns:.3in 1fr;column-gap:.06in;margin-top:.05in}
.opt>b{display:flex;align-items:center;justify-content:center;width:.3in;height:.3in;border-radius:6px;background:var(--t2);font-family:var(--display);font-weight:800;font-size:13pt;color:var(--ink)}
.opt>div p:first-child b{font-family:var(--display);font-weight:700;font-size:10.5pt}
.deck{display:grid;grid-template-columns:repeat(5,1fr);gap:.06in;margin-top:.05in}
.deck div{border-radius:6px;padding:.05in .06in .05in;display:flex;flex-direction:column;align-items:flex-start;gap:.02in}
.deck svg{width:.22in;height:.22in;color:#1b1512}
.deck b{font-family:var(--display);font-weight:700;font-size:9.4pt;line-height:1.05;color:var(--ink)}
.deck span{font-size:6.9pt;line-height:1.25;color:var(--ink-2)}
.ex{display:flex;gap:.05in;margin:.06in 0 .05in}
.mini{width:.5in;height:.7in;border-radius:4px;border:1px solid var(--line-2);background:#fffdf9;position:relative;overflow:hidden;flex:none}
.mini i{position:absolute;inset:.04in .04in .2in;border-radius:3px}
.mini b{position:absolute;left:.06in;top:.05in;font-family:var(--display);font-weight:800;font-stretch:75%;font-size:12pt;line-height:1}
.mini svg{position:absolute;right:.05in;top:.07in;width:.16in;height:.16in;color:#1b1512}
.mini span{position:absolute;left:.05in;bottom:.04in;font-size:5.6pt;font-weight:600;color:var(--ink)}
.mini.g{border-style:dashed}
.ex .plus{align-self:center;font-family:var(--display);font-weight:700;font-size:12pt;color:var(--muted);padding:0 .02in}
.calc{font-size:8.3pt;line-height:1.38;color:var(--ink-2)}
.calc .num{font-weight:600;color:var(--ink)}
.safe{background:var(--paper-2);border-radius:6px;padding:.08in .12in;font-size:8.1pt;line-height:1.38;color:var(--ink-2);flex:none}
.safe b{color:var(--ink)}
/* score sheet */
table.sc{width:100%;border-collapse:collapse;table-layout:fixed;margin-top:.12in;flex:none}
table.sc th,table.sc td{border:1px solid var(--line-2);font-size:8.2pt;padding:0 .07in;text-align:left;color:var(--ink-2)}
table.sc th{background:#2a1b13;color:#fff;font-weight:600;height:.3in}
table.sc td:first-child{width:1.25in;font-weight:600;color:var(--ink);background:var(--paper-2)}
table.sc tr.nm td{height:.34in}
table.sc tr.st td{background:#fbf1e5;height:.28in}
table.sc tr.tot td{height:.36in;border-top:2px solid var(--ink)}
table.sc tr.tot td:first-child{font-family:var(--display);font-weight:800;font-size:12pt}
table.sc tbody tr.rw td{height:.26in}
table.sc tbody tr.rw:nth-child(even) td:not(:first-child){background:#faf7f2}
.prn{display:grid;grid-template-columns:1.15fr 1fr;column-gap:.32in;margin-top:.14in;flex:none}
.prn .r ol li{font-size:8.2pt}
.sim{font-size:8pt;line-height:1.4;color:var(--ink-2)}
.sim b{color:var(--ink)}
"""


def _svg_uri(path):
    s = open(path).read()
    s = re.sub(r"<title>.*?</title>", "", s)
    return "data:image/svg+xml;base64," + base64.b64encode(s.encode()).decode()


ART_CSS = "".join(f".a-{k}{{background-image:url({_svg_uri(ILL + v[3] + '.svg')})}}" for k, v in RIT.items())


def icon(r):
    return w2.icon(RIT[r][4])


def crops():
    o = []
    L, gap, t = .2, .05, .006
    for k in range(4):
        x = k * 2.5
        o.append(f'<i class="crop" data-bleed style="left:{x - t / 2:.3f}in;top:{-gap - L:.3f}in;width:{t}in;height:{L}in"></i>')
        o.append(f'<i class="crop" data-bleed style="left:{x - t / 2:.3f}in;top:{10.5 + gap:.3f}in;width:{t}in;height:{L}in"></i>')
        y = k * 3.5
        o.append(f'<i class="crop" data-bleed style="top:{y - t / 2:.3f}in;left:{-gap - L:.3f}in;height:{t}in;width:{L}in"></i>')
        o.append(f'<i class="crop" data-bleed style="top:{y - t / 2:.3f}in;left:{7.5 + gap:.3f}in;height:{t}in;width:{L}in"></i>')
    return "".join(o)


CR = f'<div class="cr"><b style="color:var(--ink)">{NAME}</b> · DIVELUX · <a href="{C.SITE}">diveluxsaunahat.com</a></div>'


def front(card):
    r, v = card
    name, role, col, _, _ = RIT[r]
    if r == "hat":
        num = ""
        ht = ("<b>Wild.</b> Stands in for a Stones, Ladle or Birch card in your round. It counts 0. It can never be the Lake."
              "<br><b>As a guest</b> it joins any round and scores the Lake’s number.")
    else:
        num = str(v)
        ht = C.esc(HINT[r])
    ix = f'<b>{num}</b>{icon(r)}' if num else icon(r)
    return f"""<div class="card {r}"><div class="pan" style="background:{col}"></div><div class="art a-{r}"></div>
<div class="idx tl">{ix}</div><div class="role">{C.esc(role)}</div>
<div class="nm">{C.esc(name)}</div><div class="ht">{ht}</div><div class="idx br">{ix}</div>{CR}</div>"""


def ref_card():
    return f"""<div class="card ref"><div class="role" style="position:static;margin-bottom:.04in;letter-spacing:.16em">{NAME}</div><h2>Quick rules<i>.</i></h2><dl>
<dt>Your turn: do one</dt>
<dd><b>Gather:</b> take 2 cards from the Bench and/or the deck. Refill the Bench to 4. Hand limit 8.</dd>
<dd><b>Host a round:</b> 3 or 4 different rituals, one of them a Lake. Score the numbers, +3 for all four.</dd>
<dt>Joining in</dt>
<dd>Going left, each player may add one card with the Lake’s number (any ritual) or a Wool Hat. A guest scores the Lake’s number; the host scores +1 per guest.</dd>
<dt>Last call</dt>
<dd>Deck empty: shuffle the Steam pile, count off 20 cards. When those run out, finish the lap. −1 for each card left in hand.</dd>
<dt>Head start</dt><dd>First player 0, second 1, everyone else 2.</dd></dl>{CR}</div>"""


def pattern():
    """Back pattern: rows of small steam curls."""
    p = []
    for row in range(9):
        y = 12 + row * 26
        off = 10 if row % 2 else 0
        for col in range(6):
            x = 6 + off + col * 30
            p.append(f'<path d="M{x} {y + 10}c4-4 -4-6 0-10s-4-6 0-10" />')
    return ('<svg class="pat" viewBox="0 0 196 278" preserveAspectRatio="xMidYMid slice" fill="none" stroke="#1b1512" '
            f'stroke-opacity=".22" stroke-width="1.3" stroke-linecap="round" aria-hidden="true">{"".join(p)}</svg>')


BACK = f"""<div class="card back"><div class="frame">{pattern()}</div>
<div class="medal">{w2.icon("sauna-hat")}<div class="t">Good<br>Steam<i>.</i></div></div>
<div class="s"><a href="{C.SITE}">diveluxsaunahat.com</a></div></div>"""


def mini(r, v, guest=False):
    name, _, col, _, _ = RIT[r]
    return (f'<div class="mini{" g" if guest else ""}"><i style="background:{col}"></i><b>{v if v else ""}</b>{icon(r)}'
            f'<span>{C.esc(name)}</span></div>')


def rules_page():
    deck = "".join(
        f'<div style="background:{RIT[r][2]}">{icon(r)}<b>{RIT[r][0]}</b><span>{t}</span></div>' for r, t in [
            ("stones", "Heat · 1–7<br>14 cards"), ("ladle", "Steam · 1–7<br>14 cards"), ("birch", "Whisk · 1–7<br>14 cards"),
            ("lake", "Cool-down · 1–7<br>14 cards"), ("hat", "Wild<br>4 cards")])
    ex = (mini("stones", 5) + mini("ladle", 3) + mini("birch", 6) + mini("lake", 4)
          + '<span class="plus">+</span>' + mini("birch", 4, True) + mini("hat", 0, True))
    return f"""<main class="page">
<span class="kicker">A card game for the sauna lounge · 2–6 players · 15–20 minutes · ages 8 and up</span>
<div class="head"><h1>Good Steam<i>.</i></h1>
<p class="lead">Host sauna rounds, let your friends join in and collect the most points. Every round needs a cool-down at the lake.</p></div>
<div class="deck">{deck}</div>
<div class="cols">
<div class="col">
<section class="r"><h3>Setup</h3><ol>
<li><span>Shuffle the 60 game cards (keep the 3 quick-rule cards out). Deal <b>5 cards</b> to each player.</span></li>
<li><span>Lay <b>4 cards face up</b> in a row: this is <b>the Bench</b>. Put the deck face down next to it and leave room for a face-up discard pile, <b>the Steam pile</b>.</span></li>
<li><span>Whoever had a sauna most recently goes first. Play goes to the left.</span></li>
<li><span><b>Head start:</b> on the score sheet the first player starts with 0 points, the second with 1, everyone else with 2. This evens out the first player’s small edge.</span></li>
</ol></section>
<section class="r"><h3>On your turn, do one thing</h3>
<div class="opt"><b>A</b><div><p><b>Gather</b></p><p>Take <b>2 cards</b>: from the Bench, from the top of the deck, or one of each. Then refill the Bench to 4 from the deck. More than <b>8 cards</b> in your hand? Discard down to 8 onto the Steam pile.</p></div></div>
<div class="opt"><b>B</b><div><p><b>Host a round</b></p><p>Lay <b>3 or 4 cards</b> from your hand face up in front of you:</p><ul>
<li>each card is a <b>different ritual</b>,</li>
<li>one of them is a <b>Lake</b> card,</li>
<li>a <b>Wool Hat</b> may stand in for a missing Stones, Ladle or Birch. It counts 0 and is never the Lake.</li></ul>
<p>Score the <b>sum of the numbers</b>. A <b>full round</b> (Stones, Ladle, Birch and Lake) scores <b>+3</b>.</p></div></div>
</section>
<section class="r"><h3>Good to know</h3><ul>
<li>One action per turn: gather <b>or</b> host, never both.</li>
<li>You can’t join your own round, and each player joins a round at most once.</li>
<li>Once the deck is gone, you may still take cards from the Bench.</li>
<li>Keep your hand hidden. The Bench and the Steam pile are open to everyone.</li>
</ul></section>
</div>
<div class="col">
<section class="r"><h3>Joining in</h3>
<p>After a round is laid down, the other players may join, one by one, starting on the host’s left. To join, add <b>one card with the same number as the host’s Lake</b>, in any ritual, or a <b>Wool Hat</b>.</p>
<p>Each guest scores <b>the Lake’s number</b>. The host scores <b>+1 for every guest</b>. Then all the cards go to the Steam pile.</p>
</section>
<section class="r"><h3>Example</h3>
<div class="ex">{ex}</div>
<p class="calc">Mia hosts a full round: <span class="num">5 + 3 + 6 + 4 = 18</span>, plus 3 = <span class="num">21</span>. Her Lake is a 4. Leo joins with a Birch 4, Sam with a Wool Hat: each scores <span class="num">4</span>. Mia gets <span class="num">+2</span> for two guests: <span class="num">23</span>.</p>
<p class="calc"><b>Tip:</b> a high Lake scores more for you, and more for your guests too.</p>
</section>
<section class="r"><h3>Last call and the end</h3>
<p>When the deck runs out, shuffle the Steam pile and count off <b>20 cards</b> face down. That is the last deck; put the rest away. When the last deck runs out too, <b>finish the lap</b>: play on until the player on the first player’s right has had a turn. Then the game ends. Nothing left to take? Host a round or pass.</p>
<p>Each card still in your hand costs <b>1 point</b>. Most points wins. A tie is a shared win.</p>
</section>
<div class="safe"><b>Play in the lounge, not in the hot room.</b> Paper and heat don’t mix, and nothing in this game is about staying in the heat. Going in for a sauna round? Put your hand face down and the others skip you until you are back (a house rule we did not test). Drink water between rounds.</div>
</div></div>
{C.foot(NAME + " · page 1 of " + str(PAGES))}
</main>"""


def score_page():
    rows = "".join('<tr class="rw"><td></td>' + "<td></td>" * 6 + "</tr>" for _ in range(20))
    head = "".join(f"<th>Player {k}</th>" for k in range(1, 7))
    start = "".join(f"<td>{v}</td>" for v in ("0", "1", "2", "2", "2", "2"))
    printing = "<ol>" + "".join(f"<li><span>{x}</span></li>" for x in [
        "Print at 100% (actual size) on card stock, about 80–110 lb cover (216–300 gsm).",
        "<b>Cards:</b> print pages 3–16 double-sided, “flip on long edge”. Each back page follows its front page. Print one test sheet first.",
        "Cut on the crop marks. A paper trimmer gives the cleanest edges. Round the corners if you like.",
        "Print this page as often as you need score sheets. You also need a pencil.",
    ]) + "</ol>"
    sim = ("<p class='sim'><b>Tested before printing.</b> We ran the rules through a computer simulation: 4,000 games for "
           "every player count, plus games with random moves to look for stuck spots. Every game ended. Games take about "
           "36–49 turns, and with the head start each seat wins close to its fair share. The full report and the script "
           "come with the files.</p>")
    return f"""<main class="page">
<div class="ph" style="display:flex"><h2>Score sheet</h2><p>Write each score as it happens. Total up at the end, after −1 for each card left in hand.</p></div>
<table class="sc"><thead><tr><th></th>{head}</tr></thead><tbody>
<tr class="nm"><td>Name</td>{"<td></td>" * 6}</tr>
<tr class="st"><td>Head start</td>{start}</tr>
{rows}
<tr class="rw"><td>Cards in hand (−1 each)</td>{"<td></td>" * 6}</tr>
<tr class="tot"><td>Total</td>{"<td></td>" * 6}</tr></tbody></table>
<div class="prn"><section class="r"><h3>How to print</h3>{printing}</section>
<section class="r"><h3>Fair play</h3>{sim}<p class="sim" style="margin-top:.05in">More free sauna printables and tools: <a href="{C.TOOLS}">diveluxsaunahat.com/pages/sauna-tools</a></p></section></div>
{C.foot(NAME + " · page 2 of " + str(PAGES))}
</main>"""


def build():
    slots = [front(c) for c in CARDS] + [ref_card() for _ in range(3)]
    assert len(slots) == 63
    pages = [rules_page(), score_page()]
    for sh in range(7):
        chunk = slots[sh * 9:(sh + 1) * 9]
        pages.append(f'<main class="page sheet"><div class="grid">{crops()}{"".join(chunk)}</div></main>')
        # backs: identical design, laid out mirrored (columns swapped) so a long-edge flip puts each back behind its front
        pages.append(f'<main class="page sheet"><div class="grid">{crops()}{BACK * 9}</div></main>')
    assert len(pages) == PAGES
    body = "\n".join(pages)
    C.write(os.path.join(C.ROOT, SLUG, SLUG + ".html"), C.doc(TITLE, DESC, KEYWORDS, CSS + ART_CSS, body))
    meta = dict(title="Good Steam: a printable card game for the sauna lounge (2-6 players)", subject=DESC, keywords=KEYWORDS)
    jobs = C.std_jobs(SLUG, SLUG + ".html", SLUG, meta)
    return dict(slug=SLUG, jobs=jobs, preview=dict(pdf=jobs[0]["pdf"], pages=[1, 3, 4], dpi=75))
