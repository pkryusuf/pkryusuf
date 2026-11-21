"""Builds assets/activity.svg from the GitHub contribution calendar.

Runs daily in .github/workflows/activity.yml. Locally:
    GITHUB_TOKEN=$(gh auth token) python scripts/build_activity.py
"""
import json
import os
import sys
import urllib.request
from collections import defaultdict
from datetime import date, datetime, timezone

sys.path.insert(0, os.path.dirname(__file__))
from build_svgs import FONT, MUTED, OUT, TEXT, frame  # noqa: E402

# Contributions from every account listed here are added together.
ACCOUNTS = ["pkryusuf", "pkryusuf-kartega"]

QUERY = """query($login: String!) {
  user(login: $login) {
    contributionsCollection {
      contributionCalendar { weeks { contributionDays { date contributionCount } } }
    }
  }
}"""

LEVELS = ["#161d33", "#2e2a6b", "#4b3fae", "#7c6cf2", "#b5a9ff"]


def fetch(login: str, token: str) -> list[list[tuple[str, int]]]:
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": login}}).encode(),
        headers={"Authorization": f"bearer {token}", "User-Agent": "profile-readme-activity"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.load(r)
    if "errors" in data:
        raise SystemExit(data["errors"])
    weeks = data["data"]["user"]["contributionsCollection"]["contributionCalendar"]["weeks"]
    return [[(d["date"], d["contributionCount"]) for d in w["contributionDays"]] for w in weeks]


def level(count: int, cuts: list[int]) -> int:
    if count == 0:
        return 0
    return 1 + sum(count > c for c in cuts)


def build(weeks: list[list[tuple[str, int]]], counts: dict[str, int]) -> str:
    w, h = 1200, 360
    total = sum(counts.values())
    nonzero = sorted(c for c in counts.values() if c)
    cuts = [nonzero[int(len(nonzero) * q)] for q in (0.25, 0.5, 0.75)] if nonzero else [0, 0, 0]

    cell, gap = 16, 4
    gx = (w - len(weeks) * (cell + gap) + gap) / 2
    gy = 150
    rects, months, last_month = [], [], None
    for wi, week in enumerate(weeks):
        x = gx + wi * (cell + gap)
        first = date.fromisoformat(week[0][0])
        if first.month != last_month and wi < len(weeks) - 2:
            if last_month is not None or first.day <= 7:
                months.append(f'<text x="{x}" y="{gy - 12}" font-family="{FONT}" font-size="12" fill="{MUTED}">{first.strftime("%b")}</text>')
            last_month = first.month
        for d, _ in week:
            wd = (date.fromisoformat(d).weekday() + 1) % 7  # Sunday first, like GitHub
            c = counts[d]
            rects.append(f'<rect x="{x}" y="{gy + wd * (cell + gap)}" width="{cell}" height="{cell}" rx="3" '
                         f'fill="{LEVELS[level(c, cuts)]}"><title>{d}: {c}</title></rect>')

    legend_x = w - 56 - 5 * 20 - 70
    legend = "".join(f'<rect x="{legend_x + 40 + i * 20}" y="{h - 52}" width="14" height="14" rx="3" fill="{c}"/>'
                     for i, c in enumerate(LEVELS))
    updated = datetime.now(timezone.utc).strftime("%d %b %Y · %H:%M UTC")
    body = f"""
<text x="56" y="62" font-family="{FONT}" font-size="13" letter-spacing="3" fill="{MUTED}">GITHUB ACTIVITY</text>
<text x="1144" y="62" text-anchor="end" font-family="{FONT}" font-size="13" fill="{MUTED}">Updated {updated}</text>
<text x="56" y="108" font-family="{FONT}" font-size="40" font-weight="700" fill="{TEXT}">{total:,}<tspan font-size="18" font-weight="400" fill="{MUTED}" dx="12">contributions in the last year</tspan></text>
{''.join(months)}
{''.join(rects)}
<text x="56" y="{h - 40}" font-family="{FONT}" font-size="12" fill="{MUTED}">Personal + work accounts combined. Most of my work is in private repositories.</text>
<text x="{legend_x}" y="{h - 40}" font-family="{FONT}" font-size="12" fill="{MUTED}">Less</text>
{legend}
<text x="{legend_x + 40 + 5 * 20 + 4}" y="{h - 40}" font-family="{FONT}" font-size="12" fill="{MUTED}">More</text>
"""
    return frame(w, h, body, label=f"{total} GitHub contributions in the last year")


def main() -> None:
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        raise SystemExit("GITHUB_TOKEN is not set")
    counts: dict[str, int] = defaultdict(int)
    weeks = None
    for login in ACCOUNTS:
        wk = fetch(login, token)
        weeks = weeks or wk
        for week in wk:
            for d, c in week:
                counts[d] += c
    OUT.mkdir(exist_ok=True)
    (OUT / "activity.svg").write_text(build(weeks, counts), encoding="utf-8")
    print("wrote activity.svg,", sum(counts.values()), "contributions")


if __name__ == "__main__":
    main()
