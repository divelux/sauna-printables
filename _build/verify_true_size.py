#!/usr/bin/env python3
"""Measures the true-size check squares (1 in and 2 cm) on every page of the embroidery and appliqué PDFs,
and two known shapes: the 6 in spacing strip (embroidery p5) and the 1.6 in round name patch (appliqué p3). Usage: python3 verify_true_size.py"""
import os
import sys
import fitz
import common as C

TOL = 0.06
bad = 0
for slug, pages in (("sauna-hat-embroidery-monogram-patterns", [2, 3, 4, 5, 7]), ("felt-applique-templates-for-hats", [2, 3])):
    for paper in ("letter", "a4"):
        doc = fitz.open(os.path.join(C.ROOT, slug, f"{slug}-{paper}.pdf"))
        for n in pages:
            pg = doc[n - 1]
            sq = []
            for dr in pg.get_drawings():
                for it in dr["items"]:
                    if it[0] == "re" and dr.get("fill") and abs(it[1].width - it[1].height) < .2 and 50 < it[1].width < 80:
                        sq.append(round(it[1].width, 3))
            want = sorted([72.0, 200 / 2.54 / 100 * 72])
            got = sorted(set(sq))
            ok = len(got) == 2 and all(abs(g - w) <= TOL for g, w in zip(got, want))
            extra = ""
            if slug.startswith("sauna-hat") and n == 5:
                rects = [it[1] for dr in pg.get_drawings() for it in dr["items"] if it[0] == "re" and it[1].width > 400]
                strip = [r for r in rects if abs(r.height - 64 / 100 * 72) < .5]
                ok = ok and len(strip) == 1 and abs(strip[0].width - 6 * 72) <= TOL
                extra = f", spacing strip {strip[0].width / 72:.4f} in" if strip else ", spacing strip not found"
            if slug.startswith("felt") and n == 3:
                circ = [dr["rect"] for dr in pg.get_drawings() if dr.get("fill") and abs(dr["rect"].width - 1.6 * 72) < .3 and abs(dr["rect"].height - 1.6 * 72) < .3]
                ok = ok and len(circ) == 1 and abs(circ[0].width - 115.2) <= .15
                extra = f", round name patch {circ[0].width / 72:.4f} in (want 1.6)" if circ else ", round patch not found"
            bad += not ok
            print(f"{'OK' if ok else '!!'} {slug} {paper} p{n}: squares {got} pt (want {[round(w, 3) for w in want]}){extra}")
print("true-size problems:", bad)
sys.exit(1 if bad else 0)
