import aiohttp
import asyncio
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from tqdm import tqdm

HEADERS = {"User-Agent": "Mozilla/5.0"}

async def fetch_url(session, url):
    """Fetches HTML content asynchronously."""
    try:
        async with session.get(url, headers=HEADERS, timeout=10) as response:
            response.raise_for_status()
            return await response.text()
    except Exception as e:
        print(f"Failed to fetch {url}: {e}")
        return None

def parse_html(url, html):
    """Parses HTML and extracts SEO data."""
    soup = BeautifulSoup(html, "html.parser")

    title = soup.title.string.strip() if soup.title else "N/A"

    def get_meta_content(name):
        tag = soup.find("meta", attrs={"name": name})
        return tag["content"].strip() if tag else "N/A"

    meta_desc = get_meta_content("description")
    meta_keywords = get_meta_content("keywords")

    # Extracting Open Graph & Twitter Card Data
    og_title = get_meta_content("og:title")
    og_desc = get_meta_content("og:description")
    twitter_title = get_meta_content("twitter:title")
    twitter_desc = get_meta_content("twitter:description")

    # Extract Canonical URL
    canonical_tag = soup.find("link", rel="canonical")
    canonical_url = canonical_tag["href"].strip() if canonical_tag else url

    # Extract Headings
    headings = {f"H{i}": [h.get_text(strip=True) for h in soup.find_all(f"h{i}")] for i in range(1, 7)}

    # Extract Links
    internal_links, external_links = set(), set()
    for link in soup.find_all("a", href=True):
        href = link["href"].strip()
        full_url = urljoin(url, href)
        (internal_links if urlparse(full_url).netloc == urlparse(url).netloc else external_links).add(full_url)

    return {
        "URL": url,
        "Canonical URL": canonical_url,
        "Title": title,
        "Meta Description": meta_desc,
        "Meta Keywords": meta_keywords,
        "OG Title": og_title,
        "OG Description": og_desc,
        "Twitter Title": twitter_title,
        "Twitter Description": twitter_desc,
        **headings,
        "Internal Links": list(internal_links),
        "External Links": list(external_links),
    }

async def fetch_seo_data(urls):
    """Fetches SEO data for multiple URLs asynchronously."""
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_url(session, url) for url in urls]
        responses = await asyncio.gather(*tasks)

    return [parse_html(url, html) for url, html in zip(urls, responses) if html]

def save_to_csv(data, filename="seo_data.csv"):
    """Saves the extracted data to a CSV file."""
    if not data:
        print("No data to save.")
        return

    df = pd.DataFrame(data)
    df.to_csv(filename, index=False, encoding="utf-8")
    print(f"Data saved to {filename}")

if __name__ == "__main__":
    urls = ["https://example.com", "https://anotherwebsite.com"]  # Add URLs here
    seo_results = asyncio.run(fetch_seo_data(urls))
    save_to_csv(seo_results)
