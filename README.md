# alfie.com

Personal site for Alfie Meek, Ph.D. — a live "at-a-glance" read on the U.S. economy,
plus bio and links to the full toolkit (Weekly Update, Economics Guru, Georgia Economics,
Economic Impact Group, LOCI™, and the Georgia Input-Output Model).

Static HTML/CSS — no build step, no framework.

## Files

```
alfie/
├── index.html                    Dashboard (homepage) — key indicators, author band, links
├── bio.html                      Full biography page
├── style.css                     Shared styles for every page
├── assets/
│   ├── headshot.jpg              ← YOU ADD THIS (see below)
│   └── headshot-placeholder.svg  Shown until headshot.jpg exists
├── CNAME                          Custom-domain file for GitHub Pages (alfie.com)
└── README.md
```

## Add your headshot

Drop a file named exactly `headshot.jpg` into the `assets/` folder. Both the dashboard
author band and the bio page pick it up automatically — no code change needed. Until then,
a monogram placeholder shows. (Recommended: 800px+ on the short side, fairly clean/simple
background so it sits well on the dark theme. A `.png` works too — just rename the two
`src="assets/headshot.jpg"` references to `.png`.)

## Deploy on GitHub Pages

1. Create a repo named `alfie` and push these files to the `main` branch.
2. In the repo: **Settings → Pages**. Set **Source** to `Deploy from a branch`,
   branch `main`, folder `/ (root)`. Save.
3. Under **Custom domain**, enter `alfie.com` and Save. (The included `CNAME` file
   already sets this; GitHub will verify it.)
4. Wait for the check to pass, then tick **Enforce HTTPS**.

## DNS (apex domain: alfie.com)

At your registrar, create **four A records** on the apex (`@`) pointing to GitHub Pages:

```
@   A   185.199.108.153
@   A   185.199.109.153
@   A   185.199.110.153
@   A   185.199.111.153
```

Add a **CNAME** for `www` so the www variant redirects to the apex:

```
www   CNAME   alfie.com
```

Optional IPv6 (recommended alongside the A records, not instead of them):

```
@   AAAA   2606:50c0:8000::153
@   AAAA   2606:50c0:8001::153
@   AAAA   2606:50c0:8002::153
@   AAAA   2606:50c0:8003::153
```

Notes:
- Remove any old records from the previous (WordPress) host first — especially a
  conflicting apex A record or forwarding rule.
- With the custom domain set to the apex, GitHub auto-redirects `www.alfie.com` → `alfie.com`
  and issues the HTTPS certificate for both.
- DNS can take up to ~24 hours to propagate (usually much faster).

## Live data note

The dashboard's numbers live in the `DATA` object at the bottom of `index.html`
(fetched from BLS, the Federal Reserve, and U.S. Census). To make the page self-updating,
replace that object with a fetch to FRED (with your API key) or wire it to the existing
economicsguru.com pipeline. Every indicator keeps the same shape, so nothing else changes.
The Inflation (CPI) tile is intentionally left in the "connect your feed" state as the
first one to wire up.
