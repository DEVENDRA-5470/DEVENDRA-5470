"""
generate.py
Fetches live GitHub stats for a user via the GitHub REST + GraphQL APIs,
then renders them into the custom themed SVGs used in the README
(assets/generated/*.svg).

Run locally:
    GITHUB_TOKEN=xxxx GITHUB_USERNAME=DEVENDRA-5470 python generator/generate.py

In CI, GITHUB_TOKEN is provided automatically by the workflow.
"""

import html
import math
import os
import random
import sys
from datetime import date, datetime, timezone
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
          contributionCalendar {{
            totalContributions
            weeks {{ contributionDays {{ date contributionCount }} }}
          }}
          totalCommitContributions
          totalPullRequestContributions
          totalIssueContributions
          pullRequestContributions(first: 100) {{ nodes {{ occurredAt }} }}
        }}
      }}
    }}
    """
    data = gql(query)["user"]["contributionsCollection"]

    # per-day counts -> used for the monthly contributions sparkline
    daily = [
        (d["date"], d["contributionCount"])
        for w in data["contributionCalendar"]["weeks"]
        for d in w["contributionDays"]
    ]
    pr_dates = [n["occurredAt"][:10] for n in data["pullRequestContributions"]["nodes"]]

    return {
        "contributions_year": data["contributionCalendar"]["totalContributions"],
        "commits": data["totalCommitContributions"],
        "prs": data["totalPullRequestContributions"],
        "issues": data["totalIssueContributions"],
        "_daily": daily,
        "_pr_dates": pr_dates,
    }


# ---------------------------------------------------------------------------
# Time-series helpers (feed the sparklines with real data)
# ---------------------------------------------------------------------------

def last_n_months(n: int = 12) -> list[str]:
    """Return ['YYYY-MM', ...] for the last n months, oldest first."""
    today = date.today()
    y, m = today.year, today.month
    out = []
    for _ in range(n):
        out.append(f"{y:04d}-{m:02d}")
        m -= 1
        if m == 0:
            y, m = y - 1, 12
    return out[::-1]


def monthly_totals(pairs: list[tuple[str, int]], months: list[str]) -> list[int]:
    """Sum (YYYY-MM-DD, count) pairs into the given month buckets."""
    buckets = {mo: 0 for mo in months}
    for d, c in pairs:
        if d[:7] in buckets:
            buckets[d[:7]] += c
    return [buckets[mo] for mo in months]


def cumulative_by_month(pairs: list[tuple[str, int]], months: list[str]) -> list[int]:
    """Running total of (YYYY-MM-DD, count) pairs as of the end of each month (all-time)."""
    out = []
    for mo in months:
        out.append(sum(c for d, c in pairs if d[:7] <= mo))
    return out


def next_milestone(v: int) -> int:
    """Next 'nice' target above v: 1, 2, 5 x 10^k (e.g. 61 -> 100, 1057 -> 2000)."""
    if v < 1:
        return 1
    k = 10 ** int(math.floor(math.log10(v)))
    for m in (1, 2, 5, 10):
        if m * k > v:
            return m * k
    return 10 * k


def short(n: int) -> str:
    return f"{n/1000:g}k" if n >= 1000 else str(n)


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

    # merge in manually-weighted languages from config.yml (e.g. work/training repos
    # not attributed to this GitHub account), then apply exclude list + max_display
    _lang_cfg = CONFIG.get("languages", {})
    for name, weight in _lang_cfg.get("manual", {}).items():
        lang_totals[name] = lang_totals.get(name, 0) + weight

    exclude = set(_lang_cfg.get("exclude", []))
    lang_totals = {k: v for k, v in lang_totals.items() if k not in exclude}

    max_display = _lang_cfg.get("max_display", 8)
    palette = [ACCENT_A, ACCENT_B, "#c4b5fd", "#fbbf24", "#f87171", "#f472b6", "#a3e635", "#818cf8"]
    total_size = sum(lang_totals.values()) or 1
    top_langs = sorted(lang_totals.items(), key=lambda kv: kv[1], reverse=True)[:max_display]
    lang_pct = [
        (name, round(size / total_size * 100, 1), palette[i % len(palette)])
        for i, (name, size) in enumerate(top_langs)
    ]

    contrib = fetch_contributions()

    # --- 12-month series for the sparklines (all derived from real API data) ---
    months = last_n_months(12)
    repo_created = [(r["created_at"][:10], 1) for r in repos]
    # GitHub's REST API has no per-star timestamps without paging every stargazer,
    # so the stars line is "stars held by repos that existed by that month".
    star_by_repo_age = [(r["created_at"][:10], r.get("stargazers_count", 0)) for r in repos]

    series = {
        "contributions": monthly_totals(contrib.pop("_daily"), months),
        "repos": cumulative_by_month(repo_created, months),
        "stars": cumulative_by_month(star_by_repo_age, months),
        "prs": cumulative_by_month([(d, 1) for d in contrib.pop("_pr_dates")], months),
    }

    return {
        "repos": len(repos),
        "stars": stars,
        "forks": forks,
        "languages": lang_pct,
        "series": series,
        **contrib,
    }


# ---------------------------------------------------------------------------
# Stats card renderer
# ---------------------------------------------------------------------------

def _icon(kind: str, cx: float, cy: float, c: str) -> str:
    if kind == "contrib":
        return (f'<g stroke="{c}" stroke-width="1.8" fill="none" stroke-linecap="round" stroke-linejoin="round">'
                f'<polyline points="{cx-8},{cy+5} {cx-3},{cy-1} {cx+1},{cy+3} {cx+8},{cy-6}"/>'
                f'<polyline points="{cx+3},{cy-6} {cx+8},{cy-6} {cx+8},{cy-1}"/></g>')
    if kind == "repo":
        return (f'<g stroke="{c}" stroke-width="1.8" fill="none" stroke-linejoin="round">'
                f'<path d="M{cx-7},{cy-7} h11 a3,3 0 0 1 3,3 v11 h-11 a3,3 0 0 1 -3,-3 z"/>'
                f'<line x1="{cx-7}" y1="{cy+3}" x2="{cx+7}" y2="{cy+3}"/></g>')
    if kind == "star":
        pts = []
        for i in range(10):
            r = 8.5 if i % 2 == 0 else 3.6
            a = -math.pi / 2 + i * math.pi / 5
            pts.append(f"{cx + r*math.cos(a):.1f},{cy + r*math.sin(a):.1f}")
        return f'<polygon points="{" ".join(pts)}" fill="none" stroke="{c}" stroke-width="1.7" stroke-linejoin="round"/>'
    return (f'<g stroke="{c}" stroke-width="1.8" fill="none" stroke-linecap="round">'
            f'<circle cx="{cx-5}" cy="{cy-6}" r="2.2"/><circle cx="{cx-5}" cy="{cy+6}" r="2.2"/>'
            f'<circle cx="{cx+5}" cy="{cy+6}" r="2.2"/>'
            f'<line x1="{cx-5}" y1="{cy-3.8}" x2="{cx-5}" y2="{cy+3.8}"/>'
            f'<path d="M{cx+5},{cy+3.8} v-6 a3,3 0 0 0 -3,-3 h-3"/></g>')


def _count_steps(value: int) -> list[str]:
    """Intermediate numbers for the count-up animation, ending on the real value."""
    steps = []
    for f in (0, 0.2, 0.47, 0.74, 0.91, 1):
        s = f"{round(value * f):,}"
        if not steps or steps[-1] != s:
            steps.append(s)
    return steps


def render_stats_card(stats: dict) -> str:
    W, H = 900, 220
    CW, CH, CY0, GAP = 200, 136, 58, 13
    series = stats.get("series", {})

    cards = [
        ("contributions", "this year", stats["contributions_year"], ACCENT_A, "#7DFAFF", "contrib", series.get("contributions")),
        ("repositories", "owned", stats["repos"], ACCENT_B, "#86EFAC", "repo", series.get("repos")),
        ("stars", "earned", stats["stars"], "#FBBF24", "#FDE68A", "star", series.get("stars")),
        ("pull requests", "opened", stats["prs"], "#C4B5FD", "#F0ABFC", "pr", series.get("prs")),
    ]

    o: list[str] = []
    a = o.append

    a(f"""<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">
<style>
  .mono{{font-family:'Fira Code','JetBrains Mono',Consolas,monospace}}
  .twk{{animation:twk 3.2s ease-in-out infinite}}
  @keyframes twk{{0%,100%{{opacity:.15}}50%{{opacity:.9}}}}
  .blob1{{animation:drift1 14s ease-in-out infinite alternate}}
  .blob2{{animation:drift2 18s ease-in-out infinite alternate}}
  @keyframes drift1{{from{{transform:translate(0,0)}}to{{transform:translate(260px,30px)}}}}
  @keyframes drift2{{from{{transform:translate(0,0)}}to{{transform:translate(-300px,-20px)}}}}
  .cursor{{animation:blink 1s steps(1) infinite}}
  @keyframes blink{{50%{{opacity:0}}}}
  .live{{animation:livep 1.6s ease-out infinite;transform-box:fill-box;transform-origin:center}}
  @keyframes livep{{0%{{transform:scale(1);opacity:.8}}100%{{transform:scale(3.2);opacity:0}}}}
  .float{{animation:fl 5s ease-in-out infinite}}
  @keyframes fl{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-2px)}}}}
  @media (prefers-reduced-motion:reduce){{*{{animation:none!important}}}}
</style>
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{BG}"/><stop offset="1" stop-color="#0a1120"/></linearGradient>
  <radialGradient id="b1"><stop offset="0" stop-color="{ACCENT_A}" stop-opacity=".22"/><stop offset="1" stop-color="{ACCENT_A}" stop-opacity="0"/></radialGradient>
  <radialGradient id="b2"><stop offset="0" stop-color="#A855F7" stop-opacity=".18"/><stop offset="1" stop-color="#A855F7" stop-opacity="0"/></radialGradient>
  <pattern id="grid" width="24" height="24" patternUnits="userSpaceOnUse"><path d="M24 0H0V24" fill="none" stroke="{ACCENT_A}" stroke-opacity=".05"/></pattern>
  <linearGradient id="frame" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{ACCENT_A}"/><stop offset=".35" stop-color="{ACCENT_B}"/><stop offset=".7" stop-color="#C4B5FD"/><stop offset="1" stop-color="{ACCENT_A}"/>
    <animate attributeName="x1" values="0;1;0" dur="8s" repeatCount="indefinite"/><animate attributeName="x2" values="1;2;1" dur="8s" repeatCount="indefinite"/>
  </linearGradient>
  <linearGradient id="sweep" x1="0" x2="1"><stop offset="0" stop-color="#7dfaff" stop-opacity="0"/><stop offset=".5" stop-color="#7dfaff" stop-opacity=".10"/><stop offset="1" stop-color="#7dfaff" stop-opacity="0"/></linearGradient>
  <linearGradient id="title" x1="0" x2="1"><stop offset="0" stop-color="{ACCENT_A}"/><stop offset="1" stop-color="{ACCENT_B}"/></linearGradient>
  <filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="2.4" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
  <filter id="softglow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="6"/></filter>
  <clipPath id="frameclip"><rect width="{W}" height="{H}" rx="14"/></clipPath>
  <clipPath id="type"><rect x="28" y="16" width="0" height="28"><animate attributeName="width" from="0" to="420" dur="1.4s" begin="0.1s" fill="freeze" calcMode="spline" keySplines="0.4 0 0.2 1"/></rect></clipPath>""")

    for i, (_, _, _, c, c2, _, _) in enumerate(cards):
        a(f'<linearGradient id="cg{i}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{c}"/><stop offset="1" stop-color="{c2}"/></linearGradient>')
        a(f'<linearGradient id="area{i}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{c}" stop-opacity=".35"/><stop offset="1" stop-color="{c}" stop-opacity="0"/></linearGradient>')
        a(f'<linearGradient id="card{i}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{c}" stop-opacity=".09"/><stop offset=".55" stop-color="{PANEL}" stop-opacity=".92"/><stop offset="1" stop-color="#0b111b" stop-opacity=".96"/></linearGradient>')
    a("</defs>")

    # background: grid, drifting aurora blobs, twinkling stars, periodic scan sweep
    a(f'<g clip-path="url(#frameclip)"><rect width="{W}" height="{H}" fill="url(#bg)"/><rect width="{W}" height="{H}" fill="url(#grid)"/>')
    a('<circle class="blob1" cx="160" cy="60" r="220" fill="url(#b1)"/><circle class="blob2" cx="760" cy="180" r="240" fill="url(#b2)"/>')
    rng = random.Random(7)  # fixed seed -> stable output, no noisy git diffs
    for _ in range(38):
        x, y, r = rng.uniform(6, W - 6), rng.uniform(6, H - 6), rng.choice([.6, .8, 1, 1.2])
        a(f'<circle class="twk" cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="#cfefff" '
          f'style="animation-delay:{rng.uniform(0, 3.2):.2f}s;animation-duration:{rng.uniform(2.4, 4.8):.1f}s"/>')
    a(f'<rect x="-300" y="0" width="300" height="{H}" fill="url(#sweep)"><animate id="sw" attributeName="x" values="-300;{W}" dur="2.2s" begin="0.2s;sw.end+5s"/></rect>')
    a("</g>")

    # outer frame + chasing gradient border
    per = 2 * (W - 2 + H - 2)
    a(f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="14" fill="none" stroke="{BORDER}"/>')
    a(f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="14" fill="none" stroke="url(#frame)" stroke-width="1.6" stroke-dasharray="160 {per-160}" filter="url(#glow)" opacity=".85"><animate attributeName="stroke-dashoffset" from="0" to="-{per}" dur="10s" repeatCount="indefinite"/></rect>')
    a(f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="14" fill="none" stroke="url(#frame)" stroke-width="1.6" stroke-dasharray="80 {per-80}" stroke-dashoffset="-{per//2}" opacity=".5"><animate attributeName="stroke-dashoffset" from="-{per//2}" to="-{per + per//2}" dur="10s" repeatCount="indefinite"/></rect>')

    # header: typewriter title, blinking cursor, LIVE badge
    a('<g class="mono">')
    a('<g clip-path="url(#type)"><text x="30" y="36" font-size="13" fill="#4b6478">'
      f'<tspan fill="{ACCENT_A}" font-weight="700">❯</tspan> <tspan fill="url(#title)" font-weight="700">mission.telemetry</tspan>'
      '<tspan fill="#4b6478"> // live from GitHub API</tspan></text></g>')
    a(f'<rect class="cursor" x="0" y="25" width="7" height="14" fill="{ACCENT_A}" opacity="0"><set attributeName="opacity" to="1" begin="1.5s"/>'
      '<animate attributeName="x" from="30" to="372" dur="1.4s" begin="0.1s" fill="freeze" calcMode="spline" keySplines="0.4 0 0.2 1"/></rect>')
    a(f'<g transform="translate({W-128},31)"><rect x="-12" y="-13" width="110" height="22" rx="11" fill="#0d1a14" stroke="{ACCENT_B}" stroke-opacity=".45"/>'
      f'<circle class="live" cx="0" cy="-2" r="3.5" fill="{ACCENT_B}"/><circle cx="0" cy="-2" r="3.5" fill="{ACCENT_B}" filter="url(#glow)"/>'
      f'<text x="10" y="2" font-size="11" font-weight="700" fill="{ACCENT_B}" letter-spacing="2">LIVE</text>'
      '<text x="48" y="2" font-size="10" fill="#4b6478">sync ✓</text></g>')
    a("</g>")

    for i, (l1, l2, value, c, c2, kind, pts) in enumerate(cards):
        x = 30 + i * (CW + GAP)
        d = 0.15 + i * 0.14
        vals = _count_steps(value)
        goal = next_milestone(value)
        frac = value / goal

        a(f'<g opacity="0"><animate attributeName="opacity" from="0" to="1" dur=".6s" begin="{d:.2f}s" fill="freeze"/>'
          f'<animateTransform attributeName="transform" type="translate" from="0,18" to="0,0" dur=".7s" begin="{d:.2f}s" fill="freeze" calcMode="spline" keySplines="0.16 1 0.3 1"/>')
        a(f'<g class="float" style="animation-delay:{i*0.6:.1f}s">')

        # card body + chasing border + top accent
        a(f'<rect x="{x+20}" y="{CY0+CH-14}" width="{CW-40}" height="14" rx="7" fill="{c}" opacity=".18" filter="url(#softglow)"/>')
        a(f'<rect x="{x}" y="{CY0}" width="{CW}" height="{CH}" rx="12" fill="url(#card{i})" stroke="{BORDER}"/>')
        p = 2 * (CW + CH)
        a(f'<rect x="{x}" y="{CY0}" width="{CW}" height="{CH}" rx="12" fill="none" stroke="url(#cg{i})" stroke-width="1.6" stroke-linecap="round" stroke-dasharray="110 {p-110}" filter="url(#glow)">'
          f'<animate attributeName="stroke-dashoffset" from="{-i*160}" to="{-i*160-p}" dur="{5+i*0.7:.1f}s" repeatCount="indefinite"/></rect>')
        a(f'<rect x="{x+14}" y="{CY0}" width="56" height="2" rx="1" fill="url(#cg{i})" filter="url(#glow)"/>')

        # ring gauge = progress toward next milestone (real, not decorative)
        rcx, rcy, r = x + CW - 38, CY0 + 38, 21
        C = 2 * math.pi * r
        a(f'<circle cx="{rcx}" cy="{rcy}" r="{r}" fill="none" stroke="{BORDER}" stroke-width="4"/>')
        a(f'<circle cx="{rcx}" cy="{rcy}" r="{r}" fill="none" stroke="url(#cg{i})" stroke-width="4" stroke-linecap="round" stroke-dasharray="{C:.1f}" stroke-dashoffset="{C:.1f}" transform="rotate(-90 {rcx} {rcy})" filter="url(#glow)">'
          f'<animate attributeName="stroke-dashoffset" from="{C:.1f}" to="{C*(1-frac):.1f}" dur="1.4s" begin="{d+0.3:.2f}s" fill="freeze" calcMode="spline" keySplines="0.16 1 0.3 1"/></circle>')
        a(f'<circle cx="{rcx}" cy="{rcy}" r="{r+7}" fill="none" stroke="{c}" stroke-opacity=".25" stroke-width="1" stroke-dasharray="2 6">'
          f'<animateTransform attributeName="transform" type="rotate" from="0 {rcx} {rcy}" to="360 {rcx} {rcy}" dur="{14+i*2}s" repeatCount="indefinite"/></circle>')
        a(f'<circle cx="{rcx}" cy="{rcy-r-7}" r="2" fill="{c2}" filter="url(#glow)">'
          f'<animateTransform attributeName="transform" type="rotate" from="0 {rcx} {rcy}" to="-360 {rcx} {rcy}" dur="{6+i}s" repeatCount="indefinite"/></circle>')
        a(_icon(kind, rcx, rcy, c2))
        a(f'<text class="mono" x="{rcx}" y="{rcy+r+20}" font-size="9" fill="#64748b" text-anchor="middle">→ {short(goal)}</text>')

        # count-up number
        a('<g class="mono">')
        t0, step = d + 0.35, 0.11
        for j, v in enumerate(vals):
            b = t0 + j * step
            if j < len(vals) - 1:
                anim = f'<set attributeName="opacity" to="1" begin="{b:.2f}s"/><set attributeName="opacity" to="0" begin="{b+step:.2f}s"/>'
            else:
                anim = (f'<set attributeName="opacity" to="1" begin="{b:.2f}s"/>'
                        f'<animate attributeName="fill" values="#ffffff;{c2};{TEXT_MAIN}" dur=".6s" begin="{b:.2f}s" fill="freeze"/>')
            a(f'<text x="{x+18}" y="{CY0+50}" font-size="30" font-weight="700" fill="{TEXT_MAIN}" opacity="0" letter-spacing="-1">{v}{anim}</text>')
        a(f'<text x="{x+18}" y="{CY0+72}" font-size="12" fill="#cbd5e1">{l1}</text>'
          f'<text x="{x+18}" y="{CY0+87}" font-size="11" fill="#64748b">{l2}</text>')
        a("</g>")

        # sparkline (12 months of real data)
        pts = pts or [0] * 12
        sx0, sy0, sw, sh = x + 18, CY0 + CH - 14, CW - 36, 30
        lo, hi = min(pts), max(pts)
        span = (hi - lo) or 1
        coords = [
            (sx0 + k * sw / (len(pts) - 1), sy0 - 2 - ((v - lo) / span) * (sh - 4) if hi != lo else sy0 - sh / 2)
            for k, v in enumerate(pts)
        ]
        path = "M" + " L".join(f"{px:.1f},{py:.1f}" for px, py in coords)
        L = sum(math.dist(coords[k], coords[k + 1]) for k in range(len(coords) - 1))
        a(f'<path d="{path} L{sx0+sw:.1f},{sy0} L{sx0},{sy0} Z" fill="url(#area{i})" opacity="0"><animate attributeName="opacity" from="0" to="1" dur=".8s" begin="{d+1.0:.2f}s" fill="freeze"/></path>')
        # solid stroke: a gradient on a perfectly flat line (zero-height bbox) renders nothing
        a(f'<path d="{path}" fill="none" stroke="{c}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="{L:.0f}" stroke-dashoffset="{L:.0f}" filter="url(#glow)">'
          f'<animate attributeName="stroke-dashoffset" from="{L:.0f}" to="0" dur="1.2s" begin="{d+0.5:.2f}s" fill="freeze" calcMode="spline" keySplines="0.4 0 0.2 1"/></path>')
        ex, ey = coords[-1]
        a(f'<circle cx="{ex:.1f}" cy="{ey:.1f}" r="2.6" fill="{c2}" opacity="0" filter="url(#glow)"><set attributeName="opacity" to="1" begin="{d+1.6:.2f}s"/></circle>')
        a(f'<circle cx="{ex:.1f}" cy="{ey:.1f}" r="2.6" fill="none" stroke="{c2}" opacity="0">'
          f'<animate attributeName="r" values="2.6;9" dur="1.6s" begin="{d+1.6:.2f}s" repeatCount="indefinite"/>'
          f'<animate attributeName="opacity" values=".9;0" dur="1.6s" begin="{d+1.6:.2f}s" repeatCount="indefinite"/></circle>')
        a(f'<circle r="1.8" fill="#fff" opacity="0"><set attributeName="opacity" to=".9" begin="{d+1.8:.2f}s"/>'
          f'<animateMotion path="{path}" dur="3.2s" begin="{d+1.8:.2f}s" repeatCount="indefinite" calcMode="spline" keyTimes="0;1" keySplines="0.4 0 0.2 1"/></circle>')

        # particle burst when the count-up lands
        tb = t0 + (len(vals) - 1) * step
        for q in range(10):
            ang, dist = q * math.pi / 5 + 0.3, 22 + (q % 3) * 8
            bx, by = x + 40, CY0 + 38
            a(f'<circle cx="{bx}" cy="{by}" r="1.4" fill="{c2}" opacity="0">'
              f'<animate attributeName="cx" from="{bx}" to="{bx + dist*math.cos(ang):.1f}" dur=".8s" begin="{tb:.2f}s" fill="freeze" calcMode="spline" keySplines="0.1 0.8 0.3 1"/>'
              f'<animate attributeName="cy" from="{by}" to="{by + dist*math.sin(ang):.1f}" dur=".8s" begin="{tb:.2f}s" fill="freeze" calcMode="spline" keySplines="0.1 0.8 0.3 1"/>'
              f'<animate attributeName="opacity" values="0;1;0" keyTimes="0;.2;1" dur=".8s" begin="{tb:.2f}s" fill="freeze"/></circle>')

        a("</g></g>")

    a("</svg>")
    return "\n".join(o)


# ---------------------------------------------------------------------------
# Tech stack card renderer
# ---------------------------------------------------------------------------

# Used when config.yml has no `stack:` section. To override, add to config.yml:
#   stack:
#     - name: CLOUD
#       color: "#22D3A5"
#       items: [AWS, Azure, Route53]
DEFAULT_STACK = [
    ("CLOUD", "#22D3A5", ["AWS", "Azure", "Route53", "IAM/OIDC", "Lambda", "ECS Fargate"]),
    ("ORCHESTRATION", "#38BDF8", ["Docker", "Kubernetes", "K3s", "Linkerd", "Helm"]),
    ("CI/CD", "#C4B5FD", ["Jenkins", "GitHub Actions", "ArgoCD", "Git"]),
    ("NETWORKING", "#FBBF24", ["Traefik", "Nginx", "cert-manager", "TCP/IP", "DNS"]),
    ("OBSERVABILITY", "#22D3A5", ["Prometheus", "Grafana", "AlertManager", "Datadog", "ELK"]),
    ("SECURITY", "#F87171", ["HashiCorp Vault", "AWS SSM", "IAM"]),
    ("IaC", "#818CF8", ["Terraform", "Ansible"]),
    ("LANG / DATA", "#38BDF8", ["Python", "JavaScript", "React", "Django", "Flask", "FastAPI",
                                "Bash", "MySQL", "MongoDB", "Redis"]),
    ("LINUX / OS", "#A3E635", ["Linux", "Ubuntu", "systemd", "Bash scripting", "Cron"]),
    ("API TESTING", "#F472B6", ["Postman", "Swagger / OpenAPI", "cURL"]),
]


def _load_stack() -> list[tuple[str, str, list[str]]]:
    cfg = CONFIG.get("stack")
    if not cfg:
        return DEFAULT_STACK
    return [(c["name"], c.get("color", ACCENT_A), list(c.get("items", []))) for c in cfg]


def _mix(hex_color: str, base: str, t: float) -> str:
    """Blend hex_color into base by t (0 = base, 1 = hex_color). Used for dark chip fills."""
    h1, h2 = hex_color.lstrip("#"), base.lstrip("#")
    r = [round(int(h2[i:i+2], 16) * (1 - t) + int(h1[i:i+2], 16) * t) for i in (0, 2, 4)]
    return "#" + "".join(f"{v:02x}" for v in r)


def render_tech_stack() -> str:
    stack = _load_stack()
    W = 900
    CHAR_W = 6.9          # approx. glyph width of an 11.5px monospace font
    PILL_X, PILL_W = 38, 158
    CHIP_X0, CHIP_X1 = PILL_X + PILL_W + 22, W - 28
    CHIP_H, LINE_GAP, ROW_GAP = 24, 6, 12
    TOP = 62

    # ---- layout pass: wrap chips onto as many lines as each row needs ----
    rows = []
    y = TOP
    for name, color, items in stack:
        chips, cx, line = [], CHIP_X0, 0
        for it in items:
            w = len(it) * CHAR_W + 20
            if cx + w > CHIP_X1 and cx > CHIP_X0:
                line += 1
                cx = CHIP_X0
            chips.append((it, cx, y + line * (CHIP_H + LINE_GAP), w))
            cx += w + 7
        row_h = (line + 1) * CHIP_H + line * LINE_GAP
        rows.append((name, color, chips, y, row_h))
        y += row_h + ROW_GAP
    H = int(y + 18)
    total_tools = sum(len(r[2]) for r in rows)

    o: list[str] = []
    a = o.append
    a(f"""<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">
<style>
  .mono{{font-family:'Fira Code','JetBrains Mono',Consolas,monospace}}
  .twk{{animation:twk 3.2s ease-in-out infinite}}
  @keyframes twk{{0%,100%{{opacity:.15}}50%{{opacity:.9}}}}
  .blob1{{animation:drift1 16s ease-in-out infinite alternate}}
  .blob2{{animation:drift2 20s ease-in-out infinite alternate}}
  @keyframes drift1{{from{{transform:translate(0,0)}}to{{transform:translate(240px,{H*0.35:.0f}px)}}}}
  @keyframes drift2{{from{{transform:translate(0,0)}}to{{transform:translate(-280px,-{H*0.3:.0f}px)}}}}
  .cursor{{animation:blink 1s steps(1) infinite}}
  @keyframes blink{{50%{{opacity:0}}}}
  .live{{animation:livep 1.6s ease-out infinite;transform-box:fill-box;transform-origin:center}}
  @keyframes livep{{0%{{transform:scale(1);opacity:.8}}100%{{transform:scale(3.2);opacity:0}}}}
  @media (prefers-reduced-motion:reduce){{*{{animation:none!important}}}}
</style>
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{BG}"/><stop offset="1" stop-color="#0a1120"/></linearGradient>
  <radialGradient id="b1"><stop offset="0" stop-color="{ACCENT_A}" stop-opacity=".18"/><stop offset="1" stop-color="{ACCENT_A}" stop-opacity="0"/></radialGradient>
  <radialGradient id="b2"><stop offset="0" stop-color="#A855F7" stop-opacity=".15"/><stop offset="1" stop-color="#A855F7" stop-opacity="0"/></radialGradient>
  <pattern id="grid" width="24" height="24" patternUnits="userSpaceOnUse"><path d="M24 0H0V24" fill="none" stroke="{ACCENT_A}" stroke-opacity=".045"/></pattern>
  <linearGradient id="frame" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{ACCENT_A}"/><stop offset=".35" stop-color="{ACCENT_B}"/><stop offset=".7" stop-color="#C4B5FD"/><stop offset="1" stop-color="{ACCENT_A}"/>
    <animate attributeName="x1" values="0;1;0" dur="8s" repeatCount="indefinite"/><animate attributeName="x2" values="1;2;1" dur="8s" repeatCount="indefinite"/>
  </linearGradient>
  <linearGradient id="spine" gradientUnits="userSpaceOnUse" x1="0" y1="{TOP}" x2="0" y2="{y - ROW_GAP}">"""
    )
    for k, (_, color, *_rest) in enumerate(rows):
        a(f'<stop offset="{k/max(1,len(rows)-1):.2f}" stop-color="{color}"/>')
    a(f"""</linearGradient>
  <linearGradient id="sweep" x1="0" x2="1"><stop offset="0" stop-color="#7dfaff" stop-opacity="0"/><stop offset=".5" stop-color="#7dfaff" stop-opacity=".09"/><stop offset="1" stop-color="#7dfaff" stop-opacity="0"/></linearGradient>
  <linearGradient id="title" x1="0" x2="1"><stop offset="0" stop-color="{ACCENT_A}"/><stop offset="1" stop-color="{ACCENT_B}"/></linearGradient>
  <filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="2.2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
  <filter id="softglow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="5"/></filter>
  <clipPath id="frameclip"><rect width="{W}" height="{H}" rx="14"/></clipPath>
  <clipPath id="type"><rect x="28" y="16" width="0" height="28"><animate attributeName="width" from="0" to="360" dur="1.1s" begin="0.1s" fill="freeze" calcMode="spline" keySplines="0.4 0 0.2 1"/></rect></clipPath>
</defs>""")

    # background
    a(f'<g clip-path="url(#frameclip)"><rect width="{W}" height="{H}" fill="url(#bg)"/><rect width="{W}" height="{H}" fill="url(#grid)"/>')
    a(f'<circle class="blob1" cx="140" cy="{H*0.25:.0f}" r="240" fill="url(#b1)"/><circle class="blob2" cx="780" cy="{H*0.8:.0f}" r="260" fill="url(#b2)"/>')
    rng = random.Random(11)
    for _ in range(int(W * H / 9000)):
        x, yy, r = rng.uniform(6, W - 6), rng.uniform(6, H - 6), rng.choice([.6, .8, 1, 1.2])
        a(f'<circle class="twk" cx="{x:.0f}" cy="{yy:.0f}" r="{r}" fill="#cfefff" '
          f'style="animation-delay:{rng.uniform(0, 3.2):.2f}s;animation-duration:{rng.uniform(2.4, 4.8):.1f}s"/>')
    a(f'<rect x="-300" y="0" width="300" height="{H}" fill="url(#sweep)"><animate id="tsw" attributeName="x" values="-300;{W}" dur="2.4s" begin="0.2s;tsw.end+6s"/></rect>')
    a("</g>")

    # outer frame + chasing border
    per = 2 * (W - 2 + H - 2)
    a(f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="14" fill="none" stroke="{BORDER}"/>')
    a(f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="14" fill="none" stroke="url(#frame)" stroke-width="1.6" stroke-dasharray="180 {per-180}" filter="url(#glow)" opacity=".85"><animate attributeName="stroke-dashoffset" from="0" to="-{per}" dur="12s" repeatCount="indefinite"/></rect>')
    a(f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="14" fill="none" stroke="url(#frame)" stroke-width="1.6" stroke-dasharray="90 {per-90}" stroke-dashoffset="-{per//2}" opacity=".5"><animate attributeName="stroke-dashoffset" from="-{per//2}" to="-{per + per//2}" dur="12s" repeatCount="indefinite"/></rect>')

    # header
    a('<g class="mono">')
    a('<g clip-path="url(#type)"><text x="30" y="36" font-size="13">'
      f'<tspan fill="{ACCENT_A}" font-weight="700">❯ </tspan><tspan fill="#4b6478">cat </tspan>'
      '<tspan fill="url(#title)" font-weight="700">stack.yaml</tspan><tspan fill="#4b6478"> // toolchain in production</tspan></text></g>')
    a(f'<rect class="cursor" x="0" y="25" width="7" height="14" fill="{ACCENT_A}" opacity="0"><set attributeName="opacity" to="1" begin="1.2s"/>'
      '<animate attributeName="x" from="30" to="383" dur="1.1s" begin="0.1s" fill="freeze" calcMode="spline" keySplines="0.4 0 0.2 1"/></rect>')
    badge = f"{len(rows)} domains · {total_tools} tools"
    bw = len(badge) * 6.7 + 34
    a(f'<g transform="translate({W-28-bw:.0f},18)"><rect width="{bw:.0f}" height="22" rx="11" fill="#0d1a14" stroke="{ACCENT_B}" stroke-opacity=".45"/>'
      f'<circle class="live" cx="13" cy="11" r="3.2" fill="{ACCENT_B}"/><circle cx="13" cy="11" r="3.2" fill="{ACCENT_B}" filter="url(#glow)"/>'
      f'<text x="24" y="15" font-size="10.5" fill="{ACCENT_B}" letter-spacing=".5">{badge}</text></g>')
    a("</g>")

    # spine: gradient rail + data packets flowing down
    sx = 18
    y0, y1 = rows[0][3] + CHIP_H / 2, rows[-1][3] + CHIP_H / 2
    a(f'<line x1="{sx}" y1="{y0}" x2="{sx}" y2="{y0}" stroke="url(#spine)" stroke-width="2" stroke-linecap="round" opacity=".55">'
      f'<animate attributeName="y2" from="{y0}" to="{y1}" dur="1.2s" begin="0.1s" fill="freeze" calcMode="spline" keySplines="0.4 0 0.2 1"/></line>')
    for k, (col, delay) in enumerate([(ACCENT_A, 0), (ACCENT_B, 1.6), ("#C4B5FD", 3.2)]):
        a(f'<circle r="2.6" fill="{col}" filter="url(#glow)" opacity="0">'
          f'<animateMotion path="M{sx},{y0} L{sx},{y1}" dur="4.8s" begin="{1.3+delay:.1f}s" repeatCount="indefinite"/>'
          f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;.08;.9;1" dur="4.8s" begin="{1.3+delay:.1f}s" repeatCount="indefinite"/></circle>')

    # rows
    for ri, (name, color, chips, ry, row_h) in enumerate(rows):
        d = 0.2 + ri * 0.11
        cy = ry + CHIP_H / 2
        fill = _mix(color, BG, 0.16)
        edge = _mix(color, BG, 0.38)

        # spine node + connector + burst
        a(f'<circle cx="{sx}" cy="{cy}" r="9" fill="{color}" opacity="0" filter="url(#softglow)">'
          f'<animate attributeName="opacity" values="0;.6;0" dur=".9s" begin="{d:.2f}s" fill="freeze"/></circle>')
        a(f'<circle cx="{sx}" cy="{cy}" r="3.4" fill="{BG}" stroke="{color}" stroke-width="1.6" opacity="0" filter="url(#glow)">'
          f'<animate attributeName="opacity" from="0" to="1" dur=".3s" begin="{d:.2f}s" fill="freeze"/>'
          f'<animate attributeName="r" values="3.4;4.6;3.4" dur="3.6s" begin="{d+1.5:.2f}s" repeatCount="indefinite"/></circle>')
        a(f'<line x1="{sx+4}" y1="{cy}" x2="{sx+4}" y2="{cy}" stroke="{color}" stroke-width="1.2" stroke-dasharray="2 3" opacity=".7">'
          f'<animate attributeName="x2" from="{sx+4}" to="{PILL_X}" dur=".35s" begin="{d+0.05:.2f}s" fill="freeze"/></line>')
        # packet hopping from spine into the pill, periodically
        a(f'<circle r="1.8" fill="#fff" opacity="0"><animateMotion path="M{sx},{cy} L{PILL_X+6},{cy}" dur=".7s" begin="{d+2:.2f}s;{d+8:.2f}s;{d+14:.2f}s" fill="freeze"/>'
          f'<animate attributeName="opacity" values="0;1;0" dur=".7s" begin="{d+2:.2f}s;{d+8:.2f}s;{d+14:.2f}s" fill="freeze"/></circle>')

        # category pill (slides in)
        a(f'<g opacity="0" class="mono"><animate attributeName="opacity" from="0" to="1" dur=".5s" begin="{d:.2f}s" fill="freeze"/>'
          f'<animateTransform attributeName="transform" type="translate" from="-18,0" to="0,0" dur=".6s" begin="{d:.2f}s" fill="freeze" calcMode="spline" keySplines="0.16 1 0.3 1"/>')
        a(f'<rect x="{PILL_X}" y="{ry}" width="{PILL_W}" height="{CHIP_H}" rx="{CHIP_H/2}" fill="{fill}" stroke="{edge}">'
          f'<animate attributeName="stroke" values="{edge};{color};{edge}" dur="5s" begin="{d+1.2:.2f}s" repeatCount="indefinite"/></rect>')
        a(f'<rect x="{PILL_X}" y="{ry}" width="{PILL_W}" height="{CHIP_H}" rx="{CHIP_H/2}" fill="none" stroke="{color}" stroke-width="1.4" '
          f'stroke-dasharray="40 {2*(PILL_W+CHIP_H)}" filter="url(#glow)" opacity=".8">'
          f'<animate attributeName="stroke-dashoffset" from="0" to="-{2*(PILL_W+CHIP_H)+40}" dur="{4+ri%3:.0f}s" begin="{d:.2f}s" repeatCount="indefinite"/></rect>')
        a(f'<circle cx="{PILL_X+13}" cy="{cy}" r="3" fill="{color}" filter="url(#glow)"/>')
        a(f'<text x="{PILL_X+24}" y="{cy+4}" font-size="11" font-weight="700" fill="{color}" letter-spacing=".6">{html.escape(name)}</text>')
        a(f'<text x="{PILL_X+PILL_W-10}" y="{cy+4}" font-size="10" fill="{color}" opacity=".55" text-anchor="end">{len(chips):02d}</text>')
        a("</g>")

        # tool chips: staggered pop-in, then a shimmer wave sweeping across the whole card
        for ci, (label, cxp, cyp, w) in enumerate(chips):
            cd = d + 0.25 + ci * 0.045
            wave = 3.0 + ri * 0.12 + (cxp - CHIP_X0) / 900
            ccx, ccy = cxp + w / 2, cyp + CHIP_H / 2
            a(f'<g opacity="0" class="mono"><animate attributeName="opacity" from="0" to="1" dur=".35s" begin="{cd:.2f}s" fill="freeze"/>'
              f'<animateTransform attributeName="transform" type="translate" from="0,8" to="0,0" dur=".45s" begin="{cd:.2f}s" fill="freeze" calcMode="spline" keySplines="0.16 1 0.3 1"/>')
            a(f'<rect x="{cxp:.1f}" y="{cyp}" width="{w:.1f}" height="{CHIP_H}" rx="7" fill="#0d1520" fill-opacity=".85" stroke="{BORDER}">'
              f'<animate attributeName="stroke" values="{BORDER};{color};{BORDER};{BORDER}" keyTimes="0;.06;.16;1" dur="7s" begin="{wave:.2f}s" repeatCount="indefinite"/>'
              f'<animate attributeName="fill" values="#0d1520;{fill};#0d1520;#0d1520" keyTimes="0;.06;.16;1" dur="7s" begin="{wave:.2f}s" repeatCount="indefinite"/></rect>')
            a(f'<circle cx="{cxp+9:.1f}" cy="{ccy}" r="1.8" fill="{color}" opacity=".7"/>')
            a(f'<text x="{cxp+15:.1f}" y="{ccy+4}" font-size="11.5" fill="#cbd5e1">{html.escape(label)}'
              f'<animate attributeName="fill" values="#cbd5e1;#ffffff;#cbd5e1;#cbd5e1" keyTimes="0;.06;.16;1" dur="7s" begin="{wave:.2f}s" repeatCount="indefinite"/></text>')
            a("</g>")

    a("</svg>")
    return "\n".join(o)


def render_languages(stats: dict) -> str:
    rows = []
    y = 55
    bar_x = 160
    bar_max_w = 700  # widened since the percentage label column is gone
    for i, (name, pct, color) in enumerate(stats["languages"]):
        bar_w = max(4, bar_max_w * pct / 100)
        delay = i * 0.12  # cascading stagger, one row after another
        rows.append(f"""
        <text x="30" y="{y+13}" font-family="{FONT}" font-size="13" fill="{TEXT_MUTED}">{name}</text>
        <rect x="{bar_x}" y="{y}" width="{bar_max_w}" height="18" rx="4" fill="{PANEL}" stroke="{BORDER}"/>
        <rect x="{bar_x}" y="{y}" width="0" height="18" rx="4" fill="{color}" filter="url(#barGlow)">
          <animate attributeName="width" from="0" to="{bar_w:.2f}" dur="1.1s" begin="{delay:.2f}s" fill="freeze" calcMode="spline" keySplines="0.25 0.1 0.25 1"/>
        </rect>
        """)
        y += 34

    height = y + 25
    return f"""<svg width="900" height="{height}" viewBox="0 0 900 {height}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <filter id="barGlow"><feGaussianBlur stdDeviation="1.5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
  </defs>
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

    with open(os.path.join(OUT_DIR, "tech-stack.svg"), "w", encoding="utf-8") as f:
        f.write(render_tech_stack())

    print("Generated stats-card.svg, languages.svg and tech-stack.svg with live data:")
    print(stats)


if __name__ == "__main__":
    main()
