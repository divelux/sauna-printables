#!/usr/bin/env python3
"""Independent check of the published puzzles. Reads puzzles.json (written at build time) and the finished PDFs.

1. Word search: every listed word is found exactly once in the grid, at the place the answer key says;
   no blocked word appears in any direction.
2. Crossword: the grid is rebuilt from the JSON rows; every across/down run of 2+ letters is read back and must
   match a numbered answer with a clue; no stray runs; all entries cross; the grid is connected.
3. PDF: the letters printed on page 1 of each PDF are the same letters, in the same order, as the grid in the JSON,
   the word list on the page is the same set of words, and the solved crossword on page 3 carries the same letters.
"""
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import puzzles as P  # noqa: E402

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "sauna-word-search-crossword")
data = json.load(open(os.path.join(D, "puzzles.json"), encoding="utf-8"))

# 1. word search
ws = data["word_search"]
grid = [list(r) for r in ws["grid"]]
key = {w: (a["row"] - 1, a["col"] - 1, a["d_row"], a["d_col"]) for w, a in ws["answers"].items()}
assert sorted(key) == sorted(ws["words"])
P.check_word_search(grid, ws["words"], key)
dirs = {}
for w, (r, c, dr, dc) in key.items():
    dirs[(dr, dc)] = dirs.get((dr, dc), 0) + 1
print(f"word search: {len(grid)}x{len(grid[0])}, {len(ws['words'])} words, each found exactly once; directions used: {len(dirs)} of 8")

# 2. crossword
cw = data["crossword"]
cgrid = [[None if ch == "." else ch for ch in row] for row in cw["grid"]]
nums, across, down = P.number_crossword(cgrid)
assert {str(n): w for n, w in across.items()} == {n: v["answer"] for n, v in cw["across"].items()}, "across mismatch"
assert {str(n): w for n, w in down.items()} == {n: v["answer"] for n, v in cw["down"].items()}, "down mismatch"
assert all(v["clue"].strip() for v in list(cw["across"].values()) + list(cw["down"].values()))
placed = [(w, r, c, "A") for (r, c), n in nums.items() if n in across for w in [across[n]]] + \
         [(w, r, c, "D") for (r, c), n in nums.items() if n in down for w in [down[n]]]
P.check_crossword(placed, {w for w, _, _, _ in placed})
cells = sum(1 for row in cgrid for ch in row if ch)
crossings = sum(len(w) for w, _, _, _ in placed) - cells
print(f"crossword: {len(cgrid[0])}x{len(cgrid)}, {len(across)} across + {len(down)} down, {cells} letter cells, "
      f"{crossings} crossings, no stray runs, connected")

# 3. the PDFs carry the same puzzle
for size in ("letter", "a4"):
    pdf = os.path.join(D, f"sauna-word-search-crossword-{size}.pdf")
    def page_words(n):
        out = subprocess.run(["pdftotext", "-f", str(n), "-l", str(n), "-bbox", pdf, "-"], capture_output=True, text=True, check=True).stdout
        return [(float(x), float(y), t) for x, y, t in re.findall(r'<word xMin="([\d.]+)" yMin="([\d.]+)"[^>]*>([^<]*)</word>', out)]
    p1 = page_words(1)
    singles = sorted(((round(y), x, t) for x, y, t in p1 if len(t) == 1 and t.isupper()), key=lambda v: (v[0], v[1]))
    rows = {}
    for y, x, t in singles:
        rows.setdefault(y, []).append((x, t))
    got = ["".join(t for _, t in sorted(r)) for _, r in sorted(rows.items())]
    assert got == ws["grid"], f"{size}: printed grid differs from puzzles.json"
    listed = {t for _, _, t in p1 if t.isupper() and len(t) >= 3} - {"DIVELUX"}  # footer credit
    assert listed == set(ws["words"]), f"{size}: printed word list differs: {listed ^ set(ws['words'])}"
    p3 = page_words(3)
    ys = sorted({round(y) for x, y, t in p3 if len(t) == 1 and t.isupper()})
    solved = sorted(t for x, y, t in p3 if len(t) == 1 and t.isupper())
    want = sorted([ch for row in ws["grid"] for ch in row] + [ch for row in cgrid for ch in row if ch])
    assert solved == want, f"{size}: answer page letters differ"
    print(f"{size} PDF: printed grid, word list and answer page match puzzles.json")
print("ALL PUZZLE CHECKS PASSED")
