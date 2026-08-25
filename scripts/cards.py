#!/usr/bin/env python3
"""
cards.py - generate premium stat card and project cards as static SVGs.

Usage:
  python scripts/cards.py --user Shafiq-456 --out assets
"""
import argparse
import json
import os
import urllib.request

API = "https://api.github.com"

LANG_COLORS = {
    "Python": "#3572A5",
    "TypeScript": "#2b7489",
    "JavaScript": "#f1e05a",
    "Dart": "#00B4AB",
    "Java": "#b07219",
    "C++": "#f34b7d",
    "HTML": "#e34c26",
    "CSS": "#563d7c",
    "Shell": "#89e051",
    "Go": "#00ADD8",
    "Rust": "#dea584",
    "Swift": "#F05138",
}


def gh_get(path, token=None):
    req = urllib.request.Request(
        f"{API}{path}",
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "profile-cards",
            **( {"Authorization": f"Bearer {token}"} if token else {}),
        },
    )
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.loads(resp.read().decode())


def graphql(query, token):
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": query}).encode(),
        headers={
            "Authorization": f"Bearer {token}",
            "User-Agent": "profile-cards",
            "Content-Type": "application/json",
        },
    )
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.loads(resp.read().decode())


def user_stats(username, token):
    stars = 0
    forks = 0
    repos = []
    page = 1
    while True:
        batch = gh_get(f"/users/{username}/repos?per_page=100&page={page}&type=owner", token)
        if not batch:
            break
        repos.extend(batch)
        page += 1
        if len(batch) < 100:
            break
    for r in repos:
        stars += r.get("stargazers_count", 0)
        forks += r.get("forks_count", 0)

    total_contribs = None
    if token:
        try:
            q = f'''
            {{
              user(login: "{username}") {{
                contributionsCollection {{
                  contributionCalendar {{ totalContributions }}
                }}
              }}
            }}
            '''
            data = graphql(q, token)
            total_contribs = data["data"]["user"]["contributionsCollection"]["contributionCalendar"]["totalContributions"]
        except Exception:
            total_contribs = None

    return {
        "repos": len(repos),
        "stars": stars,
        "forks": forks,
        "contributions": total_contribs,
    }


def draw_stat_card(stats, out_base, accent):
    """Draws a premium stat card with gradient header, glowing numbers, and clean tile layout."""
    tiles = [
        ("Repositories", stats["repos"], "📦"),
        ("Stars Earned", stats["stars"], "⭐"),
        ("Forks", stats["forks"], "🍴"),
    ]
    if stats["contributions"] is not None:
        tiles.append(("Contributions", stats["contributions"], "🔥"))

    for theme in ("dark", "light"):
        bg         = "#0d1117" if theme == "dark" else "#f6f8fa"
        border     = "#30363d" if theme == "dark" else "#d0d7de"
        text_col   = "#e6edf3" if theme == "dark" else "#24292f"
        sub_col    = "#8b949e" if theme == "dark" else "#57606a"
        tile_bg    = "#161b22" if theme == "dark" else "#ffffff"
        tile_bdr   = "#21262d" if theme == "dark" else "#e1e4e8"

        n = len(tiles)
        tile_w = 130
        gap = 12
        pad = 20
        w = pad * 2 + tile_w * n + gap * (n - 1)
        h = 130

        parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
            f'viewBox="0 0 {w} {h}" font-family="\'JetBrains Mono\', monospace">',
            f'<defs>',
            f'  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">',
            f'    <stop offset="0%" stop-color="{accent}" stop-opacity="0.08"/>',
            f'    <stop offset="100%" stop-color="{accent}" stop-opacity="0.02"/>',
            f'  </linearGradient>',
            f'  <filter id="glow">',
            f'    <feGaussianBlur stdDeviation="2" result="blur"/>',
            f'    <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>',
            f'  </filter>',
            f'</defs>',
            f'<rect x="0" y="0" width="{w}" height="{h}" rx="14" fill="{bg}" stroke="{border}" stroke-width="1"/>',
            f'<rect x="0" y="0" width="{w}" height="{h}" rx="14" fill="url(#bg)"/>',
        ]

        for idx, (label, value, icon) in enumerate(tiles):
            x = pad + idx * (tile_w + gap)
            y = 12
            th = h - 24
            cx = x + tile_w / 2

            parts.append(f'<rect x="{x}" y="{y}" width="{tile_w}" height="{th}" rx="10" fill="{tile_bg}" stroke="{tile_bdr}" stroke-width="1"/>')
            parts.append(f'<text x="{cx}" y="{y + 26}" text-anchor="middle" font-size="18" fill="{border}">{icon}</text>')
            parts.append(f'<text x="{cx}" y="{y + 60}" text-anchor="middle" font-size="26" font-weight="700" fill="{accent}" filter="url(#glow)">{value}</text>')
            parts.append(f'<text x="{cx}" y="{y + 82}" text-anchor="middle" font-size="10" fill="{sub_col}">{label}</text>')

        parts.append("</svg>")
        out_path = f"{out_base}-{theme}.svg"
        with open(out_path, "w") as f:
            f.write("\n".join(parts))
        print(f"wrote {out_path}")


def draw_project_card(repo_meta, description, tech_stack, out_base, accent):
    """Draws a premium project card with gradient header, glow, tech badges, and star/fork row."""
    for theme in ("dark", "light"):
        bg         = "#0d1117" if theme == "dark" else "#f6f8fa"
        border     = "#30363d" if theme == "dark" else "#d0d7de"
        text_col   = "#e6edf3" if theme == "dark" else "#24292f"
        sub_col    = "#8b949e" if theme == "dark" else "#57606a"
        hdr_bg     = "#161b22" if theme == "dark" else "#eaeef2"

        w, h = 440, 170
        name   = repo_meta.get("name", "repo")
        lang   = repo_meta.get("language") or "—"
        stars  = repo_meta.get("stargazers_count", 0)
        forks  = repo_meta.get("forks_count", 0)
        desc   = description or repo_meta.get("description") or ""
        if len(desc) > 100:
            desc = desc[:97] + "…"

        # Word-wrap description
        words = desc.split()
        lines, cur = [], ""
        for wd in words:
            if len(cur) + len(wd) + 1 > 52:
                lines.append(cur)
                cur = wd
            else:
                cur = (cur + " " + wd).strip()
        if cur:
            lines.append(cur)
        lines = lines[:3]

        lang_color = LANG_COLORS.get(lang, accent)

        # Build tech stack badge string
        badges = tech_stack[:4] if tech_stack else []

        parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
            f'viewBox="0 0 {w} {h}" font-family="\'JetBrains Mono\', monospace">',
            f'<defs>',
            f'  <linearGradient id="hdr" x1="0" y1="0" x2="1" y2="0">',
            f'    <stop offset="0%" stop-color="{accent}" stop-opacity="1"/>',
            f'    <stop offset="100%" stop-color="{accent}" stop-opacity="0.5"/>',
            f'  </linearGradient>',
            f'  <linearGradient id="card-bg" x1="0" y1="0" x2="0" y2="1">',
            f'    <stop offset="0%" stop-color="{accent}" stop-opacity="0.05"/>',
            f'    <stop offset="100%" stop-color="{accent}" stop-opacity="0.0"/>',
            f'  </linearGradient>',
            f'  <clipPath id="clip"><rect width="{w}" height="{h}" rx="14"/></clipPath>',
            f'  <filter id="glow">',
            f'    <feGaussianBlur stdDeviation="3" result="blur"/>',
            f'    <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>',
            f'  </filter>',
            f'</defs>',
            # Card background
            f'<rect width="{w}" height="{h}" rx="14" fill="{bg}" stroke="{border}" stroke-width="1"/>',
            f'<rect width="{w}" height="{h}" rx="14" fill="url(#card-bg)"/>',
            # Top accent stripe
            f'<rect width="{w}" height="4" rx="0" fill="url(#hdr)" clip-path="url(#clip)"/>',
            # Folder icon placeholder
            f'<rect x="18" y="18" width="18" height="14" rx="3" fill="{accent}" opacity="0.85"/>',
            f'<rect x="18" y="16" width="8" height="5" rx="2" fill="{accent}" opacity="0.6"/>',
            # Repo name
            f'<text x="44" y="31" fill="{accent}" font-size="15" font-weight="700" filter="url(#glow)">{name}</text>',
        ]

        # Description lines
        y0 = 54
        for i, line in enumerate(lines):
            parts.append(f'<text x="18" y="{y0 + i * 17}" fill="{text_col}" font-size="11.5">{line}</text>')

        # Tech stack badges
        bx = 18
        by = h - 42
        for badge in badges:
            bw = len(badge) * 7 + 14
            parts.append(f'<rect x="{bx}" y="{by}" width="{bw}" height="16" rx="8" fill="{accent}" fill-opacity="0.15" stroke="{accent}" stroke-opacity="0.4" stroke-width="1"/>')
            parts.append(f'<text x="{bx + bw/2}" y="{by + 11}" text-anchor="middle" fill="{accent}" font-size="9.5">{badge}</text>')
            bx += bw + 6

        # Footer: language dot + stars + forks
        fy = h - 18
        parts.append(f'<circle cx="18" cy="{fy - 3}" r="5" fill="{lang_color}"/>')
        parts.append(f'<text x="28" y="{fy}" fill="{sub_col}" font-size="10.5">{lang}</text>')
        parts.append(f'<text x="{w - 120}" y="{fy}" fill="{sub_col}" font-size="10.5">★ {stars}</text>')
        parts.append(f'<text x="{w - 68}" y="{fy}" fill="{sub_col}" font-size="10.5">⑂ {forks}</text>')

        parts.append("</svg>")
        out_path = f"{out_base}-{theme}.svg"
        with open(out_path, "w") as f:
            f.write("\n".join(parts))
        print(f"wrote {out_path}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--user", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--projects", default=None, help="path to projects.json")
    ap.add_argument("--accent", default="#6366F1")
    args = ap.parse_args()

    token = os.environ.get("METRICS_TOKEN") or os.environ.get("GITHUB_TOKEN")

    stats = user_stats(args.user, token)
    draw_stat_card(stats, os.path.join(args.out, "stat-card"), args.accent)

    proj_path = args.projects or os.path.join("assets", "projects.json")
    if not os.path.exists(proj_path):
        proj_path = os.path.join(os.path.dirname(args.out), "assets", "projects.json")

    if os.path.exists(proj_path):
        with open(proj_path) as f:
            proj_data = json.load(f)
        for p in proj_data.get("projects", []):
            repo_name = p["repo"]
            tech_stack = p.get("tech", [])
            try:
                meta = gh_get(f"/repos/{args.user}/{repo_name}", token)
            except Exception:
                meta = {"name": repo_name}
            draw_project_card(
                meta,
                p.get("description"),
                tech_stack,
                os.path.join(args.out, f"card-{repo_name.lower()}"),
                args.accent
            )


if __name__ == "__main__":
    main()
