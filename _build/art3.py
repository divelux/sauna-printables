"""Vector art for the wave 3 printables: embroidery (p55), felt appliqué (p56) and the sauna tonttu story (p57).
Plain SVG written by code: line letters, stitch diagrams, motifs, cut shapes, a small tonttu character.
No raster or generated images. True-size pieces use 100 units = 1 inch.
Run `python3 art3.py` to write test PNGs to /tmp/pr-art3/."""
import math
import os
import sys

from shapely import affinity
from shapely.geometry import LineString, Point, Polygon
from shapely.ops import unary_union

import art
from art import INK, f, ln, sh

sys.path.insert(0, "/root/divelux/freebies/gfx/_tools")
import gfxlib  # noqa: E402  (text -> path, Bricolage Grotesque, SIL OFL 1.1)

U = 100  # units per inch in true-size art


def tsvg(w, h, body, sw=1.6, extra="", fill="none"):
    """True-size SVG: w and h in units (100 = 1 in). The viewBox is in CSS pixels (96 per inch), so the SVG viewport
    maps 1:1 to the page; the art is scaled by 0.96 inside a group. The size is rounded up to whole pixels:
    Chromium snaps SVG viewports to whole pixels when printing, which would otherwise shrink the art slightly."""
    pw, ph = math.ceil(w * .96 - 1e-6), math.ceil(h * .96 - 1e-6)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{pw}" height="{ph}" '
            f'viewBox="0 0 {pw} {ph}" style="width:{pw}px;height:{ph}px;flex:none;max-width:none" fill="{fill}" stroke="{INK}" '
            f'stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"{extra}><g transform="scale(.96)">{body}</g></svg>')


def geom_d(g, nd=1):
    """Shapely (Multi)Polygon -> SVG path data."""
    polys = getattr(g, "geoms", [g])
    out = []
    for p in polys:
        for ring in [p.exterior, *p.interiors]:
            c = list(ring.coords)[:-1]
            out.append("M" + "L".join(f"{c0:.{nd}f} {c1:.{nd}f}" for c0, c1 in c) + "Z")
    return "".join(out)


# ------------------------------------------------------------------ single-line capitals (cap height 100)
MONO = {
    "A": (70, "M0 100L35 0L70 100M13 64H57"),
    "B": (66, "M0 100V0H36C56 0 62 12 62 25C62 38 54 47 36 47H0M36 47C58 47 66 59 66 73C66 88 56 100 38 100H0"),
    "C": (72, "M72 20C64 7 53 0 40 0C16 0 0 22 0 50C0 78 16 100 40 100C53 100 64 93 72 80"),
    "D": (70, "M0 0V100H30C56 100 70 80 70 50C70 20 56 0 30 0Z"),
    "E": (60, "M60 0H0V100H60M0 48H50"),
    "F": (58, "M58 0H0V100M0 48H50"),
    "G": (74, "M72 20C64 7 53 0 40 0C16 0 0 22 0 50C0 78 16 100 40 100C60 100 74 88 74 64V54H44"),
    "H": (68, "M0 0V100M68 0V100M0 48H68"),
    "I": (0, "M0 0V100"),
    "J": (48, "M48 0V70C48 90 38 100 24 100C10 100 0 90 0 74"),
    "K": (64, "M0 0V100M64 0L0 64M22 42L66 100"),
    "L": (56, "M0 0V100H56"),
    "M": (84, "M0 100V0L42 72L84 0V100"),
    "N": (70, "M0 100V0L70 100V0"),
    "O": (84, "M42 0C65 0 84 22 84 50C84 78 65 100 42 100C19 100 0 78 0 50C0 22 19 0 42 0Z"),
    "P": (64, "M0 100V0H36C56 0 64 13 64 27C64 41 56 54 36 54H0"),
    "Q": (84, "M42 0C65 0 84 22 84 50C84 78 65 100 42 100C19 100 0 78 0 50C0 22 19 0 42 0ZM52 72L86 106"),
    "R": (66, "M0 100V0H36C56 0 64 13 64 27C64 41 56 54 36 54H0M32 54L66 100"),
    "S": (64, "M62 17C56 6 46 0 33 0C16 0 4 10 4 25C4 41 17 46 33 50C52 55 64 61 64 76C64 92 51 100 33 100C18 100 6 94 0 82"),
    "T": (68, "M0 0H68M34 0V100"),
    "U": (68, "M0 0V64C0 88 14 100 34 100C54 100 68 88 68 64V0"),
    "V": (70, "M0 0L35 100L70 0"),
    "W": (100, "M0 0L23 100L50 24L77 100L100 0"),
    "X": (66, "M0 0L66 100M66 0L0 100"),
    "Y": (68, "M0 0L34 52L68 0M34 52V100"),
    "Z": (66, "M0 0H66L0 100H66"),
}


def mono_letter(ch, x, y, h, sw):
    """Single-line capital with its top-left at (x, y), cap height h. Returns (markup, advance)."""
    w, d = MONO[ch]
    s = h / 100
    return (f'<path d="{d}" transform="translate({f(x)} {f(y)}) scale({f(s)})" fill="none" '
            f'stroke-width="{f(sw / s)}"/>', w * s)


class _FlatPen:
    """fontTools pen that flattens a glyph into point lists (one per contour)."""
    def __init__(self, glyphset):
        from fontTools.pens.basePen import BasePen

        outer = self

        class P(BasePen):
            def _moveTo(self, p):
                outer.cur = [p]

            def _lineTo(self, p):
                outer.cur.append(p)

            def _curveToOne(self, p1, p2, p3):
                p0 = outer.cur[-1]
                outer.cur += [tuple((1 - t) ** 3 * a + 3 * (1 - t) ** 2 * t * b + 3 * (1 - t) * t * t * c + t ** 3 * d
                                    for a, b, c, d in zip(p0, p1, p2, p3)) for t in (i / 12 for i in range(1, 13))]

            def _qCurveToOne(self, p1, p2):
                p0 = outer.cur[-1]
                outer.cur += [tuple((1 - t) ** 2 * a + 2 * (1 - t) * t * b + t * t * c for a, b, c in zip(p0, p1, p2))
                              for t in (i / 10 for i in range(1, 11))]

            def _closePath(self):
                outer.contours.append(outer.cur)

            _endPath = _closePath

        self.contours, self.cur = [], []
        self.pen = P(glyphset)


def glyph_geom(ch, size):
    """Filled area of a Bricolage capital as a shapely geometry (overlapping contours merged), y down, baseline 0, left 0."""
    t, gs, cmap, upm, kern = gfxlib._font("display")
    fp = _FlatPen(gs)
    gs[cmap[ord(ch)]].draw(fp.pen)
    s = size / upm
    fills, holes = [], []
    for c in fp.contours:
        if len(c) < 3:
            continue
        p = Polygon([(x * s, -y * s) for x, y in c]).buffer(0)
        # TrueType: outer contours run clockwise in font units (y up)
        area2 = sum(x0 * y1 - x1 * y0 for (x0, y0), (x1, y1) in zip(c, c[1:] + c[:1]))
        (holes if area2 > 0 else fills).append(p)
    g = unary_union(fills)
    if holes:
        g = g.difference(unary_union(holes))
    return g


def outline_letter(ch, x, baseline, size):
    """Outline capital (Bricolage Grotesque Bold), centered on x, for padded satin stitch. Returns path markup."""
    g = glyph_geom(ch, size)
    x0, y0, x1, y1 = g.bounds
    g = affinity.translate(g, x - (x0 + x1) / 2, baseline)
    return f'<path d="{geom_d(g)}" fill="none"/>'


def outline_width(ch, size):
    return gfxlib.text_width(ch, size, kind="display")


# ------------------------------------------------------------------ embroidery motifs (100 units = 1 in)

def m_steam():
    o = []
    for i, x in enumerate((28, 64, 100)):
        top = 22 if i == 1 else 40
        o.append(ln(f"M{x} 150C{x - 22} 128 {x + 22} 108 {x} {86}C{x - 22} 64 {x + 18} {top + 18} {x + 2} {top}"))
    return 128, 164, "".join(o)


def m_snowflake(r=74):
    cx = cy = r + 8
    d = ""
    knots = ""
    for k in range(6):
        a = math.radians(60 * k - 90)
        ca, sa = math.cos(a), math.sin(a)
        d += f"M{f(cx + 14 * ca)} {f(cy + 14 * sa)}L{f(cx + r * ca)} {f(cy + r * sa)}"
        for fr, ln_ in ((.48, .3), (.74, .22)):
            mx, my = cx + r * fr * ca, cy + r * fr * sa
            for side in (-1, 1):
                b = a + side * math.radians(42)
                d += f"M{f(mx)} {f(my)}L{f(mx + r * ln_ * math.cos(b))} {f(my + r * ln_ * math.sin(b))}"
        knots += f'<circle cx="{f(cx + (r + 7) * ca)}" cy="{f(cy + (r + 7) * sa)}" r="3.2" fill="{INK}" stroke="none"/>'
    hexa = "M" + "L".join(f"{f(cx + 14 * math.cos(math.radians(60 * k - 90)))} {f(cy + 14 * math.sin(math.radians(60 * k - 90)))}" for k in range(6)) + "Z"
    return 2 * cx, 2 * cy, ln(d) + ln(hexa) + knots


def leaf_shape(x, y, ang, L, W, vein=True):
    d = (f"M0 0C{f(L * .2)} {f(-W)} {f(L * .62)} {f(-W * .92)} {f(L)} 0"
         f"C{f(L * .62)} {f(W * .92)} {f(L * .2)} {f(W)} 0 0Z")
    v = f'<path d="M{f(L * .08)} 0L{f(L * .78)} 0" fill="none"/>' if vein else ""
    return f'<g transform="translate({f(x)} {f(y)}) rotate({f(ang)})"><path d="{d}" fill="none"/>{v}</g>'


def m_birch():
    o = [ln("M14 210C40 170 70 120 92 70C102 48 110 30 118 14")]
    for (x, y, a, L) in ((40, 166, -160, 52), (52, 146, -40, 56), (72, 108, -165, 50), (84, 86, -30, 52), (104, 46, -150, 44), (118, 14, -70, 40)):
        o.append(leaf_shape(x, y, a, L, L * .36))
    return 182, 222, "".join(o)


def m_spruce():
    o = [ln("M70 8V196")]
    d = ""
    n = 7
    for i in range(n):
        y = 34 + i * 22
        w = 14 + i * 7.5
        d += f"M70 {f(y - 12)}L{f(70 - w)} {f(y + 8)}M70 {f(y - 12)}L{f(70 + w)} {f(y + 8)}"
    o.append(ln(d))
    o.append(ln("M52 196H88"))
    return 140, 204, "".join(o)


def m_ladle():
    o = [ln("M62 74L196 14"), ln("M196 14l10 -4"),
         '<path d="M8 66C8 92 30 110 56 110C82 110 104 92 104 66Z" fill="none"/>', ln("M8 66H104"),
         ln("M24 84C40 92 72 92 88 84", ' stroke-dasharray="1 9"')]
    return 214, 120, "".join(o)


def m_stones():
    o = ['<ellipse cx="70" cy="138" rx="62" ry="24" fill="none"/>',
         '<ellipse cx="66" cy="94" rx="46" ry="20" fill="none"/>',
         '<ellipse cx="72" cy="56" rx="32" ry="16" fill="none"/>',
         '<ellipse cx="68" cy="26" rx="18" ry="11" fill="none"/>']
    return 140, 170, "".join(o)


def m_flame():
    d = "M60 6C66 44 104 60 104 104A44 44 0 0 1 16 104C16 84 26 70 36 60C40 76 46 82 52 86C46 56 50 30 60 6Z"
    i = "M60 76C70 90 78 100 78 114A18 18 0 0 1 42 114C42 100 50 90 60 76Z"
    return 120, 160, ln(d) + ln(i)


def m_cabin():
    o = [ln("M22 84L90 30L158 84"), ln("M36 74V168H144V74"), ln("M78 168V118H102V168"),
         ln("M116 52V30H132V64"), ln("M124 22c-10 -8 8 -14 -2 -22"),
         '<rect x="48" y="100" width="22" height="22" fill="none"/>', ln("M59 100V122M48 111H70"),
         ln("M12 168H170")]
    return 182, 178, "".join(o)


def m_wreath(r=118, n=8):
    """Birch-leaf wreath frame for a monogram, open at the top. Leaves scale with the radius."""
    pad = r * .34
    cx = cy = r + pad
    L, W = r * .3, r * .3 * .36
    a0, a1 = math.radians(112), math.radians(68)
    o = [f'<path d="M{f(cx + r * math.cos(a0))} {f(cy - r * math.sin(a0))}'
         f'A{f(r)} {f(r)} 0 1 0 {f(cx + r * math.cos(a1))} {f(cy - r * math.sin(a1))}" fill="none"/>']
    for side in (-1, 1):
        for k in range(n):
            deg = 270 + side * (16 + k * 140 / (n - 1))   # screen angle, 270 = bottom... measured clockwise from +x with y down
            a = math.radians(deg)
            x, y = cx + r * math.cos(a), cy - r * math.sin(a)
            # tangent direction pointing toward the top gap
            tang = -deg + (-90 if side > 0 else 90)
            for out in (1, -1):
                o.append(leaf_shape(x, y, tang + out * 34, L, W, vein=False))
    o.append(f'<circle cx="{f(cx)}" cy="{f(cy + r)}" r="{f(r * .05)}" fill="none"/>')
    return 2 * cx, 2 * cy, "".join(o)


MOTIFS = [
    ("Steam", "Stem stitch, 2 strands", m_steam),
    ("Snowflake", "Back stitch + French knots", m_snowflake),
    ("Birch sprig", "Stem stitch stem, lazy daisy or satin leaves", m_birch),
    ("Spruce", "Back stitch, or fly stitch branches", m_spruce),
    ("Ladle", "Back stitch, running stitch dots", m_ladle),
    ("Sauna stones", "Stem stitch or split stitch", m_stones),
    ("Flame", "Split stitch outline, satin center", m_flame),
    ("Sauna cabin", "Back stitch", m_cabin),
]


# ------------------------------------------------------------------ stitch diagrams (not to scale, box 200 x 90)

def _needle(x, y, ang):
    return (f'<g transform="translate({f(x)} {f(y)}) rotate({f(ang)})"><path d="M0 0L44 -3.4A3.6 3.6 0 0 1 44 3.4Z" fill="#fff"/>'
            f'<ellipse cx="38" cy="0" rx="3.6" ry="1.2" fill="none" stroke-width="1"/></g>')


def stitch_running():
    d = "".join(f"M{16 + i * 34} 50h20" for i in range(5))
    return ln(d, ' stroke-width="4"') + ln("M10 62H196", ' stroke-width="1" stroke-dasharray="2 4" opacity=".5"')


def stitch_back():
    d = "".join(f"M{17 + i * 30} 50h26" for i in range(6))
    return ln(d, ' stroke-width="4"') + ln("M10 62H196", ' stroke-width="1" stroke-dasharray="2 4" opacity=".5"')


def stitch_stem():
    d = "".join(f"M{12 + i * 17} 57L{46 + i * 17} 43" for i in range(9))
    return ln(d, ' stroke-width="4"')


def stitch_split():
    o = ""
    for i in range(6):
        x = 14 + i * 28
        o += f'<path d="M{x} 50C{x + 8} 42 {x + 26} 42 {x + 34} 50C{x + 26} 58 {x + 8} 58 {x} 50Z" fill="#fff" stroke-width="2.2"/>'
    return o


def stitch_satin():
    hh = lambda x: 32 * math.sin(math.pi * (x - 20) / 166) ** .8 if 20 <= x <= 186 else 0
    leaf = "M" + "L".join(f"{f(x)} {f(50 - hh(x))}" for x in range(20, 187, 2)) + "L" + "L".join(f"{f(x)} {f(50 + hh(x))}" for x in range(186, 19, -2)) + "Z"
    lines = ""
    for i in range(1, 19):
        x = 20 + i * 8.7
        lines += f"M{f(x - 4)} {f(50 + hh(x - 4))}L{f(x + 4)} {f(50 - hh(x + 4))}"
    return ln(leaf, ' stroke-width="1.2" stroke-dasharray="3 3"') + ln(lines, ' stroke-width="3"')


def stitch_french():
    o = ""
    for i, x in enumerate((40, 80, 120, 160)):
        o += f'<circle cx="{x}" cy="50" r="9" fill="#fff" stroke-width="2.4"/><path d="M{x - 5} 47q5 -6 10 0q-5 7 -10 0" fill="none" stroke-width="1.6"/>'
    return o


def stitch_daisy():
    o = ""
    cx, cy = 100, 50
    for k in range(6):
        a = 60 * k
        o += (f'<g transform="rotate({a} {cx} {cy})"><path d="M{cx} {cy - 6}C{cx - 11} {cy - 20} {cx - 8} {cy - 36} {cx} {cy - 38}'
              f'C{cx + 8} {cy - 36} {cx + 11} {cy - 20} {cx} {cy - 6}Z" fill="#fff" stroke-width="2.6"/>'
              f'<path d="M{cx - 3} {cy - 41}L{cx + 3} {cy - 36}" stroke-width="2.6"/></g>')
    return o + f'<circle cx="{cx}" cy="{cy}" r="4" fill="{INK}" stroke="none"/>'


def stitch_blanket():
    o = ln("M14 66H190", ' stroke-width="3.4"')
    o += ln("M14 70H190", ' stroke-width="1" stroke-dasharray="2 4" opacity=".5"')
    o += ln("".join(f"M{20 + i * 24} 66V36" for i in range(8)), ' stroke-width="3.4"')
    o += '<rect x="10" y="20" width="184" height="46" fill="none" stroke-width="1" stroke-dasharray="4 4"/>'
    return o


def stitch_whip():
    o = '<rect x="10" y="20" width="184" height="46" fill="none" stroke-width="1" stroke-dasharray="4 4"/>'
    o += ln("".join(f"M{16 + i * 23} 80L{28 + i * 23} 52" for i in range(8)), ' stroke-width="3.4"')
    return o


def stitch_box(inner):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 206 92" fill="none" stroke="{INK}" stroke-width="3" '
            f'stroke-linecap="round" stroke-linejoin="round" font-family="Inter" aria-hidden="true">{inner}</svg>')


# ------------------------------------------------------------------ appliqué cut shapes (shapely, 100 units = 1 in)

def _bez(p0, p1, p2, p3, n=24):
    return [((1 - t) ** 3 * p0[0] + 3 * (1 - t) ** 2 * t * p1[0] + 3 * (1 - t) * t * t * p2[0] + t ** 3 * p3[0],
             (1 - t) ** 3 * p0[1] + 3 * (1 - t) ** 2 * t * p1[1] + 3 * (1 - t) * t * t * p2[1] + t ** 3 * p3[1])
            for t in (i / n for i in range(n))]


def g_leaf(L=220, W=72, teeth=7):
    """Birch-like leaf with a short stem at the left. Smooth edge, easy to cut from felt."""
    top = _bez((0, 0), (L * .16, -W), (L * .62, -W * .92), (L, 0), 60)
    bot = _bez((L, 0), (L * .62, W * .92), (L * .16, W), (0, 0), 60)
    leaf = Polygon(top + bot).buffer(0)
    stem = LineString([(-28, 8), (6, 0)]).buffer(8, cap_style=1)
    return unary_union([leaf, stem])


def g_tree():
    tiers = []
    for i, (w, y0, h) in enumerate(((170, 210, 96), (136, 150, 86), (96, 96, 74))):
        tiers.append(Polygon([(100 - w / 2, y0), (100, y0 - h), (100 + w / 2, y0)]))
    trunk = Polygon([(84, 205), (116, 205), (116, 246), (84, 246)])
    return unary_union(tiers + [trunk]).buffer(5).buffer(-5)


def g_snowflake(r=112):
    parts = []
    for k in range(6):
        a = math.radians(60 * k - 90)
        ca, sa = math.cos(a), math.sin(a)
        parts.append(LineString([(0, 0), (r * ca, r * sa)]).buffer(13, cap_style=1))
        mx, my = r * .58 * ca, r * .58 * sa
        for side in (-1, 1):
            b = a + side * math.radians(45)
            parts.append(LineString([(mx, my), (mx + r * .34 * math.cos(b), my + r * .34 * math.sin(b))]).buffer(11, cap_style=1))
    g = unary_union(parts + [Point(0, 0).buffer(34)])
    return affinity.translate(g, r + 20, r + 20)


def g_star(R=110, r=50, round_=8):
    pts = [((R if k % 2 == 0 else r) * math.sin(math.radians(36 * k)), -(R if k % 2 == 0 else r) * math.cos(math.radians(36 * k))) for k in range(10)]
    g = Polygon(pts).buffer(-round_).buffer(round_)
    return affinity.translate(g, R, R)


def g_heart(s=1.0):
    pts = _bez((100, 50), (100, 10), (160, -6), (186, 24), 40) + _bez((186, 24), (214, 60), (170, 120), (100, 176), 40) \
        + _bez((100, 176), (30, 120), (-14, 60), (14, 24), 40) + _bez((14, 24), (40, -6), (100, 10), (100, 50), 40)
    return affinity.scale(Polygon(pts).buffer(0), s, s, origin=(0, 0))


def g_flame(s=1.0):
    pts = (_bez((100, 0), (110, 64), (176, 92), (176, 160), 40) + _bez((176, 160), (176, 210), (138, 240), (100, 240), 30)
           + _bez((100, 240), (60, 240), (24, 210), (24, 160), 30) + _bez((24, 160), (24, 128), (40, 108), (58, 92), 30)
           + _bez((58, 92), (62, 116), (72, 124), (82, 130), 20) + _bez((82, 130), (74, 86), (80, 40), (100, 0), 30))
    return affinity.scale(Polygon(pts).buffer(0), s, s, origin=(0, 0))


def g_flame_inner():
    pts = (_bez((100, 110), (122, 140), (138, 160), (138, 190), 30) + _bez((138, 190), (138, 214), (120, 226), (100, 226), 20)
           + _bez((100, 226), (80, 226), (62, 214), (62, 190), 20) + _bez((62, 190), (62, 160), (78, 140), (100, 110), 30))
    return Polygon(pts).buffer(0)


def g_cloud():
    circles = [Point(60, 100).buffer(44), Point(118, 74).buffer(58), Point(186, 84).buffer(50), Point(236, 108).buffer(36)]
    base = Polygon([(60, 100), (236, 100), (236, 144), (60, 144)])
    g = unary_union(circles + [base, Point(60, 110).buffer(34), Point(236, 112).buffer(32)])
    g = g.buffer(6).buffer(-6)
    return affinity.translate(g, -10, -10)


def g_ladle():
    bowl = Point(0, 0).buffer(62)
    bowl = bowl.intersection(Polygon([(-80, -14), (80, -14), (80, 80), (-80, 80)]))
    bowl = bowl.buffer(4).buffer(-4)
    handle = LineString([(40, -10), (230, -126)]).buffer(18, cap_style=1)
    knob = Point(232, -128).buffer(24)
    g = unary_union([bowl, handle, knob])
    return affinity.translate(g, 70, 156)


def g_circle(r=100):
    return Point(r, r).buffer(r, 128)


def g_scallop(r=110, n=14):
    base = Point(0, 0).buffer(r - 14, 128)
    bumps = [Point((r - 14) * math.cos(2 * math.pi * k / n), (r - 14) * math.sin(2 * math.pi * k / n)).buffer(22, 32) for k in range(n)]
    return affinity.translate(unary_union([base] + bumps), r + 10, r + 10)


def g_drop(s=1.0):
    pts = _bez((60, 0), (78, 42), (120, 80), (120, 126), 40) + _bez((120, 126), (120, 160), (94, 186), (60, 186), 30) \
        + _bez((60, 186), (26, 186), (0, 160), (0, 126), 30) + _bez((0, 126), (0, 80), (42, 42), (60, 0), 40)
    return affinity.scale(Polygon(pts).buffer(0), s, s, origin=(0, 0))


def norm(g, pad=4):
    """Move a shape so its bounding box starts at (pad, pad). Returns (geom, w, h) with w, h including padding."""
    x0, y0, x1, y1 = g.bounds
    g = affinity.translate(g, pad - x0, pad - y0)
    return g, x1 - x0 + 2 * pad, y1 - y0 + 2 * pad


def cut_piece(g, inset=11, fill="#fbf1e5", extra=""):
    """Solid outline = cut line, dashed inner line = stitch line (inset 0.11 in), light fill."""
    inner = g.buffer(-inset, join_style=1)
    s = f'<path d="{geom_d(g)}" fill="{fill}" stroke-width="1.5"/>'
    if not inner.is_empty:
        s += f'<path d="{geom_d(inner)}" fill="none" stroke-width="1" stroke-dasharray="5 4" stroke="#6f655c"/>'
    return s + extra


# ------------------------------------------------------------------ the sauna tonttu (coloring style)

CAP_POLY = Polygon(_bez((-50, -196), (-48, -252), (-16, -302), (46, -330), 40) + _bez((46, -330), (34, -298), (40, -252), (50, -196), 40))
TUNIC_POLY = Polygon(_bez((-34, -142), (-52, -118), (-62, -70), (-64, -24), 30) + [(0, -17)] + _bez((64, -24), (62, -70), (52, -118), (34, -142), 30))


def _zig(x0, x1, y, h, step):
    pts, x, up = [], x0, False
    while x <= x1:
        pts.append((x, y - h if up else y))
        x += step
        up = not up
    return pts


def _clipped(poly, lines):
    """Open polylines cut to the inside of poly (shrunk a little so they stop short of the outline)."""
    inner = poly.buffer(-2.5)
    d = ""
    for pts in lines:
        g = LineString(pts).intersection(inner)
        for part in getattr(g, "geoms", [g]):
            if part.is_empty or part.geom_type != "LineString":
                continue
            d += "M" + "L".join(f"{f(a)} {f(b)}" for a, b in part.coords)
    return ln(d)

def tonttu(x, y, s=1.0, hold="", pattern=False, uid="t", flip=False, cap_fill=None, tunic_fill=None, boot_fill=None):
    """A small bearded sauna keeper in a pointed felt cap. Feet at (x, y); about 330 units tall at s = 1.
    hold: '' | 'ladle' | 'lantern' | 'whisk' (in the right hand) | 'wave' (left arm raised)."""
    o = []
    bf = f' fill="{boot_fill}"' if boot_fill else ""
    o.append(f'<ellipse cx="-27" cy="-11" rx="29" ry="13"{bf}/><ellipse cx="27" cy="-11" rx="29" ry="13"{bf}/>')
    tunic = "M-34 -142C-52 -118 -62 -70 -64 -24Q0 -10 64 -24C62 -70 52 -118 34 -142Z"
    o.append(sh(tunic, f' fill="{tunic_fill}"' if tunic_fill else ""))
    if pattern:
        o.append(_clipped(TUNIC_POLY, [[(-80, -42), (80, -42)]] + [_zig(-80, 80, -34, 9, 7.5)]))
    o.append(sh("M-60 -76Q0 -64 60 -76L61.5 -61Q0 -49 -61.5 -61Z"))
    o.append('<rect x="-11" y="-74" width="22" height="18" rx="3"/>')
    # left arm (viewer's left)
    if hold == "wave":
        o.append(sh("M-36 -132C-60 -146 -76 -168 -80 -190L-62 -196C-58 -178 -48 -160 -30 -150Z"))
        o.append('<circle cx="-72" cy="-200" r="13"/>')
    else:
        o.append(sh("M-38 -132C-62 -116 -78 -92 -80 -70L-60 -64C-58 -84 -48 -102 -32 -112Z"))
        o.append('<circle cx="-71" cy="-62" r="13"/>')
    # item in the right hand, drawn behind the mitten
    if hold == "ladle":
        o.append(sh("M66 -60L104 -176L114 -172L76 -56Z") + sh("M92 -206H150C150 -180 136 -166 121 -166C106 -166 92 -180 92 -206Z") + ln("M98 -198H144"))
    elif hold == "lantern":
        o.append(ln("M71 -50V-30") + '<rect x="56" y="-30" width="30" height="40" rx="4"/>' + sh("M52 -30H90L82 -40H60Z")
                 + art.flame(71, 2, .22, inner=False))
    elif hold == "whisk":
        o.append(sh("M68 -58L94 -110L102 -106L76 -54Z"))
        for k, (dx, dy, a) in enumerate(((96, -112, -120), (104, -120, -80), (92, -126, -150), (110, -110, -40), (100, -134, -100))):
            o.append(art.leaf(dx, dy, a, 46, 15, veins=False))
    o.append(sh("M38 -132C62 -116 78 -92 80 -70L60 -64C58 -84 48 -102 32 -112Z"))
    o.append('<circle cx="71" cy="-62" r="13"/>')
    # face, beard, nose
    o.append('<ellipse cx="0" cy="-162" rx="44" ry="32"/>')
    o.append(sh("M-44 -160C-58 -112 -40 -64 0 -52C40 -64 58 -112 44 -160C32 -146 16 -142 0 -146C-16 -142 -32 -146 -44 -160Z"))
    o.append(ln("M-18 -120C-14 -104 -6 -92 0 -86M18 -120C14 -104 6 -92 0 -86M-30 -132C-28 -112 -20 -98 -12 -88M30 -132C28 -112 20 -98 12 -88", ' stroke-width="2"'))
    o.append('<ellipse cx="0" cy="-152" rx="14" ry="12"/>')
    o.append(ln("M-25 -171q7 -7 14 0M11 -171q7 -7 14 0"))
    # cap and its rolled edge
    cap = "M-50 -196C-48 -252 -16 -302 46 -330C34 -298 40 -252 50 -196Z"
    o.append(sh(cap, f' fill="{cap_fill}"' if cap_fill else ""))
    if pattern:
        o.append(_clipped(CAP_POLY, [[(-80, -226), (80, -226)], [(-80, -258), (80, -258)], _zig(-80, 80, -230, 10, 6)]))
        o.append("".join(f'<circle cx="{f(x)}" cy="-280" r="3.6"/>' for x in (-14, 0, 14, 28)
                         if CAP_POLY.buffer(-6).contains(Point(x, -280))))
    o.append(sh("M46 -330C56 -332 62 -324 58 -316C54 -310 46 -316 46 -330Z", f' fill="{cap_fill}"' if cap_fill else ""))
    o.append('<rect x="-57" y="-208" width="114" height="26" rx="13"' + (f' fill="{cap_fill}"' if cap_fill else "") + '/>')
    o.append(ln("M-42 -195H42", ' stroke-dasharray="2 10"'))
    tf = f"translate({f(x)} {f(y)}) scale({f(-s if flip else s)} {f(s)})"
    return f'<g transform="{tf}" stroke-width="{f(3 / s)}">{"".join(o)}</g>'


def stove(x, y, s=1.0):
    """Sauna stove with a heap of stones, about 260 wide, 330 tall, base at y."""
    o = ['<rect x="-14" y="-40" width="18" height="40" rx="3"/><rect x="216" y="-40" width="18" height="40" rx="3"/>',
         '<rect x="0" y="-250" width="220" height="214" rx="10"/>',
         '<rect x="44" y="-196" width="132" height="98" rx="8"/>',
         art.flame(84, -110, .55) + art.flame(110, -106, .72) + art.flame(138, -110, .55),
         '<rect x="70" y="-78" width="80" height="20" rx="4"/>',
         '<rect x="-12" y="-272" width="244" height="24" rx="5"/>',
         art.stones(-6, 226, -268, 3, seed=7, r=24)]
    return f'<g transform="translate({f(x)} {f(y)}) scale({f(s)})" stroke-width="{f(3 / s)}">{"".join(o)}</g>'


def svg750(body, sw=3.0):
    return art.svg(750, 900, body, sw)


def page_t_stove():
    o = ['<rect x="30" y="30" width="690" height="760"/>']
    o.append(ln("".join(f"M{30 + 98.6 * i:.1f} 30V610" for i in range(1, 7))))
    o.append(sh("M30 610H720V790H30Z") + ln("M30 680H720M190 610V680M420 610V680M600 610V680M110 680V790M330 680V790M520 680V790"))
    o.append('<rect x="560" y="90" width="120" height="16" rx="8"/>' + ln("M600 106v20"))
    o.append(art.bell_hat(566, 124, .3, pattern=False, uid="tb1"))
    o.append(art.steam(240, 290, 120, 14) + art.steam(300, 270, 130, 14) + art.steam(360, 290, 120, 14))
    o.append(stove(190, 640, 1.0))
    o.append(tonttu(560, 690, .95, hold="ladle", uid="tt1"))
    o.append(art.bucket(80, 548, .36, ladle=False))
    o.append(ln("M40 842H710"))
    return svg750("".join(o))


def page_t_bench():
    o = ['<rect x="30" y="30" width="690" height="760"/>']
    o.append(ln("".join(f"M30 {30 + 64 * i}H720" for i in range(1, 7))))
    for y in (430, 610):
        o.append(sh(f"M30 {y}H720V{y + 34}H30Z"))
        o.append(sh(f"M30 {y + 34}H720V{y + 180 if y == 610 else y + 180}H30Z"))
        o.append(ln("".join(f"M{90 + 120 * k} {y + 34}V{min(y + 180, 790)}" for k in range(6))))
    o.append(sh("M30 790H720"))
    # folded towel on the top bench
    o.append('<rect x="96" y="372" width="170" height="58" rx="8"/>' + ln("M96 392H266M96 410H266") + ln("M112 382h20M228 420h22"))
    o.append(tonttu(440, 432, 1.08, hold="whisk", uid="tt2"))
    o.append(art.bucket(560, 528, .28, ladle=True))
    for x, y, a in ((180, 560, -30), (300, 574, 200), (120, 730, -60), (380, 720, 20), (650, 740, -100)):
        o.append(art.leaf(x, y, a, 44, 14))
    o.append(ln("M40 842H710"))
    return svg750("".join(o))


def page_t_night():
    o = ['<rect x="20" y="20" width="710" height="860" rx="6"/>']
    o.append('<path d="M618 112A58 58 0 1 1 560 60A46 46 0 1 0 618 112Z"/>')
    for (x, y, r) in ((90, 90, 12), (230, 60, 9), (360, 120, 11), (470, 70, 8), (680, 230, 10), (150, 210, 8), (420, 220, 7)):
        d = (f"M{x} {y - r}L{f(x + r * .3)} {f(y - r * .3)}L{x + r} {y}L{f(x + r * .3)} {f(y + r * .3)}L{x} {y + r}"
             f"L{f(x - r * .3)} {f(y + r * .3)}L{x - r} {y}L{f(x - r * .3)} {f(y - r * .3)}Z")
        o.append(sh(d))
    o.append(sh("M20 500C140 380 260 360 360 430C450 360 590 340 730 470V612H20Z"))
    o.append(art.pine(70, 590, 220, 100) + art.pine(684, 590, 260, 110))
    o.append(art.cabin(110, 262, .9))
    o.append(tonttu(560, 610, .62, hold="lantern", uid="tt3"))
    o.append('<path d="M20 612H730V880H20Z"/>')
    o.append(sh("M20 610C200 600 420 602 730 612V664C520 650 300 676 20 660Z"))
    o.append(sh("M430 716H640L612 752H460Z") + ln("M486 716V734M584 716V734"))
    for yy, xs in [(780, [80, 250, 470, 610]), (830, [150, 330, 520])]:
        o.append(ln("".join(f"M{x} {yy}q18 -12 36 0t36 0" for x in xs)))
    for x, top in ((60, 690), (90, 712), (120, 696)):
        o.append(ln(f"M{x} 760C{x + 4} 730 {x - 4} 720 {x + 2} {top + 40}") + f'<rect x="{x - 5}" y="{top}" width="14" height="44" rx="7"/>')
    return svg750("".join(o))


def page_t_portrait():
    o = []
    o.append(f'<circle cx="375" cy="440" r="330"/><circle cx="375" cy="440" r="312"/>')
    for k in range(20):
        a = math.radians(18 * k)
        o.append(art.leaf(375 + 321 * math.cos(a), 440 + 321 * math.sin(a), math.degrees(a) + 90, 36, 11, veins=False))
    o.append(art.steam(170, 520, 150, 16) + art.steam(580, 520, 150, 16))
    o.append(tonttu(375, 720, 1.55, pattern=True, hold="wave", uid="tt4"))
    for x, a in ((210, -150), (240, -40), (520, -140), (548, -30)):
        o.append(art.leaf(x, 722, a, 40, 13))
    o.append(ln("M170 724H580"))
    return svg750("".join(o))


T_PAGES = [
    ("By the warm stove", "The tonttu keeps an eye on the stove. Only grown-ups pour water on the stones.", page_t_stove),
    ("Tidy benches", "A clean bench and a quiet voice: that is how the tonttu likes it.", page_t_bench),
    ("Night by the lake", "A little light by the cabin. Who came out to look at the stars?", page_t_night),
    ("Your own tonttu", "Give the cap and tunic your own patterns and colors.", page_t_portrait),
]


if __name__ == "__main__":
    import fitz
    os.makedirs("/tmp/pr-art3", exist_ok=True)
    tests = {}
    for i, (t, _, fn) in enumerate(T_PAGES, 1):
        tests[f"t{i}"] = fn()
    cells = ""
    x = 10
    for name, _, fn in MOTIFS:
        w, h, b = fn()
        cells += f'<g transform="translate({x} 10)">{b}</g>'
        x += w + 20
    tests["motifs"] = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {x} 240" fill="none" stroke="{INK}" stroke-width="1.6">{cells}</svg>'
    letters = ""
    x = 10
    for ch in MONO:
        m, adv = mono_letter(ch, x, 20, 80, 1.8)
        letters += m
        x += adv + 26
    tests["mono"] = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {x} 120" fill="none" stroke="{INK}" stroke-linecap="round" stroke-linejoin="round">{letters}</svg>'
    shapes = [g_leaf(), g_tree(), g_snowflake(), g_star(), g_heart(), g_flame(), g_cloud(), g_ladle(), g_scallop(), g_drop()]
    x = 10
    body = ""
    for g in shapes:
        g, w, h = norm(g)
        body += f'<g transform="translate({f(x)} 10)">{cut_piece(g)}</g>'
        x += w + 20
    tests["shapes"] = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {f(x)} 300" fill="none" stroke="{INK}">{body}</svg>'
    st = [stitch_running, stitch_back, stitch_stem, stitch_split, stitch_satin, stitch_french, stitch_daisy, stitch_blanket, stitch_whip]
    tests["stitches"] = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 320">' +
                         "".join(f'<g transform="translate({(i % 3) * 212} {(i // 3) * 100})">{stitch_box(fn())}</g>' for i, fn in enumerate(st))
                         .replace('viewBox="0 0 206 92"', 'viewBox="0 0 206 92" width="206" height="92"') + "</svg>")
    for k, s in tests.items():
        p = f"/tmp/pr-art3/{k}.svg"
        open(p, "w").write(s)
        d = fitz.open(p)
        d[0].get_pixmap(matrix=fitz.Matrix(1.0, 1.0)).save(f"/tmp/pr-art3/{k}.png")
        print(k, len(s))
