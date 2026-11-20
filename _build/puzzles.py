"""Generators and independent checkers for the word search and the crossword.

Everything is deterministic (fixed seeds). The checkers do not trust the generators: they re-read the
finished grids and look for every word / every run of letters from scratch.
"""
import random

DIRS = [(0, 1), (1, 0), (1, 1), (-1, 1), (0, -1), (-1, 0), (-1, -1), (1, -1)]
# Filler letters must not spell anything rude by accident.
BLOCK = ["ASS", "SEX", "FUCK", "FUK", "SHIT", "DAMN", "HELL", "CRAP", "PISS", "DICK", "COCK", "CUNT", "TIT", "FAG", "NAZI",
         "KKK", "RAPE", "SLUT", "ANUS", "ARSE", "BITCH", "PORN", "NUDE", "WHORE", "PUSSY", "DIE", "KILL", "HATE", "GAY", "JEW",
         "FAT", "DRUNK", "BEER", "VODKA", "WINE", "DEAD", "POO", "PEE", "BUM", "BUTT", "HOE", "HO", "WTF", "STD", "SUCK"]
BLOCK = [b for b in BLOCK if len(b) >= 3]


# ---------- word search ----------
def find_all(grid, word):
    """Every place the word can be read in the grid, in any of the 8 directions."""
    n, m = len(grid), len(grid[0])
    hits = []
    for r in range(n):
        for c in range(m):
            if grid[r][c] != word[0]:
                continue
            for dr, dc in DIRS:
                er, ec = r + dr * (len(word) - 1), c + dc * (len(word) - 1)
                if 0 <= er < n and 0 <= ec < m and all(grid[r + dr * i][c + dc * i] == word[i] for i in range(len(word))):
                    hits.append((r, c, dr, dc))
    return hits


def make_word_search(words, n=15, seed=7):
    rng = random.Random(seed)
    alphabet = sorted(set("".join(words)))
    for _ in range(500):
        grid = [[None] * n for _ in range(n)]
        placed = {}
        ok = True
        for w in sorted(words, key=lambda x: (-len(x), x)):
            for _try in range(600):
                dr, dc = rng.choice(DIRS)
                r, c = rng.randrange(n), rng.randrange(n)
                er, ec = r + dr * (len(w) - 1), c + dc * (len(w) - 1)
                if not (0 <= er < n and 0 <= ec < n):
                    continue
                if all(grid[r + dr * i][c + dc * i] in (None, w[i]) for i in range(len(w))):
                    for i in range(len(w)):
                        grid[r + dr * i][c + dc * i] = w[i]
                    placed[w] = (r, c, dr, dc)
                    break
            else:
                ok = False
                break
        if not ok:
            continue
        for _fill in range(300):
            g = [[ch if ch else rng.choice(alphabet) for ch in row] for row in grid]
            if check_word_search(g, words, placed, raise_on_fail=False):
                return g, placed
    raise RuntimeError("word search: no valid grid found")


def check_word_search(grid, words, placed=None, raise_on_fail=True):
    """True when every word is found exactly once and no blocked word appears anywhere."""
    problems = []
    n = len(grid)
    if any(len(row) != n for row in grid) or any(not ("A" <= ch <= "Z") for row in grid for ch in row):
        problems.append("grid is not a full square of A-Z")
    for w in words:
        hits = find_all(grid, w)
        if len(hits) != 1:
            problems.append(f"{w}: found {len(hits)} times")
        elif placed is not None and placed.get(w) != hits[0]:
            problems.append(f"{w}: found at {hits[0]}, answer key says {placed.get(w)}")
    for b in BLOCK:
        if b not in words and find_all(grid, b):
            problems.append(f"blocked word {b} appears")
    if problems and raise_on_fail:
        raise AssertionError("; ".join(problems))
    return not problems


# ---------- crossword ----------
def _try_layout(words, rng, max_rows, max_cols):
    order = sorted(words, key=lambda w: (-len(w), rng.random()))
    grid, dirs, placed = {}, {}, []

    def cells(w, r, c, d):
        return [(r, c + i) if d == "A" else (r + i, c) for i in range(len(w))]

    def bbox_ok(extra):
        rs = [p[0] for p in grid] + [p[0] for p in extra]
        cs = [p[1] for p in grid] + [p[1] for p in extra]
        return max(rs) - min(rs) < max_rows and max(cs) - min(cs) < max_cols

    def valid(w, r, c, d):
        cs = cells(w, r, c, d)
        before = (r, c - 1) if d == "A" else (r - 1, c)
        after = (r, c + len(w)) if d == "A" else (r + len(w), c)
        if before in grid or after in grid:
            return 0
        cross = 0
        for i, p in enumerate(cs):
            if p in grid:
                if grid[p] != w[i] or d in dirs[p]:
                    return 0
                cross += 1
            else:
                side = [(p[0] - 1, p[1]), (p[0] + 1, p[1])] if d == "A" else [(p[0], p[1] - 1), (p[0], p[1] + 1)]
                if any(s in grid for s in side):
                    return 0
        if cross == 0 or cross == len(w) or not bbox_ok(cs):
            return 0
        return cross

    def put(w, r, c, d):
        for i, p in enumerate(cells(w, r, c, d)):
            grid[p] = w[i]
            dirs.setdefault(p, set()).add(d)
        placed.append((w, r, c, d))

    put(order[0], 0, 0, "A")
    rest = order[1:]
    progress = True
    while progress and rest:
        progress = False
        for w in rest[:]:
            opts = []
            for (r, c), ch in list(grid.items()):
                for i, wc in enumerate(w):
                    if wc != ch:
                        continue
                    for d in "AD":
                        sr, sc = (r, c - i) if d == "A" else (r - i, c)
                        x = valid(w, sr, sc, d)
                        if x:
                            opts.append((x, rng.random(), sr, sc, d))
            if opts:
                _, _, sr, sc, d = max(opts)
                put(w, sr, sc, d)
                rest.remove(w)
                progress = True
    r0, c0 = min(p[0] for p in grid), min(p[1] for p in grid)
    return [(w, r - r0, c - c0, d) for w, r, c, d in placed]


def make_crossword(words, max_rows=13, max_cols=17, seed=11, tries=400):
    best, best_score = None, None
    for t in range(tries):
        placed = _try_layout(words, random.Random(seed * 1000 + t), max_rows, max_cols)
        rows = max(r + (len(w) if d == "D" else 1) for w, r, c, d in placed)
        cols = max(c + (len(w) if d == "A" else 1) for w, r, c, d in placed)
        n_cells = len({p for w, r, c, d in placed for p in ([(r, c + i) for i in range(len(w))] if d == "A" else [(r + i, c) for i in range(len(w))])})
        letters = sum(len(w) for w, _, _, _ in placed)
        score = (len(placed), letters - n_cells, -(rows * cols))
        if best_score is None or score > best_score:
            best, best_score = placed, score
    return best


def crossword_grid(placed):
    rows = max(r + (len(w) if d == "D" else 1) for w, r, c, d in placed)
    cols = max(c + (len(w) if d == "A" else 1) for w, r, c, d in placed)
    g = [[None] * cols for _ in range(rows)]
    for w, r, c, d in placed:
        for i, ch in enumerate(w):
            rr, cc = (r, c + i) if d == "A" else (r + i, c)
            if g[rr][cc] not in (None, ch):
                raise AssertionError(f"conflict at {rr},{cc}: {g[rr][cc]} vs {ch} ({w})")
            g[rr][cc] = ch
    return g


def number_crossword(grid):
    """Standard numbering: scan row by row; a cell gets a number when an across or down entry starts there.
    Returns (numbers {(r,c): n}, across {n: word}, down {n: word}) read from the grid itself."""
    rows, cols = len(grid), len(grid[0])
    L = lambda r, c: 0 <= r < rows and 0 <= c < cols and grid[r][c] is not None
    nums, across, down, n = {}, {}, {}, 0
    for r in range(rows):
        for c in range(cols):
            if not L(r, c):
                continue
            sa = not L(r, c - 1) and L(r, c + 1)
            sd = not L(r - 1, c) and L(r + 1, c)
            if sa or sd:
                n += 1
                nums[(r, c)] = n
                if sa:
                    k = c
                    w = ""
                    while L(r, k):
                        w += grid[r][k]
                        k += 1
                    across[n] = w
                if sd:
                    k = r
                    w = ""
                    while L(k, c):
                        w += grid[k][c]
                        k += 1
                    down[n] = w
    return nums, across, down


def check_crossword(placed, clue_words):
    """Rebuilds the grid from the answer key and checks it the way a solver would see it."""
    g = crossword_grid(placed)
    nums, across, down = number_crossword(g)
    want_a = sorted(w for w, _, _, d in placed if d == "A")
    want_d = sorted(w for w, _, _, d in placed if d == "D")
    assert sorted(across.values()) == want_a, f"across runs differ: {sorted(across.values())} vs {want_a}"
    assert sorted(down.values()) == want_d, f"down runs differ: {sorted(down.values())} vs {want_d}"
    for w, r, c, d in placed:  # every entry starts on a numbered cell and reads correctly from there
        n = nums[(r, c)]
        assert (across if d == "A" else down)[n] == w, f"{w} does not match the run at its number {n}"
        assert w in clue_words, f"{w} has no clue"
    assert len({w for w, _, _, _ in placed}) == len(placed), "a word is used twice"
    # every entry crosses at least one other entry, and the whole grid is one connected piece
    cells = {(r, c) for r, row in enumerate(g) for c, ch in enumerate(row) if ch}
    for w, r, c, d in placed:
        mine = [(r, c + i) if d == "A" else (r + i, c) for i in range(len(w))]
        other = set()
        for w2, r2, c2, d2 in placed:
            if w2 != w:
                other |= {(r2, c2 + i) if d2 == "A" else (r2 + i, c2) for i in range(len(w2))}
        assert any(p in other for p in mine), f"{w} crosses nothing"
    seen, stack = set(), [next(iter(cells))]
    while stack:
        p = stack.pop()
        if p in seen:
            continue
        seen.add(p)
        for q in ((p[0] + 1, p[1]), (p[0] - 1, p[1]), (p[0], p[1] + 1), (p[0], p[1] - 1)):
            if q in cells:
                stack.append(q)
    assert seen == cells, "grid is not connected"
    return g, nums, across, down
