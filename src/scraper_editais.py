"""
Scraper for INEP Revalida official documents page.
Source: https://www.gov.br/inep/pt-br/centrais-de-conteudo/legislacao/revalida

Logic: DETERMINISTIC — any new link in 2026 is a new document. No AI needed.
State: data/last_seen.json → "editais" list of known hrefs.
"""
import json
import os
import sys
from pathlib import Path

import requests
from bs4 import BeautifulSoup

sys.path.insert(0, str(Path(__file__).parent))
from cards import card_edital
from notifier import send_card

TARGET_URL = "https://www.gov.br/inep/pt-br/centrais-de-conteudo/legislacao/revalida"
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


def scrape_editais() -> list[dict]:
    """Returns list of {'title': str, 'url': str} for all links on the page."""
    response = requests.get(TARGET_URL, headers=HEADERS, timeout=20)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    container = soup.select_one("#parent-fieldname-text")
    if not container:
        print("[Editais] Warning: content container not found.")
        return []

    items = []
    for link in container.select("ul li a"):
        href = link.get("href", "").strip()
        title = link.get_text(strip=True)
        if href and title:
            items.append({"title": title, "url": href})

    print(f"[Editais] Found {len(items)} documents on page.")
    return items


def run() -> None:
    webhook_url = os.environ.get("TEAMS_WEBHOOK_URL")
    if not webhook_url:
        print("[Editais] ERROR: TEAMS_WEBHOOK_URL not set.")
        sys.exit(1)

    state = load_state()
    seen = set(state.get("editais", []))
    new_count = 0

    documents = scrape_editais()
    for doc in documents:
        if doc["url"] in seen:
            continue

        print(f"[Editais] NEW: {doc['title']}")
        card = card_edital.build(title=doc["title"], dou_url=doc["url"])
        success = send_card(webhook_url, card)

        if success:
            seen.add(doc["url"])
            new_count += 1
        else:
            print(f"[Editais] Failed to send card for: {doc['title']}")

    state["editais"] = list(seen)
    save_state(state)
    print(f"[Editais] Done. {new_count} new document(s) sent.")


if __name__ == "__main__":
    run()
