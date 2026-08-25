#!/usr/bin/env python3
"""
dotify.py - turn a photo into a dot-matrix SVG portrait.

Usage:
  python scripts/dotify.py me.jpg -o assets/portrait --cols 100 --equalize --detail 0.5 --color
"""
import argparse
import math
from PIL import Image, ImageOps, ImageFilter


def equalize_luminance(img: Image.Image) -> Image.Image:
    gray = img.convert("L")
    return ImageOps.equalize(gray)


def build_svg(cells, cols, rows, cell_size, colorized, accent="#6366F1"):
    w = cols * cell_size
    h = rows * cell_size
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">']
    parts.append(f'<rect width="{w}" height="{h}" fill="transparent"/>')
    for (x, y, r, color) in cells:
        cx = x * cell_size + cell_size / 2
        cy = y * cell_size + cell_size / 2
        fill = color if colorized else accent
        if r > 0.01:
            parts.append(f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{r:.2f}" fill="{fill}"/>')
    parts.append("</svg>")
    return "\n".join(parts)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("image")
    ap.add_argument("-o", "--out", required=True, help="output basename (without extension)")
    ap.add_argument("--cols", type=int, default=88)
    ap.add_argument("--equalize", action="store_true")
    ap.add_argument("--detail", type=float, default=0.0)
    ap.add_argument("--color", action="store_true")
    ap.add_argument("--circle", action="store_true")
    ap.add_argument("--square", action="store_true")
    ap.add_argument("--focus", default="0.5,0.5")
    ap.add_argument("--invert", action="store_true")
    ap.add_argument("--accent", default="#6366F1")
    args = ap.parse_args()

    img = Image.open(args.image).convert("RGBA")

    has_alpha = img.mode == "RGBA" and img.getchannel("A").getextrema()[0] < 255

    if args.square:
        fx, fy = (float(v) for v in args.focus.split(","))
        side = min(img.size)
        w, h = img.size
        left = int((w - side) * fx)
        top = int((h - side) * fy)
        left = max(0, min(w - side, left))
        top = max(0, min(h - side, top))
        img = img.crop((left, top, left + side, top + side))

    cell = 6
    cols = args.cols
    rows = int(img.height / img.width * cols) if not args.square else cols
    small = img.resize((cols, rows), Image.LANCZOS)

    gray = small.convert("L")
    if args.equalize:
        if has_alpha:
            mask = small.getchannel("A")
            gray = ImageOps.equalize(gray, mask=mask)
        else:
            gray = ImageOps.equalize(gray)

    if args.detail > 0:
        edges = gray.filter(ImageFilter.FIND_EDGES)
        gray_px = gray.load()
        edge_px = edges.load()
        for yy in range(rows):
            for xx in range(cols):
                v = gray_px[xx, yy] + edge_px[xx, yy] * args.detail
                gray_px[xx, yy] = max(0, min(255, int(v)))

    if args.invert:
        gray = ImageOps.invert(gray)

    gpx = gray.load()
    rgba = small.load()
    alpha = small.getchannel("A").load() if has_alpha else None

    cells = []
    max_r = cell * 0.48
    ccx, ccy = cols / 2.0, rows / 2.0
    circle_r = min(cols, rows) / 2.0
    for yy in range(rows):
        for xx in range(cols):
            if alpha is not None and alpha[xx, yy] < 10:
                continue
            if args.circle:
                dist = math.hypot(xx - ccx + 0.5, yy - ccy + 0.5)
                if dist > circle_r:
                    continue
            brightness = gpx[xx, yy] / 255.0
            radius = max_r * brightness
            if radius < 0.35:
                continue
            if args.color:
                r, g, b = rgba[xx, yy][:3]
                color = f"rgb({r},{g},{b})"
            else:
                color = args.accent
            cells.append((xx, yy, radius, color))

    svg = build_svg(cells, cols, rows, cell, args.color, args.accent)

    if args.color:
        out_path = f"{args.out}.svg"
        with open(out_path, "w") as f:
            f.write(svg)
        print(f"wrote {out_path}")
    else:
        for suffix in ("dark", "light"):
            out_path = f"{args.out}-{suffix}.svg"
            with open(out_path, "w") as f:
                f.write(svg)
            print(f"wrote {out_path}")


if __name__ == "__main__":
    main()
