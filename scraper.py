
import os
import json
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote

# URLs
BASE_URL = "https://www.chinesedrama.info"
LIST_URL = f"{BASE_URL}/p/drama-list.html"

# Load existing dramas.json if it exists
if os.path.exists("dramas.json"):
    with open("dramas.json", "r", encoding="utf-8") as f:
        existing_dramas = json.load(f)
else:
    existing_dramas = []

existing_links = {d['link'] for d in existing_dramas}

# Fetch drama list page
response = requests.get(LIST_URL)
soup = BeautifulSoup(response.text, "html.parser")

# Extract drama links
new_dramas = []
for a in soup.select("div.main-post-body a"):
    title = a.text.strip()
    href = a.get("href")
    if title and href and "chinesedrama.info" in href and "/p/" not in href:
        if href not in existing_links:
            new_dramas.append({"title": title, "link": href})

print(f"Found {len(new_dramas)} new dramas.")

# Fetch details for new dramas
for i, drama in enumerate(new_dramas):
    try:
        r = requests.get(drama["link"])
        page = BeautifulSoup(r.text, "html.parser")
        content_div = page.select_one("div.main-post-body")
        poster = None
       

        if content_div:
            # Poster inside div#dw_data
            dw_data_div = content_div.select_one("div#dw_data")
            if dw_data_div:
                img_tag = dw_data_div.find("img")
                if img_tag and img_tag.get("src"):
                    # encode URL properly
                    poster = quote(img_tag["src"], safe=":/?=&")

           

        drama.update({"poster": poster})
        existing_dramas.append(drama)
        print(f"✔ Added: {drama['title']}")
        time.sleep(1)
    except Exception as e:
        print(f"⚠ Error with {drama['title']}: {e}")

# Save updated dramas.json
with open("dramas.json", "w", encoding="utf-8") as f:
    json.dump(existing_dramas, f, ensure_ascii=False, indent=2)

print(f"🎬 Updated dramas.json with {len(new_dramas)} new dramas.")
