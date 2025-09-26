import requests, json, time
from bs4 import BeautifulSoup

BASE_URL = "https://www.chinesedrama.info"
LIST_URL = f"{BASE_URL}/p/drama-list.html"

response = requests.get(LIST_URL)
soup = BeautifulSoup(response.text, "html.parser")

dramas = []
for a in soup.select("div.main-post-body a"):
    title = a.text.strip()
    href = a.get("href")
    if title and href and "chinesedrama.info" in href:
        dramas.append({"title": title, "link": href})

print(f"Found {len(dramas)} dramas, fetching details...")

detailed = []
for i, d in enumerate(dramas[:30]):  # limit for now
    try:
        r = requests.get(d["link"])
        page = BeautifulSoup(r.text, "html.parser")
        img_tag = page.select_one("div#post-body img")
        poster = img_tag["src"] if img_tag else None
        p_tag = page.select_one("div#post-body p")
        summary = p_tag.get_text(strip=True) if p_tag else None

        detailed.append({
            "title": d["title"],
            "link": d["link"],
            "poster": poster,
            "summary": summary
        })

        print(f"✔ {i+1}. {d['title']}")
        time.sleep(1)
    except Exception as e:
        print(f"⚠ Error {d['title']}: {e}")

with open("dramas.json", "w", encoding="utf-8") as f:
    json.dump(detailed, f, ensure_ascii=False, indent=2)

print(f"✅ Saved {len(detailed)} dramas to dramas.json")
