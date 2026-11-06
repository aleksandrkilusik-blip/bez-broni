#!/usr/bin/env python3
"""Оновлює блок «Нові випуски на YouTube» на головній (UA та EN).

Читає публічну RSS-стрічку плейлиста подкасту (ключ YouTube не потрібен),
пропускає Shorts, бере 3 найновіші відео й переписує HTML між маркерами
<!-- YT:START --> і <!-- YT:END --> у index.html та en/index.html.

Запуск:  python3 scripts/update_episodes.py
Тест на локальній стрічці:  python3 scripts/update_episodes.py --feed-file feed.xml
"""
import argparse
import html
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path

PLAYLIST_ID = "PLF7PYvFUKJXKWFEcvs6UVisVNEZm91Sbm"
FEED_URL = f"https://www.youtube.com/feeds/videos.xml?playlist_id={PLAYLIST_ID}"
COUNT = 3
ROOT = Path(__file__).resolve().parent.parent

NS = {
    "atom": "http://www.w3.org/2005/Atom",
    "yt": "http://www.youtube.com/xml/schemas/2015",
    "media": "http://search.yahoo.com/mrss/",
}

MONTHS_UK = ["січня", "лютого", "березня", "квітня", "травня", "червня",
             "липня", "серпня", "вересня", "жовтня", "листопада", "грудня"]
MONTHS_EN = ["January", "February", "March", "April", "May", "June", "July",
             "August", "September", "October", "November", "December"]

PAGES = {
    "uk": {
        "file": ROOT / "index.html",
        "date": lambda d: f"{d.day} {MONTHS_UK[d.month - 1]} {d.year}",
        "more": "Дивитися на YouTube →",
        "title_lang": "",
    },
    "en": {
        "file": ROOT / "en" / "index.html",
        "date": lambda d: f"{MONTHS_EN[d.month - 1]} {d.day}, {d.year}",
        "more": "Watch on YouTube →",
        "title_lang": ' lang="uk"',  # назви відео українською
    },
}

BLOCK_RE = re.compile(r"(<!-- YT:START[^>]*-->\n)(.*?)(^[ \t]*<!-- YT:END -->)", re.S | re.M)


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (bez-broni site updater)"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()


def is_short(video_id, link, online=True):
    if "/shorts/" in link:
        return True
    if not online:
        return False
    # Стрічка плейлиста дає звичайні посилання watch?v=, тому перевіряємо:
    # для Shorts адреса /shorts/ID відповідає 200, для звичайних відео — редірект.
    try:
        req = urllib.request.Request(f"https://www.youtube.com/shorts/{video_id}", method="HEAD",
                                     headers={"User-Agent": "Mozilla/5.0"})
        opener = urllib.request.build_opener(NoRedirect)
        with opener.open(req, timeout=15) as r:
            return r.status == 200
    except Exception:
        return False


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None


def parse(xml_bytes, check_shorts=True):
    root = ET.fromstring(xml_bytes)
    videos = []
    for e in root.findall("atom:entry", NS):
        vid = e.findtext("yt:videoId", default="", namespaces=NS).strip()
        title = e.findtext("atom:title", default="", namespaces=NS).strip()
        published = e.findtext("atom:published", default="", namespaces=NS).strip()
        link_el = e.find("atom:link[@rel='alternate']", NS)
        link = link_el.get("href") if link_el is not None else f"https://www.youtube.com/watch?v={vid}"
        thumb_el = e.find("media:group/media:thumbnail", NS)
        thumb = thumb_el.get("url") if thumb_el is not None else f"https://i.ytimg.com/vi/{vid}/hqdefault.jpg"
        if not (vid and title and published):
            continue
        videos.append({
            "id": vid, "title": title, "link": link, "thumb": thumb,
            "date": datetime.fromisoformat(published.replace("Z", "+00:00")),
        })
    videos.sort(key=lambda v: v["date"], reverse=True)
    result = []
    for v in videos:
        if is_short(v["id"], v["link"], online=check_shorts):
            continue
        result.append(v)
        if len(result) == COUNT:
            break
    return result


def render(videos, lang):
    p = PAGES[lang]
    out = []
    for v in videos:
        d = v["date"]
        out.append(
            '<article class="card">\n'
            f'  <a class="card-link" href="https://www.youtube.com/watch?v={html.escape(v["id"])}">\n'
            f'    <img class="card-thumb" src="{html.escape(v["thumb"])}" width="480" height="270" alt="" loading="lazy">\n'
            f'    <span class="card-meta"><time datetime="{d:%Y-%m-%d}">{p["date"](d)}</time></span>\n'
            f'    <h3{p["title_lang"]}>{html.escape(v["title"], quote=False)}</h3>\n'
            f'    <span class="more">{p["more"]}</span>\n'
            '  </a>\n'
            '</article>\n'
        )
    return "".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--feed-file", help="локальний XML замість завантаження (для тесту)")
    args = ap.parse_args()

    try:
        data = Path(args.feed_file).read_bytes() if args.feed_file else fetch(FEED_URL)
        videos = parse(data, check_shorts=not args.feed_file)
    except Exception as exc:
        # YouTube інколи тимчасово віддає помилку — сайт не чіпаємо, спробуємо наступного разу.
        print(f"::warning::Не вдалося прочитати стрічку YouTube: {exc}")
        return 0
    if not videos:
        print("::warning::У стрічці немає відео — сайт не змінено.")
        return 0

    changed = False
    for lang, p in PAGES.items():
        text = p["file"].read_text(encoding="utf-8")
        m = BLOCK_RE.search(text)
        if not m:
            print(f"::error::У {p['file'].name} ({lang}) немає маркерів <!-- YT:START --> / <!-- YT:END -->")
            return 1
        new = text[:m.start(2)] + render(videos, lang) + text[m.end(2):]
        if new != text:
            p["file"].write_text(new, encoding="utf-8")
            changed = True
            print(f"Оновлено: {p['file'].relative_to(ROOT)}")
    if not changed:
        print("Нових відео немає — сайт без змін.")
    for v in videos:
        print(f"  {v['date']:%Y-%m-%d}  {v['title']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
