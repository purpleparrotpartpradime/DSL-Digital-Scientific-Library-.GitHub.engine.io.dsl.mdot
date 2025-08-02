import os
import requests
from bs4 import BeautifulSoup

keywords_path = 'config/keywords.txt'
output_dir = '.'  # root of the repo

def safe_filename(name):
    return "".join(c if c.isalnum() or c in "-_ " else "_" for c in name)

def search_and_save(keyword):
    folder = os.path.join(output_dir, safe_filename(keyword))
    os.makedirs(folder, exist_ok=True)

    url = f"https://www.google.com/search?q={keyword.replace(' ', '+')}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    results = soup.find_all('h3')

    with open(os.path.join(folder, 'summary.txt'), 'w', encoding='utf-8') as f:
        f.write(f"Results for: {keyword}\n\n")
        for h3 in results:
            text = h3.get_text(strip=True)
            if text:
                f.write(f"- {text}\n")

def main():
    if not os.path.exists(keywords_path):
        print("No keywords.txt found.")
        return
    with open(keywords_path, 'r') as f:
        keywords = [line.strip() for line in f if line.strip()]
    for kw in keywords:
        search_and_save(kw)

if __name__ == "__main__":
    main()
