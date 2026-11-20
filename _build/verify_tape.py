#!/usr/bin/env python3
"""Measures the finished measuring-tape PDFs: strip length, tick positions and the scale check lines must be true to size.
Usage: python3 verify_tape.py   (needs PyMuPDF)"""
import os
import sys
import fitz
import common as C

SLUG = "sauna-hat-size-measuring-tape"
TOL = 0.06          # points; 0.06 pt = 0.02 mm
bad = 0
for paper in ("letter", "a4"):
    pg = fitz.open(os.path.join(C.ROOT, SLUG, f"{SLUG}-{paper}.pdf"))[0]
    rects, lines, ticks = [], [], []
    for dr in pg.get_drawings():
        for it in dr["items"]:
            if it[0] == "re" and it[1].width > 600 and 55 < it[1].height < 70 and dr.get("fill"):
                rects.append(it[1])
            if it[0] == "l":
                p1, p2 = it[1], it[2]
                if abs(p1.y - p2.y) < 0.01 and abs(p2.x - p1.x) > 200 and dr.get("width", 0) and abs(dr["width"] - 1.05) < 0.2:
                    lines.append(abs(p2.x - p1.x))
                if abs(p1.x - p2.x) < 0.01 and 3 < abs(p2.y - p1.y) < 17:
                    ticks.append((round(min(p1.y, p2.y), 1), p1.x))
    rects.sort(key=lambda r: r.y0)
    want = [(9.5 * 72, .875 * 72), (9.5 * 72, .875 * 72), (9 * 72, .875 * 72)]
    checks = [(f"strip {i + 1} size", (r.width, r.height), w) for i, (r, w) in enumerate(zip(rects, want))]
    lines = sorted(set(round(v, 3) for v in lines), reverse=True)[:3]
    checks.append(("check lines 4 in / 10 cm / 85.6 mm", tuple(lines), (288.0, 100 / 25.4 * 72, 85.6 / 25.4 * 72)))
    # inch ticks of strip 1: 73 ticks, 9 pt apart, starting at the strip's left edge
    top = sorted(x for y, x in ticks if abs(y - rects[0].y0) < 0.3)
    step = [round(b - a, 3) for a, b in zip(top, top[1:])]
    checks.append(("strip 1 inch ticks: count, first-to-last", (len(top), top[-1] - top[0]), (73, 648.0)))
    checks.append(("strip 1 inch ticks: widest and narrowest gap", (max(step), min(step)), (9.0, 9.0)))
    print(paper)
    for name, got, exp in checks:
        ok = len(got) == len(exp) and all(abs(g - e) <= TOL for g, e in zip(got, exp))
        bad += not ok
        print(f"  {'OK' if ok else '!!'} {name}: got {tuple(round(g, 3) for g in got)}, expected {tuple(round(e, 3) for e in exp)}")
print("tape problems:", bad)
sys.exit(1 if bad else 0)
