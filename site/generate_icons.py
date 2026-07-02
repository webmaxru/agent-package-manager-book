"""Generate raster favicon / app-icon assets for the book site.

This is a LOCAL one-off tool, deliberately kept out of the CI build (which only
installs PyYAML). It draws the raster derivatives of ``site/favicon.svg`` — the
white "package cube" on the four-property gradient — and writes them into
``site/``:

    favicon.ico            (16/32/48, rounded, transparent)
    apple-touch-icon.png   (180, full-bleed square; iOS masks its own corners)
    icon-192.png           (192, rounded, transparent; PWA "any")
    icon-512.png           (512, rounded, transparent; PWA "any")
    icon-maskable-512.png   (512, full-bleed with safe padding; PWA "maskable")

Re-run only when the brand mark changes:

    python site/generate_icons.py

Requires Pillow (``pip install pillow``). The committed PNG/ICO outputs are what
ships; ``site/generate.py`` merely references them.
"""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw

SITE = Path(__file__).resolve().parent

# Four-property gradient (indigo -> teal -> amber -> magenta), matching favicon.svg.
STOPS: list[tuple[float, tuple[int, int, int]]] = [
    (0.00, (90, 84, 240)),
    (0.38, (14, 165, 165)),
    (0.70, (231, 178, 61)),
    (1.00, (194, 70, 138)),
]
WHITE = (255, 255, 255, 255)
SS = 4  # supersampling factor for antialiasing

# Package-cube glyph, defined in a 0..64 coordinate space (matches favicon.svg).
OUTLINE = [(32, 15), (49, 24), (49, 40), (32, 49), (15, 40), (15, 24), (32, 15)]
TOP = [(15, 24), (32, 33), (49, 24)]
SEAM = [(32, 33), (32, 49)]


def _lerp(a: int, b: int, t: float) -> int:
    return round(a + (b - a) * t)


def _grad_color(t: float) -> tuple[int, int, int, int]:
    t = min(1.0, max(0.0, t))
    for (t0, c0), (t1, c1) in zip(STOPS, STOPS[1:]):
        if t0 <= t <= t1:
            k = (t - t0) / (t1 - t0) if t1 > t0 else 0.0
            return (_lerp(c0[0], c1[0], k), _lerp(c0[1], c1[1], k), _lerp(c0[2], c1[2], k), 255)
    return (*STOPS[-1][1], 255)


def _diagonal_gradient(size: int) -> Image.Image:
    """A smooth top-left -> bottom-right diagonal gradient, drawn per anti-diagonal."""
    img = Image.new("RGBA", (size, size))
    draw = ImageDraw.Draw(img)
    span = 2 * (size - 1)
    for d in range(span + 1):
        color = _grad_color(d / span)
        x0 = max(0, d - (size - 1))
        y0 = d - x0
        x1 = min(d, size - 1)
        y1 = d - x1
        draw.line([(x0, y0), (x1, y1)], fill=color)
    return img


def make_icon(size: int, rounded: bool = True, pad_ratio: float = 0.0) -> Image.Image:
    """Render one icon: gradient chip (rounded or full-bleed) + white package cube."""
    big = size * SS
    chip = Image.new("RGBA", (big, big), (0, 0, 0, 0))
    gradient = _diagonal_gradient(big)

    mask = Image.new("L", (big, big), 0)
    md = ImageDraw.Draw(mask)
    if rounded:
        md.rounded_rectangle([0, 0, big - 1, big - 1], radius=int(big * 0.234), fill=255)
    else:
        md.rectangle([0, 0, big - 1, big - 1], fill=255)
    chip.paste(gradient, (0, 0), mask)

    draw = ImageDraw.Draw(chip)
    scale = big / 64.0
    shrink = 1.0 - 2.0 * pad_ratio

    def pt(x: float, y: float) -> tuple[float, float]:
        # Scale around the 32,32 center to honor the maskable safe zone.
        cx = cy = 32.0
        return ((cx + (x - cx) * shrink) * scale, (cy + (y - cy) * shrink) * scale)

    width = max(1, round(4.25 * scale * shrink))
    for poly in (OUTLINE, TOP, SEAM):
        draw.line([pt(x, y) for x, y in poly], fill=WHITE, width=width, joint="curve")
    # Round the joints/caps with dots so the cube reads cleanly at small sizes.
    r = width / 2
    for x, y in {p for poly in (OUTLINE, TOP, SEAM) for p in poly}:
        px, py = pt(x, y)
        draw.ellipse([px - r, py - r, px + r, py + r], fill=WHITE)

    return chip.resize((size, size), Image.LANCZOS)


def main() -> None:
    make_icon(512).save(SITE / "icon-512.png")
    make_icon(192).save(SITE / "icon-192.png")
    make_icon(512, rounded=False, pad_ratio=0.12).save(SITE / "icon-maskable-512.png")
    make_icon(180, rounded=False).convert("RGB").save(SITE / "apple-touch-icon.png")
    make_icon(64).save(SITE / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])
    print("Wrote favicon.ico, apple-touch-icon.png, icon-192.png, icon-512.png, icon-maskable-512.png")


if __name__ == "__main__":
    main()
