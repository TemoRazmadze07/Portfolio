#!/usr/bin/env python3
"""Generate the Open Graph / social share cards (1200x630) into assets/.

Writes the site card (og-image.png) plus one card per case study
(og-tbc.png, og-golance.png, og-novocure.png, og-rogers.png), so a shared
case-study link previews with its own title and metrics instead of the
generic site card.

Each case card reuses that case's .pcard tint from styles.css — same base
gradient and glow — so a link preview reads as the same object as the card
it came from. Uses Avenir Next as the closest system stand-in for the
site's Plus Jakarta Sans.
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1200, 630
FONT = "/System/Library/Fonts/Avenir Next.ttc"
HEAVY, BOLD, DEMI, MEDIUM = 8, 0, 2, 5
f = lambda idx, sz: ImageFont.truetype(FONT, sz, index=idx)
PAD = 84

# Avenir Next has no U+2192, so "55→64" drawn with it yields a .notdef box.
# Helvetica/Helvetica Neue don't have it either — Arial Bold does, and is a
# static bold close enough in weight to sit beside Avenir Heavy.
FALLBACK = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
MISSING = "→"
PUA = ""  # private use: renders as .notdef, i.e. what a tofu box looks like


def _renders(font, ch):
    """True if `font` has a real glyph for `ch` (not .notdef, not blank).

    Compared against a private-use codepoint rather than an empty string —
    an empty string draws nothing, so a .notdef box would read as a hit.
    """
    def px(c):
        im = Image.new("L", (110, 110), 0)
        ImageDraw.Draw(im).text((5, 5), c, font=font, fill=255)
        return im.tobytes()
    got = px(ch)
    return got != px(PUA) and got != px(" ")


def _fallback(size):
    fb = ImageFont.truetype(FALLBACK, size)
    for ch in MISSING:
        if not _renders(fb, ch):
            raise SystemExit(
                f"{FALLBACK} has no glyph for {ch!r} (U+{ord(ch):04X}) — it would "
                "render as a tofu box. Point FALLBACK at a font that covers it."
            )
    return fb


def draw_mixed(draw, xy, text, font, fill):
    """draw.text(), but characters Avenir lacks are drawn from the fallback."""
    if not any(ch in MISSING for ch in text):
        draw.text(xy, text, font=font, fill=fill)
        return draw.textlength(text, font=font)
    fb = _fallback(round(font.size * 0.92))
    x, y = xy
    for ch in text:
        cf = fb if ch in MISSING else font
        # nudge the fallback glyph onto the Avenir baseline
        draw.text((x, y + (font.size * 0.06 if ch in MISSING else 0)), ch, font=cf, fill=fill)
        x += draw.textlength(ch, font=cf)
    return x - xy[0]


def gradient(tl, tr, bl, br):
    """Bilinear diagonal gradient from four corner colours."""
    corners = Image.new("RGB", (2, 2))
    corners.putpixel((0, 0), tl)
    corners.putpixel((1, 0), tr)
    corners.putpixel((0, 1), bl)
    corners.putpixel((1, 1), br)
    return corners.resize((W, H), Image.BICUBIC)


def radial(cx, cy, r, peak):
    """A soft circular light mask centered at (cx,cy)."""
    m = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(m)
    steps = 60
    for i in range(steps, 0, -1):
        rr = r * i / steps
        a = int(peak * (1 - i / steps) ** 1.4)
        d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=a)
    return m.filter(ImageFilter.GaussianBlur(30))


def glow(img, colour, cx, cy, r, peak):
    return Image.composite(Image.new("RGB", (W, H), colour), img, radial(cx, cy, r, peak))


def dotgrid(img, colour=(150, 178, 255), step=26, alpha=42):
    dots = Image.new("L", (W, H), 0)
    dd = ImageDraw.Draw(dots)
    for y in range(0, H, step):
        for x in range(0, W, step):
            dd.ellipse([x - 1, y - 1, x + 1, y + 1], fill=alpha)
    return Image.composite(Image.new("RGB", (W, H), colour), img, dots)


def tracked(draw, x, y, text, font, fill, track):
    """Letter-spaced text (PIL has no tracking)."""
    for ch in text:
        draw.text((x, y), ch, font=font, fill=fill)
        x += draw.textlength(ch, font=font) + track
    return x


def wrap(draw, text, font, maxw):
    lines, cur = [], ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=font) <= maxw or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


LINE_RATIO = 1.2


def balance(draw, text, font, maxw):
    """Wrap at the narrowest width giving the same line count as `maxw`.

    Plain greedy wrapping leaves the leftovers alone on the last line
    ("... Portal” / 2021"). Squeezing the measure until just before the
    line count would grow pulls that orphan back up.
    """
    lines = wrap(draw, text, font, maxw)
    best = lines
    w = maxw
    while w > maxw * 0.6:
        w -= maxw * 0.02
        trial = wrap(draw, text, font, w)
        if len(trial) != len(lines):
            break
        best = trial
    return best


def fit(draw, text, maxw, maxh, max_lines, hi, lo):
    """Largest size at which `text` wraps into a maxw x maxh box.

    Bounding on height as well as line count is what keeps a 3-line title
    off the metric tiles below it — line count alone let tall type overrun.
    """
    for size in range(hi, lo - 1, -1):
        font = f(HEAVY, size)
        lines = wrap(draw, text, font, maxw)
        if len(lines) <= max_lines and len(lines) * size * LINE_RATIO <= maxh:
            return font, balance(draw, text, font, maxw)
    font = f(HEAVY, lo)
    return font, wrap(draw, text, font, maxw)[:max_lines]


def footer(draw, subtitle):
    """Shared divider + name block at the bottom of every card."""
    dy = 468
    draw.rectangle([PAD, dy, W - PAD, dy + 1], fill=(70, 84, 130))
    by = 508
    draw.rounded_rectangle([PAD, by + 4, PAD + 5, by + 52], radius=2, fill=(143, 179, 255))
    nx = PAD + 22
    draw.text((nx, by), "Temo Razmadze", font=f(BOLD, 33), fill=(255, 255, 255))
    draw.text((nx, by + 46), subtitle, font=f(MEDIUM, 20), fill=(174, 185, 216))
    return by


# ---------------------------------------------------------------- site card
def build_index():
    img = gradient((11, 16, 38), (18, 27, 77), (12, 18, 48), (28, 48, 181))
    img = glow(img, (96, 132, 255), 1015, 70, 560, 150)
    img = glow(img, (46, 91, 255), -40, 690, 520, 90)
    img = dotgrid(img)
    draw = ImageDraw.Draw(img)

    tracked(draw, PAD, 96, "SENIOR PRODUCT DESIGNER · WROCŁAW, POLAND",
            f(DEMI, 21), (170, 184, 224), 3)

    L1 = "I turn complex products"
    seg = [("into experiences people ", (255, 255, 255)),
           ("trust", (143, 179, 255)),
           (".", (255, 255, 255))]
    L2 = "".join(t for t, _ in seg)
    maxw = W - 2 * PAD
    size = 74
    while size > 40:
        hf = f(HEAVY, size)
        if max(draw.textlength(L1, font=hf), draw.textlength(L2, font=hf)) <= maxw:
            break
        size -= 1
    y0 = 176
    draw.text((PAD, y0), L1, font=hf, fill=(255, 255, 255))
    x, y1 = PAD, y0 + round(size * 1.19)
    for text, col in seg:
        draw.text((x, y1), text, font=hf, fill=col)
        x += draw.textlength(text, font=hf)

    by = footer(draw, "10+ yrs · 30+ products shipped · Global Finance “Best Online Portal” 2021")

    # 'open to work' chip, bottom-right
    chip, cf = "Open to new roles", f(DEMI, 20)
    cw = draw.textlength(chip, font=cf)
    pad_x, dot, gap = 24, 11, 14
    chip_w = pad_x + dot + gap + cw + pad_x
    cx0, ch, cy0 = W - PAD - chip_w, 46, by + 4
    draw.rounded_rectangle([cx0, cy0, cx0 + chip_w, cy0 + ch], radius=ch // 2,
                           outline=(96, 110, 158), width=1)
    dy0 = cy0 + ch // 2 - dot // 2
    draw.ellipse([cx0 + pad_x, dy0, cx0 + pad_x + dot, dy0 + dot], fill=(34, 197, 94))
    tb = cf.getbbox(chip)
    ty = cy0 + (ch - (tb[3] - tb[1])) // 2 - tb[1]
    draw.text((cx0 + pad_x + dot + gap, ty), chip, font=cf, fill=(224, 231, 246))

    img.save("assets/og-image.png", "PNG")
    print("wrote assets/og-image.png", img.size)


# ------------------------------------------------------------- case cards
# base/glow/accent mirror each .pcard tint in styles.css.
CASES = [
    dict(slug="tbc", kicker="TBC BANK · BANKING",
         base=((12, 39, 67), (6, 24, 46)), glow=(0, 163, 224), accent=(126, 205, 240),
         title="Business Internet Bank redesign — Global Finance “Best Online Portal” 2021",
         tiles=[("2021", "Best Online Portal"), ("55→64", "Business Mobile NPS"), ("−7%", "website drop-off")]),
    dict(slug="golance", kicker="GOLANCE · AI MARKETPLACE",
         base=((6, 16, 58), (2, 11, 46)), glow=(116, 52, 250), accent=(186, 158, 255),
         title="Matching trust — the UX for goLance's AI cultural-fit engine",
         tiles=[("+25%", "project engagement"), ("−22%", "checkout drop-off"), ("−40%", "support load")]),
    dict(slug="novocure", kicker="NOVOCURE · HEALTHCARE, VIA EPAM",
         base=((9, 48, 87), (4, 30, 58)), glow=(97, 180, 228), accent=(150, 208, 240),
         title="Restarting an oncology HCP portal from zero — three markets at WCAG AA",
         tiles=[("+21%", "sales, Q4 2024"), ("87/100", "SUS score"), ("3", "markets at WCAG AA")]),
    dict(slug="rogers", kicker="ROGERS · TELECOM, VIA EPAM",
         base=((35, 9, 11), (18, 4, 5)), glow=(238, 39, 34), accent=(255, 150, 145),
         title="OneView: cutting the sales rep's cognitive load",
         tiles=[("−25%", "time-on-task"), ("−80%", "user error rate"), ("3wk→1wk", "agent onboarding")]),
]


def build_case(c):
    tl, br = c["base"]
    img = gradient(tl, tl, tl, br)
    img = glow(img, c["glow"], 1000, 640, 620, 120)
    img = glow(img, c["glow"], 1060, 40, 420, 55)
    img = dotgrid(img, colour=c["accent"], step=30, alpha=26)
    draw = ImageDraw.Draw(img)

    tracked(draw, PAD, 96, c["kicker"], f(DEMI, 21), c["accent"], 3)

    # title lives in a fixed box so the tiles below keep one baseline on every card
    TITLE_Y, TITLE_H = 168, 188
    hf, lines = fit(draw, c["title"], W - 2 * PAD, TITLE_H, 3, 60, 34)
    y = TITLE_Y
    for ln in lines:
        draw.text((PAD, y), ln, font=hf, fill=(255, 255, 255))
        y += round(hf.size * LINE_RATIO)

    # three metric tiles on one baseline, evenly spaced across the content width
    ty0 = TITLE_Y + TITLE_H + 24
    col = (W - 2 * PAD) // 3
    nf, lf = f(HEAVY, 40), f(MEDIUM, 18)
    for i, (num, label) in enumerate(c["tiles"]):
        x = PAD + i * col
        draw_mixed(draw, (x, ty0), num, nf, c["accent"])
        draw.text((x, ty0 + 50), label, font=lf, fill=(198, 209, 232))

    footer(draw, "Case study · temorazmadze.com")

    out = f"assets/og-{c['slug']}.png"
    img.save(out, "PNG")
    print(f"wrote {out}", img.size)


if __name__ == "__main__":
    build_index()
    for case in CASES:
        build_case(case)
