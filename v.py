import json
import os
import time

# सुनिश्चित करें कि यह पथ सही है: आपके GitHub Repo की रूट से 'data/' फ़ोल्डर में।
DATA_FILE = 'data/movies.json'
VALID_CATEGORIES = ["bollywood", "hollywood", "south", "web"]

def get_input_validated(prompt, validation_list=None):
    """एक मान्य इनपुट प्राप्त करने के लिए प्रॉम्प्ट करता है।"""
    while True:
        value = input(prompt).strip()
        if not value:
            print("âš ï¸ यह फ़ील्ड खाली नहीं छोड़ा जा सकता।")
            continue
        if validation_list and value.lower() not in validation_list:
            print(f"âš ï¸ अमान्य इनपुट। कृपया इनमें से चुनें: {', '.join(validation_list)}")
            continue
        return value

def get_new_movie_data():
    """यूज़र से सभी आवश्यक मूवी डिटेल्स प्रॉम्प्ट करता है।"""
    print("\n\n--- âš¡ï¸ Starting New Movie Entry ---")
    
    # 1. मुख्य डिटेल्स (Validation के साथ)
    title = get_input_validated("1. Title: ")
    imdb_id = get_input_validated("2. IMDb ID (ttXXXXXXX): ")
    
    cat = get_input_validated(f"3. Category ({'/'.join(VALID_CATEGORIES)}): ", VALID_CATEGORIES).lower()
        
    quality = input("4. Quality (e.g., 4K/HDR/720p - खाली छोड़ सकते हैं): ").strip()
    thumb = input("5. Thumbnail/Poster URL (link): ").strip()
    year = input(f"6. Year ({time.strftime('%Y')} default): ").strip() or str(time.strftime("%Y"))

    # 2. स्ट्रीम सर्वर लिंक
    servers = []
    print("\n--- ðŸŽ¥ Stream Servers (Watch Online) ---")
    while True:
        server_name = input("   Server Name (e.g., Server 1 / Trailer, or type 'done'): ").strip()
        if server_name.lower() == 'done':
            break
        if not server_name: continue # खाली इनपुट को छोड़ दें
        server_link = input(f"   URL for {server_name}: ").strip()
        if server_link:
            servers.append({"name": server_name, "link": server_link})

    # 3. डाउनलोड लिंक (GB/MB के साथ)
    downloads = {}
    print("\n--- ðŸ”¥ Download Links (Custom Label & Link) ---")
    q_count = 1
    while True:
        label = input(f"   Link {q_count} Label (e.g., 1080p - 3.5GB, or type 'done'): ").strip()
        if label.lower() == 'done':
            break
        if not label: continue # खाली इनपुट को छोड़ दें
        link = input(f"   URL for {label}: ").strip()
        
        if link:
            downloads[f"q{q_count}"] = {"label": label, "link": link}
            q_count += 1
        else:
            print("   âš ï¸ URL खाली नहीं छोड़ा जा सकता, दोबारा कोशिश करें।")

    new_movie = {
        "title": title,
        "imdb_id": imdb_id,
        "thumb": thumb,
        "cat": cat,
        "quality": quality if quality else "HD", 
        "year": year, 
        "servers": servers,
        "downloads": downloads
    }
    return new_movie

def update_json_file(new_movie):
    """JSON फ़ाइल को पढ़ता है, नया डेटा जोड़ता है, और वापस लिखता है।"""
    
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    
    movie_list = []
    if os.path.exists(DATA_FILE) and os.path.getsize(DATA_FILE) > 0:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            try:
                movie_list = json.load(f)
            except json.JSONDecodeError:
                print(f"Warning: {DATA_FILE} is empty or corrupted. Starting fresh.")
                movie_list = []
    
    movie_list.insert(0, new_movie) 
    
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(movie_list, f, indent=2, ensure_ascii=False)
    
    print(f"\n\n\n✅ SUCCESS: '{new_movie['title']}' added to {DATA_FILE}\n")

if __name__ == "__main__":
    movie_data = get_new_movie_data()
    update_json_file(movie_data)

    print("\n--- ðŸš€ PUSH TO GITHUB (Run these 3 commands) ---")
    print("1. git add .")
    print(f"2. git commit -m 'feat: Added {movie_data['title']} ({movie_data['year']})'")
    print("3. git push origin main")
    print("------------------------------------------------")
