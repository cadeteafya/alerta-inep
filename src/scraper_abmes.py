"""
Scraper for ABMES INEP Editais.
Source: http://www.abmes.org.br/busca/resultado?pesquisar=EDITAL+INEP

Logic: 
- Scrapes the search results for EDITAL INEP.
- Finds posts with "EDITAL INEP" or "RETIFICAÇÃO" in the title.
- Only sends alerts for posts whose URLs are NOT in last_seen.json["abmes"].
- This inherently handles multiple posts on the same day without sending duplicate historical data.
"""
import json
import os
import sys
from pathlib import Path

import requests
from bs4 import BeautifulSoup

sys.path.insert(0, str(Path(__file__).parent))
from cards import card_abmes
from notifier import send_card

TARGET_URL = "http://www.abmes.org.br/busca/resultado?pesquisar=EDITAL+INEP"
STATE_FILE = Path(__file__).parent.parent / "data" / "last_seen.json"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "pt-BR,pt;q=0.9",
}

BASE_URL = "http://www.abmes.org.br"

def load_state() -> dict:
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    return {"editais": [], "noticias": [], "abmes": []}


def save_state(state: dict) -> None:
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def scrape_abmes() -> list[dict]:
    """
    Fetches the ABMES search page and returns structured edital items.
    """
    response = requests.get(TARGET_URL, headers=HEADERS, timeout=20)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    items = []

    # Iterating over the result containers
    for container in soup.select(".lista"):
        title_el = container.select_one("h2 a, h3 a, h4 a, h5 a")
        if not title_el:
            continue
            
        title = title_el.get_text(strip=True).upper()
        
        # Filter for EDITAL INEP or RETIFICAÇÃO
        if "EDITAL INEP" not in title and "RETIFICAÇÃO" not in title:
            continue

        href = title_el.get("href", "").strip()
        if not href:
            continue
        if not href.startswith("http"):
            href = BASE_URL + href

        download_url = None
        # Try to find the "Baixar arquivo" link
        download_a = container.find("a", string=lambda text: text and "Baixar arquivo" in text)
        if download_a:
            down_href = download_a.get("href", "").strip()
            if down_href:
                download_url = down_href if down_href.startswith("http") else BASE_URL + down_href

        # Extract summary text
        summary = ""
        parent_h = title_el.parent
        if parent_h:
            next_div = parent_h.find_next_sibling("div")
            if next_div and "Baixar arquivo" not in next_div.get_text():
                summary = next_div.get_text(strip=True)

        items.append({
            "title": title,
            "url": href,
            "download_url": download_url,
            "summary": summary
        })

    print(f"[ABMES] Found {len(items)} matching documents on page.")
    return items


def run() -> None:
    webhook_url = os.environ.get("TEAMS_WEBHOOK_URL")
    if not webhook_url:
        print("[ABMES] ERROR: TEAMS_WEBHOOK_URL not set.")
        sys.exit(1)

    state = load_state()
    # Initialize 'abmes' key if not present
    if "abmes" not in state:
        state["abmes"] = []
        
    seen = set(state.get("abmes", []))
    new_count = 0

    try:
        documents = scrape_abmes()
    except requests.RequestException as e:
        print(f"[ABMES] Failed to fetch page: {e}")
        sys.exit(1)

    # Note: To avoid sending 10+ historical items on the very first run,
    # we might want to populate last_seen manually, but the logic requires 
    # sending what is not seen. Since it's a new feature, the first run will 
    # send all current items on the first page to Teams, establishing the baseline.
    
    for doc in documents:
        if doc["url"] in seen:
            continue

        print(f"[ABMES] NEW: {doc['title']}")
        card = card_abmes.build(
            title=doc["title"], 
            post_url=doc["url"], 
            download_url=doc["download_url"],
            summary=doc.get("summary", "")
        )
        success = send_card(webhook_url, card)

        if success:
            seen.add(doc["url"])
            new_count += 1
        else:
            print(f"[ABMES] Failed to send card for: {doc['title']}")

    state["abmes"] = list(seen)
    save_state(state)
    print(f"[ABMES] Done. {new_count} new document(s) sent.")


if __name__ == "__main__":
    run()
