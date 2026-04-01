"""
Probe the real AJAX endpoints discovered in the HTML.
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
    "Accept-Language": "pt-BR,pt;q=0.9",
    "Referer": "https://www.gov.br/inep/pt-br/centrais-de-conteudo/legislacao/revalida",
}

# Test the direct year URL for editais
print("=== PROBE: Direct 2026 tab URL ===")
url_2026 = "https://www.gov.br/inep/pt-br/centrais-de-conteudo/legislacao/revalida/2026"
r = requests.get(url_2026, headers=HEADERS, timeout=20)
print(f"Status: {r.status_code}")
print(f"Content-Type: {r.headers.get('content-type', '-')}")
print(f"Content length: {len(r.text)}")
print("\nFirst 2000 chars of response:")
print(r.text[:2000])

soup = BeautifulSoup(r.text, "html.parser")
print("\n=== All links found ===")
for a in soup.find_all("a"):
    href = a.get("href", "")
    text = a.get_text(strip=True)
    if href and text and len(text) > 5:
        print(f"  TEXT: {text[:100]}")
        print(f"  HREF: {href[:120]}")
        print()

# Now test the noticias/revalida page  (discovered as a link!)
print("\n\n=== PROBE: Noticias Revalida page ===")
url_noticias = "https://www.gov.br/inep/pt-br/centrais-de-conteudo/noticias/revalida"
r2 = requests.get(url_noticias, headers=HEADERS, timeout=20)
print(f"Status: {r2.status_code}")
print(f"Content length: {len(r2.text)}")

soup2 = BeautifulSoup(r2.text, "html.parser")
print("\n=== Links on noticias/revalida ===")
links_found = []
for a in soup2.find_all("a"):
    href = a.get("href", "")
    text = a.get_text(strip=True)
    # Filter nav links, look for news article links
    if (href and text and len(text) > 10
            and "revalida" in href.lower()
            and "perguntas" not in href
            and "acesso-a-informacao" not in href
            and "#" not in href):
        links_found.append((text, href))
        
for text, href in links_found[:20]:
    print(f"  TEXT: {text[:100]}")
    print(f"  HREF: {href[:120]}")
    print()

print(f"Total relevant links found: {len(links_found)}")

# Print top CSS classes for noticias page
from collections import Counter
all_classes = []
for el in soup2.find_all(class_=True):
    all_classes.extend(el.get("class", []))
top = Counter(all_classes).most_common(20)
print("\nTop CSS classes on noticias/revalida:")
for cls, count in top:
    print(f"  .{cls}: {count}x")
