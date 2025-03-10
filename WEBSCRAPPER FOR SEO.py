import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urljoin, urlparse

def fetch_seo_data(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "html.parser")

        title = soup.title.string if soup.title else "N/A"
        meta_desc = soup.find("meta", attrs={"name": "description"})
        meta_desc = meta_desc["content"] if meta_desc else "N/A"

        meta_keywords = soup.find("meta", attrs={"name": "keywords"})
        meta_keywords = meta_keywords["content"] if meta_keywords else "N/A"

        headings = {f"H{i}": [h.text.strip() for h in soup.find_all(f"h{i}")] for i in range(1, 7)}

        internal_links, external_links = set(), set()
        for link in soup.find_all("a", href=True):
            href = link["href"]
            full_url = urljoin(url, href)
            if urlparse(full_url).netloc == urlparse(url).netloc:
                internal_links.add(full_url)
            else:
                external_links.add(full_url)

        return {
            "URL": url,
            "Title": title,
            "Meta Description": meta_desc,
            "Meta Keywords": meta_keywords,
            **headings,
            "Internal Links": list(internal_links),
            "External Links": list(external_links),
        }
    
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

def save_to_csv(data, filename="seo_data.csv"):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False, encoding="utf-8")
    print(f"Data saved to {filename}")

if __name__ == "__main__":
    urls = ["https://example.com", "https://anotherwebsite.com"]  # Add URLs here
    seo_results = [fetch_seo_data(url) for url in urls if fetch_seo_data(url)]
    save_to_csv(seo_results)
