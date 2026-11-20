"""Hand-drawn vector line art for the wave 2 printables (coloring pages, invitations, signs).
Everything is plain SVG written by hand or laid out by a few lines of geometry. No raster images.
Run `python3 art.py` to write test PNGs of the coloring pages to /tmp/pr-art/."""
import math
import random

INK = "#1b1512"
DASH = ' stroke-dasharray="2 16"'


def svg(w, h, body, sw=3.0, extra=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" fill="#fff" stroke="{INK}" '
            f'stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"{extra}>{body}</svg>')


def ln(d, extra=""):
    """Open stroke, never filled."""
    return f'<path d="{d}" fill="none"{extra}/>'


def sh(d, extra=""):
    """Closed white shape that hides what is behind it."""
    return f'<path d="{d}"{extra}/>'


def f(v):
    return f"{v:.1f}".rstrip("0").rstrip(".")


def leaf(x, y, ang, L=62, W=19, veins=True):
    """Birch-like leaf whose stem end sits at (x, y); ang in degrees, 0 = pointing right."""
    d = (f"M0 0C{f(L * .18)} {f(-W)} {f(L * .62)} {f(-W * .95)} {f(L)} 0"
         f"C{f(L * .62)} {f(W * .95)} {f(L * .18)} {f(W)} 0 0Z")
    v = f'<path d="M0 0L{f(L * .8)} 0" fill="none"/>'
    if veins:
        v += (f'<path d="M{f(L * .28)} 0L{f(L * .45)} {f(-W * .55)}M{f(L * .28)} 0L{f(L * .45)} {f(W * .55)}'
              f'M{f(L * .5)} 0L{f(L * .66)} {f(-W * .42)}M{f(L * .5)} 0L{f(L * .66)} {f(W * .42)}" fill="none" stroke-width="1.6"/>')
    return f'<g transform="translate({f(x)} {f(y)}) rotate({f(ang)})"><path d="{d}"/>{v}</g>'


def drop(x, y, s=1.0, ang=0):
    d = "M0 -26C10 -10 17 0 17 9A17 17 0 0 1 -17 9C-17 0 -10 -10 0 -26Z"
    return f'<path d="{d}" transform="translate({f(x)} {f(y)}) rotate({f(ang)}) scale({s})"/>'


def flame(x, y, s=1.0, ang=0, inner=True):
    d = "M0 -50C4 -28 26 -18 26 8A26 26 0 0 1 -26 8C-26 -4 -19 -12 -13 -19C-11 -9 -7 -5 -3 -3C-7 -22 -5 -38 0 -50Z"
    i = '<path d="M0 -8C6 0 11 6 11 14A11 11 0 0 1 -11 14C-11 6 -6 0 0 -8Z"/>' if inner else ""
    return f'<g transform="translate({f(x)} {f(y)}) rotate({f(ang)}) scale({s})"><path d="{d}"/>{i}</g>'


def steam(x, y, h=150, amp=16, n=3):
    seg = h / (2 * n)
    d = f"M{f(x)} {f(y)}"
    for k in range(2 * n):
        s = amp if k % 2 == 0 else -amp
        d += f"q{f(s)} {f(-seg / 2)} 0 {f(-seg)}"
    return ln(d)


def bell_hat(x, y, s=1.0, pattern=True, uid="h"):
    """Classic bell-shaped felt hat with a rolled edge and a hanging loop. Box about 350 x 410 units."""
    body = "M25 350C50 280 40 60 175 60C310 60 300 280 325 350Z"
    pat = ""
    if pattern:
        zig = "M20 178" + "".join(f"l15 -24l15 24" for _ in range(11))
        tri = "".join(f"M{40 + 34 * i} 320l17 -30l17 30" for i in range(9))
        dots = "".join(f'<circle cx="{66 + 31 * i}" cy="215" r="9"/>' for i in range(8))
        dia = "".join(f"M{52 + 34 * i} 265l17 -18l17 18l-17 18Z" for i in range(8))
        pat = (f'<g clip-path="url(#{uid})">{ln("M0 150H350M0 185H350M0 240H350M0 290H350")}{ln(zig)}{dots}'
               f'{sh(dia)}{ln(tri)}{ln("M175 60C150 85 142 118 140 150M175 60C200 85 208 118 210 150")}</g>')
    return (f'<g transform="translate({f(x)} {f(y)}) scale({s})" stroke-width="{f(3 / s)}"><defs><clipPath id="{uid}"><path d="{body}"/></clipPath></defs>'
            f'{sh("M175 60C140 44 136 4 163 1C190 -2 200 30 175 60Z")}{sh(body)}{pat}{ln(body)}'
            f'<rect x="0" y="350" width="350" height="56" rx="28"/>{ln("M40 378H310", DASH)}</g>')


def bucket_hat(x, y, s=1.0, pattern=True):
    """Bucket hat with a brim. Box about 540 x 240 units."""
    brim = "M5 185C45 125 145 100 270 100C395 100 495 125 535 185C465 222 365 238 270 238C175 238 75 222 5 185Z"
    crown = "M135 112C128 0 185 -30 270 -30C355 -30 412 0 405 112C360 128 180 128 135 112Z"
    p = ""
    if pattern:
        p = (ln("M139 78C185 95 355 95 401 78M137 100C182 116 358 116 403 100")
             + "".join(f'<circle cx="{168 + 34 * i}" cy="{f(100 + 6 * math.sin(math.pi * i / 6))}" r="6.5"/>' for i in range(7))
             + ln("M40 186C95 150 180 136 270 136C360 136 445 150 500 186", ' stroke-dasharray="14 12"')
             + ln("M70 196C125 170 195 160 270 160C345 160 415 170 470 196", ' stroke-dasharray="14 12"')
             + ln("M270 -30C260 5 257 45 257 86"))
    return f'<g transform="translate({f(x)} {f(y)}) scale({s})" stroke-width="{f(3 / s)}">{sh(brim)}{sh(crown)}{p}</g>'


def bucket(x, y, s=1.0, ladle=True):
    """Wooden bucket, about 300 wide and 330 tall, with an optional ladle leaning in it."""
    cx, top, bot, rt, rb, et, eb = 150, 95, 310, 150, 118, 34, 26
    out = []
    if ladle:
        out.append(sh("M178 96L322 -70L342 -53L205 108Z"))
        out.append('<circle cx="322" cy="-52" r="5" fill="none"/>')
    side = f"M{cx - rt} {top}L{cx - rb} {bot}A{rb} {eb} 0 0 0 {cx + rb} {bot}L{cx + rt} {top}"
    out.append(sh(side + f"A{rt} {et} 0 0 1 {cx - rt} {top}Z"))
    for k in range(1, 8):
        a = math.pi * k / 8
        out.append(ln(f"M{f(cx + rt * math.cos(a))} {f(top + et * math.sin(a))}L{f(cx + rb * math.cos(a))} {f(bot + eb * math.sin(a))}"))
    for fr in (.2, .7):
        yy, rr, ee = top + fr * (bot - top), rt - fr * (rt - rb), et - fr * (et - eb)
        band = (f"M{f(cx - rr)} {f(yy)}A{f(rr)} {f(ee)} 0 0 0 {f(cx + rr)} {f(yy)}L{f(cx + rr - 3)} {f(yy + 26)}"
                f"A{f(rr - 3)} {f(ee)} 0 0 1 {f(cx - rr + 3)} {f(yy + 26)}Z")
        out.append(sh(band))
    out.append(f'<ellipse cx="{cx}" cy="{top}" rx="{rt}" ry="{et}"/>')
    out.append(f'<ellipse cx="{cx}" cy="{top + 4}" rx="{rt - 16}" ry="{et - 9}"/>')
    out.append(ln(f"M{cx - 95} {top + 2}q16 -9 32 0t32 0M{cx - 20} {top + 12}q16 -9 32 0t32 0"))
    if ladle:
        out.append(sh("M178 96L205 108L196 119L170 104Z", ' stroke="none"'))
    out.append(ln(f"M{cx - rt + 6} {top - 4}C{cx - rt - 20} {top - 190} {cx + rt + 20} {top - 190} {cx + rt - 6} {top - 4}"))
    out.append(ln(f"M{cx - rt + 28} {top - 12}C{cx - rt + 10} {top - 160} {cx + rt - 10} {top - 160} {cx + rt - 28} {top - 12}"))
    return f'<g transform="translate({f(x)} {f(y)}) scale({s})" stroke-width="{f(3 / s)}">{"".join(out)}</g>'


def stones(x0, x1, ybase, rows, seed=3, r=26):
    """A heap of sauna stones between x0 and x1 sitting on ybase."""
    rnd = random.Random(seed)
    out = []
    layers = []
    width = x1 - x0
    for row in range(rows):
        n = max(2, int(width / (r * 1.9)) - row)
        span = width - row * r * 1.9
        xs = x0 + (width - span) / 2
        layer = []
        for i in range(n):
            cx = xs + span * (i + .5) / n + rnd.uniform(-4, 4)
            cy = ybase - r * .72 - row * r * 1.25 + rnd.uniform(-3, 3)
            layer.append((cx, cy, r * rnd.uniform(.95, 1.18) * span / n / (r * 1.9) * .98 + 3, r * rnd.uniform(.72, .86), rnd.uniform(-14, 14)))
        layers.append(layer)
    for layer in reversed(layers):
        for cx, cy, rx, ry, rot in layer:
            out.append(f'<ellipse cx="{f(cx)}" cy="{f(cy)}" rx="{f(rx)}" ry="{f(ry)}" transform="rotate({f(rot)} {f(cx)} {f(cy)})"/>')
    return "".join(out)


def pine(x, base, h, w):
    out = [f'<rect x="{f(x - w * .07)}" y="{f(base - h * .16)}" width="{f(w * .14)}" height="{f(h * .16)}"/>']
    tiers = 4
    for t in range(tiers):
        ty = base - h * .14 - (h * .86) * t / tiers * .82
        tw = w * (1 - t * .2) / 2
        th = h * .86 / tiers * 1.5
        out.append(sh(f"M{f(x - tw)} {f(ty)}L{f(x)} {f(ty - th)}L{f(x + tw)} {f(ty)}Q{f(x)} {f(ty + th * .16)} {f(x - tw)} {f(ty)}Z"))
    return "".join(out)


def cloud(x, y, s=1.0):
    return sh("M20 60A26 26 0 0 1 36 12A34 34 0 0 1 98 6A28 28 0 0 1 142 28A22 22 0 0 1 146 60Z",
              f' transform="translate({f(x)} {f(y)}) scale({s})"')


def cabin(x, y, s=1.0, smoke=True):
    """Small log sauna cabin, about 380 wide and 360 tall (roof peak at y = 0 without smoke)."""
    o = []
    if smoke:
        o.append(ln("M287 8c-18 -16 14 -30 -4 -48s16 -30 2 -46"))
        o.append(ln("M303 2c-14 -14 12 -24 0 -38"))
    o.append('<rect x="270" y="20" width="46" height="80"/>')
    o.append(ln("M262 20H324"))
    o.append('<rect x="40" y="140" width="300" height="220"/>')
    o.append(ln("".join(f"M40 {140 + 36.7 * i:.1f}H340" for i in range(1, 6))))
    o.append(sh("M0 150L190 0L380 150L352 168L190 40L28 168Z"))
    o.append(sh("M190 40L62 141H318Z"))
    o.append('<circle cx="190" cy="100" r="17"/>')
    o.append('<rect x="150" y="225" width="80" height="135" rx="3"/><rect x="168" y="245" width="44" height="40" rx="3"/>')
    o.append(ln("M219 300v14"))
    o.append('<rect x="262" y="218" width="58" height="58" rx="3"/>' + ln("M291 218v58M262 247h58"))
    o.append('<rect x="60" y="218" width="58" height="58" rx="3"/>' + ln("M89 218v58M60 247h58"))
    return f'<g transform="translate({f(x)} {f(y)}) scale({s})" stroke-width="{f(3 / s)}">{"".join(o)}</g>'


# ---------------------------------------------------------------- coloring pages (750 x 900 units)

def page_stove():
    o = []
    o.append('<rect x="30" y="30" width="690" height="640"/>')
    o.append(ln("".join(f"M{30 + 86.25 * i:.1f} 30V670" for i in range(1, 8))))
    o.append('<rect x="30" y="670" width="690" height="200"/>')
    o.append(ln("M30 736H720M30 803H720M210 670V736M520 670V736M90 736V803M390 736V803M640 736V803M250 803V870M560 803V870"))
    # thermometer dial
    o.append('<circle cx="600" cy="170" r="58"/><circle cx="600" cy="170" r="45"/>')
    o.append(ln("".join(f"M{600 + 45 * math.cos(math.radians(a)):.1f} {170 + 45 * math.sin(math.radians(a)):.1f}"
                        f"L{600 + 34 * math.cos(math.radians(a)):.1f} {170 + 34 * math.sin(math.radians(a)):.1f}"
                        for a in range(150, 391, 30))))
    o.append(ln("M600 170L626 142") + '<circle cx="600" cy="170" r="6"/>')
    # hat on a peg
    o.append('<rect x="60" y="92" width="150" height="16" rx="8"/>')
    o.append(ln("M135 108v16"))
    o.append(bell_hat(69, 112, .38, pattern=False, uid="hs"))
    # steam
    o.append(steam(275, 215, 150) + steam(335, 200, 150) + steam(395, 215, 150))
    # stove
    o.append('<rect x="212" y="756" width="34" height="34" rx="4"/><rect x="424" y="756" width="34" height="34" rx="4"/>')
    o.append(stones(206, 464, 372, 3, seed=5, r=27))
    o.append('<rect x="200" y="390" width="270" height="370" rx="18"/>')
    o.append('<rect x="184" y="362" width="302" height="34" rx="10"/>')
    o.append('<rect x="246" y="450" width="178" height="190" rx="14"/><rect x="270" y="474" width="130" height="118" rx="10"/>')
    o.append(flame(305, 566, .62, -6) + flame(365, 566, .62, 6) + flame(335, 560, .9))
    o.append('<rect x="318" y="606" width="34" height="14" rx="7"/>')
    o.append('<rect x="262" y="676" width="146" height="44" rx="8"/>' + ln("M284 698H386"))
    o.append(ln("M222 420H448", ' stroke-dasharray="2 18"'))
    # bucket on the floor
    o.append(bucket(520, 560, .58))
    return svg(750, 900, "".join(o), 3.2)


def page_bucket():
    o = []
    o.append(ln("M30 800H720"))
    o.append(ln("M60 838H330M420 838H700M150 872H560"))
    o.append(bucket(115, 290, 1.45))
    for x, y, s, a in [(610, 470, 1.25, 0), (662, 560, 1.0, 0), (590, 610, .8, 0), (642, 680, 1.1, 0), (90, 200, .9, 0), (70, 96, .7, 0)]:
        o.append(drop(x, y, s, a))
    o.append(leaf(84, 760, -28, 100, 31) + leaf(98, 770, 22, 86, 27) + leaf(640, 770, 200, 96, 30) + leaf(655, 758, 150, 80, 25))
    o.append(steam(200, 250, 170, 18) + steam(265, 228, 190, 18) + steam(330, 250, 170, 18))
    return svg(750, 900, "".join(o), 3.2)


def page_whisk():
    rnd = random.Random(11)
    nx, ny = 375, 640
    branches, leaves = [], []
    n = 11
    for i in range(n):
        th = -58 + 116 * i / (n - 1)
        L = 505 - 110 * abs(th) / 58 + rnd.uniform(-18, 18)
        a = math.radians(th - 90)
        bend = math.radians(th * .22)
        pts = []
        for k in range(0, 21):
            t = k / 20
            ang = a + bend * t
            pts.append((nx + L * t * math.cos(ang), ny + L * t * math.sin(ang), math.degrees(ang)))
        branches.append("M" + "L".join(f"{f(p[0])} {f(p[1])}" for p in pts))
        step = 3
        for k in range(5, 20, step):
            x, y, deg = pts[k]
            side = 1 if (k // step + i) % 2 == 0 else -1
            size = rnd.uniform(.9, 1.12)
            leaves.append((y, leaf(x, y, deg + side * rnd.uniform(38, 55), 64 * size, 20 * size)))
            if k > 8:
                leaves.append((y, leaf(x, y, deg - side * rnd.uniform(40, 58), 56 * size, 18 * size)))
        x, y, deg = pts[20]
        leaves.append((y - 5, leaf(x, y, deg + rnd.uniform(-8, 8), 70, 22)))
    leaves.sort(key=lambda t: t[0])
    o = [ln("".join(branches), ' stroke-width="4"')]
    o += [l for _, l in leaves]
    # handle
    o.append(sh("M348 628L402 628L396 850A21 9 0 0 1 354 850Z"))
    o.append(ln("M362 690V842M375 690V846M388 690V842"))
    o.append('<rect x="338" y="622" width="74" height="66" rx="10"/>')
    o.append(ln("M340 640L410 628M339 656L411 643M339 672L411 659M344 686L411 675"))
    o.append('<rect x="344" y="770" width="62" height="34" rx="8"/>' + ln("M346 784L404 776M346 798L404 790"))
    g = f'<g transform="translate(27 48) scale(.9) rotate(24 375 520) translate(-28 6)" stroke-width="3.2">{"".join(o)}</g>'
    extra = drop(660, 690, 1.1) + drop(610, 770, .8) + drop(690, 800, .7) + leaf(70, 820, -20, 84, 26) + leaf(140, 850, 10, 70, 22)
    return svg(750, 900, g + extra, 2.6)


def page_hats():
    o = []
    o.append('<rect x="60" y="34" width="630" height="20" rx="10"/>')
    o.append(ln("M240 54v22M560 54v22"))
    o.append(bell_hat(85, 74, .9, uid="h1"))
    o.append(bell_hat(432, 74, .72, pattern=False, uid="h2"))
    o.append(bucket_hat(105, 590, 1.0))
    # snowflakes and steam around
    for cx, cy, r in [(560, 470, 46), (650, 395, 26), (72, 520, 30)]:
        d = ""
        for k in range(6):
            a = math.radians(60 * k)
            ca, sa = math.cos(a), math.sin(a)
            d += f"M{cx} {cy}L{f(cx + r * ca)} {f(cy + r * sa)}"
            for side in (-1, 1):
                b = a + side * math.radians(45)
                mx, my = cx + r * .62 * ca, cy + r * .62 * sa
                d += f"M{f(mx)} {f(my)}L{f(mx + r * .3 * math.cos(b))} {f(my + r * .3 * math.sin(b))}"
        o.append(ln(d))
    o.append(steam(650, 600, 120, 14) + steam(690, 620, 120, 14))
    o.append(ln("M40 842H710"))
    return svg(750, 900, "".join(o), 3.0)


def page_cabin():
    o = []
    o.append('<rect x="20" y="20" width="710" height="860" rx="6"/>')
    # sun and clouds
    o.append('<circle cx="610" cy="130" r="52"/>')
    o.append(ln("".join(f"M{610 + 66 * math.cos(math.radians(a)):.1f} {130 + 66 * math.sin(math.radians(a)):.1f}"
                        f"L{610 + 88 * math.cos(math.radians(a)):.1f} {130 + 88 * math.sin(math.radians(a)):.1f}" for a in range(0, 360, 30))))
    o.append(cloud(70, 80, 1.2) + cloud(330, 50, .9))
    # hills
    o.append(sh("M20 470C120 330 230 300 330 380C420 290 560 280 730 440V612H20Z"))
    o.append(ln("M330 380C310 400 290 425 280 450"))
    # trees
    o.append(pine(92, 572, 250, 120) + pine(660, 580, 300, 140) + pine(556, 566, 190, 96))
    # cabin
    o.append(cabin(150, 250, 1.0))
    o.append(bucket(404, 566, .22, ladle=False))
    # shore and lake
    o.append('<path d="M20 612H730V880H20Z"/>')
    o.append(sh("M20 610C200 600 420 602 730 612V664C520 650 300 676 20 660Z"))
    o.append(ln("M60 632h40M170 640h60M560 636h50M640 644h40"))
    # dock
    o.append('<rect x="424" y="700" width="16" height="96"/><rect x="604" y="700" width="16" height="96"/>')
    o.append(sh("M400 660H644V702H400Z") + ln("M448.8 660V702M497.6 660V702M546.4 660V702M595.2 660V702"))
    for yy, xs in [(748, [190, 300, 470, 650]), (800, [70, 250, 520]), (846, [180, 330, 460])]:
        o.append(ln("".join(f"M{x} {yy}q18 -12 36 0t36 0" for x in xs)))
    o.append(ln("M412 800q20 -12 40 0M592 800q20 -12 40 0"))
    # reeds
    for x, top in ((64, 716), (98, 742), (132, 722)):
        o.append(ln(f"M{x} 880C{x + 4} 830 {x - 4} 800 {x + 2} {top + 40}"))
        o.append(f'<rect x="{x - 5}" y="{top}" width="14" height="46" rx="7"/>')
    o.append('<ellipse cx="655" cy="852" rx="44" ry="18"/><ellipse cx="596" cy="862" rx="22" ry="11"/>')
    return svg(750, 900, "".join(o), 3.0)


def page_mandala():
    cx, cy = 375, 450
    o = []

    def ring(n, fn, off=0):
        return "".join(f'<g transform="rotate({f(off + 360 * k / n)} {cx} {cy})">{fn()}</g>' for k in range(n))

    o.append(f'<circle cx="{cx}" cy="{cy}" r="352"/>')
    o.append(ring(24, lambda: sh(f"M{cx - 44} {cy - 338}A46 46 0 0 1 {cx + 44} {cy - 338}")))
    o.append(f'<circle cx="{cx}" cy="{cy}" r="338"/>')
    o.append(ring(12, lambda: drop(cx, cy - 280, 1.9) + drop(cx, cy - 268, .95)))
    o.append(ring(12, lambda: f'<circle cx="{cx}" cy="{cy - 262}" r="15"/><circle cx="{cx}" cy="{cy - 300}" r="8"/>', 15))
    o.append(f'<circle cx="{cx}" cy="{cy}" r="236"/><circle cx="{cx}" cy="{cy}" r="224"/>')
    o.append(ring(16, lambda: leaf(cx, cy - 132, -90, 90, 26)))
    o.append(ring(16, lambda: f'<circle cx="{cx}" cy="{cy - 196}" r="9"/>', 11.25))
    o.append(f'<circle cx="{cx}" cy="{cy}" r="130"/><circle cx="{cx}" cy="{cy}" r="120"/>')
    o.append(ring(8, lambda: drop(cx, cy - 76, 1.25)))
    o.append(ring(8, lambda: f'<circle cx="{cx}" cy="{cy - 100}" r="7"/>', 22.5))
    o.append(f'<circle cx="{cx}" cy="{cy}" r="44"/>')
    star = "M" + "L".join(f"{f(cx + (40 if k % 2 == 0 else 18) * math.sin(math.radians(22.5 * k)))} "
                          f"{f(cy - (40 if k % 2 == 0 else 18) * math.cos(math.radians(22.5 * k)))}" for k in range(16)) + "Z"
    o.append(sh(star) + f'<circle cx="{cx}" cy="{cy}" r="8"/>')
    return svg(750, 900, "".join(o), 2.4)


PAGES = [
    ("Sauna stove", "The stones on top hold the heat. Color the fire warm.", page_stove),
    ("Bucket and ladle", "One ladle of water on the hot stones makes a soft burst of steam.", page_bucket),
    ("Sauna hats", "Wool felt hats keep your head comfortable in the heat. Give them your own colors.", page_hats),
    ("Sauna by the lake", "Heat, then a swim, then a rest on the dock.", page_cabin),
    ("Leafy whisk", "A bundle of birch twigs, called a vihta or vasta in Finland and a venik in the banya.", page_whisk),
    ("Fire, water, leaf", "A slow one for grown-ups: flames, stones, leaves and water drops.", page_mandala),
]

if __name__ == "__main__":
    import os
    import fitz
    os.makedirs("/tmp/pr-art", exist_ok=True)
    for i, (t, _, fn) in enumerate(PAGES, 1):
        s = fn()
        p = f"/tmp/pr-art/{i}.svg"
        open(p, "w").write(s)
        d = fitz.open(p)
        d[0].get_pixmap(matrix=fitz.Matrix(1.0, 1.0)).save(f"/tmp/pr-art/{i}.png")
        print(i, t, len(s))
