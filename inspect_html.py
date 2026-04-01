from bs4 import BeautifulSoup

with open("debug_editais.html", encoding="utf-8") as f:
    soup = BeautifulSoup(f.read(), "html.parser")

# Check content-core
cc = soup.select_one("#content-core")
if cc:
    print("=== #content-core (first 3000 chars) ===")
    print(str(cc)[:3000])
else:
    print("No #content-core found")

# external-link anchors
print("\n=== All external-link anchors ===")
for a in soup.select("a.external-link")[:20]:
    print("TEXT:", a.get_text(strip=True)[:100])
    print("HREF:", a.get("href", "")[:120])
    print()

# Check in.gov.br links
print("=== All in.gov.br links ===")
for a in soup.find_all("a"):
    href = a.get("href", "")
    if "in.gov.br" in href:
        print("TEXT:", a.get_text(strip=True)[:100])
        print("HREF:", href[:120])
        print()

# Check noticias page
with open("debug_noticias.html", encoding="utf-8") as f:
    soup2 = BeautifulSoup(f.read(), "html.parser")

# Look at tile elements
print("\n=== .tile elements (first 5) ===")
for i, tile in enumerate(soup2.select(".tile")[:5]):
    print(f"--- TILE {i+1} ---")
    print(str(tile)[:500])
    print()

# cover-banner-tile
print("=== .cover-banner-tile (first 3) ===")
for i, tile in enumerate(soup2.select(".cover-banner-tile")[:3]):
    print(f"--- BANNER {i+1} ---")
    title = tile.select_one(".titulo, h2, h3, strong")
    link = tile.select_one("a")
    desc = tile.select_one("p, .texto")
    print("title:", title.get_text(strip=True)[:100] if title else "N/A")
    print("link:", link.get("href", "N/A")[:100] if link else "N/A")
    print("desc:", desc.get_text(strip=True)[:100] if desc else "N/A")
    print()

# swiper-slide
print("=== .swiper-slide (first 5) ===")
for i, sl in enumerate(soup2.select(".swiper-slide")[:5]):
    print(f"--- SLIDE {i+1} ---")
    print(str(sl)[:400])
    print()
