"""
Probe the structure of noticias/revalida and editais/2026 pages.
"""
import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "pt-BR,pt;q=0.9",
    "Referer": "https://www.gov.br/inep/pt-br",
}

# ============================================================
# NOTICIAS - using the dedicated Revalida news page
# ============================================================
print("=== NOTICIAS REVALIDA PAGE ===")
r = requests.get(
    "https://www.gov.br/inep/pt-br/centrais-de-conteudo/noticias/revalida",
    headers=HEADERS, timeout=20
)
soup = BeautifulSoup(r.text, "html.parser")

# These classes appeared 30x each - that's our news articles
print(f"\n.titulo elements: {len(soup.select('.titulo'))}")
print(f".descricao elements: {len(soup.select('.descricao'))}")
print(f".data elements: {len(soup.select('.data'))}")
print(f".subtitulo-noticia elements: {len(soup.select('.subtitulo-noticia'))}")
print(f".conteudo elements: {len(soup.select('.conteudo'))}")

print("\n--- First 5 news items structure ---")
conteudos = soup.select(".conteudo")
for i, c in enumerate(conteudos[:5]):
    titulo = c.select_one(".titulo")
    desc = c.select_one(".descricao")
    data = c.select_one(".data")
    link = c.select_one("a")
    
    print(f"\nItem {i+1}:")
    print(f"  titulo: {titulo.get_text(strip=True)[:100] if titulo else 'N/A'}")
    print(f"  descricao: {desc.get_text(strip=True)[:120] if desc else 'N/A'}")
    print(f"  data: {data.get_text(strip=True) if data else 'N/A'}")
    print(f"  link: {link.get('href','N/A')[:120] if link else 'N/A'}")

# ============================================================
# EDITAIS - try the /2026 sub-page directly
# ============================================================
print("\n\n=== EDITAIS 2026 DIRECT PAGE ===")
r2 = requests.get(
    "https://www.gov.br/inep/pt-br/centrais-de-conteudo/legislacao/revalida/2026",
    headers={**HEADERS, "Referer": "https://www.gov.br/inep/pt-br/centrais-de-conteudo/legislacao/revalida"},
    timeout=20
)
print(f"Status: {r2.status_code}, Length: {len(r2.text)}")

soup2 = BeautifulSoup(r2.text, "html.parser")
# Try searching for links to in.gov.br or actual documents
print("\nAll content links (non-nav):")
for a in soup2.find_all("a"):
    href = a.get("href", "")
    text = a.get_text(strip=True)
    # Skip nav/social/short texts
    if (href and len(text) > 15 
            and not any(skip in href for skip in ["acesso-a-informacao", "areas-de-atuacao", "composicao", "facebook", "twitter", "whatsapp", "linkedin"])
            and "#" not in href
            and "gov.br/inep/pt-br/search" not in href):
        print(f"  TEXT: {text[:100]}")
        print(f"  HREF: {href[:130]}")
        print()

# Also check for parent-fieldname-text in this sub-page
cc = soup2.select_one("#parent-fieldname-text")
print(f"\n#parent-fieldname-text found in /2026: {cc is not None}")
cc2 = soup2.select_one("#content-core")
if cc2:
    print(f"#content-core content: {str(cc2)[:1000]}")
