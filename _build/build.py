#!/usr/bin/env python3
"""Builds the DIVELUX printables. Usage: python3 build.py [slug ...]   (no args = all)

Steps: write HTML sources -> render PDFs (one Chromium, under the shared lock) -> add PDF metadata,
check page count / page size / live link on every page -> page PNGs for review in /tmp/pr-png -> preview.png.
"""
import importlib
import json
import os
import subprocess
import sys

from PIL import Image
from pypdf import PdfReader, PdfWriter

import common as C

MODULES = ["p01_rules", "p02_etiquette", "p03_care", "p04_temps", "p05_types", "p06_guestbook",
           "p07_gift", "p08_words", "p09_puzzles", "p10_schedule", "p11_bingo",
           # wave 2
           "p12_pocket", "p13_journal", "p14_invites", "p15_traditions", "p16_coloring", "p17_woodstove",
           "p18_workbook", "p19_buying", "p20_whisk", "p21_plunge", "p22_tape", "p23_signs",
           # wave 3
           "p55_embroidery", "p56_applique", "p57_gnome", "p59_rituals"]
PNG = "/tmp/pr-png"
DATE = "D:20261120000000Z"


def inches(v):
    return float(v[:-2]) if v.endswith("in") else float(v[:-2]) / 25.4


def finalize(job, rep):
    problems = list(rep["problems"])
    raw = job["pdf"] + ".raw"
    r = PdfReader(raw)
    if len(r.pages) != rep["pages"]:
        problems.append(f"PDF has {len(r.pages)} pages, HTML has {rep['pages']} sheets")
    w_pt, h_pt = inches(job["width"]) * 72, inches(job["height"]) * 72
    for i, pg in enumerate(r.pages):
        if abs(float(pg.mediabox.width) - w_pt) > 1 or abs(float(pg.mediabox.height) - h_pt) > 1:
            problems.append(f"page {i + 1}: size {pg.mediabox.width}x{pg.mediabox.height}pt")
        uris = [a.get_object().get("/A", {}).get("/URI") for a in pg.get("/Annots", [])]
        if not any(u and "diveluxsaunahat.com" in u for u in uris):
            problems.append(f"page {i + 1}: no live link to diveluxsaunahat.com")
    w = PdfWriter(clone_from=r)
    m = job["meta"]
    w.add_metadata({"/Title": m["title"], "/Author": "DIVELUX", "/Subject": m["subject"], "/Keywords": m["keywords"],
                    "/Creator": "DIVELUX (https://diveluxsaunahat.com)", "/CreationDate": DATE, "/ModDate": DATE})
    w.compress_identical_objects()
    with open(job["pdf"], "wb") as f:
        w.write(f)
    os.remove(raw)
    base = os.path.basename(job["pdf"])[:-4]
    for old in os.listdir(PNG):
        if old.startswith(base + "-p"):
            os.remove(os.path.join(PNG, old))
    subprocess.run(["pdftoppm", "-r", "80", "-png", job["pdf"], os.path.join(PNG, base + "-p")], check=True)
    return len(r.pages), problems


def make_preview(prod):
    """preview.png: page 1 for one-page products, a row of the first pages otherwise."""
    pv = prod["preview"]
    pages = pv.get("pages", [1])
    tmp = "/tmp/pr-prev"
    subprocess.run(["pdftoppm", "-r", str(pv.get("dpi", 150 if len(pages) == 1 else 75)), "-png", pv["pdf"], tmp], check=True)
    files = sorted(f for f in os.listdir("/tmp") if f.startswith("pr-prev-") and f.endswith(".png"))
    ims = []
    for n in pages:
        match = [f for f in files if int(f[len("pr-prev-"):-4]) == n]
        ims.append(Image.open(os.path.join("/tmp", match[0])).convert("RGB"))
    out = os.path.join(C.ROOT, prod["slug"], "preview.png")
    if len(ims) == 1:
        ims[0].save(out, optimize=True)
    else:
        cols = pv.get("cols", len(ims))
        rows = -(-len(ims) // cols)
        g = 24
        cw, ch = max(i.width for i in ims), max(i.height for i in ims)
        sheet = Image.new("RGB", (cols * cw + (cols + 1) * g, rows * ch + (rows + 1) * g), "#cfc9c0")
        for k, im in enumerate(ims):
            sheet.paste(im, (g + (k % cols) * (cw + g), g + (k // cols) * (ch + g)))
        sheet.save(out, optimize=True)
    for f in files:
        os.remove(os.path.join("/tmp", f))


def main():
    want = sys.argv[1:]
    os.makedirs(PNG, exist_ok=True)
    prods = []
    for name in MODULES:
        if want and not any(w in name for w in want):
            continue
        prods.append(importlib.import_module(name).build())
    jobs = [j for p in prods for j in p["jobs"]]
    json.dump(jobs, open("/tmp/pr-jobs.json", "w"))
    subprocess.run("NODE_PATH=/opt/carmax/node_modules flock /tmp/freebies-chromium.lock node "
                   f"{C.B}/render.js /tmp/pr-jobs.json /tmp/pr-report.json", shell=True, check=True)
    report = {r["pdf"]: r for r in json.load(open("/tmp/pr-report.json"))}
    bad = 0
    for p in prods:
        for j in p["jobs"]:
            n, problems = finalize(j, report[j["pdf"]])
            print(f"{os.path.relpath(j['pdf'], C.ROOT)}: {n} p, {os.path.getsize(j['pdf']) // 1024} KB",
                  "OK" if not problems else "")
            for pr in problems:
                bad += 1
                print("   !!", pr)
        make_preview(p)
    print("problems:", bad)


if __name__ == "__main__":
    main()
