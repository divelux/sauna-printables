"""11. Sauna Bingo: a rules page and six different 5 x 5 cards.
Squares are harmless things to notice. Nothing asks anyone to drink, compete or stay in the heat longer."""
import os
import random
import common as C

SLUG = "sauna-bingo"
TITLE = "Sauna Bingo"
DESC = "A printable sauna bingo game for a group: six different 5 x 5 cards and a rules page. Friendly things to notice during a sauna evening, no dares."
KEYWORDS = "sauna bingo, sauna party game, printable bingo cards, sauna night game, group game printable, spa party activity, sauna evening, DIVELUX"

POOL = [
    "Someone says “one more round”", "Glasses fog up", "A long, happy sigh", "Water hisses on the stones",
    "Someone moves down a bench", "Someone checks the thermometer", "A full minute of easy silence",
    "Someone mentions Finland", "A sauna story gets told", "A hat gets a compliment", "Someone refills the bucket",
    "Someone finishes a glass of water", "A cold-water gasp", "“Close the door!”", "The ladle changes hands",
    "Someone stretches", "The sand timer gets flipped", "Someone asks before pouring", "Steam reaches the top bench",
    "A first-timer in the room", "Someone loses track of time", "Tea gets poured", "The wood creaks",
    "Someone steps out to look at the sky", "Rosy cheeks all around", "“I could live in here”",
    "Someone forgets a towel", "Somebody yawns", "Someone hums a tune", "Talk turns to the weather",
    "A snack plate appears", "Someone says “ahhh”", "Two hands reach for the ladle", "“How hot is it?”",
    "Cold floor, quick feet", "Plans for the next sauna night", "Eyes closed, big smile", "Flip-flops get mixed up",
    "Someone wraps up in a robe", "The stove ticks or crackles", "“The steam is just right”", "A pet waits by the door",
]
FREE = "Free square: you showed up"
SEED = 2026

CSS = """
.page{padding:.5in .6in .34in}
h1{font-weight:800;font-stretch:75%;font-size:112pt;line-height:.83;letter-spacing:-.022em;margin:.12in 0 0 -.045in}
h1 i,.ch h2 i{font-style:normal;color:var(--ember)}
.lead{font-family:var(--display);font-weight:500;font-size:16pt;line-height:1.28;color:var(--ink-2);margin:.22in 0 .24in;max-width:6in;text-wrap:balance}
.cols{display:grid;grid-template-columns:1.25fr 1fr;column-gap:.4in;flex:1;min-height:0;border-top:2px solid var(--ink);padding-top:.14in}
.cols h2{font-weight:800;font-stretch:75%;font-size:24pt;line-height:1;letter-spacing:-.012em;margin-bottom:.08in}
.steps{counter-reset:s}
.steps li{counter-increment:s;display:grid;grid-template-columns:.42in 1fr;padding:.11in 0;border-top:1px solid var(--line-2);font-size:11.4pt;line-height:1.42;color:var(--ink-2)}
.steps li:first-child{border-top:0}
.steps li::before{content:counter(s);font-family:var(--display);font-weight:700;font-stretch:75%;font-size:25pt;line-height:.95;color:var(--ink)}
.steps b{font-weight:600;color:var(--ink)}
.side p{font-size:11pt;line-height:1.46;color:var(--ink-2);margin-bottom:.1in}
.side .h{margin-top:.24in}
.mini{display:grid;grid-template-columns:repeat(5,1fr);width:2.1in;height:2.1in;border:2px solid var(--ink);margin-top:.16in}
.mini i{border:.6px solid var(--ink-2);display:block}
.mini i.on{background:var(--t1)}.mini i.free{background:var(--ink)}
.cap{font-size:8.4pt!important;color:var(--muted)!important;margin-top:.07in}
.ch{display:flex;justify-content:space-between;align-items:flex-end;gap:.3in;flex:none}
.ch h2{font-weight:800;font-stretch:75%;font-size:70pt;line-height:.84;letter-spacing:-.02em;margin-left:-.03in;white-space:nowrap}
.ch .id{font-family:var(--display);font-weight:800;font-stretch:75%;font-size:70pt;line-height:.84;letter-spacing:-.02em;color:var(--ink);
border:2px solid var(--ink);border-radius:6px;padding:.07in .16in .03in;background:var(--t2)}
.ch .id small{display:block;font-family:var(--body);font-stretch:100%;font-weight:600;font-size:7pt;letter-spacing:.16em;text-transform:uppercase;line-height:1;margin-bottom:.03in}
.sub{font-size:9.6pt;line-height:1.4;color:var(--ink-2);margin:.12in 0 0}
.wrap{flex:1;min-height:0;display:flex;align-items:center;justify-content:center;padding:.14in 0}
.card{display:grid;grid-template-columns:repeat(5,1fr);grid-template-rows:repeat(5,1fr);width:100%;aspect-ratio:1/1;max-height:100%;border:2.5px solid var(--ink);border-radius:6px;overflow:hidden;background:var(--card)}
.cell{display:flex;align-items:center;justify-content:center;text-align:center;padding:.09in .08in;border-right:1px solid var(--ink);border-bottom:1px solid var(--ink);
font-family:var(--display);font-weight:600;font-size:12.2pt;line-height:1.16;letter-spacing:-.005em;text-wrap:balance;overflow:hidden}
.cell:nth-child(5n){border-right:0}.cell:nth-child(n+21){border-bottom:0}
.cell.free{background:var(--t1);font-size:10.5pt}
.cell.free b{display:block;font-weight:800;font-stretch:75%;font-size:30pt;line-height:.95;letter-spacing:-.01em}
.name{display:flex;gap:.3in;font-size:9pt;color:var(--ink-2);flex:none;margin-bottom:.12in}
.name span{flex:1;border-bottom:1px solid var(--ink-2);height:.24in;display:flex;align-items:flex-end;padding-bottom:.03in}
"""


def make_cards(n=6):
    """Six cards of 24 different squares each. Every pool item is used, and no two cards share a row,
    a column or more than 17 squares."""
    rng = random.Random(SEED)
    for _ in range(2000):
        cards = [rng.sample(POOL, 24) for _ in range(n)]
        if check_cards(cards, raise_on_fail=False):
            return cards
    raise RuntimeError("bingo: no valid set found")


def lines_of(card):
    g = card[:12] + [FREE] + card[12:]
    rows = [tuple(g[r * 5:r * 5 + 5]) for r in range(5)]
    cols = [tuple(g[c + 5 * r] for r in range(5)) for c in range(5)]
    return [frozenset(x) for x in rows + cols]


def check_cards(cards, raise_on_fail=True):
    problems = []
    for i, c in enumerate(cards):
        if len(c) != 24 or len(set(c)) != 24 or any(x not in POOL for x in c):
            problems.append(f"card {i + 1}: not 24 different squares from the pool")
    if set().union(*map(set, cards)) != set(POOL):
        problems.append("some pool items are not on any card")
    for i in range(len(cards)):
        for j in range(i + 1, len(cards)):
            if len(set(cards[i]) & set(cards[j])) > 17:
                problems.append(f"cards {i + 1} and {j + 1} share too many squares")
            if set(lines_of(cards[i])) & set(lines_of(cards[j])):
                problems.append(f"cards {i + 1} and {j + 1} share a full row or column")
    if problems and raise_on_fail:
        raise AssertionError("; ".join(problems))
    return not problems


def build():
    assert len(POOL) == len(set(POOL)) == 42
    cards = make_cards()
    check_cards(cards)
    mini = "".join(f'<i class="{"free" if k == 12 else "on" if k in (2, 7, 17, 22) else ""}"></i>' for k in range(25))
    pages = [f"""<main class="page">
<span class="kicker">A quiet game for a sauna evening</span>
<h1>Sauna<br>bingo<i>.</i></h1>
<p class="lead">Six cards of small things that happen on every good sauna night. Notice them, mark them, and call it when you have five in a row.</p>
<div class="cols">
<div><h2>How to play</h2><ol class="steps">
<li><span><b>Hand out the cards.</b> Six different cards, one per player or pair. More guests? Print a second set and trade.</span></li>
<li><span><b>Keep paper and pens in the lounge.</b> Cards stay outside the hot room.</span></li>
<li><span><b>Just notice.</b> When something on your card happens during the evening, remember it.</span></li>
<li><span><b>Mark your squares between rounds.</b> The center square is free.</span></li>
<li><span><b>Five in a row wins:</b> across, down or corner to corner. Say “bingo”, softly. It is a sauna.</span></li>
<li><span><b>The winner chooses</b> the next tea, the next playlist or the best seat.</span></li>
</ol></div>
<div class="side"><h2>Fair play</h2>
<p>Squares only count when they happen on their own. No dares and no contests.</p>
<p>Nobody stays in the heat for the game. Step out whenever you like; the cards will wait.</p>
<h2 class="h">Longer game</h2>
<p>Play blackout: keep your card for the season and fill every square over several sauna nights.</p>
<div class="mini" aria-hidden="true">{mini}</div>
<p class="cap">Five in a row, with the free square in the middle.</p>
</div></div>
{C.foot("General information, not medical advice.")}
</main>"""]
    for i, card in enumerate(cards):
        letter = "ABCDEF"[i]
        g = card[:12] + [FREE] + card[12:]
        cells = "".join('<div class="cell fit free"><span><b>Free</b>you showed up</span></div>' if k == 12 else f'<div class="cell fit">{C.esc(x)}</div>' for k, x in enumerate(g))
        pages.append(f"""<main class="page">
<div class="ch"><h2>Sauna bingo<i>.</i></h2><div class="id"><small>Card</small>{letter}</div></div>
<p class="sub">Mark a square when it happens on its own. Five in a row wins: across, down or corner to corner.</p>
<div class="wrap"><div class="card">{cells}</div></div>
<div class="name"><span>Player</span><span>Date</span></div>
{C.foot(f"Sauna Bingo · card {letter} of six")}
</main>""")
    C.write(os.path.join(C.ROOT, SLUG, SLUG + ".html"), C.doc(TITLE, DESC, KEYWORDS, CSS, "\n".join(pages)))
    meta = dict(title="Sauna Bingo: Six Printable Cards and Rules", subject=DESC, keywords=KEYWORDS)
    jobs = C.std_jobs(SLUG, SLUG + ".html", SLUG, meta)
    return dict(slug=SLUG, jobs=jobs, preview=dict(pdf=jobs[0]["pdf"], pages=[1, 2, 3], dpi=75))
