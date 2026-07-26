#!/usr/bin/env python3
"""
Refresh the "This week's read" post list on alfie.com from the Substack RSS feed.

Substack blocks cross-origin browser requests, so the list cannot be fetched from
the visitor's browser. This runs server-side in GitHub Actions, writes the three
newest posts straight into index.html (and into posts.json), and commits the result.
The list is therefore plain static HTML: it works with JavaScript off and is visible
to search engines.

Safe by design: if the feed is unreachable or returns fewer than three usable posts,
the script exits without touching anything, leaving the last good list in place.
"""

import json
import pathlib
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime

FEED = "https://www.alfiemeek.com/feed"
ROOT = pathlib.Path(__file__).resolve().parent.parent
INDEX = ROOT / "index.html"
POSTS_JSON = ROOT / "posts.json"
COUNT = 3
SUBTITLE_MAX = 150

MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def fetch_feed(url: str) -> bytes:
    req = urllib.request.Request(
        url, headers={"User-Agent": "alfie.com post-list updater (GitHub Actions)"}
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()


def strip_tags(s: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", s or "")).strip()


def esc(s: str) -> str:
    return (s.replace("&", "&amp;").replace("<", "&lt;")
             .replace(">", "&gt;").replace('"', "&quot;"))


def parse(raw: bytes):
    channel = ET.fromstring(raw).find("channel")
    posts = []
    for item in channel.findall("item"):
        title = strip_tags(item.findtext("title") or "")
        link = (item.findtext("link") or "").strip()
        if not title or not link:
            continue
        subtitle = strip_tags(item.findtext("description") or "")
        if len(subtitle) > SUBTITLE_MAX:
            subtitle = subtitle[:SUBTITLE_MAX].rsplit(" ", 1)[0].rstrip(",.;:") + "…"
        try:
            dt = parsedate_to_datetime(item.findtext("pubDate"))
            date_label = f"{MONTHS[dt.month - 1]} {dt.day}"
            iso = dt.date().isoformat()
        except Exception:
            date_label, iso = "·", ""
        posts.append({"title": title, "url": link,
                      "subtitle": subtitle, "date": iso, "label": date_label})
        if len(posts) == COUNT:
            break
    return posts


def render(posts) -> str:
    rows = []
    for i, p in enumerate(posts):
        label = "newest" if i == 0 else p["label"]
        sub = f'<span>{esc(p["subtitle"])}</span>' if p["subtitle"] else ""
        rows.append(
            f'        <a class="post" href="{esc(p["url"])}" target="_blank" '
            f'rel="noopener"><span class="p-date">{esc(label)}</span>'
            f'<span class="p-title">{esc(p["title"])}{sub}</span></a>'
        )
    return '<div id="posts">\n' + "\n".join(rows) + "\n      </div>"


def main() -> int:
    try:
        posts = parse(fetch_feed(FEED))
    except Exception as e:
        print(f"Feed unavailable ({e}) — leaving the existing list untouched.")
        return 0

    if len(posts) < COUNT:
        print(f"Only {len(posts)} usable posts in the feed — leaving the list untouched.")
        return 0

    html = INDEX.read_text(encoding="utf-8")
    block = re.compile(r'<div id="posts">.*?</div>', re.S)
    if not block.search(html):
        print('ERROR: could not find the <div id="posts"> block in index.html.')
        return 1

    updated = block.sub(lambda _: render(posts), html, count=1)
    POSTS_JSON.write_text(json.dumps(posts, indent=2) + "\n", encoding="utf-8")

    if updated == html:
        print("Already current — no change.")
        return 0

    INDEX.write_text(updated, encoding="utf-8")
    print("Updated to:")
    for p in posts:
        print(f"  {p['date']}  {p['title'][:70]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
