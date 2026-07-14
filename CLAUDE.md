# CLAUDE.md — alfie.com

Read this first. It's the full brief for this project so any new session starts oriented.

## What this is
Personal website for **Dr. Alfie Meek**, economist. It replaces his old WordPress site at
`alfie.com`. The site is a polished "front door": a live **at-a-glance economic dashboard**
plus a **bio**, that routes visitors to his other properties. Static HTML/CSS — no build
step, no framework.

## Hosting & deploy
- **GitHub Pages**, **public** repo named `alfie`, served at the **apex domain `alfie.com`**.
- `CNAME` file (contains `alfie.com`) is already in the repo.
- After push: repo **Settings → Pages → Deploy from a branch → `main` / root**, then
  **Enforce HTTPS**.
- **DNS** (at registrar): four A records on `@` → `185.199.108.153`, `185.199.109.153`,
  `185.199.110.153`, `185.199.111.153`; plus `www` CNAME → `alfie.com`. Full steps in `README.md`.
- Remove old WordPress DNS records first.

## Design system (keep every page consistent)
"Instrument panel" aesthetic. All shared styling lives in **`style.css`** (CSS variables) —
new pages must link it and reuse its components rather than restyling.
- **Palette:** deep ink (`--ink #131C28`) + **brass** accent (`--brass #C69749`); bone text;
  green/red (`--pos`/`--neg`) reserved strictly for data direction, never decoration.
- **Type:** `Newsreader` (display serif) + `IBM Plex Sans` (body) + `IBM Plex Mono` (data/labels).
- Every page: masthead + nav, footer with the personal-site disclaimer, responsive to mobile,
  respects `prefers-reduced-motion`.

## The dashboard data (index.html)
- Numbers live in the `DATA` object at the **bottom of `index.html`**, fetched from
  **BLS, the Federal Reserve, and U.S. Census** (snapshot dated 2026-07-14).
- **Not yet auto-updating.** To make it live, replace `DATA` with a fetch to **FRED**
  (Alfie's own API key) or wire it to his **economicsguru.com** pipeline. Each indicator keeps
  the same shape, so nothing else changes.
- The **Inflation (CPI)** tile is intentionally left in the "connect your feed" state as the
  first one to wire up.
- Sourcing notes: the free **BLS API** has a low daily quota (shared/unregistered); **Alpha
  Vantage** demo endpoints cover fed funds / 10-yr Treasury / retail sales without a key.

## Alfie's properties (link targets — use these exact domains)
- **Weekly Economic Update** (Substack): `https://www.alfiemeek.com`  ← must include `www.`
- **Charts:** `https://economicsguru.com` (hundreds of auto-updated charts)
- **Georgia data:** `https://georgiaeconomics.com`
- **Economic Impact Group** (consulting): `https://economicimpact.com`
- **LOCI™** (software): `https://loci.online`
- **Georgia Input-Output Model** (new): `https://economicimpact.io`

## Bio facts (authoritative — do NOT invent or embellish)
- **30 years** of experience (Alfie's instruction: use "30 years", not "25+").
- Director, **Center for Economic Development Research (CEDR)**, Georgia Tech.
- President & CEO, **Economic Impact Group, LLC**; creator of **LOCI™**.
- Former **Chief Economist & Director of Economic Analysis, Gwinnett County, GA**.
- Earlier: Director of Applied Research, UGA Business Outreach/SBDC; Research Economist, SunTrust.
- Focus: fiscal/economic impact analysis, forecasting & modeling, tax policy, target industry.
  Recent work: fiscal impact of investment tax credits across many states; legislative testimony.
- Research on the U.S. **sports industry** published in *Sport Marketing Quarterly*; cited in
  USA Today, Georgia Trend, Financial Times (London), Fortune, Investor's Business Daily; 200+
  academic citations.
- Degrees: **Ph.D. Agricultural Economics (UGA)**, **M.S. Business Economics (Georgia State)**,
  **B.S. Economics (Georgia Tech)**.
- Footer disclaimer is required: personal site, not affiliated with any organization, opinions
  are his own.

## Headshot
- Real photo at **`assets/headshot.jpg`** (square, 1200px). `assets/headshot-placeholder.svg`
  is the automatic fallback if the jpg is missing.
- Bio page portrait uses a 4:5 `cover` crop; author band uses a circular crop. If the bio crop
  ever feels too tight, switch that portrait to a 1:1 frame to show the full photo.

## Status
**Done:** `index.html` (dashboard + author band), `bio.html`, `style.css`,
`assets/headshot.jpg`, `CNAME`, `README.md`, `.gitignore`.

**To do (same style, then deploy):**
- Build **LOCI**, **Research**, and **Contact** pages; add them to the nav.
- Wire the dashboard to a live data source (FRED key or economicsguru pipeline); start with CPI.
- Optional: native **Substack subscribe embed** + auto-listing recent posts from the
  `www.alfiemeek.com` RSS feed in the "This week's read" panel.
- Then `git` push and point DNS.

## Working preferences
- Don't fabricate bio details, figures, or affiliations.
- Keep copy plain and specific; light formatting.
- Reuse `style.css`; keep the six property links pointing at the exact domains above.
