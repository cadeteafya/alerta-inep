import sys
sys.path.insert(0, "src")

# Test editais
from scraper_editais import scrape_editais
docs = scrape_editais()
print(f"Editais found: {len(docs)}")
for d in docs[:5]:
    print(f"  - {d['title'][:80]}")

print()

# Test noticias
from scraper_noticias import scrape_news_items
news = scrape_news_items()
print(f"Noticias found: {len(news)}")
for n in news[:5]:
    print(f"  [{n.get('date','')}] {n['title'][:80]}")
    print(f"    URL: {n['url'][:90]}")
