import json
import os
import time
import requests
import urllib.parse

# Agar URL mein # hai to short mat karo (player ke liye zaroori hai)
def has_hash_fragment(url):
    return '#' in url

# NORMAL LINKS (Player/Download) — #wale ko chhod do
def shorten_normal(url):
    if not url or not url.strip():
        return url
    if not url.startswith("http"):
        url = "https://" + url.strip()

    # Agar # hai (jaise #khamhf) to bilkul short mat karo — original rakho
    if has_hash_fragment(url):
        print(f"   Hash link detected → RAKHA WAISA HI (player safe): {url}")
        return url

    shorteners = [
        ("is.gd",   lambda u: f"https://is.gd/create.php?format=simple&url={u}"),
        ("v.gd",    lambda u: f"https://v.gd/create.php?format=simple&url={u}"),
        ("cutt.ly", lambda u: ("https://cutt.ly/api/api.php", {"url": u})),
        ("t.ly",    lambda u: f"https://t.ly/api/v1/link/shorten?link={u}"),
        ("rb.gy",   lambda u: f"https://rb.gy/api/shorten?url={u}"),
        ("TinyURL", lambda u: f"https://tinyurl.com/api-create.php?url={u}"),  # Last
    ]

    for name, cfg in shorteners:
        try:
            if isinstance(cfg, tuple):
                r = requests.post(cfg[0], data=cfg[1](url), timeout=10)
                if r.status_code == 200:
                    res = r.json()
                    if res.get("url", {}).get("status") == 1:
                        short = res["url"]["shortLink"]
                        print(f"   Shortened via {name} → {short}")
                        return short
            else:
                r = requests.get(cfg(url), timeout=10)
                if r.status_code == 200:
                    short = r.text.strip()
                    if short.startswith("http") and len(short) < len(url):
                        print(f"   Shortened via {name} → {short}")
                        return short
        except:
            continue
    print("   Normal link: Sab fail → original rakha")
    return url


# SCREENSHOT SPECIAL (catbox.moe 100% support)
def shorten_screenshot(url):
    if not url or not url.strip():
        return url
    if not url.startswith("http"):
        url = "https://" + url.strip()

    shorteners = [
        ("cutt.ly", lambda u: ("https://cutt.ly/api/api.php", {"url": u})),
        ("t.ly",    lambda u: f"https://t.ly/api/v1/link/shorten?link={u}"),
        ("rb.gy",   lambda u: f"https://rb.gy/api/shorten?url={u}"),
        ("chilp.it",lambda u: f"http://chilp.it/api.php?url={u}"),
        ("TinyURL", lambda u: f"https://tinyurl.com/api-create.php?url={u}"),
    ]

    for name, cfg in shorteners:
        try:
            if isinstance(cfg, tuple):
                r = requests.post(cfg[0], data=cfg[1](url), timeout=10)
                if r.status_code == 200:
                    res = r.json()
                    if res.get("url", {}).get("status") == 1:
                        short = res["url"]["shortLink"]
                        print(f"   Screenshot → {name}: {short}")
                        return short
            else:
                r = requests.get(cfg(url), timeout=10)
                if r.status_code == 200:
                    short = r.text.strip()
                    if short.startswith("http"):
                        print(f"   Screenshot → {name}: {short}")
                        return short
        except:
            continue
    return url


DATA_FILE = 'data/movies.json'

def get_new_movie_data():
    print("\n" + "="*80)
    print("     VEGAHUB MOVIE ADDER → #wale links SAFE + is.gd + catbox fixed")
    print("="*80)

    title   = input("\n1. Title: ").strip()
    tmdb_id = input("2. TMDB ID: ").strip()
    imdb_id = input("3. IMDb ID: ").strip()

    cat_options = ["bollywood", "hollywood", "south", "web", "adult", "netflix"]
    print(f"4. Category: {', '.join(cat_options)}")
    cat = input("   → ").lower()
    while cat not in cat_options:
        cat = input("   Invalid! Choose again: ").lower()

    quality = input("5. Quality: ").strip()
    thumb   = input("6. Thumbnail URL (optional): ").strip()
    year    = input(f"7. Year (default {time.strftime('%Y')}): ").strip() or str(time.strftime("%Y"))

    # SERVERS
    servers = []
    print("\n--- Stream Servers ---")
    while True:
        name = input("Server Name (or 'done'): ").strip()
        if name.lower() == 'done': break
        link = input(f"   {name} URL: ").strip()
        if link:
            print("   Processing link...")
            short = shorten_normal(link)
            servers.append({"name": name, "link": short})
            print(f"   Saved: {short}\n")

    # DOWNLOADS
    downloads = {}
    print("--- Download Links ---")
    i = 1
    while True:
        label = input(f"Label {i} (or 'done'): ").strip()
        if label.lower() == 'done': break
        link = input(f"   URL {i}: ").strip()
        if link:
            print("   Processing download link...")
            short = shorten_normal(link)
            downloads[f"q{i}"] = {"label": label, "link": short}
            print(f"   Saved: {short}\n")
            i += 1

    # SCREENSHOTS
    screenshots = []
    print("--- Screenshots (catbox.moe fully supported) ---")
    i = 1
    while True:
        ss = input(f"Screenshot {i} URL (or 'done'): ").strip()
        if ss.lower() == 'done': break
        if ss:
            print("   Shortening screenshot...")
            short_ss = shorten_screenshot(ss)
            screenshots.append(short_ss)
            print(f"   Saved: {short_ss}\n")
            i += 1

    return {
        "title": title, "tmdb_id": tmdb_id, "imdb_id": imdb_id,
        "thumb": thumb, "cat": cat, "quality": quality, "year": year,
        "servers": servers, "downloads": downloads, "screenshots": screenshots
    }

def update_json_file(movie):
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    movie_list = []
    if os.path.exists(DATA_FILE) and os.path.getsize(DATA_FILE) > 0:
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                movie_list = json.load(f)
        except:
            print("Old JSON corrupt → naya bana rahe hain...")

    movie_list.insert(0, movie)
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(movie_list, f, indent=2, ensure_ascii=False)

    print(f"\nSUCCESS: '{movie['title']}' successfully added!")
    print("   → #khamhf, #anything wale links bilkul waise ke waise rahe")
    print("   → Baaki links is.gd/cutt.ly se short hue")
    print("   → Player 100% direct chalega, zero issue!")

if __name__ == "__main__":
    movie = get_new_movie_data()
    update_json_file(movie)
    print("\nGit Commands:")
    print("   git add .")
    print(f"   git commit -m \"Added: {movie['title']} (#safe + auto short)\"")
    print("   git push origin main")
    print("\nAb tu jitni bhi movie add karega — sab perfect chalega bhai!")