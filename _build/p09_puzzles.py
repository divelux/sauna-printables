"""9. Sauna word search + crossword, with answers on a separate page.
Grids are generated and then re-checked by puzzles.py every time this file is built."""
import json
import os
import common as C
import puzzles as P

SLUG = "sauna-word-search-crossword"
TITLE = "Sauna Word Search and Crossword"
DESC = "Two printable sauna puzzles: a 28-word word search and a 27-clue crossword, with both answer keys on a separate page."
KEYWORDS = "sauna word search, sauna crossword, printable sauna puzzle, sauna party game, spa activity sheet, sauna trivia, word search printable, DIVELUX"

WS_WORDS = ("SAUNA BANYA LOYLY STEAM STONES BENCH LADLE BUCKET WHISK BIRCH TOWEL FELT WOOL HAT HEAT STOVE PLUNGE HAMMAM "
            "AUFGUSS VIHTA VENIK KIUAS EMBER SWEAT FINLAND ESTONIA SMOKE ROBE").split()
WS_SEED, CW_SEED, CW_TRIES = 7, 13, 150

CLUES = {
    "SAUNA": "The Finnish word the whole world borrowed",
    "LOYLY": "Finnish word for the steam off the stones (written here without its dots)",
    "BANYA": "Russian steam bath",
    "VENIK": "Leafy birch or oak whisk used in a banya",
    "VIHTA": "Birch whisk, as it is called in western Finland",
    "KIUAS": "Finnish word for the sauna stove",
    "AUFGUSS": "German steam ritual led by a sauna master with a towel",
    "HAMMAM": "Turkish steam bath with warm marble",
    "LADLE": "It carries water from the bucket to the stones",
    "STONES": "They sit on the stove and hold the heat",
    "BENCH": "The top one is the hottest seat",
    "FELT": "Wool pressed into a thick fabric without weaving",
    "WOOL": "Sheep fiber that a classic sauna hat is made of",
    "HAT": "Worn dry on your head in the hot room",
    "BIRCH": "Tree whose leafy twigs make a classic whisk",
    "PLUNGE": "Cold ___: the quick dip after the heat",
    "TOWEL": "What you sit on",
    "STEAM": "What water becomes on hot stones",
    "EMBER": "Glowing piece of wood in the fire",
    "FINLAND": "Its sauna culture joined UNESCO's heritage list in 2020",
    "ESTONIA": "Home of the Võromaa smoke sauna tradition",
    "AVANTO": "Finnish word for a hole cut in the ice",
    "PIRTIS": "Lithuanian bathhouse",
    "BASTU": "Swedish word for sauna",
    "ONSEN": "Japanese hot-spring bath",
    "LEIL": "Estonian word for sauna steam",
    "KERIS": "Estonian word for the sauna stove",
    "SMOKE": "___ sauna: the oldest kind, heated with no chimney",
    "BUCKET": "It holds the water for the stones",
    "SWEAT": "What your skin does in the heat",
    "REST": "What to do between rounds",
    "ROUND": "One stay in the hot room",
    "DOOR": "Close it quickly to keep the heat in",
    "TEA": "Warm drink in the lounge after a banya",
    "DRY": "How a wool sauna hat is worn",
    "HEAT": "It rises toward the ceiling",
}

CSS = """
.page{padding:.5in .6in .34in;background:#fff}
.head{display:grid;grid-template-columns:auto 1fr;column-gap:.45in;align-items:end;border-bottom:2px solid var(--ink);padding-bottom:.13in;flex:none}
h1,h2.t{font-weight:800;font-stretch:75%;font-size:62pt;line-height:.84;letter-spacing:-.02em;margin:.06in 0 0 -.025in;white-space:nowrap}
h1 i,h2.t i{font-style:normal;color:var(--ember)}
.lead{font-size:10pt;line-height:1.45;color:var(--ink-2);padding-bottom:.02in;text-wrap:balance}
.gridbox{flex:1;min-height:0;display:flex;justify-content:center;align-items:center;padding:.14in 0}
.gridbox svg{display:block;height:100%;max-width:100%}
svg .ws{font-family:var(--display);font-weight:600;font-size:17px;text-anchor:middle;fill:var(--ink)}
svg .cn{font-family:var(--body);font-weight:600;font-size:7.6px;fill:var(--ink-2)}
svg .cl{font-family:var(--display);font-weight:700;font-size:17px;text-anchor:middle;fill:var(--ink)}
.words{display:grid;grid-template-columns:repeat(7,auto);justify-content:space-between;row-gap:.07in;border-top:1px solid var(--line-2);padding-top:.12in;flex:none}
.words span{font-family:var(--display);font-weight:600;font-size:10.6pt;letter-spacing:.06em}
.fine{font-size:7.6pt;line-height:1.42;color:var(--muted);margin:.1in 0 .1in}
.clues{display:grid;grid-template-columns:1fr 1fr;column-gap:.35in;flex:none;border-top:1px solid var(--line-2);padding-top:.1in;margin-bottom:.12in}
.clues h3{font-family:var(--display);font-weight:700;font-size:12.5pt;margin-bottom:.03in}
.clues li{display:grid;grid-template-columns:.24in 1fr;font-size:8.5pt;line-height:1.36;color:var(--ink-2)}
.clues li b{font-weight:600;color:var(--ink);font-variant-numeric:tabular-nums}
.ans{flex:1;min-height:0;display:grid;grid-template-rows:1.12fr 1fr;row-gap:.1in;padding:.12in 0}
.ans section{display:grid;grid-template-columns:1.3in 1fr;column-gap:.2in;min-height:0}
.ans h3{font-family:var(--display);font-weight:700;font-size:14pt;line-height:1.15}
.ans p{font-size:8.4pt;line-height:1.4;color:var(--muted);margin-top:.05in}
.ans .g{min-height:0;display:flex;justify-content:center}
.ans svg{display:block;height:100%;max-width:100%}
"""


def ws_svg(grid, placed=None):
    n, c = len(grid), 30
    o = [f'<svg viewBox="0 0 {n * c} {n * c}" role="img" aria-label="Word search letter grid, {n} by {n}">']
    if placed:
        for w, (r, k, dr, dc) in placed.items():
            x1, y1 = k * c + c / 2, r * c + c / 2
            x2, y2 = (k + dc * (len(w) - 1)) * c + c / 2, (r + dr * (len(w) - 1)) * c + c / 2
            o.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#f5c7a0" stroke-width="19" stroke-linecap="round" opacity=".85"/>')
    o.append(f'<rect x="1" y="1" width="{n * c - 2}" height="{n * c - 2}" rx="6" fill="none" stroke="#1b1512" stroke-width="2"/>')
    for r, row in enumerate(grid):
        for k, ch in enumerate(row):
            o.append(f'<text class="ws" x="{k * c + c / 2}" y="{r * c + c / 2 + 6}">{ch}</text>')
    o.append("</svg>")
    return "".join(o)


def cw_svg(grid, nums, solved=False):
    rows, cols, c = len(grid), len(grid[0]), 30
    o = [f'<svg viewBox="-1 -1 {cols * c + 2} {rows * c + 2}" role="img" aria-label="Crossword grid, {cols} columns by {rows} rows">']
    for r, row in enumerate(grid):
        for k, ch in enumerate(row):
            if not ch:
                continue
            o.append(f'<rect x="{k * c}" y="{r * c}" width="{c}" height="{c}" fill="#fff" stroke="#1b1512" stroke-width="1.3"/>')
            if (r, k) in nums:
                o.append(f'<text class="cn" x="{k * c + 2.4}" y="{r * c + 8.6}">{nums[(r, k)]}</text>')
            if solved:
                o.append(f'<text class="cl" x="{k * c + c / 2}" y="{r * c + c / 2 + 7.5}">{ch}</text>')
    o.append("</svg>")
    return "".join(o)


def make():
    grid, placed = P.make_word_search(WS_WORDS, 15, WS_SEED)
    P.check_word_search(grid, WS_WORDS, placed)
    cw = P.make_crossword(list(CLUES), 13, 17, CW_SEED, CW_TRIES)
    cgrid, nums, across, down = P.check_crossword(cw, set(CLUES))
    assert len(cw) == 27 and len(WS_WORDS) == 28  # the counts quoted in DESC and LISTING.md
    return grid, placed, cw, cgrid, nums, across, down


def build():
    grid, placed, cw, cgrid, nums, across, down = make()
    d = os.path.join(C.ROOT, SLUG)
    # Keep the puzzle data next to the PDFs so anyone can re-check it (see _build/verify_puzzles.py).
    C.write(os.path.join(d, "puzzles.json"), json.dumps({
        "word_search": {"grid": ["".join(r) for r in grid], "words": WS_WORDS,
                        "answers": {w: {"row": p[0] + 1, "col": p[1] + 1, "d_row": p[2], "d_col": p[3]} for w, p in placed.items()}},
        "crossword": {"grid": ["".join(ch or "." for ch in r) for r in cgrid],
                      "across": {str(n): {"answer": w, "clue": CLUES[w]} for n, w in across.items()},
                      "down": {str(n): {"answer": w, "clue": CLUES[w]} for n, w in down.items()}},
    }, indent=1, ensure_ascii=False) + "\n")
    words = "".join(f"<span>{w}</span>" for w in sorted(WS_WORDS))
    cl = lambda dct: "".join(f"<li><b>{n}</b><span>{C.esc(CLUES[w])}&nbsp;({len(w)})</span></li>" for n, w in sorted(dct.items()))
    body = f"""<main class="page">
<span class="kicker">Sauna puzzles · 1 of 2</span>
<div class="head"><h1>Word search<i>.</i></h1><p class="lead">Find the {len(WS_WORDS)} sauna words hidden in the grid. They run across, down and diagonally, forward and backward. Each word appears once.</p></div>
<div class="gridbox">{ws_svg(grid)}</div>
<div class="words">{words}</div>
<p class="fine">LOYLY is the Finnish löyly, the steam off the stones, written here without its dots. Answers are on the last page.</p>
{C.foot()}
</main>
<main class="page">
<span class="kicker">Sauna puzzles · 2 of 2</span>
<div class="head"><h2 class="t">Crossword<i>.</i></h2><p class="lead">{len(across) + len(down)} clues from the hot room and the bathing traditions around it. The number in brackets is the length of the answer.</p></div>
<div class="gridbox">{cw_svg(cgrid, nums)}</div>
<div class="clues"><div><h3>Across</h3><ol>{cl(across)}</ol></div><div><h3>Down</h3><ol>{cl(down)}</ol></div></div>
{C.foot()}
</main>
<main class="page">
<span class="kicker">Sauna puzzles</span>
<div class="head"><h2 class="t">Answers<i>.</i></h2><p class="lead">No peeking until you are out of the heat.</p></div>
<div class="ans">
<section><div><h3>Word search</h3><p>Each word is marked once, start to end.</p></div><div class="g">{ws_svg(grid, placed)}</div></section>
<section><div><h3>Crossword</h3><p>LOYLY stands for löyly.</p></div><div class="g">{cw_svg(cgrid, nums, True)}</div></section>
</div>
{C.foot()}
</main>"""
    C.write(os.path.join(d, SLUG + ".html"), C.doc(TITLE, DESC, KEYWORDS, CSS, body))
    meta = dict(title="Sauna Word Search and Crossword (Printable, with Answers)", subject=DESC, keywords=KEYWORDS)
    jobs = C.std_jobs(SLUG, SLUG + ".html", SLUG, meta)
    return dict(slug=SLUG, jobs=jobs, preview=dict(pdf=jobs[0]["pdf"], pages=[1, 2], dpi=75))
