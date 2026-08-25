#!/usr/bin/env python3
"""
cards.py - generate a self-hosted stat card and project cards as static SVGs.

Usage:
  python scripts/cards.py --user Shafiq-456 --out assets
"""
import argparse
import json
import os
import urllib.request


API = "https://api.github.com"


def gh_get(path, token=None):
    req = urllib.request.Request(
        f"{API}{path}",
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "profile-cards",
            **({"Authorization": f"Bearer {token}"} if token else {}),
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
    streak = None
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


def card_shell(width, height, theme, accent):
    bg = "#0d1117" if theme == "dark" else "#ffffff"
    border = "#30363d" if theme == "dark" else "#d0d7de"
    text = "#e6edf3" if theme == "dark" else "#24292f"
    sub = "#8b949e" if theme == "dark" else "#57606a"
    return bg, border, text, sub


def draw_stat_card(stats, out_base, accent):
    tiles = [
        ("Public Repos", stats["repos"]),
        ("Total Stars", stats["stars"]),
        ("Total Forks", stats["forks"]),
    ]
    if stats["contributions"] is not None:
        tiles.append(("Contributions", stats["contributions"]))

    for theme in ("dark", "light"):
        bg, border, text, sub = card_shell(0, 0, theme, accent)
        w = 480
        h = 120 if len(tiles) <= 3 else 150
        tile_w = w / len(tiles) if len(tiles) <= 3 else w / 3
        cols = min(len(tiles), 3)
        rows = 1 if len(tiles) <= 3 else 2
        tile_w = w / cols

        parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" font-family="JetBrains Mono, monospace">']
        parts.append(f'<rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" rx="10" fill="{bg}" stroke="{border}"/>')
        for idx, (label, value) in enumerate(tiles):
            col = idx % cols
            row = idx // cols
            x = col * tile_w
            y = row * (h / rows)
            cx = x + tile_w / 2
            cy = y + (h / rows) / 2
            parts.append(f'<text x="{cx}" y="{cy-6}" text-anchor="middle" fill="{accent}" font-size="24" font-weight="700">{value}</text>')
            parts.append(f'<text x="{cx}" y="{cy+16}" text-anchor="middle" fill="{sub}" font-size="11">{label}</text>')
        parts.append("</svg>")
        out_path = f"{out_base}-{theme}.svg"
        with open(out_path, "w") as f:
            f.write("\n".join(parts))
        print(f"wrote {out_path}")


def draw_project_card(repo_meta, description, out_base, accent):
    for theme in ("dark", "light"):
        bg, border, text, sub = card_shell(0, 0, theme, accent)
        w, h = 420, 150
        name = repo_meta.get("name", "repo")
        lang = repo_meta.get("language") or "—"
        stars = repo_meta.get("stargazers_count", 0)
        forks = repo_meta.get("forks_count", 0)
        desc = description or repo_meta.get("description") or ""
        if len(desc) > 90:
            desc = desc[:87] + "..."

        words = desc.split()
        lines, cur = [], ""
        for wd in words:
            if len(cur) + len(wd) + 1 > 46:
                lines.append(cur)
                cur = wd
            else:
                cur = (cur + " " + wd).strip()
        if cur:
            lines.append(cur)
        lines = lines[:3]

        parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" font-family="JetBrains Mono, monospace">']
        parts.append(f'<rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" rx="10" fill="{bg}" stroke="{border}"/>')
        parts.append(f'<text x="20" y="34" fill="{accent}" font-size="17" font-weight="700">{name}</text>')
        y0 = 58
        for i, line in enumerate(lines):
            parts.append(f'<text x="20" y="{y0 + i*18}" fill="{text}" font-size="12">{line}</text>')
        parts.append(f'<circle cx="24" cy="{h-22}" r="5" fill="{accent}"/>')
        parts.append(f'<text x="34" y="{h-18}" fill="{sub}" font-size="11">{lang}</text>')
        parts.append(f'<text x="150" y="{h-18}" fill="{sub}" font-size="11">★ {stars}</text>')
        parts.append(f'<text x="220" y="{h-18}" fill="{sub}" font-size="11">⑂ {forks}</text>')
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

    proj_path = args.projects or os.path.join(os.path.dirname(args.out), "assets", "projects.json")
    if not os.path.exists(proj_path):
        proj_path = os.path.join("assets", "projects.json")

    if os.path.exists(proj_path):
        with open(proj_path) as f:
            proj_data = json.load(f)
        for p in proj_data.get("projects", []):
            repo_name = p["repo"]
            try:
                meta = gh_get(f"/repos/{args.user}/{repo_name}", token)
            except Exception:
                meta = {"name": repo_name}
            draw_project_card(meta, p.get("description"), os.path.join(args.out, f"card-{repo_name.lower()}"), args.accent)


if __name__ == "__main__":
    main()
