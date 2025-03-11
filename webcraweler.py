import requests
from bs4 import BeautifulSoup
import csv
import time
from urllib.parse import urljoin, urlparse

# Initialize variables
visited_urls = set()
csv_filename = "crawled_data.csv"
session = requests.Session()  # Persistent session for efficiency
session.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})  # Imitate a browser

def crawl(url, depth=2):
    if depth == 0 or url in visited_urls:
        return
    
    try:
        response = session.get(url, timeout=5)
        response.raise_for_status()
    except requests.RequestException:
        return

    visited_urls.add(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Extract title and all valid links
    title = soup.title.string.strip() if soup.title else "No Title"
    base_url = "{0.scheme}://{0.netloc}".format(urlparse(url))  # Base domain
    links = set(urljoin(base_url, a['href']) for a in soup.find_all('a', href=True) if is_valid_url(a['href'], base_url))

    # Save to CSV
    save_to_csv([url, title])

    # Crawl next links
    for link in links:
        crawl(link, depth - 1)
        time.sleep(1)  # Avoid excessive requests

def is_valid_url(link, base_url):
    """Ensure the link is absolute and within the same domain."""
    parsed_link = urlparse(urljoin(base_url, link))
    return parsed_link.scheme in {"http", "https"} and parsed_link.netloc != ""

def save_to_csv(data):
    """Append data to CSV file."""
    with open(csv_filename, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(data)

# Start crawling
start_url = "https://example.com"
crawl(start_url)
print("Crawling finished. Data saved in", csv_filename)
