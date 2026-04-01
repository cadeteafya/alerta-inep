"""
Diagnostic script - fetches both INEP pages and prints the raw HTML structure.
Run locally to debug selector issues.
Usage: python diagnose.py
"""
import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "pt-BR,pt;q=0.9,en;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Referer": "https://www.gov.br/",
}

def diagnose_editais():
    url = "https://www.gov.br/inep/pt-br/centrais-de-conteudo/legislacao/revalida"
    print(f"\n{'='*60}")
    print(f"DIAGNOSE: {url}")
    print('='*60)

    r = requests.get(url, headers=HEADERS, timeout=30)
    print(f"Status: {r.status_code}")
    print(f"Content-Type: {r.headers.get('content-type', '-')}")

    soup = BeautifulSoup(r.text, "html.parser")

    # Check for the known selector
    container = soup.select_one("#parent-fieldname-text")
    print(f"\n#parent-fieldname-text found: {container is not None}")

    # Show ALL ids in the page
    ids = [el.get("id") for el in soup.find_all(id=True)]
    print(f"\nAll IDs on page ({len(ids)} found):")
    for id_ in ids[:30]:
        print(f"  #{id_}")

    # Look for ANY links that contain "revalida" in href or text
    print("\nLinks containing 'revalida' or 'edital' or 'portaria':")
    for a in soup.find_all("a"):
        href = a.get("href", "")
        text = a.get_text(strip=True)
        if any(kw in (href + text).lower() for kw in ["revalida", "edital", "portaria", "in.gov.br"]):
            print(f"  TEXT: {text[:80]}")
            print(f"  HREF: {href[:100]}")
            print()

    # Save raw HTML for inspection
    with open("debug_editais.html", "w", encoding="utf-8") as f:
        f.write(r.text)
    print("\n[Saved raw HTML to debug_editais.html]")


def diagnose_noticias():
    url = "https://www.gov.br/inep/pt-br"
    print(f"\n{'='*60}")
    print(f"DIAGNOSE: {url}")
    print('='*60)

    r = requests.get(url, headers=HEADERS, timeout=30)
    print(f"Status: {r.status_code}")

    soup = BeautifulSoup(r.text, "html.parser")

    # Try all candidate selectors
    selectors = [
        ".tileItem", ".summary", "article.tileItem",
        ".tile-item", ".listing-item", ".news-item",
        ".portletItem", ".searchResults dt",
        "article", ".card", ".item",
    ]
    print("\nSelector probe:")
    for sel in selectors:
        found = soup.select(sel)
        print(f"  {sel}: {len(found)} elements")

    # Show ALL class names that appear 3+ times (likely content containers)
    from collections import Counter
    all_classes = []
    for el in soup.find_all(class_=True):
        all_classes.extend(el.get("class", []))
    top = Counter(all_classes).most_common(30)
    print("\nTop 30 CSS classes by frequency:")
    for cls, count in top:
        print(f"  .{cls}: {count}x")

    # Save raw HTML
    with open("debug_noticias.html", "w", encoding="utf-8") as f:
        f.write(r.text)
    print("\n[Saved raw HTML to debug_noticias.html]")


if __name__ == "__main__":
    diagnose_editais()
    diagnose_noticias()
