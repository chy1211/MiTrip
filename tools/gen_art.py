"""Generate the app's scenery / avatar / placeholder images from scratch (no third-party artwork).

All output is original, procedurally drawn with Pillow, so it can be published with the repo.
Usage: python tools/gen_art.py   -> writes into front/assets/images/
"""
import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

OUT = Path(__file__).resolve().parent.parent / "front" / "assets" / "images"
W, H = 1500, 1000
S = 2  # supersampling factor for smooth edges


def canvas(w=W, h=H):
    return Image.new("RGB", (w * S, h * S))


def finish(im, name, w=W, h=H):
    im = im.resize((w, h), Image.LANCZOS)
    im.save(OUT / name, optimize=True)
    print("wrote", name)


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def vgrad(im, stops, y0=0, y1=None):
    """Vertical gradient through color stops [(pos, rgb), ...] between y0..y1 (unscaled px)."""
    d = ImageDraw.Draw(im)
    y0, y1 = y0 * S, (y1 if y1 is not None else im.height // S) * S
    for y in range(y0, y1):
        t = (y - y0) / max(1, y1 - y0 - 1)
        for (p0, c0), (p1, c1) in zip(stops, stops[1:]):
            if p0 <= t <= p1:
                d.line([(0, y), (im.width, y)], fill=lerp(c0, c1, (t - p0) / (p1 - p0 or 1)))
                break


def P(pts):
    return [(x * S, y * S) for x, y in pts]


def poly(d, pts, fill):
    d.polygon(P(pts), fill=fill)


def circle(d, cx, cy, r, fill):
    d.ellipse([(cx - r) * S, (cy - r) * S, (cx + r) * S, (cy + r) * S], fill=fill)


def rect(d, x0, y0, x1, y1, fill, r=0):
    if r:
        d.rounded_rectangle([x0 * S, y0 * S, x1 * S, y1 * S], radius=r * S, fill=fill)
    else:
        d.rectangle([x0 * S, y0 * S, x1 * S, y1 * S], fill=fill)


def ridge(seed, base, amp, n=9, w=W):
    """Mountain-ridge polyline closed to the bottom."""
    rnd = random.Random(seed)
    xs = [i * w / n for i in range(n + 1)]
    pts = [(x, base - rnd.uniform(0.3, 1.0) * amp) for x in xs]
    return [(0, H)] + pts + [(w, H)]


def smooth_hill(base, amp, freq, phase, w=W, step=10):
    pts = [(x, base - amp * (0.5 + 0.5 * math.sin(x / w * math.pi * freq + phase))) for x in range(0, w + step, step)]
    return [(0, H)] + pts + [(w, H)]


def cloud(d, cx, cy, s, fill):
    for dx, dy, r in [(-1.1, 0.2, 0.55), (-0.45, -0.25, 0.75), (0.35, -0.1, 0.65), (1.05, 0.25, 0.5)]:
        circle(d, cx + dx * s, cy + dy * s, r * s, fill)
    rect(d, cx - 1.1 * s, cy + 0.05 * s, cx + 1.05 * s, cy + 0.75 * s, fill, r=int(0.3 * s))


def pine(d, x, base, h, fill):
    w = h * 0.42
    for i in range(3):
        top = base - h + i * h * 0.22
        bot = base - h * 0.25 + i * h * 0.12
        poly(d, [(x, top), (x - w * (0.55 + i * 0.22), bot), (x + w * (0.55 + i * 0.22), bot)], fill)
    rect(d, x - h * 0.04, base - h * 0.2, x + h * 0.04, base, (70, 50, 40))


def palm(d, x, base, h, lean=0.15, trunk=(120, 85, 55), leaf=(40, 140, 90)):
    top = (x + h * lean, base - h)
    for i in range(12):  # segmented trunk
        t0, t1 = i / 12, (i + 1) / 12
        xa, ya = x + h * lean * t0 ** 1.5, base - h * t0
        xb, yb = x + h * lean * t1 ** 1.5, base - h * t1
        wdt = 16 * (1 - t0 * 0.45)
        poly(d, [(xa - wdt / 2, ya), (xa + wdt / 2, ya), (xb + wdt / 2 * 0.95, yb), (xb - wdt / 2 * 0.95, yb)], trunk)
    for ang in [-160, -125, -90, -55, -20, 15, 200]:
        a = math.radians(ang)
        L = h * 0.55
        tip = (top[0] + math.cos(a) * L, top[1] + math.sin(a) * L * 0.55 + L * 0.35)
        mid = ((top[0] + tip[0]) / 2, (top[1] + tip[1]) / 2 - L * 0.18)
        nx, ny = -(tip[1] - top[1]), tip[0] - top[0]
        nl = math.hypot(nx, ny) or 1
        nx, ny = nx / nl * 18, ny / nl * 18
        poly(d, [top, (mid[0] + nx, mid[1] + ny), tip, (mid[0] - nx, mid[1] - ny)], leaf)
    circle(d, top[0], top[1], 12, (90, 60, 40))


def waves(d, y0, y1, color, gap=28, seed=1):
    rnd = random.Random(seed)
    y = y0 + 10
    while y < y1:
        for _ in range(int(3 + (y - y0) / 40)):
            x = rnd.uniform(0, W)
            ln = rnd.uniform(30, 90) * (0.6 + (y - y0) / (y1 - y0))
            rect(d, x, y, x + ln, y + 3 + (y - y0) / 120, color, r=2)
        y += gap * (0.7 + (y - y0) / (y1 - y0))


def glow(im, cx, cy, r, color, strength=0.55):
    mask = Image.new("L", im.size, 0)
    ImageDraw.Draw(mask).ellipse([(cx - r) * S, (cy - r) * S, (cx + r) * S, (cy + r) * S], fill=int(255 * strength))
    mask = mask.filter(ImageFilter.GaussianBlur(r * S * 0.5))
    return Image.composite(Image.new("RGB", im.size, color), im, mask)


# ---------------------------------------------------------------- scenes
def ocean():
    im = canvas(); vgrad(im, [(0, (110, 190, 240)), (0.55, (200, 235, 250)), (1, (200, 235, 250))], 0, 560)
    vgrad(im, [(0, (40, 150, 200)), (1, (10, 70, 130))], 560, H)
    d = ImageDraw.Draw(im)
    circle(d, 1160, 200, 80, (255, 245, 200))
    cloud(d, 330, 170, 70, (255, 255, 255)); cloud(d, 820, 110, 45, (240, 250, 255))
    waves(d, 570, H, (120, 200, 230), seed=3)
    # sailboat
    poly(d, [(560, 610), (720, 610), (690, 650), (590, 650)], (240, 240, 240))
    poly(d, [(640, 440), (640, 600), (560, 600)], (255, 255, 255))
    poly(d, [(650, 470), (650, 600), (720, 600)], (240, 120, 90))
    rect(d, 638, 430, 644, 612, (90, 70, 60))
    finish(im, "ocean.png")


def mountain():
    im = canvas(); vgrad(im, [(0, (150, 205, 245)), (1, (235, 245, 250))])
    d = ImageDraw.Draw(im)
    cloud(d, 1150, 150, 55, (255, 255, 255))
    layers = [(560, 380, (150, 170, 200), 5), (700, 360, (95, 125, 165), 7), (850, 280, (60, 90, 120), 11)]
    for base, amp, col, seed in layers:
        pts = ridge(seed, base, amp, n=6)
        poly(d, pts, col)
        if base == 700:  # snow caps
            for (x0, y0), (x1, y1), (x2, y2) in zip(pts[1:], pts[2:], pts[3:]):
                if y1 < y0 and y1 < y2 and y1 < 480:
                    k = 0.28
                    poly(d, [(x1, y1), (x1 + (x0 - x1) * k, y1 + (y0 - y1) * k), (x1 + (x2 - x1) * k, y1 + (y2 - y1) * k)], (245, 250, 255))
    for x in range(-20, W + 40, 55):
        pine(d, x, H - 10 + (x * 7 % 30), 110 + (x * 13 % 50), (35, 80, 70))
    finish(im, "mountain.png")


def city():
    im = canvas(); vgrad(im, [(0, (60, 60, 130)), (0.6, (240, 140, 120)), (1, (250, 200, 150))], 0, 820)
    vgrad(im, [(0, (50, 50, 90)), (1, (30, 30, 60))], 820, H)
    d = ImageDraw.Draw(im)
    circle(d, 380, 520, 90, (255, 215, 170))
    rnd = random.Random(7)
    for layer, (col, hmin, hmax) in enumerate([((120, 90, 140), 250, 450), ((70, 55, 100), 150, 380)]):
        x = -20
        while x < W:
            bw = rnd.uniform(60, 130); bh = rnd.uniform(hmin, hmax)
            rect(d, x, 820 - bh, x + bw, 820, col)
            if layer == 1:
                for wy in range(int(820 - bh + 20), 800, 34):
                    for wx in range(int(x + 12), int(x + bw - 18), 26):
                        if rnd.random() < 0.45:
                            rect(d, wx, wy, wx + 12, wy + 16, (255, 220, 140))
            x += bw + rnd.uniform(4, 14)
    # observation tower
    tx = 1020
    poly(d, [(tx - 60, 820), (tx - 12, 300), (tx + 12, 300), (tx + 60, 820)], (50, 40, 80))
    rect(d, tx - 45, 330, tx + 45, 380, (50, 40, 80), r=14)
    rect(d, tx - 35, 345, tx + 35, 360, (255, 220, 140))
    rect(d, tx - 3, 180, tx + 3, 300, (50, 40, 80))
    circle(d, tx, 176, 7, (255, 90, 90))
    waves(d, 830, H, (90, 80, 140), gap=30, seed=9)
    finish(im, "city.png")


def sunset():
    im = canvas(); vgrad(im, [(0, (70, 40, 110)), (0.45, (220, 90, 110)), (1, (255, 190, 110))], 0, 620)
    vgrad(im, [(0, (230, 130, 110)), (1, (60, 40, 90))], 620, H)
    im = glow(im, 750, 600, 260, (255, 200, 120))
    d = ImageDraw.Draw(im)
    circle(d, 750, 600, 150, (255, 225, 150))
    vgrad(im, [(0, (200, 100, 110)), (1, (55, 35, 80))], 620, H)  # sea covers lower half of the sun
    for i, y in enumerate(range(640, 900, 22)):  # sun reflection
        half = 140 - i * 11
        rect(d, 750 - half, y, 750 + half, y + 7, (255, 210, 150), r=3)
    poly(d, [(0, 640), (0, 470), (120, 430), (260, 500), (380, 560), (460, 640)], (50, 30, 70))
    poly(d, [(1500, 640), (1500, 420), (1380, 450), (1240, 540), (1120, 640)], (50, 30, 70))
    for bx, by in [(560, 280), (600, 300), (1000, 240)]:
        d.line(P([(bx - 16, by - 6), (bx, by), (bx + 16, by - 6)]), fill=(60, 30, 70), width=4 * S)
    finish(im, "sunset.png")


def hiking():
    im = canvas(); vgrad(im, [(0, (140, 200, 240)), (1, (225, 240, 245))])
    d = ImageDraw.Draw(im)
    cloud(d, 300, 160, 60, (255, 255, 255))
    poly(d, ridge(21, 600, 380, n=5), (120, 150, 185))
    poly(d, smooth_hill(760, 260, 1.3, -1.2), (110, 170, 110))
    poly(d, smooth_hill(900, 160, 2.1, 0.4), (80, 145, 90))
    # winding trail to a summit flag
    trail = [(820, H), (700, 930), (860, 860), (720, 790), (820, 720), (760, 660), (900, 560)]
    for (x0, y0), (x1, y1) in zip(trail, trail[1:]):
        d.line(P([(x0, y0), (x1, y1)]), fill=(225, 200, 150), width=int((10 + (y0 - 500) / 25) * S), joint="curve")
    rect(d, 898, 470, 904, 562, (80, 60, 50))
    poly(d, [(904, 472), (960, 490), (904, 510)], (240, 90, 80))
    # hiker
    hx, hy = 760, 780
    circle(d, hx, hy - 78, 14, (70, 60, 60))
    rect(d, hx - 13, hy - 62, hx + 13, hy - 18, (230, 110, 70), r=6)
    rect(d, hx - 30, hy - 66, hx - 10, hy - 22, (60, 110, 160), r=6)
    d.line(P([(hx - 6, hy - 20), (hx - 16, hy + 8)]), fill=(60, 60, 80), width=8 * S)
    d.line(P([(hx + 6, hy - 20), (hx + 14, hy + 8)]), fill=(60, 60, 80), width=8 * S)
    d.line(P([(hx + 12, hy - 50), (hx + 34, hy + 8)]), fill=(90, 70, 50), width=4 * S)
    for x in range(1080, W + 40, 60):
        pine(d, x, H - 20, 150, (40, 100, 70))
    finish(im, "hiking.png")


def beach():
    im = canvas(); vgrad(im, [(0, (100, 190, 240)), (1, (210, 240, 250))], 0, 520)
    vgrad(im, [(0, (60, 190, 210)), (1, (120, 220, 215))], 520, 700)
    d = ImageDraw.Draw(im)
    circle(d, 250, 170, 70, (255, 240, 180))
    cloud(d, 900, 150, 55, (255, 255, 255))
    waves(d, 525, 690, (190, 240, 240), gap=26, seed=4)
    poly(d, smooth_hill(700, 40, 1.5, 0.3), (245, 225, 170))
    rect(d, 0, 740, W, H, (245, 225, 170))
    d.line(P([(0, 700), (W, 690)]), fill=(255, 255, 255), width=6 * S)
    palm(d, 1250, 960, 520, lean=-0.25)
    palm(d, 1380, 990, 420, lean=-0.1)
    # umbrella + towel
    rect(d, 598, 640, 604, 880, (120, 90, 70))
    d.pieslice([470 * S, 590 * S, 730 * S, 760 * S], 180, 360, fill=(240, 90, 80))
    for i in range(0, 5, 2):
        d.pieslice([470 * S, 590 * S, 730 * S, 760 * S], 180 + i * 36, 180 + (i + 1) * 36, fill=(255, 245, 235))
    poly(d, [(520, 900), (700, 880), (720, 940), (540, 960)], (80, 170, 220))
    circle(d, 400, 900, 26, (255, 200, 80))
    finish(im, "beach.png")


def forest():
    im = canvas(); vgrad(im, [(0, (190, 225, 215)), (1, (240, 245, 235))])
    d = ImageDraw.Draw(im)
    circle(d, 1100, 220, 90, (255, 250, 225))
    rnd = random.Random(5)
    for base, hmin, hmax, col, gap in [(580, 180, 260, (150, 190, 170), 45), (720, 230, 330, (90, 150, 120), 60),
                                       (860, 300, 420, (50, 110, 85), 80), (990, 380, 520, (25, 70, 55), 110)]:
        rect(d, 0, base - 5, W, H, col)
        x = -30
        while x < W + 60:
            pine(d, x, base, rnd.uniform(hmin, hmax), col)
            x += gap * rnd.uniform(0.7, 1.2)
    finish(im, "forest.png")


def hotel():
    im = canvas(); vgrad(im, [(0, (120, 180, 235)), (1, (220, 238, 250))], 0, 860)
    d = ImageDraw.Draw(im)
    cloud(d, 280, 180, 60, (255, 255, 255)); cloud(d, 1250, 130, 45, (255, 255, 255))
    rect(d, 0, 860, W, H, (150, 190, 120))
    rect(d, 520, 230, 980, 860, (245, 235, 220))
    rect(d, 500, 210, 1000, 250, (190, 90, 70), r=8)
    for wy in range(290, 720, 70):
        for wx in range(560, 940, 70):
            rect(d, wx, wy, wx + 40, wy + 44, (110, 170, 215), r=4)
            rect(d, wx + 18, wy, wx + 22, wy + 44, (245, 235, 220))
    rect(d, 690, 740, 810, 860, (120, 80, 60), r=6)
    poly(d, [(660, 740), (840, 740), (870, 700), (630, 700)], (190, 90, 70))
    rect(d, 280, 520, 500, 860, (230, 215, 195)); rect(d, 1000, 470, 1220, 860, (230, 215, 195))
    for bx0, by0, bx1 in [(280, 520, 500), (1000, 470, 1220)]:
        for wy in range(by0 + 40, 820, 70):
            for wx in range(bx0 + 30, bx1 - 40, 65):
                rect(d, wx, wy, wx + 36, wy + 40, (110, 170, 215), r=4)
    palm(d, 180, 900, 380, lean=0.18); palm(d, 1330, 900, 400, lean=-0.18)
    finish(im, "hotel.png")


def island():
    im = canvas(); vgrad(im, [(0, (250, 180, 140)), (0.5, (250, 215, 170)), (1, (180, 225, 235))], 0, 560)
    vgrad(im, [(0, (80, 180, 200)), (1, (30, 100, 150))], 560, H)
    d = ImageDraw.Draw(im)
    circle(d, 1150, 330, 75, (255, 240, 200))
    cloud(d, 380, 180, 55, (255, 245, 240))
    waves(d, 570, H, (150, 215, 225), seed=11)
    d.ellipse([430 * S, 520 * S, 1070 * S, 700 * S], fill=(90, 170, 190))  # shallow ring
    d.ellipse([500 * S, 540 * S, 1000 * S, 650 * S], fill=(245, 225, 170))
    d.chord([560 * S, 460 * S, 940 * S, 640 * S], 180, 360, fill=(80, 160, 90))
    palm(d, 700, 590, 330, lean=0.2); palm(d, 820, 600, 260, lean=-0.25)
    poly(d, [(1180, 760), (1300, 760), (1280, 790), (1200, 790)], (240, 240, 240))
    poly(d, [(1238, 650), (1238, 752), (1190, 752)], (255, 255, 255))
    finish(im, "island.png")


# ---------------------------------------------------------------- avatars / placeholder
def person_avatar(name, bg, fg, ring):
    n = 512
    im = Image.new("RGBA", (n * S, n * S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.ellipse([0, 0, n * S, n * S], fill=bg)
    mask = Image.new("L", im.size, 0); ImageDraw.Draw(mask).ellipse([0, 0, n * S, n * S], fill=255)
    body = Image.new("RGBA", im.size, (0, 0, 0, 0)); bd = ImageDraw.Draw(body)
    bd.ellipse([176 * S, 110 * S, 336 * S, 270 * S], fill=fg)
    bd.ellipse([96 * S, 300 * S, 416 * S, 620 * S], fill=fg)
    if ring:
        bd.ellipse([190 * S, 300 * S, 322 * S, 360 * S], fill=ring)  # collar
    im.paste(body, (0, 0), Image.composite(body, Image.new("RGBA", im.size), mask).split()[3])
    im.resize((n, n), Image.LANCZOS).save(OUT / name, optimize=True)
    print("wrote", name)


def placeholder():
    n = 600
    im = Image.new("RGB", (n * S, n * S), (236, 239, 243)); d = ImageDraw.Draw(im)
    k = lambda v: int(v * S)
    d.rounded_rectangle([k(170), k(190), k(430), k(410)], radius=k(24), outline=(170, 178, 190), width=k(14))
    d.ellipse([k(340), k(225), k(390), k(275)], fill=(170, 178, 190))
    d.polygon([(k(185), k(395)), (k(270), k(290)), (k(330), k(360)), (k(360), k(330)), (k(415), k(395))], fill=(170, 178, 190))
    im.resize((n, n), Image.LANCZOS).save(OUT / "placeholder.png", optimize=True)
    print("wrote placeholder.png")


if __name__ == "__main__":
    for f in (ocean, mountain, city, sunset, hiking, beach, forest, hotel, island):
        f()
    person_avatar("avatar.png", (225, 228, 235), (160, 168, 182), None)            # logged out
    person_avatar("user_avatar.png", (46, 170, 120), (215, 242, 228), None)  # logged in
    placeholder()
