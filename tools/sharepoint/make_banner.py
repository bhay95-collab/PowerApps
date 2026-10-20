"""Home page banner for SharePoint title area. Same gradient as app headers.
Usage: python3 tools/sharepoint/make_banner.py [width] [height]"""
import sys
from PIL import Image, ImageDraw, ImageFilter

W = int(sys.argv[1]) if len(sys.argv) > 1 else 1920
H = int(sys.argv[2]) if len(sys.argv) > 2 else 400
STOPS = [(0.0, (0, 29, 70)), (0.5, (7, 95, 115)), (1.0, (0, 131, 138))]  # #001D46 > #075F73 > #00838A


def lerp(a, b, t):
    return tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))


def colour_at(t):
    for (t0, c0), (t1, c1) in zip(STOPS, STOPS[1:]):
        if t <= t1:
            return lerp(c0, c1, (t - t0) / (t1 - t0))
    return STOPS[-1][1]


img = Image.new("RGB", (W, H))
px = ImageDraw.Draw(img)
for x in range(W):
    px.line([(x, 0), (x, H)], fill=colour_at(x / (W - 1)))

glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
g = ImageDraw.Draw(glow)
g.ellipse([int(W * 0.70), -int(H * 0.9), int(W * 1.05), int(H * 0.7)], fill=(255, 255, 255, 34))
glow = glow.filter(ImageFilter.GaussianBlur(H * 0.25))
img = Image.alpha_composite(img.convert("RGBA"), glow).convert("RGB")

img.save(sys.argv[3] if len(sys.argv) > 3 else "powerapps/sharepoint/images/Home_Banner_1920x400.png")
