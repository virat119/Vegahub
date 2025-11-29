import json
import os
import time

# सुनिश्चित करें कि यह पथ सही है: आपके GitHub Repo की रूट से 'data/' फ़ोल्डर में।
DATA_FILE = 'data/movies.json' 

def get_new_movie_data():
    """यूज़र से सभी आवश्यक मूवी डिटेल्स प्रॉम्प्ट करता है।"""
    print("\n--- New Movie Details ---")
    
    # 1. मुख्य डिटेल्स
    title = input("1. Title: ")
    imdb_id = input("2. IMDb ID (e.g., tt1234567): ")
    cat_options = ["bollywood", "hollywood", "south", "web"]
    cat = input(f"3. Category ({'/'.join(cat_options)}): ").lower()
    while cat not in cat_options:
        cat = input(f"Invalid category. Choose from ({'/'.join(cat_options)}): ").lower()
        
    quality = input("4. Quality (HD/4K/720p etc.): ")
    thumb = input("5. Thumbnail/Poster URL (e.g., https://i.imgur.com/image.jpg): ")
    year = input(f"6. Year ({time.strftime('%Y')} default): ") or str(time.strftime("%Y"))

    # 2. स्ट्रीम सर्वर लिंक
    servers = []
    print("\n--- Stream Servers (Watch Online) ---")
    while True:
        server_name = input("Server Name (e.g., Server 1 / Trailer, or type 'done'): ")
        if server_name.lower() == 'done':
            break
        server_link = input(f"Server URL for {server_name}: ")
        servers.append({"name": server_name, "link": server_link})

    # 3. डाउनलोड लिंक (GB/MB के साथ)
    downloads = {}
    print("\n--- Download Links (Custom Label & Link) ---")
    q_count = 1
    while True:
        label = input(f"Link {q_count} Label (e.g., 720p - 1.5GB, or type 'done'): ")
        if label.lower() == 'done':
            break
        link = input(f"Link {q_count} URL (Google Drive etc.): ")
        
        # 'q1', 'q2', 'q3' key का उपयोग करें
        downloads[f"q{q_count}"] = {"label": label, "link": link}
        q_count += 1

    new_movie = {
        "title": title,
        "imdb_id": imdb_id,
        "thumb": thumb,
        "cat": cat,
        "quality": quality,
        "year": year, 
        "servers": servers,
        "downloads": downloads
    }
    return new_movie

def update_json_file(new_movie):
    """JSON फ़ाइल को पढ़ता है, नया डेटा जोड़ता है, और वापस लिखता है।"""
    
    # सुनिश्चित करें कि data/ फ़ोल्डर मौजूद है 
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    
    # फाइल को पढ़ने के लिए (r)
    movie_list = []
    if os.path.exists(DATA_FILE) and os.path.getsize(DATA_FILE) > 0:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            try:
                # मौजूदा JSON डेटा को लिस्ट में लोड करें
                movie_list = json.load(f)
            except json.JSONDecodeError:
                print(f"Warning: {DATA_FILE} is empty or corrupted. Starting fresh.")
                movie_list = []
    
    # सबसे ऊपर नई मूवी जोड़ें (index 0 पर)
    movie_list.insert(0, new_movie) 
    
    # फाइल को वापस लिखने के लिए (w)
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        # JSON को इंडेंट=2 के साथ सेव करें (पढ़ने में आसान)
        json.dump(movie_list, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ SUCCESS: '{new_movie['title']}' added to {DATA_FILE}")

if __name__ == "__main__":
    movie_data = get_new_movie_data()
    update_json_file(movie_data)

    print("\n--- Next Steps in Termux ---")
    print("1. Commit changes: git add .")
    print("2. Commit changes: git commit -m 'Added new movie: {0}'".format(movie_data['title']))
    print("3. Push to GitHub: git push origin main")
    print("----------------------------")
