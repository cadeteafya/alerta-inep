"""
Scraper for INEP main page news items.
Source: https://www.gov.br/inep/pt-br

Logic: Scrapes second carousel + news cards below.
       Uses Gemini AI to filter only Revalida-relevant content.
State: data/last_seen.json → "noticias" list of known article URLs.
"""
import json
import os
import sys
from pathlib import Path

import requests
from bs4 import BeautifulSoup

sys.path.insert(0, str(Path(__file__).parent))
from ai_filter import check_relevance
from cards import card_noticia
from notifier import send_card

TARGET_URL = "https://www.gov.br/inep/pt-br"
STATE_FILE = Path(__file__).parent.parent / "data" / "last_seen.json"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept-Language": "pt-BR,pt;q=0.9",
    "Referer": "https://www.gov.br/",
}


def load_state() -> dict:
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    return {"editais": [], "noticias": []}


def save_state(state: dict) -> None:
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def scrape_news_items(soup: BeautifulSoup) -> list[dict]:
    """
    Extracts news cards from the INEP main page.
    Returns list of {'title', 'summary', 'url', 'category'}.
    """
    items = []

    # --- News cards grid (below carousels) ---
    # The INEP page uses .tileItem or equivalent structures
    for card in soup.select(".tileItem, .summary, article.tileItem"):
        title_el = card.select_one(".tileHeadline a, h2 a, h3 a")
        summary_el = card.select_one(".tileBody p, .description, p")
        category_el = card.select_one(
            ".category-name, .listing-categories a, .visualClear + span"
        )

        if not title_el:
            continue

        title = title_el.get_text(strip=True)
        url = title_el.get("href", "").strip()
        summary = summary_el.get_text(strip=True) if summary_el else ""
        category = category_el.get_text(strip=True) if category_el else "INEP"

        if url and title:
            if not url.startswith("http"):
                url = "https://www.gov.br" + url
            items.append(
                {"title": title, "summary": summary, "url": url, "category": category}
            )

    # --- Second carousel (INEP-specific banners) ---
    # Fallback: try to catch highlighted items from the banner area
    for banner in soup.select(".banner-item, .slide-item, .carousel-item"):
        title_el = banner.select_one("h2, h3, .banner-title, strong")
        link_el = banner.find("a")
        desc_el = banner.select_one("p, .banner-description")

        if not title_el or not link_el:
            continue

        title = title_el.get_text(strip=True)
        url = link_el.get("href", "").strip()
        summary = desc_el.get_text(strip=True) if desc_el else ""

        if url and title and url not in [i["url"] for i in items]:
            if not url.startswith("http"):
                url = "https://www.gov.br" + url
            items.append(
                {"title": title, "summary": summary, "url": url, "category": "DESTAQUE"}
            )

    print(f"[Noticias] Found {len(items)} candidate items on page.")
    return items


def run() -> None:
    webhook_url = os.environ.get("TEAMS_WEBHOOK_URL")
    gemini_key = os.environ.get("GEMINI_API_KEY")

    if not webhook_url:
        print("[Noticias] ERROR: TEAMS_WEBHOOK_URL not set.")
        sys.exit(1)
    if not gemini_key:
        print("[Noticias] ERROR: GEMINI_API_KEY not set.")
        sys.exit(1)

    state = load_state()
    seen = set(state.get("noticias", []))
    new_count = 0

    try:
        response = requests.get(TARGET_URL, headers=HEADERS, timeout=20)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"[Noticias] Failed to fetch page: {e}")
        sys.exit(1)

    soup = BeautifulSoup(response.text, "html.parser")
    candidates = scrape_news_items(soup)

    for item in candidates:
        if item["url"] in seen:
            continue

        print(f"[Noticias] Checking with AI: {item['title'][:60]}...")
        result = check_relevance(
            title=item["title"],
            summary=item["summary"],
            api_key=gemini_key,
        )

        if not result.get("is_relevant"):
            print(f"[Noticias] Skipped (not relevant): {result.get('reason', '-')}")
            # Still mark as seen to avoid re-checking next run
            seen.add(item["url"])
            continue

        print(f"[Noticias] RELEVANT — sending: {item['title']}")
        card = card_noticia.build(
            title=item["title"],
            summary=item["summary"],
            url=item["url"],
            category=item.get("category", "INEP · REVALIDA"),
        )
        success = send_card(webhook_url, card)

        if success:
            seen.add(item["url"])
            new_count += 1
        else:
            print(f"[Noticias] Failed to send card for: {item['title']}")

    state["noticias"] = list(seen)
    save_state(state)
    print(f"[Noticias] Done. {new_count} relevant item(s) sent.")


if __name__ == "__main__":
    run()
