"""
Scraper for INEP Revalida-specific news.
Source: https://www.gov.br/inep/pt-br/centrais-de-conteudo/noticias/revalida

Key finding from debugging:
- This page is 100% dedicated to Revalida news — NO AI filter needed!
- Structure: .conteudo > .titulo (+ link), .descricao, .data
- This replaces the main page scraper which couldn't find content (JS-rendered)

Logic: Any new article URL = alert. No AI processing needed.
State: data/last_seen.json -> "noticias" list of known article URLs.
"""
import json
import os
import sys
from pathlib import Path

import requests
from bs4 import BeautifulSoup

sys.path.insert(0, str(Path(__file__).parent))
from cards import card_noticia
from http_client import build_session
from notifier import send_card

# Dedicated Revalida news page — server-rendered, no JS
TARGET_URL = "https://www.gov.br/inep/pt-br/centrais-de-conteudo/noticias/revalida"
STATE_FILE = Path(__file__).parent.parent / "data" / "last_seen.json"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "pt-BR,pt;q=0.9",
    "Referer": "https://www.gov.br/inep/pt-br",
}

INEP_BASE = "https://www.gov.br"


def load_state() -> dict:
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    return {"editais": [], "noticias": []}


def save_state(state: dict) -> None:
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def scrape_news_items() -> list[dict]:
    """
    Fetches the Revalida news listing page and returns structured news items.
    Confirmed structure: .conteudo container with .titulo (a), .descricao, .data
    """
    session = build_session()
    try:
        response = session.get(TARGET_URL, headers=HEADERS, timeout=20)
        response.raise_for_status()
    except requests.RequestException as exc:
        print(f"[Noticias] Fetch failed after retries: {exc}. Skipping this run.")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    items = []

    for article in soup.select(".conteudo"):
        # Title + link: the .titulo element or any anchor within
        titulo_el = article.select_one(".titulo")
        if not titulo_el:
            continue

        link_el = titulo_el.find("a") or article.find("a")
        if not link_el:
            continue

        title = titulo_el.get_text(strip=True)
        href = link_el.get("href", "").strip()
        if not href:
            continue
        if not href.startswith("http"):
            href = INEP_BASE + href

        desc_el = article.select_one(".descricao, .subtitulo-noticia")
        summary = desc_el.get_text(strip=True) if desc_el else ""

        data_el = article.select_one(".data")
        date_str = data_el.get_text(strip=True) if data_el else ""

        items.append({
            "title": title,
            "summary": summary,
            "url": href,
            "date": date_str,
            "category": "REVALIDA",
        })

    print(f"[Noticias] Found {len(items)} articles on page.")
    return items


def run() -> None:
    webhook_url = os.environ.get("TEAMS_WEBHOOK_URL")
    if not webhook_url:
        print("[Noticias] ERROR: TEAMS_WEBHOOK_URL not set.")
        sys.exit(1)

    state = load_state()
    seen = set(state.get("noticias", []))
    new_count = 0

    items = scrape_news_items()

    for item in items:
        if item["url"] in seen:
            continue

        print(f"[Noticias] NEW: {item['title'][:70]}")
        card = card_noticia.build(
            title=item["title"],
            summary=item["summary"],
            url=item["url"],
            category=item.get("category", "REVALIDA"),
        )
        success = send_card(webhook_url, card)

        if success:
            seen.add(item["url"])
            new_count += 1
        else:
            print(f"[Noticias] Failed to send card for: {item['title']}")

    state["noticias"] = list(seen)
    save_state(state)
    print(f"[Noticias] Done. {new_count} new article(s) sent.")


if __name__ == "__main__":
    run()
