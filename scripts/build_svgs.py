"""Generates the SVG cards used by README.md.

Edit the content below and run:  python scripts/build_svgs.py
"""
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parent.parent / "assets"
FONT = "'Segoe UI', Inter, -apple-system, BlinkMacSystemFont, Helvetica, Arial, sans-serif"
MONO = "'JetBrains Mono', 'Cascadia Code', Consolas, Menlo, monospace"

BG1, BG2 = "#0b1020", "#121a33"
BORDER = "#26304d"
TEXT = "#e8ecf6"
MUTED = "#8e9ab8"
ACCENT = "#9d8cff"   # soft .NET violet
ACCENT2 = "#5ec8ff"

STACK = ["C#", "ASP.NET Core", "EF Core", "PostgreSQL", "SQL Server",
         "Redis", "Elasticsearch", "TypeScript", "Next.js", "Docker"]

WORK = [
    # slug, title, meta, role, body lines
    ("dtarsiv", "DTArşiv", "Demirören News Agency", "KARTEGA · BACKEND",
     ["Media asset management. Ingest",
      "pipeline for RSS feeds and reporter",
      "uploads, Elasticsearch search and",
      "Azure AD sign-in."]),
    ("laviya", "Laviya", "laviya.app", "KARTEGA · FULL-STACK",
     ["Multi-tenant project and task",
      "management SaaS with AI orchestration",
      "(OpenAI, Gemini) and iyzico",
      "subscriptions."]),
    ("pendigit", "Pendigit", "pendigit.com", "KARTEGA · FULL-STACK",
     ["Super app with live channels, VOD,",
      "social feed and ads. .NET 8 backend",
      "features and Next.js admin panels."]),
    ("lumos", "Lumos Danışmanlık", "lumosdanismanlik.com", "FREELANCE · SOLE DEVELOPER",
     ["Platform for a counseling center: online booking,",
      "iyzico payments, video sessions and automated",
      "email/SMS reminders. Live in production."]),
    ("foxper", "Foxper Studios", "foxperstudios.com", "FREELANCE",
     ["Our freelance studio in İzmir. We build custom",
      "software for companies and individuals, along",
      "with our own mobile apps and games."]),
]


def t(s: str) -> str:
    return escape(s)


def frame(w: int, h: int, body: str, inset: int = 8, label: str = "") -> str:
    iw, ih = w - 2 * inset, h - 2 * inset
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{t(label)}">
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="{BG1}"/><stop offset="1" stop-color="{BG2}"/>
  </linearGradient>
  <linearGradient id="ac" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{ACCENT}"/><stop offset="1" stop-color="{ACCENT2}"/>
  </linearGradient>
</defs>
<rect x="{inset}" y="{inset}" width="{iw}" height="{ih}" rx="18" fill="url(#bg)" stroke="{BORDER}"/>
{body}
</svg>
"""


def header() -> str:
    w, h = 1200, 410
    chips, x, y = [], 56, 330
    for s in STACK:
        cw = int(len(s) * 8.6 + 26)
        if x + cw > w - 56:
            x, y = 56, y + 46
        chips.append(
            f'<rect x="{x}" y="{y}" width="{cw}" height="34" rx="17" fill="#18213d" stroke="{BORDER}"/>'
            f'<text x="{x + cw / 2}" y="{y + 22.5}" text-anchor="middle" font-family="{MONO}" font-size="14" fill="{TEXT}">{t(s)}</text>')
        x += cw + 10
    body = f"""
<text x="56" y="68" font-family="{FONT}" font-size="14" letter-spacing="3" fill="{MUTED}">COMPUTER ENGINEER</text>
<text x="1144" y="68" text-anchor="end" font-family="{FONT}" font-size="14" letter-spacing="3" fill="{MUTED}">İZMİR, TÜRKİYE</text>
<text x="52" y="160" font-family="{FONT}" font-size="78" font-weight="700" fill="{TEXT}">Yusuf Burak Peker<tspan fill="{ACCENT}">.</tspan></text>
<text x="56" y="210" font-family="{FONT}" font-size="26" fill="{TEXT}">Backend-focused, .NET first.</text>
<text x="56" y="244" font-family="{FONT}" font-size="26" fill="url(#ac)">Building the systems behind real products.</text>
<text x="1144" y="196" text-anchor="end" font-family="{FONT}" font-size="17" fill="{TEXT}">Backend Developer at <tspan font-weight="700">Kartega Yazılım</tspan></text>
<text x="1144" y="222" text-anchor="end" font-family="{FONT}" font-size="15" fill="{MUTED}">Multi-tenant SaaS and enterprise platforms;</text>
<text x="1144" y="244" text-anchor="end" font-family="{FONT}" font-size="15" fill="{MUTED}">lately Next.js frontends with AI-assisted development.</text>
<line x1="56" y1="282" x2="1144" y2="282" stroke="{BORDER}"/>
<text x="56" y="312" font-family="{FONT}" font-size="13" letter-spacing="3" fill="{MUTED}">WHAT I WORK WITH</text>
{''.join(chips)}
"""
    return frame(w, h, body, label="Yusuf Burak Peker, Backend Developer (.NET) at Kartega Yazılım, İzmir")


def section(title: str, right: str = "") -> str:
    w, h = 1200, 70
    body = f"""
<text x="56" y="44" font-family="{FONT}" font-size="13" letter-spacing="3" fill="{MUTED}">{t(title)}</text>
<line x1="{70 + len(title) * 11.5}" y1="40" x2="{1144 - len(right) * 8.5 - (14 if right else 0)}" y2="40" stroke="{BORDER}"/>
<text x="1144" y="44" text-anchor="end" font-family="{FONT}" font-size="13" fill="{MUTED}">{t(right)}</text>
"""
    return frame(w, h, body, inset=0, label=title).replace(
        '<rect x="0" y="0" width="1200" height="70" rx="18" fill="url(#bg)" stroke="#26304d"/>', "")


def card(w: int, title: str, meta: str, role: str, lines: list[str]) -> str:
    h = 280
    body_lines = "".join(
        f'<text x="40" y="{172 + i * 25}" font-family="{FONT}" font-size="17" fill="{MUTED}">{t(l)}</text>'
        for i, l in enumerate(lines))
    body = f"""
<rect x="40" y="8" width="64" height="4" rx="2" fill="url(#ac)"/>
<text x="40" y="58" font-family="{FONT}" font-size="12" letter-spacing="2.5" fill="{ACCENT}">{t(role)}</text>
<text x="40" y="100" font-family="{FONT}" font-size="30" font-weight="700" fill="{TEXT}">{t(title)}</text>
<text x="40" y="128" font-family="{FONT}" font-size="15" fill="{MUTED}">{t(meta)}</text>
<text x="{w - 40}" y="100" text-anchor="end" font-family="{FONT}" font-size="22" fill="{MUTED}">↗</text>
{body_lines}
"""
    return frame(w, h, body, label=f"{title} – {meta}")


def award() -> str:
    w, h = 1200, 76
    body = f"""
<text x="40" y="44" font-family="{FONT}" font-size="12" letter-spacing="2.5" fill="{ACCENT}">AWARD</text>
<text x="112" y="44" font-family="{FONT}" font-size="15" fill="{TEXT}">1st place, Mercedes-Benz Otomotiv StarHack'21 <tspan fill="{MUTED}">· CarGoo, a crowdsourced cargo delivery system</tspan></text>
<text x="1160" y="44" text-anchor="end" font-family="{FONT}" font-size="16" fill="{MUTED}">↗</text>
"""
    return frame(w, h, body, label="Award: 1st place at Mercedes-Benz StarHack'21 with CarGoo")


def button(label: str, sub: str, primary: bool = False) -> str:
    w, h = 400, 110
    fill = "url(#ac)" if primary else "#18213d"
    color = BG1 if primary else TEXT
    subc = "#1c2440" if primary else MUTED
    body = f"""
<rect x="20" y="20" width="{w - 40}" height="{h - 40}" rx="35" fill="{fill}" stroke="{BORDER if not primary else 'none'}"/>
<text x="{w / 2}" y="54" text-anchor="middle" font-family="{FONT}" font-size="20" font-weight="700" fill="{color}">{t(label)}</text>
<text x="{w / 2}" y="76" text-anchor="middle" font-family="{FONT}" font-size="13" fill="{subc}">{t(sub)}</text>
"""
    svg = frame(w, h, body, label=label)
    # buttons sit on the page background, no outer card
    return svg.replace(f'<rect x="8" y="8" width="{w - 16}" height="{h - 16}" rx="18" fill="url(#bg)" stroke="{BORDER}"/>', "")


def main() -> None:
    OUT.mkdir(exist_ok=True)
    files = {
        "header.svg": header(),
        "section-work.svg": section("SELECTED WORK", "more on pkryusuf.tech"),
        "award.svg": award(),
        "contact-email.svg": button("Email", "pekeryusufburak@gmail.com", primary=True),
        "contact-linkedin.svg": button("LinkedIn", "in/pkryusuf"),
        "contact-site.svg": button("Portfolio", "pkryusuf.tech"),
    }
    for i, (slug, title, meta, role, lines) in enumerate(WORK):
        files[f"work-{slug}.svg"] = card(400 if i < 3 else 600, title, meta, role, lines)
    for name, svg in files.items():
        (OUT / name).write_text(svg, encoding="utf-8")
        print("wrote", name)


if __name__ == "__main__":
    main()
