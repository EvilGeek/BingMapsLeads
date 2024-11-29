import requests, urllib3, re, json
from bs4 import BeautifulSoup

urllib3.disable_warnings()

def remove_html_tags(text: str) -> str:
    return re.sub(r'<[^>]+>', '', text) if isinstance(text, str) else text

def clean_data(data):
    if isinstance(data, dict):
        return {key: clean_data(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [clean_data(item) for item in data]
    elif isinstance(data, str):
        return remove_html_tags(data)
    else:
        return data


def _search(query="restaurants in Chicago"):
    URL = 'https://www.bing.com/maps/overlaybfpr?count=10000&q=' + query
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Upgrade-Insecure-Requests": "1",
        "DNT": "1",  # Do Not Track
    }
    try:
        resp = requests.get(URL, headers=HEADERS, verify=False)
        return resp.text if resp.status_code == 200 else None
    except Exception as e:
        print(e)


def extract_listings(html: str):
    soup = BeautifulSoup(html, "html.parser")
    listings = []

    for li in soup.find_all("li", {"data-priority": True}):
        a_tag = li.find("a", class_="listings-item")
        if a_tag and a_tag.has_attr("data-entity"):
            data_entity = a_tag["data-entity"]
            try:
                entity_data = json.loads(data_entity.replace('&quot;', '"'))  
                cleaned_data = clean_data(entity_data)
                listings.append(cleaned_data)
            except json.JSONDecodeError as e:
                continue

    return listings
