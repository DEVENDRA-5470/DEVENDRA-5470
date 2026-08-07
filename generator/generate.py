"""
generate.py
Fetches live GitHub stats for a user via the GitHub REST + GraphQL APIs,
then renders them into the custom themed SVGs used in the README
(assets/generated/*.svg).

Run locally:
    GITHUB_TOKEN=xxxx GITHUB_USERNAME=DEVENDRA-5470 python generator/generate.py

In CI, GITHUB_TOKEN is provided automatically by the workflow.
"""

import os
import sys
import requests
import yaml

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "config.yml")

with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    CONFIG = yaml.safe_load(f)

USERNAME = os.environ.get("GITHUB_USERNAME") or CONFIG.get("username")
TOKEN = os.environ.get("GITHUB_TOKEN")
OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "assets", "generated")

if not USERNAME:
    print("ERROR: no username found in config.yml or GITHUB_USERNAME env var")
    sys.exit(1)

if not TOKEN:
    print("ERROR: GITHUB_TOKEN not set")
    sys.exit(1)

HEADERS = {"Authorization": f"Bearer {TOKEN}"}
GRAPHQL_URL = "https://api.github.com/graphql"
REST_URL = "https://api.github.com"

_theme = CONFIG.get("theme", {})
ACCENT_A = _theme.get("synapse_cyan", "#38BDF8")
ACCENT_B = _theme.get("axon_amber", "#22D3A5")
BG = _theme.get("void", "#080c14")
PANEL = _theme.get("nebula", "#0d1520")
BORDER = _theme.get("star_dust", "#1a2b3c")
TEXT_MAIN = _theme.get("text_bright", "#f0f6fc")
TEXT_MUTED = _theme.get("text_dim", "#94a3b8")
FONT = "Fira Code, monospace"


def gql(query: str) -> dict:
    resp = requests.post(GRAPHQL_URL, json={"query": query}, headers=HEADERS, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    if "errors" in data:
        raise RuntimeError(data["errors"])
    return data["data"]


def rest_get(path: str, params: dict | None = None):
    resp = requests.get(f"{REST_URL}{path}", headers=HEADERS, params=params or {}, timeout=30)
    resp.raise_for_status()
    return resp.json()


def fetch_contributions() -> dict:
    query = f"""
    {{
      user(login: "{USERNAME}") {{
        contributionsCollection {{
          contributionCalendar {{ totalContributions }}
          totalCommitContributions
          totalPullRequestContributions
          totalIssueContributions
        }}
      }}
    }}
    """
    data = gql(query)["user"]["contributionsCollection"]
    return {
        "contributions_year": data["contributionCalendar"]["totalContributions"],
        "commits": data["totalCommitContributions"],
        "prs": data["totalPullRequestContributions"],
        "issues": data["totalIssueContributions"],
    }


def fetch_stats() -> dict:
    # repos, stars, forks via REST (works reliably with the default Actions token)
    repos = []
    page = 1
    while True:
        batch = rest_get(f"/users/{USERNAME}/repos", {"type": "owner", "per_page": 100, "page": page})
        if not batch:
            break
        repos.extend(batch)
        page += 1
        if page > 5:  # safety cap
            break

    repos = [r for r in repos if not r.get("fork")]
    stars = sum(r.get("stargazers_count", 0) for r in repos)
    forks = sum(r.get("forks_count", 0) for r in repos)

    # language breakdown via REST, capped to first 20 repos to stay within rate limits
    lang_totals: dict[str, int] = {}
    for r in repos[:20]:
        try:
            langs = rest_get(f"/repos/{USERNAME}/{r['name']}/languages")
        except requests.HTTPError:
            continue
        for name, size in langs.items():
            lang_totals[name] = lang_totals.get(name, 0) + size

    palette = [ACCENT_A, ACCENT_B, "#c4b5fd", "#fbbf24", "#f87171"]
    total_size = sum(lang_totals.values()) or 1
    top_langs = sorted(lang_totals.items(), key=lambda kv: kv[1], reverse=True)[:5]
    lang_pct = [
        (name, round(size / total_size * 100, 1), palette[i % len(palette)])
        for i, (name, size) in enumerate(top_langs)
    ]

    contrib = fetch_contributions()

    return {
        "repos": len(repos),
        "stars": stars,
        "forks": forks,
        "languages": lang_pct,
        **contrib,
    }


def render_stats_card(stats: dict) -> str:
    blocks = [
        (f'{stats["contributions_year"]:,}', "contributions", "this year"),
        (f'{stats["repos"]}', "repositories", "owned"),
        (f'{stats["stars"]}', "stars", "earned"),
        (f'{stats["prs"]}', "pull requests", "opened"),
    ]

    block_svgs = []
    x = 30
    w = 200
    gap = 13
    for value, label1, label2 in blocks:
        block_svgs.append(f"""
        <rect x="{x}" y="52" width="{w}" height="95" rx="8" fill="{PANEL}" stroke="{BORDER}"/>
        <rect x="{x}" y="52" width="4" height="95" rx="2" fill="url(#accent)"/>
        <text x="{x+22}" y="90" font-size="28" font-weight="700" fill="{TEXT_MAIN}">{value}</text>
        <text x="{x+22}" y="112" font-size="12" fill="{TEXT_MUTED}">{label1}</text>
        <text x="{x+22}" y="128" font-size="12" fill="{TEXT_MUTED}">{label2}</text>
        """)
        x += w + gap

    return f"""<svg width="900" height="170" viewBox="0 0 900 170" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="accent" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="{ACCENT_A}"/>
      <stop offset="100%" stop-color="{ACCENT_B}"/>
    </linearGradient>
  </defs>
  <rect width="900" height="170" rx="10" fill="{BG}" stroke="{BORDER}"/>
  <text x="30" y="34" font-family="{FONT}" font-size="13" fill="#4b6478">// mission telemetry — live from GitHub API</text>
  <g font-family="{FONT}">{''.join(block_svgs)}</g>
</svg>"""


def render_languages(stats: dict) -> str:
    rows = []
    y = 55
    bar_x = 160
    bar_max_w = 620
    for name, pct, color in stats["languages"]:
        bar_w = max(4, bar_max_w * pct / 100)
        rows.append(f"""
        <text x="30" y="{y+13}" font-family="{FONT}" font-size="13" fill="{TEXT_MUTED}">{name}</text>
        <rect x="{bar_x}" y="{y}" width="{bar_max_w}" height="18" rx="4" fill="{PANEL}" stroke="{BORDER}"/>
        <rect x="{bar_x}" y="{y}" width="{bar_w}" height="18" rx="4" fill="{color}"/>
        <text x="{bar_x + bar_max_w + 15}" y="{y+13}" font-family="{FONT}" font-size="12" fill="{TEXT_MAIN}">{pct}%</text>
        """)
        y += 34

    height = y + 25
    return f"""<svg width="900" height="{height}" viewBox="0 0 900 {height}" xmlns="http://www.w3.org/2000/svg">
  <rect width="900" height="{height}" rx="10" fill="{BG}" stroke="{BORDER}"/>
  <text x="30" y="34" font-family="{FONT}" font-size="13" fill="#4b6478">// language telemetry — live from GitHub API</text>
  <g>{''.join(rows)}</g>
</svg>"""


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    stats = fetch_stats()

    with open(os.path.join(OUT_DIR, "stats-card.svg"), "w", encoding="utf-8") as f:
        f.write(render_stats_card(stats))

    with open(os.path.join(OUT_DIR, "languages.svg"), "w", encoding="utf-8") as f:
        f.write(render_languages(stats))

    print("Generated stats-card.svg and languages.svg with live data:")
    print(stats)


if __name__ == "__main__":
    main()
