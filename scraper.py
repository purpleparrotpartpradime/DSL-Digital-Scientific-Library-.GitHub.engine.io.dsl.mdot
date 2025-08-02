# scraper.py
import requests, os
from bs4 import BeautifulSoup

keywords = ['physics', 'biology', 'climate', 'ecology']
base_folder = "scraped"

os.makedirs(base_folder, exist_ok=True)

for word in keywords:
    print(f"Scraping: {word}")
    try:
        url = f"https://en.wikipedia.org/wiki/{word.capitalize()}"
        r = requests.get(url)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, "html.parser")
            paragraphs = soup.select("p")
            text = "\n".join(p.get_text() for p in paragraphs[:5])

            folder = os.path.join(base_folder, word)
            os.makedirs(folder, exist_ok=True)

            with open(os.path.join(folder, "summary.txt"), "w", encoding="utf-8") as f:
                f.write(text)
    except Exception as e:
        print(f"Failed to scrape {word}: {e}")
