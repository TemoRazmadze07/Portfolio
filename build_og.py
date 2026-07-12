#!/usr/bin/env python3
"""Generate the Open Graph / social share card (assets/og-image.png, 1200x630).
Styled after the site's navy 'AI panel' — dark gradient, blue glow, electric-blue
accent on the word 'trust', echoing the hero headline. Uses Avenir Next as the
closest system stand-in for the site's Plus Jakarta Sans."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1200, 630
FONT = "/System/Library/Fonts/Avenir Next.ttc"
HEAVY, BOLD, DEMI, MEDIUM = 8, 0, 2, 5
f = lambda idx, sz: ImageFont.truetype(FONT, sz, index=idx)

# ---- base: bilinear diagonal gradient (TL deep navy -> BR electric blue) ----
corners = Image.new("RGB", (2, 2))
corners.putpixel((0, 0), (11, 16, 38))    # top-left  #0b1026
corners.putpixel((1, 0), (18, 27, 77))    # top-right #121b4d
corners.putpixel((0, 1), (12, 18, 48))    # bottom-left
corners.putpixel((1, 1), (28, 48, 181))   # bottom-right #1c30b5
img = corners.resize((W, H), Image.BICUBIC)


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

# top-right aurora + faint bottom-left glow, like the panels
img = Image.composite(Image.new("RGB", (W, H), (96, 132, 255)), img, radial(1015, 70, 560, 150))
img = Image.composite(Image.new("RGB", (W, H), (46, 91, 255)), img, radial(-40, 690, 520, 90))

# subtle dot grid, masked to the upper-right (nods to the hero/contact art)
dots = Image.new("L", (W, H), 0)
dd = ImageDraw.Draw(dots)
for y in range(0, H, 26):
    for x in range(0, W, 26):
        dd.ellipse([x - 1, y - 1, x + 1, y + 1], fill=42)
img = Image.composite(Image.new("RGB", (W, H), (150, 178, 255)), img, dots)

draw = ImageDraw.Draw(img)
PAD = 84

# ---- eyebrow (tracked uppercase) ----
def tracked(x, y, text, font, fill, track):
    for ch in text:
        draw.text((x, y), ch, font=font, fill=fill)
        x += draw.textlength(ch, font=font) + track
    return x

tracked(PAD, 96, "SENIOR PRODUCT DESIGNER · WROCŁAW, POLAND", f(DEMI, 21), (170, 184, 224), 3)

# ---- headline (auto-fit so the accent word never clips the margin) ----
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
line_h = round(size * 1.19)
y0 = 176
draw.text((PAD, y0), L1, font=hf, fill=(255, 255, 255))
# second line: the accent word 'trust' in light electric-blue
x, y1 = PAD, y0 + line_h
for text, col in seg:
    draw.text((x, y1), text, font=hf, fill=col)
    x += draw.textlength(text, font=hf)

# ---- divider ----
dy = 468
draw.line([(PAD, dy), (W - PAD, dy)], fill=(255, 255, 255, 0))
draw.rectangle([PAD, dy, W - PAD, dy + 1], fill=(70, 84, 130))

# ---- name + credential (with blue accent bar) ----
by = 508
draw.rounded_rectangle([PAD, by + 4, PAD + 5, by + 52], radius=2, fill=(143, 179, 255))
nx = PAD + 22
draw.text((nx, by), "Temuri Razmadze", font=f(BOLD, 33), fill=(255, 255, 255))
draw.text((nx, by + 46), "10+ yrs · 30+ products shipped · Global Finance “Best Online Portal” 2021",
          font=f(MEDIUM, 20), fill=(174, 185, 216))

# ---- 'open to work' chip, bottom-right ----
chip = "Open to new roles"
cf = f(DEMI, 20)
cw = draw.textlength(chip, font=cf)
pad_x, dot, gap = 24, 11, 14
chip_w = pad_x + dot + gap + cw + pad_x
cx0 = W - PAD - chip_w
ch = 46
cy0 = by + 4
draw.rounded_rectangle([cx0, cy0, cx0 + chip_w, cy0 + ch], radius=ch // 2,
                       outline=(96, 110, 158), width=1)
dy0 = cy0 + ch // 2 - dot // 2
draw.ellipse([cx0 + pad_x, dy0, cx0 + pad_x + dot, dy0 + dot], fill=(34, 197, 94))
# text vertically centered via its bbox
tb = cf.getbbox(chip)
ty = cy0 + (ch - (tb[3] - tb[1])) // 2 - tb[1]
draw.text((cx0 + pad_x + dot + gap, ty), chip, font=cf, fill=(224, 231, 246))

img.save("assets/og-image.png", "PNG")
print("wrote assets/og-image.png", img.size)
