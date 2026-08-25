#!/usr/bin/env python3
"""
radar.py - draw a radar/spider chart as SVG, in a dark and a light variant.

Self-rated:
  python scripts/radar.py --data assets/skills.json -o assets/radar

Language (from GitHub API):
  python scripts/radar.py --github USERNAME -o assets/radar-langs --limit 7 --values --curve 0.4 \
      --exclude "shell,makefile,dockerfile,batchfile,procfile"
"""
import argparse
import json
import math
import os
import urllib.request


def fetch_language_bytes(username, exclude):
    req = urllib.request.Request(
        f"https://api.github.com/users/{username}/repos?per_page=100&type=owner",
        headers={"Accept": "application/vnd.github+json", "User-Agent": "profile-radar"},
    )
    with urllib.request.urlopen(req, timeout=20) as resp:
        repos = json.loads(resp.read().decode())

    totals = {}
    for repo in repos:
        if repo.get("fork"):
            continue
        name = repo["full_name"]
        lang_req = urllib.request.Request(
            f"https://api.github.com/repos/{name}/languages",
            headers={"Accept": "application/vnd.github+json", "User-Agent": "profile-radar"},
        )
        try:
            with urllib.request.urlopen(lang_req, timeout=20) as resp:
                langs = json.loads(resp.read().decode())
        except Exception:
            continue
        for lang, count in langs.items():
            if lang.lower() in exclude:
                continue
            totals[lang] = totals.get(lang, 0) + count
    return totals


def curve_scale(value, max_value, curve):
    if max_value <= 0:
        return 0.0
    ratio = value / max_value
    return ratio ** curve


def draw_radar(axes, values_raw, out_base, show_values, accent):
    n = len(axes)
    size = 500
    cx, cy = size / 2, size / 2 + 10
    radius = 120
    max_val = max(values_raw) if values_raw else 1

    def point(i, frac):
        angle = -math.pi / 2 + i * (2 * math.pi / n)
        x = cx + math.cos(angle) * radius * frac
        y = cy + math.sin(angle) * radius * frac
        return x, y

    for theme in ("dark", "light"):
        label_color = "#e6edf3" if theme == "dark" else "#24292f"
        grid_color = "#30363d" if theme == "dark" else "#d0d7de"
        fill_color = accent

        parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} {size+20}" width="{size}" height="{size+20}" font-family="JetBrains Mono, monospace">']

        for ring in (0.25, 0.5, 0.75, 1.0):
            pts = " ".join(f"{point(i, ring)[0]:.1f},{point(i, ring)[1]:.1f}" for i in range(n))
            parts.append(f'<polygon points="{pts}" fill="none" stroke="{grid_color}" stroke-width="1"/>')

        for i in range(n):
            x, y = point(i, 1.0)
            parts.append(f'<line x1="{cx}" y1="{cy}" x2="{x:.1f}" y2="{y:.1f}" stroke="{grid_color}" stroke-width="1"/>')

        data_pts = []
        for i, raw in enumerate(values_raw):
            frac = curve_scale(raw, max_val, 1.0) if max_val <= 100 and max(values_raw) <= 100 and False else raw / max_val
            data_pts.append(point(i, frac))
        pts_str = " ".join(f"{x:.1f},{y:.1f}" for x, y in data_pts)
        parts.append(f'<polygon points="{pts_str}" fill="{fill_color}" fill-opacity="0.35" stroke="{fill_color}" stroke-width="2"/>')
        for x, y in data_pts:
            parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.5" fill="{fill_color}"/>')

        for i, label in enumerate(axes):
            lx, ly = point(i, 1.38)
            anchor = "middle"
            if lx < cx - 15:
                anchor = "end"
            elif lx > cx + 15:
                anchor = "start"
            text = label
            if show_values:
                text = f"{label} ({values_raw[i]:.0f})" if isinstance(values_raw[i], float) else f"{label} ({values_raw[i]})"
            parts.append(f'<text x="{lx:.1f}" y="{ly:.1f}" fill="{label_color}" font-size="13" text-anchor="{anchor}">{text}</text>')

        parts.append("</svg>")
        out_path = f"{out_base}-{theme}.svg"
        with open(out_path, "w") as f:
            f.write("\n".join(parts))
        print(f"wrote {out_path}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", help="path to skills.json for self-rated radar")
    ap.add_argument("--github", help="github username, for the language radar")
    ap.add_argument("-o", "--out", required=True)
    ap.add_argument("--limit", type=int, default=7)
    ap.add_argument("--values", action="store_true")
    ap.add_argument("--curve", type=float, default=1.0)
    ap.add_argument("--exclude", default="")
    ap.add_argument("--accent", default="#6366F1")
    args = ap.parse_args()

    if args.data:
        with open(args.data) as f:
            data = json.load(f)
        axes = [a["label"] for a in data["axes"]]
        values = [a["value"] for a in data["axes"]]
        draw_radar(axes, values, args.out, args.values, args.accent)

    elif args.github:
        exclude = {x.strip().lower() for x in args.exclude.split(",") if x.strip()}
        totals = fetch_language_bytes(args.github, exclude)
        if not totals:
            print("no language data found (rate-limited or no public repos) - writing placeholder")
            totals = {"No data": 1}
        ranked = sorted(totals.items(), key=lambda kv: kv[1], reverse=True)[: args.limit]
        axes = [k for k, _ in ranked]
        raw_values = [v for _, v in ranked]
        max_v = max(raw_values)
        scaled = [max_v * curve_scale(v, max_v, args.curve) for v in raw_values]
        # keep the raw byte-derived percentage for the label
        total_bytes = sum(raw_values)
        pct_values = [round(100 * v / total_bytes) for v in raw_values]
        draw_radar(axes, scaled, args.out, args.values, args.accent)
        if args.values:
            print("language share:", dict(zip(axes, pct_values)))
    else:
        raise SystemExit("pass either --data or --github")


if __name__ == "__main__":
    main()
